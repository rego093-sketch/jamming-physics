# -*- coding: utf-8 -*-
"""
order.grammar -- THE HIGHER-ORDER GRAMMAR, stated explicitly.

Appendix A..F gave the READING grammars G1..G6 with ONE single-locus operator (LEVEL,SHAPE) =
(gamma, A4): each locus is read in isolation, and the developmental SCHEDULE of Appendix H ordered
switches by spinodal(gamma). Appendix A measured that this single-locus order does NOT match real
Carnegie staging (the "measured null"). This module names the grammar that DOES.

  THE ORDER GRAMMAR (G3 on the time axis):
  --------------------------------------------------------------------------------------------
    emergence_order  =  toposort( regulatory-cascade DAG )   modulated by   barrier(gamma)=gamma^2/4
  --------------------------------------------------------------------------------------------

  It is NOT a new layer. It is the ALREADY-IDENTIFIED architecture/wiring grammar G3 -- the same
  cited parent->child edges -- read along TIME instead of space:

    * PRIMARY key  = cascade DEPTH (how many regulators must fire in series before this gene can):
                     a global NETWORK property. A gene cannot emerge until its upstream drivers
                     have delivered drive (the coupled-R19 wavefront theorem, order.coupled).
    * TIE-BREAK    = the LOCAL cusp barrier gamma^2/4: WITHIN one cascade tier (genes with equal
                     depth, co-regulated), the stiffer promoter (deeper barrier) trails the softer
                     one. gamma keeps its Appendix-A meaning, demoted from global clock to local
                     within-tier modifier. This is the COMPOSITE the user anticipated ("복합적").

  WHY "처음부터" (from the R19 substrate): with every switch on its OFF low branch s=-sqrt(gamma)
  and a sub-spinodal baseline, the ONLY route to ON is an ON parent. So firing order is FORCED to
  respect the cascade partial order -- a theorem of the substrate, not a fit (order.coupled).

  WHY "초기단계에 더 큰 문법" (a bigger grammar early): the grammar is sharpest where the cascade
  is actually wired. Along the linear axial dependency chain (organizer->clock->somite->sclerotome
  ->chondrogenesis->ossification) cascade depth recovers the cited Carnegie order EXACTLY. The
  global correlation is diluted only by NAMED kit-coverage gaps (limb-bud genes whose FGF/Wnt
  inducers are absent are artificial sources; the HOX kit is group-13-only). Canalization at the
  trunk = a tightly-predicted early regime.

  THE RESORT LEVERS (the grammar is a live function, not a fixed list):
    * cut a regulatory edge  -> the unblocked gene emerges EARLIER  (order.coupled.resort_on_edge)
    * change a promoter gamma -> reorders only WITHIN a tier (the barrier tie-break), never across
      a cascade level: depth dominates gamma. (order A vs this appendix.)
"""
from . import lock, cascade, nulltest


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
            "child => firing respects the cascade partial order (a theorem, order.coupled).",
    }


def composite_order_table():
    """The COMPOSITE order (depth primary, barrier gamma^2/4 tie-break) for every driver gene."""
    return cascade.order_table()


def early_regime_is_sharper():
    """Quantify '초기단계에 더 큰 문법': the depth<->Carnegie agreement is strongest on the wired
    axial chain and dilutes globally. Returns the chain correlation, the global correlation, and the
    named dilution sources -- all from nulltest (no new numbers)."""
    res = nulltest.absolute_strength_residual()
    return {
        "axial_chain": res["axial_chain"],
        "spearman_on_axial_chain": res["spearman_depth_vs_carnegie_axial_chain"],
        "spearman_global": res["spearman_depth_vs_carnegie_all"],
        "sharper_early": bool(res["spearman_depth_vs_carnegie_axial_chain"]
                              > res["spearman_depth_vs_carnegie_all"]),
        "named_dilution_sources": res["named_dilution_sources"],
        "grade": "[V] the order grammar is sharpest on the wired axial trunk (canalization) and "
                 "dilutes globally only through NAMED kit-coverage gaps.",
    }


def resort_levers():
    return {
        "wiring_resort": "cut a regulatory edge -> unblocked gene emerges earlier "
                         "(order.coupled.resort_on_edge: SOX9->RUNX2 cut moves RUNX2 earlier)",
        "barrier_resort": "change a promoter gamma -> reorders only WITHIN a cascade tier (the "
                          "gamma^2/4 tie-break); depth dominates gamma, so it never crosses a level",
        "grade": "[V] emergence order is a live function of the WIRING + local barrier, not a list.",
    }


def read():
    return {
        "statement": statement(),
        "early_regime_is_sharper": early_regime_is_sharper(),
        "resort_levers": resort_levers(),
        "composite_order_first10": composite_order_table()[:10],
    }
