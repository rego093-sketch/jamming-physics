#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seam_manifest.py  --  Integumentary CROSS-PACKAGE SEAM manifest (HANDOFF Section 5.3).

This is NOT a new mechanism and adds NO new constant. It is the package's single, labelled,
machine-readable SEAM record for the "one body" runner -- the artifact HANDOFF Section 5.3 asks for:

    "The pigment-loss -> oncology link (vitiligo/albinism lesion -> melanoma burst sensitivity) is
     already internal here; expose it as a labelled seam output for the 'one body' runner."

It consolidates every interface the integumentary package has, in three honestly distinct classes:

  (A) INHERITED-IN seams -- read-only inputs this package VENDORS from a sibling, never re-derives:
        * circulatory : dermal-perfusion MAGNITUDE (cited) -- consumed by the T9 vasomotor target,
                        which adds only the reactivity dynamics and leaves the magnitude an inherited
                        citation (the SSOT seam the vasomotor layer was careful not to cross).
        * DNA         : organ IDENTITY + emergence ORDER + the measured master-gene gamma [V] -- the
                        gene-clock owns these; this package cites them (inherited/organ_identity.md).
        * substrate   : the FHN / R19 bistable primitive (vendored in inherited/vp_substrate.py).

  (B) INTERNAL-LIVE seams -- cross-TARGET couplings computed live INSIDE this package and now exposed
      as labelled outputs (the Section 5.3 headline). A melanocyte-target (T3) lesion that removes the
      melanin screen RAISES the shared oncology-kernel hazard. The numbers are not recomputed here --
      they are RE-EXPORTED verbatim from the already-verified pathology layer (skin_pathology.albinism,
      skin_pathology.skin_cancer, skin_pathology.vitiligo) so the seam output IS the internal link,
      surfaced, not a parallel implementation. The intervention (sunscreen = an exogenous screen) lowers
      the hazard again, demonstrating the screen is the causal lever, not a correlate.

  (C) DECLARED-OUT seams -- CONTRACTS to sibling packages, honestly flagged as DECLARED, NOT yet live
      wiring (the integration harness of HANDOFF Section 5.3/5.4 does not exist yet). Each carries the
      in-package dynamics-side back-pointer so the bidirectional cross-reference (master map Section 6.2)
      can be closed once the harness is built:
        * gene-lesion -> disease_wp : the single-gene rare genodermatoses (HANDOFF Section 3); gene-key
                        SSOT is disease_wp's, the dynamics-side TRAJECTORY is this package's (named).
        * immune / rheumatology -> sibling : urticaria/angioedema (immune_hematologic), lichen planus
                        (immune-effector), secondary-Raynaud FIXED ischemia (connective-tissue disease),
                        and rosacea inflammatory effector chemistry beyond the LL-37/Demodex amplifier
                        flag -- all named seams, not modelled in this jamming-class package.
        * out-of-class : cutaneous infections (impetigo, cellulitis, dermatophytosis, herpes, warts) --
                        pathogen-driven, OUTSIDE the package's physical (R19-dynamics) class entirely;
                        no seam target, named as out-of-class so the boundary is explicit.

