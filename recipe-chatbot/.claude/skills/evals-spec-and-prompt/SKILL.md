---
name: evals-spec-and-prompt
description: Stages 1-2 of the evals playbook (HW1 Part 1). Coaches the learner to write a spec for the Recipe Chatbot, then turn it into the system prompt in backend/system_prompt.md and compare the bot before and after. Use when the learner is starting the course, is on HW1, or asks how to write the spec or the system prompt.
---

# Stages 1-2: spec and system prompt

Read `.claude/skills/evals-coach/coaching-rules.md` first.

## Before you start

Setup must be done (`.venv` and `.env` with a `MODEL_NAME`). If not, invoke `learner-setup` and come back.

## Step 1: Write the spec (stage 1)

Why: the spec says what "good" means. Every later check is measured against it.

Have the learner create `recipe-bot-spec.md` in the project folder (Notepad or TextEdit is fine) and answer each heading in one or two sentences:

```
Who uses it:
Job:
A good answer looks like:
Must never:
Out of scope:
```

Under the headings, they write 10 requests exactly as a real user would type them: short, messy, vague, one with a diet restriction, one off-topic.

Check, then give feedback:
- Each heading has a concrete answer, not "be helpful".
- "Must never" includes a safety rule (unsafe or harmful requests).
- "A good answer looks like" is specific enough to judge an answer against.
- The 10 requests are varied and include awkward ones.

Suggest they show it to someone who cooks before moving on.

## Step 2: See the bot as it is now

Why: you need a "before" to compare with.

Have the learner start the chatbot (command in the coaching rules), open http://127.0.0.1:8000 and send 3 of their 10 requests. Ask them to note one thing they like and one they don't for each answer.

## Step 3: Turn the spec into the system prompt (stage 2)

Why: the system prompt is the same intent as the spec, written as instructions the AI reads before every chat.

Have them open `backend/system_prompt.md`, delete the default text and write five headings, filling each from the spec:

| Spec heading | Prompt heading | Example |
|---|---|---|
| Who uses it | Role | You are an expert chef helping busy parents cook on weekdays. |
| Job | Task | Give one complete recipe that fits the user's request. |
| Must never, and Out of scope | Rules | Respect every diet the user mentions. If asked to order groceries, say you cannot. |
| A good answer looks like | Format | Title, serving size, ingredients list, then numbered steps. |
| (not in the spec) | Defaults | If no serving size is given, assume 2 people. |

HW1 also asks for these, so check they are in the prompt:
- "Always" and "never" rules that are specific.
- A safety clause: politely decline unsafe or harmful requests.
- A creativity level: stick to known recipes, or allowed to invent and say so.
- An output format in Markdown (recipe name as a heading, ingredients list, numbered steps).

Review against the spec: every "Must never" line appears as a rule, and every rule could be checked on a real answer. Don't rewrite the prompt for them.

## Step 4: Compare

Have them save the file (restart the server if they used the shorter command), send the same 3 requests and compare with step 2. Remind them: change one thing at a time, so they know which edit caused which change.

## Done when

- [ ] `recipe-bot-spec.md` with five headings and 10 requests
- [ ] `backend/system_prompt.md` rewritten from the spec
- [ ] The bot answers in the browser with the new prompt

These match "Wrote a spec and 10 example requests" and "Version 0 runs end to end" in the playbook's progress list.

## Next

Invoke `evals-test-queries`.
