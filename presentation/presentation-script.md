# Defense Presentation Script
### Spatial Estimation of Air Quality at Unmonitored Locations Using Machine Learning
29 slides · ~20 minutes at a natural pace · Abdalazeez Asaad

---

## How to present this

**Structure.** The deck has five movements: the problem and gap (slides 1–6), methodology (7–15), RQ1–RQ3 results in order (16–24), limitations and closing (25–29). Examiners are listening for whether you can narrate *why* each methodological choice was necessary, not just *what* you did — so on the methodology slides, always land on the reason, not the description.

**Tone.** Several slides exist specifically to show self-critique before an examiner can raise it: slide 18 ("Reading the result straight"), slide 24 ("The honest counterpart"), and slide 26 ("What this doesn't yet resolve"). Deliver these with confidence, not apology — say them like findings, not confessions. That contrast is one of your strongest assets in the room.

**Pacing budget.** ~20 minutes total, leaving 10 minutes for questions in a typical 30-minute slot. If you're running long, the safest slides to compress are 22 (placement map — the caption already says it) and 3 (three approaches — the card titles carry it).

**Opening line (before slide 1 title):** state your name, programme, and the one-sentence version of what you did, before you even click past the title slide. Something like: *"Thank you. I'm going to walk through how I measured the accuracy of estimating air pollution between Sweden's monitoring stations, and used that measurement to recommend where new sensors should go."*

**Closing line (slide 29):** don't just say "thank you, questions" — land the contribution one more time in one breath, then stop talking. Silence is the cue for the chair to open questions.

**A note on slides 21 and 24.** They now cover overlapping ground (both show the NO2 numbers). Slide 21's NO2 row is the quick stat; slide 24 is the fuller narrative beat. When you present, treat slide 21's NO2 mention as a preview ("we'll come back to this") and let slide 24 carry the actual emphasis — don't deliver the same point twice at full weight.

---

## Slide-by-slide script

### 1 — Title
**~20s**
> "Thank you. My thesis asks a simple question with a hard answer: between Sweden's air quality monitoring stations, what's actually happening to the air — and where should the next sensor go? I'll walk through how I measured that, and what it recommends."

*Do: don't linger — this is a runway, not content.*

---

### 2 — Between stations, nobody knows the air
**~45s**
> "SMHI runs Sweden's reference air quality network — accurate, regulatory-grade instruments, but sparse. Stations can be tens of kilometres apart. Everything in between is a blind spot. Cheap IoT sensors could fill that gap, but today they get placed by convenience — wherever's easy to install — not by any measurement of where they'd actually help. This thesis builds that missing decision rule."

*Do: emphasize "convenience, not analysis" — that's the whole motivation in four words.*

---

### 3 — Low concentrations, real health cost
**~40s**
> "This matters even at Sweden's relatively low pollution levels. PM2.5 and NO2 are linked to respiratory and cardiovascular disease, and Stockholm, Gothenburg, and Umeå studies show measurable attributable mortality from traffic exposure. Critically, exposure varies sharply *within* a city — block by block — and a handful of national stations simply can't see that variation."

*Do: pause slightly before "within" — that's the word doing the work.*

---

### 4 — Three ways to estimate the gap
**~40s**
> "Three existing approaches estimate pollution at unmonitored spots. IDW — inverse distance weighting — is the simple, assumption-free baseline. LUR, land-use regression, is Europe's established peer-reviewed standard, calibrated across twenty ESCAPE study areas. And machine learning, which the literature shows often beats LUR on raw accuracy. But — and this is the hinge of the whole methodology section — which one actually wins depends entirely on how rigorously you test it."

*Do: "depends entirely on how you test it" is the bridge into slide 5 — say it, then pause before advancing.*

---

### 5 — Why random testing lies to you
**~50s**
> "Here's the trap. If you randomly split your stations into training and test sets, it looks rigorous — but nearby stations look alike. The model gets a quiet preview of the answer through its geographic neighbors, and your reported accuracy is optimistic in a way that doesn't show up until you deploy it somewhere genuinely new. The fix, following Roberts et al. 2017, is to hide a whole neighborhood around each test station, not just the station itself. This single decision becomes the backbone of the entire validation strategy — everything downstream depends on getting this right."

