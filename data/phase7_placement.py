"""Phase 7: National uncertainty grid and greedy sequential sensor placement."""

import os, math, sys
import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
sys.stdout.reconfigure(encoding='utf-8')

# ── Paths ─────────────────────────────────────────────────────────
BASE          = "C:/Users/aziz_/Documents/mau-thesis"
CORINE_PATH   = f"{BASE}/data/raw/corine/CLC2018.tif"
DEM_PATH      = f"{BASE}/data/raw/dem/sweden_dem_100m.tif"
STATIONS_PATH = f"{BASE}/data/raw/metobs/stations.csv"
RESULTS_DIR   = f"{BASE}/data/results"
FIGURES_DIR   = f"{BASE}/writing/images"

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# ── Approximate Sweden boundary polygon (lat, lon) ───────────────
# ~25-vertex approximation of Sweden's mainland coast and land borders.
# Sufficient precision for a 10 km grid; excludes major Norwegian/Finnish land.
SWEDEN_POLY_LATLON = np.array([
    # South coast (Skåne, west→east)
    [55.34, 12.65], [55.37, 13.12], [55.38, 14.28],
    # Southeast coast (Blekinge → Kalmar → Stockholm archipelago)
    [56.10, 15.56], [57.66, 16.62], [58.60, 17.02],
    [59.45, 18.77], [59.85, 19.05],
    # Northeast coast (Bothnian Sea/Gulf of Bothnia)
    [60.55, 17.57], [61.78, 17.34], [62.74, 17.92],
    [63.87, 20.22], [65.57, 22.16], [65.61, 24.17],
    # North border (Finland)
    [68.40, 23.08], [68.84, 21.01], [68.96, 20.61],
    # Northwest (Norway border, north→south)
    [68.57, 18.40], [68.00, 17.00], [66.40, 15.25],
    [65.12, 14.55], [63.62, 12.62], [62.33, 12.11],
    [60.97, 12.00], [59.72, 11.67], [59.00, 11.20],
    [58.26, 11.16], [57.50, 11.50], [56.62, 12.20],
    [55.34, 12.65],   # close polygon
], dtype=float)

# ── Constants ─────────────────────────────────────────────────────
GRID_STEP_M      = 10_000         # 10 km grid spacing
PM25_THRESH_KM   = 64.0           # reliable PM2.5 estimation range (Phase 6 IDW exponential)
NO2_THRESH_KM    = 6.0            # reliable NO2 estimation range (Phase 6 IDW log)
PM25_THRESH_M    = PM25_THRESH_KM * 1_000
NO2_THRESH_M     = NO2_THRESH_KM  * 1_000
MAX_GREEDY_STEPS = 20

# 11 concurrent-passing stations (both pollutants, ≥90% completeness)
PASSING = {"102","8773","8780","8781","18643","20415","32423",
           "156417","157992","159404","181993"}

# ── Projections ───────────────────────────────────────────────────
to_3035   = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)
from_3035 = Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy=True)

# ── 1. Load existing stations ─────────────────────────────────────
print("=" * 60)
print("1. Loading station coordinates")
print("=" * 60)

stations = pd.read_csv(STATIONS_PATH, dtype={'code': str})
stations['code'] = stations['code'].astype(str)
passing_stns = stations[stations['code'].isin(PASSING)].copy().reset_index(drop=True)

ex, ey = to_3035.transform(passing_stns['lon'].values, passing_stns['lat'].values)
passing_stns['x3035'] = ex
passing_stns['y3035'] = ey
existing_xy = passing_stns[['x3035', 'y3035']].values   # (11, 2) metres EPSG:3035

print(f"  Passing stations loaded: {len(passing_stns)}")

# ── 2. Build 10 km national grid (EPSG:3035) ─────────────────────
print("\n" + "=" * 60)
print("2. Building 10 km national grid")
print("=" * 60)

# Sweden bounding box – add 100 km margin on each side
# Derived from corner coordinates; will be CORINE-masked to actual land
x_sw, y_sw = to_3035.transform(10.0, 55.0)   # lon, lat
x_ne, y_ne = to_3035.transform(25.0, 69.5)

