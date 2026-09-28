"""Resumable AQS yield-stress runner. Per (phi,seed): minimized packing -> AQS shear ->
record yield stress sigma_y (mean |signed stress| over the post-yield plateau) and the elastic
slope (cross-check vs static G_relaxed). Usage: python3 aqs_run.py s0 s1
"""
import sys, os, csv, time
import numpy as np
from relaxed_shear import make_packing, relaxed_G, backbone_mask, mean_z
from le_shear import forces_stress
from aqs import aqs_run

OUT = "/home/claude/vp_shear/results"; CSV = f"{OUT}/aqs_sigmay.csv"
CURVES = f"{OUT}/aqs_curves"; os.makedirs(CURVES, exist_ok=True)
COLS = ["N","phi","seed","z","G_relaxed_static","elastic_slope","sigma_y","sigma_y_std","maxmF"]
N = 128; DG = 0.005; GMAX = 0.20; FSTEPS = 2500; FTOL = 5e-8
PHIS = [0.730, 0.700, 0.675, 0.655, 0.640]
PLATEAU = (0.09, 0.20)   # steady-flow strain window for sigma_y
ELASTIC = 0.008          # gamma below which we fit the elastic slope (avoid first plastic drop)

def done_set():
    s = set()
    if os.path.exists(CSV):
        for r in csv.DictReader(open(CSV)): s.add((int(r["N"]), float(r["phi"]), int(r["seed"])))
    return s

def append(row):
    new = not os.path.exists(CSV)
    with open(CSV, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new: w.writeheader()
        w.writerow(row)

def run(s0, s1, tmax=270):
    done = done_set(); t0 = time.time()
    for sd in range(s0, s1):
        for phi in PHIS:
            if (N, phi, sd) in done: continue
            if time.time() - t0 > tmax: print("[time budget]"); return
            pos, R, E, mF = make_packing(N, phi, 1.0, sd, steps=8000, polish=True)
            if E < 1e-13: continue
            keep = backbone_mask(pos, R, 1.0); z = mean_z(pos, R, 1.0, keep)
            r = relaxed_G(pos, R, 1.0)
            _, _, s0_, _ = forces_stress(pos, R, 1.0, 0.0)
            g, s, mf = aqs_run(pos, R, 1.0, dgamma=DG, gamma_max=GMAX, fire_steps=FSTEPS)
            np.savez(f"{CURVES}/N{N}_phi{phi:.3f}_sd{sd}.npz", g=g, s=s, z=z, s0=s0_)
            # elastic slope from (sigma - sigma0) over small gamma
            el = g <= ELASTIC
            esl = abs(np.polyfit(g[el], (s - s0_)[el], 1)[0]) if el.sum() >= 2 else float("nan")
            pl = (g >= PLATEAU[0]) & (g <= PLATEAU[1])
            sy = float(abs(np.mean(s[pl]))) if pl.any() else float("nan")
            syd = float(np.std(s[pl])) if pl.any() else float("nan")
            append(dict(N=N, phi=phi, seed=sd, z=f"{z:.4f}", G_relaxed_static=f"{r['G_relaxed']:.4f}",
                        elastic_slope=f"{esl:.4f}", sigma_y=f"{sy:.5f}", sigma_y_std=f"{syd:.5f}",
                        maxmF=f"{mf.max():.1e}"))
            print(f"phi={phi:.3f} sd={sd}: z={z:.3f} G_rel(stat)={r['G_relaxed']:.3f} "
                  f"el_slope={esl:.3f} sigma_y={sy:.4f} maxmF={mf.max():.0e} [{time.time()-t0:.0f}s]")
    print(f"[chunk done] {time.time()-t0:.0f}s")

if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]))
