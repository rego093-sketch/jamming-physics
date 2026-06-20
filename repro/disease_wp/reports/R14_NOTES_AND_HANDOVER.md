# R14 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.16, phase R14)

Phase R14 is **round 6** of the curated **PMC open-access** severity/progression lift R9 opened. It uses
the **same a-priori rule** and the **same frozen R3 tier function** (the tier is *derived* from the
verbatim cited sentence, never hand-asserted), and it is implemented as a **dedicated cumulative stage
over R13** so that every R9, R10, R11, R12 **and** R13 artifact — and their recorded registry-set shas
(**d07a544475dc**, **e77c0bf0e887**, **32cf48334233**, **8c5dbae815f7**, **49af5f824afa**) — stays
**byte-identical and immutable**. Single author (Young Jae Lee, ORCID 0009-0002-7535-8245). English
deliverables, VP-SPEC v1.8 discipline (no-tuning, bit-reproducible, honest grading `[O]<[H]<[L]<[V]`). All
gates green; engine pin drift 0.

The R3/R4 BANKED files stay byte-identical (gate-verified); the cumulative registry layer
**R5+R6+R7+R8+R9+R10+R11+R12+R13+R14** is what advances. Registry-set sha **fa60be77f767** (2× identical);
unmet-need surface sha **2ee20784582e** — **CHANGED** this round (like R11, R12 and R13), because R14
raises Fabry disease's and Classic homocystinuria's `raw_burden`, so the residual `burden_score` values and
the residual ranking move (Fabry rises into the placed residual order at 0.662 `[H]` × 0.70 = 0.464); W1
site-set sha **69d1e33b7b20** (2× identical), W1 gate 17/17.

## 0. Why R14 is a separate stage (architecture)

The established pattern in this codebase is **one stage, one gate** (`r1_gate`…`r13_gate`); R7 was a
separate cumulative stage over R6, R10 over R9, R11 over R10, R12 over R11, and R13 over R12. R14 follows
that pattern exactly:

- `code/pipeline/r14_severity_litcurate.py` takes the **R13 registry** as its base (it requires the
  `R13_litcurate5` pass to be present), reads its **own** round-6 CSVs, tags `R14_litcurate6`, and writes
  the four registry artifacts. It **imports R13's helpers** (`derive_tier`, `is_spectrum`, `load_pinned`,
  the R3 bindings, …), which in turn import R12's, R11's, R10's and R9's, so the locked
  tier/spectrum/decline logic **cannot drift**.
- `code/pipeline/r14_litcurate_fetch.py` pins the round-6 cited articles via R9's exact fetch logic
  (re-exposed through R10–R13). Five PMCIDs pinned, all open-access (PMC12055052, PMC13252739,
  PMC13151537, PMC12986390, PMC13188992).
- `code/pipeline/r14_gate.py` re-proves the chain (r5→r14, 2×) **and** proves **all ten** prior recorded
  CSVs — R9's, R10's, R11's, R12's and R13's `severity_litcurate{,2,3,4,5}_join.csv` / `*_excluded.csv` —
  are **byte-identical** to their recorded digests (`prior_round_artifacts_preserved`). R14 is strictly
  **additive**.

## 1. The three lifts (cited, frozen-R3-derived, non-spectrum) — none completes a lock

R14 makes **three lifts** — two VALUE+GRADE severity lifts and one grade-only progression corroboration.
**Not one of them order-locks**, because each disease retains an `[H]` on another scored axis. This is the
honest shape of round 6: defensible grade evidence added, no lock manufactured.

| disease | axis | before | after | cited OA source | frozen-R3 tier | locks? |
|---|---|---|---|---|---|---|
| **Classic homocystinuria** (C0751202) | S | 0.50 `[H]` | **0.75 `[L]`** | PMC12055052 (PMID 40337434) | 0.75 (severe / debilitating, via `life-threatening`; non-spectrum) | no — retains mortality `[H]` + disability `[H]` |
| **Fabry disease** (C0002986) | S | 0.50 `[H]` | **0.75 `[L]`** | PMC13252739 (PMID 42268866) | 0.75 (severe / debilitating, via `severe`; non-spectrum) | no — retains mortality `[H]` |
| **Becker muscular dystrophy** (C0917713) | P | 0.50 `[H]` | **0.50 `[L]`** | PMC13151537 (PMID 41760395) | 0.50 (progressive course, via `progressive`; non-spectrum) | no — retains severity `[H]` |

**Classic homocystinuria — VALUE+GRADE severity lift, does NOT lock.**
- The cited sentence — *"Classical homocystinuria (HCU) is a rare but life-threatening autosomal recessive
  metabolic disorder resulting in buildup of amino acid methionine and homocysteine in urine and blood due
  to cystathionine-β-synthase lack (CBS deficiency, OMIM 236200) …"* — is a **disease-level,
  non-comparative, non-spectrum** statement defining HCU itself, with `life-threatening` the operative
  magnitude word and no higher-tier qualifier preceding it. Frozen R3 `first_match` over
  `PATTERNS["S_severity"]` maps it to tier **0.75**; `is_spectrum` = False.
