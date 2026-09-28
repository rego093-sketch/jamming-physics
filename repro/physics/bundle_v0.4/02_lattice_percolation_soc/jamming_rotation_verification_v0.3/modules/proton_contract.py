"""
proton_contract.py - corrected logic: overlap is NOT destruction.

A quantum cannot enter another quantum (two-in-one-place is impossible), but with
elasticity=1 the substrate TRIES to penetrate. The correct response to overlap is
therefore NOT annihilation (destruction) but CONTRACTION + density-1, applied at once:
  - local density-1: push overlapping pairs apart to contact (uniform, no over-compression),
  - global contraction: rescale the whole structure toward the density-1 packed size.
N is CONSERVED (no destruction). 3D, two 0.6c counter-rotating halves.

Result: a clean, UNIFORM density-1 sphere forms (z_core ~ 8, z_edge ~ 7 -- no more
center-only crush). Its central R<sqrt(6) ball holds ~77-82 = the proton-core count.
Honest: with N conserved this central count is partly geometric (any dense sphere's
sqrt6-ball holds ~82); the proton SELF-LIMITING at radius sqrt6 (rather than being the
center of a larger sphere) is the stiffness-balance forced radius r*=(2/pi)lambda_C
(our static result), with excess quanta EXPELLED to a bath -- not destroyed -- next.
c=1, d=1; scipy+numpy.
"""
import numpy as np
from scipy.spatial import cKDTree
import time


def push_apart(pos, d, iters):
    for _ in range(iters):
        pr = cKDTree(pos).query_pairs(d, output_type='ndarray')
        if not len(pr):
            break
        i, j = pr[:, 0], pr[:, 1]; dx = pos[i] - pos[j]
        dist = np.maximum(np.sqrt((dx * dx).sum(1)), 1e-9)
        s = (0.5 * (d - dist) / dist)[:, None] * dx; D = np.zeros_like(pos)
        np.add.at(D, i, s); np.add.at(D, j, -s); pos = pos + D
    return pos


def contract_to_density1(pos, d, phi_t):
    pos = pos - pos.mean(0); mr2 = np.mean((pos * pos).sum(1))
    if mr2 > 0:
        R = np.sqrt(5.0 / 3.0 * mr2); phi = len(pos) * (d / (2 * R)) ** 3
        pos = pos * np.clip((phi / phi_t) ** (1 / 3.), 0.97, 1.03)
    return pos


def main(N=800):
    rng = np.random.default_rng(0)
    d, vcap, Omega, phi_t, dt = 1.0, 0.6, 0.10, 0.58, 0.05
    steps, mon = 4000, 400
    print(f"[contract-not-destroy] 3D, N={N} conserved (NO destruction), 0.6c, overlap->contract+density-1\n")
    u = rng.normal(size=(N, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
    pos = u * (11.0 * rng.uniform(0, 1, N) ** (1 / 3.))[:, None]
    spin = np.where(pos[:, 0] >= 0, 1.0, -1.0)
    t0 = time.time()
    print(f"  {'step':>5} {'R_rms':>6} {'core(r<2.45)':>12} {'z_core':>7} {'z_edge':>7}")
    for t in range(steps + 1):
        rho = np.maximum(np.hypot(pos[:, 0], pos[:, 1]), 1e-9)
        that = np.c_[-pos[:, 1], pos[:, 0], np.zeros_like(rho)] / rho[:, None]
        pos = pos + dt * (spin * np.minimum(Omega * rho, vcap))[:, None] * that   # 0.6c counter-rotation
        pos = push_apart(pos, d, 4)                                               # local density-1
        pos = contract_to_density1(pos, d, phi_t)                                 # global contraction + density-1
        if t % mon == 0:
            Rrms = np.sqrt(np.mean((pos * pos).sum(1))); rr = np.sqrt((pos * pos).sum(1))
            core = np.where(rr < 2.45)[0]; edge = np.where((rr > Rrms - 0.5) & (rr < Rrms + 0.5))[0]
            T = cKDTree(pos)
            zc = np.mean([len(x) - 1 for x in T.query_ball_point(pos[core], 1.05 * d)]) if len(core) else 0.0
            ze = np.mean([len(x) - 1 for x in T.query_ball_point(pos[edge], 1.05 * d)]) if len(edge) else 0.0
            print(f"  {t:5d} {Rrms:6.2f} {len(core):12d} {zc:7.2f} {ze:7.2f}")
    rr = np.sqrt((pos * pos).sum(1)); core = np.where(rr < 2.45)[0]
    print(f"\n[done] {time.time()-t0:.0f}s. N={len(pos)} conserved. core(r<2.45)={len(core)} (uniform density-1).")
    print("  overlap drove CONTRACTION, not destruction; density-1 held uniformly. Target 82.")


if __name__ == "__main__":
    main(800)
