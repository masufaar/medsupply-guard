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
