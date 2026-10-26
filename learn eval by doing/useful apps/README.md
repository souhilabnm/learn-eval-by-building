# Useful apps

The small apps from the course, sorted by the stage of the guide where you use them.

Two kinds:
- **Viewers** (`.html`): read-only. Double-click to open in your browser, click the file button and pick a file. They read `.json` files (one list, like your bulk test results) and `.jsonl` files (one record per line, like the course's datasets). You can look, not write.
- **Labeling apps** (Python): you write notes and categories, saved into the files. They read folders inside `recipe-chatbot`, and use its Python setup; the command is in their stage's README.

| Stage | App | What for |
|---|---|---|
| 1 Define the job | none | |
| 2 Build version 0 | none | The chat page at http://127.0.0.1:8000 is the bot itself. |
| 3 Create test inputs | none | The bulk test is a script, not an app. |
| 4 Capture traces | `stage-4-capture-traces/results-viewer.html` | Read a bulk test results file, one question and answer at a time. |
| 5 Error analysis | `stage-5-error-analysis/annotation-app/annotation.py` | Open coding and axial coding on your traces, saved in `recipe-chatbot/annotation/traces`. |
| 6 Golden set and judge | `stage-6-golden-set-and-judge/labeled-traces-viewer.html` | See what PASS and FAIL look like in the course's labeled traces. |
| 7 Evaluate the parts | `stage-7-evaluate-the-parts/search-queries-viewer.html`, `agent-traces-viewer.html` | Check the search test questions; read agent chats with tool steps. |
| 8 Improve and re-run | none | Compare two results files in the stage 4 viewer, side by side. |
| 9 Monitor and repeat | none | Weekly samples go back through the stage 5 annotation app. |

The viewers are copies of the ones in `recipe-chatbot/homeworks/*/reference_files/`, renamed to say what they show. The annotation app is a copy of `recipe-chatbot/annotation/annotation.py` that reads the repo's traces folder.
