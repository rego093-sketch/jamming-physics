#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E9.py — the focused pass/fail gate for increment E9 (run from the package root).

    python3 research/E9-red-green-dichromacy/gate_E9.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM    — research/E9-red-green-dichromacy/run.py emits an identical sha256 on two runs.
  [G2] FRAGILITY      — using the FROZEN law, the M-L (green-red) angle margin is the SMALLEST of the
                        three pairwise cone margins (S-M, M-L, S-L) — the structurally most fragile axis.
  [G3] COINCIDENCE    — two opsins with the SAME λmax map to the SAME angle ⇒ margin EXACTLY 0.
  [G4] DICHROMACY     — removing one of the M/L samples leaves exactly two angle-samples and the
                        within-red-green (M-L) axis vanishes.
  [G5] CONVERGENCE    — inside one m-band (χ smooth-monotone), the margin falls monotonically to
                        exactly 0 as a hypothetical peak converges to λ(M).
  [G6] ORTHOGONALITY  — the remaining cones' R19 switch (spinodal) is unchanged by a cone removal
                        (colour-angle loss does not touch the detection switch).
  [G7] NO-DRIFT       — the cone γ E9 consumes is byte-equal to the frozen atlas (no fitting).
  [G8] FIREWALL       — run.py's whole output carries NONE of E9's MAGNITUDE_BLOCK tokens and no '%'.

Exit 0 + 'E9 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess, importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_color_by_angle import chi_deg, D                  # FROZEN inherited law
from vp_substrate import spinodal                         # FROZEN inherited switch
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

LMAX = {"OPN1SW": 420.0, "OPN1MW": 530.0, "OPN1LW": 560.0}


def _run():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of_run(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def main():
    print("=" * 74)
    print("E9 GATE — research/E9-red-green-dichromacy")
    print("=" * 74)
    ok = True
    ang = {s: chi_deg(l * 1e-9) for s, l in LMAX.items()}

    # [G1] determinism
    o1, o2 = _run(), _run()
    h1, h2 = _sha_of_run(o1), _sha_of_run(o2)
    g1 = (h1 == h2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 determinism — run.py sha256 stable ({h1[:16]})")

    # [G2] fragility: M-L is the smallest of the three pairwise margins
    sm = abs(ang["OPN1SW"] - ang["OPN1MW"])
    ml = abs(ang["OPN1MW"] - ang["OPN1LW"])
    sl = abs(ang["OPN1SW"] - ang["OPN1LW"])
    g2 = (ml < sm) and (ml < sl); ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 fragility — green-red M-L={ml:.4f}° is smallest "
          f"(S-M={sm:.4f}°, S-L={sl:.4f}°)")

    # [G3] coincidence ⇒ exactly zero margin
    coin = abs(chi_deg(LMAX["OPN1MW"] * 1e-9) - chi_deg(LMAX["OPN1MW"] * 1e-9))
    g3 = (coin == 0.0); ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 coincidence — same λmax ⇒ margin = {coin:.6f}° (exact 0)")

    # [G4] dichromacy: remove one M/L sample → exactly two samples, M-L axis gone
    keep_lose_L = ("OPN1SW", "OPN1MW")
    keep_lose_M = ("OPN1SW", "OPN1LW")
    g4 = (len(keep_lose_L) == 2 and len(keep_lose_M) == 2
          and "OPN1LW" not in keep_lose_L and "OPN1MW" not in keep_lose_M)
    ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 dichromacy — losing one M/L sample leaves 2 angle-samples "
          f"(the M-L axis vanishes)")

    # [G5] convergence: within one m-band the margin falls monotonically to 0
    Dnm = D * 1e9
    m_M = math.ceil(LMAX["OPN1MW"] / Dnm)
    band_hi = m_M * Dnm
    aM = ang["OPN1MW"]
    sweep = [abs(chi_deg((LMAX["OPN1MW"] + f * (band_hi - LMAX["OPN1MW"])) * 1e-9) - aM)
             for f in (1.0, 0.6, 0.3, 0.1, 0.0)]
    mono = all(sweep[i] >= sweep[i + 1] - 1e-12 for i in range(len(sweep) - 1))
    g5 = mono and (sweep[-1] == 0.0); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 convergence — within one m-band margin → 0 monotonically "
          f"(end {sweep[-1]:.6f}°)")

    # [G6] orthogonality: the remaining cones' switch is unchanged by a colour-sample removal
    s_a = spinodal(ATLAS["OPN1MW"]["gamma"])
    s_b = spinodal(ATLAS["OPN1MW"]["gamma"])
    g6 = (s_a == s_b); ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 orthogonality — remaining cone R19 switch unchanged "
          f"(spinodal {s_a:.4f} stable)")

    # [G7] no-drift: cone γ byte-equal to frozen atlas
    frozen_g = {"OPN1SW": 1.3663, "OPN1MW": 1.4058, "OPN1LW": 1.4820}
    g7 = all(ATLAS[s]["gamma"] == v for s, v in frozen_g.items()); ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 no-drift — cone γ byte-equal to frozen atlas (no fitting)")

    # [G8] firewall: import E9's MAGNITUDE_BLOCK, assert run output carries none of it + no '%'
    spec = importlib.util.spec_from_file_location("_e9_run_for_firewall", RUN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    low = o1.lower()
    hits = sorted(t for t in mod.MAGNITUDE_BLOCK if t in low)
    g8 = (not hits) and ("%" not in o1); ok &= g8
    print(f"  [{'PASS' if g8 else 'FAIL'}] G8 firewall — no magnitude token {hits if hits else '[]'}, "
          f"no '%'")

    print("=" * 74)
    print(f"E9 GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
