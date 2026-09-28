#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch_accuracy_dashboard.py
========================
A TRANSPARENT "accuracy across scales" dashboard for the Earth-Cosmos volume.

WHAT THIS SCRIPT DOES
---------------------
For every quantitative observable the volume touches, it prints ONE row giving:

    inputs used (each tagged MEASURED / FREE / DERIVED)  |  predicted  |
    observed  |  % accuracy  |  honest label

grouped by physical scale.  It then writes a 2-panel figure (ch_accuracy_dashboard.png).

There is NO fitting in this script and NO new physics.  Every number is either
imported unchanged from the per-chapter scripts (ch4/ch5/ch6/ch_galactic_spin) or
follows from the pi-chain anchor (physics volume, DOI 10.5281/zenodo.17932566).
Wherever a number IS the result of a fit elsewhere (only the stellar M/L of NGC 2403),
that is stated explicitly and tagged FREE.

THE ONE HEADLINE YOU MUST READ FIRST (stated up front, by design)
----------------------------------------------------------------
The disclosed galactic variables (a_gal, Omega_gal, H0) solve the GALACTIC scale:
a0 = c*H0/2pi reproduces the empirical RAR/MOND acceleration to ~90% and fits the
NGC 2403 rotation curve with NO dark halo.  They do NOT solve planetary spins:
the galactic tide at the planets is 1e-18 ... 1e-13 of the Sun's tide -- negligible.
Planetary spins are ACCOMMODATED by local accretion history, not predicted, and the
galactic knob adds nothing measurable to them.  "Fitting" a planetary spin with the
galactic knob would mean tuning a parameter ~5e16x above its measured value: that is
tuning, not physics.  This script is built to make that distinction impossible to hide.

HONEST-LABEL LEGEND
-------------------
  predicted     : output of the framework with no parameter free to absorb the answer
  distinguishing: a real, testable difference from the standard account (a0 is the case)
  degenerate    : reproduces what Newton / MOND / LCDM already give (a consistency win)
  accommodated  : fit/explained AFTER the fact by a free input (not a prediction)
  negligible    : the variable is present but too small to matter (sized, not assumed)
  open          : not settled by a working calculation -> not claimed

