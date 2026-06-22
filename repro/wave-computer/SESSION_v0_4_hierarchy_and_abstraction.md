# SESSION v0.4 — hierarchy (nested gating · abstraction) · compositional generalization

**Status:** v0.4 — blueprint Layer 3 (**hierarchy / abstraction**) **met and graded**.
Built directly on the v0.3 finding that flat binding is **shallow** (useful tree depth
d\*≈2–4) and WM is **slot-bounded** — L3 is the measured remedy. Additive; the v0.1
substrate and the v0.2/v0.3 binding·bundle·permute primitives are reused **exactly**
(non-circular). **Reproduce:** `repro/wave_hierarchy_core.py` →
`wave_hierarchy_results.json` (digest `ea4c67235b53…`), figure
`repro/wave_hierarchy_atlas.png`. **Firewall:** `consciousness_claim = 0`,
`hard_problem_open = 1`. **No tuning** (`new_tuned_constants = 0`; brain R/WM anchors
are **not** transferred — the gate centres are structural and κ is swept).

---

## 0. What this session answered

| Question (from the blueprint) | This session's proof | Result |
|---|---|---|
| Do **levels separate** (does a slow phase pick the level)? | **H1 nested gating** — a slow phase's von Mises window gates which fast sub-field is active; cued vs wrong vs off | gate **selects** every B (correct 1.0 vs wrong ≤0.16, margin **+0.92**) **[V]** |
| Can the field recognize an **abstract category** from **novel** instances? | **H2 abstraction** — prototype basins; categorize instances **never stored** | category(novel) **1.0** to ρ=0.4, up to **32** categories **[V]** |
| Does it **generalize compositionally** (and **generate** a new instance)? | **H3 compositional** — decode **held-out** (never-built) factor combos; depth-2 & depth-3 | **gap = 0.00** to **576** combos; generate valid+novel **[V]** |
| Does **hierarchy break the flat ceiling**? | **H4 head-to-head** — same T instances flat vs B gated sub-fields, **strict** clean-up | flat collapses at **T≈12**, hierarchy holds to **T=72** (**~6×**) **[V]** |

All four built on the frozen L0 substrate + v0.2/v0.3 primitives; **nothing in L0/L1/L2
was edited**, and no constant was tuned. The L3 mechanism is **nested phase coupling**:
a slow phase `g` gates the active fast sub-field through a von Mises window
`w_b(g) = exp(κ(cos(g−φ_b)−1))` with **structural** centres `φ_b = 2πb/B` and κ swept —
theta-gamma (v0.3 L2b) generalized to ≥2 coupled levels.

---

## 1. [H1] nested gating — the slow phase SELECTS the level

`B` category sub-fields are built (each a Hebbian field over its m instances). A slow
phase selects one via the von Mises gate; a corrupted instance cue is settled in the
**gated** field and read by argmax over the **whole** codebook (non-circular). Compare
the **correct** slow phase vs a **wrong** one vs **off** (flat field over all T).

| B | T | gate CORRECT | gate WRONG | gate OFF (=flat) | global R |
|---|---|---|---|---|---|
| 2 | 8 | 1.000 | 0.156 | 1.000 | 0.048 |
| 4 | 16 | 1.000 | 0.125 | 1.000 | 0.051 |
| 6 | 24 | 1.000 | 0.042 | 1.000 | 0.056 |
| 8 | 32 | 1.000 | 0.039 | 1.000 | 0.049 |

→ the gate **selects decisively at every B**: the cued slow phase routes to the correct
sub-field (1.0) while a **wrong** slow phase rejects it (≤0.16) — **select margin
+0.92**, sign-stable. This selectivity **is** the level-separation test: the slow phase
**picks the level**, so abstraction does not collapse into instance. **Gate width
matters** (a real swept dependence): a **broad** gate (κ=0.5) leaks (wrong-acc 0.83)
while **sharp** gates (κ≥2) reject (wrong-acc ≤0.13). The **off==flat** coincidence at
this light load is a *capacity* question — does routing buy capacity? — deliberately
**owned by H4**, not asserted here. **Grade [V]** (selectivity / levels separate).

*Honest scope:* at light load the OFF/flat field also recovers (1.0), so H1 alone does
not show a capacity benefit — only **selectivity**. The capacity claim is H4's.

---

## 2. [H2] abstraction — category from NOVEL instances

Each category `b` has a **prototype** `P_b`; instances are `P_b` with a fraction ρ of
bits flipped. An **upper** field stores the **prototypes**; the test categorizes
instances that were **never stored** (genuinely novel) by which prototype basin they
fall into. A **lower** field stores instances. Geometry: within-category spread vs
between-category distance sets a **principled** boundary (not tuned).

