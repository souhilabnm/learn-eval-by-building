# How to use the skills

These Claude Code skills coach a learner through the [AI Evals course](https://github.com/ai-evals-course/recipe-chatbot) using its Recipe Chatbot. Claude explains, checks your work and gives feedback. You do the thinking work: writing, labeling and running the lessons.

For how the routing works under the hood, see [notes/01-how-skills-are-mapped.md](../notes/01-how-skills-are-mapped.md).

## 1. Install

You need [Claude Code](https://claude.com/claude-code) and a copy of the course repo, either the [original](https://github.com/ai-evals-course/recipe-chatbot) or a fork.

Copy the files into the course repo like this:

| From this folder | To the recipe-chatbot project |
|---|---|
| `CLAUDE.md` | `CLAUDE.md` (project root) |
| every skill folder (`evals-coach/`, `learner-setup/`, `evals-*/`) | `.claude/skills/` |

The skills look for their shared rules at `.claude/skills/evals-coach/coaching-rules.md`, so keep that exact path.

Windows (PowerShell), run from this `skills` folder, with your own path to recipe-chatbot:

```powershell
$dest = "E:\path\to\recipe-chatbot"
Copy-Item CLAUDE.md $dest
New-Item -ItemType Directory -Force "$dest\.claude\skills" | Out-Null
Get-ChildItem -Directory | Copy-Item -Destination "$dest\.claude\skills" -Recurse -Force
```

Mac (zsh):

```bash
dest=~/path/to/recipe-chatbot
cp CLAUDE.md "$dest"
mkdir -p "$dest/.claude/skills"
for d in */; do cp -R "${d%/}" "$dest/.claude/skills/"; done
```

Done when `recipe-chatbot/.claude/skills/` holds 8 skill folders and `CLAUDE.md` sits in the project root.

## 2. Start

Open the recipe-chatbot folder in Claude Code and type:

```
start
```

On first run, `learner-setup` takes over and sets up Python 3.13, uv, the dependencies and `.env` for you. This is the only skill where Claude runs commands for you. It never reads or writes your API key: it tells you which line to fill in and you paste the key yourself. No paid key? It can set you up on the Gemini free tier.

Once the bot replies at http://127.0.0.1:8000, `evals-coach` checks your files, tells you which stage you're on, and hands you to that stage's skill.

## 3. What to say

You don't need skill names. Plain phrases route you to the right place:

| You say | Goes to |
|---|---|
| "start", "where am I", "what's next", "continue" | `evals-coach`, which finds your stage |
| "set up", "install", or a `uv sync` / Python error | `learner-setup` |
| "help me with HW1" / "how do I write the spec?" | `evals-spec-and-prompt` (stages 1–2) |
| "test queries", "bulk test", "traces" | `evals-test-queries` (stages 3–4) |
| "HW2", "error analysis", "open coding", "failure modes" | `evals-error-analysis` (stage 5) |
| "RAG", "my recipes", "recipe links", "search test", "HW4", "HW5" | `evals-component-checks` (stage 7: answer from your own recipes) |
| "HW3", "golden set", "LLM judge" | not covered yet: the coach says so and carries on (`evals-llm-judge` is kept for later) |
| "improve the bot", "regression set", "monitoring" | `evals-improve-and-monitor` (stages 8–9) |

You can also call one directly with a slash command, for example `/evals-coach` or `/evals-component-checks`.

## 4. What to expect

- **One step per message.** Claude explains the step and why it matters, tells you exactly what to do, then waits for you to say "done".
- **You write, Claude reviews.** You write the spec, prompt, queries, notes, labels, recipe links and test questions. Claude reads them and gives specific feedback. If you ask, it writes a partial example for you to finish.
- **You run the commands** in your own terminal, one command per block, matched to Windows or Mac.
- **No skipping.** Each stage checks for the previous stage's output first. Ask for stage 7 without a failure taxonomy and you're sent back to error analysis.
- **Stop anytime.** Run `/evals-coach` later and it picks up where your files say you are.
- **Your work is never deleted.** Results, traces and labels are kept so you can compare runs.

Where your work ends up:

| Stage | File |
|---|---|
| 1 Spec | `recipe-bot-spec.md` |
| 2 System prompt | `backend/system_prompt.md` |
| 3 Test queries | `data/my_queries.csv` |
| 4 Traces | `results/results_<time>.json` (the whole run) + `annotation/traces/trace_bulk_<time>_*.json` (one per question) |
| 5 Error analysis | notes and categories saved in those trace files by the annotation app + your copy of `failure_mode_taxonomy.md` |
| 7 RAG | `data/recipe_links.txt`, `data/my_recipes.json` (built by `scripts/build_recipes.py`), your copy of `template-07-search-test.csv` |
| 8 Improve | `data/regression_queries.csv` + a before/after table |

## 5. Reuse the pattern

This setup works for any step-by-step course or workflow, not only this one:

1. **A router** (`CLAUDE.md`), which is always loaded and sends setup issues to one skill and everything else to a coach.
2. **A coach skill**, which checks the learner's files to find their stage and hands off. It never teaches.
3. **One skill per stage.** Each starts with a "Before you start" gate that checks the previous stage's output, and ends by invoking the next stage.
4. **One shared rules file**, which every skill reads first, so the tone, safety rules and who-does-what stay the same everywhere.
5. **Descriptions that list the words people actually say** ("HW3", "golden set", "judge prompt"). The description is what gets a skill picked.

## Files

```
skills/
├── CLAUDE.md                          router
├── evals-coach/
│   ├── SKILL.md                       finds the stage, hands off
│   └── coaching-rules.md              shared rules for every skill
├── learner-setup/SKILL.md             environment setup
├── evals-spec-and-prompt/SKILL.md     stages 1–2
├── evals-test-queries/SKILL.md        stages 3–4
├── evals-error-analysis/SKILL.md      stage 5
├── evals-llm-judge/SKILL.md           stage 6 (not covered yet)
├── evals-component-checks/SKILL.md    stage 7 (RAG on your own recipes)
└── evals-improve-and-monitor/SKILL.md stages 8–9
```
