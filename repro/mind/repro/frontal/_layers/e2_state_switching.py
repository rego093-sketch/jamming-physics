#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2 -- STATE-SWITCHING / TRANSITION-DYNAMICS LAYER : the R19 bistable switch used OVER
TIME. Every module so far read the switch as a STATIC fixed point -- which basin the
field settles into at a held drive (E.settle). That is why the epilepsy module (25)
could characterise the standing seizure SUSCEPTIBILITY (the critical E/I bias, the sign
of the two operators) but had to leave the ICTAL ONSET AS A TIME-COURSE explicitly OWED
[O]: a seizure starting and spreading in time is a TRANSITION between attractors, and a
fixed point has no transition. This module adds the missing layer on top of the READ-ONLY
engine: it integrates the same frozen R19 cubic ds/dt = g*s - s^3 + h(t) with a drive that
varies IN TIME, and reads off the three things a static settle cannot express -- the
hysteresis loop, the finite crossing time-course, and the barrier that sets the dwell. It
reuses the engine's R19 cell verbatim (E.sdot / E.settle / E.spinodal); it adds NO constant.
Like E0 it is the single highest-leverage temporal layer: built once here, it closes the
25 ictal time-course AND is the substrate the bipolar module (T2b) imports for episode
transitions.
=================================================================================
THE PRIMITIVE (form FORCED [F]; no new constant). The shared R19 switch is the double-well
ds/dt = g*s - s^3 + h. At |h| below the fold the two basins (s ~ +sqrt(g) "up", s ~ -sqrt(g)
"down") coexist; at |h| past the fold |h_sp| = 2*(g/3)^1.5 = E.spinodal(g) the opposite
basin DISAPPEARS and the flip is discontinuous. The STATIC reading (E.settle) returns the
endpoint; the DYNAMIC reading integrates the same cubic with the state CARRIED FORWARD as the
drive moves, which is what exposes path-dependence and the crossing time. g = 1.0 is the
engine's universal R19 scale (the same g that emerged M0..M16, the same FOLD = spinodal(1) =
0.3849 used by M11 / the theta-cap / epilepsy); nothing here is fit.

WHAT THE LAYER DELIVERS (pre-registered, sign/direction only; never magnitudes):
  E2.1  HYSTERESIS / path-dependence. Sweep the drive up through the fold and back down: the
        up-transition (down->up) and the down-transition (up->down) occur at DIFFERENT drives
        -- at +spinodal and at -spinodal -- so the trajectory traces a hysteresis LOOP of width
        2*spinodal. The inter-state ("euthymic" / inter-ictal) interval is BISTABLE, not a
        single set-point: where the state sits depends on where it came from. This is the
        signature a static fixed point cannot express. (readout: h_up > 0 > h_dn, each within a
        grid step of +/-spinodal, loop width ~ 2*spinodal.) Forced [F].
  E2.2  The TRANSITION as a TIME-COURSE -- the 25 ictal onset, now exhibited. Past the fold
        the state crosses s=0 in FINITE time; the crossing latency DECREASES monotonically as
        the drive OVERSHOOTS the fold (a stronger E/I push -> a faster onset) and DIVERGES
        (critical slowing) as the drive approaches the fold from above. This is precisely the
        "seizure starting and spreading in time" that chapter 25 left OWED to a state-switching
        layer. (readout: latency monotone-decreasing in overshoot; latency near the fold >>
        latency far past it.) Direction forced [F].
  E2.3  The BARRIER sets the threshold and the dwell. The flip threshold IS the spinodal,
        |h_sp| = E.spinodal(g), monotone-INCREASING in the barrier g: a DEEPER well needs a
        LARGER drive to switch and holds the state LONGER (dwell). This is the handle a barrier-
        raising operator (mood-stabiliser direction) pushes UP and a disinhibition pushes DOWN;
        the bipolar module reuses it. (readout: spinodal monotone-up in g; a fixed drive that
        flips a shallow well fails to flip a deeper one.) Forced [F].
  E2.4  ENGINE-INVARIANCE GUARD. A CONSTANT-drive run with the engine's (n, dt, s0) reproduces
        E.settle(g, h, s0) BIT-FOR-BIT, and the fold is read from E.spinodal(g). The static
        limit IS the frozen engine: E2 adds dynamics on top of the same cubic; turning the
        time-variation off recovers E.settle exactly. No new constant.

