"""Flow curves sigma(gdot) (power-law fit, sigma_y unresolved at these rates) + viscosity
eta=sigma/gdot divergence as gdot->0 (Olsson-Teitel signature; the rheological face of tau->inf)."""
import csv, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open("/home/claude/vp_shear/results/flowcurve.csv")))
data = {}
for r in rows:
    phi=float(r["phi"]); gd=float(r["gdot"]); s=abs(float(r["sigma_ss"])); z=float(r["z"])
    data.setdefault(phi,{"g":{},"z":[]}); data[phi]["g"].setdefault(gd,[]).append(s); data[phi]["z"].append(z)
phis=sorted(data)
fig,(axL,axR)=plt.subplots(1,2,figsize=(12.4,5.0),dpi=140)
cmap=plt.cm.viridis(np.linspace(0.1,0.78,len(phis)))
print(f"{'phi':>6} {'z':>6} {'n (sigma~gdot^n)':>16}")
for phi,c in zip(phis,cmap):
    gd=np.array(sorted(data[phi]["g"])); sig=np.array([np.mean(data[phi]["g"][g]) for g in gd])
    z=np.mean(data[phi]["z"])
    # power-law fit sigma = A gdot^n
    b,loga = np.polyfit(np.log(gd), np.log(sig), 1); n=b; A=np.exp(loga)
    print(f"{phi:6.3f} {z:6.3f} {n:16.3f}")
    axL.plot(gd,sig,"o",ms=7,color=c,label=f"z={z:.2f}")
    gl=np.logspace(np.log10(gd.min()),np.log10(gd.max()),40); axL.plot(gl,A*gl**n,"-",color=c,lw=1.5,alpha=0.8)
    axR.plot(gd,sig/gd,"o-",ms=7,color=c,lw=1.5,label=f"z={z:.2f}")
axL.set_xscale("log"); axL.set_yscale("log")
axL.set_xlabel("shear rate  $\\dot\\gamma$",fontsize=12); axL.set_ylabel("steady stress  $|\\sigma_{xy}|$",fontsize=12)
axL.set_title("Flow curves $\\sigma\\sim\\dot\\gamma^{\\,n}$ (shear-thinning; no yield\nplateau down to $\\dot\\gamma{=}0.003$ even deep $\\Rightarrow\\dot\\gamma^*{\\to}0$)",fontsize=10.3)
axL.legend(fontsize=9,title="contact $z$"); axL.grid(alpha=0.2,which="both")
axR.set_xscale("log"); axR.set_yscale("log")
axR.set_xlabel("shear rate  $\\dot\\gamma$",fontsize=12); axR.set_ylabel("viscosity  $\\eta=\\sigma/\\dot\\gamma$",fontsize=12)
axR.set_title("Viscosity diverges as $\\dot\\gamma\\to0$\n(rheological face of $\\tau\\sim1/\\omega^*\\to\\infty$)",fontsize=10.5)
axR.legend(fontsize=9,title="contact $z$"); axR.grid(alpha=0.2,which="both")
fig.tight_layout()
fig.savefig("/home/claude/vp_shear/results/flow_curves.png",dpi=140)
fig.savefig("/home/claude/vp_shear/results/flow_curves.pdf")
print("saved flow_curves.png/.pdf")
