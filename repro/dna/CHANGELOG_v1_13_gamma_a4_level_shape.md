# CHANGELOG — v1.13 · γ↔A4 stated as LEVEL vs SHAPE (clarification + spec fold-in)

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
Builds on v1.12 (multi-page canonical). This increment makes the relationship between **γ** and the
**A4 coordinate** impossible to misread — clear on first contact — and folds in a standalone
specification for it. **No body number, grade, equation, table, or DOI changes.** It is append-only:
clarifying sentences are added, one abstract sentence is replaced by a strictly sharper one carrying
the same numbers, and one irreversible tombstone is added to the §8 retired register.

## Why

A reader (or a later session) can easily slide into the misconception that **γ is a special case of the
A4 coordinate — "γ ⊂ A4."** v1.12 stated γ and A4 as "two reads united into one engine" (§13) without
naming their relationship, which left that door open. The relationship is in fact exact and simple, and
was verified independently in `vp_session_gamma_a4_verified` (4 phases, 2×SHA-256,
`prereg.sha256 ff04aa7b8b025bd19c6f06c7da253d66952acbe22a3f6804ade5b6cd5fac3901`), with the mechanism
visible in the shipped engine itself (`repro/dna/_verify/engine/key_pipeline_full.py::robust_z`).

## The relationship, stated once (this version states it everywhere γ and A4 meet)

> **One stiffness signal. γ is its LEVEL (window-mean). A4 is its SHAPE (the same signal with that mean
> removed — shells, anchors, loops, anchor-relative phase). The A4 pipeline's `robust_z` subtracts the
> per-locus median, which is exactly the level γ is, so A4 = "the signal minus γ" — and "γ ⊂ A4" is not
> wrong but impossible. They are two orthogonal projections of one field; neither contains the other.**

Verified: same field (per-locus ρ = 0.939; identical coarse anchors, **0.0 bp offset across all 37
loci**) yet A4 carries **none of γ** (max |corr(axis, γ)| = **0.327**). Shared input ≠ nested output.

## What changed (edits, all append-only, applied by code)

The edits are applied by `build_v1_13_level_shape.py`, a deterministic patch that verifies each source
anchor fail-closed (exact-string, expected-count, abort-without-writing on mismatch) — no silent no-op.

1. **§13 abstract opening** — replaced the "split the read in two" sentences with the level/shape
   statement (same numbers; adds the `robust_z` orthogonality reason).
2. **§13 "The coordinate grammar, restored"** — one sentence added: the coordinate is the mean-removed
   view of the same signal γ averages (`robust_z` deletes the level = γ).
3. **§I Step 2** — a lead sentence "the relationship in one line" added before the four-part coordinate
   paragraph; plus the reusable card (below).
4. **§2 "A scale, not a locus"** — one clause added: γ is the *level* of the stiffness signal, position
   (shell/anchor/loop) is the mean-removed A4 read of §13.
5. **§8 closure** — one clause added: the four readable channels are not nested; γ and A4 are level and
   shape of one field.
6. **§8 retired register** — new irreversible tombstone: **"γ ⊂ A4" / "γ is one of the A4 coordinates"
   / "γ is a coarse A4"** is retired as an **empirically falsified** framing (Phase 1+4 same field;
   Phase 2 no γ-redundant axis), must not revive under any name.
7. **Reusable vp-card "γ and A4 are level vs shape of one field"** — added to §I and §13 (self-contained,
   graded, paste-identical).
8. **Retrieval surfaces** — `docs/llms.txt` gains one canonical read (γ=LEVEL / A4=SHAPE, neither nested);
   `_meta.json` §13 `one_liner` re-led with the relationship; `version` 1.12 → 1.13.
9. **Version chrome** — footer "(v1.12)" → "(v1.13)" on all 18 pages; hub claim-strip "· v1.12" → "· v1.13";
   `sitemap.xml` `lastmod` 2026-06-17 → 2026-06-21.

## New files

- **`GAMMA_VS_A4_LEVEL_SHAPE_SPEC.md`** — the canonical level/shape specification (the "fool-proof"
  explanation + the everyday analogy + the 10-second orthogonality self-check + the drop-in edits +
  the evidence). This is the standing reference the in-page wording is derived from.
- **`build_v1_13_level_shape.py`** — the deterministic, fail-closed patch that produced this version
  from v1.12 (shipped so the upgrade is reproducible and auditable).
- **`reports/dna-v1_13-multipage.gate.json`** — the v1.13 structural gate report.

## Updated record

- `repro/dna/13-unified-deterministic-interpreter/LEDGER_unified.md` — a v1.13 section recording the
  level/shape relationship, its evidence, the edits, and the preserved open item.

## Standing [O] — preserved, and explicitly fenced off

Clarifying the relationship must **not** silently settle the open question it raises:

- **Earned [V]:** the γ-**level** is orthogonal to developmental **timing** (heart ρ = +0.071, p = 0.882).
  A mean is a low-pass filter; the level carries no fine timing.
- **STILL OPEN [O]:** whether the A4-**shape** carries order/timing the level cannot. The one fair test —
  re-running the heart/organ timing test with **25–50 kb windows** so the A4 coordinate has real
  shell/anchor resolution — has **not** been run; the single attempt (Phase 3b) was on degenerate 2501 bp
  promoters < `min_shell_bp` (5000). **"γ-level ⊥ timing" must not be read as "sequence ⊥ timing."**

## Verification (`gate_multipage.py`)

Re-run after the edits: **VERDICT PASS** (per-page structure intact — one `<h1>`, answer-first, valid
JSON-LD, canonical correct, no `#s…` anchors, internal links resolve, size/DOM within budget, prev/next
present; hub orphans 0, `/physics/` link present; robots 7 bots; sitemap URL count = page count;
`llms.txt` < 5 KB; C2 no `.tex`). The completeness diff against the source monolith is the only WARN — the
monolith is not re-bundled in this package; paragraph fidelity is instead guaranteed by the fail-closed,
exact-string patch (every edit adds or sharpens; nothing else is touched). Report:
`reports/dna-v1_13-multipage.gate.json`.

## What is **not** changed (fidelity)

No measured value (γ = 1.287315, ρ = 0.94/0.939, 0.0 bp, 0.327, corr(γ,GC) = 0.998, heart ρ = +0.071 /
p = 0.882, CpG 11–179, …), no grade, no equation, no table, no DOI, and no `repro/` engine, input, or
frozen `expected/` is modified. The reproduction layer is byte-identical to v1.12. Only the editable HTML
surfaces, `llms.txt`, `_meta.json`, `sitemap.xml`, and three new top-level docs are added or sharpened.
