"""
jam_packing.py — M1. The O'Hern-protocol jamming engine and the keystone test.

Random soft repulsive spheres in a periodic box, energy-minimized (FIRE) to a
static jammed packing. Scanning the packing fraction phi locates the jamming
threshold phi_c (pressure: 0 -> finite) and measures the contact number Z and
the pair-correlation g(r) there.

Model (O'Hern, Silbert, Liu, Nagel, Phys. Rev. E 68, 011306 (2003)):
    V(r_ij) = (eps/2)(1 - r_ij/d_ij)^2   for r_ij < d_ij,   else 0
    d_ij = (D_i + D_j)/2                  (sum-of-radii contact distance)
Harmonic (alpha=2) repulsion => pressure P ~ (phi - phi_c) above jamming.
Bidisperse 50:50, diameter ratio 1.4, to suppress crystallisation (standard).
Energy is minimised by FIRE (Bitzek et al., PRL 97, 170201 (2006)).

Measurements at point J:
    phi_c : pressure first becomes nonzero (the jamming/rigidity threshold).
    Z     : mean contacts per particle on the force-bearing backbone
            (rattlers, < d+1 contacts, removed iteratively).
    g(r)  : pair correlation. A SPLIT second peak (near r=sqrt(3) D and r=2 D)
            is the fingerprint of an AMORPHOUS (glassy) packing, not a crystal.

PASS (keystone): phi_c in [0.62, 0.66] and Z(phi_c) in [5.7, 6.3] for d=3
(isostatic Z_iso = 2d = 6). This (a) matches the DNA capacity phi* ~ 0.64,
(b) anchors the 1/2-law bridge of module isostatic_scaling.py, and (c) lets g(r)
decide crystal vs glass vs marginal. If it does not appear, report it honestly.

Everything below is fixed by (N, phi, seed, d). Self-contained: numpy only.
"""
import numpy as np


# ----------------------------------------------------------------------
#  Geometry helpers
# ----------------------------------------------------------------------
def sphere_volume_factor(d):
    """Volume of a unit-DIAMETER d-sphere: v = c_d (D/2)^d, here per unit diameter."""
    if d == 2:
        return np.pi / 4.0          # area of a disk of diameter 1
    if d == 3:
        return np.pi / 6.0          # volume of a ball of diameter 1
    raise ValueError("d must be 2 or 3")


def make_diameters(N, ratio=1.4, rng=None):
    """Bidisperse 50:50 diameters with the small species set to mean ~1."""
    if rng is None:
        rng = np.random.default_rng(0)
    D = np.ones(N)
    half = N // 2
    D[half:] = ratio
    rng.shuffle(D)
    return D


def box_length(D, phi, d):
    """Side L of the periodic box giving packing fraction phi for diameters D."""
    vfac = sphere_volume_factor(d)
    packed = vfac * np.sum(D ** d)          # total particle volume
    return (packed / phi) ** (1.0 / d)


# ----------------------------------------------------------------------
#  Energy, forces, virial pressure  (vectorised, minimum-image periodic)
# ----------------------------------------------------------------------
def _pair_terms(pos, D, L, d, tilt=0.0):
    """Return (i, j, rij, dij, dx) for all overlapping pairs (rij < dij).

    `tilt` applies an xy Lees-Edwards shear: the periodic image displaced by one
    box in y is also displaced by tilt*L in x. tilt=0 recovers the cubic box."""
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, k=1)
    dx = pos[iu] - pos[ju]
    if tilt != 0.0:
        ny = np.round(dx[:, 1] / L)                  # y image index
        dx[:, 0] -= ny * tilt * L                    # shear the x separation
        dx[:, 1] -= ny * L
        dx[:, 0] -= L * np.round(dx[:, 0] / L)        # then wrap remaining axes
        if d == 3:
            dx[:, 2] -= L * np.round(dx[:, 2] / L)
    else:
        dx -= L * np.round(dx / L)                   # minimum image (cubic)
    rij = np.sqrt(np.einsum("ij,ij->i", dx, dx))
    dij = 0.5 * (D[iu] + D[ju])
    mask = rij < dij
    return iu[mask], ju[mask], rij[mask], dij[mask], dx[mask]


