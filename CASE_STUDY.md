# Can a drop-point model make grocery work in Tier-3 India?

**A cost model, a three-year P&L and a sensitivity analysis for a low-cost grocery launch on
a value marketplace.**

Arnab Mitra · September 2026

---

## 1. The question

Quick commerce proved Indians will buy groceries online. It did not prove they will buy them
profitably: q-commerce fulfilment costs 18–22% of GMV, which makes a ₹150 basket structurally
unviable, and one large operator's own founder has said a ₹400 basket "will never make
money". Separately, even operators with the cheapest sourcing in Indian retail have been
losing money on online grocery and shrinking their footprint rather than expanding it.

So the question is not whether grocery can be sold online. It is:

> **Can a value marketplace build a grocery supply chain in Tier-3 India that is
> structurally cheaper to serve than home delivery — and if it can, does the P&L actually
> work?**

The premise being tested is the **drop-point model**: instead of delivering to a doorstep,
batch orders into a single vehicle run to a neighbourhood pickup point and have the customer
collect.

## 2. Headline answer

**The drop-point model works as a cost innovation, and it is not enough.**

1. **The cost saving is real and large.** Cost per order falls from **₹97.10 to ₹67.85 — a
   30.1% reduction**, entirely from the last mile, which falls 63%. Every upstream stage is
   held identical between the two models so the measured advantage is attributable to the
   drop point alone and nothing else.
2. **It comes from two distinct mechanisms**, not one — and keeping them separate matters:
   *batching* (one run serves many orders) and *pay-on-collection* (a no-show at a pickup
   point is a stock event, not a wasted trip).
3. **But the base case still does not clear.** Year-3 contribution after the network is
   **−₹1.90 per order** and EBITDA is **−₹151 crore**, or −7.0% of GMV. The modelled plan
   needs 56.7 orders per drop point per day to break even and assumes 48. It is 15% short.
4. **And the drop-point mechanics are the smallest levers in the model.** Flexing orders-per-run
   and vehicle-run cost moves Year-3 EBITDA by ₹10 crore and ₹9 crore. Flexing **gross margin
   moves it by ₹171 crore** and **AOV by ₹139 crore.** The delivery innovation is real; it is
   simply not the binding constraint.

That last point is the most useful thing in this analysis, and it is not what I expected to
find. See §7.

## 3. The cost model

### 3.1 What is held constant, and why

The two models differ **only in the last mile**. First mile, sortation, line haul, payment,
packaging and shrinkage are identical line items. That is deliberate: it means the measured
advantage cannot be an artefact of a convenient assumption smuggled in elsewhere. If you want
to attack this result, you must attack the last mile — which is where the argument should
live.

| Stage | Home delivery | Drop point | Delta |
|---|---|---|---|
| First mile (seller to FC) | ₹9.00 | ₹9.00 | — |
| Sortation | ₹6.50 | ₹6.50 | — |
| Line haul (FC to city) | ₹17.00 | ₹17.00 | — |
| Payment | ₹4.50 | ₹4.50 | — |
| Packaging | ₹7.50 | ₹7.50 | — |
| Shrinkage | ₹6.16 | ₹6.16 | — |
| **Last mile** | **₹46.44** | **₹17.19** | **−63.0%** |
| **Total cost per order** | **₹97.10** | **₹67.85** | **−30.1%** |

### 3.2 The two mechanisms

**Batching.** A single vehicle run costing ₹210 serves 45 orders at one location, so the
per-order cost of that leg is ₹4.67. Add the ₹12 handling fee paid to the point operator and
the base is ₹16.67. This is the obvious mechanism and it is what most people mean by "pickup
points are cheaper".

**Pay-on-collection.** This is the mechanism that is easy to miss and materially larger.
Under home delivery, a refused COD parcel costs a full forward *and* return leg and earns
nothing — the multiplier is 1.85× the last-mile cost. At a pickup point, the customer pays on
collection, so a no-show is a **stock event rather than a wasted trip**: the goods are
non-perishable, they go back on the shelf, and nothing extra is driven because the node is
already on the next scheduled run. The multiplier is 0.35×.

That difference is why the home-delivery last mile costs ₹46.44 against a base of ₹38, while
the drop-point last mile costs ₹17.19 against a base of ₹16.67. **Failed deliveries, not
delivery distance, are where home delivery loses.**

