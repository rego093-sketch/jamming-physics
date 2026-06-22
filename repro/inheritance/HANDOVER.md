# HANDOVER — VP Inheritance Kit · research complete → FINAL RESULT (canonical site) DELIVERED

> **Read order for a new window:** this file → `START_HERE.md` → `00_CONTINUATION_BLUEPRINT.md` (Part A is
> binding) → `CHARTER.md`. This file is the single status + synthesis + next-step page.

## 0. Status: GREEN (v0.19.0-heldout-positives-published) — **Tracks I–V all closed on the simulation axis**; research complete; the one open (B) frontier now **bidirectionally scored** — the corrective sign-law's **`−` arm** (FV7, held-out DepMap CRISPR-KO) **and `+` RESTORE arm** (battery **FV8**, held-out Horlbeck 2016 CRISPRa) are both confirmed, so the sign-law is **BIDIRECTIONALLY `[V]`** (the kit's first and second held-out POSITIVES); **O-22 stays `[O]` by the firewall, not for want of data**; canonical **19-chapter** site current with **FV7/FV8 now PUBLISHED into §15** (every research result — Tracks I–V and FV1–FV8 — is on the canonical site; no deferred writing item remains)
`python repro/run_all.py` → **all_green = true**, deterministic, fully offline.

> **NEW this release (v0.19.0) — writing pass: the FV7 `−`-arm and FV8 `+`-arm held-out POSITIVES are PUBLISHED into §15; the corrective sign-law's bidirectional held-out validation is now on the canonical site; no new science, no new chapter, no new battery, no regression.** This is the pair of turnkey items that previously stood in §3 (the deferred FV7 v0.17.0 and FV8 v0.18.0 §15-extensions). `tools/build_site.py` now extends the existing **§15 (the (B) held-out validation)** with **two** subsections — *"The sign-law's `−` arm, scored on held-out data — the first held-out positive"* (FV7) and *"The sign-law's `+` RESTORE arm, scored on held-out data — the bidirectional close"* (FV8) — placed after the FV6 *"The null is a partition…"* subsection and before the *"What (B) moved"* close. Every displayed number flows from `reports/emergence_results.json` → `FV_feasibility_validation` (tests FV7/FV8) via the `num()`/`R()` zero-drift helpers (FV7: point-biserial **+0.4940**, exact p **0.0227**, per-gene **12/16** / GOF **7/7**, sign↔GC **−0.1222**, GC-partialled **+0.4939**, figshare `25880521`; FV8: point-biserial **+0.4852**, exact p **0.0274**, per-gene **10/16** / LOF **7/9**, sign↔GC **+0.1222**, GC-partialled **+0.4731**, *eLife* `19760`, DOI `10.7554/eLife.19760`), and each subsection keeps the **magnitude firewall** visible (reads only the *sign* of the separation; γ untouched) and the honest caveats intact. **The load-bearing call is on the page:** with both arms scored the sign-law is **bidirectionally `[V]`** (direction-only), removing in full the bidirectional-DATA obstacle — **and yet O-22 STILL stays `[O]`**, its residual obstacle now **the firewall itself, not data** (a class-level direction-only law cannot certify the per-patient absolute outcome, which needs the firewalled per-patient magnitude — absolute drive size = **O-21**, also `[O]`). The chapter's **headline answer and title are unchanged** (they describe the γ-ORDERING null, which remains a null; the FV7/FV8 positives are the orthogonal **sign** axis). **One small accuracy fix in the close:** inserting the subsections between FV6 and the close shifted what *"As the previous section shows…"* pointed at, so it is corrected to *"As the identifiability analysis above shows…"* (the only content change to the close; its heading, numbers, claims, and grades are unchanged). **The same rebuild flushes the stale O-22 scoreboard note** — the uploaded v0.18.0 `docs/` shipped a §16 whose O-22 cell predated the v0.17.0/v0.18.0 FV7/FV8 notes authored in `IRREPRODUCIBILITY_LEDGER.md` (the site was not rebuilt when FV7/FV8 closed on the research axis); this writing rebuild syncs it, exactly as v0.16.0 flushed the v0.15.0 ledger note (verified: rebuilding from the **unmodified** v0.18.0 `build_site.py` reproduces this same §16 byte-for-byte, so the sync is pre-existing staleness, not introduced by the edit). `tools/verify_site.py` is **green** (21 pages, **19 chapters** unchanged, sitemap = 21, **585** displayed numbers all verbatim, all answer-first, search-gate PASS); the site rebuilds **twice to an identical sha256**; the ledger grows **561 → 585** (twelve FV7 + twelve FV8 ledgered numbers; the per-gene ratios and the eLife DOI are sourced strings). **Byte-identical:** the vendored substrate, `vp_a4`, all 7 γ atlases, all **7** caches, all **18** engines, both `reports/*.json` numeric inputs, `_meta.json`, sitemap/llms.txt, hub + landing, and the **17** content chapters not adjacent to the change; only `tools/build_site.py`, the 2 regenerated pages (§15 + the §16 flush), `reports/site_numbers.json`, and `manifest/kit_manifest.csv` differ. **With FV7 and FV8 published, every research result — Tracks I–V and FV1–FV8 — is now on the canonical site; no deferred writing item remains.**

> **NEW this release (v0.18.0) — FV8: the corrective sign-law's `+` RESTORE arm is SCORED on held-out CRISPRa data — the MIRROR of FV7, completing the bidirectional held-out test; O-22 stays `[O]` by the firewall, not for want of data (no tuning, no regression).** FV7 scored the `−` arm and *narrowed* O-22's obstacle to "the `+` RESTORE arm alone." This release **scores that `+` arm** on a genuinely held-out target of the **opposite operation** and it **passes**. **Target (genuinely held out):** Horlbeck et al. 2016, *eLife* **5:e19760**, DOI `10.7554/eLife.19760`, **Supplementary file 10** = the canonical genome-scale **hCRISPRa-v2 K562** gene growth screen — a CRISPR-**activation** screen *is* the `+` (gain/restore) operation, and in a **cancer** line growth *is* a correction phenotype for a LOF suppressor (restoring a tumour brake slows the cancer program). The kit's `corr_sign` is forced by disease **MECHANISM** and **frozen before any CRISPRa data was seen**, so the K562 growth phenotype is a legitimate held-out readout (all **16/16** onco genes matched; the 9 neurodegen genes are out-of-readout-scope). **Sign-locked prediction:** under `+`, LOF suppressors (`corr_sign +`) are corrected → activation slows growth (growth phenotype < 0), GOF oncogenes (`corr_sign −`) are **not** → point-biserial(`+`, −growth_phenotype) > 0. **Result (as it falls — SCORES):** on the onco panel (n = **16**: 9 LOF + 7 GOF), **point-biserial = +0.4852**, **exact one-sided permutation p = 0.0274** (11440 perms), predicted direction; per-gene **10/16** correct (LOF **7/9**), nearly symmetric to FV7's `−` arm. **Identified (re-checked live in FV8, NOT the FV5/FV6 confound):** point-biserial(sign,GC) = **+0.1222**, LOF mean GC **0.5426** vs GOF mean GC **0.5320** (balanced, diff<0.05), GC-partialled point-biserial = **+0.4731** (unchanged, same sign) — the match cannot be a GC artifact. **Firewall-clean** (reads only the *sign* of the separation). Under the same pre-set rule the `+` arm earns a held-out **[V]** — the kit's **second held-out POSITIVE**. **Together with FV7 the corrective sign-law is now BIDIRECTIONALLY [V]** (both arms, direction-only), which **removes in full** the bidirectional-DATA obstacle FV6 named. **THE LOAD-BEARING CALL: O-22 STILL stays `[O]`.** FV8 **gently corrects** FV7's "narrows to the `+` arm alone" framing — with both arms scored, O-22's residual obstacle is **no longer DATA but the firewall itself**. The sign-law is **class-level + direction-only** (*which way* to push each disease class); O-22 is a **per-patient absolute** outcome (does a drive correct *this* patient's switch?), which needs the firewalled **per-patient magnitude/penetrance** — the absolute drive size being the separate item **O-21** (also `[O]`). A direction-only law cannot deliver a per-patient yes/no, and promoting O-22 would **leak** a direction-only `[V]` into a per-patient absolute `[V]` (a firewall breach). So O-22's obstacle **moves** from "missing `+`-arm data" to "the firewall," and it stays `[O]`. This does **not** contradict FV6 (scoring the sign-law needed bidirectional data, **not** Δh — both arms scored with **zero** Δh). **Not a fresh discovery** of the oncogene/suppressor split (frozen priors; CRISPRa is the **independent** test that the `+` arm tracks them); **K562 is a single CML line** (single-line growth screen, vs FV7's pan-cancer mean), and **TP53-null / CDKN2A-deleted** in K562 push **against** the prediction (conservative, no cherry-picking). **New files (additive):** `data/fetch_signlaw_crispra.py` (reception: `--fetch` downloads the eLife supp10 `.xlsx` via a **pure-stdlib** zipfile+ElementTree reader — no openpyxl/pandas — and rebuilds the cache, `verify()` reproduces the headline offline from the cache + **frozen** atlas — cache carries growth phenotypes only, no smuggled sign/GC/γ), `bvalidation/crispra_horlbeck2016_signlaw_heldout.cache.json`; `feasibility_validation.py` gains **FV8** (FV1–FV7 → FV1–FV8) + constant `_CRISPRA_CACHE`; `run_all.py` wires `signlaw_plus_arm_validation_ok` into `all_green`; the 2 reports regenerate (FV1–FV8). **Byte-identical:** γ, the vendored substrate, `vp_a4`, all 7 γ atlases, the **7 prior caches** (incl. the FV7 DepMap cache), the 17 other engines, and the **entire `docs/` tree**. `tools/verify_site.py` would still describe the **19-chapter** site as-is. **The FV8 §15-extension into the site is DEFERRED** (research-first rule; FV6/FV7/IM/FM/PO/VK/LV precedent) — turnkey spec in §3.

