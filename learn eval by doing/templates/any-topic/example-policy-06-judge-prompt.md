# LLM judge: supported by the passages · version v2 (filled-in example)

Made-up example for learning. Try the stage yourself first, then compare.
A real golden set has about 50 rows; the rates below assume one.

## The judge prompt

You are checking one thing only.
User question: {query}
Policy passages the bot was given: {retrieved}
Answer: {response}
Question: Is every claim in the answer supported by the policy passages? Ignore whether the passages are the right ones for the question; only check the answer against them. Saying the policies don't cover something is supported.
Reply with PASS or FAIL, then one sentence naming any unsupported claim.

## What PASS means
PASS when: every fact, number and rule in the answer appears in the passages, or the bot says the policies don't cover it.
FAIL when: any fact, number or rule is missing from the passages or contradicts them.
Borderline cases and how I decided: a wrong-topic answer that is faithful to its passages is a PASS here. It is a search failure, measured in stage 7.

## Does the judge agree with me?

| Version | Rows | True positive rate | True negative rate | What I changed |
|---|---|---|---|---|
| v1 | 30 dev | 16/21 = 0.76 | 9/9 = 1.00 | first try: it failed wrong-topic answers that were faithful |
| v2 | 30 dev | 20/21 = 0.95 | 8/9 = 0.89 | added "ignore whether the passages are the right ones" |
| v2 | 20 test | 13/14 = 0.93 | 5/6 = 0.83 | final honest score, run once |
