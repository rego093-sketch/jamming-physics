#!/usr/bin/env python3
"""
acoustic_length_hypothesis_interpretation.py  --  Re-implementation (2026-09-28) of the lost Ch 14.1
capping script "a Big-Bang-free interpretation of the scale (hypothesis)". HYP level: it reports the
five test routes and the non-claims; it does NOT derive 150 Mpc.

PAGE CLAIMS (docs/cosmology/14-acoustic-length-structurally-hard/, 15-large-scale-structure-bao/,
             16-open-problems-gathered/)
  - selected length lambda(k) = mu + eps k^2 - sigma k^4 -> L_* = 2 pi sqrt2 sqrt(sigma/eps), exact
    one-half exponent independent of mu; blind direct simulation beta_hat ~ 0.501; attractor
    x_* = 2/pi with slope -(pi/2)^5 (companion fluid-dynamics volume).
  - "The selection prefactor 2 pi sqrt2 ~ 8.89 is forced, and it independently matches the factor 10
    separating the supercluster-scale inflow length (sqrt(GM/a0) ~ 10-15 Mpc) from the BAO scale."
  - "Five independent routes were tested computationally -- the fixed constants alone, cluster
    dynamics, the selection law, the inflow rate with the c-ceiling, and the rotational-to-3D
    crossover -- and all five deliver the mechanism type while leaving the absolute normalisation
    dependent on the matter distribution's amplitude (equivalently, the literal c-limit places the
    crossover at the Hubble scale, and 150 Mpc would need an unforced velocity fraction 0.075c)."
  - "The required factor 28.6 is moreover fitted to better than 1% by several forced-constant forms
    (3(pi/2)^5 = 28.69, 9 pi = 28.27, 3 pi^2 = 29.61), so claiming any one would be curve-fitting."
  Classification on the page: mechanism closed (HYP); absolute value = empirical normalisation [O].

SEAM (declared): routes 3 imports the companion fluid-dynamics volume's own code
  repro/fluid-dynamics/.../08-pillar-iii-dynamical-arrangement-selects/length_selection.py
  and the attractor of .../03-marginal-substrate-why-jammed-arrangement/unjam_inflow.py
  (alpha = 2/pi is an inherited constant there). Nothing is re-fitted; if the import fails the
  analytic forms are evaluated instead and the failure is printed.

INPUTS (sources)
  - c, G, Mpc, M_sun = 1.98892e30 kg; H0 = 70 km/s/Mpc; a0 = c H0 / 2 pi (volume's law).
  - Supercluster masses 1e16, 1e17, 2e17 M_sun (Laniakea ~1e17 M_sun, Tully et al. 2014 Nature 513, 71).
  - Route 5 toy: sigma(R) = sigma8 (R / 8 h^-1 Mpc)^(-(n_eff+3)/2), n_eff = -1.5, h = 0.7,
    sigma8 in {0.6, 0.8, 1.0}, crossover thresholds delta_x in {1, 0.5, 0.2} (none forced).
  - Target 150 Mpc used ONLY to compute what would be required, never to set a parameter.

ALGORITHM
  Route 1: every fixed-constant length (as in probe_subhorizon_desert.py) vs 150 Mpc.
  Route 2: R_g = sqrt(G M / a0) and 2 pi sqrt2 R_g for each M; ratio 150 Mpc / R_g.
  Route 3: analytic argmax of lambda(k) for several mu; nonlinear Swift-Hohenberg exponent via the
           companion's one_half_law(); prefactor 2 pi sqrt2; sigma/eps not supplied by constants.
  Route 4: crossover L = v / H0; v = c gives the Hubble length; required v/c for 150 Mpc.
  Route 5: L_x where sigma(L_x) = delta_x; dependence on sigma8 and delta_x.
  Look-elsewhere: enumerate p * pi^q and p * (pi/2)^q (p in 1..12, q in -3..6) within 1% of F.

EXPECTED (page): all five routes give mechanism, none forces 150 Mpc; 2 pi sqrt2 = 8.89 vs factor ~10;
  v/c = 0.075; several forms within 1% of 28.6.
"""
import os, sys
import numpy as np

