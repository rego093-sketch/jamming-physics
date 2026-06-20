# Exhaustive universality ledger — cross-kingdom γ / M / E  ·  the validity gray zone, mapped

> Every cross-kingdom universality question is graded. **"No gray zone" means the reading's
> domain of validity is mapped — not that γ is magically universal (the test shows precisely
> where it is not).** Grades: **[F]** read & reproduced bit-for-bit · **[V]** measured/reproduced
> in-package · **[L]** peer-reviewed (cited) · **[O]** open-empirical, naming the closing dataset
> · **[B]** category boundary.

**Totals:** 16 questions — **12 [F] · 0 [V] · 1 [L] · 3 [O] · 0 [B]**.  Positively evidenced (F/V/L) = **13/16**. Ungraded = **0**.

Regenerate: `python3 repro/dna/11-cross-kingdom-stress-test/run.py`.

## The measured reads (12 organisms, 120 kb genomic DNA each, recomputed in-package)

| organism | clade | GC% | γ | corr(γ,GC) | CpG O/E | CHG O/E | helix pctl | CpG-meth |
|---|---|---:|---:|---:|---:|---:|---:|---|
| human | Animal/Mammal | 37.2 | 1.2584 | 0.993 | 0.129 | 1.24 | 94 | CG |
| mouse | Animal/Mammal | 42.5 | 1.3145 | 0.990 | 0.182 | 1.30 | 100 | CG |
| chicken | Animal/Bird | 42.7 | 1.3240 | 0.996 | 0.235 | 1.50 | 90 | CG |
| frog | Animal/Amphibian | 39.5 | 1.2892 | 0.986 | 0.249 | 1.35 | 96 | CG |
| zebrafish | Animal/Fish | 34.1 | 1.2323 | 0.985 | 0.418 | 1.44 | 100 | CG |
| fly | Animal/Insect | 45.7 | 1.3701 | 0.995 | 0.954 | 1.10 | 100 | none |
| worm | Animal/Nematode | 35.4 | 1.2583 | 0.988 | 0.967 | 1.14 | 97 | none |
| arabidopsis | Plant/Dicot | 33.8 | 1.2291 | 0.994 | 0.771 | 0.85 | 91 | CG+CHG+CHH |
| rice | Plant/Monocot | 44.4 | 1.3463 | 0.998 | 0.720 | 0.94 | 93 | CG+CHG+CHH |
| maize | Plant/Monocot | 43.7 | 1.3362 | 0.995 | 0.651 | 0.91 | 75 | CG+CHG+CHH |
| yeast | Fungus/Ascomycete | 38.2 | 1.2798 | 0.991 | 0.793 | 1.07 | 69 | none |
| plasmodium | Protist/Apicomplexan | 20.4 | 1.0797 | 0.994 | 0.705 | 0.88 | 74 | trace |

## The three verdicts

- **U1 — γ ≈ GC universally [F].** corr(γ,GC) ranges 0.985–0.998 across all 12 kingdoms (mean 0.992); holds at 20% GC (*Plasmodium*). γ is a GC-restatement + dinucleotide order, not an independent material axis.
- **U2 — γ is NOT taxon-invariant [F].** Bulk-genome γ CV = **5.8%** (range 0.290); histone-H4 ortholog (same protein) γ CV = **8.3%**, corr(γ,GC)=0.998. Both ≫ the abstract's 0.1–2%. Honest restatement: *γ is taxon-invariant only among iso-GC species; cross-kingdom, read γ relative to GC.* The deeper thesis survives (γ adds no axis beyond GC).
- **U3 — CpG O/E is a methylation substrate only where the clade methylates [F]+[L].** Methylating clades: CpG O/E median 0.33 (depleted); non-methylating (fly/worm/yeast): 0.95 (≈1). Plants additionally deplete CHG (0.85–0.94) vs vertebrates (1.24–1.50). The universal M-layer reads the clade's CONTEXT (CG vs CG+CHG+CHH).

## The graded ledger

