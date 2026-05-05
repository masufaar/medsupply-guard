from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class RiskResult:
    medicine_id: str
    medicine_name: str
    current_stock_units: float
    avg_daily_demand: float
    days_of_cover: Optional[float]
    projected_stockout_date: Optional[date]
    risk_level: str
    recommended_quantity_units: float
    preferred_supplier: Optional[str]
    supplier_reason: str
    expiry_warning: Optional[str]
    evidence_ids: list[str]


def _parse_date(value) -> Optional[date]:
    if pd.isna(value) or value in (None, ""):
        return None
    if isinstance(value, date):
        return value
    return pd.to_datetime(value).date()


def average_daily_demand(demand_history: pd.DataFrame, medicine_id: str, lookback_days: int = 30) -> float:
    df = demand_history[demand_history["medicine_id"] == medicine_id].copy()
    if df.empty:
        return 0.0
    df["date"] = pd.to_datetime(df["date"])
    cutoff = df["date"].max() - pd.Timedelta(days=lookback_days - 1)
    recent = df[df["date"] >= cutoff]
    total = recent["dispensed_units"].sum()
    days = max((recent["date"].max() - recent["date"].min()).days + 1, 1)
    return round(float(total) / days, 2)


def days_of_cover(current_stock_units: float, avg_daily_demand: float) -> Optional[float]:
    if avg_daily_demand <= 0:
        return None
    return round(float(current_stock_units) / float(avg_daily_demand), 1)


def risk_level(days_cover: Optional[float], criticality: str) -> str:
    crit = str(criticality).lower()
    if days_cover is None:
        return "unknown"
    if days_cover <= 7:
        return "critical"
    if days_cover <= 14:
        return "high" if crit in {"high", "critical"} else "medium"
    if days_cover <= 30:
        return "medium"
    return "low"


def recommended_quantity(avg_daily_demand: float, min_target_days: float, current_stock_units: float, pending_units: float = 0) -> float:
    target = max(float(avg_daily_demand) * float(min_target_days), 0)
    needed = target - float(current_stock_units) - float(pending_units)
    return max(round(needed), 0)


def choose_supplier(suppliers: pd.DataFrame, medicine_id: str, days_cover: Optional[float]) -> tuple[Optional[str], str]:
    options = suppliers[suppliers["medicine_id"] == medicine_id].copy()
    if options.empty:
        return None, "No supplier data available."
    options = options.sort_values(["lead_time_days", "unit_cost"])
    if days_cover is None:
        best = options.iloc[0]
        return str(best["supplier_name"]), "Selected fastest available supplier because demand history is insufficient for days-of-cover comparison."
    feasible = options[options["lead_time_days"] <= days_cover]
    if not feasible.empty:
        feasible = feasible.sort_values(["unit_cost", "lead_time_days"])
        best = feasible.iloc[0]
        return str(best["supplier_name"]), "Selected lowest-cost supplier that can arrive before projected stockout."
    best = options.iloc[0]
    return str(best["supplier_name"]), "No supplier can arrive before projected stockout; selected fastest available supplier."


def expiry_warning(expiry_date, today: date, days_cover: Optional[float]) -> Optional[str]:
    exp = _parse_date(expiry_date)
    if exp is None:
        return "Expiry date missing."
    days_to_expiry = (exp - today).days
    if days_to_expiry < 0:
        return "Stock is already expired. Remove from usable inventory."
    if days_to_expiry <= 30:
        return f"Stock expires in {days_to_expiry} days. Review before reordering."
    if days_cover is not None and days_to_expiry < days_cover:
        return "Stock may expire before projected use. Review consumption and redistribution options."
    return None


def analyze_inventory(
    inventory: pd.DataFrame,
    demand_history: pd.DataFrame,
    suppliers: pd.DataFrame,
    pending_orders: pd.DataFrame,
    today: Optional[date] = None,
) -> pd.DataFrame:
    today = today or date.today()
    rows: list[RiskResult] = []
    pending_by_med = pending_orders.groupby("medicine_id")["quantity_units"].sum().to_dict() if not pending_orders.empty else {}

    for _, item in inventory.iterrows():
        med_id = str(item["medicine_id"])
        avg = average_daily_demand(demand_history, med_id)
        cover = days_of_cover(float(item["current_stock_units"]), avg)
        stockout_date = today + timedelta(days=int(cover)) if cover is not None else None
        pending_qty = float(pending_by_med.get(med_id, 0))
        qty = recommended_quantity(avg, float(item.get("min_target_days", 30)), float(item["current_stock_units"]), pending_qty)
        supplier, reason = choose_supplier(suppliers, med_id, cover)
        expiry = expiry_warning(item.get("expiry_date"), today, cover)
        evidence = [str(item.get("evidence_id", f"inventory:{med_id}"))]
        evidence.append(f"demand:{med_id}:last_30_days")
        if supplier:
            evidence.append(f"supplier:{med_id}")
        rows.append(
            RiskResult(
                medicine_id=med_id,
                medicine_name=str(item["medicine_name"]),
                current_stock_units=float(item["current_stock_units"]),
                avg_daily_demand=avg,
                days_of_cover=cover,
                projected_stockout_date=stockout_date,
                risk_level=risk_level(cover, str(item.get("criticality", "medium"))),
                recommended_quantity_units=qty,
                preferred_supplier=supplier,
                supplier_reason=reason,
                expiry_warning=expiry,
                evidence_ids=evidence,
            )
        )
    return pd.DataFrame([r.__dict__ for r in rows])
