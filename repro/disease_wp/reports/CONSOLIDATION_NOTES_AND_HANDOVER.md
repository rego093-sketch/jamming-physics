# CONSOLIDATION — investigation notes & handover

**Phase:** CONSOLIDATION GATE (the explicit R→W pivot — "stop investigating, start writing") — **no whitepaper prose.**
**Status:** complete and banked. Consolidation gate **PASS (10/10)**; it subsumes R1–R4 and re-asserts each
green (R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11); engine pin drift 0 (15/15). One erratum (**E2**) was surfaced by the
gate and resolved at root. Clean handover point. **Project is CLEARED for Phase W1.**
**Governing standard:** VP-SPEC v1.8 — its full authoring discipline (answer-first, claim grades, repro strips,
JSON-LD, gates) **switches on at Phase W1, which now begins.** This phase itself wrote no prose.

---

## Read this first — what this gate is, and the one condition it attaches to W1

The consolidation gate is the **meta-gate** that certifies the R1–R4 investigation is ready to become a
VP-SPEC-governed whitepaper. It introduces **no new facts** and writes **no prose**. Two design choices make its
PASS trustworthy rather than ceremonial:

1. **It subsumes the four investigation gates.** It re-runs `r1_gate.py`/`r2_gate.py`/`r3_gate.py`/`r4_gate.py`
   as subprocesses and asserts each prints PASS, so a single green consolidation gate means the *whole*
   investigation is reproducibly green at the pivot point — not merely that four stale gate-JSONs once said so.
2. **It re-derives the four ROADMAP criteria independently**, across the four curated datasets jointly, rather
   than trusting any recorded digest (mirroring the R3/R4 gates' "re-derive, don't trust the recorded sha"
   discipline).

**The W1-entry condition (recorded in the gate report, repeated here because it governs all W prose).** The two
deferred **`[L]`** passes are **not** prerequisites for entering W1 — they are accuracy *upgrades*, not gate
criteria. They are scheduled as **early-W1 tasks**. **Until both land, every W-phase use of the burden or
residual order must flag it as a provisional `[H]`-grade prioritisation device, not a registry-locked ranking:**
  1. **Treatment accession-dating** — pin each of the 35 therapies to an FDA label / GeneReviews "Management" /
     OMIM clinical management / Orphanet accession + date; lift `treatments.csv` grades `[H]`→`[L]` where
     confirmed and correct any class a labelled source contradicts.
  2. **Natural-history registry pass** (R3) — lift the progression/severity/mortality/disability axes from `[H]`
     definition-inferences to `[L]`/`[V]` (Orphanet natural history / OMIM clinical synopsis / published survival).

This is the exact analogue of the framing carried in the R3 and R4 handovers, now made the formal condition under
which authoring may proceed.

---

## What the consolidation gate checks (all re-derived; living code, not in the frozen manifest)

`code/pipeline/consolidation_gate.py` → `reports/consolidation.gate.json`. **PASS (10/10).** The ten checks,
mapped to the ROADMAP criteria:

| # | check | what it proves |
|---|---|---|
| 1 | `r_phase_gates_all_pass` | re-runs R1–R4 gates; each PASSes (subsumption) |
| 2 | `cohort_identity_consistent_35` | **ROADMAP #2** — the 35-disease cohort is *one* stable CUI set across `dossiers`, `_cohort_index`, `treatments`, `burden_scores`, `burden_residual`; all 35 present in `disease_index` |
| 3 | `provenance_complete` | **ROADMAP #1** — every graded field across 35 dossiers + 35 treatments + burden axes carries a `source` (non-`[O]`) or a named `obstacle` (`[O]`); `[L]`/`[V]` dossier sources carry a date or accession token |
| 4 | `grade_complete_no_summary_drift` | **ROADMAP #3** — every field grade is in the vocabulary `{[V],[L],[H],[O],[F]}`; the `_cohort_index` `field_grades` summary matches the actual dossier grades (no drift) |
| 5 | `class_consistency_cross_artifact` | **ROADMAP #2** — inheritance / mechanism / gene agree across `disease_index` ↔ dossiers ↔ treatments ↔ burden for all 35 |
| 6 | `scope_clean_cohort` | **ROADMAP #4** — all 35 cohort entities `in_scope` in both dossier and index; no cohort primary system in the OUT list (brain/nerve/heart/mood) without a recorded cross-reference |
| 7 | `exclusions_logged_not_dropped` | **ROADMAP #4 / SCOPE.md** — every `disease_index` `in_scope=false` row carries an `exclusion_reason` (name-it-don't-hide-it); 3 such rows, all logged |
| 8 | `gene_function_symbol_sweep` | **Erratum-E1 confirmation** — every dossier `gene_function` official symbol equals one of that dossier's cohort gene symbols (the FAH/FANCA alias-collision guard, standing confirmation) |
| 9 | `treatability_no_fabricated_cure` | **constitution C-D3** — no disease-level `curative` class; no treatment row claims `[L]` (still `[H]`); residual grade is `[H]` (not overclaimed) |
| 10 | `engine_pin_drift_zero` | governed emergence-engine pin re-verified, drift 0 (15/15) |

