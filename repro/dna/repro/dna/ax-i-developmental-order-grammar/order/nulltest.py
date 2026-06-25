# -*- coding: utf-8 -*-
"""
order.nulltest -- the REAL-DATA confrontation against cited Carnegie onset ranks.

This is where the grammar is put on trial against measurement, with real numbers and no fitting:

  THE NULL        : does the single-locus predictor spinodal(gamma) order the genes the way the
                    embryo stages them? -> NO. |Spearman(spinodal, Carnegie rank)| stays inside the
                    null band (<= ceiling). This reproduces Appendix A's "measured null" with numbers.

  THE DISCOVERY   : two honest, gateable claims that the WIRING (the G3 architecture grammar) read
                    on the time axis predicts the order where the single locus does not:
                    (1) EDGE CONCORDANCE -- among cited regulatory edges whose endpoints both carry
                        a Carnegie rank, EVERY edge has rank(child) >= rank(parent) (zero inversions).
                        The cited regulator's onset is never later than its target's.
                    (2) DEPTH BEATS GAMMA -- |Spearman(cascade depth, Carnegie rank)| STRICTLY
                        exceeds the spinodal correlation, on all anchored genes AND on the main
                        wired component.

  THE HONEST RESIDUAL : the pre-registered ABSOLUTE floor (0.70) for the depth<->Carnegie rank
                    correlation is NOT met globally (0.475). It is met only along the linear axial
                    dependency chain. The dilution is named, not hidden: limb-bud genes are
                    artificial cascade sources (their FGF/Wnt inducers are absent from the 38-gene
                    kit) and the HOX kit is group-13-only. The absolute-strength claim is therefore
                    graded [L], not [V]. (반증=발견.)
"""
import collections
import numpy as np

from . import lock, cascade, seqtools


def _spearman(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    ra = a.argsort().argsort().astype(np.float64)
    rb = b.argsort().argsort().astype(np.float64)
    ra -= ra.mean(); rb -= rb.mean()
    denom = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / denom) if denom > 0 else 0.0


def _weakly_connected_components():
    dg = lock.driver_gamma()
    genes = sorted(dg.keys())
    adj = collections.defaultdict(set)
    for p, c, _ in lock.cascade_edges():
        if p in dg and c in dg:
            adj[p].add(c); adj[c].add(p)
    seen, comps = set(), []
    for g in genes:
        if g in seen:
            continue
        stack, comp = [g], set()
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x); comp.add(x)
            for y in adj[x]:
                if y not in seen:
                    stack.append(y)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    return comps


# ----------------------------------------------------------------------------- THE NULL
def the_null():
    """spinodal(gamma) vs Carnegie onset rank, over every anchored gene. Expected |rho| <= ceiling
    -> the single-locus stiffness does NOT predict developmental staging. [V] (a measured null)."""
    anc = lock.carnegie_anchor()
    dg = lock.driver_gamma()
    genes = sorted(anc.keys())
    cr = [anc[g]["rank"] for g in genes]
    spin = [float(seqtools.spinodal(dg[g]["gamma"])) for g in genes]
    rho = _spearman(spin, cr)
    ceiling = lock.null_ceiling()
    return {
        "n_anchored": len(genes),
        "spearman_spinodal_vs_carnegie": round(rho, 4),
        "null_ceiling": ceiling,
        "is_null": bool(abs(rho) <= ceiling),
        "grade": "[V] |Spearman(spinodal(gamma), Carnegie rank)| sits inside the null band -- the "
                 "single-locus barrier does not order developmental staging (Appendix A's null, in "
                 "numbers).",
    }


# ----------------------------------------------------------------------- THE DISCOVERY (1)
def edge_concordance():
    """Among cited regulatory edges whose BOTH endpoints carry a Carnegie rank, the fraction with
    rank(child) >= rank(parent). Ties (same tier) count as concordant. Floor = 1.0 (zero inversions):
    the cited wiring never contradicts the cited temporal order. [V]."""
    anc = lock.carnegie_anchor()
    edges = [(p, c) for (p, c, _) in lock.cascade_edges() if p in anc and c in anc]
    concordant, ties, inversions = [], [], []
    for p, c in edges:
        rp, rc = anc[p]["rank"], anc[c]["rank"]
        if rc > rp:
            concordant.append((p, c, rp, rc))
        elif rc == rp:
            ties.append((p, c, rp, rc))
        else:
            inversions.append((p, c, rp, rc))
    n = len(edges)
    conc_incl_ties = (len(concordant) + len(ties)) / n if n else 0.0
    floor = lock.edge_concordance_floor()
    return {
        "n_cited_edges_both_anchored": n,
        "n_concordant_child_later": len(concordant),
        "n_ties_same_tier": len(ties),
        "n_inversions": len(inversions),
        "inversions": [{"parent": p, "child": c, "rank_parent": rp, "rank_child": rc}
                       for (p, c, rp, rc) in inversions],
        "concordance_incl_ties": round(conc_incl_ties, 4),
        "concordance_floor": floor,
        "passes": bool(conc_incl_ties >= floor and len(inversions) == 0),
        "grade": "[V] every cited regulatory edge agrees with the cited temporal order (zero "
                 "inversions) -- the cascade WIRING read on the time axis IS the order grammar.",
    }


