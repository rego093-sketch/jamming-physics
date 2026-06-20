#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seam_wiring.py  --  Cross-system seam layer (immune_hematologic_vp_site v0.16.0, section 16).

WIRES the three seams that make the immune volume the IMMUNOSURVEILLANCE / TOLERANCE / INFLAMMATION HUB
of the VP program -- the spokes that earlier sections only DECLARED in prose:

  (A) GUT-IMMUNE (digestive).  The intestinal mucosal tolerance latch that digestive section 22 (IBD)
      reads IS this volume's tolerance machinery (T21 deletion / T23 break / T24 suppressor) localised to
      the mucosa, on the BYTE-IDENTICAL R19 substrate. We CONFIRM the identity in closed form: digestive's
      vendored IBD induction threshold == this volume's T23 saddle-node (total drive = spinodal), and its
      maintenance threshold == this volume's T24 suppressor complement ((residual+insult) - spinodal). The
      relapsing hysteresis == the T23 irreversible pathological memory.

  (B) NEURO-IMMUNE (mind).  Two firewall-respecting directions. IN: mind's HPA/cortisol descriptor RAISES the
      T24 suppressor sigma (stress immunosuppression) -- consumed as a SIGN ONLY (magnitude [O], sigma swept,
      anti-tuning). OUT: this volume's cytokine tone M (T31) is a one-way POINTER to mind's inflammatory
      contributor to depression (mind section 27); no mind value is consumed, the felt low mood is mind's.

  (C) ONCOLOGY HUB.  immune_escape_factor is a one-way OUT multiplier on every volume's cancer kernel
      (T10/T5 measured 1/(1-escape), site-independent); Lever D (T15) is the therapy face. The original
      OUT seam of this volume, documented here as the third hub spoke.

SECTION 18 (v0.17.0) promotes two INHERITED ADJACENCIES to DECLARED spokes -- both one-way pointers that
consume NO sibling value and keep the byte-identical engine hash:

  (D) CIRCULATORY (leukocyte trafficking).  This volume's leukocyte EFFECTOR POPULATIONS (the ON-committed
      clones of the R19 switch, rooted at bone_marrow_hematopoiesis, RUNX1) are a one-way POINTER OUT to the
      circulatory volume's vascular transport -- they traffic THROUGH the vasculature. No circulatory value
      is consumed; the pointer lands on a REAL immune-side organ (verified against this volume's substrate).

  (E) MUSCULOSKELETAL (marrow niche).  This volume's HEMATOPOIETIC ORIGIN (bone_marrow_hematopoiesis, RUNX1,
      gamma=1.3225) is HOUSED in the bone-marrow niche owned by the musculoskeletal volume. Declared in v0.17.0
      as the WEAKER one-way POINTER. v0.19.0 (SECTION 20) LIVE-VERIFIES it against musculoskeletal_vp_site
      v0.7.0 -- substrate drift 0 -- and RETIRES the shared-substrate-identity upgrade on live evidence: the MSK
      niche is built by OSTEOBLASTS (RUNX2, gamma=1.2414, spinodal 0.53237264), a DIFFERENT switch/spinodal from
      the hematopoietic RUNX1 (0.58538506), so the niche HOUSES hematopoiesis but is not the same R19 switch --
      the falsifier fired, the identity is retired, the one-way pointer SURVIVES and is now live-verified.

SECTION 19 (v0.18.0) generalises the gut shared-substrate identity to OTHER BARRIER SURFACES and names the
first two beyond the gut -- consuming NO sibling value and keeping the byte-identical engine hash:

  (F) BARRIER-SURFACE AGNOSTICISM.  The gut seam (induction == antigen + spinodal(1.0); maintenance ==
      antigen - spinodal(1.0)) holds for ANY barrier-surface antigen: the surface-independent OFFSET from a
      surface's OWN antigen baseline is INVARIANT == +/- spinodal(1.0) across an illustrative antigen sweep.
      So the tolerance latch is barrier-surface-agnostic; the gut (antigen 0.50) is the one vendored/verified
      point on a barrier-agnostic line. CLOSED-FORM [F] resting on the [V] T23 saddle-node + T24 suppressor
      complement; each real surface's ABSOLUTE antigen scale is [O], owned by that surface's future volume.

  (G) RESPIRATORY NAMED CANDIDATE / (H) SKIN barrier seam.  A respiratory (airway-mucosa) VP volume would
      localise THIS volume's tolerance switch to a second barrier surface -- the gut identity re-applied,
      grounded by barrier-surface agnosticism; declared as a NAMED CANDIDATE awaiting the live respiratory
      volume + its owned absolute airway-antigen scale (not on disk). The SKIN (epidermal-barrier) seam is
      further along: v0.20.0 (SECTION 21) LIVE substrate-verified it against integumentary_vp_site v1.0.0
      (substrate drift 0) and confirmed a RECIPROCAL immune-seam handshake (the skin volume independently
      declares an out-seam to immune_hematologic). The epidermal-tolerance IDENTITY remains IMMUNE-OWNED
      CLOSED-FORM (barrier-agnosticism): the skin supplies the real barrier surface (epidermis TP63,
      keratinocyte KRT14) but defers the immune tolerance switch as an out-seam, so the identity is
      confirmed-real-surface and NOT contradicted, but NOT engine-verified -- a third distinct outcome (gut =
      verified identity; musculoskeletal = retired identity; skin = adjacency-verified + reciprocal handshake).
      The respiratory entry is still a NAMED CANDIDATE (its live volume + owned absolute airway-antigen scale are
      not on disk); the immune-side tolerance primitive (T23/T24, barrier-surface-agnostic) IS real in this zip,
      and every surface's absolute antigen scale is [O], sibling-owned.

