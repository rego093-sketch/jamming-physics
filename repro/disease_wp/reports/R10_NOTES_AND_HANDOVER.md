# R10 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.12, phase R10)

Phase R10 is **round 2** of the curated **PMC open-access** progression/severity lift R9 opened. It uses
the **same a-priori rule** and the **same frozen R3 tier function** (the tier is *derived* from the
verbatim cited sentence, never hand-asserted), and it is implemented as a **dedicated cumulative stage
over R9** so that every R9 artifact — and R9's recorded registry-set sha **d07a544475dc** — stays
**byte-identical and immutable**. Single author (Young Jae Lee, ORCID 0009-0002-7535-8245). English
deliverables, VP-SPEC v1.8 discipline (no-tuning, bit-reproducible, honest grading `[O]<[H]<[L]<[V]`).
All gates green; engine pin drift 0.

The R3/R4 BANKED files stay byte-identical (gate-verified); the cumulative registry layer
**R5+R6+R7+R8+R9+R10** is what advances. Registry-set sha **e77c0bf0e887** (2× identical); unmet-need
surface sha **9aa184ff3dc2** — **unchanged**, because R10 is grade-only and the residual `burden_score`
values do not move; W1 site-set sha **3b0ebe982945** (2× identical), W1 gate 17/17.

## 0. Why R10 is a separate stage (architecture)

R9's in-package note sketched "add rows to `severity_litcurate_join.csv` and re-run `r9`." That one-liner
was shorthand. Following it literally would **overwrite R9's recorded artifacts** (its "2 lifts + 5
declines" description and its registry-set sha `d07a544475dc`) and destroy the historical record. The
established pattern in this codebase is **one stage, one gate** (`r1_gate`…`r9_gate`), and **R7 was already
a separate cumulative stage over R6** (`r7_naturalhistory_registry2.py`). R10 follows that pattern:

- `code/pipeline/r10_severity_litcurate.py` takes the **R9 registry** as its base (it requires the
  `R9_litcurate_severity_progression` pass to be present), reads its **own** round-2 CSVs, tags
  `R10_litcurate2`, and writes the four registry artifacts. It **imports R9's frozen helpers**
  (`derive_tier`, `is_spectrum`, `load_pinned`, the R3 bindings, …) so the locked logic **cannot drift**.
- `code/pipeline/r10_litcurate_fetch.py` pins the round-2 cited articles via R9's exact fetch logic.
- `code/pipeline/r10_gate.py` re-proves the chain (r5→r10, 2×) **and** proves R9's recorded
  `severity_litcurate_join.csv` / `severity_litcurate_excluded.csv` are **byte-identical** to their R9
  digests (`r9_artifacts_preserved`) — i.e. R10 is strictly **additive**.

## 1. The two lifts (cited, frozen-R3-derived, non-spectrum — GRADE-ONLY)

Both are **grade-only corroborations**: the progression *value* was already 0.5; R10 lifts its **grade**
from `[H]` (definition-grade inference) to `[L]` (registry-grade, literature-anchored). Neither changes
`raw_burden`, and **neither order-locks**.

| disease | axis | before | after | cited OA source | frozen-R3 tier | locks? |
|---|---|---|---|---|---|---|
| **Fabry disease** (C0002986) | P | 0.5 `[H]` | **0.5 `[L]`** | PMC9967779 (PMID 37259462) | 0.5 (`\bprogressive\b`, non-spectrum) | **No** — S 0.5 `[H]` + M 0.7 `[H]` remain |
| **Marfan syndrome** (C0024796) | P | 0.5 `[H]` | **0.5 `[L]`** | PMC9772687 (PMID 36543362) | 0.5 (non-spectrum) | **No** — S 0.5 `[H]` remains |

- **Fabry**: the cited sentence — *"FD is a progressive, multisystemic disease requiring early clinical
  recognition by clinicians to avoid life-threatening complications of renal failure, heart failure,
  arrhythmias, and stroke."* — is a disease-level progression statement; frozen R3 `first_match` maps it
  to tier 0.5 via `\bprogressive\b`, `is_spectrum` = False. Fabry keeps two `[H]` axes, so it does not
  lock.
- **Marfan**: the cited sentence — *"Aortic involvement is generally progressive, and with a growing
  aortic root diameter, the risk of dissection increases."* — is a disease-level progression statement
  for the obligate dominant sequela (aortic root dilatation → dissection); tier 0.5, non-spectrum. Marfan
  keeps S `[H]`, so it does not lock.

No secondary "corroborating" PMCIDs are asserted in the basis text: each row cites **only** the primary
verified sentence plus the dominant-sequela clinical reasoning. (Two unverified secondary IDs that briefly
appeared in draft basis text were removed — no fabricated attributions.)

## 2. The three declines (recorded, never lifted)

Each considered-but-declined statement was **found and verbatim-pinned** in the OA cache, then
**scope-disqualified** under the frozen R9 rule. Recorded with a fixed-vocabulary `decline_class` and a
per-disease reason in `methodology/severity_litcurate2_excluded.csv`; the gate re-finds each verbatim.

