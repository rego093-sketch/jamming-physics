#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E8 — GRADED → SPIKE-RATE RE-QUANTISATION  (the hand-off to the neural code; the ladder ends here)

E5/E6/E7 leave the eye's output as a **graded** low-pass signal whose band is set by the recovery τ
(E7: f_c = β/(2π·τ)). E8 is the FINAL rung: the retina re-encodes that continuous ~Hz signal as a
discrete ganglion-cell spike **RATE** — a re-quantisation at the low band (rate coding). The carrier
that was discarded back at the single-photon flip (E2) must NOT reappear here; if the hand-off were a
mixer it would put the carrier back. The one claim of E8: **the graded amplitude is re-quantised into a
firing RATE — a thresholded, bounded, monotone code that carries the slow envelope and never the
carrier.** Where seeing *feels like something* is OUT OF SCOPE — it hands off to the mind volume.

THE RE-QUANTISER IS THE FROZEN R19 NEURON (no new math).  The same FROZEN Neuron (vp_substrate.Neuron)
whose slow recovery SET the band in E7 now FIRES: a spike is an up-crossing of the membrane through
threshold — an all-or-none R19 fold-crossing event (E2's cubic −s³ is what makes it all-or-none). The
spike reader is inherited verbatim (`Neuron.spikes` / `Neuron.rate_hz` / `dominant_freq`). The graded
photoreceptor signal enters as the slowly-varying drive; the output is the spike RATE.

THE HONEST SHAPE OF THE CODE (measured off the FROZEN substrate, not assumed).  The FROZEN Neuron is an
autonomous relaxation oscillator: it is SILENT in a deep-hyperpolarised basin, FIRES across an operating
band, and is SILENCED AGAIN by depolarisation block past the band. So the rate code is a **bandpass in
drive** — a rheobase FLOOR (the switch must be driven across its fold to fire) and a depolarisation-block
CEILING (drive it too hard and the switch sticks ON, the oscillation stops). Inside that band the code is
clean and monotone; that is the honest operating envelope, and the absolute band edges/rates are [O].

WHAT IS SHOWN (and how it is graded)
  (0) THE RE-QUANTISER.  the FROZEN Neuron's membrane up-crossings ARE the spike train; the inherited
      readers turn the continuous s(t) into a discrete count → a rate. graded signal in, rate out.   [F]
  (1) THE RHEOBASE FLOOR.  from a silent hyperpolarised rest (drive = B), a graded depolarising increment
      g is SILENT below a threshold and FIRES above it — the all-or-none switch must clear its fold to
      spike (the E2/E4 condition, read forward). The code has a floor.                                [V]
  (2) THE MONOTONE CODE.  above the rheobase the firing RATE rises strictly monotonically with the graded
      amplitude g across the operating band — the graded amplitude is re-encoded as a rate.         [F]/[V]
  (3) A GENUINE QUANTISER (discrete clock).  the output is a near-periodic point process: the inter-spike
      intervals are well-defined and highly regular (CV ≪ 1). the continuous graded input is re-quantised
      into a spike train whose RATE carries the signal — not a graded continuation.                  [F]/[V]
  (4) THE HONEST CEILING (bandpass in drive).  the full-range f–I is NON-monotone: SILENT on BOTH sides
      of the band (hyperpolarisation floor AND depolarisation-block ceiling), firing only in between. the
      monotone code lives in a FINITE operating band, bounded by the switch failing to flip (floor) and
      sticking ON (ceiling). the bandpass STRUCTURE is forced; the absolute edges are a named [O].   [V]+[O]
  (5) THE CARRIER STAYS GONE (no mixing — the loop with E5/E7 closes).  hold the slow envelope fixed and
      sweep the carrier frequency → the rate is INVARIANT (rate ⟂ carrier); hold the carrier fixed and
      raise the envelope → the rate MOVES (rate ∝ envelope). the re-quantiser tracks the ENVELOPE and does
      NOT re-introduce the carrier — the hand-off preserves the ~13-order down-conversion.          [F]/[V]
  (6) THE RATE LIVES IN THE LOW BAND.  the spike train's dominant frequency EQUALS the firing rate and
      sits in the neural low band — orders below the carrier. the re-quantisation does not undo the
      collapse; what crosses to the brain is the low-band rate (the felt percept → mind volume).      [F]

WHERE γ SITS (read-only, honest).  γ is NOT the band-setter (that is τ, E7) and NOT the signal (that is
the graded drive). Raising a gene's γ raises its spinodal — the switch is harder to flip — so γ shifts the
f–I curve's POSITION (the rheobase moves) without changing the code's shape: γ is a STRUCTURAL excitability
OFFSET. Here γ moves the rate about as much as the drive does, so E8 makes **no** "γ is negligible" claim —
γ is read byte-equal from the frozen atlas (READ-ONLY) purely to show the offset, never fitted.

HONEST CAVEATS (named [O])
  • ABSOLUTE Hz / SPIKE-COUNT.  the rate is in spikes/unit-time; the ABSOLUTE spikes·s⁻¹ (and any real
    refractory period, ganglion f–I gain, or saturation count) is not fixed by the promoter-γ — the same
    ladder [O] at every rung. Only the CODE STRUCTURE (floor, monotone band, ceiling, carrier-invariance)
    is forced.
  • THE f–I SHAPE.  only the thresholded, bounded, monotone STRUCTURE is forced; whether the real curve is
    linear / sqrt / log and where it saturates is substrate/biology — a named [O].
  • ONE STAGE vs THE RETINAL NETWORK.  the substrate collapses photoreceptor→bipolar→amacrine→ganglion
    lateral processing (centre–surround, temporal filtering) into a SINGLE re-quantiser; the receptive-field
    structure is out of scope — a named [O].
  • THE FELT PERCEPT.  where seeing feels like something is OUT OF SCOPE — it hands off to the mind volume
    (firewall). E8 ends at the neural RATE, not the experience.

FIREWALL / NO-TUNING.  E8 is pure sensory MECHANISM — no disease, diagnostic, or clinical claim (the
disease layer is E4, firewalled; nothing here diagnoses, treats, or prescribes). Nothing is fitted: β,
τ_f, τ_s are the FROZEN Neuron's own constants, the spike reader is inherited verbatim, every γ used is
read byte-equal from the frozen atlas (READ-ONLY), the operating point is an input (not a fitted target).
Deterministic; run twice → identical sha256.

stdlib + numpy. Imports the FROZEN substrate; adds no γ.
"""
import os, sys, io, hashlib, math
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(PKG, "inherited"))

from vp_substrate import seed_everything, Neuron, dominant_freq, spinodal, dwell, SEED   # FROZEN substrate
import json
ATLAS = json.load(open(os.path.join(PKG, "inherited", "organ_gamma.json"), encoding="utf-8"))["genes"]

# the FROZEN Neuron's own constants (asserted byte-equal in (0)); operating window is an INPUT, not fitted.
BETA, TAU_F, TAU_S = 0.5, 1.0, 40.0
T, DT = 6000.0, 0.05          # long window → clean spike statistics; dt as in E7's neuron runs
B_REST = -1.0                 # a deep-hyperpolarised SILENT rest (the photoreceptor at its dark baseline)


def _rate(drive_scalar_or_array, gamma=1.0):
    """Run the FROZEN Neuron and read the inherited spike RATE (up-crossings of 0)."""
    S, _ = Neuron(gamma=gamma, tau_f=TAU_F, tau_s=TAU_S, beta=BETA).run(drive_scalar_or_array, T=T, dt=DT)
    return Neuron.rate_hz(S, DT), S


def _isi_cv(S):
    """Inter-spike-interval mean and coefficient of variation (regularity of the rate clock)."""
    sp = Neuron.spikes(S)
    if len(sp) < 3:
        return float("nan"), float("nan"), len(sp)
    isi = np.diff(sp) * DT
    return float(isi.mean()), float(isi.std() / isi.mean()), len(sp)


def run(P):
    seed_everything(SEED)
    P("=" * 74)
    P("E8 — GRADED → SPIKE-RATE RE-QUANTISATION   (the hand-off; the ladder's last rung)")
    P("=" * 74)

    # (0) the re-quantiser is the FROZEN Neuron's own up-crossings -------------------------------
    Nref = Neuron()
    assert (Nref.beta, Nref.tau_f, Nref.tau_s) == (BETA, TAU_F, TAU_S)   # no drift in the substrate
    P("(0) THE RE-QUANTISER IS THE FROZEN R19 NEURON (spike = membrane up-crossing = fold-crossing event):")
    P(f"    inherited readers: Neuron.spikes / Neuron.rate_hz / dominant_freq ;  β={BETA}, τ_f={TAU_F}, τ_s={TAU_S}; SEED={SEED}")
    P( "    graded photoreceptor signal → the slowly-varying DRIVE ;  output → the spike RATE (a discrete count). [F]")

    # (1) the rheobase floor: silent below threshold, fires above (the switch must clear its fold) -
    P("\n(1) THE RHEOBASE FLOOR — from a SILENT hyperpolarised rest (drive=B=%.1f), a graded increment g:" % B_REST)
    g_floor, r_floor = None, None
    for g in (0.00, 0.10, 0.20, 0.25, 0.30):
        r, _ = _rate(B_REST + g)
        if r > 0 and g_floor is None:
            g_floor = g
        tag = "SILENT" if r == 0.0 else "firing"
        P(f"    g={g:4.2f}  drive={B_REST+g:+5.2f}   rate={r:.6f}   ({tag})")
    r_silent, _ = _rate(B_REST + 0.20)
    r_fires,  _ = _rate(B_REST + 0.30)
    assert r_silent == 0.0 and r_fires > 0.0
    P(f"    → SILENT at g≤0.20, FIRES at g≥0.30: the all-or-none switch must be driven across its fold to")
    P(f"      spike (the E2/E4 condition read forward). The rate code has a FLOOR (rheobase). [V]")

    # (2) the monotone code: above rheobase, rate rises strictly with the graded amplitude ---------
    P("\n(2) THE MONOTONE CODE — above the floor, the RATE rises strictly with the graded amplitude g:")
    band_g = (0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90)
    band_r = []
    for g in band_g:
        r, _ = _rate(B_REST + g); band_r.append(r)
        P(f"    g={g:4.2f}  drive={B_REST+g:+5.2f}   rate={r:.6f}")
    mono = all(band_r[i + 1] > band_r[i] for i in range(len(band_r) - 1))
    assert mono
    P(f"    → strictly monotone increasing across the operating band ({band_g[0]}→{band_g[-1]}): the graded")
    P(f"      amplitude is RE-ENCODED as a firing rate ({band_r[0]:.5f}→{band_r[-1]:.5f}). [F]/[V]")

    # (3) a genuine quantiser: the spike train is a regular clock (CV ≪ 1) -------------------------
    P("\n(3) A GENUINE QUANTISER — the output is a near-periodic point process (regular inter-spike clock):")
    cvs = []
    for g in (0.40, 0.60, 0.80):
        _, S = _rate(B_REST + g)
        mi, cv, nsp = _isi_cv(S); cvs.append(cv)
        P(f"    g={g:4.2f}   nspikes={nsp:3d}   mean ISI={mi:7.2f}   CV(ISI)={cv:.5f}")
    assert max(cvs) < 0.05
    P( "    → CV(ISI) ≪ 1 (a clean clock): the continuous graded input is re-quantised into a discrete")
    P( "      spike train whose RATE carries the signal — not a graded continuation. [F]/[V]")

    # (4) the honest ceiling: bandpass in drive — block on BOTH sides ------------------------------
    P("\n(4) THE HONEST CEILING — the FULL-range f–I is NON-monotone (block on BOTH sides of the band):")
    r_lo, _ = _rate(-1.00)        # deep hyperpolarisation → silent (floor)
    r_op, _ = _rate(-0.30)        # operating band         → firing
    r_pk, _ = _rate( 0.00)        # near the peak
    r_hi, _ = _rate(+1.00)        # depolarisation block    → silenced again (ceiling)
    for d, r, lab in ((-1.00, r_lo, "hyperpol. floor → SILENT"),
                      (-0.30, r_op, "operating band  → firing"),
                      ( 0.00, r_pk, "near peak       → firing"),
                      (+1.00, r_hi, "depol. block    → SILENT")):
        P(f"    drive={d:+5.2f}   rate={r:.6f}   ({lab})")
    assert r_lo == 0.0 and r_op > 0.0 and r_hi < 0.05 * r_op
    P( "    → the rate code is a BANDPASS in drive: a rheobase FLOOR and a depolarisation-block CEILING")
    P( "      (the switch fails to flip below, sticks ON above). Monotone only INSIDE a finite band.")
    P( "      The bandpass STRUCTURE is forced; the absolute band edges/rates are a named [O]. [V]+[O]")

    # (5) the carrier stays gone: rate ⟂ carrier, rate ∝ envelope (no mixing) ----------------------
    P("\n(5) THE CARRIER STAYS GONE (no mixing) — re-quantiser tracks the ENVELOPE, not the carrier:")
    n = int(T / DT); t = np.arange(n) * DT
    P("    (5a) FIX the slow envelope (drive=−0.3), sweep the carrier frequency f_c only:")
    car_rates = []
    for fc in (0.0, 0.5, 1.0, 2.0, 5.0, 10.0):
        car = np.zeros(n) if fc == 0.0 else 0.25 * np.sin(2.0 * math.pi * fc * t)
        r, _ = _rate(-0.3 + car); car_rates.append(r)
        P(f"         carrier f_c={fc:5.1f}   rate={r:.6f}")
    spread = (max(car_rates) - min(car_rates)) / (sum(car_rates) / len(car_rates))
    assert spread < 0.05
    P(f"         → rate spread across a 20× carrier span = {spread*100:.2f}%  ⇒ rate ⟂ carrier (a mixer would track it). [F]")
    P("    (5b) FIX the carrier (f_c=2), raise the depolarising envelope across the rising band:")
    env_rates = []
    for env in (-0.70, -0.60, -0.50, -0.40, -0.30, -0.20):
        car = 0.15 * np.sin(2.0 * math.pi * 2.0 * t)
        r, _ = _rate(env + car); env_rates.append(r)
        P(f"         envelope drive={env:+5.2f}   rate={r:.6f}")
    env_mono = all(env_rates[i + 1] > env_rates[i] for i in range(len(env_rates) - 1))
    assert env_mono
    P(f"         → rate rises with the envelope ({env_rates[0]:.5f}→{env_rates[-1]:.5f}) ⇒ rate ∝ envelope. [F]/[V]")
    P("    ⇒ the hand-off carries the slow ENVELOPE and NEVER re-introduces the carrier: the E5/E7")
    P("      ~13-order down-conversion is PRESERVED across the re-quantisation. [F]")

    # (6) the rate lives in the low band ----------------------------------------------------------
    P("\n(6) THE RATE LIVES IN THE LOW BAND — the spike train's dominant frequency IS the rate, ≪ carrier:")
    r_op2, S_op = _rate(-0.3)
    fdom = dominant_freq(S_op, DT)
    P(f"    operating point drive=−0.3:  rate_hz={r_op2:.6f}   dominant_freq(train)={fdom:.6f}")
    assert abs(fdom - r_op2) / r_op2 < 0.10
    for fc in (2.0, 10.0):
        P(f"      vs carrier f_c={fc:4.1f}:  rate/carrier = {r_op2/fc:.6f}  (orders below)")
    P( "    → the train's frequency content sits at the RATE, in the neural low band — the re-quantisation")
    P( "      does not undo the collapse. What crosses to the brain is the low-band rate. [F]")
    P( "      (Absolute Hz is the ladder's standing [O]; only the band PLACEMENT is forced.)")

    # where γ sits (read-only, honest: a structural offset, not the band and not the signal) -------
    P("\n(7) WHERE γ SITS (READ-ONLY) — γ shifts the f–I POSITION (rheobase), not the band, not the signal:")
    P("    raising a gene's γ raises its spinodal (the switch is harder to flip) ⇒ at fixed drive the rate")
    P("    drops; γ is a STRUCTURAL excitability OFFSET. (γ moves the rate ~as much as the drive here, so")
    P("    E8 makes NO 'γ negligible' claim — γ is read byte-equal from the atlas only to show the offset):")
    for sym in ("CNGB3", "RPE65", "GUCY2D", "RHO"):
        g = float(ATLAS[sym]["gamma"])
        r, _ = _rate(-0.3, gamma=g)
        P(f"      {sym:7s} γ={g:.4f}  spinodal={spinodal(g):.4f}  dwell∝γ^1.5={dwell(g,0.5):.4f}  rate(drive=−0.3)={r:.6f}")
    P("    (band channel = τ [E7]; signal channel = graded drive [E8]; γ = structural offset. [F]/[V])")

    # ladder placement — E8 closes the spine ------------------------------------------------------
    P("\nLADDER PLACEMENT (E8 closes the down-conversion spine E0→E8):")
    P("    ν_light ~10¹⁴ Hz ──(E=hν → ONE flip; R19 event-detector, §E2)──▶ discrete flip-events")
    P("    discrete flips    ──(cascade low-pass, cutoff f_c=β/(2π·τ), §E7)──▶ graded ~Hz band")
    P("    graded band       ──(THIS rate re-quantisation; floor+monotone+ceiling, carrier gone)──▶ ~spike RATE")
    P("    spike RATE        ──(what seeing FEELS like)─────────────────────────────────▶ mind volume (firewall)")
    P("    the rate carries the slow envelope, never the carrier; the ~13-order collapse is preserved end-to-end.")

    P("\nLEARNED: the eye's last step is a RE-QUANTISER, not a mixer. The graded transduction signal is")
    P("         turned into an all-or-none spike train whose RATE encodes the graded amplitude — a")
    P("         THRESHOLDED (rheobase), BOUNDED (depolarisation-block ceiling), MONOTONE code that tracks")
    P("         the slow envelope and leaves the carrier discarded (E2) and filtered (E7). The down-")
    P("         conversion survives end-to-end because colour/place are geometry and the rate is the")
    P("         envelope, never the carrier. The absolute Hz, the f–I shape, the single-stage collapse,")
    P("         and the felt percept (→ mind volume) are the named [O].")


def main():
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
