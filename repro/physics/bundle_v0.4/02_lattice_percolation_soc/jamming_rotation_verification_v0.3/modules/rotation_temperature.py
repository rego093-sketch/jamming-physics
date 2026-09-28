"""
rotation_temperature.py - rotation = temperature: agitation -> separation (free
volume) -> flow.  solid -> liquid -> gas, along an ISOBAR (constant pressure).

User's principle:
  * ROTATION IS TEMPERATURE -- thermal agitation is the rotational jiggling/
    rolling of the caging particles (the cage-rolling mode that opened the
    tetrahedral cage at theta_c ~ 30 deg in rotation_states.py).
  * raise temperature (rotation) -> SEPARATION (이격): at constant pressure the
    substrate EXPANDS, the nearest-neighbour gap grows -> FREE VOLUME -> the
    cages roll open -> the substrate FLOWS.

KEY (honest) point learned: this needs CONSTANT PRESSURE. At fixed volume,
heating does NOT grow the gap (the box can't expand). So we run constant-P
(NPT) Monte Carlo along an isobar and watch separation appear as T rises.

We OBSERVE the motion: equilibrate at (T,P) [the density relaxes], then freeze
the box and measure mean-square displacement MSD (caged plateau vs diffusion),
together with density rho, the gap (이격), and contact number Z (cages).

Self-contained: numpy only.
"""
import time
import numpy as np

RC = 2.5
RC2 = RC ** 2
VC = 4.0 * (((1.0 / RC ** 2) ** 3) ** 2 - (1.0 / RC ** 2) ** 3)


def fcc_box(ncell, rho):
    N = 4 * ncell ** 3
    L = (N / rho) ** (1.0 / 3.0)
    a = L / ncell
    basis = np.array([[0, 0, 0], [.5, .5, 0], [.5, 0, .5], [0, .5, .5]]) * a
    pts = [np.array([i, j, k]) * a + basis
           for i in range(ncell) for j in range(ncell) for k in range(ncell)]
    return (np.vstack(pts) % L), L, N


def energy_one(i, ri, pos, L):
    dx = pos - ri
    dx -= L * np.round(dx / L)
    r2 = np.einsum("ij,ij->i", dx, dx)
    r2[i] = 1e30
    m = r2 < RC2
    sr6 = (1.0 / r2[m]) ** 3
    return np.sum(4.0 * (sr6 ** 2 - sr6) - VC)


def total_energy(pos, L):
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    dx -= L * np.round(dx / L)
    r2 = np.einsum("ij,ij->i", dx, dx)
    m = r2 < RC2
    sr6 = (1.0 / r2[m]) ** 3
    return np.sum(4.0 * (sr6 ** 2 - sr6) - VC)


def nn_gap(pos, L):
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    dx -= L * np.round(dx / L)
    d = np.sqrt(np.einsum("ij,ij->i", dx, dx))
    dmin = np.full(N, np.inf)
    np.minimum.at(dmin, iu, d)
    np.minimum.at(dmin, ju, d)
    return float(np.median(dmin) - 1.0)


def coordination(pos, L, rcut=1.3):
    N = pos.shape[0]
    iu, ju = np.triu_indices(N, 1)
    dx = pos[iu] - pos[ju]
    dx -= L * np.round(dx / L)
    d2 = np.einsum("ij,ij->i", dx, dx)
    return 2.0 * np.sum(d2 < rcut ** 2) / N


def nvt_sweeps(pos, posu, L, kT, n, delta, rng):
    N = pos.shape[0]
    for _ in range(n):
        for _ in range(N):
            i = rng.integers(N); ri = pos[i]
            e0 = energy_one(i, ri, pos, L)
            step = delta * (rng.random(3) - 0.5) * 2.0
            e1 = energy_one(i, (ri + step) % L, pos, L)
            if rng.random() < np.exp(-(e1 - e0) / kT):
                pos[i] = (ri + step) % L; posu[i] += step


