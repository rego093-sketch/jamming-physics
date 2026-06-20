# R11 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.13, phase R11)

Phase R11 is **round 3** of the curated **PMC open-access** severity/progression lift R9 opened. It uses
the **same a-priori rule** and the **same frozen R3 tier function** (the tier is *derived* from the
verbatim cited sentence, never hand-asserted), and it is implemented as a **dedicated cumulative stage
over R10** so that every R9 **and** R10 artifact — and their recorded registry-set shas
(**d07a544475dc**, **e77c0bf0e887**) — stays **byte-identical and immutable**. Single author (Young Jae
Lee, ORCID 0009-0002-7535-8245). English deliverables, VP-SPEC v1.8 discipline (no-tuning,
bit-reproducible, honest grading `[O]<[H]<[L]<[V]`). All gates green; engine pin drift 0.

The R3/R4 BANKED files stay byte-identical (gate-verified); the cumulative registry layer
**R5+R6+R7+R8+R9+R10+R11** is what advances. Registry-set sha **32cf48334233** (2× identical); unmet-need
surface sha **bc5ae3db6967** — **CHANGED** this round (unlike R10), because R11 raises Marfan's
`raw_burden` (0.5125 → 0.575), so the residual `burden_score` values and the residual ranking move; W1
site-set sha **06952f4af84e** (2× identical), W1 gate 17/17.

## 0. Why R11 is a separate stage (architecture)

The established pattern in this codebase is **one stage, one gate** (`r1_gate`…`r10_gate`); R7 was a
separate cumulative stage over R6, and R10 over R9. R11 follows that pattern exactly:

- `code/pipeline/r11_severity_litcurate.py` takes the **R10 registry** as its base (it requires the
  `R10_litcurate2` pass to be present), reads its **own** round-3 CSVs, tags `R11_litcurate3`, and writes
  the four registry artifacts. It **imports R10's helpers** (`derive_tier`, `is_spectrum`, `load_pinned`,
  the R3 bindings, …), which in turn import R9's, so the locked tier/spectrum/decline logic **cannot
  drift**.
- `code/pipeline/r11_litcurate_fetch.py` pins the round-3 cited articles via R9's exact fetch logic
  (re-exposed through R10).
- `code/pipeline/r11_gate.py` re-proves the chain (r5→r11, 2×) **and** proves **all four** prior recorded
  CSVs — R9's `severity_litcurate_join.csv` / `severity_litcurate_excluded.csv` and R10's
  `severity_litcurate2_join.csv` / `severity_litcurate2_excluded.csv` — are **byte-identical** to their
  recorded digests (`prior_round_artifacts_preserved`). R11 is strictly **additive**.

## 1. The single lift (cited, frozen-R3-derived, non-spectrum — VALUE+GRADE, completes a lock)

Unlike R10's two grade-only progression corroborations, R11's one lift is a **VALUE+GRADE severity** lift —
the first severity lift since R8, and the one that **completes an order-lock**.

| disease | axis | before | after | cited OA source | frozen-R3 tier | locks? |
|---|---|---|---|---|---|---|
| **Marfan syndrome** (C0024796) | S | 0.50 `[H]` | **0.75 `[L]`** | PMC13239629 (PMID 42229999) | 0.75 (severe/debilitating, via `life-threatening`; non-spectrum) | **YES** — 4th order-lock |

- The cited sentence — *"Introduction Marfan syndrome (MFS) is a systemic connective-tissue disorder
  caused by pathogenic variants in FBN1 , predisposing to progressive dilation of the aortic root,
  valvular dysfunction and life-threatening aortic dissection."* — is a **disease-level, non-comparative,
  non-spectrum** statement defining MFS itself. Frozen R3 `first_match` over `PATTERNS["S_severity"]` maps
  it to tier **0.75** via `life-threatening`; `is_spectrum` = False.
