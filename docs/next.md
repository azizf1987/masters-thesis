# next.md -- current state and what's next

## Where we are (as of 2026-06-22, session 3)

Phases 1-5 complete. §§1, 2, 3, and 4 drafted in `writing/thesis.tex`. Analytical dataset ready. Next phase is Phase 6 (empirical modelling).

**§4 covers (written this session):**
- §4.1 Air Quality Observations: SMHI Datavärdskap Luft; 34 stations, 13 pass 90% filter; 2020-2024; station type distribution
- §4.2 Meteorological Covariates: SMHI metobs API; 5 parameters; aggregation to daily; circular mean wind direction; known gaps (temperature: 3 stations; precipitation: 15 stations)
- §4.3 Land-Use Features: CORINE CLC 2018 at 100m; 9 class groups; 500m and 1km buffers; 18 features; ESCAPE comparability stated
- §4.4 Topographic Features: EU-DEM v1.1 at 100m; elevation and terrain roughness (1km buffer SD)
- §4.5 Population Density: JRC GEOSTAT 2018; pop_1km and pop_5km
- §4.6 Feature Matrix Construction: 48,283 rows × 37 columns; Table 1 with full column inventory; covid_period flag
- §4.7 Data Quality: 12 negative values clipped; precipitation imputation (15,236 values, 31.6%); station-level completeness filter confirmed (Göteborg Haga 69%, Östersund 79% fail)

**Five new bibliography entries added to `writing/references.bib`:** smhi_luftwebb, smhi_metobs, corine_clc_2018, eudem_v11, jrc_geostat\_2018 (all marked % VERIFY in thesis.tex)

**Variogram findings (Phase 5 EDA):**
- Raw variogram range: 150-200 km for NO2; similar for PM2.5
- This range is operationally impossible given Bredkälen's nearest neighbour is 177 km
- SLOO buffer confirmed at 5 km: justified by network structure (excludes 24 within-city pairs); sensitivity analysis (10km, 20km) planned in Phase 6
- Minimum training set per fold: 29 stations (5-station Stockholm cluster held out)

**Cleaned feature matrix:** `data/processed/feature_matrix_clean.csv` (48,283 rows × 37 columns, 10.3 MB)

---

## Where we were (as of 2026-06-18, session 2)

Phases 1, 2, and 3 complete. §§1, 2, and 3 drafted in `writing/thesis.tex`.

**§1 covers:**
- Urban AQ public health burden in Swedish cities (cited: Molnar et al. 2017)
- SMHI network structure and spatial coverage limitations
- The IoT placement problem: why ad hoc deployment is insufficient
- Research aim in general terms; no method commitments
- RQ1, RQ2, RQ3 as numbered list
- Scope and delimitations (PM2.5/NO2, 2020-2024, Sweden nationally for both training and case study, out-of-scope)
- Thesis structure paragraph with \ref{} cross-references to all sections

**§2 covers:**
- §2.1: Urban AQ monitoring and regulatory networks (SMHI Luftwebb, Swedish health evidence, spatial coverage gap)
- §2.2: Low-cost IoT sensor networks (capabilities, limitations, the placement problem as gap)
- §2.3: Spatial estimation methods (IDW baseline; LUR as established European standard with ESCAPE benchmarks; ML approaches; hybrid approaches; spatial autocorrelation concern and Roberts 2017)
- §2.4: Sensor placement optimization (PSO, outdoor application gap; greedy alternatives noted)
- §2.5: Research gaps (three named gaps, one per RQ)

**§3 covers:**
- §3.1: DSR framing; Peffers six-phase mapping as a table
- §3.2: Spatial estimation strategy (pollutant separation; feature set ~10-15 covariates named; RF argued; LUR and IDW as benchmarks)
- §3.3: Spatial validation protocol (buffered SLOO; why buffer required; k-fold excluded; buffer radius deferred to Phase 4)
- §3.4: Accuracy-distance analysis (error-distance curve fitting; AIC/BIC; urban/rural confound; stratified sensitivity analysis)
- §3.5: Sensor placement optimization (greedy sequential; argued from RQ2 connection; PSO acknowledged and rejected; suboptimality acknowledged)
- §3.6: Evaluation metrics table (RMSE, MAE, R², decay threshold, two real-world DSR criteria)
- §3.7: Validity, reliability, and ethical considerations

