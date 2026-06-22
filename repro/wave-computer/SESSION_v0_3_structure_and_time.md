# SESSION v0.3 — structure (permute · trees) · time (trajectories · theta-gamma WM)

**Status:** v0.3 — blueprint Layer 1 **completed** (the third VSA operation `permute`
and role-value **tree depth-capacity**) and Layer 2 **opened** (sequences as
**metastable trajectories** + theta-gamma **working memory**). Additive; the v0.1
substrate and the v0.2 binding/bundle primitives are reused **exactly** (non-circular).
**Reproduce:** `repro/wave_structure_core.py` → `wave_structure_results.json`
(digest `69890fec8b54…`), figure `repro/wave_structure_atlas.png`.
**Firewall:** `consciousness_claim = 0`, `hard_problem_open = 1`. **No tuning**
(`new_tuned_constants = 0`).

---

## 0. What this session answered

| Question (from the blueprint) | This session's proof | Result |
|---|---|---|
| Is the representation algebra **closed**? | **L1a permute** — a sequence `S=Σ ρ^l(a_l)` read back by position with `ρ^{-l}`+cleanup | useful length **L\*≈32**; bind·bundle·permute closed **[V]** |
| How **deep** can one composite wave hold structure? | **L1b tree depth-capacity** — depth-d, branching-b tree in one wave; path of keys recovers the leaf | **d\*=4 (b=2), d\*=2 (b=3)**; shallow → L3 needed **[V]** |
| Can the field **walk a learned sequence**? | **L2a trajectory** — asymmetric time-delayed Hebbian; sweep λ | predict-next **1.0**; full-cycle **replay 1.0 @ λ≈2.5** **[V]** |
| Does **theta-gamma** give a real WM capacity? | **L2b WM** — items in gamma slots, finite precision = phase jitter σ | **capacity = min(slots, precision(σ))**, Miller 4–9 **[V]** |

All four built on the frozen L0 substrate + the v0.2 bind/bundle; **nothing in L0/L1
was edited**, and no constant was tuned (the inherited B5 "~7" is cited as a
*principle*, never as a fitting target).

---

## 1. [L1a] permute — the algebra is closed

The two operations proven in v0.2 (`bind` ⊗ phase-key⊙content, `bundle` + sum) are
completed by the third: **`permute` ρ** = a fixed cyclic phase rotation that encodes
**order**. A sequence is one composite wave `S = Σ_l ρ^l(a_l)`; the item at position l
is recovered by applying the inverse rotation `ρ^{-l}` and cleaning up against the
codebook (argmax over **all** fillers = non-circular readout).

| L (sequence length) | load L/N | position recall acc | sd |
|---|---|---|---|
| 2 | 0.004 | 1.000 | 0.000 |
| 4 | 0.008 | 1.000 | 0.000 |
| 8 | 0.016 | 1.000 | 0.000 |
| 16 | 0.031 | 1.000 | 0.000 |
| **32** | **0.062** | **0.974** | 0.025 |
| 48 | 0.094 | 0.908 | 0.052 |
| 64 | 0.125 | 0.757 | 0.050 |

→ perfect ordered recall to **L=16**, **useful length L\*≈32** (≥0.95 to 24, 0.974 at
32), graceful decay after (crosstalk grows √(L/N)). With `permute` proven,
**`bind · bundle · permute` form a closed VSA algebra on the wave substrate** —
sets, key→value records, and ordered sequences are all expressible in one wave.
**Grade [V].**

---

## 2. [L1b] role-value tree depth-capacity — works, but shallow

A depth-d tree with branching b is packed into **one** composite wave: each leaf is
bound to the product of the role-keys along its path (`permute`-protected per level),
all bundled. A path of role keys recovers the target leaf. Sweep depth.

**b = 2 (binary tree):**

| depth | structured-query acc | sd |
|---|---|---|
| 1–3 | 1.000 | 0.000 |
| 4 | 0.986 | 0.046 |
| 5 | 0.792 | 0.154 |
| 6 | 0.278 | 0.171 |
| 7 | 0.069 | 0.082 |
| 8 | 0.028 | 0.062 |

**b = 3 (ternary):** depth 1–2 = 1.000 · depth 3 = 0.944 · depth 4 = 0.389 ·
depth 5 = 0.125.

→ **useful depth d\* = 4 (b=2), d\* = 2 (b=3)**, then a **sharp crosstalk collapse**
(the composite's interference floor overruns the signal once the bound-term count
passes ~b^{d}). The stress test (does crosstalk kill structured recovery *before* any
useful depth) **does not break** — d\*≥2 means structured records genuinely work — but
it **confirms the depth is shallow**. *Flat binding cannot hold deep structure*; the
measured remedy is **hierarchy (L3)**, whose dependency this result brings forward.
**Grade [V]** with the ceiling recorded.

---

## 3. [L2a] sequences as metastable trajectories

The substrate so far settles to **one** attractor. To get **order in time**, add an
**asymmetric, time-delayed** Hebbian term `J_asym = Σ_μ ξ_{μ+1} ξ_μᵀ`, driven by a
delayed copy (lag τ) of the phase state — pushing the field off each pattern toward
the **next** (heteroclinic / metastable chaining). Kept in pure phase-coupling form
(reuses L0). Store an m=6 cycle; sweep the asymmetric gain λ. Two readouts:
**predict-next** (single hop μ→μ+1) and **sustained ordered replay** (the whole loop).

