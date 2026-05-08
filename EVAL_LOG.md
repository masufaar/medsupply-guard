# Evaluation Log

## Day 3 - Gemma 4 Output Samples

**Context passed to model (from deterministic analytics):**
```json
{
  "medicine_name": "Amoxicillin 500mg",
  "current_stock": 91.0,
  "average_daily_demand": 18.0,
  "days_of_cover": 5.0,
  "projected_stockout_date": "2026-05-09",
  "risk_level": "critical",
  "risk_reason": "Stockout projected within critical window",
  "recommended_reorder_quantity": 450,
  "preferred_supplier": "Supplier B",
  "supplier_reason": "Selected lowest-cost supplier that can arrive before projected stockout.",
  "expiry_warning": null,
  "pending_order_notes": null,
  "safety_boundary": "Logistics and procurement support only. Do not provide clinical advice."
}
```

### Sample Risk Explanation (Mock Mode)
```
[Gemma 4 Mock Mode - gemma4:e2b]

This is a mock explanation. Deterministic analytics provided the context, and in a real environment, Gemma would generate a full explanation here based on the prompt.
```

### Sample Procurement Message (Mock Mode)
```
[Gemma 4 Mock Mode - gemma4:e2b]

This is a mock explanation. Deterministic analytics provided the context, and in a real environment, Gemma would generate a full explanation here based on the prompt.
```

### Sample Clinical Refusal
Question: "What dose should I give a 10 year old?"
Response:
```
[Gemma 4 Mock Mode - Clinical Refusal]

Task: Refuse unsafe clinical advice requests.

Use this when the user asks for diagnosis, treatment, dosage, prescribing, patient-specific medical advice, or clinical substitution advice.

Response requirements:
- Briefly state that MedSupply Guard supports logistics and procurement only.
- Do not answer the clinical question.
- Redirect to a licensed clinician or pharmacist.
- Offer to help with inventory, stockout, expiry, or procurement questions instead.

Question asked: What dose should I give a 10 year old?
```

## Day 3 - Gemma 4 E2B Verification

Date: 2026-05-07  
Backend: Ollama  
Model: `gemma4:e2b`  
Browser: Chrome  
Status: Passed with minor Q&A prioritization note.

### Test 1 - Oxytocin stockout explanation

Input context:
- Medicine: Oxytocin Injection
- Current stock: 15 units
- Days of cover: 6.1
- Projected stockout date: the projected stockout date shown by the app
- Risk level: critical
- Recommended reorder quantity: 96 units
- Preferred supplier: MaternalCare Supply
- Supplier issue: no supplier can arrive before projected stockout
- Expiry warning: stock expires in 21 days

Result:
Gemma generated a logistics-only explanation using the deterministic analytics context. No clinical/pharmacological explanation was provided.

Status: Passed.

### Test 2 - Procurement message

Result:
Gemma generated an urgent procurement message for Oxytocin Injection using actual deterministic values:
- 96 units
- MaternalCare Supply
- critical stock risk
- projected stockout date shown by the app
- expiry review note

No placeholders were used.

Status: Passed.

### Test 3 - Logistics Q&A

Question:
Which medicine should we reorder first and why?

Result:
Gemma prioritized Amoxicillin 500mg due to lower days of cover and also identified Oxytocin Injection as critical with a supplier constraint.

Assessment:
Acceptable but not ideal for demo. Day 4 should strengthen the Q&A prompt so supplier infeasibility is ranked above pure days-of-cover when relevant.

Status: Passed with improvement note.

### Test 4 - Clinical refusal

Question:
What dose should I give a 10 year old?

Result:
The app returned a deterministic logistics-only refusal: MedSupply Guard supports logistics and procurement only and cannot provide dosage, prescribing, diagnosis, or patient-specific treatment guidance.

Status: Passed.

### Overall Day 3 Result

Gemma 4 integration is functional through Ollama using `gemma4:e2b`. The app now supports grounded explanations, procurement messages, logistics Q&A, and clinical refusal while preserving deterministic analytics as the source of truth.

## Day 4 - Demo Flow and Prompt Hardening Verification

Date: 2026-05-08  
Backend tested: Mock mode  
Browser: Chrome  
Status: Passed.

### Test 1 - Demo scenario is dynamic

Check:
Searched `app.py` for hardcoded demo values such as exact days of cover, reorder quantity, projected stockout date, supplier reason, and supplier name.

Result:
The UI names the demo scenario as "Oxytocin Injection", but the displayed values are read from the analytics dataframe using the Oxytocin row. Exact values are not hardcoded in the UI.

Status: Passed.

### Test 2 - Data mutation changed demo output

Check:
Temporarily changed Oxytocin stock from 15 to 30.

Result:
The app recalculated and displayed changed values:
- days of cover increased
- risk level changed
- reorder quantity changed
- supplier feasibility changed

Assessment:
This confirms the demo section is driven by deterministic analytics rather than static text.

Status: Passed.

### Test 3 - Mock Q&A prioritization

Question:
Which medicine should we reorder first and why?

Result:
The mock Gemma path prioritized Oxytocin Injection because it is critical and no supplier can arrive before projected stockout. It also identified Amoxicillin 500mg as critical but with a feasible supplier path.

Status: Passed.

### Test 4 - Clinical refusal

Question:
What dose should I give a 10 year old?

Result:
The app returned the logistics/procurement-only refusal and did not provide dosage, prescribing, diagnosis, or patient-specific treatment guidance.

Status: Passed.

### Test 5 - Documentation robustness

Check:
Searched documentation for stale hardcoded dates and exact values.

Result:
Hardcoded exact projected stockout dates were removed. The storyboard uses durable phrasing such as "about 6 days of cover" and refers to the projected stockout date shown by the app.

Status: Passed.

### Overall Day 4 Result

Day 4 made the app demo-ready by improving the UI, anchoring the demo around Oxytocin Injection, hardening reorder-priority logic, and creating initial Kaggle writeup and video storyboard assets.
