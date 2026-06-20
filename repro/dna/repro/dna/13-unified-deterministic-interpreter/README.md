# §13 — Unified deterministic interpreter (γ · A4 coordinate · methylation, one engine)

> One deterministic interpreter that reads a locus in **five layers**, uniting the **restored
> A4 coordinate grammar** (shell · anchor · loop · anchor-relative helix) with the
> **more-accurate methylation reading** (CpG O/E · CHG/CHH · per-gene · 4-regime auto-detector).
> Append-only on `…_INTEGRATED_v1_8_ch01-12`. The locked A4 grammar and the §12 methylation
> engine are **imported** (single source) and **sha256-pinned** — nothing in 01–12 is modified.

**Verify:** `python3 run.py` → `§13 run.py: PASS` (determinism 2× sha256 + engine gates + fidelity).

## The five layers (one locus → one record)

| layer | what it reads | source (imported, unchanged) |
|---|---|---|
| MATERIAL | γ = −mean(NN ΔG), GC, AT-run | `dna_interpreter` / `gamma_lib_v10` (γ **immutable**) |
| SWITCH | R19 double-well: spinodal = (2/3√3)γ^1.5, barrier = γ²/4, \|s\| = √γ | `switch_params` |
| COORDINATE | which shell, nearest anchor (kind/strength/dist), loops from real motors, anchor-relative helical phase → `contact_competent` | `run_key` + `interpret_element` + `parse_ft_motors` |
| ENVIRONMENT | CpG **O/E**, CHG/CHH O/E, per-gene profile, regime | `clade_reader_engine` |
| LAYER-2 | brake/accelerator sign, runtime φ, cascade role | flagged, never assigned |

γ identity (checked every run): `human_SOX2` (302,512 bp) → γ = **1.287315**.

## Two deltas this engine closes (see `LEDGER_unified.md`)

- **[RESTORED] coordinate grammar** — §11/§12 read γ + global O/E only; this reads shell/anchor/
  loop/anchor-relative-helix via real motors from re-acquired feature tables.
- **[CORRECTED] helical claim** — the §10/§11 *global* WW-ACF(10–11) periodicity percentile (a
  composition surrogate) is **retired** as an element-level structural claim, superseded by the
  anchor-relative `contact_competent`.

Methylation is **KEPT and promoted**: raw `cpg_density` conflates with GC; CpG **O/E** normalizes
it (LCT promoter: 0.0148 raw → 0.335 O/E).

## Validation panel (expected output)

| locus | kind | γ | coordinate | methylation → regime |
|---|---|---:|---|---|
| LCT promoter (chr2, §10 headline) | vertebrate | 1.3153 | mid-shell, anchor 1065 bp, 1 loop / 5 motors, contact **False** | O/E 0.335 → **VERTEBRATE_global_CG** |
| Arabidopsis (§12 region) | plant | 1.2015 | stiff-shell, anchor 4423 bp, 10 loops / 39 motors | CG/CHG/CHH 0.77/0.85/1.08 → **PLANT_global_CG_CHG_CHH** |
| honeybee (§12 region + mRNA) | insect | 1.1442 | soft-shell, anchor 411 bp, 3 loops / 14 motors, contact **True** | bulk CG 1.38, per-gene spread 0.31 / 12% low → **INSECT_targeted_gene_body** |
| human chr1 (§11 region) | vertebrate | 1.2575 | soft-shell, 2 edge motors → loop **[O]** (sparse) | CG 0.13 → **VERTEBRATE_global_CG** |

**Negative control (seed 19):** shuffle the LCT region → promoter CpG O/E 0.335 → 0.998, regime no
longer a global CG blanket. **Methylation retention:** reproduces §12 (52 quantities + auto-detector
all-correct), bit-for-bit.

## Inputs (frozen)

- `inputs_annot/{human,arabidopsis,honeybee,lct}.ft` — NCBI `efetch rettype=ft`, region-relative,
  with `_provenance.json` (accession, window, sha256). Aligned to the frozen §11/§12 FASTAs.
- `inputs_lct/lct_wide.fa` — re-acquired 120 kb wide LCT window (its 46683–49183 slice is
  byte-identical to the frozen §10 LCT promoter).
- All γ / methylation sequence inputs are the existing frozen §10/§11/§12 FASTAs (read-only).

## Files

- `unified_interpreter_engine.py` — the engine (imports + five-layer read + panel + gates).
- `run.py` — determinism (2× sha256) + gates + fidelity; writes `expected/run_gate.json`.
- `expected/unified_results.json` — frozen result (the fidelity target).
- `expected/grammar_pins.sha256` — sha256 of the four imported locked modules (drift detector).
- `LEDGER_unified.md` — the two deltas, the methylation promotion, and the retired register.
