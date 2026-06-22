# SESSION v0.6 — L5 dual learning systems (fast episodic + slow semantic)

**Module:** `repro/wave_consolidation_core.py` (reuses L0 `wave_compute_core` one-shot
R3 + attractor clean-up, and L3 `wave_hierarchy_core` gating — exact, non-circular;
nothing frozen edited). **Figure:** `repro/wave_consolidation_atlas.png` (6 panels).
**Digest:** `e8a623005831d49b…` (deterministic, bit-for-bit, single-core OpenBLAS).
**Firewall:** `consciousness_claim = 0`, `hard_problem_open = 1`.
**`new_tuned_constants = 0`.**

---

## Why this session

L4 closed four of five inference forms but left **one principled debt on the books**:
the strict-fidelity capacity advantage (H4's ~6×) does **not** survive a gate **derived
from content**, because derivability needs a shared schema, a shared schema **correlates**
instances, and correlation trades **directly** against strict instance-separability — no
single content-derived operating point has both. L4 named the only escape: an
**independently-supplied context channel**. L5's job is to build that channel as the
contents of a **slow semantic store**, and — separately — to test the textbook
**complementary-learning-systems (CLS)** picture on this substrate: a fast one-shot
episodic store (R3, reused exactly) plus a slow store filled by **offline replay**, with
the standard stress (catastrophic forgetting) and the standard claim (a fast/slow
**double dissociation**). Each claim carries a sweep and a break built to refute it.

---

## What was built and found (each claim with a sweep; honest negatives kept)

The L5 mechanism sits entirely on the L0 substrate. The **fast** store is `hebbian_field`
over raw instances (R3, one-shot). **Consolidation** is offline replay: for each cycle,
reactivate a stored episode (high-fidelity — phase jitter, **no** bit corruption), settle
it in the fast field (clean-up), and Hebbian-accumulate the binary reconstruction into the
**slow additive** store (non-circular: the slow store is never handed a prototype, only
reconstructed instances). The **palimpsest** baseline `J ← (1-ε)J + ε·xxᵀ/N` is the
standard recency-biased (catastrophic) forgetting model. `ε` swept, not tuned.

### C1 — consolidation builds a GENERALISING slow store  **[V]**  (with two honest bounds)
Stream `L` prototype-clustered instances per category one-shot into the fast field,
consolidate by replay into the slow field, then probe on **NOVEL never-stored** instances
and read overlap with the **true prototype** (never imprinted). The slow store generalises
well above the single-instance baseline `1-2ρ = 0.70` and rises from a too-short stream
into the consolidated regime: semantic overlap `L=2 → 0.68`, `L=4 → 0.87`, `L=8 → 0.86`
(consolidated mean `0.84`). **The verified claim is exactly this:** replay turns one-shot
episodes into a **separate, persistent** store that generalises to novel instances.

**Two honest bounds, recorded not hidden (both point to C4):**
- The slow store does **not** out-generalise the **fast** store. The fast (episodic)
  Hebbian field already superposes its instances into an **emergent prototype**, so it
  scores *equal or higher* on the prototype at every `L` (`sem−epi < 0` throughout; fast
  reaches `≈1.00` at `L=16`). The value of consolidation here is a **separate store**
  (demonstrated in C2), **not** an abstraction the fast store lacks.
- **More replay does not keep denoising.** Replay `1 → 0.91`, `3 → 0.86`, `6 → 0.81`.
  Each cycle re-samples the **same fixed (biased) instance set**, so repetition entrenches
  that sample's bias rather than averaging fresh draws — the naïve `variance ∝ 1/(n·L)`
  argument fails because the draws are not independent. One pass is enough; the docstring
  was corrected to state this.

### C2 — dual store reduces CATASTROPHIC FORGETTING  **[V]**  (comparative, sign-stable)
`K` tasks (one category each) arrive **sequentially**. Both systems share the **same**
fast palimpsest buffer; the dual system **only** adds the slow additive store fed by
replay (fair isolation — the dual system adds nothing but the slow store). After all
tasks, recognise the **first** task's novel instances (argmax over all `K` prototypes,
non-circular). Probes are drawn from a **separate rng independent of replay**, so the
single baseline is replay-invariant and single-vs-dual is **paired**.