### U1 — γ as GC-restatement

| quantity | grade | basis / obstacle |
|---|:---:|---|
| corr(gamma,GC) per genome (12 kingdoms) | **[F]** | windowed, recomputed; min 0.984 |
| gamma is a GC-restatement (not independent material axis) | **[F]** | corr>=0.97 universal -> gamma carries GC's information, no taxon-specific extra |

### U2 — γ taxon-invariance (the stressed claim)

| quantity | grade | basis / obstacle |
|---|:---:|---|
| bulk-genome gamma CV across 12 kingdoms | **[F]** | 5.8%, recomputed |
| histone-H4 ortholog gamma CV (same protein) | **[F]** | 8.3%; clean ortholog set |
| H4 gamma-spread is GC-driven (codon usage) | **[F]** | corr 1.00 |
| abstract '0.1-2% CV' validity domain | **[F]** | holds among iso-GC species; FALSIFIED cross-kingdom -> restated, not silent |
| absolute per-species master-switch gamma catalog (OTX/ZRS across phyla) | **[O]** | would pin the iso-GC vs cross-GC crossover precisely; needs a curated ortholog-promoter panel per phylum (NCBI gene + assembly coords) -- a refinement of the mapped boundary |

### U3 — methylation-substrate universality

| quantity | grade | basis / obstacle |
|---|:---:|---|
| CpG O/E by clade (12 organisms) | **[F]** | windowed median, recomputed |
| CpG depletion separates methylating vs non-methylating | **[F]** | clean gap; max_yes<min_no |
| DNA-methylation machinery per clade (the predictor) | **[L]** | peer-reviewed: vert/plant methylate, fly/worm/yeast do not (refs in METH) |
| plant CHG (non-CG) depletion | **[F]** | plant CHG<<vertebrate CHG; sequence-read |
| context-aware substrate generalization (CG vs CG+CHG+CHH) | **[F]** | the M-layer's universal form; CpG-only is the mammal special case |
| absolute per-context methylation beta (5mCG/5mCHG/5mCHH) per tissue | **[O]** | the depletion gives the EVOLUTIONARY substrate; live beta needs WGBS per context (plant CX-report / vertebrate WGBS) -- the same Layer-2 [O] as sec 9, now cross-kingdom |

### E — helical signal universality

| quantity | grade | basis / obstacle |
|---|:---:|---|
| helical WW-ACF(10-11) percentile per genome | **[F]** | shuffle-controlled, recomputed |
| helical signal elevated above shuffle in all 12 but NON-UNIFORM in strength | **[F]** | strong in animals (>=90th), weak/borderline yeast+Plasmodium -- matches Segal/Trifonov; the non-uniformity is the honest finding, not forced to a threshold |
| absolute in-vivo nucleosome occupancy per genome | **[O]** | sequence gives the rotational TENDENCY; occupancy needs MNase-seq per organism -- the same E1 [O] as sec 10, now shown to be a cross-kingdom requirement |

## The mechanistic payoff

The stress test does more than validate — it **unifies the material layer and the methylation
layer**. γ is a GC-restatement (U1); the deviation of GC from neutrality is **CpG depletion**;
and CpG depletion **is** the evolutionary fingerprint of CpG methylation (U3). So the composition
the framework reads as γ and the methylation substrate it reads as CpG O/E are **two projections
of one history** — the genome's methylation regime, written into its dinucleotide statistics and
readable from sequence alone. Vertebrates write it in CG; plants in CG+CHG+CHH; fly/worm/yeast
not at all — and the reading now reports each correctly.

## What "no gray zone" means

13/16 questions are positively evidenced [F]/[V]/[L]. The 3 [O] items are dataset-named refinements (per-phylum master-switch panel; per-context WGBS β; MNase-seq occupancy) of an already-mapped boundary — none silent. The reading's domain of validity is now explicit: **γ tracks GC everywhere; it is invariant only among iso-GC genomes;
the methylation substrate must be read in the clade's context.** Nothing is left unaddressed.