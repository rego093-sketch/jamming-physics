# COMPLETION LEDGER — VP Inheritance Kit (explicit DONE / TODO)

`python repro/run_all.py` → **all_green = true** (both NCBI anchors + 4 A4 sets + disease cross-package check reproduce · **(B) held-out validation cache reproduces** · **(B) sign-law `−`-arm DepMap cache reproduces** · **(B) sign-law `+`-arm CRISPRa cache reproduces** · 18/18 batteries PASS · determinism holds). The FV battery is now **FV1–FV8**: as of **v0.17.0** the corrective sign-law's **`−` arm is SCORED on held-out DepMap CRISPR-KO data** (point-biserial = +0.494, exact p = 0.0227), and as of **v0.18.0** its **`+` RESTORE arm is SCORED on held-out Horlbeck 2016 CRISPRa data** (point-biserial = +0.4852, exact p = 0.0274) — both identified and firewall-clean — so the corrective sign-law is now **BIDIRECTIONALLY `[V]`** (the kit's first and second held-out POSITIVES). `python tools/build_site.py && python tools/verify_site.py` → **19-chapter canonical site, search-gate PASS, 2×sha256 identical** (PO/VK/LV published v0.14.0; **§15 carries the FV6 (B)-identifiability decomposition** as of v0.16.0; and **as of v0.19.0 the FV7 `−`-arm and FV8 `+`-arm held-out POSITIVES are PUBLISHED into §15** as two new subsections; **585** displayed numbers). **Every research result — Tracks I–V and FV1–FV8 — is now on the canonical site; no deferred writing item remains.**

> **RESEARCH PHASE COMPLETE — TRACKS I–V ALL CLOSED ON THE SIMULATION AXIS; THE ONE OPEN (B) FRONTIER IS NOW BIDIRECTIONALLY SCORED.** As of **v0.13.0** the last tractable pure-simulation items in Tracks II/IV/V are shipped as three additive batteries (**PO** parent-of-origin, **VK** RNA-vaccine kinetics, **LV** lever map), each direction-only with the magnitude firewall intact; the 15 prior batteries + vendored substrate + all measured γ atlases stay byte-identical. The only items still genuinely open were the **(B) held-out validation** crossings, and as of **v0.15.0** (test **FV6**) those crossings are *partitioned*: every **γ-ordered** prediction is **non-identified** (γ = −mean(NN ΔG37) is collinear with promoter GC, ρ≈0.99 — *do not re-run as ordering tests*); a **response-magnitude** readout is identified but firewall-blocked (needs the Δh); and the **corrective sign-law** (DM2: LOF→`+`, GOF→`−`) is the **sole identifiable *and* firewall-clean** crossing — blocked **only on bidirectional disease-correction DATA** (a `+` arm and a `−` arm), *not* on Δh and *not* on the GC confound. **As of v0.17.0 (test FV7) the `−` arm was SCORED** on held-out DepMap CRISPR-KO data and **passes** (`[V]`: point-biserial = +0.494, exact p = 0.0227; identified; firewall-clean), and **as of v0.18.0 (test FV8) the `+` RESTORE arm is now SCORED** on held-out Horlbeck 2016 CRISPRa data and **passes** (`[V]`: point-biserial = +0.4852, exact p = 0.0274; identified — point-biserial(sign,GC) = +0.122, GC-partialled +0.473 unchanged; firewall-clean). **The bidirectional test FV6 named is therefore COMPLETE** — the corrective sign-law is bidirectionally `[V]` (both arms, direction-only). **O-22 (per-patient corrected-yes/no) nonetheless stays `[O]`**: with both arms scored, its residual obstacle is no longer DATA but the **firewall itself** — a class-level direction-only law cannot certify a per-patient absolute outcome (that needs the firewalled per-patient magnitude; the absolute drive size is **O-21**). FV8 thus *corrects* FV7's "narrows to the `+` arm alone" framing. **No simulation-axis (B) item remains open; what remains for O-22/O-21 is the firewall, by design.**

## DONE (this release, v0.19.0-heldout-positives-published — writing pass: the FV7 `−`-arm and FV8 `+`-arm held-out POSITIVES are PUBLISHED into §15; no new science, no new chapter, no new battery, no regression)
| area | item | status | grade |
|---|---|---|---|
| site | **§15 extended with TWO subsections** in `tools/build_site.py` — *"The sign-law's `−` arm, scored on held-out data — the first held-out positive"* (FV7) and *"The sign-law's `+` RESTORE arm, scored on held-out data — the bidirectional close"* (FV8) — placed after the FV6 partition subsection, before the *"What (B) moved"* close. **No new chapter (stays 19), no new battery (FV stays one)** | DONE | — |
| numbers | every displayed FV7/FV8 number pulled via `num()`/`R()` from `reports/emergence_results.json` (tests FV7/FV8) — FV7 +0.4940 / p 0.0227 / 12/16 / GOF 7/7 / sign↔GC −0.1222 / partial +0.4939 / figshare `25880521`; FV8 +0.4852 / p 0.0274 / 10/16 / LOF 7/9 / sign↔GC +0.1222 / partial +0.4731 / *eLife* `19760` / DOI `10.7554/eLife.19760` — all verbatim; per-gene ratios + DOI are sourced strings | DONE | — |
| firewall — the load-bearing call | each subsection reads only the **sign** of the separation (never a magnitude); γ untouched; clinical use handed to clinicians/regulators. The FV8 subsection states it plainly: bidirectionally `[V]` (direction-only) yet **O-22 STILL `[O]`**, its obstacle now the **firewall itself, not data** (per-patient magnitude; absolute drive size = **O-21**, also `[O]`) | DONE | [V] / O-21,O-22 [O] |
| chapter framing | the §15 **headline answer and title are UNCHANGED** — they describe the γ-ORDERING null, which stays a null; FV7/FV8 are the orthogonal **sign** axis, a deeper sub-result | DONE | — |
| accuracy fix | the one content change to the *"What (B) moved"* close: *"As the previous section shows…"* → *"As the identifiability analysis above shows…"* (the inserted subsections shifted the back-reference); heading, numbers, claims, grades unchanged | DONE | — |
| scoreboard sync | the same rebuild flushes the **stale O-22 scoreboard note** (§16) — the uploaded v0.18.0 `docs/` predated the v0.17.0/v0.18.0 FV7/FV8 notes authored in `IRREPRODUCIBILITY_LEDGER.md`; verified pre-existing (a clean rebuild from the **unmodified** v0.18.0 `build_site.py` reproduces this §16 byte-for-byte). Slug stays `16-scoreboard-firewall-ledger` | DONE | — |
| verify | `tools/verify_site.py` **green**: 21 pages, **19 chapters**, sitemap = 21, **585** displayed numbers verbatim (**561 → 585**: twelve FV7 + twelve FV8 ledgered), all answer-first, search-gate PASS; site rebuilds **twice to an identical sha256** | DONE | — |
| invariant | the vendored substrate, `vp_a4`, all 7 γ atlases, all **7** caches, all **18** engines, both `reports/*.json` numeric inputs, `_meta.json`, sitemap/llms.txt, hub + landing, and the **17** content chapters not adjacent to §15 are **byte-identical**; only `build_site.py`, §15, the §16 ledger-note flush, `site_numbers.json`, and `manifest` differ | DONE | — |
| complete | **with FV7 and FV8 published, every research result — Tracks I–V and FV1–FV8 — is now on the canonical site; no deferred writing item remains** | DONE | — |

