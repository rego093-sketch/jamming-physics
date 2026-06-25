# -*- coding: utf-8 -*-
"""
grammar -- the GRAMMAR-HIERARCHY interpreter (Appendix E).

The corpus has read the DNA blueprint at ONE grammatical level: the cell-level material
(gamma = mean nearest-neighbour stacking dG; A4 = its robust-z pattern) -- the chemistry of
adjacent base pairs, the bottom blueprint. This package finds the HIGHER blueprints it
missed, each with the SAME (LEVEL, SHAPE) = (gamma, A4) decomposition lifted up the tower:

  G1 material   (cell,   PHONOLOGY)  -- stacking dG          -> (gamma_1, A4_1)
  G2 regulatory (tissue, SYNTAX)     -- cardiac TF grammar    -> (gamma_2, A4_2)  THE MISSED A4
  G3 architecture (organ, DISCOURSE) -- element layout        -> (gamma_3, A4_3)  THE 배치도

On REAL human promoters it shows: (1) the regulatory grammar G2 reads cardiac tissue
identity from sequence (~14x cardiac vs housekeeping) while the material grammar G1 does
not; (2) a dinucleotide-preserving shuffle preserves the material level gamma_1 EXACTLY yet
collapses the cardiac grammar, so the tissue identity is information ABOVE the material
level; (3) the levels are orthogonal. This locates, in the sequence, the arrangement the
heart forced Appendix D to import as external moduli -- the blueprint had it, one grammar
level up.

Discipline (inherited): LOCK -> Derive -> Gate; precision (정밀) != accuracy (정확);
반증 = 발견; no fitted parameters; 2x SHA-256 determinism; fail-closed gate; honest
[L]/[V]/[F]/[O] grades; completion earned (here False -- the upper grammar is found and
formalized, its functional/3D validation is the next [O]).

Modules:
  lock           every locked input from param_db.json (NN parameters, cardiac motifs, the
                 three REAL promoter sequences, shuffle seed); zero inline magic numbers
  seqtools       robust_z (the A4 operator, identical at every level), revcomp, the
                 dinucleotide-preserving (Altschul-Erickson) shuffle
  material       G1 -- the cell/material grammar (stacking dG -> gamma_1, A4_1)
  regulatory     G2 -- the tissue/regulatory grammar (cardiac TF syntax -> gamma_2, A4_2)
  architecture   G3 -- the organ/architecture grammar (element layout -> gamma_3, A4_3)
  hierarchy      the three results: tissue identity readable, upper-grammar-above-material,
                 orthogonality; the same-operator proof
  heart          the heart resolution: the arrangement is sequence-readable, reducing the
                 external-data reliance of Appendix D
  grading        the one place precision != accuracy; honest ledger + completion
  interpreter    interpret_grammar_hierarchy() ⊕ reading_hash (2x SHA-256)
  gate           fail-closed E1..E9
"""

from . import (lock, seqtools, material, regulatory, architecture,
               hierarchy, heart, grading, interpreter, gate)

__all__ = [
    "lock", "seqtools", "material", "regulatory", "architecture",
    "hierarchy", "heart", "grading", "interpreter", "gate",
]

__version__ = "0.1.0"
