#!/usr/bin/env python3
"""
ch3_gate.py  --  Chapter 3, GATE PHYSICS: saturation, the flux bound, and an
emergent critical radius from choking.

WHAT THIS DEMONSTRATES (and what it does NOT)
---------------------------------------------
Chapter 3 imports from the physics volume a two-channel gravity in which the
contact/restoring channel SATURATES at a yield value g_star = c^2 Psi_yield, and
the inflow reaching the wave speed defines a black-hole critical radius. Both
were *delegated* (stated, not shown). The cosmos-volume PART 08 ("Gate Physics:
Critical Radius, Choking, Saturation, Throughput") gives the minimal mechanism,
and this script SHOWS it:

  (1) Saturation (PART 08 sec.8.2):  the active->stored conversion rate is
        Gamma = Gamma_max * g(e_a),   g:[0,1]->[0,1],  g(0)=0,
      with e.g. the Hill family  g_Hill(e_a) = e_a^n / (K_Gamma^n + e_a^n).
      => Gamma cannot exceed Gamma_max: the restoring channel SATURATES (g_star).

  (2) Flux bound (PART 08 Prop. 8.1):  a microscopic speed limit ||v|| <= c forces
        ||S|| <= c * e_a      =>   mean transport velocity  u := S/e_a <= c.

  (3) Emergent critical radius (PART 08 sec.8.3.5):  for an inverse-square drive
      |F_r| = K_F / r^2 and demand u_dem = |F_r|/B = K_F/(B r^2), choking
      (demand exceeds the flux capacity, u_dem > c) sets in inside
        r_ch = sqrt( K_F / (B c) ).
      Inside r_ch the flow is CHOKED: the transport velocity saturates at c
      (u = min(u_dem, c)) and the choking ratio chi_S = u_dem/c >= 1. This is the
      "inflow reaches the wave speed" choke point -- a horizon-like critical
      radius produced *solely* by a flux capacity bound.

HONEST SCOPE (this is a MECHANISM demo, not a fit / not a proof):
  - normalised/toy units (c = B = K_F = 1 so that r_ch = 1); c, K_F, B, K_Gamma, n
    are INPUTS, not derived;
  - it does NOT derive the absolute value of G / g_star (the "four-wall" question
    stays OPEN), nor the Schwarzschild coefficient R_s = 2GM/c^2 (that scaling
    comes from the *geometric* channel / strong-field completion in the physics
    volume; here the inverse-square *choke* radius scales as r_ch ~ sqrt(K_F));
  - the EXISTENCE of a critical radius where u = c (a horizon-like choke) and the
    saturation ceiling are DEGENERATE in outcome with the standard horizon and a
    capped restoring force; the distinguishing content is the *mechanism*
    (a throughput choke with a finite, non-singular interior).

INPUTS: none fitted. DEPENDENCIES: numpy (matplotlib optional). NO RNG.
"""

import numpy as np

# ----------------------------------------------------------------------
# Normalised units: speed limit c, demand stiffness B, inverse-square strength K_F.
# Choose c = B = K_F = 1 so the analytic choke radius r_ch = sqrt(K_F/(B c)) = 1.
# ----------------------------------------------------------------------
c   = 1.0      # microscopic speed limit (emergent maximal transport speed)
B   = 1.0      # demand stiffness in S_dem ~ (e_a/B) F_r
K_F = 1.0      # inverse-square drive strength, |F_r| = K_F / r^2
r_ch_analytic = np.sqrt(K_F / (B * c))          # PART 08 eq. 8.3.5 (inverse square)

# ---- (1) saturation families g(e_a) (PART 08 sec.8.2.3-8.2.4) ----
K_Gamma = 1.0                                    # half-saturation scale
e_a = np.linspace(0.0, 5.0 * K_Gamma, 1200)      # active energy density
def g_hill(x, n):     return x**n / (K_Gamma**n + x**n)
def g_exp(x):         return 1.0 - np.exp(-x / K_Gamma)
g_h1, g_h2, g_h4 = g_hill(e_a, 1), g_hill(e_a, 2), g_hill(e_a, 4)
g_e              = g_exp(e_a)
SAT_GATE = 0.9                                   # "effectively saturated" threshold