## DONE (this release, v0.18.0-signlaw-plus-arm-bidirectional — research pass: the sign-law `+` RESTORE arm scored on held-out CRISPRa, bidirectional test complete; no tuning, no regression)
| area | item | status | grade |
|---|---|---|---|
| reception | **`data/fetch_signlaw_crispra.py` NEW** — receives the `+`-arm held-out target (Horlbeck 2016 hCRISPRa-v2 K562 growth, eLife `19760`, supp. file 10, DOI `10.7554/eLife.19760`); `--fetch` downloads the `.xlsx` via a **pure-stdlib** zipfile+ElementTree reader (no openpyxl/pandas) keeping only matched rows, `verify()` reproduces the onco `+`-arm headline offline from the cache + **frozen** atlas (no network/numpy). Cache carries **growth phenotypes only** — `corr_sign`/GC/γ never smuggled | DONE | — |
| data | **`bvalidation/crispra_horlbeck2016_signlaw_heldout.cache.json` NEW** — provenance, held-out warrant, sign-locked prediction, readout scope, honest caveats, per-gene growth phenotype + Mann-Whitney p for 16 onco + 9 neurodegen matched rows (36888 table rows; all 16 onco present) | DONE | — |
| engine | **FV8 added** to `feasibility_validation.py` (FV1–FV7 → FV1–FV8): scores the corrective sign-law's **`+` arm** — under the `+` (activation) operation LOF suppressors are growth-suppressive and GOF oncogenes are not. `corr_sign`/GC re-read **frozen**; reads only the **sign** of the separation; the explicit `O22_obstacle_corrected` field | DONE | **[V] held-out** |
| result | **the `+` arm SCORES** (n = 16 onco; 9 LOF/7 GOF): point-biserial(LOF, −growth_phenotype) = **+0.4852**, exact one-sided permutation p = **0.0274** (11440 perms), predicted direction; per-gene **10/16** correct (LOF **7/9**) — the kit's **second held-out POSITIVE**, nearly symmetric to FV7's `−` arm (≈0.49 both) | DONE | **[V]** |
| identification | **NOT a GC artifact** (re-checked live in FV8): point-biserial(sign,GC) = **+0.1222**, LOF mean GC **0.5426** vs GOF mean GC **0.5320** (balanced, diff<0.05), GC-partialled point-biserial = **+0.4731** (unchanged, same sign) — lands on the unique identified + firewall-clean axis FV6 named | DONE | [V] |
| bidirectional | with both arms scored the corrective sign-law is now **BIDIRECTIONALLY `[V]`** (direction-only), **removing in full** the bidirectional-DATA obstacle FV6 named | DONE | **[V] both arms** |
| firewall — the load-bearing call | **O-22 STILL stays `[O]`**, and FV8 **corrects** FV7's "narrows to the `+` arm alone" framing: with both arms in, O-22's residual obstacle is **no longer DATA — it is the firewall itself**. The sign-law is **class-level + direction-only**; O-22 is a **per-patient absolute** outcome needing the firewalled **per-patient magnitude/penetrance** (absolute dose = **O-21**, stays `[O]`). Promoting O-22 would leak direction-only `[V]` into per-patient absolute `[V]`. Not a contradiction of FV6 (both arms scored with **zero** Δh). NOT a discovery of the oncogene/suppressor split (frozen priors); K562 single CML line, TP53-null/CDKN2A-deleted push AGAINST | DONE | [V] / O-21,O-22 [O] |
| gate | `run_all.py` wires `fetch_signlaw_crispra.verify()` as **`signlaw_plus_arm_validation_ok`** into `all_green`; → **18 batteries** PASS (FV now FV1–FV8) + both anchors + disease cross-package + `validation_ok` + `signlaw_validation_ok` + `signlaw_plus_arm_validation_ok` + determinism; reports regenerate (FV1–FV8), `research_complete.json` byte-identical across two runs | DONE | — |
| site | **FV8 §15-extension DEFERRED** (research-first rule, FV6/FV7/IM/FM/PO/VK/LV precedent); site stays the verified **19-chapter** volume; turnkey §15-extension spec recorded in `HANDOVER.md` | DONE | — |
| invariant | γ, vendored substrate, `vp_a4`, all 7 γ atlases, the **7 prior caches** (incl. the FV7 DepMap cache), the 17 other engines, and the **entire `docs/` tree** are **byte-identical**; only the new fetcher + new cache + `feasibility_validation.py` + `run_all.py` + the 2 reports + ledgers/handover/START_HERE + manifest differ | DONE | — |

