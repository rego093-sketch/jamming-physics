# R9 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.11, phase R9 + unmet-need surface)

Phase R9 raised the axis R8 left largely open — **PROGRESSION** — using an **open, citeable** source
(curated **PMC open-access** functional/survival literature), through the same disciplined,
cited dominant-sequela join R7/R8 used, with one decisive safeguard: **the tier is not hand-asserted,
it is DERIVED by the frozen R3 tier function applied to the verbatim cited sentence.** R9 also ships the
**§4 highest-value deliverable** — a read-only **unmet-need / treatment-gap surface**. Single author
(Young Jae Lee, ORCID 0009-0002-7535-8245). English deliverables, VP-SPEC v1.8 discipline (no-tuning,
bit-reproducible, honest grading `[O]<[H]<[L]<[V]`). All gates green; engine pin drift 0.

The R3/R4 BANKED files stay byte-identical (gate-verified); the registry layer (cumulative
**R5+R6+R7+R8+R9**) is what advances. Registry-set sha **d07a544475dc** (2× identical); unmet-need
surface sha **9aa184ff3dc2** (2× identical); site-set sha regenerated, W1 gate 17/17.

## 1. What R9 lifts — progression, from curated PMC open-access literature

R8 lifted severity for the one disease whose obligate dominant sequela is annotated in the open HPO
Severity subtree, and recorded that the remaining severity/progression lift — *where it exists* — is via
deliberate, cited curation from published functional & survival literature. **R9 is that curation pass**,
built as a gated stage identical in kind to the R7 disability join and the R8 severity join.

The a-priori inclusion criterion (declared, not fitted): a disease's **S or P** lifts to registry-grade
`[L]` **iff** a cited **PMC OPEN-ACCESS** source states a **disease-level** magnitude for its **dominant
untreated sequela** — *not* a sub-phenotype, *not* a treated-cohort figure, *not* "ranges from mild to
severe" spectrum/continuum language, *not* a comparative reference to other forms — and that magnitude
maps to the fixed BURDEN_INDEX tier **by the frozen R3 tier function** (`first_match` over
`PATTERNS["P_progression"]`/`["S_severity"]`; the same a-priori cut-points R3 itself uses) applied to the
verbatim cited sentence.

The build (and the gate) **fail** if the curated sentence (i) is not re-found **verbatim** in the pinned
OA cache, (ii) does not map to the row's declared tier under frozen R3, or (iii) trips the R3 **spectrum
override**. (ii)–(iii) are machine-checked; "dominant untreated sequela" + "non-comparative" are cited
curatorial inputs recorded per row (`dominant_sequela_basis`), exactly as R8's curation inputs were.
**No new cut-points are introduced** — so the no-tuning invariant is preserved by construction.

## 2. The two lifts (cited, frozen-R3-derived, non-spectrum)

| disease | axis | before | after | cited OA source | frozen-R3 tier | effect |
|---|---|---|---|---|---|---|
| **Niemann-Pick disease, type A** (C0268242) | P | 0.5 `[H]` | **1.0 `[L]`** | PMC8903814 (PMID 35282558) | 1.0 (progressive course with fatal outcome) | **new 3rd order_locked disease**; raw_burden 0.75→0.875; residual rank 5→2 |
| **Duchenne muscular dystrophy** (C0013264) | P | 0.5 `[H]` | **0.5 `[L]`** | PMC13008492 (PMID 41871622) | 0.5 (progressive) | grade-only corroboration (value unchanged); does **NOT** lock — its `S` was honestly declined at R8 and stays `[H]` |

- **Niemann-Pick A**: the cited sentence — *"NPD type A is a rare and fatal disorder that starts in
  early infancy and progressively worsens, leading to the patient's death by two to three years of age"*
  — is a disease-level statement about type A specifically (not the type A/B continuum), corroborated
  across independent OA sources (PMC10926222, PMC11015682). It makes Niemann-Pick A the **3rd
  order_locked** disease (O, P, S, D all `[L]`; M is `[O]`).
- **Duchenne MD**: a disease-level, non-comparative, non-spectrum progression statement (Becker MD is a
  separate allelic cohort, C0917713). Its `S` was correctly declined at R8 (a `Mild` modifier on a
  non-dominant cognitive feature), so DMD **does not** order-lock even though its `P` is now `[L]` —
  recorded as a deliberate non-lock, not an omission.

## 3. The five declines (recorded, never lifted)

Every considered-but-declined statement is recorded with a `decline_class` (from a fixed vocabulary) and
a per-disease reason in `methodology/severity_litcurate_excluded.csv`, re-found verbatim in the pinned
OA cache by the gate:

| disease | axis | class | why not lifted |
|---|---|---|---|
| Hurler syndrome (C0086795) | S | `comparative` | "severe" distinguishes Hurler from the *attenuated* MPS I forms — comparative nosology, not an anchored disease-level severity (PMC13090637) |
| Hurler syndrome (C0086795) | S | `spectrum` | a 2nd OA source predicates within-entity variability ("may vary widely … mild to severe") → scored at the `[H]` spectrum midpoint, not an extreme (PMC11405063) |
| Glycogen storage disease II / Pompe (C0017921) | P | `umbrella_spectrum` | the umbrella entity's progression is an explicit IOPD↔LOPD range — no single disease-level tier defensible (PMC12805081) |
| Maple syrup urine disease (C0024776) | P | `historical` | the only "rapidly progressive" phrasing is an explicitly historical 1954 description; cohort spans classic/intermediate/intermittent/thiamine-responsive forms (PMC10363028) |
| Tyrosinemia type I (C0268490) | P | `form_specific` | available OA progression statement is specific to the *chronic* form (and concerns diagnostic delay); acute vs chronic is a form-dependent spectrum (PMC8660245) |

