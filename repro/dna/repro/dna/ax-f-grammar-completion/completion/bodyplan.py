# -*- coding: utf-8 -*-
"""
completion.bodyplan -- G5, the BODY-PLAN grammar. GENRE: the whole-body organizing form
(더 크고 더 넓게).

The highest organizing level: the grammar that lays out the whole BODY, not a single organ.
Its canonical sequence-encoded form is Hox colinearity -- the linear order of the Hox genes
along the chromosome equals their order along the anterior-posterior body axis. This is the
deepest known instance of the blueprint's spatial code: position on the DNA = position in
the body. Read on the real HOXD cluster (nine genes, GRCh38 coordinates from NCBI):

  s5 = the genomic TSS coordinates in body-axis (AP) order   the body-plan signal
  gamma_5 = mean(s5)                  the BODY-PLAN LEVEL (the cluster's genomic centroid)
  A4_5    = robust_z(s5)             the BODY-PLAN SHAPE (the body-axis arrangement)

Colinearity is the ORDER fact: the genomic order of the nine genes is monotonic with the AP
body rank. Reported as the rank-rank correlation (the proper colinearity statement, about
order not metric distance) and the Pearson correlation on raw coordinates. The same robust_z
operator gives A4_5. The real 3D body map (Hi-C across the embryo; the colinear spatial TF
domains staged through development) is the named [O] obstacle.
"""
import numpy as np

from . import lock, seqtools


def _rankdata(x):
    """Ascending ranks (1..n), ties broken by position (the cluster has no ties)."""
    order = np.argsort(np.argsort(np.asarray(x, dtype=np.float64)))
    return (order + 1).astype(np.float64)


def colinearity():
    """Hox colinearity: the genomic order of the HOXD cluster equals the AP body order.
    Rank-rank correlation (order colinearity) and Pearson on raw TSS coordinates."""
    tss, rank = lock.hox_tss_and_rank()
    tss = np.asarray(tss, dtype=np.float64)
    rank = np.asarray(rank, dtype=np.float64)

    # Pearson on raw coordinates
    pear = float(np.corrcoef(tss, rank)[0, 1])
    # rank-rank (Spearman-equivalent): genomic ascending rank vs AP body rank
    gen_rank = _rankdata(tss)
    spear = float(np.corrcoef(gen_rank, rank)[0, 1])

    thr = lock.g5_colinearity_corr_min()
    return {
        "genes": lock.hox_order(),
        "n_genes": len(tss),
        "pearson_tss_vs_bodyrank": round(pear, 4),
        "rankrank_genomic_vs_bodyrank": round(spear, 4),
        "abs_pearson": round(abs(pear), 4),
        "abs_rankrank": round(abs(spear), 4),
        "threshold": thr,
        "colinear": bool(abs(spear) >= thr and abs(pear) >= thr),
        "verdict": ("the genomic order of the nine HOXD genes is monotonic with the "
                    "anterior-posterior body axis -- linear order on the DNA equals order along "
                    "the body. The sign is a convention (3'->5' vs anterior->posterior); the "
                    "colinearity is the magnitude. This is the body-plan grammar G5."),
        "grade": "[L] real GRCh38 coordinates + cited AP colinearity (Lewis 1978; Duboule & "
                 "Dolle 1989) + [V] exact correlation; real 3D body map [O]",
    }


def read():
    """G5 read: (gamma_5 = body-plan LEVEL, A4_5 = body-plan SHAPE) via the same operator,
    on the genomic coordinates in body-axis order."""
    tss, _ = lock.hox_tss_and_rank()
    level, shape = seqtools.level_and_shape(tss)
    return {
        "grammar": "G5_bodyplan_genre",
        "linguistic_level": "genre (the whole-body organizing form)",
        "signal": "HOXD genomic TSS coordinates in anterior-posterior body order",
        "gamma_LEVEL": round(level, 3),
        "A4_SHAPE_len": int(shape.size),
        "A4_SHAPE_std": round(float(np.std(shape)), 6),
        "A4_SHAPE_first5": [round(float(v), 4) for v in shape[:5]],
        "encodes": "the anterior-posterior BODY axis -- position on the DNA = position in the body",
        "grade": "[L] real coordinates + cited colinearity + [V] exact robust_z split; "
                 "real 3D body map [O]",
    }
