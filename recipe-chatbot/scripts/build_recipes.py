"""Build data/my_recipes.json from the links in data/recipe_links.txt.

Re-run this whenever you change the links file:

    uv run python scripts/build_recipes.py

For each link it:
1. downloads the page,
2. reads the schema.org Recipe card (JSON-LD) if the page has one,
   otherwise falls back to the visible page text,
3. asks the model set in .env (MODEL_NAME, via litellm) to turn that into a
   clean English recipe, keeping the original dish name,
4. skips (and reports) any link that fails.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import warnings
from html.parser import HTMLParser
from pathlib import Path

import httpx
import litellm  # type: ignore
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LINKS_FILE = PROJECT_ROOT / "data" / "recipe_links.txt"
OUTPUT_FILE = PROJECT_ROOT / "data" / "my_recipes.json"

load_dotenv(PROJECT_ROOT / ".env", override=False)
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
litellm.suppress_debug_info = True  # keep litellm's help banners out of the output
# litellm + pydantic print a harmless serializer warning on every call; hide it.
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
MAX_TAG_CHARS = 60  # longer "tags" are sentences, not tags

MAX_ATTEMPTS = 4  # per link, for temporary model/API errors
MAX_PAGE_TEXT_CHARS = 20_000  # enough for a recipe article, keeps the prompt small
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    ),
    "Accept-Language": "en,fr;q=0.8",
}


# -----------------------------------------------------------------------------
# Page parsing
# -----------------------------------------------------------------------------

class _PageParser(HTMLParser):
    """Collects JSON-LD blocks and the visible text of a page."""

    SKIP_TAGS = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form", "iframe"}
    BLOCK_TAGS = {"p", "div", "li", "br", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "section", "article"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.json_ld: list[str] = []
        self.text_parts: list[str] = []
        self._skip_depth = 0
        self._in_json_ld = False
        self._json_buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type", "").lower() == "application/ld+json":
            self._in_json_ld = True
            self._json_buf = []
            return
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        elif tag in self.BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if self._in_json_ld and tag == "script":
            self.json_ld.append("".join(self._json_buf))
            self._in_json_ld = False
            return
        if tag in self.SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in self.BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_data(self, data):
        if self._in_json_ld:
            self._json_buf.append(data)
        elif self._skip_depth == 0:
            self.text_parts.append(data)

    def visible_text(self) -> str:
        text = "".join(self.text_parts)
        lines = [re.sub(r"[ \t\xa0]+", " ", line).strip() for line in text.splitlines()]
        return "\n".join(line for line in lines if line)


def _is_recipe(node: dict) -> bool:
    node_type = node.get("@type")
    types = node_type if isinstance(node_type, list) else [node_type]
    return "Recipe" in types


def _find_recipe(data) -> dict | None:
    """Walk a JSON-LD structure (dicts, lists, @graph) and return the first Recipe."""
    if isinstance(data, list):
        for item in data:
            found = _find_recipe(item)
            if found:
                return found
    elif isinstance(data, dict):
        if _is_recipe(data):
            return data
        for key in ("@graph", "mainEntity", "itemListElement"):
            if key in data:
                found = _find_recipe(data[key])
                if found:
                    return found
    return None


def extract_recipe_card(json_ld_blocks: list[str]) -> dict | None:
    for block in json_ld_blocks:
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError:
            continue
        recipe = _find_recipe(data)
        if recipe:
            return recipe
    return None


def iso_duration_to_minutes(value) -> int | None:
    """'PT1H30M' -> 90. Returns None if it can't be parsed or is zero."""
    if not isinstance(value, str):
        return None
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value.strip().upper())
    if not m:
        return None
    days, hours, mins, _ = (int(x) if x else 0 for x in m.groups())
    total = days * 1440 + hours * 60 + mins
    return total or None


def card_minutes(card: dict) -> int | None:
    total = iso_duration_to_minutes(card.get("totalTime"))
    if total:
        return total
    prep = iso_duration_to_minutes(card.get("prepTime")) or 0
    cook = iso_duration_to_minutes(card.get("cookTime")) or 0
    return (prep + cook) or None


# -----------------------------------------------------------------------------
# LLM step: normalise + translate
# -----------------------------------------------------------------------------

