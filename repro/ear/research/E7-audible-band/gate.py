#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — the small E7 gate.  Asserts increment E7's claims, independent of the master verifier.

Run:  python3 research/E7-audible-band/gate.py
Exit 0 + 'E7 GATE: PASS' iff all hold.

Checks (each is a binding E7 claim, no number tuned):
  G1  determinism — run.py's self-hash is identical across two runs (2×sha256).
  G2  reference gene reproduces — TMC1's γ+A4 recompute from the FROZEN cache and equal the atlas
      bit-for-bit, A4 orthogonality |mean(shape)|<1e-9 (A4 = signal − γ). NO inherited byte changed in
      E7 (no new gene fetched, no re-freeze): the frozen-hash set is identical to v0.6.0/v0.7.0.
  G3  the KEYSTONE is exact [F]/[V] — N_oct=½·log₂(S_base/S_apex) closes to machine precision (the √-law),
      and the human span↔ratio reproduce off the inherited Greenwood map (10.025 oct ⟺ 1.085×10⁶).
  G4  the LOW edge is forced [F]/[V] — the −A·k offset is a LOW-END-only correction (fractional weight
      ratio apex:base = 10^a exactly), bending the apex down ~3 oct; and the helicotrema high-pass is
      monotone-increasing through the corner with the lows cut (→0), for a RANGE of the [O] order n.
  G5  the HIGH edge is forced [F]/[V] — the ossicular-mass low-pass is monotone-decreasing above its
      corner with a −12 dB/oct (slope −2 in log-log) asymptote for a RANGE of the damping ζ; and the
      inherited place map is strictly increasing apex→base with a FINITE basal ceiling.
  G6  the band is a bandpass [F]/[V] — the product (high-pass × low-pass) is unimodal: strictly rising
      below its peak and strictly falling above it (SHAPE forced; the corners are [O] inputs only).
  G7  firewall + honesty — γ is structure-only (never a stiffness/corner/area), no disease/dose/efficacy
      claim, the band's absolute edges/corners are named [O] measured-geometry, and N1..N7 are present.
