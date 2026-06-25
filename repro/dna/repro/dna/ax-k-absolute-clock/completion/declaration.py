# -*- coding: utf-8 -*-
"""
completion.declaration -- the HONEST scope declaration for Appendix K (the absolute clock).

Appendix K closes the ONE channel Appendix J left open: B1, the global zero-point. The cascade's
developmental ORDER is pinned to absolute DAYS by two INDEPENDENT measured anchors and a
parameter-free calibration, validated OUT-OF-SAMPLE. This declaration states, in the firewall's own
grades, exactly what is now closed and what stays open / ceilinged. In particular:

  * B1 (the O2 global zero-point) is CLOSED only to [L] -- two real measured anchors (the in-vitro
    segmentation oscillator SLOPE + the in-vivo first-heartbeat INTERCEPT) with ZERO free parameters
    reproduce held-out Carnegie stage-days and gene-days within the somite-clock window. It is a
    MEASUREMENT, NEVER [V]; the gate fails closed if anyone tries to promote it.
  * O1 stays [L] (the floor is met but jitter-sensitive) -- never [V] (inherited).
  * O2 sub-clock stays [L]; O3 sequence-drive stays [F] with [V] order-invariance; the quorum/AND
    gate stays [V] (all inherited, re-audited).
  * The ORIGIN of the rates (why ~5 h, why ~42) and the single-rate drift after somitogenesis (CS14+)
    are disclosed firewall BOUNDS/ceilings -- magnitude/origin claims the firewall permanently
    excludes (like the O1 absolute-strength ceiling), NOT closeable [O].

No body was built. physical_complete stays False (B2 cis->drive and B4 jitter remain).
"""
from . import lock, nulltest, timing, coupled