> **NEW this release (v0.17.0) — FV7: the corrective sign-law's `−` arm is SCORED on held-out DepMap CRISPR data (the kit's first held-out POSITIVE; no tuning, no regression).** FV6 proved the **(B)** frontier *partitions* and named the corrective sign-law (DM2: LOF→`+`, GOF→`−`) as the **unique identified + firewall-clean crossing**, blocked only on **bidirectional disease-correction DATA** (a `+` arm and a `−` arm). This release **scores the `−` arm** and it **passes**. **Target (genuinely held out):** DepMap 24Q2 Public **CRISPRGeneEffect** (Chronos), figshare article `25880521`, file id `46489063` — a CRISPR-**knockout** screen *is* the `−` (loss) operation, and in a **cancer** line viability *is* a correction phenotype (oncogene addiction). The kit's `corr_sign` is forced by disease **MECHANISM** and **frozen before any DepMap data was seen**, so gene-effect is a legitimate held-out readout (24/25 genes matched; GBA1→GBA absent; neurodegeneration out-of-readout-scope). **Sign-locked prediction:** under `−`, GOF oncogenes (`corr_sign −`) are corrected → **dependencies** (gene-effect < 0), LOF suppressors (`corr_sign +`) are **not** → point-biserial(`−`, −gene_effect) > 0. **Result (as it falls — SCORES):** on the onco panel (n = **16**: 7 GOF + 9 LOF), **point-biserial = +0.4940**, **exact one-sided permutation p = 0.0227** (11440 perms), predicted direction; per-gene **12/16** correct (GOF **7/7**). **Identified (re-checked live in FV7, NOT the FV5/FV6 confound):** point-biserial(sign,GC) = **−0.1222**, GOF mean GC **0.532** vs LOF mean GC **0.543** (balanced), GC-partialled point-biserial = **+0.4939** (unchanged) — the match cannot be a GC artifact. **Firewall-clean** (reads only the *sign* of the separation). Under the pre-set rule (support iff exact p<0.05 **and** predicted direction) the `−` arm earns a held-out **[V]**. It promotes the `−` arm **only**: **O-22** (per-patient yes/no) stays **[O]** with its obstacle **narrowed to the `+` RESTORE arm alone** — FV7 does **not** reintroduce Δh (FV6 corrected that); the absolute dose is the separate item **O-21**, which stays [O]. This is **not** a fresh discovery of the oncogene/suppressor split (those are the kit's **frozen priors**; DepMap is the **independent** test that the `−` arm tracks them); 4/9 LOF genes are pan-essential and push **against** the prediction (conservative; pan-cancer mean). **New files (additive):** `data/fetch_signlaw_depmap.py` (reception: `--fetch` rebuilds the cache, `verify()` reproduces the headline offline from the cache + **frozen** atlas — cache carries gene-effects only, no smuggled sign/GC/γ), `bvalidation/depmap24q2_signlaw_heldout.cache.json`; `feasibility_validation.py` gains **FV7** (FV1–FV6 → FV1–FV7) + helpers `_exact_perm_p`/`_partial_pearson`; `run_all.py` wires `signlaw_validation_ok` into `all_green`; the 2 reports regenerate (FV1–FV7). **Byte-identical:** γ, the vendored substrate, `vp_a4`, all 7 γ atlases, the 6 prior caches, the 17 other engines, and the **entire `docs/` tree**. `tools/verify_site.py` would still describe the **19-chapter** site as-is. **The FV7 §15-extension into the site is DEFERRED** (research-first rule; FV6/IM/FM/PO/VK/LV precedent) — turnkey spec in §3.

