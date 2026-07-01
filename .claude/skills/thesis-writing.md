---
name: thesis-writing
description: "Writing and style guide for the MSc thesis at Malmö University on spatial air quality estimation and IoT sensor placement. Use when the user asks to draft, edit, improve, review, or check any thesis prose; when editing writing/thesis.tex; when the user mentions em dash, British spelling, abstract, popular science summary, acknowledgements, declaration, section writing, conclusion, discussion, or methodology prose; when fixing LaTeX punctuation or academic register. Not for code, data scripts, or non-thesis documents."
metadata:
  owner: abdalazeez-asaad
  email: "aziz.f1987@gmail.com"
  team: "MAU IoT Thesis"
  version: "2.0.0"
  last_validated: 2026-07-01
compatibility: "Claude Code. Requires a LaTeX environment for compilation. All rules apply to writing/thesis.tex and any thesis-related documents. Do not apply to data/ or scripts/."
---

# thesis-writing

## When to use

- User is drafting or revising any section of writing/thesis.tex
- User asks to review, improve, or check prose in the thesis
- User mentions: *edit thesis*, *fix spelling*, *check em dash*, *write abstract*, *popular science*, *improve section*, *academic writing*, *British spelling*, *LaTeX punctuation*
- User is editing the Abstract, Popular Science Summary, Declaration of AI Usage, Acknowledgements, Introduction, Background, Methodology, Results, Decay Analysis, Placement, Discussion, or Conclusion

---

## CRITICAL RULES (apply before anything else)

### No em dashes — ever

Em dashes (`—` Unicode, or --- in LaTeX) are banned everywhere: thesis prose and all generated text. No exceptions.

| Situation | Replacement |
|-----------|-------------|
| Appended list or definition | Colon : |
| Optional aside or parenthetical | Parentheses () |
| Contrast or consequence | Semicolon ; or *yet* |
| Two loosely joined clauses | Rewrite as one flowing sentence |

### No contractions

Never: *don't*, *can't*, *isn't*, *it's*, *doesn't*, *won't*, *there's*, *that's*.
Always: *do not*, *cannot*, *is not*, *it is*, *does not*, *will not*, *there is*, *that is*.

### No personal pronouns in body chapters

Do not use *I*, *my*, *we*, *our* in Introduction through Conclusion. The Acknowledgements section is the sole exception.

### British spelling throughout

*operationalisation*, *behaviour*, *standardisation*, *recognised*, *colour*, *parameterisation*, *parameterised*, *modelling*, *analysed*, *formalised*, *categorised*, *initialised*, *optimised*.

---

## En dashes in LaTeX (`--`)

Use -- only for numeric or alphabetic ranges: RQ1--RQ3, 10--64\,km, 2020--2024.
Prose date spans use "to": 2020 to 2024.
Never use -- for asides, definitions, or examples.

---

## Punctuation by function

| Intent | Use |
|--------|-----|
| List or definition after a noun phrase | Colon : |
| Short names or items in running text | Commas |
| Optional comment or parenthetical example | Parentheses () |
| Contrast or consequence between clauses | Semicolon ; or *yet* |
| Examples introduced in passing | *such as* / *including* |

---

## Patterns to avoid

| Pattern | Replace with |
|---------|-------------|
| Sentence-initial "However" | *yet*, a semicolon, or merged clause |
| "It is worth noting / It should be noted" | State the fact directly |
| "In this paper / This thesis proposes" | "The model" / "A greedy sequential algorithm was applied" |
| "Utilise" when "use" suffices | *use* |
| Three or more short contrasting sentences back to back | Merge into one or two |
| Vague hedges: *stuff*, *things*, *nice*, *very*, *quite*, *a lot of* | Precise counts or metrics (e.g. RMSE values, km thresholds) |
| "Shows" | *demonstrates*, *confirms*, *reveals* |
| "Gets" | *yields*, *produces*, *results in* |
| "Many studies" without a count | Name the review or give a number |

---

## Voice

Active voice for what the model or algorithm does:
> The greedy algorithm selects the grid cell that maximises the incremental gain in PM2.5 spatial coverage; each placement step adds exactly 129 newly covered cells.

