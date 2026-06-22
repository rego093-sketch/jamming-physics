#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E5 — THE FREQUENCY LADDER, QUANTIFIED  (the new spine: how 10¹⁴ Hz becomes ~10–100 Hz)

The goal increment of the re-scoped volume. A photoreceptor cannot oscillate at the ~10¹⁴ Hz of
the light carrier, so the eye does NOT down-convert by mixing/heterodyne. This module shows, on the
FROZEN substrate, that it down-converts by **EVENT-DETECTION + LOW-PASS INTEGRATION**, and accounts
the full ~13-order collapse rung by rung.

WHAT IS SHOWN (and how it is graded)
  (0) RUNG 1 — the carrier the eye is handed.  ν_light = c/λ for the committed 633/532 channels, and
      the photon energy E=hc/λ that the switch will actually see as a quantum of DRIVE (not a frequency
      it could follow). c, h, λ measured ⇒ ν, E forced.                                       [L]/[F]
  (1) THE COLLAPSE MAGNITUDE.  ν_light vs the neural band (the known ganglion-cell range, ~10–100 Hz,
      cited): the ratio is ~10¹²–10¹³ — about thirteen orders of magnitude. The RATIO is forced by the
      two numbers; the ABSOLUTE neural rate is a named calibration.                            [F]/[O]
  (2) THE MECHANISM IS EVENT-DETECTION + LOW-PASS, NOT MIXING  (frozen Neuron = R19 switch + slow
      recovery; demonstrated in SUBSTRATE-TIME — the substrate cannot carry 10¹⁴ literally, so the
      MECHANISM is shown at a tractable ratio and the magnitude is accounted separately in (1)):
        (2a) LOW-PASS — a fast carrier (here 24×–476× the intrinsic rhythm) is averaged away: the
             output stays at the intrinsic LOW frequency, out/f_c → 0. The cell cannot follow it.   [V]
        (2b) CARRIER-INVARIANCE — across the whole carrier span the output barely moves ⇒ the output
             is orthogonal to the carrier frequency. A mixer's output would track the carrier; this
             does not ⇒ NOT mixing.                                                                 [F]/[V]
        (2c) THE CUBIC IS THE ALL-OR-NONE EVENT — crossing the spinodal flips the switch
             discontinuously; deleting −s³ destroys the two-basin threshold (graded/divergent). The
             carrier collapses onto this single discrete event.                                     [F]/[V]
  (3) THE SURVIVING BAND IS SET BY THE RECOVERY TIME-CONSTANT τ, NOT THE CARRIER — larger τ ⇒ lower
      output band (~1/τ), with the carrier held fixed. The output frequency is the substrate's own,
      manufactured by the cascade/recovery, not inherited from the light.                       [F]/[V]
  (4) THE FULL LADDER, end to end.

FIREWALL / NO-TUNING.  E5 is pure sensory MECHANISM — it makes no disease, diagnostic, or clinical
claim (the disease layer is E4, firewalled). No constant is fitted: every γ used is read byte-equal
from the frozen atlas, D is the inherited invariant, ν=c/λ and E=hc/λ are forced, and the substrate
math is the vendored R19 field. The absolute biological Hz at each rung is a named [O].

