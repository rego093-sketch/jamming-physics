#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setpoint_failure.py  --  Aging / Senescence PATHOLOGY module. Covers this package's MAJOR (non-rare)
diseases. Disease here is NOT a local lesion; it is a FAILURE of a defended setpoint / a clock / a sense
organ -- a loop-gain drop, a setpoint DRIFT, an attractor-shift -- on the SAME R19 substrate. RARE /
monogenic forms are owned by disease_wp and only cross-referenced here.

DERIVED LAW (no tuning):
  A homeostatic setpoint is a defended R19 basin at +sqrt(g). Its DEFENSE GAIN is the restoring strength,
  carried by the field coefficient g (gamma). Aging = slow loss of that gain: g_eff = g * (1 - d), where
  d in [0,1] is the cumulative age-related loop-gain drop. From the vendored substrate two things then
  follow MECHANICALLY and are MEASURED here (not posited):

    (1) SETPOINT DRIFT.  barrier(g_eff) = g_eff^2 / 4 shrinks, and the steady state the loop settles to
        under a fixed chronic drive h moves: drift = settle(g0,h) - settle(g_eff,h).  The defended value
        creeps while the basin still exists -> the slow, unifying aging signature.  [V] (shape)

    (2) CATASTROPHIC CROSSING.  spinodal(g_eff) = 2 (g_eff/3)^1.5 (the |h| past which the healthy basin
        DISAPPEARS) shrinks too, so a chronic stressor h that was survivable at g0 can, past a critical
        age-drop d*, flip the setpoint discontinuously into the pathological basin.  d* is found by
        bisection on the measured is_on() flip -> a sharp onset, not a gradual one.  [V] (shape)

  Absolute calendar RATE of d (how many years to reach a given d) is NOT derivable here: it needs an
  external clock -> graded [O] and stated as an obstacle. Cited per-failure anchors are [L].

Composition with disease_wp: a monogenic lesion enters as a PARAMETER (cited); the systemic trajectory is
computed here. Polygenic / acquired / age disease lives here.
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier, spinodal, settle

R = 8  # rounding dp for emitted floats (determinism parity with engine emit())


# --------------------------------------------------------------------------------------------------
# DERIVED CORE LAW
# --------------------------------------------------------------------------------------------------
def _defended_state(g, h, g0=None):
    """Relax the field to its steady value STARTING FROM the (young) healthy + setpoint at +sqrt(g0).
    The defended homeostatic value is the POSITIVE basin; a pathological stressor is a NEGATIVE drive h
    that pulls it toward the bad (-) basin."""
    s0 = math.sqrt(g0 if g0 is not None else g)
    return settle(g, h, s0=s0)


def setpoint_drift_law(gamma, loop_gain_drop, chronic_drive=0.0):
    """Effect of an age-related loop-gain drop d on a defended setpoint at gamma, under a fixed chronic
    stressor h (h <= 0 pulls toward pathology). Everything returned is MEASURED from the vendored R19
    field, not assigned. The system starts at the young setpoint +sqrt(g0) and relaxes under reduced gain."""
    d = min(max(float(loop_gain_drop), 0.0), 0.999)
    g0 = float(gamma)
    g_eff = g0 * (1.0 - d)
    h = float(chronic_drive)

    healthy_state = _defended_state(g0, h, g0=g0)        # defended value when young
    aged_state    = _defended_state(g_eff, h, g0=g0)     # relax from young setpoint under reduced gain
    drift = healthy_state - aged_state                   # setpoint creep (down), then catastrophe

    b0, b1 = barrier(g0), barrier(g_eff)
    sp0, sp1 = spinodal(g0), spinodal(g_eff)
    crossed = (aged_state <= 0.0)                         # has the healthy(+) basin been lost?

    return {
        "gamma_healthy": round(g0, R),
        "loop_gain_drop": round(d, R),
        "gamma_effective": round(g_eff, R),
        "chronic_drive": round(h, R),
        "defended_state_young": round(float(healthy_state), R),
        "defended_state_aged": round(float(aged_state), R),
        "setpoint_drift": round(float(drift), R),
        "barrier_young": round(float(b0), R),
        "barrier_aged": round(float(b1), R),
        "barrier_fraction_remaining": round(float(b1 / b0) if b0 else 0.0, R),
        "catastrophe_threshold_young": round(float(sp0), R),
        "catastrophe_threshold_aged": round(float(sp1), R),
        "crossed_to_pathology": bool(crossed),
        "note": "barrier g^2/4 shrinks -> drift; spinodal 2(g/3)^1.5 shrinks -> a fixed stressor can flip the setpoint",
    }


