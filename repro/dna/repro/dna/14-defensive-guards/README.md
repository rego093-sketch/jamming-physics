# Chapter 14 — Defensive guards (new-version wrapper layer)

Implements the three modest defensive measures the v1.9 second-session stress
battery showed were needed, **without modifying any locked engine**. The locked
grammar (γ, NN table, A4 pipeline, methylation engine, all thresholds, frozen
`expected/`) stays byte-identical (**152/153**; the one diff is the appended
`LEDGER_unified.md` documentation). Guards **wrap** the locked engines, imported
single-source and **sha256-pinned**.

"Perfection" here is explicitly **not** zero-exception — it is: stop the
*demonstrated* failures and stay honest at the edges, with a small documented
residual risk.

## Run
```
cd repro/dna/14-defensive-guards/
python3 stress_guards.py        # -> stress_guards_results.json   (OVERALL_PASS = True)
```
`guards.py` is the importable layer: `detect_regime_safe`, `run_key_safe`,
`bulk_contexts_safe` (+ `*_raw` originals exposed for side-by-side checks).

## The three guards (each tied to a stress finding)

| Guard | Fixes | Mechanism | Locked engine |
|---|---|---|---|
| `detect_regime_safe` | Test C false positive (extreme-AT → PLANT) | below `GC_FLOOR=0.25`, the CpG/CpHpG-depletion→regime inference is **not trusted**: call is overridden to `no_global` and flagged `low_GC_composition_confounded`; the raw call is preserved, never hidden. NaN contexts → explicit `[O]_insufficient_sequence`. | `detect_regime` / `bulk_contexts` (unchanged) |
| `run_key_safe` | Test D opaque crash (`len < W`) | length pre-check; returns a clean `[O]` dict naming the closing condition instead of the engine's opaque `IndexError`. | `run_key` (unchanged) |
| `bulk_contexts_safe` | Test D case-sensitivity (soft-masked lowercase → NaN) | upper-cases before the locked call so soft-masked FASTA reads correctly. | `bulk_contexts` (unchanged) |

### Why `GC_FLOOR = 0.25` (empirical, from Test C)
- misclassified: Plasmodium 20.4 %, Dictyostelium 22.3 % (both < 23 %)
- knife-edge correct: Tetrahymena 23.5 %
- lowest correctly-classified **real methylator**: tomato 30.9 %

0.25 sits in the clean (22.3 %, 30.9 %) gap with a ~5.9-pt margin to the nearest
real methylator, so **no known global methylator is suppressed**, while both
demonstrated false positives are caught and the knife-edge case is flagged.

## Stress-test result — `OVERALL_PASS = True`

**Part 1 — methylation false positive fixed, zero regression.** Across all 19
organisms (12 panel + 7 adversarial), raw **17/19** → guarded **19/19**. The guard
changes exactly two calls: Plasmodium and Dictyostelium flip `PLANT → no_global`
(both biologically correct: no global 5mC) with the `low_GC_composition_confounded`
flag. Every organism correct under the raw engine stays correct — **0 regressions**.

**Part 2 — run_key no longer crashes.** The raw engine still raises `IndexError`
on a 200 bp input (gap confirmed); `run_key_safe` returns a clean `[O]` ("region
length 200 bp < window W=2000 bp …") on both 200 bp and empty input, and is a
**pass-through identical to the raw engine on a normal (> W) region** (same shells,
same anchors) — the guard adds nothing on valid input.

**Part 3 — soft-masked FASTA reads correctly.** The raw engine returns NaN on
lowercase (gap confirmed); `bulk_contexts_safe` on lowercase now **equals** the raw
engine on uppercase (CpG O/E 0.7205 == 0.7205). All-N input → explicit
`[O]_insufficient_sequence`, so "couldn't compute" is never silently read as
"no methylation".

Deterministic (fixed inputs, no RNG); 2×sha256 identical.

## Residual risk (declared, not zero by design)
A hypothetical genome with **GC < 25 % AND genuine global 5mC** would be wrongly
down-graded to `no_global` by `detect_regime_safe`. No such organism is known —
extreme-AT genomes characteristically lack global 5mC — so the guard trades that
theoretical case for fixing the demonstrated error. The raw call is always kept in
`raw_regime`, so the override is fully auditable and reversible per locus.

## Status vs the locked book
These guards are the **new-version** work the §13 LEDGER had flagged as deferred.
They do not alter chapters 1–13, do not change any threshold inside the engines,
and retire no claim. To adopt them as canonical, a caller imports
`14-defensive-guards/guards.py` instead of calling the raw engines directly.
