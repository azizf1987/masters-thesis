# Rejoinder

Responses to comments received on the thesis draft from the examiner (Erdal Akin) and the
opponents (linne, Pari). Organised in two parts, in the order the comments appear in the
thesis. Each entry states the comment, whether it was fixed or is defended as written, and
what actually changed. References are to section names, not line numbers, since the
authoritative working copy is maintained outside this repository.

---

## Part 1: Examiner Comments

### E1: Section 2.5 (Research Gaps and Positioning)

**Comment:**
Phrase cautiously if you cannot support by a systematic review, as you have not done for this work.

**Response: Fixed.**
The claim is now scoped to the literature reviewed in this thesis (not an absolute claim about
the field), and specifically extended to note that no distance-accuracy analysis exists for the
Swedish SMHI network either, citing Segersson et al. and the Stockholm/Gothenburg/Malmö
dispersion study to show the Swedish literature was checked.

---

### E2: Section 3.3 (Spatial Validation Protocol)

**Comment:**
Using buffered spatial leave-one-out validation is appropriate, but the 5 km buffer is much
smaller than the reported spatial autocorrelation range (150-200 km). Therefore, the validation
should not be described as fully "spatially honest." The limitation should be stated more
clearly, and a small sensitivity test with different feasible buffer distances would strengthen
the work.

**Response: Fixed.**
Three changes:

1. The phrase "spatially honest" is removed throughout (Introduction and §3.3) and replaced with
   language that does not overstate the protocol (e.g. "with near-neighbour leakage suppressed").
2. The existing buffer-justification paragraph in §3.3 is sharpened to state explicitly that the
   5 km buffer reduces but does not eliminate the optimistic bias from spatial autocorrelation,
   and that the reported errors should be read as a lower bound on true prediction error.
3. A buffer-distance sensitivity analysis was run: the full buffered SLOO procedure was repeated
   at 0, 5, 10, 25, and 50 km exclusion radii (`data/phase6_buffer_sensitivity.py`). The estimator
   ranking is unchanged at every buffer tested (IDW best for PM$_{2.5}$, Random Forest best for
   NO$_2$, LUR worst for both), and mean RMSE for the two selected estimators varies by no more
   than 6% between the 5 km and 50 km buffers. A new table and paragraph reporting this are added
   to §3.3, and a corresponding sentence is added to the limitations section (§8.4). Buffers
   approaching the 150-200 km autocorrelation range are not testable: above roughly 80 km, at
   least one validation fold loses all training data, which is now stated explicitly.

---

### E3: Section 4.1 (Air Quality Observations)

**Comment:**
This is a small effective spatial sample for generalization.

**Response: Defended, no change.**
Agreed, and already stated as a limitation. §8.4 notes that the 11 concurrently-passing stations
are "substantially smaller than the 20-40 monitoring sites comprising each ESCAPE study area,"
constraining the statistical power of the validation and the granularity of the resulting decay
curves. No further change made; this is treated as an acknowledged constraint of the Swedish
national network rather than a defect to correct.

---

### E4: Section 5.1 (NO2 Estimation Results, Table 5)

**Comment:**
In table 5, IDW provides better RMSE in 7/11 stations. Even RF provides lower RMSE, this
situation needs to be clarified. It would be great if you could provide R^2 and MAE of LUR and
IDW.

**Response: Fixed.**
Added MAE and R² for LUR and IDW (previously only RMSE was shown). Added a short explanation of
why IDW wins at 7/11 stations despite RF's lower mean RMSE: RF's mean is pulled down by two
isolated rural stations where it performs exceptionally well, while IDW is competitive or better
at most of the remaining nine.

---

### E5: Section 5.2 (PM2.5 Estimation Results, Table 6)

**Comment:**
As seen in Table 6 also, IDW provides better performance for all the aspects. So, it would be
better to provide all the related metrics for the three algorithms and compare fairly instead of
making RF the core algorithm.

**Response: Fixed.**
Added MAE and R² for LUR and IDW here as well. Noted that no equivalent caveat is needed for
PM$_{2.5}$: IDW wins at 10/11 stations, which is consistent with its lower mean RMSE (unlike the
NO$_2$ case).

---

### E6: Section 6.2 (Decay Curve Fitting)

**Comment:**
These criteria should be defined and elaborated to show the effect and necessity. Also, this
section needs a transition why we need to see Decay curve fitting.

**Response: Fixed.**
AIC/BIC are now defined and elaborated in §6.2 (formulas, what they measure, why AIC over raw
fit), with the design rationale for the choice moved to §3.4 so it is argued once, in the
methodology, rather than repeated. Added a transition at the start of §6.2 linking it back to
§3.4.

