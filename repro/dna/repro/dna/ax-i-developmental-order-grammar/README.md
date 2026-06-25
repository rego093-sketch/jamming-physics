# Appendix I — the developmental ORDER grammar: what predicts Carnegie staging is not γ

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

Appendix A measured a **null** and left it open: across the driver genes the single-locus promoter
stiffness γ does **not** predict the real Carnegie developmental **stage** at which each program emerges
(`spinodal(γ)`-vs-staging ρ ≈ 0, the "측정된 null"). Appendix H then *used* `argsort(spinodal(γ))` as its
4D build schedule but was honest that **whether that order matches real staging is the Appendix-A null** —
it marked schedule-timing accuracy `[O]`. **This appendix closes that hole.** It asks the question the
build left open — *발생 순서를 예측하는 것은 무엇인가?* — and answers it from the R19 substrate up.

> **반증 = 발견.** γ failing to stage development was never a defect in the operator — it was a **category
> fact**. γ is a **local** single-locus key (it sets one promoter's barrier `γ²/4` and its `spinodal`).
> Developmental order is **global**: a gene cannot fire until its **upstream regulators** have delivered
> drive. So the predictor of order is **regulatory-cascade hierarchy DEPTH** — and depth is **not a new
> grammar**. It is the architecture/wiring grammar **G3**, already identified in Appendix F, simply
> **read on the time axis**. *"설계도에 분명이 있다."* It was in the blueprint all along.

This appendix is **add-only**: Appendices A–H and every prior number, grade, equation, and DOI are
unchanged. The four skeletal/limb driver genes shared with Appendices G/H (**SOX9, RUNX2, PAX1, GLI3**)
are re-locked **byte-for-byte** (γ = 1.459260 / 1.241556 / 1.504372 / 1.298352); the entire 38-gene γ
table and the `(LEVEL, SHAPE) = (γ, A4)` operator are inherited from Appendix H **byte-identical**, proving
no parameter was retuned to make the order come out right.

---

## The claim, in one line

**emergence ORDER = toposort(regulatory cascade) modulated by the local barrier γ²/4.**
Depth is **primary** (which tier you are in — how many regulators must fire upstream of you first); the
barrier `γ²/4` is the **within-tier tie-break** (which of two same-depth genes trips first). This is the
**composite, higher-order** grammar the instruction predicted (*"복합적일수 있고 상위 문법일수 있다"*),
and it is **sharpest at the earliest stages**, where the axial cascade is most tightly wired
(canalization — *"초기단계에 더 큰 문법 예측가능한게 있을것이다"*).

| key on which we sort | what it is | Spearman vs real Carnegie order | grade |
|---|---|---|---|
| `spinodal(γ)` — single locus | local promoter stiffness (Appendix A) | **−0.266** (inside ±0.35 null) | `[V]` null |
| **cascade DEPTH** — global wiring | #regulators in series upstream | **+0.475** (all) / **+0.470** (main WCC) | `[V]` direction |
| cited regulatory **edges** | each parent→child arrow vs measured timing | **25/25 concordant, 0 inversions** | `[V]` |
| coupled-R19 **firing** | first-principles ODE on the wired net | firing-vs-depth **+0.795**, vs spinodal −0.005 | `[V]` |

## Why this is a derivation, not a fit — the four locks

**1 · The null is real (the same operator, in numbers).** `order.nulltest.the_null` recomputes
`spinodal(γ)` for all 38 drivers and correlates against the cited Carnegie onset ranks:
**ρ = −0.266**, inside the pre-registered ±0.35 null band. γ does not stage development — Appendix A,
reproduced here as a number, not asserted. `[V]`

**2 · The wiring read on the time axis IS the grammar (no cherry-pick).** `order.nulltest.edge_concordance`
takes **every** cited regulator→target edge whose *both* endpoints carry a Carnegie anchor — **25 edges** —
and asks how many point **forward in developmental time**. **24 strictly forward + 1 tie, 0 inversions →
concordance = 1.000** (floor 1.0). This is not a correlation that could be massaged: a single backward
edge (a target staged before its regulator) would break it, and there are none. The cascade **is** the
order. `[V]`

**3 · Depth beats γ, strictly.** `order.nulltest.depth_beats_gamma`: `corr(depth, Carnegie) = +0.475`
versus `corr(spinodal, Carnegie) = −0.266` on all anchored genes; `+0.470` vs `−0.267` on the main
weakly-connected component (18 genes). The global wiring out-predicts the local stiffness on the **same**
genes with the **same** anchor. `[V]`

**4 · The substrate entails it — the OR-gate wavefront theorem.** `order.coupled` integrates the genuine
coupled R19 network `ds_i/dt = γ_i·s_i − s_i³ + h_i`, every node initialised on its **stable OFF branch**
`s_i(0) = −√γ_i`, drive injected only at the **sources**, propagated along edges at uniform weight `W=1`.
A non-source switches ON **after at least its earliest already-ON regulator** (one ON parent at `W=1`
already pushes the child past its spinodal) — `partial_order_compliance` reports **0 violations** over the
whole net. Firing order then tracks **depth** (ρ = +0.795), **not** bare spinodal (ρ = −0.005). The order
grammar is not imposed on the substrate; it **falls out of** the substrate. `[V]`

## The live handle: order is a function of the wiring, not a list

`order.cascade.resort_on_edge` cuts the **SOX9 ⊣ RUNX2** repression edge and re-runs the coupled sim:
RUNX2's firing time moves **59.02 → 38.3** (it fires **earlier** once its upstream brake is removed) —
exactly the biology (SOX9 represses RUNX2; relieve the repression and ossification's master switch
advances). The order is a **live function of the edges**, the falsifiable handle that this is a *wiring*
grammar and not a stored ranking. `[V]`

## The axial trunk and the honest negative

The longest cascade path — the **axial chain**

```
FOXA2 → DLL3 → MEOX1 → PAX1 → SOX9 → RUNX2 → SP7
```

is the spine of the grammar: on this wired trunk depth-vs-Carnegie is **ρ = 1.000** (monotone, exact).
But the **absolute** global strength is graded honestly. `order.nulltest.absolute_strength_residual`
pre-registers a floor of **0.70** for the *magnitude* of `corr(depth, Carnegie)` across **all** anchored
genes, and that floor is **NOT met globally (0.475)** — it is met **only on the axial chain**. The reason
is named, not hidden: the 38-gene kit contains **artificial sources** (limb-bud **TBX4/TBX5** look like
sources because their FGF/Wnt inducers are *outside* this gene set; the HOX axis is represented by
**group-13 only**), and these **dilutors** flatten the global slope. So:

- **order direction** (which fires before which) — `[V]` (edge concordance 25/25, depth beats γ, wavefront theorem)
- **absolute rank strength** (how strongly depth pins the *exact* rank globally) — `[L]`, strongest on the wired trunk (ρ = 1.000), diluted off-trunk by named artificial sources `O1`
- **absolute timing in days** — `[O]` (`O2`)
- **per-gene cis-code → drive `h_i` from sequence** — `[O]`; here `W` is uniform, drive is not yet read off the promoter (`O3`)
- **a built / simulated human or organ** — `[O]`, out of scope; *no body is ever claimed* (`O4`)

The negative is **reported, not buried** — that is the discipline. `반증 = 발견`.

---

## §INHERIT — learn the inheritance discipline first (binding; read before adding anything)

> Every new session, collaborator, or appendix that extends this kit **must internalise the inheritance
> discipline below before adding a single line.** This section is **binding** and is carried, current, in
> every release. Skipping it is how a program silently drifts off its own substrate.

**1 · Inherited invariants (carry them byte-identical, never retune).** The substrate is fixed upstream and
is **not** yours to re-fit:

- R19 bistable switch `ds/dt = γs − s³ + h`; cusp geometry `spinodal = 2(γ/3)^1.5`, barrier `γ²/4`.
- The γ operator: `γ = −mean(SantaLucia-1998 nearest-neighbour ΔG)` over the real GRCh38 promoter window.
- The shape operator A4 = `robust_z` (`order/seqtools.py`), identical at every grammatical level and to
  Appendices E/F/G/H **character-for-character**.
- The 38 driver-γ values in `param_db.json`, inherited from Appendix H. The four overlapping Appendix-G/H
  genes (**SOX9 1.459260, RUNX2 1.241556, PAX1 1.504372, GLI3 1.298352**) are gate-checked byte-for-byte
  (`I1`). If your edit changes any inherited γ, you have broken inheritance — **stop**.

**2 · Derivation-identity / core-subset invariance.** Adding genes, edges, or anchors must **not** move any
inherited number. The overlap with the parent appendix is re-locked and **byte-compared**, not
re-derived loosely; `spinodal` and the A4 operator are proven scale/shift invariant to machine epsilon
inside the gate. A change that perturbs the inherited core is a regression, not progress.

**3 · Sub-model regression (every lever must still fire).** Each mechanism keeps its own falsifiable handle
and all must stay green together: the **null** (`spinodal` does not stage), **edge concordance** (0
inversions), **depth-beats-γ**, the **wavefront theorem** (0 partial-order violations), the **edge-cut
resort lever**, and **keys-disagree** (the spinodal order and the depth order are genuinely different,
ρ = −0.073 — otherwise the claim would be vacuous). The fail-closed gate `I1..I12` runs them all; **exit 0
iff all pass**.

**4 · Source-verified citations (no magic numbers, no uncited biology).** Every regulatory edge is `[F]`
with a literature anchor (HOX 3′→5′ temporal collinearity, Izpisúa-Belmonte 1991 EMBO J 10:2279; SOX9→RUNX2
repression then RUNX2→SP7 ossification, Zhou 2006 PNAS 103:19004 / Nakashima 2002 Cell 108:17). Every
Carnegie onset rank is `[L]` with a staging citation. `param_db.json` carries `inline_magic_numbers: 0` and
the gate (`I9`) re-counts them. Numbers that cannot be sourced do **not** enter the kit; if you cannot cite
it, it is `[O]`, not `[V]`.

**The order of operations is fixed: LOCK → Derive → Gate.** Lock the inherited substrate and the cited
facts; derive order from them; let the gate refuse anything that retunes a constant, smuggles a magic
number, breaks an inherited byte, or upgrades an open claim to a victory. Then — and only then — extend.

---

## Reproduce

```
python3 run.py            # → expected/*.json + summary.txt (deterministic, 2×SHA-256)
python3 -m order.gate     # → fail-closed I1..I12; exit 0 iff all pass
python3 make_figure.py    # → figures/order_grammar_overview.png (null · discovery · cascade DAG)
```

Gate **PASS 12/12** · `sha=ca6f907e6a2dd932` · reference reading hash (2×SHA-256)
`f90dea7a08729a3b6fca4689bd1c7c354c71cb688a0184cee188bfa560912e76` · grades **V=8 L=2 O=3** ·
`physical_complete = False`.

`I1` same operator + 4-driver byte-match · `I2` cascade is a DAG · `I3` **the null** (spinodal does not
stage) · `I4` **edge concordance** (0 inversions) · `I5` **depth beats γ** · `I6` coupled **wavefront**
theorem (0 violations) + firing tracks depth · `I7` spinodal-order ≠ depth-order (keys disagree) ·
`I8` **edge-cut resort** lever · `I9` no magic numbers · `I10` non-fit decoy ignored · `I11` determinism
(2×SHA-256) · `I12` honest declaration / no false victory (fails closed if `physical_complete` is ever
True or the absolute-strength `O1` is ever silently upgraded to `[V]`).

## Files

```
param_db.json            SantaLucia 1998 NN table (re-locked); 38 REAL GRCh38 driver-gene γ inherited
                         byte-identical from Appendix H (4 overlapping App. G/H genes byte-checked);
                         the regulatory cascade (34 cited [F] gene→gene edges); the Carnegie onset
                         anchor (22 genes, cited [L] ranks 1..11, ties allowed, absolute stage [O]);
                         thresholds — null ceiling 0.35, edge-concordance floor 1.0, depth-beats-γ
                         required, absolute-strength floor 0.70 (annotated NOT met globally); all
                         cited or declared, inline_magic_numbers: 0
order/
  lock.py                the locked surface; zero inline magic numbers; the audited lock manifest
  seqtools.py            robust_z (A4, byte-identical to App. H), γ = −mean(NN ΔG), spinodal (App. A)
  cascade.py             the regulatory DAG — toposort, sources, longest-path DEPTH, composite order
  coupled.py             the first-principles coupled-R19 net; the OR-gate wavefront theorem; resort
  nulltest.py            the null · edge concordance · depth-beats-γ · the honest absolute-strength floor
  grammar.py             states the higher-order grammar (toposort modulated by γ²/4; G3 on time axis)
  declaration.py         the honest scope — closed [V] / open [L]/[O]; physical_complete = False
  grading.py             the one place precision ≠ accuracy; claim ledger C1..C9 + O1..O4
  interpreter.py         interpret() — the full reading; reading_hash (2×SHA-256)
  gate.py                fail-closed I1..I12 (incl. the honest-declaration gate)
run.py                   top-level runner → expected/ + summary.txt
make_figure.py           the order figure → figures/order_grammar_overview.png
README.md                this file
figures/                 order_grammar_overview.png
expected/                reference outputs (byte-identical across runs)
```

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
*Add-only: Appendices A–H and every prior number, grade, equation, and DOI are unchanged; the 4 driver*
*γ's overlapping Appendix G/H are re-locked byte-for-byte. What predicts developmental ORDER is the*
*cascade wiring (G3) read on the time axis — DEPTH, tie-broken by the local barrier γ²/4 — not the*
*single-locus stiffness γ. Order direction is [V]; absolute rank strength is [L] (strongest on the wired*
*trunk); absolute timing and the cis-code → drive map remain [O]. No body is claimed.*
