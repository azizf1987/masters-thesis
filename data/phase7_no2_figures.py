"""Phase 7 addendum: NO2 coverage figures (before/after + placement distance map),
using the PM2.5-optimised sensor placement from phase7_placement.py evaluated
against the NO2 reliable-prediction threshold. Reuses coverage_grid.csv and
placement_coordinates.csv; no re-run of the DEM/CORINE pipeline is needed."""

import sys
import numpy as np
import pandas as pd
from pyproj import Transformer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
sys.stdout.reconfigure(encoding='utf-8')

BASE        = "C:/Users/aziz_/Documents/mau-thesis"
RESULTS_DIR = f"{BASE}/data/results"
FIGURES_DIR = f"{BASE}/writing/images"
STATIONS_PATH = f"{BASE}/data/raw/metobs/stations.csv"

NO2_THRESH_KM = 6.0
GRID_STEP_M   = 10_000

PASSING = {"102", "8773", "8780", "8781", "18643", "20415", "32423",
           "156417", "157992", "159404", "181993"}

to_3035 = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)

# ── Load data ─────────────────────────────────────────────────────
grid = pd.read_csv(f"{RESULTS_DIR}/coverage_grid.csv")
placement = pd.read_csv(f"{RESULTS_DIR}/placement_coordinates.csv")
dsr = pd.read_csv(f"{RESULTS_DIR}/dsr_metrics.csv").set_index('metric')['value']

stations = pd.read_csv(STATIONS_PATH, dtype={'code': str})
stations['code'] = stations['code'].astype(str)
passing_stns = stations[stations['code'].isin(PASSING)].copy()
ex, ey = to_3035.transform(passing_stns['lon'].values, passing_stns['lat'].values)
existing_xy = np.column_stack([ex, ey])
placed_xy = placement[['x3035', 'y3035']].values

pct_no2_init  = float(dsr['no2_land_pct_before'])
pct_no2_final = float(dsr['no2_land_pct_after'])
n_placed = len(placement)

# ── Reconstruct 2D grid from the land-cell list ────────────────────
x_vals = np.sort(grid['x3035'].unique())
y_vals = np.sort(grid['y3035'].unique())
x_min, y_min = x_vals.min(), y_vals.min()
n_x = int(round((x_vals.max() - x_min) / GRID_STEP_M)) + 1
n_y = int(round((y_vals.max() - y_min) / GRID_STEP_M)) + 1

xi = np.round((grid['x3035'].values - x_min) / GRID_STEP_M).astype(int)
yi = np.round((grid['y3035'].values - y_min) / GRID_STEP_M).astype(int)

def to_grid_array(value_1d):
    arr = np.full((n_y, n_x), np.nan)
    arr[yi, xi] = value_1d
    return arr

extent = [x_min, x_min + (n_x - 1) * GRID_STEP_M,
          y_min, y_min + (n_y - 1) * GRID_STEP_M]

def station_scatter(ax, xy, marker='o', color='#1f78b4', size=60, label=None, zorder=5):
    ax.scatter(xy[:, 0], xy[:, 1], s=size, c=color, marker=marker, zorder=zorder,
               edgecolors='white', linewidths=0.6, label=label)

# ── Figure: NO2 before/after coverage maps ─────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 9))
cmap_coverage = mcolors.ListedColormap(['#f7f7f7', '#d1e5f0', '#4393c3'])

def make_coverage_code(covered, urban):
    code = np.zeros(len(covered), dtype=float)
    code[covered & ~urban] = 1
    code[covered & urban] = 2
    return code

urban = grid['urban'].values.astype(bool)
before_code = make_coverage_code(grid['no2_covered_before'].values.astype(bool), urban)
after_code  = make_coverage_code(grid['no2_covered_after'].values.astype(bool), urban)

before_arr = to_grid_array(before_code)
after_arr  = to_grid_array(after_code)

