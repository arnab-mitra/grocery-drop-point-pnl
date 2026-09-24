# Data sources, and what each one actually measures

Every externally sourced figure used in this case, with its period, its provenance, and the
honest limitation. Figures are labelled by evidence quality:

- **[D]** the operator itself disclosed it (filing, DRHP, earnings call, annual report)
- **[C]** a consultancy or brokerage estimated it
- **[P]** a press report where the ultimate source is not clearly named
- **[A]** this model's own assumption — no public source exists

---

## 1. Market size and structure

| Figure | Value | Period | Type | Source |
|---|---|---|---|---|
| India grocery market | ₹55.9 trillion (~$658 bn) → ₹84.3 trn by 2030 | 2025 → 2030 | [C] Redseer | Businessworld, *Why India's mass grocery economy still belongs to kiranas*, 19 Mar 2026 |
| Kirana / general trade share of grocery | ~91% (CY25), projected ~86% by 2030 | 2025 / 2030 | [C] Redseer | same |
| Kirana outlets | ~13 million (DPIIT uses 1.4 crore) | 2025–26 | [C]/govt | Hindu BusinessLine, 29 Apr 2026; Financial Express / DPIIT, 12 Jun 2026 |
| Q-commerce GMV | ~$11.3 bn (2025) → $60–83 bn (2030) | 2025/2030 | [D] Zepto DRHP | Financial Express, 13 Jun 2026 |
| Q-commerce fulfilment cost | 18–22% of GMV including dark-store rent and last mile | 2026 | [C] Redseer | Businessworld, 19 Mar 2026 |
| Online share of grocery sales | 0.5% | 2022 | [D] Meesho statement | Economic Times, 5 Apr 2022 |
| Consumer spend survey | Average MPCE ₹4,122 rural / ₹6,996 urban; food ≈47% and ≈40% of spend | 2023–24 | [D] MoSPI HCES | Business Today, 27 Dec 2024 |

**The quote that frames the case**, from Redseer's associate partner: *"Quick commerce is
economically incompatible with the mass grocery segment."* [C]

And from BigBasket's founder Hari Menon: *"A ₹350–400 average order value business will never
make money"*, noting BigBasket's own AOV fell from ₹1,200–1,300 on scheduled delivery to ~₹600
in q-commerce. [D] ET Retail, 26 Jun 2026.

## 2. Cost benchmarks — the core validation set

These are the independent reference points the modelled cost is checked against. They are
**not inputs**; they are the reality test.

| Operator | Metric | Value | Period | Type | Source |
|---|---|---|---|---|---|
| **Meesho** | Logistics cost per **placed order** | **₹35 → ₹44 → ₹42** | Q2 FY26 → Q4 FY26 → Q1 FY27 | [D] | Livemint, 23 Sep 2026 |
| **Zepto** | Supply-chain variable cost per order (picking, packing, delivery) | **₹61.24** | Q4 FY26 | [D] DRHP | Financial Express, 16 Jun 2026 |
| **Zepto** | All-in cost per order | ₹185.11 → ₹150.71 → ₹127.79 | FY25 → FY26 → Q4 FY26 | [D] DRHP | same |
| **Blinkit + Instamart** | Fulfilment cost per order | ₹116–118 (floor ~₹98–100 with batching) | Apr–May 2026 | [C] Bernstein | Hindu BusinessLine, 21 May 2026 |
| **Spencer's Jiffy** | Fulfilment cost per order against ~₹110 gross margin on ~₹760 AOV | ₹98–99 | FY26 | [D] | Business Standard, 19 Aug 2026 |
| Warehousing | Grade-A big-box rent, from actual transacted leases | ~₹22–25 /sq ft/month | 2026 | [D] leases | HT Real Estate lease reports |
| Dark-store rent | Inside Tier-1 cities | ₹100–180 /sq ft/month; Chennai/Hyderabad/Pune ₹70–110 | Feb 2026 | [C] ANAROCK | Hindu BusinessLine, 3 Feb 2026 |
| Cold chain | Share of Indian fruit & vegetables passing through a cold chain | **~4%** (vs 80–85% in the US) | 2026 | [C] Equirus | Financial Express, 14 Aug 2026 |
| Shrinkage | Blinkit inventory loss | **1.8% of NOV** | Q1 FY27 | [D] Eternal earnings call | MediaNama, 23 Jul 2026 |
| Payment | UPI P2M ≤ ₹2,000 merchant cost | **zero MDR** from 15 Oct 2026 | 2026 | [D] regulation | Business Standard, 15 Sep 2026 |
| COD failure | Meesho COD success rate 77.7%; COD = 76% of orders | — | FY25 | [D] RHP | Livemint, 23 Oct 2025 |
| Returns | Industry return rate | 15–16% of all e-commerce orders | 2025 | [C] Forrester | Livemint, 23 Oct 2025 |

