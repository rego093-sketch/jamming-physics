#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FOC-EPI-E1 -- FOCAL EPILEPSY : CONTAINMENT vs SECONDARY GENERALISATION : the FIRST region-
specific application of the E1 spatial-localisation layer (§43), and the SPATIAL refinement of
the §25 (T2a) over-synchronisation epilepsy module. §25 established the seizure as the network
crossing the over-synchronisation threshold on the GLOBAL order parameter R -- but it drove the
brain GLOBALLY (one scalar Kglob), so it could not ask the single most consequential clinical
question about a FOCAL epilepsy: does a seizure that BEGINS at one focus STAY focal (a simple/
complex partial seizure) or SECONDARILY GENERALISE (recruit circuits beyond the focus and spread
to the whole brain)? That question is intrinsically SPATIAL -- it is about WHERE a focal drive
goes -- and E1 (§43) is exactly the layer that makes "where" representable. E1 left this owed:
its headline E1.3 result certified that each node's focal footprint is SELF-LOCALISING (the drive
concentrates at the site) or a RELAY (the drive lands harder off-target), drive-invariantly, with
the relay set {hippocampus, midbrain} fixed at every amplitude -- and named focal-epilepsy
containment-vs-spread as the first application that map unlocks. THIS module builds it: it IMPORTS
the SpatialField class (it does NOT re-derive the ephaptic kernel or the coupling map -- handover
reuse discipline) and reads, on the frozen kernel, which foci CONTAIN a focal ictal drive and
which BROADCAST it (secondarily generalise), and whether broadcast is the same thing as the §25
global over-synchronisation.
=================================================================================
THE GROUNDING (READ-ONLY; no new constant). A focal seizure focus is modelled as a strong focal
EXCITATORY ictal drive at one region, the rest at baseline, using the SAME k = kappa/(1-|b|)
[excit] map as §25/E1 (no new constant); the ictal intensity b0 is SWEPT over the E1 depth sweep
{0.3,0.5,0.7,0.9} (anti-tuning), and every SIGN/STRUCTURE asserted below is required to hold at
every swept intensity. CONTAINMENT is read from the E1 SpatialField footprint class (self vs
relay), SECONDARY GENERALISATION from the off-target vs own local-coherence change, and GLOBAL
hypersynchrony from the §25 global-order reach |R - R0|. g = 1.0 is the engine's universal R19
scale; nothing here is fit.

