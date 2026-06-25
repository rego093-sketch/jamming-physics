# CHANGELOG — Appendix F · grammar completion: the full grammar space and the decoding declaration

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.13 + Appendix E (the grammar hierarchy: G1 material, G2 regulatory, G3 architecture,
read by one operator, for one organ, completion False). This increment adds **Appendix F — grammar
completion**, a new applied volume that completes the grammar SPACE in three directions and issues an
honest two-axis decoding declaration. It is **add-only**: no chapter, appendix, number, grade,
equation, table, or DOI of v1.13 or any prior appendix is altered. The cardiac grammar and the three
Appendix E promoter sequences are **re-locked verbatim**. One new section is added (the site goes from
21 to **22** sections), the contents/sitemap/meta/gate are extended, and Appendix E gains a forward
nav link.

## The instruction

Continue past Appendix E: *there may be a larger grammar above the tissue level; there may be
organ-specific and dynamical grammars; push all the way to a 100% decoding declaration; look bigger
and wider (더 크고 더 넓게).* Each clause names a real gap. Appendix E read the regulatory grammar for
**one** organ (the heart); it stopped at the architecture level (a **fixed** property of the
sequence); and its completion, though honestly False, did not say what "decoded" would mean.

## The completed grammar space (the same operator, two axes, read across organs)

The grammar is not a single ladder but a 2D **space**, every cell read by the identical robust-z
operator:

| axis | levels | linguistics |
|---|---|---|
| **interpretation** (how a fixed text is read) | **G1** material (cell) → **G2** regulatory (tissue) → **G4** dynamical (state) | phonology → syntax → **pragmatics** |
| **organization** (how the text is laid out) | **G3** architecture (organ) → **G5** body-plan (body) | discourse → **genre** |
| **breadth** (the **organ atlas**) | G2 read across **cardiac, neural, hepatic** | — |

G1/G2/G3 are Appendix E (unchanged). The **organ atlas**, **G4**, and **G5** are this appendix.

## Three directions, on real data (not circular)

> **1 — The organ atlas (장기별).** The cardiac grammar of Appendix E is joined by a neural grammar
> (SOX, BRN/POU, REST, NEUROD, OLIG) and a hepatic grammar (HNF4A, HNF1A, FOXA, CEBPA, DBP) and run
> against **nine real human promoters** spanning three organs plus a housekeeping control. Reading is
> the **shuffle-normalized enrichment-z** of each grammar's motif content against a
> dinucleotide-preserving background (removes the GC/degeneracy confound of raw counts). The MEAN
> organ×grammar confusion matrix is **diagonal (3/3)** — cardiac 2.92, neural 1.28, hepatic 0.41 each
> the row max — and the GAPDH control is **quiet** (max z = 0.06). The regulatory grammar reads organ
> identity across the atlas, not the heart alone. `[L]`
>
> **2 — The dynamical grammar G4 (동역학, pragmatics).** A new rung: one locus → a **family** of
> readings by cell **state**, indexed by the CpG-island methylation-sensitivity potential (windowed
> CpG O/E). It is sequence-readable but indexes `drive_eff(x; s) = base(x) − κ·island(x)·s` over the
> methylation state. Two facts make it a real rung: the CpG-O/E signal is **orthogonal** to the
> material stacking signal (mean **|corr| = 0.102**, ceiling 0.30), and the **same** operator gives
> A4₄. `[V]` The absolute methylation state is named `[O]` (WGBS).
>
> **3 — The body-plan grammar G5 (genre, 더 크고 더 넓게).** The highest organizing level: Hox
> colinearity on the **real HOXD cluster** (nine GRCh38 coordinates fetched from NCBI). The genomic
> order of the nine genes is **perfectly monotonic** with the anterior-posterior body axis (rank-rank
> **|corr| = 1.000**), and the Pearson correlation on the raw coordinates is **0.968** (floor 0.90).
> Position on the DNA = position in the body; the same operator gives A4₅. `[L]`+`[V]` The real 3D
> body map is named `[O]` (Hi-C/Micro-C; staged spatial TF domains).

The SHAPE projection at **G1, G2, G4, G5** is the identical robust-z operator (scale/shift-invariant
to machine ε, 4.4e-16 / 3.6e-15). `[V]`

## The decoding declaration (해독 선언) — two axes, honest

The "100% decoding declaration" is met by separating two questions the word *decoding* conflates:

- **STRUCTURAL / grammatical decoding — COMPLETE (100%).** Every grammatical level (G1 material, G2
  regulatory, G3 architecture, G4 dynamical, G5 body-plan) is identified, formalized as a (γ, A4)
  pair, sequence-readable, orthogonal, and read by the identical operator, across organs. **No
  grammatical level remains undiscovered.** Earned by the fail-closed gate. `[V]`
- **FUNCTIONAL / quantitative decoding — OPEN.** That each level's A4 predicts the measured phenotype —
  enhancer **activity** per organ, the **absolute methylation state**, the **real 3D body map** — needs
  held-out measured data. Named `[O]`.

**`structural_complete = True` · `functional_complete = False`.** "100%" means the grammar is fully
mapped; what remains is **measurement, not undiscovered grammar**. Functional completion is never
asserted — gate `F10` fails closed on a false victory.

## What changed (all add-only)

New reproduction package `repro/dna/ax-f-grammar-completion/`:

- `completion/` — 11 modules + package init: `lock` (3 organ grammars, 9 REAL promoters with
  accession+coords, HOXD coordinates + AP body ranks, NN parameters, settings; **zero inline magic
  numbers**), `seqtools` (`robust_z` — the A4 operator, identical at every level and to Appendix E;
  `revcomp`; the Altschul-Erickson dinucleotide-preserving shuffle), `material` (G1 re-locked; the
  orthogonality reference for G4), `atlas` (the organ atlas — G2 generalized; the organ×grammar
  confusion matrix), `dynamical` (G4 — CpG O/E → γ₄, A4₄; the state family), `bodyplan` (G5 — Hox
  colinearity → γ₅, A4₅), `grammar_space` (the 2D map + the one-operator proof across G1/G2/G4/G5),
  `declaration` (the two-axis decoding declaration), `grading` (the one place precision ≠ accuracy),
  `interpreter` (`interpret_grammar_completion()` ⊕ `reading_hash` 2×SHA-256), `gate` (fail-closed
  `F1..F10`; `python3 -m completion.gate`).
- `param_db.json` — three organ TF grammars (cardiac = Appendix E; neural and hepatic from the
  respective GRN literature), nine real human promoter sequences (NPPA/TNNT2 cardiac + GAPDH control
  re-locked from Appendix E; PAX6/NEUROD1/SYN1 neural; ALB/APOA1/TTR hepatic, each with accession,
  coordinates, provenance), the HOXD cluster (nine GRCh38 TSS + AP body ranks, with the colinearity
  citation), NN stacking parameters, settings (shuffle seed/count, CpG window, gate thresholds).
- `run.py` → `expected/*.json` + `RESULT.txt` (deterministic; 2×SHA-256).
- `README.md`, `LEDGER.md`.

New HTML section `docs/dna/ax-f-grammar-completion/index.html` (VP-SPEC v1.8, answer-first, prev →
Appendix E). Site wiring extended: `_meta.json` appendix **F** row (chapters 16 + appendices 6 = 22);
`sitemap.xml` AX-F URL (hub + 22 = 23 `<loc>`); hub `index.html` TOC `<li class="apx">`, JSON-LD
`hasPart`, see-also cross-link, overview count ("five" → "six" applied appendices); Appendix E forward
nav `Appendix F →`; `gate_multipage.py` section/hub-link count `21 → 22`.

## Verification

- `python3 -m completion.gate` → **PASS 10/10** (`F1` one operator all levels · `F2` organ-atlas
  diagonal dominance · `F3` housekeeping control quiet · `F4` G4 orthogonal to material · `F5` G5 Hox
  colinear on real coords · `F6` no magic · `F7` non-fit · `F8` determinism · `F9` honest grades ·
  `F10` honest two-axis declaration / no false victory); `structural_complete = True`,
  `functional_complete = False`.
- `python3 run.py` → deterministic; reference reading hash `49ac99e570c7ab4b`; gate
  `sha=3220daaad4e94152`; byte-identical across runs.
- `python3 gate_multipage.py` → **PASS 252, WARN 1, FAIL 0** (the single WARN is the pre-existing
  source-monolith diff, warn-only).

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견. 문법.*
*Appendix E found the tower; Appendix F completes the grammar space — across organs (the atlas), up to*
*the state level (G4), out to the whole body (G5) — and declares the decoding honestly: structural*
*decoding complete, functional decoding the next obstacle. The grammar is fully mapped; what remains is measurement.*
