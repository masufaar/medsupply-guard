# MedSupply Guard — Decisions

## D001 — Use Streamlit for the MVP
Date: 2026-05-04
Reason: fastest path to a credible interactive demo with low engineering overhead.

## D002 — Use deterministic Python for inventory math
Date: 2026-05-04
Reason: prevent hallucinated calculations and make results auditable.

## D003 — Use Gemma 4 as runtime copilot, not calculator
Date: 2026-05-04
Reason: the model should explain, orchestrate, and communicate grounded recommendations; deterministic tools should compute.

## D004 — Keep the project logistics/procurement-only
Date: 2026-05-04
Reason: avoid clinical advice, diagnosis, prescribing, or unsafe medical substitution recommendations.

## D005 — Use synthetic clinic data for the demo
Date: 2026-05-04
Reason: avoid privacy issues while making the scenario controlled, reproducible, and benchmarkable.

## D006 — Prioritize a narrow, polished demo over broad functionality
Date: 2026-05-04
Reason: competition success depends on a compelling story, working app, visible Gemma 4 usage, and clear technical proof.

## D007 — Keep Gemma out of loop until deterministic logic is trustworthy
Date: 2026-05-05
Reason: Day 2 kept Gemma out of the loop until deterministic calculations were trustworthy.

## D008 — Separate warning fields
Date: 2026-05-05
Reason: The app separates supplier_reason, expiry_warning, pending_order_notes, and risk_reason to prevent one warning from hiding another.

## D009 — Visible supplier-too-slow warnings
Date: 2026-05-05
Reason: Supplier-too-slow warnings must be visible in the dashboard, not only hidden inside expanders.

## D010 — Hybrid-safe Architecture for LLM Integration
Date: 2026-05-07
Reason: Use Gemma 4 exclusively as an explanation and communication layer. Pass deterministic math outputs as a structured context dictionary to prevent hallucinations. The backend supports `mock` and `ollama` with `gemma4:e2b` as the constrained local default.

## D011 — Pre-LLM Clinical Guardrail
Date: 2026-05-07
Reason: Added a deterministic regular expression check in `GemmaClient` to intercept clinical questions (e.g., dosage, prescribing) before they reach the LLM, triggering a hard refusal template.
