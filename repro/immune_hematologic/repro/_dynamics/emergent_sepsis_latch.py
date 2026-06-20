#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_sepsis_latch.py  --  EMERGENT systemic inflammatory latch and its TIME-CRITICAL break window by direct
coupled stochastic simulation (not asserted, not fitted).  [DISEASE/TREATMENT axis: roadmap D4, target T31.]

WHY THIS EXISTS (v0.11.0). T9 (emergent_chronicity.py) MEASURED that a SINGLE inflammatory cell latches chronic
when a supra-spinodal insult is held long enough, and the latch persists after the insult clears -- hysteresis at
the single-switch scale. Sepsis / SIRS / cytokine storm is a genuinely DISTINCT dynamical regime: the same
hysteresis at SYSTEMIC scale, where a POPULATION of inflammatory cells is coupled through a shared, ACCUMULATING
cytokine tone (positive feedback with its OWN slow timescale -- activated cells raise the tone, the tone recruits
more cells), so the inflammatory state becomes COLLECTIVELY self-sustaining and progressively HARDER to reverse as
it recruits. The roadmap asks the two questions the single-cell latch cannot answer: what systemic insult LATCHES
the collective basin, and -- the clinically decisive one -- is there a NARROW, TIME-CRITICAL window in which a
counter-drive can break the latch BEFORE it self-sustains? The VP discipline is emergence: the threshold, the
window, and its time-criticality must come OUT of the SAME R19 substrate, MEASURED.

This module runs Nc inflammatory cells, each an R19 switch starting in the resting OFF basin, coupled by a shared
cytokine-tone field M(t) that ACCUMULATES from the activated fraction and decays on its own timescale τ_M,

    ds_i = (γ s_i − s_i³ + h_i(t)) dt + sqrt(2 D dt)·ξ_i,   h_i = a_ext(t)·spinodal + M(t) − counter(t)·spinodal,
    dM   = (α · frac_ON(t) · spinodal − M/τ_M) dt,

where a_ext is a rectangular SYSTEMIC insult (then withdrawn), M is the positive-feedback cytokine tone, and
counter is an optional anti-inflammatory counter-drive applied for a fixed treatment window at a chosen DELAY after
insult onset. Because cells cross the saddle one-by-one (Kramers) and every crossing feeds M which drives the next,
the activated fraction recruits AUTOCATALYTICALLY and M climbs over time -- so the longer the latch runs, the larger
M is and the harder a FIXED counter-drive is to win (the counter must overcome M to flip a cell OFF, and M
re-recruits any cell it does flip while M stays high). Nothing about the window is assumed; frac_ON and M are
counted/integrated trajectories.

WHAT EMERGES (measured, deterministic seed=19):
  1. A SYSTEMIC LATCH IGNITES NEAR THE SPINODAL AND SELF-SUSTAINS. The systemic-insult amplitude at which the
     collective state latches (measured over the population) sits at the organ's spinodal scale (the cells must
     cross their own saddle to seed the cascade), and ABOVE it the activated fraction stays high AFTER the insult is
     withdrawn -- M holds the basin, a self-sustaining inflammatory state (the systemic mirror of the T9 chronic
     latch), MEASURED.
  2. A TIME-CRITICAL BREAK WINDOW EXISTS. A FIXED counter-drive applied for a FIXED duration BREAKS the latch
     (measured final activated fraction ≈ 0) when applied EARLY but FAILS (final fraction ≈ 1) when applied LATE:
     sweeping the treatment DELAY, break-success falls monotonically and crosses ½ at a critical delay t_crit, after
     which the accumulated cytokine tone M is too large for the same counter-drive to overcome -- a measured, narrow
     window. The SAME intervention that cures early is useless late: urgency is a substrate property.
  3. THE TIME-CRITICALITY REQUIRES THE POSITIVE FEEDBACK (mechanism control). With the cytokine feedback OFF
     (α = 0, so M ≡ 0) the counter-drive flips cells OFF and -- with no tone to re-recruit them -- they STAY off, so
     break-success is essentially INDEPENDENT of delay (measured range over delays ≈ 0): the window's
     time-criticality is PRODUCED by the recruiting feedback, MEASURED by turning it off.
  4. TITRATING THE TRIGGER IS INSUFFICIENT -- THE LATCH MUST BE BROKEN. Once the supra-threshold insult has latched
     the basin, simply removing the trigger (the insult is already withdrawn) does NOT resolve it (measured final
     fraction stays high -- self-sustaining), whereas an in-window basin-exit counter-drive collapses it (measured
     final fraction ≈ 0). The dynamics say: break the latch EARLY (basin-exit before self-sustain), not titrate the
     trigger, MEASURED.