Passive voice for procedures and what was done:
> A buffered spatial leave-one-out cross-validation protocol was applied to all 13 high-completeness SMHI reference stations.

Never use rhetorical questions or promotional framing.

---

## LaTeX conventions

- Percentages: 41\,\% (thin space before `%`)
- Multiplication: 2.3$\times$
- Units: 1.40\,µg\,m$^{-3}$, 64\,km, 6\,km
- Non-breaking space before units and cross-references: 35~km, Section~\ref{sec:label}, Figure~\ref{fig:label}, Table~\ref{tab:label}
- Abbreviations: expand at first use: Inverse Distance Weighting (IDW), Land-Use Regression (LUR), Spatial Leave-One-Out (SLOO), Design Science Research (DSR), Swedish Meteorological and Hydrological Institute (SMHI)
- Chemical formula: PM$_{2.5}$, NO$_{2}$
- Degree symbol: 59\,\textdegree N
- Scope disclaimer (add whenever a result could be read as a deployment recommendation): "The placement output is a data-driven research artefact and recommendation; it does not constitute an operational infrastructure plan."

---

## Section-by-section guidance

### Popular Science Summary (~250 words)

Purpose: Translate research for a general audience: media, policy makers, the public.
Register: Conversational but not chatty. No jargon without plain-language equivalent.
Structure: Problem people recognise → gap → analogy → solution → most striking finding → practical relevance.

AQ/IoT jargon to avoid — with plain alternatives:

| Jargon | Plain alternative |
|--------|-----------------|
| PM2.5 / PM$_{2.5}$ | fine airborne particles smaller than 2.5 micrometres |
| NO2 / NO$_{2}$ | nitrogen dioxide, a traffic exhaust gas |
| Reference monitoring station | an official government air quality monitor |
| Spatial estimation / interpolation | estimating air quality between measurement points |
| Buffered SLOO cross-validation | testing the model by hiding one station at a time |
| RMSE | average prediction error |
| Random Forest | a machine learning model |
| Land-use regression (LUR) | a map-based statistical model |
| Greedy sequential placement | a step-by-step method for choosing sensor locations |
| Accuracy-distance threshold | the maximum distance at which estimates are reliable |
| SMHI Luftwebb | Sweden's national air quality monitoring network |
| IoT sensor node | a small wireless air quality sensor |
| Coverage gap / unmonitored region | an area with no air quality data |
| EPSG:3035 | a standard map coordinate system |

> Pattern: "Most of us breathe outdoor air every day without knowing whether it is clean or polluted. Sweden has only 34 official air quality monitors across the entire country, and large areas have no measurement at all. [Analogy comparing the gap to something familiar]. This thesis builds a machine learning tool that estimates air quality between official stations and identifies exactly where new sensors are most needed. The most striking result: reliable estimates are possible within 64 km for fine particles but only 6 km for traffic pollution — meaning that a sensor network designed for one pollutant may be nearly blind to the other. The work does not constitute an operational deployment plan; it provides a data-driven recommendation for where sensors would have the greatest impact."

### Abstract (~250 words)

Purpose: Self-contained IMRAD summary. No citations, no figures.
Structure: Context + gap → method → results → contribution + scope disclaimer.

> Pattern: "This thesis [investigates/develops/evaluates] [artefact] using [method]. [Key procedural step]. [Key result with exact numbers]. The contribution is [what it adds]. The work does not [scope boundary]."

> Gap sentence pattern: "Land-use regression provides [capability], yet no empirical analysis has quantified how estimation accuracy degrades with distance from the nearest reference station and translated that relationship into a systematic sensor placement criterion."

> Finding sentence pattern: "Estimation error follows exponential decay for PM$_{2.5}$ (RMSE = 1.40$\cdot$exp(0.0099$\cdot d$)) and logarithmic growth for NO$_{2}$ (RMSE = 2.85 + 1.94$\cdot\ln(d)$), yielding reliable prediction distances of 64\,km and 6\,km respectively."

### Declaration of AI Usage

