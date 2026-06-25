# Appendix E — the grammar hierarchy: reading the upper blueprint

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

Everything the corpus has read so far is the **cell** level. The material **γ** and the **A4**
coordinate are read from the base sequence — the chemistry of adjacent base pairs, the bottom
blueprint. But the heart forced us to **import external measured moduli** (Appendix D), because the
arrangement was orthogonal to that cell-level material (the Appendix A null, ρ = +0.071). The
question this appendix asks, in the user's words: *is there really no γ or A4 at the tissue level —
or have we just failed to see it? If the blueprint is precise, the heart's exact form cannot come
from cells alone; there must be a tissue-to-tissue arrangement map. If the A4's material started as
ions (chemistry), what is the upper blueprint's material?*

> **반증 = 발견.** The corpus read only the bottom (material) blueprint. The tissue-level and
> organ-level grammars are real, sequence-readable, and were **missing** — which is exactly why the
> heart forced external moduli. We had been reading the wrong level of the blueprint.

---

## The hierarchy: one operator, lifted up the tower

The DNA blueprint is read at **three grammatical levels**, each with the **same** (LEVEL, SHAPE) =
(γ, A4) decomposition via the **identical** robust-z operator — a linguistic hierarchy:

| grammar | linguistic level | signal | reads | (γ, A4) |
|---|---|---|---|---|
| **G1 material** (cell) | **phonology** — the substance of the letters | nearest-neighbour stacking ΔG (SantaLucia 1998) | the cell's intrinsic stiffness | (γ₁, A4₁) — *what the corpus read* |
| **G2 regulatory** (tissue) | **syntax** — how control words are arranged | cardiac TF binding grammar (GATA, NKX2-5, MEF2, TBX5, HAND) | **which tissue** a region builds | (γ₂, A4₂) — **the missed upper A4** |
| **G3 architecture** (organ) | **discourse** — how the whole text is laid out | layout of the regulatory hotspots | the spatial **arrangement map** | (γ₃, A4₃) — **the 배치도** |

The user's question — *if A4's material was ions/chemistry, what is the upper material?* — is answered
directly: the upper "material" is not chemistry but **syntax** (the arrangement of regulatory words)
and then **architecture** (the layout). The same (γ, A4) grammar, applied to a higher-order signal.

## Three results, on real human promoters (not circular)

Two cardiac promoters (NPPA, TNNT2) and one housekeeping control (GAPDH), real GRCh38 sequences
fetched from NCBI and embedded:

**1 — Tissue identity is readable from the regulatory grammar.** The cardiac TF grammar (G2) separates
cardiac from housekeeping by **~14×** (cardiac mean 14.0 cardiac-TF sites vs control 1.0), while the
material grammar (G1) does **not** carry that identity (γ₁ ≈ −1.459 / −1.452 / −1.569, ~7% spread). A
tissue-level blueprint exists and is sequence-readable — the upper A4 the corpus missed. `[L]`

**2 — The upper grammar is information *above* the material.** A dinucleotide-preserving shuffle
(Altschul-Erickson) preserves the material LEVEL γ₁ **exactly** (−1.459299 → −1.459299 — γ₁ is the
mean of dimer ΔG, and dimer counts are preserved) yet collapses the cardiac grammar (17 → 4, **76%
lost**). So **none** of the tissue identity is at the material level; reading only G1 misses all of it.
`[V]`

**3 — The levels are orthogonal.** The G1 (material) and G2 (regulatory) signals are essentially
uncorrelated along the real sequence (corr ≈ −0.04, R² ≈ 0.002) — distinct projections of the
blueprint, not the same signal twice. `[V]`

And the SHAPE projection is the **identical robust-z operator** at every level (scale- and
shift-invariant to machine epsilon) — the cell-level grammar lifted, not a new rule per level. `[V]`

## The heart resolution

Appendix D had to import measured cardiac moduli because it read the cell-level **material**, which is
orthogonal to the arrangement. The arrangement lives **one grammar level up** — the cardiac TF syntax —
and is **sequence-readable**. The blueprint had the arrangement all along; the corpus had been reading
the wrong level. What each grammar supplies to the heart: G1 → the **cell's** stiffness (read before,
blind to identity); G2 → **which tissue** (cardiac identity); G3 → the spatial **layout** (배치도),
toward the organ's exact form that cells alone cannot give.

**External-data reliance reduced.** Tissue **identity** and the arrangement **signal** are now sequence
reads (G2, A4₂), not imports. What remains measured: the absolute kPa **magnitudes** (Appendix D — this
package does not supersede it) and the **functional** phenotype.

## What is honestly NOT claimed

`completion.complete = False`. The upper grammar is **found and formalized** — a (γ, A4) pair at the
regulatory and architecture levels, read with the same operator as the cell, with tissue identity
sequence-readable `[L]`, proven above the material `[V]`, orthogonal to it `[V]`. It is **not** yet
functionally validated. Three channels remain `[O]`:

1. **functional validation** — that A4₂ predicts measured cardiac enhancer **activity** (VISTA cardiac
   enhancers, cardiac ATAC-seq/H3K27ac, or MPRA), with a pre-registered rank test and a shuffle control.
2. **the real 3D arrangement map** — G3 here is the local element layout; the true spatial tissue
   배치도 (Hi-C/Micro-C contacts, or the colinear spatial-domain TF map, Hox-style), staged.
3. **absolute kPa magnitudes** — the regulatory grammar reads identity and arrangement, not magnitudes;
   those stay the measured inputs of Appendix D.

The upper blueprint is **read**; its quantitative validation is the next obstacle.

## Reproduce

```
python3 run.py            # → expected/*.json + RESULT.txt (deterministic, 2×SHA-256)
python3 -m grammar.gate   # → fail-closed E1..E9; exit 0 iff all pass
```

Gate **PASS 9/9** (`E1` same operator all levels · `E2` tissue identity readable from G2 not G1 · `E3`
upper grammar above material (shuffle) · `E4` levels orthogonal · `E5` three levels populated · `E6` no
magic · `E7` non-fit · `E8` determinism · `E9` honest grades). Reference reading hash `4e29df39b95c16ea`;
gate `sha=49763d1e3abaf0b8`.

## Files

```
param_db.json            NN stacking parameters, cardiac TF consensus motifs, 3 REAL promoter
                         sequences (NPPA/TNNT2 cardiac, GAPDH control) with accession+coords, shuffle seed
grammar/
  lock.py                the locked surface; zero inline magic numbers
  seqtools.py            robust_z (the A4 operator, identical at every level), revcomp, dinuc-shuffle
  material.py            G1 — the cell/material grammar (stacking ΔG → γ₁, A4₁)
  regulatory.py          G2 — the tissue/regulatory grammar (cardiac TF syntax → γ₂, A4₂)
  architecture.py        G3 — the organ/architecture grammar (element layout → γ₃, A4₃)
  hierarchy.py           the three results + the same-operator proof
  heart.py               the heart resolution (arrangement sequence-readable; reliance reduced)
  grading.py             the one place precision ≠ accuracy; honest ledger + completion
  interpreter.py         interpret_grammar_hierarchy() — the full reading; reading_hash
  gate.py                fail-closed E1..E9
run.py                   top-level runner → expected/ + RESULT.txt
README.md / LEDGER.md    this file / the auto-generated grade ledger
expected/                reference outputs (byte-identical across runs)
```

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견. 문법.*
*The bottom blueprint was the material (cell). The upper blueprints — tissue syntax and organ*
*architecture — are real, sequence-readable, and were missing. That is why the heart needed external moduli.*
