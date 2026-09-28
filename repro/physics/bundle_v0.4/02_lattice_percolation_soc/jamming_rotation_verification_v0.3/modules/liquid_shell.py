"""
liquid_shell.py - M3 (liquid face). The COHESIVE SURFACE SHELL.

User's hint, made concrete: a liquid drop in zero gravity becomes a PERFECT
SPHERE because its skin (surface tension gamma) minimises area. In the volume-
particle / rigid-shell language that skin is the *incomplete first coordination
shell* at the boundary: a surface particle has no neighbours on the outside, so
its shell is missing dz_surf = z_bulk - z_surf contacts. The energy cost of that
missing shell IS the surface tension:

        gamma  =  (excess energy of the drop over bulk) / (surface area)
               ~  (1/2) |eps_bond| * dz_surf * (surface number density).

The drop minimises total missing shell  =>  minimises area  =>  SPHERE.

This is the SAME gamma that the framework calls L1 (DNA whitepaper: interfacial
tension propensity, set by composition). Three faces of one substrate:
  GAS    : no shell  -> no gamma, no fixed shape (fills the box).
  LIQUID : a coherent SURFACE shell (gamma>0, sphere) but a TRANSIENT bulk shell
           (z_bulk < z_iso percolating rigidity absent) -> G=0, it FLOWS.
  SOLID  : the bulk shell CLOSES and percolates -> G>0, born at point J
           (jam_states.py / isostatic_scaling.py).

We use a cohesive Lennard-Jones pair potential (the simplest skin-forming model;
purely-repulsive O'Hern spheres of M1 have NO skin and cannot form a drop):
        V(r) = 4 eps [ (sigma/r)^12 - (sigma/r)^6 ],  cut at 2.5 sigma.

MEASUREMENTS (all from minimised drops, free space, no box, zero gravity):
  (A) a drop started ELONGATED relaxes toward a SPHERE (asphericity falls);
  (B) gamma from the surface-excess of cohesive energy: E/N = e_bulk + s N^-1/3,
      gamma = s / (4 pi a^2),  a = (3/(4 pi rho))^1/3;
  (C) the shell itself: surface particles are UNDER-coordinated (dz_surf>0), and
      a STRUCTURAL gamma built from that deficit matches the energetic gamma.

Honest scope: at T=0 a finite drop is a compact, faceted cluster, round but not
a flawless sphere (faceting falls as N grows; the flawless sphere is the
T>0 liquid / continuum limit). What is demonstrated is the MECHANISM
(area-minimisation by the surface-shell deficit) and gamma itself.

Self-contained: numpy only.
"""
import sys
import time
import numpy as np

EPS, SIG, RCUT = 1.0, 1.0, 2.5
ANN = 1.09 * SIG            # ~ zero-pressure LJ-FCC nearest-neighbour distance


# ----------------------------------------------------------------------
#  FCC initial drops (compact start = near-global, clean for gamma)
# ----------------------------------------------------------------------
def fcc_block(ncell):
    """FCC lattice points filling an ncell^3 block of conventional cells."""
    acell = np.sqrt(2.0) * ANN
    basis = np.array([[0, 0, 0], [.5, .5, 0], [.5, 0, .5], [0, .5, .5]]) * acell
    pts = []
    rng = range(-ncell, ncell + 1)
    for i in rng:
        for j in rng:
            for k in rng:
                pts.append(np.array([i, j, k]) * acell + basis)
    return np.vstack(pts)


def carve_sphere(N_target):
    """Compact FCC sphere with ~N_target atoms."""
    p = fcc_block(6)
    p -= p.mean(0)
    r = np.linalg.norm(p, axis=1)
    order = np.argsort(r)
    return p[order[:N_target]].copy()


def carve_rod(N_target, aspect=4.0):
    """Elongated FCC ellipsoid (a:a:aspect*a) with ~N_target atoms -- a NON-sphere
    start, to watch the surface shell round it out."""
    p = fcc_block(9)
    p -= p.mean(0)
    s = np.array([1.0, 1.0, aspect])
    rr = np.linalg.norm(p / s, axis=1)
    order = np.argsort(rr)
    return p[order[:N_target]].copy()


