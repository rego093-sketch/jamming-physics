#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_exhaustion.py  --  EMERGENT immune exhaustion (chronic-antigen hyporesponsiveness) as a MEASURED
accumulating negative feedback that drives a committed clone back across its NEGATIVE saddle-node, reversibly
(not asserted, not fitted).

WHY THIS EXISTS (v0.10.0). Affinity maturation (T18, emergent_maturation.py) MEASURED the PRODUCTIVE arc of an
adaptive response: rising affinity, commitment, a self-sustaining ON state. Exhaustion is the dynamical MIRROR --
the failure arc under CHRONIC antigen, where a committed response progressively loses function rather than clearing
the antigen. The textbook account is a cell-intrinsic negative-feedback programme (inhibitory-receptor tone that
accumulates with persistent stimulation and relaxes when antigen is withdrawn). The VP discipline is emergence:
whether such an accumulating feedback can extinguish a COMMITTED R19 response, whether it is reversible, and where
its onset sits relative to the switch's own bifurcations, must come OUT of the substrate dynamics, MEASURED.

This module drives a HETEROGENEOUS repertoire of N R19 cells (affinity spread desynchronises the population so it
relaxes onto a basin occupancy rather than a coherent oscillation) under a persistent antigen A, and couples in a
per-cell EXHAUSTION variable x ∈ [0,1] that ACCUMULATES (saturating) while a cell is ON AND antigen is present, and
DECAYS only when antigen is withdrawn:

    ds = (γ s − s³ + aff·A − κ·x) dt + sqrt(2 D dt)·ξ
    dx = ( 1{ON}·(1 − x)/τ_up ) dt      while antigen present
    dx = ( −x/τ_dn ) dt                  while antigen withdrawn

The exhaustion term −κ·x is a drive in the OPPOSITE direction. Because the committed cell sits in a bistable ON
basin, κ·x must grow large enough to push the cell past its NEGATIVE saddle-node before the ON state collapses --
so exhaustion, like activation, is gated by a saddle-node, just traversed in reverse. The module MEASURES the
responding fraction over time, withdraws/re-applies antigen to test reversibility, and sweeps κ to locate the
onset. Nothing about it is assumed.

WHAT EMERGES (measured, deterministic seed=19):
  1. CHRONIC ANTIGEN EXTINGUISHES THE RESPONSE (direction). Under persistent antigen the responding fraction rises
     to a peak (≈ 1) and then DECLINES MONOTONICALLY to a hyporesponsive floor (≈ 0) as exhaustion accumulates --
     a measured peak→floor collapse (drop ≈ 1.0), the dynamical opposite of the T18 productive latch.
  2. THE COLLAPSE NEEDS THE FEEDBACK (honest control). With the exhaustion coupling off (κ = 0) the same chronic
     drive holds the response UP indefinitely (measured floor ≈ 1, no collapse) -- the hyporesponsiveness is the
     accumulating feedback's doing, not antigen withdrawal or thermal decay.
  3. EXHAUSTION IS REVERSIBLE (antigen-withdrawal recovery). If antigen is WITHDRAWN partway (so x decays) and then
     the clone is RE-CHALLENGED, the responding fraction RECOVERS toward its peak (measured recovered ≈ 1) whereas
     a continuously-stimulated clone stays extinguished (≈ 0) -- the exhausted state is a reversible functional
     silencing tied to ongoing antigen, not an irreversible deletion (contrast T21).
  4. THE ONSET IS A REVERSE SADDLE-NODE. Sweeping the coupling κ, the exhausted (long-time) responding fraction is
     a monotone non-increasing function of κ that crosses below ½ at a measured onset κ near the closed-form
     reverse-saddle-node estimate sp·(aff_mean·drive + 1) -- below the onset the feedback cannot push the committed
     cell over its negative saddle-node and the response persists; above it the cell is forced OFF. Exhaustion is
     gated by the SAME bifurcation as commitment, traversed in reverse, MEASURED not posited.

