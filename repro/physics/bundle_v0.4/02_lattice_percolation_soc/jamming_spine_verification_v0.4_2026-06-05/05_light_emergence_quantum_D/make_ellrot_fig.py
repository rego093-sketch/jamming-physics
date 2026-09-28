# make_ellrot_fig.py -- 빛 창발 그림: ell_rot = 2*pi*lambda/A 분포 vs 목표 4.85pm(=2 lambda_Ce).
# A 는 격자 침투 증폭(무차원). 실행: python3 make_ellrot_fig.py
import numpy as np, pandas as pd, math
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
lam=632.991e-9
B="bundle/AQD_DOI_bundle_unified_v0.3.0_logic_DOI17932567/02_lattice_percolation_soc/lattice_percolation_soc_bundle/results/soc_run3_avalanches.csv"
A1=pd.read_csv(B).replace([np.inf,-np.inf],np.nan).dropna(subset=["A_post"])["A_post"].to_numpy(float)
A2=pd.read_csv("soc_indep/results/soc_run3_avalanches.csv").replace([np.inf,-np.inf],np.nan).dropna(subset=["A_post"])["A_post"].to_numpy(float)
r1=2*math.pi*lam/A1*1e12; r2=2*math.pi*lam/A2*1e12
fig,ax=plt.subplots(figsize=(7.6,4.4))
bins=np.linspace(0,16,33)
ax.hist(r1,bins=bins,alpha=.6,color="#1f77b4",label=f"bundle N=200 ({len(r1)} av), med {np.median(r1):.2f} pm")
ax.hist(r2,bins=bins,alpha=.5,color="#ff7f0e",label=f"indep reproduction ({len(r2)} av), med {np.median(r2):.2f} pm")
ax.axvline(4.85,color="crimson",lw=2,label="target 4.85 pm")
ax.axvline(np.median(r1),color="#1f77b4",ls="--",lw=1)
ax.set_xlabel("$\\ell_{\\rm rot}=2\\pi\\lambda/A$  (pm)  —  $D$ from the lattice via the wavelength")
ax.set_ylabel("avalanche count")
ax.set_title("Light emergence on the jamming lattice:\noptical 633 nm $\\to$ A micro-steps $\\to$ proton diameter $D=2\\pi\\lambda/A$",fontsize=10.5)
ax.legend(fontsize=8); ax.set_xlim(0,16)
plt.tight_layout()
for e in ("png","pdf"): plt.savefig(f"ellrot_485pm.{e}",dpi=150,bbox_inches="tight")
print("saved ellrot_485pm")
