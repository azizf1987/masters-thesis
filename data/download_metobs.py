"""
Download meteorological covariates from the SMHI Open Data API (metobs).

For each of the 34 air quality stations in the thesis dataset this script:
  1. Queries the SMHI metobs API to discover all stations measuring each parameter
  2. Finds the nearest met station to each AQ station
  3. Downloads hourly data for 2020-2024 from the corrected-archive period
  4. Saves one merged CSV per AQ station

Usage:
    python data/download_metobs.py

Output:
    data/raw/metobs/<aq_code>_metobs.csv   (one file per AQ station)
    data/raw/metobs/download_log.csv       (summary: which met station used, distance, row count)

Notes:
  - All timestamps are UTC. The AQ data from Luftwebb uses UTC+1 (Swedish normal time).
    Align timezones before merging in Phase 5.
  - A met station is selected per parameter independently. The same met station may
    serve multiple parameters for a given AQ station.
  - If a file already exists it is skipped. Delete it to re-download.
"""

import requests
import math
import time
import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://opendata-download-metobs.smhi.se/api/version/1.0"

# SMHI metobs parameter IDs and output column names
PARAMETERS = {
    1:  "air_temperature_C",
    4:  "wind_speed_ms",
    3:  "wind_direction_deg",
    6:  "relative_humidity_pct",
    5:  "precipitation_mm",
}

START_YEAR = 2020
END_YEAR   = 2024

# Millisecond timestamps for study period boundary checks
import datetime as _dt
_START_MS = int(_dt.datetime(START_YEAR, 1, 1).timestamp() * 1000)
_END_MS   = int(_dt.datetime(END_YEAR + 1, 1, 1).timestamp() * 1000)

REQUEST_DELAY = 0.25   # seconds between API calls — be polite
RETRY_DELAY   = 5.0    # seconds before retrying a failed request
MAX_RETRIES   = 2

OUTPUT_DIR = Path(__file__).parent / "raw" / "metobs"

# ---------------------------------------------------------------------------
# All 34 AQ stations (Phase 4 audit 2026-06-17)
# ---------------------------------------------------------------------------

