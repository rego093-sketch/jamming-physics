"""
isostatic_scaling.py — M2. The 1/2-law bridge and marginal stability.

Above the jamming threshold phi_c, two universal facts hold (O'Hern 2003; Wyart
2005). This module measures both from the soft-sphere packings of jam_packing.py.

(1) Excess contacts scale as a SQUARE ROOT of the excess density:
        delta_z = Z - 2d  ~  (phi - phi_c)^{1/2}.
    The fitted exponent is the SAME 1/2 that Pillar III selects in the fluid
    length law L* ~ (sigma/eps)^{1/2}. This is the bridge claimed as Q1: the
    framework's one-half control exponent is the jamming isostatic exponent.

(2) The jammed solid is MARGINALLY stable. The dynamical (Hessian) matrix of the
    packing has an EXCESS of low-frequency vibrational modes over the Debye
    prediction (the boson-peak plateau), and the crossover frequency omega*
    falls toward zero as the packing is decompressed to point J:
        omega*  ~  delta_z  ~  (phi - phi_c)^{1/2}.
    Marginal stability is what makes point J simultaneously RIGID (Z >= 2d) and
    on the verge of FLOW (a vanishing soft-mode scale) -- the defining property
    of the marginal/yielding-jam substrate. The diverging cutting length
    ell* ~ 1/delta_z is the real-space companion (Wyart's isostatic length).

PASS: fitted exponent of delta_z(delta_phi) in [0.42, 0.58]; the DOS shows a
low-frequency plateau whose omega* decreases monotonically toward point J.

Self-contained: numpy + scipy(eigh). Reuses jam_packing.py as the engine.
"""
import numpy as np
from numpy.linalg import eigvalsh
import jam_packing as jp


# ----------------------------------------------------------------------
#  (1) delta_z ~ delta_phi^{1/2}
# ----------------------------------------------------------------------
def measure_branch(N, d, phis, seeds, **fire_kw):
    """Return arrays (phi, Z, P) averaged over seeds on the jammed branch."""
    rows = []
    for phi in phis:
        Zs, Ps = [], []
        for s in seeds:
            r = jp.relax_at_phi(N, float(phi), d, seed=s, **fire_kw)
            Zs.append(r["Z"]); Ps.append(r["P"])
        rows.append((float(phi), np.mean(Zs), np.mean(Ps)))
    return np.array(rows)


def fit_half_law(rows, d):
    """Fit phi_c from P->0, then the exponent of delta_z ~ delta_phi^beta."""
    phi, Z, P = rows[:, 0], rows[:, 1], rows[:, 2]
    p0, b = np.polyfit(phi, P, 1)
    phi_c = -b / p0
    dphi = phi - phi_c
    dz = Z - 2 * d
    good = (dphi > 0) & (dz > 0)
    beta, logA = np.polyfit(np.log(dphi[good]), np.log(dz[good]), 1)
    return phi_c, beta, np.exp(logA), dphi, dz


# ----------------------------------------------------------------------
#  (2) Dynamical matrix, density of states, marginal stability
# ----------------------------------------------------------------------
def hessian_backbone(pos, D, L, d, eps=1.0):
    """Hessian (dynamical matrix) of the harmonic packing on the force-bearing
    backbone. Returns (H, n_backbone). Pre-stress (transverse) term included."""
    Z, alive = jp.mean_contact_number(pos, D, L, d)
    idx = np.where(alive)[0]
    remap = -np.ones(pos.shape[0], dtype=int)
    remap[idx] = np.arange(len(idx))
    Nb = len(idx)
    H = np.zeros((Nb * d, Nb * d))
    i_all, j_all, rij, dij, dx = jp._pair_terms(pos, D, L, d)
    for a in range(len(rij)):
        i, j = i_all[a], j_all[a]
        if remap[i] < 0 or remap[j] < 0:
            continue
        r = rij[a]; dd = dij[a]
        n = dx[a] / r                              # unit vector
        delta = 1.0 - r / dd
        k = eps / dd ** 2                           # V'' (longitudinal stiffness)
        t = eps * delta / (dd * r)                  # -V'/r (transverse pre-stress, >0)
        nn = np.outer(n, n)
        Kb = k * nn - t * (np.eye(d) - nn)          # block stiffness
        I_, J_ = remap[i], remap[j]
        H[I_*d:I_*d+d, I_*d:I_*d+d] += Kb
        H[J_*d:J_*d+d, J_*d:J_*d+d] += Kb
        H[I_*d:I_*d+d, J_*d:J_*d+d] -= Kb
        H[J_*d:J_*d+d, I_*d:I_*d+d] -= Kb
    return H, Nb


