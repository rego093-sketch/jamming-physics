# LEDGER — gene-clock feature emergence (Layer 3 ⟂ DNA framework)

Grading discipline borrowed from the neuro VP-SPEC (C3): every quantity is either a **measured
input** (locked + cited) or a **derived value** — never a number chosen to hit a target. Each
open item names its obstacle. Grades: **[V]** simulation/cross-package verified · **[F]** forced
modelling choice · **[O]** open (absolute scale needs external calibration) · **[L]** locked
measured input.

## What this upgrade is
It replaces the single global low-pass schedule `σ(τ)` in `grow_to_target.grow` with a
**per-feature schedule from the gene engine**: each external feature switches on at a
developmental time `τ_on` set by **its own master gene's R19 spinodal** (from real measured γ),
and reads a relative size from that gene's **dwell ∝ γ^1.5**. This is HANDOFF priority #3 ("drive
the coarse-to-fine schedule from Layer-1 switches so the *order* of feature appearance is itself
emergent — heterochrony") and it re-unites Layer 3 with the DNA framework.

## Quantity-by-quantity

| quantity | grade | basis |
|---|---|---|
| `spinodal(γ) = 2(γ/3)^1.5` is the SAME function in the neuro engine and the body engine `morpho_core.spinodal` | **[V]** | asserted `max|Δ| = 2.2e-16 < 1e-12` at run time (`assert_one_switch`); `3^1.5 ≡ 3√3`. The two frameworks share **one switch**. |
| γ per gene (PAX6, PAX2, LHX2, FOXG1, SHH, MYOD1, POU2F3, TP63 …) | **[L]** | `mean(−NN stacking ΔG37)`, SantaLucia 1998, read **verbatim** from NCBI promoter sequences (`data/sensory_organ_gamma.json`, corr(γ,GC)=0.994). **Never fitted here.** |
| emergence **ORDER** of features | **[V]** (derived) | equals `argsort(spinodal(γ))` exactly (`order_is_gamma_readout = True`). It is a **pure readout of measured γ**, not a hand-typed list — change a γ and the order changes with it (`dna_sensitivity` test). This is the same spinodal-ordering mechanism that reproduces the **measured spinal ventral→dorsal order** in neuro §17, here applied in the **time** axis. |
| onset **sharpness** of each feature | **[V]** (derived) | the R19 fold turns the smooth temporal clock into a crisp switch; width set by the gene's barrier `γ²/4` (stiffer gene → sharper onset). |
| convergence (form **reaches the scan**) | **[V]** fit-to-scan · **[O]** as realized emergence | global surface RMS 2.31 → **0.055**, Chamfer → **0.000** at the demo resolution; per-feature RMS → 0 as each feature emerges. The reschedule preserves the headline proof. **Phase-4 re-label (numbers unchanged):** these verify *target-fitting geometry* — the **scan supplies the coordinates** (`grow_to_target` header: "the scan sets the individual's coordinates") and **no systemic parameter** (dynamics/dosage) produced the realized shape, so *as shape emergence* this is **[O]**. The only axis that realized shape from a measured systemic parameter is `form(P,E)` dosage — H²=0.51 [L] (`morpho_decomposition.py`); see `LEDGER_systemic_recovery.md`. |
| determinism | **[V]** | 2× run → identical sha256 of the schedule+order+convergence payload. |
| **sign convention** (higher spinodal → later `τ_on`) | **[F]** | the neuro `Organ.functional_spinodal` convention. **Flipping the sign flips the order** (documented), exactly as a flipped Shh threshold flips the spinal order. We do **not** claim this direction matches measured craniofacial timing. |
| absolute developmental **time window** `[τ0, τ1]` the order is displayed on | **[F]** | a presentation scale. Only the **order** and the **relative spacing ratios** (preserved by the affine `τ_on` map) are claimed; the absolute `τ_on_raw = spinodal/Dmax` is reported but graded [O]. |
| feature → gene **map** for sensory features (eye=PAX6, ear=PAX2, nose/olfactory=LHX2, skin=TP63) | **[V]** | genuine master genes for those structures. |
| feature → gene map for **structural** groups (cranium=FOXG1, jaw/midline=SHH, cheek=MYOD1, lips/oral=POU2F3) | **[F]** | representative (forebrain underlies the vault; SHH patterns the facial midline; etc.), labelled per feature in `feature_target.py`. A cleaner neural-crest skeletal master set would upgrade these to [V] if sourced. |
| absolute feature **sizes** from `dwell ∝ γ^1.5` | **[O]** | the relative size *law* is reported; the analytic stand-in face's sizes are hand-built and not gene-set, so we do **not** claim size validation. On a real scan one would test `corr(size, γ^1.5)`. The hook is present. |

## What is explicitly NOT claimed
- **Not** a genome→face prediction. γ sets the **schedule** (order, relative timing, onset
  sharpness, relative size law), not the individual's coordinates — those still come from the scan.
  This is the honest leap still open (HANDOFF "real aim").
- **Not** a tissue-mechanics simulation. Growth is still a coarse-to-fine SDF morph; what changed
  is that the *path* is now gene-scheduled rather than a single hand-set σ(τ).
- **Not** a claim that the derived order matches measured developmental timing. The claim is that
  the order is a **deterministic function of measured DNA** — falsifiable, and it resorts when γ
  is perturbed.

