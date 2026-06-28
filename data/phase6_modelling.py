"""Phase 6: Buffered SLOO · RF / LUR / IDW · Decay curve analysis."""

import os, sys, math
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.stdout.reconfigure(encoding='utf-8')

# ── Paths ─────────────────────────────────────────────────────────
BASE        = "C:/Users/aziz_/Documents/mau-thesis"
DATA_PATH   = f"{BASE}/data/processed/feature_matrix_clean.csv"
DIST_PATH   = f"{BASE}/data/raw/metobs/distance_matrix.csv"
RESULTS_DIR = f"{BASE}/data/results"
FIGURES_DIR = f"{BASE}/writing/images"

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# ── Config ────────────────────────────────────────────────────────
SLOO_BUFFER_KM = 5.0
RF_PARAMS = dict(n_estimators=200, random_state=42, n_jobs=-1, min_samples_leaf=5)

# 11 stations passing ≥90% completeness for both pollutants concurrently
PASSING = {"102","8773","8780","8781","18643","20415","32423",
           "156417","157992","159404","181993"}

# ── Load feature matrix ───────────────────────────────────────────
print("=" * 60)
print("Loading data")
print("=" * 60)
df = pd.read_csv(DATA_PATH, dtype={'station_code': str})
df['station_code'] = df['station_code'].astype(str)
print(f"  Shape: {df.shape}")
print(f"  Columns: {list(df.columns)}")

ID_COLS     = ['date', 'station_code', 'station_name', 'station_type']
TARGET_COLS = ['NO2_ugm3', 'PM25_ugm3']
DROP_COLS   = set(ID_COLS + TARGET_COLS + ['precip_observed'])
FEAT_COLS   = [c for c in df.columns if c not in DROP_COLS]
print(f"\n  Feature columns ({len(FEAT_COLS)}): {FEAT_COLS}")

# ── Load distance matrix ──────────────────────────────────────────
dist_df = pd.read_csv(DIST_PATH, index_col=0)
dist_df.index   = dist_df.index.astype(str)
dist_df.columns = dist_df.columns.astype(str)
all_codes = df['station_code'].unique().tolist()

def excluded_by_buffer(test_code):
    excl = {test_code}
    for code in all_codes:
        if code == test_code:
            continue
        try:
            if float(dist_df.loc[test_code, code]) <= SLOO_BUFFER_KM:
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

# ── IDW (vectorised per fold) ─────────────────────────────────────
def idw_fold(test_code, train_codes, target_col, data, power=2):
    """
    Returns Series indexed by date with IDW predictions for test_code.
    On each day uses only training stations with a non-null target value.
    """
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

    pivot = train_df.pivot_table(
        index='date', columns='station_code', values=target_col, aggfunc='first'
    )
    cols  = [c for c in pivot.columns if c in weights_dict]
    w_arr = np.array([weights_dict[c] for c in cols])
    vals  = pivot[cols].values.astype(float)    # (n_dates, n_train)

    nan_mask    = np.isnan(vals)
    numerator   = np.nansum(vals * w_arr, axis=1)
    denominator = np.where(nan_mask, 0.0, w_arr).sum(axis=1)

    with np.errstate(invalid='ignore', divide='ignore'):
        preds = np.where(denominator > 0, numerator / denominator, np.nan)

    return pd.Series(preds, index=pivot.index, name='IDW')

# ── Metrics ───────────────────────────────────────────────────────
def metrics(actual, predicted):
    a = np.asarray(actual, dtype=float)
    p = np.asarray(predicted, dtype=float)
    mask = ~(np.isnan(a) | np.isnan(p))
    n = mask.sum()
    if n < 5:
        return dict(RMSE=np.nan, MAE=np.nan, R2=np.nan, n=int(n))
    rmse = math.sqrt(mean_squared_error(a[mask], p[mask]))
    mae  = mean_absolute_error(a[mask], p[mask])
    r2   = r2_score(a[mask], p[mask])
    return dict(RMSE=round(rmse, 3), MAE=round(mae, 3), R2=round(r2, 3), n=int(n))

