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
