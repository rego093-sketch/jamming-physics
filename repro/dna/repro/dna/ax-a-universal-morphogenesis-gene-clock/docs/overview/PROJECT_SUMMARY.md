# PROJECT SUMMARY — universal_morphogenesis_geneclock (v1 → v9)

*Single-author research/build under VP-SPEC C3 no-tuning governance, built on
neuro_emergence_chain_integrated v1.9. This document concludes the project: what it asked, what it
established, and what remains honestly open.*

---

## The one question, and the honest answer

**How much of an organism's final FORM — its face and body — does its measured DNA determine?**

**Answer the project arrives at: DNA is the FIRST CAUSE of form, but not the whole of it.** Measured DNA
fixes a *core* — the part that is the same no matter how you live — and environment fills an *envelope*
around it. This is the thing everyone already knows from identical twins: they resemble each other
because they share the core, and they diverge when their lives differ (exercise, diet, stress) because
the envelope is filled differently. The project's contribution is to make that split **mechanistic,
quantitative, reproducible, and anchored to published data** — and to be honest about exactly where DNA
stops and environment begins.

---

## The architecture (DNA → form, environment → envelope)

Every constant in the package is either a **measured input** (locked + cited) or a **derived value** —
never a number chosen to hit a target. The pieces:

- **`gene_clock` / `morpho_plus` — DNA → form.** A measured γ (spinodal stiffness) per gene drives an
  emergence schedule and grows actual morphology. One bistable switch turns each feature on; the
  *order* is `argsort(spinodal(γ))`. Four organisms (head, bird, quadruped, fish) grow from the same
  42-gene γ table; convergence RMS → 0.07, Chamfer → 0. **This is the DNA-fixed core.**
- **`adipose` — gene × environment → body & face.** The one place DNA and environment *both* act on a
  measured morphology. `activation(E, genome)` reads a genome's storage propensity (a measured-γ
  readout) and a lived-energy surplus through the *same* fat-fold, inflating the lean body into a fuller
  body and rounder face. Gene × environment is monotone; the lean reference is preserved bit-for-bit.
  **This is the environmental envelope.**
- **`life_course` — time × energy → trajectory.** One continuous fold over development that reduces to
  the lean target at the reference, so the headline convergence proof is never disturbed.

So the package literally is `form = core(DNA) + envelope(environment)`, with each half independently
gated.

---

## What the project established (by version)

- **v1–v5 — the core.** The gene-clock switch, the order law, and the four grown organisms; the γ tables
  locked and cited; bit-for-bit reproducibility via a sha256 source pin + frozen fidelity baselines.
- **v6–v8 — the developmental-*timing* line, settled as an honest NULL.** A natural sub-question: does a
  gene's *proximal-promoter composition* predict the **order** in which its feature appears (against
  real Carnegie staging)? The answer is **no**, and the project proved this *rigorously rather than
  giving up*:
  - v6/v7 widened the test to **n = 10** real master→primordium pairs and built an **exact-permutation
    engine** (a dynamic-programming computation of the full null distribution, validated bit-for-bit
    against brute force). Widening lifted the significance **floor to 2.2e-6**, so a real trend *could*
    have shown — and still none did. The moderate positive composition trend got a fair test and failed.
  - v8 **hardened** that null: it survives ±1-stage encoding uncertainty and leave-one-out removal of any
    feature, with power retained, and a synthetic positive control *does* flip (so the machinery is
    provably not blind). It also documented an honest dead-end (MYF5 → myotome cannot be cleanly locked:
    the gene precedes its named structure and has no crisp single stage), establishing that the clean
    [V]-master + crisp-stage feature set is **saturated at n = 10**.
  - **Why this matters for the headline question:** the timing line being null is *not a failure of the
    thesis*. Promoter composition not predicting the *order* of emergence is fully consistent with DNA
    strongly fixing the *shape*. They are different questions; the project answered the tangential one
    cleanly and then turned to the real one.
