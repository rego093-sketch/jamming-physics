"""
proton_formation_3d.py - 3D proton-core formation (the real target: 82 = #{R^2<=6}).

Same three keys as the working 2D version, in 3D (where contraction is geometrically
stronger -- inflow converges as r^-2, and isostatic z=6 is tighter):
  1) real-time incompressible density-1 (overlap-removal projection each step),
  2) N allowed to drop via annihilation (no regen of the core) -> real contraction,
  3) strong contraction; 0.6c counter-rotation (two halves about the shared z-axis).
Finer resolution (more particles) and finer time step per guidance. c=1, d=1.
Core measured within r < sqrt(6) ~ 2.45; 3D target ~82.
"""
import numpy as np
from scipy.spatial import cKDTree
import time


def remove_overlaps(pos, d, iters):
    for _ in range(iters):
        pr = cKDTree(pos).query_pairs(d, output_type='ndarray')
        if not len(pr):
            break
        i, j = pr[:, 0], pr[:, 1]; dx = pos[i] - pos[j]
        dist = np.maximum(np.sqrt((dx * dx).sum(1)), 1e-9); push = (0.5 * (d - dist) / dist)[:, None]
        s = push * dx; disp = np.zeros_like(pos)
        np.add.at(disp, i, s); np.add.at(disp, j, -s)
        pos = pos + disp
    return pos


def main(N0=3000):
    rng = np.random.default_rng(0)
    d, dt = 1.0, 0.03                                   # finer time step
    R0, vcap, Omega, A_in = 12.0, 0.6, 0.10, 0.45       # 0.6c; strong contraction (full collapse to the core)
    ann, iters, steps, mon = 0.90, 3, 6000, 500

    est = N0 * steps * 2e-6
    print(f"[load] 3D, N0={N0}, dt={dt}, steps={steps}, incompressible density-1/step  (~{est:.0f}s, cap 280)\n")
    # init: N0 spheres uniformly in a ball of radius R0
    u = rng.normal(size=(N0, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
    rr = R0 * rng.uniform(0, 1, N0) ** (1.0 / 3.0)
    pos = u * rr[:, None]
    spin = np.where(pos[:, 0] >= 0, 1.0, -1.0)           # two counter-rotating halves about z
    pos = remove_overlaps(pos, d, 25)

    t0 = time.time()
    print(f"  {'step':>5} {'N':>5} {'R_rms':>6} {'core(r<2.45)':>12} {'z_core':>7}")
    for t in range(steps + 1):
        rho = np.maximum(np.hypot(pos[:, 0], pos[:, 1]), 1e-9)         # cylindrical radius (about z)
        r = np.maximum(np.sqrt((pos * pos).sum(1)), 1e-9)             # spherical radius
        # 0.6c counter-rotation about z (tangential in xy), capped
        vt = spin * np.minimum(Omega * rho, vcap)
        vrot = np.zeros_like(pos)
        vrot[:, 0] = -vt * pos[:, 1] / rho; vrot[:, 1] = vt * pos[:, 0] / rho
        # strong contraction (3D radial inflow) + update
        pos = pos + dt * vrot - dt * A_in * (pos / r[:, None])
        pos = pos - pos.mean(0)                                       # central alignment
        pos = remove_overlaps(pos, d, iters)                          # real-time density-1
        nnd, _ = cKDTree(pos).query(pos, k=2)
        keep = nnd[:, 1] >= ann * d                                   # annihilate excess (no regen)
        pos, spin = pos[keep], spin[keep]
        if t % mon == 0:
            Rrms = np.sqrt(np.mean((pos * pos).sum(1))); rr = np.sqrt((pos * pos).sum(1))
            core = np.where(rr < 2.45)[0]; nc = len(core)
            zc = (np.mean([len(x) - 1 for x in cKDTree(pos).query_ball_point(pos[core], 1.05 * d)])
                  if nc else 0.0)
            print(f"  {t:5d} {len(pos):5d} {Rrms:6.2f} {nc:12d} {zc:7.2f}")

    rr = np.sqrt((pos * pos).sum(1)); core = np.where(rr < 2.45)[0]
    nb = cKDTree(pos).query_ball_point(pos[core], 1.05 * d); zc = np.mean([len(x) - 1 for x in nb]) if len(core) else 0
    print(f"\n[done] {time.time()-t0:.0f}s. SELF-LIMITED 3D core: total N={len(pos)}, "
          f"core(r<2.45)={len(core)} cells, z_core={zc:.2f}")
    print(f"  3D proton-core target #{{R^2<=6}} = 82  (isostatic z=6).")


if __name__ == "__main__":
    main(3000)