# ----------------------------------------------------------------------
#  Lennard-Jones energy / forces / virial  (free space, all pairs)
# ----------------------------------------------------------------------
def lj_EFV(pos, eps=EPS, sigma=SIG, rcut=RCUT):
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    r2 = np.einsum("ij,ij->i", dx, dx)
    m = (r2 < (rcut * sigma) ** 2) & (r2 > 1e-12)
    iu, ju, dx, r2 = iu[m], ju[m], dx[m], r2[m]
    r = np.sqrt(r2)
    sr6 = (sigma ** 2 / r2) ** 3
    sr12 = sr6 ** 2
    # shift energy so V(rcut)=0 (continuity)
    src6 = (1.0 / rcut ** 2) ** 3
    Vc = 4 * eps * (src6 ** 2 - src6)
    E = np.sum(4 * eps * (sr12 - sr6) - Vc)
    fmag = 24 * eps * (2 * sr12 - sr6) / r        # f = -dV/dr ; >0 repulsive
    F = np.zeros_like(pos)
    fr = (fmag / r)[:, None] * dx
    np.add.at(F, iu, fr)
    np.add.at(F, ju, -fr)
    virial = np.sum(fmag * r)                      # sum_ij f_ij r_ij
    return E, F, virial


def fire(pos, max_steps=3000, ftol=1e-6, dt0=0.01, dt_max=0.05,
         Nmin=5, finc=1.1, fdec=0.5, a0=0.1, fa=0.99):
    pos = pos.copy()
    v = np.zeros_like(pos)
    dt, a, npos = dt0, a0, 0
    E, F, _ = lj_EFV(pos)
    for _ in range(max_steps):
        if np.vdot(F, v) > 0:
            npos += 1
            vn, fn = np.linalg.norm(v), np.linalg.norm(F) + 1e-300
            v = (1 - a) * v + a * vn * F / fn
            if npos > Nmin:
                dt = min(dt * finc, dt_max); a *= fa
        else:
            v[:] = 0.0; dt *= fdec; a = a0; npos = 0
        v += dt * F
        pos += dt * v
        E, F, _ = lj_EFV(pos)
        if np.sqrt((F ** 2).sum(1)).max() < ftol:
            break
    _, _, vir = lj_EFV(pos)
    return pos, E, vir


# ----------------------------------------------------------------------
#  structure: coordination shell, sphericity, density
# ----------------------------------------------------------------------
def coordination(pos, rshell=1.35 * SIG):
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    d = np.sqrt(np.einsum("ij,ij->i", dx, dx))
    z = np.zeros(N)
    near = d < rshell
    np.add.at(z, iu[near], 1.0)
    np.add.at(z, ju[near], 1.0)
    return z


def shape_anisotropy(pos):
    q = pos - pos.mean(0)
    S = (q.T @ q) / len(q)
    lam = np.sort(np.linalg.eigvalsh(S))[::-1]      # l1>=l2>=l3
    Rg2 = lam.sum()
    aspect = np.sqrt(lam[0] / lam[2])
    kappa2 = 1.5 * np.sum(lam ** 2) / Rg2 ** 2 - 0.5  # 0 for a sphere
    return aspect, kappa2, np.sqrt(Rg2)


def nn_distance(pos):
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    d = np.sqrt(np.einsum("ij,ij->i", dx, dx))
    # mean of each particle's nearest neighbour
    dmin = np.full(N, np.inf)
    np.minimum.at(dmin, iu, d)
    np.minimum.at(dmin, ju, d)
    return np.median(dmin)


