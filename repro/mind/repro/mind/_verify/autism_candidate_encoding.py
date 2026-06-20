#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D9.1  CANDIDATE ENCODING -- a threshold-lowering "drug" AS CODE (mechanism operator)
====================================================================================
"Make the chemical as code, like the chemistry package did" -- here a candidate is
NOT a molecule with a dose. It is a MECHANISM-OF-ACTION OPERATOR on the R19 substrate,
encoded as a JSON-serialisable object, whose EFFECT is DERIVED from the substrate
physics with ZERO free parameters (the chemistry-package discipline: forced geometry,
no knob to tune). The analgesic package RAISED the firing threshold |h_sp| by any of
three levers; autism's T-fault is the OPPOSITE direction -- LOWER the raised fold --
so we invert the three levers and ground each in a real cohort channel/receptor gene.

THE THREE LEVERS (inverted analgesic L1/L2/L3; each LOWERS the fold), grounded:
  A1  inward-excitatory gain UP   -- enhance voltage-gated Na/Ca inward current
        => adds depolarising drive => +delta_bias.   genes: SCN2A, CACNA1C  (ION)
  A2  outward-K current DOWN       -- the inverse of the analgesic K_V7 OPENER
        => less hyperpolarisation => +delta_bias.     gene:  KCNQ3          (ION/Kv7.3)
  A3  tonic GABA-A inhibition DOWN -- remove the very inhibitory bias that RAISED the
        fold (the T-fault itself)  => +delta_bias.     genes: GABRB3/GABRA2/GABRA5 (GABA)

CANDIDATE OBJECT (chemistry-as-code):
  candidate = { id, name, levers: {A1:{magnitude,gamma_target,width,selective}, A2,A3},
                mechanism_only:True, no_dose:True, no_synthesis:True, efficacy:0 }
  * gamma_target = the LEVER GENE'S real promoter gamma (from D9.0) -- the channel's
                   "molecular stiffness" the drug keys off (receptor-subtype / state /
                   allosteric selectivity = "exploit the stiffness difference", D8.14).
  * width        = selectivity bandwidth (a MECHANISM property: narrow = subtype-
                   selective; wide -> blunt). NOT tuned.
  * magnitude    = how hard the lever is pushed. A SWEPT variable in D9.3, not a tuned
                   constant: we report the whole curve and READ the restoration point
                   off it; we never pick magnitude to hit a target (no-tuning, 0.2).
  * selective    = True -> stiffness-keyed (Gaussian); False -> blunt (D8.12, hits all).

WHAT IS DERIVED (no free parameter):
  delta_bias_i(cell) = magnitude_i * key_i(gamma_cell)
  b_eff = b_fault + sum_i delta_bias_i(cell)
  fold(cell) = R19 ignition threshold _ig_thr(gamma_cell, b_eff)   [ENGINE, frozen]
  seizure?   = _spontaneous(gamma_cell, b_eff)                     [ENGINE, frozen]
The fold and the seizure boundary come from the engine's measured R19 cusp; the
candidate only supplies WHERE (gamma_target), HOW SELECTIVE (width), HOW MUCH
(magnitude, swept). No fold value is fitted.

BIOLOGICAL GROUNDING OF "SPLIT ACROSS LEVERS": a real neuron co-expresses Na, K, and
GABA-A. All three levers converge on the SAME cell -- move its threshold a LITTLE on
each of three independent systems instead of a LOT on one. That is the multi-lever
hypothesis D9.3 tests (smaller per-system push -> smaller off-target footprint on
other cells sharing that channel, and more margin to the seizure edge).