### 2.1 The claim this analysis refuses to use

It is widely repeated that pickup points are **"30–50% cheaper than home delivery."** That
figure could not be traced to any operator disclosure, consultancy report or academic source.
It appears to be folklore.

The defensible position is: node-based fulfilment avoids the marginal rider trip entirely,
and the documented floors for a *delivered* order in India are Meesho's ₹42 (value e-commerce,
national scale) and ₹61–100 (q-commerce). A batched drop to a fixed node should therefore be
modelled **bottom-up**, which is what this project does — and it reports whatever advantage
falls out rather than assuming the folklore number.

The only citable nearby evidence:

| Example | What is disclosed | Type | Source |
|---|---|---|---|
| **VilCart** — the closest Indian analogue | 100,000+ kirana stores across 30,000 villages used as "aggregation and last-mile nodes, compressing delivery costs that have historically made rural commerce unviable at scale". Revenue ₹1,173 cr FY26; EBITDA margin −6.8% FY25 → ~−4.5% FY26 | [D] | Hindu BusinessLine, 29 Apr 2026 |
| **JioMart** | 800+ dark stores plus ~1,200 existing retail stores as fulfilment points across 1,000 cities; 5,500 pin codes | [D] | Financial Express, 25 Jan 2026 |
| **Vishal Mega Mart** | Fulfils q-commerce from 767 of 819 stores across 520 cities (423 in Tier-3); ~₹800 AOV | [D] | Business Standard, 19 Aug 2026 |
| **DMart Ready** | Ran both home delivery and order-and-pick-up; in FY26 "further rationalised delivery channels with renewed focus on home delivery as the preferred channel", right-sizing from 25 cities to 11 | [D] | Livemint, 6 May 2026; Fortune India, 21 Aug 2026 |
| Academic baseline | Morganti, Dablanc, Fortin & Gouvernal (2014), *Final Deliveries for Online Shopping: The Deployment of Pickup Point Networks in Urban and Suburban Areas*, Research in Transportation Business & Management | Academic | DOI 10.1016/j.rtbm.2014.03.002 (not India-specific) |

**Note the direction of travel in that table.** JioMart and Vishal are converting existing
retail stores into pickup nodes. DMart Ready, which tried both, moved *toward* home delivery
and shrank its footprint. VilCart, the closest analogue to the model tested here, is running at
−4.5% EBITDA. None of this is encouraging, and a case that ignored it would be dishonest.

## 3. Competitive benchmarks

| Operator | Latest disclosed scale | AOV | Profitability | Source |
|---|---|---|---|---|
| Blinkit | 2,443 dark stores (Jun 2026); 77 m MAU | ₹518 net | Turned operating-profitable Q3 FY26; adj EBITDA +₹102 Cr in Q1 FY27 | [D] Eternal earnings |
| Zepto | 1,139 dark stores (Mar 2026) | not disclosed (omitted from DRHP) | Not profitable; adj EBITDA −₹59.40/order Q4 FY26 | [D] DRHP |
| Swiggy Instamart | 1,171 dark stores across 131 cities (Jun 2026) | ₹687 | Contribution-margin breakeven May 2026; +0.2% of GOV Q1 FY27 | [D] Swiggy Q1 FY27 |
| Flipkart Minutes | 1,000+ dark stores across 120–130 cities (Sep 2026) | ₹500–530 ex-mobile | — | [C] UBS note |
| DMart (Avenue Supermarts) | 500 stores; foods = 57.9% of mix | — | FY26 revenue ₹68,821 Cr, PAT ₹2,964 Cr | [D] results |
| **DMart Ready** | **11 core cities, down from 25** | — | **FY26 revenue ₹4,094 Cr, net loss ₹307 Cr** | [D] results |

