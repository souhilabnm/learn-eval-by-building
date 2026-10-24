# How skills are mapped

How Claude Code skills are found, routed and chained in the [recipe-chatbot](https://github.com/souhilabnm/recipe-chatbot) course project.

## Layer 1: How Claude finds a skill

A skill is a folder under `.claude/skills/` with a `SKILL.md` inside. Each one starts with a header:

```
---
name: evals-llm-judge
description: Stage 6 ... Use when the learner asks about golden sets, labeling, LLM-as-judge, judge prompts, TPR/TNR, judgy or HW3.
---
```

At the start of a session, Claude only sees each skill's **name and description**, not the full instructions. When a message comes in, Claude matches it against those descriptions. If the message is "how do I write a judge prompt?", the words "judge prompt" match `evals-llm-judge`. Only then does Claude load the full skill and follow it.

**PM takeaway:** the description is the routing rule. A vague description means the skill never gets picked, or gets picked at the wrong time.

## Layer 2: The front door (`CLAUDE.md`)

`CLAUDE.md` is always loaded, so it works like a receptionist:

- First time opening the project, or a setup or Python error → `learner-setup`
- Anything else → `evals-coach`

## Layer 3: The coach and the stage skills

`evals-coach` doesn't teach anything itself. It works out which stage the learner is on and hands them to the right specialist:

| Stage | Skill | Homework |
|---|---|---|
| 1–2 Spec + system prompt | `evals-spec-and-prompt` | HW1 pt 1 |
| 3–4 Test queries + traces | `evals-test-queries` | HW1 pt 2–3, HW2 pt 1 |
| 5 Error analysis | `evals-error-analysis` | HW2 pt 2 |
| 6 Golden set + LLM judge | `evals-llm-judge` | HW3 |
| 7 Evaluating parts | `evals-component-checks` | HW4–5 |
| 8–9 Improve + monitor | `evals-improve-and-monitor` | — |

Two design patterns hold this together:

1. **Gates ("Before you start").** Each stage skill checks that the previous stage is done, and sends the learner back if it isn't:
   - `evals-test-queries` checks whether `backend/system_prompt.md` has changed from the default. If it hasn't, it sends the learner to `evals-spec-and-prompt`.
   - `evals-error-analysis` needs a `results/results_*.json` file. If there isn't one, it sends the learner to `evals-test-queries`.
   - `evals-llm-judge` needs a failure taxonomy. If there isn't one, it sends the learner to `evals-error-analysis`.

   So jumping ahead doesn't let you skip a step.

2. **Shared rules.** Every stage skill starts with "Read `coaching-rules.md` first." The rules that apply everywhere ("the learner writes and labels; Claude explains, reviews and gives feedback") live in that one file instead of being copied into seven places.

## The full flow

```
User message
   ↓
CLAUDE.md (receptionist)
   ├─ setup issue → learner-setup  (the only skill where Claude runs things for the learner)
   └─ anything else → evals-coach (finds the stage)
                          ↓
                  stage skill → gate check → passes? teach : send back one stage
```

## Self-check

Say you open the project and type "help me with HW3", but you haven't done error analysis yet. Which skills fire, in what order, and where do you end up?

<details>
<summary>Answer</summary>

`CLAUDE.md` → `evals-coach` → `evals-llm-judge` (because of "HW3") → its gate finds no failure taxonomy → `evals-error-analysis`. That's where you start.
</details>
