# CHANGELOG — universal_morphogenesis_geneclock v9 (CAPSTONE)

Built on neuro_emergence_chain_integrated v1.9 (VP-SPEC C3 no-tuning governance).
**Add-only, no engine edits, no fork of `organism/core.py`.** ONE new measured input: published
twin-study heritability (`code/data/heritability_anchor.json`), **locked + cited**, used only as an
order-of-magnitude REGIME anchor and **never tuned to** (and the model is never tuned to match it).
Unified entry `verify_all.py` now **PASS 11/11** (nine gates 5/5 + sha256 source/measured-input pin
drift 0 + nine fidelity baselines leaf drift 0).

## v9 — the SHAPE-decomposition capstone: how much of FORM does measured DNA fix?

The project spent v6–v8 on the developmental-timing sub-question (does proximal-promoter composition
predict the *order* in which features emerge?) and settled it as an honest, robust **null**. But the
real question — the one the package was built around — was always **how much of the final FORM (face,
body) does measured DNA determine?** The empirically obvious answer, which everyone knows and the model
is built to embody, is: **DNA is the FIRST CAUSE of form, but not the whole of it.** Identical twins
resemble each other yet diverge when their lives differ (exercise, diet, stress); 100% of the face does
not come from DNA, just as a person who trains and a person who does not have different bodies from the
same genome. v9 makes that decomposition **explicit and quantitative**, on machinery the package already
gates, and anchors it to published twin-study heritability.

### Why the adipose fat-fold is the right substrate
The adipose module is the one place in the package where DNA and environment **both** act on a measured
morphology: `AdiposeModel.activation(E, genome)` drives a spatially-varying fat field that inflates the
lean target into an actual body **and** face, and the package already measures the result (occupancy
volume, waist:hip ratio, lower-face width:height — a "roundness" index driven by the cheek/jowl band).
The genome enters **only** through its scalar storage propensity `P = genome_propensity(gammas)` — a
measured-γ readout already gated by `propensity_is_gamma_readout` — and the environment enters through
the chronic-surplus energy `E`. So the form is `form(P, E)`: **P is the DNA axis, E is the lived-life
axis.** No engine edit was needed; `morpho_decomposition.py` reuses these public primitives.

### What v9 computes and finds (reported, not tuned)
1. **Variance decomposition → model heritability.** Over a genetic-propensity × environment grid, the
   variance of body size/shape (occupancy volume) splits into a **genetic fraction H² = Var_genetic /
   Var_total**, an **environmental fraction**, and a GxE+residual. At a realistic environmental range,
   **H² = 0.51** (E² = 0.25, GxE+res = 0.25) — inside the published twin band (BMI 0.58–0.63, body-fat
   0.59–0.63, waist 0.48–0.61). **Both fractions are substantial: body shape is neither all-DNA nor
   all-environment.**
2. **Heritability is population-dependent — and the model reproduces it.** H² **rises to 0.84** when the
   population's environmental variation is narrow and **falls to 0.10** when it is wide. This is not a
   bug; it is a published fact (a systematic review of 32 twin studies finds BMI-heritability varies
   across populations precisely because their environmental variation differs). It is also **why no
   single H² is "the" answer**, and why the anchor is a **regime** match (both contribute; the model's
   achievable H² range overlaps the published band; H² falls as environment widens) rather than a tuned
   decimal.
3. **Identical-twin decomposition.** For one genome (= MZ twins, same DNA), the morphology at the shared
   lean reference is the **DNA-fixed core, bit-identical** between the twins (the resemblance). Give the
   twins two lives — active/lean vs surplus/sedentary — and the body and face **diverge**: **same DNA,
   but the surplus life adds +37% body volume and widens lower-face roundness by +25%** (the
   environmental envelope that fills the slots DNA leaves open).
4. **Where the face is DNA vs environment.** The model's lower-face roundness moves with adiposity
   (cheek/jowl band) — environmental — while the bony face frame is the γ-fixed core. This **matches the
   twin-study finding** that cheeks/chin/lips show the most environmental variation whereas central
   midface bone (nose, orbital ridges) is the most heritable.

### The anchor (locked + cited; the model is never tuned to it)
`code/data/heritability_anchor.json` records published twin H²: BMI 0.58–0.63, body-fat 0.59–0.63, waist
0.48–0.61, hip 0.52–0.58, height 0.69–0.81 (Schousboe 2004, PubMed 14610529); children ≥0.80
(Silventoinen, PMC10023566); BMI population-dependence (systematic review, PMC4346225); facial pattern —
midface bone genetic, cheeks/chin/lips environmental (Djordjevic 2016 PLoS One e0162250; Naini & Moss;
Weinberg 3D twin, PubMed 24501696). The grade is **[L]**. The file carries an explicit caveat that
heritability is a population-variance concept, so the comparison is a regime check, not a decimal
identity.

### Honest open slot (recorded, not hidden)
The model's facial **bone** has **no** non-adiposity environmental axis — aging, sun, gravity — so for
those it trivially attributes 100% to DNA, which real faces do not. That is the **clearest remaining
[O]** and the natural next lever (it needs a measured facial-aging/soft-tissue axis as a locked input;
none is in the package).

## New gate — verify_morpho_decomposition (PASS 5/5) → gate suite is now NINE gates

PASS means: (1) at the reference range H² + E² + GxE = 1 with both genetic (≥0.15) and environmental
(≥0.10) fractions substantial; (2) the heritability **regime** holds — reference H² in the published
band, the model's H² range overlaps it, and H²(narrow) > H²(ref) > H²(wide) (population-dependence
reproduced); (3) the twin decomposition holds — same genome at the shared lean reference is bit-identical
and the surplus twin is larger and rounder (correct direction); (4) the genetic axis is a real
measured-γ readout (`propensity_is_gamma_readout`), the fat fold IS the body fold (one switch < 1e-12),
the lean baseline is preserved (α≈0 → field == lean target), the explicit α equals `model.activation`,
and the anchor sha is frozen; (5) determinism (two runs → identical sha256). The gate passes precisely
because all of this is true with the real model.

## Files

New: `code/morpho_decomposition.py`, `code/verify_morpho_decomposition.py`,
`code/data/heritability_anchor.json` (locked + cited), `LEDGER_morpho_decomposition.md`,
`CHANGELOG_v9.md`, `PROJECT_SUMMARY.md`,
`repro/morpho/expected/morpho_decomposition_verify.json`.
`verify_all.py` GATES extended to **9**; `expected_sha256.json` pins **54** files (was 51; +2 code,
+1 measured-input data).

## What did NOT change
The engine, all eight prior gates, and all prior measured-input γ/stage tables are **byte-identical** to
v8 (verified: source pin drift 0). The dev-timing null and its robustness (v6–v8) stand unchanged. v9 is
purely additive: it answers the project's headline question and concludes the work. See
**PROJECT_SUMMARY.md** for the whole arc.
