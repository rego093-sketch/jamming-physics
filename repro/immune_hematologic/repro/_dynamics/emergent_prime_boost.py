#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_prime_boost.py  --  EMERGENT prime-boost vaccination scheduling as a MEASURED interval-dependence of the
matured-affinity endpoint (not asserted, not fitted).

WHY THIS EXISTS (v0.9.0). T18 (emergent_maturation.py) shows affinity maturation EMERGES from an iterated
germinal-centre loop wrapped around the coupled clonal competition, with an HONEST inverted-U in the POOL PRESSURE:
too weak a pool (a large shared antigen pool) gives little selection and a small maturation gain; an intermediate
pool peaks; an over-tight pool collapses the responding set. A vaccination campaign asks the TEMPORAL version of
that same question: given repeated antigen exposures (a prime then boosts), how does the matured-affinity endpoint
depend on the SPACING of the boosts? The VP discipline is emergence: that interval dependence must come OUT of the
same substrate dynamics, MEASURED, never assumed. This module wraps the T18 maturation engine (its exact measured
`_compete` + `_next_generation`) in a fixed-length campaign whose only added physics is antigen pharmacokinetics --
a slowly clearing antigen DEPOT:

    depot level A  (the antigen concentration the germinal centre sees this round): each boost DEPOSITS a fixed
        dose into the depot (saturating at a carrying cap), and the depot CLEARS by a factor each round (antigen is
        consumed / degraded between exposures).
    every round is one germinal-centre cycle: the measured T18 competition runs at the CURRENT depot level (high
        depot -> a large effective pool -> weak competition; low depot -> a tight pool -> strong competition) and
        the repertoire is reseeded by the measured T18 next-generation rule.
    a boost lands every `iv` rounds; the campaign is a FIXED number of rounds for EVERY schedule, so spacing the
        boosts further also fits FEWER of them in.

So boosting too soon -- every round, while the depot has not cleared -- piles antigen into the depot and pushes the
pool pressure into T18's WEAK / large-pool regime, where selection is poor: the measured maturation gain is LOW. A
boost given after the depot has partly cleared finds a productive (tight) pool and drives a strong maturation round,
but a fixed campaign fits only a few such boosts. Nothing about an optimal interval is imposed; the matured-affinity
endpoint is MEASURED for each interval by a standardized challenge readout (the same fresh full-pool challenge for
every schedule).

