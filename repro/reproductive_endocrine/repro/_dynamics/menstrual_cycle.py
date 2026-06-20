#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
menstrual_cycle.py  --  T2 (menstrual cycle) + T3 (hormone-feedback switch / LH surge).

T2 -- the menstrual cycle is the SLOWEST relaxation oscillator in this package: a long follicular
      charge (slow oestradiol rise as the dominant follicle grows) and a fast ovulatory discharge
      (the LH surge), then a luteal plateau and reset. A relaxation oscillator is asymmetric (slow
      rise, fast excursion); a sinusoid is symmetric. We verify the relaxation ASYMMETRY directly.
      Mechanism [V]; the ~28 d period is an [L] anchor set by the recovery timescale, not derived.

T3 -- oestrogen feedback is a bistable SWITCH. Below a threshold/duration of oestradiol the axis sits
      in NEGATIVE feedback (low LH). Sustained high oestradiol crosses the spinodal and the axis FLIPS
      to POSITIVE feedback -- the mid-cycle LH surge -- DISCONTINUOUSLY. The switch shows HYSTERESIS:
      the up-threshold (trigger the surge) and the down-threshold (return) differ. This is the SAME
      R19 primitive that the oncology module uses for malignant transformation. Mechanism [V].

Uses only inherited/vp_substrate.py. Deterministic.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Neuron, spinodal, settle, seed_everything

# --- T2: menstrual cycle as a slow relaxation oscillator ---------------------------------------

def menstrual_oscillator(tau_s=600.0, drive=0.35, T=12000.0, dt=0.05):
    """The slow FHN. Returns the membrane trace S (oestradiol-analogue) and dt."""
    seed_everything()
    n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(tau_s), beta=0.5, name="menstrual")
    return n.run(drive=drive, T=T, dt=dt)

def relaxation_asymmetry(S, dt):
    """Quantify the rise/fall asymmetry over one full cycle (the relaxation signature).

    A relaxation oscillator has a fast excursion and a slow recovery: the upstroke time and the
    recovery time differ by a large factor. A sinusoid is time-symmetric: rise == fall, so the
    asymmetry ratio is exactly 1.0. We therefore measure asymmetry = max(rise,fall)/min(rise,fall);
    >> 1 is relaxation, ~ 1 is sinusoidal. (The fraction-of-time-in-the-upper-state is NOT a shape
    discriminant -- a slow decay sits 'high' for most of the period yet is still relaxation -- so we
    use the timing asymmetry directly.)"""
    sp = Neuron.spikes(S)
    if len(sp) < 2:
        return None
    i0, i1 = int(sp[0]), int(sp[1])               # one period between successive surges
    seg = S[i0:i1]
    peak = int(np.argmax(seg))                    # fast-discharge (surge) location within the period
    rise = max(peak, 1) * dt                      # trough -> peak  (fast ovulatory excursion)
    fall = max(len(seg) - peak, 1) * dt           # peak  -> reset  (slow luteal/follicular recovery)
    asym = float(max(rise, fall) / min(rise, fall))
    return dict(period_arb=round(float((i1 - i0) * dt), 3), rise_arb=round(rise, 3),
                fall_arb=round(fall, 3), asymmetry_ratio=round(asym, 3))

def run_T2():
    S, dt = menstrual_oscillator()
    sp = Neuron.spikes(S)
    asy = relaxation_asymmetry(S, dt)
    oscillates = bool(len(sp) >= 3)
    # PASS: oscillates AND the waveform is asymmetric (relaxation), not symmetric (sinusoid).
    # Boundary 2.0 = "rise and fall differ by at least 2x"; the realised ratio is far above it, so
    # the exact boundary is immaterial (qualitative asymmetric-vs-symmetric split, not a tuned value).
    relaxation = bool(asy is not None and asy["asymmetry_ratio"] > 2.0)
    passed = bool(oscillates and relaxation)
    return dict(target="T2", title="Menstrual cycle as a slow relaxation oscillator",
                oscillates=oscillates, cycles=int(len(sp)),
                **(asy or {}), is_relaxation_not_sinusoid=relaxation,
                grade="[V] relaxation mechanism; [L] ~28 d period anchor",
                status=("PASS" if passed else "FAIL"))

# --- T3: oestrogen feedback switch + LH surge with hysteresis ----------------------------------

def feedback_switch_curve(g=1.0, n=240):
    """Sweep the oestradiol drive UP then DOWN; record the settled LH-axis state. A bistable switch
    shows a discontinuous flip and hysteresis (up-threshold != down-threshold)."""
    hsp = spinodal(g)
    hs = np.linspace(-1.3 * hsp, 1.3 * hsp, n)
    up = np.empty(n); s = -math.sqrt(g)
    for i, h in enumerate(hs):
        s = settle(g, h, s0=s); up[i] = s
    down = np.empty(n); s = +math.sqrt(g)
    for i, h in enumerate(hs[::-1]):
        s = settle(g, h, s0=s); down[i] = s
    down = down[::-1]
    up_jump = int(np.argmax(np.abs(np.diff(up))))
    down_jump = int(np.argmax(np.abs(np.diff(down))))
    return dict(spinodal=round(float(hsp), 6),
                surge_up_threshold=round(float(hs[up_jump]), 6),
                return_down_threshold=round(float(hs[down_jump]), 6),
                up_jump_size=round(float(np.abs(np.diff(up))[up_jump]), 4),
                hysteresis_width=round(float(hs[up_jump] - hs[down_jump]), 6))

def run_T3():
    c = feedback_switch_curve()
    discontinuous = bool(c["up_jump_size"] > 0.5)
    hysteresis = bool(c["hysteresis_width"] > 1e-3)  # up-threshold strictly above down-threshold
    passed = bool(discontinuous and hysteresis)
    return dict(target="T3", title="Oestrogen feedback switch: negative -> positive (LH surge) flip",
                **c, surge_is_discontinuous=discontinuous, shows_hysteresis=hysteresis,
                note="same R19 bistable primitive as malignant transformation in _oncology",
                grade="[V] switch mechanism", status=("PASS" if passed else "FAIL"))

if __name__ == "__main__":
    import json
    print(json.dumps(dict(T2=run_T2(), T3=run_T3()), ensure_ascii=False, indent=2))
