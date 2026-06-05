# Literature map

Seven streams must be covered for the thesis to be defensible. Status codes: **Keep** (already in bib), **Add** (confirmed, add to bib), **Add-TBC** (relevant but author list needs verification before citing), **Drop** (irrelevant or mismatched domain).

---

## Stream 1: Urban AQ monitoring and IoT networks

**Role in thesis:** Motivation. Establishes why sparse regulatory networks leave gaps and why IoT deployment matters. Use in §2.1.

| # | Ref | Year | DOI | Status | Notes |
|---|---|---|---|---|---|
| U01 | Karinthi et al. — Sensors 22(1):394 | 2022 | 10.3390/s22010394 | Keep | Survey of low-cost IoT AQ setup; covers hardware, deployment strategies |
| U02 | Laha, Pattanayak, Pattnaik — AIMS Environmental Science | 2022 | 10.3934/environsci.2022044 | Add | Advancement of environmental monitoring using IoT and sensors; outdoor focus; strengthens §2.1 |
| U03 | Popescu & Ionescu — SIITME proc. | 2024 | 10.1109/SIITME63973.2024.10814899 | Keep | IoT devices for urban AQ monitoring; recent and practical |
| U04 | (Author TBC) — Environmental Research | 2021 | 10.1016/j.envres.2021.112574 | Add-TBC | IoT + AI for environmental toxicology and outdoor air pollution monitoring; verify author list |
| U05 | (Author TBC) — Heliyon | 2024 | 10.1016/j.heliyon.2024.e28195 | Add-TBC | Advances in real-time smart environmental monitoring via IoT and sensors; optional but strengthens breadth |

**Dropped from this stream:**

| # | Ref | Reason |
|---|---|---|
| — | Sustainable Computing 2025 (doi:10.1016/j.suscom.2025.101250) | Blockchain focus; not relevant to spatial estimation |
| — | Applied Sciences 2024, Kamal (doi:10.3390/app14135774) | Blockchain/cloud platform; not relevant |
| — | ICAIHC 2023 (doi:10.1109/ICAIHC59020.2023.10431482) | **Indoor** AQ |
| — | Applied Spectroscopy Reviews 2022 (doi:10.1080/05704928.2022.2085734) | **Indoor** low-cost sensors |
| — | IDCIOT 2025 (doi:10.1109/IDCIOT64235.2025.10915106) | Generic; no spatial or ML content |
| — | ICRTEECT 2025 (doi:10.1109/ICRTEECT67512.2025.11448673) | Classification only; not spatial estimation |
| — | AQTR 2024 (doi:10.1109/AQTR61889.2024.10554278) | **Indoor** AQ |
| — | ICCAR 2024 (doi:10.1109/ICCAR61844.2024.10569824) | **Indoor** multi-sensor |
| — | iTechSECOM 2025 (doi:10.1109/iTechSECOM64750.2025.11307649) | **Indoor**, occupancy-aware |
| — | HNICEM 2023 (doi:10.1109/HNICEM60674.2023.10589153) | **Indoor** AQ system |
| — | ICIDCA 2023 (doi:10.1109/ICIDCA56705.2023.10099569) | Generic tracking system; no analytical contribution |
| — | ICCEBS 2023 (doi:10.1109/ICCEBS58601.2023.10448553) | Generic monitoring; no relevance |
| — | Data in Brief 2024 (doi:10.1016/j.dib.2024.110578) | Dataset paper; Bangladesh context; not relevant |
| — | AIoTCs 2022, Wang & Zhang (doi:10.1109/AIoTCs58181.2022.00101) | Visualisation only; does not support spatial estimation claims |

**Gap:** One European source on known limitations of sparse regulatory networks (sub-kilometre PM2.5 heterogeneity). EEA report or peer-reviewed review acceptable.

---

## Stream 2: Land-Use Regression (LUR) — established outdoor baseline

**Role in thesis:** Critical. LUR is the peer-reviewed standard for predicting outdoor pollutants at unmonitored European locations. Must be in §2.2 and explicitly addressed in the methodology discussion.

| # | Ref | Year | DOI | Status | Notes |
|---|---|---|---|---|---|
| L01 | Hoek et al. — Atmos. Environ. 42:7561–7578 | 2008 | 10.1016/j.atmosenv.2008.05.057 | Add | Foundational LUR review; 25 studies; establishes LUR as the baseline your ML extends or supersedes |
| L02 | Eeftens et al. — Environ. Sci. Technol. | 2012 | 10.1021/es301948k | Add | ESCAPE: LUR models for PM2.5 across 20 European study areas; median R² 71%; comparable to your pollutants |
| L03 | Beelen et al. — Environ. Sci. Technol. | 2013 | 10.1021/es305129t | Add | ESCAPE: LUR evaluation for NO2 across 20 European areas; median LOOCV R² 0.83; your ML must beat this |

