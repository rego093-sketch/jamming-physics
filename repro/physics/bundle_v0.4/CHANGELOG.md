# v0.4.0 (jamming spine verification merged; physical foundation: assertion -> verified)
- Merged the 2026-06-05 jamming-spine reproducibility set (6 modules) under
  `02_lattice_percolation_soc/jamming_spine_verification_v0.4_2026-06-05/`:
  01 stiffness_to_c2 (direct bulk modulus B; c^2=B/rho), 02 shear_relaxedG (relaxed shear
  modulus G->0 at the isostatic point z=2d=6 along FIVE independent observables — closes the
  previously-open "single compression speed c^2=B/rho" demonstration), 03 forced_circle
  (proton radius r_p=(2/pi)*lambda_Cp as a globally stable attractor, F'(x*)=-(pi/2)^5),
  04 rotating_grinder (self-limited ~82-cell core; x*~1/Omega), 05 light_emergence (D=2*pi*lambda/A),
  06 constants_scales_geometry (alpha,delta,2pi; integer core 81=3^4; proton/quantum scale split).
- Added JAMMING_VERIFICATION_INDEX.md (canonical module per result; v0.3 vs v0.4 provenance).
- Deduplicated: removed AQD-origin copies under 05_.../deps/ (pointer README to canonical legacy_bundle).
- v0.3 jamming_rotation_verification retained (N=750 amplification-A run is canonical there).
- No locked constant changed. New content is [V] (verification) only.

# v0.3.0 (jamming-rotation verification merged)
- Added §8.5 grinder dynamics (incl. §8.5.0 rotational-unjamming: the geometric reason rotation breaks jamming = origin of the §6.2 inflow) + §11.6.5 reproduction table & map to the whitepaper; merged 19 verification modules under 02_lattice_percolation_soc/jamming_rotation_verification_v0.3/. No locked constant changed. Third-party reference PDFs omitted (copyright).

# Changelog

All notable changes to this unified DOI bundle are documented here.

## v0.2.6 (reproducibility patches)

### 2025-12-14
- Added top-level reproducibility scaffold required by the VP whitepaper:
  - `registry/`, `derived/`, `gate/`, `snapshot/`, `scripts/` (SSOT + sealing)
- Added DOI-pack style release scaffold (whitepaper §16.3.3):
  - `protocol/`, `locks/`, `plans/`, `runs/`, `ref_impl/`
  - `release_manifest.json`, `release_manifest.sha256`, `DOI_MAP.csv`
- Made core reproducibility scripts deterministic by using `registry/protocol_lock.json::created`
  instead of wall-clock dates.
- Added `exp10/` package skeleton (whitepaper §10.4) including configs, inputs, scripts, outputs, and
  `exp10/snapshot/` sealing.
- Added Core-82 storage artifacts at bundle root (whitepaper §8.1.9):
  - `X82.csv`, `G82.edgelist`, `layers82.csv`, `params82.yaml`.
