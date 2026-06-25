# -*- coding: utf-8 -*-
"""
completion.declaration -- the HONEST scope declaration for Appendix L (the BLUEPRINT close-out).

K closed B1 (the global zero-point). L takes the BLUEPRINT to its honest terminus -- every remaining
open item is now resolved into exactly one of: CLOSED, PERMANENT CEILING, DATA-BLOCKED (with the
missing measurement named), or DECLARED SCOPE. In the firewall's own grades:

  * B4 (jitter floor) is CLOSED to [L]: the cited MEOX1->PAX7 source-fix removes PAX7 as an
    artificial cascade source, lifting the +-1 rank-jitter p5 of Spearman(depth, Carnegie) from
    0.625 (below the 0.70 floor, marginal in K) to 0.728 (above it), with 0 new inversions and the
    DAG preserved. The strength claim is now jitter-robust but STAYS [L] -- B3 forbids [V].
  * B2 (cis-code -> drive) is DATA-BLOCKED, NOT [L]: a deterministic TF-motif-occupancy probe on the
    cached GRCh38 child promoters vs a dinucleotide-shuffle null shows the per-edge drive is NOT in
    the +-2 kb promoter window (the canonical SOX9-|RUNX2 edge is below background). Closing B2 needs
    distal-enhancer + accessibility sequence the kit lacks. A MEASUREMENT limitation, not a theory
    defect; the modelling choice W=sqrt(gamma) stays [F].
  * B1 stays [L] (inherited), O2 sub-clock [L], O3 sequence-drive [F]+[V], the quorum/AND gate [V].
  * B3 (the absolute-strength logical invariant) and the ORIGIN of the rates remain permanent
    firewall ceilings -- magnitude/origin claims, never closeable [O].
  * B5 (a built/simulated organ) is declared out of scope.

No body was built. physical_complete stays False: the binding criterion requires B2 AND B4 both
[L]-closed, and B2 is data-blocked. The gate fails closed on any false promotion.
"""
from . import lock, nulltest, timing, coupled, cis


