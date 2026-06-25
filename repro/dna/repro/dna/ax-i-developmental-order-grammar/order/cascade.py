# -*- coding: utf-8 -*-
"""
order.cascade -- THE HIGHER-ORDER GRAMMAR.

The missing predictor of developmental staging is NOT a hidden single-locus reading -- it is the
G3 ARCHITECTURE grammar (the cis-regulatory WIRING already identified by Appendices E/F) read on
the TIME axis. A gene can only fire AFTER the upstream regulators that deliver its drive have
fired. So the emergence ORDER is the topological order of the regulatory DAG:

    cascade DEPTH(gene) = longest directed path from any SOURCE down to that gene

DEPTH is DERIVED from the cited edges (it is not asserted). This module:
  * builds the directed graph from lock.cascade_edges()
  * proves it is a DAG (no cycle)  -> a topological order EXISTS                       [V]
  * computes each gene's cascade depth (the higher-order ORDER key)                    [V]
  * exposes the COMPOSITE order key (depth primary, barrier gamma^2/4 as tie-break)    [V]
"""
from . import lock, seqtools


def _nodes_and_adj():
    """Nodes = every driver gene; edges restricted to genes present in the atlas."""
    genes = set(lock.driver_gamma().keys())
    adj = {g: [] for g in genes}          # parent -> [children]
    indeg = {g: 0 for g in genes}
    rev = {g: [] for g in genes}          # child -> [parents]
    for parent, child, _cite in lock.cascade_edges():
        if parent in genes and child in genes:
            adj[parent].append(child)
            rev[child].append(parent)
            indeg[child] += 1
    return genes, adj, rev, indeg


def is_dag():
    """Kahn's algorithm: a topological order exists iff the graph is acyclic. Returns
    (is_acyclic, topo_order). [V]."""
    genes, adj, rev, indeg = _nodes_and_adj()
    indeg = dict(indeg)
    # deterministic queue: sort by name
    queue = sorted([g for g in genes if indeg[g] == 0])
    order = []
    while queue:
        n = queue.pop(0)
        order.append(n)
        for c in sorted(adj[n]):
            indeg[c] -= 1
            if indeg[c] == 0:
                queue.append(c)
        queue.sort()
    acyclic = (len(order) == len(genes))
    return acyclic, order


def sources():
    """Cascade SOURCES: genes with no upstream regulator in the atlas (developmental founders
    driven by the global ramp)."""
    genes, adj, rev, indeg = _nodes_and_adj()
    return sorted([g for g in genes if indeg[g] == 0])


def depth():
    """cascade DEPTH(gene) = longest directed path from any source. DERIVED from the edges via
    a topological relaxation (well-defined because the graph is a DAG). [V].

    depth(source) = 0 ; depth(child) = 1 + max(depth(parents)).
    """
    acyclic, topo = is_dag()
    if not acyclic:
        raise ValueError("cascade is not a DAG -- depth undefined (cycle present)")
    genes, adj, rev, indeg = _nodes_and_adj()
    d = {g: 0 for g in genes}
    for n in topo:                       # topo order guarantees parents seen before children
        for p in rev[n]:
            if d[p] + 1 > d[n]:
                d[n] = d[p] + 1
    return d


def order_table():
    """The full per-gene order table: gamma, spinodal (the single-locus key that FAILS),
    barrier gamma^2/4, cascade depth (the higher-order key), and the COMPOSITE key
    (depth primary, barrier as the within-tier tie-break)."""
    dg = lock.driver_gamma()
    d = depth()
    src = set(sources())
    rows = []
    for sym, rec in dg.items():
        g = rec["gamma"]
        rows.append({
            "gene": sym,
            "program": rec["program"],
            "system": rec["system"],
            "gamma": g,
            "spinodal": round(float(seqtools.spinodal(g)), 8),   # the single-locus order key
            "barrier": round(g * g / 4.0, 8),                    # cusp barrier (tie-break)
            "cascade_depth": d[sym],                             # the HIGHER-ORDER order key
            "is_source": sym in src,
        })
    # the COMPOSITE order: depth primary (ascending), barrier secondary (ascending), name last
    rows.sort(key=lambda r: (r["cascade_depth"], r["barrier"], r["gene"]))
    for i, r in enumerate(rows):
        r["composite_rank"] = i + 1
    return rows


def max_depth():
    return max(depth().values())


def longest_path():
    """Return ONE longest directed path (the linear axial dependency chain that realizes max
    depth), as a list of gene symbols from a source to the deepest terminus. Deterministic:
    ties in predecessor choice are broken by gene name. [V] (derived from the edges)."""
    acyclic, topo = is_dag()
    if not acyclic:
        raise ValueError("cascade is not a DAG -- longest path undefined (cycle present)")
    genes, adj, rev, indeg = _nodes_and_adj()
    d = {g: 0 for g in genes}
    pred = {g: None for g in genes}
    for n in topo:
        # choose the predecessor giving the longest path; tie-break by name for determinism
        best_p, best_d = None, -1
        for p in sorted(rev[n]):
            if d[p] + 1 > best_d:
                best_d = d[p] + 1
                best_p = p
        if best_p is not None:
            d[n] = best_d
            pred[n] = best_p
    # terminus = deepest node (tie-break by name)
    terminus = sorted(genes, key=lambda g: (-d[g], g))[0]
    path = []
    cur = terminus
    while cur is not None:
        path.append(cur)
        cur = pred[cur]
    path.reverse()
    return path


def read():
    acyclic, topo = is_dag()
    d = depth()
    return {
        "definition": "cascade DEPTH(gene) = longest directed path from a SOURCE; emergence ORDER "
                      "= toposort of the regulatory DAG (the G3 wiring read on the time axis).",
        "n_genes": len(d),
        "n_edges": len(lock.cascade_edges()),
        "is_dag": bool(acyclic),
        "topo_order_exists": bool(acyclic),
        "n_sources": len(sources()),
        "sources": sources(),
        "max_depth": max_depth(),
        "depth_by_gene": dict(sorted(d.items(), key=lambda kv: (kv[1], kv[0]))),
        "grade": "[V] the cascade is a DAG; a deterministic toposort/depth exists and is DERIVED "
                 "from the cited edges -- the higher-order (composite) order key (depth, barrier).",
    }
