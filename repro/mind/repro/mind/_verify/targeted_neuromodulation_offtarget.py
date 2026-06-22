#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROMOD-E1 -- TARGETED NEUROMODULATION : CLEAN DELIVERY vs OFF-TARGET LEAK : the THIRD and
final region-specific application of the E1 spatial-localisation layer (§43), and the THERAPEUTIC
re-reading of the §44 excitatory map. §44 drove a region with a focal EXCITATORY bias and read it
as PATHOLOGY -- an ictal focus -- asking whether a seizure stays focal or secondarily generalises.
§45 silenced a region with a focal INHIBITORY bias and read a STROKE -- local deficit vs remote
diaschisis. THIS module drives a region with a focal EXCITATORY bias and reads it as THERAPY: a
targeted neuromodulation contact (a DBS lead, a TMS focus, a tDCS anode) placed at one region, and
asks the dual-USE clinical question that §44 could not pose because it was about avoiding spread,
not selecting a target: when you AIM stimulation at this region, does the effect stay AT the target
(CLEAN delivery -- the stimulation does what you intend, where you intend it) or does it LEAK to
off-target, connected circuits (OFF-TARGET LEAK -- current spread / co-recruitment beyond the
intended target, the structural picture of a neuromodulation side effect)? That question is
intrinsically SPATIAL -- it is about WHERE a focal drive lands -- and E1 (§43) named targeted
neuromodulation off-target as the THIRD owed application of its self/relay map. THIS module builds
it, closing the E1 region-specific application TRILOGY (containment/broadcast §44 ; local/diaschisis
§45 ; clean/leak §46). It IMPORTS the SpatialField class (it does NOT re-derive the ephaptic kernel
or the coupling map -- handover reuse discipline) and reads, on the frozen kernel, which targets
DELIVER CLEANLY and which LEAK off-target, and whether the cleanest-delivering targets must be the
weakest globally.
=================================================================================
THE GROUNDING (READ-ONLY; no new constant). A stimulation target is modelled -- exactly the §44
pattern -- as a strong focal EXCITATORY bias b0 > 0 at one region, the rest at baseline, through the
SAME k = kappa/(1-|b|) [excit] cap 2*kappa map as the SZ / epilepsy / E1 modules (no new constant).
Stimulating a RELAY site (E1.3) leaks off-target; stimulating a SELF-LOCALISING site delivers
cleanly -- a direct application of the E1.3 self/relay classification under an excitatory drive. The
stimulation INTENSITY b0 is SWEPT over the full E1 depth sweep {0.3,0.5,0.7,0.9}, inheriting §44's
full-sweep scope (unlike §45's inhibitory case, the excitatory partition holds at EVERY swept
intensity including the mildest, so no moderate-to-severe floor is needed); every SIGN/STRUCTURE
asserted below is required to hold at every swept intensity. CLEAN DELIVERY (vs leak) is read from
the E1 SpatialField footprint class (self vs relay), OFF-TARGET LEAK from the off-target vs own
local-coherence change, and GLOBAL THERAPEUTIC REACH from the §25-style global-order reach |R - R0|.
g = 1.0 is the engine's universal R19 scale; nothing here is fit.

HONESTY (the central no-overclaiming point). This module reads the SAME excitatory spatial map as
§44: the footprint classes, the reach map and the off-target ratios COINCIDE with §44's numbers --
the underlying physics is identical, because a focal excitatory drive is a focal excitatory drive.
What differs is the CLINICAL QUESTION: §44 asked whether a pathological excitation SPREADS (a
seizure-prognosis question, where spread is the bad outcome); §46 asks whether a THERAPEUTIC
stimulation stays ON-TARGET (a target-SELECTION question, where leak is the failure mode and clean
delivery the goal). The numbers are §44's; the reading -- target selection for neuromodulation, and
the decoupling of delivery focality from global reach -- is the new, distinct contribution, and it
is what closes the trilogy. We state the numerical overlap with §44 plainly rather than dressing it
up as a fresh measurement.

