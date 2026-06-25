# -*- coding: utf-8 -*-
"""
run.py -- top-level runner for the HIERARCHICAL scale-renormalization interpreter.

Produces, deterministically:

  expected/hierarchy_reading.json     the full reading (classification + climb +
                                      LEVEL/SHAPE dual + orthogonality + grades)
  expected/renormalization_climb.json the per-level (B, rho, c) trajectory up the tower
  expected/scale_classification.json  every channel tagged to its structural level
  expected/lock_manifest.json         every constant + grade + provenance
  expected/gate_report.json           the fail-closed gate result (H1..H9)
  expected/RESULT.txt                 a human-readable one-screen summary

Run:  python3 run.py    (from the chapter root)

This script does no physics of its own; it only calls the locked, exact modules
under hierarchy/ and serializes their output. Every number it prints is reproduced
from a closed form / exact theorem whose constants are LOCKed from param_db.json.
"""
import os
import sys
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from hierarchy import (
    lock, interpreter, ladder, classify, grading,
)
from hierarchy.gate import run_gate

EXP = os.path.join(HERE, "expected")
os.makedirs(EXP, exist_ok=True)


def _dump(name, obj):
    path = os.path.join(EXP, name)
    blob = json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(blob + "\n")
    sha = hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
    return path, sha