## DONE (this release, v0.17.0-signlaw-minus-arm-scored — research pass: the sign-law `−` arm scored on held-out DepMap; no tuning, no regression)
| area | item | status | grade |
|---|---|---|---|
| reception | **`data/fetch_signlaw_depmap.py` NEW** — receives the `−`-arm held-out target (DepMap 24Q2 CRISPRGeneEffect, figshare `25880521`/`46489063`); `--fetch` streams the matrix keeping only matched columns, `verify()` reproduces the onco `−`-arm headline offline from the cache + **frozen** atlas (no network/numpy). Cache carries **gene-effects only** — `corr_sign`/GC/γ never smuggled | DONE | — |
| data | **`bvalidation/depmap24q2_signlaw_heldout.cache.json` NEW** — provenance, held-out warrant, sign-locked prediction, readout scope, per-gene mean/median/frac_dependent for 16 onco + 8 neurodegen matched rows (1150 models; GBA1 not in matrix) | DONE | — |
| engine | **FV7 added** to `feasibility_validation.py` (FV1–FV6 → FV1–FV7): scores the corrective sign-law's **`−` arm** — under the `−` (knockout) operation GOF oncogenes are dependencies and LOF suppressors are not. `corr_sign`/GC re-read **frozen**; reads only the **sign** of the separation | DONE | **[V] held-out** |
| result | **the `−` arm SCORES** (n = 16 onco; 7 GOF/9 LOF): point-biserial(GOF, −gene_effect) = **+0.4940**, exact one-sided permutation p = **0.0227** (11440 perms), predicted direction; per-gene **12/16** correct (GOF **7/7**) — the kit's **first held-out POSITIVE** | DONE | **[V]** |
| identification | **NOT a GC artifact** (re-checked live in FV7): point-biserial(sign,GC) = **−0.1222**, GOF mean GC **0.532** vs LOF mean GC **0.543** (balanced), GC-partialled point-biserial = **+0.4939** (unchanged) — lands on the unique identified + firewall-clean axis FV6 named | DONE | [V] |
| firewall | the `−` arm earns `[V]`; **O-22 stays `[O]`** with its obstacle **narrowed to the `+` RESTORE arm alone** (FV7 does NOT reintroduce Δh — FV6 corrected that); **O-21** (absolute dose) stays `[O]`, firewalled. NOT a discovery of the oncogene/suppressor split (frozen priors; DepMap is the independent test); 4/9 LOF genes pan-essential and push AGAINST the prediction; pan-cancer mean | DONE | [V] / O-21,O-22 [O] |
| gate | `run_all.py` wires `fetch_signlaw_depmap.verify()` as **`signlaw_validation_ok`** into `all_green`; → **18 batteries** PASS (FV now FV1–FV7) + both anchors + disease cross-package + `validation_ok` + `signlaw_validation_ok` + determinism; reports regenerate (FV1–FV7) | DONE | — |
| site | **FV7 §15-extension DEFERRED** (research-first rule, FV6/IM/FM/PO/VK/LV precedent); site stays the verified **19-chapter** volume; turnkey §15-extension spec recorded in `HANDOVER.md` | DONE | — |
| invariant | γ, vendored substrate, `vp_a4`, all 7 γ atlases, the 6 prior caches, and the **entire `docs/` tree** are **byte-identical**; only the new fetcher + new cache + `feasibility_validation.py` + `run_all.py` + the 2 reports + ledgers/handover/START_HERE + manifest differ | DONE | — |


| area | item | status | grade |
|---|---|---|---|
| site | **§15 (the (B) held-out validation) extended** with the FV6 subsection *"The null is a partition, not one fact — only the sign-law survives"* — published from `reports/` via `num()`/`R()`; **no new chapter, no new battery** (chapter count stays **19**, battery count stays **18**) | DONE | — |
| site | every FV6 number rendered zero-drift from `FV_feasibility_validation` (test FV6): ρ(γ,GC)=**0.9944**, R²(γ~GC)=**0.9948**, point-biserial(sign,GC)=**+0.0153**, R²(sign~GC)=**0.0002**, separation **≈4974×**, frozen cross-check point-biserial(sign,γ)=**−0.0148** (reproduces DM2) | DONE | [V] on [F] |
| site | the **2×2 (identified? × firewall-clean?)** rendered straight from `candidate_B_observable_map`; corrective sign-law isolated as the **unique open frontier**; the **corrected O-22 obstacle** (bidirectional disease-correction DATA, not Δh) recorded in-chapter | DONE | [V] |
| site | scoreboard page **flushes the v0.15.0 O-22 ledger note** that was authored in `IRREPRODUCIBILITY_LEDGER.md` but not yet regenerated into `docs/`; scoreboard slug preserved (`16-scoreboard-firewall-ledger`); magnitude firewall intact in the new subsection | DONE | — |
| verify | `tools/verify_site.py` green: 21 pages, **19 chapters**, sitemap = page count, **561** displayed numbers all verbatim, all pages answer-first; site rebuilds **twice to identical sha256** | DONE | [F] |
| invariants | vendored substrate + `vp_a4` + **all 7 γ atlases + 6 caches + held-out cache + all 18 engines + the 2 reports + the 14 untouched content chapters** byte-identical (diff-verified); only `tools/build_site.py`, the 2 regenerated pages (§15 + scoreboard), `reports/site_numbers.json`, and `manifest/kit_manifest.csv` change; **no γ or measured datum tuned** | DONE | [F] |


