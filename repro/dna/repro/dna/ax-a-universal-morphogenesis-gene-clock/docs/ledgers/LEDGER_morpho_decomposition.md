# LEDGER — morphogenesis decomposition: how much of SHAPE does DNA fix? (v9 CAPSTONE)

Grading discipline borrowed from the neuro VP-SPEC (C3): every quantity is either a **measured
input** (locked + cited) or a **derived value** — never a number chosen to hit a target. Each open
item names its obstacle. Grades: **[V]** simulation/cross-package verified · **[F]** forced
modelling choice · **[O]** open (the claim was tested and is *not* established) · **[L]** locked
measured input.

## What this is
The project's headline question was never the developmental *order* of features (v6–v8, an honest robust
null) — it was **how much of the final FORM (face, body) measured DNA fixes**. The empirically obvious
answer, which the model is built to embody, is: **DNA is the FIRST CAUSE of form, but not the whole of
it.** Identical twins resemble each other yet diverge when their lives differ (exercise, diet, stress);
100% of the face does not come from DNA. v9 makes that decomposition **explicit and quantitative** on the
package's already-gated gene × environment machinery and anchors it to published twin heritability. It is
add-only: `morpho_decomposition.py` reuses public `adipose` primitives, **no engine edit**.

## The substrate (why adipose, and what enters where)
`AdiposeModel.activation(E, genome)` drives a spatially-varying fat field that inflates the lean target
into an actual body **and** face; the package already measures occupancy volume, waist:hip ratio, and a
lower-face width:height "roundness" index (cheek/jowl band). The genome enters **only** through its
scalar storage propensity `P = genome_propensity(gammas)` — a **measured-γ readout** (gated by
`propensity_is_gamma_readout`) — and the environment enters through chronic-surplus energy `E`. So the
form is `form(P, E)`: **P is the DNA axis, E is the lived-life axis.**

## Claims and grades

| # | Claim | Grade | Evidence |
|---|-------|-------|----------|
| 1 | Body shape decomposes into a substantial **genetic** fraction AND a substantial **environmental** fraction (neither ~0 nor ~100%). | **[V]** | Two-way variance decomposition of occupancy volume over a P×E grid at the reference range: **H² = 0.51, E² = 0.25, GxE+res = 0.25** (sum 1). Gate check 1. |
| 2 | The genetic fraction H² sits in the **published twin-heritability regime**, not a tuned decimal. | **[V]** vs **[L]** anchor | Reference H² = 0.51 ∈ published body-composition band [0.40, 0.85] (BMI 0.58–0.63, waist 0.48–0.61); model's achievable H² range [0.10, 0.84] overlaps the band. Gate check 2. |
| 3 | **Heritability is population-dependent** — H² falls as the population's environmental variation widens — and the model reproduces it. | **[V]** | H²(narrow env) = 0.84 > H²(ref) = 0.51 > H²(wide env) = 0.10, strictly. Matches the published fact (PMC4346225). This is *why* (2) is a regime check, not a decimal match. Gate check 2. |
| 4 | **Identical-twin core is DNA-fixed.** One genome at the shared lean reference is bit-identical between the twins (the resemblance). | **[V]** | Two independent builds of (same genome, E_lean) → identical sha256 of the mesh. Gate check 3. |
| 5 | **Environmental envelope.** Same DNA, two lives → the surplus/sedentary twin is measurably larger and rounder than the active/lean twin. | **[V]** | Surplus life adds **+37% body volume** and widens lower-face roundness by **+25%** from identical DNA; both move in the correct direction. Gate check 3. |
| 6 | The genetic axis is a **real measured-γ readout**, the fat fold **is** the body fold, and the lean baseline is **preserved**. | **[V]** / **[L]** | `propensity_is_gamma_readout` true (pro-storage γ↑ → propensity↑; satiety γ↑ → propensity↓); `assert_one_switch_adipose` < 1e-12; α(lean) ≈ 0 so the inflated field == the lean target (headline convergence untouched); explicit α == `model.activation` to 1e-9. Gate check 4. |
| 7 | **Face roundness is environmental; the bony frame is genetic** — matching twin studies. | **[V]** / **[L]** anchor | The model's lower-face W:H moves with adiposity (cheek/jowl), the bony frame is the γ-fixed core; twin 3D studies (Djordjevic 2016; Naini & Moss; Weinberg, PubMed 24501696) find cheeks/chin/lips most environmental and midface bone most heritable. Qualitative regime match. |
| 8 | The whole decomposition is **deterministic** and reproducible. | **[V]** | Two independent `analyze()` runs → identical result sha256 (21479bcc88…). Gate check 5. |

## Locked inputs (this session)
- **`code/data/heritability_anchor.json`** `[L]` — published twin-study H²: BMI 0.58–0.63, body-fat
  0.59–0.63, waist 0.48–0.61, hip 0.52–0.58, height 0.69–0.81 (Schousboe 2004, PubMed 14610529);
  children ≥0.80 (Silventoinen, PMC10023566); BMI population-dependence (systematic review, PMC4346225);
  facial pattern — midface bone genetic, cheeks/chin/lips environmental (Djordjevic 2016 PLoS One
  e0162250; Naini & Moss; Weinberg 3D twin, PubMed 24501696). Used as an order-of-magnitude **regime**
  anchor only; the model is **never tuned** to it, and the file states the population-variance caveat
  explicitly. Sha frozen in the gate.
- All γ tables and the adipose machinery are **unchanged** from v8 (source pin drift 0).

## Forced choices (disclosed)
- **Reference ranges** `[F]`: genetic propensity P ∈ [−0.9, 0.9] (the model's lean↔thrifty preset span);
  environmental surplus E reference [−0.6, 1.0], narrow [0.0, 0.5], wide [−1.2, 2.0]. These are declared
  *a priori* (the genetic span = the preset range), and the gate's heritability check is deliberately a
  **regime** test (both-substantial + overlap + range-dependence) rather than a value match, *because*
  H² is range-dependent — so the result is not gameable by the range choice.
- **Twin life energies** `[F]`: active twin E = −0.3, surplus twin E = +1.0 (a realistic chronic
  difference); the genome is `neutral`. The *direction* of divergence (surplus → larger/rounder) and the
  bit-identity of the shared core are what the gate enforces, not the exact percentages.
- **Adipose fold stiffness = PPARG γ** `[F]` (its value `[L]`), inherited unchanged from the adipose
  module.

## Open items (named, with obstacle)
1. **Facial BONE has no non-adiposity environmental axis** `[O]` — the clearest remaining slot. In the
   model the bony face is γ-only, so for aging/sun/gravity it trivially attributes 100% to DNA, which
   real faces do not. *Obstacle*: needs a **measured** facial-aging / soft-tissue-change axis as a
   locked input; none is in the package.
2. **Absolute H² is range-dependent** `[O] by design` — there is no single "true" model heritability,
   only an H²(environmental range); this is reported as a feature (it reproduces the population-
   dependence of real heritability), not hidden. *Obstacle to a single number*: would require fixing a
   canonical population environmental distribution as a locked input.
3. **No real morphometric validation** `[O]` — the decomposition is an exact property of the measured-γ
   model, not fit to real twin face/body scans. *Obstacle*: needs a paired genotype–morphometry dataset
   as a locked input; none is in the package. (Carried from the standing "[O] data modality" lever.)

## One-line verdict
**DNA is the first cause of form, not all of it.** The model fixes a core (the twin resemblance, H² in
the published regime) that environment fills around (the envelope: +37% volume / +25% face roundness from
identical DNA), and it reproduces the published population-dependence of heritability — reported, not
tuned.
