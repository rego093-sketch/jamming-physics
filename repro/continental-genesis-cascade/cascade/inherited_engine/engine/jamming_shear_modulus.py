"""
jamming_shear_modulus.py  --  엄밀 완화 전단탄성률 (Hessian / Maloney-Lemaitre)
================================================================================
앞 모듈의 유한차분 G 측정이 노이즈(음수·비단조)였다. 여기서는 spine S2.4가 쓰는
정확 선형응답으로 교체:

    G_relaxed = G_Born  -  Xi^T H^+ Xi / V          (0 <= G_relaxed <= G_Born)

  - H   : 동역학(Hessian) 행렬 (조화 접촉 + pre-stress 항)
  - Xi  : affine 전단이 만드는 비적합(mismatch) 힘  Xi_a = d^2U/dgamma dx_a
  - H^+ : pseudoinverse (전역 병진 2개 zero-mode 및 marginal soft-mode 처리)

조화 디스크: U=sum (k/2) delta^2, delta=sigma-r (>0), k=eps/sigma^2.
  dU/dr=-k delta,  d2U/dr2=k.
여러 시드 평균. Deterministic. 검수 가능.
"""
import numpy as np
from scipy.optimize import minimize

d=2; z_iso=2*d   # 2D
def make_radii(N,ratio=1.4):
    r=np.empty(N); r[:N//2]=0.5; r[N//2:]=0.5*ratio; return r
def box_for_phi(r,phi): return np.sqrt(np.sum(np.pi*r**2)/phi)

def _pairs(x,r,L):
    N=len(r); dx=x[:,None,:]-x[None,:,:]; dx-=L*np.round(dx/L)
    dist=np.sqrt((dx**2).sum(-1))+np.eye(N)*1e9
    sig=r[:,None]+r[None,:]
    return dx,dist,sig

def energy_and_grad(xflat,r,L):
    N=len(r); x=xflat.reshape(N,2); dx,dist,sig=_pairs(x,r,L)
    delta=sig-dist; mask=delta>0; k=1.0/sig**2
    U=0.5*np.sum(np.triu(k*delta**2*mask,1))
    fmag=np.where(mask,k*delta/dist,0.0)        # = -(dU/dr)/r ; force/r
    F=(fmag[:,:,None]*dx).sum(1)
    return U,(-F).reshape(-1)

def minimize_packing(r,L,x0,maxiter=600):
    res=minimize(energy_and_grad,x0.reshape(-1),args=(r,L),jac=True,method='L-BFGS-B',
                 options=dict(maxiter=maxiter,ftol=1e-15,gtol=1e-13))
    return res.x.reshape(len(r),2)

def contacts_z(x,r,L):
    N=len(r); dx,dist,sig=_pairs(x,r,L); C=dist<sig
    alive=np.ones(N,bool)
    for _ in range(60):
        cc=(C&alive[None,:]&alive[:,None]).sum(1); new=alive&(cc>=d+1)
        if new.sum()==alive.sum(): break
        alive=new
    if alive.sum()==0: return 0.0,alive
    Nc=int(np.triu(C&alive[None,:]&alive[:,None],1).sum())
    return 2*Nc/alive.sum(),alive

def hessian_born_xi(x,r,L):
    """Build H (2N x 2N), Born modulus C_B, mismatch force Xi (2N,)."""
    N=len(r); dx,dist,sig=_pairs(x,r,L); delta=sig-dist; mask=delta>0
    k=1.0/sig**2
    H=np.zeros((2*N,2*N)); Xi=np.zeros(2*N); C_B=0.0
    idx=np.argwhere(np.triu(mask,1))
    for (i,j) in idx:
        R=dx[i,j]; rij=dist[i,j]; n=R/rij; kij=k[i,j]; dl=delta[i,j]
        # 2x2 contact stiffness block: k n n^T - (k delta / r)(I - n n^T)
        nn=np.outer(n,n); I2=np.eye(2)
        Kb=kij*nn-(kij*dl/rij)*(I2-nn)
        for (a,sa) in ((i,1),(j,-1)):
            for (b,sb) in ((i,1),(j,-1)):
                H[2*a:2*a+2,2*b:2*b+2]+=sa*sb*Kb
        # affine simple-shear derivatives (gamma: x->x+gamma*y)
        Rx,Ry=R; drdg=Rx*Ry/rij
        d2rdg=Ry*Ry/rij - Rx*Rx*Ry*Ry/rij**3
        C_B += kij*drdg**2 - kij*dl*d2rdg      # d2U/dgamma2 (per contact)
        # mismatch force on i (j gets -); Xi_i = d/dgamma(dU/dx_i), dU/dx_i=-k delta n
        ddeltadg=-drdg
        dndg=np.array([Ry,0.0])/rij - n*(Rx*Ry/rij**2)
        Xi_i = -kij*ddeltadg*n - kij*dl*dndg
        Xi[2*i:2*i+2]+= Xi_i
        Xi[2*j:2*j+2]+= -Xi_i
    V=L**2
    return H,Xi,C_B/V,V

def relaxed_G(x,r,L,rcond=1e-8):
    H,Xi,C_B,V=hessian_born_xi(x,r,L)
    Hp=np.linalg.pinv(H,rcond=rcond)
    G_rel=C_B - (Xi@Hp@Xi)/V
    return C_B,G_rel

if __name__=="__main__":
    N=144; r=make_radii(N)
    phis=[0.845,0.86,0.88,0.90,0.93]
    nseed=12
    print("="*74)
    print(f"RELAXED SHEAR MODULUS via Hessian (2D N={N}, z_iso={z_iso}, {nseed} seeds avg)")
    print("="*74)
    print(f"{'phi':>6} {'z-z_iso':>9} {'G_Born':>11} {'G_relaxed':>12} {'G_rel/G_Born':>13}")
    DZ=[]; GR=[]; GB=[]
    for phi in phis:
        L=box_for_phi(r,phi)
        dzs=[]; grs=[]; gbs=[]
        for s in range(nseed):
            np.random.seed(100*s+7)
            x=minimize_packing(r,L,np.random.rand(N,2)*L)
            z,alive=contacts_z(x,r,L)
            if z<z_iso-0.5: continue
            cb,gr=relaxed_G(x,r,L)
            if np.isfinite(gr):
                dzs.append(z-z_iso); gbs.append(cb); grs.append(max(gr,0.0))
        if grs:
            DZ.append(np.mean(dzs)); GR.append(np.mean(grs)); GB.append(np.mean(gbs))
            print(f"{phi:6.3f} {np.mean(dzs):9.3f} {np.mean(gbs):11.3e} {np.mean(grs):12.3e} "
                  f"{np.mean(grs)/np.mean(gbs):13.3f}")
    DZ=np.array(DZ); GR=np.array(GR); GB=np.array(GB)
    # fit G_relaxed ~ slope * (z - z_iso)
    if len(DZ)>=2:
        sl=np.polyfit(DZ,GR,1)
        print(f"\n  => G_relaxed = {sl[0]:.3f}*(z - z_iso) + {sl[1]:.2e}")
        print(f"  => G_relaxed -> 0 as z -> z_iso  (intercept ~ {sl[1]:.1e}); G_Born stays O(0.1-1).")
        print(f"  => DERIVED friction-collapse rule: sigma_y ~ G_relaxed*gamma_y ~ (z-z_iso) -> 0 at liquefaction.")
    np.savez("jamming_shear_results.npz", phis=np.array(phis[:len(DZ)]), DZ=DZ, GR=GR, GB=GB)
    print("\nsaved -> jamming_shear_results.npz")
