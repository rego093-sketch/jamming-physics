# CHANGELOG — Phase 7 + continuation handover

## Phase 7 (this session): trajectory λ-band [F] → [L]-grounded cross-validation, add-only

**Goal (Phase-5 menu, Option 3 — "continuum trajectory [F] → measurement comparison"):** take the
one **unverified qualitative line** in the Phase-3 trajectory ledger — that the DB's D-range maps to
`λ ∈ [19, 190] µm`, *"bracketing real morphogen gradients (Bicoid/FGF/Nodal/Shh)"* — and turn it
into a **gated, falsifiable measurement test**, with zero tuning and zero modification of any pinned
file.

**Outcome: achieved.** A first-principles length band, derived **purely** from `param_db` biophysics
(`D ∈ [0.1,10] µm²/s`, `τ ≈ 60 min` → `λ = √(D·τ)`, band `[18.97, 189.74] µm`, central 60 µm),
brackets six directly-measured morphogen gradient decay lengths from primary literature:
geom-mean(measured) = 31.41 µm vs central 60 µm → **factor 1.91** (< 3), **5/6 in band**, and the
strictly **independent** subset (Bicoid/Nodal/Shh, whose studies did not set the DB) is **3/3 in
band** → promoted **[F] → [L]-grounded**. Gate `verify_emergence_morphogen.py` → **8/8 PASS**.

### Files ADDED (all new; nothing pinned was touched)
- `morphogen_lengths.json` — locked, INDEPENDENTLY-MEASURED gradient decay lengths for 6 morphogens
  (Bicoid 100, Nodal 80, Fgf8 50, Dpp 20, Shh 20, Wingless 6 µm), each with system + primary-source
  provenance + `informs_db` independence flag + pre-registered inclusion rule + independence note +
  honesty note. Read **only** by the gate (the engine never reads it). Separate file so no existing
  `param_db*.json` sha256 changes.
- `emergence_morphogen_validation.py` — engine: derives the band `λ = √(D·τ)` **purely** from
  `param_db.json`; `model_band()`, `contains()`, `result_hash()`; never reads any target file;
  determinism sha `4ea1c7b4111c`.
- `verify_emergence_morphogen.py` — gate: 8 checks (DB-SOURCED · NON-FIT · DETERMINISM ·
  MEASURED-INPUT INTEGRITY · REGIME AGREEMENT · INDEPENDENT-SET · NON-BLIND · ROBUSTNESS ±30%) →
  8/8 PASS, validation sha `01b0b6ea8b10`.
- `LEDGER_morphogen_length.md` — grade-of-record: the [F]→[L]-grounded promotion, the measured-target
  table, the pre-registration + independence (non-circularity) guard, the honest Wingless band-miss.

### Wired in (add-only, one line)
`verify_all.py` `EMERGENCE_GATES` gains
`("emergence_v2/verify_emergence_morphogen", "emergence_morphogen")` — the **only** edit to a
non-pinned root file. OVERALL rises **19/19 → 20/20** (+1 check).

### Re-pin / baseline (drift 0 on everything prior)
- `expected_sha256.json` pins **84 → 87** files (+1 measured-input json, +2 code); the existing 84
  pins are **byte-identical** (changed 0, removed 0).
- `emergence_gate_baseline.json` freezes **4 → 5** gates: added
  `emergence_morphogen = {counts: "8/8", shas: ["01b0b6ea8b10", "4ea1c7b4111c"]}`; the existing four
  (`emergence_heart 939ae9924a6c`, `emergence_organs 40225433a67a`,
  `emergence_organs_wide d82eeb925973`, `emergence_trajectory b2b34a770f5a`) are **unchanged**.
- All **12 morpho fidelity baselines** kept byte-for-byte.

### Freeze method (honest disclosure)
The full `verify_all.py` cannot complete in one process within the runtime budget (the
`dev_timing_wide` gate alone is ~261 s). The baseline was therefore frozen **decomposed**: every gate
(12 morpho + 5 emergence) was run **individually to completion**, its `(rc, stdout)` cached, and the
canonical `freeze()` was driven against that cache (each gate is deterministic, so cached output is
byte-identical to an inline run; the resulting pins are identical to a literal `--freeze`). Drift-0
was then re-confirmed against a pre-freeze snapshot of `expected_sha256.json`: the 84 prior pins
unchanged, exactly the 3 new files added, and the morphogen fingerprint regenerated independently
matches the frozen baseline.

### Reproduce
```
cd code/emergence_v2
python3 emergence_morphogen_validation.py     # engine, band [18.97,189.74] central 60, sha 4ea1c7b4111c
python3 verify_emergence_morphogen.py         # gate, 8/8 PASS, [L]-grounded, sha 01b0b6ea8b10
```

### Discipline honored
NON-FIT (engine never reads the measured gradients; band target-invariant) · grade==evidence
(per-morphogen membership stays [F]; realized form stays [O]) · add-only (no pinned file changed;
four prior emergence baselines + 12 morpho fidelity baselines byte-identical) · no fabrication (every
λ, D, τ primary-source cited) · no back-fit (band fixed from generic biophysics, independent of the
gradients tested; the **independent set** Bicoid/Nodal/Shh makes the test strictly non-circular) ·
honest residual (Wingless ~6 µm named as a band miss, not excluded).

---

## Continuation handover — what remains, and why

**Completed-now (this session), see `DISCOVERY_AUDIT_phase7.md`:** the trajectory λ-band measurement
comparison (Option 3) is the last *completable-without-new-data* science item on the open menu. With
it done, the remaining roadmap items are **data-blocked by design**, not by effort:

- **Timing modality (expression-onset / chromatin ATAC atlas)** — the only lever to flip the
  DNA-vs-organ-timing NULL [O] to a positive needs a measured onset/accessibility atlas that does not
  exist in-package; **fabricating it is forbidden**. Remains [O], data-blocked.
- **Second crisp single-organ timing test (limb / neural tube)** — fetchable via NCBI but expected to
  return the same NULL [O] (gamma is orthogonal to timing, established on the heart, the gold-standard
  system); a confirmatory null, not a new result. Optional.
- **Per-organ measured shape priors** (real ellipsoid geometry in `organ_anatomy.py`) — would require
  editing a **pinned engine** (forbidden) **and** measured per-organ morphometrics. Data-blocked.
- **Facial-bone aging axis / single canonical H²** (PROJECT_SUMMARY open slots) — each needs a
  measured longitudinal or population dataset not in-package. Data-blocked.

**The data-blocked boundary is itself the result** (PROJECT_SUMMARY): under C3 no-tuning, the line
between "promoted with provenance" and "left [O]" is drawn by *what has been independently measured*,
never by tuning to close a gap.

**Option 4 — `dna_vp` main-body narrative merge:** documentation-only; the integrated emergence law
+ the new [L]-grounded length cross-check can be folded into the main whitepaper narrative in a future
pass. Carries no new science and no pin risk; recorded as a deliberate separate step.