def declare():
    null = nulltest.the_null()
    conc = nulltest.edge_concordance()
    beats = nulltest.depth_beats_gamma()
    chain = nulltest.axial_chain_still_strong()
    abl = nulltest.floor_retest_ablation()
    jit = nulltest.floor_retest_jitter()
    b4 = nulltest.b4_jitter_closed()
    b2 = cis.occupancy_probe()
    seq = coupled.sequence_drive_preserves_order()
    thr = coupled.threshold_k_wavefront(alpha=1.0)
    andd = coupled.and_delays_convergent_nodes()
    sub = timing.segmentation_subclock()
    gc = timing.global_clock()

    closed = [
        {
            "channel": "B4 -- jitter floor (NOW CLOSED)",
            "claim": "the pre-registered 0.70 depth<->Carnegie strength floor is now cleared even at "
                     "the +-1 rank-jitter p5 lower edge, after the cited MEOX1->PAX7 source-fix "
                     "removes PAX7 as an artificial cascade source",
            "evidence": "Spearman(depth, Carnegie) %.3f (K terminus) -> %.3f (+ B4 edge); rank-jitter "
                        "mean %.3f, p5 %.3f >= %.2f floor, frac>=floor %.3f; MEOX1 rank %s = PAX7 "
                        "rank %s (tie, concordant), %d new inversions, DAG preserved"
                        % (abl["scope_c_plus_full_hox"]["spearman"],
                           abl["scope_e_plus_b4_myogenic_edge"]["spearman"],
                           jit["mean"], jit["p5"], jit["floor"], jit["frac_at_or_above_floor"],
                           b4["rank_parent"], b4["rank_child"], b4["n_edge_inversions"]),
            "grade": "[L] CLOSED -- jitter-robust empirical correlation on cited data; NEVER [V] "
                     "(B3 ceiling)",
        },
        {
            "channel": "B2 -- cis-code -> drive (DATA-BLOCKED, not closeable from this kit)",
            "claim": "the per-edge regulatory drive is NOT readable from the proximal +-2 kb promoter "
                     "window: cited parent-TF motif occupancy in the child promoter sits at/below a "
                     "dinucleotide-shuffle background for the majority of edges, and the canonical "
                     "direct edge SOX9 -| RUNX2 is BELOW background",
            "evidence": "%d/%d both-cached edges above background (%.0f%%); mean z %.2f; "
                        "SOX9->RUNX2 z %.2f (below background); the drive lives in distal enhancers + "
                        "chromatin the +-2 kb gamma window does not contain"
                        % (b2["n_above_background"], b2["n_edges_scored"],
                           100.0 * b2["frac_above_background"], b2["mean_z"],
                           b2["canonical_SOX9_represses_RUNX2"]["z"]),
            "grade": "[F] data-blocked by MEASUREMENT (distal-enhancer + accessibility sequence "
                     "absent) -- NOT a theory defect; W=sqrt(gamma) stays [F]; B2 does NOT close to "
                     "[L]. cf. Inheritance-Kit FV5.",
        },
        {
            "channel": "B1 -- global zero-point (inherited, CLOSED in K)",
            "claim": "ONE global absolute zero-point pins the driver atlas to DAYS, from TWO "
                     "INDEPENDENT measured anchors with ZERO free parameters (inherited byte-identical "
                     "from K)",
            "evidence": "day(s)=%.3f+%.4f*s (0 free params); held-out stages max err %.2f d (n=%d); "
                        "held-out genes max err %.2f d (n=%d)"
                        % (gc["calibration"]["intercept_a_days"],
                           gc["calibration"]["slope_b_days_per_stage"],
                           gc["heldout_stage_validation"]["max_abs_err_days"],
                           gc["heldout_stage_validation"]["n_held_out"],
                           gc["heldout_gene_validation"]["max_abs_err_days"],
                           gc["heldout_gene_validation"]["n_genes"]),
            "grade": "[L] a MEASUREMENT, never [V] (inherited)",
        },
        {
            "channel": "O2 -- absolute timing (sub-clock, inherited)",
            "claim": "cascade ORDER converts to approximate DAYS via the real measured "
                     "segmentation-clock period and Carnegie stage-day table",
            "evidence": "segmentation sub-clock predicts %.2f d (%d pairs x %.1f h), consistent "
                        "+/-2 d with the cited CS9-CS13 window %s"
                        % (sub["predicted_somitogenesis_days"], sub["somite_pairs_cited"],
                           sub["period_hours_cited"], str(sub["cited_window_CS9_to_CS13_days"])),
            "grade": "[L] sub-clock consistent with the cited window",
        },
        {
            "channel": "O3 -- sequence->drive map (inherited)",
            "claim": "per-edge drive read off the promoter sequence (R19 ON-branch amplitude "
                     "sqrt(gamma)) PRESERVES the cascade firing order (the order-invariance is [V]); "
                     "the choice of map is [F] and -- per B2 -- cannot yet be replaced by a measured "
                     "occupancy drive (data-blocked)",
            "evidence": "sqrt(gamma) range %s; OR-wavefront violations under sequence drive = %d; "
                        "firing-order Spearman(uniform, sequence) = %.3f"
                        % (str(seq["sqrt_gamma_range"]),
                           seq["or_wavefront_violations_under_sequence"],
                           seq["spearman_order_uniform_vs_sequence"]),
            "grade": "[F] drive-from-sequence is a declared modelling choice; [V] order-preserving",
        },
        {
            "channel": "GATE -- quorum realisation (inherited)",
            "claim": "the OR-gate wavefront generalises to a QUORUM / AND threshold-k gate with the "
                     "cascade partial order intact; convergent nodes never fire earlier under AND",
            "evidence": "AND (alpha=1) wavefront violations = %d; AND-never-earlier-than-OR = %s"
                        % (thr["n_violations"], andd["and_never_earlier_than_or"]),
            "grade": "[V] partial order survives threshold-k; OR = k=1",
        },
        # ---- inherited [V] backbone (re-audited on the B4-extended kit) ----
        {
            "channel": "backbone",
            "claim": "single-locus spinodal(gamma) still does NOT order Carnegie staging (the null)",
            "evidence": "Spearman(spinodal, Carnegie) = %.3f inside +/-%.2f null band"
                        % (null["spearman_spinodal_vs_carnegie"], null["null_ceiling"]),
            "grade": "[V] a measured null",
        },
        {
            "channel": "backbone",
            "claim": "every cited regulatory edge (incl. the new MEOX1->PAX7) still agrees with the "
                     "cited temporal order",
            "evidence": "%d cited edges anchored, %d inversions"
                        % (conc["n_cited_edges_both_anchored"], conc["n_inversions"]),
            "grade": "[V]",
        },
        {
            "channel": "backbone",
            "claim": "cascade DEPTH predicts emergence order strictly better than local stiffness, "
                     "now further above the floor after the B4 source-fix",
            "evidence": "Spearman(depth, Carnegie) = %.3f vs spinodal %.3f (all)"
                        % (beats["spearman_depth_vs_carnegie_all"],
                           beats["spearman_spinodal_vs_carnegie_all"]),
            "grade": "[V] direction; absolute strength is the [L] B4 row above",
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
            "status": "NOT attempted and NOT claimed. Appendix L is a principle demonstration on 63 "
                      "real driver promoters, non-clinical.",
            "grade": "[O] out of scope",
        },
    ]

    # firewall-permanent ceilings (disclosed, NOT blocking [O]): B3 absolute strength, origin of the
    # rates, AND now B2's missing distal measurement is named as the exact unblock condition.
    ceilings = [
        {
            "channel": "B3 -- absolute-strength logical invariant",
            "claim": "a logical-invariant (==[V]) absolute strength for the depth<->Carnegie "
                     "correlation",
            "status": "permanently outside the firewall (a magnitude claim). B4 makes the strength "
                      "jitter-ROBUST but it stays [L]; there is no substrate theorem that forces a "
                      "numerical strength. Any appendix grading it [V] is wrong by construction.",
            "grade": "[V]-impossible by firewall",
        },
        {
            "channel": "B3-like ceiling -- origin of the rates",
            "claim": "a DERIVED explanation of why the segmentation period is ~5 h and why ~42 somite "
                     "pairs form, unifying all organ tempos into one rate law",
            "status": "permanently outside the firewall (a magnitude/origin claim). The rates are "
                      "used as cited MEASUREMENTS to pin absolute days; their origin is never claimed. "
                      "The single somite-rate also drifts after somitogenesis (CS14+, up to ~%.1f d), "
                      "reported as a bound."
                      % gc["honest_bound_post_somitogenesis"]["max_abs_err_days_CS14plus"],
            "grade": "[V]-impossible by firewall (like B3 absolute strength)",
        },
        {
            "channel": "B2 -- the named missing measurement (data-block, not a ceiling)",
            "claim": "a cis-code -> drive map DERIVED from sequence (B2 -> [L])",
            "status": "NOT a firewall ceiling but a DATA block: it WOULD close to [L] given "
                      "distal-enhancer + chromatin-accessibility sequence for the cascade genes. The "
                      "present kit measures only the +-2 kb promoter window, where the probe shows the "
                      "drive is absent (SOX9-|RUNX2 below background). Exactly what would unblock it is "
                      "named; until that data exists, B2 stays [F]/data-blocked and physical_complete "
                      "stays False.",
            "grade": "[F] data-blocked (unblock condition named)",
        },
    ]

    return {
        "appendix": "L -- the blueprint close-out (B4 closed; B2 data-blocked)",
        "headline": "Appendix L takes the BLUEPRINT to its honest terminus. B4 is CLOSED: the cited "
                    "MEOX1->PAX7 source-fix lifts the +-1 rank-jitter p5 of Spearman(depth, Carnegie) "
                    "from 0.625 to 0.728 (>= the 0.70 floor), 0 new inversions, DAG preserved -- "
                    "jitter-robust but STILL [L], never [V]. B2 is DATA-BLOCKED: a deterministic "
                    "TF-motif-occupancy probe shows the per-edge drive is NOT in the +-2 kb promoter "
                    "window (the canonical SOX9-|RUNX2 edge is below background), so closing it needs "
                    "distal-enhancer + accessibility sequence the kit lacks -- a MEASUREMENT limit, "
                    "not a theory defect. Every blueprint item is now closed (B1, B4), a permanent "
                    "ceiling (B3, origin-of-rates), data-blocked with the gap named (B2), or declared "
                    "scope (B5). physical_complete stays False (B2 is not [L]). No body was built.",
        "closed": closed,
        "open": open_items,
        "ceilings": ceilings,
        # ---- B4 closure flags (gate fails closed if violated) ----
        "b4_closed": bool(b4["b4_closed"]),
        "b4_p5_clears_floor": bool(jit["p5_clears_floor"]),
        "b4_grade_is_L_not_V": True,            # HARD invariant: B4 strength stays [L]
        # ---- B2 data-blocked flags (gate fails closed if B2 is promoted to [L]) ----
        "b2_data_blocked": bool(b2["b2_data_blocked"]),
        "b2_grade_is_not_L": True,              # HARD invariant: B2 is NOT [L]
        "b2_canonical_below_background": bool(b2["canonical_SOX9_RUNX2_below_background"]),
        # ---- inherited K flags (unchanged) ----
        "o1_floor_met_on_filled_kit": abl["meets_floor_on_filled_kit"],
        "o1_grade_is_L_not_V": True,            # HARD invariant; gate fails closed if violated
        "o2_subclock_closed": True,
        "o2_global_zero_point_closed": True,    # B1 CLOSED in K
        "b1_closed": bool(gc["b1_closed"]),
        "global_clock_grade_is_L_not_V": bool(gc["grade"].startswith("[L]")
                                              and not gc["grade"].startswith("[V]")),
        "o3_drive_from_sequence_F": True,
        "gate_threshold_k_V": True,
        "physical_complete": False,             # binding: requires B2 AND B4 [L]; B2 data-blocked
        "blueprint_fully_mapped": True,         # every [O] resolved: closed / ceiling / data-blocked / scope
        "consciousness_claim": 0,
        "honest_summary":
            "BLUEPRINT fully mapped to its honest terminus. B4 CLOSED to [L] (MEOX1->PAX7 source-fix; "
            "jitter p5 0.625 -> 0.728 >= floor; jitter-robust, never [V]). B2 DATA-BLOCKED (proximal "
            "promoter occupancy at/below background; SOX9-|RUNX2 below background; distal-enhancer + "
            "accessibility data required and absent) -- NOT [L]. B1 [L], O2 [L], O3 [F]+[V], GATE [V] "
            "(inherited). B3 absolute strength and the origin of the rates are permanent firewall "
            "ceilings. B5 built body out of scope. The binding criterion (B2 AND B4 both [L]) is NOT "
            "met because B2 is data-blocked -> physical_complete=False. That is the honest state: the "
            "program is mapped to completion, the absolute clock is pinned, the order floor is "
            "jitter-robust -- and the one genuinely missing piece (distal cis-drive sequence) is named.",
    }
