from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics.inventory_math import analyze_inventory
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

results = analyze_inventory(inventory, demand_history, suppliers, pending_orders, today=date(2026, 5, 4))

risk_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "unknown": 4}
results["risk_sort"] = results["risk_level"].map(risk_order).fillna(5)
results = results.sort_values(["risk_sort", "days_of_cover"], na_position="last")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Medicines monitored", len(results))
k2.metric("Critical risks", int((results["risk_level"] == "critical").sum()))
k3.metric("High risks", int((results["risk_level"] == "high").sum()))
k4.metric("Orders recommended", int((results["recommended_quantity_units"] > 0).sum()))

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
    "expiry_warning",
]
st.dataframe(results[display_cols], use_container_width=True, hide_index=True)

chart_df = results.dropna(subset=["days_of_cover"]).copy()
if not chart_df.empty:
    fig = px.bar(chart_df, x="medicine_name", y="days_of_cover", color="risk_level", title="Days of cover by medicine")
    st.plotly_chart(fig, use_container_width=True)

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
            st.write("**Evidence:** " + ", ".join(row["evidence_ids"]))

st.subheader("Gemma 4 copilot")
st.info("Day 1 uses a GemmaClient stub. On Day 3, wire this to the competition-supported Gemma 4 runtime.")
client = GemmaClient(offline_stub=True)
selected = st.selectbox("Choose a medicine for explanation", results["medicine_name"].tolist())
selected_row = results[results["medicine_name"] == selected].iloc[0].to_dict()
if st.button("Generate grounded explanation"):
    st.write(client.explain_stockout_risk(selected_row))

st.subheader("Raw sample data")
with st.expander("Inventory"):
    st.dataframe(inventory, use_container_width=True, hide_index=True)
with st.expander("Demand history"):
    st.dataframe(demand_history.tail(50), use_container_width=True, hide_index=True)
with st.expander("Suppliers"):
    st.dataframe(suppliers, use_container_width=True, hide_index=True)
with st.expander("Pending orders"):
    st.dataframe(pending_orders, use_container_width=True, hide_index=True)
