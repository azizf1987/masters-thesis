"""Buffer-distance sensitivity analysis for the buffered SLOO protocol.

Examiner comment (Section 3.3): the 5 km exclusion buffer is far below the
150-200 km spatial autocorrelation range; a small sensitivity test across
feasible buffer distances would strengthen the work.

This script re-runs the exact SLOO loop from phase6_modelling.py (RF / LUR /
IDW, NO2 and PM2.5) for a range of buffer distances and reports the mean
cross-validated error for each. It writes only data/results/buffer_sensitivity.csv
and touches no figure or other result file.
"""

import sys, math
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
sys.stdout.reconfigure(encoding='utf-8')

BASE        = "C:/Users/aziz_/Documents/mau-thesis"
DATA_PATH   = f"{BASE}/data/processed/feature_matrix_clean.csv"
DIST_PATH   = f"{BASE}/data/raw/metobs/distance_matrix.csv"
RESULTS_DIR = f"{BASE}/data/results"

BUFFERS_KM = [0.0, 5.0, 10.0, 25.0, 50.0]   # 5 km is the value adopted in the thesis
RF_PARAMS  = dict(n_estimators=200, random_state=42, n_jobs=-1, min_samples_leaf=5)
PASSING = {"102","8773","8780","8781","18643","20415","32423",
           "156417","157992","159404","181993"}

# ── Load (identical to phase6_modelling.py) ──────────────────────────
df = pd.read_csv(DATA_PATH, dtype={'station_code': str})
df['station_code'] = df['station_code'].astype(str)

ID_COLS     = ['date', 'station_code', 'station_name', 'station_type']
TARGET_COLS = ['NO2_ugm3', 'PM25_ugm3']
DROP_COLS   = set(ID_COLS + TARGET_COLS + ['precip_observed'])
FEAT_COLS   = [c for c in df.columns if c not in DROP_COLS]

dist_df = pd.read_csv(DIST_PATH, index_col=0)
dist_df.index   = dist_df.index.astype(str)
dist_df.columns = dist_df.columns.astype(str)
all_codes = df['station_code'].unique().tolist()


def excluded_by_buffer(test_code, buffer_km):
    excl = {test_code}
    for code in all_codes:
        if code == test_code:
            continue
        try:
            if float(dist_df.loc[test_code, code]) <= buffer_km:
                excl.add(code)
        except KeyError:
            pass
    return excl


def dist_to_nearest(test_code, train_codes):
    dists = []
    for code in train_codes:
        try:
            dists.append(float(dist_df.loc[test_code, code]))
        except KeyError:
            pass
    return min(dists) if dists else np.nan


