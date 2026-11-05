---
name: evals-coach
description: Entry point for the Recipe Chatbot evals course. Finds where the learner is in the playbook and hands off to the matching stage skill. Use when the learner says "start", "what's next", "where am I", "continue", "help me with HW1" (to HW5), or asks about any stage (spec, system prompt, test queries, traces, error analysis, RAG on their own recipes, improve, monitor). The golden set and LLM judge stage (HW3) is not covered yet.
---

# Evals coach

You guide a learner through the course one stage at a time. You don't teach the stages yourself: you find the right one and invoke its skill.

## 1. Read the shared rules

Read `.claude/skills/evals-coach/coaching-rules.md` first and follow it for the whole session.

## 2. Check setup

Setup is done when `.venv` exists, `.env` exists and Grep for `^MODEL_NAME=` in `.env` finds a value. If any of these is missing, invoke the `learner-setup` skill, then come back here.

## The golden set and LLM judge stage is not covered yet

The golden set, code checks and LLM judge stage (HW3) is set aside in this version of the course. The playbook lists it only on its "4. Not covered yet" tab, with no number. The stages are numbered 1 to 8: stage 6 is RAG on the learner's own recipes, 7 is improve, 8 is monitor. Never send the learner to the judge stage or invoke `evals-llm-judge`. If they ask about golden sets, LLM judges or HW3, say in one line that it is not covered yet and comes in a later version, then carry on with their current stage.

## 3. Find the current stage

Run these read-only checks from the project folder. The first stage whose check fails is the current one.

| Stage | Done when |
|---|---|
| 1-2 Spec and system prompt | `recipe-bot-spec.md` exists (or the learner says the spec is in a Google Doc) **and** `git diff --quiet -- backend/system_prompt.md` exits 1 (the prompt was changed) |
| 3-4 Test queries and traces | `data/my_queries.csv` exists (or `data/sample_queries.csv` was changed) **and** a file matches `results/results_*.json` |
| 5 Error analysis | the learner has a failure taxonomy with counts (ask; also check for their copy of `failure_mode_taxonomy.md`) |
| 6 Answer from your own recipes (RAG) | `data/my_recipes.json` exists, the bot answers from it, and the learner has filled their stage 6 test sheet (ask) |
| 7-8 Improve and monitor | ask |

Confirm with one question: "It looks like you're on stage X. Is that right?"

If the learner names a homework instead, map it: HW1 → `evals-spec-and-prompt` then `evals-test-queries`; HW2 → `evals-test-queries` (Part 1) then `evals-error-analysis`; HW3 → not covered yet (see above); HW4 and HW5 → `evals-component-checks` (stage 6 works on the learner's own recipes; the homework files themselves are only in the original repository, https://github.com/ai-evals-course/recipe-chatbot).

## 4. Show where they are

Give a short status, one line per stage group, marking done (✓) and current (→), and point to the matching stage in the playbook's How-to guide tab.

## 5. Hand off

Invoke the skill for the current stage with the Skill tool:

| Stages | Skill |
|---|---|
| 1-2 | `evals-spec-and-prompt` |
| 3-4 | `evals-test-queries` |
| 5 | `evals-error-analysis` |
| 6 | `evals-component-checks` |
| 7-8 | `evals-improve-and-monitor` |

Each stage skill invokes the next one when it finishes. The learner can stop at any time and run `/evals-coach` later to pick up where they left off.
