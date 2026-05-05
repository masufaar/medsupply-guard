from datetime import date

import pandas as pd

from src.analytics.inventory_math import analyze_inventory, days_of_cover, recommended_quantity, risk_level


def test_days_of_cover():
    assert days_of_cover(90, 18) == 5.0
    assert days_of_cover(90, 0) is None


def test_risk_level():
    assert risk_level(5, "critical") == "critical"
    assert risk_level(10, "high") == "high"
    assert risk_level(20, "medium") == "medium"
    assert risk_level(45, "low") == "low"
    assert risk_level(None, "high") == "unknown"


def test_recommended_quantity():
    assert recommended_quantity(avg_daily_demand=10, min_target_days=30, current_stock_units=100, pending_units=50) == 150
    assert recommended_quantity(avg_daily_demand=10, min_target_days=30, current_stock_units=400, pending_units=0) == 0


def test_analyze_inventory_critical_stockout():
    inventory = pd.DataFrame([
        {
            "medicine_id": "MED001",
            "medicine_name": "Amoxicillin 500mg",
            "category": "Antibiotic",
            "current_stock_units": 90,
            "unit": "pack",
            "expiry_date": "2026-12-31",
            "criticality": "high",
            "min_target_days": 30,
            "evidence_id": "inventory:14",
        }
    ])
    demand = pd.DataFrame([
        {"date": f"2026-04-{day:02d}", "medicine_id": "MED001", "dispensed_units": 18}
        for day in range(5, 31)
    ] + [
        {"date": f"2026-05-{day:02d}", "medicine_id": "MED001", "dispensed_units": 18}
        for day in range(1, 5)
    ])
    suppliers = pd.DataFrame([
        {"medicine_id": "MED001", "supplier_name": "Supplier A", "lead_time_days": 12, "unit_cost": 2.1},
        {"medicine_id": "MED001", "supplier_name": "Supplier B", "lead_time_days": 5, "unit_cost": 2.45},
    ])
    pending = pd.DataFrame(columns=["medicine_id", "quantity_units", "expected_arrival_date"])
    result = analyze_inventory(inventory, demand, suppliers, pending, today=date(2026, 5, 4)).iloc[0]
    assert result["risk_level"] == "critical"
    assert result["recommended_quantity_units"] == 450
    assert result["preferred_supplier"] == "Supplier B"
