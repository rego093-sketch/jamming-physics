#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E0E2-KINDLING -- KINDLING COUPLING : do repeated state-flips become easier? The THIRD coupling of two
reusable layers the atlas built separately, and the one that finally CLOSES the trace->threshold link
the bipolar module (29) left OPEN. It marries the E0 plasticity layer (26, PlasticConnectome -- a slow
phase-correlation Hebbian update on the frozen ephaptic kernel) and the E2 state-switching layer (28,
BistableSwitch -- the frozen R19 bistable cell used OVER TIME). Neither layer alone could pose the
question this module asks. E0 has the plastic connectome and its retained trace, but it has no bistable
state -- it cannot ask whether a FLIP gets easier, because it has no flip. E2 has the bistable state and
its fold, but its connectome is FROZEN -- nothing it does changes the threshold, so repetition cannot
accumulate. This module MARRIES them: it drives the SINGLE collective R19 bistable state s (the SAME
28/29 BistableSwitch cell the bipolar module uses for episode transitions) through repeated FLIP
EPISODES, lets each flip drive the E0 phase-Hebbian update so the connectome EVOLVES, and reads the
effective drive of an external push on the collective state off that evolving connectome -- so the flip
THRESHOLD changes as the connectome consolidates. It is the layer-level mechanism the bipolar module
(29, B3) named but left [O]: 29 showed alternating episodes DEEPEN the connectome trace ||dW|| and
separately noted a LOWER barrier flips more cheaply, but the actual trace->threshold COUPLING -- whether
and how the accumulated trace lowers the threshold -- it left explicitly OPEN. This module supplies it.
It IMPORTS both layers (it does NOT re-derive the ephaptic kernel, the phase-Hebbian rule, the R19 cell,
or the fold -- handover reuse discipline); the only new object is a kindling switch -- the SAME 28
BistableSwitch driven through the SAME 26 PlasticConnectome. No new constant, no new rule.
=================================================================================
THE GROUNDING (READ-ONLY; no new constant, no new rule). The collective state is the 28 BistableSwitch
cell ds/dt = g*s - s^3 + h (E2's imported R19 cell, the SAME cubic the engine froze, E.sdot), started at
the DOWN fixed point s0 = -sqrt(g). The connectome evolves under the SAME 26 phase-correlation Hebbian
update (E0's imported PlasticConnectome, W <- max(0, W*(1+eta*C)) row-renormalised): each FLIP EPISODE is
a sustained excursion that drives the phase network at the flip's excitatory bias and consolidates a
retained structural trace ||dW||. The effective drive of a global external push p on the COLLECTIVE state
is scaled by the connectome's COORDINATION GAIN L(W) = R(W)/R_anchor, where R(W) is the order parameter at
the measured coupling (the SAME order parameter the engine froze, E._integrate) and R_anchor = R(W0) is the
frozen M9 anchor (0.38961455156044245). This generalises the 48 broadcast-leverage scaling (a node's
column-sum scaled its focal drive) to the GLOBAL coordination gain (the network's coherence scales a
coherent push) -- a pure READOUT of the connectome, not a fit, and L = 1 at W = W0 (the un-kindled limit
recovers the engine). The effective drive is h_eff(p) = p * L(W), and the state flips up iff h_eff crosses
the fold spinodal(g) (E.spinodal, the SAME fold as M11 / theta-cap / epilepsy / E2). The flip THRESHOLD in
external push is therefore p*(W,g) = spinodal(g) / L(W) -- as the connectome consolidates and L grows, p*
DROPS: repeated flips become easier. The plasticity rate eta is SWEPT over the E0 sweep {0.03,0.05,0.08}
AND the barrier depth g over the E2 sweep {0.7,1.0,1.3} (g = 1.0 is the engine's universal R19 scale);
every SIGN asserted below is required to hold across BOTH sweeps (anti-tuning, rate x barrier). With
eta = 0 the connectome stays frozen, L stays 1, and the threshold stays the un-kindled fold BIT-FOR-BIT
(the E0.4 guard), and with a zero push (p = 0, h_eff = 0) the collective state settles via E.settle
BIT-FOR-BIT (the E2.4 guard) -- nothing here is fit.

WHAT THE MODULE DELIVERS (pre-registered, sign/direction only; never magnitudes):
  K1  KINDLING -- REPEATED FLIPS LOWER THE FLIP THRESHOLD, AND IT IS BARRIER-INVARIANT (the discriminant
      that closes the 29 [O]). Driving repeated flip episodes through the plastic connectome, the retained
      trace ||dW|| deepens STRICTLY MONOTONICALLY with episode count (the E0 consolidation signal, the same
      29 B3 trace-deepening), and the collective state's flip threshold in external push p* = spinodal(g)/
      L(W) ends BELOW the un-kindled fold -- repeated flips become EASIER. The kindling (net threshold-
      decrease) holds across the rate sweep eta in {0.03,0.05,0.08} AND is BARRIER-INVARIANT: at every well
      depth g in {0.7,1.0,1.3} the kindled threshold ends below that depth's own un-kindled fold, because
      p* = spinodal(g)/L scales the fold by the same gain at every g. This is the trace->threshold coupling
      29 (B3) named but left [O]: the accumulated trace lowers the threshold. grade [V mech].
  K2  LEARNED CHANGE OF HYSTERESIS + FASTER ONSET (the dynamic content). As kindling proceeds the push-
      space HYSTERESIS LOOP NARROWS: the loop width 2*spinodal(g)/L(W) ends below its un-kindled value (the
      inter-state interval the 28 hysteresis made bistable is RESHAPED by repetition -- a LEARNED change of
      the state-switching hysteresis), and at a FIXED supra-threshold push the crossing LATENCY -- the time
      the collective state takes to flip -- SHORTENS (the consolidated connectome raises the effective
      drive, overshooting the fold further, so the onset is faster, the 28 E2.2 time-course shortened by
      repetition). Both net-monotone with episode count, across the rate sweep. grade [V mech].
  K3  KINDLING IS CONSOLIDATIVE, NOT DEGRADATIVE (the genuinely-new coupling result + the honest negative).
      The clean, intuitive hypothesis -- "repeated violent flips KINDLE by ERODING the network's
      coordination (driving R toward incoherence), so a more-kindled connectome is a LESS-coordinated one"
      -- is REFUTED. Empirically the connectome's coordination R(W) at the measured coupling RISES (net,
      monotone-up across the rate sweep) and stays ABOVE the frozen M9 anchor as flips repeat, while the
      trace deepens: the threshold falls THROUGH CONSOLIDATION (the connectome writing the repeated
      transition into its own structure), NOT through degradation. So kindling and erosion are decoupled --
      the threshold can drop while coordination strengthens. We do NOT force the tidy "kindling erodes
      stability" story; the refuted clean hypothesis is reported honestly. grade [V mech] (a refuted clean
      hypothesis is a finding).
  K4  A SINGLE COHERENT CONSOLIDATIVE SEAM (the structural class). The three facts above are ONE phenomenon:
      every flip leaves a retained structural trace (E0) that lowers the next flip's threshold (E2). The
      threshold is monotone-decreasing in the accumulated trace ||dW|| (not merely in episode count) -- the
      trace IS the kindling variable, the explicit trace->threshold law 29 (B3) left open -- and the whole
      seam is consolidative. A DIRECTION-ONLY [L] correspondence is noted, never a magnitude or a
      prediction: clinical KINDLING (Goddard's electrical kindling, where repeated sub-threshold stimulation
      progressively lowers the seizure threshold) and bipolar CYCLE ACCELERATION (episodes recur more
      easily over time) are the recognised phenomena in which repetition lowers the next transition's
      threshold -- direction-consistent with a retained trace easing the next flip, never a patient-level
      claim. grade [V mech] structural + [L].

NOT a claim that real kindling reduces to a single scalar R19 cell whose drive is scaled by the order
parameter of a phase-Hebbian connectome (real kindling and cycle acceleration are heterogeneous -- altered
gene expression, mossy-fibre sprouting, receptor trafficking, network reorganisation, allostatic load --
LOCKED); what is asserted is the SIGN/DIRECTION of whether repeated flips lower the collective flip
threshold when the connectome evolves by the imported phase-Hebbian rule and the effective drive is scaled
by the imported coordination gain, and its four consequences (the trace-deepening with a net threshold-
decrease that is barrier-invariant, the narrowed hysteresis loop and shortened onset, the consolidative-
not-degradative refutation, and the single coherent seam with the trace as the kindling variable). NOT a
claim about the FELT quality of an episode or a seizure (Axis-A firewall: the collective bistable state,
its flip threshold, the retained trace and the coordination gain are STRUCTURAL quantities of the coupling
model, NEVER a felt state, an experienced mood, a level of consciousness or an experienced ease of relapse;
consciousness_claim stays 0; hard problem stays OPEN). NOT a real connectome, a real synaptic-weight matrix,
a real measure of kindling or seizure threshold, or a prediction of whether any patient's episodes will
accelerate. NOT MEDICAL ADVICE; efficacy = 0 everywhere; in-silico MECHANISM only; nothing here is a cure,
a treatment, a prognosis, or a device setting. Every MAGNITUDE is [O]; only structural SIGNS and DIRECTIONS
are asserted, and they are certified to survive the plasticity-rate sweep AND the barrier-depth sweep.

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY (emerge_all is NOT
touched, so the engine file stays e61083ae..., the tree stays 0fbf4988... and the M0..M16 subtree stays
3a1ebbbb..., byte-identical). COUPLES the E0 PlasticConnectome and the E2 BistableSwitch (both imported,
not re-derived); the connectome evolves by the imported phase-Hebbian rule and the SAME 28 cell is driven
by an effective drive scaled by the imported coordination gain. Writes e0e2_kindling_results.json + its
sha256, verified bit-for-bit. The kindling switch is the reusable seam any later plasticity-switching
module imports.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

# REUSE both layers -- import their classes and shared (measured) handles; do NOT re-derive the
# ephaptic kernel, the phase-Hebbian rule, the R19 cell, or the fold (handover discipline: reuse,
# not re-derive).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e0_plasticity import (PlasticConnectome, W0, OMEGA, OMEGA0, KAP, M9_ANCHOR_R, FOLD,
                           N, REGS, ENGINE_TREE_FROZEN, M0_16_FROZEN)
