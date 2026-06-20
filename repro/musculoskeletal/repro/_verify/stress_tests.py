#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stress_tests.py  --  Musculoskeletal STRESS BATTERY (load-bearing / solid-mechanics class).

Very high bar: each discriminant target (CHARTER T1..T5) is a MECHANISM that emerges from the shared
jamming substrate (R19 bistable switch + FitzHugh-Nagumo recovery) driven only by CITED rate/geometry
anchors -- no per-target tuning, the SHAPE is emergent and swept WIDE. Failures are honest; an [O] grade
with a stated obstacle is acceptable, a silent pass is not. Writing stays LOCKED until run_battery() is
all PASS and gates.write_research_complete() has signed off (see gates.py / CHARTER.md).

  T1 force-frequency : twitch summation -> fused tetanus at a cited stimulation frequency; fusion tracks 1/tau.
  T2 length-tension  : active force = thin/thick filament OVERLAP (load-bearing contact number) -> cited peak.
  T3 Wolff remodel   : sustained supra-threshold load flips bone density past the R19 yield threshold + HYSTERESIS.
  T4 growth-plate    : developmental THRESHOLD order = gamma-rank over the measured patterning/diff. masters.
  T5 fatigue         : sustained drive -> reversible exponential force decline with a cited time constant.
"""
import os, sys, json
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_disease"))
import importlib
eng = importlib.import_module("vp_msk_engine")
dyn = importlib.import_module("vp_msk_dynamics")
dis = importlib.import_module("vp_msk_disease")
trx = importlib.import_module("vp_msk_treatment")
anlg = importlib.import_module("vp_msk_analgesia")

def _organ_gammas():
    """Read MEASURED organ gamma off the emergence engine (vendored from DNA; never fitted here)."""
    base = eng.emerge_organs()
    g = {o["organ"]: o["gamma"] for o in base["organs"] if o.get("gamma") is not None}
    return g, base

def run_battery():
    dyn.seed_everything()
    g, base = _organ_gammas()

    t1 = dyn.t1_force_frequency()
    t2 = dyn.t2_length_tension()
    t3 = dyn.t3_wolff(g["bone"])
    t4 = dyn.t4_growth_plate(g)
    t5 = dyn.t5_fatigue()

    suites = [
        {"target": "T1",
         "description": "twitch summation -> fused tetanus at a cited stimulation frequency; fusion frequency tracks 1/tau across fast<->slow fibres",
         "status": t1["status"],
         "value": {"fusion_freq_hz": t1["fusion_freq_hz"], "fusion_band_hz": t1["anchor_fusion_band_hz"],
                   "fusion_tracking": t1["fusion_freq_tracks_inverse_tau"]},
         "grade": t1["grade"],
         "obstacle_if_open": "tetanus:twitch AMPLITUDE ratio is uncalibrated: linear twitch superposition has no "
                             "contractile force ceiling, and a bounded ratio requires Ca2+/cross-bridge "
                             "activation-saturation kinetics whose half-activation constant the jamming substrate "
                             "does not fix; tuning it to the cited ~3-5 would violate No-Tuning.",
         "detail": t1},
        {"target": "T2",
         "description": "active force proportional to thin/thick filament overlap (the load-bearing contact number) reproduces the cited length-tension peak + zero-overlap intercept",
         "status": t2["status"],
         "value": {"plateau_um": t2["plateau_um"], "plateau_band_um": t2["anchor_plateau_band_um"],
                   "zero_force_um": t2["zero_force_um"], "anchor_zero_um": t2["anchor_zero_um"]},
         "grade": t2["grade"],
         "obstacle_if_open": None,
         "detail": t2},
        {"target": "T3",
         "description": "sustained supra-threshold mechanical load flips bone density past the R19 yield threshold (Wolff's law); the load loop shows hysteresis = bone memory",
         "status": t3["status"],
         "value": {"yield_threshold_spinodal": t3["yield_threshold_spinodal"], "crossing_load": t3["crossing_load"],
                   "max_density_jump": t3["max_density_jump"], "hysteresis_area": t3["hysteresis_area"],
                   "sub_threshold_density": t3["sub_threshold_density"], "supra_threshold_density": t3["supra_threshold_density"]},
         "grade": t3["grade"],
         "obstacle_if_open": "absolute bone mineral density (g/cm^3) is not fixed by the substrate -> [O]; the "
                             "threshold, near-discontinuous jump and hysteresis are forced, the setpoint is cited (Frost).",
         "detail": t3},
        {"target": "T4",
         "description": "developmental THRESHOLD order = gamma-rank: functional spinodal monotone in gamma reproduces limb -> cartilage -> muscle over the measured masters",
         "status": t4["status"],
         "value": {"gamma_threshold_order_ascending": t4["gamma_threshold_order_ascending"],
                   "patterning_subsequence": t4["patterning_subsequence"], "cited_sequence": t4["cited_sequence"],
                   "sequence_reproduced": t4["sequence_reproduced"], "bone_threshold_rank_index": t4["bone_threshold_rank_index"]},
         "grade": t4["grade"],
         "obstacle_if_open": "absolute endochondral OSSIFICATION timing is drive(STATE)-gated, not gamma-timed -> [O]; "
                             "RUNX2's low measured gamma ranks bone's switching THRESHOLD early (consistent with early "
                             "osteochondroprogenitor RUNX2), but ossification waits on the cartilage template ('parts present != trait').",
         "detail": t4},
        {"target": "T5",
         "description": "sustained maximal drive loads a slow adaptation variable -> monotone exponential force decline to a plateau, fully reversible on rest; time constant in the cited band",
         "status": t5["status"],
         "value": {"force_drop_frac": t5["force_drop_frac"], "tau_recovered_s": t5["tau_recovered_s"],
                   "anchor_band_s": t5["anchor_band_s"], "recovered_frac": t5["recovered_frac"]},
         "grade": t5["grade"],
         "obstacle_if_open": "absolute force-loss MAGNITUDE (depth of the decline) is not fixed by the substrate -> [O]; "
                             "the reversible exponential SHAPE is verified and the time constant is cited (Bigland-Ritchie).",
         "detail": t5},
    ]

    results = {
        "emergence_ok": bool(base["organs"]),
        "oscillators_ok": None,  # this class has no oscillator organs (load-bearing, not rhythmic)
        "deferred_gamma": base.get("deferred_gamma", []),
        "organ_gammas": {k: round(v, 6) for k, v in sorted(g.items())},
        "suites": suites,
    }
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in suites)
    return results


# ---------------------------------------------------------------------------
# DISEASE BATTERY  --  cited-severity perturbations of the passing physiology
# targets (T1..T5) and the four master switches. Same PASS/value/grade/obstacle
# schema as run_battery(); PASS = reproduce the DIRECTION/SHAPE of the documented
# clinical sign, never an absolute number (No-Tuning). See _disease/vp_msk_disease.py.
# ---------------------------------------------------------------------------

# Per-target whitelist of headline diagnostic fields to surface as `value`
# (intersected with the keys actually present, so a schema change can never KeyError).
_DISEASE_VALUE_KEYS = {
    "T7a": ["master", "gamma", "wt_occupancy", "het_occupancy", "het_crosses", "critical_dosage_cliff"],
    "T7b": ["master", "gamma", "wt_occupancy", "het_occupancy", "het_crosses", "critical_dosage_cliff"],
    "T7c": ["master", "gamma", "wt_occupancy", "het_occupancy", "het_crosses", "critical_dosage_cliff"],
    "T7d": ["master", "gamma", "wt_occupancy", "het_occupancy", "het_crosses", "critical_dosage_cliff"],
    "T6":  ["spinodal", "loss_rate_rises_with_disuse", "density_falls_with_disuse",
            "maintenance_is_baseline", "catastrophic_past_spinodal"],
    "T6b": ["unloaded_density_normal", "unloaded_density_osteopetrosis", "down_branch_removed"],
    "T8":  ["test_freq_hz", "decrement_pct_normal", "decrement_pct_mg", "clinical_threshold_pct",
            "decrement_monotone_in_lesion"],
    "T8b": ["test_freq_hz", "increment_pct_high_freq", "decrement_pct_high_freq", "increment_monotone_in_freq"],
    "T10": ["tau_fit_normal_s", "tau_fit_metabolic_s", "recovered_frac_normal", "recovered_frac_metabolic",
            "faster_than_normal", "incomplete_recovery", "recovery_monotone_in_residual"],
    "T9":  ["sub_threshold_protected", "loss_accelerates_with_load", "progressive_at_overload", "convex_in_load"],
    "T4-ext": ["gamma_SOX9", "wt_full_output", "achondroplasia_shortened", "graded_shortening"],
    "T11": ["retained_normal", "retained_bmd", "retained_dmd", "ordering_normal_gt_bmd_gt_dmd",
            "dmd_progressive", "retained_monotone_in_dystrophin"],
    "T12": ["block_threshold_normal", "block_threshold_myotonia", "block_threshold_paralysis",
            "myotonia_resists_block", "paralysis_blocks_early", "opposite_excitability_signs",
            "block_threshold_monotone_in_beta"],
    "T13": ["single_event_yield_spinodal", "sub_endurance_protected", "supra_endurance_fractures",
            "monotone_in_cycles", "fracture_heals_under_load"],
    "T14": ["sub_threshold_protected", "loss_accelerates_with_overuse", "convex_in_load"],
    "T15": ["max_force_monotone_down", "fatigue_tau_monotone_down", "multi_axis"],
    "T16": ["density_monotone_in_supply", "normal_fully_mineralizes", "deficient_density_capped",
            "osteoporotic_matrix_rescued_by_load", "osteomalacic_load_cannot_rescue", "load_contrast_holds"],
    "T17": ["normal_forms_under_load", "myeloma_stays_lytic", "gct_aggressive_osteolysis", "mirror_of_osteopetrosis"],
}


def _obstacle_from_grade(grade):
    """Extract the open-grade obstacle clause: the ';'-separated segment that carries [O]."""
    for seg in str(grade).split(";"):
        if "[O]" in seg:
            return seg.strip()
    return None


def run_disease_suite():
    """Reshape the disease battery into the kit-standard suite schema for gate + docs consumption."""
    dyn.seed_everything()
    batt = dis.run_disease_battery()
    suites = []
    for t in batt["targets"]:
        tid = t["target"]
        keys = _DISEASE_VALUE_KEYS.get(tid, [])
        value = {k: t[k] for k in keys if k in t}
        suites.append({
            "target": tid,
            "disease": t.get("disease"),
            "perturbs": t.get("perturbs"),
            "secondary": t.get("secondary", tid == "T7d"),
            "description": t.get("signature"),
            "status": t["status"],
            "value": value,
            "grade": t.get("grade"),
            "cited_severity": t.get("cited_severity"),
            "anchor": t.get("anchor"),
            "obstacle_if_open": _obstacle_from_grade(t.get("grade")),
            "detail": t,
        })
    # Hard gate excludes the secondary T7d (rare/recent MYOD1 human disease -> [V?]); it still reports PASS.
    hard = [s for s in suites if not s["secondary"]]
    return {
        "kernel": batt["_kernel"],
        "suites": suites,
        "t7d_secondary_status": batt.get("t7d_secondary_status"),
        "grade_summary": batt.get("grade_summary"),
        "all_disease_targets_pass": all(s["status"] == "PASS" for s in hard),
    }


def run_treatment_suite():
    """Reshape the TREATMENT battery (the mirror of the disease battery) into the kit-standard suite schema.
    A reversible (mirror) treatment PASSes by restoring the disease SIGNATURE back toward the healthy attractor
    (DIRECTION, No-Tuning). Honest PARTIAL / OPEN entries (developmental dosage cliffs, no cartilage regen,
    established-tumour cytotoxic therapy, etiology-specific metabolic myopathy) are LOGGED, never silently
    dropped, and are excluded from the hard gate -- exactly the T7d-secondary policy."""
    dyn.seed_everything()
    batt = trx.run_treatment_battery()
    suites = []
    for t in batt["treatments"]:
        suites.append({
            "target": t["target"],
            "disease": t.get("disease"),
            "treatment": t.get("treatment"),
            "mirror_of": t.get("mirror_of"),
            "kernel_action": t.get("kernel_action"),
            "moa": t.get("moa"),
            "status": t["status"],
            "honest_open_or_partial": t["status"] in ("OPEN", "PARTIAL"),
            "grade": t.get("grade"),
            "detail": t,
        })
    return {
        "kernel": batt["_kernel"],
        "suites": suites,
        "grade_summary": batt.get("grade_summary"),
        "honest_open_or_partial": batt.get("honest_open_or_partial"),
        "all_reversible_treatments_restore": batt.get("all_reversible_treatments_restore"),
    }


def run_analgesia_suite():
    """Reshape the ANALGESIC battery (the three-lever threshold logic applied to owned painful diseases) into the
    kit-standard suite schema. An in-scope lever PASSes by lowering the nociceptive crossing rate by DIRECTION
    (No-Tuning), with the L2-coupled / L1-decoupled lesion cross-check holding where a structural lesion term
    exists. Honest PARTIAL / OPEN entries (exertional muscle pain has no discrete contact-loss lesion to
    cross-check) are LOGGED, never silently dropped, and excluded from the hard gate -- exactly the T7d policy."""
    dyn.seed_everything()
    batt = anlg.run_analgesic_battery()
    suites = []
    for e in batt["analgesia_entries"]:
        lm = e["lever_map"]
        suites.append({
            "target": e["target"],
            "disease": e.get("disease"),
            "mirror_of": e.get("mirror_of"),
            "L1_agent": e.get("L1_agent"), "L2_agent": e.get("L2_agent"), "L3_seam_agent": e.get("L3_seam_agent"),
            "L1_lowers": lm["L1"]["lowers_nociception"], "L2_lowers": lm["L2"]["lowers_nociception"],
            "L3_lowers": lm["L3"]["lowers_nociception"],
            "L2_structure_coupled": e.get("L2_structure_coupled"),
            "L1_structure_decoupled": e.get("L1_structure_decoupled"),
            "convergence": e.get("convergence"),
            "status": e["status"],
            "honest_open_or_partial": e["status"] in ("OPEN", "PARTIAL") or e["target"] in
                                      [h["target"] for h in batt["honest_open_or_partial"]],
            "grade": e.get("grade"),
            "detail": e,
        })
    return {
        "kernel": batt["_kernel"],
        "scope": batt["scope"],
        "suites": suites,
        "grade_summary": batt.get("grade_summary"),
        "honest_open_or_partial": batt.get("honest_open_or_partial"),
        "all_inscope_levers_direction_ok": batt.get("all_inscope_levers_direction_ok"),
        "source_doi": anlg.AL.ANALGESIC_SOURCE_DOI,
    }


if __name__ == "__main__":
    r = run_battery()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nALL PHYSIOLOGY TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
    d = run_disease_suite()
    print("\n" + "=" * 70 + "\nDISEASE BATTERY\n" + "=" * 70)
    print(json.dumps(d, ensure_ascii=False, indent=2))
    print("\nALL DISEASE TARGETS PASS:", d["all_disease_targets_pass"], "(writing stays locked until True)")
    tt = run_treatment_suite()
    print("\n" + "=" * 70 + "\nTREATMENT BATTERY\n" + "=" * 70)
    print(json.dumps(tt, ensure_ascii=False, indent=2))
    print("\nALL REVERSIBLE TREATMENTS RESTORE:", tt["all_reversible_treatments_restore"])
