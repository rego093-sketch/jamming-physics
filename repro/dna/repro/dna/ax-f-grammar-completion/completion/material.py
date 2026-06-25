# -*- coding: utf-8 -*-
"""
completion.material -- G1, the MATERIAL (cell) grammar, re-locked from Appendix E.

Here it is the reference level against which the new G4 dynamical grammar is shown to be
orthogonal. The signal is the nearest-neighbour stacking free energy along the sequence --
the chemistry of adjacent base pairs. Its LEVEL is the material gamma; its SHAPE is the
material A4. Identical to Appendix E's G1.

  s1[i] = dG(S[i:i+2])           per-step stacking signal (SantaLucia 1998)
  gamma_1 = mean(s1)             the MATERIAL LEVEL
  A4_1    = robust_z(s1)         the MATERIAL SHAPE
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
    return s[~np.isnan(s)]


def read(seq):
    """G1 read: (gamma_1 = material LEVEL, A4_1 = material SHAPE)."""
    s1 = stacking_signal(seq)
    level, shape = seqtools.level_and_shape(s1)
    return {
        "grammar": "G1_material_cell",
        "signal": "nearest-neighbour stacking dG (SantaLucia 1998)",
        "gamma_LEVEL": round(level, 6),
        "A4_SHAPE_len": int(shape.size),
        "A4_SHAPE_std": round(float(np.std(shape)), 6),
        "grade": "[L] cited NN parameters + [V] exact robust_z split",
    }


def signal_for_compare(seq):
    """The raw G1 signal (for G4 orthogonality)."""
    return stacking_signal(seq)