This is anchored on disclosed evidence rather than asserted: Meesho's cash-on-delivery
success rate is 77.7% and COD is 76% of its orders, implying roughly 17% of all orders fail
on the COD leg alone.

### 3.3 The model is a density business, not a delivery business

Cost per order falls steeply with consolidation and then flattens:

| Orders per vehicle run | Drop-point cost per order | Advantage vs home |
|---|---|---|
| 5 | ₹106.76 | **−₹9.26 (worse)** |
| 10 | ₹84.70 | +₹12.40 |
| 20 | ₹73.87 | +₹23.23 |
| 45 (planned) | ₹67.85 | +₹29.24 |
| 90 | ₹65.44 | +₹31.65 |

**Breakeven density is 6.4 orders per run.** Below that the drop-point model is *worse* than
home delivery, because you are paying for a vehicle run and filling it with nothing. The
planned density of 45 has 7.1× headroom over that — so the operational risk here is not
marginal, it is binary. Either the network aggregates orders or it destroys value.

## 4. But does the model land where real operators land?

An internally consistent model can still be externally wrong. So the modelled cost is checked
against what actual Indian operators disclose:

| Source | Cost per order | Type |
|---|---|---|
| Meesho — value e-commerce, delivered | **₹42.0** | disclosed, Q1 FY27 |
| Zepto — q-commerce, supply-chain variable | **₹61.2** | disclosed, Q4 FY26 |
| **This model — drop point** | **₹67.85** | modelled |
| **This model — home delivery** | **₹97.10** | modelled |
| Spencer's Jiffy — store-led delivery | ₹98.5 | disclosed, FY26 |
| Bernstein — q-commerce fulfilment floor | ₹99.0 | analyst estimate |

Read this carefully, because it cuts both ways.

**The home-delivery figure validates well.** ₹97.10 sits almost exactly on Spencer's disclosed
₹98.5 and Bernstein's ₹99 floor for a delivered order with a real basket. The cost stack is
not obviously understated.

**The drop-point figure needs one caveat.** ₹67.85 is *above* Meesho's ₹42 per placed order —
so the drop-point model is more expensive per order than the core business already is. That
is not a contradiction: Meesho's ₹42 is for a ₹155 apparel parcel, while this is a ₹560
grocery basket that is heavier, bulkier, and carries first-mile, sortation and line-haul costs
that scale with volume, not order count. As a **share of GMV** the comparison inverts: ₹67.85
on a ₹560 basket is 12.1% of GMV, against ₹42 on ₹155, which is 27.1%. Per order this is
expensive; per rupee of GMV it is far cheaper. Both framings are true and you should be able
to give both.

**One claim this analysis deliberately does not use.** It is widely repeated that pickup
points are "30–50% cheaper than home delivery". That figure could not be traced to any
operator disclosure, consultancy report or academic source. Rather than adopt it, this model
builds the drop-point cost bottom-up and reports whatever falls out. It happens to land at
**30.1%** — the bottom of the folklore range — which is a mildly reassuring coincidence and
nothing more.

## 5. Market sizing, and the gap in it

| Layer | Value | Basis |
|---|---|---|
| TAM — all-India household grocery | ₹36.8 lakh Cr ($443 bn) | households × monthly spend × 12 |
| TAM — Tier-2/3+ only | ₹26.5 lakh Cr ($319 bn) | 72% of households |
| Packaged staples and non-perishable FMCG | ₹14.6 lakh Cr ($176 bn) | excludes fresh, deliberately |
| **SAM — online-addressable** | **₹3.21 lakh Cr ($38.6 bn)** | 22% of staples |
| **SOM — a new entrant's 3-year share** | **₹2,564 Cr ($0.3 bn)** | 0.8% of SAM |

Fresh is excluded on purpose: it needs cold chain, carries high shrinkage, and is precisely
where q-commerce already wins on speed. A drop-point model competes on the cost of
non-perishables, so that is the addressable market.

**The triangulation is worth stating rather than hiding.** The bottom-up all-India figure
comes to $443 bn, against a published "India food and grocery" market of $658 bn — a 48% gap.
The published figure is a broader basket that typically includes eating out, which this model
excludes. The bottom-up number is used for the rest of the case because it is built from a
Tier-2/3 household base that matches the strategic question. But the gap is real and the
right response is to name the definitional difference, not to pick the flattering number.

