# ROADMAP — Genetic & Rare Disease Whitepaper (working title: *Disease Mechanisms*)

**Project code (proposed):** `disease` / `dis` — to be registered in VP-SPEC §2 by the author.
**Governing standard:** `VP_SPEC_v1_8.md` (bundled). **Sibling boundary:** the neuro/mind whitepapers own
brain, nerve, heart, and affect; this whitepaper owns the **systemic body** (see `SCOPE.md`).
**Authoring language:** English only (constitution). **Reporting language to author:** Korean, plain terms.

---

## Governing principle of the roadmap (author-directed)

> **First investigate, then write.** Phases R1–R4 are **investigation only** — they produce structured,
> provenance-tagged **data and notes**, never whitepaper prose. VP-SPEC v1.8's full authoring discipline
> (answer-first, claim grades, reproducibility strips, JSON-LD, gates) is **switched on at Phase W1**, once
> the investigation is consolidated. This matches the directive that the opening phases stay exploratory.

The reason for the split: VP-SPEC C1 requires that every quantitative claim in the *written* paper be
deterministically reproducible. We cannot assert that discipline over facts we have not yet collected and
checked. So we collect first (R-phases), then bind the written claims to that collected, cited base (W-phases).

---

## Phase R0 — Bootstrap **[COMPLETE, this session]**

| item | state |
|---|---|
| Project skeleton (`code/`, `methodology/`, `data/`, `reports/`) | created |
| Emergence engine carried in (`code/emergence_v2/`, 22 files) | **drift 0 across relocation** — 5/5 gates re-pass at the new path; morphogen `sha 01b0b6ea8b10` / band `4ea1c7b4111c` identical to the DNA package closeout |
| Governed pin `MANIFEST_governed.sha256` (15 `.py`/`.json`) | created + self-verified OK |
| Governance docs (`VP_SPEC_v1_8.md`, `CONSTITUTION_disease.md`, `SCOPE.md`) | in place |
| Methodology drafts (`DISEASE_TAXONOMY.md`, `BURDEN_INDEX.md`, `DATA_PROVENANCE.md`) | drafted (refined in R1–R3) |
| NCBI E-utilities reachability | confirmed (HTTP 200; clinvar·omim·medgen·gene·dbvar·gtr·snp·pubmed·mesh available) |

**Why the emergence engine lives here.** It is the *normal-development baseline*. Many genetic diseases are
perturbations of a developmental/morphogenetic program: a loss-of-function morphogen allele shifts the
length scale `λ = √(D·τ)`; a dosage change shifts Layer-2 `φ`; a threshold change shifts the `spinodal(γ)`
switch. Carrying the engine here lets developmental-disease sections (W-phase) reference a reproducible
baseline **inside this package**, so the large DNA package no longer has to be re-uploaded each session.

---

## Phase R1 — Disease universe & classification scaffold **[investigation only]**

- **Goal:** enumerate the in-scope disease entities and place each on the taxonomy axes (`DISEASE_TAXONOMY.md`).
- **Source:** NCBI MedGen (medical-genetics concepts) ↔ OMIM (gene–phenotype) ↔ Gene ↔ ClinVar; MeSH for vocabulary.
- **Deliverable:** `data/curated/disease_index.csv`
  `entity, omim_id, medgen_cui, gene(s), inheritance_class, mechanism_class, organ_system, in_scope, provenance`
- **No prose.** This is an index, not a section.
- **Investigation gate:** every row has a source accession + retrieval date; no duplicate entities; the
  exclusion rule in `SCOPE.md` is applied and logged (excluded entities are recorded with the reason, not silently dropped).

## Phase R2 — Per-disease molecular & clinical dossiers **[investigation only]**

- **Goal:** for each entity (or tight cluster), assemble the mechanistic + clinical facts.
- **Per-entity fields:** gene function; variant classes (ClinVar significance distribution); molecular
  mechanism (loss-of-function / gain-of-function / dominant-negative / haploinsufficiency / dosage /
  repeat-expansion / imprinting / mitochondrial / chromosomal); prevalence; age of onset; organ systems
  involved; cardinal symptoms.
- **Source:** NCBI Gene, ClinVar, dbVar (structural/CNV), PubMed (mechanism & prevalence primary literature).
- **Deliverable:** `data/curated/dossiers/<entity>.json` — structured, every field provenance-tagged and grade-tagged.

