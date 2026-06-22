# SESSION v0.12 — POST-PROGRAM COMPRESSION: the axiom-independence audit

**Status of the program:** the blueprint **CLOSED** at S10 (L9, the END CONDITION); S11 closed the last open rung A3 `[O]→[V]` inline. This session is the **other** named post-program continuation — continuation **(a) compression**, named identically in `HANDOFF.md` §3, `START_HERE_wave_computer.md` §4, and `BLUEPRINT_toward_ultimate_computer.md` §11/§12: *an axiom-independence audit of the inherited invariants.* It adds an audit; it builds no new layer, closes nothing that was open in the blueprint, and opens nothing new. With it, **both** post-program continuations the program named for itself — (a) compression and (b) hardening — are now executed.

**Frozen inputs reused exactly, non-circularly:** L0 `wave_compute_core` (`hebbian_field`, `relax` = D4 attractor clean-up, `global_R`, `overlap`, `pattern_to_phase`, `corrupt_phase`, `SEED`) — **the L0 substrate is never edited.** The audit's knock-outs are constructed in the *new* module as deliberately broken *substitutes* for L0 primitives (a random symmetric field, an asymmetric field, a linear flow, a zero-step settle, a ferromagnetic drive); the genuine primitives are imported and used unchanged for the intact arm of every paired contrast. `new_tuned_constants = 0`. Firewall held byte-for-byte: `consciousness_claim = 0`, `hard_problem_open = 1`.

**Artifacts:** `repro/wave_axiom_audit_core.py` · `repro/wave_axiom_audit_results.json` (digest pinned in `repro/expected_digest_v0_12.json`) · `repro/make_figure_v0_12.py` → `repro/wave_axiom_audit_atlas.png`. Registered in `repro/check_completeness.py` (DOCS + REPRO + SIMS) so it re-runs and pins bit-for-bit alongside the other eleven modules.

**Digest (reproduces bit-for-bit from SEED):** `7f59ced681bdf8b83396b1b4c8d37f639460f66dacbce34291633f91e4fc45a0`.

---

## Why this session

The program inherited **eight** invariants and treated them as load-bearing throughout: five from the brain — **B1** ephaptic near-field coupling, **B2** phase (Kuramoto/XY) coupling, **B3** metastable critical operating band, **B4** attractor pattern-completion, **B5** theta-gamma capacity multiplexing — and three from physics — **P1** medium stiffness = coupling gain, **P2** clock-free lattice propagation, **P3** 1/r² near-field reciprocity. The blueprint asserted these were *necessary*. But "we assumed eight things and the machine worked" is weaker than "we know which of those eight the machine actually *stands on*." Compression asks the dual of the construction question: not *do these suffice to build it* (S1–S10 answered yes), but **is the inherited set minimal, and is each surviving piece truly required** — or is some of it ballast that a leaner machine could drop?

This mirrors the program's own `[V]`/`[O]` method, turned inward on its own premises: take each thing the program was *given*, **null exactly it while keeping everything else intact**, and let the data decide whether it was load-bearing (a collapse, `[V]`) or redundant (no collapse, a further compression — an honest negative against our own assumption). No claim of irreducibility is asserted; it is **derived** from break-tests.

---

## The method (one non-circular probe, generic thresholds, no tuning)

Every axiom is judged by **one universal, non-circular probe**: store a set of random ±1 patterns in the coupling field, present a **corrupted** cue (15% sign-flips + phase jitter), settle, and measure **capacity** = the fraction of patterns recovered past an inherited recall band (overlap ≥ 0.95). The thing perturbed (which axiom is intact) is never the thing read (recovery of an independently-drawn stored pattern) — so the probe cannot smuggle in its own answer.

Two properties make the verdict trustworthy:

- **Paired & sign-stable.** Each axiom is run as a strict paired contrast — intact arm vs knocked-out arm, *identical* patterns, cues, and seed — repeated across **6 seeds**. A collapse counts only if it holds the **same sign at every seed** (`collapses_sign_stable`).
- **A positive control gates the harness.** The fully intact substrate is run through the *same* harness first: capacity **0.967**, overlap **0.997**, R **0.062** (metastable). Because the intact machine recovers, any collapse below is attributable to the **knock-out**, not to the harness.

