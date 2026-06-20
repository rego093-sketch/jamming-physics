# CHANGELOG — v11 (visceral-organ ANATOMY coupling)

**One line:** the v10 organ *emergence schedule* is now realised inside the Layer-2 voxel
*anatomy* — a grown organism **fills with organ structure in γ-order** and is **complete at τ=1** —
as a pure overlay, **add-only, no engine edit, no new measured input**. `verify_all.py` **PASS
13/13**.

---

## Why v11

v10 completed the *order* half of the internal-organ story: each visceral organ was tagged with its
master gene, so the **ORDER** of organ appearance is `argsort(spinodal(γ))` — a deterministic
gene-clock readout of measured γ (one switch, 2.2e-16). But in the actual body geometry the organs
still existed only as **hand-placed, time-less ellipsoids** in `assemble.anatomy_spec`. The grown
organism did not *fill in* with those organs over developmental time; the schedule lived only in
`organ_atlas.py`, not in the voxel anatomy.

v11 is HANDOFF_v10's prioritised next step #1: **couple the schedule into Layer-2 anatomy**. It is
explicitly *geometry*, not a new timing claim.

## What v11 does

Wraps `assemble.anatomy_spec` (no edit) and overlays the gene-clock **time-gate**:

- For each organ, radius is gated by the R19 emergence fold
  `a_f(τ; γ, tau_on)` — the **same one switch** as the face clock / body fold
  (`spinodal` identical to `morpho_core.spinodal`, max|Δ| = **2.2e-16**). Before its onset an organ
  is absent (`a_f≈0`, dropped below `off_eps=1e-2`); after onset it is present (`a_f→1`).
- Relative prominence uses only `w = dwell/max(dwell) ∈ [0.870, 1.000]` (dwell ∝ γ^1.5, from v10).
- Adds **4 new visceral ellipsoids** — stomach, pancreas, kidney, spleen — so the full v10
  **8-organ** set is realised in the body (v10's `anatomy_spec` only carried heart/lung/liver/gut).
  Spleen and pancreas are painted **last** so the central viscera do not overwrite them.

Result: as τ advances the voxel body fills in DNA-order

```
spleen < gut < pancreas < lung < heart < liver < kidney < stomach     (== argsort spinodal(γ))
```

and at **τ=1 all 8 organs are present** (`order_is_gamma_readout=True`; min organ ≈ 40 voxels at the
gate grid, so every organ resolves robustly).

## New gate — `verify_organ_anatomy.py` (PASS 5/5)

1. **ONE SWITCH** — `gene_clock.spinodal == morpho_core.spinodal` (<1e-12) **and**
   `organ_atlas.assert_one_switch()`; max|Δ| = 2.2e-16.
2. **COMPLETE AT τ=1** — spec-level (all 8 `a_f≥0.999`, realised, positive radii) **and** voxel
   corroboration (all 8 labels present in the grown body).
3. **FILL ORDER == γ readout** — `order == argsort(spinodal)`; anatomy appearance order == schedule
   order; voxel fill at the per-organ onset midpoints is a **nested prefix** (1,2,3,…) in γ-order.
4. **OVERLAY INVARIANTS** — `build_tissue == naive_tissue` **byte-for-byte** (the v10 bbox-cull
   optimisation still holds with the new organs); the body **surface occupancy is unchanged** by the
   overlay; organs relabel **interior** voxels only (`(tissue>0).sum() == occ.sum()`).
5. **DETERMINISM** — env-independent canonical organ-geometry sha identical across two builds;
   `build_tissue` re-run bit-identical.

## Files

- **New:** `code/organ_anatomy.py`, `code/verify_organ_anatomy.py`,
  `LEDGER_organ_anatomy.md`, `CHANGELOG_v11_organ_anatomy.md`,
  `HANDOFF_v11_organ_anatomy.md`, `repro/morpho/expected/organ_anatomy_verify.json`.
- **Gate suite:** 10 → **11 gates** (`verify_organ_anatomy` added to `verify_all.py`).
- **Source pin:** `expected_sha256.json` 61 → **63 files** (+2 code, +0 data).
- **Unchanged (verified, 0 drift):** every governed `code/*.py` and `code/data/*.json` from v10;
  in particular `assemble.py`, `anatomy.py`, `body.py`, `gene_clock.py`, `morpho_core.py`,
  `organ_atlas.py`, `organ_timing.py` are **byte-identical**. No engine edit, no fork.

## Honest scope (grades in `LEDGER_organ_anatomy.md`)

v11 is **GEOMETRY**: the v10 schedule realised in the voxel body. It makes **no new
timing-vs-biology claim** — whether the γ-order matches real organogenesis timing remains the v10
**measured NULL** (`organ_timing.py`: Spearman ρ=−0.414, perm p=0.360, grade **[O]**). The fill
**order** is a γ readout **[V]**; the gene→organ map, sign convention, τ window, and the 4
new-organ placements + relative dwell sizing are forced modelling choices **[F]**; absolute organ
sizes are a crude canvas **[O]**.

## Verify

```
python3 verify_all.py                 # OVERALL: PASS (13/13)   [~5 min; one gate is heavy]
python3 code/organ_anatomy.py         # print the coupled schedule + γ-ordered voxel fill table
python3 code/verify_organ_anatomy.py  # the new gate alone -> PASS 5/5
```
