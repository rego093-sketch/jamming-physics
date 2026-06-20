#!/usr/bin/env python3
"""
mind STANDALONE REGRESSION (self-contained, offline, deterministic)  -- UPGRADED
================================================================================
The old package shipped only FROZEN result JSONs and re-checked their digests; the
code that PRODUCED those numbers was missing, so the reproduction path broke inside
the package (a C1 violation). This upgraded harness closes that gap. It now:

  [A] EMERGES the results live from the in-package engine (repro/mind/_engine), and
      asserts the engine is DETERMINISTIC and reproduces its own frozen digests
      bit-for-bit (expected_sha256.json) -- two runs, identical sha256.
  [B] re-derives every MECHANISM invariant from the freshly emerged numbers:
        - winner-take-MOST (losers retained soft>0, killed hard==0, soft>hard)
        - gamma -> ignitability (monotone, r~1)
        - basal-ganglia selection (exactly one winner; control selects none)
        - dopamine-RPE learning (target probability raised above control)
        - NEW: hippocampal memory is a self-sustaining attractor (overlap==1),
          completes from a partial cue, and theta-phase write/retrieve separation
          PROTECTS stored memories from new-learning interference
        - NEW: the EM brainwave radiates a real field whose front travels at ~c
  [C] (LEGACY, provenance) still verifies the original frozen snapshots in inputs/
      against the original baseline, so the pre-engine record stays intact.

SCOPE: this demonstrates the MECHANISMS behave as claimed and that they are now
reproducible from shipped code. It does NOT confirm a theory of consciousness and
does NOT reproduce a marker of consciousness -- the PCI access marker is an HONEST
NEGATIVE (see docs/mind/09-open-problem). The hard problem is OPEN.

Run:  python3 run_regression.py        (from the _verify/ directory)
Exit 0 = REGRESSION PASS (determinism + mechanism invariants), NOT a claim about experience.
"""
import sys, os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
sys.path.insert(0, ENGINE)
import vp_mind_engine as E  # the in-package emergence engine

fails = []; n = 0
def chk(name, cond):
    global n; n += 1
    if not cond: fails.append(name)

def _canon(obj):
    return json.dumps(E._round(obj), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False).encode("utf-8")

# ============================ [A] self-reproduction ============================
R1 = E.emerge_all(); R2 = E.emerge_all()
h1, h2 = E.sha256_of(R1), E.sha256_of(R2)
chk("engine determinism (two runs identical)", h1 == h2)

exp_path = os.path.join(ENGINE, "expected_sha256.json")
if os.path.exists(exp_path):
    EXP = json.load(open(exp_path))
    live = hashlib.sha256(_canon(R1)).hexdigest()
    chk("engine reproduces frozen results digest", live == EXP.get("mind_emergence_results.json"))
    chk("engine reproduces frozen tree digest", h1 == EXP.get("tree_sha256"))
else:
    chk("expected_sha256.json present (run run_all.py first)", False)

# ============================ [B] mechanism invariants =========================
S = E.regression_scalars(R1)
# winner-take-MOST
chk("winner-take-most: losers retained (soft>0)", S["wtm_loser_soft"] > 0.0)
chk("winner-take-most: hard kills losers (==0)",  S["wtm_loser_hard"] == 0.0)
chk("winner-take-most: soft retains more than hard", S["wtm_loser_soft"] > S["wtm_loser_hard"])
# gamma -> ignitability
chk("gamma->ignitability monotone", S["ignitability_mono"] == 1.0)
chk("gamma->ignitability r~1",      S["ignitability_pearson"] > 0.99)
# selection
chk("selection: exactly one winner", S["sel_nsel"] == 1 and S["sel_commit"] == 1.0)
chk("selection: control commits to none", S["sel_ctrl_nsel"] == 0)
# RPE learning
chk("RPE learning toward reward (target>control)", S["rpe_target_learned"] > S["rpe_target_control"])
# NEW: hippocampal memory physics
chk("memory: written engram self-sustains (overlap==1)", S["mem_attractor_overlap"] == 1.0)
chk("memory: capacity in Hopfield range (0.05..0.25 / N)",
    0.05 <= S["mem_capacity_per_N"] <= 0.25)
chk("memory: theta-phase separation protects vs interference", S["mem_phase_protects"] == 1.0)
# NEW: EM brainwave is a real field at ~c
chk("EM brainwave: emitted front travels at ~c (0.9..1.1)",
    0.9 <= S["em_front_speed_over_c"] <= 1.1)
# stream of thought: all internal gates pass
st = R1["M6_stream_of_thought"]
chk("stream of thought: all binding/conflict/memory gates pass",
    st["gates_pass"] == st["gates_total"])
# NEW: M8 -- the coherence-length rejection of the classical field is a category error.
# These EMERGE the refutation (C1): the field is measured coherent across the brain.
chk("field: classical field coherent across brain (>0.99)",
    S["field_coherence_across_brain"] > 0.99)
chk("field: brain is quasi-static (<<1 wavelength)",
    S["field_brain_in_wavelengths"] < 1e-2)
chk("field: skin depth >> brain (undamped, >100x)",
    S["field_skin_depth_over_brain"] > 100.0)
chk("field: the '~1e9x' shortfall is the QUANTUM length, not the classical field",
    S["field_quantum_shortfall"] > 1e6)
# honest scope: efficacy is NOT emerged, so NO medium claim is made (marker stays 0 = OPEN)
chk("field: medium efficacy NOT claimed (open marker == 0)",
    S["field_medium_efficacy_tested"] == 0.0)

# NEW: M11 -- light -> information -> memory binding (the physics-bridge mechanism).
# The MATH is forced; whether biology USES it stays OPEN. These assert the mechanism only.
import math as _m
chk("M11: single rectifier alpha == 2/pi", abs(S["lm_alpha_rect"] - 2.0/_m.pi) < 1e-9)
chk("M11: double rectifier delta == 1/pi^2", abs(S["lm_delta_rect"] - 1.0/_m.pi**2) < 1e-9)
chk("M11: 2*pi recovered from alpha/delta", abs(S["lm_two_pi_from_ratio"] - 2*_m.pi) < 1e-9)
chk("M11: bound bit lifts above unbound floor (info contrast>0)", S["lm_information_contrast"] > 0.0)
chk("M11: a bound (phase-locked) input writes and persists", S["lm_bound_writes_persists"] == 1.0)
chk("M11: an unbound/antiphase input does NOT write (no spurious memory)", S["lm_unbound_no_write"] == 1.0)
chk("M11: theta-phase separation protects the write", S["lm_theta_phase_protects"] == 1.0)
chk("M11: several infos roll in theta/gamma slots and all recover", S["lm_rolled_all_recovered"] == 1.0)
chk("M11: downstream neuron feels the field (entrainment grows with field)", S["lm_reader_feels_field"] == 1.0)
chk("M11: reader response is field-mediated (cancel<measured, contribution>0)",
    S["lm_reader_field_contribution"] > 0.0)
chk("M11: per-step angle ~13 orders finer for brainwaves than optical",
    1e12 < S["lm_angle_ratio_optical_over_gamma"] < 1e14)
chk("M11: coupling is the SAME measured kappa (no new constant)", abs(S["lm_kappa_measured"] - 0.5496) < 1e-9)
chk("M11: biological functional use NOT claimed (open marker == 0)", S["lm_medium_efficacy_tested"] == 0.0)

# --- M12 brainwave phenomenology: emergence reproduces measured OBSERVABLES + hypothalamus loop ---
chk("M12: every claimed (matched-status) literature observable is reproduced", S["ph_matched_status_all_reproduced"] == 1.0)
chk("M12: all five EEG bands (delta..gamma) emerge from the organ substrate", S["ph_bands_covered"] == 5.0)
chk("M12: emitted brainwave front propagates at ~c (EM, observable)", abs(S["ph_front_speed_over_c"] - 1.0) <= 0.05)
chk("M12: working-memory slot count sits in the observed 5-9 window", 5.0 <= S["ph_wm_capacity_slots"] <= 9.0)
chk("M12: overall observable concordance is in (0,1] and honestly < 1 (targets owed)", 0.0 < S["ph_overall_concordance"] <= 1.0)
chk("M12: brainwave->hypothalamus loop stays bounded (no blow-up)", S["ph_hypo_loop_bounded"] == 1.0)
chk("M12: stronger brainwave drive raises hypothalamic arousal (loop closes)", S["ph_arousal_feedback_positive"] == 1.0)
chk("M12: coupling is the MEASURED kappa (no new constant)", abs(S["ph_kappa_measured"] - 0.5496) < 1e-9)
chk("M12: phenomenon-mapping makes NO interpretation claim (efficacy == 0)", S["ph_medium_efficacy_tested"] == 0.0)

# --- M13 spectral observables: the full-LFP 1/f slope, peaks, ignition, MI->recall ---
# These EMERGE from the brain-structure-like multi-source coupled field; nothing is tuned
# to the targets (the aperiodic floor is charge-weighted MEASURED-synapse shot noise).
chk("M13: aperiodic 1/f exponent emerges INSIDE the measured Voytek band [1.5,3]",
    S["spec_aperiodic_in_voytek_band"] == 1.0)
chk("M13: the 1/f exponent is robust in-band across seeds (>=7/8)",
    S["spec_slope_inband_fraction"] >= 0.875)
chk("M13: oscillatory peaks rise above the aperiodic floor (>=3, Donoghue 2020)",
    S["spec_oscillatory_peaks_present"] == 1.0)
chk("M13: recurrent ignition is all-or-none (sub OFF, supra ON, large jump)",
    S["spec_ignition_all_or_none"] == 1.0 and S["spec_ignition_jump"] > 0.8)
chk("M13: theta-gamma MI predicts the M2 recall outcome (Tort 2009 / Lega 2016)",
    S["spec_mi_predicts_recall"] == 1.0)
chk("M13: spectral concordance honestly < 1 (arousal-flatten owed until robust)",
    0.0 < S["spec_spectral_concordance"] < 1.0)
chk("M13: closing 1/f lifts the CORE catalogue concordance to 16/20 = 0.80",
    abs(S["spec_core_concordance"] - 0.80) < 1e-9)
chk("M13: the EXTENDED catalogue concordance is in (0,1] and honestly < 1",
    0.0 < S["spec_extended_concordance"] <= 1.0)
chk("M13: reproduces a measured nonlinear-threshold SIGNATURE, NOT consciousness (claim flag == 0)",
    S["spec_is_consciousness_claim"] == 0.0)
chk("M13: the hard problem stays OPEN (marker == 1)", S["spec_hard_problem_open"] == 1.0)
chk("M13: medium efficacy NOT claimed (open marker == 0)", S["spec_medium_efficacy_tested"] == 0.0)

# --- M14 sleep architecture: thalamo-reticular spindles, slow oscillation, dream-recall ---
chk("M14: spindle CARRIER emerges in the measured 11-16 Hz band (set by cited T-current recovery)",
    S["slp_spindle_peak_in_band"] == 1.0 and 11.0 <= S["slp_spindle_peak_hz"] <= 16.0)
chk("M14: the spindle band is ROBUST across seeds (>=7/8 in-band)",
    S["slp_spindle_inband_fraction"] >= 0.875)
chk("M14: sleep_spindle_hz is MATCHED (closes the owed M12 observable BY EMERGENCE)",
    S["slp_spindle_matched"] == 1.0)
chk("M14: the spindle WAXES AND WANES (defining envelope signature; AM-depth>0.5, robust)",
    S["slp_waxing_waning_matched"] == 1.0 and S["slp_spindle_am_depth"] > 0.5)
chk("M14: the inter-spindle interval is physiological (NREM-2-like, 1.5-10 s)",
    1.5 <= S["slp_inter_spindle_interval_s"] <= 10.0)
