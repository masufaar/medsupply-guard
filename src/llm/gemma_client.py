import json
import os
from pathlib import Path
from typing import Any, Dict

import requests

from src.llm.safety import is_clinical_question

"""
Gemma 4 Client integration for MedSupply Guard.
Gemma explains and communicates only. It does not perform deterministic calculations.
Both mock and Ollama backends are supported.
"""

PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts"


import re

def clean_model_output(text: str) -> str:
    """Removes reasoning leakage like 'Thinking...' or 'Thinking Process:'."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    
    blocks = text.split("\n\n")
    cleaned_blocks = []
    in_thinking = False
    
    for block in blocks:
        b_lower = block.strip().lower()
        if (b_lower.startswith("thinking...") or 
            b_lower.startswith("thinking process") or 
            b_lower.startswith("**result generation**") or 
            b_lower.startswith("**(result generation)**")):
            in_thinking = True
            if "done thinking" in b_lower:
                in_thinking = False
                parts = re.split(r"(?i)\.\.\.done thinking\.?|done thinking\.?", block)
                if len(parts) > 1 and parts[-1].strip():
                    cleaned_blocks.append(parts[-1].strip())
            continue
            
        if in_thinking:
            if "done thinking" in b_lower:
                in_thinking = False
                parts = re.split(r"(?i)\.\.\.done thinking\.?|done thinking\.?", block)
                if len(parts) > 1 and parts[-1].strip():
                    cleaned_blocks.append(parts[-1].strip())
            else:
                if b_lower.startswith("1.") or b_lower.startswith("- ") or b_lower.startswith("2.") or b_lower.startswith("3."):
                    continue
                else:
                    in_thinking = False
                    cleaned_blocks.append(block)
            continue
            
        if b_lower.startswith("...done thinking.") or b_lower.startswith("done thinking."):
            in_thinking = False
            block = re.sub(r"(?i)^\.\.\.done thinking\.?\s*|^done thinking\.?\s*", "", block)
            if block.strip():
                cleaned_blocks.append(block)
            continue
            
        cleaned_blocks.append(block)
        
    return "\n\n".join(cleaned_blocks).strip()

class GemmaClient:
    """
    Gemma 4 integration wrapper supporting 'mock' and 'ollama' modes.
    Handles communication with the LLM backend for explaining deterministic analytics.
    """

    def __init__(self):
        self.backend = os.environ.get("GEMMA_BACKEND", "mock").lower()
        self.model_name = os.environ.get("GEMMA_MODEL", "gemma4:e2b")

    def _load_prompt(self, filename: str) -> str:
        return (PROMPT_DIR / filename).read_text(encoding="utf-8")

    def _normalize_value(self, val: Any) -> Any:
        import pandas as pd
        if pd.isna(val):
            return ""
        return val

    def _prepare_context(self, analytics_row: dict[str, Any]) -> dict[str, Any]:
        """Creates a structured deterministic analytics context dictionary."""
        risk_level = self._normalize_value(analytics_row.get("risk_level"))
        return {
            "medicine_name": self._normalize_value(analytics_row.get("medicine_name")),
            "current_stock": self._normalize_value(analytics_row.get("current_stock_units")),
            "average_daily_demand": self._normalize_value(analytics_row.get("avg_daily_demand")),
            "days_of_cover": self._normalize_value(analytics_row.get("days_of_cover")),
            "projected_stockout_date": self._normalize_value(analytics_row.get("projected_stockout_date")),
            "risk_level": risk_level,
            "risk_reason": "Stockout projected within critical window" if risk_level in ["critical", "high"] else "Sufficient stock",
            "recommended_reorder_quantity": self._normalize_value(analytics_row.get("recommended_quantity_units")),
            "preferred_supplier": self._normalize_value(analytics_row.get("preferred_supplier")),
            "supplier_reason": self._normalize_value(analytics_row.get("supplier_reason")),
            "expiry_warning": self._normalize_value(analytics_row.get("expiry_warning")),
            "pending_order_notes": self._normalize_value(analytics_row.get("pending_order_notes")),
            "safety_boundary": "Logistics and procurement support only. Do not provide clinical advice."
        }

    def generate(self, system_prompt: str, user_prompt: str, mock_fallback: str = None) -> str:
        if self.backend == "mock":
            if not mock_fallback:
                mock_fallback = "This is a generic mock response. Deterministic analytics provided the context."
            return f"[Gemma 4 Mock Mode - {self.model_name}]\n\n{mock_fallback}"

        # Ollama backend
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": f"System: {system_prompt}\n\nUser: {user_prompt}",
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()
            return clean_model_output(data.get("response", ""))
        except requests.exceptions.RequestException as e:
            return (
                f"Error: Unable to connect to Ollama runtime for model '{self.model_name}'. "
                f"Please ensure Ollama is running at localhost:11434. (Details: {str(e)})"
            )

    def explain_stockout_risk(self, analytics_row: dict[str, Any]) -> str:
        system = self._load_prompt("system_logistics_copilot.md")
        task = self._load_prompt("explain_stockout_risk.md")
        context = self._prepare_context(analytics_row)
        user = f"{task}\n\nStructured deterministic analytics context:\n{json.dumps(context, default=str, indent=2)}"
        
        mock_fallback = (
            f"**Medicine:** {context.get('medicine_name', 'Unknown')}\n"
            f"**Risk Level:** {(context.get('risk_level') or 'unknown').upper()}\n"
            f"**Coverage:** {context.get('days_of_cover', 'Unknown')} days remaining (Projected stockout: {context.get('projected_stockout_date', 'Unknown')})\n"
            f"**Recommended Reorder Quantity:** {context.get('recommended_reorder_quantity', 'Unknown')}\n"
            f"**Preferred Supplier:** {context.get('preferred_supplier', 'Unknown')}\n"
            f"**Supplier Notes:** {context.get('supplier_reason') or 'No supplier reason provided.'}\n"
            f"**Expiry Notes:** {context.get('expiry_warning') or 'No upcoming expiries.'}"
        )
        return self.generate(system, user, mock_fallback=mock_fallback)

    def generate_reorder_plan(self, analytics_row: dict[str, Any]) -> str:
        system = self._load_prompt("system_logistics_copilot.md")
        task = self._load_prompt("generate_reorder_plan.md")
        context = self._prepare_context(analytics_row)
        user = f"{task}\n\nStructured deterministic analytics context:\n{json.dumps(context, default=str, indent=2)}"
        
        mock_fallback = f"Reorder Plan Mock: Need {context.get('recommended_reorder_quantity', 'Unknown')} units of {context.get('medicine_name', 'Unknown')}."
        return self.generate(system, user, mock_fallback=mock_fallback)

    def generate_procurement_message(self, analytics_row: dict[str, Any]) -> str:
        system = self._load_prompt("system_logistics_copilot.md")
        task = self._load_prompt("generate_procurement_message.md")
        context = self._prepare_context(analytics_row)
        user = f"{task}\n\nStructured deterministic analytics context:\n{json.dumps(context, default=str, indent=2)}"
        
        mock_fallback = (
            f"Subject: URGENT ({(context.get('risk_level') or 'unknown').upper()}): Procurement order for {context.get('medicine_name', 'Unknown')}\n\n"
            f"Please initiate an order for {context.get('recommended_reorder_quantity', 'Unknown')} units of {context.get('medicine_name', 'Unknown')} from {context.get('preferred_supplier', 'Unknown')}.\n"
            f"Current coverage is {context.get('days_of_cover', 'Unknown')} days, with a projected stockout on {context.get('projected_stockout_date', 'Unknown')}.\n"
            f"Supplier constraints: {context.get('supplier_reason') or 'None'}.\n"
            f"{('Expiry warning: ' + str(context.get('expiry_warning'))) if context.get('expiry_warning') not in [None, '', False] else ''}"
        )
        return self.generate(system, user, mock_fallback=mock_fallback.strip())

    def answer_question(self, question: str, analytics_row: dict[str, Any], all_results: Any = None) -> str:
        """
        Answer logistics-only questions using deterministic analytics context.
        Clinical advice is strictly blocked.
        """
        if is_clinical_question(question):
            return self.refuse_clinical_advice(question)

        q = question.lower().strip()

        is_priority_question = (
            ("reorder" in q or "order" in q or "prioritize" in q or "priority" in q)
            and ("first" in q or "why" in q or "which" in q)
        )

        backend = str(getattr(self, "backend", "mock")).lower().strip()
        model_name = getattr(self, "model_name", getattr(self, "model", "gemma4:e2b"))

        if backend == "mock" and all_results is not None and is_priority_question:
            df = all_results.copy()

            risk_order = {
                "critical": 0,
                "high": 1,
                "medium": 2,
                "low": 3,
                "unknown": 4,
            }

            if "risk_level" not in df.columns:
                return (
                    f"[Gemma 4 Mock Mode - {model_name}]\n\n"
                    "I cannot rank reorder priority because the analytics table is missing risk_level."
                )

            if "supplier_reason" not in df.columns:
                df["supplier_reason"] = ""

            if "days_of_cover" not in df.columns:
                df["days_of_cover"] = float("inf")

            if "recommended_reorder_quantity" not in df.columns and "recommended_quantity_units" in df.columns:
                df["recommended_reorder_quantity"] = df["recommended_quantity_units"]

            if "recommended_reorder_quantity" not in df.columns:
                df["recommended_reorder_quantity"] = "unknown"

            df["_risk_sort"] = df["risk_level"].map(risk_order).fillna(5)
            df["_supplier_blocked_sort"] = df["supplier_reason"].astype(str).str.contains(
                "No supplier can arrive", case=False, regex=False
            ).map(lambda blocked: 0 if blocked else 1)

            df = df.sort_values(
                by=["_risk_sort", "_supplier_blocked_sort", "days_of_cover"],
                ascending=[True, True, True],
                na_position="last",
            )

            top_rows = df.head(3)

            lines = [
                f"[Gemma 4 Mock Mode - {model_name}]",
                "",
                "Reorder priority based on deterministic analytics:",
            ]

            for idx, (_, row) in enumerate(top_rows.iterrows(), start=1):
                medicine = row.get("medicine_name", "Unknown")
                risk = row.get("risk_level", "unknown")
                days = row.get("days_of_cover", "unknown")
                qty = row.get("recommended_reorder_quantity", "unknown")
                supplier = row.get("preferred_supplier", "unknown")
                supplier_reason = row.get("supplier_reason", "")

                lines.append(
                    f"{idx}. {medicine}: {risk} risk, {days} days of cover, "
                    f"recommended reorder quantity {qty} units from {supplier}."
                )

                if supplier_reason:
                    lines.append(f"   Supplier note: {supplier_reason}")

            lines.append("")
            
            if not top_rows.empty:
                first_med = top_rows.iloc[0].get("medicine_name", "the top priority medicine")
                lines.append(
                    "Ranking Rationale: Critical medicines with supplier infeasibility ('No supplier can arrive before projected stockout') "
                    "outrank critical medicines with slightly fewer days of cover but feasible suppliers. "
                    f"Therefore, {first_med} is ranked highest due to its blocked supply path."
                )

            return "\n".join(lines)

        system = self._load_prompt("system_logistics_copilot.md")
        try:
            task = self._load_prompt("answer_user_question.md")
        except FileNotFoundError:
            task = "Answer the user's logistics question using only the structured deterministic analytics context."

        context_str = json.dumps(self._prepare_context(analytics_row), default=str, indent=2)

        if all_results is not None:
            try:
                high_risk = all_results[all_results["risk_level"].isin(["critical", "high"])].copy()
                if not high_risk.empty:
                    high_risk = high_risk.sort_values("days_of_cover")
                    ranked = []
                    for _, row in high_risk.iterrows():
                        ranked.append({
                            "medicine_name": self._normalize_value(row.get("medicine_name")),
                            "risk_level": self._normalize_value(row.get("risk_level")),
                            "days_of_cover": self._normalize_value(row.get("days_of_cover")),
                            "recommended_reorder_quantity": self._normalize_value(row.get(
                                "recommended_reorder_quantity",
                                row.get("recommended_quantity_units"),
                            )),
                            "preferred_supplier": self._normalize_value(row.get("preferred_supplier")),
                            "supplier_reason": self._normalize_value(row.get("supplier_reason")),
                            "expiry_warning": self._normalize_value(row.get("expiry_warning")),
                            "pending_order_notes": self._normalize_value(row.get(
                                "pending_order_notes",
                                row.get("pending_order_note", ""),
                            )),
                        })
                    context_str += "\n\nRanked high-risk medicines:\n" + json.dumps(ranked, default=str, indent=2)
            except Exception:
                pass

        user = f"{task}\n\nQuestion: {question}\n\nStructured deterministic analytics context:\n{context_str}"

        mock_fallback = (
            f"[Gemma 4 Mock Mode - {model_name}]\n\n"
            f"Logistics question received: {question}\n"
            f"Selected medicine context: {analytics_row.get('medicine_name', 'Unknown')}.\n"
            "This mock response confirms the app reached the GemmaClient Q&A path."
        )

        return self.generate(system, user, mock_fallback=mock_fallback)

    def refuse_clinical_advice(self, question: str) -> str:
        """Provides a standard deterministic refusal message for clinical questions."""
        safe_refusal = (
            "MedSupply Guard supports logistics and procurement only. I can't provide dosage, "
            "prescribing, diagnosis, or patient-specific treatment guidance. Please consult a "
            "licensed clinician or pharmacist. I can help with stockout risk, expiry, inventory, "
            "supplier lead times, or procurement planning."
        )
        return safe_refusal