- The dominant untreated sequela is aortic-root dilatation progressing to dissection/rupture — the
  obligate, prognosis-determining, leading cause of premature death in untreated disease.
- **Why it locks.** Marfan's other scored axes were **already** registry-`[L]` in the R10 base: onset
  0.35 `[L]` (R6), progression 0.50 `[L]` (the R10 grade lift), mortality 0.70 `[L]`. Disability is the
  one unscored axis (`[O]`, no annotation — not guessed). So lifting severity to `[L]` makes **every scored
  axis `[L]`** (4/5) → `order_locked`. `raw_burden` 0.5125 → 0.575; residual `burden_score` 0.25875
  (× R_treat 0.45).

## 2. The two declines (recorded, never lifted)

Each considered-but-declined statement was **found and verbatim-pinned** in the OA cache, then
**scope-disqualified** under the frozen R9 rule. Recorded with a fixed-vocabulary `decline_class` and a
per-disease reason in `methodology/severity_litcurate3_excluded.csv`; the gate re-finds each verbatim.

| disease | axis | class | why not lifted |
|---|---|---|---|
| **Gaucher disease type I** (C1961835) | S | `comparative` | the only retrievable OA disease-level severity framing places GD1 as the **LEAST** severe of the three GD types (*"type 1 (GD1) being most common and having the least severe manifestations"*). Frozen R3 pattern-matches `severe` *inside* `least severe` to tier 0.75, but the statement is **comparative** — it characterises GD1 as the mild, non-neuronopathic end of the spectrum relative to types 2/3 — not a clean disease-level severe magnitude for GD1's own dominant sequela (PMC13254898 / PMID 42293157) |
| **Gaucher disease** (umbrella, C0017205) | S | `comparative` | the retrievable `devastating` magnitude is explicitly attributed to GD **type 3** (*"particularly devastating in GD type 3 (GD3)"*), the neuronopathic form, not the umbrella entity's own dominant sequela. Frozen R3 maps `devastating` to tier 1.0 and the heterogeneity wording does not trip the `spectrum_S` override, but the magnitude is **comparative** (singles out GD3) and the umbrella spans non-neuronopathic-to-neuronopathic forms, so no clean disease-level umbrella tier is defensibly isolable (PMC13045098 / PMID 41821052) |

**On the Gaucher declines specifically.** GD is the textbook case where a frozen-R3-mappable severity word
is present (`severe`, `devastating`) but is **comparative** rather than a disease-level magnitude for the
entity's own dominant sequela. Both Gaucher severities therefore stay `[H]`. They are **re-litigable** —
not §C(b)-permanent — only if a clean disease-level (non-comparative) OA severity magnitude for the
entity's own dominant sequela becomes retrievable.

## 3. Net effect — honest

- **One new order-lock.** The lock set grows **3 → 4**: Achondrogenesis type II (C0220685), Niemann-Pick
  disease type A (C0268242), Tyrosinemia type II (C0268487), **+ Marfan syndrome (C0024796)**. The single
  added lock is exactly Marfan, completed by its severity `[H]`→`[L]` (gate check
  `new_order_lock_is_marfan` proves the set grows by exactly Marfan, with onset/progression/mortality
  already `[L]`). No lock removed.
- **No new placement.** R11 adds zero diseases to the placed order — the lift completes a lock for a
  disease that was already placed; the two Gaucher entities stay where they were (severity unlifted).
- **Severity coverage after R11:** `{[O]: 11, [H]: 20, [L]: 4}` (the 4 `[L]` = Achondrogenesis II,
  NPD-A, Tyrosinemia II, Marfan). Progression coverage is unchanged at `{[O]: 21, [L]: 9, [H]: 5}`.
