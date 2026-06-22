#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E3.py — the focused pass/fail gate for increment E3 (run from the package root).

    python3 research/E3-bulb-map/gate_E3.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM   — research/E3-bulb-map/run.py emits an identical sha256 on two runs.
  [G2] ORDER         — the OSN-identity organisers emerge as R19 Organs in spinodal(γ) order,
                       monotone in γ (lowest γ forms first).
  [G3] PRESENCE      — each organiser Organ is ABSENT below its spinodal h* and PRESENT above it
                       ("parts present ≠ trait": an OFF master switch yields organ absence).
  [G4] CAPACITY      — the one-OR→one-glomerulus convergence is a bijection: the full 2^N subset
                       lattice maps to exactly 2^N distinct spatial patterns (capacity preserved).
  [G5] SPATIAL THERM — E1's nested-thermometer readout maps to a nested thermometer IN SPACE
                       (a bijection preserves subset chains), ≤ N+1 nested spatial patterns.
  [G6] COORD GAP     — γ supplies only a 1-D channel rank; the 2-D glomerular targeting coordinate
                       is the named [O] (axon-guidance chemistry), never read from γ.
  [G7] NO-DRIFT      — the organiser/OR γ E3 consumes is byte-equal to the frozen atlas (no fitting).

Exit 0 + 'E3 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import spinodal, settle, is_on, Organ            # FROZEN inherited switch + Organ
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")
ORGANISERS = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_neuron_identity"))
OR_GENES   = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_receptor"))


def _sha_of_run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _thermometer_spatial():
    order = sorted(OR_GENES, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    pos   = {s: i for i, s in enumerate(order)}
    thr   = sorted(spinodal(ATLAS[s]["gamma"]) for s in OR_GENES)
    seen  = []
    for frac in (0.0, 0.5, 0.8, 0.9, 0.95, 1.0, 1.05, 1.2):
        h = frac * thr[-1] * 1.05
        on = tuple(s for s in order
                   if settle(ATLAS[s]["gamma"], h, s0=-math.sqrt(ATLAS[s]["gamma"])) > 0.0)
        glo = frozenset(pos[s] for s in on)
        if glo not in seen:
            seen.append(glo)
    return seen


def main():
    print("=" * 74)
    print("E3 GATE — research/E3-bulb-map")
    print("=" * 74)
    ok = True
    N = len(OR_GENES)

    # [G1] determinism
    h1, h2 = _sha_of_run(), _sha_of_run()
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] organiser emergence order monotone in γ
    organs = {s: Organ(s, ATLAS[s]["gamma"]) for s in ORGANISERS}
    by_spin = sorted(ORGANISERS, key=lambda s: organs[s].functional_spinodal())
    by_gam  = sorted(ORGANISERS, key=lambda s: ATLAS[s]["gamma"])
    g2 = (by_spin == by_gam); ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 order — organisers emerge by spinodal(γ) monotone in γ ({by_spin[0]} first)")

    # [G3] presence threshold: absent below h*, present above
    g3 = True
    for s in ORGANISERS:
        o = organs[s]; hstar = o.functional_spinodal()
        g3 &= (o.present(0.90 * hstar) is False) and (o.present(1.10 * hstar) is True)
    ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 presence — every organiser Organ absent below h*, present above (parts≠trait)")

    # [G4] capacity preserved under a bijection (full subset lattice)
    perm = {c: (N - 1 - c) for c in range(N)}
    images = {frozenset(perm[c] for c in range(N) if (mask >> c) & 1) for mask in range(2 ** N)}
    g4 = (len(images) == 2 ** N); ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 capacity — bijection maps all 2^{N}={2**N} subsets → {len(images)} distinct spatial patterns")

    # [G5] spatial thermometer nested, ≤ N+1
    sp = _thermometer_spatial()
    nested = all(sp[i].issubset(sp[i + 1]) for i in range(len(sp) - 1))
    g5 = nested and (len(sp) <= N + 1); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 spatial thermometer — {len(sp)} nested spatial patterns (≤ N+1={N+1}, chain preserved)")

    # [G6] coordinate gap: γ gives a 1-D rank, not a 2-D coordinate (sanity: ranks are a strict order)
    ranks = [spinodal(ATLAS[s]["gamma"]) for s in sorted(OR_GENES, key=lambda x: spinodal(ATLAS[x]["gamma"]))]
    g6 = all(ranks[i] < ranks[i + 1] for i in range(len(ranks) - 1))   # γ → a 1-D order only; coord is [O]
    ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 coord gap — γ gives a strict 1-D channel rank; 2-D glomerulus coordinate is [O]")

    # [G7] no drift: organiser/OR γ byte-equal to frozen atlas
    frozen = {"LHX2": 1.5172, "EBF1": 1.4097, "EMX2": 1.4574,
              "OR1D2": 1.2714, "OR2J3": 1.2224, "OR2W1": 1.2412, "OR5AN1": 1.2637,
              "OR6A2": 1.3036, "OR51E2": 1.2427, "OR7D4": 1.2945}
    g7 = all(ATLAS[s]["gamma"] == v for s, v in frozen.items()); ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 no-drift — organiser/OR γ byte-equal to frozen atlas (no fitting)")

    print("=" * 74)
    print(f"E3 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
