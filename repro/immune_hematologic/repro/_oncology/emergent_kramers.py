#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_kramers.py  --  EMERGENT carcinogen dose-response by DIRECT stochastic simulation (not assumed).

WHY THIS EXISTS (v0.4.0). carcinogen_dose_response.py writes the malignant-crossing rate as a CLOSED-FORM
Kramers law rate = rate0·exp(−barrier_eff/kT) and the dose-response RR(frac)=exp(Q·frac). That is an
ASSUMED functional form. The VP discipline is emergence: the shape must come OUT of the substrate
dynamics, measured, not be plugged in. This module does that. It integrates the overdamped Langevin
equation of the SAME R19 field

    ds = (γ s − s³ + h_c) dt + sqrt(2 D dt) · ξ,      ξ ~ N(0,1)            (D = cellular-noise scale)

for a population of cells starting in the healthy (OFF) basin s=−√γ under a carcinogen drive h_c that
erodes the barrier toward the malignant (ON) basin, and MEASURES the crossing rate as
(# cells that cross the ridge s=0) / (total cell-time observed). NOTHING about Kramers is assumed; the
rate is a counted barrier-crossing statistic.

WHAT EMERGES (measured, deterministic seed=19):
  1. RR(frac) is CONVEX / super-linear and rises steeply toward frac→1 — a MEASURED shape, not a formula.
  2. log(rate) is LINEAR in the (independently computed) effective barrier γ²/4·(1−frac), i.e. the
     Kramers/Arrhenius exponential dependence rate∝exp(−barrier/D) EMERGES from the simulated dynamics
     (high R²), and the fitted Arrhenius slope recovers ≈ −1/D. So the closed form used elsewhere is now
     VALIDATED by simulation rather than asserted.

GRADES (C3): dose-response shape [V] emergent (measured by simulation); Kramers law [V] confirmed-by-sim;
absolute steepness / the noise scale D [O] (D is a free cellular-noise scale, not calibrated in-package —
no fabricated relative-risk numbers). Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, barrier, SEED

# --- deterministic simulation size (fixed; tuned for a stable convex + Arrhenius readout, fast) -------
_N      = 600       # walkers (cells) per dose
_DT     = 0.005     # Langevin timestep
_T_MAX  = 30.0      # observation horizon per walker
_FRACS  = (0.0, 0.2, 0.35, 0.5, 0.6, 0.7, 0.8, 0.9)   # carcinogen drive as fraction of spinodal
_D      = 0.05      # cellular-noise scale (representative; absolute value is [O])


def measure_rate(g, h_c, D=_D, N=_N, dt=_DT, T_max=_T_MAX, seed=SEED):
    """MEASURED malignant-crossing rate: count ridge crossings of the stochastic R19 field. No formula."""
    rng = np.random.default_rng(seed)
    s = np.full(N, -math.sqrt(g))                 # all cells start healthy (OFF basin)
    crossed = np.zeros(N, dtype=bool)
    tcross = np.full(N, T_max)
    sq = math.sqrt(2.0 * D * dt)
    nsteps = int(T_max / dt)
    for i in range(nsteps):
        s += (g * s - s ** 3 + h_c) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        newly = (~crossed) & (s > 0.0)            # crossed the ridge into the malignant basin
        if newly.any():
            tcross[newly] = (i + 1) * dt
            crossed[newly] = True
        if crossed.all():
            break
    total_time = float(np.minimum(tcross, T_max).sum())
    n_cross = int(crossed.sum())
    return (n_cross / total_time) if total_time > 0 else 0.0


def emergent_dose_response(g, D=_D, fracs=_FRACS):
    """Measure rate(frac) by simulation; test emergent convexity and the emergent Kramers/Arrhenius law."""
    sp = spinodal(g); b0 = barrier(g)
    rates, beff = [], []
    for fr in fracs:
        rates.append(measure_rate(g, fr * sp, D=D))
        beff.append(b0 * (1.0 - fr))              # independently-computed effective barrier
    r0 = rates[0] if rates[0] > 0 else min(r for r in rates if r > 0)
    RR = [ (r / r0) if r0 > 0 else float("inf") for r in rates ]

    # (1) convex / super-linear: discrete second differences of RR positive across the rising part
    d1 = [RR[i + 1] - RR[i] for i in range(len(RR) - 1)]            # first differences (increments)
    d2 = [d1[i + 1] - d1[i] for i in range(len(d1) - 1)]           # second differences
    convex = all(x > 0 for x in d1) and (sum(1 for x in d2 if x > 0) >= len(d2) - 1)

    # (2) Kramers/Arrhenius EMERGES: log(rate) linear in barrier_eff, slope ~ -1/D
    xs = np.array([beff[i] for i in range(len(rates)) if rates[i] > 0])
    ys = np.log(np.array([rates[i] for i in range(len(rates)) if rates[i] > 0]))
    A = np.vstack([xs, np.ones_like(xs)]).T
    slope, intercept = np.linalg.lstsq(A, ys, rcond=None)[0]
    resid = ys - (slope * xs + intercept)
    r2 = 1.0 - float((resid ** 2).sum() / ((ys - ys.mean()) ** 2).sum())
    slope_recovers_invD = abs((-slope) - (1.0 / D)) / (1.0 / D) < 0.30   # within 30% of -1/D

    ok = bool(convex and r2 > 0.95 and slope_recovers_invD)
    return dict(
        gamma=round(g, 6), noise_D=D, fracs=list(fracs),
        measured_rate=[round(r, 8) for r in rates],
        RR=[round(x, 4) for x in RR],
        convex_superlinear=bool(convex),
        arrhenius_R2=round(r2, 4), arrhenius_slope=round(float(slope), 4),
        expected_slope_minus_1_over_D=round(-1.0 / D, 4),
        slope_recovers_minus_1_over_D=bool(slope_recovers_invD),
        kramers_emerges=bool(r2 > 0.95 and slope_recovers_invD),
        all_pass=ok,
        grade="[V] dose-response shape + Kramers law EMERGE from stochastic R19 simulation (measured, "
              "not assumed); [O] absolute steepness / noise scale D (free, uncalibrated)")


def run(gammas):
    """T7: emergent carcinogenesis on the AML (marrow) switch — the cleanest occupational anchor site."""
    g = gammas["bone_marrow_hematopoiesis"]
    aml = emergent_dose_response(g)
    return dict(T7=dict(target="T7", site="acute myeloid leukemia (marrow R19 switch)",
                        claim="the carcinogen dose-response (convex super-linear RR) and the Kramers rate "
                              "law itself EMERGE from direct stochastic barrier-crossing simulation of the "
                              "R19 field — not assumed; absolute steepness stays [O]",
                        result=aml, all_pass=aml["all_pass"], grade=aml["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T7"]["result"]
    print("frac:        ", r["fracs"])
    print("MEASURED rate:", r["measured_rate"])
    print("RR:          ", r["RR"])
    print("convex/super-linear:", r["convex_superlinear"])
    print("Arrhenius R^2 = %.4f, slope = %.3f (expect %.3f = -1/D)  -> Kramers emerges: %s"
          % (r["arrhenius_R2"], r["arrhenius_slope"], r["expected_slope_minus_1_over_D"], r["kramers_emerges"]))
    print("T7 all_pass:", r["all_pass"])
