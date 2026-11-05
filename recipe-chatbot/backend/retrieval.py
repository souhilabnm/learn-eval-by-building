#!/usr/bin/env python3
"""
BM25 recipe search (stage 6, step 3).

Searches your own recipes in data/my_recipes.json with BM25 keyword search
and returns the best matches, best first.

BM25 is keyword (lexical) search: it matches words, not meaning.
"olive" and "olives" are different words to it, and so are "tajine" and "tagine".

How many results:
    fewer than 20 recipes -> top 4
    20 recipes or more    -> top 5

Try it on its own (search only, the chat is not involved):
    uv run python backend/retrieval.py "How do I make tajine zitoune?"
    uv run python backend/retrieval.py            (runs a few example questions)

Or use the search test page:
    learn eval by doing/useful apps/stage-6-evaluate-the-parts/search-app/

Adapted from the course's HW4 retrieval engine (same BM25, same text cleaning).
It can still search the HW4 recipes: create_retriever(<path to processed_recipes.json>).
"""

import json
import pickle
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from rank_bm25 import BM25Okapi

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RECIPES_PATH = PROJECT_ROOT / "data" / "my_recipes.json"

# Fields that are searched. Each recipe is one search unit ("one recipe = one chunk"),
# so ingredients and steps are never separated.
SEARCH_FIELDS = ["name", "description", "ingredients", "steps", "tags"]


def results_count(recipe_count: int) -> int:
    """How many recipes search returns: top 4 under 20 recipes, top 5 from 20 up."""
    return 4 if recipe_count < 20 else 5


def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(str(item) for item in value if item)
    return str(value or "")