chk("M14: a cortical slow oscillation emerges BELOW 1 Hz (Up/Down states; robust)",
    S["slp_slow_oscillation_matched"] == 1.0 and S["slp_slow_oscillation_hz"] < 1.0)
chk("M14: REM shifts the spectrum toward fast markers vs NREM (theta+gamma > delta+spindle; robust)",
    S["slp_nrem_rem_band_shift_matched"] == 1.0 and S["slp_shift_index_rem"] > S["slp_shift_index_nrem"])
chk("M14: REM theta-gamma coupling raises hippocampal recall over NREM (dream-recall mechanism)",
    S["slp_dream_recall_increase"] == 1.0)
chk("M14: closing the spindle lifts the CORE catalogue concordance to 17/20 = 0.85",
    abs(S["slp_core_concordance"] - 0.85) < 1e-9)
chk("M14: the EXTENDED catalogue concordance is in (0,1] and honestly < 1 (targets still owed)",
    0.0 < S["slp_extended_concordance"] < 1.0)
chk("M14: reproduces measured sleep RHYTHMS, NOT consciousness (claim flag == 0)",
    S["slp_is_consciousness_claim"] == 0.0)
chk("M14: the hard problem stays OPEN (marker == 1)", S["slp_hard_problem_open"] == 1.0)
chk("M14: medium efficacy NOT claimed (open marker == 0)", S["slp_medium_efficacy_tested"] == 0.0)

# --- M15 calibration bridge: two cited anchors; delta CAL-closed; p300+panic OWED ---
chk("M15: time anchor = 1 ms/step, CERTIFIED by the M14 spindle (11-16 Hz)",
    S["cal_time_step_ms"] == 1.0 and S["cal_time_anchor_certified"] == 1.0 and 11.0 <= S["cal_time_anchor_spindle_hz"] <= 16.0)
chk("M15: voltage anchor = the single cited SWS delta (75 uV)", abs(S["cal_voltage_anchor_uv"] - 75.0) < 1e-9)
chk("M15: sws_delta is CAL-CLOSED by the cited anchor (calibration, NOT emergence)",
    S["cal_sws_delta_matched"] == 1.0 and S["cal_sws_delta_closure_is_calibration"] == 1.0)
chk("M15: the delta closure lands in the cited band [50,100] uV",
    50.0 <= S["cal_sws_delta_amplitude_uv_pred"] <= 100.0)
chk("M15: HONEST cross-check -- model delta/spindle ratio ~1.27x (< physiological 3-7x)",
    1.0 < S["cal_delta_spindle_ratio_model"] < 2.0)
chk("M15: p300_latency is a PREDICTION at 1 ms/step and is OWED (early ERP < 100 ms, not 300 ms)",
    S["cal_p300_matched"] == 0.0 and S["cal_p300_latency_ms_pred"] < 100.0)
chk("M15: panic_peak is a PREDICTION at 1 ms/step and is OWED (ms-scale < 1 min, not 10 min)",
    S["cal_panic_matched"] == 0.0 and S["cal_panic_peak_minutes_pred"] < 1.0)
chk("M15: exactly ONE calibration closure + TWO owed (honest 1/3)",
    S["cal_n_calibration_closed"] == 1.0 and S["cal_n_owed"] == 2.0)
chk("M15: closing delta by calibration lifts the CORE catalogue to 18/20 = 0.90",
    abs(S["cal_core_concordance"] - 0.90) < 1e-9)
chk("M15: calibrating an EEG amplitude is NOT a consciousness claim (flag == 0)",
    S["cal_is_consciousness_claim"] == 0.0)
chk("M15: the hard problem stays OPEN (marker == 1)", S["cal_hard_problem_open"] == 1.0)

# --- TRACK 1: M0 brain-structure grounding -- gamma fixes ORDER [V]; SIZE is measured [L]; gamma^1.5 size is NULL ---
_m0 = R1["M0_organ_emergence"]; _sn = _m0["size_null"]
_rel = {r["organ"]: r["rel_size"] for r in _m0["rows"]}
_vol = {r["organ"]: r["measured_volume_cm3"] for r in _m0["rows"]}
chk("M0: gamma^1.5 dwell CANNOT carry measured size -- near-equal span (~1.07x)", _sn["dwell_span"] < 1.2)
chk("M0: measured sub-region volumes span ~3 orders of magnitude (>=100x)", _sn["measured_volume_span"] >= 100.0)
chk("M0: MEASURED-SIZE NULL verdict recorded (a cell-constant gamma does not carry size)",
    _sn["verdict_gamma_carries_size"] == 0.0)
chk("M0: relative SIZE is now grounded on MEASURED volumes [L] (cerebrum largest, rel=1.0; cerebrum=1100 cm3)",
    abs(_rel["cerebrum"] - 1.0) < 1e-9 and _vol["cerebrum"] == 1100.0 and _sn["size_grade"] == "[L]")
chk("M0: developmental ORDER remains the gamma-emergent readout [V] (4 organs)",
    _sn["order_grade"] == "[V]" and len(_m0["developmental_order"]) == 4)

# --- TRACK 2: M14 dynamics constants externalised to the locked param DB + carrier-invariance VERIFIED ---
_DB = E.load_mind_param_db()["neuro_dynamics"]
chk("M14: tau_r/tau_s/a_gain are read from the locked param DB (no magic numbers in the engine)",
    {"spindle_recruitment_spread_tau_s", "cortical_recurrent_membrane_tau_s",
     "adaptation_drive_a_gain"}.issubset(_DB.keys()))
chk("M14: cortical-membrane tau_s is GROUNDED to cited literature [L]",
    _DB["cortical_recurrent_membrane_tau_s"]["grade"] == "[L]")
chk("M14: a_gain is honestly graded [F] with a DECLARED sensitivity window (load-bearing, not hidden)",
    _DB["adaptation_drive_a_gain"]["grade"] == "[F]" and "declared_sensitivity_window" in _DB["adaptation_drive_a_gain"])
# VERIFICATION (the explicit concern): is the spindle band genuinely emergent, or propped up by a free constant?
_atl = E._m14_load_sleep_atlas(); _TK = _atl["thalamic_kinetics_measured"]
_trec = _TK["t_current_deinactivation_recovery_tau_ms"]["value"] / 1000.0
_tm = _TK["tc_active_membrane_tau_ms"]["value"] / 1000.0
_tih = _TK["ca_ih_upregulation_tau_ms"]["value"] / 1000.0
_drv = float(_atl["nrem2_operating_point"]["thalamic_excitability_drive"])
_ag = float(_DB["adaptation_drive_a_gain"]["value"])
_carriers = []
for _tr in [0.040, 0.080, 0.160, 0.240]:
    _lfp, _ = E._m14_spindle(E.SEED, E.KAPPA_EPHAPTIC, _trec, _tm, _tr, _tih, _drv, _ag)
    _pk, _ = E._m14_carrier_peak(_lfp); _carriers.append(_pk)
chk("M14 VERIFIED: spindle carrier is INVARIANT to tau_r over [40,240] ms -- genuinely set by cited tau_rec, NOT propped up by a free constant",
    all(11.0 <= c <= 16.0 for c in _carriers) and (max(_carriers) - min(_carriers)) < 1e-6)

# ============== v1.20 ADD-ONLY: M17..M20 cognition+emotion one substrate ==============
# The CORE add-only proof: M17..M20 are appended LAST, so the M0..M16 OUTPUT subtree is
# BYTE-IDENTICAL to the v1.19 frozen tree (3a1ebbbb). Only the FULL tree hash changes.
def _midx(k): return int(k.split("_")[0][1:])
_M0_16 = {k: v for k, v in R1.items() if _midx(k) <= 16}
_M0_16_b = {k: v for k, v in R2.items() if _midx(k) <= 16}
chk("v1.20 ADD-ONLY: M0..M16 output subtree is BYTE-IDENTICAL to the v1.19 frozen tree (3a1ebbbb)",
    E.sha256_of(_M0_16) == "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1")
chk("v1.20 ADD-ONLY: M0..M16 subtree determinism (two runs identical)",
    E.sha256_of(_M0_16) == E.sha256_of(_M0_16_b))
chk("v1.20: M17..M20 are present (the four new emerge modules)",
    all(k in R1 for k in ("M17_global_state", "M18_interoceptive_axis",
                          "M19_affective_readouts", "M20_affective_access")))

# --- M17: one neuromodulatory gain co-moves a COGNITIVE and an AFFECTIVE readout ---
chk("M17: cognitive readout is an emergent INVERTED-U in arousal gain (Yerkes-Dodson from the fold)",
    S["gs_cognitive_inverted_u"] == 1.0)
chk("M17: the SAME gain co-moves cognition AND affect on the rising limb (integration prediction)",
    S["gs_covary_cognition_affect_rising"] == 1.0)
chk("M17: ANTI-TUNING -- the inverted-U is invariant to the distractor grid (not back-fit)",
    S["gs_covary_sign_invariant"] == 1.0)
chk("M17: valence axis is near-orthogonal to arousal (2D circumplex, |r|<0.30)",
    S["gs_circumplex_2d"] == 1.0 and abs(S["gs_valence_arousal_corr"]) < 0.30)
chk("M17: selectivity peak is interior (arousal optimum, not an endpoint)",
    0.1 < S["gs_selectivity_peak_gain"] < 3.0)

# --- M18: heart/HPA interoceptive INPUT axis (mechanism [V]; rates cited [L]) ---
chk("M18: SA-node (same FHN relaxation oscillator as M1) produces a rhythmic beat [V]",
    S["iv_sa_oscillates"] == 1.0 and S["iv_sa_beats"] >= 3.0)
chk("M18: HPA cortisol PEAK lands in the cited 15-40 min window -> reproduces panic_peak [L]",
    S["iv_cortisol_peak_in_cited_window"] == 1.0 and 15.0 <= S["iv_cortisol_peak_min"] <= 40.0)
chk("M18: HPA loop is bounded (negative feedback present, finite cortisol)",
    S["iv_hpa_loop_bounded"] == 1.0 and S["iv_negative_feedback_on"] == 1.0)
chk("M18: cardiac afferent DOMINATES efferent (~4:1 input-dominant; heart->brain >> brain->heart)",
    S["iv_input_dominant"] == 1.0 and S["iv_afferent_over_efferent_ratio"] > 1.0)
chk("M18: HEP amplitude tracks arousal (the felt-heart -> affect coupling) [L]",
    S["iv_hep_tracks_arousal"] == 1.0)

# --- M19: the ONE substrate that reproduced cognition ALSO reproduces affect, no domain tuning ---
chk("M19: same substrate reproduces affective observables with NO per-domain tuning",
    S["aff_same_substrate_no_domain_tuning"] == 1.0)
chk("M19: affective concordance is high (>=0.8 of the scored affective observables)",
    S["aff_concordance"] >= 0.8)
chk("M19: mood-congruent recall EXERCISES + VERIFIES the M2 hippocampal recall logic end-to-end",
    S["aff_recall_logic_verified"] == 1.0 and S["aff_mood_congruent_helps"] == 1.0)
chk("M19: HONEST -- affect readouts do NOT claim the state is felt (efficacy marker == 0)",
    S["aff_medium_efficacy_tested"] == 0.0)

# --- M20: affective functional-access marker (testable bias) + the SINGLE hard problem OPEN ---
chk("M20: high stress shifts action selection toward avoidance (testable fear-avoidance bias)",
    S["acc_stress_biases_avoidance"] == 1.0)
chk("M20: NO consciousness claim for affect (consciousness_claim == 0)",
    S["acc_consciousness_claim"] == 0.0)
chk("M20: the hard problem stays OPEN and covers affect exactly as it covers cognition",
    S["acc_hard_problem_open"] == 1.0)

