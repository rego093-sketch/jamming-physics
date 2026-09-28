# Unified DOI Bundle (AQD)

This archive merges three previously separated DOI bundles into a single deposit-ready package.

## Contents

- `00_metadata/`
  - `aqd_constants.json` : canonical numerical constants (single source of truth)
  - `aqd_constants.tex`  : LaTeX macro version of the same constants
- `01_quantum_annihilation/` : extracted from `quantum_annihilation_DOI_vNext_0.1.0(양자유입).zip`
- `02_lattice_percolation_soc/` : extracted from `lattice_percolation_soc_bundle_DOI_v0.2.0_plus_485pm_merged.zip`
- `03_qm_proton_whitepaper/` : extracted from `qm_proton_whitepaper_doi_full.zip`
- `04_vp_whitepaper/` : current working paper (rigor version)

## Policy: Numerical Lock

All modules SHOULD treat the values in `00_metadata/aqd_constants.json` as canonical.
If any module intentionally deviates, it must declare:
- the alternative value
- the reason (Gate/Lock)
- the scope where the alternative is valid

## Images

Per request, all image files (`.png/.jpg/...`) were removed from this merged archive.
If a submodule expects an image for documentation pages, use the included PDFs or regenerate figures from code.

## Checksums

A manifest with SHA256 checksums is provided in `00_metadata/MANIFEST.sha256`.
## Note: Dynamic stiffness closure (Eggshell)

The VP/AQD whitepaper includes a minimal *testable* closure for the jamming–unjamming–healing (“eggshell”) picture: an unjamming trigger (Psi_eff > Psi_y) and a first-order healing ODE for a coarse-grained integrity variable g(t).

## Note: Core-82 coherence additions

The VP/AQD whitepaper also includes two coherence-level (logic-first) additions:
- A radial (volume) integerization + packing-rectification argument that connects the ideal 125-slot volume ratio (n=5) to an effective realised core count near N≈82.
- A tetrahedral-locking (4-point rigidity certificate) gate that must hold before claiming full c^2 stiffness of the 82-core.


## v0.3.0 update (jamming-rotation verification merged)
- `04_vp_whitepaper/vp_whitepaper_v0_3_integrated.tex` — current whitepaper (v0.3.0). Adds §8.5 (steady-state grinder dynamics), §11.6.5 (independent-reproduction [V] table + a reproducibility MAP of the verification scripts), and a §9.4 cross-reference. No locked constant changed (`aqd_constants` unchanged).
- `02_lattice_percolation_soc/jamming_rotation_verification_v0.3/` — 19 verification modules + `FINAL_REPORT.md` + `README_STATUS.md` + `reproduce/`. One-line check: `python3 modules/final_verification.py`. Amplification re-measurement (`verify_amplification_A.py`) reproduces A_median≈8e5 at N=200 from the bundle's own `soc_percolation_pinning`.
- The whitepaper's §11.6.5 contains the script→claim→section map for these modules.
- Note: third-party published reference PDFs (`*/docs/references/*.pdf`) are omitted from this merge for copyright; restore from the master if needed. `00_metadata/MANIFEST.sha256` regenerated; `release_manifest.json` should be rebuilt with the bundle's `make_manifest.py` at release.
