#!/usr/bin/env python3
"""
ch8_lensing_consistency.py  --  Chapter 8: does the rotation-fitting deficit lens like a real mass?

Re-implementation (2026-09-28) of a script cited on the site but lost. Rotation-curve fit follows
legacy_v2_3/ch6_galaxy_rar.py part (C) (same nu-function, same 3 km/s error floor, one free
Upsilon) but at the DERIVED a0 = c H0 / 2pi instead of the empirical 1.2e-10. numpy only.

CLAIM ON THE PAGES
------------------
  08-dark-matter-vacuum-deficit: "ch8_lensing_consistency.py fits NGC 2403 with the inflow law at
     the derived a0 = cH0/2pi, reads the implied deficit as a mass (M_def/M_bar ~ 4.4 at the outer
     radius) whose density is positive at every radius -- a well-behaved real mass that lenses with
     gamma = 1 (M_lens = M_dyn), matching observed galaxy lensing, where a modify-dynamics-only
     reading would give gamma = M_bar/M_dyn -> 0.2."
  axh: "Deficit lensing gamma=1 (ch8_lensing_consistency.py; NGC 2403)".

INPUTS (sources)
  ../legacy_v2_3/NGC2403_rotmod.dat : SPARC (Lelli, McGaugh & Schombert 2016), D = 3.16 Mpc.
  a0 = c H0 / 2pi with H0 in {67.4 (Planck 2018), 70.0, 73.04 (SH0ES 2022)} -- [HAND] the page
     does not say which H0; all three are reported. Empirical a0 = 1.2e-10 shown for reference.
  nu(x) = 1/(1 - exp(-sqrt(x)))  (legacy ch6 law);  error floor 3 km/s [HAND, legacy convention].
  Free parameter: disk Upsilon only (bulge is zero for NGC 2403). G = 6.67430e-11.

ALGORITHM
  1. Fit Upsilon on [0.1, 1.5] by golden-section search on chi2 (deterministic).
  2. Spherical-equivalent enclosed masses [HAND approximation; the disk is not spherical]:
       M_bar = V_bar^2 r / G,   M_dyn = V_model^2 r / G,   M_def = M_dyn - M_bar
     (also with V_obs in place of V_model).
  3. rho_def(r) = (dM_def/dr) / (4 pi r^2) by finite differences; count negative radii.
  4. Lensing mass under the two readings:
       VP deficit, no-slip GR matching (Phi = Psi, gamma_PPN = 1): M_lens = M_bar + M_def = M_dyn.
       modify-dynamics-only (lensing sees baryons only):              M_lens / M_dyn = M_bar / M_dyn.
     IMPORTANT: gamma = 1 for the deficit is an ASSUMPTION (no-slip) carried into the script, not
     an output of it; no lensing data are used. What the script does test is that the implied
     deficit is a positive, monotone mass -- the precondition for lensing like one.

EXPECTED OUTPUT (page): M_def/M_bar ~ 4.4 at the outer radius; rho_def > 0 at every radius;
  M_bar/M_dyn -> 0.2.

DETERMINISM: no RNG. Runtime < 2 s. DEPENDENCIES: numpy (matplotlib optional).
"""
import os
import numpy as np

C = 2.99792458e8
G = 6.67430e-11
MPC = 3.0856775814913673e22
KPC = 3.0856775814913673e19
KMS = 1.0e3
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "legacy_v2_3", "NGC2403_rotmod.dat")


def nu(x):
    return 1.0 / (1.0 - np.exp(-np.sqrt(x)))


def load(path=DATA):
    d = np.genfromtxt(path, comments="#")
    return (d[:, 0] * KPC, d[:, 1] * KMS, d[:, 2] * KMS, d[:, 3] * KMS, d[:, 4] * KMS, d[:, 5] * KMS)


def vbar2(U, Vgas, Vdisk, Vbul):
    return np.clip(Vgas * np.abs(Vgas) + U * Vdisk * np.abs(Vdisk) + Vbul * np.abs(Vbul), 0, None)


def fit(a0, R, Vobs, eV, Vgas, Vdisk, Vbul):
    err = np.sqrt(eV ** 2 + (3 * KMS) ** 2)

    def model(U):
        gN = vbar2(U, Vgas, Vdisk, Vbul) / R
        return np.sqrt(gN * nu(gN / a0) * R)

    def chi2(U):
        return np.sum(((model(U) - Vobs) / err) ** 2)

    a, b = 0.1, 1.5
    gr = (np.sqrt(5) - 1) / 2
    c1, c2 = b - gr * (b - a), a + gr * (b - a)
    for _ in range(200):
        if chi2(c1) < chi2(c2):
            b, c2 = c2, c1; c1 = b - gr * (b - a)
        else:
            a, c1 = c1, c2; c2 = a + gr * (b - a)
    U = 0.5 * (a + b)
    return U, chi2(U) / (len(R) - 1), model(U)