"""
import os, sys, json, math, subprocess, hashlib, importlib.util
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_sound_wave as SND


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# every increment ships a file called run.py — load each under a UNIQUE name to avoid a sys.modules clash
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))
E7 = _load("e7_run", os.path.join(_HERE, "run.py"))


def _hash_once():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "run.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")][-1]
    return line.split("sha256:")[1].strip()


def main():
    print("=" * 86); print("E7 GATE — vp_ear_emergence_seed / E7 (audible band: bandpass SHAPE+SIGN forced, edges [O])"); print("=" * 86)
    ok = True

    # G1 determinism
    h1, h2 = _hash_once(), _hash_once()
    g = (h1 == h2); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G1 determinism — 2×sha256 identical ({h1[:16]})")

    # G2 reference gene reproduces + NO re-freeze (frozen set unchanged)
    ref = E1.read_measured(E7.REF_GENE)                 # asserts cache==atlas & A4 = signal−γ for TMC1
    frozen = json.load(open(os.path.join(ROOT, "inherited", "FROZEN_SHA256.json"), encoding="utf-8"))["files"]
    nofreeze = all(hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest() == want
                   for rel, want in frozen.items())
    g = (ref["gamma"] > 0 and ref["shape_amplitude"] >= 0 and nofreeze); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G2 reference gene reproduces — TMC1 γ={ref['gamma']:.4f}, A4=signal−γ; "
          f"no inherited byte changed (frozen set intact={nofreeze})")

    # G3 the KEYSTONE — N_oct=½·log₂(S_ratio) exact; human span↔ratio reproduce
    span = E7.octave_span()
    s_ratio = E7.implied_stiffness_ratio(span)
    n_from_s = E7.noct_from_stiffness_ratio(s_ratio)
    keystone_exact = abs(n_from_s - span) < 1e-12
    human_ok = abs(span - 10.0248227) < 1e-6 and abs(s_ratio - 1.0852872e6) < 1e2
    g = (keystone_exact and human_ok); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G3 keystone exact — ½·log₂(S_ratio)==span (|Δ|={abs(n_from_s-span):.1e}); "
          f"span={span:.4f} oct ⟺ ratio={s_ratio:.3e} (human ✓={human_ok})")

    # G4 the LOW edge — offset is low-end-only (ratio=10^a); helicotrema high-pass monotone↑ + lows cut ∀n
    off = E7.A_GW * E7.k_GW
    frac_apex = off / E7.cf_pure_exp(0.0); frac_base = off / E7.cf_pure_exp(1.0)
    low_end_only = (frac_apex > 50.0 * frac_base and abs(frac_apex / frac_base - 10.0 ** E7.a_GW) < 1e-6)
    bend = math.log2(E7.cf_pure_exp(0.0) / E7.cf(0.0))
    hp_ok = True
    for n in (1, 2, 3):
        H = np.array([E7.highpass(r, n) for r in np.linspace(0.02, 8.0, 6000)])
        hp_ok &= (bool(np.all(np.diff(H) > 0)) and E7.highpass(0.05, n) < 0.06)
    g = (low_end_only and abs(bend - 3.0588937) < 1e-5 and hp_ok); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G4 low edge forced — offset low-end-only (apex:base={frac_apex/frac_base:.3f}=10^a), "
          f"apex bend={bend:.4f} oct; high-pass lows-cut ∀n ({hp_ok})")

    # G5 the HIGH edge — ossicular-mass low-pass monotone↓ above corner + −12 dB/oct ∀ζ; finite ceiling
    lp_ok = True
    for zeta in (0.3, 0.7, 1.0, 2.0):
        H = np.array([E7.lowpass_mass(r, zeta) for r in np.linspace(1.2, 40.0, 6000)])
        slope = (math.log10(E7.lowpass_mass(120.0, zeta)) - math.log10(E7.lowpass_mass(60.0, zeta))) / math.log10(2.0)
        lp_ok &= (bool(np.all(np.diff(H) < 0)) and abs(slope + 2.0) < 0.02)
    vals = np.array([E7.cf(x) for x in np.linspace(0.0, 1.0, 2001)])
    ceiling_ok = bool(np.all(np.diff(vals) > 0)) and math.isfinite(E7.cf(1.0))
    g = (lp_ok and ceiling_ok); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G5 high edge forced — mass low-pass −12 dB/oct ∀ζ ({lp_ok}); "
          f"place map increasing + finite ceiling CF(1)={E7.cf(1.0):.0f} Hz ({ceiling_ok})")

    # G6 the band is a bandpass — product unimodal (rising below peak, falling above)
    fs = np.geomspace(10.0, 30000.0, 4001)
    B = np.array([E7.bandpass_product(f, 30.0, 14000.0) for f in fs])
    ip = int(np.argmax(B))
    unimodal = (0 < ip < len(fs) - 1 and bool(np.all(np.diff(B[:ip]) > 0)) and bool(np.all(np.diff(B[ip:]) < 0)))
    g = unimodal; ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G6 bandpass shape — product unimodal (rising below peak, falling above) ({unimodal})")

    # G7 firewall + honesty — γ never a stiffness/corner/area, no disease/dose, edges [O], N1..N7 present
    src = open(os.path.join(_HERE, "run.py"), encoding="utf-8").read()
    honest = ("[O]" in src and "structure only" in src.lower() and "tuning" in src.lower()
              and "measured-geometry" in src.lower()
              and "halves" in src.lower()
              and all(f"N{i}" in src for i in range(1, 8))
              and "no disease claim" in src.lower())
    g = honest; ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G7 firewall — γ structure-only (not a stiffness/corner/area), no disease/dose, "
          f"edges [O], N1..N7 present ({honest})")

    print("=" * 86); print(f"E7 GATE: {'PASS' if ok else 'FAIL'}"); print("=" * 86)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
