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

## Current status
Day 1 initialized: repository scaffold, state files, prompt files, sample data, Streamlit shell, analytics module, and tests created.

## Open risks
- Gemma 4 runtime integration path must be finalized.
- Live demo hosting path must be selected.
- Video must prioritize story and real app screen recording.
- Synthetic data must feel realistic but remain clearly synthetic.

## Next session startup instruction
Start each session by reviewing this file, TASKS.md, DECISIONS.md, and SUBMISSION_CHECKLIST.md. Then update priorities based on current repo status, tests, and blockers.
