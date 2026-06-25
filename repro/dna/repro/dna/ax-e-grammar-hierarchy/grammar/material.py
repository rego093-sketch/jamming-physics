# -*- coding: utf-8 -*-
"""
grammar.material -- G1, the MATERIAL (cell) grammar. PHONOLOGY: the physical substance of
the letters.

This is the level the corpus already reads. The signal is the nearest-neighbour stacking
free energy along the sequence -- the chemistry/electrostatics of adjacent base pairs, the
'ions/chemistry' material. Its LEVEL is the cell-level gamma (how stiff the material is on
average); its SHAPE is the cell-level A4 coordinate (the material pattern, mean removed).

  s1[i] = dG(S[i:i+2])           the per-step stacking signal (SantaLucia 1998)
  gamma_1 = mean(s1)             the MATERIAL LEVEL  (the corpus's gamma)
  A4_1    = robust_z(s1)         the MATERIAL SHAPE  (the corpus's A4 coordinate)
"""
import numpy as np

from . import lock, seqtools


def stacking_signal(seq):
    """Per-step nearest-neighbour stacking dG along the sequence. [L] (SantaLucia 1998)."""
    seq = seq.upper()
    tab = lock.nn_dG()
    s = []
    for i in range(len(seq) - 1):
        d = seq[i:i + 2]
        s.append(tab.get(d, np.nan))
    s = np.array(s, dtype=np.float64)
    # any non-ACGT dimer -> drop (real promoters are clean; guard anyway)
    return s[~np.isnan(s)]


def read(seq):
    """G1 read: (gamma_1 = material LEVEL, A4_1 = material SHAPE) of a sequence."""
    s1 = stacking_signal(seq)
    level, shape = seqtools.level_and_shape(s1)
    return {
        "grammar": "G1_material_cell",
        "linguistic_level": "phonology (the physical substance of the letters)",
        "signal": "nearest-neighbour stacking dG (SantaLucia 1998)",
        "gamma_LEVEL": round(level, 6),
        "A4_SHAPE_len": int(shape.size),
        "A4_SHAPE_std": round(float(np.std(shape)), 6),
        "encodes": "the CELL's intrinsic material stiffness -- what the corpus has read",
        "grade": "[L] measured material (cited NN parameters) + [V] exact robust_z split",
    }


def signal_for_compare(seq):
    """The raw G1 signal (for cross-grammar orthogonality)."""
    return stacking_signal(seq)
