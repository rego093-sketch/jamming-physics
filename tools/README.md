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
