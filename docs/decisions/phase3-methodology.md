# Phase 3 Methodology Decisions — Council Record

**Session date:** 2026-06-05
**Status:** Proceed with conditions (no blocks, four pauses resolved into eight conditions)
**Next use:** Read this before writing §3. Every condition below must appear as an explicit argument in §3.

---

## Decision 1: Spatial validation protocol

**What was decided:** Buffered Spatial Leave-One-Out CV (buffered SLOO). Not pure SLOO. Not geographic block CV. Not standard k-fold.

### Options considered

| Option | Verdict | Reason |
|---|---|---|
| Standard k-fold | Excluded | Indefensible for spatially autocorrelated data (Roberts 2017). Training and test sets share spatial proximity; error is optimistically biased. |
| Geographic block CV | Not chosen | Appropriate for large, well-distributed training sets. SMHI network is too sparse and unevenly distributed to partition into balanced blocks. |
| Pure SLOO | Not chosen | Holds out one station; trains on all others. Insufficient when the network has urban clusters: nearby stations remain in training and leak spatial information to the test point. Produces optimistically biased errors. |
| **Buffered SLOO** | **Chosen** | Holds out one station AND excludes all training stations within an exclusion buffer radius. Prevents spatial leakage. Directly simulates the real-world prediction task (estimating at a genuinely unmonitored location). Defensible for sparse fixed-station networks. |

### Key trade-off
Pure SLOO is simpler but biased in clustered networks. Buffered SLOO is the correct method but reduces the effective training set size for each fold: stations within the buffer are excluded. With a sparse network (~50-100 stations), a large buffer can leave very few training points. The buffer radius must be chosen carefully.

### Conditions for §3
- State that the validation protocol is buffered SLOO, not pure SLOO
- Buffer radius to be set after Phase 4 confirms the inter-station distance distribution; minimum = median nearest-neighbour distance in the SMHI network
- Cite Valavi et al. (2019) [blockCV] or Meyer et al. (2021) [CAST] as the methodological reference for buffered SLOO; add to `writing/references.bib`
- Explicitly state why standard k-fold is excluded (Roberts 2017 is the citation)

### Why this matters for the argument chain
The SLOO errors are the input to RQ2 (decay analysis). Biased errors produce a biased decay curve, which produces a biased distance threshold, which mis-prioritizes sensor placement in RQ3. The validation protocol is load-bearing for the entire thesis argument.

---

## Decision 2: Estimation model for RQ1

**What was decided:** Random Forest as the primary ML model. LUR and IDW as required benchmarks. No second ML model unless it carries its own argumentative role.

### Options considered

| Option | Verdict | Reason |
|---|---|---|
| IDW (Inverse Distance Weighting) | Required baseline | No covariates; purely distance-based interpolation. Well-understood floor for spatial estimation. Required to contextualize LUR and ML gains. |
| LUR (Land-Use Regression) | Required benchmark | The established European peer-reviewed standard (ESCAPE studies; Hoek 2008; Eeftens 2012; Beelen 2013). R² 0.54-0.89 for NO2 in European cities. Any ML approach must be evaluated against LUR, not just against IDW. |
| **Random Forest** | **Primary ML model** | Handles mixed feature types (categorical land use + continuous meteorological + topographic); robust to irrelevant features; no distributional assumption; well-supported for spatial AQ estimation (Chen 2021; Agbehadji 2024). Appropriate for 50-100 training locations with ~10-15 covariates. |
| Gradient Boosting / XGBoost | Not chosen | Higher potential accuracy but more sensitive to hyperparameter tuning and more prone to overfitting on sparse training sets. Defensible as a comparison but adds a results table without adding to the thesis's central argument (which is about spatial error behavior, not model selection). |
| Neural networks / hybrid (SwinLSTM-Kriging) | Excluded | Requires significantly more training locations than the SMHI network provides. Harder to argue at master's level with sparse data. The spatial error behavior contribution does not require a deep learning model. |

### Key trade-off
Adding a second ML model (RF vs. XGBoost) gives a broader comparison but shifts the thesis toward "which model is best" rather than "how does spatial error behave with distance." The thesis's contribution is the latter. One ML model plus two benchmarks is the cleaner argument.

### Conditions for §3
- State Random Forest as the primary ML model; argue from: mixed feature types, sparse training set, no distributional assumption
- Retain LUR and IDW as required benchmarks; argue why LUR is the standard the ML approach must beat (ESCAPE citations)
- Feature set: state the parsimonious design principle explicitly; approximately 10-15 covariates for 50-100 training stations to avoid overfitting
- Candidate features to name in §3: land-use class proportions within 100 m, 500 m, 1 km buffers; road length within 100 m and 500 m; elevation; terrain roughness; population density within 1 km; wind speed, wind direction, temperature, precipitation (from SMHI metobs)
- Models run separately for PM2.5 and NO2 (see Decision 4 below)

