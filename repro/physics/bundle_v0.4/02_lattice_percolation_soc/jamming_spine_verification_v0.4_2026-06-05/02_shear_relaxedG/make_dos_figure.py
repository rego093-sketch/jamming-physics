"""Density of states D(omega) and characteristic frequency omega*(z) from collected spectra.
Benchmark (Silbert-Liu-Nagel 2005; Wyart 2005): plateau edge omega* ~ Delta z -> 0 at z_iso=2d=6,
so relaxation time tau ~ 1/omega* diverges -> at the margin the system cannot follow real-time
driving and flows. Pairs with c_T = sqrt(G/rho) -> 0 (shear wave dies)."""
import os, glob, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

SPEC = "/home/claude/vp_shear/results/spectra"; N = 512
files = sorted(glob.glob(f"{SPEC}/N{N}_phi*_sd*.npz"))
byphi = {}
for f in files:
    d = np.load(f)
    if int(d["jammed"]) != 1: continue
    phi = float(os.path.basename(f).split("phi")[1].split("_sd")[0])
    byphi.setdefault(phi, {"omega": [], "z": [], "wmin": []})
    byphi[phi]["omega"].append(d["omega"]); byphi[phi]["z"].append(float(d["z"]))
    byphi[phi]["wmin"].append(float(d["w2min"]))

def omega_star(omega, nbins=70):
    """Low-frequency plateau edge: omega where D(omega) first reaches half the plateau height
    scanning from intermediate freq down to 0. Plateau height = median D over the 35-75% omega band."""
    om = np.sort(omega); om = om[om > 0]
    hi = np.percentile(om, 92)
    bins = np.linspace(0, hi, nbins); ctr = 0.5*(bins[1:]+bins[:-1])
    Dh, _ = np.histogram(om, bins=bins, density=True)
    lo_b, hi_b = np.percentile(om, 35), np.percentile(om, 75)
    band = (ctr >= lo_b) & (ctr <= hi_b)
    Dp = np.median(Dh[band]) if band.any() else Dh.max()
    half = 0.5*Dp
    # scan downward from the band start
    start = np.searchsorted(ctr, lo_b)
    ws = ctr[0]
    for k in range(start, -1, -1):
        if Dh[k] < half:
            # linear interp between k and k+1
            if k+1 < len(ctr) and Dh[k+1] >= half and (Dh[k+1]-Dh[k]) != 0:
                ws = ctr[k] + (half-Dh[k])/(Dh[k+1]-Dh[k])*(ctr[k+1]-ctr[k])
            else:
                ws = ctr[k]
            break
    return ws, ctr, Dh, Dp

phis = sorted(byphi)
rows = []
for phi in phis:
    om = np.concatenate(byphi[phi]["omega"]).astype(float)
    z = np.mean(byphi[phi]["z"]); wmin_med = np.median(byphi[phi]["wmin"])
    ws, ctr, Dh, Dp = omega_star(om)
    om2pct = np.percentile(om[om>0], 2.0)
    rows.append((phi, z, ws, np.sqrt(wmin_med), om2pct, ctr, Dh))
    print(f"phi={phi:.3f} z={z:6.3f}  omega*={ws:.4f}  omega_min(med)={np.sqrt(wmin_med):.4f}  omega_2%={om2pct:.4f}")

# ---- fit omega*(z) ----
zarr = np.array([r[1] for r in rows]); wsarr = np.array([r[2] for r in rows])
A = np.vstack([zarr, np.ones_like(zarr)]).T
(a,b),*_ = np.linalg.lstsq(A, wsarr, rcond=None); z0 = -b/a
pred = A@np.array([a,b]); R2 = 1-np.sum((wsarr-pred)**2)/np.sum((wsarr-wsarr.mean())**2)
print(f"\nomega* = {a:.4f}*(z - {z0:.3f})   R2={R2:.3f}   [z_iso=6]")
# through-origin fit in Delta z = z-6
dz = zarr-6.0; slope = float(np.dot(dz, wsarr)/np.dot(dz,dz))
ss = 1-np.sum((wsarr-slope*dz)**2)/np.sum((wsarr-wsarr.mean())**2)
print(f"omega* = {slope:.4f}*(z-6)  [forced through z_iso=6]  R2={ss:.3f}")

# ---- figure ----
fig,(axL,axR)=plt.subplots(1,2,figsize=(12.6,5.2),dpi=140,gridspec_kw={"width_ratios":[1.25,1]})
cmap = plt.cm.viridis(np.linspace(0.05,0.9,len(rows)))
for (phi,z,ws,wmm,w2,ctr,Dh),col in zip(rows,cmap):
    axL.plot(ctr, Dh, lw=1.7, color=col, label=f"z={z:.2f}")
    axL.axvline(ws, color=col, ls=":", lw=1.0, alpha=0.8)
axL.set_xlabel("frequency  $\\omega=\\sqrt{\\lambda_{\\rm Hessian}}$", fontsize=12)
axL.set_ylabel("density of states  $D(\\omega)$", fontsize=12)
axL.set_title("DOS plateau edge $\\omega^*$ slides to 0 as $z\\to z_{\\rm iso}=6$\n(dotted = $\\omega^*$; plateau extends to zero freq at the margin)", fontsize=10.8)
axL.set_xlim(0, np.percentile(np.concatenate([r[5] for r in rows]),100)*0.55)
axL.legend(fontsize=8.5, title="contact $z$", ncol=2); axL.grid(alpha=0.18)

axR.scatter(zarr, wsarr, s=55, c="#1f4e79", zorder=4, label="$\\omega^*$ (DOS edge)")
zl=np.linspace(6.0,9.4,40)
axR.plot(zl, slope*(zl-6.0), "-", c="#c0392b", lw=2.0, zorder=3,
         label=rf"$\omega^*={slope:.3f}(z-6)$  (R²={ss:.2f})")
axR.axvline(6.0, ls="--", c="#222", lw=1.3)
axR.axhline(0, ls=":", c="#999", lw=1.0)
axR.annotate("$z_{\\rm iso}=6$", xy=(6.03, 0.9*wsarr.max()), color="#222", fontsize=11)
axR.set_xlabel("contact number  $z$", fontsize=12)
axR.set_ylabel("characteristic frequency  $\\omega^*$", fontsize=12)
axR.set_title("$\\omega^*\\propto(z-6)\\to 0$  →  $\\tau\\sim 1/\\omega^*\\to\\infty$\n(real-time drive cannot be followed at the margin)", fontsize=10.8)
axR.set_xlim(5.9, 9.45); axR.set_ylim(0, wsarr.max()*1.15); axR.grid(alpha=0.2)
axR.legend(fontsize=9.5, loc="upper left")
fig.tight_layout()
fig.savefig("/home/claude/vp_shear/results/dos_omega_star.png", dpi=140)
fig.savefig("/home/claude/vp_shear/results/dos_omega_star.pdf")
print("saved dos_omega_star.png/.pdf")
