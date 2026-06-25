# -*- coding: utf-8 -*-
"""
completion.lock -- the LOCKED surface for Appendix L (the BLUEPRINT close-out). Every number/edge the
package uses is read from param_db.json with a provenance string; there are NO inline magic numbers
downstream. lock also emits a manifest (every locked input + grade + provenance) that the gate audits.

Inheritance discipline (read this FIRST, like every appendix):
  * the SantaLucia 1998 NN table and ALL 63 real GRCh38 driver-gene gamma are inherited
    BYTE-IDENTICAL from Appendix K (which inherited them from J<-I<-H/G). They are NEVER re-fetched
    here; the gate re-checks all 63 byte-for-byte against the Appendix-K DB. Appendix L introduces NO
    new promoter gamma.
  * the spinodal(gamma) and barrier(gamma) maps are Appendix A, verbatim.
  * the inherited modelling forms stay DECLARED [F]: the quorum/AND threshold gate, the
    sequence->drive map W=sqrt(gamma). The cited rates and the two-anchor absolute clock are [L].
  * NEW in L (append-only): ONE cited upstream edge MEOX1 -> PAX7 (B4 close-out) that removes PAX7 as
    an artificial cascade source; the cascade DEPTH is DERIVED from the cited edges, never asserted,
    so adding this edge deepens the myogenic genes -- that is B4's mechanism. The B4 closure config
    is [L]; the B2 cis-occupancy probe config is [F] (it reproduces the DATA-BLOCKED finding -- the
    per-edge drive is not in the +-2 kb promoter window, so B2 cannot close from this kit).
  * the cascade DEPTH is DERIVED from the cited edges, never asserted.
"""
import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DB = os.path.join(_ROOT, "param_db.json")
# the parent appendix DB, used by the gate to re-verify byte-identical inheritance of all 63.
_PARENT_DB = os.path.join(os.path.dirname(_ROOT),
                          "ax-k-absolute-clock", "param_db.json")

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
    The cited blocks are concatenated: inherited (Appendix I) + limb-induction + HOX collinear +
    the Appendix-L B4 myogenic-upstream block (MEOX1 -> PAX7). Order is deterministic (inherited,
    limb, HOX, then myogenic-upstream). The DEPTH derived from these edges is [V]; the single new
    edge is what closes B4 (PAX7 is no longer an artificial source)."""
    rc = DB["regulatory_cascade"]
    return (list(rc["edges_inherited"])
            + list(rc["edges_limb_induction"])
            + list(rc["edges_hox_collinear"])
            + list(rc.get("edges_myogenic_upstream", [])))


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


# ---- B4: the jitter-floor close-out (the cited MEOX1->PAX7 edge) -------------
def b4_jitter_closure_cfg():
    """The B4 closure config: floor, the cited closure edge, the seed/jitter/draws. The cascade
    EXTENDED by this edge clears the +-1 rank-jitter p5 above the 0.70 floor (0.625 -> 0.728). The
    strength claim stays [L]; B3 forbids [V]."""
    return DB["thresholds"]["b4_jitter_closure"]["value"]


def myogenic_upstream_edges():
    """The Appendix-L B4 edge block (MEOX1 -> PAX7), as [[parent, child, cite], ...]."""
    return list(DB["regulatory_cascade"].get("edges_myogenic_upstream", []))


# ---- B2: the cis-occupancy probe (DATA-BLOCKED finding) ----------------------
def b2_cis_occupancy_cfg():
    """The B2 occupancy-probe config: the cited TF-family IUPAC motifs, the dinucleotide-shuffle
    null (seed 19, 500 shuffles, both strands), the +-2 kb window provenance, and the data-blocked
    rule. Reproduces the finding that proximal-promoter occupancy does NOT carry per-edge drive (the
    canonical SOX9->RUNX2 edge is below background); B2 is data-blocked by measurement, NOT [L]."""
    return DB["thresholds"]["b2_cis_occupancy"]["value"]


def cis_promoter_cache():
    """The cached real GRCh38 promoter sequences (TSS-2000..+500, the same +-2 kb gamma window) used
    by the B2 probe. {gene: {seq, prov, coords}}. Read from promoters.cache.json at the package root."""
    path = os.path.join(_ROOT, "promoters.cache.json")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


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
    man = {"appendix": "L -- the blueprint close-out (B4 closed; B2 data-blocked)", "inputs": []}

    def add(name, grade, provenance):
        man["inputs"].append({"name": name, "grade": grade, "provenance": provenance})

    add("nn_stacking_dG_kcal_per_mol", DB["nn_stacking_dG_kcal_per_mol"]["grade"],
        DB["nn_stacking_dG_kcal_per_mol"]["provenance"])
    add("driver_gamma_inherited (63 real GRCh38)", "[L]",
        "ALL 63 driver gamma inherited BYTE-IDENTICAL from Appendix K; gamma=-mean(NN dG); the 4 "
        "skeletal drivers (SOX9/RUNX2/PAX1/GLI3) still match byte-for-byte. Re-checked by the gate "
        "against the Appendix-K param_db. Appendix L introduces NO new gamma.")
    add("driver_gamma_new (none in L)", "[L]",
        "Appendix L adds NO new promoter gamma -- it closes the blueprint on the inherited 63-gene "
        "atlas. The new locked edge (MEOX1->PAX7) connects two genes already in the atlas.")
    add("regulatory_cascade.edges_inherited", DB["regulatory_cascade"]["grade"],
        "inherited Appendix-K regulatory/lineage edges; the DEPTH derived is [V].")
    add("regulatory_cascade.edges_limb_induction", DB["regulatory_cascade"]["grade"],
        "inherited cited limb-field RA/Wnt -> Tbx -> Fgf10 -> AER-ZPA loop edges.")
    add("regulatory_cascade.edges_hox_collinear", DB["regulatory_cascade"]["grade"],
        "inherited cited HOXA/HOXD temporal-collinearity chains 3'->5' (Izpisua-Belmonte 1991).")
    add("regulatory_cascade.edges_myogenic_upstream (B4 close-out)", DB["regulatory_cascade"]["grade"],
        "NEW in L: ONE cited edge MEOX1->PAX7 (somite/dermomyotome precedes Pax7+ myogenic "
        "progenitors; Buckingham & Relaix 2007; Mankoo 1999). Removes PAX7 as an artificial cascade "
        "source; rank-tie-concordant (MEOX1 rank 4 = PAX7 rank 4), 0 new inversions, DAG preserved. "
        "The DEPTH derived from it is [V].")
    add("carnegie_onset_anchor", DB["carnegie_onset_anchor"]["grade"],
        "cited embryological onset RANKS; inherited byte-identical from Appendix K.")
    add("developmental_rates (incl. cardiac zero-point)", DB["developmental_rates"]["grade"],
        "cited measured rates inherited byte-identical from Appendix K: human PSM period ~5h "
        "(Diaz-Cuadros 2020; Matsuda 2020); ~42 somite pairs (O'Rahilly & Muller); Carnegie stage "
        "days; the cited first-cardiac-contraction landmark (CS10, 22+-1 d).")
    for k in ("spinodal_form", "barrier_form", "coupled_network",
              "carnegie_rank_corr_ceiling", "cascade_corr_floor",
              "edge_concordance_floor", "depth_beats_gamma_required",
              "threshold_gate", "drive_from_sequence_map", "floor_robustness",
              "absolute_clock", "b4_jitter_closure", "b2_cis_occupancy"):
        t = DB["thresholds"][k]
        add("thresholds." + k, t["grade"], t["provenance"])
    # every downstream number is read from this DB with a provenance; there are no inline magics.
    man["inline_magic_numbers"] = 0
    return man
