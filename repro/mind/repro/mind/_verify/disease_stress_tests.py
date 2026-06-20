#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DISEASE STRESS-TESTS -- construct-validity probes for the shared R19 substrate.
=================================================================================
Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). This is an ADD-ONLY decision-check in
the EXACT v1.18 geometry_grounding.py mould:

  * the frozen engine (vp_mind_engine) is imported READ-ONLY; emerge_all() is NOT
    touched, so the engine tree stays 0fbf4988... and the M0..M16 output subtree
    stays 3a1ebbbb... (byte-identical). This file changes NOTHING in the engine;
  * it writes disease_stress_results.json + expected_disease_sha256.json and is
    verified bit-for-bit (C1) by run_regression.py.

WHAT A DISEASE TEST IS (and is NOT).  The question is construct validity: does the
NORMAL substrate, with its CITED parameters perturbed ONLY in the measured CLINICAL
DIRECTION, REPRODUCE a clinical syndrome?  It is NOT a claim that the perturbed
state is FELT, and it tests NO efficacy.  Per VP-SPEC + handover sec 8:
  (i)   the perturbation is monotone + interpretable and uses the clinical DIRECTION
        only (sign), never magnitude fitting;
  (ii)  ANTI-TUNING: shaking the perturbation grid / seed must preserve the
        QUALITATIVE direction (the sign of each normal<->disease contrast);
  (iii) the NORMAL <-> DISEASE contrast is the core readout;
  (iv)  the engine tree stays invariant + the result is 2x-deterministic, frozen;
  (v)   the honesty ledger 4 flags stay invariant
        (medium_efficacy_tested=0, hard_problem_open=1, consciousness_claim=0,
         new_tuned_constants=0).

--------------------------------------------------------------------------------
D1  CHRONIC STRESS / HPA HYPERACTIVITY        (reused modules: M17, M18)
--------------------------------------------------------------------------------
Perturbation (clinical direction, [F] magnitude swept / [L] anchored direction):
    HPA gain UP + negative-feedback DOWN  ==>  basal cortisol UP, recovery DELAYED;
    tonic LC-NE arousal gain UP           ==>  the M17 operating point shifts onto
                                               the over-aroused limb (Aston-Jones &
                                               Cohen 2005 high-tonic mode degrades
                                               task performance).
Pre-registered reproduction targets (the contrasts, fixed BEFORE measuring):
    H1  disease basal cortisol  >  normal basal           (tonic hypercortisolism)
    H2  disease recovery-time   >  normal recovery-time   (impaired GR feedback)
    H3  disease cortisol AUC    >  normal AUC             (prolonged exposure / load)
    H4  disease M17 selectivity <  normal M17 selectivity (stress narrows attention)
Faithfulness cross-checks (the decision-check's NORMAL arm == the engine):
    * the local HPA 2-lag NORMAL peak reproduces the engine M18 cortisol peak
      (24.06 min) inside the cited [15,40] window (Dickerson & Kemeny 2004);
    * evaluating the local M17 readout on the engine's gain grid reproduces the
      engine M17 inverted-U curve bit-for-bit (the curve SHAPE is unchanged --
      only the OPERATING POINT moves).
"""

import sys, os, json, hashlib
import numpy as np

HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
sys.path.insert(0, ENGINE)
import vp_mind_engine as E  # frozen engine, imported READ-ONLY

# the two frozen invariants this decision-check must NOT disturb
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

# --------------------------------------------------------------------------- #
# HPA cortisol 2-lag -- VERBATIM the engine M18 biexponential structure        #
#  (mirror of _m18_hpa_cascade); kept local so the DISEASE arm can perturb the #
#  CITED kinetics without touching the engine. tau_rise / tau_fall / pulse are #
#  the engine's [F] modelling timescales; basal & feedback are the perturbable #
#  clinical handles. The NORMAL arm reproduces the engine cortisol peak.        #
# --------------------------------------------------------------------------- #
_TAU_RISE = 12.0   # cortisol production/onset lag (min) -- engine M18 [F]
_TAU_FALL = 50.0   # elimination / recovery lag (min)    -- engine M18 [F]
_PULSE    = 3.0    # acute stressor duration (min)        -- engine M18 [F]
_T_HPA    = 240.0  # integration horizon (min)
_DT_HPA   = 0.02

def _hpa_trajectory(basal=0.0, recovery_factor=1.0, drive=1.0):
    """Biexponential 2-lag cortisol response (engine M18 mechanism). A brief stress
    pulse feeds a production lag x1 -> cortisol x2. The DISEASE handles are:
      basal>0           : tonic hypercortisolism (HPA gain up / chronic drive),
      recovery_factor>1 : impaired glucocorticoid negative feedback -> the falling
                          (recovery) limb is slowed (tau_fall *= recovery_factor).
    NORMAL = basal 0, recovery_factor 1 -> reproduces the engine cortisol peak."""
    tau_fall = _TAU_FALL * recovery_factor
    n = int(_T_HPA / _DT_HPA)
    x1 = np.zeros(n); x2 = np.zeros(n)
    for i in range(1, n):
        t = i * _DT_HPA
        u = drive if t < _PULSE else 0.0
        x1[i] = x1[i-1] + _DT_HPA * ((u - x1[i-1]) / _TAU_RISE)
        x2[i] = x2[i-1] + _DT_HPA * ((x1[i-1] - x2[i-1]) / tau_fall)
    t_ax = np.arange(n) * _DT_HPA
    return t_ax, x2 + basal

def _hpa_metrics(basal=0.0, recovery_factor=1.0):
    """basal, peak time/value, recovery-time (post-peak 1/e decay -- the natural
    time-constant of the falling limb, fixed as the recovery criterion BEFORE the
    disease arm), and AUC (total exposure). All reported AS-IS."""
    t, x = _hpa_trajectory(basal=basal, recovery_factor=recovery_factor)
    pk = int(np.argmax(x)); pkt = float(t[pk]); pkv = float(x[pk])
    # recovery: post-peak time for cortisol to fall to 1/e of (peak above basal)
    target = basal + (pkv - basal) / np.e
    post = np.where((t > pkt) & (x <= target))[0]
    rec_post_peak = float(t[post[0]] - pkt) if len(post) else float("nan")
    auc = float(np.trapezoid(x, t)) if hasattr(np, "trapezoid") else float(np.trapz(x, t))
    return dict(basal=round(basal, 6),
                peak_time_min=round(pkt, 6),
                peak_value=round(pkv, 8),
                recovery_post_peak_min=round(rec_post_peak, 6),
                auc=round(auc, 6))

# --------------------------------------------------------------------------- #
# M17 inverted-U -- mirror of emerge_global_state's distractor field VERBATIM. #
#  The curve SHAPE is the engine's; the DISEASE arm only moves the OPERATING    #
#  POINT (the tonic arousal gain) rightward onto the over-aroused limb.         #
# --------------------------------------------------------------------------- #
_G_SIG  = 1.5
_SIG    = 0.80
_G_DIST = np.linspace(1.0, 1.3, 8)     # 8 distractors -- VERBATIM M17
_L_DIST = np.linspace(0.18, 0.30, 8)   # spread levels  -- VERBATIM M17
_M17_ALPHAS = [round(float(a), 6) for a in np.linspace(0.1, 3.0, 30)]  # VERBATIM M17 arousal sweep grid

def _m17_perf_at(alpha, g_dist=_G_DIST, l_dist=_L_DIST):
    """The engine's M17 cognitive readout at arousal gain alpha (calls the frozen
    engine fold logic directly -- this IS the engine's inverted-U, point for point)."""
    return E._m17_cognitive_perf(alpha, _G_SIG, _SIG, g_dist, l_dist)


def disease_stress_results():
    E.seed_everything()
    NE  = E._load_neuroendocrine()["neuromodulators"]
    cort = NE["cortisol_HPA"]
    ne   = NE["norepinephrine_LC"]
    peak_lo, peak_hi = cort["acth_to_cortisol_peak_min"]["range"]        # [15,40] [L]
    rec_lo,  rec_hi  = cort["cortisol_recovery_min"]["range"]            # [60,90] [L]
    tonic_lo, tonic_hi = ne["tonic_firing_hz"]["range"]                  # [1,3]   [L]

    # ===== faithfulness: NORMAL arm reproduces the engine ====================
    eng_hpa  = E._m18_hpa_cascade(NE)
    eng_peak = eng_hpa["cortisol_peak_min"]
    normal   = _hpa_metrics(basal=0.0, recovery_factor=1.0)
    hpa_peak_reproduces_engine = bool(abs(normal["peak_time_min"] - eng_peak) < 0.05)
    normal_recovery_in_cited   = bool(rec_lo <= normal["recovery_post_peak_min"] <= rec_hi)

    eng_gs   = E.emerge_global_state()
    eng_curve   = eng_gs["cognitive_selectivity"]
    eng_alphas  = eng_gs["arousal_gains"]
    eng_peak_gain = eng_gs["selectivity_peak_gain"]
    # the local M17 readout must reproduce the engine inverted-U on its own grid
    local_curve = [round(_m17_perf_at(a), 8) for a in eng_alphas]
    m17_curve_reproduces_engine = bool(local_curve == [round(v, 8) for v in eng_curve])

    # ===== D1 perturbation -- a single nominal clinical-direction setting =====
    # magnitudes are NOMINAL/illustrative ([F], swept below); only the SIGN is the
    # clinical anchor [L]. NONE of these is fitted to hit a target value.
    D1_BASAL     = 0.010   # tonic hypercortisolism offset (HPA gain up)      [F>0]
    D1_RECOVERY  = 1.6     # recovery-limb prolongation (neg-feedback down)   [F>1]
    D1_GAIN_SHIFT = 0.20   # operating-point shift onto over-aroused limb     [F>0]

    disease = _hpa_metrics(basal=D1_BASAL, recovery_factor=D1_RECOVERY)

    # H1-H3: the HPA contrasts (sign-only)
    H1_basal_up    = bool(disease["basal"]                 > normal["basal"])
    H2_recovery_up = bool(disease["recovery_post_peak_min"] > normal["recovery_post_peak_min"])
    H3_auc_up      = bool(disease["auc"]                    > normal["auc"])
    disease_recovery_exceeds_cited = bool(disease["recovery_post_peak_min"] > rec_hi)

    # H4: M17 operating-point shift -- normal sits AT the Yerkes-Dodson optimum,
    # disease sits Δ past it (elevated tonic NE) -> the over-aroused limb collapses.
    op_normal  = float(eng_peak_gain)
    op_disease = float(eng_peak_gain + D1_GAIN_SHIFT)
    sel_normal  = round(_m17_perf_at(op_normal), 8)
    sel_disease = round(_m17_perf_at(op_disease), 8)
    H4_selectivity_down = bool(sel_disease < sel_normal)
    curve_shape_unchanged = m17_curve_reproduces_engine   # only the operating point moved

    # ===== ANTI-TUNING -- shake the grids, the SIGNS must hold ================
    # (a) HPA: sweep basal offset x recovery factor; H1/H2/H3 sign must hold for all
    basal_grid = [0.004, 0.008, 0.012, 0.020]
    recf_grid  = [1.2, 1.4, 1.8, 2.2]
    hpa_sign_hold = True
    for b in basal_grid:
        for rf in recf_grid:
            d = _hpa_metrics(basal=b, recovery_factor=rf)
            if not (d["basal"] > normal["basal"]
                    and d["recovery_post_peak_min"] > normal["recovery_post_peak_min"]
                    and d["auc"] > normal["auc"]):
                hpa_sign_hold = False
    # (b) M17: sweep the operating-point shift AND a perturbed distractor grid
    #     (the same anti-tuning grid M17 itself uses); H4 sign must hold for all
    g_dist2 = np.linspace(1.0, 1.35, 8); l_dist2 = np.linspace(0.17, 0.31, 8)
    shift_grid = [0.10, 0.15, 0.20, 0.30]
    m17_sign_hold = True
    for grid in ((_G_DIST, _L_DIST), (g_dist2, l_dist2)):
        sel_n = _m17_perf_at(op_normal, grid[0], grid[1])
        for ds in shift_grid:
            sel_d = _m17_perf_at(op_normal + ds, grid[0], grid[1])
            if not (sel_d < sel_n):
                m17_sign_hold = False

    # ===== engine-tree invariance (this decision-check changed NOTHING) ======
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items()
                          if int(k.split("_")[0][1:]) <= 16})
    engine_tree_unchanged = bool(tree_live == ENGINE_TREE_FROZEN)
    m0_16_unchanged       = bool(sub016 == M0_16_FROZEN)

    atlas_sha = hashlib.sha256(
        open(os.path.join(ENGINE, "data", "neuroendocrine_atlas.json"), "rb").read()
    ).hexdigest()

    return {
        "_meta": {
            "test": "D1_chronic_stress_HPA_hyperactivity",
            "reused_modules": ["M17_global_state", "M18_interoceptive_axis"],
            "seed": E.SEED,
            "neuroendocrine_atlas_sha256": atlas_sha,
            "perturbation_grade": "[F] magnitude swept (direction only) + [L] cited anchors",
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
        },
        "cited_anchors": {
            "cortisol_peak_window_min": [float(peak_lo), float(peak_hi)],   # Dickerson&Kemeny 2004 [L]
            "cortisol_recovery_window_min": [float(rec_lo), float(rec_hi)], # Dickerson&Kemeny 2004 [L]
            "ne_tonic_firing_window_hz": [float(tonic_lo), float(tonic_hi)],# Aston-Jones&Cohen 2005 [L]
        },
        "faithfulness": {
            "engine_M18_cortisol_peak_min": eng_peak,
            "normal_hpa_peak_min": normal["peak_time_min"],
            "hpa_normal_peak_reproduces_engine": hpa_peak_reproduces_engine,
            "normal_recovery_post_peak_min": normal["recovery_post_peak_min"],
            "normal_recovery_in_cited_window": normal_recovery_in_cited,
            "engine_M17_peak_gain": eng_peak_gain,
            "m17_curve_reproduces_engine": m17_curve_reproduces_engine,
        },
        "perturbation_nominal": {
            "basal_offset": D1_BASAL,
            "recovery_factor": D1_RECOVERY,
            "operating_gain_shift": D1_GAIN_SHIFT,
        },
        "normal_vs_disease": {
            "hpa_normal": normal,
            "hpa_disease": disease,
            "m17_operating_point_normal": op_normal,
            "m17_operating_point_disease": op_disease,
            "m17_selectivity_normal": sel_normal,
            "m17_selectivity_disease": sel_disease,
        },
        "preregistered_contrasts": {
            "H1_basal_cortisol_up": 1.0 if H1_basal_up else 0.0,
            "H2_recovery_delayed": 1.0 if H2_recovery_up else 0.0,
            "H3_auc_exposure_up": 1.0 if H3_auc_up else 0.0,
            "H4_attention_narrows_selectivity_down": 1.0 if H4_selectivity_down else 0.0,
            "disease_recovery_exceeds_cited_window": 1.0 if disease_recovery_exceeds_cited else 0.0,
            "m17_curve_shape_unchanged_only_operating_point_moved": 1.0 if curve_shape_unchanged else 0.0,
        },
        "anti_tuning": {
            "hpa_basal_grid": basal_grid,
            "hpa_recovery_grid": recf_grid,
            "hpa_all_signs_hold": 1.0 if hpa_sign_hold else 0.0,
            "m17_shift_grid": shift_grid,
            "m17_all_signs_hold": 1.0 if m17_sign_hold else 0.0,
        },
        "invariants": {
            "engine_tree_unchanged": 1.0 if engine_tree_unchanged else 0.0,
            "m0_16_subtree_unchanged": 1.0 if m0_16_unchanged else 0.0,
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,   # a mechanism-direction test, NOT an efficacy claim
            "hard_problem_open": 1.0,         # the disease state is NOT claimed to be felt
            "consciousness_claim": 0.0,
            "new_tuned_constants": 0.0,        # perturbation magnitudes are swept, sign-only (not fitted)
        },
    }


# =================================================================================
# D3  ANXIETY / PANIC                            (reused modules: M18, M20)
# =================================================================================
# Perturbation (clinical DIRECTION only; [F] magnitude swept / [L] HEP anchor):
#     M20 avoidance: an anticipatory DEFENSIVE BIAS (resting avoid drive UP) + a
#         THREAT GAIN (stress->avoid amplification UP)  ==>  the avoidance decision
#         transitions at a LOWER stress level (lowered avoidance threshold). The
#         panic signature is avoidance emerging at a stress that is SUB-THRESHOLD
#         for the normal substrate -- NOT merely "more avoidance at high stress".
#     M18 HEP: an INTEROCEPTIVE GAIN on the heartbeat-evoked-potential vs arousal
#         slope UP (cardiac hypervigilance; the cited HEP-tracks-arousal direction
#         [L] amplified)  ==>  HEP-arousal coupling becomes hypersensitive.
# Pre-registered reproduction targets (the contrasts, fixed BEFORE measuring):
#     H1  there is a NON-EMPTY stress band in which the NORMAL substrate selects
#         approach but the DISEASE substrate selects avoid (avoidance at a stress
#         that does not warrant it); demonstrated at the band midpoint.
#     H2  the avoidance onset (smallest stress selecting avoid) is LOWER in disease.
#     H3  the HEP-vs-arousal slope is STEEPER in disease (interoceptive hyperreactivity).
# Separation from D2 (orthogonality): D3 perturbs ONLY M18+M20; the reward/approach
#     machinery (M5) is byte-identical -> anxiety is NOT anhedonia (disjoint handles).
# Faithfulness (the NORMAL arm == the frozen engine):
#     the local M20 selected_action reproduces the engine's two action points
#     (approach@low, avoid@high) and the local HEP slope reproduces the engine M18.
# --------------------------------------------------------------------------------
# M20 avoidance mirror -- VERBATIM emerge_affective_access's selected_action.
#   approach_value/avoid_value/THRESH are the engine's [F] drives; the DISEASE
#   handles are defensive_bias (resting avoid drive, [F]>=0) and threat_mult
#   (stress->avoid gain, [F]>=1). NORMAL = (0, 1) -> reproduces the engine actions.
_M20_APP, _M20_AVO, _M20_THRESH = 0.70, 0.45, 0.60

def _m20_action(stress_gain, defensive_bias=0.0, threat_mult=1.0):
    d_app = _M20_APP
    d_avo = (_M20_AVO + defensive_bias) + 0.5 * threat_mult * stress_gain
    if max(d_app, d_avo) < _M20_THRESH:
        return "none"
    return "avoid" if d_avo > d_app else "approach"

def _m20_avoid_onset(defensive_bias=0.0, threat_mult=1.0):
    """Smallest stress at which avoid is selected (closed form of _m20_action's
    avoid<->approach boundary): (AVO+bias)+0.5*tm*s = APP."""
    s = (_M20_APP - (_M20_AVO + defensive_bias)) / (0.5 * threat_mult)
    return float(max(s, 0.0))

def _m18_hep_slope(intero_mult, aff_frac):
    """HEP-vs-arousal slope -- VERBATIM the engine hep_amp(g)=aff_gain*g, with the
    DISEASE interoceptive gain (intero_mult>1) scaling the afferent gain. NORMAL
    (intero_mult=1) reproduces the engine M18 slope (Pollatos & Schandry [L])."""
    lo = aff_frac * intero_mult * 0.6
    hi = aff_frac * intero_mult * 1.5
    return (hi - lo) / (1.5 - 0.6)


def disease_D3_results():
    E.seed_everything()
    INT = E._load_interoception()
    aff_frac = INT["vagus_cn_x"]["afferent_fraction"]["value"]            # ~0.80 [L]
    aff_lo, aff_hi = INT["vagus_cn_x"]["afferent_fraction"]["range"]      # [0.75,0.90] [L]
    hep_lo_ms, hep_hi_ms = INT["heartbeat_evoked_potential"]["hep_latency_window_ms"]["value"]
    hr_hz = INT["cardiac_rhythm"]["resting_hr_hz"]["value"]               # 1.17 Hz [L]

    # ===== faithfulness: NORMAL arm reproduces the engine =====================
    m20 = E.emerge_affective_access()
    a_low_eng, a_high_eng = m20["action_low_stress"], m20["action_high_stress"]
    a_low_loc, a_high_loc = _m20_action(0.0), _m20_action(1.0)
    m20_reproduces_engine = bool(a_low_loc == a_low_eng and a_high_loc == a_high_eng)

    m18aff = E._m18_afferent_dominance(INT, arousal_gain=1.0)
    eng_hep_slope = (m18aff["hep_amp_high_arousal"] - m18aff["hep_amp_low_arousal"]) / (1.5 - 0.6)
    normal_hep_slope = _m18_hep_slope(1.0, aff_frac)
    hep_slope_reproduces_engine = bool(abs(normal_hep_slope - eng_hep_slope) < 1e-12)

    # ===== D3 perturbation -- nominal clinical-direction setting ([F], swept) ==
    D3_DEFENSIVE_BIAS = 0.10   # anticipatory resting avoid drive UP            [F>=0]
    D3_THREAT_MULT    = 1.6    # stress->avoid threat gain UP                   [F>=1]
    D3_INTERO_MULT    = 1.5    # HEP-vs-arousal interoceptive gain UP           [F>=1]

    onset_normal  = _m20_avoid_onset(0.0, 1.0)                       # = 0.50 (engine)
    onset_disease = _m20_avoid_onset(D3_DEFENSIVE_BIAS, D3_THREAT_MULT)
    H2_avoid_threshold_lowered = bool(onset_disease < onset_normal)

    # H1: a non-empty [disease_onset, normal_onset) band where normal=approach,
    #     disease=avoid -- demonstrated at the band midpoint (always interior when H2)
    s_demo = 0.5 * (onset_disease + onset_normal)
    norm_at_demo = _m20_action(s_demo, 0.0, 1.0)
    dis_at_demo  = _m20_action(s_demo, D3_DEFENSIVE_BIAS, D3_THREAT_MULT)
    H1_avoid_at_subthreshold = bool(norm_at_demo == "approach" and dis_at_demo == "avoid")

    # H3: HEP-arousal coupling steeper under disease
    disease_hep_slope = _m18_hep_slope(D3_INTERO_MULT, aff_frac)
    H3_hep_coupling_steeper = bool(disease_hep_slope > normal_hep_slope)

    # ===== orthogonality vs D2 -- D3 leaves the reward machinery untouched =====
    eng_m5 = E.emerge_learned_field()
    reward_p_target = eng_m5["p_target_learned"]
    d3_reward_unaffected = bool(eng_m5["learned_above_control"] is True)   # M5 not perturbed by D3

    # ===== ANTI-TUNING -- shake the grids, the SIGNS must hold ================
    bias_grid   = [0.05, 0.10, 0.15, 0.20]
    threat_grid = [1.3, 1.6, 2.0, 2.5]
    m20_sign_hold = True
    for db in bias_grid:
        for tm in threat_grid:
            od = _m20_avoid_onset(db, tm); sd = 0.5 * (od + onset_normal)
            if not (od < onset_normal
                    and _m20_action(sd, 0.0, 1.0) == "approach"
                    and _m20_action(sd, db, tm) == "avoid"):
                m20_sign_hold = False
    intero_grid = [1.2, 1.5, 2.0, 3.0]
    m18_sign_hold = all(_m18_hep_slope(im, aff_frac) > normal_hep_slope for im in intero_grid)

    # ===== engine-tree invariance (this decision-check changed NOTHING) =======
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    engine_tree_unchanged = bool(tree_live == ENGINE_TREE_FROZEN)
    m0_16_unchanged       = bool(sub016 == M0_16_FROZEN)

    intero_sha = hashlib.sha256(
        open(os.path.join(ENGINE, "data", "interoception_atlas.json"), "rb").read()
    ).hexdigest()

    return {
        "_meta": {
            "test": "D3_anxiety_panic",
            "reused_modules": ["M18_interoceptive_axis", "M20_affective_access"],
            "seed": E.SEED,
            "interoception_atlas_sha256": intero_sha,
            "perturbation_grade": "[F] magnitude swept (direction only) + [L] HEP anchor",
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
        },
        "cited_anchors": {
            "vagus_afferent_fraction": [float(aff_lo), float(aff_hi)],   # ~0.80 input-dominant [L]
            "hep_latency_window_ms": [float(hep_lo_ms), float(hep_hi_ms)],  # 200-600 ms [L]
            "resting_hr_hz": float(hr_hz),                              # 1.17 Hz [L]
            "hep_amplitude_tracks_arousal": True,                       # Pollatos&Schandry [L] (perturbed direction)
        },
        "faithfulness": {
            "engine_action_low_stress": a_low_eng,
            "engine_action_high_stress": a_high_eng,
            "m20_normal_actions_reproduce_engine": m20_reproduces_engine,
            "engine_hep_slope": round(float(eng_hep_slope), 8),
            "normal_hep_slope": round(float(normal_hep_slope), 8),
            "m18_hep_slope_reproduces_engine": hep_slope_reproduces_engine,
        },
        "perturbation_nominal": {
            "defensive_bias": D3_DEFENSIVE_BIAS,
            "threat_mult": D3_THREAT_MULT,
            "intero_mult": D3_INTERO_MULT,
        },
        "normal_vs_disease": {
            "avoid_onset_normal": round(float(onset_normal), 6),
            "avoid_onset_disease": round(float(onset_disease), 6),
            "subthreshold_demo_stress": round(float(s_demo), 6),
            "action_normal_at_demo": norm_at_demo,
            "action_disease_at_demo": dis_at_demo,
            "hep_slope_normal": round(float(normal_hep_slope), 8),
            "hep_slope_disease": round(float(disease_hep_slope), 8),
        },
        "preregistered_contrasts": {
            "H1_avoidance_at_subthreshold_stress": 1.0 if H1_avoid_at_subthreshold else 0.0,
            "H2_avoidance_threshold_lowered": 1.0 if H2_avoid_threshold_lowered else 0.0,
            "H3_hep_arousal_coupling_steeper": 1.0 if H3_hep_coupling_steeper else 0.0,
            "D3_orthogonal_reward_machinery_untouched": 1.0 if d3_reward_unaffected else 0.0,
        },
        "anti_tuning": {
            "defensive_bias_grid": bias_grid,
            "threat_mult_grid": threat_grid,
            "m20_all_signs_hold": 1.0 if m20_sign_hold else 0.0,
            "intero_mult_grid": intero_grid,
            "m18_all_signs_hold": 1.0 if m18_sign_hold else 0.0,
        },
        "invariants": {
            "engine_tree_unchanged": 1.0 if engine_tree_unchanged else 0.0,
            "m0_16_subtree_unchanged": 1.0 if m0_16_unchanged else 0.0,
            "reward_p_target_learned_untouched": round(float(reward_p_target), 8),
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "hard_problem_open": 1.0,            # avoidance is functional; felt fear stays OPEN
            "consciousness_claim": 0.0,
            "new_tuned_constants": 0.0,
        },
    }