TREATMENT DIRECTION (roadmap discipline -- CLASS / URGENCY-STRUCTURE only, never agent/dose). The dynamics point to
breaking the systemic latch EARLY by an active basin-exit counter-drive, within a time-critical window; trigger
removal/titration alone is insufficient once the basin self-sustains, and the window CLOSES as the cytokine tone
accumulates. This is a re-description of systemic-inflammation dynamics in the R19/Kramers formalism and a
principled treatment DIRECTION + urgency structure; it is NOT a drug, dose, schedule, clinical recommendation, or
VP validation, and NOT medical advice.

GRADES (C3): the systemic latch (ignition at the spinodal scale, self-sustaining), the existence and
time-criticality of the break window, its requirement of the positive feedback, and the trigger-removal-insufficient
contrast are [V] emergent (measured from the coupled stochastic population). The ABSOLUTE insult amplitude / window
length / clinical timing -- set by the cytokine gain α and timescale τ_M, the counter-drive amplitude/duration, and
the free cellular-noise scale D -- is [O], no fabricated numbers, and every clinical scale stays [O] with a stated
obstacle. Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_PRIMARY = "lymphoid_adaptive"     # the inflammatory compartment carrying the systemic latch

# --- deterministic simulation size (fixed; coupled population + accumulating cytokine tone; no per-condition tuning) ---
_NC        = 250      # coupled inflammatory cells
_DT        = 0.01     # integration timestep
_D         = 0.02     # cellular-noise scale (low: sharp boundary; absolute value is [O])
_ALPHA     = 0.50     # cytokine-tone accumulation gain (× spinodal per unit activated fraction); [O]
_TAU_M     = 6.0      # cytokine-tone decay timescale (time units); M_max = α·τ_M·spinodal ≈ 3·spinodal; [O]
_INSULT_DUR = 450     # systemic insult duration (steps), then withdrawn
_A_LATCH   = 1.15     # supra-threshold systemic insult (× spinodal) for the break / self-sustain experiments
_COUNTER   = 2.60     # counter-drive amplitude (× spinodal) -- overcomes M when M is small, not when large; [O]
_TREAT_DUR = 400      # counter-drive (treatment) duration (steps)
_TOTAL_THR = 1400     # steps for threshold / self-sustain sims (latch forms + settles)
_TOTAL_BRK = 2300     # steps for break-window sims (covers the latest delay + treatment + settle)

_AMPS    = (0.70, 0.90, 0.95, 1.00, 1.05, 1.15, 1.30)            # systemic-insult amplitude grid (× spinodal)
_DELAYS  = (460, 600, 720, 800, 880, 1100, 1400, 1600)          # treatment delay after insult onset (steps)


