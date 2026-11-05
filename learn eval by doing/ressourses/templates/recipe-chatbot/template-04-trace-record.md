# What each saved run records: Recipe Chatbot

Stage 4 · Observability. Evals can only check what was saved.
Each bulk test (scripts/bulk_test.py) saves every run twice. Open one of each and tick what is there.

## In the results file: recipe-chatbot/results/results_[date]_[time].json
One entry per question, all questions of the run together. Use it to compare runs.

| Field | Why you need it | There? |
|---|---|---|
| id | the row id from your query CSV, to point at one run in your notes | [ ] |
| query | what the user asked | [ ] |
| response | the full answer | [ ] |

## In the trace file: recipe-chatbot/annotation/traces/trace_bulk_[date]_[time]_[id].json
One file per question. Use it to label in stage 5.

| Field | Why you need it | There? |
|---|---|---|
| request > messages | the user's message | [ ] |
| response > messages | the whole chat, starting with the system prompt that was used | [ ] |
| open_coding | your stage 5 note (empty until you label) | [ ] |
| axial_coding_code | your stage 5 group (empty until you label) | [ ] |

## Not recorded by this repo
| Field | What to do instead |
|---|---|
| prompt_version | copy the results file and rename the copy after the prompt, for example v1-first-prompt.json |
| model | write the MODEL_NAME from your .env next to the version name |
| time | it is in the file name: results_20261026_153724 = 26 Oct 2026, 15:37:24 |

## Paste one results entry here


## The test
Pick one bad answer. From the files alone, can you tell why it happened?
Was it the instructions (open the system prompt in the trace file) or the model?

Your answer:
