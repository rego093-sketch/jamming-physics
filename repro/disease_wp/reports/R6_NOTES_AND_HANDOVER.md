# R6 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.8, phase W1.3)

Phase W1.3 executed the **second and last named deferred `[L]` pass**: the natural-history registry
read of the burden axes. Single author (Young Jae Lee, ORCID 0009-0002-7535-8245). English
deliverables, VP-SPEC v1.8 discipline (no-tuning, bit-reproducible, honest grading). All gates green;
engine pin drift 0.

With R5 (treatment accession-dating) and R6 (here) both landed, every upgrade flagged since R3/R4 is
now done. What remains open is **named and bounded** (severity / disability / most progression), not a
deferred pass.

## 1. Why Orphanet, and why it is a real upgrade over R5

R5 (GeneReviews) deliberately ran **corroboration-only**: a definition tier was confirmed against free
chapter prose, but the *value* was frozen, because a single first-match over a ~6 kB chapter
over-triggers and is the only path that would move `raw_burden`. R6 removes that limitation honestly by
choosing a source whose fields are **structured and entity-anchored** — Orphanet/Orphadata — so every
value attaches to an ORPHAcode and the "entity-anchored read" is automatic, not a free-text guess.
Therefore a registry `[L]` from Orphanet is allowed to **supersede** a prior `[H]`/`[O]` and **move
`raw_burden`**. The OMIM clinical synopsis was *not* used: it is licensed/copyrighted and needs a key,
and a structured-but-citeable source already exists.

## 2. The two stages (living code, NOT in the engine pin)

- **`code/pipeline/r6_orphanet_fetch.py`** (sha 2d8bf0101cdb): network, idempotent, sha-pinned; caches
  three Orphadata products under `data/raw/orphanet/` and writes `_fetch_log.json`:
  - `en_product1.xml` — sha fb2fbe8cc3f0, 11,456 disorders — OMIM↔ORPHA cross-refs **with mapping
    relation** (E exact / BTNT / NTBT).
  - `en_product9_ages.xml` — sha c8dba4d4a424, 7,374 — `AverageAgeOfOnset` + inheritance.
  - `en_product4.xml` — sha 82079cfb9e6f, 4,337 — HPO phenotypes per ORPHAcode **with Orphanet
    frequency**.
- **`code/pipeline/r6_naturalhistory_registry.py`** (sha ed20bb4830fb): NO network; imports the FROZEN
  R3 builder via importlib (tier maps, HPO subtree roots HP:0040006 / HP:0031797, composite,
  sensitivity), reads the R5 registry base + the Orphanet cache, and OVERWRITES `*_registry.{json,csv}`
  (cumulative R5+R6). **Self-healing / idempotent:** if its input already carries R6 (an accidental
  re-run), it regenerates the clean R5 base first, so re-runs are byte-stable. The canonical pipeline is
  `r5 → r6`; the gate runs that chain.

## 3. Declared, a-priori lift rules (recorded in the output + BURDEN_INDEX.md; gate-enforced)

- **JOIN — Exact only** (relation `E` in `en_product1`); BTNT/NTBT recorded as context, no lift.
  27/35 diseases exact-mapped; 8 have no exact mapping and take no lift.
- **Onset (O)** ← earliest `AverageAgeOfOnset` on the fixed earliness tier map
  {Antenatal/Neonatal 1.0 · Infancy 0.85 · Childhood 0.7 · Adolescent 0.55 · Adult 0.35 · Elderly 0.2};
  "All ages"/"No data" record but do not lift. Registry `[L]` supersedes `[H]`/`[O]`.
- **Mortality (M)** ← `en_product4` HPO under HP:0040006 with an R3 `MORT_VAL` tier AND frequency ≥
  Frequent. **Progression (P)** ← HP:0031797 with a `PROG_VAL` tier AND frequency ≥ Frequent.
- **Frequency gate** = {Obligate, Very frequent, Frequent}.
- **Severity (S) / Disability (D)** — NOT lifted; Orphadata has no magnitude tier (obstacle sharpened).
- **Add-only** — Orphanet absence never downgrades a banked value.

## 4. Honest results (the headline)

- **Onset `[L]` 25 → 28.** Breakdown: 9 corroborated, 6 extended-earlier (value moved to an earlier
  Orphanet category), 2 `[H]→[L]`, 1 `[O]→[L]`; 4 stay `[H]` ("All ages"-only), 3 stay `[O]`.
- **Mortality `[L]` 7 → 8** — only Hurler syndrome (0.7 `[H]` → 1.0 `[L]`), the one disease with an
  Orphanet Mortality/Aging term at ≥ Frequent.
- **Progression unchanged** (5 `[L]`) — **honest null**: no qualifying Clinical-course term at ≥ Frequent
  for this cohort.
- **Severity / Disability unchanged** — no Orphadata magnitude tier; the obstacle is now recorded as
  "consulted, no tier, deferred," not merely "no HPO branch."
- **Promotions: 0.** Onset was already scored for most placed diseases, and no not-placed disease reaches
  ≥ 3 registry-grade axes without an S/D tier. This is the data's answer, not a shortfall.
