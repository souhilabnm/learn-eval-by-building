# Recipe Chatbot

The chatbot you practise on. Open this folder in Claude Code and follow the guide, stage by stage.

- **Guide:** https://learn-eval-by-building.vercel.app (also in `../learn eval by doing/Learn evals by doing.html`).
- **Setup:** in Claude Code, type `/learner-setup`. Then add your model and API key to `.env`.
- **Start the chatbot:** `uv run uvicorn backend.main:app --reload --reload-include '*.md'`, then open http://127.0.0.1:8000.
- **Get coached:** type `/evals-coach`. It finds your stage and coaches you one step at a time.

## What is here

| Path | What it is |
|---|---|
| `backend/` | The server, the link to the AI model, the system prompt (`system_prompt.md`) and the recipe search (`retrieval.py`). |
| `frontend/index.html` | The chat page. |
| `data/` | Example test questions (`sample_queries.csv`) and the worked example's recipe links (`recipe_links.txt`). Your own files go here too: `my_queries.csv` (stage 3) and `my_recipes.json` (stage 6). |
| `scripts/` | `bulk_test.py` sends a whole CSV of questions to the bot; `build_recipes.py` turns recipe links into `data/my_recipes.json`; `search_eval.py` scores search on your stage 6 test sheet. |
| `annotation/` | Your traces (`traces/`, one file per chat) and the course's 250 sample chats (`course_samples_extra/`). The labeling app is in `../learn eval by doing/useful apps/stage-5-error-analysis/`. |
| `.claude/skills/`, `CLAUDE.md` | The coach skills Claude Code uses. |

Your own runs (`results/`, `annotation/traces/`), `.env` and `data/my_recipes.json` stay on your computer: git ignores them.

## Credits

From [ai-evals-course/recipe-chatbot](https://github.com/ai-evals-course/recipe-chatbot), the course repo of the AI Evals course, under GPL-3.0 (see `LICENSE`). Its homeworks and lessons are in that repository, not here.