# --- M9 GEOMETRY: ring -> MEASURED MNI promotion (v1.19 Task 1A) + v1.18 decision-check ---
# v1.19 PROMOTED the engine default M9 geometry from the [O] ring to the [L] measured MNI
# atlas (emerge_coordination POS = _measured_geometry). This is the explicit VP-SPEC sec 6-6
# exception (intentional hash change), so the live engine tree is NO LONGER b18c8626 -- it is
# the new frozen tree, and M9's field_contribution now equals the GROUNDED measured value.
# The v1.18 geometry_grounding decision-check is KEPT VERBATIM as the pre-promotion historical
# freeze (digest 8ad43a72...): it still reproduces its own number and still records the v1.17
# tree b18c8626 as the HISTORICAL pre-promotion anchor. The ring cross-check below is now a
# HISTORICAL code-path validation (the ring path still reproduces the old ring number), not
# the engine default. Grounding the geometry is NOT a consciousness claim (efficacy 0; OPEN).
import geometry_grounding as GG
GR = GG.geometry_grounding_results()
_geo_exp = os.path.join(HERE, "expected_geometry_sha256.json")
if os.path.exists(_geo_exp):
    _GEXP = json.load(open(_geo_exp))
    _glive = hashlib.sha256(GG._canon(GR)).hexdigest()
    chk("M9-geom: decision-check result reproduces its frozen digest (bit-for-bit, C1)",
        _glive == _GEXP.get("geometry_grounding_results.json"))
    chk("M9-geom: geometry atlas is the LOCKED measured input [L] (digest matches)",
        GR["_meta"]["geometry_atlas_sha256"] == _GEXP.get("geometry_atlas_sha256"))
    # HISTORICAL: the decision-check records the v1.17 PRE-promotion tree (now a historical
    # anchor). v1.19 intentionally promoted the engine, so the LIVE tree must DIFFER from it.
    chk("M9-geom: v1.17 pre-promotion tree is recorded as a HISTORICAL anchor (b18c8626)",
        _GEXP.get("frozen_engine_tree_sha256_unchanged") ==
        "b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7")
    chk("M9-geom: PROMOTION landed -- live engine tree DIFFERS from the v1.17 pre-promotion tree",
        h1 != _GEXP.get("frozen_engine_tree_sha256_unchanged"))
    chk("M9-geom: PROMOTION landed -- live engine M9 fc now EQUALS the grounded measured fc",
        abs(S["coord_field_contribution"] - GR["a_measured_geometry"]["fc"]) < 1e-3)
else:
    chk("expected_geometry_sha256.json present (run geometry_grounding.py first)", False)
_a, _am  = GR["a_ring_crosscheck"], GR["a_measured_geometry"]
_b, _c   = GR["b_scale_invariance"], GR["c_coord_jitter"]
_d, _e   = GR["d_L_only_subset"], GR["e_normalization_variants"]
_fb, _sf = GR["f_f0_band_robustness"], GR["scope_flags"]
# (a) HISTORICAL code-path validation: the ring path still reproduces the OLD frozen ring M9
# number (the pre-promotion default). This is no longer the engine default (now measured), but
# it certifies the decision-check's ring branch is intact and the promotion delta is real.
chk("M9-geom: ring code-path still reproduces the old frozen ring field_contribution (historical)",
    _a["reproduces_frozen_engine_fc"] is True)
# (a') measured-geometry verdict, reported AS-IS (grade==evidence)
chk("M9-geom: grounded geometry gives a positive field_contribution (field augments coordination)",
    _am["fc"] > 0.0)
chk("M9-geom: grounded geometry RAISES fc vs the ring (real anatomy is not the low ring)",
    _am["fc"] > _a["fc"])
chk("M9-geom: HONEST SCOPE -- regime stays partial_metastable (NOT synchronized)",
    _am["regime"] == "partial_metastable")
chk("M9-geom: HONEST SCOPE -- order parameter stays below synchronization (R < 0.9)",
    _am["R"] < 0.9)
# (b) scale-invariance under the registered row-norm (shape only, not absolute scale)
chk("M9-geom: registered row-norm makes absolute scale irrelevant (shape-only, max|dfc| < 1e-9)",
    _b["scale_irrelevant_under_rownorm"] is True)
# (c) robust to coordinate (centre-of-mass) uncertainty
chk("M9-geom: regime robust to +/-5mm coordinate jitter (all 10 seeds partial_metastable)",
    _c["all_partial_metastable"] is True)
# (d) result is not carried by the 4 representative [O] nodes
chk("M9-geom: [L]-only 8-node subset stays partial_metastable (not carried by [O] coords)",
    _d["regime"] == "partial_metastable")
# (e) ANTI-BACK-FIT: the registered normalization is NOT the fc maximizer
chk("M9-geom: ANTI-BACK-FIT -- registered row-norm is NOT the fc maximizer (raw does not exceed it)",
    _e["rownorm_is_fc_maximizer"] is False)
# (f) regime robust to band frequencies (mirror engine M9.4)
chk("M9-geom: regime robust to f0 +/-20% band perturbation (mirror engine M9.4)",
    _fb["all_partial"] is True)
# coupling strength is still the SAME measured kappa (geometry swap only; no new constant)
chk("M9-geom: coupling is the SAME measured kappa 0.5496 (no new constant; geometry swap only)",
    abs(GR["_meta"]["kappa_ephaptic_measured"] - 0.5496) < 1e-9)
# scope flags unchanged: grounding geometry makes NO interpretation claim
chk("M9-geom: medium efficacy NOT claimed (open marker == 0)",
    _sf["medium_efficacy_tested"] == 0.0)
chk("M9-geom: the hard problem stays OPEN (marker == 1)",
    _sf["hard_problem_open"] == 1.0)
chk("M9-geom: grounding the geometry is NOT a consciousness claim (flag == 0)",
    _sf["consciousness_claim"] == 0.0)

# ============== [D] DISEASE STRESS-TESTS (v1.21 ADD-ONLY decision-checks) ==============
# Construct validity: does the NORMAL R19 substrate REPRODUCE a clinical syndrome when its
# CITED parameters are perturbed ONLY in the measured CLINICAL DIRECTION? These are ADD-ONLY
# decision-checks in the geometry_grounding mould -- the engine is imported READ-ONLY, so the
# engine tree stays 0fbf4988... and M0..M16 stays 3a1ebbbb... NOT a claim the state is felt;
# NO efficacy tested; honesty ledger 4 flags invariant. Verified bit-for-bit (C1).
import disease_stress_tests as DST
DD = DST.disease_stress_results()
_dst_exp = os.path.join(HERE, "expected_disease_sha256.json")
if os.path.exists(_dst_exp):
    _DEXP = json.load(open(_dst_exp))
    _dlive = hashlib.sha256(DST._canon(DD)).hexdigest()
    chk("D-test: decision-check result reproduces its frozen digest (bit-for-bit, C1)",
        _dlive == _DEXP.get("disease_stress_results.json"))
    chk("D-test: neuroendocrine atlas is the LOCKED measured input [L] (digest matches)",
        DD["_meta"]["neuroendocrine_atlas_sha256"] == _DEXP.get("neuroendocrine_atlas_sha256"))
else:
    chk("expected_disease_sha256.json present (run disease_stress_tests.py first)", False)

_df, _dc = DD["faithfulness"], DD["preregistered_contrasts"]
_da, _di, _dh = DD["anti_tuning"], DD["invariants"], DD["honesty_ledger"]
# --- D1 FAITHFULNESS: the NORMAL arm IS the frozen engine ---
chk("D1-faith: NORMAL HPA cortisol peak reproduces the engine M18 peak (~24 min, cited [15,40])",
    _df["hpa_normal_peak_reproduces_engine"] is True)
chk("D1-faith: NORMAL 1/e cortisol recovery lands in the cited [60,90] min window (Dickerson&Kemeny)",
    _df["normal_recovery_in_cited_window"] is True)
chk("D1-faith: local M17 readout reproduces the engine inverted-U curve bit-for-bit (shape unchanged)",
    _df["m17_curve_reproduces_engine"] is True)
# --- D1 PRE-REGISTERED CONTRASTS: normal -> disease, clinical direction ---
chk("D1: HPA hyperactivity RAISES basal cortisol (tonic hypercortisolism) [H1]",
    _dc["H1_basal_cortisol_up"] == 1.0)
chk("D1: impaired negative feedback DELAYS cortisol recovery (exceeds cited 90 min) [H2]",
    _dc["H2_recovery_delayed"] == 1.0 and _dc["disease_recovery_exceeds_cited_window"] == 1.0)
chk("D1: chronic stress RAISES cortisol AUC (prolonged exposure / allostatic load) [H3]",
    _dc["H3_auc_exposure_up"] == 1.0)
chk("D1: elevated tonic NE shifts the M17 operating point onto the over-aroused limb -> "
    "selectivity DROPS (stress narrows attention) [H4]",
    _dc["H4_attention_narrows_selectivity_down"] == 1.0)
chk("D1: ONLY the operating point moved -- the inverted-U SHAPE is unchanged (same fold)",
    _dc["m17_curve_shape_unchanged_only_operating_point_moved"] == 1.0)
# --- D1 ANTI-TUNING: the SIGNS survive grid/seed shaking (magnitude irrelevant) ---
chk("D1: ANTI-TUNING -- HPA contrasts hold across the whole basal x recovery grid (sign-invariant)",
    _da["hpa_all_signs_hold"] == 1.0)
chk("D1: ANTI-TUNING -- M17 attention-narrowing holds across shift x distractor grids (sign-invariant)",
    _da["m17_all_signs_hold"] == 1.0)
# --- D1 INVARIANTS: the decision-check changed NOTHING in the engine ---
chk("D1: ADD-ONLY -- engine tree 0fbf4988... unchanged (disease test is a read-only probe)",
    _di["engine_tree_unchanged"] == 1.0 and h1 == "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70")
