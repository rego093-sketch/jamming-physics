# CHANGELOG — v1.10 · Decoding-forward body restructure (Parts 0–V)

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.9.2 (front-matter frame). This increment **adds and reorganizes body content**, so per the
handover it is a **new whitepaper version**, not a surface edit.

## What this version does
Surfaces the completed reading as the paper's spine. Three **new front chapters** lead; the existing 13
chapters + Appendix A are **kept byte-identical** and re-positioned by a Part-structured table of contents.

### New chapters (added at the front)
- **§0 — The reading, stated plainly** (Part 0). The whole claim in one place, with the closure argument
  welded: *complete = the admissible reading method for the readable layer (γ + A4 coordinate + R19 switch
  state + CpG handles) is fully specified and closed; the boundary is part of the reading; every remaining
  question is Layer-2 calibration or out-of-scope — **no fourth bucket.***  Grade: claim shown via closure (no new number).
- **§I — How to read a locus** (Part I, the new core). The A4 grammar walked **end-to-end on human_SOX2
  (γ = 1.287315)**: ① γ from NN stacking → R19 threshold scale (spinodal 0.5622, barrier 0.4143);
  ② the A4 coordinate (shell, nearest anchor + strength, loops, anchor-relative helical phase), with the
  helical face read as **geometry, not function** (same-face 0.337 vs chance 0.340, z = −0.09); ③ R19
  can-fire vs runtime on/off; ④ the five channels of one read.  Grade: **admissible** (method exposition).
- **§II — The DNA Dictionary** (Part II, **engine-generated**). A lexicon of mechanical reads over **26
  curated loci** (γ 1.264–1.444, **all R19-bistable**), each row emitted by the locked engine, with its own
  fail-closed gate. Makes the boundary visible in one table: **human ZRS γ 1.264 (ON lineage) vs snake
  LMBR1 γ 1.290 (OFF lineage)** read nearly the same γ — γ is blind to on/off. A Dictionary of **reads, not
  traits**.  Grade: **admissible** (mechanical Layer-1 read; STATE/sign/dosage/timing runtime).

### New reproducible artifact
- `repro/dna/15-dna-dictionary/` — `build_dictionary.py` (runs the locked `dna_interpreter` over the 26
  `sequences_v6` loci → `expected/dictionary.json`) + `gate_dictionary.py` + README. **Engine-generated,
  not hand-assigned.** Gate (fail-closed): **determinism** (two builds share one sha256) + **baseline pin**
  (every reported value matches the frozen `regression_baseline.json` to 1e-9 across all 26 loci). The
  engine re-derives **human_SOX2 γ = 1.287315** every run. `gate_dictionary.py → OVERALL: PASS (2/2)`.

### Re-positioning (no body change)
The table of contents now groups the existing chapters under Parts: **III — What the reading returns**
(§1–§7, incl. the difference-result as a corollary), **IV — The boundary is sharp** (§8), **V — The reading
is real / it grows a body** (§9–§13 + Appendix A). The chapter bodies themselves are untouched.

## Governance & verification (VP-SPEC v1.8)
- **★ Guardrail held:** every "complete / closed / finished" claim across title, meta, answer, abstract,
  JSON-LD, the 3 new chapters, and the `_meta` card carries its scope (readable · boundary · runtime ·
  sharp · no-fourth-bucket) within ~10 words. Automated audit over **18 genuine completeness triggers → PASS.**
- **Anti-작문:** every numeric token in the 3 new chapters is grounded in an existing body section, the
  locked engine, or the engine-generated Dictionary — PASS (no invented number).
- **Body preserved:** the 14 existing chapter `<section>` blocks (§1–§13 + Appendix A) are **byte-identical**
  to v1.9.1.
- **Reproducibility:** Dictionary gate PASS (2/2); the morphogenesis appendix's 87-file frozen pin re-checked
  → **drift 0** (only files added, none of the 87 touched); package frozen gate reports still PASS.
- **C4 retrieval-readiness:** answer-first on every new chapter; JSON-LD `hasPart` extended with §0/§I/§II;
  in-page anchors 0 broken; h1 exactly 1; DOM 1101 nodes (< 3000); file 101 KB (< 300 KB). Existing slugs/ids unchanged.
- **Metadata regenerated for the new structure:** `manifest/dna.csv` → 17 rows; `_meta.json` chapters +3,
  totals.words recomputed, version → 1.10. (Per-section word counts were regenerated with a consistent
  method for the restructured document; the original Phase-1 tool is not bundled.)

## Notes / next
- Part IV currently re-positions §8 (the reading mapping its own edges) via the Part-structured TOC; a
  dedicated prose closure section folding `CLOSURE.md` into §8 can follow if desired.
- Part V's "evidence" reading cross-references the neuro emergence paper (DOI 10.5281/zenodo.17979015); a
  one-line in-body cross-link can be added in a future pass.
