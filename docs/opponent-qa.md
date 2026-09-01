# Answers to Opponent Questions

Prepared responses for the defense of *Spatial Estimation of Air Quality at Unmonitored Locations Using Machine Learning: Implications for IoT Sensor Network Design in Swedish Cities*. Each answer has a short spoken version you can lead with, followed by the supporting detail and the exact thesis sections to point to if pressed.

---

## Q1. Confidence in the 64 km (PM2.5) and 6 km (NO2) thresholds, given only 11 validation stations

**Short answer to lead with:**

"My confidence is asymmetric between the two figures, and I want to be precise about what kind of number each one is. Neither is a fixed reliability limit — both are described in the thesis as *estimated prediction-distance thresholds under an adopted 50% criterion*, and I ran a sensitivity sweep specifically because I don't trust a single point estimate from 11 stations to stand on its own."

**PM2.5 (64 km) — moderate-to-reasonable confidence:**
- The decay pattern across the 11 stations is regular and monotonic for both RF and IDW (RMSE rises smoothly from under 1.3 to about 5.5 µg/m³ across the 6–82 km range) — this is a real, visually and statistically coherent trend, not noise.
- The winning functional form (exponential) beats the next-best candidate by a solid AIC margin (38.55 vs 39.03 for IDW), so the choice of curve shape isn't a coin flip.
- Under the criterion sensitivity sweep (20–80% of sample mean), the *threshold value* moves a lot (12 km at 30% to 98 km at 70%), but the *qualitative conclusion* — PM2.5 coverage exceeds NO2 coverage at every criterion tested — is stable. So I'm confident in the shape of the finding; I'm much less confident in "64" as a precise number.

**NO2 (6 km) — low confidence, and I say so explicitly in the thesis:**
- Only 2 of the 11 stations are rural; the other 9 are urban. Those 2 rural stations (Bredkälen, Norr Malma) have such low baseline NO2 concentrations that they invert the RF distance-error relationship entirely (error *decreases* with distance). The aggregate curve used to derive 6 km is fit on a sample where the rural/urban split does real damage to the signal.
- For the two best-AIC forms in this pollutant/model combination, the gap is under 1.0 (e.g., NO2 RF: log at 60.68 vs exponential at 61.33) — by standard AIC guidance (Burnham & Anderson), that's "weak evidence," meaning the two curve shapes are statistically about equally plausible given the data.
- The 10 km analysis grid is coarser than the 6 km threshold itself, so even the coverage numbers built on top of this threshold can't resolve NO2 geometry properly — a second, independent reason not to over-trust this figure.
- I flag this in the thesis itself: the NO2 threshold "should be interpreted with particular caution — more so than the PM2.5 figure."

**What would raise my confidence, if pushed:**
- More concurrently-passing stations (the completeness threshold and the requirement that a station report both pollutants cut 34 down to 11 — relaxing either would help, at a data-quality cost).
- Bootstrapped confidence intervals around the fitted decay parameters — I did not compute these, and I'd flag that as a concrete, feasible piece of future work rather than something I could claim already exists.
- Road-network distance instead of Euclidean distance for NO2, since it's traffic-sourced and Euclidean straight-line distance is a weaker proxy for exposure gradients there.
- Stratifying the NO2 curve by station type before fitting (urban-only vs. rural-only), rather than fitting one aggregate curve across a confounded sample.

**One-line summary if you need to close it out:** "Both numbers are honestly reported as criterion-dependent estimates from a small sample, not calibrated national limits. I have real, if moderate, confidence in the PM2.5 figure and the qualitative PM2.5-vs-NO2 asymmetry; I have low confidence in the specific 6 km NO2 figure and I built that caveat into the thesis rather than waiting for you to find it."

*Backing sections: §6.3–6.4 (decay curve fitting and threshold derivation), §7.4 discussion-limitations, Table "Decay curve parameters," Figure "Threshold sensitivity."*

---

## Q2. Who is this thesis meant to help — government, municipal, or computer science audiences? Were any of them involved?

**Short answer to lead with:**

"The primary intended audience is municipal and regional environmental agencies making IoT sensor placement decisions — that's stated in the abstract and the discussion. I did not have that audience explicitly named in one place up front, which in hindsight is a fair thing to flag, and I did not involve any actual municipal or government stakeholder in this study — it's a desk-based, data-driven Design Science Research artefact, evaluated on metrics rather than on practitioner feedback."

**Where the intended audience is actually stated (so you can point to it):**
- Abstract: "...prioritised sensor placement guidance for Swedish municipal air quality planning."
- Introduction: "For environmental agencies and municipalities seeking to understand exposure at street or neighbourhood scale... For engineers and planners seeking to deploy supplementary monitoring infrastructure..."
- §7.3 (Implications for Municipal IoT Planning): "Municipalities and regional environmental agencies seeking to address both pollutants with a single IoT deployment should treat the two thresholds as separate planning constraints..."
- §6.6: "The output of this artefact is a prioritised set of candidate coordinates for further evaluation by municipal planners; it does not constitute a deployment specification."

