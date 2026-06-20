# R13 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.15, phase R13)

Phase R13 is **round 5** of the curated **PMC open-access** severity/progression lift R9 opened. It uses
the **same a-priori rule** and the **same frozen R3 tier function** (the tier is *derived* from the
verbatim cited sentence, never hand-asserted), and it is implemented as a **dedicated cumulative stage
over R12** so that every R9, R10, R11 **and** R12 artifact — and their recorded registry-set shas
(**d07a544475dc**, **e77c0bf0e887**, **32cf48334233**, **8c5dbae815f7**) — stays **byte-identical and
immutable**. Single author (Young Jae Lee, ORCID 0009-0002-7535-8245). English deliverables, VP-SPEC v1.8
discipline (no-tuning, bit-reproducible, honest grading `[O]<[H]<[L]<[V]`). All gates green; engine pin
drift 0.

The R3/R4 BANKED files stay byte-identical (gate-verified); the cumulative registry layer
**R5+R6+R7+R8+R9+R10+R11+R12+R13** is what advances. Registry-set sha **49af5f824afa** (2× identical);
unmet-need surface sha **8c5643c21efd** — **CHANGED** this round (like R11 and R12, unlike R10), because
R13 raises Maple syrup urine disease's `raw_burden` (0.667 → 0.750), so the residual `burden_score` values
and the residual ranking move; W1 site-set sha **98ac7c62bcef** (2× identical), W1 gate 17/17.

## 0. Why R13 is a separate stage (architecture)

The established pattern in this codebase is **one stage, one gate** (`r1_gate`…`r12_gate`); R7 was a
separate cumulative stage over R6, R10 over R9, R11 over R10, and R12 over R11. R13 follows that pattern
exactly:

- `code/pipeline/r13_severity_litcurate.py` takes the **R12 registry** as its base (it requires the
  `R12_litcurate4` pass to be present), reads its **own** round-5 CSVs, tags `R13_litcurate5`, and writes
  the four registry artifacts. It **imports R12's helpers** (`derive_tier`, `is_spectrum`, `load_pinned`,
  the R3 bindings, …), which in turn import R11's, R10's and R9's, so the locked tier/spectrum/decline
  logic **cannot drift**.
- `code/pipeline/r13_litcurate_fetch.py` pins the round-5 cited articles via R9's exact fetch logic
  (re-exposed through R10, R11 and R12). Five PMCIDs pinned, all open-access (PMC12861732, PMC13110062,
  PMC13142844, PMC13266223, PMC13089801).
- `code/pipeline/r13_gate.py` re-proves the chain (r5→r13, 2×) **and** proves **all eight** prior recorded
  CSVs — R9's, R10's, R11's and R12's `severity_litcurate{,2,3,4}_join.csv` / `*_excluded.csv` — are
  **byte-identical** to their recorded digests (`prior_round_artifacts_preserved`). R13 is strictly
  **additive**.

## 1. The three lifts (cited, frozen-R3-derived, non-spectrum) — none completes a lock

R13 makes **three lifts** — one VALUE+GRADE severity lift and two grade-only progression corroborations.
**Not one of them order-locks**, because each disease retains an `[H]` on another scored axis. This is the
honest shape of round 5: defensible grade evidence added, no lock manufactured.

| disease | axis | before | after | cited OA source | frozen-R3 tier | locks? |
|---|---|---|---|---|---|---|
| **Maple syrup urine disease** (C0024776) | S | 0.50 `[H]` | **0.75 `[L]`** | PMC12861732 (PMID 41635633) | 0.75 (severe/debilitating, via `life-threatening`; non-spectrum) | no — retains onset `[H]` |
| **Cystic fibrosis** (C0010674) | P | 0.50 `[H]` | **0.50 `[L]`** | PMC13110062 (PMID 42039762) | 0.50 (progressive course, via `progressive`; non-spectrum) | no — retains mortality `[H]` |
| **Glycogen storage disease, type II** / Pompe (C0017921) | P | 0.50 `[H]` | **0.50 `[L]`** | PMC13142844 (PMID 40261290) | 0.50 (progressive course, via `progressive`; non-spectrum) | no — retains mortality `[H]` |