Only **generic separability thresholds** are used — the inherited recall band (0.95) and a halfway margin (0.5). **No number is fit to a target;** `new_tuned_constants = 0`. Grades are computed from the sweep booleans, never asserted. Fixed harness: N = 128, store 5 patterns, 15% flips, 0.30 jitter, 250 settle steps, 6 trials × 6 seeds.

---

## C0 — the inheritance compression (8 → 5), structural

Before ablating, the eight inherited invariants are mapped onto the operational primitives the frozen L0 actually exposes. **Several inherited invariants collapse onto the same operational mechanism**, so the inherited set is **not minimal at the operational level**:

| operational axiom (L0) | inherited invariants it absorbs |
|---|---|
| **AX1** data-encoded coupling field | B1 ephaptic field **+** B4 attractor *storage rule* |
| **AX2** field symmetry / reciprocity (J = Jᵀ) | B4 attractor *Lyapunov structure* **+** P3 1/r² near-field reciprocity |
| **AX3** coupling nonlinearity (sin Δθ) | B2 phase (Kuramoto/XY) coupling |
| **AX4** settling / clock-free relaxation | P2 clock-free propagation **+** B2 self-timed phase dynamics |
| **AX5** metastable operating band | B3 critical band **+** P1 stiffness = gain |

**B5 (theta-gamma capacity) is deliberately *not* an L0 axiom.** Theta-gamma multiplexing is a *higher-layer* realization built at L2/L3 (the capacity-multiplexing register), not a property of the L0 substrate itself. It is recorded as **deferred** — neither ablated here nor claimed as part of the minimal substrate core. So the honest compression statement is: **eight inherited invariants map onto five independent operational axioms in the frozen substrate, with one inherited item (B5) deferred to a higher layer.** Whether those five are *each* required is exactly what C1–C5 then break-test.

---

## What was built and found (paired ablations; every collapse sign-stable across 6 seeds)

### C1 — AX1 data-encoded field · **load-bearing [V]**

Knock-out: replace the Hebbian field with a **magnitude-matched random symmetric field** (same scale, data *not* encoded). Capacity **0.90 → 0.00** at every seed; gap 0.90. A medium not sculpted by the data has the stored patterns as **non-attractors** — a clean recall never happens. (The residual overlap ~0.52 sits between the cue level and chance because a non-encoding field is largely **inert**: it neither recalls the pattern nor must scramble the cue. Capacity, the decision metric, is what goes to zero.) The other four axioms are intact and do **not** rescue it. → independent.

### C2 — AX2 field symmetry · **load-bearing [V]**, with an honest graded tolerance

Knock-out: inject an **antisymmetric break** of magnitude κ·‖J‖, sweeping κ. Capacity degrades monotonically with the break:

| κ (asymmetry) | 0.0 | 0.5 | 1.0 | 2.0 | 4.0 |
|---:|---:|---:|---:|---:|---:|
| capacity | 0.867 | 0.700 | 0.500 | 0.100 | **0.000** |

A **strong** break (κ = 4) collapses recall to chance; small breaks are **tolerated** (reported tolerance κ ≈ 1.0). Breaking reciprocity removes the Lyapunov/energy structure that guarantees settling converges to the stored fixed point. The break is the *only* change — the data is still encoded. This is the program's discipline applied honestly: AX2 is load-bearing, **and** its failure is graded, not a cliff — the tolerance is reported rather than hidden. → independent.

### C3 — AX3 coupling nonlinearity · **load-bearing [V]**

Knock-out: replace the sin(Δθ) XY update with a **first-order linear (small-angle) signed-Laplacian consensus flow** — *same* field J, *same* settle budget. Capacity **0.90 → 0.00**; gap 0.90. The linearization removes the discrete phase **wells at {0, π}** that hold distinct patterns, so the corrupted cue is no longer pulled back. (Diagnostic: the settled global R stays *low* ~0.08 — with signed Hebbian weights the linear signed-Laplacian flow does **not** lock onto the stored pattern; it neither recovers it nor drives to a single global phase. The earlier-session overclaim that linear flow "syncs coherently to the wrong answer / R high" was corrected — it **scrambles**, it does not sync.) Only the nonlinearity is removed. → independent.

### C4 — AX4 settling / clock-free relaxation · **load-bearing [V]**

Knock-out: the field is present but **never iterated** (steps = 0). Capacity **1.00 → 0.00**; the read-out equals the **corrupted cue level** (overlap 0.703, `field_inert_without_relaxation = True`). With no relaxation there is no error correction: the stored field *alone* is inert. **Computation is the settling, not the storage** — which also proves AX4 is independent of AX1: you need both the field *and* the dynamics. → independent.

