"""Regenerate the placement distance-surface map (fig_placement_map.png) with
legible rank labels: black bold text with a white halo, drawn above the
heatmap, instead of the previous fontsize-7 red-on-dark-red labels that were
unreadable (opponent comment on Figure 7). Rebuilt from the already-saved
coverage_grid.csv and placement_coordinates.csv; no DEM/CORINE re-sampling
needed, and the coverage before/after figure is left untouched."""

import sys
import numpy as np
import pandas as pd
from pyproj import Transformer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
sys.stdout.reconfigure(encoding='utf-8')

BASE          = "C:/Users/aziz_/Documents/mau-thesis"
RESULTS_DIR   = f"{BASE}/data/results"
FIGURES_DIR   = f"{BASE}/writing/images"
STATIONS_PATH = f"{BASE}/data/raw/metobs/stations.csv"

GRID_STEP_M    = 10_000
PM25_THRESH_KM = 64.0

PASSING = {"102", "8773", "8780", "8781", "18643", "20415", "32423",
           "156417", "157992", "159404", "181993"}

COLOR_EXISTING = '#2166ac'  # blue
COLOR_PLACED   = '#d6604d'  # red/orange

to_3035 = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)

grid      = pd.read_csv(f"{RESULTS_DIR}/coverage_grid.csv")
placement = pd.read_csv(f"{RESULTS_DIR}/placement_coordinates.csv").sort_values('rank')
dsr       = pd.read_csv(f"{RESULTS_DIR}/dsr_metrics.csv").set_index('metric')['value']
pct_pm25_final = float(dsr['pm25_land_pct_after'])

stations = pd.read_csv(STATIONS_PATH, dtype={'code': str})
stations['code'] = stations['code'].astype(str)
passing_stns = stations[stations['code'].isin(PASSING)].copy()
ex, ey = to_3035.transform(passing_stns['lon'].values, passing_stns['lat'].values)
existing_xy = np.column_stack([ex, ey])
placed_xy   = placement[['x3035', 'y3035']].values

x_vals = np.sort(grid['x3035'].unique())
y_vals = np.sort(grid['y3035'].unique())
x_min, y_min = x_vals.min(), y_vals.min()
n_x = int(round((x_vals.max() - x_min) / GRID_STEP_M)) + 1
n_y = int(round((y_vals.max() - y_min) / GRID_STEP_M)) + 1
xi = np.round((grid['x3035'].values - x_min) / GRID_STEP_M).astype(int)
yi = np.round((grid['y3035'].values - y_min) / GRID_STEP_M).astype(int)

dist_arr = np.full((n_y, n_x), np.nan)
dist_arr[yi, xi] = grid['dist_final_km'].values

extent = [x_min, x_min + (n_x - 1) * GRID_STEP_M,
          y_min, y_min + (n_y - 1) * GRID_STEP_M]

fig, ax = plt.subplots(figsize=(8, 11))
im = ax.imshow(dist_arr, extent=extent, origin='lower', aspect='equal',
               cmap='YlOrRd_r', vmin=0, vmax=PM25_THRESH_KM + 10,
               interpolation='nearest')
cbar = plt.colorbar(im, ax=ax, fraction=0.028, pad=0.02)
cbar.set_label('Distance to nearest station (km)', fontsize=9)
cbar.ax.axhline(y=PM25_THRESH_KM, color='black', linewidth=1.5)
cbar.ax.text(1.05, PM25_THRESH_KM / (PM25_THRESH_KM + 10),
             f'{PM25_THRESH_KM:.0f} km\nthreshold', transform=cbar.ax.transAxes,
             fontsize=7, va='center')

ax.scatter(existing_xy[:, 0], existing_xy[:, 1], s=80, c=COLOR_EXISTING,
           marker='o', edgecolors='white', linewidths=0.6, zorder=6,
           label=f'Existing stations (n={len(passing_stns)})')
ax.scatter(placed_xy[:, 0], placed_xy[:, 1], s=90, c=COLOR_PLACED,
           marker='^', edgecolors='white', linewidths=0.6, zorder=7,
           label=f'Recommended sensors (n={len(placed_xy)})')

for rank, (px, py) in zip(placement['rank'].values, placed_xy):
    ax.annotate(str(int(rank)), xy=(px, py), xytext=(6, 6),
                textcoords='offset points', fontsize=10, color='black',
                fontweight='bold', zorder=8,
                path_effects=[pe.withStroke(linewidth=2.5, foreground='white')])

ax.set_title(f'Sensor placement, final distance surface\n'
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
print(f"Saved: {path}")
