# Stage 7: evaluate the parts

Both are read-only. Double-click to open, then click the file button and pick a file.

## search-queries-viewer.html (search, HW4)

Shows each search test question with the recipe it was written from and the key fact it asks about. Use it to check the questions make sense before scoring the search.

Open `recipe-chatbot\homeworks\hw4\reference_files\synthetic_queries.jsonl` (200 questions).

Copy of `recipe-chatbot/homeworks/hw4/reference_files/query_viewer.html`.

## agent-traces-viewer.html (agent steps, HW5)

Shows multi-step agent chats with their tool calls, and where each one last succeeded and first failed. Use it before drawing the heat-map, to see what the failures look like.

Open from `recipe-chatbot\homeworks\hw5\reference_files`:
- `labeled_traces.jsonl`: 96 chats with last-success and first-failure steps.
- `raw_traces.jsonl`: the same chats without labels.

It also opens your results file or your trace files, shown as a conversation.

Copy of `recipe-chatbot/homeworks/hw5/reference_files/trace_viewer.html`.
