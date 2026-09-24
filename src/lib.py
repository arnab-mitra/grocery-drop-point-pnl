"""
lib.py — shared model logic.

The numbered scripts (01_, 02_, ...) are executables and are not importable as
modules because their names begin with a digit. All logic that more than one
script needs therefore lives here, so that the cost definition exists in exactly
one place and the P&L cannot drift away from the cost model.
"""

from pathlib import Path

# Working conversion rate. Stated explicitly rather than buried, so any USD
# figure in the outputs is auditable back to the rupee number it came from.
USD_INR = 83.0
CRORE = 1e7


# ---------------------------------------------------------------------------
# COST MODEL
# ---------------------------------------------------------------------------
def last_mile_home(cost: dict) -> float:
    """
    Home delivery: one parcel, one doorstep, plus the expected cost of refusals.

    Refusals are an EXPECTED cost (rate x cost). This is where home delivery is
    structurally expensive: a refused COD parcel costs a forward and a return
    leg and earns nothing.
    """
    base = cost["home_last_mile_per_order_inr"]
    rto = cost["rto_rate_home"] * base * cost["rto_cost_multiplier_home"]
    return base + rto


def last_mile_drop_point(cost: dict, orders_per_run: float) -> float:
    """
    Drop point: a single vehicle run serves many orders at one location, so the
    per-order cost of the leg collapses as density rises.

    Two distinct advantages are modelled here, and it is worth keeping them
    separate when defending the case:
      1. BATCHING - one run serves `orders_per_run` orders.
      2. PAY-ON-COLLECTION - a no-show is a stock event, not a wasted trip, so
         the refusal cost multiplier is far below the home-delivery case.
    """
    if orders_per_run <= 0:
        raise ValueError("orders_per_run must be positive")
    run_component = cost["drop_point_vehicle_run_cost_inr"] / orders_per_run
    handling = cost["drop_point_handling_fee_per_order_inr"]
    base = run_component + handling
    rto = (cost["rto_rate_drop_point"] * base
           * cost["rto_cost_multiplier_drop_point"])
    return base + rto


def common_stages(cost: dict, aov: float) -> dict:
    """
    Supply-chain stages that are IDENTICAL in both models. Holding these fixed is
    what makes the measured advantage attributable to the drop point alone.
    """
    return {
        "First mile (seller to FC)": cost["first_mile_per_order_inr"],
        "Sortation": cost["sortation_per_order_inr"],
        "Line haul (FC to city)": cost["line_haul_per_order_inr"],
        "Payment": cost["payment_per_order_inr"],
        "Packaging": cost["packaging_per_order_inr"],
        "Shrinkage": cost["shrinkage_pct_of_gmv"] * aov,
    }


def variable_cost_per_order(cost: dict, aov: float, orders_per_run: float) -> tuple[float, float, float]:
    """
    Returns (total variable cost per order, common-stage total, drop-point last mile).
    Single definition, used by both the cost comparison and the P&L.
    """
    common = sum(common_stages(cost, aov).values())
    lm = last_mile_drop_point(cost, orders_per_run)
    return common + lm, common, lm


def home_total_cost(cost: dict, aov: float) -> tuple[float, float]:
    """Returns (total cost per order under home delivery, last-mile component)."""
    common = sum(common_stages(cost, aov).values())
    lm = last_mile_home(cost)
    return common + lm, lm


# ---------------------------------------------------------------------------
# SCENARIO RESOLUTION
# ---------------------------------------------------------------------------
def scale(value, mult: float):
    """Apply a multiplier to a scalar or to a {year: value} dict."""
    if isinstance(value, dict):
        return {k: v * mult for k, v in value.items()}
    return value * mult


def resolve_scenario(scenario: str, cfg) -> tuple[dict, dict, dict]:
    """
    Merge a scenario's multipliers over the base configuration.

    Because scenarios are expressed only as multipliers on named drivers, the
    bull and bear cases cannot silently diverge in structure from the base case.
    """
    cost = dict(cfg.COST)
    demand = dict(cfg.DEMAND)
    margin = dict(cfg.MARGIN)

    for key, mult in cfg.SCENARIOS[scenario].items():
        if key in cost:
            cost[key] = scale(cost[key], mult)
        elif key in demand:
            demand[key] = scale(demand[key], mult)
        elif key in margin:
            margin[key] = scale(margin[key], mult)
        else:
            raise KeyError(f"Scenario '{scenario}' references unknown driver '{key}'")
    return cost, demand, margin


