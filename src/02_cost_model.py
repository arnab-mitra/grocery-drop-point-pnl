"""
02_cost_model.py — unbundle cost per order, then compare home delivery with drop point.

The discipline here is that ONLY the last mile differs between the two models.
First mile, sortation, line haul, payment and packaging are held identical, so
any cost advantage measured is attributable to the drop-point thesis itself and
not to a convenient assumption smuggled in elsewhere. If an interviewer wants to
challenge the result, they must attack the last mile, which is exactly where the
argument should live.

All cost logic lives in lib.py so this comparison and the P&L share one definition.

Outputs
-------
outputs/cost_comparison.csv   line-by-line cost per order, both models
outputs/density_curve.csv     drop-point last-mile cost vs orders per vehicle run
outputs/breakeven.csv         the density and AOV at which the model turns
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
import lib


def main() -> None:
    cost = dict(C.COST)
    aov = C.DEMAND["aov_inr"][3]      # mature-year basket: the fair steady-state comparison
    orders_per_run = cost["orders_per_vehicle_run"]

    common = lib.common_stages(cost, aov)
    common_total = sum(common.values())
    home_lm = lib.last_mile_home(cost)
    dp_lm = lib.last_mile_drop_point(cost, orders_per_run)
    home_total = common_total + home_lm
    dp_total = common_total + dp_lm

    rows = [{"stage": k, "home_delivery_inr": round(v, 2), "drop_point_inr": round(v, 2),
             "delta_inr": 0.0, "note": "identical in both models"}
            for k, v in common.items()]
    rows.append({"stage": "Last mile", "home_delivery_inr": round(home_lm, 2),
                 "drop_point_inr": round(dp_lm, 2), "delta_inr": round(dp_lm - home_lm, 2),
                 "note": f"drop point at {orders_per_run:.0f} orders per vehicle run"})
    rows.append({"stage": "TOTAL cost per order", "home_delivery_inr": round(home_total, 2),
                 "drop_point_inr": round(dp_total, 2),
                 "delta_inr": round(dp_total - home_total, 2), "note": ""})

    df = pd.DataFrame(rows)
    df["delta_pct"] = (df["delta_inr"] / df["home_delivery_inr"].replace(0, pd.NA) * 100).round(1)

    C.OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(C.OUT / "cost_comparison.csv", index=False)

    print("COST PER ORDER, MATURE-YEAR BASKET")
    print("=" * 88)
    print(f"  Reference AOV: Rs {aov:,.0f}")
    print()
    print(df.to_string(index=False))
    saving = home_total - dp_total
    print()
    print(f"  Saving per order : Rs {saving:,.2f}  ({saving/home_total:.1%} of total cost)")
    print()

    # ------------------------------------------------------------------ density curve
    curve = []
    for orders in [5, 10, 15, 20, 25, 30, 40, 45, 55, 70, 90]:
        lm = lib.last_mile_drop_point(cost, orders)
        curve.append({
            "orders_per_vehicle_run": orders,
            "drop_point_last_mile_inr": round(lm, 2),
            "drop_point_total_cost_inr": round(common_total + lm, 2),
            "home_total_cost_inr": round(home_total, 2),
            "advantage_vs_home_inr": round(home_total - (common_total + lm), 2),
        })
    cdf = pd.DataFrame(curve)
    cdf.to_csv(C.OUT / "density_curve.csv", index=False)
    print("DENSITY CURVE - this is a density business, not a delivery business")
    print("=" * 88)
    print(cdf.to_string(index=False))
    print()

    # ------------------------------------------------------------------ breakeven
    # Solve for the orders-per-run at which the two models cost the same.
    lo, hi = 1.0, 500.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if common_total + lib.last_mile_drop_point(cost, mid) > home_total:
            lo = mid
        else:
            hi = mid
    be_density = (lo + hi) / 2

    # And the AOV at which the mature drop-point model covers its own variable cost
    gm = C.MARGIN["gross_margin_pct_of_gmv"][3]
    be_aov = dp_total / gm

    bdf = pd.DataFrame([
        {"metric": "Breakeven orders per vehicle run", "value": round(be_density, 1),
         "interpretation": "Below this density drop point costs MORE than home delivery"},
        {"metric": "Modelled density at maturity", "value": orders_per_run,
         "interpretation": f"Headroom: {orders_per_run/be_density:.2f}x the breakeven density"},
        {"metric": "Breakeven AOV at mature density", "value": round(be_aov, 0),
         "interpretation": f"Gross margin of {gm:.1%} must cover Rs {dp_total:,.2f} of cost per order"},
        {"metric": "Modelled AOV at maturity", "value": C.DEMAND["aov_inr"][3],
         "interpretation": "The margin, not the basket size, is the binding constraint"},
    ])
    bdf.to_csv(C.OUT / "breakeven.csv", index=False)
    print("BREAKEVEN")
    print("=" * 88)
    print(bdf.to_string(index=False))
    print()

    # ------------------------------------------------------------------ validation
    # Check the modelled cost against what real Indian operators disclose. This
    # is the step that stops a model from being internally consistent but
    # externally wrong.
    rows = []
    for b in C.BENCHMARKS:
        rows.append({"source": b["operator"], "cost_per_order_inr": b["cost_per_order_inr"],
                     "type": b["type"], "basis": b["basis"]})
    rows.append({"source": "This model - home delivery", "cost_per_order_inr": round(home_total, 2),
                 "type": "model", "basis": "All stages, home last mile with refusal cost"})
    rows.append({"source": "This model - drop point", "cost_per_order_inr": round(dp_total, 2),
                 "type": "model", "basis": f"All stages, drop point at {orders_per_run:.0f} orders/run"})
    vdf = pd.DataFrame(rows).sort_values("cost_per_order_inr")
    vdf.to_csv(C.OUT / "benchmark_validation.csv", index=False)
    print("BENCHMARK VALIDATION - does the model land where real operators land?")
    print("=" * 88)
    print(vdf.to_string(index=False))
    print()
    print("  Read: the drop-point figure should sit BELOW the delivered models (that is the")
    print("  thesis) but not implausibly far below the cheapest disclosed operator (Meesho).")
    print("  A number far under the Meesho figure would indicate the last mile is under-costed.")
    print()
    print("Wrote: cost_comparison.csv, density_curve.csv, breakeven.csv, benchmark_validation.csv")


if __name__ == "__main__":
    main()