> **NEW this release (v0.16.0) — writing pass: the FV6 (B)-identifiability decomposition is PUBLISHED into §15; no new science, no new chapter, no regression.** This is the turnkey item that previously stood in §3. `tools/build_site.py` now extends the existing **§15 (the (B) held-out validation)** with one subsection — *"The null is a partition, not one fact — only the sign-law survives"* — placed after the FV5 *"is the null even identified?"* section and before the *"What (B) moved"* close. Every displayed number flows from `reports/emergence_results.json` → `FV_feasibility_validation` (test FV6) via the `num()`/`R()` zero-drift helpers (ρ(γ,GC)=**0.9944**, R²(γ~GC)=**0.9948**, point-biserial(sign,GC)=**+0.0153**, R²(sign~GC)=**0.0002**, separation **≈4974×**, frozen cross-check point-biserial(sign,γ)=**−0.0148** reproducing DM2), and the **2×2** is rendered straight from `candidate_B_observable_map`. The chapter records the **corrected O-22 obstacle** (the sign crossing's only blocker is **bidirectional disease-correction DATA**, not the firewalled Δh) and keeps the magnitude firewall visible. `tools/verify_site.py` is **green** (21 pages, **19 chapters** unchanged, sitemap = page count, **561** displayed numbers all verbatim, all answer-first); the site rebuilds **twice to an identical sha256**. The **same regeneration flushes the v0.15.0 O-22 ledger note** (authored in `IRREPRODUCIBILITY_LEDGER.md`, not yet regenerated into `docs/`) onto the scoreboard page. **Byte-identical:** the vendored substrate, `vp_a4`, all 7 γ atlases + 6 caches + the held-out cache, all **18** engines, both `reports/*.json` numeric inputs, and the **14** content chapters not adjacent to the change; only `tools/build_site.py`, the 2 regenerated pages (§15 + scoreboard), `reports/site_numbers.json`, and `manifest/kit_manifest.csv` differ. The displayed-number ledger grows **552 → 561** (nine FV6 numbers); the scoreboard slug stays `16-scoreboard-firewall-ledger`. **With this published, every deferred writing item (IM/FM/DM/PO/VK/LV/FV/FV6) is now on the canonical site.**

> **Status of the prior release (v0.15.0-bvalidation-identifiability-decomposition-FV6) — Tracks I–V all closed on the simulation axis; research complete; the (B) frontier decomposed (FV6).**

> **NEW this release (v0.15.0) — FV6: the (B) frontier PARTITIONS (additive analysis, no new data, no regression, nothing tuned).** One measured test added *inside* the FV battery (FV1–FV5 → **FV1–FV6**); battery count and site chapter count are unchanged (FV stays one battery / §15). FV5 had shown the held-out *ordering* score is non-identified because γ = −mean(NN ΔG37) is collinear with promoter GC. FV6 proves this is a **class** property and isolates the one exception. Measured on the disease panel (n=25): **ρ(γ,GC) = 0.9944**, **R²(γ~GC) = 0.9948** — so **every γ-ORDERED VP prediction** (reachability / knockdown-depth / durability / correction-difficulty ordering) is non-identified *as a class*; re-running any of them as an ordering score adds nothing. The **mechanism corrective-SIGN** (DM2: LOF→`+`, GOF→`−`) is the **sole exception**: **point-biserial(sign,GC) = +0.0153** (R²=0.0002 — a **≈4974×** separation from the γ↔GC axis), so it is **orthogonal to the confound**, and because a sign test reads only WHICH sign corrects (never a dose) it is also **firewall-clean**. A 2×2 (identified? × firewall-clean?) then locates every candidate (B): γ-ordering = clean-but-non-identified (degenerate); response-magnitude = identified-but-firewall-blocked (needs Δh); **corrective SIGN = identified AND firewall-clean → the unique open (B)**. **This corrects the prior framing** that "all (B) crossings need the firewalled Δh": the sign-law does not — its only obstacle is **bidirectional disease-correction DATA** (an oncogene `−` arm and a suppressor/PD `+` arm scored together). FV6 reproduces DM2's point-biserial(sign,γ)=−0.0148 frozen and **promotes nothing** (O-19/O-20/O-22 stay `[O]`). Gate green + byte-reproducible; vendored substrate, all 7 γ atlases, the 17 other engines, and the entire `docs/` tree are byte-identical (only `feasibility_validation.py` + the 2 reports change). **A turnkey spec for extending site chapter §15 with the FV6 decomposition is in §3 (writing deferred per the research-first rule — `docs/` stays byte-identical this release).**

> **NEW this release (v0.14.0) — writing pass: the three deferred site chapters are PUBLISHED; no new science, no regression.** `tools/build_site.py` now emits a **19-chapter** volume — **§16 parent-of-origin (PO)**, **§17 RNA-vaccine kinetics (VK)**, **§18 gene-therapy lever map (LV)** inserted *before* the scoreboard (now **§19**). Every displayed number flows from `reports/emergence_results.json` via the existing `num()`/`R()` zero-drift helpers; `tools/verify_site.py` is **green** (21 pages, 19 chapters, sitemap = page count, all answer-first, every ledgered number verbatim) and the site rebuilds twice to an **identical** sha256. The vendored substrate, all measured γ atlases, the 18 batteries, and the **14** content chapters not adjacent to the insertion are **byte-identical**; chapter 15's only delta is its forward `next` nav link, which now points to §16 PO (an inserted neighbour, not a content change). The magnitude firewall is intact in every new chapter. **The scoreboard's directory slug is preserved (`16-scoreboard-firewall-ledger`) so every chapter's firewall-box link stays byte-identical — only its displayed number bumps 16 → 19.**

> **NEW prior release (v0.13.0) — the last pure-simulation items in Tracks II/IV/V are shipped as three additive batteries; 18/18 green; substrate + all γ atlases + 15 prior batteries byte-identical.**
> - **PO (`parent_of_origin.py`, PO1–PO4) — Track II-3.** Maternal=sustained vs paternal=transient context at EQUAL amplitude → a held switch is crossed by **duration**: maternal flips, transient paternal reverts (PO1); dominant maternal **sign** inherited under opposing parents, agreement reinforces (PO2); the asymmetry is **universal** across the measured germline atlas (13/13) (PO3). *Honesty:* PO3's first hypothesis ("paternal disadvantage rises with γ") **failed** on the substrate (ρ=−1.0); rewritten to universality, ρ reported as-it-falls, **no directional claim graded, no γ tuned**.
> - **VK (`rna_vaccine_kinetics.py`, VK1–VK3) — Track IV-1 + IV-3.** Prime–boost interval has an **interior optimum** in GC rounds (IM1 GC loop reused unchanged; decay at the measured escape rate) (VK1); saRNA's longer same-amplitude window crosses the protected basin **more reliably** than mRNA, post-flip durability honestly identical (VK2).
> - **LV (`lever_map.py`, LV1–LV5) — Track V-1…V-4.** Lever-A sub-types move the threshold, **CRISPRa re-classifies to Lever B** (LV1); Lever-B sub-types (siRNA −, ASO-splice fixed-γ coordinate, saRNA +, miRNA-sponge +) all reversible at fixed γ (LV2); decision **boundary curve** h_path*(γ)=h_cap−spinodal(γ) falls, finite γ* mandates Lever A, substrate-confirmed both sides (LV3); durable correction **without an edit** by re-dosing w>w* (LV4).
> - **Ledger:** new firewalled `[O]` items **O-23…O-27** (parent-of-origin penetrance · prime-boost days · saRNA/mRNA titre · per-modality lever efficiency · edit-free re-dose schedule).
> - **With Track V closed, every pure-simulation roadmap item is done.** The only remaining frontier is the **(B) held-out validation** — non-identified on the ordering axis (FV5), otherwise needs the firewalled Δh.
>
> **TURNKEY — DONE (v0.14.0).** The three deferred chapters (PO/VK/LV) are now published exactly per the spec that previously stood here: **§16 PO**, **§17 VK**, **§18 LV** inserted before the scoreboard and the scoreboard renumbered **§16 → §19**, each a standard answer-first chapter (graded claim-strip → LOCK→Derive→Gate → reproduce line → magnitude-firewall box) whose every displayed number is pulled from `reports/emergence_results.json` via the `num()`/`R()` helpers (battery blocks `PO_parent_of_origin` / `VK_rna_vaccine_kinetics` / `LV_lever_map`). Grades as specified: PO = parent-of-origin sign/context **[V]** / penetrance **[O]**; VK = RNA-vaccine kinetics **[V]** / days,titre **[O]**; LV = the lever map **[V]** / efficiency,schedule **[O]**. Count strings updated (16→19 chapters, 15→18 batteries) across hub/landing/scoreboard/sitemap/llms.txt; `tools/verify_site.py` passes green (sitemap = page count) and the site rebuilds twice to an identical sha256. **Implementation note for future windows:** to keep every chapter's firewall-box link byte-identical, the scoreboard's directory **slug** was preserved (`16-scoreboard-firewall-ledger`) while only its displayed number bumped to 19; reading order (hub TOC, prev/next, sitemap, llms) derives from the ordered chapter **list**, not directory sort, so it is correct regardless of slug. The 14 content chapters not adjacent to the insertion are byte-identical; chapter 15's sole delta is its forward `next` nav link (→ §16 PO), an inserted-neighbour update, not content.

### Prior status (v0.12.0-bvalidation-identifiability-FV5) — research complete + **(B) held-out score run (NULL) and stress-tested → NON-IDENTIFIED**; canonical 16-chapter site current
- **15 batteries PASS:** R, RS, A4, TC, TG, GE, CH, I, IM, V, GT, AM, FM, DM, **FV**. *(v0.13.0 adds PO, VK, LV → 18.)*
- **NEW this release — FV (feasibility_validation): the (B) held-out score, run once.** FM/DM named **(B)**
  — scoring the no-tuning (A)-map predicted SET+ORDERING against **held-out** measured pre/post expression of
  real perturbed cells — as the only honest crossing from map to evidence. FV runs it on the **ordering**
  axis and records a **clean NULL**. Target = **Replogle 2022 *Cell* genome-scale Perturb-seq (CRISPRi)**,
  DOI 10.1016/j.cell.2022.05.013 (readout `obs/fold_expr` = on-target fraction of transcript remaining); γ is
  measured purely from promoter DNA and was frozen before any expression data was seen, so it is genuinely
  held out. **Sign-locked prediction:** higher-γ resists knockdown ⇒ ρ(γ, fold_expr) > 0. **Result
  (primary, K562 genome-wide, n=43):** ρ = **−0.0760, p = 0.6283** — slightly *opposite*, non-significant
  across every cutoff, sign disagrees on RPE1 (ρ=+0.21), SET-proxy AUC = 0.389. γ **re-read frozen**,
  hash-checked; **nothing tuned**. Per the promotion rule (p<0.05 **and** ρ>0) this **promotes nothing**:
  **O-19/O-20/O-22 stay `[O]`**, the (A) map stays `[V]` and untouched. Low power (n=43/11) ⇒ does **not
  refute**, finds **no support**; consistent with FM4. FV1–FV5 = provenance/held-out integrity · no-tuning
  ordering score + promotion rule · null robustness (cutoff sweep + cross-cell-line) · (A)/(B) firewall ·
  **GC-identifiability stress test**. **FV5 (NEW, v0.12.0):** γ = −mean(NN ΔG37) tracks promoter GC by
  construction (ρ(γ,GC)=**0.9909/0.9818/0.9643**), CRISPRi efficiency is GC/accessibility-driven, so
  partialling GC out leaves the γ effect non-significant + sign-unstable (**+0.1259/−0.2228/−0.4282**, p≥0.40)
  ⇒ the ordering score is **NON-IDENTIFIED** (cannot separate barrier from GC), not "signal absent". Promotes
  nothing. See §2 and `IRREPRODUCIBILITY_LEDGER.md` → "(B) validation — first held-out score + identifiability
  stress test".
- **NEW — `bvalidation/replogle2022_heldout.cache.json` (held-out slice, vendored) + `data/fetch_bvalidation.py`
  + pure-numpy stats (Spearman + exact t-p; reproduces SciPy, no new dep).** The cache holds ONLY the matched
  held-out measurements; γ is re-read from the frozen atlases at score time. `verify()` is the offline
  integrity + headline-reproduction gate, wired into `run_all.py` as `validation_ok`; `--fetch` rebuilds from
  figshare (article 20029387). `reports/research_complete.json` gains a `heldout_validation_verify` block.
- **NEW this release — DM (disease_feasibility_map):** carries the feasibility map into the **disease class**
  named for this increment — **cancer** (16 suppressor/oncogene promoters) and **neurodegeneration** (9 genes;
  Parkinson's master genes + HTT/SOD1 proteinopathy bridge). The panels are **inherited from the sibling
  `vp-site` disease_kit by re-measuring (never importing) γ** through this kit's own SOX9-anchor-gated fetcher,
  so four shared loci (PTEN, VHL, SOD1, HTT) reproduce to 4 decimals as a **no-tuning cross-package check**.
  The disease-class content FM lacked is the **corrective-sign law** (DM2): a mechanism-forced sign (LOF→`+`
  restore / GOF→`−` knockdown) corrects each gene, the opposite sign from the same basin does not, and the sign
  is **orthogonal to γ** (suppressors/oncogenes interleave, point-biserial ≈ −0.015). DM3 makes the firewall
  operational as a **two-lever decision** (reversible Lever-B reachable for every switch; Lever-A reserved for
  coding-SET lesions). DM4 is the (A)/(B) honesty gate + cross-package invariant. The **map + sign law** are
  **[V]**; absolute corrective dose and the per-patient corrected-yes/no are firewalled — new `[O]` items
  **O-21/O-22**, the (A)/(B) principle for disease encoded in blueprint **§B.10**. See §2.
- **NEW — `inherited/onco_gamma.json` + `inherited/neurodegen_gamma.json` (measured, anchor-gated):** cancer
  (TP53/RB1/PTEN/VHL/APC/BRCA1/NF1/CDKN2A/STK11 + KRAS/MYC/EGFR/BRAF/MDM2/BCL2/PIK3CA) and neurodegeneration
  (SNCA/LRRK2/VPS35/PRKN/PINK1/PARK7/GBA1 + HTT/SOD1), declared by function, anchor reproducing **live**.
  A correctness fix was required vs the inherited fetcher: the NCBI record is chosen by **official-symbol match**,
  not blind `ids[0]` (which mis-resolves HTT→SLC6A4, APC→PROC).
- **Concept DOI embedded (this release):** **10.5281/zenodo.20783547** (Zenodo, resolves to latest). The
  writing pass regenerated `docs/`, so every page now carries it (footer/claim-strip/JSON-LD/llms.txt); the old
  "DOI pending" v0.5.0 snapshot is superseded.
- **NEW (v0.7.0) — FM (rna_feasibility_map):** answers "does putting RNA in actually change the cell?"
  honestly. The **map** is [V] (FM1 flip-drive=measured spinodal, ordered by γ; FM3 reversible-vs-latched +
  saRNA/siRNA sign); a self-contained sim **cannot** return the yes/no (FM4 — it rides on the firewalled Δh
  atop assumed R19 dynamics; crossing to evidence is the **(B)** held-out score). Includes a **measured
  autism/brain-cell extension** (FM2) on `inherited/neuro_gamma.json` (10 SFARI monogenic ASD genes). New `[O]`
  items O-19/O-20. The (A)/(B) principle is encoded in blueprint **§B.9**. See §2.
- **IM (immune_maturation, v0.6.0):** the immune-strengthening battery (IM1 affinity maturation · IM2
  innate/adaptive · IM3 tolerance), all **[V]**; O-16/O-17/O-18. See §2.
- **NCBI offline verifies reproduce** (no network): the RNA-machinery γ atlas (SOX9-anchor-gated), the
  imprinted-locus γ atlas, the **two new disease γ atlases** (cancer + neurodegeneration, SOX9-gated, with the
  4-locus cross-package check), and **42 wide-window A4 coordinate reads** across four sets.
- **Determinism:** every battery emitted twice is byte-identical (seed=19).
- **No regression:** every pre-existing inherited measured γ atlas is byte-identical (sha256-verified); the
  vendored substrate and the **entire canonical site `docs/` are byte-identical**; all additions were additive.

**FINAL RESULT (v0.9.0 site — regenerated this release):** the canonical write-up is built and verified under
VP-SPEC v1.8 → `docs/` (**15 chapters** + hub + landing) from the deterministic generator `tools/build_site.py`
(**378** displayed numbers, all fetched from `reports/`, built twice to an identical sha256; zero-drift). The
structural **search-gate is now a script** — `tools/verify_site.py` → all pages answer-first, ≥2 valid JSON-LD
per chapter, `sitemap <loc>` == page count (**17**), `llms.txt` < 5 KB, claim-strip + firewall on every chapter,
and every displayed number present verbatim. Canonical base `https://jamming-physics.org/`, volume
`/inheritance/`. The three previously-staged chapters (§9 IM, §13 FM, §14 DM) and the DOI are now **absorbed**;
RNA vaccines/gene-therapy/application-map renumbered to §10/§11/§12 and the scoreboard to §15.

**Site is now current to the 15-battery layer (v0.11.0).** The §(B)-validation writing pass is **DONE**:
`docs/` now carries **16 chapters** — FV is published as **§15 (the (B) held-out validation)** and the
scoreboard moved to **§16**. The displayed-number ledger grew 378 → 405 → **412** (FV5 added v0.12.0),
`tools/verify_site.py` re-runs green (18 pages, sitemap = 18 URLs), and the site rebuilds twice to an identical
sha256. `docs/` is generated
solely from `reports/` (byte-identical numeric inputs), so this was a documentation-only, additive pass.
`manifest/kit_manifest.csv` is produced by `tools/gen_manifest.py` (regenerable, excludes `__pycache__`).
**The next writing/research work is additive** (the *neuronal* (B) score for O-20, disease-vs-normal
corrective sign-law for DM2/O-22, and a SET-membership precision/recall scorer — see below).

**On the (B) frontier — run, stress-tested, and sharpened.** The **ordering** sub-score of (B) is **done** (FV,
above): scored on held-out Replogle CRISPRi knockdown depth, it is a **NULL** (ρ=−0.08, p=0.63) and promotes
no `[O]` item. **v0.12.0 stress-tested it (FV5):** the score is **NON-IDENTIFIED** — γ tracks promoter GC by
construction (ρ(γ,GC)=0.99/0.98/0.96) and CRISPRi efficiency is GC/accessibility-driven, so partialling GC out
leaves no identified γ signal (+0.13/−0.22/−0.43, p≥0.40). So the null is "cannot separate signal from
confound", not "signal absent". **Correcting an earlier framing:** the remaining *neuronal* (B) is **NOT
data-blocked** — public neuronal CRISPRi data exist (i³Neuron CROP-seq, Tian et al. 2019, GEO `GSE124703`;
CRISPRbrain) — but because γ↔GC collinearity is a **cell-type-invariant** property of promoter DNA, the same
knockdown-depth ordering on neuronal data inherits the **identical non-identification** and does **not** advance
O-20. *The data are not the obstacle; the test is degenerate.* What stays genuinely **open** therefore needs a
readout **not collinear with promoter GC** — a downstream **response magnitude** — which requires the firewalled
drive Δh: namely (i) an **identified** neuronal/disease (B), (ii) **SET-membership precision/recall** (operating
Δh), and (iii) the **corrective sign-law (DM2)** (disease-vs-normal corrective pre/post data — a knockdown in a
cancer line is not a correction context). Any such work is additive and must keep the measured atlases +
substrate + held-out cache byte-identical and γ re-read frozen (never tuned), exactly as FV does. Until those
run, the per-cell/per-patient yes/no stays firewalled `[O]`.

**v0.17.0 update — the sign-law `−` arm is now SCORED (FV7), reframing item (iii) above.** FV6 (v0.15.0) had
already corrected the picture: of the open (B) items, the *ordering* ones are non-identified and only the
*corrective sign-law* is identified + firewall-clean, blocked on **bidirectional** disease-correction data
rather than on Δh. FV7 then found the right held-out context for its **`−` arm**: a CRISPR-**knockout** screen
*is* the `−` (loss) operation, and in a **cancer** line viability *is* a correction phenotype — so a knockout
in a cancer line **is** a correction context for the `−` arm (the v0.12.0 remark that it is "not a correction
context" was about the *ordering*/knockdown-depth framing and is superseded for the *sign* test). Scored on
DepMap 24Q2 CRISPR-KO gene-effect (n=16 onco), the `−` arm **passes**: point-biserial(GOF, −gene_effect) =
**+0.4940**, exact one-sided p = **0.0227**, predicted direction, **identified** (point-biserial(sign,GC) =
−0.1222; GC-partialled +0.4939 unchanged), firewall-clean. This is the kit's **first held-out POSITIVE** and
earns the `−` arm a **[V]**; **O-22 stays `[O]`** with its obstacle narrowed to the **`+` RESTORE arm alone**
(the only genuinely-open item left), and **O-21** (absolute dose) stays `[O]`. So the residual open (B) list is
now: (i) an **identified** neuronal/disease (B) on a response-magnitude readout (firewalled Δh); (ii)
**SET-membership precision/recall** (operating Δh); and (iii) the sign-law's **`+` RESTORE arm** (over-
expression of a LOF suppressor / a toxic-GOF PD-gene knockdown with a disease/normal contrast) — *not* Δh-blocked.
The site §15-extension for FV7 is now PUBLISHED (v0.19.0 writing pass); turnkey record in §3.

**v0.18.0 update — the sign-law `+` RESTORE arm is now SCORED (FV8), CLOSING item (iii) and correcting the framing.** FV8 found the held-out context that mirrors FV7: a CRISPR-**activation** screen *is* the `+` (gain/restore)
operation, and in a **cancer** line growth *is* a correction phenotype for a LOF suppressor — so suppressor
activation in a cancer line **is** a correction context for the `+` arm. Scored on Horlbeck 2016 hCRISPRa-v2
K562 growth (n=16 onco), the `+` arm **passes**: point-biserial(LOF, −growth_phenotype) = **+0.4852**, exact
one-sided p = **0.0274**, predicted direction, **identified** (point-biserial(sign,GC) = +0.1222; GC-partialled
+0.4731 unchanged), firewall-clean — nearly symmetric to FV7's `−` arm. This is the kit's **second held-out
POSITIVE**, and together with FV7 the corrective sign-law is now **bidirectionally `[V]`**, which **removes in
full** the bidirectional-DATA obstacle. So **item (iii) is closed.** **But O-22 STILL stays `[O]` — and the
reason has changed.** FV8 **corrects** FV7's "obstacle narrowed to the `+` arm alone" framing: with both arms
scored, O-22's residual obstacle is **no longer DATA but the firewall itself**. The bidirectional sign-law is
a **class-level, direction-only** statement (*which way* to push each disease class); O-22 is a **per-patient,
absolute** outcome that needs the firewalled per-patient magnitude/penetrance (absolute drive size = **O-21**).
A direction-only law cannot certify a per-patient yes/no, and promoting O-22 would leak direction-only `[V]`
into per-patient absolute `[V]`. So the residual open (B) list collapses to the **firewall-bound** items only:
(i) an **identified** neuronal/disease (B) on a response-magnitude readout (firewalled Δh); (ii)
**SET-membership precision/recall** (operating Δh); and (iii→) **O-22's per-patient magnitude and O-21's
absolute dose** — both firewalled to clinicians/regulators by design, *not* simulation-axis items. **No
simulation-axis (B) item remains open.** The site §15-extension for FV8 is now PUBLISHED (v0.19.0 writing pass); turnkey record in §3.

## 1. What was built (the architecture)
The genome is read on **two channels**, and that is the spine of every result:
- **γ — the SET (material).** −mean NN-stacking ΔG (SantaLucia 1998) over the promoter; scales every R19
  switch (`spinodal=2(γ/3)^1.5`, `barrier=γ²/4`). **Fixed in the genome — the environment cannot rewrite it.**
- **A4 — the COORDINATE (structure).** Compartment shells, anchors, motor/anchor loops, and the 3D helical
  CONTACT phase, read by the vendored `vp_a4.py` from wide windows. **Orthogonal to γ** (the helical contact
  phase is ~98% independent of γ) and **the channel the environment reorganises and a small RNA targets**
  (RNA acts by complementarity = it names an A4 coordinate).
- **h — the DRIVE.** The reversible signal the environment/RNA/a vaccine writes, applied **at an A4
  coordinate**, never on γ. Methylation and small RNA are its two writers.

Everything is direction-only behind the **magnitude firewall**: WHICH switch, the SIGN of the drive, the
ORDERING/DECAY/BOUNDARY are read [V]; absolute phenotype/dose/titre/penetrance/generation-count are [O]
(named in `IRREPRODUCIBILITY_LEDGER.md`), and every clinical use is handed to clinicians/regulators.

## 2. The findings (every battery's headline claim + grade)
**Channels & RNA**
- **R (rna_layer):** small RNA is a reversible h-write (γ unchanged); two signs (siRNA→OFF / saRNA→ON);
  measured carrier atlas is R19-bistable; the drive is reversible. [V]
- **RS (rna_species):** "small RNA" resolves into miRNA/piRNA/tsRNA/m6A by measured machinery; each a signed
  drive; production-stability orders by machinery barrier (piRNA deepest); METTL3/YTHDF2 writer/eraser
  reversibility; germline-competent carriers (piRNA/tsRNA/VASA). [V]
- **A4 (a4_layer):** A4 ⊥ γ (γ tracks GC R²≈69%; helical contact phase ≈98% independent; same-γ/different-
  contact pairs exist → **γ alone is degenerate**); RNA is coordinate-targeting (contact-competence gates a
  fixed drive at fixed γ); the environment writes A4, not γ; inheritance is of an A4 configuration. [V]
- **TC (two_channel):** methylation × RNA both write the same h on one switch — same-sign ADD, opposite-sign
  VETO, hysteresis PATH-DEPENDENCE. [V]

**Environment → germline (transgenerational)**
- **TG (env_to_germline):** SET byte-identical parent→child; reprogramming firewall squares survival (p²);
  heritability ranks ascending-γ (ρ≈0.99); inherited sign preserved; RNA-only drive decays by ~F3 while a
  deep-barrier mark persists. [V]
- **GE (germline_escapee):** on the measured imprinted atlas, survival ranks ascending-γ (KCNQ1OT1 best,
  SNRPN worst, ρ=1.0); two erasures resolved (PGC vs zygotic, harsher dominates); critical re-write rate w*
  separates maintained from transient inheritance. [V]
- **CH (coordinate_heritability):** heritability couples γ AND A4 — at matched γ, the contact-competent
  coordinate inherits better (MEST vs MOS); parent-of-origin contact configuration mapped (paternal contact
  fraction 0.5 vs maternal 0.0 in-panel); joint (γ, A4) ordering puts deep-γ + contact-competent loci on top
  (NNAT). [V]

**Immunity, vaccine, gene therapy**
- **I (transgenerational_immunity):** memory = held basin, lifetime (MFPT) ranks ascending-γ; trained
  immunity = pre-tilt (smaller recall drive); transgenerational priming inheritable + fading (direction-only). [V]/[O]
- **IM (immune_maturation):** affinity maturation **emerges** from an iterated germinal-centre loop with an
  **interior optimum** in selection stringency (peak at survivor-fraction 0.4; weak selection → negative gain,
  over-stringent → gain collapses); innate (RUNX1) vs adaptive (PAX5) is a **two-timescale durability split**
  (survival-based MFPT ratio ≈2.37, slow arm = deeper barrier, tracking the measured γ); tolerance is the
  **opposite-sign drive** on the same switch — memory↔tolerance with symmetric thresholds at the spinodal
  magnitude and **both** end-states held after the drive clears (hysteresis). [V]; absolute pressure,
  lifetimes, and desensitisation dose are [O] (O-16/17/18). [V]/[O]
- **V (rna_vaccine):** vaccine = supra-spinodal flip into the protected basin, held after clearance; boost
  schedule has an interior optimum tracking the measured protection half-life; transient payload / persistent
  protection. [V]
- **GT (gene_therapy):** Lever A edits the SET (moves spinodal/barrier, irreversible by a drive); Lever B
  resets the drive reversibly via RNA; the lever choice is a geometry threshold. [V]
- **AM (a4_application_map):** the applications live on the (γ, A4) plane — prime-boost dose is
  coordinate-dependent; the two levers partition (γ, contact); the **3D contact boundary curve** δ*(γ) RISES
  with γ (a deeper switch needs more A4 contact-assist to stay drive-reachable). [V]
- **FM (rna_feasibility_map):** the honest answer to "does putting RNA in actually change the cell?" The
  **map** is [V] — the minimal flip-drive is the measured spinodal h*(γ); a flip occurs at k=h/h*≥1 and not
  below; the absolute flip-drive rises with γ (ordering of "easiest to flip" set by measured promoter γ);
  sub-spinodal transients revert while supra-spinodal transients latch (hysteresis); saRNA=+/siRNA=− sign. A
  self-contained sim **cannot** return the yes/no — it rides on the firewalled drive Δh atop assumed R19
  dynamics, so a "flipped" screen is Δh-assumption replay, not evidence; the crossing to evidence is the
  **(B)** held-out score (predicted flipped-switch set+ordering vs measured pre/post, no-tuning). Extends to
  the **measured autism atlas** (every ASD promoter R19-bistable; flip-drive ordered by γ; SCN2A shallowest →
  PTEN deepest) — structure transfers [V], per-neuron yes/no [O]/(B). O-19/O-20; principle in blueprint §B.9.
- **DM (disease_feasibility_map):** the same map carried into the **disease class** (cancer + Parkinson's),
  with the panels **inherited by re-measuring** the sibling `vp-site` disease_kit's γ through this kit's anchor
  gate — four shared loci (PTEN/VHL/SOD1/HTT) reproduce to 4 decimals as a no-tuning cross-package check. DM1
  every cancer + neurodegeneration promoter is R19-bistable, correction-difficulty ordered by measured γ. DM2
  the **corrective-sign law**: the mechanism-forced sign (LOF→`+` restore / GOF→`−` knockdown) drives each gene
  out of its pathological basin while the opposite sign from the same basin does not — and the sign is
  **orthogonal to γ** (suppressors/oncogenes interleave; point-biserial ≈ −0.015). DM3 the **two-lever
  decision**: reversible Lever-B reachable for every switch (required drive grows with γ); Lever-A reserved for
  coding-SET lesions (= the firewall, not a recommendation). DM4 the (A)/(B) honesty gate + cross-package
  invariant. Map + sign law [V]; absolute corrective dose + per-patient corrected-yes/no [O]/(B). O-21/O-22;
  principle in blueprint §B.10.

**The one-sentence synthesis.** SET (γ, genome) vs DRIVE (h, environment/RNA, applied at an A4 COORDINATE)
is the SAME decomposition behind inheritance, immunity, vaccines, and gene therapy; γ is the unwritable
ruler, A4 is the writable structure that RNA targets and the environment inherits, and reversibility (a
drive is reversible, a SET-edit is not) organises the therapeutic map.

## 3. The writing pass — add the IM + FM + DM chapters and the DOI  ✅ EXECUTED (v0.9.0); reused for the §(B) FV chapter (v0.11.0)
**Status: DONE.** This writing pass was executed in v0.9.0 — `docs/` was the **15-chapter, DOI-bearing**
canonical site (IM = §9, FM = §13, DM = §14; RNA-vaccines/gene-therapy/application-map renumbered to
§10/§11/§12, scoreboard to §15; 378 displayed numbers; `tools/verify_site.py` green). **The identical
procedure was reused in v0.11.0** to add **§15 — the (B) held-out validation (FV)** (scoreboard renumbered to
§16; 405 displayed numbers; search-gate green), so `docs/` is now the **16-chapter** volume current with the
15-battery research layer (see §0). The spec below is
retained as the **record of the procedure that was followed** — there is nothing left to do here; the next
frontier is **(B) validation** (§0). The mechanism was (blueprint §B.7; VP-SPEC v1.8):
1. Re-confirm `python repro/run_all.py` is all_green (the lock is a mechanism — a regression re-locks writing).
2. Author the IM and FM chapters **per-title in English** (VP-SPEC C0/C2/C4): one self-contained page each,
   answer-first (40–60 words), each quantitative result reproduced (2×sha256), every [O] reasoned, JSON-LD +
   breadcrumbs + a claim-strip carrying the grade + the reproduce link. **`tools/build_site.py` must be
   extended** so the battery/chapter counts and the scoreboard chapter pick up IM + FM from `reports/` (it
   derives counts from the reports; the prose strings still say "eleven batteries / 12 chapters" — update those
   too). The **DOI is already wired** into the generator (footer/claim-strip/JSON-LD/llms.txt); regeneration
   alone embeds it, replacing the frozen "DOI pending".
3. **Turnkey IM chapter (place between §8 immune strengthening (I) and the vaccine chapter):**
   - *Answer-first:* the immune system's three maturation behaviours are one switch read three ways — affinity
     maturation **emerges** from iterated selection (interior-optimal stringency), innate vs adaptive is a
     two-timescale durability split set by barrier depth, and tolerance is the same switch driven the other way.
   - *Claims + grades:* IM1 emergence + interior optimum (peak survivor-fraction 0.4) **[V]**; IM2 durability
     ordering + separation (MFPT ratio ≈2.37, slow arm = deep barrier) **[V]**; IM3 memory↔tolerance sign law +
     both states held (hysteresis) **[V]**. Firewalled: absolute selection pressure→affinity (O-16), absolute
     innate/adaptive lifetimes (O-17), absolute desensitisation dose/clinical tolerance (O-18).
   - *Reproduce:* `python engine/immune_maturation.py` (deterministic, seed 19).
   - *Firewall line (verbatim intent):* we read the SHAPE, the ORDERING/decay, and the SIGN; absolute
     pressures, lifetimes, and doses are [O]; clinical immunisation and desensitisation belong to clinicians
     and regulators.
   **Turnkey FM chapter (place last, before the scoreboard/ledger):**
   - *Answer-first:* "does putting RNA in actually change the cell?" — a self-contained model gives only the
     **map** (which switch a drive reaches, the ordering, reversibility), never the yes/no, because the answer
     rides on the firewalled drive Δh atop assumed R19 dynamics; the yes/no is earned only by **(B)** scoring
     against held-out measured pre/post expression, no-tuning.
   - *Claims + grades:* FM1 flip-drive=measured spinodal, absolute ordering by γ **[V]**; FM2 autism extension
     — every measured ASD promoter R19-bistable, flip-drive ordered by γ (SCN2A→PTEN) **[V]**; FM3
     reversible-vs-latched + saRNA/siRNA sign **[V]**; FM4 the (A)/(B) honesty invariant (a flip is
     Δh-assumption replay, not evidence) **[V]**. Firewalled: the self-contained yes/no (O-19), the per-neuron
     autism yes/no (O-20). Principle: blueprint §B.9.
   - *Reproduce:* `python engine/rna_feasibility_map.py` (deterministic, seed 19).
   - *Firewall line:* FM reads the feasibility map only; the "did the cell change" yes/no is [O] until the (B)
     held-out score exists; clinical RNA therapy belongs to clinicians and regulators.
4. Chapter map for the writing pass (one per battery group, plus framing): the two-channel architecture (γ SET
   + A4 coordinate) · the RNA writable channel (R, RS) · A4 orthogonality & coordinate-targeting (A4) · the
   two epigenetic channels (TC) · environment→germline & the reprogramming firewall (TG) · the imprinted
   escapee atlas (GE) · γ↔A4 coordinate-resolved heritability + parent-of-origin (CH) · immune strengthening &
   inheritance (I) · **immune maturation (IM) ← new** · RNA vaccines (V) · gene-therapy levers (GT) · the
   (γ, A4) application map & contact boundary (AM) · **RNA feasibility map — (A) vs (B) + autism (FM) ← new** ·
   the honest scoreboard + firewall (the ledger).
5. Keep the firewall visible in every chapter; hand every clinical claim to clinicians/regulators.
6. Authorship/DOI/authority per the program (ORCID 0009-0002-7535-8245, jamming-physics.org, CC BY 4.0);
   confirm the exact title/abbrev/DOI at write time.

**TURNKEY — DONE (v0.16.0): §15 (the (B) held-out validation chapter) was extended with the FV6 decomposition.**
This was executed exactly per the spec retained below — one subsection added to the existing §15 (after its FV5
*"is the null even identified?"* section, before the *"What (B) moved"* close), with **no new chapter** (count
stays 19) and **no new battery**. The sub-answer is the partition framing; every number is pulled from
`reports/emergence_results.json` → `FV_feasibility_validation` (test FV6) via `num()`/`R()` (ρ(γ,GC)=0.9944,
R²(γ~GC)=0.9948, point-biserial(sign,GC)=+0.0153, R²(sign~GC)=0.0002, ≈4974×, frozen cross-check
point-biserial(sign,γ)=−0.0148); the `candidate_B_observable_map` 2×2 and the `corrected_obstacle_for_O22` are
rendered from the same block; the in-chapter correction (the sign crossing is firewall-clean and GC-orthogonal, so
its only obstacle is bidirectional disease-correction DATA, **not** Δh) is recorded; grade **[V]** on an **[F]**
criterion, promoting nothing (O-19/O-20/O-22 stay `[O]`). `tools/verify_site.py` re-ran green (sitemap = page
count, 561 displayed numbers verbatim, 2×sha256 identical); chapter count stayed **19** and the scoreboard slug
stayed `16-scoreboard-firewall-ledger`. The spec that was followed is retained below as the record of the
procedure — there is nothing left to do here.
Writing is deferred per the research-first rule (blueprint §B.7), exactly as the FV chapter itself, and the
PO/VK/LV chapters, were deferred before their writing pass. **The `docs/` tree is byte-identical this release;
do not edit it until a writing pass.** When that pass runs, add one subsection to §15 (after its existing
"is the null even identified?" FV5 section), spec:
   - *Sub-answer (40–60 words):* the held-out null is not one fact but a *partition*. Because γ = −mean(NN ΔG37)
     is collinear with promoter GC (ρ=0.9944, R²=0.9948 on the disease panel), **every γ-ordered prediction is
     non-identified as a class**; the corrective sign-law is the **only** prediction orthogonal to GC and the
     only (B) that is both identifiable and firewall-clean.
   - *Claim + grade:* FV6 identifiability decomposition **[V]** on an **[F]** criterion (the partition is forced
     by the measured ρ(γ,GC) and point-biserial(sign,GC); nothing is fitted). It **promotes nothing** — O-19/
     O-20/O-22 stay `[O]`; the actual sign-law (B) *score* remains `[O]`, data-blocked.
   - *Numbers to render (all from `reports/emergence_results.json` → `FV_feasibility_validation`, via the
     `num()`/`R()` zero-drift helpers — never typed literally):* ρ(γ,GC)=**0.9944**, R²(γ~GC)=**0.9948**,
     point-biserial(sign,GC)=**+0.0153**, R²(sign~GC)=**0.0002**, separation ratio **≈4974×**, and the frozen
     cross-check point-biserial(sign,γ)=**−0.0148** (reproduces DM2). Pull the `candidate_B_observable_map`
     2×2 and `corrected_obstacle_for_O22` straight from the same block.
   - *Correction to record in-chapter:* the earlier "all (B) crossings need the firewalled Δh" framing is
     **superseded** — the sign-law crossing is firewall-clean and GC-orthogonal, so its only obstacle is
     **bidirectional disease-correction DATA** (a `−` oncogene arm and a `+` suppressor/PD arm together), not Δh.
   - *Reproduce:* `python engine/feasibility_validation.py run_battery` (deterministic, seed 19); the FV6 row
     reads PASS.
   - *Firewall line:* FV6 reads only WHICH axis is identifiable and WHICH sign corrects — never a magnitude;
     the sign-law's clinical use belongs to clinicians and regulators.
   When the chapter is extended, bump only the §15 displayed-number count and re-run `tools/verify_site.py`
   (sitemap = page count, every ledgered number verbatim, 2×sha256 identical); the chapter **count stays 19**
   and the scoreboard slug stays `16-scoreboard-firewall-ledger`.

**TURNKEY — DONE (v0.19.0): §15 extended with the FV7 sign-law `−`-arm held-out score.** ✅ EXECUTED in the v0.19.0 writing pass. The research (FV7) shipped in v0.17.0; this pass published it, exactly as FV6 (v0.15.0) was published in v0.16.0. A **subsection was added to §15** (placed *after* the v0.16.0 FV6 *"The null is a partition, only the sign-law survives"*
subsection and before the *"What (B) moved"* close), **no new chapter** (count stays 19), **no new battery**
(FV stays one battery). Spec:
   - *Sub-answer (40–60 words):* the partition's one identifiable + firewall-clean crossing — the corrective
     sign-law — is no longer only *named*; its **`−` arm is now SCORED on held-out data**. A CRISPR-knockout
     screen is the `−` operation and cancer-cell viability is its correction phenotype, so GOF oncogenes are
     dependencies and LOF suppressors are not — and the separation is significant, identified, firewall-clean.
     The kit's **first held-out POSITIVE**.
   - *Claim + grade:* FV7 sign-law `−`-arm held-out score **[V]** (held-out positive, identified, firewall-
     clean). It promotes the `−` arm only — **O-22 stays `[O]`** (obstacle narrowed to the `+` RESTORE arm
     alone), **O-21 stays `[O]`** (absolute dose). NOT a discovery of the oncogene/suppressor split (frozen
     priors; DepMap is the independent test).
   - *Numbers to render (all from `reports/emergence_results.json` → `FV_feasibility_validation` → test FV7,
     via the `num()`/`R()` zero-drift helpers — never typed literally):* n_onco = **16** (7 GOF / 9 LOF),
     point_biserial_GOFsign_vs_neg_gene_effect = **+0.4940**, exact_permutation_p_one_sided = **0.0227**
     (n_permutations **11440**), per-gene **12/16** (GOF 7/7), and the identification triplet
     point_biserial_sign_vs_GC = **−0.1222**, GOF_mean_GC = **0.532** / LOF_mean_GC = **0.543**,
     partial_point_biserial_sign_given_GC = **+0.4939**. Use the `B_signlaw_minus_arm_headline` string as the
     prose source.
   - *Provenance to state:* DepMap 24Q2 Public CRISPRGeneEffect (Chronos), figshare article `25880521`, file
     id `46489063` (Model.csv `46489732`); `corr_sign` forced by MECHANISM, frozen before any DepMap data;
     `corr_sign`/GC re-read frozen at score time (cache carries gene-effects only). Neurodegeneration genes
     cached but **out of readout scope** (cancer viability ≠ proteinopathy correction).
   - *Correction to record in-chapter:* FV7 does **not** reintroduce Δh as an O-22 obstacle — FV6 corrected
     that; the absolute magnitude is the separate item O-21. O-22's remaining obstacle is purely the `+` arm.
   - *Reproduce:* `python engine/feasibility_validation.py` (deterministic, seed 19); the FV7 row reads PASS.
     Cache rebuildable from source via `python data/fetch_signlaw_depmap.py --fetch`.
   - *Firewall line:* FV7 reads only the **sign** of the GOF-vs-LOF separation under the `−` operation — never
     a magnitude/dose/titre; γ untouched; the sign-law's clinical use belongs to clinicians and regulators.
   When the chapter is extended, bump only the §15 displayed-number count and re-run `tools/verify_site.py`
   (sitemap = page count, every ledgered number verbatim, 2×sha256 identical); the chapter **count stays 19**
   and the scoreboard slug stays `16-scoreboard-firewall-ledger`.

**TURNKEY — DONE (v0.19.0): §15 extended with the FV8 sign-law `+`-arm held-out score (the bidirectional close).** ✅ EXECUTED in the v0.19.0 writing pass. The research (FV8) shipped in v0.18.0; this pass published it together with FV7. A **subsection was added to §15** (placed *after* the v0.17.0 FV7 `−`-arm subsection
and before the *"What (B) moved"* close), **no new chapter** (count stays 19), **no new battery** (FV stays
one battery). Spec:
   - *Sub-answer (40–60 words):* the corrective sign-law's **`+` RESTORE arm is now SCORED on held-out data of
     the opposite operation** — a CRISPR-activation screen is the `+` operation and cancer-cell growth is its
     correction phenotype, so LOF suppressors are growth-suppressive on activation and GOF oncogenes are not.
     The separation is significant, identified, firewall-clean — the kit's **second held-out POSITIVE**, the
     mirror of FV7, completing the **bidirectional** test.
   - *Claim + grade:* FV8 sign-law `+`-arm held-out score **[V]** (held-out positive, identified, firewall-
     clean); together with FV7 the sign-law is **bidirectionally [V]** (both arms, direction-only). **O-22
     STILL stays `[O]`**, and the chapter must state the **corrected reason**: with both arms scored, O-22's
     obstacle is **no longer data but the firewall** — a class-level direction-only law cannot certify a
     per-patient absolute outcome (that needs the firewalled per-patient magnitude; absolute dose = **O-21**,
     also `[O]`). NOT a discovery of the oncogene/suppressor split (frozen priors; CRISPRa is the independent
     test).
   - *Numbers to render (all from `reports/emergence_results.json` → `FV_feasibility_validation` → test FV8,
     via the `num()`/`R()` zero-drift helpers — never typed literally):* n_onco = **16** (9 LOF / 7 GOF),
     point_biserial_LOFsign_vs_neg_growth = **+0.4852**, exact_permutation_p_one_sided = **0.0274**
     (n_permutations **11440**), per-gene **10/16** (LOF 7/9), and the identification triplet
     point_biserial_sign_vs_GC = **+0.1222**, LOF_mean_GC = **0.5426** / GOF_mean_GC = **0.5320**,
     partial_point_biserial_sign_given_GC = **+0.4731**. Use the `B_signlaw_plus_arm_headline` string as the
     prose source.
   - *Provenance to state:* Horlbeck et al. 2016, *eLife* 5:e19760, DOI `10.7554/eLife.19760`, Supplementary
     file 10 (hCRISPRa-v2 K562 gene growth phenotypes); `corr_sign` forced by MECHANISM, frozen before any
     CRISPRa data; `corr_sign`/GC re-read frozen at score time (cache carries growth phenotypes only).
     Neurodegeneration genes cached but **out of readout scope** (leukemia growth ≠ proteinopathy correction).
   - *Correction to record in-chapter:* FV8 **corrects** FV7's "obstacle narrowed to the `+` arm alone"
     framing — with the `+` arm now scored, O-22's residual obstacle is the **firewall** (per-patient
     magnitude), not data; the absolute drive size is the separate item O-21. This is **not** a contradiction
     of FV6 (the sign-law needed bidirectional data, not Δh; both arms scored with zero Δh).
   - *Honest caveat to state:* K562 is a single CML line (a single-line growth screen, vs FV7's pan-cancer
     mean); TP53 is null and CDKN2A is deleted in K562, so activation has a weak/absent locus to restore and
     those genes push **against** the prediction (conservative panel, no cherry-picking).
   - *Reproduce:* `python engine/feasibility_validation.py` (deterministic, seed 19); the FV8 row reads PASS.
     Cache rebuildable from source via `python data/fetch_signlaw_crispra.py --fetch` (pure-stdlib `.xlsx`
     reader, no new dependency).
   - *Firewall line:* FV8 reads only the **sign** of the LOF-vs-GOF separation under the `+` operation — never
     a magnitude/dose/titre; γ untouched; the sign-law's clinical use belongs to clinicians and regulators.
   When the chapter is extended, bump only the §15 displayed-number count and re-run `tools/verify_site.py`
   (sitemap = page count, every ledgered number verbatim, 2×sha256 identical); the chapter **count stays 19**
   and the scoreboard slug stays `16-scoreboard-firewall-ledger`.



## 4. Reproduce / file map
- Run everything: `python repro/run_all.py` → `reports/research_complete.json` (all_green) +
  `reports/emergence_results.json` (full detail).
- Inputs: `inherited/` (vendored `vp_substrate.py` + `vp_a4.py`; measured γ atlases; A4 coordinate atlases +
  wide-window caches). Engines: `engine/*.py` (one per battery + `_substrate.py` loader). Re-measure from
  NCBI (optional): `data/fetch_rna_gamma.py --fetch`, `data/fetch_imprint_gamma.py --fetch`.
- Ledgers: `COMPLETION_LEDGER.md` (DONE/TODO), `IRREPRODUCIBILITY_LEDGER.md` (every [O] + obstacle),
  `CHANGELOG.md` (per release), `manifest/kit_manifest.csv` (sha256 of every file).

## 5. Standing discipline (unchanged, binding)
One zip, internal root `vp_inheritance_kit/`, **additive only, no regression, no fragmentation**; vendored
substrate + A4 single-source and read-only; γ measured/anchor-gated and never fitted; read **both** γ and A4
(γ alone is degenerate); grade chain [F]/[V]/[O]/[L]; DNA-emergence + magnitude firewall; English docs;
state passes by files only.
