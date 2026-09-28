#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: code/simulate_proton.py
Description:
    Generate a toy 89-unit proton structure based on an 82+7 jamming-lattice model.
    - 82 "core" units: nearest integer grid points around the origin.
    - 7 "shell" units: a fixed configuration on the R^2 = 8 shell chosen so that
      6 cancel in 3 pairs and 1 survives as the electron seed at [-2, 0, -2].
"""

from pathlib import Path
import json

import numpy as np

# Canonical shell configuration (R^2 = 8)
# Pairs:
#   [0,-2,-2] + [0, 2, 2] = 0
#   [-2,-2,0] + [2, 2, 0] = 0
#   [-2, 2,0] + [2,-2, 0] = 0
# Survivor:
#   [-2, 0,-2]
SHELL_COORDS = [
    [0, -2, -2],
    [0,  2,  2],
    [-2, -2, 0],
    [ 2,  2, 0],
    [-2,  2, 0],
    [ 2, -2, 0],
    [-2,  0, -2],
]


def generate_core_points(n_core: int = 82, r_range: int = 4):
    """
    Generate n_core nearest integer grid points around the origin,
    explicitly excluding the canonical shell coordinates.
    """
    shell_set = {tuple(c) for c in SHELL_COORDS}
    points = []
    for x in range(-r_range, r_range + 1):
        for y in range(-r_range, r_range + 1):
            for z in range(-r_range, r_range + 1):
                coord = (x, y, z)
                if coord in shell_set:
                    continue
                d2 = x * x + y * y + z * z
                points.append({"coord": [x, y, z], "d2": d2})

    # Sort by distance squared (jamming-like packing)
    points.sort(key=lambda p: p["d2"])
    return points[:n_core]


def build_proton_structure():
    core = generate_core_points(n_core=82, r_range=4)
    shell = []
    for c in SHELL_COORDS:
        d2 = int(c[0] ** 2 + c[1] ** 2 + c[2] ** 2)
        shell.append({"coord": c, "d2": d2})
    return core + shell


def save_data(structure, out_path: Path):
    data = {
        "meta": {
            "total_units": len(structure),
            "core_units": 82,
            "shell_units": 7,
            "theory": "82+7 jamming lattice (toy)",
            "description": "Coordinates of sub-quantum units in a proton-like 82+7 structure."
        },
        "units": structure,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[Success] Generated {len(structure)} units. Saved to {out_path}")


def main(root: str | None = None):
    root_path = Path(root or ".").resolve()
    structure = build_proton_structure()
    out_path = root_path / "data" / "proton_89_coords.json"
    save_data(structure, out_path)


if __name__ == "__main__":
    main()
