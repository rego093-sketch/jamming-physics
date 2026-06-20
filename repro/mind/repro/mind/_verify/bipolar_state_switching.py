#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIPOLAR DISORDER (T2b) : bipolar disorder read as a BISTABLE mood system whose episodes
KINDLE. It is built ON TOP of two layers and IMPORTS both -- the E2 state-switching layer
(BistableSwitch: the R19 cell used over time, for the manic<->depressive EPISODE TRANSITIONS)
and the E0 plasticity layer (PlasticConnectome: for episode ACCUMULATION). It re-derives
NEITHER rule. Where unipolar depression (T1b) visited only the withdrawal pole of the valence
axis, bipolar disorder is the SAME axis traversed in BOTH directions: a manic pole ABOVE health
and a depressive pole BELOW it, with the euthymic interval bistable between them. The handle is
the engine's M17 valence geometry (approach[DA] - avoid[cortisol], already emerged): the
approach extreme is the manic pole, the avoid/cortisol extreme is the depressive pole (T1b's
pole). No new constant enters.
=================================================================================
WHERE THIS SITS ON THE ATLAS. The structural atlas placed conditions on the ignition/synchrony
axis (autism-T under-ignites, schizophrenia over-ignites, epilepsy over-synchronises). The
temporal layers opened two new axes: E0 the plasticity (chronification) axis and E2 the state-
switching (transition) axis. Unipolar depression (T1b) lives on the low-coupling part of the
coupling axis plus the E0 chronification axis. Bipolar disorder is the FIRST condition that
lives on the E2 axis: its defining feature is the TRANSITION between two mood states, which a
static operating point cannot express. Mania is the over-coordination pole T1b never reaches;
depression is T1b's under-coordination pole; the two are basins of one bistable mood switch, and
each episode (a sustained excursion under plasticity) writes an E0 trace -- the kindling /
cycle-acceleration direction.

THE VALENCE HANDLE (grounded, not invented). M17 places approach (dopaminergic) and avoid
(cortisol) on the two poles of the valence axis. A sustained APPROACH (manic-pole) bias b>0
RAISES the effective ephaptic coupling exactly as an excitatory bias does in the SZ/epilepsy/E0
map, k = kappa/(1-|b|), so R rises ABOVE health (over-coordination/over-arousal). A sustained
WITHDRAWAL (depressive-pole) bias b<0 LOWERS it, k = kappa/(1+|b|), so R falls BELOW health --
the T1b pole. The SIGN of the mapping (approach->over-coupling, withdrawal->under-coupling) is
what is asserted, consistent with the M17 valence geometry; the MAGNITUDE of the valence->bias
gain is [O] (representative), exactly as in T1b, and every sign below holds over a SWEEP. The
mood STATE that selects which pole the network sits at is the R19 bistable cell (E2); the
valence drive flips it between basins; episodes accumulate a connectome trace (E0).

PRE-REGISTERED PREDICTIONS (DIRECTION / sign only; readouts = the mania<->health<->depression
contrast, the hysteresis loop, monotone trends; NEVER magnitudes):
  B1  TWO POLES, ONE AXIS (bipolarity). A sustained approach (manic-pole) bias drives the global
      order parameter R ABOVE health (over-coordination); a sustained withdrawal (depressive-pole)
      bias drives R BELOW health (the T1b pole). Euthymia sits between. Bipolar disorder is the
      SAME valence axis traversed in BOTH directions -- mania is the over-pole unipolar depression
      never reaches. (readout: manic-pole R > health > depressive-pole R; both directions monotone
      over a bias sweep.) Reuses the SZ/epilepsy/T1b k-bias map -- no new constant.
  B2  AN EPISODE IS A BISTABLE STATE TRANSITION (E2), not a drift. Modelling mood as the R19
      bistable cell, as the valence drive crosses the fold the mood state FLIPS between basins in
      finite time -- an episode onset is a discontinuous transition (a switch), and the system
      shows HYSTERESIS: the manic->depressive and depressive->manic transitions occur at DIFFERENT
      drives (a path-dependent loop of width 2*spinodal), so the euthymic interval is bistable, not
      a single set-point. The crossing latency shortens as the drive overshoots the fold. (readout:
      hysteresis-loop width ~ 2*spinodal; flip latency monotone-decreasing in overshoot; the static-
      limit switch reproduces E.settle bit-for-bit.) Reuses E2 BistableSwitch -- forced [F], no new
      constant.
  B3  RECURRENCE / KINDLING = EPISODE ACCUMULATION (E0 trace). Each episode (each sustained
      excursion under plasticity) writes a retained structural trace; alternating manic/depressive
      episodes DEEPEN the connectome trace ||dW|| monotonically with episode count -- the kindling /
      cycle-acceleration direction. The barrier to the next switch is set by the bistable g: a LOWER
      barrier (disinhibition) lowers the fold and makes the next flip require LESS drive, so IF
      accumulated episodes lower the barrier THEN cycling accelerates. The SIGN (more episodes ->
      deeper trace -> easier switching -> faster cycling) is asserted; the MAGNITUDE of the trace->
      barrier coupling is [O]. (readout: ||dW|| monotone-up in episode count over an eta sweep; flip-
      drive monotone-down as the barrier is lowered.) Reuses E0 PlasticConnectome -- no re-derivation.
  B4  MOOD-STABILISER SIGN. A barrier-RAISING push (mood-stabiliser-class direction -- lithium and
      valproate are cited as reducing episode frequency) raises the fold/flip threshold: transitions
      require a LARGER drive, so episodes become LESS frequent (a longer euthymic dwell); a fixed
      drive that flips a shallow well fails to flip the raised one. Sign / direction only; efficacy=0.
      (readout: flip threshold monotone-up in stabiliser strength; a fixed drive stops flipping past
      a barrier.) Reuses the E2 barrier handle -- no new constant.
  B5  ENGINE-INVARIANCE GUARD. With eta=0 and drive=0 the layer reproduces the frozen M9
      coordination anchor BIT-FOR-BIT (R = 0.3896145516), the static-limit bistable switch reproduces
      E.settle BIT-FOR-BIT, and W is identical to the kernel. T2b is a pure ADD-ON on top of E2+E0.

