#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_immunosenescence.py  --  EMERGENT thymic involution / immunosenescence as a MEASURED coupling between a
shrinking thymic-education window and TWO drifting repertoire outputs (not asserted, not fitted).

WHY THIS EXISTS (v0.14.0). T21 (emergent_negative_selection.py) educates a repertoire with a spread of
self-affinities under the R19 saddle-node: a thymocyte that crosses ON within the education window receives the
apoptotic deletion signal (negative selection), an exported clone that never reaches the positive-selection
signal dies by neglect, and a clone that is positively selected but not deleted is EXPORTED as a naive cell.
T21 runs that education at a FIXED window. Thymic involution is the same education run with a SLOWLY SHRINKING
window: as the thymic epithelial niche ages, every thymocyte has less time to complete its selection program.
The VP discipline is emergence -- what an ageing window does to the repertoire must come OUT of the substrate
dynamics, MEASURED, never assumed. This module runs the T21 education over a descending window sweep and measures
the two outputs that drift with age, on the SAME R19 field (thymus = FOXN1 gamma), each gated by a CROSSING that
takes time:

    a thymocyte with self-affinity a_self is educated under self-drive h = a_self * spinodal with noise:
        ds = (gamma s - s^3 + h) dt + sqrt(2 D dt) . xi
    POSITIVE SELECTION (survival): it must accumulate enough self-MHC engagement -- cumulative dwell above a low
        signalling threshold s_pos -- within the window, else it DIES BY NEGLECT (kinetic-signalling model).
    NEGATIVE SELECTION (deletion): if it crosses ON (s>0) within the window it is DELETED (strong self-reactivity).
    EXPORTED = positively selected (engaged >= tau_pos) AND not deleted.

Both selection events are first-passage / accumulation events with a finite time cost, so a SHORTER window
truncates them. The two truncations push the repertoire in OPPOSITE directions, and both are MEASURED:

WHAT EMERGES (measured, deterministic seed=19):
  1. ESCAPED-AUTOREACTIVE FRACTION RISES AS THE WINDOW SHRINKS. A supra-spinodal (self-reactive, should-be-
     deleted) clone needs time to cross ON. With less education time the near-threshold supra clones do not reach
     ON in time, ESCAPE deletion, and are exported as autoreactive. The measured escaped-autoreactive fraction
     rises monotonically as the window shrinks -- the negative-selection failure of an ageing thymus.
  2. NAIVE-EXPORT RATE FALLS AS THE WINDOW SHRINKS. Positive selection (survival) needs accumulated engagement.
     With less time, marginal thymocytes fail to accumulate the survival signal and DIE BY NEGLECT, so the
     measured healthy naive-export rate falls monotonically as the window shrinks -- the falling thymic output of
     an ageing thymus.
  3. THE TWO DIVERGE (repertoire drift). Escape rises while output falls over the same shrinking window: an older
     thymus exports FEWER naive cells AND lets MORE autoreactive clones slip through -- the dynamical face of
     ageing repertoire drift, measured as a single coupled divergence, not two assumptions.
  4. THE YOUNG THYMUS IS CLEAN AND PRODUCTIVE (honest control). At the longest (young) window the measured
     escaped-autoreactive fraction is ~0 and the naive-export rate is at its maximum -- so the drift is an
     ageing effect of the shrinking window, not a baseline artefact.
  5. ESCAPE IS NEAR-THRESHOLD. The escaped clones are concentrated just above the spinodal (the longest
     deletion-crossing times), so it is precisely T21's near-threshold escaped sliver that an ageing window
     widens -- the same autoimmune seed (T23) growing with age.

GRADES (C3): the escape-rises / output-falls directions, their divergence, the young-clean control, and the
near-threshold concentration are [V] emergent (measured by simulation). The ABSOLUTE timescale -- the window
length in real units, the positive-selection engagement quota tau_pos, the signalling threshold s_pos, and the
free cellular-noise scale D (the same D as T7/T8/T21) -- is [O], no fabricated ageing-rate numbers.
Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]   # ascending-gamma
_PRIMARY = "thymus"   # the canonical involution site (FOXN1: T-cell positive/negative selection)

