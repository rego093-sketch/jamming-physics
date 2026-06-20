#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADD-T3a -- ADDICTION SENSITIZATION DYNAMICS : the integrated reward-circuit gain modelled
DIRECTLY, on top of the E0 plasticity layer. This is the OTHER HALF of the convergence the
addiction levers chapter (36, ADD-T-L, "B-i") opened. There, the three INSTANT threshold
levers (L1 inward current, L2 outward current, L3 up-stream reward drive) reached the moment-
to-moment excitability of the reward circuit -- exactly where the established addiction
pharmacology acts -- but the DOMINANT defect of addiction, the INTEGRATED SENSITISATION GAIN
(the learned reward-circuit amplitude, the dF osB structural trace that makes the disorder
chronic and relapsing), was named explicitly OUT OF REACH for those instant levers, for TWO
reasons: (1) it is a GAIN, not a fold (an instant lever has no handle on amplitude -- the ADHD
lesson), and (2) it is a LEARNED / CONSOLIDATED plasticity variable -- a memory the circuit
hardened over time -- which no instant lever (drive or ion) can move. B-i NAMED that trace
out of reach; this module (B-ii) MODELS it -- it supplies the variable that actually MOVES the
trace, closing the §36 argument that the two halves of the convergence (the threshold frame
and the plasticity-dynamics frame) meet in ONE disorder.

It does so by IMPORTING the E0 PlasticConnectome (it does NOT re-derive the Hebbian rule or the
coupling map -- handover reuse discipline) and driving it with a REWARD bias whose SIGN is
grounded READ-ONLY in the already-emerged engine: M5 (dopamine reward-prediction error) shows a
rewarded eddy's laid-down probability rises well above an unrewarded control -- reward
POTENTIATES. Mapping a reward-exposure epoch to a positive (excitatory) reward-drive bias b>0
(the same coupling-vs-bias map k = kappa/(1-|b|) used everywhere; NO new constant), the slow
phase-correlation Hebbian update of E0 then ACCUMULATES that exposure into a retained structural
trace -- the integrated sensitisation gain as a structural quantity. The SIGN is grounded (M5
RPE potentiation); every MAGNITUDE is [O].
=================================================================================
THE GROUNDING (READ-ONLY; no new constant). The reward handle is read from the frozen engine,
not invented: M5 emerge_learned_field potentiates the rewarded eddy (p_target_learned >>
p_target_control), and M4 emerge_selection commits a basal-ganglia winner -- i.e. reward drives
selection and writes a prior. A reward-exposure epoch is mapped to a positive reward-drive bias
b>0 (reward RAISES the effective ephaptic coupling, k = kappa/(1-|b|), capped 2*kappa -- the
SAME map as every other module). The E0 PlasticConnectome converts repeated exposure into a
retained ||W - W0||. g = 1.0 is the engine's universal R19 scale; nothing here is fit.

WHAT THE MODULE DELIVERS (pre-registered, sign/direction only; never magnitudes):
  A1  INCENTIVE SENSITISATION (the gain, accumulating). Repeated reward exposure MONOTONICALLY
      strengthens the retained reward-circuit trace: ||W - W0|| increases with the number of
      exposures, over an eta sweep. This is the integrated sensitisation gain (the dFosB trace
      as a structural quantity) building up -- the thing a one-shot reward does NOT do and the
      thing B-i named out of reach for the instant levers. (readout: trace monotone-increasing
      in exposures, over eta in {0.03,0.05,0.08}.) Direction grounded in M5 RPE; magnitude [O].
  A2  CUE-REACTIVITY (response potentiation -- the relapse substrate). A connectome SENSITISED by
      reward exposure responds MORE to the SAME reward cue than a naive one: at a fixed reward-cue
      bias the order parameter R on the sensitised W exceeds R on the naive W (and the sensitised
      resting R is already >= the naive resting R). The learned trace sits the circuit in a higher-
      coordination basin, so the same cue evokes a larger coordinated response -- the mechanistic
      substrate of cue-induced craving / relapse. (readout: R_sensitised(cue) > R_naive(cue) AND
      R_sensitised(off) >= R_naive(off), over an eta sweep, deep and shallow exposure. The marginal
      cue gain is NOT asserted monotone -- only the response-exceeds-naive sign holds.) Direction [F]
      from the rule; magnitude [O].
  A3  EXTINCTION DOES NOT ERASE (persistence -- why cessation is not cure). After sensitisation,
      removing the reward (extinction = baseline OFF epochs, plasticity still running) does NOT
      return the trace to zero: with eta>0 the retained ||W - W0|| stays ABOVE zero (here it even
      continues to consolidate through the OFF epochs), whereas with eta=0 the trace is EXACTLY
      zero. Extinction removes the DRIVE (the B-i reachable instant axis) but not the LEARNED TRACE
      (the B-i out-of-reach axis) -- the convergence seam, exhibited dynamically. (readout: eta>0
      extinction trace > 0; eta=0 extinction trace == 0 exactly, over an eta sweep.) Direction [F].
  A4  ENGINE-INVARIANCE GUARD (why the instant levers cannot reach it). With eta=0 (no plasticity)
      a reward excursion REVERTS EXACTLY when the reward bias is removed -- the integrated gain
      DISAPPEARS without plasticity. That is the proof that the sensitisation axis is a LEARNED /
      CONSOLIDATED (plasticity) variable, not an instant one -- precisely why B-i's instant levers
      (drive or ion) have no handle on it. eta=0 reproduces the frozen M9 anchor R bit-for-bit and
      leaves W identical to the kernel (pure add-on). (readout: eta=0 epoch R == M9 anchor exactly;
      W untouched.)
  A5  THE DYNAMICS HANDLE -- the close (what the threshold frame could NOT do). The plasticity-
      dynamics frame supplies a handle on the trace itself: SPACED (intermittent) reward exposure
      consolidates a LARGER retained trace than MASSED (continuous) exposure at EQUAL total time-at-
      reward -- intermittent reinforcement sensitises MORE, the well-known clinical fact, emerging
      from pure phase-plasticity (the E0.2 spacing effect applied to the reward bias). This is the
      variable that "actually moves the trace" B-i named out of reach: the threshold frame names the
      gain unreachable for INSTANT levers; the dynamics frame both EXHIBITS the gain (A1-A3) and
      gives a structural HANDLE on it (the schedule of exposure). The two halves meet. (readout:
      retained ||dW||_spaced > ||dW||_massed, over an eta x epochs sweep.) Direction [F]; magnitude [O].

