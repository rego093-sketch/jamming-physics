#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cochlear_amplifier.py  --  The cochlear active process as a HOPF critical oscillator.

The cochlea poises each local element at a Hopf bifurcation to obtain its four signature properties at
once: amplification, sharp tuning, COMPRESSIVE nonlinearity, and spontaneous otoacoustic emission. This
is the well-established physics of hearing (Camalet/Duke/Julicher/Prost 2000 PNAS 97:3183; Eguiluz/Ochoa/
Magnasco 2000 PRL 84:5232; Hudspeth/Julicher/Martin 2010 J Neurophysiol 104:1219; Reichenbach & Hudspeth
2014 Rep Prog Phys 77:076601). The active force comes from outer-hair-cell prestin electromotility
(SLC26A5, NCBI Gene 375611; UniProt P58743) and/or active hair-bundle motility.

Normal form (forcing at resonance w0):  dz/dt = (mu + i*w0) z - beta |z|^2 z + F e^{i w0 t}
Writing z = R e^{i w0 t}, the response amplitude R obeys at steady state:  mu R - beta R^3 + F = 0
  (the i*w0 carrier cancels; the dominant nonlinearity is CUBIC and phase-invariant -- no quadratic term).
  - AT CRITICALITY (mu = 0):   beta R^3 = F   ->   R = (F/beta)^{1/3}    => R ~ F^{1/3}  (CUBE-ROOT compression)
  - SUBCRITICAL  (mu < 0):     small F: R ~ F/|mu| (LINEAR, high gain);  large F: R ~ (F/beta)^{1/3}

KEY POINT (VP no-tuning): the compression EXPONENT 1/3 is NOT fitted -- it is a parameter-free consequence
of the cubic normal form evaluated at the bifurcation. beta only sets the amplitude UNIT (set to 1 WLOG);
mu = 0 IS the criticality hypothesis, not a tuned knob. We SWEEP mu from 0 (critical) into the stable
region and F over decades, and read the local log-log slope. The cited empirical anchor is the ~0.3-0.5
basilar-membrane compression exponent (mapped [L]); the model delivers exactly 1/3 at criticality [V].

Grades: cube-root exponent at criticality [V] (parameter-free) ; cited BM compression exponent [L].
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
import numpy as np
from vp_substrate import seed_everything


def _hopf_amplitude(mu, F, w0=1.0, beta=1.0):
    """Steady response amplitude R of the Hopf normal form forced at resonance.

    R solves the depressed cubic  beta R^3 - mu R - F = 0  (R > 0). Solved deterministically by taking
    the unique positive real root (no integration, no RNG)."""
    # beta R^3 - mu R - F = 0  ->  R^3 + p R + q = 0 with p = -mu/beta, q = -F/beta
    p = -mu / beta
    q = -F / beta
    roots = np.roots([1.0, 0.0, p, q])
    real = [r.real for r in roots if abs(r.imag) < 1e-9 and r.real > 0]
    if not real:
        # fall back to the root with the smallest imaginary part, positive real
        real = [max(r.real, 0.0) for r in roots]
    return float(max(real))


def compression_exponent(mu, F_decades=(-4.0, 0.0), n=25, w0=1.0, beta=1.0):
    """Local log-log slope d log R / d log F over the given forcing-decade window, at fixed mu."""
    F = np.logspace(F_decades[0], F_decades[1], n)
    R = np.array([_hopf_amplitude(mu, float(f), w0=w0, beta=beta) for f in F])
    slope = float(np.polyfit(np.log10(F), np.log10(R), 1)[0])
    return slope


def verify_amplifier():
    """Verify the parameter-free predictions:
       (1) at criticality mu=0 the small-signal compression exponent ~ 1/3 (cube root);
       (2) far below criticality (mu strongly negative) the small-signal response is ~ linear (slope ~ 1);
       (3) gain (R/F) at small F grows as mu -> 0 (the amplifier).
    """
    seed_everything()
    # (1) criticality: exponent over the small-signal window
    crit_slope = compression_exponent(mu=0.0, F_decades=(-5.0, -1.0))
    # (2) deep subcritical: linear small-signal response
    lin_slope = compression_exponent(mu=-1.0, F_decades=(-5.0, -3.0))
    # (3) gain at a small probe force as criticality is approached
    F_probe = 1e-4
    gains = {}
    for mu in (-1.0, -1e-1, -1e-2, 0.0):
        R = _hopf_amplitude(mu, F_probe)
        gains["mu=%g" % mu] = round(R / F_probe, 4)
    cube_root_ok = bool(abs(crit_slope - 1.0 / 3.0) < 0.03)
    linear_ok = bool(abs(lin_slope - 1.0) < 0.05)
    gain_rises = bool(gains["mu=0"] > gains["mu=-1"])
    return dict(
        critical_compression_exponent=round(crit_slope, 4),
        expected_at_criticality=round(1.0 / 3.0, 4),
        cube_root_compression_ok=cube_root_ok,
        subcritical_smallsignal_slope=round(lin_slope, 4),
        linear_offcriticality_ok=linear_ok,
        smallsignal_gain_vs_mu=gains, gain_rises_toward_criticality=gain_rises,
        cited_BM_compression_exponent="~0.3-0.5 (mapped [L]; model gives exactly 1/3 at the bifurcation [V])",
        active_force_gene=("SLC26A5/prestin", "NCBI Gene 375611; UniProt P58743"),
        grade="[V] exponent parameter-free at criticality ; [L] cited compression range",
        pass_=bool(cube_root_ok and linear_ok and gain_rises),
    )


if __name__ == "__main__":
    import json
    print(json.dumps(verify_amplifier(), ensure_ascii=False, indent=2))
