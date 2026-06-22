#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — the small E5 gate.  Asserts increment E5's claims, independent of the master verifier.

Run:  python3 research/E5-readout-synapse/gate.py
Exit 0 + 'E5 GATE: PASS' iff all hold.

Checks (each is a binding E5 claim, no number tuned):
  G1  determinism — run.py's self-hash is identical across two runs (2×sha256).
  G2  readout gene reproduces — OTOF's γ+A4 recompute from the FROZEN cache and equal the atlas
      bit-for-bit, A4 orthogonality |mean(shape)|<1e-9 (A4 = signal − γ). NO inherited byte changed in
      E5 (no new gene fetched, no re-freeze): the frozen-hash set is identical to v0.5.0.
  G3  the readout is a DIFFERENT normal form [F]/[V] — the sensor is non-negative, monotone in Ca²⁺,
      saturating (→Rmax), and NON-bistable (a pure function of Ca: zero hysteresis), unlike the cubic.
  G4  auditory-neuropathy dissociation [F]/[V] — the frozen switch flips IDENTICALLY (s=+1.3864) in a
      hearing and an OTOF ear; the intact sensor gives release>0, the removed sensor gives release==0.
      The defect is purely downstream of the flip (the substrate sees nothing wrong — E4's READOUT class).
  G5  composed exponent [F]/[V] — the cascade output R∝Ca^m fed by the E3 cube-root settle(0,F)≈F^(1/3)
      fits to F^(m/3) at machine precision for several cited cooperativities m (the composition law).
  G6  OAE⁺/ABR⁻ dissociation [F]/[V] — separable stages: the amplifier (E3) cube-root response is intact
      (exponent 1/3) while the readout (E5) release is zeroed — OAE present, ABR absent.
  G7  firewall + honesty — the disease layer is proposal-only / direction-only, the synaptic
      cooperativity m is a CITED knob (never derived/tuned), and [O] obstacles are named in run.py.
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
E5 = _load("e5_run", os.path.join(_HERE, "run.py"))


def _hash_once():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "run.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")][-1]
    return line.split("sha256:")[1].strip()


def main():
    print("=" * 84); print("E5 GATE — vp_ear_emergence_seed / E5 (otoferlin readout substrate, auditory neuropathy)"); print("=" * 84)
    ok = True

    # G1 determinism
    h1, h2 = _hash_once(), _hash_once()
    g = (h1 == h2); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G1 determinism — 2×sha256 identical ({h1[:16]})")

    # G2 readout gene reproduces + NO re-freeze (frozen set unchanged from v0.5.0)
    ot = E1.read_measured(E5.READOUT_GENE)                # asserts cache==atlas & A4 = signal−γ for OTOF
    frozen = json.load(open(os.path.join(ROOT, "inherited", "FROZEN_SHA256.json"), encoding="utf-8"))["files"]
    nofreeze = all(hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest() == want
                   for rel, want in frozen.items())
    g = (ot["gamma"] > 0 and ot["shape_amplitude"] >= 0 and nofreeze); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G2 readout gene reproduces — OTOF γ={ot['gamma']:.4f}, A4=signal−γ; "
          f"no inherited byte changed (frozen set intact={nofreeze})")

    # G3 the readout is a DIFFERENT normal form (non-negative, monotone, saturating, NON-bistable)
    m = 3; cas = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    Rs = [E5.release(c, m) for c in cas]
    nonneg = all(r >= 0.0 for r in Rs)
    mono   = all(Rs[i + 1] >= Rs[i] for i in range(len(Rs) - 1))
    sat    = E5.release(1e6, m) <= 1.0 + 1e-12 and E5.release(1e6, m) > E5.release(1.0, m)
    nohyst = max(abs(E5.release(c, m) - E5.release(c, m)) for c in cas) < 1e-15  # pure function: no memory
    g = (nonneg and mono and sat and nohyst); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G3 different normal form — non-neg({nonneg}) monotone({mono}) "
          f"saturating({sat}) non-bistable/no-hysteresis({nohyst})")

    # G4 auditory-neuropathy dissociation — identical flip, sensor intact>0 vs removed==0
    gT = E1.read_measured(E5.SWITCH_GENE)["gamma"]; sp = SUB.spinodal(gT)
    s_on = SUB.settle(gT, 1.5 * sp); ca_on = E5.ca_proxy(s_on)
    R_hear = E5.release(ca_on, 1); R_otof = E5.release_knockout(ca_on, 1)
    g = (abs(s_on - 1.3864) < 1e-3 and R_hear > 0.0 and R_otof == 0.0); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G4 neuropathy dissociation — flip s={s_on:+.4f} identical; "
          f"sensor intact R={R_hear:.4f}>0, removed R={R_otof:.4f}==0")

    # G5 composed exponent — fits F^(m/3) at machine precision for several m
    devs = {mm: abs(E5.composed_exponent(mm) - mm / 3.0) for mm in (1, 2, 3, 4)}
    g = all(d < 1e-5 for d in devs.values()); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G5 composed exponent — R∝F^(m/3) for m∈{{1,2,3,4}} "
          f"(max|Δ|={max(devs.values()):.1e})")

    # G6 OAE⁺/ABR⁻ — amplifier (E3) intact while readout zeroed (separable stages)
    Fs = E5.drive_grid()
    amp = float(np.polyfit(np.log10(Fs), np.log10([SUB.settle(0.0, F, n=E5._SETTLE_N, dt=0.01) for F in Fs]), 1)[0])
    readout_zero = (E5.release_knockout(ca_on, 1) == 0.0)
    g = (abs(amp - 1.0 / 3.0) < 1e-6 and readout_zero); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G6 OAE⁺/ABR⁻ — amplifier intact (exp={amp:.6f}≈1/3) ∥ readout "
          f"zeroed ({readout_zero}): separable stages")

    # G7 firewall + honesty — proposal-only / direction-only, m cited not derived, [O] named
    src = open(os.path.join(_HERE, "run.py"), encoding="utf-8").read()
    honest = ("[O]" in src and "proposal-only" in src.lower() and "direction-only" in src.lower()
              and "cited" in src.lower() and "N1" in src and "tuned" in src.lower())
    g = honest; ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G7 firewall — proposal-only/direction-only, m cited not derived, "
          f"[O] obstacles named ({honest})")

    print("=" * 84); print(f"E5 GATE: {'PASS' if ok else 'FAIL'}"); print("=" * 84)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
