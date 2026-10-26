# Learn eval by building

My notes and playbook from learning how to build and evaluate AI agents, from zero, by doing.

## Open the page

After cloning the repo, double-click `index.html` in the main folder. It opens the Learn Evals by Doing page in your browser. (GitHub's file viewer shows the HTML as code, so open it from your computer, not from GitHub.)

## What's here

| Path | What it is |
|---|---|
| [learn eval by doing/Learn evals by doing.html](<learn eval by doing/Learn evals by doing.html>) | The Learn Evals by Doing page (the playbook). Download the whole `learn eval by doing` folder and open the HTML file in a browser. |
| [learn eval by doing/](<learn eval by doing/>) | The page and the files it links to, kept together so the links work: `templates/` holds a blank `template-*` file for each stage plus filled-in `example-policy-*` and `example-travel-*` versions; `ressourses/` holds a copy of the course homeworks and lessons that the page opens. |
| [learn eval by doing/useful apps/](<learn eval by doing/useful apps/>) | The course's small apps, one folder per stage, each with a README: viewers for results and traces (read `.json` and `.jsonl`), and a light-theme copy of the annotation app for open and axial coding. Keep `learn eval by doing` and `recipe-chatbot` side by side: the annotation app reads `recipe-chatbot/annotation/traces`. |
| [notes/01-how-skills-are-mapped.md](notes/01-how-skills-are-mapped.md) | How Claude Code skills are found, routed and chained together in the course project. |
| [skills/](skills/) | The course's Claude Code skills: the `CLAUDE.md` router, `evals-coach` with its shared `coaching-rules.md`, `learner-setup`, and the six stage skills. **[How to use the skills →](skills/README.md)** |

## Hands-on project

The practice project lives in its own repo: **[souhilabnm/recipe-chatbot](https://github.com/souhilabnm/recipe-chatbot)**. It's a recipe chatbot used to work through a nine-stage evals playbook: spec, test queries, traces, error analysis, LLM judge, component checks, improve and monitor.

## Credits and ownership

- **Original project:** `souhilabnm/recipe-chatbot` is a fork of **[ai-evals-course/recipe-chatbot](https://github.com/ai-evals-course/recipe-chatbot)**, the course repo for the AI Evals course. The chatbot, homeworks, datasets and course material belong to the ai-evals-course authors and are licensed under [GPL-3.0](https://github.com/ai-evals-course/recipe-chatbot/blob/main/LICENSE).
- **Added in my fork:** the Claude Code skills in [skills/](skills/) and the `CLAUDE.md` router. They aren't part of the original repo. They coach a learner through the original course's stages and homeworks.
- **This repo:** my own notes and playbook from working through the course.
