# CHANGELOG — Appendix E · the grammar hierarchy: reading the upper blueprint

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.13 + Appendix A (the γ gene-clock, heart null) + Appendix C (the jamming tower) + Appendix D
(the heart that forced external moduli). This increment adds **Appendix E — the grammar hierarchy**, a new
applied volume that finds the tissue-level and organ-level (γ, A4) the cell-level reading had missed. It is
**add-only**: no chapter, appendix, number, grade, equation, table, or DOI of v1.13 or any prior appendix
is altered. One new section is added (the site goes from 20 to **21** sections), the
contents/sitemap/meta/gate are extended, and Appendix D gains a forward nav link.

## The question

Everything the corpus has read is the **cell** level. The material **γ** and the **A4** coordinate are
both computed from the base sequence — the chemistry of adjacent base pairs, the bottom blueprint. Its
limit showed at the heart: Appendix A found γ orthogonal to the heart's developmental arrangement, and
Appendix D had to import measured cardiac moduli. The instruction driving this increment names the gap
exactly: *is there really no γ or A4 at the tissue level, or have we just failed to see it? If the
blueprint is precise, the heart's exact form cannot come from cells alone — there must be a tissue-to-tissue
arrangement map. If the A4's material began as ions/chemistry, what is the upper blueprint's material?*

## The hierarchy of grammars (the same operator, lifted up the tower)

The cell's level-and-shape operation is not specific to stacking energy; it reads **any** signal as a
LEVEL and a SHAPE. Lifted up three grammatical levels:

| grammar | linguistic level | signal | reads | (γ, A4) |
|---|---|---|---|---|
| **G1 material** (cell) | phonology — substance of the letters | nearest-neighbour stacking ΔG (SantaLucia 1998) | cell stiffness | (γ₁, A4₁) — *what the corpus read* |
| **G2 regulatory** (tissue) | syntax — how control words are arranged | cardiac TF binding grammar (GATA, NKX2-5, MEF2, TBX5, HAND) | **which tissue** | (γ₂, A4₂) — **the missed upper A4** |
| **G3 architecture** (organ) | discourse — how the text is laid out | layout of the regulatory hotspots | the spatial **arrangement map** | (γ₃, A4₃) — **the 배치도** |

The upper "material" is answered directly: **not** ions/chemistry but **syntax** (the arrangement of
regulatory words), then **architecture** (the layout). The same (γ, A4) grammar on a higher-order signal.

## Three results, on real human promoters (not circular)

Two cardiac promoters (NPPA, TNNT2) and one housekeeping control (GAPDH), real GRCh38 sequences fetched
from NCBI and embedded for offline reproduction:

> **1 — Tissue identity is readable from the regulatory grammar.** G2 separates cardiac from housekeeping
> by **~14×** (cardiac mean 14.0 cardiac-TF sites vs control 1.0), while the material γ₁ does **not** carry
> that identity (−1.459 / −1.452 / −1.569, ~7% spread). A tissue-level blueprint exists and is
> sequence-readable. `[L]`
>
> **2 — The upper grammar is information *above* the material.** A dinucleotide-preserving shuffle
> (Altschul-Erickson) preserves the material LEVEL γ₁ **exactly** (−1.459299 → −1.459299 — γ₁ is the mean
> of dimer ΔG, and dimer counts are preserved) yet collapses the cardiac grammar (17 → 4, **76% lost**). So
> **none** of the tissue identity is at the material level. `[V]`
>
> **3 — The levels are orthogonal.** corr(G1, G2) ≈ −0.04, R² ≈ 0.002 — distinct projections of the
> blueprint, not the same signal twice. And the SHAPE projection is the **identical robust-z operator** at
> every level (scale/shift-invariant to machine epsilon). `[V]`

## The heart resolution