# --- deterministic simulation size (fixed; no per-window tuning) ---------------------------------------
_N        = 1400     # thymocytes per window condition (uniform self-affinity spread)
_DT       = 0.01     # Langevin timestep
_D        = 0.02     # cellular-noise scale (absolute value is [O])
_AFF_LO   = 0.20     # lowest self-affinity in the cohort (x spinodal)
_AFF_HI   = 1.40     # highest self-affinity in the cohort (x spinodal)
_S_POS_FR = 0.83     # positive-selection signalling threshold s_pos = -S_POS_FR * sqrt(gamma) (in the OFF basin)
_TAU_POS  = 5.0      # cumulative engagement (dwell above s_pos) required to survive death-by-neglect; [O]
# the involution / age axis: a DESCENDING thymic-education window (young -> old). Absolute units are [O];
# only the direction of the two outputs vs the window is the claim.
_WINDOWS  = (24.0, 18.0, 14.0, 11.0, 8.0)   # education window lengths (descending = ageing)


def educate(g, T_edu, D=_D, N=_N, dt=_DT, aff_lo=_AFF_LO, aff_hi=_AFF_HI,
            s_pos_fr=_S_POS_FR, tau_pos=_TAU_POS, seed=SEED):
    """Educate a cohort with a UNIFORM self-affinity spread for a window T_edu; MEASURE the exported repertoire.
    Returns the escaped-autoreactive fraction, the healthy naive-export fraction, the neglected fraction, and the
    mean self-affinity of the escaped (autoreactive) clones."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    aff = rng.uniform(aff_lo, aff_hi, N)                 # self-affinities (x spinodal)
    h = aff * sp
    s = np.full(N, -math.sqrt(g))                        # naive thymocytes start in the OFF basin
    s_pos = -s_pos_fr * math.sqrt(g)                     # low positive-selection signalling threshold
    engaged = np.zeros(N)                                # cumulative self-MHC engagement (dwell above s_pos)
    deleted = np.zeros(N, dtype=bool)                    # crossed ON -> negative selection (apoptosis)
    sq = math.sqrt(2.0 * D * dt)
    for _ in range(int(T_edu / dt)):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        engaged += (s > s_pos) * dt
        deleted |= (s > 0.0)
    pos_selected = engaged >= tau_pos                    # accumulated the survival signal (else death by neglect)
    exported = pos_selected & (~deleted)                 # positively selected and not deleted
    above = aff >= 1.0                                   # supra-spinodal: self-reactive, should be deleted
    escaped = exported & above                           # supra clone that escaped deletion -> exported autoreactive
    naive_healthy = exported & (~above)                  # sub-spinodal positively-selected export (healthy naive)
    neglected = ~pos_selected
    esc_aff = aff[escaped]
    return dict(window=round(T_edu, 4),
                escaped_autoreactive_fraction=round(float(escaped.mean()), 4),
                naive_export_rate=round(float(naive_healthy.mean()), 4),
                total_export_rate=round(float(exported.mean()), 4),
                neglected_fraction=round(float(neglected.mean()), 4),
                deleted_fraction=round(float(deleted.mean()), 4),
                escaped_mean_self_affinity=round(float(esc_aff.mean()), 4) if esc_aff.size else None)


def _monotone_up(xs):     # rises as the window shrinks (xs already ordered young->old)
    return all(xs[i + 1] >= xs[i] - 1e-9 for i in range(len(xs) - 1))

def _monotone_down(xs):   # falls as the window shrinks
    return all(xs[i + 1] <= xs[i] + 1e-9 for i in range(len(xs) - 1))


def emergent_immunosenescence(gammas, D=_D):
    g = gammas[_PRIMARY]; sp = spinodal(g)
    sweep = [educate(g, T, D=D) for T in _WINDOWS]               # young -> old (descending window)

    esc = [r["escaped_autoreactive_fraction"] for r in sweep]
    nai = [r["naive_export_rate"] for r in sweep]

    escaped_rises = _monotone_up(esc)
    naive_falls   = _monotone_down(nai)
    # divergence: escape clearly grows and output clearly shrinks from young to old
    diverges = bool(esc[-1] - esc[0] > 0.03 and nai[0] - nai[-1] > 0.03)
    # young-clean control: at the youngest (longest) window escape ~0 and export at its max
    young_clean = bool(esc[0] < 0.02 and abs(nai[0] - max(nai)) < 1e-9)
    # escape is near-threshold: escaped clones sit just above the spinodal (smallest at the oldest window)
    esc_affs = [r["escaped_mean_self_affinity"] for r in sweep if r["escaped_mean_self_affinity"] is not None]
    near_threshold = bool(len(esc_affs) > 0 and min(esc_affs) <= 1.15)

    ok = bool(escaped_rises and naive_falls and diverges and young_clean and near_threshold)
    return dict(
        primary_organ=_PRIMARY, gamma=round(g, 6), spinodal=round(sp, 6),
        noise_D=D, s_pos_fraction=_S_POS_FR, tau_pos=_TAU_POS,
        aff_lo=_AFF_LO, aff_hi=_AFF_HI, windows=list(_WINDOWS),
        window_sweep=sweep,
        escaped_autoreactive_rises_as_window_shrinks=bool(escaped_rises),
        naive_export_falls_as_window_shrinks=bool(naive_falls),
        outputs_diverge_with_age=bool(diverges),
        young_window_clean_and_productive=bool(young_clean),
        escape_is_near_threshold=bool(near_threshold),
        escaped_young=esc[0], escaped_old=esc[-1],
        naive_young=nai[0], naive_old=nai[-1],
        all_pass=ok,
        grade="[V] thymic involution / immunosenescence EMERGES from the T21 education run over a shrinking window: "
              "both selection events are time-costed crossings, so a shorter window truncates them in OPPOSITE "
              "directions -- the escaped-autoreactive fraction RISES (near-threshold supra clones miss deletion) "
              "while the healthy naive-export rate FALLS (marginal clones miss positive selection and die by "
              "neglect), the two diverge as the dynamical face of ageing repertoire drift, the youngest window is "
              "clean and productive (control), and the escapees are near-threshold (T21's sliver widened) -- "
              "measured, not asserted; [O] absolute timescale / engagement quota / noise scale D")


def run(gammas):
    """T34: emergent immunosenescence / thymic involution -- escaped-autoreactive rise and naive-export fall MEASURED from the T21 education run over a shrinking window, not asserted."""
    r = emergent_immunosenescence(gammas)
    return dict(T34=dict(target="T34",
                         claim="thymic involution / immunosenescence EMERGES from the T21 thymic education run with "
                               "a SLOWLY SHRINKING education window: positive selection (survival) and negative "
                               "selection (deletion) are both time-costed crossings of the one R19 field, so a "
                               "shorter (older) window truncates them in OPPOSITE directions -- near-threshold "
                               "supra-spinodal clones miss deletion so the escaped-autoreactive fraction RISES, "
                               "while marginal clones miss the positive-selection engagement quota and die by "
                               "neglect so the healthy naive-export rate FALLS; the two outputs diverge (ageing "
                               "repertoire drift), the youngest window is clean and productive, and the escapees "
                               "are near-threshold (T21's escaped sliver widened by age) -- measured, not asserted; "
                               "absolute timescale / engagement quota / noise scale D stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T34"]["result"]
    print("IMMUNOSENESCENCE / thymic involution (PRIMARY = %s, gamma=%.4f, spinodal=%.4f):"
          % (r["primary_organ"], r["gamma"], r["spinodal"]))
    print("  shrinking education window (young -> old):")
    print("    window   escaped-autoreactive   naive-export   total-export   neglected   deleted   esc-mean-aff")
    for row in r["window_sweep"]:
        print("    %5.1f         %.4f             %.4f         %.4f        %.4f      %.4f      %s"
              % (row["window"], row["escaped_autoreactive_fraction"], row["naive_export_rate"],
                 row["total_export_rate"], row["neglected_fraction"], row["deleted_fraction"],
                 ("%.4f" % row["escaped_mean_self_affinity"]) if row["escaped_mean_self_affinity"] is not None else "  -  "))
    print("  escaped rises as window shrinks: %s  (young %.4f -> old %.4f)"
          % (r["escaped_autoreactive_rises_as_window_shrinks"], r["escaped_young"], r["escaped_old"]))
    print("  naive export falls as window shrinks: %s  (young %.4f -> old %.4f)"
          % (r["naive_export_falls_as_window_shrinks"], r["naive_young"], r["naive_old"]))
    print("  outputs diverge with age: %s | young clean & productive: %s | escape near-threshold: %s"
          % (r["outputs_diverge_with_age"], r["young_window_clean_and_productive"], r["escape_is_near_threshold"]))
    print("\nT34 all_pass:", r["all_pass"])