Purpose: Formal declaration of AI tool use, aligned with academic integrity requirements.
Register: Precise, formal, passive. Name tools and scope explicitly.

> Pattern: "Artificial intelligence tools were used in a supporting capacity during the preparation of this thesis. Claude Code (Anthropic) was used for Python scripting, LaTeX formatting assistance, and prose editing. All research design, methodological choices, data analysis, and interpretation were conducted independently by the author, who retains full academic responsibility for the content and conclusions of this thesis."

### Acknowledgements

Purpose: Express professional and personal gratitude.
Register: This is the only section where first-person pronouns (*I*, *my*) and emotional expression are permitted.

> Pattern: "I would like to thank [supervisor] for [specific contribution]. Data were accessed from the SMHI Luftwebb open data repository; I am grateful for the availability of this public infrastructure. [Personal dedication if appropriate]."

### Introduction (§1)

Open with a concrete public-health motivation sentence, not a definition.

> Avoid: "Air quality is a broad concept encompassing..."
> Better: "Ground-level concentrations of fine particulate matter (PM$_{2.5}$) and nitrogen dioxide (NO$_{2}$) are among the most well-documented contributors to respiratory and cardiovascular morbidity in European cities \cite{segersson_sweden_health_2017}."

> Gap pattern: "No empirical analysis has quantified how estimation accuracy from a sparse reference network degrades with distance and translated that relationship into a replicable sensor placement criterion applicable at national scale."

### Background and Related Work (§2)

Purpose: Synthesise; do not list. Show the progression of a research thread and where it stops.

> Synthesis pattern: "Hoek et al.\ \cite{hoek_lur_review_2008} establish land-use regression as the dominant framework for intra-urban exposure modelling; Eeftens et al.\ \cite{eeftens_escape_pm_2012} and Wang et al.\ \cite{beelen_escape_no2_2013} validate it across 20 European study areas; yet none of these studies quantifies how model accuracy degrades with distance from the nearest training station, making it structurally impossible to derive a data-driven sensor deployment criterion from their results."

### Methodology (§3)

> Justification pattern: "A buffered spatial leave-one-out protocol is appropriate because standard random cross-validation does not guarantee spatial independence between training and test sets in a geographically distributed station network \cite{roberts_spatial_cv_2017}; any performance figure derived from random partitioning cannot be interpreted as an estimate of accuracy at genuinely unmonitored locations."

> Criteria derivation pattern: "The reliable prediction distance threshold is defined as the distance at which expected RMSE reaches 50 per cent of the sample mean concentration: 2.63\,µg\,m$^{-3}$ for PM$_{2.5}$ and 6.43\,µg\,m$^{-3}$ for NO$_{2}$."

### Results (§5)

> Pattern: "Table~\ref{tab:results} summarises model performance under buffered SLOO cross-validation. Random Forest yields the lowest RMSE across both pollutants, outperforming the LUR benchmark and the IDW baseline. The ESCAPE cross-validation R$^{2}$ benchmarks of 0.71 for PM$_{2.5}$ \cite{eeftens_escape_pm_2012} and 0.83 for NO$_{2}$ \cite{beelen_escape_no2_2013} represent the standard against which these results are evaluated."

### Decay Analysis (§6)

> Pattern: "Figure~\ref{fig:decay} shows per-station RMSE as a function of distance to the nearest training station. Exponential decay provides the best fit for PM$_{2.5}$ (selected by AIC); RMSE reaches the criterion bound of 2.63\,µg\,m$^{-3}$ at 64\,km. For NO$_{2}$, logarithmic growth provides the best fit; the corresponding threshold is 6\,km, reflecting the sharp spatial gradients characteristic of traffic-sourced pollutants."

### Placement Artefact (§7)

> Pattern: "Table~\ref{tab:placement-coords} lists the 20 candidate locations in priority order. The first placement raises PM$_{2.5}$ spatial coverage from 10.9\,\% to 13.7\,\% of Swedish land area; all 20 placements combined raise coverage to 67.2\,\%."