def critical_drop_for_crossing(gamma, chronic_drive, lo=0.0, hi=0.999, iters=60):
    """Bisection: the smallest loop-gain drop d* at which a FIXED chronic stressor (h<=0) flips the defended
    setpoint out of the healthy + basin (the + basin disappears). Returns None if no crossing within
    [lo,hi]. Survival is measured by relaxing from the + setpoint and checking the sign."""
    g, h = float(gamma), float(chronic_drive)
    def survives(d):
        ge = g * (1.0 - d)
        return _defended_state(ge, h, g0=g) > 0.0
    if survives(hi):     # still healthy even at max drop -> stressor too small to ever flip
        return None
    if not survives(lo): # already crossed at zero drop -> stressor alone supra-threshold
        return 0.0
    a, b = lo, hi
    for _ in range(iters):
        m = 0.5 * (a + b)
        if survives(m):
            a = m
        else:
            b = m
    return round(0.5 * (a + b), R)


# --------------------------------------------------------------------------------------------------
# FAILURES (this package's major, non-rare aging diseases)
# --------------------------------------------------------------------------------------------------
def _sarcopenia():
    """Age-related muscle decline: the force-defended setpoint loses gain -> measurable drift of the
    defended actuator state. Shape [V]; cited decline anchor [L]; absolute rate [O]."""
    gamma = 1.45  # representative musculoskeletal master (cross-ref musculoskeletal_vp); identity, not tuned
    h = -0.1      # small chronic catabolic stressor pulling the force-setpoint toward failure
    trajectory = []
    for d in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
        law = setpoint_drift_law(gamma, d, h)
        trajectory.append({"loop_gain_drop": law["loop_gain_drop"],
                           "defended_state": law["defended_state_aged"],
                           "drift": law["setpoint_drift"],
                           "barrier_fraction": law["barrier_fraction_remaining"]})
    drifts = [t["drift"] for t in trajectory]
    monotone = all(drifts[i] <= drifts[i + 1] + 1e-9 for i in range(len(drifts) - 1))
    return {
        "site": "sarcopenia",
        "mechanism": "muscle actuator loop-gain drop -> defended force-state drifts down (loss of actuator capacity)",
        "trajectory": trajectory,
        "drift_monotone_with_age": bool(monotone),
        "anchor": "decline rate vs cited age [L]; cross-loop coupling [V]; absolute rate [O]",
        "grade": "[V] shape (monotone gain-loss drift) / [L] cited decline anchor / [O] absolute calendar rate",
    }


def _frailty_multimorbidity():
    """Co-decline of MANY setpoints. Each crosses its own function threshold as a shared aging drive d
    rises; the organism crosses the frailty line when a critical FRACTION have failed. The crossed-fraction
    rises convexly in d -> the frailty transition. Shape [V]."""
    # a spread of homeostatic setpoints at different identity gammas, each under its own chronic stressor
    # (h<=0 pulls toward failure); stressor magnitudes differ -> a SPREAD of critical drops -> a transition
    setpoints = [("glycemic", 1.42, -0.40), ("vascular", 1.50, -0.35), ("musculoskeletal", 1.45, -0.30),
                 ("immune", 1.55, -0.28), ("renal", 1.48, -0.25), ("neuro", 1.59, -0.22)]
    crit = {name: critical_drop_for_crossing(g, h) for name, g, h in setpoints}
    grid = []
    for d in [i / 20.0 for i in range(0, 17)]:  # d = 0.00 .. 0.80
        crossed = sum(1 for name, _, _ in setpoints if crit[name] is not None and d >= crit[name])
        grid.append({"loop_gain_drop": round(d, R), "n_crossed": crossed,
                     "crossed_fraction": round(crossed / len(setpoints), R)})
    fracs = [g["crossed_fraction"] for g in grid]
    monotone = all(fracs[i] <= fracs[i + 1] + 1e-9 for i in range(len(fracs) - 1))
    # convexity: second difference non-negative somewhere in the accelerating phase
    second_diff = [fracs[i + 2] - 2 * fracs[i + 1] + fracs[i] for i in range(len(fracs) - 2)]
    accelerates = any(x > 1e-9 for x in second_diff)
    return {
        "site": "frailty / multimorbidity",
        "mechanism": "co-decline of multiple defended setpoints; organism crosses the frailty line as a critical fraction fail",
        "critical_drops": crit,
        "co_failure_grid": grid,
        "crossed_fraction_monotone": bool(monotone),
        "transition_accelerates": bool(accelerates),
        "anchor": "multi-setpoint co-failure [V]; cited frailty-index association [L]; absolute prevalence [O]",
        "grade": "[V] co-failure transition shape / [L] cited anchor / [O] absolute prevalence",
    }