**Maple syrup urine disease — VALUE+GRADE severity lift, does NOT lock.**
- The cited sentence — *"Maple syrup urine disease (MSUD, OMIM # 248600 ) is a life-threatening metabolic
  disorder caused by biallelic pathogenic variants in the BCKDHA , BCKDHB, DBT , and DLD genes, which
  encode the E1α, E1β, E2 and E3 subunits (respectively) of the branched-chain amino acid (BCKD) enzyme
  complex [ 11 , 12 ]."* — is a **disease-level, non-comparative, non-spectrum** statement defining MSUD
  itself. Frozen R3 `first_match` over `PATTERNS["S_severity"]` maps it to tier **0.75** via
  `life-threatening` (the `[L]`-tier severity vocabulary), with no higher-tier qualifier preceding it;
  `is_spectrum` = False.
- The dominant untreated sequela is acute neonatal branched-chain amino-acid (especially leucine)
  intoxication — metabolic encephalopathic crisis with cerebral edema — the obligate, prognosis-determining
  course and cause of neonatal death or permanent neurological injury.
- **Why it does NOT lock.** MSUD's onset is 1.00 `[H]` and its progression and mortality are unscored
  `[O]` (not guessed). Lifting severity to `[L]` resolves the prior `[H]` severity-midpoint to MSUD's own
  severe magnitude but leaves onset `[H]`, so MSUD stays **placed-but-unlocked**. This is a severity
  coverage + raw_burden advance only: `raw_burden` 0.667 → 0.750; residual `burden_score` 0.300 → 0.3375
  (× R_treat 0.45).

**Cystic fibrosis — grade-only progression corroboration, does NOT lock.**
- The cited sentence — *"Cystic fibrosis (CF) is a progressive genetic disease characterized by defective
  ion transport, mucus accumulation, chronic infection, and inflammation that drive airway damage and
  ultimately end-stage lung failure."* — is disease-level and non-spectrum; frozen R3 maps it to tier
  **0.50** via `progressive`, the **same** value CF's progression already carried, so this is a
  **grade-only** corroboration (`[H]`→`[L]`, `raw_burden` unchanged).
- The dominant untreated sequela is chronic progressive obstructive lung disease culminating in end-stage
  respiratory failure.
- **Why it does NOT lock.** CF retains mortality 0.70 `[H]` (and severity / disability `[O]`), so it stays
  placed-but-unlocked.

**Glycogen storage disease type II (Pompe) — grade-only progression corroboration, does NOT lock.**
- The cited sentence — *"Pompe disease is a rare neuromuscular disorder caused by acid alpha-glucosidase
  deficiency, leading to glycogen accumulation and progressive striated muscle weakness."* — is the
  **umbrella disease-level** statement defining Pompe disease itself; the form-specific
  (infantile-onset-is-more-severe / late-onset-is-slowly-progressive) framings in the same article are
  comparative or form-stratified and were **NOT** used. Frozen R3 maps it to tier **0.50** via
  `progressive`, the same value Pompe's progression already carried — a **grade-only** corroboration
  (`[H]`→`[L]`, `raw_burden` unchanged).
- The dominant untreated sequela is progressive lysosomal-glycogen myopathy (progressive striated skeletal
  and respiratory muscle weakness) across the disease entity.
- **Why it does NOT lock.** Pompe retains mortality 1.00 `[H]`, so it stays placed-but-unlocked.

## 2. The two declines (recorded, never lifted)

Each considered-but-declined statement was **found and verbatim-pinned** in the OA cache, then
**scope-disqualified** under the frozen R9 rule. Recorded with a fixed-vocabulary `decline_class` and a
per-disease reason in `methodology/severity_litcurate5_excluded.csv`; the gate re-finds each verbatim.

| disease | axis | class | why not lifted |
|---|---|---|---|
| **Osteogenesis imperfecta** (C0029434) | S | `comparative` | the retrievable OA disease-level severity framing — *"Severe osteogenesis imperfecta is often diagnosed earlier than milder disease."* — uses `severe` as the **Sillence phenotype-CLASS label** distinguishing severe OI (type III / perinatally-lethal type II) from *"milder disease"* (type I), in explicit contrast, not a clean disease-level magnitude for the umbrella entity's own dominant untreated sequela (heritable bone fragility / recurrent fractures). OI severity is Sillence-type-stratified across a mild-to-perinatally-lethal range; frozen R3 pattern-matches `severe` to tier 0.75, but the word is a within-entity phenotype-class label, not an isolable disease-level magnitude (PMC13266223 / PMID 42305572) |
| **alpha Thalassemia** (C0002312) | S | `umbrella_spectrum` | the retrievable OA severity framing — *"Clinical presentation can vary widely in severity from resulting in stillbirth to being asymptomatic, correlating with the number of functional alpha globin genes inherited."* — is an **umbrella spectrum**, gene-dosage-stratified from asymptomatic (silent carrier / one affected gene) through HbH disease to fatal Hb Bart's hydrops fetalis (stillbirth, all four genes). The disease-level magnitude is genotype-stratified across the asymptomatic-to-lethal continuum, so a clean disease-level magnitude for the umbrella entity's own single dominant sequela is not isolable; the frozen R3 **spectrum override trips** on this within-entity range (PMC13089801 / PMID 42004318) |

