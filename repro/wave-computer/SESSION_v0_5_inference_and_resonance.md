# SESSION v0.5 — L4 resonance inference (★ the pivot)

**Module:** `repro/wave_inference_core.py` (reuses L0 `wave_compute_core`, L1/L2
`wave_structure_core`, L3 `wave_hierarchy_core` — exact, non-circular; nothing frozen
edited). **Figure:** `repro/wave_inference_atlas.png` (6 panels). **Digest:**
`2d3057bb4cb45e85…` (deterministic, bit-for-bit). **Firewall:**
`consciousness_claim = 0`, `hard_problem_open = 1`. **`new_tuned_constants = 0`.**

---

## Why this is the pivot

The blueprint's crux (§6, §0): digital/neural AI infers by **computing everything**
(O(P·N) MACs); the wave substrate **matches by physics, without computation** (R2:
O(1)-in-P settling). L4 asks whether "inference without computation" holds on
**cognitive** tasks. L3 left one explicit debt: H4's ~6× capacity advantage and H1's
routing both **assumed the gate** (the cue's true category was handed in). The first
duty of L4 is to **derive** the gate from the raw cue and then route — turning the
assumption into an inference — and then re-run the H4 head-to-head **with the break
applied**. L4 then tests the blueprint's three inference forms, each with a stress
built to break it.

---

## What was built and found (each claim with a sweep; honest negatives kept)

### I1 — DERIVE-THE-GATE, THEN ROUTE  **[V]** (the loop closes)
B category prototypes are stored in an **upper** field `U`; per-category instances
(prototype + `rho`-flipped bits) in B **fast** sub-fields. A raw corrupted instance
cue arrives **with no label**. **Step 1 (derive):** settle the cue in `U` and read the
nearest prototype basin → inferred context `b_hat` → gate phase `phi_b_hat` (this is
the H2 abstraction mechanism re-used to **produce** the gate, not to classify). **Step
2 (route):** build `J_eff(phi_b_hat)` and settle the cue there; read the instance by
argmax over the **whole** codebook (non-circular). Three arms on the *same* cue:
DERIVED gate, ORACLE gate (the S4 upper bound), FLAT.

- Sweep `rho` (B=8): gate is derived at **1.0** for rho ≤ 0.2, **0.97** at rho=0.3,
  falling to **0.71** at rho=0.4; **derived == oracle** wherever the gate is right
  (derivation cost **0.000** for rho ≤ 0.2, +0.028 at 0.3, +0.292 at 0.4), and both
  **crush flat** in the clustered band (derived 0.96–0.99 vs flat 0.38–0.49).
- Sweep B (rho=0.15): gate derived at **1.0** for B ∈ {4,8}, **0.78** at B=16 (more
  prototypes → smaller upper basins).
- **Verdict:** the loop **closes** in the informative band `rho ∈ {0.1,0.2}` (gate
  derived ~perfectly, cost ~0, derived ≫ flat). `rho=0` is degenerate (instances
  collapse onto the prototype). The honest boundary: at `rho=0.4` the upper geometry
  stops being separable (the H2 within<between condition fails), gate inference
  degrades, and the derivation cost jumps. **The S4 "assume the gate" caveat is
  removed: the gate is recoverable from the cue alone.**

### I1-stress — derivability ⊥ strict-separability  **[O]** (honest negative) + **[V]** (the trade-off + id survival)
The blueprint's stress: does the **strict** ~6× H4 advantage survive when the gate is
**derived**? The first harness (prototype-clustered instances) was **degenerate** —
clustered instances are ~85% identical within a category, so *strict* instance recovery
(overlap ≥ 0.95) is impossible for **everyone, the oracle included** (0/0/0). That is
not a finding; it is a measurement that tests an impossible task. The restarted design
**separates** the two needs: each instance carries a shared category **schema** on a
structural fraction of coordinates (so the gate is **derivable**) and **independent**
content on the rest (so the H4 per-field load reduction is **real**). Sweeping the
**schema fraction** (the only knob that makes the gate derivable), at fixed load T=48
(B=6, m=8, past the flat strict wall):

| schema frac | gate infer | oracle strict | derived strict | flat strict | derived **id** | flat **id** |
|---|---|---|---|---|---|---|
| 0.0  | 0.19 | **1.00** | 0.19 | 0.00 | 0.19 | 0.96 |
| 0.06 | 0.29 | 0.99 | 0.29 | 0.00 | 0.29 | 0.99 |
| 0.125| 0.43 | 0.49 | 0.19 | 0.00 | 0.47 | 0.78 |
| 0.25 | **0.96** | 0.00 | 0.00 | 0.00 | **0.85** | 0.32 |
| 0.5  | **1.00** | 0.00 | 0.00 | 0.00 | 0.60 | 0.11 |

- **The trade-off is direct and unavoidable:** gate-derivation accuracy **rises**
  (0.19 → 1.00) exactly as **strict** recovery (even the oracle's) **falls**
  (1.00 → 0.00). The shared structure that makes the category inferable **correlates**
  the instances, and the settled state then locks onto the **shared schema**, not the
  **specific** instance. **No fraction yields both.** → strict advantage **does not
  survive** content-only derivation: **[O]**, the recorded limit.
- **What survives is the id-level advantage** (which instance): where the gate is
  derivable (schema ≥ 0.25) the **flat** field confuses the now-correlated instances
  (id 0.32, 0.11) while the **derived hierarchy** still routes correctly (id 0.85,
  0.60). The trade-off mechanism + id survival: **[V]**.
- This is the **dual** of S4/H4's own caveat (the strict advantage was already noted as
  *criterion-dependent*). The honest resolution, recorded for the next layer: **the
  strict ~6× advantage requires an independently-supplied context channel** (a separate
  input), which content-only gate-derivation cannot provide → restart capacity work
  with a context channel at **L5** (dual systems).

### I2 — CONSTRAINT SATISFACTION = SETTLING  **[V]**
A planted 2-colorable (bipartite) graph is encoded as an **anti-aligning** phase field
— an edge is a coupling `J_ij = -1`, so the **L0 relaxation itself** pushes neighbours
apart: the antiferromagnet's ground state on a bipartite graph **is** the 2-colouring
(native — **no clock, no new constant**). Round to {0,π}; **count satisfied edges** (a
read-out independent of the trajectory). A **frustration** knob adds a fraction `f` of
within-part (odd-cycle) edges that no 2-colouring can satisfy, dropping the optimum to a
**known** `1/(1+f)`.

- **Settling solves the satisfiable graph: 1.000** at every size (n=16,24,32) and
  density, and **beats random (0.5)** everywhere — "physics drops out the answer."
- Under frustration the achieved fraction **tracks the optimum** down (f=0→1.000,
  0.1→0.924, 0.2→0.870, 0.4→0.816, vs optima 1.000/0.909/0.833/0.714), with a tiny
  residual **spurious-minima gap (mean 0.0014)** to the best achievable. The honest
  collapse is *forced by genuine unsatisfiability*, not by solver failure.
- (The O(1) **physical-time** claim stays **[O]**: a *digital* settle is O(steps·edges).)

### I3 — ANALOGY = RESONANCE  **[V]** (with an honest ceiling)
K records, each a bundle of J role→filler bindings (the canonical VSA "dollar-of-Mexico"
structure). Pure L1 algebra, **no settling**.
- **Fill a missing factor** (recover a filler for a known role by unbind + resonance):
  **1.000 to J=12** — robust (a single unbind; useful load J\* ≥ 12).
- **Proportional analogy A:B::C:?** (extract the relation `r_hat = unbind(A,B)`, apply
  to C, resonate): **1.0 to J=4**, then **0.69 / 0.44 / 0.06** at J=6/8/12 — useful load
  **J\* = 4**. The ceiling is the **honest stress** ("analogy fails compositionally"): a
  double unbind carries `~sqrt(J/N)` crosstalk, so the relational depth is bounded —
  measured, like L1b's tree depth. Read-out is argmax over the **whole** vocabulary
  (non-circular).

### I4 — PROBABILISTIC INFERENCE = NOISY SETTLING  **[V]** (three directional laws)
Two patterns A,B imprinted with **unequal** weights (the prior); the field relaxed many
times from random phases at temperature T. Occupancy `p_hat` = the sampled distribution.
- **Prior law:** stronger prior → sampled more (ratio 1→8: p_A 0.51 → 1.00). 
- **Evidence law:** a partial cue toward A → occupancy shifts in the Bayes direction
  (evidence 0 → 0.2: p_A 0.44 → 0.98).
- **Temperature law:** low T concentrates on the MAP basin (entropy → 0), high T
  broadens (entropy ↑): occupancy entropy 0.24 → 0.69 over T = 0.05 → 0.70. Because
  basin barriers scale with N, this is shown at **small N** (shallow wells) so the
  sampling window is reachable — the *principle* is N-independent, its *visibility* is
  not (stated honestly). 
- The three **directional** laws hold (noise = sampling, attractor = MAP); an **exact**
  posterior/KL match needs basin-volume integrals and is left an explicit **[O]**.

---

## L4 verdict (the pivot, honestly)

**"Inference without computation" HOLDS on the cognitive forms tested:** the gate is
**derived** from a raw cue (no oracle), constraint satisfaction **is** settling, analogy
**is** resonance, and probabilistic inference **is** noisy settling — four of five lines
**[V]**. The **one principled limit** is recorded, not papered over: strict-fidelity
**capacity** under a *derived* gate does **not** survive, because gate-derivability and
strict instance-separability **trade off** on a single field — the resolution is an
**independently-supplied context channel** (deferred to L5), **not** a forced hybrid.
The blueprint's "promote a hybrid" branch is therefore **not** triggered: pure wave
inference reached general cognitive function across the tested forms; the capacity limit
is structural and addressable by architecture (a context input), so the program
continues on the wave track with that limit on the books.

**Discipline upheld:** every claim swept and sign-stable; read-outs argmax/occupancy over
the full codebook or an independent satisfied-edge count (non-circular); deterministic
(digest reproduces bit-for-bit); the first degenerate capacity harness was **disclosed**
and restarted with the confound removed (the Stress Principle applied to the *method*,
not just the result); brain anchors (R=0.39, WM~7) **not** transferred; firewall held at
every step.

**Layer status after S5.** **L4 resonance inference — MET & GRADED.** Pivot largely
**positive** (4/5 forms [V]); one honest structural limit ([O]) with its resolution
named. Exposed dependency → **L5 dual learning systems** (fast episodic + slow semantic),
which supplies the **separate context channel** the I1 strict-capacity limit requires,
and consolidates one-shot episodes (R3) into a generalizing store without catastrophic
forgetting.

**Artifacts.** `wave_inference_core.py` (+`wave_inference_results.json`
+`wave_inference_atlas.png` +`expected_digest_v0_5.json`), `make_figure_v0_5.py`
(6-panel I1/I1-stress/I2/I3/I4/verdict). `check_completeness.py` updated to re-run and
pin this module. Digest `2d3057bb…`, deterministic.