**References: no unverified citations remain in the thesis.**
All % VERIFY flags resolved this session: sweden_dispersion_2024 (Kilbo Edlund et al. 2024) and pso_node_deployment_2024 (Bhargavi et al. 2024). valavi_blockcv_2019 added (Valavi et al. 2019, Methods in Ecology and Evolution).

## Session summary (2026-06-15)

This session covered four areas: supervisor preparation, expert feedback responses, data source mapping, and the first data download attempt.

### Thesis written sections status
Phases 1, 2, and 3 complete. §§1, 2, and 3 drafted. No unverified citations remain.

### Expert feedback received and actioned (2026-06-15)

Two rounds of expert critique were received. The following actions were identified:

| Issue | Action | Status |
|---|---|---|
| Appendix C still titled "PSO Placement Parameters" | Delete or rewrite as greedy parameters | **Must fix immediately — contradiction in document** |
| Distance metric not named in §3.4 | Add "Euclidean distance" + justification sentence | Before next draft |
| COVID-19 strategy vague | Add sensitivity analysis strategy to §3.4: binary COVID indicator covariate + two-model comparison (2020-2024 vs 2022-2024) | Before next draft |
| Seasonality not addressed in decay model | Add seasonal stratification (winter/summer) to Phase 6 plan; acknowledge in §3.4 | Phase 6 |
| ESCAPE benchmarks outdated (2012-2013) | Add 1-2 recent northern European LUR studies (post-2018) to §2.3 | Before next draft |
| IoT infrastructure constraints ignored | Add scope boundary sentence to §3.5 and §8: output is candidate locations, not deployment specs | Before next draft |
| Sample size justification implicit | Add ESCAPE precedent sentence to §3.2 explicitly | Before next draft |
| Daily averages scope not stated | Add delimitation sentence to §1 and §8 | Before next draft |
| PSO not acknowledged as future work | Add one sentence to §3.5 | Before next draft |

**Most urgent:** Fix Appendix C PSO contradiction before sharing with anyone.

### COVID-19 strategy (agreed in session)

Concrete approach for §3.4:
1. Add binary covariate: COVID_period = 1 for 2020-2021, 0 for 2022-2024. RF model learns the anomaly rather than treating those years as normal.
2. Sensitivity analysis: run full model on 2020-2024, then re-run on 2022-2024 only. Compare decay curves. If similar, COVID period is not distorting results. If divergent, 2022-2024 model becomes primary.

### Data source mapping (confirmed in session)

| Data | Source | URL | Status |
|---|---|---|---|
| PM2.5 + NO2 daily readings | SMHI Datavärdskap Luft | datavardluft.smhi.se/portal/concentrations-in-air | Partially downloaded — see below |
| Weather covariates | SMHI metobs API | opendata-download-metobs.smhi.se/api | Confirmed accessible; script needed |
| CORINE Land Cover | EU Copernicus | land.copernicus.eu/pan-european/corine-land-cover | Not yet downloaded |
| Terrain height (DEM) | Lantmäteriet | lantmateriet.se (Höjddata product) | Not yet downloaded |
| Population density | Eurostat GEOSTAT | ec.europa.eu/eurostat GEOSTAT grid | Not yet downloaded |

### Air quality data download — first attempt (2026-06-15)

Two ZIP files uploaded and inspected. Both contained the same 11 stations. Assessment:

| Station | Type | Pollutants | Completeness | Verdict |
|---|---|---|---|---|
| Bredkälen | Rural Background | NO2 + PM2.5 | 93.7% | PASS |
| Norunda Stenen | Rural-Regional | NO2 | 97.5% | PASS |
| Hallahus | Rural-Regional | NO2 | 98.5% | PASS |
| Burlöv Församlingshemmet | Urban Background | PM2.5 | 92.8% | PASS |
| Umeå Förskolan Uven | Urban Background | PM2.5 | 91.8% | PASS |
| Stockholm Olaus Petri | Urban Background | PM2.5 | 63.5% | FAIL — below 90% |
| Piteå Prästgårdsgatan | Urban Traffic | NO2 | 81.2% | FAIL — short + incomplete |
| Köping Glasgatan | Urban Traffic | NO2 | 96.5% | FAIL — 2020 only |
| Stockholm Valhallavägen 81 | Urban Background | PM2.5 | 93.3% | FAIL — ends Sep 2022 |
| Kramfors Limstagatan | Urban Traffic | NO2 | 97.8% | FAIL — only 6 months |
| Råö | Rural Background | NO2 + PM2.5 | 22.8% | FAIL — almost no data |