---

### E7: Section 6.4 (Estimated Prediction-Distance Threshold and Answer to RQ2)

**Comment:**
I would therefore recommend that 64 km should not be called "the reliable prediction distance"
without qualification. It would be better described as something like: the estimated
prediction-distance threshold under the adopted 50% RMSE criterion. This distinction should
appear in the Abstract, Results, Discussion and Conclusion. The 64 km and especially the 6 km
values should therefore be presented as criterion-dependent estimates, not precise national
reliability limits.

**Response: Fixed.**
The thesis presents 64 km and 6 km as "estimated prediction-distance thresholds under the
adopted 50% criterion," not fixed reliability limits, with an added note that both are
criterion-dependent estimates (with extra caution on the 6 km NO$_2$ figure). This is applied in
the Abstract, in §6.4 (retitled "Estimated Prediction-Distance Threshold and Answer to RQ2"), in
the Discussion's RQ2-answer paragraph, and in the Conclusion.

On review, three further occurrences of the unqualified phrase "the reliable prediction
distance/threshold" attached directly to the 64 km figure had survived outside §6.4, in the
Placement section's opening paragraph, in the Integrated Results (RQ1-RQ3) paragraph (two
occurrences), and in the Discussion's Risks and Constraints subsection, the last of which also
asserted that a covered location was "trustworthy" without qualification. All three are now
corrected to "estimated prediction-distance threshold," and the Risks and Constraints sentence is
reworded to state that coverage indicates the location is expected to meet the adopted 50%
criterion, not that it is unqualifiedly "trustworthy."

---

### E8: Section 7.1 (National Coverage Surface)

**Comment:**
Good point to declare. *(on the statement that NO2 baseline coverage is minimal: 7 of 4,588 land
cells, 0.2%)*

**Response: Acknowledged, no change requested.**
This was agreement with a point already made in the thesis, not a request for revision.

---

### E9: Section 7.3 (Coverage Evaluation and DSR Assessment)

**Comment:**
Can you extend the work for population-weighted coverage. You can use same experiment you have
done for this evaluation and do again wrt population. I would like to see this. If time permits,
you can also work on urban-area coverage, which is pretty similar to the population-based
approach.

**Response: Fixed.**
Urban-area coverage was already reported in the thesis (land coverage 10.9% → 67.2%; urban
coverage 38.8% → 71.4%). Population-weighted coverage is new: each 10 km grid cell was weighted
by its resident population, aggregated from the JRC GEOSTAT 2018 1 km population grid (~10.6
million inhabitants assigned across the national land grid; `data/phase7_population_coverage.py`).
Results: population-weighted PM$_{2.5}$ coverage rises from 45.0% to 77.1% nationally (67.1% to
75.9% within urban fabric) after the 20 recommended placements, markedly higher than the
land-area figures, because existing stations are concentrated in populated areas. For NO$_2$,
population-weighted coverage moves only from 10.1% to 10.4% nationally and is unchanged at 17.0%
within urban fabric, consistent with the land-area result: the PM$_{2.5}$-optimised deployment
does not materially improve NO$_2$ coverage on any measure. A new paragraph and table
(land-area vs. population-weighted, national vs. urban, before/after, both pollutants) are added
to §7.3, and a caveat is added to §8.4 noting that the population-weighted NO$_2$ figures inherit
the same 10 km grid-resolution limitation already stated for the land-area NO$_2$ figures.

---

### E10: Figures 2 and 3, decay curves (LUR centre panel)

**Comment:**
Explain more about the middle (LUR) panel: the fitted line is nearly straight/flat, which could
be read as LUR being more stable with respect to distance. Why was LUR not selected?