Both severities therefore stay `[H]`. Each is **re-litigable** — not §C(b)-permanent — only if a clean
disease-level (non-comparative, non-spectrum) OA severity magnitude for the entity's own dominant sequela
becomes retrievable.

## 2a. Frontier observations — Hemophilia B and Becker MD (honestly NOT forced into declines)

Mirroring R12's Hemophilia A handling, two further entities are recorded as **observations** rather than
manufactured into the excluded CSV, because their only retrievable `severe` framings were never
disease-level magnitudes to begin with:

- **Hemophilia B** (C0008533) — the only retrievable OA `severe` framing is a **factor-activity
  sub-phenotype** stratum (severe / moderate / mild by residual factor IX level), i.e. a severity stratum
  defined by clotting-factor level, not a disease-level magnitude for the entity's own dominant sequela.
  Severity left `[H]`; liftable only on a disease-level (not factor-stratum) OA magnitude.
- **Becker muscular dystrophy** (C0917713) — the only retrievable `severe` framing jointly groups Duchenne
  **and** Becker (the dystrophinopathy class), and BMD is characteristically **milder and more variable**
  than DMD with no isolable BMD-specific disease-level magnitude. Severity left `[H]`; liftable only on a
  clean BMD-specific disease-level magnitude.

This keeps the decline CSV semantically clean (it records *considered disease-level statements that were
scope-disqualified*, not factor-strata or class-grouped labels that were never disease-level) — the "lift
only where defensible; decline transparently; never fish for a lock" discipline applied to the boundary
between a disease-level magnitude and a within-disease severity stratum.

## 3. Net effect — honest

- **No new order-lock.** The lock set is **unchanged at 5**: Achondrogenesis type II (C0220685),
  Niemann-Pick disease type A (C0268242), Tyrosinemia type II (C0268487), Marfan syndrome (C0024796), and
  Duchenne muscular dystrophy (C0013264). The three R13 lifts each raise an axis grade `[H]`→`[L]` but
  **none completes a lock** — MSUD retains onset `[H]`, CF and Pompe each retain mortality `[H]` (gate
  check `no_new_order_lock` proves the set is unchanged with nothing added and nothing removed, and that
  each lift produces its `[H]`→`[L]` grade change without locking). The round adds defensible grade
  evidence without manufacturing a lock.
- **No new placement.** R13 adds zero diseases to the placed order — MSUD, CF and Pompe were already
  placed; the two declined entities (OI, alpha-Thalassemia) stay where they were (severity unlifted).
- **Severity coverage after R13:** `{[O]: 11, [H]: 17, [L]: 7}` (the 7 `[L]` = the prior 6 +
  **Maple syrup urine disease**). **Progression coverage after R13:** `{[O]: 21, [L]: 11, [H]: 3}` (the
  11 `[L]` = the prior 9 + **Cystic fibrosis** + **Glycogen storage disease type II**). Onset / mortality /
  disability byte-identical to R12.
- **Unmet-need surface CHANGED** (sha `ec01978d5919` → `8c5643c21efd`): R13 raises Maple syrup urine
  disease's `raw_burden`, so its residual `burden_score` moves. The **headline rule is unaffected** — MSUD,
  CF and Pompe each carry a treatment offset (R_treat 0.45), so none is a "no disease-directed therapy"
  headline disease; the headline stays Achondrogenesis type II + Niemann-Pick type A.

## 4. Gates and verification

- `r13_gate.py` **PASS (16/16)**: determinism (r5→r13, 2×); banked unchanged; cumulative-over-R12; round-5
  join re-anchored + tier-from-frozen-R3 + non-spectrum; cut-points a-priori; round-5 declines recorded;
  add-only no-downgrade vs R12; S/P-only changed only for the 3 round-5 joined diseases (O/M/D
  byte-identical to R12); **no new order-lock** (set unchanged R12=5 → R13=5, nothing added, nothing
  removed; the three lifts each raise grade `[H]`→`[L]` without completing a lock); raw_burden re-derived;
  rankability; residual; order-lock rule + sensitivity (equal ρ=1.0); round-5 sources open-access +
  source-bound; **`prior_round_artifacts_preserved`** (all eight R9+R10+R11+R12 join/excluded CSVs
  byte-identical to their recorded digests); engine pin drift 0. `reports/r13.gate.json`.
