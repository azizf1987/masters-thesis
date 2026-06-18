# Phase 4 Data Audit

**Date completed:** 2026-06-18
**Status:** All five data sources confirmed; SLOO buffer set to 5 km (preliminary).

---

## 1. Air quality data

**Source:** SMHI Datavärdskap Luft (datavardluft.smhi.se)
**Pollutants:** PM2.5 and NO2 daily averages
**Period:** 2020-2024 (1 January 2020 to 31 December 2024)
**Quality filter:** ≥90% daily completeness AND ≥80% temporal period coverage

| Metric | Value |
|---|---|
| Stations downloaded (both PM2.5 and NO2) | 34 |
| Stations passing quality filter | 13 |
| Regions covered (of 21 Swedish regions) | 14 |
| Regions with zero passing stations | 7 (Södermanland, Jönköping, Gotland, Blekinge, Örebro, Dalarna, Norrbotten) |

**Regional breakdown of 13 passing stations:**

| Region | Count | Stations |
|---|---|---|
| Stockholm | 6 | Hornsgatan, Torkel Knutssongatan, Lilla Essingen, Sveavägen, St Eriksgatan, + 1 |
| Uppsala | 2 | Kungsgatan, Dragarbrunnsgatan |
| Östergötland | 1 | Norrköping Trädgårdsgatan |
| Västernorrland | 1 | Sundsvall Köpmangatan |
| Skåne | 1 | Malmö Rådhuset |
| Kalmar | 1 | Kalmar Södra Vägen |
| Jämtland | 1 | Bredkälen |

**Note:** Norr Malma (Norrtälje, Stockholm County) serves as the only rural-background station in the dataset; all other passing stations are urban traffic or urban background.

**Implication for RQ3:** Case study scope widened from Skåne (1 passing station) to all of Sweden. Seven unmonitored regions provide the application context for the placement optimization.

---

## 2. Meteorological covariates

**Source:** SMHI Open Data metobs API (opendata-download-metobs.smhi.se)
**Script:** `data/download_metobs.py`
**Approach:** Nearest SMHI met station per AQ station, per parameter, with period-overlap filtering

**Parameters downloaded:**

| Parameter | SMHI ID | Source resolution | Notes |
|---|---|---|---|
| Air temperature | 1 | Hourly | 31/34 stations ≥80% coverage |
| Wind speed | 4 | Hourly | 34/34 stations high coverage |
| Wind direction | 3 | Hourly | 34/34 stations high coverage |
| Relative humidity | 6 | Hourly | 34/34 stations high coverage |
| Precipitation | 5 | Daily | 19/34 stations full 1827 rows |

**Known limitations:**

- **Temperature gaps (3 stations):** Västerås Melkertorget and Västerås Stora Gatan share the same inactive met station (operated Feb 2020 to Nov 2021 only), giving 14,378 rows (31.5%). Varberg Västra Vallgatan: 5,481 rows (12.0%). These are genuine SMHI network gaps; nearest full-coverage alternative stations are 25-30 km away.
- **Precipitation gaps (15 stations):** SMHI transitioned from traditional precipitation gauges to the PST network circa 2023. Stations in the Stockholm area and several cities have precipitation data only from 2023 onward. Phase 5 must handle systematic NaN for 2020-2022 at these stations (multiple imputation or mean imputation per month).
- **Datetime key mismatch:** Hourly parameters use key format "YYYY-MM-DD HH:MM:SS"; precipitation uses "YYYY-MM-DD". Phase 5 must aggregate hourly to daily (mean for temperature, humidity; max or sum for precipitation) before joining.

**Output files:** `data/raw/metobs/<aq_code>_metobs.csv` (34 files) + `stations.csv` + `distance_matrix.csv` + `download_log.csv`

---

## 3. CORINE Land Cover

**Source:** EU Copernicus Land Monitoring Service (land.copernicus.eu)
**Product:** CLC2018, raster 100m, version 2020_20u1
**File:** `data/raw/corine/CLC2018.tif`

| Property | Value |
|---|---|
| Format | BigTIFF (GeoTIFF with 64-bit offsets) |
| CRS | EPSG:3035 (ETRS89-LAEA) |
| Resolution | 100 m |
| Size | 65,000 × 46,000 pixels |
| Extent | European (left=900,000 bottom=900,000 right=7,400,000 top=5,500,000) |
| File size | 196.6 MB |
| Classes | 44 CORINE land-use classes |

