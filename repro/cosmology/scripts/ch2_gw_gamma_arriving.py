#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_gw_gamma_arriving.py  --  Chapter 2 ("What actually arrives", v2): source energy vs arriving
fluence for GRB 170817A / GW170817, and the distance at which a burst becomes dangerous.
=================================================================================================
Re-implementation (2026-09-28) of the lost script cited by
  docs/cosmology/02-light-lattice-elastic-wave-sharpest/  ("What actually arrives (v2)")

PAGE CLAIM (verbatim)
  "The often-quoted '10^53 erg' is a source energy ... it is not what reaches a detector. The
   arriving fluence is F = E_iso/(4 pi d^2) -- for GRB 170817A, F ~ 2.6x10^-7 erg cm^-2, the energy
   of 10^-13 s of sunlight on the same area, harmless. Only a Galactic-scale (kpc) burst delivers a
   dangerous fluence."

WHAT THIS SCRIPT DOES
  (1) F = E_iso / (4 pi d^2) for GRB 170817A from published E_iso and distance; compare with the
      directly MEASURED fluence (these must agree up to band/k-correction; this is the check).
  (2) Convert to 'seconds of sunlight' with the solar constant.
  (3) The distance inside which a burst's fluence exceeds a biologically significant threshold
      (100 kJ m^-2 = 1e8 erg cm^-2; Thomas et al. 2005, ApJ 634, 509; Melott & Thomas 2011),
      for E_iso = 1e46 ... 1e54 erg, including the page's '10^53 erg'.
  (4) The gravitational-wave counterpart: fluence of the GW energy of GW170817 at 40 Mpc
      (radiated energy lower bound), to show the same 1/(4 pi d^2) dilution for the GW channel.
  The 1/(4 pi d^2) law itself is shown on the lattice in ch2_gw_gamma_3d.py (r^2 F const to 0.15%).

INPUTS (sources; measured, never tuned)
  GRB 170817A (Fermi-GBM; Goldstein et al. 2017, ApJL 848, L14):
      fluence (10-1000 keV) = (2.8 +- 0.2)e-7 erg cm^-2 ;  E_iso (1 keV-10 MeV) = (3.1 +- 0.7)e46 erg
  Distance: 40 (+8 -14) Mpc (LIGO/Virgo, PRL 119, 161101 (2017)); host NGC 4993.
  GW170817 radiated energy: > 0.025 M_sun c^2 (LIGO/Virgo PRL 119, 161101; lower bound).
  Solar constant 1361 W m^-2 (Kopp & Lean 2011).  1 Mpc = 3.0856775814913673e24 cm.
  M_sun c^2 = 1.787e54 erg.

EXPECTED OUTPUT (run 2026-09-28): F(E_iso, 40 Mpc) = 1.62e-7 erg cm^-2 (0.87e-7 - 4.7e-7 over the
  quoted E_iso and d errors) vs measured 2.8e-7; 1.2e-13 - 2.1e-13 s of sunlight; danger radius
  2.9 kpc for 1e53 erg (0.9 kpc for 1e52); GW170817 GW fluence > 0.23 erg cm^-2.
  NOTE: the E_GW > 0.025 M_sun c^2 input should be re-checked against the LIGO/Virgo paper.
DETERMINISM: SEED = 19 (no RNG); 2 x SHA-256 over 6-sig-fig results. Runtime < 1 s. numpy only.
"""
import json, hashlib
import numpy as np

SEED = 19
MPC = 3.0856775814913673e24          # cm
KPC = MPC / 1e3
SOLAR = 1361.0 * 1e7 / 1e4           # erg s^-1 cm^-2  (1361 W m^-2)
MSUNC2 = 1.98841e33 * (2.99792458e10) ** 2   # erg
F_DANGER = 1e8                       # erg cm^-2 = 100 kJ m^-2

def sig(x, n=6):
    x = float(x)
    if x == 0.0 or not np.isfinite(x):
        return x
    from math import floor, log10
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))

def digest(obj):
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(hashlib.sha256(blob).digest()).hexdigest()

fluence = lambda E, d_cm: E / (4 * np.pi * d_cm ** 2)

if __name__ == "__main__":
    np.random.seed(SEED)
    Eiso, dEiso = 3.1e46, 0.7e46
    d, dlo, dhi = 40 * MPC, 26 * MPC, 48 * MPC
    F_meas = 2.8e-7
    F = fluence(Eiso, d)
    F_min = fluence(Eiso - dEiso, dhi); F_max = fluence(Eiso + dEiso, dlo)
    print("=" * 90)
    print(" ch2_gw_gamma_arriving.py -- what actually arrives from GRB 170817A / GW170817")
    print("=" * 90)
    print(f" (1) F = E_iso/(4 pi d^2), E_iso = 3.1e46 erg, d = 40 Mpc:  F = {F:.3e} erg cm^-2")
    print(f"     over E_iso +- 0.7e46 and d = 26-48 Mpc:               F = {F_min:.2e} .. {F_max:.2e}")
    print(f"     measured (GBM, 10-1000 keV):                          F = {F_meas:.2e} erg cm^-2")
    print(f"     page value 2.6e-7 would correspond to E_iso = {2.6e-7*4*np.pi*d**2:.2e} erg at 40 Mpc")
    print(f"     source energy / arriving fluence = 4 pi d^2 = {4*np.pi*d**2:.3e} cm^2")
    print(f"\n (2) seconds of sunlight (solar constant {SOLAR:.3e} erg s^-1 cm^-2):")
    for lab, f in (("F(E_iso,40 Mpc)", F), ("measured", F_meas), ("page 2.6e-7", 2.6e-7)):
        print(f"     {lab:16s}: {f/SOLAR:.2e} s")
    print(f"\n (3) danger radius d* = sqrt(E_iso / (4 pi F*)), F* = 1e8 erg cm^-2 (100 kJ m^-2):")
    res = {"seed": SEED, "F": sig(F), "F_min": sig(F_min), "F_max": sig(F_max),
           "sun_s": sig(F / SOLAR), "danger_kpc": {}}
    for E in (1e46, 3.1e46, 1e50, 1e52, 1e53, 1e54):
        ds = np.sqrt(E / (4 * np.pi * F_DANGER))
        res["danger_kpc"][f"{E:.1e}"] = sig(ds / KPC)
        print(f"     E_iso = {E:.1e} erg  ->  d* = {ds/KPC:9.4f} kpc  ({ds/KPC*1e3:10.1f} pc)")
    print("     => a '1e53 erg' burst is dangerous only within a few kpc (inside the Galaxy);")
    print(f"        GRB 170817A itself would have had to be within ~{np.sqrt(Eiso/(4*np.pi*F_DANGER))/KPC*1e3:.1f} pc.")
    Egw = 0.025 * MSUNC2
    Fgw = fluence(Egw, d)
    res["F_gw"] = sig(Fgw)
    print(f"\n (4) GW170817: E_GW > 0.025 M_sun c^2 = {Egw:.2e} erg  ->  GW fluence at 40 Mpc > {Fgw:.2f} erg cm^-2")
    print(f"     (= {Fgw/SOLAR:.1e} s of sunlight), ~{Fgw/F_meas:.0e} x the gamma fluence, yet deposited")
    print("     in matter only at strain h ~ 1e-21: same 1/(4 pi d^2) dilution in both channels.")
    print("\n SCOPE: pure bookkeeping with measured inputs; it does not test any VP-specific mechanism.")
    print(f"\nDETERMINISM-DIGEST (2xSHA-256, 6 sig-fig): {digest(res)}")
