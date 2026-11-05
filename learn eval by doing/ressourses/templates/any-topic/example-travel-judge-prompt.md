# LLM judge: stays within budget · version v2 (filled-in example)

Made-up example for learning. Try the stage yourself first, then compare.
A real golden set has about 50 rows; the rates below assume one.

## The judge prompt

You are checking one thing only.
User request: {query}
Answer: {response}
Question: Does the plan's total cost stay within the budget the user stated? If no total is given, add up the listed costs yourself. If the user gave no budget and the answer asks for one, that is a PASS.
Reply with PASS or FAIL, then one sentence explaining why.

## What PASS means
PASS when: the total (stated or added up) is at or under the budget, or no budget was given and the bot asks for one.
FAIL when: the total is over the budget, or the budget is clearly impossible and the bot plans anyway without saying so.
Borderline cases and how I decided: costs listed with no total. I add them up; over budget is a FAIL.

## Does the judge agree with me?

| Version | Rows | True positive rate | True negative rate | What I changed |
|---|---|---|---|---|
| v1 | 30 dev | 19/20 = 0.95 | 6/10 = 0.60 | first try: it passed plans with no total line |
| v2 | 30 dev | 19/20 = 0.95 | 9/10 = 0.90 | added "add up the listed costs yourself" |
| v2 | 20 test | 12/13 = 0.92 | 6/7 = 0.86 | final honest score, run once |

Both rates are high enough for me to trust v2 on this one failure.
