# Appendix J — the order-grammar COMPLETION: closing O1/O2/O3 and realising the gate

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

Appendix I identified the developmental ORDER grammar — *emergence order = toposort(regulatory cascade)
modulated by the local barrier γ²/4* — and was **honest about four things it left open**: the
pre-registered 0.70 absolute-strength floor was **not met globally** (only on the wired axial trunk),
because the 38-gene kit had **named coverage gaps** (`O1`); absolute timing in **days** was untouched
(`O2`); per-edge drive was a **uniform** `W=1`, not read from sequence (`O3`); and the wavefront theorem
was demonstrated for the **OR-gate** only. **This appendix closes all four — with real data, no tuning.**

> **반증을 메우니 발견이 선다.** The Appendix-I floor miss was a *diagnosis*, not a defect: it named the
> exact dilutors (limb-bud genes whose FGF/Wnt inducers were outside the kit; the HOX axis represented by
> group-13 only). Appendix J fills **precisely those gaps** with real GRCh38 promoter γ and the cited limb
> and HOX-collinear edges, and **re-tests the same floor**. The floor is now **REACHED** (≈0.755 vs 0.475
> inherited) — and the lift is shown to require **both** named fixes, with an honest jitter band. The
> grammar statement itself is **unchanged**; only its evidence is now closed.

This appendix is **add-only**: Appendices A–I and every prior number, grade, equation, and DOI are
unchanged. The four skeletal drivers shared with Appendices G/H (**SOX9, RUNX2, PAX1, GLI3**) are re-locked
**byte-for-byte**; **all 38 inherited driver-γ** are gate-checked **byte-identical against the parent
Appendix-I `param_db.json` read off disk** (`J1`), proving no parameter was retuned to make the floor pass.

---

## What the four channels now say

| channel | Appendix I | Appendix J (this work) | grade |
|---|---|---|---|
| **O1** gene-set fill | floor 0.70 **not met** globally (0.475); met only on the axial chain | filled kit (63 genes / 62 edges) **REACHES** the floor: **0.755** (n=47); lift needs **both** fixes | `[L]` |
| **O2** absolute timing | untouched `[O]` | segmentation **sub-clock** (42 × 5.0 h = **8.75 d**) consistent with the cited CS9–CS13 window; one global zero-point still open | `[L]` + `[O]` |
| **O3** sequence→drive | uniform `W=1`, declared not derived | per-edge drive = **√γ_parent** (R19 ON-branch amplitude) read from the promoter; **firing order preserved** (ρ=0.988) | `[F]` + `[V]` |
| **GATE** realisation | OR-gate wavefront only | generalised to a **quorum / AND threshold-k** gate (`k_i = ⌈α·indeg⌉`); partial order intact (0 viol.); OR is the **k=1** case | `[V]` |

### O1 — the floor re-test, with the lift localised (the honest part)

`completion.nulltest.floor_retest_ablation` runs a **nested-scope ablation** so the lift cannot be a
coincidence of throwing in genes:

| scope | corr(depth, Carnegie) | n | meets 0.70? |
|---|---|---|---|
| inherited 38-kit | **0.475** | 22 | no — *reproduces Appendix I exactly* |
| + limb FGF/Wnt inducers only | **0.700** | 29 | at the floor (cleanly-independent fix) |
| **+ full HOX collinear chains (FILLED)** | **0.755** | 47 | **yes — floor MET globally** |
| HOX only, limb ablated | **0.657** | 40 | no — **both fixes are required** |

`completion.nulltest.floor_retest_jitter` perturbs **every** Carnegie rank by ±1 (seed = **19**, the
canonical R19 constant; 4000 draws): mean **0.694**, p5 **0.625**, p95 **0.759**, fraction ≥ floor
**0.449**. The floor is cleared by the cited ranks but **marginal at the lower edge of citation
uncertainty** — so the claim is graded **`[L]` (empirical, on cited data), and is *never* promoted to
`[V]`**. The gate (`J11`) **fails closed** if anyone tries to upgrade it.

### O2 — order → days, only as far as the data licenses

