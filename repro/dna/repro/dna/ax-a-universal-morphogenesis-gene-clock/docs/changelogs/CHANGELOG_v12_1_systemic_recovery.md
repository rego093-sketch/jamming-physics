# CHANGELOG — v12.1 (systemic-parameter shape-emergence fold-in)

DNA whitepaper **v1.9.1** living-version snapshot · VP-SPEC C3 no-tuning · **add-only**.
**DOI of record `10.5281/zenodo.20471407` maintained.**

## Added (fold-in into `code/`)
- `code/emergence_v2/` — the systemic-recovery engines + gates (location-independent via `__file__`):
  - Phase 1 heart dynamics: `emergence_engine.py` + `verify_emergence.py` — **gate 7/7** (`939ae9924a6c`).
  - Phase 2 organs + allometry: `emergence_organs.py` + `verify_emergence_organs.py` — **gate 6/6** (`40225433a67a`).
  - Phase 3 reduced-order RD trajectory: `emergence_trajectory.py` + `verify_emergence_trajectory.py` — **gate 7/7** (`b2b34a770f5a`).
  - `param_db.json` (measured γ + cited/universal parameters, each `value+grade+provenance`),
    `validation_targets.json` (held separate from the engine), three `LEDGER_emergence_*.md`.
- `code/analyses/` — boundary studies `reduced_order_timing.py`, `shape_emergence_dosage.py`,
  `emergence_with_parameter.py`, and `NULL_존재이유_그리고_모델한계.md`.
- `LEDGER_systemic_recovery.md` — integrated grade-of-record + the integrated law.
- `repro/morpho/expected/emergence_gate_baseline.json` — frozen emergence fidelity pin.

## Verification lane (`verify_all.py`, add-only)
- New layer **[1b]** runs the three emergence gates (native `OVERALL: N/N -> PASS`).
- New layer **[3b]** pins each emergence gate's PASS count + engine result-hash (the gates emit no
  JSON). Layers [1]/[2]/[3] and the 12 morpho fidelity baselines are unchanged (preserved byte-for-byte).
- **`OVERALL: PASS (18/18)`**; `expected_sha256.json` pins **80** files (was 69; +11), **drift 0**.

## Re-labelled (interpretation only — numbers unchanged)
- The old `grow_to_target` scan-convergence (RMS 2.31→0.055, Chamfer→0.000; head 0.06 / bird 0.08 /
  quadruped 0.10 / fish 0.07) is now graded **target-fitting geometry [V] · NOT realized shape
  emergence [O]** — the scan supplies the coordinates; no systemic parameter realized the form.
  The only realized-shape-from-measured-systemic-parameter axis is `form(P,E)` dosage, H²=0.51 [L].
- Corrected in `LEDGER_gene_clock.md` (two convergence rows) and `README.md` (Layer 3 note).
  `grow_to_target.py` is **byte-identical**.

## Elevated
- The **integrated law** is now the appendix abstract claim-strip at the top of `README.md`.

## Unchanged (to the byte)
- Whitepaper §1–§13, the locked engines, the measured γ / Carnegie-stage tables, every null value,
  and all 69 originally-pinned `code/` files (verified byte-identical).
