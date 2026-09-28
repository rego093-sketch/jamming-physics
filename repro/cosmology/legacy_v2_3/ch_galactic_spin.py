#!/usr/bin/env python3
"""
ch_galactic_spin.py -- TRANSPARENT test: does the galactic one-sided inflow set or correct
planetary rotation/revolution?  Built for full parameter transparency (project honesty gates):
EVERY galactic-inflow knob is disclosed, and the FREE/tunable ones are flagged explicitly so
they cannot hide. Transparency is the point: the galactic inflow is easy to tune, so its value
and effect must be open, or a tuned fit could masquerade as a prediction.

RESULT: the galactic inflow at the Sun is a near-UNIFORM field (~MOND a0 scale) -> NO internal
effect on the solar system (equivalence principle). Only its tidal GRADIENT acts internally, and
that is ~1e-12 to 1e-18 of the Sun's tidal effect on each planet -> NEGLIGIBLE at every planet.
So it cannot set Venus's retrograde spin, Uranus's tilt, or improve orbital accuracy; those are
LOCAL (Sun's inflow + accretion/impact history). Planetary spins are ACCOMMODATED, not predicted,
by accretion history (Ch5 Part A). The knob is easy to tune but the honest value makes it irrelevant.
DEPENDENCIES: numpy, matplotlib.
"""
import numpy as np

# ===================== DISCLOSED PARAMETERS (galactic inflow) =====================
# MEASURED (not free):
V_GAL = 220e3                 # m/s   solar orbital speed about the galactic centre (measured)
R_GAL = 8.0*3.086e19          # m     galactocentric radius ~8 kpc (measured)
# FREE / TUNABLE knobs -- disclosed so they cannot hide:
PASS_THROUGH_FRAC = 0.0       # [FREE] extra "passing-through" inflow as a fraction of V_GAL^2/R_GAL
                              #        (medium continuing through the Galaxy toward its centre).
                              #        Scales the UNIFORM field only -> still no internal effect.
EXTRA_GAL_TIDE    = 0.0       # [FREE] any extra galactic tidal GRADIENT (s^-2) one wishes to assert.
                              #        This is the ONLY quantity that could act internally.
# ==================================================================================

G=6.674e-11; Msun=1.989e30; AU=1.496e11

PLANETS = {  # a[AU], spin period[d] (neg=retrograde), obliquity[deg]
 "Mercury": (0.387,  58.6,   0.03), "Venus":  (0.723,-243.0, 177.4),
 "Earth":   (1.000,   1.00,  23.4), "Mars":   (1.524,   1.03,  25.2),
 "Jupiter": (5.203,   0.41,   3.1), "Saturn": (9.537,   0.44,  26.7),
 "Uranus":  (19.19,  -0.72,  97.8), "Neptune":(30.07,   0.67,  28.3)}

if __name__ == "__main__":
    Omega = V_GAL/R_GAL
    a_gal = V_GAL**2/R_GAL*(1+PASS_THROUGH_FRAC)
    tide  = Omega**2 + EXTRA_GAL_TIDE
    print("=== TRANSPARENT galactic-inflow test for planetary spin/revolution ===\n")
    print("DISCLOSED galactic parameters:")
    print(f"  V_GAL={V_GAL/1e3:.0f} km/s (measured),  R_GAL={R_GAL/3.086e19:.1f} kpc (measured)")
    print(f"  [FREE] PASS_THROUGH_FRAC={PASS_THROUGH_FRAC},  [FREE] EXTRA_GAL_TIDE={EXTRA_GAL_TIDE} s^-2")
    print(f"  -> Omega_gal={Omega:.2e}/s;  a_gal(at Sun)={a_gal:.2e} m/s^2 (~MOND a0 scale);  galactic tide={tide:.2e}/s^2")
    print("  KEY: a_gal is near-UNIFORM across the solar system -> NO internal effect (equivalence")
    print("       principle). Only the tidal GRADIENT acts internally.\n")
    print(f"  {'planet':9}{'spin(d)':>9}{'obliq':>7}   {'solar tide/s^2':>15}   {'gal/solar tide':>15}")
    ratios=[]
    for n,(a,P,ob) in PLANETS.items():
        st=G*Msun/(a*AU)**3; r=tide/st; ratios.append((n,r))
        print(f"  {n:9}{P:9.2f}{ob:7.1f}   {st:15.2e}   {r:15.1e}")
    worst=max(ratios,key=lambda x:x[1])
    print(f"\n  largest gal/solar tidal ratio: {worst[0]} = {worst[1]:.1e}  -> NEGLIGIBLE at every planet.")
    print("  obliquities span 0-177 deg with no common alignment: observed spins are UNcorrelated")
    print("  with the single galactic direction -> a galactic field is NOT setting them.\n")
    print("TUNING WARNING (transparency): to make the galactic tide rival the Sun's at Earth one must")
    print(f"  set EXTRA_GAL_TIDE ~ 4e-14 s^-2 -- about {4e-14/Omega**2:.0e}x the measured galactic tide,")
    print("  which is unphysical. The knob is easy to tune; the honest value (~1e-30 s^-2) makes it")
    print("  irrelevant, so any 'fit' of planetary spins to galactic inflow would be tuning, not physics.\n")
    print("FRAMEWORK STATUS (honest): planetary spins are ACCOMMODATED, not predicted, by accretion")
    print("  history (Ch5 Part A: intrinsic spin = accreted swirl). Venus retrograde = retrograde")
    print("  accretion swirl (a free input); the Moon's 1:1 lock is shown (Ch5 Part B); Mercury's 3:2")
    print("  is reproduced (Ch5 Part D). The galactic inflow adds nothing measurable to planetary spin.")
    print("  NB (fairness): the galactic tide IS non-negligible for the Oort cloud (wide orbits), just not planets.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        names=[n for n,_ in ratios]; vals=[r for _,r in ratios]
        fig,ax=plt.subplots(figsize=(9,4.2))
        ax.bar(names, vals, color="#185FA5")
        ax.axhline(1.0, ls="--", color="#D85A30", lw=1.4)
        ax.text(0.1, 1.5, "ratio = 1 (would matter)", color="#D85A30", fontsize=9)
        ax.set_yscale("log"); ax.set_ylim(1e-19,1e1)
        ax.set_ylabel("galactic tide / solar tide"); ax.set_title("Galactic one-sided inflow vs the Sun's tidal effect on each planet (transparent)")
        plt.tight_layout(); plt.savefig("ch_galactic_spin.png", dpi=110, bbox_inches="tight")
        print("\n[figure written: ch_galactic_spin.png]")
    except Exception as e:
        print(f"[matplotlib unavailable: {e}]")
