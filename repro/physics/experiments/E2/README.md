# E2 — λ–D link test

**Question.** Does the wavelength-free lattice output A = a_med/g* connect two lengths that were measured independently: the light wavelength λ (I₂-HeNe, 632.991 nm) and the grain diameter D = 2λ_C,e (CODATA 2022, 4.8526 pm)? If both the lattice-wave = light identification and the grain size are right, A must equal A_req = 2πλ/D = 8.196×10⁵.

**Protocol.** Pre-registered in `PREREG.json`, which was committed (235a911) before the analysis was run. No new simulation was run. The test re-analyses the existing SOC outputs (N = 200, g₀ = 2×10⁻⁷, original defaults, two seeds, 96 avalanches), whose hashes are pinned. The statistic is the pooled median with an event-level bootstrap 95% interval (10 000 resamples, seed 19). There is no best-avalanche selection.

**Result: PASS** (`RESULT.json`)

| quantity | value |
|---|---|
| A_req (from measured λ, D) | 8.196×10⁵ |
| simulated A, pooled median [95% CI] | 7.79×10⁵ [6.95, 8.53]×10⁵ |
| A_req / median | 1.052 (pull 0.51 half-widths) |
| D predicted from λ | 5.11 pm [4.66, 5.72] vs 4.853 measured |
| λ predicted from D | 602 nm [537, 659] vs 633 measured |

**Reading.**
- The two measured lengths are consistent with a single lattice A within the resolving power of the existing data.
- That resolving power is about ±10% (interval width 20% of the median). This is a consistency at the ~10% level, not a precision confirmation.
- The two seeds differ (8.01 vs 6.90 ×10⁵), so seed-to-seed spread is part of the uncertainty.

**Limits (stated in the registration).**
- Not blind: the run summaries were seen before registering.
- Only two seeds. Replace the event bootstrap with a seed-cluster bootstrap once more independent runs exist.
- The result is conditional on the original N = 200 and g₀ = 2×10⁻⁷ settings. A scales as N^(−1/3)/g₀, and what fixes g₀ physically is still open.

**What this replaces.** This test supersedes, as evidence, two earlier checks that could not fail:
- the 633/532 ratio (λ/D)₆₃₃/(λ/D)₅₃₂, which is arithmetic once D is fixed;
- the RCROSS gate, in which `dt_633` and `dt_532` are the same locked value copied twice (dev = 0).
