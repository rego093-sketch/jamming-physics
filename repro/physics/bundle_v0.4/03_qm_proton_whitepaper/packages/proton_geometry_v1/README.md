# Nucleon Geometry & Electron Genesis Simulation Data
**DOI (placeholder):** 10.xxxx/proton-geometry-v1  
**Author:** Institute of Grid Space Physics (IGSP)  
**Date:** 2025-05-20

## Overview

This bundle implements the minimal reproducible package described in the
proton–electron electromagnetic–origin whitepaper (“82+7 jamming lattice” model).
It contains a toy but fully deterministic simulation pipeline that:

1. Builds an 82‑core + 7‑shell nucleon configuration (proton = 89 sub‑units).
2. Verifies that the 7 shell units split into 3 cancelling vibration pairs + 1 survivor.
3. Confirms that the survivor vector `[-2, 0, -2]` has a 135° ejection angle from the spin axis.
4. Demonstrates the 3‑sector integerization (82 → 28+27+27, 89 → 30+30+29) and maps the
   proton imbalance to a canonical 23.48° axial tilt (Earth‑like obliquity).

This is a *minimal* DOI‑style bundle for the proton geometry layer. It does **not** yet
include the full quantum_annihilation_DOI_vNext structure; that can be added as a higher‑
level package once the time‑standard (electron‑second) layer is fully coded.

## Directory Structure

- `code/`  – Python simulation scripts (packing + vector analysis).
- `data/`  – Generated coordinates of the 89 units (JSON).
- `results/` – Human‑readable report with all key derived angles.
- `docs/`  – Source whitepaper material (as provided by the author).
- `scripts/` – Utility tools (currently only manifest generator).
- `MANIFEST.sha256` – Hashes of all files in this archive (integrity check).

## Reproduction Recipe (local run)

Requirements: Python 3.8+ and NumPy installed in the active environment.

```bash
cd proton_geometry_v1_reproducibility

# (optional) create env and install numpy
# python -m venv .venv && source .venv/bin/activate
# pip install -r requirements.txt

# Step 1: generate the 89‑unit structure (82 core + 7 shell)
python code/simulate_proton.py

# Step 2: analyze shell dynamics and write the report
python code/analyze_vectors.py

# Step 3 (optional but recommended for DOI): update integrity manifest
python scripts/make_manifest_sha256.py
```

After Step 2, you should see:

- `data/proton_89_coords.json`
- `results/simulation_log.txt`

`simulation_log.txt` is the canonical report that can be cited as
“geometrically verified by simulation” in the whitepaper.

## Notes

- No Standard‑Model field equations are used here; this is a pure geometric /
  combinatorial toy model matched to observed constants only through
  comparison of *results* (e.g. proton radius, Earth obliquity).
- Hydrodynamic length‑selection and δ=1/π², α=2/π enter only through the
  separate hydrodynamic proton‑radius paper and the electron‑second whitepaper,
  which can be referenced from a higher‑level DOI bundle.
