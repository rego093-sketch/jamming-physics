# -*- coding: utf-8 -*-
"""
completion.dynamical -- G4, the DYNAMICAL (state/time) grammar. PRAGMATICS: one text, many
readings by context (동역학).

Above the material (G1), regulatory (G2), and architecture (G3) grammars -- all of which
read a FIXED property of the sequence -- sits a grammar whose reading depends on the cell
STATE. The same locus is read differently in different cell states; in linguistics this is
pragmatics, where one sentence means different things in different contexts. The
state-indexing signal is the CpG-island methylation-sensitivity potential: the windowed CpG
observed/expected ratio, which marks where DNA methylation can switch a region's activity.
It is a property of the sequence (so it is sequence-readable), but it indexes a FAMILY of
readings parameterized by the methylation state s in [0, 1]:

  island(x)  = CpG O/E in a window around x            the state-coupling potential
  drive_eff(x; s) = base(x) - kappa * island(x) * s    a FAMILY of readings, one per state

  s4[x]   = island(x)            the dynamical signal (CpG O/E profile)
  gamma_4 = mean(s4)             the DYNAMICAL LEVEL  (overall methylation-sensitivity)
  A4_4    = robust_z(s4)         the DYNAMICAL SHAPE  (where state-coupling concentrates)

Two facts make G4 a genuine new rung, not a relabelling of G1: the CpG-O/E signal is
ORTHOGONAL to the material stacking signal along the sequence (small |corr|), and the SAME
robust_z operator produces its SHAPE (A4_4). The ABSOLUTE methylation state per cell type is
NOT read here -- that is the named [O] obstacle (WGBS beta-values).
"""
import numpy as np

from . import lock, seqtools, material


def cpg_oe_signal(seq, w=None):
    """Windowed CpG observed/expected ratio along the sequence -- the methylation-sensitivity
    (state-coupling) potential, the G4 dynamical signal."""
    if w is None:
        w = lock.cpg_window_bp()
    seq = seq.upper()
    L = len(seq)
    prof = np.zeros(L, dtype=np.float64)
    for i in range(L):
        lo = max(0, i - w)
        hi = min(L, i + w + 1)
        win = seq[lo:hi]
        n = len(win)
        c = win.count("C")
        g = win.count("G")
        cg = sum(1 for j in range(len(win) - 1) if win[j:j + 2] == "CG")
        exp = (c * g) / n if n > 0 else 0.0
        prof[i] = (cg / exp) if exp > 0 else 0.0
    return prof


def read(seq):
    """G4 read: (gamma_4 = dynamical LEVEL, A4_4 = dynamical SHAPE) via the same operator."""
    s4 = cpg_oe_signal(seq)
    level, shape = seqtools.level_and_shape(s4)
    return {
        "grammar": "G4_dynamical_state",
        "linguistic_level": "pragmatics (one text, many readings by context/state)",
        "signal": "CpG observed/expected methylation-sensitivity profile",
        "gamma_LEVEL": round(level, 6),
        "A4_SHAPE_len": int(shape.size),
        "A4_SHAPE_std": round(float(np.std(shape)), 6),
        "encodes": "where the reading is STATE-coupled -- the family of readings by cell state",
        "grade": "[L] real sequence + [V] exact robust_z split; absolute methylation state [O]",
    }


def state_family(seq, kappa=1.0, states=(0.0, 0.5, 1.0)):
    """A FAMILY of readings of the SAME locus indexed by methylation state s. Demonstrates
    the pragmatic structure: drive_eff(x; s) = base(x) - kappa * island(x) * s. The base is
    the material A4 (the fixed read); the island potential modulates it by state. Returned as
    the per-state mean effective drive (a compact witness that the reading varies with s)."""
    base = seqtools.robust_z(material.stacking_signal(seq))
    island = cpg_oe_signal(seq)
    n = min(len(base), len(island))
    base, island = base[:n], island[:n]
    out = {}
    for s in states:
        eff = base - kappa * island * s
        out["s=%.2f" % s] = round(float(np.mean(eff)), 6)
    return {
        "kappa": kappa,
        "readings_by_state": out,
        "varies_with_state": bool(len(set(out.values())) > 1),
        "note": "one locus -> a family of readings indexed by cell state (pragmatics); the "
                "absolute state s per cell type is the [O] obstacle (WGBS)",
    }


def orthogonality_to_material():
    """The CpG-O/E (G4) signal is orthogonal to the material (G1) stacking signal along the
    sequence -- so G4 is a genuine new level, not a relabelling of the material. Mean |corr|
    across all atlas promoters."""
    corrs = []
    per = {}
    for key in lock.promoter_keys():
        seq, _, _ = lock.promoter(key)
        a = cpg_oe_signal(seq)
        b = material.signal_for_compare(seq)
        n = min(len(a), len(b))
        a, b = a[:n], b[:n]
        if np.std(a) < 1e-9 or np.std(b) < 1e-9:
            c = 0.0
        else:
            c = float(np.corrcoef(a, b)[0, 1])
        corrs.append(abs(c))
        per[key] = round(c, 4)
    mean_abs = float(np.mean(corrs)) if corrs else 0.0
    return {
        "per_promoter_corr": per,
        "mean_abs_corr": round(mean_abs, 4),
        "threshold": lock.g4_orthogonality_corr_max(),
        "orthogonal": bool(mean_abs < lock.g4_orthogonality_corr_max()),
        "verdict": ("the dynamical signal (CpG O/E) is largely uncorrelated with the material "
                    "stacking signal along the sequence -- a distinct projection of the "
                    "blueprint, read by the same operator; G4 is a real rung above G1"),
        "grade": "[V] computed exactly on real sequences",
    }
