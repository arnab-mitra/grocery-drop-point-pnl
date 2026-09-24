# Interview notes — how to defend this project

A project you cannot defend is worse than no project. Read the case study, then be able to
answer everything below without looking at it.

---

## 1. The 60-second version

> "I modelled whether a drop-point grocery model — batching orders to a neighbourhood pickup
> point instead of delivering to doorsteps — could make grocery work in Tier-3 India. The cost
> case is real: cost per order falls about 30%, almost entirely from the last mile, and it
> comes from two things, batching and pay-on-collection. But when I built the P&L, the base
> case still lands about two rupees per order short of covering its network, and the driver
> tornado said the interesting thing: gross margin and basket size move EBITDA by ₹170 crore
> and ₹139 crore, while the drop-point mechanics I set out to test move it by about ₹10 crore.
> So the cost innovation is necessary and not sufficient, and the real constraint is margin
> and basket size, not delivery."

Lead with the negative finding. It signals that you can read your own model critically.

## 2. The questions you will get

### "How do you know your cost model is right?"

Two ways. First, the two models differ **only in the last mile** — everything upstream is an
identical line item — so the advantage cannot be an artefact of an assumption hidden
elsewhere. Second, I validated the output against disclosed figures: my home-delivery cost of
₹97.10 lands almost exactly on Spencer's disclosed ₹98.5 per order and Bernstein's ₹99
q-commerce floor. If my cost stack were badly understated, it would not land there.

### "Why is the drop-point cost more than Meesho's ₹42 per order?"

Because they are not the same parcel. Meesho's ₹42 is a ₹155 apparel order. This is a ₹560
grocery basket — heavier, bulkier, and carrying first-mile, sortation and line-haul costs that
scale with volume rather than order count. As a **share of GMV** the comparison flips: ₹67.85
on ₹560 is 12.1% of GMV, versus ₹42 on ₹155, which is 27.1%. Per order this is more expensive;
per rupee of GMV it is much cheaper.

### "What is pay-on-collection and why does it matter more than batching?"

Under home delivery a refused COD parcel costs a full forward and return leg and earns
nothing — I model that as 1.85× the last-mile cost. At a pickup point the customer pays on
collection, so a no-show is a **stock event, not a wasted trip**: the goods are non-perishable,
they go back on the shelf, and nothing extra is driven because the node is already on the next
scheduled run. So the multiplier is 0.35×. That is why home delivery's last mile costs ₹46.44
against a base of ₹38, while the drop-point last mile costs ₹17.19 against a base of ₹16.67.
**Failed deliveries, not delivery distance, are where home delivery loses.**

The rate is anchored on disclosed evidence, not invented: Meesho's COD success rate is 77.7%
and COD is 76% of its orders, implying roughly 17% of orders fail on the COD leg alone.

### "So does the business work or not?"

The base case does not clear, and I say so in the headline. Year-3 contribution after the
network is −₹1.90 per order and EBITDA is −₹151 crore, or −7% of GMV. The bull case works
(+₹18.83 per order, −1.7% EBITDA) and the bear case is clearly bad (−₹26.90, −15.7%). The
honest read is that the model is within about two rupees per order of covering its network and
a long way from covering its overhead, and getting there needs margin and scale, not a better
delivery model.

### "Then why build the model at all?"

Because it tells you what to fix. If I had assumed the drop-point saving made the business
work, I would have recommended scaling a loss-making network. The modelling output is a ranked
list of what actually moves the answer: gross margin, then basket size, then marketing and the
fixed base — with the delivery mechanics near the bottom.

### "Isn't the '30-50% cheaper pickup point' figure well known?"

It is widely repeated and I could not source it anywhere — not in an operator filing, not in a
consultancy report, not in the academic literature I could reach. So I did not use it. I built
the drop-point cost bottom-up and reported what fell out, which was 30.1%. That happens to sit
at the bottom of the folklore range and I would not read anything into the coincidence.

### "What is the weakest part of this analysis?"

