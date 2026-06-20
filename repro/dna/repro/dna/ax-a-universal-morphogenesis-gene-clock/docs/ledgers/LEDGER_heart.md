# LEDGER — v12 cardiac single-organ deep dive (honest per-quantity grades)

Grade key (neuro VP-SPEC C3 discipline):
**[V]** validated / proven in-package · **[L]** locked measured/cited input, read-only ·
**[F]** fixed modelling choice (defensible, documented, not measured) · **[O]** open / not earned.

The governing rule: **a claim never outranks its evidence.** Every constant is a measured input
(locked + cited) or a derived quantity — never tuned to a target. The gate
`verify_heart_substages.py` enforces grade==evidence, so the [O] below passes the gate *because* it
is reported honestly.

| # | Quantity / claim | Grade | Basis |
|---|---|---|---|
| 1 | **One switch** — the cardiac sub-stage fold uses the SAME `morpho_core.spinodal` as the whole body | **[V]** | `verify_heart_substages` check 1: max\|Δ spinodal\| = 2.2e-16 over γ∈[1.2,1.8] |
| 2 | **Sub-stage schedule order == γ readout** — heart milestone order = `argsort(spinodal(γ))`; perturb a γ and it resorts | **[V]** | `derived_schedule.order_is_gamma_readout`; check 3 asserts order==argsort(spinodal); no hand-typed order |
| 3 | **Real cardiac-gene γ** — 8 master-gene promoter γ values | **[L]** | `heart_gamma.json` via `fetch_heart_gamma.py`, the **identical** NCBI→SantaLucia pipeline; READ-ONLY human promoters (TSS−2000..+500); cached → reproduces offline bit-for-bit |
| 4 | **Identical-pipeline guarantee** — same pipeline as `organ_gamma.json` | **[L]/[V]** | check 2: corr(γ,GC)=0.999 (kit sanity ~0.99) **and** NKX2-5 = `organ_gamma.json` value to 1e-9 — same gene, same pipeline, same number |
| 5 | **Cardiac Carnegie staging** — ordinal first-appearance/peak CS of the 8 milestones | **[L]** | `heart_substages.json`, compiled from O'Rahilly & Müller; Moorman & Christoffels; Sadler; Larsen's. Integer, ordinal, content-frozen (sha pinned), γ-independent |
| 6 | **Anti-back-fit** — staging not reverse-engineered to fit γ | **[V]** | check 2 `stages_independent_of_gamma`: stages unchanged under γ-perturbation **and** \|ρ\|=0.071 < 0.99 (not a suspicious perfect match) |
| 7 | **One specifier per milestone** — each milestone tagged with a single canonical master | **[F]** | Cardiac TFs are pleiotropic and combinatorial (NKX2-5/GATA4/TBX5 act across many stages). One-per-milestone is a documented forced choice (`heart_substages.json/_forced_choice_note`); each gene used for its single most characteristic role |
| 8 | **Sign / direction convention** — lower γ → earlier (spinodal→τ_on monotone) | **[F]** | Inherited from `gene_clock`/`organ_atlas`; a modelling convention, not measured. (The null is robust to this: Pearson r=−0.030, Spearman ρ=+0.071 — both ≈0.) |
| 9 | **γ predicts cardiac sub-stage TIMING vs biology** | **[O]** | **honest null.** Spearman ρ=+0.0714, exact perm p=0.882 (n!=40320), Pearson r=−0.030 → grade [O]. NKX2-5 (first, CS9) ranked near-last by γ; MEF2C (late septation) ranked first |
| 10 | **Robustness of the null** — verdict stable under staging uncertainty | **[V]** | 2000 ±1-CS jitter re-encodings: max ρ=0.395 < ρ_crit(.05)=0.714 → 0% reach significance |
| 11 | **Test is falsifiable / not blind** | **[V]** | `apparatus_detects_signal`: synthetic γ ordered to stages → ρ=+1.000 (a [V] *would* be earned if data supported it); shuffle → mean\|ρ\|=0.323 |
| 12 | **Determinism / reproducibility** | **[V]** | check 5: two `calibrate()` runs → identical result sha; integrity 69 files drift 0; fidelity `heart_substages_verify.json` 19/19 |
| 13 | **Statistical power** — n=8 is power-limited | **[O] (disclosed)** | n=8 → n!=40320; perfect order would give p≈2.5e-5, but realistic effects do not; same ceiling as the 8-organ test. Disclosed, not hidden |
| 14 | **Path to a positive result** — different measured modality | **[O] data-blocked** | A timing-relevant observable (expression-onset / chromatin accessibility) is the only lever to a possible [V]; not available as a locked input here (see HANDOFF) |

## The headline, stated honestly

Promoter thermodynamic stiffness γ is **orthogonal to developmental timing — even within one
exceptionally-well-characterised organ's own cascade.** The model's deterministic structure/order
claims remain **[V]**; the "DNA predicts *when*, vs biology" claim is a robust, single-system,
power-disclosed **[O] null**. This is the project's central methodological result, now established on
the best test system available. It is a recognized-worthy *negative*: a falsifiable prediction made
on the right system and honestly reported as not confirmed. A *positive* result would require a
different measured modality and is not claimed.