GRADES (C3): the collapse DIRECTION, the feedback-required control, the antigen-withdrawal REVERSIBILITY, and the
reverse-saddle-node ONSET (monotone in κ, crossing near the closed form) are [V] emergent (measured from the coupled
stochastic repertoire with an accumulating feedback). The ABSOLUTE exhaustion rate / timing — set by τ_up, the
coupling κ, and the free cellular-noise scale D — is [O], no fabricated numbers. Determinism: fixed seed, BLAS
pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_PRIMARY = "lymphoid_adaptive"        # the adaptive compartment that exhausts under chronic antigen

# --- deterministic simulation size (fixed; heterogeneous repertoire desynchronises the FHN dynamics) ---
_N        = 220       # cells (heterogeneous affinity) per condition
_DT       = 0.02      # integration timestep
_D        = 0.02      # cellular-noise scale (absolute value is [O])
_TAU_UP   = 40.0      # exhaustion accumulation time (ON + antigen present)
_TAU_DN   = 40.0      # exhaustion recovery time (antigen withdrawn)
_SPREAD   = 0.4       # affinity spread (desynchronises the population)
_AFF_MEAN = 1.4       # mean affinity
_DRIVE    = 1.2       # antigen drive level (× spinodal)
_KAPPA    = 2.0       # reference exhaustion coupling (above the measured onset)
_T        = 300.0     # chronic-stimulation horizon
_NWIN     = 16        # trajectory windows

_KSWEEP   = (1.0, 1.5, 2.0, 2.5, 3.0)                 # coarse coupling sweep (collapse vs no-collapse)
_KFINE    = tuple(round(0.3 * k, 1) for k in range(4, 11))    # fine sweep 1.2 .. 3.0 for the onset crossing (coarsened)


def _simulate(g, drive_level, kappa, T, withdraw_at=None, rechallenge_at=None,
              D=_D, N=_N, dt=_DT, tau_up=_TAU_UP, tau_dn=_TAU_DN,
              aff_spread=_SPREAD, aff_mean=_AFF_MEAN, seed=SEED):
    """MEASURED responding-fraction time series for a heterogeneous R19 repertoire under antigen A=drive·spinodal,
    with a per-cell exhaustion variable x that accumulates (saturating, rate 1/tau_up) while the cell is ON AND
    antigen is present, and decays (rate 1/tau_dn) only when antigen is withdrawn; the feedback −kappa·x opposes
    the drive. Optional withdraw_at / rechallenge_at toggle the antigen for the reversibility test."""
    rng = np.random.default_rng(seed)
    aff = aff_mean + rng.uniform(-aff_spread / 2.0, aff_spread / 2.0, N)
    s = np.full(N, -math.sqrt(g)); x = np.zeros(N)
    sq = math.sqrt(2.0 * D * dt)
    nsteps = int(T / dt); A_on = drive_level * spinodal(g)
    ser = np.empty(nsteps)
    for i in range(nsteps):
        t = i * dt; A = A_on
        if withdraw_at is not None and t >= withdraw_at: A = 0.0
        if rechallenge_at is not None and t >= rechallenge_at: A = A_on
        on = (s > 0.0)
        s += (g * s - s ** 3 + aff * A - kappa * x) * dt + sq * rng.standard_normal(N)
        if A > 0.0:
            x += (on * (1.0 - x) / tau_up) * dt       # accumulate while ON + antigen (saturating)
        else:
            x += (-x / tau_dn) * dt                    # recover only when antigen withdrawn
        np.clip(s, -5.0, 5.0, out=s); np.clip(x, 0.0, 1.0, out=x)
        ser[i] = on.mean()
    return ser, dt


def _windows(ser, dt, T, nwin=_NWIN):
    step = T / nwin
    return [round(float(ser[int(k * step / dt):int((k + 1) * step / dt)].mean()), 3) for k in range(nwin)]


def _peak_floor(ser, dt, T):
    peak = float(ser[int(5.0 / dt):int(45.0 / dt)].max())              # early peak (post-commitment)
    floor = float(ser[int((T - 60.0) / dt):int(T / dt)].mean())        # late floor
    return peak, floor