*Do: this is the most important methodological idea in the talk. Slow down here.*

---

### 6 — Nobody had chained these together
**~40s**
> "So here's the gap in the literature. Plenty of research estimates pollution at unmonitored locations. Plenty of research optimizes sensor placement. But nobody had used a *measured* accuracy-versus-distance relationship, at national scale, on public data, as the actual placement rule. That's the missing link this thesis provides — between 'how good is our estimate' and 'so where do we put the next sensor.'"

---

### 7 — Three questions, one chain
**~35s**
> "That translates into three research questions that chain together. RQ1: how accurately can we estimate PM2.5 and NO2 at a station, using only the other stations? RQ2: how does that accuracy decay with distance, and where's the cutoff? RQ3: using that cutoff, where should new sensors go? Each answer feeds the next."

*Do: trace the arrows with your hand or pointer as you say each RQ — it's a chain, show it as one.*

---

### 8 — Design Science Research
**~40s**
> "Methodologically, this follows Design Science Research. The problem and objectives are the coverage gap, framed into those three RQs. Design and development is the Random Forest model, the accuracy-distance decay curve, and the greedy placement algorithm together. Demonstration is applying it nationally across all of Sweden. And evaluation is judged by real-world coverage gained — not just how well the model scores on paper."

*Do — if pressed on rigor/ethics: this thesis doesn't require ethical review — all data sources are open-data products with no personal information and no human participants, so nothing to add here unless asked (see Q&A prep below).*

---

### 9 — Two pollutants, two models
**~35s**
> "One modelling decision up front: PM2.5 and NO2 are treated as two entirely separate models throughout. NO2 is traffic-sourced, with sharp gradients that fade fast near roads. PM2.5 has mixed regional sources and spreads smoothly over tens of kilometres. Different physics — merging them into one model would blur two real, distinct patterns into a meaningless average."

---

### 10 — 30 features, five groups
**~45s**
> "The estimation model draws on 30 features across five physically-motivated groups — eighteen land-use proportions, two topographic, two population, five weather, two spatial position, plus a COVID-period flag. Every group ties back to a physical mechanism for why it should predict pollution — this isn't a data-dump, every input earns its place."

*Do: point at the diagram as each group lights up conceptually — land use, topography, population, weather, position, COVID.*

---

### 11 — Random Forest, deliberately
**~40s**
> "For the estimator itself, Random Forest, deliberately. It handles mixed feature types without assuming straight-line relationships, and — critically — it doesn't fall apart on a small, oddly-shaped dataset. We only have 11 usable stations. Deep learning and hybrid Kriging approaches were explicitly excluded — they need far more training locations than this network offers. This is about matching model complexity to data availability, not chasing the fanciest option on the shelf."

---

### 12 — Buffered spatial leave-one-out
**~55s**
> "This is the validation method, and it's the single most defensible decision in the thesis. Left panel: a random split leaves nearby stations in the training set right next to the held-out station — the model previews the answer through them. Right panel: buffered spatial hold-out excludes every station within a 5-kilometre buffer of the test station, not just the station itself. An inter-station audit found 24 station pairs closer than that distance — so this isn't a theoretical concern, it's a real leakage risk in this specific network that had to be closed."

*Do: this is your strongest methodological card. Say "single most defensible decision" with full confidence, not as a hedge.*

---

### 13 — Greedy, on purpose
**~45s**
> "For sensor placement: a greedy algorithm, chosen on purpose over swarm-based optimization like PSO, for two reasons. First, transparency — a planner can see exactly why each sensor was recommended, no black box to trust. Second, a provable guarantee: for this class of coverage objective, greedy search is mathematically guaranteed to land within a constant factor of the true optimum. That's not a heuristic hope, it's a proof."

---

