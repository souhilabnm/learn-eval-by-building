---
name: evals-error-analysis
description: Stage 5 of the evals playbook (HW2 Part 2). Coaches the learner through open coding and axial coding in the course's FastHTML annotation app, with LLM-drafted groups the learner checks, then counting to build a failure taxonomy. Use when the learner asks about error analysis, open coding, axial coding, failure modes, the taxonomy, HW2, the annotation tool or the trace viewer.
---

# Stage 5: error analysis

Read `.claude/skills/evals-coach/coaching-rules.md` first.

This stage follows the course: HW2 Part 2 in `homeworks/hw2/README.md`, the open and axial coding video, and the annotation app in `annotation/` (see `annotation/README.md`).

## Before you start

The learner needs traces from a bulk run: `annotation/traces/trace_bulk_<time>_*.json`, which `scripts/bulk_test.py` writes next to `results/results_<time>.json` (same `<time>`). If there are none, say so and invoke `evals-test-queries`. A results file from before the bulk test saved traces has no trace files: have them run the bulk test again.

Point them to the course help before they start:
- **Watch it done first:** Isaac and Hamel doing open and axial coding in the annotation app, https://youtu.be/AKg27L4E0M8. The full HW2 video is https://youtu.be/h9oAAAYnGx4.
- **Official steps:** HW2 Part 2 in `homeworks/hw2/README.md`.

## Step 1: Open their traces in the annotation app

Why: the course reads and labels traces in a small app, one chat at a time, with a box for the note and one for the category. Notes are saved inside each trace file, so nothing gets lost. Isaac made the bot save every chat as its own file for exactly this; the bulk test does the same for each query.

Results and traces are separate on purpose: `results/` holds one file per run for the before/after comparison in stage 8; `annotation/traces/` holds one file per chat for labeling. Never convert one into the other, and never edit the results files.

They start the app (commands in the coaching rules: the original in `annotation/`, or the light-theme copy in `useful apps/stage-5-error-analysis/annotation-app`, same traces either way) and open http://localhost:5001. The home page lists files by name: their browser chats (2026...), then their bulk runs, shown as `bulk <date>` with the question. They click the first trace of the run they're coding. Save (or Ctrl+Enter) moves to the next file.

Each trace shows the system prompt it was made with, so older chats show an older prompt. If older chats or runs get in the way, they move them (never delete) into `annotation/old_traces/`: they're the "before" for stage 8. A run where some questions failed (for example a `429` rate limit) has gaps in its numbering; have them rerun with `--workers 2` and code the complete run.

If they would rather use a spreadsheet, the course allows it (HW2 Step 4, and Isaac in the video: Excel is fine if the chats are easy to read). Use the guide's open-coding sheet (columns `id,what went wrong,category`), then add one 1/0 column per failure mode and SUM each one. They can still read the answers in the app.

## Step 2: Open coding

Why: you find out how the bot actually fails, in your own words, before deciding on categories.

For each trace they ask: would a real user be happy? Did it follow my spec? (The System Prompt panel in the app shows what the bot was told.) They write in the big text box:
- in full sentences, specific enough that someone else, or an LLM later, understands them,
- one line per problem; several problems in one answer is fine (single-turn chats),
- no categories yet: the category box stays empty.

Have them send their first 5 notes for feedback before doing the rest. You can read the notes yourself: they are in the `open_coding` field of each `trace_bulk_<time>_*.json`.

Coach on quality:
- Good: specific and visible in the answer ("says 'silky sauce' without saying how thick, too vague for a beginner").
- Weak: vague ("bad answer", "not great").
- Encourage the product view from the video: is this what the product should do for its users? Notes about the spec itself are welcome.

You may do one trace together as a demonstration. The rest is theirs.

When to stop: aim for 50-100 traces. If the last 10 or so only repeat problems they already noted, they have read enough for this round (the video calls this saturation; it stops at 10 only to demonstrate).

## Step 3: Axial coding, with an LLM draft

Why: grouping notes turns many observations into a few problems you can fix and measure. In the video, an LLM drafted the groups from the notes and the humans checked them.

When they ask, read the `open_coding` fields of their `trace_bulk_<time>_*.json` files (read-only) and suggest groups of similar problems: a name, a count, two example trace ids each, and which groups often occur together. Do not write anything into the trace files.

Then the decisions are theirs. Have them:
- open the example traces of each group and check the group fits,
- rename unclear names (in the video "prescriptive issues" became "ambiguous instruction"), merge or split, until they have 4-8 failure modes,
- write each one in their own copy of `homeworks/hw2/reference_files/failure_mode_taxonomy.md` (it already holds sample modes to replace): **Title**, a one-sentence **Definition**, and 1-2 real **Examples**.

Check that each definition is sharp enough that two people would label the same trace the same way.

## Step 4: Label each trace

They go through their traces again in the app and set the category box above the notes. The first time they type a name it is saved; after that it appears in the list for every trace. The box holds one category per trace: if a trace has two problems, they pick the most important and keep the other in the note. Two ✅ on the home page mean notes and category are both saved.

## Step 5: Count

When they ask, count the `axial_coding_code` values across their `trace_bulk_<time>_*.json` files (read-only) and show the counts next to your draft counts from Step 3. Differences show where they and the LLM disagreed: worth a look. The two most frequent modes are the first targets; also ask which mode would hurt a user most, even if rare.

## Step 6: Compare with the solution (after their own attempt)

`homeworks/hw2/hw2_walkthrough.ipynb` is the course's solution. Suggest it only once their taxonomy and counts exist, to compare categories, not to copy them. Command: `uv run --with jupyter jupyter notebook homeworks/hw2/hw2_walkthrough.ipynb`.

## Other data and tools

- **More data:** the course's 250 sample chats (`trace_2024-01-15_...`, ids like `SYN025`) are in `annotation/course_samples_extra/`; they move some into `annotation/traces/` to open them in the app. Their system prompt is a placeholder, so they can't be checked against the learner's spec. Browse the same pairs in `homeworks/hw2/reference_files/viewer.html` with `query_response.jsonl`; the course's viewers read both `.jsonl` and `.json` files. To read a whole bulk run outside the app, `homeworks/hw3/reference_files/trace_viewer.html` (or the HW5 one) can open all its `trace_bulk_<time>_*.json` files at once: select them together in the file picker.
- **Several categories per chat:** `lesson-7/labeling-tool` (the course's Lesson 6) has a multi-select. It loads `lesson-7/data/traces.csv`, 118 agent chats with tool calls; that file has no label columns.
- **Multi-step chats (HW5):** note only the first failure in each trace; later failures are often caused by it.

## Done when

- [ ] Notes on at least 50 traces (or fewer, if nothing new was showing up)
- [ ] 4-8 failure modes with title, definition and examples
- [ ] Every trace they read labeled with one mode, and a count per mode

These match "Read 100 traces and wrote notes" and "Failure taxonomy with counts".

## Next

Invoke `evals-llm-judge`.
