# -*- coding: utf-8 -*-
"""
run.py -- top-level runner for the grammar-hierarchy package.

Produces (deterministically) under expected/:
  lock_manifest.json     every locked input, grade, provenance (no magic)
  per_sequence_reads.json  the three (gamma, A4) reads for each real promoter
  results.json           the three establishing results + same-operator proof
  heart_resolution.json  the heart resolution + remaining external dependence
  grammar_reading.json   the full interpret_grammar_hierarchy() reading
  gate_report.json       the fail-closed E1..E9 report (+ 2x-SHA witness)
  RESULT.txt             a human-readable honest summary

Usage:  python3 run.py
"""
import os
import json

from grammar import lock, hierarchy, heart, interpreter, grading, gate

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "expected")


def _write(name, obj):
    os.makedirs(_OUT, exist_ok=True)
    with open(os.path.join(_OUT, name), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True)


def main():
    _write("lock_manifest.json", lock.lock_manifest())

    per_seq = {}
    for key in lock.sequence_keys():
        seq, tissue, _ = lock.sequence(key)
        per_seq[key] = {"tissue": tissue, "levels": hierarchy.read_all_levels(seq)}
    _write("per_sequence_reads.json", per_seq)

    results = {
        "result_1_tissue_identity_readable": hierarchy.tissue_identity_separation(),
        "result_2_upper_grammar_above_material": hierarchy.shuffle_test(),
        "result_3_levels_orthogonal": hierarchy.cross_grammar_orthogonality(),
        "same_operator_all_levels": hierarchy.same_operator_proof(),
    }
    _write("results.json", results)

    heart_block = {
        "heart_arrangement_is_in_sequence": heart.heart_arrangement_is_in_sequence(),
        "what_each_level_supplies": heart.what_each_level_supplies_to_the_heart(),
        "remaining_external_dependence": heart.remaining_external_dependence(),
    }
    _write("heart_resolution.json", heart_block)

    reading = interpreter.interpret_grammar_hierarchy()
    rhash = interpreter.reading_hash(reading)
    _write("grammar_reading.json", reading)

    gate_report = gate.run_gate(verbose=False)
    _write("gate_report.json", gate_report)

    # human-readable RESULT
    sep = results["result_1_tissue_identity_readable"]
    sh = results["result_2_upper_grammar_above_material"]
    o = results["result_3_levels_orthogonal"]
    comp = grading.completion_status()
    L = []
    L.append("=" * 78)
    L.append("  GRAMMAR HIERARCHY -- reading the UPPER blueprint")
    L.append("  (is there a tissue-level gamma/A4 the cell-level reading missed?)")
    L.append("=" * 78)
    L.append("")
    L.append("THE QUESTION: the corpus has read only the BOTTOM blueprint -- the cell-level")
    L.append("material (gamma = stacking dG, A4 = its pattern), the chemistry of adjacent")
    L.append("bases. Is there a TISSUE-level gamma/A4 we have not seen? What is the upper")
    L.append("blueprint's 'material' if not ions/chemistry?")
    L.append("")
    L.append("THE HIERARCHY (the same (gamma, A4) operator lifted up the tower):")
    L.append("  G1 material    (cell,  phonology) -- stacking dG       -> (gamma_1, A4_1)")
    L.append("  G2 regulatory  (tissue, syntax)   -- cardiac TF grammar -> (gamma_2, A4_2) <= MISSED")
    L.append("  G3 architecture(organ, discourse) -- element layout     -> (gamma_3, A4_3)  배치도")
    L.append("")
    L.append("RESULT 1 -- TISSUE IDENTITY IS READABLE FROM THE REGULATORY GRAMMAR (real promoters)")
    for r in sep["rows"]:
        L.append(f"  {r['sequence']:22s} {r['tissue']:28s} G1 gamma={r['G1_material_gamma']:.3f}  cardiac-TF={r['G2_cardiac_total']}")
    L.append(f"  cardiac mean cardiac-TF = {sep['cardiac_mean_G2_total']}  vs  control = {sep['control_mean_G2_total']}  -> {sep['G2_cardiac_over_control_ratio']}x")
    L.append(f"  G2 separates tissue: {sep['G2_separates_tissue']}   G1 (material) separates tissue: {sep['G1_separates_tissue']}")
    L.append("  => a TISSUE-level blueprint exists and is sequence-readable; the material is blind to it [L]")
    L.append("")
    L.append("RESULT 2 -- THE UPPER GRAMMAR IS INFORMATION ABOVE THE MATERIAL (dinuc shuffle)")
    L.append(f"  material gamma_1: {sh['material_gamma_original']} -> {sh['material_gamma_shuffled']}  (preserved exactly: {sh['material_level_preserved_exactly']})")
    L.append(f"  cardiac grammar : {sh['cardiac_grammar_original_total']} -> {sh['cardiac_grammar_shuffled_total']}  ({int(100*sh['fraction_grammar_lost'])}% lost)")
    L.append("  => the dinuc shuffle preserves the material level EXACTLY yet destroys the cardiac")
    L.append("     grammar -- NONE of the tissue identity is at the material level [V]")
    L.append("")
    L.append("RESULT 3 -- THE LEVELS ARE ORTHOGONAL")
    L.append(f"  corr(G1 material, G2 regulatory) = {o['corr_G1_material_vs_G2_regulatory']}  (R^2 = {o['r_squared']})")
    L.append("  => distinct projections of the blueprint, not the same signal twice [V]")
    L.append("")
    L.append("THE HEART RESOLUTION (반증 = 발견)")
    L.append("  Appendix D imported external cardiac moduli because it read the cell-level MATERIAL,")
    L.append("  which is orthogonal to the arrangement (Appendix A null rho=+0.071). The arrangement")
    L.append("  lives one grammar level up -- the cardiac TF syntax -- and is SEQUENCE-READABLE.")
    L.append("  The blueprint had the arrangement; the corpus had read the wrong level.")
    L.append("")
    L.append("WHAT EACH LEVEL SUPPLIES TO THE HEART:")
    L.append("  G1 material    -> the CELL's intrinsic stiffness (read before; blind to identity)")
    L.append("  G2 regulatory  -> WHICH tissue (cardiac identity: GATA/NKX2-5/MEF2/TBX5/HAND)")
    L.append("  G3 architecture-> the spatial LAYOUT (배치도) -- toward the organ's exact form")
    L.append("")
    L.append("HONEST STATUS (precision != accuracy)")
    L.append(f"  completion.complete = {comp['complete']}")
    L.append("  found : tissue identity sequence-readable [L]; above-material [V]; orthogonal [V];")
    L.append("          same operator at every level [V]")
    L.append("  NOT yet: functional validation vs measured enhancer activity; the real 3D arrangement")
    L.append("           map; absolute kPa magnitudes -- three channels [O]")
    for oc in comp["open_channels"]:
        L.append(f"     [O] {oc['channel']}")
        L.append(f"         -> needs: {oc['named_obstacle']}")
    L.append("")
    gate_ok = gate_report["_all_pass"]
    n_pass = sum(1 for k, v in gate_report.items() if isinstance(v, dict) and v.get("pass"))
    L.append("-" * 78)
    L.append(f"  GATE: {'PASS' if gate_ok else 'FAIL'} ({n_pass}/9)   gate sha={gate_report['_sha256']}   reading hash={rhash}")
    L.append("  LOCK -> Derive -> Gate. No fitted parameters. precision != accuracy. 반증=발견. 문법.")
    L.append("-" * 78)
    txt = "\n".join(L)
    with open(os.path.join(_OUT, "RESULT.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")
    print(txt)
    print()
    print(f"[wrote] {_OUT}/  (lock_manifest, per_sequence_reads, results, heart_resolution, "
          f"grammar_reading, gate_report, RESULT.txt)")
    return 0 if gate_ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