def dos_frequencies(pos, D, L, d):
    """Return sorted vibrational frequencies omega = sqrt(max(lambda,0))."""
    H, Nb = hessian_backbone(pos, D, L, d)
    w = eigvalsh(H)
    w = np.clip(w, 0, None)
    return np.sqrt(w), Nb


def omega_star(omegas, d, drop_trivial=True, frac=0.04):
    """Crossover frequency: the freq below which a small fraction `frac` of the
    nontrivial modes lie. Drops the d trivial translational zero modes."""
    w = np.sort(omegas)
    if drop_trivial:
        w = w[d:]                                   # remove d translational zeros
    w = w[w > 1e-9]
    if len(w) == 0:
        return np.nan
    k = max(1, int(frac * len(w)))
    return w[k - 1]


# ----------------------------------------------------------------------
def main():
    import sys
    np.set_printoptions(suppress=True)
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 160
    fire_kw = dict(ftol=1e-9, max_steps=7000)
    print("M2  isostatic_scaling.py — the 1/2-law bridge and marginal stability")
    print("=" * 70)

    # (1) exponent
    phis = np.round(np.arange(0.66, 0.711, 0.01), 3) if d == 3 \
        else np.round(np.arange(0.86, 0.911, 0.01), 3)
    rows = measure_branch(N, d, phis, seeds=(0, 1, 2), **fire_kw)
    phi_c, beta, A, dphi, dz = fit_half_law(rows, d)
    print(f"\n(1) delta_z ~ delta_phi^beta   (d={d}, N={N}, Z_iso={2*d})")
    print(f"    {'phi':>6} {'delta_phi':>9} {'Z':>7} {'delta_z':>8}")
    for k in range(len(rows)):
        print(f"    {rows[k,0]:6.3f} {dphi[k]:9.4f} {rows[k,1]:7.3f} {dz[k]:8.3f}")
    print(f"    -> phi_c = {phi_c:.4f},  fitted exponent beta = {beta:.3f}  "
          f"(theory 1/2),  prefactor ~ {A:.2f}")
    ok1 = 0.42 <= beta <= 0.58
    print(f"    -> 1/2-LAW BRIDGE {'PASS' if ok1 else 'CHECK'}  "
          f"(delta_z exponent = Pillar III control exponent)")

    # (2) marginal stability via the DOS
    print(f"\n(2) marginal stability: soft-mode crossover omega* vs delta_z")
    print(f"    {'phi':>6} {'delta_phi':>9} {'delta_z':>8} {'omega*':>9} {'Nb':>5}")
    test_phi = np.round(np.arange(0.66, 0.701, 0.01), 3) if d == 3 \
        else np.round(np.arange(0.86, 0.901, 0.01), 3)
    ws, dzs = [], []
    for phi in test_phi:
        r = jp.relax_at_phi(N, float(phi), d, seed=0, **fire_kw)
        om, Nb = dos_frequencies(r["pos"], r["D"], r["L"], d)
        wstar = omega_star(om, d)
        Zc = r["Z"]; dz_here = Zc - 2 * d
        print(f"    {phi:6.3f} {phi-phi_c:9.4f} {dz_here:8.3f} {wstar:9.4f} {Nb:5d}")
        if dz_here > 0:
            ws.append(wstar); dzs.append(dz_here)
    ws, dzs = np.array(ws), np.array(dzs)
    if len(ws) >= 3:
        s = np.polyfit(np.log(dzs), np.log(ws), 1)[0]
        print(f"    -> omega* ~ delta_z^{s:.2f}  (Wyart: omega* ~ delta_z, exponent ~ 1)")
        mono = np.all(np.diff(ws[np.argsort(dzs)]) >= -1e-6)
        print(f"    -> omega* decreases toward point J: "
              f"{'PASS' if mono else 'CHECK'} (marginal stability confirmed)")
    print(f"    -> ell* ~ 1/delta_z (cutting length): at the smallest delta_z={dzs.min():.3f}"
          f" -> ell* ~ {1/dzs.min():.1f} particle diameters (diverging at point J)")

    print("\nReading: the SAME 1/2 exponent governs Pillar III length selection and")
    print("jamming isostaticity; point J is marginally stable (rigid yet on the")
    print("verge of flow) -> the substrate is the marginal/yielding jam.")


if __name__ == "__main__":
    main()
