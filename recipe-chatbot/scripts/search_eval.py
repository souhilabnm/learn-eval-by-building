"""Score your recipe search with Recall@k and MRR (stage 6).

Reads your search test sheet (your copy of template-06-search-test.csv),
runs every question through the real search in backend/retrieval.py,
fills the in_results and rank columns, and prints:

    Recall@1   right recipe ranked 1st
    Recall@k   right recipe in the results the bot gets (k = 4 under 20 recipes, 5 from 20 up)
    MRR        average of 1 / rank (1st = 1, 2nd = 0.5, 3rd = 0.33, not found = 0)

per kind of question (exact, vague) and overall. "not in data" questions have no
right recipe, so they are left out of the scores: judge their answers yourself.

Your own columns (uses_only_found_recipes, correct, notes) are never changed.
Each run is also saved to results/search_eval_<time>.json, to compare runs after a fix.

Usage (in recipe-chatbot):
    uv run python scripts/search_eval.py
    uv run python scripts/search_eval.py --sheet path/to/your-search-test.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.retrieval import DEFAULT_RECIPES_PATH, create_retriever  # noqa: E402

DEFAULT_SHEET = PROJECT_ROOT / "data" / "my_search_test.csv"
RESULTS_DIR = PROJECT_ROOT / "results"

KINDS = ["exact", "vague"]
NOT_IN_DATA = "not in data"
# Older sheets used in_top_3 / in_top_4; any of these is filled.
RESULT_COLUMNS = ["in_results", "in_top_4", "in_top_5", "in_top_3"]


def short(name: str) -> str:
    """Column name without its hint: 'kind (exact / vague / not in data)' -> 'kind'."""
    return name.split("(")[0].strip().lower()


def read_sheet(path: Path):
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    reader = csv.DictReader(text.splitlines())
    return reader.fieldnames or [], list(reader)


def find_column(fieldnames: List[str], *names: str) -> Optional[str]:
    for wanted in names:
        for field in fieldnames:
            if short(field) == wanted:
                return field
    return None


def parse_kind(value: str) -> str:
    value = (value or "").strip().lower().replace("-", " ").replace("_", " ")
    if "not" in value:
        return NOT_IN_DATA
    if value.startswith("vag"):
        return "vague"
    if value.startswith("exa"):
        return "exact"
    return value


def parse_id(value: str):
    value = (value or "").strip()
    if not value or value.lower() in {"none", "n/a", "-"} or value.startswith("("):
        return None
    try:
        return int(value)
    except ValueError:
        return value


def scores(rows: List[Dict], k: int) -> Dict:
    n = len(rows)
    if not n:
        return {"questions": 0, "recall_at_1": None, f"recall_at_{k}": None, "mrr": None}
    return {
        "questions": n,
        "recall_at_1": sum(r["rank"] == 1 for r in rows) / n,
        f"recall_at_{k}": sum(r["rank"] is not None for r in rows) / n,
        "mrr": sum(1 / r["rank"] for r in rows if r["rank"]) / n,
    }


def pct(value: Optional[float]) -> str:
    return "  -  " if value is None else f"{value * 100:4.0f}%"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Score your recipe search with Recall@k and MRR.")
    parser.add_argument("--sheet", type=Path, default=DEFAULT_SHEET, help="your search test CSV")
    args = parser.parse_args()
    sheet: Path = args.sheet

    if not sheet.exists():
        print(f"Test sheet not found: {sheet}")
        print("Copy learn eval by doing/templates/recipe-chatbot/template-06-search-test.csv")
        print(f"to {DEFAULT_SHEET} and write your questions in it (or pass --sheet).")
        sys.exit(1)
    if not DEFAULT_RECIPES_PATH.exists():
        print(f"Recipes not found: {DEFAULT_RECIPES_PATH}. Build them: uv run python scripts/build_recipes.py")
        sys.exit(1)

    fieldnames, rows = read_sheet(sheet)
    col_question = find_column(fieldnames, "question")
    col_kind = find_column(fieldnames, "kind")
    col_expected = find_column(fieldnames, "expected_recipe_id")
    col_in = find_column(fieldnames, *RESULT_COLUMNS)
    col_rank = find_column(fieldnames, "rank")
    missing = [n for n, c in [("question", col_question), ("kind", col_kind),
                              ("expected_recipe_id", col_expected), ("in_results", col_in), ("rank", col_rank)] if not c]
    if missing:
        print(f"The sheet is missing these columns: {', '.join(missing)}")
        print("Start from learn eval by doing/templates/recipe-chatbot/template-06-search-test.csv")
        sys.exit(1)

    retriever = create_retriever(DEFAULT_RECIPES_PATH, verbose=False)
    k = retriever.default_top_k()
    names = {r.get("id"): r.get("name") for r in retriever.recipes}

    scored: List[Dict] = []
    not_in_data: List[Dict] = []
    problems: List[str] = []

    for line, row in enumerate(rows, start=2):
        question = (row.get(col_question) or "").strip()
        if not question or question.lower().startswith("(example"):
            continue
        kind = parse_kind(row.get(col_kind, ""))
        expected = parse_id(row.get(col_expected, ""))
        results = retriever.retrieve_bm25(question)
        found = [r.get("id") for r in results]
        first = results[0] if results else None

        if kind == NOT_IN_DATA:
            row[col_in], row[col_rank] = "n/a", ""
            not_in_data.append({"line": line, "question": question,
                                "top_result": first.get("name") if first else None,
                                "top_score": round(first["bm25_score"], 2) if first else None})
            continue
        if kind not in KINDS:
            problems.append(f"line {line}: kind '{row.get(col_kind, '')}' should be exact, vague or not in data")
            continue
        if expected is None:
            problems.append(f"line {line}: no expected_recipe_id for '{question}'")
            continue
        if expected not in names:
            problems.append(f"line {line}: expected_recipe_id {expected} is not in my_recipes.json")
            continue

        rank = found.index(expected) + 1 if expected in found else None
        row[col_in], row[col_rank] = ("yes", str(rank)) if rank else ("no", "")
        scored.append({"line": line, "question": question, "kind": kind,
                       "expected_id": expected, "expected_name": names[expected], "rank": rank,
                       "results": [{"id": r.get("id"), "name": r.get("name"),
                                    "score": round(r["bm25_score"], 2)} for r in results]})

    # Write the two search columns back; everything else stays as you wrote it.
    try:
        with open(sheet, "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except PermissionError:
        print(f"Can't write to {sheet}: close it in Excel and run again.")
        sys.exit(1)

    summary = {kind: scores([r for r in scored if r["kind"] == kind], k) for kind in KINDS}
    summary["all"] = scores(scored, k)

    print(f"\nSearch scores for {sheet.name}  ({len(retriever.recipes)} recipes, the bot gets the top {k})\n")
    print(f"  {'':8} {'questions':>9}  {'Recall@1':>8}  {f'Recall@{k}':>8}  {'MRR':>5}")
    for label in KINDS + ["all"]:
        s = summary[label]
        mrr = "  -  " if s["mrr"] is None else f"{s['mrr']:.2f}"
        print(f"  {label:8} {s['questions']:>9}  {pct(s['recall_at_1']):>8}  {pct(s[f'recall_at_{k}']):>8}  {mrr:>5}")

    misses = [r for r in scored if r["rank"] != 1]
    if misses:
        print("\nNot ranked 1st:")
        for r in misses:
            where = f"rank {r['rank']}" if r["rank"] else f"not in top {k}"
            top = r["results"][0]["name"] if r["results"] else "nothing"
            print(f"  [{r['kind']}] {r['question']}\n      expected {r['expected_name']} ({where}); 1st was {top}")

    if not_in_data:
        print(f"\nNot in data ({len(not_in_data)}, not scored; search still returns {k} recipes, so judge the answers):")
        for r in not_in_data:
            print(f"  {r['question']}  -> 1st: {r['top_result']} (score {r['top_score']})")

    if problems:
        print("\nSkipped:")
        for p in problems:
            print(f"  {p}")

    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / f"search_eval_{dt.datetime.now():%Y%m%d_%H%M%S}.json"
    out.write_text(json.dumps({"sheet": str(sheet), "recipes": len(retriever.recipes), "k": k,
                               "summary": summary, "questions": scored, "not_in_data": not_in_data,
                               "skipped": problems}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFilled in_results and rank in {sheet.name}. Run saved to {out.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