class RecipeRetriever:
    """BM25 search over a list of recipes."""

    def __init__(self, verbose: bool = True):
        self.recipes: List[Dict[str, Any]] = []
        self.bm25_index: Optional[BM25Okapi] = None
        self.recipe_id_to_index: Dict[Any, int] = {}
        self.index_to_recipe_id: Dict[int, Any] = {}
        self.is_indexed = False
        self.verbose = verbose

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message)

    def preprocess_text(self, text: str) -> List[str]:
        """Lowercase, replace punctuation with spaces, split into words."""
        if not text:
            return []
        text = re.sub(r"[^\w\s]", " ", text.lower())
        return [token for token in text.split() if token]

    def recipe_text(self, recipe: Dict[str, Any]) -> str:
        """All searchable text of one recipe, joined."""
        return " ".join(filter(None, (_as_text(recipe.get(field)) for field in SEARCH_FIELDS)))

    def load_recipes(self, recipes_path: Path) -> None:
        """Load recipes from a JSON file (a list of recipes, each with an id)."""
        self._log(f"Loading recipes from {recipes_path}")
        with open(recipes_path, "r", encoding="utf-8") as file:
            self.recipes = json.load(file)

        self.recipe_id_to_index = {}
        self.index_to_recipe_id = {}
        for idx, recipe in enumerate(self.recipes):
            recipe_id = recipe.get("id", idx)
            self.recipe_id_to_index[recipe_id] = idx
            self.index_to_recipe_id[idx] = recipe_id

        self._log(f"Loaded {len(self.recipes)} recipes")

    def build_index(self) -> None:
        """Build the BM25 index: one list of words per recipe."""
        if not self.recipes:
            raise ValueError("No recipes loaded. Call load_recipes() first.")
        documents = [self.preprocess_text(self.recipe_text(recipe)) for recipe in self.recipes]
        self.bm25_index = BM25Okapi(documents)
        self.is_indexed = True
        self._log(f"BM25 index built for {len(documents)} recipes")

    def save_index(self, index_path: Path) -> None:
        """Save the index to disk (only useful for large recipe sets like HW4's)."""
        if not self.is_indexed:
            raise ValueError("No index to save. Call build_index() first.")
        index_data = {
            "bm25_index": self.bm25_index,
            "recipe_id_to_index": self.recipe_id_to_index,
            "index_to_recipe_id": self.index_to_recipe_id,
        }
        with open(index_path, "wb") as file:
            pickle.dump(index_data, file)
        self._log(f"Index saved to {index_path}")

    def load_index(self, index_path: Path) -> None:
        """Load an index saved with save_index (only load files you made yourself)."""
        self._log(f"Loading BM25 index from {index_path}")
        with open(index_path, "rb") as file:
            index_data = pickle.load(file)
        self.bm25_index = index_data["bm25_index"]
        self.recipe_id_to_index = index_data["recipe_id_to_index"]
        self.index_to_recipe_id = index_data["index_to_recipe_id"]
        self.is_indexed = True

    def default_top_k(self) -> int:
        return results_count(len(self.recipes))

    def retrieve_bm25(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Return the best-matching recipes for a question, best first.

        Each result is the full recipe plus:
            bm25_score  - the BM25 score (not a percentage; only compare within one question)
            rank        - 1 for the best match
            matched_words - the question's words found in this recipe
        top_k defaults to results_count() (4 under 20 recipes, 5 from 20 up).
        """
        if not self.is_indexed:
            raise ValueError("Index not built. Call build_index() or load_index() first.")
        if top_k is None:
            top_k = self.default_top_k()

        query_tokens = self.preprocess_text(query)
        if not query_tokens:
            return []

        scores = self.bm25_index.get_scores(query_tokens)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in top_indices:
            recipe = dict(self.recipes[idx])
            recipe_words = set(self.preprocess_text(self.recipe_text(recipe)))
            recipe["bm25_score"] = float(scores[idx])
            recipe["rank"] = len(results) + 1
            recipe["matched_words"] = sorted({word for word in query_tokens if word in recipe_words})
            results.append(recipe)
        return results

    def search_by_recipe_id(self, recipe_id: Any) -> Optional[Dict[str, Any]]:
        """Get one recipe by its id."""
        idx = self.recipe_id_to_index.get(recipe_id)
        return self.recipes[idx] if idx is not None else None

    def get_recipe_rank(self, query: str, target_recipe_id: Any, top_k: int = 100) -> Optional[int]:
        """Where a given recipe lands for a question (1 = first), or None if not in top_k."""
        for result in self.retrieve_bm25(query, top_k=top_k):
            if result.get("id") == target_recipe_id:
                return result["rank"]
        return None

    def get_stats(self) -> Dict[str, Any]:
        """Counts about the loaded recipes."""
        if not self.recipes:
            return {"error": "No recipes loaded"}
        count = len(self.recipes)
        timed = [r["minutes"] for r in self.recipes if isinstance(r.get("minutes"), (int, float)) and r["minutes"] > 0]
        return {
            "total_recipes": count,
            "indexed": self.is_indexed,
            "results_per_search": results_count(count),
            "avg_ingredients": round(sum(len(r.get("ingredients") or []) for r in self.recipes) / count, 1),
            "avg_steps": round(sum(len(r.get("steps") or []) for r in self.recipes) / count, 1),
            "avg_cooking_time": round(sum(timed) / len(timed), 1) if timed else None,
        }


def create_retriever(
    recipes_path: Path = DEFAULT_RECIPES_PATH,
    index_path: Optional[Path] = None,
    rebuild_index: bool = False,
    verbose: bool = True,
) -> RecipeRetriever:
    """Load recipes and build (or load) the BM25 index. Defaults to data/my_recipes.json."""
    retriever = RecipeRetriever(verbose=verbose)
    retriever.load_recipes(Path(recipes_path))
    if index_path and Path(index_path).exists() and not rebuild_index:
        try:
            retriever.load_index(Path(index_path))
            return retriever
        except Exception as error:
            retriever._log(f"Failed to load index ({error}), building a new one")
    retriever.build_index()
    if index_path:
        retriever.save_index(Path(index_path))
    return retriever


_default_retriever: Optional[RecipeRetriever] = None


def search(query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
    """Search data/my_recipes.json. The index is built once, on first use."""
    global _default_retriever
    if _default_retriever is None:
        _default_retriever = create_retriever(DEFAULT_RECIPES_PATH, verbose=False)
    return _default_retriever.retrieve_bm25(query, top_k=top_k)


def retrieve_bm25(query: str, corpus: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """Kept from HW4: search a list of recipes passed in directly (rebuilds the index each call)."""
    retriever = RecipeRetriever(verbose=False)
    retriever.recipes = corpus
    for idx, recipe in enumerate(corpus):
        recipe_id = recipe.get("id", idx)
        retriever.recipe_id_to_index[recipe_id] = idx
        retriever.index_to_recipe_id[idx] = recipe_id
    retriever.build_index()
    return retriever.retrieve_bm25(query, top_k=top_n)


def _print_results(question: str, results: List[Dict[str, Any]]) -> None:
    print(f"\nQuestion: {question}")
    if not results:
        print("  (no searchable words in the question)")
        return
    for recipe in results:
        words = ", ".join(recipe["matched_words"]) or "none"
        print(f"  {recipe['rank']}. {recipe.get('name', '?')}  (id {recipe.get('id')}, score {recipe['bm25_score']:.2f}, matched: {words})")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if not DEFAULT_RECIPES_PATH.exists():
        print(f"Recipes file not found: {DEFAULT_RECIPES_PATH}")
        print("Build it first: uv run python scripts/build_recipes.py")
        return

    retriever = create_retriever(DEFAULT_RECIPES_PATH)
    print("\n--- Your recipes ---")
    for key, value in retriever.get_stats().items():
        print(f"{key}: {value}")

    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else [
        "How do I make tajine zitoune?",
        "a soup with cracked wheat and lamb",
        "Give me a couscous recipe",
    ]
    for question in questions:
        _print_results(question, retriever.retrieve_bm25(question))


if __name__ == "__main__":
    main()
