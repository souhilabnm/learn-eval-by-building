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

Without `--csv` it uses `data/sample_queries.csv`. When it finishes it prints two lines starting with "Saved": the new results file in `results/` (all answers in one list, for comparing runs) and the trace files in `annotation/traces/` (`trace_bulk_<time>_001.json` and on, one per query, for labeling in stage 5). Both carry the same `<time>`. On the Gemini free tier, a large file may hit the rate limit (`429`); suggest fewer rows or a pause.

## Step 4: Read the traces

Why: a trace is one question plus the bot's answer. Reading a few shows what your evals will work with.

There are exactly three actions. Give them one at a time and wait for the learner to finish each before the next:

1. **Open** the newest `results/results_<time>.json` in Notepad or VS Code. Each entry is one trace, with an `id`, a `query` (the question) and a `response` (the bot's answer). Have them read three entries.
2. **Copy** the file and **rename the copy** after the prompt version that produced it, for example `results/v1-first-prompt.json`. Why: the file does not record the prompt version, and the next bulk test creates a new file. The renamed copy keeps this version for the before/after comparison in stage 8. Never edit or delete old copies. After every prompt change: run the bulk test again, then rename the new file (`v2-...`).
3. **Know what is not saved.** The file has no model name, prompt version, time taken or cost. A real product would save them. The learner does not add them here; they only need to know to ask for them. The renamed copy is the manual stand-in for the prompt version.

Do not ask them to re-run queries by hand or run each query twice. That is optional and not part of this stage.

Optional, only if the learner asks: `annotation/traces/` holds one file per chat, the format the annotation app reads in stage 5. Files named `trace_bulk_<time>_...` are this bulk run, one per query. Files named `trace_2026...` are the learner's own browser chats, one file per message. The course's 250 ready-made sample chats (`trace_2024-...`, ids like `SYN025`) are kept apart in `annotation/course_samples_extra/`. In each, `request` is what was sent and `response` is the full conversation with the bot's answer at the end (the system prompt is the first message), with empty `open_coding` and `axial_coding_code` fields. It is a separate place from `results/`: the results file is for comparing runs, the trace files are for labeling. Never convert one into the other.

If they want an easier way to read the answers now, point them to `useful apps/stage-4-capture-traces/results-viewer.html`: double-click it, then pick the results file. It shows one question and answer at a time. The course's viewers read both `.jsonl` files (one record per line) and `.json` files (one list), such as bulk test results. Stage 5 then opens the same answers one at a time in the annotation app, where they label them.

## Done when

- [ ] `data/my_queries.csv` with varied queries (100+ is the target over time)
- [ ] At least one results file in `results/`, read (3 entries), then copied and renamed by prompt version

These match "Test query set of 100+ inputs saved" and "Traces are saved as JSON".

## Next

Invoke `evals-error-analysis`.
