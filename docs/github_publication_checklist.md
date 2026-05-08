# GitHub Publication Checklist

Before marking the repository as public or submitting the link, verify the following checks have passed:

- [ ] **No private paths:** Ensure no absolute paths to local user directories (like `C:\Users\...`) remain in configuration files or documentation.
- [ ] **No API keys:** Verify no OpenAI, Anthropic, Gemini, or other secret API keys are hardcoded in the source code or `.env` file templates.
- [ ] **No old project folders:** Confirm that legacy CAIO project folders or unrelated directories have been removed from the repository tree.
- [ ] **README complete:** The `README.md` is fully up-to-date, providing clear instructions for setup, running tests, and understanding the architecture.
- [ ] **Tests pass:** A clean run of `python -m pytest` yields a 100% pass rate.
- [ ] **Requirements present:** The `requirements.txt` is complete, accurate, and lists only the necessary dependencies for the project.
- [ ] **Sample data included:** The `data/sample/` folder contains functional CSVs (inventory, demand, suppliers, pending orders) to allow instant evaluation.
- [ ] **Prompts included:** The `prompts/` directory contains all Gemma system and task prompt text files.
- [ ] **Docs included:** The `docs/` folder contains all final writeup drafts, video scripts, diagrams, and evaluation logs necessary for submission.