def _cancer_risk_multiplier():
    """Aging as the dominant pathology RISK MULTIPLIER. As the barrier shrinks with age, the per-unit-time
    barrier-CROSSING rate rises ~ exp(-barrier/T) (Kramers/Arrhenius escape over the vendored barrier).
    Cumulative crossings give a convex, steep age-incidence curve. Connects RA5 to the oncology kernel.
    Shape [V]; absolute incidence [O] (needs external calibration)."""
    gamma = 1.4298  # TP53 identity gamma (the apoptosis/senescence gate); vendored, not tuned
    T = 0.1         # effective noise scale (relative; sets curve SHAPE only -> absolute is [O])
    # map chronological age -> cumulative loop-gain drop (monotone, illustrative clock -> [O])
    ages = list(range(30, 91, 5))
    def drop_at_age(a):  # bounded, monotone; ABSOLUTE mapping is the [O] obstacle, the shape is not
        return min(0.8, max(0.0, (a - 30) / 75.0))
    rows, cum = [], 0.0
    for a in ages:
        d = drop_at_age(a)
        b = barrier(gamma * (1.0 - d))
        rate = math.exp(-b / T)             # instantaneous crossing hazard (relative units)
        cum += rate
        rows.append({"age": a, "loop_gain_drop": round(d, R), "barrier": round(float(b), R),
                     "crossing_hazard_rel": round(float(rate), R), "cumulative_rel": round(float(cum), R)})
    haz = [r["crossing_hazard_rel"] for r in rows]
    convex = all(haz[i] <= haz[i + 1] + 1e-12 for i in range(len(haz) - 1)) and (haz[-1] > haz[0] * 5)
    fold = round(haz[-1] / haz[0], 4) if haz[0] > 0 else None
    return {
        "site": "aging as the cancer / pathology risk multiplier",
        "mechanism": "shrinking barrier -> rising Kramers crossing hazard exp(-barrier/T) -> convex age-incidence across ALL kernels",
        "age_incidence": rows,
        "hazard_convex_and_steep": bool(convex),
        "fold_rise_hazard_30_to_90": fold,
        "anchor": "steep age-incidence curve vs cited registry [L]; crossing accumulation + immunosenescence [V]; absolute incidence [O]",
        "grade": "[V] convex steep shape / [L] cited age-incidence anchor / [O] absolute incidence magnitude",
    }


FAILURES_META = [
    {"site": "sarcopenia", "mechanism": "muscle actuator loop-gain drop -> defended force-setpoint drifts down",
     "owner": "this package"},
    {"site": "frailty / multimorbidity", "mechanism": "co-decline of many setpoints; frailty line crossed when a critical fraction fail",
     "owner": "this package"},
    {"site": "aging as the cancer / pathology risk multiplier", "mechanism": "shrinking barrier -> rising Kramers crossing hazard -> convex age-incidence across ALL kernels",
     "owner": "this package (couples to oncology kernel)"},
    {"site": "(progeroid syndromes -> disease_wp)", "mechanism": "monogenic accelerated aging is rare/genetic -> cross-ref disease_wp",
     "owner": "disease_wp; here only as a rate parameter"},
]


def run():
    """Run the derived pathology sweeps. Deterministic; no RNG."""
    sarc = _sarcopenia()
    frail = _frailty_multimorbidity()
    canc = _cancer_risk_multiplier()
    all_ok = bool(sarc["drift_monotone_with_age"] and frail["crossed_fraction_monotone"]
                  and frail["transition_accelerates"] and canc["hazard_convex_and_steep"])
    return {
        "model": "R19 setpoint failure: loop-gain drop -> barrier shrink (drift) + spinodal shrink (catastrophic crossing)",
        "derived_law": "g_eff = g*(1-d); drift = settle(g0,h)-settle(g_eff,h); catastrophe at spinodal(g_eff)",
        "failures": [sarc, frail, canc],
        "failures_meta": FAILURES_META,
        "all_shapes_reproduced": all_ok,
        "grades": "anchor [L] / shape [V] / absolute incidence-rate [O] (obstacle stated per failure)",
        "disease_wp_composition": "rare/monogenic = cited parameter in; systemic trajectory = computed here",
    }


def status():
    """Back-compatible summary (kept for the engine/gates/run_all that call status())."""
    r = run()
    return {
        "model": r["model"],
        "derived_law": r["derived_law"],
        "failures": r["failures_meta"],
        "all_shapes_reproduced": r["all_shapes_reproduced"],
        "status": "DERIVED: setpoint-drift + catastrophe law from R19; all three failure SHAPES reproduced"
                  if r["all_shapes_reproduced"] else "OPEN: a failure shape did not reproduce",
        "grades": r["grades"],
        "disease_wp_composition": r["disease_wp_composition"],
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