x_range = np.arange(x_sw, x_ne + GRID_STEP_M, GRID_STEP_M)
y_range = np.arange(y_sw, y_ne + GRID_STEP_M, GRID_STEP_M)
xx, yy   = np.meshgrid(x_range, y_range)
grid_x   = xx.ravel()
grid_y   = yy.ravel()
n_total  = len(grid_x)

print(f"  Grid dimensions: {len(x_range)} cols × {len(y_range)} rows = {n_total:,} cells")

# ── 3. Sample DEM (Sweden land mask) and CORINE (urban) ──────────
print("\n" + "=" * 60)
print("3. Sampling DEM and CORINE at grid points")
print("=" * 60)

coords = list(zip(grid_x.tolist(), grid_y.tolist()))

# DEM: used as Sweden-specific land mask (clipped to Sweden; CORINE covers all Europe)
with rasterio.open(DEM_PATH) as src:
    print(f"  DEM  CRS: {src.crs}  dtype: {src.dtypes[0]}  nodata: {src.nodata}")
    dem_nodata = src.nodata
    dem_v = np.array([v[0] for v in src.sample(coords, indexes=1)], dtype=float)

# Valid DEM = Sweden land (DEM is pre-clipped to Sweden + narrow Norway margin)
# dem_nodata may be NaN: must use np.isnan, not != (NaN != NaN is always True)
if dem_nodata is not None and np.isnan(float(dem_nodata)):
    land_mask = ~np.isnan(dem_v)
elif dem_nodata is not None:
    land_mask = (dem_v != float(dem_nodata)) & ~np.isnan(dem_v)
else:
    land_mask = ~np.isnan(dem_v)

# CORINE: used only for urban classification within the Sweden land mask
with rasterio.open(CORINE_PATH) as src:
    print(f"  CORINE CRS: {src.crs}  dtype: {src.dtypes[0]}  nodata: {src.nodata}")
    corine_v = np.array([v[0] for v in src.sample(coords, indexes=1)])

unique_c = np.unique(corine_v[land_mask])
print(f"  CORINE values at Sweden land points: {unique_c[:20]}")

# Detect CORINE encoding
if corine_v.max() <= 50:
    urban_codes = {1, 2}     # palette codes for CLC 111 (continuous) + 112 (discontinuous urban)
    print("  Detected: palette encoding (1-44)")
else:
    urban_codes = {111, 112}
    print("  Detected: CLC-code encoding")

urban_mask = np.isin(corine_v, list(urban_codes))

# Apply Sweden polygon filter to exclude Norway, Finland, Denmark from land mask
# matplotlib.path.Path is available via the existing matplotlib import
from matplotlib.path import Path as MplPath
grid_lon, grid_lat = from_3035.transform(grid_x.tolist(), grid_y.tolist())
grid_lonlat = np.column_stack([grid_lon, grid_lat])
sweden_path = MplPath(SWEDEN_POLY_LATLON[:, ::-1])  # Path expects (lon, lat)
in_sweden   = sweden_path.contains_points(grid_lonlat)
land_mask   = land_mask & in_sweden

n_land  = land_mask.sum()
n_urban = (land_mask & urban_mask).sum()
print(f"\n  Total grid cells (bounding box): {n_total:,}")
print(f"  Sweden land cells (DEM + polygon filter): {n_land:,}  ({n_land*100/n_total:.1f}%)")
print(f"  Urban cells within Sweden (CLC 111+112): {n_urban:,}  ({n_urban*100/n_land:.1f}% of land)")

# Extract land-only arrays (urban_mask already refers to full grid; restrict to land)
land_x     = grid_x[land_mask]
land_y     = grid_y[land_mask]
land_urban = urban_mask[land_mask]   # True where land cell is also urban
land_xy    = np.column_stack([land_x, land_y])   # (n_land, 2)

# ── 4. Compute distance from each land cell to existing stations ──
print("\n" + "=" * 60)
print("4. Computing distances to existing stations")
print("=" * 60)

existing_tree         = cKDTree(existing_xy)
dist_to_existing, _   = existing_tree.query(land_xy, k=1)   # metres (n_land,)

pm25_covered_initial  = dist_to_existing <= PM25_THRESH_M
no2_covered_initial   = dist_to_existing <= NO2_THRESH_M