## Phase R3 — Burden indexing ("suffering order") **[investigation only]**

- **Goal:** apply the deterministic burden index (`BURDEN_INDEX.md`) to each entity from R2's collected inputs.
- **Deliverable:** `data/curated/burden_scores.csv` — component scores (onset, progression, severity,
  mortality, disability, treatability offset), composite, and an input-floor **grade** per entity.
- **Output property:** the resulting ordering is a **reproducible function of cited inputs** (VP-SPEC C1) —
  re-running the index on the same dossiers reproduces the same ranking (2× identical hash).
- **Optional annotation:** developmental/morphogenesis diseases get a baseline note from `code/emergence_v2/`
  (which engine quantity — `λ`, `γ`-threshold, dosage — the disease perturbs).
- **Status:** ✅ **complete (v0.4)** — `burden_scores.{csv,json}` (35 diseases, 5 graded axes; 17 placed,
  18 not-placed by the ≥3-axis rankability cut). Gate `reports/r3.gate.json` **PASS 9/9**. Treatability
  offset was deferred to R4 (now supplied; see below).

## Phase R4 — Treatment-mechanism survey **[investigation only]**

- **Goal:** for **treatable** diseases, record the established therapy and its **mechanism**, stated *only when
  mechanistically established* (enzyme replacement, substrate reduction, pharmacologic chaperone, antisense
  oligonucleotide / splice modulation, gene addition / editing, transplant, dietary restriction, etc.).
- **For incurable diseases:** flag as an **open problem**; mechanistic reasoning about candidate approaches is
  allowed but graded `[O]`/`[H]` with the obstacle named — **no fabricated cures** (constitution C-D3).
- **Source:** PubMed (mechanism & trial literature), GTR (testing → clinical actionability), MeSH.
- **Deliverable:** `data/curated/treatments.csv`
  `entity, modality, mechanism, evidence_status, grade, provenance`.
- **Status:** ✅ **complete (v0.5)** — `treatments.{csv,json}` (35 diseases; two honest [H] tiers,
  12/12 definition-tier corroborated, no fabricated cure) + residual re-ranking
  `burden_residual.{csv,json}` (post-treatment order). Gate `reports/r4.gate.json` **PASS 11/11**;
  R3 gate still PASS 9/9; engine pin drift-0. The accession-dated **[L]** treatment pass
  (FDA/GeneReviews/OMIM/Orphanet) is the deferred validation path.

---

## ▣ CONSOLIDATION GATE — "stop investigating, start writing"  **[PASS 10/10, this session]**

Before any Phase W work begins, all four R-phase datasets must pass:
1. **Provenance-complete** — every fact carries source DB + accession + retrieval date. ✅
2. **Internally consistent** — inheritance/mechanism classes agree across `disease_index`, dossiers, and treatments. ✅
3. **Grade-complete** — every quantitative field carries a grade; estimated/unavailable values are `[O]`, not guessed. ✅
4. **Scope-clean** — no excluded entity has leaked into the in-scope set (multi-system handling per `SCOPE.md`). ✅

This checkpoint is the explicit moment the project pivots from collection to VP-SPEC-governed authoring.

**Status:** ✅ **PASS (10/10)** — `reports/consolidation.gate.json` (`code/pipeline/consolidation_gate.py`,
living code). The gate **subsumes** R1–R4 (re-runs all four investigation gates and asserts each PASSes:
R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11) and then independently re-derives the four criteria above plus the
Erratum-E1 gene_function symbol sweep, constitution C-D3 (no fabricated cure), and engine-pin drift-0. It
writes **no whitepaper prose**. Running it surfaced and resolved **erratum E2** (one gene-less aggregate
dossier, Gaucher disease, carried an empty-string `variant_spectrum` grade instead of `[O]`; fixed at root in
the builder by mirroring the existing `gene_function` fallback — exactly one dossier changed, downstream
byte-identical; see `reports/CONSOLIDATION_NOTES_AND_HANDOVER.md`).

**Recorded W1-entry condition.** The two deferred `[L]` passes are **not** consolidation prerequisites — they
are accuracy upgrades scheduled as **early-W1 tasks**, and **until both land every W-phase use of the burden /
residual order must flag it as a provisional `[H]`-grade prioritisation device, not a registry-locked ranking**:
(1) treatment accession-dating (FDA label / GeneReviews Management / OMIM clinical management / Orphanet),
(2) natural-history registry pass (lift P/S/M/D `[H]`→`[L]`/`[V]`).

