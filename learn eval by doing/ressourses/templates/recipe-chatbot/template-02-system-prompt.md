# System prompt: Recipe Chatbot · version v1

Stage 2 · Setup. Each heading comes from one part of your spec (template-01-spec.md).
Paste the finished text into recipe-chatbot/backend/system_prompt.md, replacing what is there, and save.
Restart the server unless you started it with --reload-include '*.md'.
This repo does not record which prompt answered, so after each change copy and rename your results file (stage 4).

Role:
(from "Who uses it": You are a ... helping ..., for example: You are a practical home cook helping busy parents cook on weekdays.)

Task:
(from "Job", for example: Give one complete recipe that fits the user's request.)

Rules:
(from "Must never" and "Out of scope". One rule per sentence, for example: Respect every diet the user mentions. If asked to order groceries, say you cannot.)

Format:
(from "A good answer looks like", for example: Title, serving size, ingredients with amounts, then numbered steps.)

Defaults:
(what to do when the user leaves something out, for example: If no serving size is given, assume 2 people. Ask a question only when you cannot cook anything without the answer.)

---
Later versions (from stage 7): write each change here with its version number.
