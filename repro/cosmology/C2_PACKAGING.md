# C2 Packaging — what this distribution excludes

VP_SPEC v1.8 Constitution **C2** (inverted single-source rule): the one canonical
form is the HTML under `docs/`. Merge/distribution packages **do not bundle** the
TeX/text SSOT, because keeping two materials in sync invites drift and undermines
reproducibility. When TeX is needed it is produced **on demand** from the
canonical HTML by `tools/extract.py` (it reads the LaTeX from each equation SVG's
`img alt`).

## Excluded from this handoff (kept in the author's working repo)

| path | what it is | why excluded |
|---|---|---|
| `src/cosmology/VP_EarthCosmos_v2.tex` | TeX body source | C2 — not the canonical form; drifts from HTML |
| `manifest/cosmology.eq_list.tsv` | base64-encoded TeX of every equation | C2 — TeX SSOT, regenerable via `extract.py` |
| `tools/render_eq.js` | TeX → SVG renderer | C2 — full-rebuild pipeline only |
| `tools/split.py` | TeX → section/slug splitter | C2 — full-rebuild pipeline only |
| `src/` (all) | TeX build inputs | C2 — full-rebuild pipeline only |
| `repro/` | reproduction scripts/data | verification layer, publication-excluded (lives in the GitHub repo; chapter `isBasedOn` links point to its github.com tree) |

These files are **not deleted** from the author's repository; they are simply not
shipped in the distribution. A dedicated full-rebuild session may still use the
`src/` + `split.py` + `render_eq.js` pipeline.

## Included (the distribution = canonical + governance)

- `docs/` — the canonical site: 28 chapter pages + hub, each with answer-first,
  `vp-card`s and 6-R.4 JSON-LD; plus `robots.txt`, `sitemap.xml`, `llms.txt`,
  `llms-full.txt`, `assets/`, and the equation SVGs under `eq/` (whose `alt`
  carries the LaTeX SSOT).
- `manifest/cosmology.csv`, `manifest/slugs.csv` — read-only derived indices.
- `registry/cross_volume_doi.{csv,md}` — the 9-paper concept-DOI registry.
- `reports/phase-v1_8-cosmology.gate.json` — the v1.8 gate result (PASS).
- `tools/` — the deterministic pipeline (inventory, derive_meta, build_hub,
  reconcile_meta, upgrade_v1_8, cos_locks.json, upgrade_hub, build_site_infra,
  build_registry, build_ledger, extract, gate_v1_8), minus the TeX tooling above.
- `IRREPRODUCIBILITY_LEDGER.md`, `CHANGELOG_v1_8.md`, this file.

To recover any chapter's TeX from the canonical HTML:

```
python3 tools/extract.py <slug> --out _extract
# or every chapter:
python3 tools/extract.py --all --out _extract
```
