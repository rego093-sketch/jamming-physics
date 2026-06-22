#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LESION-E1 -- STROKE / LESION FIELD : LOCAL DEFICIT vs REMOTE DIASCHISIS : the SECOND region-
specific application of the E1 spatial-localisation layer (§43), the spatial sibling of the §44
focal-epilepsy application. §44 drove a region with a focal EXCITATORY (ictal) bias and asked
whether a seizure stays focal or secondarily generalises. THIS module asks the complementary
lesion question: when a focal lesion (a stroke) SILENCES one region, does the deficit stay LOCAL
(a focal deficit at the lesion) or does it disrupt circuits FAR from the lesion -- the classical
neurological phenomenon of DIASCHISIS (von Monakow), remote dysfunction at sites anatomically
distant from but connected to a focal injury? That question is intrinsically SPATIAL -- it is
about WHERE the loss of a node propagates -- and E1 (§43) is exactly the layer that makes "where"
representable. E1 named stroke/lesion fields as an owed application of its self/relay map. THIS
module builds it: it IMPORTS the SpatialField class (it does NOT re-derive the ephaptic kernel or
the coupling map -- handover reuse discipline) and reads, on the frozen kernel, which lesions
CONTAIN their deficit (a focal deficit) and which cause REMOTE DIASCHISIS, and whether remote
diaschisis is the same thing as collapsing GLOBAL coordination.
=================================================================================
THE GROUNDING (READ-ONLY; no new constant). A focal lesion is modelled as a strong focal
INHIBITORY (silencing) bias at one region, the rest at baseline, using the SAME k = kappa/(1+|b|)
[inhib] map as the SZ / epilepsy / E1 modules (no new constant). CRUCIALLY the lesioned node is
NOT deleted -- deleting a node would break the frozen ephaptic kernel W0 and forfeit the kernel
reuse -- it is SILENCED (its effective coupling driven down by a strong inhibitory bias), so the
frozen kernel is reused intact (the handover's explicit lesion-modelling directive). The lesion
SEVERITY b0 is SWEPT over the MODERATE-TO-SEVERE range {-0.5,-0.7,-0.9}; this severity floor
|b0|>=0.5 is INHERITED from E1.2 (which certified reach-ranking invariance only for moderate-to-
high drive b0>=0.5), so it is a principled reuse of the layer's own invariance scope, NOT a tuned
choice. A single MILD severity -0.3 (BELOW the E1.2 floor) is additionally probed and reported
HONESTLY (a marginal node enters at mild severity), exactly to show why the invariant claims are
scoped to the moderate-to-severe core. Every SIGN/STRUCTURE asserted below is required to hold at
every severity in the swept core. CONTAINMENT (local deficit) is read from the E1 SpatialField
footprint class (self vs relay), REMOTE DIASCHISIS from the off-target vs own local-coherence
change, and GLOBAL-COORDINATION DISRUPTION from the §25-style global-order reach |R - R0|.
g = 1.0 is the engine's universal R19 scale; nothing here is fit.

WHAT THE MODULE DELIVERS (pre-registered, sign/structure only; never magnitudes):
  L1  THE LESION PARTITION (local deficit vs remote diaschisis) IS DRIVE-INVARIANT over the
      moderate-to-severe core, and the diaschisis set is the E1.3 relay set. Silencing each region
      as a focal lesion, the 12 lesions partition into LOCAL-DEFICIT (self-localising -- the
      coherence deficit concentrates at the lesion, a focal deficit) and REMOTE-DIASCHISIS (relay
      -- the deficit lands harder off-target, the lesion disrupts distal circuits). This binary
      partition is IDENTICAL across the moderate-to-severe lesion-severity sweep {-0.5,-0.7,-0.9}:
      the diaschisis set is {hippocampus, midbrain} at every severity, the other ten lesions
      local at every severity, and the diaschisis set is exactly the E1.3 RELAY set. Whether a
      focal lesion stays local or causes remote diaschisis is a fixed property of lesion LOCATION,
      not of lesion severity. HONEST sub-floor note: at the MILD severity -0.3, BELOW the E1.2
      |b|>=0.5 invariance floor, the thalamus ADDITIONALLY enters the diaschisis set -- a severity-
      dependent marginal reported honestly, exactly why the invariant claim is scoped to the
      moderate-to-severe core (inheriting the E1.2 floor). grade [V mech].
  L2  REMOTE DIASCHISIS IS OFF-TARGET DOMINANCE (the structural content of diaschisis). For a
      DIASCHISIS lesion the coherence deficit lands HARDER on distal circuits than at the lesion
      itself: mean off-target |dc| > own |dc| (ratio > 1) -- the structural signature of remote
      dysfunction beyond the lesion (the hippocampus ~1.2x, the midbrain ~3.0x at the
      representative severity). For a LOCAL-DEFICIT lesion it concentrates at the lesion (ratio < 1
      -- the cerebellum ~0.06x, an overwhelmingly focal deficit). The diaschisis <-> (off/own > 1)
      equivalence holds at every swept severity, tying "diaschisis" to its clinical meaning. grade
      [V mech].
  L3  GLOBAL-COORDINATION DISRUPTION IS NOT REMOTE DIASCHISIS -- TWO DISTINCT AXES (the honest no-
      tuning result). A clean, attractive hypothesis -- "the lesions that most disrupt GLOBAL
      coordination (the largest global-order reach |R - R0|) are exactly the remote-diaschisis
      lesions" -- is tested and FOUND FALSE. The single largest global disruptor is the CEREBELLUM,
      a LOCAL-DEFICIT lesion (NOT in the diaschisis set), at the representative moderate severities
      (it is the rank-1 global disruptor at -0.5 and -0.7) and it remains a top-3 global disruptor
      at every swept severity while producing NO diaschisis (its deficit concentrates locally,
      off/own < 1 and LOCAL class at every severity). A lesion can therefore maximally disrupt
      GLOBAL coordination while being maximally LOCAL in its field footprint. Global-coordination
      disruption (reach) and remote diaschisis (off-target deficit) are therefore TWO DISTINCT,
      decoupled spatial properties: which sites cause remote dysfunction is SITE-DETERMINED and not
      reducible to a single "global impact = diaschisis" rule. An HONEST contrast with §44 is
      reported: unlike the ictal case (where the cerebellum topped the reach ranking at EVERY
      intensity), the lesion global-reach hub is itself NOT drive-invariant -- it is the contained
      cerebellum at -0.5 and -0.7 but the remote midbrain at the most severe -0.9 -- so the very
      ranking shifts with severity; the decoupling is carried by the cerebellum being LOCAL-yet-
      top-reach across all severities. We do NOT force the tidy single-axis story; the refuted
      clean hypothesis is reported honestly -- the E1.4 lesson made concrete for stroke/lesion.
      grade [V mech] (a refuted clean hypothesis is a finding).
  L4  THE DIASCHISIS SET IS A COHERENT MINORITY RELAY-HUB CLASS (local deficit is the structural
      default). The two diaschisis lesions {hippocampus, midbrain} are SIMULTANEOUSLY the E1.3
      relay set AND the off-target-dominant set (L2), a STRICT MINORITY (2 of 12, so LOCAL DEFICIT
      is the structural default -- most focal lesions cause focal deficits), AND decoupled from the
      global-reach hub (the local cerebellum at moderate severity, L3) -- one coherent class of
      limbic/brainstem relay hubs. Structurally, remote diaschisis is the EXCEPTION carried by
      specific relay hubs, not a generic property of lesions; this convergence holds across the
      moderate-to-severe sweep. A DIRECTION-ONLY [L] correspondence is noted, never a magnitude or
      a prediction: clinically most focal lesions produce focal deficits, while diaschisis (remote
      dysfunction after focal injury -- e.g. crossed cerebellar diaschisis, thalamic/limbic remote
      effects, von Monakow's classical concept) is the recognised EXCEPTION at specific connected
      hubs -- consistent with the diaschisis set being a strict minority of relay hubs. grade
      [V mech] structural + [L] cited correspondence.

NOT a claim that real stroke/lesion deficits reduce to a phase-coupling footprint on a frozen
1/r^3 kernel (real lesion consequences are heterogeneous -- the vascular territory, white-matter
tractography, the individual connectome, oedema, penumbra and reorganisation -- LOCKED); what is
asserted is the SIGN/STRUCTURE of a focal silencing bias on the frozen kernel and its four
consequences (the local/diaschisis partition, off-target dominance, the decoupling from global-
coordination disruption, and the minority relay-hub class). NOT a claim about the FELT quality of
a deficit (Axis-A firewall: a local/diaschisis class is a STRUCTURAL spatial property of the
coupling model, NEVER a felt deficit; consciousness_claim stays 0; hard problem stays OPEN). NOT a
real lesion, a real perfusion/diffusion map, a real connectome, or a real diaschisis measurement;
the per-node bias is not a real lesion. NOT a prediction of WHICH patient's lesion will cause
remote dysfunction, and NOT clinical, prognostic, or rehabilitation guidance -- stroke diagnosis,
deficit localisation and prognosis are external clinical decisions made by clinicians with real
data. NOT MEDICAL ADVICE; efficacy = 0 everywhere; in-silico MECHANISM only; nothing here is a
cure, a treatment, a localisation, or a prognosis. Every MAGNITUDE is [O]; only structural SIGNS
and RELATIONS are asserted, and they are certified to survive the lesion-severity sweep.

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY
(emerge_all is NOT touched, so the engine file stays e61083ae..., the tree stays 0fbf4988...
and the M0..M16 subtree stays 3a1ebbbb..., byte-identical). REUSES the E1 SpatialField
(imported, not re-derived); the lesion is a SILENCING bias on the frozen kernel, never a node
deletion. Writes lesion_field_diaschisis_results.json + its sha256, verified bit-for-bit.
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

# Lesion-severity sweep = the NEGATIVE (silencing) image of the E1 depth sweep, restricted to the
# MODERATE-TO-SEVERE core |b0|>=0.5 -- the SAME invariance floor E1.2 used for reach-ranking
# invariance (principled inheritance, NOT a tuned choice). A single MILD severity -0.3 (BELOW the
# floor) is probed separately for the honest L1 sub-floor note.
LESION_DEPTHS = (-0.5, -0.7, -0.9)        # moderate-to-severe lesion-severity sweep (swept, not tuned)
MILD_DEPTH    = -0.3                       # a single sub-floor probe for the honest marginal note
REP           = -0.7                       # representative lesion severity for headline reads [swept]
HIPPO = REGS.index("hippocampus")
MIDB  = REGS.index("midbrain")
CEREB = REGS.index("cerebellum")
THAL  = REGS.index("thalamus")
EXPECTED_DIASCHISIS = sorted([REGS[HIPPO], REGS[MIDB]])   # the E1.3 relay set


def _footprint(sf, node, b0):
    """Own and mean-off-target |dc| for a focal silencing (lesion) bias at `node`, severity b0."""
    _, c = sf.focal(node, b0)
    dc = c - sf.c0
    own = float(abs(dc[node]))
    off = float(np.mean([abs(dc[j]) for j in range(N) if j != node]))
    return own, off


def _reach_rank(sf, node, b0):
    """1-indexed rank of `node` in the descending global-reach |R-R0| ranking at severity b0."""
    rv = np.array([sf.reach(t, b0) for t in range(N)])
    order = list(np.argsort(rv)[::-1])
    return order.index(node) + 1


# ------------------------------- the four sub-studies + guard ----------------------------

def _partition(sf):
    """L1: the local-deficit/remote-diaschisis partition over the moderate-to-severe lesion-
    severity sweep. The partition is drive-invariant; the diaschisis (relay) set is fixed and
    equals the E1.3 relay set. The mild sub-floor severity is probed separately for honesty."""
    vectors = {}
    for b0 in LESION_DEPTHS:
        vectors[round(b0, 2)] = [sf.footprint_class(t, b0) for t in range(N)]
    base = vectors[round(LESION_DEPTHS[0], 2)]
    invariant = bool(all(v == base for v in vectors.values()))
    diaschisis = sorted([REGS[k] for k in range(N) if base[k] < 0])
    local = sorted([REGS[k] for k in range(N) if base[k] > 0])
    diaschisis_is_relay_set = bool(diaschisis == EXPECTED_DIASCHISIS)
    labelled = {round(b0, 2): {REGS[t]: ("diaschisis" if vectors[round(b0, 2)][t] < 0 else "local")
                               for t in range(N)} for b0 in LESION_DEPTHS}
    # honest sub-floor probe: at MILD severity (below the E1.2 |b|>=0.5 floor) the thalamus also
    # relays -- the diaschisis set is {hippocampus, midbrain} ONLY at and above the moderate floor.
    mild_classes = [sf.footprint_class(t, MILD_DEPTH) for t in range(N)]
    mild_diaschisis = sorted([REGS[k] for k in range(N) if mild_classes[k] < 0])
    thalamus_enters_at_mild = bool(REGS[THAL] in mild_diaschisis and REGS[THAL] not in diaschisis)
    return (invariant, diaschisis, local, diaschisis_is_relay_set, labelled,
            mild_diaschisis, thalamus_enters_at_mild)


def _off_target_dominance(sf):
    """L2: diaschisis <-> (mean off-target |dc| > own |dc|), at every swept severity."""
    per_site = {}
    equivalence_all = True
    for b0 in LESION_DEPTHS:
        for t in range(N):
            own, off = _footprint(sf, t, b0)
            is_diaschisis = bool(off > own)
            want_diaschisis = bool(t in (HIPPO, MIDB))
            if is_diaschisis != want_diaschisis:
                equivalence_all = False
            if round(b0, 2) == REP:
                per_site[REGS[t]] = {"own_abs_dc": round(own, 6),
                                     "off_target_abs_dc": round(off, 6),
                                     "off_over_own": round(off / own, 4) if own > 0 else None,
                                     "off_target_dominant": is_diaschisis}
    return bool(equivalence_all), per_site


def _disruption_is_not_diaschisis(sf):
    """L3 (honest negative): global-coordination disruption is NOT remote diaschisis. The single
    largest global disruptor is the LOCAL-deficit cerebellum at the representative moderate
    severities, and the cerebellum is a top-3 global disruptor at EVERY severity while producing
    NO diaschisis (LOCAL class, off/own<1, at every severity) -- a lesion can max global disruption
    while being maximally local. The clean 'global disruption = diaschisis' hypothesis is FALSE --
    two distinct, decoupled spatial axes. The global-reach hub itself is NOT drive-invariant (it
    flips cerebellum->midbrain at the most severe), reported honestly as a contrast with §44."""
    # the cerebellum (a candidate local-deficit lesion) across the severity sweep
    cereb_local_all = True
    cereb_top3_all = True
    cereb_off_lt_own_all = True
    reach_dump = {}
    top_disruptor_is_local_at_moderate = True
    reach_hub_per_severity = {}
    clean_hypothesis_refuted = False           # refuted if any top disruptor is NOT in diaschisis set
    for b0 in LESION_DEPTHS:
        rv = np.array([sf.reach(t, b0) for t in range(N)])
        top = int(np.argmax(rv))
        reach_hub_per_severity[round(b0, 2)] = REGS[top]
        if top not in (HIPPO, MIDB):
            clean_hypothesis_refuted = True     # a LOCAL lesion tops global disruption
        # cerebellum properties
        if sf.footprint_class(CEREB, b0) <= 0:
            cereb_local_all = False
        crank = _reach_rank(sf, CEREB, b0)
        if crank > 3:
            cereb_top3_all = False
        own_c, off_c = _footprint(sf, CEREB, b0)
        if not (off_c < own_c):
            cereb_off_lt_own_all = False
        # at the moderate severities (-0.5,-0.7) the top global disruptor should be a LOCAL lesion
        if round(b0, 2) in (-0.5, -0.7) and top in (HIPPO, MIDB):
            top_disruptor_is_local_at_moderate = False
        reach_dump[round(b0, 2)] = {"top_global_disruptor": REGS[top],
                                    "top_reach": round(float(rv[top]), 6),
                                    "cerebellum_reach": round(float(rv[CEREB]), 6),
                                    "cerebellum_reach_rank": crank,
                                    "cerebellum_is_local_deficit": bool(sf.footprint_class(CEREB, b0) > 0),
                                    "cerebellum_off_over_own": round(off_c / own_c, 4) if own_c > 0 else None}
    # the reach hub is NOT drive-invariant (honest contrast with §44, which had cerebellum at all)
    reach_hub_drive_invariant = bool(len(set(reach_hub_per_severity.values())) == 1)
    local_lesion_maxes_global_disruption = bool(cereb_local_all and cereb_top3_all
                                                and cereb_off_lt_own_all
                                                and top_disruptor_is_local_at_moderate)
    decoupled = bool(local_lesion_maxes_global_disruption and clean_hypothesis_refuted)
    return (decoupled, cereb_local_all, cereb_top3_all, cereb_off_lt_own_all,
            top_disruptor_is_local_at_moderate, clean_hypothesis_refuted,
            reach_hub_drive_invariant, reach_hub_per_severity, reach_dump)


def _minority_hub_class(sf):
    """L4: the diaschisis set is a coherent minority relay-hub class -- the E1.3 relay set AND the
    off-target-dominant set (L2), a strict minority (local deficit the default), decoupled from the
    global-reach hub. Convergence holds across the moderate-to-severe sweep."""
    invariant, diaschisis, local, is_relay_set, _, _, _ = _partition(sf)
    n_diaschisis = len(diaschisis)
    is_minority = bool(n_diaschisis < N - n_diaschisis)        # diaschisis is the strict minority
    local_is_default = bool(len(local) > n_diaschisis)
    # the diaschisis set is the off-target-dominant set (L2 equivalence) at the representative depth
    od_set = sorted([REGS[t] for t in range(N) if _footprint(sf, t, REP)[1] > _footprint(sf, t, REP)[0]])
    diaschisis_eq_off_target = bool(od_set == diaschisis)
    # decoupled from the global-reach hub: at moderate severity the top global disruptor (cerebellum)
    # is a LOCAL-deficit lesion, NOT in the diaschisis set -- the L3 decoupling
    decoupled_from_reach_hub = bool(REGS[CEREB] not in diaschisis
                                    and int(np.argmax([sf.reach(t, REP) for t in range(N)])) not in (HIPPO, MIDB))
    coherent_class = bool(is_relay_set and diaschisis_eq_off_target and is_minority
                          and local_is_default and decoupled_from_reach_hub)
    return (coherent_class, diaschisis, n_diaschisis, is_minority, local_is_default,
            decoupled_from_reach_hub, diaschisis_eq_off_target)


def _invariance(sf):
    """S5: a zero lesion (no node silenced) reproduces the frozen M9 anchor R bit-for-bit and the
    per-node field equals the baseline exactly -- the lesion-field reads are a pure structural read
    on the frozen kernel (no new mechanism/measurement/constant)."""
    R_direct = E._integrate(OMEGA, W0, KAP * OMEGA0)[0]          # frozen M9 anchor (engine)
    Rb, cb = sf.drive(np.zeros(N))                               # zero lesion (off-state)
    matches_anchor = bool(R_direct == M9_ANCHOR_R)
    offstate_matches = bool(Rb == R_direct)
    field_matches = bool(np.array_equal(cb, sf.c0))
    baseline_matches = bool(sf.R0 == M9_ANCHOR_R)
    return R_direct, Rb, matches_anchor, offstate_matches, field_matches, baseline_matches


def run():
    sf = SpatialField()

    # ===== L1 : the local-deficit/remote-diaschisis partition, drive-invariant =====
    (part_inv, diaschisis, local, is_relay_set, part_labelled,
     mild_diaschisis, thal_enters_mild) = _partition(sf)
    L1 = bool(part_inv and is_relay_set)

    # ===== L2 : remote diaschisis = off-target dominance =====
    od_equiv, od_per_site = _off_target_dominance(sf)
    L2 = bool(od_equiv)

    # ===== L3 : global-coordination disruption != remote diaschisis (honest negative) =====
    (decoupled, cereb_local_all, cereb_top3_all, cereb_off_lt_own_all,
     top_local_moderate, clean_refuted, reach_hub_invariant,
     reach_hub_per_sev, reach_dump) = _disruption_is_not_diaschisis(sf)
    L3 = bool(decoupled)

    # ===== L4 : the diaschisis set is a coherent minority relay-hub class =====
    (coherent, d4, n_d, is_min, local_default, disjoint, d_eq_od) = _minority_hub_class(sf)
    L4 = bool(coherent)

    # ===== S5 : engine-invariance guard =====
    Rinv, Roff, anchor_ok, off_ok, field_ok, base_ok = _invariance(sf)
    S5 = bool(anchor_ok and off_ok and field_ok and base_ok)

    preds = {
        "L1_lesion_partition_drive_invariant":   "CONFIRMED" if L1 else "REFUTED",
        "L2_diaschisis_is_off_target_dominance": "CONFIRMED" if L2 else "REFUTED",
        "L3_disruption_not_diaschisis":          "CONFIRMED" if L3 else "REFUTED",
        "L4_diaschisis_minority_relay_hub_class":"CONFIRMED" if L4 else "REFUTED",
    }

    res = {
        "_what": "LESION-E1 -- stroke / lesion field: local deficit vs remote diaschisis. The "
                 "SECOND region-specific application of the E1 spatial-localisation layer (§43) and "
                 "the spatial sibling of the §44 focal-epilepsy application. §44 drove a region with "
                 "a focal EXCITATORY (ictal) bias; this module SILENCES a region with a focal "
                 "INHIBITORY (lesion) bias -- a stroke -- and asks whether the deficit stays LOCAL "
                 "(a focal deficit) or disrupts circuits FAR from the lesion (DIASCHISIS), and "
                 "whether remote diaschisis is the same thing as collapsing GLOBAL coordination. "
                 "The lesion is a SILENCING bias on the frozen kernel, NOT a node deletion (which "
                 "would break the kernel freeze) -- the handover's explicit lesion-modelling "
                 "directive. This module IMPORTS the E1 SpatialField (it does NOT re-derive the "
                 "kernel or coupling map). Four sign-only results: L1 the local-deficit/remote-"
                 "diaschisis partition is drive-invariant over the moderate-to-severe core (the "
                 "diaschisis set {hippocampus, midbrain} = the E1.3 relay set, fixed across the "
                 "lesion-severity sweep -- whether a focal lesion stays local or causes remote "
                 "diaschisis is a property of lesion LOCATION; the thalamus enters only at the mild "
                 "sub-floor severity, reported honestly); L2 remote diaschisis is off-target "
                 "dominance (the deficit lands harder on distal circuits than at the lesion -- the "
                 "structural content of diaschisis); L3 (honest negative) global-coordination "
                 "disruption is NOT remote diaschisis (the largest global disruptor is the LOCAL-"
                 "deficit cerebellum, a top-3 global disruptor at every severity yet causing no "
                 "diaschisis -- two distinct decoupled axes, the E1.4 lesson for stroke; the reach "
                 "hub itself is not drive-invariant, an honest contrast with §44); L4 the diaschisis "
                 "set is a coherent minority relay-hub class (local deficit is the structural "
                 "default, remote diaschisis the exception carried by specific relay hubs). "
                 "MECHANISM only -- a local/diaschisis class is a STRUCTURAL spatial quantity, NOT a "
                 "felt deficit, NOT a real lesion/perfusion/connectome map, NOT a clinical "
                 "prediction of which lesions cause remote dysfunction, and NOT prognostic or "
                 "rehabilitation guidance. efficacy=0; not medical advice.",
        "roadmap_id": "E1 region-specific application #2 (stroke/lesion field), the spatial sibling "
                      "of the §44 focal-epilepsy application; the second application of the E1.3 "
                      "self/relay map named owed by §43; RESEARCH_ROADMAP_post_autism_adhd.md",
        "application_of_E1": {
            "E1_supplied": "the E1.3 SELF-LOCALISING vs RELAY classification (drive-invariant, relay "
                           "set {hippocampus, midbrain}) and the E1.2 heterogeneous global reach with "
                           "a drive-stable hub for moderate-to-high drive -- a fixed spatial MAP of "
                           "the frozen kernel, here READ under a SILENCING (lesion) bias",
            "this_module_reads": "which lesions CONTAIN their deficit (stay local) and which cause "
                                 "REMOTE DIASCHISIS, and tests whether remote diaschisis coincides "
                                 "with collapsing GLOBAL coordination -- it finds it does NOT (L3), so "
                                 "remote dysfunction is site-determined, exactly the region-specific "
                                 "reading E1.4 demanded",
            "reuse_discipline": "imports SpatialField; does NOT re-derive the ephaptic kernel W0 or "
                                "the k(b) coupling map; the lesion is a SILENCING bias on the frozen "
                                "kernel, NEVER a node deletion; engine emerged READ-ONLY, byte-unchanged",
            "sibling_with_sec44": "§44 drove a focal EXCITATORY (ictal) bias and read containment vs "
                                  "secondary generalisation; §45 silences with a focal INHIBITORY "
                                  "(lesion) bias and reads local deficit vs remote diaschisis -- the "
                                  "excitatory and inhibitory faces of the same E1 self/relay map, both "
                                  "finding the off-target axis decoupled from the global axis (L3/F3)",
            "severity_floor_inherited": "the moderate-to-severe severity floor |b0|>=0.5 is INHERITED "
                                        "from E1.2 (which certified reach-ranking invariance only for "
                                        "b0>=0.5), a principled reuse of the layer's own invariance "
                                        "scope -- NOT a tuned choice; the mild -0.3 probe is reported "
                                        "honestly to show why the scope is needed",
        },
        "lesion_model": {
            "form": "a focal lesion = a strong focal INHIBITORY (silencing) bias at one region (the "
                    "rest at baseline), via the SAME k = kappa/(1+|b|) [inhib] map as the SZ/epilepsy/"
                    "E1 modules (no new constant); the lesioned node is SILENCED, NOT deleted, so the "
                    "frozen kernel is reused intact; lesion severity b0 swept over {-0.5,-0.7,-0.9}",
            "form_grade": "[F] forced -- the frozen ephaptic kernel W0 plus the existing k(b) map; "
                          "no free constant; a zero lesion reproduces the scalar engine bit-for-bit",
            "lesion_severity_sweep": list(LESION_DEPTHS),
            "mild_subfloor_probe": MILD_DEPTH,
            "representative_severity": REP,
            "profile_grade": "[O] swept -- the lesion severity is a SWEEP, not a tuned constant; every "
                             "SIGN/STRUCTURE holds across the moderate-to-severe sweep",
            "node_not_deleted": "the lesion is a SILENCING inhibitory bias on the frozen kernel, NEVER "
                                "a node deletion -- deleting a node would break the frozen W0 and "
                                "forfeit kernel reuse (handover's explicit lesion-modelling directive)",
            "reused_constants": {"kappa_measured": round(KAP, 6), "R19_fold_spinodal": round(FOLD, 6),
                                 "n_regions": N, "baseline_R0_M9_anchor": round(sf.R0, 10)},
        },
        "L1_lesion_partition": {
            "partition_drive_invariant": part_inv,
            "diaschisis_set": diaschisis,
            "diaschisis_set_is_E1_relay_set": is_relay_set,
            "local_set": local,
            "partition_per_severity": part_labelled,
            "mild_subfloor_diaschisis_set": mild_diaschisis,
            "thalamus_enters_at_mild_severity": thal_enters_mild,
            "reproduced": L1,
            "reading": "silencing each region as a focal lesion, the 12 lesions partition into "
                       "LOCAL-DEFICIT (self-localising -- the coherence deficit concentrates at the "
                       "lesion, a focal deficit) and REMOTE-DIASCHISIS (relay -- the deficit lands "
                       "harder off-target, the lesion disrupts distal circuits). The partition is "
                       "IDENTICAL across the moderate-to-severe lesion-severity sweep, the diaschisis "
                       "set {hippocampus, midbrain} fixed at every severity and equal to the E1.3 "
                       "relay set. Whether a focal lesion stays local or causes remote diaschisis is "
                       "a fixed property of lesion LOCATION, not of lesion severity. HONESTLY, at the "
                       "mild sub-floor severity -0.3 (below the E1.2 |b|>=0.5 invariance floor) the "
                       "thalamus also relays, which is exactly why the invariant claim is scoped to "
                       "the moderate-to-severe core (inheriting the E1.2 floor). Inherits the E1.3 "
                       "self/relay class read on a silencing bias; structure-only.",
        },
        "L2_off_target_dominance": {
            "diaschisis_iff_off_target_dominant_all_severities": od_equiv,
            "per_site_at_representative_severity": od_per_site,
            "reproduced": L2,
            "reading": "for a DIASCHISIS lesion the coherence deficit lands HARDER on distal circuits "
                       "than at the lesion itself (mean off-target |dc| > own |dc|, ratio > 1 -- the "
                       "hippocampus ~1.2x, the midbrain ~3.0x at the representative severity) -- the "
                       "structural signature of remote dysfunction beyond the lesion; for a LOCAL-"
                       "deficit lesion it concentrates at the lesion (ratio < 1 -- the cerebellum "
                       "~0.06x, an overwhelmingly focal deficit). The diaschisis <-> (off/own > 1) "
                       "equivalence holds at every swept severity, tying 'diaschisis' to its clinical "
                       "meaning. Sign-only; magnitudes [O].",
        },
        "L3_disruption_not_diaschisis": {
            "_what": "the honest no-tuning result -- a clean hypothesis ('the lesions that most "
                     "disrupt GLOBAL coordination are exactly the remote-diaschisis lesions') tested "
                     "and FOUND FALSE",
            "local_lesion_maxes_global_disruption": bool(cereb_local_all and cereb_top3_all
                                                         and cereb_off_lt_own_all and top_local_moderate),
            "cerebellum_is_local_deficit_all_severities": cereb_local_all,
            "cerebellum_is_top3_global_disruptor_all_severities": cereb_top3_all,
            "cerebellum_off_over_own_below_1_all_severities": cereb_off_lt_own_all,
            "top_global_disruptor_is_local_at_moderate_severities": top_local_moderate,
            "clean_hypothesis_refuted": clean_refuted,
            "reach_hub_drive_invariant": reach_hub_invariant,
            "global_reach_hub_per_severity": reach_hub_per_sev,
            "reach_per_severity": reach_dump,
            "two_axes_decoupled": decoupled,
            "reproduced": L3,
            "verdict": "the lesions that most disrupt GLOBAL coordination are NOT the remote-"
                       "diaschisis lesions: the single largest global disruptor is the CEREBELLUM, a "
                       "LOCAL-deficit lesion, at the representative moderate severities (rank-1 at "
                       "-0.5 and -0.7), and the cerebellum is a top-3 global disruptor at EVERY "
                       "severity while producing NO diaschisis (LOCAL class, off/own < 1, at every "
                       "severity) -- a lesion can max global disruption while being maximally local. "
                       "Global-coordination disruption (reach) and remote diaschisis (off-target "
                       "deficit) are TWO DISTINCT, decoupled spatial properties; which sites cause "
                       "remote dysfunction is SITE-DETERMINED, not reducible to a 'global impact = "
                       "diaschisis' rule. An HONEST contrast with §44: unlike the ictal case (where "
                       "the cerebellum topped the reach ranking at EVERY intensity), the lesion "
                       "global-reach hub is itself NOT drive-invariant -- it is the contained "
                       "cerebellum at -0.5 and -0.7 but the remote midbrain at -0.9 -- so the very "
                       "ranking shifts with severity; the decoupling is carried by the cerebellum "
                       "being LOCAL-yet-top-reach across all severities. The refuted clean hypothesis "
                       "is reported honestly -- the E1.4 lesson made concrete for stroke/lesion. A "
                       "refuted clean hypothesis is a finding.",
        },
        "L4_diaschisis_minority_relay_hub_class": {
            "diaschisis_set": d4,
            "n_diaschisis": n_d,
            "diaschisis_is_strict_minority": is_min,
            "local_deficit_is_structural_default": local_default,
            "diaschisis_equals_off_target_dominant_set": d_eq_od,
            "decoupled_from_global_reach_hub": disjoint,
            "coherent_minority_relay_hub_class": coherent,
            "reproduced": L4,
            "clinical_correspondence_grade": "[L] direction-only",
            "clinical_correspondence": "a DIRECTION-ONLY cited correspondence, never a magnitude or a "
                                       "prediction: clinically most focal lesions produce focal "
                                       "deficits, while diaschisis (remote dysfunction after focal "
                                       "injury -- e.g. crossed cerebellar diaschisis, thalamic/limbic "
                                       "remote effects, von Monakow's classical concept) is the "
                                       "recognised EXCEPTION at specific connected hubs -- consistent "
                                       "with the diaschisis set being a strict minority of relay hubs "
                                       "and with local deficit being the structural majority. NOT a "
                                       "patient-level prediction.",
            "reading": "the two diaschisis lesions {hippocampus, midbrain} are simultaneously the "
                       "E1.3 relay set AND the off-target-dominant set (L2), a STRICT MINORITY (2 of "
                       "12 -- local deficit is the structural default), AND decoupled from the global-"
                       "reach hub (the local cerebellum at moderate severity) -- one coherent class "
                       "of limbic/brainstem relay hubs. Remote diaschisis is structurally the "
                       "EXCEPTION carried by specific relay hubs, not a generic property of lesions. "
                       "Structure-only; the clinical correspondence is [L] direction-only.",
        },
        "S5_engine_invariance_guard": {
            "_what": "a zero lesion (no node silenced) reproduces the frozen M9 coordination anchor "
                     "bit-for-bit and the per-node field equals the baseline exactly -- the lesion-"
                     "field reads are a pure structural read on the frozen kernel (no new mechanism)",
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
                "this module shapes a focal SILENCING (lesion) bias on the frozen kernel, it does not "
                "re-derive it",
            "epilepsy_sibling_cited": "§44 (the first E1 application) drove a focal EXCITATORY (ictal) "
                "bias and read containment vs secondary generalisation; §45 silences with a focal "
                "INHIBITORY (lesion) bias and reads local deficit vs remote diaschisis -- the same "
                "self/relay map read in its two faces, both finding the off-target axis decoupled from "
                "the global axis (L3 mirrors F3)",
            "partition_is_position_LOCK": "whether a focal lesion stays local or causes remote "
                "diaschisis is a fixed property of lesion LOCATION (the E1.3 relay class), drive-"
                "invariant over the moderate-to-severe core -- structure, not a fitted result",
            "no_universal_disruption_law_LOCK": "global-coordination disruption is NOT remote "
                "diaschisis; the clean 'global impact = diaschisis' hypothesis is explicitly refuted, "
                "not forced -- remote dysfunction is site-determined (the E1.4 lesson for stroke)",
            "severity_floor_LOCK": "the |b0|>=0.5 moderate-to-severe scope is inherited from E1.2's "
                "own reach-ranking invariance floor, NOT a tuned choice; the mild -0.3 sub-floor probe "
                "(where the thalamus also relays) is reported honestly to show why the scope is needed",
            "real_lesions_heterogeneous_LOCK": "real lesion consequences are HETEROGENEOUS (the "
                "vascular territory, white-matter tractography, the individual connectome, oedema, "
                "penumbra and reorganisation); this module asserts the SIGN/STRUCTURE of a focal "
                "silencing bias on the FROZEN kernel, not that any real lesion follows it",
            "not_clinical_LOCK": "nothing here is a real lesion, a perfusion/diffusion map, a real "
                "connectome, a diaschisis measurement, a prediction of which patient's lesion causes "
                "remote dysfunction, or prognostic/rehabilitation guidance; localisation and prognosis "
                "are external clinical decisions",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; whether "
                "any real lesion stays local or causes diaschisis by this structure is external",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "spatial_quantities_are_structural": 1.0,
            "reuses_E1_spatial_field": 1.0,
            "lesion_is_silencing_bias_not_deletion": 1.0,
            "lesion_severity": "OPEN [O] -- swept; signs/structure hold over the moderate-to-severe "
                               "lesion-severity sweep, not tuned",
            "severity_floor_inherited_not_tuned": "the |b0|>=0.5 scope is inherited from E1.2, not a "
                                                  "tuned choice; the mild sub-floor probe is reported "
                                                  "honestly",
            "clean_hypothesis_refuted": "L3 reports a REFUTED clean hypothesis honestly (global-"
                                        "coordination disruption is NOT remote diaschisis) rather than "
                                        "forcing a single-axis 'global impact = diaschisis' narrative",
            "clinical_prediction": "NONE -- no patient-level prediction of which lesion causes remote "
                                   "dysfunction, no localisation, no prognosis; the only clinical "
                                   "correspondence (L4) is [L] direction-only",
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
            "L1_lesion_partition_drive_invariant": {
                "claim": "silencing each region as a focal lesion, the local-deficit/remote-diaschisis "
                         "partition is identical across the moderate-to-severe lesion-severity sweep "
                         "and the diaschisis (relay) set is {hippocampus, midbrain} = the E1.3 relay "
                         "set at every severity",
                "status": preds["L1_lesion_partition_drive_invariant"]},
            "L2_diaschisis_is_off_target_dominance": {
                "claim": "a lesion is diaschisis IFF its coherence deficit lands harder off-target "
                         "than at the lesion (mean off-target |dc| > own |dc|), at every swept severity",
                "status": preds["L2_diaschisis_is_off_target_dominance"]},
            "L3_disruption_not_diaschisis": {
                "claim": "global-coordination disruption is NOT remote diaschisis: the largest global "
                         "disruptor is the LOCAL-deficit cerebellum (a top-3 global disruptor at every "
                         "severity yet causing no diaschisis), so the two are decoupled axes; the clean "
                         "'global impact = diaschisis' hypothesis is refuted",
                "status": preds["L3_disruption_not_diaschisis"]},
            "L4_diaschisis_minority_relay_hub_class": {
                "claim": "the diaschisis set is the E1.3 relay set AND the off-target-dominant set, a "
                         "strict minority (local deficit the default), decoupled from the global-reach "
                         "hub -- one coherent minority relay-hub class",
                "status": preds["L4_diaschisis_minority_relay_hub_class"]},
        },
        "overall": {
            "lesion_partition_drive_invariant": L1,
            "diaschisis_is_off_target_dominance": L2,
            "disruption_not_diaschisis": L3,
            "diaschisis_minority_relay_hub_class": L4,
            "engine_invariance_guard": S5,
            "is_full_module": bool(L1 and L2 and L3 and L4 and S5),
            "verdict": "stroke/lesion field -- local deficit vs remote diaschisis -- the second "
                       "region-specific application of the E1 spatial-localisation layer and the "
                       "spatial sibling of §44 focal epilepsy. Silencing each region as a focal lesion "
                       "(a strong inhibitory bias, NOT a node deletion), the local-deficit/remote-"
                       "diaschisis partition is DRIVE-INVARIANT over the moderate-to-severe core, the "
                       "diaschisis (remote-disruption) set {hippocampus, midbrain} = the E1.3 relay "
                       "set, fixed at every severity (L1; the thalamus enters only at the mild sub-"
                       "floor severity, reported honestly); diaschisis IS off-target dominance, the "
                       "structural content of remote dysfunction (L2); global-coordination disruption "
                       "is NOT remote diaschisis -- the largest global disruptor is the LOCAL-deficit "
                       "cerebellum (a top-3 global disruptor at every severity yet causing no "
                       "diaschisis), so the two are distinct decoupled axes (L3, the honest no-tuning "
                       "result, the E1.4 lesson for stroke; the reach hub itself is not drive-"
                       "invariant, an honest contrast with §44); and the diaschisis set is a coherent "
                       "minority relay-hub class, local deficit the structural default (L4). A zero "
                       "lesion reproduces the frozen M9 anchor bit-for-bit (S5). The lesion form is "
                       "forced, the severity swept, every sign survives the sweep, no new tuned "
                       "constant, engine byte-unchanged; the SpatialField is imported, not re-derived, "
                       "and the lesion is a silencing bias, never a node deletion. Axis-A firewall: a "
                       "local/diaschisis class is a structural spatial quantity, NOT a felt deficit, "
                       "NOT a real lesion/perfusion/connectome map, NOT a prediction of which lesions "
                       "cause remote dysfunction, NOT prognostic or rehabilitation guidance. "
                       "efficacy=0; not medical advice.",
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

def lesion_field_diaschisis_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "lesion_field_diaschisis_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_lesion_field_diaschisis_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"lesion_field_diaschisis_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = lesion_field_diaschisis_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    m = res["lesion_model"]
    l1 = res["L1_lesion_partition"]; l2 = res["L2_off_target_dominance"]
    l3 = res["L3_disruption_not_diaschisis"]; l4 = res["L4_diaschisis_minority_relay_hub_class"]
    g = res["S5_engine_invariance_guard"]
    print("=" * 78)
    print("LESION-E1 -- STROKE/LESION FIELD: LOCAL DEFICIT vs REMOTE DIASCHISIS (E1 application #2)")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  lesion model: focal silencing bias (not deletion); severity sweep={m['lesion_severity_sweep']}  form={m['form_grade'][:18]}")
    print("-" * 78)
    print(f"  L1 partition     : drive-invariant={l1['partition_drive_invariant']}  diaschisis(relay) set={l1['diaschisis_set']}  (mild -0.3 adds thalamus={l1['thalamus_enters_at_mild_severity']})")
    print(f"  L2 off-target    : diaschisis<->off>own (all severities)={l2['diaschisis_iff_off_target_dominant_all_severities']}")
    print(f"  L3 NOT diaschisis: local cerebellum top-3 reach all={l3['cerebellum_is_top3_global_disruptor_all_severities']}  clean-hyp refuted={l3['clean_hypothesis_refuted']}  reach-hub drive-invariant={l3['reach_hub_drive_invariant']}  -> decoupled={l3['two_axes_decoupled']}")
    print(f"  L4 minority hub  : diaschisis={l4['diaschisis_set']} n={l4['n_diaschisis']}  minority={l4['diaschisis_is_strict_minority']}  decoupled-from-reach-hub={l4['decoupled_from_global_reach_hub']}  -> coherent={l4['coherent_minority_relay_hub_class']}")
    print(f"  S5 invariance    : off-state R={g['offstate_R']}  ==anchor:{g['matches_frozen_anchor_bitwise'] and g['offstate_matches_direct_bitwise']}  field==baseline:{g['offstate_field_equals_baseline']}")
    print("-" * 78)
    print(f"  reach hub per severity: {l3['global_reach_hub_per_severity']}")
    print(f"  pre-registered: {[ (k, v['status']) for k,v in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  LESION-FIELD SPATIAL MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
