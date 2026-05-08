# MedSupply Guard: Offline-First Gemma 4 Copilot for Clinic Logistics

## Track Recommendation
**Primary Track:** Health & Accessibility
*(Note: Can also apply to Local Copilots / Productivity)*

## 1. Problem Statement
Under-resourced clinics face critical stockouts of essential medicines. Clinic logistics staff often manage inventory, demand, and suppliers using messy CSV records or manual data entry with limited connectivity. They need rapid insights into what to order and from whom, without the risk of an AI hallucinating inventory quantities or offering unsafe clinical advice.

## 2. Solution
**MedSupply Guard** is an offline-first inventory logistics copilot powered by Gemma 4. It converts raw CSV data (inventory, demand history, suppliers, pending orders) into actionable, deterministic procurement plans, and uses Gemma to explain these risks and draft procurement messages.

## 3. Architecture & How Gemma 4 is Used
- **Deterministic Analytics Engine:** Python calculates days of cover, projected stockout dates, recommended reorder quantities, and supplier feasibility. This is the source of truth.
- **Gemma 4 Copilot:** Receives the deterministic structured context. It generates grounded stockout explanations, drafts procurement emails, and answers logistics Q&A (e.g., "Why are we prioritizing Oxytocin?").
- **Offline-First:** Supports `gemma4:e2b` via Ollama for local execution, ensuring privacy and reliability without internet access.

## 4. Safety Guardrails
- **No LLM Math:** Inventory calculations are deterministic to prevent hallucinated stock levels.
- **Strict Scope:** Prompt constraints and safety functions strictly block clinical advice (diagnosis, dosage, prescribing).

## 5. Evaluation & Impact
- Validated via automated test suite against synthetic clinic datasets.
- Tested successfully to ensure proper handling of supplier infeasibility and prompt leakage prevention.

## 6. Limitations & Future Work
- Currently relies on structured CSVs; future work could include OCR for paper logbooks.
- Real-time supplier API integration would enhance the offline capability.

## 7. Demo Narrative (Video Reference)
A 3-minute walk-through showing a critical scenario: Oxytocin Injection is at risk, and the primary supplier cannot deliver in time. The app demonstrates the Python analytics detecting the risk, and Gemma 4 explaining the supplier infeasibility and drafting an emergency procurement message.