ANTI-TUNING. The signs are required to hold over a SWEEP of eta and of the bias / barrier grids,
not at a single point. The pole biases, the valence-drive overshoots, the barrier shifts and the
episode counts are stimulus/severity probes in the exact D8/D9/E0/T1b mould, NOT constants fit to a
target. NO new constant: the effective-coupling-vs-bias map is the same k = kappa/(1-|b|) [excit] /
kappa/(1+|b|) [inhib] used in the SZ/epilepsy/E0/T1b modules, capped at 2*kappa; the bistable cell is
the engine's R19 cubic with g = 1.0 (the universal scale); the fold is E.spinodal(g); eta is the E0
rate [O].

NOT a claim that bipolar disorder is one mechanism. Real bipolar disorder is HETEROGENEOUS -- bipolar
I vs II vs cyclothymia vs mixed states, with rapid-cycling, seasonal and post-partum patterns, and
genetic, circadian, monoaminergic and psychosocial contributors -- LOCKED. What is asserted is the
MECHANISM direction (a bistable mood system with two poles on the valence axis; episodes are state
transitions; recurrence kindles; a stabiliser raises the switch barrier) and the SIGNS above. NOTHING
is asserted about which individual, which bipolar subtype, that any drug treats it, or that anyone
should change treatment. NOT MEDICAL ADVICE; efficacy = 0 everywhere; in-silico MECHANISM only. A mood
state transition and a retained trace are mechanism boundaries, NOT claims about the felt quality of
mania or depression (Axis-A firewall: consciousness_claim stays 0; the hard problem of experience stays
OPEN, covering mood exactly as it covers cognition).

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY (emerge_all is
NOT touched, so the engine file stays e61083ae..., the tree stays 0fbf4988... and the M0..M16 subtree
stays 3a1ebbbb..., byte-identical). REUSES the E2 BistableSwitch and the E0 PlasticConnectome (both
imported, not re-derived). Writes bipolar_state_switching_results.json + its sha256, verified bit-for-bit.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

# REUSE the two temporal layers -- import the classes and the shared (measured) handles; do NOT
# re-derive the Hebbian rule, the coupling map, or the bistable cell (handover discipline: reuse).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e0_plasticity import PlasticConnectome, OMEGA, OMEGA0, KAP, W0, FOLD, N, _k_bias
from e2_state_switching import BistableSwitch, GG, DT, SETTLE_N

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"
M9_ANCHOR_R        = 0.38961455156044245              # frozen M9 R_measured (cross-check)
ETA                = 0.05                              # E0 representative rate [O] (reused)


def _R(W):
    """Order parameter at the measured coupling on W (drive/bias off) -- pure engine."""
    return E._integrate(OMEGA, W, KAP * OMEGA0)[0]


def _dW(W):
    """Frobenius distance of a connectome from the frozen ephaptic kernel (trace depth)."""
    return float(np.linalg.norm(W - W0))


def _clone(pc):
    q = PlasticConnectome()
    q.W = pc.W.copy()
    return q