def _mono_nonincreasing_from_peak(win, tol=0.03):
    pk = int(np.argmax(win)); seg = win[pk:]
    return all(seg[i + 1] <= seg[i] + tol for i in range(len(seg) - 1))


def _onset_kappa(g, drive_level, kappas, T, D=_D, seed=SEED):
    """Interpolate the coupling kappa at which the late (exhausted) responding fraction crosses 0.5 DOWNWARD."""
    floors = []
    for k in kappas:
        ser, dt = _simulate(g, drive_level, k, T, D=D, seed=seed)
        floors.append(float(ser[int((T - 60.0) / dt):int(T / dt)].mean()))
    if floors[0] < 0.5:
        return kappas[0], floors
    for i in range(1, len(floors)):
        if floors[i - 1] >= 0.5 > floors[i]:
            f = (floors[i - 1] - 0.5) / (floors[i - 1] - floors[i])
            return kappas[i - 1] + f * (kappas[i] - kappas[i - 1]), floors
    return kappas[-1], floors


def emergent_exhaustion(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # (1) CHRONIC COLLAPSE (direction): peak -> floor, monotone non-increasing from the peak
    ser, dt = _simulate(g_ref, _DRIVE, _KAPPA, _T, D=D)
    win = _windows(ser, dt, _T)
    peak, floor = _peak_floor(ser, dt, _T)
    drop = peak - floor
    collapse = bool(peak > 0.8 and floor < 0.2 and drop > 0.6 and _mono_nonincreasing_from_peak(win))

    # (2) ADAPTATION REQUIRED (control): kappa=0 -> stays up
    ser0, dt0 = _simulate(g_ref, _DRIVE, 0.0, _T, D=D)
    floor0 = float(ser0[int((_T - 60.0) / dt0):int(_T / dt0)].mean())
    feedback_required = bool(floor0 > 0.8 and (floor0 - floor) > 0.6)

    # (3) REVERSIBLE: withdraw t=180, rechallenge t=280 -> recovers; continued chronic stays extinguished
    serc, dtc = _simulate(g_ref, _DRIVE, _KAPPA, _T + 20.0, withdraw_at=180.0, rechallenge_at=280.0, D=D)
    rech_peak = float(serc[int(280.0 / dtc):int(330.0 / dtc)].max())     # peak right after re-challenge
    chronic_same = floor                                                  # continued-chronic late level
    reversible = bool(rech_peak > 0.6 and (rech_peak - chronic_same) > 0.5)

    # (4) ONSET == REVERSE SADDLE-NODE: monotone in kappa, crossing near sp*(aff_mean*drive+1)
    onset_k, fine_floors = _onset_kappa(g_ref, _DRIVE, _KFINE, _T, D=D)
    predicted = sp_ref * (_AFF_MEAN * _DRIVE + 1.0)
    onset_near = bool(abs(onset_k - predicted) < 0.5)
    coarse_floors = []
    for k in _KSWEEP:
        sk, dk = _simulate(g_ref, _DRIVE, k, _T, D=D)
        coarse_floors.append(round(float(sk[int((_T - 60.0) / dk):int(_T / dk)].mean()), 3))
    kappa_monotone = bool(all(coarse_floors[i] >= coarse_floors[i + 1] - 1e-9 for i in range(len(coarse_floors) - 1))
                          and coarse_floors[0] - coarse_floors[-1] > 0.6)

    ok = bool(collapse and feedback_required and reversible and onset_near and kappa_monotone)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6),
        noise_D=D, kappa_ref=_KAPPA, drive_over_spinodal=_DRIVE,
        aff_mean=_AFF_MEAN, aff_spread=_SPREAD, tau_up=_TAU_UP, tau_dn=_TAU_DN,
        trajectory=dict(windows=win, peak=round(peak, 3), floor=round(floor, 3), drop=round(drop, 3),
                        monotone_from_peak=bool(_mono_nonincreasing_from_peak(win)), collapses=bool(collapse)),
        control_kappa0=dict(floor=round(floor0, 3), feedback_required=bool(feedback_required)),
        reversibility=dict(rechallenge_peak=round(rech_peak, 3), continued_chronic=round(chronic_same, 3),
                           reversible=bool(reversible)),
        onset=dict(measured_kappa=round(onset_k, 3), predicted_reverse_saddle_node=round(predicted, 3),
                   near=bool(onset_near), coarse_sweep_floors=coarse_floors, kappa_monotone=bool(kappa_monotone)),
        all_pass=ok,
        grade="[V] immune exhaustion EMERGES from an accumulating per-cell negative feedback on a committed R19 "
              "repertoire under chronic antigen: the responding fraction collapses peak→floor (drop ≈ 1, monotone), "
              "the collapse needs the feedback (κ=0 stays up), it is REVERSIBLE on antigen withdrawal + re-challenge "
              "(recovers vs continued chronic stays extinguished -- functional silencing, not deletion), and its "
              "onset is a REVERSE SADDLE-NODE (exhausted fraction monotone in κ, crossing near sp·(aff_mean·drive+1) "
              "-- the feedback must push the committed cell over its negative saddle-node) -- measured, not assumed; "
              "[O] absolute exhaustion rate / timing (τ_up, κ, cellular-noise scale D)")


