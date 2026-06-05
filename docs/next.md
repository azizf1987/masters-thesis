# next.md -- current state and what's next

## Where we are (as of 2026-06-05)

Phases 1, 2, and 3 complete. §§1, 2, and 3 drafted in `writing/thesis.tex`.

**§1 covers:**
- Urban AQ public health burden in Swedish cities (cited: Molnar et al. 2017)
- SMHI network structure and spatial coverage limitations
- The IoT placement problem: why ad hoc deployment is insufficient
- Research aim in general terms; no method commitments
- RQ1, RQ2, RQ3 as numbered list
- Scope and delimitations (PM2.5/NO2, 2020-2024, Sweden nationally, Skåne case study, out-of-scope)
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

## Immediate next step

**Phase 4: Data feasibility audit.** This must be done before any code is written.

Phase 4 confirms whether the Phase 3 methodology is executable with the available data. Two scope decision points:
1. If Skåne PM2.5 coverage is too sparse, expand geographic scope to southern Sweden
2. If national station count falls below a viable RF training threshold, return to Phase 3 to revisit model scope

Phase 4 also resolves the one open dependency from §3: the buffered SLOO exclusion buffer radius, which §3.3 defers to the inter-station distance distribution established here.

**Work sequence for Phase 4:**
1. Pull SMHI Luftwebb station inventory: count PM2.5 and NO2 stations nationally and in Skåne
2. Check data completeness by station and year (2020-2024); apply 90% threshold
3. Confirm SMHI metobs API access; test pull of meteorological covariates
4. Download and verify CORINE Land Cover for Sweden
5. Identify DEM source (Lantmäteriet) and confirm coverage for Skåne
6. Confirm population density grid source and resolution
7. Establish inter-station distance distribution; set buffered SLOO exclusion radius
8. Make the two geographic scope decisions
9. Document audit results in `docs/data-audit.md`

## Open threads

- Buffered SLOO exclusion radius: set in Phase 4 from inter-station distance distribution
- Decay threshold criterion (specific error bound): set in Phase 5 after EDA
- Logo file needed before first LaTeX compile: `writing/images/logo.jpg`

## Decisions made (all sessions to date)

- Phases 1 and 2 complete; §1 and §2 drafted without method commitments
- LUR established as the baseline benchmark in §2.3 (ESCAPE R² values documented)
- Roberts et al. 2017 positioned as the methodological foundation for spatial CV in §2.3
- The three research gaps in §2.5 are the explicit inputs to Phase 3
- All \label{} commands added to sections for cross-referencing
- **Phase 3 council complete (2026-06-05):** buffered SLOO; RF + LUR + IDW; PM2.5 and NO2 modelled separately; greedy sequential placement; real-world DSR criterion in §3.6; full record in `docs/decisions/phase3-methodology.md`
- **Phase 3 §3 drafted (2026-06-05):** all seven subsections written; all ten council conditions met; no assumed choices remain
- All % VERIFY citations resolved (2026-06-05); references.bib clean
