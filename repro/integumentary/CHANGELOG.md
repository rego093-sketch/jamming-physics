# CHANGELOG

## v1.0.0 — in-lane program complete: consolidation + release-readiness audit + four-document SSOT (label-only over v0.9.0 computation; no new mechanism, no new constant)

**This is the 0.x → 1.0 transition.** With every in-lane (jamming barrier/interface + external-insult)
mechanism delivered through v0.9.0 — ten targets (T1–T9 + oncology), twenty-three diseases, and the
cross-package seam manifest — and the in-package, harness-free roadmap explicitly exhausted (v0.9.0 was
"the one remaining in-package, harness-free next step"), this release **consolidates and certifies** the
program rather than extending it. It adds **no new mechanism, no new constant, no new γ, and no new
disease**. What remains genuinely future is the *live wiring* of the DECLARED-OUT cross-package contracts,
which needs an integration harness that does not exist in this self-contained package (recorded, not faked).

**Added one additive, read-only artifact:**
- `repro/run_release_audit.py` — a top-level **release-readiness consolidation gate**. It re-runs every
  canonical runner (`run_all`, `run_pathology`, `run_cycle`, `run_seb`, `run_adhesion`, `run_vasomotor`,
  `run_seam`) in its own subprocess, reads the determinism sha each one emits, and **asserts it equals the
  value pinned in `START_HERE` / `HANDOFF`**, then asserts each layer reports its pass/all-green token, and
  writes the machine-readable `reports/release_audit.json` (`all_frozen_hashes_match`, `all_gates_green`,
  `all_ok`, plus the 10-target / 23-disease / 3-1-6-seam coverage record). It imports nothing from the
  engine or the gates and computes no physics, so the seven frozen hashes are an **input contract** here —
  checked, never produced. Verdict on this release: **all 7/7 hashes match, all gates green, RELEASE-READY**.

**Verified the cited `[L]` anchors against current literature (network) — `ANCHORS_VERIFIED.md`:**
- **T4 epidermal turnover** — the CHARTER `TO-ANCHOR` flag is **cleared**: stratum-corneum transit
  ~14–20 d; whole-epidermis turnover ~28–48 d (classic Weinstein-class), extending to ~56 d in newer
  density-based estimates; the widely-quoted "28-day" figure is a lower-bound simplification. The model's
  modelled ~28 d total sits at the **conservative lower edge** of the literature — stated, not tuned; the
  `[V]` dwell-cascade structure is unchanged, the absolute total stays `[O]`.
- **Oncology dichotomy** — confirmed: **melanoma** ← intermittent/recreational + sunburn (Gandini SRR
  ~1.6), chronic/occupational **inverse** (the "tan paradox"); **SCC** ← cumulative UV, near-linear
  (occupational pooled OR ~1.77). Matches the model's `[V]` shapes. (Refinement recorded: BCC is more
  intermittent-like than SCC; a future SCC/BCC split could place BCC nearer the melanoma pole.)
- **Pigment-loss → oncology (the INTERNAL-LIVE seam)** — OCA → SCC confirmed (SCC dominant, ≈75–88 % of
  albino skin cancers; up to ~1000× risk in sub-Saharan-African albinos; sunscreen the preventive/causal
  lever). **Honesty flag (master map §6.3):** the seam's **"melanoma burst RR ≈10.59×" is a property of
  the shared oncology kernel** (screen removed → burst-sensitivity of the multistage rate rises), **not** a
  claim that albinos have ~10.6× the melanoma incidence — OCA melanoma is clinically **rare** because OCA
  removes the melanocytic substrate. The two are **consistent** (different axes), and the package already
  grades the burst RR `[O]`, never as a cited incidence. No computation changed.

**Wrote the four-document SSOT (governance):**
- `MASTER_MANUAL.md` — consolidated operating reference (architecture, reproduce commands, grading system,
  the mechanism-first no-tuning extension recipe, the physical-class boundary, the writing-phase clauses,
  the governance invariants).
- `COMPLETION_LEDGER.md` — the SSOT for *what is done*: the 10 targets, the 23 diseases (with handles and
  grades), the seam manifest's three classes, the seven frozen hashes, the verified anchors, and the
  honest open items.
- `HANDOVER.md` — the v1.0.0 session-to-session handover (state, what changed, the frozen-hash contract,
  what the next session can and cannot do).
- `CHANGELOG.md` — this entry.
- (plus `ANCHORS_VERIFIED.md`, the anchor-verification record.)

**Version label bumped to 1.0.0; HTML re-stamped.** `VERSION` → 1.0.0; `build_docs.py` `BUILD_DATE` →
2026-06-19; `tools/build_docs.py` re-run (writing gate green). The **only** change to the fourteen existing
HTML sections + hub is the version/date label (in the footer and the JSON-LD `version`/`datePublished`/
`dateModified` fields) — verified by a full before/after diff. `_meta.json`, `sitemap.xml`, `robots.txt`
and `llms.txt` refreshed to 1.0.0.

