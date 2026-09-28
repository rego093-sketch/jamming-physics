#!/usr/bin/env python3
"""
ch_spin_locking.py  --  Re-implementation (2026-09-28) of the lost Chapter 5 script
                        "Spin/tidal-locking dichotomy (12/12): tau_lock vs age".

CLAIM TESTED  (docs/cosmology/05-axial-spin-tidal-locking-inflow/, 16-open-problems-gathered/,
               axh ledger, axj log #12)
------------
The despinning time implied by the inflow-gradient tidal torque (page Eq. taulock),
    tau_lock ~ (2 alpha/3) * M * omega_i * Q * a^6 / (k2 * G * Mp^2 * R^3),   I = alpha M R^2,
compared with the age of the Solar System (4.5 Gyr), with ONE fiducial (alpha, Q, k2, omega_i)
and no per-body tuning, sorts twelve test bodies correctly:
    locked / despun : Moon; Io, Europa, Ganymede; Titan; Charon; Phobos; Mercury (3:2)
    free            : Earth, Mars, and the giants.
The page lists the giants without naming them; with 8 locked + Earth + Mars the count of 12
requires two giants, taken here as Jupiter and Saturn.  Uranus, Neptune, Callisto and Venus
are reported as an out-of-sample extension (not scored in the 12).
G*M enters only as kappa*Q (Ch 3), so G*Mp is used directly -- no framework-specific number
enters: at the level of predictions this is degenerate with conventional tidal theory.

INPUTS  (textbook; no fitting)
------
* Single fiducial, fixed BEFORE running (pre-registered here, never adjusted):
    alpha = 0.4   (homogeneous sphere, I = 0.4 M R^2)
    Q     = 100   (the standard rocky-body tidal quality factor, e.g. Gladman et al. 1996,
                   Icarus 122, 166; Murray & Dermott 1999 ch. 4)
    k2    = 0.3   (Earth's measured Love number; used for every body)
    P_i   = 12 h  (initial spin period, as in Gladman et al. 1996)  -> omega_i = 2 pi / P_i
* Masses, radii, semi-major axes: NASA/JPL planetary & satellite fact sheets (mean values).
* Age = 4.5 Gyr (page).  G = 6.674e-11 (only the product G*M enters).
* For a planet with a satellite, tau is taken for EVERY listed primary and the shortest is used
  (Earth: Sun and Moon).

ALGORITHM
---------
(1) evaluate tau_lock for every body with the fiducial;  (2) classify despun if tau < age;
(3) compare with the observed state; (4) robustness: repeat over a grid
    Q in {10,30,100,300,1000} x k2 in {0.01,0.03,0.1,0.3,1} x P_i in {6,12,24} h x alpha in {0.33,0.4}
    and report the fraction of grid points giving 12/12 and which bodies fail where.
EXPECTED OUTPUT (page): 12/12 bodies sorted correctly; Mercury tau < age (despun into 3:2).
DEPENDENCIES: numpy (matplotlib optional). Deterministic.
"""
import numpy as np

G = 6.674e-11
YR = 3.15576e7
AGE = 4.5e9*YR

# primaries: mass [kg]
PRIM = {"Sun": 1.98847e30, "Earth": 5.9722e24, "Mars": 6.4171e23, "Jupiter": 1.89813e27,
        "Saturn": 5.6832e26, "Pluto": 1.303e22, "Moon": 7.342e22}

# name, M [kg], R [m], [(primary, a [m]) ...], observed_locked (True/False), note
BODIES = [
    ("Moon",     7.342e22,  1.7374e6, [("Earth", 3.844e8)],     True,  "1:1"),
    ("Io",       8.932e22,  1.8216e6, [("Jupiter", 4.217e8)],   True,  "1:1"),
    ("Europa",   4.800e22,  1.5608e6, [("Jupiter", 6.709e8)],   True,  "1:1"),
    ("Ganymede", 1.4819e23, 2.6341e6, [("Jupiter", 1.0704e9)],  True,  "1:1"),
    ("Titan",    1.3452e23, 2.5747e6, [("Saturn", 1.22187e9)],  True,  "1:1"),
    ("Charon",   1.586e21,  6.06e5,   [("Pluto", 1.9596e7)],    True,  "1:1 (mutual)"),
    ("Phobos",   1.0659e16, 1.108e4,  [("Mars", 9.376e6)],      True,  "1:1"),
    ("Mercury",  3.3011e23, 2.4397e6, [("Sun", 5.7909e10)],     True,  "despun, 3:2"),
    ("Earth",    5.9722e24, 6.371e6,  [("Sun", 1.49598e11), ("Moon", 3.844e8)], False, "free, 1 d"),
    ("Mars",     6.4171e23, 3.3895e6, [("Sun", 2.27939e11)],    False, "free, 1.03 d"),
    ("Jupiter",  1.89813e27, 6.9911e7, [("Sun", 7.78570e11)],   False, "free, 0.41 d"),
    ("Saturn",   5.6832e26, 5.8232e7, [("Sun", 1.43353e12)],    False, "free, 0.44 d"),
]
EXTENSION = [
    ("Callisto", 1.0759e23, 2.4103e6, [("Jupiter", 1.8827e9)],  True,  "1:1"),
    ("Uranus",   8.6811e25, 2.5362e7, [("Sun", 2.87246e12)],    False, "free, 0.72 d"),
    ("Neptune",  1.02409e26, 2.4622e7, [("Sun", 4.49506e12)],   False, "free, 0.67 d"),
    ("Venus",    4.8675e24, 6.0518e6, [("Sun", 1.08210e11)],    None,  "243 d retrograde (anomalous)"),
]
FIDUCIAL = dict(alpha=0.4, Q=100.0, k2=0.3, P_i_h=12.0)


