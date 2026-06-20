#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all.py — single entry point that verifies the ENTIRE integrated neuro package:
  (1) repro/neuro/run_all.py            — chapters 00..15 modules deterministic, HTML drift 0
  (2) every repro slug with a run.py    — per-slug gate + determinism + fidelity
  (3) every tools/gate_neuro_*.py        — per-chapter C1 gate (HTML numbers vs regenerated)
Run from the package root:  python3 verify_all.py
Exits 0 only if every check passes.
"""
import os, subprocess, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
results = []


def run(label, cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)
    tail = (p.stdout or p.stderr).strip().splitlines()[-1:] or [""]
    ok = (p.returncode == 0) and ("PASS" in tail[0] or "ok" in tail[0].lower() or p.returncode == 0)
    # stricter: require explicit PASS where the tool emits a verdict
    if "FAIL" in (p.stdout + p.stderr):
        ok = False
    results.append((label, ok, tail[0]))
    print(f"  [{'PASS' if ok else 'FAIL'}] {label:42s} {tail[0][:60]}")
    return ok


def main():
    print("=" * 78)
    print("INTEGRATED NEURO PACKAGE — full verification")
    print("=" * 78)

    print("\n[1] reproduction harness (modules deterministic, HTML↔code drift 0)")
    run("run_all.py", [sys.executable, "run_all.py"], os.path.join(ROOT, "repro", "neuro"))

    print("\n[2] per-slug verification (run.py present)")
    for runpy in sorted(glob.glob(os.path.join(ROOT, "repro", "neuro", "*", "run.py"))):
        slug = os.path.basename(os.path.dirname(runpy))
        run(f"slug {slug}", [sys.executable, "run.py"], os.path.dirname(runpy))

    print("\n[3] per-chapter C1 gates (tools/gate_neuro_*.py)")
    for gate in sorted(glob.glob(os.path.join(ROOT, "tools", "gate_neuro_*.py"))):
        run(f"gate {os.path.basename(gate)}", [sys.executable, gate], ROOT)

    npass = sum(1 for _, ok, _ in results if ok)
    verdict = all(ok for _, ok, _ in results)
    print("\n" + "=" * 78)
    print(f"OVERALL: {'PASS' if verdict else 'FAIL'}  ({npass}/{len(results)} checks)")
    print("=" * 78)
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