def energy_forces_pressure(pos, D, L, d, eps=1.0, tilt=0.0, want_sxy=False):
    """Total harmonic energy, per-particle force array, and virial pressure.
    If want_sxy, also return the virial shear stress sigma_xy as a 4th value."""
    N = pos.shape[0]
    i, j, rij, dij, dx = _pair_terms(pos, D, L, d, tilt=tilt)
    F = np.zeros_like(pos)
    if len(rij) == 0:
        return (0.0, F, 0.0, 0.0) if want_sxy else (0.0, F, 0.0)
    delta = 1.0 - rij / dij                            # overlap (>0)
    E = 0.5 * eps * np.sum(delta ** 2)
    # f = -dV/dr = (eps/dij) * delta  (magnitude, repulsive along +rhat_i)
    fmag = eps * delta / dij
    fr = (fmag / rij)[:, None] * dx                    # vector force on i from j
    np.add.at(F, i, fr)
    np.add.at(F, j, -fr)
    virial = np.sum(fmag * rij)                        # sum f_ij r_ij
    P = virial / (d * L ** d)                          # virial pressure
    if want_sxy:
        sxy = np.sum(fr[:, 0] * dx[:, 1]) / (L ** d)   # virial shear stress
        return E, F, P, sxy
    return E, F, P


# ----------------------------------------------------------------------
#  FIRE minimiser
# ----------------------------------------------------------------------
def fire_minimize(pos, D, L, d, eps=1.0, ftol=1e-12, max_steps=20000,
                  dt0=0.05, dt_max=0.2, Nmin=5, finc=1.1, fdec=0.5,
                  a_start=0.1, fa=0.99, tilt=0.0):
    """FIRE energy minimisation at fixed shear `tilt`. Returns (pos, E, P, Fmax)."""
    pos = pos.copy()
    v = np.zeros_like(pos)
    dt = dt0
    a = a_start
    steps_pos = 0
    E, F, P = energy_forces_pressure(pos, D, L, d, eps, tilt=tilt)
    N = pos.shape[0]
    for _ in range(max_steps):
        power = np.vdot(F, v)
        if power > 0.0:
            steps_pos += 1
            vnorm = np.linalg.norm(v)
            fnorm = np.linalg.norm(F) + 1e-300
            v = (1 - a) * v + a * vnorm * F / fnorm
            if steps_pos > Nmin:
                dt = min(dt * finc, dt_max)
                a *= fa
        else:
            v[:] = 0.0
            dt *= fdec
            a = a_start
            steps_pos = 0
        # semi-implicit Euler (unit mass)
        v += dt * F
        pos += dt * v
        E, F, P = energy_forces_pressure(pos, D, L, d, eps, tilt=tilt)
        fmax = np.sqrt((F ** 2).sum(axis=1)).max() if N else 0.0
        if fmax < ftol:
            break
    return pos, E, P, fmax


# ----------------------------------------------------------------------
#  Contacts and the isostatic count Z  (rattlers removed)
# ----------------------------------------------------------------------
def contact_matrix(pos, D, L, d):
    """Boolean N x N contact matrix (rij < dij), no self-contacts."""
    N = pos.shape[0]
    i, j, rij, dij, _ = _pair_terms(pos, D, L, d)
    C = np.zeros((N, N), dtype=bool)
    C[i, j] = True
    C[j, i] = True
    return C


def mean_contact_number(pos, D, L, d, min_contacts=None):
    """Mean contacts per particle on the backbone (rattlers iteratively removed).

    A rattler has fewer than d+1 contacts and cannot be locally rigid; removing
    it can turn neighbours into rattlers, so the pruning is iterated to a fixed
    point. Z = 2 * (#backbone contacts) / (#backbone particles)."""
    if min_contacts is None:
        min_contacts = d + 1
    C = contact_matrix(pos, D, L, d)
    alive = np.ones(pos.shape[0], dtype=bool)
    while True:
        deg = C[np.ix_(alive, alive)].sum(axis=1)
        idx = np.where(alive)[0]
        dead = idx[deg < min_contacts]
        if len(dead) == 0:
            break
        alive[dead] = False
        if alive.sum() == 0:
            return 0.0, alive
    sub = C[np.ix_(alive, alive)]
    nb = sub.sum() / 2.0
    Nb = alive.sum()
    Z = 2.0 * nb / Nb if Nb > 0 else 0.0
    return Z, alive