def run(gammas):
    """T25: emergent immune exhaustion -- an accumulating, antigen-gated negative feedback extinguishes a committed clone under chronic antigen MEASURED, reversibly on withdrawal, with onset at the switch's negative saddle-node (the dynamical mirror of T18 maturation)."""
    r = emergent_exhaustion(gammas)
    return dict(T25=dict(target="T25",
                         claim="immune exhaustion EMERGES as an accumulating, antigen-gated negative-feedback "
                               "variable on a committed R19 repertoire (the dynamical mirror of T18 maturation): "
                               "under chronic antigen the responding fraction rises then collapses to a "
                               "hyporesponsive floor (measured peak→floor, monotone), the collapse REQUIRES the "
                               "feedback (κ=0 holds the response up), it is REVERSIBLE -- antigen withdrawal lets "
                               "the feedback decay so a re-challenge recovers the response while continued "
                               "stimulation stays extinguished (functional silencing, not deletion) -- and its "
                               "onset is the switch's NEGATIVE saddle-node (exhausted fraction monotone in the "
                               "coupling, crossing near sp·(aff_mean·drive+1)) -- measured, not assumed; absolute "
                               "exhaustion rate stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T25"]["result"]
    print("IMMUNE EXHAUSTION under chronic antigen (primary=%s, γ=%.4f, spinodal=%.4f, D=%.3f, κ=%.1f, drive=%.1f×sp):"
          % (r["primary"], r["gamma"], r["spinodal"], r["noise_D"], r["kappa_ref"], r["drive_over_spinodal"]))
    t = r["trajectory"]
    print("\n(1) CHRONIC COLLAPSE (peak -> floor, monotone from peak):")
    print("     windows:", t["windows"])
    print("     peak=%.3f floor=%.3f drop=%.3f monotone=%s -> collapses=%s"
          % (t["peak"], t["floor"], t["drop"], t["monotone_from_peak"], t["collapses"]))
    c = r["control_kappa0"]
    print("\n(2) ADAPTATION REQUIRED (control κ=0):")
    print("     floor=%.3f -> feedback_required=%s" % (c["floor"], c["feedback_required"]))
    rev = r["reversibility"]
    print("\n(3) REVERSIBLE (withdraw t=180, rechallenge t=280):")
    print("     rechallenge_peak=%.3f vs continued_chronic=%.3f -> reversible=%s"
          % (rev["rechallenge_peak"], rev["continued_chronic"], rev["reversible"]))
    o = r["onset"]
    print("\n(4) ONSET == REVERSE SADDLE-NODE:")
    print("     measured onset κ=%.3f vs predicted sp·(aff_mean·drive+1)=%.3f -> near=%s"
          % (o["measured_kappa"], o["predicted_reverse_saddle_node"], o["near"]))
    print("     coarse κ-sweep floors=%s -> monotone (deeper κ => more complete exhaustion)=%s"
          % (o["coarse_sweep_floors"], o["kappa_monotone"]))
    print("\nT25 all_pass:", r["all_pass"])