# ── AIC / BIC ─────────────────────────────────────────────────────
def aic_bic(residuals, k):
    n   = len(residuals)
    rss = float(np.sum(residuals ** 2))
    if rss <= 0 or n <= k:
        return np.nan, np.nan
    ll  = -n / 2 * math.log(rss / n) - n / 2 * (1 + math.log(2 * math.pi))
    aic = -2 * ll + 2 * k
    bic = -2 * ll + k * math.log(n)
    return round(aic, 3), round(bic, 3)

# ── SLOO loop ─────────────────────────────────────────────────────
def run_sloo(target_col, data):
    label = "NO2" if "NO2" in target_col else "PM25"
    unit  = "µg/m³"
    print(f"\n{'='*60}")
    print(f"Buffered SLOO: {label}  (buffer={SLOO_BUFFER_KM} km, n_stations={len(PASSING)})")
    print(f"{'='*60}")

    station_records = []
    all_predictions = []

    for test_code in sorted(PASSING):
        excl        = excluded_by_buffer(test_code)
        train_codes = [c for c in all_codes if c not in excl]
        nn_dist     = dist_to_nearest(test_code, train_codes)

        test_data  = data[data['station_code'] == test_code].copy()
        train_data = data[data['station_code'].isin(train_codes)].copy()

        test_valid  = test_data.dropna(subset=[target_col])
        train_valid = train_data.dropna(subset=[target_col])

        stn_name = test_data['station_name'].iloc[0] if len(test_data) else test_code
        stn_type = test_data['station_type'].iloc[0] if len(test_data) else ''

        if len(train_valid) < 20 or len(test_valid) < 10:
            print(f"  {test_code} {stn_name[:28]}: skipped (train={len(train_valid)}, test={len(test_valid)})")
            continue

        X_tr = train_valid[FEAT_COLS].values.astype(float)
        y_tr = train_valid[target_col].values
        X_te = test_valid[FEAT_COLS].values.astype(float)
        y_te = test_valid[target_col].values

        imp = SimpleImputer(strategy='median')
        X_tr = imp.fit_transform(X_tr)
        X_te = imp.transform(X_te)

        # ── Random Forest ─────────────────────────────────────────
        rf = RandomForestRegressor(**RF_PARAMS)
        rf.fit(X_tr, y_tr)
        pred_rf = rf.predict(X_te)
        m_rf = metrics(y_te, pred_rf)

        # ── LUR (linear regression, same features) ────────────────
        lur = LinearRegression()
        lur.fit(X_tr, y_tr)
        pred_lur = lur.predict(X_te)
        m_lur = metrics(y_te, pred_lur)

        # ── IDW ───────────────────────────────────────────────────
        idw_series = idw_fold(test_code, train_codes, target_col, data)
        pred_idw   = test_valid['date'].map(idw_series).values.astype(float)
        m_idw = metrics(y_te, pred_idw)

        print(f"\n  {test_code} {stn_name[:30]:<30} [{stn_type}]")
        print(f"    nn={nn_dist:.1f} km  n_train_stns={len(train_codes)}  n_test_days={len(test_valid)}")
        print(f"    RF:  RMSE={m_rf['RMSE']}  MAE={m_rf['MAE']}  R²={m_rf['R2']}")
        print(f"    LUR: RMSE={m_lur['RMSE']}  MAE={m_lur['MAE']}  R²={m_lur['R2']}")
        print(f"    IDW: RMSE={m_idw['RMSE']}  MAE={m_idw['MAE']}  R²={m_idw['R2']}")

        station_records.append({
            'station_code': test_code,
            'station_name': stn_name,
            'station_type': stn_type,
            'pollutant':    label,
            'nn_dist_km':   round(nn_dist, 1),
            'n_train_stns': len(train_codes),
            'n_test_days':  len(test_valid),
            'RF_RMSE':  m_rf['RMSE'],  'RF_MAE':  m_rf['MAE'],  'RF_R2':  m_rf['R2'],
            'LUR_RMSE': m_lur['RMSE'], 'LUR_MAE': m_lur['MAE'], 'LUR_R2': m_lur['R2'],
            'IDW_RMSE': m_idw['RMSE'], 'IDW_MAE': m_idw['MAE'], 'IDW_R2': m_idw['R2'],
        })

        for i in range(len(y_te)):
            all_predictions.append({
                'station_code': test_code,
                'date':   test_valid['date'].iloc[i],
                'actual': y_te[i],
                'RF':     float(pred_rf[i]),
                'LUR':    float(pred_lur[i]),
                'IDW':    float(pred_idw[i]) if i < len(pred_idw) else np.nan,
            })

    return pd.DataFrame(station_records), pd.DataFrame(all_predictions)

