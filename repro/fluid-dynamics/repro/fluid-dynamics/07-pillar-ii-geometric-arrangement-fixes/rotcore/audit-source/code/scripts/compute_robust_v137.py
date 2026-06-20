# -*- coding: utf-8 -*-
"""compute_robust_v137.py — compute robust metrics from metrics_long_v137.csv"""
import math
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

GLOBAL_SEED = 20251117

df = pd.read_csv(DATA / "metrics_long_v137.csv")
rows = []
for (case, method), g in df.groupby(["case","method"]):
    r_pred = g["r_pred"].to_numpy()
    r_meas = g["r_meas"].to_numpy()
    rel = abs(r_meas - r_pred) / (r_pred + 1e-12)
    mae = float(abs(r_meas - r_pred).mean())
    mape = float(rel.mean() * 100.0)
    rel_med = float(np.median(rel) * 100.0)
    iqr_rel = float((np.percentile(rel,75) - np.percentile(rel,25)) * 100.0)
    rmse = float(math.sqrt(((r_meas - r_pred)**2).mean()))
    nrmse = float(rmse / (np.median(r_pred) + 1e-12) * 100.0)
    rho = float(pd.Series(r_pred).corr(pd.Series(r_meas), method="spearman"))

    # bootstrap
    n_boot = 800
    rng = np.random.default_rng(GLOBAL_SEED)
    idx = np.arange(len(g))
    rel_boot = np.empty(n_boot)
    nrm_boot = np.empty(n_boot)
    for i in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        rb = rel[b]
        rpb = r_pred[b]
        rmb = r_meas[b]
        rel_boot[i] = float(np.median(rb) * 100.0)
        nrm_boot[i] = float(math.sqrt(((rmb - rpb)**2).mean()) / (np.median(rpb) + 1e-12) * 100.0)
    lo_rel, hi_rel = np.percentile(rel_boot, [2.5, 97.5])
    lo_nrm, hi_nrm = np.percentile(nrm_boot, [2.5, 97.5])

    rows.append({
        "case": case,
        "method": method,
        "n": int(len(g)),
        "MAE": mae,
        "MAPE_percent": mape,
        "rel_med_percent": rel_med,
        "rel_IQR_percent": iqr_rel,
        "RMSE": rmse,
        "NRMSE_percent": nrmse,
        "rho_spearman": rho,
        "CI95_rel_med_percent_low": float(lo_rel),
        "CI95_rel_med_percent_high": float(hi_rel),
        "CI95_NRMSE_percent_low": float(lo_nrm),
        "CI95_NRMSE_percent_high": float(hi_nrm)
    })
out = pd.DataFrame(rows)
out.to_csv(DATA / "metrics_robust_v137.csv", index=False)
print("Wrote data/metrics_robust_v137.csv")