def main():
    print("=" * 78)
    print("  VP DNA  —  HIERARCHICAL SCALE-RENORMALIZATION INTERPRETER")
    print("=" * 78)

    pc, _, _ = lock.phi_c()
    zi, _, _ = lock.z_isostatic()
    print(f"  jamming onset      phi_c = {pc}   [L] (O'Hern 2003, RCP)")
    print(f"  isostatic anchor   z_iso = 2d = {zi}   [L] (Maxwell)")
    print(f"  renormalization R  rho'=phi*rho ; B'=phi*B*J(phi) in [0, phi*B] ; "
          f"c'=c*sqrt(J)")
    print(f"  rigidity onset     J(phi) = sqrt((phi-phi_c)/(1-phi_c))  [L]-grounded")
    print()

    # --- the full hierarchical reading -----------------------------------
    reading = interpreter.interpret_hierarchy()
    rh = interpreter.reading_hash(reading)

    climb = reading["renormalization_climb"]
    cls = reading["scale_classification"]
    ortho = reading["orthogonality"]
    comp = reading["rg_composition_associativity"]

    # --- print the classification (the '분류') ---------------------------
    print("  SCALE CLASSIFICATION  (every channel tagged to a tower level)")
    print("  " + "-" * 74)
    for c in cls["channels"]:
        print(f"    [{c['reads_level']:<28s}] {c['channel']}")
    print(f"    levels covered: {', '.join(cls['levels_covered'])}")
    print(f"    coverage_ok = {cls['coverage_ok']}")
    print()

    # --- print the climb (the 'how to go up') ----------------------------
    print("  RENORMALIZATION CLIMB  (each level DERIVED from the one below by R)")
    print("  " + "-" * 74)
    print(f"    {'level':<22s} {'phi':>7s} {'B (Pa)':>14s} "
          f"{'rho':>10s} {'c (m/s)':>12s} {'c/c_prev':>10s}")
    for L in climb["levels"]:
        phi = L.get("phi_used", None)
        sr = L.get("softening_ratio_c_over_prev", None)
        phi_s = f"{phi:.4f}" if phi is not None else "  base"
        sr_s = f"{sr:.6f}" if sr is not None else "   -"
        print(f"    {L['name']:<22s} {phi_s:>7s} {L['B_pa']:>14.4f} "
              f"{L['rho_kg_per_m3']:>10.2f} {L['c_m_per_s']:>12.4f} {sr_s:>10s}")
    print(f"    wave speed monotone decreasing: "
          f"{climb['wave_speed_monotone_decreasing']}   "
          f"(softening ratio per rung = sqrt(J), EXACT [V])")
    print(f"    NOTE: absolute moduli per real level are [O] "
          f"(needs measured elastography/AFM atlas)")
    print()

    # --- LEVEL/SHAPE dual + orthogonality --------------------------------
    lvl = reading["LEVEL_channel_stiffness_size"]
    shp = reading["SHAPE_channel_stiffness_pattern"]
    print("  MECHANICAL LEVEL / SHAPE  (the cell gamma/A4 split, at the tissue scale)")
    print("  " + "-" * 74)
    print(f"    LEVEL = mean(B(x))     -> effective modulus "
          f"{lvl['level_effective_modulus_pa']:.4f} Pa   {lvl['grade_value']}")
    print(f"    SHAPE = robust_z(B(x)) -> {shp['n_anchors']} stiffness anchors; "
          f"z in [{shp['shape_z_min']:.3f}, {shp['shape_z_max']:.3f}]   "
          f"{shp['grade_form']}")
    print(f"    LEVEL ⟂ SHAPE : orthogonal={ortho['orthogonal']}   "
          f"R composes={comp['composes_exactly']}")
    print(f"    reading hash  : {rh}")
    print()

    # --- serialize everything --------------------------------------------
    p1, s1 = _dump("hierarchy_reading.json", reading)
    p2, s2 = _dump("renormalization_climb.json", interpreter.renormalization_demo())
    p3, s3 = _dump("scale_classification.json",
                   {"tower_levels": cls["tower_levels"],
                    "channels": classify.classification_table(),
                    "levels_covered": classify.levels_covered(),
                    "coverage_ok": classify.coverage_ok()})
    p4, s4 = _dump("lock_manifest.json", lock.lock_manifest())

    gate = run_gate(verbose=False)
    p5, s5 = _dump("gate_report.json", gate)

    status = grading.completion_status()

    # --- human-readable result -------------------------------------------
    lines = []
    lines.append("VP DNA — HIERARCHICAL SCALE-RENORMALIZATION INTERPRETER — RESULT")
    lines.append("=" * 64)
    lines.append("")
    lines.append("THE OVER-SIMPLIFICATION REPAIRED:")
    lines.append("  Appendix B used two scales, unconnected, chemical axis only.")
    lines.append("  Here: every channel is CLASSIFIED by structural level, and the")
    lines.append("  tower is CLIMBED by the renormalization operator R — each level's")
    lines.append("  stiffness & density DERIVED from the level below by jamming.")
    lines.append("  '세포들이 모이면 그자체로 부피이자 강성이 될것이다.'")
    lines.append("")
    lines.append("THE OPERATOR R  (units (B,rho) packed at fraction phi):")
    lines.append("  rho' = phi*rho                         [V] exact (mass/volume)")
    lines.append("  0 = B_Reuss <= B' <= B_Voigt = phi*B   [V] exact bracket (theorems)")
    lines.append("  B' = phi*B*J(phi),  J in [0,1]         [L]-grounded jamming onset")
    lines.append("  c' = sqrt(B'/rho') = c*sqrt(J)         [V] exact (VP master twice)")
    lines.append("")
    lines.append("  => softening ratio per rung = sqrt(J)  EXACT; c decreases up the tower.")
    lines.append("")
    lines.append("SCALE CLASSIFICATION:  " + ", ".join(cls["levels_covered"]))
    lines.append(f"  coverage_ok = {cls['coverage_ok']}   "
                 f"(every channel tagged to a tower level)")
    lines.append("")
    lines.append("CLIMB (demonstration profile, phi above phi_c each rung):")
    for L in climb["levels"]:
        phi = L.get("phi_used", None)
        phi_s = f"phi={phi:.4f}" if phi is not None else "BASE   "
        lines.append(f"  {L['name']:<22s} {phi_s}  c = {L['c_m_per_s']:.4f} m/s")
    lines.append(f"  monotone softening = {climb['wave_speed_monotone_decreasing']}")
    lines.append("")
    lines.append(f"  LEVEL ⟂ SHAPE exact   |   R composes exact   |   hash {rh}")
    lines.append("")
    lines.append(f"GATE: {'PASS' if gate['_all_pass'] else 'FAIL'} "
                 f"({sum(1 for k,v in gate.items() if isinstance(v,dict) and v.get('pass'))}"
                 f"/9)  sha={gate['_sha256']}")
    lines.append("")
    lines.append(f"COMPLETION: complete = {status['complete']}  "
                 f"(precision earned, accuracy not yet claimed)")
    for ch in status["open_channels"]:
        lines.append(f"  [O] {ch['channel']}")
        lines.append(f"      obstacle: {ch['named_obstacle']}")
    lines.append("")
    lines.append("precision (정밀) ≠ accuracy (정확).  반증 = 발견.")
    txt = "\n".join(lines)
    with open(os.path.join(EXP, "RESULT.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")

    print("  wrote:")
    for nm, sha in [("hierarchy_reading.json", s1),
                    ("renormalization_climb.json", s2),
                    ("scale_classification.json", s3),
                    ("lock_manifest.json", s4),
                    ("gate_report.json", s5)]:
        print(f"    expected/{nm:30s} sha={sha}")
    print(f"    expected/RESULT.txt")
    print()
    print(f"  GATE {'PASS' if gate['_all_pass'] else 'FAIL'}  "
          f"completion.complete={status['complete']}")
    return 0 if gate["_all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
