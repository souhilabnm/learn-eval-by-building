# Stage 6: answer from your own recipes

Two apps: a viewer to check your recipe file, and a local page to try the search on it.


## recipes-viewer.html (your recipes, before search)

Shows one recipe at a time: name, description, time, ingredients, numbered steps, tags and a link to the source page. The top bar counts recipes, how many have a cooking time, and how many miss a name, ingredients or steps; each recipe lists any missing field in red.

1. Put one recipe link per line in `recipe-chatbot\data\recipe_links.txt`.
2. In `recipe-chatbot`, run `uv run python scripts/build_recipes.py`. It saves `recipe-chatbot\data\my_recipes.json` and names any link it skipped.

Adapted from the course's HW4 query viewer in [ai-evals-course/recipe-chatbot](https://github.com/ai-evals-course/recipe-chatbot).


## search-app (your search, step 3)

Type a question and see which recipes the bot's search would hand over, before the chat is involved (the Question → Context check). It runs the real search in `recipe-chatbot\backend\retrieval.py` (BM25 keyword search) on `recipe-chatbot\data\my_recipes.json`, so what you see is what the bot will get. Fewer than 20 recipes: top 4. 20 or more: top 5.

1. Open a terminal in this folder's `search-app` folder.
2. Run `uv run --project "../../../../recipe-chatbot" python search_app.py`
3. Open http://localhost:5002 . Stop it with Ctrl+C.

For each question you see:
- **Words searched:** each word of your question and how many recipes contain it. Rare words (green) count a lot, common ones (grey) little, words in no recipe (red) nothing.
- **Results:** ranked, with the BM25 score, a bar next to the top score, the words that matched, and the full recipe on click with the matched words highlighted. Scores are not percentages: compare them within one question only.

The same search works without the page: in `recipe-chatbot`, `uv run python backend/retrieval.py "your question"`.

