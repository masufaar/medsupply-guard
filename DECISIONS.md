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

## D010 - Use hybrid-safe Gemma runtime architecture

Decision:
MedSupply Guard uses a `GemmaClient` abstraction instead of calling Ollama directly from `app.py`.

Reason:
This keeps the app model-flexible and makes the Gemma 4 implementation easy for Kaggle judges to verify. The same app can run in mock mode, local Ollama mode, or later in a stronger Kaggle/cloud runtime.

## D011 - Use `gemma4:e2b` for constrained local Ollama runtime

Decision:
The local development machine uses `gemma4:e2b` through Ollama.

Reason:
`gemma4:e4b` exceeded available system memory. `gemma4:e2b` successfully runs locally and fits the project's constrained/offline deployment story.

## D012 - Keep mock mode as a required development fallback

Decision:
`GEMMA_BACKEND=mock` remains available even after Ollama integration.

Reason:
Mock mode allows UI testing, CI testing, and demo-flow development even when Ollama is unavailable, slow, or memory-constrained.

## D013 - Gemma 4 explains; Python calculates

Decision:
Gemma 4 is used only for explanation, procurement-message generation, logistics Q&A, and clinical-advice refusal.

Reason:
Inventory calculations must remain deterministic, testable, and auditable. Gemma receives structured analytics context and must not invent stockout dates, reorder quantities, supplier choices, or expiry logic.

## D014 - Clinical advice is blocked before model generation

Decision:
Clinical questions are detected before Gemma generation and routed to a deterministic refusal.

Reason:
MedSupply Guard is a logistics/procurement tool, not a clinical decision-support system. It must not answer dosage, prescribing, diagnosis, treatment, side-effect, contraindication, or patient-specific medical questions.

## D015 - Keep Day 4 demo scenario analytics-driven

Decision:
The Oxytocin Injection demo section may explicitly highlight Oxytocin as the story scenario, but all displayed values must be read from deterministic analytics output.

Reason:
This prevents the demo from becoming hardcoded theater. Judges should be able to inspect the code and see that stockout risk, days of cover, reorder quantity, supplier rationale, and expiry warning come from the analytics engine.

## D016 - Prioritize supplier infeasibility above slightly lower days-of-cover

Decision:
When ranking reorder urgency, critical medicines with supplier infeasibility should outrank critical medicines with slightly fewer days of cover but feasible supplier paths.

Reason:
Operational urgency is not only "which item runs out first." A medicine with no supplier able to arrive before stockout can be a harder procurement problem than one with slightly lower days of cover but a feasible supplier route.

## D017 - Use writeup and video storyboard as living submission assets

Decision:
`docs/writeup_outline.md` and `docs/video_storyboard.md` are now treated as submission-planning artifacts.

Reason:
The Kaggle submission depends heavily on story, architecture clarity, and demo quality. Maintaining these files prevents the final writeup and video from becoming last-minute work.
