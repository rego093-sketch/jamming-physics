# HANDOFF — continue the upgrade in a fresh session

Paste this file + the zip into a new conversation and say "continue from HANDOFF.md".
Everything runs from `code/` (flat imports). Results are in `results/`.

---

## Where we are (session log)

1. **Layer 1 built & validated.** R19 switch as a field (validated 4.4e-16 vs in-package
   `organism/core.py`). Emergent AP registers, segmentation clock (somite count scales with
   length & γ), digit clock (4/5), metamorphosis switch. Egg→adult salamander series renders;
   per-stage timing profiled; load scales ~linearly (≈380 ms / Mvoxel).
2. **Layer 2 built (bones + organs).** Skeleton with vertebra-per-somite (41), ribs, skull,
   limb bones+phalanges; viscera fill the cavity; whole body tissue-typed (84% differentiated).
   **Optimization proven: uint8 labels + bbox culling → ~310–420× over naive, identical output**
   (naive 11 s → 35 ms for 88 internal parts).
3. **Layer 3 built (target-driven growth).** Target = SDF + landmarks. Coarse-to-fine growth
   converges the generic egg onto a scan; convergence measured (RMS, Chamfer → 0). Works on
   **fish, bird, quadruped, and a human face** from one engine.
4. **Layer 3 ⟂ DNA — gene-clock feature emergence (priority #3 DONE).** The single global σ(τ)
   schedule is replaced by a **per-feature** schedule driven by Layer-1 gene switches. Each face
   feature is tagged with a master gene (eye=PAX6, ear=PAX2, nose=LHX2, skin=TP63, + representative
   cranium/jaw/cheek/lip genes); the feature switches on at a developmental time τ_on set by **its
   gene's R19 spinodal** computed from the **measured** stiffness γ (mean −NN ΔG, SantaLucia 1998,
   NCBI promoters — read-only, never fitted). The R19 fold makes onset sharp (width ∝ barrier),
   relative size follows dwell ∝ γ^1.5. Net result: the **order** of feature appearance is now an
   emergent, deterministic readout of DNA (heterochrony), and it **resorts** when a γ is perturbed.
   The headline convergence proof is preserved exactly: at τ=1 every feature curve a_f=1, the egg
   envelope A=1, and σ_res=0, so φ → full target and RMS/Chamfer → 0 (face RMS 2.31→**0.055**,
   Chamfer→**0.000**, *better* than the global-σ baseline 0.077). Verified by a neuro-style 5/5 gate.
   New modules: `gene_clock.py`, `feature_target.py`, `grow_gene_clock.py`, `verify_gene_clock.py`,
   `demo_gene_clock_face.py`, `demo_gene_clock_universal.py`; data `code/data/sensory_organ_gamma.json`
   (26 genes, provenance preserved). Honest grading in `LEDGER_gene_clock.md`. **This is the
   re-unification of Layer 3 with the DNA framework that the previous handoff asked for.**

## Current limitations (be honest about these)
- **Renders are coarse splat clouds.** The software renderer (`morpho_core.render_mesh`) is a
  z-buffered point splat; surfaces look grainy. Fine for proof, not for beauty.
- **Face target is analytic**, not a real scan, and only roughly human. No identity, no texture.
- **Growth is a coarse-to-fine SDF blend**, not a tissue-mechanics simulation. It *reaches* the
  target (provably) but the path is a morph, not grown-from-cells dynamics.
- **No genotype→shape mapping yet.** DNA sets the egg's size (via γ) *and now the feature-emergence
  schedule/order* (via γ→R19), but it does **not** set feature coordinates. The leap to "predict a
  face's geometry from DNA" is still not attempted — Layer 3 shows the template can reach any face,
  and the gene clock shows the *timetable* to get there is a DNA readout.
- **Generic engine and Layer 3 are not yet coupled per-target.** For animals other than the
  salamander, Layer-1 registers aren't used to seed the growth; the egg is a plain sphere.

## Prioritized next steps (roughly in order of value)

1. **Couple Layer 1 → Layer 3 seeding.** Start growth from the *engine's* generic body for the
   target's clade (use `animal_target`/registers), not a bare sphere, so growth is shorter and
   the body plan (limb stations, somite count) is inherited, then refined to the individual.
   → expect faster convergence + emergent segment counts visible in the grown form.
2. **Real scan ingestion.** Implement `ScanTarget` (snippet in `README.md`), load a face/animal
   point cloud (e.g. a public 3DMM mean mesh, or a Basel/LSFM-style template), grow to it.
   Add a landmark detector hook for nose/eyes/ears so features are placed semantically.
3. **Per-feature growth timing from gene clocks. ✅ DONE (this session).** Each feature now
   switches on at a τ_on set by its own gene's R19 threshold from measured γ, so the *order* of
   feature appearance is emergent (heterochrony) and re-unites Layer 3 with the DNA framework.
   See `gene_clock.py` / `feature_target.py` / `grow_gene_clock.py`, the 5/5 `verify_gene_clock.py`
   gate, and `LEDGER_gene_clock.md`. **Natural follow-ons now unlocked:**
   (3a) tag *animal* features (fins, limbs, beak, digits) with their master genes the same way the
        face features are tagged, so quadruped/fish/bird emergence order is also a DNA readout
        (the universal demo already runs the engine on them; only the gene→part map is generic);
   (3b) calibrate τ_on against a measured developmental-timing dataset (Carnegie stages / somite
        counts) and report correlation — turning "order is a deterministic DNA function" into
        "order matches biology", which the LEDGER currently and correctly does **not** claim.
