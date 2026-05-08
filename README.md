# MedSupply Guard

Offline-first Gemma 4 copilot for medicine inventory logistics in under-resourced clinics.

## Purpose
MedSupply Guard helps clinic logistics/procurement staff detect essential medicine stockout risks, evaluate supplier lead times, generate reorder recommendations, and create evidence-backed procurement messages.

This is a Kaggle competition prototype. It is not a clinical decision system.

## Safety boundary
MedSupply Guard supports logistics and procurement decisions only. It does not provide diagnosis, prescribing advice, dosage guidance, clinical substitutions, or patient-specific medical recommendations.

## Architecture
- Streamlit UI
- CSV data ingestion
- Deterministic Python inventory analytics
- Gemma 4 runtime copilot for grounded explanations and procurement messages
- Evidence trail for source rows and assumptions

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Mock Mode
```bash
# Windows
$env:GEMMA_BACKEND="mock"
streamlit run app.py
```

### Ollama Mode
```bash
ollama pull gemma4:e2b
# Windows
$env:GEMMA_BACKEND="ollama"
$env:GEMMA_MODEL="gemma4:e2b"
streamlit run app.py
```

### Demo Scenario Flow
When the app launches, check the **Demo Scenario: Oxytocin Injection** section. It highlights a critical stockout risk where suppliers cannot arrive in time, demonstrating how MedSupply Guard handles infeasible supply chains. Use the Gemma 4 Copilot section below to generate a procurement message or ask why Oxytocin is prioritized over Amoxicillin.

## Tests
```bash
pytest
```

## Sample data
Synthetic sample data is in `data/sample/`.