**Gap:** None critical. Optional: one recent (2020+) LUR paper in a Scandinavian context.

---

## Stream 3: Machine learning for spatial AQ estimation

**Role in thesis:** Core technical stream. Positions your ML approach, justifies model progression (IDW → RF/XGBoost → hybrid), and supports RQ1.

| # | Ref | Year | DOI | Status | Notes |
|---|---|---|---|---|---|
| M01 | Agbehadji & Obagbuwa — Atmosphere 15(11):1352 | 2024 | 10.3390/atmos15111352 | Keep | Systematic ML/DL review for spatiotemporal AQ; foundation for §2.3 |
| M02 | Chen & Lin — Environ. Pollut. 292:118401 | 2021 | 10.1016/j.envpol.2021.118401 | Keep | Note: year in original bib says 2022 but DOI indicates 2021; verify and correct. Smart spatial interpolation + microsensor clustering for PM2.5 |
| M03 | Xie et al. — Sustainability 17(7):2918 | 2025 | 10.3390/su17072918 | Keep-conditional | SwinLSTM + Kriging hybrid; keep only if hybrid geostatistical models remain in scope after Phase 2 station audit |
| M04 | (Author TBC) — Sci. Rep. PMC11890590 | 2025 | 10.1038/s41598-025-92019-3 | Add-TBC | ML for PM2.5 prediction at unmonitored locations (virtual monitoring stations); conceptually closest paper to RQ1; verify author list |
| M05 | (Author TBC) — Expert Syst. Appl. | 2025 | 10.1016/j.eswa.2025.127749 | Add-TBC | AQ forecasting in **non-monitored urban areas** via ML/DL; directly supports RQ1 framing; verify author list |
| M06 | (Author TBC) — Sci. Total Environ. | 2025 | 10.1016/j.scitotenv.2025.180593 | Add-TBC | Review: ML for AQ prediction and data analysis, recent advances; can supplement M01; verify author list |
| M07 | (Author TBC) — Sustain. Cities Soc. | 2024 | 10.1016/j.scs.2024.105976 | Add-TBC | Urban form and seasonal PM2.5 dynamics using interpretable ML + IoT sensor data; land-use feature relevance; verify author list |
| M08 | (Author TBC) — Atmos. Pollut. Res. | 2026 | 10.1016/j.apr.2026.102975 | Add-TBC | RF vs XGBoost vs MLR for PM10; includes RMSE/MAE comparison; directly relevant to model benchmarking in §5; verify author list |

**Gap:** One paper specifically comparing RF or XGBoost against Kriging for spatial AQ interpolation using RMSE/MAE. Provides the bridge between streams 3 and stream 2.

---

## Stream 4: Spatial cross-validation methodology

**Role in thesis:** Required for SLOOCV justification. Without this, SLOOCV reads as an ad-hoc design choice.

| # | Ref | Year | DOI | Status | Notes |
|---|---|---|---|---|---|
| CV01 | Roberts et al. — Ecography 40:913–929 | 2017 | 10.1111/ecog.02881 | Add | Canonical paper on spatial/temporal CV strategies; proves standard CV underestimates prediction error under spatial autocorrelation; cite when introducing SLOOCV in §3 |

**Gap:** One applied paper using spatial block CV specifically for AQ or environmental ML. Shows SLOOCV is used in this domain, not just ecology.

---

## Stream 5: Sensor placement optimization

**Role in thesis:** Supports RQ3 and the PSO artefact. Needs algorithmic foundation and at least one outdoor application.

| # | Ref | Year | DOI | Status | Notes |
|---|---|---|---|---|---|
| P01 | Gupta & Thakur — ICACCTech proc. | 2023 | 10.1109/ICACCTech61146.2023.00073 | Keep | PSO for **outdoor** AQ sensor placement; directly relevant to RQ3 |
| P02 | (Author TBC) — PMC11478801 | 2024 | PMC:11478801 | Add-TBC | Enhanced PSO-based node deployment and coverage in sensor networks; outdoor WSN; algorithmic PSO foundation |
| P03 | Filios et al. — DCOSS-IoT proc. | 2024 | 10.1109/DCOSS-IoT61029.2024.00067 | Drop | **Indoor** AQ (IAQ). Domain mismatch. If kept at all, §2.4 must explicitly state this is an indoor study and explain what transfers to outdoor; strongly recommend dropping |

**Gap:** One paper on uncertainty-driven or coverage-maximizing sensor placement in an outdoor environmental network (non-PSO methods acceptable). Provides methodological breadth.

---

