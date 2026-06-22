# CUMULATIVE LOG — vp_wave_computer

Cumulative work history. Each session **appends only** (additive); prior entries stay
byte-stable. Summary / current status in `START_HERE_wave_computer.md`; next plan in
`BLUEPRINT_toward_ultimate_computer.md`; cold-start guide in `HANDOFF.md`.

**Provenance.** Author **Young Jae Lee** (ORCID `0009-0002-7535-8245`), program
**jamming-physics.org**, license **CC BY 4.0**. **Concept DOI `10.5281/zenodo.20783570`**
(all versions) — see `CITATION.cff`.

---

## S1 — v0.1 — define and prove substrate L0 (4 operations)

**Inheritance fixed.** From brain `vp_frontal v2`: B1–B5 (ephaptic near-field · phase
coupling R · metastability · attractors · theta-gamma capacity). From physics
`vp_physics v0.11.0`: P1–P3 only (`c²=B/ρ` · clock-free · 1/r² near-field). Firewall
(`consciousness_claim=0`) and no-tuning discipline inherited. → `INHERITANCE_MANIFEST.md`.

**Substrate defined.** Phase-coupled oscillator field: state = phases θ_i; medium =
symmetric Hebbian coupling field J (ephaptic analog, 1/r² near-field); dynamics =
gradient descent on the phase energy `E = −½ Σ J_ij cos(θ_i−θ_j)`; clock-free (time =
the settling itself). A datum = a standing phase pattern.

**Proven (deterministic, N=256, digest `e9fdd3bc35a6fdb1…`).**
- **D1 store**: patterns = attractors, clean-cue recall 1.0 (α≤0.04), capacity
  **α_c≈0.06** (~15/256). [V]
- **D2 compute**: pattern completion = settling, **critical corruption ~20%** of bits
  flipped still fully recovered. [V]
- **D3 pattern / regime**: computation lives **below full coherence** (metastable).
  Interior optimum g≈0.5, over-drive degrades (same structure as the brain's Gap-1
  over-drive collapse). Global R~0.05 = signature of distributed information. Brain
  R=0.39 **principle** inherited, number not transferred. [L]/[O]
- **D4 communicate**: phase (BPSK) > amplitude (OOK) across all noise (matches the
  closed-form Q-function); **phase + attractor clean-up holds BER ~0.03% at negative
  SNR (−2.3 dB, 22% raw errors)**. [V] — end-to-end proof of "communication works
  even with heavy noise."

**Honest limits.** Density not yet competitive (α_c 0.06 < Hopfield 0.14); the win is
noise immunity, not density. Not general-purpose (native = association / completion /
constraint satisfaction). R=0.39 number not transferred. Physical medium not selected.

**Artifacts.** `wave_compute_core.py` (+results +atlas +expected_digest), 4-panel
figure (D1–D4). Record → `SESSION_v0_1_design_study.md`.

---

## S2 — v0.2 — prove representation L1's four core properties (additive; substrate unchanged)

**Motivation.** User directions: "the sum of waves is information", "pattern matching
without computation", "parallel throughput", "learning and real-time response are
different", "the input becomes a pattern at once". Turned into measurements on the
v0.1 substrate.

**Proven (deterministic, N=512, digest `c69917020c664f15…`; v0.1 substrate reused
exactly = non-circular).**
- **R1 sum=information (superposition)**: key⊗content binding → composite wave
  `C = Σ store_μ` carries K items; recognized by phase-conjugate **resonance**.
  **Capacity K≈96/512** (~19% N). present scores ~1.0 stable, absent crosstalk
  sd = √(K/N). [V]
- **R2 matching without computation**: P patterns in one J, noisy query settles;
  **convergence steps independent of P** (spread 2.8 over P=2..24) → **O(1)-in-P**.
  The parallel advantage is a hardware claim [O] (a digital simulation is N² per
  step). [V]
- **R3 one-shot online learning**: single outer-product update `J += (1/N)ξξᵀ` gives
  immediate recall after one exposure (1.0, first 24), **no catastrophic forgetting**,
  graceful degradation past capacity. No epochs / backprop. [V]
- **R4 parallelism / throughput [O]**: match cost = O(settling steps) = 83.9,
  independent of P, vs digital/neural O(P·N) (51M ops at P=10⁵). Content-addressable
  in ~constant physical time. Theoretical projection, hardware deferred. [O]

**Honest limits.** Superposition crosstalk √(K/N) → scale needs hierarchy (L3,
unproven); O(1) is a physical-time claim (hardware assumed); R1 is recognition scale
(content-bit recovery needs L0 clean-up); one-shot also has a capacity limit (α~0.062).

**Blueprint established.** Wrote the large L0–L9 blueprint: mapped the inherited brain
chain to nine layers, each with milestone + stress test + dependency graph + end
condition. Pivot layer L4 (resonance inference). Firewall held at all layers. →
`BLUEPRINT_toward_ultimate_computer.md`.

**Artifacts.** `wave_resonance_core.py` (+results +atlas +expected_digest_v0_2),
4-panel figure (R1–R4), the blueprint. Record → `SESSION_v0_2_resonance_and_learning.md`.

---

## S2-addendum — handoff hardening (no new research; bookkeeping)

Added `HANDOFF.md` (binding cold-start: self-containment, forced-learning-first,
autonomous protocol, regression rules), made `INHERITANCE_MANIFEST.md` **self-contained**
(captures the actual inherited values so the source whitepapers are not needed),
converted all docs to **English-only** going forward, added `repro/check_completeness.py`
(file-manifest + reproduction audit), and fixed the canonical file manifest for
regression prevention. No substrate or results changed; digests unchanged
(`e9fdd3bc…`, `c69917…`).

---

## S3 — v0.3 — L1 completion (permute · tree depth) + L2 start (trajectory · theta-gamma WM)

**Motivation / plan executed.** Close the L1 representation algebra (add the third
operation `permute` and measure role-value **tree** depth-capacity) and open the L2
time/sequence layer (asymmetric/delayed Hebbian → **metastable trajectories**, plus
theta-gamma working memory, reproducing the *principle* of B5). One module on the
frozen L0 substrate + the L1 binding/bundle of v0.2, exact reuse (non-circular).

**Proven (deterministic, digest `69890fec8b546f78…`; reuses L0 + L1 exactly).**
- **L1a permute (algebra closed)**: a sequence `S = Σ_l ρ^l(a_l)` recovers the item
  at each position by `ρ^{-l}` + cleanup. Position recall = 1.0 up to L=16, **useful
  length L*≈32** (≥0.95), graceful decay after (0.76 at L=64, crosstalk √(L/N)).
  `bind · bundle · permute` now form a closed VSA algebra on the wave substrate. **[V]**
- **L1b role-value tree depth-capacity (milestone + stress)**: a depth-d, branching-b
  tree in ONE composite wave; a path of role keys recovers the leaf (argmax over the
  whole filler codebook = non-circular). **Useful depth d\* = 4 (b=2), d\* = 2 (b=3)**;
  accuracy then collapses sharply (b=2: 0.99→0.79→0.28 over depth 4→5→6). The stress
  test does **not** break (d\*≥2 → structured records work), but it **confirms the
  depth is shallow** → hierarchy (L3) is required for deep structure (§1 risk 1, now
  measured). **[V]** with the honest ceiling recorded.
