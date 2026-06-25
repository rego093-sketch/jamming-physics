# -*- coding: utf-8 -*-
"""
completion -- the GRAMMAR-COMPLETION interpreter (Appendix F).

Appendix E found that the DNA blueprint is read at a TOWER of grammatical levels, each with
the same (LEVEL, SHAPE) = (gamma, A4) decomposition lifted by one operator: G1 material
(cell, phonology), G2 regulatory (tissue, syntax), G3 architecture (organ, discourse). It
left the grammar a single ladder, read for one organ, and completion honestly False.

This package COMPLETES the grammar map in three directions and issues an honest decoding
declaration:

  ORGAN ATLAS (장기별)  -- G2 generalized horizontally: the SAME regulatory operator reads
                          cardiac, neural, AND hepatic identity from real promoters (a 3x3
                          organ x grammar confusion matrix), not the heart alone.
  DYNAMICAL G4 (동역학) -- a new rung, pragmatics: one locus -> a FAMILY of readings by cell
                          state, indexed by a CpG-island methylation-sensitivity signal that
                          is orthogonal to the material and read by the same operator ->
                          (gamma_4, A4_4).
  BODY-PLAN G5 (장르)   -- a new rung, genre (더 크고 더 넓게): Hox colinearity -- linear
                          genomic order equals anterior-posterior body order -- read on the
                          real HOXD cluster by the same operator -> (gamma_5, A4_5).

The grammar is thus not a ladder but a 2D SPACE: an INTERPRETATION axis (G1 -> G2 -> G4) and
an ORGANIZATION axis (G3 -> G5), read across organs (the atlas), every cell by one operator.

THE DECODING DECLARATION is two-axis and honest:
  STRUCTURAL / grammatical decoding -- COMPLETE (100%): every grammatical level is identified,
      formalized as a (gamma, A4) pair, sequence-readable, orthogonal, and read by one
      operator. No grammatical level remains undiscovered.
  FUNCTIONAL / quantitative decoding -- OPEN: the prediction of measured enhancer activity,
      absolute methylation state, and the real 3D body map are named [O] obstacles.
"100%" means the grammar is fully mapped -- what remains is MEASUREMENT, not undiscovered
grammar. Functional completion is held False and never asserted.

Discipline (inherited): LOCK -> Derive -> Gate; precision (정밀) != accuracy (정확);
반증 = 발견; no fitted parameters; 2x SHA-256 determinism; fail-closed gate; honest
[L]/[V]/[F]/[O] grades. Add-only: Appendix E's G1/G2/G3 and every prior number, grade,
equation, and DOI are unchanged; the cardiac grammar and the three Appendix E sequences are
re-locked verbatim; G4/G5 are new rungs and the atlas is G2 generalized.

Modules:
  lock           every locked input from param_db.json (3 organ grammars, 9 real promoters,
                 HOXD coordinates + body ranks, NN parameters, settings); zero inline magic
  seqtools       robust_z (the A4 operator, identical at every level and to Appendix E),
                 revcomp, the Altschul-Erickson dinucleotide-preserving shuffle
  material       G1 -- the material signal (re-locked; the orthogonality reference for G4)
  atlas          the ORGAN ATLAS -- G2 generalized; the organ x grammar confusion matrix
  dynamical      G4 -- the dynamical/state grammar (CpG O/E -> gamma_4, A4_4; state family)
  bodyplan       G5 -- the body-plan grammar (Hox colinearity -> gamma_5, A4_5)
  grammar_space  the 2D grammar-space map + the one-operator proof across G1, G2, G4, G5
  declaration    the two-axis decoding declaration (structural complete / functional open)
  grading        the one place precision != accuracy; honest ledger + two-axis completion
  interpreter    interpret_grammar_completion() (+) reading_hash (2x SHA-256)
  gate           fail-closed F1..F10 (incl. the honest-declaration gate)
"""

from . import (lock, seqtools, material, atlas, dynamical, bodyplan,
               grammar_space, declaration, grading, interpreter, gate)

__all__ = [
    "lock", "seqtools", "material", "atlas", "dynamical", "bodyplan",
    "grammar_space", "declaration", "grading", "interpreter", "gate",
]

__version__ = "0.1.0"