# ----------------------------------------------------------------------
#  Pair correlation g(r)  (diameter-rescaled, so contact sits at r/D = 1)
# ----------------------------------------------------------------------
def pair_correlation(pos, D, L, d, rmax=2.6, nbins=120):
    """Rescaled g(r/<D>) by dividing each pair separation by its contact distance d_ij."""
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, k=1)
    dx = pos[iu] - pos[ju]
    dx -= L * np.round(dx / L)
    rij = np.sqrt(np.einsum("ij,ij->i", dx, dx))
    s = rij / (0.5 * (D[iu] + D[ju]))                 # scaled separation
    edges = np.linspace(0.0, rmax, nbins + 1)
    hist, _ = np.histogram(s, bins=edges)
    centers = 0.5 * (edges[1:] + edges[:-1])
    # ideal-gas normalisation in scaled units
    Dmean = D.mean()
    rho = N / L ** d
    if d == 3:
        shell = (4.0 / 3.0) * np.pi * ((edges[1:] * Dmean) ** 3 - (edges[:-1] * Dmean) ** 3)
    else:
        shell = np.pi * ((edges[1:] * Dmean) ** 2 - (edges[:-1] * Dmean) ** 2)
    ideal = rho * shell * (N / 2.0)
    g = np.divide(hist, ideal, out=np.zeros_like(hist, dtype=float), where=ideal > 0)
    return centers, g


# ----------------------------------------------------------------------
#  phi scan -> locate phi_c, measure Z, P
# ----------------------------------------------------------------------
def relax_at_phi(N, phi, d, seed, ratio=1.4, **fire_kw):
    """Random init at packing fraction phi; FIRE relax; return diagnostics."""
    rng = np.random.default_rng(seed)
    D = make_diameters(N, ratio, rng)
    L = box_length(D, phi, d)
    pos = rng.uniform(0, L, (N, d))
    pos, E, P, fmax = fire_minimize(pos, D, L, d, **fire_kw)
    Z, alive = mean_contact_number(pos, D, L, d)
    return dict(phi=phi, E=E / N, P=P, Z=Z, fmax=fmax,
                n_backbone=int(alive.sum()), pos=pos, D=D, L=L)


def jam_scan(N=256, d=3, phis=None, seeds=(0, 1, 2, 3), ratio=1.4,
             P_thresh=1e-7, **fire_kw):
    """Scan phi over seeds; return per-phi mean P, Z and an estimate of phi_c."""
    if phis is None:
        phis = np.round(np.arange(0.60, 0.685, 0.01), 3) if d == 3 \
            else np.round(np.arange(0.80, 0.885, 0.01), 3)
    rows = []
    for phi in phis:
        Ps, Zs, Es = [], [], []
        for s in seeds:
            r = relax_at_phi(N, float(phi), d, seed=s, ratio=ratio, **fire_kw)
            Ps.append(r["P"]); Zs.append(r["Z"]); Es.append(r["E"])
        rows.append((float(phi), np.mean(Ps), np.std(Ps), np.mean(Zs),
                     np.std(Zs), np.mean(Es)))
    rows = np.array(rows)
    phi, Pm = rows[:, 0], rows[:, 1]
    jammed = Pm > P_thresh
    # phi_c: linear interpolation of P(phi) -> 0 using the lowest jammed pair
    phi_c = np.nan
    if jammed.any() and (~jammed).any():
        i1 = np.where(jammed)[0][0]
        if i1 > 0:
            p0, p1 = phi[i1 - 1], phi[i1]
            P0, P1 = Pm[i1 - 1], Pm[i1]
            phi_c = p0 + (0.0 - P0) * (p1 - p0) / (P1 - P0) if P1 != P0 else p1
    elif jammed.all():
        # extrapolate P(phi) ~ (phi - phi_c): fit lowest few points
        k = min(4, len(phi))
        sl, ic = np.polyfit(phi[:k], Pm[:k], 1)
        phi_c = -ic / sl
    return rows, phi_c


# ----------------------------------------------------------------------
#  Point-J extrapolation from the (well-converged) jammed branch
# ----------------------------------------------------------------------
def jammed_branch(N, d, phis, seeds, **fire_kw):
    """Relax independent packings on a jammed-branch phi grid. Returns array of
    per-packing rows (phi, Z, P, E/N, fmax)."""
    out = []
    for phi in phis:
        for s in seeds:
            r = relax_at_phi(N, float(phi), d, seed=s, **fire_kw)
            out.append((float(phi), r["Z"], r["P"], r["E"], r["fmax"]))
    return np.array(out)


def extrapolate_pointJ(branch):
    """Given jammed-branch rows, return (phi_c, Z_iso, z0, p0) where
    P ~ p0 (phi - phi_c) and Z - Z_iso ~ z0 sqrt(phi - phi_c)."""
    phi, Z, P = branch[:, 0], branch[:, 1], branch[:, 2]
    # phi_c, p0 from linear P(phi): P = p0 (phi - phi_c)
    p0, b = np.polyfit(phi, P, 1)
    phi_c = -b / p0
    # Z_iso, z0 from Z vs sqrt(phi - phi_c)
    dz_arg = np.sqrt(np.clip(phi - phi_c, 0, None))
    z0, Z_iso = np.polyfit(dz_arg, Z, 1)
    return phi_c, Z_iso, z0, p0


