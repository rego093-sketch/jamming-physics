#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
intervention_logic.py  --  v0.7.0  --  the THREE-LEVER hemodynamic comfort map.

This module imports the analgesic_threshold_logic v2.0 idiom (Zenodo concept DOI
10.5281/zenodo.20733420) into the hemodynamic package and applies it to arterial-pressure
control. The analgesic work read the nociceptor's FIRING THRESHOLD from real promoter DNA and
proposed -- as a HYPOTHESIS only -- to raise it from three directions (L1 reduce the inward
current / L2 increase the outward K+ current / L3 remove the up-stream sensitising drive). The
SAME organising frame is applied here, with the defended-MAP setpoint playing the role of the
threshold:

  the pain gate  : raise the firing threshold |h_sp|, selectively, by any of three levers.
  the MAP loop   : LOWER the defended arterial-pressure setpoint, durably, by any of three levers,
                   WITHOUT provoking the loop's own counter-regulation.

THE COMFORT PRINCIPLE (the reason this is worth porting).
  This package already PROVED (RP4 + T1) that the arterial-pressure loop is an integral controller
  that REJECTS operating-point pushes back toward its (high) reference. That rejection -- the
  baroreflex/RAAS/renal counter-regulation -- IS the structural origin of the familiar
  antihypertensive side-effect class (reflex tachycardia, fluid retention, fatigue, escape). A
  direction that moves the loop's OWN setpoint provokes no rejection, because there is no error
  signal to oppose. "Counter-regulation-free" is therefore a STRUCTURAL property of a lever, read
  off the proven loop -- it is NOT a clinical tolerability or safety claim (those are [O]).

