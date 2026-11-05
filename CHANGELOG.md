# Changelog

Each version covers the guide, the coach skills and the `recipe-chatbot` folder together. They move as one: a guide stage and its `/evals-coach` step always match.

## v1.0 · 2026-11-05 · First version

The first version shared with learners and colleagues.

**Covered**

- **Setup:** clone the repo, `/learner-setup`, add your model and API key, start the chatbot.
- **Stages 1–2:** write the spec (your definition of good) and the system prompt.
- **Stages 3–4:** write test queries, run the bulk test, capture traces.
- **Stage 5:** error analysis: open coding and axial coding in the annotation app, failure counts.
- **Stage 6, points 1–3 (RAG, building search):** turn your recipe links into `data/my_recipes.json` (`scripts/build_recipes.py`), check them in the recipes viewer, make them searchable with BM25 (`backend/retrieval.py`) and try search in the search app (`useful apps/stage-6-evaluate-the-parts/search-app/`).
- **Coach skills:** `/evals-coach` and the stage skills, `/learner-setup`.

**Updated on 2026-11-05, still v1.0**

- Stages renumbered 1 to 8: the golden set and judge stage moved out, so RAG is now stage 6, improve 7, monitor 8. Templates and app folders renamed to match.
- Cleaner repo: templates in `learn eval by doing/ressourses/templates/`, apps in `useful apps/`. The course homeworks, lessons and the duplicate `skills/` folder are no longer in the repo (homeworks and lessons are in the original course repository).
- Guide: clearer stage 1, 2, 5 and 6 steps, copy button in the template popup, hover definitions, footer with credits.

**Coming in v2**

- Stage 6, points 4–7: connect search to the chat, then test the RAG (exact, vague and not-in-data questions, checked as Question → Context → Answer).
- Stage 7: improve the system prompt and re-run, before and after.
- Stage 8: monitor and repeat.

These parts are visible in the guide as a preview, marked **Coming in v2**.

**Not covered yet**

- The golden set and LLM judge (the Not covered yet page of the guide, no stage number).
