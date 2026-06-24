import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
mu0=4*np.pi*1e-7; yr=3.15e7
W_in=3.0e26
Q_earth=4.7e13
rho=3e3; cp=1e3; v_imp=2e4
R_core=3.48e6; V_core=(4/3)*np.pi*R_core**3

# best-case magnitudes per candidate
E_he1_th = 0.05*(rho*cp*1e14*1e5*500)      # thermal, eta=5%, Pacific-scale 100km dT500
E_he1_pv = 0.01*1e20*1e8                    # PV work best
E_he2_1k = Q_earth*1e3*yr                   # whole-Earth heat, 1 kyr
E_he2_10k= Q_earth*1e4*yr                   # 10 kyr
E_he2_imp= 0.5*rho*(np.pi/6)*((98e3)**3)*v_imp**2   # 98 km impactor (excluded by signature)
E_he3    = (5e-3)**2/(2*mu0)*V_core         # strong core toroidal field

labels=["H-E1\nthermal\n(eta=5%)","H-E1\nPV-work","H-E2\nheat 1kyr","H-E2\nheat 10kyr",
        "H-E2\nimpact 98km*","H-E3\ncore field"]
vals  =[E_he1_th,E_he1_pv,E_he2_1k,E_he2_10k,E_he2_imp,E_he3]
# admissible (energetically + signature): only H-E1 thermal
adm   =[True,False,False,False,False,False]
colors=["#3a7d44" if a else "#b23a3a" for a in adm]

fig,ax=plt.subplots(figsize=(10,4.6))
x=np.arange(len(vals))
ax.bar(x,vals,color=colors,edgecolor="k",width=0.62)
ax.axhline(W_in,ls="--",color="k",lw=1.6)
ax.text(len(vals)-0.4,W_in*1.25,f"required W_in ~ {W_in:.0e} J",ha="right",fontsize=9)
ax.set_yscale("log"); ax.set_ylim(1e19,1e29)
ax.set_xticks(x); ax.set_xticklabels(labels,fontsize=8)
ax.set_ylabel("available / required energy [J]")
ax.set_title("C-17 AR-1 source audit: only H-E1 (release of stored heat) clears the bar",fontsize=11)
# annotate the gaps
for xi,(v,a) in enumerate(zip(vals,adm)):
    g=W_in/v
    tag = "ADMISSIBLE" if a else (f"{g:.0f}x short" if g>=2 else "marginal")
    ax.text(xi,v*1.3 if v<W_in else v*1.3,tag,ha="center",fontsize=7.5,
            color=("#3a7d44" if a else "#b23a3a"))
ax.text(0.0,1.3e19,"* impact magnitude is reachable but EXCLUDED by the absence of a global melt/ejecta signature",
        fontsize=7,color="#555")
fig.tight_layout()
fig.savefig("figures/fig_c17_energy_source.png",dpi=130)
print("saved figures/fig_c17_energy_source.png")