# =================================================================================
# D2  DEPRESSION / ANHEDONIA                     (reused modules: M5, M17, M19)
# =================================================================================
# Perturbation (clinical DIRECTION only; [F] magnitude swept):
#     M5 reward: a REWARD SENSITIVITY scaling on the dopamine RPE magnitude DOWN
#         (blunted reward-prediction-error; Pizzagalli reduced reward sensitivity)
#         ==>  weaker target potentiation (anhedonia) + weakened approach (valence+).
#     M19 mood-congruent recall: the prevailing MOOD turned NEGATIVE
#         ==>  pattern-completion is biased toward affect-congruent (negative)
#         engrams (Bower 1981 mood-congruent recall, in the depressive direction).
# Pre-registered reproduction targets (the contrasts, fixed BEFORE measuring):
#     H1  the learned target potentiation p_target is LOWER in disease (blunted RPE).
#     H2  the approach gap (p_target - chance) SHRINKS in disease (valence+ weakened).
#     H3  the NEGATIVITY of recall (neg_recall - pos_recall under the prevailing
#         mood) FLIPS from < 0 (euthymic: positive memories dominate) to > 0
#         (depressed: negative memories dominate).
# Separation from D3 (orthogonality): D2 perturbs ONLY M5+M19; the avoidance/HEP
#     machinery (M18+M20) is byte-identical -> anhedonia is NOT anxiety.
# Faithfulness (the NORMAL arm == the frozen engine):
#     the local RPE NORMAL arm (full reward sensitivity) reproduces the engine M5
#     p_target_learned bit-for-bit; the local mood-recall mirror at the engine
#     regime reproduces the engine M19 pos-under-pos-mood bit-for-bit.
# --------------------------------------------------------------------------------
# M5 RPE mirror -- VERBATIM emerge_learned_field's loop; the DISEASE handle is a
#   reward-sensitivity multiplier on the reward magnitude ([F] in (0,1]). NORMAL
#   (reward_sens=1.0) reproduces the engine p_target_learned exactly.
def _m5_rpe_learn(reward_sens=1.0, trials=80, lr=0.10):
    n = 5
    p = np.full(n, 1.0 / n)
    target = 2
    rng = np.random.RandomState(E.SEED + 7)
    V = 0.0
    for _ in range(trials):
        choice = int(rng.choice(n, p=p / p.sum()))
        reward = reward_sens * (1.0 if choice == target else 0.0)   # blunted under disease
        rpe = reward - V
        V += lr * rpe
        if choice == target:
            p[target] += lr * max(rpe, 0.0)
        p = np.clip(p, 1e-3, None); p = p / p.sum()
    return float(p[target])

# M19 mood-congruent recall mirror -- VERBATIM _m19_mood_congruent_recall's
#   construction + recall logic (same SEED+51), so the NORMAL arm at the engine
#   regime reproduces the engine. cue_frac is the [F] retrieval-difficulty knob
#   (the regime where the mood bias is decisive); only the contrast SIGN is claimed.
def _m19_four_recalls(cue_frac, bias):
    N = 120
    hp = E.Hippocampus(n_cells=N); hp.W = np.zeros((N, N)); hp.stored = []
    rng = np.random.RandomState(E.SEED + 51)
    pos = [np.where(rng.rand(N) < 0.5, 1.0, -1.0) for _ in range(4)]
    neg = [np.where(rng.rand(N) < 0.5, 1.0, -1.0) for _ in range(4)]
    pos_ids = [hp.write(p) for p in pos]; neg_ids = [hp.write(p) for p in neg]
    pos_axis = np.sign(np.mean(pos, axis=0)); neg_axis = np.sign(np.mean(neg, axis=0))
    def recall(ids, mood_axis):
        fids = []
        for j in ids:
            x = hp.stored[j]; ncue = max(1, int(round(cue_frac * N)))
            cue = rng.choice(N, size=ncue, replace=False)
            s = np.zeros(N); s[cue] = x[cue]; s = s.astype(float)
            for _ in range(40):
                h = hp.W @ s + bias * mood_axis
                sn = np.sign(h); sn[cue] = x[cue]
                if np.array_equal(sn, s): break
                s = sn
            fids.append(float(np.mean(s == x)))
        return float(np.mean(fids))
    pp = recall(pos_ids, pos_axis); npn = recall(neg_ids, pos_axis)
    pn = recall(pos_ids, neg_axis); nn = recall(neg_ids, neg_axis)
    return pp, npn, pn, nn

def _m19_engine_regime_pos_under_pos():
    """The mirror run at the engine's EXACT regime (30% cue, +mood bias 0.6, the
    first recall = pos-under-pos) -> reproduces the engine M19 value bit-for-bit."""
    N = 120
    hp = E.Hippocampus(n_cells=N); hp.W = np.zeros((N, N)); hp.stored = []
    rng = np.random.RandomState(E.SEED + 51)
    pos = [np.where(rng.rand(N) < 0.5, 1.0, -1.0) for _ in range(4)]
    neg = [np.where(rng.rand(N) < 0.5, 1.0, -1.0) for _ in range(4)]
    pos_ids = [hp.write(p) for p in pos]; [hp.write(p) for p in neg]
    pos_axis = np.sign(np.mean(pos, axis=0))
    fids = []
    for j in pos_ids:
        x = hp.stored[j]; ncue = max(1, int(round(0.3 * N)))
        cue = rng.choice(N, size=ncue, replace=False)
        s = np.zeros(N); s[cue] = x[cue]; s = s.astype(float)
        for _ in range(40):
            h = hp.W @ s + 0.6 * pos_axis
            sn = np.sign(h); sn[cue] = x[cue]
            if np.array_equal(sn, s): break
            s = sn
        fids.append(float(np.mean(s == x)))
    return float(np.mean(fids))


def disease_D2_results():
    E.seed_everything()

    # ===== faithfulness: NORMAL arms reproduce the engine =====================
    eng_m5 = E.emerge_learned_field()
    p_normal = _m5_rpe_learn(reward_sens=1.0)
    p_control = eng_m5["p_target_control"]                            # chance = 0.2
    m5_normal_reproduces_engine = bool(abs(p_normal - eng_m5["p_target_learned"]) < 1e-12)

    eng_m19 = E._m19_mood_congruent_recall()
    m19_normal = _m19_engine_regime_pos_under_pos()
    m19_normal_reproduces_engine = bool(abs(m19_normal - eng_m19["pos_recall_under_pos_mood"]) < 1e-12)
    engine_mood_congruent_helps  = bool(eng_m19["mood_congruent_helps"] == 1.0
                                        and eng_m19["recall_logic_verified"] == 1.0)

    # ===== D2 perturbation -- nominal clinical-direction setting ([F], swept) ==
    D2_REWARD_SENS = 0.40   # dopamine RPE reward sensitivity DOWN (anhedonia)   [F in (0,1)]
    D2_CUE_FRAC    = 0.10   # retrieval-difficulty regime where mood is decisive [F]
    D2_MOOD_BIAS   = 3.0    # mood-field strength                                [F>0]

    # H1/H2: blunted reward learning -> weakened approach
    p_disease = _m5_rpe_learn(reward_sens=D2_REWARD_SENS)
    gap_normal  = p_normal  - p_control
    gap_disease = p_disease - p_control
    H1_reward_blunted    = bool(p_disease < p_normal)
    H2_approach_weakened = bool(gap_disease < gap_normal)

    # H3: the negativity of recall flips euthymic(<0) -> depressed(>0)
    pp, npn, pn, nn = _m19_four_recalls(D2_CUE_FRAC, D2_MOOD_BIAS)
    negativity_normal  = npn - pp     # +mood: negative-minus-positive recall (euthymic, want < 0)
    negativity_disease = nn  - pn     # -mood: negative-minus-positive recall (depressed, want > 0)
    H3_recall_shifts_negative = bool(negativity_disease > negativity_normal
                                     and negativity_disease > 0.0
                                     and negativity_normal < 0.0)

    # ===== orthogonality vs D3 -- D2 leaves the avoidance/HEP machinery alone ==
    m20 = E.emerge_affective_access()
    d2_avoidance_unaffected = bool(m20["action_low_stress"] == "approach"
                                   and m20["action_high_stress"] == "avoid")

    # ===== ANTI-TUNING -- shake the grids, the SIGNS must hold ================
    sens_grid = [0.20, 0.40, 0.60, 0.80]
    m5_sign_hold  = all(_m5_rpe_learn(reward_sens=rs) < p_normal for rs in sens_grid)
    m5_gap_hold   = all((_m5_rpe_learn(reward_sens=rs) - p_control) < gap_normal for rs in sens_grid)
    cue_grid  = [0.10, 0.12]
    bias_grid = [2.0, 2.5, 3.0]
    m19_sign_hold = True
    for cf in cue_grid:
        for b in bias_grid:
            a, c, d, e = _m19_four_recalls(cf, b)
            nn_n = c - a; nn_d = e - d
            if not (nn_d > nn_n and nn_d > 0.0 and nn_n < 0.0):
                m19_sign_hold = False

    # ===== engine-tree invariance (this decision-check changed NOTHING) =======
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    engine_tree_unchanged = bool(tree_live == ENGINE_TREE_FROZEN)
    m0_16_unchanged       = bool(sub016 == M0_16_FROZEN)

    affect_sha = hashlib.sha256(
        open(os.path.join(ENGINE, "data", "affect_observables_atlas.json"), "rb").read()
    ).hexdigest()

    return {
        "_meta": {
            "test": "D2_depression_anhedonia",
            "reused_modules": ["M5_learned_field", "M17_global_state", "M19_affective_readouts"],
            "seed": E.SEED,
            "affect_observables_atlas_sha256": affect_sha,
            "perturbation_grade": "[F] magnitude swept (direction only)",
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
        },
        "cited_anchors": {
            "reward_prediction_error_dopamine": "M5 RPE learning (Schultz); blunted in anhedonia [direction]",
            "mood_congruent_memory": "Bower 1981 mood-congruent recall (negative-mood direction)",
            "reward_chance_p_target": float(p_control),
        },
        "faithfulness": {
            "engine_M5_p_target_learned": round(float(eng_m5["p_target_learned"]), 8),
            "normal_p_target_learned": round(float(p_normal), 8),
            "m5_normal_reproduces_engine": m5_normal_reproduces_engine,
            "engine_M19_pos_under_pos_mood": round(float(eng_m19["pos_recall_under_pos_mood"]), 8),
            "normal_m19_pos_under_pos_mood": round(float(m19_normal), 8),
            "m19_normal_reproduces_engine": m19_normal_reproduces_engine,
            "engine_mood_congruent_helps": engine_mood_congruent_helps,
        },
        "perturbation_nominal": {
            "reward_sensitivity": D2_REWARD_SENS,
            "recall_cue_fraction": D2_CUE_FRAC,
            "mood_bias_strength": D2_MOOD_BIAS,
        },
        "normal_vs_disease": {
            "p_target_normal": round(float(p_normal), 8),
            "p_target_disease": round(float(p_disease), 8),
            "approach_gap_normal": round(float(gap_normal), 8),
            "approach_gap_disease": round(float(gap_disease), 8),
            "recall_negativity_normal_euthymic": round(float(negativity_normal), 8),
            "recall_negativity_disease_depressed": round(float(negativity_disease), 8),
            "recall_pos_under_pos": round(float(pp), 8),
            "recall_neg_under_pos": round(float(npn), 8),
            "recall_pos_under_neg": round(float(pn), 8),
            "recall_neg_under_neg": round(float(nn), 8),
        },
        "preregistered_contrasts": {
            "H1_reward_learning_blunted": 1.0 if H1_reward_blunted else 0.0,
            "H2_approach_valence_weakened": 1.0 if H2_approach_weakened else 0.0,
            "H3_recall_shifts_negative": 1.0 if H3_recall_shifts_negative else 0.0,
            "D2_orthogonal_avoidance_machinery_untouched": 1.0 if d2_avoidance_unaffected else 0.0,
        },
        "anti_tuning": {
            "reward_sensitivity_grid": sens_grid,
            "m5_blunting_signs_hold": 1.0 if m5_sign_hold else 0.0,
            "m5_approach_gap_signs_hold": 1.0 if m5_gap_hold else 0.0,
            "recall_cue_grid": cue_grid,
            "recall_bias_grid": bias_grid,
            "m19_all_signs_hold": 1.0 if m19_sign_hold else 0.0,
        },
        "invariants": {
            "engine_tree_unchanged": 1.0 if engine_tree_unchanged else 0.0,
            "m0_16_subtree_unchanged": 1.0 if m0_16_unchanged else 0.0,
            "avoidance_machinery_untouched": 1.0 if d2_avoidance_unaffected else 0.0,
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "hard_problem_open": 1.0,            # blunted reward is functional; felt anhedonia OPEN
            "consciousness_claim": 0.0,
            "new_tuned_constants": 0.0,
        },
    }


