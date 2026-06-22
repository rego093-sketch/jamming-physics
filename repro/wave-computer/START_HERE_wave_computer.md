# START HERE — vp_wave_computer
## A wave-substrate computer inherited from the brain (ephaptic) and physics (jamming) — long-term program

> **New session?** Read **`HANDOFF.md` first** — it is the binding cold-start guide
> (self-containment, forced learning, autonomous protocol, regression rules).
> This file is the master living doc: current status, cumulative session ledger,
> and pointers. Output is **always one zip, additive, nothing dropped** — carrying
> cumulative history + this session's results + the updated blueprint.

> **Provenance.** Author **Young Jae Lee** (ORCID `0009-0002-7535-8245`),
> program **jamming-physics.org**, license **CC BY 4.0**.
> **Concept DOI `10.5281/zenodo.20783570`** (all versions) — see `CITATION.cff`.

---

## 0. Status at a glance

| Item | Status |
|---|---|
| **Substrate L0** | ✔ PROVEN (v0.1: store · compute · pattern · communicate / v0.2: sum=info · resonance-match · one-shot · parallelism) |
| **Representation L1** | ✔ COMPLETE (binding · bundle · **permute** proven; role-value **tree depth-capacity** measured, d\*≈2–4) |
| **Time L2** | ◑ MILESTONES MET (metastable **trajectory** replay/predict · **theta-gamma WM** capacity law) |
| **Hierarchy L3** | ✔ MET & GRADED (nested gating **selects levels** · abstraction from **novel** instances · **zero**-gap composition · nesting **~6×** capacity under strict clean-up) |
| **Inference L4** | ✔ MET & GRADED ★ (**gate DERIVED** from a raw cue, no oracle · constraint-satisfaction **= settling** · analogy **= resonance** · probabilistic **= noisy settling**; one honest limit: strict capacity ⊥ derivability) |
| **Dual learning L5** | ✔ MET & GRADED (consolidation builds a **generalising slow store** · dual **reduces catastrophic forgetting** vs single-store · **L4 [O]→[V] closed**: an independent **context channel** restores strict capacity to ~oracle; one honest limit: no textbook double dissociation) |
| **World model L6** | ✔ MET & GRADED (self-supervised **prediction = forward settling** · error = **difference wave** drives learning · **generative rollout** to a finite horizon · **novelty** flagged by the error wave · **forward model > reactive recall**, advantage is **directionality/structure** — the C4 break honoured; one honest limit: error-gating halts at **prediction-sufficiency**, operator directionally L2 but not magnitude-identical) |
| **Embodiment L7** | ✔ MET & GRADED ★ (closed clock-free real-time loop: **control = continuous settling** · forward model **holds a moving target through sensorimotor delay** where reactive **lags** and open-loop **drifts** · **analog I/O beats ADC/DAC** under graded noise (D4 at the I/O boundary; tax closes at higher b) and the **dimensional advantage scales** (aggregate N×gap grows) · **prediction-sufficiency suffices** → the inherited **S7 [O] is resolved [V]** · stable **bandwidth/latency** band recorded; honest two-sides caveat: single-channel **Shannon-capped** + exact-arithmetic **digital hand-off** [O]×2, and the parallelism/latency form the **R4-inherited principle** [O]) |
| **Global access L8** | ✔ MET & GRADED (a global metastable **resonant hub** **selectively binds + broadcasts** the dominant pattern across L1–L7 (lock margin ≥0.92, non-source recall 1.0 vs chance) · **flexible routing** (1.0 vs fixed-gate ≈1/M) · a **functional PCI-analog** = integration × differentiation **peaks at the metastable edge** — Gap-4 inverted-U, the **number R=0.39 NOT transferred**, the band **emerges** · inherited operating-band made concrete: routing holds within the hub's **lock-latency band** (edge ≈20 steps) [V]; **unbounded-rate** + **no-release over-write** routing **[O]**) |
| **L9 (end)** | ✔ **MET & GRADED — END CONDITION REACHED ★** functional general intelligence: the integrated L0–L8 machine on the **capability ladder** = **6/7 rungs [V]** · A1 **compositional/multi-item** (capacity K\* **emerges** =6/10 by N, scales toward θ–γ ~7, no-tag control recovers single) [V] · A2 **one-shot** (novel-instance acc ≈1.0 ≫ chance) [V] · A3 **real-time adaptation** **[O]** the lone honest shortfall (a single additive store cannot **over-write** a switched rule; recovery 0.78/0.58 < band) — mitigation = the **proven L5 dual store** (A7) · A4 **noise-immersed robustness** (D4 clean-up **lifts fidelity** to the true prototype by a sign-stable margin, off-lattice `corrupt_phase`; accuracy over-determined, stated) [V] · A5 **scale CAM** (hierarchy holds recall 1.0 past flat ceiling T=16 at O(1)-in-T) [V] · A6 **cross-domain transfer** (filler-independent, to a crosstalk ceiling J\*=3) [V] · A7 **open-ended acquisition** (dual store retains ~1.0 vs single decaying) [V]. **The blueprint CLOSES** (hypothesis settled layer by layer). Firewall: passing = **functional** GI, the hard problem stays an open blank |
| **L9+ (hardening)** | ✔ **A3 [O]→[V] CLOSED, INLINE** *(post-program continuation (b))* — re-probed the lone A3 shortfall with the **proven L5 dual store** wired in, on the **adaptation task itself**: a strict paired contrast where the single store is **exactly the dual's SLOW component alone**, so the only change is the added **fast** one-shot episodic field (the inherited **R3/C2** `_episodic_field`, reused unchanged). Single fails the full switch (post-recovery 0.583 < band, reproducing the inherited 0.78/0.58); **dual recovers to 1.000 at every shift fraction** → `A3_closure_O_to_V=True`. The **raw, unnormalized** dual sum *also* beats single everywhere → equal-vote is scale-equalizing only, the fast store is the mechanism. **Sign-stable** across (B,N) ∈ {(6,128),(8,128),(6,256)}. Ladder now **7/7 [V]** *with the dual store wired in*; the **S10 6/7 single-store [O] record STANDS** as the minimal machine's honest limit (paired, not overwritten). `new_tuned_constants=0`, firewall held, digest `ad93057afac2054e…` |
| **L9++ (compression)** | ✔ **AXIOM SET IRREDUCIBLE — 8→5, 5/5 LOAD-BEARING [V]** *(post-program continuation (a))* — an **axiom-independence audit** of the inherited invariants. The **eight** inherited invariants (brain B1–B5, physics P1–P3) compress structurally onto **five** operational L0 axioms — **AX1** data-encoded field (B1+B4), **AX2** symmetry/reciprocity (B4+P3), **AX3** nonlinearity (B2), **AX4** settling/clock-free (P2+B2), **AX5** metastable band (B3+P1) — with **B5 theta-gamma capacity deferred** as a higher-layer (L2/L3) realization, *not* an L0 axiom. Then each axiom is **nulled while the others stay intact**, judged by one **non-circular** probe (recover an independently-drawn stored pattern from a corrupted cue), **paired & sign-stable across 6 seeds**, gated by a **passing intact control** (cap 0.967). **Every one collapses → all five load-bearing:** AX1 cap 0.90→0.00 · AX2 graded (0.867→0.000 as κ→4, tolerance κ≈1.0) · AX3 cap 0.90→0.00 (linear flow *scrambles*, R stays low ~0.08) · AX4 cap 1.00→0.00 (no-settle = corrupted cue; field inert) · AX5 cap 0.967→0.00 as R→1.000 (over-coherence carries zero stored info). `redundant_axioms=[]`, `axiom_set_irreducible=True` — the five-axiom core is **minimal**, no further compression. L0 substrate **never edited** (knock-outs are broken substitutes built beside it). `new_tuned_constants=0`, firewall held, digest `7f59ced681bd…` |
| **Discipline** | no tuning; every claim with a sweep; honest negatives recorded; physical realization deferred |

**Latest reproduction anchors:** v0.1 `e9fdd3bc…` · v0.2 `c69917020c66…` · v0.3 `69890fec8b54…` · v0.4 `ea4c6723…` · v0.5 `2d3057bb…` · v0.6 `e8a623005831…` · v0.7 `41e81a7f2eb9…` · v0.8 `17aa27bf34b7…` · v0.9 `52a0ce34b54f…` · v0.10 `20b5f2c2c9b1…` (L9 END CONDITION, 6/7 [V]) · v0.11 `ad93057afac2…` (post-program hardening — A3 [O]→[V] closed inline, ladder 7/7 [V] with the dual store wired in) · v0.12 `7f59ced681bd…` (post-program compression — axiom-independence audit, 8→5 axioms, 5/5 load-bearing, irreducible [V])
(all deterministic, bit-for-bit). Verify with `python3 repro/check_completeness.py`.

---

## 1. What is being built (one line)

**Reproduce, on the same wave substrate, the properties by which the brain reaches
general intelligence — phase coding, resonance matching, one-shot learning,
metastability, noise immunity, sum=information — and test whether they suffice for
at-least-human-level functional intelligence.** Not a static bit (0/1) but a wave
(phase θ) carries information; not arithmetic but physics settling does the matching;
the input becomes a pattern at once; learning is one-shot. **Function only** — the
hard problem is an explicit blank.

Inherited from `vp_frontal v2` (B1–B5) + `vp_physics v0.11.0` (P1–P3), fully captured
in `INHERITANCE_MANIFEST.md` (self-contained).

---

## 2. Cumulative session ledger (work history)

| Session | Version | Did | Key result | Record |
|---|---|---|---|---|
| S1 | v0.1 | Define & prove substrate L0 (4 operations) | store α_c≈0.06 · compute corruption~20% · metastable · **comms BER~0.03% at negative SNR** | `SESSION_v0_1_design_study.md` |
| S2 | v0.2 | Prove L1's four core properties | **sum=info K≈96** · **O(1)-in-P match** · **one-shot 1.0** · parallelism [O] | `SESSION_v0_2_resonance_and_learning.md` |
| S3 | v0.3 | L1 completion (permute · tree depth) + L2 start (trajectory · WM) | **algebra closed** (permute L*≈32) · tree d\*≈2–4 · **replay 1.0** @λ≈2.5 · **WM capacity law** (Miller 4–9) | `SESSION_v0_3_structure_and_time.md` |
| S4 | v0.4 | L3 hierarchy / abstraction | **gate selects levels** (margin +0.92) · category from **novel** inst (≤32) · **zero**-gap composition (576, depth-3) · hierarchy **~6×** ceiling (strict) | `SESSION_v0_4_hierarchy_and_abstraction.md` |
| S5 | v0.5 | L4 resonance / inference ★ pivot | **gate DERIVED** from raw cue (loop closes, derived==oracle, cost~0) · CSP **= settling** (1.0 ≫ random, tracks 1/(1+f)) · analogy **= resonance** (fill J\*≥12, analogy J\*=4) · probabilistic **= noisy settling** (3 Bayes laws) · honest [O]: strict capacity ⊥ derivability | `SESSION_v0_5_inference_and_resonance.md` |
| S6 | v0.6 | L5 dual learning systems | consolidation builds a **generalising slow store** (novel-probe overlap > 1-2ρ; honest: does not beat fast) · **dual ≪ single forgetting** at every load (paired) · **L4 [O]→[V]**: independent **context channel** strict ≈ oracle ≫ content/flat, robust to ctx-corruption 0.3 · honest [O]: no CLS **double** dissociation (fast generalises for free) | `SESSION_v0_6_dual_learning_systems.md` |
| S7 | v0.7 | L6 self-supervised world model | prediction = **forward settling**, learning = **difference wave**: held-out error `0.978→0.126` monotone (all m, all η) · **rollout** faithful to horizon 12, drift at 13 · **surprise** graded, novelty margin 0.97 · **forward ≫ reactive** everywhere (a symmetric store that saw every transition only returns the present — advantage is **directionality**, C4 honoured) · honest [O]: error-gating halts at **prediction-sufficiency** (operator directionally L2, cosine ≈0.81, not magnitude-identical) | `SESSION_v0_7_self_supervised_world_model.md` |
| S8 | v0.8 | L7 embodiment / real-time control | **control = continuous settling** in a closed clock-free **analog** loop: forward **holds a moving target through delay** (E1 [V]) · **analog I/O beats ADC/DAC** + dimensional advantage **scales** (E2 [V]; E2c parallelism R4 [O]) · **prediction-sufficiency suffices → S7 [O] resolved [V]** (E3) · stable **bandwidth/latency** band (E4 [V]) · honest two-sides caveat: Shannon cap + hybrid hand-off (E5 [O]×2) | `SESSION_v0_8_embodiment_and_control.md` |
| S9 | v0.9 | L8 global integration / functional access | a global metastable **resonant hub** **selectively binds + broadcasts** the dominant pattern (lock margin **≥0.92**, non-source recall **1.0** vs no-hub chance) (G1 [V]) · **flexible routing** (1.0 vs fixed-gate ≈1/M) (G2 [V]) · a **functional PCI-analog** = integration × differentiation is an **inverted-U**, interior peak (g=0.5/0.25), `0` both isolated (I=0) and over-driven (D→0) — Gap-4, **R=0.39 not transferred** (G3 [V]) · inherited operating-band concrete: routing holds within the hub's **lock-latency band** (edge ≈20) (G4 band [V]); honest **[O]**: unbounded-rate + no-release over-write routing | `SESSION_v0_9_global_integration_and_access.md` |
| S10 | v0.10 | **L9 functional general intelligence — THE END CONDITION** | the integrated L0–L8 machine on the **capability ladder** = **6/7 rungs [V]**: A1 compositional/multi-item (capacity K\* **emerges** 6/10 by N, toward θ–γ~7; no-tag control recovers single) [V] · A2 one-shot (≈1.0 ≫ chance) [V] · **A3 real-time adaptation [O]** the lone shortfall (single additive store cannot **over-write**; recovery 0.78/0.58 < band) — mitigation = **proven L5 dual store** (A7) · A4 noise-immersed robustness (D4 **lifts fidelity** off-lattice `corrupt_phase`; accuracy over-determined, stated) [V] · A5 scale CAM (hierarchy holds 1.0 past flat ceiling T=16, O(1)-in-T) [V] · A6 cross-domain transfer (filler-independent, ceiling J\*=3) [V] · A7 open-ended acquisition (dual ~1.0 vs single decaying) [V]. **Blueprint CLOSES.** Two methodological corrections documented (A4 lattice-freeze→inherited noise model; A3 clean baseline, outcome unchanged). Firewall unchanged | `SESSION_v0_10_functional_general_intelligence.md` |

| S11 | v0.11 | **POST-PROGRAM HARDENING — the A3 [O]→[V] closure, INLINE** | re-probed the lone A3 shortfall with the **proven L5 dual store** wired in, on the **adaptation task itself** (continuation (b)). Strict paired contrast: single store = **exactly the dual's SLOW component alone**, only change = the added **fast** one-shot episodic field (inherited **R3/C2** `_episodic_field`, reused unchanged), read by **equal vote**. **T1:** single fails the full switch (post-recovery 0.583 < band; reproduces the inherited 0.78/0.58 to the digit), **dual recovers to 1.000 at every shift fraction** → `A3_closure_O_to_V=True`; the **raw unnormalized** dual sum *also* beats single everywhere → normalization is scale-equalizing only, the fast store is the mechanism. **T2:** sign-stable across (6,128),(8,128),(6,256). Old-rule retention for over-written cues correctly low under both (= adaptation, not a defect; A7 not re-graded). Ladder **7/7 [V]** with the dual store wired in; **S10 6/7 single-store [O] record STANDS** (paired, not overwritten). `new_tuned_constants=0`, firewall held | `SESSION_v0_11_adaptation_closure.md` |
| S12 | v0.12 | **POST-PROGRAM COMPRESSION — the axiom-independence audit** | an audit of the inherited invariants (continuation (a)). **C0 (structural):** the **8** inherited invariants compress onto **5** operational L0 axioms — AX1 data-encoded field (B1+B4), AX2 symmetry (B4+P3), AX3 nonlinearity (B2), AX4 settling (P2+B2), AX5 band (B3+P1) — **B5 theta-gamma deferred** as a higher-layer realization, not an L0 axiom. **C1–C5 (empirical):** null each axiom with the others intact; one **non-circular** probe (recover an independently-drawn pattern from a corrupted cue), **paired & sign-stable across 6 seeds**, gated by a **passing intact control** (cap 0.967). **All five collapse → all load-bearing:** AX1 0.90→0.00 · AX2 graded 0.867→0.000 (κ→4, tolerance κ≈1.0) · AX3 0.90→0.00 (linear flow *scrambles*, R low ~0.08 — earlier "syncs wrong/R high" overclaim corrected) · AX4 1.00→0.00 (no-settle = cue level, field inert) · AX5 0.967→0.00 as R→1.000 (over-coherence = zero stored info). **C6:** `redundant_axioms=[]`, `axiom_set_irreducible=True` — minimal core, no further compression. L0 **never edited**. Both named post-program continuations (a)+(b) now executed. `new_tuned_constants=0`, firewall held | `SESSION_v0_12_axiom_independence_audit.md` |

Full detail → `CUMULATIVE_LOG.md`.

---

## 3. Key findings so far (what is proven)

1. **Phase beats bits under noise** — phase coding + attractor clean-up holds
   **BER ≈ 0.03% at negative SNR (−2.3 dB, 22% raw bit errors)** (D4). End-to-end
   proof of "communication works even with heavy noise."
2. **The sum is the information** — one composite wave holds K≈96 items, read by
   resonance (R1).
3. **Matching without computation** — settling steps are independent of the number
   stored P, O(1)-in-P (R2); in parallel hardware P=10⁵ costs the same physical time
   as P=1 (R4 [O]).
4. **One-shot learning** — one exposure → immediate recall, no catastrophic
   forgetting (R3).
5. **Compute lives below full coherence** — the metastable band (low R) is the
   condition for many coexisting patterns (D3); shares the **principle** of the brain
   at R=0.39 (the number is not transferred).
6. **The representation algebra is closed** — `bind · bundle · permute` form a complete
   VSA on the wave substrate; a sequence of useful length L\*≈32 is read back by position
   (L1a). Role-value **trees** work but are **shallow** (useful depth d\*≈2–4) — measured
   evidence that deep structure needs hierarchy (L3), not flatter binding (L1b).
7. **Sequences are metastable trajectories** — an asymmetric time-delayed Hebbian term
   makes the field walk a learned loop: predict-next is verified, and full-cycle **replay
   reaches 1.0 at λ≈2.5** (L2a). **Working-memory capacity = min(slots, precision)** —
   a real capacity *law* that lands in the Miller range (4–9) under realistic gamma
   jitter; the brain's ~7 is the **slot count**, not a tuned constant (L2b).
8. **Hierarchy breaks the flat ceiling** — a slow phase **gates** which fast sub-field
   is active (nested phase coupling, theta-gamma generalized to ≥2 levels). The gate
   **selects the level** (correct vs wrong margin +0.92), an abstract **category** is
   recognized from **novel** instances (up to 32 categories), composition has **zero**
   train/test gap (576 combos, depth-3), and storing instances in gated sub-fields
   **multiplies effective capacity ~6×** (strict clean-up: flat dies at T≈12, hierarchy
   holds to T=72) — the measured remedy for L1's shallow depth (L3). *Honest:* the
   capacity win is criterion-dependent (vanishes under a forgiving read-out) and assumes
   the correct gate, which L4 must **derive**.
9. **Inference is settling — the gate derives itself** ★ — the slow context is **read
   from a raw, unlabeled cue** by resonance in an upper field and **then** routes the
   fast field (S4's "assume the gate" caveat removed): the loop **closes** where the
   geometry is separable (gate derived ~1.0, derivation cost ~0, derived == oracle ≫
   flat). On the substrate, **constraint satisfaction *is* settling** (a native q=2
   anti-ferromagnet solves a planted graph at 1.0 ≫ random 0.5 and tracks the
   frustration optimum 1/(1+f) — no clock, no constant), **analogy *is* resonance**
   (fill-a-missing-factor robust to J=12; proportional analogy to J\*=4, an honest
   crosstalk ceiling), and **probabilistic inference *is* noisy settling** (prior,
   evidence, and temperature each move occupancy in the Bayes direction). *Honest
   negative:* the strict ~6× capacity advantage does **not** survive a *derived* gate —
   gate-derivability needs shared structure that correlates instances, and that
   **trades off directly** against strict instance-separability (no operating point has
   both); the id-level advantage **does** survive, and the strict version needs an
   **independently-supplied context channel** (→ L5). "Inference without computation"
   holds on the cognitive forms; no hybrid is forced (L4).

10. **Two stores separate by persistence, not abstraction** ★ — offline **replay**
   consolidates one-shot episodes into a **separate, persistent** slow store that
   generalises to **novel** instances (overlap > the single-instance baseline `1-2ρ`), and
   that store **greatly reduces catastrophic forgetting** vs a single leaky store (dual ≪
   single at every load, paired comparison). Supplied as an **independent context channel**,
   it **closes L4's one open limit**: strict instance recovery returns to ~oracle where a
   content-derived gate degrades (context strict ≈ 1.0 ≫ content ≈ 0.68 ≫ flat 0 at heavy
   load, robust to context-cue corruption ≤ 0.3). *Honest negative:* the textbook
   complementary-systems **double** dissociation does **not** hold — the **fast** Hebbian
   store already generalises for free (superposition → emergent prototype), so the slow
   store never out-generalises it; the two systems are functionally distinct by
   **persistence/capacity**, not by an abstraction the fast store lacks (L5).

11. **The substrate predicts — a self-supervised world model** ★ — with **prediction =
   forward settling** (the learned asymmetric transition field acts on the present, the L0
   attractor field cleans up the next) and **learning = the difference wave** (an
   error-gated delta rule), the substrate learns an **unlabeled** structured stream from
   its own error: held-out next-step error falls `0.978 → 0.126`, monotone across stream
   length and rate (sign-stable). The same error wave **rolls out** plausible continuations
   to a finite horizon (faithful to 12 steps, honest drift after) and serves **unmodified**
   as a **graded novelty detector** (familiar ≈ 0, full violation ≈ 0.97). The headline:
   a **forward model anticipates** where a **reactive** store that has seen **every**
   transition only returns the **present** — the advantage is **directionality (structure)**,
   honouring L5's C4 break (the second system earns its place by structure, not a missing
   abstraction). *Honest negative:* error-gating **halts at prediction-sufficiency** — the
   learned operator is **directionally** the L2 transition coupling (cosine ≈ 0.81) but not
   **magnitude-identical**; the early-halt is recorded as the seed limit for L7 (L6).

12. **It controls in real time, in a closed analog loop — and the analog I/O thesis holds** ★ —
   placing the L6 forward model in a **closed, clock-free, end-to-end analog sensorimotor loop**
   (sense graded-analog → clean-up by L0 settling = D4 → predict +1 → act by a continuous phase
   step), the substrate performs **real-time control by continuous settling**: the forward model
   **holds a moving target through a sensorimotor delay** (`err≈0`) where a **reactive** controller
   **lags** (`≈0.96`) and **open-loop drifts** (`≈0.77`) — prediction's embodiment role is
   **compensating loop latency** (E1 [V]). The principal's **analog-I/O thesis** is now **tested**:
   the **analog loop beats a b-bit ADC/DAC loop** under graded noise (`1-bit 0.159` vs `analog
   0.001`; **D4 at the I/O boundary**; tax **closes at 2 bits**), and the **dimensional advantage
   scales** — the per-channel gap stays positive and the **aggregate `N×gap` grows** (`4.6→42.1`),
   "the gap widens as resolution rises" (E2 [V]; the O(1)-vs-O(N) latency form is the **R4-inherited
   principle** [O]). **Prediction-sufficiency suffices for control** — the L6 error-gated operator
   (cosine `0.803`) tracks **identically** to the magnitude-identical L2 operator in the working
   regime, so **the inherited S7 [O] is resolved [V]** (E3). A **stable operating band exists**
   (bandwidth threshold + matched prediction horizon; self-corrects from displacement) — the L7
   stress did **not break** real-time control, it **bounds** it (E4 [V]). *Honest two-sides caveat
   (the directive's own):* single-channel bit depth is **Shannon-capped** (effective bits saturate,
   ceiling ∝ SNR) and **exact arithmetic needs a digital hand-off** (analog tally `0.96→0.41` vs
   digital exact `1.00`) — the analog win is **dimensional, not per-channel precision**, with the
   **hybrid** as the named resolution (E5 [O]×2). **4/4 milestone capabilities [V]** (L7).

13. **It shares — a global workspace integrates the specialised modules** ★ — a **global
   metastable resonant hub** (its own L0 clean-up field, so it locks to a **valid** concept, not a
   blur; the L3 von Mises gate selects which module drives it; one **clock-free joint relaxation**)
   **selectively binds** the gated module's pattern and **broadcasts** it so a module that **never
   held it** recovers it from the broadcast **alone** (lock margin **≥0.92** every config;
   non-source recall **1.0** vs a no-hub control at chance) — information made **globally available**
   (G1 [V]). Moving the gate **flexibly routes** any module's content system-wide (**1.0** vs a
   fixed gate at **≈1/M**) — the workspace is **reconfigurable**, not hard-wired (G2 [V]). And a
   **functional PCI-analog** — **integration × differentiation** of the modules' response to a hub
   kick (no Lempel-Ziv, no critical-point tuning; the hub locked **without** broadcasting so modules
   stay distinct, then kicked vs a matched no-kick run, modules read) — is a clean **inverted-U**:
   `0` at **isolated** (`I=0`, no integration), `0` at **over-driven** (`D→0`, no differentiation),
   and a high **interior peak** at the **metastable edge** (g=0.5 for M=4,6; g=0.25 for M=8); the
   integration term **rises** while differentiation **falls** and their **crossover is the access
   band** — exactly the inherited **Gap-4 inverted-U**, with the **number R=0.39 NOT transferred**
   (the access point **emerges** from the sweep) (G3 [V]). The inherited L7 **operating-band limit
   is made concrete**: routing **holds within** the hub's **lock-latency band** (collapses below
   ~10 settle-steps toward chance, holds at ≥20 → 1.0; band edge ≈20) (G4 band [V]). **3/3 milestone
   capabilities [V]** (L8). *Firewall, unchanged at the high-PCI engaged point too:* "access" =
   broadcast **availability** that is integrated **and** differentiated — **no felt quality is
   claimed or measured** (`consciousness_claim=0`, `hard_problem_open=1`). *Honest negatives ([O]):*
   **unbounded-rate** routing is impossible, and a hub that does **not release** its previous
   content (carries it forward) is **not reliably re-routable** even given 4× the dwell (0.71 vs the
   re-cued band's 1.0) — sequential access **favours a fresh ignition per route**.

---

## 4. Next plan (blueprint)

**Large long-term blueprint** → `BLUEPRINT_toward_ultimate_computer.md` (L0–L9,
dependency graph, each layer's milestone + stress test, end condition, firewall).

**Program status (after S10): THE END CONDITION IS REACHED — the blueprint CLOSES.** L9 assessed the
integrated L0–L8 machine against the **capability ladder** (BLUEPRINT §11): **6/7 rungs [V]**, with
**A3 (real-time adaptation)** the lone honest `[O]` — a single additive Hebbian store cannot
*over-write* a switched rule (the old and new associations superpose and interfere; recovery
0.78/0.58 < band), whose **already-proven** mitigation is the L5 **dual store** (A7, retention ~1.0).
The standing caveats on passing rungs (A1 finite capacity, A6 analogy ceiling J\*=3, A7 unbounded
retention) are inherited laws, each stated. The **sufficiency hypothesis is settled**: the L0
wave-substrate properties reach general FUNCTION across the ladder within stated bounds. Closing is
**not** a claim of human intelligence — it is the hypothesis resolved layer by layer.

**Any future session is optional and post-program** (the blueprint has no further layers). The two
disciplined continuations, if pursued, are: (a) **compression** — an axiom-independence audit
(which inherited invariants are load-bearing vs derivable); (b) **hardening** — convergent-evidence
grading and broadening the sweeps (e.g. the A1 K×N sweep, trimmed to N∈{128,256} on a single-core
box, can be widened; A3's single-store limit can be re-probed with the dual store wired in to show
the `[O]→[V]` closure inline). **Of these, the A3 inline closure was executed in S11 (v0.11)** and
**the compression audit (a) was executed in S12 (v0.12):** the re-probe with the dual store wired in
closes A3 `[O]→[V]` on the adaptation task itself (ladder 7/7 [V] with the dual store wired in; the
S10 6/7 single-store record stands as the minimal machine's honest limit), and the axiom-independence
audit compresses the 8 inherited invariants to a **minimal, irreducible 5-axiom operational core**
(all 5 load-bearing, `redundant_axioms=[]`). **Both named continuations (a)+(b) are now done.** What
remains optional and post-program: only further hardening (b) such as widening the A1 K×N sweep. No
new layer, no tuning; one zip, additive. Firewall (final, invariant): passing the ladder is
**functional** general intelligence — the hard-problem blank stays open.

**Immediate next chunk (S12) — DONE.** Post-program compression, the axiom-independence audit (8→5,
irreducible, 5/5 load-bearing): see the S12 ledger row and `SESSION_v0_12_axiom_independence_audit.md`.
*(Prior: S11 — DONE — post-program hardening, A3 `[O]→[V]` closed inline,
`SESSION_v0_11_adaptation_closure.md`; S10 — DONE — L9 functional general intelligence,
`SESSION_v0_10_functional_general_intelligence.md`.)*

**Global access L8 — RESOLVED (strongly positive) ★.** A **global metastable resonant hub**
**selectively binds** the gated module's pattern and **broadcasts** it so a non-holder module
recovers it (lock margin ≥0.92; non-source recall 1.0 vs no-hub chance) — information made
**globally available** (G1 [V]); moving the gate **flexibly routes** any module's content
system-wide (1.0 vs fixed-gate ≈1/M) — reconfigurable, not hard-wired (G2 [V]); and a **functional
PCI-analog** = integration × differentiation is an **inverted-U** with a high **interior** peak,
`0` both isolated (I=0) and over-driven (D→0) — the inherited **Gap-4** signature, the **number
R=0.39 NOT transferred** (the band emerges) (G3 [V]). **3/3 milestone capabilities [V].** The
inherited L7 operating-band limit is **made concrete**: routing **holds within** the hub's
**lock-latency band** (edge ≈20 steps) (G4 band [V]), with two honest counterpoints recorded
([O]: unbounded-rate routing; [O]: persistent no-release over-write routing — given 4× dwell a
carry-forward hub reaches only 0.71 vs the re-cued 1.0). The **firewall holds at the high-PCI
engaged point too**: a high functional-PCI-analog is **broadcast information made globally
available and kept distinct**, nothing more — no felt quality claimed or measured.

**Embodiment L7 — RESOLVED (strongly positive) ★.** **Control = continuous settling** in a
closed, clock-free, **end-to-end analog** sensorimotor loop. The forward model **holds a moving
target through sensorimotor delay** where reactive lags and open-loop drifts (E1 [V]); the
**analog loop beats a b-bit ADC/DAC loop** under graded noise (D4 at the I/O boundary; tax closes
at higher b) and the **dimensional advantage scales** — aggregate `N×gap` grows (E2 [V]; the
O(1)-vs-O(N) latency form is the **R4-inherited principle** [O]); **prediction-sufficiency
suffices for control** so **the inherited S7 [O] is resolved [V]** (E3); and a **stable operating
band exists** (E4 [V]). The principal's **analog-I/O thesis is now tested, not asserted** — analog
**dominates the dimensional axis** and is **capped on single-value bit depth** (Shannon), with the
**hybrid** for exact arithmetic: the two honest counterpoints are recorded (E5 [O]×2).

**World model L6 — RESOLVED (strongly positive).** Prediction = **forward settling** and
learning = the **difference wave**: the substrate learns an unlabeled stream from its own
error (W1 [V]), rolls out plausible continuations to a finite horizon (W2 [V]), flags
novelty with the same error wave (W3 [V]), and a **forward model beats reactive recall**
because the advantage is **directionality**, not a missing abstraction (W4 [V], the
headline — the C4 break honoured). The one honest limit is that error-gating **halts at
prediction-sufficiency** (operator directionally L2, not magnitude-identical) — **now resolved
in L7** (prediction-sufficiency suffices for control).

**Dual learning L5 — RESOLVED (mostly positive), and it CLOSES L4.** Consolidation builds
a generalising slow store (C1 [V]); the dual store reduces catastrophic forgetting (C2 [V]);
and as an **independent context channel** the slow store restores strict capacity to ~oracle
where content-derivation degrades — **the L4 [O] is now [V]** (C3, the headline). The only
honest limit is the textbook **double** dissociation, which does **not** hold on a single
Hebbian substrate (C4 [O], fast generalises for free) — recorded with its mechanism named.

**Pivotal layer L4 — RESOLVED (largely positive).** *Resonance inference without
computation* **holds** on the cognitive forms: the gate is derived (no oracle),
constraint satisfaction **= settling**, analogy **= resonance**, probabilistic inference
**= noisy settling** (4/5 [V]). One honest structural limit ([O], strict capacity ⊥
derivability) is recorded with its resolution named (a context channel, L5) — so the
"go to a hybrid" branch was **not** triggered; the machine reaches general cognitive
function on the wave track, with the limit on the books.

---

## 5. File map

```
HANDOFF.md                              ← read first (cold-start, binding)
START_HERE_wave_computer.md             ← this file (entry · status · ledger)
INHERITANCE_MANIFEST.md                 ← what was inherited (self-contained)
BLUEPRINT_toward_ultimate_computer.md   ← large long-term blueprint (L0–L9)
CUMULATIVE_LOG.md                       ← cumulative work history (append-only)
SESSION_v0_1_design_study.md            ← S1 full record (substrate L0)
SESSION_v0_2_resonance_and_learning.md  ← S2 full record (L1 four properties)
SESSION_v0_3_structure_and_time.md      ← S3 full record (L1 complete + L2 start)
SESSION_v0_4_hierarchy_and_abstraction.md ← S4 full record (L3 hierarchy + abstraction)
SESSION_v0_5_inference_and_resonance.md ← S5 full record (L4 resonance inference ★ pivot)
SESSION_v0_6_dual_learning_systems.md   ← S6 full record (L5 dual learning systems · L4 [O]→[V])
SESSION_v0_7_self_supervised_world_model.md ← S7 full record (L6 world model: prediction = forward settling)
SESSION_v0_8_embodiment_and_control.md  ← S8 full record (L7 embodiment / real-time control: control = continuous settling, analog loop)
SESSION_v0_9_global_integration_and_access.md ← S9 full record (L8 global integration / functional access: a global resonant hub broadcasts the dominant pattern)
SESSION_v0_10_functional_general_intelligence.md ← S10 full record (L9 END CONDITION: the integrated L0–L8 machine on the capability ladder, 6/7 [V])
SESSION_v0_11_adaptation_closure.md     ← S11 full record (POST-PROGRAM HARDENING: A3 [O]→[V] closed inline with the dual store wired in, ladder 7/7 [V])
SESSION_v0_12_axiom_independence_audit.md ← S12 full record (POST-PROGRAM COMPRESSION: axiom-independence audit, 8→5 axioms, 5/5 load-bearing, irreducible [V])
CITATION.cff                            ← citation metadata (concept DOI 10.5281/zenodo.20783570)
repro/
  wave_compute_core.py   + results.json + atlas.png + expected_digest.json    (S1, FROZEN L0)
  wave_resonance_core.py + results.json + atlas.png + expected_digest_v0_2.json (S2)
  wave_structure_core.py + results.json + atlas.png + expected_digest_v0_3.json (S3)
  wave_hierarchy_core.py + results.json + atlas.png + expected_digest_v0_4.json (S4)
  wave_inference_core.py + results.json + atlas.png + expected_digest_v0_5.json (S5)
  wave_consolidation_core.py + results.json + atlas.png + expected_digest_v0_6.json (S6)
  wave_world_model_core.py + results.json + atlas.png + expected_digest_v0_7.json (S7)
  wave_embodiment_core.py + results.json + atlas.png + expected_digest_v0_8.json (S8)
  wave_workspace_core.py + results.json + atlas.png + expected_digest_v0_9.json (S9)
  wave_agi_core.py + wave_agi_results.json + wave_agi_atlas.png + expected_digest_v0_10.json (S10, L9 END CONDITION)
  wave_adapt_closure_core.py + wave_adapt_closure_results.json + wave_adapt_closure_atlas.png + expected_digest_v0_11.json (S11, POST-PROGRAM HARDENING — A3 [O]→[V] closed inline)
  wave_axiom_audit_core.py + wave_axiom_audit_results.json + wave_axiom_audit_atlas.png + expected_digest_v0_12.json (S12, POST-PROGRAM COMPRESSION — axiom-independence audit, 8→5 irreducible)
  make_figure.py / make_figure_v0_2.py / make_figure_v0_3.py / make_figure_v0_4.py / make_figure_v0_5.py / make_figure_v0_6.py / make_figure_v0_7.py / make_figure_v0_8.py / make_figure_v0_9.py / make_figure_v0_10.py / make_figure_v0_11.py / make_figure_v0_12.py
  check_completeness.py   ← self-containment + reproduction audit
```

**Reproduce / audit:** `python3 repro/check_completeness.py` (checks all files
present, re-runs all twelve sims, compares digests bit-for-bit).

---

## 6. Invariant rules (inherited; every session)

1. **English only**, going forward.
2. **One zip, additive, no fresh tree, nothing dropped** (cumulative + this session +
   updated blueprint).
3. **Frozen substrate L0 is READ-ONLY** — upper layers reuse, never modify.
4. **No tuning** — inherited numbers are principles, not fitting targets.
5. **Stress Principle** — a new claim earns `[V]`/`[L]` only by passing a test
   designed to break it; a break is recorded and the line restarts with it applied.
6. **Firewall** — function only; the hard-problem blank stays open, never erased.
7. **Physical realization deferred** — theory track now.

---

*This is an in-silico model + theory blueprint — not validated engineering, not a
built device. A new long-term program atop two frozen whitepapers (`vp_frontal v2`,
`vp_physics v0.11.0`), whose inherited content is fully captured here so this archive
stands alone.*