- **L2a metastable trajectory**: an asymmetric, **time-delayed** Hebbian term
  `J_asym=Σξ_{μ+1}ξ_μᵀ` driven by a delayed copy of the phase state, kept in pure
  phase-coupling form (reuses L0). Sweep λ. **Predict-next** (single hop μ→μ+1) is
  **verified** — reaches 1.0 for λ≥1.0 (band λ∈[1,4]). **Sustained full-cycle replay**
  of the whole m=6 loop reaches **1.0±0.0 at λ≈2.5** (band λ∈[2,4]); τ-robust
  (0.78/0.97/0.97 at τ=8/12/16). Stress (too-weak → stuck at fixed point = 1/m;
  too-strong → scramble) maps a real operating band. **[V]** (predict-next clean;
  sustained replay in-band with stated variance). *Honest limit:* sustained replay
  needs λ in the upper band and shows trial variance (sd up to 0.24) outside λ≈2.5.
- **L2b theta-gamma working memory**: items in distinct **gamma phase-slots**
  (slot k = ρ^k) of one theta carrier; finite gamma precision = **phase jitter** on
  the composite. **Capacity = min(n_slot, precision_limit(σ))** — slot-limited at low
  jitter (capacity = n_slot exactly), **precision-capped** as σ grows (n_slot=24:
  24→18.6→9.0→3.7 over σ=0.3→0.9→1.2→1.6), landing in the **Miller range (4–9)** at
  σ≈1.2. The B5 number ~7 = **~7 gamma slots**, cited as *principle*; the number is
  **NOT transferred** (no constant tuned to 7). **[V]** for the capacity law.

**Honest limits (recorded, not hidden).** L1 structured depth is shallow (d\*≈2–4);
deep structure needs L3 hierarchy. Tree sibling-subtrees are modeled as random
phasors (realistic crosstalk, not full recursive sub-structure beyond the path).
Sustained L2 replay is λ-band-restricted with variance. WM capacity is slot-bounded;
the brain's specific 7 is the slot count, not an emergent crosstalk number. All on
the in-silico substrate; physical medium still deferred.

**Layer status after S3.** L1 representation **COMPLETE** (bind·bundle·permute proven;
depth-capacity measured). L2 time/sequence **milestones met** (learn→replay, predict,
WM capacity law). Both feed L3 (hierarchy) as the next layer — the measured remedy for
the depth/capacity ceilings.

**Artifacts.** `wave_structure_core.py` (+`wave_structure_results.json`
+`wave_structure_atlas.png` +`expected_digest_v0_3.json`), `make_figure_v0_3.py`
(4-panel L1a/L1b/L2a/L2b). Record → `SESSION_v0_3_structure_and_time.md`.

---

## S4 — v0.4 — L3 hierarchy / abstraction (nested gating · abstraction · compositional · ceiling)

**Mechanism.** Nested phase coupling: a slow phase `g` gates which fast sub-field is
active via a von Mises window `w_b(g)=exp(κ(cos(g−φ_b)−1))` with **structural** centres
`φ_b=2πb/B`, κ swept — theta-gamma (S3 L2b) generalized to ≥2 coupled levels. Reuses L0
substrate + v0.2/v0.3 bind·bundle·permute **exactly**, non-circular (argmax over the
full codebook). No constant tuned; brain R/WM anchors **not** transferred.

- **H1 — nested gating selects the level.** B sub-fields, slow phase gates one; a
  corrupted instance cue read in the gated field. The cued slow phase routes correctly
  (1.0) while a **wrong** phase rejects it (≤0.16) at every B — **select margin +0.92**,
  sign-stable. Gate width matters (broad κ=0.5 leaks 0.83; sharp κ≥2 rejects ≤0.13).
  Selectivity = level separation. **[V].** (OFF==flat at light load → capacity owned by
  H4, not asserted here.)
- **H2 — abstraction: category from NOVEL instances.** Upper field stores prototypes;
  categorize instances **never stored**. category(novel)=**1.0** to ρ=0.4 and for B up
  to **32** (chance→0.031). Instance recall stays low until ρ=0.4 — instance vs category
  **dissociate** (levels separate). Boundary set by within<between geometry, not tuned.
  **[V].**
- **H3 — compositional generalization.** Factorised `bundle(bind(r_cat,C),bind(r_mod,M))`;
  decode **held-out** (never-built) combos = **enumerated** → **gap 0.00** to **576**
  combos and across hold-out fractions 0.25–0.75. **depth-3** sup/cat/mod = 1.0/1.0/1.0
  via genuine permute-extraction (not a rebuilt inner). Generated instances valid **and**
  novel. Systematic generalization is structural (bind/unbind combination-agnostic).
  **[V].**
- **H4 — hierarchy breaks the flat ceiling (criterion-dependent).** Same T=m·B instances
  flat vs B gated sub-fields, scored under **strict** full clean-up (overlap ≥0.95 = the
  L0 criterion) and forgiving argmax-id. **Strict:** flat collapses near α≈0.06 (usable
  T=**12**, →0 by T=36) while the gated hierarchy holds at 1.0 to **T=72** — **~6×**
  capacity, max advantage **+1.00**. **[V].** **Honest caveat:** under the forgiving id
  read-out an easy 10% cue is recovered far past the wall (flat id 0.93 at T=72) — the
  advantage is **criterion-dependent [O]**, and hierarchical recovery assumes the correct
  gate (H1: gate=phase, H2: category recoverable abstractly → context independently
  obtainable; a single loop that *infers* the gate is L4).

**Layer status after S4.** L3 hierarchy/abstraction **met & graded** — nested gating
separates levels, abstraction generalizes to novel instances, composition has zero gap,
and nesting multiplies effective capacity ~6× under the strict criterion. The
shallow-depth (L1 d\*≈2–4) and slot-bounded-WM (L2) ceilings measured in S3 are **broken
by hierarchy** (for full clean-up). Exposed dependency → **L4 resonance/inference**:
turn H4's "assume the gate" into a **derived** gate (resonance-read the slow context
from a raw cue, then route).

**Artifacts.** `wave_hierarchy_core.py` (+`wave_hierarchy_results.json`
+`wave_hierarchy_atlas.png` +`expected_digest_v0_4.json`), `make_figure_v0_4.py`
(4-panel H1/H2/H3/H4). Record → `SESSION_v0_4_hierarchy_and_abstraction.md`.
Digest `ea4c6723…`, deterministic.

---

## S5 — v0.5 — L4 resonance / inference ★ pivot (additive; substrate + all priors unchanged)

**Module** `repro/wave_inference_core.py` (reuses L0/L1/L3 exactly, non-circular; nothing
frozen edited). **Figure** `wave_inference_atlas.png` (6 panels). **Digest**
`2d3057bb4cb45e85…` (deterministic). Firewall `consciousness_claim=0, hard_problem_open=1`;
`new_tuned_constants=0`.