# =================================================================================
# D4  PTSD / HYPERAROUSAL                         (reused modules: M17, M2, M18)
# =================================================================================
# Perturbation (clinical DIRECTION only; [F] magnitude swept / [L] NE-tonic anchor):
#     M17 tonic arousal: a raised tonic NE arousal FLOOR (Aston-Jones & Cohen high-tonic
#         mode) TRUNCATES the bottom of the Yerkes-Dodson operable window -> the usable
#         arousal band NARROWS (협착); the operating point is pinned past the optimum so
#         selectivity COLLAPSES on the over-aroused limb.
#     M2 extinction: a REDUCED extinction-LTD rate (Milad/Quirk fear-extinction deficit)
#         -> the fear engram is depotentiated more weakly -> a DEEPER residual fear basin
#         (a wider catchment for an intrusive cue = intrusion susceptibility UP).
#     M18 HEP: at the elevated operating arousal the HEP amplitude RIDES higher (cardiac
#         hyperarousal). The afferent GAIN is held at the engine value (intero_mult=1) --
#         D4 moves the operating point, NOT the afferent slope (that is D5's handle).
# Pre-registered reproduction targets (the contrasts, fixed BEFORE measuring):
#     H1  the operable arousal band (gains clearing half-peak above the tonic floor) is
#         NARROWER in disease than in normal (협착).
#     H2  selectivity at the elevated operating arousal is LOWER than at the optimum.
#     H3  the residual fear-engram basin depth after extinction is DEEPER in disease
#         (impaired extinction) than in normal (intact extinction).
#     H4  the HEP amplitude at the elevated operating arousal is HIGHER than at normal.
# Separation from D5 (orthogonality): D4 leaves the afferent interoceptive SLOPE (D5's
#     handle) byte-identical -> PTSD hyperarousal is NOT autonomic blunting (disjoint M18
#     sub-handles: operating-point shift vs afferent-gain reduction).
# Faithfulness (the NORMAL arm == the frozen engine):
#     the local M17 readout reproduces the engine inverted-U bit-for-bit; the fear engram
#     with NO extinction reproduces the engine M2 basin_depth_x_spinodal bit-for-bit.
# --------------------------------------------------------------------------------
# M17 operable-band mirror -- the count of engine arousal gains whose selectivity clears
#   half-peak AND sit at/above a tonic-arousal FLOOR. A raised floor (elevated tonic NE)
#   truncates the LOW end of the operable window. Uses the engine inverted-U point-for-point.
def _m17_operable_band(floor):
    curve = [_m17_perf_at(a) for a in _M17_ALPHAS]
    peak = max(curve)
    return int(sum(1 for a, p in zip(_M17_ALPHAS, curve) if p >= 0.5 * peak and a >= floor))

# M2 fear-engram extinction mirror -- the engine M2 pattern p0 written Hebbian into a fresh
#   Hippocampus (the NORMAL write == the engine). Extinction is LTD: each trial multiplicatively
#   DECAYS the trace toward zero (never inverts it -- an anti-Hebbian flip makes an oscillator,
#   not a weakened memory). The DISEASE handle is a REDUCED extinction-LTD rate. The readout is
#   basin_depth (the engine's R19-fold stability = how wide a catchment an intrusive cue falls
#   into). ext_lr=0 (no extinction) reproduces the engine basin_depth_x_spinodal bit-for-bit.
def _m2_fear_basin_after_extinction(ext_lr, trials=24):
    N = 120
    p0 = E._patterns(1, N, seed=E.SEED)[0]
    hp = E.Hippocampus(n_cells=N); hp.W = np.zeros((N, N)); hp.stored = []
    i0 = hp.write(p0)                                            # fear engram (Hebbian == engine)
    for _ in range(trials):                                      # extinction = LTD toward zero
        hp.W *= (1.0 - ext_lr); np.fill_diagonal(hp.W, 0.0)
    return float(hp.basin_depth(i0))

# M18 HEP amplitude -- VERBATIM the engine hep_amp(gain)=aff_gain*gain, with the afferent gain
#   scaled by intero_mult. At the elevated operating arousal of hyperarousal (intero_mult FIXED
#   at 1) the HEP amplitude RIDES higher; the afferent SLOPE is unchanged (NOT D5's handle).
def _m18_hep_amp(arousal, aff_frac, intero_mult=1.0):
    return float(aff_frac * intero_mult * arousal)

# M18 interoceptive affective-discriminability margin -- the HEP-amplitude SEPARATION between a
#   low-arousal and a high-arousal affective state (the bodily signal M19's affective readout
#   resolves) = hep_amp(1.5)-hep_amp(0.6). A blunted afferent gain (intero_mult<1) SHRINKS it.
def _m18_hep_margin(intero_mult, aff_frac):
    return _m18_hep_amp(1.5, aff_frac, intero_mult) - _m18_hep_amp(0.6, aff_frac, intero_mult)


def disease_D4_results():
    E.seed_everything()
    NE  = E._load_neuroendocrine()["neuromodulators"]
    ne  = NE["norepinephrine_LC"]
    tonic_lo, tonic_hi = ne["tonic_firing_hz"]["range"]                 # [1,3] Hz [L]
    INT = E._load_interoception()
    aff_frac = INT["vagus_cn_x"]["afferent_fraction"]["value"]          # ~0.80 [L]
    aff_lo, aff_hi = INT["vagus_cn_x"]["afferent_fraction"]["range"]    # [0.75,0.90] [L]

    # ===== faithfulness: NORMAL arms reproduce the engine =====================
    eng_gs = E.emerge_global_state()
    eng_peak_gain = eng_gs["selectivity_peak_gain"]
    eng_alphas    = eng_gs["arousal_gains"]
    local_curve   = [round(_m17_perf_at(a), 8) for a in eng_alphas]
    m17_curve_reproduces_engine = bool(local_curve == [round(v, 8) for v in eng_gs["cognitive_selectivity"]])

    eng_mem   = E.emerge_memory()
    eng_basin = eng_mem["basin_depth_x_spinodal"]
    normal_fear_basin_no_ext = _m2_fear_basin_after_extinction(0.0)     # no extinction == engine write
    m2_basin_reproduces_engine = bool(abs(normal_fear_basin_no_ext - eng_basin) < 1e-12)

    m18aff = E._m18_afferent_dominance(INT, arousal_gain=1.0)
    eng_hep_slope = (m18aff["hep_amp_high_arousal"] - m18aff["hep_amp_low_arousal"]) / (1.5 - 0.6)

    # ===== D4 perturbation -- nominal clinical-direction setting ([F], swept) ==
    D4_TONIC_FLOOR  = 1.20   # tonic NE arousal FLOOR raised (operable band truncated)  [F > band_lo]
    D4_OP_SHIFT     = 0.70   # operating point pushed past the optimum (over-aroused)    [F>0]
    D4_EXT_NORMAL   = 0.16   # intact extinction-LTD rate (NORMAL)                       [F]
    D4_EXT_DISEASE  = 0.04   # impaired extinction-LTD rate (PTSD)                        [F < normal]
    D4_AROUSAL_NORMAL  = float(eng_peak_gain)                  # normal operating arousal (optimum)
    D4_AROUSAL_DISEASE = float(eng_peak_gain + D4_OP_SHIFT)    # elevated operating arousal

    # H1: operable arousal band NARROWS (협착) -- raised tonic floor truncates the low end
    band_normal  = _m17_operable_band(0.1)                    # full operable window
    band_disease = _m17_operable_band(D4_TONIC_FLOOR)         # floor truncates the bottom
    H1_operable_band_narrows = bool(band_disease < band_normal)

    # H2: operating-point selectivity collapse on the over-aroused limb (Yerkes-Dodson)
    sel_normal  = round(_m17_perf_at(D4_AROUSAL_NORMAL), 8)
    sel_disease = round(_m17_perf_at(D4_AROUSAL_DISEASE), 8)
    H2_operating_point_selectivity_down = bool(sel_disease < sel_normal)

    # H3: impaired extinction -> a DEEPER residual fear basin (intrusion susceptibility up)
    basin_normal  = _m2_fear_basin_after_extinction(D4_EXT_NORMAL)
    basin_disease = _m2_fear_basin_after_extinction(D4_EXT_DISEASE)
    H3_intrusion_susceptibility_up = bool(basin_disease > basin_normal)

    # H4: HEP amplitude rides the elevated operating arousal (cardiac hyperarousal); the afferent
    #     GAIN is FIXED at the engine value (intero_mult=1) -> NOT D5's blunting handle.
    hep_amp_normal  = _m18_hep_amp(D4_AROUSAL_NORMAL,  aff_frac, intero_mult=1.0)
    hep_amp_disease = _m18_hep_amp(D4_AROUSAL_DISEASE, aff_frac, intero_mult=1.0)
    H4_hep_amp_rides_arousal = bool(hep_amp_disease > hep_amp_normal)

    # ===== orthogonality vs D5 -- D4 leaves the afferent interoceptive GAIN untouched =====
    #  D4 moves the arousal OPERATING POINT; D5 lowers the afferent SLOPE. Disjoint M18 sub-handles.
    d4_afferent_slope = _m18_hep_slope(1.0, aff_frac)                   # == engine slope (D5's handle)
    d4_orthogonal_afferent_gain_untouched = bool(abs(d4_afferent_slope - eng_hep_slope) < 1e-12)

    # ===== ANTI-TUNING -- shake the grids, the SIGNS must hold ================
    floor_grid = [1.0, 1.1, 1.2, 1.3]
    band_sign_hold = all(_m17_operable_band(b) < band_normal for b in floor_grid)
    band_monotone  = all(_m17_operable_band(floor_grid[i]) >= _m17_operable_band(floor_grid[i + 1])
                         for i in range(len(floor_grid) - 1))
    shift_grid = [0.3, 0.5, 0.7, 1.0]
    op_sign_hold = all(_m17_perf_at(eng_peak_gain + s) < sel_normal for s in shift_grid)
    ext_grid = [0.04, 0.08, 0.12, 0.16, 0.20]                 # impaired -> intact extinction-LTD rates
    b_dis = _m2_fear_basin_after_extinction(D4_EXT_DISEASE)
    ext_sign_hold = all(b_dis > _m2_fear_basin_after_extinction(r) for r in ext_grid if r > D4_EXT_DISEASE)
    ext_monotone  = all(_m2_fear_basin_after_extinction(ext_grid[i]) > _m2_fear_basin_after_extinction(ext_grid[i + 1])
                        for i in range(len(ext_grid) - 1))
    amp_grid = [0.3, 0.5, 0.7, 1.0]
    hep_sign_hold = all(_m18_hep_amp(eng_peak_gain + s, aff_frac, 1.0) > hep_amp_normal for s in amp_grid)

    # ===== engine-tree invariance (this decision-check changed NOTHING) =======
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    engine_tree_unchanged = bool(tree_live == ENGINE_TREE_FROZEN)
    m0_16_unchanged       = bool(sub016 == M0_16_FROZEN)

    neuro_sha = hashlib.sha256(
        open(os.path.join(ENGINE, "data", "neuroendocrine_atlas.json"), "rb").read()
    ).hexdigest()

    return {
        "_meta": {
            "test": "D4_ptsd_hyperarousal",
            "reused_modules": ["M17_global_state", "M2_memory", "M18_interoceptive_axis"],
            "seed": E.SEED,
            "neuroendocrine_atlas_sha256": neuro_sha,
            "perturbation_grade": "[F] magnitude swept (direction only) + [L] NE-tonic anchor",
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
        },
        "cited_anchors": {
            "ne_tonic_firing_window_hz": [float(tonic_lo), float(tonic_hi)],   # Aston-Jones&Cohen 2005 [L]
            "vagus_afferent_fraction": [float(aff_lo), float(aff_hi)],         # ~0.80 [L]
            "extinction_learning_blunted_in_ptsd": "Milad/Quirk fear-extinction deficit [direction]",
        },
        "faithfulness": {
            "engine_M17_peak_gain": eng_peak_gain,
            "m17_curve_reproduces_engine": m17_curve_reproduces_engine,
            "engine_M2_basin_depth_x_spinodal": round(float(eng_basin), 8),
            "normal_fear_basin_no_extinction": round(float(normal_fear_basin_no_ext), 8),
            "m2_basin_reproduces_engine": m2_basin_reproduces_engine,
            "engine_hep_slope": round(float(eng_hep_slope), 8),
        },
        "perturbation_nominal": {
            "tonic_arousal_floor": D4_TONIC_FLOOR,
            "operating_point_shift": D4_OP_SHIFT,
            "extinction_ltd_rate_normal": D4_EXT_NORMAL,
            "extinction_ltd_rate_disease": D4_EXT_DISEASE,
        },
        "normal_vs_disease": {
            "operable_band_normal": float(band_normal),
            "operable_band_disease": float(band_disease),
            "m17_operating_arousal_normal": round(D4_AROUSAL_NORMAL, 6),
            "m17_operating_arousal_disease": round(D4_AROUSAL_DISEASE, 6),
            "m17_selectivity_normal": sel_normal,
            "m17_selectivity_disease": sel_disease,
            "fear_basin_normal_extinction": round(float(basin_normal), 8),
            "fear_basin_disease_extinction": round(float(basin_disease), 8),
            "hep_amp_normal_arousal": round(float(hep_amp_normal), 8),
            "hep_amp_disease_arousal": round(float(hep_amp_disease), 8),
        },
        "preregistered_contrasts": {
            "H1_operable_arousal_band_narrows": 1.0 if H1_operable_band_narrows else 0.0,
            "H2_operating_point_selectivity_collapses": 1.0 if H2_operating_point_selectivity_down else 0.0,
            "H3_extinction_deficit_deepens_fear_basin": 1.0 if H3_intrusion_susceptibility_up else 0.0,
            "H4_hep_amplitude_rides_hyperarousal": 1.0 if H4_hep_amp_rides_arousal else 0.0,
            "D4_orthogonal_afferent_gain_untouched": 1.0 if d4_orthogonal_afferent_gain_untouched else 0.0,
        },
        "anti_tuning": {
            "tonic_floor_grid": floor_grid,
            "operable_band_all_signs_hold": 1.0 if band_sign_hold else 0.0,
            "operable_band_monotone": 1.0 if band_monotone else 0.0,
            "operating_shift_grid": shift_grid,
            "operating_point_all_signs_hold": 1.0 if op_sign_hold else 0.0,
            "extinction_rate_grid": ext_grid,
            "extinction_basin_all_signs_hold": 1.0 if ext_sign_hold else 0.0,
            "extinction_basin_monotone": 1.0 if ext_monotone else 0.0,
            "hep_amp_grid": amp_grid,
            "hep_amp_all_signs_hold": 1.0 if hep_sign_hold else 0.0,
        },
        "invariants": {
            "engine_tree_unchanged": 1.0 if engine_tree_unchanged else 0.0,
            "m0_16_subtree_unchanged": 1.0 if m0_16_unchanged else 0.0,
            "afferent_slope_untouched": round(float(d4_afferent_slope), 8),
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "hard_problem_open": 1.0,            # hyperarousal/intrusion functional; felt terror OPEN
            "consciousness_claim": 0.0,
            "new_tuned_constants": 0.0,
        },
    }