WHAT EMERGES (measured, deterministic seed=19):
  1. MATURED AFFINITY DEPENDS ON THE BOOST INTERVAL, WITH AN INTERIOR OPTIMUM. Sweeping the boost interval at a
     fixed campaign length, the measured matured-affinity gain is an inverted-U: an intermediate interval maximises
     it. The optimum is INTERIOR (neither the most frequent nor the most spaced schedule) -- the temporal face of
     the T18 pool-pressure inverted-U.
  2. TOO-FREQUENT BOOSTING OVER-SUPPLIES THE DEPOT. The most frequent schedule never lets the depot clear, so the
     measured pool pressure sits in T18's weak / large-pool regime (measured steady-state depot well above the
     productive level) and the maturation gain is sharply suppressed below the optimum -- a measured over-supply
     failure, not assumed.
  3. TOO-SPACED BOOSTING UNDER-USES THE CAMPAIGN. The most spaced schedule lets the depot clear to a productive
     pool for each boost, but fits too few boosts into the fixed campaign, so the measured gain falls back below
     the optimum.
  4. OVER-SUPPLY REQUIRED (honest control). Clamping the depot carrying cap down to the productive pool level
     removes the over-supply penalty: now even the most frequent schedule only ever holds a productive pool, so
     more rounds is strictly better and the measured optimum moves to the most-frequent BOUNDARY (not interior).
     This proves the interior optimum is DRIVEN by depot over-supply pushing the pool into T18's weak regime, not
     by the maturation rule alone (the temporal analogue of T18's unlimited-pool control).

GRADES (C3): the interval dependence with an interior optimum, the too-frequent over-supply, the too-spaced
under-use, and the over-supply-required control are [V] emergent (measured from the iterated coupled stochastic
campaign). The ABSOLUTE optimal interval / timing -- set by the depot clearance factor, the boost dose / carrying
cap, the campaign length, and the free cellular-noise scale D -- is [O], no fabricated schedule numbers.
Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
sys.path.insert(0, os.path.dirname(__file__))     # so we can reuse the T18 measured competition engine
from vp_substrate import spinodal, SEED
from emergent_maturation import _compete, _next_generation, _AFF_LO, _AFF_HI    # the EXACT T18 measured engine

_ORGAN = "lymphoid_adaptive"          # the adaptive compartment (PAX5): a maturing repertoire on one pool

# --- deterministic simulation size (fixed; reuse the T18 regime; no per-schedule tuning) --------------
_M        = 32        # independent hosts per schedule
_N        = 10        # clones per repertoire
_D        = 0.02      # cellular-noise scale (absolute value is [O])
_CONSUME  = 0.6       # antigen consumption per committed clone inside a GC round (T18)
_MUT      = 0.05      # somatic-hypermutation step (T18 baseline)
_AFF_MEAN = 0.80      # initial mean clone affinity (T18; straddles the spinodal)
_AFF_SPR  = 0.30      # initial affinity spread (T18)
_A0_CHALLENGE = 1.0   # standardized challenge pool (T18 productive level; same readout for every schedule)

# --- antigen pharmacokinetics of the campaign (the only added physics; all absolute values are [O]) ---
_R_TOTAL   = 15       # FIXED campaign length (rounds) -- identical for every schedule (creates the trade-off)
_INTERVALS = (1, 2, 3, 4, 6)          # boost-interval sweep (rounds between boosts)
_DOSE      = 1.5      # antigen deposited into the depot per boost; [O]
_CLEAR     = 0.70     # per-round depot clearance factor (antigen consumed / degraded between exposures); [O]
_CAP       = 6.0      # depot carrying cap (saturation) -- allows over-supply on frequent boosting; [O]
_CAP_PRODUCTIVE = _A0_CHALLENGE       # control cap: clamp the depot to the productive pool (removes over-supply)


def _challenge_affinity(g, aff, A0=_A0_CHALLENGE, seed=SEED):
    """Standardized readout (same for every schedule): mean affinity of the clones that respond to a fresh full
    antigen challenge. Lets matured repertoires be compared on a common yardstick."""
    committed = _compete(g, aff, A0, seed=seed)
    n = int(committed.sum())
    return float(aff[committed].mean()) if n > 0 else float(aff.mean())


def campaign(g, interval, dose=_DOSE, clear=_CLEAR, cap=_CAP, rounds=_R_TOTAL,
             M=_M, N=_N, mut=_MUT, consume=_CONSUME, aff_mean=_AFF_MEAN, aff_spr=_AFF_SPR, seed=SEED):
    """Run a fixed-length prime-boost campaign at the given boost interval; MEASURE the matured-affinity gain by a
    standardized challenge readout (final repertoire minus the initial repertoire). The only added physics is the
    antigen depot: each boost deposits `dose` (saturating at `cap`); the depot clears by `clear` each round; every
    round runs the measured T18 competition at the current depot pool pressure and reseeds the repertoire."""
    rng = np.random.default_rng(seed)
    aff = aff_mean + rng.uniform(-aff_spr / 2.0, aff_spr / 2.0, (M, N))
    np.clip(aff, _AFF_LO, _AFF_HI, out=aff)
    aff0 = aff.copy()
    depot = 0.0                                       # antigen depot level (shared pool concentration this round)
    nboost = 0
    pool_sum = 0.0
    for r in range(rounds):
        if r % interval == 0:                         # a boost lands this round -> deposit antigen (saturating)
            depot = min(depot + dose, cap)
            nboost += 1
        committed = _compete(g, aff, depot, D=_D, consume=consume, seed=seed + 1000 + r)
        aff = _next_generation(aff, committed, mut, rng)
        pool_sum += depot
        depot *= clear                                # the depot clears between exposures (antigen wanes)
    gain = _challenge_affinity(g, aff, seed=seed + 9000) - _challenge_affinity(g, aff0, seed=seed + 9000)
    return dict(interval=interval, n_boosts=nboost,
                mean_depot_pool=round(pool_sum / rounds, 4),
                affinity_gain=round(float(gain), 4))


def emergent_prime_boost(gammas):
    g = gammas[_ORGAN]; sp = spinodal(g)

    # ---- over-supply allowed: sweep the boost interval at fixed campaign length (the real prime-boost question) --
    on = [campaign(g, iv, cap=_CAP, seed=SEED + 10 * k) for k, iv in enumerate(_INTERVALS)]
    gains_on = [r["affinity_gain"] for r in on]
    peak = max(gains_on); peak_idx = int(np.argmax(gains_on))
    opt_interval = _INTERVALS[peak_idx]
    interior_optimum = bool(0 < peak_idx < len(_INTERVALS) - 1)           # optimum is interior, not a boundary
    frequent_oversupplied = bool(gains_on[0] < peak - 0.03)               # most frequent clearly below optimum
    spaced_underused = bool(gains_on[-1] < peak - 0.01)                   # most spaced clearly below optimum

    # ---- control: clamp the depot cap to the productive pool -> over-supply removed -> optimum -> frequent edge --
    off = [campaign(g, iv, cap=_CAP_PRODUCTIVE, seed=SEED + 10 * k) for k, iv in enumerate(_INTERVALS)]
    gains_off = [r["affinity_gain"] for r in off]
    off_peak_idx = int(np.argmax(gains_off))
    oversupply_required = bool(off_peak_idx == 0 and interior_optimum)    # control optimum moves to the boundary

    ok = bool(interior_optimum and frequent_oversupplied and spaced_underused and oversupply_required)
    return dict(
        organ=_ORGAN, gamma=round(g, 6), spinodal=round(sp, 6),
        noise_D=_D, campaign_rounds=_R_TOTAL, boost_dose=_DOSE, depot_clearance=_CLEAR, depot_cap=_CAP,
        intervals=list(_INTERVALS),
        oversupply_on_sweep=on,
        oversupply_off_sweep=off,
        peak_gain=round(peak, 4), optimal_interval=opt_interval,
        interior_optimum=bool(interior_optimum),
        too_frequent_oversupplies=bool(frequent_oversupplied),
        too_spaced_underuses=bool(spaced_underused),
        control_optimal_interval=_INTERVALS[off_peak_idx],
        oversupply_required=bool(oversupply_required),
        all_pass=ok,
        grade="[V] the prime-boost interval dependence EMERGES from the T18 maturation engine run as a fixed-length "
              "campaign with a slowly clearing antigen depot: the measured matured-affinity gain is an inverted-U "
              "in the boost interval with an INTERIOR optimum (too-frequent boosting over-supplies the depot into "
              "T18's weak / large-pool regime and starves selection, too-spaced boosting under-uses the fixed "
              "campaign), and clamping the depot cap to the productive pool removes the over-supply penalty and "
              "moves the optimum to the most-frequent boundary -- measured, not assumed; [O] absolute optimal "
              "interval / timing (depot clearance, boost dose / cap, campaign length, cellular-noise scale D)")


def run(gammas):
    """T22: emergent prime-boost scheduling -- the matured-affinity endpoint's dependence on the boost interval MEASURED from a fixed-length campaign, with an interior optimum."""
    r = emergent_prime_boost(gammas)
    return dict(T22=dict(target="T22",
                         claim="prime-boost scheduling EMERGES from the T18 maturation loop run as a fixed-length "
                               "vaccination campaign with a slowly clearing antigen depot: the measured "
                               "matured-affinity gain is an inverted-U in the boost interval with an interior optimum "
                               "-- too-frequent boosts over-supply the depot into T18's weak / large-pool regime and "
                               "starve maturation, too-spaced boosts waste the fixed campaign, and clamping the depot "
                               "cap to the productive pool moves the optimum to the most-frequent schedule (proving "
                               "the optimum is driven by depot over-supply) -- measured, not assumed; absolute "
                               "optimal interval stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T22"]["result"]
    print("PRIME-BOOST SCHEDULING in the adaptive lymphoid compartment (γ=%.4f, spinodal=%.4f), fixed campaign = %d rounds:"
          % (r["gamma"], r["spinodal"], r["campaign_rounds"]))
    print("\nover-supply allowed (real prime-boost: depot clears slowly, cap=%.1f):" % r["depot_cap"])
    print("  interval   n_boosts   mean_depot_pool   affinity_gain")
    for row in r["oversupply_on_sweep"]:
        print("     %d           %2d            %.4f            %.4f"
              % (row["interval"], row["n_boosts"], row["mean_depot_pool"], row["affinity_gain"]))
    print("  -> peak gain %.4f at interval=%d  (interior optimum=%s; too-frequent over-supplies=%s; too-spaced under-uses=%s)"
          % (r["peak_gain"], r["optimal_interval"], r["interior_optimum"], r["too_frequent_oversupplies"], r["too_spaced_underuses"]))
    print("\ncontrol: depot cap clamped to productive pool (%.1f) -> over-supply removed:" % _CAP_PRODUCTIVE)
    print("  interval   n_boosts   mean_depot_pool   affinity_gain")
    for row in r["oversupply_off_sweep"]:
        print("     %d           %2d            %.4f            %.4f"
              % (row["interval"], row["n_boosts"], row["mean_depot_pool"], row["affinity_gain"]))
    print("  -> optimum at interval=%d (most-frequent boundary) -> over-supply required for the interior optimum: %s"
          % (r["control_optimal_interval"], r["oversupply_required"]))
    print("\nT22 all_pass:", r["all_pass"])
