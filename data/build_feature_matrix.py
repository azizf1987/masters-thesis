"""
Phase 5: Build unified feature matrix
Inputs:
  - AQ CSV files (Desktop): daily PM2.5 and NO2 per station
  - metobs CSVs (data/raw/metobs/): hourly weather, aggregated to daily
  - station_features.csv (data/processed/): static land-use, DEM, population
Output:
  - data/processed/feature_matrix.csv
"""

import os, re, math, csv
from collections import defaultdict
import sys
sys.stdout.reconfigure(encoding='utf-8')

AQ_DIR     = "C:/Users/aziz_/Desktop/Final terms thesis/thesis/Data NO2& PM2.5"
METOBS_DIR = "C:/Users/aziz_/Documents/mau-thesis/data/raw/metobs"
FEAT_PATH  = "C:/Users/aziz_/Documents/mau-thesis/data/processed/station_features.csv"
OUT_PATH   = "C:/Users/aziz_/Documents/mau-thesis/data/processed/feature_matrix.csv"

START_YEAR, END_YEAR = 2020, 2024

# ─────────────────────────────────────────────────────────────────
# STEP 1: Ingest AQ data
# ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Ingesting AQ data")
print("=" * 60)

def parse_aq_file(path):
    """
    Returns dict: date_str -> {"NO2": float|None, "PM25": float|None}
    Handles both hourly (aggregated to daily mean) and daily files.
    """
    station_info = {}
    col_no2 = col_pm25 = None
    in_data = False
    daily_records = defaultdict(lambda: {"NO2": [], "PM25": []})

    with open(path, encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n").rstrip("\r")
            if line.startswith("#"):
                # Parse station metadata
                m = re.match(r"#([^;]+);(\d+);([^;]+);([0-9.-]+);([0-9.-]+)", line)
                if m:
                    station_info = {
                        "name": m.group(1).strip(),
                        "code": m.group(2).strip(),
                        "type": m.group(3).strip(),
                        "lon":  float(m.group(4)),
                        "lat":  float(m.group(5)),
                    }
                continue

            # Data header line
            if not in_data:
                if line.startswith("Start;"):
                    cols = line.split(";")
                    for i, c in enumerate(cols):
                        if "NO2" in c.upper():
                            col_no2 = i
                        if "PM2.5" in c.upper() or "PM25" in c.upper():
                            col_pm25 = i
                    in_data = True
                continue

            # Data row
            parts = line.split(";")
            if len(parts) < 2:
                continue
            date_raw = parts[0].strip()
            # Extract date portion (YYYY-MM-DD)
            date_str = date_raw[:10]
            try:
                year = int(date_str[:4])
            except ValueError:
                continue
            if year < START_YEAR or year > END_YEAR:
                continue

            def safe_float(s):
                s = s.strip()
                if s == "" or s.lower() in ("nan", "n/a", "-"):
                    return None
                try:
                    return float(s.replace(",", "."))
                except ValueError:
                    return None

            if col_no2 is not None and col_no2 < len(parts):
                v = safe_float(parts[col_no2])
                if v is not None:
                    daily_records[date_str]["NO2"].append(v)
            if col_pm25 is not None and col_pm25 < len(parts):
                v = safe_float(parts[col_pm25])
                if v is not None:
                    daily_records[date_str]["PM25"].append(v)

    # Aggregate to daily means
    result = {}
    for date_str, vals in daily_records.items():
        no2  = round(sum(vals["NO2"])  / len(vals["NO2"]),  3) if vals["NO2"]  else None
        pm25 = round(sum(vals["PM25"]) / len(vals["PM25"]), 3) if vals["PM25"] else None
        result[date_str] = {"NO2": no2, "PM25": pm25}

    return station_info, result

# Pick one file per station code (skip "(1)" duplicates)
aq_files = {}
for fname in sorted(os.listdir(AQ_DIR)):
    if not fname.endswith(".csv"):
        continue
    m = re.match(r"shair-(\d+)-", fname)
    if not m:
        continue
    code = m.group(1)
    if code not in aq_files:          # first alphabetically wins
        aq_files[code] = os.path.join(AQ_DIR, fname)

aq_data = {}   # code -> {date -> {NO2, PM25}}
aq_meta = {}   # code -> station_info
for code, path in sorted(aq_files.items()):
    info, records = parse_aq_file(path)
    aq_data[code] = records
    aq_meta[code] = info
    no2_days  = sum(1 for v in records.values() if v["NO2"]  is not None)
    pm25_days = sum(1 for v in records.values() if v["PM25"] is not None)
    print(f"  {code:>7}  {info.get('name','?'):<35}  "
          f"dates={len(records)}  NO2_days={no2_days}  PM25_days={pm25_days}")

print(f"\nLoaded {len(aq_data)} stations")

# ─────────────────────────────────────────────────────────────────
# STEP 2: Aggregate metobs hourly → daily
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Aggregating metobs to daily")
print("=" * 60)

def circular_mean_deg(angles):
    """Mean of wind direction angles (degrees), handles 0/360 wrap."""
    if not angles:
        return None
    sin_sum = sum(math.sin(math.radians(a)) for a in angles)
    cos_sum = sum(math.cos(math.radians(a)) for a in angles)
    mean_rad = math.atan2(sin_sum, cos_sum)
    deg = math.degrees(mean_rad) % 360
    return round(deg, 1)

def aggregate_metobs(path):
    """
    Read metobs CSV, return dict: date_str -> {temp, wind_speed, wind_dir, rh, precip}
    """
    PARAMS = ["air_temperature_C", "wind_direction_deg", "wind_speed_ms",
              "precipitation_mm", "relative_humidity_pct"]
    daily = defaultdict(lambda: {p: [] for p in PARAMS})
    precip_daily = {}   # date -> float (already daily in some files)

    with open(path, encoding="utf-8", errors="replace") as f:
        header = None
        for line in f:
            line = line.rstrip()
            if line.startswith("#"):
                continue
            if header is None:
                header = line.split(",")
                continue
            parts = line.split(",")
            if len(parts) < 2:
                continue
            dt_str = parts[0].strip()
            date_str = dt_str[:10]
            try:
                year = int(date_str[:4])
            except ValueError:
                continue
            if year < START_YEAR or year > END_YEAR:
                continue

            for i, col in enumerate(header):
                col = col.strip()
                if col not in PARAMS or i >= len(parts):
                    continue
                val_str = parts[i].strip()
                if val_str == "" or val_str.lower() == "nan":
                    continue
                try:
                    val = float(val_str)
                except ValueError:
                    continue
                # Precipitation: if key is just a date (daily format), store directly
                if col == "precipitation_mm":
                    if len(dt_str) == 10:
                        precip_daily[date_str] = val
                    else:
                        daily[date_str][col].append(val)
                else:
                    daily[date_str][col].append(val)

    result = {}
    all_dates = set(daily.keys()) | set(precip_daily.keys())
    for date_str in all_dates:
        d = daily[date_str]
        def mean(lst): return round(sum(lst)/len(lst), 3) if lst else None
        temp       = mean(d["air_temperature_C"])
        wind_speed = mean(d["wind_speed_ms"])
        wind_dir   = circular_mean_deg(d["wind_direction_deg"]) if d["wind_direction_deg"] else None
        rh         = mean(d["relative_humidity_pct"])
        if date_str in precip_daily:
            precip = precip_daily[date_str]
        else:
            precip = round(sum(d["precipitation_mm"]), 3) if d["precipitation_mm"] else None
        result[date_str] = {
            "temp_C":       temp,
            "wind_speed_ms": wind_speed,
            "wind_dir_deg": wind_dir,
            "rh_pct":       rh,
            "precip_mm":    precip,
        }
    return result

metobs_daily = {}   # code -> {date -> weather dict}
for fname in sorted(os.listdir(METOBS_DIR)):
    if not fname.endswith("_metobs.csv"):
        continue
    code = fname.split("_")[0]
    path = os.path.join(METOBS_DIR, fname)
    metobs_daily[code] = aggregate_metobs(path)
    dates = len(metobs_daily[code])
    print(f"  {code:>7}  {dates} daily records")

print(f"\nAggregated {len(metobs_daily)} metobs station files")

# ─────────────────────────────────────────────────────────────────
# STEP 3: Load static station features
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: Loading static station features")
print("=" * 60)

static_feats = {}
with open(FEAT_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    static_cols = [c for c in reader.fieldnames if c not in ("code","name","lat","lon")]
    for row in reader:
        static_feats[row["code"]] = {c: row[c] for c in static_cols}

print(f"  Loaded {len(static_feats)} stations, {len(static_cols)} static features")
print(f"  Features: {', '.join(static_cols)}")

# ─────────────────────────────────────────────────────────────────
# STEP 4: Build unified feature matrix
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: Building unified feature matrix")
print("=" * 60)

from datetime import date, timedelta

# Generate all dates in study period
all_dates = []
d = date(START_YEAR, 1, 1)
end_d = date(END_YEAR, 12, 31)
while d <= end_d:
    all_dates.append(d.isoformat())
    d += timedelta(days=1)

print(f"  Study period: {all_dates[0]} to {all_dates[-1]} ({len(all_dates)} days)")
print(f"  Stations: {len(aq_data)}")
print(f"  Max possible rows: {len(all_dates) * len(aq_data):,}")

# Flag COVID period
def covid_flag(date_str):
    year = int(date_str[:4])
    return 1 if year in (2020, 2021) else 0

WEATHER_COLS = ["temp_C","wind_speed_ms","wind_dir_deg","rh_pct","precip_mm"]
TARGET_COLS  = ["NO2_ugm3","PM25_ugm3"]

fieldnames = (["date","station_code","station_name","station_type","lat","lon","covid_period"]
              + WEATHER_COLS + static_cols + TARGET_COLS)

rows_written = 0
rows_missing_aq = 0

with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    for code in sorted(aq_data.keys(), key=int):
        meta    = aq_meta.get(code, {})
        weather = metobs_daily.get(code, {})
        static  = static_feats.get(code, {})

        station_rows = 0
        for date_str in all_dates:
            aq_row = aq_data[code].get(date_str, {})
            no2  = aq_row.get("NO2")
            pm25 = aq_row.get("PM25")

            # Skip rows where both targets are missing
            if no2 is None and pm25 is None:
                rows_missing_aq += 1
                continue

            w = weather.get(date_str, {})
            row = {
                "date":          date_str,
                "station_code":  code,
                "station_name":  meta.get("name",""),
                "station_type":  meta.get("type",""),
                "lat":           meta.get("lat",""),
                "lon":           meta.get("lon",""),
                "covid_period":  covid_flag(date_str),
                "temp_C":        w.get("temp_C",""),
                "wind_speed_ms": w.get("wind_speed_ms",""),
                "wind_dir_deg":  w.get("wind_dir_deg",""),
                "rh_pct":        w.get("rh_pct",""),
                "precip_mm":     w.get("precip_mm",""),
                "NO2_ugm3":      no2 if no2 is not None else "",
                "PM25_ugm3":     pm25 if pm25 is not None else "",
            }
            row.update(static)
            writer.writerow(row)
            station_rows += 1
            rows_written += 1

        print(f"  {code:>7}  {meta.get('name',''):<35}  {station_rows} rows")

print(f"\nTotal rows written  : {rows_written:,}")
print(f"Rows skipped (no AQ): {rows_missing_aq:,}")
print(f"Output: {OUT_PATH}")
EOF