def tau_lock(M, R, prims, alpha, Q, k2, P_i_h):
    w = 2*np.pi/(P_i_h*3600.0)
    taus = [(2*alpha/3)*M*w*Q*a**6/(k2*G*PRIM[p]**2*R**3) for p, a in prims]
    k = int(np.argmin(taus))
    return taus[k], prims[k][0]


def classify(bodies, **par):
    out = []
    for nm, M, R, prims, obs, note in bodies:
        t, p = tau_lock(M, R, prims, **par)
        out.append((nm, t, p, t < AGE, obs, note))
    return out


if __name__ == "__main__":
    print("=" * 92)
    print(" ch_spin_locking.py -- locked-vs-free dichotomy from tau_lock (inflow-gradient tide) vs 4.5 Gyr")
    print("=" * 92)
    print(f" single fiducial (pre-registered): alpha={FIDUCIAL['alpha']}, Q={FIDUCIAL['Q']:.0f}, "
          f"k2={FIDUCIAL['k2']}, P_i={FIDUCIAL['P_i_h']:.0f} h\n")
    rows = classify(BODIES, **FIDUCIAL)
    print(f"{'body':9s} {'primary':8s} {'tau_lock [yr]':>14} {'log10(tau/age)':>15} {'predicted':>10} {'observed':>22}  ok")
    nok = 0
    for nm, t, p, pred, obs, note in rows:
        ok = (pred == obs); nok += ok
        print(f"{nm:9s} {p:8s} {t/YR:14.3e} {np.log10(t/AGE):15.2f} {'despun' if pred else 'free':>10} "
              f"{note:>22}  {'OK' if ok else 'MISS'}")
    print(f"\n  => {nok}/{len(rows)} sorted correctly with the single fiducial.")
    margins = np.array([abs(np.log10(t/AGE)) for _, t, _, _, _, _ in rows])
    j = int(margins.argmin())
    print(f"  smallest margin: {rows[j][0]} at |log10(tau/age)| = {margins[j]:.2f} dex")

    print("\n  out-of-sample extension (not in the 12):")
    for nm, t, p, pred, obs, note in classify(EXTENSION, **FIDUCIAL):
        verdict = "n/a" if obs is None else ("OK" if pred == obs else "MISS")
        print(f"   {nm:9s} {p:8s} tau={t/YR:10.3e} yr  predicted {'despun' if pred else 'free':7s} "
              f"observed {note:30s} {verdict}")

    # robustness over a grid of fiducials (each grid point is ONE fiducial for all bodies)
    grid = [(al, Q, k2, P) for al in (0.33, 0.4) for Q in (10, 30, 100, 300, 1000)
            for k2 in (0.01, 0.03, 0.1, 0.3, 1.0) for P in (6.0, 12.0, 24.0)]
    n12 = 0; fails = {}
    for al, Q, k2, P in grid:
        r = classify(BODIES, alpha=al, Q=Q, k2=k2, P_i_h=P)
        bad = [x[0] for x in r if x[3] != x[4]]
        if not bad: n12 += 1
        for b in bad: fails[b] = fails.get(b, 0) + 1
    print(f"\n  robustness: {n12}/{len(grid)} grid fiducials give 12/12 "
          f"({100*n12/len(grid):.0f} %). Failures by body: {fails if fails else 'none'}")
    print("  (tau scales as Q*omega_i/k2, so the grid spans ~3.5 dex. Mercury sits 0.5 dex below the age")
    print("   line with the fiducial and flips to 'free' for large Q/k2; Earth (1.3 dex above) flips for")
    print("   small Q/k2. The 12/12 therefore holds for a band of fiducials, not for any fiducial.)")
    print("\nSTATUS: the dichotomy follows from the a^6/Mp^2 scaling (degenerate with standard tidal theory).")
    print("Intrinsic spin rates (and Venus's sign) stay formation-contingent, as the page says.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8.2, 4.6))
        for i, (nm, t, p, pred, obs, note) in enumerate(rows):
            ax.scatter(i, np.log10(t/YR), color="#D85A30" if obs else "#185FA5", s=50, zorder=3)
        ax.axhline(np.log10(4.5e9), ls="--", color="#555", label="age 4.5 Gyr")
        ax.set_xticks(range(len(rows))); ax.set_xticklabels([r[0] for r in rows], rotation=45, fontsize=8)
        ax.set_ylabel(r"$\log_{10}\tau_{\rm lock}$ [yr]")
        ax.set_title("tau_lock vs age (orange = observed locked/despun, blue = free)")
        ax.legend(fontsize=8); ax.grid(alpha=0.25)
        plt.tight_layout(); plt.savefig("ch_spin_locking.png", dpi=120, bbox_inches="tight"); plt.close()
        print("[figure written: ch_spin_locking.png]")
    except Exception as exc:
        print(f"[matplotlib unavailable: {exc}] numbers above are the result.")
