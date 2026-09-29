
import numpy as np, json, csv, os
from pathlib import Path
from dns2d import run_dns

def run_suite(outdir, seed=12345):
    Path(outdir).mkdir(parents=True, exist_ok=True)
    params = []
    # 5 representative amplitudes; other params held fixed
    A0_list = [0.25, 0.35, 0.45, 0.60, 0.80]
    for i, A0 in enumerate(A0_list):
        k, E, stats = run_dns(N=64, L=1.0, dt=0.004, steps=400, save_every=40,
                              nu=1e-3, alpha=5e-3, k0=8.0, sigma_k=0.6,
                              theta_deg=30.0, Omega=1.0, tau=0.6,
                              A0=A0, sigmaA=0.15, seed=seed+i)
        np.savez(Path(outdir)/f"run_{i:02d}.npz", k=k, E=E, stats=json.dumps(stats))
        params.append({"run": i, "A0": A0, **stats})
    # Write metrics CSV
    with open(Path(outdir)/"metrics.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(params[0].keys()))
        w.writeheader(); w.writerows(params)

if __name__ == "__main__":
    run_suite("data/dns_runs")