**Invariant preserved — the seven determinism hashes are byte-identical to v0.9.0:** core
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92`, pathology `0a4404ccde65…`, hair-cycle
`d910fa5d2854…`, sebaceous `1e8a557d9a8d…`, adhesion `55dce8c267ea…`, vasomotor `53a99f522ad6…`, seam
`52b49a95a9ad…`. `research all_green` remains true; `_to_measure` remains empty; no constant fitted. The
release is additive (one read-only audit script) + governance + a label bump, and nothing else.


## v0.9.0 — cross-package seam manifest: the pigment-loss→oncology coupling exposed as a labelled output + the inherited/declared seam record (additive, no new mechanism, no new constant)

**Executed HANDOFF §5.3 (the one remaining in-package, harness-free next step).** With the in-lane disease
mechanisms all delivered through v0.8.0 (§5.2 complete), the next step the package's own roadmap points to is
§5.3's doable bullet: *"the pigment-loss → oncology link (vitiligo/albinism lesion → melanoma burst
sensitivity) is already internal here; expose it as a labelled seam output for the 'one body' runner."* This
release does exactly that and nothing more — it adds **no new mechanism and no new constant**; it consolidates
every interface the package has into one labelled, machine-readable **seam manifest** for the one-body runner.

**New additive layer `repro/_seam/`** (mirrors the additive-layer pattern — its own research-first
determinism hash, the core and every disease layer left frozen):

- `seam_manifest.py` — assembles the manifest in three honestly distinct classes. **(A) INHERITED-IN** (3):
  read-only inputs the package vendors from a sibling and never re-derives — circulatory dermal-perfusion
  *magnitude* (cited, consumed by T9), DNA organ identity + emergence order + measured γ `[V]`, the R19
  substrate primitive. **(B) INTERNAL-LIVE** (1, the §5.3 headline): the **pigment-loss → oncology** coupling
  — a melanocyte-target (T3) lesion that removes the melanin screen raises the shared oncology-kernel hazard.
  The numbers are **re-exported verbatim** from the verified pathology layer (`skin_pathology.albinism`,
  `skin_cancer`, `vitiligo`), so the seam output provably *is* the internal link surfaced, not a parallel
  implementation: an albinism-type screen-loss raises the SCC cumulative-hazard RR to ≈ **2.58×** (incidence
  RR ≈ 2.24×) and the melanoma **burst** RR to ≈ **10.59×**, while an exogenous sunscreen lowers the SCC
  hazard RR back to ≈ **1.13×** — the screen is the **causal lever**, not a correlate. **(C) DECLARED-OUT**
  (6): contracts to sibling packages, flagged honestly as **DECLARED, not yet live wiring** (the integration
  harness of §5.3/§5.4 does not exist), each carrying its in-package dynamics-side back-pointer (master map
  §6.2): gene-lesion → `disease_wp` (the §3 genodermatosis list), immune/rheumatology seams (urticaria,
  lichen planus, secondary-Raynaud fixed ischemia, rosacea inflammatory chemistry beyond the LL-37/Demodex
  flag), and out-of-class cutaneous infections.
- `seam_verify.py` — `run_battery`, `determinism_ok`, and `seam_gate()` (the layer's own gate). Four
  fidelity/honesty checks rather than a physical sweep: **(A) re-export fidelity** — every internal value
  equals the pathology layer's own return value field-by-field (what makes "expose the already-internal link"
  truthful); **(B) coupling sign + causal lever** — every exposed RR > 1 and the sunscreen intervention RR is
  lower; **(C) provenance + contract validity** — every internal number traces to a named pathology field (no
  orphan constant) and every declared-out seam is validly targeted or explicitly out-of-class; **(D)
  non-disturbance** — the pathology layer's own 2×sha256 hash is unchanged after the seam runs (the seam reads
  it, it does not perturb it; the core battery is never imported here).
- `run_seam.py` — runner, writes `reports/seam_manifest.json` (the machine-readable seam record) and
  `reports/seam_results.json` (the gate record).
- `README.md` — layer documentation.

**Doc section §14 (writing phase, gate green).** `docs/14-cross-package-seams/index.html` is generated by
`tools/build_docs.py` to VP-SPEC C4 — answer-first `<p class="answer">` (64 words), JSON-LD
(`ScholarlyArticle` + `BreadcrumbList`), `canonical`, a claim-strip (grade + reproduce link + DOI
placeholder), and four vp-cards. It is registered in `docs/_meta.json` `sections[]`; the hub, `sitemap.xml`,
`robots.txt` and `llms.txt` are refreshed; and the per-page HTML version label is bumped to 0.9.0 across all
fourteen sections (the only change to the existing thirteen pages, plus §13 gaining a "next →" link to §14).
`build_docs.py` is neither the engine nor the gates, so extending it to render the new section is within the
CHARTER invariant.

**Seam manifest determinism:** `52b49a95a9add070a05a02848b1a4cef0589f4a36791167232fda3fc1c1d58f7`
(identical across independent processes).

**Invariant preserved:** the addition is purely additive. The seam layer **reads** the disease layers and
never alters them, and it never imports the core battery, so the core T1–T5+oncology determinism hash
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` is unchanged, `research all_green` remains
true, and every disease-layer hash is unchanged (pathology `0a4404…`, hair-cycle `d910fa…`, sebaceous
`1e8a55…`, adhesion `55dce8…`, vasomotor `53a99f…`). No new γ is fetched and no constant is fitted.

## v0.8.0 — neurovascular reactivity: a hysteretic vasomotor-jam target on the existing measured γ + rosacea & Raynaud phenomenon (additive, mechanism-first)

