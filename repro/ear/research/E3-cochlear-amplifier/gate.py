#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — the small E3 gate.  Asserts increment E3's claims, independent of the master verifier.

Run:  python3 research/E3-cochlear-amplifier/gate.py
Exit 0 + 'E3 GATE: PASS' iff all hold.

Checks (each is a binding E3 claim, no number tuned):
  G1  determinism — run.py's self-hash is identical across two runs (2×sha256).
  G2  amplifier gene reproduces — SLC26A5 γ+A4 recompute from the FROZEN cache and equal the atlas
      bit-for-bit, with A4 orthogonality |mean(shape)|<1e-9 (A4 = signal − γ).
  G3  cube-root fixed point [F] — the INHERITED cubic sdot(s,0,F) vanishes at s=F^(1/3) (residual
      <1e-9 across decades): the cube root IS the inherited cubic's critical fixed point, parameter-free.
  G4  compression exponent [V] — the inherited integrator settle(0,F) fits exponent = 1/3 (|Δ|<1e-6)
      on the converged drive range; the exponent is read off, not imposed.
  G5  two regimes — g=γ_TMC1 gives an all-or-none flip across the spinodal (E1 switch); g=0 gives the
      continuous compressive cube root s=h^(1/3) (E3 amplifier). One cubic, two regimes.
  G6  gain compression — gain r/F fits exponent = −2/3 (|Δ|<1e-6): faint drives amplified more than loud.
  G7  placement + honesty — SLC26A5 emerges between PCDH15 and ATOH1 in argsort(spinodal(γ)); and the
      absolute gain/Q/dB are declared [O] with an obstacle named in run.py (VP-SPEC C3).
"""
import os, sys, json, math, subprocess, hashlib, importlib.util
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_substrate as SUB


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# both increments ship a file called run.py — load each under a UNIQUE name to avoid a sys.modules clash
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))
E3 = _load("e3_run", os.path.join(_HERE, "run.py"))


def _hash_once():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "run.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")][-1]
    return line.split("sha256:")[1].strip()


def main():
    print("=" * 80); print("E3 GATE — vp_ear_emergence_seed / E3 (cochlear amplifier, cube-root compression)"); print("=" * 80)
    ok = True

    # G1 determinism
    h1, h2 = _hash_once(), _hash_once()
    g = (h1 == h2); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G1 determinism — 2×sha256 identical ({h1[:16]})")

    # G2 amplifier gene reproduces (read_measured asserts cache==atlas & A4⊥)
    amp = E1.read_measured(E3.AMPLIFIER)
    g = (amp["sym"] == "SLC26A5" and amp["node"] == "cochlear_amplifier"); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G2 amplifier gene — {amp['sym']} γ+A4 == atlas, A4=signal−γ, "
          f"node={amp['node']}")

    # G3 cube-root fixed point of the inherited cubic at criticality
    max_res = max(abs(SUB.sdot((10.0 ** e) ** (1 / 3), 0.0, 10.0 ** e)) for e in range(-3, 4))
    g = (max_res < 1e-9); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G3 cube-root fixed point — inherited sdot(F^(1/3),0,F)≈0 "
          f"(max|res|={max_res:.1e})")

    # G4 compression exponent from the inherited integrator
    Fs = E3.drive_grid()
    rs = [SUB.settle(0.0, F, n=E3._SETTLE_N, dt=0.01) for F in Fs]
    slope = float(np.polyfit(np.log10(Fs), np.log10(rs), 1)[0])
    g = (abs(slope - 1.0 / 3.0) < 1e-6); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G4 compression exponent — fit = {slope:.6f} (1/3; |Δ|={abs(slope-1/3):.1e})")

    # G5 two regimes
    g_sw = E1.read_measured("TMC1")["gamma"]; sp = SUB.spinodal(g_sw)
    switch_flips = (not SUB.is_on(g_sw, 0.99 * sp)) and SUB.is_on(g_sw, 1.01 * sp)
    amp_cube     = abs(SUB.settle(0.0, sp, n=E3._SETTLE_N) - sp ** (1 / 3)) < 1e-6
    g = (switch_flips and amp_cube); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G5 two regimes — switch all-or-none ({switch_flips}); "
          f"amplifier cube root ({amp_cube})")

    # G6 gain compression exponent
    gains = [rs[i] / Fs[i] for i in range(len(Fs))]
    gslope = float(np.polyfit(np.log10(Fs), np.log10(gains), 1)[0])
    g = (abs(gslope - (-2.0 / 3.0)) < 1e-6); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G6 gain compression — fit = {gslope:.6f} (−2/3; |Δ|={abs(gslope+2/3):.1e})")

    # G7 placement + honesty ([O] declared with obstacle)
    rows = sorted((E1.read_measured(s) for s in E3.LINEAGE), key=lambda r: r["spinodal"])
    order = [r["sym"] for r in rows]; i = order.index("SLC26A5")
    placed = (order[i - 1] == "PCDH15" and order[i + 1] == "ATOH1")
    src = open(os.path.join(_HERE, "run.py"), encoding="utf-8").read()
    honest = ("[O]" in src and "Q" in src and ("OAE" in src or "otoacoustic" in src) and "N1" in src)
    g = (placed and honest); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G7 placement PCDH15<SLC26A5<ATOH1 ({placed}); gain/Q/dB [O] "
          f"declared ({honest})")

    print("=" * 80); print(f"E3 GATE: {'PASS' if ok else 'FAIL'}"); print("=" * 80)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
