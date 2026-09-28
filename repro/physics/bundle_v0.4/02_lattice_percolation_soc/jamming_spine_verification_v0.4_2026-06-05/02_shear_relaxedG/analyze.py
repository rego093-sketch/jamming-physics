"""Analyze relaxedG.csv: acceptance audit, per-phi stats, pooled G=a(z-z0) fit + bootstrap z0 CI."""
import sys, csv, numpy as np

CSV = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/vp_shear/results/relaxedG.csv"
NFILT = int(sys.argv[2]) if len(sys.argv) > 2 else None

rows = []
with open(CSV) as f:
    for r in csv.DictReader(f):
        rows.append(r)

def fnum(x):
    try: return float(x)
    except: return np.nan

recs = []
for r in rows:
    N = int(r["N"])
    if NFILT and N != NFILT: continue
    jam = int(r["jammed"]); psd = (r["psd"] == "1")
    mF = fnum(r["mF"]); z = fnum(r["z"])
    GB = fnum(r["G_Born"]); GR = fnum(r["G_relaxed"])
    recs.append(dict(N=N, phi=float(r["phi"]), seed=int(r["seed"]), jam=jam, psd=psd,
                     mF=mF, z=z, GB=GB, GR=GR))

njam = sum(1 for x in recs if x["jam"])
print(f"file={CSV}  N-filter={NFILT}")
print(f"total rows={len(recs)}  jammed={njam}  unjammed={len(recs)-njam}")

# ---- audit: are gross-negative G correlated with non-PSD? ----
jrecs = [x for x in recs if x["jam"]]
neg = [x for x in jrecs if np.isfinite(x["GR"]) and x["GR"] < -0.02*abs(x["GB"])]
print(f"\nconfigs with G_relaxed < -2% of G_Born: {len(neg)}")
for x in neg:
    print(f"   phi={x['phi']:.3f} sd={x['seed']} z={x['z']:.3f} GB={x['GB']:.3f} GR={x['GR']:.4f} psd={x['psd']} mF={x['mF']:.1e}")

# ---- acceptance: PSD + converged ----
def accepted(x):
    return x["jam"] and x["psd"] and np.isfinite(x["mF"]) and x["mF"] < 1e-7 and np.isfinite(x["GR"])
acc = [x for x in jrecs if accepted(x)]
print(f"\nACCEPTED (jammed & PSD & mF<1e-7): {len(acc)} / {njam} jammed")
GRm = np.array([x["GR"] for x in acc])
print(f"  among accepted: min G_relaxed = {GRm.min():.4f}, # negative = {(GRm<0).sum()}  (PSD => should be ~0 within roundoff)")
print(f"  G_Born range among accepted: [{min(x['GB'] for x in acc):.3f}, {max(x['GB'] for x in acc):.3f}]  (check (iv): finite O(1))")

# ---- per-phi stats ----
print(f"\n{'phi':>6} {'n':>3} {'z_mean':>7} {'GB_mean':>8} {'GR_mean':>8} {'GR_sem':>7}")
phis = sorted(set(x["phi"] for x in acc))
zmeans=[]; grmeans=[]
for phi in phis:
    g = [x for x in acc if x["phi"] == phi]
    z = np.array([x["z"] for x in g]); gr = np.array([x["GR"] for x in g]); gb = np.array([x["GB"] for x in g])
    sem = gr.std(ddof=1)/np.sqrt(len(gr)) if len(gr) > 1 else float('nan')
    zmeans.append(z.mean()); grmeans.append(gr.mean())
    print(f"{phi:6.3f} {len(g):3d} {z.mean():7.3f} {gb.mean():8.3f} {gr.mean():8.4f} {sem:7.4f}")

# ---- monotonicity check on per-phi means ----
gm = np.array(grmeans)
print(f"\n(ii) monotonic G_relaxed(z) on phi-means: {'YES' if np.all(np.diff(gm) > -0.02) else 'NO (dips: '+str(np.where(np.diff(gm)<=-0.02)[0])+')'}")

# ---- pooled linear fit G = a*(z - z0) using ALL accepted points ----
z = np.array([x["z"] for x in acc]); g = np.array([x["GR"] for x in acc])
A = np.vstack([z, np.ones_like(z)]).T
(a, b), *_ = np.linalg.lstsq(A, g, rcond=None)
z0 = -b/a; pred = A @ np.array([a, b]); R2 = 1 - np.sum((g-pred)**2)/np.sum((g-g.mean())**2)
print(f"\n(iii) POOLED fit  G = {a:.5f}*(z - {z0:.3f})   R^2={R2:.4f}   [isostatic prediction z_iso=2d=6.000]")

# bootstrap CI on z0
rng = np.random.default_rng(0); z0s = []
for _ in range(4000):
    idx = rng.integers(0, len(z), len(z))
    aa, bb = np.linalg.lstsq(np.vstack([z[idx], np.ones(len(idx))]).T, g[idx], rcond=None)[0]
    if abs(aa) > 1e-6: z0s.append(-bb/aa)
z0s = np.array(z0s); lo, hi = np.percentile(z0s, [2.5, 97.5])
print(f"      bootstrap z0 = {np.median(z0s):.3f}  95% CI [{lo:.3f}, {hi:.3f}]   (contains 6.0? {'YES' if lo<=6.0<=hi else 'NO'})")