WHAT THE MODULE DELIVERS (pre-registered, sign/structure only; never magnitudes):
  N1  THE TARGET PARTITION (clean delivery vs off-target leak) IS DRIVE-INVARIANT, and the leak set
      is the E1.3 relay set. Aiming a focal excitatory stimulation at each region, the 12 targets
      partition into CLEAN-DELIVERY (self-localising -- the excitation concentrates at the target,
      the stimulation stays where it is aimed) and OFF-TARGET-LEAK (relay -- the excitation lands
      harder off-target, the stimulation bleeds to distal circuits). This binary partition is
      IDENTICAL across the FULL stimulation-intensity sweep {0.3,0.5,0.7,0.9}: the leak set is
      {hippocampus, midbrain} at every intensity, the other ten targets clean at every intensity,
      and the leak set is exactly the E1.3 RELAY set. Whether aiming at a region delivers cleanly or
      leaks off-target is a fixed property of target LOCATION, not of stimulation intensity. (Unlike
      §45's inhibitory case -- where a marginal node entered the set only at a mild sub-floor
      severity -- the excitatory partition is exactly stable at EVERY swept intensity including the
      mildest, inheriting §44's full-sweep scope; this is stated as the honest contrast with §45.)
      grade [V mech].
  N2  OFF-TARGET LEAK IS OFF-TARGET DOMINANCE (the structural content of leak). For a LEAK target the
      excitation lands HARDER on distal circuits than at the target itself: mean off-target |dc| >
      own |dc| (ratio > 1) -- the structural signature of stimulation spreading beyond the intended
      target (the hippocampus ~4.2x, the midbrain ~1.6x at the representative intensity). For a
      CLEAN target it concentrates at the target (ratio < 1 -- the cerebellum ~0.04x, an
      overwhelmingly focal delivery). The leak <-> (off/own > 1) equivalence holds at every swept
      intensity, tying "off-target leak" to its clinical meaning (current spread / co-recruitment).
      grade [V mech].
  N3  CLEAN DELIVERY AND GLOBAL THERAPEUTIC REACH ARE DECOUPLED -- TWO DISTINCT AXES (the honest no-
      tuning result). A clean, attractive hypothesis -- "to achieve a large GLOBAL (network-wide)
      therapeutic effect you must accept off-target leak; the targets with the largest global reach
      |R - R0| are exactly the leaky targets, and a clean target is necessarily a weak one" -- is
      tested and FOUND FALSE. The single largest global-reach target is the CEREBELLUM, a CLEAN
      (self-localising, off/own << 1, no leak) target, at EVERY stimulation intensity (it is the
      rank-1 reach target at every intensity, and -- inheriting §44, an HONEST contrast with §45
      whose inhibitory reach hub was NOT drive-invariant -- the reach hub here IS drive-invariant).
      A target can therefore achieve the LARGEST global effect while delivering maximally CLEANLY:
      delivery focality (clean vs leak) and global therapeutic reach are TWO DISTINCT, decoupled
      spatial properties, so a clinician need NOT trade delivery focality for global effect; the
      "focal = weak, leaky = strong" intuition is refuted. Moreover, even among the two LEAK targets
      the off-target effect is NOT a controllable point-to-point relay: the two leak targets push
      global coordination in OPPOSITE directions (the hippocampus LOWERS global R, the midbrain
      RAISES it, at every intensity), so "leak" is site-determined in both magnitude AND direction,
      not a single predictable spillover -- a relay target cannot be treated as a clean conduit to a
      chosen remote site. We do NOT force the tidy "focality = weak" story; the refuted clean
      hypothesis is reported honestly -- the E1.4 lesson made concrete for neuromodulation. grade
      [V mech] (a refuted clean hypothesis is a finding).
  N4  THE LEAK SET IS A COHERENT MINORITY RELAY-HUB CLASS (clean delivery is the structural default).
      The two leak targets {hippocampus, midbrain} are SIMULTANEOUSLY the E1.3 relay set AND the
      off-target-dominant set (N2), a STRICT MINORITY (2 of 12, so CLEAN DELIVERY is the structural
      default -- most targets deliver focally), AND decoupled from the global-reach hub (the clean
      cerebellum, N3) -- one coherent class of limbic/brainstem relay hubs. Structurally, off-target
      leak is the EXCEPTION carried by specific relay hubs, not a generic property of targets; this
      convergence holds across the intensity sweep. A DIRECTION-ONLY [L] correspondence is noted,
      never a magnitude or a prediction: clinically, off-target effects of focal neuromodulation
      (current spread beyond the intended target, DBS side effects from co-recruiting adjacent or
      connected structures, TMS spread to connected regions) are a recognised concern at specific
      connected hubs -- consistent with the leak set being a strict minority of relay hubs and clean
      delivery the structural majority. grade [V mech] structural + [L] cited correspondence.

NOT a claim that real neuromodulation off-target effects reduce to a phase-coupling footprint on a
frozen 1/r^3 kernel (real off-target spread is heterogeneous -- the actual electrode geometry,
tissue conductivity, white-matter tractography, the individual connectome, the specific montage /
contact configuration -- LOCKED); what is asserted is the SIGN/STRUCTURE of a focal excitatory bias
on the frozen kernel and its four consequences (the clean/leak partition, off-target dominance, the
decoupling of delivery focality from global reach, and the minority relay-hub class). NOT a claim
about the FELT effect of stimulation (Axis-A firewall: a clean/leak class is a STRUCTURAL spatial
property of the coupling model, NEVER a felt effect; consciousness_claim stays 0; hard problem stays
OPEN). NOT a real electric-field / current-density / lead-position / SAR map, a real connectome, or a
real off-target measurement; the per-node bias is not a real stimulation. NOT a prediction of WHICH
patient's stimulation will spread off-target or WHICH target is clinically optimal, and NOT clinical,
device-programming, or target-selection guidance -- DBS/TMS/tDCS target selection, lead placement and
programming are external clinical decisions made by clinicians with real data. NOT MEDICAL ADVICE;
efficacy = 0 everywhere; in-silico MECHANISM only; nothing here is a cure, a treatment, a
localisation, a device setting, or a prognosis. Every MAGNITUDE is [O]; only structural SIGNS and
RELATIONS are asserted, and they are certified to survive the stimulation-intensity sweep.

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY
(emerge_all is NOT touched, so the engine file stays e61083ae..., the tree stays 0fbf4988...
and the M0..M16 subtree stays 3a1ebbbb..., byte-identical). REUSES the E1 SpatialField
(imported, not re-derived); the stimulation is an EXCITATORY bias on the frozen kernel. Writes
targeted_neuromodulation_offtarget_results.json + its sha256, verified bit-for-bit.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

# REUSE the E1 spatial-localisation layer -- import the class and the shared (measured) handles;
# do NOT re-derive the ephaptic kernel or the coupling map (handover discipline: reuse).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e1_spatial_localisation import (SpatialField, REGS, N, DEPTHS, OMEGA, OMEGA0, KAP, W0, FOLD,
                                     M9_ANCHOR_R, ENGINE_TREE_FROZEN, M0_16_FROZEN)

HERE = os.path.dirname(os.path.abspath(__file__))

# Stimulation-intensity sweep = the E1 depth sweep in full -- inheriting §44's full-sweep scope
# (the excitatory partition holds at EVERY swept intensity, so no moderate-to-severe floor is
# needed; this is the honest contrast with §45's inhibitory case). Swept, NOT tuned.
STIM_DEPTHS = DEPTHS                  # {0.3, 0.5, 0.7, 0.9}
REP         = 0.7                     # representative stimulation intensity for headline reads [swept]
HIPPO = REGS.index("hippocampus")
MIDB  = REGS.index("midbrain")
CEREB = REGS.index("cerebellum")
EXPECTED_LEAK = sorted([REGS[HIPPO], REGS[MIDB]])   # the E1.3 relay set