- All prior gates still green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 ·
  R7 16/16 · R8 16/16 · R9 15/15 · R10 16/16 · R11 16/16 · R12 16/16 · unmet-need 6/6 · W1 site 17/17 ·
  boundary 6/6. Engine pin `MANIFEST_governed.sha256` verifies OK (drift 0, 15/15).

Reproduce from the package root:

```
python3 code/pipeline/r5_accession_apply.py
python3 code/pipeline/r6_naturalhistory_registry.py
python3 code/pipeline/r7_naturalhistory_registry2.py
python3 code/pipeline/r8_severity_registry.py
python3 code/pipeline/r9_severity_litcurate.py
python3 code/pipeline/r10_severity_litcurate.py
python3 code/pipeline/r11_severity_litcurate.py
python3 code/pipeline/r12_severity_litcurate.py
python3 code/pipeline/r13_litcurate_fetch.py        # pins 5 round-5 PMC-OA articles (idempotent)
python3 code/pipeline/r13_severity_litcurate.py     # registry-set sha 49af5f824afa
python3 code/pipeline/r9_gate.py                     # PASS 15/15
python3 code/pipeline/r10_gate.py                    # PASS 16/16
python3 code/pipeline/r11_gate.py                    # PASS 16/16
python3 code/pipeline/r12_gate.py                    # PASS 16/16
python3 code/pipeline/r13_gate.py                    # PASS 16/16
python3 code/pipeline/w_unmet_need_surface.py
python3 code/pipeline/w_unmet_need_gate.py           # PASS 6/6  (surface sha 8c5643c21efd)
python3 tools/w1_build.py                            # site-set sha 98ac7c62bcef
python3 tools/w1_gate.py                             # PASS 17/17
```

(Each gate is self-healing and leaves the registry at **its own** stage, so after running `r9_gate`,
`r10_gate`, `r11_gate` or `r12_gate` re-run the full r5→r13 chain before inspecting the registry at R13.)

## 5. Handover → R14

The curated-PMC-OA frontier now has placed diseases still carrying an `[H]` axis — overwhelmingly
**severity** (the cohort-wide open axis after R13). Obstacle-bound / frontier entities to **not**
re-litigate unless a clean disease-level OA magnitude becomes retrievable:

- **Hb SS disease** (progression + severity) and **Alpha-1-antitrypsin deficiency** (progression) —
  umbrella/genotype-scoped or spectrum, recorded as permanent §C(b) obstacles.
- **Gaucher disease type I** and **Gaucher disease (umbrella)** severities — declined `comparative` at R11
  (`severity_litcurate3_excluded.csv`).
- **Hurler syndrome** severity (comparative phenotype-class label) and **Beta-thalassemia** severity
  (umbrella spectrum) — declined at R12 (`severity_litcurate4_excluded.csv`).
- **Osteogenesis imperfecta** severity (comparative Sillence phenotype-class label) and **alpha
  Thalassemia** severity (umbrella spectrum, stillbirth-to-asymptomatic) — declined at R13
  (`severity_litcurate5_excluded.csv`).
- **Hemophilia A** severity (R12), **Hemophilia B** severity (R13) — only factor-stratum sub-phenotype
  framing retrievable; liftable only on a disease-level (not factor-stratum) magnitude.
- **Becker muscular dystrophy** severity (R13) — only the dystrophinopathy-class-grouped `severe` is
  retrievable; liftable only on a clean BMD-specific disease-level magnitude.

**R14** continues the **same rule** on the placed cohort's remaining `[H]`/`[O]` **severity** /
**progression** (and any further **mortality**) axes, lifting only where a cited disease-level OA magnitude
for the dominant untreated sequela maps to a frozen-R3 tier, **non-spectrum and non-comparative**.
**Implement R14 as a new cumulative stage** (`r14_*` + `r14_gate`) over the R13 registry — its own
`severity_litcurate6_*` CSVs, its own fetch+pin, leaving all prior artifacts byte-identical — per the
established one-stage-one-gate pattern. The OMIM clinical-synopsis path stays **removed** (key unobtainable
for an individual researcher), not deferred. The forward plan is carried in the whitepaper (site §1
`#forward`) and `FUTURE_WORK.md` until a dated completion declaration (§C) replaces it.
