#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spermatogenesis.py  --  T4: the seminiferous (spermatogenic) cycle.

The seminiferous epithelium turns over on a fixed clock -- in man the cycle of the seminiferous
epithelium is ~16 days, INTERMEDIATE between the minute-scale GnRH pulse (T1) and the ~28 day
menstrual relaxation oscillator (T2). T4 makes the structural claim, NOT a fitted number:

  (a) the SAME R19/FHN substrate yields a THIRD relaxation oscillator just by changing the slow
      recovery timescale tau_s -- nothing else in the kernel changes; and
  (b) the three reproductive clocks come out in the correct ORDER:
            pulse (T1)  <  spermatogenic (T4)  <  menstrual (T2).

tau_s for T4 is fixed from the MEASURED clinical period ratio (~16 d : ~28 d ~ 0.57) applied to the
menstrual tau_s that T2 already locked (600) -> ~343, rounded to 350. That makes the *period* an [L]
anchor (it inherits a measured ratio); the relaxation CHARACTER and the ORDERING are the [V] claims.
No parameter is chosen to hit a target output.

Uses only inherited/vp_substrate.py. Deterministic.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Neuron, seed_everything

# clinical period anchors (days) -- MEASURED inputs, used only to set the recovery timescale ratio.
PULSE_DAYS_L        = 0.0625    # GnRH pulse ~ 1 / 90 min   (follicular)            [L]
SPERMATOGENIC_DAYS_L = 16.0     # human seminiferous epithelial cycle               [L]
MENSTRUAL_DAYS_L    = 28.0      # menstrual cycle                                    [L]

TAU_S_MENSTRUAL = 600.0                                   # locked by T2
TAU_S_SPERMATO  = round(TAU_S_MENSTRUAL * SPERMATOGENIC_DAYS_L / MENSTRUAL_DAYS_L / 10.0) * 10.0  # ->350

def spermatogenic_oscillator(tau_s=TAU_S_SPERMATO, drive=0.35, T=9000.0, dt=0.05):
    """Intermediate-timescale FHN. Returns the membrane trace S and dt."""
    seed_everything()
    n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(tau_s), beta=0.5, name="spermatogenic")
    return n.run(drive=drive, T=T, dt=dt)

def _period_and_asymmetry(S, dt):
    sp = Neuron.spikes(S)
    if len(sp) < 2:
        return None
    i0, i1 = int(sp[0]), int(sp[1])
    seg = S[i0:i1]
    peak = int(np.argmax(seg))
    rise = max(peak, 1) * dt
    fall = max(len(seg) - peak, 1) * dt
    asym = float(max(rise, fall) / min(rise, fall))
    return dict(cycles=int(len(sp)), period_arb=round(float((i1 - i0) * dt), 3),
                asymmetry_ratio=round(asym, 3))

def _period_of(tau_s, T, dt=0.05):
    seed_everything()
    n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(tau_s), beta=0.5, name="probe")
    S, _ = n.run(drive=0.35, T=T, dt=dt)
    sp = Neuron.spikes(S)
    if len(sp) < 2:
        return None
    return float((int(sp[1]) - int(sp[0])) * dt)

def run_T4():
    S, dt = spermatogenic_oscillator()
    pa = _period_and_asymmetry(S, dt)
    oscillates = bool(pa is not None and pa["cycles"] >= 3)
    relaxation = bool(pa is not None and pa["asymmetry_ratio"] > 2.0)
    # period ordering from the SAME substrate at the three locked recovery timescales
    p_pulse = _period_of(60.0,  T=3000.0)    # T1 default generator
    p_sperm = pa["period_arb"] if pa else None
    p_menst = _period_of(600.0, T=12000.0)   # T2 menstrual
    ordered = bool(p_pulse is not None and p_sperm is not None and p_menst is not None
                   and p_pulse < p_sperm < p_menst)
    passed = bool(oscillates and relaxation and ordered)
    return dict(target="T4", title="Seminiferous (spermatogenic) cycle -- intermediate relaxation clock",
                tau_s=TAU_S_SPERMATO, oscillates=oscillates,
                **(pa or {}),
                is_relaxation_not_sinusoid=relaxation,
                period_ordering=dict(pulse_arb=(round(p_pulse,3) if p_pulse else None),
                                     spermatogenic_arb=(round(p_sperm,3) if p_sperm else None),
                                     menstrual_arb=(round(p_menst,3) if p_menst else None),
                                     pulse_lt_spermatogenic_lt_menstrual=ordered),
                clinical_days=dict(pulse=PULSE_DAYS_L, spermatogenic=SPERMATOGENIC_DAYS_L,
                                   menstrual=MENSTRUAL_DAYS_L),
                grade="[V] third-oscillator + ordering; [L] ~16 d period anchor (clinical ratio)",
                status=("PASS" if passed else "FAIL"))

if __name__ == "__main__":
    import json
    print(json.dumps(dict(T4=run_T4()), ensure_ascii=False, indent=2))