pct_pm25_init  = pm25_covered_initial.sum()  / n_land  * 100
pct_no2_init   = no2_covered_initial.sum()   / n_land  * 100
pct_pm25_urban = (pm25_covered_initial & land_urban).sum() / n_urban * 100 if n_urban else 0
pct_no2_urban  = (no2_covered_initial  & land_urban).sum() / n_urban * 100 if n_urban else 0

print(f"\n  PM2.5 coverage BEFORE placement (threshold {PM25_THRESH_KM} km):")
print(f"    Land area:  {pm25_covered_initial.sum():,} / {n_land:,} cells = {pct_pm25_init:.1f}%")
print(f"    Urban area: {(pm25_covered_initial & land_urban).sum():,} / {n_urban:,} cells = {pct_pm25_urban:.1f}%")
print(f"\n  NO2 coverage BEFORE placement (threshold {NO2_THRESH_KM} km):")
print(f"    Land area:  {no2_covered_initial.sum():,} / {n_land:,} cells = {pct_no2_init:.1f}%")
print(f"    Urban area: {(no2_covered_initial & land_urban).sum():,} / {n_urban:,} cells = {pct_no2_urban:.1f}%")

# ── 5. Greedy sequential placement ───────────────────────────────
print("\n" + "=" * 60)
print(f"5. Greedy sequential placement (PM2.5, threshold={PM25_THRESH_KM} km, max={MAX_GREEDY_STEPS} steps)")
print("=" * 60)

# Precompute which land cells are within PM25 threshold of each candidate land cell.
# This is an all-pairs query used in each greedy iteration.
print("  Precomputing within-threshold neighbour lists...")
land_tree        = cKDTree(land_xy)
neighbors_within = land_tree.query_ball_tree(land_tree, r=PM25_THRESH_M)
print(f"  Done. Average neighbours per cell: {np.mean([len(n) for n in neighbors_within]):.0f}")

# Running state
min_dist   = dist_to_existing.copy()      # (n_land,) metres
pm25_cov   = min_dist <= PM25_THRESH_M    # (n_land,) bool

placed_land_indices = []   # indices into land_xy
coverage_trace = [pm25_cov.sum() / n_land * 100]   # before any placement

print(f"\n  Initial PM2.5 coverage: {coverage_trace[0]:.1f}%")

placed_set = set()
for step in range(MAX_GREEDY_STEPS):
    uncovered = ~pm25_cov   # (n_land,)
    n_uncov   = uncovered.sum()
    if n_uncov == 0:
        print(f"  Step {step+1}: 100% coverage reached — stopping.")
        break

    best_gain = 0
    best_idx  = -1
    for i in range(n_land):
        if i in placed_set:
            continue
        nb  = neighbors_within[i]
        gain = int(uncovered[nb].sum())
        if gain > best_gain:
            best_gain = gain
            best_idx  = i

    if best_idx == -1 or best_gain == 0:
        print(f"  Step {step+1}: no further gain possible — stopping.")
        break

    placed_land_indices.append(best_idx)
    placed_set.add(best_idx)

    # Update min_dist and coverage
    d_new   = np.linalg.norm(land_xy - land_xy[best_idx], axis=1)
    min_dist = np.minimum(min_dist, d_new)
    pm25_cov = min_dist <= PM25_THRESH_M

    new_pct = pm25_cov.sum() / n_land * 100
    coverage_trace.append(new_pct)

    lon_p, lat_p = from_3035.transform(land_xy[best_idx, 0], land_xy[best_idx, 1])
    print(f"  Step {step+1:2d}: lat={lat_p:.2f}, lon={lon_p:.2f}  "
          f"gain={best_gain} cells  cumulative={new_pct:.1f}%")

n_placed = len(placed_land_indices)
print(f"\n  Placement complete. Sensors placed: {n_placed}")

# Final coverage metrics
pm25_covered_final = pm25_cov
no2_covered_final  = min_dist <= NO2_THRESH_M

pct_pm25_final       = pm25_covered_final.sum() / n_land  * 100
pct_pm25_urban_final = (pm25_covered_final & land_urban).sum() / n_urban * 100 if n_urban else 0
pct_no2_final        = no2_covered_final.sum()  / n_land  * 100
pct_no2_urban_final  = (no2_covered_final & land_urban).sum() / n_urban * 100 if n_urban else 0

