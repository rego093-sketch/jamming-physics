# rot_aniso module artifacts (reference stub)

This module is a deterministic reference stub intended to satisfy the reproducibility contract described in the whitepaper (§17.1.7).

## Expected run directory outputs
A run directory produced by `src/simulate_rot_aniso.py` SHOULD contain:

- `run_log.jsonl` — JSON Lines log (schema: `schemas/run_log.schema.json`)
- `metrics.json` — summary metrics (schema: `schemas/metrics.schema.json`)
- `manifest.json` — file list + SHA256 checksums (schema: `schemas/manifest.schema.json`)
- `outputs/` — optional artifacts (tables, intermediate arrays, etc.)

## Notes
- This stub does NOT claim physical validation. It provides deterministic file generation and schema compliance.