---

## Phase W1+ — Whitepaper authoring under VP-SPEC v1.8 **[English; full discipline ON]**

**▶ W1 underway. W1.1 + W1.2 COMPLETE (gate PASS 17/17).** The full 35-disease page set is built:
`tools/w1_build.py` deterministically emits **one standalone HTML per disease** (hub + framework §1 +
17 placed pages in residual-burden order + 18 not-placed pages + 2 mechanism-class chapters = 39 URLs),
gate `reports/w1.gate.json` PASS, all prior gates still green, engine pin drift 0. The R5 GeneReviews pass
**accession-dated 33/35 treatments to `[L]`** (2 honestly `[H]`, no therapy exists) and corroborated 21
burden axes `[H]→[L]`, with **no promotions** (corroboration-only; `[O]`-fill withheld as risky) so the
order is numerically identical to R4 and carried as provisional `[H]` cohort-wide (order_locked 0/35).
**Next: the natural-history registry pass** — the one remaining `[L]` upgrade — to lift the order toward
registry-locked and let not-placed promotions occur once ≥3 registry-grade axes are scored.

From here, every VP-SPEC v1.8 rule binds:

- **C1 reproducibility.** The burden index, the classification logic, and any derived ranking are
  deterministic, regenerated by a `tools/` module, and gate-checked (2× sha256, drift 0). **Clinical facts
  from NCBI are *observed* inputs — respected and cited, never claimed as "reproduced"** (C1: "관찰값은 존중한다").
  The whitepaper's *reproducible contribution* is the analysis layer built on those observed inputs.
- **C2 canonical HTML.** Sections are `docs/disease/<slug>/index.html`; no TeX bundled; rendered SVG for any display math.
- **C3 obstacle disclosure.** Incurable diseases, and any clinical magnitude not reproducible inside the
  package, are graded `[O]` with a named obstacle; `IRREPRODUCIBILITY_LEDGER.md` aggregates them.
- **C4 retrieval-readiness.** Each disease section opens with a 40–60-word `<p class="answer">`; each cited
  mechanism/quantity gets a self-contained card with grade + repro link; JSON-LD per page
  (`MedicalCondition` + `ScholarlyArticle`); answer-first, ≤3-sentence paragraphs.
- **Structure.** Hub (`docs/disease/index.html`) + **one standalone `docs/disease/<slug>/index.html` per
  disease — never grouped** (so Google/RAG can extract and rank each disease as its own passage). Each page
  carries inheritance · mechanism · burden score · treatment, all graded. Cross-cutting class chapters are
  separate pages that *link* the individual disease pages, never absorb them.
- **Gates.** VP-SPEC Phase 1/2/3 gates + constitution gates (C1/C2/C3) + search gate (C4), all PASS before handoff.

**Suggested W ordering** (revisited after the consolidation gate): highest-burden, well-characterized,
treatable monogenic systemic diseases first (clean mechanism + clean reproducible burden), then rare/ultra-rare
and incurable entities (where `[O]` sections dominate), then cross-cutting mechanism chapters (e.g., lysosomal
storage as a class, repeat-expansion as a class).

---

## Author actions deferred to later sessions (not done here)

- Register `disease`/`dis` (title, concept DOI, branch) in VP-SPEC §2 and `registry/cross_volume_doi.*`.
- Decide whether the whitepaper joins `jamming-physics.org` as a 10th volume or ships standalone first.
- Optional NCBI API key + contact email for higher E-utilities throughput (see `DATA_PROVENANCE.md`).

---

## One-line status