## 6. The P&L, and why the base case does not clear

GMV is not assumed. It falls out of the network — drop points × orders per point per day ×
365 — because the whole investment case is a bet on density. Costs then build in the order a
P&L is read.

**Base case:**

| Year | Drop points | Orders (mn) | GMV (₹ Cr) | Gross margin | Ad revenue | CM1/order | CM2/order | EBITDA (₹ Cr) |
|---|---|---|---|---|---|---|---|---|
| 1 | 120 | 0.96 | 46.3 | ₹6.6 Cr | ₹0.5 Cr | −₹30.13 | −₹57.03 | −42.7 |
| 2 | 650 | 8.07 | 419.5 | ₹63.3 Cr | ₹6.7 Cr | −₹9.29 | −₹26.70 | −100.7 |
| 3 | 2,200 | 38.54 | 2,158.5 | ₹341.0 Cr | ₹43.2 Cr | **+₹10.43** | **−₹1.90** | **−151.3** |

**Three cases, Year 3:**

| Scenario | GMV (₹ Cr) | CM1/order | CM2/order | EBITDA (₹ Cr) | EBITDA % of GMV | Peak cumulative burn |
|---|---|---|---|---|---|---|
| Bull | 2,974.4 | +₹27.56 | +₹18.83 | −49.6 | −1.7% | ₹176.5 Cr |
| **Base** | **2,158.5** | **+₹10.43** | **−₹1.90** | **−151.3** | **−7.0%** | **₹294.7 Cr** |
| Bear | 1,365.0 | −₹6.96 | −₹26.90 | −214.5 | −15.7% | ₹366.1 Cr |

Read the base case honestly: **Variable contribution turns positive in Year 3 (+₹10.43 per
order), and the drop-point network fixed cost takes it back below zero (−₹1.90), and the
warehouse, tech and people base pushes EBITDA to −₹151 crore.** The business is within ₹2 per
order of covering its network, and ₹151 crore away from covering its overhead.

This is not a model failure. It is what thin-margin grocery looks like, and it is consistent
with the observable record: operators with far more scale than a new entrant are still
loss-making on online grocery, and one of them retreated from 25 cities to 11 after
concluding that its tail markets lacked order density.

**Two things the base case needs, and neither is a delivery innovation:**

- **Gross margin.** Modelled at 15.8% of GMV in Year 3. Reaching the low-20s — via private
  label and a richer non-staples mix — is what changes the answer.
- **Scale.** The fixed base (warehouse, tech, people) is ₹1,466 crore per year in Year 3
  against ₹2,159 crore of GMV. It is 68% of GMV. That ratio only falls with volume.

## 7. What actually moves the answer

Every driver flexed independently by ±25%, measured on Year-3 EBITDA (base −₹151.3 Cr):

| Rank | Driver | Swing |
|---|---|---|
| 1 | **Gross margin % of GMV** | **₹170.5 Cr** |
| 2 | **Average order value** | **₹139.2 Cr** |
| 3 | Marketing % of GMV | ₹41.0 Cr |
| 4 | Warehouse fixed cost | ₹37.2 Cr |
| 5 | Tech and people cost | ₹34.8 Cr |
| 6 | Drop-point handling fee | ₹23.9 Cr |
| 7 | Drop-point fixed cost | ₹23.7 Cr |
| 8 | Ad revenue % of GMV | ₹21.6 Cr |
| 9 | Orders per drop point per day | ₹20.3 Cr |
| 10 | Shrinkage | ₹11.9 Cr |
| 11 | **Orders per vehicle run** | **₹9.8 Cr** |
| 12 | **Vehicle run cost** | **₹9.3 Cr** |
| 13 | Refusal rate at drop point | ₹1.0 Cr |

**The premise of the case ranks eleventh and twelfth.** Gross margin and basket size are an
order of magnitude more important than the last-mile mechanics the model was built to test.

The correct reading is not that the drop-point model is irrelevant — it delivers a genuine 30%
cost reduction and it is what makes a Tier-3 grocery business *conceivable at all*. It is that
**cost innovation is necessary and not sufficient**, and that anyone who fixes only the
delivery leg and stops there will still lose money. A second, equally useful reading: at
₹560 of AOV the model is thin; the two-way grid shows contribution turning positive at
roughly ₹620 AOV and 35 orders/point/day, or ₹580 AOV and 50 orders.