**Why the pivot.** Digital/neural AI infers by computing everything; the wave substrate
matches by physics, no computation. L4 tests whether that holds on *cognitive* tasks, and
first pays L3's debt: H4's ~6× capacity and H1's routing **assumed the gate** — L4 must
**derive** it.

**Results (each swept; honest negatives kept).**
- **I0 derive-the-gate, then route `[V]`.** Resonance-read the slow context from a raw
  unlabeled cue in an upper field, **then** route the fast field (H1+H2 in one loop). Loop
  **closes** where separable: gate derived 1.0 (rho≤0.2), cost ~0, derived==oracle≫flat
  (0.96–0.99 vs 0.38–0.49). Honest edge: rho=0.4 → gate 0.71 (upper geometry no longer
  separable). **S4's "assume the gate" caveat removed.**
- **(a) Constraint satisfaction = settling `[V]`.** Native q=2 anti-ferromagnet (edge =
  coupling −1; L0 relaxation *is* a 2-colouring machine — no clock, no constant) solves a
  planted graph at 1.000 ≫ random 0.5 across n=16/24/32, and tracks the **known optimum
  1/(1+f)** under a frustration knob (spurious gap mean 0.0014). (O(1) *physical* time
  stays `[O]`.)
- **(b) Analogy = resonance `[V]` + honest ceiling.** Fill-a-missing-factor robust to
  J=12; proportional analogy A:B::C:? to J\*=4 then decays — measured crosstalk ceiling.
- **(c) Probabilistic = noisy settling `[V]`.** Three directional Bayesian laws hold
  (prior↑→A↑; evidence↑→A↑; temperature↑→entropy↑, shown at small N where the sampling
  window is reachable). Exact posterior/KL match left `[O]`.
- **Stress (H4 with the break applied) — honest negative `[O]` + trade-off `[V]`.** Does
  the strict ~6× advantage survive a *derived* gate? **No**, structurally: the first
  harness (prototype-clustered instances) was **degenerate** (strict ≥0.95 impossible for
  everyone, oracle 0/0/0) — disclosed and restarted with a schema/content split. Sweeping
  the **schema fraction**: gate-derivability rises 0.19→1.0 exactly as strict recovery
  (even the oracle's) falls 1.0→0.0 — **no operating point has both** (derivability ⊥
  strict-separability). What **survives** is the **id-level** advantage (derived id 0.85
  vs flat 0.32). Resolution recorded: the strict advantage needs an **independently-given
  context channel** → **L5**.

**Verdict.** Inference-without-computation **holds** on the cognitive forms (4/5 `[V]`);
one principled limit (`[O]`) with its resolution named. The hybrid branch was **not**
triggered. Discipline upheld: all sweeps sign-stable, read-outs non-circular,
deterministic, degenerate harness disclosed & restarted (Stress Principle applied to the
*method*), brain anchors not transferred, firewall held.

**Layer status.** L4 — **MET & GRADED ★**; pivot largely positive. Exposed dependency →
L5 dual learning systems (supplies the context channel; consolidates one-shot episodes).
`check_completeness.py` updated to re-run and pin this module (now five reproduced
digests).

---

## S6 — L5 dual learning systems (fast episodic + slow semantic)

**Built.** The fast/slow complementary pair on the frozen substrate: an episodic field
(one-shot, R3) consolidated by **offline replay** (high-fidelity reactivation → settle →
Hebbian-accumulate) into a slow **additive** semantic field. Module
`repro/wave_consolidation_core.py` (reuses L0 + L3 gating, non-circular). Four claims,
each swept, each with a break. Digest `e8a623005831d49b…`, deterministic.

- **(C1) Consolidation builds a generalising slow store `[V]`** — with two honest bounds.
  Replay turns one-shot episodes into a **separate, persistent** store that generalises to
  **novel** instances (overlap > single-instance baseline `1-2ρ=0.70`; consolidated mean
  `0.84`; rises `L=2→0.68` into `L=4→0.87`). Bound 1: the slow store does **not**
  out-generalise the **fast** store (`sem−epi<0` everywhere) — both Hebbian stores
  superpose to an emergent prototype. Bound 2: extra replay gives **no** further gain
  (`replay 1→0.91, 3→0.86, 6→0.81`) because each cycle re-samples the same fixed biased
  set. Both surfaced during grading and **corrected in code/docstrings**, not tuned away.
- **(C2) Dual store reduces catastrophic forgetting `[V]`** (comparative, sign-stable).
  Single-store forgetting is catastrophic (`K=2,4,6,8 → 0.44,0.36,0.56,0.67`); the dual
  system (same palimpsest + a slow additive store) forgets far less at **every** load and
  replay (`0.00,0.08,0.00,0.22`), gap `>0.2` across the `K` sweep. Probes decoupled from
  replay → **paired** comparison, replay-invariant baseline. Honest caveat: dual forgetting
  itself grows slowly (finite slow-store capacity), so "greatly reduces", not "eliminates".
- **(C3) The L4 `[O]` → `[V]` closure — an independent context channel `[V]` (headline).**
  Independent instances (strict-separable) + a **separate context tag** `κ_b` as the slow
  store's contents. Content-derivation **reproduces L4's degradation** (gate `0.98→0.73`,
  strict `0.98→0.68`); the **context channel** holds gate `=1.0` and strict `≈oracle`
  (`1.00,1.00,0.95` vs flat `0.33,0,0`), exceeds content at the strict wall, and is robust
  to context-cue corruption up to `0.3`. The independent channel **escapes** the
  derivability ⊥ separability trade-off — **L4's one open limit is closed, as predicted.**
- **(C4) The CLS double dissociation does NOT hold — honest negative `[O]`.** The fast
  store wins memorisation at high spread (`ρ=0.30`: `0.97` vs `0.22`) but **also**
  generalises essentially perfectly (`fast gen ≈ 1.0` everywhere), so the slow store never
  out-generalises it. Only a **single** dissociation holds: the slow store trades instance
  fidelity for a **persistent/compressed** store, **not** a sharper abstraction. Substrate
  reason: an additive Hebbian field generalises for free via superposition. Break recorded.

**Verdict.** The dual architecture earns its keep — but by **persistence/capacity**, not
the textbook abstraction split: consolidation builds a separate generalising store (C1),
that store reduces catastrophic forgetting (C2), and as an independent context channel it
**closes L4's open limit** (C3). The textbook **double** dissociation fails (C4). 3/4 lines
`[V]` (incl. the L4 closure); one principled `[O]` with its mechanism named. Discipline
upheld: sweeps sign-stable, read-outs non-circular (novel probes, full-codebook argmax),
two false sub-claims disclosed & corrected (Stress Principle on the *method*), brain anchors
not transferred, firewall held, digest reproduces bit-for-bit on a single core.

