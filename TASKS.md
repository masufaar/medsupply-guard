# MedSupply Guard — Tasks

## Day 1 — Product lock and repo skeleton
- [x] Lock narrow MVP scope
- [x] Define primary user story
- [x] Define architecture
- [x] Create repo structure
- [x] Create sample synthetic data
- [x] Create Streamlit shell
- [x] Create deterministic calculation module
- [x] Create initial prompt files
- [x] Create project management files
- [x] Run app locally
- [x] Run tests locally
- [ ] Commit initial repo to GitHub

## Day 2 — Analytics engine
- [x] Harden data validation
- [x] Improve stockout/risk ranking logic
- [x] Add safety stock / target coverage logic
- [x] Add supplier feasibility scoring
- [x] Add expiry risk classification
- [x] Add benchmark scenarios
- [x] Expand pytest coverage

## Day 3 — Gemma 4 integration
- [x] choose Gemma 4 runtime path
- [x] wire Gemma client
- [x] connect prompt templates
- [x] generate stockout explanations
- [x] generate procurement messages
- [x] add clinical-advice refusal behavior
- [x] add Gemma output examples to EVAL_LOG.md
- [x] update README with model usage

## Day 4 — UI polish
- [ ] Improve Streamlit dashboard layout
- [ ] Add evidence panel
- [ ] Add action-plan page
- [ ] Add sample scenario one-click loader
- [ ] Add charting
- [ ] Add disclaimer and safety boundaries

## Day 5 — Evaluation and robustness
- [ ] Run golden scenario tests
- [ ] Fill EVAL_LOG.md
- [ ] Document benchmark results
- [ ] Improve prompts based on failures
- [ ] Write README setup instructions

## Day 6 — Submission assets
- [ ] Draft Kaggle writeup under 1,500 words
- [ ] Draft video script
- [ ] Create cover image
- [ ] Capture screenshots
- [ ] Clean repository

## Day 7 — Final packaging
- [ ] Record final demo video
- [ ] Upload YouTube video
- [ ] Verify public repo link
- [ ] Verify live demo or downloadable demo files
- [ ] Finalize Kaggle writeup
- [ ] Submit

## Day 3 - Gemma 4 Integration

Status: Complete

Completed:
- [x] Choose Gemma 4 runtime path.
- [x] Add `GemmaClient` abstraction.
- [x] Support mock backend.
- [x] Support Ollama backend.
- [x] Default local model to `gemma4:e2b`.
- [x] Load prompts from `prompts/`.
- [x] Generate stockout risk explanations.
- [x] Generate procurement messages.
- [x] Add logistics Q&A.
- [x] Add clinical-advice refusal behavior.
- [x] Add `src/llm/safety.py`.
- [x] Add Gemma client tests.
- [x] Verify mock mode.
- [x] Verify Ollama mode with `gemma4:e2b`.
- [x] Update README with runtime strategy.

## Day 4 - UI Polish, Prompt Hardening, Demo Flow

Planned:
- [ ] Improve UI layout for demo readability.
- [ ] Make the Gemma Copilot section clearer.
- [ ] Add a "demo scenario" flow for Oxytocin Injection.
- [ ] Strengthen Q&A prompt so supplier infeasibility is prioritized above simple days-of-cover when relevant.
- [ ] Add screenshots for README / Kaggle media gallery.
- [ ] Add architecture diagram.
- [ ] Draft Kaggle writeup outline.
- [ ] Draft 3-minute video storyboard.
- [ ] Review README for judge-facing clarity.
