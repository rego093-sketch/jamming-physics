# -*- coding: utf-8 -*-
"""
order.grading -- the honest claim-by-claim ledger for Appendix I.

Every claim the appendix makes, with its grade and the function that backs it. The gate audits that
nothing graded [V] is actually unsupported and that no [O] is quietly upgraded.
"""
from . import lock, cascade, coupled, nulltest, declaration


def ledger():
    is_dag, _ = cascade.is_dag()
    poc = coupled.partial_order_compliance()
    cvk = coupled.coupled_vs_keys()
    roe = coupled.resort_on_edge()
    null = nulltest.the_null()
    conc = nulltest.edge_concordance()
    beats = nulltest.depth_beats_gamma()
    resid = nulltest.absolute_strength_residual()

    rows = [
        {"id": "C1", "claim": "38 driver gamma inherited byte-identical from Appendix H; operator "
                              "(gamma, A4) unchanged", "grade": "[L]",
         "backing": "lock.driver_gamma + gate.I1 (4 skeletal drivers match Appendix G/H)"},
        {"id": "C2", "claim": "the regulatory cascade is a DAG (a topological order exists)",
         "grade": "[V]", "backing": "cascade.is_dag = %s" % is_dag},
        {"id": "C3", "claim": "single-locus spinodal(gamma) does NOT order Carnegie staging",
         "grade": "[V]", "backing": "nulltest.the_null: rho=%.3f in null band"
                                    % null["spearman_spinodal_vs_carnegie"]},
        {"id": "C4", "claim": "every cited regulatory edge agrees with cited temporal order "
                              "(zero inversions)", "grade": "[V]",
         "backing": "nulltest.edge_concordance: %d inversions" % conc["n_inversions"]},
        {"id": "C5", "claim": "cascade depth predicts order strictly better than gamma",
         "grade": "[V]", "backing": "nulltest.depth_beats_gamma: %.3f vs %.3f (all)"
                                    % (beats["spearman_depth_vs_carnegie_all"],
                                       beats["spearman_spinodal_vs_carnegie_all"])},
        {"id": "C6", "claim": "coupled-R19 firing respects the cascade DAG (wavefront theorem)",
         "grade": "[V]", "backing": "coupled.partial_order_compliance: %d violations"
                                    % poc["n_violations"]},
        {"id": "C7", "claim": "coupled firing order tracks cascade depth, not bare spinodal",
         "grade": "[V]", "backing": "coupled.coupled_vs_keys: depth_beats_gamma=%s"
                                    % cvk["depth_beats_gamma"]},
        {"id": "C8", "claim": "emergence order is a live function of the wiring (edge-cut resort)",
         "grade": "[V]", "backing": "coupled.resort_on_edge: RUNX2 earlier=%s"
                                    % roe["runx2_fires_earlier_when_unblocked"]},
        {"id": "C9", "claim": "order grammar is sharpest on the wired axial trunk (canalization)",
         "grade": "[V]", "backing": "nulltest.absolute_strength_residual: chain rho=%.3f vs global "
                                    "%.3f" % (resid["spearman_depth_vs_carnegie_axial_chain"],
                                              resid["spearman_depth_vs_carnegie_all"])},
        # ---- the honest NEGATIVES / OPENS (not [V]) ----
        {"id": "O1", "claim": "ABSOLUTE depth<->Carnegie strength reaches the pre-registered floor "
                              "0.70 globally", "grade": "[L] NOT met globally (%.3f); met on chain "
                              "only" % resid["spearman_depth_vs_carnegie_all"],
         "backing": "reported honestly; absolute strength is [L], not [V]"},
        {"id": "O2", "claim": "absolute developmental timing in days", "grade": "[O] open",
         "backing": "order != clock; rates not granted by firewall"},
        {"id": "O3", "claim": "per-gene cis-code -> drive h_i from sequence", "grade": "[O] open",
         "backing": "edge weights uniform W=1, declared not derived"},
        {"id": "O4", "claim": "a built/simulated human or organ", "grade": "[O] out of scope",
         "backing": "principle demonstration on 38 real promoters; non-clinical"},
    ]
    n_v = sum(1 for r in rows if r["grade"].startswith("[V]"))
    n_l = sum(1 for r in rows if r["grade"].startswith("[L]"))
    n_o = sum(1 for r in rows if r["grade"].startswith("[O]"))
    return {"rows": rows, "counts": {"V": n_v, "L": n_l, "O": n_o},
            "physical_complete": declaration.declare()["physical_complete"]}


def read():
    return ledger()