### C5 — AX5 metastable operating band · **load-bearing [V]**

Knock-out: add a **uniform ferromagnetic drive** d that forces global synchrony, sweeping d:

| drive d | 0.0 | 0.5 | 1.0 | 2.0 | 4.0 | 8.0 |
|---:|---:|---:|---:|---:|---:|---:|
| capacity | 0.967 | 0.167 | 0.000 | 0.000 | 0.000 | 0.000 |
| global R | 0.102 | 0.885 | **1.000** | 1.000 | 1.000 | 1.000 |

Forced toward full coherence (R → 1) the global mode **swamps** the stored structure: one global state carries **zero** stored information, and capacity collapses to chance (collapse onset d = 0.5). **Maximal coherence is not optimal** — the band is necessary. (The inherited D3 regime scan already pins the *lower*, field-off edge of the band; this pins the *upper*, over-driven edge.) → independent.

### C6 — verdict: **the axiom set is IRREDUCIBLE [V]**

`load_bearing` is True for all five; `redundant_axioms = []`; `axiom_set_irreducible = True`. Every one of the five operational axioms is load-bearing — each knock-out collapses a core capability that the other (intact) axioms do **not** rescue, sign-stable across seeds, while the intact positive control passes. **No further compression is possible:** the eight inherited invariants compress to a **minimal five-axiom operational core** (B5 deferred), and no axiom in that core is itself redundant.

---

## Two honesty fixes applied this session (recorded, not hidden)

Both changed the digest; both were re-pinned. (1) **C3 reading corrected** — an earlier draft claimed the linear flow "synchronises coherently to the wrong pattern (R high)." The data say the opposite: linear signed-Laplacian flow on signed weights gives **low** R (~0.08); it *scrambles* rather than syncs. The overclaim was removed. (2) **C1 reading tightened** — to distinguish **capacity** (the decision metric, → 0 at every seed) from the **residual ~0.52 overlap** (a non-encoding field is inert — neither recalls nor scrambles), so the residual is not misread as partial success. These are exactly the kind of self-corrections the Stress Principle requires: the collapse is recorded with its honest mechanism, not dressed up.

---

## Inheritance discipline (internalised first, as required)

Before adding the audit, the four inherited things were internalised: **the invariants** (firewall `consciousness_claim=0` / `hard_problem_open=1`; no-tuning `new_tuned_constants=0`; the brain anchor cited as a *principle*, the **number never transferred** — `brain anchors NOT transferred` is asserted in the results); **the derivation identity / core-subset invariance** (the audit imports the *existing* L0 primitives byte-faithfully and only constructs *broken substitutes* alongside them — L0 is never edited); **the register chain** L0→L9 (the audit sits *beside* L0, perturbing nothing in the built stack); and **the source warrant** of every reused primitive (`hebbian_field`, `relax`, `global_R`, `overlap`, `corrupt_phase`, `pattern_to_phase` from frozen L0). The probe is non-circular — the thing perturbed (which axiom is intact) is never the thing read (recovery of an independently-drawn stored pattern). No constant was tuned. The firewall is held byte-for-byte.

---

## L9++ verdict (honestly)

**The inherited premises are not ballast.** The eight inherited invariants compress to **five** independent operational axioms in the frozen substrate (B5 theta-gamma capacity deferred as a higher-layer realization), and an ablation audit — one non-circular probe, generic thresholds, paired and sign-stable across six seeds, gated by a passing intact control — finds **every one of the five load-bearing**: AX1 data-encoded field, AX2 symmetry (with a reported graded asymmetry tolerance), AX3 nonlinearity, AX4 settling, AX5 metastable band. `redundant_axioms = []`, `axiom_set_irreducible = True`. The five-axiom core is **minimal**; there is no further compression. With this, both post-program continuations the program named — (a) compression and (b) hardening — are executed; what remains is optional hardening only (e.g. widening sweeps).

**FIREWALL (unchanged):** auditing which *functional* axioms a *functional* machine stands on is a **FUNCTIONAL** result. The hard problem — felt quality, Gap-5 — remains an **OPEN BLANK, never erased**. `consciousness_claim = 0`, `hard_problem_open = 1`, `new_tuned_constants = 0`.
