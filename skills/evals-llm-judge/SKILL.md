---
name: evals-llm-judge
description: Stage 6 of the evals playbook (HW3). Coaches the learner to turn one failure mode into a check: a code check for objective failures, or an LLM judge validated against a hand-labeled golden set with TPR/TNR and judgy bias correction. Use when the learner asks about golden sets, labeling, LLM-as-judge, judge prompts, TPR/TNR, judgy or HW3.
---

# Stage 6: golden set and LLM judge

Read `.claude/skills/evals-coach/coaching-rules.md` first.

## Before you start

The learner needs a failure taxonomy from stage 5. If they don't have one, say so and invoke `evals-error-analysis`.

HW3 uses dietary adherence ("asked for vegan, got a vegan recipe?") because its rules are clear. They may follow HW3 or pick a failure mode from their own taxonomy. Ready-made HW3 data in `homeworks/hw3/reference_files/`: `raw_traces.jsonl` (about 2,400 traces), `labeled_traces.jsonl` (101 labeled), `dietary_queries.csv` (60 hard queries).

## Step 1: Pick one failure and the cheapest check

Why: one check tests one failure. Cheap checks first.

- **Objective** (format, length, a missing section): a code check. Have the learner write the rule in words and the expected PASS/FAIL for 3 example answers. If they want it automated, you may write the small script with them, explaining each line, and they confirm it gives their expected results.
- **Subjective** (diet respected, tone right): an LLM judge. Continue below.

## Step 2: Define PASS and FAIL in words

Have them write one sentence each for PASS and FAIL, plus edge cases (for example: "vegetarian" allows eggs and dairy, "vegan" does not). Check that two people would label the same answer the same way.

## Step 3: Build the golden set

Why: the golden set is the answer key. Without it you can't know if the judge is right.

They label traces themselves, PASS or FAIL, and save `data/golden_set.csv` with columns `id,query,response,label,note`. Start with about 50; HW3 asks for 100-200. The set needs both enough PASS and enough FAIL; if failures are rare, they pull more traces. You may load traces into the CSV for them; the labels are theirs.

## Step 4: Split it

HW3 split: Train 10-20% (examples for the judge prompt), Dev 40% (to improve the judge), Test 40-50% (touched once, at the end).

## Step 5: Write the judge prompt

Have them write `data/judge_prompt.md` with:
- the task and the criterion,
- the PASS and FAIL definitions from step 2,
- 2-3 examples from Train, each with input, output, reasoning and label,
- the output format: JSON with `reasoning` and `answer` (PASS or FAIL).

The judge uses `MODEL_NAME_JUDGE` from `.env`.

## Step 6: Measure the judge

Run the judge on Dev and compare with their labels:
- **TPR** (true positive rate): of the answers they marked PASS, how many the judge also marked PASS.
- **TNR** (true negative rate): of the answers they marked FAIL, how many the judge also marked FAIL.

If either is low, they change the prompt and run Dev again. When satisfied, run Test once and report TPR and TNR. The code for this is in the guided notebook: `uv run --with jupyter jupyter notebook homeworks/hw3/hw3_walkthrough.ipynb`.

## Step 7: Correct the result with judgy

Run the judge on many new traces (HW3: 500-1000). The `judgy` library (already installed) uses TPR and TNR to report the raw pass rate, the corrected pass rate and a 95% confidence interval. Have them write 1-2 paragraphs: how well does the bot follow the rule, and how sure are they?

## Done when

- [ ] At least one code check for an objective failure (if their taxonomy has one)
- [ ] `data/golden_set.csv` labeled by them, with both PASS and FAIL
- [ ] A judge with TPR and TNR measured on the Test split

These match "Code checks for objective failures", "Golden set labeled by me" and "LLM judge checked against my golden set".

## Next

If the learner wants to evaluate search or agent steps, invoke `evals-component-checks`. Otherwise invoke `evals-improve-and-monitor`.
