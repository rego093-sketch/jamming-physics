# W1.2 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.7)

Phase W1.2 executed the two deferred accuracy passes and completed the volume's page set.
Single author (Young Jae Lee, ORCID 0009-0002-7535-8245). English deliverables, VP-SPEC v1.8
discipline (no-tuning, bit-reproducible, honest grading). All gates green; engine pin drift 0.

## 1. R5 — treatment accession-dating + natural-history corroboration (GeneReviews)

Two new pipeline stages were added under `code/pipeline/` (living code, NOT in the engine pin):

- **`r5_genereviews_fetch.py`** (sha f1fbcbb5ea81): pulls the GeneReviews chapter for each of the
  35 diseases via NCBI E-utilities (`db=books`, `gene[book]`), extracting the NBK accession, the
  initial-posting and last-revision dates, the page sha256, and the Management / Natural-History /
  Summary section text. Cache: `data/raw/genereviews/<cui>.json` + `_fetch_log.json`. Two disjoint
  match paths: a **curated `cui→NBK` map** (clinically-named or shared-gene chapters, each confirmed
  by direct fetch with a gene-in-body cross-check) and **title-only auto-discovery** (gene-in-title
  OR distinctive-token-in-title). Result: 35/35 chapters matched.

- **`r5_accession_apply.py`** (sha ea0aeaffdc9a): NO network; imports the FROZEN R3 lexicon via
  importlib. Writes SEPARATE `data/curated/*_registry.{json,csv}` so the R3/R4 banked files stay
  byte-identical (the R3 builder regenerates from dossiers and would otherwise revert any lift).

### Honest results (the headline)
- **Treatments: 33 [H]→[L]**, **2 [H]**. The 33 are accession-dated to the GeneReviews
  Management/Summary section (NBK + initial-posting/last-revision dates + the specific drug term that
  corroborates the curated modality — e.g. vosoritide, nitisinone, alglucosidase alfa, agalsidase,
  cysteamine, hydroxyurea, emicizumab, tolvaptan, sapropterin/pegvaliase). The 2 retained `[H]` are
  **evidence_status = none** (Achondrogenesis type II; Niemann-Pick disease type A): no
  disease-directed therapy exists, so there is nothing to accession-date — a bare disease-name or a
  why-it-fails drug mention must not manufacture a treatment `[L]`.
- **Burden axes: 21 [H]→[L] corroborated**, 28 kept `[H]` (discrepancy), **0 `[O]`-fill**, 81 `[O]`
  kept. Policy is **CORROBORATION-ONLY**: an axis lifts to `[L]` only when the frozen lexicon's
  independent read of the GeneReviews natural-history text AGREES with the definition-derived tier
  (value never changes → raw_burden cannot move). `[O]`-fill was deliberately **WITHHELD**: a single
  first-match over a ~6 kB chapter returns whatever top-severity word appears anywhere (often in a
  differential-diagnosis or variant-spectrum sentence), so it is not a sound basis to SET a
  previously-absent value — and it is the only path that would move raw_burden and promote a
  not-placed disease. The withheld lexicon suggestion + accession are RECORDED on each open axis's
  basis, so the deferred opportunity is documented, not hidden.
- **No promotions.** No not-placed disease reached 3 registry-scored axes. The residual ORDER and the
  placed/not-placed split are **numerically identical to R4** (burden_residual_registry self-checks
  byte-identical to the banked R4 residual). The pass lifts GRADES only.
- **order_locked = 0/35.** Every placed disease retains ≥1 `[H]` axis (HPO carries no severity or
  disability branch, so those axes are definition-inferred and GeneReviews did not corroborate all of
  them). Therefore the burden order stays a provisional-`[H]` prioritisation device cohort-wide; the
  flag is held on every placed page and the hub.

### Pre-registered rule honoured
The R3/R4 handover pre-registered: *if [O]-fill proves risky, do grade-lift ONLY and report honestly
rather than fabricate promotions.* The audit demonstrated the risk (Cystinosis S=1.0; three
adult-normal-lifespan diseases getting O=1.0 "congenital" from differential-diagnosis text), so the
rule was followed exactly — corroboration-only grade lift, no promotions.

### Fetch bugs found and fixed during R5
- **Pompe / GSD II GAA-symbol collision.** Auto-discovery matched NBK599589 = "GAA-FGF14-Related
  Ataxia" (a spinocerebellar ataxia; "GAA" is both the Pompe gene and the FGF14 repeat motif).
  Corrected to the curated **NBK1261 "Pompe Disease"** (GAA + enzyme replacement + alglucosidase
  confirmed in body). Gene-in-title alone is now known to be insufficient for symbol-collision genes.
- **Vosoritide extraction.** For achondroplasia (NBK1152, a correct match) the drug sits in the
  chapter **Summary** box ("Management. Targeted therapies: Vosoritide…"), which the section
  extractor did not capture. A **Summary-section** extraction was added and treatment corroboration
  now reads Management + Summary. Both fixes turned the 2 wrongly-`[H]` treatments into honest `[L]`.

