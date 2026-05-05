from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts"


class GemmaClient:
    """Thin Gemma 4 integration wrapper.

    Replace `generate` with the competition-supported Gemma 4 runtime/API.
    Keep this class small so model integration changes are isolated.
    """

    def __init__(self, model_name: str = "gemma-4", offline_stub: bool = True):
        self.model_name = model_name
        self.offline_stub = offline_stub

    def _load_prompt(self, filename: str) -> str:
        return (PROMPT_DIR / filename).read_text(encoding="utf-8")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if self.offline_stub:
            return (
                "[Gemma 4 stub] Replace this stub with the actual Gemma 4 runtime. "
                "The deterministic analytics are ready; this layer should generate grounded explanations and procurement text."
            )
        raise NotImplementedError("Wire this method to the chosen Gemma 4 runtime/API.")

    def explain_stockout_risk(self, analytics_row: dict[str, Any]) -> str:
        system = self._load_prompt("system_logistics_copilot.md")
        task = self._load_prompt("explain_stockout_risk.md")
        user = f"{task}\n\nAnalytics context JSON:\n{json.dumps(analytics_row, default=str, indent=2)}"
        return self.generate(system, user)

    def generate_procurement_message(self, action_plan: dict[str, Any]) -> str:
        system = self._load_prompt("system_logistics_copilot.md")
        task = self._load_prompt("generate_procurement_message.md")
        user = f"{task}\n\nAction plan JSON:\n{json.dumps(action_plan, default=str, indent=2)}"
        return self.generate(system, user)