def analyse(label, a0, data, verbose=True):
    R, Vobs, eV, Vgas, Vdisk, Vbul = data
    U, c2, Vm = fit(a0, R, Vobs, eV, Vgas, Vdisk, Vbul)
    Mbar = vbar2(U, Vgas, Vdisk, Vbul) * R / G
    Mdyn = Vm ** 2 * R / G
    Mdef = Mdyn - Mbar
    Mdef_obs = Vobs ** 2 * R / G - Mbar
    rho = np.gradient(Mdef, R) / (4 * np.pi * R ** 2)
    rho_obs = np.gradient(Mdef_obs, R) / (4 * np.pi * R ** 2)
    res = dict(U=U, c2=c2, ratio_last=Mdef[-1] / Mbar[-1], ratio_out5=np.mean(Mdef[-5:] / Mbar[-5:]),
               ratio_obs_last=Mdef_obs[-1] / Mbar[-1], nneg=int(np.sum(rho <= 0)),
               nneg_obs=int(np.sum(rho_obs <= 0)), nneg_M=int(np.sum(Mdef < 0)),
               g_mdo=Mbar[-1] / Mdyn[-1], N=len(R), Rlast=R[-1] / KPC, Mdef=Mdef, Mbar=Mbar, Mdyn=Mdyn, R=R)
    if verbose:
        print(f"  {label:<24s} a0={a0:.3e}  Upsilon={U:.3f}  chi2/dof={c2:.2f}  "
              f"M_def/M_bar(last r={res['Rlast']:.1f} kpc)={res['ratio_last']:.2f}  "
              f"(outer-5 mean {res['ratio_out5']:.2f}; with V_obs {res['ratio_obs_last']:.2f})")
        print(f"  {'':<24s} rho_def<=0 at {res['nneg']}/{res['N']} radii (model V), "
              f"{res['nneg_obs']}/{res['N']} (observed V);  M_def<0 at {res['nneg_M']} radii;  "
              f"modify-dynamics-only M_bar/M_dyn(last) = {res['g_mdo']:.3f}")
    return res


if __name__ == "__main__":
    print("=== ch8_lensing_consistency.py : NGC 2403 deficit as a lensing mass ===")
    data = load()
    runs = {}
    for H0 in (67.4, 70.0, 73.04):
        a0 = C * H0 * KMS / MPC / (2 * np.pi)
        runs[H0] = analyse(f"derived, H0={H0}", a0, data)
    ref = analyse("empirical a0 (ch6 ref)", 1.2e-10, data)

    r70 = runs[70.0]
    print("\nLENSING (last radius, H0 = 70):")
    print(f"  VP deficit, no-slip (gamma=1 ASSUMED): M_lens/M_dyn = 1.000")
    print(f"  modify-dynamics-only (baryons lens):   M_lens/M_dyn = {r70['g_mdo']:.3f}")
    print("  No galaxy-lensing data are used; gamma = 1 is the no-slip input, not a measured output.")

    lo = min(r['ratio_last'] for r in runs.values()); hi = max(r['ratio_last'] for r in runs.values())
    print("\nRESULT vs PAGE")
    print(f"  M_def/M_bar at the outer radius: {lo:.2f}-{hi:.2f} over H0 = 67.4-73.04 (page: ~4.4).")
    print(f"  rho_def > 0 at every radius (model V): "
          f"{'YES' if all(r['nneg']==0 for r in runs.values()) else 'NO'} "
          f"(with the noisy observed V: {r70['nneg_obs']} non-positive radii at H0=70).")
    print(f"  modify-dynamics-only M_bar/M_dyn: {min(r['g_mdo'] for r in runs.values()):.3f}-"
          f"{max(r['g_mdo'] for r in runs.values()):.3f} (page: -> 0.2).")
    print("  Grade: consistency check under an assumed gamma = 1; the joint fit against measured")
    print("  lensing of the same systems remains open [O].")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 4))
        Rk = r70["R"] / KPC
        ax.plot(Rk, r70["Mbar"] / 1.989e30, label="M_bar")
        ax.plot(Rk, r70["Mdef"] / 1.989e30, label="M_def (deficit)")
        ax.plot(Rk, r70["Mdyn"] / 1.989e30, "--", label="M_dyn = M_lens (gamma=1)")
        ax.set_xlabel("r [kpc]"); ax.set_ylabel("enclosed mass [M_sun]"); ax.legend(fontsize=8)
        ax.set_title("NGC 2403, a0 = cH0/2pi (H0=70)")
        plt.tight_layout(); plt.savefig(os.path.join(HERE, "ch8_lensing_consistency.png"), dpi=110)
        print("  [figure written: ch8_lensing_consistency.png]")
    except Exception as exc:
        print(f"  [matplotlib unavailable: {exc}] numbers above are the result.")