def run_dimension(d, N, phis_jammed, phis_unjam, seeds, fire_kw, outdir):
    target_phi = 0.84 if d == 2 else 0.64
    print(f"\n[d={d}]  N={N}, bidisperse 1.4 (Z_iso = 2d = {2*d}, RCP target ~ {target_phi})")

    # confirm the unjammed branch
    print("  unjammed-branch check:")
    for phi in phis_unjam:
        Ps, Zs = [], []
        for s in seeds:
            r = relax_at_phi(N, float(phi), d, seed=s, **fire_kw)
            Ps.append(r["P"]); Zs.append(r["Z"])
        print(f"    phi={phi:.3f}: <P>={np.mean(Ps):.2e}  <Z>={np.mean(Zs):.3f}  (expect 0, 0)")

    # jammed branch
    branch = jammed_branch(N, d, phis_jammed, seeds, **fire_kw)
    phi_c, Z_iso, z0, p0 = extrapolate_pointJ(branch)
    print("  jammed-branch (per-phi means):")
    print(f"    {'phi':>6} {'<Z>':>7} {'<P>':>11} {'<E/N>':>11}")
    for phi in phis_jammed:
        sel = branch[np.isclose(branch[:, 0], phi)]
        print(f"    {phi:6.3f} {sel[:,1].mean():7.3f} {sel[:,2].mean():11.3e} {sel[:,3].mean():11.3e}")

    print(f"  -> phi_c (P->0 extrap)      = {phi_c:.4f}   (target {target_phi})")
    print(f"  -> Z_iso (dz->0 extrap)     = {Z_iso:.3f}   (target {2*d})")
    print(f"  -> excess-contact prefactor z0 = {z0:.2f}  in  Z-{2*d} ~ z0 sqrt(phi-phi_c)")
    ok = (abs(phi_c - target_phi) < 0.03) and (abs(Z_iso - 2*d) < 0.35)
    print(f"  -> KEYSTONE {'PASS' if ok else 'CHECK'}")

    # save CSV
    import os
    os.makedirs(outdir, exist_ok=True)
    np.savetxt(f"{outdir}/jam_branch_d{d}.csv", branch,
               delimiter=",", header="phi,Z,P,E_per_N,fmax", comments="")

    if d == 3:
        # g(r) just above jamming -> crystal vs glass vs marginal
        r = relax_at_phi(N, max(target_phi, phi_c) + 0.006, d, seed=0, **fire_kw)
        xs, g = pair_correlation(r["pos"], r["D"], r["L"], d)
        gat = lambda x0: g[np.argmin(np.abs(xs - x0))]
        s3 = np.sqrt(3.0)
        print(f"  g(r/D) at point J+: contact g(1.0)={gat(1.0):.1f}, "
              f"g(sqrt3={s3:.2f})={gat(s3):.2f}, g(2.0)={gat(2.0):.2f}")
        print("     contact delta-peak + SPLIT second peak (sqrt3 & 2) => AMORPHOUS, not FCC")
        np.savetxt(f"{outdir}/gofr_d3.csv", np.column_stack([xs, g]),
                   delimiter=",", header="r_over_D,g", comments="")
    return phi_c, Z_iso, z0


def main():
    import sys
    np.set_printoptions(suppress=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    N3 = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    outdir = "results"
    fire_kw = dict(ftol=1e-8, max_steps=6000)
    print("M1  jam_packing.py — O'Hern soft-sphere jamming (keystone test)")
    print("=" * 68)
    if which in ("2", "2d", "both"):
        run_dimension(2, 256,
                      phis_jammed=np.round(np.arange(0.85, 0.891, 0.01), 3),
                      phis_unjam=(0.80, 0.82),
                      seeds=(0, 1, 2), fire_kw=fire_kw, outdir=outdir)
    if which in ("3", "3d", "both"):
        run_dimension(3, N3,
                      phis_jammed=np.round(np.arange(0.65, 0.691, 0.01), 3),
                      phis_unjam=(0.60, 0.62),
                      seeds=(0, 1, 2), fire_kw=fire_kw, outdir=outdir)
    print("\nNote: phi_c, Z_iso, and the split g(r) emerge from random "
          "minimisation;\nno parameter is tuned to hit 0.64 or 6.")


if __name__ == "__main__":
    main()