# ── Run SLOO: full period (2020-2024) ────────────────────────────
metrics_no2,  preds_no2  = run_sloo('NO2_ugm3',  df)
metrics_pm25, preds_pm25 = run_sloo('PM25_ugm3', df)
metrics_no2['period']  = '2020-2024'
metrics_pm25['period'] = '2020-2024'

# ── COVID sensitivity: 2022-2024 only ────────────────────────────
print("\n" + "=" * 60)
print("COVID sensitivity: SLOO restricted to 2022-2024")
print("=" * 60)
df_post = df[df['covid_period'] == 0].copy()
sens_no2,  _ = run_sloo('NO2_ugm3',  df_post)
sens_pm25, _ = run_sloo('PM25_ugm3', df_post)
sens_no2['period']  = '2022-2024'
sens_pm25['period'] = '2022-2024'

# ── Traffic vs. Background stratification ─────────────────────────
print("\n" + "=" * 60)
print("Traffic vs. Background stratification")
print("=" * 60)

strat_rows = []
for label, mdf in [('NO2', metrics_no2), ('PM25', metrics_pm25)]:
    is_traffic = mdf['station_type'].str.contains('Traffic', case=False, na=False)
    for grp_name, grp in [('Traffic', mdf[is_traffic]), ('Background', mdf[~is_traffic])]:
        if grp.empty:
            continue
        print(f"  {label} {grp_name:12} (n={len(grp)}): "
              f"RF={grp['RF_RMSE'].mean():.3f}  "
              f"LUR={grp['LUR_RMSE'].mean():.3f}  "
              f"IDW={grp['IDW_RMSE'].mean():.3f}")
        strat_rows.append({
            'pollutant': label, 'group': grp_name, 'n': len(grp),
            'RF_RMSE_mean':  round(grp['RF_RMSE'].mean(), 3),
            'LUR_RMSE_mean': round(grp['LUR_RMSE'].mean(), 3),
            'IDW_RMSE_mean': round(grp['IDW_RMSE'].mean(), 3),
            'RF_R2_mean':    round(grp['RF_R2'].mean(), 3),
        })

# ── Seasonal stratification (winter Nov-Apr / summer May-Oct) ─────
print("\n" + "=" * 60)
print("Seasonal stratification")
print("=" * 60)

for label, preds_df in [('NO2', preds_no2), ('PM25', preds_pm25)]:
    preds_df['month'] = pd.to_datetime(preds_df['date']).dt.month
    preds_df['season'] = preds_df['month'].apply(
        lambda m: 'Winter (Nov-Apr)' if m in (11, 12, 1, 2, 3, 4) else 'Summer (May-Oct)'
    )
    print(f"\n  {label}")
    for season, grp in preds_df.groupby('season'):
        m_rf  = metrics(grp['actual'].values, grp['RF'].values)
        m_lur = metrics(grp['actual'].values, grp['LUR'].values)
        m_idw = metrics(grp['actual'].values, grp['IDW'].values)
        print(f"    {season}: RF RMSE={m_rf['RMSE']}  LUR={m_lur['RMSE']}  IDW={m_idw['RMSE']}  n={m_rf['n']:,}")
        strat_rows.append({
            'pollutant': label, 'group': season, 'n': m_rf['n'],
            'RF_RMSE_mean':  m_rf['RMSE'],
            'LUR_RMSE_mean': m_lur['RMSE'],
            'IDW_RMSE_mean': m_idw['RMSE'],
            'RF_R2_mean':    m_rf['R2'],
        })

# ── Decay curve fitting ───────────────────────────────────────────
print("\n" + "=" * 60)
print("Decay curve fitting (log / power / exponential)")
print("=" * 60)