# ---- (2)+(3) radial demand, flux cap, choke (PART 08 Prop.8.1 + sec.8.3.5) ----
r       = np.linspace(0.20, 3.0, 1400)
u_dem   = K_F / (B * r**2)                        # demanded transport velocity ~ 1/r^2
u_act   = np.minimum(u_dem, c)                    # flux-limited (choked) velocity, <= c
chi_S   = u_dem / c                               # choking ratio (admissible if <= 1)
# spherical throughput J = 4 pi r^2 u e_a, with e_a constant (set 1) for the diagnostic
e_a_r   = np.ones_like(r)
J_dem   = 4*np.pi * r**2 * u_dem * e_a_r          # what demand would carry (unbounded inward)
J_act   = 4*np.pi * r**2 * u_act * e_a_r          # actual, capacity-limited throughput

# measured choke radius = where u_dem crosses c
i_cross = int(np.argmin(np.abs(u_dem - c)))
r_ch_meas = r[i_cross]

# closure (trace) bound from the same speed limit (PART 08 sec.8.4.3, CL-ISO)
kappaT_max = c**2 / 3.0

# ----------------------------------------------------------------------
print("=== gate physics: saturation, flux bound, emergent critical radius (PART 08) ===")
print(f"  speed limit c = {c};  demand stiffness B = {B};  drive K_F = {K_F}")
print(f"  flux bound (Prop.8.1):  ||S|| <= c*e_a  =>  u = S/e_a <= c   (max u_act = {u_act.max():.3f} <= {c})")
print()
print("  (1) SATURATION  Gamma = Gamma_max * g(e_a),  g in [0,1], g(0)=0:")
print(f"      Hill n=2: g(0)={g_hill(0.0,2):.3f},  g(K_Gamma)={g_hill(K_Gamma,2):.3f} (half-sat),"
      f"  g(5K_Gamma)={g_hill(5*K_Gamma,2):.3f} -> 1 (= g_star ceiling)")
print(f"      all families bounded in [0,1]:  "
      f"{np.all((g_h1>=0)&(g_h1<=1)&(g_h2>=0)&(g_h2<=1)&(g_h4>=0)&(g_h4<=1)&(g_e>=0)&(g_e<=1))}")
e_sat = e_a[np.argmax(g_h2 >= SAT_GATE)]
print(f"      saturation gate (g_Hill,n=2 >= {SAT_GATE}) turns on at e_a = {e_sat:.2f} K_Gamma")
print()
print("  (3) EMERGENT CRITICAL RADIUS from choking (inverse-square drive):")
print(f"      r_ch = sqrt(K_F/(B c)) = {r_ch_analytic:.3f}  (analytic),  {r_ch_meas:.3f}  (measured, u_dem=c)")
print(f"      match: {abs(r_ch_analytic - r_ch_meas) < 2*(r[1]-r[0])}  "
      f"=> inner choked zone r<r_ch (u=c, chi_S>=1), outer unchoked r>r_ch")
print(f"      choking ratio at r_ch: chi_S = {chi_S[i_cross]:.3f} (=1 at the boundary)")
print(f"      closure bound from same c (CL-ISO): kappa_T <= c^2/3 = {kappaT_max:.3f}")
print()
print("  EXPECTED: g(e_a) rises 0 -> 1 (conversion rate saturates at Gamma_max = g_star);")
print("            u_dem ~ 1/r^2 crosses the cap c at r_ch, giving a choked interior.")
print("  SCOPE: mechanism shown in toy units; NOT a derivation of G's absolute value")
print("         or of R_s=2GM/c^2. Critical-radius existence is degenerate with the")
print("         standard horizon; the finite, non-singular choked interior distinguishes it.")

