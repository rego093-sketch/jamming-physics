# Stress Test D — abnormal-input robustness of the locked engines (T4.1)

**Verifies:** that the three locked engines degrade *gracefully* on malformed input
(honest NaN / clean exception) rather than crashing opaquely or silently returning a
content-free-but-plausible result. No engine modified; single-source import + sha256
pin; deterministic (fixed inputs, no RNG); 2×sha256 identical.

## Run
```
cd repro/dna/_verify/stress_abnormal_inputs/
python3 stress_abnormal_inputs.py     # -> stress_abnormal_inputs_results.json
```

## Expected output (deterministic)
`grades = {gamma: GRACEFUL, bulk_contexts: GRACEFUL, run_key: FLAGGED}`. Behavior
matrix over inputs {lowercase, all_N, half_N, single_base, IUPAC_codes, sub_window,
empty} + a valid control.

## Finding (honest grade: robust, with one specific actionable gap)

**No engine is silently wrong.** Across the whole battery, no engine returns a
plausible-but-fabricated number for garbage input. The worst case is a *loud* crash
(detectable), never a quiet wrong answer.

**gamma() — GRACEFUL.** `s = seq.upper()` normalizes case (lowercase == uppercase
exactly), the NN-table comprehension *skips* any dinucleotide not in the table (so
IUPAC codes / Ns are ignored cleanly), and it returns `nan` when no valid
dinucleotide remains (all-N, empty). Featureless valid input (ACGT-repeat,
homopolymer) returns a finite value, which is correct.

**bulk_contexts() — GRACEFUL (with a case-sensitivity note).** Returns finite O/E on
uppercase ACGT input and `nan` on everything it cannot compute (all-N, single-base,
IUPAC, empty). It is **case-sensitive**: lowercase (soft-masked repeat) input returns
`nan`, unlike `gamma()` which upper-cases. Both are graceful (neither emits a wrong
number), but this asymmetry means **soft-masked FASTA must be upper-cased before
methylation calls** or the contexts silently come back NaN.

**run_key() — FLAGGED (one gap).** Featureless valid sequences correctly yield a
minimal result (1 shell / trivial edge anchors) — that is the right answer for a
featureless input, not a bug, so it is **not** graded down. The genuine gap:

- **sub-window input crashes opaquely.** `run_key()` assumes `len(seq) >= W` (2000 bp).
  A 200 bp region — or empty — raises `IndexError: index 2000 is out of bounds`
  instead of a clean `[O]` / `ValueError` ("region shorter than window"). This is loud
  (not silent-wrong) but **ungraceful**: no diagnostic, opaque numpy traceback.

- **content-free all-N is not separately flagged.** all-N returns the same minimal
  1-shell result as a featureless-but-valid sequence. Since that minimal result is
  correct for featureless input, this is not silent-wrong — only a minor
  interpretability note (all-N is indistinguishable from featureless-valid in the
  output), not a grade-down.

## Grade
- gamma, bulk_contexts: **GRACEFUL** — NaN on the uncomputable, never a wrong number.
- run_key: **graceful on featureless valid input; one robustness gap** — opaque
  `IndexError` on sub-window (`len < W=2000`) / empty input where a clean `[O]` is
  expected. Detectable (loud), not silent-wrong.
- Consistency note: upper-case soft-masked (lowercase) FASTA before `bulk_contexts`
  (it returns NaN on lowercase; `gamma` does not need this).

No engine modified. A sub-window guard / case-normalization in `run_key`/`bulk_contexts`
would be a **new version**, not part of this stress test.
