# LEDGER — adipose / energy-balance morphology (Layer 4)

Grading discipline borrowed from the neuro VP-SPEC (C3): every quantity is either a **measured
input** (locked + cited) or a **derived value** — never a number chosen to hit a target. Each
open item names its obstacle. Grades: **[V]** simulation/cross-package verified · **[F]** forced
modelling choice · **[O]** open (absolute scale needs external calibration) · **[L]** locked
measured input.

## What this layer is
The gene clock (Layer 3 ⟂ DNA) makes the **order and timing** of feature appearance a readout of
measured γ. But the single largest source of variation in a real individual's *external* form —
the same genome looking **lean vs heavy, in the face and the body** — is body **composition**,
i.e. adipose deposition. Layer 4 adds exactly that axis, with **no HPC and no learned data**: an
analytic deformation field driven by

1. **measured obesity-gene γ** — the same NCBI → SantaLucia-NN pipeline that made the original
   table; **[L]**, never fitted;
2. an **energy-balance dial E** — chronic caloric surplus(+) / deficit(−); an **input**, not a fit;
3. an anatomical **depot map** — *where* fat sits (sex/pattern influenced); geometry is **[F]**.

The store-vs-mobilize set-point of an adipocyte is **bistable with hysteresis** (a defended fat
set-point), so it is modelled with the **same R19 fold** that writes DNA, fires neurons, folds the
body and schedules the face. Adiposity is therefore **the time clock's twin in the composition
axis**: the face clock turns a smooth *temporal* drive into a crisp feature onset; the fat clock
turns a smooth *energy* drive into a defended storage set-point.

## Quantity-by-quantity

| quantity | grade | basis |
|---|---|---|
| `spinodal(γ) = 2(γ/3)^1.5` of the adipose fold IS the body fold `morpho_core.spinodal` | **[V]** | `max|Δ| = 2.2e-16 < 1e-12` at run time (`assert_one_switch_adipose`, `verify_adipose.py` check 1). **One switch**, now also in the composition axis. |
| obesity-gene γ (PPARG, CEBPA, LPL, FTO, NPY, AGRP, GHRL, INSR, MC4R, LEP, LEPR, POMC, SIM1, BDNF, ADIPOQ, ADRB3, UCP1) | **[L]** | `mean(−NN stacking ΔG37)`, SantaLucia 1998, read **verbatim** from NCBI promoter sequences (TSS−2000..+500) into `data/obesity_gamma.json`; corr(γ,GC)=**0.998**. **Never fitted.** Cache: `data/obesity_promoters.cache.json`; fetcher: `data/fetch_obesity_gamma.py`. |
| γ-table **superset**: the original 42 genes are **bit-for-bit identical** inside the new 59 | **[V]** | `verify_adipose.py` check 2 (`missing=0, moved=0`); adding the obesity panel perturbed **no** measured base value. |
| **activation** `α(E, genome)` is monotone non-decreasing in `E` | **[V]** (derived) | the lower (lean) branch rises, jumps at the spinodal, the upper branch saturates — `adipose_setpoint`. Verified per genome (`verify_adipose.py` check 3a). |
| **gene × environment**: at fixed `E`, absolute adiposity is ordered **thrifty ≥ neutral ≥ lean** | **[V]** (derived) | a thriftier genome reaches the storage tipping point at lower `E`. Verified exactly on a 41-point `E` grid (activation) and by occupancy **volume** at fixed `E` (`10263 < 10615 < 12301`), check 3b. |
| **genome propensity** `P_geno` is a readout of measured γ | **[V]** (derived) | `propensity_is_gamma_readout = True`: perturb a pro-storage γ → propensity moves **+**, a satiety/thermogenic γ → **−** (annotated directions). Neutral propensity `≡ 0` by construction — a falsifiable anchor, not a tuned offset. |
| **baseline preserved**: neutral genome at `E_lean` → α `≡ 0` → thickness field `≡ 0` → inflated surface **== lean target bit-for-bit** | **[V]** | `verify_adipose.py` check 4 (sha256 of sampled fields match for face **and** body). The Layer-3 convergence proof is **untouched** by adding fat. |
| determinism | **[V]** | building the same inflated body twice → identical sha256 of the thickness field **and** of the mesh vertices (`verify_adipose.py` check 5). |
| the **sign** of each gene's adipose effect (pro-storage vs satiety/thermogenic) | **[F]** | `PANEL_SIGN` in `adipose.py`, from textbook adipocyte/melanocortin biology (PPARG/CEBPA/LPL/FTO drive storage; MC4R/LEP/LEPR/POMC/UCP1 oppose it). The **magnitude** each contributes is `spinodal(γ)` (measured); only the **sign label** is forced. Flipping a sign flips that gene's contribution (falsifiable). |
| **depot geometry** (where each subcutaneous pad sits: buccal, jowl, jawline, abdominal, gluteofemoral, dewlap, furcular …) | **[F]** | `adipose_atlas.py`, placed on textbook subcutaneous anatomy. Declared, not measured per individual. |
| `android ∈ [0,1]` apple↔pear mix (central/visceral vs gluteofemoral) and its **0.5/0.6 default** | **[F]** | sex/pattern influenced; the *contrast* (android WHR > gynoid WHR at equal energy) is a model property, but the default split is a forced choice. |
| max subcutaneous thickness `t_max` and the energy **window** `E ∈ [−1, 1]` | **[F]** | presentation scales for the deformation field; only the **monotonic laws** and **orderings** are claimed, not these magnitudes. |
| **absolute fat mass (kg), real BMI, person-specific depot pattern** | **[O]** | needs anthropometric/DXA data we do **not** fit here. The package claims the **adiposity index** (fractional volume added) and the **laws** (monotone in E, ordered by genome), not calibrated kilograms. |

## What is explicitly NOT claimed
- **Not** a genome → fat-mass prediction. Measured obesity γ sets a **propensity** (which way and
  how strongly the storage fold is biased), **not** an individual's kilograms or BMI.
- **Not** a metabolic simulation. There is no energy ODE; `E` is a single dial standing in for
  chronic balance, and the fold is the same algebraic R19 switch used everywhere else.
- **Not** a claim that the depot geometry matches a particular person. The depots are textbook
  anatomical placements ([F]); matching a specific individual's pattern is [O].
- **Not** a re-tuning of anything upstream. The original 42 γ, the emergence order, and the
  convergence proof are all preserved bit-for-bit (enforced by the two gates).

## Invariants to preserve (add to the package's existing list)
- `adipose.assert_one_switch_adipose()` must stay `< 1e-12` (the adipose fold == the body fold).
- obesity γ values are **read-only measured**; never tune a γ to move an adiposity result.
- neutral genome at `E_lean` must give α `≡ 0` so the inflated surface equals the lean target and
  the Layer-3 convergence proof survives (the headline result is not allowed to move).
- cross-genome ordering is on **absolute** adiposity (α / volume); self-referential AI is reserved
  for the **within-genome** energy sweep.

## Reproduce
```
cd code
python3 data/fetch_obesity_gamma.py     # re-fetch obesity γ from NCBI (extends the table; cached)
python3 demo_adipose.py                 # face/body/animal energy sweeps + gene×environment figures
python3 verify_adipose.py               # 5/5 Layer-4 gate
python3 verify_morpho_plus.py           # 5/5 — confirms Layer 4 did not perturb the gene clock
```
Outputs land in `code/results/` (`adipose_*.png`, `adipose.json`, `adipose_verify.json`).
