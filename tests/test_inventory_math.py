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


def test_average_daily_demand():
    from src.analytics.inventory_math import average_daily_demand
    df = pd.DataFrame([
        {"date": "2026-05-01", "medicine_id": "MED1", "dispensed_units": 10},
        {"date": "2026-05-02", "medicine_id": "MED1", "dispensed_units": 20},
        {"date": "2026-05-01", "medicine_id": "MED2", "dispensed_units": 5},
    ])
    assert average_daily_demand(df, "MED1", lookback_days=30) == 15.0
    assert average_daily_demand(df, "MED2", lookback_days=30) == 5.0
    assert average_daily_demand(df, "MED3", lookback_days=30) == 0.0


def test_choose_supplier():
    from src.analytics.inventory_math import choose_supplier
    df = pd.DataFrame([
        {"medicine_id": "MED1", "supplier_name": "Fast", "lead_time_days": 2, "unit_cost": 10.0},
        {"medicine_id": "MED1", "supplier_name": "Slow", "lead_time_days": 5, "unit_cost": 5.0},
    ])
    name, reason = choose_supplier(df, "MED1", 10.0)
    assert name == "Slow"
    assert "lowest-cost" in reason

    name, reason = choose_supplier(df, "MED1", 3.0)
    assert name == "Fast"
    assert "lowest-cost" in reason

    name, reason = choose_supplier(df, "MED1", 1.0)
    assert name == "Fast"
    assert "No supplier can arrive before" in reason

    name, reason = choose_supplier(df, "MED1", None)
    assert name == "Fast"
    assert "insufficient" in reason


def test_expiry_warning():
    from src.analytics.inventory_math import expiry_warning
    today = date(2026, 5, 4)
    assert "already expired" in expiry_warning(date(2026, 5, 1), today, 10.0)
    assert "expires in" in expiry_warning(date(2026, 6, 1), today, 40.0)
    assert "expire before projected use" in expiry_warning(date(2026, 6, 15), today, 50.0)
    assert expiry_warning(date(2027, 1, 1), today, 10.0) is None


def test_parse_date():
    from src.analytics.inventory_math import _parse_date
    assert _parse_date("2026-05-04") == date(2026, 5, 4)
    assert _parse_date(date(2026, 5, 4)) == date(2026, 5, 4)
    assert _parse_date(None) is None
    assert _parse_date("") is None


def test_analyze_inventory_no_demand():
    from src.analytics.inventory_math import analyze_inventory
    inventory = pd.DataFrame([{
        "medicine_id": "MED999", "medicine_name": "New Drug", "category": "Pain",
        "current_stock_units": 100, "unit": "pack", "expiry_date": "2027-12-31",
        "criticality": "low", "min_target_days": 21, "evidence_id": "inv:999",
    }])
    demand = pd.DataFrame(columns=["date", "medicine_id", "dispensed_units"])
    suppliers = pd.DataFrame([{"medicine_id": "MED999", "supplier_name": "Supplier X", "lead_time_days": 5, "unit_cost": 1.0}])
    pending = pd.DataFrame(columns=["medicine_id", "quantity_units", "expected_arrival_date"])
    
    result = analyze_inventory(inventory, demand, suppliers, pending, today=date(2026, 5, 4)).iloc[0]
    assert result["risk_level"] == "unknown"
    assert result["days_of_cover"] is None
    assert result["projected_stockout_date"] is None
    assert result["recommended_quantity_units"] == 0


def test_analyze_inventory_with_pending():
    from src.analytics.inventory_math import analyze_inventory
    inventory = pd.DataFrame([{
        "medicine_id": "MED001", "medicine_name": "Amox", "category": "Anti",
        "current_stock_units": 100, "unit": "pack", "expiry_date": "2026-12-31",
        "criticality": "high", "min_target_days": 30,
    }])
    demand = pd.DataFrame([{"date": "2026-05-01", "medicine_id": "MED001", "dispensed_units": 10}])
    suppliers = pd.DataFrame([{"medicine_id": "MED001", "supplier_name": "Sup A", "lead_time_days": 5, "unit_cost": 2.0}])
    pending = pd.DataFrame([{"medicine_id": "MED001", "quantity_units": 50, "expected_arrival_date": "2026-05-06"}])
    
    result = analyze_inventory(inventory, demand, suppliers, pending, today=date(2026, 5, 4)).iloc[0]
    assert result["recommended_quantity_units"] == 150
