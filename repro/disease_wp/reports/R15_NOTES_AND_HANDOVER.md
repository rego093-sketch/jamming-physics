# R15 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.17, phase R15)

Phase R15 is **round 7** of the curated **PMC open-access** severity/progression lift R9 opened. It uses
the **same a-priori rule** and the **same frozen R3 tier function** (the tier is *derived* from the
verbatim cited sentence, never hand-asserted), and it is implemented as a **dedicated cumulative stage
over R14** so that every R9, R10, R11, R12, R13 **and** R14 artifact — and their recorded registry-set shas
(**d07a544475dc**, **e77c0bf0e887**, **32cf48334233**, **8c5dbae815f7**, **49af5f824afa**, **fa60be77f767**)
— stays **byte-identical and immutable**. Single author (Young Jae Lee, ORCID 0009-0002-7535-8245). English
deliverables, VP-SPEC v1.8 discipline (no-tuning, bit-reproducible, honest grading `[O]<[H]<[L]<[V]`). All
gates green; engine pin drift 0.

The R3/R4 BANKED files stay byte-identical (gate-verified); the cumulative registry layer
**R5+R6+R7+R8+R9+R10+R11+R12+R13+R14+R15** is what advances. Registry-set sha **efe81b447194** (2× identical);
unmet-need surface sha **a3c6c16fdeeb** — **CHANGED** this round (like R11–R14), because R15 raises
Achondroplasia's, Phenylketonuria's and Acute intermittent porphyria's `raw_burden`, so the residual
`burden_score` values and the residual ranking move (Achondroplasia enters the placed residual order); W1
site-set sha **c5559c704a75** (2× identical), W1 gate 17/17.

This round differs from R9–R14 in one honest respect: **one of the three lifts completes an order-lock**
(Phenylketonuria, 5 → 6). It is disclosed as a **consequence**, not engineered — see §1a. The other two
lifts do **not** lock (Acute intermittent porphyria stays sub-rankable at 2 axes; Achondroplasia becomes
rankable but retains mortality `[H]`).

## 0. Why R15 is a separate stage (architecture)

The established pattern in this codebase is **one stage, one gate** (`r1_gate`…`r14_gate`); R7 was a
separate cumulative stage over R6, R10 over R9, and each of R11–R14 over its predecessor. R15 follows that
pattern exactly:

- `code/pipeline/r15_severity_litcurate.py` takes the **R14 registry** as its base (it requires the
  `R14_litcurate6` pass to be present), reads its **own** round-7 CSVs, tags `R15_litcurate7`, and writes
  the four registry artifacts. It **imports R14's helpers** (`derive_tier`, `is_spectrum`, `load_pinned`,
  the R3 bindings, …), which chain back through R13→R12→R11→R10→R9, so the locked
  tier/spectrum/decline logic **cannot drift**.
- `code/pipeline/r15_litcurate_fetch.py` pins the round-7 cited articles via R9's exact fetch logic
  (re-exposed through R10–R14). Five PMCIDs pinned, all open-access (PMC13091603, PMC13046303,
  PMC13259324, PMC13214666, PMC13019597).
- `code/pipeline/r15_gate.py` re-proves the chain (r5→r15, 2×) **and** proves **all twelve** prior recorded
  CSVs — R9's…R14's `severity_litcurate{,2,3,4,5,6}_join.csv` / `*_excluded.csv` — are **byte-identical**
  to their recorded digests (`prior_round_artifacts_preserved`). R15 is strictly **additive**. The only
  gate-logic change vs `r14_gate.py`: the `no_new_order_lock` check is replaced by
  **`order_lock_change_documented`**, which asserts the lock-set delta is **exactly +Phenylketonuria**
  (added=`['C0031485']`, removed=`[]`) and that AIP and Achondroplasia each correctly do **not** lock.

## 1. The three lifts (cited, frozen-R3-derived, non-spectrum) — two do not lock, PKU does (disclosed)

R15 makes **three severity lifts**, all to the **same severe / tier-0.75 bucket** (each tier *derived* from
the disease-defining sentence by the frozen R3 function via the operative word `severe`). They differ only
in **prior grade**: AIP was a scored `[H]` midpoint; Achondroplasia and Phenylketonuria were **previously
unscored `[O]`** severity axes now scored for the first time.