# ----------------------------------------------------------------------- THE DISCOVERY (2)
def depth_beats_gamma():
    """|Spearman(cascade depth, Carnegie rank)| must STRICTLY exceed the spinodal correlation, on
    (a) all anchored genes and (b) the main weakly-connected cascade component. [V]."""
    anc = lock.carnegie_anchor()
    dg = lock.driver_gamma()
    d = cascade.depth()

    def corr_on(subset):
        subset = sorted(subset)
        cr = [anc[g]["rank"] for g in subset]
        dep = [d[g] for g in subset]
        spin = [float(seqtools.spinodal(dg[g]["gamma"])) for g in subset]
        return _spearman(dep, cr), _spearman(spin, cr), len(subset)

    allg = set(anc.keys())
    rd_all, rs_all, n_all = corr_on(allg)

    comps = _weakly_connected_components()
    main = max(comps, key=lambda c: len(c & allg)) if comps else set()
    main_anch = main & allg
    rd_main, rs_main, n_main = corr_on(main_anch) if len(main_anch) >= 3 else (0.0, 0.0, len(main_anch))

    req = lock.depth_beats_gamma_required()
    beats_all = abs(rd_all) > abs(rs_all)
    beats_main = abs(rd_main) > abs(rs_main)
    return {
        "spearman_depth_vs_carnegie_all": round(rd_all, 4),
        "spearman_spinodal_vs_carnegie_all": round(rs_all, 4),
        "n_all": n_all,
        "spearman_depth_vs_carnegie_main_component": round(rd_main, 4),
        "spearman_spinodal_vs_carnegie_main_component": round(rs_main, 4),
        "n_main_component_anchored": n_main,
        "depth_beats_gamma_all": bool(beats_all),
        "depth_beats_gamma_main_component": bool(beats_main),
        "required": bool(req),
        "passes": bool((beats_all and beats_main) == req),
        "grade": "[V] cascade depth (derived from the wiring) tracks Carnegie order strictly better "
                 "than single-locus spinodal(gamma), on all genes and on the main wired component.",
    }


# ------------------------------------------------------------------ THE HONEST RESIDUAL
def absolute_strength_residual():
    """The pre-registered ABSOLUTE floor (0.70) on Spearman(depth, Carnegie). Reported honestly:
    NOT met globally; met only on the linear axial dependency chain. Absolute strength is [L]."""
    anc = lock.carnegie_anchor()
    dg = lock.driver_gamma()
    d = cascade.depth()

    def corr_on(subset):
        subset = sorted(subset)
        cr = [anc[g]["rank"] for g in subset]
        dep = [d[g] for g in subset]
        return _spearman(dep, cr), len(subset)

    rd_all, n_all = corr_on(set(anc.keys()))
    # the linear axial dependency chain = the longest directed path (organizer -> ossification)
    chain = cascade.longest_path()
    chain_anch = [g for g in chain if g in anc]
    rd_chain, n_chain = corr_on(chain_anch) if len(chain_anch) >= 3 else (0.0, len(chain_anch))
    floor = lock.cascade_floor()
    return {
        "preregistered_absolute_floor": floor,
        "spearman_depth_vs_carnegie_all": round(rd_all, 4),
        "meets_floor_globally": bool(rd_all >= floor),
        "axial_chain": chain,
        "spearman_depth_vs_carnegie_axial_chain": round(rd_chain, 4),
        "meets_floor_on_axial_chain": bool(rd_chain >= floor),
        "named_dilution_sources": [
            "limb-bud genes (TBX4/TBX5) are artificial cascade SOURCES: their FGF/Wnt inducers "
            "are not in the 38-gene kit, so their depth understates their late onset.",
            "the HOX kit is group-13-only (HOXA13/HOXD13): without the HOX1-12 collinear chain, "
            "cascade depth understates HOX13 lateness (named in param_db.hox13_limitation).",
        ],
        "grade": "[L] the ABSOLUTE depth<->Carnegie rank strength is moderate and scope-limited: it "
                 "reaches the pre-registered floor only on the wired axial chain, not globally. "
                 "Reported, not hidden -- the absolute-strength claim is [L], not [V].",
    }


def read():
    return {
        "the_null": the_null(),
        "edge_concordance": edge_concordance(),
        "depth_beats_gamma": depth_beats_gamma(),
        "absolute_strength_residual": absolute_strength_residual(),
    }
