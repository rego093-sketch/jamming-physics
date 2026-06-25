# Appendix L — the blueprint close-out: B4 closed (jitter-robust), B2 resolved as data-blocked

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

Appendix K closed **B1** (the global zero-point) and left a **binding BLUEPRINT** with two open items
(**B2**, **B4**), one permanent ceiling (**B3**), and one declared scope (**B5**). **This appendix takes
that blueprint to its honest terminus.** Every remaining open item is now resolved into exactly one of:
**CLOSED**, **PERMANENT CEILING**, **DATA-BLOCKED** (with the missing measurement named), or **DECLARED
SCOPE** — and the gate fails closed on any false promotion.

> **반증을 메우면 발견이 서고, 못 메우는 곳은 정확히 어디가 비었는지 말한다.** B4 closes because the
> dilution was a *named* coverage gap (PAX7 had no cited upstream edge); B2 does **not** close because the
> per-edge drive genuinely is **not in the measured window** — and the appendix says exactly which data
> would unblock it. Neither is hand-waved; both are gated.

This appendix is **add-only**: Appendices A–K and every prior number, grade, equation, and DOI are
unchanged. **Appendix L introduces NO new γ.** All 63 inherited driver-γ are gate-checked **byte-identical
against the parent Appendix-K `param_db.json` read off disk** (`L1`, 0 mismatches); the only new locked edge
(MEOX1→PAX7) connects two genes already in the atlas.

---

## The two items this appendix resolves

| item | Appendix K | Appendix L (this work) | grade |
|---|---|---|---|
| **B4** jitter floor | floor MET but **p5 0.625 < 0.70** (marginal at the lower edge) | one cited upstream edge **MEOX1→PAX7** removes PAX7 as an artificial source; **p5 0.625 → 0.728 ≥ 0.70**, 0 new inversions, DAG preserved | **CLOSED → [L]**, never [V] |
| **B2** cis-code → drive | modelling choice `W=√γ` `[F]`; "derive from sequence" **open** | a real motif-occupancy probe shows the drive is **NOT in the ±2 kb promoter window** (SOX9⊣RUNX2 **below** background) | **DATA-BLOCKED → [F]**, not [L] |

Everything else is **inherited from Appendix K and re-audited byte-for-byte on the B4-extended cascade**: the
two-anchor absolute clock (`B1`), the null (`L3`), edge concordance (`L4`), depth-beats-γ (`L5`), the OR
wavefront (`L6`) and quorum/AND threshold-k gate (`G1`), sequence-drive order-preservation (`O3`), the O1
floor (`O1`), and the segmentation sub-clock (`O2`).

### B4 — the jitter floor closes (the PAX7 source-fix)

In K, **PAX7** was an **artificial cascade source** — indegree 0, depth 0 — despite carrying **Carnegie rank
4**, because its real cited upstream regulator (the somite/dermomyotome marker **MEOX1**) had no edge to it.
That artifact (shallow depth, late rank) is exactly what dragged the ±1 rank-jitter **p5 below the floor**.
Appendix L adds the **single cited edge**:

```
MEOX1 → PAX7   "somite/dermomyotome (Meox1+) precedes & gives rise to Pax7+ myogenic progenitors"
               (Buckingham & Relaix 2007 Annu Rev Cell Dev Biol 23:645; Mankoo 1999 Nature 400:69)
```

This is the **same source-fix class** the program already used for TBX5/HOX13 in Appendix J. Its effect,
measured on the kit's own functions:

| quantity | K (62 edges) | L (+ MEOX1→PAX7, 63 edges) |
|---|---|---|
| PAX7 cascade depth | 0 (artificial source) | **3** |
| Spearman(depth, Carnegie) | 0.7546 | **0.8575** |
| ±1 rank-jitter mean (seed 19) | 0.6931 | **0.7854** |
| ±1 rank-jitter **p5** | **0.6245** (< 0.70) | **0.7277** (≥ 0.70) |
| fraction ≥ floor | 0.44 | **0.99** |
| new edge inversions | — | **0** (MEOX1 rank 4 = PAX7 rank 4, a concordant tie) |
| cascade is a DAG | yes | **yes** |