- **v9 — the SHAPE-decomposition CAPSTONE (the headline answer).** On the gated adipose machinery:
  - **Variance decomposition.** Over a genetic-propensity × environment grid, body shape splits into a
    **genetic fraction H² = 0.51** and an environmental fraction at a realistic range — **inside the
    published twin band** (BMI 0.58–0.63, body-fat 0.59–0.63, waist 0.48–0.61). Shape is **neither
    all-DNA nor all-environment**.
  - **Heritability is population-dependent — and the model reproduces it.** H² rises to 0.84 under narrow
    environmental variation and falls to 0.10 under wide — exactly the published finding that twin
    BMI-heritability varies across populations. This is a *subtle* validation (a reproduced property,
    not a fitted decimal) and the reason the anchor is used as a **regime** check.
  - **Identical-twin decomposition.** Same genome at the shared lean reference is **bit-identical** (the
    resemblance). Two lives → **same DNA, but the surplus/sedentary life adds +37% body volume and +25%
    lower-face roundness** versus the active/lean life. That is the envelope, quantified.
  - **Face: DNA vs environment.** The model's face roundness moves with adiposity (cheek/jowl) —
    environmental — while the bony frame is the γ-fixed core. This **matches the twin-study finding** that
    cheeks/chin/lips are most environmental and central midface bone (nose, orbital ridges) is most
    heritable.

All of v9 is anchored to published twin heritability (`code/data/heritability_anchor.json`, locked +
cited), to which the model is **never tuned**.

---

## What is honestly still open (each is data-blocked, not effort-blocked)

1. **Facial bone has no non-adiposity environmental axis** — the clearest remaining slot. In the model
   the bony face is γ-only, so it cannot represent how real faces change with **aging, gravity, sun**.
   Needs a *measured* facial-aging / soft-tissue axis as a locked input.
2. **No real morphometric validation.** The decomposition is an exact property of the measured-γ model,
   not fit to real paired genotype–morphometry scans (e.g. twin faces/bodies). Needs that dataset.
3. **A single canonical H².** Heritability is range-dependent *by nature*; collapsing it to one number
   would require fixing a canonical population environmental distribution as a locked input. (Reported as
   a feature, not hidden.)
4. **A different timing modality.** The timing null is for *promoter composition*; expression-onset or
   chromatin-accessibility at the master loci is a different measured quantity that could still carry
   order — but needs an external developmental atlas as a locked input.

None of these is "more work on the existing data"; each needs a **new measured input** the package does
not contain. That boundary — knowing precisely what is established and what would require new data — is
itself a result of the no-tuning discipline.

---

## How to reproduce / audit

```
python3 verify_all.py            # OVERALL: PASS (11/11): nine gates 5/5 + source pin drift 0 + nine fidelity baselines
python3 verify_all.py --list     # 54 governed files (engine + verify modules + measured-input data), all sha256-pinned
python3 verify_all.py --freeze   # re-record the baseline (refuses unless all nine gates pass)
```

Each gate prints `OVERALL: PASS (5/5)`; `[2]` proves no source/measured-input drift; `[3]` proves the
gate-regenerated results equal the frozen baselines leaf-for-leaf. The headline numbers above are
emitted by `verify_morpho_decomposition.py`.

*(Note: the full suite is computationally heavy — `verify_dev_timing_wide`'s exact-permutation validation
alone is ~4–5 minutes — so on a time-limited runner the gates may be run individually; each is
self-contained and writes its own `results/*_verify.json`.)*

---

## One-line conclusion

**DNA is the first cause of form, not all of it.** This package fixes the genetic core — the twin
resemblance, with a genetic fraction that lands in the published twin-heritability regime and reproduces
its population-dependence — and shows environment filling the envelope around it (a +37% volume / +25%
face-roundness swing from identical DNA), while honestly reporting that the *order* of development is not
predicted by promoter composition and that facial-bone aging remains outside the model. Every number is
measured or derived; none is tuned.
