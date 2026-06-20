# Universal Morphogenesis — grow any animal (and a human face) to scanned 3D coordinates

> ## INTEGRATED LAW — systemic-parameter shape emergence · *(v1.9.1 systemic-recovery fold-in — claim-strip)*
>
> **Intrinsic promoter-stiffness γ deterministically fixes WHAT structure forms and in WHICH ORDER
> [V]. But WHEN it forms and HOW LARGE it grows is a *systemic, relational* quantity that no static
> genomic scalar can carry. Supply the systemic parameter — time = dynamics, size = dosage — and the
> realized quantity is recovered: graded [L] if that parameter is *measured*, [F] if *model-only*, [O]
> if *absent*.** This re-reads Appendix A's measured null (γ predicts neither developmental *timing*
> nor *absolute size*) as a **boundary**, then fills past it with provenance-graded systemic parameters
> under strict no-tuning — the engine never reads a validation target (NON-FIT invariant), so a DB
> value is [L], never back-fit.
>
> | axis | intrinsic γ | systemic parameter | grade |
> |---|---|---|---|
> | emergence **order** | `argsort(spinodal γ)` | — | **[V]** |
> | timing (relative order) | null (ρ=0.07) | relay network topology | **[F]** recovered (ρ=0.44, core 0.85) |
> | timing **absolute clock** | — | measured protein half-life (Schwanhäusser 2011) | **[L]**-grounded *(Phase 1)* |
> | **body / face shape** | dwell core | E (lifestyle-energy **dosage**) | **[L]** H²=0.51, twin +37% |
> | organ ratio-change (growth) | — | cited allometric exponent | **[L]-grounded** (widened n=11: ρ=0.80, exact p=0.0047; pre-registered set) |
> | organ **absolute mass** | dwell null (ρ=0.11) | measured coefficient / growth atlas | **[O]** |
> | continuum **3-D trajectory** (positional info) | — | measured morphogen D·τ → λ=√(Dτ) | **[L]**-scale (λ=60 µm) / partition·form **[F]** *(Phase 3)* |
> | morphogen **length-scale** (band vs real gradients) | — | 6 directly-measured gradient λ (Bicoid/Nodal/Fgf8/Dpp/Shh/Wg) | **[L]-grounded** (geom-mean factor 1.91 < 3, 5/6 in band, independent set 3/3; *Phase 7*) |
> | exact anatomy (cell resolution) | — | measured tissue mechanics + HPC | **[O]** (back-fit forbidden) |
>
> **Verification.** The folded-in emergence gates pass `7/7 · 6/6 · 7/7 · 8/8 · 8/8`
> (`code/emergence_v2/verify_emergence{,_organs,_trajectory,_organs_wide,_morphogen}.py`), wired into
> the single-entry `verify_all.py` (**OVERALL: PASS 20/20**; pin 87 files, drift 0). Full grade ledger:
> `LEDGER_systemic_recovery.md` (+ `LEDGER_organ_allometry_wide.md`, `LEDGER_morphogen_length.md`). The
> old `grow_to_target` scan-convergence is re-labelled
> **target-fitting geometry [V], *not* realized shape emergence [O]** (numbers unchanged). DOI of
> record **10.5281/zenodo.20471407** (maintained; living-version snapshot). §1–§13 body, engine, γ
> tables and null values are **unchanged** — this strip is add-only.

> **v5 (this release)** adds two things on top of Layer 4, both **add-only** and **no-tuning** (all five gates stay green): **(1)** a **developmental-timing calibration** that finally *tests* the framework's open question — does measured promoter-stiffness γ predict real human-embryo (Carnegie) staging? — and reports the **honest answer (it does not: ρ=−0.018, permutation p=0.99)**, downgrading the order claim from an untested hedge to a *measured* result; and **(2)** a **life-course coupling** that runs the gene clock (TIME) and the adipose fold (ENERGY) **together on one genome** as a single continuous R19 fold — child → adult → heavier adult. See the **v5** section below, `LEDGER_dev_timing.md`, `LEDGER_life_course.md`, `verify_dev_timing.py`, and `verify_life_course.py`.
>
> *Prior:* **v4** added **Layer 4 — adipose / energy-balance morphology**: one genome made lean ↔ heavy in the face and body, driven by measured obesity-gene γ + an energy dial, using the same R19 fold (`LEDGER_adipose.md`, `verify_adipose.py`).


