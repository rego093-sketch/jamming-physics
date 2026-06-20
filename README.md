# VP-SITE — unified Vacuum-Physics framework

This repository is the **single deterministic projection** of 25 VP Theory volumes,
produced by `build_site.py` from the distributed source packages. The repository is a *function
output*: do not hand-edit `docs/`; change sources or the registry and re-run the build.

## Layers
- **`docs/`** — the published site (609 pages). GitHub Pages must serve **`/docs`** only.
  URLs are frozen: `/{volume}/`, `/{volume}/{chapter}/`. Canonical domain: https://jamming-physics.org.
- **`repro/`** — verification layer (engines, manifests, pipelines, reports). Intentionally **not**
  web-served, so every `/repro/...` URL 404s on the live site. Present in the repo for reproducibility.
- **`registry/`** — `nodes.csv`, `seam_edges.csv` (authored mesh), and
  `integrated_versions.lock.csv` (content hashes + content-derived lastmod).
- **`tools/`** — offload manifest + Zenodo re-fetch script.

## Mesh — author once, project twice
Cross-volume relations are authored **only** in `registry/seam_edges.csv`. The build projects them into
(1) each hub's *Cross-package connections* block (forward links + reverse "cited by" backlinks) and
(2) a machine-readable `/{volume}/seams.json`. Backlinks are reverse-computed, never stored by hand.

## GitHub Pages setup (Phase F)
Settings → Pages → Source: *Deploy from a branch* → Branch: `main` → Folder: **`/docs`**.
This excludes `repro/` from publication automatically. A `.nojekyll` file in `docs/` keeps
underscore-prefixed paths (e.g. `_meta.json`) servable and disables Jekyll processing.

## Determinism
No wall-clock, no RNG. `lastmod` is derived from each volume's own build metadata (or a fixed
bootstrap anchor), so regenerating the whole site does not churn sitemap dates. Two successive builds
produce a bit-for-bit identical `docs/` tree (verified by the build's determinism gate).

Author: Young Jae Lee · https://orcid.org/0009-0002-7535-8245 · CC BY 4.0