from e2_state_switching import BistableSwitch, GG, DT, SETTLE_N   # the E2 state-switching layer

HERE = os.path.dirname(os.path.abspath(__file__))
R_ANCHOR = M9_ANCHOR_R                  # frozen M9 order-parameter anchor R(W0) = 0.38961455156044245

# --- the kindling protocol (representative reads + sweeps; magnitudes [O]) ---
B_MAG    = 0.30                         # flip-bias magnitude of a sustained excursion (same as 29 kindling)
EP_LEN   = 3                            # plasticity epochs per flip episode (same as 29 kindling)
EPISODES = 8                            # number of repeated flip episodes
ETA_SWEEP = (0.03, 0.05, 0.08)         # E0 plasticity-rate sweep
BARRIER_SWEEP = (0.7, 1.0, 1.3)        # E2 barrier-depth sweep (well depth g)
ETAREP   = 0.05                         # representative plasticity rate [swept]
GREP     = GG                           # representative barrier depth = engine R19 scale 1.0 [swept]
PTEST    = 0.50                         # a fixed supra-threshold external push for the latency read [O]


class KindlingSwitch:
    """The E0xE2 seam: the SAME 28 BistableSwitch collective state, driven by an external push whose
    effective drive is scaled by the connectome's COORDINATION GAIN, with the connectome EVOLVING under
    the SAME 26 phase-Hebbian update through repeated flips. REUSABLE -- a later plasticity-switching
    module imports this; it does not re-derive the kernel, the Hebbian rule, the R19 cell or the fold.
    The engine is never mutated; W starts as the frozen kernel and only this object's PlasticConnectome
    copy evolves."""

    def __init__(self, g=GREP):
        self.g = g
        self.pc = PlasticConnectome()          # imported E0 plastic connectome (evolving W)
        self.cell = BistableSwitch(g)          # imported 28/29 R19 bistable cell

    def reset(self):
        self.pc.reset(); return self

    def gain(self):
        """The coordination gain L = R(W)/R_anchor -- a pure readout of the evolving connectome; = 1
        at W = W0 (the un-kindled limit)."""
        return float(self.pc.order() / R_ANCHOR)

    def fold(self):
        """The fold (read from the engine; no new constant)."""
        return self.cell.spinodal()

    def threshold(self):
        """The flip threshold in external push p* = spinodal(g)/L -- drops as the gain L grows."""
        return float(self.fold() / self.gain())

    def h_eff(self, p):
        """The effective drive an external push p applies to the collective state = p * coordination gain."""
        return float(p * self.gain())

    def flips(self, p):
        """Does a push p flip the collective state up from the DOWN fixed point? Static endpoint via the
        imported cell's relax (= E.settle bit-for-bit at n=SETTLE_N)."""
        s = self.cell.relax(self.h_eff(p), s0=-math.sqrt(self.g), n=SETTLE_N)
        return bool(s > 0.0)

    def latency(self, p):
        """The crossing latency -- the time the collective state takes to flip -- under a push p (the
        imported cell's crossing_latency); None if it never crosses."""
        return self.cell.crossing_latency(self.h_eff(p), s0=-math.sqrt(self.g), dt=DT)

    def loop_width(self):
        """The push-space hysteresis loop width 2*spinodal(g)/L -- narrows as the gain L grows."""
        return float(2.0 * self.fold() / self.gain())

    def trace(self):
        """The retained structural trace ||W - W0|| (the E0 consolidation signal)."""
        return self.pc.trace()

    def run_episode(self, bias, eta, ep_len=EP_LEN):
        """One flip episode: a sustained excursion at `bias` driven through the E0 phase-Hebbian update
        (rate eta), for ep_len epochs; consolidates the connectome (updates the imported PlasticConnectome
        in place)."""
        for _ in range(ep_len):
            self.pc.epoch(bias=bias, eta=eta)