## 2. Site generator extended (`tools/w1_build.py`, sha 9956701facd5)

- Reads the **registry CSVs** when present (treatment grades show `[L]`; order_locked available);
  falls back to R3/R4 banked files. All prior column reads unchanged.
- Placed disease pages now show the **GeneReviews accession** in the treatment evidence tier when the
  treatment is `[L]` (NBK link + posting/revision dates + corroborating term), instead of the old
  "deferred" text.
- **18 not-placed disease pages authored** (§19–36), each on its own URL with the same SEO surface
  (disease-name `<title>`, answer-first 40–60 w, abstract, claim strip with `[O] not placed` badge,
  MedicalCondition + ScholarlyArticle + Breadcrumb JSON-LD, organ + axis tables, treatment section).
  Framing is honest: *not placed — N of 5 burden axes scored (cut three of five); the remaining axes
  stay graded open `[O]`, not guessed.* No partial composite is used to rank them.
- **2 mechanism-class chapters authored** (§37–38): **Lysosomal storage and transport disorders**
  (7 members) and **Fibrillar collagenopathies** (4 members). A class chapter LINKS its member
  disease pages (ScholarlyArticle + ItemList + Breadcrumb JSON-LD, `[F]` marker) and does not restate
  them; membership is read from the curated dossiers' gene/mechanism, so the class list is
  reproducible. **Repeat-expansion was requested but has ZERO systemic-cohort members** — those
  diseases are neurological and owned by the sibling neuro volume — so collagenopathy was substituted
  as the second class and the absence is stated on the hub. (Hemoglobinopathy — alpha-thal, beta-thal,
  Hb SS — is a further candidate if a third class is ever wanted.)
- Hub, `_meta.json`, `sitemap.xml`, `llms.txt`, and `IRREPRODUCIBILITY_LEDGER.md` updated to cover the
  full set. Sitemap now lists **39 URLs** (1 hub + 1 framework + 17 placed + 18 not-placed + 2 class).
  The ledger's volume-level treatment row now reads 33×[L] / 2×[H] (none), and an explicit row records
  that GeneReviews `[O]`-fill was withheld.

## 3. Gate updated (`tools/w1_gate.py`, sha 323e203e1d8c) — PASS 17/17

Rewritten to read the registry CSVs and map all page roles format-independently (by JSON-LD content:
MedicalCondition → disease, placed vs not-placed by rankability; ItemList → class chapter). New/changed
checks: `structure_full_set` (17+18+2); `not_placed_honest`; `class_links_members` (no orphan, `[F]`
marker, membership read from `w1_build.CLASSES`); `treatment_grade_honest` (replaces the old
"treatments must be `[H]`" assertion — now every `[L]` must carry a GeneReviews NBK accession shown on
the page, hedged "curative intent" is allowed, an unhedged disease-level cure claim is not); sitemap
URL count derived from `_meta.json` (not hard-coded).

## 4. Verification snapshot (v0.7)

- Determinism: `w1_build.py` run twice → site-set sha **0aaa244a7a09** (identical).
- Gates: **R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · W1 17/17** (59 checks).
- Engine pin `MANIFEST_governed.sha256` verifies OK — **drift 0 (15/15)**. R5 code, W1 tools, and docs
  are living artifacts, intentionally NOT in the frozen engine pin; the R3/R4 banked files are
  byte-identical (proven by R3/R4 gates regenerating from dossiers and still passing).
- Digests: w1_build 9956701facd5 · w1_gate 323e203e1d8c · r5_fetch f1fbcbb5ea81 ·
  r5_apply ea0aeaffdc9a · w1.gate.json c33227227e24 · sitemap 71abdd0058c8 · llms 3555e7bb65a8
  (4479 B) · _meta dc00043d45bb · ledger 26c60aacac2a · burden_scores_registry 0413f0fd66cd ·
  treatments_registry 8b3eb63b1496 · burden_residual_registry c90bbf871848.

## 5. What remains open (named obstacles, honest)

- **Natural-history registry pass** — the single remaining `[L]` upgrade. A sentence-level,
  entity-anchored read of Orphanet / OMIM clinical synopsis / published survival could (a) lift the 81
  open axis cells and the 28 discrepant `[H]` axes toward `[L]`/`[V]`, and (b) once a placed disease
  reaches all-`[L]` across ≥3 axes, drop its provisional-`[H]` flag (order_locked). Until then the
  burden order remains provisional `[H]` cohort-wide.
- **Promotions of not-placed diseases** depend on that same pass scoring ≥3 registry-grade axes for a
  currently sub-threshold disease.
- **Volume DOI** — disease/dis not yet registered in VP-SPEC §2 (shown "pending" everywhere).
- **Gaucher aggregate (C0017205)** gene-less fields stay `[O]`; the gene-resolved Gaucher type I page
  carries the molecular detail.