4. **Better rendering.** Replace splat with a proper triangle rasteriser (or export meshes to
   `.obj`/`.glb` and note that the client can view them). At minimum: per-face normals + simple
   shadow. Crisper voxels (smaller `vox`) where affordable — watch the load (Layer-2 culling
   already keeps interior cheap; the cost is surface marching-cubes ∝ voxels).
5. **Genotype→shape, the real aim.** Two honest routes:
   (a) *fit* — given a scan, solve for the engine/growth parameters that best reach it
       (registration → parameters), giving a low-dim "developmental code" per individual;
   (b) *learn* — if real (DNA, face-scan) pairs were available, regress the developmental code
       from sequence features. Document clearly that (b) needs data we don't have; (a) is doable
       now and yields a compact per-face parameter vector.
6. **Anatomy inside the grown target.** Run Layer-2 tissue labeling *inside* a grown target
   (not just the salamander), so any reached animal also gets bones/organs filling its volume.
7. **Determinism + packaging for the DNA whitepaper.** Still pending from earlier: wrap all of
   this as VP_SPEC chapter `15-morphogenesis-full-organism` (engine imports `organism/core.py`
   single-source + sha256-pin, `run.py` with 2× sha256 determinism gates + frozen `expected/`,
   `README.md`, `LEDGER` stating the [O] obstacle), then merge into the original package and
   return with a CHANGELOG entry. The original package lives at the user's side
   (`dna_vp_site_INTEGRATED_v1_9_stress_merged.zip`); this work goes under `repro/dna/`.

## Map of the code (`code/`)
- `organism/core.py` — the in-package R19 substrate (single source; do not fork).
- `morpho_core.py` — switch field (validated vs core) + software renderer.
- `develop.py` — registers, segmentation/digit clocks, metamorphosis switch (γ regime genes).
- `body.py` — implicit SDF primitives + bbox-culled voxelizer.
- `assemble.py` — build_body (egg→adult) + `anatomy_spec` (bones/organs from registers).
- `anatomy.py` — tissue-label rasteriser (optimized + naive) + volume report.
- `target.py` — `face_target`, `animal_target`, `Target` interface.
- `targets_zoo.py` — fish/bird/quadruped analytic targets.
- `grow_to_target.py` — coarse-to-fine growth + convergence metrics.
- `gene_clock.py` — **DNA↔morphogenesis bridge.** spinodal/barrier/dwell primitives,
  `assert_one_switch()` (proves the neuro fold == `morpho_core` fold to <1e-12), `load_gamma()`
  (read-only measured γ), `emergence_curve()` (R19 fold → sharp per-feature onset),
  `feature_schedule()` (γ → τ_on/dwell/a_f(τ) per feature + the derived emergence order, with an
  `order_is_gamma_readout` self-check).
- `feature_target.py` — `FeatureTarget` (env-aware seat: features grow *out of* the body envelope)
  + `face_features()` (gene-tagged human head), `quadruped_features()`, `fish_features()`.
- `grow_gene_clock.py` — `grow_gene_clock()`: gene-clock-driven growth with global RMS/Chamfer
  **and** per-feature RMS convergence metrics.
- `verify_gene_clock.py` — neuro-style 5-check gate (one-switch, γ-verbatim, order=DNA,
  convergence, size-law+determinism). Writes `results/gene_clock_verify.json`.
- `stages.py`, `profile_load.py`, `anatomy_figure.py`, `demo_face.py`, `demo_universal.py`,
  `demo_gene_clock_face.py`, `demo_gene_clock_universal.py` — demos.

## Invariants to preserve
- `organism/core.py` is the single source for the switch; `morpho_core.validate_against_core()`
  must stay ≤ 1e-9. γ regime is ~1.2–1.4 (NN stacking); `human_SOX2` γ identity = 1.287315.
- Vertebra count must equal somite count (the on-thesis link). Keep it.
- Keep the optimization honest: any new volume-filling must use bbox-culled label writes, and a
  naive comparator should confirm identical output + report the speedup.
- **Gene clock (new):** `gene_clock.assert_one_switch()` must stay < 1e-12 (the neuro fold and the
  body fold are literally one function); γ is **read-only** — loaded from `data/sensory_organ_gamma.json`,
  never tuned or back-fitted to make the order come out nicely; the τ=1 state must equal the full
  target (every a_f=1, σ_res=0) so the RMS/Chamfer→0 proof is never weakened by the schedule; and
  the emergence order must remain exactly `argsort(spinodal(γ))` (a pure DNA readout, `order_is_gamma_readout`
  stays True), so perturbing a γ deterministically resorts the order.

---

## SESSION UPDATE — priority #3a DONE: head detail + animal features gene-tagged (v3)

Built on the neuro engine as technical base, this session **expanded the body scope and deepened
the face**, and grew the measured γ table from 26 → 42 genes — all invariants held (5/5 gate).

**What was added**
- **Human head deepened to 34 features / 13 master genes:** scalp hair (EDAR), eyebrows (FOXN1),
  eyelashes (HOXC13), eyelids (TP63), iris (MITF), philtrum (SHH), teeth (PAX9), tongue (POU2F3),
  neck — on top of the original eye/ear/nose/skin/cranium/jaw/cheek/lip set.