- Dominant untreated sequela: vascular thromboembolism (arterial and venous thrombosis — the leading cause
  of premature morbidity and of death in untreated patients), with ectopia lentis, skeletal abnormalities
  and developmental delay.
- **Why it does NOT lock.** HCU's mortality is `[H]` and its disability is `[H]`; progression is unscored
  `[O]`. The severity `[H]`→`[L]` lift resolves the prior severity-midpoint to the entity's own severe
  magnitude (S 0.50→0.75) — a coverage + `raw_burden` advance, **not** a lock.

**Fabry disease — VALUE+GRADE severity lift, does NOT lock.**
- The cited sentence — *"Fabry disease (FD) in an inherited lysosomal storage disorder with severe lifelong
  issues if not therapeutically managed."* — is a **disease-level, non-comparative, non-spectrum**
  statement that explicitly frames the **untreated** magnitude, with `severe` the operative word (not
  preceded by more/most/less/other). Frozen R3 maps it to tier **0.75**; `is_spectrum` = False.
- Dominant untreated sequela: progressive multi-organ globotriaosylceramide accumulation — progressive
  renal failure, hypertrophic cardiomyopathy and cerebrovascular disease (stroke) — the prognosis-
  determining course absent enzyme/chaperone therapy.
- **Why it does NOT lock.** Fabry's mortality remains `[H]`; disability is unscored `[O]`. S 0.50→0.75 is a
  coverage + `raw_burden` advance only.

**Becker muscular dystrophy — GRADE-only progression lift, does NOT lock.**
- The cited sentence — *"Becker muscular dystrophy (BMD) is an X-linked recessive neuromuscular disorder
  characterised by progressive muscle weakness and wasting."* — characterises **BMD on its own terms, NOT
  relative to Duchenne**; `progressive` is the operative word. Frozen R3 maps it to tier **0.50**;
  `is_spectrum` = False. The value is **unchanged** (already 0.50); only the grade lifts `[H]`→`[L]`.
- **Why it does NOT lock, and why it is honest.** BMD's severity stays 0.50 `[H]` — its only retrievable
  `severe` framing is the dystrophinopathy-class-grouped one (Duchenne+Becker), which was **declined at
  R13**. R14 does **not** revisit that; it lifts a **different** axis (progression) from a clean
  BMD-specific sentence. The R13 BMD frontier is advanced where newly defensible, not re-litigated where it
  is not.

## 2. The two declines (recorded, never lifted)

Both considered statements were found and **verbatim-pinned**, then disqualified under the frozen rule.
Each is recorded in `methodology/severity_litcurate6_excluded.csv` with its `decline_class` and per-disease
reason, and surfaced in `IRREPRODUCIBILITY_LEDGER.md` (Round-6 block).

| disease | axis | decline class | why it does not lift | source |
|---|---|---|---|---|
| **Polycystic kidney disease 2** (C2751306) | S | `comparative` | the framing is PKD1-vs-PKD2: *"PKD1 variants are associated with more severe disease and earlier ESRD … compared to PKD2 mutations, in which the disease progression is less severe …"* — PKD2's magnitude is given only **relative** to PKD1 (PKD2 = the milder, later-ESRD form). The frozen R3 severity function does not even match it (the `severe` tier is blocked by the `more `/`less ` negative lookbehinds); no non-comparative disease-level PKD2 magnitude is retrievable. S left `[H]`. | PMC12986390 / PMID 41828581 |
| **Osteogenesis imperfecta** (C0029434) | P | `spectrum` | *"The phenotypes of these 17 OI patients varied widely, ranging from moderate (multiple fractures with progressive skeletal deformities) to mild …"* — `progressive` attaches only to the **moderate** Sillence sub-form inside a 17-patient cohort that varies moderate→mild. A within-entity / form-specific spectrum, not an isolable disease-level progression magnitude. P left `[H]`. | PMC13188992 / PMID 42170682 |

Lift only where defensible; decline transparently; never fish for a lock.

## 2a. A note on the OI entity across two rounds

Osteogenesis imperfecta was declined on **severity** at R13 (`comparative` Sillence phenotype-class) and is
now declined on **progression** at R14 (`spectrum`, moderate-to-mild cohort range). Two different axes, two
different obstacles, both honestly recorded — the entity remains open on both axes, neither manufactured
into a lift.

## 3. Net effect — honest

- **Severity** coverage rises to **9/35** `[L]` ({[L]: 9, [O]: 11, [H]: 15}); **progression** to **12/35**
  `[L]` ({[O]: 21, [L]: 12, [H]: 2}).
