# MERGE CHECKLIST — DNA v1.18.1 → vp-site (build_site/)

Date 2026-06-25 · paper_id `dna` · governed by VP-SPEC v1.9. Every box below was executed and verified.
`[x]` = verified pass · `[!]` = deferred to a build/registry session (with reason).

## A. Replacement (in-place upgrade, not append)
- [x] Old `docs/dna/` (18 pages) removed; v1.18.1 `docs/dna/` (29 pages) put in its place.
- [x] 29 pages on disk = hub + 16 sections + 12 appendices (ax-a … ax-l). 11 new appendix pages present.
- [x] Volume was **replaced**, not duplicated — no stale/duplicate DNA tree anywhere in the package.
- [x] `_decl.json` preserved (source omitted it; shared-infra surface unchanged by the upgrade).

## B. Assets & link integrity (C2 / C4)
- [x] All 29 DNA pages reference `/dna/assets/css/site.css` (base site's per-volume convention).
- [x] `docs/dna/assets/css/site.css` present and resolvable (byte-identical to source CSS).
- [x] Dangling font preload `/assets/fonts/text.woff2` (font ships in neither package) removed from all 29.
- [x] **Zero dangling shared-asset (`/assets/…`) references** remain in `docs/dna/`.
- [x] Internal `/dna/{slug}/` links: 29 distinct targets, **all resolve** (0 orphans).
- [x] Cross-site links into `/dna/` from every other volume: **all resolve** (old slugs preserved, only additions made).
- [x] Hub `index.html` lists all 28 section pages (0 orphan chapters).

## C. Canonical / C2 (HTML is the single canonical; no TeX sources)
- [x] No `*.tex`, `*.eq_list.*`, or `txt/` body sources under `docs/dna/`.
- [x] Each page: exactly one `<h1>`, an answer-first `<p class="answer">`, prev/next nav present.

## D. Word-count / manifest regeneration (C1) — see MERGE_NOTES §2
- [x] Problem identified: source manifest stopped at appendix B (10 rows short); `_meta` `words=null` for B–F;
      manifest↔`_meta` disagreements; mixed counting methods (no single stored algorithm).
- [x] Entire `words`+`tables` index **regenerated uniformly** under the VP-SPEC §8 body-prose rule, in both
      `_meta.json` and `manifest/dna.csv` (deterministic, reproducible — rule + code in MERGE_NOTES §2).
- [x] Previously-blank counts filled: ax-b 958, ax-c 1245, ax-d 1438, ax-e 1478, ax-f 1443.
- [x] Whole-`<main>` outliers corrected onto the rule: ax-g 1761→782, ax-k 2534→965.
- [x] manifest = **28 rows, 0 blank** word counts; manifest ↔ `_meta` **0 mismatches**.
- [x] Totals recomputed and verified equal to the section sums: `words`=21016, `tables`=8.
- [!] `_meta` `eq_inline` for B–F left `null` — inline unicode math is untagged (no in-package deterministic
      counter); informational only, gate-irrelevant.

## E. Reproduction kit (verification layer)
- [x] Section repro for ax-b … ax-l added under `repro/dna/repro/dna/` (26 section dirs total; ax-g is a
      docs-only synthesis page, repro points to ax-l — matches source).
- [x] New CHANGELOGs (v1_14…v1_18_1, ax_b…ax_f) + `INTEGRITY_ATTESTATION_v1_18_1.md` added.
- [x] Base-only kit files preserved: `_research/`, `build_single_file_dna.py`, `build_v1_13_level_shape.py`,
      `FINALIZATION_VPSPEC_v1_8_ABSTRACT_CALIBRATION.md`.

## F. Sitemap (search layer, C4) — explicitly requested
- [x] 11 new DNA URLs (ax-b … ax-l) added at priority 0.7.
- [x] DNA volume `lastmod` refreshed to 2026-06-25 (whole volume re-released).
- [x] Totals: 1579 → **1590** site URLs; DNA 18 → **29** (= hub + 28 disk pages); sitemap is valid XML.
- [x] sitemap DNA set == DNA pages on disk (no in-sitemap-only / on-disk-only discrepancies).

## G. C5 shared-infrastructure — RESTORED (was a silent regression in the v1.18.1 source)
- [x] Detected: the v1.18.1 source pages dropped **all** C5 machine-readable provenance — 73 vp-cards had
      `data-locked` but **0** `data-concept`/`/concepts/#id` links, and **0** `inherits-strip` (the base had them).
- [x] Restored via the author's own idempotent tools (regenerate, don't hand-edit): `tools/retrofit_cards.py`
      (added `data-concept` + `/concepts/#id` to the 93 cards whose `data-locked` resolves via `concepts.json`)
      and `tools/build_strips.py` (hub `inherits-strip`: "Defines: DNA interpretation / Inherits: R19 switch").