| area | item | status | grade |
|---|---|---|---|
| engine | **FV6 added** to `feasibility_validation.py` (FV1–FV5 → FV1–FV6): the **(B) identifiability decomposition** — partitions every (B)-testable VP prediction into the non-identified γ-ordered class vs the identifiable mechanism-sign | DONE | [V] on [F] criterion |
| finding | **confound axis measured on the disease panel:** ρ(γ,GC) = **0.9944** (Spearman), **R²(γ~GC) = 0.9948** — γ essentially *is* GC; every γ-ORDERED prediction (FM1 reachability, FV knockdown-depth, IM2 durability, DM1 difficulty) is non-identified **as a class** (FV5 was one instance) | DONE | [V]/[F] |
| finding | **sign axis is the sole identifiable exception:** point-biserial(sign,γ) = **−0.0148** (reproduces DM2's −0.015, frozen cross-check) and the **new** point-biserial(sign,**GC**) = **+0.0153**, R²(sign~GC) = **0.0002** — a **≈4974×** variance-explained separation; the corrective sign is **orthogonal to the GC confound** | DONE | [V] |
| finding | **2×2 (identified? × firewall-clean?):** knockdown-depth = clean-but-non-identified (degenerate); response-magnitude = identified-but-firewall-blocked (needs Δh); **corrective SIGN = identified AND firewall-clean** → the unique open (B) | DONE | [V] |
| correction | **O-22 obstacle CORRECTED:** prior framing said all (B) crossings "need the firewalled Δh"; the **sign** crossing (DM/(B)) does **not** — a sign test is firewall-clean and GC-orthogonal, so its only obstacle is **bidirectional disease-correction DATA** (a `+` arm and a `−` arm). The ordering crossings remain non-identified | DONE | — |
| ledger | IRREPRODUCIBILITY_LEDGER "(B) validation" section upgraded (FV1–FV5 → FV1–FV6); the decomposition, the 2×2, and the corrected O-22 obstacle recorded; O-19/O-20/O-22 stay `[O]` (FV6 promotes nothing) | DONE | — |
| gate | `run_all.py` → **18 batteries** PASS (FV now FV1–FV6) + both anchors + disease cross-package + `validation_ok` + determinism; reports rebuild **twice to identical sha256** | DONE | — |
| invariants | vendored substrate + `vp_a4` + **all 7 γ atlases + 6 caches + held-out cache + `_substrate.py` + the 17 other engines + the generated `docs/` tree** byte-identical (diff-verified); only `feasibility_validation.py` + the 2 regenerated reports change; **no γ or cached datum tuned** | DONE | [F] |
| site | FV6 chapter **deferred** (research-first rule, IM/FM/PO/VK/LV precedent); site stays the verified **19-chapter** volume; turnkey §15-extension spec in HANDOVER §0 | DONE | — |



## DONE (this release, v0.13.0-tracks-II-IV-V-closed — three additive batteries, no regression)
| area | item | status | grade |
|---|---|---|---|
| engine | **PO `parent_of_origin.py` (PO1–PO4)** — Track II-3: maternal (sustained) vs paternal (transient) context asymmetry at EQUAL amplitude (crossing set by DURATION); inherited SIGN law under opposing parents; asymmetry **universal** across the measured germline atlas (13/13) | DONE | [V] / penetrance [O] |
| engine | **VK `rna_vaccine_kinetics.py` (VK1–VK3)** — Track IV-1 prime–boost interval **interior optimum** in GC rounds (reuses IM1 GC loop unchanged, decay at measured escape rate); IV-3 saRNA's longer same-amplitude window crosses the protected basin more reliably than mRNA (post-flip durability honestly identical) | DONE | [V] / days,titre [O] |
| engine | **LV `lever_map.py` (LV1–LV5)** — Track V-1 Lever-A sub-types (knockout/base-edit/prime-edit move the threshold; **CRISPRa re-classifies to Lever B**); V-2 Lever-B sub-types (siRNA −, ASO-splice fixed-γ coordinate, saRNA +, miRNA-sponge +, all reversible at fixed γ); V-3 decision **boundary curve** h_path*(γ)=h_cap−spinodal(γ) falls, finite γ* mandates Lever A (substrate-confirmed both sides); V-4 durable correction **without an edit** via re-dosing (w>w*) | DONE | [V] / efficiency,schedule [O] |
| honesty | PO3's first hypothesis ("paternal disadvantage rises with γ") **failed** on the substrate (ρ=−1.0 under equal-relative amplitude); rewritten to the robust **universality** claim with ρ reported as-it-falls, **no directional claim graded, no γ tuned** | DONE | [V] |
| honesty | LV1 CRISPRa reversibility read against the **standing pathological repression** it treats (not bistable h=0, where any flip sticks); the substrate then correctly returns it to Lever B | DONE | [V] |
| ledger | IRREPRODUCIBILITY_LEDGER **O-23..O-27** itemised (parent-of-origin penetrance · prime-boost days · saRNA/mRNA titre · per-modality lever efficiency · edit-free re-dose schedule) | DONE | — |
| blueprint | Part B STATUS: **II-3, IV-1, IV-3, V-1, V-2, V-3, V-4 marked done; Tracks II/IV/V complete** | DONE | — |
| gate | `run_all.py` → **18 batteries** PASS + both anchors + disease cross-package + `validation_ok` + determinism (3 new batteries wired into batteries/runners/scoreboards) | DONE | — |
| invariants | vendored substrate + `vp_a4` + **all 7 γ atlases + 6 caches + held-out cache + all 15 prior engines** byte-identical (diff-verified); only `run_all.py` changed (additive wiring) | DONE | [F] |
| site | PO/VK/LV chapters **deferred** (research-first rule, IM/FM precedent); site stays the verified 16-chapter volume; turnkey 3-chapter spec in HANDOVER §0 | DONE | — |

> **RESEARCH PHASE COMPLETE + FINAL RESULT DELIVERED + (B) FRONTIER RUN, STRESS-TESTED & PUBLISHED.** The canonical write-up is built and verified as the **16-chapter, DOI-bearing** volume (`docs/`, `tools/build_site.py`); `PHASE = writing`. The named next-research frontier — **(B) held-out validation** — was **run** (battery **FV**, ORDERING axis) as a recorded **NULL** (ρ=−0.08, p=0.63 on held-out Replogle CRISPRi) and, as of **v0.12.0**, **stress-tested** (test **FV5**): the score is **NON-IDENTIFIED** — γ = −mean(NN ΔG37) tracks promoter GC by construction (ρ(γ,GC)=0.99/0.98/0.96), CRISPRi efficiency is GC/accessibility-driven, and partialling GC out leaves no identified γ signal (+0.13/−0.22/−0.43, all p≥0.40). So the null is "cannot separate signal from confound", not "signal absent"; it promotes no `[O]`. **This also settles the open neuronal (B):** γ↔GC collinearity is cell-type-invariant, so repeating the knockdown-depth ordering on neuronal data (which **exists** — i³Neuron CROP-seq, GEO `GSE124703`/CRISPRbrain) inherits the same degeneracy and does **not** advance O-20 — *the data are not the obstacle; the test is degenerate*. An identified (B) needs a downstream response-magnitude readout, which needs the firewalled Δh. The published site carries FV as **§15** (now with an *"is the null even identified?"* section); scoreboard is §16. **Still genuinely open:** an identified neuronal/disease (B) (response-magnitude, firewalled Δh) and the corrective sign-law DM2 (disease-vs-normal corrective data) — see HANDOVER §0 and blueprint §B.9/§B.10.

## DONE (this release, v0.12.0-bvalidation-identifiability-FV5 — additive (B) stress test, no regression)
| area | item | status | grade |
|---|---|---|---|
| engine | **FV5 added** to `feasibility_validation.py` (FV1–FV4 → FV1–FV5): GC-identifiability stress test of the (B) ordering null | DONE | [V] |
| finding | γ↔GC near-collinear **by construction** (ρ=0.9909/0.9818/0.9643); GC-partialled γ effect non-significant + sign-unstable (+0.1259/−0.2228/−0.4282, p≥0.40) → ordering score **non-identified** | DONE | [V] |
| finding | neuronal (B) for O-20 **settled without new data**: collinearity is cell-type-invariant, so neuronal knockdown-depth ordering (GEO `GSE124703`/CRISPRbrain, data exist) inherits the same degeneracy | DONE | — |
| correction | earlier "remaining neuronal (B) is data-blocked" **overstatement corrected** → the data exist; the *test* is degenerate; an identified (B) needs firewalled Δh | DONE | — |
| ledger | IRREPRODUCIBILITY_LEDGER "(B) validation" section upgraded (FV1–FV4 → FV1–FV5); confound footnote → measured non-identification; O-19/O-20/O-22 stay [O] with sharpened obstacle | DONE | — |
| blueprint | §B.9 + §B.10 STATUS notes updated to v0.12.0 (non-identification; neuronal consequence; identified (B) needs Δh) | DONE | — |
| site | §15 chapter gains *"Is the null even identified?"* section; 405 → **412** displayed numbers; 2×sha256 identical; search-gate PASS | DONE | — |
| invariants | vendored substrate + 7 γ atlases + A4 + **`bvalidation/` held-out cache byte-identical**; FV5 adds only analysis (no tuning); gate **15/15 green**, anchor reproduces, determinism holds | DONE | — |

## DONE (this release, v0.11.0-canonical-site-16ch — the §(B) writing pass, documentation-only, no regression)
| area | item | status | grade |
|---|---|---|---|
| site | canonical site regenerated **15 → 16 chapters**; the published volume now catches up to the research layer (FV) | DONE | — |
| site | **§15 (B) held-out validation (FV)** chapter authored — the one honest crossing from map to evidence, run once: ρ=−0.0760, p=0.6283, n=43 (K562 GWPS), a recorded **NULL** that promotes nothing | DONE | [V] (honest null) |
| site | FV chapter is answer-first with the graded claim-strip + the magnitude firewall; FV1 held-out integrity (61 γ hash-equal, zero mismatches) · FV2 no-tuning score + promotion rule · FV3 null robustness (cutoff sweep + RPE1 sign-disagreement) · FV4 (A)/(B) firewall | DONE | [V] |
| site | scoreboard renumbered **§15 → §16**; battery/chapter counts updated (14→15 batteries, 15→16 chapters) throughout hub/landing/scoreboard | DONE | — |
| site | every displayed value fetched from `reports/` via `num()`/`R()` (zero-drift); **405** numbers (was 378); **2×sha256 identical** determinism gate | DONE | [F] |
| verify | `tools/verify_site.py` search-gate re-run green: answer-first all pages, ≥2 JSON-LD/chapter, sitemap = **18** URLs = pages, llms.txt 2.8 KB, every number verbatim | DONE | [F] |
| invariance | vendored substrate + **all seven measured γ atlases** + A4 + engines + `reports/emergence_results.json` (the site's only numeric input) + the `bvalidation` cache byte-identical to v0.10.0 (sha256-verified) | DONE | [F] |


| area | item | status | grade |
|---|---|---|---|
| (B) | **battery FV (feasibility_validation): the (B) held-out score, run once** on the ordering axis | DONE | [V] honest null |
| (B) | held-out target = **Replogle 2022 CRISPRi** (DOI 10.1016/j.cell.2022.05.013); γ measured from DNA, frozen before any expression seen | DONE | — |
| (B) | **sign-locked** prediction ρ(γ,`fold_expr`)>0 → **ρ=−0.0760, p=0.6283, n=43** (K562 GWPS); non-sig across all cutoffs; RPE1 sign disagrees; AUC 0.389 | DONE | NULL, reported as it falls |
| (B) | **promotion rule applied honestly** (p<0.05 ∧ ρ>0) → **promotes nothing**; O-19/O-20/O-22 stay `[O]`; (A) map stays `[V]` untouched | DONE | [V] firewall |
| (B) | FV1 provenance/held-out integrity · FV2 no-tuning score+rule · FV3 null robustness (cutoff sweep + cross-cell-line) · FV4 (A)/(B) firewall | DONE | [V] |
| data | `bvalidation/replogle2022_heldout.cache.json` (matched held-out slice + provenance); γ **not** stored as truth (re-read frozen at score time) | DONE | [F] |
| tooling | `data/fetch_bvalidation.py` — offline `verify()` (integrity + headline reproduction, wired as `validation_ok`); `--fetch` rebuilds from figshare | DONE | [F] |
| tooling | pure-numpy Spearman + exact t-based p (incomplete beta) — **reproduces SciPy bit-for-bit**, no new dependency | DONE | [F] |
| gate | `run_all.py` → **15 batteries** PASS + anchors + disease cross-package + **`validation_ok`** + determinism; `heldout_validation_verify` block added to report | DONE | — |
| invariance | vendored substrate + **all seven measured γ atlases** + A4 + engines + **canonical site `docs/`** byte-identical to v0.9.0 (sha256-verified) | DONE | [F] |

## DONE (this release, v0.9.0-canonical-site-15ch — the writing pass, documentation-only, no regression)
| area | item | status | grade |
|---|---|---|---|
| site | canonical site regenerated **12 → 15 chapters**; published volume now level with the research layer (IM/FM/DM) | DONE | — |
| site | **§9 Immune maturation (IM)** chapter authored — interior optimum (sf 0.40), MFPT ratio 2.369×, memory↔tolerance sign law | DONE | [V] / abs [O] |
| site | **§13 RNA feasibility map + autism (FM)** chapter authored — reachability=spinodal, 10 ASD promoters, FM4 honesty gate | DONE | [V] / yes-no [O]/(B) |
| site | **§14 Disease feasibility map + corrective sign (DM)** chapter authored — 25 loci, mechanism-forced sign ⟂ γ, 4-locus cross-package | DONE | [F]/[V] / dose [O] |
| site | DOI `10.5281/zenodo.20783547` now embedded on every page (was "DOI pending"); chapters renumbered (V→10, GT→11, AM→12, scoreboard→15) | DONE | — |
| site | every displayed value fetched from `reports/` via `num()`/`R()` (zero-drift); **378** numbers; **2×sha256 identical** determinism gate | DONE | [F] |
| verify | `tools/verify_site.py` — search-gate script: answer-first all pages, ≥2 JSON-LD/chapter, sitemap=17 URLs=pages, llms.txt 2.6 KB, every number verbatim | DONE | [F] |
| tooling | `tools/gen_manifest.py` — `kit_manifest.csv` is now a **regenerable** artifact (sha256 of every tracked file; excludes `__pycache__`) | DONE | [F] |
| phase | `PHASE` + `run_all.py` phase field → `writing`; gate unaffected; `emergence_results.json` **byte-identical** across re-run | DONE | — |
| invariance | vendored substrate + **all measured γ atlases** + A4 + engines byte-identical to v0.8.0 (sha256-verified) | DONE | [F] |

## DONE (this release, v0.8.0-disease-feasibility-map — additive disease-class extension, no regression)
| area | item | status | grade |
|---|---|---|---|
| measure | cancer γ atlas `inherited/onco_gamma.json` (16 genes; suppressors + oncogenes, declared by function, anchor reproduced **live**) | DONE | [V] on measurement |
| measure | neurodegeneration γ atlas `inherited/neurodegen_gamma.json` (9 genes; Parkinson's + HTT/SOD1 bridge, declared by function, anchor **live**) | DONE | [V] on measurement |
| inherit | panels inherited from sibling `vp-site` disease_kit by **re-measuring** (not importing) γ — cross-package check (PTEN/VHL/SOD1/HTT reproduce to 4 dp) | DONE | [V] no-tuning |
| fix | fetcher selects NCBI record by **official-symbol match** (not blind `ids[0]`); correct loci pinned (HTT 3064, APC 324, RB1 5925) | DONE | [F] correctness |
| DM | disease reachability: every cancer + neurodegen promoter R19-bistable; correction-difficulty ordered by measured γ (DM1) | DONE | [V] / abs. Δh [O] |
| DM | corrective-sign law: mechanism-forced sign (LOF→`+` / GOF→`−`) corrects each gene; opposite sign from same basin does not; **orthogonal to γ** (DM2) | DONE | [V] / abs. dose [O] |
| DM | two-lever decision: reversible Lever-B reachable for every switch (drive grows with γ); Lever-A reserved for coding-SET lesions = firewall (DM3) | DONE | [V] / cap [O] |
| DM | (A)/(B) honesty gate + cross-package consistency invariant (4 anchors reproduce) (DM4) | DONE | [V] invariant / per-patient yes-no [O] |
| blueprint | §B.10 (inherit-by-re-measuring, corrective-sign law, two-lever firewall, named (B) disease validation, deliberate-sampling scope) | DONE | — |
| ledger | O-21 (absolute corrective dose) + O-22 (per-patient corrected yes/no = (B)) itemised | DONE | — |
| gate | run_all.py → **14 batteries** PASS + anchors + disease cross-package + determinism | DONE | — |
| invariance | vendored substrate + **all five** prior γ atlases + A4 byte-identical to v0.7.0 (sha256-verified) | DONE | [F] |

## DONE (this release, v0.7.0-feasibility-map — additive research extension + DOI, no regression)
| area | item | status | grade |
|---|---|---|---|
| identity | concept **DOI 10.5281/zenodo.20783547** reflected (generator + START_HERE/HANDOVER); docs pick it up next regen | DONE | — |
| measure | autism-spectrum γ atlas `inherited/neuro_gamma.json` (10 SFARI genes, declared by function, anchor reproduced **live**) | DONE | [V] on measurement |
| FM | reachability map: flip-drive = measured spinodal; absolute flip-drive ordered by measured γ (FM1) | DONE | [V] / abs. Δh [O] |
| FM | autism / brain-cell extension: every ASD promoter R19-bistable, flip-drive ordering tracks γ (FM2) | DONE | [V] / per-neuron yes-no [O]/(B) |
| FM | reversibility + sign law: sub-spinodal reverts, supra-spinodal latches (hysteresis); saRNA↔siRNA (FM3) | DONE | [V] / hold-time [O] |
| FM | (A)/(B) honesty gate: flip is Δh-assumption replay; self-contained sim cannot return yes/no (FM4) | DONE | [V] invariant / yes-no [O] |
| blueprint | §B.9 (A)-map vs (B)-validation split + no-tuning trap + autism extension + named (B) next-research | DONE | — |
| ledger | O-19 (self-contained yes/no) + O-20 (per-neuron autism yes/no) itemised | DONE | — |
| gate | run_all.py → **13 batteries** PASS + anchors + determinism | DONE | — |
| invariance | substrate + all four prior γ atlases + canonical site `docs/` byte-identical (sha256-verified) | DONE | [F] |

## DONE (this release, v0.6.0-immune-maturation — additive research extension, no regression)
| area | item | status | grade |
|---|---|---|---|
| measure | IM battery reads the **measured** immune γ atlas (FOXN1/TLX1/RUNX1/PAX5) on the single substrate | DONE | [V] on measurement |
| IM | affinity maturation **emerges** from the iterated germinal-centre loop; gain has an **interior optimum** (peak at survivor-frac 0.4) | DONE | [V] / abs. pressure [O] |
| IM | innate (RUNX1) vs adaptive (PAX5) = **two-timescale durability split**, MFPT ratio 2.369, slow arm = deep barrier | DONE | [V] / abs. lifetimes [O] |
| IM | tolerance = **opposite-sign drive** on the same switch; symmetric thresholds, **both** end-states held (hysteresis) | DONE | [V] / abs. dose [O] |
| ledger | O-16/O-17/O-18 itemised (each names its obstacle) | DONE | — |
| gate | run_all.py → **12 batteries** PASS + anchors + determinism | DONE | — |
| invariance | substrate + **all four** γ atlases + canonical site `docs/` byte-identical (sha256-verified) | DONE | [F] |
| write | IM chapter intentionally **deferred** — site frozen at 11-chapter v0.5.0 (turnkey spec in HANDOVER) | DONE | — |

## DONE (this release, v0.5.0-canonical-site — the FINAL RESULT)
| area | item | status | grade |
|---|---|---|---|
| write | `PHASE` flipped research→writing after re-confirming all_green | DONE | — |
| write | canonical site `docs/` per VP-SPEC v1.8 (12 chapters + hub + landing) | DONE | [V] |
| write | answer-first + JSON-LD (ScholarlyArticle+BreadcrumbList) every page | DONE | [V] |
| write | graded claim-strip (grade + LOCK→Derive→Gate + reproduce + volume) every chapter | DONE | [V] |
| write | magnitude firewall visible on every chapter; all 15 [O] itemised in §12 | DONE | [V] |
| write | retrieval-ready: robots (7 bots) · sitemap (14 URLs=pages) · llms.txt (2220B<5KB) | DONE | [V] |
| write | deterministic generator `tools/build_site.py` (253 numbers, 2×sha256 identical) | DONE | [V] |
| write | zero-drift: all 253 displayed numbers fetched from `reports/`, appear verbatim in HTML | DONE | [V] |
| write | DOI **pending** (none minted — not fabricated) | DONE | — |
| invariance | vendored substrate + γ/A4 atlases + engines byte-identical to v0.4.0 | DONE | [F] |

## DONE (this release, v0.1.0-research)
| area | item | status | grade |
|---|---|---|---|
| inherit | vendored R19 substrate (single source) | DONE | — |
| inherit | germline γ atlas (13 genes) + offline cache | DONE | [L] measured |
| inherit | immune master γ (FOXN1/TLX1/RUNX1/PAX5) + cache | DONE | [L] measured |
| measure | RNA-machinery γ (12 genes) from **NCBI**, SOX9-gated, cached | DONE | [V] on measurement |
| R | RNA = reversible h-write (γ unchanged) | DONE | [V] |
| R | two signs on one channel (siRNA-OFF / saRNA-ON) | DONE | [V] |
| R | measured RNA-carrier atlas is R19-bistable | DONE | [V] |
| R | payload reversibility (cleared → basin returns) | DONE | [V] |
| TG | SET invariance (genome byte-identical parent→child) | DONE | [V] |
| TG | reprogramming firewall (two erasures → p²) | DONE | [V] |
| TG | heritability ranks ascending-γ (Spearman ρ≈0.99) | DONE | [V] |
| TG | inherited sign preserved through firewall | DONE | [V] |
| TG | RNA decays by ~F3; deep-barrier mark persists | DONE | [V] |
| I | immune memory lifetime (MFPT) ranks ascending-γ | DONE | [V] |
| I | trained immunity = pre-tilt (smaller recall drive) | DONE | [V] |
| I | transgenerational immune priming (direction-only) | DONE | [V]/[O] |
| V | vaccine = supra-spinodal flip + hysteretic hold | DONE | [V] |
| V | boost schedule interior optimum ≈ protection half-life | DONE | [V] |
| V | transient payload / persistent protection | DONE | [V] |
| GT | Lever A: SET-edit moves spinodal/barrier | DONE | [V] |
| GT | Lever B: reversible RNA drive-reset | DONE | [V] |
| GT | decision rule separates the two levers | DONE | [V] |
| gate | run_all.py + research_complete.json (all_green) | DONE | — |
| docs | START_HERE / BLUEPRINT / CHARTER / ledgers / manifest (English) | DONE | — |

## DONE (first research pass, v0.2.0-research — additive on v0.1.0)
| area | item | status | grade |
|---|---|---|---|
| measure | imprinted-locus γ (12 loci) from **NCBI**, SOX9-gated, cached | DONE | [V] on measurement |
| RS | small RNA resolved into miRNA/piRNA/tsRNA/m6A signed drives | DONE | [V] |
| RS | production-stability ordering by machinery barrier (piRNA deepest) | DONE | [V] ordering |
| RS | METTL3/YTHDF2 writer/eraser mark-side reversibility | DONE | [V] |
| RS | germline competence (piRNA/tsRNA/VASA load the gamete) | DONE | [F/V] |
| TC | methylation × RNA same-sign ADD | DONE | [V] |
| TC | methylation × RNA opposite-sign VETO | DONE | [V] |
| TC | hysteresis path-dependence (order of writes latches) | DONE | [V/F] |
| GE | imprinted survival ranks ascending-γ (KCNQ1OT1 best, ρ=1.0) | DONE | [V] |
| GE | two erasures resolved (PGC vs zygotic, harsher dominates) | DONE | [V] |
| GE | re-writing vs persistence: measured critical re-write rate w* | DONE | [V] |
| gate | run_all.py extended to 8 batteries + imprint offline verify | DONE | — |

## DONE (A4 coordinate channel, v0.3.0-research — additive on v0.2.0)
| area | item | status | grade |
|---|---|---|---|
| inherit | vendored A4 engine `vp_a4.py` (shells/anchors/loops/helical contact) | DONE | — |
| measure | A4 coordinates for 12 RNA carriers from **wide NCBI windows** (±15 kb), cached | DONE | [V] |
| A4 | A4 orthogonal to γ (helical contact phase ≈98% independent; same-γ/diff-contact pairs) | DONE | [V] |
| A4 | RNA is coordinate-targeting (contact-competence gates a fixed drive at fixed γ) | DONE | [V] |
| A4 | environment writes A4, not γ (γ sequence-fixed; contact state writable) | DONE | [V/F] |
| A4 | inheritance is of an A4 configuration (held contact state survives erasure) | DONE | [V] |
| gate | run_all.py extended to 9 batteries + A4 offline verify | DONE | — |

## DONE (gamma<->A4 coupling, v0.4.0 — research-closing, additive on v0.3.0)
| area | item | status | grade |
|---|---|---|---|
| measure | wide A4 coordinates for imprinted (12) + germline (13) + immune (4) loci, NCBI-direct, cached | DONE | [V] |
| CH | coordinate-resolved heritability (contact adds heritability at matched gamma) | DONE | [V] |
| CH | parent-of-origin contact configuration mapped (paternal vs maternal) | DONE | [V] |
| CH | joint (gamma, A4) heritability ordering (deep-gamma + contact on top) | DONE | [V] |
| AM | prime-boost dose is A4-coordinate-dependent | DONE | [V] |
| AM | lever map partitions the (gamma, A4) plane | DONE | [V] |
| AM | **3D contact boundary curve** delta*(gamma) rises with gamma | DONE | [V] |
| gate | run_all.py -> 11 batteries + 4-set A4 verify | DONE | — |
| handover | HANDOVER.md (status + synthesis + final-result instructions) | DONE | — |

## TODO (next sessions — see 00_CONTINUATION_BLUEPRINT.md Part B for the full roadmap)
All pure-**simulation** items in Tracks I–V are now **DONE** (Track V closed by the v0.13.0 PO/VK/LV batteries). The **(B) held-out validation** crossings that **FV6 (v0.15.0) re-ranked** are now **fully resolved on the simulation axis**: the two **γ-ordering** tests are **non-identified as a class** (γ≈GC, ρ≈0.99 — *do not re-run as ordering scores*), and **both arms of the corrective sign-law are now SCORED `[V]`** — the **`−` arm** on held-out DepMap CRISPR-KO (FV7, v0.17.0) and the **`+` RESTORE arm** on held-out Horlbeck 2016 CRISPRa (FV8, v0.18.0). **The bidirectional held-out test FV6 named is COMPLETE; no simulation-axis (B) item remains open.** What remains for **O-22** (per-patient corrected-yes/no) and **O-21** (absolute dose) is **not data but the firewall itself** — a class-level direction-only sign-law cannot certify a per-patient absolute outcome, which is firewalled to clinicians/regulators by design (see the FV8 note below):
| track | next item | type | grade target |
|---|---|---|---|
| **FM/(B) validation** | *(γ-ordering — **non-identified**, do not re-run)* score predicted flipped-switch set+ordering vs HELD-OUT siRNA/saRNA pre/post expression | **data** | **non-identified (FV6)** |
| **FM/(B) autism** | *(γ-ordering — **non-identified**, do not re-run)* same ordering (B) score on a neuronal ASD target (ASO/siRNA/saRNA series) | **data** | **non-identified (FV6)** |
| **DM/(B) sign-law — `−` arm** | ✅ **DONE (FV7, v0.17.0)** — scored predicted **corrective SIGN** (GOF→`−` silence) vs HELD-OUT DepMap oncogene knockout: point-biserial = +0.494, exact p = 0.0227, identified, firewall-clean | done | **[V] SCORED** |
| **DM/(B) sign-law — `+` arm** | ✅ **DONE (FV8, v0.18.0)** — scored predicted **corrective SIGN** (LOF→`+` restore) vs HELD-OUT Horlbeck 2016 CRISPRa suppressor activation: point-biserial = +0.4852, exact p = 0.0274, identified, firewall-clean — completes the bidirectional test | done | **[V] SCORED** |

> Note (v0.15.0 result, test FV6 — corrects the v0.12.0 note): the **(B) frontier partitions**. The **γ-ordering** axis is **non-identified** — γ tracks promoter GC by construction (ρ(γ,GC)=0.9944 on the disease panel, R²=0.9948), so an ordering/knockdown-depth score cannot separate γ from the GC/accessibility confound; that class needs a response-magnitude readout (firewalled Δh) and should not be re-run. But the **corrective sign-law** is **orthogonal** to GC (point-biserial(sign,GC)=+0.0153, R²=0.0002 — a ≈4974× separation vs the γ↔GC axis) and reads only WHICH sign corrects, so it is **identified AND firewall-clean**: its only obstacle is **bidirectional disease-correction DATA**, *not* Δh. This corrects the earlier "all (B) crossings need Δh" framing. See FV6 and IRREPRODUCIBILITY_LEDGER "(B) validation".
>
> Note (v0.17.0 result, test FV7): the sign-law's **`−` arm is now SCORED** on a genuinely held-out target (DepMap 24Q2 CRISPR-KO gene-effect). A knockout screen *is* the `−` operation; in a cancer line viability is a correction phenotype, so GOF oncogenes (`corr_sign −`) should be dependencies and LOF suppressors (`corr_sign +`) should not. On the onco panel (n=16): **point-biserial(GOF, −gene_effect) = +0.4940, exact one-sided p = 0.0227** (predicted direction; per-gene 12/16, GOF 7/7). It is the **identified** axis FV6 named — re-checked live: **point-biserial(sign,GC) = −0.1222**, GOF/LOF mean GC **0.532/0.543** (balanced), **GC-partialled point-biserial = +0.4939** (unchanged) — so the match cannot be a GC artifact — and **firewall-clean** (sign only). It is the kit's **first held-out POSITIVE** and confirms the substrate's mechanism sign-law is biologically faithful on independent dependency data; it is **not** a fresh discovery of the oncogene/suppressor split (those are the kit's frozen priors). It promotes the `−` arm `[V]`; **O-22 stays `[O]`** with its obstacle **narrowed to the `+` RESTORE arm alone** (FV7 does not reintroduce Δh); **O-21** stays `[O]` (absolute dose). The site §15-extension is deferred (research-first); see HANDOVER §0.
>
> Note (v0.18.0 result, test FV8 — the MIRROR of FV7, and a CORRECTION of its framing): the sign-law's **`+` RESTORE arm is now SCORED** on a genuinely held-out target of the **opposite operation** (Horlbeck 2016 hCRISPRa-v2 K562 growth). A CRISPR-**activation** screen *is* the `+` operation; in a cancer line growth is a correction phenotype, so LOF suppressors (`corr_sign +`) should be growth-suppressive on activation and GOF oncogenes (`corr_sign −`) should not. On the onco panel (n=16): **point-biserial(LOF, −growth_phenotype) = +0.4852, exact one-sided p = 0.0274** (predicted direction; per-gene 10/16, LOF 7/9), nearly symmetric to FV7's `−` arm. It is the **identified** axis — re-checked live: **point-biserial(sign,GC) = +0.1222**, LOF/GOF mean GC **0.5426/0.5320** (balanced), **GC-partialled point-biserial = +0.4731** (unchanged) — and **firewall-clean** (sign only). It is the kit's **second held-out POSITIVE**; together with FV7 the corrective sign-law is now **bidirectionally `[V]`**, which **removes in full** the bidirectional-DATA obstacle FV6 named. **But O-22 STILL stays `[O]`**: FV8 **corrects** FV7's "narrows to the `+` arm alone" framing — with both arms scored, O-22's residual obstacle is **no longer DATA but the firewall itself**. The sign-law is class-level + direction-only (*which way* to push each class); O-22 is a per-patient absolute outcome needing the firewalled per-patient magnitude/penetrance (absolute drive size = **O-21**). A direction-only law cannot deliver a per-patient yes/no, and promoting O-22 would leak direction-only `[V]` into per-patient absolute `[V]`. This is **not** a contradiction of FV6 (the sign-law needed bidirectional data, not Δh; both arms scored with zero Δh). K562 is a single CML line, and TP53-null/CDKN2A-deleted push AGAINST the prediction (conservative, no cherry-picking). The site §15-extension is deferred (research-first); see HANDOVER §0 and IRREPRODUCIBILITY_LEDGER "(B) validation".

## PERMANENTLY OUT OF SCOPE (firewalled [O] — see IRREPRODUCIBILITY_LEDGER.md)
Absolute inherited phenotype magnitude · absolute payload→phenotype dose · absolute vaccine titre /
correlate of protection · absolute wild generation-count · clinical efficacy/safety. Handed to
clinicians and regulators. These are not "future work"; the substrate does not fix them.