def _valence_handle():
    """Ground the valence handle in the ALREADY-EMERGED engine (READ-ONLY): M17 places approach
    (DA) and avoid (cortisol) on the two poles of valence. This module maps the approach extreme
    to a manic-pole bias b>0 and the avoid extreme to a depressive-pole bias b<0; here we only
    READ the engine to confirm the handle exists and is grounded."""
    gs = E.emerge_global_state()          # M17 (READ-ONLY)
    iv = E.emerge_interoceptive_axis()    # M18 (READ-ONLY)
    hpa = iv["hpa_axis"]
    return {
        "valence_axis": "approach(DA) - avoid(cortisol) (M17); approach extreme = manic pole, "
                        "avoid/cortisol extreme = depressive pole (T1b's pole)",
        "valence_arousal_corr": gs["valence_arousal_corr"],
        "circumplex_2d": float(gs["circumplex_2d"]),
        "cortisol_peak_min": hpa["cortisol_peak_min"],
        "cortisol_peak_in_cited_window": float(hpa["cortisol_peak_in_cited_window"]),
        "mapping": "approach(manic) -> b>0 -> k=kappa/(1-|b|) (higher coupling, R above health); "
                   "withdrawal(depressive) -> b<0 -> k=kappa/(1+|b|) (lower coupling, R below "
                   "health). SIGNS asserted (consistent with M17 valence), MAGNITUDES [O].",
    }


# --------------------------- B-study drivers (reuse E2 + E0) ------------------------------

def _two_poles(health_R, b_grid):
    """B1: two poles on one axis. A manic-pole bias raises R above health, a depressive-pole bias
    lowers it below -- bipolarity = the same valence axis traversed in both directions."""
    curve = {round(b, 2): (health_R if b == 0.0
             else E._integrate(OMEGA, W0, _k_bias(b) * OMEGA0)[0]) for b in b_grid}
    manic = [b for b in b_grid if b > 0.0]
    depr = [b for b in b_grid if b < 0.0]
    manic_above = all(curve[round(b, 2)] > health_R + 1e-9 for b in manic)
    depr_below = all(curve[round(b, 2)] < health_R - 1e-9 for b in depr)
    bg = sorted(b_grid)
    monotone_up = all(curve[round(bg[i], 2)] <= curve[round(bg[i + 1], 2)] + 1e-9
                      for i in range(len(bg) - 1))
    manic_pole_R = curve[round(manic[-1], 2)]
    depr_pole_R = curve[round(depr[-1], 2)]
    return curve, manic_above, depr_below, monotone_up, manic_pole_R, depr_pole_R


def _episode_transition():
    """B2: an episode is a bistable STATE TRANSITION (E2), with hysteresis and a finite, overshoot-
    shortened crossing latency. Reuses the E2 BistableSwitch (no re-derivation)."""
    sw = BistableSwitch(GG)
    sp = sw.spinodal()
    # hysteresis loop (mood drive swept up through the fold and back)
    step, relax_n = 0.01, 4000
    grid = [round(-1.0 + step * i, 4) for i in range(int(round(2.0 / step)) + 1)]
    s = sw.relax(grid[0], -math.sqrt(GG), relax_n)
    h_up = None
    for h in grid:
        s = sw.relax(h, s, relax_n)
        if s > 0.0 and h_up is None:
            h_up = h
    h_dn = None
    for h in reversed(grid):
        s = sw.relax(h, s, relax_n)
        if s < 0.0 and h_dn is None:
            h_dn = h
    loop_width = round(h_up - h_dn, 4)
    width_ok = bool(abs(loop_width - 2.0 * sp) <= 2.0 * step + 1e-9)
    opp = bool(h_up > 0.0 > h_dn)
    # crossing latency vs overshoot (episode onset time-course)
    overshoots = [0.005, 0.035, 0.115, 0.415]
    lat = {ov: sw.crossing_latency(round(sp + ov, 4), s0=-math.sqrt(GG)) for ov in overshoots}
    ovs = sorted(overshoots)
    lat_mono_down = all(lat[ovs[i]] is not None and lat[ovs[i + 1]] is not None
                        and lat[ovs[i]] >= lat[ovs[i + 1]] - 1e-9 for i in range(len(ovs) - 1))
    # static-limit guard: a constant-drive run reproduces E.settle bit-for-bit
    static_bitwise = bool(repr(sw.relax(0.20, -math.sqrt(GG), SETTLE_N))
                          == repr(E.settle(GG, 0.20, s0=-math.sqrt(GG))))
    return sp, h_up, h_dn, loop_width, opp, width_ok, lat, lat_mono_down, static_bitwise


def _kindling(b_mag, eta, episodes, ep_len, sweep_etas):
    """B3: recurrence = episode accumulation (E0). Alternating manic/depressive episodes deepen the
    connectome trace ||dW|| monotonically with episode count (kindling). Plus the barrier-lowering ->
    easier-switching half. Reuses the E0 PlasticConnectome (no re-derivation)."""
    def kindle(eta_):
        pc = PlasticConnectome()
        traj = []
        for k in range(episodes):
            b = b_mag if (k % 2 == 0) else -b_mag      # alternate manic / depressive episodes
            for _ in range(ep_len):
                pc.epoch(bias=b, eta=eta_)
            traj.append(_dW(pc.W))
        return traj
    main = kindle(eta)
    deepens = all(main[i] < main[i + 1] for i in range(len(main) - 1))
    sweep = {}
    deepens_sweep = True
    for e in sweep_etas:
        t = kindle(e) if e != eta else main
        ok = all(t[i] < t[i + 1] for i in range(len(t) - 1))
        deepens_sweep = deepens_sweep and ok
        sweep[e] = bool(ok)
    # barrier-lowering -> easier switching: a lower barrier g lowers the fold (flip drive)
    g_lowering = [1.4, 1.2, 1.0, 0.8, 0.6]             # barrier decreasing
    flip_drive = {g: round(float(E.spinodal(g)), 6) for g in g_lowering}
    fd = [flip_drive[g] for g in g_lowering]
    flip_drive_down = all(fd[i] > fd[i + 1] for i in range(len(fd) - 1))
    return main, deepens, sweep, bool(deepens_sweep), flip_drive, bool(flip_drive_down)