GRADES (C3): the live coupling is a simulation-verified cross-target SHAPE [V] resting on cited
epidemiology [L]; the absolute RR magnitude is [O] (inherits the oncology obstacle: population baseline
+ absolute dose calibration). Inherited/declared seams carry the grade of the owning package.
Determinism (C1): the manifest is assembled from deterministic engine/pathology outputs + fixed
declarations; two emits hash to an identical SHA-256. The core battery and every disease layer are
READ, never altered -- this layer's hash is its own and the core run_all.py hash is untouched.
"""
import os, sys, json, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "_oncology"))
sys.path.insert(0, os.path.join(_HERE, "..", "_pathology"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))

import skin_pathology as PATHO          # the already-verified disease layer (read-only here)
import carcinogen_dose_response as ONCO  # the shared oncology kernel (read-only here)


# ===========================================================================
#  (B) INTERNAL-LIVE seam: pigment-loss (T3) -> oncology kernel
#      Re-exported verbatim from the pathology layer -- NOT recomputed.
# ===========================================================================
def pigment_loss_to_oncology():
    """Expose the already-internal melanocyte-target -> oncology-kernel coupling as a labelled seam.

    Every numeric field is pulled straight from the pathology layer's own return values, so the seam
    output is provably the internal link surfaced (the verifier asserts re-export fidelity). The two
    couplings are the SCC cumulative-hazard RR (albinism, screen removed) and the melanoma burst RR
    (any depigmenting lesion -- albinism or vitiligo -- removing the screen that blunts a sunburn).
    """
    alb = PATHO.albinism()            # T3->oncology: functional screen removed -> SCC hazard up
    can = PATHO.skin_cancer()         # oncology: pigment loss -> melanoma intermittent/burst RR up
    vit = PATHO.vitiligo()            # T3: melanocyte-viability loss -> delivered-UV attenuation -> full

    return {
        "seam_id": "pigment_loss__to__oncology",
        "from_target": "T3 (melanin photoprotection)",
        "from_organ": "melanocyte (MITF)",
        "to_target": "oncology (UV multistage Kramers kernel)",
        "mechanism": "a melanocyte-target lesion removes the melanin screen, so the UV reaching DNA stays "
                     "full, and the shared multistage hazard rises (RR>1); restoring an (exogenous) screen "
                     "lowers it again -- the screen is the causal lever",
        # --- re-exported live couplings (verbatim from the pathology layer) ---
        "scc_hazard_RR_screen_removed": alb["hazard_RR_albino_vs_pigmented"],     # albinism vs pigmented
        "scc_incidence_RR_screen_removed": alb["incidence_RR_albino_vs_pigmented"],
        "scc_hazard_RR_with_sunscreen": alb["intervention_hazard_RR"],            # exogenous screen restores
        "melanoma_burst_RR_pigment_loss": can["pigment_loss_burst_RR"],           # screen-removed sunburn
        "lesion_delivered_uv_attenuation": vit["disease_attenuation"],            # 1.0 == no screen at all
        # --- provenance: every number above traces to a named pathology field (no orphan constant) ---
        "source_fields": {
            "scc_hazard_RR_screen_removed": "skin_pathology.albinism().hazard_RR_albino_vs_pigmented",
            "scc_incidence_RR_screen_removed": "skin_pathology.albinism().incidence_RR_albino_vs_pigmented",
            "scc_hazard_RR_with_sunscreen": "skin_pathology.albinism().intervention_hazard_RR",
            "melanoma_burst_RR_pigment_loss": "skin_pathology.skin_cancer().pigment_loss_burst_RR",
            "lesion_delivered_uv_attenuation": "skin_pathology.vitiligo().disease_attenuation",
        },
        "screen_is_causal_lever": bool(alb["intervention_hazard_RR"] < alb["hazard_RR_albino_vs_pigmented"]),
        "coupling_sign_raises_hazard": bool(alb["hazard_RR_albino_vs_pigmented"] > 1.0
                                            and can["pigment_loss_burst_RR"] > 1.0),
        "grade_shape": "[V] cross-target coupling: a T3 screen-loss lesion raises the oncology hazard (sign + direction verified)",
        "grade_anchor": "[L] albinism markedly elevates cSCC/melanoma; vitiligo patches are photoprotection-deficient; Gandini 2005 intermittent SRR 1.61",
        "grade_absolute": "[O] absolute RR magnitude: inherits the oncology obstacle (population baseline rate + absolute dose calibration)",
    }


# ===========================================================================
#  (A) INHERITED-IN seams  +  (C) DECLARED-OUT seams (fixed declarations)
# ===========================================================================
def inherited_in_seams():
    """Read-only inputs this package vendors from a sibling and never re-derives."""
    return [
        {"seam_id": "in__circulatory__dermal_perfusion", "direction": "IN", "kind": "inherited_citation",
         "source_package": "circulatory", "imported": "dermal-perfusion MAGNITUDE (cited)",
         "consumed_by": "T9 (neurovascular reactivity)", "live": True,
         "note": "the vasomotor layer adds only the reactivity dynamics and leaves the perfusion magnitude "
                 "an inherited citation -- the SSOT seam it was careful not to cross",
         "grade": "[L] cited (owned by circulatory)"},
        {"seam_id": "in__DNA__organ_identity", "direction": "IN", "kind": "inherited_result",
         "source_package": "DNA (morphogenesis gene-clock)",
         "imported": "organ IDENTITY + emergence ORDER + measured master-gene gamma (TP63/KRT14/MITF/EDAR/PRDM1)",
         "consumed_by": "every target (each organ rides its measured gamma)", "live": True,
         "note": "identity + order live in DNA; gamma is measured, read-only, never fitted; vendored in "
                 "inherited/organ_gamma.json + organ_identity.md and re-vendored on change",
         "grade": "[V] emergence (owned by DNA); gamma measured [V]"},
        {"seam_id": "in__substrate__R19", "direction": "IN", "kind": "vendored_primitive",
         "source_package": "substrate", "imported": "the FHN / R19 bistable switch ds/dt = g*s - s^3 + h (+ spinodal/barrier/dwell)",
         "consumed_by": "every target + every additive layer", "live": True,
         "note": "the one shared primitive; vendored in inherited/vp_substrate.py",
         "grade": "[F] substrate primitive"},
    ]


def declared_out_seams():
    """Contracts to sibling packages: DECLARED, not yet live wiring (the harness does not exist yet).

    Each gene-lesion / immune seam carries the in-package dynamics-side back-pointer so the bidirectional
    cross-reference (master map Section 6.2) can be closed once the integration harness is built.
    """
    gene_lesion = [
        {"entity": "genetic ichthyoses (FLG / TGM1 / ABCA12 / STS)", "dynamics_side": "T1+T4 (retention near the spinodal)"},
        {"entity": "ectodermal dysplasias (EDA / EDAR / EDARADD)", "dynamics_side": "T5 (capped-sweat danger band)"},
        {"entity": "oculocutaneous albinism (TYR / OCA2 / TYRP1 / SLC45A2)", "dynamics_side": "T3->oncology (screen removed -> hazard RR)"},
        {"entity": "xeroderma pigmentosum (XPA-XPG / POLH)", "dynamics_side": "oncology (an extreme of the same UV multistage kernel)"},
        {"entity": "hereditary skin-cancer syndromes (Gorlin/PTCH1, familial melanoma/CDKN2A)", "dynamics_side": "oncology (sporadic UV cancers are ours; hereditary syndromes are gene-key)"},
        {"entity": "other genodermatoses (Netherton/SPINK5, Darier/ATP2A2, Hailey-Hailey/ATP2C1, epidermolysis bullosa/COL7A1·KRT5·KRT14·LAMB3)", "dynamics_side": "T8 cell-adhesion (acquired autoimmune bullous is ours; congenital EB is gene-key)"},
    ]
    out = [
        {"seam_id": "out__disease_wp__gene_lesion", "direction": "OUT", "kind": "declared_contract",
         "target_package": "disease_wp", "status": "DECLARED (not live -- awaits the integration harness)",
         "owns": "the single-gene gene->lesion FACT (gene-key SSOT)",
         "this_package_owns": "the dynamics-side TRAJECTORY each lesion drives (already covered)",
         "entities": gene_lesion,
         "note": "master map Section 6.2 bidirectional cross-reference: register each gene-lesion on the "
                 "disease_wp side with a back-pointer to the dynamics section here",
         "grade": "contract (no number); dynamics side already [V] in this package"},
        {"seam_id": "out__immune_hematologic__urticaria", "direction": "OUT", "kind": "declared_contract",
         "target_package": "immune_hematologic", "status": "DECLARED (not live)",
         "owns": "mast-cell / histamine effector (urticaria / angioedema)",
         "this_package_owns": "nothing -- not a skin jamming-class target",
         "note": "named sibling seam, not modelled in this package", "grade": "contract"},
        {"seam_id": "out__immune_effector__lichen_planus", "direction": "OUT", "kind": "declared_contract",
         "target_package": "immune_effector", "status": "DECLARED (not live)",
         "owns": "interface inflammation (lichen planus / inflammatory dermatoses)",
         "this_package_owns": "nothing -- needs an immune-effector seam",
         "note": "named sibling seam, not modelled in this package", "grade": "contract"},
        {"seam_id": "out__rheumatology__secondary_raynaud", "direction": "OUT", "kind": "declared_contract",
         "target_package": "immune_rheumatology", "status": "DECLARED (not live)",
         "owns": "the FIXED digital-ischemia / ulcer of SECONDARY Raynaud (connective-tissue disease)",
         "this_package_owns": "PRIMARY Raynaud's reversible vasospasm (T9, already covered)",
         "note": "the T9 layer models primary (reversible) Raynaud and names the fixed secondary state as this seam",
         "grade": "contract; primary side [V] here"},
        {"seam_id": "out__immune_effector__rosacea_inflammation", "direction": "OUT", "kind": "declared_contract",
         "target_package": "immune_effector", "status": "DECLARED (not live)",
         "owns": "rosacea inflammatory effector chemistry BEYOND the LL-37 / Demodex amplifier flag",
         "this_package_owns": "the vasomotor reactivity + the papulopustular amplifier flag (T9, already covered)",
         "note": "the T9 layer carries the dilation/fixation + amplifier flag; deeper effector chemistry is the seam",
         "grade": "contract; vasomotor side [V] here"},
        {"seam_id": "out__none__cutaneous_infection", "direction": "OUT", "kind": "out_of_class",
         "target_package": None, "status": "OUT-OF-CLASS (no seam target)",
         "owns": "pathogen-driven infections (impetigo, cellulitis, dermatophytosis, herpes, warts)",
         "this_package_owns": "nothing -- these are not an R19-dynamics failure",
         "note": "outside the package's physical (jamming) class entirely; named so the boundary is explicit",
         "grade": "out-of-class"},
    ]
    return out


# ===========================================================================
#  Manifest assembly + deterministic emit
# ===========================================================================
def seam_manifest():
    internal = pigment_loss_to_oncology()
    in_seams = inherited_in_seams()
    out_seams = declared_out_seams()
    return {
        "_about": "Integumentary cross-package seam manifest (HANDOFF 5.3): labelled IN / INTERNAL-LIVE / "
                  "OUT seams for the 'one body' runner. No new mechanism, no new constant; the internal "
                  "coupling is re-exported from the verified pathology layer, the rest are declarations.",
        "_classes": {
            "inherited_in": "read-only inputs vendored from a sibling (never re-derived here)",
            "internal_live": "cross-target couplings computed live in this package, exposed as labelled outputs",
            "declared_out": "contracts to sibling packages -- DECLARED, not yet live wiring",
        },
        "internal_live": [internal],
        "inherited_in": in_seams,
        "declared_out": out_seams,
        "_counts": {"inherited_in": len(in_seams), "internal_live": 1, "declared_out": len(out_seams)},
        "_no_new_constant": True,
        "_grades": "internal coupling shape [V] / cited epidemiology [L] / absolute RR [O] (oncology obstacle); "
                   "inherited + declared seams carry the owning package's grade",
    }


def _canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _emit(manifest):
    s = json.dumps(manifest, ensure_ascii=False, indent=2)
    h = hashlib.sha256(_canon(manifest).encode("utf-8")).hexdigest()
    return s, h


if __name__ == "__main__":
    m = seam_manifest(); s, h = _emit(m)
    print(s)
    print("\nseam_manifest sha256:", h)
