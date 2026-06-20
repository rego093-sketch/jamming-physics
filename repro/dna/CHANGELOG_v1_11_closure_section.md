# CHANGELOG — v1.11 · §8 closure section + full re-review

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.10. This increment folds the closure argument into §8 and applies an editorial re-review.
No CLOSURE.md file was available; the closure is reconstructed from quantities verifiable in this package.

## Changes
- **§8 lead reframed** (editable surface): an answer-first block plus a reframed abstract present §8 as the
  reading's boundary — "the boundary is part of the reading, not a gap in it" — rather than as a list of limits.
- **§8 closure section added** ("Closure — why the readable layer's reading is closed"). The argument is
  stated mechanically from package data:
  1. The four readable channels each map to a measured quantity — γ (§2), the A4 coordinate (§13), the R19
     switch state (§I), the CpG handles (§6) — and the **Dictionary (§II)** is the enumerated demonstration
     (26 loci, all R19-bistable, baseline-pinned to 1e-9).
  2. The mapping holds across the tree of life — γ tracks GC in twelve genomes at corr ≥ 0.97 (§11), the
     methylation reader routes vertebrate/plant/insect regimes (§12), the same gene reads at comparable γ
     across species (§II).
  3. What is not readable is enumerated, not hidden — size, sign, dosage, timing are runtime; each open item
     names the measured input that would settle it (Layer-2 calibration); the remainder is out of scope by
     construction (§1). **An item is a readable channel, a calibration with a named input, or out of scope —
     there is no fourth bucket.**
  4. Reproduction is deterministic and read-only (human_SOX2 γ = 1.287315 every run; Dictionary gate PASS;
     87-file applied-volume pin at drift 0).

## Re-review (this pass)
- **Self-deprecation:** whole-document scan returned only technical descriptors ("gene-poor", "CpG-poor",
  "not just a context", "only a subset") — no self-deprecating tone. The closure section is written neutrally
  and mechanically; honest grades (admissible / principle-demonstration / open / null) are retained as required.
- **Guardrail:** full-document audit of every "complete / closed / closure / finished / decoded" trigger.
  All decoding-completeness claims carry scope (readable · boundary · runtime · calibration · no-fourth-bucket)
  within ~10 words. One pre-existing token in §13 ("two accuracy deltas are closed") is a different sense
  (discrepancies resolved, not a completeness claim) and is left unchanged in the byte-identical author body.
- **Anti-작문:** the closure section's numbers (26, 1e-9, corr ≥ 0.97, twelve genomes, γ = 1.287315) are all
  grounded in existing body sections or the engine-generated Dictionary.
- **Body preserved:** §1–§7, §9–§13 and Appendix A remain byte-identical to v1.9.1; only §8 changed (by design).
- **Structure:** sections 17 = manifest 17; JSON-LD valid; in-page anchors 0 broken; h1 = 1; DOM 1112 (< 3000);
  file 104 KB (< 300 KB). `manifest/dna.csv` and `_meta.json` §8 word count + totals updated; version → 1.11.