print(f"\n  PM2.5 coverage AFTER placement:")
print(f"    Land area:  {pm25_covered_final.sum():,} / {n_land:,} = {pct_pm25_final:.1f}%")
print(f"    Urban area: {(pm25_covered_final & land_urban).sum():,} / {n_urban:,} = {pct_pm25_urban_final:.1f}%")
print(f"\n  NO2 coverage AFTER placement (threshold {NO2_THRESH_KM} km):")
print(f"    Land area:  {no2_covered_final.sum():,} / {n_land:,} = {pct_no2_final:.1f}%")
print(f"    Urban area: {(no2_covered_final & land_urban).sum():,} / {n_urban:,} = {pct_no2_urban_final:.1f}%")

# ── 6. Save results ───────────────────────────────────────────────
print("\n" + "=" * 60)
print("6. Saving results")
print("=" * 60)

# Placement coordinates (ranked by step order)
placement_rows = []
for rank, idx in enumerate(placed_land_indices, start=1):
    lon_p, lat_p = from_3035.transform(float(land_xy[idx, 0]), float(land_xy[idx, 1]))
    placement_rows.append({
        'rank':                rank,
        'lat':                 round(lat_p, 4),
        'lon':                 round(lon_p, 4),
        'x3035':               int(land_xy[idx, 0]),
        'y3035':               int(land_xy[idx, 1]),
        'cumulative_pm25_pct': round(coverage_trace[rank], 2),
    })

placement_df = pd.DataFrame(placement_rows)
placement_df.to_csv(f"{RESULTS_DIR}/placement_coordinates.csv", index=False)
print(f"  placement_coordinates.csv ({len(placement_df)} rows)")

# Coverage grid (all land cells)
land_lons, land_lats = from_3035.transform(land_x.tolist(), land_y.tolist())
coverage_grid = pd.DataFrame({
    'lat':                 np.round(land_lats, 4),
    'lon':                 np.round(land_lons, 4),
    'x3035':               land_x.astype(int),
    'y3035':               land_y.astype(int),
    'urban':               land_urban.astype(int),
    'dist_to_existing_km': np.round(dist_to_existing / 1000, 2),
    'dist_final_km':       np.round(min_dist / 1000, 2),
    'pm25_covered_before': pm25_covered_initial.astype(int),
    'pm25_covered_after':  pm25_covered_final.astype(int),
    'no2_covered_before':  no2_covered_initial.astype(int),
    'no2_covered_after':   no2_covered_final.astype(int),
})
coverage_grid.to_csv(f"{RESULTS_DIR}/coverage_grid.csv", index=False)
print(f"  coverage_grid.csv ({len(coverage_grid):,} rows)")

# DSR metrics summary
dsr_rows = [
    {'metric': 'n_existing_stations',          'value': len(passing_stns)},
    {'metric': 'n_grid_cells_land',            'value': int(n_land)},
    {'metric': 'n_grid_cells_urban',           'value': int(n_urban)},
    {'metric': 'pm25_threshold_km',            'value': PM25_THRESH_KM},
    {'metric': 'no2_threshold_km',             'value': NO2_THRESH_KM},
    {'metric': 'pm25_land_pct_before',         'value': round(pct_pm25_init, 2)},
    {'metric': 'pm25_urban_pct_before',        'value': round(pct_pm25_urban, 2)},
    {'metric': 'no2_land_pct_before',          'value': round(pct_no2_init, 2)},
    {'metric': 'no2_urban_pct_before',         'value': round(pct_no2_urban, 2)},
    {'metric': 'n_sensors_placed',             'value': n_placed},
    {'metric': 'pm25_land_pct_after',          'value': round(pct_pm25_final, 2)},
    {'metric': 'pm25_urban_pct_after',         'value': round(pct_pm25_urban_final, 2)},
    {'metric': 'no2_land_pct_after',           'value': round(pct_no2_final, 2)},
    {'metric': 'no2_urban_pct_after',          'value': round(pct_no2_urban_final, 2)},
    {'metric': 'pm25_absolute_gain_pct',       'value': round(pct_pm25_final - pct_pm25_init, 2)},
    {'metric': 'pm25_urban_absolute_gain_pct', 'value': round(pct_pm25_urban_final - pct_pm25_urban, 2)},
]
pd.DataFrame(dsr_rows).to_csv(f"{RESULTS_DIR}/dsr_metrics.csv", index=False)
print(f"  dsr_metrics.csv ({len(dsr_rows)} rows)")

