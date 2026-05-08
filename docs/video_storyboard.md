# MedSupply Guard: Demo Video Storyboard (3 Minutes)

## 0:00 - 0:20: Problem Hook
- **Visuals:** Title screen, transitioning to messy CSV data in a spreadsheet.
- **Narrative:** "Under-resourced clinics face critical medicine stockouts because managing messy inventory and supplier records manually is slow and error-prone. MedSupply Guard solves this offline with deterministic analytics and Gemma 4."

## 0:20 - 0:45: Messy Data to Dashboard
- **Visuals:** Show the Streamlit UI. Upload the sample CSVs. The "Stockout risk dashboard" loads instantly.
- **Narrative:** "We upload standard inventory, demand, and supplier CSVs. The Python engine deterministically calculates days of cover and risk levels—no LLM hallucinations."

## 0:45 - 1:25: Oxytocin Demo Scenario
- **Visuals:** Highlight the "Demo Scenario: Oxytocin Injection" section in the UI.
- **Narrative:** "Let's look at a critical case: Oxytocin. We have about 6 days of cover, but the system flags a supplier infeasibility: no supplier can arrive before the projected stockout. It recommends an emergency reorder from the fastest available option."

## 1:25 - 2:00: Gemma Explanation and Procurement Message
- **Visuals:** Scroll down to the Gemma 4 Copilot section. Click "Generate risk explanation" and then "Generate procurement message".
- **Narrative:** "Gemma 4 takes the deterministic data as context. It explains the stockout risk clearly and instantly drafts an emergency procurement email to the supplier, ready to send."

## 2:00 - 2:30: Safety, Evidence, and Refusal
- **Visuals:** Type a logistics question: "Why prioritize Oxytocin?". Show Gemma's response citing the supplier infeasibility rule. Then type a clinical question: "What is the dosage for Oxytocin?". Show the safety refusal message.
- **Narrative:** "Gemma correctly ranks Oxytocin as top priority due to supplier constraints. Crucially, if asked for clinical advice like dosage, our guardrails immediately block it."

## 2:30 - 3:00: Impact and Architecture Close
- **Visuals:** Architecture diagram overlay. Link to GitHub repo.
- **Narrative:** "MedSupply Guard runs locally using Ollama and Gemma 4, ensuring privacy, reliability without internet, and mathematically safe logistics support. Thank you."
