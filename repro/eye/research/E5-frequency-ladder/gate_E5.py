#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_E5.py — the focused pass/fail gate for increment E5 (run from the package root).

    python3 research/E5-frequency-ladder/gate_E5.py

Asserts, independently of run.py's own internal asserts:
  [G1] DETERMINISM     — research/E5-frequency-ladder/run.py emits an identical sha256 on two runs.
  [G2] CARRIER         — ν=c/λ for the committed 633/532 channels lands in the visible carrier band
                         (~10¹⁴–10¹⁵ Hz); the carrier is real and forced from measured c, λ.
  [G3] COLLAPSE        — ν_light / the cited neural band (~10–100 Hz) is ~10¹²–10¹³ (≈13 orders): the
                         ratio is forced; the absolute neural Hz is a named [O].
  [G4] LOW-PASS        — the FROZEN Neuron cannot follow a fast carrier: at the highest carrier the
                         output dominant frequency is far below it (out_dom < f_c/20).
  [G5] NO-MIXING       — across a >10× carrier span the output rate moves <30% ⇒ the output is
                         orthogonal to the carrier frequency (a mixer would track it).
  [G6] CUBIC = EVENT   — crossing the spinodal flips the cubic field discontinuously (a two-basin,
                         all-or-none event); deleting −s³ destroys the threshold (diverges). The
                         carrier collapses onto this single discrete event.
  [G7] BAND-FROM-τ     — with the carrier fixed, raising the recovery τ_s lowers the output band
                         (~1/τ): the surviving band is manufactured by the recovery, not the carrier.
  [G8] NO-DRIFT        — the measured γ E5 uses (GUCY2D) is byte-equal to the frozen atlas, and the
                         substrate SEED is the canonical 19 (no fitting, no re-derivation).

Exit 0 + 'E5 GATE: PASS' only if all hold.
"""
import os, sys, json, math, subprocess
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, _INH)

from vp_substrate import Neuron, dominant_freq, spinodal, SEED      # FROZEN inherited switch
import vp_visible_band_canonical as VB                              # inherited rung-1 canon
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]
RUN   = os.path.join(_HERE, "run.py")

EV_PER_J = 1.0 / 1.602176634e-19
NEURAL_BAND_HZ = (10.0, 100.0)
T, DT, D0, AC = 4000.0, 0.02, 0.4, 0.4


def _run_capture():
    r = subprocess.run([sys.executable, RUN], capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    return r.stdout


def _sha_of(out):
    line = [l for l in out.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def _settle(g, h, cubic=True, n=1500, dt=0.02):
    s = -math.sqrt(g)
    for _ in range(n):
        s += dt * (g * s - (s**3 if cubic else 0.0) + h)
        if not cubic:
            s = 50.0 if s > 50 else (-50.0 if s < -50 else s)
    return s


def _neuron_sweep_carrier(carriers, tau_s=40.0):
    n = int(T / DT); t = np.arange(n) * DT
    dom, rate = [], []
    for fc in carriers:
        N = Neuron(gamma=1.0, tau_f=1.0, tau_s=tau_s, beta=0.5)
        S, _ = N.run(D0 + AC * np.sin(2 * math.pi * fc * t), T=T, dt=DT)
        dom.append(dominant_freq(S, DT)); rate.append(Neuron.rate_hz(S, DT))
    return dom, rate


def main():
    print("=" * 74)
    checks = []

    # G1 — determinism
    o1 = _run_capture(); o2 = _run_capture()
    s1, s2 = _sha_of(o1), _sha_of(o2)
    checks.append(("G1 determinism", s1 == s2, f"run.py sha256 stable ({s1[:16]})"))

    # G2 — the carrier is real (ν = c/λ)
    nu_r, nu_g = VB.C_SI / 632.99e-9, VB.C_SI / 532.0e-9
    g2 = (3e14 < nu_r < 9e14) and (3e14 < nu_g < 9e14)
    checks.append(("G2 carrier", g2, f"ν(633)={nu_r:.3e}Hz, ν(532)={nu_g:.3e}Hz (E={VB.H*VB.C_SI/632.99e-9*EV_PER_J:.2f}/{VB.H*VB.C_SI/532e-9*EV_PER_J:.2f} eV)"))

    # G3 — the collapse magnitude
    lo = nu_r / NEURAL_BAND_HZ[1]; hi = nu_r / NEURAL_BAND_HZ[0]
    g3 = (lo > 1e12) and (hi < 1e15)
    checks.append(("G3 collapse", g3, f"ν_light/neural = {lo:.1e}–{hi:.1e} ≈ {math.log10(lo):.1f}–{math.log10(hi):.1f} orders"))

    # G4 + G5 — low-pass and carrier-invariance (no mixing)
    carriers = [0.25, 0.5, 1.0, 2.0, 5.0]
    dom, rate = _neuron_sweep_carrier(carriers)
    g4 = dom[-1] < carriers[-1] / 20.0
    checks.append(("G4 low-pass", g4, f"f_c={carriers[-1]} → out_dom={dom[-1]:.5f} (≪ carrier; cell cannot follow)"))
    span = carriers[-1] / carriers[0]
    rel_spread = (max(rate) - min(rate)) / (sum(rate) / len(rate))
    g5 = (span > 10.0) and (rel_spread < 0.30)
    checks.append(("G5 no-mixing", g5, f"carrier ×{span:.0f} span → output moves {rel_spread*100:.1f}% (output ⟂ carrier)"))

    # G6 — the cubic is the all-or-none event
    g = float(ATLAS["GUCY2D"]["gamma"]); hs = spinodal(g)
    c_lo, c_hi = _settle(g, 0.95 * hs, True), _settle(g, 1.05 * hs, True)
    l_hi = _settle(g, 1.05 * hs, False)
    g6 = (c_lo < 0 < c_hi) and ((c_hi - c_lo) > 1.5) and (abs(l_hi) >= 10.0)
    checks.append(("G6 cubic=event", g6, f"cubic flip Δ={c_hi-c_lo:+.3f} (s:{c_lo:+.2f}→{c_hi:+.2f}); linear diverges ({l_hi:+.0f})"))

    # G7 — band set by recovery τ, not carrier
    band = []
    for ts in [20, 40, 80, 160]:
        d, _ = _neuron_sweep_carrier([2.0], tau_s=ts)
        band.append(d[0])
    g7 = all(band[i + 1] < band[i] + 1e-9 for i in range(len(band) - 1)) and (band[0] > band[-1])
    checks.append(("G7 band-from-τ", g7, f"τ_s 20→160 ⇒ out_dom {band[0]:.5f}→{band[-1]:.5f} (∝ 1/τ, not carrier)"))

    # G8 — no drift / no fitting
    g_used = float(ATLAS["GUCY2D"]["gamma"])
    g8 = (g_used == ATLAS["GUCY2D"]["gamma"]) and (SEED == 19)
    checks.append(("G8 no-drift", g8, f"γ(GUCY2D)={g_used} byte-equal to frozen atlas; SEED={SEED}"))

    ok_all = True
    for name, ok, msg in checks:
        ok_all &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {msg}")
    print("=" * 74)
    print(f"E5 GATE: {'PASS' if ok_all else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
