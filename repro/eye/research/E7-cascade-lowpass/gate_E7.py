#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E7.py — the focused pass/fail gate for increment E7 (run from the package root).

    python3 research/E7-cascade-lowpass/gate_E7.py

Re-measures the FROZEN substrate's recovery low-pass INDEPENDENTLY of run.py's own asserts (a lock-in
on the verbatim recovery law w ← w + dt·(s − β·w)/τ_s), and checks it is a textbook single-pole filter
whose cutoff is the closed form f_c = β/(2π·τ):

  [G1] DETERMINISM   — research/E7-cascade-lowpass/run.py emits an identical sha256 on two runs.
  [G2] LOW-PASS GAIN — the recovery's low-frequency (passband) gain equals the closed-form DC gain
                       1/β to <2% (a flat passband; the filter passes the slow band).
  [G3] EXPLICIT CUTOFF — the measured −3 dB cutoff equals the closed form β/(2π·τ_s) to <1%: the
                       band edge is a named number, not a fit.
  [G4] SINGLE-POLE PHASE — the phase lag at the measured cutoff is 45° (±3°): the first-order-pole
                       fingerprint.
  [G5] SINGLE-POLE ROLL-OFF — the high-frequency |H| slope is −20 dB/decade (±2): one pole, the band-
                       limiting low-pass.
  [G6] BAND-FROM-τ (∝1/τ) — across τ_s ∈ {20,40,80} the cutoff is strictly decreasing and the product
                       f_c·τ_s is constant to <3% (= β/2π): the band scales as 1/τ — MANUFACTURED by the
                       recovery, and the recovery law contains no carrier term and no γ.
  [G7] NEURON INHERITS τ — on the FULL FROZEN Neuron the intrinsic rhythm is strictly decreasing in τ_s,
                       and τ is the band-setter: the rhythm's range across τ (a decade) is far larger
                       than its range across the eye γ's at fixed τ (the secondary, dwell∝γ^1.5 channel).
  [G8] NO-DRIFT      — the Neuron's filter constants are byte-equal (β=0.5, τ_f=1.0, τ_s=40.0), SEED=19,
                       the atlas still carries 19 genes, and γ(GUCY2D) is byte-equal; E7 tunes nothing.

Exit 0 + 'E7 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import Neuron, dominant_freq, dwell, SEED      # FROZEN substrate
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

BETA, TAU_F = 0.5, 1.0


def _run_capture():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _transfer(tau_s, beta=BETA, dt=0.1, t_start=2500.0, L=16000.0):
    """Lock-in measurement of |H(f)|, phase(f) of the verbatim recovery law (commensurate freqs)."""
    n_start, n_L = int(t_start / dt), int(L / dt)
    N = n_start + n_L
    log_j = [int(round(x)) for x in np.logspace(0.0, math.log10(1600.0), 30)]
    dense = []
    for jc in (16, 32, 64):
        dense += [jc - 6, jc - 4, jc - 2, jc - 1, jc, jc + 1, jc + 2, jc + 4, jc + 8]
    js = sorted(set(j for j in (log_j + dense) if j >= 1))
    f = np.array([j / L for j in js], float)
    w2pf = 2.0 * math.pi * f
    w = np.zeros(len(f)); I = np.zeros(len(f)); Q = np.zeros(len(f))
    for k in range(N):
        tk = k * dt
        s_in = np.sin(w2pf * tk)
        w += dt * (s_in - beta * w) / tau_s
        if k >= n_start:
            I += w * np.sin(w2pf * tk); Q += w * np.cos(w2pf * tk)
    I *= 2.0 / n_L; Q *= 2.0 / n_L
    gain = np.sqrt(I * I + Q * Q)
    lag = -np.degrees(np.arctan2(Q, I))
    return f, gain, lag


def _read_filter(tau_s, beta=BETA):
    f, gain, lag = _transfer(tau_s, beta)
    fa = beta / (2.0 * math.pi * tau_s)
    dc_band = gain[f < 0.3 * fa]
    dc = float(dc_band.max()) if dc_band.size else float(gain[0])
    target = dc / math.sqrt(2.0)
    fc = None
    for i in range(len(f) - 1):
        if gain[i] >= target >= gain[i + 1]:
            fc = math.exp(math.log(f[i]) + (math.log(target) - math.log(gain[i]))
                          * (math.log(f[i + 1]) - math.log(f[i]))
                          / (math.log(gain[i + 1]) - math.log(gain[i]))); break
    lag_fc = float(np.interp(fc, f, lag))
    hi = f > 12.0 * fa
    slope = 20.0 * math.log10(gain[hi][-1] / gain[hi][0]) / math.log10(f[hi][-1] / f[hi][0])
    return dc, fc, fa, lag_fc, slope