## 8. Kill criteria

Stated in advance, so the answer is not renegotiated after the fact.

1. **Orders per drop point per day below 34 by month 18** (the operational rollout gate) → stop
   opening points. Note the economic breakeven is 57, materially above the operational gate,
   and both numbers are reported for that reason.
2. **Peak cumulative burn above ₹900 crore** → the case is not financeable at this cost base.
   The base case burns ₹295 crore, so there is headroom, but the bear case burns ₹366 crore
   and the fixed base scales with the network.
3. **Gross margin below 15% at the end of Year 2** → the mix is wrong; staples alone will not
   carry the fixed base.
4. **Contribution margin after the network still negative at the end of Year 3** in the base
   case → restructure rather than scale. This is the gate the base case currently fails.
5. **Refusal rate above 12% at pickup points** → customers are not converting intention into
   collection, and the pay-on-collection mechanism that justifies the model is not working.

## 9. Limitations, declared

1. **No public benchmark exists for drop-point economics.** The widely quoted "30–50% cheaper"
   claim could not be sourced. This model builds the cost bottom-up, which is more honest and
   also means the result is only as good as its two key assumptions: ₹210 per vehicle run and
   45 orders per run. Both are inferred, and the case study's conclusion is more sensitive to
   the second than to the first.
2. **Gross margin is the largest driver and the softest input.** At 14.2–15.8% it is an
   assumption informed by the structure of Indian grocery retail, not a disclosed figure.
   Since it is the top of the tornado, it deserves more sourcing than it has.
3. **AOV is the second-largest driver and is also inferred.** ₹480–560 sits between
   q-commerce convenience baskets of roughly ₹518 and scheduled-delivery grocery baskets of
   ₹1,200–1,300. The justification is that a pickup model serves planned, bulk grocery
   shopping rather than impulse convenience, so the scheduled-delivery comparison is the right
   analogue. That is a defensible argument, not a measurement — and in smaller towns reported
   AOVs run 25–30% below metro, which would break the model.
4. **Shrinkage and cold chain.** Fresh is excluded entirely, which avoids the cold-chain
   problem but also concedes the highest-frequency part of the grocery basket.
5. **Fixed costs are the model's least examined area.** Warehouse, tech and people are
   year-keyed assumptions that were not benchmarked against anything, and they are the third,
   fourth and fifth largest drivers.
6. **Single-year granularity.** Months-to-contribution-positive is reported as an annual
   proxy, not a monthly cash curve.
7. **This is not a Meesho forecast.** It is an independent model using public disclosures.
   Meesho's own grocery history is relevant context — a full retreat in 2022, a re-entry, a
   wind-down, and a pivot toward B2B kirana retail via a 2026 acquisition — and a reader
   should treat that record as evidence about how hard this is.

## 10. What I would do next

1. **Test the two levers that matter.** A pilot measuring real basket size and real gross
   margin mix in three Tier-3 towns would move this analysis more than any further modelling.
2. **Benchmark the fixed base.** Warehouse, tech and people cost are ₹1,466 crore a year in
   Year 3 and were assumed rather than sourced. They are collectively a ₹72 crore swing.
3. **Model private label explicitly** as a gross-margin lever rather than leaving margin as a
   single blended number.
4. **Add a monthly cash curve** for the financeable question, rather than annual EBITDA.
5. **Test the small-town AOV discount.** If Tier-3 baskets really run 25–30% below metro, the
   case needs a different basket strategy, not a better delivery model.

## 11. Reproducing this

```bash
pip install -r requirements.txt
python src/run_all.py
```

Every assumption is in `src/config.py`, and the P&L mechanics are shared from `src/lib.py` so
the cost model and the P&L cannot drift apart. Change one driver and re-run — the bull and
bear cases are defined as multipliers on named drivers, so they cannot silently diverge in
structure from the base case.

**Charts:** `outputs/charts/` · **Data:** `outputs/pnl_*.csv`,
`outputs/cost_comparison.csv`, `outputs/sensitivity_*.csv` · **Sources:**
`data/SOURCES.md`
