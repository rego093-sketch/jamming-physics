"""
liquid_tension.py - why a liquid holds together in ZERO GRAVITY: internal tension.

User's point: constant-pressure confinement is really GRAVITY -- an external push
holding a body together against the outward drive of rotation/temperature. But a
liquid exists in ZERO GRAVITY (the floating drop) with NO external pressure. So
what holds it is an INTERNAL attractive TENSION (cohesion) = the COHESIVE/RIGID
SHELL: surface particles are under-coordinated (missing outward neighbours), and
the drive to COMPLETE the coordination shell pulls the surface inward. That
inward pull is the surface tension gamma, and it is GEOMETRIC:
gamma = surface coordination deficit (shown in liquid_shell.py).

So we remove the box AND the external pressure entirely (= zero gravity) and let
a cohesive cluster hold ITSELF together by its own tension. Sweeping temperature
(rotation) we watch the balance:
  low  T : tension wins   -> frozen SOLID drop (intact, no internal motion);
  mid  T : balance        -> self-bound LIQUID drop (intact, FLOWS) -- the zero-g liquid;
  high T : agitation wins -> tension overcome -> EVAPORATION -> GAS.

Metropolis MC in FREE SPACE (stable; no box, no external pressure). OBSERVED:
drop integrity (largest cluster), internal motion (COM-subtracted MSD), size
(radius of gyration), and the surface coordination deficit (the shell = tension).

Self-contained: numpy only.
"""
import time
import numpy as np

RC = 2.5
RC2 = RC ** 2
VC = 4.0 * (((1.0 / RC ** 2) ** 3) ** 2 - (1.0 / RC ** 2) ** 3)
ANN = 1.09


def carve_sphere(N_target):
    acell = np.sqrt(2.0) * ANN
    basis = np.array([[0, 0, 0], [.5, .5, 0], [.5, 0, .5], [0, .5, .5]]) * acell
    pts = [np.array([i, j, k]) * acell + basis
           for i in range(-6, 7) for j in range(-6, 7) for k in range(-6, 7)]
    p = np.vstack(pts); p -= p.mean(0)
    order = np.argsort(np.linalg.norm(p, axis=1))
    return p[order[:N_target]].copy()


def e_one(i, ri, pos):
    dx = pos - ri
    r2 = np.einsum("ij,ij->i", dx, dx)
    r2[i] = 1e30
    m = r2 < RC2
    sr6 = (1.0 / r2[m]) ** 3
    return np.sum(4.0 * (sr6 ** 2 - sr6) - VC)


def largest_cluster(pos, rlink=1.5):
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    d2 = np.einsum("ij,ij->i", dx, dx)
    e = d2 < rlink ** 2
    adj = [[] for _ in range(N)]
    for a, b in zip(iu[e], ju[e]):
        adj[a].append(b); adj[b].append(a)
    seen = np.zeros(N, bool); best = []
    for s in range(N):
        if seen[s]:
            continue
        st, comp = [s], []; seen[s] = True
        while st:
            u = st.pop(); comp.append(u)
            for w in adj[u]:
                if not seen[w]:
                    seen[w] = True; st.append(w)
        if len(comp) > len(best):
            best = comp
    return np.array(best)


def coordination(pos, idx, rcut=1.35):
    sub = pos[idx]
    n = len(idx)
    iu, ju = np.triu_indices(n, 1)
    dx = sub[iu] - sub[ju]
    d2 = np.einsum("ij,ij->i", dx, dx)
    near = d2 < rcut ** 2
    z = np.zeros(n)
    np.add.at(z, iu[near], 1.0)
    np.add.at(z, ju[near], 1.0)
    return z


def mc_sweeps(pos, kT, n, delta, rng):
    N = pos.shape[0]
    for _ in range(n):
        for _ in range(N):
            i = rng.integers(N); ri = pos[i]
            e0 = e_one(i, ri, pos)
            step = delta * (rng.random(3) - 0.5) * 2.0
            e1 = e_one(i, ri + step, pos)
            if rng.random() < np.exp(-(e1 - e0) / kT):
                pos[i] = ri + step


def main():
    np.set_printoptions(suppress=True)
    t0 = time.time()
    print("liquid_tension.py - zero-gravity drop held by internal tension (the shell)")
    print("=" * 74)
    print("\nNO box, NO external pressure = ZERO GRAVITY. The drop is held only by its")
    print("own cohesion (the shell). Heat it and watch tension vs agitation:")
    print(f"    {'kT':>5} {'drop(N_clu)':>11} {'MSD_int':>9} {'Rg':>6} {'z_bulk':>7} {'<dz_surf>':>10} {'state':>10}")

    rng = np.random.default_rng(0)
    N0 = 220
    pos = carve_sphere(N0)
    for kT in [0.2, 0.4, 0.6, 0.8, 1.0, 1.3]:
        mc_sweeps(pos, kT, 350, 0.10, rng)             # equilibrate
        cl = largest_cluster(pos)                       # the drop at start of window
        com0 = pos[cl].mean(0)
        ref = pos[cl] - com0
        mc_sweeps(pos, kT, 300, 0.10, rng)             # measurement window
        cl_now = largest_cluster(pos)
        # internal MSD over the originally-tracked drop atoms, COM-subtracted
        com1 = pos[cl].mean(0)
        msd_int = float(np.mean(np.sum(((pos[cl] - com1) - ref) ** 2, axis=1)))
        Rg = float(np.sqrt(np.mean(np.sum((pos[cl_now] - pos[cl_now].mean(0)) ** 2, axis=1))))
        z = coordination(pos, cl_now)
        zb = float(np.median(z[z >= np.percentile(z, 70)])) if len(z) else 0.0
        surf = z < 0.85 * zb
        dz = float((zb - z[surf]).mean()) if surf.any() else 0.0
        frac = len(cl_now) / N0
        state = ("solid" if msd_int < 0.2 else "liquid") if frac > 0.85 else "evaporating/gas"
        print(f"    {kT:5.2f} {len(cl_now):11d} {msd_int:9.3f} {Rg:6.2f} {zb:7.1f} {dz:10.2f} {state:>10}")

    print("\nReading: with NO gravity and NO external pressure, the drop still holds together")
    print("at low/mid T -- proof the binder is INTERNAL tension, not gravity. That tension is")
    print("the shell: surface atoms carry a coordination deficit <dz_surf> (the missing")
    print("outward neighbours), and the pull to close it = surface tension gamma (geometric).")
    print("Low T: tension wins -> solid drop. Mid T: balance -> LIQUID drop that flows")
    print("(MSD_int climbs, drop intact) = the zero-gravity liquid. High T: agitation beats")
    print("the tension -> the drop evaporates (N_clu falls, Rg grows) -> GAS.")
    print(f"\n[elapsed {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
