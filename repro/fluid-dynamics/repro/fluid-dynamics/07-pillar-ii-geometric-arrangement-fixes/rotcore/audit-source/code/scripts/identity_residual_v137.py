# -*- coding: utf-8 -*-
"""identity_residual_v137.py — summary of identity residual from metrics_long_v137.csv"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

df = pd.read_csv(DATA / "metrics_long_v137.csv")
rows = []
for (case, method), g in df.groupby(["case","method"]):
    lhs = g["N_star"] * (g["r_meas"]**2)
    rhs = g["phi"] * g["s"] * (g["L_core"]**2)
    resid = abs(lhs - rhs) / (rhs + 1e-12)
    rows.append({
        "case": case,
        "method": method,
        "n": int(len(g)),
        "median_resid_percent": float(np.median(resid) * 100.0),
        "mean_resid_percent": float(np.mean(resid) * 100.0)
    })
out = pd.DataFrame(rows)
out.to_csv(DATA / "identity_resid_v137.csv", index=False)
print("Wrote data/identity_resid_v137.csv")