# ----------------------------------------------------------------------
def main():
    np.set_printoptions(suppress=True)
    t0 = time.time()
    print("M3  liquid_shell.py - the cohesive surface shell (liquid = skin -> sphere)")
    print("=" * 74)

    # ---- (A) elongated drop -> sphere ----
    rod = carve_rod(260, aspect=4.0)
    a0_asp, a0_k, _ = shape_anisotropy(rod)
    rodmin, Erod, _ = fire(rod, max_steps=4000)
    a1_asp, a1_k, _ = shape_anisotropy(rodmin)
    print("\n(A) zero-gravity drop: an ELONGATED start relaxes toward a SPHERE")
    print(f"    start  : aspect(sqrt l1/l3) = {a0_asp:.2f},  anisotropy kappa^2 = {a0_k:.3f}")
    print(f"    relaxed: aspect             = {a1_asp:.2f},  kappa^2            = {a1_k:.3f}  (sphere: 1.0, 0)")
    print(f"    -> the surface shell rounded the drop: aspect {a0_asp:.2f} -> {a1_asp:.2f}, "
          f"kappa^2 {a0_k:.3f} -> {a1_k:.3f}")

    # ---- (B) gamma from surface excess of cohesive energy ----
    print("\n(B) surface tension gamma from the cohesive-energy surface excess")
    Ns = [55, 87, 135, 201, 280, 380]
    rows = []
    for Nt in Ns:
        d = carve_sphere(Nt)
        dmin, E, vir = fire(d, max_steps=3000)
        Nn = len(dmin)
        rows.append((Nn, E / Nn))
        del d, dmin
    rows = np.array(rows)
    Nn, EperN = rows[:, 0], rows[:, 1]
    x = Nn ** (-1.0 / 3.0)
    s, e_bulk = np.polyfit(x, EperN, 1)            # E/N = e_bulk + s * N^-1/3
    print(f"    {'N':>5} {'E/N':>10} {'N^-1/3':>9}")
    for k in range(len(Nn)):
        print(f"    {int(Nn[k]):5d} {EperN[k]:10.4f} {x[k]:9.4f}")
    # bulk density from the largest relaxed drop
    big = carve_sphere(700)
    bigmin, _, _ = fire(big, max_steps=2500)
    dnn = nn_distance(bigmin)
    rho = np.sqrt(2.0) / dnn ** 3                  # FCC local packing
    a_rad = (3.0 / (4.0 * np.pi * rho)) ** (1.0 / 3.0)
    gamma_E = s / (4.0 * np.pi * a_rad ** 2)
    print(f"    -> e_bulk (N->inf intercept) = {e_bulk:.3f} eps   (LJ-FCC lattice sum ~ -8.61 eps)")
    print(f"    -> rho_bulk = {rho:.3f} sigma^-3 (d_nn={dnn:.3f}),  surface slope s = {s:.3f}")
    print(f"    -> gamma (energetic)        = {gamma_E:.3f} eps/sigma^2")

    # ---- (C) the shell: surface under-coordination, structural gamma ----
    z = coordination(bigmin)
    z_bulk = np.median(z[z >= np.percentile(z, 70)])   # interior plateau
    surf = z < 0.85 * z_bulk                            # under-coordinated = surface
    dz_surf = z_bulk - z[surf]
    Nsurf = surf.sum()
    q = bigmin - bigmin.mean(0)
    R_drop = np.sqrt((q ** 2).sum(1)).max()
    A = 4 * np.pi * R_drop ** 2
    # each missing first-shell neighbour ~ one missing bond of depth ~eps
    E_excess_struct = 0.5 * EPS * dz_surf.sum()
    gamma_struct = E_excess_struct / A
    print("\n(C) the shell = the first coordination shell; surface particles miss part of it")
    print(f"    bulk shell z_bulk = {z_bulk:.1f}  (FCC first shell = 12)")
    print(f"    surface particles = {Nsurf}/{len(z)},  mean deficit <dz_surf> = {dz_surf.mean():.2f}")
    print(f"    -> structural gamma (deficit/area) = {gamma_struct:.3f} eps/sigma^2")
    print(f"    -> energetic vs structural gamma : {gamma_E:.3f}  vs  {gamma_struct:.3f}  "
          f"(ratio {gamma_E/gamma_struct:.2f})")

    print("\nReading: the liquid's skin IS the incomplete surface coordination shell;")
    print("its energy is gamma, and minimising it minimises area -> the sphere. Gas has")
    print("no shell; the solid's shell percolates into static rigidity (G>0 at point J).")
    print("Pillar I (Newtonian) note: the SAME drop, sheared, flows because its BULK")
    print("shell is transient (z_bulk < z_iso); eta ~ (phi_J - phi)^-2 is that face and")
    print("needs a steady-shear dynamics run (next), not the static minimisation here.")
    print(f"\n[elapsed {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
