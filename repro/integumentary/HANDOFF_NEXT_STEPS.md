# HANDOFF — integumentary disease coverage + next steps

**Package:** `integumentary_vp_site` v0.8.0-research · **author:** Young Jae Lee (ORCID 0009-0002-7535-8245)
**Read order for a new session:** `START_HERE.md` → `CHARTER.md` → this file.
**State is carried by files only** (VP-SPEC §1); a single zip is the unit of handoff.

This file answers one question honestly per the framework's own discipline ("name it, don't hide it",
master map §6.3): **which integumentary diseases are covered, which belong to a sibling package, and
which cannot yet be modeled without a new mechanism.** It then gives the explicit next steps.

---

## 1. Ownership recap (master map §6)

This package owns the **acquired / multifactorial / dynamics-key** skin diseases, and the **dynamics
side** of borderline genetic ones. The **gene-lesion fact** of any single-gene rare genodermatosis is
`disease_wp`'s (gene-key SSOT), imported here by contract (§6.2), not re-derived. The split is by
**etiology class**, not body part: a disease is ours if a *dynamics* mechanism (T1..T5 / oncology
Kramers–multistage) explains it; it is `disease_wp`'s if a *single gene* defines it.

---

## 2. COVERED — 13 + 4 + 2 + 2 + 2 in-lane diseases (mechanism + treatment, all verified)

Each is a named perturbation of one existing knob; each intervention is the same knob reversed; all pass
the clinical-sign + intervention-reversal battery with no new constant (`repro/run_pathology.py`;
findings in `PATHOLOGY_FINDINGS.md`; obstacles in `IRREPRODUCIBILITY_LEDGER.md`).

| # | disease | target | covered as |
|---|---|---|---|
| 1 | atopic dermatitis | T1 | chronic barrier-reserve collapse |
| 2 | contact dermatitis | T1 | acute insult crossing the discontinuous collapse |
| 3 | ichthyosis (dynamics) | T1+T4 | desquamation retention near the spinodal |
| 4 | psoriasis | T4 | differentiation-spinodal threshold + autonomous acceleration |
| 5 | chronic / diabetic / pressure wound | T2 | non-closure below the critical unjamming drive |
| 6 | vitiligo | T3 | discontinuous melanocyte-viability loss |
| 7 | melasma / hyperpigmentation | T3 | regulated melanin overshoot (opposite pole of vitiligo) |
| 8 | albinism / OCA (dynamics) | T3→oncology | melanin screen removed → hazard RR |
| 9 | hypohidrotic ectodermal dysplasia (dynamics) | T5 | capped sweat → danger band at lower load |
| 10 | primary hyperhidrosis | T5 | lowered recruitment threshold (opposite pole of HED) |
| 11 | heat stroke | T5 | capacity exceeded → runaway |
| 12 | skin cancer (melanoma / SCC / BCC) | oncology | intermittent-vs-cumulative dichotomy + pigment-loss burst |
| 13 | actinic keratosis | oncology | SCC precursor (fewer multistage hits) |

Note #3/#8/#9 are covered on their **dynamics side only**; their single-gene forms are §3 below.

**Hair-cycle layer (v0.5.0, `repro/run_cycle.py`, separate hash).** A new emergent **relaxation
oscillator** on the *existing measured* EDAR γ unlocked four more in-lane diseases — each a signed
perturbation of the one cycle, intervention = the drive reversed, no new constant:

| # | disease | cycle handle | covered as |
|---|---|---|---|
| 14 | androgenetic alopecia | anagen duration | standing anti-growth drive shortens anagen → progressive miniaturisation (0.59→0.49); minoxidil/anti-androgen → 0.63 |
| 15 | alopecia areata | premature catagen | sustained immune-type drive collapses anagen (→0.48); regrows on removal (bistable hysteresis) |
| 16 | telogen effluvium | phase synchronisation | a transient stressor synchronises a cohort into telogen; sheds **one telogen later** (365-step lag), self-limited |
| 17 | anagen effluvium | anagen-matrix arrest | a direct cytotoxic insult sheds **immediately** (lag 0), bypassing telogen |

These pass a clinical-sign + intervention-reversal battery and a **three-way opposite-sign / opposite-timing
discriminant**; published as `docs/10-hair-follicle-cycle-anagen-telogen/`; layer hash
`d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822`.