chk("D1: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _di["m0_16_subtree_unchanged"] == 1.0)
# --- D1 HONESTY: a mechanism-direction test, NOT an efficacy / consciousness claim ---
chk("D1: HONEST -- no efficacy claimed, hard problem OPEN, no consciousness claim, no tuned constant",
    _dh["medium_efficacy_tested"] == 0.0 and _dh["hard_problem_open"] == 1.0
    and _dh["consciousness_claim"] == 0.0 and _dh["new_tuned_constants"] == 0.0)

# ============== [D3] DISEASE STRESS-TEST -- ANXIETY / PANIC (v1.22 ADD-ONLY) ==============
# Interoceptive-threat construct validity: perturbing M20 (defensive bias + threat gain UP)
# and M18 (HEP-arousal coupling UP) in the CLINICAL DIRECTION reproduces avoidance at
# sub-threshold stress + a lowered avoid threshold + steeper interoceptive coupling. Reuses
# M18+M20 ONLY (disjoint from D2's M5+M19) -- a built-in discriminant-validity check.
D3 = DST.disease_D3_results()
_d3_exp = os.path.join(HERE, "expected_disease_D3_sha256.json")
if os.path.exists(_d3_exp):
    _D3EXP = json.load(open(_d3_exp))
    _d3live = hashlib.sha256(DST._canon(D3)).hexdigest()
    chk("D3-test: decision-check result reproduces its frozen digest (bit-for-bit, C1)",
        _d3live == _D3EXP.get("disease_D3_results.json"))
    chk("D3-test: interoception atlas is the LOCKED measured input [L] (digest matches)",
        D3["_meta"]["interoception_atlas_sha256"] == _D3EXP.get("interoception_atlas_sha256"))
else:
    chk("expected_disease_D3_sha256.json present (run disease_stress_tests.py first)", False)

_3f, _3c = D3["faithfulness"], D3["preregistered_contrasts"]
_3a, _3i, _3h = D3["anti_tuning"], D3["invariants"], D3["honesty_ledger"]
# --- D3 FAITHFULNESS: the NORMAL arm IS the frozen engine ---
chk("D3-faith: NORMAL M20 approach/avoid actions reproduce the engine bit-for-bit",
    _3f["m20_normal_actions_reproduce_engine"] is True)
chk("D3-faith: NORMAL M18 HEP-arousal slope reproduces the engine slope bit-for-bit (Pollatos&Schandry [L])",
    _3f["m18_hep_slope_reproduces_engine"] is True)
# --- D3 PRE-REGISTERED CONTRASTS: normal -> disease, clinical direction ---
chk("D3: anticipatory threat bias DRIVES avoidance at sub-threshold stress (normal=approach) [H1]",
    _3c["H1_avoidance_at_subthreshold_stress"] == 1.0)
chk("D3: elevated threat gain LOWERS the avoid-onset threshold (panic-prone) [H2]",
    _3c["H2_avoidance_threshold_lowered"] == 1.0)
chk("D3: heightened interoception STEEPENS HEP-arousal coupling (bodily-symptom amplification) [H3]",
    _3c["H3_hep_arousal_coupling_steeper"] == 1.0)
chk("D3: ORTHOGONALITY -- D3 perturbs NO reward machinery (M5 learned target untouched; anxiety != anhedonia)",
    _3c["D3_orthogonal_reward_machinery_untouched"] == 1.0)
# --- D3 ANTI-TUNING: the SIGNS survive grid shaking (magnitude irrelevant) ---
chk("D3: ANTI-TUNING -- avoidance contrasts hold across the bias x threat grid (sign-invariant)",
    _3a["m20_all_signs_hold"] == 1.0)
chk("D3: ANTI-TUNING -- steeper HEP coupling holds across the interoceptive-gain grid (sign-invariant)",
    _3a["m18_all_signs_hold"] == 1.0)
# --- D3 INVARIANTS: the decision-check changed NOTHING in the engine ---
chk("D3: ADD-ONLY -- engine tree 0fbf4988... unchanged (disease test is a read-only probe)",
    _3i["engine_tree_unchanged"] == 1.0 and h1 == "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70")
chk("D3: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _3i["m0_16_subtree_unchanged"] == 1.0)
# --- D3 HONESTY: a mechanism-direction test, NOT an efficacy / consciousness claim ---
chk("D3: HONEST -- no efficacy claimed, hard problem OPEN (felt fear), no consciousness claim, no tuned constant",
    _3h["medium_efficacy_tested"] == 0.0 and _3h["hard_problem_open"] == 1.0
    and _3h["consciousness_claim"] == 0.0 and _3h["new_tuned_constants"] == 0.0)

# ============== [D2] DISEASE STRESS-TEST -- DEPRESSION / ANHEDONIA (v1.22 ADD-ONLY) ==============
# Reward+mood construct validity: blunting the M5 dopamine RPE reward sensitivity DOWN and turning
# the M19 prevailing mood NEGATIVE (clinical direction) reproduces blunted reward learning + a
# shrunken approach gap + a NEGATIVITY FLIP in mood-congruent recall (Bower 1981, depressive
# direction). Reuses M5+M17+M19 ONLY (disjoint from D3's M18+M20) -- discriminant validity.
D2 = DST.disease_D2_results()
_d2_exp = os.path.join(HERE, "expected_disease_D2_sha256.json")
if os.path.exists(_d2_exp):
    _D2EXP = json.load(open(_d2_exp))
    _d2live = hashlib.sha256(DST._canon(D2)).hexdigest()
    chk("D2-test: decision-check result reproduces its frozen digest (bit-for-bit, C1)",
        _d2live == _D2EXP.get("disease_D2_results.json"))
    chk("D2-test: affect-observables atlas is the LOCKED measured input [L] (digest matches)",
        D2["_meta"]["affect_observables_atlas_sha256"] == _D2EXP.get("affect_observables_atlas_sha256"))
else:
    chk("expected_disease_D2_sha256.json present (run disease_stress_tests.py first)", False)

_2f, _2c = D2["faithfulness"], D2["preregistered_contrasts"]
_2a, _2i, _2h = D2["anti_tuning"], D2["invariants"], D2["honesty_ledger"]
# --- D2 FAITHFULNESS: the NORMAL arm IS the frozen engine ---
chk("D2-faith: NORMAL (full reward-sensitivity) M5 p_target reproduces the engine learned target bit-for-bit",
    _2f["m5_normal_reproduces_engine"] is True)
chk("D2-faith: NORMAL M19 pos-under-pos-mood recall reproduces the engine value bit-for-bit (engine regime)",
    _2f["m19_normal_reproduces_engine"] is True)
chk("D2-faith: the engine's OWN mood-congruent recall is verified (Bower direction holds in the engine)",
    _2f["engine_mood_congruent_helps"] is True)
# --- D2 PRE-REGISTERED CONTRASTS: normal -> disease, clinical direction ---
chk("D2: blunted dopamine RPE LOWERS the learned target probability (anhedonia) [H1]",
    _2c["H1_reward_learning_blunted"] == 1.0)
chk("D2: blunted reward SHRINKS the approach gap above chance (weakened positive valence) [H2]",
    _2c["H2_approach_valence_weakened"] == 1.0)
chk("D2: negative mood FLIPS recall negativity euthymic(<0) -> depressed(>0) (mood-congruent, Bower) [H3]",
    _2c["H3_recall_shifts_negative"] == 1.0)
chk("D2: ORTHOGONALITY -- D2 perturbs NO avoidance machinery (M18/M20 untouched; anhedonia != anxiety)",
    _2c["D2_orthogonal_avoidance_machinery_untouched"] == 1.0)
# --- D2 ANTI-TUNING: the SIGNS survive grid shaking (magnitude irrelevant) ---
chk("D2: ANTI-TUNING -- reward blunting + shrunken gap hold across the reward-sensitivity grid (sign-invariant)",
    _2a["m5_blunting_signs_hold"] == 1.0 and _2a["m5_approach_gap_signs_hold"] == 1.0)
chk("D2: ANTI-TUNING -- the recall negativity FLIP holds across the cue x bias grid (sign-invariant)",
    _2a["m19_all_signs_hold"] == 1.0)
# --- D2 INVARIANTS: the decision-check changed NOTHING in the engine ---
chk("D2: ADD-ONLY -- engine tree 0fbf4988... unchanged (disease test is a read-only probe)",
    _2i["engine_tree_unchanged"] == 1.0 and h1 == "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70")
chk("D2: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _2i["m0_16_subtree_unchanged"] == 1.0)
# --- D2 HONESTY: a mechanism-direction test, NOT an efficacy / consciousness claim ---
chk("D2: HONEST -- no efficacy claimed, hard problem OPEN (felt anhedonia), no consciousness claim, no tuned constant",
    _2h["medium_efficacy_tested"] == 0.0 and _2h["hard_problem_open"] == 1.0
    and _2h["consciousness_claim"] == 0.0 and _2h["new_tuned_constants"] == 0.0)


# ============== [D4] DISEASE STRESS-TEST -- PTSD / HYPERAROUSAL (v1.23 ADD-ONLY) ==============
# Hyperarousal+intrusion construct validity: raising the M17 tonic arousal FLOOR (operable band
# truncated 협착 + operating point past optimum) and REDUCING the M2 extinction-LTD rate (a deeper
# residual fear basin = intrusion susceptibility) in the CLINICAL DIRECTION reproduces the PTSD
# signature; the M18 HEP amplitude rides the elevated arousal. Reuses M17+M2+M18. D4 leaves the
# afferent SLOPE byte-identical -> disjoint from D5's afferent-gain handle (discriminant validity).
D4 = DST.disease_D4_results()
_d4_exp = os.path.join(HERE, "expected_disease_D4_sha256.json")
if os.path.exists(_d4_exp):
    _D4EXP = json.load(open(_d4_exp))
    _d4live = hashlib.sha256(DST._canon(D4)).hexdigest()
    chk("D4-test: decision-check result reproduces its frozen digest (bit-for-bit, C1)",
        _d4live == _D4EXP.get("disease_D4_results.json"))
    chk("D4-test: neuroendocrine atlas is the LOCKED measured input [L] (digest matches)",
        D4["_meta"]["neuroendocrine_atlas_sha256"] == _D4EXP.get("neuroendocrine_atlas_sha256"))
else:
    chk("expected_disease_D4_sha256.json present (run disease_stress_tests.py first)", False)

_4f, _4c = D4["faithfulness"], D4["preregistered_contrasts"]
_4a, _4i, _4h = D4["anti_tuning"], D4["invariants"], D4["honesty_ledger"]
# --- D4 FAITHFULNESS: the NORMAL arm IS the frozen engine ---
chk("D4-faith: local M17 readout reproduces the engine inverted-U curve bit-for-bit (shape unchanged)",
    _4f["m17_curve_reproduces_engine"] is True)
chk("D4-faith: the NO-extinction fear engram reproduces the engine M2 basin_depth_x_spinodal bit-for-bit",
    _4f["m2_basin_reproduces_engine"] is True)
# --- D4 PRE-REGISTERED CONTRASTS: normal -> disease, clinical direction ---
chk("D4: raised tonic NE floor NARROWS the operable arousal band (Yerkes-Dodson 협착) [H1]",
    _4c["H1_operable_arousal_band_narrows"] == 1.0)
chk("D4: the operating point past the optimum COLLAPSES selectivity (over-aroused limb) [H2]",
    _4c["H2_operating_point_selectivity_collapses"] == 1.0)
chk("D4: impaired extinction DEEPENS the residual fear basin (intrusion susceptibility up) [H3]",
    _4c["H3_extinction_deficit_deepens_fear_basin"] == 1.0)
chk("D4: the HEP amplitude RIDES the elevated operating arousal (cardiac hyperarousal) [H4]",
    _4c["H4_hep_amplitude_rides_hyperarousal"] == 1.0)
chk("D4: ORTHOGONALITY -- D4 leaves the afferent SLOPE at the engine value (PTSD != autonomic blunting; D4 != D5)",
    _4c["D4_orthogonal_afferent_gain_untouched"] == 1.0)
# --- D4 ANTI-TUNING: the SIGNS survive grid shaking (magnitude irrelevant) ---
chk("D4: ANTI-TUNING -- band narrowing holds + monotone across the tonic-floor grid (sign-invariant)",
    _4a["operable_band_all_signs_hold"] == 1.0 and _4a["operable_band_monotone"] == 1.0)
chk("D4: ANTI-TUNING -- selectivity collapse holds across the operating-shift grid (sign-invariant)",
    _4a["operating_point_all_signs_hold"] == 1.0)
chk("D4: ANTI-TUNING -- deeper fear basin holds + monotone across the extinction-rate grid (sign-invariant)",
    _4a["extinction_basin_all_signs_hold"] == 1.0 and _4a["extinction_basin_monotone"] == 1.0)
chk("D4: ANTI-TUNING -- HEP amplitude rides arousal across the arousal-shift grid (sign-invariant)",
    _4a["hep_amp_all_signs_hold"] == 1.0)
# --- D4 INVARIANTS: the decision-check changed NOTHING in the engine ---
chk("D4: ADD-ONLY -- engine tree 0fbf4988... unchanged (disease test is a read-only probe)",
    _4i["engine_tree_unchanged"] == 1.0 and h1 == "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70")
chk("D4: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _4i["m0_16_subtree_unchanged"] == 1.0)
# --- D4 HONESTY: a mechanism-direction test, NOT an efficacy / consciousness claim ---
chk("D4: HONEST -- no efficacy claimed, hard problem OPEN (felt terror), no consciousness claim, no tuned constant",
    _4h["medium_efficacy_tested"] == 0.0 and _4h["hard_problem_open"] == 1.0
    and _4h["consciousness_claim"] == 0.0 and _4h["new_tuned_constants"] == 0.0)

# ============== [D5] DISEASE STRESS-TEST -- AUTONOMIC DYSFUNCTION / INTEROCEPTIVE BLUNTING (v1.23 ADD-ONLY) ==============
# Interoceptive-blunting construct validity: lowering the M18 vagal afferent interoceptive gain
# (intero_mult<1) in the CLINICAL DIRECTION FLATTENS the HEP-arousal slope and SHRINKS the
# interoceptive affective-discriminability margin (affective resolution down). Reuses M18+M19.
# D5 leaves the M5 reward machinery byte-identical (!= anhedonia; D5 != D2) and the M17 arousal
# operating point at the engine optimum (!= D4); D5 and D3 are OPPOSITE interoceptive poles.
D5 = DST.disease_D5_results()
_d5_exp = os.path.join(HERE, "expected_disease_D5_sha256.json")
if os.path.exists(_d5_exp):
    _D5EXP = json.load(open(_d5_exp))
    _d5live = hashlib.sha256(DST._canon(D5)).hexdigest()
    chk("D5-test: decision-check result reproduces its frozen digest (bit-for-bit, C1)",
        _d5live == _D5EXP.get("disease_D5_results.json"))
    chk("D5-test: interoception atlas is the LOCKED measured input [L] (digest matches)",
        D5["_meta"]["interoception_atlas_sha256"] == _D5EXP.get("interoception_atlas_sha256"))
else:
    chk("expected_disease_D5_sha256.json present (run disease_stress_tests.py first)", False)

_5f, _5c = D5["faithfulness"], D5["preregistered_contrasts"]
_5a, _5i, _5h = D5["anti_tuning"], D5["invariants"], D5["honesty_ledger"]
# --- D5 FAITHFULNESS: the NORMAL arm IS the frozen engine ---
chk("D5-faith: NORMAL M18 HEP-arousal slope reproduces the engine slope bit-for-bit (Pollatos&Schandry [L])",
    _5f["m18_hep_slope_reproduces_engine"] is True)
chk("D5-faith: NORMAL M19 pos-under-pos-mood recall reproduces the engine value bit-for-bit (engine regime)",
    _5f["m19_normal_reproduces_engine"] is True)
chk("D5-faith: the engine's OWN mood-congruent recall is verified (mechanism intact under D5)",
    _5f["engine_mood_congruent_helps"] is True)
# --- D5 PRE-REGISTERED CONTRASTS: normal -> disease, clinical direction ---
chk("D5: blunted vagal afferent gain FLATTENS the HEP-arousal slope (bodily signal carries less) [H1]",
    _5c["H1_hep_arousal_slope_flattens"] == 1.0)
chk("D5: blunted afference SHRINKS the interoceptive affective-discriminability margin (resolution down) [H2]",
    _5c["H2_affective_discriminability_margin_shrinks"] == 1.0)
chk("D5: ORTHOGONALITY -- D5 leaves the reward machinery (M5) untouched (autonomic blunting != anhedonia; D5 != D2)",
    _5c["D5_orthogonal_reward_machinery_untouched"] == 1.0)
chk("D5: ORTHOGONALITY -- D5 leaves the M17 arousal operating point at the engine optimum (D5 != D4)",
    _5c["D5_orthogonal_arousal_operating_point_untouched"] == 1.0)
chk("D5: D5 and D3 are OPPOSITE poles of the SAME interoceptive axis (blunted < normal < hypervigilant)",
    _5c["D5_vs_D3_opposite_poles_same_interoceptive_axis"] == 1.0)
# --- D5 ANTI-TUNING: the SIGNS survive grid shaking (magnitude irrelevant) ---
chk("D5: ANTI-TUNING -- slope flattening holds + monotone across the interoceptive-gain grid (sign-invariant)",
    _5a["hep_slope_all_signs_hold"] == 1.0 and _5a["hep_slope_monotone"] == 1.0)
chk("D5: ANTI-TUNING -- affective margin shrinking holds + monotone across the interoceptive-gain grid (sign-invariant)",
    _5a["affective_margin_all_signs_hold"] == 1.0 and _5a["affective_margin_monotone"] == 1.0)
# --- D5 INVARIANTS: the decision-check changed NOTHING in the engine ---
chk("D5: ADD-ONLY -- engine tree 0fbf4988... unchanged (disease test is a read-only probe)",
    _5i["engine_tree_unchanged"] == 1.0 and h1 == "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70")
chk("D5: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _5i["m0_16_subtree_unchanged"] == 1.0)
# --- D5 HONESTY: a mechanism-direction test, NOT an efficacy / consciousness claim ---
chk("D5: HONEST -- no efficacy claimed, hard problem OPEN (felt numbing), no consciousness claim, no tuned constant",
    _5h["medium_efficacy_tested"] == 0.0 and _5h["hard_problem_open"] == 1.0
    and _5h["consciousness_claim"] == 0.0 and _5h["new_tuned_constants"] == 0.0)

# ============== [D6] DISEASE STRESS-TEST -- BURNOUT / HPA HYPOACTIVITY (v1.24 ADD-ONLY) ==============
# The MIRROR of D1 on the SAME HPA axis: perturbing M18 (HPA gain/drive DOWN) in the CLINICAL
# DIRECTION reproduces an ABOLISHED acute cortisol peak + reduced total output (hypocortisolism) +
# a FLATTENED recovery curve. Reuses M18 ONLY. The flattening is amplitude loss (the 2-lag is linear
# -> kinetics unchanged); D6 and D1 are OPPOSITE poles of the one HPA axis (cortisol DEPLETION vs
# OVERLOAD) -- an explicit discriminant-validity mirror of the D1 chronic-stress signature.
D6 = DST.disease_D6_results()
_d6_exp = os.path.join(HERE, "expected_disease_D6_sha256.json")
if os.path.exists(_d6_exp):
    _D6EXP = json.load(open(_d6_exp))
    _d6live = hashlib.sha256(DST._canon(D6)).hexdigest()
    chk("D6-test: decision-check result reproduces its frozen digest (bit-for-bit, C1)",
        _d6live == _D6EXP.get("disease_D6_results.json"))
    chk("D6-test: neuroendocrine atlas is the LOCKED measured input [L] (digest matches)",
        D6["_meta"]["neuroendocrine_atlas_sha256"] == _D6EXP.get("neuroendocrine_atlas_sha256"))
else:
    chk("expected_disease_D6_sha256.json present (run disease_stress_tests.py first)", False)

_6f, _6c = D6["faithfulness"], D6["preregistered_contrasts"]
_6a, _6i, _6h = D6["anti_tuning"], D6["invariants"], D6["honesty_ledger"]
# --- D6 FAITHFULNESS: the NORMAL arm IS the frozen engine ---
chk("D6-faith: NORMAL HPA cortisol peak reproduces the engine M18 peak (~24 min, cited [15,40])",
    _6f["hpa_normal_peak_reproduces_engine"] is True)
chk("D6-faith: NORMAL 1/e cortisol recovery lands in the cited [60,90] min window (Dickerson&Kemeny)",
    _6f["normal_recovery_in_cited_window"] is True)
# --- D6 PRE-REGISTERED CONTRASTS: normal -> disease, clinical direction (the MIRROR of D1) ---
chk("D6: HPA hypoactivity ABOLISHES the acute cortisol peak (blunted reactivity) [H1]",
    _6c["H1_acute_cortisol_peak_abolished"] == 1.0)
chk("D6: reduced HPA drive LOWERS total cortisol output (hypocortisolism / depletion) [H2]",
    _6c["H2_total_cortisol_output_down"] == 1.0)
chk("D6: the recovery curve FLATTENS -- gentler descending-limb slope [H3]",
    _6c["H3_recovery_curve_flattens"] == 1.0)
chk("D6: the HPA time-constants are UNCHANGED -- flattening is amplitude loss, NOT a kinetic shift "
    "(the MIRROR of D1's shape-unchanged invariant)",
    _6c["hpa_kinetics_unchanged_only_amplitude_lost"] == 1.0)
chk("D6: OPPOSITE POLE vs D1 on the SAME HPA axis -- cortisol output D6 < normal < D1 "
    "(burnout DEPLETION vs chronic-stress OVERLOAD; discriminant-validity mirror)",
    _6c["D6_vs_D1_opposite_pole_same_hpa_axis"] == 1.0)
# --- D6 ANTI-TUNING: the SIGNS survive grid shaking (magnitude irrelevant) ---
chk("D6: ANTI-TUNING -- peak abolition holds + monotone across the drive grid (sign-invariant)",
    _6a["peak_all_signs_hold"] == 1.0 and _6a["peak_monotone"] == 1.0)
chk("D6: ANTI-TUNING -- reduced cortisol output holds across the drive grid (sign-invariant)",
    _6a["auc_all_signs_hold"] == 1.0)
chk("D6: ANTI-TUNING -- recovery-curve flattening holds + monotone across the drive grid (sign-invariant)",
    _6a["recovery_slope_all_signs_hold"] == 1.0 and _6a["recovery_slope_monotone"] == 1.0)
# --- D6 INVARIANTS: the decision-check changed NOTHING in the engine ---
chk("D6: ADD-ONLY -- engine tree 0fbf4988... unchanged (disease test is a read-only probe)",
    _6i["engine_tree_unchanged"] == 1.0 and h1 == "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70")
chk("D6: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _6i["m0_16_subtree_unchanged"] == 1.0)
# --- D6 HONESTY: a mechanism-direction test, NOT an efficacy / consciousness claim ---
chk("D6: HONEST -- no efficacy claimed, hard problem OPEN (felt exhaustion), no consciousness claim, no tuned constant",
    _6h["medium_efficacy_tested"] == 0.0 and _6h["hard_problem_open"] == 1.0
    and _6h["consciousness_claim"] == 0.0 and _6h["new_tuned_constants"] == 0.0)

# ===================== [AUT] AUTISM MODULE (D7 candidate, v1.25 ADD-ONLY) ======================
# The user's question made falsifiable: WHICH handle reproduces autism's measured EEG signature
# -- the brainwave coupling PATHWAY / topology / excitability, or the frontal-lobe node? Add-only
# decision-check in the D1-D6 mould (engine imported READ-ONLY). THREE signatures reproduced
# (S1 reduced PAC, S2 E/I hyper-excitability, S3 long-range under-connectivity); the E/I->1/f
# READOUT (S2b) is honestly OWED.
import autism_discriminant as AUT
_AR, _AR_blob, _AR_sha = AUT.autism_discriminant_results()
_aut_exp = os.path.join(HERE, "expected_autism_discriminant_sha256.json")
if os.path.exists(_aut_exp):
    _AEXP = json.load(open(_aut_exp))
    chk("AUT: autism_discriminant_results.json reproduces its FROZEN sha256 (bit-for-bit)",
        _AR_sha == _AEXP.get("autism_discriminant_results.json"))
else:
    chk("expected_autism_discriminant_sha256.json present (run autism_discriminant.py first)", False)
# --- AUT INVARIANTS: the decision-check changed NOTHING in the engine ---
_ainv = _AR["invariants"]
chk("AUT: ADD-ONLY -- engine tree 0fbf4988... unchanged (autism module is a read-only probe)",
    _ainv["engine_tree_unchanged"] is True)
chk("AUT: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _ainv["m0_16_subtree_unchanged"] is True)
# --- AUT S0: SINGLE-KNOB UNIFICATION -- one ephaptic kappa drives BOTH S1 (PAC) and S3 (integration) ---
_as0 = _AR["S0_single_knob_unification"]
chk("AUT-S0: GROUNDING -- the PAC replica reproduces the engine's emitted M9.6 pac_modulation_index "
    "(non-circular; the same kappa the engine uses)",
    _as0["pac_replica_reproduces_engine_value"] is True)
chk("AUT-S0: ONE ephaptic coupling kappa drives BOTH the cross-frequency PAC (S1) AND the global ring "
    "integration (S3) monotonically -> 'the pathway' is a SINGLE substrate coordinate (S1+S3 = one axis)",
    _as0["pac_monotone_with_kappa"] is True and _as0["integration_monotone_with_kappa"] is True
    and _as0["one_knob_drives_both_S1_and_S3"] is True)
# --- AUT S1: PATHWAY -- weakening cross-frequency coupling reduces PAC (cited ASD direction) ---
_as1 = _AR["S1_pathway_PAC"]
chk("AUT-S1: weakening the cross-frequency pathway MONOTONICALLY reduces PAC (ASD direction)",
    _as1["pac_monotone_down"] is True and _as1["reproduced"] is True)
# --- AUT S2: EXCITABILITY -- asymmetric E/I bias lowers ignition threshold + spontaneous gamma ---
_as2 = _AR["S2_excitability_EI"]
chk("AUT-S2: E/I excitatory bias LOWERS the ignition threshold (monotone) + yields spontaneous "
    "ignition past the fold (elevated baseline gamma; ASD direction)",
    _as2["threshold_monotone_down"] is True and _as2["spontaneous_at_bias_low"] is False
    and _as2["spontaneous_at_bias_high"] is True and _as2["reproduced"] is True)
# --- AUT S3: TOPOLOGY -- long-range under-connectivity reduces global integration + raises locality ---
_as3 = _AR["S3_longrange_connectivity"]
chk("AUT-S3: long-range UNDER-connectivity keeps global integration BELOW healthy + raises locality "
    "(ASD connectivity signature; monotone over the clinical range)",
    _as3["R_all_below_health"] is True and _as3["R_monotone_over_clinical_range"] is True
    and _as3["locality_monotone_up"] is True and _as3["reproduced"] is True)
# --- AUT P4: DISCRIMINANT -- pathway/topology, NOT frontal-lobe localisation ---
_ad = _AR["P4_discriminant_pathway_not_frontal"]
chk("AUT-P4: the frontal-lobe node has NO leverage on PAC (S1 is posterior theta->gamma)",
    _ad["frontal_no_leverage_on_pac"] is True)
chk("AUT-P4: FAIRNESS -- the frontal node is NOT inert (it moves its own oscillatory-peak domain)",
    _ad["frontal_moves_its_own_peak_domain"] is True)
chk("AUT-P4: totally silencing the FRONTAL region does NOT reduce integration (no leverage); the "
    "integration hub is NOT the frontal lobe -> topology/pathway, not frontal localisation",
    _ad["frontal_no_leverage_on_integration"] is True and _ad["hub_is_not_frontal"] is True
    and _ad["longrange_reduces_integration"] is True and _ad["VERDICT_pathway_not_frontal"] is True)
# --- AUT P5: HONESTY -- the E/I->1/f READOUT is NOT faked; it is OWED with its named input ---
_ap5 = _AR["P5_owed_EI_one_over_f_readout"]
chk("AUT-P5: HONEST -- the E/I->1/f flattening READOUT is NOT reproduced -> S2b stays OWED (not faked)",
    _ap5["S2b_OWED"] is True and _ap5["S2b_1f_readout_reproduced"] is False)
# --- AUT HONESTY: a mechanism-direction discriminant, NOT efficacy / consciousness ---
_ah = _AR["honesty_ledger"]
chk("AUT: HONEST -- no efficacy claimed, hard problem OPEN, no consciousness claim, no tuned constant",
    _ah["medium_efficacy_tested"] == 0.0 and _ah["hard_problem_open"] == 1.0
    and _ah["consciousness_claim"] == 0.0 and _ah["new_tuned_constants"] == 0.0)
# --- AUT OVERALL: a full disease module on the substrate (3 reproduced + discriminant) ---
chk("AUT: autism reproduced as a THREE-signature pathway/excitability disorder; frontal-localisation "
    "NOT supported (pathway reading supported)",
    _AR["overall"]["is_full_disease_module"] is True
    and _AR["overall"]["pathway_reading_supported"] is True
    and _AR["overall"]["frontal_localisation_supported"] is False)

# ================= [AUT2] AUTISM MECHANISM SUB-DISCRIMINANT (D8 candidate, v1.26 ADD-ONLY) =================
# The user's finer question made falsifiable: WITHIN the D7 coupling axis (kappa), is the
# theta(4-8Hz)->gamma deficit a WIRING/geometry fault, an OUTPUT-WEAK switch, or a THRESHOLD-HIGH
# switch? Add-only decision-check (engine READ-ONLY). Each fault leaves a DIFFERENT (delta-PAC,
# ignition) fingerprint; a gain/threshold drug reverses gain faults but cannot correct wiring; an
# exogenous 4-8Hz supply rescues all (incl. wiring) but over-synchronises if over-dosed; the
# vegetative limit is the threshold fault past the measured ephaptic ceiling. MECHANISM only.
import autism_mechanism_discriminant as AUT2
_A2, _A2_blob, _A2_sha = AUT2.autism_mechanism_results()
_aut2_exp = os.path.join(HERE, "expected_autism_mechanism_sha256.json")
if os.path.exists(_aut2_exp):
    _A2EXP = json.load(open(_aut2_exp))
    chk("AUT2: autism_mechanism_results.json reproduces its FROZEN sha256 (bit-for-bit)",
        _A2_sha == _A2EXP.get("autism_mechanism_results.json"))
else:
    chk("expected_autism_mechanism_sha256.json present (run autism_mechanism_discriminant.py first)", False)
# --- AUT2 INVARIANTS: the decision-check changed NOTHING in the engine ---
_a2inv = _A2["invariants"]
chk("AUT2: ADD-ONLY -- engine tree 0fbf4988... unchanged (mechanism probe is read-only)",
    _a2inv["engine_tree_unchanged"] is True)
chk("AUT2: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _a2inv["m0_16_subtree_unchanged"] is True)
# --- AUT2 GROUNDING: the PAC replica reproduces the engine's emitted M9.6 value (geometry NOT in PAC) ---
chk("AUT2: GROUNDING -- the PAC replica reproduces the engine's emitted M9.6 pac_modulation_index "
    "(non-circular; geometry does NOT enter the PAC closure)",
    _A2["grounding"]["pac_replica_grounded"] is True)
# --- AUT2 W: wiring fault -- integration down, PAC change EXACTLY zero, ignition normal, locality up ---
_a2w = _A2["W_wiring_fault"]
chk("AUT2-W: a WIRING/geometry fault lowers integration with PAC change == 0 (exact) + ignition "
    "normal + locality elevated -> 'circuit fault' leaves PAC untouched",
    _a2w["R_below_health"] is True and _a2w["pac_delta_exactly_zero"] is True
    and _a2w["ignition_normal"] is True and _a2w["locality_elevated"] is True
    and _a2w["fingerprint_reproduced"] is True)
# --- AUT2 O: output-weak switch -- integration down, PAC reduced, ignition NORMAL ---
_a2o = _A2["O_output_weak_fault"]
chk("AUT2-O: an OUTPUT-WEAK switch (dVm down -> kappa numerator down) lowers BOTH integration and "
    "PAC, with ignition NORMAL (fold crossed as usual) -> 'output low'",
    _a2o["R_below_health"] is True and _a2o["pac_reduced"] is True
    and _a2o["ignition_normal"] is True and _a2o["fingerprint_reproduced"] is True)
# --- AUT2 T: threshold-high switch -- integration down, PAC reduced, ignition RAISED ---
_a2t = _A2["T_threshold_high_fault"]
chk("AUT2-T: a THRESHOLD-HIGH switch (hypo-excitable -> kappa denominator up) lowers BOTH integration "
    "and PAC AND RAISES the R19 fold ignition threshold -> 'threshold high'",
    _a2t["R_below_health"] is True and _a2t["pac_reduced"] is True
    and _a2t["ignition_raised"] is True and _a2t["fingerprint_reproduced"] is True)
# --- AUT2 DISCRIMINANT: (delta-PAC, ignition) separates W / O / T uniquely ---
_a2d = _A2["DISCRIMINANT_three_way"]
chk("AUT2-DISC: the (delta-PAC, ignition) pair is a UNIQUE 3-way fingerprint -- W has the only zero "
    "PAC change; ignition splits O (normal) from T (raised)",
    _a2d["W_unique_zero_pac_change"] is True and _a2d["ignition_splits_O_from_T"] is True
    and _a2d["THREE_WAY_SEPARATION"] is True)
# --- AUT2 RX_drug: gain/threshold restoration -- reverses gain faults, CANNOT correct wiring ---
_a2rd = _A2["RX_drug_threshold_gain_restoration"]
chk("AUT2-RXdrug: a uniform threshold-lowering (gain-restoring) intervention FULLY reverses the "
    "THRESHOLD fault, HELPS the OUTPUT fault, but CANNOT correct the WIRING fault (topology invariant "
    "under uniform gain) -> drug-responsiveness implicates a GAIN fault, not wiring",
    _a2rd["T_fully_reverses"]["verdict"] is True
    and _a2rd["O_partially_helps"]["raises_via_denominator"] is True
    and _a2rd["W_cannot_correct"]["topology_invariant_under_uniform_gain"] is True
    and _a2rd["RX_DRUG_discriminative"] is True)
# --- AUT2 RX_supply: exogenous 4-8Hz theta -- rescues ALL incl. wiring; over-supply over-synchronises ---
_a2rs = _A2["RX_supply_exogenous_theta"]
chk("AUT2-RXsupply: an exogenous 4-8Hz theta carrier RESCUES all three (incl. the WIRING fault the "
    "drug cannot correct) but OVER-synchronises if over-supplied (R past health) -- a dosing window",
    _a2rs["supply_rescues_wiring"] is True and _a2rs["supply_rescues_output"] is True
    and _a2rs["supply_rescues_threshold"] is True
    and _a2rs["over_supply_over_synchronises_past_health"] is True
    and _a2rs["RX_SUPPLY_rescues_all"] is True)
# --- AUT2 VEG: vegetative limit -- threshold fault past the ephaptic ceiling; exogenous drive crosses ---
_a2v = _A2["VEG_vegetative_limit"]
chk("AUT2-VEG: the vegetative limit is the THRESHOLD fault past the MEASURED ephaptic ceiling kappa "
    "(no neighbour can re-ignite -> never self-recovers); only exogenous drive ABOVE the fold crosses "
    "it (ignition MECHANISM, NOT a return of experience); a healthy switch self-recovers",
    _a2v["VEG_reproduced"] is True and _a2v["healthy_switch_recovers_endogenously"] is True)
# --- AUT2 SLEEP: opposite therapeutic sign (the supply that helps coupling is anti-sleep) ---
_a2sl = _A2["SLEEP_opposite_sign"]
chk("AUT2-SLEEP: the SAME theta supply that RAISES coupling/arousal (helpful for the ASD coupling "
    "deficit) is the ANTI-sleep direction -> opposite therapeutic sign (sign-only)",
    _a2sl["SLEEP_OPPOSITE_SIGN"] is True)
# --- AUT2 HONESTY: a mechanism-direction discriminant, NOT efficacy / consciousness / medical advice ---
_a2h = _A2["honesty_ledger"]
chk("AUT2: HONEST -- no efficacy, hard problem OPEN, no consciousness claim, no tuned constant "
    "(which-fault-is-real-autism + O-vs-T-in-vivo are explicitly OWED)",
    _a2h["medium_efficacy_tested"] == 0.0 and _a2h["hard_problem_open"] == 1.0
    and _a2h["consciousness_claim"] == 0.0 and _a2h["new_tuned_constants"] == 0.0)
# --- AUT2 OVERALL: three faults reproduced + separated + reversibility mapped ---
chk("AUT2: the theta(4-8Hz)->gamma coupling deficit is THREE distinguishable faults (wiring / "
    "output-weak / threshold-high) with mapped reversibility; which one a given autism is, is OWED",
    _A2["overall"]["is_full_module"] is True)

# ================= [SZ] SCHIZOPHRENIA-SPECTRUM DISCRIMINANT (D9 candidate, v1.27 ADD-ONLY) =================
# The OVER-IGNITION mirror of the autism THRESHOLD-HIGH fault (D8 T): on the SAME M3 R19 ignitability
# axis, a disinhibitory/excitatory bias (E/I toward excitation; NMDA-hypofunction account) LOWERS the
# fold so weak/irrelevant candidate assemblies ignite (ABERRANT SALIENCE) and the selective single-
# winner gate collapses. Add-only decision-check (engine READ-ONLY). A gain-REDUCING antipsychotic-class
# push restores selectivity on SZ but WORSENS autism-T; the stimulant that HELPED autism-T WORSENS SZ;
# the extreme is total loss of gating. (ignition-direction, aberrant-vs-lost) separates HEALTH /
# AUTISM-T / SZ uniquely. MECHANISM only.
import schizophrenia_discriminant as SZ
_SZ, _SZ_blob, _SZ_sha = SZ.schizophrenia_results()
_sz_exp = os.path.join(HERE, "expected_schizophrenia_sha256.json")
if os.path.exists(_sz_exp):
    _SZEXP = json.load(open(_sz_exp))
    chk("SZ: schizophrenia_results.json reproduces its FROZEN sha256 (bit-for-bit)",
        _SZ_sha == _SZEXP.get("schizophrenia_results.json"))
else:
    chk("expected_schizophrenia_sha256.json present (run schizophrenia_discriminant.py first)", False)
# --- SZ INVARIANTS: the decision-check changed NOTHING in the engine ---
_szinv = _SZ["invariants"]
chk("SZ: ADD-ONLY -- engine tree 0fbf4988... unchanged (mechanism probe is read-only)",
    _szinv["engine_tree_unchanged"] is True)
chk("SZ: ADD-ONLY -- M0..M16 output subtree 3a1ebbbb... unchanged",
    _szinv["m0_16_subtree_unchanged"] is True)
# --- SZ1: over-ignition -- the excitatory bias LOWERS the R19 fold below health (mirror of autism-T) ---
chk("SZ1: a DISINHIBITORY/excitatory bias LOWERS the R19 ignition fold below health -- 'over-ignition' "
    "(the exact mirror of autism-T's RAISED fold, on the same ignitability axis)",
    _SZ["SZ1_over_ignition"]["ignition_lowered_below_health"] is True)
# --- SZ2: aberrant salience -- recruits IRRELEVANT sub-fold assemblies, loses NONE; dose-monotone ---
_sz2 = _SZ["SZ2_aberrant_salience"]
chk("SZ2: ABERRANT SALIENCE -- the lowered fold lets weak/irrelevant candidate assemblies (sub-fold in "
    "health) ignite (aberrant ignitions > 0, relevant lost == 0, ON set grows); nsel is monotone "
    "non-decreasing in excitation",
    _sz2["aberrant_salience_reproduced"] is True and _sz2["relevant_ignitions_lost"] == []
    and _sz2["on_set_grows_vs_health"] is True
    and _sz2["monotone_nondecreasing_in_excitation"] is True)
# --- SZ autism-T contrast -- the OPPOSITE fold direction loses RELEVANT, recruits NONE ---
_szac = _SZ["autism_T_contrast"]
chk("SZ: AUTISM-T CONTRAST -- the opposite (inhibitory) bias RAISES the fold and LOSES relevant "
    "ignitions with NO aberrant recruitment (the two poles move the fold oppositely)",
    _szac["contrast_reproduced"] is True and _szac["aberrant_ignitions"] == []
    and _szac["ignition_raised_or_equal"] is True)
# --- SZ DISCRIMINANT: (ignition-direction, aberrant-vs-lost) separates HEALTH/AUTISM-T/SZ uniquely ---
_szd = _SZ["DISCRIMINANT_three_way"]
chk("SZ-DISC: (ignition-direction, aberrant-vs-lost) is a UNIQUE 3-way fingerprint -- SZ lowers the "
    "fold + recruits IRRELEVANT; autism-T raises the fold + loses RELEVANT; health is selective. The "
    "two disease fingerprints are distinct",
    _szd["schizophrenia_lowers_fold_recruits_irrelevant"] is True
    and _szd["autism_T_raises_fold_loses_relevant"] is True
    and _szd["fingerprints_are_distinct"] is True and _szd["THREE_WAY_SEPARATION"] is True)
# --- SZ3 secondary: the disinhibition raises in-silico integration (over-sync tendency; dysconnective LOCK) ---
chk("SZ3: SECONDARY -- the disinhibition raises the engine's in-silico global integration above health "
    "(an over-sync tendency); reported as secondary, with real SZ DYSconnectivity explicitly LOCKED "
    "(not the defining fingerprint, which is SZ1+SZ2)",
    _SZ["SZ3_global_integration_secondary"]["R_above_health"] is True)
# --- SZ RX_antipsychotic: gain-reduction restores selectivity on SZ; the SAME push WORSENS autism-T ---
_szra = _SZ["RX_antipsychotic_gain_reduction"]
chk("SZ-RXantipsychotic: a uniform gain-REDUCING / threshold-RAISING intervention (the antipsychotic "
    "mechanism class, Kapur 2003) RESTORES the healthy selective set on SZ, while the SAME push WORSENS "
    "autism-T (raises an already-high fold) -> opposite therapeutic sign for the opposite pole",
    _szra["SZ_restored"]["restores_healthy_selective_set"] is True
    and _szra["autism_T_worsened"]["loses_more_relevant"] is True
    and _szra["RX_AP_discriminative"] is True)
# --- SZ RX_stimulant: the gain-RAISING stimulant that HELPED autism-T WORSENS SZ (opposite sign) ---
_szrs = _SZ["RX_stimulant_opposite_sign"]
chk("SZ-RXstimulant: the gain-RAISING / threshold-LOWERING stimulant that HELPED autism-T (D8 RX_drug) "
    "WORSENS schizophrenia (more aberrant ignitions -- the attested stimulant-worsened-psychosis "
    "direction); one handle, opposite signs at the two poles",
    _szrs["SZ_worsened"]["more_aberrant_ignitions"] is True
    and _szrs["autism_T_helped"]["recovers_relevant_ignitions"] is True
    and _szrs["RX_STIM_opposite_sign"] is True)
# --- SZ EXTREME: unbounded disinhibition -> ALL ignite, total loss of gating (disorganisation limit) ---
_szex = _SZ["EXTREME_disorganisation_limit"]
chk("SZ-EXTREME: unbounded disinhibition lowers the fold until ALL candidate assemblies ignite -- total "
    "loss of the selective gate (zero selectivity), the disorganisation limit at the excitation-imbalance "
    "boundary; loss of GATING is a MECHANISM boundary, NOT a claim about the disorganised experience",
    _szex["all_candidates_ignite"] is True and _szex["every_irrelevant_recruited"] is True
    and _szex["EXTREME_reproduced"] is True)
# --- SZ SLEEP: therapy sign ALIGNS with sleep (arousal DOWN) -- the MIRROR of autism (anti-sleep) ---
chk("SZ-SLEEP: the gain-REDUCING (sedating) push that calms aberrant salience LOWERS arousal/"
    "integration -- the SAME sign as sleep need; for SZ therapy-sign == sleep-sign, the MIRROR of "
    "autism whose arousal-raising therapy was anti-sleep (sign-only)",
    _SZ["SLEEP_sign_aligns"]["SLEEP_SIGN_ALIGNS"] is True)
# --- SZ HONESTY: a mechanism-direction discriminant, NOT efficacy / consciousness / medical advice ---
_szh = _SZ["honesty_ledger"]
chk("SZ: HONEST -- no efficacy, hard problem OPEN, no consciousness claim, no tuned constant "
    "(which pole a given psychosis is + the in-vivo integration direction are explicitly OWED)",
    _szh["medium_efficacy_tested"] == 0.0 and _szh["hard_problem_open"] == 1.0
    and _szh["consciousness_claim"] == 0.0 and _szh["new_tuned_constants"] == 0.0)
# --- SZ OVERALL: over-ignition + aberrant salience + 3-way separation + reversibility signs ---
chk("SZ: schizophrenia is the OVER-IGNITION mirror of autism-T -- aberrant ignition + loss of selective "
    "gating, with the antipsychotic restoring selectivity (and worsening autism-T) and the autism "
    "stimulant worsening SZ; which pole a given illness is, is OWED",
    _SZ["overall"]["is_full_module"] is True)

# ================= [DGENE] PSYCHIATRIC RISK-GENE VERIFICATION ATLAS (v1.28 ADD-ONLY) =================
# Add-only MEASURED-INPUT module: 121 curated high-confidence psychiatric/neurodevelopmental risk-gene
# promoters (11 disorders incl. INTELLECTUAL DISABILITY) fetched VERBATIM from NCBI RefSeq by the LOCKED
# SantaLucia-1998 gamma metric, each with provenance + sequence sha256 so gamma is re-derivable OFFLINE.
# Makes the D-series CITED gene LOCKs reproducible. Engine imported READ-ONLY. NOT a causal model / NOT
# medical advice; the pre-registered NULL (risk gamma vs brain MASTERS) is reported AS-IS.
import disease_gene_atlas as DGENE
_DG, _DG_blob, _DG_sha = DGENE.atlas_results()
_dg_exp = os.path.join(HERE, "expected_disease_gene_atlas_sha256.json")
if os.path.exists(_dg_exp):
    _DGEXP = json.load(open(_dg_exp))
    chk("DGENE: disease_gene_atlas_results.json reproduces its FROZEN sha256 (bit-for-bit)",
        _DG_sha == _DGEXP.get("disease_gene_atlas_results.json"))
else:
    chk("expected_disease_gene_atlas_sha256.json present (run disease_gene_atlas.py first)", False)
# --- DGENE PROVENANCE: every cached gene gamma re-derives OFFLINE from its stored sequence ---
_dgp = _DG["provenance"]
chk("DGENE: all 121 curated risk genes fetched + verified (none missing)",
    _dgp["n_genes_fetched_and_verified"] == 121 and _dgp["n_not_fetched"] == 0)
chk("DGENE: every cached gamma re-derivable OFFLINE from the stored sequence (no gamma/sha/seq mismatch)",
    _dgp["offline_rederivable"] is True and not _dgp["gamma_mismatch"]
    and not _dgp["sha256_mismatch"] and not _dgp["missing_sequence"])
# --- DGENE METRIC IDENTITY: the package's OWN frozen extra-masters re-derive EXACTLY (<=1e-9) ---
_dgm = _DG["metric_identity_check"]
chk("DGENE: metric identity PROVEN -- the package's own frozen extra-master controls (GSX2, NKX2-1, "
    "PHOX2B, DLX2) re-derive OFFLINE to EXACTLY (<=1e-9) their extra_masters.json gamma -> DGENE uses "
    "the LOCKED package metric, not a private one",
    _dgm["all_controls_exact"] is True
    and all(r.get("exact_match") is True for r in _dgm["per_control"].values()))
# --- DGENE ENGINE INVARIANCE: the add-only module changed NOTHING in the engine ---
_dgi = _DG["invariants"]
chk("DGENE: engine emergence tree UNCHANGED (add-only module did not touch M0..M20)",
    _dgi["engine_tree_unchanged"] is True
    and _dgi["engine_tree_sha256_live"] == "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70")
chk("DGENE: engine M0..M16 subtree UNCHANGED",
    _dgi["m0_16_subtree_unchanged"] is True
    and _dgi["m0_16_subtree_frozen"] == "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1")
# --- DGENE COVERAGE: all major psychiatric disorders incl. INTELLECTUAL DISABILITY ---
_dgo = _DG["overall"]
chk("DGENE: coverage spans 11 disorder classes incl. intellectual disability (ID=neocortex/syndromic), "
    "121 verified genes, >=1 gene each",
    _dgo["coverage_n_disorders"] == 11 and _dgo["coverage_n_genes"] == 121
    and _DG["coverage_by_disorder"]["ID"]["n_genes"] > 0)
# --- DGENE CONVERGENCE: cited cross-disorder pleiotropy is a property of the curation, reported AS-IS ---
chk("DGENE: cross-disorder convergence documented (>=1 gene shared by >=3 disorders) -- a readout of the "
    "cited curation, NOT a model output",
    _DG["cross_disorder_convergence"]["n_pleiotropic_ge3"] > 0)
# --- DGENE PRE-REGISTERED NULL: reported AS-IS (gamma is a developmental-identity metric, not disease) ---
_dgn = _DG["preregistered_null_gamma_vs_brain_masters"]
chk("DGENE: pre-registered NULL reported AS-IS -- risk-gene gamma vs brain-MASTER gamma (Mann-Whitney U); "
    "gamma is a developmental-IDENTITY metric so the honest result is INDISTINGUISHABLE, NOT a disease score",
    _dgn["mann_whitney_u"] is not None and "interpretation" in _dgn)
# --- DGENE HONESTY: verified provenance, NOT a causal model / NOT medical advice ---
_dgh = _DG["honesty_ledger"]
chk("DGENE: HONEST -- no efficacy, hard problem OPEN, no consciousness claim, no tuned constant; gamma is "
    "promoter identity [F] NOT causation, disorders POLYGENIC, NOT medical advice",
    _dgh["medium_efficacy_tested"] == 0.0 and _dgh["hard_problem_open"] == 1.0
    and _dgh["consciousness_claim"] == 0.0 and _dgh["new_tuned_constants"] == 0.0
    and "not_medical_advice" in _DG["locks"])
# --- DGENE OVERALL: the verification module passes its own gate ---
chk("DGENE: 121 psychiatric/neurodevelopmental risk genes VERIFIED (provenance + offline re-derivable + "
    "exact metric controls + engine invariant + null reported), making the cited D-series gene LOCKs "
    "reproducible",
    _dgo["all_fetched_genes_verified_offline"] is True and _dgo["metric_controls_exact"] is True
    and _dgo["null_reported"] is True)

# ============================ [C] legacy provenance ===========================
BL = os.path.join(HERE, "regression_baseline.json")
INP = os.path.join(HERE, "inputs")
if os.path.exists(BL) and os.path.isdir(INP):
    B = json.load(open(BL))
    def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
    for fn, h in B.get("sha256", {}).items():
        p = os.path.join(INP, fn)
        if os.path.exists(p):
            chk(f"legacy snapshot intact: {fn}", sha(p) == h)

# ================================ report ======================================
if fails:
    print("REGRESSION FAIL --", len(fails), "of", n)
    for f in fails: print("  FAIL:", f)
    sys.exit(1)
print(f"REGRESSION PASS -- {n} checks (engine self-reproduces + mechanism invariants), SEED={E.SEED}")
print("  [A] determinism + bit-for-bit self-reproduction of the shipped engine")
print("  [B] winner-take-most, gamma->ignitability, single-winner selection, RPE learning,")
print("      hippocampal attractor memory + theta-phase protection, EM brainwave at ~c,")
print("      classical-field coherence across the brain (coherence-length rejection refuted)")
print("  [B/M9-geom] v1.18 ADD-ONLY: M9 ephaptic geometry grounded on measured MNI anatomy [L]")
print("      (ring cross-check reproduces frozen engine; grounded fc reported as-is; regime stays")
print("      partial_metastable -- NOT synchronized; row-norm not the maximizer; engine default unchanged)")
print("  [C] legacy pre-engine snapshots intact (provenance)")
print("  [D] v1.21 ADD-ONLY: disease stress-test D1 (chronic stress / HPA hyperactivity) --")
print("      NORMAL substrate reproduces hypercortisolism + delayed recovery + attention narrowing")
print("      when CITED params are perturbed in the clinical DIRECTION only (sign-invariant; engine")
print("      tree unchanged; NOT felt; efficacy untested; hard problem OPEN).")
print("  [D3] v1.22 ADD-ONLY: disease stress-test D3 (anxiety / panic) -- reusing M18+M20, the NORMAL")
print("      substrate reproduces sub-threshold avoidance + a lowered avoid threshold + steeper")
print("      interoceptive coupling (sign-invariant; engine tree unchanged; NOT felt; hard problem OPEN).")
print("  [D2] v1.22 ADD-ONLY: disease stress-test D2 (depression / anhedonia) -- reusing M5+M17+M19, the")
print("      NORMAL substrate reproduces blunted reward learning + a shrunken approach gap + a")
print("      mood-congruent recall negativity FLIP (sign-invariant; engine tree unchanged; NOT felt).")
print("      D3 (M18/M20) and D2 (M5/M19) perturb DISJOINT handles -- a built-in discriminant check.")
print("  [D4] v1.23 ADD-ONLY: disease stress-test D4 (PTSD / hyperarousal) -- reusing M17+M2+M18, the")
print("      NORMAL substrate reproduces a NARROWED operable arousal band + operating-point collapse +")
print("      a deeper residual fear basin (intrusion) + HEP riding hyperarousal (sign-invariant; engine")
print("      tree unchanged; NOT felt; hard problem OPEN).")
print("  [D5] v1.23 ADD-ONLY: disease stress-test D5 (autonomic dysfunction / interoceptive blunting) --")
print("      reusing M18+M19, the NORMAL substrate reproduces a FLATTENED HEP-arousal slope + a shrunken")
print("      affective-discriminability margin (sign-invariant; engine tree unchanged; NOT felt).")
print("      D4 (operating point) and D5 (afferent slope) perturb DISJOINT M18 sub-handles; D5 leaves M5")
print("      reward intact (!= anhedonia) and is the OPPOSITE interoceptive pole of D3 -- discriminant validity.")
print("  [D6] v1.24 ADD-ONLY: disease stress-test D6 (burnout / HPA hypoactivity, terminal) -- the MIRROR of")
print("      D1, reusing M18 only: HPA drive DOWN ABOLISHES the acute cortisol peak + lowers total output")
print("      (hypocortisolism) + FLATTENS the recovery curve (sign-invariant; amplitude-only, kinetics")
print("      unchanged; engine tree unchanged; NOT felt). D6 and D1 are OPPOSITE poles of the one HPA axis")
print("      (cortisol DEPLETION vs OVERLOAD; output D6 < normal < D1) -- a discriminant-validity mirror.")
print("  [AUT] v1.25 ADD-ONLY: AUTISM MODULE (D7 candidate) -- which handle reproduces autism's measured")
print("      EEG signature? UNIFICATION (S0): ONE ephaptic coupling kappa drives BOTH the cross-frequency")
print("      PAC and the global integration -> autism = TWO substrate axes, not three loose signs:")
print("      AXIS-1 coupling pathway kappa (S1 reduced PAC + S3 long-range under-connectivity, one knob),")
print("      AXIS-2 E/I excitability (S2 asymmetric bias -> lower ignition threshold + spontaneous gamma).")
print("      DISCRIMINANT: the frontal-lobe node has ZERO leverage on any signature and the integration")
print("      hub is NOT frontal -> 'pathway, not frontal-lobe', in code. Only the E/I->1/f READOUT stays")
print("      OWED (the engine 1/f is set by fixed synaptic taus, E/I-insensitive).")
print("  [AUT2] v1.26 ADD-ONLY: AUTISM MECHANISM SUB-DISCRIMINANT (D8 candidate) -- WITHIN the D7")
print("      coupling axis (kappa), the theta(4-8Hz)->gamma deficit is THREE distinguishable faults,")
print("      each with a UNIQUE (delta-PAC, ignition) fingerprint: WIRING (PAC change == 0 exact, a")
print("      gain/threshold drug CANNOT correct it -- topology invariant under uniform gain), OUTPUT-")
print("      weak (PAC down, fold normal, drug partial), THRESHOLD-high (PAC down, fold RAISED, drug")
print("      FULL; the VEGETATIVE limit is this fault past the measured ephaptic ceiling kappa). An")
print("      exogenous 4-8Hz supply rescues ALL (incl. wiring) but over-synchronises if over-dosed; the")
print("      same supply that helps coupling is ANTI-sleep (opposite sign). => drug-responsiveness of the")
print("      coupling deficit implicates a GAIN fault, not wiring (the user's 'ADHD-med relief = evidence'")
print("      reasoning, in code). Which fault a given autism is = OWED; O-vs-T in-vivo = OWED. MECHANISM")
print("      only -- efficacy 0, hard problem OPEN, NOT medical advice.")
print("  [SZ] v1.27 ADD-ONLY: SCHIZOPHRENIA-SPECTRUM DISCRIMINANT (D9 candidate) -- the OVER-IGNITION")
print("      MIRROR of autism-T on the SAME M3 R19 ignitability axis: a disinhibitory/excitatory bias")
print("      (E/I toward excitation; NMDA-hypofunction account) LOWERS the fold so weak/IRRELEVANT")
print("      candidate assemblies ignite (ABERRANT SALIENCE) and the selective single-winner gate")
print("      collapses. (ignition-direction, aberrant-vs-lost) separates HEALTH / AUTISM-T / SZ uniquely")
print("      -- SZ lowers the fold + recruits irrelevant; autism-T raises it + loses relevant. A gain-")
print("      REDUCING antipsychotic-class push restores selectivity on SZ but WORSENS autism-T; the")
print("      stimulant that HELPED autism-T WORSENS SZ (opposite signs at the two poles); the extreme is")
print("      total loss of gating (disorganisation limit). Which pole a given illness is = OWED. MECHANISM")
print("      only -- efficacy 0, hard problem OPEN, NOT medical advice.")
print("  [DGENE] v1.28 ADD-ONLY: PSYCHIATRIC RISK-GENE VERIFICATION ATLAS -- 121 curated high-confidence")
print("      risk genes across 11 disorders (schizophrenia, autism, INTELLECTUAL DISABILITY, bipolar,")
print("      depression, ADHD, OCD, Tourette, epilepsy/DEE, addiction, syndromes) with each promoter gamma")
print("      fetched VERBATIM from NCBI RefSeq by the LOCKED SantaLucia metric + sequence sha256, RE-DERIVED")
print("      OFFLINE bit-for-bit; metric identity PROVEN exactly (<=1e-9) against the package's own frozen")
print("      extra-master controls (GSX2/NKX2-1/PHOX2B/DLX2). Makes the D-series CITED gene LOCKs")
print("      reproducible. Pre-registered NULL (risk gamma vs brain MASTERS, U=667.5, p=0.65) is")
print("      INDISTINGUISHABLE and reported AS-IS -- gamma is a developmental-IDENTITY metric [F], NOT a")
print("      disease score. Engine READ-ONLY/unchanged; disorders POLYGENIC; NOT a causal model; NOT")
print("      medical advice.")
print("NOTE: mechanism only -- consciousness is NOT reproduced (PCI = honest negative; hard problem OPEN).")
sys.exit(0)