THE THREE LEVERS (each LOWERS the defended MAP; ordered by counter-regulation provoked).
  H1  RESET THE INTEGRATOR REFERENCE DOWN  (counter-regulation-free; the fundamental lever)
       lower the renal pressure-natriuresis / RAAS reference itself. The loop's target moves WITH
       the intervention, so no error signal is generated and nothing opposes it. DNA-grounded axis:
       REN (renin master gene, gamma MEASURED in-package = 1.3634). <-- analgesic L3 analogue
       ("remove the up-stream drive": here, the sympathetic/RAAS/Na drive that holds the reference high).
  H2  RESTORE THE FAST RESTORING BUFFER  (low counter-regulation; the stability lever)
       strengthen baroreflex buffer gain so excursions self-correct toward the (now-lower) setpoint.
       DNA/biology-grounded sensor: PIEZO1/2 baroreceptor. <-- analgesic L2 analogue
       ("increase the outward/restoring current": raise the loop's own error-correcting current).
  H3  UNLOAD THE EFFECTOR, PAIRED-ONLY  (counter-regulation-PRONE alone; the symptomatic lever, made honest)
       reduce SVR/volume pressor drive at the effector. ALONE at the operating point it is rejected
       back (RP4) -- the rejection is the side-effect class. PAIRED with H1 (the reference has moved)
       it is no longer opposed. <-- analgesic L1 analogue ("reduce the inward/excitatory current"),
       WITH a caveat the pain gate does not have (see CROSS-PACKAGE CONTRAST).

CROSS-PACKAGE CONTRAST (evidence the technique was applied with understanding, not copied).
  The nociceptor firing gate has NO integral controller downstream, so the analgesic L1 lever
  (block the inward current) works ALONE. The arterial-pressure loop HAS an integral controller
  (the kidney reference, RP3 "infinite gain"), so the H3 analogue (block the effector) is REJECTED
  alone (RP4) and must be PAIRED with a reference reset (H1) to be durable AND counter-regulation-free.
  Same lever frame; the integrator is the difference -- and the integrator is exactly what this
  package is the SSOT for.

FIREWALL (Axis-C comfort firewall, binding -- mirrors the analgesic Axis-A firewall).
  This module READS loop STRUCTURE (the proven RP4/T1 counter-regulation direction) and PLACES each
  axis in the lever map. It is NOT a drug, NOT a dose, NOT an efficacy/safety/tolerability/PK result,
  NOT an in-vivo selectivity. Those are Layer-2 [O] and are never asserted. The per-axis MOLECULAR
  mechanism link is [O] cited biology, never derived from the loop read (enforced by the
  counter-regulation-honesty gate, counterreg_honesty.py). No medical responsibility.

No new substrate math: every number is reused from the locked loop modules (vp_hmd_loops, RX) or is
a measured gamma; nothing is fitted (C1).

Run:  python3 intervention_logic.py   -> expected/comfort_map.json
"""
import os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
for _sub in ("_engine", "_therapy"):
    sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", _sub)))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "..", "inherited")))
import vp_hmd_loops as L           # proven RP1-RP5 loop primitives (locked)
import fundamental_targets as RX   # proven T1/T2 fundamental-vs-symptomatic therapy (locked)

_GAMMA = os.path.normpath(os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json"))

# --- the unifying lever frame (parallels analgesic L1/L2/L3) ----------------------------------
LEVER_FRAME = {
    "H1": ("reset the integrator reference DOWN -- lower the renal pressure-natriuresis / RAAS "
           "setpoint itself; the loop's target moves WITH the intervention so nothing opposes it "
           "(counter-regulation-free). Analgesic L3 analogue."),
    "H2": ("restore the fast restoring buffer -- strengthen baroreflex buffer gain so excursions "
           "self-correct toward the lower setpoint; raises the loop's own error-correcting current. "
           "Analgesic L2 analogue."),
    "H3": ("unload the effector, PAIRED-ONLY -- reduce SVR/volume pressor drive; alone it is "
           "rejected back (counter-regulation = the side-effect class), paired with H1 it is not. "
           "Analgesic L1 analogue, with the integrator caveat."),
}

# CITED Layer-2 context (NOT a loop output) -- source-tagged axes, one per intervention target.
# grade_mechanism: [V] structural direction from the PROVEN loop (RP4/T1) for the lever placement;
#                  the per-axis MOLECULAR mechanism link is [O] cited biology, never derived.
HV = "[V] structural direction read off the PROVEN loop (RP4 reject / T1 durable; no new math)"
HO = ("[O] cited biology: the loop read PLACES the axis in the lever map; the receptor/transporter/"
      "channel pharmacology is NOT derived from the read")

AXES = {
  # ---- H1: reference-reset axes (counter-regulation-free) ----
  "renal_sympathetic": dict(
      lever="H1", push="lower the renal sympathetic drive that holds the pressure-natriuresis reference high",
      node="renal efferent sympathetic nerves", gene=None, gamma=None,
      counterreg="free (reference moves; no operating-point error to reject)",
      dna_grounded=False,
      selectivity_tier="renal-reference axis (cited): renal denervation lowers the defended reference",
      burden_tier="Tier-1 resistant/essential hypertension",
      src="Bohm 2020 Lancet 395:1444 (SPYRAL-HTN-ON-MED); FDA approval of renal denervation 2023",
      grade_lever=HV, grade_mechanism=HO),
  "raas_ren": dict(
      lever="H1", push="down-regulate the RAAS drive (renin-angiotensin-aldosterone) that raises the renal reference",
      node="raas_endocrine", gene="REN", gamma="MEASURED",
      counterreg="free (reference axis; RAAS blockade resets the defended pressure, T1)",
      dna_grounded=True,
      selectivity_tier="RAAS reference axis (cited): the slow integrator's hormonal arm; REN node is DNA-grounded",
      burden_tier="Tier-1 essential hypertension + HF overlap",
      src="Guyton 1972 (pressure-natriuresis/RAAS integral control); ACEi/ARB/MRA renal-reference backbone [L]",
      grade_lever=HV, grade_mechanism=HO),
  "sodium_volume_reference": dict(
      lever="H1", push="lower the sustained Na+/volume load that sets the renal pressure-natriuresis reference",
      node="kidney_volume_integrator", gene="SIX2", gamma="MEASURED",
      counterreg="free (the integrator's own reference is lowered, RP3/RP4)",
      dna_grounded=True,
      selectivity_tier="volume-reference axis (cited): sustained Na/weight reduction resets the integrator",
      burden_tier="Tier-1 essential hypertension (population-attributable)",
      src="INTERSALT / DASH-sodium (Na-BP exposure-response) [L]; the kidney integrator is SIX2-grounded",
      grade_lever=HV, grade_mechanism=HO),
  # ---- H2: buffer-restoration axis (low counter-regulation) ----
  "baroreflex_piezo": dict(
      lever="H2", push="restore baroreflex buffer gain (PIEZO1/2 stretch transduction) so excursions self-correct",
      node="baroreceptor", gene=None, gamma=None,
      counterreg="low (improves the loop's own error correction; does not fight the setpoint, RP2/RP6)",
      dna_grounded=False,
      selectivity_tier="fast-buffer axis (cited): baroreflex activation; PIEZO1/2 is the stretch sensor",
      burden_tier="Tier-2 resistant hypertension / autonomic lability",
      src="Zeng 2018 Science 362:464 (PIEZO1/2 baroreceptor); baroreflex activation therapy [L]",
      grade_lever=HV, grade_mechanism=HO),
  # ---- H3: effector-unload axis (counter-regulation-prone ALONE; paired-only) ----
  "svr_effector": dict(
      lever="H3", push="reduce SVR / volume pressor drive at the effector -- PAIRED with H1 only",
      node="vascular_resistance", gene=None, gamma=None,
      counterreg="PRONE alone (operating-point push is rejected back, RP4 -> the side-effect class); "
                 "FREE only when paired with an H1 reference reset",
      dna_grounded=False,
      selectivity_tier="effector axis (cited): vasodilators/diuretics; durable ONLY with a renal/volume arm",
      burden_tier="adjunct (paired); monotherapy escapes",
      src="vasodilator-monotherapy escape without a volume/renal arm; the diuretic/renal backbone [L]",
      grade_lever=HV, grade_mechanism=HO),
  # ---- HF arm: basin-margin axis (the heart-failure comfort direction) ----
  "hf_margin_fourpillar": dict(
      lever="H1-like (HF)", push="grow the basin margin M=spinodal(kappa)-|load| by load-reduce + cycle-break, never effector-flog",
      node="cardiac high-output basin", gene=None, gamma=None,
      counterreg="margin grows (T2): load reduction + neurohormonal cycle-break restores the basin; "
                 "inotrope flogging SHRINKS the margin (accelerated collapse)",
      dna_grounded=False,
      selectivity_tier="HF margin axis (cited): the four-pillar direction (ARNI/BB/MRA/SGLT2i)",
      burden_tier="Tier-1 chronic heart failure",
      src="PROMISE milrinone +28% mortality (Packer 1991) vs four pillars (PARADIGM-HF/CIBIS-II/RALES/DAPA-HF) [L]",
      grade_lever=HV, grade_mechanism=HO),
}


def _gamma(sym):
    if sym is None:
        return None
    try:
        return round(float(json.load(open(_GAMMA, encoding="utf-8"))["genes"][sym]["gamma"]), 6)
    except Exception:
        return None


def _entry(name, c):
    return {
        "axis": name,
        "lever": c["lever"],
        "push_direction": c["push"],
        "node": c["node"],
        "master_gene": c["gene"],
        "measured_gamma": _gamma(c["gene"]) if c["gamma"] == "MEASURED" else None,
        "dna_grounded": c["dna_grounded"],
        "counter_regulation": c["counterreg"],
        "selectivity_tier": c["selectivity_tier"],
        "burden_tier": c["burden_tier"],
        "grade_lever": c["grade_lever"],
        "grade_mechanism": c["grade_mechanism"],
        "grade_clinical_map": "[O] OPEN -- not a drug, dose, efficacy, safety, tolerability, or in-vivo selectivity",
        "context_grade": "CITED Layer-2 biology (not a loop output)",
        "src": c["src"],
    }


def comfort_map():
    """The three-lever comfort map: every axis placed in its lever, with the proven-loop direction
    that makes it counter-regulation-free (or, for H3, prone-alone). No new substrate math (C1)."""
    # pull the two proven directions the comfort principle rests on (locked modules)
    htn = RX.hypertension_therapies()
    hf = RX.heart_failure_therapies()
    op_opposed = bool(htn["operating_point_drug"]["opposed_back"])           # RP4/T1: rejected back
    op_durable_drop = htn["operating_point_drug"]["durable_drop_mmHg"]        # ~0 (not durable)
    ref_durable = bool(htn["reference_reset"]["durable"])                     # reference reset holds
    ref_durable_drop = htn["reference_reset"]["durable_drop_mmHg"]
    ino_shrinks = bool(hf["inotrope_flog"]["margin_shrinks"])                 # effector flog shrinks M
    pillar_grows = bool(hf["load_reduce_cycle_break"]["margin_grows"])        # four-pillar grows M

    entries = [_entry(name, c) for name, c in AXES.items()]
    by_lever = {}
    for e in entries:
        by_lever.setdefault(e["lever"], []).append(e["axis"])

    return {
        "title": "Three-lever hemodynamic comfort map (proven-loop directions + cited axis frame)",
        "imported_from": "analgesic_threshold_logic v2.0 (Zenodo concept DOI 10.5281/zenodo.20733420)",
        "primitive": ("the analgesic three-lever frame applied to the defended-MAP setpoint: LOWER the "
                      "setpoint durably without provoking the loop's counter-regulation, by any of three levers"),
        "comfort_principle": (
            "operating-point antagonism is REJECTED back by the integral controller (RP4: opposed_back=%s, "
            "durable drop=%g mmHg) -- that rejection is the structural origin of the side-effect class; a "
            "reference-reset direction provokes no rejection (T1: reference reset durable=%s, durable drop=%g "
            "mmHg). 'Counter-regulation-free' is a STRUCTURAL property of the lever, NOT a tolerability/safety "
            "claim ([O])." % (op_opposed, op_durable_drop, ref_durable, ref_durable_drop)),
        "cross_package_contrast": (
            "the nociceptor gate has no integral controller, so the analgesic L1 lever works ALONE; the MAP "
            "loop HAS one (the kidney reference), so the H3 analogue is rejected alone (RP4) and must be paired "
            "with an H1 reference reset. Same lever frame; the integrator is the difference."),
        "levers": LEVER_FRAME,
        "proven_loop_anchors": {
            "operating_point_opposed_back": op_opposed,
            "operating_point_durable_drop_mmHg": op_durable_drop,
            "reference_reset_durable": ref_durable,
            "reference_reset_durable_drop_mmHg": ref_durable_drop,
            "hf_inotrope_margin_shrinks": ino_shrinks,
            "hf_fourpillar_margin_grows": pillar_grows,
        },
        "firewall": (
            "READS loop STRUCTURE (the proven RP4/T1 counter-regulation direction) and PLACES each axis in the "
            "lever map. NOT a drug, dose, efficacy, safety, tolerability, PK, or in-vivo selectivity (those are "
            "[O]). The per-axis molecular mechanism link is [O] cited biology, never derived from the loop read. "
            "'Counter-regulation-free' is structural, not a safety/tolerability claim. No medical responsibility."),
        "n_axes": len(entries),
        "axes_by_lever": by_lever,
        "dna_grounded_axes": sorted([e["axis"] for e in entries if e["dna_grounded"]]),
        "entries": entries,
    }


def all_intervention():
    """Deterministic, docs-INDEPENDENT aggregate of the whole comfort-logic layer.

    Folds the three-lever map, the burden prioritisation, the counter-regulation
    honesty gate, the falsification register and the fail-closed forbidden-claim
    scan (scan_docs=False so the engine hash never depends on built HTML) into one
    object for inclusion in the engine's circulate() hash. Imports the sibling
    modules by absolute path so it works when called from the engine.
    """
    import importlib
    if _HERE not in sys.path:
        sys.path.insert(0, _HERE)
    prio = importlib.import_module("burden_prioritisation").prioritise()
    honesty = importlib.import_module("counterreg_honesty").run()
    falsify = importlib.import_module("falsification").register()
    scan = importlib.import_module("forbidden_claim_scan").run(scan_docs=False)
    cmap = comfort_map()
    return {
        "title": "Hemodynamic comfort-logic layer (analgesic three-lever technique, ported)",
        "imported_from": "analgesic_threshold_logic v2.0 (Zenodo concept DOI 10.5281/zenodo.20733420)",
        "comfort_map": {
            "n_axes": cmap["n_axes"],
            "axes_by_lever": cmap["axes_by_lever"],
            "dna_grounded_axes": cmap["dna_grounded_axes"],
            "order": [e["axis"] for e in cmap["entries"]],
            "levers": [e["axis"] + ":" + e["lever"] for e in cmap["entries"]],
            "proven_loop_anchors": cmap["proven_loop_anchors"],
        },
        "prioritisation": {"n_axes": prio["n_axes"], "order": prio["order"]},
        "counterreg_honesty": {"overall": honesty["overall"], "failures": honesty["failures"]},
        "falsification": {"overall": falsify["overall"], "n": len(falsify.get("falsifiers", {}))},
        "claim_scan": {"overall": scan["overall"],
                       "selftest_fired": scan["selftest_fired"],
                       "safety_not_suppressed_ok": scan["safety_not_suppressed_ok"]},
        "all_gates_pass": (honesty["overall"] == "PASS" and falsify["overall"] == "PASS"
                           and scan["overall"] == "PASS"),
    }


if __name__ == "__main__":
    m = comfort_map()
    os.makedirs(os.path.join(_HERE, "expected"), exist_ok=True)
    json.dump(m, open(os.path.join(_HERE, "expected", "comfort_map.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("IV three-lever comfort map (axes by lever; counter-regulation read off the proven loop):")
    print("  %-26s %-10s %-14s %s" % ("axis", "lever", "DNA-grounded", "counter-regulation"))
    for e in m["entries"]:
        cr = e["counter_regulation"].split("(")[0].strip()
        print("  %-26s %-10s %-14s %s" % (e["axis"], e["lever"], e["dna_grounded"], cr[:40]))
    print("  axes by lever: " + ", ".join("%s=%d" % (k, len(v)) for k, v in m["axes_by_lever"].items()))
    print("  DNA-grounded axes: %s" % ", ".join(m["dna_grounded_axes"]))
    print("wrote expected/comfort_map.json  (%d axes)" % m["n_axes"])