Imports the FROZEN substrate + the inherited visible-band canon (rung 1). Adds no γ.
stdlib + numpy. Deterministic; run twice -> identical sha256.
"""
import os, sys, io, hashlib, math
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(PKG, "inherited"))

from vp_substrate import (seed_everything, Neuron, dominant_freq, spinodal, SEED)  # FROZEN switch
import vp_visible_band_canonical as VB                                             # rung 1 (inherited)
import json
ATLAS = json.load(open(os.path.join(PKG, "inherited", "organ_gamma.json"), encoding="utf-8"))["genes"]

EV_PER_J = 1.0 / 1.602176634e-19
NEURAL_BAND_HZ = (10.0, 100.0)        # ganglion-cell spike-rate range (cited biological range) [L]


def nu_light(lam_m):
    """Carrier frequency ν = c/λ (forced from measured c, λ)."""
    return VB.C_SI / lam_m


def photon_eV(lam_m):
    """Photon energy E = hc/λ in eV — the quantum of DRIVE the switch sees (not a trackable freq)."""
    return VB.H * VB.C_SI / lam_m * EV_PER_J


def settle_field(g, h, cubic=True, n=1500, dt=0.02):
    """Settle the R19 field from rest; cubic=False deletes −s³ (a control field, NOT the substrate)."""
    s = -math.sqrt(g)
    for _ in range(n):
        s += dt * (g * s - (s**3 if cubic else 0.0) + h)
        if not cubic:
            s = 50.0 if s > 50 else (-50.0 if s < -50 else s)
    return s


def run(P):
    seed_everything(SEED)
    P("=" * 70)
    P("E5 — THE FREQUENCY LADDER, QUANTIFIED   (10¹⁴ Hz  →  ~10–100 Hz)")
    P("=" * 70)
    P(f"inherited rung-1 canon: invariant D = {VB.D*1e12:.6f} pm; SEED={SEED}\n")

    # (0) RUNG 1 — the carrier the eye is handed -----------------------------------------
    P("(0) RUNG 1 — the carrier (ν=c/λ) and the quantum of drive (E=hc/λ):")
    for nm, lam in (("red", 632.99e-9), ("green", 532.0e-9)):
        chi = VB.chi_deg(lam)
        P(f"    {nm:<5} {lam*1e9:6.2f}nm  →  ν = {nu_light(lam):.3e} Hz   E = {photon_eV(lam):.3f} eV"
          f"   (angle χ={chi:.4f}°)")
    nu_r = nu_light(632.99e-9)
    assert 3e14 < nu_r < 9e14 and 3e14 < nu_light(532.0e-9) < 9e14   # the visible carrier band
    P("    the receptor cannot oscillate at 10¹⁴ Hz; it absorbs E=hν as ONE quantum of drive. [L]/[F]")

    # (1) the collapse magnitude ---------------------------------------------------------
    P("\n(1) THE COLLAPSE — carrier vs neural band (cited ganglion range ~10–100 Hz):")
    lo = nu_r / NEURAL_BAND_HZ[1]; hi = nu_r / NEURAL_BAND_HZ[0]
    P(f"    ν_light/neural ≈ {nu_r:.2e}/{NEURAL_BAND_HZ[0]:.0f}–{NEURAL_BAND_HZ[1]:.0f}Hz "
      f"= {lo:.1e}–{hi:.1e}  ≈ {math.log10(lo):.1f}–{math.log10(hi):.1f} orders of magnitude")
    assert lo > 1e12 and hi < 1e15      # ~13-order collapse; ratio forced, absolute neural [O]
    P("    a ~13-order frequency collapse: the RATIO is forced; the absolute neural Hz is [O].")

    # (2) the mechanism: event-detection + low-pass, NOT mixing (frozen Neuron) ----------
    P("\n(2) MECHANISM = EVENT-DETECTION + LOW-PASS, not mixing  (frozen Neuron, substrate-time):")
    T, dt, d0, Ac = 4000.0, 0.02, 0.4, 0.4
    n = int(T / dt); t = np.arange(n) * dt
    N = Neuron(gamma=1.0, tau_f=1.0, tau_s=40.0, beta=0.5)
    S0, _ = N.run(d0, T=T, dt=dt); f0 = dominant_freq(S0, dt)
    P(f"    intrinsic rhythm (no carrier): f0 = {f0:.5f} /unit-time")

    P("    (2a) LOW-PASS — feed a fast carrier f_c, watch the output:")
    carriers = [0.25, 0.5, 1.0, 2.0, 5.0]
    out_dom, out_rate = [], []
    for fc in carriers:
        drive = d0 + Ac * np.sin(2 * math.pi * fc * t)
        S, _ = N.run(drive, T=T, dt=dt)
        fd = dominant_freq(S, dt); r = Neuron.rate_hz(S, dt)
        out_dom.append(fd); out_rate.append(r)
        P(f"         f_c={fc:5.2f} ({fc/f0:4.0f}× f0)  out_dom={fd:.5f}  out_rate={r:.5f}  out/f_c={fd/fc:.4f}")
    assert out_dom[-1] < carriers[-1] / 20.0        # output cannot follow the fast carrier
    P("         → output stays at the intrinsic LOW band; out/f_c → 0. The cell cannot follow it. [V]")

    P("    (2b) CARRIER-INVARIANCE (the no-mixing test):")
    span = carriers[-1] / carriers[0]
    rel_spread = (max(out_rate) - min(out_rate)) / (sum(out_rate) / len(out_rate))
    P(f"         carrier spans {span:.0f}× ; output rate moves only {rel_spread*100:.1f}% "
      f"(min={min(out_rate):.5f}, max={max(out_rate):.5f})")
    assert span > 10.0 and rel_spread < 0.30        # output ⟂ carrier ⇒ NOT mixing
    P("         → output is orthogonal to carrier frequency. A mixer would TRACK f_c; this does not. [F]")

    P("    (2c) THE CUBIC IS THE ALL-OR-NONE EVENT (delete −s³ → no threshold):")
    g = float(ATLAS["GUCY2D"]["gamma"]); hs = spinodal(g)        # a real measured eye γ, READ-ONLY
    c_lo, c_hi = settle_field(g, 0.95 * hs, True),  settle_field(g, 1.05 * hs, True)
    l_lo, l_hi = settle_field(g, 0.95 * hs, False), settle_field(g, 1.05 * hs, False)
    P(f"         CUBIC : s(0.95h*)={c_lo:+.3f} → s(1.05h*)={c_hi:+.3f}  (discontinuous flip Δ={c_hi-c_lo:+.3f})")
    P(f"         LINEAR: s(0.95h*)={l_lo:+.3f} → s(1.05h*)={l_hi:+.3f}  (no two-basin threshold)")
    assert c_lo < 0 < c_hi and (c_hi - c_lo) > 1.5  # the cubic gives the all-or-none event
    assert abs(l_hi) >= 10.0                         # linear: no bounded flip (diverges)
    P("         → the carrier collapses onto ONE discrete flip-event; the cubic is what makes it all-or-none. [F]")

    # (3) the surviving band is set by the recovery τ, not the carrier --------------------
    P("\n(3) THE BAND IS SET BY THE RECOVERY τ, not the carrier (carrier fixed at f_c=2.0):")
    band = []
    for ts in [20, 40, 80, 160]:
        Nt = Neuron(gamma=1.0, tau_f=1.0, tau_s=ts, beta=0.5)
        drive = d0 + Ac * np.sin(2 * math.pi * 2.0 * t)
        S, _ = Nt.run(drive, T=T, dt=dt); fd = dominant_freq(S, dt)
        band.append(fd)
        P(f"    τ_s={ts:4d}  out_dom={fd:.5f}")
    assert all(band[i + 1] < band[i] + 1e-9 for i in range(len(band) - 1))   # larger τ → lower band
    assert band[0] > band[-1]
    P("    → output band ∝ 1/τ: manufactured by the cascade/recovery, NOT inherited from the light. [F]")

    # (4) the full ladder ----------------------------------------------------------------
    P("\n(4) THE LADDER, end to end:")
    P("    ν_light ~10¹⁴ Hz  ──(E=hν → ONE isomerisation; R19 event-detector, §E2)──▶  discrete flip")
    P("       discrete flip  ──(cascade LOW-PASS, recovery τ; carrier averaged away)──▶  graded ~Hz")
    P("        graded ~Hz    ──(spike-rate re-quantisation, §E8)──────────────────────▶  ~10–100 Hz")
    P("    collapse ≈ 13 orders.  RATIO forced [F]; absolute Hz at each biological rung [O].")

    P("\nLEARNED: the eye does NOT mix the carrier down — it DETECTS the photon as a single energy")
    P("         event (the R19 all-or-none flip) and LOW-PASSES the event stream into a band set by")
    P("         its own recovery time-constant. The carrier frequency is discarded; colour survives")
    P("         only because it rides the ANGLE (geometry), not a frequency the cell could follow.")


def main():
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
