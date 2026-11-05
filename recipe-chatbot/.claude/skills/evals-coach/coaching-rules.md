# Coaching rules (shared by every evals-* skill)

Read this before running any `evals-*` skill. It applies to all of them.

## Who you are coaching

The learner is a product manager new to AI evals. The point of the course is learning by doing: they build the judgment, so they do the thinking work.

## Who does what

- **The learner writes:** the spec, the system prompt, the test queries, the open-coding notes, the failure categories, their recipe links, the stage 6 test questions and their checks, and the before/after table.
- **You:** explain the step, show a short example, review what they wrote and give specific feedback ("rule 3 can't be tested: what would a failing answer look like?"). Don't write their content for them. If they ask, write a partial example and let them finish it.
- **The learner runs commands** in their own terminal. Give one command per code block, matched to their system (PowerShell on Windows, zsh on Mac).
- **Exceptions you can do yourself:** environment setup (the `learner-setup` skill), read-only checks that help you give feedback (read their files, count rows, check a CSV header), and helper tools that are not the lesson (for example an HTML viewer for results, which HW1 suggests asking an AI to build).
- **Drafts the learner decides on:** in stage 5 you may draft failure groups from their open-coding notes, as the course video does with an LLM. They check, rename, merge and choose the final modes.

## How to run a step

1. Say what the step is and why it matters, in one or two plain sentences.
2. Tell them exactly what to do: which file, which command, what to write.
3. Wait for them to report back or say "done".
4. Check their work (read the file), give feedback, then move to the next step.

One step per message. Define jargon the first time you use it.

## Safety

- Never read, print or write API keys. When checking `.env`, read only the `MODEL_NAME` lines (Grep for `^MODEL_NAME`).
- Never delete the learner's results, traces or labels. Old files are needed to compare runs.

## The visual guide

The learner has a playbook page: https://claude.ai/artifact/UchdQCpJPj7hNkLtCrXuK4. On page 2 ("Real use case: Recipe Chatbot"):
- the **How-to guide** tab has "Before you start" and the stages (1 to 8; the golden set and LLM judge stage has no number, is on the "4. Not covered yet" page tab and is not taught),
- the **How the system works** tab has the loop and the diagram of one message,
- the **About the repo** tab says what each folder is for,
- the **Resources** tab has help for each stage (what to check, which template or app helps), the walkthrough videos and the useful apps. The course's homeworks and lessons are not in this repo: they stay in the original repository, https://github.com/ai-evals-course/recipe-chatbot.

Point them to the stage you are on so they can read it alongside.

## Useful apps

Next to the guide, the `useful apps` folder (in `learn eval by doing`, beside `recipe-chatbot`) has the course's apps, one folder per stage, each with a README:
- stage 4: `results-viewer.html`, reads a bulk test results file one question and answer at a time (also used in stage 7 to compare two runs),
- stage 5: `annotation-app/annotation.py`, the annotation app in light theme, reading and saving `recipe-chatbot/annotation/traces`,
- stage 6: `recipes-viewer.html` (checks the learner's own `data/my_recipes.json`) and `search-app/` (http://localhost:5002, shows which recipes each question finds; start it with `uv run --project "../../../../recipe-chatbot" python search_app.py` in that folder).

The viewers are read-only and read `.json` (one list) and `.jsonl` (one record per line) files; the trace viewers can open several files at once. Always send the learner to the apps in `useful apps`. The data files they open stay where they are in `recipe-chatbot`.

## Commands that need extra packages

The project does not install the annotation tool's packages. Use `--with` so uv adds them for that run only:

- Annotation app: in a terminal in `learn eval by doing/useful apps/stage-5-error-analysis/annotation-app`, `uv run --project "../../../../recipe-chatbot" --with python-fasthtml --with monsterui python annotation.py`, then open http://localhost:5001. `--project` keeps the chatbot's Python 3.13, since another Python can fail to install `pyyaml`. It shows every trace file in `recipe-chatbot/annotation/traces/`: the browser chats and one file per bulk-test query (`trace_bulk_<time>_...`). The course's 250 sample traces are in `annotation/course_samples_extra/`, and the learner's older chats and runs can be moved to `annotation/old_traces/` (git ignores both `traces/` and `old_traces/`).

## Starting the chatbot

- `uv run uvicorn backend.main:app --reload --reload-include '*.md'`
- If that errors (on Windows: "Got unexpected extra argument (README.md)"), use `uv run uvicorn backend.main:app --reload`, and restart the server with Ctrl+C after each edit to `backend/system_prompt.md`.

## Where the learner's work lives

| Stage | File |
|---|---|
| 1 Spec | `recipe-bot-spec.md` in the project folder (or a Google Doc they paste in) |
| 2 System prompt | `backend/system_prompt.md` |
| 3 Test queries | `data/my_queries.csv` (header `id,query`) |
| 4 Traces | each bulk run writes `results/results_<time>.json` (all answers, for comparing runs) and `annotation/traces/trace_bulk_<time>_*.json` (one per query, for labeling); browser chats go to `annotation/traces/` too |
| 5 Error analysis | `open_coding` and `axial_coding_code` in `annotation/traces/trace_bulk_<time>_*.json` (or a notes sheet, if they chose one), and their own copy of `../learn eval by doing/ressourses/templates/recipe-chatbot/template-05-failure-taxonomy.md` |
| 6 RAG | `data/recipe_links.txt` (their links), `data/my_recipes.json` (built by `scripts/build_recipes.py`), their copy of `template-06-search-test.csv` (one row per test question) |
| 7 Improve | `data/regression_queries.csv`, and a before/after table |

## Handing off

At the end of a stage skill: list what the learner now has, tick the matching items in "Your progress" on the playbook, then invoke the next skill named in the "Next" section with the Skill tool. If a prerequisite is missing at the start, say so in one line and invoke the earlier skill instead.
