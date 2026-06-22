# CHANGELOG — VP Inheritance Kit

## v0.19.0-heldout-positives-published (writing pass: the FV7 `−`-arm and FV8 `+`-arm held-out POSITIVES are PUBLISHED into §15 — the corrective sign-law's bidirectional held-out validation is now on the canonical site; no new science, no new chapter, no new battery, no regression)
A **writing pass** that publishes the two turnkey items that previously stood in `HANDOVER.md` §3 (the deferred FV7 v0.17.0 and FV8 v0.18.0 §15-extensions). `tools/build_site.py` now extends the existing **§15 (the (B) held-out validation)** with **two** new subsections — *"The sign-law's `−` arm, scored on held-out data — the first held-out positive"* (FV7) and *"The sign-law's `+` RESTORE arm, scored on held-out data — the bidirectional close"* (FV8) — placed after the FV6 *"The null is a partition…"* subsection and before the *"What (B) moved"* close. **No new chapter (stays 19), no new battery (FV stays one, §15).** Every displayed number flows from `reports/emergence_results.json` → `FV_feasibility_validation` (tests FV7/FV8) via the `num()`/`R()` zero-drift helpers; nothing is hand-typed.

**What is published (numbers, all verbatim from the reports).** FV7 (`−` arm, held-out DepMap 24Q2 CRISPR-KO, figshare `25880521`): n = **16** onco (7 GOF / 9 LOF), **point-biserial(GOF, −gene-effect) = +0.4940**, **exact one-sided p = 0.0227** (11440 perms), per-gene **12/16** (GOF **7/7**); identified — **point-biserial(sign,GC) = −0.1222** (GOF mean GC **0.532** vs LOF **0.543**, balanced), GC-partialled **+0.4939**; 8 neurodegen out-of-scope. FV8 (`+` RESTORE arm, held-out Horlbeck 2016 hCRISPRa-v2 K562, *eLife* **19760**, DOI `10.7554/eLife.19760`, supp 10): n = **16** onco (9 LOF / 7 GOF), **point-biserial(LOF, −growth) = +0.4852**, **exact one-sided p = 0.0274** (11440 perms), per-gene **10/16** (LOF **7/9**); identified — **point-biserial(sign,GC) = +0.1222** (LOF mean GC **0.543** vs GOF **0.532**, balanced), GC-partialled **+0.4731**; 9 neurodegen out-of-scope. Each subsection keeps the firewall visible (reads only the **sign** of the separation, never a magnitude; γ untouched) and the honest caveats intact (the labels are frozen priors, not a fresh discovery; FV7's 4/9 pan-essential LOF push against; K562 is a single TP53-null / CDKN2A-deleted CML line that pushes against).

**The load-bearing call is preserved on the page.** The FV8 subsection states that with both arms scored the corrective sign-law is **bidirectionally `[V]`** (direction-only), removing in full the bidirectional-DATA obstacle FV6 named — **and yet O-22 (per-patient corrected-yes/no) STILL stays `[O]`**, its residual obstacle now **the firewall itself, not data**: a class-level direction-only law cannot certify a per-patient absolute outcome, which needs the firewalled per-patient magnitude (the absolute drive size = the separate item **O-21**, also `[O]`). The chapter's headline answer and title are **unchanged** — they describe the γ-ORDERING null, which remains a null; the FV7/FV8 positives are the orthogonal **sign** axis, a deeper sub-result, exactly as the chapter already framed it.

**One small accuracy fix in the close.** Inserting the FV7/FV8 subsections between FV6 and the *"What (B) moved"* close shifted what *"As the previous section shows…"* pointed at (it would now read as the FV8 positive, not the FV5/FV6 identifiability analysis it refers to). Corrected to *"As the identifiability analysis above shows, the ordering test is moreover non-identified…"* — the **only** content change to the close; its heading and every number, claim, and grade are unchanged.

**The same regeneration flushes the stale O-22 scoreboard note.** The uploaded v0.18.0 `docs/` shipped a §16 scoreboard whose O-22 ledger cell predated the v0.17.0/v0.18.0 FV7/FV8 notes authored in `IRREPRODUCIBILITY_LEDGER.md` (the site was not rebuilt when FV7/FV8 closed on the research axis). This writing rebuild brings the scoreboard O-22 cell in sync with the canonical ledger — exactly as the v0.16.0 writing pass flushed the v0.15.0 ledger note. (Verified: rebuilding from the **unmodified** v0.18.0 `build_site.py` reproduces this same §16 byte-for-byte, so the sync is pre-existing staleness, not introduced by the FV7/FV8 edit.) The scoreboard slug stays `16-scoreboard-firewall-ledger`.

**Files changed (additive / regenerated only).**
- `tools/build_site.py` — extends §15 with the FV7/FV8 subsections + their `num()`/`R()` number-extraction block (bindings `SLM`/`SLP` for the figshare/eLife provenance) and the one back-reference fix in the close. **No** battery/chapter-count change.
- `docs/inheritance/15-held-out-b-validation-null/index.html` — the two published subsections + the corrected close.
- `docs/inheritance/16-scoreboard-firewall-ledger/index.html` — the O-22 ledger note synced from `IRREPRODUCIBILITY_LEDGER.md` (pre-existing staleness flush; see above).
- `reports/site_numbers.json`, `manifest/kit_manifest.csv` — regenerated.
- ledgers / handover / START_HERE / blueprint / VERSION updated additively.

**Gate, verify & determinism.** `python repro/run_all.py` → **all_green = true** (18 batteries, both anchors, `validation_ok`, `signlaw_validation_ok`, `signlaw_plus_arm_validation_ok`, determinism — engines/reports untouched). `python tools/verify_site.py` → **green**: **21 pages**, **19 chapters** (unchanged), sitemap = 21, **585** displayed numbers all verbatim, all answer-first, search-gate PASS; the site rebuilds **twice to an identical sha256**. The displayed-number ledger grows **561 → 585** (the twelve ledgered FV7 + twelve ledgered FV8 numbers; the per-gene ratios `12/16`, `7/7`, `10/16`, `7/9` and the eLife DOI are sourced strings, not ledgered). **Byte-identical:** the vendored substrate, `vp_a4`, all 7 γ atlases, all **7** caches, all **18** engines, both `reports/*.json` numeric inputs, `_meta.json`, the sitemap / llms.txt, the hub + landing, and the **17** content chapters not adjacent to the change; the only deltas are `tools/build_site.py`, the 2 regenerated pages (§15 + the §16 ledger-note flush), `reports/site_numbers.json`, and `manifest/kit_manifest.csv`. **With FV7 and FV8 published, every research result — Tracks I–V and FV1–FV8 — is now on the canonical site; no deferred writing item remains.**

## v0.18.0-signlaw-plus-arm-bidirectional (research: the corrective sign-law's `+` RESTORE arm is SCORED on held-out CRISPRa data — the MIRROR of FV7, completing the bidirectional held-out test; O-22 stays `[O]` by the firewall, not for want of data; no tuning, no regression)
A **research pass** that closes the bidirectional half of the single genuinely-open frontier. FV7 (v0.17.0) scored the corrective sign-law's **`−` arm** on held-out DepMap CRISPR-**KO** data (the kit's first held-out positive) and **narrowed** O-22's obstacle to "the `+` RESTORE arm alone." This release **scores that `+` arm** on a genuinely held-out target of the **opposite operation** (CRISPR-**activation**) and it **passes** — the mirror image of FV7. Site regeneration is **deferred** (research-first rule; the FV6/FV7/IM/FM/PO/VK/LV precedent) — `docs/` stays byte-identical, with the turnkey §15-extension writing spec recorded in `HANDOVER.md`.

**The held-out target (genuinely held out).** Horlbeck et al. 2016, *eLife* **5:e19760**, DOI `10.7554/eLife.19760`, **Supplementary file 10** = the canonical genome-scale **hCRISPRa-v2 K562** gene growth screen (Weissman lab). A CRISPR-**activation** viability screen applies the `+` (gain / restore) operation to every gene from its own promoter; in a **cancer** line the resulting growth change **is** a disease-correction phenotype for a LOF suppressor (restoring a tumour brake slows the cancer program). The kit's `corr_sign` is forced by each gene's **disease MECHANISM** (GOF/LOF), declared by function and **frozen before any CRISPRa data was seen** — so the CRISPRa K562 growth phenotype, a functional viability readout that expresses none of that label, is a legitimate held-out target. All **16/16** oncology genes are present (one row each); the 9 neurodegeneration genes are cached for transparency but **out of readout scope** (a leukemia growth screen does not measure neuronal proteinopathy correction). 36888 table gene rows.

**The sign-locked prediction (locked before scoring).** Under the `+` (activation) operation a **LOF suppressor** (`corr_sign +`) is CORRECTED → activation slows growth (growth phenotype < 0), while a **GOF oncogene** (`corr_sign −`) is **not** corrected by `+` (activating an already-active driver is neutral/pro-growth → growth phenotype ≥ 0). Predicted: **point-biserial(corr_sign==`+`, −growth_phenotype) > 0**.

**The result (reported as it falls — SCORES).** On the **oncology panel** (n = **16**: 9 LOF/`+` + 7 GOF/`−`), **point-biserial = +0.4852**, **exact one-sided permutation p = 0.0274** (11440 label assignments), in the **predicted direction**; per-gene sign-correct **10/16** (LOF **7/9**, GOF 3/7). LOF mean growth phenotype ≈ −0.0198 (growth-suppressive on activation) vs GOF ≈ +0.0021. The `+` arm is **nearly symmetric** to FV7's `−` arm (point-biserial ≈ 0.49 on both).