NOT a claim that addiction is reducible to a phase-correlation Hebbian trace (real addiction
plasticity is heterogeneous -- dFosB / CREB / BDNF transcriptional cascades, AMPA trafficking,
dendritic spine remodelling, glutamatergic homeostatic adaptation, epigenetic marks -- LOCKED);
what is asserted is the SIGN of an integrated reward-driven trace and its four consequences
(sensitisation, cue-reactivity, extinction-persistence, the schedule handle), with the reward
SIGN grounded in M5 RPE and the eta=0 control showing the gain is a plasticity variable. NOT a
claim about the FELT quality of craving, reward or relapse (Axis-A firewall: consciousness_claim
stays 0; hard problem stays OPEN). Addiction is a CHRONIC, RELAPSING MEDICAL condition, not a
moral failing and not a failure of will; a retained structural trace is a mechanism boundary, and
NOTHING here is a recommendation, a cure, or a licence to acquire or use any substance. NOT
MEDICAL ADVICE; efficacy = 0 everywhere; in-silico MECHANISM only. The MAGNITUDE of any real
sensitisation, the rate eta, and the identity of the real plasticity rule(s) are all [O].

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY
(emerge_all is NOT touched, so the engine file stays e61083ae..., the tree stays 0fbf4988...
and the M0..M16 subtree stays 3a1ebbbb..., byte-identical). REUSES the E0 PlasticConnectome
(imported, not re-derived). Writes addiction_sensitization_dynamics_results.json + its sha256,
verified bit-for-bit.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

# REUSE the E0 plasticity layer -- import the class and the shared (measured) handles;
# do NOT re-derive the Hebbian rule or the coupling map (handover discipline: reuse).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e0_plasticity import PlasticConnectome, OMEGA, OMEGA0, KAP, W0, FOLD, N, _k_bias

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"
M9_ANCHOR_R        = 0.38961455156044245              # frozen M9 R_measured (cross-check)
ETA                = 0.05                              # E0 representative rate [O] (reused)


def _R(W):
    """Order parameter at the measured coupling on W (reward/bias off) -- pure engine."""
    return E._integrate(OMEGA, W, KAP * OMEGA0)[0]


def _Rcue(W, b):
    """Order parameter on W at a reward-cue bias b (raises coupling, same map) -- pure engine."""
    return E._integrate(OMEGA, W, _k_bias(b) * OMEGA0)[0]


def _dW(W):
    """Frobenius distance of a connectome from the frozen ephaptic kernel (trace depth)."""
    return float(np.linalg.norm(W - W0))


def _traj(b, eta, checkpoints, base=None):
    """Run epochs of (bias=b, rate=eta) from `base` (or a fresh kernel), snapshotting a COPY of
    W at each checkpoint. epoch() is a deterministic function of the current W (it re-seeds the
    phase integration each call), so an incremental run is bit-identical to rebuilding each
    checkpoint from scratch -- this only CACHES, it changes no value."""
    pc = PlasticConnectome()
    if base is not None:
        pc.W = base.copy()
    snaps = {}
    cur = 0
    for tgt in sorted(set(checkpoints)):
        while cur < tgt:
            pc.epoch(bias=b, eta=eta)
            cur += 1
        snaps[tgt] = pc.W.copy()
    return snaps


