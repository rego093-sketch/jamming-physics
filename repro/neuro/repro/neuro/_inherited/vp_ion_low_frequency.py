#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_ion_low_frequency.py — how IONS make the LOW frequency.

After light/colour (which live at the quantum carrier, ~10^19 Hz), the neural signal
is the opposite extreme: a LOW-frequency rhythm. This module reproduces WHY — it is
ionic, not electromagnetic.

A neuron is the R19 bistable switch plus a slow recovery variable — a FitzHugh–Nagumo
relaxation oscillator:

    dv/dt = v − v³/3 − w + I          fast : v = membrane potential; Na⁺ in (activator)
    dw/dt = ε (v + a − b w)           slow : w = recovery;          K⁺ out (recovery)

The fast Na⁺ upstroke is brief; the slow K⁺ recovery (ε ≪ 1) dominates the cycle, so
the PERIOD is long and the frequency is LOW. The frequency is set by ε — the slowness
of the ionic recovery — not by any carrier. Make ε smaller (slower K⁺) and the rhythm
drops further. That is the whole reason neural signalling is low-frequency: the ions
recover slowly. (It is NOT 'energy→information' — that conflation is retired, §9.)

stdlib + numpy. Deterministic.
"""
import math, hashlib, io
import numpy as np

def fhn(eps, I=0.5, a=0.7, b=0.8, T=4000.0, dt=0.02):
    """Integrate the ionic relaxation oscillator; return (t, v) and the period."""
    n = int(T/dt); v, w = -1.0, 1.0
    vs = np.empty(n); 
    for k in range(n):
        dv = v - v**3/3.0 - w + I
        dw = eps*(v + a - b*w)
        v += dt*dv; w += dt*dw
        vs[k] = v
    # period from upstroke crossings (v rising through 0) after a settling transient
    t = np.arange(n)*dt
    s = n//4
    cross = [(k) for k in range(s+1, n) if vs[k-1] < 0 <= vs[k]]
    if len(cross) >= 2:
        per = float(np.mean(np.diff(cross))*dt)
    else:
        per = float('nan')
    # fast upstroke duration vs slow recovery duration within one cycle
    return t, vs, per

def run(P):
    P("="*70)
    P("IONS MAKE THE LOW FREQUENCY — the slow K⁺ recovery sets the rhythm")
    P("="*70)
    P("neuron = R19 switch + slow recovery = FitzHugh–Nagumo relaxation oscillator")
    P("  fast: dv/dt = v − v³/3 − w + I   (Na⁺ in, activator)")
    P("  slow: dw/dt = ε(v + a − b w)     (K⁺ out, recovery; ε≪1)\n")

    # the frequency is LOW and is set by ε (the slowness of ionic recovery)
    P(f"{'ε (K⁺ recovery rate)':>22}{'period':>12}{'frequency':>14}")
    rows = []
    for eps in [0.08, 0.04, 0.02, 0.01]:
        _, _, per = fhn(eps)
        f = 1.0/per if per==per else float('nan')
        rows.append((eps, per, f))
        P(f"{eps:>22.3f}{per:>12.2f}{f:>13.5f} ")
    # slower recovery (smaller ε) → longer period → LOWER frequency  [V]
    fs = [f for _,_,f in rows]
    assert all(fs[i] > fs[i+1] for i in range(len(fs)-1))   # ε↓ ⇒ frequency↓
    P("\n  → smaller ε (slower K⁺ recovery) ⇒ longer period ⇒ LOWER frequency  [V]")

    # timescale separation: the slow phase dominates the cycle (why it is low-freq)
    eps = 0.02
    t, vs, per = fhn(eps)
    s = len(vs)//4
    # within the last full cycle, fraction of time spent in the slow (recovery) phase
    seg = vs[s:]
    above = np.mean(seg > 0.0)     # depolarised fraction
    P(f"\n  timescale separation at ε={eps}: one cycle is mostly the slow recovery")
    P(f"    (fast Na⁺ upstroke is brief; recovery fills the period) — period={per:.1f} ")
    P(f"    depolarised-time fraction ≈ {above:.2f}  (the rest is slow recovery)")

    # contrast: the neural rhythm vs the quantum carrier
    f_neural = rows[2][2]            # ε=0.02 frequency (dimensionless model units)
    P(f"\n  CONTRAST: colour/light lives at the quantum carrier f_q=c/D≈6.2×10¹⁹ Hz;")
    P(f"    the neural rhythm is ~1–40 Hz — ~10¹⁸× lower — because the IONS recover")
    P(f"    slowly. Low frequency is a slow-ion consequence, not a carrier and not")
    P(f"    'energy→information' (retired, §9).")

    P("\nLEARNED: the low frequency is made by ions — the slow K⁺ recovery of the")
    P("         relaxation oscillator. ε sets the rhythm; slower ions ⇒ lower Hz.")

def main():
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()

if __name__ == "__main__":
    print("\nsha256:", main())
