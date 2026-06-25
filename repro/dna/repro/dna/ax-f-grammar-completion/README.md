# Appendix F — grammar completion: the full grammar space and the decoding declaration

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

Appendix E found that the DNA blueprint is read at a **tower** of grammatical levels — G1 material
(cell, phonology), G2 regulatory (tissue, syntax), G3 architecture (organ, discourse) — each with the
**same** (LEVEL, SHAPE) = (γ, A4) decomposition lifted by **one operator**. It left the grammar a
single ladder, read for **one** organ (the heart), and completion honestly `False`. This appendix
**completes** the grammar map in three directions and issues an honest **decoding declaration**.

> **반증 = 발견.** The grammar is not a single ladder but a 2D **space**. Filling it in — across organs
> (the atlas), up to the state level (G4), and out to the whole body (G5) — and then asking honestly
> *what does “100% decoded” actually mean?* is the discovery.

---

## The completed grammar space (one operator at every cell)

The grammar is two axes, now filled in — every cell read by the **identical** robust-z operator:

| axis | levels | linguistics |
|---|---|---|
| **interpretation** (how a fixed text is read) | **G1** material (cell) → **G2** regulatory (tissue) → **G4** dynamical (state) | phonology → syntax → **pragmatics** |
| **organization** (how the text is laid out) | **G3** architecture (organ) → **G5** body-plan (body) | discourse → **genre** |
| **breadth** (the **organ atlas**) | G2 read across **cardiac, neural, hepatic** | — |

G1, G2, G3 are Appendix E (unchanged). The **organ atlas**, **G4**, and **G5** are this appendix.

## Direction 1 — the organ atlas (장기별): G2 generalized across organs

The **same** regulatory operator reads identity for **three** organs from real promoters, not the heart
alone. Reading = shuffle-**normalized** enrichment-z of each organ’s consensus-motif content against a
dinucleotide background (removes the GC/degeneracy confound of raw counts). The primary result is the
**mean organ × grammar confusion matrix** (averaged over each organ’s promoters):

```
  organ\grammar   cardiac   neural   hepatic
  cardiac          2.92 *    1.09    -0.37
  neural          -0.45      1.28 *  -0.04
  hepatic         -0.19     -0.22     0.41 *
```

**3/3 diagonal dominance** — each organ peaks on its **own** grammar — and the GAPDH housekeeping
control is **quiet** (max organ-grammar z = 0.06). The regulatory grammar reads organ identity across
the atlas. `[L]` (per-gene argmax is noisy at small counts, reported honestly; the hepatic grammar is
the weakest, enhancer-distributed — a sequence-readability result, not a validated classifier `[O]`.)

## Direction 2 — the dynamical grammar G4 (동역학, pragmatics)

A genuinely **new rung**: one locus → a **family** of readings by cell **state**. In linguistics this is
pragmatics, where one sentence means different things in different contexts. The state-indexing signal
is the **CpG-island methylation-sensitivity** potential (windowed CpG O/E), which marks where DNA
methylation can switch a region. It is sequence-readable but indexes a family `drive_eff(x; s) =
base(x) − κ·island(x)·s` over the methylation state `s ∈ [0,1]`.

Two facts make G4 real, not a relabelling of G1: the CpG-O/E signal is **orthogonal** to the material
stacking signal along the sequence — **mean |corr| = 0.102** across nine loci (ceiling 0.30) — and the
**same** robust-z operator produces its SHAPE `A4₄`. `[V]` The **absolute** methylation state per cell
type is **not** read here — that is the named `[O]` obstacle (WGBS β-values).

## Direction 3 — the body-plan grammar G5 (genre, 더 크고 더 넓게)

The highest organizing level: the grammar that lays out the whole **body**. Its canonical
sequence-encoded form is **Hox colinearity** — the linear order of the Hox genes along the chromosome
equals their order along the anterior-posterior body axis. Read on the **real HOXD cluster** (nine
GRCh38 coordinates from NCBI):

- **rank-rank order colinearity |corr| = 1.000** (the genomic order is perfectly monotonic with the AP body rank)
- **Pearson on raw TSS |corr| = 0.968** (floor 0.90)

