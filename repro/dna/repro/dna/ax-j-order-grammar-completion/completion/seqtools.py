# -*- coding: utf-8 -*-
"""
build.seqtools -- shared operators (Appendix H), re-locked so they are LITERALLY identical to
Appendices E/F/G:

  robust_z        the EXACT level/shape (A4) operator: median-centred, MAD-scaled. The SHAPE
                  projection used at every grammar level; identical to the cell-level A4.
  gamma           gamma = -mean(nearest-neighbour stacking dG, SantaLucia 1998) -- the material
                  LEVEL. The driver-gene gammas in param_db were computed with THIS function
                  (the 8 overlapping with Appendix G match byte-for-byte).
  level_and_shape (mean, robust_z) of a signal -- the (gamma, A4) pair at any level.
  spinodal        the gamma -> emergence-onset map, re-used verbatim from Appendix A.

stdlib + numpy only. Deterministic.
"""
import numpy as np


def robust_z(x):
    """Median-centred, MAD-scaled robust z-score. SHAPE projection; identical to the cell A4
    and to Appendices E/F/G."""
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


def stacking_signal(seq, nn):
    """Per-step nearest-neighbour stacking dG along the sequence (SantaLucia 1998)."""
    seq = seq.upper()
    s = [nn.get(seq[i:i + 2], np.nan) for i in range(len(seq) - 1)]
    s = np.asarray(s, dtype=np.float64)
    return s[~np.isnan(s)]


def gamma(seq, nn):
    """gamma = -mean(NN stacking dG); stiffness convention (more stable stacking = stiffer).
    IDENTICAL to Appendices E/F/G -- the driver-gene gammas in param_db came from this."""
    s = stacking_signal(seq, nn)
    return float(-np.mean(s)) if s.size else 0.0


def spinodal(g):
    """The gamma -> emergence-onset map, re-used verbatim from Appendix A's emergence engine
    (code/emergence_v2): spinodal(g) = 2*(g/3)^1.5. Monotone increasing in gamma, so a stiffer
    promoter emerges LATER. argsort(spinodal(gamma)) is the deterministic emergence ORDER."""
    g = np.asarray(g, dtype=np.float64)
    return 2.0 * (g / 3.0) ** 1.5