**Identification (this is NOT the FV5/FV6 confound — re-checked live in FV8).** The γ↔GC collinearity that sinks every *ordering* score does **not** apply: `corr_sign` is set by biology and is **orthogonal to promoter GC** — measured here at **point-biserial(sign,GC) = +0.1222**, with **LOF mean GC = 0.5426 vs GOF mean GC = 0.5320** (balanced, diff < 0.05), and the **GC-partialled** point-biserial = **+0.4731** (essentially unchanged, same sign). So the separation **cannot be manufactured by GC** — it lands on the unique identified + firewall-clean axis FV6 named.

**What it promotes — and what it does NOT (firewall kept exact — the load-bearing call of this release).** Under the same pre-set rule as FV7 (support iff exact p < 0.05 **and** predicted direction), the sign-law's **`+` arm earns a held-out `[V]`** — the kit's **second held-out POSITIVE**. Together with FV7, the corrective sign-law is now **BIDIRECTIONALLY `[V]`** on held-out data (both arms, **direction-only**), which **removes in full** the bidirectional-DATA obstacle FV6 named.
- **O-22** (per-patient corrected-yes/no) **STILL stays `[O]`** — and this is deliberate. FV8 **gently corrects** FV7's "narrows to the `+` arm alone" framing: with both arms scored, O-22's residual obstacle is **no longer DATA** — it is the **firewall itself**. The bidirectional sign-law is a **class-level, direction-only** statement (it certifies *which way* to push each disease class); O-22 is a **per-patient, absolute** outcome that needs the firewalled **per-patient magnitude / penetrance**. A direction-only law cannot certify that a given drive corrects a given patient's switch. Promoting O-22 here would leak a direction-only `[V]` into a per-patient absolute `[V]` — a firewall breach. So O-22's obstacle **moves** from "missing `+`-arm data" to "the firewall (per-patient magnitude)," and it stays `[O]`. This does **not** contradict FV6 (scoring the sign-law needed bidirectional data, **not** Δh — and both arms were scored with **zero** Δh). The absolute drive size is the separate item **O-21**, which stays `[O]` (firewalled).
- **NOT a fresh discovery** of the oncogene/suppressor distinction: those labels are the kit's **frozen priors**; CRISPRa is the **independent** test that the `+` arm tracks them. **K562 is a single CML line** (a single-line growth screen, vs FV7's pan-cancer mean), and **TP53 is null / CDKN2A is deleted** in K562 (activation has a weak/absent endogenous locus to restore) — both push **against** the prediction (a conservative panel, no cherry-picking).
- **Firewall-clean:** reads only the **sign** of the LOF-vs-GOF separation; no magnitude/dose/titre is predicted. γ untouched; `corr_sign`/GC re-read **frozen**; nothing fitted.

**New / changed files (additive only).**
- `data/fetch_signlaw_crispra.py` — **NEW** reception module for the `+`-arm target: `--fetch` downloads the eLife supp10 `.xlsx` (a **pure-stdlib** zipfile + ElementTree reader — no openpyxl/pandas dependency) and rebuilds the cache (only the matched panel rows retained); default `verify()` reproduces the onco `+`-arm headline offline from the cache + the **frozen** atlas (no network/numpy). The cache carries **growth phenotypes only** — `corr_sign`/GC/γ are never smuggled.
- `bvalidation/crispra_horlbeck2016_signlaw_heldout.cache.json` — **NEW** cached scoring sheet (provenance, held-out warrant, sign-locked prediction, readout scope, honest caveats, per-gene growth phenotype + Mann-Whitney p for the matched onco + neurodegen rows).
- `engine/feasibility_validation.py` — **FV7 → FV8**: adds `FV8_signlaw_plus_arm_heldout_score()` (point-biserial + exact permutation p + the live identification gate: group-GC balance and the GC-partialled point-biserial; the explicit `O22_obstacle_corrected` field) and a `B_signlaw_plus_arm_headline`. Constant added: `_CRISPRA_CACHE`. Battery range **FV1–FV7 → FV1–FV8**.
- `repro/run_all.py` — wires `fetch_signlaw_crispra.verify()` as a sibling gate (`signlaw_plus_arm_validation_ok`) into `all_green`, with a `heldout_signlaw_plus_arm_verify` report block.
- `reports/emergence_results.json`, `reports/research_complete.json` — regenerated (now FV1–FV8).
- ledgers/handover/START_HERE/manifest updated additively. **`docs/` stays byte-identical** (site extension deferred).

**Gate & determinism.** `python repro/run_all.py` → **all_green = true** (18 batteries, both NCBI anchors, disease cross-package, `validation_ok`, `signlaw_validation_ok`, **`signlaw_plus_arm_validation_ok`**, determinism re-run identical — `research_complete.json` byte-identical across two runs). γ, the vendored substrate, `vp_a4`, all seven γ atlases, the **seven** prior caches (incl. the FV7 DepMap cache), the 17 other engines, and the entire `docs/` tree are **byte-identical**; the only deltas are the new fetcher + new cache, `feasibility_validation.py` (FV8), `run_all.py`, the two reports, the ledgers/handover/START_HERE, the manifest generator's description registry (`tools/gen_manifest.py`), and the regenerated `manifest/kit_manifest.csv`.

## v0.17.0-signlaw-minus-arm-scored (research: the corrective sign-law's `−` arm is SCORED on held-out DepMap CRISPR data — the kit's first held-out POSITIVE; no tuning, no regression)
A **research pass** that advances the single genuinely-open frontier. FV6 (v0.15.0) proved the **(B)** frontier *partitions*: every γ-ordered prediction is non-identified (γ≈GC, ρ≈0.99), and the **corrective sign-law** (DM2: LOF→`+` restore / GOF→`−` silence) is the **unique crossing that is both identified (orthogonal to GC) and firewall-clean** — blocked only on **bidirectional disease-correction DATA** (a `+` arm and a `−` arm). This release **scores the `−` arm** on a genuinely held-out target and it **passes**. Site regeneration is **deferred** (research-first rule; the FV6/IM/FM/PO/VK/LV precedent) — `docs/` stays byte-identical, with the turnkey §15-extension writing spec recorded in `HANDOVER.md`.

**The held-out target (genuinely held out).** DepMap 24Q2 Public **CRISPRGeneEffect** (Chronos gene-effect), Broad Institute, figshare article `25880521`, file id `46489063` (Model.csv `46489732`). A CRISPR-knockout viability screen applies the `−` (loss) operation to every gene; in a **cancer** line the resulting viability change **is** a disease-correction phenotype (oncogene addiction). The kit's `corr_sign` is forced by each gene's **disease MECHANISM** (GOF/LOF), declared by function and **frozen before any DepMap data was seen** — so DepMap gene-effect, a functional viability readout that expresses none of that label, is a legitimate held-out target. 24/25 disease genes are in the matrix (GBA1→GBA absent; neurodegeneration is out-of-readout-scope anyway), 1150 models screened.

**The sign-locked prediction (locked before scoring).** Under the `−` (knockout) operation a **GOF oncogene** (`corr_sign −`) is CORRECTED → a **dependency** (gene-effect < 0), while a **LOF suppressor** (`corr_sign +`) is **not** corrected by `−` (knockout neutral/pro-tumour → gene-effect ≥ 0). Predicted: **point-biserial(corr_sign==`−`, −gene_effect) > 0**.

**The result (reported as it falls — SCORES).** On the **oncology panel** (n = **16**: 7 GOF/`−` + 9 LOF/`+`), **point-biserial = +0.4940**, **exact one-sided permutation p = 0.0227** (11440 label assignments), in the **predicted direction**; per-gene sign-correct **12/16** (GOF **7/7**, LOF 5/9). GOF median −gene-effect ≈ +0.499 vs LOF ≈ +0.040.

**Identification (this is NOT the FV5/FV6 confound — re-checked live in FV7).** The γ↔GC collinearity that sinks every *ordering* score does **not** apply: `corr_sign` is set by biology and is **orthogonal to promoter GC** — measured here at **point-biserial(sign,GC) = −0.1222**, with **GOF mean GC = 0.532 vs LOF mean GC = 0.543** (balanced), and the **GC-partialled** point-biserial = **+0.4939** (essentially unchanged from +0.4940). So the separation **cannot be manufactured by GC** — it lands on the unique identified + firewall-clean axis FV6 named.

**What it promotes — and what it does NOT (firewall kept exact).** Under a pre-set rule mirroring FV2 (support iff exact p < 0.05 **and** predicted direction), the sign-law's **`−` arm earns a held-out `[V]`** — the kit's **first held-out POSITIVE**. It promotes the `−` arm **only**:
- **O-22** (per-patient corrected-yes/no) **stays `[O]`** — its FV6 obstacle is *bidirectional* data and FV7 supplies only the `−` arm (half the test); the obstacle **narrows to the `+` RESTORE arm alone** (over-expression of a LOF suppressor with a disease/normal contrast). FV7 does **not** reintroduce Δh — FV6 corrected that; the absolute magnitude is the separate item **O-21**, which stays `[O]` (firewalled).
- **NOT a fresh discovery** of the oncogene/suppressor distinction: those labels are the kit's **frozen priors**; DepMap is the **independent** test that the `−` arm tracks them. 4/9 LOF genes (VHL/BRCA1/APC/STK11) are pan-essential for reasons orthogonal to tumour-suppression and **push against** the prediction (a conservative panel); the score is a **pan-cancer mean** across all lines, never lineage-cherry-picked.
- **Firewall-clean:** reads only the **sign** of the GOF-vs-LOF separation; no magnitude/dose/titre is predicted. γ untouched; `corr_sign`/GC re-read **frozen**; nothing fitted.

