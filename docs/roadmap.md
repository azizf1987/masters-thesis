# Roadmap

## Key dates

| Milestone | Target | Status |
|---|---|---|
| Phase 1 complete (§1 Introduction drafted) | 2026-06-12 | Done |
| Phase 2 complete (§2 Background drafted) | 2026-06-22 | Done |
| Phase 3 complete (§3 Methodology argued and drafted) | 2026-06-29 | Done (2026-06-05) |
| Phase 4 complete (data feasibility confirmed) | 2026-07-06 | Done (2026-06-18) |
| Phase 5 complete (unified feature matrix ready) | 2026-07-13 | Done (2026-06-22) |
| Phase 6 complete (RQ1 and RQ2 answered) | 2026-07-20 | Pending |
| Phase 7 complete (RQ3 answered; artefact produced) | 2026-07-24 | Pending |
| Phase 8 complete (full thesis compiled and submitted) | 2026-08-01 | Pending |
| Defense | TBD | — |

---

## Phase 0: Harness setup

**Status:** Done

- [x] Repo scaffold created
- [x] CLAUDE.md, AGENTS.md, docs/project.md chain established
- [x] Roadmap and project brief restructured to follow scientific research progression
- [x] Council POV files updated to remove predetermined technical assumptions
- [x] Working method documented in AGENTS.md

---

## Phase 1: Problem grounding and §1 Introduction

**Status:** Done

**Goal:** Establish why the problem is real and consequential, name the gap, and state the research claim in general terms. No method names in §1.

- [x] Write motivation and urban AQ context (public health burden; Swedish cities; PM2.5 and NO2)
- [x] Describe the SMHI monitoring network and its spatial coverage limitations
- [x] Articulate the IoT placement problem (why ad hoc deployment is insufficient)
- [x] State the research aim in general terms
- [x] State RQ1, RQ2, RQ3
- [x] Write scope and delimitations (pollutants, time window, geography, out-of-scope)
- [x] Write thesis structure paragraph with \ref{} cross-references

---

## Phase 2: Literature review and §2 Background and Related Work

**Status:** Done (two VERIFY citations still open — must resolve before submission)

**Goal:** Survey the field; identify what the literature leaves unresolved. End with gap statements that motivate the RQs. Phase 2 describes the landscape; it does not choose methods.

- [x] Write §2.1: Urban AQ monitoring and regulatory networks (SMHI context; spatial coverage problem; Swedish health evidence)
- [x] Write §2.2: Low-cost IoT sensor networks (capabilities, limitations, placement problem)
- [x] Write §2.3: Spatial estimation methods (IDW; LUR as European standard; ML approaches; spatial autocorrelation)
- [x] Write §2.4: Sensor placement optimization (existing approaches; outdoor vs. indoor gap)
- [x] Write §2.5: Research gaps (three gaps; one per RQ)
- [x] Add confirmed references to `writing/references.bib`
- [x] Verify `sweden_dispersion_2024` author list — resolved 2026-06-05
- [x] Verify `pso_node_deployment_2024` author list — resolved 2026-06-05

---

## Phase 3: Research design and §3 Methodology

**Status:** Done (2026-06-05)

**Full decision record:** `docs/decisions/phase3-methodology.md` — all options, trade-offs, council findings, and conditions

**Goal:** Argue every technical choice from the Phase 2 literature. Nothing assumed; everything earned.

### Prerequisites before writing §3

- [x] Add `valavi_blockcv_2019` to `writing/references.bib` — Valavi, Elith, Lahoz-Monfort, Guillera-Arroita (2019) Methods in Ecology and Evolution 10(2):225-232; doi:10.1111/2041-210X.13107
- [x] Verify `sweden_dispersion_2024` author list — Kilbo Edlund et al. (14 authors); full entry in references.bib; % VERIFY removed from thesis.tex
- [x] Verify `pso_node_deployment_2024` author list — Bhargavi, Varma, Hemalatha, Dilli; Sensors 24(19):6238; doi:10.3390/s24196238; % VERIFY removed from thesis.tex

### Phase 3 tasks

