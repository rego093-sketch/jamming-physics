#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
temporal_pattern.py  --  the TEMPORAL-PATTERN therapeutic lever (high-ambition capstone).

ONE control axis the textbook level-based picture misses
--------------------------------------------------------
The reproductive substrate is a relaxation oscillator (T1-T4) sitting on a bistable R19 switch (T3,
oncology). For such a system the TIME PATTERN of the hormone drive -- pulsatile vs continuous, cycling
vs sustained -- is a control axis SEPARATE from the drive LEVEL. Two consequences, each retrodicting
established clinical practice and each a falsifiable model statement:

  (A) SAME MOLECULE, OPPOSITE EFFECT (endocrine).
      PULSATILE GnRH drives the downstream oscillator (each pulse re-ignites it) -> axis ACTIVATED
      (clinical: pulsatile GnRH pump restores ovulation in hypothalamic amenorrhoea).
      CONTINUOUS GnRH-agonist pins the same drive high, past the fold, so the oscillator can no longer
      cycle -> axis SUPPRESSED by desensitisation (clinical: depot GnRH agonists for precocious
      puberty, endometriosis, prostate cancer). The substrate reproduces both from ONE molecule.

  (B) CYCLING DEFEATS ADAPTATION (oncology).
      Endocrine therapy resistance = receptor OVER-EXPRESSION = amplified drive-coupling kappa (NOT a
      deeper well). A resistant clone (high kappa) tolerates ANY constant drive by re-settling, so
      continuous high (T) and continuous low (ADT) leave it quiet. CYCLING the drive whipsaws its
      amplified coupling across the fold faster than it can settle -> large transition stress it cannot
      escape. Selectivity is measured by the transition-stress index = mean |ds/dt| over the schedule
      (no arbitrary kill threshold). Retrodicts Bipolar Androgen Therapy in CRPC and oestrogen-induced
      apoptosis in long-term-oestrogen-deprived (LTED) breast cancer.

GRADES: the qualitative principle (pattern is a lever; cycling stresses the adapted clone most) is
[V] simulation-verified; the clinical translation (schedules, periods, doses) is [O] -- it needs
trials. No parameter is tuned to a target; kappa, amplitude and period are stated inputs.

Uses only inherited/vp_substrate.py. Deterministic.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, Neuron, seed_everything

# ---------------------------------------------------------------------------------------------------
# (B) Cycling-vs-continuous selectivity  (Bipolar Androgen Therapy / LTED-pulse)
# ---------------------------------------------------------------------------------------------------

def transition_stress(g, kappa, h_sched, dt=0.01, steps=160):
    """Integrated mean |ds/dt| of the R19 state under EFFECTIVE drive kappa*h.
    Resistance is amplified receptor coupling kappa (not a deeper well). Forced fold crossings that
    the cell cannot settle through produce large slew; adiabatic following produces almost none."""
    s = -math.sqrt(g); total = 0.0
    for h in h_sched:
        heff = kappa * h
        for _ in range(steps):
            ds = (g * s - s ** 3 + heff) * dt
            s += ds; total += abs(ds)
    return total / (len(h_sched) * steps * dt)

