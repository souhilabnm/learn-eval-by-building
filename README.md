# Learn eval by building

My notes and playbook from learning how to build and evaluate AI agents, from zero, by doing. Everything you need is in this one repo: the guide, its templates and apps, and a working Recipe Chatbot to practise on.

**Version 1.0 (November 2026).** Covers setup, stages 1–5 and building search for the RAG (stage 6, points 1–3). Testing the RAG and improving the system prompt come in v2. See the [changelog](CHANGELOG.md).

**Versions:** each version is its own branch. You are on [v1.0](https://github.com/souhilabnm/learn-eval-by-building/tree/v1.0). `main` holds only the README that lists the versions.

**Read the guide online:** https://learn-eval-by-building.vercel.app

## Get started

You work in two places: the **guide** (a page you open in your browser) tells you what to do at each stage, and the **`recipe-chatbot` folder** is where you do it, with Claude Code coaching you.

1. **Clone this repo.** In the Claude app: **Code** tab > new session > select a course folder (any name, any place). Type:

   ```
   Clone the v1.0 branch of https://github.com/souhilabnm/learn-eval-by-building.git into this folder
   ```

   You get a `learn-eval-by-building` folder with `learn eval by doing/` and `recipe-chatbot/` side by side. Keep them that way: the annotation app and the coach skills point from one to the other.

2. **Open the guide:** https://learn-eval-by-building.vercel.app. Bookmark it.

3. **Open the chatbot folder in Claude Code.** **Code** tab > new session > select `learn-eval-by-building/recipe-chatbot`. Every command and coaching session from here on runs in this folder.

4. **Set it up.** Type:

   ```
   /learner-setup
   ```

   It installs everything and creates `.env`. Done when you see `Setup OK`.

5. **Add your model and API key** to `recipe-chatbot/.env` (Windows: right-click > **Open with** > **Notepad**; Mac: in Finder press Cmd+Shift+. to show hidden files, then **Open With** > **TextEdit**). For Anthropic:

   ```
   MODEL_NAME=anthropic/claude-sonnet-5-5
   MODEL_NAME_JUDGE=anthropic/claude-haiku-5-5
   ANTHROPIC_API_KEY=paste-your-key-here
   ```

   Save the file.

6. **Start the chatbot.** In Claude Code, type:

   ```
   Start the chatbot with: uv run uvicorn backend.main:app --reload --reload-include '*.md'
   ```

   Then open http://127.0.0.1:8000. On Windows, if you see `Got unexpected extra argument (README.md)`, use `--reload` alone and restart the server (Ctrl+C, then start again) after each edit to the system prompt.

7. **Get coached, stage by stage.** In Claude Code, type:

   ```
   /evals-coach
   ```

   It finds the stage you are on and coaches you one step at a time, matching the stages in the guide. You write and label; it explains and reviews. Type it again any time to pick up where you left off.

**The stages:** 1–2 spec and system prompt, 3–4 test queries and traces, 5 error analysis, 6 answer from your own recipes (RAG, worked example: an Algerian chef; v1 covers building search), 7–8 improve and monitor (coming in v2). The golden set and LLM judge are not covered yet.

## What's here

```
learn-eval-by-building/
├── learn eval by doing/         the guide and everything it links to
│   ├── Learn evals by doing.html    the guide (same as the online one)
│   ├── ressourses/templates/        one template per stage
│   │   ├── recipe-chatbot/              for this chatbot (the guide's page 2)
│   │   └── any-topic/                   for any bot, with two filled-in examples
│   └── useful apps/                 one folder per stage, each with a README
│       ├── stage-4-capture-traces/      results viewer
│       ├── stage-5-error-analysis/      annotation app (http://localhost:5001)
│       └── stage-6-evaluate-the-parts/  recipes viewer, search page (http://localhost:5002)
├── recipe-chatbot/              the chatbot you work on; open this folder in Claude Code
│   ├── backend/  frontend/  data/  scripts/  annotation/
│   └── .claude/skills/, CLAUDE.md   the coach skills
└── notes/                       how the coach skills are routed
```

| Path | What it is |
|---|---|
| [learn eval by doing/](<learn eval by doing/>) | The guide (`Learn evals by doing.html`) and the files it links to, kept together so the links work. `ressourses/templates/` holds one template per stage: `recipe-chatbot/` for this chatbot, `any-topic/` for any bot (with filled-in `example-policy-*` and `example-travel-*` versions). |
| [learn eval by doing/useful apps/](<learn eval by doing/useful apps/>) | Small apps, one folder per stage, each with a README: a viewer for your results, the annotation app for open and axial coding, a viewer for your recipe file and a page to try the search. |
| [recipe-chatbot/](recipe-chatbot/) | The chatbot you work on: the course code plus my changes (system prompt, bulk test that also saves trace files, `scripts/build_recipes.py` that turns recipe links into `data/my_recipes.json`, `scripts/search_eval.py`, the Algerian recipe links, the coach skills in `.claude/skills/` and `CLAUDE.md`). Your own runs (`results/`, `annotation/traces/`), `.env`, `.venv` and your recipe file stay on your computer. |
| [notes/01-how-skills-are-mapped.md](notes/01-how-skills-are-mapped.md) | How Claude Code skills are found, routed and chained together in the course project. |
| [index.html](index.html) | Opens the guide. |

**Not in this repo:** the course's homeworks, lessons and solution notebooks. They stay in the [original repository](https://github.com/ai-evals-course/recipe-chatbot); the guide links their walkthrough videos in its Resources tab.

## Credits and ownership

- **Original project:** the chatbot in `recipe-chatbot/` comes from **[ai-evals-course/recipe-chatbot](https://github.com/ai-evals-course/recipe-chatbot)**, the course repo for the AI Evals course. The chatbot, its datasets and the course material belong to the ai-evals-course authors and are licensed under [GPL-3.0](https://github.com/ai-evals-course/recipe-chatbot/blob/main/LICENSE).
- **Added by me:** the guide, the templates, the useful apps folder, the Claude Code skills and `CLAUDE.md`, and the changes to the chatbot listed above. The changed chatbot stays under GPL-3.0, as the original.
- **Older fork:** [souhilabnm/recipe-chatbot](https://github.com/souhilabnm/recipe-chatbot) is my earlier fork and does not have these changes. Use the `recipe-chatbot/` folder in this repo instead.