| ρ (instance jitter) | category(novel) | instance recall | within-spread | between-dist | separable |
|---|---|---|---|---|---|
| 0.00 | 1.000 | 0.125 | 0.000 | 0.499 | yes |
| 0.05 | 1.000 | 0.115 | 0.096 | 0.502 | yes |
| 0.10 | 1.000 | 0.188 | 0.181 | 0.500 | yes |
| 0.15 | 1.000 | 0.125 | 0.252 | 0.502 | yes |
| 0.20 | 1.000 | 0.208 | 0.318 | 0.500 | yes |
| 0.30 | 1.000 | 0.365 | 0.419 | 0.499 | yes |
| 0.40 | 1.000 | 0.969 | 0.485 | 0.496 | yes |

**Category capacity (at fixed ρ):** category(novel)=**1.0** for B = 4 · 8 · 16 · 32
(α up to 0.125), vs chance 0.25 → 0.031. **Max 32 categories abstracted.**

→ the abstract read-out is **1.0 on instances it has never seen**, while **instance**
recall stays low until instances are so jittered (ρ=0.4) they nearly span the space.
The two move **independently** — category knowledge is **not** instance memorization,
i.e. **the levels genuinely separate**. The boundary is set by *within < between*
geometry (separable across the whole sweep), not a tuned threshold. **Grade [V].**

*Honest reading:* high category-acc is **easy** when prototypes are orthogonal (the
basins are wide); the non-trivial content is that it **holds on novel instances** and
that instance/category **dissociate**. Instance recall rising with ρ is the lower level
finally getting distinct signatures, not a category effect.

---

## 3. [H3] compositional generalization — zero gap, generate new instances

A factorised concept is `bundle(bind(r_cat,C), bind(r_mod,M))` (depth-2). Each factor
is decoded by `unbind`+resonance over the **full** codebook. The test compares
**ENUMERATED** combinations (actually composed before) vs **HELD-OUT** combinations
(never built, composed on demand) — a **generalization-gap** test — and asks whether a
**generated** instance for a category is a **valid** member yet genuinely **novel**.

| K×J | combos | enumerated | **held-out** | gap | generated valid | generated novel |
|---|---|---|---|---|---|---|
| 6×6 | 36 | 1.000 | 1.000 | +0.000 | 1.000 | 1.000 |
| 10×10 | 100 | 1.000 | 1.000 | +0.000 | 1.000 | 1.000 |
| 16×16 | 256 | 1.000 | 1.000 | +0.000 | 1.000 | 1.000 |
| 24×24 | 576 | 1.000 | 1.000 | +0.000 | 1.000 | 1.000 |

**Hold-out fraction** 0.25 / 0.50 / 0.75 → gap **0.00** throughout (the split size is
irrelevant — nothing is "trained"). **Depth:** depth-2 levels (cat 1.0, mod 1.0);
**depth-3** super-ordinate/category/modifier = **1.0 / 1.0 / 1.0** with a **genuine**
extraction (undo the per-level permute on the *whole* composite to expose the inner
bundle — the outer super-term becomes crosstalk — then unbind; **not** a rebuilt inner).

→ **systematic generalization with no train/test gap** — the property neural nets must
learn case-by-case is **structural** here, because `bind`/`unbind` is
combination-agnostic. Generated instances are valid category members **and** distinct
from every composed exemplar. **Grade [V].** *Limit:* the ceiling is bundle crosstalk at
very high load (not reached by 576 here; read off the sweep when it appears).

---

## 4. [H4] hierarchy vs flat — nesting breaks the ceiling (criterion-dependent)

The decisive test. The **same** T = m·B instances are stored two ways: **FLAT** (one
Hebbian field over all T) vs **HIERARCHICAL** (B gated category sub-fields, correct
slow context). Instance recovery is scored under **two** read-outs: **argmax-id**
(argmax overlap over the whole codebook — forgiving for an easy cue) and **strict**
(settled overlap with the cued target **≥ 0.95** — the L0 full-clean-up capacity
criterion, **not** a new constant).

| T | α=T/N | flat **strict** | hier **strict** | Δ | flat (id) | hier (id) |
|---|---|---|---|---|---|---|
| 6 | 0.023 | 1.000 | 1.000 | +0.00 | 1.000 | 1.000 |
| 12 | 0.047 | 1.000 | 1.000 | +0.00 | 1.000 | 1.000 |
| 18 | 0.070 | 0.653 | 1.000 | +0.35 | 1.000 | 1.000 |
| 24 | 0.094 | 0.448 | 1.000 | +0.55 | 1.000 | 1.000 |
| 36 | 0.141 | 0.000 | 1.000 | +1.00 | 1.000 | 1.000 |
| 48 | 0.188 | 0.000 | 1.000 | +1.00 | 0.990 | 1.000 |
| 60 | 0.234 | 0.000 | 1.000 | +1.00 | 0.950 | 1.000 |
| 72 | 0.281 | 0.000 | 1.000 | +1.00 | 0.927 | 1.000 |

