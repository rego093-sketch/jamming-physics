# -*- coding: utf-8 -*-
"""coverage_v137.py — coverage within ±10%% / ±20%% from metrics_long_v137.csv"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

df = pd.read_csv(DATA / "metrics_long_v137.csv")
rel = abs(df["r_meas"] - df["r_pred"]) / (df["r_pred"] + 1e-12)
df["rel"] = rel

rows = []
for (case, method), g in df.groupby(["case","method"]):
    cov10 = float((g["rel"] <= 0.10).mean())
    cov20 = float((g["rel"] <= 0.20).mean())
    rows.append({
        "case": case,
        "method": method,
        "n": int(len(g)),
        "coverage_10_percent": cov10,
        "coverage_20_percent": cov20
    })
out = pd.DataFrame(rows)
out.to_csv(DATA / "coverage_v137.csv", index=False)
print("Wrote data/coverage_v137.csv")
