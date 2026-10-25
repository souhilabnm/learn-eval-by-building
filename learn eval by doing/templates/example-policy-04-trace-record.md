# What each saved run must record (filled-in example: HR policy bot)

Made-up example for learning. Try the stage yourself first, then compare.

| Field | Why you need it | There? |
|---|---|---|
| id | to point at one run in your notes | [x] |
| time | to sort runs and sample by week | [x] |
| query | what the user asked | [x] |
| response | the full answer | [x] |
| prompt_version | to compare before and after a change | [x] |
| model | to know which model answered | [x] |
| retrieved | the policy passages search found, with document ids | [x] doc ids only at first; passage text added before stage 5 |

## One saved record

```json
{
  "id": "3",
  "time": "2026-10-25T09:40:00",
  "query": "parental leave how long",
  "response": "You get 10 sick days per year. Source: Sick leave policy, section 2.1",
  "prompt_version": "v1",
  "model": "the model I used",
  "retrieved": [
    { "doc_id": "sick-leave-policy.pdf", "text": "2.1 Employees receive 10 paid sick days per year..." },
    { "doc_id": "benefits-overview.pdf", "text": "Health cover includes..." },
    { "doc_id": "sick-leave-policy.pdf", "text": "2.3 A doctor's note is needed after 3 days..." }
  ]
}
```

## The test
Record 3 answers a parental leave question with sick days. None of the three passages came from leave-policy.pdf, which holds the answer. Cause: the search, not the instructions. The answer was faithful to what it was given.
