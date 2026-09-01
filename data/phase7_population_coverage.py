"""Population-weighted coverage evaluation (examiner request on Section 7.3).

Repeats the national coverage evaluation from phase7_placement.py, but weights
each 10 km grid cell by its resident population instead of counting cells /
land area. Population per cell is aggregated from the JRC GEOSTAT 2018 1 km
population grid (EPSG:3035): every populated 1 km pixel is assigned to its
nearest coverage-grid cell, so the assignment is exact and non-overlapping.
Reuses the already-saved coverage_grid.csv; no DEM/CORINE re-sampling and no
change to any existing result or figure.

Outputs data/results/population_coverage.csv only.
"""

import sys
import numpy as np
import pandas as pd
import rasterio
sys.stdout.reconfigure(encoding='utf-8')

BASE        = "C:/Users/aziz_/Documents/mau-thesis"
RESULTS_DIR = f"{BASE}/data/results"
POP_PATH    = f"{BASE}/data/raw/population/JRC_1K_POP_2018.tif"
STEP_M      = 10_000

grid = pd.read_csv(f"{RESULTS_DIR}/coverage_grid.csv")

# lattice origin (x mod 10000 == 1000, y mod 10000 == 3839 for this grid)
x0 = int(grid['x3035'].min())
y0 = int(grid['y3035'].min())
cell_index = {(int(round((r.x3035 - x0) / STEP_M)),
               int(round((r.y3035 - y0) / STEP_M))): i
              for i, r in grid.iterrows()}

with rasterio.open(POP_PATH) as src:
    band = src.read(1).astype(np.float64)
    if src.nodata is not None:
        band[band == src.nodata] = 0.0
    band[band < 0] = 0.0
    rows_px, cols_px = np.nonzero(band)
    vals = band[rows_px, cols_px]
    # pixel centre coordinates in EPSG:3035
    px, py = rasterio.transform.xy(src.transform, rows_px, cols_px)
    px = np.asarray(px); py = np.asarray(py)

ix = np.round((px - x0) / STEP_M).astype(int)
iy = np.round((py - y0) / STEP_M).astype(int)

pop_cell = np.zeros(len(grid))
matched = 0
for gx, gy, v in zip(ix, iy, vals):
    j = cell_index.get((gx, gy))
    if j is not None:
        pop_cell[j] += v
        matched += v
grid['pop'] = pop_cell

tot_pop       = grid['pop'].sum()
tot_pop_urban = grid.loc[grid['urban'] == 1, 'pop'].sum()

def wcov(mask_col, denom, subset=None):
    g = grid if subset is None else grid[subset]
    return 100.0 * g.loc[g[mask_col] == 1, 'pop'].sum() / denom

rows = []
for pol, before, after in [("PM2.5", "pm25_covered_before", "pm25_covered_after"),
                           ("NO2",   "no2_covered_before",   "no2_covered_after")]:
    rows.append(dict(pollutant=pol, metric="population_weighted_national",
                     before_pct=round(wcov(before, tot_pop), 2),
                     after_pct=round(wcov(after, tot_pop), 2)))
    rows.append(dict(pollutant=pol, metric="population_weighted_urban",
                     before_pct=round(wcov(before, tot_pop_urban, grid['urban'] == 1), 2),
                     after_pct=round(wcov(after, tot_pop_urban, grid['urban'] == 1), 2)))
    rows.append(dict(pollutant=pol, metric="land_area (reference)",
                     before_pct=round(100.0 * grid[before].sum() / len(grid), 2),
                     after_pct=round(100.0 * grid[after].sum() / len(grid), 2)))

out = pd.DataFrame(rows)
out.to_csv(f"{RESULTS_DIR}/population_coverage.csv", index=False)

print(f"Total population assigned to land grid cells: {tot_pop:,.0f}")
print(f"  (national raster total for reference:      {band.sum():,.0f} over all of EU extent)")
print(f"Population in urban (CORINE 111/112) cells:  {tot_pop_urban:,.0f}")
print(f"Grid cells: {len(grid)}  (urban: {(grid['urban'] == 1).sum()})\n")
print(out.to_string(index=False))
print(f"\nSaved: {RESULTS_DIR}/population_coverage.csv")
