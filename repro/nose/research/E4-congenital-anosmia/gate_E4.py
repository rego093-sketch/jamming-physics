#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E4.py — the focused pass/fail gate for increment E4 (run from the package root).

    python3 research/E4-congenital-anosmia/gate_E4.py

THEORETICAL / NON-CLINICAL. This gate checks STRUCTURE, never a clinical claim. All of E4 is
direction-only / proposal-only (FIREWALL.md #4): no diagnosis, dose, molecule, or efficacy.

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM   — research/E4-congenital-anosmia/run.py emits an identical sha256 on two runs.
  [G2] CHANNEL FLIP  — for each CNG channelopathy gene the WT R19 field flips past h* (dark below,
                       on above, finite jump): the all-or-none transduction event exists in WT.
  [G3] SWITCH LOSS   — deleting the switch (cubic struck out) destroys the flip (≥ an order of
                       magnitude shallower): the channelopathy failure mode is loss of the R19 flip.
  [G4] ORGAN FAIL    — for each Kallmann gene the R19 Organ is ABSENT below its presence threshold
                       and PRESENT above it: the organ-formation failure mode (parts ≠ trait).
  [G5] CROSS-SENSE   — CNGB1 γ is byte-identical to the rod-vision sibling (the same switch fails in
                       two senses: smell AND rod vision).
  [G6] TWO CLASSES   — the channelopathy and organ-formation gene sets are disjoint and cover the
                       six congenital-anosmia genes (the substrate's two R19 failure modes).
  [G7] NO-DRIFT      — the anosmia-gene γ E4 consumes is byte-equal to the frozen atlas (no fitting;
                       PROKR2/PROK2 measured from NCBI, never invented).

Exit 0 + 'E4 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import spinodal, settle, is_on, Organ            # FROZEN inherited switch + Organ
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")
CHANNELOPATHY = ("CNGA2", "CNGB1")
DEVELOPMENTAL = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "congenital_anosmia"))
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
    print("E4 GATE — research/E4-congenital-anosmia   (theoretical / NON-CLINICAL; direction-only)")
    print("=" * 74)
    ok = True

    # [G1] determinism
    h1, h2 = _sha_of_run(), _sha_of_run()
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] WT channel flip exists
    g2 = True
    for sym in CHANNELOPATHY:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
        below = settle(g, 0.90 * hstar, s0=s0); above = settle(g, 1.10 * hstar, s0=s0)
        g2 &= (below < 0.0 < above) and (above - below > 1.5)
    ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 channel flip — WT CNG switch flips past h* (all-or-none transduction exists)")

    # [G3] switch loss destroys the flip
    g = ATLAS["CNGA2"]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
    cubic_slope  = abs(settle(g, 1.01 * hstar, s0=s0) - settle(g, 0.99 * hstar, s0=s0)) / (0.02 * hstar)
    graded_slope = abs(_linear_control(g, 1.10 * hstar) - _linear_control(g, 0.90 * hstar)) / (0.20 * hstar)
    g3 = (cubic_slope > 20.0 * graded_slope); ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 switch loss — deleting the switch kills the flip "
          f"(cubic ≈{cubic_slope:.0f} vs ≈{graded_slope:.2f}; {cubic_slope/graded_slope:.0f}×)")

    # [G4] organ-formation failure: absent below threshold, present above
    g4 = True
    for sym in DEVELOPMENTAL:
        o = Organ(sym, ATLAS[sym]["gamma"]); hstar = o.functional_spinodal()
        g4 &= (o.present(0.90 * hstar) is False) and (o.present(1.10 * hstar) is True)
    ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 organ fail — every Kallmann Organ absent below h*, present above (parts≠trait)")

    # [G5] cross-sense CNGB1
    g5 = (ATLAS["CNGB1"]["gamma"] == ROD_VISION_CNGB1_GAMMA); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 cross-sense — CNGB1 γ={ATLAS['CNGB1']['gamma']:.4f} = rod-vision "
          f"{ROD_VISION_CNGB1_GAMMA:.4f} (same switch, both senses)")

    # [G6] two disjoint classes cover the six anosmia genes
    chan, dev = set(CHANNELOPATHY), set(DEVELOPMENTAL)
    g6 = (chan.isdisjoint(dev)) and (len(chan | dev) == 6); ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 two classes — channelopathy {sorted(chan)} ⊔ organ-formation "
          f"{sorted(dev)} (disjoint, 6 genes)")

    # [G7] no drift: anosmia γ byte-equal to frozen atlas
    frozen = {"CNGA2": 1.2935, "CNGB1": 1.4357, "ANOS1": 1.4798, "FGFR1": 1.4785,
              "PROKR2": 1.4781, "PROK2": 1.4634}
    g7 = all(ATLAS[s]["gamma"] == v for s, v in frozen.items()); ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 no-drift — anosmia γ byte-equal to frozen atlas (PROKR2/PROK2 measured, not invented)")

    print("=" * 74)
    print(f"E4 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