## Invariants to preserve (add to the package's existing list)
- `gene_clock.assert_one_switch()` must stay `< 1e-12` (the neuro fold == the body fold).
- γ values are **read-only measured**; never tune a γ to change an order.
- The final τ=1 state must remain the full target (so convergence → 0); the gene clock only
  reschedules the path.

---

## v3 addendum — expanded atlas (head detail + bird/quadruped/fish), table grown 26 → 42

Same discipline: every γ is a **measured input** read by the pipeline; nothing was tuned to make
an order come out nicely. The verifier (`verify_morpho_plus.py`) enforces it.

### New measured γ (16 genes) — grade [L]
`EDAR, FOXN1, LEF1, FGF5, HOXC13, MITF, TYR, PAX9, MSX1, TBX5, TBX4, FGF8, HOXD13, GLI3, BMP4, SOX9`,
each `mean(−NN stacking ΔG37)` (SantaLucia 1998) read verbatim from NCBI promoter sequences via the
**identical** fetch used for the original set (`data/fetch_morpho_gamma.py`), corr(γ,GC)=0.997,
provenance (accession/strand) stored in `data/morpho_promoters.cache.json`. **[L]**
Original 26 kept **bit-for-bit** (verifier check #2: 0 value drift, and == neuro table). **[V]**

### New feature → gene maps
| group | genes | grade | basis |
|---|---|---|---|
| **limb identity** fore vs hind (wings/forelegs/pectoral = TBX5; legs/hindlegs/pelvic = TBX4) | TBX5, TBX4 | **[V]** | the textbook *Tbx5*/*Tbx4* forelimb/hindlimb identity split — genuine masters. |
| **digits** (feet/paws) | HOXD13 | **[V]** | *Hoxd13* is a genuine autopod/digit master. |
| **iris pigment** | MITF | **[V]** | *Mitf* is the master regulator of melanocyte/pigment cell fate. |
| **hair/skin appendage placode** (scalp hair, feathers, coat, scales) | EDAR | **[V]** for placode initiation; the **shaft/coat geometry** tag is **[F]** | *Edar* genuinely initiates ectodermal appendage placodes; using it for the *rendered shaft/coat shape* is a representative stand-in. |
| **eyebrow / hair-shaft keratin** | FOXN1, HOXC13 | **[F]** | both act in the hair/nail keratin program (genuine pathway members), used here as representative shaft masters rather than eyebrow-specific regulators. |
| **teeth** | PAX9 | **[V]** | *Pax9* is a genuine tooth-germ master (with *Msx1*). |
| **beak** | BMP4 | **[F]** (genuine pathway) | *Bmp4* dosage genuinely tunes beak depth/width (Darwin's-finch work); as a single "beak master" it is representative. |
| **gills / operculum / cartilage / horns** | SOX9 | **[F]** (genuine pathway) | *Sox9* is the genuine chondrogenesis master; mapping it to the whole gill/operculum/horn *structure* is representative. |
| **whiskers** | LEF1 | **[F]** | *Lef1* is required for whisker/vibrissa follicles (genuine), used as the representative whisker tag. |
| philtrum/median, body axis, tongue, neck (SHH/POU2F3) | — | **[F]** | representative, as in the base ledger. |

### Derived claims for the expanded atlas
| quantity | grade | basis |
|---|---|---|
| emergence **ORDER** for **each** of the 4 organisms = `argsort(spinodal(γ))` | **[V]** (derived) | `order_is_gamma_readout = True` for human_head/bird/quadruped/fish (verifier check #3). Pure γ readout, not hand-typed. |
| **DNA sensitivity** (perturb one γ → order resorts) for each organism | **[V]** (derived) | `dna_sensitivity` in `demo_morpho_plus.py`: e.g. lowering TBX4 γ moves hind-limb/pelvic-fin appearance from last toward first, deterministically, for bird/quadruped/fish; LHX2 for the head nose. |
| **convergence** to the scan for each organism | **[V]** fit-to-scan · **[O]** as realized emergence | Chamfer → 0.0000 and all features present at τ=1 for all four (verifier check #4); head RMS→0.06, bird→0.08, quadruped→0.10, fish→0.07. **Phase-4 re-label (numbers unchanged):** target-fitting geometry [V] — the scan supplies the coordinates and no systemic parameter realizes the shape, so *as emergence* this is **[O]** (contrast `form(P,E)` dosage, H²=0.51 [L]). |
| **mesh determinism** | **[V]** | growing an organism twice → identical sha256 of its vertex set (verifier check #5), in addition to schedule-hash determinism. |
| crisp **render** (gene-coloured triangles) | **[F]** | a deterministic painter's-algorithm rasterizer for visualization; not a physical light-transport claim. |

### Still NOT claimed (unchanged, important)
- **Not** that any emergence order matches **measured** developmental timing. The claim remains:
  the order is a **deterministic, falsifiable function of measured DNA**, and it resorts when a γ
  is perturbed. Calibrating τ_on against Carnegie-stage/somite data is the open **[O]** next step.
- **Not** a genome→coordinate prediction. γ sets the **schedule** (order, relative timing/spacing,
  onset sharpness, relative-size *law*); the **scan** sets the coordinates.
- Representative **[F]** structural/appendage tags above are honest stand-ins, not claims that the
  single named gene is the sole regulator of that whole rendered structure.
