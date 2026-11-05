# Useful apps

Small apps for the guide, sorted by the stage where you use them. Each folder has a README with the steps.

Two kinds:
- **Viewers** (`.html`): read-only. Double-click to open in your browser, click the file button and pick a file. They read `.json` files, like your bulk test results and your recipe file.
- **Local pages** (Python): they run on your computer with the chatbot's Python setup and open at a `localhost` address. The command is in their stage's README.

| Stage | App | What for |
|---|---|---|
| 1 Define the job | none | |
| 2 Build version 0 | none | The chat page at http://127.0.0.1:8000 is the bot itself. |
| 3 Create test inputs | none | The bulk test is a script, not an app. |
| 4 Capture traces | `stage-4-capture-traces/results-viewer.html` | Read a bulk test results file, one question and answer at a time. |
| 5 Error analysis | `stage-5-error-analysis/annotation-app/` (http://localhost:5001) | Open coding and axial coding on your traces, saved in `recipe-chatbot/annotation/traces`. |
| 6 Answer from your own recipes | `stage-6-evaluate-the-parts/recipes-viewer.html`, `stage-6-evaluate-the-parts/search-app/` (http://localhost:5002) | Check your own recipes before search uses them; see which recipes each question finds. |
| 7 Improve and re-run | none | Compare two results files in the stage 4 viewer. |
| 8 Monitor and repeat | none | Weekly samples go back through the stage 5 annotation app. |

Keep `learn eval by doing` and `recipe-chatbot` side by side in the same folder: the local pages find the chatbot at `../../../../recipe-chatbot`.

Credits: `results-viewer.html` and the annotation app are copies of the course's own tools from [ai-evals-course/recipe-chatbot](https://github.com/ai-evals-course/recipe-chatbot); `recipes-viewer.html` is adapted from its HW4 query viewer. The search app is new.