**Sebaceous-duct layer (v0.6.0, `repro/run_seb.py`, separate hash).** A **new measured organ** —
PRDM1/Blimp1 (γ=1.3432, fetched + cached + vendored through the same promoter-ΔG pipeline as MITF/EDAR,
reproduces offline) — run as a **hysteretic two-state occlusion jam** on the *same* R19 switch unlocked two
more in-lane diseases, each a signed perturbation of the one jam, intervention = the drive reversed, no new
constant:

| # | disease | occlusion handle | covered as |
|---|---|---|---|
| 18 | acne vulgaris | standing high occlusion | sebum + hyperkeratinisation + *C. acnes* drive (≈1.10) past the upper spinodal → inflammatory comedo; combined comedolytic + sebostatic + antimicrobial / isotretinoin drives below the lower spinodal → reopens; de-inflame alone leaves a comedonal-but-jammed residue |
| 19 | hidradenitis suppurativa | deep occlusion + rupture | the same jam in deeper apocrine follicles (≈1.50) where the plug **ruptures** → a scarring sinus-tract sub-state; drive-down to the sub-acne level that clears acne leaves the ruptured tract → biologics de-inflame, deroofing/excision resets the scar |

These pass a clinical-sign + intervention-reversal battery and a **three-way opposite-mode discriminant**
(reversible superficial ↔ irreversible deep rupture; inflammatory ↔ comedonal; lighter ↔ heavier plug);
published as `docs/11-sebaceous-duct-jamming-acne/`; layer hash
`1e8a557d9a8d7b05823259bb2fcac31e372b96272e47ef1f2f5d89b1b0246a84`.

**Cell-adhesion layer (v0.7.0, `repro/run_adhesion.py`, separate hash).** A **new target on the existing
measured KRT14 γ** (no new organ, no γ fetched, none fitted — desmosomes/hemidesmosomes anchor the
keratinocyte's keratin network, so adhesion is intrinsic to it; the hair-cycle pattern, not the sebaceous
new-organ pattern) — run as a **hysteretic two-state binding jam** on the *same* R19 switch, with two coupled
compartments on the *same* γ and spinodal — unlocked two more in-lane diseases, each a signed de-adhesion of
the one bond at the *same* antibody magnitude, intervention = the antibody cleared, no new constant:

| # | disease | compartment handle | covered as |
|---|---|---|---|
| 20 | pemphigus vulgaris | cell-cell (desmosomal, DSG3) | an anti-DSG3 antibody drives the cell-cell bond below the spinodal → intraepidermal/suprabasal split, cell-matrix bond intact ("tombstone"); failing bond is lateral → shear propagates → **Nikolsky positive**, flaccid; partial titre reduction does not re-adhere, clearance (rituximab/immunosuppression) does |
| 21 | bullous pemphigoid | cell-matrix (hemidesmosomal, BP180) | an anti-BP180 antibody of the **same magnitude** drives the cell-matrix bond below the spinodal → subepidermal split, cell-cell bonds intact (epidermis lifts whole); failing bond is basal, not lateral → shear does not propagate → **Nikolsky negative**, tense; corticosteroid/immunosuppression re-adheres |

The **Nikolsky sign is derived** from which compartment failed, not asserted. These pass a clinical-sign +
intervention-reversal battery and a **three-axis opposite-property discriminant** (intraepidermal ↔
subepidermal plane; positive ↔ negative Nikolsky; flaccid ↔ tense blister) — reproduced *from the compartment
alone*, at the *same* antibody magnitude; published as `docs/12-cell-adhesion-blistering/`; layer hash
`55dce8c267ea4c76d8d5b967535a4ee0876c4b67f605e6ae7d65bf38516f28ad`. *(Congenital epidermolysis bullosa is
gene-key → `disease_wp`, §3.)*

