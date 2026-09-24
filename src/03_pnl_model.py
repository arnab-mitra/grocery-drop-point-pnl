"""
03_pnl_model.py — three-year P&L for the drop-point grocery model, base / bull / bear.

Structure
---------
GMV is not assumed. It falls out of the network (drop points x orders per point
per day x 365), because the entire investment case is a bet on density. Costs are
then built in the order a real P&L is read:

    GMV
      - COGS                          -> Gross margin
      - fulfilment cost per order     -> CM1  (contribution after variable cost)
      - marketing
      - drop-point fixed cost         -> CM2  (contribution after the network)
      - warehouse, tech and people    -> EBITDA

Scenarios are applied as MULTIPLIERS on named drivers (lib.resolve_scenario), so
the bull and bear cases cannot silently diverge in structure from the base case.
The P&L mechanics themselves live in lib.build_pnl, so this script cannot drift
away from the cost model in 02_cost_model.py.

Outputs
-------
outputs/pnl_<scenario>.csv      full P&L by year
outputs/pnl_all_scenarios.csv   long format, all three cases
outputs/case_summary.csv        the comparison an investor would actually read
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
import lib


# ---------------------------------------------------------------------------
def build(scenario: str) -> pd.DataFrame:
    """Resolve a scenario's multipliers, then build its three-year P&L."""
    cost, demand, margin = lib.resolve_scenario(scenario, C)
    df = pd.DataFrame(lib.build_pnl(cost, demand, margin))
    df.insert(0, "scenario", scenario)
    return df


# ---------------------------------------------------------------------------
def main() -> None:
    C.OUT.mkdir(parents=True, exist_ok=True)

    frames = []
    for scenario in C.SCENARIOS:
        df = build(scenario)
        df.to_csv(C.OUT / f"pnl_{scenario}.csv", index=False)
        frames.append(df)
    allsc = pd.concat(frames, ignore_index=True)
    allsc.to_csv(C.OUT / "pnl_all_scenarios.csv", index=False)

    # ------------------------------------------------------------------ summary
    summary = []
    for scenario in C.SCENARIOS:
        d = allsc[allsc["scenario"] == scenario]
        y3 = d[d["year"] == 3].iloc[0]
        cm_positive = d[d["cm2_per_order_inr"] > 0]["year"].tolist()
        peak_burn = abs(min(d["cumulative_ebitda_cr"].min(), 0))
        summary.append({
            "scenario": scenario,
            "y3_orders_mn": y3["orders_mn"],
            "y3_gmv_cr": y3["gmv_cr"],
            "y3_gross_margin_cr": y3["gross_margin_cr"],
            "y3_cm1_per_order_inr": y3["cm1_per_order_inr"],
            "y3_cm2_per_order_inr": y3["cm2_per_order_inr"],
            "y3_ebitda_cr": y3["ebitda_cr"],
            "y3_ebitda_pct": y3["ebitda_pct_of_gmv"],
            "first_year_cm2_positive": cm_positive[0] if cm_positive else None,
            "cumulative_ebitda_cr": round(d["ebitda_cr"].sum(), 1),
            "peak_cumulative_burn_cr": round(peak_burn, 1),
        })
    sdf = pd.DataFrame(summary)
    sdf.to_csv(C.OUT / "case_summary.csv", index=False)

    # ------------------------------------------------------------------ report
    print("THREE-YEAR P&L - BASE CASE")
    print("=" * 104)
    base = allsc[allsc["scenario"] == "base"]
    cols = ["year", "drop_points", "orders_mn", "gmv_cr", "gross_margin_cr",
            "ad_revenue_cr", "platform_gross_profit_cr", "variable_cost_per_order_inr",
            "cm1_per_order_inr", "cm2_per_order_inr", "ebitda_cr", "ebitda_pct_of_gmv"]
    print(base[cols].to_string(index=False))
    print()

    print("SCENARIO COMPARISON (Year 3)")
    print("=" * 104)
    print(sdf[["scenario", "y3_orders_mn", "y3_gmv_cr", "y3_cm1_per_order_inr",
               "y3_cm2_per_order_inr", "y3_ebitda_cr", "y3_ebitda_pct",
               "peak_cumulative_burn_cr"]].to_string(index=False))
    print()

    # ------------------------------------------------------------------ gates
    print("DECISION GATES  (a recommendation without kill criteria is not a business case)")
    print("=" * 104)
    for scenario in C.SCENARIOS:
        d = allsc[allsc["scenario"] == scenario]
        y3 = d[d["year"] == 3].iloc[0]
        cm_ok = bool(y3["cm2_per_order_inr"] > C.GATES["target_cm_per_order_inr"])
        dens_ok = bool(y3["orders_per_point_per_day"] >= C.GATES["target_orders_per_point_per_day"])
        burn = abs(min(d["cumulative_ebitda_cr"].min(), 0))
        burn_ok = bool(burn <= C.GATES["max_cumulative_cash_burn_cr"])
        verdict = "PROCEED" if (cm_ok and dens_ok and burn_ok) else "STOP / RESTRUCTURE"
        print(f"  {scenario:<6} CM2/order>0: {str(cm_ok):<5}  density gate: {str(dens_ok):<5}  "
              f"peak burn Rs {burn:>6,.0f} Cr (limit {C.GATES['max_cumulative_cash_burn_cr']:,}): "
              f"{str(burn_ok):<5} -> {verdict}")
    print()
    print("Wrote: pnl_base.csv, pnl_bull.csv, pnl_bear.csv, pnl_all_scenarios.csv, case_summary.csv")


if __name__ == "__main__":
    main()