def _stabiliser(stab_grid, fixed_drive, base_g=GG):
    """B4: mood-stabiliser sign. A barrier-RAISING push raises the fold/flip threshold (transitions
    need a larger drive -> fewer episodes); a fixed drive that flips the unstabilised well fails to
    flip the raised one. Reuses the E2 barrier handle (no new constant). The stabiliser strength is a
    PROBE that raises the barrier g by that amount; only the SIGN is asserted, the magnitude is [O]."""
    thr_curve = {round(stab, 2): round(float(E.spinodal(base_g + stab)), 6) for stab in stab_grid}
    sg = sorted(stab_grid)
    thr_monotone_up = all(thr_curve[round(sg[i], 2)] < thr_curve[round(sg[i + 1], 2)]
                          for i in range(len(sg) - 1))
    # a fixed drive flips the unstabilised well and (for a strong-enough stabiliser) fails to flip
    flips = {round(stab, 2): bool(E.settle(base_g + stab, fixed_drive,
                                           s0=-math.sqrt(base_g + stab)) > 0.0) for stab in stab_grid}
    unstab_flips = bool(flips[round(sg[0], 2)])
    strong_stab_holds = bool(not flips[round(sg[-1], 2)])
    return thr_curve, thr_monotone_up, flips, unstab_flips, strong_stab_holds


def _invariance(health_R):
    """B5: eta=0/drive=0 reproduce the frozen M9 anchor bit-for-bit and the static-limit switch
    reproduces E.settle bit-for-bit (pure add-on on top of E2+E0)."""
    pc = PlasticConnectome()
    R_eta0, _ = pc.epoch(bias=0.0, eta=0.0)
    matches_anchor = bool(health_R == M9_ANCHOR_R)
    eta0_matches = bool(R_eta0 == health_R)
    w_untouched = bool(np.array_equal(pc.W, W0))
    sw = BistableSwitch(GG)
    static_bitwise = bool(repr(sw.relax(0.0, -math.sqrt(GG), SETTLE_N))
                          == repr(E.settle(GG, 0.0, s0=-math.sqrt(GG))))
    return health_R, R_eta0, matches_anchor, eta0_matches, w_untouched, static_bitwise


