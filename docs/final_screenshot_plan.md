# Final Screenshot Plan

The following screenshots are required to demonstrate the complete functionality and safety of MedSupply Guard for the Kaggle submission and documentation:

- [ ] **1. Dashboard Overview:** Full view of the Streamlit app showing the successfully loaded CSV data and the generated inventory table.
- [ ] **2. Oxytocin Demo Scenario:** Close-up of the "Oxytocin Injection" row in the inventory table, highlighting its red/critical status.
- [ ] **3. Risk Table - Supplier Reason:** Specific capture of the risk table showing the `supplier_reason` explicitly detailing the infeasibility (e.g., "Supplier lead time (8 days) exceeds stockout window (6 days)").
- [ ] **4. Gemma Explanation:** Screenshot of the Gemma 4 Copilot section showing a successfully generated, deterministic "Risk Explanation" for Oxytocin Injection.
- [ ] **5. Procurement Message:** Screenshot of the Gemma 4 Copilot section showing the drafted "Emergency Procurement Message" addressed to the backup supplier.
- [ ] **6. Logistics Q&A:** Screenshot of the Q&A box where the user asked "Why prioritize Oxytocin?" and Gemma's mathematically grounded response.
- [ ] **7. Clinical Refusal:** Screenshot of the Q&A box where the user asked for clinical advice (e.g., "What is the dosage for Oxytocin?"), showcasing the red banner refusal message: "I am an inventory and logistics assistant. I cannot provide clinical, diagnostic, or prescribing advice."
- [ ] **8. Architecture Diagram:** A capture of the project's architecture diagram (`docs/architecture_diagram.md` or rendered image) detailing the flow from CSV to Python Engine to Guardrails to Gemma 4.
