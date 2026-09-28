#!/usr/bin/env python3
"""
probe_subhorizon_desert.py  --  Re-implementation (2026-09-28) of the lost Ch 14.1 diagnostic
"why the missing length is structurally hard, not merely unknown".

PAGE CLAIMS (docs/cosmology/14-acoustic-length-structurally-hard/, 15-large-scale-structure-bao/)
  "Listing every length the fixed constants can build -- the lattice cell a, the per-nucleon inflow
   length c/nu_p ~ 10^3 km, their geometric mean, the Hubble length c/H0, the relativistic Jeans
   length c sqrt(pi/(G rho_c)), and the a0-length 2 pi c/H0 -- places them in exactly two regimes:
   microscopic inflow scales (<~10^6 m) and cosmological scales (>~10^26 m). The target ~5e24 m
   (150 Mpc) falls in the empty 10-decade gap between them, 8.6 dex above the nearest
   microscopic-cosmological geometric mean and 1.5 dex below the Hubble length. ... writing
   L = (c/H0)(H0/nu_p)^p and solving for the exponent that lands on 150 Mpc returns p ~ 0.072."
  "Evaluating [the comoving sound-horizon integral] with standard parameters -- invoked here only
   diagnostically -- returns r_s ~ 144 Mpc and (c/H0)/r_s ~ 30, with R(a_rec) ~ 0.62 ... the
   'factor 29' ... is ~28.6 at H0 = 70, ~30.8 at H0 = 67.4."

INPUTS (sources)
  - c, G (CODATA); Mpc; nu_p = 3 pi^4 (legacy ch1); a = 6.33e-19 m (legacy ch9).
  - H0 = 70 km/s/Mpc for the desert audit (page), rho_c = 3H0^2/(8 pi G). Target 150 Mpc.
  - Sound horizon (DIAGNOSTIC ONLY, standard LCDM history the volume rejects): Planck 2018
    h = 0.674, omega_b = 0.02237, omega_c = 0.1200, T_CMB = 2.7255 K, N_eff = 3.046,
    massless neutrinos, z_rec = 1090 (page). omega_gamma = 2.473e-5 (T/2.7255)^4.

ALGORITHM
  1. Tabulate the six lengths, split into regimes, locate the target; gap width; distance of target
     from the geometric mean of the largest microscopic and smallest cosmological length; distance
     below c/H0; p = log(L_T H0/c) / log(H0/nu_p).
  2. r_s = int_{z_rec}^inf c_s(z) dz / H(z), c_s = c / sqrt(3(1+R)), R = (3 omega_b / 4 omega_gamma)/(1+z);
     report r_s, R(z_rec), (c/H0)/r_s at h = 0.674 and h = 0.70 (r_s depends only on omega's).

EXPECTED (page): two regimes; target 8.6 dex above micro-cosmo mean, 1.5 dex below c/H0;
  p ~ 0.072; r_s ~ 144 Mpc; R ~ 0.62; ratio ~30 (30.8 at 67.4).
"""
import numpy as np

c = 2.99792458e8; G = 6.674e-11; Mpc = 3.0856775814913673e22
nu_p = 3 * np.pi ** 4; a = 6.33e-19
H0 = 70e3 / Mpc; rho_c = 3 * H0 ** 2 / (8 * np.pi * G); L_T = 150 * Mpc

def desert():
    L = {"lattice cell a": a, "c/nu_p": c / nu_p, "sqrt(a c/nu_p)": np.sqrt(a * c / nu_p),
         "Hubble c/H0": c / H0, "rel. Jeans c sqrt(pi/(G rho_c))": c * np.sqrt(np.pi / (G * rho_c)),
         "a0-length 2 pi c/H0": 2 * np.pi * c / H0}
    micro = {k: v for k, v in L.items() if v < 1e10}; cosmo = {k: v for k, v in L.items() if v > 1e20}
    top_micro = max(micro.values()); bot_cosmo = min(cosmo.values())
    gmean = np.sqrt(top_micro * bot_cosmo)
    p = np.log(L_T * H0 / c) / np.log(H0 / nu_p)
    return L, micro, cosmo, top_micro, bot_cosmo, gmean, p

def sound_horizon(h=0.674, ob=0.02237, oc=0.1200, T=2.7255, Neff=3.046, zrec=1090.0):
    og = 2.473e-5 * (T / 2.7255) ** 4; orad = og * (1 + 0.2271 * Neff)
    om = ob + oc; H100 = 100e3 / Mpc
    lnz = np.linspace(np.log(1 + zrec), np.log(1 + 1e9), 200001); zp1 = np.exp(lnz)
    H = H100 * np.sqrt(orad * zp1 ** 4 + om * zp1 ** 3)        # Lambda negligible at z > 1090
    R = (3 * ob / (4 * og)) / zp1
    cs = c / np.sqrt(3 * (1 + R))
    f = cs / H * zp1                                           # dz = (1+z) dlnz
    rs = np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(lnz)) / Mpc
    return rs, (3 * ob / (4 * og)) / (1 + zrec)

if __name__ == "__main__":
    print("=== 1. The sub-horizon desert (H0 = 70) ===")
    L, micro, cosmo, tm, bc, gm, p = desert()
    for k, v in L.items():
        print(f"  {k:32s} {v:10.3e} m   log10 = {np.log10(v):6.2f}")
    print(f"  microscopic regime: max = {tm:.2e} m (log {np.log10(tm):.2f}); cosmological regime: min = {bc:.2e} m (log {np.log10(bc):.2f})")
    print(f"  empty gap between regimes: {np.log10(bc/tm):.1f} decades   (page text: '10-decade gap')")
    print(f"  target 150 Mpc = {L_T:.2e} m (log {np.log10(L_T):.2f}): {np.log10(L_T/gm):.2f} dex above the micro-cosmo "
          f"geometric mean, {np.log10(bc/L_T):.2f} dex below c/H0")
    print(f"  power-law bridge L = (c/H0)(H0/nu_p)^p -> p = {p:.4f}  (not 0, 1/2, 1, 2)")
    print("  RESULT: no fixed-constant length reaches 150 Mpc; the desert is real.\n")
    print("=== 2. What kind of object 150 Mpc is (diagnostic: standard history, NOT adopted) ===")
    rs, Rrec = sound_horizon()
    print(f"  comoving sound horizon r_s(z_rec=1090) = {rs:.1f} Mpc;  R(a_rec) = {Rrec:.3f}")
    for hh in (0.674, 0.70):
        print(f"  h = {hh}: (c/H0)/r_s = {(c/(hh*100e3/Mpc))/Mpc/rs:.2f};   (c/H0)/150 Mpc = {(c/(hh*100e3/Mpc))/Mpc/150:.2f}")
    for om_shift in (-0.01, +0.01):
        rs2, _ = sound_horizon(oc=0.1200 + om_shift)
        print(f"  sensitivity: omega_c {0.1200+om_shift:.3f} -> r_s = {rs2:.1f} Mpc")
    print("  RESULT: the 'factor ~29' is the value of a history integral (depends on omega_m, omega_b,")
    print("  omega_r, z_rec), not a geometric constant; a static present-emission lattice has neither")
    print("  an expansion history nor a recombination epoch, so this route is structurally absent.")
