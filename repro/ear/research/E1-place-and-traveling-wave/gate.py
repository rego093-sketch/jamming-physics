#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — the small E1 gate.  Asserts increment E1's claims, independent of the master verifier.

Run:  python3 research/E1-place-and-traveling-wave/gate.py
Exit 0 + 'E1 GATE: PASS' iff all hold.

Checks (each is a binding E1 claim, no number tuned):
  G1  determinism — run.py's self-hash is identical across two runs (2×sha256).
  G2  inputs reproduce — γ + A4 of every consumed MET gene recompute from the FROZEN cache and equal
      the atlas bit-for-bit, with A4 orthogonality |mean(shape)|<1e-9 (A4 = signal − γ).
  G3  emergence order — the tip-link trio orders TMC1 < PCDH15 < CDH23 by argsort(spinodal(γ)).
  G4  A4 tie-break refuses to collapse equal-γ genes — a constructed same-γ pair stays distinct (2≠1).
  G5  R19 discontinuity — the MET switch is OFF below the spinodal and ON above it (all-or-none flip).
  G6  place map — the inherited √-law Greenwood SHAPE reproduces (max|ratio−1| < 1e-9).
  G7  traveling-wave peak place — x*(f)=inverse-Greenwood round-trips Greenwood(x*) to <1e-6 Hz, and
      the full dispersive ENVELOPE is declared [O] in run.py (obstacle named, VP-SPEC C3).
"""
import os, sys, json, math, subprocess, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_dna_reading as DNA
import vp_substrate   as SUB
import vp_sound_wave  as SND
sys.path.insert(0, _HERE)
import run as E1


def _hash_once():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "run.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")][-1]
    return line.split("sha256:")[1].strip()


def main():
    print("=" * 78); print("E1 GATE — vp_ear_emergence_seed / E1 (tip-link MET on the place map)"); print("=" * 78)
    ok = True

    # G1 determinism
    h1, h2 = _hash_once(), _hash_once()
    g = (h1 == h2); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G1 determinism — 2×sha256 identical ({h1[:16]})")

    # G2 inputs reproduce from frozen cache == atlas
    genes = {s: E1.read_measured(s) for s in E1.MET_FULL}      # read_measured already asserts cache==atlas & A4⊥
    g = True; ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G2 inputs reproduce — {len(genes)} MET genes γ+A4 == atlas, A4=signal−γ")

    # G3 emergence order
    trio_order = [x["sym"] for x in sorted((genes[s] for s in E1.MET_TRIO), key=E1.order_key)]
    g = (trio_order == ["TMC1", "PCDH15", "CDH23"]); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G3 emergence order — argsort(spinodal(γ)) = {' < '.join(trio_order)}")

    # G4 A4 tie-break no-collapse (constructed same-γ pair)
    gx, gy = genes["TMC1"], genes["CDH23"]
    a = dict(sym="A", gamma=gx["gamma"], spinodal=gx["spinodal"], shape_amplitude=gx["shape_amplitude"],
             shape_range=gx["shape_range"], stiffest_offset_bp=gx["stiffest_offset_bp"])
    b = dict(sym="B", gamma=gx["gamma"], spinodal=gx["spinodal"], shape_amplitude=gy["shape_amplitude"],
             shape_range=gy["shape_range"], stiffest_offset_bp=gy["stiffest_offset_bp"])
    same_gamma = (round(a["gamma"], 9) == round(b["gamma"], 9))
    distinct   = (E1.order_key(a) != E1.order_key(b))
    g = (same_gamma and distinct); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G4 A4 tie-break — equal-γ pair kept distinct (same_γ={same_gamma}, distinct={distinct})")

    # G5 R19 discontinuity
    gm = genes["TMC1"]["gamma"]; sp = SUB.spinodal(gm)
    below, above = SUB.is_on(gm, 0.99 * sp), SUB.is_on(gm, 1.01 * sp)
    g = ((not below) and above); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G5 R19 discontinuity — OFF below spinodal ({below}), ON above ({above})")

    # G6 place map reproduces
    _, _, _, max_dev = SND.stiffness_graded_tonotopy()
    g = (max_dev < 1e-9); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G6 place map — Greenwood SHAPE reproduces (max|ratio−1|={max_dev:.1e})")

    # G7 traveling-wave peak place round-trips; envelope declared [O]
    worst = max(abs(SND.greenwood_f(E1.inv_greenwood(f)) - f) for f in (250, 1000, 4000, 16000))
    src = open(os.path.join(_HERE, "run.py"), encoding="utf-8").read()
    envelope_open = ("ENVELOPE" in src and "[O]" in src and "OBSTACLE" in src)
    g = (worst < 1e-6 and envelope_open); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G7 peak place round-trip <1e-6 Hz (worst={worst:.1e}); envelope [O] declared={envelope_open}")

    print("=" * 78); print(f"E1 GATE: {'PASS' if ok else 'FAIL'}"); print("=" * 78)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
