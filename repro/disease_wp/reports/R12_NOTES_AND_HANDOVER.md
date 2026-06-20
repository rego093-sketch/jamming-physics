# R12 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.14, phase R12)

Phase R12 is **round 4** of the curated **PMC open-access** severity/progression lift R9 opened. It uses
the **same a-priori rule** and the **same frozen R3 tier function** (the tier is *derived* from the
verbatim cited sentence, never hand-asserted), and it is implemented as a **dedicated cumulative stage
over R11** so that every R9, R10 **and** R11 artifact — and their recorded registry-set shas
(**d07a544475dc**, **e77c0bf0e887**, **32cf48334233**) — stays **byte-identical and immutable**. Single
author (Young Jae Lee, ORCID 0009-0002-7535-8245). English deliverables, VP-SPEC v1.8 discipline
(no-tuning, bit-reproducible, honest grading `[O]<[H]<[L]<[V]`). All gates green; engine pin drift 0.

The R3/R4 BANKED files stay byte-identical (gate-verified); the cumulative registry layer
**R5+R6+R7+R8+R9+R10+R11+R12** is what advances. Registry-set sha **8c5dbae815f7** (2× identical);
unmet-need surface sha **ec01978d5919** — **CHANGED** this round (like R11, unlike R10), because R12 raises
Duchenne MD's `raw_burden` (0.630 → 0.680), so the residual `burden_score` values and the residual ranking
move; W1 site-set sha **c5dd896d4fe6** (2× identical), W1 gate 17/17.

## 0. Why R12 is a separate stage (architecture)

The established pattern in this codebase is **one stage, one gate** (`r1_gate`…`r11_gate`); R7 was a
separate cumulative stage over R6, R10 over R9, and R11 over R10. R12 follows that pattern exactly:

- `code/pipeline/r12_severity_litcurate.py` takes the **R11 registry** as its base (it requires the
  `R11_litcurate3` pass to be present), reads its **own** round-4 CSVs, tags `R12_litcurate4`, and writes
  the four registry artifacts. It **imports R11's helpers** (`derive_tier`, `is_spectrum`, `load_pinned`,
  the R3 bindings, …), which in turn import R10's, which import R9's, so the locked tier/spectrum/decline
  logic **cannot drift**.
- `code/pipeline/r12_litcurate_fetch.py` pins the round-4 cited articles via R9's exact fetch logic
  (re-exposed through R10 and R11). Four PMCIDs pinned, all open-access; one (PMC13090637) was already in
  the cache from R11's Hurler decline and is re-found byte-identical.
- `code/pipeline/r12_gate.py` re-proves the chain (r5→r12, 2×) **and** proves **all six** prior recorded
  CSVs — R9's `severity_litcurate_join.csv` / `severity_litcurate_excluded.csv`, R10's
  `severity_litcurate2_join.csv` / `severity_litcurate2_excluded.csv`, and R11's
  `severity_litcurate3_join.csv` / `severity_litcurate3_excluded.csv` — are **byte-identical** to their
  recorded digests (`prior_round_artifacts_preserved`). R12 is strictly **additive**.

## 1. The two lifts (cited, frozen-R3-derived, non-spectrum)

R12 makes **two severity lifts** — one VALUE+GRADE that completes an order-lock, one grade-only that
honestly does not.

| disease | axis | before | after | cited OA source | frozen-R3 tier | locks? |
|---|---|---|---|---|---|---|
| **Duchenne muscular dystrophy** (C0013264) | S | 0.50 `[H]` | **0.75 `[L]`** | PMC13205412 (PMID 42194990) | 0.75 (severe/debilitating, via `severe`; non-spectrum) | **YES** — 5th order-lock |
| **Tyrosinemia type I** (C0268490) | S | 0.75 `[H]` | **0.75 `[L]`** | PMC12844047 (PMID 41590629) | 0.75 (severe/debilitating, via `severe`; non-spectrum) | no (grade-only) |

