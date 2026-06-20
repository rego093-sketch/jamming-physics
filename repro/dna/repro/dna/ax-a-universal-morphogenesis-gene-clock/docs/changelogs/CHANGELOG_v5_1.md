# CHANGELOG — v5.1 (precision backbone)

Built on **v5** (all five gates 5/5) and on **neuro_emergence_chain_integrated
v1.9** governance. This is an **infrastructure / "초정밀" (ultra-precise)**
increment toward the universal-morphogenesis goal: it brings the package up to
neuro v1.9's single-entry, bit-for-bit verification standard.

**Add-only. No engine edits. No fork of `organism/core.py`. All five v5 gates
still PASS 5/5; the unified entry is PASS 7/7.**

## Added

### Single-command verification — `verify_all.py`
Mirrors neuro v1.9's `verify_all.py`. One command verifies the whole package in
three layers (strictest last):

1. **Gate suite** — runs the five existing gates; each must print
   `OVERALL: PASS (5/5)`.
2. **Source integrity** — sha256 of every governed module **and every measured
   input** (the 42-/59-gene γ tables, the Carnegie-stage table, the promoter
   caches) must equal the frozen `expected_sha256.json`, drift 0. This is the
   pin that enforces the standing invariant *"the measured γ stays bit-for-bit,
   never tuned"*, and it catches behaviour-identical edits the gates cannot see.
3. **Fidelity** — the gate-regenerated `results/*_verify.json` must equal the
   frozen `repro/morpho/expected/*.json` leaf-for-leaf (numeric leaves to 1e-9,
   bool/str exact), so cross-session numeric drift is caught even when a single
   run is internally deterministic.

`--freeze` re-records the baseline (and refuses unless the gates pass);
`--list` prints the pinned set.

### Frozen baseline
- `expected_sha256.json` — sha256 pin over the 42 governed source + measured-
  input files.
- `repro/morpho/expected/{gene_clock,morpho_plus,adipose,dev_timing,life_course}_verify.json`
  — the frozen fidelity baseline, recorded from the green 5/5 state.

### Docs
- `REPRODUCE.md` — the one-command verification contract and the deliberate
  re-freeze workflow.

## Falsifiability self-test (recorded, not shipped as a gate)
A behaviour-identical stealth edit (a comment appended to `morpho_core.py`) was
injected: all five behavioural gates and the fidelity layer stayed green, while
**source integrity caught the change and forced `OVERALL: FAIL (6/7)`**; restore
returned `PASS (7/7)`. The pin is non-blind — it adds coverage the behavioural
layer does not have.

## Unchanged / preserved (enforced by the pin)
The engine, the R19 switch, the measured γ tables (42-gene morpho, 59-gene
obesity), the emergence order, the Layer-3 convergence proof, the honest dev-
timing null, and the life-course coupling are all preserved bit-for-bit. The
five v5 gates were re-run and stay 5/5.

## Note on versioning
This is labelled **v5.1** because it is a verification-infrastructure increment,
not a new science deliverable. If it is folded into the planned **v6** work
(HANDOFF NEXT #7: package as a VP-SPEC `repro/dna/15-morphogenesis-full-organism`
chapter and merge into the master DNA package), renumber freely — nothing in the
code depends on the directory name.
