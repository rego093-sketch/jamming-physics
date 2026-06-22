#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E2.py — the focused pass/fail gate for increment E2 (run from the package root).

    python3 research/E2-single-photon-switch/gate_E2.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM   — research/E2-single-photon-switch/run.py emits an identical sha256 on two runs.
  [G2] ALL-OR-NONE   — for every rod gene (RHO/CNGA1/CNGB1/GNAT1), the FROZEN R19 field settled from
                       rest stays dark below its spinodal (s<0) and snaps on above it (s>0).
  [G3] DISCONTINUITY — RHO shows a genuine off→on flip across h* (a step, not a graded ramp).
  [G4] COOPERATIVITY — the cubic switch is ≥ an order of magnitude steeper than the same field with
                       the cubic deleted (the −s³ is what makes the response all-or-none).
  [G5] CASCADE ORDER — the four switches order by spinodal(γ); the order is consistent with γ
                       (lowest-γ switch lowest threshold), with the cascade↔biochemistry match left [O].
  [G6] A4 IN-SWITCH  — CNGA1/CNGB1 (the one CNG channel's α/β) COLLAPSE at γ-only 3-decimal resolution
                       and are separated by their A4 shape (γ alone is lossy even inside one switch).
  [G7] NO-DRIFT      — the rod-gene γ E2 consumes is byte-equal to the frozen atlas (no fitting).

Exit 0 + 'E2 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import spinodal, settle                       # FROZEN inherited switch
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")
ROD   = ("RHO", "CNGA1", "CNGB1", "GNAT1")


def _sha_of_run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _linear_control(g, h, s0=0.0, n=4000, dt=0.02):
    """Substrate with the cubic struck out (control only): ds/dt = −g·s + h."""
    s = s0
    for _ in range(n):
        s += dt * (-g * s + h)
    return s


def main():
    print("=" * 74)
    print("E2 GATE — research/E2-single-photon-switch")
    print("=" * 74)
    ok = True

    # [G1] determinism
    h1, h2 = _sha_of_run(), _sha_of_run()
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] all-or-none on all four rod genes
    g2 = True
    for sym in ROD:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
        below = settle(g, 0.90 * hstar, s0=s0)
        above = settle(g, 1.10 * hstar, s0=s0)
        g2 &= (below < 0.0 < above) and (above - below > 1.5)
    ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 all-or-none — all 4 rod switches dark below h*, on above "
          f"(finite saddle-node jump)")

    # [G3] discontinuity: RHO flips off→on across h*
    g = ATLAS["RHO"]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
    below_on = settle(g, 0.99 * hstar, s0=s0) > 0.0
    above_on = settle(g, 1.01 * hstar, s0=s0) > 0.0
    g3 = (not below_on) and above_on; ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 discontinuity — RHO off at 0.99·h*, on at 1.01·h* (a step)")

    # [G4] cooperativity: cubic >> linear-control steepness
    s_lo = settle(g, 0.99 * hstar, s0=s0); s_hi = settle(g, 1.01 * hstar, s0=s0)
    cubic_slope = abs(s_hi - s_lo) / (0.02 * hstar)
    graded_slope = abs(_linear_control(g, 1.10 * hstar) - _linear_control(g, 0.90 * hstar)) / (0.20 * hstar)
    g4 = (cubic_slope > 20.0 * graded_slope); ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 cooperativity — cubic switch ≈{cubic_slope:.0f} vs control "
          f"≈{graded_slope:.2f} per h ({cubic_slope/graded_slope:.0f}×; the −s³ is necessary)")

    # [G5] cascade order = argsort(spinodal(γ)), consistent with γ
    by_spin = sorted(ROD, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    by_gam  = sorted(ROD, key=lambda s: ATLAS[s]["gamma"])
    g5 = (by_spin == by_gam); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 cascade order — by spinodal(γ) = {by_spin} (monotone in γ; "
          f"cascade↔biochemistry [O])")

    # [G6] A4 tie-break inside the CNG channel
    a, b = ATLAS["CNGA1"], ATLAS["CNGB1"]
    collapse = (round(a["gamma"], 3) == round(b["gamma"], 3)
                and round(a["spinodal"], 3) == round(b["spinodal"], 3))
    shape_diff = a["shape_amplitude"] != b["shape_amplitude"]
    g6 = collapse and shape_diff; ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 A4 in-switch — CNGA1/CNGB1 collapse at γ-only 3dp "
          f"({round(a['gamma'],3)}), A4 shape differs ({a['shape_amplitude']:.5f}≠{b['shape_amplitude']:.5f})")

    # [G7] no drift: E2 consumes the frozen atlas γ unchanged
    frozen_g = {"RHO": 1.4719, "CNGA1": 1.4360, "CNGB1": 1.4357, "GNAT1": 1.4511}
    g7 = all(ATLAS[s]["gamma"] == v for s, v in frozen_g.items()); ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 no-drift — rod γ byte-equal to frozen atlas (no fitting)")

    print("=" * 74)
    print(f"E2 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
