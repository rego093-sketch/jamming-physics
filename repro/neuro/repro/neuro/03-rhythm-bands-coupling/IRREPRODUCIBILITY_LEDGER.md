# IRREPRODUCIBILITY LEDGER — 03-rhythm-bands-coupling (band-ratio gate) (VP-SPEC C3)

This is the ledger for the **minimal in-package gate** `verify_band_ratio.py`, which reproduces
the **one validated quantity** of §03 — the dimensionless count of slow-gamma sub-cycles nested
in a single theta cycle, i.e. the theta-gamma **working-memory span**. It does **not** reproduce
the §03 model+real-data direction (tau_inh sweep, disease tilts, the 17x phase modulation); that
stays in the separate `neuro_extension` lane, disclosed in `README.md`. Per Constitution C3, every
`[O]` quantity below carries a stated obstacle; an `[O]` without an obstacle is a gate FAIL.

**Grades.** `[F]` read from structure · `[V]` verified/reproduced in-package · `[L]` peer-reviewed
(cited, not re-derived) · `[O]` empirically open but **dataset/obstacle-named**.

## The reproducible core (NOT in this ledger because it reproduces)

- **gamma/theta = 6.25, DERIVED — not asserted, not fitted.** Computed in-package as the ratio of
  **geometric-mean band centres**, `geomean(25,50)/geomean(4,8) = sqrt((25·50)/(4·8)) = sqrt(39.0625)`,
  using the package's own non-tuned "centre of a range" (the same construction §14 uses for its
  geometric-mean cell). Bit-for-bit deterministic (2x run -> identical stdout sha256). `[V]`
- **VALIDATED by containment in an INDEPENDENT bound.** `6.25 ∈ Miller [5,9]` (7±2). The band edges
  come from **electrophysiology**; the 7±2 comes from **psychophysics** (memory-span experiments,
  no EEG in them) — two unrelated measurements that **agree**. The agreement is the claim; it is not
  a circular fit, because nothing about the band edges was chosen with Miller's number in view. `[V]`/`[L]`
- **The containment has TEETH (falsifiable).** Broad gamma (30-100 Hz) gives
  `geomean(30,100)/geomean(4,8) = sqrt(93.75) = 9.68`, **outside** [5,9] -> the gate would FAIL.
  So the check **selects** the biologically-correct theta-coupled **slow** gamma (Colgin 2009);
  it does not assume it. `[F]`/`[V]`
- **Input integrity is self-verifying.** The four band edges live in a locked JSON whose
  `payload_sha256` the gate asserts on load; a silent edit trips it even when the tampered ratio
  still happens to land in-window (verified by tamper test). `[V]`
- **The span maps to a discrete item count.** `round(6.25) = 6 ∈ {5..9}` — the dimensionless ratio
  is the number of nested gamma packets, i.e. the working-memory span (Lisman & Jensen 2013). `[F]`/`[L]`

## The open items

| # | `[O]` item | obstacle (why it cannot be derived here) | location |
|---|------------|-------------------------------------------|----------|
| B1 | **absolute theta frequency (Hz)** | The band's absolute frequency is set by the absolute inhibitory time-constant tau_inh, an **external calibration** not in the dimensionless reading. Only the *ratio* is pinned. **Closes with:** a tau_inh measurement (or a direct theta-peak recording). A magnitude on an already-validated ratio. | `band_ratio_properties.json` `theta_band_hz`; §03 chapter `[O]` |
| B2 | **absolute gamma frequency (Hz)** | Same obstacle as B1 — the slow-gamma centre in Hz depends on the absolute inhibitory kinetics. The *band edges* are cited (Colgin 2009) but their placement on the absolute Hz axis is the external calibration. **Closes with:** the same tau_inh / direct-recording route. | `band_ratio_properties.json` `slow_gamma_band_hz`; §03 chapter `[O]` |
| B3 | **theta-phase modulation depth (~17x)** | The chapter's "gamma power ~17x higher at the preferred theta phase" is a **separate** cross-frequency quantity (modulation index), reproduced in the `neuro_extension` lane, **not** by this gate. This gate covers only the *count* ratio. **Closes with:** running the `neuro_extension` `_verify/run_regression.py` (it is already PASS there). Out of scope, not unresolved. | `neuro_extension` lane; §03 chapter prose |

## What is explicitly MEASURED / cited (locked input — so NOT `[O]`)

- **theta band 4-8 Hz** — canonical clinical human theta range (standard oscillation taxonomy;
  Buzsaki & Draguhn 2004). A locked input, not a tuned number. `[L]`
- **slow gamma 25-50 Hz** — the theta-**coupled** gamma component (Colgin et al. 2009, Nature; the
  slow band routes CA3->CA1 storage, while fast gamma 80-140 Hz routes the entorhinal input). The
  choice of the slow band is **biological**, and the gate proves it is load-bearing (broad gamma fails). `[L]`
- **Miller 7±2** — human immediate-memory / channel capacity (Miller 1956). Used only as the
  **independent** containment bound; it is not adjusted. `[L]`
- **count = WM span identity** — Lisman & Jensen 2013 (theta-gamma neural code): the number of gamma
  sub-cycles per theta cycle is the span. Cited mechanism, not re-derived. `[L]`

## Cross-references to sibling reproductions

- **neuro §14 (motor quantification).** Same non-tuned **geometric-mean centre** construction (the
  "geometric-mean cell" threshold) and the same **containment** validation pattern (derive a value,
  validate by containment in a measured range, never fit to the target).
- **neuro §16 (force-length).** The containment-not-`|Δ|=0` validation style originates here (GHJ
  plateau validated by containment, not exact fit); the band-ratio gate applies the identical logic.
- **§03 `neuro_extension` lane.** The full model+real-data §03 reproduction (tau_inh sweep, autism /
  Alzheimer direction, the 17x modulation, OpenNeuro ds004117 / ds004752 reads) lives there and is
  unchanged. This gate is the **in-package dimensionless floor** for the ratio claim only — it does
  not replace that lane, it makes the headline ratio re-checkable from the one package zip alone.
