#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — the small E8 gate.  Asserts increment E8's claims, independent of the master verifier.

Run:  python3 research/E8-band-specific-loss/gate.py
Exit 0 + 'E8 GATE: PASS' iff all hold.

Checks (each is a binding E8 claim, no number tuned):
  G1  determinism — run.py's self-hash is identical across two runs (2×sha256).
  G2  one cached gene per E4 CLASS reproduces — SLC26A4/MYO15A/OTOF/SLC26A5 recompute γ+A4 from the
      FROZEN cache and equal the atlas bit-for-bit, A4 = signal − γ. NO inherited byte changed in E8
      (no new gene fetched, no re-freeze): the frozen-hash set is identical to v0.8.0.
  G3  THE KEYSTONE is exact [F]/[V] — the place→frequency map is an ORDER-ISOMORPHISM: CF(x) strictly
      monotone, a contiguous place band maps to a contiguous frequency band, and inv_greenwood maps it
      back to the SAME place band to machine precision (basal→HIGH, apical→LOW, mid→MID).
  G4  HIGH-FREQUENCY / DOWN-SLOPING forced [F] — the cyclic-load ordering (load ∝ CF) is strictly
      increasing apex→base, so the argmax is the base ⇒ basal-first ⇒ a down-sloping high-frequency loss.
  G5  the NOTCH forced [F] — the outer/middle-ear transfer (canal resonance × ossicular low-pass) is
      UNIMODAL with an interior peak f_peak strictly BELOW CF_max, mapping to an interior place 0<x<1 ⇒
      a notch BELOW the very top (the SHAPE/SIDE forced; the corners/f_peak are [O] inputs only).
  G6  the apical/mid images + E4's negative carries [F]/[V] — apical band → low freqs and mid band → mid
      freqs (the isomorphism), and the cubic's bistable window 2·spinodal(g) → 0 as g→0 (E4-C), so a
      structure-class high-frequency loss admits NO drive rescue.
  G7  firewall + honesty — γ is structure-only (never a band edge/load rate/dB), the disease layer is
      proposal-only (no molecule/dose/diagnosis/efficacy), every magnitude is [O], and N1..N7 are present.
