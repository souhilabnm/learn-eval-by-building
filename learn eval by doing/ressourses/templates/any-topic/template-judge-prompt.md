# LLM judge: [failure name] · version v1

Later stage (not covered yet) · Evals. One judge checks one failure. Fill in the question, then test the judge against your golden set (template-judge-golden-set.csv).
Stuck? Two filled-in examples sit next to this file: example-travel-judge-prompt.md (stays within budget) and example-policy-judge-prompt.md (claims supported by the documents).

## The judge prompt

Keep the first three lines and the last line as they are. Write your Question in place of the text in brackets: the brackets are guidance, not part of the prompt.

You are checking one thing only.
User request: {query}
Answer: {response}
Question:
(One yes or no question about the one failure you picked in stage 5.
Phrase it so that YES means PASS.
Example for another failure: Does the answer respect every diet restriction the user mentioned?
Once you have settled a borderline case below, add its rule here in one sentence.)
Reply with PASS or FAIL, then one sentence explaining why.

## Write down what PASS means
Write these before you label the golden set. Test them: would a colleague label the same trace the same way?

PASS when:
(What a good answer does, in one sentence, concrete enough to point at in the answer.)

FAIL when:
(The failure, in one sentence. The opposite of PASS, with no case that fits neither.)

Borderline cases and how you decided:
(Traces where you hesitated while labeling, and which way you went and why. Start with one you already met in stage 5, and add more as you label.)

## Does the judge agree with you?
Run the judge on the dev rows of your golden set and fill template-judge-agreement.csv.
Then count (PASS counts as positive):

- True positive rate = rows where you said PASS and the judge said PASS ÷ all rows where you said PASS
- True negative rate = rows where you said FAIL and the judge said FAIL ÷ all rows where you said FAIL

| Version | Rows | True positive rate | True negative rate | What I changed |
|---|---|---|---|---|
| v1 | (for example 30 dev) | (for example 19/20 = 0.95) | | first try |
| v2 | | | | (the one sentence you added or changed in the Question) |

A low rate tells you where to look: a low true negative rate means the judge passes answers you failed, so your Question is too loose.
Both rates high on the dev rows? Run it once on the test rows. That is your honest score.