**R0–R4 done; consolidation PASS (10/10); Phase W1 site built (W1 gate PASS 17/17); R6/R7/R8/R9/R10/R11/R12/R13/R14/R15 COMPLETE.**
The full 35-disease per-disease site is built under VP-SPEC v1.8 discipline — one standalone HTML per
disease (hub + framework + 21 placed + 14 not-placed + 2 mechanism-class chapters = 39 URLs), deterministic,
JSON-LD + sitemap + crawler-allowed for Google/RAG discoverability, burden order carried as provisional
`[H]`. **Eleven registry `[L]` passes have now landed:** R5 accession-dated 33/35 treatments to `[L]`
(2 honestly `[H]`, no therapy); **R6** (Orphanet/Orphadata, PASS 14/14) lifted onset to registry `[L]`
(28/35) plus one mortality axis; **R7** (PASS 16/16) lifted **disability to `[L]` 13/35** from the openly
published **GBD 2013 disability-weights table** and corroborated 2 mortality axes from PMC survival
literature; **R8** (PASS 16/16) lifted **severity to `[L]`** for the one disease whose obligate dominant
sequela is annotated in the open **HPO Severity subtree (HP:0012824)** via a cited dominant-sequela join
(creating the 2nd order-lock); **R9** (PASS 15/15) lifted **progression to `[L]` 7/35** from curated **PMC
open-access** literature via a cited dominant-sequela join **whose tier is DERIVED by the frozen R3 tier
function** over the verbatim sentence (no new cut-points) — Niemann-Pick disease type A → tier 1.0, the
**3rd order-locked disease**; Duchenne MD corroborated to `[L]` but deliberately not locked (its severity
was honestly declined at R8); five considered statements declined and recorded
(spectrum/comparative/umbrella/historical/form-specific). **R10** (PASS 16/16) ran round 2 of the same curated-PMC-OA progression lift as a **dedicated cumulative stage over R9** (leaving every R9 artifact byte-identical): two **grade-only** corroborations — **Fabry disease** and **Marfan syndrome**, progression `[H]`→`[L]` with the value unchanged, **neither locking** — taking progression coverage to **9/35**; and three declines recorded (Hb SS disease P+S, Alpha-1-antitrypsin deficiency P) whose only retrievable open-access statement was umbrella/genotype-scoped or spectrum, so **no new order-lock and no new placement** (HbSS and AATD stay not-placed, now with these as permanent open-data-irreducible obstacles). **R11** (PASS 16/16) ran round 3 of the same curated-PMC-OA lift as a **dedicated cumulative stage over R10** (leaving every R9 and R10 artifact byte-identical): one **VALUE+GRADE severity** lift — **Marfan syndrome** severity `[H]`→`[L]` (0.50→0.75, tier **derived** by the frozen R3 function via 'life-threatening' from the disease-defining sentence) — which, because Marfan's onset, progression and mortality were already `[L]`, **completes its order-lock** (the **4th order-locked disease**, taking severity coverage to 4/35); and two declines recorded (Gaucher disease type I severity, Gaucher umbrella severity) whose only retrievable open-access statement was **comparative** (least-severe-of-three / "devastating" attributed to GD3), so both Gaucher severities stay `[H]`. **R12** (PASS 16/16) ran round 4 of the same curated-PMC-OA lift as a **dedicated cumulative stage over R11** (leaving every R9, R10 and R11 artifact byte-identical): two **severity** lifts — **Duchenne muscular dystrophy** severity `[H]`→`[L]` (0.50→0.75, **VALUE+GRADE**, tier **derived** by the frozen R3 function via 'severe' from the disease-defining sentence), which, because Duchenne MD's onset, progression, mortality and disability were already `[L]`, **completes its order-lock** (the **5th order-locked disease**, and the only cohort disease with all five axes scored and every one `[L]`), and **Tyrosinemia type I** severity `[H]`→`[L]` (0.75→0.75, **grade-only**, no lock — onset + mortality stay `[H]`), taking severity coverage to **6/35**; and two declines recorded (Hurler syndrome severity = comparative phenotype-class label, Beta-thalassemia severity = umbrella spectrum) plus a Hemophilia A frontier observation (only retrievable 'severe' framing is the factor-activity sub-phenotype "severe hemophilia A (FVIII < 1%)", recorded not forced into a decline). **R13** (PASS 16/16) ran round 5 over R12 (every R9–R12 artifact byte-identical): three lifts — **Maple syrup urine disease** severity `[H]`→`[L]` (0.50→0.75, **VALUE+GRADE**, via 'life-threatening'), **Cystic fibrosis** and **Glycogen storage disease type II / Pompe** progression `[H]`→`[L]` (**grade-only**) — **none locking** (MSUD retains onset `[H]`; CF and Pompe retain mortality `[H]`); two declines (Osteogenesis imperfecta comparative, Beta-thalassemia-adjacent alpha-Thalassemia umbrella) plus Hemophilia B + Becker MD frontier observations. **R14** (PASS 16/16) ran round 6 over R13 (every R9–R13 artifact byte-identical): three lifts — **Classic homocystinuria** and **Fabry disease** severity `[H]`→`[L]` (0.50→0.75, **VALUE+GRADE**, via 'life-threatening' / 'severe'), and **Becker muscular dystrophy** progression `[H]`→`[L]` (**grade-only**, via 'progressive' — advancing the R13 BMD frontier on a *different* axis with a clean BMD-specific sentence) — **none locking** (Classic homocystinuria retains mortality + disability `[H]`; Fabry retains mortality `[H]`; Becker retains severity `[H]`), taking severity coverage to **9/35** and progression to **12/35**; two declines recorded (Polycystic kidney disease 2 = PKD1-vs-PKD2 comparative, Osteogenesis imperfecta = moderate-to-mild umbrella spectrum). **R15** (PASS 16/16) ran round 7 over R14 (every R9–R14 artifact byte-identical): three **severity** lifts, all to tier 0.75 via 'severe' — **Acute intermittent porphyria** 0.50→0.75 (**VALUE+GRADE**; only 2 scored axes, sub-rankable, **no lock**), **Achondroplasia** `[O]`→0.75 (**previously-unscored axis**; becomes rankable but retains mortality `[H]`, **no lock**), and **Phenylketonuria** `[O]`→0.75 (**previously-unscored axis**) — and because PKU's onset and disability were **already** `[L]`, this **completes its order-lock as a disclosed CONSEQUENCE** (the **6th order-locked disease**; not engineered — S and D are orthogonal axes from different sources and the cited sentence passes every criterion independently), moving the lock set **5→6** and severity coverage to **12/35**; two declines recorded (21-Hydroxylase-Deficient CAH = form-specific severest-form salt-wasting, Hemochromatosis type 1 = high-vs-low-TSAT comparative) plus a Wilson disease frontier observation. The **§4 highest-value deliverable ships**: a
read-only, fully-graded **unmet-need / treatment-gap surface** (`data/curated/unmet_need_surface.*`,
gate PASS 6/6) — residual = `raw_burden·(1−e)`, framed as a research-prioritisation signal and never as
clinical advice; its honest headline (burden `[L]` + no disease-directed therapy) is **Achondrogenesis
type II and Niemann-Pick type A**, the latter locked precisely because R9 lifted its progression. The
**OMIM clinical-synopsis path stays REMOVED** (key unobtainable for an individual researcher), not deferred.
order_locked 6/35 (Achondrogenesis type II, Niemann-Pick type A, Tyrosinemia type II, Marfan syndrome, Duchenne muscular dystrophy, Phenylketonuria). All prior gates
still green (R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 · R7 16/16 · R8 16/16 · R9 15/15 · R10 16/16 · R11 16/16 · R12 16/16 · R13 16/16 · R14 16/16 · R15 16/16 · unmet-need 6/6 · W1 17/17 · boundary 6/6),
engine pin drift 0. **Next (R16, remaining `[L]` lift): the rest of severity/progression and mortality** — R9–R15 worked the curated-PMC-OA frontier to where the clearly defensible disease-level joins reach (NPD-A progression locked at R9; Fabry/Marfan progression grade-only; Marfan severity completing its lock at R11; Duchenne MD severity completing its lock at R12; MSUD severity + CF/Pompe progression at R13; Classic homocystinuria/Fabry severity + Becker MD progression at R14 — none of those completing a new lock; AIP/Achondroplasia/PKU severity at R15, of which **PKU completes its order-lock as a disclosed consequence** since its onset+disability were already `[L]`), with HbSS and AATD obstacle-bound and the Gaucher / Hurler / Beta-thalassemia / Osteogenesis imperfecta / PKD2 / 21-OHD CAH / Hemochromatosis type 1 statements declined (comparative / umbrella-spectrum / sub-phenotype / form-specific) and Wilson disease a recorded frontier. With **17 placed diseases still carrying an `[H]` axis** (overwhelmingly severity), R16 continues the **same** rule on the remaining axes as a **new cumulative stage** (leaving all prior artifacts byte-identical, never widening the cut-points) — the path to any further order-locks and not-placed promotions, toward the completion-declaration criterion. If a lift again completes a lock, disclose it as a consequence (as PKU was at R15) and let the gate's `order_lock_change_documented` check assert the exact delta.
`reports/R15_NOTES_AND_HANDOVER.md`.