# =================================================================================
# D5  AUTONOMIC DYSFUNCTION / INTEROCEPTIVE BLUNTING   (reused modules: M18, M19)
# =================================================================================
# Perturbation (clinical DIRECTION only; [F] magnitude swept / [L] HEP anchor):
#     M18 afferent: the vagal afferent interoceptive gain DOWN (intero_mult<1; autonomic
#         dysfunction / reduced interoceptive accuracy) -> the HEP-vs-arousal slope FLATTENS
#         (the bodily arousal signal carries less information).
#     M19 affective readout: because the affective readout RESOLVES the interoceptive signal,
#         the blunted afferent gain SHRINKS the interoceptive affective-discriminability margin
#         (the HEP-amplitude separation between affective states) -> affective resolution DOWN.
# Pre-registered reproduction targets (the contrasts, fixed BEFORE measuring):
#     H1  the HEP-vs-arousal slope is FLATTER in disease than in normal.
#     H2  the interoceptive affective-discriminability margin is SMALLER in disease.
# Separation from D2 (orthogonality): D5 perturbs ONLY M18+M19; the reward machinery (M5) is
#     byte-identical -> autonomic blunting is NOT anhedonia. Separation from D4: D5 leaves the
#     M17 arousal operating point at the engine optimum (D4 shifts it). D5 and D3 are OPPOSITE
#     poles of the SAME interoceptive axis (D3 intero_mult>1 hypervigilant; D5 intero_mult<1 blunted).
# Faithfulness (the NORMAL arm == the frozen engine):
#     the local HEP slope at intero_mult=1 reproduces the engine M18 slope bit-for-bit; the local
#     M19 mood-congruent recall at the engine regime reproduces the engine pos-under-pos bit-for-bit.
# --------------------------------------------------------------------------------
def disease_D5_results():
    E.seed_everything()
    INT = E._load_interoception()
    aff_frac = INT["vagus_cn_x"]["afferent_fraction"]["value"]          # ~0.80 [L]
    aff_lo, aff_hi = INT["vagus_cn_x"]["afferent_fraction"]["range"]    # [0.75,0.90] [L]
    hr_hz = INT["cardiac_rhythm"]["resting_hr_hz"]["value"]             # 1.17 Hz [L]

    # ===== faithfulness: NORMAL arms reproduce the engine =====================
    m18aff = E._m18_afferent_dominance(INT, arousal_gain=1.0)
    eng_hep_slope = (m18aff["hep_amp_high_arousal"] - m18aff["hep_amp_low_arousal"]) / (1.5 - 0.6)
    normal_hep_slope = _m18_hep_slope(1.0, aff_frac)
    hep_slope_reproduces_engine = bool(abs(normal_hep_slope - eng_hep_slope) < 1e-12)

    eng_m19    = E._m19_mood_congruent_recall()
    m19_normal = _m19_engine_regime_pos_under_pos()
    m19_normal_reproduces_engine = bool(abs(m19_normal - eng_m19["pos_recall_under_pos_mood"]) < 1e-12)
    engine_mood_congruent_helps  = bool(eng_m19["mood_congruent_helps"] == 1.0
                                        and eng_m19["recall_logic_verified"] == 1.0)

    # ===== D5 perturbation -- nominal clinical-direction setting ([F], swept) ==
    D5_INTERO_MULT = 0.30   # vagal afferent interoceptive gain DOWN (blunting)   [F in (0,1)]

    normal_margin     = _m18_hep_margin(1.0, aff_frac)
    disease_margin    = _m18_hep_margin(D5_INTERO_MULT, aff_frac)
    disease_hep_slope = _m18_hep_slope(D5_INTERO_MULT, aff_frac)

    # H1: HEP-arousal slope FLATTENS (the bodily arousal signal carries less information)
    H1_hep_slope_flattens = bool(disease_hep_slope < normal_hep_slope)
    # H2: the interoceptive affective-discriminability margin SHRINKS (affective resolution down)
    H2_affective_resolution_down = bool(disease_margin < normal_margin)

    # ===== orthogonality vs D2 -- D5 leaves the reward machinery untouched =====
    eng_m5 = E.emerge_learned_field()
    reward_p_target = eng_m5["p_target_learned"]
    d5_orthogonal_reward_untouched = bool(eng_m5["learned_above_control"] is True)
    # ===== orthogonality vs D4 -- D5 leaves the arousal operating point at the engine optimum ====
    eng_gs = E.emerge_global_state()
    d5_arousal_operating_point_untouched = bool(
        round(_m17_perf_at(eng_gs["selectivity_peak_gain"]), 8) == round(max(eng_gs["cognitive_selectivity"]), 8))
    # D5 vs D3: OPPOSITE poles on the SAME interoceptive axis (D3 intero_mult>1 hypervigilant)
    d3_axis_pole_slope = _m18_hep_slope(1.5, aff_frac)                  # D3-direction (steepened), for contrast
    opposite_poles_same_axis = bool(disease_hep_slope < normal_hep_slope < d3_axis_pole_slope)

    # ===== ANTI-TUNING -- shake the grid, the SIGNS must hold ================
    intero_grid = [0.7, 0.5, 0.3, 0.15]                       # all blunted (<1)
    slope_sign_hold = all(_m18_hep_slope(im, aff_frac) < normal_hep_slope for im in intero_grid)
    slope_monotone  = all(_m18_hep_slope(intero_grid[i], aff_frac) > _m18_hep_slope(intero_grid[i + 1], aff_frac)
                          for i in range(len(intero_grid) - 1))
    margin_sign_hold = all(_m18_hep_margin(im, aff_frac) < normal_margin for im in intero_grid)
    margin_monotone  = all(_m18_hep_margin(intero_grid[i], aff_frac) > _m18_hep_margin(intero_grid[i + 1], aff_frac)
                           for i in range(len(intero_grid) - 1))

    # ===== engine-tree invariance (this decision-check changed NOTHING) =======
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    engine_tree_unchanged = bool(tree_live == ENGINE_TREE_FROZEN)
    m0_16_unchanged       = bool(sub016 == M0_16_FROZEN)

    intero_sha = hashlib.sha256(
        open(os.path.join(ENGINE, "data", "interoception_atlas.json"), "rb").read()
    ).hexdigest()

    return {
        "_meta": {
            "test": "D5_autonomic_dysfunction_interoceptive_blunting",
            "reused_modules": ["M18_interoceptive_axis", "M19_affective_readouts"],
            "seed": E.SEED,
            "interoception_atlas_sha256": intero_sha,
            "perturbation_grade": "[F] magnitude swept (direction only) + [L] HEP anchor",
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
        },
        "cited_anchors": {
            "vagus_afferent_fraction": [float(aff_lo), float(aff_hi)],   # ~0.80 input-dominant [L]
            "resting_hr_hz": float(hr_hz),                              # 1.17 Hz [L]
            "hep_amplitude_tracks_arousal": True,                       # Pollatos&Schandry [L] (blunted direction)
        },
        "faithfulness": {
            "engine_hep_slope": round(float(eng_hep_slope), 8),
            "normal_hep_slope": round(float(normal_hep_slope), 8),
            "m18_hep_slope_reproduces_engine": hep_slope_reproduces_engine,
            "engine_M19_pos_under_pos_mood": round(float(eng_m19["pos_recall_under_pos_mood"]), 8),
            "normal_m19_pos_under_pos_mood": round(float(m19_normal), 8),
            "m19_normal_reproduces_engine": m19_normal_reproduces_engine,
            "engine_mood_congruent_helps": engine_mood_congruent_helps,
        },
        "perturbation_nominal": {
            "interoceptive_afferent_gain": D5_INTERO_MULT,
        },
        "normal_vs_disease": {
            "hep_slope_normal": round(float(normal_hep_slope), 8),
            "hep_slope_disease": round(float(disease_hep_slope), 8),
            "affective_margin_normal": round(float(normal_margin), 8),
            "affective_margin_disease": round(float(disease_margin), 8),
        },
        "preregistered_contrasts": {
            "H1_hep_arousal_slope_flattens": 1.0 if H1_hep_slope_flattens else 0.0,
            "H2_affective_discriminability_margin_shrinks": 1.0 if H2_affective_resolution_down else 0.0,
            "D5_orthogonal_reward_machinery_untouched": 1.0 if d5_orthogonal_reward_untouched else 0.0,
            "D5_orthogonal_arousal_operating_point_untouched": 1.0 if d5_arousal_operating_point_untouched else 0.0,
            "D5_vs_D3_opposite_poles_same_interoceptive_axis": 1.0 if opposite_poles_same_axis else 0.0,
        },
        "anti_tuning": {
            "interoceptive_gain_grid": intero_grid,
            "hep_slope_all_signs_hold": 1.0 if slope_sign_hold else 0.0,
            "hep_slope_monotone": 1.0 if slope_monotone else 0.0,
            "affective_margin_all_signs_hold": 1.0 if margin_sign_hold else 0.0,
            "affective_margin_monotone": 1.0 if margin_monotone else 0.0,
        },
        "invariants": {
            "engine_tree_unchanged": 1.0 if engine_tree_unchanged else 0.0,
            "m0_16_subtree_unchanged": 1.0 if m0_16_unchanged else 0.0,
            "reward_p_target_learned_untouched": round(float(reward_p_target), 8),
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "hard_problem_open": 1.0,            # blunted afference functional; felt numbing OPEN
            "consciousness_claim": 0.0,
            "new_tuned_constants": 0.0,
        },
    }


# =================================================================================
# D6  BURNOUT / HPA HYPOACTIVITY (terminal stage)         (reused module: M18)
# =================================================================================
# Perturbation (clinical DIRECTION only; [F] magnitude swept / [L] cortisol anchors):
#     M18 HPA: after chronic overdrive the axis becomes HYPOactive -- the HPA gain/drive
#         goes DOWN (drive<1). This is the MIRROR of D1 (chronic stress / HPA hyperactivity)
#         on the SAME HPA axis. D1 raised basal + delayed recovery (cortisol OVERLOAD); D6
#         abolishes the acute cortisol PEAK and flattens the recovery curve (cortisol
#         DEPLETION / hypocortisolism). basal stays 0 (NOT D1's tonic hypercortisolism --
#         the OPPOSITE pole) and the falling-limb time-constant stays at the engine value:
#         the 2-lag is LINEAR, so scaling the drive scales the AMPLITUDE but not the
#         kinetics -> the flattening is a pure REACTIVITY loss, not a kinetic shift.
# Pre-registered reproduction targets (the contrasts, fixed BEFORE measuring):
#     H1  the acute cortisol PEAK is ABOLISHED -- disease peak value < normal peak value.
#     H2  total cortisol OUTPUT is DOWN (hypocortisolism) -- disease AUC < normal AUC.
#     H3  the recovery curve FLATTENS -- the descending-limb slope (cortisol fall per min
#         over the 1/e window) is GENTLER in disease than in normal.
# Invariant (the MIRROR of D1's "shape unchanged, only operating point moved"): the HPA
#     time-constants (peak time + 1/e recovery time) are UNCHANGED normal<->disease --
#     burnout flattening is amplitude loss, NOT a faster/slower curve. (H1/H3 co-vary as
#     drive scales -- collinear, disclosed -- the same allowance D5 took for HEP margin.)
# Orthogonality vs D1 (OPPOSITE poles, SAME HPA axis): the shared-axis pole is total
#     cortisol OUTPUT -- the D6 (gain DOWN) arm sits BELOW normal which sits BELOW the
#     D1-direction (gain UP) arm: AUC D6 < normal < D1 AND tonic basal D6 <= normal < D1
#     (chronic-stress OVERLOAD / hypercortisolism vs burnout DEPLETION / hypocortisolism --
#     the D5<->D3 opposite-pole pattern). Peak is NOT the pole metric: D1's prolonged
#     recovery slows the 2-lag accumulation and lowers the brief-pulse peak -- it is the
#     cortisol LOAD, not the peak height, that separates the two poles.
# Faithfulness (the NORMAL arm == the frozen engine): the NORMAL HPA peak (drive 1, basal 0)
#     reproduces the engine M18 cortisol peak (~24 min, cited [15,40]) bit-for-bit and the
#     NORMAL 1/e recovery lands in the cited [60,90] window (Dickerson & Kemeny 2004 [L]).
# --------------------------------------------------------------------------------
# HPA metrics WITH an explicit drive handle -- mirrors _hpa_metrics (D1's metric, kept
#   byte-identical) but threads the acute drive AND reports the descending-limb slope. The
#   2-lag itself is the engine M18 mechanism (_hpa_trajectory, reused verbatim).
def _hpa_metrics_drive(basal=0.0, recovery_factor=1.0, drive=1.0):
    t, x = _hpa_trajectory(basal=basal, recovery_factor=recovery_factor, drive=drive)
    pk = int(np.argmax(x)); pkt = float(t[pk]); pkv = float(x[pk])
    target = basal + (pkv - basal) / np.e
    post = np.where((t > pkt) & (x <= target))[0]
    rec_post_peak = float(t[post[0]] - pkt) if len(post) else float("nan")
    auc = float(np.trapezoid(x, t)) if hasattr(np, "trapezoid") else float(np.trapz(x, t))
    # recovery-limb slope = cortisol drop per minute over the 1/e recovery window
    rec_slope = ((pkv - target) / rec_post_peak) if (rec_post_peak == rec_post_peak and rec_post_peak) else float("nan")
    return dict(basal=round(basal, 6),
                peak_time_min=round(pkt, 6),
                peak_value=round(pkv, 8),
                recovery_post_peak_min=round(rec_post_peak, 6),
                recovery_slope=round(rec_slope, 10),
                auc=round(auc, 6))