- **Unmet-need surface CHANGED** (sha `9aa184ff3dc2` → `bc5ae3db6967`): R11 raises Marfan's `raw_burden`,
  so its residual `burden_score` moves and its residual rank shifts (raw rank 19 → residual rank 20). The
  **headline rule is unaffected** — Marfan carries a treatment offset (R_treat 0.45), so it is not a "no
  disease-directed therapy" headline disease; the headline stays Achondrogenesis type II + Niemann-Pick
  type A.

## 4. Gates and verification

- `r11_gate.py` **PASS (16/16)**: determinism (r5→r11, 2×); banked unchanged; cumulative-over-R10; round-3
  join re-anchored + tier-from-frozen-R3 + non-spectrum; cut-points a-priori; round-3 declines recorded;
  add-only no-downgrade vs R10; S/P-only changed only for the 1 round-3 joined pair (O/M/D byte-identical
  to R10); **exactly one new order-lock = Marfan** (set grows 3→4, completed by S `[H]`→`[L]`,
  onset/progression/mortality already `[L]`, no lock removed); raw_burden re-derived; rankability;
  residual; order-lock rule + sensitivity (equal ρ=1.0); round-3 sources open-access + source-bound;
  **`prior_round_artifacts_preserved`** (all four R9+R10 join/excluded CSVs byte-identical to their
  recorded digests); engine pin drift 0. `reports/r11.gate.json`.
- All prior gates still green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 ·
  R7 16/16 · R8 16/16 · R9 15/15 · R10 16/16 · unmet-need 6/6 · W1 site 17/17. Engine pin
  `MANIFEST_governed.sha256` verifies OK (drift 0, 15/15).

Reproduce from the package root:

```
python3 code/pipeline/r5_accession_apply.py
python3 code/pipeline/r6_naturalhistory_registry.py
python3 code/pipeline/r7_naturalhistory_registry2.py
python3 code/pipeline/r8_severity_registry.py
python3 code/pipeline/r9_severity_litcurate.py
python3 code/pipeline/r10_severity_litcurate.py
python3 code/pipeline/r11_severity_litcurate.py    # registry-set sha 32cf48334233
python3 code/pipeline/r9_gate.py                     # PASS 15/15
python3 code/pipeline/r10_gate.py                    # PASS 16/16
python3 code/pipeline/r11_gate.py                    # PASS 16/16
python3 code/pipeline/w_unmet_need_surface.py
python3 code/pipeline/w_unmet_need_gate.py           # PASS 6/6  (surface sha bc5ae3db6967)
python3 tools/w1_build.py                            # site-set sha 06952f4af84e
python3 tools/w1_gate.py                             # PASS 17/17
```

(Each gate is self-healing and leaves the registry at **its own** stage, so after running `r9_gate` or
`r10_gate` re-run the full r5→r11 chain before inspecting the registry at R11.)

## 5. Handover → R12

The curated-PMC-OA frontier now has **17 placed diseases still carrying an `[H]` axis** — overwhelmingly
**severity** (the cohort-wide open axis after R11). Two entities are progression/severity obstacle-bound
(Hb SS disease, Alpha-1-antitrypsin deficiency — umbrella/genotype-scoped or spectrum), and the two
Gaucher severities are declined as comparative (re-litigable, not permanent). **R12** continues the **same
rule** on the placed cohort's remaining `[H]`/`[O]` **severity** / **progression** (and any further
**mortality**) axes, lifting only where a cited disease-level OA magnitude for the dominant untreated
sequela maps to a frozen-R3 tier, **non-spectrum and non-comparative**. **Implement R12 as a new cumulative
stage** (`r12_*` + `r12_gate`) over the R11 registry — its own `severity_litcurate4_*` CSVs, its own
fetch+pin, leaving all prior artifacts byte-identical — per the established one-stage-one-gate pattern. The
OMIM clinical-synopsis path stays **removed** (key unobtainable for an individual researcher), not
deferred. The forward plan is carried in the whitepaper (site §1 `#forward`) and `FUTURE_WORK.md` until a
dated completion declaration (§C) replaces it.