**New / changed files (additive only).**
- `data/fetch_signlaw_depmap.py` — **NEW** reception module for the `−`-arm target: `--fetch` streams the DepMap matrix and rebuilds the cache (only matched columns retained); default `verify()` reproduces the onco `−`-arm headline offline from the cache + the **frozen** atlas (no network/numpy). The cache carries **gene-effects only** — `corr_sign`/GC/γ are never smuggled.
- `bvalidation/depmap24q2_signlaw_heldout.cache.json` — **NEW** cached scoring sheet (provenance, held-out warrant, sign-locked prediction, readout scope, per-gene mean/median/frac_dependent for the matched onco + neurodegen rows).
- `engine/feasibility_validation.py` — **FV6 → FV7**: adds `FV7_signlaw_minus_arm_heldout_score()` (point-biserial + exact permutation p + the live identification gate: group-GC balance and the GC-partialled point-biserial) and a `B_signlaw_minus_arm_headline`. Helpers added: `_exact_perm_p`, `_partial_pearson`, `_SIGNLAW_CACHE`.
- `repro/run_all.py` — wires `fetch_signlaw_depmap.verify()` as a sibling gate (`signlaw_validation_ok`) into `all_green`, with a `heldout_signlaw_minus_arm_verify` report block.
- `reports/emergence_results.json`, `reports/research_complete.json` — regenerated (now FV1–FV7).
- ledgers/handover/manifest updated additively. **`docs/` stays byte-identical** (site extension deferred).

**Gate & determinism.** `python repro/run_all.py` → **all_green = true** (18 batteries, both NCBI anchors, disease cross-package, `validation_ok`, **`signlaw_validation_ok`**, determinism re-run identical). γ, the vendored substrate, `vp_a4`, all seven γ atlases, the six prior caches, and the entire `docs/` tree are **byte-identical**; the only deltas are the new fetcher + new cache, `feasibility_validation.py` (FV7), `run_all.py`, the two reports, the ledgers/handover/START_HERE, and the regenerated manifest.

