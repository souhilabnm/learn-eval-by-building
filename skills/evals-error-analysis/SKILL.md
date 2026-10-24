---
name: evals-error-analysis
description: Stage 5 of the evals playbook (HW2 Part 2). Coaches the learner through open coding, axial coding and counting to build a failure taxonomy from the bot's traces. Use when the learner asks about error analysis, open coding, axial coding, failure modes, the taxonomy, HW2 or the annotation tool.
---

# Stage 5: error analysis

Read `.claude/skills/evals-coach/coaching-rules.md` first.

## Before you start

The learner needs traces: at least one `results/results_*.json`. If there is none, say so and invoke `evals-test-queries`.

If they want more data than their own run, HW2 offers 250 ready query/response pairs in `homeworks/hw2/reference_files/query_response.jsonl`, with `viewer.html` in the same folder to browse them.

## Step 1: Set up a notes sheet

Why: you will read many answers. A sheet keeps every note next to its trace.

Have the learner create a sheet (Google Sheets, Excel or a CSV) with the HW2 columns: `Trace_ID`, `User_Query`, `Full_Bot_Trace_Summary`, `Open_Code_Notes`.

## Step 2: Open coding

Why: you find out how the bot actually fails, in your own words, before deciding on categories.

For each trace they ask: would a real user be happy? Did it follow my spec? They write one short note per problem, with no categories yet. Aim for 50-100 traces.

Check a few notes and coach on quality:
- Good: specific and visible in the answer ("used butter after the user said vegan").
- Weak: vague ("bad answer", "not great").

You may do one trace together as a demonstration. The rest is theirs.

Optional tools:
- The annotation tool (command in the coaching rules) has fields for open and axial coding. It shows browser chats from `annotation/traces/`, not bulk results.
- The guided notebook: `uv run --with jupyter jupyter notebook homeworks/hw2/hw2_walkthrough.ipynb`. The course video on open and axial coding is linked in `homeworks/hw2/README.md`.

## Step 3: Axial coding

Why: grouping notes turns 100 observations into a few problems you can fix and measure.

Have them group similar notes into 4-8 failure modes. For each one, HW2 asks for:
- **Title**: a clear name
- **Definition**: one sentence
- **Examples**: 1-2 real traces

They write these in their own copy of `homeworks/hw2/reference_files/failure_mode_taxonomy.md` (the template already contains sample failure modes to replace). Check that each definition is sharp enough that two people would label the same trace the same way.

## Step 4: Count

Have them add one column per failure mode to the sheet, mark 1 or 0 for each trace, and count each column. If the sheet is a CSV in the project, you may count it for them to check their totals. The two most frequent modes are the first targets.

## Done when

- [ ] Notes on at least 50 traces
- [ ] 4-8 failure modes with title, definition and examples
- [ ] A count per failure mode

These match "Read 100 traces and wrote notes" and "Failure taxonomy with counts".

## Next

Invoke `evals-llm-judge`.