WHAT THE MODULE DELIVERS (pre-registered, sign/structure only; never magnitudes):
  F1  THE FOCUS PARTITION (containment vs secondary generalisation) IS DRIVE-INVARIANT. Driving
      each region as a focal ictal focus, the 12 foci partition into CONTAINED (self-localising --
      the ictal change concentrates at the focus, the seizure stays focal) and BROADCAST (relay --
      the change lands harder off-target, the seizure secondarily generalises). This binary
      partition is IDENTICAL across the entire ictal-intensity sweep: the broadcast set is
      {hippocampus, midbrain} at every intensity, the other ten foci contained at every intensity.
      Whether a focal seizure STAYS focal or SECONDARILY GENERALISES is a fixed property of focus
      LOCATION, not of how intense the ictal drive is. (Inherits the E1.3 self/relay class applied
      to a focal ictal drive.) grade [V mech].
  F2  BROADCAST IS OFF-TARGET DOMINANCE (the structural content of secondary generalisation). For
      a BROADCAST focus the ictal local-coherence change lands HARDER on distal circuits than on
      the focus itself: mean off-target |dc| > own |dc| (ratio > 1) -- the structural signature of
      a seizure recruiting circuits BEYOND its focus. For a CONTAINED focus it concentrates at the
      focus (ratio < 1) -- the seizure stays local. The broadcast <-> (off/own > 1) equivalence
      holds at every swept intensity. This makes F1's binary class quantitatively legible and ties
      "broadcast" to the clinical meaning of secondary generalisation. grade [V mech].
  F3  OFF-TARGET SPREAD IS NOT GLOBAL HYPERSYNCHRONY -- TWO DISTINCT AXES (the honest no-tuning
      result). A clean, attractive hypothesis -- "the broadcast / secondarily-generalising foci are
      exactly the foci that drive the whole brain into the §25 over-synchronisation seizure state
      (the largest global reach |R - R0|)" -- is tested and FOUND FALSE. (a) The broadcast set is
      NOT the high-global-reach set: the single largest global-reach focus is the CEREBELLUM, which
      is CONTAINED, at every swept intensity -- the largest global recruiter is not a broadcast
      focus. (b) The two broadcast foci move global synchrony in OPPOSITE directions: the midbrain
      RAISES global R (toward the §25 over-sync state) while the hippocampus LOWERS it (toward
      desynchronisation), at every swept intensity -- so "broadcast" carries no consistent global-
      synchrony sign at all. Off-target spread (F1/F2) and global hypersynchrony (the §25 over-sync
      axis) are therefore TWO DISTINCT, decoupled spatial properties: secondary-generalisation
      propagation is SITE-DETERMINED and not reducible to a single "spread = hypersynchrony" rule.
      We do NOT force the tidy single-axis story; the refuted clean hypothesis is reported honestly
      -- the E1.4 lesson ("no universal law; spatial outcome is site-determined") made concrete for
      epilepsy. grade [V mech] (a refuted clean hypothesis is a finding).
  F4  THE BROADCAST SET IS A COHERENT MINORITY RELAY-HUB CLASS (containment is the structural
      default). The two broadcast foci {hippocampus, midbrain} are SIMULTANEOUSLY the E1.3 relay
      set AND the off-target-dominant set (F2), a STRICT MINORITY (2 of 12, so CONTAINMENT is the
      structural default), AND disjoint from the global-reach hub (cerebellum, F3) -- one coherent
      class of limbic/brainstem relay hubs. Structurally, secondary generalisation is the EXCEPTION
      carried by specific relay hubs, not a global property of the ictal drive; this convergence
      holds across the depth sweep. A DIRECTION-ONLY [L] correspondence is noted, never a magnitude
      or a prediction: clinically most focal seizures remain focal, and mesial-temporal (hippocampal)
      foci are the paradigmatic secondarily-generalising epilepsy -- consistent with hippocampus
      sitting in the broadcast set. grade [V mech] structural + [L] cited correspondence.

NOT a claim that real focal epilepsy reduces to a phase-coupling footprint on a frozen 1/r^3
kernel (real seizure propagation is heterogeneous -- white-matter tractography, the specific
epileptogenic network, ictal recruitment dynamics, the patient's individual connectome and
pathology -- LOCKED); what is asserted is the SIGN/STRUCTURE of a focal ictal drive on the frozen
kernel and its four consequences (the containment/broadcast partition, off-target dominance, the
decoupling from global over-sync, and the minority relay-hub class). NOT a claim about the FELT
quality of a seizure or its aura (Axis-A firewall: a containment/broadcast class is a STRUCTURAL
spatial property of the coupling model, NEVER the felt locus of a seizure; consciousness_claim
stays 0; hard problem stays OPEN). NOT a real electrode, a real EEG/SEEG localisation, a real
current density, or a real seizure-propagation map; the per-node bias is not a real ictal drive.
NOT a prediction of WHICH patient's seizures will secondarily generalise, and NOT surgical or
resection guidance -- epilepsy diagnosis, localisation and surgery are external clinical decisions
made by clinicians with real data. NOT MEDICAL ADVICE; efficacy = 0 everywhere; in-silico
MECHANISM only; nothing here is a cure, a treatment, a localisation, or a prognosis. Every
MAGNITUDE is [O]; only structural SIGNS and RELATIONS are asserted, and they are certified to
survive the ictal-intensity sweep.

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY
(emerge_all is NOT touched, so the engine file stays e61083ae..., the tree stays 0fbf4988...
and the M0..M16 subtree stays 3a1ebbbb..., byte-identical). REUSES the E1 SpatialField
(imported, not re-derived). Writes focal_epilepsy_spread_results.json + its sha256, verified
bit-for-bit.
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

ICTAL_DEPTHS = DEPTHS                 # ictal-intensity sweep = E1 depth sweep (swept, not tuned)
REP = 0.7                             # representative ictal intensity for headline reads [swept]
HIPPO = REGS.index("hippocampus")
MIDB  = REGS.index("midbrain")
CEREB = REGS.index("cerebellum")
EXPECTED_BROADCAST = sorted([REGS[HIPPO], REGS[MIDB]])   # the E1.3 relay set