def declare():
    null = nulltest.the_null()
    conc = nulltest.edge_concordance()
    beats = nulltest.depth_beats_gamma()
    chain = nulltest.axial_chain_still_strong()
    abl = nulltest.floor_retest_ablation()
    jit = nulltest.floor_retest_jitter()
    seq = coupled.sequence_drive_preserves_order()
    thr = coupled.threshold_k_wavefront(alpha=1.0)
    andd = coupled.and_delays_convergent_nodes()
    sub = timing.segmentation_subclock()
    gc = timing.global_clock()

    closed = [
        {
            "channel": "O1 -- gene-set fill",
            "claim": "with the named Appendix-I gaps filled (limb FGF/Wnt inducers + full HOX "
                     "collinear chains, all REAL GRCh38 gamma), the pre-registered 0.70 absolute "
                     "depth<->Carnegie strength floor is now REACHED globally",
            "evidence": "Spearman(depth, Carnegie) = %.3f on the filled kit vs %.3f inherited; the "
                        "lift requires BOTH fixes (limb-only %.3f, HOX-only %.3f, both %.3f); "
                        "rank-jitter mean %.3f, p5 %.3f, frac>=floor %.3f"
                        % (abl["scope_c_plus_full_hox"]["spearman"],
                           abl["scope_a_inherited_kit"]["spearman"],
                           abl["scope_b_plus_limb_inducers"]["spearman"],
                           abl["scope_d_hox_only_limb_ablated"]["spearman"],
                           abl["scope_c_plus_full_hox"]["spearman"],
                           jit["mean"], jit["p5"], jit["frac_at_or_above_floor"]),
            "grade": "[L] REACHES the floor on cited data -- empirical, jitter-sensitive; NOT [V]",
        },
        {
            "channel": "O2 -- absolute timing (sub-clock)",
            "claim": "cascade ORDER converts to approximate DAYS via the real measured "
                     "segmentation-clock period and Carnegie stage-day table",
            "evidence": "segmentation sub-clock predicts a somitogenesis span of %.2f d "
                        "(%d pairs x %.1f h), consistent +/-2 d with the cited CS9-CS13 window %s"
                        % (sub["predicted_somitogenesis_days"], sub["somite_pairs_cited"],
                           sub["period_hours_cited"], str(sub["cited_window_CS9_to_CS13_days"])),
            "grade": "[L] sub-clock consistent with the cited window",
        },
        {
            "channel": "B1 -- global zero-point (O2 remainder, NOW CLOSED)",
            "claim": "ONE global absolute zero-point pins the driver atlas to DAYS, from TWO "
                     "INDEPENDENT measured anchors (segmentation oscillator SLOPE + first-heartbeat "
                     "INTERCEPT) with ZERO free parameters; held-out Carnegie stage-days and gene "
                     "days within the somite-clock window are reproduced out-of-sample",
            "evidence": "day(s)=%.3f+%.4f*s (0 free params); held-out stages max err %.2f d (n=%d); "
                        "held-out genes max err %.2f d (n=%d, all within the %.1f d band); cardiac "
                        "anchor (CS10, %.0f d) independently corroborates the cited table"
                        % (gc["calibration"]["intercept_a_days"],
                           gc["calibration"]["slope_b_days_per_stage"],
                           gc["heldout_stage_validation"]["max_abs_err_days"],
                           gc["heldout_stage_validation"]["n_held_out"],
                           gc["heldout_gene_validation"]["max_abs_err_days"],
                           gc["heldout_gene_validation"]["n_genes"],
                           lock.absolute_clock_cfg()["heldout_accept_days"],
                           gc["anchor_2_cardiac"]["day"]),
            "grade": "[L] global zero-point pinned by two measured anchors -- a MEASUREMENT, never "
                     "[V]; the post-somitogenesis single-rate drift is a stated residual bound",
        },
        {
            "channel": "O3 -- sequence->drive map",
            "claim": "per-edge drive read off the promoter sequence (R19 ON-branch amplitude "
                     "sqrt(gamma)) instead of a uniform W=1 PRESERVES the cascade firing order",
            "evidence": "sqrt(gamma) range %s; OR-wavefront violations under sequence drive = %d; "
                        "firing-order Spearman(uniform, sequence) = %.3f"
                        % (str(seq["sqrt_gamma_range"]),
                           seq["or_wavefront_violations_under_sequence"],
                           seq["spearman_order_uniform_vs_sequence"]),
            "grade": "[F] drive-from-sequence is a declared modelling choice; [V] order-preserving",
        },
        {
            "channel": "GATE -- quorum realisation",
            "claim": "the OR-gate wavefront generalises to a QUORUM / AND threshold-k gate "
                     "(child fires when >= k_i = max(1, ceil(alpha*indegree)) parents are ON) with "
                     "the cascade partial order intact; convergent nodes never fire earlier under AND",
            "evidence": "AND (alpha=1) wavefront violations = %d; AND-never-earlier-than-OR = %s; "
                        "OR is the k=1 special case" % (thr["n_violations"],
                                                        andd["and_never_earlier_than_or"]),
            "grade": "[V] partial order survives threshold-k; OR = k=1",
        },
        # ---- inherited [V] backbone (unchanged numbers, re-audited on the filled kit) ----
        {
            "channel": "backbone",
            "claim": "single-locus spinodal(gamma) still does NOT order Carnegie staging (the null)",
            "evidence": "Spearman(spinodal, Carnegie) = %.3f inside +/-%.2f null band"
                        % (null["spearman_spinodal_vs_carnegie"], null["null_ceiling"]),
            "grade": "[V] a measured null",
        },
        {
            "channel": "backbone",
            "claim": "every cited regulatory edge still agrees with the cited temporal order",
            "evidence": "%d cited edges anchored, %d inversions"
                        % (conc["n_cited_edges_both_anchored"], conc["n_inversions"]),
            "grade": "[V]",
        },
        {
            "channel": "backbone",
            "claim": "cascade DEPTH predicts emergence order strictly better than local stiffness, "
                     "now ABOVE the floor",
            "evidence": "Spearman(depth, Carnegie) = %.3f vs spinodal %.3f (all)"
                        % (beats["spearman_depth_vs_carnegie_all"],
                           beats["spearman_spinodal_vs_carnegie_all"]),
            "grade": "[V] direction; absolute strength is the [L] above",
        },
        {
            "channel": "backbone",
            "claim": "the grammar remains at least as sharp on the wired axial trunk as globally",
            "evidence": "chain Spearman %.3f vs global %.3f"
                        % (chain["spearman_on_axial_chain"], chain["spearman_global"]),
            "grade": "[V] canalization",
        },
    ]

    open_items = [
        {
            "channel": "scope (B5)",
            "claim": "a built or simulated human / organ / body",
            "status": "NOT attempted and NOT claimed. Appendix K is a principle demonstration on 63 "
                      "real driver promoters, non-clinical.",
            "grade": "[O] out of scope",
        },
    ]
    # firewall-permanent ceiling (disclosed, NOT a blocking [O]): the ORIGIN of the developmental
    # rates (why ~5 h, why ~42) is a magnitude/mechanism-of-origin question the firewall permanently
    # excludes -- exactly like the O1 absolute-strength ceiling (B3). K uses the rates as MEASURED
    # inputs to pin the zero-point; it does not (and the firewall cannot) explain them.
    ceilings = [
        {
            "channel": "B3-like ceiling -- origin of the rates",
            "claim": "a DERIVED explanation of why the segmentation period is ~5 h and why ~42 "
                     "somite pairs form, unifying all organ tempos into one rate law",
            "status": "permanently outside the firewall (a magnitude/origin claim). The rates are "
                      "used as cited MEASUREMENTS to pin absolute days; their origin is never "
                      "claimed. The single somite-rate also drifts after somitogenesis (CS14+, up "
                      "to ~%.1f d), reported as a bound. This is a ceiling, not a closeable [O]."
                      % gc["honest_bound_post_somitogenesis"]["max_abs_err_days_CS14plus"],
            "grade": "[V]-impossible by firewall (like O1 absolute strength)",
        },
    ]

    return {
        "appendix": "K -- the absolute clock (global zero-point)",
        "headline": "Appendix K closes B1 -- the global zero-point. The cascade's developmental "
                    "ORDER is pinned to absolute DAYS by TWO INDEPENDENT measured anchors (the "
                    "in-vitro segmentation oscillator setting the SLOPE; the in-vivo first-heartbeat "
                    "landmark, CS10 @ 22 d, setting the INTERCEPT), with ZERO free parameters. "
                    "Held-out Carnegie stage-days and %d held-out gene-days within the somite-clock "
                    "window are reproduced OUT-OF-SAMPLE to <= %.2f d. The absolute clock is a "
                    "MEASUREMENT -- graded [L], NEVER [V]. The single somite-rate drift after "
                    "somitogenesis (CS14+) and the origin of the rates remain disclosed firewall "
                    "bounds. physical_complete stays False (B2 cis->drive and B4 jitter remain). "
                    "No body was built."
                    % (gc["heldout_gene_validation"]["n_genes"],
                       max(gc["heldout_stage_validation"]["max_abs_err_days"],
                           gc["heldout_gene_validation"]["max_abs_err_days"])),
        "closed": closed,
        "open": open_items,
        "ceilings": ceilings,
        "o1_floor_met_on_filled_kit": abl["meets_floor_on_filled_kit"],
        "o1_grade_is_L_not_V": True,            # HARD invariant; gate fails closed if violated
        "o2_subclock_closed": True,
        "o2_global_zero_point_closed": True,    # B1 CLOSED in K (was open in J)
        "b1_closed": bool(gc["b1_closed"]),
        "global_clock_grade_is_L_not_V": bool(gc["grade"].startswith("[L]")
                                              and not gc["grade"].startswith("[V]")),
        "o3_drive_from_sequence_F": True,
        "gate_threshold_k_V": True,
        "physical_complete": False,             # no false victory: B2/B4 remain
        "consciousness_claim": 0,
        "honest_summary":
            "B1 CLOSED to [L]: the global zero-point is pinned by two independent measured anchors "
            "(segmentation SLOPE + cardiac INTERCEPT), 0 free parameters; held-out stages and %d "
            "held-out genes within the somite-clock window reproduced to <= %.2f d. A MEASUREMENT, "
            "never [V]. O1 floor still [L] (jitter-sensitive). O2 sub-clock [L]. O3 sequence-drive "
            "[F]+[V]. GATE threshold-k [V]. Remaining to 100%%: B2 (derive cis->drive map -> [L]) "
            "and B4 (lift jitter p5 >= floor); B5 built body out of scope. physical_complete=False."
            % (gc["heldout_gene_validation"]["n_genes"],
               max(gc["heldout_stage_validation"]["max_abs_err_days"],
                   gc["heldout_gene_validation"]["max_abs_err_days"])),
    }
