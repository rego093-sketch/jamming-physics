# Irreproducibility Ledger — Vacuum-Inflow Cosmology

VP_SPEC v1.8 · Constitution **C3**. Every quantity or result that this volume does **not** reproduce from first principles within its own scope is collected here, marked `[O]` with a reason and a canonical location. Consistent with the volume's discipline ("present facts in present physics; origins unclaimed; *exhibiting a mechanism ≠ deriving a value*"), every entry is a **gap or a conditional, not a contradiction**. No parameter below is tuned to fit data.

## A. Locked quantities held as input or anchor

Derived from the locked-quantity registry (`tools/cos_locks.json`).

| quantity | mark | why irreproducible (in-scope) | canonical |
|---|---|---|---|
| κ = GM_⊙/Q_⊙ ≈ 3.81×10⁻⁴⁰ (SI) | `[O] input — single absolute anchor` | Fixed by one empirical anchor (the absolute surface-gravity / G normalization, the 'four-wall' problem); the absolute scale is deferred to the physics volume, not derived here. | [canonical derivation §3](https://jamming-physics.org/cosmology/03-gravity-momentum-absorbed-inflow/) |
| κ_opt = H₀/c | `[O] input — open` | Held as a raw input; the mechanism behind its time-evolution is an explicit open question (E-COSMO), deferred to the physics volume §17.5. | [canonical use §7](https://jamming-physics.org/cosmology/07-non-expanding-lattice-optics-cosmology/) |

**Reproducible by cross-volume import (not irreproducible):** νₚ = 3π⁴ ≈ 292.227 s⁻¹; mₚ/mₑ = 6π⁵ ≈ 1836.118. These come from the physics volume with their own DOI and reproduction tree (see `registry/cross_volume_doi.csv`, Appendix D).

## B. Documented open problems and out-of-scope normalizations

Transcribed from the canonical honest-ledger chapter (§16) and `REMAINING_OPEN_PROBLEMS.md`.

| item | mark | status | canonical | repro |
|---|---|---|---|---|
| absolute acoustic length L ≈ 150 Mpc (ℓ ≈ 220) | `[O] empirical normalization` | Mechanism closed without a Big Bang (HYP): one fixed inflow-shell length sets both the BAO real-space peak and the P(k) oscillation spacing, and 2 of 3 success conditions (1:2:3 standing-wave heights, harmless γ-ray dispersion) are met. The remaining condition — deriving the *absolute* 150 Mpc from lattice/inflow constants — stays open: the needed factor ≈28.6 of the Hubble length has no forced π-chain or geometric basis, so it is reclassified as an empirical normalization (same box as BBN, absolute g, absolute 2.725 K) rather than tuned. | [§14·15](https://jamming-physics.org/cosmology/14-cmb-anisotropies-acoustic-scale/) | `repro/cosmology/14-cmb-anisotropies-acoustic-scale/derive_acoustic_length.py` |
| supernova Hubble-diagram fit vs ΛCDM | `[O] data-limited (degenerate)` | The static lattice-optics distance law d_L=(c/H₀)(1+z)ln(1+z) fits the SN Hubble diagram with a single marginalised offset at χ²/dof = 0.50, against 0.44 for ΛCDM (Ω_Λ=0.7); the two laws differ by at most |Δμ| = 0.145 mag. The fit is statistically degenerate with ΛCDM, so present data cannot distinguish them — a data limitation, not a contradiction. No dark-energy term is used. | [§7 (cited §12)](https://jamming-physics.org/cosmology/07-non-expanding-lattice-optics-cosmology/) | `repro/cosmology/07-non-expanding-lattice-optics-cosmology/` |
| absolute CMB temperature 2.725 K | `[O] empirical normalization` | Mechanism closed (a warm present lattice emits thermal radiation = light, §9); the absolute temperature is anchored to the observed radiation density (~80× starlight) and a full energy balance is still required. Out of scope, not contradicted. | [§9](https://jamming-physics.org/cosmology/09-microwave-background-present-lattice-emission/) | — |
| two length scales ratio D/a ≈ 7.7×10⁶ | `[O] input (deferred to physics volume)` | The ratio of the angular scale D = 4.8526 pm to the cell size a = 6.33×10⁻¹⁹ m is an imported absolute scale; its origin is a physics-volume question, left as input here. | [Appendix C](https://jamming-physics.org/cosmology/axc-two-length-scales-d-versus/) | — |
| post-Newtonian second-order coefficient β = 1 | `[O] assumption (degenerate)` | β = 1 is assumed, making the sector fully degenerate with General Relativity at this order; the second-order coefficient is not independently derived. | [§10](https://jamming-physics.org/cosmology/10-post-newtonian-sector/) | — |
| gamma-ray vacuum dispersion | `[O] relaxed, not fully closed` | The sharpest tension of the lattice-light identification; relaxed but not fully closed, and mutually constrained with the acoustic-length program (§1 of the open-problems ledger). | [§2](https://jamming-physics.org/cosmology/02-light-lattice-elastic-wave-sharpest/) | — |

## Summary

- Tier A: **2** locked quantities held as input/anchor (2 further locks are reproducible by import).
- Tier B: **6** documented open problems / empirical normalizations.
- The single largest open item is the **absolute** acoustic length 150 Mpc; its mechanism is closed (Big-Bang-free) and only the absolute value remains an empirical normalization.
- Every item is in-scope-closed at the mechanism level, deferred to the physics volume, out of scope by the volume's own rule, or data-limited — none is a contradiction with observation.
