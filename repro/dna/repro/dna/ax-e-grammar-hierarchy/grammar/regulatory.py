# -*- coding: utf-8 -*-
"""
grammar.regulatory -- G2, the REGULATORY (tissue) grammar. SYNTAX: how control words are
arranged.

THE MISSED UPPER A4. The cell-level material grammar reads the chemistry of adjacent bases;
it does not read which TISSUE a region specifies. That is written one level up, in the
arrangement of transcription-factor binding sites -- the cis-regulatory grammar. For the
heart, that grammar is the cardiac TF code: GATA4, NKX2-5 (NKE), MEF2C, TBX5, and bHLH/HAND
E-boxes, whose combinatorial syntax specifies cardiac enhancers.

  s2[i] = (cardiac-TF consensus matches, either strand, in a window around i)
  gamma_2 = mean(s2)            the REGULATORY LEVEL  (overall cardiac drive)
  A4_2    = robust_z(s2)        the REGULATORY SHAPE  (the tissue-identity ARRANGEMENT)

A4_2 is the tissue-level A4 the corpus had not formalized: the arrangement map of cardiac
control along the sequence. Where it peaks, cardiac regulation concentrates.
"""
import re
import numpy as np

from . import lock, seqtools


def _compiled_motifs():
    return {name: re.compile(pat) for name, pat in lock.cardiac_motifs().items()}


def motif_hits(seq):
    """All cardiac-TF consensus match midpoints on BOTH strands -> list of (name, position).
    Positions are mapped back to the forward-strand coordinate."""
    seq = seq.upper()
    L = len(seq)
    rc = seqtools.revcomp(seq)
    hits = []
    for name, rx in _compiled_motifs().items():
        for m in rx.finditer(seq):
            hits.append((name, (m.start() + m.end()) // 2))
        for m in rx.finditer(rc):
            # map rc coordinate back to forward strand
            mid_rc = (m.start() + m.end()) // 2
            hits.append((name, L - 1 - mid_rc))
    return hits


def regulatory_signal(seq):
    """Sliding-window cardiac-TF density along the sequence (both strands). The G2 signal."""
    seq = seq.upper()
    L = len(seq)
    w = lock.regulatory_window_bp()
    dens = np.zeros(L, dtype=np.float64)
    for _name, pos in motif_hits(seq):
        lo = max(0, pos - w)
        hi = min(L, pos + w + 1)
        dens[lo:hi] += 1.0
    return dens


def motif_counts(seq):
    """Total cardiac-TF consensus matches by motif (both strands)."""
    counts = {}
    for name, _pos in motif_hits(seq):
        counts[name] = counts.get(name, 0) + 1
    # ensure all motif names present
    for name in lock.cardiac_motifs():
        counts.setdefault(name, 0)
    return counts


def read(seq):
    """G2 read: (gamma_2 = regulatory LEVEL, A4_2 = regulatory SHAPE) of a sequence."""
    s2 = regulatory_signal(seq)
    level, shape = seqtools.level_and_shape(s2)
    counts = motif_counts(seq)
    total = int(sum(counts.values()))
    return {
        "grammar": "G2_regulatory_tissue",
        "linguistic_level": "syntax (how control words are arranged)",
        "signal": "cardiac TF binding grammar density (GATA, NKE, MEF2, TBX5, E-box; both strands)",
        "gamma_LEVEL": round(level, 6),
        "A4_SHAPE_len": int(shape.size),
        "A4_SHAPE_std": round(float(np.std(shape)), 6),
        "cardiac_motif_counts": counts,
        "cardiac_motif_total": total,
        "encodes": "the TISSUE identity / arrangement -- the upper A4 the corpus missed",
        "grade": "[L] real sequence + cited cardiac TF grammar + [V] exact robust_z split",
    }


def signal_for_compare(seq):
    """The raw G2 signal (for cross-grammar orthogonality)."""
    return regulatory_signal(seq)