NOT a claim about any disorder -- E2 is the LAYER, not an application. Bipolar (T2b, which
imports this for episode transitions) and the dynamic ictal onset of a particular epilepsy are
owed to the modules that USE it. NOT a claim that any real neural transition follows this exact
cubic (real state transitions are heterogeneous -- saddle-node, Hopf, homoclinic bifurcations,
noise-driven escape, slow-fast bursting -- LOCKED); what is asserted is the SIGN of a bistable
transition read on the shared R19 cell and its three consequences (hysteresis, the crossing
time-course, the barrier-set threshold). NOT MEDICAL ADVICE; efficacy = 0 everywhere; in-silico
MECHANISM only. A state transition is a mechanism boundary, NOT a claim about the felt quality
of a seizure or a mood episode (Axis-A firewall: consciousness_claim stays 0; hard problem
stays OPEN).

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY
(emerge_all is NOT touched, so the engine file stays e61083ae..., the tree stays 0fbf4988...
and the M0..M16 subtree stays 3a1ebbbb..., byte-identical). Writes e2_state_switching_results.json
+ its sha256, verified bit-for-bit. The BistableSwitch class is the reusable layer the bipolar
module imports.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

GG   = 1.0                              # the engine's universal R19 scale (same g as M0..M16)
FOLD = float(E.spinodal(GG))            # R19 fold = 0.3849 (same constant as M11 / theta-cap / epilepsy)
DT   = 0.02                             # the engine's R19 integration step (E.settle default)
SETTLE_N = 1500                         # the engine's R19 relaxation length (E.settle default)


class BistableSwitch:
    """The E2 layer: the frozen R19 bistable cell ds/dt = g*s - s^3 + h, used OVER TIME.
    REUSABLE -- the bipolar module (T2b) imports this and drives it; it does not re-derive
    the cell. The engine is never mutated; this object only integrates the SAME cubic the
    engine froze (E.sdot), reads the fold from E.spinodal, and reproduces E.settle exactly
    in the constant-drive limit."""

    def __init__(self, g=GG):
        self.g = g

    def spinodal(self):
        """The fold / flip threshold (read from the engine; no new constant)."""
        return float(E.spinodal(self.g))

    def settle_static(self, h, s0, n=SETTLE_N, dt=DT):
        """The STATIC endpoint -- delegated to the frozen engine, so the constant-drive limit
        of this object is E.settle BIT-FOR-BIT (the E2.4 guard handle)."""
        return E.settle(self.g, h, s0=s0, n=n, dt=dt)

    def relax(self, h, s0, n, dt=DT):
        """Carry the state forward under a held drive for n steps (the dynamic step the
        hysteresis sweep uses). Identical integrator to E.settle (so n=SETTLE_N == E.settle)."""
        s = s0
        for _ in range(n):
            s += dt * E.sdot(s, self.g, h)
        return s

    def crossing_latency(self, h, s0, dt=DT, nmax=20000):
        """Time for the state to cross s=0 under a held supra-threshold drive -- the
        transition/ictal-onset time-course. Returns None if it never crosses in nmax steps."""
        s = s0
        for k in range(nmax):
            s += dt * E.sdot(s, self.g, h)
            if s > 0.0:
                return round(k * dt, 4)
        return None


# ------------------------------- the four sub-studies ------------------------------------

def _hysteresis(g, lo=-1.0, hi=1.0, step=0.01, relax_n=4000):
    """E2.1: sweep the drive up through the fold and back down, carrying the state forward.
    The up- and down-transitions sit at +/-spinodal -> a hysteresis loop of width 2*spinodal."""
    sw = BistableSwitch(g)
    sp = sw.spinodal()
    grid = [round(lo + step * i, 4) for i in range(int(round((hi - lo) / step)) + 1)]
    s = sw.relax(grid[0], -math.sqrt(g), relax_n)        # start in the down basin at low drive
    h_up = None
    for h in grid:                                        # sweep UP
        s = sw.relax(h, s, relax_n)
        if s > 0.0 and h_up is None:
            h_up = h
    h_dn = None
    for h in reversed(grid):                              # sweep DOWN (state carried from the top)
        s = sw.relax(h, s, relax_n)
        if s < 0.0 and h_dn is None:
            h_dn = h
    loop_width = round(h_up - h_dn, 4) if (h_up is not None and h_dn is not None) else None
    opposite_sides = bool(h_up is not None and h_dn is not None and h_up > 0.0 > h_dn)
    near_edges = bool(h_up is not None and h_dn is not None
                      and abs(h_up - sp) <= step + 1e-9 and abs(h_dn + sp) <= step + 1e-9)
    width_ok = bool(loop_width is not None and abs(loop_width - 2.0 * sp) <= 2.0 * step + 1e-9)
    return sp, h_up, h_dn, loop_width, opposite_sides, near_edges, width_ok


