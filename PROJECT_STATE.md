# MedSupply Guard — Project State

## Competition
Gemma 4 Kaggle competition.

## Product
MedSupply Guard is an offline-first medicine inventory copilot for under-resourced clinics. It helps logistics/procurement staff prevent essential medicine stockouts by converting messy inventory, demand, supplier, and pending-order data into explainable procurement recommendations.

## Core claim
MedSupply Guard uses Gemma 4 as the user-facing logistics copilot while deterministic Python tools perform all inventory calculations. The app is designed for privacy-sensitive, low-connectivity environments and avoids clinical advice.

## Scope — Day 1 Locked MVP
Must-have:
- Inventory CSV upload
- Demand history CSV upload
- Supplier lead-time CSV upload
- Pending orders CSV upload
- Stockout risk calculation
- Reorder recommendation
- Supplier feasibility check
- Expiry warning
- Evidence trail
- Gemma 4 explanation layer
- Procurement message generation
- Streamlit demo
- Public repo-ready structure
- Kaggle writeup/video/submission checklist

Nice-to-have, only if time permits:
- Shelf-photo OCR mock or limited prototype
- Multilingual output
- Hugging Face Spaces or Streamlit Cloud deployment
- Synthetic benchmark report

Out of scope:
- Diagnosis
- Prescribing
- Clinical substitution advice
- EHR integration
- Production-grade pharmacy management
- Real supplier APIs
- Authentication/multi-tenant deployment
- Advanced ML forecasting beyond transparent baseline logic

## Primary user story
As a clinic logistics officer with intermittent internet and messy records, I want to upload inventory, dispensing, supplier, and pending-order data so I can quickly see which essential medicines are at risk of stockout, what to order, from whom, and why.

## Architecture
```text
Streamlit UI
  ↓
CSV upload / sample data loader
  ↓
Validation + normalization
  ↓
Deterministic analytics
  - days of cover
  - projected stockout date
  - reorder quantity
  - supplier feasibility
  - expiry risk
  - pending-order adjustment
  ↓
Gemma 4 logistics copilot
  - grounded explanations
  - user Q&A
  - procurement message generation
  - refusal of clinical advice
  ↓
Evidence-backed dashboard and action plan
```

## Technical principles
- Python calculations are the source of truth for math.
- Gemma 4 explains, summarizes, structures, and communicates decisions.
- Every recommendation should show data evidence and assumptions.
- The app supports logistics/procurement decisions only.
- The demo must be narrow, reliable, and story-driven.

Day 3 completed: Gemma 4 integration is complete.
- Added `GemmaClient` supporting `mock` and `ollama` modes.
- Default constrained local model is `gemma4:e2b`.
- Added safety layer to detect and refuse clinical advice queries.
- UI now supports stockout risk explanation, procurement message generation, and logistics Q&A.
- Deterministic analytics are passed directly as structured context to prevent hallucinations.
- 16 tests passing, including tests for LLM client failure states.

## Open risks
- Gemma 4 runtime integration path must be finalized.
- Live demo hosting path must be selected.
- Video must prioritize story and real app screen recording.
- Synthetic data must feel realistic but remain clearly synthetic.

## Next session startup instruction
Start each session by reviewing this file, TASKS.md, DECISIONS.md, and SUBMISSION_CHECKLIST.md. Then update priorities based on current repo status, tests, and blockers.

## Day 4 Status - Complete

Day 4 focused on UI polish, adding the Oxytocin demo scenario, improving Q&A ranking prompts for supplier infeasibility, and generating submission assets (writeup, video storyboard). Tests passed and mock mode successfully prioritizes Oxytocin due to supplier infeasibility.

## Day 3 Status - Complete

Day 3 completed the Gemma 4 integration layer.


Implemented:
- Hybrid-safe `GemmaClient` architecture.
- `GEMMA_BACKEND=mock` fallback mode.
- `GEMMA_BACKEND=ollama` local runtime mode.
- `GEMMA_MODEL` environment variable, tested with `gemma4:e2b`.
- Prompt loading from the `prompts/` directory.
- Gemma-generated stockout explanations.
- Gemma-generated procurement messages.
- Logistics Q&A over deterministic analytics context.
- Clinical-advice refusal path.
- Output cleaning to prevent reasoning / "Thinking Process" leakage.
- Safety utility: `is_clinical_question()`.
- Tests for Gemma client behavior and clinical guardrails.

Verified:
- Mock mode works.
- Ollama mode works with `gemma4:e2b`.
- Oxytocin Injection explanation uses deterministic analytics values.
- Procurement message uses actual reorder quantity and supplier.
- Clinical dosage question is refused safely.
- All tests passed after Day 3 integration.

Important architecture rule:
Gemma 4 does not calculate stockout risk, reorder quantities, supplier feasibility, expiry risk, or pending-order impact. Those remain deterministic Python analytics. Gemma receives structured deterministic context and generates explanations, procurement text, logistics Q&A, and safety refusals.
