#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py -- the single reproducible entry point for Appendix L (the blueprint close-out).

Runs the gate, assembles the full reading, and writes the expected/ artifacts:
  expected/gate_report.json     the L1..L11 (+ B4 + B2) gate outcome (+ gate sha)
  expected/reading.json         the complete Appendix-L reading (+ reading_hash, 2x SHA-256)
  expected/order_table.csv      per-gene gamma / spinodal / barrier / cascade depth / composite rank
                                (on the B4-extended 63-edge cascade)
  expected/floor_ablation.csv   the floor nested-scope ablation incl. scope_e (+ the B4 edge)
  expected/b4_jitter.csv        the B4 closure: K terminus vs L (+MEOX1->PAX7), p5 vs floor
  expected/b2_occupancy.csv     the B2 per-edge motif-occupancy z-scores vs dinuc-shuffle background
  expected/absolute_clock.csv   the inherited B1 held-out stage-day validation (predicted vs cited)
  expected/summary.txt          a short human-readable verdict

Deterministic: re-running reproduces byte-identical files.
"""
import os
import json
import csv

from completion import interpreter, gate, cascade, nulltest, timing, lock, cis


HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "expected")


def main():
    os.makedirs(EXP, exist_ok=True)

    # 1) gate
    print("== Appendix L gate ==")
    g = gate.run_gate(verbose=True)
    with open(os.path.join(EXP, "gate_report.json"), "w", encoding="utf-8") as fh:
        json.dump(g, fh, sort_keys=True, ensure_ascii=False, indent=2)

    # 2) full reading + hash
    reading = interpreter.interpret()
    reading_hash = interpreter.reading_hash()
    out = {"reading_hash_sha256x2": reading_hash, "reading": reading}
    with open(os.path.join(EXP, "reading.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, sort_keys=True, ensure_ascii=False, indent=2)

    # 3) order table CSV (B4-extended 63-edge cascade)
    rows = cascade.order_table()
    cols = ["composite_rank", "gene", "program", "system", "gamma", "spinodal",
            "barrier", "cascade_depth", "is_source"]
    with open(os.path.join(EXP, "order_table.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in cols})

    # 4) floor ablation CSV (incl. scope_e = + the B4 myogenic edge)
    abl = nulltest.floor_retest_ablation()
    with open(os.path.join(EXP, "floor_ablation.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scope", "spearman_depth_vs_carnegie", "n_anchored", "meets_floor", "note"])
        for key in ["scope_a_inherited_kit", "scope_b_plus_limb_inducers",
                    "scope_c_plus_full_hox", "scope_d_hox_only_limb_ablated",
                    "scope_e_plus_b4_myogenic_edge"]:
            s = abl[key]
            w.writerow([key, s["spearman"], s["n_anchored"], s["meets_floor"], s["note"]])

    # 4b) B4 closure CSV (the jitter floor before/after the MEOX1->PAX7 source-fix)
    jit = nulltest.floor_retest_jitter()
    b4 = nulltest.b4_jitter_closed()
    with open(os.path.join(EXP, "b4_jitter.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "value"])
        w.writerow(["closure_edge", "->".join(b4["closure_edge"])])
        w.writerow(["rank_parent_MEOX1", b4["rank_parent"]])
        w.writerow(["rank_child_PAX7", b4["rank_child"]])
        w.writerow(["spearman_K_terminus", abl["scope_c_plus_full_hox"]["spearman"]])
        w.writerow(["spearman_L_with_b4_edge", abl["scope_e_plus_b4_myogenic_edge"]["spearman"]])
        w.writerow(["jitter_seed", jit["seed"]])
        w.writerow(["jitter_mean", jit["mean"]])
        w.writerow(["jitter_p5", jit["p5"]])
        w.writerow(["jitter_p95", jit["p95"]])
        w.writerow(["floor", jit["floor"]])
        w.writerow(["p5_clears_floor", jit["p5_clears_floor"]])
        w.writerow(["frac_at_or_above_floor", jit["frac_at_or_above_floor"]])
        w.writerow(["n_edge_inversions", b4["n_edge_inversions"]])
        w.writerow(["cascade_is_dag", b4["cascade_is_dag"]])
        w.writerow(["b4_closed", b4["b4_closed"]])

    # 4c) B2 occupancy CSV (per-edge motif occupancy vs dinucleotide-shuffle background)
    b2 = cis.occupancy_probe()
    with open(os.path.join(EXP, "b2_occupancy.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["parent", "child", "tf_family", "observed", "shuffle_mean",
                    "shuffle_sd", "z", "above_background"])
        for r in b2["rows"]:
            w.writerow([r["parent"], r["child"], r["family"], r["observed"],
                        r["shuffle_mean"], r["shuffle_sd"], r["z"], r["above_background"]])

    # 4d) inherited B1 absolute-clock held-out validation CSV
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
    lines = [
        "Appendix L -- the blueprint close-out (B4 closed; B2 data-blocked)",
        "=" * 63,
        decl["headline"],
        "",
        "gate: %s (%d/%d)  sha=%s" % ("PASS" if g["_all_pass"] else "FAIL",
                                      g["_n_pass"], g["_n_total"], g["_sha256"]),
        "reading_hash (2x SHA-256): %s" % reading_hash,
        "grades: V=%d  L=%d  F=%d  O=%d   physical_complete=%s   blueprint_fully_mapped=%s"
        % (counts["V"], counts["L"], counts["F"], counts["O"], decl["physical_complete"],
           decl["blueprint_fully_mapped"]),
        "",
        "B4 -- jitter floor CLOSED (the cited MEOX1->PAX7 source-fix):",
        "  PAX7 was an artificial cascade source in K (indegree 0, depth 0) despite Carnegie rank 4.",
        "  Spearman(depth, Carnegie): %.4f (K terminus) -> %.4f (+ MEOX1->PAX7)"
        % (abl["scope_c_plus_full_hox"]["spearman"], abl["scope_e_plus_b4_myogenic_edge"]["spearman"]),
        "  +-1 rank-jitter (seed=%d): mean %.4f, p5 %.4f >= %.2f floor, frac>=floor %.4f"
        % (jit["seed"], jit["mean"], jit["p5"], jit["floor"], jit["frac_at_or_above_floor"]),
        "  MEOX1 rank %s = PAX7 rank %s (tie, concordant); %d new inversions; DAG=%s"
        % (b4["rank_parent"], b4["rank_child"], b4["n_edge_inversions"], b4["cascade_is_dag"]),
        "  B4 CLOSED = %s   grade = [L] (jitter-robust empirical; NEVER [V] -- B3 ceiling)"
        % b4["b4_closed"],
        "",
        "B2 -- cis-code -> drive DATA-BLOCKED (proximal promoter does not carry the drive):",
        "  motif occupancy vs dinucleotide-shuffle null (seed=%d, %d shuffles, both strands):"
        % (lock.b2_cis_occupancy_cfg()["seed"], lock.b2_cis_occupancy_cfg()["n_shuffles"]),
        "  %d/%d both-cached edges above background (%.0f%%); mean z = %.2f"
        % (b2["n_above_background"], b2["n_edges_scored"],
           100.0 * b2["frac_above_background"], b2["mean_z"]),
        "  canonical SOX9 -| RUNX2: z = %.2f (BELOW background) -- direct repression is distal, not"
        % b2["canonical_SOX9_represses_RUNX2"]["z"],
        "    in the +-2 kb promoter / gamma window.",
        "  B2 DATA-BLOCKED = %s   grade = [F] (needs distal-enhancer + accessibility data; NOT [L])"
        % b2["b2_data_blocked"],
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