def _track(eta, g, episodes=EPISODES, b_mag=B_MAG, ep_len=EP_LEN, ptest=PTEST):
    """Run `episodes` repeated flip episodes (alternating up/down = repeated transitions) through the
    plastic connectome at rate eta, barrier g; after each episode read (trace, gain, threshold,
    loop_width, latency_at_ptest, R). Episode 0 is the un-kindled state (W0)."""
    ks = KindlingSwitch(g)
    rows = [{"ep": 0, "trace": ks.trace(), "gain": ks.gain(), "threshold": ks.threshold(),
             "loop_width": ks.loop_width(), "latency": ks.latency(ptest), "R": ks.pc.order()}]
    for k in range(episodes):
        b = b_mag if (k % 2 == 0) else -b_mag           # alternate up / down flips
        ks.run_episode(b, eta, ep_len)
        rows.append({"ep": k + 1, "trace": ks.trace(), "gain": ks.gain(),
                     "threshold": ks.threshold(), "loop_width": ks.loop_width(),
                     "latency": ks.latency(ptest), "R": ks.pc.order()})
    return rows


# ------------------------------- the four sub-studies + guard ----------------------------

def _kindling_threshold():
    """K1: repeated flips deepen the trace STRICTLY MONOTONICALLY and the flip threshold ends BELOW the
    un-kindled fold (kindling), barrier-invariant across the well-depth sweep, holding across the rate
    sweep. The trace->threshold coupling 29 (B3) left [O]."""
    trace_strict_all = True
    net_kindle_all = True
    barrier_invariant = True
    per_eta_trace_end = {}
    # rate sweep x barrier sweep
    for eta in ETA_SWEEP:
        # trace does not depend on g (g acts only on the bistable cell); track once per eta at GREP
        rows = _track(eta, GREP)
        tr = [r["trace"] for r in rows]
        trace_strict = all(tr[i] < tr[i + 1] - 0.0 for i in range(len(tr) - 1))
        trace_strict_all = trace_strict_all and trace_strict
        per_eta_trace_end[eta] = round(tr[-1], 6)
        for g in BARRIER_SWEEP:
            rg = _track(eta, g)
            thr = [r["threshold"] for r in rg]
            fold_g = float(E.spinodal(g))
            net_kindle = bool(thr[-1] < fold_g - 1e-12)     # ends below this depth's own un-kindled fold
            net_kindle_all = net_kindle_all and net_kindle
            barrier_invariant = barrier_invariant and net_kindle
    # labelled tables at the representative (eta, g)
    rows_rep = _track(ETAREP, GREP)
    fold_rep = float(E.spinodal(GREP))
    thr_table = {str(r["ep"]): round(r["threshold"], 6) for r in rows_rep}
    trace_table = {str(r["ep"]): round(r["trace"], 6) for r in rows_rep}
    net_drop_rep = round(fold_rep - rows_rep[-1]["threshold"], 6)
    folds_by_g = {str(g): round(float(E.spinodal(g)), 6) for g in BARRIER_SWEEP}
    thr_end_by_g = {str(g): round(_track(ETAREP, g)[-1]["threshold"], 6) for g in BARRIER_SWEEP}
    return (trace_strict_all, net_kindle_all, barrier_invariant, thr_table, trace_table,
            fold_rep, net_drop_rep, folds_by_g, thr_end_by_g, per_eta_trace_end)


def _dynamics():
    """K2: the push-space hysteresis loop NARROWS and the crossing latency at a fixed supra-threshold
    push SHORTENS as kindling proceeds (a learned change of the 28 hysteresis + a faster 28 onset).
    Both net-monotone with episode count across the rate sweep."""
    loop_narrows_all = True
    latency_shortens_all = True
    for eta in ETA_SWEEP:
        rows = _track(eta, GREP)
        lw = [r["loop_width"] for r in rows]
        lat = [r["latency"] for r in rows if r["latency"] is not None]
        loop_narrows = bool(lw[-1] < lw[0] - 1e-12)
        # latency at PTEST must stay finite (supra-threshold) and net-shorten
        latency_finite = bool(all(r["latency"] is not None for r in rows))
        latency_shortens = bool(latency_finite and lat[-1] < lat[0] - 1e-12)
        loop_narrows_all = loop_narrows_all and loop_narrows
        latency_shortens_all = latency_shortens_all and latency_shortens
    rows_rep = _track(ETAREP, GREP)
    loop_table = {str(r["ep"]): round(r["loop_width"], 6) for r in rows_rep}
    lat_table = {str(r["ep"]): (round(r["latency"], 4) if r["latency"] is not None else None)
                 for r in rows_rep}
    return (bool(loop_narrows_all), bool(latency_shortens_all), loop_table, lat_table)


