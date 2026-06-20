# HANDOFF — v11 visceral-organ anatomy coupling → continue in a fresh session

**How to resume:** paste this file + the zip
(`universal_morphogenesis_geneclock_v11_organ_anatomy.zip`) into a new conversation and say
*"continue from HANDOFF_v11_organ_anatomy.md"*. Everything runs from `code/` (flat imports). Results
land in `results/`. Verify the whole package from the package root:

```
python3 verify_all.py                 # expect OVERALL: PASS (13/13)   [see runtime note below]
python3 code/organ_anatomy.py         # print the coupled schedule + γ-ordered voxel fill table
python3 code/verify_organ_anatomy.py  # the new gate alone -> PASS 5/5
python3 code/organ_atlas.py           # v10 emergence schedule (order)
python3 code/organ_timing.py          # v10 organ-timing test (honest null [O])
```

> **Runtime note (matters for whoever continues).** The full gate suite is ~320 s wall — the
> `verify_dev_timing_wide` gate alone is ~158 s and `verify_morpho_plus` ~44 s. If your shell/tool
> caps a single command near 300 s, `verify_all.py` will be killed mid-suite (this is a *timeout*,
> not a failure). In that case verify in two pieces, which is logically identical:
> (1) run each `code/verify_*.py` individually — each prints `OVERALL: PASS (5/5 checks)` and
> regenerates its `results/*_verify.json`; (2) run layers [2]+[3] alone (import `verify_all`, call
> `compute_shas()` for the sha pin and `diff_json()`/`leaves()` over `GATES` for fidelity). v11 was
> sealed exactly this way: 11/11 gates PASS, source pin 63 files drift 0, fidelity all 11 baselines
> leaf-drift 0 → **PASS (13/13)**.

This is an **add-only, no-tuning, no-engine-edit** package under neuro VP-SPEC C3 governance:
**every constant is a measured input (locked + cited) or a derived value — never a number chosen to
hit a target.** Keep it that way.

---

## 1. What v11 did (session log)

v10 completed the *order* half of the internal-organ story: each visceral organ tagged with its
master gene, so the **ORDER** of organ appearance is `argsort(spinodal(γ))` — a deterministic
gene-clock readout of measured γ (one switch, 2.2e-16). But in the actual body the organs still
lived only as **hand-placed, time-less ellipsoids** in `assemble.anatomy_spec`; the grown organism
did not *fill in* with organs over developmental time.

v11 is HANDOFF_v10's prioritised next step #1 — **couple the schedule into Layer-2 anatomy**, as
*geometry*. One new module wraps `anatomy_spec` (no edit) and overlays the gene-clock **time-gate**:

1. **`organ_anatomy.py` — the coupling.** `timed_anatomy_spec(τ)` gates each organ ellipsoid's
   radius by the R19 emergence fold `a_f(τ; γ, tau_on)` — the **same one switch** as the face clock
   / body fold (`spinodal` identical to `morpho_core.spinodal`, max|Δ| = **2.2e-16**). An organ is
   absent before its onset (`a_f≈0`, dropped below `off_eps=1e-2`) and present after (`a_f→1`).
   Relative prominence uses only `w = dwell/max(dwell) ∈ [0.870,1.000]` (dwell ∝ γ^1.5, from v10).
   It also adds **4 new visceral ellipsoids** (stomach, pancreas, kidney, spleen) so the full v10
   **8-organ** set is realised in the body — spleen/pancreas painted **last** so central viscera do
   not overwrite them. Result: as τ advances the voxel body fills in DNA-order
   **spleen < gut < pancreas < lung < heart < liver < kidney < stomach** (== argsort spinodal(γ)),
   **complete (8/8) at τ=1**.
2. **`verify_organ_anatomy.py` — the gate → PASS 5/5.** (1) one switch; (2) complete-at-τ=1
   (spec: all 8 `a_f≥0.999`, realised, positive radii; voxel: all 8 labels present, min ≈ 40 vox);
   (3) fill order == γ readout (anatomy appearance order == schedule order; per-organ onset-midpoint
   voxel fill is a nested prefix 1,2,3,…; grid/threshold-independent); (4) overlay invariants
   (`build_tissue == naive_tissue` byte-for-byte; body surface occupancy unchanged; organs relabel
   interior voxels only); (5) determinism (env-independent canonical sha identical 2× build).

**Honest scope.** v11 is **GEOMETRY** — the v10 schedule realised in the voxel body. It makes **no
new timing-vs-biology claim**: whether the γ-order matches real organogenesis timing remains the v10
**measured NULL** (`organ_timing.py`: Spearman ρ=−0.414, perm p=0.360, grade **[O]**). Grades in
`LEDGER_organ_anatomy.md`: fill **order** [V]; gene→organ map, sign, τ-window, 4 new-organ
placement + dwell sizing [F]; absolute organ sizes [O].

