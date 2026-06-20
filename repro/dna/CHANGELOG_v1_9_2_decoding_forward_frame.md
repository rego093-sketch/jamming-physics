# CHANGELOG — v1.9.2 · Decoding-forward frame (Step 1 of the reframe)

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
**Scope of this increment:** editable surface only (head + page-level answer/abstract + claim-strip + _meta card).
Body **unchanged** — all 14 `<section>` blocks are byte-identical to v1.9.1; body word count invariant (gate-style count 6569, Δ0); `_meta.totals` unchanged (5471 words, 13 chapters, 6 tables).

## Why (the under-reporting fix, now at the level of the thesis)
v1.9.1 led with a *negative* headline ("difference is **not** in the readable material") and framed the
single largest result — that DNA's readable layer can be read completely and mechanically from sequence —
as if it were a limitation. This increment **flips the frame**: the completed reading and *what it reads*
lead; the difference-result is demoted to a corollary; the body-growing emergence work reads as **evidence**.
This is Step 1 (frame + front matter) of the staged reframe in `WORK_HANDOVER_dna_whitepaper_reframe.md`.

## The guardrail (NON-NEGOTIABLE — held on every new sentence)
"Complete / closed / finished" **never** appears without its scope welded in the same breath:
*complete = the **readable layer** (γ + A4 coordinate grammar + R19 switch state + CpG handles) is fully
specified and closed; readability ends at a **sharp, enumerated boundary** — size, sign, dosage, timing are
**runtime**, never asserted.* Automated audit: 8 completeness triggers across title / meta / answer /
abstract / JSON-LD / _meta, **all** with a scope token (readable · boundary · runtime · sharp) within ~10 words. PASS.

## What changed (8 surface edits)
1. `<title>` — keeps the **locked** formal title (registry §2 + DOI deposit) as the citation anchor and adds a
   decoding-forward, paradigm-unique phrase: *"A Deterministic Two-Layer Interpretation of DNA — Reading Any
   Locus from Sequence | 4D DNA Blueprint."*
2. `<meta name="description">` — rewritten conclusion-first, decoding-forward, scope-welded, **160 chars** (gate 80–160).
3. JSON-LD `ScholarlyArticle` — `version` 1.9 → 1.9.2; added a scoped `description`; enriched `knowsAbout`
   with paradigm-specific + decoding-forward terms (reading DNA from sequence · deterministic DNA interpretation ·
   A4 coordinate grammar · R19 double-well switch · anchor-relative helical phase · readable layer of DNA · …).
4. `<p class="answer">` (page) — re-ordered **DECODING → BOUNDARY → difference → evidence**; scope welded.
5. `<p class="abstract">` (page) — the new flagship abstract in the same order; every number grounded in the body
   (seed=7 · human_SOX2 γ=1.287315 · corr(γ,GC)=0.998 · CV 0.1–2% · 5.8% · γ^1.5 · CpG 11–179 · heart ρ=+0.071, p=0.882).
6. page `.claim-strip` version → v1.9.2.
7. `<footer>` version → v1.9.2.
8. `docs/dna/_meta.json` — homepage card `abstract` re-framed decoding-forward (76 words, scope-welded); `version` → 1.9.2.

## Verification (VP-SPEC v1.8)
- **Anti-작문**: every numeric token in the new front matter is present in the body — PASS (no invented number).
- **Body invariance**: 14 `<section>` blocks byte-identical; body word count Δ0; `_meta.totals` unchanged.
- **C4 retrieval-readiness**: answer-first preserved; JSON-LD (ScholarlyArticle + BreadcrumbList) parses; in-page anchors 0 broken; h1 exactly 1 (= locked formal title); file 84 KB (< 300 KB).
- **Source integrity (engine)**: `expected_sha256.json` re-checked over **87 governed files → drift 0**; frozen gate reports all PASS (appendixA 16/16, ch13, ch14 guards, integration, phase2).

## NOT done in this increment (next, pending author sign-off)
The **body restructure** (Parts I–V: *How to read a locus* / *The DNA Dictionary* / *What the reading returns* /
*The boundary is sharp* / *The reading is real*) adds and reorganizes body content and is therefore a **new
whitepaper version (v1.10 / v14)**, not a surface edit. Per the handover, the title and scope-wording decisions
shape those chapters, so they are held for author sign-off (see accompanying report).
