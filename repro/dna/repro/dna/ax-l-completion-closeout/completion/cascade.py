# -*- coding: utf-8 -*-
"""
completion.cascade -- THE HIGHER-ORDER GRAMMAR, on the FILLED gene set.

Identical machinery to Appendix I (the cascade DEPTH = longest directed path from a SOURCE; the
emergence ORDER = toposort of the regulatory DAG), now run on the COMPLETED atlas: the 38 inherited
drivers PLUS the 25 new genes (limb FGF/Wnt inducers + full HOXA/HOXD clusters). The two named
Appendix-I dilutors are removed by data:
  * TBX5/TBX4 are no longer artificial cascade SOURCES -- the cited limb-field RA/Wnt inducers now
    sit upstream of them, so they acquire real upstream depth.
  * HOXA13/HOXD13 are no longer isolated group-13 nodes -- the cited 3'->5' collinear chains now
    sit upstream of them, so they acquire their true late depth.

DEPTH is DERIVED from the cited edges (it is not asserted):
  * builds the directed graph from lock.cascade_edges()
  * proves it is a DAG (no cycle) -> a topological order EXISTS                        [V]
  * computes each gene's cascade depth (the higher-order ORDER key)                    [V]
  * exposes the COMPOSITE order key (depth primary, barrier gamma^2/4 as tie-break)    [V]
"""
from . import lock, seqtools


def _nodes_and_adj():
    """Nodes = every driver gene (merged atlas); edges restricted to genes present in the atlas."""
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
    queue = sorted([g for g in genes if indeg[g] == 0])   # deterministic queue: sort by name
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
    """cascade DEPTH(gene) = longest directed path from any source. DERIVED via a topological
    relaxation (well-defined because the graph is a DAG). [V].
    depth(source) = 0 ; depth(child) = 1 + max(depth(parents))."""
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


def indegree():
    """In-degree of every gene in the merged atlas (number of cited regulators). Used by the
    quorum/AND gate to set k_i."""
    genes, adj, rev, indeg = _nodes_and_adj()
    return dict(indeg)


def order_table():
    """The full per-gene order table: gamma, spinodal (the single-locus key that FAILS), barrier
    gamma^2/4, cascade depth (the higher-order key), and the COMPOSITE key (depth primary, barrier
    as the within-tier tie-break)."""
    dg = lock.driver_gamma()
    d = depth()
    src = set(sources())
    rows = []
    for sym, rec in dg.items():
        g = rec["gamma"]
        rows.append({
            "gene": sym,
            "program": rec.get("program", ""),
            "system": rec.get("system", ""),
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
    depth), from a source to the deepest terminus. Deterministic: predecessor ties broken by gene
    name. [V] (derived from the edges)."""
    acyclic, topo = is_dag()
    if not acyclic:
        raise ValueError("cascade is not a DAG -- longest path undefined (cycle present)")
    genes, adj, rev, indeg = _nodes_and_adj()
    d = {g: 0 for g in genes}
    pred = {g: None for g in genes}
    for n in topo:
        best_p, best_d = None, -1
        for p in sorted(rev[n]):
            if d[p] + 1 > best_d:
                best_d = d[p] + 1
                best_p = p
        if best_p is not None:
            d[n] = best_d
            pred[n] = best_p
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
                      "= toposort of the regulatory DAG (the G3 wiring read on the time axis), on "
                      "the FILLED 63-gene atlas.",
        "n_genes": len(d),
        "n_edges": len(lock.cascade_edges()),
        "is_dag": bool(acyclic),
        "topo_order_exists": bool(acyclic),
        "n_sources": len(sources()),
        "sources": sources(),
        "max_depth": max_depth(),
        "depth_by_gene": dict(sorted(d.items(), key=lambda kv: (kv[1], kv[0]))),
        "grade": "[V] the filled cascade is a DAG; a deterministic toposort/depth exists and is "
                 "DERIVED from the cited edges -- the higher-order (composite) order key.",
    }