Appendix D imported measured cardiac moduli because it read the cell-level **material**, orthogonal to the
arrangement. The arrangement lives **one grammar level up** — the cardiac TF syntax — and is
**sequence-readable**. The blueprint had it; the corpus had read the wrong level. What each grammar
supplies to the heart: G1 → the **cell's** stiffness (blind to identity); G2 → **which tissue** (cardiac
identity); G3 → the spatial **layout** (배치도). **External-data reliance reduced:** tissue identity and
the arrangement signal become sequence reads; absolute kPa **magnitudes** (Appendix D) and **functional**
phenotype remain measured.

## What is honestly NOT claimed (three open obstacles)

`completion.complete = False`. The upper grammar is **found and formalized** — tissue identity
sequence-readable `[L]`, above the material `[V]`, orthogonal `[V]`, same operator at every level `[V]`. It
is **not** yet functionally validated. Three channels remain **[O]**: (1) **functional validation** that
A4₂ predicts measured cardiac enhancer **activity** (VISTA/ATAC/MPRA) with a pre-registered rank test and
shuffle control; (2) the **real 3D arrangement map** (Hi-C/Micro-C or Hox-style colinear spatial TF map);
(3) **absolute kPa magnitudes** (the measured inputs of Appendix D, not superseded). The upper blueprint is
read; its quantitative validation is the next step.

## What changed (all add-only)

New reproduction package `repro/dna/ax-e-grammar-hierarchy/`:

- `grammar/` — 9 modules + package init: `lock` (NN parameters, cardiac TF consensus motifs, 3 REAL
  promoter sequences with accession+coords, shuffle seed; **zero inline magic numbers**), `seqtools`
  (`robust_z` — the A4 operator, identical at every level; `revcomp`; the Altschul-Erickson
  dinucleotide-preserving shuffle), `material` (G1 stacking ΔG → γ₁, A4₁), `regulatory` (G2 cardiac TF
  syntax → γ₂, A4₂), `architecture` (G3 element layout → γ₃, A4₃), `hierarchy` (the three results + the
  same-operator proof), `heart` (the resolution; reliance reduced), `grading` (the one place precision ≠
  accuracy), `interpreter` (`interpret_grammar_hierarchy()` ⊕ `reading_hash` 2×SHA-256), `gate`
  (fail-closed `E1..E9`; `python3 -m grammar.gate`).
- `param_db.json` — NN stacking parameters, cardiac TF consensus motifs (JASPAR + cardiac-GRN literature),
  the three real human promoter sequences (each with accession, coordinates, provenance), shuffle seed.
- `run.py` → `expected/*.json` + `RESULT.txt` (deterministic; 2×SHA-256).
- `README.md`, `LEDGER.md`.

New HTML section `docs/dna/ax-e-grammar-hierarchy/index.html` (VP-SPEC v1.8, answer-first, prev → Appendix
D). Site wiring extended: `_meta.json` appendix **E** row (chapters 16 + appendices 5 = 21); `sitemap.xml`
AX-E URL (hub + 21 = 22 `<loc>`); hub `index.html` TOC `<li class="apx">`, JSON-LD `hasPart`, see-also
cross-link, overview count ("four" → "five" applied appendices); Appendix D forward nav `Appendix E →`;
`gate_multipage.py` section/hub-link count `20 → 21`.

## Verification

- `python3 -m grammar.gate` → **PASS 9/9** (`E1` same operator all levels · `E2` tissue identity readable
  from G2 not G1 · `E3` upper grammar above material via dinuc shuffle · `E4` levels orthogonal · `E5`
  three levels populated · `E6` no magic · `E7` non-fit · `E8` determinism · `E9` honest grades);
  `completion.complete = False`.
- `python3 run.py` → deterministic; reference reading hash `4e29df39b95c16ea`; gate `sha=49763d1e3abaf0b8`;
  byte-identical across runs.
- `python3 gate_multipage.py` → **PASS 241, WARN 1, FAIL 0** (the single WARN is the pre-existing
  source-monolith diff, warn-only).

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견. 문법.*
*The bottom blueprint was the material (cell). The upper blueprints — tissue syntax and organ architecture*
*— are real, sequence-readable, and were missing. That is why the heart needed external moduli.*
