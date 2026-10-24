---
name: evals-test-queries
description: Stages 3-4 of the evals playbook (HW1 Parts 2-3, HW2 Part 1). Coaches the learner to build a varied test query file, run it through the bot with the bulk test, and read the saved traces. Use when the learner asks about test queries, sample_queries.csv, bulk_test.py, results files or traces.
---

# Stages 3-4: test queries and traces

Read `.claude/skills/evals-coach/coaching-rules.md` first.

## Before you start

The system prompt must have been rewritten: `git diff --quiet -- backend/system_prompt.md` exits 1. If it exits 0 (still the default), say so and invoke `evals-spec-and-prompt`.

## Step 1: Pick dimensions (stage 3)

Why: random questions miss whole groups of users. Dimensions make sure every kind of request is covered.

Have the learner choose 3-4 dimensions with at least 3 values each, for example cuisine (Italian, Thai, Mexican), diet (vegan, gluten-free, none), meal type (breakfast, dinner, snack), time available, cooking skill.

## Step 2: Write the query file

Have them create `data/my_queries.csv`:

```
id,query
1,What can I cook with chicken and rice?
2,"Vegan dinner, 15 minutes, no oven"
```

- Start with their 10 requests from the spec, then add combinations of the dimensions. HW1 asks for at least 10 new queries. Aim for 20-30 now and grow towards 100+ over the course.
- Include awkward ones: vague ("help"), conflicting ("vegan steak dinner"), off-topic ("who is the president?").
- They may ask an AI to generate combinations and wording (HW2 Steps 2-3). They must read every generated query and delete the unrealistic ones.

Check the file yourself (read-only): the header is exactly `id,query`, ids are unique, and any query containing a comma is wrapped in double quotes. Report the row count and which dimensions are missing.

## Step 3: Run the bulk test (stage 4)

Why: one command sends every query to the bot and saves all answers, so you can read them side by side.

The learner runs, from the project folder:

```
uv run python scripts/bulk_test.py --csv data/my_queries.csv
```

Without `--csv` it uses `data/sample_queries.csv`. When it finishes it prints a line starting with "Saved" and the new file name in `results/`. On the Gemini free tier, a large file may hit the rate limit (`429`); suggest fewer rows or a pause.

## Step 4: Read the traces

Have them open the newest `results/results_<time>.json` in Notepad or VS Code and read three entries (`id`, `query`, `response`). Explain that this file is their set of traces, and that chats in the browser are also saved, one file per message, in `annotation/traces/`.

Point out what is not saved: the model, the prompt version, the time and the cost. Have them copy the results file and rename the copy to say which prompt version produced it (for example `results/v1-first-prompt.json`).

If they want an easier way to read the file, you may build a simple HTML viewer for it (HW1 suggests this). It is a tool, not the lesson.

## Done when

- [ ] `data/my_queries.csv` with varied queries (100+ is the target over time)
- [ ] At least one results file in `results/`, kept and renamed by version

These match "Test query set of 100+ inputs saved" and "Traces are saved as JSON".

## Next

Invoke `evals-error-analysis`.
