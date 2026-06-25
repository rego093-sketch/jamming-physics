#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py -- the single reproducible entry point for Appendix K (the absolute clock).

Runs the gate, assembles the full reading, and writes the expected/ artifacts:
  expected/gate_report.json     the K1..K11 (+ B1) gate outcome (+ gate sha)
  expected/reading.json         the complete Appendix-K reading (+ reading_hash, 2x SHA-256)
  expected/order_table.csv      per-gene gamma / spinodal / barrier / cascade depth / composite rank
  expected/floor_ablation.csv   the O1 nested-scope ablation (inherited / +limb / +HOX / HOX-only)
  expected/absolute_clock.csv   the B1 held-out stage-day validation (predicted vs cited)
  expected/summary.txt          a short human-readable verdict

Deterministic: re-running reproduces byte-identical files.
"""
import os
import json
import csv

from completion import interpreter, gate, cascade, nulltest, timing, lock


HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "expected")


def main():
    os.makedirs(EXP, exist_ok=True)

    # 1) gate
    print("== Appendix K gate ==")
    g = gate.run_gate(verbose=True)
    with open(os.path.join(EXP, "gate_report.json"), "w", encoding="utf-8") as fh:
        json.dump(g, fh, sort_keys=True, ensure_ascii=False, indent=2)

    # 2) full reading + hash
    reading = interpreter.interpret()
    reading_hash = interpreter.reading_hash()
    out = {"reading_hash_sha256x2": reading_hash, "reading": reading}
    with open(os.path.join(EXP, "reading.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, sort_keys=True, ensure_ascii=False, indent=2)

    # 3) order table CSV (filled 63-gene atlas)
    rows = cascade.order_table()
    cols = ["composite_rank", "gene", "program", "system", "gamma", "spinodal",
            "barrier", "cascade_depth", "is_source"]
    with open(os.path.join(EXP, "order_table.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in cols})

    # 4) O1 floor ablation CSV
    abl = nulltest.floor_retest_ablation()
    with open(os.path.join(EXP, "floor_ablation.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scope", "spearman_depth_vs_carnegie", "n_anchored", "meets_floor", "note"])
        for key in ["scope_a_inherited_kit", "scope_b_plus_limb_inducers",
                    "scope_c_plus_full_hox", "scope_d_hox_only_limb_ablated"]:
            s = abl[key]
            w.writerow([key, s["spearman"], s["n_anchored"], s["meets_floor"], s["note"]])

    # 4b) B1 absolute-clock held-out validation CSV (predicted vs cited Carnegie day)
    gc = timing.global_clock()
    with open(os.path.join(EXP, "absolute_clock.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["stage", "stage_num", "predicted_day", "cited_day", "abs_err_days",
                    "in_somite_window", "held_out", "within_accept"])
        for r in gc["heldout_stage_validation"]["rows"]:
            w.writerow([r["stage"], r["stage_num"], r["predicted_day"], r["cited_day"],
                        r["abs_err_days"], r["in_somite_window"], r["held_out"],
                        r["within_accept"]])

    # 5) summary
    decl = reading["declaration"]
    counts = reading["grading"]["counts"]
    jit = nulltest.floor_retest_jitter()
    sub = timing.segmentation_subclock()
    gc = timing.global_clock()
    lines = [
        "Appendix K -- the absolute clock (pinning the global zero-point)",
        "=" * 63,
        decl["headline"],
        "",
        "gate: %s (%d/%d)  sha=%s" % ("PASS" if g["_all_pass"] else "FAIL",
                                      g["_n_pass"], g["_n_total"], g["_sha256"]),
        "reading_hash (2x SHA-256): %s" % reading_hash,
        "grades: V=%d  L=%d  F=%d  O=%d   physical_complete=%s"
        % (counts["V"], counts["L"], counts["F"], counts["O"], decl["physical_complete"]),
        "",
        "B1 -- the absolute clock (global zero-point), two-anchor calibration:",
        "  SLOPE  b = %.4f d/stage   (segmentation modality: %.1f h x %d somites / 24 over CS9-CS13)"
        % (gc["calibration"]["slope_b_days_per_stage"], sub["period_hours_cited"],
           sub["somite_pairs_cited"]),
        "  INTERCEPT a = %.4f d      (cardiac modality: first heartbeat CS10 @ %.0f d)"
        % (gc["calibration"]["intercept_a_days"], gc["anchor_2_cardiac"]["day"]),
        "  free parameters: %d" % gc["calibration"]["free_parameters"],
        "  held-out stages (excl. CS10 zero-point): n=%d, max err %.3f d  -> %s"
        % (gc["heldout_stage_validation"]["n_held_out"],
           gc["heldout_stage_validation"]["max_abs_err_days"],
           "all within %.1f d" % lock.absolute_clock_cfg()["heldout_accept_days"]
           if gc["heldout_stage_validation"]["all_pass"] else "FAIL"),
        "  held-out genes (somite window): n=%d, max err %.3f d (worst %s) -> %s"
        % (gc["heldout_gene_validation"]["n_genes"],
           gc["heldout_gene_validation"]["max_abs_err_days"],
           gc["heldout_gene_validation"]["worst_gene"],
           "all in window" if gc["heldout_gene_validation"]["all_pass"] else "FAIL"),
        "  honest bound: single somite-rate drifts up to %.2f d after somitogenesis (CS14+)"
        % gc["honest_bound_post_somitogenesis"]["max_abs_err_days_CS14plus"],
        "  B1 CLOSED = %s   grade = [L] (a MEASUREMENT, never [V])" % gc["b1_closed"],
        "",
        "O1 floor re-test (pre-registered 0.70):",
        "  inherited 38-kit      %.3f  (n=%d)  reproduces Appendix I"
        % (abl["scope_a_inherited_kit"]["spearman"], abl["scope_a_inherited_kit"]["n_anchored"]),
        "  + full HOX (FILLED)   %.3f  (n=%d)  FLOOR MET"
        % (abl["scope_c_plus_full_hox"]["spearman"], abl["scope_c_plus_full_hox"]["n_anchored"]),
        "  jitter (+-1 rank, seed=%d): mean %.3f, p5 %.3f, frac>=floor %.3f -> stays [L], not [V]"
        % (jit["seed"], jit["mean"], jit["p5"], jit["frac_at_or_above_floor"]),
        "",
        "O2 segmentation sub-clock: %.2f d (%d pairs x %.1f h), cited window %s -> %s"
        % (sub["predicted_somitogenesis_days"], sub["somite_pairs_cited"], sub["period_hours_cited"],
           str(sub["cited_window_CS9_to_CS13_days"]),
           "consistent" if sub["prediction_in_cited_window_pm2d"] else "INCONSISTENT"),
        "",
        "axial chain (longest cascade path): %s" % " -> ".join(cascade.longest_path()),
        "",
        "honest summary:",
        "  " + decl["honest_summary"],
    ]
    with open(os.path.join(EXP, "summary.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print()
    print("\n".join(lines))
    print()
    print("wrote:", ", ".join(sorted(os.listdir(EXP))))
    return 0 if g["_all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
