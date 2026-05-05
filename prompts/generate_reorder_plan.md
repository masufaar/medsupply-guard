Task: Generate a logistics reorder plan from supplied deterministic analytics.

Instructions:
- Use only the supplied analytics output.
- Prioritize critical medicines with low days of cover and long replenishment lead time.
- Compare suppliers based on lead time feasibility first, then cost.
- Do not recommend clinical substitutions.
- Include evidence IDs and assumptions.

Return valid JSON with this schema:
{
  "summary": "string",
  "recommended_orders": [
    {
      "medicine_id": "string",
      "medicine_name": "string",
      "risk_level": "critical|high|medium|low",
      "recommended_quantity_units": number,
      "preferred_supplier": "string|null",
      "reason": "string",
      "evidence_ids": ["string"]
    }
  ],
  "warnings": ["string"],
  "assumptions": ["string"]
}