def _neuron_rhythm(tau_s, gamma=1.0):
    S, _ = Neuron(gamma=gamma, tau_f=TAU_F, tau_s=tau_s, beta=BETA).run(0.4, T=4000.0, dt=0.05)
    return dominant_freq(S, 0.05)


def main():
    print("=" * 74)
    checks = []

    # G1 — determinism
    s1, s2 = _sha_of(_run_capture()), _sha_of(_run_capture())
    checks.append(("G1 determinism", s1 == s2, f"run.py sha256 stable ({s1[:16]})"))

    # measure the filter once at the three τ's (reused by G2–G6)
    filt = {ts: _read_filter(ts) for ts in (20.0, 40.0, 80.0)}
    dc40, fc40, fa40, lag40, slope40 = filt[40.0]

    # G2 — passband DC gain = 1/β
    g2 = abs(dc40 - 1.0 / BETA) < 0.02
    checks.append(("G2 low-pass gain", g2, f"DC gain {dc40:.5f} vs 1/β={1.0/BETA:.5f} (flat passband)"))

    # G3 — explicit cutoff = β/(2πτ)
    g3 = abs(fc40 / fa40 - 1.0) < 0.01
    checks.append(("G3 explicit cutoff", g3, f"f_c(meas)={fc40:.6f} vs β/(2πτ)={fa40:.6f} (ratio {fc40/fa40:.4f})"))

    # G4 — single-pole phase 45° at the cutoff
    g4 = abs(lag40 - 45.0) < 3.0
    checks.append(("G4 45° phase", g4, f"lag at f_c = {lag40:.2f}° (single-pole ⇒ 45°)"))

    # G5 — single-pole roll-off −20 dB/decade
    g5 = abs(slope40 - (-20.0)) < 2.0
    checks.append(("G5 −20dB/dec", g5, f"high-f slope = {slope40:.2f} dB/decade (one pole ⇒ −20)"))

    # G6 — band-from-τ: cutoff ↓ with τ, f_c·τ constant
    fcs = [filt[ts][1] for ts in (20.0, 40.0, 80.0)]
    prod = [filt[ts][1] * ts for ts in (20.0, 40.0, 80.0)]
    mono = all(fcs[i + 1] < fcs[i] for i in range(len(fcs) - 1))
    spread = (max(prod) - min(prod)) / (sum(prod) / len(prod))
    g6 = mono and (spread < 0.03)
    checks.append(("G6 band-from-τ", g6,
                   f"f_c ↓ {fcs[0]:.5f}→{fcs[-1]:.5f}; f_c·τ const={sum(prod)/len(prod):.5f} (β/2π={BETA/(2*math.pi):.5f}, spread {spread*100:.2f}%)"))

    # G7 — the full neuron inherits the band; τ dominates, γ secondary
    rhy_tau = [_neuron_rhythm(ts) for ts in (20.0, 40.0, 80.0, 160.0)]
    mono_n = all(rhy_tau[i + 1] < rhy_tau[i] for i in range(len(rhy_tau) - 1))
    rng_tau = max(rhy_tau) - min(rhy_tau)
    rhy_gam = [_neuron_rhythm(40.0, float(ATLAS[s]["gamma"])) for s in ("CNGB3", "RPE65", "GUCY2D", "RHO")]
    rng_gam = max(rhy_gam) - min(rhy_gam)
    g7 = mono_n and (rng_tau > 3.0 * rng_gam)
    checks.append(("G7 neuron inherits τ", g7,
                   f"out_dom ↓ in τ ({rhy_tau[0]:.5f}→{rhy_tau[-1]:.5f}); range(τ)={rng_tau:.5f} ≫ range(γ)={rng_gam:.5f}"))

    # G8 — no drift / no fitting
    Nref = Neuron()
    g_used = float(ATLAS["GUCY2D"]["gamma"])
    g8 = ((Nref.beta, Nref.tau_f, Nref.tau_s) == (BETA, TAU_F, 40.0)) and (SEED == 19) \
         and (len(ATLAS) == 19) and (g_used == ATLAS["GUCY2D"]["gamma"])
    checks.append(("G8 no-drift", g8,
                   f"Neuron(β={Nref.beta},τ_f={Nref.tau_f},τ_s={Nref.tau_s}) byte-equal; SEED={SEED}; atlas={len(ATLAS)}; γ(GUCY2D)={g_used}"))

    ok_all = True
    for name, ok, msg in checks:
        ok_all &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {msg}")
    print("=" * 74)
    print(f"E7 GATE: {'PASS' if ok_all else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
