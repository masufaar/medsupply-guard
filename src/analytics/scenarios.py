import pandas as pd
from typing import Tuple, Dict, Any

"""Deterministic what-if scenario helpers.

Scenarios operate on in-memory dataframe copies and never mutate source CSV files.
They do not call Gemma or any external model.
"""

def apply_what_if_scenario(
    inventory: pd.DataFrame, 
    demand_history: pd.DataFrame, 
    suppliers: pd.DataFrame, 
    pending_orders: pd.DataFrame, 
    scenario_name: str
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Applies deterministic what-if scenario transformations to copies of the input dataframes.
    Original dataframes are never mutated.
    """
    inv = inventory.copy()
    dem = demand_history.copy()
    sup = suppliers.copy()
    pen = pending_orders.copy()

    if scenario_name == "Base case":
        pass

    elif scenario_name == "Demand surge +25%":
        demand_cols = ["demand_units", "quantity", "dispensed_units", "units_dispensed"]
        target_col = None
        for col in demand_cols:
            if col in dem.columns:
                target_col = col
                break
        
        if target_col:
            dem[target_col] = dem[target_col] * 1.25

    elif scenario_name == "Supplier delay +7 days":
        if "lead_time_days" in sup.columns:
            sup["lead_time_days"] = sup["lead_time_days"] + 7

    elif scenario_name == "Stock count correction -25%":
        if "current_stock_units" in inv.columns:
            inv["current_stock_units"] = inv["current_stock_units"] * 0.75

    elif scenario_name == "Pending order delayed +7 days":
        if "expected_arrival_date" in pen.columns:
            pen["expected_arrival_date"] = pd.to_datetime(pen["expected_arrival_date"]) + pd.Timedelta(days=7)
            # Ensure it's stored back as string/date to match original format if needed,
            # or leave as datetime since _parse_date in inventory_math handles it.

    elif scenario_name == "Combined shock":
        # Demand +25%
        demand_cols = ["demand_units", "quantity", "dispensed_units", "units_dispensed"]
        target_col = None
        for col in demand_cols:
            if col in dem.columns:
                target_col = col
                break
        if target_col:
            dem[target_col] = dem[target_col] * 1.25
        
        # Supplier delay +5 days
        if "lead_time_days" in sup.columns:
            sup["lead_time_days"] = sup["lead_time_days"] + 5
            
        # Stock count correction -10%
        if "current_stock_units" in inv.columns:
            inv["current_stock_units"] = inv["current_stock_units"] * 0.90

    return inv, dem, sup, pen

def summarize_scenario_delta(
    base_results: pd.DataFrame, 
    scenario_results: pd.DataFrame, 
    focus_medicine: str = "Oxytocin Injection"
) -> Dict[str, Any]:
    """
    Computes differences between base and scenario results.
    """
    summary = {
        "base_critical": int((base_results["risk_level"] == "critical").sum()),
        "scenario_critical": int((scenario_results["risk_level"] == "critical").sum()),
        "base_high": int((base_results["risk_level"] == "high").sum()),
        "scenario_high": int((scenario_results["risk_level"] == "high").sum()),
        "base_orders": int((base_results["recommended_quantity_units"] > 0).sum()),
        "scenario_orders": int((scenario_results["recommended_quantity_units"] > 0).sum()),
        "focus_base": {},
        "focus_scenario": {},
        "top_changed": []
    }

    base_focus = base_results[base_results["medicine_name"] == focus_medicine]
    scen_focus = scenario_results[scenario_results["medicine_name"] == focus_medicine]

    if not base_focus.empty:
        summary["focus_base"] = base_focus.iloc[0].to_dict()
    if not scen_focus.empty:
        summary["focus_scenario"] = scen_focus.iloc[0].to_dict()

    # Compare all to find top changes in days_of_cover
    merged = pd.merge(
        base_results[["medicine_name", "risk_level", "days_of_cover", "recommended_quantity_units"]],
        scenario_results[["medicine_name", "risk_level", "days_of_cover", "recommended_quantity_units"]],
        on="medicine_name",
        suffixes=("_base", "_scenario")
    )
    
    # Calculate days of cover change
    merged["days_of_cover_change"] = merged["days_of_cover_scenario"] - merged["days_of_cover_base"]
    
    # Sort by absolute change
    merged["abs_change"] = merged["days_of_cover_change"].abs()
    top_changed_df = merged.sort_values("abs_change", ascending=False).head(5)
    
    summary["top_changed"] = top_changed_df.to_dict("records")
    return summary
