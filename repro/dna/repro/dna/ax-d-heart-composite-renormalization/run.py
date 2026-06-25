# -*- coding: utf-8 -*-
"""
run.py -- top-level runner for the heart composite-renormalization accuracy package.

Produces (deterministically) under expected/:
  lock_manifest.json        every measured cardiac input, grade, provenance (no magic)
  two_phase_bracket.json    the exact bracket + containment of the measured tissue
  trajectory.json           the predicted composition-flow trajectory + span check
  decomposition.json        the three parameter-free results (A falsification, B null, C consistency)
  heart_reading.json        the full interpret_heart() reading
  gate_report.json          the fail-closed D1..D9 report (+ 2x-SHA witness)
  RESULT.txt                a human-readable honest summary

Usage:  python3 run.py
"""
import os
import json
import hashlib

from heart import lock, composite, trajectory, decomposition, interpreter, grading, gate

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "expected")


def _write(name, obj):
    os.makedirs(_OUT, exist_ok=True)
    path = os.path.join(_OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True)
    return path


def main():
    # 1) lock manifest
    man = lock.lock_manifest()
    _write("lock_manifest.json", man)

    # 2) two-phase bracket + containment
    B_cell, _, _ = lock.cell_adult_kpa()
    B_ecm_lv, _, _ = lock.ecm_lv_kpa()
    phi_cell, _, _ = lock.phi_cell_adult()
    adult, _, _ = lock.target_adult_rat_kpa()
    bracket_block = {
        "bracket_adult_LV_inputs": composite.bracket(B_cell, B_ecm_lv, phi_cell),
        "contains_measured_adult": composite.contains(B_cell, B_ecm_lv, phi_cell, adult),
    }
    _write("two_phase_bracket.json", bracket_block)

    # 3) trajectory
    traj_block = {
        "predicted_trajectory_table": trajectory.predicted_trajectory_table(11),
        "spans_measured_range": trajectory.trajectory_spans_measured(),
        "measured_endpoints": trajectory.measured_endpoints(),
    }
    _write("trajectory.json", traj_block)

    # 4) decomposition (the three parameter-free results)
    decomp_block = {
        "RESULT_A_jamming_insufficiency": decomposition.jamming_insufficiency(),
        "RESULT_B_gamma_orthogonality": decomposition.gamma_orthogonality(),
        "RESULT_C_bracket_consistency": decomposition.bracket_consistency(),
        "axis_identification": decomposition.axis_identification(),
    }
    _write("decomposition.json", decomp_block)

    # 5) full reading
    reading = interpreter.interpret_heart()
    rhash = interpreter.reading_hash(reading)
    _write("heart_reading.json", reading)

    # 6) gate
    gate_report = gate.run_gate(verbose=False)
    _write("gate_report.json", gate_report)

    # 7) human-readable RESULT
    A = decomp_block["RESULT_A_jamming_insufficiency"]
    B = decomp_block["RESULT_B_gamma_orthogonality"]
    C = decomp_block["RESULT_C_bracket_consistency"]
    span = traj_block["spans_measured_range"]
    comp = grading.completion_status()
    lines = []
    lines.append("=" * 78)
    lines.append("  HEART COMPOSITE-RENORMALIZATION -- ACCURACY RESULT")
    lines.append("  (challenging the heart that 'failed' in Appendix A)")
    lines.append("=" * 78)
    lines.append("")
    lines.append("THE QUESTION: what sets the heart's developmental stiffening")
    lines.append("  measured: 0.1 + 0.3*day kPa (chick); E2 <1 -> E14 ~10 kPa; adult 10-50 kPa")
    lines.append("  -- the sequence material gamma? pure cell-jamming? or ECM composition?")
    lines.append("")
    lines.append("RESULT A -- PURE CELL-JAMMING IS INSUFFICIENT (falsification, parameter-free)")
    lines.append(f"  embryonic cell modulus      : {A['embryonic_cell_modulus_kpa']} kPa")
    lines.append(f"  pure-jamming ceiling        : {A['pure_jamming_ceiling_kpa']} kPa (<= cell modulus)")
    lines.append(f"  measured E14 tissue         : {A['measured_E14_tissue_kpa']} kPa")
    lines.append(f"  rise factor (ceiling->E14)  : {A['rise_factor_ceiling_to_E14']}x  >> 1")
    lines.append(f"  => pure jamming insufficient : {A['pure_cell_jamming_insufficient']}")
    lines.append(f"     the stiff ECM phase / cell maturation is NECESSARY  [V]")
    lines.append("")
    lines.append("RESULT B -- GAMMA IS ORTHOGONAL TO THE STIFFENING (explains the null)")
    lines.append(f"  gamma time-invariant        : {B['gamma_time_invariant']} (sequence-fixed)")
    lines.append(f"  Appendix A heart null       : rho={B['appendix_a_heart_null_rho']}, p={B['appendix_a_heart_null_p']}")
    lines.append(f"  reproduces & explains null  : {B['reproduces_and_explains_null']}  [V]+[L]")
    lines.append("     a constant cannot encode a rising trajectory; the timing axis is")
    lines.append("     COMPOSITION (ECM), orthogonal to the material gamma")
    lines.append("")
    lines.append("RESULT C -- EXACT TWO-PHASE BRACKET CONTAINS THE MEASURED TISSUE (consistency)")
    lines.append(f"  ventricular LV bracket      : {C['ventricular_LV_bracket_kpa']} kPa")
    lines.append(f"  measured adult tissue       : {C['measured_adult_tissue_kpa']} kPa")
    lines.append(f"  contained (LV ECM)          : {C['contained_with_LV_ECM']}  [L]")
    lines.append(f"  note                        : measured tissue sits low in bracket")
    lines.append(f"                                (isolated cells stiffer than bulk)")
    lines.append("")
    lines.append("COMPOSITION-FLOW TRAJECTORY (illustration, [F])")
    lines.append(f"  predicted span              : {span['predicted_start_kpa']} -> {span['predicted_end_kpa']} kPa")
    lines.append(f"  measured embryonic / adult  : {span['measured_embryonic_kpa']} / {span['measured_adult_band_kpa']} kPa")
    lines.append(f"  spans measured range        : {span['spans_measured_range']} (monotone={span['monotone_rising']})")
    lines.append("")
    lines.append("THE DISCOVERY (반증 = 발견)")
    lines.append("  the heart's developmental stiffening is a COMPOSITION + MATURATION flow")
    lines.append("  (ECM collagen deposition + cell jamming), NOT the sequence material gamma.")
    lines.append("  Falsifying pure-jamming and material-gamma REVEALS the right axis -- which")
    lines.append("  is exactly why gamma was orthogonal to heart timing in Appendix A.")
    lines.append("")
    lines.append("HONEST STATUS (precision != accuracy)")
    lines.append(f"  completion.complete         : {comp['complete']}")
    lines.append("  achieved : exact bracket [V], pure-jamming falsified [V], gamma-null")
    lines.append("             explained [V], measured phase moduli [L], bracket-consistency [L]")
    lines.append("  NOT yet  : a TIGHT zero-parameter trajectory prediction (3 channels [O])")
    lines.append(f"  closes with: {comp['distance_to_close']}")
    for oc in comp["open_channels"]:
        lines.append(f"     [O] {oc['channel']}")
        lines.append(f"         -> needs: {oc['named_obstacle']}")
    lines.append("")
    gate_ok = gate_report["_all_pass"]
    n_pass = sum(1 for k, v in gate_report.items()
                 if isinstance(v, dict) and v.get("pass"))
    lines.append("-" * 78)
    lines.append(f"  GATE: {'PASS' if gate_ok else 'FAIL'} ({n_pass}/9)   "
                 f"gate sha={gate_report['_sha256']}   reading hash={rhash}")
    lines.append("  LOCK -> Derive -> Gate. No fitted parameters. precision != accuracy. 반증=발견.")
    lines.append("-" * 78)
    txt = "\n".join(lines)
    with open(os.path.join(_OUT, "RESULT.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")
    print(txt)
    print()
    print(f"[wrote] {_OUT}/  (lock_manifest, two_phase_bracket, trajectory, "
          f"decomposition, heart_reading, gate_report, RESULT.txt)")
    return 0 if gate_ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