c = 2.99792458e8; G = 6.674e-11; Mpc = 3.0856775814913673e22; Msun = 1.98892e30
H0 = 70e3 / Mpc; a0 = c * H0 / (2 * np.pi); L_T = 150 * Mpc
nu_p = 3 * np.pi ** 4; a_lat = 6.33e-19
PREF = 2 * np.pi * np.sqrt(2)
HERE = os.path.dirname(os.path.abspath(__file__))
FLUID = os.path.normpath(os.path.join(HERE, "..", "..", "fluid-dynamics", "repro", "fluid-dynamics"))

def route1():
    rho_c = 3 * H0 ** 2 / (8 * np.pi * G)
    Ls = [a_lat, c / nu_p, np.sqrt(a_lat * c / nu_p), c / H0, c * np.sqrt(np.pi / (G * rho_c)), 2 * np.pi * c / H0]
    return min(abs(np.log10(l / L_T)) for l in Ls)

def route2():
    return [(M, np.sqrt(G * M * Msun / a0) / Mpc) for M in (1e16, 1e17, 2e17)]

def route3():
    info = {}
    try:
        sys.path.insert(0, os.path.join(FLUID, "08-pillar-iii-dynamical-arrangement-selects"))
        import length_selection as ls
        kk = np.linspace(0.01, 5, 200000)
        info["argmax"] = [(mu, kk[np.argmax(mu + kk ** 2 - 0.25 * kk ** 4)], ls.k_star(1.0, 0.25)) for mu in (-0.5, 0.0, 0.5)]
        info["beta_hat"] = ls.one_half_law()
        info["src"] = "companion length_selection.py"
    except Exception as exc:
        info["src"] = f"import failed ({exc}); analytic only"
        info["argmax"] = [(mu, None, np.sqrt(1.0 / 0.5)) for mu in (-0.5, 0.0, 0.5)]
        info["beta_hat"] = None
    alpha = 2 / np.pi
    F = lambda x: alpha * x ** -5 - x ** -4
    ends = []
    for x0 in (0.2, 0.5, 1.0, 2.0, 5.0):                     # same RK4 scheme as companion attractor()
        x, dt = x0, 1e-4
        for _ in range(400000):
            k1 = F(x); k2 = F(x + 0.5 * dt * k1); k3 = F(x + 0.5 * dt * k2); k4 = F(x + dt * k3)
            x += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0; dt = min(2e-2, dt * 1.001)
            if abs(F(x)) < 1e-14: break
        ends.append(x)
    eps = 1e-7; slope = (F(alpha + eps) - F(alpha - eps)) / (2 * eps)
    info["attractor"] = (np.array(ends), alpha, slope)
    return info

def route4():
    return (c / H0) / Mpc, L_T * H0 / c

def route5(n_eff=-1.5, h=0.7):
    R8 = 8 / h
    out = []
    for s8 in (0.6, 0.8, 1.0):
        for dx in (1.0, 0.5, 0.2):
            out.append((s8, dx, R8 * (s8 / dx) ** (2 / (n_eff + 3))))
    return out

def look_elsewhere(F, tol=0.01):
    hits = []
    for p in range(1, 13):
        for q in range(-3, 7):
            for base, name in ((np.pi, "pi"), (np.pi / 2, "(pi/2)")):
                v = p * base ** q
                if abs(v / F - 1) < tol and q != 0:
                    hits.append((f"{p}*{name}^{q}", v, 100 * (v / F - 1)))
    return hits