- [x] Choose and argue the spatial validation protocol → **Buffered SLOO** (council 2026-06-05)
- [x] Choose and argue the estimation model(s) for RQ1 → **Random Forest + LUR + IDW** (council 2026-06-05)
- [x] Choose and argue the decay analysis approach for RQ2 → **error-distance curve fitting; AIC/BIC selection** (council 2026-06-05)
- [x] Choose and argue the placement optimization approach for RQ3 → **greedy sequential** (council 2026-06-05)
- [x] Define evaluation metrics → RMSE, MAE, R², decay threshold, real-world DSR criterion (council 2026-06-05)
- [x] Invoke council before finalizing methodological commitments (done 2026-06-05)
- [x] Write §3.1 DSR framing: Peffers six-phase mapping as a table
- [x] Write §3.2 Spatial estimation strategy: RF argument; feature set (~10-15 covariates named); IDW/LUR baselines
- [x] Write §3.3 Spatial validation: buffered SLOO; why buffer required; why k-fold excluded (Roberts 2017)
- [x] Write §3.4 Accuracy-distance analysis: method for RQ2; urban/rural confound strategy named
- [x] Write §3.5 Sensor placement: greedy sequential argued from RQ2 connection; PSO acknowledged and rejected; suboptimality acknowledged
- [x] Write §3.6 Evaluation metrics: RMSE, MAE, R², decay threshold, real-world criterion
- [x] Write §3.7 Validity, reliability, and ethical considerations

### §3 conditions checklist (from council — all must be met before §3 is finalised)

- [x] Buffered SLOO stated; buffer radius noted as Phase 4 dependency; Valavi/Meyer cited
- [x] Standard k-fold explicitly excluded; Roberts (2017) cited
- [x] Random Forest argued from data environment (sparse spatial locations, mixed features)
- [x] LUR and IDW benchmarks included; LUR framed as the standard to beat
- [x] Feature set named and parsimonious design principle stated (~10-15 covariates)
- [x] PM2.5 and NO2 modelled separately; stated explicitly
- [x] Decay confound (urban/rural) named and analytical strategy stated
- [x] Greedy placement argued from RQ2 connection; suboptimality acknowledged
- [x] At least one real-world DSR evaluation criterion named
- [x] Peffers six-phase DSR mapping written as a table

### Council decisions summary (2026-06-05)

**Validation: Buffered SLOO.** Pure SLOO produces optimistic errors in clustered networks (Stockholm, Gothenburg, Malmö). Buffer radius from Phase 4 inter-station distance audit. Valavi et al. (2019) or Meyer et al. (2021) as citation. Standard k-fold excluded (Roberts 2017).

**Model: RF + LUR + IDW.** Random Forest as sole primary ML model. LUR (ESCAPE R² 0.54-0.89) and IDW as required benchmarks. No second ML model; the contribution is spatial error behavior, not model comparison. Feature set parsimonious: ~10-15 covariates for ~50-100 training stations.

**Pollutants: fully separate.** PM2.5 and NO2 modelled, validated, and decay-analysed independently. Pooling is a domain error. NO2 gradients are sharp at 500 m-2 km; PM2.5 gradients are smooth at 5-20 km. Thresholds will differ.

**Decay: error-distance curve fitting.** Per-station RMSE vs. distance to nearest training station. Fit log, power, exponential; select by AIC/BIC. Urban/rural confound must be addressed (stratified analysis or named sensitivity test). Distance metric: Euclidean (acknowledged simplification for NO2). Threshold criterion defined in Phase 5 EDA.

**Placement: greedy sequential.** Directly operationalises the RQ2 decay threshold. PSO excluded: requires demonstrating multimodal landscape pre-Phase 6; adds complexity not central to the contribution. Greedy suboptimality acknowledged in §3.

**DSR criterion.** At least one real-world evaluation criterion in §3.5: proportion of Swedish urban area within reliable estimation range, and number of currently unmonitored regions transitioning to served. (Updated from Skåne to national scope 2026-06-18.)

---

## Phase 4: Data feasibility audit

**Status:** Done (2026-06-18)

