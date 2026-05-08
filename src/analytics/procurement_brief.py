import pandas as pd

def _safe_str(val) -> str:
    """Helper to safely format a value, returning empty string for NaN/NaT/None."""
    if pd.isna(val) or val in (None, "", "nan", "NaT"):
        return ""
    return str(val).strip()

def generate_procurement_brief(row: dict) -> str:
    """
    Deterministically generates a Markdown procurement brief from an analytics row.
    """
    medicine_name = _safe_str(row.get("medicine_name", "Unknown Medicine"))
    risk_level = _safe_str(row.get("risk_level", "Unknown")).upper()
    current_stock = _safe_str(row.get("current_stock_units", "0"))
    avg_demand = _safe_str(row.get("avg_daily_demand", "0"))
    days_cover = _safe_str(row.get("days_of_cover", "0"))
    stockout_date = _safe_str(row.get("projected_stockout_date", "Unknown"))
    
    # Handle recommended quantity column variants
    reorder_qty = row.get("recommended_quantity_units")
    if pd.isna(reorder_qty):
        reorder_qty = row.get("recommended_reorder_quantity")
    reorder_qty_str = _safe_str(reorder_qty) or "0"
    
    preferred_supplier = _safe_str(row.get("preferred_supplier", "Unknown"))
    supplier_reason = _safe_str(row.get("supplier_reason", "No reason provided."))
    
    # Handle pending order notes variants
    pending_notes = row.get("pending_order_notes")
    if pd.isna(pending_notes):
        pending_notes = row.get("pending_order_note")
    pending_notes_str = _safe_str(pending_notes)
    
    expiry_warning = _safe_str(row.get("expiry_warning"))
    
    lines = [
        f"# Procurement Brief — {medicine_name}",
        "",
        "**Source:** Deterministic Analytics Context",
        "**Safety Boundary:** Logistics and procurement support only. Not clinical advice.",
        "",
        "## Inventory Status",
        f"- **Risk Level:** {risk_level}",
        f"- **Current Stock:** {current_stock} units",
        f"- **Average Daily Demand:** {avg_demand} units/day",
        f"- **Days of Cover:** {days_cover} days",
        f"- **Projected Stockout Date:** {stockout_date}",
    ]
    
    if expiry_warning:
        lines.append(f"- **Expiry Warning:** {expiry_warning}")
        
    if pending_notes_str:
        lines.append(f"- **Pending Orders:** {pending_notes_str}")
        
    lines.extend([
        "",
        "## Procurement Recommendation",
        f"- **Recommended Reorder Quantity:** {reorder_qty_str} units",
        f"- **Preferred Supplier:** {preferred_supplier}",
        f"- **Supplier Reason:** {supplier_reason}"
    ])
    
    return "\n".join(lines)