**Duchenne MD — VALUE+GRADE, completes the 5th lock.**
- The cited sentence — *"Introduction Duchenne muscular dystrophy (DMD) is a severe, progressive
  neuromuscular disorder characterized by the gradual deterioration and weakening of skeletal and cardiac
  muscle tissue [1]."* — is a **disease-level, non-comparative, non-spectrum** statement defining DMD
  itself. Frozen R3 `first_match` over `PATTERNS["S_severity"]` maps it to tier **0.75** via `severe`;
  `is_spectrum` = False.
- The dominant untreated sequela is progressive skeletal- and cardiac-muscle degeneration leading to loss
  of ambulation and respiratory/cardiac failure — the obligate, prognosis-determining course.
- **Why it locks.** DMD's other four axes were **already** registry-`[L]` in the R11 base: onset 0.70 `[L]`
  (R6), progression 0.50 `[L]` (the R9 grade lift), mortality 0.70 `[L]`, disability 0.75 `[L]` (the R7 GBD
  lift). So lifting severity to `[L]` makes **every one of all five axes `[L]`** → `order_locked`. DMD is
  the **only** cohort disease with **all five axes scored AND every one registry-grade `[L]`**.
  `raw_burden` 0.630 → 0.680; residual `burden_score` 0.476 (× R_treat 0.70).

**Tyrosinemia type I — grade-only, does NOT lock (honest).**
- The cited sentence — *"Background/Objectives: Tyrosinemia type 1 (HT-1) is a treatable inherited disorder
  characterized by disrupted tyrosine metabolism, leading to severe liver, renal, and occasionally
  neurological dysfunction."* — is disease-level and non-spectrum; frozen R3 maps it to tier **0.75** via
  `severe`, the **same** value HT-1's severity already carried, so this is a **grade-only** corroboration
  (`[H]`→`[L]`, `raw_burden` unchanged).
- **Why it does not lock.** HT-1 retains onset 0.70 `[H]` and mortality 1.00 `[H]` (and progression /
  disability `[O]`, not guessed), so it stays **placed-but-unlocked**. Lifting one axis's *grade* does not
  manufacture a lock when other scored axes remain `[H]` — recorded honestly, not forced.

## 2. The two declines (recorded, never lifted)

Each considered-but-declined statement was **found and verbatim-pinned** in the OA cache, then
**scope-disqualified** under the frozen R9 rule. Recorded with a fixed-vocabulary `decline_class` and a
per-disease reason in `methodology/severity_litcurate4_excluded.csv`; the gate re-finds each verbatim.

| disease | axis | class | why not lifted |
|---|---|---|---|
| **Hurler syndrome** (C0086795) | S | `comparative` | the retrievable OA disease-level severity framing defines Hurler **AS** *"the severe phenotype"* of mucopolysaccharidosis type I in explicit contrast to the *"attenuated"* forms (Hurler-Scheie, Scheie). Frozen R3 pattern-matches `severe` to tier 0.75, but the word is the **phenotype-CLASS label** distinguishing Hurler from the milder MPS I forms (severe-vs-attenuated within the MPS I spectrum), not a clean disease-level magnitude for Hurler's own dominant untreated sequela; the only other retrievable `severe` in the dedicated MPS I-H burden paper (*"Severe manifestations can include organ failure, cognitive impairments, and shortened lifespan"*) is a property of the MPS **disorder class** generally (PMC13090637 / PMID 42004902) |
| **Beta-thalassemia HBB/LCRB** (CN322236) | S | `umbrella_spectrum` | the retrievable OA severity framing is an **umbrella spectrum** ranging from asymptomatic (thalassemia silent and minor) through thalassemia intermedia to transfusion-dependent **β-thalassemia major** (*"severe anemia ... lifelong transfusions and oral iron chelation"*). The disease-level magnitude is genotype/form-stratified across the silent-to-major continuum, and `severe` is explicitly attached to the **major** form, not the umbrella entity's own single dominant sequela; the frozen R3 **spectrum override trips** on this within-entity range, so a clean disease-level umbrella severity tier is not defensibly isolable (PMC13262897 / PMID 42201229) |