**Minimal by design** — exactly one edge, to avoid over-fitting the statistic. The strength claim is now
**jitter-robust but STILL `[L]`** (an empirical correlation on cited ranks); **B3 forbids `[V]` permanently**
— there is no substrate theorem that forces a numerical strength.

### B2 — the per-edge drive is not in the promoter (data-blocked)

The blueprint's B2 asks to replace `W=√γ_parent` with a drive **read off the sequence** (TF-motif occupancy).
For that to close to `[L]`, the cited **parent** TF-family motif must actually be present in the **child**
promoter above background. `completion/cis.py` measures exactly this, **parameter-free**:

- for every cited edge whose **both** endpoints have a cached real GRCh38 promoter, scan the **child**
  promoter (TSS−2000..+500, 2501 bp — the **same ±2 kb window the γ operator reads**) for the **parent**
  TF-family's cited IUPAC consensus motif(s), on **both strands**;
- compare the observed count to a **dinucleotide-preserving shuffle** null (**seed 19, 500 shuffles**), which
  controls GC/CpG composition — the shuffle **is** the null, so there is no fitted threshold;
- an edge is "above background" iff its observed count strictly exceeds the **95th percentile** of its own
  shuffle null.

**The finding (data-blocked):** only **5 / 21** both-cached edges sit above background (mean z **0.82**), and
**decisively the canonical direct edge SOX9 ⊣ RUNX2 is BELOW background (z ≈ −2.13)** — SOX9 represses RUNX2
through **distal enhancers** and protein–protein contacts, not a proximal SOX-site array (PAX1→SOX9 is
likewise below background, z ≈ −1.73). The per-edge drive is therefore **not in the ±2 kb promoter window**.
Closing B2 needs **distal-enhancer + chromatin-accessibility** sequence the present kit does not contain. This
is a **MEASUREMENT limitation** (directly parallel to the Inheritance-Kit **FV5** "data-blocked-by-measurement"
result), **not a theory defect and not a modelling failure** — so `W=√γ` stays `[F]`, **B2 does not close to
`[L]`**, and `physical_complete` stays **False**.

---

## Why this is honest, not a fit — the locks

**1 · Inheritance is byte-exact, and L adds no γ.** `L1` proves the A4 `robust_z` operator is scale/shift
invariant to machine epsilon, the γ operator reproduces `−mean(NN ΔG)`, the four skeletal drivers (**SOX9
1.459260, RUNX2 1.241556, PAX1 1.504372, GLI3 1.298352**) match byte-for-byte, **and all 63 inherited γ equal
the parent Appendix-K `param_db` to the last digit** (0 mismatches). L adds **0** new γ.

**2 · B4 is mechanistic, not tuned.** `B4` checks that the closure edge is **present**, **rank-tie-concordant**
(MEOX1 rank 4 = PAX7 rank 4 → 0 new inversions), the cascade is **still a DAG**, and the ±1 jitter **p5 ≥ the
0.70 floor** on the extended cascade (seed 19). One minimal cited edge; seed 19 is the R19 constant.

**3 · B2 is a reproducible negative.** `B2` re-runs the deterministic occupancy probe and verifies the
**majority** of edges are at/below background **and** the canonical **SOX9⊣RUNX2 is below background** — i.e.
the proximal window does not carry the drive. The verdict is **locked, falsifiable, and byte-identical in
`expected/`**.

**4 · No false victory.** `L11`: the declaration **closes B4 to `[L]`** (jitter-robust, never `[V]`), holds
**B2 `[F]`/data-blocked** (never `[L]`), keeps O1/B1 `[L]`, keeps the built body `[O]`, and holds
**`physical_complete = False`** — failing closed if B4 is promoted to `[V]`, if B2 is promoted to `[L]`, or if
`physical_complete` is ever `True`.

