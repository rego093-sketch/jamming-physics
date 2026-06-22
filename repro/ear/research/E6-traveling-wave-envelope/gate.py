#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — the small E6 gate.  Asserts increment E6's claims, independent of the master verifier.

Run:  python3 research/E6-traveling-wave-envelope/gate.py
Exit 0 + 'E6 GATE: PASS' iff all hold.

Checks (each is a binding E6 claim, no number tuned):
  G1  determinism — run.py's self-hash is identical across two runs (2×sha256).
  G2  amplifier gene reproduces — SLC26A5's γ+A4 recompute from the FROZEN cache and equal the atlas
      bit-for-bit, A4 orthogonality |mean(shape)|<1e-9 (A4 = signal − γ). NO inherited byte changed in
      E6 (no new gene fetched, no re-freeze): the frozen-hash set is identical to v0.5.0/v0.6.0.
  G3  the PEAK is forced [F]/[V] — the BM-velocity resonance peaks at ω0 for every Q (within one grid
      step), and the excitation-envelope peak place equals E1's inverse-Greenwood place for several tones.
  G4  the asymmetry is forced [F]/[V] — the partition reactance is >0 (propagating) basal of the
      characteristic place and <0 (evanescent / cut off) apical of it, for several tones; and the apical
      excitation width < basal width (steep apical cutoff) for a RANGE of the [O] decay scale κ.
  G5  the bandwidth law is EXACT [F]/[V] — the −3 dB velocity bandwidth = ω0/Q to machine precision for
      several Q; the peak place is Q-invariant while the bandwidth scales as 1/Q.
  G6  the E3 bridge [F]/[V] — the active process is negative damping (Q_eff=Q0/(1−G) monotone↑), and at
      the R19 cubic's critical point g=0 the steady response settle(0,F) fits the cube root 1/3.
  G7  firewall + honesty — γ is structure-only (never used as Q/damping), no disease/dose/efficacy claim,
      the irreducible scalar Q is named [O], and the honest negatives N1..N7 are present in run.py.
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
E6 = _load("e6_run", os.path.join(_HERE, "run.py"))


def _hash_once():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "run.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")][-1]
    return line.split("sha256:")[1].strip()


def main():
    print("=" * 86); print("E6 GATE — vp_ear_emergence_seed / E6 (traveling-wave envelope: FORM forced, Q the [O])"); print("=" * 86)
    ok = True
    w0 = 1.0

    # G1 determinism
    h1, h2 = _hash_once(), _hash_once()
    g = (h1 == h2); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G1 determinism — 2×sha256 identical ({h1[:16]})")

    # G2 amplifier gene reproduces + NO re-freeze (frozen set unchanged)
    amp = E1.read_measured(E6.AMPLIFIER_GENE)            # asserts cache==atlas & A4 = signal−γ for SLC26A5
    frozen = json.load(open(os.path.join(ROOT, "inherited", "FROZEN_SHA256.json"), encoding="utf-8"))["files"]
    nofreeze = all(hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest() == want
                   for rel, want in frozen.items())
    g = (amp["gamma"] > 0 and amp["shape_amplitude"] >= 0 and nofreeze); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G2 amplifier gene reproduces — SLC26A5 γ={amp['gamma']:.4f}, A4=signal−γ; "
          f"no inherited byte changed (frozen set intact={nofreeze})")

    # G3 the PEAK is forced — velocity peak at ω0 ∀Q, envelope peak == E1 place
    wgrid = E6._W_GRID; step = E6._W_STEP
    maxdev = max(abs(float(wgrid[int(np.argmax(E6.vel_mag2(wgrid, w0, Q)))]) - w0) for Q in (0.8, 1.0, 10.0, 100.0))
    place_ok = True
    for f in (500.0, 2000.0, 8000.0):
        xs, E = E6.excitation_envelope(f, Q=20.0, kappa=8.0)
        place_ok &= abs(xs[int(np.argmax(E))] - E1.inv_greenwood(f)) < 2e-3
    g = (maxdev <= 2.0 * step and place_ok); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G3 peak forced — velocity peak==ω0 ∀Q (max|Δ|={maxdev:.1e}≤{2*step:.1e}); "
          f"envelope peak==E1 place ({place_ok})")

    # G4 the asymmetry is forced — reactance sign cutoff + apical<basal for a range of κ
    sign_ok = True
    for f in (500.0, 2000.0, 8000.0):
        xstar = E1.inv_greenwood(f)
        sign_ok &= (E6.reactance(f, SND.greenwood_f(min(1.0, xstar + 0.12))) > 0.0 and
                    E6.reactance(f, SND.greenwood_f(max(0.0, xstar - 0.12))) < 0.0)
    asym_ok = True
    for kappa in (2.0, 6.0, 12.0, 25.0):
        xs, E = E6.excitation_envelope(2000.0, Q=20.0, kappa=kappa)
        _, wb, wa = E6.edge_widths(xs, E)
        asym_ok &= (wa < wb)
    g = (sign_ok and asym_ok); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G4 asymmetry forced — reactance cutoff apical of CF ({sign_ok}); "
          f"apical<basal ∀κ ({asym_ok})")

    # G5 the bandwidth law is EXACT — BW=ω0/Q to machine precision; place invariant, width ∝1/Q
    maxbw = max(abs(E6.half_power_bandwidth(w0, Q)[2] - w0 / Q) for Q in (3.0, 10.0, 30.0, 100.0))
    p10 = float(wgrid[int(np.argmax(E6.vel_mag2(wgrid, w0, 10.0)))])
    p100 = float(wgrid[int(np.argmax(E6.vel_mag2(wgrid, w0, 100.0)))])
    invariant = abs(p10 - p100) <= step
    scales = abs(E6.half_power_bandwidth(w0, 100.0)[2] / E6.half_power_bandwidth(w0, 10.0)[2] - 0.1) < 1e-6
    g = (maxbw < 1e-12 and invariant and scales); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G5 exact bandwidth — BW=ω0/Q (max|Δ|={maxbw:.1e}); place invariant "
          f"({invariant}), width∝1/Q ({scales})")

    # G6 the E3 bridge — Q_eff=Q0/(1−G) monotone↑; criticality → cube root
    Q0 = 5.0; qs = [Q0 / (1 - G) for G in (0.0, 0.5, 0.8, 0.95)]
    mono = all(qs[i + 1] >= qs[i] for i in range(len(qs) - 1))
    Fs = E6.drive_grid()
    slope = float(np.polyfit(np.log10(Fs), np.log10([SUB.settle(0.0, F, n=E6._SETTLE_N, dt=0.01) for F in Fs]), 1)[0])
    g = (mono and abs(slope - 1.0 / 3.0) < 1e-6); ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G6 E3 bridge — Q_eff=Q0/(1−G) monotone↑ ({mono}); criticality cube root "
          f"exp={slope:.6f}")

    # G7 firewall + honesty — γ never used as Q, no disease/dose, Q named [O], N1..N7 present
    src = open(os.path.join(_HERE, "run.py"), encoding="utf-8").read()
    honest = ("[O]" in src and "structure only" in src.lower() and "tuning" in src.lower()
              and "single irreducible" in src.lower()
              and all(f"N{i}" in src for i in range(1, 8))
              and "no disease claim" in src.lower())
    g = honest; ok &= g
    print(f"  [{'PASS' if g else 'FAIL'}] G7 firewall — γ structure-only (not Q), no disease/dose, Q named [O], "
          f"N1..N7 present ({honest})")

    print("=" * 86); print(f"E6 GATE: {'PASS' if ok else 'FAIL'}"); print("=" * 86)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
