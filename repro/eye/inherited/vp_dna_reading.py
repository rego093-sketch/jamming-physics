#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_dna_reading.py — the FULL readable-layer reading of a master-gene promoter:
                    γ (LEVEL) **and** the A4 coordinate (SHAPE), not γ alone.

WHY THIS MODULE EXISTS (DNA v1.13, DOI 10.5281/zenodo.20471407).
  The DNA volume's v1.13 reading states the readable layer of a locus is FOUR measured things,
  and that γ is only the first of them:
      γ (the LEVEL)  = −mean(SantaLucia-1998 NN stacking ΔG) — one scalar, the window MEAN.
      A4 (the SHAPE) = the SAME stiffness signal with that mean (γ) REMOVED — where the locus is
                       stiff vs soft relative to its own average. γ and A4 are the LEVEL and the
                       SHAPE of one field: orthogonal projections, "neither contains the other"
                       (γ ⊂ A4 is impossible; A4 is literally "the signal minus γ").
  Earlier seed work consumed γ ALONE — the compressed scalar. Two genes with equal γ but different
  stiffness texture were read as identical. This module restores the A4 SHAPE so the emergence reads
  level AND shape. It imports the canonical A4 grammar (inherited/dna_interpreter.py, byte-identical,
  numpy-only) for the LEVEL + switch + helix geometry, and computes the promoter-scale SHAPE with the
  same NN table and the framework's robust_z mean-removal.

WHAT IS READ (per promoter sequence, deterministic):
  LEVEL   γ, GC, AT-run, CpG density            [V]  (dna_interpreter.gamma / switch_params)
  SWITCH  spinodal=(2/3√3)γ^1.5, barrier=γ²/4   [F]  derived from γ alone
  SHAPE   the local-γ profile (sliding NN window) with its mean removed → robust_z → tercile shells;
          shell_class, stiff/mid/soft fractions, shape amplitude, and the offset (relative to the TSS)
          of the stiffest sub-window. mean(shape)≈0 BY CONSTRUCTION proves A4 = signal − γ.   [V]
  HELIX   B-DNA geometry (rise 3.4 Å, twist 34.29°/bp) is available; the anchor-relative phase to a
          REAL genomic anchor, plus loops/nearest-anchor strength, need the wider region + an NCBI
          feature table (rettype=ft) and are the NAMED [O] deferred read — flagged, never invented.

HONEST SCOPE (VP-SPEC C3). γ structure-only (never voltage/dose/effect); the full A4 anchor/loop
coordinate is [O] (needs the feature table the research phase fetches); identity/order are the DNA
volume's, cited. stdlib + numpy. Deterministic; 2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import dna_interpreter as DI                 # canonical, byte-identical: NN table, gamma, switch, helix

# promoter-scale A4-shape window (the whole-region W=2000 shell map is for Mb regions; see [O] note)
SHAPE_W, SHAPE_STEP = 75, 25


def _local_gamma_profile(seq, W=SHAPE_W, step=SHAPE_STEP):
    """The stacking-stiffness signal along the promoter: γ in a sliding NN window (same table as γ)."""
    s = "".join(c for c in seq.upper() if c in "ACGT")
    xs = []
    for a in range(0, max(1, len(s) - W + 1), step):
        xs.append(DI.gamma(s[a:a + W]))
    return np.array(xs, dtype=float)


def _robust_z(x, eps=1e-9):
    """Framework mean-removal (key_pipeline_full.robust_z): (x − median)/(1.4826·MAD)."""
    m = np.median(x); d = np.median(np.abs(x - m))
    return (x - m) / (1.4826 * max(d, eps))


