#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_memory.py  --  EMERGENT immune-memory lifetime by DIRECT stochastic simulation (not asserted).

WHY THIS EXISTS (v0.5.0). clonal_inflammation.py (T4) shows the ON state persists after antigen clears and
RANKS memory stability by the analytic barrier γ²/4. That ranking is asserted from the closed-form barrier.
The VP discipline is emergence: the durability ordering must come OUT of the substrate dynamics, MEASURED,
not read off a formula. This module does that. It integrates the overdamped Langevin equation of the SAME
R19 field for a cell sitting in the activated (ON) basin with the antigen drive removed,

    ds = (γ s − s³) dt + sqrt(2 D dt) · ξ,      ξ ~ N(0,1),     start ON at s = +√γ,   h = 0

and MEASURES the spontaneous escape rate back to the resting (OFF) basin as
(# cells that fall back across the ridge s=0) / (total cell-time observed) — the time-reversed twin of the
carcinogen crossing in emergent_kramers.py. The mean memory lifetime is the mean first-passage time
MFPT = 1/rate. NOTHING about Kramers is assumed; the rate is a counted barrier-crossing statistic.

WHAT EMERGES (measured, deterministic seed=19):
  1. The measured mean memory lifetime (MFPT) RANKS in ASCENDING γ across the four organs, i.e. the
     deeper-barrier (higher-γ) compartment holds memory longer — the durability ordering EMERGES from the
     dynamics, it is not asserted from γ²/4. The adaptive lymphoid compartment (largest barrier) is the
     most durable store, the marrow the least, MEASURED.
  2. log(escape-rate) is LINEAR in the barrier γ²/4 (high R²) with an Arrhenius slope ≈ −1/D, so the
     Kramers exponential dependence rate ∝ exp(−barrier/D) — equivalently lifetime ∝ exp(+barrier/D) —
     EMERGES from the simulated dynamics. The barrier-stability law used analytically in T4 is therefore
     VALIDATED by simulation rather than asserted.

GRADES (C3): durability ranking + barrier law [V] emergent (measured by simulation); the ABSOLUTE lifetime
(set by the cellular-noise scale D, the same free scale as T7) is [O] — no fabricated half-life numbers.
Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, barrier, SEED

_ORGANS = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]   # ascending-γ expectation

# --- deterministic simulation size (fixed; tuned for a stable ranking + Arrhenius readout, fast) -----
_N      = 1600      # walkers (memory cells) per organ
_DT     = 0.005     # Langevin timestep
_T_MAX  = 30.0      # observation horizon per walker (same SAME horizon for every organ — no per-organ tuning)
_D      = 0.15      # cellular-noise scale (representative; absolute value is [O])


def measure_escape_rate(g, D=_D, N=_N, dt=_DT, T_max=_T_MAX, seed=SEED):
    """MEASURED spontaneous escape rate: count ridge crossings ON->OFF of the stochastic R19 field. No formula."""
    rng = np.random.default_rng(seed)
    s = np.full(N, math.sqrt(g))                  # all cells start activated (ON basin), antigen removed (h=0)
    escaped = np.zeros(N, dtype=bool)
    tesc = np.full(N, T_max)
    sq = math.sqrt(2.0 * D * dt)
    nsteps = int(T_max / dt)
    for i in range(nsteps):
        s += (g * s - s ** 3) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        newly = (~escaped) & (s < 0.0)            # fell back across the ridge into the resting basin
        if newly.any():
            tesc[newly] = (i + 1) * dt
            escaped[newly] = True
        if escaped.all():
            break
    total_time = float(np.minimum(tesc, T_max).sum())
    n_esc = int(escaped.sum())
    return (n_esc / total_time) if total_time > 0 else 0.0


