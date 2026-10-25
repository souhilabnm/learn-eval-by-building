# What each saved run must record (filled-in example: City trip planner)

Made-up example for learning. Try the stage yourself first, then compare.

| Field | Why you need it | There? |
|---|---|---|
| id | to point at one run in your notes | [x] |
| time | to sort runs and sample by week | [x] |
| query | what the user asked | [x] |
| response | the full answer | [x] |
| prompt_version | to compare before and after a change | [x] was missing at first; added before stage 5 |
| model | to know which model answered | [x] |
| retrieved | the guide passages search found, with document ids | [x] |

## One saved record

```json
{
  "id": "41",
  "time": "2026-10-25T10:12:00",
  "query": "3 days in Rome, 300 euros, I hate museums",
  "response": "Day 1: Trastevere food walk (40 euros) ... Day 3: ... Total: 420 euros",
  "prompt_version": "v1",
  "model": "the model I used",
  "retrieved": [
    { "doc_id": "rome-guide.pdf", "text": "Trastevere food tours run daily, about 40 euros per person..." },
    { "doc_id": "rome-guide.pdf", "text": "Colosseum and Forum combined ticket: 18 euros..." }
  ]
}
```

## The test
Record 41 totals 420 euros on a 300 euro budget. The passages were right: every price came from the guide. Nothing in the v1 instructions told the bot to add up costs and compare them with the budget. Cause: the instructions, not the search.
