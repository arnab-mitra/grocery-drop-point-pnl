"""
01_market_sizing.py — TAM / SAM / SOM for grocery in Tier-2/3+ India.

Built bottom-up from households, then triangulated against the published
top-down market size. Where the two disagree the script says so rather than
quietly picking the flattering number, because the definitional gap between
"grocery" and "food and grocery" is a real analytical trap in this category.

Outputs
-------
outputs/market_sizing.csv     layered funnel with INR crore and USD billion
outputs/triangulation.csv     bottom-up vs published top-down, with the gap explained
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

USD_INR = 83.0  # [ASSUMPTION] working rate; stated so the conversion is auditable
CRORE = 1e7


def bn_to_cr(usd_bn: float) -> float:
    return usd_bn * USD_INR * 1e2  # 1 bn USD = 100 cr INR * rate


def main() -> None:
    m = C.MARKET

    households = m["india_population"] / m["avg_household_size"]
    tier23_hh = households * m["tier23plus_household_share"]

    annual_spend_per_hh = m["monthly_grocery_spend_per_hh_inr"] * 12
    tam_all_india = households * annual_spend_per_hh
    tam = tier23_hh * annual_spend_per_hh
    staple_tam = tam * m["packaged_staples_share_of_spend"]
    sam = staple_tam * m["online_addressable_share"]
    som = sam * m["three_year_share_of_sam"]

    layers = [
        ("TAM - all-India household grocery spend",
         households, tam_all_india, "All Indian households x monthly grocery spend x 12"),
        ("TAM - Tier-2/3+ household grocery spend",
         tier23_hh, tam, "Households outside the top metros"),
        ("Served-adjacent - packaged staples and non-perishable FMCG",
         tier23_hh, staple_tam, "Excludes fresh (cold chain, shrinkage, q-commerce's home turf)"),
        ("SAM - online-addressable share of that",
         tier23_hh, sam, "What is realistically transactable online in the medium term"),
        ("SOM - a new entrant's 3-year share",
         tier23_hh, som, "Deliberately conservative: a 0-1 bet against q-commerce and kirana"),
    ]

    rows = []
    for name, hh, value, note in layers:
        rows.append({
            "layer": name,
            "base_households_mn": round(hh / 1e6, 1),
            "value_inr_cr": round(value / CRORE, 0),
            "value_usd_bn": round(value / CRORE / 100 / USD_INR, 1),
            "basis": note,
        })
    df = pd.DataFrame(rows)

    C.OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(C.OUT / "market_sizing.csv", index=False)

    print("MARKET SIZING (bottom-up)")
    print("=" * 78)
    print(f"  India households                     : {households/1e6:,.1f} mn")
    print(f"  Tier-2/3+ households                 : {tier23_hh/1e6:,.1f} mn "
          f"({m['tier23plus_household_share']:.0%} of total)")
    print(f"  Assumed monthly grocery spend        : Rs {m['monthly_grocery_spend_per_hh_inr']:,}")
    print()
    for _, r in df.iterrows():
        print(f"  {r['layer']:<52} Rs {r['value_inr_cr']:>10,.0f} Cr  (${r['value_usd_bn']:>6,.1f} bn)")
    print()

    # ------------------------------------------------------------------ triangulation
    published_food_grocery_usd_bn = 658.0   # [PUBLISHED] India food & grocery market
    published_grocery_usd_bn = None         # set if a narrower published figure is available
    bottom_up_all_india_cr = tam_all_india / CRORE

    tri = pd.DataFrame([
        {"method": "Bottom-up: all-India household grocery",
         "value_inr_cr": round(bottom_up_all_india_cr, 0),
         "value_usd_bn": round(bottom_up_all_india_cr / 100 / USD_INR, 1),
         "basis": "This model: households x spend x 12"},
        {"method": "Top-down published: India food & grocery",
         "value_inr_cr": round(bn_to_cr(published_food_grocery_usd_bn), 0),
         "value_usd_bn": published_food_grocery_usd_bn,
         "basis": "Published industry estimate (see data/SOURCES.md)"},
    ])
    tri["gap_pct"] = (
        (tri["value_usd_bn"] - tri["value_usd_bn"].iloc[0])
        / tri["value_usd_bn"].iloc[0] * 100
    ).round(1)
    tri.to_csv(C.OUT / "triangulation.csv", index=False)

    print("TRIANGULATION")
    print("=" * 78)
    print(tri[["method", "value_usd_bn", "gap_pct"]].to_string(index=False))
    print()
    print("  Read the gap, do not hide it. 'Food and grocery' in the published figure is")
    print("  a broader basket than household groceries and typically includes eating out,")
    print("  which this model deliberately excludes. The bottom-up number is the one used")
    print("  for the rest of the case, because it is built from a Tier-2/3+ household base")
    print("  that matches the strategic question being asked.")
    print()
    print("Wrote: market_sizing.csv, triangulation.csv")


if __name__ == "__main__":
    main()
