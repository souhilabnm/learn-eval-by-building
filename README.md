# Learn eval by building

My notes and playbook from learning how to build and evaluate AI agents, from zero, by doing.

## Open the page

After cloning the repo, double-click `index.html` in the main folder. It opens the Learn Evals by Doing page in your browser. (GitHub's file viewer shows the HTML as code, so open it from your computer, not from GitHub.)

## What's here

| Path | What it is |
|---|---|
| [learn eval by doing/Learn evals by doing.html](<learn eval by doing/Learn evals by doing.html>) | The Learn Evals by Doing page (the playbook). Download the whole `learn eval by doing` folder and open the HTML file in a browser. |
| [learn eval by doing/](<learn eval by doing/>) | The page and the files it links to, kept together so the links work: `templates/any-topic/` holds a blank `template-*` file for each stage plus filled-in `example-policy-*` and `example-travel-*` versions, `templates/recipe-chatbot/` the same templates made for the Recipe Chatbot; `ressourses/` holds a copy of the course homeworks and lessons that the page opens. |
| [recipe-chatbot/](recipe-chatbot/) | My working version of the Recipe Chatbot: the course code plus my changes (system prompt, bulk test that also saves trace files, `scripts/build_recipes.py` that turns recipe links into `data/my_recipes.json`, my recipe links and test queries, failure taxonomy, the coach skills in `.claude/skills/` and `CLAUDE.md`). Not included: `.env`, `.venv`, `results/`, `annotation/traces/` and the scraped recipe text. |
| [learn eval by doing/useful apps/](<learn eval by doing/useful apps/>) | The course's small apps, one folder per stage, each with a README: viewers for results and traces (read `.json` and `.jsonl`), and a light-theme copy of the annotation app for open and axial coding. Keep `learn eval by doing` and `recipe-chatbot` side by side: the annotation app reads `recipe-chatbot/annotation/traces`. |
| [notes/01-how-skills-are-mapped.md](notes/01-how-skills-are-mapped.md) | How Claude Code skills are found, routed and chained together in the course project. |
| [skills/](skills/) | The course's Claude Code skills: the `CLAUDE.md` router, `evals-coach` with its shared `coaching-rules.md`, `learner-setup`, and the six stage skills. **[How to use the skills →](skills/README.md)** |

## Hands-on project

The practice project is in [recipe-chatbot/](recipe-chatbot/), next to `learn eval by doing/` (keep them side by side: the annotation app and the coach skills point across them). It's a recipe chatbot used to work through the evals playbook: spec, test queries, traces, error analysis, answering from your own recipes (RAG, worked example: an Algerian chef), improve and monitor. Stage 6 (golden set and LLM judge) is not covered yet. The fork **[souhilabnm/recipe-chatbot](https://github.com/souhilabnm/recipe-chatbot)** has not been updated with these changes yet.

## Credits and ownership

- **Original project:** `souhilabnm/recipe-chatbot` is a fork of **[ai-evals-course/recipe-chatbot](https://github.com/ai-evals-course/recipe-chatbot)**, the course repo for the AI Evals course. The chatbot, homeworks, datasets and course material belong to the ai-evals-course authors and are licensed under [GPL-3.0](https://github.com/ai-evals-course/recipe-chatbot/blob/main/LICENSE).
- **Added in my fork:** the Claude Code skills in [skills/](skills/) and the `CLAUDE.md` router. They aren't part of the original repo. They coach a learner through the original course's stages and homeworks.
- **This repo:** my own notes and playbook from working through the course, and my working version of the chatbot in `recipe-chatbot/` (GPL-3.0, as the original).
