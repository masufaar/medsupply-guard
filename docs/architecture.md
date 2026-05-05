# MedSupply Guard Architecture

## Summary
MedSupply Guard combines deterministic inventory analytics with a Gemma 4 logistics copilot. The deterministic layer performs all stockout, reorder, supplier, and expiry calculations. Gemma 4 provides grounded explanations, procurement messages, and natural-language interaction.

## Components
1. Streamlit UI
2. CSV ingestion and validation
3. Inventory analytics module
4. Gemma 4 client wrapper
5. Prompt library
6. Evaluation log and tests

## Agent design
One main Gemma 4 logistics copilot has access to deterministic tool outputs. The agent does not perform raw calculations and does not provide clinical advice.

## Tool responsibilities
- calculate days of cover
- estimate projected stockout date
- classify risk level
- compute reorder quantity
- compare supplier lead time feasibility
- identify expiry warnings
- retrieve evidence IDs

## Safety boundary
The app supports logistics/procurement only. Clinical questions are refused and redirected to qualified clinicians/pharmacists.
