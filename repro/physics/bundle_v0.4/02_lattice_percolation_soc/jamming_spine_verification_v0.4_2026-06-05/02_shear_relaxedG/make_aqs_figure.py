"""AQS figure: (L) representative stress-strain curve sigma(gamma) (elastic + plastic sawtooth);
(R) yield stress sigma_y(z) -> 0 toward z_iso=6 (gamma_dot->0 limit; dynamic analog of G->0)."""
import csv, glob, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows=list(csv.DictReader(open("/home/claude/vp_shear/results/aqs_sigmay.csv")))
z=np.array([float(r["z"]) for r in rows]); sy=np.array([float(r["sigma_y"]) for r in rows])
o=np.argsort(z); z,sy=z[o],sy[o]
for r in sorted(rows,key=lambda r:float(r["z"])):
    print(f"z={float(r['z']):.3f}  sigma_y={float(r['sigma_y']):.4f}  G_relaxed(static)={float(r['G_relaxed_static']):.3f}")
a,b=np.polyfit(z,sy,1); z0=-b/a
print(f"\nsigma_y linear fit -> 0 at z0={z0:.3f}   [z_iso=6]")

fig,(axL,axR)=plt.subplots(1,2,figsize=(12.4,5.0),dpi=140)
# representative curve: pick the phi=0.700 config
f=sorted(glob.glob("/home/claude/vp_shear/results/aqs_curves/*phi0.700*.npz"))
if f:
    d=np.load(f[0]); g=d["g"]; s=np.abs(d["s"]); zc=float(d["z"])
    axL.plot(g,s,"-",color="#1f4e79",lw=1.3,marker="o",ms=3)
    pl=(g>=0.09)&(g<=0.20)
    syc=abs(np.mean(d["s"][pl]))
    axL.axhline(syc,color="#c0392b",ls="--",lw=1.4,label=f"$\\sigma_y$={syc:.4f} (plateau mean)")
    axL.axvspan(0.09,0.20,color="#c0392b",alpha=0.08,label="plateau window")
    axL.set_title(f"AQS stress-strain (z={zc:.2f}): elastic rise + plastic sawtooth",fontsize=10.5)
axL.set_xlabel("strain  $\\gamma$",fontsize=12); axL.set_ylabel("$|\\sigma_{xy}|$",fontsize=12)
axL.legend(fontsize=9); axL.grid(alpha=0.2)

axR.scatter(z,sy,s=70,c="#7b1fa2",zorder=4,label="$\\sigma_y$ (AQS, $\\dot\\gamma\\to0$)")
zl=np.linspace(6.0,z.max()+0.2,30); axR.plot(zl,a*zl+b,"-",c="#c0392b",lw=1.8,
    label=f"linear: $\\sigma_y\\to0$ at z={z0:.2f}")
axR.axvline(6.0,ls="--",c="#222",lw=1.3); axR.axhline(0,ls=":",c="#999",lw=1.0)
axR.annotate("$z_{\\rm iso}=6$",xy=(6.03,sy.max()*0.85),fontsize=11,color="#222")
axR.set_xlabel("contact number  $z$",fontsize=12); axR.set_ylabel("yield stress  $\\sigma_y$",fontsize=12)
axR.set_title("Yield stress $\\to 0$ toward the margin\n(AQS $\\dot\\gamma{\\to}0$ limit; N=128, single seed)",fontsize=10.5)
axR.set_xlim(5.9,z.max()+0.3); axR.set_ylim(0,sy.max()*1.25); axR.grid(alpha=0.2)
axR.legend(fontsize=9.5,loc="upper left")
fig.tight_layout(); fig.savefig("/home/claude/vp_shear/results/aqs_yield.png",dpi=140)
fig.savefig("/home/claude/vp_shear/results/aqs_yield.pdf"); print("saved aqs_yield.png/.pdf")
