"""
04_sensitivity.py — what actually drives the answer, and where it breaks.

Three analyses, in increasing order of usefulness:

1. TORNADO   — flex one driver at a time by +/-25% and measure the swing in the
               mature-year contribution margin per order. This answers "which
               assumption do I need to be right about?"
2. TWO-WAY   — AOV x drop-point density on the same metric. This answers "what
               combinations of basket size and network utilisation work?"
3. BREAKEVEN — solve for the density at which the mature business stops losing
               money. This is the number to put on a dashboard.

Outputs
-------
outputs/sensitivity_tornado.csv
outputs/sensitivity_2way.csv
outputs/sensitivity_breakeven.csv
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
import lib

FLEX = 0.25   # every driver flexed by +/-25%, so the tornado bars are comparable

# (display name, config container, key, year to flex or None for a scalar)
DRIVERS = [
    ("Gross margin % of GMV (Year 3)", "margin", "gross_margin_pct_of_gmv", 3),
    ("AOV (Year 3)", "demand", "aov_inr", 3),
    ("Ad revenue % of GMV (Year 3)", "margin", "ad_revenue_pct_of_gmv", 3),
    ("Marketing % of GMV (Year 3)", "cost", "marketing_pct_of_gmv", 3),
    ("Orders per drop point per day (Year 3)", "demand", "orders_per_drop_point_per_day", 3),
    ("Shrinkage % of GMV", "cost", "shrinkage_pct_of_gmv", None),
    ("Drop-point fixed cost per month", "cost", "drop_point_fixed_cost_per_month_inr", None),
    ("Vehicle run cost", "cost", "drop_point_vehicle_run_cost_inr", None),
    ("Orders per vehicle run", "cost", "orders_per_vehicle_run", None),
    ("Drop-point handling fee per order", "cost", "drop_point_handling_fee_per_order_inr", None),
    ("Refusal rate at drop point", "cost", "rto_rate_drop_point", None),
    ("Warehouse fixed cost (Year 3)", "cost", "warehouse_fixed_cost_per_month_inr", 3),
    ("Tech and people cost (Year 3)", "cost", "tech_and_people_per_month_inr", 3),
]


def configs():
    return lib.resolve_scenario("base", C)


def flexed_metric(container: str, key: str, year, mult: float, metric: str) -> float:
    """Mature-year result with exactly one driver flexed."""
    cost, demand, margin = configs()
    target = {"cost": cost, "demand": demand, "margin": margin}[container]

    if year is None:
        target[key] = target[key] * mult
    else:
        target[key] = dict(target[key])
        target[key][year] = target[key][year] * mult

    return lib.build_pnl(cost, demand, margin)[-1][metric]


def main() -> None:
    C.OUT.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ tornado
    # Measured on Year-3 EBITDA rather than CM2 per order, so that fixed-cost
    # drivers register a non-zero swing and the ranking covers every assumption
    # in the model rather than only those above the CM2 line.
    METRIC = "ebitda_cr"
    base_val = flexed_metric("demand", "aov_inr", 3, 1.0, METRIC)
    rows = []
    for name, container, key, year in DRIVERS:
        low = flexed_metric(container, key, year, 1 - FLEX, METRIC)
        high = flexed_metric(container, key, year, 1 + FLEX, METRIC)
        rows.append({
            "driver": name,
            "low_inr_cr": low,
            "high_inr_cr": high,
            "swing_inr_cr": round(abs(high - low), 2),
            "direction": "higher driver is better" if high >= low else "lower driver is better",
        })
    tor = pd.DataFrame(rows).sort_values("swing_inr_cr", ascending=False).reset_index(drop=True)
    tor.insert(0, "rank", tor.index + 1)
    tor.to_csv(C.OUT / "sensitivity_tornado.csv", index=False)

    print(f"TORNADO - swing in Year-3 EBITDA when each driver moves +/-{FLEX:.0%}")
    print("=" * 92)
    print(f"  Base-case Year-3 EBITDA: Rs {base_val:,.1f} Cr")
    print()
    for _, r in tor.iterrows():
        print(f"  {r['rank']:>2}. {r['driver']:<42} "
              f"Rs {r['low_inr_cr']:>9,.1f} Cr  to  Rs {r['high_inr_cr']:>9,.1f} Cr   "
              f"swing Rs {r['swing_inr_cr']:>8,.1f} Cr")
    print()

    # ------------------------------------------------------------------ two-way
    aov_grid = [420, 460, 500, 540, 580, 620]
    dens_grid = [20, 25, 30, 35, 40, 45, 50, 55]
    grid = []
    for dens in dens_grid:
        row = {"orders_per_point_per_day": dens}
        for aov in aov_grid:
            cost, demand, margin = configs()
            demand["aov_inr"] = dict(demand["aov_inr"]); demand["aov_inr"][3] = float(aov)
            demand["orders_per_drop_point_per_day"] = dict(demand["orders_per_drop_point_per_day"])
            demand["orders_per_drop_point_per_day"][3] = float(dens)
            row[f"aov_{aov}"] = lib.build_pnl(cost, demand, margin)[-1]["cm2_per_order_inr"]
        grid.append(row)
    two = pd.DataFrame(grid)
    two.to_csv(C.OUT / "sensitivity_2way.csv", index=False)

    print("TWO-WAY - Year-3 CM2 per order by basket size and network density")
    print("=" * 92)
    print(two.round(1).to_string(index=False))
    print()

    # ------------------------------------------------------------------ breakeven
    # Solve for the mature-year density at which CM2 per order crosses zero.
    lo, hi = 1.0, 400.0
    cost, demand, margin = configs()
    demand = {**demand, "orders_per_drop_point_per_day":
              {**demand["orders_per_drop_point_per_day"], 3: lo}}
    if lib.build_pnl(cost, demand, margin)[-1]["cm2_per_order_inr"] > 0:
        be_density = float("nan")
    else:
        for _ in range(120):
            mid = (lo + hi) / 2
            demand = {**demand, "orders_per_drop_point_per_day":
                      {**demand["orders_per_drop_point_per_day"], 3: mid}}
            if lib.build_pnl(cost, demand, margin)[-1]["cm2_per_order_inr"] < 0:
                lo = mid
            else:
                hi = mid
        be_density = (lo + hi) / 2

    planned = C.DEMAND["orders_per_drop_point_per_day"][3]
    bdf = pd.DataFrame([
        {"metric": "Mature-year CM2 breakeven density (orders per point per day)",
         "value": round(be_density, 1)},
        {"metric": "Planned mature-year density", "value": planned},
        {"metric": "Headroom vs breakeven",
         "value": round(planned / be_density, 2) if be_density == be_density else None},
        {"metric": "Operational rollout gate in config",
         "value": C.GATES["target_orders_per_point_per_day"]},
        {"metric": "Note",
         "value": "The config gate is an operational floor for opening a point; "
                  "the economic threshold above it is stricter. Both must be reported."},
    ])
    bdf.to_csv(C.OUT / "sensitivity_breakeven.csv", index=False)

    print("BREAKEVEN DENSITY")
    print("=" * 92)
    print(bdf.to_string(index=False))
    print()
    print("Wrote: sensitivity_tornado.csv, sensitivity_2way.csv, sensitivity_breakeven.csv")


if __name__ == "__main__":
    main()
