# -*- coding: utf-8 -*-
"""
run.py -- top-level runner for the tissue-level DUAL interpreter (이원화).

Produces, deterministically:

  expected/tissue_reading.json        the dual reading at the reference domain
  expected/developmental_run.json     LEVEL(size) & SHAPE(form) across dev time
  expected/lock_manifest.json         every constant + grade + provenance
  expected/gate_report.json           the fail-closed gate result (G1..G7)
  expected/RESULT.txt                 a human-readable one-screen summary

Run:  python3 run.py    (from the chapter root)

This script does no physics of its own; it only calls the locked, exact
modules under tissue/ and serializes their output. Every number it prints is
reproduced from a closed form whose constants are LOCKed from param_db.json.
"""
import os
import sys
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from tissue import (
    lock, interpreter, grading,
)
from tissue.gate import run_gate

EXP = os.path.join(HERE, "expected")
os.makedirs(EXP, exist_ok=True)

REF_L_UM = 360.0   # reference domain = 6*lambda at lambda=60 um (deep tissue)
DEV_TIMES = (1.0, 1.5, 2.0, 3.0)


def _dump(name, obj):
    path = os.path.join(EXP, name)
    blob = json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(blob + "\n")
    sha = hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
    return path, sha


def main():
    print("=" * 78)
    print("  VP DNA  —  TISSUE-LEVEL DUAL INTERPRETER  (이원화 / dualized)")
    print("=" * 78)

    lam = lock.lambda_um()
    print(f"  intrinsic length   lambda = sqrt(D*tau) = {lam:.6f} um   [L]-grounded")
    print(f"  morphogen field    D*lap(c) - c/tau + source = 0   (screened-Poisson)")
    print(f"  planar closed form c(x) = cosh((L-x)/lambda)/cosh(L/lambda)")
    print()

    # --- the dual reading -------------------------------------------------
    reading = interpreter.interpret_tissue(REF_L_UM)
    rh = interpreter.reading_hash(reading)

    lvl = reading["LEVEL_channel_size"]
    shp = reading["SHAPE_channel_form"]

    print(f"  domain L = {REF_L_UM:.1f} um")
    print("  " + "-" * 74)
    print("  LEVEL  =  mean(c)        ->  SIZE   (the size channel; cell-level gamma)")
    print(f"           level_mean   = {lvl['level_mean']:.8f}")
    print(f"           size_budget  = {lvl['size_budget']:.6f} um   "
          f"[{lvl['grade_value']}]")
    print(f"           closed form  = {lvl['closed_form']}")
    print(f"           vs real mass : {lvl['grade_size_vs_real_mass']}")
    print("  " + "-" * 74)
    print("  SHAPE  =  robust_z(c)    ->  FORM   (the territory channel; cell-level A4)")
    print(f"           n_territories     = {shp['n_territories']}")
    print(f"           apical_width_um   = {shp['apical_width_um']:.6f}")
    print(f"           apical_axial_frac = {shp['apical_axial_frac']:.6f}   "
          f"[{shp['grade_form']}]")
    bnds = ", ".join(f"{b:.3f}" for b in shp["territory_boundaries_um"])
    print(f"           boundaries (um)   = [{bnds}]")
    print(f"           closed form       = {shp['closed_form']}")
    print(f"           vs real anatomy   : {shp['grade_form_vs_real_anatomy']}")
    print("  " + "-" * 74)
    ortho = reading["orthogonality"]
    print(f"  LEVEL ⟂ SHAPE : orthogonal={ortho['orthogonal']}  "
          f"[{ortho['grade']}]")
    print(f"                  {ortho['two_knob_test']['verdict']}")
    print(f"  reading hash  : {rh}")
    print()

    # --- developmental trajectory ----------------------------------------
    dev = interpreter.developmental_run(DEV_TIMES)

    # --- serialize everything --------------------------------------------
    p1, s1 = _dump("tissue_reading.json", reading)
    p2, s2 = _dump("developmental_run.json", dev)
    p3, s3 = _dump("lock_manifest.json", lock.lock_manifest())

    gate = run_gate(verbose=False)
    p4, s4 = _dump("gate_report.json", gate)

    status = grading.completion_status()

    # --- human-readable result -------------------------------------------
    lines = []
    lines.append("VP DNA — TISSUE-LEVEL DUAL INTERPRETER — RESULT")
    lines.append("=" * 62)
    lines.append("")
    lines.append("ONE morphogen field, TWO orthogonal projections:")
    lines.append("")
    lines.append("  LEVEL = mean(c)      -> SIZE   (cell-level gamma, lifted)")
    lines.append(f"      size_budget = {lvl['size_budget']:.6f} um   {lvl['grade_value']}")
    lines.append(f"      vs real mass: {lvl['grade_size_vs_real_mass']}")
    lines.append("")
    lines.append("  SHAPE = robust_z(c)  -> FORM   (cell-level A4, lifted)")
    lines.append(f"      {shp['n_territories']} territories; apical {shp['apical_width_um']:.3f} um   {shp['grade_form']}")
    lines.append(f"      vs real anatomy: {shp['grade_form_vs_real_anatomy']}")
    lines.append("")
    lines.append(f"  lambda = {lam:.4f} um  [L]   |   LEVEL ⟂ SHAPE exact   |   hash {rh}")
    lines.append("")
    lines.append(f"GATE: {'PASS' if gate['_all_pass'] else 'FAIL'} "
                 f"({sum(1 for k,v in gate.items() if isinstance(v,dict) and v.get('pass'))}"
                 f"/7)  sha={gate['_sha256']}")
    lines.append("")
    lines.append(f"COMPLETION: complete = {status['complete']}  (precision earned, accuracy not yet claimed)")
    for ch in status["open_channels"]:
        lines.append(f"  [O] {ch['channel']}")
        lines.append(f"      obstacle: {ch['named_obstacle']}")
    lines.append("")
    lines.append("precision (정밀) ≠ accuracy (정확).  반증 = 발견.")
    txt = "\n".join(lines)
    with open(os.path.join(EXP, "RESULT.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")

    print("  wrote:")
    for nm, sha in [("tissue_reading.json", s1),
                    ("developmental_run.json", s2),
                    ("lock_manifest.json", s3),
                    ("gate_report.json", s4)]:
        print(f"    expected/{nm:28s} sha={sha}")
    print(f"    expected/RESULT.txt")
    print()
    print(f"  GATE {'PASS' if gate['_all_pass'] else 'FAIL'}  "
          f"completion.complete={status['complete']}")
    return 0 if gate["_all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