So the intended reader is consistently framed as a municipal/regional environmental-agency planner deciding where to put sensors — not a national government policy body, and not primarily a computer science audience (though the estimation and validation methodology is a secondary contribution of interest to that community).

**Honest answer on stakeholder involvement — no, none were:**
- No municipality, county administrative board, or SMHI representative was interviewed, consulted, or asked to review the placement recommendations.
- The DSR "Evaluation" phase (Peffers et al. mapping, §3.1) is carried out entirely through internal metrics — RMSE/MAE/R², percentage of urban area brought into coverage, number of previously-unmonitored regions served — not through practitioner review or field validation.
- This is a legitimate DSR pattern for a first-iteration artefact (Hevner et al. distinguish artefact construction from artefact validation-in-use), but it does mean the "for municipal planning" framing is a design intention, not a confirmed fit demonstrated with real planners.

**If the opponent pushes on why this wasn't done:**
- Scope and time: a 30-credit single-author thesis with a national-scale case study did not have room for a stakeholder engagement phase alongside the modelling, decay analysis, and placement work.
- Reasonable next step: a follow-up validation phase presenting the 20 candidate coordinates to one or two regional environmental agencies (e.g., in one of the four newly-served regions — Jönköping, Örebro, Dalarna, Norrbotten) to check whether the recommendations align with their own siting constraints (power, access, existing infrastructure) not modelled here.

**One-line summary:** "Municipal and regional environmental agencies are the named intended audience throughout the thesis, but that audience was not consulted during the research — the evaluation is metric-based, and I'd frame that as a clear, named direction for follow-up work rather than something I can claim was already done."

---

## Q3. The literature review (§2.3) — was Europe a deliberate filter, and what databases/libraries did you search?

**Short answer to lead with:**

"Europe wasn't a geographic filter I applied — it's where the relevant methodology actually lives. The established peer-reviewed standard for this exact problem, land-use regression validated through the ESCAPE project, is a European multi-cohort study, so any thesis addressing spatial estimation of air quality at unmonitored European locations has to engage with it directly. I did include non-European work — the machine-learning and IoT-sensor-placement literature I cite spans a wider geographic range — but for the specific benchmark of 'what accuracy should a spatial estimation method achieve in a European context,' Europe is genuinely where that benchmark comes from, not a search constraint I imposed."

**Detail to have ready:**
- §2.3 is built around one specific comparison: your model has to be judged against *something*, and the field's actual established standard for this task in Europe is LUR/ESCAPE (Hoek et al. 2008 review of 25 studies; Eeftens et al. 2012 for PM2.5, R² ≈ 0.71; Wang et al. 2013 for NO2, R² ≈ 0.83). That's not me choosing Europe — that's the literature choosing itself, because ESCAPE is the largest and most-cited standardized validation of this exact method across 20 European study areas.
- Separately, §2.2 (IoT/low-cost sensor literature) and §2.3's ML-methods paragraph draw on work that is not Europe-restricted — e.g. IoT air-quality reviews and ML spatial interpolation studies from broader international venues.
- I also deliberately searched for Swedish/Scandinavian-specific work (Segersson et al. 2017; the Stockholm/Gothenburg/Malmö dispersion study) because the case study *is* Sweden — that's a case-study-relevance filter, not a "Europe only" filter, and I'd distinguish those two things clearly if asked.
- I'd be direct that this was **not run as a formal systematic review** with a documented PRISMA-style search protocol, string, and database export — my supervisor raised exactly this point on an earlier draft (the claims in §2.3 were rephrased to be scoped to "the literature reviewed in this thesis" rather than asserted as an absolute claim about the field, precisely because I can't back a systematic-review-strength claim). I'd rather say that plainly than overstate the rigor of the search process.

**On "which databases/libraries":**
This is the one part of your answer I can't respond for you — I don't have a record in your project files of exactly which discovery tools you personally used session to session. Based on the mix of publishers actually cited (IEEE Xplore conference proceedings, MDPI journals — *Sensors*, *Atmosphere*, *Sustainability* — Elsevier journals, ACS's *Environmental Science & Technology*, Springer), your search clearly wasn't confined to one index. If that matches your memory, a safe, accurate answer is something like: "I searched broadly via Google Scholar and cross-checked coverage in Scopus/IEEE Xplore for the IoT and sensor-placement literature, and went directly to publisher databases (ScienceDirect, SpringerLink, MDPI) once I'd identified the key papers by citation chasing from Hoek et al. and the ESCAPE studies." Please confirm or correct that before you say it out loud — I'd rather you state the real tools than a plausible-sounding guess.

**One-line summary:** "Europe wasn't a filter, it's where the established comparison standard comes from; the literature review was a targeted, gap-driven review organized around seven thematic streams rather than a formal systematic review, and I said so on the record already when my supervisor raised it on an earlier draft."

---

*Cross-reference: docs/rejoinder.md, Comments 4 and 5, already document that (a) claims in §2.5 were rephrased to avoid overstating systematic-review rigor, and (b) the 64 km/6 km figures were relabeled as criterion-dependent estimates rather than fixed reliability limits — both directly relevant if the opponent has read the earlier draft and notices the change.*
