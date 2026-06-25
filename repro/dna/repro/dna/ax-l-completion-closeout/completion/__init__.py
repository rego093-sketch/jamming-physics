# -*- coding: utf-8 -*-
"""
Appendix L -- the blueprint close-out (B4 closed; B2 data-blocked; the roadmap fully mapped).

Takes the K BLUEPRINT to its honest terminus, ADD-ONLY:
  B4  CLOSE the jitter floor: ONE cited upstream edge (MEOX1 -> PAX7) removes PAX7 as an artificial
      cascade source, lifting the +-1 rank-jitter p5 of Spearman(depth, Carnegie) from 0.625 (below
      the 0.70 floor) to 0.728 (above it), 0 new inversions, DAG preserved. Jitter-robust but [L],
      NEVER [V] (B3 ceiling).
  B2  RESOLVE the cis-code -> drive map as DATA-BLOCKED: a deterministic TF-motif-occupancy probe on
      the cached GRCh38 child promoters vs a dinucleotide-shuffle null shows the per-edge drive is
      NOT in the +-2 kb promoter window (the canonical SOX9-|RUNX2 edge is below background). Closing
      it needs distal-enhancer + accessibility sequence the kit lacks -- a MEASUREMENT limit, graded
      [F], not [L].

Everything else (the 63-gene atlas, the DAG/wavefront/order results, B1 absolute clock, O2 sub-clock,
O3 sequence-drive, the quorum/AND gate) is inherited from Appendix K and RE-AUDITED byte-for-byte on
the B4-extended cascade. physical_complete stays False (B2 is data-blocked). No body is built.

ADD-ONLY over Appendices A-K: every prior page, number, grade, equation and DOI is unchanged.
"""
from . import (seqtools, lock, cascade, coupled, timing, nulltest, grammar,
               cis, declaration, grading, interpreter, gate)  # noqa: F401,E402

__all__ = ["seqtools", "lock", "cascade", "coupled", "timing", "nulltest",
           "grammar", "cis", "declaration", "grading", "interpreter", "gate"]