**Goal:** Confirm the Phase 3 methodology is executable with the available data. Can adjust scope; cannot adjust methodology without returning to Phase 3.

- [x] Pull SMHI Luftwebb station inventory: count PM2.5 and NO2 stations nationally (2026-06-17)
- [x] Check data completeness by station and year (2020-2024); apply 90% threshold (2026-06-17)
- [x] Confirm SMHI metobs API access; write and run meteorological covariates download script (2026-06-18)
- [x] Download and verify CORINE Land Cover for Sweden (2026-06-18)
- [x] Download EU-DEM, clip to Sweden at 100m (2026-06-18)
- [x] Confirm population density grid source and resolution (Eurostat GEOSTAT JRC 2018) (2026-06-18)
- [x] Establish inter-station distance distribution → set buffered SLOO exclusion radius (preliminary: 5 km) (2026-06-18)
- [x] **Decision point:** Skåne PM2.5 coverage too sparse (1 passing station) → case study expanded to all Sweden (2026-06-18)
- [x] **Decision point:** National station count below 40-50 threshold (13 passing, 34 raw) → §3 updated; supervisor discussion required before any time period extension
- [x] Document audit results in `docs/data-audit.md` (2026-06-18)

---

## Phase 5: Data engineering

**Status:** Done (2026-06-22)

- [x] Ingest SMHI air quality records (2020-2024): PM2.5 and NO2 daily averages per station
- [x] Pull and align meteorological covariates from metobs API (temperature, wind, humidity)
- [x] Extract CORINE land-use features per station (500 m and 1 km buffers; 9 class groups; 18 features)
- [x] Add DEM topographic features (elevation_m; terrain_rough_m within 1 km buffer)
- [x] Add population density grid values (pop_1km, pop_5km)
- [x] Compute inter-station distance matrix (34 × 34 Haversine; done in Phase 4)
- [x] Apply 90% completeness filter: 13 stations pass (11 for both pollutants; 2 pass only NO2)
- [x] Flag 2020-2021 COVID-19 period (covid_period binary column; sensitivity analysis planned Phase 6)
- [x] Run EDA: distributions, negative clipping (12 values), precipitation imputation (15,236 values, 31.6%), empirical variogram
- [x] Finalise SLOO buffer: 5 km confirmed (variogram raw range 150-200 km is operationally impossible; buffer justified by network structure)
- [x] Write §4 (Data Sources and Feature Engineering) — all 7 subsections drafted in `writing/thesis.tex`
- [ ] Decay threshold criterion (specific error bound): deferred to Phase 6 after decay curve fitting

**Output:** `data/processed/feature_matrix_clean.csv` — 48,283 rows × 37 columns (10.3 MB)

**Key findings:**
- Station count: 13 passing 90% threshold nationally; 7 Swedish regions unmonitored
- SLOO buffer: 5 km final (excludes 24 within-city pairs; minimum training set 29 stations)
- Precipitation: 31.6% missing, imputed with monthly station climatological mean; precip\_observed flag added
- Negative AQ values: 12 clipped to 0
- COVID signal: mean NO2 13.82 µg/m³ (2020-2021) vs 12.34 µg/m³ (2022-2024); likely station composition effect

---

## Phase 6: Empirical work (RQ1 and RQ2)

**Status:** Pending (blocked by Phase 5)

- [ ] Implement buffered SLOO validation protocol (buffer radius from Phase 4)
- [ ] Train and evaluate Random Forest — PM2.5
- [ ] Train and evaluate Random Forest — NO2
- [ ] Compute RMSE, MAE, R² per pollutant
- [ ] Compare RF against IDW baseline and LUR benchmarks
- [ ] Run accuracy-distance analysis: per-station error vs. distance to nearest training station
- [ ] Address urban/rural confound (stratified analysis or sensitivity test per §3.4 strategy)
- [ ] Fit decay curves (log, power, exponential) per pollutant; select by AIC/BIC
- [ ] Identify reliable prediction distance threshold per pollutant
- [ ] Save all result tables and figures
- [ ] Write §5 (estimation results; RQ1 answer)
- [ ] Write §6 (decay analysis; RQ2 answer)