def _footprint(sf, node, b0):
    """Own and mean-off-target |dc| for a focal excitatory (stimulation) bias at `node`, b0."""
    _, c = sf.focal(node, b0)
    dc = c - sf.c0
    own = float(abs(dc[node]))
    off = float(np.mean([abs(dc[j]) for j in range(N) if j != node]))
    return own, off


def _reach_rank(sf, node, b0):
    """1-indexed rank of `node` in the descending global-reach |R-R0| ranking at intensity b0."""
    rv = np.array([sf.reach(t, b0) for t in range(N)])
    order = list(np.argsort(rv)[::-1])
    return order.index(node) + 1


# ------------------------------- the four sub-studies + guard ----------------------------

def _partition(sf):
    """N1: the clean-delivery/off-target-leak partition over the FULL stimulation-intensity sweep.
    The partition is drive-invariant; the leak (relay) set is fixed and equals the E1.3 relay set.
    Unlike §45's inhibitory case the partition is exactly stable at every swept intensity including
    the mildest, so no sub-floor caveat is needed (the honest contrast with §45)."""
    vectors = {}
    for b0 in STIM_DEPTHS:
        vectors[round(b0, 2)] = [sf.footprint_class(t, b0) for t in range(N)]
    base = vectors[round(STIM_DEPTHS[0], 2)]
    invariant = bool(all(v == base for v in vectors.values()))
    leak = sorted([REGS[k] for k in range(N) if base[k] < 0])
    clean = sorted([REGS[k] for k in range(N) if base[k] > 0])
    leak_is_relay_set = bool(leak == EXPECTED_LEAK)
    labelled = {round(b0, 2): {REGS[t]: ("leak" if vectors[round(b0, 2)][t] < 0 else "clean")
                               for t in range(N)} for b0 in STIM_DEPTHS}
    # honest contrast with §45: the partition holds at the MILDEST swept intensity too (no marginal
    # node enters at the floor -- the excitatory case has no sub-floor caveat).
    mild_classes = [sf.footprint_class(t, STIM_DEPTHS[0]) for t in range(N)]
    mild_leak = sorted([REGS[k] for k in range(N) if mild_classes[k] < 0])
    stable_at_mildest = bool(mild_leak == EXPECTED_LEAK)
    return (invariant, leak, clean, leak_is_relay_set, labelled, mild_leak, stable_at_mildest)


def _off_target_dominance(sf):
    """N2: off-target leak <-> (mean off-target |dc| > own |dc|), at every swept intensity."""
    per_site = {}
    equivalence_all = True
    for b0 in STIM_DEPTHS:
        for t in range(N):
            own, off = _footprint(sf, t, b0)
            is_leak = bool(off > own)
            want_leak = bool(t in (HIPPO, MIDB))
            if is_leak != want_leak:
                equivalence_all = False
            if round(b0, 2) == REP:
                per_site[REGS[t]] = {"own_abs_dc": round(own, 6),
                                     "off_target_abs_dc": round(off, 6),
                                     "off_over_own": round(off / own, 4) if own > 0 else None,
                                     "off_target_dominant_leak": is_leak}
    return bool(equivalence_all), per_site


def _clean_vs_reach_decoupled(sf):
    """N3 (honest negative): clean delivery and global therapeutic reach are DECOUPLED. (a) the
    single largest global-reach target is the CLEAN cerebellum at every intensity, and the reach
    hub IS drive-invariant (inheriting §44, the honest contrast with §45); (b) the two LEAK targets
    push global R in OPPOSITE directions at every intensity. The clean 'clean = weak / leak = strong
    reach' hypothesis is FALSE -- a target can be maximally clean AND maximally globally reaching;
    two distinct, decoupled spatial axes."""
    reach_hub_clean_all = True
    top_reach_is_clean_all = True
    cereb_top_reach_all = True
    clean_hypothesis_refuted = False      # refuted if the top-reach target is NOT in the leak set
    reach_hub_per_intensity = {}
    reach_dump = {}
    for b0 in STIM_DEPTHS:
        rv = np.array([sf.reach(t, b0) for t in range(N)])
        top = int(np.argmax(rv))
        reach_hub_per_intensity[round(b0, 2)] = REGS[top]
        # the top-reach target must be CLEAN (self-localising), NOT in the leak set
        if sf.footprint_class(top, b0) <= 0:
            top_reach_is_clean_all = False
        if top not in (HIPPO, MIDB):
            clean_hypothesis_refuted = True   # a CLEAN target tops global reach
        if top != CEREB:
            cereb_top_reach_all = False
        # the reach hub (cerebellum) is clean at this intensity
        if sf.footprint_class(CEREB, b0) <= 0:
            reach_hub_clean_all = False
        own_c, off_c = _footprint(sf, CEREB, b0)
        reach_dump[round(b0, 2)] = {"top_reach_target": REGS[top],
                                    "top_reach": round(float(rv[top]), 6),
                                    "cerebellum_reach": round(float(rv[CEREB]), 6),
                                    "cerebellum_reach_rank": _reach_rank(sf, CEREB, b0),
                                    "cerebellum_is_clean": bool(sf.footprint_class(CEREB, b0) > 0),
                                    "cerebellum_off_over_own": round(off_c / own_c, 4) if own_c > 0 else None}
    # the reach hub IS drive-invariant (honest contrast with §45, which had it flip)
    reach_hub_drive_invariant = bool(len(set(reach_hub_per_intensity.values())) == 1)

    # (b) the two leak targets push global R in OPPOSITE directions at every intensity
    opposite_sign_all = True
    direction_dump = {}
    for b0 in STIM_DEPTHS:
        Rh, _ = sf.focal(HIPPO, b0)
        Rm, _ = sf.focal(MIDB, b0)
        dh = float(Rh - sf.R0)
        dm = float(Rm - sf.R0)
        ok = bool(dm > 0 and dh < 0)        # midbrain raises global R, hippocampus lowers it
        if not ok:
            opposite_sign_all = False
        direction_dump[round(b0, 2)] = {"midbrain_dR": round(dm, 6), "midbrain_raises_R": bool(dm > 0),
                                        "hippocampus_dR": round(dh, 6), "hippocampus_lowers_R": bool(dh < 0)}

    clean_target_maxes_reach = bool(reach_hub_clean_all and top_reach_is_clean_all
                                    and cereb_top_reach_all and clean_hypothesis_refuted)
    leak_not_point_to_point = bool(opposite_sign_all)
    decoupled = bool(clean_target_maxes_reach and leak_not_point_to_point)
    return (decoupled, reach_hub_clean_all, top_reach_is_clean_all, cereb_top_reach_all,
            clean_hypothesis_refuted, reach_hub_drive_invariant, leak_not_point_to_point,
            reach_hub_per_intensity, reach_dump, direction_dump)