> Scope disclaimer (include in §7): "The placement output is a data-driven research artefact and recommendation; it does not constitute an operational infrastructure plan and does not determine which specific sensor hardware should be purchased or deployed."

### Discussion (§8)

> Criterion assessment pattern: "Random Forest achieves a cross-validation R$^{2}$ of [X] for PM$_{2.5}$, [meeting/falling short of] the ESCAPE benchmark of 0.71 \cite{eeftens_escape_pm_2012}. The gap is consistent with the training network size: the ESCAPE study areas each comprised 20--40 monitoring sites, whereas the present analysis uses 13 stations."

> Limitation pattern: "Thirteen stations with a 5\,km exclusion buffer constitute the validation set; error estimates may be conservative in network-dense areas and optimistic in network-sparse areas where the buffer constraint is rarely triggered."

> Scope boundary pattern: "A station falling within the 64\,km PM$_{2.5}$ threshold does not mean air quality at that location meets regulatory limits; it means estimation from the existing network is reliable at that distance."

### Conclusion (§9)

> Contribution pattern: "The contribution of this thesis is a greedy sequential placement algorithm that operationalises empirically derived accuracy-distance thresholds to identify priority IoT sensor locations across Sweden, demonstrated on the SMHI reference station network. The work does not constitute a deployment plan and does not determine regulatory compliance."

> RQ answer pattern (one sentence per RQ):
> "RQ1: Random Forest achieves the lowest RMSE across both pollutants under buffered SLOO cross-validation, outperforming the LUR benchmark on PM$_{2.5}$ and the IDW baseline on both pollutants."
> "RQ2: PM$_{2.5}$ estimation remains reliable within 64\,km of the nearest station; NO$_{2}$ estimation degrades beyond 6\,km, reflecting the distinct spatial gradient behaviours of the two pollutants."
> "RQ3: Twenty sensor locations identified by the greedy sequential algorithm raise PM$_{2.5}$ spatial coverage from 10.9\,\% to 67.2\,\% of Swedish land area."

> Future work pattern: "Validation across a denser monitoring network or a different national context would allow the accuracy-distance relationship to be generalised beyond the sparse Swedish station configuration used here."

---

## Vocabulary and linking phrases

| Rhetorical purpose | Recommended phrases |
|--------------------|---------------------|
| Cause, effect, result | consequently, therefore, thereby, yields, gives rise to, results in, produces, manifests as |
| Contrast and limitation | yet, conversely, whereas, despite, albeit, by contrast, this limitation is inherent to |
| Addition and progression | furthermore, moreover, additionally, in turn, subsequently, building on this, in tandem with |
| Precision and emphasis | specifically, notably, principally, in particular, precisely, exclusively |
| Evaluation and validation | demonstrates, confirms, validates, corroborates, is consistent with, is evidenced by, outperforms |
| Gap and absence | lacks, omits, does not implement, makes no provision for, is structurally absent from, fails to |
| Scope and boundary | is outside the scope of, does not constitute, is not a substitute for, is bounded to, is deliberately excluded |

---

## Register patterns (copy-ready)

Model comparison (active):
> Random Forest outperforms land-use regression on RMSE for PM$_{2.5}$ under buffered SLOO cross-validation; the margin narrows for NO$_{2}$, where the sharp spatial gradients characteristic of traffic-sourced pollution reduce the advantage of land-use covariates.

Procedure (passive):
> A buffered spatial leave-one-out cross-validation protocol was applied to all 13 high-completeness stations, excluding all stations within 5\,km of the withheld location from the training set.

Empirical finding with quantification:
> Estimation error for PM$_{2.5}$ follows exponential decay (RMSE = 1.40$\cdot$exp(0.0099$\cdot d$)); the criterion bound of 2.63\,µg\,m$^{-3}$ is reached at 64\,km, beyond which physical sensor deployment is required.

Scope boundary:
> The contribution of this thesis is a data-driven placement recommendation; the work does not evaluate regulatory compliance and does not constitute an operational infrastructure plan.

Limitation with boundary:
> A 13-station training network constrains the generalisability of the findings; the accuracy-distance relationship is calibrated to the spatial distribution of the Swedish SMHI network and may not transfer to denser or differently distributed monitoring systems.

