# -*- coding: utf-8 -*-
"""
grammar.architecture -- G3, the ARCHITECTURE (organ) grammar. DISCOURSE: how the whole text
is laid out.

The 배치도 -- the arrangement map. Above the regulatory syntax sits the LAYOUT: how the
control elements are spaced and ordered along the genome, the architecture that becomes the
spatial arrangement of tissues. The canonical sequence-encoded arrangement map is Hox
colinearity (linear genomic order = spatial body order); here the same idea is read locally
as the spacing/arrangement of the G2 regulatory hotspots.

  s3 = the inter-element spacing sequence between successive cardiac-TF hotspots
  gamma_3 = mean(s3)            the ARCHITECTURE LEVEL  (mean layout spacing / regularity)
  A4_3    = robust_z(s3)        the ARCHITECTURE SHAPE  (the arrangement map -- where the
                                layout is dense vs sparse)

This is the third (gamma, A4) pair, read with the identical robust_z operator -- the same
grammar lifted one more level, from syntax to discourse.
"""
import numpy as np

from . import seqtools, regulatory


def hotspot_positions(seq):
    """Sorted forward-strand positions of all cardiac-TF hits (the elements to be laid out)."""
    hits = regulatory.motif_hits(seq)
    return sorted(p for _name, p in hits)


def spacing_signal(seq):
    """Inter-element spacings between successive cardiac-TF hotspots -- the layout signal.
    A sequence with regular cardiac architecture has structured spacings; a sequence with
    no cardiac program has few/erratic elements."""
    pos = hotspot_positions(seq)
    if len(pos) < 2:
        return np.array([], dtype=np.float64)
    return np.diff(np.array(pos, dtype=np.float64))


def read(seq):
    """G3 read: (gamma_3 = architecture LEVEL, A4_3 = architecture SHAPE) of a sequence."""
    s3 = spacing_signal(seq)
    if s3.size == 0:
        return {
            "grammar": "G3_architecture_organ",
            "linguistic_level": "discourse (how the whole text is laid out)",
            "signal": "inter-element spacing of cardiac-TF hotspots (the arrangement map)",
            "gamma_LEVEL": None,
            "A4_SHAPE_len": 0,
            "n_elements": len(hotspot_positions(seq)),
            "encodes": "the spatial LAYOUT of tissues (배치도) -- too few elements to lay out",
            "grade": "[O] sparse: needs more elements / real arrangement data",
        }
    level, shape = seqtools.level_and_shape(s3)
    return {
        "grammar": "G3_architecture_organ",
        "linguistic_level": "discourse (how the whole text is laid out)",
        "signal": "inter-element spacing of cardiac-TF hotspots (the arrangement map)",
        "gamma_LEVEL": round(level, 6),
        "A4_SHAPE_len": int(shape.size),
        "A4_SHAPE_std": round(float(np.std(shape)), 6),
        "n_elements": len(hotspot_positions(seq)),
        "mean_spacing_bp": round(float(np.mean(s3)), 3),
        "encodes": "the spatial LAYOUT of tissues (배치도) -- the arrangement map",
        "grade": "[L] real element layout + [V] exact robust_z split; real 3D-arrangement [O]",
    }


def signal_for_compare(seq):
    """The raw G3 signal (spacings), resampled onto a common length for orthogonality is not
    meaningful (different support); G3 is compared structurally, not pointwise."""
    return spacing_signal(seq)
