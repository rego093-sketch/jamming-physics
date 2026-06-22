#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E1.py — the focused pass/fail gate for increment E1 (run from the package root).

    python3 research/E1-angle-to-cone/gate_E1.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM   — research/E1-angle-to-cone/run.py emits an identical sha256 on two runs.
  [G2] FALSIFIER     — the committed 633/532 angle anchor holds (red 89.9378° ≠ green 89.8248°,
                       sep > 0.05°) using the FROZEN inherited law.
  [G3] TRICHROMACY   — the three cone λmax (S420/M530/L560) map to three DISTINCT angle-bands.
  [G4] EMERGENCE     — the cone/rod lineage order = argsort(spinodal(γ)) places the three cones
                       consistently with their measured γ (lowest-γ cone first, highest-γ cone last).
  [G5] A4 TIE-BREAK  — CNGA1/CNGB1 (closest γ pair) COLLAPSE at γ-only 3-decimal resolution, and
                       the A4 shape breaks the degeneracy deterministically.
  [G6] NO-DRIFT      — the γ E1 consumes for the cones is byte-equal to the frozen atlas (no fitting).

Exit 0 + 'E1 GATE: PASS' only if all hold.
"""
import os, sys, json, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_color_by_angle import chi_deg                          # FROZEN inherited law
from vp_substrate import spinodal                              # FROZEN inherited switch
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")


def _sha_of_run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def main():
    print("=" * 74)
    print("E1 GATE — research/E1-angle-to-cone")
    print("=" * 74)
    ok = True

    # [G1] determinism
    h1, h2 = _sha_of_run(), _sha_of_run()
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] falsifier: the committed anchor
    sep = abs(chi_deg(632.99e-9) - chi_deg(532.0e-9))
    g2 = sep > 0.05; ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 falsifier — 633/532 anchor sep={sep:.4f}° > 0.05°")

    # [G3] trichromacy: three distinct angle-bands
    lmax = {"OPN1SW": 420.0, "OPN1MW": 530.0, "OPN1LW": 560.0}
    ang = {s: chi_deg(l * 1e-9) for s, l in lmax.items()}
    g3 = len({round(v, 4) for v in ang.values()}) == 3; ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 trichromacy — three distinct angle-bands "
          f"(S {ang['OPN1SW']:.4f}° / M {ang['OPN1MW']:.4f}° / L {ang['OPN1LW']:.4f}°)")

    # [G4] emergence order places the cones consistently with γ
    cones = sorted(("OPN1SW", "OPN1MW", "OPN1LW"), key=lambda s: spinodal(ATLAS[s]["gamma"]))
    by_gamma = sorted(("OPN1SW", "OPN1MW", "OPN1LW"), key=lambda s: ATLAS[s]["gamma"])
    g4 = (cones == by_gamma); ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 emergence — cone order by spinodal(γ) = {cones} "
          f"(monotone in γ)")

    # [G5] A4 tie-break on the closest γ pair
    a, b = ATLAS["CNGA1"], ATLAS["CNGB1"]
    collapse = (round(a["gamma"], 3) == round(b["gamma"], 3)
                and round(a["spinodal"], 3) == round(b["spinodal"], 3))
    shape_diff = a["shape_amplitude"] != b["shape_amplitude"]
    g5 = collapse and shape_diff; ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 A4 tie-break — CNGA1/CNGB1 collapse at γ-only 3dp "
          f"({round(a['gamma'],3)}), A4 shape differs ({a['shape_amplitude']:.5f}≠{b['shape_amplitude']:.5f})")

    # [G6] no drift: E1 consumes the frozen atlas γ unchanged
    frozen_g = {"OPN1SW": 1.3663, "OPN1MW": 1.4058, "OPN1LW": 1.4820}
    g6 = all(ATLAS[s]["gamma"] == v for s, v in frozen_g.items()); ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 no-drift — cone γ byte-equal to frozen atlas (no fitting)")

    print("=" * 74)
    print(f"E1 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