Both severities therefore stay `[H]`. Each is **re-litigable** — not §C(b)-permanent — only if a clean
disease-level (non-comparative, non-spectrum) OA severity magnitude for the entity's own dominant sequela
becomes retrievable.

## 2a. Frontier observation — Hemophilia A (honestly NOT forced into a decline)

**Hemophilia A** (C0019069) is a noted frontier, recorded as a `sub_phenotype` **observation** rather than
manufactured into the excluded CSV. The only retrievable OA `severe` framing is *"severe hemophilia A
(FVIII < 1%)"* — a **factor-activity sub-phenotype** label, i.e. a severity **stratum** defined by residual
clotting-factor level, not a disease-level magnitude for the entity's own dominant sequela. No clean
disease-level severity sentence was retrievable, so severity is left `[H]` and the case is logged as a
frontier observation. This keeps the decline CSV semantically clean (it records *considered disease-level
statements that were scope-disqualified*, not factor-stratum labels that were never disease-level to begin
with) — the "lift only where defensible; decline transparently; never fish for a lock" discipline applied
to the boundary between a disease-level magnitude and a within-disease severity stratum. Hemophilia A's
severity is liftable only if a disease-level (not factor-stratum) OA magnitude becomes retrievable.

## 3. Net effect — honest

- **One new order-lock.** The lock set grows **4 → 5**: Achondrogenesis type II (C0220685), Niemann-Pick
  disease type A (C0268242), Tyrosinemia type II (C0268487), Marfan syndrome (C0024796), **+ Duchenne
  muscular dystrophy (C0013264)**. The single added lock is exactly Duchenne MD, completed by its severity
  `[H]`→`[L]` (gate check `new_order_lock_is_duchenne` proves the set grows by exactly DMD, with
  onset/progression/mortality/disability already `[L]`). No lock removed. DMD is the only cohort disease
  with all five axes scored and every one registry-`[L]`.
- **No new placement.** R12 adds zero diseases to the placed order — the DMD lift completes a lock for a
  disease that was already placed; HT-1 was already placed (grade-only); the Hurler and Beta-thalassemia
  entities stay where they were (severity unlifted).
- **Severity coverage after R12:** `{[O]: 11, [H]: 18, [L]: 6}` (the 6 `[L]` = Achondrogenesis II, NPD-A,
  Tyrosinemia II, Marfan, **Duchenne MD, Tyrosinemia type I**). Progression coverage is unchanged at
  `{[O]: 21, [L]: 9, [H]: 5}`; onset/mortality/disability byte-identical to R11.
- **Unmet-need surface CHANGED** (sha `bc5ae3db6967` → `ec01978d5919`): R12 raises Duchenne MD's
  `raw_burden`, so its residual `burden_score` moves. The **headline rule is unaffected** — DMD carries a
  treatment offset (R_treat 0.70), so it is not a "no disease-directed therapy" headline disease; the
  headline stays Achondrogenesis type II + Niemann-Pick type A.

## 4. Gates and verification

- `r12_gate.py` **PASS (16/16)**: determinism (r5→r12, 2×); banked unchanged; cumulative-over-R11; round-4
  join re-anchored + tier-from-frozen-R3 + non-spectrum; cut-points a-priori; round-4 declines recorded;
  add-only no-downgrade vs R11; S/P-only changed only for the 2 round-4 joined diseases (O/M/D
  byte-identical to R11); **exactly one new order-lock = Duchenne MD** (set grows 4→5, completed by S
  `[H]`→`[L]`, onset/progression/mortality/disability already `[L]`, no lock removed); raw_burden
  re-derived; rankability; residual; order-lock rule + sensitivity (equal ρ=1.0); round-4 sources
  open-access + source-bound; **`prior_round_artifacts_preserved`** (all six R9+R10+R11 join/excluded CSVs
  byte-identical to their recorded digests); engine pin drift 0. `reports/r12.gate.json`.
