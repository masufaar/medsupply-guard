# MedSupply Guard — Prompt Changelog

## Template

### YYYY-MM-DD — Prompt file changed
File:
Reason:
Before:
After:
Evaluation result:

## Day 3 - Prompt Hardening for Gemma 4 Integration

Changes:
- Strengthened system prompt to define MedSupply Guard as a logistics/procurement assistant.
- Added instructions that Gemma must use only structured deterministic analytics context.
- Added constraints against clinical/pharmacological explanations.
- Added constraints against diagnosis, dosage, prescribing, treatment, and clinical substitution advice.
- Added final-answer-only instruction to avoid reasoning / "Thinking Process" leakage.
- Updated procurement prompt to require actual context values and avoid placeholders.
- Updated Q&A prompt to use available analytics context instead of asking the user for data already loaded in the app.

Reason:
Initial Ollama outputs behaved like a generic medical assistant and included reasoning traces. Prompt hardening corrected the app toward grounded, logistics-only behavior.

## Day 4 - Supplier Infeasibility Prioritization

Changes:
- Added `CRITICAL RANKING RULE` to `prompts/answer_user_question.md`.
- Explicitly instructed the model to prioritize critical medicines with supplier infeasibility over those with slightly fewer days of cover but feasible suppliers.

Reason:
To ensure the LLM correctly reflects the deterministic severity of a blocked supply chain over a simple days-of-cover sort, improving the validity of logistics Q&A.
