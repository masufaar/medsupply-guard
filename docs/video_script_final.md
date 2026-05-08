# MedSupply Guard: Demo Video Script (3 Minutes)

**Target Length:** Under 3 minutes.
**Focus:** The offline, deterministic safety of the system, using the Oxytocin supplier infeasibility scenario.

---

## Scene 1: The Problem Hook (0:00 - 0:25)

**Visuals:**
- Title screen: "MedSupply Guard: Offline-First Gemma 4 Copilot for Clinic Logistics".
- Cut to a screen showing a messy, hard-to-read CSV file full of medical inventory data.
- Small visual text overlays: "Messy Data", "Manual Entry", "High Risk".

**Narration:**
"Under-resourced clinics face critical stockouts of life-saving medicines because managing supply chains manually is slow and error-prone. Worse, using standard AI to help is risky—hallucinating inventory numbers or giving unsafe clinical advice can be dangerous. MedSupply Guard solves this by combining the absolute safety of deterministic analytics with the communicative power of Gemma 4, all running completely offline."

---

## Scene 2: Loading the Dashboard (0:25 - 0:50)

**Visuals:**
- The Streamlit MedSupply Guard application interface.
- Mouse cursor clicks "Upload CSVs" and selects inventory, demand, and supplier files.
- The "Stockout Risk Dashboard" populates instantly with color-coded risk levels.

**Narration:**
"We start by loading standard CSV files into the system. Our Python analytics engine instantly and deterministically calculates days of cover and risk levels. This is the source of truth—there is absolutely no LLM math happening here, guaranteeing that the numbers are always correct."

---

## Scene 3: The Oxytocin Scenario (0:50 - 1:30)

**Visuals:**
- The cursor highlights the row for "Oxytocin Injection" marked in red (Critical).
- Zooms in on the "Supplier Infeasibility" warning tag.
- Shows the Days of Cover (e.g., 6 days) versus the fastest supplier lead time (e.g., 8 days).

**Narration:**
"Let's look at a critical case: Oxytocin Injection. The dashboard flags a severe risk. We only have six days of cover remaining. Crucially, the system has detected a 'supplier infeasibility'—meaning our primary supplier cannot deliver the medicine before we run out. The deterministic engine automatically calculates a required emergency order to bridge the gap."

---

## Scene 4: Gemma 4 Copilot in Action (1:30 - 2:05)

**Visuals:**
- Scroll down to the "Gemma 4 Logistics Copilot" chat area.
- Click a pre-set button: "Generate Risk Explanation for Oxytocin".
- Gemma outputs a concise explanation citing the exact math.
- Click another button: "Draft Emergency Procurement Message".
- Gemma generates a professional email to the backup supplier.

**Narration:**
"This is where Gemma 4 comes in. Taking only the mathematically verified context, Gemma explains the stockout risk clearly. It then instantly drafts an emergency procurement email to the fastest available supplier, saving clinic staff critical time. It understands the context without ever needing internet access."

---

## Scene 5: Guardrails and Safety (2:05 - 2:40)

**Visuals:**
- In the Q&A box, user types: "Why prioritize Oxytocin?".
- Gemma responds: "Based on the data, Oxytocin is prioritized due to an impending stockout in 6 days and a supplier lead time of 8 days."
- User then types: "What is the dosage for Oxytocin?".
- Instant red banner/refusal message: "I am an inventory and logistics assistant. I cannot provide clinical, diagnostic, or prescribing advice."

**Narration:**
"You can also ask Gemma logistics questions, and it will prioritize intelligently based on the data. But what about safety? If a user accidentally asks for clinical advice, like a dosage requirement, our strict regex-based guardrails intercept it before it even reaches the LLM. Clinical advice is strictly blocked."

---

## Scene 6: Architecture and Impact (2:40 - 3:00)

**Visuals:**
- An overlay of the architecture diagram: CSV -> Python Engine -> Guardrails -> Gemma 4.
- Link to the GitHub repository on screen.

**Narration:**
"MedSupply Guard runs locally using Ollama and the `gemma4:e2b` model. By separating the math from the language model, we ensure data privacy, offline reliability, and mathematically safe logistics support for clinics worldwide. Thank you."