## v0.16.0-site-fv6-decomposition-published (writing pass: the FV6 decomposition is published into §15; no new science, no regression)
A **documentation-only writing pass** — the turnkey item that stood in `HANDOVER.md` §3. It publishes the
**FV6 (B)-identifiability decomposition** (shipped as research in v0.15.0) into the canonical site by extending
the existing **§15 (the (B) held-out validation)** chapter with one new subsection; it adds **no new science, no
new battery, and no new chapter**. The vendored substrate, `vp_a4`, **all seven γ atlases + six caches + the
held-out cache**, the **18 batteries**, `reports/emergence_results.json` and `reports/research_complete.json`
(the site's only numeric inputs), and the **14 content chapters not touched** are byte-identical; the only deltas
are `tools/build_site.py` (the §15 subsection generator + FV6 number bindings), the two regenerated pages
(**§15** gains the subsection; the **scoreboard** flushes the v0.15.0 O-22 ledger note that was already authored in
`IRREPRODUCIBILITY_LEDGER.md` but had not yet been regenerated into `docs/`), `reports/site_numbers.json`, and the
regenerated `manifest/kit_manifest.csv`.

**What the new §15 subsection carries** — *"The null is a partition, not one fact — only the sign-law survives."*
Every displayed number flows from `reports/emergence_results.json` → `FV_feasibility_validation` (test FV6) via the
existing `num()`/`R()` zero-drift helpers; nothing is typed literally:
- **ρ(γ,GC) = 0.9944**, **R²(γ~GC) = 0.9948** on the disease panel (n = 25: 13 LOF/`+` + 12 GOF/`−`) — so **every
  γ-ordered prediction is non-identified as a class** (FM1/FV/IM2/DM1), FV5 being one instance.
- The **mechanism corrective-SIGN** is the sole exception: **point-biserial(sign,GC) = +0.0153**,
  **R²(sign~GC) = 0.0002** — a **≈4974×** separation; the frozen cross-check **point-biserial(sign,γ) = −0.0148**
  reproduces DM2 with zero drift.
- The **2×2** (identified? × firewall-clean?) is rendered straight from `candidate_B_observable_map`, isolating the
  **corrective sign-law** as the **unique open frontier** (identified AND firewall-clean), and the chapter records
  the **corrected obstacle**: the sign crossing's only blocker is **bidirectional disease-correction data**, not the
  firewalled Δh. Grade **[V]** on an **[F]** criterion; FV6 promotes nothing (O-19/O-20/O-22 stay `[O]`).

**Gate & determinism.** `python repro/run_all.py` → **all_green** (18 batteries, both anchors, disease
cross-package, `validation_ok`, determinism). `tools/build_site.py` rebuilds **twice to an identical sha256**;
`tools/verify_site.py` is **green** (21 pages, **19 chapters** unchanged, sitemap = page count, every displayed
number verbatim, all pages answer-first). The displayed-number ledger grows **552 → 561** (the nine FV6 numbers);
the scoreboard directory slug stays `16-scoreboard-firewall-ledger` and the magnitude firewall is intact in the new
subsection.

## v0.15.0-bvalidation-identifiability-decomposition-FV6 (additive analysis: the (B) frontier is partitioned; no regression, nothing tuned)
An **additive analysis** release. It adds **one new measured test, FV6**, to the existing `FV` battery
(`engine/feasibility_validation.py`, FV1–FV5 → FV1–FV6) and sharpens the program's single open frontier — the
**(B) held-out validation** — by converting a status note into a measured structural result. The vendored
substrate, `vp_a4`, **all seven γ atlases + six caches + the held-out cache**, `engine/_substrate.py`, the
**17 other engines**, and the generated **`docs/` tree are byte-identical** (diff-verified); only
`feasibility_validation.py` and the two regenerated `reports/*.json` change. The magnitude firewall is intact —
FV6 reads correlations, orthogonality, and signs, never an absolute magnitude. **No γ or cached datum is tuned;
FV6 adds only analysis.**

**FV6 — the (B) identifiability decomposition.** FV5 (v0.12.0) proved that *one* (B) score — the knockdown-depth
ordering — is **non-identified**, because γ = −mean(NN ΔG37) is collinear with promoter GC (ρ ≈ 0.99) and CRISPRi
efficiency is GC/accessibility-driven. FV6 **generalises that single empirical case into a structural partition of
every (B)-testable VP prediction**, measured on the disease atlas (γ re-read frozen; gc read from the same frozen
atlas; n = 25, 13 LOF/`+` + 12 GOF/`−`; nothing fitted):

- **The criterion is forced by the collinearity.** With a near-perfect confound c ≈ γ (here c = GC, measured
  **ρ(γ,GC) = 0.9944, R² = 0.9948**), a prediction scored against a GC-driven observable is **non-identified if
  it is monotone in γ** (then it is collinear with GC and any match is explainable by GC) and **identified only
  if it is orthogonal to γ** (then a match cannot be produced by GC).
- **The γ-ORDERED class is non-identified as a class.** FM1 reachability ordering, the FV knockdown-depth ordering,
  IM2 durability ordering, and DM1 correction-difficulty ordering are **all** monotone in γ — FV5 was one instance
  of a class property, not an isolated failure.
- **The mechanism corrective-SIGN (DM2: LOF→`+`, GOF→`−`) is the sole identifiable exception.** It is set by
  biology, not promoter DNA, and interleaves along γ: **point-biserial(sign,γ) = −0.0148** (this **reproduces DM2's
  −0.015 as a frozen cross-check** — no drift) and, the **new** measurement, **point-biserial(sign,GC) = +0.0153**,
  **R²(sign~GC) = 0.0002** — a **≈4974× variance-explained separation** from the γ-ordered class. The sign is
  **orthogonal to the very confound** that defeats the ordering axis.
- **The 2×2 (identified? × firewall-clean?).** *Knockdown-depth ordering* = firewall-clean **but non-identified**
  (degenerate, FV5); *downstream response-magnitude* = identified **but firewall-blocked** (it IS a magnitude →
  needs Δh); the **corrective SIGN** (bidirectional, mechanism-classified) = **identified AND firewall-clean** (it
  reads *which* sign corrects, never a dose) → the **unique open frontier**.

**Consequence — the open (B) is re-ranked and O-22's obstacle is corrected.** Of the four TODO (B) crossings, the
three ordering-based ones are non-identified (do not run another), and the **sign-law crossing (DM/(B)) is the
unique identifiable AND firewall-clean target.** The prior framing that *all* (B) crossings "need the firewalled
Δh" is **corrected**: the sign crossing does **not** need a magnitude and is **not** GC-confounded — its **only**
obstacle is **bidirectional disease-correction data** (a `+` arm and a `−` arm with a disease/normal contrast).
FV6 **promotes nothing** (O-22 stays `[O]` until the sign-law is actually scored on such data). Grade: **[V]** on
a **[F]** criterion. **Gate:** `run_all.py` → 18 batteries (FV now FV1–FV6) + both anchors + disease cross-package +
`validation_ok` + determinism, all green; reports rebuild **twice to an identical sha256**. Site chapter deferred
(research-first; IM/FM/PO/VK/LV precedent) — turnkey §15-extension spec in HANDOVER §0; `docs/` stays the verified
19-chapter volume.

## v0.14.0-po-vk-lv-chapters-published (writing pass: the three deferred site chapters are published; no new science, no regression)
A **publication-only** release. It carries the three batteries already shipped in v0.13.0 (PO parent-of-origin,
VK RNA-vaccine kinetics, LV lever map) into the canonical reader site as full chapters. No engine, substrate, γ
atlas, battery, report, or ledger changes — `reports/emergence_results.json` and `reports/research_complete.json`
are byte-identical; only `tools/build_site.py`, the generated `docs/` tree, the manifest, and the status docs move.

**The site grows 16 → 19 chapters.** `tools/build_site.py` now inserts **§16 — parent-of-origin: sign and
context (PO)**, **§17 — RNA-vaccine kinetics (VK)**, and **§18 — gene-therapy lever map (LV)** immediately before
the scoreboard, and the scoreboard is renumbered **§16 → §19**. Each new chapter is a standard answer-first volume
chapter (graded claim-strip → LOCK→Derive→Gate → reproduce line → magnitude-firewall box); every displayed number
is pulled live from `reports/emergence_results.json` through the existing `num()`/`R()` zero-drift helpers (battery
blocks `PO_parent_of_origin` / `VK_rna_vaccine_kinetics` / `LV_lever_map`), so the search-gate's verbatim-number
check stays exact. Grades: PO/VK/LV each carry the **[V]** result with the firewalled magnitude items (penetrance ·
prime-boost days, titre · per-modality efficiency, re-dose schedule) held **[O]** (ledger O-23…O-27, unchanged).

**Firewall-link preservation (implementation note).** Every chapter renders a magnitude-firewall box that links to
the scoreboard by its **directory slug**; to keep those links — and therefore the 14 non-adjacent content chapters —
**byte-identical**, the scoreboard's slug is preserved as `16-scoreboard-firewall-ledger` while only its *displayed*
number bumps to 19. Reading order (hub TOC, prev/next, sitemap, `llms.txt`) derives from the ordered chapter **list**,
not directory sort, so it is correct regardless of the slug. The only content-chapter delta is **chapter 15**, whose
forward `next` nav link now points to the inserted §16 PO instead of the scoreboard — an inserted-neighbour update,
not a body change.

**Counts + gate.** Count strings updated (16→19 chapters, 15→18 batteries shown) across hub/landing/scoreboard/
sitemap/`llms.txt`. `tools/verify_site.py` passes green — 21 pages, 19 chapters, sitemap `<loc>` = page count,
`llms.txt` < 5 KB, every chapter answer-first with ≥2 valid JSON-LD blocks, and every `num()`-ledgered value present
verbatim in the HTML corpus — and `tools/build_site.py` rebuilds the tree twice to an **identical** sha256. The
magnitude firewall is intact in every new chapter: each reads a sign, an ordering, a reachability, or a boundary —
never an absolute dose / titre / penetrance / day-count.

## v0.13.0-tracks-II-IV-V-closed (the last simulation items in Tracks II/IV/V; three additive batteries, no regression)
An **additive research** release that closes every remaining *pure-simulation* item on the roadmap. Three new
direction-only batteries are added; the vendored substrate, all measured γ atlases, and the 15 prior batteries
are **byte-identical**. The magnitude firewall is intact throughout — every new claim reads a sign, an
ordering, a reachability, or a boundary, never an absolute dose / titre / penetrance / day-count.

**PO — `parent_of_origin.py` (PO1–PO4), Track II-3.** Sperm and egg deliver the same kind of object — a drive
written at an A4 coordinate — in two different temporal contexts: the egg's large cytoplasm holds the maternal
payload **sustained**, while the sperm's small bolus (the tsRNA/piRNA carrier) is diluted to a **transient**
burst. Held at **equal** supra-spinodal amplitude (the fairness condition that keeps this direction-only), a
held switch is crossed by the **duration** of supra-spinodal exposure: the sustained maternal drive flips it;
the matched transient paternal burst relaxes back (PO1). Under opposing parents the dominant maternal **sign**
is inherited and the transient paternal burst is vetoed; agreement reinforces (PO2). **Honest course-correction:**
PO3 was first hypothesised as "the paternal disadvantage rises with γ," but the substrate returned the opposite
ordering (ρ=−1.0 under equal-*relative* amplitude); per the inheritance discipline the claim was **rewritten**
to the robust, non-tuned **universality** result — the asymmetry holds at **every** measured germline locus
(13/13) — with ρ reported as-it-falls and **no directional claim graded and no γ tuned**.

**VK — `rna_vaccine_kinetics.py` (VK1–VK3), Track IV-1 + IV-3.** The prime–boost interval has an **interior
optimum** in germinal-centre rounds: too short under-matures (the IM1 GC loop, reused **unchanged**), too long
lets protection decay at the **measured** escape rate — a genuine inverted-U in time (VK1). saRNA's longer
same-amplitude drive window crosses the protected (near-spinodal) basin **more reliably** than a shorter mRNA
pulse (0.5317 > 0.5072), with the honest note that post-flip durability is the **identical** barrier — the
advantage is in *reaching*, not *holding* (VK2).

**LV — `lever_map.py` (LV1–LV5), Track V-1…V-4.** The two levers resolve into their real sub-types on the one
substrate. Lever A: knockout (γ→~0), base-edit (small δγ), prime-edit (larger δγ) all **move the threshold**
and are not restorable by a drive; **CRISPRa**, marketed as "activation," leaves γ untouched and is reversible,
so the substrate **re-classifies it as Lever B** (LV1). Lever B: siRNA (− drive), ASO splice-switch (an A4
**coordinate** change at fixed γ), saRNA (+ drive), miRNA-sponge (net + drive) all leave spinodal/barrier
byte-identical and revert on withdrawal (LV2). The lever-choice **decision boundary** is an explicit curve,
h_path*(γ) = h_cap − spinodal(γ): it **falls** with γ and crosses zero at a finite γ* = 3·(h_cap/2)^(2/3),
beyond which even a zero-hold switch needs Lever A — confirmed by actual substrate settles on both sides and in
the Lever-A-mandatory regime (LV3). And a corrected state can be held with **no edit** by re-dosing a Lever-B
drive each cycle: above a critical re-write rate w* the correction is maintained, below it fades (LV4, the GE3
boundary applied therapeutically). The LV1 CRISPRa reversibility is read against the **standing pathological
repression** it treats — not bistable h=0, where any flipped switch trivially sticks by hysteresis.

**No tuning; invariants byte-identical.** The three batteries add only new simulations. The vendored substrate,
`vp_a4`, all seven measured γ atlases, the six promoter/A4 caches, and `bvalidation/…cache.json` are all
**diff-verified byte-identical** to v0.12.0; the only changed pre-existing file is `repro/run_all.py` (the three
batteries wired into the batteries/runners/scoreboards). The gate reports **18/18 batteries green**, both NCBI
anchors reproduce (SOX9 γ=1.4598), the disease cross-package check holds, `validation_ok` holds, and determinism
holds (seed 19, 2×sha256 per battery). New open items **O-23…O-27** are itemised in the ledger (parent-of-origin
penetrance · prime-boost days · saRNA/mRNA titre · per-modality lever efficiency · edit-free re-dose schedule),
all firewalled. **Site:** the PO/VK/LV chapters are **deferred** (the research-first rule, IM/FM precedent); the
published volume stays the verified 16-chapter DOI-bearing site, with a turnkey 3-chapter spec in HANDOVER §0.
With Track V closed, **every pure-simulation item on the roadmap is now done** — the only remaining frontier is
the (B) held-out validation, which is non-identified on the ordering axis and otherwise needs the firewalled Δh.

## v0.12.0-bvalidation-identifiability-FV5 (the (B) stress test: the null is non-identified; additive, no regression)
An **additive research** release that stress-tests the (B) held-out null instead of leaving its confound as a
footnote. The previous releases *recorded* that γ is entangled with promoter GC; this release **measures
whether the (B) ordering score is even identifiable**, and finds it is not. **A new test FV5 is added to the
FV battery** (FV1–FV4 → FV1–FV5); nothing else in the substrate or atlases is touched.

**FV5 — GC-identifiability stress test.** γ = −mean(nearest-neighbour ΔG37), and stacking free energy is
dominated by G/C content, so γ and promoter GC are near-collinear **by construction** — measured here at
Spearman ρ(γ,GC) = **0.9909 / 0.9818 / 0.9643** on the K562-GWPS / RPE1 / K562-essential panels. The held-out
readout (on-target CRISPRi `fold_expr`) is itself driven by sgRNA accessibility, a known function of TSS
chromatin/GC — so the predictor and the readout's nuisance driver are the **same ordering**. Partialling GC
out, the surviving γ effect is non-significant and sign-unstable across panels (ρ(γ,fold_expr|GC) =
**+0.1259 / −0.2228 / −0.4282**, all p ≥ 0.40; no identified positive on any panel). The recorded null is
therefore the **stronger, measured statement**: the knockdown-depth ordering score is **non-identified** — it
cannot separate a barrier effect from a GC/accessibility effect — *not merely "signal absent."* FV5 promotes
nothing; O-19/O-20/O-22 stay **[O]** with this sharpened obstacle. Grade **[V]** (identifiability invariant).

**A roadmap question settled without new data.** γ↔GC collinearity is a property of promoter DNA — *identical
in any cell type*. So scoring the **same observable** (on-target knockdown depth vs γ) on a neuronal
CRISPRi/Perturb-seq panel (the data **exist** and are public — i³Neuron CRISPRi CROP-seq, Tian et al. 2019,
GEO `GSE124703`; CRISPRbrain) would **inherit the identical non-identification**. The open neuronal (B) for
O-20 is therefore **not advanced** by repeating the knockdown-depth ordering in neurons: *the data are not the
obstacle; the test is degenerate.* An **identified** (B) needs a readout **not collinear with promoter GC** —
a downstream **response magnitude** — which requires the firewalled drive size Δh. So the
self-contained-decidable (B) axis is non-identified, and the identifiable (B) axis is firewalled. This
**corrects an earlier overstatement** that the remaining neuronal (B) was merely "data-blocked."

**No tuning; cache byte-identical.** FV5 adds only *analysis* over the existing held-out slice — the vendored
substrate, all seven measured γ atlases, A4, and `bvalidation/replogle2022_heldout.cache.json` are all
**byte-identical** to v0.11.0. The gate reports **15/15 batteries green**, the SOX9 anchor reproduces
(γ=1.4598), determinism holds (seed 19), and `reports/{research_complete,emergence_results}.json` are
regenerated by the gate to carry FV5. **Site: still 16 chapters** — the §15 (B)-validation chapter gains an
*"Is the null even identified?"* section (378 → 405 → **412** displayed numbers); rebuilds twice to an
identical sha256 and passes the structural search-gate. Ledger, blueprint §B.9/§B.10 STATUS, COMPLETION_LEDGER,
and HANDOVER updated to record the non-identification finding.

## v0.11.0-canonical-site-16ch (the §(B) writing pass; documentation-only, no regression)
A **documentation-only** release: the canonical site is regenerated so the **published** volume catches up to
the research layer, which had run one battery ahead of the site (FV, the (B) held-out score, added in v0.10.0
but deliberately not yet written). **No measured γ changed, no inherited file touched, no engine touched** —
every frozen invariant (vendored substrate + all seven measured γ atlases + A4) is byte-identical to v0.10.0,
and `reports/emergence_results.json` (the site's only numeric input) and the `bvalidation/` held-out cache are
byte-identical across the re-run (sha256-verified). The gate still reports **15/15 batteries green**, the SOX9
anchor reproduces (γ=1.4598), determinism holds (seed 19), and the site rebuilds twice to an identical sha256.

**Site: 15 → 16 chapters — the (B) validation is now published.** A new chapter is authored, answer-first with
the graded claim-strip and the magnitude firewall, every displayed value fetched from `reports/` through
`num()`/`R()` (zero-drift):
- **§15 The (B) held-out validation (FV)** — the one honest crossing FM/DM named, from feasibility *map* to
  *evidence*: a no-tuning score of the frozen γ-ordering against held-out measured expression. Run once on the
  ordering axis against **Replogle 2022 *Cell* genome-scale Perturb-seq (CRISPRi)** (DOI
  10.1016/j.cell.2022.05.013): the pre-registered, sign-locked prediction ρ(γ, on-target `fold_expr`) **> 0**
  came out **ρ = −0.0760, p = 0.6283, n = 43** (K562 GWPS) — slightly *opposite*, non-significant across every
  control-expression cutoff (−0.08 → −0.33), sign **disagrees** on RPE1 (ρ=+0.21), SET-proxy AUC = 0.389. By
  the promotion rule (p<0.05 **and** ρ>0) it **promotes nothing**: O-19/O-20/O-22 stay `[O]`, the (A) map stays
  `[V]` and untouched, γ re-read frozen and hash-checked. The chapter records the four sub-tests (FV1 held-out
  integrity · FV2 no-tuning score + rule · FV3 null robustness · FV4 the (A)/(B) firewall) and is graded
  **[V] (a recorded null)** — the verified object is the honestly-run score and the firewall holding, not any
  positive finding. Consistent with FM4.

**Renumbering + counts.** The scoreboard moves **§15 → §16**; the battery/chapter counts are updated wherever
they were typed in prose (hub "15/15 green" + "fifteen discriminant batteries"; landing "16 chapters · 15
batteries green"; scoreboard "Fifteen batteries, all green" + desc "15 discriminant batteries"). The
generator now derives the FV chapter's numbers via `R("FV_feasibility_validation", …)`; the displayed-number
ledger grew **378 → 405** and `tools/verify_site.py` re-runs green (18 pages, sitemap = 18 URLs, llms.txt
2.8 KB, every number present verbatim).

**Files changed (additive / regenerated only):** `tools/build_site.py` (the §15 chapter + the renumber/count
edits), the entire regenerated `docs/` tree, `reports/site_numbers.json` (the audit ledger), and the
bookkeeping (`VERSION`, this `CHANGELOG`, `COMPLETION_LEDGER`, `HANDOVER`, `manifest/kit_manifest.csv`).
Nothing else moved. Bringing the *neuronal* (B) score (O-20), the disease-vs-normal corrective sign-law
(DM2), and the SET-membership precision/recall to a chapter remains future, additive work (HANDOVER §0).

## v0.10.0-bvalidation-FV (the (B) held-out score; additive, no regression)
The **single named next frontier — (B) validation — is now run once**, on the RNA/disease **ordering** axis,
and recorded honestly. This is the first battery whose inputs include a **measured, genuinely held-out
expression target** rather than only the promoter γ + the vendored substrate. **No measured γ changed, no
inherited file touched, no engine primitive touched** — the vendored substrate and all seven measured γ
atlases (+ A4) are **byte-identical** to v0.9.0 (sha256-verified); every addition is additive. The gate now
reports **15/15 batteries green**, the SOX9 anchor reproduces (γ=1.4598), determinism holds (seed 19), and a
new offline integrity gate `validation_ok` passes.

**The result is a clean NULL — reported as it falls.** Pre-registered prediction (sign-locked before
scoring): higher-γ promoters resist the knockdown drive ⇒ Spearman ρ(γ, on-target `fold_expr`) **> 0**.
Scored against **Replogle et al. 2022 *Cell* genome-scale Perturb-seq (CRISPRi)** (DOI
10.1016/j.cell.2022.05.013), primary set K562 genome-wide, n=43 matched: **ρ = −0.0760, p = 0.6283** — slightly
*opposite* to the prediction and far from significance, non-significant across every expression cutoff
(−0.08→−0.33), sign **disagrees** on RPE1 (ρ=+0.21), SET-proxy AUC = 0.389 (near chance). γ was **re-read
frozen** and hash-checked; **nothing was tuned** to the target. Per the promotion rule (p<0.05 **and** ρ>0),
this **promotes nothing**: O-19/O-20/O-22 (per-cell / per-patient yes/no) stay `[O]`; the (A) map stays `[V]`
and untouched. The null is low-power (n=43/11) — it does **not refute** the map, it finds **no support** — and
is **consistent with FM4** (the part the sim can compute does not by itself predict the firewalled per-cell
effect).

**New (additive):**
- `engine/feasibility_validation.py` — **battery FV1–FV4** (the (B) score): FV1 provenance + held-out
  integrity (real Replogle target; γ re-read frozen and hash-equal to the cache; fixed union panel rule),
  FV2 the no-tuning ordering score + the **promotion rule applied honestly** (kept `[O]`), FV3 null
  robustness (no control-expr cutoff yields significant support; cell-line signs disagree), FV4 the (A)/(B)
  firewall (a real (B) score exists, it moved no `[O]` item, γ untouched). Pure-numpy Spearman with an exact
  t-based two-sided p (regularized incomplete beta) — **reproduces SciPy bit-for-bit**, no new dependency.
- `bvalidation/replogle2022_heldout.cache.json` — the **(B) scoring sheet**: the small held-out slice
  (matched-panel `fold_expr`/`control_expr` for the genes intersecting the frozen atlases, across all three
  Replogle datasets) + full provenance (DOI, figshare ids, readout meaning, held-out warrant, sign-lock,
  panel rule). γ is **not** stored here as truth — it is re-read from the frozen atlases at score time.
- `data/fetch_bvalidation.py` — reception of the (B) target (mirrors the γ fetchers): `verify()` is the
  offline integrity + headline-reproduction gate (now wired into `run_all.py`); `--fetch` rebuilds the cache
  from the figshare pseudobulk (how it was built; not needed to reproduce).
- `repro/run_all.py` — FV registered (battery + determinism + scoreboard); new `validation_ok` gate folded
  into `all_green`; `heldout_validation_verify` block added to `reports/research_complete.json`.

**Site note.** The canonical `docs/` site still presents the **14-battery** volume; FV is a **research-layer**
addition that the site does **not** yet carry. The site stays **byte-identical** this release; bringing it to
15 batteries (a §(B)-validation chapter) is the next **writing pass** (HANDOVER §3).

## v0.9.0-canonical-site-15ch (the writing pass; additive, no regression)
A **documentation-only** release: the canonical site is regenerated so the **published** volume catches up to
the research layer, which had run three batteries ahead of the site (IM/FM/DM). **No measured γ changed, no
inherited file touched, no engine touched** — every frozen invariant (vendored substrate + the measured γ
atlases + A4) is byte-identical to v0.8.0, and `reports/emergence_results.json` (the site's only numeric input)
is byte-identical across the re-run. The gate still reports **14/14 batteries green**, the SOX9 anchor
reproduces (γ=1.4598), and determinism holds (seed 19).

**Site: 12 → 15 chapters, and "DOI pending" → minted DOI.** The frozen v0.5.0 snapshot carried 12 chapters and
a placeholder DOI; the generator already had the Zenodo DOI (`10.5281/zenodo.20783547`) wired, so regeneration
embeds it on every page. Three new chapters are authored, each answer-first with the graded claim-strip and the
magnitude firewall, every displayed value fetched from `reports/` through `num()`/`R()` (zero-drift):
- **§9 Immune maturation (IM)** — affinity maturation EMERGES from the germinal-centre loop with an interior
  optimum (peak at survivor-fraction 0.40); innate (RUNX1) vs adaptive (PAX5) split into a measured MFPT ratio
  of 2.369×; tolerance is the equal-and-opposite drive on the same PAX5 switch (memory ↔ tolerance sign law).
- **§13 RNA feasibility map + autism (FM)** — reachability = the measured spinodal, absolute flip-drive ordered
  by measured promoter γ; the structure transfers to 10 measured SFARI ASD-gene promoters (SCN2A shallowest →
  PTEN deepest); the honesty gate (FM4) shows a self-contained flip is a Δh-replay over all 22 switches, not
  evidence — only **(B)** scores it.
- **§14 Disease feasibility map + corrective sign (DM)** — 25 cancer+neurodegeneration promoters (SNCA →
  HTT) are R19 switches; the corrective **sign** is mechanism-forced (GOF→−, LOF→+) and orthogonal to γ
  (point-biserial −0.0148); a reversible Lever-B drive reaches every switch; the 4-locus cross-package γ
  reproduces against reference with no tuning.
Chapters renumbered accordingly (RNA vaccines 9→10, gene therapy 10→11, application map 11→12, scoreboard
12→15); all navigation, hub cards, sitemap, and JSON-LD are list-driven and renumber automatically. **378**
displayed numbers, **2×sha256 identical** on the determinism gate.

**Phase: research → writing.** `PHASE` and the `run_all.py` phase field are set to `writing` (the canonical
deliverable is the site); the change is cosmetic to the gate (the site reads only `all_green`), and the re-run
confirms `all_green` with the emergence report unchanged.

**New tooling (additive, reproducible-discipline).**
- `tools/verify_site.py` — the structural **search-gate** as a script (was a v0.5.0 manual check): every page
  answer-first, ≥2 valid JSON-LD blocks per chapter, `sitemap <loc>` count == page count (17), `llms.txt` < 5 KB,
  claim-strip + firewall present on every chapter, and every one of the 378 displayed numbers appearing verbatim
  in the rendered HTML. Exits non-zero on any failure.
- `tools/gen_manifest.py` — `manifest/kit_manifest.csv` is now a **regenerable artifact** instead of a
  hand-maintained file: it walks every tracked file (excluding `__pycache__`), recomputes bytes + sha256,
  preserves each curated description by path, and is sorted/emitted with the original CSV dialect.

**Next frontier (unchanged, and still the named one): (B) held-out validation.** Everything here is the
**(A)-map** — geometry the substrate forces. The single honest crossing is **(B)**: score the predicted
flipped/corrected-switch SET + ORDERING against HELD-OUT measured pre/post expression of real
siRNA/saRNA/ASO/edit-treated cells, with **no tuning** of Δh or parameters to the target. Until (B) is run, the
per-cell yes/no stays firewalled `[O]`. This release does not attempt (B); it ships the finished canonical site.

## v0.8.0-disease-feasibility-map (additive disease-class extension; no regression)
One coherent addition, fully additive and anchor-gated, **no measured γ changed and no inherited file touched**:
the feasibility map is carried from the RNA-carrier / ASD setting into the **disease class** the sibling
`vp-site` program curates — **cancer** (tumour-suppressor / oncogene promoters) and **neurodegeneration**
(Parkinson's master genes, with the Huntington/ALS proteinopathy bridge). Two new **measured** γ atlases plus
one new measured battery **DM**. The gate now verifies **14/14 batteries green** (was 13/13):
`python repro/run_all.py` re-confirms `all_green`, the SOX9 anchor reproduces (**live this release**, γ=1.4598,
GC=0.545), determinism holds (seed 19), and every one of the 8 frozen invariants (vendored substrate + the five
pre-existing measured atlases + A4) is byte-identical to the v0.7.0 baseline.

**Inheritance, not import (the cross-package validation).** `vp-site` already measures ~90 monogenic-disease
promoters through the *same* TSS−2000..+500 / SantaLucia-NN-ΔG37 / GRCh38 pipeline. Their γ values are **not**
copied. Instead the panels are re-declared **by function** and re-measured here through this kit's own
SOX9-anchor-gated fetcher — so four independently-shared loci (**PTEN, VHL, SOD1, HTT**) become a **no-tuning
cross-package consistency check**. All four reproduce to 4 decimals (PTEN 1.5694, VHL 1.4325, SOD1 1.4443,
HTT 1.6142); the two pipelines agree because both are pinned to the same measured anchor, not to each other.
This agreement is **reported, never used to tune** (A.2).

**New — `data/fetch_disease_gamma.py` (measured, anchor-gated):** the canonical disease-γ fetcher, byte-faithful
to `fetch_rna_gamma.py` (identical `NN_DG37`, `gamma_gc`, `window_for`, SOX9 anchor, online `--fetch` /
offline `verify`). Two panels **declared by function** before any γ was seen:
- **ONCO (16):** tumour suppressors TP53 / RB1 / PTEN / VHL / APC / BRCA1 / NF1 / CDKN2A / STK11 and oncogenes
  KRAS / MYC / EGFR / BRAF / MDM2 / BCL2 / PIK3CA.
- **NEURODEGEN (9):** PD dominant-GOF SNCA / LRRK2 / VPS35, PD recessive-LOF PRKN / PINK1 / PARK7 / GBA1, and
  the proteinopathy bridge HTT / SOD1.
One correctness fix over the inherited fetcher was required: the NCBI record is selected by **official-symbol
match**, not the blind first hit `ids[0]` (which returns SLC6A4 for "HTT" and PROC for "APC"); the correct
loci are pinned (HTT 3064, APC 324, RB1 5925). Writes `inherited/onco_gamma.json`,
`inherited/neurodegen_gamma.json`, and their offline `*_promoters.cache.json`. Atlases ordered by measured γ:
onco APC 1.3748 → PTEN 1.5694; neurodegen SNCA 1.2490 → HTT 1.6142.

**New — the corrective-sign law (the disease-class content beyond FM).** Each gene carries a mechanism-forced
**corrective sign**, orthogonal to γ: a loss-of-function lesion (suppressor knocked out) is corrected by a
**`+` (restore / up-regulate)** drive; a gain-of-function lesion (oncogene / dominant-toxic PD gene) by a
**`−` (knockdown / silence)** drive. The sign is set by the disease mechanism (GOF→`−`, LOF→`+`), **never** by
the promoter's depth — suppressors and oncogenes interleave freely along the γ-ordering (point-biserial of sign
vs γ ≈ −0.015, 14 sign-changes along the order). This is the law FM did not contain.

**New — `engine/disease_feasibility_map.py` (battery DM, DM1–DM4):** the feasibility map specialised to disease,
on the SAME R19 substrate.
- **DM1** disease reachability: every cancer + neurodegeneration promoter is **R19-bistable**; the flip-drive is
  the measured spinodal h*(γ) and the "easiest to correct" ordering is set by measured γ. Geometry + ordering
  **[V]**; absolute Δh **[O]**.
- **DM2** the corrective-sign law: the mechanism-forced sign drives every gene **out** of its pathological basin
  (integration-confirmed), while the **opposite** sign applied from the *same* pathological basin does **not** —
  and the sign is **orthogonal** to γ (interleaving + ~0 point-biserial). Sign law **[V]**; absolute corrective
  dose **[O]** (O-21).
- **DM3** the two-lever decision: a reversible **Lever-B** drive (RNA-style, transient, at the A4 coordinate) is
  reachable for every measured switch and the required drive **grows with γ**; **Lever-A** (permanent edit) is
  reserved for coding-**SET** lesions where the promoter γ itself is unwritable — i.e. the firewall, not a
  recommendation. Decision rule **[V]**; tolerability cap absolute value **[O]** (reuses O-7's logic).
- **DM4** the (A)/(B) honesty gate + **cross-package consistency invariant**: proves the same circularity as
  FM4 (a flip exists at k≥1 for every switch and at no k<1, so a "corrected" screen is Δh-assumption replay, not
  evidence — the per-patient yes/no is doubly undecidable self-contained), **and** asserts the four cross-package
  anchors reproduce. The map is **[V]**; the per-patient yes/no is **[O]/(B)** (O-22), promoted only by a
  held-out, no-tuning score.

**New `[O]` items O-21 / O-22** (absolute corrective dose per disease; per-patient corrected-yes/no = (B)).
Accessors `onco_gamma() / onco_meta() / neurodegen_gamma() / neurodegen_meta() / disease_meta()` added to
`engine/_substrate.py` (additive). The magnitude firewall is intact: DM reads **which** switch, the **sign**,
and the **ordering** only — never an absolute dose — and every clinical application is handed to clinicians and
regulators.

## v0.7.0-feasibility-map (additive research extension + DOI; no regression)
Two additions, both additive, anchor-gated, no measured γ changed: (1) the **concept DOI** is reflected
throughout the kit, and (2) a new **measured battery FM** answers the feasibility question — "does putting
RNA in actually change the cell?" — honestly, including a **measured autism / brain-cell extension**. The
gate now verifies **13/13 batteries green** (was 12/12): `python repro/run_all.py` re-confirms `all_green`,
the SOX9 anchor reproduces (**live this release**, γ=1.4598, GC=0.545), determinism holds (seed 19).

**DOI reflected (concept DOI `10.5281/zenodo.20783547`, Zenodo, resolves to the latest version):** wired into
the site generator `tools/build_site.py` (footer link, claim-strip badge, JSON-LD `doi`, `llms.txt`) so the
next writing pass embeds it; recorded in `START_HERE.md`, `HANDOVER.md`, `COMPLETION_LEDGER.md`. The frozen
`docs/` still display "DOI pending" (v0.5.0 snapshot) and pick up the DOI at the next regeneration — see
HANDOVER §3.

**New — `engine/rna_feasibility_map.py` (battery FM, FM1–FM4):** encodes the (A)-map vs (B)-validation split
(blueprint §B.9) as runnable, graded discriminants on the SAME R19 substrate.
- **FM1** reachability map (RNA-carrier set): the minimal flip-drive is the measured spinodal h*(γ); a flip
  occurs at k=h/h*≥1 and not below (integration-confirmed); the **absolute** flip-drive rises with γ, so the
  ordering of "easiest to flip" is set by measured promoter γ. Geometry + ordering **[V]**; absolute Δh **[O]**.
- **FM2** autism / brain-cell extension on the **measured** ASD atlas (see below): every ASD promoter is
  R19-bistable and the flip-drive ordering tracks measured γ (SCN2A shallowest → PTEN deepest). The structure
  transfers to real autism-gene promoters **[V]**; the per-neuron yes/no is **[O]/(B)** (O-20).
- **FM3** reversibility + sign law: saRNA=+drive/siRNA=−drive; a sub-spinodal transient reverts on clearance,
  a supra-spinodal transient **latches** (hysteresis) and needs an opposite supra-spinodal drive to undo.
  Sign + reversibility structure **[V]**; hold-time **[O]**.
- **FM4** the (A)/(B) honesty gate: proves the circularity as an invariant — a flip exists at k≥1 for every
  measured switch and at no k<1, so the screen is a function of the assumed k alone and is **Δh-assumption
  replay, not evidence**; a self-contained sim **cannot** return the yes/no (it rides on the firewalled Δh
  atop assumed R19 dynamics); the only honest crossing is the **(B)** held-out score, no-tuning. **[V]** as an
  honesty invariant; the yes/no itself **[O]** (O-19).

**New — `inherited/neuro_gamma.json` (measured, anchor-gated):** the autism-spectrum master-gene γ atlas
(MECP2 1.4951, FMR1 1.4563, SHANK3 1.5207, CHD8 1.4080, NRXN1 1.3505, NLGN3 1.4366, PTEN 1.5694, TSC2 1.5435,
SCN2A 1.1982, SYNGAP1 1.4463) — the panel **declared by function** (SFARI monogenic ASD genes) before any γ
was seen, measured via the identical NN-stacking ΔG37 / TSS−2000..+500 / GRCh38 pipeline with the SOX9 anchor
reproducing live. New `[O]` items **O-19/O-20**. Accessors `neuro_gamma()/neuro_roles()` added to
`engine/_substrate.py`.

**Blueprint — new §B.9** (the (A)-map vs (B)-validation split, the no-tuning trap, and the autism extension
with the named (B) next-research protocol) added in English so the feasibility line is inherited.

**Byte-identical preservation (sha256-verified):** the vendored substrate, **all four prior** γ atlases, the
A4 atlases, and the entire canonical site `docs/` are **unchanged**. Only `reports/*.json` change (now carry
FM). Site regeneration is still deferred (it would alter `docs/`); the next writing pass absorbs IM + FM + the
DOI (HANDOVER §3).

## v0.6.0-immune-maturation (additive research extension; no regression)
A new **measured discriminant battery** is added at the research layer, closing the three open immune-track
TODOs (III-1 affinity maturation, III-2 innate/adaptive split, III-3 tolerance). The gate now verifies
**12/12 batteries green** (was 11/11): `python repro/run_all.py` re-confirms `all_green`, SOX9 anchor
reproduces, determinism holds (seed 19). The discipline is unchanged — every γ is the **measured** immune
atlas value (FOXN1/TLX1/RUNX1/PAX5), read on the single vendored R19 substrate; nothing is fitted.

**New — `engine/immune_maturation.py` (battery IM, IM1–IM4):**
- **IM1** — affinity maturation **emerges** from an iterated germinal-centre loop (compete → keep top
  survivor-fraction → reseed + mutate; affinity read as barrier depth γ²/4; on GC collapse the centre is
  re-founded from the naive PAX5 master). Sweeping selection stringency yields an **interior optimum**
  (peak gain at survivor-fraction 0.4 / pressure 0.6); weak selection gives a *negative* gain and
  over-stringent selection collapses the gain toward zero. Shape + emergence **[V]**; absolute
  selection-pressure→affinity mapping is **[O]** (O-16).
- **IM2** — innate (**RUNX1**, shallowest measured barrier) vs adaptive (**PAX5**, deepest) is a
  **two-timescale durability split**: a survival-based first-passage estimate at the rare-escape regime
  (D=0.12) gives MFPT 77.5 (innate) vs 183.7 (adaptive), ratio **2.369** — two well-separated decay
  timescales, slow arm = deep barrier, durability tracking the *measured* γ. Ordering + separation **[V]**;
  absolute innate/adaptive lifetimes are **[O]** (O-17).
- **IM3** — tolerance is the **opposite-sign drive on the same switch** (PAX5): +drive past spinodal →
  memory ON, equal −drive → tolerance OFF; the two flip thresholds are **symmetric** (both ≈ spinodal
  magnitude) and **both** end-states are **held basins** after the drive clears (hysteresis). Sign law +
  held-basin **[V]**; absolute desensitisation dose/schedule is **[O]**, clinical tolerance firewalled to
  clinicians/regulators (O-18).

**Byte-identical preservation (verified by sha256):** the vendored substrate (`inherited/vp_substrate.py`,
`inherited/vp_a4.py`), **all four** measured γ atlases (`germline_gamma.json`, `immune_gamma.json`,
`rna_carrier_gamma.json`, `imprint_gamma.json`), and the entire canonical site (`docs/`) are **unchanged**.
Only `reports/research_complete.json` and `reports/emergence_results.json` change (they now carry IM) — as
expected. New `[O]` items **O-16/O-17/O-18** are itemised in `IRREPRODUCIBILITY_LEDGER.md`, each naming its
obstacle.

**Site is intentionally frozen at the 11-chapter v0.5.0 snapshot.** `tools/build_site.py` derives chapter
and battery counts from the reports, so rebuilding would alter `docs/`. Per the handover's byte-identical
requirement the site is **not** regenerated in this release; the IM chapter is staged as a turnkey spec in
`HANDOVER.md` for the next deliberate writing pass.

## v0.5.0-canonical-site (FINAL RESULT — the canonical write-up; additive, no regression)
The writing phase delivered: `PHASE` flipped `research -> writing` only after `python repro/run_all.py`
re-confirmed **all_green** (SOX9 anchor reproduces, 11/11 batteries PASS, determinism holds). No research
object changed — the vendored R19 substrate (`vp_substrate.py`, `vp_a4.py`), the measured gamma atlases, the
A4 coordinate atlases, and every engine are **byte-identical** to v0.4.0. This release adds only the artifact
and its generator.

**New — the canonical site (`docs/`, per VP-SPEC v1.8):**
- One self-contained English page per chapter, **answer-first**, with JSON-LD (`ScholarlyArticle` +
  `BreadcrumbList`), a graded **claim-strip** (grade + `LOCK -> Derive -> Gate` + reproduce link + volume),
  and the **magnitude firewall** visible on every page.
- Twelve chapters mapped one-per-battery-group plus framing: §1 two-channel architecture [F] · §2 RNA
  writable channel (R, RS) · §3 A4 orthogonality (A4) · §4 two epigenetic channels (TC) · §5
  environment->germline + reprogramming firewall (TG) · §6 imprinted escapee atlas (GE) · §7 gamma<->A4
  coordinate-resolved heritability + parent-of-origin (CH) · §8 immune strengthening (I) · §9 RNA vaccines
  (V) · §10 gene-therapy levers (GT) · §11 (gamma, A4) application map + contact boundary (AM) · §12 the
  honest scoreboard + firewall ledger (all 15 [O] items itemised with their obstacle).
- Retrieval-ready: `robots.txt` (7 crawlers incl. GPTBot/ClaudeBot/PerplexityBot/OAI-SearchBot), `sitemap.xml`
  (14 URLs = page count), `llms.txt` (2220 bytes < 5KB). Canonical base `https://jamming-physics.org/`,
  volume at `/inheritance/`. DOI **pending** (none minted for this kit — not fabricated).

**New — the deterministic generator (`tools/build_site.py`):**
- Every displayed number is fetched from `reports/` through a recording ledger, so the HTML **cannot diverge**
  from the gate output. **253** displayed numbers, all traced; built **twice** and sha256'd over the whole
  `docs/` tree -> identical (`deterministic_2xsha256 = true`). Audit trail written to `reports/site_numbers.json`.

**Verification of this release:** 119/119 search-gate checks pass (answer-first on every page; >=2 valid JSON-LD
blocks each; claim-strip + grade badge + reproduce path + firewall on every chapter; 7 crawlers; sitemap == page
count; llms.txt < 5KB). Zero-drift: all 253 gate numbers appear verbatim in the rendered site.

## v0.4.0-research-complete (gamma<->A4 coupling; RESEARCH COMPLETE — additive, no regression)
Executed the final research frontier (the four remaining items) and closed the research phase. gamma
atlases unchanged byte-for-byte; the nine prior batteries still green. Gate now runs **eleven** batteries +
A4 verification across **four** coordinate sets (42 wide windows). A new `HANDOVER.md` hands the **final
result** (the canonical write-up) to the next session.

**New measured data (NCBI-direct, wide +/-15kb windows -> A4 coordinates):**
- `inherited/a4_imprint_coordinates.json` (+ cache) — A4 coordinates for the 12 imprinted loci.
- `inherited/a4_germline_coordinates.json` (+ cache) — A4 coordinates for the 13 gamete-machinery genes.
- `inherited/a4_immune_coordinates.json` (+ cache) — A4 coordinates for the 4 immune masters.

**New research engines (batteries green, deterministic seed=19):**
- `engine/coordinate_heritability.py` — CH1-CH4 [items: germline/immune/escapee coupling, parent-of-origin]:
  heritability couples gamma AND A4 (at matched gamma the contact-competent coordinate inherits better,
  MEST vs MOS); parent-of-origin contact configuration mapped (paternal contact fraction 0.5 vs maternal 0.0
  in-panel); joint (gamma, A4) ordering puts deep-gamma + contact-competent loci on top (NNAT).
- `engine/a4_application_map.py` — AM1-AM4 [items: prime-boost/lever map, 3D contact boundary]: prime-boost
  dose is coordinate-dependent; the two levers partition the (gamma, contact) plane; the **3D contact
  boundary curve** delta*(gamma) RISES with gamma (a deeper switch needs more A4 contact-assist to stay
  drive-reachable).

**Gate, handover & docs:** `repro/run_all.py` -> 11 batteries + 4-set A4 verify; `HANDOVER.md` added
(research-complete status + full findings synthesis + the final-result instructions for the next session);
COMPLETION_LEDGER marks research complete; blueprint Part B frontier items moved to DONE;
IRREPRODUCIBILITY_LEDGER extended (O-14, O-15).

## v0.3.0-research (A4 coordinate channel made central — additive, no regression)
Acted on the architectural correction: **measuring gamma alone is not enough for RNA research.** gamma is
the SET (fixed in the genome — the environment cannot rewrite it); whatever the environment writes, and
whatever a small RNA carries, lives in the **A4 COORDINATE channel** (compartment shells, anchors, loops,
and the 3D helical CONTACT phase). RNA acts by sequence complementarity = it specifies an A4 coordinate. So
the kit now reads BOTH channels (gamma + A4). gamma atlases unchanged byte-for-byte; the eight prior
batteries still green. Gate now runs **nine** batteries + an A4 offline reproduction check.

**New vendored engine (single source, read-only):**
- `inherited/vp_a4.py` — the A4 coordinate/structure channel: the KEY pipeline (stiffness signal ->
  compartment shells -> anchors -> motor/anchor loops) + the interpreter coordinate reads (shell class,
  nearest anchor, and the 3D helical face / contact-competence), plus the orthogonal material reads
  (CpG observed/expected). Direct transcription of the DNA whitepaper KEY (Section 3).

**New measured data (NCBI-direct):**
- `inherited/a4_coordinates.json` — A4 coordinate reads for the 12 RNA carriers, measured from WIDE
  (+/-15 kb) NCBI windows centered on each TSS (real shells/anchors form at this scale), with cpg_oe.
- `inherited/a4_windows.cache.json` — the cached wide windows for offline bit-for-bit A4 reproduction.

**New research engine (battery green, deterministic seed=19):**
- `engine/a4_layer.py` — A4-1..A4-5: (A4-1) **A4 is orthogonal to gamma** — gamma tracks GC (R2~69%) but
  the CpG-island signal (R2~18%) and especially the 3D helical CONTACT phase (R2~2%, ~98% independent)
  carry information gamma does NOT, and same-gamma / different-contact pairs exist (gamma alone is
  degenerate); (A4-2) **RNA is coordinate-targeting** — a contact-competent coordinate's loop-assist lets a
  fixed payload cross the spinodal where a non-contact coordinate of the SAME gamma does not; (A4-3) **the
  environment writes A4, not gamma** — gamma is sequence-fixed while the contact/compartment state is the
  writable R19 variable; (A4-4) **inheritance is of an A4 configuration** — a held contact state at a
  coordinate survives reprogramming (direction-only).

**Gate & docs:** `repro/run_all.py` -> 9 batteries + A4 verify; the discipline note now records the
two-channel read (gamma = unwritable SET; A4 = the writable coordinate the environment/RNA use);
COMPLETION_LEDGER / blueprint / IRREPRODUCIBILITY_LEDGER updated.

## v0.2.0-research (first research pass — additive, no regression)
Executed the first-pass research from the blueprint's highest-priority items (Track I RNA-channel
hardening + Track II germline-firewall deepening). Inherited γ atlases unchanged byte-for-byte; the v0.1.0
five batteries still green. Gate now runs **eight** batteries, all_green.

**New measured data (NCBI-direct):**
- `inherited/imprint_gamma.json` (+ cache) — imprinted / parent-of-origin locus γ (12 loci: IGF2, H19,
  KCNQ1OT1, SNRPN, MEST, PEG3, PLAGL1, GNAS, DLK1, MEG3, NNAT, GRB10) — the canonical reprogramming
  ESCAPEES — measured via the identical SantaLucia pipeline, SOX9-anchor-gated, cached offline.
  `data/fetch_imprint_gamma.py` carries the online fetch + offline verify.

**New research engines (all batteries green, deterministic seed=19):**
- `engine/rna_species.py` — RS1–RS5 [blueprint I-1, I-3]: resolves "small RNA" into miRNA / piRNA / tsRNA /
  m6A-mRNA by their measured machinery; each a signed drive; production-stability ordering by machinery
  barrier (piRNA deepest); METTL3/YTHDF2 writer/eraser mark-side reversibility; germline competence
  (piRNA/tsRNA/VASA load the gamete).
- `engine/two_channel.py` — TC1–TC4 [blueprint I-2]: methylation × RNA both write the same h on one switch —
  same-sign ADD, opposite-sign VETO, hysteresis PATH-DEPENDENCE (order of writes latches the state).
- `engine/germline_escapee.py` — GE1–GE4 [blueprint II-1, II-2, II-4]: imprinted survival ranks
  ascending-γ (KCNQ1OT1 best-inherited, SNRPN worst, Spearman ρ=1.0); the two erasures resolved (PGC vs
  zygotic, harsher window dominates); re-writing vs persistence with a measured critical re-write rate w*.

**Gate & docs:** `repro/run_all.py` extended to 8 batteries + the imprint offline verify; COMPLETION_LEDGER
and blueprint items moved to DONE; IRREPRODUCIBILITY_LEDGER extended (O-9..O-11).

## v0.1.0-research (this release)
First self-contained release. Establishes the substrate logic of environmental inheritance, the RNA
writable channel, immune strengthening, and the extension to RNA vaccines and gene therapy.

**Inherited (vendored from the vp-site, read-only):**
- `inherited/vp_substrate.py` — the R19 jamming switch (single source of the switch math).
- `inherited/germline_gamma.json` (+ cache) — measured gamete-machinery γ (13 genes; DAZL/REC8/…).
- `inherited/immune_gamma.json` (+ cache) — measured immune master γ (FOXN1/TLX1/RUNX1/PAX5).
- `VP_SPEC_v1_8.md` — vendored discipline.

**Measured here from NCBI (new):**
- `inherited/rna_carrier_gamma.json` (+ cache) — the small-RNA / transgenerational-RNA machinery γ
  (12 genes: DROSHA, DGCR8, DICER1, AGO2, TARBP2, PIWIL1, MOV10L1, DDX4, METTL3, YTHDF2, ELAVL1, ANG),
  measured via the identical SantaLucia pipeline, SOX9-anchor-gated, cached for offline reproduction.
  `data/fetch_rna_gamma.py` carries both the online fetch and the offline verify.

**New research engines (all batteries green, deterministic seed=19):**
- `engine/rna_layer.py` — R1–R5, the RNA writable channel (reversible h-write; two signs; measured atlas;
  reversibility).
- `engine/env_to_germline.py` — TG1–TG6, environment→germline transmission (SET invariance; reprogramming
  firewall p²; heritability ranks ascending-γ, Spearman ρ≈0.99; sign preserved; RNA decays by ~F3 while a
  deep-barrier mark persists).
- `engine/transgenerational_immunity.py` — I1–I4, immune strengthening (memory MFPT ranks ascending-γ;
  trained pre-tilt lowers the recall drive; inherited priming, direction-only and fading).
- `engine/rna_vaccine.py` — V1–V5, vaccine as a dosed RNA drive (supra-spinodal flip + hysteretic hold;
  interior schedule optimum tracking the measured protection half-life; transient payload / persistent protection).
- `engine/gene_therapy.py` — GT1–GT4, two levers (SET-edit moves spinodal/barrier, irreversible by a drive;
  reversible drive-reset via RNA; geometry decision rule).

**Gate & docs:**
- `repro/run_all.py` — NCBI offline verify + five batteries + 2×sha256 determinism → `reports/research_complete.json`
  (`all_green = true`).
- `START_HERE.md`, `00_CONTINUATION_BLUEPRINT.md` (large roadmap toward vaccines + gene therapy, with the
  binding "learn the inheritance discipline first" section), `CHARTER.md`, `COMPLETION_LEDGER.md`,
  `IRREPRODUCIBILITY_LEDGER.md`, `manifest/kit_manifest.csv`.

**Discipline:** additive-only, no regression; vendored substrate single-source; γ measured/anchor-gated,
never fitted; grade chain [F]/[V]/[O]/[L]; DNA-emergence + magnitude firewall; one zip; English docs.