def _minority_hub_class(sf):
    """N4: the leak set is a coherent minority relay-hub class -- the E1.3 relay set AND the
    off-target-dominant set (N2), a strict minority (clean delivery the default), decoupled from the
    global-reach hub. Convergence holds across the intensity sweep."""
    invariant, leak, clean, is_relay_set, _, _, _ = _partition(sf)
    n_leak = len(leak)
    is_minority = bool(n_leak < N - n_leak)        # leak is the strict minority
    clean_is_default = bool(len(clean) > n_leak)
    # the leak set is the off-target-dominant set (N2 equivalence) at the representative intensity
    od_set = sorted([REGS[t] for t in range(N) if _footprint(sf, t, REP)[1] > _footprint(sf, t, REP)[0]])
    leak_eq_off_target = bool(od_set == leak)
    # decoupled from the global-reach hub: the top global-reach target (cerebellum) is CLEAN, NOT in
    # the leak set -- the N3 decoupling
    decoupled_from_reach_hub = bool(REGS[CEREB] not in leak
                                    and int(np.argmax([sf.reach(t, REP) for t in range(N)])) not in (HIPPO, MIDB))
    coherent_class = bool(is_relay_set and leak_eq_off_target and is_minority
                          and clean_is_default and decoupled_from_reach_hub)
    return (coherent_class, leak, n_leak, is_minority, clean_is_default,
            decoupled_from_reach_hub, leak_eq_off_target)


def _invariance(sf):
    """S5: a zero stimulation (no target driven) reproduces the frozen M9 anchor R bit-for-bit and
    the per-node field equals the baseline exactly -- the neuromodulation reads are a pure structural
    read on the frozen kernel (no new mechanism/measurement/constant)."""
    R_direct = E._integrate(OMEGA, W0, KAP * OMEGA0)[0]          # frozen M9 anchor (engine)
    Rb, cb = sf.drive(np.zeros(N))                               # zero stimulation (off-state)
    matches_anchor = bool(R_direct == M9_ANCHOR_R)
    offstate_matches = bool(Rb == R_direct)
    field_matches = bool(np.array_equal(cb, sf.c0))
    baseline_matches = bool(sf.R0 == M9_ANCHOR_R)
    return R_direct, Rb, matches_anchor, offstate_matches, field_matches, baseline_matches