A developmental engine that starts from an egg and grows an organism's **external form**,
driven by the DNA-whitepaper framework (the **R19 bistable switch** + **γ** material
stiffness + a **segmentation clock**). On top of the generic engine sits a **target-driven
growth** layer: give it a real entity captured as 3D coordinates (a "scan"), and the form
**develops into those coordinates**, coarse-to-fine, with features (nose, ears, limbs…)
appearing as detail sharpens.

> **Goal (the bold one):** one logic that demonstrates most animals and ultimately predicts
> a human face. This is, in effect, a *developmental morphable model*: a biologically-seeded
> deformable template fit to any target body plan.

This snapshot already grows to **fish · bird · quadruped · human face** from one engine,
with surface error → 0 in every case (see `results/universal_growth.png`).

---

## The three layers

```
   DNA / γ  ─────────────►  LAYER 1   emergent generic engine        engine: morpho_core, develop, body, assemble
   (NN stacking ΔG)         · R19 switch sharpens morphogen
                              gradients into body-plan registers
                            · segmentation clock -> somite count
                            · digit clock -> 4/5 urodele formula
                            · metamorphosis switch (fin↔limb)
                                     │
                                     ▼
                            LAYER 2   solid anatomy (bones+organs)    engine: anatomy
                            · vertebrae = somite count (1 per segment)
                            · ribs, skull, limb long-bones + phalanges
                            · viscera fill the cavity (heart/lung/liver/gut)
                            · whole body tissue-typed (muscle/bone/organ/skin)
                            · uint8 labels + bbox culling  → 300–420× vs naive
                                     │
                                     ▼
   SCAN (3D coords) ───────► LAYER 3   target-driven growth            growth: target, targets_zoo, grow_to_target
   (SDF + landmarks)        · coarse-to-fine convergence of the
                              generic form onto the scan
                            · features emerge as σ shrinks
                            · convergence measured (RMS, Chamfer → 0)
```

### Layer 1 — emergent generic engine  (`code/morpho_core.py, develop.py, body.py, assemble.py`)
The on-thesis content of the DNA framework, all deterministic & reproducible:
- **`morpho_core.settle_field`** — the R19 cusp/fold switch as a vectorised field, validated
  bit-for-bit against the in-package `organism/core.py` (max |Δ| = 4.4e-16).
- **`develop.emergent_registers`** — two opposing morphogen gradients read through the fold
  give sharp AP body-plan boundaries (head 21% / trunk / tail 52%), limb stations.
- **`develop.somite_count`** — a relaxation oscillator built on `core`'s **own cubic** is the
  segmentation clock; count scales with axis length **and** with γ (stiffer → fewer somites).
- **`develop.digit_count`** — a faster distal clock; the larger hindlimb fits one more digit,
  so the classic **urodele 4-fingers / 5-toes** formula emerges.
- **`assemble.build_body`** — maps registers + clocks + a metamorphosis switch onto an
  implicit (SDF) salamander, egg → adult (`results/stage_series.png`).

### Layer 2 — solid anatomy  (`code/anatomy.py`)
Fills the body with rough internal structure so it is a *solid, tissue-typed* organism:
- vertebral column with **one vertebra per somite** (the same emergent count), ribs, skull,
  limb long-bones + phalanges (`results/skeleton_check.png`).