The discipline is deliberately asymmetric: lift only where defensible, decline transparently — never
fish for an order-lock.

## 4. The §4 deliverable — unmet-need / treatment-gap surface

A transparent, fully-graded **research-prioritisation signal**, framed explicitly as *where to look*, not
a claim about *what will be found* — **not** clinical advice, **not** a diagnosis/prognosis, **not** a
cure claim. It needs almost no new data: it is a deterministic re-presentation of what the index already
computes.

- **residual (unmet-need) signal = `burden_score = raw_burden · (1 − e)`** — high burden + low
  treatability ⇒ large gap between suffering and available therapy.
- **honest headline = (burden grade `[L]`) AND (evidence_status = `none`, no disease-directed therapy).**
  Exactly two diseases qualify: **Achondrogenesis type II** and **Niemann-Pick disease type A** — both
  no-therapy, both `[L]`-burden, and **both now order-locked**. Niemann-Pick A appears as a **locked**
  headline *precisely because R9 lifted its progression* — the two deliverables reinforce each other.
- every cell carries its grade; `burden_order_provisional` is kept intact wherever the disease is not
  order-locked; a `treatment_gap_class` is assigned from `evidence_status`
  (`no_disease_directed_therapy` / `symptomatic_only` / `partial_disease_modifying` /
  `substantial_disease_modifying`).

The surface is a **pure view**: its gate re-derives every cell from the R9 registry (residual = the
registry `burden_score`, gap-class, provisional flag, all grades), so it **cannot drift** from the
registry, and asserts it changes nothing upstream (banked files + engine pin untouched) and leaks no
cure/outcome field.

## 5. Gates

- **`r9_gate.py` — PASS 15/15.** Determinism (r5→r9 chain, 2× identical); banked unchanged;
  cumulative-over-R8; join re-anchored in the pinned OA cache + **tier-from-frozen-R3** + non-spectrum;
  cut-points are the a-priori BURDEN_INDEX map; declines recorded; add-only no-downgrade; **R9 touches
  only S/P** (O/M/D byte-identical to R8) and changes S/P only for joined diseases; **new order-lock
  proven** (Niemann-Pick A locks, count 2→3; DMD does not); raw_burden re-derived; rankability;
  residual; order-lock rule + sensitivity (equal-weight ρ=1.0); every cited source open-access +
  source-bound; engine pin drift 0.
- **`w_unmet_need_gate.py` — PASS 6/6.** Determinism; every cell re-derived from the registry
  (residual == registry `burden_score`); sorted by residual desc; headline rule exact; no
  cure/outcome claim; read-only (no upstream change).
- Full suite re-run green: R1 5/5, R2 7/7, R3 9/9, R4 11/11, consolidation 10/10, R6 14/14, R7 16/16,
  R8 16/16, R9 15/15, unmet-need 6/6, **W1 site 17/17**.

## 6. Files added (living code; NOT in the frozen engine pin)

```
code/pipeline/r9_litcurate_fetch.py        fetch + pin cited PMC-OA articles (text_sha256, OA flag)
code/pipeline/r9_severity_litcurate.py     R9 apply (frozen-R3-derived tier; add-only; S/P only)
code/pipeline/r9_gate.py                    R9 gate (15/15)
code/pipeline/w_unmet_need_surface.py       §4 unmet-need / treatment-gap surface (pure view)
code/pipeline/w_unmet_need_gate.py          surface gate (6/6)
methodology/severity_litcurate_join.csv     2 lifts (cui, axis, pmcid, pmid, tier, exact_sentence, basis)
methodology/severity_litcurate_excluded.csv 5 declines (decline_class + per-disease reason)
data/raw/litcurate/<PMCID>.json             7 pinned OA snapshots (idempotent re-validation)
data/curated/unmet_need_surface.{json,csv}  the surface deliverable
reports/r9.gate.json, reports/unmet_need.gate.json
```

The site (`tools/w1_build.py`) prose was synced to R9: five registry passes, the curated progression
lift, Niemann-Pick A as the 3rd order-lock, DMD corroborated-not-locked, `order_locked` made dynamic,
and the unmet-need surface referenced on the framework/hub pages, `_meta.json`, the ledger, and
`llms.txt` (kept <5 KB). The page-set contract is unchanged (39 pages); the surface ships as a data
artifact, not a new HTML page.

## 7. Handover forward

- **Progression / severity remaining lift.** P is now `[L]` for 7/35, S for 3/35. The rest stay
  `[H]`/`[O]` with the obstacle named. Further lift is more curated PMC-OA dominant-sequela joins under
  the **same** frozen-R3-derived-tier rule — add rows to the join/excluded CSVs and re-run; never widen
  the cut-points, never lift on spectrum/comparative/treated-cohort statements.
- **Mortality** remains the thinnest axis (most `[O]`; 2 corroborated `[L]` from PMC). A disease-typical
  quantitative survival figure is required before an `[O]` mortality cell may lift — free text does not
  fill it (over-trigger risk), consistent with R7.
- **Order-locks.** 3/35 (Achondrogenesis II, Niemann-Pick A, Tyrosinemia II). The cohort order stays a
  provisional `[H]` device until more axes reach registry grade — not guessed.
- **The OMIM clinical-synopsis path stays removed** (key unobtainable for an individual researcher), not
  deferred.