- [x] Footprint kept to DNA: the site-wide tools also touched 3 non-DNA hubs (continental-genesis,
      recent-sequence-cascade, concepts) with unverified changes — those were reverted to base; only the 7 DNA
      files differ from the file-merge state.
- [x] **`tools/gate_shared_infra.py dna` → PASS** on every check (decl/registry/manifest + body notation).

## H. Objective gates
- [x] Author DNA gate `repro/dna/gate_multipage.py` on the merged + C5-updated 29 pages (kit-native layout):
      **PASS 318 / WARN 1 / FAIL 0** (WARN = optional source-monolith diff, absent by C2).
      Evidence: `repro/dna/reports/dna-merge-reverify-v1_18_1.gate.json`.
- [x] Site-wide `tools/gate.py`: **22 PASS / 0 WARN / 1 FAIL**. All 32 slug-sets pass (no volume dropped),
      lineage chain valid (14 entries), manifest self-hash recomputes, sitemap bijection 1590, all links resolve.

## I. Registry close-out (DNA fully closed; one residual is pre-existing + tool-blocked)
- [x] `registry/vp.manifest.json` dna row: `pages` 18→**29**; `content_sha256`+`repro_sha256` recomputed via the
      tool's own `dir_content_hash`. `dna` is now **out** of gate.py's drift list; `repro_sha256` 32/32.
- [x] `registry/lineage.jsonl`: chain **continued** (entry 14, parent→this verified by gate.py self-hash check).
      `tools/master.json` dna `pages` → 29 (source consistency).
- [!] The lone site-gate FAIL — `content_sha256` drift on **29 other volumes** — is **pre-existing in the base**
      (gate.py on the pre-merge backup shows the same drift for 30 volumes incl. dna; after this merge: 29, dna
      removed). NOT caused by this merge. Clean fix is blocked → see `TOOLBUG_make_manifest_stale_order.md`.
- [!] `tools/make_manifest.py` is **stale** (ORDER/REL missing continental-genesis + recent-sequence-cascade);
      running it regresses 32→30 volumes. This blocks the canonical full-registry regen (incl. the 29-volume
      hash refresh and any `grades` aggregate update). Reported, not fixed (tool edits need approval, VP-SPEC §1).
- [!] `grades` aggregate (manifest/`_decl`) left as-is: the new appendices use `[L]` "locked" (88 body tokens),
      a first-class grade in the framework's own vocabulary (`honest-grading[F/V/L/O]`) that the `grades` **dict**
      schema `{forced,verified,open,hypothesis}` has no slot for. Needs an author schema decision. `_decl`↔manifest
      remain mutually consistent, so `gate_shared_infra` passes.

---

### Package facts
- Returned artifact: `build_site/` (the base, with the DNA upgrade folded in). One zip, no fragmentation.
- DNA pages 29 · appendices 12 · manifest rows 28 · DNA C5 gate PASS · site gate 22/1 (the 1 pre-existing).
- Home `index.html` and `llms.txt` unchanged (they link only the `/dna/` hub; DOI unchanged).
- New top-level docs: `MERGE_NOTES_…`, `MERGE_CHECKLIST_…`, `TOOLBUG_make_manifest_stale_order.md`.