**Phase 5 use:** For each AQ station, compute the proportion of each CORINE class within 500 m and 1 km buffers. Standard LUR feature: percent urban fabric (class 111+112), percent road/transport (122), percent industrial (121), percent agriculture (211-244), percent green urban (141).

---

## 4. Population density

**Source:** Eurostat GEOSTAT 2018 (JRC 1 km² population grid)
**File:** `data/raw/population/JRC_1K_POP_2018.tif`

| Property | Value |
|---|---|
| Format | GeoTIFF |
| CRS | EPSG:3035 (ETRS89-LAEA) |
| Resolution | 1000 m (1 km) |
| Size | 4,472 × 5,561 pixels |
| Extent | European (left=944,000 bottom=942,000 right=6,505,000 top=5,414,000) |
| File size | 4.0 MB |

**Phase 5 use:** Extract population within 1 km and 5 km radius of each AQ station as a density covariate.

---

## 5. Digital elevation model

**Source:** EU-DEM v1.1 mosaic (GISCO/Copernicus)
**File:** `data/raw/dem/sweden_dem_100m.tif`
**Original:** `EU_DEM_mosaic_1000K.ZIP` (23 GB uncompressed) — clipped via rasterio `/vsizip/` without full extraction.

| Property | Value |
|---|---|
| Format | GeoTIFF (deflate compressed) |
| CRS | EPSG:3035 (ETRS89-LAEA) |
| Resolution | 100 m (resampled from 25 m using average) |
| Size | 13,000 × 15,700 pixels |
| Extent | Sweden + small Norway/Finland margins (left=3,800,000 bottom=3,580,000 right=5,100,000 top=5,150,000) |
| File size | 281.6 MB |
| Elevation range | −58 m to 2,415 m (margins include Norwegian peaks) |

**Phase 5 use:** Extract elevation at each AQ station location. Optionally compute terrain roughness (standard deviation of elevation within 1 km buffer) as an additional covariate.

---

## 6. Inter-station distance matrix and SLOO buffer

**File:** `data/raw/metobs/distance_matrix.csv` (34 × 34 pairwise Haversine distances)

**Nearest-neighbour distance distribution (all 34 stations):**

| Statistic | Distance (km) |
|---|---|
| Minimum | 0.5 |
| P10 | 0.6 |
| Median | 10.9 |
| P75 | 37.8 |
| P90 | 96.5 |
| Maximum | 176.9 |

**Urban station clusters** (pairs within 5 km):
- Stockholm: 5 inner-city stations (0.5–2 km apart)
- Solna: 2 stations (~1.5 km apart)
- Uppsala: 2 stations (0.6 km apart)
- Norrköping: 2 stations (0.7 km apart)
- Västerås: 2 stations (0.8 km apart)
- Malmö: 2 stations (~1.5 km apart)

**SLOO buffer decision:** Preliminary buffer set to **5 km**.

- A 5 km buffer excludes 24 station pairs from each fold's training set (all within-city co-located pairs), preventing spatial leakage from stations measuring the same local environment.
- The buffer is a preliminary value. The final buffer will be set in Phase 5 after computing empirical variograms of PM2.5 and NO2 residuals; the buffer should match the estimated variogram range (Roberts et al. 2017).
- For each held-out station with a nearest neighbour beyond 5 km (14 of 34 stations), the buffer has no practical effect — all other stations remain in training. This is expected and appropriate: spatially isolated stations can legitimately use all available training data.
- Impact on training set size: with a 5 km buffer, the expected minimum training set per fold is 29 stations (5-station Stockholm cluster held out); for isolated rural stations it is 33.

---

## Summary: Phase 4 status

| Task | Status |
|---|---|
| AQ data collected (34 stations) | Complete |
| Quality filter applied (13 pass) | Complete |
| Metobs covariates downloaded (34 stations, 5 params) | Complete |
| CORINE Land Cover 2018 obtained | Complete |
| Population density (GEOSTAT 2018) obtained | Complete |
| EU-DEM clipped to Sweden at 100m | Complete |
| Inter-station distance matrix computed | Complete |
| SLOO buffer set (preliminary: 5 km) | Complete |

**Phase 4 is complete.** All data sources are in place. Phase 5 (EDA and feature extraction) can begin.
