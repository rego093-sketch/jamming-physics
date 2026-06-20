# Reproducing *Felt Cognition* — the emergence engine

This directory (`repro/mind/_engine/`) holds the **in-package emergence engine** for the
mind paper. It is the code that the previous release was missing: every quantitative
claim in `docs/mind/` is now produced **here**, offline, from first principles, so the
reproduction path no longer leaves the package (VP-SPEC **C1**).

## What changed from the old package

The old release shipped only **frozen result JSONs** plus a harness that re-checked their
sha256. The generating code was not included, so the numbers could not be regenerated from
within the package — a C1 reproducibility break. This release **adds the generator** and
makes the package **self-reproducing**:

* `vp_mind_engine.py` — the engine. Nine modules, M0→M8, in developmental order.
* `run_all.py` — runs the engine and **freezes** its output + sha256 digests.
* `../_verify/run_regression.py` — **upgraded** harness: re-emerges live, asserts the
  engine is deterministic and reproduces its own digests bit-for-bit, re-derives every
  mechanism invariant, and still checks the legacy snapshots for provenance.

## Quick start

```bash
# from this directory (repro/mind/_engine)
python3 run_all.py                 # emerge + freeze results/ and expected_sha256.json

# from repro/mind/_verify
python3 run_regression.py          # self-reproduction + mechanism invariants  (exit 0 = PASS)
```

Both are pure-Python + NumPy, offline, single-threaded (BLAS threads are pinned to 1 inside
the engine so the digest is portable), fixed `SEED = 19`.

## The modules (and what each one *emerges*)

| Module | Emerges | Physical substrate |
|---|---|---|
| **M0** | brain organs from 4D-DNA | each organ's master gene sets an R19 bistable γ (FOXG1 cerebrum, EN1 cerebellum, SIM1 hypothalamus, LHX2 hippocampus); developmental **order** = ascending functional spinodal |
| **M1** | the EM **brainwave** | excitatory/inhibitory populations → a local field potential; θ (slow inhibition) and γ (fast inhibition) bands; the γ field is then **radiated** by the driven wave equation `u_tt = c²∇²u + f` and its front is measured to travel at **~c** |
| **M2** | **hippocampal memory** | engram cells are R19 bistables; **write** = Hebbian outer-product (deepens an attractor); **retrieve** = pattern completion from a partial cue; **θ-phase** write/retrieve separation **protects** stored memories from new-learning interference |
| **M3** | parallel γ micro-eddies | γ → ignitability (monotone, r≈1); lateral inhibition gives **winner-take-MOST** (losers retained under soft inhibition, killed under hard) |
| **M4** | basal-ganglia selection | Go/NoGo selects **exactly one** eddy; a sub-threshold control selects **none**; γ predicts the selection delay |
| **M5** | the learned field | a dopamine **reward-prediction error** updates which eddies are laid down next — the system learns *what to think* |
| **M6** | the **stream of thought** | serial selection chained through associative memory (a heteroassociative replay trajectory is autocorrelated; an independent control is not); conflict slows near-ties; contents are bound within one **θ frame** — the emerged brainwave, not an abstract phase |
| **M7** | the embodied loop / open problem | arousal (hypothalamic setpoint) couples to recall; hemispheric asymmetry is **graded**; the access marker (PCI) is an **HONEST NEGATIVE** — consciousness is not reproduced; the hard problem is **OPEN** |
| **M8** | **coherence of the emitted field at brain scale** | solves the classical field across a brain-sized transect (exact lossy-medium Maxwell wavenumber + an independent numerical solve, swept 1–100 Hz): coherence across the brain **≈0.998** (brain ~10⁻⁴ of a wavelength; skin depth >600× the brain). The coherence-length rejection imported the **quantum** ~10⁹× number for a **classical** field — a category error. Whether the field is the binding **medium** stays **OPEN** (field strength / ephaptic efficacy is *not* emerged) |

Run order and assembly live in `emerge_all()`.

## Honest grading (VP-SPEC F / V / O)

* **[V] verified, reproduced here:** the *mechanisms* — winner-take-most, γ→ignitability
  monotonicity, single-winner selection, RPE learning, a self-sustaining attractor memory
  with cue-completion and θ-phase interference protection, and that the radiated brainwave
  front travels at the wave speed *c*.
* **[F] forced by the substrate:** the developmental **ordering** of the organs (set by the
  measured γ → spinodal), and the qualitative band split θ < γ.
* **[O] open / not reproduced at scale:**
  * **Absolute physical units** (Hz, μV, ms, radiated **power** in watts). The engine works
    in the dimensionless R19/FHN time and a normalized field; mapping to SI requires the
    membrane RC, channel densities, and a full antenna calculation. The neuro chain already
    grades EM **power** as `[O]` (the source radiates — existence is `[V]` — but its antenna
    efficiency is unresolved); the mind paper inherits that obstacle and does not re-derive it.
  * **Whole-brain scale.** A literal cerebrum is ~10¹⁰ neurons with metre-long axons, solved
    against full Maxwell in a heterogeneous head — an HPC-scale computation. Per C3 this is
    **simplified to a tractable population** here; the *mechanism* is what is asserted, not
    the cell count. The simplification is declared, not hidden.
  * **Consciousness.** No marker of experience is produced. M7 reports an **honest negative**;
    the functional stream is specified, the *quale* is not. The hard problem is **deferred**.

## Determinism notes

* BLAS/OpenMP thread counts are pinned to 1 **before** NumPy is imported, inside the engine.
* All floats are rounded with a fixed precision (`_round`, 10 decimals) before hashing, so
  `sha256_of()` is portable across machines that agree on the mathematics.
* `expected_sha256.json` is regenerated by `run_all.py`; the verifier checks the live run
  against it. If you change the engine, re-run `run_all.py` to refreeze.

## Provenance of the measured γ

`_engine/data/brain_organ_gamma.json` vendors the four organ master-gene γ values used by
M0. They are **measured** (SantaLucia-1998 nearest-neighbour metric on the master-gene
sequence), read-only, and carried from the neuro chain's `_engine/data/`. They are never
fitted to the results here.