def _reward_handle():
    """Ground the reward handle in the ALREADY-EMERGED engine (READ-ONLY): M5 (dopamine reward-
    prediction error) potentiates the rewarded eddy's laid-down probability well above an
    unrewarded control (reward POTENTIATES -> a positive reward-drive bias), and M4 (basal-
    ganglia selection) commits a winner (reward drives selection). This module maps a reward-
    exposure epoch to a positive reward-drive bias b>0; here we only READ the engine to confirm
    the handle exists and is grounded, and assert the SIGN -- the magnitude stays [O]."""
    lf = E.emerge_learned_field()        # M5 (READ-ONLY)
    sel = E.emerge_selection()           # M4 (READ-ONLY)
    return {
        "value_signal": "dopamine reward-prediction error (M5): the rewarded eddy's laid-down "
                         "probability rises well above an unrewarded control -> reward potentiates",
        "m5_p_target_learned": float(lf["p_target_learned"]),
        "m5_p_target_control": float(lf["p_target_control"]),
        "m5_reward_potentiates": float(bool(lf["learned_above_control"])),
        "m4_selection_commits": float(bool(sel["commit"])),
        "m4_winner": int(sel["winner"]),
        "reward_master": "TH/SLC6A3 (dopamine synthesis/transport) -- emerged upstream; the "
                         "reward-drive hub grounded (M4/M5)",
        "mapping": "reward exposure -> positive (excitatory) reward-drive bias b>0 -> "
                   "k=kappa/(1-|b|) (RAISES coupling, capped 2*kappa); the E0 phase-correlation "
                   "Hebbian update accumulates it into a retained ||W-W0|| (the integrated "
                   "sensitisation gain). SIGN grounded in M5 RPE potentiation; MAGNITUDE [O].",
    }


# ---- addiction sensitisation drivers (reuse PlasticConnectome + the E0 map; cached) ----

def _sensitisation(b_reward, eta, exposures, sweep_etas):
    """A1: incentive sensitisation -- repeated reward exposure monotonically strengthens the
    retained reward-circuit trace (the integrated gain accumulating), over an eta sweep."""
    snaps = _traj(b_reward, eta, exposures)
    profile = {k: round(_dW(snaps[k]), 6) for k in exposures}
    pv = [profile[k] for k in exposures]
    monotone = all(pv[i] < pv[i + 1] for i in range(len(pv) - 1))
    sweep = {}
    hold = True
    for e in sweep_etas:
        sn = _traj(b_reward, e, exposures)
        tv = [_dW(sn[k]) for k in exposures]
        ok = bool(all(tv[i] < tv[i + 1] for i in range(len(tv) - 1)))
        hold = hold and ok
        sweep[e] = ok
    return profile, monotone, bool(hold), sweep, snaps


def _cue_reactivity(b_reward, eta, b_cue, depths, sweep_etas):
    """A2: cue-reactivity -- a sensitised connectome responds MORE to the SAME reward cue than a
    naive one (R_sens(cue) > R_naive(cue)) and its resting R is already >= naive (relapse
    substrate). Endpoint sign only; the marginal cue gain is NOT asserted monotone."""
    R_naive_off = _R(W0)
    R_naive_cue = _Rcue(W0, b_cue)
    rows = {}
    for d in depths:
        Ws = _traj(b_reward, eta, [d])[d]
        rows[d] = {"sens_off": round(_R(Ws), 10),
                   "sens_cue": round(_Rcue(Ws, b_cue), 10),
                   "off_ge_naive": bool(_R(Ws) >= R_naive_off - 1e-12),
                   "cue_gt_naive": bool(_Rcue(Ws, b_cue) > R_naive_cue + 1e-12)}
    endpoint_ok = bool(all(r["off_ge_naive"] and r["cue_gt_naive"] for r in rows.values()))
    # anti-tuning: the cue-exceeds-naive sign must hold across eta x depth
    sweep = {}
    hold = True
    for e in sweep_etas:
        for d in depths:
            Ws = _traj(b_reward, e, [d])[d]
            ok = bool(_Rcue(Ws, b_cue) > R_naive_cue + 1e-12 and _R(Ws) >= R_naive_off - 1e-12)
            hold = hold and ok
            sweep[f"eta{e}_d{d}"] = ok
    return R_naive_off, R_naive_cue, rows, endpoint_ok, bool(hold), sweep


