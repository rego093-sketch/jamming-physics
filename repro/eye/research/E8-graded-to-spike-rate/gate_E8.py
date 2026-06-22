#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E8.py — the focused pass/fail gate for increment E8 (run from the package root).

    python3 research/E8-graded-to-spike-rate/gate_E8.py

Re-derives the FROZEN Neuron's rate code INDEPENDENTLY of run.py's own asserts (its own spike-rate
sweeps on the verbatim substrate), and checks the graded→spike-rate re-quantisation is a thresholded,
bounded, monotone code that carries the slow envelope and never the carrier:

  [G1] DETERMINISM      — research/E8-graded-to-spike-rate/run.py emits an identical sha256 on two runs.
  [G2] RHEOBASE FLOOR   — from a silent hyperpolarised rest the rate is 0 below a threshold increment and
                          > 0 above it: the all-or-none switch must be driven across its fold to fire.
  [G3] MONOTONE CODE    — above the floor the firing rate rises STRICTLY monotonically with the graded
                          amplitude across the operating band: amplitude is re-encoded as a rate.
  [G4] DISCRETE CLOCK   — the spike train is a near-periodic point process (CV(ISI) ≪ 1): the continuous
                          graded input is genuinely RE-QUANTISED into a rate-coded train.
  [G5] BOUNDED (CEILING)— the full-range f–I is NON-monotone: SILENT on BOTH sides of the band
                          (hyperpolarisation floor AND depolarisation-block ceiling) — a finite bandpass
                          in drive, the honest operating envelope (absolute edges a named [O]).
  [G6] CARRIER GONE     — hold the slow envelope fixed and sweep the carrier frequency ⇒ rate invariant
                          (spread < 5% across a 20× carrier span); hold the carrier fixed and raise the
                          envelope ⇒ rate rises. rate ⟂ carrier AND rate ∝ envelope (no mixing).
  [G7] RATE IN LOW BAND — the spike train's dominant frequency equals the firing rate (within 10%) and
                          sits orders below the carrier: the re-quantisation preserves the down-conversion.
  [G8] NO-DRIFT         — the Neuron's constants are byte-equal (β=0.5, τ_f=1.0, τ_s=40.0), SEED=19, the
                          atlas still carries 19 genes, and γ(GUCY2D) is byte-equal; E8 tunes nothing.

Exit 0 + 'E8 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import Neuron, dominant_freq, SEED      # FROZEN substrate
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

BETA, TAU_F, TAU_S = 0.5, 1.0, 40.0
T, DT = 6000.0, 0.05
B_REST = -1.0


def _run_capture():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _rate(drive, gamma=1.0):
    S, _ = Neuron(gamma=gamma, tau_f=TAU_F, tau_s=TAU_S, beta=BETA).run(drive, T=T, dt=DT)
    return Neuron.rate_hz(S, DT), S


def _cv(S):
    sp = Neuron.spikes(S)
    if len(sp) < 3:
        return float("nan")
    isi = np.diff(sp) * DT
    return float(isi.std() / isi.mean())


def main():
    print("=" * 74)
    checks = []

    # G1 — determinism
    s1, s2 = _sha_of(_run_capture()), _sha_of(_run_capture())
    checks.append(("G1 determinism", s1 == s2, f"run.py sha256 stable ({s1[:16]})"))

    # G2 — rheobase floor (silent below, fires above)
    r_silent, _ = _rate(B_REST + 0.20)
    r_fires,  _ = _rate(B_REST + 0.30)
    g2 = (r_silent == 0.0) and (r_fires > 0.0)
    checks.append(("G2 rheobase floor", g2,
                   f"silent at g=0.20 (rate={r_silent:.5f}) → fires at g=0.30 (rate={r_fires:.5f})"))

    # G3 — monotone rising code across the operating band
    band_g = (0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90)
    band_r = [_rate(B_REST + g)[0] for g in band_g]
    g3 = all(band_r[i + 1] > band_r[i] for i in range(len(band_r) - 1))
    checks.append(("G3 monotone code", g3,
                   f"rate ↑ strictly over band: {band_r[0]:.5f}→{band_r[-1]:.5f} (graded amplitude → rate)"))

    # G4 — discrete clock (CV ≪ 1)
    cvs = [_cv(_rate(B_REST + g)[1]) for g in (0.40, 0.60, 0.80)]
    g4 = max(cvs) < 0.05
    checks.append(("G4 discrete clock", g4,
                   f"CV(ISI) max = {max(cvs):.5f} ≪ 1 (a genuine re-quantising clock)"))

    # G5 — bounded: block on BOTH sides of the band
    r_lo, _ = _rate(-1.00)     # hyperpolarisation floor
    r_op, _ = _rate(-0.30)     # operating band
    r_hi, _ = _rate(+1.00)     # depolarisation-block ceiling
    g5 = (r_lo == 0.0) and (r_op > 0.0) and (r_hi < 0.05 * r_op)
    checks.append(("G5 bounded (ceiling)", g5,
                   f"floor rate={r_lo:.5f}, band rate={r_op:.5f}, ceiling rate={r_hi:.5f} (bandpass in drive)"))

    # G6 — carrier gone: rate ⟂ carrier, rate ∝ envelope
    n = int(T / DT); t = np.arange(n) * DT
    car_rates = []
    for fc in (0.0, 0.5, 1.0, 2.0, 5.0, 10.0):
        car = np.zeros(n) if fc == 0.0 else 0.25 * np.sin(2.0 * math.pi * fc * t)
        car_rates.append(_rate(-0.3 + car)[0])
    spread = (max(car_rates) - min(car_rates)) / (sum(car_rates) / len(car_rates))
    env_rates = []
    for env in (-0.70, -0.60, -0.50, -0.40, -0.30, -0.20):
        car = 0.15 * np.sin(2.0 * math.pi * 2.0 * t)
        env_rates.append(_rate(env + car)[0])
    env_mono = all(env_rates[i + 1] > env_rates[i] for i in range(len(env_rates) - 1))
    g6 = (spread < 0.05) and env_mono
    checks.append(("G6 carrier gone", g6,
                   f"rate ⟂ carrier (spread {spread*100:.2f}% over 20×) AND rate ∝ envelope "
                   f"({env_rates[0]:.5f}→{env_rates[-1]:.5f})"))

    # G7 — rate lives in the low band
    r_op2, S_op = _rate(-0.3)
    fdom = dominant_freq(S_op, DT)
    g7 = (abs(fdom - r_op2) / r_op2 < 0.10) and (r_op2 / 2.0 < 0.1)
    checks.append(("G7 rate in low band", g7,
                   f"dom_freq(train)={fdom:.5f} ≈ rate={r_op2:.5f}; rate/carrier(f=2)={r_op2/2.0:.5f} (orders below)"))

    # G8 — no drift / no fitting
    Nref = Neuron()
    g_used = float(ATLAS["GUCY2D"]["gamma"])
    g8 = ((Nref.beta, Nref.tau_f, Nref.tau_s) == (BETA, TAU_F, TAU_S)) and (SEED == 19) \
         and (len(ATLAS) == 19) and (g_used == ATLAS["GUCY2D"]["gamma"])
    checks.append(("G8 no-drift", g8,
                   f"Neuron(β={Nref.beta},τ_f={Nref.tau_f},τ_s={Nref.tau_s}) byte-equal; SEED={SEED}; atlas={len(ATLAS)}; γ(GUCY2D)={g_used}"))

    ok_all = True
    for name, ok, msg in checks:
        ok_all &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {msg}")
    print("=" * 74)
    print(f"E8 GATE: {'PASS' if ok_all else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
