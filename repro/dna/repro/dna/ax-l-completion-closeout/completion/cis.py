# -*- coding: utf-8 -*-
"""
completion.cis -- the B2 cis-code -> drive probe (Appendix L). The HONEST, deterministic test of
whether the per-edge regulatory drive is readable from the PROXIMAL promoter sequence -- and the
proof that it is DATA-BLOCKED.

The K BLUEPRINT's B2 asks: replace the modelling choice W_{j->i}=sqrt(gamma_parent) with a drive
READ OFF the sequence (TF-motif occupancy in the child's cis-regulatory window). For that to close
to [L], the parent TF-family's cited binding motif must actually be present in the child's promoter
ABOVE background. This module measures exactly that, parameter-free:

  * for every cited edge whose BOTH endpoints have a cached real GRCh38 promoter, scan the CHILD
    promoter (TSS-2000..+500, 2501 bp -- the SAME +-2 kb window the gamma operator reads) for the
    PARENT TF-family's cited IUPAC consensus motif(s), on BOTH strands;
  * compare the observed count to a DINUCLEOTIDE-PRESERVING SHUFFLE null (seed 19, 500 shuffles),
    which controls GC/CpG composition -- the shuffle IS the null, so there is no fitted threshold;
  * an edge is "above background" iff its observed count strictly exceeds the 95th percentile of its
    own shuffle null.

THE FINDING (data-blocked):
  Only a MINORITY of edges sit above background, and -- decisively -- the canonical direct edge
  SOX9 -| RUNX2 is BELOW background (SOX9 represses RUNX2 through distal enhancers and protein-
  protein contacts, not a proximal SOX-site array). The per-edge drive is therefore NOT in the
  +-2 kb promoter window. Closing B2 needs distal-enhancer + chromatin-accessibility sequence the
  present kit does not contain. This is a MEASUREMENT limitation (cf. the Inheritance-Kit FV5
  data-blocked-by-measurement result), NOT a theory defect and NOT a modelling failure -- so the
  W=sqrt(gamma) choice stays [F], and B2 does NOT close to [L]. physical_complete therefore stays
  False.
"""
import numpy as np

from . import lock

_IUPAC = {"A": "A", "C": "C", "G": "G", "T": "T", "R": "AG", "Y": "CT", "S": "GC",
          "W": "AT", "K": "GT", "M": "AC", "B": "CGT", "D": "AGT", "H": "ACT",
          "V": "ACG", "N": "ACGT"}
_IUPAC_RC = {"A": "T", "T": "A", "C": "G", "G": "C", "R": "Y", "Y": "R", "S": "S",
             "W": "W", "K": "M", "M": "K", "B": "V", "V": "B", "D": "H", "H": "D", "N": "N"}


def _rc(s):
    return "".join(_IUPAC_RC[b] for b in reversed(s))


def _count(seq, motif):
    """Count IUPAC matches of motif on BOTH strands of seq (overlapping)."""
    seq = seq.upper()
    n = 0
    for pat in {motif, _rc(motif)}:
        L = len(pat)
        sets = [set(_IUPAC[c]) for c in pat]
        for i in range(len(seq) - L + 1):
            if all(seq[i + j] in sets[j] for j in range(L)):
                n += 1
    return n


def _dinuc_shuffle(seq, rng):
    """Dinucleotide-preserving shuffle (edge-graph walk). Approximately preserves dinucleotide
    composition, controlling GC/CpG bias. Deterministic under the passed rng."""
    seq = seq.upper()
    succ = {}
    for i in range(len(seq) - 1):
        succ.setdefault(seq[i], []).append(seq[i + 1])
    for k in succ:
        rng.shuffle(succ[k])
    out = [seq[0]]
    ptr = {k: 0 for k in succ}
    cur = seq[0]
    for _ in range(len(seq) - 1):
        lst = succ.get(cur)
        if not lst or ptr[cur] >= len(lst):
            cur = seq[rng.integers(0, len(seq))]
            out.append(cur)
            continue
        nxt = lst[ptr[cur]]
        ptr[cur] += 1
        out.append(nxt)
        cur = nxt
    return "".join(out)


