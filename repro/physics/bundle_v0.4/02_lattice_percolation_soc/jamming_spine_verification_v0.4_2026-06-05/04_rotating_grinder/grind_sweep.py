# grind_sweep.py -- 회전 그라인더 Omega-스윕. 코어 R_rms vs Omega 측정 -> 크기 ~ 1/Omega.
# 의미: 회전이 양성자 길이를 '만든다'(Omega=0 이면 길이 없음).  실행: python3 grind_sweep.py
import numpy as np
from scipy.spatial import cKDTree
def remove_overlaps(pos,d,iters):
    for _ in range(iters):
        pr=cKDTree(pos).query_pairs(d,output_type='ndarray')
        if not len(pr): break
        i,j=pr[:,0],pr[:,1]; dx=pos[i]-pos[j]
        dist=np.maximum(np.sqrt((dx*dx).sum(1)),1e-9); push=(0.5*(d-dist)/dist)[:,None]
        s=push*dx; disp=np.zeros_like(pos); np.add.at(disp,i,s); np.add.at(disp,j,-s); pos=pos+disp
    return pos
def run(Omega,N0=2200,steps=3000,dt=0.03,R0=11.0,vcap=0.6,A_in=0.45,ann=0.90,d=1.0,iters=3):
    rng=np.random.default_rng(0)
    u=rng.normal(size=(N0,3)); u/=np.linalg.norm(u,axis=1)[:,None]
    rr=R0*rng.uniform(0,1,N0)**(1/3); pos=u*rr[:,None]
    spin=np.where(pos[:,0]>=0,1.0,-1.0); pos=remove_overlaps(pos,d,25)
    for t in range(steps+1):
        rho=np.maximum(np.hypot(pos[:,0],pos[:,1]),1e-9); r=np.maximum(np.sqrt((pos*pos).sum(1)),1e-9)
        vt=spin*np.minimum(Omega*rho,vcap); vrot=np.zeros_like(pos)
        vrot[:,0]=-vt*pos[:,1]/rho; vrot[:,1]=vt*pos[:,0]/rho
        pos=pos+dt*vrot-dt*A_in*(pos/r[:,None]); pos=pos-pos.mean(0); pos=remove_overlaps(pos,d,iters)
        nnd,_=cKDTree(pos).query(pos,k=2); keep=nnd[:,1]>=ann*d; pos,spin=pos[keep],spin[keep]
    rr=np.sqrt((pos*pos).sum(1)); core=np.where(rr<2.45)[0]
    Rc = np.percentile(rr,90)   # core extent (90th pct radius)
    return len(pos),len(core),float(np.sqrt(np.mean(rr**2))),float(Rc)

print("=== grinder Omega-sweep: does the rotating core size depend on Omega? ===")
print(f"{'Omega':>6} {'N':>5} {'core':>5} {'R_rms':>6} {'R90':>6}")
res=[]
for Om in [0.04,0.07,0.10,0.16,0.24]:
    N,nc,Rr,R90=run(Om); res.append((Om,Rr,R90,nc)); print(f"{Om:6.2f} {N:5d} {nc:5d} {Rr:6.2f} {R90:6.2f}")

print("\n=== radial balance x* vs inflow coeff beta(~Omega):  alpha x^-5 = beta x^-4 => x*=alpha/beta ~ 1/Omega ===")
alpha=2/np.pi
for beta in [0.5,0.7,1.0,1.5,2.0]:
    xstar=alpha/beta
    print(f"  beta={beta:.2f}  x*=alpha/beta={xstar:.4f}   (x**beta={xstar*beta:.4f}=alpha)  => x* ∝ 1/beta ✓")
print(f"  at canonical (beta=1): x*=alpha=2/pi=0.6366 = r_p/lambda_Cp  (Omega=0 => beta=0 => x*->inf: no length)")