| disease | axis | before | after | cited OA source | frozen-R3 tier | locks? |
|---|---|---|---|---|---|---|
| **Acute intermittent porphyria** (C0162565) | S | 0.50 `[H]` | **0.75 `[L]`** | PMC13091603 (PMID 42005216) | 0.75 (severe / debilitating, via `severe`; non-spectrum) | **no** — only 2 scored axes (< 3) |
| **Achondroplasia** (C0001080) | S | — `[O]` | **0.75 `[L]`** | PMC13046303 (PMID 41615893) | 0.75 (severe / debilitating, via `severe`; non-spectrum) | **no** — retains mortality `[H]` |
| **Phenylketonuria** (C0031485) | S | — `[O]` | **0.75 `[L]`** | PMC13259324 (PMID 42280447) | 0.75 (severe / debilitating, via `severe`; non-spectrum) | **YES** — O+D already `[L]`; completes lock (disclosed, §1a) |

**Acute intermittent porphyria — VALUE+GRADE severity lift, does NOT lock.**
- The cited sentence — *"Acute intermittent porphyria (AIP) is a rare metabolic disorder characterized by
  neurovisceral manifestations, most commonly severe abdominal pain."* — is a **disease-level,
  non-comparative, non-spectrum** statement defining AIP itself, with `severe` the operative magnitude word
  characterising the cardinal manifestation (severe abdominal pain), not preceded by more/most/less/other.
  Frozen R3 `first_match` over `PATTERNS["S_severity"]` maps it to tier **0.75**; `is_spectrum` = False.
- Dominant untreated sequela: the acute neurovisceral attack — severe abdominal pain with autonomic and
  peripheral-neuropathic features, which can progress to respiratory paralysis and death if untreated.
- **Why it does NOT lock.** AIP has only **two scored axes** — onset `[L]` and (now) severity `[L]`;
  progression, mortality and disability are all unscored `[O]`. Two scored axes is **below the 3-axis
  rankability cut**, so AIP is **not even placed**: the lift resolves the prior mild-to-severe
  MedGen-range `[H]` midpoint to the entity's own severe magnitude (the penetrance issue is *who* manifests,
  not the *magnitude* of manifest disease) — a severity-coverage + `raw_burden` advance only.

**Achondroplasia — VALUE+GRADE severity lift on a previously-unscored axis, does NOT lock.**
- The cited sentence — *"Achondroplasia is a rare skeletal dysplasia characterized by severe disproportionate
  short stature."* — is a **disease-level, non-comparative, non-spectrum** definitional statement, with
  `severe` the operative word qualifying the dominant sequela (disproportionate short stature). Frozen R3
  maps it to tier **0.75**; `is_spectrum` = False.
- Dominant sequela: rhizomelic disproportionate short stature with macrocephaly and midface hypoplasia.
- **Why it does NOT lock.** Scoring severity makes Achondroplasia **rankable** (now 3 scored axes: onset
  1.0 `[L]` + severity 0.75 `[L]` + mortality 0.40 `[H]`) and **promotes it into the placed order**, but
  mortality 0.40 `[H]` — the qualified foramen-magnum / cervicomedullary infant-mortality risk — **remains
  `[H]` on a scored axis**, so the all-`[L]` lock condition is not met.

**Phenylketonuria — VALUE+GRADE severity lift on a previously-unscored axis, COMPLETES a lock.**
- The cited sentence — *"PAH deficiency leads to hyperphenylalaninemia, with untreated blood Phe levels often
  exceeding 1200 μmol/L in classical PKU [ 2 ], resulting in severe intellectual disability and irreversible
  brain damage if not managed promptly [ 1 ]."* — is a **disease-level, non-comparative, non-spectrum**
  statement that explicitly frames the **untreated** magnitude in classical PKU, with `severe` the operative
  word. Frozen R3 maps it to tier **0.75**; `is_spectrum` = False. (The verbatim string includes the
  `μmol/L` unit and the source's `[ 2 ]` / `[ 1 ]` citation spacing; it was extracted programmatically and
  is re-found byte-for-byte in the pinned cache by the gate.)
- Dominant untreated sequela: severe, irreversible neurological injury — progressive intellectual disability
  and brain damage from chronic hyperphenylalaninaemia — the prognosis-determining outcome absent dietary
  Phe restriction (the magnitude for which universal newborn screening exists).
- **Why it locks — and why that is honest:** see §1a.

## 1a. The PKU order-lock — disclosed as a consequence, not engineered

