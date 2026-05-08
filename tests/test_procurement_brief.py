import pandas as pd
from src.analytics.procurement_brief import generate_procurement_brief

def test_procurement_brief_normal_oxytocin():
    row = {
        "medicine_name": "Oxytocin Injection",
        "risk_level": "critical",
        "current_stock_units": 10.0,
        "avg_daily_demand": 5.0,
        "days_of_cover": 2.0,
        "projected_stockout_date": "2026-05-06",
        "recommended_quantity_units": 140.0,
        "preferred_supplier": "FastMed Distributors",
        "supplier_reason": "Selected fastest available supplier.",
    }
    
    brief = generate_procurement_brief(row)
    
    assert "# Procurement Brief — Oxytocin Injection" in brief
    assert "Risk Level:** CRITICAL" in brief
    assert "Recommended Reorder Quantity:** 140.0 units" in brief
    assert "Preferred Supplier:** FastMed Distributors" in brief
    assert "Supplier Reason:** Selected fastest available supplier." in brief
    assert "Safety Boundary:** Logistics and procurement support only" in brief
    assert "Deterministic Analytics Context" in brief

def test_procurement_brief_missing_and_nan_values():
    row = {
        "medicine_name": "Paracetamol",
        "risk_level": "low",
        "current_stock_units": 500.0,
        "avg_daily_demand": 10.0,
        "days_of_cover": 50.0,
        "projected_stockout_date": "2026-06-23",
        "recommended_reorder_quantity": 0.0,  # Testing alternative field name
        "preferred_supplier": "GenericPharma",
        "supplier_reason": "Sufficient stock.",
        "expiry_warning": pd.NA,
        "pending_order_note": float("nan"),
    }
    
    brief = generate_procurement_brief(row)
    
    # Missing/NaN values should not result in "nan" or "NaT" in the text.
    assert "nan" not in brief.lower()
    assert "nat" not in brief.lower()
    
    # Optional fields should not appear if they are NaN/None
    assert "Expiry Warning:" not in brief
    assert "Pending Orders:" not in brief
    
    # Ensure recommended quantity still picked up correctly via alternative key
    assert "Recommended Reorder Quantity:** 0.0 units" in brief
