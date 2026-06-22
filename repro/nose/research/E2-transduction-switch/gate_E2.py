#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E2.py — the focused pass/fail gate for increment E2 (run from the package root).

    python3 research/E2-transduction-switch/gate_E2.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM   — research/E2-transduction-switch/run.py emits an identical sha256 on two runs.
  [G2] ALL-OR-NONE   — for every transduction gene the FROZEN R19 field settled from rest stays dark
                       below its spinodal (s<0) and snaps on above it (s>0), with a finite jump.
  [G3] DISCONTINUITY — CNGA2 (principal CNG subunit) flips off→on across h* (a step, not a ramp).
  [G4] COOPERATIVITY — the cubic switch is ≥ an order of magnitude steeper than the same field with
                       the cubic deleted (the −s³ is what makes transduction all-or-none).
  [G5] CROSS-SENSE   — CNGB1 γ is byte-identical to the rod-vision sibling value (same gene reused).
  [G6] SUBUNITS READ — the olfactory CNG subunits (CNGA2/CNGA4/CNGB1) are γ-separable at 3 decimals.
  [G7] NO-DRIFT      — the transduction-gene γ E2 consumes is byte-equal to the frozen atlas.

Exit 0 + 'E2 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import spinodal, settle                        # FROZEN inherited switch
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")
TRANSD = ("GNAL", "ADCY3", "CNGA2", "CNGA4", "CNGB1", "ANO2")
ROD_VISION_CNGB1_GAMMA = 1.4357


def _sha_of_run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _linear_control(g, h, s0=0.0, n=4000, dt=0.02):
    s = s0
    for _ in range(n):
        s += dt * (-g * s + h)
    return s


def main():
    print("=" * 74)
    print("E2 GATE — research/E2-transduction-switch")
    print("=" * 74)
    ok = True

    # [G1] determinism
    h1, h2 = _sha_of_run(), _sha_of_run()
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] all-or-none on all six transduction genes
    g2 = True
    for sym in TRANSD:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
        below = settle(g, 0.90 * hstar, s0=s0); above = settle(g, 1.10 * hstar, s0=s0)
        g2 &= (below < 0.0 < above) and (above - below > 1.5)
    ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 all-or-none — all 6 transduction switches dark below h*, on above")

    # [G3] discontinuity on CNGA2
    g = ATLAS["CNGA2"]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
    g3 = (settle(g, 0.99 * hstar, s0=s0) < 0.0) and (settle(g, 1.01 * hstar, s0=s0) > 0.0); ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 discontinuity — CNGA2 off at 0.99·h*, on at 1.01·h* (a step)")

    # [G4] cooperativity: cubic >> linear control
    s_lo = settle(g, 0.99 * hstar, s0=s0); s_hi = settle(g, 1.01 * hstar, s0=s0)
    cubic_slope = abs(s_hi - s_lo) / (0.02 * hstar)
    graded_slope = abs(_linear_control(g, 1.10 * hstar) - _linear_control(g, 0.90 * hstar)) / (0.20 * hstar)
    g4 = (cubic_slope > 20.0 * graded_slope); ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 cooperativity — cubic ≈{cubic_slope:.0f} vs control "
          f"≈{graded_slope:.2f} per h ({cubic_slope/graded_slope:.0f}×; the −s³ is necessary)")

    # [G5] cross-sense: CNGB1 == rod-vision sibling
    g5 = (ATLAS["CNGB1"]["gamma"] == ROD_VISION_CNGB1_GAMMA); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 cross-sense — CNGB1 γ={ATLAS['CNGB1']['gamma']:.4f} = rod-vision "
          f"{ROD_VISION_CNGB1_GAMMA:.4f} (same gene, shared switch)")

    # [G6] CNG subunits γ-separable
    cng = ("CNGA2", "CNGA4", "CNGB1")
    g3dp = [round(ATLAS[s]["gamma"], 3) for s in cng]
    g6 = (len(set(g3dp)) == len(g3dp)); ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 subunits read — CNG α/mod γ-separable at 3dp {g3dp} "
          f"(no degeneracy to break here)")

    # [G7] no drift
    frozen_t = {"GNAL": 1.4109, "ADCY3": 1.5435, "CNGA2": 1.2935,
                "CNGA4": 1.4016, "CNGB1": 1.4357, "ANO2": 1.3500}
    g7 = all(ATLAS[s]["gamma"] == v for s, v in frozen_t.items()); ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 no-drift — transduction γ byte-equal to frozen atlas (no fitting)")

    print("=" * 74)
    print(f"E2 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