## Stream 6: Swedish and Scandinavian AQ context

**Role in thesis:** Expected by any Swedish examiner. Establishes understanding of the SMHI network and pollutant patterns in the case study region (Skåne / southern Sweden).

| # | Ref | Year | DOI | Status | Notes |
|---|---|---|---|---|---|
| SE01 | (Author TBC) — Air Qual. Atmos. Health | 2024 | 10.1007/s11869-024-01535-0 | Add-TBC | High-resolution dispersion modeling of PM2.5, PM10, NOx, NO2 in six Swedish metropolitan areas 2000–2018; same pollutants and time window as this thesis; must verify full author list |
| SE02 | Molnar et al. — Int. J. Environ. Res. Public Health 14(7):742 | 2017 | 10.3390/ijerph14070742 | Add | Health impact of PM10, PM2.5, BC in Stockholm, Gothenburg, Umeå; Swedish health-effects motivation for §1 |

**Gap (high priority):** One source specifically on air quality in Skåne or southern Sweden. Search: SMHI regional reports, Naturvårdsverket (Swedish EPA) publications, or peer-reviewed studies on Malmö/Lund/Helsingborg air pollution.

---

## Stream 7: Design Science Research methodology

**Role in thesis:** Required framing. Must map Peffers (2007) six phases explicitly in §3.

| # | Ref | Year | DOI | Status | Notes |
|---|---|---|---|---|---|
| D01 | Peffers et al. — J. Manag. Inf. Syst. 24(3):45–77 | 2007 | 10.2753/MIS0742-1222240302 | Keep | Primary DSR methodology reference |
| D02 | Hevner et al. — MIS Q. 28(1) | 2004 | 10.2307/25148625 | Keep | **Year in bib is wrong (shows 2008); correct to 2004.** Secondary DSR reference |

**Gap:** None required. Optional: one DSR application in an environmental or IoT engineering context.

---

## Coverage summary

| Stream | Papers confirmed | Status |
|---|---|---|
| 1. IoT monitoring context | U01, U02, U03 (+ U04, U05 TBC) | Covered after adds |
| 2. LUR baseline | L01, L02, L03 | Gap filled once added |
| 3. ML spatial estimation | M01–M08 | Strong; TBC papers need author verification |
| 4. Spatial CV | CV01 | Covered once added; secondary gap remains |
| 5. Sensor placement | P01, P02 (TBC) | Covered; Filios dropped |
| 6. Swedish AQ context | SE01 (TBC), SE02 | Partially covered; Skåne gap remains |
| 7. DSR methodology | D01, D02 | Covered; fix Hevner year |

**Minimum before writing §2:** Streams 2, 4, and 6 gaps filled. That means L01–L03, CV01, SE01, SE02 added to references.bib (6 confirmed entries).

---

## References.bib action list

### Add now (full citations confirmed or user-provided):

```
laha_iot_env_monitoring_2022    Laha, Pattanayak, Pattnaik (2022)   doi:10.3934/environsci.2022044
roberts_spatial_cv_2017         Roberts et al. (2017)                doi:10.1111/ecog.02881
hoek_lur_review_2008            Hoek et al. (2008)                   doi:10.1016/j.atmosenv.2008.05.057
eeftens_escape_pm_2012          Eeftens et al. (2012)                doi:10.1021/es301948k
beelen_escape_no2_2013          Beelen et al. (2013)                 doi:10.1021/es305129t
molnar_sweden_health_2017       Molnar et al. (2017)                 doi:10.3390/ijerph14070742
```

### Add after verifying author list:

```
iot_env_toxicology_2021         TBC (2021)    doi:10.1016/j.envres.2021.112574
virtual_monitoring_pm25_2025    TBC (2025)    doi:10.1038/s41598-025-92019-3
nonmonitored_urban_aq_2025      TBC (2025)    doi:10.1016/j.eswa.2025.127749
ml_aq_review_stoten_2025        TBC (2025)    doi:10.1016/j.scitotenv.2025.180593
urban_form_pm25_ml_2024         TBC (2024)    doi:10.1016/j.scs.2024.105976
rf_xgboost_pm10_2026            TBC (2026)    doi:10.1016/j.apr.2026.102975
sweden_dispersion_2024          TBC (2024)    doi:10.1007/s11869-024-01535-0
pso_node_deployment_2024        TBC (2024)    PMC:11478801
```

### Correct in bib:

```
hevner_design_science_2004      Year: 2008 → 2004; add doi:10.2307/25148625
chen_pm25_interpolation_2022    Year: verify 2021 vs 2022 against DOI record
```

### Drop from bib:

```
wang_urban_aq_mining_2022       Visualisation paper; does not support spatial estimation claims
```
