---
name: evals-error-analysis
description: Stage 5 of the evals playbook (HW2 Part 2). Coaches the learner through open coding, axial coding and counting to build a failure taxonomy from the bot's traces. Use when the learner asks about error analysis, open coding, axial coding, failure modes, the taxonomy, HW2, the trace viewer or the annotation tool.
---

# Stage 5: error analysis

Read `.claude/skills/evals-coach/coaching-rules.md` first.

## Before you start

The learner needs traces: at least one `results/results_*.json`. If there is none, say so and invoke `evals-test-queries`.

If they want more data than their own run, HW2 offers 250 ready query/response pairs in `homeworks/hw2/reference_files/query_response.jsonl`.

Point them to the course help before they code (all in `homeworks/hw2/`):
- **Watch it done first:** Isaac and Hamel doing open and axial coding, https://youtu.be/AKg27L4E0M8. The full HW2 video is https://youtu.be/h9oAAAYnGx4.
- **Official steps:** HW2 Part 2 in `homeworks/hw2/README.md`.

## Step 1: Set up a reading view and a notes sheet

Why: raw JSON is hard to scan and you lose your place. Read in a viewer on one side of the screen, write notes in a sheet on the other.

1. **Viewer.** Have them double-click `homeworks/hw2/reference_files/viewer.html`, click the file button and pick their results file from `results/` (for example `results_20261024_222451.json`). It shows one question and answer at a time, with Previous and Next. It reads both formats: a bulk test `.json` list and a `.jsonl` file (one object per line), such as `query_response.jsonl`.
2. **Sheet.** Google Sheets, Excel or a CSV with the HW2 columns: `Trace_ID`, `User_Query`, `Full_Bot_Trace_Summary`, `Open_Code_Notes`. For a finished example of the layout, they can open `lesson-7/data/traces.csv` (one row per conversation, a failure mode column).

If the viewer shows an error: a file renamed from `.json` to `.jsonl` still holds a list, which is fine now; anything else, read the file's first characters to see what it holds. Never delete their results files.

## Step 2: Open coding

Why: you find out how the bot actually fails, in your own words, before deciding on categories.

For each trace they ask: would a real user be happy? Did it follow my spec? They write one short note per problem, with no categories yet. Aim for 50-100 traces. Have them send their first 5 notes for feedback before doing the rest.

Check a few notes and coach on quality:
- Good: specific and visible in the answer ("used butter after the user said vegan").
- Weak: vague ("bad answer", "not great").

You may do one trace together as a demonstration. The rest is theirs.

Optional tool: the annotation tool (command in the coaching rules) has fields for open and axial coding. It shows browser chats from `annotation/traces/`, not bulk results, so the viewer and sheet are the main route.

## Step 3: Axial coding

Why: grouping notes turns 100 observations into a few problems you can fix and measure.

Have them group similar notes into 4-8 failure modes. For each one, HW2 asks for:
- **Title**: a clear name
- **Definition**: one sentence
- **Examples**: 1-2 real traces

They write these in their own copy of `homeworks/hw2/reference_files/failure_mode_taxonomy.md` (the template already contains sample failure modes to replace). Check that each definition is sharp enough that two people would label the same trace the same way.

## Step 4: Count

Have them add one column per failure mode to the sheet, mark 1 or 0 for each trace, and SUM each column. If the sheet is a CSV in the project, you may count it for them to check their totals. The two most frequent modes are the first targets.

## Step 5: Compare with the solution (after their own attempt)

`homeworks/hw2/hw2_walkthrough.ipynb` is the course's solution. Suggest it only once their taxonomy and counts exist, to compare categories, not to copy them. Command: `uv run --with jupyter jupyter notebook homeworks/hw2/hw2_walkthrough.ipynb`.

## Done when

- [ ] Notes on at least 50 traces
- [ ] 4-8 failure modes with title, definition and examples
- [ ] A count per failure mode

These match "Read 100 traces and wrote notes" and "Failure taxonomy with counts".

## Next

Invoke `evals-llm-judge`.