DISCIPLINE: a forbidden-claim scan (analgesic M5 analogue) runs over every candidate's
text; any dose/mg, synthesis/route, efficacy, or safety claim FAILS the build.
efficacy=0; NOT medical advice; Axis-A firewall. Governed by VP-SPEC v1.8
(C0-C4, SEED=19). ADD-ONLY; vp_mind_engine READ-ONLY (tree 0fbf4988...). 2x sha256.
"""
import os, sys, json, math, hashlib, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY

ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
COHORT_RESULT = os.path.join(HERE, "autism_cohort_moderate_results.json")
RESULT = os.path.join(HERE, "autism_candidate_encoding_results.json")
EXPECT = os.path.join(HERE, "expected_autism_candidate_encoding_sha256.json")

# ----- engine fold primitives (D8.12 convention, byte-identical) -----
def ig_thr(g, b, cap=2.0, ngrid=801):
    for s in np.linspace(0.0, cap, ngrid):
        if E.settle(g, b + float(s), s0=-math.sqrt(g)) > 0.0:
            return float(s)
    return float("inf")

def spontaneous(g, b):
    return bool(E.settle(g, b, s0=-math.sqrt(g)) > 0.0)

# ----- the lever key (stiffness selectivity) -----
def lever_key(gamma, gamma_target, width, selective):
    if not selective:
        return 1.0
    return math.exp(-((gamma - gamma_target) ** 2) / (2.0 * width ** 2))

def apply_candidate(gamma_cell, b_fault, candidate):
    b = b_fault
    for lv in candidate["levers"].values():
        b += lv["magnitude"] * lever_key(gamma_cell, lv["gamma_target"], lv["width"], lv["selective"])
    return b

# =====================================================================================
#  CANDIDATE LIBRARY  -- grounded in the D9.0 cohort lever genes
# =====================================================================================
def lever_gamma_targets():
    co = json.load(open(COHORT_RESULT, encoding="utf-8"))["genes"]
    tgt = {"A1": [], "A2": [], "A3": []}
    for sym, rec in co.items():
        if rec["lever"] in tgt:
            tgt[rec["lever"]].append((sym, rec["gamma"]))
    means = {lv: round(sum(g for _, g in v) / len(v), 4) for lv, v in tgt.items() if v}
    return tgt, means

def L(mag, gt, sel, basis, width):
    return dict(magnitude=round(mag, 4), gamma_target=round(gt, 4), width=round(width, 4),
                selective=sel, gene_basis=basis)

def build_library(total_correction=0.25, width=0.05):
    """blunt single -> selective single -> dual -> tri-lever. total_correction is the
    SUM of lever magnitudes at the reference point; D9.3 SWEEPS magnitudes and reads the
    restoration point off (not tuned here). width = subtype-selectivity (mechanism)."""
    _, gA = lever_gamma_targets()
    A1, A2, A3 = gA["A1"], gA["A2"], gA["A3"]
    lib = {}
    lib["C0_blunt_single"] = dict(
        id="C0_blunt_single",
        name="blunt single-lever threshold operator (D8.12 baseline: uniform E/I shift)",
        rationale="one global depolarising shift; hits every cell equally (no subtype/state selectivity)",
        levers={"A3": L(total_correction, A3, False, "GABRB3/GABRA2/GABRA5 (tonic GABA-A), applied BLUNT", width)})
    lib["C1_selective_single"] = dict(
        id="C1_selective_single",
        name="stiffness-selective single-lever operator (D8.14: subtype/state-selective)",
        rationale="one lever keyed to the faulted stiffness (receptor-subtype / use-dependent selectivity)",
        levers={"A3": L(total_correction, A3, True, "GABRB3/GABRA2/GABRA5 (tonic GABA-A), subtype-selective", width)})
    lib["C2_dual_selective"] = dict(
        id="C2_dual_selective",
        name="dual-lever stiffness-selective operator (A1 excitability + A3 disinhibition)",
        rationale="split the correction across two independent channel systems, each subtype-selective",
        levers={"A1": L(total_correction / 2, A1, True, "SCN2A/CACNA1C (Nav/Cav inward gain)", width),
                "A3": L(total_correction / 2, A3, True, "GABA-A tonic disinhibition", width)})
    lib["C3_trilever_selective"] = dict(
        id="C3_trilever_selective",
        name="tri-lever stiffness-selective threshold operator (A1 + A2 + A3) -- THE PROPOSAL",
        rationale="a real neuron co-expresses Na, K, GABA-A; move the fold a little on each of three "
                  "independent, subtype-selective systems instead of a lot on one -- smaller per-system "
                  "footprint, more margin to the seizure edge. The analgesic three-lever logic, inverted.",
        levers={"A1": L(total_correction / 3, A1, True, "SCN2A/CACNA1C (Nav/Cav inward gain UP)", width),
                "A2": L(total_correction / 3, A2, True, "KCNQ3 (Kv7.3 outward current DOWN)", width),
                "A3": L(total_correction / 3, A3, True, "GABA-A a5/b3/a2 (tonic inhibition DOWN)", width)})
    common = dict(mechanism_only=True, no_dose=True, no_synthesis=True, efficacy=0,
                  not_medical_advice=True,
                  axis_A_firewall="lowering a fold = ignition mechanism, not experience")
    for c in lib.values():
        c.update(common)
    return lib, gA

# ----- forbidden-claim scan (analgesic M5 analogue; fail-closed) -----
FORBIDDEN = {
    "DOSING":   [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdosage\b", r"\bdose[sd]?\b",
                 r"\btwice\s+daily\b", r"\bonce\s+daily\b", r"\bmilligram"],
    "SYNTHESIS":[r"\bsynthesi[sz]e[sd]?\b", r"\breagent", r"\breflux", r"\bmmol\b", r"\bsynthetic\s+route\b"],
    "EFFICACY": [r"\bcures\b", r"\bwill\s+cure\b", r"\btreats?\s+patients?\b",
                 r"\bis\s+effective\s+in\s+patients\b", r"\beliminates?\s+(pain|symptoms)\b"],
    "SAFETY":   [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                 r"\bwithout\s+side[-\s]?effects?\b", r"\bcompletely\s+safe\b"],
}
NEG = re.compile(r"\b(?:no|not|without|never|non)\b(?:[\s\-]+(?:a|an|any|the))?[\s\-]*$", re.I)

def scan_text(text):
    hits = []
    for cls, pats in FORBIDDEN.items():
        for p in pats:
            for m in re.finditer(p, text, flags=re.I):
                if cls in ("DOSING", "SYNTHESIS") and NEG.search(text[max(0, m.start() - 24):m.start()]):
                    continue
                hits.append([cls, m.group(0)])
    return hits

def _round(o, nd=6):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, dict):  return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v, nd) for v in o]
    return o

def run():
    E.seed_everything()
    lib, gA = build_library()

    # SELF-TEST 1: lever physics reproduces the D8.12 baseline (no free param)
    G = 1.0
    fold_health = round(ig_thr(G, 0.0), 4)
    fold_fault  = round(ig_thr(G, -0.25), 4)
    baseline_ok = bool(abs(fold_health - 0.3925) < 1e-6 and abs(fold_fault - 0.6425) < 1e-6)

    # SELF-TEST 2: a BLUNT full-correction lever returns a faulted cell to health exactly
    #   (apply C0 to a faulted cell of stiffness G with key=1) -> b_eff = -0.25 + 0.25 = 0
    b_eff_blunt = apply_candidate(G, -0.25, lib["C0_blunt_single"])
    fold_after_blunt = round(ig_thr(G, b_eff_blunt), 4)
    blunt_restores = bool(abs(fold_after_blunt - fold_health) < 1e-6)

    # SELF-TEST 3: a SELECTIVE lever whose target == the cell's stiffness acts ~fully on it,
    #   but acts WEAKLY on a distant-stiffness cell (the selectivity property)
    A3 = gA["A3"]
    key_on_target  = lever_key(A3, A3, 0.05, True)            # ~1.0
    key_off_target = lever_key(A3 + 0.20, A3, 0.05, True)     # ~0 (0.20 >> width 0.05)
    selectivity_ok = bool(key_on_target > 0.99 and key_off_target < 0.01)

    # SELF-TEST 4: forbidden-claim scan over the whole library text (must be CLEAN)
    lib_text = json.dumps(lib, ensure_ascii=False)
    forbidden_hits = scan_text(lib_text)
    # planted positive proves the scanner actually fires
    planted = scan_text("administer 50 mg twice daily; this cures patients and is completely safe")
    scanner_fires = len(planted) >= 3
    library_clean = len(forbidden_hits) == 0

    out = {
        "_what": "D9.1 candidate encoding: a threshold-lowering 'drug' is a multi-lever MECHANISM "
                 "operator on the R19 substrate (chemistry-as-code), its EFFECT derived from the engine "
                 "fold with zero free parameters. Library spans blunt-single (D8.12) -> selective-single "
                 "(D8.14) -> dual -> tri-lever (the proposal). Magnitudes are SWEPT in D9.3, not tuned. "
                 "Levers grounded in the real cohort channel/receptor gammas (D9.0).",
        "lever_definitions": {
            "A1": "inward-excitatory gain UP (Nav/Cav) -> +delta_bias  [SCN2A, CACNA1C]",
            "A2": "outward-K current DOWN (Kv7.3, inverse of analgesic opener) -> +delta_bias  [KCNQ3]",
            "A3": "tonic GABA-A inhibition DOWN (remove the fault's own bias) -> +delta_bias  [GABRB3/GABRA2/GABRA5]",
        },
        "lever_gamma_targets_from_cohort": gA,
        "candidate_library": lib,
        "self_tests": {
            "baseline_fold_health": fold_health, "baseline_fold_fault": fold_fault,
            "baseline_reproduces_D8_12": baseline_ok,
            "blunt_full_correction_restores_health": blunt_restores,
            "fold_after_blunt": fold_after_blunt,
            "selective_key_on_target": round(key_on_target, 6),
            "selective_key_off_target": round(key_off_target, 6),
            "selectivity_behaves": selectivity_ok,
            "library_forbidden_claim_clean": library_clean,
            "forbidden_hits": forbidden_hits,
            "scanner_self_test_fires_on_planted": scanner_fires,
        },
        "no_free_parameter_statement": "the candidate supplies only gamma_target (a measured gene gamma), "
            "width (a mechanism property), and magnitude (swept). The fold and the seizure boundary are "
            "the engine's measured R19 cusp -- no fold value is fitted; no constant is tuned to a target.",
        "firewall": "mechanism only; efficacy=0; no dose; no synthesis; NOT medical advice; Axis-A firewall.",
        "honesty_ledger": {"medium_efficacy_tested": 0, "consciousness_claim": 0,
                           "new_tuned_constants": 0, "no_cure_claimed": 1},
        "invariants": {"engine_tree_frozen": ENGINE_TREE_FROZEN},
        "overall_pass": bool(baseline_ok and blunt_restores and selectivity_ok
                             and library_clean and scanner_fires),
    }
    return out

if __name__ == "__main__":
    res = run()
    open(RESULT, "w", encoding="utf-8").write(json.dumps(_round(res), indent=1, sort_keys=True, ensure_ascii=False))
    h = hashlib.sha256(json.dumps(_round(res), sort_keys=True, ensure_ascii=False,
                                  separators=(",", ":")).encode()).hexdigest()
    json.dump({"autism_candidate_encoding_results.json": h}, open(EXPECT, "w"), indent=1)
    st = res["self_tests"]
    print("D9.1 candidate encoding")
    print(f"  baseline reproduces D8.12 : {st['baseline_reproduces_D8_12']} "
          f"(health {st['baseline_fold_health']}, fault {st['baseline_fold_fault']})")
    print(f"  blunt full correction -> health : {st['blunt_full_correction_restores_health']}")
    print(f"  selectivity on/off target : {st['selective_key_on_target']} / {st['selective_key_off_target']} "
          f"-> behaves {st['selectivity_behaves']}")
    print(f"  library forbidden-claim clean : {st['library_forbidden_claim_clean']}  "
          f"scanner fires on planted : {st['scanner_self_test_fires_on_planted']}")
    print(f"  candidates: {list(res['candidate_library'].keys())}")
    print(f"  OVERALL PASS: {res['overall_pass']}")
    print(f"  result sha256: {h}")