**Vasomotor layer (v0.8.0, `repro/run_vasomotor.py`, separate hash).** A **new target on the existing
measured EDAR γ** (no new organ, no γ fetched, none fitted — the cutaneous thermoregulatory interface, the
EDAR organ, carries two autonomic effector arms, the sudomotor/sweat arm (T5) and the vasomotor/blood-flow
arm; rosacea dysregulates the vasomotor arm, the **vascular mirror of hyperhidrosis** on the sudomotor arm,
so it is intrinsic to this organ; the hair-cycle / adhesion pattern, not the sebaceous new-organ pattern) —
run as a **hysteretic two-lock reactivity jam** on the *same* R19 switch — unlocked two more in-lane
diseases, each a signed vasomotor drive of the *opposite sign*, intervention = the drive reversed, no new
constant:

| # | disease | drive handle | covered as |
|---|---|---|---|
| 22 | rosacea | standing vasodilator reactivity (lowered flush threshold) | a standing dilator drive carries the vessel past the **upper** spinodal → **locks dilated** into persistent erythema and fixed telangiectasia (an early transient flush still returns); the LL-37/Demodex amplifier on the same dilated background gives the **papulopustular** subtype; anti-inflammatories clear the papules, brimonidine blanches transiently but does **not** reset (hysteresis), laser/IPL resets the telangiectasia |
| 23 | Raynaud phenomenon | cold/stress vasoconstrictor | a vasoconstrictor drive carries the vessel negative into the constricted/ischemic basin → a **reversible** digital vasospastic attack (primary Raynaud crosses **no** lock); rewarming and a vasodilator / calcium-channel blocker abort it; the **fixed** digital-ischemia/ulcer of secondary Raynaud (connective-tissue disease) is a named seam |

The **reversibility is derived** from whether a drive crosses its lock, not asserted. These pass a
clinical-sign + intervention-reversal battery and a **three-axis opposite-property discriminant**
(vasodilation ↔ vasoconstriction; fixed telangiectasia ↔ reversible vasospasm; vascular
erythematotelangiectatic ↔ inflammatory papulopustular) — reproduced *from the drive sign and the lock rule
alone*, on the *one reused EDAR γ*; published as `docs/13-neurovascular-reactivity-rosacea/`; layer hash
`53a99f522ad684a11bcc6d4d33c5e8123d1f4dff5a75836c0bbced6736a62003`. *(Secondary Raynaud's fixed ischemia is
an immune/rheumatology seam, and the dermal-perfusion magnitude is an inherited circulatory seam — neither
re-emerged here.)*

**Seam-manifest layer (v0.9.0, `repro/run_seam.py`, separate hash).** Not a new physical sweep but the
**consolidation** the master map's §9.2 calls for — every interface the package has, gathered into one
labelled, machine-readable record (HANDOFF §5.3, second bullet). **No new mechanism, no new constant.** Three
honestly distinct classes: **INHERITED-IN** (3 — the cited circulatory dermal-perfusion magnitude, the DNA
organ identity + emergence order + measured γ `[V]`, the R19 substrate; vendored read-only, never
re-derived); **INTERNAL-LIVE** (1 — the **pigment-loss → oncology** coupling: a melanocyte-target (T3) lesion
removing the melanin screen raises the shared oncology-kernel hazard, with the numbers **re-exported
verbatim** from the verified pathology layer so the seam output provably *is* the internal link surfaced, not
a parallel implementation — albinism-type screen-loss → SCC cumulative-hazard RR ≈ **2.58×**, melanoma burst
RR ≈ **10.59×**, exogenous sunscreen → SCC hazard RR back to ≈ **1.13×**, the screen as **causal lever**);
**DECLARED-OUT** (6 — sibling-package contracts flagged honestly as *declared, not yet live wiring*:
gene-lesion → `disease_wp`, the immune/rheumatology seams, out-of-class infections). The layer's own gate
runs four fidelity/honesty checks (re-export fidelity field-by-field, coupling sign + causal lever,
provenance + contract validity, non-disturbance — the pathology layer's `0a4404cc...` hash is unchanged after
the seam reads it). Published as `docs/14-cross-package-seams/`; layer hash
`52b49a95a9add070a05a02848b1a4cef0589f4a36791167232fda3fc1c1d58f7`. *(The live wiring of the DECLARED-OUT
contracts — §5.3 first bullet + §5.4 — remains future work: it needs the integration harness that does not
yet exist.)*

---

## 3. OUT OF LANE → `disease_wp` (single-gene rare genodermatoses, gene-key)

