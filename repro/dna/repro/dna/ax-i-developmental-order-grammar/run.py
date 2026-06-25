#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py -- the single reproducible entry point for Appendix I.

Runs the gate, assembles the full reading, and writes the expected/ artifacts:
  expected/gate_report.json   the I1..I12 gate outcome (+ gate sha)
  expected/reading.json       the complete Appendix-I reading (+ reading_hash, 2x SHA-256)
  expected/order_table.csv    per-gene gamma / spinodal / barrier / cascade depth / composite rank
  expected/summary.txt        a short human-readable verdict

Deterministic: re-running reproduces byte-identical files.
"""
import os
import json
import csv

from order import interpreter, gate, cascade


HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "expected")


def main():
    os.makedirs(EXP, exist_ok=True)

    # 1) gate
    print("== Appendix I gate ==")
    g = gate.run_gate(verbose=True)
    with open(os.path.join(EXP, "gate_report.json"), "w", encoding="utf-8") as fh:
        json.dump(g, fh, sort_keys=True, ensure_ascii=False, indent=2)

    # 2) full reading + hash
    reading = interpreter.interpret()
    reading_hash = interpreter.reading_hash()
    out = {"reading_hash_sha256x2": reading_hash, "reading": reading}
    with open(os.path.join(EXP, "reading.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, sort_keys=True, ensure_ascii=False, indent=2)

    # 3) order table CSV
    rows = cascade.order_table()
    cols = ["composite_rank", "gene", "program", "system", "gamma", "spinodal",
            "barrier", "cascade_depth", "is_source"]
    with open(os.path.join(EXP, "order_table.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in cols})

    # 4) summary
    decl = reading["declaration"]
    counts = reading["grading"]["counts"]
    lines = [
        "Appendix I -- developmental ORDER grammar",
        "=" * 52,
        decl["headline"],
        "",
        "gate: %s (%d/%d)  sha=%s" % ("PASS" if g["_all_pass"] else "FAIL",
                                      g["_n_pass"], g["_n_total"], g["_sha256"]),
        "reading_hash (2x SHA-256): %s" % reading_hash,
        "grades: V=%d  L=%d  O=%d   physical_complete=%s"
        % (counts["V"], counts["L"], counts["O"], decl["physical_complete"]),
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