PROMPT = """You turn a recipe from a web page into clean English JSON for a recipe database.

Return ONLY a JSON object with exactly these keys:
- "name": the dish's short ORIGINAL name only, as the source spells it, with the first letter capitalised (e.g. "Chorba frik", "Mderbel", "Maadnoussia", "Tajine zitoune"). Do not translate it. If the title pairs a traditional name with a generic description (e.g. "Maadnoussia : tajine viande hachée et persil", "gâteau algérien à la confiture / mderbel"), keep only the traditional name; if there is no traditional name, use the source's short dish title. Drop filler like "recipe", "easy", "homemade", "gâteau algérien", subtitles after ":" or "/", and any site name.
- "description": 1-3 sentences in English describing the dish.
- "ingredients": list of strings in English, one ingredient per item, with quantities as given.
- "steps": list of strings in English, one step per item, in order.
- "tags": list of short lowercase strings: cuisine/region, course, main ingredients, diet (in English), AND the original-language name of the dish, the source's full original title or descriptive name, plus common alternate spellings/transliterations (e.g. "chorba frik", "chorba frick", "jari frik", "chorba"). Omit duplicates.
- "minutes": total time in minutes as a number if the page states it (or it can be reliably summed from stated times), otherwise null.

If the source is not in English, translate description, ingredients and steps to English.
Use only information from the source; do not invent ingredients or steps.
If the source does not contain a recipe, return {{"error": "no recipe found"}}.

Source URL: {url}
Source ({kind}):
{content}
"""


def _parse_json_reply(text: str) -> dict:
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("model did not return JSON")
    return json.loads(text[start : end + 1])


class NoRecipeError(Exception):
    """The model looked at the page and found no recipe (not worth retrying)."""


def normalise_with_llm(url: str, kind: str, content: str) -> dict:
    """Call the model, retrying temporary failures (overloaded API, network blips)."""
    last_exc: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            completion = litellm.completion(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": PROMPT.format(url=url, kind=kind, content=content)}],
                temperature=0,
            )
            reply = completion["choices"][0]["message"]["content"] or ""
            data = _parse_json_reply(reply)
            if "error" in data:
                raise NoRecipeError(data["error"])
            return data
        except NoRecipeError:
            raise
        except Exception as exc:
            last_exc = exc
            if attempt < MAX_ATTEMPTS:
                wait = 5 * attempt
                print(f"    model call failed ({type(exc).__name__}), retrying in {wait}s...")
                time.sleep(wait)
    assert last_exc is not None
    raise last_exc


def _str_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(v).strip() for v in value if str(v).strip()]


def build_recipe(url: str, client: httpx.Client) -> dict:
    response = client.get(url)
    response.raise_for_status()

    parser = _PageParser()
    parser.feed(response.text)
    card = extract_recipe_card(parser.json_ld)

    if card:
        kind = "schema.org Recipe card, JSON"
        content = json.dumps(card, ensure_ascii=False)[:MAX_PAGE_TEXT_CHARS]
    else:
        kind = "page text, no recipe card found"
        content = parser.visible_text()[:MAX_PAGE_TEXT_CHARS]
        if len(content) < 200:
            raise ValueError("page has no recipe card and almost no text")

    data = normalise_with_llm(url, kind, content)

    name = str(data.get("name") or "").strip()
    ingredients = _str_list(data.get("ingredients"))
    steps = _str_list(data.get("steps"))
    if not name or not ingredients or not steps:
        raise ValueError("model output is missing a name, ingredients or steps")

    minutes = card_minutes(card) if card else None
    if minutes is None and isinstance(data.get("minutes"), (int, float)) and data["minutes"] > 0:
        minutes = int(data["minutes"])

    tags: list[str] = []
    for tag in _str_list(data.get("tags")):
        tag = tag.lower()
        if len(tag) <= MAX_TAG_CHARS and tag not in tags:
            tags.append(tag)

    return {
        "name": name,
        "description": str(data.get("description") or "").strip(),
        "ingredients": ingredients,
        "steps": steps,
        "tags": tags,
        "minutes": minutes,
        "source_url": url,
    }


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def read_links() -> list[str]:
    links = []
    for line in LINKS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and line not in links:
            links.append(line)
    return links


def main() -> int:
    if not LINKS_FILE.exists():
        print(f"Links file not found: {LINKS_FILE}")
        return 1

    links = read_links()
    print(f"Model: {MODEL_NAME}")
    print(f"Reading {len(links)} links from {LINKS_FILE.relative_to(PROJECT_ROOT)}\n")

    recipes: list[dict] = []
    failed: list[tuple[str, str]] = []

    with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=30) as client:
        for i, url in enumerate(links, start=1):
            print(f"[{i}/{len(links)}] {url}")
            try:
                recipe = build_recipe(url, client)
            except Exception as exc:  # skip this link, keep going
                reason = f"{type(exc).__name__}: {exc}"
                # Never echo anything that could contain the API key.
                reason = reason.splitlines()[0][:200]
                print(f"    SKIPPED - {reason}")
                failed.append((url, reason))
                continue
            recipe = {"id": len(recipes) + 1, **recipe}
            recipes.append(recipe)
            print(f"    ok - {recipe['name']}")

    OUTPUT_FILE.write_text(json.dumps(recipes, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nSaved {len(recipes)} recipes to {OUTPUT_FILE.relative_to(PROJECT_ROOT)}:")
    for r in recipes:
        print(f"  {r['id']}. {r['name']}")
    if failed:
        print(f"\nSkipped {len(failed)} link(s):")
        for url, reason in failed:
            print(f"  - {url}\n      {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