### 14 — Five public datasets, five years
**~35s**
> "The data itself: five public datasets — SMHI air quality, SMHI weather, CORINE land cover, EU-DEM elevation, GEOSTAT population — covering 2020 to 2024, 1,827 days of daily records. Everything is public and reproducible, no custom hardware, no proprietary data, and every source shares a common map projection."

---

### 15 — 34 stations, 11 usable
**~40s**
> "Here's the data reality check. 34 SMHI stations have records at all. A 90% daily-completeness bar per station, per pollutant, brings that to 19 passing for at least one pollutant. Only 11 pass for *both* PM2.5 and NO2 concurrently — and those 11 carry every validation fold, every decay curve, in the entire thesis. That's the honest sample size I'm working with."

*Do: say "11" with weight — it recurs constantly through the results and limitations, and the audience needs to register it now.*

---

### 16 — The network on the map
**~35s**
> "Here's what that looks like geographically — all 34 stations plotted by real coordinates, the 11 analytical stations highlighted. The north is almost entirely uncovered above roughly 64 degrees latitude. That empty north is exactly the kind of gap this thesis is built to reason about."

---

### 17 — Accuracy, pollutant by pollutant (RQ1)
**~45s**
> "First result: answering RQ1. For NO2, Random Forest wins outright — mean RMSE of 7.27 micrograms per cubic metre, against 8.90 for IDW and 15.33 for LUR. For PM2.5, the story flips: simple distance-averaging, IDW, wins at 2.33, against 3.56 for Random Forest and 5.87 for LUR. Two pollutants, two different winners — and that's not noise, it's the next slide."

---

### 18 — The simple method won where it mattered most
**~55s**
> "I want to be direct about both of these. PM2.5 is the pollutant the entire sensor-placement result rests on — and the simple method beat my machine learning model, winning at 10 of 11 stations. That's not a failure to bury, it's a finding: PM2.5 spreads smoothly enough that feature-based learning adds little over just averaging nearby stations. NO2 is subtler — Random Forest wins on the *mean*, but IDW actually has lower error at 7 of the 11 individual stations. RF's mean is pulled down by two isolated rural stations where it performs exceptionally well; IDW is competitive or ahead across the rest."

*Do: this is a "reported, not hidden" slide — deliver both paragraphs at the same steady pace you'd use for a positive result. Don't slow down or soften your voice for the second one.*

---

### 19 — Choosing the decay curve: AIC picks the winner
**~45s**
> "Before I show the decay curves themselves, one methodological note. For each pollutant-model combination, I fitted three candidate functional forms — logarithmic, power, and exponential — to the per-station error-distance data, eighteen fits in total, and kept whichever had the lowest AIC. NO2 turned out log-shaped across all three estimators. PM2.5 is exponential for Random Forest and IDW, but log for LUR. The shape wasn't chosen to fit the story — it's what the data selected. Worth noting: Random Forest also posts the lowest AIC of the three models for both pollutants, meaning its error-distance relationship is the cleanest fit of the three, even though IDW is still the more accurate PM2.5 estimator on RMSE."

*Do: this slide exists to pre-empt "how did you actually choose the curve shape" before anyone has to ask it. Deliver it briskly and technically — it's a methods aside, not a result to dwell on.*

---

### 20 — How far can an estimate be trusted? (RQ2)
**~55s**
> "Answering RQ2: fitting decay curves to per-station error against distance gives an estimated prediction-distance threshold of about 64 kilometres for PM2.5, and about 6 kilometres for NO2, under an adopted 50% RMSE criterion — I want to stress these are estimated thresholds under a stated criterion, not fixed reliability limits carved in stone. You can see why in the charts: PM2.5's curve rises gently across all three methods. NO2's error is tied tightly to nearby traffic and degrades far faster — notice the RF panel actually trends down at long range, pulled by those same two rural stations from the last slide."

*Do: point at the PM2.5/NO2 panel labels explicitly so the audience tracks which chart is which.*

---

