# LEDGER — Appendix F · grammar completion (the full grammar space + decoding declaration)

Honest per-channel grades. This appendix **completes** the grammar map (organ atlas + G4 dynamical +
G5 body-plan) and issues a **two-axis** decoding declaration, so the ledger is explicit about which
results are exact decompositions / real-data facts, which are modelling choices, and which remain open
functional validations. The completion is two-axis: **structural complete, functional `False`**.

| grade | meaning |
|---|---|
| `[L]` | locked: real genomic sequence / assembly coordinates / cited TF motifs / cited colinearity |
| `[V]` | verified: exact decomposition / logical invariant (precision) |
| `[F]` | fixed modelling choice (consensus motifs, windows, seed, thresholds); declared |
| `[O]` | open: functional / quantitative validation absent; named obstacle |

## Channels

| channel | grade | basis |
|---|:---:|---|
| one operator across the whole grammar space (G1, G2, G4, G5) | `[V]` | the SAME robust_z operator (median-centred, MAD-scaled) is applied at the material, regulatory, dynamical, and body-plan levels -- scale- and shift-invariant SHAPE to machine epsilon; one operator applied many times, not a pile of ad hoc rules. |
| the ORGAN ATLAS -- the regulatory grammar reads identity across organs | `[L]` | on real human promoters the MEAN organ × grammar confusion matrix is diagonal-dominant: cardiac, neural, and hepatic each peak on their OWN grammar (shuffle-normalized enrichment-z), and the GAPDH housekeeping control stays quiet. G2 is not heart-specific. |
| the DYNAMICAL grammar G4 is a real rung above the material | `[V]` | the CpG-O/E methylation-sensitivity signal is orthogonal to the material stacking signal along the sequence (mean \|corr\| = 0.102 < 0.30), and the SAME operator produces A4₄ -- a distinct level (pragmatics), not a relabelling of G1; one locus → a family of readings by cell state. |
| the BODY-PLAN grammar G5 -- Hox colinearity on real coordinates | `[L]` | on the real HOXD cluster (nine GRCh38 coordinates from NCBI), the genomic order is monotonic with the AP body axis (rank-rank \|corr\| = 1.000; Pearson \|corr\| = 0.968, both ≥ 0.90); the same operator gives A4₅. Position on the DNA = position in the body. |
| the organ grammars, the CpG window, the shuffle, and the thresholds | `[F]` | the organ consensus-motif sets (cardiac identical to App. E; neural and hepatic from the respective GRN literature), the CpG-island window, the shuffle seed and count, and the gate thresholds are declared modelling choices, not tuned to a target. |
| STRUCTURAL decoding declaration -- the grammar is fully mapped | `[V]` | every grammatical level (G1..G5) is identified, formalized as a (γ, A4) pair, sequence-readable, orthogonal, and read by one operator, across organs. No grammatical level remains undiscovered; the structural completion is earned by the fail-closed gate. |
| FUNCTIONAL decoding: each level's A4 predicts the MEASURED phenotype | `[O]` | the grammar is read from sequence; that each level's arrangement predicts the measured phenotype is not yet tested. |
| the organ atlas as a validated CLASSIFIER / the liver grammar strength | `[O]` | the mean matrix is diagonal-dominant on an eight-promoter organ panel, but per-gene argmax is noisy at small counts and the hepatic grammar is the weakest (enhancer-distributed); a sequence-readability result, not a validated classifier. |
| ABSOLUTE magnitudes (kPa moduli, methylation β, 3D coordinates) | `[O]` | the grammar reads identity, arrangement, state-coupling, and body order, not the absolute physical magnitudes; those remain measured inputs. |

## Earned-completion test (two axes)

`structural_complete = True` · `functional_complete = False`

The **grammar** is fully mapped -- the interpretation axis (G1 material → G2 regulatory → G4 dynamical)
and the organization axis (G3 architecture → G5 body-plan), read across organs by one operator, with no
remaining undiscovered level `[V]`/`[L]`. But the **functional** phenotype (measured enhancer activity,
absolute methylation state, the real 3D body map, absolute moduli) is not yet validated -- named `[O]`.
**Structural decoding: 100%. Functional decoding: open.** The “100% decoding declaration” means the
grammar is fully mapped; what remains is measurement, not undiscovered grammar. Functional completion
is never asserted (gate `F10` fails closed on a false victory).

### What was found

The grammar is not a single ladder but a 2D space, now filled in: the organ atlas generalizes the
regulatory grammar across cardiac, neural, and hepatic; G4 (pragmatics) adds the state/time-dependent
reading; G5 (genre) adds the whole-body Hox colinearity. The same operator reads every cell of the
space.

### Open obstacles (named)

- **FUNCTIONAL validation per level** → needs: held-out functional datasets — organ enhancer **activity**
  (VISTA / ATAC-seq / H3K27ac / MPRA, pre-registered rank test + shuffle control); **absolute methylation
  state** (WGBS β-values); the **real 3D body map** (Hi-C/Micro-C across the embryo; staged colinear
  spatial TF domains).
- **the organ atlas as a validated classifier** → needs: a larger held-out promoter/enhancer panel per
  organ with a pre-registered classification test (the hepatic grammar is the weakest).
- **ABSOLUTE magnitudes** → needs: the measured modulus series (Appendix D), WGBS methylation levels, and
  3D-genome coordinates — this appendix does not supersede them.

---

*precision (정밀) ≠ accuracy (정확). 반증 = 발견. The grammar is fully mapped — structural decoding*
*complete; functional decoding is the next obstacle.*
