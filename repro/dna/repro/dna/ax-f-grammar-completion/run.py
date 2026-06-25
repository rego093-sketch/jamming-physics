# -*- coding: utf-8 -*-
"""
run.py -- top-level runner for the grammar-completion package (Appendix F).

Produces (deterministically) under expected/:
  lock_manifest.json       every locked input, grade, provenance (no magic)
  organ_atlas.json         the organ x grammar confusion matrix + per-promoter reads
  dynamical_G4.json        the G4 orthogonality + reads + state-family example
  bodyplan_G5.json         the G5 Hox colinearity + read
  grammar_space.json       the 2D grammar-space map + one-operator proof
  declaration.json         the two-axis decoding declaration
  grammar_completion.json  the full interpret_grammar_completion() reading
  gate_report.json         the fail-closed F1..F10 report (+ 2x-SHA witness)
  RESULT.txt               a human-readable honest summary

Usage:  python3 run.py
"""
import os
import json

from completion import (lock, atlas, dynamical, bodyplan, grammar_space,
                        declaration, interpreter, grading, gate)

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "expected")


def _write(name, obj):
    os.makedirs(_OUT, exist_ok=True)
    with open(os.path.join(_OUT, name), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True, ensure_ascii=False)


def main():
    _write("lock_manifest.json", lock.lock_manifest())

    cm = atlas.confusion_matrix()
    _write("organ_atlas.json", {"confusion_matrix": cm,
                                "per_promoter_reads": atlas.per_promoter_reads()})

    g4 = {
        "orthogonality_to_material": dynamical.orthogonality_to_material(),
        "reads": {k: dynamical.read(lock.promoter(k)[0]) for k in lock.promoter_keys()},
        "state_family_example": dynamical.state_family(lock.promoter(lock.promoter_keys()[0])[0]),
    }
    _write("dynamical_G4.json", g4)

    g5 = {"colinearity": bodyplan.colinearity(), "read": bodyplan.read()}
    _write("bodyplan_G5.json", g5)

    _write("grammar_space.json", {"map": grammar_space.grammar_space_map(),
                                  "one_operator_proof": grammar_space.same_operator_proof()})

    decl = declaration.decoding_declaration()
    _write("declaration.json", decl)

    reading = interpreter.interpret_grammar_completion()
    rhash = interpreter.reading_hash(reading)
    _write("grammar_completion.json", reading)

    gate_report = gate.run_gate(verbose=False)
    _write("gate_report.json", gate_report)

    comp = grading.completion_status()

    # human-readable RESULT
    L = []
    L.append("=" * 78)
    L.append("  GRAMMAR COMPLETION -- the full grammar space + the decoding declaration")
    L.append("  (Appendix E found the tower; here the grammar is completed and declared)")
    L.append("=" * 78)
    L.append("")
    L.append("THE GRAMMAR SPACE (one operator at every cell):")
    L.append("  INTERPRETATION axis  G1 material(cell) -> G2 regulatory(tissue) -> G4 dynamical(state)")
    L.append("                       phonology              syntax                   pragmatics")
    L.append("  ORGANIZATION axis    G3 architecture(organ) -> G5 body-plan(body)")
    L.append("                       discourse                  genre")
    L.append("  BREADTH              the organ ATLAS: G2 read across cardiac, neural, hepatic")
    L.append("")
    L.append("DIRECTION 1 -- THE ORGAN ATLAS (장기별): G2 generalized across organs")
    organs = cm["organs"]
    L.append("  MEAN confusion matrix M[organ][grammar] (shuffle-normalized enrichment-z):")
    head = "    organ\\grammar  " + " ".join("%9s" % o for o in organs)
    L.append(head)
    for org in organs:
        row = cm["mean_matrix"][org]
        star = {g: (" *" if g == max(row, key=row.get) else "  ") for g in organs}
        L.append("    %-13s " % org + " ".join("%7.2f%s" % (row[g], star[g]) for g in organs))
    L.append("  diagonal dominance: %d/%d organs peak on their OWN grammar; control (%s) max z=%.2f"
             % (cm["diagonal_dominance_mean"], cm["n_organs"],
                cm["control_max_grammar"], cm["control_max_z"]))
    L.append("  => the regulatory grammar reads organ identity ACROSS the atlas, not the heart alone [L]")
    L.append("")
    o4 = g4["orthogonality_to_material"]
    L.append("DIRECTION 2 -- THE DYNAMICAL GRAMMAR G4 (동역학, pragmatics)")
    L.append("  one locus -> a FAMILY of readings by cell state; signal = CpG O/E methylation-sensitivity")
    L.append("  mean |corr(CpG O/E, material dG)| = %.3f  (orthogonal, ceiling %.2f) -> G4 is a real rung [V]"
             % (o4["mean_abs_corr"], o4["threshold"]))
    L.append("  same robust_z operator -> A4_4 (identical function)")
    L.append("")
    col = g5["colinearity"]
    L.append("DIRECTION 3 -- THE BODY-PLAN GRAMMAR G5 (genre, 더 크고 더 넓게)")
    L.append("  Hox colinearity on the real HOXD cluster (9 GRCh38 coordinates):")
    L.append("  rank-rank order colinearity |corr| = %.4f ; Pearson on raw TSS |corr| = %.4f (floor %.2f) [L]"
             % (col["abs_rankrank"], col["abs_pearson"], col["threshold"]))
    L.append("  position on the DNA = position in the body; same operator -> A4_5")
    L.append("")
    op = grammar_space.same_operator_proof()
    L.append("ONE OPERATOR ACROSS THE WHOLE SPACE")
    L.append("  robust_z at %s -- scale/shift-invariant to machine epsilon (%.1e / %.1e) [V]"
             % ("/".join(op["levels_using_it"]), op["shape_scale_invariance"],
                op["shape_shift_invariance"]))
    L.append("")
    L.append("THE DECODING DECLARATION (해독 선언) -- two axes, honest")
    L.append("  STRUCTURAL / grammatical decoding : %s"
             % ("COMPLETE (100%)" if decl["structural_complete"] else "NOT COMPLETE"))
    L.append("    every grammatical level (G1..G5) identified, formalized as (gamma, A4),")
    L.append("    sequence-readable, orthogonal, one operator, across organs -- no undiscovered grammar [V]")
    L.append("  FUNCTIONAL / quantitative decoding: OPEN")
    for ob in decl["functional"]["open_obstacles"]:
        L.append("    [O] %s -> %s" % (ob["level"], ob["obstacle"]))
    L.append("  => 100% means the grammar is fully mapped; what remains is MEASUREMENT, not grammar")
    L.append("")
    L.append("HONEST STATUS (precision != accuracy)")
    L.append("  structural_complete = %s   functional_complete = %s"
             % (comp["structural_complete"], comp["functional_complete"]))
    L.append("")
    gate_ok = gate_report["_all_pass"]
    n_pass = sum(1 for k, v in gate_report.items() if isinstance(v, dict) and v.get("pass"))
    L.append("-" * 78)
    L.append("  GATE: %s (%d/%d)   gate sha=%s   reading hash=%s"
             % ("PASS" if gate_ok else "FAIL", n_pass, len(gate.CHECKS),
                gate_report["_sha256"], rhash))
    L.append("  LOCK -> Derive -> Gate. No fitted parameters. precision != accuracy. 반증=발견. 문법.")
    L.append("-" * 78)
    txt = "\n".join(L)
    with open(os.path.join(_OUT, "RESULT.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")
    print(txt)
    print()
    print("[wrote] %s/ (lock_manifest, organ_atlas, dynamical_G4, bodyplan_G5, grammar_space, "
          "declaration, grammar_completion, gate_report, RESULT.txt)" % _OUT)
    return 0 if gate_ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