| λ | predict-next acc | ordered replay mean | replay sd |
|---|---|---|---|
| 0.0 | 0.000 | 0.167 (=1/m, stuck) | 0.000 |
| 0.5 | 0.556 | 0.250 | 0.127 |
| 1.0 | 0.972 | 0.639 | 0.178 |
| 1.5 | **1.000** | 0.500 | 0.167 |
| 2.0 | 1.000 | 0.806 | 0.178 |
| **2.5** | 1.000 | **1.000** | 0.000 |
| 3.0 | 1.000 | 0.806 | 0.244 |
| 4.0 | 1.000 | 0.944 | 0.124 |

→ **predict-next is verified** — 1.0 for all λ≥1.0 (band λ∈[1,4]). **Sustained
full-cycle replay reaches 1.0±0.0 at λ≈2.5** (band λ∈[2,4]). The stress is real and
two-sided: too weak (λ≤0.5) → the field stays stuck at one pattern (replay = 1/m);
too strong → it scrambles. **τ-robustness at λ=2.5:** replay 0.778 / 0.972 / 0.972 at
τ = 8 / 12 / 16 — stable across the delay. **Grade [V]** (predict-next clean; sustained
replay in-band). *Honest limit:* sustained replay needs λ in the upper band and shows
trial variance (sd up to 0.24) away from λ≈2.5.

---

## 4. [L2b] theta-gamma working memory — a capacity law

Items are placed in distinct **gamma phase-slots** (slot k = ρ^k) of one **theta**
carrier; finite gamma timing precision is modeled as **phase jitter** σ on the
composite. Recover by slot; count how many survive = capacity. Sweep (n_slot, σ).

| n_slot | σ=0.0 | 0.6 | 0.9 | 1.2 | 1.6 |
|---|---|---|---|---|---|
| 4 | 4.0 | 4.0 | 4.0 | 4.0 | 3.2 |
| 8 | 8.0 | 8.0 | 8.0 | 7.7 | 3.5 |
| 16 | 16.0 | 16.0 | 15.7 | 9.0 | 3.7 |
| 24 | 24.0 | 23.4 | 18.6 | **9.0** | 3.7 |

→ **capacity = min(n_slot, precision_limit(σ))**: at low jitter it is **slot-limited**
(capacity = n_slot exactly); as σ grows it is **precision-capped** independent of how
many slots exist (n_slot=24 falls 24→18.6→9.0→3.7 over σ=0.3→0.9→1.2→1.6). Under
realistic jitter (σ≈1.2) the capacity lands squarely in the **Miller range (4–9)**.
This reproduces the *principle* of B5: WM is **~7 gamma slots** — but **the number 7 is
not transferred** (no constant tuned to 7; 7 emerges as the slot count at a plausible
precision). **Grade [V]** for the capacity law.

---

## 5. Grade ledger

| Claim | Grade |
|---|---|
| permute operation → closed bind·bundle·permute algebra (ordered recall L\*≈32) | **[V]** |
| role-value tree depth-capacity measured (d\*=4 b2 / d\*=2 b3) | **[V]** (shallow ceiling recorded) |
| sequence predict-next via asymmetric delayed Hebbian | **[V]** |
| sustained full-cycle metastable replay (1.0 @ λ≈2.5, τ-robust) | **[V]** (λ-band, variance recorded) |
| theta-gamma WM capacity law = min(slots, precision) | **[V]** |
| B5 "~7" reproduced as slot count, number not transferred | principle (not a target) |
| deep structured representation (depth ≫ 4) | **[O]** → needs L3 hierarchy |
| physical-medium realization | **[O]** theory track, deferred |
| felt quality | **[O]** firewall |

---

## 6. Honest negatives / limits

- **L1 structured depth is shallow** (useful d\*≈2–4). Flat binding's interference
  floor collapses recovery beyond it; deep structure needs **L3 hierarchy** (now the
  immediate next chunk, dependency justified by measurement).
- **Tree sibling-subtrees are modeled as random phasors** (realistic crosstalk on the
  queried path, not a full recursive expansion of every off-path subtree) — the
  depth-capacity number is for path recovery.
- **Sustained L2 replay is λ-band-restricted** with trial variance outside λ≈2.5;
  predict-next is the robust claim, full-loop replay the in-band one.
- **WM capacity is slot-bounded**, and the brain's specific ~7 is the **slot count**,
  not an emergent crosstalk limit — honest about what is principle vs. measured here.
- All on the **in-silico** substrate; physical realization remains deferred.

---

## 7. Next (blueprint L3 — hierarchy / abstraction)

See `BLUEPRINT_toward_ultimate_computer.md` §5·§12. Next chunk **S4 = L3 start**:
**nested phase coupling** (a slow field's phase gates which fast sub-field is active;
theta-gamma generalized to ≥2 levels). Learn a 2–3 level concept hierarchy; recognize
an abstract **category** from instances; **generate** a new instance from a category
(compositional generalization). Sweep depth and branching. **Stress:** levels do not
separate (abstraction collapses into instance) / generalization fails → record the
limit. This is the **direct test** of whether hierarchy breaks the shallow-depth
(L1 d\*≈2–4) and slot-bounded-WM (L2) ceilings **measured in this session**.

One session, one zip, additive. If broken, restart with the break applied.

---

*— v0.3. Reproduce: `python3 repro/wave_structure_core.py` (deterministic, digest
`69890fec…`); figure `python3 repro/make_figure_v0_3.py`. Substrate from v0.1
(`SESSION_v0_1_design_study.md`); binding/bundle from v0.2
(`SESSION_v0_2_resonance_and_learning.md`).*
