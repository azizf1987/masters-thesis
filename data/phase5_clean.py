"""Phase 5: clean, impute, variogram."""
import csv, math, sys, os
from collections import defaultdict
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')

IN_PATH  = "C:/Users/aziz_/Documents/mau-thesis/data/processed/feature_matrix.csv"
OUT_PATH = "C:/Users/aziz_/Documents/mau-thesis/data/processed/feature_matrix_clean.csv"

with open(IN_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"Loaded {len(rows):,} rows x {len(fieldnames)} columns\n")

# ─── TASK 1: Clip negative AQ values to 0 ───────────────────────
print("TASK 1: Clipping negative AQ values to 0")
clipped = 0
for r in rows:
    for col in ("NO2_ugm3", "PM25_ugm3"):
        if r[col] != "":
            v = float(r[col])
            if v < 0:
                r[col] = "0.0"
                clipped += 1
print(f"  Clipped {clipped} negative readings to 0\n")

# ─── TASK 2: Precipitation imputation ───────────────────────────
print("TASK 2: Precipitation imputation (monthly mean per station)")

monthly_means = defaultdict(list)
for r in rows:
    if r["precip_mm"] != "":
        monthly_means[(r["station_code"], r["date"][5:7])].append(float(r["precip_mm"]))

monthly_clim = {k: round(np.mean(v), 3) for k, v in monthly_means.items()}

national_monthly = defaultdict(list)
for (code, month), vals in monthly_means.items():
    national_monthly[month].extend(vals)
national_clim = {m: round(np.median(v), 3) for m, v in national_monthly.items()}

imputed = 0
for r in rows:
    month = r["date"][5:7]
    code  = r["station_code"]
    if r["precip_mm"] == "":
        r["precip_observed"] = "0"
        key = (code, month)
        r["precip_mm"] = str(monthly_clim.get(key, national_clim.get(month, "0")))
        imputed += 1
    else:
        r["precip_observed"] = "1"

print(f"  Imputed {imputed:,} missing values using monthly station climatology")
print(f"  Added column: precip_observed (1=measured, 0=imputed)")

stn_precip = defaultdict(lambda: {"obs": 0, "imp": 0, "name": ""})
for r in rows:
    c = r["station_code"]
    stn_precip[c]["name"] = r["station_name"]
    if r["precip_observed"] == "1":
        stn_precip[c]["obs"] += 1
    else:
        stn_precip[c]["imp"] += 1

print("\n  Stations with >5% imputed precipitation:")
for code in sorted(stn_precip.keys(), key=int):
    s = stn_precip[code]
    tot = s["obs"] + s["imp"]
    obs_pct = s["obs"] / tot * 100
    if obs_pct < 95:
        print(f"    {code:>7}  {s['name']:<36}  observed={obs_pct:.0f}%  imputed={100-obs_pct:.0f}%")

# ─── TASK 3: Empirical variogram ────────────────────────────────
print("\nTASK 3: Empirical variogram")

PASSING = {"102","8773","8780","8781","18643","20415","32423",
           "156417","157992","159404","181993"}

daily = defaultdict(dict)
for r in rows:
    if r["station_code"] in PASSING:
        no2  = float(r["NO2_ugm3"])  if r["NO2_ugm3"]  != "" else None
        pm25 = float(r["PM25_ugm3"]) if r["PM25_ugm3"] != "" else None
        daily[r["date"]][r["station_code"]] = {
            "NO2": no2, "PM25": pm25,
            "lat": float(r["lat"]), "lon": float(r["lon"])
        }

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    return R * 2 * math.asin(math.sqrt(a))

bins_km    = [0, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
no2_sv     = defaultdict(list)
pm25_sv    = defaultdict(list)

codes = sorted(PASSING)
for date_str, stns in daily.items():
    if len(stns) < 4:
        continue
    for i, ci in enumerate(codes):
        if ci not in stns or stns[ci]["NO2"] is None:
            continue
        for cj in codes[i+1:]:
            if cj not in stns or stns[cj]["NO2"] is None:
                continue
            si, sj = stns[ci], stns[cj]
            dist = haversine_km(si["lat"], si["lon"], sj["lat"], sj["lon"])
            for b in range(len(bins_km) - 1):
                if bins_km[b] <= dist < bins_km[b+1]:
                    no2_sv[b].append((si["NO2"] - sj["NO2"])**2)
                    if si["PM25"] is not None and sj["PM25"] is not None:
                        pm25_sv[b].append((si["PM25"] - sj["PM25"])**2)
                    break

print(f"\n  Distance bin        NO2 gamma(h)   n pairs   PM2.5 gamma(h)   n pairs")
print(f"  {'-'*72}")
for b in range(len(bins_km) - 1):
    label = f"{bins_km[b]}-{bins_km[b+1]} km"
    no2_g  = round(0.5 * np.mean(no2_sv[b]),  2) if no2_sv[b]  else None
    pm25_g = round(0.5 * np.mean(pm25_sv[b]), 3) if pm25_sv[b] else None
    n1 = len(no2_sv[b]); n2 = len(pm25_sv[b])
    ns = f"{no2_g:>12.2f}" if no2_g is not None else f"{'—':>12}"
    ps = f"{pm25_g:>15.3f}" if pm25_g is not None else f"{'—':>15}"
    print(f"  {label:>18}  {ns}  {n1:>8,}  {ps}  {n2:>8,}")

# Estimate range: first bin where gamma reaches 80% of sill
no2_gseries  = [(b, 0.5*np.mean(no2_sv[b]))  for b in range(len(bins_km)-1) if no2_sv[b]]
pm25_gseries = [(b, 0.5*np.mean(pm25_sv[b])) for b in range(len(bins_km)-1) if pm25_sv[b]]

def find_range(gseries, bins):
    sill = max(g for _, g in gseries)
    for b, g in gseries:
        if g >= 0.80 * sill:
            return f"{bins[b]}-{bins[b+1]} km", round(sill, 2)
    return "not reached", round(sill, 2)

no2_range_str,  no2_sill  = find_range(no2_gseries,  bins_km)
pm25_range_str, pm25_sill = find_range(pm25_gseries, bins_km)

print(f"\n  Estimated variogram range (80% of sill):")
print(f"    NO2:   {no2_range_str}   (sill={no2_sill})")
print(f"    PM2.5: {pm25_range_str}  (sill={pm25_sill})")

no2_range_km  = int(no2_range_str.split("-")[0])
pm25_range_km = int(pm25_range_str.split("-")[0])
recommended_buffer = max(no2_range_km, pm25_range_km)
print(f"\n  Recommended SLOO buffer: {recommended_buffer} km")
print(f"  (use the larger of the two ranges to ensure spatial independence for both pollutants)")

# ─── Save cleaned matrix ─────────────────────────────────────────
new_fields = list(fieldnames) + ["precip_observed"]
with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=new_fields)
    writer.writeheader()
    writer.writerows(rows)

size_mb = os.path.getsize(OUT_PATH) / 1024 / 1024
print(f"\nSaved: {OUT_PATH}  ({size_mb:.1f} MB)")
print(f"Shape: {len(rows):,} rows x {len(new_fields)} columns")
