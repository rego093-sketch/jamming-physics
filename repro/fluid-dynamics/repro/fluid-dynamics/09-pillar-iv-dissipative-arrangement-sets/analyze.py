# -*- coding: utf-8 -*-
"""analyze.py N statefile poolfile [nsnap] -- general P4 analyzer at resolution N.
Loads a developed state, collects decorrelated snapshots (accumulating into the
pool across calls), and fits the thresholded dissipation-structure size
distribution P(s)~s^{-tau}. Threshold scan -> plateau; logbin + LLR + d_f."""
import numpy as np, time, os, sys
import ns3d as S
import dissipation_avalanche as DA

N = int(sys.argv[1]); STATE = sys.argv[2]; POOL = sys.argv[3]
NSNAP = int(sys.argv[4]) if len(sys.argv) > 4 else 6
nu, dt, GAP = 0.008, 0.004, 14
THR = [2.0, 3.0, 4.0, 6.0]

t0 = time.time(); L = []
def log(m): L.append(m); print(m, flush=True)

z = np.load(STATE); uh, vh, wh = z['uh'], z['vh'], z['wh']; g = S.grid(N)
log(f"== P4 analysis: N={N} nu={nu}, +{NSNAP} snapshots gap={GAP} ==")

pooled = {h: [] for h in THR}; frac = {h: [] for h in THR}
if os.path.exists(POOL):
    pz = np.load(POOL, allow_pickle=True)
    pooled = {h: list(pz[f"h{int(h)}"]) for h in THR}
    frac = {h: list(map(tuple, pz[f"f{int(h)}"])) for h in THR}
    log("   resumed pool: " + ", ".join(f"h{int(h)}={len(pooled[h])}" for h in THR))

sks = []
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
log(f"   snapshot skewness mean={np.mean(sks):+.2f}")
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
    log(f"   PLATEAU (h>=3): tau = {tbar:.3f} +- {terr:.3f}  | tau_logbin in "
        f"[{min(lbs):.2f},{max(lbs):.2f}]  | d_f ~ {np.mean(dfs):.2f}")
    log(f"   power-law vs exponential LLR/pt = {np.mean([r[9] for r in plat]):+.2f}")
log(f"   runtime {time.time()-t0:.0f}s")
open(f"avalanche_N{N}.out.txt", "w").write("\n".join(L) + "\n")
