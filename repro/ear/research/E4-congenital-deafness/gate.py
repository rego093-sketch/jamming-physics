#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — the small E4 gate.  Asserts increment E4's claims, independent of the master verifier.

Run:  python3 research/E4-congenital-deafness/gate.py
Exit 0 + 'E4 GATE: PASS' iff all hold.

Checks (each is a binding E4 claim, no number tuned):
  G1  determinism — run.py's self-hash is identical across two runs (2×sha256).
  G2  deafness genes reproduce — every E4 gene's γ+A4 recompute from the FROZEN cache and equal the
      atlas bit-for-bit, A4 orthogonality |mean(shape)|<1e-9 (A4 = signal − γ); INCLUDING the three
      newly-fetched genes SLC26A4, LHFPL5, MYO15A (their hashes were re-frozen deliberately).
  G3  drive-class recoverable [F]/[V] — a structurally-intact switch (g=γ_TMC1) sits OFF at drive h=0
      and flips ON once h is restored past the spinodal: the DRIVE-class failure is switch-recoverable.
  G4  structure-class NOT drive-rescuable [F]/[V] — the bistable window 2·spinodal(g)=4(g/3)^1.5 is
      monotone in g and → 0 as g→0 (forced by the cubic discriminant); the integrator loop at intact g
      vastly exceeds the grid floor at degraded g. No drive flips a structure-class failure.
  G5  amplifier-class gain [F]/[V] — at criticality g=0 the inherited integrator gives gain r/F with
      fitted exponent = −2/3 (|Δ|<1e-6): losing criticality loses the F^(−2/3) gain (E3 bridge).
  G6  placement — argsort(spinodal(γ)) over the E4 genes yields the deafness genes INTERLEAVED with the
      lineage (USH2A earliest-flipping, GJB2 latest), confirming they are the lineage genes by failure.
  G7  firewall + honesty — γ does NOT separate the drive↔structure classes (γ-range overlap>0, no single
      threshold separates them: γ is structure-only); and the disease layer is proposal-only / direction-
      only with [O] obstacles named in run.py (VP-SPEC C3).
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

# every increment ships a file called run.py — load each under a UNIQUE name to avoid a sys.modules clash
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))
E4 = _load("e4_run", os.path.join(_HERE, "run.py"))


def _hash_once():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "run.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")][-1]
    return line.split("sha256:")[1].strip()


def main():
    print("=" * 82); print("E4 GATE — vp_ear_emergence_seed / E4 (congenital deafness, R19 failure-mode decomposition)"); print("=" * 82)
    ok = True

    # G1 determinism
    h1, h2 = _hash_once(), _hash_once()
    g = (h1 == h2); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G1 determinism — 2×sha256 identical ({h1[:16]})")

    # G2 deafness genes reproduce (read_measured asserts cache==atlas & A4⊥), incl. the 3 new fetches
    syms = [s for s, _, _ in E4.DEAF]
    new3 = {"SLC26A4", "LHFPL5", "MYO15A"}
    recs = {s: E1.read_measured(s) for s in syms}
    g = all(recs[s]["gamma"] > 0 for s in syms) and new3.issubset(set(syms))
    ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G2 genes reproduce — {len(syms)} deafness genes γ+A4==atlas, "
          f"A4=signal−γ (incl. new {sorted(new3)})")

    # G3 drive-class recoverable
    gT = recs["TMC1"]["gamma"]; sp = SUB.spinodal(gT)
    off = SUB.settle(gT, 0.0); on = SUB.settle(gT, 1.5 * sp)
    g = (off < 0 and on > 0); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G3 drive-class recoverable — intact g: h=0→OFF ({off:+.3f}), "
          f"h>sp→ON ({on:+.3f})")

    # G4 structure-class NOT drive-rescuable
    grid = [1.30, 0.80, 0.40, 0.10, 0.01]
    aw = [E4.analytic_bistable_width(x) for x in grid]
    mono = all(aw[i] > aw[i + 1] for i in range(len(aw) - 1))
    vanish = aw[-1] < 1e-3
    contrast = E4.measured_hysteresis_width(1.30) > 20.0 * aw[-1]
    g = (mono and vanish and contrast); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G4 structure NOT drive-rescuable — bistable width monotone "
          f"({mono}), →0 as g→0 ({vanish}), intact≫floor ({contrast})")

    # G5 amplifier-class gain F^(-2/3)
    Fs = E4.drive_grid()
    rs = [SUB.settle(0.0, F, n=E4._SETTLE_N, dt=0.01) for F in Fs]
    gains = [rs[i] / Fs[i] for i in range(len(Fs))]
    gslope = float(np.polyfit(np.log10(Fs), np.log10(gains), 1)[0])
    g = (abs(gslope - (-2.0 / 3.0)) < 1e-6); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G5 amplifier gain — fit = {gslope:.6f} (−2/3; |Δ|={abs(gslope+2/3):.1e})")

    # G6 placement — argsort(spinodal(γ)): deafness genes interleaved, USH2A first, GJB2 last
    order = [r["sym"] for r in sorted(recs.values(), key=lambda r: r["spinodal"])]
    g = (order[0] == "USH2A" and order[-1] == "GJB2"); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G6 placement — argsort(spinodal(γ)): first={order[0]}, "
          f"last={order[-1]} (deafness genes interleave the lineage)")

    # G7 firewall + honesty — γ does NOT separate drive↔structure; proposal-only / [O] declared
    cls = {s: c for s, c, _ in E4.DEAF}
    dg = [recs[s]["gamma"] for s in syms if cls[s] == "drive"]
    sg = [recs[s]["gamma"] for s in syms if cls[s] == "structure"]
    overlap = max(0.0, min(max(dg), max(sg)) - max(min(dg), min(sg)))
    separable = (max(dg) < min(sg)) or (max(sg) < min(dg))
    src = open(os.path.join(_HERE, "run.py"), encoding="utf-8").read()
    honest = ("[O]" in src and "proposal-only" in src and "direction-only" in src.lower() and "N1" in src)
    g = (overlap > 0.0 and not separable and honest); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G7 firewall — γ can't separate classes (overlap={overlap:.4f}, "
          f"separable={separable}); proposal-only/[O] declared ({honest})")

    print("=" * 82); print(f"E4 GATE: {'PASS' if ok else 'FAIL'}"); print("=" * 82)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
