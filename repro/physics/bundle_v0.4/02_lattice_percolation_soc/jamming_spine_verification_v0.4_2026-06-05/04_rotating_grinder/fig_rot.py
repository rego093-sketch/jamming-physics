# fig_rot.py -- 회전 그라인더 그림: 입자수 감쇠, 코어 크기 안정화(~82 = #{r^2<=6}=81+1), z_core.
# 실행: python3 fig_rot.py  (vp_grinder_3d.py 의 출력/로직에 대응)
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

# --- panel A: grinder formation (baseline run, N0=3000) ---
step=np.array([0,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000])
N   =np.array([3000,1985,1131,711,531,451,399,375,351,339,319,301,301])
core=np.array([31,65,72,73,72,73,79,81,77,77,74,77,79])
# --- panel B: Omega sweep + balance ---
Om =np.array([0.04,0.07,0.10,0.16,0.24]); Rrms=np.array([3.48,3.34,3.19,3.15,2.98])
alpha=2/np.pi

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(11.4,4.5))
axb=ax1.twinx()
ax1.plot(step,N,'o-',color="#999",lw=1.5,label="total N (collapses)")
axb.plot(step,core,'s-',color="#1f77b4",lw=1.8,label="core $r<\\sqrt{6}$")
axb.axhline(82,color="crimson",ls="--",lw=1.3,label="target 82 (= #cells, $R^2{\\leq}6$)")
ax1.set_xlabel("grind step"); ax1.set_ylabel("total N",color="#999")
axb.set_ylabel("core cells",color="#1f77b4"); axb.set_ylim(0,95)
ax1.set_title("Rotating grinder: a stationary non-collapsing core\n(counter-rotating hemispheres $v=\\Omega\\times r$, density-1, annihilation)",fontsize=10)
l1,la=ax1.get_legend_handles_labels(); l2,lb=axb.get_legend_handles_labels()
axb.legend(l1+l2,la+lb,fontsize=7.5,loc="center right")

# balance curve x*=alpha/beta vs beta(~Omega)
b=np.linspace(0.3,2.2,100); ax2.plot(b,alpha/b,'k-',lw=2,label="$x^*=\\alpha/\\beta\\ \\ (\\propto1/\\Omega)$")
ax2.scatter([1.0],[alpha],s=130,marker="*",color="crimson",zorder=5,edgecolor="k",
            label="canonical: $x^*=2/\\pi=r_p/\\lambda_{C,p}$")
# grinder R_rms(Omega) normalized to overlay the inverse trend (right axis)
ax2b=ax2.twinx()
ax2b.plot(Om/0.10,Rrms,'o-',color="#2ca02c",lw=1.5,label="grinder $R_{\\rm rms}(\\Omega)$ (MD)")
ax2b.set_ylabel("grinder $R_{\\rm rms}$",color="#2ca02c"); ax2b.set_ylim(2.7,3.7)
ax2.set_xlabel("inflow coeff $\\beta\\propto\\Omega$  (rotation rate)")
ax2.set_ylabel("$x^*=r/\\lambda_{C,p}$ (balance)")
ax2.set_title("Rotation CREATES the size:  $x^*\\propto1/\\Omega$\n$\\Omega\\!\\to\\!0\\Rightarrow$ no length;  canonical $\\Rightarrow x^*=2/\\pi$",fontsize=10)
l3,lc=ax2.get_legend_handles_labels(); l4,ld=ax2b.get_legend_handles_labels()
ax2.legend(l3+l4,lc+ld,fontsize=7.5,loc="upper right"); ax2.set_xlim(0.3,2.2)
plt.tight_layout()
for e in ("png","pdf"): plt.savefig(f"rotating_quantum.{e}",dpi=150,bbox_inches="tight")
print("saved rotating_quantum")