| disease | axis | class | why not lifted |
|---|---|---|---|
| **Hb SS disease** (C0002895) | P | `umbrella_spectrum` | the cohort entity is the **specific homozygous-SS** genotype, but the only retrievable OA disease-level progression sentence is scoped to the **sickle cell disease umbrella** (SCD spans HbSS, HbSC, HbS/β-thal). Frozen R3 *would* map it to 0.5, but the magnitude is the umbrella's, not the HbSS entity's own dominant sequela (PMC12635507 / PMID 41281092) |
| **Hb SS disease** (C0002895) | S | `spectrum` | an OA source predicates wide within-entity variability ("varies widely … some … very severe … whereas others can go unnoticed until adulthood"); the R3 `spectrum_S` override **trips**, so a clean non-spectrum disease-level severe tier is not isolable (PMC3459630 / PMID 23049411) |
| **Alpha-1-antitrypsin deficiency** (C0221757) | P | `umbrella_spectrum` | progression is predicated as **genotype-dependent** ("varies by AATD genotype"), and the entity spans a genotype spectrum (PiZZ, PiSZ, rare) with **two distinct dominant sequelae** (pulmonary emphysema vs hepatic cirrhosis) whose untreated courses differ — no single disease-level tier defensible (PMC11843710 / PMID 39980299) |

**On the Hb SS progression decline specifically.** Both R9 accepted lifts (NPD-A, DMD) named the entity
*in the cited sentence*; R9's one umbrella decline was GSD-II. For HbSS, a **deliberate entity-specific OA
search** (`sickle cell an[ae]mia[Title] AND progressive`, PMC open-access, ~16 candidates fetched and
scanned) found **no entity-specific disease-level progression sentence** exposed in retrievable
open-access full text — entity-specific articles bury it in introductions not captured by `efetch`. So
the honest disposition is **decline over placement**: a frozen-R3-mappable sentence exists, but only at
umbrella scope. HbSS stays **not-placed** (its open axes: O 0.7 `[L]`, M 0.7 `[H]`).

These declines are now **permanent §C(b) obstacles**: Hb SS disease (P + S) and AATD (P) have only
umbrella/genotype-scoped or spectrum OA statements available, so they are recorded as open-data-irreducible
and are **not re-litigated** unless an entity-specific disease-level OA magnitude becomes retrievable.

## 3. Net effect — honest

- **No new order-lock.** The lock set is unchanged: **3/35** (Achondrogenesis type II C0220685,
  Niemann-Pick disease type A C0268242, Tyrosinemia type II C0268487). The two Fabry/Marfan `[H]`→`[L]`
  grade lifts do not lock because each disease retains an `[H]` severity (and, for Fabry, `[H]` mortality).
- **No new placement.** Hb SS disease and AATD remain not-placed (each scores < 3 of 5 axes at registry
  grade). R10 added zero diseases to the placed order.
- **Progression coverage after R10:** `{[O]: 21, [L]: 9, [H]: 5}` (the 9 `[L]` = R9's 7 + Fabry + Marfan).
  This is surfaced in the published prose as **R9+R10** provenance (framework page, `IRREPRODUCIBILITY_
  LEDGER.md`, `llms.txt`), not as R9 alone.
- **Unmet-need surface unchanged** (sha `9aa184ff3dc2`): R10 is grade-only, residual values do not move.

## 4. Gates and verification

- `r10_gate.py` **PASS (16/16)**: determinism (r5→r10, 2×); banked unchanged; cumulative-over-R9; round-2
  join re-anchored + tier-from-frozen-R3 + non-spectrum; cut-points a-priori; round-2 declines recorded;
  add-only no-downgrade vs R9; S/P-only changed only for the 2 round-2 joined pairs (O/M/D byte-identical
  to R9); **no new order-lock** (R9=3 → R10=3); raw_burden re-derived; rankability; residual; order-lock
  rule + sensitivity (equal ρ=1.0); round-2 sources open-access + source-bound; **`r9_artifacts_preserved`**
  (R9 join/excluded CSVs byte-identical to their recorded R9 digests); engine pin drift 0.
  `reports/r10.gate.json`.
- All prior gates still green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 ·
  R7 16/16 · R8 16/16 · R9 15/15 · unmet-need 6/6 · W1 site 17/17. Engine pin
  `MANIFEST_governed.sha256` verifies OK (drift 0, 15/15).

Reproduce from the package root:

```
python3 code/pipeline/r5_accession_apply.py
python3 code/pipeline/r6_naturalhistory_registry.py
python3 code/pipeline/r7_naturalhistory_registry2.py
python3 code/pipeline/r8_severity_registry.py
python3 code/pipeline/r9_severity_litcurate.py
python3 code/pipeline/r10_severity_litcurate.py     # registry-set sha e77c0bf0e887
python3 code/pipeline/r9_gate.py                     # PASS 15/15
python3 code/pipeline/r10_gate.py                    # PASS 16/16
python3 code/pipeline/w_unmet_need_surface.py
python3 code/pipeline/w_unmet_need_gate.py           # PASS 6/6  (surface sha 9aa184ff3dc2)
python3 tools/w1_build.py                            # site-set sha 3b0ebe982945
python3 tools/w1_gate.py                             # PASS 17/17
```

## 5. Handover → R11

The curated-PMC-OA frontier has now been worked to the point where the **clearly defensible** disease-level
progression joins are exhausted (3 progression lifts; NPD-A locked; Fabry/Marfan grade-only) and two
entities are obstacle-bound (HbSS, AATD). **R11** continues the **same rule** on the placed cohort's
remaining `[H]`/`[O]` **severity** / **progression** (and any further **mortality**) axes, lifting only
where a cited disease-level OA magnitude for the dominant untreated sequela maps to a frozen-R3 tier,
non-spectrum. **Implement R11 as a new cumulative stage** (`r11_*` + `r11_gate`) over the R10 registry —
its own `severity_litcurate3_*` CSVs, its own fetch+pin, leaving all prior artifacts byte-identical — per
the established one-stage-one-gate pattern. The OMIM clinical-synopsis path stays **removed** (key
unobtainable for an individual researcher), not deferred. The forward plan is carried in the whitepaper
(site §1 `#forward`) and `FUTURE_WORK.md` until a dated completion declaration (§C) replaces it.
