# LEDGER — Appendix E · the grammar hierarchy (reading the upper blueprint)

Honest per-channel grades. This appendix answers a **conceptual** question — is there a
tissue-level (and organ-level) γ/A4 the cell-level reading missed? — so the ledger is
explicit about which results are exact decompositions and real-sequence facts, which are
modelling choices, and which remain open functional/arrangement validations.

| grade | meaning |
|---|---|
| `[L]` | locked: real genomic sequence, published NN parameters, or cited TF motifs |
| `[V]` | verified: exact decomposition / logical invariant (precision) |
| `[F]` | fixed modelling choice (consensus motif set, window, seed); declared |
| `[O]` | open: functional / real-arrangement validation absent; named obstacle |

## Channels

| channel | grade | basis |
|---|:---:|---|
| the (LEVEL, SHAPE) = (gamma, A4) decomposition at every grammar level | `[V]` | the SAME robust_z operator (median-centred, MAD-scaled) is applied at G1, G2, G3 -- scale- and shift-invariant SHAPE to machine epsilon; the cell-level grammar lifted, not a new ad hoc rule per level. |
| TISSUE IDENTITY readable from the regulatory grammar (G2) | `[L]` | on REAL human promoters, the cardiac TF grammar separates cardiac (NPPA, TNNT2) from housekeeping (GAPDH) by ~14x, while the material grammar gamma_1 does not carry that identity. A tissue-level blueprint exists and is sequence-readable -- the upper A4 the corpus missed. |
| the upper grammar is information ABOVE the material (shuffle invariance) | `[V]` | a dinucleotide-preserving shuffle preserves the material LEVEL gamma_1 EXACTLY (gamma_1 is the mean of dimer dG, and dimer counts are preserved) yet collapses the cardiac grammar (~76% lost) -- so NONE of the tissue identity is at the material level. |
| the grammar levels are orthogonal | `[V]` | the G1 (material) and G2 (regulatory) signals are largely uncorrelated along the real sequence (\|corr\| ~ 0.04) -- distinct projections of the blueprint, not the same signal twice. |
| the cardiac TF grammar (GATA, NKX2-5, MEF2, TBX5, HAND) | `[L]` | the core cardiac regulatory network; consensus motifs from JASPAR and the cardiac-GRN literature (Olson 2006; Bruneau 2013). Their combinatorial binding-site syntax is the established cis-regulatory grammar of cardiac enhancers. |
| consensus (IUPAC) motif matching and the window/seed choices | `[F]` | consensus matching is a documented simplification of full PWM scoring; the sliding-window half-width and the shuffle seed are declared modelling choices, not tuned to a target. |
| FUNCTIONAL validation: A4_2 predicts measured cardiac enhancer ACTIVITY | `[O]` | the regulatory grammar is READ from sequence; that its arrangement A4_2 predicts measured cardiac enhancer activity is not yet tested. |
| the real spatial ARRANGEMENT MAP (배치도) at the organ level (G3) | `[O]` | G3 here is the local element layout (spacing of regulatory hotspots); the true spatial tissue arrangement is not yet validated. |
| ABSOLUTE modulus magnitudes (kPa) | `[O]` | the regulatory grammar reads tissue IDENTITY and ARRANGEMENT, not the kilopascal magnitudes; those remain measured inputs (Appendix D). |

## Earned-completion test

`completion.complete = False`

the tissue-level and organ-level grammars are found and formalized -- a (gamma, A4) pair at the regulatory and architecture levels, read with the same operator as the cell, with tissue identity sequence-readable [L], proven to be information above the material level [V], and orthogonal to it [V]. But the arrangement's FUNCTIONAL phenotype (measured enhancer activity) and the real 3D arrangement map are not yet validated -- three channels [O]. The upper blueprint is read; its quantitative validation is the next obstacle.

### What was found

the corpus had read only the bottom (material) blueprint; the tissue blueprint (cardiac TF grammar -> A4_2) and the organ blueprint (element layout -> A4_3) are real, sequence-readable, and were missing -- which is why the heart forced external moduli.

### Open obstacles (named)

- **FUNCTIONAL validation: A4_2 predicts measured cardiac enhancer ACTIVITY** → needs: a held-out cardiac functional dataset (VISTA cardiac enhancers, cardiac ATAC-seq/H3K27ac, or MPRA) with a pre-registered rank test and a shuffle control
- **the real spatial ARRANGEMENT MAP (배치도) at the organ level (G3)** → needs: measured 3D-genome contacts (Hi-C/Micro-C) or the colinear spatial-domain TF map (Hox-style), staged across development
- **ABSOLUTE modulus magnitudes (kPa)** → needs: the co-registered modulus series of Appendix D (this package does not supersede it; it reduces the IDENTITY/ARRANGEMENT import)

---

*precision (정밀) ≠ accuracy (정확). 반증 = 발견. The upper blueprint is found and
formalized — its functional and 3D-arrangement validation is the next obstacle.*
