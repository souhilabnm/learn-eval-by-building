---
name: evals-component-checks
description: Stage 7 of the evals playbook, "Answer from your own recipes (RAG)". Coaches the learner to turn recipe links into a recipe file, make the bot answer only from it (BM25 search, top 3), and test search and answer separately with Paweł Huryn's Question, Context, Answer method. Worked example - an Algerian chef with 15 Algerian recipes. HW4 and HW5 are optional extras. Use when the learner asks about RAG, their own recipes, recipe links, build_recipes, retrieval, BM25, search tests, hybrid search, query rewriting, HW4 or HW5.
---

# Stage 7: answer from your own recipes (RAG)

Read `.claude/skills/evals-coach/coaching-rules.md` first.

## Before you start

The learner needs their failure counts from stage 5. If they don't have them, say so and invoke `evals-error-analysis`. Stage 6 (LLM judge) is not covered yet: don't mention it as a prerequisite.

Explain in two sentences: RAG means the bot first searches a set of documents (here, recipes the learner chose), then answers only from what it found, like an open-book exam. When an answer is wrong, the test tells you whether search found the wrong recipe or the answer ignored the right one, because they need different fixes.

The method comes from Paweł Huryn, "How to build a RAG chatbot" (https://www.productcompass.pm/p/how-to-build-a-rag-chatbot), written for PMs. Point them to stage 7 on page 2 of the playbook.

**Worked example:** an Algerian chef. 15 Algerian recipes from one French recipe site (chorba frik, mderbel, tchouktchouka and more); the bot always answers in English. The learner can use any cuisine and any language: the steps are the same.

**Fixed for everyone,** so builds stay comparable: the file names below, the recipe fields (`id`, `name`, `description`, `ingredients`, `steps`, `tags`, `minutes`, `source_url`), BM25 keyword search returning the top 3, English answers, and the test sheet columns.

## Step 1: Pick the recipes

1. The learner picks 10 to 20 recipes and puts one link per line in `data/recipe_links.txt`.
2. They also write down 3 dishes they leave out on purpose (in the example: couscous). These become "not in data" test questions in Step 5.

Review: are the links recipe pages (not category pages)? Is there enough variety for vague questions to be hard (two soups, two tajines)?

## Step 2: Build the recipe file

1. They run, in `recipe-chatbot`: `uv run python scripts/build_recipes.py`. It reads each page's recipe card (or the page text), translates to English, keeps the dish's own name, and saves `data/my_recipes.json`. A link that fails is skipped and named at the end.
2. They open `data/my_recipes.json` in `useful apps/stage-7-evaluate-the-parts/recipes-viewer.html` and compare 3 recipes with their source page (click the link): wrong names, missing steps, odd tags, guessed times.

You may read `data/my_recipes.json` to count recipes and spot missing fields. The file is in `.gitignore`: the recipe text belongs to the source sites.

## Steps 3 and 4: Make the recipes searchable, connect search to the chat

The learner builds these with Claude Code themselves (the course author's decision: learners build the RAG, the guide fixes names and formats). The playbook's ready-to-paste prompt for these steps is still being tested on the worked example.

Until it is in the guide:
- Have the learner write, in their own words, what they want built: search over `data/my_recipes.json` with `backend/retrieval.py` (BM25), the top 3 recipes passed to the model before it answers.
- Have them update `backend/system_prompt.md` themselves: the persona (example: an Algerian chef), answer only from the recipes given, name the recipe used, say "I don't have that recipe" when none fits, always answer in English.
- Review their brief and their prompt against the fixed points above. Don't write the code or the prompt for them; if they ask, give a partial example.

Done when they ask the bot about one of their recipes and it answers from it, and ask about a left-out dish and it says it doesn't have it.

## Step 5: Write the test questions

Why: you can only judge search if you know which recipe each question should find.

1. 20 to 30 questions, each written from one recipe they know, in three kinds:
   - **exact**: names the dish ("How do I make chorba frik?"),
   - **vague**: describes it without the name ("a green wheat soup with lamb"),
   - **not in data**: one of the left-out dishes ("Give me a couscous recipe"). Expected recipe: none.
2. One row each in their copy of `learn eval by doing/templates/recipe-chatbot/template-07-search-test.csv`. Columns: question, kind, expected_recipe_id, in_top_3, rank, uses_only_found_recipes, correct, notes.

Review: is each question answerable by exactly one recipe? Are the vague ones really vague, or do they give away the name?

## Step 6: Check each answer in three parts

Paweł's Question, Context, Answer. For each question they fill:
- **in_top_3 / rank**: did search return the expected recipe in the top 3, and where?
- **uses_only_found_recipes**: did the answer use only what search returned, with nothing added?
- **correct**: is the answer right? For "not in data", correct means it said it doesn't have that recipe; giving a recipe anyway is a fail.

Then they count each column by kind. Keep the search column and the answer columns apart: they point to different fixes.

## Step 7: Fix the weaker part, re-run

- Search missed (mostly vague questions): hybrid search (keywords plus meaning) or query rewriting (`backend/query_rewrite_agent.py`).
- Answer added things not in the recipe, or answered "not in data" questions: tighten the system prompt.

One change at a time, then re-run the same questions. The detailed fix steps are still being written in the guide; coach the reasoning (which column is worse, what that points to) rather than inventing a build recipe.

## Optional extras (the course's version, more technical)

Only if the learner asks:
- **HW4:** search scored on 200 ready recipes and 200 queries with Recall@k and MRR (`homeworks/hw4/README.md`, viewer `search-queries-viewer.html`, notebook `uv run --with jupyter jupyter notebook homeworks/hw4/hw4_walkthrough.ipynb`).
- **HW5:** which step of a multi-step agent fails, as a heat-map (`uv run python homeworks/hw5/analysis/transition_heatmaps.py`, traces in `agent-traces-viewer.html`).

## The PM takeaway

Have the learner write one line: which part is weaker, search or answer, on which kind of question, and what they would fix first.

## Done when

- [ ] Recipe file built from their own links and checked
- [ ] Bot answers only from their recipes
- [ ] Stage 7 test sheet: search and answer checked for each question

These match the three stage 7 items in "Your progress" on the playbook.

## Next

Invoke `evals-improve-and-monitor`.