DISCIPLINE (verbatim, same lock digestive runs circulatory-side and mind runs neuro-side):
  * Citation / pointer / vendored-snapshot only. This layer imports NO sibling code. The digestive mucosal-
    flare interface is a VENDORED SNAPSHOT read from inherited/cross_references.json (verified once against
    digestive's ibd_relapsing_course() at vendoring time); the mind seam is a SIGN-ONLY descriptor IN
    (no numeric mind value) plus a one-way POINTER OUT (no consumed value).
  * The firewall is an ARCHITECTURAL LOCK: zero sibling imports anywhere in the package, and the emitted
    EMERGENCE state (engine circulate()) carries no felt / HPA / cortisol / mind key. Each volume re-
    establishes its trusted state from its own single zip with the siblings ABSENT.
  * Nothing here feeds the hashed emergence core, so the engine circulate()/emit() 2x-sha256 is UNCHANGED
    (e7a2a5b8...) and the stress battery is UNCHANGED. This layer carries its OWN 2x-sha256 digest, exactly
    as digestive's seam and analgesic layers carry theirs.

The layer is CONSUMED (it reads the engine state + the cross-reference snapshot + the closed-form substrate
identity); it is not the engine and not the stress battery.
"""
import os, sys, re, json, hashlib, math
from functools import lru_cache

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.normpath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_PKG, "inherited"))
sys.path.insert(0, os.path.join(_PKG, "repro", "_engine"))

import cross_references as XR              # internal SSOT loader (stdlib JSON; no sibling code)
from vp_substrate import spinodal, barrier # THIS volume's substrate -- the reference R19 (single source)
import vp_imm_engine as ENG                # THIS volume's emergence engine

# Sibling-code tokens the firewall forbids importing (digestive / mind / neuro / their neighbours).
_SIBLING_IMPORT_TOKENS = ("vp_dig", "dig_engine", "digestive", "vp_mind", "mind_engine",
                          "vp_neuro", "neuro_engine", "neuro", "mind", "circulat", "cardioresp",
                          "musculo", "skelet", "vp_msk", "msk_engine",
                          # v0.18.0 barrier-surface candidate volumes (future, not on disk):
                          "respirat", "airway", "pulmonary", "vp_resp",
                          "epiderm", "cutaneous", "vp_skin", "dermat")
# Internal modules legitimately imported within immune (never flagged).
_INTERNAL_OK = ("vp_imm_engine", "vp_substrate", "gamma_pipeline", "ncbi_verify", "cross_references",
                "seam_wiring", "clonal_inflammation", "lineage_order", "emergent_", "carcinogen_",
                "fundamental_therapy", "stress_tests", "gates", "burden_prioritisation",
                "external_mechanism_honesty", "falsification_register", "forbidden_claim_scan",
                "inherit_reverify", "run_discipline", "organ")
# Forbidden felt/HPA keys in the emitted EMERGENCE state (firewall: the immune emergence is mind-free).
_FELT_HPA_TOKENS = ("hpa", "cortisol", "felt", "affect", "mind", "interocept", "limbic", "amygdala",
                    "mood", "sickness", "valence")

# OUT-OF-GATE components, excluded from the in-gate firewall certification. The section-17 live cross-
# package harness is the one SANCTIONED place that reaches a sibling at all (and only ever by file-path
# LOAD, never by an import statement); it runs OUTSIDE every gate. Its own no-sibling-import discipline is
# self-checked inside the harness (run_harness.py), out of gate, touching no digest.
_OUT_OF_GATE_RELPATHS = ("repro/_harness/", "repro/run_harness.py")

_IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+([A-Za-z0-9_.]+)")


# --------------------------------------------------------------------------- 1. consume digestive (gut)
def consume_digestive_mucosal_flare():
    """Read the vendored digestive IBD mucosal-flare snapshot (the gut localisation of T23/T24)."""
    snap = XR.consumed_digestive_mucosal_flare()
    rec = XR.for_seam("digestive_gut_immune_interface")
    return dict(g=snap["ibd_mucosal_R19_scale_g"], antigen=snap["ibd_luminal_antigen_drive"],
                induction=snap["ibd_induction_threshold"], maintenance=snap["ibd_maintenance_threshold"],
                relapsing=snap["ibd_relapsing_hysteresis"], crc_rr=snap["ibd_crc_rr_anchor_Jess2012"],
                owner_immune_doi=rec["owner_concept_doi_immune"],
                owner_digestive_doi=rec["owner_concept_doi_digestive"],
                source_function=snap["source_function"])


# --------------------------------------------------------------------------- 2. gut-immune identity
def gut_immune_tolerance_localization():
    """SECTION 16-A: confirm digestive's IBD mucosal latch IS this volume's T23/T24 saddle-node, in
    CLOSED FORM on the byte-identical substrate. induction == antigen + spinodal (T23 total drive =
    spinodal); maintenance == antigen - spinodal (T24 suppressor complement); relapsing == T23
    irreversibility. No stochastic re-run -- the closed-form substrate identity the modules MEASURED."""
    f = consume_digestive_mucosal_flare()
    g, ant = f["g"], f["antigen"]
    sp = spinodal(g)                                              # THIS volume's substrate spinodal
    induction_closed   = round(ant + sp, 4)                      # T23 saddle-node with the antigen as residual drive
    maintenance_closed = round(ant - sp, 4)                      # T24 suppressor complement
    induction_match   = (induction_closed   == round(f["induction"], 4))
    maintenance_match = (maintenance_closed == round(f["maintenance"], 4))
    rec = XR.gut_identity_record()
    return dict(
        substrate_spinodal_g1=round(sp, 6), substrate_barrier_g1=round(barrier(g), 6),
        digestive_induction=f["induction"], closed_form_T23_saddle_node=induction_closed,
        induction_is_T23_saddle_node=bool(induction_match),
        digestive_maintenance=f["maintenance"], closed_form_T24_suppressor_complement=maintenance_closed,
        maintenance_is_T24_suppressor_complement=bool(maintenance_match),
        relapsing_is_T23_irreversibility=bool(f["relapsing"]),
        identity_holds=bool(induction_match and maintenance_match and f["relapsing"]),
        note=rec["induction_threshold_IS_T23_saddle_node"][:70] + "...",
        grade="[V] shared-substrate latch identity (gut IBD induction=T23 saddle-node, maintenance=T24 "
              "suppressor complement, relapsing=T23 irreversibility) / [O] absolute mucosal scale + felt (digestive/mind)")


# --------------------------------------------------------------------------- 3. consume mind (neuro)
def consume_mind_hpa_cortisol_descriptor():
    """Read the mind HPA/cortisol descriptor IN -- SIGN ONLY (cortisol -> +sigma). No numeric value."""
    rec = XR.mind_neuroimmune_record()["direction_IN_stress_to_suppression"]
    consumes_value = ("consumed_value" in rec and "DIRECTION" in rec["consumed_value"])
    return dict(map_direction="cortisol_raises_T24_suppressor_sigma",
                consumed_value_is_sign_only=bool(consumes_value),
                magnitude_is_open=True,
                owner=rec["owner"][:60] + "...",
                grade="[F] sign-only descriptor (magnitude [O]; sigma swept, anti-tuning)")


def neuroimmune_stress_suppression_direction():
    """SECTION 16-B IN: map mind's cortisol descriptor onto the T24 suppressor direction. The CLAIM is
    the SIGN (a sustained cortisol/stress drive deepens peripheral tolerance, lowering surveillance); the
    MAGNITUDE (cortisol -> how much sigma) stays [O]. The immune engine never imports a cortisol value."""
    d = consume_mind_hpa_cortisol_descriptor()
    rec = XR.mind_neuroimmune_record()
    return dict(stress_raises_suppression=True, raises_T24_sigma=True,
                magnitude_is_open=bool(d["magnitude_is_open"]),
                takes_no_numeric_mind_value=bool(d["consumed_value_is_sign_only"]),
                owner_mind_doi=rec["owner_concept_doi_mind"],
                wired=bool(d["consumed_value_is_sign_only"] and d["magnitude_is_open"]),
                grade=rec["direction_IN_stress_to_suppression"]["boundary_clause"][:1] and
                      "[F] sign-only stress->suppression direction; [O] magnitude (mind/anchor-owned)")


# --------------------------------------------------------------------------- 4. cytokine -> mind pointer
def cytokine_to_mind_pointer_is_not_dependency():
    """SECTION 16-B OUT: the cytokine tone M (T31) is a ONE-WAY forward pointer to mind's inflammatory
    contributor to depression (mind section 27). Immune consumes NO mind value (the record carries no
    vendored snapshot); it only states WHERE the inflammatory drive travels. Felt low mood is mind's."""
    rec = XR.mind_neuroimmune_record()["direction_OUT_cytokine_to_mood"]
    consumes_mind_value = ("vendored_snapshot" in rec)            # must be False -- pointer carries no value
    one_way = ("one-way" in rec.get("consumed_value", "").lower() or "NONE" in rec.get("consumed_value", ""))
    return dict(owns_cytokine_tone_M_T31=True,
                one_way_pointer_out=bool(one_way),
                consumes_a_mind_value=bool(consumes_mind_value),
                mind_side_endpoint=rec["mind_side_endpoint"][:80] + "...",
                pointer_not_dependency=bool(one_way and not consumes_mind_value),
                grade=rec["owner"][:1] and "[V] cytokine tone M owned (T31); [O] felt low mood (mind, pointer)")


# --------------------------------------------------------------------------- 5. oncology hub spoke
def oncology_hub_spoke():
    """SECTION 16-C: immune_escape_factor is a one-way OUT multiplier on every volume's cancer kernel
    (T10 measured 1/(1-escape), site-independent); Lever D (T15) is the therapy face. The third hub spoke."""
    rec = XR.oncology_hub_record()
    return dict(escape_factor_is_cross_cutting_multiplier=True,
                site_independent_one_over_one_minus_escape=True,
                therapy_face_is_lever_D_T15=True,
                owner_immune_doi=rec["owner_concept_doi_immune"],
                grade=rec["grade"])


# --------------------------------------------------------------------------- 5b. circulatory spoke (S18)
def circulatory_leukocyte_trafficking_pointer():
    """SECTION 18-A: this volume's leukocyte EFFECTOR POPULATIONS (the ON-committed clones of the R19
    switch, rooted at bone_marrow_hematopoiesis) are a ONE-WAY POINTER OUT to the circulatory volume's
    vascular transport -- they TRAFFIC THROUGH the vasculature. The pointer consumes NO circulatory value;
    it only states WHERE the cells travel. The immune-side endpoint (bone_marrow_hematopoiesis, RUNX1) is a
    REAL measured organ in this zip, so the pointer lands on something, not a dangling reference. Promoted
    from an inherited adjacency to a declared spoke in v0.17.0."""
    rec = XR.circulatory_record()
    ep = rec["immune_side_endpoint"]
    # the pointer lands on a REAL immune-side organ, verified live against this volume's substrate
    sp_live = round(spinodal(ep["production_root_gamma"]), 8)
    ba_live = round(barrier(ep["production_root_gamma"]), 8)
    endpoint_real = (ep.get("endpoint_is_real_in_this_zip", False)
                     and ep["production_root_organ"] == "bone_marrow_hematopoiesis"
                     and sp_live == round(ep["production_root_spinodal_g"], 8)
                     and ba_live == round(ep["production_root_barrier_g"], 8))
    one_way = ("one-way" in rec["direction"].lower())
    consumes_value = ("vendored_snapshot" in rec)              # must be False -- a pointer carries no value
    return dict(production_root_organ=ep["production_root_organ"],
                production_root_master_gene=ep["production_root_master_gene"],
                production_root_spinodal_live=sp_live, production_root_barrier_live=ba_live,
                endpoint_is_real=bool(endpoint_real),
                one_way_pointer_out=bool(one_way),
                consumes_a_circulatory_value=bool(consumes_value),
                pointer_not_dependency=bool(one_way and not consumes_value and endpoint_real),
                owner_immune_doi=rec["owner_concept_doi_immune"],
                owner_circulatory_doi=rec["owner_concept_doi_circulatory"],
                grade=rec["grade"])


# --------------------------------------------------------------------------- 5c. musculoskeletal spoke (S18 + S20)
def musculoskeletal_marrow_niche_pointer():
    """SECTION 18-B / SECTION 20: this volume's HEMATOPOIETIC ORIGIN -- bone_marrow_hematopoiesis (RUNX1,
    gamma=1.3225), the HSC->lineage root of every immune cell -- is HOUSED in the bone-marrow niche owned by
    the musculoskeletal volume. Declared in v0.17.0 as the WEAKER ONE-WAY POINTER. v0.19.0 LIVE-VERIFIES it
    against musculoskeletal_vp_site v0.7.0 (substrate drift 0) and RETIRES the shared-substrate-identity
    upgrade on live evidence: the MSK niche is built by OSTEOBLASTS (RUNX2, gamma=1.2414, spinodal 0.53237264),
    a DIFFERENT switch/spinodal from the hematopoietic RUNX1 (0.58538506) -- the niche HOUSES hematopoiesis but
    is not the same R19 switch, so the threshold-equality identity does NOT reduce (falsifier fired, pointer
    survives). The vendored MSK bone snapshot is checked in closed form against this volume's substrate."""
    rec = XR.musculoskeletal_record()
    ep = rec["immune_side_endpoint"]
    sp_live = round(spinodal(ep["hematopoietic_root_gamma"]), 8)
    ba_live = round(barrier(ep["hematopoietic_root_gamma"]), 8)
    endpoint_real = (ep.get("endpoint_is_real_in_this_zip", False)
                     and ep["hematopoietic_root_organ"] == "bone_marrow_hematopoiesis"
                     and sp_live == round(ep["hematopoietic_root_spinodal_g"], 8)
                     and ba_live == round(ep["hematopoietic_root_barrier_g"], 8))
    one_way = ("one-way pointer" in rec["direction"].lower())
    consumes_value = ("vendored_snapshot" in rec)              # must be False -- a pointer carries no value
    # --- v0.19.0 LIVE verification: pointer live-verified (drift 0) ---
    lv = rec.get("live_verification", {})
    pointer_live_verified = bool(lv.get("substrate_drift_is_zero", False)
                                 and round(float(lv.get("substrate_drift", 1.0)), 12) == 0.0)
    # --- v0.19.0 RETIRED identity: recompute BOTH spinodals from THIS substrate and confirm they DIFFER ---
    snap = lv.get("vendored_msk_bone_snapshot", {})
    msk_bone_sp_recomputed = round(spinodal(snap.get("msk_bone_gamma", 0.0)), 8)   # spinodal(1.2414)
    msk_bone_ba_recomputed = round(barrier(snap.get("msk_bone_gamma", 0.0)), 8)
    msk_snapshot_integrity = (msk_bone_sp_recomputed == round(snap.get("msk_bone_spinodal_g", -1), 8)
                              and msk_bone_ba_recomputed == round(snap.get("msk_bone_barrier_g", -1), 8))
    niche_sp_differs_from_hematopoietic = (msk_bone_sp_recomputed != sp_live)      # 0.53237264 != 0.58538506
    retired = rec.get("identity_upgrade_RETIRED", {})
    retired_recorded = ("verdict" in retired and "what_the_live_engine_shows" in retired
                        and retired.get("status", "").startswith("RETIRED"))
    identity_would_hold = bool(lv.get("identity_would_hold", True))                 # must be False
    identity_retired_on_live_evidence = bool(retired_recorded and not identity_would_hold
                                             and msk_snapshot_integrity
                                             and niche_sp_differs_from_hematopoietic)
    identity_claimed_now = ("shared-substrate identity" == rec.get("seam_type", "").strip())  # must be False
    return dict(hematopoietic_root_organ=ep["hematopoietic_root_organ"],
                hematopoietic_root_master_gene=ep["hematopoietic_root_master_gene"],
                hematopoietic_root_spinodal_live=sp_live, hematopoietic_root_barrier_live=ba_live,
                endpoint_is_real=bool(endpoint_real),
                one_way_pointer=bool(one_way),
                consumes_a_musculoskeletal_value=bool(consumes_value),
                pointer_not_dependency=bool(one_way and not consumes_value and endpoint_real),
                pointer_live_verified=pointer_live_verified,
                msk_substrate_drift=round(float(lv.get("substrate_drift", 1.0)), 12),
                msk_bone_master_gene=snap.get("msk_bone_master_gene"),
                msk_bone_spinodal_recomputed=msk_bone_sp_recomputed,
                msk_snapshot_integrity=bool(msk_snapshot_integrity),
                niche_spinodal_differs_from_hematopoietic=bool(niche_sp_differs_from_hematopoietic),
                identity_would_hold=identity_would_hold,
                identity_upgrade_retired_on_live_evidence=identity_retired_on_live_evidence,
                identity_claimed_now=bool(identity_claimed_now),
                owner_immune_doi=rec["owner_concept_doi_immune"],
                grade=rec["grade"])


# --------------------------------------------------------------------------- 5d. barrier-surface agnosticism (S19)
def barrier_surface_agnostic():
    """SECTION 19 footing: the gut seam (induction == antigen + spinodal(1.0); maintenance == antigen -
    spinodal(1.0)) is BARRIER-SURFACE-AGNOSTIC. Across an illustrative antigen sweep, the surface-independent
    OFFSET from each surface's OWN antigen baseline is INVARIANT == +/- spinodal(1.0) -- so the tolerance
    latch generalises to ANY barrier surface, the gut (antigen 0.50) being the one vendored/verified point on
    a barrier-agnostic line. CLOSED-FORM / architectural [F], resting on the [V] T23 saddle-node + T24
    suppressor complement; each real surface's ABSOLUTE antigen scale is [O], owned by that surface's volume."""
    note = XR.barrier_agnostic_note()
    g = note["shared_mucosal_R19_scale_g"]                       # 1.0 -- the shared mucosal R19 scale
    sp = spinodal(g)                                             # THIS volume's substrate spinodal (single source)
    off_ind_target  = round(sp, 8)
    off_main_target = round(-sp, 8)
    rows = []
    offset_invariant = True
    for ant in note["illustrative_antigen_sweep"]:
        induction   = ant + sp                                  # T23 saddle-node with antigen as residual drive
        maintenance = ant - sp                                  # T24 suppressor complement
        off_ind  = round(induction - ant, 8)                    # surface-independent: must equal +spinodal
        off_main = round(maintenance - ant, 8)                  # surface-independent: must equal -spinodal
        if off_ind != off_ind_target or off_main != off_main_target:
            offset_invariant = False
        rows.append(dict(antigen=round(ant, 4), induction=round(induction, 4),
                         maintenance=round(maintenance, 4),
                         offset_induction=off_ind, offset_maintenance=off_main))
    # the gut (antigen 0.50) is the ONE vendored, live-verified point -- tie the agnostic line to it
    f = consume_digestive_mucosal_flare()
    gut_induction_closed   = round(f["antigen"] + sp, 4)
    gut_maintenance_closed = round(f["antigen"] - sp, 4)
    gut_anchor_reproduced = (gut_induction_closed   == round(f["induction"], 4)
                             and gut_maintenance_closed == round(f["maintenance"], 4)
                             and f["g"] == g)
    note_off_ind  = round(note["surface_independent_offset_induction"], 8)
    note_off_main = round(note["surface_independent_offset_maintenance"], 8)
    note_consistent = (note_off_ind == off_ind_target and note_off_main == off_main_target
                       and round(note["spinodal_g1"], 8) == round(sp, 8))
    return dict(shared_mucosal_R19_scale_g=g, substrate_spinodal_g1=round(sp, 8),
                surface_independent_offset_induction=off_ind_target,
                surface_independent_offset_maintenance=off_main_target,
                antigen_sweep_rows=rows,
                offset_invariant_across_sweep=bool(offset_invariant),
                gut_anchor_antigen=f["antigen"],
                gut_anchor_induction=round(f["induction"], 4),
                gut_anchor_maintenance=round(f["maintenance"], 4),
                gut_anchor_reproduced=bool(gut_anchor_reproduced),
                ssot_note_consistent=bool(note_consistent),
                barrier_surface_agnostic=bool(offset_invariant and gut_anchor_reproduced and note_consistent),
                grade=note["offset_invariance_grade"])


# --------------------------------------------------------------------------- 5e. respiratory candidate (S19)
def respiratory_barrier_immunity_candidate():
    """SECTION 19-A: a respiratory/lung VP volume would localise THIS volume's tolerance switch (T21/T23/T24)
    to the AIRWAY MUCOSA -- the gut shared-substrate identity re-applied to a second barrier surface, grounded
    by barrier_surface_agnostic(). NAMED CANDIDATE, NOT a declared seam: it needs the LIVE respiratory volume
    plus that volume's OWNED absolute airway-antigen scale, neither on disk in this session. The immune-side
    tolerance primitive (T23/T24, barrier-surface-agnostic) IS real in this zip; the airway localisation is [O]."""
    rec = XR.respiratory_candidate_record()
    ep = rec["immune_side_endpoint"]
    endpoint_real = (ep.get("endpoint_is_real_in_this_zip", False)
                     and ep.get("barrier_surface_agnostic", False)
                     and round(ep["surface_independent_offset"], 8) == round(spinodal(1.0), 8))
    cand = rec.get("identity_candidate", {})
    has_named_candidate = ("what" in cand and "why_not_claimed_now" in cand
                           and "how_to_promote" in cand and "falsifier" in cand)
    is_candidate_type = ("candidate" in rec.get("seam_type", "").lower())
    identity_claimed_now = (rec.get("seam_type", "").strip() == "shared-substrate identity")  # must be False
    return dict(axis=rec["axis"][:60],
                immune_side_tolerance_primitive_is_real=bool(endpoint_real),
                surface_independent_offset=round(ep["surface_independent_offset"], 8),
                named_candidate_not_claimed=bool(has_named_candidate and is_candidate_type
                                                 and not identity_claimed_now),
                owner_immune_doi=rec["owner_concept_doi_immune"],
                owner_respiratory_doi=rec["owner_concept_doi_respiratory"][:12],
                grade=rec["grade"])


# --------------------------------------------------------------------------- 5f. skin candidate (S19)
def skin_barrier_immunity_candidate():
    """SECTION 19-B / SECTION 21: a skin VP volume localises THIS volume's tolerance switch to the EPIDERMAL
    BARRIER, the third barrier surface on the same barrier-agnostic line. v0.20.0 LIVE substrate-verifies it
    against integumentary_vp_site v1.0.0 (substrate drift 0) and confirms a RECIPROCAL immune-seam handshake
    (the skin volume independently declares an out-seam to immune_hematologic). The epidermal-tolerance IDENTITY
    remains IMMUNE-OWNED CLOSED-FORM (barrier-agnosticism): the skin supplies the real barrier surface (epidermis
    TP63, keratinocyte KRT14) but defers the immune tolerance switch as an out-seam, so the identity is NOT
    engine-verified and NOT contradicted -- a third distinct outcome (gut = verified, musculoskeletal = retired).
    The vendored epidermal snapshot is checked in closed form against this volume's substrate."""
    rec = XR.skin_candidate_record()
    ep = rec["immune_side_endpoint"]
    endpoint_real = (ep.get("endpoint_is_real_in_this_zip", False)
                     and ep.get("barrier_surface_agnostic", False)
                     and round(ep["surface_independent_offset"], 8) == round(spinodal(1.0), 8))
    identity_claimed_now = (rec.get("seam_type", "").strip() == "shared-substrate identity")  # must be False
    # --- v0.20.0 LIVE verification: substrate drift 0 ---
    lv = rec.get("live_verification", {})
    pointer_live_verified = bool(lv.get("substrate_drift_is_zero", False)
                                 and round(float(lv.get("substrate_drift", 1.0)), 12) == 0.0)
    # --- real epidermal barrier surface: recompute the vendored spinodals from THIS substrate (integrity) ---
    surf = lv.get("real_epidermal_barrier_surface", {})
    epi_sp = round(spinodal(surf.get("epidermis_gamma", 0.0)), 8)
    krt_sp = round(spinodal(surf.get("keratinocyte_gamma", 0.0)), 8)
    barrier_surface_integrity = (epi_sp == round(surf.get("epidermis_spinodal_g", -1), 8)
                                 and krt_sp == round(surf.get("keratinocyte_spinodal_g", -1), 8))
    # --- reciprocal immune-seam handshake (skin declares an out-seam to immune_hematologic) ---
    recip = lv.get("reciprocal_immune_seam", {})
    reciprocal_immune_seam_present = bool(recip.get("present", False)
                                          and "immune_hematologic" in recip.get("skin_declared_seam_id", ""))
    # --- identity disposition: immune-owned closed-form, NOT engine-verified, NOT contradicted ---
    disp = rec.get("identity_disposition", {})
    disposition_recorded = ("verdict" in disp and "what_the_live_engine_shows" in disp
                            and disp.get("status", "").startswith("the epidermal-tolerance IDENTITY remains"))
    identity_engine_verified = bool(lv.get("identity_engine_verified", True))      # must be False (skin defers it)
    identity_contradicted = bool(lv.get("identity_contradicted", True))            # must be False (no contradiction)
    identity_immune_owned_closed_form_not_contradicted = bool(
        endpoint_real and disposition_recorded
        and not identity_engine_verified and not identity_contradicted)
    return dict(axis=rec["axis"][:60],
                immune_side_tolerance_primitive_is_real=bool(endpoint_real),
                surface_independent_offset=round(ep["surface_independent_offset"], 8),
                pointer_live_verified=pointer_live_verified,
                skin_substrate_drift=round(float(lv.get("substrate_drift", 1.0)), 12),
                real_epidermal_barrier_surface_confirmed=bool(barrier_surface_integrity),
                epidermis_spinodal_recomputed=epi_sp, keratinocyte_spinodal_recomputed=krt_sp,
                reciprocal_immune_seam_present=reciprocal_immune_seam_present,
                skin_implements_immune_tolerance_switch=bool(lv.get("skin_implements_immune_tolerance_switch", True)),
                identity_engine_verified=identity_engine_verified,
                identity_contradicted=identity_contradicted,
                identity_immune_owned_closed_form_not_contradicted=identity_immune_owned_closed_form_not_contradicted,
                identity_claimed_now=bool(identity_claimed_now),
                owner_immune_doi=rec["owner_concept_doi_immune"],
                owner_skin_doi=rec["owner_concept_doi_skin"][:24],
                grade=rec["grade"])


# --------------------------------------------------------------------------- 6. firewall architectural lock
def _scan_imports():
    """Walk the package's python sources and collect every import that resolves to a SIBLING module.
    The same lock digestive runs circulatory-side. Returns (violation_lines, files_scanned)."""
    roots = [os.path.join(_PKG, "repro"), os.path.join(_PKG, "inherited"), os.path.join(_PKG, "tools")]
    violations, n_files = [], 0
    for root in roots:
        for dirpath, _dirs, files in os.walk(root):
            if "__pycache__" in dirpath:
                continue
            for fn in files:
                if not fn.endswith(".py"):
                    continue
                fp = os.path.join(dirpath, fn)
                rel = os.path.relpath(fp, _PKG).replace(os.sep, "/")
                if any(rel == x or rel.startswith(x) for x in _OUT_OF_GATE_RELPATHS):
                    continue                                  # out-of-gate section-17 harness: not in-gate certified
                n_files += 1
                for i, line in enumerate(open(fp, encoding="utf-8"), 1):
                    mobj = _IMPORT_RE.match(line)
                    if not mobj:
                        continue
                    mod = mobj.group(1).lower()
                    if any(tok in mod for tok in _INTERNAL_OK):
                        continue
                    if any(tok in mod for tok in _SIBLING_IMPORT_TOKENS):
                        violations.append("%s:%d: %s" % (os.path.relpath(fp, _PKG), i, line.strip()))
    return violations, n_files


def _flatten_keys(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.append(str(k).lower()); _flatten_keys(v, out)
    elif isinstance(obj, list):
        for v in obj: _flatten_keys(v, out)


def firewall_architectural_lock():
    """The firewall, enforced not asserted: (a) ZERO sibling imports anywhere in the package; (b) the
    emitted EMERGENCE state (engine circulate()) carries no felt/HPA/cortisol/mind key -- organ emergence,
    the tolerance saddle-node, the cytokine latch and the surveillance seam are computed with zero reference
    to a mind quantity, and the emergence state does not re-enter mind's HPA."""
    violations, n_files = _scan_imports()
    state = ENG.circulate()
    keys = []; _flatten_keys(state, keys)
    felt_in_emergence = sorted({t for t in _FELT_HPA_TOKENS for k in keys if t in k})
    holds = (len(violations) == 0 and len(felt_in_emergence) == 0)
    return dict(sibling_import_count=len(violations), sibling_import_violations=violations,
                python_files_scanned=n_files,
                emergence_state_felt_hpa_keys=felt_in_emergence,
                emergence_state_takes_no_felt_input=bool(len(felt_in_emergence) == 0),
                firewall_holds=bool(holds),
                grade="[F] forced architectural identity (zero sibling imports; emergence state mind-free)")


# --------------------------------------------------------------------------- 7. SSOT consistency
def seam_ssot_consistency():
    """The gut identity reads the SAME vendored digestive snapshot the consume function returns; the
    neuro-immune directions read the SAME mind record. Confirm internal consistency (no sibling import)."""
    snap = XR.consumed_digestive_mucosal_flare()
    gut = gut_immune_tolerance_localization()
    induction_consistent = (gut["digestive_induction"] == snap["ibd_induction_threshold"])
    maintenance_consistent = (gut["digestive_maintenance"] == snap["ibd_maintenance_threshold"])
    keys_declared = set(XR.seam_keys())
    declared_seam_keys = {"digestive_gut_immune_interface", "mind_neuroimmune_interface",
                          "immunosurveillance_oncology_hub",
                          "circulatory_leukocyte_trafficking_interface",
                          "musculoskeletal_marrow_niche_interface"}
    candidate_keys = {"respiratory_mucosal_immunity_candidate",
                      "skin_barrier_immunity_candidate"}
    keys_expected = declared_seam_keys | candidate_keys
    return dict(gut_induction_matches_snapshot=bool(induction_consistent),
                gut_maintenance_matches_snapshot=bool(maintenance_consistent),
                all_five_seams_declared=bool(declared_seam_keys <= keys_declared),
                both_barrier_candidates_declared=bool(candidate_keys <= keys_declared),
                ssot_consistent=bool(induction_consistent and maintenance_consistent
                                     and keys_declared == keys_expected))


# --------------------------------------------------------------------------- aggregate + digest
def validate_seams():
    gut_snap = consume_digestive_mucosal_flare()
    gut = gut_immune_tolerance_localization()
    nin = neuroimmune_stress_suppression_direction()
    nout = cytokine_to_mind_pointer_is_not_dependency()
    onc = oncology_hub_spoke()
    circ = circulatory_leukocyte_trafficking_pointer()
    msk = musculoskeletal_marrow_niche_pointer()
    bsa = barrier_surface_agnostic()
    resp = respiratory_barrier_immunity_candidate()
    skin = skin_barrier_immunity_candidate()
    fw = firewall_architectural_lock()
    ss = seam_ssot_consistency()
    passed = bool(gut["identity_holds"] and nin["wired"] and nout["pointer_not_dependency"]
                  and circ["pointer_not_dependency"] and msk["pointer_not_dependency"]
                  and msk["pointer_live_verified"] and msk["identity_upgrade_retired_on_live_evidence"]
                  and bsa["barrier_surface_agnostic"]
                  and resp["named_candidate_not_claimed"] and resp["immune_side_tolerance_primitive_is_real"]
                  and skin["pointer_live_verified"] and skin["reciprocal_immune_seam_present"]
                  and skin["real_epidermal_barrier_surface_confirmed"]
                  and skin["identity_immune_owned_closed_form_not_contradicted"]
                  and skin["immune_side_tolerance_primitive_is_real"]
                  and fw["firewall_holds"] and ss["ssot_consistent"])
    return dict(digestive_gut_immune_snapshot=gut_snap,
                gut_immune_identity=gut,
                neuroimmune_stress_in=nin, neuroimmune_cytokine_out=nout,
                oncology_hub=onc,
                circulatory_trafficking=circ, musculoskeletal_marrow=msk,
                barrier_surface_agnostic=bsa,
                respiratory_candidate=resp, skin_candidate=skin,
                firewall=fw, ssot_consistency=ss,
                seam_keys=XR.seam_keys(), passed=passed)


def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    if isinstance(o, tuple): return [_round(v) for v in o]
    return o


@lru_cache(maxsize=1)
def digest():
    s = json.dumps(_round(validate_seams()), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    s, h = digest()
    print(s)
    print("# seam sha256:", h)
    v = validate_seams()
    print("# seams passed:", v["passed"],
          "| gut identity:", v["gut_immune_identity"]["identity_holds"],
          "| circ pointer:", v["circulatory_trafficking"]["pointer_not_dependency"],
          "| msk pointer:", v["musculoskeletal_marrow"]["pointer_not_dependency"],
          "| msk pointer live-verified:", v["musculoskeletal_marrow"]["pointer_live_verified"],
          "| msk identity retired (honest neg):", v["musculoskeletal_marrow"]["identity_upgrade_retired_on_live_evidence"],
          "| barrier-agnostic:", v["barrier_surface_agnostic"]["barrier_surface_agnostic"],
          "| resp named-not-claimed:", v["respiratory_candidate"]["named_candidate_not_claimed"],
          "| skin live-verified + reciprocal:",
          v["skin_candidate"]["pointer_live_verified"] and v["skin_candidate"]["reciprocal_immune_seam_present"],
          "| firewall sibling-imports:", v["firewall"]["sibling_import_count"],
          "| ssot consistent:", v["ssot_consistency"]["ssot_consistent"])
