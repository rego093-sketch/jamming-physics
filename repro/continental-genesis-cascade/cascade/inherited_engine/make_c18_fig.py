import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng=np.random.default_rng(20260605)

rows=[("P19 sea level","sea_level",4.05,0.45),("P16 d18O","isotope",4.55,0.50),
      ("P16 AMOC","circulation",3.75,0.55),("P24 endorheic","hydrology",4.80,0.55),
      ("P20 misfit R","hydrology",3.95,0.60),("P20 delta","sediment",4.45,0.50)]
mod=[r[0] for r in rows]; t=np.array([r[2] for r in rows]); sig=np.array([r[3] for r in rows])
w=1/sig**2; tb=np.sum(w*t)/np.sum(w)
Kobs=np.sqrt(np.sum(w*(t-tb)**2)/np.sum(w))/np.median(sig)

RLO,RHI,WIN=0.0,11.7,0.5; M=200000
sims=rng.uniform(RLO,RHI,size=(M,len(t)))
tbm=(sims*w).sum(1)/w.sum(); Ksim=np.sqrt(((w*(sims-tbm[:,None])**2).sum(1))/w.sum())/np.median(sig)
p_raw=(Ksim<=Kobs).mean(); N_LEE=(RHI-RLO)/WIN; p_LEE=1-(1-p_raw)**N_LEE

fig,ax=plt.subplots(1,2,figsize=(12,4.4))
y=np.arange(len(rows))[::-1]
ax[0].errorbar(t,y,xerr=sig,fmt="o",color="#2c5f8a",ecolor="#2c5f8a",capsize=3)
ax[0].axvline(tb,color="#b23a3a",ls="--",label=f"weighted mean {tb:.2f} ka")
ax[0].set_yticks(y); ax[0].set_yticklabels(mod,fontsize=8)
ax[0].set_xlabel("event-time estimate [ka BP]"); ax[0].legend(fontsize=8)
ax[0].set_title(f"(a) proxy event times  (K_joint={Kobs:.2f})",fontsize=10)
ax[0].set_xlim(2.5,6.0)

ax[1].hist(Ksim,bins=80,color="#cdd7e2",edgecolor="none",density=True)
ax[1].axvline(Kobs,color="#b23a3a",lw=2,label=f"K_obs={Kobs:.2f}")
ax[1].set_xlabel("K_joint under RANGE NULL  (t_i ~ U[0,11.7] ka)")
ax[1].set_ylabel("density"); ax[1].legend(fontsize=8)
ax[1].set_title("(b) correct null: 'tighter than chance?'",fontsize=10)
ax[1].text(0.97,0.78,f"p_raw = {p_raw:.1e}\nlook-elsewhere x{int(N_LEE)}\n"
           f"p_LEE = {p_LEE:.1e}",transform=ax[1].transAxes,ha="right",va="top",
           fontsize=9,bbox=dict(boxstyle="round",fc="#fff3e0",ec="#d9a441"))

fig.suptitle("C-18 P29 coherence: corrected null + look-elsewhere (permutation-of-values null is invalid here)",fontsize=11)
fig.tight_layout(rect=[0,0,1,0.95])
fig.savefig("figures/fig_c18_p29_coherence.png",dpi=130)
print("saved figures/fig_c18_p29_coherence.png  (p_raw=%.1e p_LEE=%.1e)"%(p_raw,p_LEE))