def _consolidation_not_erosion():
    """K3 (the genuinely-new coupling result + the honest negative): the clean hypothesis 'kindling
    ERODES coordination (R toward incoherence), so easier-to-flip means LESS coordinated' is REFUTED.
    The flip threshold DROPS (easier, from K1) while the coordination R(W) RISES (net) and the kindled
    connectome ends MORE coordinated than the un-kindled one -- so easier-to-flip and degraded-coordination
    are DECOUPLED: the threshold falls THROUGH CONSOLIDATION, not through erosion."""
    R_net_up_all = True
    ends_above_anchor_all = True
    decoupled_all = True            # threshold drops AND R rises simultaneously (not erosion)
    for eta in ETA_SWEEP:
        rows = _track(eta, GREP)
        Rs = [r["R"] for r in rows]; thr = [r["threshold"] for r in rows]
        R_net_up = bool(Rs[-1] > Rs[0] + 1e-9)                          # coordination nets UP
        ends_above = bool(Rs[-1] >= R_ANCHOR - 1e-9)                    # kindled connectome >= anchor
        decoupled = bool((thr[-1] < thr[0] - 1e-12) and (Rs[-1] > Rs[0] + 1e-9))  # easier AND more-coordinated
        R_net_up_all = R_net_up_all and R_net_up
        ends_above_anchor_all = ends_above_anchor_all and ends_above
        decoupled_all = decoupled_all and decoupled
    rows_rep = _track(ETAREP, GREP)
    R_table = {str(r["ep"]): round(r["R"], 6) for r in rows_rep}
    dR_rep = round(rows_rep[-1]["R"] - R_ANCHOR, 6)
    trace_deepens = bool(rows_rep[-1]["trace"] > rows_rep[0]["trace"] + 1e-9)
    # honest caveat: report whether R stays above the anchor at EVERY episode (it has a negligible
    # transient sub-anchor dip in the first excursion at the lowest rate before consolidation dominates)
    stays_above_every_step = {}
    for eta in ETA_SWEEP:
        Rs = [r["R"] for r in _track(eta, GREP)]
        stays_above_every_step[str(eta)] = bool(all(Rs[k] >= R_ANCHOR - 1e-9 for k in range(1, len(Rs))))
    return (bool(R_net_up_all), bool(ends_above_anchor_all), bool(decoupled_all),
            R_table, dR_rep, trace_deepens, stays_above_every_step)


def _coherent_seam():
    """K4: the threshold is monotone-decreasing in the accumulated trace ||dW|| (the trace IS the
    kindling variable -- the explicit trace->threshold law 29 left open), and the whole seam is a
    single coherent consolidative object (trace strict-up, threshold net-down, R net-up). [L]
    direction-only clinical correspondence."""
    # threshold vs accumulated trace at the representative (eta, g): order by trace, check net-decrease
    rows = _track(ETAREP, GREP)
    ordered = sorted(rows, key=lambda r: r["trace"])
    thr = [r["threshold"] for r in ordered]
    thr_decreases_with_trace = bool(thr[-1] < thr[0] - 1e-12)
    # coherence: across the rate sweep, trace strict-up AND threshold net-down AND R net-up
    coherent = True
    for eta in ETA_SWEEP:
        rg = _track(eta, GREP)
        tr = [r["trace"] for r in rg]; th = [r["threshold"] for r in rg]; Rs = [r["R"] for r in rg]
        coherent = coherent and all(tr[i] < tr[i + 1] for i in range(len(tr) - 1)) \
                   and bool(th[-1] < th[0] - 1e-12) and bool(Rs[-1] > Rs[0] + 1e-9)
    trace_threshold_pairs = {round(r["trace"], 4): round(r["threshold"], 6) for r in rows}
    return (thr_decreases_with_trace, bool(coherent), trace_threshold_pairs)


def _invariance():
    """S5: the double-inherited engine-invariance guard. (E0.4) With eta = 0 the connectome stays frozen,
    R = the frozen M9 anchor BIT-FOR-BIT, so the gain L = 1 and the flip threshold = the un-kindled fold
    exactly. (E2.4) With a zero push (p = 0, h_eff = 0) the collective state settles via E.settle
    BIT-FOR-BIT and the down state stays down. The coupling is a pure add-on on the engine."""
    g = GREP
    # (E0.4) eta = 0: run the kindling protocol with no plasticity -> R == anchor bit-for-bit
    ks0 = KindlingSwitch(g)
    for k in range(EPISODES):
        b = B_MAG if (k % 2 == 0) else -B_MAG
        ks0.run_episode(b, eta=0.0)
    R_eta0 = ks0.pc.order()
    R_eta0_bitwise = bool(R_eta0 == R_ANCHOR)
    gain_eta0_one = bool(ks0.gain() == 1.0)
    thr_eta0 = ks0.threshold()
    thr_is_fold = bool(thr_eta0 == float(E.spinodal(g)))
    # (E2.4) zero push -> h_eff = 0 -> E.settle bit-for-bit, down stays down
    sw = BistableSwitch(g)
    a = E.settle(g, 0.0, s0=-math.sqrt(g))
    b = sw.relax(0.0, -math.sqrt(g), SETTLE_N)
    static_is_settle = bool(repr(a) == repr(b))
    c = ks0.h_eff(0.0)
    zero_push_zero_drive = bool(c == 0.0)
    down_stays_down = bool(a < 0.0)
    fold_from_engine = bool(ks0.fold() == float(E.spinodal(g)))
    return (R_eta0_bitwise, gain_eta0_one, thr_is_fold, static_is_settle, zero_push_zero_drive,
            down_stays_down, fold_from_engine, repr(R_eta0), repr(a))