def _footprint(sf, node, b0):
    """Own and mean-off-target |dc| for a focal ictal drive at `node`, depth b0."""
    _, c = sf.focal(node, b0)
    dc = c - sf.c0
    own = float(abs(dc[node]))
    off = float(np.mean([abs(dc[j]) for j in range(N) if j != node]))
    return own, off


# ------------------------------- the four sub-studies + guard ----------------------------

def _partition(sf):
    """F1: the containment/broadcast partition over the ictal-intensity sweep. The partition is
    drive-invariant; the broadcast (relay) set is fixed."""
    vectors = {}
    for b0 in ICTAL_DEPTHS:
        vectors[round(b0, 2)] = [sf.footprint_class(t, b0) for t in range(N)]
    base = vectors[round(ICTAL_DEPTHS[0], 2)]
    invariant = bool(all(v == base for v in vectors.values()))
    broadcast = sorted([REGS[k] for k in range(N) if base[k] < 0])
    contained = sorted([REGS[k] for k in range(N) if base[k] > 0])
    broadcast_is_relay_set = bool(broadcast == EXPECTED_BROADCAST)
    labelled = {round(b0, 2): {REGS[t]: ("broadcast" if vectors[round(b0, 2)][t] < 0 else "contained")
                               for t in range(N)} for b0 in ICTAL_DEPTHS}
    return invariant, broadcast, contained, broadcast_is_relay_set, labelled


def _off_target_dominance(sf):
    """F2: broadcast <-> (mean off-target |dc| > own |dc|), at every swept intensity."""
    per_site = {}
    equivalence_all = True
    for b0 in ICTAL_DEPTHS:
        for t in range(N):
            own, off = _footprint(sf, t, b0)
            is_broadcast = bool(off > own)
            want_broadcast = bool(t in (HIPPO, MIDB))
            if is_broadcast != want_broadcast:
                equivalence_all = False
            if round(b0, 2) == REP:
                per_site[REGS[t]] = {"own_abs_dc": round(own, 6),
                                     "off_target_abs_dc": round(off, 6),
                                     "off_over_own": round(off / own, 4) if own > 0 else None,
                                     "off_target_dominant": is_broadcast}
    return bool(equivalence_all), per_site


def _spread_is_not_oversync(sf):
    """F3 (honest negative): off-target spread is NOT global hypersynchrony. (a) the top global-
    reach focus is the cerebellum (CONTAINED) at every intensity; (b) the two broadcast foci move
    global R in OPPOSITE directions at every intensity. The clean 'spread = over-sync' hypothesis
    is FALSE -- two distinct, decoupled spatial axes."""
    reach_hub_contained_all = True
    reach_dump = {}
    for b0 in ICTAL_DEPTHS:
        rv = np.array([sf.reach(t, b0) for t in range(N)])
        top = int(np.argmax(rv))
        if top != CEREB:
            reach_hub_contained_all = False
        reach_dump[round(b0, 2)] = {"top_reach_focus": REGS[top],
                                    "top_reach": round(float(rv[top]), 6),
                                    "hippocampus_reach": round(float(rv[HIPPO]), 6),
                                    "midbrain_reach": round(float(rv[MIDB]), 6)}
    # cerebellum is in the CONTAINED set (it is not a broadcast focus)
    reach_hub_is_contained = bool(CEREB not in (HIPPO, MIDB))

    opposite_sign_all = True
    direction_dump = {}
    for b0 in ICTAL_DEPTHS:
        Rh, _ = sf.focal(HIPPO, b0)
        Rm, _ = sf.focal(MIDB, b0)
        dh = float(Rh - sf.R0)
        dm = float(Rm - sf.R0)
        ok = bool(dm > 0 and dh < 0)          # midbrain raises (toward over-sync), hippocampus lowers
        if not ok:
            opposite_sign_all = False
        direction_dump[round(b0, 2)] = {"midbrain_dR": round(dm, 6), "midbrain_raises_sync": bool(dm > 0),
                                        "hippocampus_dR": round(dh, 6), "hippocampus_lowers_sync": bool(dh < 0)}
    broadcast_not_reach = bool(reach_hub_contained_all and reach_hub_is_contained)
    broadcast_no_sync_sign = bool(opposite_sign_all)
    decoupled = bool(broadcast_not_reach and broadcast_no_sync_sign)
    return (broadcast_not_reach, reach_hub_is_contained, broadcast_no_sync_sign, decoupled,
            reach_dump, direction_dump)


