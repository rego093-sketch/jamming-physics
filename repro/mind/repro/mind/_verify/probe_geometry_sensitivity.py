import numpy as np, math, sys
sys.path.insert(0,".")
import vp_mind_engine as E
np.random.seed(0)
A=E.load_brain_atlas(); regs=list(A["organs"].keys()); N=len(regs)
F0=np.array([A["organs"][r]["f0_hz"] for r in regs]); OMEGA=2*math.pi*F0; omega0=float(np.mean(OMEGA))
kap=E.KAPPA_EPHAPTIC

def field_contrib(POS, normalize=True):
    n=len(POS); W=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i!=j: W[i,j]=1.0/(np.linalg.norm(POS[i]-POS[j])**3)
    if normalize: W=W/W.sum(axis=1,keepdims=True)
    Rm=E._integrate(OMEGA,W,1.0*kap*omega0)[0]
    Rc=E._integrate(OMEGA,W,0.0*kap*omega0)[0]
    return Rm-Rc, Rm

print("=== (a) Does R_BRAIN value matter under row-normalization? ===")
for r in [0.085, 0.0085, 0.85, 2.0]:
    fc,Rm=field_contrib(E._ring(N,r), normalize=True)
    print(f"  R_BRAIN={r:6.4f} m : field_contribution={fc:+.5f}  R_meas={Rm:.4f}")

print("\n=== (b) Does TOPOLOGY matter? ring vs random-3D vs two-cluster (folded) [row-normalized] ===")
# ring (current)
fc,Rm=field_contrib(E._ring(N), normalize=True); print(f"  ring (equal-spacing)        : fc={fc:+.5f}  R={Rm:.4f}")
# random 3D in a sphere ~ realistic-ish scatter
P3=np.random.randn(N,3)*0.04; fc,Rm=field_contrib(P3, normalize=True); print(f"  random 3D scatter           : fc={fc:+.5f}  R={Rm:.4f}")
# two tight clusters a few mm apart (mimics opposing sulcal banks: subsets very close)
P=np.random.randn(N,3)*0.002
P[:N//2]+=np.array([0.03,0,0]); P[N//2:]+=np.array([0.03+0.0015,0,0])  # two banks 1.5mm apart
fc,Rm=field_contrib(P, normalize=True); print(f"  two banks 1.5mm (folded)    : fc={fc:+.5f}  R={Rm:.4f}")

print("\n=== (c) ABANDON row-normalization (raw 1/r^3) -- does folding then blow up coupling? ===")
for lab,POS in [("ring", E._ring(N)), ("two banks 1.5mm", P)]:
    fc,Rm=field_contrib(POS, normalize=False)
    print(f"  {lab:18s} raw 1/r^3 : fc={fc:+.5f}  R={Rm:.4f}")
