"""Regenerate the PM2.5 and NO2 before/after coverage figures with a colour
scheme unified against the distance-surface figures (existing stations =
blue circles, placed/recommended sensors = red triangles), fixing the
inconsistency where the coverage-map figures previously used red=existing,
green=placed while the distance-surface figures used blue=existing,
red=placed. Rebuilt from the already-saved coverage_grid.csv and
placement_coordinates.csv; no DEM/CORINE re-sampling needed."""

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

GRID_STEP_M = 10_000
PM25_THRESH_KM = 64.0
NO2_THRESH_KM  = 6.0

PASSING = {"102", "8773", "8780", "8781", "18643", "20415", "32423",
           "156417", "157992", "159404", "181993"}

# Unified colours (matches the existing distance-surface figures)
COLOR_EXISTING = '#2166ac'  # blue
COLOR_PLACED   = '#d6604d'  # red/orange

to_3035 = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)

grid = pd.read_csv(f"{RESULTS_DIR}/coverage_grid.csv")
placement = pd.read_csv(f"{RESULTS_DIR}/placement_coordinates.csv")
dsr = pd.read_csv(f"{RESULTS_DIR}/dsr_metrics.csv").set_index('metric')['value']

stations = pd.read_csv(STATIONS_PATH, dtype={'code': str})
stations['code'] = stations['code'].astype(str)
passing_stns = stations[stations['code'].isin(PASSING)].copy()
ex, ey = to_3035.transform(passing_stns['lon'].values, passing_stns['lat'].values)
existing_xy = np.column_stack([ex, ey])
placed_xy = placement[['x3035', 'y3035']].values
n_placed = len(placement)

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

def make_coverage_code(covered, urban):
    code = np.zeros(len(covered), dtype=float)
    code[covered & ~urban] = 1
    code[covered & urban] = 2
    return code

cmap_coverage = mcolors.ListedColormap(['#f7f7f7', '#d1e5f0', '#4393c3'])
urban = grid['urban'].values.astype(bool)

def build_coverage_figure(before_col, after_col, thresh_km, pct_before, pct_after,
                           pollutant_label, out_path, note=None):
    before_code = make_coverage_code(grid[before_col].values.astype(bool), urban)
    after_code  = make_coverage_code(grid[after_col].values.astype(bool), urban)
    before_arr = to_grid_array(before_code)
    after_arr  = to_grid_array(after_code)

    fig, axes = plt.subplots(1, 2, figsize=(14, 9))
    for ax, arr, title, panel in zip(
            axes, [before_arr, after_arr],
            [f'Before placement ({pct_before:.1f}% covered)',
             f'After {n_placed} sensors ({pct_after:.1f}% covered)'],
            ['before', 'after']):
        ax.imshow(arr, extent=extent, origin='lower', aspect='equal',
                  cmap=cmap_coverage, vmin=0, vmax=2, interpolation='nearest')
        ax.set_title(title, fontsize=11)
        ax.set_xlabel('EPSG:3035 x (m)')
        ax.set_ylabel('EPSG:3035 y (m)')
        ax.tick_params(axis='both', labelsize=7)
        station_scatter(ax, existing_xy, marker='o', color=COLOR_EXISTING, size=70,
                        label='Existing stations', zorder=6)
        if panel == 'after':
            station_scatter(ax, placed_xy, marker='^', color=COLOR_PLACED, size=80,
                            label='Placed sensors', zorder=7)
        ax.legend(fontsize=8, loc='upper left')

    patches = [
        mpatches.Patch(color='#f7f7f7', label='Uncovered land'),
        mpatches.Patch(color='#d1e5f0', label=f'Covered (non-urban, {pollutant_label} ≤{thresh_km:.0f} km)'),
        mpatches.Patch(color='#4393c3', label='Covered (urban)'),
    ]
    fig.legend(handles=patches, loc='lower center', ncol=3, fontsize=9, bbox_to_anchor=(0.5, 0.0))
    title = f'{pollutant_label} national coverage, greedy sequential placement\n(10 km grid, {len(grid):,} land cells)'
    if note:
        title = f'{pollutant_label} national coverage under the PM2.5-optimised placement\n{note}'
    fig.suptitle(title, fontsize=12)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

build_coverage_figure(
    'pm25_covered_before', 'pm25_covered_after', PM25_THRESH_KM,
    float(dsr['pm25_land_pct_before']), float(dsr['pm25_land_pct_after']),
    'PM2.5', f"{FIGURES_DIR}/fig_coverage_before_after.png",
)

build_coverage_figure(
    'no2_covered_before', 'no2_covered_after', NO2_THRESH_KM,
    float(dsr['no2_land_pct_before']), float(dsr['no2_land_pct_after']),
    'NO2', f"{FIGURES_DIR}/fig_no2_coverage_before_after.png",
    note='(sensors were not placed to serve the NO2 threshold)',
)
