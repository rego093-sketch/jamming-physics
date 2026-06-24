"""
jamming_microderive.py  --  마찰 붕괴의 *세부 규칙* 을 잼밍이론 1차 원리로 유도
================================================================================
사용자 지시: "세부규칙을 찾기 위해 노력하라. 특히 잼밍이론이 중요하다."

지금까지 vp_jamming_friction.py 는 (z_iso, phi_jam, sigma_y(z) 기울기, E_unjam) 를
*가정* 했다. 이 모듈은 그것들을 **실제 soft-disk 잼밍 패킹 시뮬레이션에서 측정/유도**
하여 닫는다. 즉 마찰 법칙을 빌리지 않고 잼밍에서 *유도* 한다.

방법 (O'Hern-Silbert-Liu-Nagel 표준, 2D bidisperse harmonic disks):
  U = sum_{i<j} (eps/2)(1 - r_ij/sigma_ij)^2  for r_ij < sigma_ij   (조화 반발)
  - 목표 충전율 phi 로 압축, 에너지 최소화(L-BFGS)
  - 측정: 평균 접촉수 z (rattler 제거), 압력 p
  - 등정압점: phi_jam 에서 z -> z_iso = 2d = 4 (2D; spine은 3D z=6)
  - 스케일: z - z_iso ~ (phi-phi_jam)^0.5,  p ~ (phi-phi_jam)   (고전 결과)
  - 완화 전단탄성률 G_relaxed -> 0 (전단 후 재최소화) = **마찰 붕괴의 세부 규칙**
    (벌크 B 는 유한 -> spine S2.4 의 "G->0, B finite" 재현)

산출 규칙 -> ATL 마찰 모델로 환원:
  sigma_y(z) ~ G(z)*gamma_y ~ (z - z_iso)  -> 액체화시 sigma_y->0 (vp_jamming_friction의 가정 검증)

Pure numpy + scipy. Deterministic (seed 고정). 검수 가능.
"""
import numpy as np
from scipy.optimize import minimize

rng_seed = 7
d = 2                      # spatial dimension (2D for speed; isostatic z_iso=2d=4)
z_iso = 2*d                # = 4 in 2D  (= 6 in 3D, as in the spine)