**HONESTY/SCOPE re-stated (C-D1).** Clinical facts from NCBI are *observed inputs* — respected and cited, never
"reproduced." The package's reproducible contribution is the *analysis* layer (classification, burden index,
residual offset). Treatment evidence is `[H]` (cited text / established science), and the burden/residual order is
`[H]`-grade provisional, until the two deferred `[L]` passes complete.

---

## Erratum E2 — Gaucher disease `variant_spectrum` grade-completeness (RESOLVED, v0.5.2)

The consolidation gate surfaced one genuine grade-completeness gap. Recorded here in full for the audit trail
(the same depth as E1).

**Symptom.** The **Gaucher disease** dossier (CUI `C0017205`) — a MedGen *aggregate* concept with **no causative
gene annotated** (`n_genes=0`, `identity.genes=[]`) — carried `variant_spectrum` as an **empty list `[]`**, so its
`_cohort_index` `field_grades.variant_spectrum` was an **empty string `''`** rather than a grade. Constitution C-D2
("each disease carries … each with provenance and a grade; untagged entities do not enter `data/curated/`") and
ROADMAP consolidation criterion 3 ("unavailable values are `[O]`, not guessed") require the field to be graded and
self-describing. (Note: the same dossier's `gene_function` was *already* correctly `[O]` with a named obstacle —
the asymmetry is the bug.) The gene-resolved subtype **Gaucher disease type I** (`C1961835`, GBA) is fully graded
and was unaffected.

**Root cause.** `code/pipeline/r2_build_dossiers.py` built `gene_function` with an `if not genes:` fallback that
emits a single `[O]` record with a named obstacle, but `variant_spectrum` had **no such fallback** — with an empty
gene list its build loop never executed and the field stayed `[]`. The `field_grades` summary,
`"/".join(sorted({x["grade"] for x in vs}))`, then evaluated over an empty set to `""`.

**Fix (root cause, not a hand-edit).** Added the **symmetric** `if not genes:` `[O]` fallback to
`variant_spectrum`, mirroring the existing `gene_function` fallback exactly:

```python
if not genes:
    vs.append(graded({"gene": None}, "[O]",
                     obstacle="causative gene not annotated at this MedGen aggregate concept; "
                              "no ClinVar gene query possible; see gene-resolved subtype dossier(s)"))
```

This hardens the *whole* gene-less-aggregate class, not just Gaucher. The dossiers were regenerated by re-running
the builder from its caches (offline), so the corrected field is a **genuine builder output**, not a manual patch.

**Containment verified.** Regeneration was surgical: **exactly one dossier changed** (`gaucher_disease.json`) plus
the derived `_cohort_index.json`; the other **34 dossiers are byte-identical**. Downstream digests are **UNCHANGED**
(`burden_scores`, `treatments`, `burden_residual`, `disease_index` all byte-identical) because **no R3/R4 stage
reads `variant_spectrum`** (verified by source scan). Dossier-set sha `b70b12d01e75 → 94818007c9cc` (expected and
documented). After the fix, **all gates re-pass**: R1 5/5, R2 7/7, R3 9/9, R4 11/11, consolidation 10/10; engine
pin drift 0 (15/15). The corrected `variant_spectrum` is graded `[O]` with a named obstacle.

**Residual recommendation.** The new `variant_spectrum` fallback now enforces this on rebuild for any future
gene-less aggregate concept; the consolidation gate's `grade_complete_no_summary_drift` check is a standing
guard against any field re-introducing an empty-string grade.

---

## Confirmed, reusable findings (so the next session does not re-derive them)

- **The 35-disease cohort is one stable identity.** The same CUI set appears in all five curated artifacts and is
  fully present in `disease_index`; the join key throughout is `medgen_cui`. Cross-artifact consistency
  (inheritance / mechanism / gene) holds with **0 inconsistencies**.
- **Provenance and grade are complete with zero violations.** Every graded field across dossiers, treatments, and
  burden axes carries a source or a named obstacle; no value is present without a grade; `[L]`/`[V]` dossier
  sources carry a date/accession token. The only gap found anywhere was E2, now closed.
- **Scope is clean.** All 35 cohort entities are in-scope in both their dossier and the index; none has an OUT
  primary system without a cross-reference; the 3 `in_scope=false` index rows are all logged with a reason.
- **The Erratum-E1 guard holds as a sweep.** Every dossier `gene_function` official symbol matches its cohort
  gene symbol — the FAH/FANCA alias-collision class is confirmed clean across all 35.