def disease_D6_results():
    E.seed_everything()
    NE   = E._load_neuroendocrine()["neuromodulators"]
    cort = NE["cortisol_HPA"]
    peak_lo, peak_hi = cort["acth_to_cortisol_peak_min"]["range"]        # [15,40] [L]
    rec_lo,  rec_hi  = cort["cortisol_recovery_min"]["range"]            # [60,90] [L]

    # ===== faithfulness: NORMAL arm reproduces the engine ====================
    eng_hpa  = E._m18_hpa_cascade(NE)
    eng_peak = eng_hpa["cortisol_peak_min"]
    normal   = _hpa_metrics_drive(basal=0.0, recovery_factor=1.0, drive=1.0)
    hpa_peak_reproduces_engine = bool(abs(normal["peak_time_min"] - eng_peak) < 0.05)
    normal_recovery_in_cited   = bool(rec_lo <= normal["recovery_post_peak_min"] <= rec_hi)

    # ===== D6 perturbation -- a single nominal clinical-direction setting =====
    # magnitude is NOMINAL/illustrative ([F], swept below); only the SIGN (gain DOWN) is the
    # clinical anchor. NOTHING is fitted to hit a target value.
    D6_DRIVE_DISEASE = 0.30   # HPA gain/drive DOWN (blunted acute cortisol reactivity)  [F in (0,1)]

    disease = _hpa_metrics_drive(basal=0.0, recovery_factor=1.0, drive=D6_DRIVE_DISEASE)

    # H1: the acute cortisol PEAK is ABOLISHED (peak value down)
    H1_peak_abolished    = bool(disease["peak_value"]     < normal["peak_value"])
    # H2: total cortisol OUTPUT is DOWN (hypocortisolism)
    H2_output_down       = bool(disease["auc"]            < normal["auc"])
    # H3: the recovery curve FLATTENS (gentler descending-limb slope)
    H3_recovery_flattens = bool(disease["recovery_slope"] < normal["recovery_slope"])

    # the MIRROR of D1's "shape unchanged": the HPA time-constants are UNCHANGED --
    # the flattening is a pure amplitude/reactivity loss, NOT a kinetic shift.
    kinetics_unchanged = bool(disease["recovery_post_peak_min"] == normal["recovery_post_peak_min"]
                              and disease["peak_time_min"] == normal["peak_time_min"])

    # ===== orthogonality vs D1 -- OPPOSITE poles of the SAME HPA axis =========
    #  D1-direction (gain UP) = chronic-stress hyperactivity: basal up + recovery prolonged
    #  (the SAME nominal handles D1 uses; recomputed here purely to assert the opposite sign).
    #  The shared-axis pole is total cortisol OUTPUT: D1 = OVERLOAD (AUC up + tonic basal up
    #  = hypercortisolism); D6 = DEPLETION (AUC down + no tonic elevation = hypocortisolism).
    #  (Peak is NOT the pole metric -- D1's prolonged recovery_factor slows the 2-lag
    #  accumulation and actually lowers the brief-pulse peak; the cortisol LOAD is the pole.)
    d1_dir = _hpa_metrics_drive(basal=0.010, recovery_factor=1.6, drive=1.0)
    d6_vs_d1_opposite_pole = bool(disease["auc"] < normal["auc"] < d1_dir["auc"]
                                  and disease["basal"] <= normal["basal"] < d1_dir["basal"])

    # ===== ANTI-TUNING -- shake the drive grid -> the SIGNS must hold =========
    drive_grid = [0.8, 0.6, 0.4, 0.2]                        # all blunted (<1)
    peak_sign_hold  = all(_hpa_metrics_drive(drive=d)["peak_value"] < normal["peak_value"] for d in drive_grid)
    peak_monotone   = all(_hpa_metrics_drive(drive=drive_grid[i])["peak_value"]
                          > _hpa_metrics_drive(drive=drive_grid[i + 1])["peak_value"]
                          for i in range(len(drive_grid) - 1))
    auc_sign_hold   = all(_hpa_metrics_drive(drive=d)["auc"] < normal["auc"] for d in drive_grid)
    slope_sign_hold = all(_hpa_metrics_drive(drive=d)["recovery_slope"] < normal["recovery_slope"] for d in drive_grid)
    slope_monotone  = all(_hpa_metrics_drive(drive=drive_grid[i])["recovery_slope"]
                          > _hpa_metrics_drive(drive=drive_grid[i + 1])["recovery_slope"]
                          for i in range(len(drive_grid) - 1))

    # ===== engine-tree invariance (this decision-check changed NOTHING) ======
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    engine_tree_unchanged = bool(tree_live == ENGINE_TREE_FROZEN)
    m0_16_unchanged       = bool(sub016 == M0_16_FROZEN)

    neuro_sha = hashlib.sha256(
        open(os.path.join(ENGINE, "data", "neuroendocrine_atlas.json"), "rb").read()
    ).hexdigest()

    return {
        "_meta": {
            "test": "D6_burnout_HPA_hypoactivity",
            "reused_modules": ["M18_interoceptive_axis"],
            "seed": E.SEED,
            "neuroendocrine_atlas_sha256": neuro_sha,
            "perturbation_grade": "[F] magnitude swept (direction only) + [L] cortisol anchors",
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
        },
        "cited_anchors": {
            "cortisol_peak_window_min": [float(peak_lo), float(peak_hi)],     # Dickerson&Kemeny 2004 [L]
            "cortisol_recovery_window_min": [float(rec_lo), float(rec_hi)],   # Dickerson&Kemeny 2004 [L]
            "burnout_hpa_hypoactivity_blunted_cortisol":
                "terminal-stage HPA down-regulation / hypocortisolism [direction]",
        },
        "faithfulness": {
            "engine_M18_cortisol_peak_min": eng_peak,
            "normal_hpa_peak_min": normal["peak_time_min"],
            "hpa_normal_peak_reproduces_engine": hpa_peak_reproduces_engine,
            "normal_recovery_post_peak_min": normal["recovery_post_peak_min"],
            "normal_recovery_in_cited_window": normal_recovery_in_cited,
        },
        "perturbation_nominal": {
            "acute_drive_disease": D6_DRIVE_DISEASE,
        },
        "normal_vs_disease": {
            "hpa_normal": normal,
            "hpa_disease": disease,
            "hpa_d1_direction": d1_dir,
        },
        "preregistered_contrasts": {
            "H1_acute_cortisol_peak_abolished": 1.0 if H1_peak_abolished else 0.0,
            "H2_total_cortisol_output_down": 1.0 if H2_output_down else 0.0,
            "H3_recovery_curve_flattens": 1.0 if H3_recovery_flattens else 0.0,
            "hpa_kinetics_unchanged_only_amplitude_lost": 1.0 if kinetics_unchanged else 0.0,
            "D6_vs_D1_opposite_pole_same_hpa_axis": 1.0 if d6_vs_d1_opposite_pole else 0.0,
        },
        "anti_tuning": {
            "acute_drive_grid": drive_grid,
            "peak_all_signs_hold": 1.0 if peak_sign_hold else 0.0,
            "peak_monotone": 1.0 if peak_monotone else 0.0,
            "auc_all_signs_hold": 1.0 if auc_sign_hold else 0.0,
            "recovery_slope_all_signs_hold": 1.0 if slope_sign_hold else 0.0,
            "recovery_slope_monotone": 1.0 if slope_monotone else 0.0,
        },
        "invariants": {
            "engine_tree_unchanged": 1.0 if engine_tree_unchanged else 0.0,
            "m0_16_subtree_unchanged": 1.0 if m0_16_unchanged else 0.0,
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "hard_problem_open": 1.0,            # hypocortisolism/exhaustion functional; felt burnout OPEN
            "consciousness_claim": 0.0,
            "new_tuned_constants": 0.0,
        },
    }


