# LEDGER — visceral-organ anatomy coupling (v11)

Honest, per-quantity grading for the v11 coupling of the v10 organ emergence schedule into the
Layer-2 voxel anatomy, in the neuro VP-SPEC C3 discipline (every quantity graded; no silent gap).
Grades: **[V]** validated/derived, **[F]** forced modelling choice (representative; documented),
**[L]** locked + cited measured input, **[O]** open (named obstacle; not claimed).

**Scope reminder.** v11 is **GEOMETRY** — it realises the v10 schedule inside the voxel body. It
introduces **no new measured input** and makes **no new timing-vs-biology claim**. The falsifiable
DNA-vs-organ-timing test and its **[O] null** are untouched in `organ_timing.py` (LEDGER row 7 of
`LEDGER_organ_emergence.md`).

## The claims, graded

| # | quantity | grade | basis / why this grade |
|---|---|---|---|
| 1 | one switch (organ time-gate fold == body fold) | **[V]** | the gate uses `gene_clock.emergence_curve`, whose `spinodal(g)=2*(g/3)^1.5` is identical to `morpho_core.spinodal` to **2.2e-16** over γ∈[1.2,1.8] (checked in-gate + `organ_atlas.assert_one_switch`). The organ time-gate is literally the same R19 fold as the face clock / neuro ch17 spinodal — not a second clock. |
| 2 | the grown body **fills with organs in γ-order** | **[V]** | first-appearance order across τ == `argsort(spinodal(γ))` == v10 schedule order (`order_is_gamma_readout=True`), verified three ways: (a) `anatomy_appearance_order` (first τ with `a_f≥0.5`), (b) per-organ onset-midpoint voxel fill is a **nested prefix** (1,2,3,…) in γ-order, (c) grid/threshold-independent (held at 140×66×72, 160×76×82, 200×96×104). Perturb a γ and the fill order resorts. No hand-typed order. |
| 3 | **complete at τ=1** (all 8 organs present) | **[V]** | spec-level: every organ `a_f(1)≥0.999`, realised in the spec, positive radius. Voxel-level: all 8 labels present in the grown body (min organ ≈ 40 voxels at the gate grid → robust, not a one-voxel sliver). |
| 4 | **overlay invariants** (optimisation + surface untouched) | **[V]** | `build_tissue == naive_tissue` **byte-for-byte** with the new organs included (the v10 bbox-cull optimisation invariant still holds); the body **surface occupancy is unchanged** by the overlay (`occ` sha identical); organs relabel **interior** voxels only (`(tissue>0).sum() == occ.sum()`). The coupling cannot silently alter the v10 body shape or break the optimised renderer. |
| 5 | **determinism / reproducibility** | **[V]** | an env-independent canonical organ-geometry sha (sorted, rounded organ list) is identical across two builds; `build_tissue` re-run is `array_equal`. The fidelity baseline `repro/morpho/expected/organ_anatomy_verify.json` reproduces leaf-drift 0. |
| 6 | gene → organ → anatomy-feature map | **[F]** | each of the 8 v10 masters mapped to a named primordium feature (heart→heart_tube, lung→lung_bud, liver→hepatic_diverticulum, gut→midgut_intestine, stomach→gastric_dilation, pancreas→dorsal_pancreatic_bud, kidney→metanephric_cap, spleen→splenic_primordium). The gene→organ identities are the v10 masters (graded [V]/[L] there); the feature **labels** attached for geometry are representative, documented choices. |
| 7 | sign convention (later onset → later fill) + τ window | **[F]** | inherited from v10: higher `spinodal` → later `tau_on` → later fill. Flipping the sign flips the fill order. The absolute τ window is display-only; only the **order + relative spacing** are read from γ. |
| 8 | **placement of the 4 new organs** (stomach/pancreas/kidney/spleen) + relative dwell sizing | **[F]** | v10's `anatomy_spec` carried only heart/lung/liver/gut; the 4 new ellipsoids are hand-placed in anatomically plausible quadrants (spleen at the dorsal apex pocket, painted **last** so central viscera do not overwrite it; pancreas painted late; stomach/kidneys in distinct quadrants), sized from the local body radius and scaled by `w = dwell/max(dwell) ∈ [0.870,1.000]`. These positions/sizes are **forced** (no per-organ measured shape prior in package), chosen only so all 8 organs resolve robustly — **not** fitted to any target. |
| 9 | **absolute organ sizes / true 3D morphology** | **[O]** | the body is a crude voxel canvas; organ ellipsoids are coarse stand-ins, not measured organ shapes. v11 claims the **fill order** and **completeness**, **not** quantitatively correct organ geometry. A per-organ measured shape/placement prior is the documented next lever (see HANDOFF). |
| 10 | **does γ predict organ TIMING vs biology?** | **[O]** | **unchanged from v10 — honest null.** v11 adds **no** timing evidence. `organ_timing.py` still reports Spearman ρ=−0.414, perm p=0.360, grade **[O]**: promoter stiffness is not the organ-timing correlate. v11's γ-ordered fill is an internal-consistency *geometry* statement, **not** a claim that this order matches real organogenesis timing. |

## What v11 deliberately does NOT do (no silent gap)

- **No engine edit / no fork.** `assemble.py`, `anatomy.py`, `body.py`, `gene_clock.py`,
  `morpho_core.py`, `organ_atlas.py`, `organ_timing.py` are **byte-identical** to v10 (verified by
  the unchanged `expected_sha256.json` entries). The coupling is a *new* module that *wraps*
  `anatomy_spec`; the original time-less `anatomy_spec` and its only consumer (`anatomy_figure.py`)
  are untouched, so no frozen v10 result can move.
- **No new measured input.** Zero new `code/data/*.json`. All γ, dwell, and Carnegie data are the
  v10 locked tables, read-only.
- **No tuning.** No constant is chosen to hit a target. `slope=14.0` (R19 onset sharpness) and
  `off_eps=1e-2` (presence threshold) are display/threshold parameters; the **order** they produce is
  invariant to them (verified across grids/thresholds), which is exactly the non-tuning guarantee.

## Open levers (each DATA-blocked, not effort-blocked) — carried to HANDOFF_v11

1. **A different measured modality for organ timing** (expression-onset / chromatin accessibility at
   the organ master loci) — the only honest lever to actually test "DNA predicts organ timing".
   **[O] data-blocked** (needs an external organogenesis atlas as a locked input; none in package).
2. **Per-organ measured shape/placement priors** — replace the forced [F] ellipsoid placements/sizes
   (row 8) with measured organ primordium geometry, to upgrade row 9 from [O].
3. **Widen the crisp-staged organ set** (thyroid, adrenal, gonad, …) to lift permutation power —
   blocked by input quality (clean [V] master + crisp single-CS staging), as for the external set.
4. **dna_vp merge route** — surface the coupled organ anatomy through the dna_vp interpreter line.
