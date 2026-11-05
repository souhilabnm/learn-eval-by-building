---
name: evals-improve-and-monitor
description: Stages 7-8 of the evals playbook. Coaches the learner to fix one failure at a time with a before/after comparison, keep a regression set, and set a weekly monitoring routine that feeds new failures back into error analysis. Use when the learner asks how to improve the bot, compare prompt versions, build a regression set, or monitor it over time.
---

# Stages 7-8: improve and monitor

Read `.claude/skills/evals-coach/coaching-rules.md` first.

## Before you start

The learner needs failure counts (stage 5) and their stage 6 test sheet. If either is missing, say so and invoke `evals-error-analysis` or `evals-component-checks`. The LLM judge stage is not covered yet, so they measure by reading and counting, not with a judge.

## Step 1: Pick one target (stage 7)

Why: fixing one thing at a time is the only way to know what worked.

Have them choose the failure mode with the highest count, or the one that hurts users most, and write down its current rate (for example "ignores diet: 9 of 40").

## Step 2: Save the "before"

Have them copy `backend/system_prompt.md` to a file named for its version (for example `prompts/v1.md`), and keep the results file the current prompt produced.

## Step 3: Change one thing

One edit to `backend/system_prompt.md` that targets the failure, such as a clearer rule or one example. Review it with them: does it address the failure, and could it break another rule?

## Step 4: Re-run and compare

1. They run the same query file again: `uv run python scripts/bulk_test.py --csv data/my_queries.csv`.
2. They check the new answers the same way as before: read and count the target failure, and re-run their stage 6 test questions if they changed the recipes, search or the parts of the prompt about recipes.
3. They fill a before/after table: version, rate for the target failure, rates for the other failures.
4. To compare the answers themselves, they open the old and the new results file in `useful apps/stage-4-capture-traces/results-viewer.html`, in two browser tabs.

Keep the change only if the target improved and nothing else got worse.

## Step 5: Regression set

Why: a fixed failure can quietly come back after the next change.

Have them add the queries that now pass to `data/regression_queries.csv` (same `id,query` format) and run it after every future change.

## Step 6: Monitoring routine (stage 8)

Why: real users find failures your tests missed.

Help them write their weekly routine:
1. Pick 20 recent conversations at random (here: browser chats in `annotation/traces/` or the newest bulk run). To code them in the annotation app, move last week's coded traces into `annotation/old_traces/` first, so only the new sample is listed.
2. Run the checks and read the failures themselves.
3. Add any new failure type to the taxonomy and its queries to the regression set.
4. Go back to error analysis.

In a real product, they would also ask engineering for a dashboard of the main checks and an alert when a score drops.

## Done when

- [ ] A before/after table for one improvement
- [ ] `data/regression_queries.csv`
- [ ] A written weekly routine

These match the last three items in the playbook's progress list.

## Next

The loop starts again. When new failures show up, invoke `evals-error-analysis`. Otherwise tell the learner they've completed the playbook once and can run `/evals-coach` any time to continue.
