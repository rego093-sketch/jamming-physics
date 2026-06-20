# CHANGELOG — v6 (predictor battery + standalone-repro backbone fix)

Built on **v5.1** (unified entry `verify_all.py` PASS 7/7) and on
**neuro_emergence_chain_integrated v1.9** governance (VP-SPEC C3 no-tuning).

**Add-only. No engine edits. No fork of `organism/core.py`.** Two independent,
clearly-separated pieces of work:

- **Part A** — a backbone fix that makes the v5.1 verification reproduce
  **standalone** (no sibling package required). Science-null, information-preserving.
- **Part B** — the v6 #1 science deliverable: keep the developmental-timing
  apparatus, **swap the input variable**, and report an honest result.

Unified entry is now **PASS 8/8** (six gates 5/5 + source pin drift 0 + six
fidelity baselines, leaf drift 0).

---

## Part A — standalone-reproducibility backbone fix

### The defect
v5.1's source-integrity layer is bit-for-bit. Two gate messages pinned an
**environment-dependent** string: a *bonus* cross-package provenance line that only
resolves when the sibling `neuro_emergence_chain_integrated_v1.9` happens to be
co-located on disk. In a clean checkout of *this* package alone, that string takes a
different branch, so the frozen fidelity baseline mismatched on one leaf and
`verify_all.py` reported `FAIL (6/7)` — even though the science was untouched and every
gate still printed `OVERALL: PASS (5/5)`. The two gates had also been frozen in
*different* co-location environments, so the inconsistency was latent.

### Root cause (diagnosed, not guessed)
The single failing leaf was a **string** in `morpho_plus_verify.json`
(`$.2 GAMMA SUPERSET … msg`); all 15 other leaves on that gate (numeric/boolean) were
identical and the gate itself stayed PASS 5/5. The mirror pattern lived in
`verify_gene_clock.py`'s check-2, whose baseline happened to capture the *other* branch
(so it passed standalone but would have failed *with* neuro present). The cross-package
check is explicitly labelled a "bonus … if co-located" in the source — i.e. genuinely
optional provenance, not a correctness invariant.

### The fix (the honest option)
Two bad options were **rejected**: (a) fabricating a neuro sibling by copying an
in-package file into the expected sibling path — a circular, dishonest back-door; and
(b) re-freezing to bury the red leaf. Instead the two gates' **pinned** messages were
made environment-independent:

- `verify_gene_clock.py :: check_gamma_verbatim` — pinned msg is now the stable
  `"in-package measured gamma loaded verbatim (26 genes)"`.
- `verify_morpho_plus.py :: check_gamma_superset` — pinned msg is now the
  environment-independent superset statement (missing/moved/value-drift counts) with no
  neuro suffix.

In **both** gates the neuro cross-check **still runs**, still prints as
`[bonus, unpinned]`, and **still gates a genuine mismatch when neuro IS present**
(`ok = ok and same`). Only the env-dependent *string* was removed from the pinned set.
Net effect: the v5.1 backbone now reproduces from a clean, standalone checkout while
losing no cross-package verification power. This is folded into v6 (rather than shipped
as a separate v5.2) because it lands together with the Part B science.

---

## Part B — v6 #1: swap the input variable (timing predictor battery)

### The question
v5 established an honest null (`LEDGER_dev_timing.md`): measured promoter-stiffness γ
does not predict Carnegie first-appearance staging for the 7 [V]-master features
(Spearman ρ = −0.018, exact-permutation p = 0.986). γ is only one quantity readable from
those promoters. v6 #1 keeps the **exact** apparatus — same locked Carnegie stages, same
exact-permutation Spearman test, same grade==evidence rule — and asks whether a
**different measured promoter quantity** predicts the staging order.

### What was added
- `code/timing_predictors.py` — runs a **battery** of six measured promoter quantities
  against the same locked stage vector: `gamma`, `gc` (both read **verbatim** from the
  locked `morpho_gamma.json`, never recomputed), and `cpg_oe`, `tata`, `gcbox`, `caat`
  (computed from promoter sequence, each motif a **fixed a-priori** canonical consensus).
  Reuses dev_timing's exact-permutation engine. Applies **Bonferroni** correction over the
  K = 6 predictors and computes + discloses the **exact-permutation power floor**.
