# MedSupply Guard: Offline-First Gemma 4 Copilot for Clinic Logistics

## Subtitle
Preventing essential medicine stockouts with deterministic analytics and grounded local Gemma 4 explanations.

## Submission Track
**Impact Track**

MedSupply Guard is submitted to the Impact Track because it targets a practical, high-stakes logistics problem: helping resource-constrained clinics see essential medicine stockout risk early enough to act.

## Problem

In many clinics, the problem is not that medicine does not exist. It is that no one sees the stockout coming early enough.

Inventory is often tracked across spreadsheets, manual stock sheets, delayed supplier updates, and fragmented demand records. A medicine shelf can look acceptable today while a critical item is only days away from running out. Logistics staff need fast answers: What will run out first? Which supplier can arrive in time? What should be reordered now?

A generic chatbot is not enough for this setting. If an AI system invents stock quantities, reorder dates, supplier options, or clinical advice, it can create real operational risk. MedSupply Guard is built around a stricter principle: deterministic code calculates the facts; Gemma 4 explains them.

## Solution

**MedSupply Guard** is an offline-first medicine inventory logistics copilot. It ingests structured CSV data for inventory, demand history, suppliers, and pending orders. A deterministic Python analytics engine calculates days of cover, projected stockout dates, risk levels, reorder quantities, supplier feasibility, expiry warnings, and pending-order impact.

Gemma 4 is then used as the communication layer. It turns structured analytics output into clear stockout explanations, procurement messages, and logistics Q&A. The app is intentionally scoped to logistics and procurement support only. It does not provide diagnosis, dosage, prescribing, treatment advice, or clinical substitution recommendations.

The core value is time: time to reorder, time to choose the fastest feasible supplier, and time to escalate before a shelf goes empty. A deterministic What-if Scenario Simulator lets managers test demand surges, supplier delays, stock count corrections, pending order delays, and combined shocks without modifying source CSV files.

## Architecture

The system uses a hybrid-safe architecture:

1. **CSV inputs:** inventory, demand history, suppliers, and pending orders.
2. **Deterministic analytics engine:** Python and Pandas compute stockout, reorder, supplier, expiry, and pending-order logic.
3. **Structured analytics context:** calculated results are packaged into a controlled dictionary.
4. **GemmaClient abstraction:** the UI calls Gemma through a single interface, never directly.
5. **Backends:** `GEMMA_BACKEND=mock` supports deterministic testing and demos; `GEMMA_BACKEND=ollama` runs local Gemma 4 through Ollama.
6. **Streamlit UI:** provides the risk dashboard, Oxytocin demo scenario, Gemma explanation, procurement message, Q&A, and clinical refusal flow.

The local demo uses `gemma4:e2b` through Ollama because it fits constrained hardware better than larger Gemma 4 variants. The architecture remains model-flexible: stronger environments can switch to larger Gemma 4 variants by changing `GEMMA_MODEL`.

## How Gemma 4 Is Used

Gemma 4 is used only after deterministic analytics are complete. It receives structured context such as medicine name, current stock, days of cover, projected stockout date, risk level, supplier rationale, expiry warning, and recommended reorder quantity.

Gemma 4 performs four user-facing tasks:

- **Risk explanation:** explains why a medicine is at stockout risk.
- **Procurement messaging:** drafts supplier-facing or internal procurement text using calculated values.
- **Logistics Q&A:** answers operational questions grounded in the loaded inventory data.
- **Safety refusal:** supports logistics-only refusal behavior when users ask clinical questions.

The main demo scenario focuses on **Oxytocin Injection**. The app identifies a critical procurement problem: the clinic has about six days of cover, and no supplier can arrive before projected stockout. This is more than a “low stock” alert; it is a supplier feasibility warning that requires urgent action.

## Safety and Trust

MedSupply Guard uses several guardrails:

- **No LLM math:** Gemma does not calculate stockout dates, reorder quantities, or supplier feasibility.
- **Grounded context:** prompts instruct Gemma to use only deterministic analytics context.
- **Clinical boundary:** dosage, diagnosis, prescribing, side effects, contraindications, treatment, and clinical substitution questions are intercepted and refused.
- **Transparent outputs:** the dashboard shows the analytics behind recommendations.
- **Fallback mode:** mock mode supports testing and demos when a local model is unavailable.

This separation makes the app auditable. If a reorder recommendation needs review, the deterministic formula and source data can be inspected directly.

## Evaluation

The project includes an automated test suite with **20 passing tests**. Tests cover deterministic logistics calculations, supplier infeasibility, expiry warnings, pending orders, mock Gemma behavior, missing-value handling, and clinical refusal.

Manual verification confirmed:

- Oxytocin Injection is highlighted as a critical supplier-infeasibility scenario.
- Gemma 4 E2B via Ollama generates logistics-only explanations.
- Procurement messages use actual deterministic values rather than placeholders.
- Clinical dosage questions are refused safely.
- The demo section updates dynamically when sample inventory data changes.

## Limitations and Future Work

The MVP currently uses structured CSV inputs rather than scanned paper records. Future work could add local OCR for paper stock sheets, multilingual logistics interfaces, offline tablet deployment, anomaly detection, supplier API synchronization, and multi-clinic depot planning.

The current app is not a production medical system and does not replace pharmacists, clinicians, or procurement officers. It is a focused logistics support tool.

## Impact

MedSupply Guard demonstrates a practical pattern for safe AI in high-stakes operational environments: deterministic systems make operational calculations, open models communicate and assist, and guardrails keep the system within scope.

For clinics with limited connectivity and limited procurement staff, the impact is practical: earlier stockout warnings, faster supplier decisions, clearer escalation messages, and safer use of local AI. By combining deterministic supply-chain analytics with grounded Gemma 4 language generation, MedSupply Guard offers a blueprint for trustworthy offline AI in essential medicine logistics.