---

## Decision 3: Accuracy-distance decay analysis for RQ2

**What was decided:** Per-station RMSE vs. distance to nearest training station; fit candidate decay curves (logarithmic, power law, exponential); select functional form by AIC/BIC. Address the urban/rural confound explicitly.

### Options considered

| Option | Verdict | Reason |
|---|---|---|
| **Error-distance curve fitting** | **Chosen** | Compute per-station prediction error (RMSE or MAE) from buffered SLOO. Plot against distance to nearest training station. Fit three candidate functional forms. Select by AIC/BIC. Direct empirical answer to RQ2. |
| Variogram-based decay | Not chosen | Fits a semivariogram to model residuals. Appropriate for Kriging-style analysis; produces a spatial autocorrelation range. Does not directly answer RQ2 as stated (accuracy degradation vs. distance). Better suited if geostatistics were the core method. |
| Distance-band aggregation | Not chosen | Bins stations into distance ranges; computes mean error per band. Simpler but loses station-level variation and makes curve fitting less rigorous. |

### Key trade-off
The error-distance relationship may confound two phenomena: (a) genuine distance-based accuracy degradation (the target signal); (b) urban/rural differences in land-use complexity, emission heterogeneity, and feature-model generalizability. A station 5 km from its nearest neighbour in urban Gothenburg and a station 5 km from its nearest neighbour in rural Norrland are not equivalent data points. If this confound is not addressed, an examiner can attribute the decay to the urban/rural effect rather than to distance.

### Conditions for §3
- Name the potential confound (urban cluster density vs. rural isolation) explicitly
- State the analytical strategy for addressing it: stratified analysis (urban vs. rural station subsets), covariate control, or a named sensitivity analysis comparing decay curves for the two subsets
- Decay analyses run separately for PM2.5 and NO2 (thresholds will likely differ; PM2.5 has a larger spatial footprint than NO2)
- State the distance metric: Euclidean distance to nearest training station; acknowledge that for NO2 (traffic-source-dominated), road-network distance would be more physically meaningful but is used here for simplicity; justify the simplification
- Name the threshold definition criterion: the distance at which RMSE exceeds a stated bound (e.g., WHO guideline tolerance or a pre-defined relative error threshold); the specific bound is set in Phase 5 after EDA

---

## Decision 4: PM2.5 and NO2 separation

**What was decided:** PM2.5 and NO2 are modelled independently throughout. Separate feature extraction, separate model training, separate spatial validation, separate decay analyses, separate decay thresholds.

### Why this is a separate decision
This was not framed as a choice in the original plan; it emerged from the council as a domain accuracy requirement. Pooling both pollutants into a single model or a single decay analysis is a domain error.

### The physical basis
| Pollutant | Primary source | Spatial scale | Gradient behavior |
|---|---|---|---|
| NO2 | Traffic combustion | 500 m to 2 km | Sharp gradients near roads; drops rapidly with distance from source |
| PM2.5 | Mixed (traffic, industry, regional transport) | 5 to 20 km | Smoother gradients; more regionally homogeneous |

The decay threshold for NO2 will be shorter (reliable estimation range smaller) than for PM2.5. A single pooled threshold would be misleading for both pollutants and would not be defensible to an examiner familiar with air quality science.

### Conditions for §3
- State explicitly that models are trained, validated, and evaluated separately for PM2.5 and NO2
- Acknowledge in §3.2 that the spatial scales differ and that separate decay thresholds are expected
- All results tables and figures in §§5-6 must present PM2.5 and NO2 separately

---

## Decision 5: Placement optimization for RQ3

**What was decided:** Greedy sequential placement. Not PSO. Not geometric coverage optimization.

### Options considered

| Option | Verdict | Reason |
|---|---|---|
| **Greedy sequential** | **Chosen** | At each step, place the next sensor at the location that maximally reduces total estimation uncertainty below the decay threshold. Directly operationalizes the RQ2 output. Transparent optimality condition. Directly connected to the DSR artefact design. |
| Particle Swarm Optimization (PSO) | Not chosen | Population-based global optimizer. Appropriate when the objective function is multimodal (many local optima). The argument for PSO requires demonstrating that the Skåne placement landscape is multimodal, which cannot be established before Phase 6 produces the uncertainty surface. PSO also requires fitness function design and parameter tuning, which adds complexity without a clear contribution gain for this thesis. The §2.4 literature (Gupta 2023; pso_node_deployment_2024) established PSO as a candidate; it does not establish it as the correct choice for this specific application. |
| Voronoi / geometric coverage | Not chosen | Does not use the empirical uncertainty surface from Phase 6. Placement would be data-free, which contradicts the thesis's claim that deployment should be evidence-based. |

