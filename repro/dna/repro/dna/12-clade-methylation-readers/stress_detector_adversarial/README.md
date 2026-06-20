# Stress Test C — methylation auto-detector, adversarial / out-of-panel (T2.3)

**Verifies:** whether `detect_regime()` (the 4-regime methylation auto-detector
frozen in `clade_reader_engine.py`) generalizes beyond the 12-organism panel, and
where it misclassifies. **No threshold is changed** (probe only; a threshold change
would be a new version). Single-source engine import + sha256 pin; seed=19; 2×sha256
identical.

## Run
```
cd repro/dna/12-clade-methylation-readers/stress_detector_adversarial/
python3 stress_detector_adversarial.py     # -> stress_detector_adversarial_results.json
```
Inputs: 7 frozen 120 kb RefSeq regions (`inputs/*.fa` + `_provenance.json` with
accession/region/sha256). Re-uses the 12 panel regions (read-only) for re-check.

## Expected output (deterministic)
- `summary.correct = 4`, `misclassified = 1`, `out_of_category = 2` (adversarial set).
- Within-class generalization **CORRECT 3/3**: tomato→PLANT, cow→VERTEBRATE, dog→VERTEBRATE.
- Composition false-positive: dictyostelium **MISCLASSIFIED** (→PLANT), tetrahymena CORRECT (escapes by a hair).
- Panel re-check: **11/12 correct**, `plasmodium` **MISCLASSIFIED** (latent panel error).
- Nulls: for all AT-rich organisms, iid-random & mono-shuffle return CHG O/E ≈ 0.99 and **no** methylation class.

## Finding (honest grade: REFINED — generalizes within regimes; characterized false-positive boundary at GC ≲ 23%)

**1. Within-regime generalization is robust (strength).** Fed unseen species, the
detector lands every one in its correct trained class: tomato → `PLANT_global_CG_CHG_CHH`,
cow & dog → `VERTEBRATE_global_CG`. The CG/CHG/CHH thresholds transfer across species
within the plant and vertebrate regimes they were tuned on.

**2. Out-of-category biology is handled honestly ([O], not forced).** Neurospora
(fungal RIP/targeted 5mC; CG O/E 0.862) and oyster (mollusk gene-body mosaic; CG O/E
0.824) both return `no_global_methylation_pergene_unknown`. No fungal / invertebrate-
gene-body class exists, and a random euchromatic region shows no *global* depletion,
so the honest "no global signal, per-gene unknown (needs annotations)" is the right
[O]. The detector does not fabricate a class.

**3. Characterized false-positive boundary at GC ≲ 23% (the overclaim).** Two
genomes are **misclassified as PLANT** despite having **no global 5mC** (6mA/ trace
only): Plasmodium (GC 20.4%, CHG O/E 0.878) and Dictyostelium (GC 22.3%, CHG O/E
0.938). Tetrahymena (GC 23.5%, CHG O/E 0.9959) sits exactly on the knife edge and
escapes by 0.004 O/E. The `T_PLANT_CHG = 0.96` boundary is being crossed by AT-rich
genomes that carry **real CpG/CpHpG depletion from non-methylation causes** (AT-biased
mutational pressure, codon usage), which the detector reads as an RdDM methylation
fingerprint.

**Mechanistic null proves it is structure, not estimator bias, and not methylation.**
For every AT-rich organism, both nulls collapse the signal:
| organism | obs CHG O/E | iid-random CHG O/E | mono-shuffle CHG O/E | null calls methylation? |
|----------|-----------:|-------------------:|---------------------:|:-----------------------:|
| plasmodium    | 0.878 | 0.991 | 0.988 | no (40/40 no_global) |
| dictyostelium | 0.938 | 0.987 | 0.994 | no (40/40 no_global) |
| tetrahymena   | 0.996 | 0.991 | 0.991 | no (40/40 no_global) |

- iid-random at matched GD≈22% returns CHG O/E ≈ 0.99, **not** < 0.96 → the O/E
  estimator is **not** biased low at extreme GC (rules out a pure composition artifact).
- mono-shuffle (exact base composition, structure destroyed) also returns ≈ 0.99 →
  the observed depletion is **real di/tri-nucleotide sequence structure**, present in
  the genome but absent after shuffling.
- These organisms have no global 5mC, so that real depletion is **not methylation** —
  it is AT-rich compositional/codon avoidance the detector cannot distinguish from an
  RdDM fingerprint.

**Convergence with Test A.** Test A (γ-beyond-GC residual) independently found that at
GC ≈ 20% (Plasmodium) the CpG-O/E-as-methylation mapping **inverts** and CpG O/E
becomes uninformative. Test C shows the *same* GC≈20–23% region is exactly where the
methylation auto-detector false-positives. Two independent reads place the boundary of
"CpG depletion ⇒ methylation" at GC ≲ ~23%.

## Grade
- Within-regime generalization (plants, mammals): **ROBUST** — unseen species classify correctly.
- Out-of-category handling (fungal, invertebrate gene-body): **HONEST [O]** — declines rather than mis-forcing.
- Global validity: **bounded** — the detector carries an uncharacterized false-positive
  mode at **GC ≲ ~23%**, where non-methylation AT-rich di/tri-nucleotide depletion is
  misread as PLANT/RdDM. Affects **2 of 19** organisms tested (Plasmodium, Dictyostelium),
  both AT-extreme; Tetrahymena is a knife-edge pass. The auto-detector's
  "depletion ⇒ methylation regime" inference should be qualified as **unreliable for
  extreme-AT genomes (GC ≲ 23%) absent independent methylation evidence**; default to
  `no_global` / `[O]` there.
- **Latent panel error surfaced:** the v1.9 panel's Plasmodium call
  (`PLANT_global_CG_CHG_CHH`) is itself a false positive of this mode.

No threshold changed. Threshold re-tuning (e.g. a GC-conditioned `T_PLANT_CHG`, or a
GC ≲ 23% guard) would be a **new version**, not part of this stress test.