def run():
    sf = SpatialField()

    # ===== N1 : the clean-delivery/off-target-leak partition, drive-invariant =====
    (part_inv, leak, clean, is_relay_set, part_labelled,
     mild_leak, stable_at_mildest) = _partition(sf)
    N1 = bool(part_inv and is_relay_set)

    # ===== N2 : off-target leak = off-target dominance =====
    od_equiv, od_per_site = _off_target_dominance(sf)
    N2 = bool(od_equiv)

    # ===== N3 : clean delivery != global reach (honest negative, decoupled axes) =====
    (decoupled, reach_hub_clean_all, top_reach_clean_all, cereb_top_all,
     clean_refuted, reach_hub_invariant, leak_not_p2p,
     reach_hub_per_int, reach_dump, direction_dump) = _clean_vs_reach_decoupled(sf)
    N3 = bool(decoupled)

    # ===== N4 : the leak set is a coherent minority relay-hub class =====
    (coherent, l4, n_l, is_min, clean_default, disjoint, l_eq_od) = _minority_hub_class(sf)
    N4 = bool(coherent)

    # ===== S5 : engine-invariance guard =====
    Rinv, Roff, anchor_ok, off_ok, field_ok, base_ok = _invariance(sf)
    S5 = bool(anchor_ok and off_ok and field_ok and base_ok)

    preds = {
        "N1_target_partition_drive_invariant":  "CONFIRMED" if N1 else "REFUTED",
        "N2_leak_is_off_target_dominance":      "CONFIRMED" if N2 else "REFUTED",
        "N3_clean_delivery_reach_decoupled":    "CONFIRMED" if N3 else "REFUTED",
        "N4_leak_minority_relay_hub_class":     "CONFIRMED" if N4 else "REFUTED",
    }

    res = {
        "_what": "NEUROMOD-E1 -- targeted neuromodulation: clean delivery vs off-target leak. The "
                 "THIRD and final region-specific application of the E1 spatial-localisation layer "
                 "(§43), closing the E1 region-specific application TRILOGY (containment/broadcast "
                 "§44 ; local/diaschisis §45 ; clean/leak §46), and the THERAPEUTIC re-reading of the "
                 "§44 excitatory map. §44 drove a region with a focal EXCITATORY bias and read it as "
                 "PATHOLOGY (a seizure focus -- does it stay focal or generalise?); this module drives "
                 "a region with a focal EXCITATORY bias and reads it as THERAPY -- a targeted "
                 "neuromodulation contact (DBS/TMS/tDCS) at one region -- and asks the target-SELECTION "
                 "question: does the stimulation DELIVER CLEANLY (stay at the target) or LEAK off-"
                 "target (bleed to connected circuits)? HONESTLY, the underlying numbers COINCIDE with "
                 "§44's (a focal excitatory drive is a focal excitatory drive); what differs is the "
                 "clinical reading -- target selection, and the decoupling of delivery focality from "
                 "global reach -- and that reading is what closes the trilogy. This module IMPORTS the "
                 "E1 SpatialField (it does NOT re-derive the kernel or coupling map). Four sign-only "
                 "results: N1 the clean-delivery/off-target-leak partition is drive-invariant over the "
                 "FULL intensity sweep (the leak set {hippocampus, midbrain} = the E1.3 relay set, "
                 "fixed at every intensity including the mildest -- whether a target delivers cleanly "
                 "or leaks is a property of target LOCATION; no sub-floor caveat, the honest contrast "
                 "with §45); N2 off-target leak is off-target dominance (the excitation lands harder on "
                 "distal circuits than at the target -- the structural content of current spread / co-"
                 "recruitment); N3 (honest negative) clean delivery and global therapeutic reach are "
                 "DECOUPLED (the largest global-reach target is the CLEAN cerebellum at every intensity "
                 "and the reach hub IS drive-invariant, inheriting §44; so a clinician need not trade "
                 "delivery focality for global effect, and even among leak targets the spillover is "
                 "site-determined in direction -- two distinct decoupled axes, the E1.4 lesson for "
                 "neuromodulation); N4 the leak set is a coherent minority relay-hub class (clean "
                 "delivery is the structural default, off-target leak the exception carried by specific "
                 "relay hubs). MECHANISM only -- a clean/leak class is a STRUCTURAL spatial quantity, "
                 "NOT a felt effect, NOT a real field/current-density/lead-position map, NOT a clinical "
                 "prediction of which targets leak or which is optimal, and NOT device-programming or "
                 "target-selection guidance. efficacy=0; not medical advice.",
        "roadmap_id": "E1 region-specific application #3 (targeted neuromodulation off-target), the "
                      "third and FINAL application of the E1.3 self/relay map named owed by §43, "
                      "closing the trilogy (containment/broadcast §44, local/diaschisis §45, clean/leak "
                      "§46); RESEARCH_ROADMAP_post_autism_adhd.md",
        "application_of_E1": {
            "E1_supplied": "the E1.3 SELF-LOCALISING vs RELAY classification (drive-invariant, relay "
                           "set {hippocampus, midbrain}) and the E1.2 heterogeneous global reach with "
                           "a drive-stable cerebellar hub -- a fixed spatial MAP of the frozen kernel, "
                           "here READ under an EXCITATORY (stimulation) bias as a target-selection map",
            "this_module_reads": "which targets DELIVER CLEANLY (stay at the target) and which LEAK "
                                 "off-target, and tests whether the cleanest-delivering targets must be "
                                 "the weakest globally -- it finds they need NOT be (N3), so delivery "
                                 "focality and global reach are decoupled, exactly the region-specific "
                                 "reading E1.4 demanded",
            "reuse_discipline": "imports SpatialField; does NOT re-derive the ephaptic kernel W0 or the "
                                "k(b) coupling map; the stimulation is an EXCITATORY bias on the frozen "
                                "kernel; engine emerged READ-ONLY, byte-unchanged",
            "trilogy_closed": "the THIRD and FINAL E1 region-specific application. §44 drove the map "
                              "with a focal EXCITATORY bias as PATHOLOGY (containment vs broadcast); §45 "
                              "with a focal INHIBITORY bias as a STROKE (local deficit vs remote "
                              "diaschisis); §46 with a focal EXCITATORY bias as THERAPY (clean delivery "
                              "vs off-target leak) -- the E1 application trilogy is now closed",
            "honest_overlap_with_sec44": "this module reads the SAME excitatory spatial map as §44 -- "
                                         "the footprint classes, reach map and off-target ratios COINCIDE "
                                         "with §44's numbers, stated plainly. What is new is the THERAPEUTIC "
                                         "SELECTION reading (clean delivery as the goal, leak as the failure "
                                         "mode) and the N3 decoupling of delivery focality from global "
                                         "reach -- a target-selection finding §44 (about avoiding spread) "
                                         "never posed; not dressed up as a fresh measurement",
        },
        "stimulation_model": {
            "form": "a targeted stimulation = a strong focal EXCITATORY bias b0>0 at one region (the "
                    "rest at baseline), via the SAME k = kappa/(1-|b|) [excit] cap 2*kappa map as the "
                    "SZ/epilepsy/E1 modules (no new constant) -- the §44 pattern; stimulating a RELAY "
                    "site leaks off-target, stimulating a SELF-LOCALISING site delivers cleanly; "
                    "stimulation intensity b0 swept over {0.3,0.5,0.7,0.9} (the full E1 sweep)",
            "form_grade": "[F] forced -- the frozen ephaptic kernel W0 plus the existing k(b) map; no "
                          "free constant; a zero stimulation reproduces the scalar engine bit-for-bit",
            "stimulation_intensity_sweep": list(STIM_DEPTHS),
            "representative_intensity": REP,
            "profile_grade": "[O] swept -- the stimulation intensity is a SWEEP, not a tuned constant; "
                             "every SIGN/STRUCTURE holds across the full intensity sweep",
            "excitatory_bias_not_deletion": "the stimulation is an EXCITATORY bias on the frozen kernel "
                                            "(the §44 pattern), never a node deletion -- the SpatialField "
                                            "is reused intact",
            "reused_constants": {"kappa_measured": round(KAP, 6), "R19_fold_spinodal": round(FOLD, 6),
                                 "n_regions": N, "baseline_R0_M9_anchor": round(sf.R0, 10)},
        },
        "N1_target_partition": {
            "partition_drive_invariant": part_inv,
            "leak_set": leak,
            "leak_set_is_E1_relay_set": is_relay_set,
            "clean_set": clean,
            "partition_per_intensity": part_labelled,
            "leak_set_at_mildest_intensity": mild_leak,
            "stable_at_mildest_no_subfloor_caveat": stable_at_mildest,
            "reproduced": N1,
            "reading": "aiming a focal excitatory stimulation at each region, the 12 targets partition "
                       "into CLEAN-DELIVERY (self-localising -- the excitation concentrates at the "
                       "target, the stimulation stays where it is aimed) and OFF-TARGET-LEAK (relay -- "
                       "the excitation lands harder off-target, the stimulation bleeds to distal "
                       "circuits). The partition is IDENTICAL across the FULL stimulation-intensity "
                       "sweep, the leak set {hippocampus, midbrain} fixed at every intensity and equal "
                       "to the E1.3 relay set. Whether aiming at a region delivers cleanly or leaks "
                       "off-target is a fixed property of target LOCATION, not of stimulation "
                       "intensity. Unlike §45's inhibitory case (where a marginal node entered only at "
                       "a mild sub-floor severity), the excitatory partition is exactly stable at "
                       "EVERY swept intensity including the mildest -- inheriting §44's full-sweep "
                       "scope, the honest contrast with §45. Inherits the E1.3 self/relay class read "
                       "on an excitatory bias; structure-only.",
        },
        "N2_off_target_leak": {
            "leak_iff_off_target_dominant_all_intensities": od_equiv,
            "per_site_at_representative_intensity": od_per_site,
            "reproduced": N2,
            "reading": "for a LEAK target the excitation lands HARDER on distal circuits than at the "
                       "target itself (mean off-target |dc| > own |dc|, ratio > 1 -- the hippocampus "
                       "~4.2x, the midbrain ~1.6x at the representative intensity) -- the structural "
                       "signature of stimulation spreading beyond the intended target (current spread "
                       "/ co-recruitment); for a CLEAN target it concentrates at the target (ratio < 1 "
                       "-- the cerebellum ~0.04x, an overwhelmingly focal delivery). The leak <-> "
                       "(off/own > 1) equivalence holds at every swept intensity, tying 'off-target "
                       "leak' to its clinical meaning. Sign-only; magnitudes [O].",
        },
        "N3_clean_delivery_reach_decoupled": {
            "_what": "the honest no-tuning result -- a clean hypothesis ('to get a large GLOBAL "
                     "therapeutic effect you must accept off-target leak; a clean target is "
                     "necessarily a weak one') tested and FOUND FALSE",
            "clean_target_maxes_global_reach": bool(reach_hub_clean_all and top_reach_clean_all
                                                    and cereb_top_all and clean_refuted),
            "top_reach_target_is_clean_all_intensities": top_reach_clean_all,
            "cerebellum_is_top_reach_all_intensities": cereb_top_all,
            "reach_hub_is_clean_all_intensities": reach_hub_clean_all,
            "clean_hypothesis_refuted": clean_refuted,
            "reach_hub_drive_invariant": reach_hub_invariant,
            "global_reach_hub_per_intensity": reach_hub_per_int,
            "reach_per_intensity": reach_dump,
            "leak_targets_push_R_opposite_directions_all": leak_not_p2p,
            "leak_direction_per_intensity": direction_dump,
            "two_axes_decoupled": decoupled,
            "reproduced": N3,
            "verdict": "the cleanest-delivering targets need NOT be the weakest globally: the single "
                       "largest global-reach target is the CEREBELLUM, a CLEAN (self-localising, "
                       "off/own << 1, no leak) target, at EVERY stimulation intensity (rank-1 at every "
                       "intensity, and the reach hub IS drive-invariant -- inheriting §44, an honest "
                       "contrast with §45 whose inhibitory reach hub was NOT drive-invariant). A "
                       "target can achieve the LARGEST global effect while delivering maximally "
                       "CLEANLY -- so delivery focality (clean vs leak) and global therapeutic reach "
                       "are TWO DISTINCT, decoupled spatial properties, and a clinician need not trade "
                       "delivery focality for global effect; the 'focal = weak, leaky = strong' "
                       "intuition is refuted. Moreover, even among the two LEAK targets the off-target "
                       "effect is NOT a controllable point-to-point relay: the two leak targets push "
                       "global coordination in OPPOSITE directions (the hippocampus LOWERS global R, "
                       "the midbrain RAISES it, at every intensity), so leak is site-determined in "
                       "both magnitude AND direction, not a single predictable spillover -- a relay "
                       "target cannot be treated as a clean conduit to a chosen remote site. The "
                       "refuted clean hypothesis is reported honestly -- the E1.4 lesson made concrete "
                       "for neuromodulation. A refuted clean hypothesis is a finding.",
        },
        "N4_leak_minority_relay_hub_class": {
            "leak_set": l4,
            "n_leak": n_l,
            "leak_is_strict_minority": is_min,
            "clean_delivery_is_structural_default": clean_default,
            "leak_equals_off_target_dominant_set": l_eq_od,
            "decoupled_from_global_reach_hub": disjoint,
            "coherent_minority_relay_hub_class": coherent,
            "reproduced": N4,
            "clinical_correspondence_grade": "[L] direction-only",
            "clinical_correspondence": "a DIRECTION-ONLY cited correspondence, never a magnitude or a "
                                       "prediction: clinically, off-target effects of focal "
                                       "neuromodulation (current spread beyond the intended target, "
                                       "DBS side effects from co-recruiting adjacent or connected "
                                       "structures, TMS spread to connected regions) are a recognised "
                                       "concern at specific connected hubs -- consistent with the leak "
                                       "set being a strict minority of relay hubs and clean delivery "
                                       "the structural majority. NOT a patient-level prediction.",
            "reading": "the two leak targets {hippocampus, midbrain} are simultaneously the E1.3 relay "
                       "set AND the off-target-dominant set (N2), a STRICT MINORITY (2 of 12 -- clean "
                       "delivery is the structural default), AND decoupled from the global-reach hub "
                       "(the clean cerebellum, N3) -- one coherent class of limbic/brainstem relay "
                       "hubs. Off-target leak is structurally the EXCEPTION carried by specific relay "
                       "hubs, not a generic property of targets. Structure-only; the clinical "
                       "correspondence is [L] direction-only.",
        },
        "S5_engine_invariance_guard": {
            "_what": "a zero stimulation (no target driven) reproduces the frozen M9 coordination "
                     "anchor bit-for-bit and the per-node field equals the baseline exactly -- the "
                     "neuromodulation reads are a pure structural read on the frozen kernel (no new "
                     "mechanism)",
            "R_direct_measured": repr(Rinv),
            "frozen_M9_anchor": repr(M9_ANCHOR_R),
            "matches_frozen_anchor_bitwise": anchor_ok,
            "offstate_R": repr(Roff),
            "offstate_matches_direct_bitwise": off_ok,
            "offstate_field_equals_baseline": field_ok,
            "baseline_equals_anchor": base_ok,
            "guard": S5,
        },
        "cited_and_locked": {
            "spatial_layer_cited": "the E1 spatial-localisation layer (§43) supplies the SpatialField "
                "class, the self/relay classification (E1.3) and the heterogeneous global reach (E1.2); "
                "this module shapes a focal EXCITATORY (stimulation) bias on the frozen kernel, it does "
                "not re-derive it",
            "excitatory_sibling_cited": "§44 (the first E1 application) drove the SAME focal EXCITATORY "
                "bias and read it as a seizure focus (containment vs broadcast); §46 reads the same "
                "excitatory map as THERAPY (clean delivery vs off-target leak) -- the numbers coincide, "
                "the target-selection reading is the new contribution",
            "lesion_dual_cited": "§45 (the second E1 application) silenced a region with a focal "
                "INHIBITORY bias and read a stroke (local deficit vs remote diaschisis); §46 is the "
                "THIRD application, completing the trilogy, and inherits §44's drive-invariant reach "
                "hub -- the honest contrast with §45, whose inhibitory reach hub was NOT drive-invariant",
            "partition_is_position_LOCK": "whether a target delivers cleanly or leaks off-target is a "
                "fixed property of target LOCATION (the E1.3 relay class), drive-invariant over the "
                "full intensity sweep -- structure, not a fitted result",
            "no_focality_strength_tradeoff_LOCK": "clean delivery is NOT in tension with global reach; "
                "the clean 'clean = weak / leak = strong' hypothesis is explicitly refuted, not forced "
                "-- the largest-reach target is clean and delivery focality is decoupled from global "
                "reach (the E1.4 lesson for neuromodulation)",
            "full_sweep_scope_LOCK": "the excitatory partition holds at every swept intensity including "
                "the mildest (no moderate-to-severe floor needed), inheriting §44's full-sweep scope -- "
                "the honest contrast with §45's inhibitory sub-floor caveat",
            "real_neuromodulation_heterogeneous_LOCK": "real neuromodulation off-target effects are "
                "HETEROGENEOUS (the electrode geometry, tissue conductivity, white-matter tractography, "
                "the individual connectome, the specific montage/contact configuration); this module "
                "asserts the SIGN/STRUCTURE of a focal excitatory bias on the FROZEN kernel, not that "
                "any real stimulation follows it",
            "not_clinical_LOCK": "nothing here is a real electric field, a current-density/SAR map, a "
                "lead-position map, a real connectome, an off-target measurement, a prediction of which "
                "patient's stimulation leaks or which target is optimal, or device-programming/target-"
                "selection guidance; target selection and programming are external clinical decisions",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; whether any "
                "real stimulation delivers cleanly or leaks by this structure is external",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "spatial_quantities_are_structural": 1.0,
            "reuses_E1_spatial_field": 1.0,
            "stimulation_is_excitatory_bias_not_deletion": 1.0,
            "stimulation_intensity": "OPEN [O] -- swept; signs/structure hold over the full "
                                     "stimulation-intensity sweep, not tuned",
            "shares_excitatory_map_with_sec44": "STATED PLAINLY -- the footprint classes, reach map and "
                                                "off-target ratios COINCIDE with §44's numbers (a focal "
                                                "excitatory drive is a focal excitatory drive); what is "
                                                "new is the THERAPEUTIC target-selection reading and the "
                                                "N3 decoupling, not dressed up as a fresh measurement",
            "reach_hub_drive_invariant_inherits_sec44": "the excitatory reach hub IS drive-invariant "
                                                        "(cerebellum at every intensity), inheriting "
                                                        "§44 -- the honest contrast with §45's inhibitory "
                                                        "reach hub, which was NOT drive-invariant",
            "clean_hypothesis_refuted": "N3 reports a REFUTED clean hypothesis honestly (clean delivery "
                                        "and global reach are decoupled, the cleanest target need not "
                                        "be the weakest) rather than forcing a 'focality = weak' story",
            "completes_E1_trilogy": 1.0,
            "clinical_prediction": "NONE -- no patient-level prediction of which target leaks, no "
                                   "localisation, no device setting, no claim of clinical optimality; "
                                   "the only clinical correspondence (N4) is [L] direction-only",
            "not_medical_advice": 1.0,
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "m9_anchor_reproduced_bitwise": anchor_ok,
        },
        "preregistered_results": {
            "N1_target_partition_drive_invariant": {
                "claim": "aiming a focal excitatory stimulation at each region, the clean-delivery/off-"
                         "target-leak partition is identical across the full stimulation-intensity "
                         "sweep and the leak (relay) set is {hippocampus, midbrain} = the E1.3 relay "
                         "set at every intensity including the mildest",
                "status": preds["N1_target_partition_drive_invariant"]},
            "N2_leak_is_off_target_dominance": {
                "claim": "a target leaks off-target IFF its excitation lands harder off-target than at "
                         "the target (mean off-target |dc| > own |dc|), at every swept intensity",
                "status": preds["N2_leak_is_off_target_dominance"]},
            "N3_clean_delivery_reach_decoupled": {
                "claim": "clean delivery and global therapeutic reach are decoupled: the largest "
                         "global-reach target is the CLEAN cerebellum (rank-1 at every intensity, the "
                         "reach hub drive-invariant), so a clean target need not be a weak one; the "
                         "clean 'clean = weak / leak = strong' hypothesis is refuted, and the two leak "
                         "targets push global R in opposite directions",
                "status": preds["N3_clean_delivery_reach_decoupled"]},
            "N4_leak_minority_relay_hub_class": {
                "claim": "the leak set is the E1.3 relay set AND the off-target-dominant set, a strict "
                         "minority (clean delivery the default), decoupled from the global-reach hub -- "
                         "one coherent minority relay-hub class",
                "status": preds["N4_leak_minority_relay_hub_class"]},
        },
        "overall": {
            "target_partition_drive_invariant": N1,
            "leak_is_off_target_dominance": N2,
            "clean_delivery_reach_decoupled": N3,
            "leak_minority_relay_hub_class": N4,
            "engine_invariance_guard": S5,
            "is_full_module": bool(N1 and N2 and N3 and N4 and S5),
            "verdict": "targeted neuromodulation -- clean delivery vs off-target leak -- the third and "
                       "final region-specific application of the E1 spatial-localisation layer, "
                       "closing the trilogy (containment/broadcast §44, local/diaschisis §45, "
                       "clean/leak §46) and the THERAPEUTIC re-reading of the §44 excitatory map. "
                       "Aiming a focal excitatory stimulation at each region (the §44 pattern, read "
                       "now as therapy not pathology), the clean-delivery/off-target-leak partition is "
                       "DRIVE-INVARIANT over the full intensity sweep, the leak set {hippocampus, "
                       "midbrain} = the E1.3 relay set, fixed at every intensity including the mildest "
                       "(N1; no sub-floor caveat, the honest contrast with §45); off-target leak IS "
                       "off-target dominance, the structural content of current spread / co-recruitment "
                       "(N2); clean delivery and global therapeutic reach are DECOUPLED -- the largest "
                       "global-reach target is the CLEAN cerebellum (rank-1 at every intensity, the "
                       "reach hub drive-invariant, inheriting §44), so a clinician need not trade "
                       "delivery focality for global effect, and the leak spillover is site-determined "
                       "in direction (N3, the honest no-tuning result, the E1.4 lesson for "
                       "neuromodulation); and the leak set is a coherent minority relay-hub class, "
                       "clean delivery the structural default (N4). HONESTLY, the numbers coincide with "
                       "§44's (a focal excitatory drive is a focal excitatory drive); what is new is "
                       "the target-selection reading and the N3 decoupling. A zero stimulation "
                       "reproduces the frozen M9 anchor bit-for-bit (S5). The stimulation form is "
                       "forced, the intensity swept, every sign survives the sweep, no new tuned "
                       "constant, engine byte-unchanged; the SpatialField is imported, not re-derived, "
                       "and the stimulation is an excitatory bias, never a node deletion. Axis-A "
                       "firewall: a clean/leak class is a structural spatial quantity, NOT a felt "
                       "effect, NOT a real field/current-density/lead-position map, NOT a prediction of "
                       "which targets leak or which is optimal, NOT device-programming or target-"
                       "selection guidance. efficacy=0; not medical advice.",
        },
    }
    return res


