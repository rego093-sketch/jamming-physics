# R7 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.9, phase R7)

Phase R7 closed the **open DISABILITY axis** that R6 named, using the canonical, openly published
**GBD 2013 disability-weights table**, and attempted the open **MORTALITY** path from PMC survival
literature. Single author (Young Jae Lee, ORCID 0009-0002-7535-8245). English deliverables, VP-SPEC
v1.8 discipline (no-tuning, bit-reproducible, honest grading). All gates green; engine pin drift 0.

R6 left exactly two axes open with **no structured registry source**: disability and severity. R7
closes disability honestly and bounds severity precisely. The R3/R4 BANKED files stay byte-identical
(gate-verified); the registry layer (cumulative R5+R6+R7) is what advances.

## 1. The OMIM decision — worked around, not used (per directive)

The intended SEVERITY source was the OMIM clinical synopsis. It is **worked around**, not scraped:

- OMIM is **not an institutional licensee here and no short-term API key is obtainable**.
- Its canonical reproduction path (the pinned `bash`/`curl` fetch every gate re-runs) is
  **datacenter-IP-blocked (HTTP 403)**; `web_fetch` returns only the homepage shell, no structured
  synopsis, and nothing sha-pinnable.
- Baking values obtained out-of-band into the pipeline would therefore **break bit-reproducibility**
  (a second party re-running the canonical path could not reproduce them) and violate the no-tuning
  discipline.

So `r7_omim_synopsis_fetch.py` is coded to **clean-skip without a key** (status `SKIPPED`, obstacle
recorded, `exit 0`), and R7 substitutes **open** sources for what they can honestly carry:
**disability ← GBD** (strong, structured, citeable) and **mortality ← PMC** (corroboration-only).
There is **no open structured severity tier**, so severity takes **no lift** — the obstacle is recorded
on each `[O]` severity axis, never guessed.

## 2. The four stages (living code, NOT in the engine pin)

- **`code/pipeline/r7_gbd_dw_fetch.py`** (sha a5b609b656ed): network, idempotent, sha-pinned. Downloads
  the Salomon JA et al. *"Disability weights for the GBD 2013 study,"* Lancet Glob Health 2015;3(11):e712-23
  appendix (`mmc1.pdf`, Elsevier gold-OA CDN, CC BY) — **PDF sha c7d22442bad8** (695,121 B) — runs
  `pdftotext -layout`, deterministically parses the two-column table taking the **GBD2013 estimate
  (LEFT column)**, and writes `data/raw/gbd/gbd_disability_weights.json` (233 health states).
  **6 anchor self-checks** guard the GBD2013-vs-2010 column read and the parser; the stage exits nonzero
  on any mismatch. 6/6 pass.
- **`code/pipeline/r7_omim_synopsis_fetch.py`** (sha 573f8f89513b): the worked-around stage above —
  clean-skip without a key; full key-present fetch logic included but dormant.
- **`code/pipeline/r7_litsurvival_fetch.py`** (sha ce781c0eeca1): NCBI E-utilities (no key, <3 req/s).
  Per disease, a **title-anchored** PMC OA query (the disease token must appear in `<article-title>`);
  full-text XML cached + sha-pinned per CUI. **30/35** cached; 5 not found (Hb SS, factor VIII, factor IX,
  hemochromatosis, β-thalassemia — and β-thal/FVIII/FIX are promoted by the disability pass anyway).
- **`code/pipeline/r7_naturalhistory_registry2.py`** (sha 353e8e7d9ee6): no network; imports the **frozen
  R3 builder** via `importlib` for tier maps / composite / sensitivity. Writes the separate
  `data/curated/*_registry.{json,csv}` (cumulative R5+R6+R7); self-healing/idempotent.

## 3. Declared, a-priori rules (no tuning; recorded in the output + BURDEN_INDEX.md)

- **DISABILITY (D) ← GBD 2013 disability weight** of the disease's single dominant untreated-natural-
  history functional sequela, via the **cited curation join** `methodology/gbd_dw_join.csv`
  (sha 2314174f7379; 10 rows, one disease → one named GBD health state, each with a clinical evidence
  basis). The published dw is binned to the BURDEN_INDEX disability tier by cut-points declared a priori:
  **dw<0.10 → 0.2 · 0.10–0.30 → 0.5 · 0.30–0.55 → 0.75 · >0.55 → 1.0**. GRADE = **`[L]`** (curation join,
  not a disease-specific measured distribution — the same conservative call R6 made for onset); the raw
  dw + 95% UI are recorded, and the join is validated at runtime against the pinned DW table. Multi-domain
  / variable / mortality-dominant diseases are **not** mapped (`methodology/gbd_dw_excluded.csv`,
  sha 5a810f379a97; 9 rows, each with a specific reason). Registry `[L]` **supersedes** a prior `[H]`/`[O]`;
  an existing `[L]` is corroborated (max, add-only).