def bat_selectivity(g=1.0, kappa_sens=1.0, kappa_res=3.0, amp_frac=0.9, N=48, period=8):
    sp = spinodal(g); amp = amp_frac * sp
    half = period // 2
    scheds = {
        "continuous_high_T":   [+amp] * N,
        "continuous_low_ADT":  [-amp] * N,
        "cycling_BAT":         [(+amp if (i // half) % 2 == 0 else -amp) for i in range(N)],
    }
    rows = {}
    for name, sch in scheds.items():
        ss = transition_stress(g, kappa_sens, sch)
        sr = transition_stress(g, kappa_res, sch)
        rows[name] = dict(sensitive=round(ss, 4), resistant=round(sr, 4),
                          res_over_sens=round(sr / ss, 2) if ss > 0 else None)
    cyc_r = rows["cycling_BAT"]["resistant"]
    cont_r = rows["continuous_high_T"]["resistant"]
    cycling_amplifies = bool(cyc_r > cont_r)
    fold = round(cyc_r / cont_r, 1) if cont_r > 0 else None
    # resistant clone is stressed MORE than the sensitive one under cycling (selective)
    selective = bool(rows["cycling_BAT"]["res_over_sens"] is not None and rows["cycling_BAT"]["res_over_sens"] > 1.0)
    return dict(kappa_sensitive=kappa_sens, kappa_resistant=kappa_res, amplitude_frac_spinodal=amp_frac,
                cycle_period=period, table=rows,
                cycling_amplifies_resistant_stress=cycling_amplifies,
                cycling_over_continuous_high_resistant_fold=fold,
                cycling_selective_for_resistant=selective,
                retrodicts="Bipolar Androgen Therapy (CRPC); oestrogen-induced apoptosis in LTED breast",
                grade="[V] selectivity principle; [O] clinical schedule")

# ---------------------------------------------------------------------------------------------------
# (A) Same molecule, opposite effect  (pulsatile vs continuous GnRH)
# ---------------------------------------------------------------------------------------------------

def _count_pulses(S):
    return int(len(Neuron.spikes(S)))

def gnrh_pulsatile_vs_continuous(tau_s=60.0, T=4000.0, dt=0.05, pulse_period=200, pulse_width=20):
    """Downstream gonadotrope as an FHN. Deliver the SAME agent two ways and count output pulses.
    Pulsatile -> the gonadotrope keeps firing (ACTIVATION). Continuous high -> driven past the fold,
    output stops (SUPPRESSION by desensitisation)."""
    import numpy as np
    sp = spinodal(1.0)
    drive_hi = 2.5 * sp                     # above the depolarization-block threshold (~2*spinodal):
                                            # held continuously it blocks the oscillator (desensitisation);
                                            # delivered as brief pulses it evokes one excursion each.
    n_steps = int(T / dt)
    # pulsatile schedule: brief supra-threshold pulses separated by silence
    phase = np.arange(n_steps) % pulse_period
    pulsatile = np.where(phase < pulse_width, drive_hi, 0.0)
    # continuous schedule: the same agent held on
    continuous = np.full(n_steps, drive_hi)

    def run(drive_series):
        seed_everything()
        nn = Neuron(gamma=1.0, tau_f=1.0, tau_s=tau_s, beta=0.5, name="gonadotrope")
        S, _ = nn.run(drive=drive_series, T=T, dt=dt, s0=0.0, w0=0.0)
        return S

    S_pulse = run(pulsatile)
    S_cont = run(continuous)
    p_pulse = _count_pulses(S_pulse)
    p_cont = _count_pulses(S_cont)
    activates = bool(p_pulse >= 3)
    suppresses = bool(p_cont <= 1)
    same_molecule_opposite = bool(activates and suppresses)
    return dict(pulsatile_output_pulses=p_pulse, continuous_output_pulses=p_cont,
                pulsatile_activates=activates, continuous_suppresses=suppresses,
                same_molecule_opposite_effect=same_molecule_opposite,
                retrodicts="pulsatile GnRH pump activates (FHA); depot GnRH agonist suppresses "
                           "(precocious puberty / endometriosis / prostate)",
                grade="[V] pattern-dependent sign of effect")

def run_therapy():
    bat = bat_selectivity()
    gnrh = gnrh_pulsatile_vs_continuous()
    checks = dict(
        cycling_amplifies_resistant=bat["cycling_amplifies_resistant_stress"],
        cycling_selective=bat["cycling_selective_for_resistant"],
        gnrh_same_molecule_opposite=gnrh["same_molecule_opposite_effect"],
    )
    passed = all(checks.values())
    return dict(principle="temporal pattern of hormone drive is a control axis separate from level",
                bat_cycling=bat, gnrh_pattern=gnrh, checks=checks,
                status=("PASS" if passed else "FAIL"),
                grades="principle [V]; clinical schedule [O]")

def status():
    return run_therapy()

if __name__ == "__main__":
    print(json.dumps(run_therapy(), ensure_ascii=False, indent=2))
