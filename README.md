# Low-Cost Grocery Launch in Tier-3 India — Drop-Point Model

**Can a value marketplace build a grocery supply chain in Tier-3 India that is structurally
cheaper to serve than home delivery — and if it can, does the P&L work?**

A bottom-up cost model, a three-year P&L with base/bull/bear cases, and a sensitivity
analysis that identifies what actually decides the answer.

---

## The answer in five lines

1. **The drop-point model works as a cost innovation.** Cost per order falls from **₹97.10 to
   ₹67.85 — 30.1%**, entirely from the last mile, which falls 63%.
2. It works through **two mechanisms**: batching (one run serves many orders) and
   pay-on-collection (a no-show at a pickup point is a stock event, not a wasted trip). The
   second is larger and easier to miss.
3. **But it is not enough.** Base-case Year-3 contribution after the network is **−₹1.90 per
   order** and EBITDA is **−₹151 crore** (−7.0% of GMV). The plan needs 56.7 orders per drop
   point per day to break even and assumes 48.
4. **The drop-point mechanics are the smallest levers in the model.** Flexing orders-per-run
   moves Year-3 EBITDA by ₹10 crore. Flexing **gross margin moves it by ₹170 crore** and **AOV
   by ₹139 crore**.
5. So the finding is: **cost innovation is necessary and not sufficient.** Fixing only the
   delivery leg and stopping there still loses money.

## Why the cost model is credible

The two models differ **only in the last mile** — first mile, sortation, line haul, payment,
packaging and shrinkage are identical line items in both. The measured advantage therefore
cannot come from an assumption smuggled in elsewhere.

And the result is checked against what real Indian operators disclose:

| Source | Cost per order |
|---|---|
| Meesho (value e-commerce, delivered) | ₹42.0 |
| Zepto (q-commerce, supply-chain variable) | ₹61.2 |
| **This model — drop point** | **₹67.85** |
| **This model — home delivery** | **₹97.10** |
| Spencer's Jiffy (store-led delivery) | ₹98.5 |
| Bernstein (q-commerce floor) | ₹99.0 |

The home-delivery figure lands almost exactly on Spencer's disclosed ₹98.5 and Bernstein's ₹99
floor. The drop-point figure sits above Meesho's ₹42 — because Meesho's ₹42 is a ₹155 apparel
parcel while this is a ₹560 grocery basket. Per order this is expensive; as a share of GMV
(12.1% versus 27.1%) it is far cheaper. Both framings are in the case study.

## One claim deliberately not used

It is widely repeated that pickup points are **"30–50% cheaper than home delivery."** That
figure could not be traced to any operator, consultancy or academic source. This model builds
the drop-point cost bottom-up instead and reports what falls out — which happens to be 30.1%,
the bottom of the folklore range, and nothing more should be read into that.

## Repository structure

```
├── CASE_STUDY.md            ← start here: the full written analysis
├── INTERVIEW_NOTES.md       ← the questions this will attract, and the answers
├── requirements.txt
├── data/
│   └── SOURCES.md           every external figure, its provenance, and the claims refused
├── src/
│   ├── config.py            ALL assumptions, in one place, with sources marked
│   ├── lib.py               shared cost and P&L logic — one definition, used by both
│   ├── 01_market_sizing.py  TAM/SAM/SOM bottom-up, with top-down triangulation
│   ├── 02_cost_model.py     cost unbundling, density curve, breakeven, benchmark validation
│   ├── 03_pnl_model.py      three-year P&L, base / bull / bear, decision gates
│   ├── 04_sensitivity.py    tornado, two-way grid, breakeven density
│   ├── 05_charts.py         exhibits
│   └── run_all.py           reproduce everything in one command
└── outputs/
    ├── *.csv                P&L by scenario, cost comparison, sensitivity tables
    └── charts/*.png         exhibits
```

## Run it

```bash
pip install -r requirements.txt
python src/run_all.py
```

Runs offline. Every assumption is in `src/config.py`; bull and bear are defined as
**multipliers on named drivers**, so they cannot silently diverge in structure from the base
case. The P&L imports its cost logic from `src/lib.py`, so the cost model and the P&L can
never drift apart.

## The P&L, Year 3

| Scenario | GMV (₹ Cr) | CM1/order | CM2/order | EBITDA (₹ Cr) | EBITDA % of GMV |
|---|---|---|---|---|---|
| Bull | 2,974.4 | +₹27.56 | +₹18.83 | −49.6 | −1.7% |
| **Base** | **2,158.5** | **+₹10.43** | **−₹1.90** | **−151.3** | **−7.0%** |
| Bear | 1,365.0 | −₹6.96 | −₹26.90 | −214.5 | −15.7% |

Variable contribution turns positive in Year 3; the drop-point network takes it back below
zero; warehouse, tech and people push EBITDA to −₹151 crore. The business is within ₹2 per
order of covering its network and ₹151 crore away from covering its overhead.

## What this analysis does *not* do

- **Gross margin and AOV are the two largest drivers and both are assumptions.** They are
  disclosed as such, and sourcing them properly is the top priority before this model is used
  for a decision.
- **Fixed costs (warehouse, tech, people) were never benchmarked.** They are the third, fourth
  and fifth largest drivers.
- **No public benchmark exists for drop-point economics.** The result is only as good as its
  ₹210-per-run and 45-orders-per-run assumptions.
- **Official annual figures are used as the proxy for months-to-contribution-positive.**
- **This is not a company forecast.** It is an independent model using public disclosures.

## Charts

`outputs/charts/` — cost stack by supply-chain stage, the density curve with its breakeven
point, the Year-3 P&L waterfall, scenario comparison, the driver tornado, the AOV × density
heatmap, the TAM-to-SOM funnel, and the benchmark validation against real operators.