def fit_decay(metrics_df, label):
    rows = []
    d_all = metrics_df['nn_dist_km'].values.astype(float)

    for model in ['RF', 'LUR', 'IDW']:
        rmse_all = metrics_df[f'{model}_RMSE'].values.astype(float)
        mask = ~(np.isnan(d_all) | np.isnan(rmse_all)) & (d_all > 0) & (rmse_all > 0)
        if mask.sum() < 4:
            print(f"  {label} {model}: only {mask.sum()} valid points — skipping")
            continue
        d, r = d_all[mask], rmse_all[mask]
        ln_d, ln_r = np.log(d), np.log(r)

        # Log:   RMSE = a + b·ln(d)
        c = np.polyfit(ln_d, r, 1)
        pred = c[0] * ln_d + c[1]
        aic_l, bic_l = aic_bic(r - pred, 2)
        rows.append({'pollutant': label, 'model': model, 'form': 'log',
                     'a': round(c[1], 4), 'b': round(c[0], 4),
                     'AIC': aic_l, 'BIC': bic_l, 'n': int(mask.sum())})

        # Power: RMSE = a·d^b  →  ln(RMSE) = ln(a) + b·ln(d)
        c = np.polyfit(ln_d, ln_r, 1)
        a_p, b_p = math.exp(c[1]), c[0]
        pred = a_p * (d ** b_p)
        aic_p, bic_p = aic_bic(r - pred, 2)
        rows.append({'pollutant': label, 'model': model, 'form': 'power',
                     'a': round(a_p, 4), 'b': round(b_p, 4),
                     'AIC': aic_p, 'BIC': bic_p, 'n': int(mask.sum())})

        # Exponential: RMSE = a·e^(b·d)  →  ln(RMSE) = ln(a) + b·d
        c = np.polyfit(d, ln_r, 1)
        a_e, b_e = math.exp(c[1]), c[0]
        pred = a_e * np.exp(b_e * d)
        aic_e, bic_e = aic_bic(r - pred, 2)
        rows.append({'pollutant': label, 'model': model, 'form': 'exponential',
                     'a': round(a_e, 4), 'b': round(b_e, 6),
                     'AIC': aic_e, 'BIC': bic_e, 'n': int(mask.sum())})

        best = min(
            [('log', aic_l), ('power', aic_p), ('exponential', aic_e)],
            key=lambda x: x[1] if not math.isnan(x[1]) else math.inf
        )
        print(f"  {label} {model:<4}  n={mask.sum()}  "
              f"log AIC={aic_l}  power AIC={aic_p}  exp AIC={aic_e}  "
              f"→ best: {best[0]}")

    return pd.DataFrame(rows)

decay_no2  = fit_decay(metrics_no2,  'NO2')
decay_pm25 = fit_decay(metrics_pm25, 'PM25')
decay_all  = pd.concat([decay_no2, decay_pm25], ignore_index=True)

# ── Figures ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Generating figures")
print("=" * 60)

COLORS = {'RF': '#2166ac', 'LUR': '#d6604d', 'IDW': '#4dac26'}

def plot_decay_curves(metrics_df, decay_df, label):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f'{label} — Error vs. Distance (Buffered SLOO)', fontsize=13)

    d_max = metrics_df['nn_dist_km'].max()
    d_range = np.linspace(1, d_max + 20, 300)

    for ax, model in zip(axes, ['RF', 'LUR', 'IDW']):
        d    = metrics_df['nn_dist_km'].values.astype(float)
        rmse = metrics_df[f'{model}_RMSE'].values.astype(float)
        mask = ~(np.isnan(d) | np.isnan(rmse))

        ax.scatter(d[mask], rmse[mask], color=COLORS[model], zorder=5,
                   s=70, label='Per-station RMSE')

        sub = decay_df[(decay_df['model'] == model) & (decay_df['pollutant'] == label)]
        if not sub.empty:
            best = sub.loc[sub['AIC'].dropna().index[sub['AIC'].dropna().values.argmin()]]
            a, b, form = best['a'], best['b'], best['form']
            if form == 'log':
                y_fit = a + b * np.log(d_range)
            elif form == 'power':
                y_fit = a * (d_range ** b)
            else:
                y_fit = a * np.exp(b * d_range)
            ax.plot(d_range, y_fit, color=COLORS[model], lw=2,
                    label=f'{form} fit (AIC={best["AIC"]:.1f})')

        ax.set_xlabel('Distance to nearest training station (km)')
        ax.set_ylabel('RMSE (µg/m³)')
        ax.set_title(model)
        ax.set_ylim(bottom=0)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = f"{FIGURES_DIR}/fig_decay_{label.lower()}.png"
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")

