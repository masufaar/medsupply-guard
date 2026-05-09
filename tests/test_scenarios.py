import pandas as pd
import pytest
from src.analytics.scenarios import apply_what_if_scenario, summarize_scenario_delta

@pytest.fixture
def sample_data():
    inventory = pd.DataFrame({
        "medicine_id": ["MED1", "MED2"],
        "medicine_name": ["Oxytocin Injection", "Amoxicillin"],
        "current_stock_units": [100.0, 200.0]
    })
    demand_history = pd.DataFrame({
        "medicine_id": ["MED1", "MED2"],
        "dispensed_units": [10.0, 20.0]
    })
    suppliers = pd.DataFrame({
        "medicine_id": ["MED1", "MED2"],
        "lead_time_days": [5, 10]
    })
    pending_orders = pd.DataFrame({
        "medicine_id": ["MED1"],
        "expected_arrival_date": ["2026-05-15"]
    })
    return inventory, demand_history, suppliers, pending_orders

def test_demand_surge_does_not_mutate_inputs(sample_data):
    inv, dem, sup, pen = sample_data
    orig_dem = dem.copy()
    
    inv_new, dem_new, sup_new, pen_new = apply_what_if_scenario(
        inv, dem, sup, pen, "Demand surge +25%"
    )
    
    # Original should remain unchanged
    pd.testing.assert_frame_equal(dem, orig_dem)
    
    # New should be multiplied by 1.25
    assert dem_new["dispensed_units"][0] == 12.5

def test_stock_count_correction_reduces_stock(sample_data):
    inv, dem, sup, pen = sample_data
    inv_new, _, _, _ = apply_what_if_scenario(
        inv, dem, sup, pen, "Stock count correction -25%"
    )
    assert inv_new["current_stock_units"][0] == 75.0

def test_supplier_delay_increases_lead_time(sample_data):
    inv, dem, sup, pen = sample_data
    _, _, sup_new, _ = apply_what_if_scenario(
        inv, dem, sup, pen, "Supplier delay +7 days"
    )
    assert sup_new["lead_time_days"][0] == 12

def test_combined_shock_changes_multiple_inputs(sample_data):
    inv, dem, sup, pen = sample_data
    inv_new, dem_new, sup_new, _ = apply_what_if_scenario(
        inv, dem, sup, pen, "Combined shock"
    )
    assert dem_new["dispensed_units"][0] == 12.5
    assert sup_new["lead_time_days"][0] == 10
    assert inv_new["current_stock_units"][0] == 90.0

def test_summarize_scenario_delta_returns_focus_medicine_metrics():
    base_results = pd.DataFrame({
        "medicine_name": ["Oxytocin Injection", "Other"],
        "risk_level": ["medium", "low"],
        "days_of_cover": [10.0, 20.0],
        "recommended_quantity_units": [0, 0]
    })
    scenario_results = pd.DataFrame({
        "medicine_name": ["Oxytocin Injection", "Other"],
        "risk_level": ["critical", "medium"],
        "days_of_cover": [5.0, 15.0],
        "recommended_quantity_units": [50, 0]
    })
    
    summary = summarize_scenario_delta(base_results, scenario_results)
    
    assert summary["base_critical"] == 0
    assert summary["scenario_critical"] == 1
    assert summary["focus_base"]["days_of_cover"] == 10.0
    assert summary["focus_scenario"]["days_of_cover"] == 5.0
    assert len(summary["top_changed"]) == 2
    assert summary["top_changed"][0]["medicine_name"] == "Oxytocin Injection"
    assert summary["top_changed"][0]["days_of_cover_change"] == -5.0