- All prior gates still green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 ·
  R7 16/16 · R8 16/16 · R9 15/15 · R10 16/16 · R11 16/16 · unmet-need 6/6 · W1 site 17/17 · boundary 6/6.
  Engine pin `MANIFEST_governed.sha256` verifies OK (drift 0, 15/15).

Reproduce from the package root:

```
python3 code/pipeline/r5_accession_apply.py
python3 code/pipeline/r6_naturalhistory_registry.py
python3 code/pipeline/r7_naturalhistory_registry2.py
python3 code/pipeline/r8_severity_registry.py
python3 code/pipeline/r9_severity_litcurate.py
python3 code/pipeline/r10_severity_litcurate.py
python3 code/pipeline/r11_severity_litcurate.py
python3 code/pipeline/r12_severity_litcurate.py    # registry-set sha 8c5dbae815f7
python3 code/pipeline/r9_gate.py                     # PASS 15/15
python3 code/pipeline/r10_gate.py                    # PASS 16/16
python3 code/pipeline/r11_gate.py                    # PASS 16/16
python3 code/pipeline/r12_gate.py                    # PASS 16/16
python3 code/pipeline/w_unmet_need_surface.py
python3 code/pipeline/w_unmet_need_gate.py           # PASS 6/6  (surface sha ec01978d5919)
python3 tools/w1_build.py                            # site-set sha c5dd896d4fe6
python3 tools/w1_gate.py                             # PASS 17/17
```

(Each gate is self-healing and leaves the registry at **its own** stage, so after running `r9_gate`,
`r10_gate` or `r11_gate` re-run the full r5→r12 chain before inspecting the registry at R12.)

## 5. Handover → R13

The curated-PMC-OA frontier now has **16 placed diseases still carrying an `[H]` axis** — overwhelmingly
**severity** (the cohort-wide open axis after R12). Obstacle-bound / frontier entities to **not**
re-litigate unless a clean disease-level OA magnitude becomes retrievable:

- **Hb SS disease** (progression + severity) and **Alpha-1-antitrypsin deficiency** (progression) —
  umbrella/genotype-scoped or spectrum, recorded as permanent §C(b) obstacles.
- **Gaucher disease type I** and **Gaucher disease (umbrella)** severities — declined `comparative` at R11
  (`severity_litcurate3_excluded.csv`); re-litigable only on a clean non-comparative disease-level
  magnitude.
- **Hurler syndrome** severity (comparative phenotype-class label) and **Beta-thalassemia** severity
  (umbrella spectrum) — declined at R12 (`severity_litcurate4_excluded.csv`); re-litigable only on a clean
  non-comparative/non-spectrum disease-level magnitude.
- **Hemophilia A** severity — only the factor-stratum sub-phenotype framing is retrievable; liftable only
  on a disease-level (not factor-stratum) magnitude.

**R13** continues the **same rule** on the placed cohort's remaining `[H]`/`[O]` **severity** /
**progression** (and any further **mortality**) axes, lifting only where a cited disease-level OA magnitude
for the dominant untreated sequela maps to a frozen-R3 tier, **non-spectrum and non-comparative**.
**Implement R13 as a new cumulative stage** (`r13_*` + `r13_gate`) over the R12 registry — its own
`severity_litcurate5_*` CSVs, its own fetch+pin, leaving all prior artifacts byte-identical — per the
established one-stage-one-gate pattern. The OMIM clinical-synopsis path stays **removed** (key unobtainable
for an individual researcher), not deferred. The forward plan is carried in the whitepaper (site §1
`#forward`) and `FUTURE_WORK.md` until a dated completion declaration (§C) replaces it.