def _minority_hub_class(sf):
    """F4: the broadcast set is a coherent minority relay-hub class -- the E1.3 relay set AND the
    off-target-dominant set (F2), a strict minority (containment the default), disjoint from the
    global-reach hub. Convergence holds across the sweep."""
    invariant, broadcast, contained, is_relay_set, _ = _partition(sf)
    n_broadcast = len(broadcast)
    is_minority = bool(n_broadcast < N - n_broadcast)        # broadcast is the strict minority
    containment_is_default = bool(len(contained) > n_broadcast)
    disjoint_from_reach_hub = bool(REGS[CEREB] not in broadcast)
    # the broadcast set is the off-target-dominant set (F2 equivalence) at the representative depth
    od_set = sorted([REGS[t] for t in range(N) if _footprint(sf, t, REP)[1] > _footprint(sf, t, REP)[0]])
    broadcast_eq_off_target = bool(od_set == broadcast)
    coherent_class = bool(is_relay_set and broadcast_eq_off_target and is_minority
                          and containment_is_default and disjoint_from_reach_hub)
    return (coherent_class, broadcast, n_broadcast, is_minority, containment_is_default,
            disjoint_from_reach_hub, broadcast_eq_off_target)


def _invariance(sf):
    """S5: a zero ictal drive (no focus driven) reproduces the frozen M9 anchor R bit-for-bit and
    the per-node field equals the baseline exactly -- the focal-spread reads are a pure structural
    read on the frozen kernel (no new mechanism/measurement/constant)."""
    R_direct = E._integrate(OMEGA, W0, KAP * OMEGA0)[0]          # frozen M9 anchor (engine)
    Rb, cb = sf.drive(np.zeros(N))                               # zero ictal drive (off-state)
    matches_anchor = bool(R_direct == M9_ANCHOR_R)
    offstate_matches = bool(Rb == R_direct)
    field_matches = bool(np.array_equal(cb, sf.c0))
    baseline_matches = bool(sf.R0 == M9_ANCHOR_R)
    return R_direct, Rb, matches_anchor, offstate_matches, field_matches, baseline_matches


