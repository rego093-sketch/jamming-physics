# Appendix K — the absolute clock: pinning the global zero-point from two measured anchors

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

Appendix J closed four obstacles the order grammar left open, but **halved the fourth on purpose**: it
converted the somite *cadence* to days via the measured segmentation clock (`O2`), yet left **one global
zero-point** — a single absolute origin pinning *every* gene to an absolute embryonic day — explicitly
`[O]`, because that needs a **second independently measured anchor** the cadence alone cannot supply.
**This appendix closes exactly that one piece (B1) — with a parameter-free two-anchor calibration validated
out of sample, no tuning.**

> **영점은 맞추는 것이 아니라 측정되는 것이다.** A zero-point is the single most tunable object in the whole
> timing claim — any origin can be slid to fit. So it is closed the *one* way that cannot be tuned: with
> **two anchors from two independent measurement modalities**, fixing a straight line `day(s) = a + b·s`
> with **zero free parameters**, and tested on **held-out** Carnegie stage-days and gene-days the anchors
> never touched. The clock is a **measurement**, graded `[L]` and **never `[V]`** — there is no substrate
> theorem that forces a zero-point. The gate fails closed if anyone promotes it.

This appendix is **add-only**: Appendices A–J and every prior number, grade, equation, and DOI are
unchanged. **Appendix K introduces NO new γ.** The four skeletal drivers shared with Appendices G/H
(**SOX9, RUNX2, PAX1, GLI3**) are re-locked **byte-for-byte**; **all 63 inherited driver-γ** are
gate-checked **byte-identical against the parent Appendix-J `param_db.json` read off disk** (`K1`, merging
J's 38-inherited + 25-new blocks into the full 63), proving the closure rides on the identical atlas.

---

## The one channel this appendix closes

| channel | Appendix J | Appendix K (this work) | grade |
|---|---|---|---|
| **B1** global zero-point | sub-clock `[L]`; one global zero-point **open** `[O]` (needs a 2nd anchor) | a **parameter-free two-anchor clock** pins it: held-out stage-days & 31 gene-days in the somite window reproduced **≤ 0.56 d**; honest CS14+ drift ≤ 6.56 d | `[O] → [L]` |

Everything else is **inherited from Appendix J and re-audited byte-for-byte on the identical 63-gene
atlas**: the filled cascade DAG (`K2`), the null (`K3`), edge concordance (`K4`), depth-beats-γ (`K5`), the
OR wavefront (`K6`) and quorum/AND threshold-k gate (`G1`), sequence-drive order-preservation (`O3`), the
O1 floor on the filled kit (`O1`) and its jitter band (`O1J`), and the segmentation sub-clock (`O2`).

### B1 — the two-anchor calibration (parameter-free)

`completion.timing.global_clock` builds a straight line from Carnegie stage number `s` to post-fertilization
day, with its **slope and intercept each supplied by a different real measurement** so that **nothing is
fitted**:

- **SLOPE — the segmentation modality (in vitro).** The human presomitic-mesoderm oscillator period
  **5.0 h** (Diaz-Cuadros 2020 *Nature* 580:113; Matsuda 2020 *Science* 369:1450) × cited **42** somite
  pairs (O'Rahilly & Müller) = **8.75 d** of somitogenesis, spread over the cited **CS9 → CS13** bracket
  (4 stages) ⇒ **b = 2.1875 d/stage**.
- **INTERCEPT — the cardiac modality (in vivo).** The first embryonic heart contraction is a **CS10** event
  at **22 ± 1 d** post-fertilization (O'Rahilly & Müller 1987 staging convention; Moore, Persaud & Torchia,
  *The Developing Human*, "22–23 d"; PMC9225347 "22 ± 1 d"). ⇒ **a = 22 − 2.1875×10 = 0.125 d**.

**Neither anchor consumes a tabulated stage-day**, so the cited Carnegie stage-day table and every gene's
onset day become **held-out** targets:

| held-out test | result | band |
|---|---|---|
| Carnegie **stage-days** in the somite window (CS8–13, the CS10 intercept excluded) | **5 stages, max err 0.562 d** | all within ±1.5 d |
| anchored **gene-days** in the somite window | **31 genes, max err 0.562 d** (worst TBX5) | all inside the band |
| cardiac anchor vs the tabulated CS10 day | **independently corroborates** | recorded, not fitted |

**Honest bound (reported, not hidden):** extended past somitogenesis, the *single* somite-derived rate
**drifts** — up to **6.56 d** at the latest stages (CS17 off 3.69 d) — because once the somite series is
complete the oscillator no longer sets the body's pace. The clock works precisely where its mechanism
applies and visibly fails where the mechanism stops, which is what a real mechanism does. Unifying the
somite and post-somite tempos into one *derived* rate law, and explaining the **origin** of the rates
(why ~5 h, why ~42), are **firewall-permanent ceilings** — magnitude/origin questions excluded exactly as
the absolute *strength* of the order prediction is (B3). The rates are used as **cited measurements** to
pin the zero-point; their origin is never claimed.

---

## Why this is a closure, not a fit — the locks

**1 · Inheritance is byte-exact, and K adds no γ.** `K1` proves the A4 `robust_z` operator is scale/shift
invariant to machine epsilon, the γ operator reproduces `−mean(NN ΔG)` on a probe, the four skeletal
drivers match byte-for-byte, **and all 63 inherited γ equal the parent Appendix-J `param_db` to the last
digit** (0 mismatches), its 38-inherited and 25-new blocks merged. Appendix K adds **0** new γ — it lays a
*measurement* over the identical atlas.

**2 · Zero free parameters.** `B1` checks that the calibration has `free_parameters == 0`, that the two
anchors come from **two different modalities**, and that the held-out stages **and** held-out genes both
land in band. A clock with a fitted origin would fail this check.

**3 · The clock is `[L]`, never `[V]`.** `B1` and `K11` both verify the global-clock grade **starts `[L]`
and is not `[V]`** — a measurement, not a substrate invariant. The `[V]`-detection tests the *grade prefix*,
so the honest phrase "never `[V]`" in the grade string cannot be mistaken for a `[V]` promotion.

**4 · Everything inherited still holds on the identical atlas.** `K2`–`K7`, `G1`, `O1`, `O1J`, `O2`, `O3`
re-run green byte-for-byte — filling no gap and moving no inherited number (the inherited-kit O1 scope still
reproduces **0.475**; the filled kit still **0.755**; the jitter p5 still **0.625**).

**5 · No false victory.** `K11`: the declaration closes B1 (the O2 global zero-point) to `[L]`, keeps the
absolute clock `[L]`, keeps O1 `[L]`, keeps the built body `[O]`, and holds **`physical_complete = False`**
— failing closed if `physical_complete` is ever True or the absolute clock or O1 is ever upgraded to `[V]`.

---

## §INHERIT — learn the inheritance discipline first (binding; read before adding anything)

> Every new session, collaborator, or appendix that extends this kit **must internalise the inheritance
> discipline below before adding a single line.** This section is **binding** and is carried, current, in
> every release. Skipping it is how a program silently drifts off its own substrate.

**1 · Inherited invariants (carry them byte-identical, never retune).** The substrate is fixed upstream and
is **not** yours to re-fit:

- R19 bistable switch `ds/dt = γs − s³ + h`; cusp geometry `spinodal = 2(γ/3)^1.5`, barrier `γ²/4`.
- The γ operator: `γ = −mean(SantaLucia-1998 nearest-neighbour ΔG)` over the real GRCh38 promoter window.
- The shape operator A4 = `robust_z` (`completion/seqtools.py`), identical at every grammatical level and
  to Appendices E–J **character-for-character**.
- **All 63 driver-γ inherited from Appendix J**, byte-identical. The four overlapping Appendix-G/H genes
  (**SOX9 1.459260, RUNX2 1.241556, PAX1 1.504372, GLI3 1.298352**) and the whole 63-γ table are
  gate-checked byte-for-byte against the **parent `param_db.json`** (`K1`, J's two γ-blocks merged). **K
  introduces no new γ.** If your edit changes any inherited γ, you have broken inheritance — **stop**.

**2 · Derivation-identity / core-subset invariance.** Laying the absolute clock over the atlas must **not**
move any inherited number. The inherited core is **byte-compared**, not re-derived loosely; `spinodal` and
the A4 operator are proven scale/shift invariant to machine epsilon inside the gate. The inherited-kit scope
of the O1 ablation **must keep reproducing 0.475**, the filled kit **0.755** — if the clock moved the
inherited core, that is a regression, not progress.

**3 · Sub-model regression (every lever must still fire).** Each mechanism keeps its falsifiable handle and
all must stay green together: the **null** (`K3`), **edge concordance** 0 inversions (`K4`),
**depth-beats-γ** (`K5`), the **OR wavefront** theorem (`K6`), the **quorum/AND wavefront** (`G1`),
**sequence-drive order-preservation** (`O3`), the **floor re-test on the filled kit** (`O1`) and its
**jitter band** (`O1J`), the **sub-clock consistency** (`O2`), and now the **two-anchor global clock**
(`B1`). The fail-closed gate `K1..K11` (with `B1`) runs them all; **exit 0 iff all pass**.

**4 · Source-verified citations (no magic numbers, no uncited biology).** Every regulatory edge is `[F]`
with a literature anchor (HOX 3′→5′ temporal collinearity, Izpisúa-Belmonte 1991 EMBO J 10:2279; limb FGF8
AER → FGF10 feedback, Ohuchi 1997 Development 124:2235; SOX9→RUNX2 then RUNX2→SP7, Zhou 2006 PNAS 103:19004
/ Nakashima 2002 Cell 108:17). Every Carnegie onset rank is `[L]` with a staging citation; every developmental
rate is `[L]` with a measurement citation; **the new cardiac zero-point anchor is `[L]` (CS10 @ 22 ± 1 d,
O'Rahilly & Müller 1987 / Moore-Persaud-Torchia)**. `param_db.json` carries `inline_magic_numbers: 0`; the
gate (`K8`) re-counts them — **including the absolute-clock config and the floor-robustness seed**. If you
cannot cite it, it is `[O]`, not `[V]`.

**The order of operations is fixed: LOCK → Derive → Gate.** Lock the inherited substrate and the cited
facts; derive the closures from them; let the gate refuse anything that retunes a constant, smuggles a magic
number, breaks an inherited byte, or upgrades an open claim to a victory. Then — and only then — extend.

---

## BLUEPRINT — the path to 100% completion (what would close the remaining `[O]`)

> This kit is **honestly incomplete**. Appendix K closes **B1** (the global zero-point, to `[L]`); it does
> **not** claim a derived cis→drive map, a jitter-robust strength, or a built body. The following is the
> binding roadmap for any future appendix — each item lists the **single thing** that is missing and the
> **grade it would earn** if closed under this discipline.

**B1 · O2 → a single absolute zero-point `[O] → [L]`. ✅ CLOSED (this appendix).** Two independently
measured anchors (the segmentation-oscillator slope + the first-heartbeat intercept) pin the global
zero-point with **zero free parameters**; the predicted absolute days for **held-out** stages and genes in
the somite-clock window land within the cited band. Graded `[L]` — a measurement, **never `[V]`**. *Residual,
disclosed as a ceiling, not a blocking `[O]`:* a single *derived* rate law unifying the somite and
post-somite tempos, and the **origin** of the rates.

**B2 · O3 → cis-code → drive *derived* from sequence `[F] → [L]`. ⬜ OPEN — next most rational.** *Missing:* a
real, cited promoter/enhancer → drive map (TF-motif occupancy, accessibility) so `h_i` is **read off the
sequence** rather than set to `√γ_parent` by choice. *Closes when:* the per-edge weight is computed from the
**measured** regulatory sequence and the firing order is reproduced — graded `[L]`, the modelling choice
retired.

**B3 · O1 → a logical-invariant strength claim — NOT pursued (permanent ceiling).** The absolute
depth↔Carnegie magnitude is an **empirical correlation on cited ranks**; it can be made *more robust* (B4)
but can **never** become `[V]` — there is no substrate theorem that forces a numerical strength. Any
appendix that grades O1 `[V]` is **wrong by construction** and the gate rejects it. The **origin of the
rates** (B1's residual) is a ceiling of the *same* kind.

**B4 · Coverage → shrink the jitter sensitivity `[L]` stays `[L]`, but stronger. ⬜ OPEN.** *Missing:* more of
the real cascade (additional limb/axial inducers, non-group-13 HOX with cited Carnegie ranks) so the p5
jitter edge rises above the floor. *Closes when:* `floor_retest_jitter` p5 ≥ floor on the enlarged cited
kit — still `[L]`, but no longer marginal (currently p5 **0.625**).

**B5 · Scope → a built / simulated organ `[O]`, out of scope.** This kit is a **principle demonstration on
real driver promoters, non-clinical**. No body is claimed here or in any future appendix without an
explicit, separately-gated clinical-scope declaration. `physical_complete` stays **False** until B2+B4 are
closed **and** a built artifact is independently validated; until then, claiming completion is a firewall
violation.

**Completion criterion (binding):** `physical_complete` may flip True **only** when **B2 and B4** are
`[L]`-closed under this gate (B1 is now closed), O3's map is derived (B2), and no `[O]` remains except B5's
declared clinical scope. Appendix K closes **B1** and satisfies none of the remaining flips, so it keeps
`physical_complete = False`. That is the honest state — **the absolute clock is pinned, but the program is
not 100% complete.**

---

## Reproduce

```
python3 run.py                # → expected/*.json + *.csv + summary.txt (deterministic, 2×SHA-256)
python3 -m completion.gate    # → fail-closed K1..K11 (with B1); exit 0 iff all pass
python3 make_figure.py        # → figures/absolute_clock_overview.png (two-anchor clock · held-out genes)
```

Gate **PASS 17/17** · `sha=49bbaa2a0ea2971f` · reference reading hash (2×SHA-256)
`f443a05f709b70e4437bb0acf629905eac09a7d750367ebb6e2694bd2d3bde55` · grades **V=10 L=4 F=1 O=1** ·
`physical_complete = False`.

`K1` same operator + **63-γ byte-identical to parent** (J's 38+25 merged) · `K2` filled cascade is a DAG
(63/62) · `K3` the null still holds · `K4` edge concordance 0 inversions · `K5` depth beats γ · `K6` OR
wavefront theorem · `K7` keys disagree · `G1` quorum/AND threshold-k wavefront (0 viol.) · `O3`
sequence-drive preserves order · `O1` floor reached on the filled kit · `O1J` jitter honest (seed 19, p5 <
floor → stays `[L]`) · `O2` segmentation sub-clock consistent · **`B1` two-anchor global clock: 0 free
parameters, held-out stages ≤ 0.56 d & 31 held-out genes ≤ 0.56 d, two independent modalities, graded
`[L]` never `[V]`** · `K8` no magic numbers (incl. the absolute-clock config) · `K9` non-fit decoy ignored
(incl. a cardiac-day decoy) · `K10` determinism (2×SHA-256) · `K11` honest declaration / no false victory
(**fails closed** if `physical_complete` is True, or the absolute clock or O1 is upgraded to `[V]`).

## Files

```
param_db.json            SantaLucia 1998 NN table (re-locked); ALL 63 REAL GRCh38 driver-γ inherited
                         byte-identical from Appendix J (driver_gamma_inherited = J's 38+25 merged;
                         driver_gamma_new = {} — K adds NO γ); the FILLED 62-edge cascade; the Carnegie
                         onset anchor (47 genes, cited [L] ranks); developmental rates (segmentation
                         period, somite count, Carnegie stage-days) + the NEW cardiac_onset_anchor
                         (CS10 @ 22 ± 1 d, [L] cited first-heartbeat landmark); thresholds — incl. the
                         absolute_clock config [F] (rate window CS9–13, zero-point CS10 @ 22 d, held-out
                         accept ±1.5 d, validated window CS8–13, linear day(s)=a+b·s); inline_magic_numbers: 0
completion/
  lock.py                the locked surface; parent_db_path() → Appendix-J param_db; cardiac_onset_anchor()
                         and absolute_clock_cfg() accessors; zero inline magic numbers; audited manifest
  seqtools.py            robust_z (A4, byte-identical), γ = −mean(NN ΔG), spinodal (App. A)
  cascade.py             the FILLED regulatory DAG — toposort, sources, longest-path DEPTH, indegree
  coupled.py             coupled-R19 net; OR wavefront; AND/threshold-k quorum gate; sequence-drive
  timing.py              O2 sub-clock → days; **global_clock() — the B1 two-anchor calibration + held-out
                         stage & gene validation + honest CS14+ bound**; global_clock_open() reports closure
  nulltest.py            the null · edge concordance · depth-beats-γ · O1 floor ablation + jitter
  grammar.py             re-states the higher-order grammar; order_to_days() reflects B1 closed
  declaration.py         the honest scope — B1 [L] / O1 [L] / O2 [L] / O3 [F]+[V] / GATE [V]; physical=False;
                         ceilings list (origin-of-rates, like O1 strength)
  grading.py             the one place precision ≠ accuracy; claim ledger (O1 and the O2b clock held [L])
  interpreter.py         interpret() — the full reading; reading_hash (2×SHA-256)
  gate.py                fail-closed K1..K11 with B1 (byte-identical-inherit, B1 closure, honest declaration)
run.py                   top-level runner → expected/ (incl. absolute_clock.csv) + summary.txt
make_figure.py           the absolute-clock figure → figures/absolute_clock_overview.png
README.md                this file (incl. §INHERIT and the 100%-completion BLUEPRINT)
figures/                 absolute_clock_overview.png
expected/                reference outputs (byte-identical across runs; incl. absolute_clock.csv)
```

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 영점은 측정되는 것이다.*
*Add-only: Appendices A–J and every prior number, grade, equation, and DOI are unchanged; all 63 inherited*
*γ are re-locked byte-for-byte against the parent param_db and K adds none. The global zero-point Appendix J*
*left `[O]` is closed by two independent measured anchors (segmentation slope + first-heartbeat intercept),*
*0 free parameters, held-out stage-days and 31 gene-days reproduced ≤ 0.56 d in the somite window — but it*
*stays `[L]`, a measurement, never `[V]`; the single-rate post-somitogenesis drift and the origin of the*
*rates are disclosed ceilings. No body is claimed; physical_complete = False; remaining to 100% = B2 + B4.*