- **MORTALITY (M) ← PMC survival literature, CORROBORATION ONLY.** An entity-verified article whose text
  contains a sentence with a quantitative **disease-typical** survival / age-of-death / explicit-lifespan
  figure **agreeing** with the banked M band adds the published citation (PMCID + exact sentence) and
  promotes an `[H]` M to `[L]`. A fixed EXCLUDE filter drops model/treated/subgroup/comparison sentences.
  **Free text does NOT fill an `[O]` mortality axis.** M values are never changed.
- **SEVERITY (S) / PROGRESSION (P) NOT lifted** — no open structured source (see §1). Obstacle recorded,
  never guessed. **ADD-ONLY** throughout — a missing GBD mapping or PMC sentence never downgrades a value.

## 4. Results (all gate-verified)

- **Disability coverage (the headline): `[L]` 4 → 13 / 35** (was `[O]`27/`[L]`4/`[H]`4 → now
  `[O]`21/`[L]`13/`[H]`1). 10 mapped (6 `[O]`→`[L]`, 3 `[H]`→`[L]`, 1 `[L]` corroborated); 9 declined and
  recorded; 13 kept `[O]` with obstacle.
- **PKU correction:** D 0.75`[H]` → **0.5`[L]`** — the definition tier had overstated it; the GBD
  Intellectual-disability-severe weight (dw=0.160) bins to 0.5. A published value *lowering* a guess is
  the discipline working as intended.
- **4 promotions** (not-placed → placed, each now 3/5 on the new disability axis): **Beta-thalassemia,
  Hereditary factor IX deficiency, Hereditary factor VIII deficiency, Maple syrup urine disease**.
- **Mortality:** **2 corroborations**, both on already-`[L]` axes — Achondrogenesis type II ↔ PMC12692501
  (*"death usually … in utero or … the early neonatal period"*); Hurler ↔ PMC13090637 (*"untreated median
  lifespan … under 10 years"*). Citations added; **no grade/coverage change**. The free-text `[O]`-fill is
  an **honest null**: empirically the matched sentences were overwhelmingly treated-cohort / comparison /
  non-mortality noise — the over-trigger risk R5 withheld for, confirmed. Conservative misses (e.g. OI's
  reduced-life-expectancy line) were left uncited rather than loosen the extractor.
- **order_locked unchanged at 1** (Tyrosinemia type II). A disability lift alone creates no new lock while
  S/P/M stay `[H]` for the rest; a new lock now needs **severity**, which has no open source.
- Axis-grade coverage after R7 (over 35): O `[L]`28 · P `[L]`5 · S `[L]`2 · M `[L]`8 · **D `[L]`13**.
  Sensitivity (Spearman vs equal default): equal 1.00 · onset 0.921 · mortality 0.990 · severity 0.924 ·
  disability 0.937 · drop-disability-core4 0.892. `treatments_registry` sha **8b3eb63b1496** unchanged.

## 5. Gate

`code/pipeline/r7_gate.py` (sha b357ee652d47) **PASS 16/16** (`reports/r7.gate.json`). Re-derives every
claim independently and proves the **r5→r6→r7 chain deterministic** (2× identical, registry-set sha
5641ac51b00f): determinism · banked-unchanged · **GBD PDF sha==pin + 6/6 GBD2013 anchors re-parsed** ·
GBD-join-anchored-cited · a-priori-cut-points · excluded-recorded · add-only-no-downgrade ·
supersede/corroborate-only · **PMC corroborations re-found in cached text, signal+exclude+direction
re-checked, 0 illicit `[O]` fills** · S/P-not-lifted · OMIM-skip-recorded · raw-burden-rederived ·
rankability+promotions(4) · residual-correct · order-lock+sensitivity · engine-pin-drift-zero.

## 6. W1.4 site sync

`tools/w1_build.py` (sha 39fc427a7c70) — narrative brought into line with reality: per-disease pages name
the GBD 2013 disability-weights table as the disability source; the registry note credits R6 (onset) +
R7 (disability + PMC mortality corroboration) and states that severity/most-progression have no open
structured source (OMIM licensed/keyless); framework limitation, hub reading-order, not-placed notes,
`_meta.json`, `llms.txt`, and the builder-generated `IRREPRODUCIBILITY_LEDGER.md` (74 `[O]` cells, was 80)
updated. **Numbers stay data-bound from the curated CSVs — only framing was edited.** `tools/w1_gate.py`
(unchanged, sha 323e203e1d8c) **PASS 17/17**; site-set sha **6d319dd166f8** (2× identical; was 5c81ff0c14cb).

## 7. Severity — investigation closeout (the one remaining open axis)

The **one** remaining named `[L]` lift is **SEVERITY** (33/35 diseases still `[H]`/`[O]`). It was investigated
exhaustively across every open source reachable from NCBI/this environment; the honest finding is that **no open
source carries a disease-level severity-magnitude tier**, so severity stays `[H]`/`[O]` with the obstacle named.
Sources checked and why each fails:

- **Orphadata (Orphanet, R6)** — no structured severity-magnitude field at all.
- **HPO severity modifiers (`phenotype.hpoa`, cached)** — only **4/35** cohort diseases carry *any* severity
  modifier, and each is a single **feature-level** modifier on one phenotype (e.g. OI → one phenotype tagged
  "Mild"), not a disease-level assessment. Using it as the disease's tier is a category error (a disease that
  ranges mild→lethal is not "Mild" because one of its features is). Honest null.