**Problem:** 11 stations is far too few. The portal exported a subset, not the full national network. The thesis needs 50-100 stations.

**Solution agreed:** Use the SMHI metobs-style API (or the Datavärdskap Luft bulk download) to pull all stations programmatically. A Python script needs to be written to do this.

### Time period discussion (2026-06-15)

Question raised: should the study period be extended beyond 2020-2024 to capture more stations (including those that stopped before 2020)?

Decision framework agreed:
1. First: run the full API download for 2020-2024 and count actual stations
2. If 60+ stations nationally → keep 2020-2024, no change
3. If fewer than 40-50 stations → consider modest extension to 2017-2018 to bring in closed stations that add spatial coverage
4. Extension is only justified if it adds new station LOCATIONS, not just more years of the same locations
5. NO2 extension carries higher risk (emission regime changed pre/post Euro 6); PM2.5 extension is lower risk
6. Any extension requires supervisor discussion before implementing

## Data status (as of 2026-06-18)

### Air quality data: collected
- 34 unique stations with both PM2.5 and NO2 (hourly, 2020-2024)
- 13 pass quality filters (≥90% completeness, ≥80% period coverage)
- Regional breakdown: Stockholm (11 raw / 6 pass), Uppsala (2/2), Östergötland (3/1), Västernorrland (3/1), Skåne (3/1), Kalmar (1/1), Jämtland (2/1), plus 7 regions with 0-1 raw stations passing
- 7 of 21 Swedish regions have zero stations: Södermanland, Jönköping, Gotland, Blekinge, Örebro, Dalarna, Norrbotten
- Files: Desktop "Data NO2& PM2.5" folder (32 hourly) + Downloads Bredkälen (daily) + Råö (daily, PM2.5 unusable)

### Case study scope: changed to all Sweden (2026-06-18)
- RQ3 now covers Sweden nationally, not Skåne only
- Rationale: only 1 passing station in Skåne; 7 unmonitored regions nationally make Sweden the more defensible and impactful scope
- All Skåne references removed from §§1 and 3; Appendix C renamed from "PSO Placement Parameters" to "Placement Algorithm Parameters"

### Still needed
- Meteorological covariates: Python script to download from SMHI metobs API (34 stations)
- CORINE Land Cover for Sweden
- DEM (Lantmäteriet Höjddata)
- Population density (Eurostat GEOSTAT)

## Metobs download script: status (2026-06-18)

Script `data/download_metobs.py` written, debugged, and running.

**Bugs found and fixed this session (3 rounds of debugging):**

Round 1 -- wrong parameter IDs and station coverage:
- Parameter 17 is precipitation (Nederbördsmängd), NOT wind direction. Wind direction is parameter **3** (Vindriktning, 185 active stations).
- Active PST precipitation gauges near AQ stations all started 2023. Fixed: include stations whose period overlaps 2020-2024 (not just `active: true`).
- Precipitation CSV uses different column layout ("Från Datum...") vs hourly ("Datum;Tid..."). Fixed: parser detects header type and reads correct columns.

Round 2 -- nearest-station preference too aggressive:
- `started_early` filter (prefer stations starting before 2020) was applied to ALL parameters. For temperature/wind/humidity near Linköping and Västerås, this selected old sparse stations (Härsnäs: 3,595 rows; Gävle: partial) over nearby active ones.
- Fixed: `_PREFER_EARLY = {5}` -- only precipitation uses the early-station preference. All other parameters prefer currently active stations (which reliably cover 2020-2024), falling back to period-overlap inactive stations only if no active station exists.

Round 3 -- active-station false positive:
- Active stations (to = current date) were incorrectly scoring `early=True` via the to-date proxy. Fixed: proxy only applies to inactive stations.
- Root cause confirmed by debug: active Västerås station (from=invalid, active=True) had to=2026 → early=True → selected over the inactive station at 4.1km.

