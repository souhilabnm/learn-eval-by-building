# Recipe chatbot evals course

When a learner opens this project for the first time, or reports a setup, Python, `uv sync` or dependency error, use the `learner-setup` skill to set up their environment for them (Windows and macOS). Don't ask the learner to run setup commands themselves.

For everything after setup, use the `evals-coach` skill. It finds the learner's stage in the playbook and hands off to one stage skill (`evals-spec-and-prompt`, `evals-test-queries`, `evals-error-analysis`, `evals-component-checks`, `evals-improve-and-monitor`). Stage 6 (`evals-llm-judge`, golden set and LLM judge) is not covered yet: never send learners to it. Shared coaching rules are in `.claude/skills/evals-coach/coaching-rules.md`: the learner writes and labels; Claude explains, reviews and gives feedback.
