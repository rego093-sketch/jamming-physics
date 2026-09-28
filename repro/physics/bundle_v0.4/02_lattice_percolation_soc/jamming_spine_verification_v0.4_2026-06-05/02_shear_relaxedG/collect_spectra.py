"""Collect the full vibrational spectrum (Hessian eigenvalues -> frequencies omega) of the rigid
backbone for each packing, to build the density of states D(omega) and the characteristic
frequency omega*(z). Marginal-stability benchmark: omega* ~ Delta z -> 0 at z_iso=2d=6
(Silbert-Liu-Nagel PRL 95, 098301 (2005); Wyart-Nagel-Witten EPL 72, 486 (2005)).

Resumable: one .npz per (N,phi,seed). Usage: python3 collect_spectra.py N s0 s1
"""
import sys, os, numpy as np
from numpy.linalg import eigvalsh
from relaxed_shear import make_packing, backbone_mask, mean_z, hessian_dense, d

OUT = "/home/claude/vp_shear/results/spectra"
os.makedirs(OUT, exist_ok=True)
PHIS = [0.640, 0.658, 0.685, 0.705, 0.730, 0.760]

def one(N, phi, sd):
    f = f"{OUT}/N{N}_phi{phi:.3f}_sd{sd}.npz"
    if os.path.exists(f): return "skip"
    pos, R, E, mF = make_packing(N, phi, 1.0, sd, steps=8000, ftol=1e-12, polish=True)
    if E < 1e-13: 
        np.savez(f, jammed=0); return "unjammed"
    keep = backbone_mask(pos, R, 1.0); z = mean_z(pos, R, 1.0, keep)
    p = pos[keep]
    H = hessian_dense(p, R, 1.0)
    w = eigvalsh(H)          # ascending eigenvalues = omega^2
    w = np.sort(w)
    # drop the 3 global translational zero modes
    w_phys = w[d:]
    omega = np.sqrt(np.clip(w_phys, 0, None))
    np.savez(f, jammed=1, omega=omega.astype(np.float32), z=float(z),
             nbb=int(keep.sum()), mF=float(mF), w2min=float(w_phys.min()),
             nneg=int((w_phys < -1e-9).sum()))
    return f"z={z:.3f} nbb={keep.sum()} w2min={w_phys.min():.2e} nneg={(w_phys<-1e-9).sum()}"

if __name__ == "__main__":
    import time
    N = int(sys.argv[1]); s0 = int(sys.argv[2]); s1 = int(sys.argv[3])
    t0 = time.time(); n = 0
    for sd in range(s0, s1):
        for phi in PHIS:
            if time.time() - t0 > 270:
                print(f"[time budget] {n} configs this call"); sys.exit()
            r = one(N, phi, sd); n += 1
            if r != "skip":
                print(f"N={N} phi={phi:.3f} sd={sd}: {r}  [{time.time()-t0:.0f}s]")
    print(f"[done] {n} this call ({time.time()-t0:.0f}s)")