Scoring PKU's severity at `[L]` makes its **three scored axes all `[L]`** — onset O 1.0 `[L]` (HPO
congenital onset), disability D 0.50 `[L]` (GBD severe-intellectual-disability weight), and now severity
S 0.75 `[L]` — with progression and mortality unscored `[O]`. Three scored axes, all `[L]`, clears the
order-lock rule (`rankable ≥3 AND every scored axis ∈ {[L],[V]}`), so **PKU becomes `order_locked` and the
lock set moves 5 → 6** — the **same 3-scored-axes-all-`[L]` pattern** as the existing Achondrogenesis type II
and Tyrosinemia type II locks.

This is **not lock-fishing**, on four independent grounds:

1. **The axes are orthogonal by design.** Severity (magnitude of disease) and disability (functional
   dependence, the GBD disability weight) measure different things; onset is a third, independent axis. The
   lock is not the same evidence counted twice.
2. **The sources differ.** S comes from the curated PMC-OA severity literature; D from the GBD 2013
   disability weight (banked at R7); O from HPO. No single source was leaned on to assemble the lock.
3. **The cited sentence passes every inclusion criterion on its own.** It is a disease-level, non-spectrum,
   non-comparative, untreated-magnitude statement whose tier is *derived* by the frozen R3 function — it
   would be lifted regardless of what the other two axes happened to be.
4. **PKU's untreated severity is the single most robustly documented disease-level magnitude in the
   cohort** — universal newborn screening exists precisely because the untreated outcome is severe and
   irreversible. Declining this lift to *avoid* a lock would itself be a tuning decision (suppressing
   defensible evidence to hold a number), which the no-tuning discipline forbids.

The order-lock is therefore the **honest consequence of a maximally defensible lift** — disclosed in the
join CSV's `dominant_sequela_basis`, in VERSION, and here, and **gated**: the R15
`order_lock_change_documented` check asserts the delta is **exactly +Phenylketonuria** and that AIP (2 axes)
and Achondroplasia (retains mortality `[H]`) each correctly do **not** lock. Lift where defensible; disclose
the consequence; never *suppress* a defensible lift to hold a number, and never *manufacture* one to gain a
number.

## 2. The two declines (recorded, never lifted)

Both considered statements were found and **verbatim-pinned**, then disqualified under the frozen rule.
Each is recorded in `methodology/severity_litcurate7_excluded.csv` with its `decline_class` and per-disease
reason, and surfaced in `IRREPRODUCIBILITY_LEDGER.md` (Round-7 block).

| disease | axis | decline class | why it does not lift | source |
|---|---|---|---|---|
| **21-Hydroxylase-Deficient Congenital Adrenal Hyperplasia** (C2936858) | S | `form_specific` | *"The severest form of CAH results from an almost complete absence in enzyme activity that can lead to life-threatening salt-wasting (SW-CAH) in the first weeks of life …"* — the `life-threatening` magnitude attaches to the **severest form** (classic salt-wasting SW-CAH), one allelic sub-form, not to the 21-OHD CAH entity as a whole (which also comprises the simple-virilizing classic form and the characteristically **mild** non-classic late-onset form). The entity's own registry basis already records a mild-to-severe variable-severity spectrum, so no clean isolable disease-level magnitude is retrievable. Consistent with the umbrella/form declines for alpha-thalassaemia, beta-thalassaemia and Hb SS. S left `[H]`. | PMC13214666 / PMID 42201219 |
| **Hemochromatosis type 1** (C3469186) | S | `comparative` | *"Male HFE C282Y homozygotes genetically predisposed to higher TSAT had a greater risk of haemochromatosis and severe clinical outcomes … compared with those with genetically predicted low TSAT."* — `severe clinical outcomes` is framed only as a **between-stratum contrast** (high- vs low-TSAT-predisposed homozygotes), not a clean disease-level magnitude for the HFE-HH entity's dominant untreated sequela (progressive parenchymal iron overload → cirrhosis / HCC / cardiomyopathy / diabetes). Type 1 HH is characteristically **low-penetrance**; the other retrievable `severe` framings are a C282Y-heterozygote case report and a non-dominant arthropathy hedge. S left `[H]` at value 0.75. | PMC13019597 / PMID 41951274 |

Lift only where defensible; decline transparently; never fish for a lock.

## 2a. A note on the previously-unscored severity axes, and on the frontier not re-litigated

