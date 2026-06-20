#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cross_references.py  --  internal SSOT loader for the immune/hematologic cross-system seams
(immune_hematologic_vp_site v0.16.0, section 16).

Reads inherited/cross_references.json with the stdlib only. Imports NO sibling code: the seam layer
and the live harness reach a sibling (when present) ONLY by file-path load, never by an import statement.
This module just hands back the vendored snapshots and seam records the seam layer consumes.
"""
import os, json
from functools import lru_cache

_HERE = os.path.dirname(os.path.abspath(__file__))
_JSON = os.path.join(_HERE, "cross_references.json")


@lru_cache(maxsize=1)
def load():
    with open(_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def seam_keys():
    """Declared seam keys (skip the leading _doc / _grade_legend / _firewall metadata keys)."""
    return [k for k in load().keys() if not k.startswith("_")]


def for_seam(key):
    """The full record for one seam key."""
    return load()[key]


# --- gut-immune (digestive) -------------------------------------------------
def consumed_digestive_mucosal_flare():
    """The vendored digestive IBD mucosal-flare snapshot (the gut localisation of T23/T24)."""
    return for_seam("digestive_gut_immune_interface")["vendored_snapshot"]


def gut_identity_record():
    return for_seam("digestive_gut_immune_interface")["identity_to_immune_primitives"]


# --- neuro-immune (mind) ----------------------------------------------------
def mind_neuroimmune_record():
    return for_seam("mind_neuroimmune_interface")


# --- oncology hub -----------------------------------------------------------
def oncology_hub_record():
    return for_seam("immunosurveillance_oncology_hub")


# --- circulatory (leukocyte trafficking) ------------------------------------
def circulatory_record():
    return for_seam("circulatory_leukocyte_trafficking_interface")


# --- musculoskeletal (marrow niche) -----------------------------------------
def musculoskeletal_record():
    return for_seam("musculoskeletal_marrow_niche_interface")


def musculoskeletal_live_verification():
    """The v0.19.0 LIVE verification of the marrow-niche pointer against musculoskeletal_vp_site v0.7.0:
    substrate drift 0 (pointer live-verified) + the RETIRED shared-substrate-identity candidate (honest
    negative: the MSK niche is built by RUNX2, a different switch/spinodal from the hematopoietic RUNX1)."""
    return for_seam("musculoskeletal_marrow_niche_interface")["live_verification"]


# --- barrier-surface mucosal immunity (v0.18.0) -----------------------------
def barrier_agnostic_note():
    """The closed-form barrier-surface-agnosticism footing under the respiratory/skin
    candidates: the tolerance offset from a surface's own antigen baseline is always
    +/- spinodal(1.0), so the gut seam generalises to any barrier surface."""
    return load()["_barrier_surface_agnostic"]


def respiratory_candidate_record():
    """The NAMED respiratory (airway-mucosa) shared-substrate-identity candidate.
    NOT a declared seam -- it needs a live respiratory volume + its owned airway-antigen scale."""
    return for_seam("respiratory_mucosal_immunity_candidate")


def skin_candidate_record():
    """The skin (epidermal-barrier) barrier-surface seam. v0.20.0 LIVE substrate-verified against
    integumentary_vp_site v1.0.0 (drift 0) + reciprocal immune-seam handshake; the epidermal-tolerance
    identity remains immune-owned closed-form (real surface confirmed, not contradicted, not engine-verified)."""
    return for_seam("skin_barrier_immunity_candidate")


def skin_live_verification():
    """The v0.20.0 LIVE verification of the skin barrier-surface seam against integumentary_vp_site v1.0.0:
    substrate drift 0 + a confirmed real epidermal barrier surface (TP63/KRT14) + a reciprocal immune out-seam
    declared by the skin volume. The epidermal-tolerance identity stays immune-owned closed-form (the skin
    volume supplies the barrier surface but defers the immune tolerance switch as an out-seam)."""
    return for_seam("skin_barrier_immunity_candidate")["live_verification"]


def as_prose(key):
    """One-line human summary of a seam (for logs / sanity)."""
    r = for_seam(key)
    return "%s  [%s]" % (r.get("seam", key), r.get("grade", ""))


if __name__ == "__main__":
    print("seam keys:", seam_keys())
    for k in seam_keys():
        print(" -", as_prose(k))
    print("\nconsumed digestive mucosal-flare snapshot:", consumed_digestive_mucosal_flare())