- `code/data/timing_promoters.cache.json` — a self-contained 7-gene promoter cache so the
  battery reproduces **offline**. Four sequences (TBX5/TBX4/HOXD13/PAX9) are copied
  **byte-for-byte** from `morpho_promoters.cache.json`; three (PAX2/PAX6/LHX2, which had no
  in-package sequence) were re-fetched once by the **identical** pipeline and frozen, with
  their reproduction residuals recorded.
- `code/verify_timing_predictors.py` — the gate (PASS = 5/5): grade==evidence, locked
  inputs (stage sha frozen & equal to dev_timing's; copies byte-identical; fetches
  reproduce locked γ within tol; γ ρ equals dev_timing's), falsifiability (non-blind),
  no-tuning motifs + power disclosed, determinism.
- `LEDGER_timing_predictors.md` — the honest grading.

### The result (reported, not tuned)
**Every predictor is [O].** K = 6, Bonferroni α = 0.00833:

| predictor | ρ | perm p | Bonferroni p | grade |
|---|---|---|---|---|
| gamma | −0.018 | 0.986 | 1.000 | [O] |
| gc | −0.108 | 0.821 | 1.000 | [O] |
| cpg_oe | +0.432 | 0.329 | 1.000 | [O] |
| tata | +0.399 | 0.476 | 1.000 | [O] |
| gcbox | −0.624 | 0.144 | 0.867 | [O] |
| caat | +0.468 | 0.292 | 1.000 | [O] |

This **widens** the v5 null from "stiffness" to "proximal-promoter composition": GC,
CpG o/e, and the three core promoter motifs are *also* not the molecular correlate of
developmental timing for these features. The `gamma` row reproduces v5 **exactly**
(a built-in consistency check, since `spinodal` is strictly monotone in γ).

### Power, disclosed
At n = 7 with one stage tie, the exact-permutation **floor** (smallest reachable p) is
**0.00079** < α = 0.00833 — so Bonferroni significance *was* reachable; this is a real
null on a live test. Three composition predictors show a **moderate, non-significant
positive** trend (ρ ≈ +0.40 … +0.47) that n = 7 cannot resolve — a motivation for the
open items, not a finding.

### Honest provenance: re-fetch residuals
The three re-fetched promoters reproduce the **locked** sensory γ/gc to within
assembly-version drift (LHX2 exact; PAX6 |Δgc| = 4×10⁻⁴; PAX2 |Δγ| = 3×10⁻⁴) — far below
the inter-gene γ spread (~0.14). Per VP-SPEC C3 the locked γ/GC tables are **never
overwritten**; the residuals are recorded and the gate tolerates only this drift
(tol = 5×10⁻³, ~15× the largest residual, ~30× below a wrong-gene error).

---

## Frozen baseline (re-recorded from the green 8/8 state)
- `expected_sha256.json` — now pins **45** governed source + measured-input files
  (42 prior + `timing_predictors.py`, `verify_timing_predictors.py`,
  `data/timing_promoters.cache.json`).
- `repro/morpho/expected/timing_predictors_verify.json` — new frozen fidelity baseline
  (17 leaves); the five prior baselines are unchanged.

## Unchanged / preserved (enforced by the pin)
The engine, the R19 switch, the measured γ tables, the emergence order, the Layer-3
convergence proof, the honest dev-timing null, and the life-course coupling are all
preserved bit-for-bit. The five prior gates were re-run and stay 5/5; the sixth is new.

## Open items after v6 #1 (honest)
1. **[O] widen the feature table** beyond n = 7 (the binding power constraint) so the
   moderate positive composition trend gets a fair test.
2. **[O] change data modality** to expression-onset / chromatin accessibility — more
   plausibly the timing correlate — which is **data-blocked** until that external atlas
   is added as a locked input.
