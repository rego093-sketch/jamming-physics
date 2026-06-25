# -*- coding: utf-8 -*-
"""
completion.grammar -- THE HIGHER-ORDER GRAMMAR, re-stated on the FILLED kit.

Appendix I named the order grammar but had to leave its single pre-registered quantitative target
(the 0.70 absolute-strength floor on corr(cascade-depth, Carnegie-onset-rank)) UNMET globally --
not because the grammar was wrong, but because the kit was sparse (limb-bud inducers absent => some
limb genes were artificial cascade sources; the HOX kit was group-13-only). Appendix J fills exactly
those NAMED gaps with REAL GRCh38 promoter gamma and the cited limb / HOX collinear edges, and
RE-TESTS the same floor. The grammar statement itself is UNCHANGED; only its evidence is now closed.

  THE ORDER GRAMMAR (G3 on the time axis) -- identical to Appendix I:
  --------------------------------------------------------------------------------------------
    emergence_order  =  toposort( regulatory-cascade DAG )   modulated by   barrier(gamma)=gamma^2/4
  --------------------------------------------------------------------------------------------

  It is NOT a new layer. It is the already-identified architecture/wiring grammar G3 -- the same
  cited parent->child edges -- read along TIME instead of space:

    * PRIMARY key  = cascade DEPTH (a global NETWORK property): a gene cannot emerge until its
                     upstream regulators have fired (the coupled-R19 wavefront theorem,
                     completion.coupled). Now measured over 63 genes / 62 edges.
    * TIE-BREAK    = the LOCAL cusp barrier gamma^2/4: within one cascade tier (equal depth,
                     co-regulated) the stiffer promoter trails the softer one. gamma keeps its
                     Appendix-A meaning, demoted from global clock to local within-tier modifier.

  WHAT APPENDIX J ADDS to the statement (evidence, not grammar):
    * O1  the absolute floor is now RE-TESTED on the filled kit and is MET globally
          (~0.755 vs the 0.475 inherited value), and the lift is shown to require BOTH named fixes
          (limb inducers AND full HOX), with a jitter band that keeps the claim honest -> [L].
    * O2  cascade ORDER is converted to approximate DAYS by attaching the real measured
          segmentation-clock period and Carnegie stage-day table (completion.timing) -> sub-clock
          [L], the single global zero-point still [O].
    * O3  per-edge drive is read off the promoter sequence (ON-branch amplitude sqrt(gamma))
          rather than a uniform W=1; firing order is PRESERVED (completion.coupled) -> wiring
          weights now come from sequence, a declared modelling choice [F] whose order-invariance
          is [V].
    * GATE the OR-gate wavefront is generalised to a QUORUM / AND threshold-k gate; the partial
          order still holds (completion.coupled) -> [V], OR being the k=1 special case.

  WHY "처음부터" (from the R19 substrate) -- unchanged: every switch sits on its OFF low branch
  s=-sqrt(gamma) with a sub-spinodal baseline, so the ONLY route to ON is an ON parent; firing
  order is FORCED to respect the cascade partial order. A theorem of the substrate, not a fit.

  THE RESORT LEVERS (the grammar is a live function, not a fixed list) -- unchanged:
    * cut a regulatory edge   -> the unblocked gene emerges EARLIER (depth shrinks).
    * change a promoter gamma  -> reorders only WITHIN a tier (the barrier tie-break), never across
      a cascade level: depth dominates gamma.
"""
from . import lock, cascade, nulltest, coupled, timing


def statement():
    return {
        "single_locus_order_key": "spinodal(gamma) = 2*(gamma/3)^1.5   (Appendix A; the NULL here)",
        "higher_order_order_grammar":
            "emergence_order = toposort(regulatory-cascade DAG) modulated by barrier(gamma)=gamma^2/4",
        "primary_key": "cascade DEPTH (network property: #regulators in series upstream)",
        "tiebreak_key": "local cusp barrier gamma^2/4 (within-tier, stiffer trails softer)",
        "is_new_layer": False,
        "identity": "the architecture/wiring grammar G3, read on the TIME axis (not a new operator)",
        "substrate_reason":
            "OFF=low branch s=-sqrt(gamma); sub-spinodal baseline => only an ON parent can flip a "
            "child => firing respects the cascade partial order (a theorem, completion.coupled).",
        "unchanged_from_appendix_I": True,
        "what_completion_adds": "evidence that closes O1/O2/O3/GATE -- the statement is identical.",
    }


def composite_order_table():
    """The COMPOSITE order (depth primary, barrier gamma^2/4 tie-break) for every driver gene."""
    return cascade.order_table()