Round 4 -- final re-download of 3 stations:
- 155530 (Västerås Melkertorget): temp=14,378 rows (31.5%) — best available; inactive met station operated 2020-02 to 2021-11
- 344172 (Västerås Stora Gatan): temp=14,378 rows (31.5%) — same met station
- 369485 (Varberg Västra Vallgatan): temp=5,481 rows (12.0%) — best available; nearest station with unknown start, to=2026-06
- These 3 are genuine SMHI network gaps; nearest alternative active stations are 25-30km away

**Final audit results (34 station files):**

Temperature (31/34 stations >= 80% coverage):
- 31 stations: 95-99% hourly coverage (typically 43,000-45,000 rows)
- 3 stations with genuine SMHI network gaps:
  - 155530 Västerås Melkertorget: 14,378 rows (31.5%) — inactive station, operated Feb 2020 to Nov 2021 only
  - 344172 Västerås Stora Gatan: 14,378 rows (31.5%) — same station
  - 369485 Varberg Västra Vallgatan: 5,481 rows (12.0%) — nearest active early station is Källsjö (30.7km, also sparse)
  - Nearest full-coverage alternative for both: Eskilstuna A (25.6km) and Nidingen A (30.3km) respectively

Precipitation (19/34 stations with full 1,827 daily rows):
- Stockholm (10 stations): 367 rows via Stockholm-Observatoriekullen A (post-2023 corrected archive only)
- Göteborg Haga: 1,032 rows (Barlastplatsen)
- Sundsvall: 527 rows (Heffners)
- Timrå: 664 rows (Fillan)
- Östersund: 1,767 rows (Litsnäset)
- Kalmar: 141 rows (Lindolundgatan, PST gauge 2023+)
- Root cause: SMHI transitioned from traditional precipitation gauges to PST network ~2023. No traditional gauge started before 2020 exists within city proximity for these areas.
- Phase 5 implication: precipitation will have systematic NaN for 2020-2022 at these 15 stations.

**Output format note:** hourly parameters (temp, wind, rh) use datetime key "YYYY-MM-DD HH:MM:SS"; precipitation uses date key "YYYY-MM-DD". Phase 5 must join on date when building the daily feature matrix.

Final output: `data/raw/metobs/<aq_code>_metobs.csv` (34 files) + `download_log.csv`.

## Session summary (2026-06-18 continued — Phase 4 completion)

### Data downloads completed this session

All three remaining ancillary data sources for Phase 4 have been downloaded and verified.

**CORINE Land Cover 2018:**
- File: `data/raw/corine/CLC2018.tif`
- Source: EU Copernicus (land.copernicus.eu), product CLC2018 raster 100m v2020_20u1
- Format: BigTIFF, EPSG:3035, 100m resolution, 65,000 × 46,000 px, 196.6 MB
- Contains 44 land-use classes covering all of Europe

**Population density (GEOSTAT JRC 2018):**
- File: `data/raw/population/JRC_1K_POP_2018.tif`
- Source: Eurostat GEOSTAT (JRC 1 km² population grid)
- Format: GeoTIFF, EPSG:3035, 1000m resolution, 4,472 × 5,561 px, 4.0 MB

**EU-DEM v1.1 (Sweden clip):**
- File: `data/raw/dem/sweden_dem_100m.tif`
- Source: EU-DEM mosaic (GISCO/Copernicus), original 23 GB uncompressed
- Clipped via rasterio `/vsizip/` without full extraction; resampled from 25m to 100m (average)
- Format: GeoTIFF (deflate), EPSG:3035, 100m resolution, 13,000 × 15,700 px, 281.6 MB
- Elevation range: −58 m to 2415 m (bbox includes SW Norway margin)

### Dependency: rasterio v1.4.4

rasterio (with `/vsizip/` support) installed this session: `pip install rasterio`. Required to read the 23 GB EU-DEM ZIP without full extraction.

### Inter-station distance matrix

- File: `data/raw/metobs/distance_matrix.csv` (34 × 34, Haversine km)
- File: `data/raw/metobs/stations.csv` (code, name, lat, lon, nn_km)

Key statistics:
- Min nearest-neighbour: 0.5 km (Stockholm Hornsgatan / Torkel Knutssongatan)
- Median nearest-neighbour: 10.9 km
- Max nearest-neighbour: 176.9 km (Bredkälen, isolated Jämtland rural station)

Urban clusters (within-city pairs < 5 km): Stockholm 5 inner-city stations, plus 2-station clusters in Solna, Uppsala, Norrköping, Västerås, Malmö.

