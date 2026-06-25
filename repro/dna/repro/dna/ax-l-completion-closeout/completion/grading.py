# -*- coding: utf-8 -*-
"""
completion.grading -- the honest claim-by-claim ledger for Appendix L (the blueprint close-out).

Every claim the appendix makes, with its grade and the function that backs it. The gate audits that
nothing graded [V] is unsupported and -- critically -- that the O1/B4 absolute-strength row stays
[L] (never quietly upgraded to [V] just because B4 made it jitter-robust), AND that the B2 row stays
[F]/data-blocked (never quietly upgraded to [L]).

Grade key: [L] locked real data / measured empirical; [V] exact logical invariant of the substrate;
[F] declared modelling choice; [O] open / out of scope.
"""
from . import lock, cascade, coupled, nulltest, timing, declaration, cis


def ledger():
    is_dag, _ = cascade.is_dag()
    null = nulltest.the_null()
    conc = nulltest.edge_concordance()
    beats = nulltest.depth_beats_gamma()
    chain = nulltest.axial_chain_still_strong()
    abl = nulltest.floor_retest_ablation()
    jit = nulltest.floor_retest_jitter()
    b4 = nulltest.b4_jitter_closed()
    b2 = cis.occupancy_probe()
    poc = coupled.or_partial_order_compliance()
    thr = coupled.threshold_k_wavefront(alpha=1.0)
    andd = coupled.and_delays_convergent_nodes()
    seq = coupled.sequence_drive_preserves_order()
    cvk = coupled.coupled_vs_keys()
    sub = timing.segmentation_subclock()
    gc = timing.global_clock()

    rows = [
        # ---- inheritance backbone ----
        {"id": "J1", "claim": "38 inherited driver gamma byte-identical to Appendix I; SantaLucia "
                              "NN table + operator (gamma, A4=robust_z) unchanged; 25 NEW genes are "
                              "real GRCh38", "grade": "[L]",
         "backing": "lock.driver_gamma + gate.J1 (4 skeletal drivers + 38-gamma byte check vs parent "
                    "param_db)"},
        {"id": "J2", "claim": "the FILLED regulatory cascade (63 genes / 62 edges) is still a DAG",
         "grade": "[V]", "backing": "cascade.is_dag = %s" % is_dag},
        # ---- O1: gene-set fill, floor re-test ----
        {"id": "J3", "claim": "single-locus spinodal(gamma) still does NOT order Carnegie staging",
         "grade": "[V]", "backing": "nulltest.the_null: rho=%.3f in +/-%.2f band"
                                    % (null["spearman_spinodal_vs_carnegie"], null["null_ceiling"])},
        {"id": "J4", "claim": "every cited regulatory edge agrees with cited temporal order (zero "
                              "inversions) on the filled kit", "grade": "[V]",
         "backing": "nulltest.edge_concordance: %d inversions over %d anchored edges"
                    % (conc["n_inversions"], conc["n_cited_edges_both_anchored"])},
        {"id": "J5", "claim": "cascade depth predicts order strictly better than gamma, now ABOVE "
                              "the floor", "grade": "[V]",
         "backing": "nulltest.depth_beats_gamma: %.3f vs %.3f (all)"
                    % (beats["spearman_depth_vs_carnegie_all"],
                       beats["spearman_spinodal_vs_carnegie_all"])},
        {"id": "O1", "claim": "ABSOLUTE depth<->Carnegie strength REACHES the pre-registered 0.70 "
                              "floor globally on the filled kit (both named fixes required)",
         "grade": "[L] met=%s (%.3f); empirical -- not a logical invariant (B3 ceiling)"
                  % (abl["meets_floor_on_filled_kit"], abl["scope_c_plus_full_hox"]["spearman"]),
         "backing": "nulltest.floor_retest_ablation (inherited %.3f -> filled %.3f; limb-only %.3f, "
                    "HOX-only %.3f)"
                    % (abl["scope_a_inherited_kit"]["spearman"],
                       abl["scope_c_plus_full_hox"]["spearman"],
                       abl["scope_b_plus_limb_inducers"]["spearman"],
                       abl["scope_d_hox_only_limb_ablated"]["spearman"])},
        {"id": "B4", "claim": "the floor is now JITTER-ROBUST: the cited MEOX1->PAX7 source-fix lifts "
                              "the +-1 rank-jitter p5 above the 0.70 floor (no longer marginal), with "
                              "0 new inversions and the DAG preserved",
         "grade": "[L] CLOSED met=%s (p5 %.3f >= %.2f); jitter-robust empirical -- NEVER [V]"
                  % (b4["b4_closed"], jit["p5"], jit["floor"]),
         "backing": "nulltest.b4_jitter_closed (edge %s, ranks %s/%s tie-concordant, %d inversions, "
                    "dag=%s) + floor_retest_jitter (mean %.3f, p5 %.3f, frac>=floor %.3f) + ablation "
                    "scope_e %.3f"
                    % (b4["closure_edge"], b4["rank_parent"], b4["rank_child"],
                       b4["n_edge_inversions"], b4["cascade_is_dag"],
                       jit["mean"], jit["p5"], jit["frac_at_or_above_floor"],
                       abl["scope_e_plus_b4_myogenic_edge"]["spearman"])},
        {"id": "B2", "claim": "the per-edge cis-code -> drive is NOT readable from the proximal "
                              "+-2 kb promoter window (the canonical SOX9-|RUNX2 edge is below a "
                              "dinucleotide-shuffle background); B2 is DATA-BLOCKED by measurement",
         "grade": "[F] data-blocked -- NOT [L]; W=sqrt(gamma) stays [F]; needs distal-enhancer data",
         "backing": "cis.occupancy_probe (%d/%d edges above background, mean z %.2f, SOX9->RUNX2 "
                    "z %.2f below background, data_blocked=%s)"
                    % (b2["n_above_background"], b2["n_edges_scored"], b2["mean_z"],
                       b2["canonical_SOX9_represses_RUNX2"]["z"], b2["b2_data_blocked"])},
        {"id": "J6", "claim": "the grammar is at least as sharp on the wired axial trunk as globally",
         "grade": "[V]", "backing": "nulltest.axial_chain_still_strong: chain %.3f vs global %.3f"
                                    % (chain["spearman_on_axial_chain"], chain["spearman_global"])},
        # ---- coupled-R19 theorem on the filled kit ----
        {"id": "J7", "claim": "coupled-R19 OR firing respects the cascade DAG (wavefront theorem) "
                              "on 63 genes", "grade": "[V]",
         "backing": "coupled.or_partial_order_compliance: %d violations" % poc["n_violations"]},
        {"id": "J8", "claim": "coupled firing order tracks cascade depth, not bare spinodal",
         "grade": "[V]", "backing": "coupled.coupled_vs_keys: depth_beats_gamma=%s (%.3f vs %.3f)"
                                    % (cvk["depth_beats_gamma"],
                                       cvk["spearman_firing_vs_cascade_depth"],
                                       cvk["spearman_firing_vs_bare_spinodal"])},
        # ---- GATE: quorum / AND threshold-k ----
        {"id": "G1", "claim": "the OR-gate wavefront generalises to a QUORUM/AND threshold-k gate "
                              "(k_i=max(1,ceil(alpha*indeg))) with the partial order intact",
         "grade": "[V]", "backing": "coupled.threshold_k_wavefront(alpha=1): %d violations; OR=k=1"
                                    % thr["n_violations"]},
        {"id": "G2", "claim": "convergent nodes never fire EARLIER under AND than under OR",
         "grade": "[V]", "backing": "coupled.and_delays_convergent_nodes: never_earlier=%s"
                                    % andd["and_never_earlier_than_or"]},
        # ---- O3: sequence -> drive ----
        {"id": "O3", "claim": "per-edge drive read from the promoter sequence (sqrt(gamma) ON-branch "
                              "amplitude) instead of uniform W=1", "grade": "[F]",
         "backing": "lock.drive_map_cfg (declared modelling choice); sqrt(gamma) range %s"
                    % str(seq["sqrt_gamma_range"])},
        {"id": "O3b", "claim": "sequence-derived drive PRESERVES the cascade firing order",
         "grade": "[V]", "backing": "coupled.sequence_drive_preserves_order: %d OR-violations, "
                                    "order rho=%.3f" % (seq["or_wavefront_violations_under_sequence"],
                                                        seq["spearman_order_uniform_vs_sequence"])},
        # ---- O2: absolute timing ----
        {"id": "O2", "claim": "cascade ORDER converts to approximate DAYS via the measured "
                              "segmentation-clock period + Carnegie stage-day table", "grade": "[L]",
         "backing": "timing.segmentation_subclock: %.2f d span, consistent with cited window %s"
                    % (sub["predicted_somitogenesis_days"],
                       str(sub["cited_window_CS9_to_CS13_days"]))},
        {"id": "O2b", "claim": "ONE global zero-point pins ALL genes to absolute days via TWO "
                              "INDEPENDENT measured anchors (segmentation oscillator SLOPE + "
                              "first-heartbeat INTERCEPT), validated OUT-OF-SAMPLE (B1 closed)",
         "grade": "[L] closed (held-out, 0 free params) -- a MEASUREMENT, never [V]",
         "backing": "timing.global_clock: b1_closed=%s; held-out stages max %.2f d (n=%d), %d "
                    "held-out genes max %.2f d, 0 free params; cardiac anchor corroborates table"
                    % (gc["b1_closed"], gc["heldout_stage_validation"]["max_abs_err_days"],
                       gc["heldout_stage_validation"]["n_held_out"],
                       gc["heldout_gene_validation"]["n_genes"],
                       gc["heldout_gene_validation"]["max_abs_err_days"])},
        # ---- scope ----
        {"id": "S1", "claim": "a built / simulated human or organ", "grade": "[O] out of scope",
         "backing": "principle demonstration on 63 real promoters; non-clinical"},
    ]
    n_v = sum(1 for r in rows if r["grade"].startswith("[V]"))
    n_l = sum(1 for r in rows if r["grade"].startswith("[L]"))
    n_f = sum(1 for r in rows if r["grade"].startswith("[F]"))
    n_o = sum(1 for r in rows if r["grade"].startswith("[O]"))

    # HARD self-audit: the O1 row must be CLASSIFIED [L], never [V].
    o1_row = next(r for r in rows if r["id"] == "O1")
    o1_is_L_not_V = o1_row["grade"].startswith("[L]") and not o1_row["grade"].startswith("[V]")
    # HARD self-audit: the B4 closure row must stay [L], never [V] (B3 ceiling).
    b4_row = next(r for r in rows if r["id"] == "B4")
    b4_is_L_not_V = (b4_row["grade"].startswith("[L]") and not b4_row["grade"].startswith("[V]")
                     and bool(b4["b4_closed"]))
    # HARD self-audit: the B2 row must stay [F]/data-blocked, NEVER [L] (no false closure).
    b2_row = next(r for r in rows if r["id"] == "B2")
    b2_is_not_L = (not b2_row["grade"].startswith("[L]")) and bool(b2["b2_data_blocked"])
    # HARD self-audit: the absolute-clock row (O2b) must also stay [L], never [V].
    o2b_row = next(r for r in rows if r["id"] == "O2b")
    global_clock_is_L_not_V = (o2b_row["grade"].startswith("[L]")
                               and not o2b_row["grade"].startswith("[V]")
                               and gc["grade"].startswith("[L]")
                               and not gc["grade"].startswith("[V]"))

    return {"rows": rows,
            "counts": {"V": n_v, "L": n_l, "F": n_f, "O": n_o},
            "o1_is_L_not_V": o1_is_L_not_V,
            "b4_is_L_not_V": b4_is_L_not_V,
            "b2_is_not_L": b2_is_not_L,
            "global_clock_is_L_not_V": global_clock_is_L_not_V,
            "physical_complete": declaration.declare()["physical_complete"]}


def read():
    return ledger()
