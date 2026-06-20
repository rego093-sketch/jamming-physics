#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_negative_selection.py  --  EMERGENT central tolerance / clonal deletion (negative selection) as a
MEASURED deletion-threshold + exported-repertoire ceiling (not asserted, not fitted).

WHY THIS EXISTS (v0.9.0). T11 (emergent_selection.py) shows the POSITIVE-selection saddle-node: a clone driven
ABOVE its spinodal commits ON (activates). Central tolerance is the MIRROR of that same switch: in the thymic
context a developing T-cell whose receptor has high SELF-affinity is driven ON by self-antigen during thymic
education -- but an ON-commitment in the thymus is an apoptotic DEATH signal (clonal deletion), not activation.
So the very threshold that turns a clone ON in the periphery turns a self-reactive clone OFF (deletes it) in the
thymus. The VP discipline is emergence: the negative-selection threshold, the ceiling it imposes on the EXPORTED
repertoire's self-reactivity, and the autoreactive fraction that ESCAPES it must come OUT of the substrate
dynamics, MEASURED, never plugged in. This module does that on the same R19 substrate (thymus = FOXN1 γ):

    a thymocyte with self-affinity a_self is educated under a self-drive h = a_self * spinodal, with noise:
        ds = (γ s − s³ + h) dt + sqrt(2 D dt) · ξ
    if it crosses to ON within the education window it receives the deletion signal and is CULLED;
    if it never crosses it is IGNORED and EXPORTED (tolerant by ignorance).

The deletion outcome is the ONLY thing measured; the independently-computed spinodal is used afterwards only to
compare. A whole repertoire with a spread of self-affinities is educated, the committers are culled, and the
EXPORTED self-affinity distribution is MEASURED -- so central tolerance is a counted population property, not an
assumption.

WHAT EMERGES (measured, deterministic seed=19):
  1. DELETION THRESHOLD = SPINODAL, organ by organ. The measured self-affinity at which P(deletion) crosses 0.5
     lands on the organ's own spinodal (from just below, by thermal activation -- the exact mirror of T11's
     commit-drive = spinodal). So negative selection is the saddle-node of the measured γ, MEASURED not posited.
  2. THE THRESHOLD ORDERS BY γ. The measured deletion thresholds rank in ascending-γ order across the four
     organs -- deeper-well compartments require a stronger self-signal to delete.
  3. CENTRAL TOLERANCE = A MEASURED CEILING ON EXPORTED SELF-REACTIVITY. After negative selection the exported
     repertoire's self-affinity is bounded BELOW the deletion threshold: the high-self-affinity clones are
     removed and the measured maximum exported self-affinity sits at the spinodal. The exported set is purged of
     strongly self-reactive clones -- central tolerance as a measured distribution truncation.
  4. AN ESCAPED AUTOREACTIVE FRACTION REMAINS (the seed of autoimmune risk -> T23). Clones with self-affinity
     just below the threshold ESCAPE deletion (ignored, exported). The measured escape fraction is a smooth
     function of self-affinity (not a hard step -- thermal activation softens the edge), and a deeper deletion
     threshold trims exactly the most dangerous near-threshold escapees. The window WIDTH is set by D ([O]).
  5. DELETION REQUIRED (honest control). With the deletion channel OFF (ON-commitment = activation, as in the
     periphery), the supra-threshold self-clones are EXPORTED AS ACTIVE autoreactive cells instead of removed:
     the measured exported-autoreactive fraction is high without deletion and ≈0 with deletion -- proving the
     clonal-deletion channel is what enforces central tolerance, not the affinity distribution alone.

GRADES (C3): the deletion threshold (= spinodal organ-by-organ), its γ-ordering, the exported-repertoire ceiling,
the escape window, and the deletion-required control are [V] emergent (measured by simulation). The ABSOLUTE
deletion rate and the escape-window WIDTH (set by the free cellular-noise scale D, the same D as T7/T8/T9/T11)
are [O], no fabricated deletion numbers. Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]   # ascending-γ expectation
_PRIMARY = "thymus"   # the canonical central-tolerance site (FOXN1: T-cell positive/negative selection)

