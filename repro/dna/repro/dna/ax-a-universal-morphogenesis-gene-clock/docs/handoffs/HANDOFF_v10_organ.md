# HANDOFF — v10 visceral-organ emergence → continue in a fresh session

**How to resume:** paste this file + the zip
(`universal_morphogenesis_geneclock_v10_organ.zip`) into a new conversation and say
*"continue from HANDOFF_v10_organ.md"*. Everything runs from `code/` (flat imports). Results land
in `results/`. Verify the whole package with one command from the package root:

```
python3 verify_all.py            # expect OVERALL: PASS (12/12)   [~5 min; one gate is heavy]
python3 code/organ_atlas.py      # print the visceral-organ emergence schedule
python3 code/organ_timing.py     # print the organ-timing test (honest null)
```

This is an **add-only, no-tuning, no-engine-edit** package under neuro VP-SPEC C3 governance:
**every constant is a measured input (locked + cited) or a derived value — never a number chosen
to hit a target.** Keep it that way.

---

## 1. What v10 did (session log)

The package already grew the EXTERNAL form (face/body/skeleton, v1–v3) + the COMPOSITION axis
(adipose, v3–v5) + the heritability decomposition (v9) from measured γ. The one missing piece for a
complete **DNA → whole body** arc was the **internal organs**: in `assemble.anatomy_spec` they
existed only as **hand-placed ellipsoids** that inherit the switch decisions geometrically. v10 gives
each visceral organ its own master gene so the **ORDER/timing of organ appearance is a gene-clock
readout of measured γ** — internal organogenesis as heterochrony, the same R19 fold that drives the
face features. (This was the named open item "anatomy inside the grown target" / the
`15-morphogenesis-full-organism` packaging from the project's first handoff.)

Two pieces were built and **both gate green**:

1. **`organ_atlas.py` — the emergence schedule (geometry/order).** 8 organs tagged with specification
   masters; emergence order = `argsort(spinodal(γ))` (`order_is_gamma_readout=True`); one switch
   (organ fold == body fold) = **2.2e-16**.
2. **`organ_timing.py` — the falsifiable timing test → HONEST NULL.** Does the measured-γ schedule
   predict the observed Carnegie staging? **No.** Spearman ρ = **−0.414**, exact perm p = **0.360**
   (n!=5040), Pearson r = −0.447 → grade **[O]**. Promoter stiffness is **not** the organ-timing
   correlate — consistent with the external-feature dev-timing null (v5–v8).

New gate `verify_organ_timing` (PASS 5/5, grade==evidence) → the suite is now **ten gates**;
`verify_all.py` = **PASS 12/12**; `expected_sha256.json` pins **61** files (was 54).

---

## 2. Embedded reference (so you don't have to re-derive it)

### Gene → organ map + MEASURED γ + observed Carnegie stage

All γ fetched by the **identical** pipeline (`code/data/fetch_organ_gamma.py`): NCBI exact human
TSS → promoter window **TSS-2000..+500** → **γ = −mean(NN ΔG37, SantaLucia 1998)**. All from `NC_`
(GRCh38) accessions; **corr(γ,GC)=0.994**. Sequences cached in `organ_promoters.cache.json` so γ
reproduces offline bit-for-bit. CS from O'Rahilly & Müller (Carnegie Publ. 637), Larsen's, Moore,
UNSW Embryology — **locked, integer, γ-independent, sha-frozen** in `data/organ_timing.json`.

| organ (primordium) | master | grade | γ | spinodal | obs CS | in timing test? |
|---|---|---|---|---|---|---|
| heart (cardiogenic→heart tube) | NKX2-5 | [V] | 1.5130 | 0.71632 | 10 | yes |
| liver (hepatic diverticulum) | HHEX | [V] | 1.5250 | 0.72486 | 11 | yes |
| stomach (gastric dilation) | BARX1 | [V] | 1.5609 | 0.75060 | 12 | yes |
| lung (respiratory diverticulum) | NKX2-1 | [V] | 1.5088 | 0.71334 | 13 | yes |
| pancreas (dorsal bud) | PDX1 | [V] | 1.4732 | 0.68824 | 13 | yes |
| kidney (metanephric cap) | SIX2 | [V] | 1.5556 | 0.74678 | 14 | yes |
| spleen (splenic primordium) | TLX1 | [V] | 1.4228 | 0.65323 | 15 | yes |
| midgut/intestine | CDX2 | [V] | 1.4500 | 0.67205 | — | **no (soft staging)** |

- **DNA-derived order** (earliest→latest): spleen < pancreas < lung < heart < liver < kidney < stomach
- **Observed order** (by CS): heart < liver < stomach < (lung=pancreas) < kidney < spleen
- The two are nearly **anti-correlated** (spleen γ-earliest but biologically latest; stomach γ-latest
  but CS12) → the [O] null. The γ values are all in a **narrow band** (1.42–1.56), so γ has little
  discriminating power for organ timing — a real observation, not a bug.

**Scope decision (recorded, not silent):** midgut/intestine (CDX2) is carried in `organ_atlas.py`
for the geometry but **excluded from the locked timing test** — intestinal first-appearance is
progressive (CS10–13, no crisp single stage), the **same** soft-staging reason MYF5/myotome was
excluded in v8. Including it would mean picking one stage from a range (disguised tuning).

### Grades at a glance (full ledger: `LEDGER_organ_emergence.md`)
**[V]** one-switch; emergence order = γ readout; gene→organ masters (HHEX also thyroid/forebrain,
NKX2-1 also thyroid — noted). **[F]** sign convention (higher spinodal→later) + τ window. **[L]**
measured γ; Carnegie stages. **[O]** "γ predicts organ timing" (NULL, ρ=−0.414); organ size/shape/3D
placement from dwell (schedule **not yet** coupled to anatomy geometry).

---

## 3. Current limitations (be honest about these)

- **The schedule is NOT yet coupled to 3D anatomy.** v10 produces the per-organ `tau_on`/`dwell`/
  `a_f(τ)` and the emergence **order**, but `assemble.anatomy_spec` still places the organ ellipsoids
  by anatomical spec, **not** driven by the gene-clock schedule. So "organs appear in γ-order *in the
  grown body*" is not yet demonstrated in the voxel volume — only the schedule is. ← **biggest gap.**
- **The timing claim is a null, by design.** v10 does NOT claim DNA predicts organ timing; it claims
  the order is a deterministic γ readout and reports honestly that it does **not** match staging.
- **n=7 crisp organs** is small for permutation power (floor for n=7 ~ 7.9e-4); widening helps.
- **HHEX / NKX2-1 are multi-tissue** masters (liver-bud / lung used here); noted, not hidden.

---

## 4. Prioritized next steps (roughly in order of value)

**1. Couple the gene-clock schedule INTO Layer-2 anatomy — the clearest completion (geometry).**
   Wire `organ_atlas.organ_schedule()` into `assemble.anatomy_spec(tau, reg, somites)` so each organ
   ellipsoid (heart/lung/liver/gut already there; add stomach/pancreas/kidney/spleen) **appears at its
   `tau_on` and scales by its `dwell`** as τ advances — i.e. a grown organism *fills with organ
   structure in γ-order*. Then add a gate `verify_organ_anatomy` proving: (a) at τ=1 every organ is
   present (so the body is complete), (b) the appearance order across τ == the schedule order
   (`order_is_gamma_readout`), (c) the lean baseline / convergence proof is untouched at the reference,
   (d) the bbox-culled label write still matches a naive comparator (the optimization invariant), (e)
   determinism. **This is geometry — still NOT a timing-vs-biology claim** (keep that grade [O]).
   *Obstacle:* none — addable now. This is the natural v11.

**2. A DIFFERENT measured modality to actually test "DNA predicts organ timing".**
   Promoter *stiffness* γ is now ruled out for organ timing (as for external features). The remaining
   honest lever is a different measured quantity at the organ master loci — **expression-onset** or
   **chromatin accessibility**. Build the same `*_timing.py` apparatus around it and report whatever ρ
   falls out. *Obstacle:* **[O] data-blocked** — needs an external organogenesis/atlas (e.g. a
   developmental expression timecourse) added as a **locked** input; none is in the package.

**3. Widen the crisp-staged organ set** to lift permutation power: candidate clean [V] masters with
   citable single-CS staging — **thyroid** (FOXE1, but borderline master), **adrenal cortex** (NR5A1/
   SF1; CS14), **gonad/genital ridge** (NR5A1/WT1; CS15). *Obstacle:* each must be a genuine master with
   a crisp single first-appearance CS (avoid the MYF5 trap); confirm before locking. Re-fetch γ by the
   identical pipeline and **freeze** before computing any correlation.

**4. (If you take the dna_vp merge route discussed with the user.)** Package the organ work as a
   `15-morphogenesis-full-organism` block under `repro/dna/` of
   `dna_vp_site_INTEGRATED_v1_9_stress_merged.zip` (engine imports `organism/core.py` single-source +
   sha256-pin, `run.py` with 2× sha256 determinism gates + frozen `expected/`, `README.md`, `LEDGER`).
   Note: v10 has outgrown a single appendix chapter — consider a multi-section block or a companion
   "Part II" framing rather than one appendix. γ provenance is already dna_vp (the morpho_gamma
   tables are `extracted verbatim from dna_vp_site human_organ_interpretation.json`), so the merge is
   non-circular.

---

## 5. Invariants to preserve (in addition to all prior-session invariants)

- `organ_atlas.assert_one_switch()` and `verify_organ_timing` check 1 must stay **< 1e-12** (the organ
  fold IS the body fold — `spinodal(g)=2*(g/3)^1.5`). Never fork `organism/core.py` or `morpho_core`.
- `data/organ_gamma.json` is **read-only measured**: γ fetched by the identical NCBI→SantaLucia
  pipeline, cached for offline reproduction, **never tuned**. If you re-fetch, the cached sequence must
  recompute the same γ (assembly-drift tol ≤ 5e-3), and you re-freeze deliberately.
- `data/organ_timing.json` stages are **integer, γ-independent, sha-frozen**; **never edit a stage to
  move ρ**. `verify_organ_timing` enforces **grade == evidence** — a green gate means the truth was
  reported, not that the correlation was good. The non-blind self-test (synthetic γ ordered to stages
  → ρ=+1.000; shuffle → small) must keep passing or the null is meaningless.
- The emergence order must stay **exactly `argsort(spinodal(γ))`** (`order_is_gamma_readout=True`), so
  perturbing a γ deterministically resorts the order (a pure DNA readout, no hand-typed order).
- Keep the timing test to genuine **[V] masters with crisp single-CS staging**; soft-staged organs
  (like midgut) go in the atlas geometry but **not** the locked test (the MYF5 precedent).

### Freeze workflow (how to add the next gate/files — what v10 did)
1. Build the module + gate; run the gate → confirm `OVERALL: PASS (5/5)` and that it writes
   `results/<name>_verify.json`.
2. Add `("<gate_stem>", "<name>_verify.json")` to `GATES` in `verify_all.py`.
3. Pin + freeze (deliberate): either run `python3 verify_all.py --freeze` (re-runs ALL gates, ~5 min,
   refuses unless all pass), **or** the targeted equivalent — add the new files' sha256 to
   `expected_sha256.json` and copy `results/<name>_verify.json` → `repro/morpho/expected/`. Do **not**
   silently alter existing pins (confirm 0 drift on the shared files first).
4. Re-run `python3 verify_all.py` → confirm the new `OVERALL: PASS (N/N)`.

---

## 6. Map of the new code (v10)

- `code/organ_atlas.py` — `ORGAN_MASTERS` (organ→gene→grade→anat_label→note), `load_organ_gamma()`,
  `organ_schedule(include_midgut=True)` (the gene-clock schedule + derived order + readout check),
  `schedule_rows()`, `assert_one_switch()`. Run it to print the emergence schedule.
- `code/organ_timing.py` — `load_organ_timing()`, `derived_schedule()`, `calibrate()` (Spearman/
  Pearson/exact-permutation, grade==evidence), falsifiability self-checks
  (`apparatus_detects_signal`, `stages_independent_of_gamma`), `write_results()`. Run it to print the
  honest null.
- `code/verify_organ_timing.py` — the 5-check gate (one-switch, locked-cited-input, grade==evidence,
  falsifiability, determinism). Writes `results/organ_timing_verify.json`.
- `code/data/fetch_organ_gamma.py` — the NCBI→SantaLucia fetch (identical pipeline). Re-run only to
  re-fetch; the cache makes γ reproduce offline.
- `code/data/organ_gamma.json` — measured γ for the 8 organ masters (provenance per gene).
- `code/data/organ_promoters.cache.json` — cached promoter sequences (offline reproduction).
- `code/data/organ_timing.json` — locked + cited Carnegie stages (the timing test target).
- `LEDGER_organ_emergence.md`, `CHANGELOG_v10_organ.md` — the honest grading + the v10 record.

---

## 7. One-line state

v10 extends the framework to the **internal organs**: the visceral-organ emergence **order** is now a
deterministic readout of measured γ (one switch, order=argsort(spinodal(γ))), and — tested honestly
against locked Carnegie staging — promoter stiffness does **not** predict organ timing (ρ=−0.414,
grade [O]), exactly as for external features. `verify_all.py` = **PASS 12/12**. The clear next step is
to **couple the schedule into the Layer-2 anatomy geometry** (v11), keeping the timing claim [O].
