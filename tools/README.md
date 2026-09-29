# tools/ — build & manifest generation

The site is regenerated from a single machine spine. To rebuild after editing a volume:

1. `python3 tools/make_manifest.py "change note 1" "change note 2"`
   → writes `registry/vp.manifest.json` (framework + primitives + per-volume inherits/adds
     + content hashes) and appends one hash-chained line to `registry/lineage.jsonl`.
2. `python3 tools/build_index.py`
   → regenerates `docs/index.html` (homepage), reading primitive counts from the manifest
     so the page can never drift from it.

Run both from the repo root (the dir containing `docs/`, `registry/`, `tools/`).

Files:
- `make_manifest.py` — builds the manifest + lineage chain.
- `build_index.py`   — builds the homepage from `tools/master.json` + the manifest.
- `master.json`      — the per-volume data table (homepage builder input; mirrors manifest.volumes).
- `map.svg`          — the architecture diagram injected into the homepage.

See `../AGENTS.md` for the full reading guide and the inheritance contract.

## Recurrence guards (added 2026-09-29)

`tools/check_integrity.py` is run by `tools/gate.py` (section J). It performs three checks:

- **Links resolve.** Every link on every page must point to something that exists: site-relative, absolute `jamming-physics.org`, relative, and GitHub repro links.
- **Cited scripts exist.** Every `*.py` a page cites must exist under `repro/<volume>/`. Known gaps live in `registry/missing_scripts_baseline.json`, and only a **new** gap fails the check. Refresh the file with `--update-baseline` after restoring code.
- **Aggregates are generated, not hand-edited.** `docs/index.html` and `docs/concepts/index.html` must equal a fresh regeneration.

`make_manifest.py` now:

- covers all 32 volumes;
- keeps the top-level sections owned by other tools;
- leaves editorial `lt-note` asides out of primitive matching.

`build_strips.py` leaves hubs with hand-authored volume-link strips alone.