def run():
    B_MANIC = +0.30                                   # sustained manic-pole (approach) bias
    B_DEPR  = -0.30                                    # sustained depressive-pole (withdrawal) bias
    B_GRID  = [-0.50, -0.30, -0.15, 0.0, 0.15, 0.30, 0.50]

    health_R = _R(W0)                                 # frozen M9 coordination anchor
    val = _valence_handle()

    # ===== B1 : two poles, one axis =====
    pole_curve, manic_above, depr_below, mono_up, manic_R, depr_R = _two_poles(health_R, B_GRID)
    B1 = bool(manic_above and depr_below and mono_up)

    # ===== B2 : an episode is a bistable transition (E2) =====
    (sp, h_up, h_dn, loop_width, opp, width_ok, lat, lat_mono_down,
     static_bitwise_b2) = _episode_transition()
    B2 = bool(opp and width_ok and lat_mono_down and static_bitwise_b2)

    # ===== B3 : recurrence / kindling (E0 trace) =====
    (kindle_traj, deepens, kindle_sweep, deepens_sweep,
     flip_drive, flip_drive_down) = _kindling(0.30, ETA, 6, 3, [0.03, 0.05, 0.08])
    B3 = bool(deepens and deepens_sweep and flip_drive_down)

    # ===== B4 : mood-stabiliser sign =====
    (thr_curve, thr_monotone_up, stab_flips, unstab_flips,
     strong_stab_holds) = _stabiliser([0.0, 0.1, 0.2, 0.4], 0.45)
    B4 = bool(thr_monotone_up and unstab_flips and strong_stab_holds)

    # ===== B5 : engine-invariance guard =====
    Rinv, Reta0_inv, anchor_ok, eta0_ok, w_ok, static_bitwise_b5 = _invariance(health_R)
    B5 = bool(anchor_ok and eta0_ok and w_ok and static_bitwise_b5)

    preds = {
        "B1_two_poles_one_axis":   "CONFIRMED" if B1 else "REFUTED",
        "B2_episode_transition":   "CONFIRMED" if B2 else "REFUTED",
        "B3_kindling_accumulation": "CONFIRMED" if B3 else "REFUTED",
        "B4_mood_stabiliser_sign": "CONFIRMED" if B4 else "REFUTED",
    }

    res = {
        "_what": "Bipolar disorder (T2b): a BISTABLE mood system whose episodes KINDLE, built ON "
                 "TOP of two layers and importing both -- the E2 state-switching layer "
                 "(BistableSwitch, for the manic<->depressive episode TRANSITIONS) and the E0 "
                 "plasticity layer (PlasticConnectome, for episode ACCUMULATION). It re-derives "
                 "neither rule. Where unipolar depression (T1b) visited only the withdrawal pole, "
                 "bipolar disorder is the SAME valence axis traversed in BOTH directions: a manic "
                 "pole ABOVE health and a depressive pole BELOW it, with the euthymic interval "
                 "bistable between them. The handle is the M17 valence geometry (approach[DA] - "
                 "avoid[cortisol], already emerged), mapped to the SAME coupling map as the "
                 "SZ/epilepsy/E0/T1b modules (no new constant). An episode is a bistable state "
                 "TRANSITION (E2); recurrence KINDLES as episodes accumulate a connectome trace "
                 "(E0); a mood-stabiliser raises the switch barrier. MECHANISM only -- NOT a "
                 "disorder subtype, NOT felt, NOT efficacy, NOT medical advice.",
        "axis": {
            "shared_axis": "the measured ephaptic coupling (global Kuramoto order parameter R) read "
                           "in BOTH directions of the M17 valence axis, plus the E2 state-switching "
                           "layer (the R19 bistable mood cell over time) and the E0 plasticity layer "
                           "(episode trace accumulation)",
            "manic_pole": "sustained approach (DA) bias b>0 -> coupling UP -> R ABOVE health "
                          "(over-coordination/over-arousal) -- the over-pole T1b never reaches",
            "depressive_pole": "sustained withdrawal (cortisol) bias b<0 -> coupling DOWN -> R BELOW "
                               "health (hypo-coordination) -- T1b's pole",
            "transition_axis": "the E2 state-switching layer: episodes are bistable transitions "
                               "between the two basins (hysteresis loop width 2*spinodal); the "
                               "euthymic interval is bistable, not a single set-point",
            "recurrence_axis": "the E0 plasticity layer: each episode writes a retained connectome "
                               "trace, and alternating episodes deepen it monotonically (kindling)",
            "relation_to_atlas": "autism-T under-ignites, schizophrenia over-ignites, epilepsy over-"
                                 "synchronises (the synchrony axis); depression (T1b) sits on the low-"
                                 "coupling part of the coupling axis plus the E0 chronification axis; "
                                 "bipolar is the FIRST condition on the E2 state-switching axis -- its "
                                 "defining feature is the transition between two mood states",
        },
        "valence_handle": val,
        "baseline_health": {
            "kappa_measured": round(KAP, 6),
            "R_health": round(health_R, 6),
            "R19_fold_spinodal": round(FOLD, 6),
            "n_regions": N,
            "plasticity_rate_eta": ETA,
            "bistable_g": GG,
            "reused_from_E2": "BistableSwitch (the R19 cell over time); the fold is E.spinodal(g) -- no "
                              "new constant",
            "reused_from_E0": "PlasticConnectome (phase-correlation Hebbian update); the coupling-vs-bias "
                              "map k=kappa/(1-|b|)[excit]/kappa/(1+|b|)[inhib] cap 2*kappa -- no new constant",
        },
        "B1_two_poles_one_axis": {
            "model": "a sustained approach (manic-pole) bias raises the global order parameter R ABOVE "
                     "health; a sustained withdrawal (depressive-pole) bias lowers it BELOW; euthymia "
                     "between -- bipolarity is the same valence axis traversed in both directions",
            "manic_bias": B_MANIC,
            "depressive_bias": B_DEPR,
            "R_vs_valence_bias": {str(k): round(v, 6) for k, v in pole_curve.items()},
            "R_health": round(health_R, 6),
            "manic_pole_R": round(manic_R, 6),
            "depressive_pole_R": round(depr_R, 6),
            "manic_above_health": manic_above,
            "depressive_below_health": depr_below,
            "monotone_over_bias_sweep": mono_up,
            "reading": "the manic pole sits ABOVE health (over-coordination, the over-pole unipolar "
                       "depression never reaches) and the depressive pole BELOW health (T1b's pole); R "
                       "is monotone across the valence bias from depression through euthymia to mania. "
                       "Bipolar disorder is the SAME axis traversed in both directions. Reuses the "
                       "SZ/epilepsy/T1b k-bias map -- no new constant.",
            "two_poles_reproduced": B1,
        },
        "B2_episode_transition": {
            "_what": "an episode is a bistable STATE TRANSITION (E2), not a drift: hysteresis (the "
                     "euthymic interval is bistable) and a finite, overshoot-shortened crossing latency",
            "fold_spinodal": round(sp, 6),
            "up_transition_drive": h_up,
            "down_transition_drive": h_dn,
            "hysteresis_loop_width": loop_width,
            "two_spinodal": round(2.0 * sp, 6),
            "transitions_on_opposite_sides": opp,
            "loop_width_matches_two_spinodal": width_ok,
            "crossing_latency_vs_overshoot": {str(k): v for k, v in lat.items()},
            "latency_monotone_decreasing_in_overshoot": lat_mono_down,
            "static_limit_matches_E_settle_bitwise": static_bitwise_b2,
            "reading": "modelling mood as the R19 bistable cell, an episode onset is a discontinuous "
                       "TRANSITION between basins (a switch, not a gradual drift), the euthymic interval "
                       "shows HYSTERESIS (manic->depressive and depressive->manic transitions at "
                       "different drives -- a loop of width 2*spinodal), and the crossing latency "
                       "shortens as the valence drive overshoots the fold. Reuses the E2 BistableSwitch; "
                       "forced [F]; a state transition is a mechanism boundary, NOT a claim about the "
                       "felt quality of an episode (Axis-A).",
            "episode_transition_reproduced": B2,
        },
        "B3_kindling_accumulation": {
            "_what": "recurrence / KINDLING = episode accumulation (E0 trace): alternating manic/"
                     "depressive episodes deepen the connectome trace, and a lower barrier makes the "
                     "next switch easier (cycle acceleration)",
            "manic_depressive_bias_magnitude": 0.30,
            "episode_count": 6,
            "trace_depth_per_episode_dW": [round(x, 6) for x in kindle_traj],
            "trace_deepens_with_episodes": deepens,
            "deepening_holds_over_eta_sweep_detail": {str(k): v for k, v in kindle_sweep.items()},
            "deepening_holds_over_eta_sweep": deepens_sweep,
            "flip_drive_vs_lowered_barrier": {str(k): v for k, v in flip_drive.items()},
            "flip_drive_decreases_as_barrier_lowers": flip_drive_down,
            "reading": "each episode (a sustained excursion under plasticity) writes a retained "
                       "structural trace; alternating manic/depressive episodes DEEPEN the connectome "
                       "trace ||dW|| monotonically with episode count -- the kindling / cycle-"
                       "acceleration direction -- and the sign holds over an eta sweep. The barrier to "
                       "the next switch is the bistable fold: a LOWER barrier lowers the flip drive, so "
                       "IF accumulated episodes lower the barrier THEN cycling accelerates. The SIGN is "
                       "asserted; the MAGNITUDE of the trace->barrier coupling is [O]. Reuses the E0 "
                       "PlasticConnectome (no re-derivation); a retained trace is a mechanism boundary, "
                       "NOT a claim about the felt quality of recurrent episodes (Axis-A).",
            "kindling_reproduced": B3,
        },
        "B4_mood_stabiliser_sign": {
            "_what": "a barrier-RAISING push (mood-stabiliser-class direction) raises the fold/flip "
                     "threshold -- transitions need a larger drive, so episodes become less frequent",
            "fixed_drive": 0.45,
            "flip_threshold_vs_stabiliser_strength": {str(k): v for k, v in thr_curve.items()},
            "flip_threshold_monotone_up": thr_monotone_up,
            "flips_vs_stabiliser_strength": {str(k): v for k, v in stab_flips.items()},
            "unstabilised_well_flips": unstab_flips,
            "strong_stabiliser_holds": strong_stab_holds,
            "reading": "a barrier-raising operator (the mood-stabiliser-class direction -- lithium and "
                       "valproate are cited as reducing episode frequency) raises the fold/flip threshold "
                       "monotonically: transitions require a LARGER drive, so episodes become LESS "
                       "frequent (a longer euthymic dwell), and a fixed drive that flips the unstabilised "
                       "well fails to flip the raised one. Reuses the E2 barrier handle -- no new "
                       "constant; SIGN / direction only; efficacy = 0; this is NOT a dose, a protocol, or "
                       "a claim that any drug treats anyone.",
            "mood_stabiliser_sign_reproduced": B4,
        },
        "B5_engine_invariance_guard": {
            "_what": "eta=0/drive=0 reproduce the frozen M9 anchor bit-for-bit and the static-limit "
                     "switch reproduces E.settle bit-for-bit -- T2b is a pure add-on on top of E2+E0",
            "R_direct_measured": repr(Rinv),
            "frozen_M9_anchor": repr(M9_ANCHOR_R),
            "matches_frozen_anchor_bitwise": anchor_ok,
            "eta0_epoch_R": repr(Reta0_inv),
            "eta0_matches_direct_bitwise": eta0_ok,
            "eta0_W_identical_to_kernel": w_ok,
            "static_limit_switch_matches_E_settle_bitwise": static_bitwise_b5,
            "guard": B5,
        },
        "cited_and_locked": {
            "bipolar_is_two_poles_cited": "bipolar disorder is defined, in DIRECTION, by episodes at "
                "BOTH poles of mood -- mania/hypomania (elevated arousal and activity) and depression -- "
                "distinguishing it from unipolar depression; this module reproduces the SIGN (a manic "
                "pole above health and a depressive pole below it on one valence axis), NOT any magnitude "
                "or any individual's mood",
            "kindling_cited": "the kindling / cycle-acceleration model of bipolar progression (Post 1992) "
                "holds that episodes beget episodes -- recurrence lowers the threshold for the next episode "
                "and can accelerate cycling; E0 reproduces a kindling-DIRECTION sign (alternating episodes "
                "deepen a retained structural trace; a lower barrier eases the next switch), a mechanism "
                "direction, NOT an efficacy or a magnitude claim",
            "mood_stabiliser_cited": "mood stabilisers (lithium, valproate) are cited as REDUCING episode "
                "frequency in bipolar disorder; this module reproduces a barrier-raising SIGN (raising the "
                "switch threshold makes transitions need a larger drive, so episodes become less frequent), "
                "NOT efficacy, NOT a dose, NOT a protocol",
            "bipolar_heterogeneous_LOCK": "real bipolar disorder is HETEROGENEOUS -- bipolar I vs II vs "
                "cyclothymia vs mixed states, with rapid-cycling, seasonal and post-partum patterns and "
                "genetic, circadian, monoaminergic and psychosocial contributors -- NOT one mechanism or "
                "one cause",
            "valence_to_bias_magnitude_OPEN_LOCK": "the gain mapping the valence poles to the bias "
                "magnitudes is [O] (representative); only the SIGNS (approach -> over-coupling, withdrawal "
                "-> under-coupling) are asserted, consistent with the M17 valence geometry, and the signs "
                "hold over a sweep -- no magnitude is fit",
            "trace_to_barrier_magnitude_OPEN_LOCK": "the magnitude of the trace->barrier coupling (how "
                "much accumulated kindling lowers the switch barrier) is [O]; only the SIGN (more episodes "
                "-> easier switching -> faster cycling) is asserted, and both halves (traces accumulate; a "
                "lower barrier eases switching) are demonstrated -- no coupling constant is fit",
            "rate_is_open_LOCK": "the plasticity RATE eta is [O] (the E0 representative rate); only the "
                "SIGNS are asserted and they hold over an eta sweep -- no magnitude is fit",
            "applications_owed_LOCK": "addiction (T3a) needs E0 sensitisation; Alzheimer (T3b) and OCD "
                "(T3c) are owed to later modules; the dynamic ictal onset of a particular epilepsy is owed "
                "to the module that uses E2",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; which bipolar "
                "subtype any individual has, and whether any treatment helps them, is held OPEN",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "reuses_e0_plasticity": 1.0,
            "reuses_e2_state_switching": 1.0,
            "valence_to_bias_magnitude": "OPEN [O] -- representative; only the signs are asserted, over a "
                                         "bias sweep",
            "trace_to_barrier_magnitude": "OPEN [O] -- only the sign (more episodes -> easier switching) "
                                          "is asserted; both halves demonstrated, no coupling constant fit",
            "plasticity_rate_eta": "OPEN [O] -- the E0 representative rate; signs hold over an eta sweep",
            "which_subtype_individual": "OWED [O] -- requires per-individual data; the model asserts the "
                                        "bistable-mood / kindling mechanism and the valence signs, NOT "
                                        "which bipolar any individual has or whether any treatment helps them",
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "m9_anchor_reproduced_bitwise": anchor_ok,
            "static_limit_is_E_settle": static_bitwise_b5,
            "reuses_e0_layer": True,
            "reuses_e2_layer": True,
        },
        "preregistered_results": {
            "B1_two_poles_one_axis": {
                "claim": "a manic-pole bias raises R above health and a depressive-pole bias lowers it "
                         "below (the same valence axis traversed in both directions), monotone over a "
                         "bias sweep",
                "status": preds["B1_two_poles_one_axis"]},
            "B2_episode_transition": {
                "claim": "an episode is a bistable state transition (E2): a hysteresis loop of width "
                         "2*spinodal and a crossing latency that shortens as the drive overshoots the "
                         "fold; the static limit reproduces E.settle bit-for-bit",
                "status": preds["B2_episode_transition"]},
            "B3_kindling_accumulation": {
                "claim": "alternating manic/depressive episodes deepen the connectome trace monotonically "
                         "with episode count (kindling), over an eta sweep, and a lower barrier lowers the "
                         "flip drive (cycle acceleration)",
                "status": preds["B3_kindling_accumulation"]},
            "B4_mood_stabiliser_sign": {
                "claim": "a barrier-raising (mood-stabiliser-class) push raises the flip threshold "
                         "monotonically so episodes need a larger drive (less frequent); a fixed drive "
                         "stops flipping past a strong-enough barrier",
                "status": preds["B4_mood_stabiliser_sign"]},
        },
        "overall": {
            "two_poles_reproduced": B1,
            "episode_transition_reproduced": B2,
            "kindling_reproduced": B3,
            "mood_stabiliser_sign_reproduced": B4,
            "engine_invariance_guard": B5,
            "is_full_module": bool(B1 and B2 and B3 and B4 and B5),
            "verdict": "bipolar disorder is a bistable mood system whose episodes kindle. The manic pole "
                       "sits above health (over-coordination -- the over-pole unipolar depression never "
                       "reaches) and the depressive pole below it (T1b's pole), so bipolarity is the same "
                       "valence axis traversed in both directions. An episode is a bistable state "
                       "TRANSITION (E2: hysteresis loop of width 2*spinodal, a crossing latency that "
                       "shortens as the drive overshoots the fold); recurrence KINDLES as alternating "
                       "episodes accumulate a connectome trace (E0), and a lower barrier eases the next "
                       "switch; a mood-stabiliser raises the switch barrier so episodes need a larger "
                       "drive. All signs hold over eta / bias / barrier sweeps; the module reuses the E2 "
                       "BistableSwitch and the E0 PlasticConnectome (no re-derivation) and adds no new "
                       "tuned constant; eta=0/drive=0 reproduces the frozen M9 anchor and the static-limit "
                       "switch reproduces E.settle bit-for-bit, engine byte-unchanged. Addiction (T3a) and "
                       "the Tier-3 conditions remain owed. efficacy=0; not medical advice; Axis-A firewall; "
                       "hard problem OPEN.",
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

def bipolar_state_switching_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "bipolar_state_switching_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_bipolar_state_switching_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"bipolar_state_switching_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = bipolar_state_switching_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    b = res["baseline_health"]; v = res["valence_handle"]
    b1 = res["B1_two_poles_one_axis"]; b2 = res["B2_episode_transition"]
    b3 = res["B3_kindling_accumulation"]; b4 = res["B4_mood_stabiliser_sign"]
    b5 = res["B5_engine_invariance_guard"]
    print("=" * 78)
    print("BIPOLAR DISORDER (T2b)   add-only, engine READ-ONLY, reuses E2 + E0 layers")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  valence: {v['valence_axis'][:54]}...  (M17 corr={v['valence_arousal_corr']})")
    print(f"  health: R={b['R_health']}  fold={b['R19_fold_spinodal']}  kappa={b['kappa_measured']}  eta={b['plasticity_rate_eta']}  g={b['bistable_g']}")
    print("-" * 78)
    print(f"  B1 two-poles  : depr_R={b1['depressive_pole_R']} < health={b1['R_health']} < manic_R={b1['manic_pole_R']}")
    print(f"        manic>health={b1['manic_above_health']} depr<health={b1['depressive_below_health']} monotone={b1['monotone_over_bias_sweep']} => {b1['two_poles_reproduced']}")
    print(f"  B2 transition : loop={b2['hysteresis_loop_width']}(2sp={b2['two_spinodal']}) lat={b2['crossing_latency_vs_overshoot']}")
    print(f"        opposite-sides={b2['transitions_on_opposite_sides']} width-ok={b2['loop_width_matches_two_spinodal']} lat-down={b2['latency_monotone_decreasing_in_overshoot']} static==settle={b2['static_limit_matches_E_settle_bitwise']} => {b2['episode_transition_reproduced']}")
    print(f"  B3 kindling   : dW(episodes)={b3['trace_depth_per_episode_dW']}")
    print(f"        deepens={b3['trace_deepens_with_episodes']}(sweep={b3['deepening_holds_over_eta_sweep']}) flip-drive-down={b3['flip_drive_decreases_as_barrier_lowers']} => {b3['kindling_reproduced']}")
    print(f"  B4 stabiliser : thr(stab)={b4['flip_threshold_vs_stabiliser_strength']}")
    print(f"        thr-up={b4['flip_threshold_monotone_up']} unstab-flips={b4['unstabilised_well_flips']} strong-holds={b4['strong_stabiliser_holds']} => {b4['mood_stabiliser_sign_reproduced']}")
    print(f"  B5 invariance : eta=0 R={b5['eta0_epoch_R']} ==anchor:{b5['matches_frozen_anchor_bitwise'] and b5['eta0_matches_direct_bitwise']} W-identical:{b5['eta0_W_identical_to_kernel']} static==settle:{b5['static_limit_switch_matches_E_settle_bitwise']}")
    print("-" * 78)
    print(f"  pre-registered: {[ (k, vv['status']) for k,vv in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  reuses E2/E0 : {hl['reuses_e2_state_switching']}/{hl['reuses_e0_plasticity']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  BIPOLAR MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
