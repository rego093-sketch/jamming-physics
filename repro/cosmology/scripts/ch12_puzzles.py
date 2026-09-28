#!/usr/bin/env python3
"""
ch12_puzzles.py -- Ch 12 "Cosmological puzzles that dissolve": the one quantitative item (Olbers).
RE-IMPLEMENTATION (2026-09-28). The original script was lost; this rebuilds what the site pages
say it did. No parameter is adjusted to reach a page number.

PAGE CLAIMS (docs/cosmology/12-cosmological-puzzles-that-dissolve/, axb-reproducibility-map/):
  "Olbers integral diverges without attenuation, -> nL/kappa_opt (finite) with kappa_opt = H0/c
   => dark sky (distinguishing)"
  Sim A printout on the page:
    no attenuation: B(R) grows without bound as R increases (Olbers paradox)
    with attenuation: B -> nL/kappa_opt (finite) -> dark night sky
  Side numbers in the text: H0^-1 ~ 1.4e10 yr; vacuum energy ~1e113 J/m^3 vs dark energy
  ~1e-9 J/m^3 "a factor of about 1e120".

INPUTS (declared, not fitted):
  H0 = 70 km/s/Mpc (round value used across the volume; kappa_opt = H0/c is an INPUT, Ch 7 [open])
  n*L = cosmic luminosity density j = 1.5e35 W/Mpc^3 (0.1-2 um energy output, order of
        Driver et al. 2016, ApJ 827, 108; used ONLY for the optional physical-units cross-check)
  Sun mean surface brightness = L_sun/(4 pi^2 R_sun^2) (IAU nominal L_sun, R_sun)
  Planck energy density c^7/(hbar G^2) and dark-energy density 0.69*rho_crit c^2 (Planck 2018)
  are used only to check the page's "1e120" arithmetic.

ALGORITHM:
  (A) B(R) = int_0^R n L exp(-kappa r) dr, evaluated by trapezoid quadrature on a fine grid,
      with kappa = 0 (no attenuation) and kappa = H0/c; compared with the closed form nL/kappa.
  (B) Physical units: sky intensity I = j c /(4 pi H0) vs the Sun's surface brightness and the
      measured extragalactic background (~50-100 nW m^-2 sr^-1, e.g. Driver+2016; Hill+2018).
  (C) Arithmetic checks of the page's side numbers (Hubble time; vacuum-energy ratio).
EXPECTED OUTPUT: B(R) linear in R without attenuation; B/(nL/kappa) -> 1 with attenuation.
Deterministic, numpy only (matplotlib optional, MPLBACKEND=Agg).
"""
import numpy as np

c = 2.99792458e8; Mpc = 3.0856775814913673e22; yr = 3.15576e7
H0 = 70e3 / Mpc                     # s^-1
kappa = H0 / c                      # m^-1
L_H = 1 / kappa                     # Hubble length, m

def B_of_R(R_over_LH, kap_over, n=200001):
    """int_0^R exp(-kap r) dr in units nL*L_H (r in Hubble lengths)."""
    r = np.linspace(0.0, R_over_LH, n)
    f = np.exp(-kap_over * r)
    return np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(r))

if __name__ == "__main__":
    print("=== ch12_puzzles: Olbers' integral with and without lattice attenuation ===")
    print(f"H0 = 70 km/s/Mpc -> kappa_opt = H0/c = {kappa:.4e} m^-1 ; 1/kappa = c/H0 = {L_H/Mpc:.1f} Mpc\n")
    print("(A) B(R) in units of nL * (c/H0)")
    print("     R [c/H0]    no attenuation    with attenuation   ratio to nL/kappa")
    Rs = [0.1, 1, 3, 10, 30, 100, 300]
    Bn = []; Ba = []
    for R in Rs:
        b0 = B_of_R(R, 0.0); b1 = B_of_R(R, 1.0); Bn.append(b0); Ba.append(b1)
        print(f"     {R:8.1f}    {b0:14.4f}    {b1:14.6f}      {b1/1.0:.6f}")
    slope = np.polyfit(np.log(Rs[2:]), np.log(Bn[2:]), 1)[0]
    print(f"  no attenuation: log-log slope dlnB/dlnR = {slope:.4f} (=1 -> grows without bound: PARADOX)")
    print(f"  with attenuation: B(300 c/H0) / (nL/kappa) = {Ba[-1]:.6f} -> finite (closed form nL c/H0)")
    ok = abs(slope - 1) < 1e-6 and abs(Ba[-1] - 1) < 1e-6
    print(f"  PASS (page claim reproduced): {ok}\n")

    print("(B) physical-units cross-check (not a page number; order of magnitude only)")
    j = 1.5e35 / Mpc**3                                   # W m^-3
    I_sky = j * L_H / (4 * np.pi)                         # W m^-2 sr^-1
    Lsun = 3.828e26; Rsun = 6.957e8
    I_sun = Lsun / (4 * np.pi**2 * Rsun**2)
    print(f"  j = 1.5e35 W/Mpc^3 -> I_sky = j c/(4 pi H0) = {I_sky:.2e} W m^-2 sr^-1 = {I_sky*1e9:.0f} nW m^-2 sr^-1")
    print(f"  Sun surface brightness = {I_sun:.2e} W m^-2 sr^-1 -> sky/Sun = {I_sky/I_sun:.1e} (dark)")
    print("  Measured EBL (UV-to-far-IR) is ~50-100 nW m^-2 sr^-1: same order.")
    print("  CAVEAT: the expanding-FRW calculation gives the same order (the redshift dilution plays")
    print("  the role of the attenuation), so this number is DEGENERATE; only the interpretation")
    print("  (absorption vs finite age) differs. The page does not say where the attenuated energy")
    print("  goes (a static absorber must re-emit/heat); that closure is not computed here.\n")

    print("(C) side-number arithmetic")
    print(f"  1/H0 = {1/H0/yr:.3e} yr (page: ~1.4e10 yr)")
    hbar = 1.054571817e-34; G = 6.67430e-11
    u_pl = c**7 / (hbar * G**2)
    rho_c = 3 * H0**2 / (8 * np.pi * G); u_de = 0.69 * rho_c * c**2
    print(f"  Planck energy density c^7/(hbar G^2) = {u_pl:.2e} J/m^3 (page: ~1e113)")
    print(f"  dark-energy density 0.69 rho_c c^2   = {u_de:.2e} J/m^3 (page: ~1e-9)")
    print(f"  ratio = 10^{np.log10(u_pl/u_de):.1f}; with the page's own round numbers 1e113/1e-9 = 1e122")
    print("  -> the conventional '10^120' is a loose label; the page's stated numbers give 10^122-10^123.")
    print("  The Lambda 'dissolution' (uniform background does not gravitate) is a statement of the")
    print("  Ch 3 postulate, not a computation; nothing to reproduce numerically.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        R = np.linspace(0, 6, 400)
        plt.figure(figsize=(6, 4))
        plt.plot(R, R, label="no attenuation (diverges)")
        plt.plot(R, 1 - np.exp(-R), label=r"$e^{-\kappa r}$, $\kappa=H_0/c$")
        plt.axhline(1, ls=":", c="gray"); plt.xlabel("R [c/H0]"); plt.ylabel("B / (nL c/H0)")
        plt.legend(); plt.tight_layout(); plt.savefig("ch12_puzzles.png", dpi=110)
        print("\n[figure written: ch12_puzzles.png]")
    except Exception as e:
        print(f"[matplotlib unavailable: {e}]")
