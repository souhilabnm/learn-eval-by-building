# LLM judge: [failure name] · version v1

Stage 6 · Evals. One judge checks one failure. Fill in the question, then test the judge against your golden set (template-06-golden-set.csv).

## The judge prompt

You are checking one thing only.
User request: {query}
Answer: {response}
Question: (one yes or no question about one failure)
Reply with PASS or FAIL, then one sentence explaining why.

## Write down what PASS means
PASS when:
FAIL when:
Borderline cases and how you decided:

## Does the judge agree with you?
Run the judge on the dev rows of your golden set and fill template-06-judge-agreement.csv.
Then count (PASS counts as positive):

- True positive rate = rows where you said PASS and the judge said PASS ÷ all rows where you said PASS
- True negative rate = rows where you said FAIL and the judge said FAIL ÷ all rows where you said FAIL

| Version | Rows | True positive rate | True negative rate | What I changed |
|---|---|---|---|---|
| v1 | | | | |
| v2 | | | | |

Both rates high on the dev rows? Run it once on the test rows. That is your honest score.
