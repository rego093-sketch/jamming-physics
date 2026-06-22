# F1 — Is the cortical node a temporal chain-holder? A first-principles test on the frozen engine

**Simulation:** `vp_frontal` (independent; not the 29th atlas citizen).
**Discipline:** physics-derived · gene-grounded · LOCK→Derive→Gate · **no-tuning** · SEED = 19 · READ-ONLY engine · anti-tuning sweeps + seed-averaging · honest grading **[V]/[L]/[O]** · **efficacy = 0** · **NOT medical advice** · **Axis-A firewall** (`consciousness_claim = 0`) · **hard problem OPEN**.
**Status:** gated chapter. The companion document `frontal_lobe_hypothesis.md` is a **candidate idea**, not a specification; its probe tables are **not** treated as ground truth. Every read-out below is defined on principle and graded by what the frozen engine **robustly** supports.

---

## 0. The question, and the two hard limits

The hypothesis under test (**H1**): the cortical node is **not** where many inputs are *gathered* into a percept (a spatial convergence node) but the node that, once a coherent state is built, **holds** it across time (a temporal chain-holder). Two limits bound everything here and are stated once:

1. **The engine cannot resolve "the frontal lobe."** The frozen substrate has **12 coarse organ nodes**; the cortical node is the undifferentiated `neocortex` (FOXG1) lump. Every claim that says "frontal" is a claim about **the whole cortical node**. There is no cortico-cortical microstructure, so a frontal-specific function cannot be localised within cortex. A real test needs a v2 substrate that resolves cortical long-range hubs — which the **frozen READ-ONLY engine cannot provide without being broken**.
2. **Intellectual disability (ID) is not a module** here — only a proposed discriminant test (the O×W double dissociation, owed a large cohort simulation, F3).

The engine-invariance guard reproduces the frozen **M9 anchor** `R = 0.38961455156044245` **bit-for-bit** via the engine integrator (not ~1e-13): the read-outs run on the unmodified substrate, and the full emergence tree + the M0–M16 developmental subtree are byte-unchanged after the chapter runs.

---

## 1. The cortical node is **not a gatherer** — robust [V mech]

"Gathering" is operationalised as **convergence**: the effective fan-in of each kernel row, `1 / Σ_j W0[i,j]²` (the inverse participation ratio — the effective number of neighbours a node draws input from). This is static geometry of the frozen ephaptic kernel.

The cortical node has the **lowest** fan-in of all twelve nodes (effective in-degree ≈ 1.00, rank 1/12): it draws essentially **all** of its input from a single neighbour. The convergence **hub** is the **thalamus** (effective in-degree ≈ 4.95). The cortical node does not gather; the thalamus does. This is robust and exact, and it **refutes** the earlier "frontal = patternisation / convergence node" idea.

## 2. The cortical node is a **fast broadcaster** — robust [V mech]

Pairing fan-in with **out-influence** (the column mass other nodes place on a node) gives a clean asymmetry. The cortical node has the lowest fan-in (rank 1/12) but **moderate-to-high out-influence** (column-mass rank ≈ 4/12) at a natural frequency of **40 Hz**. It listens to ≈ one source and influences many: a fast **broadcaster locked to one input**, not an integrator. Robust.

## 3. The cortical node is **not a robust temporal holder** — honest negative [O]

H1's positive claim is that the cortical node *holds* the chain. Three independent tests, under anti-tuning, do **not** support it.

**(a) Thread-holding under a scatter sweep is operating-point-specific.** Driving the cortical node focally and measuring how well it maintains the global order parameter against frequency scatter `disp`, the cortical node ranks 2/12 at the probe's `disp = 5` but its rank ranges across **2–9** as the scatter level is swept (at low scatter the cerebellar reach-hub dominates; at high scatter no single node holds). The rank-2 result is a scatter-specific artefact.