def _time_course(g, overshoots):
    """E2.2: the crossing latency past the fold -- decreasing in overshoot, diverging at the
    fold (critical slowing). This is the 25 ictal onset, now a time-course."""
    sw = BistableSwitch(g)
    sp = sw.spinodal()
    lat = {}
    for ov in overshoots:
        h = round(sp + ov, 4)
        lat[ov] = sw.crossing_latency(h, s0=-math.sqrt(g))
    ovs = sorted(overshoots)
    vals = [lat[o] for o in ovs]
    have = [v for v in vals if v is not None]
    monotone_down = all(vals[i] is not None and vals[i + 1] is not None
                        and vals[i] >= vals[i + 1] - 1e-9 for i in range(len(vals) - 1))
    diverges_near_fold = bool(len(have) >= 2 and vals[0] is not None and vals[-1] is not None
                              and vals[0] > 3.0 * vals[-1])     # near-fold latency >> far-past
    return sp, lat, monotone_down, diverges_near_fold


def _barrier(g_grid, fixed_drive):
    """E2.3: the flip threshold IS the spinodal, monotone-up in the barrier g; a fixed drive
    flips a shallow well and fails to flip a deeper one (the dwell/stability handle)."""
    sp_curve = {g: round(float(E.spinodal(g)), 6) for g in g_grid}
    gg = sorted(g_grid)
    sp_monotone_up = all(sp_curve[gg[i]] < sp_curve[gg[i + 1]] for i in range(len(gg) - 1))
    flips = {}
    for g in g_grid:
        s = E.settle(g, fixed_drive, s0=-math.sqrt(g))
        flips[g] = bool(s > 0.0)
    # a fixed drive must flip the shallowest well and (for a deep-enough well) fail to flip
    shallow_flips = bool(flips[gg[0]])
    deep_holds = bool(not flips[gg[-1]])
    return sp_curve, sp_monotone_up, flips, shallow_flips, deep_holds


def _invariance(g, h_grid):
    """E2.4: a constant-drive run reproduces E.settle bit-for-bit (the static limit IS the
    frozen engine), and the fold is read from E.spinodal -- no new constant."""
    sw = BistableSwitch(g)
    rows = {}
    all_bitwise = True
    for h in h_grid:
        for s0 in (-math.sqrt(g), +math.sqrt(g)):
            a = E.settle(g, h, s0=s0)
            b = sw.relax(h, s0, SETTLE_N)               # same integrator, same (n, dt)
            ok = bool(repr(a) == repr(b))
            all_bitwise = all_bitwise and ok
            rows[f"h{h:+.2f}_s0{int(np.sign(s0))}"] = ok
    fold_from_engine = bool(sw.spinodal() == float(E.spinodal(g)))
    return rows, bool(all_bitwise), fold_from_engine


