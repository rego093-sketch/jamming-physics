# CHANGELOG — universal_morphogenesis_geneclock v10 (INTERNAL/visceral organ emergence)

Built on v9 (the SHAPE-decomposition capstone) and the same neuro_emergence_chain_integrated v1.9
VP-SPEC C3 no-tuning governance. **Add-only, no engine edits, no fork of `organism/core.py`.** ONE
new measured input table (visceral-organ master γ, fetched by the identical NCBI→SantaLucia
pipeline) + ONE locked + cited staging table (organ-primordium Carnegie stages). Unified entry
`verify_all.py` now **PASS 12/12** (ten gates 5/5 + sha256 source/measured-input pin drift 0 + ten
fidelity baselines leaf drift 0). `expected_sha256.json` pins **61** files (was 54; +3 code, +4 data).

## Why v10 — completing the "DNA → body" arc with the INTERNAL organs

v9 concluded the external/composition arc (face/body shape + heritability). The one piece missing
for a complete *DNA → whole body* framework was the **internal organs**: in `assemble.anatomy_spec`
they exist only as hand-placed ellipsoids that inherit the switch decisions *geometrically*. v10
gives each visceral organ its own master gene, so the **ORDER and relative timing of organ
appearance fall out of the SAME R19 gene clock** that already drives the face features — internal
organogenesis as a deterministic readout of measured γ (heterochrony), not a hand-set sequence.

This was a named open item from the project's first handoff (`anatomy inside the grown target`;
the `15-morphogenesis-full-organism` packaging the original handoff scoped for the DNA whitepaper).

## What v10 computes and finds (reported, not tuned)

**1 · Visceral-organ emergence schedule (gene-clock readout) — `organ_atlas.py`.**
8 organs tagged with their specification masters: heart=NKX2-5, liver=HHEX, stomach=BARX1,
lung=NKX2-1, pancreas=PDX1, kidney=SIX2, spleen=TLX1, midgut=CDX2. The emergence ORDER is
`argsort(spinodal(γ))` (`order_is_gamma_readout=True`); perturb a γ and it resorts. The fold is the
**same** body fold (`assert_one_switch` = 2.2e-16). γ is read VERBATIM from `data/organ_gamma.json`
(NCBI exact TSS → promoter TSS-2000..+500 → γ=−mean(NN ΔG37, SantaLucia 1998); all `NC_`/GRCh38;
corr(γ,GC)=0.994; cached so it reproduces offline). **[V]** order; **[F]** sign + τ window; **[L]** γ.

**2 · Organ-timing test — the HEADLINE is an HONEST NULL — `organ_timing.py`.**
The same falsifiable question the external dev-timing line asked, now for internal organs: does the
measured-γ schedule predict the observed first-appearance Carnegie stages? **Result: NO.**
Spearman ρ(spinodal, observed CS) = **−0.414** (exact permutation p = **0.360**, n!=5040);
Pearson r = −0.447. If anything weakly **anti**-correlated — spleen (TLX1) is γ-earliest but
biologically **latest** (CS15); stomach (BARX1) is γ-latest but CS12. A positive "DNA predicts organ
timing" claim is **not earned** → grade **[O]**. This is fully consistent with the external-feature
null (v5–v8): promoter stiffness is not the molecular correlate of timing, internal or external.
The staging table (`data/organ_timing.json`) is locked + cited (O'Rahilly & Müller Publ. 637;
Larsen's; Moore; UNSW Embryology), integer, γ-independent, sha256-frozen, **never adjusted**.

**Scope decision (recorded, not silent):** midgut/intestine (CDX2) is carried in the atlas (geometry)
but **EXCLUDED from the locked timing test** because intestinal first-appearance is progressive
(CS10–13, no crisp single stage) — the same soft-staging reason MYF5/myotome was excluded in v8.

## New gate — `verify_organ_timing` (PASS 5/5) → gate suite is now TEN gates

PASS means (exactly like `verify_dev_timing`, and **not** requiring any correlation value):
(1) ONE SWITCH — organ fold == body fold < 1e-12; (2) LOCKED CITED INPUT — provenance present,
all test genes genuine [V] masters, integer stages, sha frozen, stages γ-independent and not a
suspicious match (|ρ|<0.99); (3) GRADE == EVIDENCE — schedule is a pure γ readout and the recorded
grade is [V] iff (perm p<0.05 and ρ>0) else [O]; (4) FALSIFIABILITY — apparatus detects a synthetic
signal (ρ→1) and collapses on a shuffle (true null, not a dead test); (5) DETERMINISM — 2× run
identical sha256. The gate passes **because** the package reports the honest [O].

## Files

New code: `code/organ_atlas.py`, `code/organ_timing.py`, `code/verify_organ_timing.py`.
New measured input: `code/data/fetch_organ_gamma.py`, `code/data/organ_gamma.json`,
`code/data/organ_promoters.cache.json`, `code/data/organ_timing.json` (locked + cited).
New docs: `LEDGER_organ_emergence.md`, `CHANGELOG_v10_organ.md`, this `HANDOFF_v10_organ.md`.
New fidelity baseline: `repro/morpho/expected/organ_timing_verify.json`.
`verify_all.py` GATES extended to **10**; `expected_sha256.json` pins **61** files (was 54).

## What did NOT change

The engine, all nine prior gates, and all prior measured-input γ/stage tables are **byte-identical**
to v9 (verified: source pin drift 0 over the shared files). The v9 capstone, the dev-timing null and
its robustness (v6–v8), and the heritability decomposition stand unchanged. v10 is purely additive:
it extends the framework to internal organs and finds the same honest timing null.

## What is still open (each DATA-blocked, not effort-blocked) — see LEDGER + HANDOFF

1. **Couple the schedule to Layer-2 anatomy** (`assemble.anatomy_spec`) so a grown organism fills
   with organ structure in γ-order (geometry; still not a timing-validation claim). ← clearest next.
2. A **different measured modality** (expression-onset / chromatin accessibility) to actually test
   "DNA predicts organ timing" — [O] data-blocked (needs an external organogenesis atlas).
3. **Widen** the crisp-staged organ set (thyroid/adrenal/gonad) to lift permutation power.