def plot_metrics_bar(m_no2, m_pm25):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, (label, mdf) in zip(axes, [('NO2', m_no2), ('PM2.5', m_pm25)]):
        x   = np.arange(len(mdf))
        w   = 0.25
        names = [n[:14] for n in mdf['station_name']]
        ax.bar(x - w, mdf['RF_RMSE'],  w, label='RF',  color=COLORS['RF'])
        ax.bar(x,     mdf['LUR_RMSE'], w, label='LUR', color=COLORS['LUR'])
        ax.bar(x + w, mdf['IDW_RMSE'], w, label='IDW', color=COLORS['IDW'])
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax.set_ylabel('RMSE (µg/m³)')
        ax.set_title(f'{label} — Per-station RMSE by model')
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    path = f"{FIGURES_DIR}/fig_metrics_comparison.png"
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")

def plot_scatter(preds_df, label):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f'{label} — Predicted vs. Actual (all SLOO folds)', fontsize=13)
    for ax, model in zip(axes, ['RF', 'LUR', 'IDW']):
        sub  = preds_df.dropna(subset=['actual', model])
        lim  = max(sub['actual'].max(), sub[model].max()) * 1.05
        ax.scatter(sub['actual'], sub[model], alpha=0.15, s=8, color='#555555', rasterized=True)
        ax.plot([0, lim], [0, lim], 'r--', lw=1)
        ax.set_xlabel(f'Actual {label} (µg/m³)')
        ax.set_ylabel(f'Predicted {label} (µg/m³)')
        ax.set_title(model)
        ax.set_xlim(left=0); ax.set_ylim(bottom=0)
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = f"{FIGURES_DIR}/fig_scatter_{label.lower()}.png"
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")

plot_decay_curves(metrics_no2,  decay_all, 'NO2')
plot_decay_curves(metrics_pm25, decay_all, 'PM25')
plot_metrics_bar(metrics_no2, metrics_pm25)
plot_scatter(preds_no2,  'NO2')
plot_scatter(preds_pm25, 'PM25')

# ── Save results ──────────────────────────────────────────────────
print("\n" + "=" * 60)
print("Saving results")
print("=" * 60)

metrics_full = pd.concat([metrics_no2, metrics_pm25], ignore_index=True)
metrics_full.to_csv(f"{RESULTS_DIR}/station_metrics.csv", index=False)
print(f"  station_metrics.csv ({len(metrics_full)} rows)")

decay_all.to_csv(f"{RESULTS_DIR}/decay_curves.csv", index=False)
print(f"  decay_curves.csv ({len(decay_all)} rows)")

preds_no2.to_csv(f"{RESULTS_DIR}/sloo_predictions_no2.csv", index=False)
preds_pm25.to_csv(f"{RESULTS_DIR}/sloo_predictions_pm25.csv", index=False)
print(f"  sloo_predictions_no2.csv ({len(preds_no2):,} rows)")
print(f"  sloo_predictions_pm25.csv ({len(preds_pm25):,} rows)")

sensitivity = pd.concat([sens_no2, sens_pm25, metrics_no2, metrics_pm25], ignore_index=True)
sensitivity.to_csv(f"{RESULTS_DIR}/covid_sensitivity.csv", index=False)
print(f"  covid_sensitivity.csv ({len(sensitivity)} rows)")

pd.DataFrame(strat_rows).to_csv(f"{RESULTS_DIR}/stratification_summary.csv", index=False)
print(f"  stratification_summary.csv")

print("\n" + "=" * 60)
print("Phase 6 complete.")
print("Output files in: data/results/")
print("Figures in:      writing/images/")
print("=" * 60)