- **Three animals, gene-tagged** (`feature_atlas_plus.py`, registry `ATLAS`): **bird**,
  **quadruped**, **fish**. Limb identity uses the real *Tbx5*(fore)/*Tbx4*(hind) split; digits
  *Hoxd13*; beak *Bmp4*; gills/cartilage *Sox9*; feathers/coat/scales *Edar* (representative).
- **Measured table 26 → 42** (`data/morpho_gamma.json` + `data/fetch_morpho_gamma.py`): 16 new
  genes fetched by the **identical** NCBI→SantaLucia-NN pipeline used for the taste set,
  corr(γ,GC)=0.997. Original 26 preserved **bit-for-bit** (verifier check #2).
- **Crisp triangle renderer** (`render_plus.py`): deterministic painter's flat-shaded raster,
  every surface patch tinted by the master gene that built it. (Replaces the grainy splat for
  these figures; `morpho_core.render_mesh` is still there.)
- **Demo** `demo_morpho_plus.py` → per-organism montage+schedule+convergence figures,
  `morpho_heroes.png`, `morpho_heterochrony.png`, `morpho_plus.json` (+ DNA-sensitivity test).
- **Gate** `verify_morpho_plus.py` → **PASS (5/5)** over ALL FOUR organisms: one-switch 2.2e-16;
  base-26 γ bit-identical inside the 42 (0 drift) and == neuro table; order==argsort(spinodal(γ))
  for each body; convergence Chamfer→0 for each; dwell monotone over 42 γ + schedule & **mesh**
  sha256 determinism.

**Results (all Chamfer 0.0000):** head RMS→0.06 (34/34 feats), bird→0.08 (18/18), quadruped→0.10
(22/22), fish→0.07 (15/15). Each emergence order is a DNA readout that resorts under a γ perturbation.

**A limitation now improved:** renders are no longer coarse splat clouds for these figures — the
triangle rasterizer is crisp. (The analytic-vs-real-scan and absolute-timing limitations below
still stand.)

## NEXT (open [O], in priority order)
1. **Calibrate the emergence order against real developmental timing. ✅ DONE (v5) — honest NULL.**
   Built `dev_timing.py` + `data/dev_timing.json` (7 master features → Carnegie stage, [L] locked &
   cited: O'Rahilly & Müller / Larsen's / UNSW Hill) and tested `corr(spinodal(γ), observed_stage)`
   with zero tuning. **Result: it does NOT match** — Spearman ρ = −0.018, exact permutation p = 0.986.
   Measured promoter stiffness is **not** the molecular correlate of developmental timing. The order
   claim is now a **measured [O]** (tested-and-not-matching), a stronger position than the prior
   untested hedge. Apparatus proven non-blind (synthetic γ∝stage → ρ=1.0). Gate `verify_dev_timing.py`
   → PASS (5/5), enforcing **grade == evidence**. Full grading in `LEDGER_dev_timing.md`. *Next on this
   thread:* test whether some OTHER measured molecular quantity (expression onset, enhancer count)
   predicts staging — γ is now ruled out for these features.
2. **Test the size law on a real scan:** `corr(feature_size, γ^1.5)` once features carry measured
   sizes (the hook exists in `dwell`); the analytic stand-ins are not gene-sized so size is [O].
3. **Upgrade representative [F] gene tags to [V]** by sourcing cleaner masters (e.g. neural-crest
   skeletal set for vault/jaw; a feather/hair-shaft master distinct from EDAR for the placode vs.
   shaft distinction).
4. **Real human scan** instead of the analytic head (identity + texture), then re-run the whole gate.

## New invariants to preserve (in addition to all above)
- `data/morpho_gamma.json` must keep the **original 26 γ bit-for-bit** — `verify_morpho_plus.py`
  check #2 (0 value drift, and == neuro table). New γ are **measured by the pipeline, never tuned**.
- `feature_atlas_plus.ATLAS` schedules must stay `order_is_gamma_readout == True` for every organism.
- The τ=1 state still equals the full target for every organism (every a_f=1, σ_res=0) → Chamfer→0.

---

## v3 addendum — Layer 4: adipose / energy-balance morphology (composition axis)

5. **Layer 4 ⟂ DNA — adipose built.** The gene clock sets feature *order/timing*; Layer 4 adds the
   *composition* axis so **one genome can be lean ↔ heavy, in the face and the body** — the single
   largest driver of real external variation. No HPC, no learned data: an analytic SDF-dilation
   field driven by (1) **measured obesity-gene γ** (same NCBI→SantaLucia-NN pipeline; [L]), (2) an
   **energy dial E** (chronic surplus/deficit; an input), (3) an anatomical **depot map** ([F]).
   An adipocyte's store/mobilize set-point is bistable with hysteresis, so it uses the **identical
   R19 fold** (`assert_one_switch_adipose() = 2.2e-16`) — adiposity is the time clock's twin in the
   energy axis.

**What was added**
- **Engine** `code/adipose.py`: `spinodal` (same switch), `adipose_setpoint` (fold readout that
  actually crosses the spinodal → real tipping into storage), `AdiposeModel` (drive = k_E·E +
  P_geno; floor-subtracted so neutral@E_lean → α≡0), `DepotMap` (android/gynoid soft-OR depots),
  `inflate_sampler` (φ' = φ_lean − t_max·α·depot), and readouts (`adiposity_index`,
  `face_width_height_ratio` = lower-face cheek/jowl band, `waist_hip_ratio`). `GENOME_PRESETS`
  {neutral, thrifty, lean} are **weightings over the SAME measured panel** ([F] which genome to
  simulate; γ values identical/measured). `propensity_is_gamma_readout == True` (neutral≡0).
- **Atlas** `code/adipose_atlas.py`: `human_body()` + depot factories for **face / body /
  quadruped / bird** (`SCENES` registry). Textbook subcutaneous placements (buccal, jowl, jawline;
  abdominal-visceral vs gluteofemoral; dewlap/rump; furcular premigratory fat).
- **Obesity γ** `code/data/obesity_gamma.json` + `data/fetch_obesity_gamma.py`: 17 obesity genes
  fetched by the **identical** pipeline, corr(γ,GC)=**0.998**. Table **42 → 59**; original 42
  preserved **bit-for-bit**; `_provenance_obesity` records it. Cache `obesity_promoters.cache.json`.
- **Demo** `code/demo_adipose.py` → `results/adipose_face.png` (lean→heavy face, W:H 0.44→0.56),
  `adipose_body.png` (belly+hips, AI 0→0.55), `adipose_quadruped.png` (general), and the key
  `adipose_gene_x_env.png` (**same E, lean vs thrifty genome** → AI 0.01 vs 0.55), plus
  `adipose.json` (every number + sha256).
- **Gate** `code/verify_adipose.py` → **PASS (5/5)**: (1) one-switch 2.2e-16; (2) γ-superset — orig
  42 bit-identical inside 59, obesity γ measured (prov + corr 0.998); (3) gene×env — within-genome
  AI monotone in E, **cross-genome absolute α/volume ordered thrifty≥neutral≥lean on a 41-pt E
  grid**, propensity=γ-readout, neutral≡0; (4) baseline preserved — neutral@E_lean → α≡0 → inflated
  surface == lean target **bit-for-bit** (face+body); (5) determinism — field + mesh sha256 stable.
- **`verify_morpho_plus.py` re-run → still PASS (5/5)** — Layer 4 perturbed nothing upstream.

**Subtlety worth remembering:** the **self-referential** adiposity index (vs a genome's *own* lean
baseline) is correct for the **within-genome energy sweep** ("eat more → store more"), but it is the
**wrong** cross-genome metric, because a thrifty genome is already not lean at E_lean. Cross-genome
comparison ("the gene effect") must use **absolute** adiposity (α / occupancy volume); the gate and
the gene×env figure both do this (figure measures AI against a single shared lean-genome reference).

## NEXT for Layer 4 (open [O], in priority order)
1. **Calibrate to kilograms/BMI.** Fit `t_max` and the E-window against anthropometric/DXA data so
   the adiposity index maps to real fat mass. Until then only the index + the laws are claimed.
2. **Person-specific depot pattern.** Replace the textbook [F] DepotMap with a subject's measured
   subcutaneous distribution; test the android/gynoid axis against waist–hip data.
3. **Validate gene signs/magnitudes** against adipose GWAS effect sizes (does measured γ-propensity
   correlate with per-gene BMI effect?). This is the honest leap from "γ sets a propensity" to
   "γ-*predicted* propensity".
4. **Couple to the time clock: ✅ DONE (v5).** `life_course.py` runs the gene clock (TIME axis, τ)
   and the adipose fold (ENERGY axis, E) **together on one genome** as a single continuous R19
   process: `assert_one_continuous_fold()` proves both folds are the body fold (2.2e-16 each). A
   chosen life (`default_life()`: infant→child→adolescent→adult-lean→surplus→heavy) gives a monotone
   trajectory — A(τ)↑ with growth, occupancy↑ with E at maturity — with **baseline preserved
   bit-for-bit** at the lean reference (α≡0). `demo_life_course.py` renders the face + body montages;
   `verify_life_course.py` → PASS (5/5). Grading in `LEDGER_life_course.md`. *Remaining [O] on this
   thread:* real ages/BMI and a child-specific depot map (adult depot is reused throughout life [F]).

## New invariants to preserve (in addition to all above)
- `adipose.assert_one_switch_adipose()` must stay `< 1e-12` (the adipose fold == the body fold).
- `data/obesity_gamma.json` must keep the **original 42 γ bit-for-bit** (`verify_adipose.py` #2);
  obesity γ are **measured by the pipeline, never tuned**.
- neutral genome at `E_lean` must give α ≡ 0 so the inflated surface == the lean target and the
  Layer-3 convergence proof survives (`verify_adipose.py` #4). The headline result may not move.
- cross-genome ordering is on **absolute** adiposity; self-referential AI is for the within-genome
  sweep only.

---

## SESSION UPDATE — v5: developmental-timing calibration (honest null) + life-course coupling

Both items were **add-only** (no engine edit, no fork of `organism/core.py`) and **no-tuning**.
**All five gates pass 5/5:** `verify_gene_clock`, `verify_morpho_plus`, `verify_adipose`,
`verify_dev_timing`, `verify_life_course`.

**1 · Developmental-timing calibration (was NEXT #1) — the headline is an HONEST NULL.** This is the
correct VP-SPEC outcome and should be read as the governance *working*, not failing. The framework's
central open claim ("emergence order is a γ readout, not claimed to match biology") was put at risk
against canonical Carnegie staging and **refuted**: ρ = −0.018, exact permutation p = 0.986. Measured
promoter stiffness γ is not the molecular correlate of developmental timing. The claim is now a
**measured [O]** (tested-and-not-matching) — strictly stronger than the prior untested hedge. No γ,
constant, or stage was touched to soften this; the gate certifies *honesty* (grade == evidence), not
a good correlation. New: `dev_timing.py`, `verify_dev_timing.py`, `data/dev_timing.json`,
`LEDGER_dev_timing.md`.

**2 · Life-course coupling (was Layer-4 NEXT #4).** Self-contained, no external data, no null risk.
Unifies the TIME axis (gene clock) and the ENERGY axis (adipose) into **one continuous R19 fold** on
a single individual: child → adult (τ) → heavier adult (E). Both folds proven to be the body fold
(2.2e-16). Baseline preserved bit-for-bit at lean (α≡0), so Layer-3 convergence is untouched. New:
`life_course.py`, `demo_life_course.py`, `verify_life_course.py`, `LEDGER_life_course.md`,
`results/life_course_face.png`, `results/life_course_body.png`, `results/life_course.json`.

### NEXT from here (v6 candidates, in rough priority)
1. **Find the *right* timing predictor. ✅ DONE (v6 #1) — wider honest NULL.** Kept the apparatus,
   swapped the input variable across a 6-predictor battery (γ, GC, CpG o/e, TATA/GC-box/CAAT density).
   **All six are [O]** (best |ρ| = 0.624 on gcbox, wrong sign; best positive ρ = 0.468 on caat,
   Bonferroni p = 1.0). Promoter *composition* — not just stiffness — does not predict Carnegie order
   for these 7 features. The remaining sub-paths are still open: **expression-onset / chromatin
   accessibility** predictors are **[O] data-blocked** (atlas not in package), and the moderate
   positive composition trend is unresolved at n = 7 → see #2. See `LEDGER_timing_predictors.md`,
   `verify_timing_predictors.py`, `CHANGELOG_v6.md`.
2. **Widen the dev-timing table** beyond 7 features (add somite-count milestones, more [V] masters
   with unambiguous first-appearance stages) to sharpen the permutation test's power.
3. **Calibrate the life course to real ages/BMI** ([O]) and give the child a **child-specific depot
   map** (currently the adult depot is reused throughout life, declared [F]).
4. The standing Layer-4 items (kilograms/BMI calibration, person-specific depot, GWAS sign/magnitude
   validation) and the standing gene-clock items (size law on a real scan, [F]→[V] tag upgrades,
   real human scan) remain open.

### Invariants added this session (in addition to all above)
- `data/dev_timing.json` is **read-only measured**, frozen by sha256; never edit a stage to move ρ.
  `verify_dev_timing.py` enforces **grade == evidence** — a green gate means the truth was reported,
  not that the correlation was good. The falsifiability self-test (synthetic γ∝stage → ρ=1.0) must
  keep passing or the null is meaningless.
- `life_course.assert_one_continuous_fold()` must stay `< 1e-12` for **both** the TIME and ENERGY
  folds; at the lean reference the trajectory must keep `α ≡ 0` and reproduce the pure gene-clock
  field **bit-for-bit**; at τ=1 `DevTarget` must reduce to the full lean target (no developmental
  freeze leaking into the converged adult).

## SESSION UPDATE — v6: standalone-repro backbone fix + #1 timing predictor battery

Two clearly-separated pieces; **add-only, no engine edits; unified entry now PASS 8/8** (six gates
5/5 + source pin drift 0 + six fidelity baselines leaf drift 0). Full detail in `CHANGELOG_v6.md`.

**Part A · standalone-reproducibility backbone fix.** v5.1's bit-for-bit fidelity layer pinned an
**environment-dependent** *bonus* string (a cross-package provenance line that only resolves when the
neuro v1.9 sibling is co-located), so a clean standalone checkout reported `FAIL (6/7)` despite
untouched science and green gates. Diagnosed to a single string leaf; the mirror pattern in
`verify_gene_clock.py` check-2 had been frozen in the opposite environment. Fixed by making **both**
gates' *pinned* messages environment-independent — the neuro cross-check still runs, still prints
`[bonus, unpinned]`, still gates a genuine mismatch when neuro is present (`ok = ok and same`); only
the env-dependent string left the pinned set. Rejected the two dishonest options (fabricating a neuro
sibling; re-freezing to bury the red). The backbone now reproduces standalone with no loss of
cross-package power.

**Part B · v6 #1 — swap the input variable (honest, wider NULL).** Kept the exact dev-timing
apparatus (same locked Carnegie stages, same exact-permutation Spearman test, same grade==evidence)
and ran a **6-predictor battery**: `gamma`, `gc` (read verbatim from locked `morpho_gamma.json`),
`cpg_oe`, `tata`, `gcbox`, `caat` (computed from promoter sequence, fixed a-priori motifs).
**Every predictor is [O]** (Bonferroni α = 0.00833; smallest Bonferroni p = 0.867). `gamma`
reproduces the v5 null exactly (consistency check). The exact-permutation **floor** (0.00079 < α) is
computed and disclosed → significance *was* reachable, so the null is real, not a dead test. Three
composition predictors show a moderate non-significant positive trend (ρ ≈ +0.40…+0.47) that n = 7
cannot resolve.

New files: `code/timing_predictors.py`, `code/verify_timing_predictors.py`,
`code/data/timing_promoters.cache.json` (self-contained 7-gene cache: 4 byte-for-byte copies +
3 re-fetched-and-frozen with residuals recorded), `LEDGER_timing_predictors.md`, `CHANGELOG_v6.md`.
`verify_all.py` GATES extended to 6; `expected_sha256.json` now pins 45 files; new fidelity baseline
`repro/morpho/expected/timing_predictors_verify.json` (17 leaves).

### NEXT from here (v6 candidates, updated)
1. ~~Find the right timing predictor~~ — **DONE for promoter composition (all [O])**; remaining
   sub-paths: **[O] expression-onset / chromatin-accessibility predictors are data-blocked** (need an
   external developmental atlas added as a locked input).
2. **Widen the dev-timing table** beyond n = 7 — now the **binding constraint**: the permutation
   floor and the unresolved moderate positive composition trend both demand more [V]-master features
   with citable first-appearance stages. This is the highest-value next step.
3. Calibrate the life course to real ages/BMI ([O]); child-specific depot map (adult depot reused, [F]).
4. Standing Layer-4 and gene-clock items remain open (kg/BMI calibration, person-specific depot,
   GWAS sign/magnitude, size law on a real scan, [F]→[V] upgrades).

### Invariants added this session (in addition to all above)
- `data/timing_promoters.cache.json` is **frozen**: the 4 copied sequences must stay byte-identical
  to `morpho_promoters.cache.json`, and the 3 re-fetched sequences must reproduce the **locked** γ
  within assembly-drift tol (5e-3); never overwrite a locked γ/GC value to chase a match.
- `verify_timing_predictors.py` enforces **grade == evidence** over the whole battery, Bonferroni
  correction, motif consensus fixed a priori, and the disclosed permutation floor. Its non-blind
  self-test (synthetic comonotone predictor → ρ = 1.0, perm p < 0.05) must keep passing or the
  all-[O] null is meaningless. `gamma`'s rank correlation must keep equalling dev_timing's spinodal ρ.
- Both env-dependent gate strings (`verify_gene_clock.check_gamma_verbatim`,
  `verify_morpho_plus.check_gamma_superset`) must stay environment-independent in the **pinned** msg
  while keeping the neuro cross-check live when the sibling is present.

## SESSION UPDATE — v7: widen the dev-timing table to n=10 (lift the power floor)

**Add-only, no engine edits; unified entry now PASS 9/9** (seven gates 5/5 + source pin drift 0 +
seven fidelity baselines leaf drift 0). Full detail in `CHANGELOG_v7.md` / `LEDGER_dev_timing_wide.md`.

This is v6 NEXT #2 — the step the v6 HANDOFF named as the **highest-value next** and the **binding
constraint**. v5 reported the honest null (promoter-stiffness γ does not predict Carnegie staging,
ρ = −0.018, perm p = 0.986); v6 widened it to proximal-promoter *composition* (6-predictor battery,
all [O]) and flagged the two limitations: at **n = 7** the exact-permutation **floor was 7.9e-4** (the
power ceiling), and a moderate positive composition trend (`cpg_oe`/`tata`/`caat`, ρ ≈ +0.4) could not
be resolved. v7 does exactly that step with the **same apparatus and zero tuning**.

**What was added.** Three more genuine **[V]-master** features, each pinned from a primary source
**before** any correlation, on top of the locked 7 (loaded byte-for-byte, unchanged):
`foxg1_cerebral_vesicle/FOXG1/CS14` (Müller&O'Rahilly 1988, PMID 3377191 — the gene in the *title* of
the CS14 staging paper), `mitf_rpe_pigment/MITF/CS15` (O'Rahilly&Müller; PMID 1927245),
`sox9_chondrification/SOX9/CS17` (O'Rahilly&Müller Publ. 637). Full n = 10 stage vector
`[9,10,12,13,13,14,15,17,17,18]`. **Two documented scope corrections** (not silent): FOXG1 and SOX9 are
`[F]` in the broad atlas (vague multi-feature programs) but the canonical **[V]** masters for these
*specific* features (telencephalon; chondrogenesis); MITF was already a `[V]` master. γ/GC read
**verbatim** from locked `morpho_gamma.json`; the new cache supplies raw sequence only — **MITF/SOX9
byte-for-byte copies** recompute the locked γ **exactly (Δ=0)**, **FOXG1 re-fetched once** by the
identical pipeline reproduces it within assembly drift (Δγ = 2e-4 ≤ tol 5e-3).

**New exact-permutation engine.** At n = 10, 10! × 6 predictors is too slow to brute-force through
scipy. Since Spearman ρ is an **affine function** of `S = Σ rank_x·rank_y[perm]`, the permutation null
of ρ depends only on the stage-rank multiset (for tie-free predictors), so the exact null of `S` is
computed **once by dynamic programming** and reused for every predictor + the floor (predictor ties
handled in the same DP; ranks ×2 → exact integer keys; tied stages counted with multiplicity → DP
total = n!). ~0.02 s. **Validated in the gate before the n = 10 claim**: reproduces the v5 brute-force
oracle (`DT._perm_p`) **bit-for-bit at n = 7, 8** and a vectorised oracle at **n = 9**.

**Result (reported, not tuned).** Widening to n = 10 **lifts the floor from 7.9e-4 to 2.2e-6**, so
Bonferroni significance (α = 8.3e-3) is amply reachable. **Every test is still [O]** (γ/spinodal
ρ = −0.280, perm p = 0.429; best composition predictor `tata` ρ = +0.490, perm p = 0.183). The moderate
positive composition trend **survived the widening and still did not reach significance** → a **real
null at n = 10**, not a power artifact. Proximal-promoter composition does not predict Carnegie staging
order even with the floor lifted.

New files: `code/dev_timing_wide.py`, `code/verify_dev_timing_wide.py`, `code/data/dev_timing_ext.json`,
`code/data/dev_timing_ext_promoters.cache.json`, `LEDGER_dev_timing_wide.md`, `CHANGELOG_v7.md`,
`repro/morpho/expected/dev_timing_wide_verify.json`. `verify_all.py` GATES extended to **7**;
`expected_sha256.json` now pins **49** files (was 45).

### NEXT from here (v7 candidates, updated)
1. **More [V]-master features still helps** (the floor keeps dropping). Next clean candidate:
   **MYF5 → first myotome**, deliberately *excluded* from v7 (would be n = 11) because its
   first-appearance staging is too soft for a locked input — the first myotome spans CS11–13 across
   sources (somite CS9, myotomal differentiation CS10–11, "myotomes fuse at 10.5–12 mm" in the Manual
   of Human Embryology). **Obstacle**: pin a single citable first-myotome CS *and* re-fetch + freeze
   the MYF5 promoter (reproducing its locked γ) before adding. Remaining 42-table genes are `[F]` for
   any single feature and would confound the test.
2. **[O] data modality is now the main lever** — proximal-promoter composition is **exhausted**
   (all [O] at n = 10 *with* ample power, so this is settled, not underpowered). The remaining honest
   lever is a **different measured quantity** at the master loci: expression-onset or chromatin
   accessibility. **Obstacle**: needs an external developmental atlas added as a *locked* input; none
   is in the package, so it stays data-blocked.
3. Standing items unchanged: life-course kg/BMI calibration ([O]); child-specific depot map ([F]);
   GWAS sign/magnitude; size law on a real scan; `[F]→[V]` upgrades.

### Invariants added this session (in addition to all above)
- `data/dev_timing_ext.json` is **frozen**: 3 stages stay integer + γ-independent; never overwrite a
  locked γ/GC to chase a match.
- `data/dev_timing_ext_promoters.cache.json` is **frozen**: MITF/SOX9 sequences stay byte-identical to
  `morpho_promoters.cache.json` and reproduce the locked γ **exactly**; FOXG1 reproduces it within
  assembly-drift tol (5e-3).
- `verify_dev_timing_wide.py` enforces **grade == evidence** over both tests, Bonferroni, a-priori
  motifs, and the disclosed permutation floor (which must stay **below** the n = 7 floor of 7.9e-4 —
  more features, more power, by construction).
- The **DP exact-permutation engine must keep matching** the brute-force/vectorised oracles at
  n = 7, 8, 9, and its n = 10 non-blind self-test (synthetic comonotone → ρ = 1.0, perm p < 0.05) must
  keep passing, or the all-[O] null is meaningless. The original 7 features must stay bit-identical to
  `dev_timing.json` with the stage sha frozen.

## SESSION UPDATE — v8: harden the n=10 dev-timing null (robustness); MYF5 dead-end documented

**Add-only, no engine edits, NO new measured input, NO new feature; unified entry now PASS 10/10**
(eight gates 5/5 + source pin drift 0 + eight fidelity baselines leaf drift 0). Full detail in
`CHANGELOG_v8.md` / `LEDGER_dev_timing_robust.md`.

v7 widened the dev-timing test to n=10 (every predictor [O], floor lifted to 2.2e-6, ample power) and
named **MYF5 → first myotome** (n→11) as the next clean feature. v8 did two things.

**1 · Investigated MYF5/myotome from the primary literature and did NOT lock it.** A locked stage must
be a genuine, citable, single-stage measured input — never picked from a range. MYF5/myotome fails for
two independent reasons: (a) **the gene precedes the structure** — MYF5 is first expressed in the
*dermomyotome*, before the myotome forms (Ott et al., *Development* 111:1097, 1991: "myf-5 … first
detected in the earliest somites … in the dermomyotome, **before** formation of the dermatome, myotome
and sclerotome"); the other ten [V] masters turn on *at* their named primordium. (b) **No crisp single
Carnegie stage** — first-myotome appearance is progressively distributed (somite CS9+, dermomyotome
CS11–12, myotome after), spanning **CS11–13** across sources, with no textbook single "myotome at CS X"
of the kind O'Rahilly & Gardner give for the limb buds. Locking it would mean choosing one stage from a
range AND papering over the dermomyotome/myotome distinction — disguised tuning. The remaining 42-table
genes (EDAR/FOXN1/HOXC13 → hair [late/fetal]; MSX1 → tooth [redundant]; BMP4 [pleiotropic]; LEF1
[multi-feature]; TYR/GLI3 [F]) are likewise unsuitable. **The clean [V]-master + crisp-Carnegie-stage
set is saturated at n=10** — a real finding, not a stopping-for-convenience.

**2 · Hardened the n=10 null** by *verifying* two robustness properties (predictor values fixed; only
the stage target is perturbed/subsetted; no free parameters; same validated DP engine):
- **Stage ±1 ordinal robustness** — `dev_timing.json`'s `_method` *asserts* the rank test is "robust to
  ±1-stage encoding uncertainty"; v8 *tests* it. 20 one-at-a-time ±1 perturbations flip no predictor to
  [V]; smallest perm p over all = **0.119** (≫ Bonferroni α = 8.3e-3). Stable.
- **Leave-one-out jackknife** — dropping any single feature (n=9) flips no predictor to [V]; every fold
  retains power (floor ≤ 2.2e-5 < α). The most favorable fold (drop `tooth_germ`) lifts `tata` to
  ρ = +0.830 (raw perm p = 0.024) — yet Bonferroni (×6 = 0.143) keeps it [O]. Even the best subset for
  the composition trend fails honest correction.
- **Non-blind control** — a synthetic comonotone predictor (ρ = 1.000) flips to [V] at n=10 and in every
  fold → the no-flip result is a *true negative*.

**Result (reported, not tuned):** the n=10 every-predictor-[O] null is **ROBUST** — stable under ±1
stage uncertainty and to single-feature removal, power retained throughout, machinery provably non-blind.

New files: `code/dev_timing_robust.py`, `code/verify_dev_timing_robust.py`, `LEDGER_dev_timing_robust.md`,
`CHANGELOG_v8.md`, `repro/morpho/expected/dev_timing_robust_verify.json`. `verify_all.py` GATES extended
to **8**; `expected_sha256.json` pins **51** files (was 49; +2 code, no new data).

### NEXT from here (v8 candidates, updated)
1. **Widening n further is blocked by input quality, not effort.** No clean [V]-master + crisp-Carnegie
   feature remains in the current table (MYF5/myotome and all others are too soft/fetal/redundant/
   pleiotropic). **Obstacle**: a genuinely new feature needs a curated master→primordium pair with
   textbook-crisp staging, or a larger measured γ table.
2. **[O] data modality is the main scientific lever** (unchanged): expression-onset or chromatin-
   accessibility at the master loci — a *different measured quantity*, not more promoter composition.
   **Obstacle**: needs an external developmental atlas as a *locked* input; none is in the package.
3. Standing items unchanged: life-course kg/BMI calibration ([O]); person-specific depot map ([F]);
   GWAS sign/magnitude; size law on a real scan; [F]→[V] upgrades.

### Invariants added this session (in addition to all above)
- `verify_dev_timing_robust.py` enforces: stage ±1 perturbation flips no predictor to [V] and never
  drives any perm p below the Bonferroni α; leave-one-out flips no predictor and every fold retains
  power; the positive control (synthetic comonotone) **does** flip (non-blind); the analysis runs on the
  exact locked n=10 inputs (original 7 bit-identical, 3 appended, stage shas frozen) with the predictor
  matrix bit-identical to `dev_timing_wide`'s. If any breaks, the robustness claim is void.

---

## v9 session — the SHAPE-decomposition CAPSTONE (project conclusion)

**What v9 did.** Answered the project's actual headline question — *how much of the final FORM (face,
body) does measured DNA fix?* — which the v6–v8 developmental-*timing* line (an honest robust null) was
only tangential to. The model is built to embody the empirically obvious answer: **DNA is the FIRST
CAUSE of form but not the whole of it** — identical twins resemble yet diverge with different lives. v9
makes that decomposition explicit and quantitative on the package's already-gated gene × environment
machinery (the adipose fat-fold) and anchors it to published twin-study heritability. Add-only, no
engine edit; one new locked + cited input.

**Result (reported, not tuned).**
- Variance decomposition of body shape over a genetic-propensity × environment grid: at a realistic
  range **H² = 0.51** (E² = 0.25) — inside the published twin band (BMI/body-fat/waist 0.48–0.63).
  **Shape is neither all-DNA nor all-environment.**
- **Heritability is population-dependent and the model reproduces it**: H² rises to 0.84 (narrow
  environment) and falls to 0.10 (wide environment) — matching the published fact that twin BMI-
  heritability varies across populations. So the anchor is a **regime** match, not a tuned decimal.
- **Identical-twin decomposition**: same genome at the shared lean reference is **bit-identical** (the
  resemblance); two lives → **same DNA, but the surplus life adds +37% body volume and +25% lower-face
  roundness** (the environmental envelope).
- **Face**: roundness is environmental (cheek/jowl), the bony frame is the γ-fixed core — matching twin
  3D studies (cheeks/chin/lips most environmental, midface bone most heritable).

**Files.** `code/morpho_decomposition.py`, `code/verify_morpho_decomposition.py`,
`code/data/heritability_anchor.json` (locked + cited), `LEDGER_morpho_decomposition.md`,
`CHANGELOG_v9.md`, `PROJECT_SUMMARY.md`, `repro/morpho/expected/morpho_decomposition_verify.json`.
`verify_all.py` GATES extended to **9**; `expected_sha256.json` pins **54** files (was 51; +2 code, +1
data). `verify_all.py` → **PASS 11/11** (nine gates 5/5 + source pin drift 0 + nine fidelity baselines).

### Invariants added this session
`verify_morpho_decomposition.py` enforces: (1) at the reference range H² + E² + GxE = 1 with both
genetic (≥0.15) and environmental (≥0.10) fractions substantial; (2) the heritability regime — reference
H² in the published band, model H² range overlaps it, and H²(narrow) > H²(ref) > H²(wide); (3) the twin
decomposition — same-genome shared core bit-identical and the surplus twin larger AND rounder; (4) the
genetic axis is a measured-γ readout, one switch < 1e-12, α(lean) ≈ 0 (lean baseline preserved),
explicit α == `model.activation`, anchor sha frozen; (5) determinism. If any breaks, the decomposition
claim is void.

### NEXT from here — the project is intentionally CONCLUDED (see PROJECT_SUMMARY.md)
The headline question is answered. The remaining open levers, each needing a **measured** input the
package does not contain (so none is "more effort" — each is data-blocked):
1. **Facial-bone non-adiposity environmental axis** `[O]` (clearest slot): the model's bony face is
   γ-only, so it attributes facial *aging/gravity/sun* change to nothing — real faces change there.
   Needs a measured facial-aging / soft-tissue axis as a locked input.
2. **Real morphometric validation** `[O]`: decompose against real paired genotype–morphometry scans
   (twin face/body), not just the model's internal property. Needs that dataset as a locked input.
3. **Canonical population for a single H²** `[O] by design`: fix a reference environmental distribution
   to collapse the range-dependent H² to one number (currently reported as a feature, not a bug).
4. Standing items unchanged from v8: a genuinely new [V]-master+crisp-stage timing feature (the clean
   set is saturated at n=10); expression-onset/chromatin modality for the timing line; life-course
   kg/BMI calibration; GWAS sign/magnitude; size law on a real scan; [F]→[V] upgrades.