- **`order_locked` 0 → 1 = Tyrosinemia type II.** Its three scored axes are O `[L]` (Orphanet onset),
  S `[L]` and D `[L]` (both R5 GeneReviews-corroborated). So its burden **value** is registry-grade.
  The cohort **order** is still provisional `[H]` — its *rank* depends on `[H]`-valued neighbours — so the
  provisional flag is held cohort-wide and Tyr-II's page carries an explicit value-vs-rank note. (This is
  deliberately stricter than the R5 handover's loose "drop the flag" phrasing.)
- **Axis VALUE changes** (registry supersedes; `raw_burden` re-derived & gate-checked): NPD-A O 0.85→1.0 ·
  Becker O 0.35→0.7 · Fabry O 0.55→0.7 · Hurler O 0.85→1.0 & M 0.7→1.0 · GSD-II/Pompe O 0.35→1.0 ·
  Tyr-II O 0.85→1.0 · 21-OH-CAH O 0.35→1.0 · AIP O 0.35→0.55 · factor VIII O —→1.0.
- **Coverage after R6** (over 35): O `[L]`28/`[H]`4/`[O]`3 · P 5/9/21 · S 2/22/11 · M 8/9/18 ·
  D 4/4/27 (80 `[O]` axis cells total). **Sensitivity** (Spearman vs equal default): equal 1.00 ·
  onset 0.917 · mortality 0.995 · severity 0.944 · drop-disability 0.985.
- Registry digests: `burden_scores_registry` 6e9017984291 · `burden_residual_registry` 59fd22716c82 ·
  `treatments_registry` 8b3eb63b1496 (byte-identical to R5 — R6 does not touch the treatment layer).

## 5. R6 gate — `code/pipeline/r6_gate.py` (sha a03033bc1588) — PASS 14/14

`reports/r6.gate.json` (sha ae2ed3e3dc75). Re-derives every claim independently and proves the chain
deterministic (registry-set sha fd5f750c9141, 2×): determinism_chain_2x · orphanet_sources_pinned ·
banked_unchanged · join_exact_only · onset_tier_map_a_priori · frequency_gate_enforced (re-checked against
`en_product4`) · addonly_no_downgrade · supersede_only_on_registry · raw_burden_rederived ·
rankability_and_promotions · residual_correct · order_lock_rule · sensitivity_present · engine_pin_drift_zero.

## 6. W1.3 site/prose update — `tools/w1_build.py` (sha 074f2f13b201)

The W1 prose still described the natural-history pass as "deferred / the one remaining upgrade." It is now
accurate: per-disease pages state which axes are registry `[L]` for that disease (onset cited to Orphanet);
Tyr-II carries the order-locked value note; every page names the precise remaining obstacle (no Orphadata
severity/disability/typical-course tier → OMIM clinical synopsis (licensed) / GBD / published literature).
Framework honest-limitation, hub, the 18 not-placed upgrade-path notes, `_meta.json`, `llms.txt`, and the
builder-generated `IRREPRODUCIBILITY_LEDGER.md` (counts now computed from the registry) are all updated.

**Two builder bugs fixed in this pass:**
1. **Stale-output orphans.** The build never cleaned its output dir, so when R6 reordered the residual
   ranking the old `<rank>-<slug>/` page directories from prior builds lingered (55 dirs / 17 duplicate
   slugs, e.g. an orphan `14-hurler-syndrome` beside the correct `12-`). `main()` now prunes every
   `docs/disease/` subdirectory before regenerating → 38 page dirs, no dups. The site is now reproducible
   across reorders (this was a latent reproducibility hole independent of R6).
2. **Stale treatment paragraph.** The framework page still read "treatment evidence is uniformly `[H]` …
   deferred," which had been false since the R5 accession-dating. Corrected to 33/35 `[L]`, matching the
   per-disease pages.

W1 gate `tools/w1_gate.py` (sha 323e203e1d8c, unchanged) PASS 17/17 with the R6 numbers; site-set sha
**5c81ff0c14cb** (2× identical). Retrieval surface unchanged in shape: sitemap 39 URLs, llms.txt, `_meta`,
ledger all regenerated.

## 7. State and what is genuinely left

All gates green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 · W1 17/17. Engine
pin drift 0 (15/15).

**Remaining `[L]` lift (the only open accuracy item):** severity, disability, and most progression have no
structured tier in Orphadata. The path is the OMIM clinical synopsis (licensed — needs access), GBD
disability weights, and published functional & survival literature. Until that lands:

- the burden **order** stays a provisional `[H]` prioritisation device cohort-wide (one disease's *value*
  is registry-locked, but no *ranking* among `[H]` neighbours is registry-trustworthy);
- not-placed promotions still await ≥ 3 registry-grade axes (which, for the gene-mapped not-placed
  diseases, now turns entirely on getting an S or D magnitude — onset alone is not enough).

Everything else — classification, mechanism, the deterministic burden machinery, treatment accession-dating,
and onset — is in place, cited, graded, and reproducible.
