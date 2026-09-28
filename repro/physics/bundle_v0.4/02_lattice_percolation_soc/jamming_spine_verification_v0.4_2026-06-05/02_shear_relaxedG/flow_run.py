"""Resumable flow-curve runner. For each (phi, seed, gdot): generate packing, run overdamped LE
shear, record steady-state stress. Usage: python3 flow_run.py s0 s1   (seeds [s0,s1))."""
import sys, os, csv, time
import numpy as np
from relaxed_shear import make_packing, backbone_mask, mean_z
from le_shear import run_shear

OUT = "/home/claude/vp_shear/results"; CSV = f"{OUT}/flowcurve.csv"
COLS = ["N","phi","seed","gdot","z","sigma_ss","sigma_std","nsteps"]
N = 256; DT = 0.04; GTOT = 3.0; GEQ = 1.0
PHIS = [0.645, 0.660, 0.700]
GDOTS = [0.003, 0.01, 0.03, 0.1]

def done_set():
    s = set()
    if os.path.exists(CSV):
        for r in csv.DictReader(open(CSV)):
            s.add((int(r["N"]), float(r["phi"]), int(r["seed"]), float(r["gdot"])))
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
            # generate once per (phi,seed); reuse for all rates
            todo = [g for g in GDOTS if (N, phi, sd, g) not in done]
            if not todo: continue
            if time.time() - t0 > tmax: print("[time budget]"); return
            pos, R, E, mF = make_packing(N, phi, 1.0, sd, steps=8000, polish=True)
            keep = backbone_mask(pos, R, 1.0); z = mean_z(pos, R, 1.0, keep)
            for gd in todo:
                if time.time() - t0 > tmax: print("[time budget]"); return
                g, s, sm, sd_ = run_shear(pos, R, 1.0, gd, gamma_total=GTOT, dt=DT, gamma_eq=GEQ)
                append(dict(N=N, phi=phi, seed=sd, gdot=gd, z=f"{z:.4f}",
                            sigma_ss=f"{sm:.6f}", sigma_std=f"{sd_:.6f}", nsteps=len(g)))
                print(f"phi={phi:.3f} sd={sd} gdot={gd:6.3f}: z={z:.3f} |sigma|={abs(sm):.4f} steps={len(g)} [{time.time()-t0:.0f}s]")
    print(f"[chunk done] {time.time()-t0:.0f}s")

if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]))
