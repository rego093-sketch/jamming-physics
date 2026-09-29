import argparse, sys
from pathlib import Path
import pandas as pd
import numpy as np

def ols_slope(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    A = np.vstack([x, np.ones_like(x)]).T
    beta, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    return float(beta), float(intercept)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Assertions for JFM v4/v3 reproducibility")
    p.add_argument("--v3-root", default="v3", help="Path where JFM_DOI_FULLSTORY_v3.zip is unpacked")
    p.add_argument("--tol", type=float, default=0.02, help="Tolerance for |beta-0.5| assertion on synthetic GT")
    args = p.parse_args()

    v3 = Path(args.v3_root)
    syn_csv = v3 / "source_data" / "Synthetic_k6.csv"
    alt_syn = v3 / "source_data" / "Synthetic_k6_DNSlike.csv"
    if not syn_csv.exists() and alt_syn.exists():
        syn_csv = alt_syn

    if not syn_csv.exists():
        print(f"[FAIL] Synthetic dataset not found: {syn_csv} or {alt_syn}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(syn_csv)
    # Expect columns: S, L_star, logS, logL
    cols = set(df.columns.str.strip().tolist())
    need = {"logS", "logL"}
    if not need.issubset(cols):
        print(f"[FAIL] Required columns {need} not in {cols}", file=sys.stderr)
        sys.exit(1)

    beta, b0 = ols_slope(df["logS"], df["logL"])
    dev = abs(beta - 0.5)

    # Soft check on demo outputs (not asserting any particular slope there)
    demo_csv = Path("data") / "dns_runs" / "dns_suite_with_Sb.csv"
    demo_exists = demo_csv.exists()

    print(f"[INFO] Synthetic slope beta={beta:.5f} (target 0.5), intercept={b0:.5f}, |beta-0.5|={dev:.5f}")
    if dev > args.tol:
        print(f"[FAIL] |beta-0.5|={dev:.5f} exceeds tol={args.tol}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[PASS] Synthetic ground-truth assertion OK within tol={args.tol}")

    if demo_exists:
        try:
            ddf = pd.read_csv(demo_csv)
            print(f"[INFO] Demo suite rows={len(ddf)}, columns={list(ddf.columns)}")
        except Exception as e:
            print(f"[WARN] Could not parse demo output {demo_csv}: {e}", file=sys.stderr)

    sys.exit(0)
