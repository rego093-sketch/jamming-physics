#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E7 — THE CASCADE AS THE BAND-SETTING LOW-PASS  (τ is the explicit filter; the band is ~1/τ)

E5 showed, qualitatively, that the surviving band is set by the recovery time-constant τ (out_dom ∝
1/τ) and that the carrier is averaged away (out/f_c → 0). E7 makes that the NAMED FILTER: it reads an
explicit transfer function off the FROZEN substrate, locates the cutoff, and shows the cutoff is the
closed-form f_c = β/(2πτ) — so the output band is MANUFACTURED by the recovery τ, not inherited from
the carrier.

THE FILTER IS ALREADY IN THE SUBSTRATE (no new math).  The FROZEN Neuron (vp_substrate.Neuron) updates
its recovery variable by the verbatim law

        w ← w + dt·(s − β·w)/τ_s            # vp_substrate.Neuron.run, copied byte-for-byte below

which is a first-order **leaky integrator** — i.e. a single-pole low-pass on the membrane signal s. In
the Fourier domain (s as input, w as output):

        τ_s·dw/dt + β·w = s     ⇒     H(f) = 1/(β + i·2π f·τ_s)
        |H(f)| = 1 / √(β² + (2π f·τ_s)²)

with three FORCED consequences (closed form, no fit):
        DC gain |H(0)| = 1/β        the flat passband,
        cutoff  f_c   = β/(2π·τ_s)  the −3 dB point  ⇒  f_c·τ_s = β/(2π)  (so f_c ∝ 1/τ EXACTLY),
        phase(f_c) = −45°, roll-off −20 dB/decade   the single-pole signature.

WHAT IS SHOWN (and how it is graded)
  (0) THE CLOSED-FORM FILTER.  state H(f) from the substrate's own recovery law; print the forced
      DC gain, cutoff f_c=β/(2πτ), 45° cutoff phase, −20 dB/dec roll-off.                       [F]
  (1) MEASURE IT on the FROZEN recovery law (a lock-in: drive s=sin(2πf t), read the amplitude and
      phase of w at f). The measurement reproduces the closed form:
        (1a) the passband is flat at the DC gain 1/β,
        (1b) the measured −3 dB cutoff = β/(2πτ_s) to <1%,
        (1c) the phase lag at the cutoff = 45° (the single-pole fingerprint),
        (1d) the high-frequency roll-off = −20 dB/decade (one pole).                            [V]
  (2) THE BAND IS β/(2πτ): manufactured by the recovery, not the carrier.  Sweep τ_s; the cutoff
      tracks 1/τ EXACTLY — the product f_c·τ_s is constant (= β/2π).  The cutoff carries NO γ and NO
      carrier frequency: the recovery law has neither.  ⇒ band ⟂ carrier (E5) AND band ⟂ γ.       [F]/[V]
  (3) THE LOW-PASS *IS* E5's "AVERAGED AWAY".  E5's fast carriers sit at f ≫ f_c, where the closed-form
      |H| ∝ 1/f drives the response toward zero — the carrier-rejection of §E5 is exactly this
      roll-off.  (The real 10¹⁴ Hz carrier is ~17 orders above any plausible f_c ⇒ total rejection.)  [F]
  (4) THE EMERGENT RHYTHM FOLLOWS THE SAME τ.  On the FULL FROZEN Neuron the intrinsic rhythm falls
      monotonically as τ_s rises and is ASYMPTOTICALLY ∝ 1/τ — honestly only *approximately*, because a
      relaxation oscillator's period = (slow recovery ∝ τ) + (a τ-independent fast transit), so out_dom·τ
      drifts toward an asymptote. The CLEAN 1/τ law lives in the explicit filter; the neuron inherits it.
      γ (the switch nonlinearity, dwell ∝ γ^1.5) is a SECONDARY mover of the full-neuron rhythm; τ dominates. [V]

HONEST CAVEATS (named [O])
  • ONE POLE vs A CASCADE.  the substrate models the NET transduction as a SINGLE pole (−20 dB/dec).
    The real photoreceptor cascade is multi-stage (rhodopsin→transducin→PDE→cGMP→CNG) — higher-order,
    so the real roll-off is steeper. The single-pole STRUCTURE and band∝1/τ are forced; the pole COUNT
    is a named [O].
  • ABSOLUTE Hz.  the cutoff is in 1/unit-time; the ABSOLUTE τ in seconds (hence the absolute cutoff in
    Hz) is not fixed by the promoter-γ — the same [O] that runs through every rung of the ladder. Only
    the SCALING (band ∝ 1/τ) and the filter's shape are forced.

