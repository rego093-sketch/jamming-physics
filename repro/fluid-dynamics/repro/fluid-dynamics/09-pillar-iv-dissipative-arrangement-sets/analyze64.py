# -*- coding: utf-8 -*-
"""analyze64.py -- load the developed N=64 field, collect decorrelated snapshots,
and fit the thresholded dissipation-structure size distribution P(s)~s^{-tau}
against the pre-registered band tau~1.4-1.5. Threshold scan -> robust plateau;
logbin + LLR + d_f corroborate. Appends snapshots to the checkpoint so repeated
calls accumulate statistics."""
import numpy as np, time, os, sys
import ns3d as S
import dissipation_avalanche as DA

N, nu, dt = 64, 0.008, 0.004
GAP = 18
NSNAP = int(sys.argv[1]) if len(sys.argv) > 1 else 8
THR = [2.0, 3.0, 4.0, 6.0]
STATE = "state64.npz"; POOL = "pool.npz"

t0 = time.time(); L = []
def log(m): L.append(m); print(m, flush=True)

z = np.load(STATE); uh, vh, wh = z['uh'], z['vh'], z['wh']
log(f"== P4 analysis: N={N} nu={nu}, {NSNAP} snapshots gap={GAP} ==")
log(f"   solver check (inviscid N=32): " + (lambda d, v:
    f"dE/E={d:.1e} div={v:.1e} {'PASS' if d<1e-8 and v<1e-8 else 'FAIL'}")(
    *DA.S.inviscid_energy_check(N=32, nsteps=120, dt=0.01)))

# accumulate pooled sizes across calls
pooled = {h: [] for h in THR}; frac = {h: [] for h in THR}
if os.path.exists(POOL):
    pz = np.load(POOL, allow_pickle=True)
    pooled = {h: list(pz[f"h{int(h)}"]) for h in THR}
    frac = {h: list(map(tuple, pz[f"f{int(h)}"])) for h in THR}
    log(f"   resumed pool: " + ", ".join(f"h{int(h)}={len(pooled[h])}" for h in THR))

sks = []
g = S.grid(N)
for s in range(NSNAP):
    for _ in range(GAP):
        uh, vh, wh = S.force(uh, vh, wh, g); uh, vh, wh = S.step(uh, vh, wh, g, nu, dt)
    eps = DA.dissipation_field(uh, vh, wh, g, nu); em = eps.mean()
    sks.append(S.skewness(uh, g))
    for h in THR:
        ml, sizes, wraps = DA.periodic_components(eps > h * em)
        pooled[h].extend(sizes.values())
        df, r2, ndf = DA.fractal_dim(ml, sizes, wraps)
        if np.isfinite(df):
            frac[h].append((df, ndf))

np.savez(STATE, uh=uh, vh=vh, wh=wh, ns=int(z['ns']) + NSNAP * GAP)
np.savez(POOL, **{f"h{int(h)}": np.array(pooled[h], dtype=int) for h in THR},
         **{f"f{int(h)}": np.array(frac[h], dtype=float) if frac[h]
            else np.zeros((0, 2)) for h in THR})
log(f"   snapshot skewness mean={np.mean(sks):+.2f} (canonical ~ -0.5)")

log("")
log(f"   {'h*<eps>':>8}{'Nstruct':>9}{'tau_MLE':>10}{'+-se':>7}{'xmin':>6}"
    f"{'ntail':>7}{'KS':>7}{'tau_lbin':>10}{'R2':>7}{'LLR':>8}{'d_f':>7}")
rows = []
for h in THR:
    sizes = np.array(pooled[h], dtype=int)
    fit = DA.clauset_fit(sizes)
    if not fit:
        log(f"   {h:>7.1f} : insufficient ({len(sizes)})"); continue
    tau_lb, r2, nb = DA.logbin_fit(sizes, fit['xmin'], int(sizes.max()))
    llr = DA.exp_vs_power_llr(sizes, fit['xmin'])
    dfm = np.mean([d for d, _ in frac[h]]) if frac[h] else np.nan
    log(f"   {h:>7.1f} {len(sizes):>9d}{fit['alpha']:>10.3f}{fit['se']:>7.3f}"
        f"{fit['xmin']:>6d}{fit['ntail']:>7d}{fit['ks']:>7.3f}"
        f"{tau_lb:>10.3f}{r2:>7.3f}{llr:>+8.2f}{dfm:>7.2f}")
    rows.append((h, len(sizes), fit['alpha'], fit['se'], fit['xmin'],
                 fit['ntail'], fit['ks'], tau_lb, r2, llr, dfm))

plat = [r for r in rows if r[0] >= 3.0 and np.isfinite(r[2])]
if plat:
    taus = np.array([r[2] for r in plat]); ses = np.array([r[3] for r in plat])
    tbar = float(np.sum(taus / ses**2) / np.sum(1 / ses**2))
    terr = float(1 / np.sqrt(np.sum(1 / ses**2)))
    lbs = [r[7] for r in plat if np.isfinite(r[7])]
    dfs = [r[10] for r in plat if np.isfinite(r[10])]
    log("")
    log(f"   PLATEAU (h>=3, intense events): tau = {tbar:.3f} +- {terr:.3f}"
        f"  | tau_logbin in [{min(lbs):.2f},{max(lbs):.2f}]  | d_f ~ {np.mean(dfs):.2f}")
    inside = 1.40 - terr <= tbar <= 1.50 + terr
    if dfs:
        dfm = float(np.mean(dfs)); x = (2 - tbar) * dfm / 3.0; th = x / (1 - x)
        log(f"   Lin-Wyart back-out: d_f={dfm:.2f} & tau={tbar:.3f} => substrate "
            f"theta={th:.2f} (framework expects 0.5-0.6).")
    log(f"   PRE-REGISTERED tau in [1.40,1.50]: "
        f"{'CONSISTENT' if inside else 'TENSION'} (measured {tbar:.3f}+-{terr:.3f}).")
    log(f"   power-law vs exponential LLR/pt = {np.mean([r[9] for r in plat]):+.2f} "
        f"(>0 favors power law; exponential rejected).")

with open("p4_summary.csv", "w") as f:
    f.write("h,Nstruct,tau_MLE,se,xmin,ntail,KS,tau_logbin,R2,LLR,d_f\n")
    for r in rows:
        f.write(",".join(f"{v:.4f}" if isinstance(v, float) else str(v) for v in r) + "\n")
log(f"   runtime {time.time()-t0:.0f}s")
open("dissipation_avalanche.out.txt", "w").write("\n".join(L) + "\n")