### 21 — 20 sensors, national coverage (RQ3)
**~55s**
> "Answering RQ3, applying the PM2.5 threshold: a 20-sensor greedy placement raises national PM2.5 land coverage from 10.9% to 67.2%, and urban coverage from 38.8% to 71.4%, bringing 4 of Sweden's 7 currently unmonitored regions into service. But — same 20 sensors, checked against NO2's stricter 6-kilometre threshold — land coverage barely moves, 0.2% to 0.6%, and urban coverage doesn't move at all, flat at 6.1%. I'll come back to why that matters in a moment."

*Do: this is the slide where RQ1→RQ2→RQ3 clicks into one story — PM2.5's smooth spatial pattern (RQ1) is why its decay is gradual (RQ2), which is why 20 sensors can move its coverage this much (RQ3); NO2's sharp gradient explains the opposite outcome. Say that connection out loud if you have the time — it's not on any slide, but it's the single best sentence you can add live.*

---

### 22 — 20 recommended locations
**~35s**
> "Here's where those 20 sensors actually land — spreading from Götaland in the south, through Svealand, up into Norrland in the north, each one chosen to close the biggest remaining gap at the time it was placed."

*Do: shortest slide to talk over if you're behind schedule — the caption and map do the work.*

---

### 23 — Before and after
**~35s**
> "And the coverage picture before and after: grey is beyond the PM2.5 threshold, blue is within reliable range of a station or sensor. The shift from the left panel to the right is the 10.9%-to-67.2% number made visible."

---

### 24 — The same 20 sensors barely help NO2
**~40s**
> "I already previewed this, but it's worth landing properly: checked against the stricter 6-kilometre NO2 threshold, the same 20 sensors move national NO2 land coverage only from 0.2% to 0.6% — and urban NO2 coverage doesn't move at all, flat at 6.1% before and after. A sensor plan sized for PM2.5 does not solve NO2. I'm saying that plainly because the thesis says it plainly, rather than letting the headline PM2.5 number imply otherwise."

*Do: this is the second "reported, not hidden" beat — same steady, confident delivery as slide 18.*

---

### 25 — Two pollutants, two planning problems
**~40s**
> "So what does that mean practically? A PM2.5-sized deployment leaves NO2 exposure near traffic effectively unmonitored between stations. Municipalities planning IoT deployments need to treat the two thresholds as separate constraints, not a shared budget. And four newly-served regions — Jönköping, Örebro, Dalarna, Norrbotten — are concrete near-term priorities today, independent of any future NO2-specific work."

---

### 26 — What this doesn't yet resolve
**~55s**
> "No thesis is without limits, and I'd rather name mine than have them found. Only 11 stations carry every result here. The 5-kilometre exclusion buffer is justified by how the network happens to cluster, not by the true spatial autocorrelation range. The evaluation grid, at 10 kilometres, is coarser than the NO2 threshold itself, so it can't fully resolve NO2's coverage geometry. Straight-line distance stands in for road-network distance, which would be more physically right for NO2, but wasn't computable from this network's sparsity. And the 50% criterion itself is a modelling choice, not a fixed rule — sweeping it from 20 to 80% swings the post-placement PM2.5 coverage figure all the way from 2.9% to 94.7%."

*Do: deliver this list briskly and matter-of-factly — five items, no dramatic pauses. The confidence is in the pacing, not the content.*

---

### 27 — One sentence
**~35s**
> "If I had to put the contribution in one sentence: a reproducible method, built entirely on public data, that turns 'how accurate is our estimate at distance X' into a ranked list of where to put the next sensor — demonstrated at the scale of an entire country. What it is *not*: an operational deployment plan, and not a regulatory compliance tool. It's a starting point for site-level planning, not a finished answer."

---

### 28 — Future work
**~35s**
> "Looking ahead: validating against a denser reference network, or replicating this in another country; jointly optimizing placement for both pollutants instead of PM2.5 alone; a finer national grid that can actually resolve the NO2 threshold; and periodic recalibration as traffic patterns shift — vehicle electrification in particular is likely to flatten NO2's spatial gradient over the coming years."