def floor_now_met():
    """O1: the pre-registered 0.70 absolute-strength floor, RE-TESTED on the filled kit.

    Reports the nested-scope ablation (inherited / +limb / +full-HOX / HOX-only) and the rank-jitter
    band, both from nulltest (no new numbers). Graded [L]: an empirical correlation on cited data
    that REACHES the floor, NOT a logical invariant -- it must never be promoted to [V]."""
    abl = nulltest.floor_retest_ablation()
    jit = nulltest.floor_retest_jitter()
    return {
        "preregistered_floor": abl["preregistered_absolute_floor"],
        "inherited_kit_spearman": abl["scope_a_inherited_kit"]["spearman"],
        "filled_kit_spearman": abl["scope_c_plus_full_hox"]["spearman"],
        "meets_floor_on_filled_kit": abl["meets_floor_on_filled_kit"],
        "requires_both_fixes": (not abl["scope_b_plus_limb_inducers"]["meets_floor"]
                                and not abl["scope_d_hox_only_limb_ablated"]["meets_floor"]
                                and abl["scope_c_plus_full_hox"]["meets_floor"]),
        "jitter_mean": jit["mean"],
        "jitter_p5": jit["p5"],
        "jitter_frac_ge_floor": jit["frac_at_or_above_floor"],
        "grade": "[L] the ABSOLUTE depth<->Carnegie strength now REACHES the pre-registered 0.70 "
                 "floor globally on the filled kit, requiring BOTH named fixes; the jitter band "
                 "keeps it honest. Empirical on cited ranks -- NOT promoted to [V].",
    }


def early_regime_is_sharper():
    """Quantify '초기단계에 더 큰 문법': the depth<->Carnegie agreement is at least as sharp on the
    wired axial chain as globally (canalization at the trunk). From nulltest (no new numbers)."""
    res = nulltest.axial_chain_still_strong()
    return {
        "axial_chain": res["axial_chain"],
        "spearman_on_axial_chain": res["spearman_on_axial_chain"],
        "spearman_global": res["spearman_global"],
        "sharper_or_equal_on_chain": res["sharper_or_equal_on_chain"],
        "grade": "[V] the order grammar is at least as sharp on the wired axial trunk as globally; "
                 "now the global value itself clears the floor.",
    }


def order_to_days():
    """O2: the order grammar, converted to absolute DAYS. The segmentation sub-clock is [L]
    (inherited); the global zero-point is now CLOSED [L] in Appendix K via two measured anchors
    (completion.timing.global_clock), validated out-of-sample."""
    sub = timing.segmentation_subclock()
    gc = timing.global_clock()
    return {
        "segmentation_subclock_days": sub["predicted_somitogenesis_days"],
        "cited_window_days": sub["cited_window_CS9_to_CS13_days"],
        "subclock_consistent": sub["prediction_in_cited_window_pm2d"],
        "global_zero_point_closed": gc["b1_closed"],
        "calibration": gc["calibration"],
        "heldout_stage_max_err_days": gc["heldout_stage_validation"]["max_abs_err_days"],
        "heldout_gene_max_err_days": gc["heldout_gene_validation"]["max_abs_err_days"],
        "grade": "[L] the segmentation sub-clock predicts a somitogenesis span consistent with the "
                 "cited Carnegie window AND the global zero-point is pinned by two independent "
                 "measured anchors (B1 closed), reproducing held-out stage/gene days within the "
                 "somite-clock window. A MEASUREMENT, never [V]; the post-somitogenesis single-rate "
                 "drift and the origin of the rates are disclosed firewall bounds.",
    }


def drive_from_sequence():
    """O3: per-edge drive read off the promoter sequence (ON-branch amplitude sqrt(gamma)) instead
    of a uniform weight. Firing order is PRESERVED (completion.coupled). [F] choice, [V] invariance."""
    seq = coupled.sequence_drive_preserves_order()
    return {
        "weight_rule": "W_edge = sqrt(gamma_parent)  (R19 ON-branch fixed-point amplitude)",
        "sqrt_gamma_range": seq["sqrt_gamma_range"],
        "or_wavefront_violations": seq["or_wavefront_violations_under_sequence"],
        "firing_order_rho_uniform_vs_sequence": seq["spearman_order_uniform_vs_sequence"],
        "order_preserved": seq["order_preserved"],
        "grade": "[F] wiring weights now come from the promoter sequence (a declared modelling "
                 "choice, sqrt(gamma) ON-branch); [V] this preserves the cascade firing order.",
    }


def quorum_gate():
    """GATE: the OR-gate wavefront generalised to a QUORUM / AND threshold-k gate. Partial order
    still holds (completion.coupled). [V], OR being the k=1 special case."""
    thr = coupled.threshold_k_wavefront(alpha=1.0)
    return {
        "gate_rule": "child fires when >= k_i parents are ON, k_i = max(1, ceil(alpha*indegree))",
        "alpha": 1.0,
        "and_wavefront_violations": thr["n_violations"],
        "order_preserved_under_AND": thr["respects_threshold_k_wavefront"],
        "or_is_special_case": "k_i=1 (alpha->0) recovers the Appendix-I OR-gate wavefront",
        "grade": "[V] the cascade partial order survives a QUORUM/AND threshold-k gate; the "
                 "Appendix-I OR-gate is the k=1 special case.",
    }


def resort_levers():
    return {
        "wiring_resort": "cut a regulatory edge -> unblocked gene emerges earlier (depth shrinks)",
        "barrier_resort": "change a promoter gamma -> reorders only WITHIN a cascade tier (the "
                          "gamma^2/4 tie-break); depth dominates gamma, so it never crosses a level",
        "grade": "[V] emergence order is a live function of the WIRING + local barrier, not a list.",
    }


def read():
    return {
        "statement": statement(),
        "floor_now_met": floor_now_met(),
        "early_regime_is_sharper": early_regime_is_sharper(),
        "order_to_days": order_to_days(),
        "drive_from_sequence": drive_from_sequence(),
        "quorum_gate": quorum_gate(),
        "resort_levers": resort_levers(),
        "composite_order_first10": composite_order_table()[:10],
    }