**DMart Ready is the most important benchmark in this table.** A formidable operator with the
cheapest grocery sourcing in Indian retail, an owned store network to fulfil from, and
scheduled delivery instead of a speed promise, still lost ₹307 crore on ₹4,094 crore of online
revenue and *shrank* its city footprint, citing orders that were too thin. Any Tier-3 online
grocery case has to be read against that.

**On take rates:** no Indian online grocery operator publishes a clean take rate. The closest
proxies are Zepto's advertising revenue at 7.9% of net receivable value [D], and Spencer's
Jiffy at ~14.5% gross margin against ~13% fulfilment cost [I] from the disclosed figures
above.

## 4. Meesho's own grocery history

Included because it is the most directly relevant evidence available, and because it is a
record of difficulty rather than of success.

| Date | Event |
|---|---|
| Apr 2022 | Farmiso rebranded **Meesho Superstore**; 150+ grocery roles cut |
| **Aug 2022** | **Superstore shut in >90% of cities**, retained Nagpur and Mysuru; ~300 jobs lost. Reason cited: low revenue and high cash burn |
| Jan 2024 | Signals re-entry — grocery in "one or two cities from April" |
| Apr 2026 | Superstore grocery business **shuttered** |
| **Jun 2026** | **Acquires Kirana Club for ₹202 crore** — 4.1 m registered kirana retailers, asset-light B2B, operating independently |
| Aug 2026 | CEO describes grocery as *"still at an experimental stage"*, with a **new low-cost logistics arm separate from Valmo** built for grocery, perishables and FMCG |
| Q1 FY27 | Financial services and the new logistics arm together posted a **₹39 crore loss** |

Sources: ET / Inc42 (2022), ET (Jan 2024), Indian Retailer (Apr 2026), Business Standard and
VCCircle (Jun 2026), ETtech explainer (Aug 2026), Livemint (Sep 2026).

**Important caution:** Meesho's ₹42 cost per placed order is the **Valmo-era marketplace**
figure. It is *not* the grocery arm's cost, and using it as such would be an error. The grocery
logistics arm has no disclosed cost per order at all.

## 5. Assumptions with no public source

These are the modeller's own estimates. Where a figure does not exist publicly, the honest
move is to state the assumption, state the basis, and show how much the answer depends on it.

| Assumption | Value | Basis | Sensitivity |
|---|---|---|---|
| **Vehicle run cost** | ₹210 | Rider, fuel and vehicle for one dedicated run | Small. ±25% moves Y3 EBITDA by ₹9.3 Cr |
| **Orders per vehicle run** | 45 | One point per run at maturity | Small. ₹9.8 Cr |
| **Gross margin on goods** | 14.2% → 15.8% | Informed by the structure of Indian grocery retail; DMart and staples-heavy formats run thin | **Largest in the model: ₹170.5 Cr.** Sourcing this properly is the top priority |
| **AOV** | ₹480 → ₹560 | Between q-commerce convenience (~₹518) and scheduled grocery (₹1,200–1,300). Justified because pickup serves planned bulk shopping | **Second largest: ₹139.2 Cr.** Reported small-town AOVs run 25–30% below metro, which would break the case |
| **Drop-point fixed cost** | ₹18,000/month | Operator retainer, signage, space | ₹23.7 Cr |
| **Warehouse fixed cost** | ₹9 Cr → ₹62 Cr/month | Not benchmarked | ₹37.2 Cr |
| **Tech and people** | ₹22 Cr → ₹58 Cr/month | Not benchmarked | ₹34.8 Cr |
| Marketing | 7.5% → 3.8% of GMV | Inference | ₹41.0 Cr |
| Payment cost per order | ₹4.50 | UPI below ₹2,000 carries zero MDR, so this is cash handling and reconciliation on COD baskets | Minor |
| Packaging cost per order | ₹7.50 | No operator publishes this | Minor |
| Shrinkage | 1.1% of GMV | Non-perishables only. Blinkit's 1.8% of NOV is the upper anchor and is q-commerce with faster-turning, fresher stock | ₹11.9 Cr |
| Drop-point handling fee | ₹12/order | Paid to the point operator | ₹23.9 Cr |

**The honest summary:** the model's two largest drivers — gross margin and AOV — are both
assumptions. That is disclosed in §9 of the case study and it is the first thing an interviewer
should be told.