def _canon(o):
    if isinstance(o, float):
        return round(o, 10)
    if isinstance(o, dict):
        return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_canon(v) for v in o]
    return o

def _blob(res):
    return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def targeted_neuromodulation_offtarget_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "targeted_neuromodulation_offtarget_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_targeted_neuromodulation_offtarget_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"targeted_neuromodulation_offtarget_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = targeted_neuromodulation_offtarget_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    m = res["stimulation_model"]
    n1 = res["N1_target_partition"]; n2 = res["N2_off_target_leak"]
    n3 = res["N3_clean_delivery_reach_decoupled"]; n4 = res["N4_leak_minority_relay_hub_class"]
    g = res["S5_engine_invariance_guard"]
    print("=" * 78)
    print("NEUROMOD-E1 -- TARGETED NEUROMODULATION: CLEAN DELIVERY vs OFF-TARGET LEAK (E1 application #3)")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  stimulation model: focal excitatory bias (not deletion); intensity sweep={m['stimulation_intensity_sweep']}  form={m['form_grade'][:18]}")
    print("-" * 78)
    print(f"  N1 partition     : drive-invariant={n1['partition_drive_invariant']}  leak(relay) set={n1['leak_set']}  (stable at mildest, no sub-floor={n1['stable_at_mildest_no_subfloor_caveat']})")
    print(f"  N2 off-target    : leak<->off>own (all intensities)={n2['leak_iff_off_target_dominant_all_intensities']}")
    print(f"  N3 decoupled     : clean cerebellum top-reach all={n3['top_reach_target_is_clean_all_intensities']}  clean-hyp refuted={n3['clean_hypothesis_refuted']}  reach-hub drive-invariant={n3['reach_hub_drive_invariant']}  leak dirs opposite={n3['leak_targets_push_R_opposite_directions_all']}  -> decoupled={n3['two_axes_decoupled']}")
    print(f"  N4 minority hub  : leak={n4['leak_set']} n={n4['n_leak']}  minority={n4['leak_is_strict_minority']}  decoupled-from-reach-hub={n4['decoupled_from_global_reach_hub']}  -> coherent={n4['coherent_minority_relay_hub_class']}")
    print(f"  S5 invariance    : off-state R={g['offstate_R']}  ==anchor:{g['matches_frozen_anchor_bitwise'] and g['offstate_matches_direct_bitwise']}  field==baseline:{g['offstate_field_equals_baseline']}")
    print("-" * 78)
    print(f"  reach hub per intensity: {n3['global_reach_hub_per_intensity']}")
    print(f"  pre-registered: {[ (k, v['status']) for k,v in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  NEUROMODULATION OFF-TARGET SPATIAL MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
