#!/usr/bin/env python3
"""
Search test page for stage 7, step 3.

Runs the real search in recipe-chatbot/backend/retrieval.py on your
recipe-chatbot/data/my_recipes.json, so what you see here is what the bot will get.

Start it from this folder:
    uv run --project "../../../../recipe-chatbot" python search_app.py
then open http://localhost:5002 . Stop it with Ctrl+C.

If you rebuild my_recipes.json, just search again: the page picks up the new file.
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
CHATBOT = (HERE / ".." / ".." / ".." / ".." / "recipe-chatbot").resolve()
PORT = 5002

if not (CHATBOT / "backend" / "retrieval.py").exists():
    sys.exit(
        f"Can't find recipe-chatbot at {CHATBOT}.\n"
        "Keep 'learn eval by doing' and 'recipe-chatbot' side by side in the same folder."
    )
sys.path.insert(0, str(CHATBOT))

from backend.retrieval import DEFAULT_RECIPES_PATH, create_retriever  # noqa: E402

_retriever = None
_loaded_mtime = None


def get_retriever():
    """Build the search once, and again whenever my_recipes.json changes."""
    global _retriever, _loaded_mtime
    mtime = DEFAULT_RECIPES_PATH.stat().st_mtime
    if _retriever is None or mtime != _loaded_mtime:
        _retriever = create_retriever(DEFAULT_RECIPES_PATH, verbose=False)
        _loaded_mtime = mtime
    return _retriever


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status, payload):
        self._send(status, json.dumps(payload, ensure_ascii=False), "application/json; charset=utf-8")

    def do_GET(self):
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            self._send(200, (HERE / "search.html").read_text(encoding="utf-8"), "text/html; charset=utf-8")
            return

        if not DEFAULT_RECIPES_PATH.exists():
            self._json(404, {"error": f"No recipe file yet at {DEFAULT_RECIPES_PATH}. "
                                      "Build it with: uv run python scripts/build_recipes.py"})
            return

        if url.path == "/api/info":
            retriever = get_retriever()
            self._json(200, {"recipes_file": str(DEFAULT_RECIPES_PATH), "stats": retriever.get_stats()})
            return

        if url.path == "/api/search":
            question = parse_qs(url.query).get("q", [""])[0].strip()
            retriever = get_retriever()
            results = retriever.retrieve_bm25(question) if question else []
            words = retriever.preprocess_text(question)
            recipe_words = [set(retriever.preprocess_text(retriever.recipe_text(r))) for r in retriever.recipes]
            self._json(200, {
                "question": question,
                "words": [{"word": w, "in_recipes": sum(w in rw for rw in recipe_words)} for w in dict.fromkeys(words)],
                "total_recipes": len(retriever.recipes),
                "results_per_search": retriever.default_top_k(),
                "results": results,
            })
            return

        self._json(404, {"error": "Not found"})

    def log_message(self, format, *args):
        pass  # keep the terminal quiet


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Search test page: http://localhost:{PORT}")
    print(f"Recipes: {DEFAULT_RECIPES_PATH}")
    print("Stop with Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")


if __name__ == "__main__":
    main()