# ── 7. Figures ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("7. Generating figures")
print("=" * 60)

# Helper: rebuild a 2D grid array for imshow
def to_grid_array(land_mask_1d, value_1d):
    """Map a 1D land-cell array back to the 2D (n_y, n_x) grid for imshow."""
    arr = np.full(n_total, np.nan)
    arr[land_mask] = value_1d
    return arr.reshape(len(y_range), len(x_range))

def station_scatter(ax, xy_3035, marker='o', color='#1f78b4', size=60, label=None, zorder=5):
    """Plot stations on an EPSG:3035 axes."""
    ax.scatter(xy_3035[:, 0], xy_3035[:, 1],
               s=size, c=color, marker=marker, zorder=zorder,
               edgecolors='white', linewidths=0.6, label=label)

# Placed sensor coordinates in 3035
placed_xy = land_xy[placed_land_indices] if placed_land_indices else np.empty((0, 2))

# ── Figure 1: Coverage gain curve ────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
x_ticks = list(range(len(coverage_trace)))
ax.plot(x_ticks, coverage_trace, 'o-', color='#2166ac', linewidth=2, markersize=6)
ax.axhline(coverage_trace[0], color='grey', linestyle='--', linewidth=1,
           label=f'Baseline ({coverage_trace[0]:.1f}%)')
ax.set_xlabel('Number of additional sensors placed')
ax.set_ylabel('PM2.5 land area coverage (%)')
ax.set_title(f'Greedy placement: PM2.5 coverage gain\n'
             f'(threshold = {PM25_THRESH_KM:.0f} km, 10 km grid, {n_land:,} land cells)')
ax.set_xticks(x_ticks)
ax.set_ylim(bottom=0, top=105)
ax.legend()
ax.grid(True, alpha=0.3)

# Annotate final value
if len(coverage_trace) > 1:
    ax.annotate(f'{coverage_trace[-1]:.1f}%',
                xy=(len(coverage_trace)-1, coverage_trace[-1]),
                xytext=(6, -12), textcoords='offset points', fontsize=9)