def _canon(obj):
    return json.dumps(E._round(obj), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def _fmt(x):
    try: return f"{float(x):+.6f}"
    except Exception: return str(x)

def main():
    D = disease_stress_results()
    blob = _canon(D)
    digest = hashlib.sha256(blob).hexdigest()

    res_path = os.path.join(HERE, "disease_stress_results.json")
    with open(res_path, "wb") as f:
        f.write(blob)

    exp_path = os.path.join(HERE, "expected_disease_sha256.json")
    payload = {"disease_stress_results.json": digest,
               "neuroendocrine_atlas_sha256": D["_meta"]["neuroendocrine_atlas_sha256"],
               "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN}
    if os.path.exists(exp_path):
        prev = json.load(open(exp_path)).get("disease_stress_results.json")
        status = "MATCHES locked digest" if prev == digest else f"MISMATCH (locked={prev})"
    else:
        with open(exp_path, "w") as f:
            json.dump(payload, f, indent=2)
        status = "WROTE expected_disease_sha256.json (first freeze)"

    f = D["faithfulness"]
    c = D["preregistered_contrasts"]
    p = D["normal_vs_disease"]
    a, inv, h = D["anti_tuning"], D["invariants"], D["honesty_ledger"]
    nh, nd = p["hpa_normal"], p["hpa_disease"]

    print("=" * 78)
    print("DISEASE STRESS-TEST  D1 -- CHRONIC STRESS / HPA HYPERACTIVITY   SEED=", E.SEED, sep="")
    print("  reused: M17 (arousal inverted-U) + M18 (HPA cortisol)   ADD-ONLY decision-check")
    print("-" * 78)
    print("FAITHFULNESS (the NORMAL arm == the frozen engine):")
    print(f"  HPA  normal peak={f['normal_hpa_peak_min']:.2f} min  "
          f"(engine M18={f['engine_M18_cortisol_peak_min']:.2f})  "
          f"reproduces: {f['hpa_normal_peak_reproduces_engine']}")
    print(f"       normal 1/e recovery={f['normal_recovery_post_peak_min']:.1f} min post-peak  "
          f"in cited [60,90]: {f['normal_recovery_in_cited_window']}")
    print(f"  M17  curve reproduces engine inverted-U bit-for-bit: {f['m17_curve_reproduces_engine']}  "
          f"(peak gain={f['engine_M17_peak_gain']})")
    print("-" * 78)
    print("PERTURBATION (clinical DIRECTION only; magnitudes swept, NOT fitted):")
    print(f"  HPA: basal +{D['perturbation_nominal']['basal_offset']}  "
          f"recovery x{D['perturbation_nominal']['recovery_factor']}  (gain up, feedback down)")
    print(f"  M17: operating gain {p['m17_operating_point_normal']} -> "
          f"{p['m17_operating_point_disease']}  (elevated tonic NE)")
    print("NORMAL -> DISEASE (the contrasts):")
    print(f"  basal cortisol     {_fmt(nh['basal'])} -> {_fmt(nd['basal'])}        "
          f"H1 up: {c['H1_basal_cortisol_up']:.0f}")
    print(f"  recovery post-peak {nh['recovery_post_peak_min']:7.1f} -> "
          f"{nd['recovery_post_peak_min']:7.1f} min   H2 delayed: {c['H2_recovery_delayed']:.0f}  "
          f"(exceeds cited 90: {c['disease_recovery_exceeds_cited_window']:.0f})")
    print(f"  cortisol AUC       {nh['auc']:7.3f} -> {nd['auc']:7.3f}     "
          f"H3 exposure up: {c['H3_auc_exposure_up']:.0f}")
    print(f"  M17 selectivity    {p['m17_selectivity_normal']:7.4f} -> "
          f"{p['m17_selectivity_disease']:7.4f}   H4 attention narrows: "
          f"{c['H4_attention_narrows_selectivity_down']:.0f}")
    print(f"  (curve SHAPE unchanged, only operating point moved: "
          f"{c['m17_curve_shape_unchanged_only_operating_point_moved']:.0f})")
    print("-" * 78)
    print("ANTI-TUNING (shake the grids -> the SIGNS must hold; magnitude irrelevant):")
    print(f"  HPA  basal x recovery grid {a['hpa_basal_grid']} x {a['hpa_recovery_grid']}  "
          f"all signs hold: {a['hpa_all_signs_hold']:.0f}")
    print(f"  M17  shift grid {a['m17_shift_grid']} x 2 distractor grids  "
          f"all signs hold: {a['m17_all_signs_hold']:.0f}")
    print("-" * 78)
    print(f"  INVARIANT  engine tree 0fbf4988... unchanged: {inv['engine_tree_unchanged']:.0f}   "
          f"M0..M16 3a1ebbbb... unchanged: {inv['m0_16_subtree_unchanged']:.0f}")
    print(f"  HONESTY    efficacy={h['medium_efficacy_tested']:.0f}  "
          f"hard_problem_open={h['hard_problem_open']:.0f}  "
          f"consciousness_claim={h['consciousness_claim']:.0f}  "
          f"new_tuned_constants={h['new_tuned_constants']:.0f}")
    print(f"  RESULTS DIGEST  {digest}")
    print(f"  {status}")
    print("=" * 78)
    print("NOTE: construct-validity MECHANISM-DIRECTION test. The disease state is NOT")
    print("      claimed to be felt; efficacy is UNTESTED; the hard problem stays OPEN.")

    # ===================== D3  ANXIETY / PANIC =======================
    D3 = disease_D3_results()
    blob3 = _canon(D3)
    digest3 = hashlib.sha256(blob3).hexdigest()
    with open(os.path.join(HERE, "disease_D3_results.json"), "wb") as fp:
        fp.write(blob3)
    exp3 = os.path.join(HERE, "expected_disease_D3_sha256.json")
    if os.path.exists(exp3):
        prev3 = json.load(open(exp3)).get("disease_D3_results.json")
        status3 = "MATCHES locked digest" if prev3 == digest3 else f"MISMATCH (locked={prev3})"
    else:
        with open(exp3, "w") as fp:
            json.dump({"disease_D3_results.json": digest3,
                       "interoception_atlas_sha256": D3["_meta"]["interoception_atlas_sha256"],
                       "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN}, fp, indent=2)
        status3 = "WROTE expected_disease_D3_sha256.json (first freeze)"

    f3, c3 = D3["faithfulness"], D3["preregistered_contrasts"]
    p3, a3 = D3["normal_vs_disease"], D3["anti_tuning"]
    inv3, h3, pn3 = D3["invariants"], D3["honesty_ledger"], D3["perturbation_nominal"]
    print()
    print("=" * 78)
    print("DISEASE STRESS-TEST  D3 -- ANXIETY / PANIC (interoceptive threat)   SEED=", E.SEED, sep="")
    print("  reused: M18 (interoceptive axis) + M20 (affective access)   ADD-ONLY decision-check")
    print("-" * 78)
    print("FAITHFULNESS (the NORMAL arm == the frozen engine):")
    print(f"  M20  normal actions reproduce engine "
          f"(low='{f3['engine_action_low_stress']}', high='{f3['engine_action_high_stress']}'): "
          f"{f3['m20_normal_actions_reproduce_engine']}")
    print(f"  M18  HEP-arousal slope normal={f3['normal_hep_slope']:.6f}  "
          f"(engine={f3['engine_hep_slope']:.6f})  reproduces: {f3['m18_hep_slope_reproduces_engine']}")
    print("-" * 78)
    print("PERTURBATION (clinical DIRECTION only; magnitudes swept, NOT fitted):")
    print(f"  M20: defensive_bias +{pn3['defensive_bias']}  threat_mult x{pn3['threat_mult']}  "
          f"(anticipatory avoid drive up, threat gain up)")
    print(f"  M18: interoceptive_mult x{pn3['intero_mult']}  (HEP-arousal coupling up)")
    print("NORMAL -> DISEASE (the contrasts):")
    print(f"  avoid onset        {p3['avoid_onset_normal']:.4f} -> {p3['avoid_onset_disease']:.4f}   "
          f"H2 threshold lowered: {c3['H2_avoidance_threshold_lowered']:.0f}")
    print(f"  @subthreshold s={p3['subthreshold_demo_stress']:.4f}: "
          f"normal='{p3['action_normal_at_demo']}' -> disease='{p3['action_disease_at_demo']}'   "
          f"H1 avoid at subthreshold: {c3['H1_avoidance_at_subthreshold_stress']:.0f}")
    print(f"  HEP-arousal slope  {p3['hep_slope_normal']:.4f} -> {p3['hep_slope_disease']:.4f}   "
          f"H3 coupling steeper: {c3['H3_hep_arousal_coupling_steeper']:.0f}")
    print(f"  (D3 perturbs NO reward machinery -- M5 untouched: "
          f"{c3['D3_orthogonal_reward_machinery_untouched']:.0f})")
    print("-" * 78)
    print("ANTI-TUNING (shake the grids -> the SIGNS must hold; magnitude irrelevant):")
    print(f"  M20  bias x threat grid {a3['defensive_bias_grid']} x {a3['threat_mult_grid']}  "
          f"all signs hold: {a3['m20_all_signs_hold']:.0f}")
    print(f"  M18  intero grid {a3['intero_mult_grid']}  all signs hold: {a3['m18_all_signs_hold']:.0f}")
    print("-" * 78)
    print(f"  INVARIANT  engine tree 0fbf4988... unchanged: {inv3['engine_tree_unchanged']:.0f}   "
          f"M0..M16 3a1ebbbb... unchanged: {inv3['m0_16_subtree_unchanged']:.0f}")
    print(f"  HONESTY    efficacy={h3['medium_efficacy_tested']:.0f}  "
          f"hard_problem_open={h3['hard_problem_open']:.0f}  "
          f"consciousness_claim={h3['consciousness_claim']:.0f}  "
          f"new_tuned_constants={h3['new_tuned_constants']:.0f}")
    print(f"  RESULTS DIGEST  {digest3}")
    print(f"  {status3}")
    print("=" * 78)

    # ===================== D2  DEPRESSION / ANHEDONIA ================
    D2 = disease_D2_results()
    blob2 = _canon(D2)
    digest2 = hashlib.sha256(blob2).hexdigest()
    with open(os.path.join(HERE, "disease_D2_results.json"), "wb") as fp:
        fp.write(blob2)
    exp2 = os.path.join(HERE, "expected_disease_D2_sha256.json")
    if os.path.exists(exp2):
        prev2 = json.load(open(exp2)).get("disease_D2_results.json")
        status2 = "MATCHES locked digest" if prev2 == digest2 else f"MISMATCH (locked={prev2})"
    else:
        with open(exp2, "w") as fp:
            json.dump({"disease_D2_results.json": digest2,
                       "affect_observables_atlas_sha256": D2["_meta"]["affect_observables_atlas_sha256"],
                       "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN}, fp, indent=2)
        status2 = "WROTE expected_disease_D2_sha256.json (first freeze)"

    f2, c2 = D2["faithfulness"], D2["preregistered_contrasts"]
    p2, a2 = D2["normal_vs_disease"], D2["anti_tuning"]
    inv2, h2, pn2 = D2["invariants"], D2["honesty_ledger"], D2["perturbation_nominal"]
    print()
    print("=" * 78)
    print("DISEASE STRESS-TEST  D2 -- DEPRESSION / ANHEDONIA   SEED=", E.SEED, sep="")
    print("  reused: M5 (reward RPE) + M17 (arousal) + M19 (mood-congruent recall)   ADD-ONLY")
    print("-" * 78)
    print("FAITHFULNESS (the NORMAL arm == the frozen engine):")
    print(f"  M5   normal p_target={f2['normal_p_target_learned']:.8f}  "
          f"(engine={f2['engine_M5_p_target_learned']:.8f})  reproduces: {f2['m5_normal_reproduces_engine']}")
    print(f"  M19  normal pos-under-pos={f2['normal_m19_pos_under_pos_mood']:.6f}  "
          f"(engine={f2['engine_M19_pos_under_pos_mood']:.6f})  reproduces: {f2['m19_normal_reproduces_engine']}")
    print(f"       engine mood-congruent recall verified: {f2['engine_mood_congruent_helps']}")
    print("-" * 78)
    print("PERTURBATION (clinical DIRECTION only; magnitudes swept, NOT fitted):")
    print(f"  M5 : reward_sensitivity x{pn2['reward_sensitivity']}  (blunted dopamine RPE / anhedonia)")
    print(f"  M19: prevailing mood NEGATIVE  (cue_frac={pn2['recall_cue_fraction']}, "
          f"bias={pn2['mood_bias_strength']})")
    print("NORMAL -> DISEASE (the contrasts):")
    print(f"  learned p_target   {p2['p_target_normal']:.6f} -> {p2['p_target_disease']:.6f}   "
          f"H1 reward blunted: {c2['H1_reward_learning_blunted']:.0f}")
    print(f"  approach gap       {p2['approach_gap_normal']:.6f} -> {p2['approach_gap_disease']:.6f}   "
          f"H2 approach weakened: {c2['H2_approach_valence_weakened']:.0f}")
    print(f"  recall negativity  {p2['recall_negativity_normal_euthymic']:+.6f} -> "
          f"{p2['recall_negativity_disease_depressed']:+.6f}   "
          f"H3 recall shifts negative: {c2['H3_recall_shifts_negative']:.0f}")
    print(f"  (D2 perturbs NO avoidance machinery -- M18/M20 untouched: "
          f"{c2['D2_orthogonal_avoidance_machinery_untouched']:.0f})")
    print("-" * 78)
    print("ANTI-TUNING (shake the grids -> the SIGNS must hold; magnitude irrelevant):")
    print(f"  M5   reward-sens grid {a2['reward_sensitivity_grid']}  "
          f"blunting holds: {a2['m5_blunting_signs_hold']:.0f}  "
          f"gap holds: {a2['m5_approach_gap_signs_hold']:.0f}")
    print(f"  M19  cue x bias grid {a2['recall_cue_grid']} x {a2['recall_bias_grid']}  "
          f"all signs hold: {a2['m19_all_signs_hold']:.0f}")
    print("-" * 78)
    print(f"  INVARIANT  engine tree 0fbf4988... unchanged: {inv2['engine_tree_unchanged']:.0f}   "
          f"M0..M16 3a1ebbbb... unchanged: {inv2['m0_16_subtree_unchanged']:.0f}")
    print(f"  HONESTY    efficacy={h2['medium_efficacy_tested']:.0f}  "
          f"hard_problem_open={h2['hard_problem_open']:.0f}  "
          f"consciousness_claim={h2['consciousness_claim']:.0f}  "
          f"new_tuned_constants={h2['new_tuned_constants']:.0f}")
    print(f"  RESULTS DIGEST  {digest2}")
    print(f"  {status2}")
    print("=" * 78)
    print("NOTE: D1/D3/D2 are construct-validity MECHANISM-DIRECTION tests. The disease")
    print("      states are NOT claimed to be felt; efficacy is UNTESTED; the hard")
    print("      problem stays OPEN. D3 (anxiety) and D2 (anhedonia) perturb DISJOINT")
    print("      handles (M18/M20 vs M5/M19) -- a built-in discriminant-validity check.")

    # ===================== D4  PTSD / HYPERAROUSAL ===================
    D4 = disease_D4_results()
    blob4 = _canon(D4)
    digest4 = hashlib.sha256(blob4).hexdigest()
    with open(os.path.join(HERE, "disease_D4_results.json"), "wb") as fp:
        fp.write(blob4)
    exp4 = os.path.join(HERE, "expected_disease_D4_sha256.json")
    if os.path.exists(exp4):
        prev4 = json.load(open(exp4)).get("disease_D4_results.json")
        status4 = "MATCHES locked digest" if prev4 == digest4 else f"MISMATCH (locked={prev4})"
    else:
        with open(exp4, "w") as fp:
            json.dump({"disease_D4_results.json": digest4,
                       "neuroendocrine_atlas_sha256": D4["_meta"]["neuroendocrine_atlas_sha256"],
                       "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN}, fp, indent=2)
        status4 = "WROTE expected_disease_D4_sha256.json (first freeze)"

    f4, c4 = D4["faithfulness"], D4["preregistered_contrasts"]
    p4, a4 = D4["normal_vs_disease"], D4["anti_tuning"]
    inv4, h4, pn4 = D4["invariants"], D4["honesty_ledger"], D4["perturbation_nominal"]
    print()
    print("=" * 78)
    print("DISEASE STRESS-TEST  D4 -- PTSD / HYPERAROUSAL   SEED=", E.SEED, sep="")
    print("  reused: M17 (arousal inverted-U) + M2 (fear extinction) + M18 (HEP)   ADD-ONLY")
    print("-" * 78)
    print("FAITHFULNESS (the NORMAL arm == the frozen engine):")
    print(f"  M17  curve reproduces engine inverted-U bit-for-bit: {f4['m17_curve_reproduces_engine']}  "
          f"(peak gain={f4['engine_M17_peak_gain']})")
    print(f"  M2   no-extinction fear basin={f4['normal_fear_basin_no_extinction']:.6f}  "
          f"(engine={f4['engine_M2_basin_depth_x_spinodal']:.6f})  reproduces: {f4['m2_basin_reproduces_engine']}")
    print("-" * 78)
    print("PERTURBATION (clinical DIRECTION only; magnitudes swept, NOT fitted):")
    print(f"  M17: tonic arousal floor {pn4['tonic_arousal_floor']}  operating shift +{pn4['operating_point_shift']}  "
          f"(elevated tonic NE)")
    print(f"  M2 : extinction-LTD rate {pn4['extinction_ltd_rate_normal']} -> {pn4['extinction_ltd_rate_disease']}  "
          f"(impaired fear extinction)")
    print("NORMAL -> DISEASE (the contrasts):")
    print(f"  operable arousal band {p4['operable_band_normal']:.0f} -> {p4['operable_band_disease']:.0f}   "
          f"H1 band narrows (협착): {c4['H1_operable_arousal_band_narrows']:.0f}")
    print(f"  M17 selectivity       {p4['m17_selectivity_normal']:.4f} -> {p4['m17_selectivity_disease']:.4f}   "
          f"H2 operating point collapses: {c4['H2_operating_point_selectivity_collapses']:.0f}")
    print(f"  fear basin (post-ext) {p4['fear_basin_normal_extinction']:.4f} -> {p4['fear_basin_disease_extinction']:.4f}   "
          f"H3 intrusion susceptibility up: {c4['H3_extinction_deficit_deepens_fear_basin']:.0f}")
    print(f"  HEP amp @arousal      {p4['hep_amp_normal_arousal']:.4f} -> {p4['hep_amp_disease_arousal']:.4f}   "
          f"H4 rides hyperarousal: {c4['H4_hep_amplitude_rides_hyperarousal']:.0f}")
    print(f"  (D4 leaves the afferent SLOPE at engine value -- NOT D5's blunting handle: "
          f"{c4['D4_orthogonal_afferent_gain_untouched']:.0f})")
    print("-" * 78)
    print("ANTI-TUNING (shake the grids -> the SIGNS must hold; magnitude irrelevant):")
    print(f"  M17  tonic-floor grid {a4['tonic_floor_grid']}  band narrows all: {a4['operable_band_all_signs_hold']:.0f}  "
          f"monotone: {a4['operable_band_monotone']:.0f}")
    print(f"  M2   extinction-rate grid {a4['extinction_rate_grid']}  basin signs hold: "
          f"{a4['extinction_basin_all_signs_hold']:.0f}  monotone: {a4['extinction_basin_monotone']:.0f}")
    print("-" * 78)
    print(f"  INVARIANT  engine tree 0fbf4988... unchanged: {inv4['engine_tree_unchanged']:.0f}   "
          f"M0..M16 3a1ebbbb... unchanged: {inv4['m0_16_subtree_unchanged']:.0f}")
    print(f"  HONESTY    efficacy={h4['medium_efficacy_tested']:.0f}  "
          f"hard_problem_open={h4['hard_problem_open']:.0f}  "
          f"consciousness_claim={h4['consciousness_claim']:.0f}  "
          f"new_tuned_constants={h4['new_tuned_constants']:.0f}")
    print(f"  RESULTS DIGEST  {digest4}")
    print(f"  {status4}")
    print("=" * 78)

    # ===================== D5  AUTONOMIC DYSFUNCTION / INTEROCEPTIVE BLUNTING ====
    D5 = disease_D5_results()
    blob5 = _canon(D5)
    digest5 = hashlib.sha256(blob5).hexdigest()
    with open(os.path.join(HERE, "disease_D5_results.json"), "wb") as fp:
        fp.write(blob5)
    exp5 = os.path.join(HERE, "expected_disease_D5_sha256.json")
    if os.path.exists(exp5):
        prev5 = json.load(open(exp5)).get("disease_D5_results.json")
        status5 = "MATCHES locked digest" if prev5 == digest5 else f"MISMATCH (locked={prev5})"
    else:
        with open(exp5, "w") as fp:
            json.dump({"disease_D5_results.json": digest5,
                       "interoception_atlas_sha256": D5["_meta"]["interoception_atlas_sha256"],
                       "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN}, fp, indent=2)
        status5 = "WROTE expected_disease_D5_sha256.json (first freeze)"

    f5, c5 = D5["faithfulness"], D5["preregistered_contrasts"]
    p5, a5 = D5["normal_vs_disease"], D5["anti_tuning"]
    inv5, h5, pn5 = D5["invariants"], D5["honesty_ledger"], D5["perturbation_nominal"]
    print()
    print("=" * 78)
    print("DISEASE STRESS-TEST  D5 -- AUTONOMIC DYSFUNCTION / INTEROCEPTIVE BLUNTING   SEED=", E.SEED, sep="")
    print("  reused: M18 (afferent HEP axis) + M19 (affective readouts)   ADD-ONLY decision-check")
    print("-" * 78)
    print("FAITHFULNESS (the NORMAL arm == the frozen engine):")
    print(f"  M18  HEP-arousal slope normal={f5['normal_hep_slope']:.6f}  "
          f"(engine={f5['engine_hep_slope']:.6f})  reproduces: {f5['m18_hep_slope_reproduces_engine']}")
    print(f"  M19  pos-under-pos recall normal={f5['normal_m19_pos_under_pos_mood']:.6f}  "
          f"(engine={f5['engine_M19_pos_under_pos_mood']:.6f})  reproduces: {f5['m19_normal_reproduces_engine']}")
    print(f"       engine mood-congruent recall verified: {f5['engine_mood_congruent_helps']}")
    print("-" * 78)
    print("PERTURBATION (clinical DIRECTION only; magnitudes swept, NOT fitted):")
    print(f"  M18: interoceptive afferent gain x{pn5['interoceptive_afferent_gain']}  (vagal afferent blunting)")
    print("NORMAL -> DISEASE (the contrasts):")
    print(f"  HEP-arousal slope     {p5['hep_slope_normal']:.4f} -> {p5['hep_slope_disease']:.4f}   "
          f"H1 slope flattens: {c5['H1_hep_arousal_slope_flattens']:.0f}")
    print(f"  affective margin      {p5['affective_margin_normal']:.4f} -> {p5['affective_margin_disease']:.4f}   "
          f"H2 affective resolution down: {c5['H2_affective_discriminability_margin_shrinks']:.0f}")
    print(f"  (D5 leaves reward machinery (M5) intact -- autonomic blunting != anhedonia: "
          f"{c5['D5_orthogonal_reward_machinery_untouched']:.0f})")
    print(f"  (D5 leaves the M17 arousal operating point at the engine optimum -- not D4's shift: "
          f"{c5['D5_orthogonal_arousal_operating_point_untouched']:.0f})")
    print(f"  (D5 and D3 are OPPOSITE poles of the SAME interoceptive axis: "
          f"{c5['D5_vs_D3_opposite_poles_same_interoceptive_axis']:.0f})")
    print("-" * 78)
    print("ANTI-TUNING (shake the grid -> the SIGNS must hold; magnitude irrelevant):")
    print(f"  M18  intero-gain grid {a5['interoceptive_gain_grid']}  slope signs hold: "
          f"{a5['hep_slope_all_signs_hold']:.0f}  monotone: {a5['hep_slope_monotone']:.0f}")
    print(f"  M19  affective margin signs hold: {a5['affective_margin_all_signs_hold']:.0f}  "
          f"monotone: {a5['affective_margin_monotone']:.0f}")
    print("-" * 78)
    print(f"  INVARIANT  engine tree 0fbf4988... unchanged: {inv5['engine_tree_unchanged']:.0f}   "
          f"M0..M16 3a1ebbbb... unchanged: {inv5['m0_16_subtree_unchanged']:.0f}")
    print(f"  HONESTY    efficacy={h5['medium_efficacy_tested']:.0f}  "
          f"hard_problem_open={h5['hard_problem_open']:.0f}  "
          f"consciousness_claim={h5['consciousness_claim']:.0f}  "
          f"new_tuned_constants={h5['new_tuned_constants']:.0f}")
    print(f"  RESULTS DIGEST  {digest5}")
    print(f"  {status5}")
    print("=" * 78)
    print("NOTE: D4 (PTSD) and D5 (autonomic blunting) BOTH reuse M18 but perturb DISJOINT")
    print("      sub-handles -- D4 moves the arousal OPERATING POINT (HEP rides higher, slope")
    print("      unchanged); D5 lowers the afferent SLOPE (operating point unchanged). D5 also")
    print("      leaves M5 reward intact (!= anhedonia) and is the OPPOSITE interoceptive pole")
    print("      of D3 (hypervigilance). Mechanism-direction only -- felt states stay OPEN.")

    # ===================== D6  BURNOUT / HPA HYPOACTIVITY (terminal) ============
    D6 = disease_D6_results()
    blob6 = _canon(D6)
    digest6 = hashlib.sha256(blob6).hexdigest()
    with open(os.path.join(HERE, "disease_D6_results.json"), "wb") as fp:
        fp.write(blob6)
    exp6 = os.path.join(HERE, "expected_disease_D6_sha256.json")
    if os.path.exists(exp6):
        prev6 = json.load(open(exp6)).get("disease_D6_results.json")
        status6 = "MATCHES locked digest" if prev6 == digest6 else f"MISMATCH (locked={prev6})"
    else:
        with open(exp6, "w") as fp:
            json.dump({"disease_D6_results.json": digest6,
                       "neuroendocrine_atlas_sha256": D6["_meta"]["neuroendocrine_atlas_sha256"],
                       "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN}, fp, indent=2)
        status6 = "WROTE expected_disease_D6_sha256.json (first freeze)"

    f6, c6 = D6["faithfulness"], D6["preregistered_contrasts"]
    p6, a6 = D6["normal_vs_disease"], D6["anti_tuning"]
    inv6, h6, pn6 = D6["invariants"], D6["honesty_ledger"], D6["perturbation_nominal"]
    nh6, nd6, dd6 = p6["hpa_normal"], p6["hpa_disease"], p6["hpa_d1_direction"]
    print()
    print("=" * 78)
    print("DISEASE STRESS-TEST  D6 -- BURNOUT / HPA HYPOACTIVITY (terminal)   SEED=", E.SEED, sep="")
    print("  reused: M18 (HPA cortisol)   ADD-ONLY decision-check -- the MIRROR of D1")
    print("-" * 78)
    print("FAITHFULNESS (the NORMAL arm == the frozen engine):")
    print(f"  HPA  normal peak={f6['normal_hpa_peak_min']:.2f} min  "
          f"(engine M18={f6['engine_M18_cortisol_peak_min']:.2f})  "
          f"reproduces: {f6['hpa_normal_peak_reproduces_engine']}")
    print(f"       normal 1/e recovery={f6['normal_recovery_post_peak_min']:.1f} min post-peak  "
          f"in cited [60,90]: {f6['normal_recovery_in_cited_window']}")
    print("-" * 78)
    print("PERTURBATION (clinical DIRECTION only; magnitudes swept, NOT fitted):")
    print(f"  HPA: acute drive x{pn6['acute_drive_disease']}  (HPA gain DOWN -- blunted reactivity)")
    print("NORMAL -> DISEASE (the contrasts) -- the MIRROR of D1's hyperactivity:")
    print(f"  acute peak value   {nh6['peak_value']:.6f} -> {nd6['peak_value']:.6f}   "
          f"H1 peak abolished: {c6['H1_acute_cortisol_peak_abolished']:.0f}")
    print(f"  cortisol AUC       {nh6['auc']:7.3f} -> {nd6['auc']:7.3f}     "
          f"H2 output down (hypocortisol): {c6['H2_total_cortisol_output_down']:.0f}")
    print(f"  recovery slope     {nh6['recovery_slope']:.6f} -> {nd6['recovery_slope']:.6f}   "
          f"H3 curve flattens: {c6['H3_recovery_curve_flattens']:.0f}")
    print(f"  (kinetics UNCHANGED -- peak time + 1/e recovery identical, amplitude-only loss: "
          f"{c6['hpa_kinetics_unchanged_only_amplitude_lost']:.0f})")
    print(f"  OPPOSITE POLE vs D1 (same HPA axis): AUC  D6 {nd6['auc']:.3f} < "
          f"normal {nh6['auc']:.3f} < D1-dir {dd6['auc']:.3f}   "
          f"({c6['D6_vs_D1_opposite_pole_same_hpa_axis']:.0f})")
    print("-" * 78)
    print("ANTI-TUNING (shake the drive grid -> the SIGNS must hold; magnitude irrelevant):")
    print(f"  HPA  drive grid {a6['acute_drive_grid']}  peak signs hold: {a6['peak_all_signs_hold']:.0f}  "
          f"monotone: {a6['peak_monotone']:.0f}  AUC signs hold: {a6['auc_all_signs_hold']:.0f}")
    print(f"  HPA  recovery-slope signs hold: {a6['recovery_slope_all_signs_hold']:.0f}  "
          f"monotone: {a6['recovery_slope_monotone']:.0f}")
    print("-" * 78)
    print(f"  INVARIANT  engine tree 0fbf4988... unchanged: {inv6['engine_tree_unchanged']:.0f}   "
          f"M0..M16 3a1ebbbb... unchanged: {inv6['m0_16_subtree_unchanged']:.0f}")
    print(f"  HONESTY    efficacy={h6['medium_efficacy_tested']:.0f}  "
          f"hard_problem_open={h6['hard_problem_open']:.0f}  "
          f"consciousness_claim={h6['consciousness_claim']:.0f}  "
          f"new_tuned_constants={h6['new_tuned_constants']:.0f}")
    print(f"  RESULTS DIGEST  {digest6}")
    print(f"  {status6}")
    print("=" * 78)
    print("NOTE: D6 (burnout / HPA hypoactivity) is the MIRROR of D1 (chronic stress / HPA")
    print("      hyperactivity) on the SAME HPA axis -- D1 = cortisol OVERLOAD (AUC/basal up),")
    print("      D6 = cortisol DEPLETION (acute peak abolished, recovery curve flattened). The")
    print("      two are OPPOSITE poles (cortisol output AUC/basal: D6 < normal < D1). Mechanism-")
    print("      direction only; the flattening is amplitude loss (kinetics unchanged); felt")
    print("      exhaustion stays OPEN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