Requires: numpy.  matplotlib optional (only for the figure).
Deterministic; no RNG; reproducible to machine precision.
"""

import numpy as np

# =====================================================================
#  DISCLOSED PARAMETERS  (every input, tagged)
#  ---------------------------------------------------------------
#  Tag meanings:  MEASURED = textbook/observed value (not tunable by us)
#                 DERIVED  = forced by the pi-chain / cosine integrals (not tunable)
#                 FREE     = a genuine free/fitted parameter (the honesty flags)
# =====================================================================

# --- universal constants -------------------------------------------------
c      = 2.99792458e8        # m/s     speed of light                       # MEASURED
G      = 6.674e-11           # m^3/kg/s^2  Newton constant                  # MEASURED
kpc    = 3.0857e19           # m       kiloparsec                           # MEASURED
AU     = 1.495978707e11      # m       astronomical unit                    # MEASURED
day    = 86400.0             # s                                            # MEASURED
GM_sun = 1.32712440018e20    # m^3/s^2 standard gravitational param of Sun  # MEASURED
#   NB: in the framework GM_sun = kappa*Q_sun (a LOCAL property of the Sun's
#   own inflow); only the product kappa*Q is physical (Ch3 result C).

# --- the framework's DERIVED full-cycle constant -------------------------
#   2pi = alpha/delta = (2/pi)/(1/pi^2), the ratio of the two cosine-integral
#   rectification constants (physics volume S5.1-5.2, S13.5.5).  This is the
#   SAME 2pi as in m_p/m_e = 6 pi^5 = 2 pi * 3 pi^4.  It is NOT a free factor.
alpha  = 2.0/np.pi                                   # = <|cos|>_full        # DERIVED
delta  = ((1.0/(2*np.pi))*2.0)**2                    # = (1/pi)^2 = 1/pi^2   # DERIVED
TWO_PI = alpha/delta                                 # = 2*pi (cos-derived)  # DERIVED

# --- Hubble constant (carries the well-known tension; we show the range) -
H0_kms = 70.0                # km/s/Mpc  baseline                           # MEASURED
H0_lo, H0_hi = 67.4, 73.0    # the tension band (Planck .. SH0ES)           # MEASURED
Mpc = 1.0e3*kpc              # m   1 Mpc = 1000 kpc                        # MEASURED
def H0_SI(H0):               # convert km/s/Mpc -> 1/s
    return H0*1000.0/Mpc

# --- galactic parameters of the Sun's orbit (the "galactic variables") ---
V_GAL  = 220e3               # m/s   Sun's circular speed about the centre  # MEASURED
R_GAL  = 8.0*kpc             # m     Sun's galactocentric radius            # MEASURED
#   two knobs that an over-eager fitter might reach for -- disclosed and set OFF:
PASS_THROUGH_FRAC = 0.0      # fraction of galactic inflow not near-uniform # FREE (=0)
EXTRA_GAL_TIDE    = 0.0      # s^-2  any ad-hoc extra galactic tide         # FREE (=0)

# --- the one genuinely fitted astrophysical parameter in the whole volume-
UPSILON_NGC2403 = 0.567      # disk stellar mass-to-light ratio (SPARC fit) # FREE (fitted)

# --- empirical comparison values ----------------------------------------
A0_RAR_OBS = 1.2e-10         # m/s^2  empirical RAR/MOND acceleration scale # MEASURED


def pct(pred, obs):
    """% accuracy = 100*(1 - |pred-obs|/|obs|), capped display at >=0."""
    return 100.0*(1.0 - abs(pred-obs)/abs(obs))


# =====================================================================
#  ROWS OF THE DASHBOARD
#  Each row: (scale, name, inputs_string, predicted, observed, unit,
#             accuracy_string, label)
#  accuracy_string is precomputed text so we can show ratios/ranges where a
#  bare percentage would be misleading (e.g. the negligible galactic tide).
# =====================================================================
rows = []

# ---------------------------------------------------------------------
#  SCALE 1 -- GALACTIC  (where the disclosed galactic variables do the work)
# ---------------------------------------------------------------------
a0_70 = c*H0_SI(H0_kms)/TWO_PI
a0_lo = c*H0_SI(H0_lo)/TWO_PI
a0_hi = c*H0_SI(H0_hi)/TWO_PI
rows.append((
    "GALACTIC", "a0 = c H0 / 2pi  (acceleration scale)",
    "c[M], H0[M], 2pi=alpha/delta[D]",
    a0_70, A0_RAR_OBS, "m/s^2",
    f"{pct(a0_70,A0_RAR_OBS):.0f}%  (band {pct(a0_lo,A0_RAR_OBS):.0f}-{pct(a0_hi,A0_RAR_OBS):.0f}% over H0=67-73)",
    "distinguishing"))

# NGC 2403 rotation-curve fit (numbers imported unchanged from ch6_galaxy_rar.py)
NGC_CHI2_DOF = 1.99
NGC_V_OBS, NGC_V_MODEL, NGC_V_BARYON = 134.4, 126.4, 52.8   # km/s, outer point
rows.append((
    "GALACTIC", "NGC 2403 outer rotation speed (no dark halo)",
    f"a0[D from above], Upsilon={UPSILON_NGC2403}[F fitted], baryons[M]",
    NGC_V_MODEL, NGC_V_OBS, "km/s",
    f"{pct(NGC_V_MODEL,NGC_V_OBS):.0f}%   chi^2/dof={NGC_CHI2_DOF}, N=73   (Newton-only gives {NGC_V_BARYON:.0f})",
    "degenerate"))     # curve shape degenerate w/ MOND/DM; the SCALE is the distinguishing part

# Baryonic Tully-Fisher slope (the deep-MOND limit v^4 = a0 G M)
rows.append((
    "GALACTIC", "BTFR slope  (v^4 = a0 G M, deep-MOND limit)",
    "a0[D], G[M], M_baryon[M]",
    4.0, 4.0, "power",
    "exact slope 4 by construction (amplitude uses a0)",
    "degenerate"))

# ---------------------------------------------------------------------
#  SCALE 2 -- SOLAR SYSTEM  (the Sun's LOCAL inflow, NOT galactic)
# ---------------------------------------------------------------------
#  Kepler check imported from ch4_solar_system.py (8 planets, one period each).
KEP_CONST   = 1.00001        # mean T^2/a^3 (theory 4pi^2/GM = 1.00000)
KEP_SCATTER = 9.62e-12
KEP_WORST_T = 0.73           # % worst-case period error (Saturn)
rows.append((
    "SOLAR-SYSTEM", "Kepler T^2/a^3  (8 planets, Sun's local inflow)",
    "GM_sun=kappa*Q_sun[M, LOCAL], a,e[M]",
    KEP_CONST, 1.00000, "",
    f"periods <= {KEP_WORST_T:.2f}%, speeds <= 0.7%, scatter {KEP_SCATTER:.0e}",
    "degenerate"))

# ---------------------------------------------------------------------
#  SCALE 3 -- SPINS & SATELLITES  (local accretion/tidal history)
# ---------------------------------------------------------------------
#  Moon 1:1 lock (ch5 part B/C)
MOON_RATIO = 1.000           # omega_spin/n driven 4 -> 1
rows.append((
    "SPIN/SAT", "Moon 1:1 tidal lock  (one face to Earth)",
    "tidal inflow gradient[M], no free knob",
    MOON_RATIO, 1.000, "spin/orbit",
    "omega_spin/n: 4 -> 1.000; tidal dg=4.88e-5=2GML/R^3 (within 0.02%)",
    "degenerate"))

#  Mercury 3:2 (ch5 part D) -- reproduced; capture PROBABILITY is the open piece
MERC_TURNS = 1.500           # turns per orbit at the 3:2 lock
rows.append((
    "SPIN/SAT", "Mercury 3:2 spin-orbit resonance",
    "e=0.206[M], inflow tidal torque[M]; triaxiality[F]",
    MERC_TURNS, 1.500, "turns/orbit",
    "p=1.5 dominant (|H|=0.65); libration 23.8 deg (bounded); trapped at e=0.206",
    "degenerate"))           # mechanism degenerate; capture probability -> see 'open' row

rows.append((
    "SPIN/SAT", "Mercury 3:2 capture PROBABILITY",
    "tidal model[F], triaxiality[F], history[unknown]",
    np.nan, np.nan, "",
    "model-dependent (~1e-4 with realistic triaxiality) -- not a forced prediction",
    "open"))

#  Venus retrograde -- accommodated by a free input (retrograde accretion swirl)
rows.append((
    "SPIN/SAT", "Venus retrograde spin (obliquity 177 deg)",
    "retrograde accretion swirl sign[F free input]",
    -1.0, -1.0, "spin sign",
    "sign reproduced IF swirl is retrograde -- a free input, not predicted",
    "accommodated"))

# ---------------------------------------------------------------------
#  THE HONEST KNOB -- the galactic tide ON the planets (sized, not assumed)
#  numbers reproduced from ch_galactic_spin.py
# ---------------------------------------------------------------------
Omega_gal = V_GAL/R_GAL                      # rad/s
a_gal     = V_GAL**2/R_GAL                   # m/s^2 (near-uniform => no internal effect)
gal_tide  = Omega_gal**2 + EXTRA_GAL_TIDE    # s^-2  (the tidal GRADIENT that DOES act)
# Sun's tidal field GM/r^3 at each planet, and the gal/solar ratio:
planet_r_AU = {"Mercury":0.387,"Venus":0.723,"Earth":1.000,"Mars":1.524,
               "Jupiter":5.203,"Saturn":9.537,"Uranus":19.19,"Neptune":30.07}
ratios = {}
for name, rAU in planet_r_AU.items():
    solar_tide = GM_sun/(rAU*AU)**3          # s^-2
    ratios[name] = gal_tide/solar_tide
ratio_min = min(ratios.values()); ratio_max = max(ratios.values())
tune_factor = (GM_sun/(1.0*AU)**3)/gal_tide  # x needed to rival Sun's tide at EARTH

rows.append((
    "GAL-KNOB", "Galactic tide acting on planetary spin",
    "V_gal[M], R_gal[M]; PASS_THROUGH[F=0], EXTRA_TIDE[F=0]",
    np.nan, np.nan, "",
    f"gal/solar tide = {ratio_min:.0e} (Mercury) .. {ratio_max:.0e} (Neptune): NEGLIGIBLE."
    f" Needs ~{tune_factor:.0e}x to matter at Earth (unphysical).",
    "negligible"))


# =====================================================================
#  PRINT THE DASHBOARD
# =====================================================================
print("="*94)
print(" VP EARTH-COSMOS  --  ACCURACY ACROSS SCALES (transparent dashboard)")
print("="*94)
print(" HEADLINE (up front, by design):")
print("   * The disclosed GALACTIC variables solve the GALACTIC scale:")
print(f"       a0 = c*H0/2pi = {a0_70:.3e} m/s^2  =  {pct(a0_70,A0_RAR_OBS):.0f}% of the empirical RAR scale,")
print( "       and fit NGC 2403 with NO dark halo (chi^2/dof=1.99).  2pi=alpha/delta is DERIVED.")
print( "   * They do NOT solve planetary spins: the galactic tide at the planets is")
print(f"       {ratio_min:.0e} .. {ratio_max:.0e} of the Sun's tide -- negligible.  Planetary spins are")
print( "       ACCOMMODATED by local accretion history, not predicted.  Tuning the galactic")
print(f"       knob to matter at Earth means ~{tune_factor:.0e}x its measured value = tuning, not physics.")
print("="*94)

hdr = f"{'scale':<13}{'observable':<46}{'predicted':>12}{'observed':>11}   {'%/note'}"
last_scale = None
print()
print(hdr); print("-"*120)
scale_pretty = {"GALACTIC":"GALACTIC","SOLAR-SYSTEM":"SOLAR-SYS","SPIN/SAT":"SPIN/SAT",
                "GAL-KNOB":"GAL-KNOB"}
for scale, name, inp, pred, obs, unit, acc, label in rows:
    if scale != last_scale:
        print(f"\n[{scale_pretty.get(scale,scale)}]")
        last_scale = scale
    ps = "  --" if (isinstance(pred,float) and np.isnan(pred)) else f"{pred:>12.5g}"
    os_ = "  --" if (isinstance(obs,float) and np.isnan(obs)) else f"{obs:>11.5g}"
    print(f"  {name:<44}{ps}{os_}   [{label}]")
    print(f"      inputs : {inp}")
    print(f"      note   : {acc}")

print()
print("-"*120)
print(" LABEL LEGEND: predicted | distinguishing(testable diff) | degenerate(=Newton/MOND/LCDM)"
      " | accommodated(free input) | negligible(sized) | open(not claimed)")
print(" Cross-checks: a0/NGC2403 match ch6_galaxy_rar.py; Kepler matches ch4_solar_system.py;")
print("               spins match ch5_spin_tidal.py; galactic tide matches ch_galactic_spin.py.")
print(" No fitting here; the only FREE astrophysical parameter in the volume is Upsilon(NGC2403)=0.567.")
print("="*94)


# =====================================================================
#  FIGURE  (optional; English labels only)
# =====================================================================
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    # ---- panel A: accuracy bars for the rows that HAVE a clean % ----
    barrows = [
        ("a0 = cH0/2pi (galactic scale)",        pct(a0_70, A0_RAR_OBS),    "distinguishing"),
        ("NGC 2403 outer speed",                 pct(NGC_V_MODEL,NGC_V_OBS),"degenerate"),
        ("Kepler T^2/a^3 (solar system)",        100.0 - KEP_WORST_T,       "degenerate"),
        ("Moon 1:1 lock",                        100.0,                     "degenerate"),
        ("Mercury 3:2 resonance",                100.0,                     "degenerate"),
        ("Venus retrograde sign",                100.0,                     "accommodated"),
    ]
    colors = {"distinguishing":"#1f77b4","degenerate":"#2ca02c",
              "accommodated":"#ff7f0e","negligible":"#d62728","open":"#7f7f7f"}
    names  = [r[0] for r in barrows][::-1]
    vals   = [r[1] for r in barrows][::-1]
    cols   = [colors[r[2]] for r in barrows][::-1]

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.5, 5.4))

    y = np.arange(len(names))
    axA.barh(y, vals, color=cols, edgecolor="black", height=0.6)
    axA.set_yticks(y); axA.set_yticklabels(names, fontsize=9)
    axA.set_xlim(0, 108)
    axA.axvline(100, color="black", lw=0.8, ls=":")
    axA.set_xlabel("accuracy vs observation  (%)")
    axA.set_title("(A) Accuracy across scales\n(green = degenerate / consistency; "
                  "blue = distinguishing; orange = accommodated)", fontsize=10)
    for yi, v in zip(y, vals):
        axA.text(min(v,100)+1.0, yi, f"{v:.0f}%", va="center", fontsize=8.5)
    leg = [Patch(facecolor=colors[k], edgecolor="black", label=k)
           for k in ["distinguishing","degenerate","accommodated"]]
    axA.legend(handles=leg, fontsize=8, loc="lower left", framealpha=0.9)

    # ---- panel B: the honest galactic knob -- gal/solar tide per planet ----
    pnames = list(planet_r_AU.keys())
    rr = [ratios[p] for p in pnames]
    xp = np.arange(len(pnames))
    axB.semilogy(xp, rr, "o-", color=colors["negligible"], lw=1.5, ms=6)
    axB.axhline(1.0, color="black", lw=1.0, ls="--")
    axB.text(len(pnames)-1, 1.4, "ratio = 1  (where it would matter)",
             ha="right", va="bottom", fontsize=8.5)
    axB.set_xticks(xp); axB.set_xticklabels(pnames, rotation=45, ha="right", fontsize=8.5)
    axB.set_ylabel("galactic tide / Sun's tide")
    axB.set_ylim(1e-19, 1e2)
    axB.set_title("(B) Where the galactic variables do NOT work\n"
                  "galactic tide on planetary spin is 1e-18 ... 1e-13 of the Sun's",
                  fontsize=10)
    # annotate the tuning gap at Earth
    earth_i = pnames.index("Earth")
    axB.annotate("", xy=(earth_i, 1.0), xytext=(earth_i, ratios["Earth"]),
                 arrowprops=dict(arrowstyle="<->", color="gray", lw=1.2))
    axB.text(earth_i+0.15, 1e-9, f"~{tune_factor:.0e}x\nto matter\n(unphysical)",
             fontsize=8, color="gray")

    fig.suptitle("VP Earth-Cosmos: a transparent accuracy dashboard "
                 "(galactic variables solve the galactic scale; planetary spins are local/accommodated)",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig("ch_accuracy_dashboard.png", dpi=150)
    print("[figure written: ch_accuracy_dashboard.png]")
except Exception as e:
    print(f"[figure skipped: {e}]")