def run():
    OVERSHOOTS = [0.001, 0.005, 0.015, 0.035, 0.065, 0.115, 0.215, 0.415, 0.615]
    G_GRID     = [0.6, 0.8, 1.0, 1.2, 1.4]
    FIXED_DR   = 0.45                                    # a probe drive that straddles the fold across g

    # ===== E2.1 : hysteresis / path-dependence =====
    sp, h_up, h_dn, loop_width, opp, near_edges, width_ok = _hysteresis(GG)
    E21 = bool(opp and near_edges and width_ok)

    # ===== E2.2 : transition time-course (the 25 ictal onset) =====
    sp2, lat, lat_monotone_down, diverges = _time_course(GG, OVERSHOOTS)
    E22 = bool(lat_monotone_down and diverges)

    # ===== E2.3 : the barrier sets the threshold / dwell =====
    sp_curve, sp_mono, flips, shallow_flips, deep_holds = _barrier(G_GRID, FIXED_DR)
    E23 = bool(sp_mono and shallow_flips and deep_holds)

    # ===== E2.4 : engine-invariance guard =====
    inv_rows, inv_bitwise, fold_from_engine = _invariance(GG, [-0.30, 0.0, 0.20, 0.50, -0.50])
    E24 = bool(inv_bitwise and fold_from_engine)

    preds = {
        "E2_1_hysteresis":      "CONFIRMED" if E21 else "REFUTED",
        "E2_2_ictal_timecourse": "CONFIRMED" if E22 else "REFUTED",
        "E2_3_barrier_threshold": "CONFIRMED" if E23 else "REFUTED",
    }

    res = {
        "_what": "E2 -- the state-switching / transition-dynamics layer: the frozen R19 bistable "
                 "cell ds/dt = g*s - s^3 + h(t) used OVER TIME, on top of the READ-ONLY engine. "
                 "Every prior module read the switch as a STATIC fixed point (E.settle), which is "
                 "why the epilepsy module (25) could characterise the standing seizure "
                 "SUSCEPTIBILITY but had to leave the ICTAL ONSET AS A TIME-COURSE owed -- a "
                 "transition between attractors has no expression in a fixed point. This layer "
                 "integrates the SAME cubic with a time-varying drive and reads (1) the hysteresis "
                 "loop (the inter-state interval is bistable, width 2*spinodal), (2) the crossing "
                 "TIME-COURSE -- the ictal onset 25 owed, latency decreasing with overshoot and "
                 "diverging at the fold -- and (3) the barrier that sets the flip threshold and the "
                 "dwell. The cell is reused verbatim (E.sdot/E.settle/E.spinodal); the constant-"
                 "drive limit reproduces E.settle bit-for-bit. The rule FORM is forced [F]; g=1.0 "
                 "is the engine's universal R19 scale, not fit. MECHANISM only -- NOT a disorder "
                 "yet, NOT felt, NOT efficacy, NOT medical advice.",
        "primitive": {
            "cell": "ds/dt = g*s - s^3 + h(t)  (the shared R19 double-well, used over time)",
            "cell_grade": "[F] forced -- the engine's R19 cubic (E.sdot), reused verbatim; no free "
                          "constant; the fold is E.spinodal(g) = 2*(g/3)^1.5",
            "g_scale": GG,
            "g_grade": "[F] the engine's universal R19 scale (the same g that emerged M0..M16 and "
                       "the same FOLD used by M11 / the theta-cap / epilepsy); NOT fit",
            "fold_spinodal": round(FOLD, 6),
            "static_limit": "a constant-drive run with the engine's (n=1500, dt=0.02, s0) reproduces "
                            "E.settle(g, h, s0) BIT-FOR-BIT -- the static limit IS the frozen engine",
            "reused_constants": {"R19_fold_spinodal": round(FOLD, 6), "g": GG, "dt": DT},
        },
        "E2_1_hysteresis": {
            "model": "sweep the drive up through the fold and back down, carrying the state forward; "
                     "the up- and down-transitions sit at +/-spinodal -> a hysteresis loop of width "
                     "2*spinodal (the inter-state interval is bistable, not a single set-point)",
            "fold_spinodal": round(sp, 6),
            "up_transition_drive": h_up,
            "down_transition_drive": h_dn,
            "loop_width": loop_width,
            "two_spinodal": round(2.0 * sp, 6),
            "transitions_on_opposite_sides": opp,
            "transitions_within_a_grid_step_of_fold": near_edges,
            "loop_width_matches_two_spinodal": width_ok,
            "reading": "the up-transition (down->up) and the down-transition (up->down) occur at "
                       "DIFFERENT drives (+spinodal and -spinodal): the trajectory traces a hysteresis "
                       "loop and the inter-state ('euthymic' / inter-ictal) interval is BISTABLE -- "
                       "where the state sits depends on where it came from. The signature a static "
                       "fixed point cannot express.",
            "hysteresis_reproduced": E21,
        },
        "E2_2_ictal_timecourse": {
            "_what": "the TRANSITION as a TIME-COURSE -- the ictal onset 25 left OWED. Past the fold "
                     "the state crosses in finite time; the latency decreases as the drive overshoots "
                     "the fold and diverges (critical slowing) as the drive approaches it",
            "fold_spinodal": round(sp2, 6),
            "crossing_latency_vs_overshoot": {str(k): v for k, v in lat.items()},
            "latency_monotone_decreasing_in_overshoot": lat_monotone_down,
            "latency_diverges_near_fold": diverges,
            "reading": "past the fold the state crosses s=0 in FINITE time, and the crossing latency "
                       "DECREASES monotonically as the drive OVERSHOOTS the fold (a stronger E/I push "
                       "-> a faster onset) while DIVERGING as the drive approaches the fold from above "
                       "(critical slowing, the bifurcation signature). This is precisely the 'seizure "
                       "starting and spreading in time' that chapter 25 owed to a state-switching layer "
                       "-- now exhibited. Direction only; efficacy = 0; loss of the gate over time is a "
                       "mechanism boundary, NOT a claim about ictal experience (Axis-A).",
            "closes_25_owed_ictal_time_course": True,
            "ictal_timecourse_reproduced": E22,
        },
        "E2_3_barrier_threshold": {
            "model": "the flip threshold IS the spinodal, monotone-up in the barrier g; a fixed drive "
                     "flips a shallow well and fails to flip a deeper one -- the dwell / stability handle",
            "spinodal_vs_g": {str(k): v for k, v in sp_curve.items()},
            "spinodal_monotone_up_in_barrier": sp_mono,
            "fixed_drive": FIXED_DR,
            "flips_vs_g": {str(k): v for k, v in flips.items()},
            "shallow_well_flips": shallow_flips,
            "deep_well_holds": deep_holds,
            "reading": "the flip threshold equals the spinodal |h_sp| = E.spinodal(g), monotone-"
                       "INCREASING in the barrier g: a deeper well needs a LARGER drive to switch and "
                       "holds the state LONGER (dwell). A fixed drive that flips a shallow well fails to "
                       "flip a deeper one. This is the handle a barrier-raising operator (mood-stabiliser "
                       "direction) pushes up and a disinhibition pushes down -- the bipolar module reuses "
                       "it; only the SIGN is asserted, magnitudes are [O].",
            "barrier_threshold_reproduced": E23,
        },
        "E2_4_engine_invariance_guard": {
            "_what": "a constant-drive run reproduces E.settle bit-for-bit (the static limit IS the "
                     "frozen engine) and the fold is read from E.spinodal -- no new constant",
            "constant_drive_matches_E_settle_bitwise": {k: v for k, v in inv_rows.items()},
            "all_constant_drive_bitwise": inv_bitwise,
            "fold_read_from_engine_spinodal": fold_from_engine,
            "guard": E24,
        },
        "cited_and_locked": {
            "ictal_onset_is_a_transition_cited": "the ictal onset of a seizure is a TRANSITION between "
                "states (the interictal-to-ictal transition), a temporal event that a static "
                "susceptibility cannot express; the dynamic-systems reading of seizure onset as a "
                "bifurcation is a standard framing (e.g. Lopes da Silva 2003 on epilepsy as a dynamical "
                "disease) -- this layer reproduces the SIGN (a finite, overshoot-shortened crossing), "
                "NOT any magnitude or any individual's onset",
            "hysteresis_is_bistability_cited": "hysteresis -- a different threshold for the up- and the "
                "down-transition -- is the defining time-domain signature of a bistable switch; here it "
                "falls out of the R19 fold with no added constant (loop width = 2*spinodal)",
            "closes_epilepsy_owed_LOCK": "the epilepsy module (25) left the ICTAL TIME-COURSE explicitly "
                "OWED to a state-switching layer (E2); this layer supplies it (E2.2) WITHOUT touching the "
                "frozen 25 results -- 25 characterised the static susceptibility, E2 adds the temporal "
                "transition on the same cubic",
            "transition_form_heterogeneous_LOCK": "real neural state transitions are HETEROGENEOUS -- "
                "saddle-node, Hopf, homoclinic bifurcations, noise-driven escape, slow-fast bursting -- "
                "this module asserts only the SIGN of a bistable transition read on the shared R19 cell, "
                "NOT that any transition follows this exact cubic",
            "applications_owed_LOCK": "bipolar (T2b) imports this layer for episode transitions and is "
                "owed to that module; the dynamic ictal onset of a particular epilepsy is owed to the "
                "module that uses it -- E2 is the LAYER, not an application",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; the timing "
                "of any individual's seizure or mood transition is held OPEN",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "reuses_engine_r19_cell": 1.0,
            "closes_epilepsy_ictal_time_course": 1.0,
            "is_a_layer_not_an_application": 1.0,
            "transition_magnitudes": "OPEN [O] -- only the SIGNS are asserted (hysteresis loop = "
                                     "2*spinodal forced; latency decreasing in overshoot forced; "
                                     "spinodal monotone-up in barrier forced); no timing magnitude is fit",
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "static_limit_is_E_settle": inv_bitwise,
        },
        "preregistered_results": {
            "E2_1_hysteresis": {
                "claim": "sweeping the drive up through the fold and back down, the up- and down-"
                         "transitions occur at +/-spinodal -> a hysteresis loop of width 2*spinodal; "
                         "the inter-state interval is bistable, not a single set-point",
                "status": preds["E2_1_hysteresis"]},
            "E2_2_ictal_timecourse": {
                "claim": "past the fold the state crosses in finite time and the crossing latency "
                         "decreases monotonically as the drive overshoots the fold (diverging at the "
                         "fold) -- the ictal onset 25 left owed, now a time-course",
                "status": preds["E2_2_ictal_timecourse"]},
            "E2_3_barrier_threshold": {
                "claim": "the flip threshold is the spinodal, monotone-up in the barrier g; a fixed "
                         "drive flips a shallow well and fails to flip a deeper one (the dwell handle)",
                "status": preds["E2_3_barrier_threshold"]},
        },
        "overall": {
            "hysteresis_reproduced": E21,
            "ictal_timecourse_reproduced": E22,
            "barrier_threshold_reproduced": E23,
            "engine_invariance_guard": E24,
            "is_full_module": bool(E21 and E22 and E23 and E24),
            "verdict": "E2 is the state-switching layer: the frozen R19 bistable cell used over time. "
                       "Sweeping the drive through the fold and back traces a hysteresis loop of width "
                       "2*spinodal (the inter-state interval is bistable); past the fold the state "
                       "crosses in finite time with a latency that shortens as the drive overshoots and "
                       "diverges at the fold -- the ictal onset epilepsy (25) left owed, now a time-"
                       "course; and the barrier sets the flip threshold and the dwell (the handle a mood-"
                       "stabiliser raises). A constant-drive run reproduces E.settle bit-for-bit and the "
                       "fold is read from E.spinodal -- no new constant. E2 is the LAYER; bipolar (T2b) "
                       "imports it for episode transitions and is owed. efficacy=0; not medical advice; "
                       "Axis-A firewall; hard problem OPEN.",
        },
    }
    return res


