#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
barrier_therapeutics.py  --  Circulatory Transport ONCOLOGY, therapeutic-target layer.

This module does NOT add a new mechanism. It reads consequences of the SAME R19 carcinogenesis
kernel already derived in carcinogen_dose_response.py (cell fate = bistable switch
ds/dt = g*s - s^3 + h; carcinogen = sustained drive h lowering the escape barrier; malignant
crossing = Kramers escape). The question here is the one the dose-response layer does not ask:
once the substrate view is taken seriously, what does it predict about REVERSING the malignant
transition -- i.e. about treatment and prevention?

Four forced/derived consequences (each turned into a discriminant T18-T21):

  T18  REVERSIBILITY THRESHOLD = the spinodal.  A driven pre-malignant cell, on removal of the
       drive, relaxes back to the healthy basin IF AND ONLY IF the drive stayed below the spinodal
       h_sp = 2(g/3)^1.5.  Past h_sp the healthy basin has annihilated: the cell has fallen into the
       malignant basin and drive-removal alone cannot retrieve it.  => a SHARP responder boundary
       for de-driving / differentiation therapy, set by how far past threshold the lesion was driven.

  T19  CRITICAL SLOWING near the threshold.  The healthy-basin relaxation rate is the eigenvalue
       lambda(h) = g - 3 s_h(h)^2 -> 0 as h -> h_sp (saddle-node), so the reversion time
       tau = 1/|lambda| diverges with the universal fold exponent 1/2: tau ~ (h_sp - h)^(-1/2).
       => pre-malignant lesions near threshold revert SLOWLY and are marginally stable (relapse-prone).

  T20  SYNERGY REVERSAL (de-escalation).  Because additive barrier decrements make risks multiply
       (RR_comb = RR_a*RR_v, the headline T7 result), REMOVING one of two synergistic drivers
       DIVIDES the combined risk by that driver's RR -- a multiplicative, not additive, benefit.
       For aflatoxin x HBV this predicts that eliminating HBV cuts risk ~11x, not ~1.2x as additive
       thinking expects -- matching the large observed benefit of HBV control in aflatoxin regions.

  T21  BARRIER-RESTORATION LEVERAGE.  The crossing rate is k = k0*exp(-barrier/D), so raising the
       effective barrier by delta suppresses the malignant-crossing rate by exp(-delta/D):
       EXPONENTIAL leverage, d(ln k)/d(delta) = -1/D.  => small reductions in carcinogen drive
       (prevention) and partial barrier-restoring agents suppress transition exponentially; this is
       the quantitative reason prevention dominates cure.

HONEST BOUNDARY (read before citing).  Bistable cell-fate landscapes (Waddington; Huang & Kauffman)
and the reversion logic behind differentiation therapy (APL/ATRA; IDH inhibitors in AML and glioma)
are ESTABLISHED systems biology -- the *reversion-on-drive-removal* idea is NOT new here. What this
package adds, and what is therefore the falsifiable burden, is QUANTITATIVE: (a) the escape barrier
equals g^2/4 read from the MEASURED master-gene promoter stacking energy g (a claim that cell-fate
barrier height scales with NN-stacking dG37), and (b) the spinodal is a SHARP irreversibility
threshold with a 1/2 critical exponent.  The de-escalation result (T20) is the most robust (an
epidemiological retrodiction); the barrier=g^2/4 grounding is the weakest link and is graded [O]/[H]
with a stated obstacle (no direct measurement linking promoter stacking energy to a cell-fate
barrier).  Nothing here is clinical advice; these are testable mechanistic predictions / target
hypotheses.

GRADES (C3): the dynamics on the double well are forced [F] and verified in simulation [V]; the
de-escalation magnitude is [V] vs cited epidemiology [L]; the THERAPEUTIC interpretation is a
prediction [H]; the absolute drive<->exposure mapping and the barrier=g^2/4 biological grounding are
[O] with stated obstacles.
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
import numpy as np
from vp_substrate import sdot, spinodal, barrier, seed_everything

GAMMA_KIDNEY = 1.5556   # SIX2 (RCC), measured NN-stacking dG37; read-only
GAMMA_LIVER  = 1.525    # HHEX (HCC), measured; read-only


# ---------------------------------------------------------------------------
#  Reversion dynamics on the R19 double well (forced [F], simulated [V])
# ---------------------------------------------------------------------------
def reversion_after_drive(gamma, h_c, expo_steps=6000, relax_steps=6000, dt=0.02):
    """Start a cell in the healthy basin (s = -sqrt(g)), apply carcinogen drive h_c for an exposure
    window, then REMOVE the drive (h=0) and relax. Returns the exposed and final states and whether
    the cell reverted to the healthy basin (s_final < 0)."""
    g = float(gamma)
    s = -math.sqrt(g)
    for _ in range(expo_steps):
        s += dt * sdot(s, g, h_c)
    s_exposed = s
    for _ in range(relax_steps):
        s += dt * sdot(s, g, 0.0)
    return {"s_exposed": float(s_exposed), "s_final": float(s), "reverted": bool(s < 0.0)}


def reversibility_threshold(gamma, lo=0.40, hi=0.98, n=80):
    """Smallest drive at which a driven cell no longer reverts on drive-removal (bisection-style
    sweep). The R19 landscape forces this to equal the spinodal h_sp = 2(g/3)^1.5."""
    g = float(gamma)
    hs = np.linspace(lo, hi, n)
    rev = [reversion_after_drive(g, float(h))["reverted"] for h in hs]
    for i in range(len(hs) - 1):
        if rev[i] and not rev[i + 1]:
            return 0.5 * (hs[i] + hs[i + 1])
    return None


def healthy_root(gamma, h):
    """The metastable (healthy) fixed point: the outer root opposite a positive drive."""
    g = float(gamma)
    roots = np.roots([1.0, 0.0, -g, -h])
    real = sorted(r.real for r in roots if abs(r.imag) < 1e-9)
    return real[0] if len(real) == 3 else None     # negative (healthy) root for h>0


def healthy_relaxation_tau(gamma, h):
    """Reversion time of the healthy basin = 1/|lambda|, lambda = g - 3 s_h^2 (the linearised
    R19 eigenvalue). Diverges as h -> spinodal (critical slowing)."""
    g = float(gamma)
    s_h = healthy_root(g, h)
    if s_h is None:
        return float("inf")
    lam = g - 3.0 * s_h * s_h
    return 1.0 / abs(lam) if lam != 0 else float("inf")


def barrier_restoration_suppression(delta, D):
    """Crossing-rate suppression factor when the effective barrier is RAISED by delta:
    k(b+delta)/k(b) = exp(-delta/D). Exponential leverage."""
    return math.exp(-float(delta) / float(D))


if __name__ == "__main__":
    for nm, g in [("RCC", GAMMA_KIDNEY), ("HCC", GAMMA_LIVER)]:
        print(nm, "spinodal", round(spinodal(g), 5),
              "reversibility threshold", round(reversibility_threshold(g), 5))
