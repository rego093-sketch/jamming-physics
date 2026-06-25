# CHANGELOG — v1.18.1 · recover accidentally-dropped, still-referenced provenance files

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

Pure-recovery, add-only point release on top of v1.18 (`…_AX-G_cleaned`). **No `docs/` page, no number,
grade, equation, hash, or DOI is changed.** Three root-level files that v1.18's dead-code pass removed
**without** the reference-severing step it applied to its *intended* removals are restored byte-identical to
their v1.17 source. One genuinely-orphaned v1.8-era file is left removed by design. The site section count
stays 28; the gate, the `ax-l` completion gate, and every per-chapter reproduction gate are unaffected.

## Why this was needed (the diagnostic)

v1.18's documented dead-code pass removed three items **and severed their references first** — the signature of
a deliberate removal:
- `build_v1_13_level_shape.py` → the only machine reference (`gate_multipage.py` build-provenance hash) was
  **repointed to `build_multipage_dna.py`** before deletion.
- `build_single_file_dna.py` → only historical changelog / docstring mentions remained (no live ref).
- `repro/dna/_research/` → zero references anywhere.

Those three removals are correct and are **kept removed**.

Separately, **four root `*.md` files were also dropped, but their references in *retained* artifacts were left
intact** — the signature of a collateral / accidental deletion, not a prepared one. v1.18's changelog does not
list them in its "Removed (proven dead — zero references anywhere)" section, and they fail that section's own
stated criterion. Three of them are still pointed to by files that ship in the package (including the published
HTML), so their absence is a dangling-reference defect:

| dropped file | retained artifact still pointing at it | nature |
|---|---|---|
| `IRREPRODUCIBILITY_LEDGER.md` (root [O] aggregator) | **published** `docs/dna/ax-a-…/index.html` ("The full register is aggregated in IRREPRODUCIBILITY_LEDGER.md"), `repro/dna/09-…/README.md`, `repro/dna/ax-a-…/VERSION`, `repro/dna/_engine/methylation_layer_4d.py`, `reports/dna-ch14-defensive-guards.gate.json`, `CHANGELOG_v1_9_appendix_merge.md` | live, **unreplaced** — no other file aggregates the whole-paper [O] register; consistent with v1.18 (its honest-`[O]` discipline was preserved, not retired) |
| `GAMMA_VS_A4_LEVEL_SHAPE_SPEC.md` (the γ↔A4 level/shape manual) | `repro/dna/13-…/LEDGER_unified.md` ("Full spec: `GAMMA_VS_A4_LEVEL_SHAPE_SPEC.md`"), `CHANGELOG_v1_13_…` | live, **not absorbed** by the new Appendix G / §2 ALGO block (those only *use* `robust_z`; they are not the dedicated "γ ⊂ A4" spec the ledger cites) |
| `FINALIZATION_VPSPEC_v1_8_CLOSEOUT.md` (v1.8 finalization audit) | `repro/dna/ax-a-…/VERSION` ("See FINALIZATION_VPSPEC_v1_8_CLOSEOUT.md for the full audit") | older content, but still the cited target of a shipping provenance record; restoring it repairs that pointer at zero risk |

## Restored (byte-identical to v1.17 source; md5 verified)

- `IRREPRODUCIBILITY_LEDGER.md`
- `GAMMA_VS_A4_LEVEL_SHAPE_SPEC.md`
- `FINALIZATION_VPSPEC_v1_8_CLOSEOUT.md`

## Kept removed by design (honoring v1.18's intent + the user's "some were superseded past content")

- `FINALIZATION_VPSPEC_v1_8_ABSTRACT_CALIBRATION.md` — **zero** references from any retained file (its only
  citation was inside the also-removed `…_CLOSEOUT.md`, which does not point back to it). Restoring the closeout
  re-dangles nothing. This is a genuinely-orphaned v1.8-era session record; its removal is accepted as
  intentional pruning.
- `build_single_file_dna.py`, `build_v1_13_level_shape.py`, `repro/dna/_research/` — v1.18's deliberate,
  reference-severed, gate-verified dead-code pass. Unchanged.

## What v1.18 got right (left untouched here)

- **Appendix G — the grammar space** (`docs/dna/ax-g-the-grammar-space/`) filling the previously-empty G slot;
  the F → G → H nav chain, hub `hasPart`, `_meta.json` (A–L, twelve), `sitemap.xml` (29 `<loc>`), and the
  sanctioned gate section-count bump 27 → 28 are all preserved.
- The prose **confidence reframing** on §0/§2/§9/§13 and Appendices A/D/F/I — verified add-only: no measured
  value, Spearman, γ, hash, grade token, or DOI was altered (heart null `+0.071 / p = 0.882`, methylation
  `74th percentile`, `corr(γ,GC) = 0.998`, DOI `10.5281/zenodo.20471407` all unchanged).
- The reproduction substrate (`repro/dna/_verify`, `repro/dna/_engine`, every `ax-*` package) is byte-identical
  to v1.17; `python3 -m completion.gate` → PASS 18/18, gate sha `b0cf5eae7285b50a`.

— v1.18.1, pure recovery; LOCK → Derive → Gate. Restored files carry their original v1.17 bytes.