def emergent_memory_lifetime(gammas, D=_D):
    """Measure escape-rate (=1/MFPT) per organ by simulation; test emergent durability ranking + Kramers law."""
    rates, barr = {}, {}
    for o in _ORGANS:
        g = gammas[o]
        rates[o] = measure_escape_rate(g, D=D)
        barr[o]  = barrier(g)
    mfpt = {o: (1.0 / rates[o] if rates[o] > 0 else float("inf")) for o in _ORGANS}

    # (1) durability ranking EMERGES: ascending MFPT == ascending γ == ascending barrier
    order_mfpt  = sorted(_ORGANS, key=lambda o: mfpt[o])
    order_gamma = sorted(_ORGANS, key=lambda o: gammas[o])
    ranking_emerges = (order_mfpt == order_gamma)

    # (2) Kramers/Arrhenius EMERGES: log(escape-rate) linear in barrier, slope ~ -1/D (lifetime ~ exp(+barrier/D))
    xs = np.array([barr[o] for o in _ORGANS])
    ys = np.log(np.array([rates[o] for o in _ORGANS]))
    A = np.vstack([xs, np.ones_like(xs)]).T
    slope, intercept = np.linalg.lstsq(A, ys, rcond=None)[0]
    resid = ys - (slope * xs + intercept)
    r2 = 1.0 - float((resid ** 2).sum() / ((ys - ys.mean()) ** 2).sum())
    slope_recovers_invD = abs((-slope) - (1.0 / D)) / (1.0 / D) < 0.30   # within 30% of -1/D (prefactor drift)

    ok = bool(ranking_emerges and r2 > 0.95 and slope_recovers_invD)
    return dict(
        noise_D=D,
        measured_escape_rate={o: round(rates[o], 8) for o in _ORGANS},
        mean_lifetime_MFPT={o: round(mfpt[o], 4) for o in _ORGANS},
        barrier={o: round(barr[o], 6) for o in _ORGANS},
        durability_order_ascending=order_mfpt,
        gamma_order_ascending=order_gamma,
        durability_ranking_emerges=bool(ranking_emerges),
        arrhenius_R2=round(r2, 4), arrhenius_slope=round(float(slope), 4),
        expected_slope_minus_1_over_D=round(-1.0 / D, 4),
        slope_recovers_minus_1_over_D=bool(slope_recovers_invD),
        kramers_law_emerges=bool(r2 > 0.95 and slope_recovers_invD),
        all_pass=ok,
        grade="[V] memory-durability ranking (ascending γ) + barrier/Kramers law EMERGE from a direct "
              "stochastic ON->OFF escape simulation (measured, not asserted); [O] absolute lifetime / "
              "cellular-noise scale D (free, uncalibrated)")


def run(gammas):
    """T8: emergent memory lifetime — durability ordering MEASURED from a stochastic escape simulation, not asserted from γ²/4."""
    r = emergent_memory_lifetime(gammas)
    return dict(T8=dict(target="T8",
                        claim="immune-memory lifetime EMERGES from a direct stochastic ON->OFF escape "
                              "simulation of the R19 field: the measured mean first-passage time ranks in "
                              "ascending γ (deeper barrier = longer memory) and log-rate is linear in the "
                              "barrier (Kramers law emerges, slope recovers −1/D) — not asserted from γ²/4; "
                              "absolute lifetime stays [O]",
                        result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T8"]["result"]
    print("measured escape rate:", r["measured_escape_rate"])
    print("mean lifetime (MFPT):", r["mean_lifetime_MFPT"])
    print("durability order (ascending MFPT):", r["durability_order_ascending"])
    print("ascending-γ order:                ", r["gamma_order_ascending"])
    print("durability ranking emerges:", r["durability_ranking_emerges"])
    print("Arrhenius R^2 = %.4f, slope = %.3f (expect %.3f = -1/D)  -> Kramers law emerges: %s"
          % (r["arrhenius_R2"], r["arrhenius_slope"], r["expected_slope_minus_1_over_D"], r["kramers_law_emerges"]))
    print("T8 all_pass:", r["all_pass"])
