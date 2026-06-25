# -*- coding: utf-8 -*-
"""
order.declaration -- the HONEST scope declaration for Appendix I. No false victory.

What this appendix CLOSED, and what it left OPEN, stated in the firewall's own grades. The point
of the appendix is to fill the schedule-ORDER [O] that Appendix H flagged, WITHOUT pretending the
absolute developmental clock (days) is solved or that a body was built.
"""
from . import lock, nulltest


def declare():
    null = nulltest.the_null()
    conc = nulltest.edge_concordance()
    beats = nulltest.depth_beats_gamma()
    resid = nulltest.absolute_strength_residual()

    closed = [
        {
            "claim": "single-locus spinodal(gamma) does NOT predict Carnegie staging order",
            "evidence": "Spearman(spinodal, Carnegie) = %.3f, inside +/-%.2f null band"
                        % (null["spearman_spinodal_vs_carnegie"], null["null_ceiling"]),
            "grade": "[V] (a measured null, reproducing Appendix A in numbers)",
        },
        {
            "claim": "the cascade WIRING read on the time axis IS the order grammar -- every cited "
                     "regulatory edge agrees with the cited temporal order",
            "evidence": "%d/%d cited edges concordant incl ties, %d inversions"
                        % (conc["n_concordant_child_later"] + conc["n_ties_same_tier"],
                           conc["n_cited_edges_both_anchored"], conc["n_inversions"]),
            "grade": "[V]",
        },
        {
            "claim": "cascade DEPTH predicts emergence order strictly better than local stiffness",
            "evidence": "Spearman(depth, Carnegie)=%.3f vs spinodal=%.3f (all); %.3f vs %.3f (main "
                        "component)" % (beats["spearman_depth_vs_carnegie_all"],
                                        beats["spearman_spinodal_vs_carnegie_all"],
                                        beats["spearman_depth_vs_carnegie_main_component"],
                                        beats["spearman_spinodal_vs_carnegie_main_component"]),
            "grade": "[V] (direction); see OPEN for absolute strength",
        },
        {
            "claim": "in the coupled-R19 substrate the firing order respects the cascade DAG "
                     "(no gene fires before its earliest regulator) -- a theorem, not a fit",
            "evidence": "order.coupled.partial_order_compliance: 0 violations",
            "grade": "[V]",
        },
    ]

    open_items = [
        {
            "claim": "ABSOLUTE depth<->Carnegie rank STRENGTH (a strong global correlation)",
            "status": "pre-registered floor %.2f NOT met globally (%.3f); met only on the linear "
                      "axial chain (%.3f). Dilution is named (limb-bud artificial sources; "
                      "HOX group-13-only)." % (resid["preregistered_absolute_floor"],
                                               resid["spearman_depth_vs_carnegie_all"],
                                               resid["spearman_depth_vs_carnegie_axial_chain"]),
            "grade": "[L] moderate, scope-limited -- NOT [V]",
        },
        {
            "claim": "ABSOLUTE developmental timing (onset in days / hours, not just rank order)",
            "status": "the cascade fixes ORDER; converting order to a real clock needs rates the "
                      "firewall does not grant. Untouched.",
            "grade": "[O] open",
        },
        {
            "claim": "per-gene cis-regulatory CODE -> drive (h_i) from sequence",
            "status": "edge weights are UNIFORM (W=1), declared not derived; deriving real drive "
                      "from each promoter/enhancer is future work.",
            "grade": "[O] open",
        },
        {
            "claim": "a built or simulated human / organ",
            "status": "NOT attempted and NOT claimed. This is a principle demonstration on 38 real "
                      "driver promoters, non-clinical.",
            "grade": "[O] out of scope",
        },
    ]

    return {
        "appendix": "I -- developmental ORDER grammar",
        "headline": "The predictor of Carnegie ORDER is regulatory-cascade hierarchy DEPTH (the "
                    "G3 wiring grammar on the time axis), composited with the local barrier "
                    "gamma^2/4 as a within-tier tie-break -- NOT the single-locus spinodal(gamma).",
        "closed": closed,
        "open": open_items,
        "schedule_order_O_closed": True,        # Appendix H's schedule-ORDER [O] is now filled
        "absolute_timing_open": True,           # absolute clock stays [O]
        "physical_complete": False,             # no false victory
        "consciousness_claim": 0,
        "honest_summary":
            "Order: predicted and validated at the edge/rank level (direction [V]); absolute rank "
            "strength [L], strongest on the wired trunk. Absolute timing and cis-code->drive remain "
            "[O]. physical_complete=False. No body was built.",
    }