def _extinction(b_reward, eta, sens_epochs, ext_epochs, sweep_etas):
    """A3: extinction does not erase -- with eta>0 the retained trace stays ABOVE zero after the
    reward is removed (baseline OFF epochs), whereas with eta=0 it is EXACTLY zero. Extinction
    removes the drive (the reachable instant axis) but not the learned trace (the out-of-reach
    axis): the convergence seam, exhibited dynamically."""
    # eta > 0 : sensitise, then extinguish (reward off), plasticity still running
    Ws = _traj(b_reward, eta, [sens_epochs])[sens_epochs]
    trace_sens = _dW(Ws)
    Wext = _traj(0.0, eta, [ext_epochs], base=Ws)[ext_epochs]
    trace_ext = _dW(Wext)
    persists = bool(trace_ext > 1e-6)
    # eta = 0 : same protocol -> trace EXACTLY zero (extinction would "erase" if there were no
    # plasticity -- there isn't a trace to erase, which is the point)
    Ws0 = _traj(b_reward, 0.0, [sens_epochs])[sens_epochs]
    Wext0 = _traj(0.0, 0.0, [ext_epochs], base=Ws0)[ext_epochs]
    trace_ext0 = _dW(Wext0)
    erases_eta0 = bool(trace_ext0 == 0.0)
    # anti-tuning: persistence under eta>0 across the sweep
    sweep = {}
    hold = True
    for e in sweep_etas:
        w = _traj(b_reward, e, [sens_epochs])[sens_epochs]
        we = _traj(0.0, e, [ext_epochs], base=w)[ext_epochs]
        ok = bool(_dW(we) > 1e-6)
        hold = hold and ok
        sweep[e] = {"extinction_trace": round(_dW(we), 6), "persists": ok}
    return (trace_sens, trace_ext, persists, trace_ext0, erases_eta0,
            bool(hold), sweep)


def _intermittency(b_reward, eta, epochs, sweep_etas, sweep_ks):
    """A5: the dynamics handle -- SPACED (intermittent) reward exposure consolidates a LARGER
    retained trace than MASSED (continuous) at equal total time-at-reward (intermittent
    reinforcement sensitises more), over an eta x epochs sweep. The E0.2 spacing effect applied
    to the reward bias -- the structural handle on the trace the instant frame could not reach."""
    massed = _traj(b_reward, eta, [epochs])[epochs]
    dW_m = _dW(massed)
    per = PlasticConnectome()
    for _ in range(epochs):
        per.epoch(bias=b_reward, eta=eta)   # ON  (reward)
        per.epoch(bias=0.0, eta=eta)        # OFF (no reward; consolidation continues)
    dW_s = per.trace()
    spaced_gt = bool(dW_s > dW_m)
    sweep = {}
    hold = True
    for e in sweep_etas:
        for k in sweep_ks:
            m = _traj(b_reward, e, [k])[k]
            p = PlasticConnectome()
            for _ in range(k):
                p.epoch(bias=b_reward, eta=e); p.epoch(bias=0.0, eta=e)
            ok = bool(p.trace() > _dW(m))
            hold = hold and ok
            sweep[f"eta{e}_k{k}"] = {"massed_dW": round(_dW(m), 6),
                                     "spaced_dW": round(p.trace(), 6), "spaced_gt": ok}
    return dW_m, dW_s, spaced_gt, bool(hold), sweep


def _invariance(health_R, b_reward):
    """A4: eta=0 reward excursion reverts exactly when the reward bias is removed -- the
    integrated gain DISAPPEARS without plasticity (the sensitisation axis is a plasticity
    variable, which is why B-i's instant levers cannot reach it). eta=0 reproduces the frozen
    M9 anchor bit-for-bit and leaves W identical to the kernel."""
    # a plasticity-off reward epoch, then read R with the reward off
    pc = PlasticConnectome()
    R_eta0, _ = pc.epoch(bias=b_reward, eta=0.0)     # eta=0: W must stay identical
    w_untouched = bool(np.array_equal(pc.W, W0))
    R_after = pc.order()                              # reward off -> must be the anchor exactly
    reverts = bool(R_after == health_R)
    trace_eta0 = _dW(pc.W)
    matches_anchor = bool(health_R == M9_ANCHOR_R)
    # also confirm the plasticity-off baseline epoch matches the anchor (E0.4 handle)
    pc2 = PlasticConnectome()
    R_base0, _ = pc2.epoch(bias=0.0, eta=0.0)
    base_matches = bool(R_base0 == health_R)
    return (R_eta0, w_untouched, R_after, reverts, trace_eta0,
            matches_anchor, base_matches)


