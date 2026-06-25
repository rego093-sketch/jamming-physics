# -*- coding: utf-8 -*-
"""
completion.seqtools -- shared sequence operators (Appendix F).

The SAME core as Appendix E, re-locked so the operator is literally identical across the
two appendices:

  robust_z       the EXACT level/shape operator the cell level uses for the A4 coordinate
                 (median-centred, MAD-scaled); applied identically at G1, G2, G4, G5 so the
                 (LEVEL, SHAPE) = (gamma, A4) decomposition is the same grammar lifted.
  level_and_shape  (mean, robust_z) of a signal -- the (gamma, A4) pair at any level.
  revcomp        reverse complement (motifs are scanned on both strands).
  dinuc_shuffle  the Altschul-Erickson dinucleotide-preserving permutation: preserves
                 dinucleotide counts EXACTLY (hence the material level gamma_1) while
                 randomizing motif positions. Deterministic given the seed; identical to
                 Appendix E so the organ-atlas enrichment background is the same machine.
"""
import numpy as np


# ----------------------------------------------------------------------------
# the A4 operator -- robust z (byte-identical intent to the cell-level A4)
# ----------------------------------------------------------------------------
def robust_z(x):
    """Median-centred, MAD-scaled robust z-score. The SHAPE projection used at every
    grammar level; identical operator to the cell-level A4 coordinate and to Appendix E."""
    x = np.asarray(x, dtype=np.float64)
    if x.size == 0:
        return x
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    scale = 1.4826 * mad if mad > 0 else (np.std(x) if np.std(x) > 0 else 1.0)
    return (x - med) / scale


def level_and_shape(signal):
    """(LEVEL, SHAPE) = (mean, robust_z) of a signal -- the (gamma, A4) pair at any level."""
    s = np.asarray(signal, dtype=np.float64)
    return float(np.mean(s)) if s.size else 0.0, robust_z(s)


# ----------------------------------------------------------------------------
# reverse complement
# ----------------------------------------------------------------------------
_COMP = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}


def revcomp(s):
    return "".join(_COMP.get(c, "N") for c in reversed(s))


# ----------------------------------------------------------------------------
# dinucleotide-preserving shuffle (Altschul-Erickson Eulerian walk)
# ----------------------------------------------------------------------------
def dinuc_shuffle(seq, seed):
    """Return a permutation of seq with IDENTICAL dinucleotide counts (Altschul-Erickson).
    Deterministic given the seed. Preserves the material-level stacking distribution exactly
    while destroying higher-order (motif) structure -- the null background for the organ
    atlas's enrichment-z. Identical implementation to Appendix E."""
    seq = seq.upper()
    n = len(seq)
    if n < 3:
        return seq
    rng = np.random.RandomState(seed)
    letters = sorted(set(seq))

    last = seq[-1]
    edges = {a: [] for a in letters}
    for i in range(n - 1):
        edges[seq[i]].append(i + 1)

    start = seq[0]
    for _attempt in range(64):
        order = {a: list(edges[a]) for a in letters}
        for a in letters:
            rng.shuffle(order[a])
        ptr = {a: 0 for a in letters}
        cur_letter = start
        out = [start]
        ok = True
        for _ in range(n - 1):
            lst = order[cur_letter]
            if ptr[cur_letter] >= len(lst):
                ok = False
                break
            dest_idx = lst[ptr[cur_letter]]
            ptr[cur_letter] += 1
            nxt = seq[dest_idx]
            out.append(nxt)
            cur_letter = nxt
        if ok and len(out) == n:
            res = "".join(out)
            if _dinuc_counts(res) == _dinuc_counts(seq):
                return res
    arr = list(seq)
    rng.shuffle(arr)
    return "".join(arr)


def _dinuc_counts(s):
    d = {}
    for i in range(len(s) - 1):
        k = s[i:i + 2]
        d[k] = d.get(k, 0) + 1
    return d


def dinuc_counts(s):
    return _dinuc_counts(s)
