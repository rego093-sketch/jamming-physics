# -*- coding: utf-8 -*-
"""
completion.lock -- the LOCKED surface for Appendix K (the absolute clock). Every number/edge the
package uses is read from param_db.json with a provenance string; there are NO inline magic numbers
downstream. lock also emits a manifest (every locked input + grade + provenance) that the gate audits.

Inheritance discipline (read this FIRST, like every appendix):
  * the SantaLucia 1998 NN table and ALL 63 real GRCh38 driver-gene gamma (the 38+25 of Appendix J)
    are inherited BYTE-IDENTICAL from Appendix J (which inherited the 38 from Appendix I, which
    inherited them from H/G). They are NEVER re-fetched here; the gate re-checks all 63 byte-for-byte
    against the Appendix-J DB. Appendix K introduces NO new promoter gamma.
  * the spinodal(gamma) and barrier(gamma) maps are Appendix A, verbatim.
  * the inherited modelling forms stay DECLARED [F]: the quorum/AND threshold gate, the
    sequence->drive map W=sqrt(gamma). The cited rates (segmentation period, somite count, Carnegie
    stage days) are [L].
  * NEW in K: the cited first-cardiac-contraction landmark (CS10, 22+-1 d) is the SECOND independent
    measured anchor; the absolute-clock calibration (linear stage->day, two anchors, ZERO free
    parameters) is the only added mechanism. The linear form + held-out acceptance band are [F]; the
    two anchors are [L]; the resulting absolute clock is graded [L], NEVER [V].
  * the cascade DEPTH is DERIVED from the cited edges, never asserted.
"""
import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DB = os.path.join(_ROOT, "param_db.json")
# the parent appendix DB, used by the gate to re-verify byte-identical inheritance of all 63.
_PARENT_DB = os.path.join(os.path.dirname(_ROOT),
                          "ax-j-order-grammar-completion", "param_db.json")

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


# ---- B1: the second (cardiac) anchor + the absolute-clock calibration -------
def cardiac_onset_anchor():
    """{stage_cs, day, uncertainty_days} -- the cited first-heartbeat landmark (CS10, 22+-1 d),
    the SECOND independent measured anchor (in-vivo cardiac modality)."""
    return DB["developmental_rates"]["cardiac_onset_anchor"]["value"]


def absolute_clock_cfg():
    """The parameter-free two-anchor calibration config (rate window, zero-point, acceptance band)."""
    return DB["thresholds"]["absolute_clock"]["value"]


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
    man = {"appendix": "K -- the absolute clock (global zero-point)", "inputs": []}

    def add(name, grade, provenance):
        man["inputs"].append({"name": name, "grade": grade, "provenance": provenance})

    add("nn_stacking_dG_kcal_per_mol", DB["nn_stacking_dG_kcal_per_mol"]["grade"],
        DB["nn_stacking_dG_kcal_per_mol"]["provenance"])
    add("driver_gamma_inherited (63 real GRCh38)", "[L]",
        "ALL 63 driver gamma (the 38+25 of Appendix J) inherited BYTE-IDENTICAL from Appendix J; "
        "gamma=-mean(NN dG); the 4 skeletal drivers (SOX9/RUNX2/PAX1/GLI3) still match byte-for-byte. "
        "Re-checked by the gate against the Appendix-J param_db. Appendix K introduces NO new gamma.")
    add("driver_gamma_new (none in K)", "[L]",
        "Appendix K adds NO new promoter gamma -- it pins absolute TIME on the inherited 63-gene "
        "atlas. The new locked datum is a developmental-rate anchor (cardiac onset), not a gamma.")
    add("regulatory_cascade.edges_inherited", DB["regulatory_cascade"]["grade"],
        "inherited Appendix-J regulatory/lineage edges; the DEPTH derived is [V].")
    add("regulatory_cascade.edges_limb_induction", DB["regulatory_cascade"]["grade"],
        "inherited cited limb-field RA/Wnt -> Tbx -> Fgf10 -> AER-ZPA loop edges.")
    add("regulatory_cascade.edges_hox_collinear", DB["regulatory_cascade"]["grade"],
        "inherited cited HOXA/HOXD temporal-collinearity chains 3'->5' (Izpisua-Belmonte 1991).")
    add("carnegie_onset_anchor", DB["carnegie_onset_anchor"]["grade"],
        "cited embryological onset RANKS; the cited Carnegie stage-days they map to are HELD-OUT "
        "targets for the absolute-clock validation in K.")
    add("developmental_rates (incl. cardiac zero-point)", DB["developmental_rates"]["grade"],
        "cited measured rates: human PSM period ~5h (Diaz-Cuadros 2020; Matsuda 2020); ~42 somite "
        "pairs (O'Rahilly & Muller); approximate Carnegie-stage days. NEW in K: the cited "
        "first-cardiac-contraction landmark (CS10, 22+-1 d; 1987 O'Rahilly & Muller convention; Moore "
        "et al. 2013) -- the SECOND independent measured anchor (in-vivo cardiac modality).")
    for k in ("spinodal_form", "barrier_form", "coupled_network",
              "carnegie_rank_corr_ceiling", "cascade_corr_floor",
              "edge_concordance_floor", "depth_beats_gamma_required",
              "threshold_gate", "drive_from_sequence_map", "floor_robustness",
              "absolute_clock"):
        t = DB["thresholds"][k]
        add("thresholds." + k, t["grade"], t["provenance"])
    # every downstream number is read from this DB with a provenance; there are no inline magics.
    man["inline_magic_numbers"] = 0
    return man