→ under the **strict** criterion the flat field **collapses near α≈0.06** (usable
T = **12**, then 0.65 → 0.45 → 0 by T=36) while the **gated hierarchy holds at 1.0 to
T=72** — usable T = **72**, a **~6× capacity multiplication**, max advantage **+1.00**.
The hierarchy keeps each sub-field light (≤ m instances) regardless of total T.
**Grade [V]: hierarchy breaks the flat ceiling.**

**Honest, central caveat — the advantage is criterion-dependent.** Under the
**forgiving** argmax-id read-out an easy 10%-corrupted cue is recovered far past the
strict wall (flat id-acc still 0.93 at T=72), so flat and hierarchical look the same
there. The ceiling break is real **for full attractor clean-up** (the capacity-relevant
regime), and is stated as such, not as an unconditional win. A second honesty point:
hierarchical recovery is **conditional on the correct slow context** (the gate). That is
not circular — **H1** shows the gate is just a **phase**, and **H2** shows the
**category is recoverable abstractly** from the instance itself, so the context is
**independently obtainable** rather than assumed.

---

## 5. Grade ledger

| Claim | Grade |
|---|---|
| nested phase coupling: slow phase **selects** the cued sub-field at all B (margin +0.92) | **[V]** |
| levels separate (gate width matters; sharp rejects, broad leaks) | **[V]** |
| abstraction: category from **novel** instances (1.0 to ρ=0.4, up to 32 categories) | **[V]** |
| instance vs category **dissociate** (independent read-outs) | **[V]** |
| compositional generalization: **zero** enum/held-out gap to 576 combos | **[V]** |
| depth-3 nested decode (sup/cat/mod = 1.0) via genuine permute-extraction | **[V]** |
| generate a new instance: valid member **and** novel | **[V]** |
| hierarchy breaks the flat ceiling under **strict** clean-up (~6×, T 12→72) | **[V]** |
| that capacity advantage under the **forgiving** id read-out | **[O]** (criterion-dependent; honest negative) |
| brain R / WM "~7" anchors used here | **not transferred** (gate centres structural, κ swept) |
| physical-medium realization | **[O]** theory track, deferred |
| felt quality | **[O]** firewall |

---

## 6. Honest negatives / limits

- **The capacity win is criterion-dependent.** It is decisive under strict full
  clean-up (overlap ≥ 0.95) but **vanishes** under a forgiving argmax-id read-out of an
  easy cue. Recorded as an **[O]** alongside the **[V]**, not hidden.
- **Hierarchical recovery assumes the correct gate** (slow context). H1 (gate = phase)
  and H2 (category recoverable abstractly) make the context independently obtainable,
  but a *single* end-to-end loop that **infers** the gate from a raw cue and **then**
  routes is **not** built here — that is exactly **L4 (resonance / inference)**, the
  next chunk, whose dependency this brings forward.
- **Abstraction is easy with orthogonal prototypes** (wide basins). The non-trivial
  content is novel-instance generalization + instance/category dissociation, not the
  bare 1.0.
- **H3 high-load ceiling not reached** (gap still 0 at 576 combos); the crosstalk limit
  exists but is beyond the swept range — stated, not extrapolated.
- All on the **in-silico** substrate; physical realization remains deferred.

---

## 7. Next (blueprint L4 — resonance / inference) ★ pivot

See `BLUEPRINT_toward_ultimate_computer.md` §5·§12. The L3 results close hierarchy but
expose the next dependency directly: a hierarchical field is powerful **once correctly
gated**, and H2 shows the category is abstractly recoverable — so the next chunk **S5 =
L4 start: resonance-as-inference**. Build the single closed loop that **resonance-reads
the slow context (gate) from a raw cue** and **then** routes to the fast sub-field
(H1+H2 composed into one pass), turning the "assume the gate" caveat of H4 into a
**derived** gate. Then iterative resonance for **best-match / nearest-concept** retrieval
and simple **inference** (fill a missing factor by resonance over the hierarchy).
**Stress:** the inferred gate is wrong often enough to erase the H4 capacity advantage
→ record the limit and restart that line with the break applied.

One session, one zip, additive. If broken, restart with the break applied.

---

*— v0.4. Reproduce: `python3 repro/wave_hierarchy_core.py` (deterministic, digest
`ea4c6723…`); figure `python3 repro/make_figure_v0_4.py`. Substrate from v0.1; binding/
bundle/permute from v0.2 (`SESSION_v0_2_resonance_and_learning.md`) and v0.3
(`SESSION_v0_3_structure_and_time.md`).*
