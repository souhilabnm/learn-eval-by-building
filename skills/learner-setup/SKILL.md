---
name: learner-setup
description: Sets up the recipe-chatbot environment for a learner on Windows or macOS (Python 3.13, uv, dependencies, .env). Use when the learner opens the project for the first time, or says "set up", "install", "get started", or hits a uv sync / Python / dependency error.
---

# Learner setup

The learner is new to evals and may be new to the terminal. Do the setup for them. Don't ask them to run commands, and explain each step in one plain sentence.

This works on **Windows** and **macOS**. Detect the OS first (PowerShell on Windows, zsh/bash on Mac) and use the matching command. Use backslashes in paths on Windows and forward slashes on Mac.

## Steps (run in order, stop and fix at the first failure)

1. **Check uv is installed:** run `uv --version`. If it is missing, ask the learner, then install it:
   - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - Mac: `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `brew install uv` if Homebrew is installed)
   - Have the learner open a new terminal so `uv` is on the PATH, then re-run `uv --version`.
2. **Use Python 3.13, not newer.** The project needs 3.13+, but the newest Python (3.14/3.15) can lack prebuilt packages such as `regex`. uv then tries to compile them and fails. Run (same on both systems):
   - `uv python install 3.13`
   - `uv python pin 3.13`
3. **Rebuild the virtual environment** if `.venv` already exists, since it may have been built with the wrong Python. Read `.venv/pyvenv.cfg` (Windows: `.venv\pyvenv.cfg`); if the version is not 3.13.x, delete `.venv`:
   - Windows: `Remove-Item -Recurse -Force .venv`
   - Mac: `rm -rf .venv`
4. **Install dependencies:** `uv sync --python 3.13` (same on both systems).
5. **Create the env file:** if `.env` does not exist, copy `env.example` to `.env`:
   - Windows: `Copy-Item env.example .env`
   - Mac: `cp env.example .env`
   - Never write API keys yourself. Tell the learner which line to fill in and where to get the key, and let them paste it.
6. **Verify:** run `uv run python -c "import litellm, pandas, fastapi; print('Setup OK')"` (same on both systems). Tell the learner setup worked only if it prints `Setup OK`.

7. **Match the models to the learner's provider:** `env.example` defaults to OpenAI (`MODEL_NAME=openai/gpt-4.1-mini`, `MODEL_NAME_JUDGE=openai/gpt-4.1-nano`). Ask which provider they have a key for (OpenAI, Gemini, Anthropic, Together). If it isn't OpenAI, change both model lines to that provider's models in LiteLLM format (`provider/model`, e.g. `gemini/...`, `anthropic/...`) and tell them which `*_API_KEY` line to uncomment and fill. Read the model lines with Grep for `^MODEL_NAME`; never read or print key lines.
   - **No paid key, or just want to experiment?** Offer the Gemini free tier as an option, not a requirement. The learner creates a free key at https://aistudio.google.com/apikey (Google account, no card needed). Set:
     - `MODEL_NAME=gemini/gemini-3.5-flash-lite`
     - `MODEL_NAME_JUDGE=gemini/gemini-3.5-flash-lite`
     - Have them uncomment `GEMINI_API_KEY=` and paste their key after it.
     - Tell them the free tier has per-minute and per-day request limits. Fine for the chatbot and small experiments, but bulk homework runs (many queries or judge calls) may hit a rate limit (`429`) and need a pause or a paid key.
8. **Run the chatbot and confirm it replies.** It is a long-running server, so the learner starts it in their own terminal with the README command (same on both systems):
   - `uv run uvicorn backend.main:app --reload --reload-include '*.md'`
   - If that command errors (on Windows usually "Got unexpected extra argument (README.md)"), use the fallback instead: `uv run uvicorn backend.main:app --reload`. It works the same, except the learner restarts the server (Ctrl+C, then the command again) after editing `backend/system_prompt.md`.
   - Open http://127.0.0.1:8000 and send a message. Setup is done when the bot replies.
   - `uv run` uses `.venv` automatically, so skip the README's `source .venv/bin/activate` (it doesn't work in PowerShell anyway).
   - `.env` is read only at startup. After any `.env` change, stop the server with Ctrl+C and start it again.

## If something fails

### Setup (steps 1-6)

- **Windows: "Microsoft Visual C++ 14.0 or greater is required"**: uv is on the wrong Python. Redo steps 2-4. Don't ask the learner to install C++ Build Tools unless 3.13 also fails.
- **Mac: "xcrun: error: invalid active developer path", "command not found: cc/clang", or a similar compiler error**: redo steps 2-4 first. If it still fails, ask the learner to run `xcode-select --install`, then retry.
- **"requested Python version is incompatible with requires-python"**: do not use 3.12 or older. This project needs 3.13.
- **`uv` not found right after installing**: the terminal must be closed and reopened.

### Running the chatbot (steps 7-8)

These are edge cases seen in testing. Use them only when the matching error appears.

- **Windows: "Error: Got unexpected extra argument (README.md)"** when starting uvicorn: on Windows, uvicorn's command-line parser expands `*.md` into file names itself, so quoting doesn't help. Have the learner drop the flag: `uv run uvicorn backend.main:app --reload`. The only difference is they restart the server after editing a prompt `.md` file. Mac users don't hit this; keep the README command for them.
- **"litellm.AuthenticationError" or "API key not valid"**: the key line in `.env` is empty, still commented out (`#`), or belongs to a different provider than `MODEL_NAME`. Have the learner fix it, then restart the server.
- **"litellm.NotFoundError" or "model not found"**: the model name is wrong or retired. Switch to a current model from the same provider and restart.
- **"litellm.RateLimitError" or "429 ... quota" (common on the Gemini free tier)**: the learner hit the free tier's request limit. Wait a minute (per-minute limit) or until the next day (daily limit), or slow the run down. It is not a setup problem.
- **"litellm.ServiceUnavailableError ... 503 ... high demand"** (seen with Gemini): the provider is overloaded, not a setup problem. Wait a minute and retry. If it persists, switch `MODEL_NAME` to another model from the same provider and restart. For Gemini, `gemini/gemini-2.0-flash` kept returning 503 in testing and `gemini/gemini-3.5-flash-lite` worked.

### Anything else

- Show the learner the last lines of the error in plain language and say what you will try next.

## Style

The learner is a PM learning evals, not setup. Keep it quick and quiet, and get them to the first lesson as soon as it works.

## Next

When the bot replies in the browser, setup is done. If this skill was invoked by `evals-coach`, return to it. Otherwise invoke `evals-coach` to start stage 1.
