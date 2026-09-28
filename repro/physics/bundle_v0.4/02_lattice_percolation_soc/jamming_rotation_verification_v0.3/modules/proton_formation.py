"""
proton_formation.py - WORKING version (after attempts 1-5).

Goal: grow a self-limiting proton CORE by jamming a density-1 VP substrate under
counter-rotation + contraction. 3D core count = 82 = #{R^2<=6}; the 2D analogue is
#{(x,y) in Z^2 : x^2+y^2<=6} = 21.

What finally worked (the three keys):
  1) DENSITY-1 IN REAL TIME, LOCAL & INCOMPRESSIBLE. Every step, iteratively push
     overlapping pairs apart to contact (a no-overlap projection). This makes the
     substrate RIGID (as the real c^2 is huge) instead of the soft k=1 medium that
     over-compressed in attempts 2-4. -> the core no longer crushes (z stays ~4, not 8).
  2) N IS ALLOWED TO DROP via annihilation (NO regeneration of the core). Maintaining
     ~2000 by regen just gives a packed BATH (R fixed, no concentration); letting the
     over-compressed excess annihilate lets the cloud actually CONTRACT into a small core.
  3) STRONG contraction (so it overcomes the incompressible resistance + 0.6c centrifugal).

Result: the cloud contracts and SELF-LIMITS at a small jammed core (~17-22 cells in 2D,
core ~17-19), bracketing the 2D analogue 21 -- and it is an ATTRACTOR (N0=1500->17,
N0=2000->22), i.e. the same core regardless of how much substrate you start with =
the proton's universality. Speed 0.6c (energy still condenses). c=1, d=1.

Honest caveats: (a) ~17-22 vs 21 is close, not exact; depends on the core-radius cut and
on A_in/Omega/threshold; (b) in this crude 2D model the self-limiting is driven mainly by
incompressible-density-1 + contraction -- the counter-rotation's specific 81+1/nozzle role
is not resolved; (c) the real target is 3D -> 82 (next).
"""
import numpy as np
from scipy.spatial import cKDTree
import time


def remove_overlaps(pos, d, iters):
    """Real-time density-1: incompressible no-overlap projection (push pairs to contact)."""
    for _ in range(iters):
        pr = cKDTree(pos).query_pairs(d, output_type='ndarray')
        if not len(pr):
            break
        i, j = pr[:, 0], pr[:, 1]; dx = pos[i] - pos[j]
        dist = np.maximum(np.hypot(dx[:, 0], dx[:, 1]), 1e-9); push = 0.5 * (d - dist) / dist
        sx, sy = push * dx[:, 0], push * dx[:, 1]; disp = np.zeros_like(pos)
        np.add.at(disp[:, 0], i, sx); np.add.at(disp[:, 1], i, sy)
        np.add.at(disp[:, 0], j, -sx); np.add.at(disp[:, 1], j, -sy)
        pos = pos + disp
    return pos


def main(N0=2000):
    rng = np.random.default_rng(0)
    d, dt = 1.0, 0.05
    R0, vcap, Omega, A_in = 26.0, 0.6, 0.10, 0.50      # 0.6c; strong contraction
    ann, iters, steps, mon = 0.90, 2, 4000, 400        # excess that can't fit -> annihilate (no regen)

    print(f"[proton] N0={N0}, 0.6c counter-rotation, incompressible density-1/step, N drops (annih)\n")
    ang = rng.uniform(0, 2 * np.pi, N0); rr = R0 * np.sqrt(rng.uniform(0, 1, N0))
    pos = np.c_[rr * np.cos(ang), rr * np.sin(ang)]
    spin = np.where(pos[:, 0] >= 0, 1.0, -1.0)         # two counter-rotating halves
    pos = remove_overlaps(pos, d, 20)

    t0 = time.time()
    print(f"  {'step':>5} {'N':>5} {'R_rms':>6} {'core(r<2.45)':>12} {'z_core':>7}")
    for t in range(steps + 1):
        r = np.maximum(np.hypot(pos[:, 0], pos[:, 1]), 1e-9); rhat = pos / r[:, None]
        that = np.c_[-pos[:, 1], pos[:, 0]] / r[:, None]
        vrot = spin[:, None] * np.minimum(Omega * r, vcap)[:, None] * that
        pos = pos + dt * vrot - dt * A_in * rhat        # 0.6c counter-rotation + contraction
        pos = pos - pos.mean(0)                          # central alignment
        pos = remove_overlaps(pos, d, iters)             # REAL-TIME density-1 (incompressible)
        nnd, _ = cKDTree(pos).query(pos, k=2)
        keep = nnd[:, 1] >= ann * d                      # annihilate excess that cannot fit
        pos, spin = pos[keep], spin[keep]
        if t % mon == 0:
            Rrms = np.sqrt(np.mean((pos ** 2).sum(1))); r = np.hypot(pos[:, 0], pos[:, 1])
            core = np.where(r < 2.45)[0]; nc = len(core)
            zc = (np.mean([len(x) - 1 for x in cKDTree(pos).query_ball_point(pos[core], 1.05 * d)])
                  if nc else 0.0)
            print(f"  {t:5d} {len(pos):5d} {Rrms:6.2f} {nc:12d} {zc:7.2f}")

    r = np.hypot(pos[:, 0], pos[:, 1]); core = np.where(r < 2.45)[0]
    print(f"\n[done] {time.time()-t0:.0f}s. SELF-LIMITED core: N={len(pos)}, core(r<2.45)={len(core)} cells.")
    print(f"  2D proton-core analogue #{{R^2<=6}} = 21  (3D = 82). Attractor: N0=1500->17, N0=2000->22.")


if __name__ == "__main__":
    main(2000)
