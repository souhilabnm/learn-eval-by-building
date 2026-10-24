# Learn eval by building

My notes and playbook from learning how to build and evaluate AI agents, from zero, by doing.

## What's here

| Path | What it is |
|---|---|
| [playbook/agent-build-eval-playbook.html](playbook/agent-build-eval-playbook.html) | The Agent Build and Eval Playbook. Download it and open it in a browser. |
| [notes/01-how-skills-are-mapped.md](notes/01-how-skills-are-mapped.md) | How Claude Code skills are found, routed and chained together in the course project. |
| [skills/](skills/) | The course's Claude Code skills: the `CLAUDE.md` router, `evals-coach` with its shared `coaching-rules.md`, `learner-setup`, and the six stage skills. **[How to use the skills →](skills/README.md)** |

## Hands-on project

The practice project lives in its own repo: **[souhilabnm/recipe-chatbot](https://github.com/souhilabnm/recipe-chatbot)**. It's a recipe chatbot used to work through a nine-stage evals playbook: spec, test queries, traces, error analysis, LLM judge, component checks, improve and monitor.

## Credits and ownership

- **Original project:** `souhilabnm/recipe-chatbot` is a fork of **[ai-evals-course/recipe-chatbot](https://github.com/ai-evals-course/recipe-chatbot)**, the course repo for the AI Evals course. The chatbot, homeworks, datasets and course material belong to the ai-evals-course authors and are licensed under [GPL-3.0](https://github.com/ai-evals-course/recipe-chatbot/blob/main/LICENSE).
- **Added in my fork:** the Claude Code skills in [skills/](skills/) and the `CLAUDE.md` router. They aren't part of the original repo. They coach a learner through the original course's stages and homeworks.
- **This repo:** my own notes and playbook from working through the course.