**Response: Fixed.**
The single existing sentence in §6.2 ("LUR curves are reported for completeness but carry
substantial uncertainty due to the high cross-fold variability of the linear model") is expanded
to explain the flat line explicitly. The LUR fit is flat because its error is uniformly poor, not
because it is distance-robust: LUR RMSE sits at approximately 15 µg/m³ (NO$_2$) and 6 µg/m³
(PM$_{2.5}$) at every distance, in both cases above the pollutant's own mean concentration
(12.85 and ~5.3 µg/m³). The near-zero slope arises because LUR's error is dominated by cross-fold
instability (30 partly collinear predictors on 11 folds), which is large relative to any distance
effect; the wide vertical scatter of the points and the poor curve fit (AIC 83.5 / 58.8 versus
60.7--63.4 and 25.3--38.6 for RF and IDW) show the flat line is not an informative relationship.
LUR is therefore not a candidate for the threshold, consistent with it being the least accurate
estimator for both pollutants in §5. A one-clause note to the same effect is added to the
captions of Figures 2 and 3.

---

## Part 2: Opponent Comments

### O1: Title page

**Comment (linne):**
Shouldn't this be a sub-title? *(on the portion of the title after the colon)*

**Response: Defended, no change.**
The title is the one approved in the research proposal; the wording is unchanged either way.
Reformatting it as a two-line title/sub-title is a cosmetic option, not a required change, and is
left as a single line consistent with the approved proposal.

---

### O2: Section 2 (Background and Related Work)

**Comment (linne):**
A short introduction to the different topics you talk about in this section would be nice.

**Response: Fixed.**
A short paragraph was added immediately after the section heading, previewing the five
subsections that follow (regulatory monitoring, low-cost IoT sensors, spatial estimation methods,
sensor placement optimisation, and the research gaps).

---

### O3: Section 2 / 2.1 (Background and Related Work)

**Comment (Pari):**
The section discusses relevant previous studies but the process used to identify and select the
literature is not described. Could you briefly explain which databases or search tools were used.

**Response: Fixed.**
A paragraph was added describing the search process: literature was identified primarily through
Google Scholar, with IEEE Xplore used for the conference proceedings, and by following the
reference lists of the principal review papers (Hoek et al.; the ESCAPE studies) to trace related
work. Search terms are listed. The paragraph states explicitly that this was a targeted narrative
review, not a systematic review, consistent with the hedge already applied to §2.5 (E1 above).

---

### O4: Section 2.1 (Urban Air Quality Monitoring and Regulatory Networks)

**Comment (linne):**
This thesis? *(on the phrase "The present thesis")*

**Response: Fixed.**
"The present thesis" is reworded to "This thesis" at this location and at one further, equivalent
occurrence in §2.3.

---

### O5: Section 2.3 (Spatial Estimation of Air Quality at Unmonitored Locations)

**Comment (linne):**
When writing abbreviations the text should be "Inverse Distance Weighting." By some university
writing guidelines for acronyms and abbreviations.

**Response: Defended, no change.**
The term is introduced in the standard form used throughout the thesis: lower case at first use
with the acronym given in parentheses, and capitalised in the List of Abbreviations. This follows
the convention used consistently for every other abbreviation in the thesis (e.g. "land-use
regression (LUR)"), so it is retained for consistency rather than treated as an isolated
exception.

---

### O6: Section 2.3 (Spatial Estimation of Air Quality at Unmonitored Locations)

**Comment (linne):**
Reference? *(on the paragraph describing LUR's known limitations)*

**Response: Fixed.**
The paragraph is attributed to Hoek et al. and reworded to state only what that review supports:
that LUR models are empirical and area-specific, and their predictive performance is not
guaranteed to transfer to areas or periods outside the monitoring campaign used to fit them,
alongside the existing point that a linear form does not represent non-linear predictor
interactions by construction. The citation metadata was confirmed against ADS and ScienceDirect,
and the transferability limitation is consistently attributed to this review in the secondary
literature, so no verification marker remains in the thesis source.

---

### O7: Section 3 (Research Methodology)

**Comment (linne):**
All theses do not need to look exactly the same, but I think best-practice is that new "chapters"
should start on a new page.

**Response: Defended, no change.**
The opponent's own phrasing acknowledges this is a formatting preference, not a requirement. The
document follows the MAU thesis template's layout conventions. Left as is.

---

### O8: Section 3.2.2 (Feature Set)

**Comment (Pari):**
Section 4.1 represents that all 34 stations may contribute training data, while only 11 stations
are eligible as validation targets. So, the phrase "11 unique spatial training locations" is
unclear and appears inconsistent with Sections 4.1 and 5.

**Response: Fixed.**
This was a genuine wording inconsistency; §4.1 already states the correct relationship (34
stations may contribute training rows; 11 concurrently-passing stations are eligible to be
withheld as validation targets), and §5 confirms training uses 26-33 stations per fold, not 11.
The phrase "11 unique spatial training locations" is corrected to "11 spatially independent
validation targets" (or equivalent) at the three locations where it previously appeared
incorrectly (§3.2.2, §3.2.3, §8.4), aligning them with §4.1.

---

### O9: Section 5 (Spatial Estimation Models)

**Comment (linne):**
What is "this chapter"? I think the structure of what is results could perhaps be better
structured or perhaps just named differently so it is more clear what is the actual results of
the study. I cannot see that chapter is used anywhere else in the thesis and it is therefore
unclear what is chapter/section.

**Response: Partially fixed.**
"This chapter" was a genuine slip: it is the only use of "chapter" in the entire thesis, which
otherwise uses "section" as the top-level unit throughout. It is corrected to "the results" with
an explicit section range. The broader structural point is defended: the three results sections
are each named by research question (RQ1/RQ2/RQ3) and explicitly signposted in the opening
paragraph of §5, which is judged sufficient without renaming the sections themselves.

---

### O10: Section 5 (Spatial Estimation Models)

**Comment (linne):**
This is "double negative" phrasing which is a bit unclear, and as per my understanding should be
avoided. *(on "not excluded by the 5 km buffer")*

**Response: Fixed.**
Reworded to "the stations that remained after the 5 km exclusion buffer was applied," removing
the double negative.

---

### O11: Section 6.4 (Estimated Prediction-Distance Threshold and Answer to RQ2)

**Comment (Pari):**
The sensitivity analysis clearly explains that the 50% criterion is a modelling choice. But, it
is still unclear why this level represents the "minimum requirement" for spatial planning.

**Response: Fixed.**
The unsupported claim that 50% is the "minimum requirement for spatial planning purposes" is
removed. The paragraph is reworded to state plainly that the 50% level is a working threshold
adopted for this study, not a universal planning standard, and to point immediately to the
sensitivity analysis that tests it, consistent with the criterion-dependent framing already
applied elsewhere in §6.4 (E7 above).

---

### O12: Figure 6

**Comment (linne):**
The triangles are red not green. A little confusion to write "placed sensors" on the figure, and
"recommended sensor locations" in the description? There are no red circles in the figure.

**Response: Fixed.**
The figure itself (`fig_coverage_before_after.png`) already used the correct, current colour
scheme (blue circles for existing stations, red triangles for recommended sensors), matching
Figures 7 and 8; only the caption was stale, describing an earlier colour scheme (red circles,
green triangles). The caption is corrected to match the actual figure, and the "placed sensors"
legend label vs. "recommended sensor locations" caption wording is reconciled by noting the
legend label explicitly in the caption.

---

### O13: Figure 7

**Comment (linne):**
These labels are impossible to see or read. *(on the numbered placement-rank labels)*

**Response: Fixed.**
Confirmed: the rank labels were drawn at font size 7 in the same colour as the marker, directly
on top of the darkest part of the heatmap, and were effectively illegible. The figure
(`fig_placement_map.png`) is regenerated with larger, bold, black labels with a white halo,
clearly legible against both the heatmap and the markers. A new standalone script,
`data/phase7_fix_placement_labels.py`, rebuilds this figure from saved results without touching
any other figure or data file.

---

### O14: References

**Comment (Pari):**
IEEE reference guide is to write et al. after six authors.

**Response: Fixed.**
Four bibliography entries exceeded six authors (Hoek et al. 2008, 7 authors; Segersson et al.
2017, 7 authors; Roberts et al. 2017, 14 authors; Kilbo Edlund et al. 2024, 14 authors). Each is
now truncated to the first author plus "and others" in `references.bib`, which the thesis's
`ieeetr` bibliography style renders as "et al." No other references or the bibliography style
itself were changed.

---

## Summary

| # | Comment | Outcome |
|---|---|---|
| E1 | §2.5 systematic-review hedging | Fixed |
| E2 | §3.3 buffer / "spatially honest" | Fixed (wording + sensitivity table + limitation) |
| E3 | §4.1 small validation sample | Defended |
| E4 | §5.1 Table 5 IDW/RF | Fixed |
| E5 | §5.2 Table 6 IDW/RF | Fixed |
| E6 | §6.2 AIC/BIC definition | Fixed |
| E7 | §6.4 threshold terminology | Fixed |
| E8 | §7.1 NO2 baseline coverage | Acknowledged |
| E9 | §7.3 population-weighted coverage | Fixed (new analysis) |
| E10 | Figures 2-3 LUR centre panel | Fixed (expanded §6.2 + caption clauses) |
| O1 | Title sub-title | Defended |
| O2 | §2 intro paragraph | Fixed |
| O3 | §2/2.1 literature search process | Fixed |
| O4 | §2.1 "This thesis?" wording | Fixed |
| O5 | §2.3 IDW capitalisation | Defended |
| O6 | §2.3 LUR limitations reference | Fixed |
| O7 | §3 chapters on new page | Defended |
| O8 | §3.2.2 "11 unique spatial training locations" | Fixed |
| O9 | §5 "this chapter" / structure | Partially fixed (wording fixed; structure defended) |
| O10 | §5 double negative | Fixed |
| O11 | §6.4 "minimum requirement" | Fixed |
| O12 | Figure 6 caption | Fixed |
| O13 | Figure 7 labels | Fixed |
| O14 | References "et al." | Fixed |