plt.tight_layout()
path = f"{FIGURES_DIR}/fig_placement_gain.png"
plt.savefig(path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {path}")

# ── Figure 2: Before / After coverage maps (side-by-side) ─────────
fig, axes = plt.subplots(1, 2, figsize=(14, 9))

# Colour scheme: uncovered land = light salmon, covered = steelblue, urban = darker variant
cmap_coverage = mcolors.ListedColormap(['#f7f7f7', '#d1e5f0', '#4393c3'])
# 0 = uncovered land (light grey), 1 = covered non-urban, 2 = covered urban
# We encode: uncovered=0, covered non-urban=1, covered urban=2

def make_coverage_code(covered, urban):
    code = np.zeros(len(covered), dtype=float)
    code[covered & ~urban] = 1
    code[covered & urban]  = 2
    return code

before_code = make_coverage_code(pm25_covered_initial, land_urban)
after_code  = make_coverage_code(pm25_covered_final,   land_urban)

before_arr = to_grid_array(land_mask, before_code)
after_arr  = to_grid_array(land_mask, after_code)

extent = [x_range[0], x_range[-1], y_range[0], y_range[-1]]

for ax, arr, title, panel in zip(axes,
                                  [before_arr, after_arr],
                                  [f'Before placement ({pct_pm25_init:.1f}% covered)',
                                   f'After {n_placed} sensors ({pct_pm25_final:.1f}% covered)'],
                                  ['before', 'after']):
    im = ax.imshow(arr, extent=extent, origin='lower', aspect='equal',
                   cmap=cmap_coverage, vmin=0, vmax=2,
                   interpolation='nearest')
    ax.set_title(title, fontsize=11)
    ax.set_xlabel('EPSG:3035 x (m)')
    ax.set_ylabel('EPSG:3035 y (m)')
    ax.tick_params(axis='both', labelsize=7)

    # Existing stations
    station_scatter(ax, existing_xy, marker='o', color='#d6604d',
                    size=70, label='Existing stations', zorder=6)
    if panel == 'after' and len(placed_xy) > 0:
        station_scatter(ax, placed_xy, marker='^', color='#1a9641',
                        size=80, label='Placed sensors', zorder=7)
    ax.legend(fontsize=8, loc='upper left')

# Shared legend patches
patches = [
    mpatches.Patch(color='#f7f7f7', label='Uncovered land'),
    mpatches.Patch(color='#d1e5f0', label=f'Covered (non-urban, PM2.5 ≤{PM25_THRESH_KM:.0f} km)'),
    mpatches.Patch(color='#4393c3', label='Covered (urban)'),
]
fig.legend(handles=patches, loc='lower center', ncol=3, fontsize=9,
           bbox_to_anchor=(0.5, 0.0))
fig.suptitle(f'PM2.5 national coverage — greedy sequential placement\n'
             f'(10 km grid, {n_land:,} land cells)', fontsize=12)
plt.tight_layout(rect=[0, 0.06, 1, 1])

path = f"{FIGURES_DIR}/fig_coverage_before_after.png"
plt.savefig(path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {path}")

# ── Figure 3: Placement map with ranked labels ─────────────────────
fig, ax = plt.subplots(figsize=(8, 11))

# Background: land cells coloured by final PM2.5 min-dist
dist_arr = to_grid_array(land_mask, min_dist / 1000)  # km
im = ax.imshow(dist_arr, extent=extent, origin='lower', aspect='equal',
               cmap='YlOrRd_r', vmin=0, vmax=PM25_THRESH_KM + 10,
               interpolation='nearest')
cbar = plt.colorbar(im, ax=ax, fraction=0.028, pad=0.02)
cbar.set_label('Distance to nearest station (km)', fontsize=9)
cbar.ax.axhline(y=PM25_THRESH_KM, color='black', linewidth=1.5)
cbar.ax.text(1.05, PM25_THRESH_KM / (PM25_THRESH_KM + 10),
             f'{PM25_THRESH_KM:.0f} km\nthreshold', transform=cbar.ax.transAxes,
             fontsize=7, va='center')

# Existing stations
station_scatter(ax, existing_xy, marker='o', color='#2166ac', size=80,
                label=f'Existing stations (n={len(passing_stns)})', zorder=6)

# Placed sensors with rank labels
if len(placed_xy) > 0:
    station_scatter(ax, placed_xy, marker='^', color='#d6604d', size=90,
                    label=f'Recommended sensors (n={n_placed})', zorder=7)
    for rank, idx in enumerate(placed_land_indices, start=1):
        ax.annotate(str(rank), xy=(land_xy[idx, 0], land_xy[idx, 1]),
                    xytext=(4, 4), textcoords='offset points',
                    fontsize=7, color='#d6604d', fontweight='bold')

ax.set_title(f'Sensor placement — final distance surface\n'
             f'PM2.5 threshold: {PM25_THRESH_KM:.0f} km  |  '
             f'After placement: {pct_pm25_final:.1f}% land coverage', fontsize=10)
ax.set_xlabel('EPSG:3035 x (m)')
ax.set_ylabel('EPSG:3035 y (m)')
ax.legend(fontsize=9, loc='upper left')
ax.tick_params(axis='both', labelsize=7)
plt.tight_layout()

path = f"{FIGURES_DIR}/fig_placement_map.png"
plt.savefig(path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {path}")

# ── 8. Summary ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Phase 7 complete.")
print(f"  PM2.5 land coverage:  {pct_pm25_init:.1f}% → {pct_pm25_final:.1f}% "
      f"(+{pct_pm25_final - pct_pm25_init:.1f} pp, {n_placed} sensors)")
print(f"  PM2.5 urban coverage: {pct_pm25_urban:.1f}% → {pct_pm25_urban_final:.1f}%")
print(f"  NO2 land coverage:    {pct_no2_init:.1f}% → {pct_no2_final:.1f}%")
print(f"  NO2 urban coverage:   {pct_no2_urban:.1f}% → {pct_no2_urban_final:.1f}%")
print(f"\nOutput files:")
print(f"  data/results/placement_coordinates.csv")
print(f"  data/results/coverage_grid.csv")
print(f"  data/results/dsr_metrics.csv")
print(f"  writing/images/fig_placement_gain.png")
print(f"  writing/images/fig_coverage_before_after.png")
print(f"  writing/images/fig_placement_map.png")
print("=" * 60)