Gap statement:
> None of the reviewed studies quantifies how estimation accuracy degrades with distance from the nearest reference station; thresholds are reported as fixed performance figures with no spatial decay analysis, making it structurally impossible to derive a data-driven sensor deployment criterion from their results.

---

## Spelling reference

| American (banned) | British (correct) |
|-------------------|-------------------|
| operationalization | operationalisation |
| parameterized | parameterised |
| recognized | recognised |
| standardized | standardised |
| modeled | modelled |
| analyzed | analysed |
| formalized | formalised |
| initialized | initialised |
| characterized | characterised |
| optimized | optimised |
| behavior | behaviour |
| color | colour |
| analog | analogue |
| labeled | labelled |
| prioritized | prioritised |

---

## Correction examples

| Banned | Correct |
|--------|---------|
| PM2.5 and NO2 --- both regulated pollutants. | PM$_{2.5}$ and NO$_{2}$ are both regulated under the EU Ambient Air Quality Directive. |
| The threshold --- 64 km for PM2.5 --- was derived from IDW decay. | The threshold of 64\,km for PM$_{2.5}$ was derived from the IDW error-distance decay curve. |
| However, the algorithm does not guarantee optimality. | The greedy algorithm does not guarantee a globally optimal placement; it is a sequential heuristic that maximises incremental coverage gain at each step. |
| The model doesn't handle sub-daily data. | The model does not handle sub-daily concentration data; it is trained and evaluated on daily mean observations. |
| It should be noted that the 5 km buffer is a simplification. | The 5\,km exclusion buffer is justified by network structure rather than the empirical variogram range; this constraint is acknowledged as a limitation. |
| Many studies have used Random Forest for air quality. | Agbehadji and Obagbuwa \cite{agbehadji_ml_aq_review_2024} review machine learning applications to spatiotemporal air quality prediction, documenting consistent RMSE improvements over regression baselines across diverse geographic contexts. |
| I selected a 10 km grid for the placement analysis. | A 10\,km national grid was constructed over Sweden, yielding 4,588 land cells covering approximately 458,800\,km$^{2}$. |

---

## Quick review checklist

1. Any --- or Unicode —? Replace per the em dash table.
2. Any sentence starting with "However"? Rewrite.
3. Any -- used for something other than a numeric/alphabetic range? Replace.
4. Any contractions (*don't*, *can't*, *isn't*, *it's*)? Expand.
5. Any "It should be noted / It is worth noting"? Cut and restate directly.
6. Any personal pronouns in body text (*I*, *my*, *we*)? Replace with passive or structural agent.
7. Any vague quantifiers (*many*, *a lot of*, *very*)? Replace with exact figures (RMSE, km, %).
8. British spelling consistent? Check: *operationalisation*, *parameterised*, *behaviour*, *recognised*, *modelled*.
9. Percentages formatted as 41\,\%? Units with thin space: 64\,km, 1.40\,µg\,m$^{-3}$? Cross-references use non-breaking space: Section~\ref{...}?
10. Any result that could be read as a regulatory compliance or deployment claim? Add scope disclaimer.

---

## Troubleshooting

Em dash reappears after editing:
Run `grep -nE "---| — " writing/thesis.tex` to find all instances. The Unicode em dash (—) and the triple-hyphen (---) are both banned.

British spelling check:
Run `grep -inE "ize\b|ized\b|izing\b|behavior\b|color\b|labeled\b|modeled\b|analyzed\b" writing/thesis.tex` to catch American spellings.

Scope disclaimer missing:
Any sentence reporting a placement result near a deployment context needs a nearby disclaimer that the output is a research artefact, not an operational plan. Check the Abstract and Conclusion in particular.

---

## Boundaries

- Apply rules only to writing/ and thesis-related documents
- Do not apply to data/, scripts/, or any Python files
- Do not add comments to LaTeX code unless the reason is non-obvious
- Do not introduce rhetorical questions into thesis prose
- Do not claim the placement output constitutes an operational deployment plan
- Do not modify writing/references.bib without confirming the source
