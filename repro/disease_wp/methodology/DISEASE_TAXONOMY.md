# DISEASE_TAXONOMY — classification axes  *(DRAFT — refined in Phase R1)*

Each in-scope entity is placed on **three orthogonal axes**: *inheritance*, *molecular mechanism*, and
*organ system*. Keeping them orthogonal prevents the common confusion of mixing "how it's inherited" with
"what the mutation does to the protein."

## Axis 1 — inheritance class

- **Autosomal dominant** — one altered allele suffices.
- **Autosomal recessive** — two altered alleles required.
- **X-linked recessive** — typically affects males; carrier females.
- **X-linked dominant** — affects both sexes; may be male-lethal.
- **Y-linked** — rare; holandric.
- **Mitochondrial (maternal)** — mtDNA, maternal transmission, heteroplasmy threshold effects.
- **Genomic imprinting** — parent-of-origin–dependent expression (e.g., 15q11-q13 disorders).
- **Chromosomal** — aneuploidy (trisomy/monosomy) or structural (deletion, duplication, translocation, inversion).
- **Microdeletion / microduplication (CNV)** — contiguous-gene syndromes.
- **Multifactorial / polygenic** — major-gene contribution on a polygenic + environmental background.
- **Mosaic / somatic** — post-zygotic; tissue-restricted.

## Axis 2 — molecular mechanism (what the variant does)

- **Loss-of-function (LoF)** — null/hypomorphic; reduced or absent product.
- **Haploinsufficiency** — one functional copy is not enough (a dominant LoF mode).
- **Gain-of-function (GoF)** — novel or excessive activity.
- **Dominant-negative** — mutant product poisons the wild-type (relevant for multimeric proteins, e.g., collagen).
- **Dosage / copy-number** — phenotype tracks gene copy number (Layer-2 `φ` in the DNA framework).
- **Repeat expansion** — short-tandem-repeat instability (note: many repeat-expansion diseases are primarily
  neurological and therefore **out of scope** — see `SCOPE.md`; included only when the primary system is systemic).
- **Imprinting / epigenetic** — methylation/expression dysregulation rather than coding change (Layer-1 `γ`
  environment layer in the DNA framework).
- **Splicing** — variants altering splice sites / isoform balance.
- **Trafficking / folding** — misfolded but partially functional product (the target of pharmacologic chaperones).
- **Structural / contiguous-gene** — deletion/duplication of multiple genes.

## Axis 3 — organ system (in-scope set only)

metabolic · lysosomal/peroxisomal (systemic) · connective-tissue/skeletal · hematologic · immunologic ·
renal · hepatic · gastrointestinal · pulmonary/exocrine · endocrine/growth · dermatologic ·
chromosomal/CNV-systemic. (CNS/cardiac/affective features of multi-system entities are cross-referenced, not classified here.)

## Link to the carried emergence engine (developmental subset)

For diseases that perturb a **developmental / morphogenetic** program, R3 may annotate *which engine quantity*
the disease maps to — this connects the disease to a reproducible normal-development baseline in `code/emergence_v2/`:

- altered morphogen diffusion/clearance → shifts `λ = √(D·τ)` (the engine's `[L]`-grounded length band);
- altered gene dosage → shifts Layer-2 `φ` (quantity);
- altered switch threshold → shifts the `spinodal(γ) = 2(γ/3)^1.5` onset (the engine's `[V]` switch).

This is an *annotation*, not a fit: the engine never reads disease data, exactly as its NON-FIT invariant requires.

## Index columns produced (Phase R1)

`entity · omim_id · medgen_cui · gene(s) · inheritance_class · mechanism_class · organ_system · in_scope ·
exclusion_reason(if any) · provenance(db:accession:date)`
