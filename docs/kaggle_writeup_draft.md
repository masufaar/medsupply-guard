# MedSupply Guard: Offline-First Gemma 4 Copilot for Clinic Logistics

## Track Recommendation
**Primary Track:** Health & Accessibility
*(Note: Can also apply to Local Copilots / Productivity)*

## 1. Problem Statement
In resource-constrained environments, clinics frequently face critical stockouts of life-saving medicines. Managing supply chains effectively requires balancing current inventory against unpredictable demand and variable supplier lead times. Clinic logistics staff often manage these variables using messy, disparate CSV records or manual data entry with limited or non-existent internet connectivity. They need rapid insights into what to order, when to order it, and from whom. Crucially, any assistive technology deployed in these environments must be perfectly reliable—hallucinating inventory quantities or offering unsafe clinical advice could have devastating real-world consequences.

## 2. Solution
**MedSupply Guard** is an offline-first inventory logistics copilot powered by the open-weights Gemma 4 model. It acts as an intelligent, hybrid pipeline. It converts raw CSV data (inventory, demand history, suppliers, pending orders) into actionable, deterministic procurement plans. It then uses Gemma 4 to translate these analytical findings into human-readable risk explanations, draft emergency procurement communications, and answer ad-hoc logistical queries.

By decoupling the math from the language generation, MedSupply Guard ensures that all numbers are exact and verifiable, while still providing the intuitive interaction experience of a modern Large Language Model.

## 3. Architecture
The architecture is designed specifically to maximize reliability and data privacy:

- **Deterministic Analytics Engine:** Built with Python and Pandas, this engine acts as the source of truth. It calculates days of cover, projected stockout dates, recommended reorder quantities (capped by maximum capacity), and supplier feasibility (flagging if lead times exceed stockout windows).
- **Structured Analytics Context:** The analytical outputs are packaged into a clear, structured format.
- **GemmaClient Interface:** An abstraction layer that communicates with the LLM backends.
- **Ollama Backend (`gemma4:e2b`):** Facilitates local execution of the Gemma 4 model, ensuring data privacy and operability without an internet connection.
- **Mock Backend:** Allows the application to be tested and demonstrated purely deterministically, without requiring the local model to be loaded.
- **Streamlit UI:** Provides a user-friendly dashboard for logistics personnel.

## 4. How Gemma 4 is Used
Gemma 4 is strictly utilized for its natural language capabilities, specifically constrained to the logistics domain:

- **Risk Explanation:** Gemma consumes the deterministic data context to generate concise, grounded explanations of why specific medicines are at risk (e.g., highlighting that demand has spiked or suppliers are too slow).
- **Procurement Communication:** It automatically drafts emergency procurement emails to suppliers based on calculated shortfalls, saving critical administrative time.
- **Logistics Q&A:** It answers specific supply chain queries, such as "Why are we prioritizing Oxytocin over Amoxicillin?", using the provided analytical context to form its reasoning.

## 5. Safety and Trust Guardrails
Trust is the most important feature of healthcare technology. MedSupply Guard implements several layers of safety:

- **No LLM Math:** All inventory levels, dates, and order quantities are calculated deterministically. The LLM only receives and formats the results, eliminating the risk of hallucinated stock levels.
- **Clinical Refusal:** A rigorous regex-based pattern matcher scans all user inputs before they reach the LLM. If an input appears to ask for clinical advice, diagnostics, or dosage information, the system blocks the request and returns a deterministic refusal message: "I am an inventory and logistics assistant. I cannot provide clinical, diagnostic, or prescribing advice."
- **Prompt Engineering:** System prompts are strictly scoped to command the model to only act as a procurement assistant and to only use the provided context.

## 6. Evaluation
The application has been validated to ensure perfect alignment with its safety constraints:

- **Automated Test Suite:** Achieved 100% pass rate across 19 Pytest cases.
- **Deterministic Validations:** Comprehensive tests confirm the math engine handles edge cases, such as supplier infeasibility correctly.
- **Guardrail Testing:** Refusal mechanisms successfully intercept simulated clinical queries.
- **End-to-End Mocks:** Ensure the UI functions identically regardless of whether the live Gemma 4 model or the deterministic mock backend is active.

## 7. Limitations and Future Work
- **Data Ingestion:** The current MVP relies on structured CSVs. Future iterations aim to integrate local OCR to digitize paper logbooks directly.
- **Live Integration:** While the offline-first design is a core feature, optional synchronization with real-time supplier APIs would enhance predictive capabilities when internet is sporadically available.
- **Scale:** Extending support to complex multi-clinic depot networks.

## 8. Impact
MedSupply Guard demonstrates how powerful open-weight models like Gemma 4 can be safely deployed in critical, resource-limited health environments. By combining the absolute certainty of deterministic code with the communicative power of Gemma, it offers a blueprint for building trustworthy, offline AI solutions that directly address global health supply chain challenges.