# ---------------------------------------------------------------------------
# P&L CONSTRUCTION
# ---------------------------------------------------------------------------
def pnl_year(cost: dict, demand: dict, margin: dict, year: int) -> dict:
    """
    One year of the P&L.

    GMV is not assumed: it falls out of the network (drop points x orders per
    point per day x 365), because the investment case is a bet on density.
    """
    points = demand["drop_points"][year]
    density = demand["orders_per_drop_point_per_day"][year]
    orders = points * density * demand["days_per_year"]
    aov = demand["aov_inr"][year]
    gmv = orders * aov

    gm_pct = margin["gross_margin_pct_of_gmv"][year]
    gross_margin = gmv * gm_pct
    ad_pct = margin["ad_revenue_pct_of_gmv"][year]
    ad_revenue = gmv * ad_pct
    platform_gross_profit = gross_margin + ad_revenue

    variable_per_order, _, _ = variable_cost_per_order(
        cost, aov, cost["orders_per_vehicle_run"]
    )
    fulfilment = orders * variable_per_order
    marketing = gmv * cost["marketing_pct_of_gmv"][year]

    dp_fixed = points * cost["drop_point_fixed_cost_per_month_inr"] * 12
    wh_fixed = cost["warehouse_fixed_cost_per_month_inr"][year] * 12
    tech_people = cost["tech_and_people_per_month_inr"][year] * 12

    cm1 = platform_gross_profit - fulfilment - marketing   # after variable cost and acquisition
    cm2 = cm1 - dp_fixed                                   # after the drop-point network
    ebitda = cm2 - wh_fixed - tech_people

    return {
        "year": year,
        "drop_points": int(points),
        "orders_per_point_per_day": density,
        "orders_mn": round(orders / 1e6, 2),
        "customers_mn": round(orders / demand["orders_per_customer_per_year"][year] / 1e6, 2),
        "aov_inr": round(aov, 0),
        "gmv_cr": round(cr(gmv), 1),
        "gross_margin_cr": round(cr(gross_margin), 1),
        "gross_margin_pct": round(gm_pct, 4),
        "ad_revenue_cr": round(cr(ad_revenue), 1),
        "ad_revenue_pct": round(ad_pct, 4),
        "platform_gross_profit_cr": round(cr(platform_gross_profit), 1),
        "platform_gross_profit_pct": round(platform_gross_profit / gmv, 4),
        "fulfilment_cost_cr": round(cr(fulfilment), 1),
        "variable_cost_per_order_inr": round(variable_per_order, 2),
        "marketing_cr": round(cr(marketing), 1),
        "cm1_cr": round(cr(cm1), 1),
        "cm1_per_order_inr": round(cm1 / orders, 2),
        "drop_point_fixed_cr": round(cr(dp_fixed), 1),
        "cm2_cr": round(cr(cm2), 1),
        "cm2_per_order_inr": round(cm2 / orders, 2),
        "warehouse_fixed_cr": round(cr(wh_fixed), 1),
        "tech_people_cr": round(cr(tech_people), 1),
        "ebitda_cr": round(cr(ebitda), 1),
        "ebitda_pct_of_gmv": round(ebitda / gmv, 4),
    }


def build_pnl(cost: dict, demand: dict, margin: dict) -> list[dict]:
    """Three years of P&L plus cumulative EBITDA."""
    rows = [pnl_year(cost, demand, margin, y) for y in (1, 2, 3)]
    cum, out = 0.0, []
    for r in rows:
        cum += r["ebitda_cr"]
        r["cumulative_ebitda_cr"] = round(cum, 1)
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# FORMATTING
# ---------------------------------------------------------------------------
def cr(rupees: float) -> float:
    """Rupees to crore."""
    return rupees / CRORE


def pct(x: float, places: int = 2) -> str:
    return f"{x * 100:.{places}f}%"