**Added a new target ahead of its diseases, on an organ already in the atlas** (HANDOFF §5.2, mechanism-first
expansion; HANDOFF §4 "Rosacea … needs a neurovascular / inflammatory module … Missing mechanism (dermal
perfusion is an inherited citation, not a dynamics target here)"): **neurovascular reactivity (target T9)**.
The cutaneous thermoregulatory interface has **two autonomic effector arms** — the **sudomotor** arm (sweat
glands, the T5 target and the hyperhidrosis/HED diseases) and the **vasomotor** arm (skin blood flow,
flushing). Rosacea is a dysregulation of the **vasomotor arm** — the **vascular mirror of hyperhidrosis** on
the sudomotor arm — so vasomotor reactivity is an **intrinsic property of the thermoregulation-interface
organ**. This is the **hair-cycle / adhesion pattern** (a new *target* on an *existing* organ), **not** the
sebaceous pattern (a new measured organ). It runs on the **already-measured EDAR γ = 1.3696**, with **no new
γ fetched and none fitted** (`new_gamma_fetched = false`). A vessel is read as a member of the package's
**jamming** class the natural way round: **dilated = jammed ON** (s>0, flushed), **constricted = OFF** (s<0,
quiescent/ischemic).

**Seam not crossed (SSOT).** The dermal-**perfusion magnitude** stays an **inherited circulatory citation**
(CHARTER *"Seams IN: circulatory dermal perfusion (cited)"*) and is **not re-emerged**. This target adds
**only the vasomotor reactivity dynamics** the §4 note says is missing — a reactivity threshold and a
hysteretic fixation. The fixed digital-ischemia / ulcer state of **secondary Raynaud** (connective-tissue
disease) and the rosacea inflammatory effector chemistry beyond the LL-37/Demodex amplifier flag are
**immune/rheumatology sibling-package seams**, named not modeled.

**New additive layer `repro/_vasomotor/`** (mirrors the `repro/_cycle/` / `repro/_adhesion/` pattern — a new
target on an existing γ — with its own research-first determinism hash, so the core stays frozen):