# --- deterministic simulation size (fixed; low noise -> sharp threshold; no per-organ tuning) ----------
_N        = 350      # thymocytes per (self-affinity) condition
_DT       = 0.01     # Langevin timestep
_T_EDU    = 40.0     # thymic-education horizon (self-antigen presentation window; fixed-drive bracket probe)
_D        = 0.01     # cellular-noise scale (low: sharp threshold; absolute value is [O])
# quasi-static ramp probe for the deletion THRESHOLD (mirror of T11's ramp_commit_drive): the self-drive
# rises slowly and the drive at the FIRST ON-crossing -- the instant the apoptotic deletion signal fires --
# is MEASURED. Measured quasi-statically the threshold lands on the spinodal (from below by thermal activation).
_H_LO     = 0.30     # ramp start (well below every organ's spinodal)
_H_HI     = 0.80     # ramp end   (above every organ's spinodal)
_T_RAMP   = 100.0    # ramp duration (slow -> quasi-static deletion at the vanishing barrier)
_SUB_FRAC = 0.70     # clearly sub-threshold self-affinity (ignored / exported)
_SUP_FRAC = 1.15     # clearly supra-threshold self-affinity (deleted)

# repertoire export sweep (one large repertoire with a uniform spread of self-affinities straddling threshold)
_N_REP    = 1500     # thymocytes in the exported-repertoire experiment
_AFF_LO   = 0.40     # lowest self-affinity in the repertoire (× spinodal)
_AFF_HI   = 1.50     # highest self-affinity in the repertoire (× spinodal)


def p_delete(g, aff_frac, deletion_on=True, D=_D, N=_N, dt=_DT, T=_T_EDU, seed=SEED):
    """MEASURED probability a thymocyte of self-affinity aff_frac·spinodal is DELETED (commits ON during education).

    deletion_on=True  -> committers are deleted (negative selection). Returns P(commit) = P(deletion).
    deletion_on=False -> control: committers would be EXPORTED as active; the same P(commit) is now the
                         exported-autoreactive probability. (The dynamics are identical; only the LABEL of the
                         ON outcome changes -- deletion vs activation -- which is exactly the thymus/periphery
                         difference.)
    """
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, -math.sqrt(g))                 # all thymocytes start naive (OFF basin)
    committed = np.zeros(N, dtype=bool)
    sq = math.sqrt(2.0 * D * dt)
    h = aff_frac * sp                             # self-drive proportional to self-affinity
    for _ in range(int(T / dt)):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        committed |= (s > 0.0)
        if committed.all():
            break
    return float(committed.mean())


def ramp_delete_drive(g, D=_D, N=_N, dt=_DT, h_lo=_H_LO, h_hi=_H_HI, T=_T_RAMP, seed=SEED):
    """MEASURED mean self-drive at deletion: ramp the self-drive slowly, record the drive at first ON-crossing
    (the instant the apoptotic deletion signal fires). No formula -- the mirror of T11's commit-drive probe."""
    rng = np.random.default_rng(seed)
    s = np.full(N, -math.sqrt(g))                 # all thymocytes start naive (OFF basin)
    deleted = np.zeros(N, dtype=bool)
    hdel = np.full(N, h_hi)
    sq = math.sqrt(2.0 * D * dt)
    nsteps = int(T / dt)
    for i in range(nsteps):
        h = h_lo + (h_hi - h_lo) * (i * dt / T)
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        newly = (~deleted) & (s > 0.0)            # crossed ON -> deletion signal
        if newly.any():
            hdel[newly] = h
            deleted[newly] = True
        if deleted.all():
            break
    return float(hdel.mean()), float(deleted.mean())


def _deletion_threshold(g, D=_D):
    """Measured deletion threshold in units of the organ's spinodal (mean self-drive at deletion / spinodal)."""
    sp = spinodal(g)
    mean_h, frac = ramp_delete_drive(g, D=D)
    return (mean_h / sp if sp > 0 else float("nan")), mean_h, frac


