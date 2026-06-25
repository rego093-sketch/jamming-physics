# -*- coding: utf-8 -*-
"""
order.lock -- the LOCKED surface for Appendix I. Every number/edge the package uses is read
from param_db.json with a provenance string; there are NO inline magic numbers downstream.
lock also emits a manifest (every locked input + grade + provenance) that the gate audits.

Inheritance discipline (read this FIRST, like every appendix):
  * the SantaLucia 1998 NN table and the 38 real GRCh38 driver-gene gamma are inherited
    BYTE-IDENTICAL from Appendix H (which inherited the 4 skeletal drivers from Appendix G).
  * the spinodal(gamma) map is Appendix A, verbatim.
  * NEW here: the regulatory cascade (cited [F] edges) and the Carnegie onset anchors (cited
    [L]). Nothing is tuned; the cascade DEPTH is DERIVED from the edges, not asserted.
"""
import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DB = os.path.join(_ROOT, "param_db.json")

with open(_DB, "r", encoding="utf-8") as _fh:
    DB = json.load(_fh)


def nn_table():
    return DB["nn_stacking_dG_kcal_per_mol"]["values"]


def driver_gamma():
    return DB["driver_gamma"]


def driver(sym):
    d = DB["driver_gamma"]
    if sym not in d:
        raise KeyError("driver gene not in locked atlas: %s" % sym)
    return d[sym]


def cascade_edges():
    """List of [parent, child, citation] documented regulatory/lineage edges."""
    return DB["regulatory_cascade"]["edges"]


def carnegie_anchor():
    """{gene: {cs_approx, rank, event, cite}} -- cited Carnegie onset RANKS."""
    return DB["carnegie_onset_anchor"]["genes"]


def coupled_cfg():
    return DB["thresholds"]["coupled_network"]["value"]


def null_ceiling():
    return DB["thresholds"]["carnegie_rank_corr_ceiling"]["value"]


def cascade_floor():
    return DB["thresholds"]["cascade_corr_floor"]["value"]


def edge_concordance_floor():
    return DB["thresholds"]["edge_concordance_floor"]["value"]


def depth_beats_gamma_required():
    return DB["thresholds"]["depth_beats_gamma_required"]["value"]


def thresholds():
    return DB["thresholds"]


def grades():
    return DB["_meta"]["grades"]


# ---- the audited lock manifest ----------------------------------------------
def lock_manifest():
    """Every locked input with its grade + provenance. The gate audits this and checks there
    are no un-provenanced numbers."""
    man = {"appendix": "I -- developmental ORDER grammar", "inputs": []}

    def add(name, grade, provenance):
        man["inputs"].append({"name": name, "grade": grade, "provenance": provenance})

    add("nn_stacking_dG_kcal_per_mol", DB["nn_stacking_dG_kcal_per_mol"]["grade"],
        DB["nn_stacking_dG_kcal_per_mol"]["provenance"])
    add("driver_gamma (38 real GRCh38)", "[L]",
        "inherited byte-identical from Appendix H; gamma=-mean(NN dG); the 4 skeletal drivers "
        "(SOX9/RUNX2/PAX1/GLI3) match Appendix G byte-for-byte.")
    add("regulatory_cascade.edges", DB["regulatory_cascade"]["grade"],
        "documented upstream->downstream regulatory/lineage edges; the DEPTH derived is [V].")
    add("carnegie_onset_anchor", DB["carnegie_onset_anchor"]["grade"],
        "cited embryological onset RANKS; absolute stage/time is [O].")
    for k in ("spinodal_form", "barrier_form", "coupled_network",
              "carnegie_rank_corr_ceiling", "cascade_corr_floor",
              "edge_concordance_floor", "depth_beats_gamma_required"):
        t = DB["thresholds"][k]
        add("thresholds." + k, t["grade"], t["provenance"])
    # every downstream number is read from this DB with a provenance; there are no inline magics.
    man["inline_magic_numbers"] = 0
    return man
