# IRREPRODUCIBILITY LEDGER — DNA paper (v1.9) + Appendix A (gene-clock application)

Constitution **C3**: every `[O]` (open / not reproducible from the package) item names a
**specific obstacle**, and that obstacle is a measured-input or calibration gap that sequence
cannot close — never an invented number. This root ledger aggregates the `[O]` register across
the whole single-file paper and the applied appendix, and points to the per-section ledgers that
hold the detail.

The grade discipline is shared across the paper and the appendix:
**[V]** verified / reproduced in-package (2× sha256) · **[L]** locked, cited, read-only measured
input · **[F]** fixed modelling choice (documented, not measured) · **[O]** open / not earned.

---

## 1. Body §1–§13 (canonical paper)

The chapter `[O]` items are reproduced bit-for-bit where the engine allows and isolated where they
need external data. The authoritative per-section registers are:

- `repro/dna/09-environment-methylation-layer/IRREPRODUCIBILITY_LEDGER.md` — absolute methylation
  level β, absolute age-of-silencing, Layer-2 rate magnitudes κ/λ/h_base, microbiome "training"
  (each `[O]`: a wet-lab / calibration quantity not derivable from sequence).
- `repro/dna/10-…/LEDGER_no_gray_zone.md`, `repro/dna/11-…/LEDGER_cross_kingdom.md`,
  `repro/dna/12-…/LEDGER_clade_readers.md`, `repro/dna/13-…/LEDGER_unified.md` — per-section grades.

Two standing `[O]` themes recur in the body and carry into the appendix:

| `[O]` item | location | obstacle (why not reproducible from the package) |
|---|---|---|
| absolute body/organ **size** (only the *direction* dwell ∝ γ^1.5 is reproduced) | §5 Dwell | absolute size is `dwell × dosage` at runtime; the magnitude needs developmental-rate and dosage measurements the sequence does not contain. |
| anchor-relative `contact_competent` as a **functional** contact claim | §13 helical stress test | the flag is deterministic Layer-1 **geometry** but at **chance** biologically (same-face rate 0.337 vs chance 0.340, z = −0.09); realized looping is Layer-2 (bound factors, cohesin), outside sequence. |

---

## 2. Appendix A — universal_morphogenesis_geneclock (applied volume)

The appendix imports the paper's R19 switch as a single sha256-pinned source and measures every γ by
the identical NCBI→SantaLucia pipeline; its `[V]`/`[L]` machinery reproduces bit-for-bit
(`verify_all.py` PASS 20/20: twelve morpho gates 5/5 + five emergence gates (7/7·6/6·7/7·8/8·8/8) +
a source pin over 87 governed files, drift 0 + twelve morpho fidelity baselines + five emergence
fingerprints, leaf drift 0). Its central scientific result is a **measured null**, and
that null plus the model's structural boundaries are the `[O]` register below. The authoritative
detail is in the appendix's own ledgers (`repro/dna/ax-a-…/LEDGER_*.md`,
`WHY_THE_NULL_AND_MODEL_LIMITS.md`).

| `[O]` item | location (in `repro/dna/ax-a-…/`) | obstacle (the measured input that would close it) |
|---|---|---|
| **DNA → developmental timing** — γ does **not** predict *when* a feature appears (ρ=−0.018, p=0.99 over 7 master features; ρ=−0.414, p=0.36 over 8 organs; ρ=+0.071, exact p=0.882 over the heart's 8 sub-stages) | `code/dev_timing.py`, `organ_timing.py`, `heart_substages.py`; `LEDGER_dev_timing.md`, `LEDGER_heart.md` | timing is a *systemic* quantity; γ is an *intrinsic*, per-gene, cell-invariant scalar (same in every cell), so it can sort relative **order** `[V]` but cannot carry realized timing. A **different measured modality** — expression-onset or chromatin accessibility at the master loci, from an external developmental atlas locked as input — is required. The null is principled, not a defect (see `WHY_THE_NULL_AND_MODEL_LIMITS.md`). |
| **absolute organ / body sizes** (only emergence order + relative dwell are read from γ) | `code/organ_atlas.py`, `organ_anatomy.py`, `morpho_core.py` | absolute scale needs anthropometric / morphometric measurement; the τ window and absolute sizes are display-only `[F]`/`[O]`, the order is `[V]`. |
| **facial bone has no non-adiposity environmental axis** (aging, gravity, sun) | `code/morpho_decomposition.py`; `LEDGER_morpho_decomposition.md` | the bony face is γ-only in the model, so it trivially attributes 100% to DNA for those axes, which real faces do not; needs a *measured* facial-aging / soft-tissue axis as a locked input. |
| **no real morphometric validation** of the shape decomposition | `code/morpho_decomposition.py` | H²=0.51 and the +37% / +25% twin-divergence swing are exact properties of the measured-γ model, **not** fit to paired genotype–morphometry scans (e.g. twin faces/bodies); needs that dataset. |
| **single canonical H²** | `code/morpho_decomposition.py` | heritability is range-dependent **by nature** (0.84 narrow env → 0.10 wide env, a reproduced published fact); collapsing it to one number needs a fixed canonical population environmental distribution as a locked input. Reported as a feature, not hidden. |
| **Layers 2–3 geometry is a principle-demonstration** | `code/anatomy.py`, `body.py`, `assemble.py`, `grow_to_target.py` | the organ shapes, face surface, and growth path are a parametric coarse-to-fine read-out, **not** a continuum tissue-mechanics simulation grown from cells; the genome→morphogen→continuum-mechanics→shape map needs HPC-scale tissue mechanics. The framework's on-thesis Layer-1 content (switch decisions, somite/digit counts) **is** reproduced bit-for-bit `[V]`. |
| one-specifier-per-milestone map (cardiac and organ masters are pleiotropic) | `code/heart_substages.py`, `organ_atlas.py`; `heart_substages.json/_forced_choice_note` | a **forced choice** `[F]`, documented, not a measured assignment; multi-tissue notes (e.g. NKX2-1 lung+thyroid, HHEX liver+forebrain) are recorded, not hidden. |

**What is reproduced bit-for-bit in the appendix (`[V]`/`[L]`):** the one-switch identity
(`max|Δ spinodal| = 2.2e-16` against the body engine and the neural-emergence engine); every measured
γ table (corr(γ,GC)=0.994–0.998), read-only and never fitted; the emergence **order**
`= argsort(spinodal(γ))` and its re-sort under a γ perturbation; the four-target convergence
(RMS→0.05–0.11, Chamfer→0); the variance decomposition H²=0.51 and its population-dependence; the
identical-twin bit-identical core; and determinism (2× sha256 on every gate payload).

---

## 3. Constitutional boundary (restated)

Across the paper and the appendix, **the same scalar γ fixes *what* and in *what order* deterministically
`[V]`, and does not fix *when* or *how big* `[O]`.** That boundary is itself a result of the no-tuning
discipline: every `[O]` above is data-blocked (it names a measured input the package does not contain),
never effort-blocked, and no number anywhere was chosen to hit a target.
