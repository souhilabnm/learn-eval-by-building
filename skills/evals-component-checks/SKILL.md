---
name: evals-component-checks
description: Stage 7 of the evals playbook (HW4 and HW5). Coaches the learner to evaluate parts of an agent on their own - search quality with Recall@k and MRR, and agent-step failures with a transition heat-map. Use when the learner asks about retrieval, BM25, Recall@k, MRR, query rewriting, transition matrices, heat-maps, HW4 or HW5.
---

# Stage 7: evaluate the parts

Read `.claude/skills/evals-coach/coaching-rules.md` first.

## Before you start

Tell the learner up front: the chatbot in the browser has no search and no tool steps, so this stage uses the course's ready-made data. The goal is to learn how to find which part of a bigger agent is the bottleneck.

## Part A: search quality (HW4)

Why: if search returns the wrong recipe, even a perfect prompt gives a wrong answer. Test search on its own.

1. Explain the setup: 200 recipes in `homeworks/hw4/reference_files/processed_recipes.json`, and 200 questions in `synthetic_queries.jsonl`, each written from one known recipe.
2. The search is BM25, a keyword search (`backend/retrieval.py`). For each question, check whether its source recipe appears in the top results.
3. The two scores, both in `backend/evaluation_utils.py`:
   - **Recall@k**: how often the right recipe is in the top k (k = 1, 3, 5, 10).
   - **MRR**: how high it ranks on average (first place = 1, second = 0.5, third = 0.33).
4. Before scoring, they check the questions make sense: open `synthetic_queries.jsonl` in `useful apps/stage-7-evaluate-the-parts/search-queries-viewer.html` (or `homeworks/hw4/reference_files/query_viewer.html`). Then they run the notebook: `uv run --with jupyter jupyter notebook homeworks/hw4/hw4_walkthrough.ipynb`.
5. Have them look at 5 questions where search failed and say why (wording mismatch, too vague, several similar recipes). Optional: query rewriting (`backend/query_rewrite_agent.py`) rewords the question before searching. Compare the scores with and without it.

## Part B: which agent step fails (HW5)

Why: in a multi-step agent, you need to know which hand-off between steps breaks most often.

1. Data: 96 labeled conversations in `homeworks/hw5/reference_files/labeled_traces.jsonl`, each marked with the last step that worked and the first step that failed.
2. The learner runs the starter script, which draws a heat-map of those transitions:
   `uv run python homeworks/hw5/analysis/transition_heatmaps.py`
3. Have them find the darkest cell and explain in plain words what it means ("most failures happen when the agent hands the search results to the recipe writer").
4. Have them read the traces behind the darkest cell in `useful apps/stage-7-evaluate-the-parts/agent-traces-viewer.html` (or `homeworks/hw5/reference_files/trace_viewer.html`) with `labeled_traces.jsonl`. Only the first failure in each trace counts: later failures are often caused by it.
5. Guided version: `uv run --with jupyter jupyter notebook homeworks/hw5/hw5_walkthrough.ipynb`.

## The PM takeaway

Have the learner write one line per part: which component scores lowest, and what they would ask the team to fix first.

## Done when

- [ ] Recall@k and MRR reported, with a short reason for the failures
- [ ] The weakest transition named from the heat-map

## Next

Invoke `evals-improve-and-monitor`.