- viscera ellipsoids tiling the trunk cavity; leftover interior → segmented muscle, shell → skin.
- **Optimization (the "volume game"):** a `uint8` label volume (not float SDF per part) +
  **per-part bounding-box culling**, so cost ~ Σ(part bbox volumes), not parts × grid. Adding
  88 internal parts costs **35 ms** optimized vs **11 s** naive — **~310–420× faster, identical
  output** (`results/load_anatomy.png`). More small parts make culling *better*, not worse.

### Layer 3 — target-driven growth  (`code/target.py, targets_zoo.py, grow_to_target.py`)
- a **Target** = a signed-distance field `sample(P)` (negative inside) + semantic `landmarks`.
  `face_target()` is an analytic human head (cranium, brow, nose, eyes, cheeks, ears, lips,
  chin); `targets_zoo.py` has fish/bird/quadruped; `animal_target()` reuses Layer-1 bodies.
- **`grow_to_target.grow`** runs developmental time τ∈[0,1]: the target SDF is low-pass
  filtered to scale σ(τ) (large early → only the gross blob; →0 late → full detail) and blended
  with the starting egg by a(τ). The moving zero-level-set is the growing organism; **features
  appear as σ passes their size**. DNA/γ sets the egg's size; the scan sets the coordinates.
- **Convergence** (both → 0 as the form reaches the scan): `surface_rms` = RMS of the true
  target SDF sampled on the grown surface; `chamfer` = symmetric nearest-point distance.

> **Phase-4 re-label — target-fitting geometry, NOT realized shape emergence (numbers unchanged).**
> The Layer-3 convergence (global RMS 2.31 → 0.055, Chamfer → 0.000; per-organism head 0.06 / bird
> 0.08 / quadruped 0.10 / fish 0.07) is real and **[V] as a geometric fit to a supplied scan** — but
> the **scan supplies the coordinates** and **no systemic parameter** (timing dynamics or dosage)
> produced the realized form, so *as shape emergence* it is graded **[O]**. In the systemic-recovery
> framing (`LEDGER_systemic_recovery.md`), the only axis whose realized shape comes from a *measured
> systemic parameter* is the gene×environment fat-fold `form(P,E)` driven by lifestyle-energy
> **dosage** (variance decomposition H²=0.51, twin-anchored [L]; `morpho_decomposition.py`). The
> gene-clock still fixes the **order/identity** of features deterministically [V]; what Layer-3 does
> *not* establish is that any DNA-or-systemic quantity realized the **coordinates** — those came from
> the scan.