### SLOO buffer decision: preliminary 5 km

A 5 km buffer excludes all 24 within-city station pairs from training when any of them is held out. For isolated rural stations (14 of 34 have nearest-neighbour > 5 km), the buffer has no effect.

This is a preliminary value. The final buffer will be set in Phase 5 after computing empirical variograms of PM2.5 and NO2 residuals (Roberts et al. 2017 recommends setting the buffer to the variogram range). Preliminary 5 km is documented in §3.3 as "buffer radius determined in Phase 4."

### Phase 4 complete

All tasks in roadmap.md Phase 4 are now checked. `docs/data-audit.md` written with full documentation of all five data sources.

## Session summary (2026-06-22 — Phase 5 started)

### Feature matrix built

Script: `data/build_feature_matrix.py`
Output: `data/processed/feature_matrix.csv`

**Shape:** 48,283 rows × 36 columns
**Study period:** 2020-01-01 to 2024-12-31 (1,827 days)
**Stations:** 34

**Columns:** date, station_code, station_name, station_type, lat, lon, covid_period, temp_C, wind_speed_ms, wind_dir_deg, rh_pct, precip_mm, [18 CORINE features at 500m and 1km], elevation_m, terrain_rough_m, pop_1km, pop_5km, NO2_ugm3, PM25_ugm3

### EDA findings

**Station completeness (revised):** 11 stations pass ≥90% for BOTH NO2 and PM2.5 (previously documented as 13 — revised down after counting against the full 1,827-day period with actual downloaded files).

Passing stations:
- Bredkälen (Rural Background)
- Malmö Rådhuset (Urban Background)
- Stockholm Hornsgatan (Urban Traffic)
- Stockholm Torkel Knutssongatan (Urban Background)
- Norr Malma (Rural-Regional Background)
- Sollentuna E4 Häggvik (Urban Traffic)
- Sundsvall Köpmangatan (Urban Traffic)
- Uppsala Kungsgatan (Urban Traffic)
- Stockholm St Eriksgatan (Urban Traffic)
- Uppsala Dragarbrunnsgatan (Urban Background)
- Kalmar Södra Vägen (Urban Traffic)

**Target variable statistics:**
- NO2: mean 12.85 ± 9.61 µg/m³, range −0.47 to 108.9 (1 negative = instrument artefact, clip to 0)
- PM2.5: mean 5.26 ± 4.28 µg/m³, range −0.86 to 86.25 (11 negative = instrument artefact, clip to 0)
- Both distributions right-skewed (P95 = 30.89 and 12.92 respectively)

**Weather covariate completeness:**
- Temperature: 97.4% (3 stations with poor met coverage reduce this)
- Wind speed/direction/humidity: 99.4–99.8% (excellent)
- Precipitation: 68.4% (known limitation: SMHI PST network rollout ~2023)

**COVID signal:**
- Mean NO2 2020–2021: 13.82 µg/m³ vs 2022–2024: 12.34 µg/m³ (12% higher in COVID period)
- This is counterintuitive (lockdowns should lower NO2) — likely a station composition effect (more active stations in 2022–2024 include lower-traffic areas). The covid_period binary flag is in the matrix; Phase 6 sensitivity analysis will address this.

### Phase 5 remaining tasks

- [ ] Clip negative values to 0 (12 instrument artefact readings)
- [ ] Decide precipitation imputation strategy (31.6% missing)
- [ ] Write §4 (Data Sources and Feature Engineering)
- [ ] Variogram analysis to finalise SLOO buffer radius

## Immediate next step

**Continue Phase 5:**

Phase 5 entry point:
1. Ingest the 34 AQ station CSV files from the SMHI Datavärdskap Luft download (Desktop "Data NO2& PM2.5" folder + Downloads)
2. Parse and align daily PM2.5 and NO2 values per station for 2020-2024
3. Aggregate metobs hourly data to daily (mean temp/wind/humidity; total or max precip)
4. Extract CORINE land-use proportions within 500m and 1km buffers per station
5. Extract DEM elevation and terrain roughness per station
6. Extract population density within 1km per station
7. Build unified feature matrix (34 stations × ~1,827 days × ~15 covariates)
8. Run EDA: missing data audit, spatial distribution maps, correlation heatmap, variogram to finalize SLOO buffer
9. Write §4 (Data Sources and Feature Engineering)