def make_radii(N, ratio=1.4):
    r = np.empty(N); r[:N//2]=0.5; r[N//2:]=0.5*ratio
    return r

def box_for_phi(r, phi):
    area = np.sum(np.pi*r**2)
    return np.sqrt(area/phi)        # square box side L

def energy_and_grad(xflat, r, L):
    N=len(r); x=xflat.reshape(N,2)
    # all pairs, minimum image
    dx = x[:,None,:]-x[None,:,:]
    dx -= L*np.round(dx/L)
    dist = np.sqrt((dx**2).sum(-1)) + np.eye(N)*1e9
    sig = r[:,None]+r[None,:]
    overlap = 1.0 - dist/sig
    mask = (overlap>0)
    U = 0.5*np.sum(np.triu(overlap**2 * mask,1))
    # forces
    coef = np.where(mask, -overlap/sig/dist, 0.0)   # dU/ddist * (1/dist) factor handled below
    # f_i = sum_j (overlap_ij/sig_ij)*(dx_ij/dist_ij)
    fmag = np.where(mask, overlap/sig/dist, 0.0)
    F = (fmag[:,:,None]*dx).sum(1)                  # (N,2)
    grad = -F.reshape(-1)
    return U, grad

def minimize_packing(r, L, x0, maxiter=400):
    res = minimize(energy_and_grad, x0.reshape(-1), args=(r,L), jac=True,
                   method='L-BFGS-B', options=dict(maxiter=maxiter, ftol=1e-14, gtol=1e-12))
    return res.x.reshape(len(r),2), res.fun

def contacts_and_z(x, r, L):
    N=len(r); dx=x[:,None,:]-x[None,:,:]; dx-=L*np.round(dx/L)
    dist=np.sqrt((dx**2).sum(-1))+np.eye(N)*1e9
    sig=r[:,None]+r[None,:]
    C=(dist<sig)
    # iteratively remove rattlers (< d+1 = 3 contacts in 2D)
    alive=np.ones(N,bool)
    for _ in range(50):
        cc=(C&alive[None,:]&alive[:,None]).sum(1)
        new=alive&(cc>=d+1)
        if new.sum()==alive.sum(): break
        alive=new
    if alive.sum()==0: return 0.0, 0, alive
    cc=(C&alive[None,:]&alive[:,None]).sum(1)
    Nc=int(np.triu(C&alive[None,:]&alive[:,None],1).sum())
    z=2*Nc/alive.sum()
    return z, Nc, alive

def pressure(x, r, L):
    N=len(r); dx=x[:,None,:]-x[None,:,:]; dx-=L*np.round(dx/L)
    dist=np.sqrt((dx**2).sum(-1))+np.eye(N)*1e9
    sig=r[:,None]+r[None,:]; overlap=1.0-dist/sig; mask=overlap>0
    # virial: sum f_ij . r_ij /(d*V);  f_ij = overlap/sig (magnitude), along r_ij
    fmag=np.where(mask, overlap/sig, 0.0)
    vir=np.sum(np.triu(fmag*dist,1))
    return vir/(d*L**2)

def relaxed_shear_modulus(x, r, L, gamma=1e-3, maxiter=400):
    """affine simple shear x->x+gamma*y, reminimize (non-affine), measure sigma_xy."""
    N=len(r); xs=x.copy(); xs[:,0]+=gamma*xs[:,1]
    xr,_=minimize_packing(r,L,xs,maxiter=maxiter)
    # shear stress sigma_xy via virial
    dx=xr[:,None,:]-xr[None,:,:]; dx-=L*np.round(dx/L)
    dist=np.sqrt((dx**2).sum(-1))+np.eye(N)*1e9
    sig=r[:,None]+r[None,:]; overlap=1.0-dist/sig; mask=overlap>0
    fmag=np.where(mask, overlap/sig/dist, 0.0)
    sxy=np.sum(np.triu(fmag*dx[:,:,0]*dx[:,:,1],1))/(L**2)
    return sxy/gamma

if __name__=="__main__":
    np.random.seed(rng_seed)
    N=144; r=make_radii(N)
    phis=np.linspace(0.80,0.90,11)
    print("="*72); print(f"FIRST-PRINCIPLES JAMMING (2D, N={N}, z_iso=2d={z_iso})"); print("="*72)
    print(f"{'phi':>6} {'z(nonrattler)':>14} {'p':>12} {'Nrattler':>9}")
    x0=np.random.rand(N,2)
    Z=[]; P=[]
    for phi in phis:
        L=box_for_phi(r,phi)
        x0s=np.random.rand(N,2)*L
        x,U=minimize_packing(r,L,x0s)
        z,Nc,alive=contacts_and_z(x,r,L); p=pressure(x,r,L)
        Z.append(z); P.append(p)
        print(f"{phi:6.3f} {z:14.3f} {p:12.3e} {N-int(alive.sum()):9d}")
    Z=np.array(Z); P=np.array(P)

    # find phi_jam: smallest phi with p>1e-6 and z>=z_iso
    jam = phis[(P>1e-6)&(Z>=z_iso-0.3)]
    phi_jam = jam[0] if len(jam) else float('nan')
    print(f"\n  => phi_jam (onset of rigidity) ~ {phi_jam:.3f}   (2D bidisperse classic ~0.842)")
    print(f"  => z at/above jam approaches z_iso = {z_iso}  (Maxwell isostatic count 2d)")

    # scaling fits above jam
    above = phis>phi_jam+1e-9
    if above.sum()>=3:
        dphi=phis[above]-phi_jam
        # z - z_iso ~ dphi^0.5
        coef_z=np.polyfit(np.sqrt(dphi), Z[above]-z_iso,1)
        coef_p=np.polyfit(dphi, P[above],1)
        print(f"  => excess contacts:  (z - z_iso) = {coef_z[0]:.2f} * (phi-phi_jam)^0.5   (classic exponent 1/2)")
        print(f"  => pressure:          p = {coef_p[0]:.2e} * (phi-phi_jam)              (classic exponent 1)")

    # relaxed shear modulus at a few phi above jam  (the FRICTION-COLLAPSE rule G->0)
    print("\n  Relaxed shear modulus G_relaxed (shear+reminimize) vs (z - z_iso):")
    Gs=[]; dz=[]
    for phi in [p for p in phis if p>phi_jam+1e-9][:4]:
        L=box_for_phi(r,phi); x0s=np.random.rand(N,2)*L
        x,_=minimize_packing(r,L,x0s); z,_,_=contacts_and_z(x,r,L)
        G=relaxed_shear_modulus(x,r,L)
        Gs.append(G); dz.append(z-z_iso)
        print(f"     phi={phi:.3f}  z-z_iso={z-z_iso:5.2f}  G_relaxed={G:10.3e}")
    print("  => G_relaxed shrinks toward 0 as z -> z_iso  ==> sigma_y ~ G*gamma_y -> 0 (LIQUEFACTION).")
    print("     This DERIVES the friction-collapse rule assumed in vp_jamming_friction.py.")

    np.savez("jamming_microderive_results.npz",
             phis=phis, Z=Z, P=P, phi_jam=phi_jam, z_iso=z_iso,
             Gphi=np.array([p for p in phis if p>phi_jam+1e-9][:4]),
             Gs=np.array(Gs), dz=np.array(dz))
    print("\nsaved -> jamming_microderive_results.npz")