---

## Phase 7: Placement artefact (RQ3)

**Status:** Pending (blocked by Phase 6)

- [ ] Construct national uncertainty grid from Phase 6 decay results (all Sweden, 10 km grid)
- [ ] Implement greedy sequential placement algorithm
- [ ] Run placement optimization; produce prioritized deployment coordinates
- [ ] Generate coverage uncertainty heatmaps (before and after placement)
- [ ] Evaluate artefact against real-world criterion named in §3.5
- [ ] Write §7 (artefact design, case study, placement output; RQ3 answer)

---

## Phase 8: Thesis synthesis and submission

**Status:** Pending (blocked by Phase 7)

- [ ] Write §8 Discussion (explicit RQ answers; comparison with related work; limitations; implications)
- [ ] Write §9 Conclusion (summary; contributions; future work)
- [ ] Write Abstract (~200 words: problem, aim, method, contribution)
- [ ] Write Popular Science Summary (1-2 pages; non-technical)
- [ ] Write Declaration of AI Usage
- [ ] Write Acknowledgements
- [ ] Full formatting check: margins (30 mm), line spacing, figure captions, table titles, reference list
- [ ] Council review on §8 Discussion and §9 Conclusion
- [ ] Compile LaTeX; resolve all warnings; confirm bibliography complete and correctly formatted
- [ ] Resolve all % VERIFY citations before submission
- [ ] Submit by 2026-08-01

---

## What is decided

| Choice | Decision | Decided in |
|---|---|---|
| Spatial validation protocol | Buffered SLOO | Phase 3 council (2026-06-05) |
| Primary ML model | Random Forest | Phase 3 council (2026-06-05) |
| Required benchmarks | LUR (ESCAPE) and IDW | Phase 3 council (2026-06-05) |
| Pollutant handling | Separate models and analyses per pollutant | Phase 3 council (2026-06-05) |
| Placement optimization | Greedy sequential | Phase 3 council (2026-06-05) |
| Kriging / geostatistics | Not in scope | Phase 3 council (2026-06-05) |
| Case study geographic scope | All Sweden (national) | Phase 4 data audit (2026-06-18) |
| Station count (final) | 34 raw, 13 passing quality filters | Phase 4 data audit (2026-06-17) |

## What is still open

| Choice | Decided in |
|---|---|
| Buffered SLOO exclusion radius | **Preliminary: 5 km** (set Phase 4, 2026-06-18); finalize in Phase 5 after variogram |
| Decay threshold criterion (specific error bound) | Phase 5 (EDA) |
| COVID-19 period treatment | Phase 5 (EDA) |
| Time period extension (2017-2018) | Requires supervisor discussion; station count (13 passing) is below the 40-50 threshold agreed in 2026-06-15 session |
| §3.2 station count text (still says "50-100") | Fix before next draft |
| §3.4 urban/rural stratification — rural n=1 | Replace with traffic vs. background contrast; fix before next draft |

## What is anchored (from approved proposal)

- Pollutants: PM2.5 and NO2
- Data period: 2020-2024
- Primary data sources: SMHI Luftwebb, SMHI metobs API, CORINE Land Cover
- Geographic scope: Sweden nationally for both model training and case study (Skåne-only scope ruled out in Phase 4 audit 2026-06-18)
- DSR framing: required; Peffers (2007) six phases must be mapped in §3
- Validation principle: spatial CV required; standard k-fold not defensible
- Submission: 2026-08-01

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Buffered SLOO leaves too few training stations per fold | High | Phase 4 distance audit sets the buffer; if too restrictive, use adaptive buffer |
| Station count very low (13 passing) | High | §3.2 updated; buffered SLOO adaptive fallback added; supervisor discussion on time period extension pending |
| Urban/rural confound makes decay curve undefensible | High | §3.4 names the strategy; Phase 6 executes it |
| COVID-19 period contaminates 2020-2021 data | Medium | Flag in Phase 5; sensitivity analysis |
| Phases 5-6 run over time | High | Phase 7 artefact is most compressible; simplify placement approach if needed |
