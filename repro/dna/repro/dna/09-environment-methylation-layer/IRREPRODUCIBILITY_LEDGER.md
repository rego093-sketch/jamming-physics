# IRREPRODUCIBILITY LEDGER — environment-methylation-layer (v1.9, Workstream A)

Constitution **C3**: every `[O]` item states a specific obstacle. This case keeps the
material γ and the CpG substrate `[F]` (measured, reproduced bit-for-bit) and isolates the
non-reproducible quantities below. None is invented; each is a calibration/external-data
gap that sequence cannot close.

| `[O]` item | location | obstacle (why not reproducible from the package) |
|---|---|---|
| absolute methylation level (β) | `m_layer`, `hysteresis` | β is a wet-lab measurement (WGBS / 450K array) per tissue·age·condition. It is **not derivable from sequence** — the sequence gives the *substrate* (CpG positions, `[F]`), not the *state*. Requires external epigenome data (ENCODE / Roadmap / GEO). |
| absolute age-of-silencing | `m_layer.flip_age_OPEN` | the flip *exists and is discontinuous* (`[F]`), but the *age* at which it occurs is a calibration onto the rate magnitudes, not a derivation. The printed "~age 19" is illustrative. |
| rate magnitudes κ, λ, h_base | `knobs_layer2` | κ (age-methylation rate, set by genotype), λ (methylation→drive coupling), and h_base (infancy drive) are **Layer-2 illustrative knobs** carrying the documented *direction* only (non-persistence κ > persistence κ; methylation lowers drive). Their numeric values are not measured. |
| lactose-tolerance "training" | `hysteresis.scope_note` | the improved tolerance from regular dairy is **dominantly colonic-microbiome adaptation + physiological tolerance**, a layer **above** the DNA switch. It is **outside this model** by construction — the model represents only the DNA-methylation component (which is hysteretic: lactase is not re-induced). |

**What is reproduced bit-for-bit (`[F]`, in `expected/`):** the measured γ of LCT
(human/mouse) and the MCM6 enhancer; the same-material check `|Δγ|=0.034`; the CpG O/E mean
and local-max (the methylation substrate); the discontinuous R19 flip; and the hysteresis
verdict. Two consecutive engine runs are sha256-identical.

**Honest boundary restated:** this is a principle-demonstration of a *mechanism class* —
that an environment-sensitive trait's switch carries a methylation substrate readable from
structure, tuned in a stateable direction — **not** a clinical or quantitative prediction of
lactase status.

---

## v1.9 stress addendum — bounds found by the stress battery (Workstream: stress + guards)

The stress battery (chapters 02/12/13/14, `stress_*/`) added the following bounded /
`[O]` items. Each is deterministic (2×sha256) and names its obstacle per C3. None alters
the locked grammar (γ, NN table, A4 pipeline, methylation engine, frozen `expected/` all
byte-identical); corrections live in the chapter-14 guard wrapper.

| `[O]` / bounded item | location | obstacle (why the claim is bounded, not closeable from sequence) |
|---|---|---|
| auto-detector regime call below ~25% GC | `12.../stress_detector_adversarial`, `14.../stress_guard_validation` | extreme-AT genomes carry real CpG/CpHpG depletion from composition (AT-biased mutation, codon usage), **not** methylation — so the depletion→regime inference false-positives PLANT. Proven by matched-composition nulls (shuffle/iid return CHG O/E ~0.99). Not closeable from sequence alone; needs independent methylation evidence (WGBS). Guarded (`detect_regime_safe`, floor 0.25). |
| γ-beyond-GC → CpG-O/E coupling at GC extremes | `02.../stress_gamma_vs_gc` | the small (~1%) structured dinucleotide residual of γ couples to CpG O/E in the normal GC band (partial-corr 0.572) but **inverts at GC ≈ 20%** (Plasmodium, TA-driven). The "two projections of one history" link is GC-domain-limited; not a universal identity. |
| A4 anchor **count** (not position) | `13.../stress_coordinate_stability` | anchor *positions* recur (93% within 2 kb across settings/crops, `[F]`), but anchor *inventory/count* is set by `min_shell_bp` resolution, not absolute. Reported anchor counts are resolution-relative, not a closed quantity. |
| `run_key` on sub-window input (`len < W=2000`) | `_verify/stress_abnormal_inputs` | the locked engine raises an opaque `IndexError` (not silently wrong). Guarded (`run_key_safe` returns a clean `[O]` naming the closing condition). A fix in the locked engine would be a new version. |

**Declared residual risk (chapter-14 guard, not zero by design):** a hypothetical genome
with GC < 25% **and** genuine global 5mC would be wrongly down-graded by `detect_regime_safe`.
None known across 3 independent extreme-AT non-methylators caught (Plasmodium, Dictyostelium,
Entamoeba) and 6 real methylators all ≥ 31.6% GC; the raw call is always retained for audit.
