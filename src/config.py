"""
config.py — every assumption for the grocery drop-point business case, in one place.

Anchors marked [PUBLISHED] are from public disclosures (see data/SOURCES.md).
Anchors marked [ASSUMPTION] are the modeller's estimates and are the ones an
interviewer will attack. `SCENARIOS` defines the base / bull / bear cases, so the
difference between them is visible as a small set of named overrides rather than
being buried in the arithmetic.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"

DECISION = (
    "Can a value marketplace build a structurally lower-cost grocery supply chain "
    "in Tier-3 India using a drop-point model, and what does the P&L look like if it does?"
)

# ===========================================================================
# 1. MARKET SIZING
# ===========================================================================
MARKET = {
    "india_population": 1_420_000_000,          # [PUBLISHED] ~2025 estimate
    "avg_household_size": 4.4,                  # [PUBLISHED] Census 2011 / NFHS-5

    # Share of households outside the top metros. Meesho reports ~80% of its
    # 264M annual transacting users come from Tier-2 and beyond, so Tier-2/3+
    # is where this business is being built, not a secondary segment.
    "tier23plus_household_share": 0.72,         # [ASSUMPTION]

    "monthly_grocery_spend_per_hh_inr": 9_500,  # [ASSUMPTION] see SOURCES.md

    # Deliberately excluding fresh. Fresh needs cold chain, has high shrinkage
    # and is where q-commerce already wins on speed. A drop-point model competes
    # on cost of non-perishables, so that is the addressable market modelled.
    "packaged_staples_share_of_spend": 0.55,    # [ASSUMPTION]

    # Share of that spend realistically transactable online in the medium term.
    "online_addressable_share": 0.22,           # [ASSUMPTION]

    # Meesho's own disclosed share of India's grocery market after three years.
    # Set low on purpose: this is a 0-1 bet competing against q-commerce and
    # kirana, and the incumbent history (Superstore retreat) argues for humility.
    "three_year_share_of_sam": 0.008,          # [ASSUMPTION]
}

# ===========================================================================
# 2. DEMAND BUILD (driver-based)
# ===========================================================================
# Orders are not assumed directly. They fall out of the network: how many drop
# points exist x how many orders each handles per day. That makes the operational
# assumption explicit and attackable, which is the point.
DEMAND = {
    "drop_points": {1: 120, 2: 650, 3: 2_200},          # year -> count
    "orders_per_drop_point_per_day": {1: 22, 2: 34, 3: 48},
    "days_per_year": 365,
    "orders_per_customer_per_year": {1: 9.0, 2: 14.0, 3: 19.0},   # [ASSUMPTION]
    "aov_inr": {1: 480, 2: 520, 3: 560},                # [ASSUMPTION] grocery basket
}

# ===========================================================================
# 3. COST MODEL — the core of the case
# ===========================================================================
# Per-order cost is unbundled into the standard supply-chain stages so that the
# only difference between the two models is the stage that actually differs:
# the last mile. Everything upstream is assumed identical, which isolates the
# drop-point thesis cleanly.
COST = {
    # --- stages common to both models --------------------------------------
    "first_mile_per_order_inr": 9.0,
    "sortation_per_order_inr": 6.5,
    "line_haul_per_order_inr": 17.0,
    "payment_per_order_inr": 4.5,        # UPI-dominant basket
    "packaging_per_order_inr": 7.5,
    "shrinkage_pct_of_gmv": 0.011,       # non-perishables only, so low

    # --- last mile: home delivery (the incumbent model) --------------------
    "home_last_mile_per_order_inr": 38.0,
    # Failed deliveries are the expensive part of home delivery: a refused COD
    # parcel costs a full forward AND return leg with no revenue. The rate is
    # anchored on disclosed evidence: Meesho's COD success rate is 77.7%, and
    # COD is 76% of its orders, so ~17% of all orders fail on the COD leg alone.
    # Grocery is a necessity purchase with less fit-risk than apparel, so this
    # is set below that, but above a prepaid-only basket.
    "rto_rate_home": 0.12,
    "rto_cost_multiplier_home": 1.85,    # multiple of the last-mile cost

    # --- last mile: drop point (the proposed model) -----------------------
    # A single vehicle run delivers N orders to one point, so the per-order cost
    # of that leg collapses. This is half the economic thesis.
    "drop_point_vehicle_run_cost_inr": 210.0,   # one run: rider + fuel
    "orders_per_vehicle_run": 45.0,             # at maturity, one point per run
    "drop_point_handling_fee_per_order_inr": 12.0,   # paid to the point operator

    # The other half of the thesis: at a pickup point the customer pays on
    # collection, so a no-show is a STOCK event, not a wasted trip. The goods
    # are non-perishable and go back on the shelf, and nothing extra is driven,
    # because the node is already on the next scheduled run. Hence a rate that
    # is lower AND a cost multiplier far below the home-delivery case.
    "rto_rate_drop_point": 0.09,
    "rto_cost_multiplier_drop_point": 0.35,

    # --- drop point fixed cost --------------------------------------------
    "drop_point_fixed_cost_per_month_inr": 18_000.0,  # operator retainer, signage, space

    # --- upstream fixed cost ----------------------------------------------
    "warehouse_fixed_cost_per_month_inr": {1: 9_000_000, 2: 28_000_000, 3: 62_000_000},
    "tech_and_people_per_month_inr": {1: 22_000_000, 2: 38_000_000, 3: 58_000_000},

    # --- demand generation ------------------------------------------------
    "marketing_pct_of_gmv": {1: 0.075, 2: 0.055, 3: 0.038},
}

# Gross margin on goods sold. A grocery marketplace/wholesale model runs thin:
# staples are the most price-transparent category in Indian retail.
MARGIN = {
    "gross_margin_pct_of_gmv": {1: 0.142, 2: 0.151, 3: 0.158},  # [ASSUMPTION]

    # Advertising and seller-promotion revenue, as a share of GMV. This is a real
    # and material revenue line for e-grocery, not a plug: Meesho's own ad
    # contribution margin is 3.1% of NMV on its core marketplace, and management
    # names ad monetisation as the key profitability lever. Grocery ads start
    # thinner than marketplace ads and build as seller density grows, so these
    # are set well below the core-business rate.
    "ad_revenue_pct_of_gmv": {1: 0.010, 2: 0.016, 3: 0.020},    # [ASSUMPTION]
}

# ===========================================================================
# 4. SCENARIOS
# ===========================================================================
# Multipliers applied to named drivers. Keeping them as multipliers means the
# bull and bear cases cannot silently diverge in structure from the base case.
SCENARIOS = {
    "base": {},
    "bull": {
        "orders_per_drop_point_per_day": 1.30,   # density compounds faster
        "aov_inr": 1.06,                          # basket builds with trust
        "gross_margin_pct_of_gmv": 1.08,          # mix shifts to higher-margin SKUs
        "ad_revenue_pct_of_gmv": 1.15,            # seller density supports more ad load
        "rto_rate_drop_point": 0.80,              # better than expected
        "marketing_pct_of_gmv": 0.85,
        "drop_point_fixed_cost_per_month_inr": 0.92,
    },
    "bear": {
        "orders_per_drop_point_per_day": 0.68,
        "aov_inr": 0.93,
        "gross_margin_pct_of_gmv": 0.92,
        "ad_revenue_pct_of_gmv": 0.85,
        "rto_rate_drop_point": 1.35,
        "marketing_pct_of_gmv": 1.20,
        "drop_point_fixed_cost_per_month_inr": 1.10,
    },
}

# ===========================================================================
# 5. DECISION RULES — the kill criteria
# ===========================================================================
# A recommendation without kill criteria is not a business case. These are the
# thresholds at which the answer becomes "stop".
GATES = {
    # Operational floor for opening a drop point. Note that the ECONOMIC
    # breakeven density is higher than this and is solved for in
    # 04_sensitivity.py; the point of a gate is that it is a stated intention
    # set in advance, not a number reverse-engineered after the fact.
    "target_orders_per_point_per_day": 34,
    "target_cm_per_order_inr": 0.0,             # contribution must be positive
    "max_months_to_cm_positive": 24,
    "max_cumulative_cash_burn_cr": 900,
}

# ===========================================================================
# 6. EXTERNAL BENCHMARKS
# ===========================================================================
# Disclosed figures from real Indian operators. These are NOT inputs to the
# model; they are the independent reference points the modelled cost is checked
# against. If a modelled cost falls outside this range, the model is wrong.
#
# Note on a claim this project deliberately does NOT use: it is widely repeated
# that pickup points are "30-50% cheaper than home delivery". That figure could
# not be traced to any operator disclosure, consultancy report or academic
# source. This model therefore builds the drop-point cost bottom-up instead, and
# reports whatever advantage falls out.
# ===========================================================================
BENCHMARKS = [
    {"operator": "Meesho - value e-commerce, delivered",
     "cost_per_order_inr": 42.0, "type": "disclosed",
     "basis": "Logistics cost per placed order, Q1 FY27"},
    {"operator": "Zepto - q-commerce, supply-chain variable",
     "cost_per_order_inr": 61.2, "type": "disclosed",
     "basis": "Picking, packing and delivery per order, Q4 FY26 DRHP"},
    {"operator": "Spencer's Jiffy - store-led delivery",
     "cost_per_order_inr": 98.5, "type": "disclosed",
     "basis": "Fulfilment cost per order, FY26"},
    {"operator": "Bernstein - q-commerce fulfilment floor",
     "cost_per_order_inr": 99.0, "type": "analyst",
     "basis": "Floor even with batching and efficiency, Apr-May 2026"},
]
