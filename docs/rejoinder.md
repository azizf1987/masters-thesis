# Rejoinder

Responses to examiner comments received on the thesis draft.

---

## Comment 1 — Section 6.2 (Decay Curve Fitting)

**Comment:**
These criteria should be defined and elaborated to show the effect and necessity. Also, this section needs a transition explaining why we need to see decay curve fitting.

**Response:**
Fixed. AIC/BIC are now defined and elaborated in Section 6.2 (formulas, what they measure, why AIC over raw fit), with the design rationale for the choice moved to Section 3.4 so it's argued once, in the methodology, rather than repeated. Added a transition at the start of 6.2 linking it back to 3.4.

---

## Comment 2 — Table 5

**Comment:**
In table 5, IDW provides better RMSE in 7/11 stations. Even RF provides lower RMSE, this situation needs to be clarified. It would be great if you could provide R^2 and MAE of LUR and IDW.

**Response:**
Added MAE and R² for LUR and IDW (previously only RMSE was shown). Added a short explanation of why IDW wins at 7/11 stations despite RF's lower mean RMSE: RF's mean is pulled down by two isolated rural stations where it performs exceptionally well, while IDW is competitive or better at most of the remaining nine.

---

## Comment 3 — Table 6

**Comment:**
As seen in Table 6 also, IDW provides better performance for all the aspects. So, it would be better to provide all the related metrics for the three algorithms and compare fairly instead of making RF the core algorithm.

**Response:**
Added MAE and R² for LUR and IDW here as well. Noted that no equivalent caveat is needed for PM₂.₅: IDW wins at 10/11 stations, which is consistent with its lower mean RMSE (unlike the NO₂ case).

---

## Comment 4 — Section 2.5 (Research Gaps and Positioning)

**Comment:**
Phrase cautiously if you cannot support by a systematic review, as you have not done for this work.

**Response:**
Revised. The claim is now scoped to the literature reviewed in this thesis (not an absolute claim about the field), and specifically extended to note that no distance-accuracy analysis exists for the Swedish SMHI network either, citing Segersson et al. and the Stockholm/Gothenburg/Malmö dispersion study to show the Swedish literature was checked.
