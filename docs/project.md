# Project brief

## Identity

**Title:** Spatial Estimation of Air Quality at Unmonitored Locations Using Machine Learning: Implications for IoT Sensor Network Design in Swedish Cities
**Student:** Abdalazeez Asaad
**Supervisor:** Fisseha Mekuria
**Programme:** MSc Internet of Things, Malmö University
**Method framing:** Design Science Research (Peffers 2007, Hevner 2008) -- required; must be argued in §3, not assumed
**Submission target:** 2026-08-01 (confirm exact date with supervisor)

## Research questions

From the approved proposal. May be refined as Phase 2 literature reveals more precise framings; any change must be noted and justified.

- **RQ1:** How accurately can ML models estimate daily PM2.5 and NO2 at spatially withheld SMHI stations using land-use, topography, and meteorological covariates?
- **RQ2:** How does estimation accuracy degrade with distance from the nearest reference station, and what is the reliable prediction distance threshold?
- **RQ3:** How can optimization heuristics guide step-by-step IoT sensor placement in a Swedish metropolitan case study?

## Anchored commitments (from approved proposal)

These are fixed by the proposal. They define scope and direction, not technical conclusions.

- **Pollutants:** PM2.5 and NO2
- **Data period:** 2020-2024
- **Primary data sources:** SMHI Luftwebb, SMHI metobs API, CORINE Land Cover
- **Geographic scope:** Sweden nationally for model training; Skåne region for case study (subject to Phase 4 data audit; widen to southern Sweden if coverage is too sparse)
- **DSR framing:** Required; all artefact-producing phases must map to Peffers six phases in §3
- **Validation principle:** Spatial cross-validation is required; standard k-fold is not defensible given spatial autocorrelation

## Open questions (resolved through Phases 1-3)

Do not treat these as decided until the relevant phase earns the decision through literature and problem grounding.

- Which ML models to compare: determined by Phase 2 literature survey
- Which spatial validation protocol: determined by Phases 2-3 methodology design
- Whether Kriging or hybrid geostatistics are warranted: determined by Phase 4 station audit
- Which optimization approach for RQ3: determined by Phase 3, based on what literature supports
- How to handle the COVID-19 data period: determined by Phase 5 EDA

## Candidate data sources

Usability confirmed in Phase 4. Do not treat as settled until then.

| Source | Content | Access |
|---|---|---|
| SMHI Luftwebb | PM2.5 and NO2 daily averages at Swedish reference stations + coordinates (2020-2024) | Downloadable, free |
| SMHI metobs API | Meteorological covariates (temperature, wind, humidity) | REST API, free |
| CORINE Land Cover | Land-use classification per station radius | EU open data, free |
| DEM + population density | Topography and gridded population within 1 km | Confirmed in Phase 4 |

## Known risks

| Risk | Impact | Mitigation |
|---|---|---|
| Literature does not clearly support the proposal's methodological direction | High | Phase 3 is where methodology is argued; revise if literature demands it |
| Spatial autocorrelation and overfitting | High | Validation protocol chosen in Phase 3 must address this explicitly |
| Data incompleteness and API downtime (2020-2024) | Medium | 90% completeness filter; spatial imputation for gaps |
| Skåne station coverage too sparse | Medium | Widen to southern Sweden if needed; decided in Phase 4 |

## Still open

- Exact defense date (TBD after submission)
- All technical choices (models, validation protocol, optimization method): determined through Phases 1-3