def idw_fold(test_code, train_codes, target_col, data, power=2):
    weights_dict = {}
    for code in train_codes:
        try:
            d = float(dist_df.loc[test_code, code])
            if d > 0:
                weights_dict[code] = 1.0 / (d ** power)
        except KeyError:
            pass
    if not weights_dict:
        dates = data[data['station_code'] == test_code]['date'].values
        return pd.Series(np.nan, index=pd.Index(dates, name='date'), name='IDW')
    train_df = (data[data['station_code'].isin(weights_dict.keys())]
                [['date', 'station_code', target_col]]
                .dropna(subset=[target_col]))
    pivot = train_df.pivot_table(index='date', columns='station_code',
                                 values=target_col, aggfunc='first')
    cols  = [c for c in pivot.columns if c in weights_dict]
    w_arr = np.array([weights_dict[c] for c in cols])
    vals  = pivot[cols].values.astype(float)
    nan_mask    = np.isnan(vals)
    numerator   = np.nansum(vals * w_arr, axis=1)
    denominator = np.where(nan_mask, 0.0, w_arr).sum(axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        preds = np.where(denominator > 0, numerator / denominator, np.nan)
    return pd.Series(preds, index=pivot.index, name='IDW')


def metrics(actual, predicted):
    a = np.asarray(actual, dtype=float)
    p = np.asarray(predicted, dtype=float)
    mask = ~(np.isnan(a) | np.isnan(p))
    n = mask.sum()
    if n < 5:
        return dict(RMSE=np.nan, MAE=np.nan, R2=np.nan, n=int(n))
    return dict(RMSE=math.sqrt(mean_squared_error(a[mask], p[mask])),
                MAE=mean_absolute_error(a[mask], p[mask]),
                R2=r2_score(a[mask], p[mask]), n=int(n))


def run_sloo(target_col, data, buffer_km):
    label = "NO2" if "NO2" in target_col else "PM25"
    recs = []
    for test_code in sorted(PASSING):
        excl        = excluded_by_buffer(test_code, buffer_km)
        train_codes = [c for c in all_codes if c not in excl]

        test_valid  = data[data['station_code'] == test_code].dropna(subset=[target_col])
        train_valid = data[data['station_code'].isin(train_codes)].dropna(subset=[target_col])
        if len(train_valid) < 20 or len(test_valid) < 10:
            continue

        X_tr = train_valid[FEAT_COLS].values.astype(float)
        y_tr = train_valid[target_col].values
        X_te = test_valid[FEAT_COLS].values.astype(float)
        y_te = test_valid[target_col].values
        imp = SimpleImputer(strategy='median')
        X_tr = imp.fit_transform(X_tr)
        X_te = imp.transform(X_te)

        rf = RandomForestRegressor(**RF_PARAMS); rf.fit(X_tr, y_tr)
        m_rf = metrics(y_te, rf.predict(X_te))
        lur = LinearRegression(); lur.fit(X_tr, y_tr)
        m_lur = metrics(y_te, lur.predict(X_te))
        idw_series = idw_fold(test_code, train_codes, target_col, data)
        pred_idw   = test_valid['date'].map(idw_series).values.astype(float)
        m_idw = metrics(y_te, pred_idw)

        recs.append(dict(station=test_code, n_train_stns=len(train_codes),
                         RF_RMSE=m_rf['RMSE'], RF_MAE=m_rf['MAE'], RF_R2=m_rf['R2'],
                         LUR_RMSE=m_lur['RMSE'], LUR_MAE=m_lur['MAE'], LUR_R2=m_lur['R2'],
                         IDW_RMSE=m_idw['RMSE'], IDW_MAE=m_idw['MAE'], IDW_R2=m_idw['R2']))
    return pd.DataFrame(recs)


rows = []
for buf in BUFFERS_KM:
    print(f"\n{'='*64}\nBuffer = {buf:g} km\n{'='*64}")
    for target in ['NO2_ugm3', 'PM25_ugm3']:
        sd = run_sloo(target, df, buf)
        label = "NO2" if "NO2" in target else "PM25"
        for model in ['RF', 'LUR', 'IDW']:
            rec = dict(
                buffer_km=buf, pollutant=label, model=model,
                n_folds=int(sd[f'{model}_RMSE'].notna().sum()),
                mean_n_train_stns=round(sd['n_train_stns'].mean(), 1),
                min_n_train_stns=int(sd['n_train_stns'].min()),
                mean_RMSE=round(sd[f'{model}_RMSE'].mean(), 3),
                mean_MAE=round(sd[f'{model}_MAE'].mean(), 3),
                mean_R2=round(sd[f'{model}_R2'].mean(), 3),
            )
            rows.append(rec)
            print(f"  {label:5} {model:4}  RMSE={rec['mean_RMSE']:<7} "
                  f"MAE={rec['mean_MAE']:<7} R2={rec['mean_R2']:<7} "
                  f"folds={rec['n_folds']}  min_train_stns={rec['min_n_train_stns']}")

out = pd.DataFrame(rows)
path = f"{RESULTS_DIR}/buffer_sensitivity.csv"
out.to_csv(path, index=False)
print(f"\nSaved: {path}  ({len(out)} rows)")

# Compact wide view: mean RMSE by buffer, per pollutant/model
print("\nMean RMSE by buffer distance:")
piv = out.pivot_table(index=['pollutant', 'model'], columns='buffer_km', values='mean_RMSE')
print(piv.to_string())