---

## §INHERIT — learn the inheritance discipline first (binding; read before adding anything)

> Every new session, collaborator, or appendix that extends this kit **must internalise the inheritance
> discipline below before adding a single line.** This section is **binding** and is carried, current, in
> every release. Skipping it is how a program silently drifts off its own substrate.

**1 · Inherited invariants (carry them byte-identical, never retune).** The substrate is fixed upstream and is
**not** yours to re-fit:

- R19 bistable switch `ds/dt = γs − s³ + h`; cusp geometry `spinodal = 2(γ/3)^1.5`, barrier `γ²/4`.
- The γ operator: `γ = −mean(SantaLucia-1998 nearest-neighbour ΔG)` over the real GRCh38 promoter window.
- The shape operator A4 = `robust_z` (`completion/seqtools.py`), identical at every grammatical level and to
  Appendices E–K **character-for-character**.
- **All 63 driver-γ inherited from Appendix K**, byte-identical. The four overlapping Appendix-G/H genes and
  the whole 63-γ table are gate-checked byte-for-byte against the **parent `param_db.json`** (`L1`). **L
  introduces no new γ.** If your edit changes any inherited γ, you have broken inheritance — **stop**.

**2 · Derivation-identity / core-subset invariance.** Adding the B4 edge must **not** move any inherited γ,
operator, or the K edge subset. The inherited core is **byte-compared**, not re-derived loosely; `spinodal`
and the A4 operator are proven scale/shift invariant inside the gate. The cascade **DEPTH is DERIVED** from the
cited edges — so adding the cited MEOX1→PAX7 edge is *allowed to deepen* the myogenic genes (that is B4's whole
mechanism), but it must move **no inherited number** and introduce **no inversion**.

**3 · Sub-model regression (every lever must still fire).** Each mechanism keeps its falsifiable handle and all
must stay green together: the **null** (`L3`), **edge concordance** 0 inversions (`L4`), **depth-beats-γ**
(`L5`), the **OR wavefront** (`L6`), the **quorum/AND wavefront** (`G1`), **sequence-drive order-preservation**
(`O3`), the **floor** (`O1`), the **sub-clock** (`O2`), the **two-anchor global clock** (`B1`), the **B4
closure** (`B4`), and the **B2 data-block** (`B2`). The fail-closed gate `L1..L11` (with `B1`, `B4`, `B2`) runs
them all; **exit 0 iff all pass**.

**4 · Source-verified citations (no magic numbers, no uncited biology).** Every regulatory edge is `[F]` with a
literature anchor — including the new **MEOX1→PAX7** (Buckingham & Relaix 2007; Mankoo 1999). Every Carnegie
onset rank is `[L]` with a staging citation; every developmental rate is `[L]` with a measurement citation; the
B2 motif consensus strings are **cited** (Noyes 2008; Berger 2008; Mertin 1999; Ducy 1997; Szeto 1996; Epstein
1994; van de Wetering 1997). `param_db.json` carries `inline_magic_numbers: 0`; the gate (`L8`) re-counts them —
**including the B4 closure config and the B2 occupancy config**. If you cannot cite it, it is `[O]`/`[F]`, not
`[V]`/`[L]`.

**The order of operations is fixed: LOCK → Derive → Gate.** Lock the inherited substrate and the cited facts;
derive the closures from them; let the gate refuse anything that retunes a constant, smuggles a magic number,
breaks an inherited byte, upgrades an open claim to a victory, or **closes a data-blocked item without the
missing data**. Then — and only then — extend.

---

## BLUEPRINT — now FULLY MAPPED (every `[O]` resolved)

> Appendix L resolves the last open items. The blueprint below is the **binding** map of the whole program's
> completion state. Every item is now **closed**, a **permanent ceiling**, **data-blocked with the gap named**,
> or **declared scope** — nothing is left vaguely "open".