Two of this round's lifts (Achondroplasia, Phenylketonuria) scored a **previously-unscored `[O]` severity
axis** for the first time — distinct from the R9–R14 pattern of lifting an already-scored `[H]` midpoint to
`[L]`. The frozen rule is identical either way: the tier is *derived* from a disease-level, non-spectrum,
non-comparative cited sentence; the only difference is that the prior cell was `[O]` (no obstacle now stands)
rather than `[H]`.

The curated-PMC-OA frontier still has placed diseases carrying an `[H]` axis where **no clean disease-level
OA magnitude is currently retrievable**; these were **not** forced into the excluded CSV this round (mirroring
the R12 Hemophilia-A and R13 BMD-severity frontier handling):
- **Wilson disease** — the retrievable OA `severe` framings attach to sub-symptoms (e.g. severe hepatic
  presentation in a subset) rather than a single disease-level magnitude for the entity's dominant untreated
  sequela; left as a frontier observation, not manufactured into a lift or a decline.
- **Hemochromatosis type 1** — the retrievable disease-level framings are now **exhausted** as of R15 (the
  comparative high-vs-low-TSAT statement is recorded as a decline above; no non-comparative disease-level
  magnitude is retrievable).

## 3. Net effect — honest

- **Severity** coverage rises to **12/35** `[L]` (`{[L]: 12, [O]: 9, [H]: 14}`); **progression** unchanged at
  **12/35** `[L]` (`{[O]: 21, [L]: 12, [H]: 2}`). Onset `{[L]: 28, [H]: 4, [O]: 3}`; mortality
  `{[L]: 8, [O]: 18, [H]: 9}`; disability `{[O]: 21, [L]: 13, [H]: 1}` — all unchanged from R14 (S-only round).
- **order_locked moves 5 → 6** — **+Phenylketonuria** (Achondrogenesis type II, Niemann-Pick disease type A,
  **Phenylketonuria**, Tyrosinemia type II, Marfan syndrome, Duchenne muscular dystrophy); nothing removed.
  PKU completes a lock as a **disclosed consequence** (§1a); the other two lifts do not lock (AIP
  sub-rankable at 2 axes; Achondroplasia retains mortality `[H]`).
- **Placement:** 23 placed (rankable ≥3 axes). **+2 promoted from not-placed this round** — Achondroplasia
  and Phenylketonuria (each crossed the 3-axis cut as severity was scored). AIP stays **not placed** (2 axes).
- **Placed diseases carrying ≥1 `[H]` axis: 16 → 17** — the **+1** is Achondroplasia, newly placed while
  retaining mortality `[H]`. This is the visible signature of the no-lock property for that lift (a newly
  placed disease that retains an `[H]` axis joins the `[H]` set rather than locking).
- The burden **order** remains a provisional `[H]` prioritisation device cohort-wide. The OMIM
  clinical-synopsis path stays **REMOVED** (key unobtainable for an individual researcher), not deferred.

## 4. Gates and verification

R15 gate **PASS 16/16** (`code/pipeline/r15_gate.py`): determinism (r5→r15, 2×, sha `efe81b447194`);
banked unchanged; cumulative-over-R14; round-7 join re-anchored verbatim in the pinned PMC-OA cache +
tier-from-frozen-R3 + non-spectrum; cut-points a-priori; round-7 declines recorded; add-only no-downgrade
vs R14; S/P-only changed only for the 3 round-7 joined diseases (O/M/D byte-identical to R14);
**order-lock change documented** (5 → 6, exactly +Phenylketonuria — disclosed consequence, AIP and
Achondroplasia each do not lock); raw_burden re-derived; rankability + promotions (6 promoted); residual;
order-lock rule + sensitivity (equal ρ=1.0); round-7 sources open-access + source-bound; **all twelve**
prior join/excluded CSVs byte-identical (R15 additive); engine pin drift 0 (15/15).

```
python3 code/pipeline/r15_litcurate_fetch.py         # 5/5 OA cached
python3 code/pipeline/r15_severity_litcurate.py      # registry-set sha efe81b447194
python3 code/pipeline/r15_gate.py                    # PASS 16/16
python3 code/pipeline/w_unmet_need_surface.py
python3 code/pipeline/w_unmet_need_gate.py           # PASS 6/6  (surface sha a3c6c16fdeeb)
python3 tools/w1_build.py                            # site-set sha c5559c704a75
python3 tools/w1_gate.py                             # PASS 17/17
```