- `vasomotor_switch.py` — the **hysteretic two-lock reactivity jam** (`vasomotor_hysteresis`) on the *shared
  R19 switch* (`vp_substrate` + `skn_dynamics`, the same machinery as T1/T2), the signed net-drive model
  (`net_vasodilator` = resting tone + reactivity − constrictor), the state/excursion continuations
  (`_state_outcome`/`_excursion_returns`/`_fix_then`/`_constrict_from_fixed`), the **lock rule** that makes
  reversibility a uniform consequence of *whether a drive crosses its spinodal*, two diseases, and
  `vasomotor_summary()`. The vessel **locks dilated discontinuously** at the upper spinodal (up-jump ≈ 2.03
  at net drive ≈ +1.005) and **locks constricted discontinuously** at the lower spinodal (≈ −1.005), tracing
  a **hysteresis loop of width ≈ 2.01** — both **[V]**; the healthy vessel sits **responsive in the
  reversible middle** at net drive −0.3. Honest no-tuning grade: the resting tone, reactivity gains and
  trigger/constrictor drives are dimensionless regime scales **[F]**; the clinical mappings are cited anchors
  **[L]**; the *absolute* erythema index, vessel density, flush magnitude, digital temperature, attack
  frequency and involved body-surface area are **[O]** (a per-vessel calibration, and the perfusion magnitude
  is an inherited circulatory seam — the vasomotor target's obstacle).
- `vasomotor_verify.py` — `run_battery`, `determinism_ok`, and `vasomotor_gate()` (the layer's own gate;
  checks mechanism + both diseases + the discriminant + that γ is the existing measured value; does **not**
  touch `repro/_verify/gates.py`).
- `run_vasomotor.py` — runner, writes `reports/vasomotor_results.json`.
- `README.md` — layer documentation.

**Two vasomotor diseases** unlocked, each a signed vasomotor drive on the one switch (intervention = the
drive reversed; **no new constant**): **rosacea** (a standing vasodilator reactivity drive — a lowered flush
threshold under heat/alcohol/ultraviolet/spice — carries the net dilator drive past the upper spinodal so the
vessel **locks dilated** into persistent erythema and fixed telangiectasia; an early transient flush is a
sub-lock excursion that still **returns**, and only crossing the lock fixes the vessel; the LL-37/Demodex
inflammatory amplifier on the same dilated background gives the **papulopustular** subtype; anti-inflammatory
therapy clears the papules, an α-agonist (brimonidine) blanches transiently but does **not** reset the fixed
vessels — the hysteresis — and only **laser/IPL** physically resets the telangiectasia), and **Raynaud
phenomenon** (a cold/stress vasoconstrictor drive carries the net dilator drive negative into the
constricted/ischemic basin → the white-blue-red digital attack; **primary** Raynaud is a reversible excursion
that crosses **no** lock, so it reverses on rewarming and a vasodilator / calcium-channel blocker aborts it;
the **fixed** digital-ischemia/ulcer state of **secondary** Raynaud with connective-tissue disease is named
as a seam, not modeled). Both pass a clinical-sign + intervention-reversal battery and a **three-axis
opposite-property discriminant** (vasodilation ↔ vasoconstriction; fixed telangiectasia ↔ reversible
vasospasm, by the lock rule; vascular erythematotelangiectatic ↔ inflammatory papulopustular) — all
reproduced **from the drive sign and the lock rule alone, on the one reused EDAR γ**.

**Disease-home boundary (stated, not crossed):** primary Raynaud's reversible vasospasm is keyed by
*dynamics* (a reversible vasoconstrictor excursion) and is built here; the **fixed** digital ischemia of
secondary Raynaud is a downstream structural change of connective-tissue disease (an immune/rheumatology
seam), and the dermal-perfusion magnitude is an inherited circulatory seam — neither is re-emerged here.

**Published** as canonical HTML **`docs/13-neurovascular-reactivity-rosacea/`** (VP-SPEC C4: answer-first
block, JSON-LD `ScholarlyArticle` + `BreadcrumbList`, canonical, claim-strip, one vp-card per cited `[L]`
anchor + a determinism card; **English** body C0; every `[O]` names the vasomotor obstacle C3). The layer's
own 2×sha256 determinism hash
`53a99f522ad684a11bcc6d4d33c5e8123d1f4dff5a75836c0bbced6736a62003` is emitted in the page.

**Generator change (writing phase only):** `tools/build_docs.py` imports `repro/_vasomotor`
(`vasomotor_switch.vasomotor_summary` / `_emit`) in `gather()` so every displayed number mirrors the engine
(C1), and emits section 13. No engine, oncology, pathology, cycle, sebaceous, adhesion, or gate file was
touched.

**No atlas change:** because vasomotor reactivity reuses the existing EDAR γ, `inherited/organ_gamma.json` is
**unchanged** and no new organ is introduced — the contrast with v0.6.0, which promoted a new measured organ
(PRDM1); the parallel with v0.5.0 (hair-cycle) and v0.7.0 (adhesion), which added new targets on existing γ.

**Invariant preserved:** purely additive. The core target battery (`repro/run_all.py`) and all gate files
are untouched — its determinism hash
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` is **unchanged**, `research all_green`
remains true — and the pathology battery (`repro/run_pathology.py`, hash
`0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8`), the hair-cycle battery
(`repro/run_cycle.py`, hash `d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822`), the
sebaceous battery (`repro/run_seb.py`, hash
`1e8a557d9a8d7b05823259bb2fcac31e372b96272e47ef1f2f5d89b1b0246a84`) and the cell-adhesion battery
(`repro/run_adhesion.py`, hash `55dce8c267ea4c76d8d5b967535a4ee0876c4b67f605e6ae7d65bf38516f28ad`) all still
pass with their hashes unchanged. Disease count is now 13 (pathology) + 4 (cycle) + 2 (sebaceous) + 2
(adhesion) + 2 (vasomotor). Organ count is **still 5** (TP63, KRT14, MITF, EDAR, PRDM1) — vasomotor adds no
organ. `docs/_meta.json` lists 13 sections; `sitemap.xml` / `llms.txt` include the new section; the per-page
version label tracks 0.8.0.

## v0.7.0 — cell adhesion: a hysteretic binding-jam target on the existing measured γ + pemphigus vulgaris & bullous pemphigoid (additive, mechanism-first)

**Added a new target ahead of its diseases, on an organ already in the atlas** (HANDOFF §5.2, mechanism-first
expansion; HANDOFF §4 "Autoimmune bullous … needs a cell-adhesion target"): **cell adhesion (target T8)**.
Desmosomes and hemidesmosomes anchor the keratinocyte's keratin network, so junctional adhesion is an
**intrinsic property of the keratinocyte** — this is the **hair-cycle pattern** (a new *target* on an
*existing* organ), **not** the sebaceous pattern (a new measured organ). It runs on the **already-measured
KRT14 γ = 1.4894**, with **no new γ fetched and none fitted** (`new_gamma_fetched = false`). A bond is read
as a member of the package's **jamming** class the natural way round: **adherent = jammed ON** (s>0),
**blistered = unjammed OFF** (s<0).

**New additive layer `repro/_adhesion/`** (mirrors the `repro/_cycle/` pattern — a new target on an existing
γ — with its own research-first determinism hash, so the core stays frozen):

- `adhesion_switch.py` — the **hysteretic two-state binding jam** (`adhesion_hysteresis`) on the *shared R19
  switch* (`vp_substrate` + `skn_dynamics`, the same machinery as T1/T2), the net-adhesion model
  (`net_adhesion` = reserve − autoantibody), a **two-compartment** continuation on the *same γ and the same
  spinodal* — cell-cell (desmosomal, DSG3) and cell-matrix (hemidesmosomal, BP180/COL17A1) — the
  outcome/continuation helpers (`_compartment_outcome`/`_separate_then`/`_treat_from`), a **derived** Nikolsky
  rule (`_nikolsky_positive`: positive iff the cell-cell bond failed and the cell-matrix bond held), two
  diseases, and `adhesion_summary()`. The bond **detaches discontinuously** at the lower spinodal (down-jump
  ≈ 2.11 at net adhesion ≈ −1.005) and **re-adheres only at a higher spinodal** (≈ +1.005), tracing a
  **hysteresis loop of width ≈ 2.01** — both **[V]**; the healthy bond sits **adherent above the upper
  spinodal** at net adhesion +1.4. Honest no-tuning grade: the adhesion reserve and antibody titres are
  dimensionless regime scales **[F]**; the clinical mappings are cited anchors **[L]**; the *absolute* blister
  counts, antibody titre (IU/mL), cleavage depth (µm) and involved body-surface area are **[O]** (a
  per-junction calibration, the adhesion target's obstacle).
- `adhesion_verify.py` — `run_battery`, `determinism_ok`, and `adhesion_gate()` (the layer's own gate;
  checks mechanism + both diseases + the discriminant + that γ is the existing measured value; does **not**
  touch `repro/_verify/gates.py`).
- `run_adhesion.py` — runner, writes `reports/adhesion_results.json`.
- `README.md` — layer documentation.

**Two autoimmune bullous diseases** unlocked, each a signed de-adhesion of the one bond (intervention = the
antibody cleared; **no new constant**): **pemphigus vulgaris** (an anti-DSG3 autoantibody drives the
*cell-cell* compartment below the spinodal → an **intraepidermal/suprabasal** split with the cell-matrix bond
intact (basal "tombstone" row); because the failing bond *is* the lateral one, a tangential shear propagates
→ **Nikolsky positive**, and the thin roof gives a **flaccid** blister; a partial titre reduction does not
re-adhere, clearance (rituximab/immunosuppression) does), and **bullous pemphigoid** (an anti-BP180 antibody
of the **same magnitude** instead drives the *cell-matrix* compartment below the spinodal → a **subepidermal**
split with the cell-cell bonds intact (epidermis lifts whole); the failing bond is basal, not lateral, so
shear does not propagate → **Nikolsky negative**, and the full-thickness roof gives a **tense** blister;
corticosteroid/immunosuppression re-adheres it). The **Nikolsky sign is derived** from which compartment
failed, not asserted. Both pass a clinical-sign + intervention-reversal battery and a **three-axis
opposite-property discriminant** (intraepidermal ↔ subepidermal plane; positive ↔ negative Nikolsky; flaccid
↔ tense blister) — all reproduced **from the compartment alone, at the same antibody magnitude**.

**Disease-home boundary (stated, not crossed):** acquired autoimmune blistering is keyed by *dynamics* (a
de-adhesive drive on an intact bond) and is built here; its congenital mirror **epidermolysis bullosa** is
keyed by a *defective adhesion gene* (KRT14/COL17A1/LAMB3) and belongs to the gene-lesion disease registry,
not to this dynamical layer.

**Published** as canonical HTML **`docs/12-cell-adhesion-blistering/`** (VP-SPEC C4: answer-first 60-word
block, JSON-LD `ScholarlyArticle` + `BreadcrumbList`, canonical, claim-strip, one vp-card per cited `[L]`
anchor + a determinism card; **English** body C0; every `[O]` names the adhesion obstacle C3). The layer's
own 2×sha256 determinism hash
`55dce8c267ea4c76d8d5b967535a4ee0876c4b67f605e6ae7d65bf38516f28ad` is emitted in the page.

**Generator change (writing phase only):** `tools/build_docs.py` imports `repro/_adhesion`
(`adhesion_switch.adhesion_summary` / `_emit`) in `gather()` so every displayed number mirrors the engine
(C1), and emits section 12. No engine, oncology, pathology, cycle, sebaceous, or gate file was touched.

**No atlas change:** because adhesion reuses the existing KRT14 γ, `inherited/organ_gamma.json` is
**unchanged** and no new organ is introduced — the contrast with v0.6.0, which promoted a new measured organ
(PRDM1).

**Invariant preserved:** purely additive. The core target battery (`repro/run_all.py`) and all gate files
are untouched — its determinism hash
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` is **unchanged**, `research all_green`
remains true — and the pathology battery (`repro/run_pathology.py`, hash
`0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8`), the hair-cycle battery
(`repro/run_cycle.py`, hash `d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822`) and the
sebaceous battery (`repro/run_seb.py`, hash
`1e8a557d9a8d7b05823259bb2fcac31e372b96272e47ef1f2f5d89b1b0246a84`) all still pass with their hashes
unchanged. Disease count is now 13 (pathology) + 4 (cycle) + 2 (sebaceous) + 2 (adhesion). Organ count is
**still 5** (TP63, KRT14, MITF, EDAR, PRDM1) — adhesion adds no organ. `docs/_meta.json` lists 12 sections;
`sitemap.xml` / `llms.txt` include the new section; the per-page version label tracks 0.7.0.

## v0.6.0 — sebaceous duct: a new measured organ + a hysteretic occlusion-jam target + acne & hidradenitis suppurativa (additive, mechanism-first)

**Added a new organ on a newly measured γ, ahead of its diseases** (HANDOFF §5.2, mechanism-first
expansion): the **sebaceous gland / pilosebaceous duct**, the textbook member of the package's own
**jamming** class the earlier targets did not cover. Unlike the hair-cycle layer (a new *target* on an
*existing* organ), this is a **new organ** — its master gene **PRDM1/Blimp1** (the committed
sebaceous-lineage master; Horsley et al., *Cell* 2006) was promoted **`to_measure → fetched → vendored`**
exactly as MITF/EDAR were: **γ = 1.3432** is the proximal-promoter nearest-neighbour ΔG37 (SantaLucia 1998)
over the cached NCBI window TSS−2000..+500, computed with the **same pipeline validated to reproduce MITF
and EDAR byte-for-byte**, cached so it reproduces **offline bit-for-bit** (`gamma_from_cached_sequence` =
1.343156; `seq_sha256 = b27d035762375a71…`). The master gene was committed on the biology **before**
reading γ; PRDM1 then turns out to carry the **lowest γ in the whole organ atlas**, so its functional
spinodal opens **earliest** — an honest **emergence-order prediction graded by sign [V]**, not a fit.

**New additive layer `repro/_seb/`** (mirrors the `repro/_cycle/` pattern; its own research-first lock and
its own determinism hash, so the core stays frozen):

- `sebaceous_duct.py` — the **hysteretic two-state occlusion jam** (`jamming_hysteresis`) on the *shared
  R19 switch* (`vp_substrate` + `skn_dynamics`, the same machinery as T1/T2), the net-occlusion model
  (`net_occlusion` = sebum + keratinisation + *C. acnes* − clearance), the duct-outcome continuation
  (`_duct_outcome`/`_form_then`/`_treat_from`), two diseases, and `sebaceous_summary()`. The duct **snaps
  shut discontinuously** at the upper spinodal (up-jump ≈ 2.01 at net occlusion ≈ 1.005) and **reopens only
  at a lower spinodal** (≈ −1.005), tracing a **hysteresis loop of width ≈ 2.01** — both **[V]**; the
  healthy duct sits **patent** at net occlusion −0.3. Honest no-tuning grade: the occlusion set-points are
  dimensionless regime scales **[F]**; the *absolute* comedo/lesion counts, Hurley-stage extent and sebum
  excretion rate are **[O]** (a per-gland calibration, the new sebaceous target's obstacle).
- `seb_verify.py` — `run_battery`, `determinism_ok`, a **γ-offline-provenance check**, and `seb_gate()`
  (the layer's own gate; does **not** touch `repro/_verify/gates.py`).
- `run_seb.py` — runner, writes `reports/seb_results.json`.
- `README.md` — layer documentation.

**Two occlusion diseases** unlocked, each a signed perturbation of the one jam (intervention = the drive
reversed; **no new constant**): **acne vulgaris** (a standing high occlusion drive ≈ 1.10 pushes the duct
past the upper spinodal into an *inflammatory* comedo; retinoid monotherapy is insufficient — the duct must
be driven below the *lower* spinodal — but a combined comedolytic + sebostatic + antimicrobial regimen /
isotretinoin reopens it; de-inflaming alone leaves a comedonal-but-jammed residue), and **hidradenitis
suppurativa** (the same jam in deeper apocrine-bearing follicles, drive ≈ 1.50, where the plug **ruptures**
into the dermis → a chronic scarring **sinus-tract** sub-state acne lacks; dropping the drive to the same
sub-acne level that *clears* acne still leaves the ruptured tract, so anti-inflammatory biologics calm
activity but only **deroofing/excision** resets the scar). Both pass a clinical-sign + intervention-reversal
battery and a **three-way opposite-mode discriminant** (reversible superficial ↔ irreversible deep rupture;
inflammatory ↔ comedonal on the *C. acnes* amplifier; lighter ↔ heavier plug) — all reproduced.

**Published** as canonical HTML **`docs/11-sebaceous-duct-jamming-acne/`** (VP-SPEC C4: answer-first 54-word
block, JSON-LD `ScholarlyArticle` + `BreadcrumbList`, canonical, claim-strip, one vp-card per cited `[L]`
anchor + a determinism card; **English** body C0; every `[O]` names the sebaceous obstacle C3). The layer's
own 2×sha256 determinism hash
`1e8a557d9a8d7b05823259bb2fcac31e372b96272e47ef1f2f5d89b1b0246a84` is emitted in the page.

**Generator change (writing phase only):** `tools/build_docs.py` imports `repro/_seb`
(`sebaceous_duct.sebaceous_summary` / `_emit`) in `gather()` so every displayed number mirrors the engine
(C1), and emits section 11. No engine, oncology, pathology, cycle, or gate file was touched.

**Atlas change (inert to core):** `inherited/organ_gamma.json` gains PRDM1 as a vendored measured organ
(`_organ = sebaceous_gland`, γ = 1.3432) and `inherited/organ_promoters.cache.json` carries its cached
promoter + the SantaLucia NN table; `inherited/organ_identity.md` documents the row. The core engine's
`ORGAN_ROWS` does **not** reference PRDM1, so the atlas addition is **inert** to the core battery.

**Invariant preserved:** purely additive. The core target battery (`repro/run_all.py`) and all gate files
are untouched — its determinism hash
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` is **unchanged**, `research all_green`
remains true — and both the pathology battery (`repro/run_pathology.py`, hash
`0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8`) and the hair-cycle battery
(`repro/run_cycle.py`, hash `d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822`) still pass
with their hashes unchanged. Disease count is now 13 (pathology) + 4 (cycle) + 2 (sebaceous). Organ count
is now 5 (TP63, KRT14, MITF, EDAR + PRDM1). `docs/_meta.json` lists 11 sections; `sitemap.xml` / `llms.txt`
include the new section; the per-page version label tracks 0.6.0.

## v0.5.0 — hair-follicle cycle: a new emergent oscillator target + four alopecias (additive, mechanism-first)

**Added a new verified target ahead of its diseases** (HANDOFF §5.2, mechanism-first expansion): the
**hair-follicle cycle**, the one integumentary structure that cycles autonomously, modelled as an
emergent **relaxation oscillator** on the *existing measured* EDAR γ = 1.3696 using the *already-vendored*
FHN relaxation element (`inherited/vp_substrate.Neuron`, the same one the T5 thermoregulation page uses).
This closes the gap the core battery itself reports — no autonomous oscillator anywhere in the
integumentary class — with **no new organ and no new fitted constant**. The follicle organ (`skin_appendage`)
and its γ already existed; only the *cycling dynamics* target was missing, and it is now built.

**New additive layer `repro/_cycle/`** (mirrors the `repro/_pathology/` pattern; its own research-first
lock and its own determinism hash, so the core stays frozen):

- `hair_cycle.py` — the oscillator (`cycle_metrics`, `anagen_fraction_at`), a deterministic population
  shedding model (`shedding_dichotomy`), four diseases, and `hair_cycle_summary()`. The cycle is
  **anagen-dominant** (anagen fraction ≈ 0.59) with a **plateau-then-collapse relaxation waveform**
  (plateau dominance ≈ 0.87) — both **[V]**. Honest no-tuning grade: the *absolute* anagen fraction
  (cited 85–90 %) and the years-long *period* are **[O]**, not fitted — a constant drive strong enough to
  reach 88 % would cross the Hopf point and kill oscillation, so the substrate is graded by **dominance and
  direction**, not magnitude. Healthy growth bias = ½·spinodal(EDAR), a substrate-scaled regime scale **[F]**.
- `cycle_verify.py` — `run_battery`, `determinism_ok`, and `cycle_gate()` (the layer's own gate; does **not**
  touch `repro/_verify/gates.py`).
- `run_cycle.py` — runner, writes `reports/cycle_results.json`.
- `README.md` — layer documentation.

**Four alopecias** unlocked, each a signed perturbation of the one oscillator (intervention = the drive
reversed; **no new constant**): **androgenetic alopecia** (standing anti-growth drive shortens anagen,
fraction 0.59→0.54→0.49 progressive miniaturisation; minoxidil/anti-androgen → 0.63), **alopecia areata**
(sustained premature-catagen drive collapses anagen to 0.48; regrows to 0.59 on removal — bistable
hysteresis), **telogen effluvium** (a transient stressor synchronises a cohort into telogen; sheds **exactly
one telogen later** — a 365-step lag = (1 − 0.59) of the cycle — then self-limits), and **anagen effluvium**
(a direct cytotoxic insult sheds **immediately**, lag 0, bypassing telogen). All four pass a clinical-sign +
intervention-reversal battery and a **three-way opposite-sign / opposite-timing discriminant**
(anagen-short↔long; shed delayed↔immediate; loss sustained↔self-limited) — all reproduced.

**Published** as canonical HTML **`docs/10-hair-follicle-cycle-anagen-telogen/`** (VP-SPEC C4: answer-first,
JSON-LD `ScholarlyArticle` + `BreadcrumbList`, canonical, claim-strip, one vp-card per cited `[L]` anchor +
a determinism card; **English** body C0; every `[O]` names the appendage obstacle C3). The layer's own
2×sha256 determinism hash
`d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822` is emitted in the page.

**Generator change (writing phase only):** `tools/build_docs.py` imports `repro/_cycle` (`hair_cycle.
hair_cycle_summary` / `_emit`) in `gather()` so every displayed number mirrors the engine (C1), and emits
section 10. No engine, oncology, pathology, or gate file was touched.

**Invariant preserved:** purely additive. The core target battery (`repro/run_all.py`) and all gate files
are untouched — its determinism hash
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` is **unchanged**, `research all_green`
remains true — and the pathology battery (`repro/run_pathology.py`) still passes with its hash
`0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8` unchanged. Disease count is now
13 (pathology layer) + 4 (cycle layer). `docs/_meta.json` lists 10 sections; `sitemap.xml` / `llms.txt`
include the new section; the per-page version label tracks 0.5.0.

## v0.4.0 — pathology promoted to the canonical HTML artifact (additive, writing phase)

**Published** the 13-disease pathology research (added in v0.3.0 as a `reports/`-backed research artifact)
as the canonical per-title HTML section **`docs/09-integumentary-pathology/`**, completing the main
remaining writing step (HANDOFF §5.1). HTML is the canonical artifact (VP-SPEC C2), so this promotes the
disease layer from research record to publication. Built by `tools/build_docs.py` with the writing gate
green (`research all_green=true`, writing unlocked).

The section follows VP-SPEC C4: answer-first `<p class="answer">` (52 words), JSON-LD `ScholarlyArticle` +
`BreadcrumbList`, `canonical`, a claim-strip, and **one vp-card per cited `[L]` clinical anchor** (13 anchor
cards + a determinism card). Body is **English** (C0); every `[O]` magnitude names its parent-target
obstacle (C3); the pathology layer's own 2×sha256 determinism hash
`0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8` is emitted in the page (distinct from
the core-battery hash). Content organisation: a 13-row disease→target map, six mechanism subsections
(T1 barrier; T4 turnover; T2 wound; T3 pigment; T5 thermoregulation; oncology) carrying the deterministic
readouts, the **five-way opposite-sign discriminant** table, and a grades/reproducibility section.

**Generator change (writing phase only):** `tools/build_docs.py` now imports `repro/_pathology`
(`skin_pathology.pathology_summary` / `_emit`) in `gather()` so every displayed disease number mirrors the
engine (C1), and emits section 09. No engine, oncology, or gate file was touched.

**Also refreshed:** the per-page HTML version label, which had been stale at 0.1.0, now tracks the package
version; `docs/_meta.json` lists 9 sections; `sitemap.xml` / `llms.txt` include the new section.

**Invariant preserved:** purely additive. The core target battery (`repro/run_all.py`) and all gate files
are untouched; its determinism hash
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` is unchanged, `research all_green`
remains true, and the pathology battery (`repro/run_pathology.py`) still passes with its hash unchanged.

## v0.3.0 — full in-lane disease coverage (additive)

**Expanded** the pathology module from 8 to **13 diseases**, completing the integumentary package's
**in-lane** set per the framework ownership contract (master map §6: acquired / multifactorial /
dynamics-key, plus the dynamics side of borderline genetic ones). Five diseases added, each a named
perturbation of an existing knob with intervention = the knob reversed; **no new constants**:

- **contact dermatitis** (T1) — ACUTE insult crossing the discontinuous barrier collapse (the acute
  complement to atopic dermatitis's chronic reserve erosion); TEWL jumps ×20 at insult ≈ spinodal, active
  barrier repair re-crosses → 1.0.
- **melasma / hyperpigmentation** (T3) — regulated melanin OVERSHOOT (×3.1 baseline) from a standing
  pro-melanogenic drive; the opposite-sign pole to vitiligo on the same MITF switch; depigmenting → baseline.
- **primary hyperhidrosis** (T5) — sweat recruitment threshold LOWERED (sweats at rest); the opposite-sign
  pole to HED on the same EDAR switch; threshold-raising therapy → dry.
- **heat stroke** (T5) — evaporative capacity EXCEEDED → core-temperature runaway (slope ×0.77 → ×2.0 past
  saturation load 2.55); rapid cooling + load reduction → controlled.
- **actinic keratosis** (oncology) — SCC PRECURSOR: fewer multistage hits → far more prevalent than
  invasive SCC (field prevalence 0.96 vs 0.18 at the same UV), low per-lesion conversion; sun protection
  + field treatment → reduced burden.

**Opposite-sign discriminant extended to 5 checks across 3 switches** (was 3): added the **melanin** pair
(melasma overshoot ↔ vitiligo loss) and the **sweat** pair (hyperhidrosis excess ↔ HED deficit), joining
turnover (psoriasis ↔ ichthyosis), barrier (intact ↔ atopic), and photoprotection (tan ↔ pigment loss).
All five reproduced with no new constant.

**Added** `HANDOFF_NEXT_STEPS.md` — the coverage audit (13 covered / out-of-lane → `disease_wp` /
not-yet-modelable, "name it don't hide it") and the explicit next-session instructions (formal docs/09
HTML promotion, mechanism-first expansion rule, cross-package seam wiring).

**Performance:** the pathology module's thermo sweeps now integrate at a coarser, fully-converged
resolution (`_TH_T`/`_TH_DT`) so the determinism re-run stays fast; the engine
(`skn_dynamics.thermo_run`) defaults are untouched.

**Invariant preserved:** purely additive. The core target battery (`repro/run_all.py`) and all gate
files are untouched; its determinism hash
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` is unchanged, `research all_green`
remains true, and the writing gate is not touched (pathology is a research artifact under `reports/`).

## v0.2.0 — pathology module (additive)

**Added** `repro/_pathology/` — the major integumentary diseases simulated **and addressed** on the
package's own internal mechanisms, with **no new constants**:

- `repro/_pathology/skin_pathology.py` — eight diseases, each a named perturbation of one existing
  target knob (T1..T5 / oncology); each intervention is the same knob reversed. Includes the
  `opposite_sign_pairs()` discriminant and `pathology_summary()`.
- `repro/_pathology/pathology_verify.py` — clinical-sign + intervention-reversal battery and the
  determinism check (analogue of `stress_tests.py`).
- `repro/run_pathology.py` — entry point; writes `reports/pathology_results.json`.
- `repro/_pathology/README.md`, `PATHOLOGY_FINDINGS.md` — module doc and research findings.
- `IRREPRODUCIBILITY_LEDGER.md` — extended with the pathology `[O]` rows (each inherits the parent
  target's obstacle; no disease adds a constant).

**Diseases:** atopic dermatitis (T1), ichthyosis (T1+T4), psoriasis (T4), chronic/diabetic/pressure
wound (T2), vitiligo (T3), albinism/OCA (T3→oncology), hypohidrotic ectodermal dysplasia (T5), skin
cancer melanoma/SCC/BCC (oncology). All eight pass clinical-sign + intervention-reversal; the
opposite-sign discriminant (same R19 switch, opposite drives → opposite clinic, no new constant)
holds on all three pairs.

**Honesty fixes during development:** psoriasis reframed from a coarse-sweep single day-count (a
spinodal discretization artifact) to a **threshold + several-fold autonomous acceleration** with the
absolute transit graded `[O]`; atopic dermatitis reframed from an uninformative baseline-TEWL multiple
to the **dimensionless barrier-reserve collapse** as the primary `[V]` signature.

**Invariant preserved:** the additions are purely additive. The core target battery
(`repro/run_all.py`) and all gate files are untouched; its determinism hash
`1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` is unchanged, `research all_green`
remains true, and the writing gate is not touched (pathology is a research artifact under `reports/`).

## v0.1.0 — research baseline

Self-contained integumentary package: substrate (FHN/R19) + VP-SPEC v1.8 + measured master-gene γ
vendored internally; targets T1 (barrier/TEWL), T2 (wound jamming), T3 (melanin/UV), T4 (turnover),
T5 (thermoregulation); oncology UV dose-response kernel; stress battery feeding the research gate.
