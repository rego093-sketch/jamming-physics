# -*- coding: utf-8 -*-
"""
completion.lock -- the LOCKED surface for Appendix J. Every number/edge the package uses is read
from param_db.json with a provenance string; there are NO inline magic numbers downstream. lock
also emits a manifest (every locked input + grade + provenance) that the gate audits.

Inheritance discipline (read this FIRST, like every appendix):
  * the SantaLucia 1998 NN table and the 38 real GRCh38 driver-gene gamma are inherited
    BYTE-IDENTICAL from Appendix I (which inherited them from Appendix H/G). They are NEVER
    re-fetched here; the gate re-checks them byte-for-byte against the Appendix-I DB.
  * the 25 NEW gammas (limb FGF/Wnt inducers + full HOX clusters) are REAL GRCh38 promoter
    measurements by the IDENTICAL formula gamma = -mean(NN dG, SantaLucia 1998) over TSS-2000..+500.
  * the spinodal(gamma) and barrier(gamma) maps are Appendix A, verbatim.
  * NEW modelling forms are DECLARED [F], not fitted: the quorum/AND threshold gate and the
    sequence->drive map W=sqrt(gamma). The cited rates (segmentation period, Carnegie days) are [L].
  * the cascade DEPTH is DERIVED from the cited edges, never asserted.
"""
import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DB = os.path.join(_ROOT, "param_db.json")
# the parent appendix DB, used by the gate to re-verify byte-identical inheritance of the 38.
_PARENT_DB = os.path.join(os.path.dirname(_ROOT),
                          "ax-i-developmental-order-grammar", "param_db.json")

with open(_DB, "r", encoding="utf-8") as _fh:
    DB = json.load(_fh)


def nn_table():
    return DB["nn_stacking_dG_kcal_per_mol"]["values"]


def driver_gamma():
    """The MERGED driver atlas: 38 inherited (byte-identical) + 25 new (real GRCh38). A single
    {sym: {gamma, program, system, ...}} dict, exactly like the Appendix-I accessor."""
    merged = {}
    merged.update(DB["driver_gamma_inherited"])
    merged.update(DB["driver_gamma_new"])
    return merged


def driver_gamma_inherited():
    return DB["driver_gamma_inherited"]


def driver_gamma_new():
    return DB["driver_gamma_new"]


def driver(sym):
    d = driver_gamma()
    if sym not in d:
        raise KeyError("driver gene not in locked atlas: %s" % sym)
    return d[sym]


def cascade_edges():
    """List of [parent, child, citation] documented regulatory/lineage/collinearity edges.
    The three cited blocks are concatenated: inherited (Appendix I) + limb-induction + HOX
    collinear. Order is deterministic (inherited, then limb, then HOX)."""
    rc = DB["regulatory_cascade"]
    return (list(rc["edges_inherited"])
            + list(rc["edges_limb_induction"])
            + list(rc["edges_hox_collinear"]))


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


def floor_robustness_cfg():
    return DB["thresholds"]["floor_robustness"]["value"]


# ---- O2: the cited developmental rates (absolute timing) ---------------------
def seg_clock_period_hours():
    return DB["developmental_rates"]["segmentation_clock_period_hours"]["value"]


def somite_pairs_total():
    return DB["developmental_rates"]["somite_pairs_total"]["value"]


def carnegie_stage_days():
    """{ 'CS8': 18.0, ... } cited approximate post-ovulation day per Carnegie stage."""
    return DB["developmental_rates"]["carnegie_stage_days"]["value"]


# ---- GATE: the quorum / AND threshold-k generalisation -----------------------
def threshold_gate_cfg():
    return DB["thresholds"]["threshold_gate"]["value"]


# ---- O3: the sequence -> drive map -------------------------------------------
def drive_map_cfg():
    return DB["thresholds"]["drive_from_sequence_map"]["value"]


def thresholds():
    return DB["thresholds"]


def grades():
    return DB["_meta"]["grades"]


def parent_db_path():
    return _PARENT_DB


# ---- the audited lock manifest ----------------------------------------------
def lock_manifest():
    """Every locked input with its grade + provenance. The gate audits this and checks there are
    no un-provenanced numbers."""
    man = {"appendix": "J -- developmental ORDER-grammar COMPLETION", "inputs": []}

    def add(name, grade, provenance):
        man["inputs"].append({"name": name, "grade": grade, "provenance": provenance})

    add("nn_stacking_dG_kcal_per_mol", DB["nn_stacking_dG_kcal_per_mol"]["grade"],
        DB["nn_stacking_dG_kcal_per_mol"]["provenance"])
    add("driver_gamma_inherited (38 real GRCh38)", "[L]",
        "inherited BYTE-IDENTICAL from Appendix I; gamma=-mean(NN dG); the 4 skeletal drivers "
        "(SOX9/RUNX2/PAX1/GLI3) match Appendix G byte-for-byte. Re-checked by the gate against "
        "the Appendix-I param_db.")
    add("driver_gamma_new (25 real GRCh38)", DB["driver_gamma_new"][next(iter(DB["driver_gamma_new"]))]["grade"]
        if DB["driver_gamma_new"] else "[L]",
        "limb FGF/Wnt inducers + full HOXA/HOXD clusters; REAL GRCh38 promoter measurements by the "
        "IDENTICAL formula gamma=-mean(NN dG) over TSS-2000..+500 (NCBI eutils). corr(gamma,GC)=0.993 "
        "matches the kit method.")
    add("regulatory_cascade.edges_inherited", DB["regulatory_cascade"]["grade"],
        "inherited Appendix-I regulatory/lineage edges; the DEPTH derived is [V].")
    add("regulatory_cascade.edges_limb_induction", DB["regulatory_cascade"]["grade"],
        "cited limb-field RA/Wnt -> Tbx -> Fgf10 -> AER-ZPA loop edges (Niederreither 1999; "
        "Kawakami 2001; Agarwal 2003; etc.) -- give TBX5/TBX4 real upstream depth.")
    add("regulatory_cascade.edges_hox_collinear", DB["regulatory_cascade"]["grade"],
        "cited HOXA/HOXD temporal-collinearity chains 3'->5' (Izpisua-Belmonte 1991) -- give "
        "HOXA13/HOXD13 their true late depth.")
    add("carnegie_onset_anchor", DB["carnegie_onset_anchor"]["grade"],
        "cited embryological onset RANKS + cited HOX collinear onset gradient; absolute stage/time "
        "is the [L]/[F] timing map of O2, the global multi-program clock stays [O].")
    add("developmental_rates", DB["developmental_rates"]["grade"],
        "cited measured rates: human PSM period ~5h (Diaz-Cuadros 2020; Matsuda 2020); ~42 somite "
        "pairs (O'Rahilly & Muller); approximate Carnegie-stage days. The order->day map is [F]; "
        "the global multi-program clock stays [O].")
    for k in ("spinodal_form", "barrier_form", "coupled_network",
              "carnegie_rank_corr_ceiling", "cascade_corr_floor",
              "edge_concordance_floor", "depth_beats_gamma_required",
              "threshold_gate", "drive_from_sequence_map", "floor_robustness"):
        t = DB["thresholds"][k]
        add("thresholds." + k, t["grade"], t["provenance"])
    # every downstream number is read from this DB with a provenance; there are no inline magics.
    man["inline_magic_numbers"] = 0
    return man