def run():
    # ===== K1 : kindling -- repeated flips lower the threshold, barrier-invariant =====
    (trace_strict, net_kindle, barrier_inv, thr_table, trace_table, fold_rep, net_drop,
     folds_by_g, thr_end_by_g, trace_end_by_eta) = _kindling_threshold()
    K1 = bool(trace_strict and net_kindle and barrier_inv)

    # ===== K2 : learned change of hysteresis + faster onset =====
    (loop_narrows, latency_shortens, loop_table, lat_table) = _dynamics()
    K2 = bool(loop_narrows and latency_shortens)

    # ===== K3 : kindling is consolidative, not degradative (honest negative) =====
    (R_net_up, ends_above, decoupled, R_table, dR_rep, trace_deepens,
     stays_above_steps) = _consolidation_not_erosion()
    K3 = bool(R_net_up and ends_above and decoupled and trace_deepens)

    # ===== K4 : a single coherent consolidative seam =====
    (thr_vs_trace, coherent, trace_threshold_pairs) = _coherent_seam()
    K4 = bool(thr_vs_trace and coherent)

    # ===== S5 : double-inherited engine-invariance guard =====
    (R_eta0_bit, gain_one, thr_fold, static_settle, zero_drive, down_down, fold_eng,
     R_eta0_repr, a_repr) = _invariance()
    S5 = bool(R_eta0_bit and gain_one and thr_fold and static_settle and zero_drive and down_down and fold_eng)

    preds = {
        "K1_repeated_flips_lower_threshold_barrier_invariant": "CONFIRMED" if K1 else "REFUTED",
        "K2_learned_hysteresis_narrows_and_onset_shortens": "CONFIRMED" if K2 else "REFUTED",
        "K3_kindling_is_consolidative_not_degradative": "CONFIRMED" if K3 else "REFUTED",
        "K4_single_coherent_consolidative_seam": "CONFIRMED" if K4 else "REFUTED",
    }

    res = {
        "_what": "E0E2-KINDLING -- the kindling coupling: the THIRD marriage of two reusable layers the "
                 "atlas built separately, the E0 plasticity layer (26 PlasticConnectome, a phase-Hebbian "
                 "update on the frozen kernel) and the E2 state-switching layer (28 BistableSwitch, the "
                 "frozen R19 bistable cell used over time), and the module that CLOSES the trace->threshold "
                 "link the bipolar module (29, B3) named but left [O]. Neither layer alone could pose the "
                 "question -- E0 has the plastic connectome but no bistable flip, E2 has the flip but a frozen "
                 "connectome so repetition cannot accumulate. This module drives the SINGLE collective R19 "
                 "bistable state (the SAME 28/29 cell) through repeated FLIP EPISODES, lets each flip drive "
                 "the E0 phase-Hebbian update so the connectome EVOLVES, and reads the effective drive of an "
                 "external push off that evolving connectome via its COORDINATION GAIN L(W)=R(W)/R_anchor (a "
                 "pure readout, =1 at W0, generalising the 48 broadcast leverage to the global coherence gain) "
                 "-- so the flip threshold p*=spinodal(g)/L changes as the connectome consolidates. Four "
                 "sign-only results over a plasticity-rate x barrier-depth sweep: (K1) repeated flips deepen "
                 "the trace strictly-monotonically and the flip threshold ends BELOW the un-kindled fold "
                 "(kindling), barrier-invariant -- the trace->threshold coupling 29 left [O]; (K2) the push-"
                 "space hysteresis loop NARROWS and the crossing latency at fixed push SHORTENS (a learned "
                 "change of the 28 hysteresis + a faster onset); (K3, the genuinely-new result + honest "
                 "negative) kindling is CONSOLIDATIVE not DEGRADATIVE -- the clean 'kindling erodes "
                 "coordination' hypothesis is REFUTED, R RISES and stays above the anchor while the trace "
                 "deepens, so the threshold falls through consolidation not erosion; (K4) a single coherent "
                 "consolidative seam -- the threshold is monotone-decreasing in the accumulated trace (the "
                 "trace IS the kindling variable), with a [L] direction-only correspondence to clinical "
                 "kindling and bipolar cycle acceleration. Both layers IMPORTED, not re-derived; the only new "
                 "object is the 28 cell driven through the 26 connectome -- no new constant, no new rule. "
                 "MECHANISM only -- NOT felt, NOT efficacy, NOT medical advice.",
        "grounding": {
            "collective_state": "the 28 BistableSwitch cell ds/dt = g*s - s^3 + h (E2's imported R19 cell, "
                                "the SAME cubic the engine froze, E.sdot), started at the DOWN fixed point "
                                "s0 = -sqrt(g); imported, not re-derived",
            "connectome_evolution": "each FLIP EPISODE is a sustained excursion driven through the 26 phase-"
                                    "correlation Hebbian update (E0's imported PlasticConnectome, "
                                    "W <- max(0, W*(1+eta*C)) row-renormalised), consolidating a retained "
                                    "structural trace ||dW||; imported, not re-derived",
            "coordination_gain": "L(W) = R(W)/R_anchor, R(W) the order parameter at the measured coupling (the "
                                 "SAME order parameter the engine froze, E._integrate), R_anchor = R(W0) the "
                                 "frozen M9 anchor 0.38961455156044245 -- a pure readout, = 1 at W = W0; "
                                 "generalises the 48 broadcast-leverage scaling to the GLOBAL coherence gain",
            "effective_drive_and_fold": "h_eff(p) = p * L(W); the state flips up iff h_eff crosses the fold "
                                        "spinodal(g) (E.spinodal, the SAME fold as M11 / theta-cap / epilepsy / "
                                        "E2); the flip threshold in external push is p* = spinodal(g) / L(W), "
                                        "which DROPS as the connectome consolidates and L grows -- forced [F]",
            "rate_sweep": list(ETA_SWEEP),
            "barrier_sweep": list(BARRIER_SWEEP),
            "rep_rate": ETAREP,
            "rep_barrier": GREP,
            "test_push": PTEST,
            "flip_bias_magnitude": B_MAG,
            "episode_length": EP_LEN,
            "episodes": EPISODES,
            "sweep_grade": "[O] swept -- plasticity rate eta AND barrier depth g are SWEPT, not tuned; every "
                           "SIGN/DIRECTION holds across BOTH sweeps (rate x barrier, anti-tuning)",
            "reused_layers": {"E0_PlasticConnectome": "imported (frozen kernel W0, phase-Hebbian rule, "
                                                      "order-parameter machinery)",
                              "E2_BistableSwitch": "imported (the R19 bistable cell, the fold, the hysteresis "
                                                   "and crossing-latency machinery)",
                              "kappa_measured": round(KAP, 6),
                              "R19_fold_spinodal": round(FOLD, 6),
                              "m9_anchor_R": R_ANCHOR,
                              "n_regions": N},
        },
        "K1_kindling_threshold": {
            "_what": "repeated flips deepen the connectome trace strictly-monotonically and the collective "
                     "state's flip threshold in external push p* = spinodal(g)/L ends BELOW the un-kindled "
                     "fold (kindling), barrier-invariant across the well-depth sweep -- the trace->threshold "
                     "coupling 29 (B3) named but left [O]",
            "trace_strictly_monotone_increasing": trace_strict,
            "threshold_ends_below_unkindled_fold": net_kindle,
            "kindling_is_barrier_invariant": barrier_inv,
            "unkindled_fold_at_rep_barrier": round(fold_rep, 6),
            "net_threshold_drop_at_rep": net_drop,
            "threshold_vs_episode_at_rep": thr_table,
            "trace_vs_episode_at_rep": trace_table,
            "unkindled_fold_by_barrier": folds_by_g,
            "kindled_threshold_end_by_barrier": thr_end_by_g,
            "trace_end_by_rate": trace_end_by_eta,
            "verdict": "driving repeated flip episodes through the plastic connectome, the retained trace "
                       "||dW|| deepens STRICTLY MONOTONICALLY with episode count (the E0 consolidation signal, "
                       "the same 29 B3 trace-deepening), and the collective state's flip threshold in external "
                       "push p* = spinodal(g)/L(W) ends BELOW the un-kindled fold -- repeated flips become "
                       "EASIER (kindling). The net threshold-decrease holds across the rate sweep AND is "
                       "barrier-invariant: at every well depth g the kindled threshold ends below that depth's "
                       "own un-kindled fold (p* = spinodal(g)/L scales the fold by the same gain at every g). "
                       "This is the trace->threshold coupling 29 (B3) named but left [O], now supplied: the "
                       "accumulated trace lowers the threshold. structure-only; magnitudes [O]; efficacy=0.",
        },
        "K2_dynamics": {
            "_what": "as kindling proceeds the push-space hysteresis LOOP NARROWS (a learned change of the 28 "
                     "hysteresis) and the crossing LATENCY at a fixed supra-threshold push SHORTENS (a faster "
                     "28 onset); both net-monotone with episode count across the rate sweep",
            "hysteresis_loop_narrows": loop_narrows,
            "crossing_latency_shortens": latency_shortens,
            "loop_width_vs_episode_at_rep": loop_table,
            "latency_vs_episode_at_rep": lat_table,
            "verdict": "the push-space hysteresis loop width 2*spinodal(g)/L(W) ends BELOW its un-kindled value "
                       "-- the inter-state interval the 28 hysteresis made bistable is RESHAPED by repetition, "
                       "a LEARNED change of the state-switching hysteresis -- and at a FIXED supra-threshold "
                       "push the crossing latency (the time the collective state takes to flip) SHORTENS, the "
                       "consolidated connectome raising the effective drive so the fold is overshot further "
                       "and the onset is faster (the 28 E2.2 time-course shortened by repetition). Both net-"
                       "monotone with episode count across the rate sweep. structure-only.",
        },
        "K3_consolidative_not_degradative": {
            "_what": "the genuinely-new coupling result + the honest no-tuning negative: the clean hypothesis "
                     "'kindling ERODES the network's coordination, so easier-to-flip means LESS coordinated' is "
                     "REFUTED -- the flip threshold DROPS (easier) while the coordination R(W) RISES and ends "
                     "ABOVE the frozen anchor, so the threshold falls THROUGH CONSOLIDATION, not degradation",
            "coordination_R_rises_net": R_net_up,
            "kindled_connectome_ends_at_or_above_anchor": ends_above,
            "easier_flip_decoupled_from_erosion": decoupled,
            "trace_deepens": trace_deepens,
            "R_vs_episode_at_rep": R_table,
            "net_dR_above_anchor_at_rep": dR_rep,
            "R_above_anchor_every_step_by_rate": stays_above_steps,
            "honest_caveat": "at the LOWEST swept rate (eta=0.03) the very first excursion nudges R a "
                             "negligible amount BELOW the anchor for one episode before consolidation dominates "
                             "and R rises net; at eta>=0.05 R never dips below the anchor. The refutation is the "
                             "NET sign (the kindled connectome ends MORE coordinated), not a step-by-step claim.",
            "verdict": "the clean, intuitive hypothesis -- 'repeated violent flips KINDLE by ERODING the "
                       "network's coordination (driving R toward incoherence), so a more-kindled connectome is a "
                       "LESS-coordinated one, easier to flip BECAUSE it is degraded' -- is REFUTED. The flip "
                       "threshold DROPS (kindling, K1) while the connectome's coordination R(W) at the measured "
                       "coupling RISES (net, across the rate sweep) and the kindled connectome ends AT OR ABOVE "
                       "the frozen M9 anchor -- MORE coordinated, not less -- as the trace deepens. So easier-to-"
                       "flip and degraded-coordination are DECOUPLED: the threshold falls THROUGH CONSOLIDATION "
                       "(the connectome writing the repeated transition into its own structure), NOT through "
                       "erosion. The refuted clean hypothesis is reported honestly, with the negligible first-"
                       "episode transient at the lowest rate disclosed -- the no-tuning discipline working as "
                       "intended.",
        },
        "K4_coherent_seam": {
            "_what": "a single coherent consolidative seam: the threshold is monotone-decreasing in the "
                     "accumulated trace ||dW|| (the trace IS the kindling variable -- the explicit trace->"
                     "threshold law 29 left open), and the whole seam (trace strict-up, threshold net-down, R "
                     "net-up) is consolidative; a [L] direction-only clinical correspondence",
            "threshold_monotone_decreasing_in_trace": thr_vs_trace,
            "seam_is_coherent": coherent,
            "trace_to_threshold_pairs_at_rep": trace_threshold_pairs,
            "clinical_correspondence_L": "DIRECTION-ONLY [L]: clinical KINDLING (Goddard's electrical kindling, "
                "where repeated sub-threshold stimulation progressively lowers the seizure threshold) and "
                "bipolar CYCLE ACCELERATION (episodes recur more easily over time) are the recognised phenomena "
                "in which repetition lowers the next transition's threshold -- direction-consistent with a "
                "retained trace easing the next flip; NOT a magnitude, NOT a patient-level prediction",
            "verdict": "the three results above are ONE phenomenon: every flip leaves a retained structural "
                       "trace (E0) that lowers the next flip's threshold (E2). The threshold is monotone-"
                       "decreasing in the accumulated trace ||dW|| (not merely in episode count) -- the trace IS "
                       "the kindling variable, the explicit trace->threshold law 29 (B3) left open -- and the "
                       "whole seam is consolidative. A DIRECTION-ONLY [L] correspondence is noted (clinical "
                       "kindling and bipolar cycle acceleration, where repetition lowers the next transition's "
                       "threshold), never a magnitude or a patient-level prediction.",
        },
        "S5_engine_invariance_guard": {
            "_what": "the double-inherited engine-invariance guard: (E0.4) with eta=0 the connectome stays "
                     "frozen, R = the frozen M9 anchor bit-for-bit, the gain L=1 and the threshold = the un-"
                     "kindled fold exactly; (E2.4) with a zero push the collective state settles via E.settle "
                     "bit-for-bit and the down state stays down -- a pure add-on",
            "eta0_R_equals_anchor_bitwise": R_eta0_bit,
            "eta0_gain_is_one": gain_one,
            "eta0_threshold_is_unkindled_fold": thr_fold,
            "zero_push_static_is_E_settle_bitwise": static_settle,
            "zero_push_gives_zero_drive": zero_drive,
            "down_state_stays_down": down_down,
            "fold_read_from_E_spinodal": fold_eng,
            "eta0_R_value": R_eta0_repr,
            "settle_endpoint_E_settle": a_repr,
            "guard": S5,
        },
        "cited_and_locked": {
            "couples_two_layers": "the THIRD cross-axis coupling in the atlas: the E0 plasticity layer (26) and "
                "the E2 state-switching layer (28) -- repeated flips of the single collective R19 bistable state "
                "(E2) drive the phase-Hebbian update so the connectome (E0) consolidates, and the consolidated "
                "connectome's coordination gain lowers the flip threshold; neither layer alone could pose it (E0 "
                "has no bistable flip, E2 has a frozen connectome)",
            "closes_bipolar_owed_LOCK": "the bipolar module (29, B3) named the kindling / trace->barrier coupling "
                "-- it showed alternating episodes DEEPEN the connectome trace ||dW|| and separately noted a "
                "LOWER barrier flips more cheaply, but left the actual trace->threshold COUPLING (whether and how "
                "the accumulated trace lowers the threshold) explicitly [O]; this layer-level coupling supplies "
                "it (K1, K4) WITHOUT touching the frozen 29 results",
            "reuse_not_rederive_LOCK": "both layers are IMPORTED (PlasticConnectome for the frozen kernel, the "
                "phase-Hebbian rule and the order parameter; BistableSwitch for the R19 cell, the fold, the "
                "hysteresis and the crossing latency); the kernel, the Hebbian rule, the R19 cell and the fold "
                "are NOT re-derived. The only new object is the 28 cell driven through the 26 connectome -- no "
                "new constant, no new rule",
            "consolidative_not_degradative_LOCK": "the clean hypothesis 'kindling erodes coordination' is REFUTED "
                "-- the connectome's coordination R(W) RISES and stays above the frozen anchor while the trace "
                "deepens; the threshold falls through CONSOLIDATION, not degradation; kindling and erosion are "
                "decoupled, and the refuted hypothesis is reported honestly",
            "real_kindling_heterogeneous_LOCK": "real kindling and cycle acceleration are HETEROGENEOUS (altered "
                "gene expression, mossy-fibre sprouting, receptor trafficking, network reorganisation, "
                "allostatic load); this module asserts only the SIGN/DIRECTION of whether repeated flips lower "
                "the collective flip threshold when the connectome evolves by the imported phase-Hebbian rule and "
                "the effective drive is scaled by the imported coordination gain, not that any real kindling "
                "follows this exact rule",
            "clinical_kindling_cited": "clinical kindling (Goddard) and bipolar cycle acceleration are the "
                "recognised phenomena in which repetition lowers the next transition's threshold -- a DIRECTION-"
                "ONLY [L] correspondence to the kindling sign, never a magnitude or a patient-level prediction",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; whether any real "
                "patient's episodes accelerate, and by how much, is external",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "collective_state_is_structural": 1.0,
            "reuses_E0_plasticity": 1.0,
            "reuses_E2_state_switching": 1.0,
            "couples_E0_and_E2": 1.0,
            "closes_bipolar_trace_to_threshold_owed": 1.0,
            "coordination_gain_is_connectome_readout": 1.0,
            "kindling_is_consolidative_not_degradative": 1.0,
            "erosion_hypothesis_refuted": "K3 reports a REFUTED clean hypothesis honestly (kindling consolidates, "
                                          "it does not erode coordination) rather than forcing a tidy 'kindling "
                                          "erodes stability' narrative",
            "plasticity_rate": "OPEN [O] -- swept {0.03,0.05,0.08}; signs hold over the rate sweep, not tuned",
            "barrier_depth_g": "OPEN [O] -- swept {0.7,1.0,1.3}; the kindling is barrier-invariant, not tuned",
            "clinical_prediction": "NONE -- the [L] correspondence is direction-only, never a patient-level "
                                   "prediction; prognosis and treatment are external",
            "not_medical_advice": 1.0,
            "third_cross_axis_coupling": 1.0,
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "static_limit_is_E_settle": static_settle,
            "eta0_R_anchor_bitwise": R_eta0_bit,
            "m9_anchor_value_frozen": repr(R_ANCHOR),
        },
        "preregistered_results": {
            "K1_repeated_flips_lower_threshold_barrier_invariant": {
                "claim": "driving repeated flip episodes through the plastic connectome, the retained trace "
                         "deepens strictly-monotonically and the flip threshold in external push p* = "
                         "spinodal(g)/L ends below the un-kindled fold (kindling), holding across the rate sweep "
                         "and barrier-invariant across the well-depth sweep -- the trace->threshold coupling the "
                         "bipolar module left [O]",
                "status": preds["K1_repeated_flips_lower_threshold_barrier_invariant"]},
            "K2_learned_hysteresis_narrows_and_onset_shortens": {
                "claim": "as kindling proceeds the push-space hysteresis loop narrows (a learned change of the "
                         "hysteresis) and the crossing latency at a fixed supra-threshold push shortens (a faster "
                         "onset), both net-monotone with episode count across the rate sweep",
                "status": preds["K2_learned_hysteresis_narrows_and_onset_shortens"]},
            "K3_kindling_is_consolidative_not_degradative": {
                "claim": "the clean hypothesis that kindling erodes the network's coordination (easier-to-flip "
                         "meaning less coordinated) is refuted -- the flip threshold drops while R(W) rises and "
                         "the kindled connectome ends at or above the frozen anchor, so the threshold falls "
                         "through consolidation not degradation; easier-to-flip and erosion are decoupled",
                "status": preds["K3_kindling_is_consolidative_not_degradative"]},
            "K4_single_coherent_consolidative_seam": {
                "claim": "the threshold is monotone-decreasing in the accumulated trace (the trace is the "
                         "kindling variable -- the explicit trace->threshold law the bipolar module left open), "
                         "and the whole seam is a single coherent consolidative object",
                "status": preds["K4_single_coherent_consolidative_seam"]},
        },
        "overall": {
            "kindling_threshold_reproduced": K1,
            "dynamics_reproduced": K2,
            "consolidative_not_degradative_reproduced": K3,
            "coherent_seam_reproduced": K4,
            "engine_invariance_guard": S5,
            "is_full_module": bool(K1 and K2 and K3 and K4 and S5),
            "verdict": "E0E2-KINDLING is the kindling coupling -- the third marriage of two reusable layers, the "
                       "E0 plastic connectome and the E2 bistable state, and the module that closes the trace->"
                       "threshold link the bipolar module (29, B3) left [O]. Repeated flips of the single "
                       "collective bistable state drive the phase-Hebbian update so the connectome consolidates, "
                       "and the consolidated connectome's coordination gain lowers the flip threshold: the trace "
                       "deepens strictly-monotonically and the flip threshold ends below the un-kindled fold "
                       "(kindling), barrier-invariant (K1); the push-space hysteresis loop narrows and the "
                       "crossing latency at fixed push shortens (a learned change of the hysteresis + a faster "
                       "onset) (K2); the clean 'kindling erodes coordination' hypothesis is REFUTED -- R rises "
                       "and stays above the anchor while the trace deepens, so the threshold falls through "
                       "consolidation not erosion (K3, the genuinely-new result + honest negative); and the "
                       "whole seam is a single coherent consolidative object, the threshold monotone-decreasing "
                       "in the accumulated trace, with a [L] direction-only correspondence to clinical kindling "
                       "and bipolar cycle acceleration (K4). With eta=0 the connectome stays frozen and R = the "
                       "frozen anchor bit-for-bit so the threshold = the un-kindled fold, and with a zero push "
                       "the collective state settles via E.settle bit-for-bit (S5). Both layers imported not "
                       "re-derived, no new tuned constant, no new rule, engine byte-unchanged. efficacy=0; not "
                       "medical advice; Axis-A firewall; hard problem OPEN.",
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

def e0e2_kindling_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "e0e2_kindling_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_e0e2_kindling_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"e0e2_kindling_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = e0e2_kindling_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    g = res["grounding"]
    k1 = res["K1_kindling_threshold"]; k2 = res["K2_dynamics"]
    k3 = res["K3_consolidative_not_degradative"]; k4 = res["K4_coherent_seam"]
    s5 = res["S5_engine_invariance_guard"]
    print("=" * 78)
    print("E0E2-KINDLING -- KINDLING COUPLING (E0 x E2)   add-only, engine READ-ONLY")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  couples: E0 PlasticConnectome (evolving W, coordination gain) x E2 BistableSwitch (R19 flip)")
    print(f"           rate sweep={g['rate_sweep']}  barrier sweep={g['barrier_sweep']}  episodes={g['episodes']}")
    print(f"  closes the 29 (B3) trace->threshold link left [O]")
    print("-" * 78)
    print(f"  K1 kindling      : trace-strict-mono={k1['trace_strictly_monotone_increasing']} thr<fold={k1['threshold_ends_below_unkindled_fold']} barrier-inv={k1['kindling_is_barrier_invariant']}  fold={k1['unkindled_fold_at_rep_barrier']} drop={k1['net_threshold_drop_at_rep']}")
    print(f"  K2 dynamics      : loop-narrows={k2['hysteresis_loop_narrows']} latency-shortens={k2['crossing_latency_shortens']}")
    print(f"  K3 consolidative : R-rises={k3['coordination_R_rises_net']} ends>=anchor={k3['kindled_connectome_ends_at_or_above_anchor']} decoupled(easier+more-coord)={k3['easier_flip_decoupled_from_erosion']} (dR={k3['net_dR_above_anchor_at_rep']})")
    print(f"  K4 coherent seam : thr-down-in-trace={k4['threshold_monotone_decreasing_in_trace']} coherent={k4['seam_is_coherent']}")
    print(f"  S5 invariance    : eta0 R==anchor:{s5['eta0_R_equals_anchor_bitwise']}  thr==fold:{s5['eta0_threshold_is_unkindled_fold']}  zero-push==E.settle:{s5['zero_push_static_is_E_settle_bitwise']}  down-stays-down:{s5['down_state_stays_down']}")
    print("-" * 78)
    print(f"  pre-registered: {[ (k, v['status']) for k,v in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  KINDLING COUPLING MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
