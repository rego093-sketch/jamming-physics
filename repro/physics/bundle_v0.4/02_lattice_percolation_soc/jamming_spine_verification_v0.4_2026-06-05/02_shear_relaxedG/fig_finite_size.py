"""Finite-size figure across N=256,512,1024: G_relaxed(z) means+fits, and z0 vs 1/N consistency."""
import csv, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "/home/claude/vp_shear/results/relaxedG.csv"
def fnum(x):
    try: return float(x)
    except: return np.nan

def load(N):
    out=[]
    for r in csv.DictReader(open(CSV)):
        if int(r["N"])!=N or int(r["jammed"])!=1: continue
        psd=(r["psd"]=="1"); mF=fnum(r["mF"]); GR=fnum(r["G_relaxed"]); GB=fnum(r["G_Born"]); z=fnum(r["z"])
        if not(psd and np.isfinite(mF) and mF<1e-7 and np.isfinite(GR)): continue
        out.append((float(r["phi"]),z,GB,GR))
    a=np.array(out); return a[:,0],a[:,1],a[:,2],a[:,3]

def linfit(zz,gg):
    A=np.vstack([zz,np.ones_like(zz)]).T;(a,b),*_=np.linalg.lstsq(A,gg,rcond=None)
    pred=A@np.array([a,b]); R2=1-np.sum((gg-pred)**2)/np.sum((gg-gg.mean())**2); return a,b,-b/a,R2
def boot(zz,gg,nb=5000):
    rng=np.random.default_rng(1);o=[]
    for _ in range(nb):
        k=rng.integers(0,len(zz),len(zz));a,b,*_=linfit(zz[k],gg[k])
        if abs(a)>1e-6:o.append(-b/a)
    o=np.array(o);return np.median(o),np.percentile(o,[2.5,97.5])

Ns=[256,512,1024]; cols={256:"#7aa6c2",512:"#2e6f9e",1024:"#c0392b"}
fig,(axL,axR)=plt.subplots(1,2,figsize=(12.4,5.2),dpi=140,gridspec_kw={"width_ratios":[1.7,1]})
summary={}
for N in Ns:
    phi,z,GB,GR=load(N)
    phis=sorted(set(phi)); zb=[];gm=[];se=[];gbm=[]
    for p in phis:
        m=phi==p; zb.append(z[m].mean()); gm.append(GR[m].mean())
        se.append(GR[m].std(ddof=1)/np.sqrt(m.sum())); gbm.append(GB[m].mean())
    zb=np.array(zb);gm=np.array(gm);se=np.array(se)
    a,b,z0,R2=linfit(z,GR); zm,(lo,hi)=boot(z,GR); summary[N]=(zm,lo,hi,R2,a,np.mean(gbm))
    axL.errorbar(zb,gm,yerr=se,fmt="o",ms=5.5,c=cols[N],capsize=2.5,lw=1.2,
                 label=f"N={N}: $G_r$ mean$\\pm$SEM",zorder=4)
    zl=np.linspace(5.9,9.4,40); axL.plot(zl,a*(zl-zm),"-",c=cols[N],lw=1.8,alpha=0.85,zorder=3,
                 label=f"   fit $z_0$={zm:.2f} ($R^2$={R2:.2f})")
    # G_Born band (finite) per N -- thin dashed at its mean level range
    axL.plot(zb,gbm,"s--",ms=4,c=cols[N],alpha=0.35,lw=0.9,zorder=2)
axL.axvline(6.0,ls="--",c="#222",lw=1.4,zorder=1)
axL.axhline(0,ls=":",c="#999",lw=1.0,zorder=1)
axL.annotate("$z_{\\rm iso}=2d=6$",xy=(6.03,1.30),color="#222",fontsize=10.5)
axL.annotate("$G_{\\rm Born}$ (affine) — stays finite",xy=(8.0,1.30),color="#555",fontsize=9.5)
axL.set_xlabel("contact number  $z$  (rigid backbone)",fontsize=12)
axL.set_ylabel("shear modulus",fontsize=12)
axL.set_title("$G_{\\rm relaxed}\\to 0$ at $z_{\\rm iso}=6$; $G_{\\rm Born}$ finite — across system size",fontsize=11.5)
axL.set_xlim(5.9,9.45); axL.set_ylim(-0.1,1.62); axL.grid(alpha=0.18)
axL.legend(fontsize=8.0,loc="upper left",ncol=1,framealpha=0.92)

# right: z0 vs 1/N
invN=np.array([1.0/N for N in Ns])
z0s=np.array([summary[N][0] for N in Ns])
los=np.array([summary[N][1] for N in Ns]); his=np.array([summary[N][2] for N in Ns])
axR.errorbar(invN,z0s,yerr=[z0s-los,his-z0s],fmt="o",ms=9,c="#1f4e79",capsize=5,lw=1.6,zorder=4)
for N in Ns:
    axR.annotate(f"N={N}",xy=(1.0/N,summary[N][0]),xytext=(1.0/N+3e-5,summary[N][0]+0.04),fontsize=9)
axR.axhline(6.0,ls="--",c="#c0392b",lw=1.6,zorder=2,label="$z_{\\rm iso}=2d=6$")
axR.set_xlabel("$1/N$",fontsize=12); axR.set_ylabel("fit zero-crossing  $z_0$",fontsize=12)
axR.set_title("$z_0$ consistent with 6 at every $N$\n(95% CI; precision $\\uparrow$ with $N$)",fontsize=11)
axR.set_xlim(-3e-4,4.4e-3); axR.set_ylim(5.4,6.7); axR.grid(alpha=0.2)
axR.legend(fontsize=9.5,loc="lower right")
fig.tight_layout()
fig.savefig("/home/claude/vp_shear/results/relaxedG_finite_size.png",dpi=140)
fig.savefig("/home/claude/vp_shear/results/relaxedG_finite_size.pdf")
print("FINITE-SIZE SUMMARY  (z0 [95% CI], R2, slope a, <G_Born>)")
for N in Ns:
    zm,lo,hi,R2,a,gbm=summary[N]
    print(f"  N={N:5d}:  z0={zm:.3f} [{lo:.3f},{hi:.3f}]   R2={R2:.3f}   a={a:.4f}   <G_Born>={gbm:.3f}")
print("saved relaxedG_finite_size.png/.pdf")