`completion.timing` attaches the **real measured** segmentation-clock period (5.0 h, Diaz-Cuadros 2020 /
Matsuda 2020) and the cited somite count (42 pairs, O'Rahilly & Müller) to predict a somitogenesis span of
**8.75 days**, consistent ±2 d with the cited CS9–CS13 window. That converts *cadence* to days. A **single
global zero-point** that pins *all* genes to absolute days needs a **second** measured anchor the firewall
does not grant — left **`[O]`**, explicitly.

### O3 — drive read off the sequence, and what it preserves

`completion.coupled.sequence_drive_preserves_order` replaces the uniform weight with **W_edge = √γ_parent**
— the R19 ON-branch fixed-point amplitude `s* = +√γ`, so a stiffer parent delivers proportionally more
drive. This is a **declared modelling choice `[F]`** (the cis-code → drive map is not yet *derived* from
sequence alone), but its consequence is an **invariant `[V]`**: 0 OR-wavefront violations under sequence
drive, and the firing order is **preserved** (Spearman(uniform, sequence) = **0.988**).

### GATE — the quorum generalisation

`completion.coupled.threshold_k_wavefront(α)` fires a child when **≥ k_i = max(1, ⌈α·indeg⌉)** parents are
ON. At α = 1 (full AND) the cascade partial order still holds (**0 violations**), and convergent nodes
**never fire earlier** under AND than under OR. The Appendix-I OR-gate is exactly the **k = 1** special
case. `[V]`

---

## Why this is a completion, not a fit — the locks

**1 · Inheritance is byte-exact.** `J1` proves the A4 `robust_z` operator is scale/shift-invariant to machine
epsilon, the γ operator reproduces `−mean(NN ΔG)` on a probe, the four skeletal drivers match
byte-for-byte, **and all 38 inherited γ equal the parent Appendix-I `param_db` to the last digit** (0
mismatches). Nothing was retuned.

**2 · The null still holds on the filled kit.** `J3`: `spinodal(γ)` vs Carnegie staging stays inside the
±0.35 null band even with 25 new genes — the local stiffness still does **not** stage development.

**3 · Zero edge inversions on the filled kit.** `J4`: every cited regulatory edge (limb + HOX included)
whose endpoints both carry a Carnegie anchor points **forward** in developmental time — the wiring read on
the time axis never contradicts the order.

**4 · The substrate still entails it.** `J6`/`G1`: the coupled-R19 firing order respects the cascade DAG
under OR **and** under AND/threshold-k; firing tracks **depth**, not bare spinodal.

**5 · No false victory.** `J11`: the declaration closes O1 (to `[L]`), the O2 sub-clock (`[L]`), O3
(`[F]`+`[V]`) and the gate (`[V]`), but keeps the O2 global zero-point `[O]`, the built body `[O]`, and
**`physical_complete = False`**. The O1 absolute-strength row is held at `[L]` and the gate fails closed on
any `[V]` promotion.

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
  to Appendices E–I **character-for-character**.
- **All 38 driver-γ inherited from Appendix I**, byte-identical. The four overlapping Appendix-G/H genes
  (**SOX9 1.459260, RUNX2 1.241556, PAX1 1.504372, GLI3 1.298352**) and the whole 38-γ table are
  gate-checked byte-for-byte against the **parent `param_db.json`** (`J1`). If your edit changes any
  inherited γ, you have broken inheritance — **stop**.

**2 · Derivation-identity / core-subset invariance.** Adding the 25 new genes, 28 new edges, or new anchors
must **not** move any inherited number. The inherited core is **byte-compared**, not re-derived loosely;
`spinodal` and the A4 operator are proven scale/shift invariant to machine epsilon inside the gate. The
inherited-kit scope of the O1 ablation **must keep reproducing 0.475** — if filling the kit moved the
inherited core, that is a regression, not progress.

**3 · Sub-model regression (every lever must still fire).** Each mechanism keeps its falsifiable handle and
all must stay green together: the **null** (`J3`), **edge concordance** 0 inversions (`J4`),
**depth-beats-γ** (`J5`), the **OR wavefront** theorem (`J6`), the **quorum/AND wavefront** (`G1`),
**sequence-drive order-preservation** (`O3`), the **floor re-test on the filled kit** (`O1`) and its
**jitter band** (`O1J`), and the **sub-clock consistency** (`O2`). The fail-closed gate `J1..J11` runs them
all; **exit 0 iff all pass**.

**4 · Source-verified citations (no magic numbers, no uncited biology).** Every regulatory edge is `[F]`
with a literature anchor (HOX 3′→5′ temporal collinearity, Izpisúa-Belmonte 1991 EMBO J 10:2279; limb FGF8
AER → FGF10 feedback, Ohuchi 1997 Development 124:2235; SOX9→RUNX2 repression then RUNX2→SP7, Zhou 2006 PNAS
103:19004 / Nakashima 2002 Cell 108:17). Every Carnegie onset rank is `[L]` with a staging citation; every
new γ carries its GRCh38 coordinate provenance. Every developmental rate is `[L]` with a measurement
citation. `param_db.json` carries `inline_magic_numbers: 0`; the gate (`J8`) re-counts them — **including a
provenance string on the floor-robustness seed**. If you cannot cite it, it is `[O]`, not `[V]`.

**The order of operations is fixed: LOCK → Derive → Gate.** Lock the inherited substrate and the cited
facts; derive the closures from them; let the gate refuse anything that retunes a constant, smuggles a
magic number, breaks an inherited byte, or upgrades an open claim to a victory. Then — and only then —
extend.

---

## BLUEPRINT — the path to 100% completion (what would close the remaining `[O]`)

> This kit is **honestly incomplete**. Appendix J closes O1 (to `[L]`), the O2 sub-clock, O3, and the gate;
> it does **not** claim the absolute clock or a built body. The following is the binding roadmap for any
> future appendix that wants to retire the remaining open channels — each item lists the **single thing**
> that is missing and the **grade it would earn** if closed under this discipline.

**B1 · O2 → a single absolute zero-point `[O] → [L]`.** *Missing:* one **second** independently measured
absolute anchor (e.g. a cited absolute onset day for one non-segmentation driver) to pin the whole atlas,
not just the somite cadence. *Closes when:* `completion.timing.global_clock_open` can attach two real
measured anchors and the predicted absolute days for a **held-out** gene land within the cited window —
graded `[L]`, never `[V]` (it is a measurement, not a substrate invariant).

**B2 · O3 → cis-code → drive *derived* from sequence `[F] → [L]`.** *Missing:* a real, cited promoter/enhancer
→ drive map (TF-motif occupancy, accessibility) so `h_i` is **read off the sequence** rather than set to
`√γ_parent` by choice. *Closes when:* the per-edge weight is computed from the **measured** regulatory
sequence and the firing order is reproduced — graded `[L]` (real-data), the modelling choice retired.

**B3 · O1 → a logical-invariant strength claim — NOT pursued.** The absolute depth↔Carnegie magnitude is an
**empirical correlation on cited ranks**. It can be made *more robust* (B4) but it can **never** become
`[V]`: there is no substrate theorem that forces a particular numerical strength. Any appendix that grades
O1 `[V]` is **wrong by construction** and the gate will reject it. This is a permanent ceiling, stated so
no future session mistakes robustness for invariance.

**B4 · Coverage → shrink the jitter sensitivity `[L]` stays `[L]`, but stronger.** *Missing:* more of the real
cascade (additional limb/axial inducers, non-group-13 HOX with cited Carnegie ranks) so the p5 jitter edge
rises above the floor. *Closes when:* `floor_retest_jitter` p5 ≥ floor on the enlarged cited kit — still
`[L]`, but no longer marginal.

**B5 · Scope → a built / simulated organ `[O]`, out of scope.** *Missing:* everything — this kit is a
**principle demonstration on real driver promoters, non-clinical**. No body is claimed here or in any
future appendix without an explicit, separately-gated clinical-scope declaration. `physical_complete`
stays **False** until B1+B2+B4 are all closed **and** a built artifact is independently validated; until
then, claiming completion is a firewall violation.

**Completion criterion (binding):** `physical_complete` may flip True **only** when B1, B2, and B4 are all
`[L]`-closed under this gate, O3's map is derived (B2), and no `[O]` remains except B5's declared clinical
scope. Appendix J satisfies **none** of these flips and therefore keeps `physical_complete = False`. That
is the honest state.

---

## Reproduce

```
python3 run.py                # → expected/*.json + *.csv + summary.txt (deterministic, 2×SHA-256)
python3 -m completion.gate    # → fail-closed J1..J11; exit 0 iff all pass
python3 make_figure.py        # → figures/order_grammar_completion_overview.png (floor · filled · gate)
```

Gate **PASS 16/16** · `sha=8f04f931d51d3526` · reference reading hash (2×SHA-256)
`5d366e7e405f367758a2dc7f18cdf5ce7debce2fcbc730ad5f73330eea63092b` · grades **V=10 L=3 F=1 O=2** ·
`physical_complete = False`.

`J1` same operator + **38-γ byte-identical to parent** · `J2` filled cascade is a DAG (63/62) · `J3` the
null still holds · `J4` edge concordance 0 inversions · `J5` depth beats γ (now above floor) · `J6` OR
wavefront theorem · `J7` keys disagree · `G1` **quorum/AND threshold-k** wavefront (0 viol.) · `O3`
**sequence-drive** preserves order · `O1` **floor REACHED on the filled kit** (both fixes required) ·
`O1J` **jitter honest** (seed 19, p5 < floor → stays `[L]`) · `O2` **segmentation sub-clock** consistent ·
`J8` no magic numbers (incl. seed provenance) · `J9` non-fit decoy ignored · `J10` determinism (2×SHA-256) ·
`J11` honest declaration / no false victory (**fails closed** if `physical_complete` is ever True or O1 is
ever upgraded to `[V]`).

## Files

```
param_db.json            SantaLucia 1998 NN table (re-locked); 38 REAL GRCh38 driver-γ inherited
                         byte-identical from Appendix I; 25 NEW real GRCh38 γ (7 limb FGF/Wnt inducers +
                         18 HOXA/HOXD collinear), each with coordinate provenance; the FILLED regulatory
                         cascade (34 inherited + 10 limb-induction + 18 HOX-collinear = 62 cited [F]
                         edges); the Carnegie onset anchor (47 genes, cited [L] ranks, ties allowed,
                         absolute stage [O]); developmental rates (segmentation period, somite count,
                         Carnegie stage-days, all [L] cited); thresholds — null ceiling 0.35,
                         edge-concordance floor 1.0, depth-beats-γ required, absolute-strength floor 0.70
                         (annotated MET on filled kit), threshold-gate quorum config [F], drive-from-
                         sequence map [F], floor-robustness seed=19 [F]; inline_magic_numbers: 0
completion/
  lock.py                the locked surface (merges 38 inherited + 25 new γ; concatenates the 3 edge
                         blocks); zero inline magic numbers; audited lock manifest; parent_db_path()
  seqtools.py            robust_z (A4, byte-identical to App. I), γ = −mean(NN ΔG), spinodal (App. A)
  cascade.py             the FILLED regulatory DAG — toposort, sources, longest-path DEPTH, indegree,
                         composite order
  coupled.py             coupled-R19 net; OR wavefront; AND/threshold-k quorum gate; sequence-drive
  timing.py              O2 — segmentation sub-clock (real rates) → days; global zero-point [O]
  nulltest.py            the null · edge concordance · depth-beats-γ · O1 floor ablation + jitter ·
                         axial-chain sharpness
  grammar.py             re-states the higher-order grammar on the filled kit (statement unchanged)
  declaration.py         the honest scope — O1 [L] / O2 [L]+[O] / O3 [F]+[V] / GATE [V]; physical=False
  grading.py             the one place precision ≠ accuracy; claim ledger J1..S1 (O1 held [L], audited)
  interpreter.py         interpret() — the full reading; reading_hash (2×SHA-256)
  gate.py                fail-closed J1..J11 (incl. the byte-identical-inherit and honest-declaration gates)
run.py                   top-level runner → expected/ + summary.txt
make_figure.py           the completion figure → figures/order_grammar_completion_overview.png
README.md                this file (incl. §INHERIT and the 100%-completion BLUEPRINT)
figures/                 order_grammar_completion_overview.png
expected/                reference outputs (byte-identical across runs)
```

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증을 메우니 발견이 선다.*
*Add-only: Appendices A–I and every prior number, grade, equation, and DOI are unchanged; all 38 inherited*
*γ are re-locked byte-for-byte against the parent param_db. The Appendix-I floor miss was a diagnosis: fill*
*the named gaps and the 0.70 floor is REACHED (0.755), requiring both fixes — but it stays `[L]`, marginal*
*at the jitter edge, never `[V]`. Order → days via the measured segmentation clock is `[L]` with the global*
*zero-point still `[O]`; drive read from sequence is `[F]` and order-preserving `[V]`; the gate generalises*
*to a quorum/AND threshold-k gate `[V]`. No body is claimed; physical_complete = False.*
