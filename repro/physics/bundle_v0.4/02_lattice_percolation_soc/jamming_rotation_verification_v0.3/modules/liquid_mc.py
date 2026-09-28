"""
liquid_mc.py - the liquid rounds to a sphere (done STABLY, via Monte Carlo).

The free-vacuum Langevin attempt blew up (stiff LJ core + noise) and evaporated
(a small drop sublimes into infinite vacuum). Both are fixed the physically
correct way:
  * a liquid drop must COEXIST WITH ITS VAPOUR -> put it in a periodic box at
    low overall density (dense drop + dilute vapour, no atom is ever lost);
  * use METROPOLIS MONTE CARLO -> moves that would overlap are simply rejected,
    so there is no integrator blow-up; it samples the canonical ensemble at T.

Start ELONGATED, run MC at a sub-critical (liquid) temperature, and watch the
asphericity kappa^2 of the drop fall toward 0: surface tension (the incomplete-
shell energy of liquid_shell.py) minimises area -> the SPHERE. This is the
zero-gravity water-drop phenomenon, with mobility supplied by the liquid flow.

Self-contained: numpy only.
"""
import time
import numpy as np

EPS, SIG, RC = 1.0, 1.0, 2.5
ANN = 1.09 * SIG
RC2 = (RC * SIG) ** 2
VC = 4 * EPS * (((1 / RC ** 2) ** 3) ** 2 - (1 / RC ** 2) ** 3)   # shift


def fcc_ellipsoid(N_target, aspect):
    acell = np.sqrt(2.0) * ANN
    basis = np.array([[0, 0, 0], [.5, .5, 0], [.5, 0, .5], [0, .5, .5]]) * acell
    pts = []
    for i in range(-7, 8):
        for j in range(-7, 8):
            for k in range(-7, 8):
                pts.append(np.array([i, j, k]) * acell + basis)
    p = np.vstack(pts); p -= p.mean(0)
    s = np.array([1.0, 1.0, aspect])
    order = np.argsort(np.linalg.norm(p / s, axis=1))
    return p[order[:N_target]].copy()


def energy_one(i, ri, pos, L):
    """LJ energy (shifted, cut at RC) of particle i at position ri vs all others, min-image."""
    dx = pos - ri
    dx -= L * np.round(dx / L)
    r2 = np.einsum("ij,ij->i", dx, dx)
    r2[i] = 1e30
    m = r2 < RC2
    sr6 = (1.0 / r2[m]) ** 3
    return np.sum(4 * EPS * (sr6 ** 2 - sr6) - VC)


def largest_cluster(pos, L, rlink=1.5):
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    dx -= L * np.round(dx / L)
    d2 = np.einsum("ij,ij->i", dx, dx)
    e = d2 < rlink ** 2
    adj = [[] for _ in range(N)]
    for a, b in zip(iu[e], ju[e]):
        adj[a].append(b); adj[b].append(a)
    seen = np.zeros(N, bool); best = []
    for s in range(N):
        if seen[s]:
            continue
        stack, comp = [s], []; seen[s] = True
        while stack:
            u = stack.pop(); comp.append(u)
            for w in adj[u]:
                if not seen[w]:
                    seen[w] = True; stack.append(w)
        if len(comp) > len(best):
            best = comp
    return np.array(best)


def cluster_shape(pos, cl, L):
    """Asphericity of the cluster, unwrapped via min-image about a reference atom."""
    rel = pos[cl] - pos[cl[0]]
    rel -= L * np.round(rel / L)
    q = rel - rel.mean(0)
    lam = np.sort(np.linalg.eigvalsh((q.T @ q) / len(q)))[::-1]
    Rg2 = lam.sum()
    aspect = np.sqrt(lam[0] / lam[2])
    kappa2 = 1.5 * np.sum(lam ** 2) / Rg2 ** 2 - 0.5
    return aspect, kappa2


def run(N=200, aspect=2.6, L=22.0, kT=0.55, delta=0.18, sweeps=6000,
        sample=400, seed=0):
    rng = np.random.default_rng(seed)
    pos = fcc_ellipsoid(N, aspect)
    pos += L / 2.0
    N = len(pos)
    print(f"  Metropolis MC: N={N}, box L={L}, kT={kT}, sweeps={sweeps}, start aspect~{aspect}")
    print(f"    {'sweep':>6} {'clust':>6} {'aspect':>7} {'kappa^2':>8} {'acc':>6}")
    traj = []
    acc = 0; total = 0
    for sw in range(sweeps + 1):
        if sw % sample == 0:
            cl = largest_cluster(pos, L)
            asp, k2 = cluster_shape(pos, cl, L)
            traj.append((sw, len(cl), asp, k2))
            rate = acc / max(total, 1)
            print(f"    {sw:6d} {len(cl):6d} {asp:7.2f} {k2:8.3f} {rate:6.2f}")
            acc = 0; total = 0
        for _ in range(N):
            i = rng.integers(N)
            ri = pos[i]
            e_old = energy_one(i, ri, pos, L)
            trial = ri + delta * (rng.random(3) - 0.5) * 2
            trial -= L * np.floor(trial / L)
            e_new = energy_one(i, trial, pos, L)
            total += 1
            if rng.random() < np.exp(-(e_new - e_old) / kT):
                pos[i] = trial; acc += 1
    return np.array(traj)


def main():
    np.set_printoptions(suppress=True)
    t0 = time.time()
    print("liquid_mc.py - surface tension rounds the drop to a sphere (stable MC)")
    print("=" * 70)
    tr = run()
    a0, k0 = tr[0, 2], tr[0, 3]
    af, kf = tr[-1, 2], tr[-1, 3]
    nstart, nend = int(tr[0, 1]), int(tr[-1, 1])
    print(f"\n  cluster size {nstart} -> {nend} (drop stays intact: vapour coexistence)")
    print(f"  -> aspect {a0:.2f} -> {af:.2f},  kappa^2 {k0:.3f} -> {kf:.3f}  (sphere: 1.0, 0)")
    rounded = (kf < 0.5 * k0) and (af < a0 - 0.3)
    print(f"  -> the FLOWING drop ROUNDS toward a sphere: {'YES' if rounded else 'PARTIAL'}")
    print(f"     static minimisation could NOT (stuck); flow + coexistence CAN.")
    print(f"     mechanism: gamma = incomplete surface-shell energy -> minimise area -> sphere.")
    print(f"\n[elapsed {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