These are **not** this package's to model as primary entities. `disease_wp` owns the gene→lesion fact;
this package owns (and already covers, §2) the *dynamics* the lesion drives. The seam is §6.2: a
**bidirectional cross-reference**, not a merge. Items to register on the `disease_wp` side (and which
this package's dynamics entries should point to once the harness exists, §4.3):

- **Genetic ichthyoses** — FLG (ichthyosis vulgaris), TGM1 / ABCA12 (lamellar / harlequin), STS
  (X-linked) → gene-lesion entities; our T1+T4 retention dynamics is the systemic-trajectory side.
- **Ectodermal dysplasias** — EDA / EDAR / EDARADD → gene-lesion entities; our T5 capped-sweat dynamics
  (#9) is the trajectory side.
- **Oculocutaneous albinism subtypes** — TYR (OCA1), OCA2, TYRP1, SLC45A2 → gene-lesion entities; our
  T3→oncology screen-removed dynamics (#8) is the trajectory side.
- **Xeroderma pigmentosum** — XPA–XPG, POLH (DNA-repair genodermatosis) → `disease_wp`; our oncology
  UV-carcinogenesis dynamics is the trajectory side (an extreme of the same multistage kernel).
- **Hereditary skin-cancer syndromes** — Gorlin / PTCH1 (BCC), familial melanoma / CDKN2A → `disease_wp`
  (§6.1 rule 3: hereditary cancer syndromes are gene-key); our sporadic UV-driven cancers (#12) are ours.
- **Other genodermatoses** — Netherton (SPINK5), Darier (ATP2A2), Hailey–Hailey (ATP2C1), epidermolysis
  bullosa (COL7A1 / KRT5 / KRT14 / LAMB3 …) → `disease_wp`.

---

## 4. NOT YET MODELABLE in-lane — needs a NEW verified mechanism (honestly flagged, not faked)

These are common acquired skin diseases that *would* be this package's lane by etiology, but the package
does **not** yet have a mechanism for them. The organs are epidermis (TP63), keratinocyte (KRT14),
melanocyte (MITF), appendage = hair/sweat (EDAR), and sebaceous_gland (PRDM1, v0.6.0); the targets are T1
barrier, T2 wound, T3 melanin, T4 turnover, T5 thermoregulation, T6 hair-cycle oscillator (v0.5.0), T7
sebaceous-duct occlusion jam (v0.6.0), T8 cell-adhesion binding jam (v0.7.0), and the oncology kernel. None of the following maps onto those
without a **new** knob, and bolting them onto an unrelated knob would violate no-tuning. So they are
deferred to a mechanism-first step (§5.2), each with the missing piece named:

- ~~**Acne vulgaris** — needs a **sebaceous-gland** target (sebum + follicular keratinization + *C. acnes*).~~
  ✅ **DONE (v0.6.0):** a new measured sebaceous organ (PRDM1) was built as a hysteretic occlusion jam,
  unlocking acne vulgaris. See §2 (sebaceous-duct layer) and `repro/_seb/`.
- ~~**Androgenetic / areata alopecia** — needs a **hair-cycle oscillator**.~~ ✅ **DONE (v0.5.0):** the
  hair-cycle oscillator was built on the existing EDAR γ (the appendage organ already existed; only the
  cycling-dynamics target was missing), unlocking androgenetic alopecia, alopecia areata, telogen
  effluvium, and anagen effluvium. See §2 (hair-cycle layer) and `repro/_cycle/`.
- ~~**Rosacea** — needs a **neurovascular / inflammatory** module (flushing, dermal vessel reactivity).~~
  ✅ **DONE (v0.8.0):** built as a hysteretic two-state **reactivity jam** on the *existing measured* EDAR γ
  (the appendage / thermoregulation-interface organ already existed; its **vasomotor arm** — the vascular
  mirror of the sudomotor/sweat arm T5 — was the missing *target*, not a new organ; no γ fetched, none
  fitted). A standing vasodilator drive locks the vessel dilated (fixed telangiectasia) and a cold
  vasoconstrictor drive gives a reversible vasospastic attack, unlocking **rosacea** and **Raynaud
  phenomenon**, separated by a three-axis opposite-property discriminant (vasodilation/vasoconstriction;
  fixed/reversible by the lock rule; vascular/inflammatory). The **dermal-perfusion magnitude stays an
  inherited circulatory citation** — only the reactivity dynamics is added, so the SSOT seam is not crossed.
  See §2 (vasomotor layer) and `repro/_vasomotor/`. *(Secondary Raynaud's fixed ischemia (connective-tissue
  disease) remains an immune/rheumatology seam, §3-style.)*
- ~~**Autoimmune bullous** (pemphigus / bullous pemphigoid) — needs a **cell-adhesion** target
  (desmosome / hemidesmosome integrity as a binding switch).~~ ✅ **DONE (v0.7.0):** built as a hysteretic
  two-state **binding jam** on the *existing measured* KRT14 γ (the keratinocyte organ already existed;
  desmosomes/hemidesmosomes anchor its keratin network, so adhesion is intrinsic — a new *target*, not a new
  organ; no γ fetched, none fitted). Two coupled compartments on the *same* γ and spinodal — cell-cell
  (DSG3) and cell-matrix (BP180) — with a **derived** Nikolsky sign unlock **pemphigus vulgaris** and
  **bullous pemphigoid**, separated by a three-axis opposite-property discriminant (plane / Nikolsky /
  tension) at the *same* antibody magnitude. See §2 (cell-adhesion layer) and `repro/_adhesion/`. *(Congenital
  epidermolysis bullosa remains gene-key → `disease_wp`, §3.)*
- **Urticaria / angioedema** — mast-cell / histamine effector; this is the **`immune_hematologic`** seam
  (master map §3), not a skin-dynamics target. *Sibling-package seam.*
- ~~**Hidradenitis suppurativa** — follicular occlusion + inflammation; needs the same sebaceous/follicular
  machinery as acne.~~ ✅ **DONE (v0.6.0):** built as the same occlusion jam at greater depth with an
  irreversible rupture/scar branch. See §2 (sebaceous-duct layer) and `repro/_seb/`.
- **Lichen planus / inflammatory dermatoses** — interface inflammation; needs an immune-effector seam. *Sibling/seam.*
- **Cutaneous infections** (impetigo, cellulitis, dermatophytosis, herpes, warts) — pathogen-driven, **out
  of the package's physical class** entirely (not an R19-dynamics failure). Not in any dynamics lane.

---

## 5. NEXT STEPS (in priority order)

### 5.1 Promote the pathology research to a formal doc section (docs/09) — ✅ DONE (v0.4.0)
**Completed.** The pathology research is now published as the canonical HTML section
`docs/09-integumentary-pathology/index.html` (generated by `tools/build_docs.py`, the writing gate being
green: `research_gate` `all_green=true`, writing unlocked). It is built to VP-SPEC C4:
- answer-first `<p class="answer">` (52 words), JSON-LD (`ScholarlyArticle` + `BreadcrumbList`),
  `canonical`, a **claim-strip** (grade + reproduce link + DOI placeholder), and **one vp-card per cited
  `[L]` clinical anchor** (13 anchor cards + a determinism card = 14 total).
- The section is registered in `docs/_meta.json` `sections[]` and `sitemap.xml` / `llms.txt` are refreshed;
  the per-page HTML version label was also refreshed (it had been stale at 0.1.0).
- Body is **English** (C0); every `[O]` magnitude states its parent-target obstacle (C3); the pathology
  layer's own 2×sha256 determinism line is emitted in the section
  (`0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8`).
- Core battery untouched: `result_sha256` in `_meta.json` stays `1fb59f556e01…` (the disease layer is an
  additive `reports/`-backed research artifact whose hash is separate from the core T1–T5+oncology hash).

The remaining steps below (5.2–5.4) are unchanged future work.

### 5.2 Expand disease coverage ONLY after adding the mechanism (mechanism-first, no-tuning) — ⏳ FOUR ITEMS DONE (v0.5.0, v0.6.0, v0.7.0, v0.8.0)
For each §4 item, the correct order is: (1) add the **new target** (e.g. the hair-cycle T6 oscillator, the
sebaceous-duct T7 occlusion jam, and the cell-adhesion T8 binding jam already delivered) with its **own stress
suite** feeding `research_gate`;
(2) verify it green; (3) **then** add the disease as a perturbation of that new target. Never add the
disease first. If a γ is needed for a new organ, it is a **measured input or a "measurement target"**
(DNA pipeline), never fitted.

**Delivered (v0.5.0):** the **hair-cycle oscillator** (the §4 alopecia item) was added exactly this way —
the new target (a relaxation oscillator) was built on the *already-measured* EDAR γ with its own stress
suite (`repro/_cycle/cycle_verify.py` → `cycle_gate()`), verified green, and *only then* were the four
alopecias added as perturbations of it. No γ was fitted; the absolute anagen fraction and period are held
open `[O]` rather than tuned to the cited 85–90 %.

**Delivered (v0.6.0):** the **sebaceous-duct occlusion jam** (the §4 acne/HS item) was added the same way —
but as a **new measured organ**: PRDM1's γ was *fetched from NCBI, cached, and vendored* through the
identical promoter-ΔG pipeline validated against MITF/EDAR (never fitted; reproduces offline), the duct was
built as a hysteretic R19 occlusion jam with its own stress suite (`repro/_seb/seb_verify.py` →
`seb_gate()`), verified green, and *only then* were acne vulgaris and hidradenitis suppurativa added as
perturbations of it. Occlusion set-points are held as regime-scale `[F]`; absolute lesion counts stay open
`[O]`.

**Delivered (v0.7.0):** the **cell-adhesion binding jam** (the §4 autoimmune-bullous item) was added the same
way — but, like the hair-cycle layer, as a **new target on an existing measured organ**, not a new organ:
junctional adhesion is intrinsic to the keratinocyte (desmosomes/hemidesmosomes anchor its keratin network),
so it reuses the *already-measured* KRT14 γ with **no γ fetched and none fitted**. The bond was built as a
hysteretic R19 binding jam — two coupled compartments (cell-cell DSG3 / cell-matrix BP180) on the *same* γ and
spinodal, with a **derived** Nikolsky sign — with its own stress suite (`repro/_adhesion/adhesion_verify.py` →
`adhesion_gate()`), verified green, and *only then* were pemphigus vulgaris and bullous pemphigoid added as
signed de-adhesions of it, separated by a three-axis opposite-property discriminant (plane / Nikolsky /
tension) at the *same* antibody magnitude. Adhesion reserve and titres are held as regime-scale `[F]`;
absolute blister counts, titre, cleavage depth and BSA stay open `[O]`.

**Delivered (v0.8.0):** the **vasomotor reactivity jam** (the §4 rosacea item) was added the same way — like
the hair-cycle and adhesion layers, as a **new target on an existing measured organ**, not a new organ:
cutaneous vasomotor tone is intrinsic to the EDAR thermoregulation-interface organ (its vasomotor arm, the
vascular mirror of the sudomotor/sweat arm T5), so it reuses the *already-measured* EDAR γ with **no γ
fetched and none fitted**. The vessel was built as a hysteretic R19 reactivity jam with **two spinodal
locks** (a dilation lock above, a constriction lock below) and its own stress suite
(`repro/_vasomotor/vasomotor_verify.py` → `vasomotor_gate()`), verified green, and *only then* were rosacea
and Raynaud phenomenon added as signed vasomotor drives of opposite sign, separated by a three-axis
opposite-property discriminant (direction / reversibility by the lock rule / vascular-vs-inflammatory). The
resting tone, reactivity gains and constrictor drives are held as regime-scale `[F]`; absolute erythema
index, vessel density, digital temperature, attack frequency and BSA stay open `[O]`. Crucially the
**dermal-perfusion magnitude is left an inherited circulatory seam** — only the reactivity dynamics is added
— so the §4 note's caution ("dermal perfusion is an inherited citation, not a dynamics target here") is
honoured, not crossed. The remaining §4 items (immune-effector seams for urticaria and lichen planus;
out-of-class infections; and the fixed-ischemia secondary-Raynaud connective-tissue seam) still await their
own sibling-package seam — they are **not** this package's jamming-class lane.

### 5.3 Cross-package seam wiring (§9.2 of the master map) — ⏳ SECOND BULLET DONE (v0.9.0); first bullet still needs the harness
- The §3 gene-lesion cross-references are **contracts**, not wiring. When the integration harness exists,
  import the `disease_wp` gene-key parameters (XP/OCA/EDA/genetic-ichthyosis) and have the §2 dynamics
  entries emit the systemic-trajectory side. *(Still future work — the harness does not exist yet; recorded
  in the seam manifest as a DECLARED-OUT contract, not live wiring.)*
- The pigment-loss → oncology link (vitiligo/albinism lesion → melanoma burst sensitivity) is already
  internal here; expose it as a labeled seam output for the "one body" runner. — ✅ **DONE (v0.9.0).**

**Delivered (v0.9.0):** the **cross-package seam manifest** was added as a new additive layer `repro/_seam/`
(its own research-first determinism hash `52b49a95a9add070...`; the core battery and every disease layer left
byte-frozen). It consolidates every interface the package has into one labelled, machine-readable record in
three honestly distinct classes — **INHERITED-IN** (3: the cited circulatory dermal-perfusion magnitude, the
DNA organ identity + emergence order + measured γ `[V]`, the R19 substrate; vendored, never re-derived),
**INTERNAL-LIVE** (1, the headline above: the pigment-loss → oncology coupling, with the numbers
**re-exported verbatim** from the verified pathology layer — an albinism-type screen-loss raises the SCC
cumulative-hazard RR to ≈ 2.58× and the melanoma burst RR to ≈ 10.59×, while an exogenous sunscreen lowers
the SCC hazard RR back to ≈ 1.13×, so the screen is the **causal lever**, not a correlate), and
**DECLARED-OUT** (6: the sibling-package contracts including the first bullet's gene-lesion → `disease_wp`
list, flagged honestly as *declared, not yet live wiring*). **No new mechanism, no new constant** — it
surfaces the already-internal link, it does not invent one. The layer's own gate `seam_gate()` runs four
fidelity/honesty checks (re-export fidelity field-by-field, coupling sign + causal lever, provenance +
contract validity, non-disturbance — the pathology layer's `0a4404cc...` hash is unchanged after the seam
reads it). Promoted to the writing phase as **docs §14 "Cross-package seams"** (gate green). Grades: internal
coupling shape [V] / cited epidemiology [L] / absolute RR [O] (inherits the oncology obstacle — population
baseline + dose calibration). What remains genuinely future is the **live** wiring of the DECLARED-OUT
contracts (first bullet + §5.4), which needs the integration harness that does not yet exist.

### 5.4 Register the gene-lesion entities on the `disease_wp` side
Hand the §3 list to the `disease_wp` track so each gene-lesion is a named entity there, with a back-pointer
to this package's dynamics section. This closes the bidirectional cross-reference (§6.2).

---

## 6. How to continue (commands)

```
cd integumentary_vp_site
python repro/run_all.py          # core battery: all targets pass, sha must stay 1fb59f556e01..., writing unlocked
python repro/run_pathology.py    # 13 diseases pass + 5-way opposite-sign discriminant + 2xsha256 (~20-30s)
python repro/run_cycle.py        # hair-cycle oscillator + 4 alopecias + 3-way discriminant + 2xsha256 (sha d910fa5d2854...)
python repro/run_seb.py          # sebaceous-duct jam + acne + hidradenitis suppurativa + 3-way discriminant + 2xsha256 (sha 1e8a557d9a8d...)
python repro/run_adhesion.py     # cell-adhesion binding jam + pemphigus vulgaris + bullous pemphigoid + 3-axis discriminant + 2xsha256 (sha 55dce8c267ea...)
python repro/run_vasomotor.py    # vasomotor reactivity jam + rosacea + Raynaud phenomenon + 3-axis discriminant + 2xsha256 (sha 53a99f522ad6...)
python repro/run_seam.py         # cross-package seam manifest: pigment-loss->oncology re-exported (RR 2.58/10.59/1.13) + inherited/declared seams + 4 fidelity checks + 2xsha256 (sha 52b49a95a9ad...)
```

Invariant to preserve on every future edit: **additions are additive.** Touch neither the engine
(`repro/_engine`, `repro/_oncology`) nor the gates (`repro/_verify`) when adding pathology/doc content,
and re-confirm the core `run_all.py` hash is unchanged before packaging. Return a **single** zip
(package-relative paths), never fragments.
