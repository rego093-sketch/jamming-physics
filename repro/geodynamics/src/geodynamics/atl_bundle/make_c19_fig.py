import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

mu_byerlee=0.6; mu_exp=0.1; mu_claim=2.2e-3
lam_req=1-mu_claim/mu_byerlee

fig,ax=plt.subplots(1,2,figsize=(12,4.4))

# (a) friction weakening ladder (log)
labels=["Byerlee\n(static)","dynamic\n(experiment)","paper mu_eff\n(liquefaction)"]
vals=[mu_byerlee,mu_exp,mu_claim]
cols=["#555555","#3a7d44","#b23a3a"]
x=np.arange(3)
ax[0].bar(x,vals,color=cols,edgecolor="k",width=0.6)
ax[0].set_yscale("log"); ax[0].set_ylim(1e-3,1)
ax[0].set_xticks(x); ax[0].set_xticklabels(labels,fontsize=9)
ax[0].set_ylabel("friction coefficient")
ax[0].axhspan(0.05,0.2,alpha=0.12,color="#3a7d44")
ax[0].text(1.0,0.22,"experimentally confirmed\nrange (~0.05-0.2)",ha="center",fontsize=7.5,color="#2c5f2c")
ax[0].text(2.0,mu_claim*1.4,f"requires pore P\nwithin {100*(1-lam_req):.2f}% of\nlithostatic",ha="center",fontsize=7.5,color="#b23a3a")
ax[0].annotate("",xy=(1,mu_exp),xytext=(0,mu_byerlee),arrowprops=dict(arrowstyle="->",color="#3a7d44"))
ax[0].text(0.5,0.32,"~6x (lab)",fontsize=7.5,color="#3a7d44")
ax[0].set_title("(a) dynamic weakening: confirmed direction, extreme magnitude",fontsize=10)

# (b) lab vs Earth dimensionless regime
groups=["inertial\nnumber I","sigma_n/\nsigma_crush","grain count\nlog10 N"]
lab_v=[2.6e-2, 0.003, np.log10(3e15)]   # lab N illustrative
earth_v=[1.4e-4, 0.50, np.log10(3e21)]
xx=np.arange(3); w=0.35
ax[1].bar(xx-w/2,lab_v,w,label="lab",color="#9ecae1",edgecolor="k")
ax[1].bar(xx+w/2,earth_v,w,label="Earth",color="#fc9272",edgecolor="k")
ax[1].set_xticks(xx); ax[1].set_xticklabels(groups,fontsize=8.5)
ax[1].axhline(1.0,ls="--",color="gray",lw=1); ax[1].text(2.4,1.05,"=1",fontsize=7.5,color="gray")
ax[1].set_yscale("log"); ax[1].legend(fontsize=8)
ax[1].set_title("(b) what transfers: I<<1 both (yes); crushing & N (regime differs)",fontsize=10)

fig.suptitle("C-19 master-scale: dense-granular regime + continuum limit transfer; exact phi_J & mu_eff are HOLD",fontsize=11)
fig.tight_layout(rect=[0,0,1,0.95])
fig.savefig("figures/fig_c19_master_scale.png",dpi=130)
print("saved figures/fig_c19_master_scale.png  (lambda_req=%.4f)"%lam_req)