FIREWALL / NO-TUNING.  E7 is pure sensory MECHANISM — no disease, diagnostic, or clinical claim (the
disease layer is E4, firewalled). Nothing is fitted: β, τ_f, τ_s are the FROZEN Neuron's own constants,
the recovery law is copied verbatim, every γ used is read byte-equal from the frozen atlas (READ-ONLY),
and the cutoff is the substrate's closed form. Deterministic; run twice → identical sha256.

stdlib + numpy. Imports the FROZEN substrate; adds no γ.
"""
import os, sys, io, hashlib, math
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(PKG, "inherited"))

from vp_substrate import seed_everything, Neuron, dominant_freq, dwell, SEED   # FROZEN substrate
import json
ATLAS = json.load(open(os.path.join(PKG, "inherited", "organ_gamma.json"), encoding="utf-8"))["genes"]

# the FROZEN Neuron's own recovery constants (asserted byte-equal to the substrate in (0))
BETA, TAU_F = 0.5, 1.0


# ---- the substrate's recovery law, copied VERBATIM from vp_substrate.Neuron.run -----------------
#      w += dt * (s - self.beta * w) / self.tau_s
# driven by a unit sinusoid s(t)=sin(2πf t); a lock-in reads the steady-state amplitude+phase of w.
def _transfer(tau_s, beta=BETA, dt=0.1, t_start=2500.0, L=16000.0):
    """Measure |H(f)| and phase(f) of the recovery low-pass. Frequencies are commensurate with the
    analysis window (f_j = j/L) so every lock-in integrates an exact integer number of periods."""
    n_start, n_L = int(t_start / dt), int(L / dt)
    N = n_start + n_L
    log_j = [int(round(x)) for x in np.logspace(0.0, math.log10(1600.0), 30)]
    dense = []
    for jc in (16, 32, 64):                       # extra resolution near the cutoffs of τ_s=80,40,20 (L=16000)
        dense += [jc - 6, jc - 4, jc - 2, jc - 1, jc, jc + 1, jc + 2, jc + 4, jc + 8]
    js = sorted(set(j for j in (log_j + dense) if j >= 1))
    f = np.array([j / L for j in js], float)
    w2pf = 2.0 * math.pi * f
    w = np.zeros(len(f)); I = np.zeros(len(f)); Q = np.zeros(len(f))
    for k in range(N):
        tk = k * dt
        s_in = np.sin(w2pf * tk)
        w += dt * (s_in - beta * w) / tau_s        # <-- verbatim recovery law
        if k >= n_start:
            I += w * np.sin(w2pf * tk)
            Q += w * np.cos(w2pf * tk)
    I *= 2.0 / n_L; Q *= 2.0 / n_L
    gain = np.sqrt(I * I + Q * Q)
    lag_deg = -np.degrees(np.arctan2(Q, I))
    return f, gain, lag_deg


def _read_filter(tau_s, beta=BETA):
    """From the measured response: DC gain, the −3 dB cutoff (log-interp), the phase lag there, and the
    high-frequency roll-off slope in dB/decade. Returns the analytic cutoff too for comparison."""
    f, gain, lag = _transfer(tau_s, beta)
    fa = beta / (2.0 * math.pi * tau_s)            # closed-form cutoff
    dc_band = gain[f < 0.3 * fa]
    dc = float(dc_band.max()) if dc_band.size else float(gain[0])
    target = dc / math.sqrt(2.0)
    fc = None
    for i in range(len(f) - 1):
        if gain[i] >= target >= gain[i + 1]:
            lf = (math.log(f[i]) + (math.log(target) - math.log(gain[i]))
                  * (math.log(f[i + 1]) - math.log(f[i]))
                  / (math.log(gain[i + 1]) - math.log(gain[i])))
            fc = math.exp(lf); break
    lag_fc = float(np.interp(fc, f, lag))
    hi = f > 12.0 * fa
    slope = 20.0 * math.log10(gain[hi][-1] / gain[hi][0]) / math.log10(f[hi][-1] / f[hi][0])
    return dc, fc, fa, lag_fc, slope


def run(P):
    seed_everything(SEED)
    P("=" * 74)
    P("E7 — THE CASCADE AS THE BAND-SETTING LOW-PASS   (cutoff f_c = β/(2π·τ))")
    P("=" * 74)

    # (0) the closed-form filter, straight from the FROZEN recovery law --------------------------
    Nref = Neuron()                                # the FROZEN Neuron, default constants
    assert (Nref.beta, Nref.tau_f, Nref.tau_s) == (BETA, TAU_F, 40.0)   # no drift in the filter params
    P("(0) THE FILTER IS THE SUBSTRATE'S RECOVERY (verbatim):  w ← w + dt·(s − β·w)/τ_s")
    P(f"    ⇒ a single-pole low-pass  H(f) = 1/(β + i·2πf·τ_s),  β={BETA} (frozen Neuron β); SEED={SEED}")
    P( "    forced (closed form):  DC gain = 1/β = %.4f ;  cutoff f_c = β/(2π·τ_s) ;  f_c·τ_s = β/2π = %.6f"
       % (1.0 / BETA, BETA / (2.0 * math.pi)))
    P( "                           phase(f_c) = −45° ;  roll-off = −20 dB/decade  (one pole)")

    # (1) measure the transfer function on the FROZEN recovery law (τ_s = 40, the Neuron default) --
    P("\n(1) MEASURED transfer function on the FROZEN recovery law (τ_s=40 = Neuron default):")
    dc, fc, fa, lag_fc, slope = _read_filter(40.0)
    P(f"    (1a) passband  DC gain = {dc:.5f}   (closed form 1/β = {1.0/BETA:.5f})            [V]")
    P(f"    (1b) cutoff    f_c(meas) = {fc:.6f}   vs  β/(2π·τ) = {fa:.6f}   ratio = {fc/fa:.4f}   [V]")
    P(f"    (1c) phase     lag at f_c = {lag_fc:.2f}°   (single-pole ⇒ 45°)                      [V]")
    P(f"    (1d) roll-off  high-f slope = {slope:.2f} dB/decade   (one pole ⇒ −20)               [V]")
    assert abs(dc - 1.0 / BETA) < 0.02
    assert abs(fc / fa - 1.0) < 0.01
    assert abs(lag_fc - 45.0) < 3.0
    assert abs(slope - (-20.0)) < 2.0
    P("    → the cascade IS a first-order low-pass; its band edge is the explicit number β/(2π·τ). [F]/[V]")

    # (2) the band is β/(2πτ): manufactured by the recovery, not the carrier, not γ ---------------
    P("\n(2) THE BAND ∝ 1/τ — sweep the recovery τ_s, the cutoff halves with it (carrier never enters):")
    prod = []
    prev = None
    for ts in (20.0, 40.0, 80.0):
        _, fcs, fas, _, _ = _read_filter(ts)
        prod.append(fcs * ts)
        flag = "" if prev is None else ("  (↓ with τ)" if fcs < prev else "  (NOT ↓)")
        P(f"    τ_s={ts:5.0f}   f_c = {fcs:.6f}   β/(2π·τ) = {fas:.6f}   f_c·τ_s = {fcs*ts:.6f}{flag}")
        prev = fcs
    mean_p = sum(prod) / len(prod)
    spread = (max(prod) - min(prod)) / mean_p
    P(f"    f_c·τ_s constant = {mean_p:.6f}  (β/2π = {BETA/(2*math.pi):.6f});  spread {spread*100:.2f}%  ⇒ f_c ∝ 1/τ EXACTLY")
    assert all(prod[i + 1] > prod[i] - 1e-3 for i in range(len(prod) - 1)) and spread < 0.03
    P("    the recovery law carries NO γ and NO carrier term ⇒ the band is PURELY τ: ⟂ carrier (E5) and ⟂ γ. [F]")

    # (3) the low-pass IS E5's 'averaged away' (carrier rejection = the roll-off) ------------------
    P("\n(3) THE LOW-PASS *IS* E5's CARRIER-REJECTION (closed-form |H| at E5's fast carriers, τ_s=40):")
    fc40 = BETA / (2.0 * math.pi * 40.0)
    for f_c_in in (1.0, 5.0):                       # E5's carriers, in substrate-time
        H = 1.0 / math.sqrt(BETA**2 + (2.0 * math.pi * f_c_in * 40.0) ** 2)
        P(f"    carrier f={f_c_in:4.1f}  (= {f_c_in/fc40:6.0f}× f_c)  →  |H|/DC = {H/(1.0/BETA):.5f}  (rejected ∝ 1/f)")
    assert (1.0 / math.sqrt(BETA**2 + (2*math.pi*5.0*40.0)**2)) / (1.0/BETA) < 0.01
    P("    E5 said the carrier is 'averaged away (out/f_c→0)'; here it IS the −20 dB/dec roll-off. [F]")
    P("    the REAL ~10¹⁴ Hz carrier sits ~17 orders above any plausible f_c ⇒ rejection is total")
    P("    (the RATIO is forced; the absolute f_c in Hz is the ladder's standing [O]).")

    # (4) the emergent full-neuron rhythm follows the same τ (only approximately ∝ 1/τ — honest) ---
    P("\n(4) THE FULL FROZEN NEURON inherits the band — emergent rhythm vs τ_s (constant drive d0=0.4):")
    T, dt, d0 = 4000.0, 0.05, 0.4
    rhythm = []
    for ts in (20.0, 40.0, 80.0, 160.0):
        S, _ = Neuron(gamma=1.0, tau_f=TAU_F, tau_s=ts, beta=BETA).run(d0, T=T, dt=dt)
        fd = dominant_freq(S, dt); rhythm.append(fd)
        P(f"    τ_s={ts:5.0f}   out_dom = {fd:.6f}   out_dom·τ_s = {fd*ts:.4f}")
    assert all(rhythm[i + 1] < rhythm[i] for i in range(len(rhythm) - 1))     # strictly ↓ in τ
    P("    out_dom ↓ monotonically with τ; out_dom·τ DRIFTS upward to an asymptote ⇒ only APPROX ∝ 1/τ:")
    P("    a relaxation period = (slow recovery ∝ τ) + (τ-independent fast transit). The CLEAN 1/τ is the")
    P("    explicit filter's; the neuron inherits it. [V]")

    P("\n    γ is the SECONDARY mover (the switch nonlinearity; dwell ∝ γ^1.5), not the band-setter — at")
    P("    fixed τ_s=40 the eye γ's shift the rhythm only mildly while τ sets the decade:")
    for sym in ("CNGB3", "RPE65", "GUCY2D", "RHO"):
        g = float(ATLAS[sym]["gamma"])
        S, _ = Neuron(gamma=g, tau_f=TAU_F, tau_s=40.0, beta=BETA).run(d0, T=T, dt=dt)
        P(f"      {sym:7s} γ={g:.4f}  dwell∝γ^1.5={dwell(g,0.5):.4f}  out_dom={dominant_freq(S,dt):.6f}")
    P("    (γ READ-ONLY from the frozen atlas; band channel = τ, size/settle channel = γ. [F]/[V])")

    # ladder placement ----------------------------------------------------------------------------
    P("\nLADDER PLACEMENT (E7 fixes the low-pass rung):")
    P("    ν_light ~10¹⁴ Hz ──(E=hν → ONE flip; R19 event-detector, §E2)──▶ discrete flip-events")
    P("    discrete flips    ──(THIS low-pass, cutoff f_c=β/(2π·τ); carrier ∝1/f rejected)──▶ graded band")
    P("    graded band       ──(spike-rate re-quantisation, §E8)─────────────────────────────▶ ~10–100 Hz")
    P("    the output band is the FILTER's (set by τ), never the light's. RATIO forced [F]; absolute Hz [O].")

    P("\nLEARNED: the band the eye speaks in is not chosen by the photon — it is the cutoff of the")
    P("         transduction low-pass, f_c = β/(2π·τ). Raise the recovery τ and the band drops with it;")
    P("         the carrier (and γ) leave the cutoff untouched. The carrier is detected as one event and")
    P("         then filtered out; what survives is the recovery's own band. ONE pole vs the real cascade")
    P("         (multi-stage) and the absolute τ→Hz are named [O].")


def main():
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
