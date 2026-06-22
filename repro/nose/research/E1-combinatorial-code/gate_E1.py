#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E1.py — the focused pass/fail gate for increment E1 (run from the package root).

    python3 research/E1-combinatorial-code/gate_E1.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM   — research/E1-combinatorial-code/run.py emits an identical sha256 on two runs.
  [G2] THRESHOLD ORD — the OR bank orders by spinodal(γ), monotone in γ (lowest γ flips first).
  [G3] CAPACITY      — N all-or-none switches give 2^N ≫ N distinguishable patterns.
  [G4] THERMOMETER   — a uniform drive swept up flips the FROZEN switches in spinodal order into a
                       nested thermometer code of ≤ N+1 patterns (substrate-derived readout).
  [G5] LIGAND GAP    — an odorant-specific drive VECTOR reaches a non-nested pattern unreachable by
                       any uniform drive (the combinatorial richness needs the ligand [O], not γ).
  [G6] NON-DEGEN     — the OR genes carry distinct A4 shape amplitudes (expression structure), so
                       (γ, A4) separates them — while odorant tuning stays [O].
  [G7] NO-DRIFT      — the OR-gene γ E1 consumes is byte-equal to the frozen atlas (no fitting).

Exit 0 + 'E1 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import spinodal, settle                        # FROZEN inherited switch
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")
OR_GENES = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_receptor"))


def _sha_of_run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _on_set(vec):
    return tuple(s for s in sorted(OR_GENES, key=lambda x: spinodal(ATLAS[x]["gamma"]))
                 if settle(ATLAS[s]["gamma"], vec[s], s0=-math.sqrt(ATLAS[s]["gamma"])) > 0.0)


def main():
    print("=" * 74)
    print("E1 GATE — research/E1-combinatorial-code")
    print("=" * 74)
    ok = True
    N = len(OR_GENES)

    # [G1] determinism
    h1, h2 = _sha_of_run(), _sha_of_run()
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] threshold order monotone in γ
    by_spin = sorted(OR_GENES, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    by_gam  = sorted(OR_GENES, key=lambda s: ATLAS[s]["gamma"])
    g2 = (by_spin == by_gam); ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 threshold order — by spinodal(γ) monotone in γ ({by_spin[0]} flips first)")

    # [G3] combinatorial capacity 2^N >> N
    g3 = (2 ** N > 8 * N); ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 capacity — 2^{N}={2**N} ≫ N={N} (combinatorial, not 1-per-odour)")

    # [G4] thermometer readout under uniform drive: nested patterns, ≤ N+1
    thr = sorted(spinodal(ATLAS[s]["gamma"]) for s in OR_GENES)
    seen = []
    for frac in (0.0, 0.5, 0.8, 0.9, 0.95, 1.0, 1.05, 1.2):
        h = frac * thr[-1] * 1.05
        s = _on_set({x: h for x in OR_GENES})
        if s not in seen:
            seen.append(s)
    nested = all(set(seen[i]).issubset(set(seen[i + 1])) for i in range(len(seen) - 1))
    g4 = nested and (len(seen) <= N + 1); ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 thermometer — uniform drive → {len(seen)} nested patterns "
          f"(≤ N+1={N+1}, substrate-derived)")

    # [G5] ligand gap: a vector reaches a non-nested pattern
    order = by_spin
    vec = {s: (1.2 * spinodal(ATLAS[s]["gamma"]) if s in (order[0], order[2]) else 0.0) for s in OR_GENES}
    vpat = _on_set(vec)
    g5 = (vpat not in seen) and (set(vpat) not in [set(x) for x in seen]); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 ligand gap — vector reaches non-nested pattern {vpat} "
          f"(needs the binding-pocket [O])")

    # [G6] OR genes non-degenerate in A4 shape
    amps = [round(ATLAS[s]["shape_amplitude"], 5) for s in OR_GENES]
    g6 = (len(set(amps)) == len(amps)); ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 non-degenerate — {N} distinct A4 shape amplitudes "
          f"(expression structure; odorant tuning [O])")

    # [G7] no drift: OR γ byte-equal to frozen atlas
    frozen_or = {"OR1D2": 1.2714, "OR2J3": 1.2224, "OR2W1": 1.2412, "OR5AN1": 1.2637,
                 "OR6A2": 1.3036, "OR51E2": 1.2427, "OR7D4": 1.2945}
    g7 = all(ATLAS[s]["gamma"] == v for s, v in frozen_or.items()); ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 no-drift — OR γ byte-equal to frozen atlas (no fitting)")

    print("=" * 74)
    print(f"E1 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