### Key trade-off
Greedy is suboptimal in theory (it cannot backtrack; early placements constrain later ones). PSO can find globally better solutions if the landscape is multimodal. However, the thesis's contribution is not "optimally placed sensors" but "evidence-based guidance for sensor placement." Greedy is more transparent, directly connected to the RQ2 output, and produces a result that a municipality can understand and reproduce. PSO would add a results section on convergence and parameter sensitivity that is not the thesis's contribution.

### Conditions for §3
- Argue greedy placement from the direct connection to RQ2: the uncertainty surface is constructed from the decay threshold; greedy is the natural operationalization of coverage maximization on that surface
- Acknowledge PSO as an alternative and state explicitly why greedy is preferred: transparency of decisions, direct connection to empirical findings, DSR requirement that the artefact is explainable to practitioners
- Acknowledge the suboptimality of greedy and frame it as acceptable given the thesis's contribution scope

---

## Decision 6: DSR artefact evaluation criterion

**What was decided:** At least one real-world criterion must be named in §3 for the artefact evaluation (Peffers Evaluation phase). Internal model metrics (RMSE, MAE) alone are not sufficient for a DSR claim.

### Why this was flagged
DSR requires that the artefact be evaluated against criteria that reflect the real problem, not only internal model performance. Naming only RMSE and MAE as evaluation criteria makes the DSR framing a label rather than a methodology.

### Candidate real-world criteria for §3
- Proportion of Skåne urban area brought within reliable estimation range after placement (percentage of urban land area within the decay threshold of at least one sensor)
- Number of currently unmonitored municipalities in Skåne that would fall within reliable estimation range
- Reduction in maximum unmonitored gap distance (largest distance from any urban grid point to the nearest sensor, before vs. after placement)

### Condition for §3
Name at least one of the above criteria explicitly in §3.5 as the primary evaluation criterion for the placement artefact. RMSE and MAE remain the evaluation metrics for the estimation model (RQ1); the real-world criterion is the evaluation metric for the artefact (RQ3).

---

## Evaluation metrics summary

| Metric | Used for | Notes |
|---|---|---|
| RMSE | RQ1 model accuracy | Primary; penalizes large errors; units in µg/m³ (interpretable) |
| MAE | RQ1 model accuracy | Secondary; robust to outliers; complements RMSE |
| R² | RQ1 goodness of fit | Required for LUR benchmark comparison (ESCAPE literature uses R²) |
| Decay threshold distance | RQ2 | Distance at which RMSE exceeds stated bound; separate per pollutant |
| Real-world coverage criterion | RQ3 artefact | One criterion from the list above; named in §3 |

---

## References to add to `writing/references.bib`

| Key | Work | Required for |
|---|---|---|
| valavi_blockcv_2019 | Valavi et al. (2019) blockCV: an R package for generating spatially or environmentally blocked cross-validation data. *Methods in Ecology and Evolution* | Buffered SLOO citation in §3.3 |
| meyer_cast_2021 | Meyer et al. (2021) Predicting into unknown space? Estimating the area of applicability of spatial prediction models. *Methods in Ecology and Evolution* | Alternative buffered SLOO citation |

Add one of these (or both). Verify author lists and years before adding.

---

## Open threads from this council session

- [ ] Verify `sweden_dispersion_2024` author list (% VERIFY in §2.1)
- [ ] Verify `pso_node_deployment_2024` author list (% VERIFY in §2.4)
- [ ] Add valavi_blockcv_2019 or meyer_cast_2021 to `writing/references.bib`
- [ ] Phase 4 must establish inter-station distance distribution to set the exclusion buffer radius
- [ ] Decay threshold definition criterion (specific bound) set in Phase 5 after EDA

---

## What goes in the thesis vs. what stays here

| Content | Location |
|---|---|
| The argued conclusions (SLOO with buffer, RF, greedy, separate pollutants) | §3 of the thesis |
| The options considered and rejected | This document only |
| The council deliberation and seat findings | This document only |
| The trade-offs | This document only (referenced implicitly by the §3 arguments) |
| The eight conditions as a checklist | This document (use as a §3 writing checklist) |