## Open threads

### Already resolved
- Appendix C PSO contradiction — fixed (renamed to "Placement Algorithm Parameters") 2026-06-18
- Case study scope — resolved: all Sweden 2026-06-18

### Still open (thesis text edits — before next draft)
- **§8 Discussion** — when written: add daily averages delimitation sentence; add infrastructure scope boundary; note PSO as future work

### Fixed (thesis text edits — 2026-06-27)
- ~~**§3.2 station count**~~ — updated: "50-100" replaced with actual count (13 stations, 11 concurrent); parsimony argument restated
- ~~**§3.4 COVID strategy**~~ — paragraph added: binary covariate + 2022-2024 sensitivity run
- ~~**§3.4 distance metric**~~ — "Euclidean distance" named explicitly + NO2 road-network justification sentence added
- ~~**§3.4 urban/rural stratification**~~ — replaced with traffic vs. background contrast; 13 stations named explicitly
- ~~**Appendix B TODO**~~ — "RF, XGBoost, Kriging" replaced with "RF, LUR, and IDW"
- ~~**§2.3 benchmarks**~~ — sentence added citing sweden_dispersion_2024 as modern Swedish evidence; ESCAPE benchmarks reaffirmed as the standard
- ~~**§3.5 scope boundary**~~ — paragraph added: output is candidate coordinates not deployment specs; infrastructure constraints out of scope; PSO noted as future work
- ~~**§1 daily averages delimitation**~~ — rewritten as explicit delimitation: sub-daily dynamics and real-time forecasting stated as outside scope
- ~~**§3.2 ESCAPE precedent**~~ — sentence added: 13 stations consistent with individual ESCAPE study areas (20--40 sites); parsimony principle justified by precedent

### Still open (data and decisions)
- Buffered SLOO exclusion radius: set after inter-station distance matrix computed (Phase 4 remaining)
- Decay threshold criterion: set in Phase 5 EDA
- Time period extension (2017-2018): station count (13 passing) is below 40-50 threshold — needs supervisor discussion before deciding
- Seasonal decay curves: add to Phase 6 task list
- Logo file needed before first LaTeX compile: `writing/images/logo.jpg`

## Decisions made (all sessions to date, chronological)

- Phases 1 and 2 complete; §1 and §2 drafted without method commitments
- LUR established as the baseline benchmark in §2.3 (ESCAPE R² values documented)
- Roberts et al. 2017 positioned as the methodological foundation for spatial CV in §2.3
- The three research gaps in §2.5 are the explicit inputs to Phase 3
- All \label{} commands added to sections for cross-referencing
- **Phase 3 council complete (2026-06-05):** buffered SLOO; RF + LUR + IDW; PM2.5 and NO2 modelled separately; greedy sequential placement; real-world DSR criterion in §3.6; full record in `docs/decisions/phase3-methodology.md`
- **Phase 3 §3 drafted (2026-06-05):** all seven subsections written; all ten council conditions met; no assumed choices remain
- **All % VERIFY citations resolved (2026-06-05)**
- **Data source locations confirmed (2026-06-15):** Datavärdskap Luft portal, metobs API, CORINE, Lantmäteriet, Eurostat GEOSTAT
- **Portal download filter decisions (2026-06-15):** all Län (national), all Kommun (unfiltered), all stations (Alla), Dygn resolution, all Områdesklassificering, all Klassificering
- **Time period rationale confirmed (2026-06-15):** 2020-2024; extension only if station count below threshold after full API download
- **COVID strategy agreed (2026-06-15):** binary covariate + sensitivity analysis (2020-2024 vs 2022-2024 models)
- **Air quality data audit complete (2026-06-17):** 34 unique stations with both PM2.5 and NO2; 13 pass quality filters (≥90% completeness, ≥80% period coverage); distributed across 14 of 21 Swedish regions; 7 regions unmonitored (Södermanland, Jönköping, Gotland, Blekinge, Örebro, Dalarna, Norrbotten)
- **Case study scope changed to all Sweden (2026-06-18):** Skåne ruled out (1 passing station); national scope more defensible and impactful given 7 unmonitored regions; all §§1 and 3 updated accordingly
- **Appendix C renamed (2026-06-18):** "PSO Placement Parameters" → "Placement Algorithm Parameters"
