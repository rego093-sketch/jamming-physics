"""
liquid_flow.py - the LIQUID flows: surface tension rounds the drop to a sphere.

Static minimisation (liquid_shell.py part A) leaves an elongated drop STUCK --
rounding needs the liquid to FLOW. Here we let it flow: overdamped Langevin
dynamics (the simplest model liquid; inertia-free, thermostatted by the noise)
on a FREE Lennard-Jones drop in vacuum (zero gravity). Surface tension -- the
energy of the incomplete surface shell -- then drives the drop toward the shape
of least area: the SPHERE.

    overdamped Langevin (drag zeta=1):
        dx = F dt + sqrt(2 kT dt) * xi,    xi ~ N(0, I)

We start from an ELONGATED drop and watch the asphericity kappa^2 of the
largest connected cluster fall toward 0 (sphere). The cluster is tracked (atoms
that evaporate into vacuum are dropped from the shape measure).

kT is set in the LJ LIQUID range (cohesive enough not to boil over the run,
mobile enough to flow). This is the SAME mobility that, under shear, gives the
Newtonian/diverging viscosity of Pillar I.

Self-contained: numpy; reuses liquid_shell.py for the LJ engine.
"""
import sys
import time
import numpy as np
from liquid_shell import lj_EFV, carve_rod, shape_anisotropy


def largest_cluster(pos, rlink=1.5):
    """Indices of the largest connected component (atoms within rlink)."""
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    d2 = np.einsum("ij,ij->i", dx, dx)
    e = d2 < rlink ** 2
    adj = [[] for _ in range(N)]
    for a, b in zip(iu[e], ju[e]):
        adj[a].append(b); adj[b].append(a)
    seen = np.zeros(N, bool)
    best = []
    for s in range(N):
        if seen[s]:
            continue
        stack, comp = [s], []
        seen[s] = True
        while stack:
            u = stack.pop(); comp.append(u)
            for w in adj[u]:
                if not seen[w]:
                    seen[w] = True; stack.append(w)
        if len(comp) > len(best):
            best = comp
    return np.array(best)


def run(N=200, aspect=2.4, kT=0.50, dt=0.004, steps=44000, sample=2000, seed=0):
    rng = np.random.default_rng(seed)
    pos = carve_rod(N, aspect=aspect)
    N = len(pos)
    noise = np.sqrt(2 * kT * dt)
    print(f"  overdamped Langevin: N={N}, kT={kT}, dt={dt}, steps={steps}, start aspect~{aspect}")
    print(f"    {'step':>6} {'clust':>6} {'aspect':>7} {'kappa^2':>8}")
    traj = []
    for t in range(steps + 1):
        if t % sample == 0:
            cl = largest_cluster(pos)
            asp, k2, _ = shape_anisotropy(pos[cl])
            traj.append((t, len(cl), asp, k2))
            print(f"    {t:6d} {len(cl):6d} {asp:7.2f} {k2:8.3f}")
        _, F, _ = lj_EFV(pos)
        pos += F * dt + noise * rng.standard_normal(pos.shape)
    return np.array(traj)


def main():
    np.set_printoptions(suppress=True)
    t0 = time.time()
    print("liquid_flow.py - the liquid flows: surface tension -> sphere")
    print("=" * 64)
    tr = run()
    a0, k0 = tr[0, 2], tr[0, 3]
    a1, k1 = tr[-1, 2], tr[-1, 3]
    print(f"\n  -> aspect {a0:.2f} -> {a1:.2f},  kappa^2 {k0:.3f} -> {k1:.3f}  (sphere: 1.0, 0)")
    rounded = (k1 < 0.6 * k0) and (a1 < a0 - 0.2)
    print(f"  -> the FLOWING drop rounds toward a sphere: "
          f"{'YES' if rounded else 'PARTIAL'} "
          f"(static minimisation could not; flow can)")
    print(f"  -> mechanism: surface tension gamma (incomplete-shell energy) minimises")
    print(f"     area; mobility (liquid flow) lets it actually reach the round shape.")
    print(f"\n[elapsed {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
