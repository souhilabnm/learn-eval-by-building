# Stage 5: error analysis

## annotation-app (the main tool)

The course's annotation app, for open coding and axial coding. One chat at a time:
- a big box for your open-coding notes,
- a box above it for the axial-coding category (type a new one, or pick one you already used),
- Save (or Ctrl+Enter) stores both in that trace's file and opens the next one.

It shows every file in `recipe-chatbot\annotation\traces`: your browser chats (2026...) and one file per bulk test question (`trace_bulk_<time>_001.json` and on). Each trace shows the system prompt it was made with.

Older chats or runs you don't want in the list: move them to `recipe-chatbot\annotation\old_traces` (keep them for a before/after comparison). The course's 250 sample chats are in `recipe-chatbot\annotation\course_samples_extra`; move some into `traces` to practise on them.

`annotation-app\annotation.py` is a copy of `recipe-chatbot\annotation\annotation.py` with two changes: it reads and writes the traces in `recipe-chatbot\annotation\traces`, and it always uses the light theme. Use this copy, not the original. Keep `learn eval by doing` and `recipe-chatbot` in the same folder (here `E:\learn eval`).

1. Run the bulk test first, so your traces exist. In a terminal in `recipe-chatbot`:

   ```
   uv run python scripts/bulk_test.py --csv data/my_queries.csv
   ```

2. Start the app. In a terminal in this `annotation-app` folder:

   ```
   uv run --project "../../../../recipe-chatbot" --with python-fasthtml --with monsterui python annotation.py
   ```

   `--project` uses the chatbot's own Python setup; without it, uv may pick a newer Python and fail to install a package.

3. Open http://localhost:5001. Your run is at the bottom, shown as "bulk" and its date. Stop the app with Ctrl+C.

Steps for open and axial coding: stage 5 on page 2 of the guide. The app's own notes: `recipe-chatbot\annotation\README.md`.

## Labeling tool with several categories per chat (optional)

From the course's Lesson 6, in `recipe-chatbot\lesson-7\labeling-tool` (not copied: it only loads `lesson-7\data\traces.csv`, 118 agent chats with tool calls, not your traces). It lets you pick more than one failure mode per chat. It uses port 8000, the same as the chatbot, so stop the chatbot first. In a terminal in `recipe-chatbot`:

```
uv run --with fastapi --with "uvicorn[standard]" python lesson-7/labeling-tool/main.py
```

Then open http://localhost:8000. Labels are added to `lesson-7\data\labeled_traces_latest.jsonl`.
