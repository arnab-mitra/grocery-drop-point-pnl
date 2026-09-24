"""
05_charts.py — exhibits for the grocery drop-point case study.

Chart labels use "Rs" rather than the rupee glyph because the default matplotlib
font stack does not reliably include U+20B9, and a missing glyph renders as a box
in a published exhibit.

Outputs (outputs/charts/):
  01_cost_stack.png      cost per order by supply-chain stage, both models
  02_density_curve.png   the thesis in one chart: cost vs network density
  03_pnl_waterfall.png   Year-3 base case, GMV down to EBITDA
  04_scenarios.png       Year-3 outcome across base / bull / bear
  05_tornado.png         which assumption matters most
  06_two_way_heatmap.png basket size x density
  07_market_funnel.png   TAM to SOM
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200,
    "font.size": 9, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
    "figure.facecolor": "white", "axes.facecolor": "white",
})

HOME = "#C0392B"
DP = "#1B6CA8"
ACC = "#1B6CA8"
POS = "#2E7D5B"
NEG = "#C0392B"


def _save(fig, name):
    C.CHARTS.mkdir(parents=True, exist_ok=True)
    fig.savefig(C.CHARTS / name, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote charts/{name}")


# ---------------------------------------------------------------------------
def chart_cost_stack():
    df = pd.read_csv(C.OUT / "cost_comparison.csv")
    df = df[df["stage"] != "TOTAL cost per order"]
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    y = np.arange(len(df))
    h = 0.38

    ax.barh(y + h / 2, df["home_delivery_inr"], height=h, color=HOME, alpha=0.88,
            label="Home delivery (incumbent)", edgecolor="white")
    ax.barh(y - h / 2, df["drop_point_inr"], height=h, color=DP, alpha=0.88,
            label="Drop point (proposed)", edgecolor="white")

    for i, r in enumerate(df.itertuples()):
        ax.text(r.home_delivery_inr + 0.5, i + h / 2, f"{r.home_delivery_inr:.1f}",
                va="center", fontsize=7.5, color="#333333")
        ax.text(r.drop_point_inr + 0.5, i - h / 2, f"{r.drop_point_inr:.1f}",
                va="center", fontsize=7.5, color="#333333")

    ax.set_yticks(y)
    ax.set_yticklabels(df["stage"])
    ax.set_xlabel("Cost per order (Rs)")
    ax.set_title("Only the last mile differs - which is exactly where the argument should live\n"
                 "Every upstream stage is held identical between the two models")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    _save(fig, "01_cost_stack.png")


# ---------------------------------------------------------------------------
def chart_density_curve():
    df = pd.read_csv(C.OUT / "density_curve.csv")
    be = pd.read_csv(C.OUT / "breakeven.csv")
    be_density = float(be.loc[be["metric"].str.contains("Breakeven orders"),
                              "value"].iloc[0])

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.plot(df["orders_per_vehicle_run"], df["drop_point_total_cost_inr"],
            marker="o", color=DP, lw=2, ms=5, label="Drop point: total cost per order")
    home_line = df["home_total_cost_inr"].iloc[0]
    ax.axhline(home_line, color=HOME, ls="--", lw=1.6,
               label="Home delivery: total cost per order")
    ax.axvline(be_density, color="#666666", ls=":", lw=1.4)

    # Annotations are placed in the empty band BETWEEN the drop-point curve and the
    # home-delivery line. Putting them above the home line collides with the title,
    # and below the curve collides with the axis labels.
    ax.annotate(f"breakeven density: {be_density:.1f} orders per run",
                xy=(be_density, home_line), xytext=(be_density + 7, home_line - 9),
                fontsize=8, color="#444444",
                arrowprops=dict(arrowstyle="->", color="#888888", lw=0.9))

    planned = C.COST["orders_per_vehicle_run"]
    ax.axvline(planned, color=ACC, ls="-", lw=1.0, alpha=0.6)
    ax.annotate(f"planned: {planned:.0f} orders per run",
                xy=(planned, df["drop_point_total_cost_inr"].min()),
                xytext=(planned - 24, df["drop_point_total_cost_inr"].min() + 18),
                fontsize=8, color=ACC,
                arrowprops=dict(arrowstyle="->", color=ACC, lw=0.9))

    ax.set_ylim(df["drop_point_total_cost_inr"].min() - 6, home_line + 8)
    ax.set_xlabel("Orders consolidated per vehicle run (network density)")
    ax.set_ylabel("Total cost per order (Rs)")
    ax.set_title("This is a density business, not a delivery business\n"
                 "Below breakeven density the drop-point model is worse than home delivery",
                 pad=12)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    _save(fig, "02_density_curve.png")


# ---------------------------------------------------------------------------
def chart_waterfall():
    """
    A bridge, not a stacked bar. GMV is REPLACED by gross margin as COGS leaves,
    ad revenue is added, and each cost line is then subtracted in sequence until
    the running total lands on EBITDA.

    The chart asserts its own arithmetic: if the bridge does not land on EBITDA the
    figure is wrong and it says so rather than drawing a plausible-looking picture.
    """
    rows = pd.read_csv(C.OUT / "pnl_base.csv")
    y3 = rows[rows["year"] == 3].iloc[0]

    steps = [
        ("GMV", y3["gmv_cr"], "level"),
        ("COGS", -(y3["gmv_cr"] - y3["gross_margin_cr"]), "delta"),
        ("Gross\nmargin", y3["gross_margin_cr"], "subtotal"),
        ("Ad\nrevenue", y3["ad_revenue_cr"], "delta"),
        ("Platform\ngross profit", y3["platform_gross_profit_cr"], "subtotal"),
        ("Fulfilment", -y3["fulfilment_cost_cr"], "delta"),
        ("Marketing", -y3["marketing_cr"], "delta"),
        ("CM1", y3["cm1_cr"], "subtotal"),
        ("Drop-point\nfixed", -y3["drop_point_fixed_cr"], "delta"),
        ("CM2", y3["cm2_cr"], "subtotal"),
        ("Warehouse,\ntech, people",
         -(y3["warehouse_fixed_cr"] + y3["tech_people_cr"]), "delta"),
        ("EBITDA", y3["ebitda_cr"], "total"),
    ]

    running = 0.0
    for _, v, kind in steps:
        running = v if kind in ("level", "subtotal", "total") else running + v
    if abs(running - y3["ebitda_cr"]) > 0.5:
        raise AssertionError(
            f"Waterfall does not reconcile: bridge lands on {running:,.1f} "
            f"but EBITDA is {y3['ebitda_cr']:,.1f}"
        )

    fig, ax = plt.subplots(figsize=(10.4, 5.6))
    running = 0.0
    span = y3["gmv_cr"]
    # One decimal place throughout. Rounding to whole crore made the printed steps
    # fail to sum to the printed subtotal (384 - 262 - 82 showed 40 against a CM1
    # of 41), which is fatal in an exhibit titled "a reconciled bridge".
    fmt = lambda v: f"{v:,.1f}"
    for i, (lab, v, kind) in enumerate(steps):
        if kind == "level":
            ax.bar(i, v, color="#8FAFC4", edgecolor="white")
            running = v
            ax.text(i, v + span * 0.025, fmt(v), ha="center", fontsize=7.6, color="#333333")
        elif kind == "delta":
            ax.bar(i, v, bottom=running, color=NEG if v < 0 else POS, alpha=0.85,
                   edgecolor="white")
            running += v
            ax.text(i, running - span * 0.055, fmt(v), ha="center", fontsize=7.0,
                    color="#333333")
            ax.plot([i - 0.4, i + 0.4], [running, running], color="#AAAAAA", lw=0.8)
        else:
            colour = "#12455F" if kind == "subtotal" else (POS if v >= 0 else NEG)
            ax.bar(i, v, color=colour, edgecolor="white")
            running = v
            ax.text(i, v + (span * 0.025 if v >= 0 else -span * 0.075), fmt(v),
                    ha="center", fontsize=7.8, color="#333333")

    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels([s[0] for s in steps], fontsize=7.4)
    ax.axhline(0, color="#999999", lw=0.9)
    # Explicit headroom: the GMV bar is the tallest and its value label was landing
    # on the title. Padding the title as well keeps the two apart.
    ax.set_ylim(y3["ebitda_cr"] - span * 0.07, y3["gmv_cr"] * 1.13)
    ax.set_ylabel("Rs crore")
    ax.set_title("Year-3 base case: a reconciled bridge from GMV to EBITDA\n"
                 "COGS consumes 84% of GMV; what is left must absorb fulfilment, "
                 "marketing and the network", pad=14)
    # Each label is rounded independently, so a reader adding the displayed steps can
    # land 0.1 crore away from a displayed subtotal. Standard practice is to say so
    # rather than to leave an exhibit that appears not to add up.
    fig.text(0.01, -0.02, "All figures in Rs crore, rounded to 0.1. Subtotals may differ "
                          "from the sum of displayed steps by up to 0.1.",
             fontsize=7, color="#666666")
    _save(fig, "03_pnl_waterfall.png")


# ---------------------------------------------------------------------------
def chart_scenarios():
    df = pd.read_csv(C.OUT / "case_summary.csv")
    order = ["bear", "base", "bull"]
    df = df.set_index("scenario").loc[order].reset_index()

    fig, axes = plt.subplots(2, 2, figsize=(9.4, 6.2))
    specs = [
        ("y3_gmv_cr", "Year-3 GMV (Rs crore)", "#8FAFC4"),
        ("y3_cm2_per_order_inr", "Year-3 CM2 per order (Rs)", DP),
        ("y3_ebitda_cr", "Year-3 EBITDA (Rs crore)", POS),
        ("peak_cumulative_burn_cr", "Peak cumulative burn (Rs crore)", NEG),
    ]
    for ax, (col, title, colour) in zip(axes.ravel(), specs):
        vals = df[col].values
        bars = ax.bar(df["scenario"].str.capitalize(), vals, color=colour,
                      alpha=0.88, edgecolor="white", width=0.6)
        ax.axhline(0, color="#999999", lw=0.8)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2,
                    v + (abs(vals).max() * 0.04 if v >= 0 else -abs(vals).max() * 0.10),
                    f"{v:,.1f}", ha="center", fontsize=8, color="#333333")
        ax.set_title(title, fontsize=9.5)
        ax.margins(y=0.20)
    fig.suptitle("Year-3 outcome across cases: the bear case is still cash-negative\n"
                 "which is the honest read, not a reason to hide the scenario",
                 fontsize=11, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    _save(fig, "04_scenarios.png")


# ---------------------------------------------------------------------------
def chart_tornado():
    df = pd.read_csv(C.OUT / "sensitivity_tornado.csv")
    df = df.sort_values("swing_inr_cr")
    base = pd.read_csv(C.OUT / "pnl_base.csv")
    base_ebitda = base[base["year"] == 3]["ebitda_cr"].iloc[0]

    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    y = np.arange(len(df))
    low = df["low_inr_cr"].values
    high = df["high_inr_cr"].values
    ax.barh(y, high - low, left=low, height=0.6, color=ACC, alpha=0.75,
            edgecolor="white")
    ax.axvline(base_ebitda, color=HOME, ls="--", lw=1.5,
               label=f"Base case: Rs {base_ebitda:,.0f} Cr")
    ax.axvline(0, color="#999999", lw=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels(df["driver"], fontsize=8)
    ax.set_xlabel("Year-3 EBITDA (Rs crore)")
    ax.set_title("Which assumption do I need to be right about?\n"
                 "Each driver flexed independently by +/-25%")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    _save(fig, "05_tornado.png")


# ---------------------------------------------------------------------------
def chart_benchmarks():
    """Where the modelled cost sits against what real operators disclose."""
    path = C.OUT / "benchmark_validation.csv"
    if not path.exists():
        print("  skip 08: benchmark_validation.csv missing")
        return
    df = pd.read_csv(path).sort_values("cost_per_order_inr")
    colours = []
    for t in df["type"]:
        colours.append(ACC if t == "model" else ("#8FAFC4" if t == "disclosed" else "#C9D4DD"))

    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    bars = ax.barh(df["source"], df["cost_per_order_inr"], color=colours,
                   edgecolor="white", height=0.6)
    for b, (_, r) in zip(bars, df.iterrows()):
        ax.text(b.get_width() + 1.2, b.get_y() + b.get_height() / 2,
                f"Rs {r['cost_per_order_inr']:,.1f}", va="center", fontsize=8,
                color="#333333")
    ax.set_xlim(0, df["cost_per_order_inr"].max() * 1.22)
    ax.set_xlabel("Cost per order (Rs)")
    ax.set_title("Does the model land where real operators land?\n"
                 "Dark bars are this model; light bars are external reference points, "
                 "whether disclosed or analyst-estimated")
    ax.legend(handles=[Patch(color=ACC, label="This model"),
                       Patch(color="#8FAFC4", label="Disclosed by an operator"),
                       Patch(color="#C9D4DD", label="Analyst estimate")],
              frameon=False, fontsize=8, loc="lower right")
    _save(fig, "08_benchmark_validation.png")


# ---------------------------------------------------------------------------
def chart_two_way():
    df = pd.read_csv(C.OUT / "sensitivity_2way.csv")
    dens = df["orders_per_point_per_day"].values
    aov_cols = [c for c in df.columns if c.startswith("aov_")]
    aovs = [float(c.split("_")[1]) for c in aov_cols]
    mat = df[aov_cols].values

    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    vmax = np.nanmax(np.abs(mat))
    im = ax.imshow(mat, cmap="RdYlGn", aspect="auto", vmin=-vmax, vmax=vmax)

    ax.set_xticks(range(len(aovs)))
    ax.set_xticklabels([f"{a:,.0f}" for a in aovs])
    ax.set_yticks(range(len(dens)))
    ax.set_yticklabels([f"{d:.0f}" for d in dens])
    ax.set_xlabel("Average order value (Rs)")
    ax.set_ylabel("Orders per drop point per day")
    ax.set_title("Year-3 CM2 per order: basket size x network density\n"
                 "Green is profitable; the boundary is the operating requirement")
    ax.grid(False)

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            # Avoid the signed zero: a value rounded to zero was printing "-0".
            txt = "0" if abs(v) < 0.5 else f"{v:,.0f}"
            ax.text(j, i, txt, ha="center", va="center", fontsize=7.4,
                    color="white" if abs(v) > vmax * 0.55 else "#333333")

    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label("CM2 per order (Rs)", fontsize=8)
    _save(fig, "06_two_way_heatmap.png")


# ---------------------------------------------------------------------------
def chart_market_funnel():
    df = pd.read_csv(C.OUT / "market_sizing.csv")
    df = df[~df["layer"].str.contains("all-India")]
    vals = df["value_inr_cr"].values
    labels = [l.split(" - ")[-1] for l in df["layer"]]

    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    y = np.arange(len(labels))[::-1]
    colours = ["#12455F", "#1B6CA8", "#4FA3D1", "#8CC0DE", "#D6B98C"]
    ax.barh(y, vals, color=colours[:len(vals)], alpha=0.9, edgecolor="white", height=0.62)
    for i, (v, yy) in enumerate(zip(vals, y)):
        ax.text(v * 1.02, yy, f"Rs {v:,.0f} Cr", va="center", fontsize=8, color="#333333")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xlim(min(vals) * 0.5, max(vals) * 4)
    ax.set_xlabel("Rs crore (log scale)")
    ax.set_title("TAM to SOM: the funnel narrows by roughly three orders of magnitude\n"
                 "Built bottom-up from Tier-2/3+ households, not asserted top-down")
    _save(fig, "07_market_funnel.png")


# ---------------------------------------------------------------------------
def main():
    print("Generating exhibits")
    chart_cost_stack()
    chart_density_curve()
    chart_waterfall()
    chart_scenarios()
    chart_tornado()
    chart_two_way()
    chart_market_funnel()
    chart_benchmarks()
    print("done")


if __name__ == "__main__":
    main()