**(b) The lobotomy sustained collapse is a single-window resonance.** Silencing the cortical node and comparing **instant** coherence (built from incoherent input) with **sustained** coherence (an already-coherent state held over a window `Th`), the cortical node is the only major node with the spared-instant/collapsed-sustained signature **only at `Th ≈ 0.5 s`** — at the adjacent windows the winner is a different node (hippocampus, midbrain). Across a fine `Th` sweep it is the major winner at exactly **one of eight** windows. The probe's table happened to sample that one window. (The instant-spared sign *is* robust across every window — but that only confirms the cortical node is peripheral to *building* coherence, consistent with its low fan-in.)

**(c) The decisive test: seed-averaged perturbation-recovery.** The single-point probes lack the anti-tuning that distinguishes a real sustaining role from an operating-point coincidence: averaging over perturbation realisations. Settling to the coherent attractor, applying a standardised phase kick, and measuring the recovered order parameter with each node silenced — averaged over **20 kick realisations** — silencing the cortical node has a **negligible, non-significant** effect on recovery (mean ΔR ≈ −0.0003 ± 0.0013; rank 4/12). The nodes whose silencing genuinely degrades recovery are the **slower, well-coupled subcortical hubs** (cerebellum f0 = 12 Hz, with midbrain and basal-forebrain next), **not** the fast cortical broadcaster.

**Verdict.** The apparent thread-holding signatures are operating-point artefacts; the robust, seed-averaged test finds the cortical node's sustaining role negligible. **H1's temporal-holding claim is not confirmed by this engine.** The role of *holding coherence over time* lives in slower subcortical hubs, not the cortical node.

**Why the negative.** This is a direct consequence of **Hard Limit 1**: the engine has no cortico-cortical microstructure to carry a frontal-specific holding function. The model **generates** H1 — sharply enough to test — but the frozen engine **cannot confirm** it; confirming it would require a v2 substrate that resolves cortical hubs, which would break the frozen engine. This is an honest scope limit, reported as such, not a confirmation. It is the recurring lesson of the framework in its cleanest form: the model alone cannot settle the frontal question; the substrate is blind to the structure the question is about.

---

## 3.5 Can the engine reproduce the leucotomy patient record? — honest negative [O]

If the cortical node is not a holder, perhaps removing it reproduces the *documented* frontal-lesion behaviour another way. The leucotomy/lobotomy record is two-sided: **perception, sensation and immediate response preserved**, but **perseveration, cognitive inflexibility and behavioural flattening** (the Wisconsin Card Sort deficit; the loss of set-shifting). Crucially, leucotomy **severed** the cortical node's white-matter connections — it did not silence the node — so the faithful lesion is a **disconnection** (remove the cortical node's coupling row and column, isolating it), not an inhibitory bias.

Two behavioural read-outs on this disconnection, input → process → output:

- **Perception** — the order parameter while a stimulus is present (focal drive on a cue node). Across a duration sweep this is **robustly spared** (≈ −3%): disconnecting the cortical node barely touches the immediate response. But this is *because the cortical node is peripheral to coherence* (its low fan-in), **not** evidence of a preserved-perception/lost-executive dissociation.

- **Flexibility (set-shifting)** — drive cue A, then switch the drive to B, and measure how far the field's configuration moves away from the A-pattern (`1 − |⟨exp(i(θ_endB − θ_endA))⟩|`); low = the output stayed locked to A = **perseveration**. A single operating point (phase duration ≈ 1.2 s) gives a clean perseveration result (≈ −9% flexibility) that *looks* exactly like the frontal record. **But it does not survive anti-tuning.** Across the duration sweep the sign **flips**: at 0.8–1.0 s disconnecting the cortical node makes the field *more* flexible (+13 to +15%); at 1.2–1.5 s it makes it *less* flexible (−9 to −12%). The perseveration signal is an **operating-point artefact**, exactly like the holding signal in §3.

**Verdict.** The engine reproduces **no robust frontal-lesion behavioural phenotype** by removing the cortical node. The temporal-holding signature is negligible; the set-shifting/perseveration signature flips sign under anti-tuning. The only robust facts are the **static structure** (§1–§2) and that **removal is nearly silent** (perception spared because the node is peripheral). This is **Hard Limit 1 in its strongest form**: a 12-node engine whose cortical node is an undifferentiated lump cannot carry a stable frontal phenotype.

