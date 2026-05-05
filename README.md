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
streamlit run app.py
```

## Tests
```bash
pytest
```

## Sample data
Synthetic sample data is in `data/sample/`.
