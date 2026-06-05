# MSc Thesis — Spatial Air Quality Estimation and IoT Sensor Placement

**Program:** MSc Internet of Things, Malmö University, Autumn 2026
**Student:** Abdalazeez Asaad
**Supervisor:** Fisseha Mekuria
**Submission target:** 2026-08-01 (confirm with supervisor)

---

## What this is about

Swedish urban air pollution (PM2.5, NO2) varies sharply across sub-kilometre scales, but the SMHI reference network is sparse. Low-cost IoT sensors can fill gaps, yet placement is often ad hoc. This thesis develops spatial ML models to estimate pollutant concentrations at unmonitored locations, quantifies how estimation error degrades with distance from reference stations, and builds a PSO-based placement tool for municipal IoT deployments.

---

## The claim

Machine learning spatial estimation, validated with Spatial Leave-One-Out Cross-Validation across the national SMHI network, produces an accuracy-distance decay curve that operationalises when physical IoT nodes are needed. A PSO placement artefact applies that boundary to a Swedish metropolitan case study.

---

## Research questions

| RQ | Question |
|---|---|
| RQ1 | How accurately can ML models estimate daily PM2.5 and NO2 at spatially withheld SMHI stations? |
| RQ2 | How does accuracy degrade with distance, and what is the reliable prediction threshold? |
| RQ3 | How can optimization heuristics guide IoT sensor placement in a metropolitan case study? |

---

## Data sources

- **SMHI Luftwebb** — PM2.5, NO2 daily averages (2020--2024)
- **SMHI metobs API** — meteorological covariates
- **CORINE Land Cover** — land-use classification
- **DEM + population density** — topography and population features

---

## Repo structure

```
writing/              — LaTeX thesis, bibliography, figures
  proposal.md         — approved research proposal
  thesis.tex          — thesis skeleton (TODO stubs)
  thesis-structure.md — MAU formatting rules
  references.bib      — bibliography
docs/
  roadmap.md          — phase tracking
  next.md             — session handoff
agents/               — council deliberation (opt-in)
Taskfile.yml          — runnable commands
```

Planned (Phase 2+): `data/`, `src/`, `scripts/`

---

## Tasks

```
task install    — pip install dependencies
task compile    — compile thesis.tex to PDF
task status     — print roadmap
```

Future: `task ingest`, `task sloocv` (Phase 2+)

---

## Agents

| Trigger | Agent | Use when |
|---|---|---|
| Council invocation (see `AGENTS.md`) | `agents/council.md` | Non-trivial decisions about scope, method, or structure |

Council seats: Skeptic, Editor, Researcher, Domain Expert.

---

## Status

See `docs/roadmap.md` for current phase. Phase 0 (harness reset) complete. Phase 1 (literature + data feasibility) is next.