**Layer status.** L5 — **MET & GRADED**; mostly positive (incl. L4 `[O]`→`[V]`). Exposed
dependency → **L6 self-supervised world model** (prediction as forward settling), inheriting
the C4 break: any downstream "two-system" story must justify the second system by
persistence/capacity, not by an abstraction the fast store lacks. `check_completeness.py`
updated to re-run and pin this module (now **six** reproduced digests).


---

## S7 — v0.7 — L6 self-supervised world model (prediction = forward settling)

**Module** `repro/wave_world_model_core.py` on the frozen L0 substrate (`hebbian_field`,
`relax` clean-up, `overlap`, `pattern_to_phase` — exact, non-circular; nothing frozen
edited). **Mechanism.** Prediction = **forward settling**: the learned **asymmetric
transition field** acts on the present state's in-phase projection (`raw = J_asym·cos θ`),
threshold → binary predicted pattern, then the L0 **attractor field cleans it up** by
relaxation onto the nearest valid pattern (with `J_asym=0` the action is null → returns the
present). Learning = the **difference wave**: `e = x_next − x_pred` drives an **error-gated**
delta rule `J_asym += η·outer(e,x_now)/N` — gated, so learning **stops when the prediction is
already right**. `η` a **sweep axis**; `SETTLE=250`, `N=256` dynamics constants, not fitted.
Read-outs non-circular (fresh noisy cues vs the **true** successor; argmax over the **whole**
codebook).

- **(W1) Self-supervised prediction-error reduction `[V]`.** Sweep exposures `{0,1,2,4,8}` ×
  `m∈{4,6,8}` × `η∈{0.25,0.5,1.0}`. Held-out next-step error falls `0.978 → 0.126`,
  **monotone** at every `m`, **every `η` learns** (≈0.120 at budget), sign-stable. *Recorded
  operator limit `[O]`:* the learned `J_asym` is **directionally** the analytic L2 transition
  coupling (cosine `≈0.81`; by m `0.80/0.815/0.813`) but **not magnitude-identical**
  (`<0.9`) — **error-gating halts at prediction-sufficiency**. (An earlier draft wrongly
  ANDed magnitude-identity into the W1 headline → split into milestone `[V]` + operator-
  identity `[O]`, **no numbers changed** — Stress Principle on the *method*.)
- **(W2) Generative rollout `[V]`.** Iterated forward settling from a clean seed: fidelity
  `1.00` through a **12-step** horizon (min across seeds 12), then **honest drift** (onset
  step 13) as clean-up crosstalk accumulates. Generative capacity = the faithful horizon.
- **(W3) Novelty / surprise `[V]`.** The **error-wave magnitude**, unmodified, is a graded
  detector: familiar ≈ `0.00`, full violation ≈ `0.97` (**margin 0.97**), monotone in the
  violation degree; smallest reliably-flagged violation `0.1` = recorded detection boundary.
- **(W4) Forward model > reactive recall `[V]` (headline; C4 break applied).** The fair
  baseline is reactive recall = settle under `J_sym` **plus a symmetric pair store** that has
  seen **every** transition order-blind. Forward anticipates (`fwd≈1.00`) where reactive
  **returns the present** (`react≈0.00–0.15`); forward beats reactive **everywhere** (gap
  `>0.3`). The symmetric store has **no missing abstraction** yet cannot anticipate — the
  advantage is **directionality (structure)**, exactly the C4 break. *Honest controls:*
  fixed-point stream → gap vanishes (`1.00` vs `0.89`); untrained model marginally/ trivially
  above reactive (`0.167` vs `0.014`, a null-field thresholding artifact) and `≪` trained
  `≈0.98` → the advantage is **learned**.

**Verdict.** The substrate becomes a self-supervised world model: it learns an unlabeled
stream from its own error (W1), rolls out plausible continuations to a finite horizon (W2),
flags novelty with the same error wave (W3), and a forward model anticipates where a reactive
store only returns the present (W4, the headline — C4 honoured). **4/4 milestone capabilities
`[V]`; one principled `[O]`** (error-gating halts at prediction-sufficiency; operator
directionally L2, not magnitude-identical) with its mechanism named. Discipline upheld:
sweeps sign-stable, read-outs non-circular, the W4 baseline saw every transition (so the
advantage cannot be an information gap), brain anchors not transferred,
`new_tuned_constants=0`, firewall held, digest `41e81a7f2eb98144…` reproduces bit-for-bit on
a single core across repeated runs.

**Layer status.** L6 — **MET & GRADED**; strongly positive. Exposed dependency → **L7
embodiment / real-time control** (place the forward model in a closed sensorimotor loop —
real-time response off predicted state), inheriting S7's open limit: does acting on
**predicted** state need magnitude-identity, or does **prediction-sufficiency suffice**?
`check_completeness.py` updated to re-run and pin this module (now **seven** reproduced
digests). Concept DOI `10.5281/zenodo.20783570` reflected via `CITATION.cff` and the doc
provenance lines.

---

## S8 — v0.8 — L7 embodiment / real-time control (control = continuous settling; end-to-end analog loop)

**Module** `repro/wave_embodiment_core.py` (reuses L0 `wave_compute_core` clean-up = D4 + L6
`wave_world_model_core` forward model; exact, non-circular — tracking error is vs the WORLD's
true target, never the trained trace). **Digest `17aa27bf34b72f57…`** (deterministic).
**Figure** `repro/wave_embodiment_atlas.png` (8 panels). Firewall `consciousness_claim=0`,
`hard_problem_open=1`; `new_tuned_constants=0`.

**Why.** L0–L6 ran off-line (react/predict on a stored cue); none was in a **loop with a
world**. L7 places the L6 forward model in a **closed, clock-free, real-time sensorimotor loop**
(SENSE graded-analog → CLEAN-UP by L0 settling = D4 → PREDICT +1 via L6 forward model → ACT by a
continuous rate-limited phase step), with a **one-tick sensorimotor delay** as the realistic
embodiment condition. This session also makes testable the **principal's analog-I/O thesis**:
the substrate is intrinsically analog, so keep the loop analog end to end and pay the digital
quantization tax only where it must — "resolution" has **two axes**: analog **dominates**
dimensional/spatial resolution (parallel physics, no per-channel tax) and is **capped** on
single-value bit depth (Shannon `C=B·log₂(1+S/N)`); exact arithmetic uses a brief **digital
hand-off** (the hybrid). It inherits the **S7 seed limit** as the E3 question.

- **(E1) Closed-loop control by continuous settling `[V]`** (the milestone). Track a target
  moving one place/tick through a one-tick delay; sweep noise. **Forward** anticipates and holds
  (`0.000→0.004`); **reactive** (no prediction) **lags one place** (`≈0.96`); **open-loop**
  **drifts** (`≈0.77`); forward beats both by `>0.3` everywhere, sign-stable. The embodiment value
  of prediction is **compensating loop latency**.