**Methodological note.** The first probe — one phase duration — produced a clean, publishable-looking perseveration result that matched the clinical record. The duration sweep revealed it flips sign. This is the framework's anti-tuning discipline catching a false positive: a single operating point can manufacture any frontal signature you expect to see; only sweeping the operating point separates structure from coincidence. The same discipline retired the probe's "thread-holder" tables.

---

## 4. Where this leaves the axis decomposition

The proposed **D axis** (temporal chain depth / sustaining) is **not cleanly carried by the cortical node in this engine** — a caution that propagates to the cohort work (F3). By contrast the **W** (long-range routing), **T** (R19 ignition fold) and **E0** (plasticity) axes *are* robust engine handles; the stereotypy coupling (F2, `T × W × E0`) and the O×W double dissociation (F3) are built on those, not on the engine-blind D axis. F1's honest negatives sharpen what F2/F3 may and may not claim: **clinical phenotypes that require cortical microstructure cannot be read off this 12-node engine**, and any frontal-lesion signature must be shown sign-stable under a duration sweep before it is believed.

| pre-registered | verdict | grade |
|---|---|---|
| **P1** cortical node = not a gatherer, a fast broadcaster | **CONFIRMED** (robust, exact) | **[V mech]** |
| **P2** cortical node = temporal chain-holder | **NOT CONFIRMED** (apparent signatures operating-point-only; seed-averaged role negligible; holding lives in subcortical hubs) | **[O — honest negative]**, Hard Limit 1 |
| **P6** removing the cortical node reproduces the leucotomy record | **NOT CONFIRMED** (perception robustly spared, but only because the node is peripheral; the perseveration signal flips sign under a duration sweep — an operating-point artefact) | **[O — honest negative]**, Hard Limit 1 |
| **P3** autism = W-fault with dissociable D | candidate; D-axis caution from P2 | [V/L] |
| **P4** stereotypy = T × W × E0 | owed (F2) | [L candidate] |
| **P5** O×W double dissociation | owed (F3 cohort sim) | [L candidate] |

---

## 5. Firewall, grading, provenance

**Firewall (absolute, YMYL/medical).** Every quantity — fan-in, out-influence, thread-holding, lesion asymmetry, recovery — is a **structural quantity of the coupling model on a frozen 12-node kernel**, **not** the felt quality of cognition, perception, sociality, disability or any clinical state; **not** a real connectome, current density, electrode or dose; **not** a diagnosis, prognosis or treatment-matching. A node "holding the thread" or "losing the chain" is a statement about coherence in a 12-node model, **not** a claim that anything is experienced. Lobotomy/leucotomy is read **only** as lesion evidence; it was a crude, abandoned procedure — **not** an endorsement, **not** medical advice. `consciousness_claim = 0`; **hard problem OPEN**.

**Grading.** P1 (not a gatherer, a broadcaster): **[V mech]**, robust. P2 (temporal holding) and P6 (leucotomy behavioural record): both **[O — honest negative]**. All magnitudes are **[O]**; only signs/structure are asserted.

**Provenance (frozen engine, READ-ONLY; unchanged by this chapter).** engine file sha `e61083ae…`; emergence tree `0fbf4988…`; M9 anchor `R = 0.38961455156044245`; R19 fold spinodal(1) = 0.3849; B(1) = 0.25; KAPPA = 0.5496; OMEGA0 = 118.857; N = 12; SEED = 19. Reusable layers hash-pinned (e0/e1/e2). The frontal gate runs the engine tripwire, byte-determinism ×2, and the honesty-ledger discipline, and never calls the mind atlas runner.

*This chapter's value is its honesty. It states a sharp hypothesis, tests it three ways, and reports that the frozen engine robustly refutes the convergence reading, cannot confirm the temporal-holding reading, and cannot reproduce a stable leucotomy behavioural phenotype — every apparent frontal signature dissolving into an operating-point artefact under anti-tuning — and says exactly why: a 12-node engine is blind to the cortical microstructure the frontal question is about. The user asked the simulation to find the frontal-removal record; the rigorous answer is that this substrate does not contain it, and a v2 substrate that did would have to break the frozen engine.*