if __name__ == "__main__":
    F = (c / H0) / L_T
    print(f"Target factor F = (c/H0)/150 Mpc = {F:.3f} (H0=70). 150 Mpc is used only as the thing to be explained.\n")
    print("Route 1 -- fixed constants alone:")
    print(f"  nearest fixed-constant length is {route1():.2f} dex from 150 Mpc -> no length (mechanism: none).\n")
    print("Route 2 -- cluster dynamics, R_g = sqrt(G M / a0), a0 = cH0/2pi = %.3e m/s^2:" % a0)
    for M, Rg in route2():
        print(f"  M = {M:.0e} Msun: R_g = {Rg:6.2f} Mpc;  2pi*sqrt2*R_g = {PREF*Rg:7.1f} Mpc;  150/R_g = {150/Rg:6.2f}")
    print(f"  2 pi sqrt2 = {PREF:.3f}. The 'factor ~10' holds only for M ~ 1-2e17 Msun: R_g scales as M^1/2,")
    print("  so the absolute length inherits the (measured) supercluster mass -> amplitude-dependent.\n")
    print("Route 3 -- selection law lambda(k) = mu + eps k^2 - sigma k^4 (companion fluid volume):")
    r3 = route3(); print(f"  source: {r3['src']}")
    for mu, km, ka in r3["argmax"]:
        print(f"  mu = {mu:+.1f}: argmax k = {km if km is None else round(km, 5)}  analytic k* = {ka:.5f}  (mu-independent)")
    if r3["beta_hat"] is not None:
        print(f"  nonlinear Swift-Hohenberg exponent d log L*/d log(sigma/eps) = {r3['beta_hat']:.4f} (theory 0.5; page 0.501)")
    ends, alpha, slope = r3["attractor"]
    print(f"  attractor dx/dt = a x^-5 - x^-4, a = 2/pi: all x0 -> {ends.mean():.6f} (2/pi = {alpha:.6f}); "
          f"F'(x*) = {slope:.4f} vs -(pi/2)^5 = {-(np.pi/2)**5:.4f}")
    print(f"  L* = {PREF:.3f} sqrt(sigma/eps): the prefactor is forced, but sigma/eps is NOT supplied by the")
    print("  fixed constants -> the absolute L* is a normalisation.\n")
    Lh, vfrac = route4()
    print("Route 4 -- inflow rate with the c-ceiling, crossover L = v/H0:")
    print(f"  v = c -> L = c/H0 = {Lh:.0f} Mpc (Hubble scale). 150 Mpc needs v/c = {vfrac:.4f}.")
    print(f"  PAGE says 0.075c; the plain L = v/H0 reading gives {vfrac:.3f}c (factor {0.075/vfrac:.2f} apart; the page's")
    print("  crossover definition is not recorded). Either way the fraction is unforced.\n")
    print("Route 5 -- 2D-rotational -> 3D-isotropic crossover (toy: sigma(L_x) = delta_x, n_eff = -1.5):")
    for s8, dx, Lx in route5():
        print(f"  sigma8 = {s8:.1f}, delta_x = {dx:.1f}: L_x = {Lx:7.1f} Mpc")
    print("  L_x scales as sigma8^(2/(n+3)) and with the unforced threshold -> set by the matter amplitude.\n")
    print("Look-elsewhere: simple forms p*pi^q, p*(pi/2)^q within 1% of F:")
    for name, v, d in look_elsewhere(F):
        print(f"  {name:14s} = {v:8.3f}  ({d:+.2f}%)")
    for name, v in (("3(pi/2)^5", 3 * (np.pi / 2) ** 5), ("9 pi", 9 * np.pi), ("3 pi^2", 3 * np.pi ** 2)):
        print(f"  page form {name:10s} = {v:.3f}  deviation from F = {100*(v/F-1):+.2f}%  (from 28.6: {100*(v/28.6-1):+.2f}%)")
    print("\nVERDICT (HYP): mechanism type and the prefactor 2 pi sqrt2 close; all five routes leave the")
    print("absolute 150 Mpc to the matter distribution's amplitude -> empirical normalisation [O]. No constant moved.")