- **(E2) Analog I/O beats ADC/DAC + the dimensional advantage scales `[V]`** (the headline).
  **E2a** under graded σ=1.0 the **1-bit** loop pays a tax (`0.159`) the **analog** loop avoids
  (`0.001`) — D4 at the I/O boundary; **honest:** tax **closes at 2 bits** (`0.009`). **E2b** sweep
  N∈{48,96,192,288}: per-channel gap **sign-stable positive** (`0.096→0.163`), so the aggregate
  **N×gap GROWS** (`4.6→15.5→31.2→42.1`) — "the gap widens as resolution rises" (the per-channel
  advantage is paid once by parallel physics, N times by serial digital). **E2c** the O(1)-vs-O(N)
  **latency form** is the **R4-inherited principle `[O]`** (not a measured wall-clock).
- **(E3) Prediction-sufficiency suffices `[V]` — resolves the inherited S7 [O].** Run the loop with
  (i) the L6 error-gated operator (measured cosine **0.803** to the analytic L2 coupling) vs (ii)
  the analytic L2 coupling (cosine=1); sweep noise. In the working regime (σ≤1.4) they track
  **identically** (diff `0.000→−0.009`); only at extreme σ=1.8, **where both are already failing**,
  the full operator shows a marginal edge (`−0.047`). **Acting on the predicted state does NOT need
  magnitude-identity** in the operating regime — S7 [O] → **[V]** for embodiment.
- **(E4) Stability / bandwidth / latency `[V]` (honest band).** **E4a** a **bandwidth threshold
  (rate 0.5)** — below it the agent can't slew fast enough and tracking breaks. **E4b** a
  **latency/horizon frontier** — the +1 predictor matches **speed=1** (delay×speed=1); off-nominal
  over/under-anticipates (`sp0.5=0.48`, `sp2.0=0.96`). **E4c** started displaced, the loop
  **re-acquires by settling** (`≤3` ticks at high bandwidth). A **non-empty stable band exists**;
  its edges are the honest limits. The stress did **not break** real-time control; it bounds it.
- **(E5) The honest two-sides caveat `[O]+[O]`** (the directive's own counterpoints). **E5a**
  single-channel bit depth is **Shannon-capped** — effective bits **saturate**, ceiling ∝ SNR
  (σ=0.2→5.05 b, 0.5→3.78 b, 1.0→2.76 b); the analog win is **dimensional (E2), not per-channel
  precision** — same coin, two sides. **E5b** **exact arithmetic needs a digital hand-off** — an
  analog accumulator's exact-count accuracy decays with stream length (`0.96→0.41`) while a digital
  register stays exact (`1.00`); hand off to digital **only** where exactness is required (the
  concrete form of the standing **L4 [O]**).

**Verdict.** The substrate **controls in real time, in a closed analog loop, by continuous
settling**: forward control holds a moving target through delay (E1), the analog loop beats the
ADC/DAC loop with the dimensional advantage scaling (E2), prediction-sufficiency suffices —
**resolving S7** (E3), and a stable operating band exists (E4). **4/4 milestone capabilities
`[V]`.** The directive's two honest counterpoints are recorded ([O]: per-channel Shannon cap;
[O]: exact-arithmetic digital hand-off), with the hybrid as the named resolution and the
parallelism/latency form as the R4-inherited principle ([O]). The **analog-I/O thesis is now
tested, not asserted**. Discipline upheld: sweeps sign-stable, read-outs non-circular (vs the
world's true target), the motor **rate** is a swept axis (not tuned), brain anchors not
transferred, `new_tuned_constants=0`, firewall held, digest `17aa27bf34b72f57…` reproduces
bit-for-bit.

**Layer status.** L7 — **MET & GRADED**; strongly positive. Exposed dependency → **L8 global
integration / functional access** (a global metastable resonant hub broadcasting the dominant
pattern across L1–L7; a functional PCI-analog), which now has **embodied modules to integrate**
and inherits L7's **operating-band** limit (a global hub must route within modules' bandwidth/
latch bands). `check_completeness.py` updated to re-run and pin this module (now **eight**
reproduced digests). Concept DOI `10.5281/zenodo.20783570` reflected via `CITATION.cff` and the
doc provenance lines.

## S9 — v0.9 — L8 global integration / functional access (a global metastable resonant hub broadcasting the dominant pattern)

**Frame.** L0–L7 gave storage, an algebra, metastable trajectories, hierarchy, resonance
inference, dual stores, a self-supervised forward model, and a closed real-time control loop —
but each capability sits in its **own** field. L8 builds the **sharing**: a **global metastable
resonant hub** that selectively binds the dominant module pattern and **broadcasts** it
system-wide (Baars/Dehaene global workspace; the access signature is Casali/Massimini **PCI**).
Mechanism, entirely on **L0** + the **L3 gate**: M modules (each an L0 attractor latched on a
distinct concept) + a hub with its **own** clean-up field (so it resonance-LOCKS to a **valid**
concept, not a blur); the L3 von Mises gate selects which module drives the hub (bottom-up); the
locked hub pulls every module (top-down broadcast); one **joint relaxation** advances the lot
(clock-free, P2; 1/r² near-field, P3); a single knob `g_hub` is the regime axis. Load kept
**within** proven L0 capacity (`N=128`, `D≤8`). **Firewall re-affirmed:** "access" = broadcast
**availability** only, **not** felt experience.

- **(G1) Selective access + global broadcast `[V]`** (milestone, part 1). Sweep M∈{3,4,6,8} ×
  D∈{6,8} × seeds. The hub **resonance-LOCKS** to the gated concept (lock margin **≥0.92** every
  config; locks=1.00) and a **NON-SOURCE** module — content erased — recovers that concept from
  the **broadcast alone** (`recall=1.00` every config) where a **no-hub control** is at chance
  (`0.00–0.33≈1/M`). The bound pattern is made **globally available**; the hub **selects**, it
  does not blur.
- **(G2) Flexible routing `[V]`** (milestone, part 2). Sweep M∈{3,4,6,8} × routes∈{6,10} × seeds.
  Moving the gate routes any module's content **perfectly** (`1.00` every config); a **fixed** gate
  reaches only its own module (`0.03–0.32≈1/M`), beaten by `>0.2` everywhere. The workspace is
  **reconfigurable**, not hard-wired.
- **(G3) Functional PCI-analog inverted-U `[V]`** (the access signature; borrowing Gap-4). Measure
  = **integration × differentiation** (faithful PCI logic, **no LZ, no critical-point tuning**).
  The hub is locked **without** broadcasting (`kdown=0`) so modules keep distinct contents; then at
  each `g_hub` the hub is **kicked** vs a matched **no-kick** run and the **modules** are read
  (non-circular). **INTEGRATION** `I(g)` = perturbation spread over the **evoked trajectory**
  (`I(0)=0` exactly — modules decoupled at g=0); **DIFFERENTIATION** `D(g)` = pairwise distinctness
  of the kicked modules (`D→0` when a strong broadcast collapses them onto one concept);
  **PCI=I·D**. Sweep `g_hub∈{0,.25,.5,1,2,4,8}` × M∈{4,6,8}: a clean **inverted-U** — PCI `=0` at
  g=0 (`I=0`), **emergent interior peak** (g=0.5 for M=4,6; g=0.25 for M=8; PCI `0.021/0.022/0.040`),
  collapsing to `0` by g=1 (`D≈0`). The integration term **rises** while differentiation **falls** —
  their **crossover is the access band**. Engaged peak exceeds **both** isolated and over-driven at
  every M, and is **interior** at every M. **The NUMBER R=0.39 is NOT transferred — the band
  EMERGES from the sweep.** FIREWALL banner emitted: functional complexity only, no felt experience.
