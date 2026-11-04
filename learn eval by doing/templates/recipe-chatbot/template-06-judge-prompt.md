# LLM judge: [failure name] · version v1

Stage 6 · Evals. One judge checks one failure from your stage 5 list (annotation/failure_mode_taxonomy.md).
Save your copy as recipe-chatbot/data/judge_prompt.md. The judge runs on MODEL_NAME_JUDGE from your .env.
Test it against your golden set, recipe-chatbot/data/golden_set.csv (template-06-golden-set.csv).

## The judge prompt

Keep the first three lines and the last line as they are. Write your Question in place of the text in brackets: the brackets are guidance, not part of the prompt.
{query} and {response} are filled in from the query and response columns of your golden set.

You are checking one thing only.
User request: {query}
Answer: {response}
Question:
(One yes or no question about the one failure you picked.
Phrase it so that YES means PASS.
Example, for a diet failure: Does the answer respect every diet restriction the user mentioned?
Once you have settled a borderline case below, add its rule here in one sentence,
for example: "Vegetarian" allows eggs and dairy; "vegan" does not.)
Reply with PASS or FAIL, then one sentence explaining why.

## Write down what PASS means
Write these before you label the golden set. Test them: would a colleague label the same trace the same way?

PASS when:
(What a good answer does, in one sentence, concrete enough to point at in the answer.
For the diet example: every ingredient fits every diet the user named.)

FAIL when:
(The failure, in one sentence. The opposite of PASS, with no case that fits neither.
For the diet example: at least one ingredient breaks a diet the user named.)

Borderline cases and how you decided:
(Traces where you hesitated while labeling, and which way you went and why.
For the diet example: honey in a vegan recipe. Decided FAIL: most vegans avoid it.
Start with one you already met in stage 5, and add more as you label.)

## Does the judge agree with you?
Run the judge on the dev rows of your golden set and fill template-06-judge-agreement.csv.
Then count (PASS counts as positive):

- True positive rate = rows where you said PASS and the judge said PASS ÷ all rows where you said PASS
- True negative rate = rows where you said FAIL and the judge said FAIL ÷ all rows where you said FAIL

| Version | Rows | True positive rate | True negative rate | What I changed |
|---|---|---|---|---|
| v1 | (for example 30 dev) | (for example 19/20 = 0.95) | | first try |
| v2 | | | | (the one sentence you added or changed in the Question) |

A low rate tells you where to look: a low true negative rate means the judge passes answers you failed, so your Question is too loose.
Both rates high on the dev rows? Run it once on the test rows. That is your honest score.
To see how the course does the split and the maths: homeworks/hw3/hw3_walkthrough.ipynb (after your own attempt).