(Each gate is self-healing and leaves the registry at **its own** stage, so after running an earlier
`rN_gate` re-run the full r5→r15 chain before inspecting the registry at R15.)

**Two `tools/w1_build.py` maintenance edits this round** (both correcting genuine drift, neither touching
the registry):
1. **`llms.txt` staleness + size.** The "Registry passes" summary line still described an **R10 / 3-locks**
   state; it was corrected to the accurate *"severity & progression [L] via curated PMC-OA literature,
   frozen-R3 tier (R8–R15, 12+12/35)"* wording. This also brought `docs/llms.txt` back **under the 5 KB gate
   limit** (5009 → 4954 bytes).
2. **Framework-page narrative.** The retrospective span was advanced **R9–R14 → R9–R15** with the R15 round
   (3 lifts + the PKU 6th-lock disclosed + 2 declines) inserted; the now-historical *live* order-lock count
   in the R14-era sentence was pinned to its literal value; and the forward framing was repointed
   **"R15 continues …" → R16**. A new **Round-7 (R15)** literature-curation declines block is auto-generated
   into `IRREPRODUCIBILITY_LEDGER.md` straight from `severity_litcurate7_excluded.csv`.

All prior gates still green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 ·
R7 16/16 · R8 16/16 · R9 15/15 · R10 16/16 · R11 16/16 · R12 16/16 · R13 16/16 · R14 16/16 · unmet-need 6/6 ·
W1 17/17 · boundary 6/6.

## 5. Handover → R16

The curated-PMC-OA frontier still has placed diseases carrying an `[H]` axis — overwhelmingly **severity**
(the cohort-wide open axis after R15: `{[L]: 12, [O]: 9, [H]: 14}`). Obstacle-bound / frontier entities to
**not** re-litigate unless a clean disease-level OA magnitude becomes retrievable:

- **Hb SS disease** (progression + severity) and **Alpha-1-antitrypsin deficiency** (progression) —
  umbrella/genotype-scoped or spectrum, recorded as permanent §C(b) obstacles.
- **Gaucher disease type I** and **Gaucher disease (umbrella)** severities — declined `comparative` at R11.
- **Hurler syndrome** severity (comparative phenotype-class label) and **Beta-thalassemia** severity
  (umbrella spectrum) — declined at R12.
- **Osteogenesis imperfecta** severity (comparative Sillence label, R13) + progression (spectrum, R14);
  **alpha Thalassemia** severity (umbrella spectrum, R13); **Polycystic kidney disease 2** severity
  (PKD1-vs-PKD2 comparative, R14).
- **Hemophilia A** severity (R12) and **Hemophilia B** severity (R13) — only factor-stratum sub-phenotype
  framing retrievable; liftable only on a disease-level (not factor-stratum) magnitude.
- **Becker muscular dystrophy** severity (R13) — only the dystrophinopathy-class-grouped `severe`
  retrievable; liftable only on a clean BMD-specific disease-level magnitude.
- **21-Hydroxylase-Deficient CAH** severity (`form_specific`, severest-form salt-wasting) and
  **Hemochromatosis type 1** severity (`comparative`, high-vs-low-TSAT) — **new this round** (R15
  declines); the latter's retrievable disease-level framings are now exhausted.
- **Wilson disease** severity — only sub-symptom `severe` framings retrievable; left as a frontier
  observation (not yet a recorded decline).

**R16** continues the **same rule** on the placed cohort's remaining `[H]`/`[O]` **severity** /
**progression** (and any further **mortality**) axes, lifting only where a cited disease-level OA magnitude
for the dominant untreated sequela maps to a frozen-R3 tier, **non-spectrum and non-comparative**.
**Implement R16 as a new cumulative stage** (`r16_*` + `r16_gate`) over the R15 registry — its own
`severity_litcurate8_*` CSVs, its own fetch+pin, leaving all prior artifacts byte-identical — per the
established one-stage-one-gate pattern. If a lift again completes a lock, **disclose it as a consequence**
(as PKU was at R15) and let the gate's `order_lock_change_documented` check assert the exact delta; never
suppress a defensible lift to hold a number, never manufacture one to gain a number. The OMIM
clinical-synopsis path stays **removed** (key unobtainable for an individual researcher), not deferred. The
forward plan is carried in the whitepaper (site §1 `#forward`) and `FUTURE_WORK.md` until a dated completion
declaration (§C) replaces it.