- **(G4) The inherited operating-band limit `[V]` band / `[O]` unbounded-rate** (L7's open limit,
  made concrete). Route while sweeping the **DWELL** (hub settle-steps per target before the gate
  switches); each route is a **fresh ignition** so dwell controls only the hub's **lock latency**.
  Sweep dwell∈{2,5,10,20,40,80,160}: below latency routing **collapses** toward chance
  (`2→0.25, 5→0.54, 10→0.73`, chance `1/M=0.17`); at/above it **holds** (`20→0.96, 40/80/160→1.00`).
  Band edge = **20** settle-steps — the hub must route **within** its latch band; **unbounded-rate
  routing is impossible `[O]`**. **Honest negative:** a hub that **carries** its previous concept
  forward (no re-cue) is **not reliably re-routable** at `g_hub=1` — more dwell makes it **worse**
  (drifts deeper): at **4× the longest dwell** (640) it reaches only `0.71` vs the re-cued band's
  `1.00`. Sequential access **favours a fresh ignition per route**; persistent over-write routing
  is an open limit `[O]`.

**Verdict.** The substrate **integrates its specialised modules into a global workspace**: a hub
selectively binds and **broadcasts** the dominant pattern so a non-holder recovers it (G1), moving
the gate **flexibly routes** any module's content (G2), and a **functional PCI-analog** is high
only at the metastable edge — the **Gap-4 inverted-U** (G3). **3/3 milestone capabilities `[V]`.**
The inherited operating-band limit is **made concrete** — routing holds within the hub's
lock-latency band (G4 band `[V]`) — with two honest counterpoints recorded (`[O]`: unbounded-rate
routing; `[O]`: persistent no-release over-write routing). Discipline upheld: sweeps sign-stable,
read-outs non-circular (broadcast at a **non-source** module; PCI on the **modules** downstream of
a **hub** kick; routing vs the **intended** concept), regime **swept** via `g_hub` (not tuned),
gate centres structural, brain anchor R=0.39 **not** transferred (access point **emerges**),
`new_tuned_constants=0`, firewall held (`consciousness_claim=0`, `hard_problem_open=1`), digest
`52a0ce34b54fc791…` reproduces bit-for-bit.