Single-store forgetting is catastrophic and grows with load (`K=2,4,6,8 →
0.44, 0.36, 0.56, 0.67`); dual forgetting stays far lower at **every** point
(`0.00, 0.08, 0.00, 0.22`), beating single at **every** `K` and **every** replay amount,
gap `> 0.2` across the `K` sweep. **Honest caveat (recorded):** the dual store does **not**
forget *zero* — its slow store has finite capacity, so dual forgetting itself grows slowly
with `K` (0.00 → 0.22). The verified claim is the **sign-stable comparative advantage**
(dual ≪ single everywhere) — precisely the catastrophic-forgetting benefit a complementary
slow store is meant to confer. (The blueprint's single-system fallback is **not** triggered.)

### C3 — the L4 [O] → [V] CLOSURE: an INDEPENDENT context channel  **[V]**  (headline)
`B` categories × `m` **independent** instances (strict-separable, the H4 regime). Category
identity rides a **separate context tag** `κ_b` (independent of instance content) — the
slow store's contents. At recall an instance cue **and** a (corruptible) context cue
arrive. Four arms: **content-derived** gate (L4's loser), **context-channel** gate (L5),
**oracle**, **flat**; score **strict** recovery (overlap ≥ 0.95).

L4's trade-off is **reproduced** in the content arm: as load grows it **degrades**
(gate `0.98 → 0.73`; content strict `0.98 → 0.68`) — weak category centroids leak some
signal but not enough. The **context channel does not pay that price**: gate `= 1.00` and
strict recovery `≈ oracle` at **every** load (strict `1.00, 1.00, 0.95` vs flat
`0.33, 0.00, 0.00`), **exceeding** the content arm at the strict wall by a clear margin
(`0.95` vs `0.68` at `T=72`), and **robust** to context-cue corruption up to `0.3`
(gate stays `1.00`). The independent channel **escapes** the derivability ⊥ separability
trade-off — **the L4 [O] is closed to [V], exactly as L4 predicted.** Recorded boundary:
heavy context-cue corruption eventually degrades the gate.

### C4 — the CLS DOUBLE DISSOCIATION does NOT hold  **[O]**  (honest negative)
Two distinct, imprint-independent read-outs: **memorisation** = recall of a literally
**stored** instance (argmax over the stored codebook); **generalisation** = category
recognition of a freshly drawn **novel** instance (argmax over prototypes). The textbook
CLS picture predicts a **double** dissociation (fast wins memorisation, slow wins
generalisation). **Half of it fails on this substrate.** The fast store **does** win
memorisation at high within-category spread (`ρ=0.30`: `0.97` vs `0.22`) — but it **also**
generalises essentially perfectly (`fast gen ≈ 1.00` at every `ρ`) because an additive
Hebbian field superposes its instances into an emergent prototype. So the slow store
**never** out-generalises the fast store, and only a **single** dissociation holds: the
slow store trades instance fidelity for a **persistent, compressed, interference-resistant**
store (the value shown in C2), **not** for a sharper abstraction. The break is recorded;
the next session inherits it.

---

## L5 verdict (honestly)

**The dual architecture earns its keep — but for a different reason than the textbook
gives.** Consolidation builds a **separate generalising store** (C1 [V]); that separate
store **greatly reduces catastrophic forgetting** (C2 [V]); and supplied as an
**independent context channel** it **closes L4's one open limit**, restoring strict
capacity to oracle level where content-derivation could not (C3 [V] — the headline).
What does **not** hold is the textbook **double dissociation** (C4 [O]): on a single
Hebbian substrate the **fast store already generalises for free** (superposition →
emergent prototype), so the two stores are functionally separated by
**persistence/capacity**, not by an abstraction the fast store lacks. **Three of four
lines [V]; one principled negative [O], with its mechanism named.**

**Discipline upheld.** Every claim swept and sign-stable; read-outs are argmax over the
full codebook / true-prototype overlap on **novel** probes (non-circular); the C2 probe
stream is decoupled from replay so the comparison is **paired** and the baseline
**replay-invariant**; two false sub-claims surfaced during grading (a) "slow out-abstracts
fast" and (b) "more replay denoises" were **disclosed and corrected in the code and
docstrings** rather than tuned away (the Stress Principle applied to the *method*); brain
anchors (R=0.39, WM~7) **not** transferred; firewall held at every step; digest reproduces
bit-for-bit on a single core.

**Layer status after S6. L5 dual learning systems — MET & GRADED.** Mostly positive
(3/4 lines [V], including the L4 [O]→[V] closure); one honest structural limit ([O]) with
its substrate mechanism named. Exposed dependency → **L6 self-supervised world model**
(prediction as forward settling; learning the substrate's own dynamics from unlabeled
streams), inheriting the C4 break: any "two-system" story downstream must justify the
second system by **persistence/capacity**, not by an abstraction the fast store lacks.

**Artifacts.** `wave_consolidation_core.py` (+`wave_consolidation_results.json`
+`wave_consolidation_atlas.png` +`expected_digest_v0_6.json`), `make_figure_v0_6.py`
(6-panel C1 / C1-bound / C2 / C3-closure / C3-robustness / C4). `check_completeness.py`
updated to re-run and pin this module. Digest `e8a623005831d49b…`, deterministic.
