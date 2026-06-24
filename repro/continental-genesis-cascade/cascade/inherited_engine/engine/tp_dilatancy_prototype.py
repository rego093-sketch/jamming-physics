"""
tp_dilatancy_prototype.py  --  ATL 백서 WP-T1/WP-T2 핵심 물리 prototype (implicit)
================================================================================
1D fault-normal coupled diffusion of T and p across a shear zone of width w,
with frictional heating, thermal pressurization (TP, weakening) and dilatancy
(strengthening). Diffusion is solved implicitly (backward Euler, tridiagonal)
so the timestep is set by accuracy, not stability.

Established physics (refs for the plan, text not reproduced):
  Rice (2006) JGR 111 B05311; Lachenbruch (1980); Segall & Rice (1995);
  Aben & Brantut (2020); Parez et al. (2023). Pure numpy/scipy, deterministic.
"""
import numpy as np
from scipy.linalg import solve_banded

# ---- physical parameters (literature ranges) ----
rho_c=2.7e6; alpha_th=1.0e-6; f=0.6
sigma_n=150e6; p0=50e6
Lam_TP=0.5e6; beta_str=3.0e-10
eps_dil=1.0e-4; dc_dil=2.0e-3
w=3.0e-3; T_melt=1000.0

# ---- grid ----
Y=0.10; Ny=401
y=np.linspace(-Y,Y,Ny); dy=y[1]-y[0]
in_zone=np.abs(y)<=w/2.0

def _banded(r, n):
    """tridiagonal (I - r*D2) in banded form for solve_banded, Dirichlet ends."""
    ab=np.zeros((3,n))
    ab[0,1:]=-r          # upper
    ab[1,:]=1+2*r        # diag
    ab[2,:-1]=-r         # lower
    ab[1,0]=1.0; ab[0,1]=0.0          # row 0 Dirichlet
    ab[1,-1]=1.0; ab[2,-2]=0.0        # row N-1 Dirichlet
    return ab

def run(V, alpha_hy, total_slip=0.05, nsteps=2000):
    gammadot=V/w
    t_end=total_slip/V; dt=t_end/nsteps
    rT=dt*alpha_th/dy**2; rP=dt*alpha_hy/dy**2
    abT=_banded(rT,Ny); abP=_banded(rP,Ny)

    T=np.zeros(Ny); p=np.full(Ny,p0)
    rec=dict(slip=[],tau=[],pz=[],Tz=[])
    p_min=p0; cross=None
    for n in range(nsteps):
        slip=V*n*dt
        p_zone=p[in_zone].mean()
        tau=f*max(sigma_n-p_zone,0.0)
        q=tau*gammadot
        srcT=np.zeros(Ny); srcP=np.zeros(Ny)
        srcT[in_zone]=q/rho_c
        ddil=eps_dil*gammadot*np.exp(-slip/dc_dil)
        srcP[in_zone]=Lam_TP*(q/rho_c)-ddil/beta_str
        # backward-Euler implicit diffusion with explicit source (IMEX)
        rhsT=T+dt*srcT; rhsT[0]=0.0; rhsT[-1]=0.0
        rhsP=p+dt*srcP; rhsP[0]=p0;  rhsP[-1]=p0
        T=solve_banded((1,1),abT,rhsT)
        p=solve_banded((1,1),abP,rhsP)
        p=np.maximum(p,0.0)
        pz_now=p[in_zone].mean()
        if pz_now<p_min: p_min=pz_now
        if cross is None and pz_now>p0: cross=slip
        if n%max(1,nsteps//300)==0:
            rec['slip'].append(slip); rec['tau'].append(tau)
            rec['pz'].append(p[in_zone].mean()); rec['Tz'].append(T[in_zone].max())
    for k in rec: rec[k]=np.array(rec[k])
    tau0=f*(sigma_n-p0)
    return dict(**rec, tau0=tau0, V=V, alpha_hy=alpha_hy,
                weakening=1.0-rec['tau'][-1]/tau0, Tmax=rec['Tz'].max(),
                melted=bool(rec['Tz'].max()>=T_melt), dp_net=rec['pz'][-1]-p0,
                dp_dil=p_min-p0, cross=cross)

if __name__=="__main__":
    print("="*72); print("BASELINE (WP-T1: TP weakening + melting check)"); print("="*72)
    cases=[("undrained V=1",1.0,1e-6),("drained   V=1",1.0,1e-2),
           ("undrained V=0.01",0.01,1e-6)]
    b07={}
    for name,V,a in cases:
        o=run(V,a); b07[name]=o
        print(f"{name:18s}: weaken={o['weakening']*100:5.1f}%  "
              f"Tmax={o['Tmax']:6.0f}K  dp_net={o['dp_net']/1e6:+6.1f}MPa  melted={o['melted']}")
    print("\n"+"="*72); print("REGIME SWEEP (WP-T2: weaken / strengthen / melt)"); print("="*72)
    Vs=np.array([0.01,0.03,0.1,0.3,1.0,3.0]); alphas=np.logspace(-6,-2,5)
    W=np.zeros((len(Vs),len(alphas))); Tm=np.zeros_like(W); DP=np.zeros_like(W)
    hdr="V \\ a_hy".rjust(9)+"  "+"  ".join(f"{a:.0e}" for a in alphas)
    print(hdr)
    for i,V in enumerate(Vs):
        tags=[]
        for j,a in enumerate(alphas):
            o=run(V,a); W[i,j]=o['weakening']; Tm[i,j]=o['Tmax']; DP[i,j]=o['dp_net']
            tags.append("MELT" if o['melted'] else "WEAK" if o['weakening']>0.5
                        else "STRG" if o['dp_net']<0 else "----")
        print(f"{V:9.2f}  "+"  ".join(f"{t:>4}" for t in tags))
    np.savez("tp_dilatancy_results.npz", Vs=Vs, alphas=alphas, W=W, Tm=Tm, DP=DP,
             u_slip=b07["undrained V=1"]['slip'], u_tau=b07["undrained V=1"]['tau'],
             u_T=b07["undrained V=1"]['Tz'], u_tau0=b07["undrained V=1"]['tau0'],
             d_slip=b07["drained   V=1"]['slip'], d_tau=b07["drained   V=1"]['tau'],
             d_T=b07["drained   V=1"]['Tz'])
    print("\nsaved -> tp_dilatancy_results.npz")
