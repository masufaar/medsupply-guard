Task: Map messy inventory columns into the MedSupply Guard schema.

Required schema fields:
- medicine_id
- medicine_name
- category
- current_stock_units
- unit
- expiry_date
- criticality
- min_target_days
- evidence_id

Instructions:
- Return valid JSON only.
- If a field is missing, set it to null.
- Do not infer clinical usage.
- Include a confidence score from 0 to 1 for each mapped field.