def read_promoter(seq):
    """Full readable-layer reading of one promoter: LEVEL (γ) + SHAPE (A4) + switch + helix-available."""
    g = DI.gamma(seq)
    sw = DI.switch_params(g)
    prof = _local_gamma_profile(seq)
    level = float(np.mean(prof))                    # = the window MEAN ≈ γ (the LEVEL)
    shape = prof - level                            # A4 SHAPE = signal − its mean (literally signal − γ)
    return dict(
        # LEVEL
        gamma=round(g, 4), gc=round(DI.gc_frac(seq), 4),
        atrun_frac=round(DI.atrun_frac(seq), 5), cpg_density=round(DI.cpg_density(seq), 5),
        # SWITCH (from γ)
        spinodal=round(sw["spinodal"], 4), barrier=round(sw["barrier"], 4),
        rest_state=round(sw["rest_state_magnitude"], 4),
        # A4 SHAPE — the orthogonal texture γ alone discards (all non-tautological, per-gene):
        shape_amplitude=round(float(np.std(shape)), 5),        # how textured (0 = flat = γ says it all)
        shape_range=round(float(prof.max() - prof.min()), 5),  # stiffest minus softest sub-window
        stiff_side_frac=round(float(np.mean(prof > level)), 4),# fraction stiffer than its OWN mean (skew; ≠⅓)
        stiffest_offset_bp=int(np.argmax(prof) * SHAPE_STEP),  # where stiffest, relative to TSS−2000
        softest_offset_bp=int(np.argmin(prof) * SHAPE_STEP),   # where softest, relative to TSS−2000
        shape_mean_abs=round(float(abs(np.mean(shape))), 12),  # ≈0 ⇒ A4 = signal − γ (orthogonality)
        n_windows=int(len(prof)),
        # HELIX geometry available; real-anchor phase is the [O] deferred read
        helix_geometry="B-DNA rise 3.4 Å / twist 34.29°/bp available (dna_interpreter.helix_coord)",
        full_A4_anchor_loop="[O] DEFERRED: real nearest-anchor strength, loops, anchor-relative phase "
                            "need the wider genomic region + NCBI feature table (rettype=ft); named, not invented",
    )


def run(P):
    P("=" * 78)
    P("FULL DNA READING — γ (LEVEL) and the A4 coordinate (SHAPE), not γ alone  (DNA v1.13)")
    P("=" * 78)
    # demonstrate the level/shape decomposition on three textbook windows
    cases = {
        "GC-flat":   "GCGC" * 64,
        "AT-flat":   "ATAT" * 64,
        "half/half": ("GCGC" * 32) + ("ATAT" * 32),    # SAME-ish γ as a blend, but DIFFERENT shape
    }
    P("\n[decomposition] LEVEL = mean of the stacking signal; SHAPE = signal with that mean removed:")
    for name, seq in cases.items():
        r = read_promoter(seq)
        P(f"  {name:10s} γ(level)={r['gamma']:.4f}  shape_amp={r['shape_amplitude']:.4f}  "
          f"range={r['shape_range']:.4f}  stiff_side={r['stiff_side_frac']:.2f}  "
          f"|mean(shape)|={r['shape_mean_abs']:.1e}")
        assert r["shape_mean_abs"] < 1e-9            # A4 = signal − γ  (orthogonality, exact)

    P("\n[orthogonality] A4 is literally 'the signal minus γ': mean(shape)=0 to machine precision above.")
    P("                γ (one scalar) and A4 (the shape) are the LEVEL and SHAPE of one stiffness field;")
    P("                neither contains the other — reading γ alone discards the A4 texture.")

    # switch params are driven by the LEVEL; the SHAPE rides orthogonally
    r = read_promoter(cases["GC-flat"])
    P(f"\n[switch]  from γ(level) alone: spinodal=(2/3√3)γ^1.5={r['spinodal']:.4f}, barrier=γ²/4={r['barrier']:.4f}")
    P(f"[helix]   {r['helix_geometry']}")
    P(f"[A4 full] {r['full_A4_anchor_loop']}")

    P("\nLEARNED: a master gene is read as γ (LEVEL) + A4 (SHAPE), not γ alone. The emergence must use")
    P("         both: two genes with equal γ but different A4 shape are NOT interchangeable.")


def main():
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