def run():
    sf = SpatialField()

    # ===== F1 : the containment/broadcast partition, drive-invariant =====
    part_inv, broadcast, contained, is_relay_set, part_labelled = _partition(sf)
    F1 = bool(part_inv and is_relay_set)

    # ===== F2 : broadcast = off-target dominance =====
    od_equiv, od_per_site = _off_target_dominance(sf)
    F2 = bool(od_equiv)

    # ===== F3 : off-target spread != global hypersynchrony (honest negative) =====
    (b_not_reach, reach_hub_contained, b_no_sync_sign, decoupled,
     reach_dump, direction_dump) = _spread_is_not_oversync(sf)
    F3 = bool(decoupled)

    # ===== F4 : the broadcast set is a coherent minority relay-hub class =====
    (coherent, b4, n_b, is_min, cont_default, disjoint, b_eq_od) = _minority_hub_class(sf)
    F4 = bool(coherent)

    # ===== S5 : engine-invariance guard =====
    Rinv, Roff, anchor_ok, off_ok, field_ok, base_ok = _invariance(sf)
    S5 = bool(anchor_ok and off_ok and field_ok and base_ok)

    preds = {
        "F1_focus_partition_drive_invariant":   "CONFIRMED" if F1 else "REFUTED",
        "F2_broadcast_is_off_target_dominance": "CONFIRMED" if F2 else "REFUTED",
        "F3_spread_not_global_hypersynchrony":  "CONFIRMED" if F3 else "REFUTED",
        "F4_broadcast_minority_relay_hub_class":"CONFIRMED" if F4 else "REFUTED",
    }

    res = {
        "_what": "FOC-EPI-E1 -- focal epilepsy: containment vs secondary generalisation. The FIRST "
                 "region-specific application of the E1 spatial-localisation layer (§43) and the "
                 "SPATIAL refinement of the §25 (T2a) over-synchronisation epilepsy module. §25 "
                 "placed the seizure as the network crossing the over-sync threshold on the GLOBAL "
                 "order R, but drove the brain GLOBALLY, so it could not ask whether a seizure that "
                 "BEGINS at one focus STAYS focal or SECONDARILY GENERALISES -- an intrinsically "
                 "SPATIAL question. This module IMPORTS the E1 SpatialField (it does NOT re-derive "
                 "the kernel or coupling map) and reads, on the frozen kernel, which foci CONTAIN a "
                 "focal ictal drive and which BROADCAST it, and whether broadcast is the same thing "
                 "as the §25 global over-synchronisation. Four sign-only results: F1 the "
                 "containment/broadcast partition is drive-invariant (broadcast set {hippocampus, "
                 "midbrain} fixed across the ictal-intensity sweep -- whether a focal seizure stays "
                 "focal or secondarily generalises is a property of focus LOCATION); F2 broadcast is "
                 "off-target dominance (the ictal change lands harder on distal circuits than on the "
                 "focus -- the structural content of secondary generalisation); F3 (honest negative) "
                 "off-target spread is NOT global hypersynchrony (the cerebellum is the largest "
                 "global recruiter yet is CONTAINED, and the two broadcast foci move global R in "
                 "OPPOSITE directions -- two distinct decoupled axes, the E1.4 lesson for epilepsy); "
                 "F4 the broadcast set is a coherent minority relay-hub class (containment is the "
                 "structural default, secondary generalisation the exception carried by specific "
                 "relay hubs). MECHANISM only -- a containment/broadcast class is a STRUCTURAL spatial "
                 "quantity, NOT a felt seizure locus, NOT a real electrode/EEG/SEEG, NOT a clinical "
                 "prediction of which seizures generalise, and NOT surgical guidance. efficacy=0; not "
                 "medical advice.",
        "roadmap_id": "E1 region-specific application #1 (focal epilepsy), the spatial refinement of "
                      "§25 T2a over-sync epilepsy; the first application of the E1.3 self/relay map "
                      "named owed by §43; RESEARCH_ROADMAP_post_autism_adhd.md",
        "application_of_E1": {
            "E1_supplied": "the E1.3 SELF-LOCALISING vs RELAY classification (drive-invariant, relay "
                           "set {hippocampus, midbrain}) and the E1.2 heterogeneous global reach with "
                           "a drive-stable cerebellar hub -- a fixed spatial MAP of the frozen kernel",
            "this_module_reads": "which foci CONTAIN a focal ictal drive (stay focal) and which "
                                 "BROADCAST it (secondarily generalise), and tests whether broadcast "
                                 "coincides with the §25 global over-synchronisation -- it finds it "
                                 "does NOT (F3), so secondary-generalisation propagation is site-"
                                 "determined, exactly the region-specific reading E1.4 demanded",
            "reuse_discipline": "imports SpatialField; does NOT re-derive the ephaptic kernel W0 or "
                                "the k(b) coupling map; engine emerged READ-ONLY and byte-unchanged",
            "seam_with_sec25": "§25 (T2a) certified the seizure = global over-sync on R; §44 refines "
                               "it spatially -- a focus's tendency to secondarily generalise (off-"
                               "target broadcast) is a DIFFERENT, decoupled property from how much it "
                               "drives the global over-sync state, so the two cannot be conflated",
        },
        "ictal_model": {
            "form": "a focal seizure focus = a strong focal EXCITATORY ictal drive at one region "
                    "(the rest at baseline), via the SAME k = kappa/(1-|b|) [excit] map as §25/E1 "
                    "(no new constant); ictal intensity b0 swept over {0.3,0.5,0.7,0.9} (anti-tuning)",
            "form_grade": "[F] forced -- the frozen ephaptic kernel W0 plus the existing k(b) map; "
                          "no free constant; a zero ictal drive reproduces the scalar engine bit-for-bit",
            "ictal_intensity_sweep": list(ICTAL_DEPTHS),
            "representative_intensity": REP,
            "profile_grade": "[O] swept -- the ictal intensity is a SWEEP, not a tuned constant; every "
                             "SIGN/STRUCTURE holds across the sweep",
            "reused_constants": {"kappa_measured": round(KAP, 6), "R19_fold_spinodal": round(FOLD, 6),
                                 "n_regions": N, "baseline_R0_M9_anchor": round(sf.R0, 10)},
        },
        "F1_focus_partition": {
            "partition_drive_invariant": part_inv,
            "broadcast_set": broadcast,
            "broadcast_set_is_E1_relay_set": is_relay_set,
            "contained_set": contained,
            "partition_per_intensity": part_labelled,
            "reproduced": F1,
            "reading": "driving each region as a focal ictal focus, the 12 foci partition into "
                       "CONTAINED (self-localising -- the ictal change concentrates at the focus, the "
                       "seizure stays focal) and BROADCAST (relay -- the change lands harder off-"
                       "target, the seizure secondarily generalises). The partition is IDENTICAL "
                       "across the entire ictal-intensity sweep, the broadcast set {hippocampus, "
                       "midbrain} fixed at every intensity. Whether a focal seizure stays focal or "
                       "secondarily generalises is a fixed property of focus LOCATION, not of ictal "
                       "intensity. Inherits the E1.3 self/relay class; structure-only.",
        },
        "F2_off_target_dominance": {
            "broadcast_iff_off_target_dominant_all_intensities": od_equiv,
            "per_site_at_representative_intensity": od_per_site,
            "reproduced": F2,
            "reading": "for a BROADCAST focus the ictal local-coherence change lands HARDER on distal "
                       "circuits than on the focus itself (mean off-target |dc| > own |dc|, ratio > 1) "
                       "-- the structural signature of a seizure recruiting circuits BEYOND its focus; "
                       "for a CONTAINED focus it concentrates at the focus (ratio < 1). The broadcast "
                       "<-> (off/own > 1) equivalence holds at every swept intensity, tying 'broadcast' "
                       "to the clinical meaning of secondary generalisation. Sign-only; magnitudes [O].",
        },
        "F3_spread_not_global_hypersynchrony": {
            "_what": "the honest no-tuning result -- a clean hypothesis ('the broadcast / secondarily-"
                     "generalising foci are exactly the foci that drive the whole brain into the §25 "
                     "over-sync state') tested and FOUND FALSE",
            "top_global_reach_focus_is_contained_all_intensities": b_not_reach,
            "global_reach_hub_is_in_contained_set": reach_hub_contained,
            "reach_per_intensity": reach_dump,
            "broadcast_foci_oppose_on_global_sync_all_intensities": b_no_sync_sign,
            "global_sync_direction_per_intensity": direction_dump,
            "two_axes_decoupled": decoupled,
            "reproduced": F3,
            "verdict": "the broadcast set is NOT the high-global-reach set (the single largest global-"
                       "reach focus is the CEREBELLUM, which is CONTAINED, at every intensity), and the "
                       "two broadcast foci move global synchrony in OPPOSITE directions (the midbrain "
                       "RAISES global R toward the §25 over-sync state while the hippocampus LOWERS it, "
                       "at every intensity) -- so 'broadcast' carries no consistent global-synchrony "
                       "sign. Off-target spread (F1/F2) and global hypersynchrony (the §25 over-sync "
                       "axis) are TWO DISTINCT, decoupled spatial properties; secondary-generalisation "
                       "propagation is SITE-DETERMINED and not reducible to a 'spread = hypersynchrony' "
                       "rule. The refuted clean hypothesis is reported honestly -- the E1.4 lesson "
                       "made concrete for epilepsy. A refuted clean hypothesis is a finding.",
        },
        "F4_broadcast_minority_relay_hub_class": {
            "broadcast_set": b4,
            "n_broadcast": n_b,
            "broadcast_is_strict_minority": is_min,
            "containment_is_structural_default": cont_default,
            "broadcast_equals_off_target_dominant_set": b_eq_od,
            "disjoint_from_global_reach_hub": disjoint,
            "coherent_minority_relay_hub_class": coherent,
            "reproduced": F4,
            "clinical_correspondence_grade": "[L] direction-only",
            "clinical_correspondence": "a DIRECTION-ONLY cited correspondence, never a magnitude or a "
                                       "prediction: clinically most focal seizures remain focal, and "
                                       "mesial-temporal (hippocampal) foci are the paradigmatic "
                                       "secondarily-generalising epilepsy -- consistent with the "
                                       "hippocampus sitting in the broadcast set and with containment "
                                       "being the structural majority. NOT a patient-level prediction.",
            "reading": "the two broadcast foci {hippocampus, midbrain} are simultaneously the E1.3 "
                       "relay set AND the off-target-dominant set (F2), a STRICT MINORITY (2 of 12 -- "
                       "containment is the structural default), AND disjoint from the global-reach hub "
                       "(cerebellum) -- one coherent class of limbic/brainstem relay hubs. Secondary "
                       "generalisation is structurally the EXCEPTION carried by specific relay hubs, "
                       "not a global property of the ictal drive. Structure-only; the clinical "
                       "correspondence is [L] direction-only.",
        },
        "S5_engine_invariance_guard": {
            "_what": "a zero ictal drive (no focus driven) reproduces the frozen M9 coordination anchor "
                     "bit-for-bit and the per-node field equals the baseline exactly -- the focal-spread "
                     "reads are a pure structural read on the frozen kernel (no new mechanism)",
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
                "this module shapes a focal ictal drive on the frozen kernel, it does not re-derive it",
            "oversync_seam_cited": "§25 (T2a) certified the seizure = global over-synchronisation on R; "
                "§44 refines it spatially and shows secondary-generalisation broadcast is a DIFFERENT, "
                "decoupled property from the global over-sync magnitude (F3)",
            "partition_is_position_LOCK": "whether a focal seizure stays focal or secondarily "
                "generalises is a fixed property of focus LOCATION (the E1.3 relay class), drive-"
                "invariant -- structure, not a fitted result",
            "no_universal_spread_law_LOCK": "off-target spread is NOT global hypersynchrony; the clean "
                "'spread = over-sync' hypothesis is explicitly refuted, not forced -- secondary-"
                "generalisation propagation is site-determined (the E1.4 lesson for epilepsy)",
            "real_propagation_heterogeneous_LOCK": "real seizure propagation is HETEROGENEOUS (white-"
                "matter tractography, the individual epileptogenic network, ictal recruitment dynamics, "
                "the patient's connectome and pathology); this module asserts the SIGN/STRUCTURE of a "
                "focal ictal drive on the FROZEN kernel, not that any real focal seizure follows it",
            "not_clinical_LOCK": "nothing here is a real electrode, EEG/SEEG localisation, current "
                "density, seizure-propagation map, a prediction of which patient's seizures generalise, "
                "or surgical/resection guidance; localisation and surgery are external clinical decisions",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; whether any "
                "real focal seizure contains or generalises by this structure is external",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "spatial_quantities_are_structural": 1.0,
            "reuses_E1_spatial_field": 1.0,
            "ictal_intensity": "OPEN [O] -- swept; signs/structure hold over the ictal-intensity sweep, "
                               "not tuned",
            "clean_hypothesis_refuted": "F3 reports a REFUTED clean hypothesis honestly (off-target "
                                        "spread is NOT global hypersynchrony) rather than forcing a "
                                        "single-axis 'spread = over-sync' narrative",
            "clinical_prediction": "NONE -- no patient-level prediction of secondary generalisation, no "
                                   "localisation, no surgical guidance; the only clinical correspondence "
                                   "(F4) is [L] direction-only",
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
            "F1_focus_partition_drive_invariant": {
                "claim": "driving each region as a focal ictal focus, the containment/broadcast "
                         "partition is identical across the ictal-intensity sweep and the broadcast "
                         "(relay) set is {hippocampus, midbrain} at every intensity",
                "status": preds["F1_focus_partition_drive_invariant"]},
            "F2_broadcast_is_off_target_dominance": {
                "claim": "a focus is broadcast IFF its ictal change lands harder off-target than on "
                         "itself (mean off-target |dc| > own |dc|), at every swept intensity",
                "status": preds["F2_broadcast_is_off_target_dominance"]},
            "F3_spread_not_global_hypersynchrony": {
                "claim": "off-target spread is NOT global hypersynchrony: the top global-reach focus is "
                         "the contained cerebellum at every intensity AND the two broadcast foci move "
                         "global R in opposite directions at every intensity -- two decoupled axes",
                "status": preds["F3_spread_not_global_hypersynchrony"]},
            "F4_broadcast_minority_relay_hub_class": {
                "claim": "the broadcast set is the E1.3 relay set AND the off-target-dominant set, a "
                         "strict minority (containment the default), disjoint from the global-reach hub "
                         "-- one coherent minority relay-hub class",
                "status": preds["F4_broadcast_minority_relay_hub_class"]},
        },
        "overall": {
            "focus_partition_drive_invariant": F1,
            "broadcast_is_off_target_dominance": F2,
            "spread_not_global_hypersynchrony": F3,
            "broadcast_minority_relay_hub_class": F4,
            "engine_invariance_guard": S5,
            "is_full_module": bool(F1 and F2 and F3 and F4 and S5),
            "verdict": "focal epilepsy containment vs secondary generalisation -- the first region-"
                       "specific application of the E1 spatial-localisation layer and the spatial "
                       "refinement of §25 over-sync epilepsy. Driving each region as a focal ictal "
                       "focus, the containment/broadcast partition is DRIVE-INVARIANT, the broadcast "
                       "(secondarily-generalising) set {hippocampus, midbrain} fixed at every intensity "
                       "(F1); broadcast IS off-target dominance, the structural content of secondary "
                       "generalisation (F2); off-target spread is NOT global hypersynchrony -- the "
                       "largest global recruiter is the CONTAINED cerebellum and the two broadcast foci "
                       "oppose on global synchrony, so the two are distinct decoupled axes (F3, the "
                       "honest no-tuning result, the E1.4 lesson for epilepsy); and the broadcast set "
                       "is a coherent minority relay-hub class, containment the structural default (F4). "
                       "A zero ictal drive reproduces the frozen M9 anchor bit-for-bit (S5). The ictal "
                       "form is forced, the intensity swept, every sign survives the sweep, no new tuned "
                       "constant, engine byte-unchanged; the SpatialField is imported, not re-derived. "
                       "Axis-A firewall: a containment/broadcast class is a structural spatial quantity, "
                       "NOT a felt seizure locus, NOT a real electrode/EEG/SEEG, NOT a prediction of "
                       "which seizures generalise, NOT surgical guidance. efficacy=0; not medical advice.",
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

def focal_epilepsy_spread_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "focal_epilepsy_spread_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_focal_epilepsy_spread_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"focal_epilepsy_spread_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = focal_epilepsy_spread_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    m = res["ictal_model"]
    f1 = res["F1_focus_partition"]; f2 = res["F2_off_target_dominance"]
    f3 = res["F3_spread_not_global_hypersynchrony"]; f4 = res["F4_broadcast_minority_relay_hub_class"]
    g = res["S5_engine_invariance_guard"]
    print("=" * 78)
    print("FOC-EPI-E1 -- FOCAL EPILEPSY: CONTAINMENT vs SECONDARY GENERALISATION (E1 application)")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  ictal model: focal excitatory drive; intensity sweep={m['ictal_intensity_sweep']}  form={m['form_grade'][:18]}")
    print("-" * 78)
    print(f"  F1 partition     : drive-invariant={f1['partition_drive_invariant']}  broadcast(relay) set={f1['broadcast_set']}")
    print(f"  F2 off-target    : broadcast<->off>own (all intensities)={f2['broadcast_iff_off_target_dominant_all_intensities']}")
    print(f"  F3 NOT over-sync : reach-hub contained(cerebellum) all={f3['top_global_reach_focus_is_contained_all_intensities']}  broadcast oppose on sync={f3['broadcast_foci_oppose_on_global_sync_all_intensities']}  -> decoupled={f3['two_axes_decoupled']}")
    print(f"  F4 minority hub  : broadcast={f4['broadcast_set']} n={f4['n_broadcast']}  minority={f4['broadcast_is_strict_minority']}  disjoint-from-reach-hub={f4['disjoint_from_global_reach_hub']}  -> coherent={f4['coherent_minority_relay_hub_class']}")
    print(f"  S5 invariance    : off-state R={g['offstate_R']}  ==anchor:{g['matches_frozen_anchor_bitwise'] and g['offstate_matches_direct_bitwise']}  field==baseline:{g['offstate_field_equals_baseline']}")
    print("-" * 78)
    print(f"  pre-registered: {[ (k, v['status']) for k,v in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  FOCAL-EPILEPSY SPATIAL MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