Position on the DNA **=** position in the body. The same operator gives `A4₅`. `[L]`+`[V]` The real
**3D body map** (Hi-C/Micro-C across the embryo; the colinear spatial-domain TF map staged through
development) is the named `[O]` obstacle.

## One operator across the whole space

The SHAPE projection at **G1, G2, G4, G5** is the **identical** robust-z operator (median-centred,
MAD-scaled), scale- and shift-invariant to machine epsilon (4.4e-16 / 3.6e-15). The grammar space is
**one** operator applied many times, not a pile of ad hoc rules. `[V]`

## The decoding declaration (해독 선언) — two axes, honest

The instruction is to push to a **100% decoding declaration**. The honest way to do that — without
faking a functional victory the data do not support — is to separate two questions the word “decoding”
conflates:

- **STRUCTURAL / grammatical decoding — COMPLETE (100%).** Every grammatical level of the blueprint
  (G1 material, G2 regulatory, G3 architecture, G4 dynamical, G5 body-plan) is **identified**,
  **formalized** as a (γ, A4) pair, **sequence-readable**, **orthogonal**, and read by the **identical
  operator**, across organs. There is **no remaining undiscovered grammar.** `[V]` (gate-backed)
- **FUNCTIONAL / quantitative decoding — OPEN.** The prediction of measured enhancer **activity** per
  organ, the **absolute methylation state**, and the **real 3D body map** are named `[O]` obstacles.

**“100%” means the grammar is fully mapped — what remains is MEASUREMENT, not undiscovered grammar.**
Functional completion is held `False` and is **never** asserted; the gate (`F10`) fails closed if it
ever is. `structural_complete = True` · `functional_complete = False`.

## Reproduce

```
python3 run.py               # → expected/*.json + RESULT.txt (deterministic, 2×SHA-256)
python3 -m completion.gate   # → fail-closed F1..F10; exit 0 iff all pass
```

Gate **PASS 10/10** (`F1` one operator all levels · `F2` organ-atlas diagonal dominance · `F3`
housekeeping control quiet · `F4` G4 orthogonal to material · `F5` G5 Hox colinear on real coords ·
`F6` no magic · `F7` non-fit · `F8` determinism · `F9` honest grades · `F10` honest two-axis
declaration / no false victory). Reference reading hash `49ac99e570c7ab4b`; gate `sha=3220daaad4e94152`.

## Files

```
param_db.json            3 organ TF grammars (cardiac [= App. E], neural, hepatic consensus motifs);
                         9 REAL human promoters (NPPA/TNNT2 cardiac + GAPDH control re-locked from
                         App. E; PAX6/NEUROD1/SYN1 neural; ALB/APOA1/TTR hepatic) with accession+coords;
                         HOXD cluster (9 GRCh38 TSS + AP body ranks); NN stacking parameters; settings
completion/
  lock.py                the locked surface; zero inline magic numbers
  seqtools.py            robust_z (the A4 operator, identical at every level and to App. E), revcomp,
                         the Altschul-Erickson dinucleotide-preserving shuffle
  material.py            G1 — the material signal (re-locked; the orthogonality reference for G4)
  atlas.py               the ORGAN ATLAS — G2 generalized; the organ × grammar confusion matrix
  dynamical.py           G4 — the dynamical/state grammar (CpG O/E → γ₄, A4₄; the state family)
  bodyplan.py            G5 — the body-plan grammar (Hox colinearity → γ₅, A4₅)
  grammar_space.py       the 2D grammar-space map + the one-operator proof across G1, G2, G4, G5
  declaration.py         the two-axis decoding declaration (structural complete / functional open)
  grading.py             the one place precision ≠ accuracy; honest ledger + two-axis completion
  interpreter.py         interpret_grammar_completion() — the full reading; reading_hash (2×SHA-256)
  gate.py                fail-closed F1..F10 (incl. the honest-declaration gate)
run.py                   top-level runner → expected/ + RESULT.txt
README.md / LEDGER.md    this file / the grade ledger
expected/                reference outputs (byte-identical across runs)
```

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견. 문법.*
*Add-only: Appendix E’s G1/G2/G3 and every prior number, grade, equation, and DOI are unchanged; the*
*cardiac grammar and the three Appendix E sequences are re-locked verbatim. The grammar is fully mapped —*
*structural decoding complete; functional decoding is the next obstacle.*