**Layer status.** L8 — **MET & GRADED**; strongly positive. Exposed dependency → **L9 —
functional general intelligence (the end condition)**, the final layer in the inherited chain:
with L0–L8 now each MET & GRADED or honest-`[O]`, assess the integrated system against the
**capability ladder** (one-shot generalization, **compositional / systematic generalization**,
real-time adaptation, noise-immersed robustness, scale content-addressable memory, cross-domain
transfer, open-ended skill acquisition), each scored pass / honest-negative. The workspace now
broadcasts a **single** dominant pattern, so the **compositional / multi-item** rung (holding and
binding **several** broadcast items at once within theta-gamma capacity `≈7` — the system-scale
form of L4's binding question) is the natural first probe. Firewall (final): even if every
criterion passes, that is **functional** GI — the hard-problem blank stays open.
`check_completeness.py` updated to re-run and pin this module (now **nine** reproduced digests).
Concept DOI `10.5281/zenodo.20783570` reflected via `CITATION.cff` and the doc provenance lines.

---

## S10 — v0.10 — L9 functional general intelligence (THE END CONDITION; the integrated L0–L8 machine on the capability ladder)

**Frame.** The inherited chain's final layer. With L0–L8 each MET & GRADED or recorded as an honest
`[O]`, the **sufficiency hypothesis** — *the wave-substrate properties proven at L0 SUFFICE for
at-least-human-level FUNCTION* — is settled the only honest way: the **integrated** machine is
assessed against a falsifiable **capability ladder** (BLUEPRINT §11, seven rungs), each rung
carrying a stress test, each scored pass `[V]` / honest shortfall `[O]`, the grade **DERIVED** from
the sweep booleans. Built additively on the frozen L0 substrate and reusing, exactly and
non-circularly, L1 (the slot/role phase-keys) and L3 (the von Mises gate); nothing below is edited;
every read-out is non-circular; `new_tuned_constants = 0`.

**Result — 6/7 rungs `[V]`.**
- **A1 compositional / multi-item** `[V]` (the flagged first probe): K concepts co-hosted in distinct
  θ–γ slots (L1 `permute` keys), each routable from the composite broadcast **alone**; per-slot
  recovery ≥0.9 up to an **emergent** capacity K\* = 6 (N=128) / 10 (N=256), scaling with precision
  toward the inherited θ–γ ~7 (the number is the *comparison*, not an input); no-tag control recovers
  only one item. The L8 single-pattern limit is lifted.
- **A2 one-shot generalization** `[V]`: novel-instance accuracy ≈1.0 ≫ chance from one example.
- **A3 real-time adaptation** **`[O]` — the lone honest shortfall**: from a clean ~1.0 baseline a rule
  switch causes a real dip, and online additive re-imprinting recovers only partially (post 0.78/0.58
  < 0.8 band). A single Hebbian store can only **accumulate, never over-write** — old and new
  associations superpose and interfere. **Named, already-proven mitigation:** the L5 **dual store**
  (A7), retention ~1.0.
- **A4 noise-immersed robustness** `[V]`: the L0 attractor clean-up **lifts representational fidelity**
  (overlap to the true prototype) over a no-clean-up read by a sign-stable margin (+0.20…+0.56),
  degrading gracefully toward the ~0.5 information wall, using the **inherited** `corrupt_phase`
  noise model; matched-filter accuracy is over-determined and reported as such.
- **A5 scale content-addressable memory** `[V]`: hierarchical (L3-gated) recall holds at 1.0 as the
  store grows to T=64 while a flat store collapses past T=16, at O(1)-in-T cost.
- **A6 cross-domain transfer** `[V]`: relational structure transfers to never-trained fillers
  (filler-independent L1 phase-key binding) up to a crosstalk ceiling J\*=3.
- **A7 open-ended skill acquisition** `[V]`: the L5 dual store keeps acquiring (latest-skill 1.0) while
  retaining old skills at ~1.0, far above a single store; truly unbounded retention is `[O]` and
  recorded as such.

**Two methodological corrections (documented transparently).** (1) **A4 lattice-freeze → inherited
noise model.** The first A4 draft corrupted cues with pure bit-flips encoded via `pattern_to_phase`,
landing every phase exactly on the {0,π} lattice where the Kuramoto coupling `sin(θⱼ−θᵢ)` is
identically zero — so `relax` sat frozen and the clean-up did nothing (fidelity margin exactly
+0.0000; verified: on-lattice raw 0.359 ≡ relaxed 0.359). The test was insensitive to D4 by
construction. Fixed by using the **inherited** `corrupt_phase` (flip + continuous jitter — the exact
perturbation L0 used to prove D4); the jitter keeps the cue off-lattice so descent flows to the
attractor, giving the genuine fidelity lift. No constant tuned — only the noise model corrected to
the inherited one. (2) **A3 clean baseline** (validity/clarity; **outcome unchanged**): the uneven
repeated stream (artificial pre≈0.44) was replaced by one clean imprint per category (pre≈1.0); the
post-shift shortfall persists (0.78/0.58 < band), confirming `[O]` is a real single-store limit, not
an artifact. Two engineering notes (no scientific effect): the A1 K×N sweep was trimmed to N∈{128,256},
trials=3 for a single-core time budget (sweep breadth only, no inherited constant); and `main()` was
made checkpoint-aware (per-rung cache, deterministic, digest unchanged whether one pass or resumed).

**Verdict.** The capability ladder is **settled: 6/7 rungs `[V]`** on the integrated L0–L8 wave
machine; the lone `[O]` (A3) is a stated single-store bound with a proven dual-store mitigation, and
the standing caveats on passing rungs (A1 finite capacity, A6 ceiling J\*=3, A7 unbounded retention)
are inherited laws. The sufficiency hypothesis is **settled** — the L0 properties reach general
FUNCTION across the ladder within stated bounds. **This closes the blueprint.** Closing is **not** a
claim of human intelligence; closing = the hypothesis resolved layer by layer. Discipline upheld:
sweeps sign-stable, read-outs non-circular (slot recovered from the broadcast alone; fidelity to a
prototype never imprinted as the readout target; transfer to never-trained fillers), regimes swept
not tuned, brain anchor R=0.39 and θ–γ ~7 **not transferred** (capacity **emerges**),
`new_tuned_constants=0`, firewall held (`consciousness_claim=0`, `hard_problem_open=1`), digest
`20b5f2c2c9b11a3c…` reproduces bit-for-bit from a clean state.

**Layer status.** L9 — **MET & GRADED ★ — END CONDITION REACHED.** The blueprint **closes**. Any
further session is **post-program**: compression (axiom-independence audit) or hardening
(convergent-evidence grading / wider sweeps) — no new layer, no tuning. `check_completeness.py`
updated to re-run and pin this module (now **ten** reproduced digests). **FIREWALL (final):** passing
the ladder is **functional** general intelligence; the hard-problem blank (Gap-5) stays open, never
erased.

## S11 — v0.11 — POST-PROGRAM HARDENING: the A3 [O]→[V] closure, INLINE (additive; substrate + all priors unchanged)

**Post-program, not a new layer.** The blueprint CLOSED at S10. This is the disciplined continuation **(b) hardening**, named identically in HANDOFF §3 / START_HERE §4 / BLUEPRINT §11–§12: re-probe the A3 single-store `[O]` with the dual store wired in, to show the `[O]→[V]` closure **on the adaptation probe itself**. It adds one paired battery; it opens nothing new and edits nothing prior.

**The gap it removes.** S10 left A3 as the lone `[O]` (a single additive Hebbian store cannot over-write a switched rule) and named the L5 dual store as the fix — but demonstrated that fix *by reference* (at A7 open-ended acquisition), not on the adaptation task A3 failed. S11 runs the fix **inline** on that exact task, isolating the one variable that changes.

**Mechanism (clean paired contrast).** Identical cues / responses / shift. **Single store** = one additive field `hebbian_field([cue|resp])` accumulated over the stream — a re-mapped cue adds cue→resp2 to the *same* field holding cue→resp, the two superpose with equal weight, the settle lands on a blend (a lone additive field accumulates, never over-writes). **Dual store** = slow additive history (= the A7 persistent store) **+** a fast one-shot episodic field over the *current-rule snapshot* — the inherited **R3 / C2** `_episodic_field`, **reused unchanged** — read out by settling under both fields combined by **equal vote** (each L2-normalized, then summed; scale-free, no scalar fit). The single store is **exactly the dual store's SLOW component alone**, so the *only* difference is the added fast store.

**Found (trials=6; sweeps sign-stable; grades DERIVED).** Pre-shift baseline 1.000 at every shift; the dip deepens with the remap fraction (0.833 → 0.222). **T1 closure:** single post-recovery 0.917 / 0.778 / 0.806 / **0.583** across remap fraction {0.25,0.5,0.75,1.0} — fails the full switch (reproduces the inherited 0.78/0.58 to the digit) — while the **dual store recovers to 1.000 at every shift fraction** → `A3_closure_O_to_V=True`. **Normalization is not the trick:** the **raw, unnormalized** dual sum *also* beats single everywhere (0.889–1.000) → equal-vote is scale-equalizing only; the fast store is the mechanism. **T2 size-robustness:** the same sign at (6,128), (8,128), (6,256) — single fails the full switch (0.58/0.54/0.56), dual closes everywhere → `closure_sign_stable_across_size=True`. **Honest note:** old-rule retention for *over-written* cues is correctly low under both stores (≈0.5–0.75) — that is the definition of adaptation (a cue cannot map to two responses), not a defect; retention of *non-conflicting* skills is the separate A7 property, already `[V]`, and is **not** re-graded here.

**Verdict.** **A3 `[O]→[V]` is CLOSED, inline.** With the proven L5 dual store wired in the capability ladder reads **7/7 `[V]`**; the **S10 6/7 single-store `[O]` record STANDS** as the minimal machine's honest limit (paired, not overwritten — the negative is kept alongside the positive, the program's own `[V]`/`[O]` discipline applied to its last open rung). Discipline upheld: read-out non-circular (recovery on the *new* rule, response half masked), sweeps sign-stable, regimes swept not tuned, the fast store byte-faithful to R3/C2, brain anchor R=0.39 **not transferred**, `new_tuned_constants=0`, firewall held (`consciousness_claim=0`, `hard_problem_open=1`), digest `ad93057afac2054e…` reproduces bit-for-bit from SEED.

**Layer status.** No new layer — L9 remains the END CONDITION. `check_completeness.py` updated to re-run and pin this module (now **eleven** reproduced digests). **FIREWALL (unchanged):** closing an *adaptation* rung is a **functional** result; the hard-problem blank (Gap-5) stays open, never erased.

---

## S12 — v0.12 — POST-PROGRAM COMPRESSION: the axiom-independence audit (additive; substrate + all priors unchanged)

**Post-program, not a new layer.** The blueprint CLOSED at S10; S11 closed the last open rung A3 `[O]→[V]` inline. This is the **other** disciplined continuation **(a) compression**, named identically in HANDOFF §3 / START_HERE §4 / BLUEPRINT §11–§12: an **axiom-independence audit of the inherited invariants**. It adds an audit; it builds no new layer, opens nothing new, and edits nothing prior. With it, **both** post-program continuations the program named for itself — (a) compression and (b) hardening — are executed.

