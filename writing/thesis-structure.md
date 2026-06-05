# Thesis Format and Structure — Spatial Air Quality ML Master's Thesis (MAU)

**Status:** Canonical structure document
This file defines the **authoritative structure and formatting rules** for the thesis and must be followed unless explicitly agreed otherwise with the supervisor.

---

## Front Matter (Before Page 1)

These pages are not numbered or use Roman numerals, depending on the template.

---

## Front Page (Mandatory)

**Top (full width):**
- Malmö University logo as a wide banner

**Center of the page:**
- Degree project title
- Subtitle (if applicable)
- Name of student(s)

**Bottom left corner:**
- Name of programme
- Bachelor's or Master's programme
- 30 credits
- Department of Technology and Society
- Spring/Autumn 20XX
- Main academic supervisor: Name

No page number is displayed.

---

## Popular Science Summary (Mandatory)

- 1--2 pages
- Non-technical language
- Explain:
  - What urban air pollution is and why it matters in Swedish cities
  - Why sparse SMHI monitoring leaves coverage gaps
  - What spatial ML estimation and IoT placement contribute
- No formulas or architecture diagrams

---

## Abstract (Mandatory)

- ~150--250 words
- Academic summary:
  - Problem
  - Aim
  - Method (DSR, SLOOCV, PSO artefact)
  - Contribution
- Must align exactly with research questions and scope

---

## Declaration of AI Usage (Mandatory)

Describe:
- Whether AI tools were used
- For what purpose
- Confirmation that academic responsibility remains with the author

---

## Acknowledgements (Optional)

Brief acknowledgements (supervisor, data providers, personal).

---

## Contents (Mandatory)

- Must be titled **"Contents"**
- Appears **immediately after the front page**
- May span multiple pages
- Section titles listed **without "Chapter X"**
- Page numbers right-aligned
- **Dotted leaders** before page numbers
- Generated automatically

---

## Main Thesis Content

Page numbering starts here at **page 1**.
The thesis starts on a **right-hand page**.

---

## Introduction

- Motivation and context (urban air pollution, SMHI monitoring gaps)
- Research gap (spatial estimation to IoT placement translation)
- Aim and research questions
- Scope and delimitations
- Thesis outline

---

## Background and Related Work

- Urban air quality monitoring and regulatory networks
- Low-cost IoT sensor networks
- Spatiotemporal machine learning for air quality
- Sensor placement optimization (heuristic and PSO-based)
- Research gaps

No implementation details.

---

## Research Methodology

- Design Science Research approach
- Spatial Leave-One-Out Cross-Validation (SLOOCV) design
- Model progression (IDW, RF/XGBoost, Kriging hybrid)
- Evaluation metrics (RMSE, MAE)
- Ethical considerations
- Validity and reliability

---

## Data and Feature Engineering

- SMHI Luftwebb (PM2.5, NO2)
- SMHI metobs API (meteorological covariates)
- CORINE Land Cover, DEM, population density
- Feature matrix construction
- Completeness filtering (90% threshold)
- Missing-data handling

---

## Spatial Estimation Models

- Model architectures and training procedure
- SLOOCV results per pollutant
- Benchmark comparison (IDW vs ML vs hybrid)
- Addresses RQ1

No interpretation beyond reporting metrics.

---

## Accuracy-Distance Analysis

- Error as a function of distance to nearest reference station
- Decay curve fitting
- Reliable prediction distance threshold
- Addresses RQ2

---

## IoT Placement Optimization

- DSR artefact: PSO-based placement tool
- Case-study city selection and uncertainty grid
- Coverage uncertainty heatmaps
- Prioritized deployment coordinates
- Addresses RQ3

---

## Analysis and Discussion

- Explicit answers to RQ1, RQ2, RQ3
- Comparison with related work
- Implications for municipal IoT planning
- Limitations (spatial autocorrelation, data gaps, case-study generalizability)
- Risks and constraints

---

## Conclusion

- Summary of findings
- Explicit answers to research questions
- Contributions
- Future work

---

## Reference List (Mandatory)

- Consistent reference style (IEEE recommended)
- Properly formatted
- May span multiple pages

---

## Appendices (Optional)

- Station inventory and completeness tables
- Model hyperparameters
- PSO placement parameters

No essential arguments here.

---

## Formatting Rules (Mandatory)

- Single line spacing
- Single column layout
- Justified text
- Margins: **30 mm** (top, bottom, left, right)
- Page numbers on all pages
- Body text: **10--11 pt**
- Headings: **14--18 pt**
- Avoid Times font
- All headings numbered
- Do **not** write "Chapter X"
- Tables:
  - Numbered
  - Title above
- Figures:
  - Numbered
  - Caption below
- Tables and figures must be self-explanatory
- Copyright permission required

---

## Structural Balance Guideline (30--30--30 Rule)

- ~30% theory and background
- ~30% method and empirical work
- ~30% scientific analysis
- ~10% front matter, references, appendices

---

## Usage Note

This structure is **binding**.
All drafts, reviews, and revisions must follow it unless explicitly approved by the supervisor.