- **order_locked stays 5/35** (Achondrogenesis type II, Niemann-Pick disease type A, Tyrosinemia type II,
  Marfan syndrome, Duchenne muscular dystrophy) — **nothing added, nothing removed**. The three lifts each
  raise a grade `[H]`→`[L]` **without** completing a lock (each retains an `[H]` on another scored axis).
- **16 placed diseases still carry ≥1 `[H]` axis** — unchanged, the visible signature of the no-lock
  property: a disease that retains an `[H]` axis after a lift stays in the `[H]` set.
- The burden **order** remains a provisional `[H]` prioritisation device cohort-wide. The OMIM
  clinical-synopsis path stays **REMOVED** (key unobtainable for an individual researcher), not deferred.

## 4. Gates and verification

R14 gate **PASS 16/16** (`code/pipeline/r14_gate.py`): determinism (r5→r14, 2×, sha `fa60be77f767`);
banked unchanged; cumulative-over-R13; round-6 join re-anchored verbatim in the pinned PMC-OA cache +
tier-from-frozen-R3 + non-spectrum; cut-points a-priori; round-6 declines recorded; add-only no-downgrade
vs R13; S/P-only changed only for the 3 round-6 joined diseases (O/M/D byte-identical to R13); **no new
order-lock** proved (5→5); raw_burden re-derived; rankability; residual; order-lock rule + sensitivity
(equal ρ=1.0); round-6 sources open-access + source-bound; **all ten** prior join/excluded CSVs
byte-identical (R14 additive); engine pin drift 0 (15/15).

```
python3 code/pipeline/r14_litcurate_fetch.py         # 5/5 OA cached
python3 code/pipeline/r14_severity_litcurate.py      # registry-set sha fa60be77f767
python3 code/pipeline/r14_gate.py                    # PASS 16/16
python3 code/pipeline/w_unmet_need_surface.py
python3 code/pipeline/w_unmet_need_gate.py           # PASS 6/6  (surface sha 2ee20784582e)
python3 tools/w1_build.py                            # site-set sha 69d1e33b7b20
python3 tools/w1_gate.py                             # PASS 17/17
```

(Each gate is self-healing and leaves the registry at **its own** stage, so after running an earlier
`rN_gate` re-run the full r5→r14 chain before inspecting the registry at R14.)

All prior gates still green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 ·
R7 16/16 · R8 16/16 · R9 15/15 · R10 16/16 · R11 16/16 · R12 16/16 · R13 16/16 · unmet-need 6/6 · W1 17/17 ·
boundary 6/6.

## 5. Handover → R15

The curated-PMC-OA frontier still has placed diseases carrying an `[H]` axis — overwhelmingly **severity**
(the cohort-wide open axis after R14). Obstacle-bound / frontier entities to **not** re-litigate unless a
clean disease-level OA magnitude becomes retrievable:

- **Hb SS disease** (progression + severity) and **Alpha-1-antitrypsin deficiency** (progression) —
  umbrella/genotype-scoped or spectrum, recorded as permanent §C(b) obstacles.
- **Gaucher disease type I** and **Gaucher disease (umbrella)** severities — declined `comparative` at R11
  (`severity_litcurate3_excluded.csv`).
- **Hurler syndrome** severity (comparative phenotype-class label) and **Beta-thalassemia** severity
  (umbrella spectrum) — declined at R12 (`severity_litcurate4_excluded.csv`).
- **Osteogenesis imperfecta** severity (comparative Sillence label, R13) and **alpha Thalassemia** severity
  (umbrella spectrum, R13) — `severity_litcurate5_excluded.csv`; **Osteogenesis imperfecta** progression
  (spectrum) and **Polycystic kidney disease 2** severity (PKD1-vs-PKD2 comparative) — declined at R14
  (`severity_litcurate6_excluded.csv`).
- **Hemophilia A** severity (R12) and **Hemophilia B** severity (R13) — only factor-stratum sub-phenotype
  framing retrievable; liftable only on a disease-level (not factor-stratum) magnitude.
- **Becker muscular dystrophy** **severity** (R13) — only the dystrophinopathy-class-grouped `severe` is
  retrievable; liftable only on a clean BMD-specific disease-level magnitude. (Its **progression** was
  lifted at R14 from a clean BMD-specific sentence.)

**R15** continues the **same rule** on the placed cohort's remaining `[H]`/`[O]` **severity** /
**progression** (and any further **mortality**) axes, lifting only where a cited disease-level OA magnitude
for the dominant untreated sequela maps to a frozen-R3 tier, **non-spectrum and non-comparative**.
**Implement R15 as a new cumulative stage** (`r15_*` + `r15_gate`) over the R14 registry — its own
`severity_litcurate7_*` CSVs, its own fetch+pin, leaving all prior artifacts byte-identical — per the
established one-stage-one-gate pattern. The OMIM clinical-synopsis path stays **removed** (key unobtainable
for an individual researcher), not deferred. The forward plan is carried in the whitepaper (site §1
`#forward`) and `FUTURE_WORK.md` until a dated completion declaration (§C) replaces it.
