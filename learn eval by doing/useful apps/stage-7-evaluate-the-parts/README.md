# Stage 7: evaluate the parts

All three are read-only. Double-click to open, then click the file button and pick a file.

## search-queries-viewer.html (search, HW4)

Shows each search test question with the recipe it was written from and the key fact it asks about. Use it to check the questions make sense before scoring the search.

Open `recipe-chatbot\homeworks\hw4\reference_files\synthetic_queries.jsonl` (200 questions).

Copy of `recipe-chatbot/homeworks/hw4/reference_files/query_viewer.html`.

## recipes-viewer.html (your recipes, before search)

Shows one recipe at a time: name, description, time, ingredients, numbered steps, tags and a link to the source page. The top bar counts recipes, how many have a cooking time, and how many miss a name, ingredients or steps; each recipe lists any missing field in red.

1. Put one recipe link per line in `recipe-chatbot\data\recipe_links.txt`.
2. In `recipe-chatbot`, run `uv run python scripts/build_recipes.py`. It saves `recipe-chatbot\data\my_recipes.json` and names any link it skipped.
3. Open `my_recipes.json` here. For a few recipes, click the source link and compare: is the name the dish's own name, are steps missing, are the tags and time right?

It also opens the course's `recipe-chatbot\homeworks\hw4\reference_files\processed_recipes.json` (200 recipes; they have no source link, so that field shows as missing).

Adapted from `recipe-chatbot/homeworks/hw4/reference_files/query_viewer.html`.

## search-app (your search, step 3)

Type a question and see which recipes the bot's search would hand over, before the chat is involved (the Question → Context check). It runs the real search in `recipe-chatbot\backend\retrieval.py` (BM25 keyword search) on `recipe-chatbot\data\my_recipes.json`, so what you see is what the bot will get. Fewer than 20 recipes: top 4. 20 or more: top 5.

1. Open a terminal in this folder's `search-app` folder.
2. Run `uv run --project "../../../../recipe-chatbot" python search_app.py`
3. Open http://localhost:5002 . Stop it with Ctrl+C.

For each question you see:
- **Words searched:** each word of your question and how many recipes contain it. Rare words (green) count a lot, common ones (grey) little, words in no recipe (red) nothing.
- **Results:** ranked, with the BM25 score, a bar next to the top score, the words that matched, and the full recipe on click with the matched words highlighted. Scores are not percentages: compare them within one question only.

The same search works without the page: in `recipe-chatbot`, `uv run python backend/retrieval.py "your question"`.

## agent-traces-viewer.html (agent steps, HW5)

Shows multi-step agent chats with their tool calls, and where each one last succeeded and first failed. Use it before drawing the heat-map, to see what the failures look like.

Open from `recipe-chatbot\homeworks\hw5\reference_files`:
- `labeled_traces.jsonl`: 96 chats with last-success and first-failure steps.
- `raw_traces.jsonl`: the same chats without labels.

It also opens your results file or your trace files, shown as a conversation.

Copy of `recipe-chatbot/homeworks/hw5/reference_files/trace_viewer.html`.
