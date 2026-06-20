# LEDGER — life-course coupling: gene clock (TIME) × adipose (ENERGY) (v5)

Grading discipline borrowed from the neuro VP-SPEC (C3): every quantity is either a **measured
input** (locked + cited) or a **derived value** — never a number chosen to hit a target. Each open
item names its obstacle. Grades: **[V]** simulation/cross-package verified · **[F]** forced
modelling choice · **[O]** open (absolute scale needs external calibration) · **[L]** locked
measured input.

## What this is
Two axes that until v5 lived in separate demos:

- the **gene clock** (Layer 3 ⟂ DNA) makes the **order/timing** of feature appearance a readout of
  measured γ — the **TIME** axis;
- the **adipose fold** (Layer 4) makes body **composition** (lean↔heavy) a readout of measured
  obesity-γ + an energy dial — the **ENERGY** axis.

v5 runs them **together on one genome**, as a single individual lived forward:

```
(developmental time τ ∈ [0,1])   ×   (lifelong chronic energy E)
```

At each life point the gene-clock body is built **frozen at τ** (which features have emerged is the
γ readout) and then **inflated** by the adipose fold's `α(E, genome)` over the anatomical depot. The
result is one continuous trajectory — small lean child → grown lean adult → grown heavier adult —
and the headline is that **both halves are literally the same R19 switch**, so child→adult→heavy is
**one fold** expressed first in time and then in energy.

This makes the unifying claim of the whole package concrete on a single individual: **one switch**
writes DNA, fires neurons, folds the body, schedules the face, **and** defends the fat set-point —
across a lifetime.

## Quantity-by-quantity

| quantity | grade | basis |
|---|---|---|
| the **TIME** fold (gene clock) and the **ENERGY** fold (adipose) are *both* the body fold | **[V]** | `assert_one_continuous_fold()`: `max|GC.spinodal − morpho_core.spinodal| = 2.2e-16` **and** `max|AD.spinodal − morpho_core.spinodal| = 2.2e-16`, both `< 1e-12` (`verify_life_course.py` check 1). **One switch across the whole life.** |
| γ (gene clock) and obesity-γ (adipose) | **[L]** | measured `mean(−NN ΔG37)` tables (`morpho_gamma.json` 42 genes, `obesity_gamma.json` 59), read-only. The coupling introduces **no** new constant. |
| the gene-clock 42-gene table is **bit-identical inside** the adipose 59-gene table | **[V]** | `verify_life_course.py` check 2 (`missing=0, moved=0`): composing the two axes drifted **no** measured value — no tuning entered through the back door. |
| developmental completeness `A(τ) = smoothstep(τ)` is **monotone non-decreasing** in τ | **[V]** (derived) | child→adult grows; verified over the lean τ sweep (check 3a). |
| adiposity **occupancy volume** is monotone non-decreasing in E at maturity (τ=1) | **[V]** (derived) | eat more → store more; verified `10141 ≤ 10720 ≤ 12849` over the surplus points (check 3b). |
| the emergence **order** over the life is still the measured-γ readout | **[V]** (derived) | `order_is_gamma_readout = True` (check 3c) — coupling did not disturb the γ ordering. |
| **baseline preserved**: at the lean reference (`E_lean`, neutral) `α = 0` for the **entire** τ sweep → inflated field **== pure gene-clock field bit-for-bit** | **[V]** | `verify_life_course.py` check 4: `max|α| = 0`, `max|field Δ| = 0`. The energy axis perturbs **nothing** at lean, so Layer-3 convergence survives untouched. |
| at τ=1 the developing body **== the full lean target** | **[V]** | `DevTarget` has `A=1` and every feature presence `=1` at τ≥1, so it reduces to the Layer-3 lean target — the convergence proof is intact by construction. |
| determinism | **[V]** | two independent trajectories → identical sha256 of the field payload (check 5). |
| `DevTarget` omits the **residual sub-feature low-pass** of `grow_gene_clock` | **[F]** | a cosmetic crispening only, and **0 at τ=1** anyway; dropped so the developing body stays a clean point-sampleable SDF for the adipose inflater. Declared, not hidden. |
| the **life schedule** `τ(t)` / `E(t)` in `default_life()` (infant→…→heavy) | **[F]** | a **chosen life**, an input — not a prediction of how a real person ages. The package claims the *machinery* (one continuous fold), not this particular itinerary. |
| the **depot map** is the adult anatomical map applied throughout life | **[F]** | a declared simplification: a real child's depot pattern differs from an adult's. The composition *axis* is general; the child-specific depot geometry is not modelled. |
| **real ages / BMI in absolute units**, and a specific person's trajectory | **[O]** | needs anthropometric/longitudinal data not fit here. Only the **laws** (A↑ in τ, occupancy↑ in E) and the **one-fold identity** are claimed. |

## What is explicitly NOT claimed
- **Not** a prediction of a real individual's life course. `default_life()` is a chosen schedule
  ([F]); the claim is that the *fold* is continuous and shared, not that this itinerary is real.
- **Not** absolute ages, weights, or BMI ([O]); only the monotone laws and orderings are claimed.
- **Not** a child-accurate depot map — adult depot geometry is reused throughout life ([F]).
- **Not** any re-tuning of upstream: the gene-clock order, the measured γ tables, and the Layer-3
  convergence proof are all preserved bit-for-bit (enforced by checks 2 and 4, and by the three
  upstream gates staying 5/5).

## Invariants to preserve
- `assert_one_continuous_fold()` must stay `< 1e-12` for **both** the TIME and ENERGY folds.
- the gene-clock 42 γ must stay **bit-identical** inside the adipose 59 (no value may drift when
  the axes are coupled).
- at the lean reference the trajectory must keep `α ≡ 0` and reproduce the pure gene-clock field
  **bit-for-bit**, so the headline convergence result never moves.
- at τ=1 `DevTarget` must reduce to the full lean target (do not let the developmental freeze leak
  into the converged adult).

## Reproduce
```
cd code
python3 life_course.py         # one-fold delta + the chosen-life trajectory (A, α, #emerged, volume)
python3 demo_life_course.py    # renders results/life_course_face.png and results/life_course_body.png
python3 verify_life_course.py  # 5/5 gate: one fold, measured-γ identity, monotone, baseline, determinism
```
Outputs: `results/life_course.json`, `results/life_course_face.png`, `results/life_course_body.png`,
and `results/life_course_verify.json`.