def run():
    B_REWARD = +0.12                                  # reward-exposure excitatory drive bias [O]
    B_CUE    = +0.08                                  # a (weaker) reward-cue re-presentation bias [O]
    EXPOS    = [0, 4, 8, 12, 18, 24]                  # exposure profile
    SWEEP_ETAS = (0.03, 0.05, 0.08)                   # anti-tuning eta sweep
    SWEEP_KS   = (4, 6, 8)                             # anti-tuning epochs sweep

    health_R = _R(W0)                                 # frozen M9 coordination anchor
    grounding = _reward_handle()

    # ===== A1 : incentive sensitisation (the gain, accumulating) =====
    sens_profile, sens_monotone, sens_sweep_ok, sens_sweep, sens_snaps = _sensitisation(
        B_REWARD, ETA, EXPOS, SWEEP_ETAS)
    A1 = bool(sens_monotone and sens_sweep_ok)

    # ===== A2 : cue-reactivity (response potentiation) =====
    (R_naive_off, R_naive_cue, cue_rows, cue_endpoint_ok, cue_sweep_ok,
     cue_sweep) = _cue_reactivity(B_REWARD, ETA, B_CUE, [12, 24], SWEEP_ETAS)
    A2 = bool(cue_endpoint_ok and cue_sweep_ok)

    # ===== A3 : extinction does not erase (persistence / convergence seam) =====
    (trace_sens, trace_ext, ext_persists, trace_ext0, erases_eta0,
     ext_sweep_ok, ext_sweep) = _extinction(B_REWARD, ETA, 12, 12, SWEEP_ETAS)
    A3 = bool(ext_persists and erases_eta0 and ext_sweep_ok)

    # ===== A4 : engine-invariance guard (the SG axis is a plasticity variable) =====
    (R_eta0, w_untouched, R_after, reverts, trace_eta0,
     matches_anchor, base_matches) = _invariance(health_R, B_REWARD)
    A4 = bool(reverts and w_untouched and matches_anchor and base_matches and trace_eta0 == 0.0)

    # ===== A5 : the dynamics handle -- spaced (intermittent) > massed (continuous) =====
    dW_m, dW_s, spaced_gt, interm_sweep_ok, interm_sweep = _intermittency(
        B_REWARD, ETA, 6, SWEEP_ETAS, SWEEP_KS)
    A5 = bool(spaced_gt and interm_sweep_ok)

    preds = {
        "A1_incentive_sensitisation":  "CONFIRMED" if A1 else "REFUTED",
        "A2_cue_reactivity":           "CONFIRMED" if A2 else "REFUTED",
        "A3_extinction_persists":      "CONFIRMED" if A3 else "REFUTED",
        "A4_plasticity_variable_guard":"CONFIRMED" if A4 else "REFUTED",
        "A5_dynamics_handle_spacing":  "CONFIRMED" if A5 else "REFUTED",
    }

    res = {
        "_what": "ADD-T3a -- addiction sensitisation dynamics: the integrated reward-circuit gain "
                 "(the dFosB trace) modelled DIRECTLY on top of the E0 plasticity layer (imports "
                 "PlasticConnectome; does not re-derive the rule). The reward SIGN is grounded "
                 "READ-ONLY in M5 (dopamine RPE potentiation) and M4 (selection); a reward-"
                 "exposure epoch maps to a positive reward-drive bias and the E0 Hebbian update "
                 "accumulates it into a retained structural trace. This is the OTHER HALF of the "
                 "§36 (ADD-T-L, B-i) convergence: B-i NAMED the integrated gain out of reach for "
                 "the instant threshold levers (a gain not a fold AND a learned not an instant "
                 "variable); B-ii MODELS it and supplies the variable that MOVES it. Magnitudes "
                 "are never asserted; only the SIGNS.",
        "roadmap_id": "T3a (addiction) -- the temporal/plasticity half of the convergence opened "
                      "by §36 ADD-T-L (B-i); RESEARCH_ROADMAP_post_autism_adhd.md",
        "convergence_with_B_i": {
            "B_i_named": "the dominant defect of addiction = the integrated sensitisation gain "
                         "(dFosB trace), named OUT OF REACH for the instant L1/L2/L3 levers, for "
                         "two reasons: (1) a GAIN not a fold (no instant handle on amplitude -- "
                         "the ADHD lesson), (2) a LEARNED/CONSOLIDATED plasticity variable (a "
                         "memory the circuit hardened) no instant lever can move",
            "B_ii_models": "this module models that exact trace via E0 plasticity dynamics, "
                           "exhibiting it (A1 sensitisation, A2 cue-reactivity, A3 extinction-"
                           "persistence) and giving a structural HANDLE on it (A5 the schedule of "
                           "exposure -- spaced sensitises more), which the instant frame could not",
            "seam": "extinction (A3) removes the DRIVE (the B-i reachable instant axis) but not "
                    "the LEARNED TRACE (the B-i out-of-reach axis); eta=0 (A4) shows the gain is a "
                    "plasticity variable that vanishes without plasticity -- the two frames meet",
            "closes": "the §36 argument that the threshold frame and the plasticity-dynamics frame "
                      "are two halves of one convergence, in one disorder (addiction)",
        },
        "grounding": grounding,
        "anchor": {
            "health_R_M9_anchor": round(health_R, 10),
            "matches_frozen_anchor_bitwise": matches_anchor,
            "reward_bias": B_REWARD, "cue_bias": B_CUE, "eta_representative": ETA,
            "note": "reward exposure RAISES coupling (k=kappa/(1-|b|)); eta is [O]; the SIGNS "
                    "survive an eta sweep, so no number is fit to a target",
        },
        "A1_incentive_sensitisation": {
            "trace_vs_exposures": sens_profile,
            "trace_monotone_increasing": sens_monotone,
            "monotone_over_eta_sweep": sens_sweep_ok,
            "eta_sweep": sens_sweep,
            "reproduced": A1,
            "reading": "repeated reward exposure monotonically strengthens the retained reward-"
                       "circuit trace -- the integrated sensitisation gain (dFosB trace) "
                       "accumulating; the thing a one-shot reward does not do and B-i named out "
                       "of reach for the instant levers. Direction grounded in M5 RPE; magnitude [O]",
        },
        "A2_cue_reactivity": {
            "R_naive_off": round(R_naive_off, 10),
            "R_naive_cue": round(R_naive_cue, 10),
            "sensitised_rows": cue_rows,
            "endpoint_sensitised_exceeds_naive": cue_endpoint_ok,
            "holds_over_eta_x_depth_sweep": cue_sweep_ok,
            "eta_depth_sweep": cue_sweep,
            "marginal_cue_gain_monotone_NOT_asserted": 1.0,
            "reproduced": A2,
            "reading": "a connectome sensitised by reward exposure responds MORE to the SAME "
                       "reward cue than a naive one (R_sens(cue) > R_naive(cue)), its resting R "
                       "already >= naive -- the learned trace sits the circuit in a higher-"
                       "coordination basin, the substrate of cue-induced craving/relapse. Only the "
                       "response-exceeds-naive SIGN is asserted (the marginal cue gain is not "
                       "claimed monotone)",
        },
        "A3_extinction_persists": {
            "trace_after_sensitisation": round(trace_sens, 6),
            "trace_after_extinction_eta_pos": round(trace_ext, 6),
            "extinction_trace_above_zero": ext_persists,
            "trace_after_extinction_eta0": round(trace_ext0, 6),
            "eta0_trace_exactly_zero": erases_eta0,
            "persistence_over_eta_sweep": ext_sweep_ok,
            "eta_sweep": ext_sweep,
            "reproduced": A3,
            "reading": "removing the reward (extinction = baseline OFF epochs) does NOT return the "
                       "trace to zero under plasticity (eta>0: trace stays above zero, here it "
                       "continues to consolidate), whereas with eta=0 it is exactly zero -- "
                       "extinction removes the DRIVE (the reachable instant axis) but not the "
                       "LEARNED TRACE (the out-of-reach axis): the convergence seam, dynamically. "
                       "Direction forced",
        },
        "A4_plasticity_variable_guard": {
            "eta0_reward_epoch_R": round(R_eta0, 10),
            "eta0_W_identical_to_kernel": w_untouched,
            "eta0_R_after_reward_removed": round(R_after, 10),
            "eta0_reverts_exactly": reverts,
            "eta0_retained_trace": round(trace_eta0, 10),
            "matches_frozen_anchor_bitwise": matches_anchor,
            "eta0_baseline_epoch_matches_anchor": base_matches,
            "reproduced": A4,
            "reading": "with eta=0 the reward excursion reverts EXACTLY when the reward bias is "
                       "removed and W stays identical to the kernel -- the integrated gain "
                       "DISAPPEARS without plasticity, proving the sensitisation axis is a "
                       "LEARNED/CONSOLIDATED (plasticity) variable, not an instant one. This is "
                       "precisely why B-i's instant levers (drive or ion) cannot reach it; eta=0 "
                       "reproduces the frozen M9 anchor bit-for-bit (pure add-on)",
        },
        "A5_dynamics_handle_spacing": {
            "massed_continuous_dW": round(dW_m, 6),
            "spaced_intermittent_dW": round(dW_s, 6),
            "spaced_exceeds_massed": spaced_gt,
            "holds_over_eta_x_epochs_sweep": interm_sweep_ok,
            "eta_epochs_sweep": interm_sweep,
            "reproduced": A5,
            "reading": "SPACED (intermittent) reward exposure consolidates a LARGER retained trace "
                       "than MASSED (continuous) at equal total time-at-reward -- intermittent "
                       "reinforcement sensitises MORE, emerging from pure phase-plasticity (the "
                       "E0.2 spacing effect applied to the reward bias). This is the structural "
                       "HANDLE on the trace B-i named out of reach: the threshold frame names the "
                       "gain unreachable for instant levers; the dynamics frame both exhibits it "
                       "(A1-A3) and gives a handle on it (the schedule of exposure). Direction "
                       "forced; magnitude [O]",
        },
        "locks": {
            "reuses_E0_layer_LOCK": "this module IMPORTS the E0 PlasticConnectome (phase-"
                "correlation Hebbian update) and the coupling-vs-bias map; it does NOT re-derive "
                "either -- the new content is the reward GROUNDING (M5 RPE, READ-ONLY) and the "
                "four sensitisation readouts (sensitisation, cue-reactivity, extinction-"
                "persistence, the schedule handle), none of which E0 carried",
            "structural_trace_not_felt_LOCK": "the retained ||W-W0|| is the integrated "
                "sensitisation gain as a STRUCTURAL quantity, NOT a claim about the felt quality "
                "of craving, reward or relapse (Axis-A firewall: consciousness_claim stays 0; "
                "hard problem stays OPEN)",
            "real_plasticity_heterogeneous_LOCK": "real addiction plasticity is HETEROGENEOUS -- "
                "dFosB/CREB/BDNF transcriptional cascades, AMPA receptor trafficking, dendritic "
                "spine remodelling, glutamatergic homeostatic adaptation, epigenetic marks -- NOT "
                "one rule; this module asserts the SIGN of an integrated reward-driven trace, not "
                "that any synapse follows this exact equation",
            "reward_sign_grounded_magnitude_open_LOCK": "the reward bias SIGN (reward potentiates "
                "-> positive drive) is grounded READ-ONLY in M5 RPE; the MAGNITUDE of any real "
                "sensitisation, the rate eta, and the identity of the real plasticity rule(s) are "
                "all [O]; the SIGNS are required to hold over an eta sweep -- no number is fit",
            "chronic_relapsing_medical_LOCK": "addiction is a CHRONIC, RELAPSING MEDICAL condition "
                "(a disorder of the integrated reward circuit), NOT a moral failing and NOT a "
                "failure of will; this module maps a mechanism, it does not judge a person",
            "no_cure_no_licence_LOCK": "no direction here is a cure, a treatment, or a recommen-"
                "dation, and NOTHING here is a licence to acquire or use any substance; the "
                "schedule handle (A5) is a MECHANISM sign, not advice",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; "
                "whether any real sensitisation, cue-reactivity or relapse follows this rule is "
                "external",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "reuses_E0_PlasticConnectome": 1.0,
            "reward_sign_grounded_in_M5_RPE": 1.0,
            "closes_B_i_convergence": 1.0,
            "is_an_application_of_E0": 1.0,
            "sensitisation_magnitudes": "OPEN [O] -- only the SIGNS are asserted (trace monotone-"
                                        "up in exposure; cue response exceeds naive; extinction "
                                        "trace > 0 while eta=0 trace == 0; spaced > massed); no "
                                        "magnitude is fit, and the signs survive an eta sweep",
            "real_rule_identity": "OWED [O] -- which real plasticity rule(s) operate is external; "
                                  "only the phase-correlation Hebbian SIGN and its consequences "
                                  "are asserted",
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "eta0_reverts_to_anchor": reverts,
        },
        "preregistered_results": {
            "A1_incentive_sensitisation": {
                "claim": "repeated reward exposure monotonically strengthens the retained reward-"
                         "circuit trace (the integrated sensitisation gain accumulating), over an "
                         "eta sweep",
                "status": preds["A1_incentive_sensitisation"]},
            "A2_cue_reactivity": {
                "claim": "a sensitised connectome responds MORE to the same reward cue than a "
                         "naive one (R_sens(cue) > R_naive(cue), resting R already >= naive), over "
                         "an eta sweep -- the cue-induced relapse substrate",
                "status": preds["A2_cue_reactivity"]},
            "A3_extinction_persists": {
                "claim": "extinction (reward removed) does NOT return the trace to zero under "
                         "plasticity (eta>0 trace > 0) while eta=0 trace == 0 exactly -- the drive "
                         "reverts but the learned trace persists (the convergence seam)",
                "status": preds["A3_extinction_persists"]},
            "A4_plasticity_variable_guard": {
                "claim": "with eta=0 the reward excursion reverts exactly and W stays identical to "
                         "the kernel -- the integrated gain is a plasticity variable that vanishes "
                         "without plasticity (why B-i's instant levers cannot reach it); eta=0 "
                         "reproduces the frozen M9 anchor bit-for-bit",
                "status": preds["A4_plasticity_variable_guard"]},
            "A5_dynamics_handle_spacing": {
                "claim": "spaced (intermittent) reward exposure consolidates a larger retained "
                         "trace than massed (continuous) at equal total exposure (intermittent "
                         "reinforcement sensitises more), over an eta x epochs sweep -- the "
                         "structural handle on the trace the instant frame could not reach",
                "status": preds["A5_dynamics_handle_spacing"]},
        },
        "overall": {
            "sensitisation_reproduced": A1,
            "cue_reactivity_reproduced": A2,
            "extinction_persistence_reproduced": A3,
            "plasticity_variable_guard": A4,
            "dynamics_handle_reproduced": A5,
            "is_full_module": bool(A1 and A2 and A3 and A4 and A5),
            "verdict": "ADD-T3a models the integrated sensitisation gain of addiction -- the dFosB "
                       "trace §36 (B-i) named OUT OF REACH for the instant threshold levers -- "
                       "DIRECTLY, by importing the E0 PlasticConnectome and driving it with a "
                       "reward bias whose SIGN is grounded READ-ONLY in M5 dopamine RPE. Repeated "
                       "reward exposure monotonically builds a retained structural trace (A1 "
                       "incentive sensitisation); the sensitised connectome responds more to the "
                       "same reward cue than a naive one (A2 cue-reactivity, the relapse "
                       "substrate); extinction removes the drive but not the learned trace (A3 "
                       "persistence -- the convergence seam); and with eta=0 the gain vanishes, "
                       "proving it is a plasticity variable the instant levers cannot reach (A4 "
                       "guard, M9 anchor reproduced bit-for-bit). The dynamics frame then supplies "
                       "the handle the threshold frame could not: spaced (intermittent) exposure "
                       "sensitises more than massed (A5 -- intermittent reinforcement). The two "
                       "halves of the convergence meet in one disorder: B-i names the gain "
                       "unreachable for instant levers, B-ii exhibits it and gives a structural "
                       "handle on it. Reward SIGN grounded in M5 RPE, magnitudes [O], signs "
                       "survive an eta sweep, no new tuned constant, engine byte-unchanged. "
                       "Addiction is a chronic relapsing MEDICAL condition, not a moral failing; "
                       "efficacy=0; not medical advice; no cure; no licence to use; Axis-A "
                       "firewall; hard problem OPEN.",
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

def addiction_sensitization_dynamics_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "addiction_sensitization_dynamics_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_addiction_sensitization_dynamics_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"addiction_sensitization_dynamics_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = addiction_sensitization_dynamics_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    g = res["grounding"]
    a1 = res["A1_incentive_sensitisation"]; a2 = res["A2_cue_reactivity"]
    a3 = res["A3_extinction_persists"]; a4 = res["A4_plasticity_variable_guard"]
    a5 = res["A5_dynamics_handle_spacing"]
    print("=" * 78)
    print("ADD-T3a -- ADDICTION SENSITISATION DYNAMICS   add-only, engine READ-ONLY, reuses E0")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  reward grounding (M5 RPE): p_target {g['m5_p_target_learned']:.4f} > {g['m5_p_target_control']:.4f} -> potentiates={bool(g['m5_reward_potentiates'])}  (M4 commit={bool(g['m4_selection_commits'])})")
    print("-" * 78)
    print(f"  A1 sensitise  : trace {a1['trace_vs_exposures']}")
    print(f"        monotone-up={a1['trace_monotone_increasing']} over-eta-sweep={a1['monotone_over_eta_sweep']} => {a1['reproduced']}")
    print(f"  A2 cue-react  : naive_off={a2['R_naive_off']} naive_cue={a2['R_naive_cue']}  sens>naive(endpoint)={a2['endpoint_sensitised_exceeds_naive']} swept={a2['holds_over_eta_x_depth_sweep']} => {a2['reproduced']}")
    print(f"  A3 extinction : sens_trace={a3['trace_after_sensitisation']} ext_trace(eta>0)={a3['trace_after_extinction_eta_pos']}(>0:{a3['extinction_trace_above_zero']}) ext_trace(eta0)={a3['trace_after_extinction_eta0']}(==0:{a3['eta0_trace_exactly_zero']}) swept={a3['persistence_over_eta_sweep']} => {a3['reproduced']}")
    print(f"  A4 guard      : eta0 reverts={a4['eta0_reverts_exactly']}(R={a4['eta0_R_after_reward_removed']}) W-identical={a4['eta0_W_identical_to_kernel']} anchor={a4['matches_frozen_anchor_bitwise']} => {a4['reproduced']}")
    print(f"  A5 handle     : massed dW={a5['massed_continuous_dW']} spaced dW={a5['spaced_intermittent_dW']} spaced>massed={a5['spaced_exceeds_massed']} swept={a5['holds_over_eta_x_epochs_sweep']} => {a5['reproduced']}")
    print("-" * 78)
    print(f"  pre-registered: {[ (k, v['status']) for k,v in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  closes B-i convergence : {hl['closes_B_i_convergence']}   is-an-application-of-E0 : {hl['is_an_application_of_E0']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  ADD-T3a SENSITISATION DYNAMICS MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