def _run_systemic(g, a_ext, alpha, counter=0.0, delay=None, treat_dur=_TREAT_DUR,
                  insult_dur=_INSULT_DUR, total=_TOTAL_BRK, tau_m=_TAU_M, D=_D, Nc=_NC, dt=_DT, seed=SEED):
    """MEASURE the final activated fraction of a cytokine-coupled inflammatory population: a rectangular systemic
    insult a_ext·sp for insult_dur, an accumulating shared cytokine tone M (gain α, decay τ_M), and an optional
    counter-drive −counter·sp for treat_dur starting at `delay`; then settle. Returns frac_ON at the end."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(Nc, -math.sqrt(g))                 # all cells resting (OFF)
    M = 0.0
    sq = math.sqrt(2.0 * D * dt)
    t_start = delay if delay is not None else (total + 1)
    t_end = t_start + treat_dur
    for t in range(total):
        frac_on = float((s > 0.0).mean())
        M += (alpha * frac_on * sp - M / tau_m) * dt        # accumulating cytokine tone (positive feedback)
        h_ext   = (a_ext * sp) if t < insult_dur else 0.0
        h_count = (-counter * sp) if (t_start <= t < t_end) else 0.0
        s += (g * s - s ** 3 + h_ext + M + h_count) * dt + sq * rng.standard_normal(Nc)
        np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _latch_threshold(g, alpha=_ALPHA, amps=_AMPS, D=_D, seed=SEED):
    """Interpolate the systemic-insult amplitude (× spinodal) at which the final activated fraction crosses 0.5
    (no treatment) -- the collective latch ignition threshold."""
    fr = [_run_systemic(g, a, alpha, counter=0.0, delay=None, total=_TOTAL_THR, D=D, seed=seed) for a in amps]
    if fr[0] >= 0.5:
        return amps[0], fr
    for i in range(1, len(fr)):
        if fr[i - 1] < 0.5 <= fr[i]:
            f = (0.5 - fr[i - 1]) / (fr[i] - fr[i - 1])
            return amps[i - 1] + f * (amps[i] - amps[i - 1]), fr
    return (amps[-1] if fr[-1] >= 0.5 else float("inf")), fr


def _break_curve(g, alpha, insult=_A_LATCH, counter=_COUNTER, delays=_DELAYS, D=_D, seed=SEED):
    """MEASURE final activated fraction vs treatment DELAY at fixed insult / counter-drive. Break-success = 1 −
    final fraction (low final fraction = latch broken)."""
    rows = []
    for d in delays:
        fr = _run_systemic(g, insult, alpha, counter=counter, delay=d, total=_TOTAL_BRK, D=D, seed=seed)
        rows.append((d, fr, 1.0 - fr))
    return rows


def _crit_delay(rows):
    """Interpolate the delay at which break-success crosses 0.5 downward (final fraction crosses 0.5 upward)."""
    for i in range(1, len(rows)):
        if rows[i - 1][1] < 0.5 <= rows[i][1]:
            f = (0.5 - rows[i - 1][1]) / (rows[i][1] - rows[i - 1][1])
            return rows[i - 1][0] + f * (rows[i][0] - rows[i - 1][0])
    return None


def emergent_sepsis_latch(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # (1) SYSTEMIC LATCH IGNITION near the spinodal scale, organ by organ + self-sustaining persistence
    thr_rows = {}
    crit_ok = True
    for o in _ORGANS:
        g = gammas[o]
        a_crit, _fr = _latch_threshold(g, alpha=_ALPHA, D=D)
        thr_rows[o] = dict(a_crit_over_spinodal=round(a_crit, 3),
                           near_spinodal=bool(abs(a_crit - 1.0) < 0.16))
        crit_ok = crit_ok and thr_rows[o]["near_spinodal"]
    # self-sustain: supra-threshold insult, NO treatment -> stays high after withdrawal; sub-threshold -> resolves
    frac_supra = _run_systemic(g_ref, _A_LATCH, _ALPHA, counter=0.0, delay=None, total=_TOTAL_THR, D=D)
    frac_sub   = _run_systemic(g_ref, 0.70,     _ALPHA, counter=0.0, delay=None, total=_TOTAL_THR, D=D)
    self_sustains = bool(frac_supra >= 0.85 and frac_sub <= 0.15)

    # (2) TIME-CRITICAL BREAK WINDOW (α>0): break-success monotone DECREASING in delay, crosses 0.5
    rows_on = _break_curve(g_ref, _ALPHA, D=D)
    succ_on = [r[2] for r in rows_on]
    t_crit = _crit_delay(rows_on)
    succ_decreasing = all(succ_on[i + 1] <= succ_on[i] + 0.06 for i in range(len(succ_on) - 1))
    early_breaks = bool(succ_on[0] >= 0.85)
    late_fails   = bool(succ_on[-1] <= 0.15)
    window_ok = bool(succ_decreasing and early_breaks and late_fails and (t_crit is not None))

    # (3) TIME-CRITICALITY REQUIRES THE POSITIVE FEEDBACK: α=0 -> break-success ~flat (range ≈ 0)
    rows_off = _break_curve(g_ref, 0.0, D=D)
    succ_off = [r[2] for r in rows_off]
    range_off = float(max(succ_off) - min(succ_off))
    range_on  = float(max(succ_on)  - min(succ_on))
    off_breaks_always = bool(min(succ_off) >= 0.85)     # with no tone, the counter-drive always wins
    feedback_required = bool(range_off < 0.15 and range_on > 0.6 and off_breaks_always)

    # (4) TITRATING THE TRIGGER IS INSUFFICIENT vs IN-WINDOW LATCH-BREAK
    frac_no_treat = frac_supra                                                   # self-sustained (high)
    frac_early    = _run_systemic(g_ref, _A_LATCH, _ALPHA, counter=_COUNTER,
                                  delay=_DELAYS[0], total=_TOTAL_BRK, D=D)         # broken (low)
    trigger_removal_insufficient = bool(frac_no_treat >= 0.85)
    in_window_break_works        = bool(frac_early <= 0.15)
    direction_ok = bool(trigger_removal_insufficient and in_window_break_works)

    ok = bool(crit_ok and self_sustains and window_ok and feedback_required and direction_ok)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6),
        cytokine_gain_alpha=_ALPHA, cytokine_tau=_TAU_M, M_max_over_spinodal=round(_ALPHA * _TAU_M, 3),
        noise_D=D, Nc=_NC,
        systemic_latch_threshold=thr_rows, latch_ignites_near_spinodal=bool(crit_ok),
        self_sustain=dict(frac_supra_after_withdraw=round(frac_supra, 3),
                          frac_sub_after_withdraw=round(frac_sub, 3), self_sustains=bool(self_sustains)),
        break_window=dict(insult=_A_LATCH, counter=_COUNTER, treat_dur=_TREAT_DUR,
                          delays=[r[0] for r in rows_on],
                          final_fraction=[round(r[1], 3) for r in rows_on],
                          break_success=[round(r[2], 3) for r in rows_on],
                          t_crit_delay=(round(t_crit, 1) if t_crit is not None else None),
                          monotone_decreasing=bool(succ_decreasing),
                          early_breaks=bool(early_breaks), late_fails=bool(late_fails),
                          window_exists=bool(window_ok)),
        feedback_control=dict(break_success_alpha0=[round(x, 3) for x in succ_off],
                              range_alpha0=round(range_off, 3), range_alpha_on=round(range_on, 3),
                              alpha0_breaks_at_all_delays=bool(off_breaks_always),
                              time_criticality_requires_feedback=bool(feedback_required)),
        treatment_direction=dict(final_fraction_no_treatment=round(frac_no_treat, 3),
                                 final_fraction_early_break=round(frac_early, 3),
                                 trigger_removal_insufficient=bool(trigger_removal_insufficient),
                                 in_window_break_works=bool(in_window_break_works),
                                 break_early_not_titrate=bool(direction_ok)),
        all_pass=ok,
        grade="[V] a systemic inflammatory LATCH and a TIME-CRITICAL break window EMERGE from a cytokine-coupled "
              "R19 population: the collective latch ignites at the organ's spinodal scale and the basin SELF-SUSTAINS "
              "after the insult is withdrawn (the accumulated cytokine tone M holds it -- the systemic mirror of the "
              "T9 chronic latch), a FIXED counter-drive BREAKS the latch when applied early but FAILS when applied "
              "late (measured break-success falls monotonically with treatment delay and crosses a critical delay "
              "once M has accumulated past what the counter can overcome -- a narrow window), the window's "
              "time-criticality REQUIRES the positive feedback (α=0 -> break-success independent of timing), and "
              "trigger-removal alone is insufficient once self-sustaining while an in-window basin-exit counter-drive "
              "collapses it -- measured, not assumed; [O] absolute insult amplitude / window length / clinical "
              "timing (cytokine gain α / timescale τ_M, counter amplitude / duration, cellular-noise scale D); "
              "treatment = DIRECTION/URGENCY-STRUCTURE (break the latch early, basin-exit before self-sustain), never "
              "agent / dose / recommendation")


def run(gammas):
    """T31: emergent systemic inflammatory latch + time-critical break window -- a cytokine-coupled R19 population
    latches a self-sustaining inflammatory basin past a spinodal-scale threshold, and a fixed counter-drive breaks
    it only inside a narrow, recruitment-closed time window whose urgency REQUIRES the positive feedback; trigger
    removal alone is insufficient -- the latch-break dual of the T23 persistence at systemic scale."""
    r = emergent_sepsis_latch(gammas)
    return dict(T31=dict(target="T31",
                         claim="a systemic inflammatory LATCH and a TIME-CRITICAL break window EMERGE from a "
                               "cytokine-coupled R19 population: a supra-spinodal systemic insult latches a "
                               "self-sustaining inflammatory basin held by an accumulating cytokine tone (systemic "
                               "mirror of the T9 chronic latch), a FIXED counter-drive breaks it when applied EARLY "
                               "but FAILS when applied LATE (measured break-success falls monotonically with delay, "
                               "crossing a critical delay -- a narrow window), the time-criticality REQUIRES the "
                               "positive feedback (α=0 removes it), and trigger-removal alone is insufficient once "
                               "self-sustaining while an in-window basin-exit counter-drive collapses it; treatment "
                               "is direction/urgency-structure only and absolute scales stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T31"]["result"]
    print("SYSTEMIC INFLAMMATORY LATCH + BREAK WINDOW (cytokine-coupled population, primary=%s, γ=%.4f, spinodal=%.4f, "
          "α=%.2f, τ_M=%.1f, M_max=%.2f×sp, Nc=%d, D=%.3f):"
          % (r["primary"], r["gamma"], r["spinodal"], r["cytokine_gain_alpha"], r["cytokine_tau"],
             r["M_max_over_spinodal"], r["Nc"], r["noise_D"]))
    print("\n(1) SYSTEMIC LATCH IGNITION near the spinodal scale, organ by organ:")
    for o, row in r["systemic_latch_threshold"].items():
        print("     %-28s a_crit=%.3f×sp  near_spinodal=%s" % (o, row["a_crit_over_spinodal"], row["near_spinodal"]))
    ss = r["self_sustain"]
    print("     self-sustain: supra-insult frac after withdrawal=%.3f | sub-insult=%.3f -> self_sustains=%s"
          % (ss["frac_supra_after_withdraw"], ss["frac_sub_after_withdraw"], ss["self_sustains"]))
    bw = r["break_window"]
    print("\n(2) TIME-CRITICAL BREAK WINDOW (insult=%.2f×sp, counter=%.2f×sp, treat_dur=%d), t_crit_delay=%s:"
          % (bw["insult"], bw["counter"], bw["treat_dur"], bw["t_crit_delay"]))
    for d, ff, bs in zip(bw["delays"], bw["final_fraction"], bw["break_success"]):
        print("     delay=%4d  final_frac=%.3f  break_success=%.3f  %s" % (d, ff, bs, "#" * int(round(bs * 30))))
    print("     monotone decreasing=%s | early breaks=%s | late fails=%s -> window exists=%s"
          % (bw["monotone_decreasing"], bw["early_breaks"], bw["late_fails"], bw["window_exists"]))
    fc = r["feedback_control"]
    print("\n(3) TIME-CRITICALITY REQUIRES THE POSITIVE FEEDBACK (α=0 control):")
    print("     break_success(α=0) over delays:", fc["break_success_alpha0"])
    print("     range(α=0)=%.3f | range(α>0)=%.3f | α=0 breaks at all delays=%s -> requires feedback=%s"
          % (fc["range_alpha0"], fc["range_alpha_on"], fc["alpha0_breaks_at_all_delays"],
             fc["time_criticality_requires_feedback"]))
    td = r["treatment_direction"]
    print("\n(4) TITRATING THE TRIGGER IS INSUFFICIENT vs IN-WINDOW LATCH-BREAK:")
    print("     no treatment (trigger already removed) final frac=%.3f -> insufficient=%s"
          % (td["final_fraction_no_treatment"], td["trigger_removal_insufficient"]))
    print("     early in-window counter-drive final frac=%.3f -> break works=%s -> break early not titrate=%s"
          % (td["final_fraction_early_break"], td["in_window_break_works"], td["break_early_not_titrate"]))
    print("\nT31 all_pass:", r["all_pass"])
