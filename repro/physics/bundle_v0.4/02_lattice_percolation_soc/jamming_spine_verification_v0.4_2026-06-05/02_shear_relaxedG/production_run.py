"""Chunked, resumable ensemble run for relaxed G(z). Appends one CSV row per config.
Usage: python3 production_run.py N s0 s1   (runs seeds [s0,s1) over the fixed phi grid)
Idempotent: skips (N,phi,seed) already present in the CSV.
"""
import sys, os, csv, time
import numpy as np
from relaxed_shear import make_packing, relaxed_G, mean_z, backbone_mask

OUTDIR = "/home/claude/vp_shear/results"
os.makedirs(OUTDIR, exist_ok=True)
CSV = os.path.join(OUTDIR, "relaxedG.csv")
COLS = ["N","phi","seed","jammed","mF","z","nbb","ncontacts","G_Born","G_relaxed","nonaff","psd","residual","accepted"]

PHIS = [0.640, 0.648, 0.658, 0.670, 0.685, 0.705, 0.730, 0.760]

def load_done():
    done = set()
    if os.path.exists(CSV):
        with open(CSV) as f:
            for row in csv.DictReader(f):
                done.add((int(row["N"]), float(row["phi"]), int(row["seed"])))
    return done

def append(row):
    new = not os.path.exists(CSV)
    with open(CSV, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new: w.writeheader()
        w.writerow(row)

def run(N, s0, s1, tmax=270):
    done = load_done(); t0 = time.time(); n = 0
    for sd in range(s0, s1):
        for phi in PHIS:
            if (N, phi, sd) in done: continue
            if time.time() - t0 > tmax:
                print(f"[time budget hit] did {n} configs this call"); return
            pos, R, E, mF = make_packing(N, phi, 1.0, sd, steps=8000, ftol=1e-12, polish=True)
            jammed = E > 1e-13
            if not jammed:
                append(dict(N=N,phi=phi,seed=sd,jammed=0,mF=mF,z=0,nbb=0,ncontacts=0,
                            G_Born="",G_relaxed="",nonaff="",psd="",residual="",accepted=0)); n+=1; continue
            r = relaxed_G(pos, R, 1.0)
            if not r["ok"]:
                append(dict(N=N,phi=phi,seed=sd,jammed=1,mF=mF,z=0,nbb=r["nbb"],ncontacts=0,
                            G_Born="",G_relaxed="",nonaff="",psd="",residual="",accepted=0)); n+=1; continue
            keep = backbone_mask(pos, R, 1.0); z = mean_z(pos, R, 1.0, keep)
            GB, GR = r["G_Born"], r["G_relaxed"]
            conv = mF < 1e-7; psd = bool(r["psd"]); gross = GR < -0.1*abs(GB)
            acc = 1 if (conv and psd and not gross) else 0
            append(dict(N=N,phi=phi,seed=sd,jammed=1,mF=f"{mF:.3e}",z=f"{z:.4f}",nbb=r["nbb"],
                        ncontacts=r["n_contacts"],G_Born=f"{GB:.6f}",G_relaxed=f"{GR:.6f}",
                        nonaff=f"{r['nonaff']:.6f}",psd=int(psd),residual=f"{r['lin_residual']:.2e}",accepted=acc))
            n += 1
            print(f"N={N} phi={phi:.3f} sd={sd}  z={z:6.3f} GB={GB:6.3f} GR={GR:8.4f} acc={acc} mF={mF:.0e}  [{time.time()-t0:.0f}s, {n} done]")
    print(f"[chunk complete] {n} configs this call ({time.time()-t0:.0f}s)")

if __name__ == "__main__":
    N = int(sys.argv[1]); s0 = int(sys.argv[2]); s1 = int(sys.argv[3])
    run(N, s0, s1)