for ax, arr, title, panel in zip(
        axes, [before_arr, after_arr],
        [f'Before placement ({pct_no2_init:.2f}% covered)',
         f'After {n_placed} PM2.5-optimised sensors ({pct_no2_final:.2f}% covered)'],
        ['before', 'after']):
    ax.imshow(arr, extent=extent, origin='lower', aspect='equal',
              cmap=cmap_coverage, vmin=0, vmax=2, interpolation='nearest')
    ax.set_title(title, fontsize=11)
    ax.set_xlabel('EPSG:3035 x (m)')
    ax.set_ylabel('EPSG:3035 y (m)')
    ax.tick_params(axis='both', labelsize=7)
    station_scatter(ax, existing_xy, marker='o', color='#d6604d', size=70,
                    label='Existing stations', zorder=6)
    if panel == 'after':
        station_scatter(ax, placed_xy, marker='^', color='#1a9641', size=80,
                        label='Placed sensors (PM2.5-optimised)', zorder=7)
    ax.legend(fontsize=8, loc='upper left')

patches = [
    mpatches.Patch(color='#f7f7f7', label='Uncovered land'),
    mpatches.Patch(color='#d1e5f0', label=f'Covered (non-urban, NO2 ≤{NO2_THRESH_KM:.0f} km)'),
    mpatches.Patch(color='#4393c3', label='Covered (urban)'),
]
fig.legend(handles=patches, loc='lower center', ncol=3, fontsize=9, bbox_to_anchor=(0.5, 0.0))
fig.suptitle('NO2 national coverage under the PM2.5-optimised placement\n'
             '(10 km grid; sensors were not placed to serve the NO2 threshold)', fontsize=12)
plt.tight_layout(rect=[0, 0.06, 1, 1])
path1 = f"{FIGURES_DIR}/fig_no2_coverage_before_after.png"
plt.savefig(path1, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {path1}")

# ── Figure: NO2-threshold distance surface with placement ─────────
fig, ax = plt.subplots(figsize=(8, 11))
dist_arr = to_grid_array(grid['dist_final_km'].values)
vmax = NO2_THRESH_KM + 10
im = ax.imshow(dist_arr, extent=extent, origin='lower', aspect='equal',
               cmap='YlOrRd_r', vmin=0, vmax=vmax, interpolation='nearest')
cbar = plt.colorbar(im, ax=ax, fraction=0.028, pad=0.02, extend='max')
cbar.set_label('Distance to nearest station/sensor (km)', fontsize=9)
cbar.ax.axhline(y=NO2_THRESH_KM / vmax, color='black', linewidth=1.5)
cbar.ax.text(1.05, NO2_THRESH_KM / vmax, f'{NO2_THRESH_KM:.0f} km\nthreshold',
             transform=cbar.ax.transAxes, fontsize=7, va='center')

station_scatter(ax, existing_xy, marker='o', color='#2166ac', size=80,
                label=f'Existing stations (n={len(passing_stns)})', zorder=6)
station_scatter(ax, placed_xy, marker='^', color='#d6604d', size=90,
                label=f'PM2.5-optimised sensors (n={n_placed})', zorder=7)
for rank, (px, py) in enumerate(placed_xy, start=1):
    ax.annotate(str(rank), xy=(px, py), xytext=(4, 4), textcoords='offset points',
                fontsize=7, color='#d6604d', fontweight='bold')

ax.set_title(f'Distance to nearest station/sensor vs. the NO2 threshold\n'
             f'NO2 threshold: {NO2_THRESH_KM:.0f} km  |  '
             f'Coverage under PM2.5-optimised placement: {pct_no2_final:.2f}% land', fontsize=10)
ax.set_xlabel('EPSG:3035 x (m)')
ax.set_ylabel('EPSG:3035 y (m)')
ax.legend(fontsize=9, loc='upper left')
ax.tick_params(axis='both', labelsize=7)
plt.tight_layout()
path2 = f"{FIGURES_DIR}/fig_no2_placement_map.png"
plt.savefig(path2, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {path2}")

print(f"\nNO2 land coverage:  {pct_no2_init:.2f}% -> {pct_no2_final:.2f}%")
print(f"NO2 urban coverage: {float(dsr['no2_urban_pct_before']):.2f}% -> {float(dsr['no2_urban_pct_after']):.2f}%")
