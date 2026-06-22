#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_completeness.py — self-containment + reproduction audit for vp_wave_computer.

Run from anywhere:  python3 repro/check_completeness.py
(or from repro/:     python3 check_completeness.py)

Verifies the archive is INTACT and SELF-CONTAINED for a cold-start new session:
  (1) every file in the canonical manifest is present  -> regression prevention
  (2) the inheritance manifest is self-contained         -> no external file needed
  (3) all simulations re-run and reproduce their pinned digests bit-for-bit
      (S1-S9 layer sims + the S10 L9 END-CONDITION module wave_agi_core.py + the S11 post-program
       hardening module wave_adapt_closure_core.py, which re-probes the A3 [O] with the proven L5
       dual store wired in and shows the [O]->[V] closure inline + the S12 post-program compression
       module wave_axiom_audit_core.py, which ablates each operational substrate axiom and tests
       whether the inherited invariants reduce to a minimal irreducible set; the L9 module is the
       heaviest -- on a single core it computes its 7 ladder rungs once and is checkpoint-cached
       to .cache_v0_10/ so re-runs resume; determinism is unchanged, the digest is identical
       whether produced in one pass or resumed)

Exit 0 = package whole and reproducing. Exit non-zero = regressed; fix before new work.
"""

import os
import sys
import json
import subprocess
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---- canonical file manifest (must all be present; additive-only) ----
DOCS = [
    "HANDOFF.md",
    "START_HERE_wave_computer.md",
    "INHERITANCE_MANIFEST.md",
    "BLUEPRINT_toward_ultimate_computer.md",
    "CUMULATIVE_LOG.md",
    "SESSION_v0_1_design_study.md",
    "SESSION_v0_2_resonance_and_learning.md",
    "SESSION_v0_3_structure_and_time.md",
    "SESSION_v0_4_hierarchy_and_abstraction.md",
    "SESSION_v0_5_inference_and_resonance.md",
    "SESSION_v0_6_dual_learning_systems.md",
    "SESSION_v0_7_self_supervised_world_model.md",
    "SESSION_v0_8_embodiment_and_control.md",
    "SESSION_v0_9_global_integration_and_access.md",
    "SESSION_v0_10_functional_general_intelligence.md",
    "SESSION_v0_11_adaptation_closure.md",
    "SESSION_v0_12_axiom_independence_audit.md",
    "CITATION.cff",
]
REPRO = [
    "wave_compute_core.py", "wave_compute_results.json", "wave_compute_atlas.png",
    "make_figure.py", "expected_digest.json",
    "wave_resonance_core.py", "wave_resonance_results.json", "wave_resonance_atlas.png",
    "make_figure_v0_2.py", "expected_digest_v0_2.json",
    "wave_structure_core.py", "wave_structure_results.json", "wave_structure_atlas.png",
    "make_figure_v0_3.py", "expected_digest_v0_3.json",
    "wave_hierarchy_core.py", "wave_hierarchy_results.json", "wave_hierarchy_atlas.png",
    "make_figure_v0_4.py", "expected_digest_v0_4.json",
    "wave_inference_core.py", "wave_inference_results.json", "wave_inference_atlas.png",
    "make_figure_v0_5.py", "expected_digest_v0_5.json",
    "wave_consolidation_core.py", "wave_consolidation_results.json", "wave_consolidation_atlas.png",
    "make_figure_v0_6.py", "expected_digest_v0_6.json",
    "wave_world_model_core.py", "wave_world_model_results.json", "wave_world_model_atlas.png",
    "make_figure_v0_7.py", "expected_digest_v0_7.json",
    "wave_embodiment_core.py", "wave_embodiment_results.json", "wave_embodiment_atlas.png",
    "make_figure_v0_8.py", "expected_digest_v0_8.json",
    "wave_workspace_core.py", "wave_workspace_results.json", "wave_workspace_atlas.png",
    "make_figure_v0_9.py", "expected_digest_v0_9.json",
    "wave_agi_core.py", "wave_agi_results.json", "wave_agi_atlas.png",
    "make_figure_v0_10.py", "expected_digest_v0_10.json",
    "wave_adapt_closure_core.py", "wave_adapt_closure_results.json", "wave_adapt_closure_atlas.png",
    "make_figure_v0_11.py", "expected_digest_v0_11.json",
    "wave_axiom_audit_core.py", "wave_axiom_audit_results.json", "wave_axiom_audit_atlas.png",
    "make_figure_v0_12.py", "expected_digest_v0_12.json",
    "check_completeness.py",
]

# ---- reproduction targets: (module, results.json, expected.json, digest-key) ----
SIMS = [
    ("wave_compute_core.py", "wave_compute_results.json",
     "expected_digest.json", "wave_compute_results_digest"),
    ("wave_resonance_core.py", "wave_resonance_results.json",
     "expected_digest_v0_2.json", "wave_resonance_results_digest"),
    ("wave_structure_core.py", "wave_structure_results.json",
     "expected_digest_v0_3.json", "wave_structure_results_digest"),
    ("wave_hierarchy_core.py", "wave_hierarchy_results.json",
     "expected_digest_v0_4.json", "wave_hierarchy_results_digest"),
    ("wave_inference_core.py", "wave_inference_results.json",
     "expected_digest_v0_5.json", "wave_inference_results_digest"),
    ("wave_consolidation_core.py", "wave_consolidation_results.json",
     "expected_digest_v0_6.json", "wave_consolidation_results_digest"),
    ("wave_world_model_core.py", "wave_world_model_results.json",
     "expected_digest_v0_7.json", "wave_world_model_results_digest"),
    ("wave_embodiment_core.py", "wave_embodiment_results.json",
     "expected_digest_v0_8.json", "wave_embodiment_results_digest"),
    ("wave_workspace_core.py", "wave_workspace_results.json",
     "expected_digest_v0_9.json", "wave_workspace_results_digest"),
    ("wave_agi_core.py", "wave_agi_results.json",
     "expected_digest_v0_10.json", "wave_agi_results_digest"),
    ("wave_adapt_closure_core.py", "wave_adapt_closure_results.json",
     "expected_digest_v0_11.json", "wave_adapt_closure_results_digest"),
    ("wave_axiom_audit_core.py", "wave_axiom_audit_results.json",
     "expected_digest_v0_12.json", "wave_axiom_audit_results_digest"),
]


def check_files():
    print("[1] file manifest (regression prevention)")
    missing = []
    for f in DOCS:
        ok = os.path.exists(os.path.join(ROOT, f))
        print(f"    {'OK ' if ok else 'MISS'}  {f}")
        if not ok:
            missing.append(f)
    for f in REPRO:
        ok = os.path.exists(os.path.join(HERE, f))
        print(f"    {'OK ' if ok else 'MISS'}  repro/{f}")
        if not ok:
            missing.append("repro/" + f)
    return missing


def check_self_contained():
    print("[2] self-containment (inheritance captured in-archive)")
    p = os.path.join(ROOT, "INHERITANCE_MANIFEST.md")
    if not os.path.exists(p):
        print("    MISS  INHERITANCE_MANIFEST.md")
        return False
    txt = open(p, encoding="utf-8").read()
    # the manifest must carry the actual inherited anchors, not just references
    needles = ["0.38961455156044245", "c\u00b2 = B/\u03c1", "consciousness_claim = 0",
               "clock-free", "1/r\u00b2"]
    ok = all(n in txt for n in needles)
    for n in needles:
        print(f"    {'OK ' if n in txt else 'MISS'}  captures: {n}")
    return ok


def run_sim(module):
    """Run a sim module in-process (so cwd-independent) by importing and calling main."""
    cwd = os.getcwd()
    os.chdir(HERE)  # results are written next to the module
    try:
        spec = importlib.util.spec_from_file_location(
            module.replace(".py", ""), os.path.join(HERE, module))
        mod = importlib.util.module_from_spec(spec)
        # ensure sibling imports (wave_resonance imports wave_compute) resolve
        if HERE not in sys.path:
            sys.path.insert(0, HERE)
        spec.loader.exec_module(mod)
        # silence stdout from main()
        import io
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            mod.main()
    finally:
        os.chdir(cwd)


def check_reproduction():
    print("[3] reproduction audit (deterministic digests)")
    all_ok = True
    for module, results, expected, key in SIMS:
        try:
            run_sim(module)
            got = json.load(open(os.path.join(HERE, results)))["_digest"]
            exp = json.load(open(os.path.join(HERE, expected)))[key]
            ok = (got == exp)
            print(f"    {'OK ' if ok else 'FAIL'}  {module:<26} {got[:16]}  reproduces={ok}")
            all_ok = all_ok and ok
        except Exception as e:
            print(f"    FAIL  {module:<26} error: {e}")
            all_ok = False
    return all_ok


def main():
    print("=" * 64)
    print("vp_wave_computer — completeness & reproduction audit")
    print("=" * 64)
    missing = check_files()
    sc = check_self_contained()
    repro = check_reproduction()
    print("-" * 64)
    files_ok = (len(missing) == 0)
    verdict = files_ok and sc and repro
    print(f"files_present        : {'PASS' if files_ok else 'FAIL (missing: %s)' % missing}")
    print(f"self_contained       : {'PASS' if sc else 'FAIL'}")
    print(f"reproduces_bitforbit : {'PASS' if repro else 'FAIL'}")
    print(f"\nAUDIT: {'PASS — package whole, self-contained, reproducing' if verdict else 'FAIL — fix before new work'}")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