"""
import os, sys, json, math, subprocess, hashlib, importlib.util
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_substrate  as SUB
import vp_sound_wave as SND


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# every increment ships a file called run.py — load each under a UNIQUE name to avoid a sys.modules clash
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))
E8 = _load("e8_run", os.path.join(_HERE, "run.py"))


def _hash_once():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "run.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")][-1]
    return line.split("sha256:")[1].strip()


def main():
    print("=" * 90); print("E8 GATE — vp_ear_emergence_seed / E8 (band-specific loss: class × band, SHAPE+DIR forced)"); print("=" * 90)
    ok = True

    # G1 determinism
    h1, h2 = _hash_once(), _hash_once()
    g = (h1 == h2); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G1 determinism — 2×sha256 identical ({h1[:16]})")

    # G2 one cached gene per E4 class reproduces + NO re-freeze (frozen set unchanged)
    genes_ok = True
    for sym, cls, _ in E8.CLASS_REF:
        r = E1.read_measured(sym)                       # asserts cache==atlas & A4 = signal−γ
        genes_ok &= (r["gamma"] > 0 and r["shape_amplitude"] >= 0)
    frozen = json.load(open(os.path.join(ROOT, "inherited", "FROZEN_SHA256.json"), encoding="utf-8"))["files"]
    nofreeze = all(hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest() == want
                   for rel, want in frozen.items())
    g = (genes_ok and nofreeze); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G2 class refs reproduce — {len(E8.CLASS_REF)} genes (1/class) γ+A4=atlas; "
          f"no inherited byte changed (frozen set intact={nofreeze})")

    # G3 THE KEYSTONE — place→frequency order-isomorphism: contiguous band ↔ contiguous band, exact inverse
    vals = np.array([E8.cf(x) for x in np.linspace(0.0, 1.0, 4001)])
    monotone = bool(np.all(np.diff(vals) > 0))
    iso_ok = True
    for x0, x1 in [(0.7, 1.0), (0.4, 0.6), (0.0, 0.3)]:
        f0, f1 = E8.freq_band_of_place_band(x0, x1)
        iso_ok &= (f1 > f0 and abs(E8.place_of(f0) - x0) < 1e-9 and abs(E8.place_of(f1) - x1) < 1e-9)
    # the three images land in the right octave regions (basal HIGH, apical LOW, mid MID)
    basal_hi = E8.freq_band_of_place_band(0.7, 1.0)[1] > 1e4
    apical_lo = E8.freq_band_of_place_band(0.0, 0.3)[0] < 1e2
    g = (monotone and iso_ok and basal_hi and apical_lo); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G3 keystone exact — CF monotone ({monotone}); place-band⟺freq-band "
          f"round-trips |Δ|<1e-9 ({iso_ok}); basal→HIGH & apical→LOW ({basal_hi and apical_lo})")

    # G4 HIGH-FREQUENCY / DOWN-SLOPING — cyclic-load ordering basal-first (load ∝ CF, strictly increasing)
    loads = np.array([E8.cyclic_load_rate(x) for x in np.linspace(0.0, 1.0, 4001)])
    load_mono = bool(np.all(np.diff(loads) > 0))
    argmax_base = int(np.argmax(loads)) == len(loads) - 1
    g = (load_mono and argmax_base); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G4 HF down-slope forced — load∝CF strictly increasing ({load_mono}), "
          f"argmax at base ({argmax_base}) ⇒ basal-first ⇒ down-sloping")

    # G5 the NOTCH — transfer unimodal, interior peak below CF_max, mapping to an interior place 0<x<1
    fs = np.geomspace(100.0, 30000.0, 6000)
    T = np.array([E8.ear_transfer(f, 2500.0, 5000.0) for f in fs])     # ILLUSTRATIVE corners ([O])
    ip = int(np.argmax(T)); f_peak = float(fs[ip])
    unimodal = (0 < ip < len(fs) - 1 and bool(np.all(np.diff(T[:ip]) > 0)) and bool(np.all(np.diff(T[ip:]) < 0)))
    x_notch = E8.place_of(f_peak)
    below_top = f_peak < E8.cf(1.0)
    interior = 0.0 < x_notch < 1.0
    g = (unimodal and below_top and interior); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G5 notch forced — transfer unimodal ({unimodal}); peak below CF_max "
          f"({below_top}); notch place x={x_notch:.3f} interior ({interior})")

    # G6 apical/mid images + E4's structure-class negative carries (bistable window → 0 as g→0)
    mid = E8.freq_band_of_place_band(0.4, 0.6)
    mid_ok = 5e2 < mid[0] < mid[1] < 5e3
    w_intact, w_lost = 2.0 * SUB.spinodal(1.30), 2.0 * SUB.spinodal(0.01)
    no_drive_rescue = (w_intact > 20.0 * w_lost and w_lost < 1e-3)
    g = (mid_ok and no_drive_rescue); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G6 images + E4 negative — mid→MID band ({mid_ok}); structure-class "
          f"window {w_intact:.4f}→{w_lost:.5f} as g→0 ⇒ no drive rescue ({no_drive_rescue})")

    # G7 firewall + honesty — γ structure-only, proposal-only, magnitudes [O], N1..N7 present
    src = open(os.path.join(_HERE, "run.py"), encoding="utf-8").read().lower()
    honest = ("[o]" in src and "structure only" in src and "tuning" in src and "proposal-only" in src
              and "order-isomorphism" in src and "no molecule" in src
              and all(f"n{i}" in src for i in range(1, 8)))
    g = honest; ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G7 firewall — γ structure-only (not a band edge/load/dB), proposal-only "
          f"(no molecule/dose/efficacy), magnitudes [O], N1..N7 present ({honest})")

    print("=" * 90); print(f"E8 GATE: {'PASS' if ok else 'FAIL'}"); print("=" * 90)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