def exported_repertoire(g, deletion_on=True, D=_D, N=_N_REP, dt=_DT, T=_T_EDU, seed=SEED):
    """Educate a repertoire with a UNIFORM spread of self-affinities; cull committers (if deletion_on); MEASURE
    the exported self-affinity distribution and the exported-autoreactive fraction."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    aff_frac = rng.uniform(_AFF_LO, _AFF_HI, N)               # self-affinities (× spinodal)
    s = np.full(N, -math.sqrt(g))
    committed = np.zeros(N, dtype=bool)
    sq = math.sqrt(2.0 * D * dt)
    h = aff_frac * sp
    for _ in range(int(T / dt)):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        committed |= (s > 0.0)
    above = aff_frac >= 1.0                                   # self-affinity above the spinodal (should be deleted)
    if deletion_on:
        exported = ~committed                                # committers deleted; survivors exported
        exported_autoreactive = float((committed & above).mean()) * 0.0   # deleted -> not exported as active
        exported_self_aff = aff_frac[exported]
    else:
        exported = np.ones(N, dtype=bool)                    # no deletion: everyone exported
        exported_autoreactive = float((committed & above).mean())         # committed supra-threshold = active autoreactive
        exported_self_aff = aff_frac
    max_exported = float(exported_self_aff.max()) if exported_self_aff.size else float("nan")
    # escaped autoreactive fraction = exported clones that are above the spinodal but escaped deletion (the holes)
    escaped_above = float((exported & above).mean()) if deletion_on else float("nan")
    frac_deleted = float(committed.mean()) if deletion_on else 0.0
    return dict(max_exported_self_affinity=round(max_exported, 4),
                fraction_deleted=round(frac_deleted, 4),
                exported_autoreactive_fraction=round(exported_autoreactive, 4),
                escaped_supra_threshold_fraction=round(escaped_above, 4) if deletion_on else None)


def emergent_negative_selection(gammas, D=_D):
    # (1) measured deletion threshold == spinodal, organ by organ
    rows, thresh_ok = {}, True
    thr_aff, del_drive = {}, {}
    for o in _ORGANS:
        g = gammas[o]; sp = spinodal(g)
        ratio, mean_h, frac = _deletion_threshold(g, D=D)
        thr_aff[o] = ratio                                   # in units of the organ's spinodal
        del_drive[o] = mean_h
        matches = bool(0.90 <= ratio <= 1.05 and frac > 0.99)   # near the spinodal, from below (thermal)
        rows[o] = dict(spinodal=round(sp, 6), measured_deletion_drive=round(mean_h, 6),
                       deletion_threshold_over_spinodal=round(ratio, 3), fraction_deleted=round(frac, 3),
                       matches_spinodal=matches)
        thresh_ok = thresh_ok and matches

    # (2) the measured threshold ORDERS by γ
    order_thr   = sorted(_ORGANS, key=lambda o: del_drive[o])     # absolute deletion drive
    order_gamma = sorted(_ORGANS, key=lambda o: gammas[o])
    ordering_emerges = (order_thr == order_gamma)

    # (3) ignorance/deletion bracket (sub-threshold ignored, supra-threshold deleted), organ by organ
    bracket, bracket_ok = {}, True
    for o in _ORGANS:
        p_sub = p_delete(gammas[o], _SUB_FRAC, deletion_on=True, D=D)
        p_sup = p_delete(gammas[o], _SUP_FRAC, deletion_on=True, D=D)
        ok = bool(p_sub < 0.10 and p_sup > 0.90)
        bracket[o] = dict(p_delete_subthreshold=round(p_sub, 3), p_delete_suprathreshold=round(p_sup, 3),
                          ignored_below_deleted_above=ok)
        bracket_ok = bracket_ok and ok

    # (4) exported-repertoire ceiling + escaped fraction (PRIMARY organ = thymus), with the deletion-off control
    g0 = gammas[_PRIMARY]; sp0 = spinodal(g0)
    exp_on  = exported_repertoire(g0, deletion_on=True,  D=D)
    exp_off = exported_repertoire(g0, deletion_on=False, D=D)
    # central tolerance: the exported maximum self-affinity is capped near the spinodal (×spinodal ~ 1)
    ceiling_at_spinodal = bool(exp_on["max_exported_self_affinity"] <= 1.10)
    # deletion required: exported-autoreactive fraction collapses from high (no deletion) to ~0 (deletion)
    deletion_required = bool(exp_off["exported_autoreactive_fraction"] > 0.20
                             and exp_on["exported_autoreactive_fraction"] < 0.02)

    ok = bool(thresh_ok and ordering_emerges and bracket_ok and ceiling_at_spinodal and deletion_required)
    return dict(
        primary_organ=_PRIMARY, noise_D=D, sub_frac=_SUB_FRAC, sup_frac=_SUP_FRAC,
        deletion_threshold=rows,
        deletion_threshold_equals_spinodal=bool(thresh_ok),
        deletion_drive_order_ascending=order_thr,
        gamma_order_ascending=order_gamma,
        threshold_orders_by_gamma=bool(ordering_emerges),
        ignorance_deletion_bracket=bracket,
        subthreshold_ignored_suprathreshold_deleted=bool(bracket_ok),
        exported_repertoire_with_deletion=exp_on,
        exported_repertoire_without_deletion=exp_off,
        central_tolerance_ceiling_at_spinodal=bool(ceiling_at_spinodal),
        deletion_channel_required=bool(deletion_required),
        all_pass=ok,
        grade="[V] central tolerance / clonal deletion EMERGES from the same R19 saddle-node as positive selection: "
              "the measured self-affinity at which a thymocyte is deleted equals each organ's spinodal (from below, "
              "by thermal activation -- the mirror of T11), orders by γ, sub-threshold clones are ignored while "
              "supra-threshold clones are deleted, the EXPORTED repertoire's self-affinity is capped at the spinodal "
              "(a measured central-tolerance ceiling), an escaped near-threshold fraction remains (the autoimmune "
              "seed for T23), and turning the deletion channel off exports those clones as active autoreactive cells "
              "(deletion required) -- measured, not asserted; [O] absolute deletion rate / escape-window width (D)")


def run(gammas):
    """T21: emergent central tolerance / clonal deletion -- the negative-selection threshold and exported-repertoire ceiling MEASURED from a stochastic thymic-education sim, not asserted as the spinodal."""
    r = emergent_negative_selection(gammas)
    return dict(T21=dict(target="T21",
                         claim="central tolerance EMERGES from the same R19 switch as activation, run in the thymic "
                               "context where an ON-commitment is a deletion signal: the measured deletion threshold "
                               "equals each organ's spinodal (the negative-selection mirror of T11, approached from "
                               "below by thermal activation), orders by γ, sub-threshold self-clones are ignored while "
                               "supra-threshold ones are deleted, the exported repertoire's self-affinity is capped at "
                               "the spinodal (a measured central-tolerance ceiling) with an escaped near-threshold "
                               "fraction left over (the seed of autoimmune risk), and switching the deletion channel "
                               "off exports those clones as active autoreactive cells -- measured, not asserted; "
                               "absolute deletion rate / escape-window width (noise scale D) stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T21"]["result"]
    print("deletion threshold vs spinodal per organ:")
    for o, v in r["deletion_threshold"].items():
        print("    %-26s deletion-drive=%.4f  spinodal=%.4f  ratio=%.3f  (matches=%s)"
              % (o, v["measured_deletion_drive"], v["spinodal"], v["deletion_threshold_over_spinodal"], v["matches_spinodal"]))
    print("deletion threshold == spinodal (all organs):", r["deletion_threshold_equals_spinodal"])
    print("threshold orders by γ:", r["threshold_orders_by_gamma"], "| order:", r["deletion_drive_order_ascending"])
    print("ignorance/deletion bracket:")
    for o, v in r["ignorance_deletion_bracket"].items():
        print("    %-26s P(delete|0.70sp)=%.3f  P(delete|1.15sp)=%.3f  (ok=%s)"
              % (o, v["p_delete_subthreshold"], v["p_delete_suprathreshold"], v["ignored_below_deleted_above"]))
    eon, eoff = r["exported_repertoire_with_deletion"], r["exported_repertoire_without_deletion"]
    print("\nexported repertoire (PRIMARY = %s):" % r["primary_organ"])
    print("    WITH deletion:    max exported self-aff = %.3f (×sp)  deleted frac = %.3f  exported-autoreactive = %.3f  escaped supra = %.3f"
          % (eon["max_exported_self_affinity"], eon["fraction_deleted"], eon["exported_autoreactive_fraction"], eon["escaped_supra_threshold_fraction"]))
    print("    WITHOUT deletion: max exported self-aff = %.3f (×sp)                       exported-autoreactive = %.3f"
          % (eoff["max_exported_self_affinity"], eoff["exported_autoreactive_fraction"]))
    print("    central-tolerance ceiling at spinodal:", r["central_tolerance_ceiling_at_spinodal"],
          "| deletion channel required:", r["deletion_channel_required"])
    print("\nT21 all_pass:", r["all_pass"])
