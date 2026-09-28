"""Finalize N=512: robustness (with/without negatives), weighted-means fit, and the figure."""
import csv, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "/home/claude/vp_shear/results/relaxedG.csv"
NF = 512
def fnum(x):
    try: return float(x)
    except: return np.nan

recs = []
with open(CSV) as f:
    for r in csv.DictReader(f):
        if int(r["N"]) != NF: continue
        if int(r["jammed"]) != 1: continue
        psd = (r["psd"] == "1"); mF = fnum(r["mF"])
        GR = fnum(r["G_relaxed"]); GB = fnum(r["G_Born"]); z = fnum(r["z"])
        if not (psd and np.isfinite(mF) and mF < 1e-7 and np.isfinite(GR)): continue
        recs.append((float(r["phi"]), z, GB, GR))
recs = np.array(recs)
phi, z, GB, GR = recs[:,0], recs[:,1], recs[:,2], recs[:,3]

def linfit(zz, gg):
    A = np.vstack([zz, np.ones_like(zz)]).T
    (a,b),*_ = np.linalg.lstsq(A, gg, rcond=None)
    pred = A@np.array([a,b]); R2 = 1-np.sum((gg-pred)**2)/np.sum((gg-gg.mean())**2)
    return a, b, -b/a, R2

def boot_z0(zz, gg, nb=5000):
    rng = np.random.default_rng(1); out=[]
    for _ in range(nb):
        k = rng.integers(0,len(zz),len(zz))
        a,b,*_ = linfit(zz[k], gg[k])
        if abs(a)>1e-6: out.append(-b/a)
    out=np.array(out); return np.median(out), np.percentile(out,[2.5,97.5])

# full pooled
a,b,z0,R2 = linfit(z, GR); zm,(lo,hi)=boot_z0(z,GR)
print(f"[ALL accepted, n={len(z)}]     G={a:.4f}(z-{z0:.3f})  R2={R2:.3f}  z0_boot={zm:.3f} CI[{lo:.3f},{hi:.3f}]")

# robustness: drop G < -2% of GB
keep = GR > -0.02*np.abs(GB)
a2,b2,z02,R22 = linfit(z[keep], GR[keep]); zm2,(lo2,hi2)=boot_z0(z[keep],GR[keep])
print(f"[drop G<-2%GB,  n={keep.sum()}]  G={a2:.4f}(z-{z02:.3f})  R2={R22:.3f}  z0_boot={zm2:.3f} CI[{lo2:.3f},{hi2:.3f}]")

# weighted fit on per-phi means
phis = sorted(set(phi)); zb=[]; gb_m=[]; gr_m=[]; gr_se=[]
for p in phis:
    m = phi==p
    zb.append(z[m].mean()); gb_m.append(GB[m].mean())
    gr_m.append(GR[m].mean()); gr_se.append(GR[m].std(ddof=1)/np.sqrt(m.sum()))
zb=np.array(zb); gr_m=np.array(gr_m); gr_se=np.array(gr_se); gb_m=np.array(gb_m)
w = 1.0/gr_se**2
A = np.vstack([zb, np.ones_like(zb)]).T
WA = A*w[:,None]; coef = np.linalg.solve(A.T@WA, (WA*gr_m[:,None]).sum(0).reshape(-1) if False else A.T@(w*gr_m))
aw, bw = coef; z0w = -bw/aw
predw = A@coef; R2w = 1-np.sum(w*(gr_m-predw)**2)/np.sum(w*(gr_m-np.average(gr_m,weights=w))**2)
print(f"[weighted phi-means] G={aw:.4f}(z-{z0w:.3f})  wR2={R2w:.3f}")

# ---------------- figure ----------------
fig, ax = plt.subplots(figsize=(7.2,5.2), dpi=140)
ax.scatter(z, GR, s=14, c="#9bbcd6", alpha=0.55, edgecolors="none", label="per-config $G_{\\rm relaxed}$ (N=512)", zorder=2)
ax.errorbar(zb, gr_m, yerr=gr_se, fmt="o", ms=7, c="#1f4e79", capsize=3, lw=1.4,
            label="$\\phi$-ensemble mean $\\pm$ SEM", zorder=4)
zline = np.linspace(5.8, 9.4, 50)
ax.plot(zline, a*(zline-z0), "-", c="#c0392b", lw=2.0,
        label=f"fit $G={a:.3f}(z-z_0)$,  $z_0={zm:.2f}$", zorder=3)
ax.fill_between(zline, a2*(zline-lo2*0+ a2*0), a2*(zline-z02), alpha=0)  # noop keep colors
ax.axvline(6.0, ls="--", c="#444", lw=1.3, zorder=1)
ax.axhline(0.0, ls=":", c="#888", lw=1.0, zorder=1)
ax.annotate("$z_{\\rm iso}=2d=6$", xy=(6.0,0.55), xytext=(6.05,0.55), color="#444", fontsize=11)
ax.axvspan(lo, hi, color="#c0392b", alpha=0.10, zorder=0, label=f"$z_0$ 95% CI [{lo:.2f}, {hi:.2f}]")
# Born modulus on twin axis
ax.scatter(z, GB, s=10, c="#8fbf8f", alpha=0.5, marker="s", edgecolors="none",
           label="$G_{\\rm Born}$ (affine, stays finite)", zorder=2)
ax.set_xlabel("contact number  $z$  (rigid backbone)", fontsize=12)
ax.set_ylabel("shear modulus", fontsize=12)
ax.set_title("Relaxed shear modulus vanishes at the isostatic point\n$G_{\\rm relaxed}\\to0$ as $z\\to z_{\\rm iso}=6$, while $G_{\\rm Born}$ stays finite", fontsize=11.5)
ax.set_xlim(5.85, 9.45); ax.set_ylim(-0.12, 1.42)
ax.legend(fontsize=8.6, loc="upper left", framealpha=0.9)
ax.grid(alpha=0.18)
fig.tight_layout()
fig.savefig("/home/claude/vp_shear/results/relaxedG_vs_z.png", dpi=140)
fig.savefig("/home/claude/vp_shear/results/relaxedG_vs_z.pdf")
print("figure saved.")
