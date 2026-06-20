#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stress_tests.py  --  Hemodynamic Homeostasis STRESS BATTERY (v0.2.0-research).

Each target is now COMPUTED from the in-package modules and PASSES only on a real, stated
discriminant -- never a silent pass. Very high bar: swept WIDE, no per-target tuning, failures honest,
[O]+obstacle acceptable. Writing stays LOCKED until run_battery()["all_targets_pass"] is True and
gates.write_research_complete() is called.

Suites:
  RP1-RP5  closed setpoint loops (vp_hmd_loops): MAP from seams; baroreflex buffering + PIEZO-KO;
           kidney integral controller (perfect adaptation); hypertension setpoint reset (opposed back);
           HF basin collapse (saddle-node fold).
  S1-S2    sensory transduction (baroreceptor PIEZO monotone + KO-flat; macula-densa NKCC2 renin-down /
           TGF-up + SGLT2i restores TGF).
  T1-T2    fundamental-vs-symptomatic therapy (reference-reset durable vs operating-point opposed back;
           HF inotrope shrinks margin vs load-reduce+cycle-break grows margin).

Grades per suite: reproduced loop/curve SHAPE or DIRECTION = [V]; cited identity / gain / mortality = [L];
ABSOLUTE scales (pressure in mmHg, incidence, firing Hz, GFR, effect sizes) = [O] with a stated obstacle.
"""
import os, sys, json
_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "_sensory"))
sys.path.insert(0, os.path.join(_HERE, "..", "_therapy"))
sys.path.insert(0, os.path.join(_HERE, "..", "_pathology"))
sys.path.insert(0, os.path.join(_HERE, "..", "_comparative"))
sys.path.insert(0, os.path.join(_HERE, "..", "_calibration"))
sys.path.insert(0, os.path.join(_HERE, "..", "_intervention"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
import importlib
eng = importlib.import_module("vp_hmd_engine")
LOOPS = importlib.import_module("vp_hmd_loops")
BARO = importlib.import_module("baroreceptor")
MD = importlib.import_module("macula_densa")
RX = importlib.import_module("fundamental_targets")
HYPO = importlib.import_module("hypotension_family")
COMP = importlib.import_module("setpoint_emergence")
CAL = importlib.import_module("scale_calibration")
IV = importlib.import_module("intervention_logic")
IVSCAN = importlib.import_module("forbidden_claim_scan")
IVHON = importlib.import_module("counterreg_honesty")
IVFALS = importlib.import_module("falsification")
IVPRIO = importlib.import_module("burden_prioritisation")

_OBST = "absolute scale needs external calibration (clinical units / cohort incidence); model fixes SHAPE/DIRECTION only"


def _suite(tid, desc, passed, value, grade, obstacle=None):
    return {"target": tid, "description": desc, "status": "PASS" if passed else "FAIL",
            "value": value, "grade": grade, "obstacle_if_open": obstacle}


# ---- RP1-RP5: closed loops ------------------------------------------------
def rp1():
    r = LOOPS.rp1_map_product()
    ok = (abs(r["abs_err_mmHg"]) < 1e-6) and (r["owned_by_single_organ"] is False)
    return _suite("RP1", "MAP = CVP + CO x SVR reproduces resting ~93 mmHg from the seam variables; owned by no single organ",
                  ok, {"MAP_mmHg": r["MAP_mmHg"], "abs_err_mmHg": r["abs_err_mmHg"]}, "[V] relation / [L] numeric / [O] absolute", _OBST)

def rp2():
    r = LOOPS.rp2_baroreflex()
    ok = (r["intact"]["buffered_fraction"] >= 0.70) and r["ko_is_labile"]
    return _suite("RP2", "baroreflex buffers the majority of a pressure step (G=3 -> 75%); PIEZO double-KO is labile (no buffering)",
                  ok, {"buffered_fraction": r["intact"]["buffered_fraction"], "ko_buffered": r["piezo_double_ko"]["buffered_fraction"]},
                  "[V] shape / [L] gain+latency / [O] absolute", _OBST)

def rp3():
    r = LOOPS.rp3_pressure_natriuresis()
    ok = (r["load_independent_spread_mmHg"] < 1e-6) and r["perfect_adaptation"]
    return _suite("RP3", "pressure-natriuresis integral controller: transient salt/volume loads correct to the SAME setpoint (perfect adaptation, Guyton infinite gain)",
                  ok, {"spread_mmHg": r["load_independent_spread_mmHg"], "setpoint": r["setpoint"]},
                  "[V] shape / [L] anchor / [O] absolute setpoint", _OBST)

def rp4():
    r = LOOPS.rp4_setpoint_reset()
    ok = r["attractor_moved_up"] and (r["reset_shift_mmHg"] > 5.0) and r["opposed_back"]
    return _suite("RP4", "hypertension = setpoint RESET: defended pressure moves UP (attractor-shift); an operating-point drug is opposed back to the reset reference",
                  ok, {"reset_shift_mmHg": r["reset_shift_mmHg"], "drug_steady_mmHg": r["drug_steady_mmHg"], "opposed_back": r["opposed_back"]},
                  "[V] shape / [L] risk anchor / [O] absolute incidence", _OBST)

def rp5():
    r = LOOPS.rp5_basin_collapse()
    # discriminant: a high-output basin exists at high kappa and ANNIHILATES (fold) at low kappa
    states = r["sweep_kappa_high_to_low"]
    had_basin = any(s["high_output_basin"] for s in states)
    lost_basin = any(not s["high_output_basin"] for s in states)
    ok = had_basin and lost_basin and bool(r.get("is_fold_not_reset", lost_basin))
    return _suite("RP5", "heart failure = basin COLLAPSE: as contractility kappa falls at fixed load, the high-output basin annihilates in a saddle-node fold (distinct from a reset)",
                  ok, {"collapse_kappa": r.get("collapse_kappa"), "had_basin": had_basin, "lost_basin": lost_basin},
                  "[V] fold / [L] markers / [O] absolute", _OBST)

# ---- S1-S2: sensory transduction -----------------------------------------
def s1():
    r = BARO.status()
    ok = r["intact_pressure_sensitive"] and r["ko_flat_no_afferent"] and bool(r["substrate_spikes"]["spikes"] > 0)
    return _suite("S1", "baroreceptor PIEZO1/2 mechanosensor: intact firing is monotone in pressure; double-KO is flat (no afferent); afferent firing is a shared-R19 spike train",
                  ok, {"intact_monotone": r["intact_pressure_sensitive"], "ko_flat": r["ko_flat_no_afferent"], "r19_spikes": r["substrate_spikes"]["spikes"]},
                  "[V] curve / [L] molecular identity / [O] absolute Hz", _OBST)

def s2():
    r = MD.status()
    mono = r["both_transductions_monotone"]
    sglt = r["sglt2i"]
    tgf_up = bool(sglt["tgf_on_sglt2i"] > sglt["tgf_baseline"])
    ok = bool(mono) and tgf_up
    return _suite("S2", "macula-densa NKCC2 NaCl chemosensor: renin DECREASES and TGF INCREASES with luminal NaCl (both monotone); SGLT2i raises delivered NaCl -> restores TGF",
                  ok, {"both_monotone": mono, "tgf_baseline": sglt["tgf_baseline"], "tgf_on_sglt2i": sglt["tgf_on_sglt2i"]},
                  "[V] shape / [L] identity / [O] absolute", _OBST)

# ---- T1-T2: fundamental-vs-symptomatic therapy ---------------------------
def t1():
    r = RX.hypertension_therapies()
    ok = r["operating_point_drug"]["opposed_back"] and r["reference_reset"]["durable"] \
         and (r["reference_reset"]["durable_drop_mmHg"] > r["operating_point_drug"]["durable_drop_mmHg"])
    return _suite("T1", "hypertension therapy: an operating-point drug is opposed back (not durable) while a renal REFERENCE reset durably lowers the defended pressure",
                  ok, {"op_durable_drop": r["operating_point_drug"]["durable_drop_mmHg"], "reset_durable_drop": r["reference_reset"]["durable_drop_mmHg"]},
                  "[V] direction / [L] clinical durability / [O] absolute effect", _OBST)

def t2():
    r = RX.heart_failure_therapies()
    ok = r["inotrope_flog"]["margin_shrinks"] and r["load_reduce_cycle_break"]["margin_grows"] \
         and (r["load_reduce_cycle_break"]["d_margin"] > 0.0 > r["inotrope_flog"]["d_margin"])
    return _suite("T2", "heart-failure therapy: effector-flog (inotrope) SHRINKS the barrier margin (accelerated collapse) while load-reduce + cycle-break GROWS it (basin restored)",
                  ok, {"inotrope_d_margin": r["inotrope_flog"]["d_margin"], "blockade_d_margin": r["load_reduce_cycle_break"]["d_margin"]},
                  "[V] direction / [L] clinical mortality / [O] absolute", _OBST)



# ---- RP6-RP9: hypotension as a NODE DECOMPOSITION ------------------------
def rp6():
    r = HYPO.rp6_orthostatic()
    ok = r["intact_buffers_majority"] and r["autonomic_failure_is_orthostatic"]
    return _suite("RP6", "orthostatic/autonomic hypotension: intact baroreflex buffers a downward postural step; autonomic failure (PIEZO-KO) passes the full drop (orthostatic) -- symmetric with RP2",
                  ok, {"intact_buffered": r["intact_buffered_fraction"], "failed_buffered": r["failed_buffered_fraction"]},
                  "[V] shape / [L] gain+latency / [O] absolute", _OBST)

def rp7():
    r = HYPO.rp7_adrenal_reference_loss()
    ok = r["attractor_moved_down"] and r["bolus_opposed_back"] and r["reference_restore_durable"]
    return _suite("RP7", "adrenal insufficiency: the renal reference resets DOWN (lost RAAS set-point); a fluid bolus is opposed back to the low reference while restoring the reference (mineralocorticoid) is durable -- mirror of RP4/T1",
                  ok, {"reset_shift_mmHg": r["reset_shift_mmHg"], "bolus_steady": r["bolus_steady_mmHg"]},
                  "[V] shape / [L] clinical / [O] absolute", _OBST)

def rp8():
    r = HYPO.rp8_distributive_svr_collapse()
    ok = (r["vasoplegia_floor_svr"] is not None) and r["vasopressor_beats_inotrope"]
    return _suite("RP8", "distributive/vasoplegic shock: SVR effector collapse drops MAP below the perfusion floor even with doubled CO; a vasopressor (restore SVR) beats inotrope-only -- distinct from the RP5 cardiac arm",
                  ok, {"floor_svr": r["vasoplegia_floor_svr"], "MAP_inotrope": r["MAP_inotrope_only"], "MAP_pressor": r["MAP_vasopressor"]},
                  "[V] shape / [L] clinical / [O] absolute", _OBST)

def rp9():
    r = HYPO.rp9_hypovolemic_substrate_fold()
    ok = r["excess_self_corrects"] and r["deficit_is_uncorrected_fold"] and r["transfusion_restores"]
    return _suite("RP9", "hypovolemic shock: renal natriuresis is excrete-only, so a volume EXCESS self-corrects (RP3) but a volume DEFICIT is a substrate fold the kidney cannot self-correct -- only transfusion restores it",
                  ok, {"P_excess": r["steady_P_after_excess"], "P_deficit": r["steady_P_after_deficit"], "P_transfused": r["steady_P_after_transfusion"]},
                  "[V] shape / [L] clinical / [O] absolute", _OBST)

# ---- C1: cross-organism setpoint emergence (universality) -----------------
def c1():
    r = COMP.setpoint_emergence()
    ok = r["qualitative_jump_ordered"] and r["defended_requires_all_three"]
    return _suite("C1", "universality: a defended pressure setpoint EMERGES by loop accretion -- incidental (open systems) -> error-regulated (single-circuit fast reflex) -> defended (closed + effector + integrator); the defended regime requires all three legs simultaneously",
                  ok, {"jump_ordered": r["qualitative_jump_ordered"], "requires_all_three": r["defended_requires_all_three"]},
                  "[V] emergence shape / [L] phylogeny / [O] absolute per taxon", _OBST)


# ---- CAL1-CAL7: absolute-scale calibration (anchor + propagate + cross-check)
# Each CAL closes a declared absolute-scale [O] item by [CAL] (cited anchor ->
# locked [V] relation -> independent cross-check with a COMPUTED discriminant).
# First-principles derivation stays [O]; residual-open items are NOT forced.
def _cal_suite(r):
    rid = r["id"]
    res = r.get("residual_open", [])
    obst = ("first-principles absolute scale stays [O]"
            + ("; residual-open: " + "; ".join(res) if res else ""))
    return _suite(rid, r["title"], bool(r["passed"]),
                  {k: r[k] for k in ("propagated", "independent_check") if k in r},
                  r["grade"], obst)

def cal1(): return _cal_suite(CAL.cal1_pressure_scale())
def cal2(): return _cal_suite(CAL.cal2_baroreflex_gain())
def cal3(): return _cal_suite(CAL.cal3_baroreceptor_hz())
def cal4(): return _cal_suite(CAL.cal4_macula_densa_scale())
def cal5(): return _cal_suite(CAL.cal5_hypertension_reset_clinical())
def cal6(): return _cal_suite(CAL.cal6_therapy_effect_sizes())
def cal7(): return _cal_suite(CAL.cal7_floor_and_orthostatic())


# ---- IV1-IV5: comfort-logic intervention layer (analgesic technique, ported) ----
# These stress the PORTED three-lever discipline, not new substrate physics: the map must
# build with all three levers placed and the counter-regulation direction READ off the proven
# loops (RP4 opposed-back / T1 reference-reset durable); the fail-closed firewall, the
# counter-regulation honesty gate, the falsification register and the burden ranking must all
# pass. Firewall scan runs docs-INDEPENDENT (scan_docs=False) so the battery never depends on
# built HTML. Grade [V] = ported logic verified against the proven loop; [O] = the per-axis
# molecular mechanism stays cited biology, never derived.
def iv1():
    m = IV.comfort_map()
    levers = set(m["axes_by_lever"].keys())
    a = m["proven_loop_anchors"]
    ok = (m["n_axes"] >= 6 and {"H1", "H2", "H3"}.issubset(levers)
          and a["operating_point_opposed_back"] is True        # H3-alone is rejected (RP4)
          and a["reference_reset_durable"] is True              # H1 reset is durable (T1)
          and a["hf_fourpillar_margin_grows"] is True           # HF H1-analogue grows the margin
          and len(m["dna_grounded_axes"]) >= 2)                 # SIX2 + REN axes DNA-grounded
    return _suite("IV1", "comfort map builds with all three levers placed and the counter-regulation "
                         "direction read off the proven loops (RP4 opposed-back / T1 reference-reset durable)",
                  ok, {"n_axes": m["n_axes"], "levers": sorted(levers),
                       "dna_grounded": m["dna_grounded_axes"]},
                  "[V] ported logic vs proven loop / [O] per-axis mechanism cited", _OBST)

def iv2():
    r = IVSCAN.run(scan_docs=False)
    ok = (r["overall"] == "PASS" and r["selftest_fired"] and r["safety_not_suppressed_ok"]
          and not r["missing_disclaimers"] and not r["missing_firewalls"])
    return _suite("IV2", "HP1-HP7 hypothesis-only proposal passes the fail-closed forbidden-claim firewall "
                         "(no dosing/efficacy/safety-as-fact; self-test fires; 'no side effects' not suppressed)",
                  ok, {"overall": r["overall"], "selftest_fired": r["selftest_fired"],
                       "safety_not_suppressed_ok": r["safety_not_suppressed_ok"]},
                  "[V] firewall fail-closed / [O] proposals are hypotheses, not claims", _OBST)

def iv3():
    r = IVHON.run()
    ok = (r["overall"] == "PASS" and not r["failures"])
    return _suite("IV3", "counter-regulation honesty gate: every per-axis molecular mechanism graded [O] cited "
                         "(never derived), lever placement [V] structural, gamma not presented as mechanism",
                  ok, {"overall": r["overall"], "n_failures": len(r["failures"])},
                  "[V] honesty gate fail-closed / [O] mechanisms cited", _OBST)

def iv4():
    r = IVFALS.register()
    ok = (r["overall"] == "PASS" and not r["missing"] and len(r["falsifiers"]) >= 7)
    return _suite("IV4", "falsification register: every HP1-HP7 proposal plus the framework has a named, "
                         "stated falsifier (the technique is refutable, not unfalsifiable)",
                  ok, {"overall": r["overall"], "n_falsifiers": len(r["falsifiers"]),
                       "n_missing": len(r["missing"])},
                  "[V] every proposal refutable / [O] outcomes are predictions", _OBST)

def iv5():
    r = IVPRIO.prioritise()
    order_ok = r["order"][0] in ("raas_ren", "sodium_volume_reference")  # DNA-grounded H1 axes lead
    ok = (r["n_axes"] >= 6 and order_ok
          and all(row.get("measured_gamma_carried_not_scored") is not None or row["dna_grounded"] is False
                  for row in r["ranking"]))
    return _suite("IV5", "burden-weighted prioritisation ranks target AXES (never drugs/doses) by declared "
                         "weights; measured gamma is carried for provenance, never folded into the score",
                  ok, {"n_axes": r["n_axes"], "order": r["order"]},
                  "[F] declared-weight rank / [O] axes only, not agents", _OBST)


STRESS_FUNCS = [rp1, rp2, rp3, rp4, rp5, s1, s2, t1, t2, rp6, rp7, rp8, rp9, c1,
                cal1, cal2, cal3, cal4, cal5, cal6, cal7,
                iv1, iv2, iv3, iv4, iv5]


def run_battery():
    base = eng.circulate()
    suites = [f() for f in STRESS_FUNCS]
    results = {
        "emergence_ok": bool(base["organs"]["organs"]),
        "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values()) if base["oscillators"] else None),
        "sensory_ok": ("baroreceptor" in base["sensory"] and "macula_densa" in base["sensory"]),
        "interaction_map_ok": (len(base["interaction_map"]["edges"]) >= 8 and len(base["interaction_map"]["nodes"]) >= 6),
        "deferred_gamma": base["organs"].get("deferred_gamma", []),
        "suites": suites,
    }
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in suites)
    results["calibration_ok"] = all(s["status"] == "PASS" for s in suites if s["target"].startswith("CAL"))
    results["n_pass"] = sum(1 for s in suites if s["status"] == "PASS")
    results["n_total"] = len(suites)
    return results


if __name__ == "__main__":
    r = run_battery(); print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nPASS %d/%d   ALL TARGETS PASS: %s (writing stays locked until True)" % (r["n_pass"], r["n_total"], r["all_targets_pass"]))