- **No fabricated cure.** No disease-level `curative` class; no treatment row claims `[L]`; residual grade `[H]`.
- **Determinism / governance.** The dossier builder is offline (caches only); the consolidation gate re-runs the
  R-gates (which themselves re-run their builders 2×). Engine pin drift 0 (15/15). consolidation_gate.py sha
  `df8f3c393816`, report sha `e84b88420db0`, dossier-set sha `94818007c9cc`.

---

## Known limitations carried forward (all transparent and graded)

1. **The burden/residual order is `[H]`-grade provisional** until the two deferred `[L]` passes land (see the
   W1-entry condition). This is the single most important caveat carried into W1 and **must be stated in any W
   prose that uses the order**.
2. **Treatment evidence is `[H]`, not `[L]`** (R4 limitation): accession-dating is the upgrade path.
3. **R3's P/S/M/D axes are mostly `[H]`** definition-inferences (R3 limitation): the natural-history registry
   pass is the upgrade path.
4. **Aggregate vs gene-resolved concepts coexist in the cohort** by design (e.g. "Gaucher disease" aggregate +
   "Gaucher disease type I" gene-resolved). The aggregate carries `[O]` for gene-dependent fields with a pointer
   to the subtype; W-phase structure should decide whether to author the aggregate, the subtype, or both as a
   cluster (the SCOPE.md cross-reference rule already governs the multi-system axis).

---

## Next session — begin Phase W1 (authoring ON)

Consolidation is **complete and PASS**. Per `ROADMAP.md`, **Phase W1 authoring now begins under full VP-SPEC v1.8
discipline** (this is the first phase that may write prose). Recommended order:

- **Run the two deferred `[L]` passes as the first W1 tasks** (each lifts a provisional `[H]` order toward
  registry-locked; both require NCBI/registry network access, deferred until now precisely because the R-phases
  banked offline-reproducible inputs):
  1. **Treatment accession-dating** — FDA label / GeneReviews "Management"/"Treatment of Manifestations" / OMIM
     clinical management / Orphanet → pin accession + date per therapy; upgrade `treatments.csv` `[H]`→`[L]`
     where confirmed; correct any class a labelled source contradicts. Revisit whether any disease's *standard of
     care* has become curative (this changes fast, e.g. gene therapies) — only then may the class change, and
     only with the accession.
  2. **Natural-history registry pass** — lift burden P/S/M/D `[H]`→`[L]`/`[V]`; re-rank under the locked axes.
- **Then author** under VP-SPEC v1.8: `docs/disease/<slug>/index.html` per disease or cluster (answer-first
  `<p class="answer">`, per-quantity cards with grade + repro link, JSON-LD `MedicalCondition` +
  `ScholarlyArticle`, ≤3-sentence paragraphs), hub at `docs/disease/index.html`. **Suggested W ordering**
  (ROADMAP): highest-burden, well-characterized, treatable monogenic systemic diseases first; then rare/ultra-rare
  and incurable entities (`[O]`-dominant); then cross-cutting mechanism chapters (lysosomal storage as a class,
  etc.). **Every W use of the burden order carries the provisional-`[H]` flag until the two passes above complete.**
- **Author actions still deferred** (ROADMAP): register `disease`/`dis` in VP-SPEC §2 + `registry/cross_volume_doi.*`;
  decide standalone vs 10th volume on jamming-physics.org; optional NCBI API key + contact email.

### Run order (consolidation, for reference / re-banking)
```
# investigation (unchanged; all offline from caches)
python3 code/pipeline/r1_build_index.py   ; python3 code/pipeline/r1_gate.py   # R1 5/5
python3 code/pipeline/r2_enrich_inscope.py ; python3 code/pipeline/r2_boundary_review.py
python3 code/pipeline/r2_mechanism.py     ; python3 code/pipeline/r2_cohort_medgen.py
python3 code/pipeline/r2_cohort_gene_resources.py ; python3 code/pipeline/r2_build_dossiers.py  # set sha 94818007c9cc
python3 code/pipeline/r2_gate.py          # R2 7/7
python3 code/pipeline/r3_burden_index.py  ; python3 code/pipeline/r3_gate.py   # R3 9/9
python3 code/pipeline/r4_treatment_survey.py ; python3 code/pipeline/r4_burden_residual.py
python3 code/pipeline/r4_gate.py          # R4 11/11
# the pivot
python3 code/pipeline/consolidation_gate.py   # -> reports/consolidation.gate.json  PASS (10/10)
sha256sum -c MANIFEST_governed.sha256          # engine pin drift 0 (15/15)
```
The consolidation gate is **living code** (post-dates the R2 freeze) and is intentionally **not** in
`MANIFEST_governed.sha256`; the governed engine set is unchanged (drift 0, 15/15).