**The question it answers.** The program *inherited* eight invariants (brain B1–B5, physics P1–P3) and treated them as load-bearing throughout. "We assumed eight things and the machine worked" is weaker than "we know which of those eight the machine actually stands on." Compression asks the dual of the construction question: not *do these suffice to build it* (S1–S10: yes), but **is the inherited set minimal, and is each surviving piece truly required** — or is some of it ballast a leaner machine could drop?

**C0 — the structural compression (8 → 5).** The eight inherited invariants map onto the operational primitives the frozen L0 actually exposes; several collapse onto the *same* mechanism, so the inherited set is **not minimal**: **AX1** data-encoded coupling field (B1 ephaptic + B4 attractor storage rule), **AX2** field symmetry/reciprocity J=Jᵀ (B4 Lyapunov structure + P3 1/r² near-field reciprocity), **AX3** coupling nonlinearity sin Δθ (B2 phase coupling), **AX4** settling/clock-free relaxation (P2 clock-free propagation + B2 self-timed dynamics), **AX5** metastable operating band (B3 critical band + P1 stiffness=gain). **B5 theta-gamma capacity is deliberately NOT an L0 axiom** — it is a higher-layer (L2/L3) realization (theta-gamma multiplexing), recorded as **deferred**, neither ablated nor claimed as part of the minimal substrate core. So the honest compression statement: **eight inherited invariants → five independent operational axioms in the frozen substrate, with B5 deferred to a higher layer.**

**Method (one non-circular probe, generic thresholds, no tuning).** Every axiom is judged by **one universal, non-circular probe**: store random ±1 patterns in the coupling field, present a **corrupted** cue (15% sign-flips + 0.30 phase jitter), settle, measure **capacity** = fraction recovered past the inherited recall band (overlap ≥ 0.95). The thing perturbed (which axiom is intact) is never the thing read (recovery of an independently-drawn stored pattern). Two trust properties: **paired & sign-stable** — each axiom run as intact-vs-knockout on identical patterns/cues/seed, repeated across **6 seeds**, a collapse counting only if it holds the same sign at every seed; and **a positive control gates the harness** — the fully intact substrate runs the *same* harness first (capacity 0.967, overlap 0.997, R 0.062 metastable), so any collapse below is attributable to the knock-out, not the harness. Only **generic separability thresholds** (recall band 0.95, halfway margin 0.5); **no number fit to a target**; `new_tuned_constants=0`. The L0 substrate is **never edited** — the knock-outs are deliberately broken *substitutes* (a random symmetric field, an asymmetric field, a linear flow, a zero-step settle, a ferromagnetic drive) built *beside* the genuine imported primitives.

**Found (paired ablations; every collapse sign-stable across 6 seeds; grades DERIVED).**
- **C1 — AX1 data-encoded field — load-bearing [V].** Magnitude-matched **random symmetric** field (data not encoded): capacity **0.90 → 0.00** at every seed; the stored patterns are **non-attractors**, a clean recall never happens. (Residual overlap ~0.52 sits between cue level and chance because a non-encoding field is **inert** — it neither recalls nor scrambles; capacity, the decision metric, is what goes to zero.)
- **C2 — AX2 symmetry — load-bearing [V], graded.** **Antisymmetric break** κ·‖J‖, κ swept: capacity 0.867 / 0.700 / 0.500 / 0.100 / **0.000** at κ = 0/0.5/1/2/4. A **strong** break collapses recall (the Lyapunov/energy structure that guarantees convergence to the stored fixed point is gone); small breaks are **tolerated** (reported tolerance κ ≈ 1.0). Honest graded result, not a cliff.
- **C3 — AX3 nonlinearity — load-bearing [V].** First-order **linear** (small-angle) signed-Laplacian consensus flow, same J, same budget: capacity **0.90 → 0.00**. The linearization removes the discrete phase **wells at {0, π}** that hold distinct patterns. Diagnostic: settled global R stays **low** ~0.08 — the linear signed-Laplacian flow *scrambles*, it does **not** lock onto the stored pattern. (An earlier draft's "syncs coherently to the wrong answer / R high" was **corrected** to this — a recorded honesty fix.)
- **C4 — AX4 settling — load-bearing [V].** Field present but **never iterated** (steps=0): capacity **1.00 → 0.00**, the read-out equals the **corrupted cue** (overlap 0.703, `field_inert_without_relaxation=True`). Computation **is** the settling, not the storage — which also proves AX4 independent of AX1 (you need both the field *and* the dynamics).
- **C5 — AX5 metastable band — load-bearing [V].** **Uniform ferromagnetic drive** d forcing global synchrony, d swept: capacity 0.967 / 0.167 / 0.000 … while R 0.102 / 0.885 / **1.000** … at d = 0/0.5/1+. Forced toward full coherence the global mode **swamps** the stored structure — one global state carries **zero** stored information; maximal coherence is **not** optimal. (The inherited D3 regime scan pins the *lower*, field-off edge; this pins the *upper*, over-driven edge.)
- **C6 — verdict: IRREDUCIBLE [V].** `load_bearing` True for all five; `redundant_axioms=[]`; `axiom_set_irreducible=True`. Every operational axiom is load-bearing — each knock-out collapses a core capability the other (intact) axioms do **not** rescue, sign-stable across seeds, while the intact control passes. **No further compression:** the eight inherited invariants compress to a **minimal five-axiom operational core** (B5 deferred), no axiom in it redundant.

**Two honesty fixes (recorded, not hidden; both changed the digest, both re-pinned).** (1) **C3 reading corrected** — linear flow gives **low** R (~0.08) and *scrambles*; the earlier "synchronises to the wrong pattern / R high" overclaim was removed. (2) **C1 reading tightened** — capacity (decision metric, → 0 every seed) is distinguished from the residual ~0.52 overlap (a non-encoding field is inert), so the residual is not misread as partial success. Exactly the self-corrections the Stress Principle requires.

**Verdict.** **The inherited premises are not ballast.** The eight inherited invariants compress to **five** independent operational axioms (B5 theta-gamma deferred as a higher-layer realization), and an ablation audit — one non-circular probe, generic thresholds, paired and sign-stable across six seeds, gated by a passing intact control — finds **all five load-bearing**. `redundant_axioms=[]`, `axiom_set_irreducible=True`: the five-axiom core is **minimal**, no further compression. Discipline upheld: L0 **never edited**, read-out non-circular, sweeps sign-stable, thresholds generic not tuned, brain anchors **not transferred**, `new_tuned_constants=0`, firewall held (`consciousness_claim=0`, `hard_problem_open=1`), digest `7f59ced681bdf8b83396b1b4c8d37f639460f66dacbce34291633f91e4fc45a0` reproduces bit-for-bit from SEED.

**Layer status.** No new layer — L9 remains the END CONDITION; both named post-program continuations (a)+(b) now executed. `check_completeness.py` updated to re-run and pin this module (now **twelve** reproduced digests). **FIREWALL (unchanged):** auditing which *functional* axioms a *functional* machine stands on is a **functional** result; the hard-problem blank (Gap-5) stays open, never erased.
