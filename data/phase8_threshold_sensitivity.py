"""Phase 8: Sensitivity analysis on the decay-threshold criterion.

The reliable prediction distance threshold (Section 6.4 / RQ2) is defined as
the distance at which IDW RMSE reaches a stated fraction of the sample mean
concentration. The thesis uses 50%. This script re-derives d* and national
PM2.5 / NO2 coverage for a sweep of alternative fractions (20-80%), holding
everything else fixed (fitted IDW decay curves, sample means, existing
station network, and the 20 PM2.5-optimised sensor locations already
recommended in Section 6/7), to test how sensitive the headline results are
to the choice of 50%.

Reuses:
  - data/results/decay_curves.csv       (fitted IDW decay parameters)
  - data/results/coverage_grid.csv       (per-cell distances, threshold-independent)
Sample means (µg/m3) are taken from thesis Section 6.4 (PM2.5: 5.26, NO2: 12.85),
computed at the same stage as the reported 50%-criterion figures, so that the
50% row of this sweep reproduces the thesis numbers exactly (64 km / 6 km).
"""

import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE        = "C:/Users/aziz_/Documents/mau-thesis"
RESULTS_DIR = f"{BASE}/data/results"
FIGURES_DIR = f"{BASE}/writing/images"

# ── Fixed inputs (unchanged from Phase 6 / Phase 7) ─────────────────────
# IDW decay fits (data/results/decay_curves.csv)
PM25_A, PM25_B = 1.3994, 0.009881      # RMSE = a * exp(b*d)   (exponential)
NO2_A,  NO2_B  = 2.8522, 1.9409        # RMSE = a + b*ln(d)    (log)

PM25_MEAN = 5.26     # µg/m3, thesis Section 6.4
NO2_MEAN  = 12.85    # µg/m3, thesis Section 6.4

FRACTIONS = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]

def d_star_pm25(threshold_rmse):
    """Solve 1.3994*exp(0.009881*d) = threshold_rmse for d (km)."""
    if threshold_rmse <= PM25_A:
        return np.nan  # below curve's intercept at d->0; not solvable on this branch
    return math.log(threshold_rmse / PM25_A) / PM25_B

def d_star_no2(threshold_rmse):
    """Solve 2.8522 + 1.9409*ln(d) = threshold_rmse for d (km)."""
    return math.exp((threshold_rmse - NO2_A) / NO2_B)

# ── Coverage grid (threshold-independent distances) ──────────────────────
grid = pd.read_csv(f"{RESULTS_DIR}/coverage_grid.csv")
n_land  = len(grid)
n_urban = int(grid['urban'].sum())
dist_existing = grid['dist_to_existing_km'].values   # nearest of 11 existing stations
dist_final    = grid['dist_final_km'].values          # nearest of 11 existing + 20 placed
urban         = grid['urban'].values.astype(bool)

def coverage_pct(dist_arr, threshold_km, urban_only=False):
    if np.isnan(threshold_km):
        return np.nan
    covered = dist_arr <= threshold_km
    if urban_only:
        return covered[urban].sum() / n_urban * 100 if n_urban else np.nan
    return covered.sum() / n_land * 100

# ── Sweep ──────────────────────────────────────────────────────────────
rows = []
for frac in FRACTIONS:
    pm25_thresh_rmse = frac * PM25_MEAN
    no2_thresh_rmse  = frac * NO2_MEAN

    d_pm25 = d_star_pm25(pm25_thresh_rmse)
    d_no2  = d_star_no2(no2_thresh_rmse)

    rows.append({
        'criterion_pct':        int(frac * 100),
        'pm25_threshold_rmse':  round(pm25_thresh_rmse, 3),
        'pm25_dstar_km':        round(d_pm25, 1) if not np.isnan(d_pm25) else np.nan,
        'pm25_land_pct_before': round(coverage_pct(dist_existing, d_pm25), 2),
        'pm25_land_pct_after':  round(coverage_pct(dist_final, d_pm25), 2),
        'pm25_urban_pct_before':round(coverage_pct(dist_existing, d_pm25, urban_only=True), 2),
        'pm25_urban_pct_after': round(coverage_pct(dist_final, d_pm25, urban_only=True), 2),
        'no2_threshold_rmse':   round(no2_thresh_rmse, 3),
        'no2_dstar_km':         round(d_no2, 1),
        'no2_land_pct_before':  round(coverage_pct(dist_existing, d_no2), 2),
        'no2_land_pct_after':   round(coverage_pct(dist_final, d_no2), 2),
        'no2_urban_pct_before': round(coverage_pct(dist_existing, d_no2, urban_only=True), 2),
        'no2_urban_pct_after':  round(coverage_pct(dist_final, d_no2, urban_only=True), 2),
    })

out = pd.DataFrame(rows)
out.to_csv(f"{RESULTS_DIR}/threshold_sensitivity.csv", index=False)
print(out.to_string(index=False))

# ── Sanity check against thesis baseline (50% row) ───────────────────────
base = out[out['criterion_pct'] == 50].iloc[0]
print("\nBaseline (50%) check against thesis Section 6.4 / 7:")
print(f"  PM2.5 d* = {base['pm25_dstar_km']} km (thesis: 64 km)")
print(f"  NO2   d* = {base['no2_dstar_km']} km (thesis: 6 km)")
print(f"  PM2.5 land coverage before/after = {base['pm25_land_pct_before']}% / {base['pm25_land_pct_after']}% "
      f"(thesis: 10.9% / 67.2%)")
print(f"  NO2   land coverage before/after = {base['no2_land_pct_before']}% / {base['no2_land_pct_after']}% "
      f"(thesis: 0.2% / 0.6%)")

# ── Figure ────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

ax = axes[0]
ax.plot(out['criterion_pct'], out['pm25_dstar_km'], 'o-', color='#2166ac', label='PM$_{2.5}$ $d^*$')
ax.plot(out['criterion_pct'], out['no2_dstar_km'],  's-', color='#d6604d', label='NO$_2$ $d^*$')
ax.axvline(50, color='grey', linestyle='--', linewidth=1, label='Thesis criterion (50%)')
ax.set_xlabel('Threshold criterion (% of sample mean concentration)')
ax.set_ylabel('Reliable prediction distance $d^*$ (km)')
ax.set_title('Distance threshold vs. criterion')
ax.set_yscale('log')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

ax2 = axes[1]
ax2.plot(out['criterion_pct'], out['pm25_land_pct_before'], 'o--', color='#2166ac', alpha=0.6, label='PM$_{2.5}$ before')
ax2.plot(out['criterion_pct'], out['pm25_land_pct_after'],  'o-',  color='#2166ac', label='PM$_{2.5}$ after (20 sensors)')
ax2.plot(out['criterion_pct'], out['no2_land_pct_before'],  's--', color='#d6604d', alpha=0.6, label='NO$_2$ before')
ax2.plot(out['criterion_pct'], out['no2_land_pct_after'],   's-',  color='#d6604d', label='NO$_2$ after (same 20 sensors)')
ax2.axvline(50, color='grey', linestyle='--', linewidth=1)
ax2.set_xlabel('Threshold criterion (% of sample mean concentration)')
ax2.set_ylabel('National land-area coverage (%)')
ax2.set_title('Coverage vs. criterion')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
path = f"{FIGURES_DIR}/fig_threshold_sensitivity.png"
plt.savefig(path, dpi=150, bbox_inches='tight')
plt.close()
print(f"\nSaved figure: {path}")
print(f"Saved table:  {RESULTS_DIR}/threshold_sensitivity.csv")
