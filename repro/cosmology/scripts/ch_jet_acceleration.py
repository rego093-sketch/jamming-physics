#!/usr/bin/env python3
"""
ch_jet_acceleration.py -- Ch 9 jets: the rotating-inflow funnel as a relativistic de Laval nozzle.
RE-IMPLEMENTATION (2026-09-28) of a lost script, rebuilt from the site pages. No parameter is
adjusted to reach a page number.

PAGE CLAIMS
  docs/cosmology/09-black-holes-jets-critical-inflow/: "On a steady streamline the relativistic
    Bernoulli invariant is Gamma w = const, with specific enthalpy w = 1 + Gad/(Gad-1) p/(rho c^2);
    a base that is hot or magnetized (w0>1) and slow (Gamma~1) expands adiabatically through the
    converging-diverging funnel ... so that the flow asymptotes to Gamma_inf = w0. The script
    ch_jet_acceleration.py integrates this and recovers the observed ranges: a mildly relativistic
    base w0 ~ 10 gives the Gamma ~ 10 of AGN jets, an extreme base w0 ~ 1e2-1e3 the Gamma ~ 1e2-1e3
    of gamma-ray bursts, each with a causal opening angle 1/Gamma of a few degrees down to a
    fraction of a degree -- matching what is seen." Loading of w0 is stated as NOT derived.
  axh / axj / 16-open-problems: "Jet acceleration Gamma -> w0 ... qualitative -> feasibility shown".

INPUTS (declared):
  base enthalpies w0 in {10, 100, 1000} (the page's illustrative values; NOT derived -- the page
  says the loading is open); adiabatic index Gad = 4/3 (relativistically hot gas; declared);
  base Lorentz factor Gamma0 -> 1 (subsonic reservoir). Units c = 1, base rest density rho0 = 1.
  Observed comparison values (literature, for the "matching what is seen" check only):
    AGN: Gamma ~ 5-50, intrinsic half-opening angle with Gamma*theta_j ~ 0.13 (Pushkarev+2009 A&A 507 L33)
    GRB: Gamma ~ 1e2-1e3; jet half-opening angles ~ 2-10 deg from breaks (Frail+2001 ApJ 562 L55)

ALGORITHM (steady 1-D relativistic nozzle, no fitting):
  Polytrope p = K rho^Gad  =>  w(rho) = 1 + (w0-1) rho^(Gad-1).
  Bernoulli: Gamma(rho) = w0 / w(rho); mass flux rho*Gamma*beta*A = const  =>  A(rho) ∝ 1/(rho u),
  u = Gamma*beta. A(rho) has a single minimum = the throat (transonic point); the supersonic branch
  (rho below the throat) is tabulated on a log grid; Gamma is read off at given area ratios A/A*.
  Checks: beta at the throat equals the sound speed c_s^2 = (Gad-1)(w-1)/w; Gamma -> w0 as A -> inf.
EXPECTED OUTPUT: Gamma_inf = w0 (to the grid limit); throat Mach 1; area ratio needed to reach 90% of
  w0; opening angle 1/Gamma in degrees.
Deterministic, numpy only.
"""
import numpy as np

GAD = 4.0 / 3.0

def nozzle(w0, gad=GAD, n=400001):
    rho = np.logspace(-30, np.log10(1 - 1e-12), n)
    w = 1 + (w0 - 1) * rho ** (gad - 1)
    G = w0 / w
    u = np.sqrt(np.maximum(G * G - 1, 1e-300))
    A = 1.0 / (rho * u)
    return rho, w, G, u, A

if __name__ == "__main__":
    print("=== ch_jet_acceleration: relativistic de Laval nozzle, Bernoulli Gamma*w = w0 ===")
    print(f"Gad = {GAD:.4f}, Gamma0 -> 1, c = 1\n")
    print("  w0     throat: Gamma*  beta*/c_s   A/A* for 0.9 w0   Gamma(A/A*=1e2,1e4,1e8)       Gamma_inf/w0   1/Gamma_inf [deg]")
    rows = []
    for w0 in [10.0, 100.0, 1000.0]:
        rho, w, G, u, A = nozzle(w0)
        i = np.argmin(A); As = A[i]
        cs = np.sqrt((GAD - 1) * (w[i] - 1) / w[i]); beta_t = u[i] / G[i]
        sup = slice(0, i + 1)                          # supersonic branch: rho < rho_throat
        Ar = A[sup][::-1] / As; Gs = G[sup][::-1]      # increasing area ratio
        g_at = [np.interp(np.log(a), np.log(Ar), Gs) for a in (1e2, 1e4, 1e8)]
        a90 = np.exp(np.interp(0.9 * w0, Gs, np.log(Ar)))
        Ginf = G[0]
        th = np.degrees(1 / Ginf)
        rows.append((w0, Ginf, th, a90))
        print(f"  {w0:6.0f}  {G[i]:8.3f}  {beta_t/cs:9.5f}   {a90:14.3e}   "
              f"{g_at[0]:8.2f} {g_at[1]:8.2f} {g_at[2]:8.2f}   {Ginf/w0:10.6f}   {th:10.4f}")
    print("\n  -> Gamma_inf = w0 reproduced (Bernoulli; exact as w -> 1). Throat is sonic (beta*/c_s = 1).")
    print("  -> for a conical funnel (A ∝ r^2) Gamma grows ∝ A^{1/2} ∝ r until saturation; radius to reach")
    print("     0.9 w0: r/r* = sqrt(A/A*) = " + ", ".join(f"{np.sqrt(r[3]):.0f} (w0={r[0]:.0f})" for r in rows)
          + "  i.e. ~15-18 w0 throat radii.\n")

    print("HONEST READING")
    print("  * Gamma_inf = w0 is an identity of the Bernoulli invariant; choosing w0 = 10 / 1e2-1e3 to")
    print("    'recover' AGN / GRB Lorentz factors is an input choice, not a prediction. The loading of")
    print("    w0 (the only physical content) is open, exactly as the page says.")
    print("  * Opening angles: 1/Gamma = %.1f deg (w0=10), %.2f deg (1e2), %.3f deg (1e3)." %
          tuple(r[2] for r in rows))
    print("    AGN: observed Gamma*theta_j ~ 0.13 (Pushkarev+2009), i.e. theta_j ~ 0.13/Gamma < 1/Gamma.")
    print("    GRB: observed jet half-angles ~2-10 deg >> 1/Gamma ~ 0.06-0.6 deg. So 1/Gamma is the causal")
    print("    (beaming) angle, not the measured jet opening angle; 'matching what is seen' holds only for")
    print("    the order of magnitude at AGN and does NOT hold for GRB jet angles.")
    print("  * Magnetized bases (sigma) and the Blandford-Znajek/Payne analogue are not modelled.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        plt.figure(figsize=(6, 4))
        for w0 in [10.0, 100.0, 1000.0]:
            rho, w, G, u, A = nozzle(w0, n=40001); i = np.argmin(A)
            plt.loglog(A[:i + 1] / A[i], G[:i + 1], label=f"w0={w0:.0f}")
        plt.xlabel("A/A* (supersonic branch)"); plt.ylabel("Gamma"); plt.legend(); plt.tight_layout()
        plt.savefig("ch_jet_acceleration.png", dpi=110); print("\n[figure written: ch_jet_acceleration.png]")
    except Exception as e:
        print(f"[matplotlib unavailable: {e}]")