- **GeneReviews "Clinical characteristics" / "Clinical Description" (R5 cache) and PMC OA (R7 cache)** — the
  disease-level severity statements are overwhelmingly **spectrum/range** language ("ranges from mild to severe,"
  "continuum from perinatal-lethal to asymptomatic," "spectrum of phenotypes ranging from the severe classic
  …"). A single tier (0.25/0.5/0.75/1.0) cannot be read from a range without **inference** — which is exactly
  what earns `[H]`, not `[L]`. The few entity-specific "severe" mentions (Hurler, MSUD-classic) would *change*
  the banked value on a single free-text word, the same inference problem. So a free-text severity pass would
  relabel inference as registry-grade; it is **deliberately not done**.
- **OMIM clinical synopsis — the only disease-level source — re-tested.** Correction to an earlier note: the
  OMIM **API host `api.omim.org` IS reachable from this environment** (the earlier "403/IP-blocked" was the
  *website* `www.omim.org`, which bot-blocks; the API is a separate Cloudflare-fronted host). The keyless API
  returns `HTTP 400 "An API key is required"` and a malformed key returns `"Invalid API key string length,
  expected 22 characters"` — i.e. it is **auth-gated, not IP-blocked**: a valid 22-char OMIM API key would work
  directly from here. But the key is **unobtainable** (no institutional registration available), so the OMIM
  path stays closed and `r7_omim_synopsis_fetch.py` continues to clean-skip. Note that even *with* OMIM, the
  synopsis is a categorised **feature list**, not a numeric severity tier, so severity would still be a declared
  curation mapping → `[L]` (like the GBD disability join), not `[V]`.

**Conclusion:** v0.9 is the honest, complete endpoint. Forcing severity to `[L]` from any reachable open source
would require inference the discipline forbids; an honest `[H]`/`[O]` with a precisely named obstacle is correct.

### Next phase (R8 candidate) — the only two discipline-compatible severity paths
1. **An OMIM API key** (confirmed it would work from this environment): set `OMIM_API_KEY`, activate the dormant
   fetch, map the clinical-synopsis content to the declared S tier per MIM (entity-anchored, add-only, `[L]`).
   The raw OMIM dump stays local (licensed; gitignored); the published artifact carries derived S `[L]` tiers +
   MIM citations, reproducible by re-fetching with one's own key.
2. **A deliberate human-in-the-loop per-disease curation** from open, *citeable* sources the curator points at
   (specific PMC IDs / Orphanet ORPHAcodes / GeneReviews NBKs), each tier explicitly approved — `[L]` curation
   with recorded human judgment, honestly graded, not auto-extracted from free text.

Either way: re-run the full chain (r5→r6→r7→r8) + all gates, keep R3/R4 banked byte-identical, re-sync the W1
site, and bump VERSION.