### Layer 3 ⟂ DNA — gene-clock feature emergence  (`code/gene_clock.py, feature_target.py, grow_gene_clock.py`)
**The upgrade that re-couples Layer 3 to the DNA framework** (HANDOFF priority #3). The original
growth uses one *global* low-pass `σ(τ)`, so features emerge purely by physical size — no biology
in the *order*. This layer replaces that with a **per-feature schedule driven by measured genes**:

- Each external feature is tagged with its **master gene** (eye=PAX6, ear=PAX2, nose/olfactory=
  LHX2, skin=TP63 are genuine masters; cranium/jaw/cheek/lips use representative genes, labelled).
- Each feature switches on at a developmental time **`τ_on` set by its gene's R19 spinodal**
  (`spinodal(γ)=2(γ/3)^1.5`) read from **real measured γ** (`mean(−NN ΔG37)`, SantaLucia 1998,
  from NCBI promoters; corr(γ,GC)=0.994). The R19 *fold* makes each onset **sharp** (smooth clock
  → crisp appearance), with width set by the gene's barrier `γ²/4`. Relative size reads from
  **dwell ∝ γ^1.5**.
- **One switch across the whole chain.** The spinodal here is *identical* to the body engine's
  `morpho_core.spinodal` **and** the neuro emergence engine's `Organ.functional_spinodal`
  (`max|Δ| = 2.2e-16`, asserted at run time). Coupling the neuro gene engine to morphogenesis is
  not a bolt-on — it is **the same R19 primitive** that writes DNA, fires neurons, and folds the
  body, now scheduling facial development.
- **The emergence ORDER is a readout of DNA**: it equals `argsort(spinodal(γ))` exactly, and it
  **resorts when a γ is perturbed** (the `dna_sensitivity` test moves nose earlier by lowering
  LHX2's γ). This is the *same spinodal-ordering mechanism* that reproduces the **measured spinal
  ventral→dorsal order** in the neuro package (§17), here applied in the **time** axis.
- Convergence is preserved (the reschedule only changes the path): global surface RMS 2.31 →
  **0.055**, Chamfer → **0.000**, and **per-feature** RMS → 0 as each feature reaches its
  coordinates. Verified by a neuro-style gate: **`verify_gene_clock.py` → PASS (5/5)**.
- **General**: the same `gene_clock` + `grow_gene_clock` drive **face · quadruped · fish** from
  one engine (`demo_gene_clock_universal.py`), each with a γ-derived order and RMS→0.

Honest scope is in `LEDGER_gene_clock.md`: γ sets the *schedule* (order, relative timing, onset
sharpness, size law) — **not** the individual's coordinates (still from the scan) and **not** a
genome→face prediction; the sign convention and absolute time window are declared [F]/[O].

### Layer 4 ⟂ DNA — adipose / energy-balance morphology  (`code/adipose.py, adipose_atlas.py`)
**The composition axis: one genome made lean ↔ heavy.** The gene clock sets the *order and timing*
of features, but the single largest source of variation in an individual's *external* form — the
same genome looking lean vs heavy, **in the face and the body** — is body **composition**. Layer 4
adds that axis, with **no HPC and no learned data**:

- **Same R19 fold, in the energy axis.** An adipocyte's store-vs-mobilize set-point is bistable
  with hysteresis (a *defended* fat set-point), so it is modelled with the **identical**
  `morpho_core` fold (`assert_one_switch_adipose()` → `max|Δ| = 2.2e-16`). Adiposity is the **time
  clock's twin**: the face clock turns a smooth *temporal* drive into a crisp feature onset; the
  fat clock turns a smooth *energy* drive `E` into a defended storage set-point `α(E)`.
- **Obesity genes, measured the same way.** 17 obesity genes (PPARG, CEBPA, LPL, FTO, NPY, AGRP,
  GHRL, INSR, MC4R, LEP, LEPR, POMC, SIM1, BDNF, ADIPOQ, ADRB3, UCP1) were fetched from NCBI and
  reduced to γ by the **same** `mean(−NN ΔG37)` pipeline (corr(γ,GC)=**0.998**), extending the
  table **42 → 59 genes with the original 42 bit-for-bit untouched**. γ is **[L] measured, never
  fitted**; only each gene's pro-storage/satiety **sign** is a declared [F] label.
- **Gene × environment (the user's point).** The fold's drive is `drive = k_E·E + P_geno`, where
  `P_geno` is a **readout of measured obesity γ** (`propensity_is_gamma_readout = True`; neutral ≡
  0). A **thrifty** genome reaches the storage tipping point at **lower E** (gains readily); a
  **lean** genome resists. At a fixed energy, absolute adiposity is ordered **thrifty ≥ neutral ≥
  lean** (verified exactly on a 41-point E grid and by occupancy volume).
- **Where fat sits.** A `DepotMap` places subcutaneous fat on textbook anatomy (face: buccal pad,
  jowl, jawline; body: abdominal/visceral **android “apple”** vs gluteofemoral **gynoid “pear”**,
  mixed by `android∈[0,1]`), then inflates the lean surface by a spatially-varying thickness
  `t = t_max·α(E,genome)·depot(P)`. Depot geometry is declared **[F]**.
- **Human *and* animal.** The same axis is general: a **quadruped** grows a sagging belly + rump +
  dewlap; a **bird** lays down premigratory furcular/abdominal fat (`adipose_atlas.SCENES`).
- **The headline proof is untouched.** Neutral genome at `E_lean` → α ≡ 0 → thickness ≡ 0 → the
  inflated surface **equals the lean target bit-for-bit**, so Layer-3 convergence still holds.
  Two gates stay green: **`verify_adipose.py` → 5/5** *and* **`verify_morpho_plus.py` → 5/5**.

Honest scope is in `LEDGER_adipose.md`: the package claims the **adiposity index** (fractional
volume added) and the **laws** (monotone in `E`, ordered by genome) — **not** kilograms, BMI, or a
specific person's depot pattern ([O], needs anthropometric data), and **not** a genome→fat-mass
prediction (measured γ sets a *propensity*, not a mass).

---

## Headline results (in `results/`)

| figure | what it shows |
|---|---|
| `stage_series.png` | egg → neurula → tadpole → metamorphosis → adult salamander (Layer 1) |
| `load_profile.png` | adult build cost breakdown + load scales linearly with resolution |
| `skeleton_check.png` | emergent skeleton: 41 vertebrae (= 41 somites), ribs, skull, 4 limbs |
| `anatomy.png` | solid tissue-typed body: skeleton + cross-sections + volume table (84% differentiated) |
| `load_anatomy.png` | **adding 88 internal parts: 310× speedup, identical output** |
| `face_growth.png` | **egg grows into a scanned human face**, coarse-to-fine |
| `face_convergence.png` | surface RMS 2.3 → 0.05, Chamfer → 0.00 |
| `universal_growth.png` | **one engine → fish · bird · quadruped · human face**, RMS→0 each |
| `adipose_face.png` | **one genome, lean → heavy face**: cheeks/jowl/chin fill, fat glows, W:H 0.44→0.56 |
| `adipose_body.png` | **one genome, lean → heavy body**: belly + hips emerge, adiposity index 0→0.55 |
| `adipose_quadruped.png` | the composition axis is general: an animal grows belly + rump + dewlap |
| `adipose_gene_x_env.png` | **same energy, different obesity genome** → lean vs thrifty fat (AI 0.01 vs 0.55) |
| `life_course_face.png` | **one genome, one continuous fold**: round baby face → adult (TIME) → heavy (ENERGY) |
| `life_course_body.png` | the same life on the body: small child → grown adult → android belly fat (E↑) |

Key numbers: switch-field validation 4.4e-16 · somites scale 8→41 with body & γ ·
digits 4/5 · anatomy optimization ~310–420× · target convergence RMS→~0.05–0.11 on 4 targets.

---

## How to run

```bash
cd code
python3 stages.py            # Layer 1: egg→adult developmental series + per-stage timing
python3 profile_load.py      # Layer 1: cost breakdown + resolution sweep
python3 anatomy_figure.py    # Layer 2: skeleton + organs + cross-sections + volume + load
python3 demo_face.py         # Layer 3: grow an egg into the human-face scan + convergence
python3 demo_universal.py    # Layer 3: one engine grows to fish/bird/quadruped/face
python3 data/fetch_obesity_gamma.py  # Layer 4: fetch obesity-gene γ from NCBI (extends table 42→59; cached)
python3 demo_adipose.py      # Layer 4: lean→heavy face/body/animal sweeps + gene×environment figures
python3 verify_adipose.py    # Layer 4 gate → PASS (5/5); verify_morpho_plus.py stays 5/5
python3 dev_timing.py        # v5: test measured γ vs real Carnegie staging → honest null (ρ=-0.018, p=0.99)
python3 verify_dev_timing.py # v5 gate → PASS (5/5): grade == evidence (reported the truth)
python3 demo_life_course.py  # v5: render the child→adult→heavy life-course montage (face + body)
python3 verify_life_course.py# v5 gate → PASS (5/5): gene clock (TIME) × adipose (ENERGY) = one fold
```
Requires: numpy, scipy, scikit-image, matplotlib. All outputs are deterministic (analytic +
fixed seeds); the only RNG is the seeded switch-field validator.

---

## Plugging in a REAL scan (the whole point of Layer 3)

`grow()` only needs a `Target` with `sample(P)→signed distance` and `landmarks`. To use a real
3D scan (point cloud or mesh) instead of the analytic stand-ins:

```python
from scipy.spatial import cKDTree
class ScanTarget:
    def __init__(self, points, normals, landmarks, box):
        self.tree = cKDTree(points); self.pts = points; self.nrm = normals
        self.landmarks = landmarks; self.box = box; self.name = "scan"
    def sample(self, P):
        d, idx = self.tree.query(P.reshape(-1,3), k=1)         # nearest surface point
        sign = np.sign(np.einsum('ij,ij->i', P.reshape(-1,3)-self.pts[idx], self.nrm[idx]))
        return (d*sign).reshape(P.shape[:-1])                  # signed distance from the scan
```
Landmarks (nose tip, eye corners, ears…) come from any face/keypoint detector. Everything
downstream (coarse-to-fine growth, convergence metrics) is unchanged.

---

## Honest scope ([O] obstacles — what is demonstration vs. reproduced)

- **Reproduced / deterministic (Layer 1):** the switch decisions, the segmentation-clock somite
  count and its γ/length scaling, the digit formula, the metamorphosis switch event. These are
  the framework's on-thesis content and pass bit-for-bit determinism.
- **Principle-demonstration (Layers 2–3):** the *geometry* — radius profiles, organ shapes, the
  face surface, and the growth path — is a parametric/▼coarse-to-fine read-out, **not** a
  continuum tissue-mechanics simulation grown from cells, and **not** a genome→face prediction.
  The genome→morphogen-geometry→continuum-mechanics→shape map needs HPC-scale tissue mechanics;
  here the engine demonstrates the *principle* (positional information → registers → a form that
  can be driven onto any target) at illustrative resolution. "Predicting a human face from DNA"
  is the **aim**; what is shown is the *machinery* (a developmental template that provably
  reaches arbitrary scanned coordinates), not a learned genotype→face function.

See `HANDOFF.md` for the prioritized path from here to that aim.

---

## v5 — Developmental-timing calibration (an honest null) + life-course coupling

Two add-only deliverables on top of Layer 4. Neither edits the engine; every invariant above is
preserved by construction, and **all five gates pass 5/5** (`verify_gene_clock`, `verify_morpho_plus`,
`verify_adipose`, `verify_dev_timing`, `verify_life_course`).

### 1 · Developmental-timing calibration — *does measured γ predict real embryo timing?* (`code/dev_timing.py`)

From v1 the package was careful to claim only that emergence **order** is a deterministic γ function
(`order = argsort(spinodal(γ))`), and to **disclaim** any match to real developmental timing. v5
builds the apparatus to **test that disclaimer against data** — and reports whatever falls out, with
**zero tuning**.

- **Locked, cited input.** `data/dev_timing.json` pins the first-appearance **Carnegie stage** of 7
  genuine-master features to their master gene — otic placode (PAX2, CS9), optic vesicle (PAX6, CS10),
  upper-limb bud (TBX5, CS12), olfactory placode (LHX2, CS13), lower-limb bud (TBX4, CS13), digital
  rays (HOXD13, CS17), tooth germ (PAX9, CS18) — from O'Rahilly & Müller, Larsen's, and the UNSW Hill
  embryology atlas. It is **[L] measured, read-only, frozen by sha256**, and provably independent of γ.
- **The test.** `calibrate(γ)` computes the rank correlation between the package's own γ-derived
  schedule and the observed stage ordinal (Spearman ρ, exact n!=5040 permutation p, plus Pearson).
  The grade is set **by the evidence**: [V] only if `perm_p<0.05 AND ρ>0`, else [O].
- **The honest result.** **ρ(spinodal, observed CS) = −0.018, exact permutation p = 0.986** (Pearson
  r = −0.257, p = 0.58). Measured promoter stiffness is **evidently not** the molecular correlate of
  developmental timing. The order claim is therefore graded a **measured [O]** (tested-and-not-matching)
  — a **stronger, more honest** position than the prior untested hedge. *This is the governance working
  as intended: the central open claim got tested and the result is reported, not tuned away.*
- **The apparatus is not blind.** `apparatus_detects_signal()` feeds it a synthetic γ made proportional
  to stage → it recovers **ρ = 1.0 exactly**; a shuffle collapses it. So the null is a real null, not a
  broken test. `verify_dev_timing.py` enforces **grade == evidence** (PASS means "you reported the
  truth", *not* "the correlation was good" — requiring a good correlation would itself invite tuning).

### 2 · Life-course coupling — gene clock (TIME) × adipose (ENERGY) = one continuous fold (`code/life_course.py`)

Until v5 the time axis (gene clock) and the energy axis (adipose) ran in **separate** demos. v5 runs
them **together on one genome**, as a single individual lived forward:

```
(developmental time τ ∈ [0,1])   ×   (lifelong chronic energy E)
   gene clock: which features        adipose fold: how heavy the
   have emerged (the γ readout)       mature body is (α(E,genome))
```

- **One switch across the whole life.** `assert_one_continuous_fold()` proves the **time** fold and
  the **energy** fold are *both* the body fold: `max|spinodal − morpho_core.spinodal| = 2.2e-16 < 1e-12`
  for each. Child→adult→heavy is literally **one R19 process**, expressed first in time, then in energy.
- **One continuous trajectory.** `DevTarget` exposes the gene-clock body **frozen at τ** as a point-
  sampleable SDF (`(1−A)·egg + A·lean_body` with each feature scaled to its R19 emergence curve at τ);
  the adipose fold then inflates it by `α(E,genome)` over the anatomical depot. At τ=1 it is the **full
  lean target**, so Layer-3 convergence is untouched. `default_life()` walks infant → child →
  adolescent → adult-lean → adult-surplus → adult-heavy.
- **Baseline preserved bit-for-bit.** At the lean reference (`E_lean`, neutral) `α = 0` for the entire
  τ sweep, so the inflated field **equals the pure gene-clock field bit-for-bit** (`max|Δ| = 0`) — the
  energy axis perturbs nothing at lean.
- **The picture.** `demo_life_course.py` renders the montage (`results/life_course_face.png`,
  `results/life_course_body.png`): a round baby face (13/34 features) elongates to a full adult
  (34/34, α=0), then re-rounds as fat fills the buccal pad/jowl (α→1.0); the body grows small→adult
  then lays down android belly fat (waist:hip rises with E). `verify_life_course.py` checks one fold,
  measured-γ identity (gene-clock 42 bit-identical inside adipose 59), monotonicity (A↑ in τ,
  occupancy↑ in E), baseline preservation, and determinism → **PASS (5/5)**.

Honest grades for both are in `LEDGER_dev_timing.md` and `LEDGER_life_course.md`. Run:
```bash
cd code
python3 dev_timing.py          # prints ρ, permutation p, and the evidence-set grade ([O])
python3 verify_dev_timing.py   # gate → PASS (5/5): grade == evidence
python3 life_course.py         # prints the one-fold delta + the chosen-life trajectory
python3 demo_life_course.py    # renders the face + body life-course montages
python3 verify_life_course.py  # gate → PASS (5/5)
```

---

## v3 — Expanded gene-clock atlas (head detail + animals), measured table grown to 42 genes

This snapshot **widens the body scope** and **deepens the face**, while keeping every
invariant above intact (the verifier proves it).

**Deeper human head (34 features, 13 master genes).** On top of the original face it now grows
**scalp hair** (EDAR), **eyebrows** (FOXN1), **eyelashes** (HOXC13), **eyelids** (TP63),
**iris** (MITF), **philtrum/midline** (SHH), **teeth** (PAX9), **tongue** (POU2F3) and **neck**.
Each switches on at the developmental time set by *its own* gene's R19 spinodal.

**Three animals, gene-tagged.** `feature_atlas_plus.py` adds **bird** (beak=BMP4, wings=TBX5,
legs=TBX4, feet=HOXD13, crest/primaries/tail=EDAR, body=SHH), **quadruped** (forelegs=TBX5,
hindlegs=TBX4, paws=HOXD13, whiskers=LEF1, coat=EDAR, horns=SOX9) and **fish** (pectoral=TBX5,
pelvic=TBX4, median fins/caudal=SHH, gills/operculum=SOX9, scales=EDAR). Limb **identity** is the
real *Tbx5*(fore)/*Tbx4*(hind) split; digits are *Hoxd13*; these are genuine masters.

**Measured table grown 26 → 42 — still never fitted.** `data/morpho_gamma.json` keeps the
original 26 γ **bit-for-bit** and adds 16 new genes (EDAR, FOXN1, LEF1, FGF5, HOXC13, MITF, TYR,
PAX9, MSX1, TBX5, TBX4, FGF8, HOXD13, GLI3, BMP4, SOX9) fetched by the **same** NCBI→SantaLucia-NN
pipeline (`data/fetch_morpho_gamma.py`), corr(γ,GC)=0.997. The verifier checks the base 26 are
unperturbed (0 value drift) and still bit-identical to the neuro package.

**Crisp renders.** `render_plus.py` replaces the grainy z-buffer splat with a deterministic
painter's-algorithm flat-shaded **triangle** rasterizer; every surface patch is tinted by the
**master gene** that built it (legend in every figure).

**Emergence order is a DNA readout for each body** (order = `argsort(spinodal(γ))`, resorts under
a γ perturbation — the `dna_sensitivity` test moves a limb/nose gene and the order deterministically
re-sequences). All four converge to the scan (Chamfer → 0.0000):

| organism | features | genes | final RMS | Chamfer | emergence order (genes) |
|---|---|---|---|---|---|
| human head | 34 | 13 | 0.06 | 0.0000 | TP63>EDAR>MITF>POU2F3>SHH>FOXN1>PAX2>FOXG1>HOXC13>PAX9>MYOD1>PAX6>LHX2 |
| bird | 18 | 8 | 0.08 | 0.0000 | EDAR>BMP4>HOXD13>TBX5>SHH>FOXG1>PAX6>TBX4 |
| quadruped | 22 | 11 | 0.10 | 0.0000 | EDAR>LEF1>HOXD13>TBX5>SHH>SOX9>PAX2>FOXG1>PAX6>LHX2>TBX4 |
| fish | 15 | 7 | 0.07 | 0.0000 | EDAR>TBX5>SHH>SOX9>FOXG1>PAX6>TBX4 |

Run: `cd code && python3 demo_morpho_plus.py` (figures + `results/morpho_plus.json`), then
`python3 verify_morpho_plus.py` → **PASS (5/5)**. New modules: `feature_atlas_plus.py`,
`render_plus.py`, `demo_morpho_plus.py`, `verify_morpho_plus.py`, `data/fetch_morpho_gamma.py`,
`data/morpho_gamma.json`. Honest grades for the new genes are in `LEDGER_gene_clock.md`.

**On the developmental-timing question (now answered in v5):** whether this emergence order matches
*measured* developmental timing was the open [O] next step in v3. **v5 tests it directly** against
canonical human-embryo Carnegie staging and finds that measured promoter-stiffness γ **does not**
predict observed staging (Spearman ρ=−0.018, exact permutation p=0.99). That is reported as the
result — the order claim is now a *measured* [O] (tested, not matching), which is a stronger and
more honest position than the prior untested hedge. Details in the **v5** section and
`LEDGER_dev_timing.md`. **Still not claimed:** a genome→coordinate prediction (γ sets the schedule,
the scan sets the coordinates).
