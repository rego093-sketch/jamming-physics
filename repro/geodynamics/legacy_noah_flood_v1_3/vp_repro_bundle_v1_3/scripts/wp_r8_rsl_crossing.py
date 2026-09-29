from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Tuple, Optional

import pandas as pd

from common import repo_root

TARGET_RSL_M = -5.0

def crossing_age_minus5m(df: pd.DataFrame) -> Optional[float]:
    # expects columns Age_BP (increasing or decreasing) and RSL_m
    if "Age_BP" not in df.columns or "RSL_m" not in df.columns:
        return None
    d = df[["Age_BP", "RSL_m"]].dropna()
    if d.empty:
        return None
    d = d.sort_values("Age_BP", ascending=True)  # older to younger? Age_BP increases to past; keep ascending
    ages = d["Age_BP"].to_numpy()
    rsl = d["RSL_m"].to_numpy()

    # find segment where rsl crosses TARGET (linear interp)
    for i in range(len(rsl) - 1):
        y1, y2 = rsl[i], rsl[i + 1]
        if (y1 - TARGET_RSL_M) == 0:
            return float(ages[i])
        if (y1 - TARGET_RSL_M) * (y2 - TARGET_RSL_M) <= 0:
            # interpolate
            x1, x2 = ages[i], ages[i + 1]
            if y2 == y1:
                return float(x1)
            t = (TARGET_RSL_M - y1) / (y2 - y1)
            return float(x1 + t * (x2 - x1))
    return None

def main() -> int:
    root = repo_root()
    site_dir = root / "data" / "full" / "datasets_v1_2" / "R8_RSL" / "sites_plus"
    out = root / "outputs" / "full" / "r8_rsl_crossing_minus5m.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    rows: List[Tuple[str, str]] = []
    for p in sorted(site_dir.glob("*.csv")):
        df = pd.read_csv(p)
        age = crossing_age_minus5m(df)
        rows.append((p.stem, "" if age is None else f"{age:.3f}"))

    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["site_file_stem", "Age_BP_at_RSL_minus5m_linear_interp"])
        for r in rows:
            w.writerow(list(r))

    print(f"Wrote: {out.relative_to(root).as_posix()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
