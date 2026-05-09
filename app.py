from __future__ import annotations

"""
MedSupply Guard Streamlit Application.
This is the main entry point for the Kaggle demo.
The UI layout is intentionally maintained as-is.
Deterministic analytics serve as the source of truth, while Gemma provides explanations.
Clinical advice is strictly blocked.
"""

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from src.analytics.inventory_math import analyze_inventory
from src.analytics.procurement_brief import generate_procurement_brief
from src.analytics.scenarios import apply_what_if_scenario, summarize_scenario_delta
from src.llm.gemma_client import GemmaClient

BASE_DIR = Path(__file__).parent
SAMPLE_DIR = BASE_DIR / "data" / "sample"

st.set_page_config(page_title="MedSupply Guard", page_icon="💊", layout="wide")

st.title("MedSupply Guard")
st.caption("Offline-first Gemma 4 copilot for clinic medicine inventory logistics")

st.warning(
    "Safety boundary: MedSupply Guard supports logistics and procurement decisions only. "
    "It does not provide diagnosis, prescribing advice, dosage guidance, or clinical substitutions."
)


def load_csv_upload(label: str, sample_file: str) -> pd.DataFrame:
    """Loads CSV data from user upload or falls back to synthetic sample data."""
    uploaded = st.sidebar.file_uploader(label, type=["csv"], key=sample_file)
    if uploaded is not None:
        return pd.read_csv(uploaded)
    return pd.read_csv(SAMPLE_DIR / sample_file)


st.sidebar.header("Data")
st.sidebar.write("Upload CSVs or use the synthetic sample clinic scenario.")

inventory = load_csv_upload("Inventory CSV", "inventory.csv")
demand_history = load_csv_upload("Demand history CSV", "demand_history.csv")
suppliers = load_csv_upload("Suppliers CSV", "suppliers.csv")
pending_orders = load_csv_upload("Pending orders CSV", "pending_orders.csv")

client = GemmaClient()
st.sidebar.header("Gemma 4 Copilot Configuration")
st.sidebar.write(f"**Backend:** `{client.backend}`")
st.sidebar.write(f"**Model:** `{client.model_name}`")
st.sidebar.caption("Change via GEMMA_BACKEND and GEMMA_MODEL env vars.")

# Run deterministic analytics engine to calculate risks and reorder plans
# This is the single source of truth for the application.
results = analyze_inventory(inventory, demand_history, suppliers, pending_orders, today=date(2026, 5, 4))

risk_sort_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "unknown": 4}
results["risk_sort"] = results["risk_level"].map(risk_sort_order).fillna(5)
results = results.sort_values(["risk_sort", "days_of_cover"], na_position="last")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Medicines monitored", len(results))
k2.metric("Critical risks", int((results["risk_level"] == "critical").sum()))
k3.metric("High risks", int((results["risk_level"] == "high").sum()))
k4.metric("Orders recommended", int((results["recommended_quantity_units"] > 0).sum()))

# Risk distribution chart
risk_counts = results['risk_level'].fillna('unknown').value_counts()

# Days of cover chart
doc_df = results[['medicine_name', 'days_of_cover']].copy()
doc_df = doc_df[pd.notna(doc_df['days_of_cover'])]
doc_df = doc_df.sort_values('days_of_cover')
st.subheader("Days of Cover per Medicine")
st.bar_chart(doc_df.set_index('medicine_name')['days_of_cover'])
st.caption("Lower days of cover indicates earlier projected stockout risk.")

# Ensure order
risk_chart_order = ['critical', 'high', 'medium', 'low', 'unknown']
risk_counts = risk_counts.reindex(risk_chart_order, fill_value=0)
st.subheader("Risk Distribution")
st.bar_chart(risk_counts)
st.caption("Risk levels are calculated deterministically from stock, demand, and target coverage.")

st.subheader("Demo Scenario: Oxytocin Injection")
st.info("This section highlights how MedSupply Guard handles a critical stockout with supplier infeasibility. This is logistics/procurement support only, not clinical advice.")