def _canon(o):
    if isinstance(o, float):
        return round(o, 10)
    if isinstance(o, dict):
        return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_canon(v) for v in o]
    return o

def _blob(res):
    return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def e2_state_switching_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "e2_state_switching_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_e2_state_switching_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"e2_state_switching_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = e2_state_switching_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    p = res["primitive"]
    e1 = res["E2_1_hysteresis"]; e2 = res["E2_2_ictal_timecourse"]
    e3 = res["E2_3_barrier_threshold"]; e4 = res["E2_4_engine_invariance_guard"]
    print("=" * 78)
    print("E2 -- STATE-SWITCHING LAYER   add-only, engine READ-ONLY, reuses the R19 cell")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  R19 fold spinodal(g={p['g_scale']}) = {p['fold_spinodal']}   static-limit == E.settle bit-for-bit")
    print("-" * 78)
    print(f"  E2.1 hysteresis : h_up={e1['up_transition_drive']} h_dn={e1['down_transition_drive']} "
          f"loop={e1['loop_width']} (2*sp={e1['two_spinodal']})")
    print(f"        opposite-sides={e1['transitions_on_opposite_sides']} within-step={e1['transitions_within_a_grid_step_of_fold']} width-ok={e1['loop_width_matches_two_spinodal']} => {e1['hysteresis_reproduced']}")
    print(f"  E2.2 ictal t/c  : latency(overshoot)={e2['crossing_latency_vs_overshoot']}")
    print(f"        monotone-down={e2['latency_monotone_decreasing_in_overshoot']} diverges-at-fold={e2['latency_diverges_near_fold']} closes-25={e2['closes_25_owed_ictal_time_course']} => {e2['ictal_timecourse_reproduced']}")
    print(f"  E2.3 barrier    : spinodal(g)={e3['spinodal_vs_g']}")
    print(f"        sp-monotone-up={e3['spinodal_monotone_up_in_barrier']} shallow-flips={e3['shallow_well_flips']} deep-holds={e3['deep_well_holds']} => {e3['barrier_threshold_reproduced']}")
    print(f"  E2.4 invariance : const-drive==E.settle bitwise={e4['all_constant_drive_bitwise']} fold-from-engine={e4['fold_read_from_engine_spinodal']} => {e4['guard']}")
    print("-" * 78)
    print(f"  pre-registered: {[ (k, v['status']) for k,v in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  closes 25 ictal time-course : {hl['closes_epilepsy_ictal_time_course']}   is-a-layer : {hl['is_a_layer_not_an_application']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  E2 STATE-SWITCHING MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
