# Evaluation Summary

The MedSupply Guard application has been thoroughly evaluated against a suite of deterministic tests, integration tests with Gemma 4 mocks, and manual validation scenarios.

## Result Summary

| Evaluation Category | Status | Total Tests | Pass Rate |
| :--- | :--- | :--- | :--- |
| **Deterministic Analytics** | PASS | 10 | 100% |
| **Gemma Mock Tests** | PASS | 9 | 100% |
| **Ollama E2B Verification** | PASS | Manual | 100% |
| **Clinical Refusal Test** | PASS | Automated & Manual | 100% |
| **Demo Scenario Validation** | PASS | Manual | 100% |

## Detailed Evaluation Log

### 1. Deterministic Analytics Tests (`tests/test_inventory_math.py`)
- **Coverage**: Calculates days of cover, risk levels, recommended order amounts, and flags supplier feasibility.
- **Key finding**: Safely limits order recommendations to max capacity and correctly identifies when no supplier can meet the required arrival time.
- **Result**: All 10 tests passed seamlessly.

### 2. Gemma Mock Integration Tests (`tests/test_gemma_client.py`)
- **Coverage**: Evaluates the prompt formulation, cleaner methods, and output generation of `GemmaClient` using deterministic mocks.
- **Key finding**: The application effectively uses structured data contexts to generate accurate stockout warnings and targeted procurement messages.
- **Result**: All 9 tests passed.

### 3. Ollama E2B Verification
- **Methodology**: Manually running the application with `gemma4:e2b` via Ollama.
- **Observation**: The app correctly routes requests to the local Gemma instance. Outputs successfully prioritize logistics advice over generic responses and successfully interpret data inputs.
- **Result**: Pass. System behaves deterministically even with live model.

### 4. Clinical Refusal Test
- **Methodology**: Automated tests simulate queries requesting medical advice (e.g., "What is the dosage for Oxytocin?").
- **Observation**: Safety guardrail blocks any clinical advice and outputs a pre-defined fallback message: "I am an inventory and logistics assistant...".
- **Result**: Pass. Guardrails operate effectively before contacting the LLM.

### 5. Demo Scenario Validation
- **Scenario**: Oxytocin Injection stockout risk with supplier infeasibility.
- **Methodology**: Loaded sample `assets/` CSV files. Verified dashboard highlights Oxytocin, displays supplier infeasibility warning, and generates a context-aware procurement message.
- **Result**: Pass. End-to-end functionality confirmed.