**B1 · the global zero-point `[O] → [L]`. ✅ CLOSED (Appendix K).** Two independently measured anchors
(segmentation-oscillator slope + first-heartbeat intercept) pin the zero-point with **zero free parameters**;
held-out stage-days and gene-days in the somite window reproduced ≤ 0.56 d. A measurement, never `[V]`.

**B4 · the jitter floor `[L]` (marginal) → `[L]` (jitter-robust). ✅ CLOSED (this appendix).** The cited
MEOX1→PAX7 source-fix lifts the ±1 rank-jitter **p5 0.625 → 0.728 ≥ 0.70**, 0 new inversions, DAG preserved.
The strength is now jitter-robust but stays `[L]` — **never `[V]` (B3 ceiling)**.

**B2 · cis-code → drive. ⛔ DATA-BLOCKED (this appendix) — the one genuinely missing measurement.** The
proximal ±2 kb promoter window does **not** carry the per-edge drive (SOX9⊣RUNX2 below a dinucleotide-shuffle
background; only 5/21 edges above). `W=√γ` stays `[F]`. **It would close to `[L]` given distal-enhancer +
chromatin-accessibility sequence for the cascade genes** — that exact data is named as the unblock condition.
Until it exists, B2 stays data-blocked.

**B3 · a logical-invariant strength claim — NOT pursued (permanent ceiling).** The depth↔Carnegie magnitude is
an **empirical correlation**; B4 made it *robust* but it can **never** become `[V]`. The **origin of the rates**
(why ~5 h, why ~42; B1's residual) is a ceiling of the **same** kind. Any appendix grading either `[V]` is
wrong by construction and the gate rejects it.

**B5 · a built / simulated organ `[O]`, out of scope.** A principle demonstration on 63 real driver promoters,
non-clinical. No body is claimed.

**Completion criterion (binding):** `physical_complete` may flip `True` **only** when **B2 and B4 are both
`[L]`-closed** under this gate. **B4 is now closed; B2 is data-blocked** (not `[L]`), so `physical_complete`
stays **False**. That is the honest terminus — **the absolute clock is pinned, the order floor is
jitter-robust, the program is fully mapped, and the one missing piece (distal cis-drive sequence) is named.**

---

## Reproduce

```
python3 run.py                # → expected/*.json + *.csv + summary.txt (deterministic, 2× SHA-256)
python3 -m completion.gate    # → fail-closed L1..L11 (with B1, B4, B2); exit 0 iff all pass
python3 make_figure.py        # → figures/blueprint_closeout_overview.png (B4 jitter shift · B2 z-scores)
```

Gate **PASS 18/18** · `sha=b0cf5eae7285b50a` · reference reading hash (2× SHA-256)
`a817287d1b57d84ea30a2c6ce7ade71f1333561205a4e1b4785abda78af37aca` · grades **V=10 L=5 F=2 O=1** ·
`physical_complete = False` · `blueprint_fully_mapped = True`.

`L1` same operator + **63-γ byte-identical to parent K** · `L2` cascade is a DAG (63 genes / **63 edges**) ·
`L3` the null still holds · `L4` edge concordance 0 inversions (incl. MEOX1→PAX7) · `L5` depth beats γ · `L6`
OR wavefront · `L7` keys disagree · `G1` quorum/AND threshold-k wavefront · `O3` sequence-drive preserves order
· `O1` floor reached on the filled kit · **`B4` jitter CLOSED: p5 0.728 ≥ 0.70 on the extended cascade, 0 new
inversions, edge cited + rank-tie-concordant, strength stays `[L]` never `[V]`** · **`B2` cis-drive
DATA-BLOCKED: majority at/below background, SOX9⊣RUNX2 below background, graded `[F]` not `[L]`** · `O2`
segmentation sub-clock · `B1` two-anchor global clock (`[L]`, never `[V]`) · `L8` no magic numbers (incl. the
B4 + B2 configs) · `L9` non-fit decoy ignored · `L10` determinism (2× SHA-256) · `L11` honest declaration / no
false victory (**fails closed** if B4→`[V]`, if B2→`[L]`, or if `physical_complete=True`).

## Files

```
param_db.json            SantaLucia 1998 NN table (re-locked); ALL 63 REAL GRCh38 driver-γ inherited
                         byte-identical from Appendix K (driver_gamma_new = {} — L adds NO γ); the
                         62-edge cascade + the NEW edges_myogenic_upstream block (MEOX1→PAX7, B4);
                         the Carnegie onset anchor; developmental rates incl. the cardiac zero-point;
                         thresholds — incl. b4_jitter_closure [L] and b2_cis_occupancy [F];
                         inline_magic_numbers: 0
completion/
  lock.py                the locked surface; parent_db_path() → Appendix-K param_db; cascade_edges()
                         concatenates the 3 inherited blocks + the B4 myogenic block; b4/b2 accessors;
                         cis_promoter_cache(); audited manifest; zero inline magic numbers
  seqtools.py            robust_z (A4, byte-identical), γ = −mean(NN ΔG), spinodal (App. A)
  cascade.py             the B4-extended regulatory DAG — toposort, sources, longest-path DEPTH
  coupled.py             coupled-R19 net; OR wavefront; AND/threshold-k quorum gate; sequence-drive
  timing.py              O2 sub-clock; the inherited B1 two-anchor absolute clock + held-out validation
  nulltest.py            the null · edge concordance · depth-beats-γ · floor ablation (+ scope_e) ·
                         floor_retest_jitter (now clears at p5) · b4_jitter_closed (the B4 closure)
  cis.py                 the B2 occupancy probe — IUPAC motif scan (both strands) vs dinucleotide-
                         shuffle null (seed 19, 500 shuffles); reproduces the DATA-BLOCKED finding
  grammar.py             re-states the higher-order grammar
  declaration.py         the honest scope — B4 [L] closed / B2 [F] data-blocked / B1 [L] / O1 [L] /
                         O2 [L] / O3 [F]+[V] / GATE [V]; physical_complete=False; blueprint_fully_mapped
  grading.py             the claim ledger; B4 row [L], B2 row [F]; self-audits B4 stays [L], B2 not [L]
  interpreter.py         interpret() — the full reading; reading_hash (2× SHA-256)
  gate.py                fail-closed L1..L11 with B1, B4, B2 (byte-identical-inherit, B4 closure, B2
                         data-block, honest declaration)
run.py                   top-level runner → expected/ (incl. b4_jitter.csv, b2_occupancy.csv) + summary
make_figure.py           the close-out figure → figures/blueprint_closeout_overview.png
promoters.cache.json     29 real GRCh38 promoter windows (TSS−2000..+500) used by the B2 probe
README.md                this file (incl. §INHERIT and the FULLY-MAPPED BLUEPRINT)
figures/                 blueprint_closeout_overview.png
expected/                reference outputs (byte-identical across runs)
```

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증을 메우면 발견이 서고,
못 메우는 곳은 어디가 비었는지 말한다.*
*Add-only: Appendices A–K and every prior number, grade, equation, and DOI are unchanged; all 63 inherited γ are
re-locked byte-for-byte against the parent param_db and L adds none. B4 is closed by one cited edge (MEOX1→PAX7;
jitter p5 0.625 → 0.728 ≥ floor, 0 new inversions, DAG preserved) — jitter-robust but [L], never [V]. B2 is
data-blocked by measurement (the per-edge drive is not in the ±2 kb promoter window; SOX9⊣RUNX2 below
background) — [F], not [L]; distal-enhancer data is the named unblock condition. The blueprint is fully mapped;
physical_complete = False; no body is claimed.*