# ----------------------------------------------------------------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 3, figsize=(16, 4.8))

    # (a) saturation of the conversion rate
    ax[0].plot(e_a, g_h1, color="tab:blue",   lw=1.6, label=r"Hill $n=1$")
    ax[0].plot(e_a, g_h2, color="tab:green",  lw=2.0, label=r"Hill $n=2$")
    ax[0].plot(e_a, g_h4, color="tab:purple", lw=1.6, label=r"Hill $n=4$")
    ax[0].plot(e_a, g_e,  color="tab:orange", lw=1.4, ls="--", label="exponential")
    ax[0].axhline(1.0, color="k", ls=":", lw=1)
    ax[0].text(3.4, 1.02, r"$g_\star$ ceiling ($\Gamma\!\to\!\Gamma_{\max}$)", fontsize=8)
    ax[0].axhline(SAT_GATE, color="gray", ls=":", lw=0.8)
    ax[0].text(0.1, SAT_GATE+0.02, "saturation gate", color="gray", fontsize=8)
    ax[0].set_xlabel(r"active energy density $e_{\rm a}$  [units of $K_\Gamma$]")
    ax[0].set_ylabel(r"$g(e_{\rm a})=\Gamma/\Gamma_{\max}$")
    ax[0].set_title(r"(a) saturation: conversion rate $\to\Gamma_{\max}$ ($=g_\star$)")
    ax[0].set_ylim(0, 1.12); ax[0].legend(fontsize=8, loc="lower right")

    # (b) emergent critical radius: demand 1/r^2 vs the flux cap c
    ax[1].plot(r, u_dem, color="tab:red", lw=2.0, label=r"demand $u_{\rm dem}=K_F/(Br^2)$")
    ax[1].axhline(c, color="k", lw=1.6, label=r"flux cap $c$ ($|S|\leq c\,e_{\rm a}$)")
    ax[1].axvline(r_ch_analytic, color="tab:purple", ls="--", lw=1.2)
    ax[1].text(r_ch_analytic+0.05, c*2.2, r"$r_{\rm ch}=\sqrt{K_F/(Bc)}$",
               color="tab:purple", fontsize=9)
    ax[1].axvspan(r[0], r_ch_analytic, color="tab:red",  alpha=0.08)
    ax[1].axvspan(r_ch_analytic, r[-1], color="tab:green", alpha=0.08)
    ax[1].text(0.30, c*4.2, "choked\n(inner)", color="tab:red",  fontsize=8)
    ax[1].text(1.9,  c*4.2, "unchoked\n(outer)", color="tab:green", fontsize=8, ha="center")
    ax[1].set_yscale("log")
    ax[1].set_xlabel(r"radius $r$  [units of $r_{\rm ch}$]")
    ax[1].set_ylabel(r"transport velocity demand / cap")
    ax[1].set_title(r"(b) emergent critical radius: $u_{\rm dem}=c$ at $r_{\rm ch}$")
    ax[1].legend(fontsize=8, loc="upper right")

    # (c) actual (capacity-limited) velocity and choking ratio
    ax[2].plot(r, u_act, color="tab:blue", lw=2.0, label=r"actual $u=\min(u_{\rm dem},c)$")
    ax[2].plot(r, chi_S, color="tab:orange", lw=1.6, label=r"choking ratio $\chi_S=u_{\rm dem}/c$")
    ax[2].axhline(c, color="k", ls=":", lw=1)
    ax[2].axhline(1.0, color="gray", ls=":", lw=0.8)
    ax[2].axvline(r_ch_analytic, color="tab:purple", ls="--", lw=1.2)
    ax[2].text(r_ch_analytic+0.05, 2.6, r"$r_{\rm ch}$", color="tab:purple", fontsize=9)
    ax[2].text(0.30, 1.05, r"$u=c$ (choked, $\chi_S\!\geq\!1$)", color="tab:blue", fontsize=8)
    ax[2].set_ylim(0, 3.0)
    ax[2].set_xlabel(r"radius $r$  [units of $r_{\rm ch}$]")
    ax[2].set_ylabel(r"velocity (units of $c$) / ratio")
    ax[2].set_title(r"(c) choked interior: $u$ saturates at $c$, throughput capacity-limited")
    ax[2].legend(fontsize=8, loc="upper right")

    plt.tight_layout()
    plt.savefig("ch3_gate.png", dpi=120, bbox_inches="tight")
    print("\n[figure written: ch3_gate.png]")
except Exception as exc:        # matplotlib optional
    print(f"\n[matplotlib unavailable: {exc}]  numbers above are the result.")
