#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hpg_axis.py  --  T1 (GnRH pulse generator) + T5 (puberty onset) on the shared substrate.

T1 -- the hypothalamic GnRH pulse generator (the arcuate KNDy network) is the shared FHN relaxation
      oscillator: a fast R19 switch with slow recovery emits a relaxation PULSE train. Each GnRH
      pulse drives a downstream gonadotrope pulse (LH/FSH). The clinically central fact -- pulse
      FREQUENCY decodes to gonadotropin identity (fast pulses favour LH, slow favour FSH) -- is
      reproduced as a property of the recovery timescale tau_s. Mechanism [V]; pulse RATE is an
      [L] anchor (follicular ~1 pulse / 60-90 min), not emergent.

T5 -- the juvenile pause is the GnRH oscillator held in the R19 OFF basin. Puberty is the SAME
      switch crossing its spinodal as a slow maturation drive rises: the onset of pulsing is
      DISCONTINUOUS (a threshold crossing), not a gradual ramp. This is the discriminant -- the
      pulse amplitude jumps at h ~ spinodal. Mechanism/order [V]; chronological age is [O].

No new physics: everything uses inherited/vp_substrate.py (FHN Neuron + R19 spinodal). Deterministic
(BLAS pinned, fixed seed, round-before-hash upstream in the engine).
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Neuron, spinodal, sdot, seed_everything, dominant_freq

# --- T1: GnRH pulse generator ------------------------------------------------------------------

def gnrh_pulse_generator(tau_s, drive=0.30, T=8000.0, dt=0.05):
    """Run the GnRH pulse generator as the shared FHN. Returns (pulse_count, mean_interval, freq)."""
    seed_everything()
    n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(tau_s), beta=0.5, name="GnRH")
    S, _dt = n.run(drive=drive, T=T, dt=dt)
    sp = Neuron.spikes(S)
    isi = np.diff(sp) * dt
    return int(len(sp)), (float(isi.mean()) if len(isi) else float("nan")), float(dominant_freq(S, dt))

def frequency_decoding():
    """Pulse-frequency -> gonadotropin identity. Fast pulses (short tau_s) emit MORE pulses per unit
    time = LH-favouring; slow pulses (long tau_s) = FSH-favouring. We report pulse RATE vs tau_s and
    confirm the monotone mapping (the substrate basis of GnRH frequency coding). [V]; rate anchor [L]."""
    rows = []
    for tau_s in (20.0, 60.0, 150.0, 400.0):
        nb, mean_isi, f = gnrh_pulse_generator(tau_s)
        rate = nb / 8000.0  # pulses per arb-time
        rows.append(dict(tau_s=tau_s, pulses=nb, mean_interval_arb=round(mean_isi, 4),
                         pulse_rate_arb=round(rate, 8),
                         favours=("LH (fast)" if tau_s <= 60.0 else "FSH (slow)")))
    rates = [r["pulse_rate_arb"] for r in rows]
    monotone = all(rates[i] > rates[i + 1] for i in range(len(rates) - 1))  # rate falls as tau_s rises
    return dict(rows=rows, rate_monotone_in_tau=bool(monotone),
                interpretation="pulse rate decreases monotonically with tau_s -> frequency decodes to "
                               "LH/FSH balance; fast=LH, slow=FSH",
                mechanism_grade="[V]", rate_anchor="follicular GnRH/LH ~1 pulse / 60-90 min [L]")

def run_T1():
    nb, mean_isi, f = gnrh_pulse_generator(60.0)
    dec = frequency_decoding()
    oscillates = bool(nb >= 3 and f > 0.0)
    passed = bool(oscillates and dec["rate_monotone_in_tau"])
    return dict(target="T1", title="GnRH pulse generator (FHN relaxation oscillator)",
                oscillates=oscillates, pulses=nb, mean_interval_arb=round(mean_isi, 4),
                relaxation_freq_arb=round(f, 8), frequency_decoding=dec,
                grade="[V] mechanism; [L] rate anchor", status=("PASS" if passed else "FAIL"))

# --- T5: puberty onset as a spinodal crossing --------------------------------------------------

def puberty_onset(g=1.0, ramp_hi_mult=1.3, n_steps=400, settle=400, dt=0.02):
    """Slowly ramp a maturation drive from 0 past the spinodal; the R19 gate (pulse-enable) jumps
    DISCONTINUOUSLY at the spinodal. Returns the location of the jump relative to the spinodal."""
    hsp = spinodal(g)
    s = -math.sqrt(g)  # juvenile: held OFF
    hs = np.linspace(0.0, ramp_hi_mult * hsp, n_steps)
    states = np.empty(n_steps)
    for i, h in enumerate(hs):
        for _ in range(settle):
            s += dt * sdot(s, g, h)
        states[i] = s
    jumps = np.abs(np.diff(states))
    j = int(np.argmax(jumps))
    return dict(spinodal=round(float(hsp), 6), jump_drive=round(float(hs[j]), 6),
                jump_over_spinodal=round(float(hs[j] / hsp), 4), jump_size=round(float(jumps[j]), 4),
                state_before=round(float(states[j]), 4), state_after=round(float(states[j + 1]), 4))

def run_T5():
    p = puberty_onset()
    # PASS: a single large discontinuous jump localised at the spinodal (0.9..1.1 x), OFF->ON.
    localised = bool(0.9 <= p["jump_over_spinodal"] <= 1.1)
    discontinuous = bool(p["jump_size"] > 0.5 and p["state_before"] < 0.0 < p["state_after"])
    passed = bool(localised and discontinuous)
    return dict(target="T5", title="Puberty onset as a discontinuous spinodal crossing",
                **p, jump_localised_at_spinodal=localised, onset_discontinuous=discontinuous,
                grade="[V] mechanism/order; [O] chronological age (needs external calibration)",
                status=("PASS" if passed else "FAIL"))

if __name__ == "__main__":
    import json
    print(json.dumps(dict(T1=run_T1(), T5=run_T5()), ensure_ascii=False, indent=2))
