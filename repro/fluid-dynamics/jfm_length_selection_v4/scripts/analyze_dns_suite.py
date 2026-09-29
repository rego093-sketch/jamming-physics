
import numpy as np, json, csv
from pathlib import Path
import pandas as pd

def load_suite(indir):
    rows = []
    for npz in sorted(Path(indir).glob("run_*.npz")):
        data = np.load(npz, allow_pickle=True)
        stats = json.loads(str(data["stats"]))
        rows.append({"run": int(npz.stem.split("_")[1]), **stats})
    df = pd.DataFrame(rows).sort_values("run")
    return df

def compute_Sb(df, L0=1.0, theta_deg=30.0, wE=0.20, nu=1e-3, alpha=5e-3):
    # Simple mapping consistent with paper nomenclature:
    #   C^2 ~ geometric factor ~ (theta in radians)^2
    #   E   ~ injected energy density proxy ~ A2_mean
    #   r+eps0 ~ binding/drag ~ (nu*k0^2 + alpha) with k0=8 (same as forcing center)
    theta = np.deg2rad(theta_deg)
    C2 = theta**2 * np.ones(len(df))
    E = df["A2_mean"].to_numpy()
    k0 = 8.0
    r_eps0 = nu*(k0**2) + alpha
    sigma_eff = C2 + wE*E
    eps_bind = r_eps0 * np.ones_like(E)
    S = sigma_eff/eps_bind
    Sb = S/(L0**2)
    out = df.copy()
    out["Sb"] = Sb
    return out

def slope_loglog(df):
    x = np.log(df["Sb"].to_numpy())
    y = np.log(df["L_star"].to_numpy())
    # simple OLS on tiny set (demo)
    A = np.vstack([x, np.ones_like(x)]).T
    beta, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    return float(beta), float(intercept)

if __name__ == "__main__":
    indir = "data/dns_runs"
    df = load_suite(indir)
    df = compute_Sb(df)
    beta, b0 = slope_loglog(df)
    df.to_csv("data/dns_runs/dns_suite_with_Sb.csv", index=False)
    with open("data/dns_runs/slope.txt", "w") as f:
        f.write(f"beta = {beta:.3f}, intercept = {b0:.3f}\n")
    print(f"beta = {beta:.3f}, intercept = {b0:.3f}")