The two largest drivers are assumptions. Gross margin at 14–16% and AOV at ₹480–560 are both
informed estimates, not disclosed figures, and between them they swing Year-3 EBITDA by ₹310
crore. If Tier-3 baskets really run 25–30% below metro — which is reported — the case needs a
different basket strategy, not a better delivery model. The fixed cost base was also never
benchmarked, and it is the third, fourth and fifth largest driver.

### "What does the industry evidence say?"

Mostly that this is hard, and I have included it rather than filtered it. DMart Ready — a
formidable operator with the cheapest sourcing in Indian retail and an owned store network to
fulfil from — lost ₹307 crore on ₹4,094 crore of online revenue and shrank from 25 cities to
11, citing orders that were too thin. VilCart, the closest analogue to a drop-point model,
runs at about −4.5% EBITDA. DMart Ready, which tried both home delivery and pickup, moved
*toward* home delivery. Meesho itself has entered, retreated from, re-entered and exited
consumer grocery, and now describes it as "still experimental". Ignoring that record would
have made the analysis worthless.

## 3. Hostile questions

**"Your base case fails. Isn't the answer just no?"**
No — the answer is "not at this cost base and basket." The model identifies precisely what
would have to be true: gross margin into the low 20s, or AOV around ₹620 at 35 orders per
point per day, or both. That is a much more actionable conclusion than a binary.

**"You assumed your own answer by picking assumptions that make the drop-point model look good."**
The opposite risk is larger, and I've disclosed both. I set the refusal-cost multiplier for
pickup points at 0.35× against 1.85× for home delivery, which is a strong assumption in the
model's favour — and I documented the mechanism behind it so it can be challenged. On the
other side, I refused the unsourced 30–50% claim, held every upstream cost identical between
the models, and validated against real operator disclosures. And the headline conclusion is
negative, which is not what an answer-motivated model produces.

**"Why is breakeven density 57 when your operational gate is 34?"**
Because they answer different questions. 34 is an operational floor for opening a point; 57 is
the economic threshold where contribution after the network turns positive. I report both and
flag the gap, because a gate that is quietly set below the economic threshold is how a rollout
scales into a loss.

**"Grocery is a low-margin business. Did you really need a model to discover that?"**
No. The model is not there to discover that margins are thin — it is there to quantify *how*
thin relative to the cost of serving, to show that a 30% cost reduction still is not enough,
and to rank the remaining levers. The counter-intuitive part is that the delivery innovation
ranks eleventh of thirteen.

**"You excluded fresh. Isn't that most of grocery?"**
It is the highest-frequency part of the basket and I excluded it deliberately: fresh needs
cold chain that only ~4% of Indian fruit and vegetables currently pass through, and it is
exactly where quick commerce wins on speed. A drop-point model competes on the cost of
non-perishables, so that is the honest addressable market. The cost of excluding it is that I
have conceded frequency to the incumbents.

## 4. What you must NOT claim

- Do not say "this saves 30–50%." Say "I could not source that figure, so I built it bottom-up
  and got 30.1%."
- Do not say "the business works." Say "the base case does not clear, and here is exactly what
  would have to be true."
- Do not present gross margin or AOV as sourced. Say "these are the two biggest drivers and
  both are assumptions."
- Do not claim Meesho is building this or would endorse it. Meesho's actual grocery route is
  B2B kirana via an acquisition, plus an experimental low-cost logistics arm — and its ₹42
  cost per order is a *marketplace* figure, not the grocery arm's cost.
- Do not present the drop-point cost as a benchmark. No public benchmark exists; it is my
  bottom-up model.

## 5. If you get asked to improve it live

Lead with the ranking, not the list:

1. **Validate gross margin and basket size with a three-town pilot.** They are the top two
   drivers and together a ₹310 crore swing. More modelling adds nothing here.
2. **Benchmark the fixed cost base.** Warehouse, tech and people are ₹1,466 crore a year in
   Year 3 and were assumed, not sourced.
3. **Model private label explicitly** as a margin lever rather than leaving margin as one
   blended number.
4. **Add a monthly cash curve** to answer the financeability question properly, instead of
   annual EBITDA.
5. **Test the small-town AOV discount** before scaling, because if Tier-3 baskets are 25–30%
   below metro the whole basket strategy changes.