---

### 29 — Thank you
**~15s**
> "Thank you. I'm happy to take questions."

*Do: say it, then stop. Don't fill the silence — let the chair take over.*

---

## Q&A prep — points that aren't on any slide

These didn't make the cut as slides (by your own call, to keep the deck tight), but examiners may ask about them directly. Each answer below is taken straight from your thesis text, not improvised — cite it with the same confidence as anything that *is* on a slide.

**"Why don't I see R² anywhere?"**
R² for NO2 is deliberately *omitted* from the mean-metrics tables — not forgotten. Two rural stations (Bredkälen, Norr Malma) have near-constant, very low NO2 concentrations. For LUR and IDW at those two stations, R² blows up to extreme negative values (LUR: −10,018 at Bredkälen, −151 at Norr Malma) that would dominate and misrepresent any simple mean. RMSE and MAE are the primary RQ1 metrics for exactly this reason — they're not distorted by this effect. R² is still reported *per station* in Tables 5 and 6 (added specifically in response to your examiner's Comment 2/3), just not averaged. For PM2.5 the R² spread is much tamer (−5.92 to +0.92 across methods), but it's omitted from that table too, for direct comparability with the NO2 table.

**"How does this compare to the ESCAPE R² benchmarks you mentioned in Related Work?"**
Say directly that a clean comparison isn't possible, and explain why — that's a stronger answer than trying to force one. ESCAPE's R² benchmarks (0.71 PM2.5, 0.83 NO2) come from spatial cross-validation of *annual mean* concentrations across 20–40 monitoring sites per study area. Your R² values are computed per station across *daily* time series under buffered SLOO — a stricter, differently-structured evaluation that frequently produces negative R² even when RMSE is low. The more comparable evaluation is RMSE against the LUR benchmark, calibrated on the *same* station network — and both Random Forest and IDW beat LUR on RMSE for both pollutants.

**"What about validity, reliability, and ethics?"**
Internal validity rests on the buffered SLOO design specifically preventing spatial leakage, so reported errors reflect genuinely unmonitored locations. External validity is limited to the Swedish network and its geographic/meteorological context — generalizing elsewhere would need replication in that new data environment. Reliability: every data source is public and documented, and the full pipeline runs with fixed random seeds for reproducibility. Ethics: every data source is an open-data product with no personal information, no human participants are involved, and the study doesn't require ethical review under Swedish research ethics legislation.

**"Did you check whether the NO2 urban/rural confound is real, or just assumed?"**
It's measured, not assumed — Section 6.3 stratifies explicitly. Traffic stations show mean RF RMSE of 8.30 µg/m³ versus 6.03 for background stations (background looks better only because the two rural stations have near-zero concentrations that suppress absolute error). For IDW the pattern *reverses* — traffic stations do better (7.44) than background (10.66), because IDW at isolated rural stations has to interpolate from distant, dissimilar urban training stations. There's also a seasonal effect: NO2 RF RMSE rises from 7.13 in summer to 8.74 in winter, consistent with winter inversion and heating emissions sharpening spatial gradients.

**"What about the low-cost IoT sensor literature specifically — smart cities, calibration, integration?"**
If pressed, acknowledge the thesis's related-work section covers this (low-cost IoT sensor networks for urban monitoring, and the smart-city framing where air quality is one of several sensed domains a city acts on), but that your contribution is squarely the placement decision rule, not sensor hardware or calibration — that's explicitly out of scope, consistent with the "not an operational deployment plan" framing on slide 27.

---

## Final checklist before you present

- Rehearse the full script once against a timer — you're targeting ~19 minutes, leaving room for the room's actual clock.
- Know the four numbers cold: **7.27** (NO2 RF RMSE), **64 km / 6 km** (thresholds), **67.2% / 71.4%** (PM2.5 coverage after), **0.6% / 6.1%** (NO2 coverage after). If you forget everything else, these four carry the whole results section.
- If a laptop or projector substitution happens, the deck is a single self-contained HTML file — open it directly, no other files needed.