demo_df = results[results["medicine_name"] == "Oxytocin Injection"]
if not demo_df.empty:
    demo_row = demo_df.iloc[0]
    st.write(f"**Medicine:** {demo_row['medicine_name']} (Risk: **{demo_row['risk_level'].upper()}**)")
    
    # Safely handle potential float formatting
    days_cover_val = demo_row['days_of_cover']
    days_cover_str = f"{days_cover_val:.1f}" if pd.notna(days_cover_val) and isinstance(days_cover_val, (int, float)) else str(days_cover_val)
    
    st.write(f"**Stock:** {demo_row['current_stock_units']} units (approx. {days_cover_str} days cover)")
    st.write(f"**Projected Stockout Date:** {demo_row['projected_stockout_date']}")
    st.warning(f"**Supplier Status:** {demo_row['supplier_reason']}")
    st.write(f"**Action:** Recommended reorder **{demo_row['recommended_quantity_units']}** units. Selected **{demo_row['preferred_supplier']}** as the fastest available supplier.")
else:
    st.warning("Oxytocin Injection data not found in the current dataset.")

st.markdown("---")

st.subheader("What-if Scenario Simulator")
st.caption("Scenarios are deterministic simulations applied to in-memory copies of the CSV data. They do not change source files and do not use Gemma to invent values.")
scenario_name = st.selectbox("Select a scenario to simulate:", [
    "Base case",
    "Demand surge +25%",
    "Supplier delay +7 days",
    "Stock count correction -25%",
    "Pending order delayed +7 days",
    "Combined shock"
])
if st.button("Run what-if scenario"):
    with st.spinner("Simulating..."):
        inv_scen, dem_scen, sup_scen, pen_scen = apply_what_if_scenario(inventory, demand_history, suppliers, pending_orders, scenario_name)
        scenario_results = analyze_inventory(inv_scen, dem_scen, sup_scen, pen_scen, today=date(2026, 5, 4))
        
        scenario_results["risk_sort"] = scenario_results["risk_level"].map(risk_sort_order).fillna(5)
        scenario_results = scenario_results.sort_values(["risk_sort", "days_of_cover"], na_position="last")
        
        summary = summarize_scenario_delta(results, scenario_results)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Critical Items", summary["scenario_critical"], summary["scenario_critical"] - summary["base_critical"], delta_color="inverse")
        col2.metric("High Risk Items", summary["scenario_high"], summary["scenario_high"] - summary["base_high"], delta_color="inverse")
        col3.metric("Orders Recommended", summary["scenario_orders"], summary["scenario_orders"] - summary["base_orders"], delta_color="inverse")
        
        if summary["focus_scenario"]:
            st.write(f"**Oxytocin Injection Metrics:**")
            st.write(f"- Days of cover: {summary['focus_scenario'].get('days_of_cover')} (was {summary['focus_base'].get('days_of_cover')})")
            st.write(f"- Risk level: {summary['focus_scenario'].get('risk_level')} (was {summary['focus_base'].get('risk_level')})")
            st.write(f"- Reorder qty: {summary['focus_scenario'].get('recommended_quantity_units')} (was {summary['focus_base'].get('recommended_quantity_units')})")
        
        if summary["top_changed"]:
            st.write("**Top Impacted Medicines (Days of Cover Change):**")
            top_df = pd.DataFrame(summary["top_changed"])[["medicine_name", "risk_level_base", "risk_level_scenario", "days_of_cover_base", "days_of_cover_scenario", "days_of_cover_change", "recommended_quantity_units_base", "recommended_quantity_units_scenario"]]
            st.dataframe(top_df, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("Stockout risk dashboard")
display_cols = [
    "medicine_name",
    "current_stock_units",
    "avg_daily_demand",
    "days_of_cover",
    "projected_stockout_date",
    "risk_level",
    "recommended_quantity_units",
    "preferred_supplier",
    "supplier_reason",
    "expiry_warning",
]

pending_col = next((col for col in ["pending_order_note", "pending_order_notes"] if col in results.columns), None)
if pending_col:
    display_cols.append(pending_col)

st.dataframe(results[display_cols], use_container_width=True, hide_index=True)


st.subheader("Action plan")
critical_or_high = results[results["risk_level"].isin(["critical", "high"])]
if critical_or_high.empty:
    st.success("No critical or high stockout risks detected in the current sample data.")
else:
    for _, row in critical_or_high.iterrows():
        with st.expander(f"{row['risk_level'].upper()} — {row['medicine_name']}", expanded=True):
            st.write(f"**Recommended quantity:** {row['recommended_quantity_units']} units")
            st.write(f"**Preferred supplier:** {row['preferred_supplier']}")
            st.write(f"**Supplier rationale:** {row['supplier_reason']}")
            if row["expiry_warning"]:
                st.write(f"**Expiry warning:** {row['expiry_warning']}")
            pending_val = row.get(pending_col) if pending_col else None
            if pd.notna(pending_val) and pending_val:
                st.write(f"**Pending orders:** {pending_val}")
            st.write("**Evidence:** " + ", ".join(row["evidence_ids"]))

st.subheader("Gemma 4 Copilot")
st.info("Logistics and procurement support only. Deterministic calculations are the source of truth.")

selected = st.selectbox("Choose a medicine for Gemma to analyze", results["medicine_name"].tolist())
selected_row = results[results["medicine_name"] == selected].iloc[0].to_dict()
if "pending_order_note" in selected_row:
    selected_row["pending_order_notes"] = selected_row.pop("pending_order_note")

with st.expander("Evidence & Audit Trail", expanded=False):
    st.caption("These values are calculated by the deterministic analytics engine. Gemma 4 receives this structured context for explanation only.")
    st.write(f"- **Medicine Name:** {selected_row.get('medicine_name')}")
    st.write(f"- **Medicine ID:** {selected_row.get('medicine_id')}")
    st.write(f"- **Current Stock:** {selected_row.get('current_stock_units')} units")
    st.write(f"- **Avg Daily Demand:** {selected_row.get('avg_daily_demand')}")
    st.write(f"- **Days of Cover:** {selected_row.get('days_of_cover')}")
    st.write(f"- **Projected Stockout Date:** {selected_row.get('projected_stockout_date')}")
    st.write(f"- **Risk Level:** {str(selected_row.get('risk_level', '')).upper()}")
    
    qty = selected_row.get('recommended_quantity_units')
    if pd.isna(qty):
        qty = selected_row.get('recommended_reorder_quantity')
    st.write(f"- **Recommended Quantity:** {qty} units")
    
    st.write(f"- **Preferred Supplier:** {selected_row.get('preferred_supplier')}")
    st.write(f"- **Supplier Reason:** {selected_row.get('supplier_reason')}")
    
    exp_warn = selected_row.get('expiry_warning')
    if pd.notna(exp_warn) and exp_warn:
        st.write(f"- **Expiry Warning:** {exp_warn}")
        
    pending = selected_row.get('pending_order_notes')
    if pd.isna(pending):
        pending = selected_row.get('pending_order_note')
    if pd.notna(pending) and pending:
        st.write(f"- **Pending Orders:** {pending}")
        
    ev_ids = selected_row.get('evidence_ids', [])
    if ev_ids:
        st.write(f"- **Evidence IDs:** {', '.join(ev_ids)}")

st.markdown("---")
st.write("**Generate Artifacts**")

col1, col2 = st.columns(2)
with col1:
    if st.button("Generate risk explanation (Gemma)"):
        with st.spinner("Generating explanation..."):
            st.write(client.explain_stockout_risk(selected_row))

with col2:
    if st.button("Generate procurement message (Gemma)"):
        with st.spinner("Generating message..."):
            st.write(client.generate_procurement_message(selected_row))

st.markdown("---")
st.write("**Export Procurement Brief (Deterministic)**")
brief_md = generate_procurement_brief(selected_row)
with st.expander("Preview Procurement Brief", expanded=False):
    st.markdown(brief_md)

st.download_button(
    label="Download procurement brief",
    data=brief_md,
    file_name=f"procurement_brief_{str(selected_row.get('medicine_name', 'medicine')).replace(' ', '_')}.md",
    mime="text/markdown"
)

st.markdown("---")
st.write("**Ask a logistics question about this medicine:**")
question = st.text_input("Example: 'Why are we reordering from Supplier B?'")
if st.button("Ask Gemma"):
    if question:
        with st.spinner("Answering..."):
            st.write(client.answer_question(question, selected_row, all_results=results))
    else:
        st.warning("Please enter a question.")

st.subheader("Raw sample data")
with st.expander("Inventory"):
    st.dataframe(inventory, use_container_width=True, hide_index=True)
with st.expander("Demand history"):
    st.dataframe(demand_history.tail(50), use_container_width=True, hide_index=True)
with st.expander("Suppliers"):
    st.dataframe(suppliers, use_container_width=True, hide_index=True)
with st.expander("Pending orders"):
    st.dataframe(pending_orders, use_container_width=True, hide_index=True)