def npt_equilibrate(pos, L, kT, P, n, delta, dlnV, rng):
    """Constant-pressure MC: particle moves + volume moves. Returns (pos, L)."""
    N = pos.shape[0]
    U = total_energy(pos, L)
    dummy = pos.copy()
    for _ in range(n):
        nvt_sweeps(pos, dummy, L, kT, 1, delta, rng)
        U = total_energy(pos, L)
        V = L ** 3
        lnVn = np.log(V) + dlnV * (rng.random() - 0.5)
        Vn = np.exp(lnVn); scale = (Vn / V) ** (1.0 / 3.0)
        Ln = L * scale; posn = pos * scale
        Un = total_energy(posn, Ln)
        arg = (Un - U) + P * (Vn - V) - N * kT * np.log(Vn / V)
        if rng.random() < np.exp(-arg / kT):
            pos = posn; L = Ln
    return pos, L


def main():
    np.set_printoptions(suppress=True)
    t0 = time.time()
    print("rotation_temperature.py - rotation=temperature -> separation -> flow (isobar)")
    print("=" * 74)

    # (1) geometry anchor
    print("\n(1) geometry: a CONTACTING tetrahedral cage has ZERO free room")
    print("    every centre move u has some u.n_i>0 -> overlaps neighbour i -> 0 free")
    print("    volume -> SOLID. Only rotation (rolling contacts, theta_c~30) opens a gap; T does that.")

    # (2) constant-pressure isobar: heat -> expand -> gap (이격) -> flow
    P = 0.5
    rng = np.random.default_rng(0)
    pos, L, N = fcc_box(4, rho=1.00)
    print(f"\n(2) heat at CONSTANT PRESSURE (P={P}, N={N}): does separation appear?")
    print(f"    {'kT':>5} {'rho':>6} {'gap(이격)':>10} {'Z':>6} {'MSD@mid':>9} {'MSD@end':>9} {'state':>8}")
    for kT in [0.2, 0.5, 0.8, 1.1, 1.5, 2.0]:
        pos, L = npt_equilibrate(pos, L, kT, P, 220, 0.08, 0.008, rng)
        # freeze the box, measure clean diffusion + structure
        posu = pos.copy(); ref = posu.copy()
        nvt_sweeps(pos, posu, L, kT, 200, 0.08, rng)
        msd_mid = float(np.mean(np.sum((posu - ref) ** 2, axis=1)))
        nvt_sweeps(pos, posu, L, kT, 200, 0.08, rng)
        msd_end = float(np.mean(np.sum((posu - ref) ** 2, axis=1)))
        rho = N / L ** 3
        gap = nn_gap(pos, L); Z = coordination(pos, L)
        state = "solid" if msd_end < 0.15 else ("liquid" if msd_end < 5 else "gas/fluid")
        print(f"    {kT:5.2f} {rho:6.3f} {gap:10.3f} {Z:6.2f} {msd_mid:9.3f} {msd_end:9.3f} {state:>8}")

    # (3) gas limit (dilute + hot)
    rng2 = np.random.default_rng(1)
    posg, Lg, Ng = fcc_box(4, rho=0.05)
    posug = posg.copy(); refg = posug.copy()
    nvt_sweeps(posg, posug, Lg, 2.0, 200, 0.30, rng2)
    msd_gas = float(np.mean(np.sum((posug - refg) ** 2, axis=1)))
    print(f"\n(3) gas limit (rho=0.05, kT=2.0): Z={coordination(posg, Lg):.2f}, "
          f"gap={nn_gap(posg, Lg):.2f}, MSD={msd_gas:.1f}  -> no cage, free flight: GAS.")

    print("\nReading: rotation = temperature. At CONSTANT PRESSURE, heating (rotating) the")
    print("substrate EXPANDS it: density falls, the nearest-neighbour GAP (이격) grows ->")
    print("free volume -> cages roll open (Z falls) -> particles DIFFUSE (MSD climbs):")
    print("solid -> liquid -> gas. The switch is geometric: flow begins once the agitation")
    print("supplies the gap a cage-rolling rearrangement (theta_c) needs.")
    print(f"\n[elapsed {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