## 2. Invariants / what is frozen (do not silently break)

- **No engine edit / no fork.** `assemble.py`, `anatomy.py`, `body.py`, `gene_clock.py`,
  `morpho_core.py`, `organ_atlas.py`, `organ_timing.py`, `develop.py` are **byte-identical** to v10
  (proven by the unchanged entries in `expected_sha256.json`). The coupling is a *new* module that
  *wraps* `anatomy_spec`; the original time-less `anatomy_spec` and its only consumer
  (`anatomy_figure.py`) are untouched, so no frozen v10 result can move.
- **No new measured input.** Zero new `code/data/*.json`. All γ / dwell / Carnegie tables are the
  v10 locked files, read-only.
- **Source pin:** `expected_sha256.json` pins **63** files (was 61; +2 code only). Gate suite
  **11 gates** (was 10). Fidelity baselines **11** (added `organ_anatomy_verify.json`).
- **The one switch is load-bearing.** `gene_clock.spinodal == morpho_core.spinodal` to 2.2e-16; the
  organ time-gate is the same R19 fold, not a second clock. Any future organ work must keep this.
- **`TIS` is untouched.** `organ_anatomy.py` extends it via a *local* `TIS_EXT`
  (stomach=10, pancreas=11, kidney=12, spleen=13) and `ORGAN_COLORS_EXT`; the engine's `TIS` /
  `ORGAN_COLORS` are not edited.

## 3. File inventory (what changed in v11)

- **New code:** `code/organ_anatomy.py`, `code/verify_organ_anatomy.py`.
- **New docs:** `CHANGELOG_v11_organ_anatomy.md`, `LEDGER_organ_anatomy.md`,
  `HANDOFF_v11_organ_anatomy.md`, `repro/morpho/expected/organ_anatomy_verify.json`.
- **Edited (non-engine):** `verify_all.py` (registered the new gate; it is at ROOT, not in the
  pinned `code/` set), `VERSION` (→ 11.0), `expected_sha256.json` (61→63 pin).
- **Everything else:** unchanged from v10, verified drift 0.

## 4. Next steps (prioritised) — each DATA-blocked, not effort-blocked

1. **A different measured modality for organ TIMING** (expression-onset / chromatin accessibility at
   the 8 organ-master loci). This is the **only honest lever** to actually test "DNA predicts organ
   timing" and lift row 10 of the ledger out of [O]. **[O] data-blocked**: needs an external
   organogenesis atlas as a *locked, cited* input (none in package). Same obstacle as the
   external-feature dev-timing line (v5–v8). Do **not** fabricate or back-fit timings.
2. **Per-organ measured shape / placement priors.** Replace the forced [F] ellipsoid placements and
   sizes (ledger row 8) with measured primordium geometry, to upgrade absolute organ shape (row 9)
   from [O]. Pure geometry; addable once a cited source exists. Keep it add-only (extend
   `new_visceral_organs` / `timed_anatomy_spec`, don't edit `assemble.anatomy_spec`).
3. **Widen the crisp-staged organ set** (thyroid, adrenal, gonad, …) to lift permutation power for
   the timing test — blocked by input quality (clean [V] master + crisp single-CS staging), as for
   the n=10 external set. Carry soft-staged organs in geometry only (as midgut is), never in the
   locked timing test.
4. **dna_vp merge route.** Surface the coupled organ anatomy through the dna_vp interpreter line so
   a genome → 4D body with γ-ordered organ fill is one call. Keep the VP-SPEC governance and the
   honest [O] timing caveat intact across the merge.
5. **(Optional, presentational) v11 anatomy figure.** `organ_anatomy.py` already exposes
   `ORGAN_COLORS_EXT` + `reference_volume`; a τ-sweep render would show the γ-ordered fill
   (spleen→…→stomach) visually. Display only — no new claim.

---

### One-paragraph orientation for the next session

The package grows a whole organism from measured DNA: external form (face/body/skeleton, v1–v3),
composition (adipose, v3–v5), heritability decomposition (v9), internal-organ **emergence order**
(v10), and now internal-organ **anatomy fill** (v11). The central, repeatedly-confirmed
methodological result is that measured promoter stiffness γ fixes **what emerges and in what order**
(a deterministic DNA readout, [V]) but does **not** predict **when, vs. real biology** — an honest,
robust **null** that holds for external features *and* internal organs ([O]). v11 adds no exception
to that: it realises the γ-order schedule as voxel geometry and is complete at τ=1, while the
DNA-vs-organ-timing question stays an explicitly-graded open null awaiting a different measured
modality. Everything is gated, bit-for-bit reproducible (`verify_all.py` → PASS 13/13), and built
add-only with no engine edits and no tuned constants.