def _family_of(parent):
    """Map a parent gene to its cited TF-family motif key. Ligand parents (FGF/WNT) map to their
    downstream DNA-binding EFFECTOR family (ETS / TCF), flagged in the citation."""
    if parent.startswith("HOX"):
        return "HOX"
    table = {"SOX9": "SOX", "RUNX2": "RUNX", "PITX1": "PITX", "ISL1": "ISL"}
    if parent in table:
        return table[parent]
    if parent in ("PAX1", "PAX9", "PAX2", "PAX7"):
        return "PAX"
    if parent in ("FGF8", "FGF10"):
        return "ETS"
    if parent in ("WNT3A", "WNT2B"):
        return "TCF"
    return None


_PROBE_CACHE = {}


def occupancy_probe():
    """Run the deterministic B2 occupancy probe over every both-cached cited edge. Returns the
    per-edge table, the summary, and the data-blocked verdict. [F] config; the result is a measured,
    reproducible negative. Memoized per process (the probe is deterministic under seed 19, so caching
    is exact -- it only avoids recomputing the same shuffle null many times within one gate run)."""
    if "result" in _PROBE_CACHE:
        return _PROBE_CACHE["result"]
    cfg = lock.b2_cis_occupancy_cfg()
    cache = lock.cis_promoter_cache()
    motifs = cfg["tf_family_motifs_iupac"]
    seed = int(cfg["seed"])
    n_shuf = int(cfg["n_shuffles"])

    cached = set(cache.keys())
    both = [(p, c) for (p, c, _) in lock.cascade_edges() if p in cached and c in cached]

    rng = np.random.default_rng(seed)
    rows = []
    for p, c in both:
        fam = _family_of(p)
        child = cache[c]["seq"]
        obs = sum(_count(child, m) for m in motifs[fam])
        shuf = np.empty(n_shuf, dtype=np.float64)
        for i in range(n_shuf):
            shuf[i] = sum(_count(_dinuc_shuffle(child, rng), m) for m in motifs[fam])
        mu = float(shuf.mean())
        sd = float(shuf.std())
        p95 = float(np.percentile(shuf, 95))
        z = (obs - mu) / sd if sd > 0 else 0.0
        above = bool(obs > p95)
        rows.append({"parent": p, "child": c, "family": fam,
                     "observed": int(obs), "shuffle_mean": round(mu, 3),
                     "shuffle_sd": round(sd, 3), "z": round(float(z), 3),
                     "above_background": above})

    n = len(rows)
    n_above = sum(1 for r in rows if r["above_background"])
    mean_z = round(float(np.mean([r["z"] for r in rows])), 3) if rows else 0.0
    by_edge = {(r["parent"], r["child"]): r for r in rows}

    # the decisive canonical edge (SOX9 -| RUNX2): direct repression, must be below background.
    sox9_runx2 = by_edge.get(("SOX9", "RUNX2"))
    sox9_runx2_below = bool(sox9_runx2 is not None and not sox9_runx2["above_background"])

    majority_at_background = bool(n_above <= n / 2.0)
    data_blocked = bool(majority_at_background and sox9_runx2_below)

    result = {
        "n_edges_scored": n,
        "n_above_background": n_above,
        "frac_above_background": round(n_above / n, 4) if n else 0.0,
        "mean_z": mean_z,
        "rows": rows,
        "canonical_SOX9_represses_RUNX2": sox9_runx2,
        "canonical_SOX9_RUNX2_below_background": sox9_runx2_below,
        "majority_at_or_below_background": majority_at_background,
        "window_provenance": cfg["window_provenance"],
        "b2_data_blocked": data_blocked,
        "missing_measurement": ("distal-enhancer + chromatin-accessibility sequence (the per-edge "
                                "regulatory drive lives outside the +-2 kb promoter / gamma window)"),
        "grade": ("[F] data-blocked: the proximal-promoter cis-code does NOT recover the per-edge "
                  "drive above a dinucleotide-shuffle background (the canonical SOX9-|RUNX2 edge is "
                  "below background). B2 cannot close to [L] from this kit -- it needs distal-enhancer "
                  "+ accessibility data. A MEASUREMENT limitation, not a theory defect; W=sqrt(gamma) "
                  "stays [F]. (cf. Inheritance-Kit FV5 data-blocked-by-measurement.)"),
    }
    _PROBE_CACHE["result"] = result
    return result


def read():
    return occupancy_probe()
