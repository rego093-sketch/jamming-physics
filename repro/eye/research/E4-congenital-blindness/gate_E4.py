#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E4.py — the focused pass/fail gate for increment E4 (run from the package root).

    python3 research/E4-congenital-blindness/gate_E4.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM    — research/E4-congenital-blindness/run.py emits an identical sha256 on two runs.
  [G2] LOF = DARK     — for every blindness gene (GUCY2D/RPE65/AIPL1/RPGR/PDE6B/CNGB3), the FROZEN R19
                        field settled from rest under the LOF-attenuated drive (0.85·h*) stays in the
                        dark basin (s<0): the switch cannot flip.
  [G3] HEALTHY FLIP   — the same field under a clearing drive (1.15·h*) flips on (s>0): the only
                        difference between affected and healthy is whether the drive clears h*.
  [G4] LEVER (i)      — raising the drive across h* re-flips the switch (restore-the-drive direction),
                        and only past h* (a drive still below h* does not flip): direction, not dose.
  [G5] LEVER (ii)     — with the residual drive fixed, a switch whose effective threshold is pushed
                        below that drive flips, while at the native threshold it stays dark (lower-the-
                        barrier direction); the measured γ is never altered.
  [G6] THRESHOLD RANK — the six switches order by spinodal(γ) (a structural ordering, not severity);
                        the six γ are all distinct at 3dp (no tie) yet the closest-γ pair is separated
                        by A4 shape (γ + A4, never γ alone).
  [G7] NO-DRIFT       — the six blindness-gene γ E4 consumes are byte-equal to the frozen atlas (no fitting).
  [G8] MAGNITUDE FW   — the entire run.py output carries NO quantitative clinical token and no "%"
                        (the disease layer is direction-only / proposal-only, machine-checked).

Exit 0 + 'E4 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import spinodal, settle                       # FROZEN inherited switch
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")
BLIND = ("GUCY2D", "RPE65", "AIPL1", "RPGR", "PDE6B", "CNGB3")

# the firewall token list (kept in lock-step with run.py's MAGNITUDE_BLOCK)
MAGNITUDE_BLOCK = (
    "dose", "dosage", "mg/kg", "ic50", "ec50", "µmol", "nmol", "µg", "µm)", "nm)",
    "potency", "efficacy", "selectivity", "diopter", "dioptre", "mmhg",
    "milligram", "microgram", "micromolar", "nanomolar",
)


def _run_capture():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _gamma_for_threshold(h_star):
    return 3.0 * (h_star / 2.0) ** (2.0 / 3.0)


def main():
    print("=" * 74)
    print("E4 GATE — research/E4-congenital-blindness")
    print("=" * 74)
    ok = True

    # [G1] determinism
    o1, o2 = _run_capture(), _run_capture()
    h1, h2 = _sha_of(o1), _sha_of(o2)
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] LOF = dark on all six genes
    g2 = True
    for sym in BLIND:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
        g2 &= settle(g, 0.85 * hstar, s0=s0) < 0.0
    ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 LOF=dark — all 6 blindness switches stay dark under the "
          f"LOF drive (0.85·h*): cannot flip")

    # [G3] healthy flip on all six
    g3 = True
    for sym in BLIND:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
        g3 &= settle(g, 1.15 * hstar, s0=s0) > 0.0
    ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 healthy flip — all 6 flip on under a clearing drive "
          f"(1.15·h*): only the drive vs h* differs")

    # [G4] lever (i): raise drive — flips only past h*
    g = ATLAS["GUCY2D"]["gamma"]; hstar = spinodal(g); s0 = -math.sqrt(g)
    below = settle(g, 0.95 * hstar, s0=s0) > 0.0      # still below h* → no flip
    above = settle(g, 1.05 * hstar, s0=s0) > 0.0      # past h* → flip
    g4 = (not below) and above; ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 lever (i) — raising drive re-flips only past h* "
          f"(dark at 0.95·h*, on at 1.05·h*): direction, not dose")

    # [G5] lever (ii): lower the effective threshold below the fixed residual drive (γ untouched)
    d = 0.85 * hstar
    g_native = _gamma_for_threshold(1.00 * hstar)     # threshold at native h* (> d) → dark
    g_lower  = _gamma_for_threshold(0.80 * hstar)     # threshold below d        → flip
    stays_dark = settle(g_native, d, s0=-math.sqrt(g_native)) < 0.0
    flips      = settle(g_lower,  d, s0=-math.sqrt(g_lower))  > 0.0
    g5 = stays_dark and flips; ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 lever (ii) — fixed drive, threshold below it flips "
          f"(dark at native h*, on at 0.80·h*): lower-the-barrier direction")

    # [G6] threshold rank by spinodal(γ); all γ distinct at 3dp; closest-γ pair A4-separated
    by_spin = sorted(BLIND, key=lambda s: ATLAS[s]["spinodal"])
    gam3 = {s: round(ATLAS[s]["gamma"], 3) for s in BLIND}
    all_distinct = (len(set(gam3.values())) == len(BLIND))
    pair = sorted(BLIND, key=lambda s: ATLAS[s]["gamma"])
    g1n, g2n, dgam = min(((pair[i], pair[i+1], abs(ATLAS[pair[i]]["gamma"] - ATLAS[pair[i+1]]["gamma"]))
                          for i in range(len(pair) - 1)), key=lambda t: t[2])
    a1, a2 = ATLAS[g1n]["shape_amplitude"], ATLAS[g2n]["shape_amplitude"]
    a4_sep = (a1 != a2) and (max(a1, a2) / min(a1, a2) > 1.2)
    g6 = all_distinct and a4_sep; ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 threshold rank — order by spinodal(γ)={by_spin}; "
          f"γ all distinct@3dp ({all_distinct}); closest pair {g1n}/{g2n} A4-separated")

    # [G7] no drift: E4 consumes the frozen atlas γ unchanged
    frozen_g = {"GUCY2D": 1.3650, "RPE65": 1.2842, "AIPL1": 1.4656,
                "RPGR": 1.3915, "PDE6B": 1.5354, "CNGB3": 1.2425}
    g7 = all(ATLAS[s]["gamma"] == v for s, v in frozen_g.items()); ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 no-drift — six blindness γ byte-equal to frozen atlas (no fitting)")

    # [G8] magnitude firewall: the run output carries no clinical-magnitude token and no "%"
    low = o1.lower()
    hits = [tok for tok in MAGNITUDE_BLOCK if tok in low]
    g8 = (not hits) and ("%" not in o1); ok &= g8
    print(f"  [{'PASS' if g8 else 'FAIL'}] G8 magnitude firewall — no clinical-magnitude token, no '%' "
          f"(direction-only) {('hits='+str(hits)) if hits else ''}")

    print("=" * 74)
    print(f"E4 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