AQ_STATIONS = [
    # --- Skåne ---
    {"code": "8773",   "name": "Malmö Rådhuset",                  "lat": 55.606388, "lon": 13.001964},
    {"code": "8813",   "name": "Malmö Dalaplan",                   "lat": 55.584747, "lon": 13.00623},
    {"code": "38350",  "name": "Lund Trollebergsvägen",            "lat": 55.703335, "lon": 13.180275},
    # --- Kalmar ---
    {"code": "181993", "name": "Kalmar Södra Vägen",               "lat": 56.664192, "lon": 16.33362},
    # --- Kronoberg ---
    {"code": "181002", "name": "Växjö Liedbergsgatan",             "lat": 56.879883, "lon": 14.799273},
    # --- Halland ---
    {"code": "8105",   "name": "Råö",                              "lat": 57.3937,   "lon": 11.9142},
    {"code": "369485", "name": "Varberg Västra Vallgatan",         "lat": 57.105484, "lon": 12.24852},
    # --- Västra Götaland ---
    {"code": "11636",  "name": "Göteborg Haga",                    "lat": 57.697857, "lon": 11.960547},
    # --- Östergötland ---
    {"code": "338685", "name": "Linköping Hamngatan",              "lat": 58.41239,  "lon": 15.630079},
    {"code": "301111", "name": "Norrköping Kungsgatan",            "lat": 58.591515, "lon": 16.177876},
    {"code": "301113", "name": "Norrköping Trädgårdsgatan",        "lat": 58.59204,  "lon": 16.189333},
    # --- Värmland ---
    {"code": "343956", "name": "Karlstad Jungmansgatan",           "lat": 59.376675, "lon": 13.490342},
    # --- Stockholm ---
    {"code": "363072", "name": "Botkyrka Kumla",                   "lat": 59.236626, "lon": 17.836193},
    {"code": "8780",   "name": "Stockholm Hornsgatan",             "lat": 59.31726,  "lon": 18.049023},
    {"code": "8781",   "name": "Stockholm Torkel Knutssongatan",   "lat": 59.316006, "lon": 18.057808},
    {"code": "18644",  "name": "Stockholm Lilla Essingen",         "lat": 59.32554,  "lon": 18.004381},
    {"code": "8779",   "name": "Stockholm Sveavägen",              "lat": 59.34084,  "lon": 18.058279},
    {"code": "157992", "name": "Stockholm St Eriksgatan",          "lat": 59.34056,  "lon": 18.037039},
    {"code": "164905", "name": "Solna Råsundavägen",               "lat": 59.365116, "lon": 17.996862},
    {"code": "428510", "name": "Solna Enköpingsvägen",             "lat": 59.37687,  "lon": 18.006},
    {"code": "301757", "name": "Sundbyberg Tulegatan",             "lat": 59.364258, "lon": 17.976278},
    {"code": "20415",  "name": "Sollentuna E4 Häggvik",            "lat": 59.442196, "lon": 17.923315},
    {"code": "18643",  "name": "Norr Malma",                       "lat": 59.832382, "lon": 18.631313},
    # --- Västmanland ---
    {"code": "344172", "name": "Västerås Stora Gatan",             "lat": 59.6077,   "lon": 16.535915},
    {"code": "155530", "name": "Västerås Melkertorget",            "lat": 59.60987,  "lon": 16.550459},
    # --- Uppsala ---
    {"code": "156417", "name": "Uppsala Kungsgatan",               "lat": 59.85723,  "lon": 17.646107},
    {"code": "159404", "name": "Uppsala Dragarbrunnsgatan",        "lat": 59.86052,  "lon": 17.637596},
    # --- Gävleborg ---
    {"code": "338683", "name": "Gävle Staketgatan",                "lat": 60.676167, "lon": 17.137638},
    # --- Västernorrland ---
    {"code": "32423",  "name": "Sundsvall Köpmangatan",            "lat": 62.38856,  "lon": 17.30889},
    {"code": "144",    "name": "Timrå",                            "lat": 62.48678,  "lon": 17.324438},
    {"code": "363450", "name": "Härnösand Storgatan",              "lat": 62.629883, "lon": 17.935776},
    # --- Jämtland ---
    {"code": "181259", "name": "Östersund Rådhusgatan",            "lat": 63.17391,  "lon": 14.641086},
    {"code": "102",    "name": "Bredkälen",                        "lat": 63.845497, "lon": 15.319731},
    # --- Västerbotten ---
    {"code": "13532",  "name": "Umeå Västra Esplanaden",           "lat": 63.828857, "lon": 20.258492},
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def api_get(url):
    """GET with simple retry logic. Returns Response or None on failure."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            r = requests.get(url, timeout=60)
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return None  # station/period does not exist — do not retry
            print(f"    HTTP {r.status_code} — {'retrying' if attempt < MAX_RETRIES else 'giving up'}")
        except requests.RequestException as e:
            print(f"    Network error: {e} — {'retrying' if attempt < MAX_RETRIES else 'giving up'}")
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)
    return None


def get_stations_for_parameter(param_id):
    """Return stations that were operational at any point during START_YEAR–END_YEAR.

    Inclusion rules:
      - Active stations: always included (currently operating).
      - Inactive stations with known from+to: include if period overlaps study window.
      - Inactive stations with unknown from (from=null): include if to > START_YEAR;
        many legacy SMHI stations lack a from timestamp but clearly have historical data.
    """
    url = f"{BASE_URL}/parameter/{param_id}.json"
    r = api_get(url)
    if r is None:
        return []
    result = []
    for s in r.json().get("station", []):
        if s.get("active", False):
            result.append(s)
            continue
        from_ms = s.get("from")
        to_ms   = s.get("to")
        if to_ms is None:
            continue  # no end date at all — cannot assess
        if to_ms <= _START_MS:
            continue  # closed before 2020
        # to > _START_MS: station was still operating at some point in/after 2020
        if from_ms is None or from_ms < _END_MS:
            result.append(s)
    return result


# Parameter IDs where active stations may have only post-2020 data (PST precipitation
# gauges all started ~2023). For these, prefer stations that started before START_YEAR.
_PREFER_EARLY = {5}  # precipitation_mm


def nearest_station(aq_lat, aq_lon, met_stations, param_id=None):
    """Return (station, distance_km) for the nearest station.

    For precipitation (param_id 5): prefer stations that started by START_YEAR,
    because the SMHI PST gauge network only started ~2023 and would give
    2 years of missing data if selected.

    For all other parameters: prefer currently active stations, which reliably
    have full 2020-2024 coverage; fall back to any period-overlap station only
    if no active station exists.
    """
    import datetime as _dt2

    def started_before_study(s):
        """True if the station is likely to have data covering the start of the study period.

        Primary signal: known from-year <= START_YEAR.
        Proxy for inactive stations only: if from is missing or has an invalid
        placeholder timestamp, a to-date >= 2022 implies the station was long-running
        (to = current date is NOT used as proxy for active stations, because active
        stations always have to = current date, which would give false positives).
        """
        f = s.get("from")
        t = s.get("to")
        active = s.get("active", False)
        if f is not None:
            try:
                return _dt2.datetime.fromtimestamp(f / 1000).year <= START_YEAR
            except Exception:
                pass  # invalid placeholder timestamp — fall through
        # from is None or invalid. Use to-date proxy only for inactive stations:
        # an inactive station that ran until 2022+ was almost certainly active pre-2020.
        if not active and t is not None:
            try:
                return _dt2.datetime.fromtimestamp(t / 1000).year >= 2022
            except Exception:
                return False
        return False

    if param_id in _PREFER_EARLY:
        # Precipitation: PST gauges started 2023 but are "active". Require early start.
        early = [s for s in met_stations if started_before_study(s)]
        pool = early if early else met_stations
    else:
        # Hourly params: prefer stations that predate the study period (likely full coverage).
        # Within that group: active stations first, then inactive ones that ran through 2022+.
        # Fall back to all active, then any period-overlap station.
        early_active   = [s for s in met_stations
                          if s.get("active", False) and started_before_study(s)]
        early_inactive = [s for s in met_stations
                          if not s.get("active", False) and started_before_study(s)]
        early_all  = early_active + early_inactive
        all_active = [s for s in met_stations if s.get("active", False)]
        pool = early_all if early_all else (all_active if all_active else met_stations)

    best, best_dist = None, float("inf")
    for s in pool:
        d = haversine_km(aq_lat, aq_lon, s["latitude"], s["longitude"])
        if d < best_dist:
            best_dist = d
            best = s
    return best, round(best_dist, 1)


def download_parameter_data(param_id, met_station_id):
    """
    Download corrected-archive CSV for one met station + parameter.
    Returns dict {key: value_str} filtered to START_YEAR–END_YEAR, or None.

    Two CSV layouts exist in the SMHI metobs API:
      Hourly  — header starts with "Datum": key = "YYYY-MM-DD HH:MM:SS"
      Daily   — header starts with "Fr"   : key = "YYYY-MM-DD" (precipitation)
    The key format difference is intentional; Phase 5 aligns them when building
    the daily feature matrix.
    """
    url = (f"{BASE_URL}/parameter/{param_id}"
           f"/station/{met_station_id}/period/corrected-archive/data.csv")
    r = api_get(url)
    if r is None:
        return None

    data = {}
    in_data = False
    daily_format = False  # True for aggregated daily params (e.g. precipitation)

    for line in r.text.splitlines():
        line = line.strip().lstrip("﻿")
        if not line:
            continue
        if not in_data:
            if "Datum" in line and ";" in line:
                in_data = True
                # "Från Datum Tid (UTC);..." vs "Datum;Tid (UTC);..."
                daily_format = line.lower().startswith("fr")
            continue

        parts = line.split(";")
        if daily_format:
            # layout: from_dt ; to_dt ; rep_date ; value ; quality
            if len(parts) < 4:
                continue
            date_str = parts[2].strip()  # representative date YYYY-MM-DD
            value    = parts[3].strip()
        else:
            # layout: date ; time ; value ; quality
            if len(parts) < 3:
                continue
            date_str = parts[0].strip()
            time_str = parts[1].strip()
            value    = parts[2].strip()

        try:
            year = int(date_str[:4])
        except (ValueError, IndexError):
            continue
        if START_YEAR <= year <= END_YEAR:
            dt_key = date_str if daily_format else f"{date_str} {time_str}"
            data[dt_key] = value

    return data if data else None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    log_path = OUTPUT_DIR / "download_log.csv"

    print(f"SMHI metobs download — {len(AQ_STATIONS)} AQ stations, "
          f"{len(PARAMETERS)} parameters, {START_YEAR}–{END_YEAR}")
    print(f"Output: {OUTPUT_DIR}\n")

    # --- Step 1: fetch met station lists for each parameter ---
    print("Fetching met station inventories...")
    param_stations = {}
    for pid, label in PARAMETERS.items():
        stations = get_stations_for_parameter(pid)
        param_stations[pid] = stations
        print(f"  Parameter {pid:2d} ({label}): {len(stations)} met stations")
        time.sleep(REQUEST_DELAY)

    # --- Step 2: download data per AQ station ---
    log_rows = []

    for aq in AQ_STATIONS:
        out_path = OUTPUT_DIR / f"{aq['code']}_metobs.csv"

        if out_path.exists():
            print(f"\n[skip] {aq['name']} ({aq['code']}) — file already exists")
            continue

        print(f"\n[{aq['code']}] {aq['name']}")

        param_data  = {}   # pid -> {dt: value}
        meta_lines  = [
            f"# AQ station: {aq['name']} (code {aq['code']})",
            f"# Coordinates: lat={aq['lat']}, lon={aq['lon']}",
            "# Timestamps: UTC  (AQ Luftwebb data uses UTC+1 — align before merging)",
        ]

        for pid, label in PARAMETERS.items():
            nearest, dist_km = nearest_station(
                aq["lat"], aq["lon"], param_stations[pid], param_id=pid
            )
            if nearest is None:
                print(f"  {label}: no met station found")
                continue

            met_name = nearest.get("name", str(nearest["id"]))
            print(f"  {label}: {met_name} ({dist_km} km) ... ", end="", flush=True)

            data = download_parameter_data(pid, nearest["id"])
            time.sleep(REQUEST_DELAY)

            if data is None:
                print("no data")
                log_rows.append({
                    "aq_code": aq["code"], "aq_name": aq["name"],
                    "parameter": label, "met_station": met_name,
                    "distance_km": dist_km, "rows": 0, "status": "failed",
                })
            else:
                print(f"{len(data)} rows")
                param_data[pid] = data
                meta_lines.append(
                    f"# {label}: met station = {met_name} "
                    f"(id {nearest['id']}, {dist_km} km)"
                )
                log_rows.append({
                    "aq_code": aq["code"], "aq_name": aq["name"],
                    "parameter": label, "met_station": met_name,
                    "distance_km": dist_km, "rows": len(data), "status": "ok",
                })

        if not param_data:
            print("  No parameters downloaded — skipping output file")
            continue

        # Merge on union of all datetime keys
        all_dt  = sorted(set(dt for rows in param_data.values() for dt in rows))
        pid_list = sorted(param_data.keys())
        col_names = ["datetime"] + [PARAMETERS[p] for p in pid_list]

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            for m in meta_lines:
                f.write(m + "\n")
            writer = csv.writer(f)
            writer.writerow(col_names)
            for dt in all_dt:
                writer.writerow([dt] + [param_data[p].get(dt, "") for p in pid_list])

        print(f"  Saved {out_path.name}  ({len(all_dt)} hourly rows, "
              f"{len(pid_list)} parameters)")

    # --- Step 3: write download log ---
    if log_rows:
        with open(log_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["aq_code", "aq_name", "parameter",
                               "met_station", "distance_km", "rows", "status"]
            )
            writer.writeheader()
            writer.writerows(log_rows)
        print(f"\nDownload log: {log_path}")

    # --- Summary ---
    completed = [r for r in log_rows if r["status"] == "ok"]
    failed    = [r for r in log_rows if r["status"] == "failed"]
    print(f"\n{'='*50}")
    print(f"Done. {len(completed)} parameter downloads succeeded, "
          f"{len(failed)} failed.")
    if failed:
        print("Failed downloads:")
        for r in failed:
            print(f"  {r['aq_name']} — {r['parameter']}")


if __name__ == "__main__":
    main()
