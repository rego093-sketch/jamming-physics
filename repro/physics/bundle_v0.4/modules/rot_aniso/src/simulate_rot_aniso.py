#!/usr/bin/env python3
"""Deterministic reference runner for the rot_aniso module.

Usage:
  python modules/rot_aniso/src/simulate_rot_aniso.py --protocol modules/rot_aniso/protocol.yaml --out runs/rot_aniso_<id>

This runner is intentionally lightweight. It is meant to:
- demonstrate deterministic metrics + Gate evaluation
- generate schema-conforming artifacts
- avoid external data dependencies

It does NOT constitute experimental validation.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

# Allow running this file directly (without installing as a package).
import sys
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from estimators import compute_metrics, to_json
from gates import run_all_gates
from io_schema import append_jsonl, build_manifest, sha256_file, write_json



# ------------------------------
# Deterministic RNG: splitmix64 + xorshift128+
# ------------------------------

def _uint64(x: int) -> int:
    return x & 0xFFFFFFFFFFFFFFFF


def splitmix64(seed: int) -> int:
    z = _uint64(seed + 0x9E3779B97F4A7C15)
    z = _uint64((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9)
    z = _uint64((z ^ (z >> 27)) * 0x94D049BB133111EB)
    return _uint64(z ^ (z >> 31))


class XorShift128Plus:
    def __init__(self, seed0: int):
        # Expand one seed into two 64-bit states.
        s1 = splitmix64(seed0)
        s2 = splitmix64(s1)
        if s1 == 0 and s2 == 0:
            s2 = 1
        self.s0 = s1
        self.s1 = s2

    def next_u64(self) -> int:
        s1 = self.s0
        s0 = self.s1
        self.s0 = s0
        s1 ^= _uint64(s1 << 23)
        s1 ^= _uint64(s1 >> 17)
        s1 ^= s0
        s1 ^= _uint64(s0 >> 26)
        self.s1 = s1
        return _uint64(self.s0 + self.s1)

    def rand(self) -> float:
        # Use top 53 bits for IEEE double in [0,1)
        return ((self.next_u64() >> 11) & ((1 << 53) - 1)) / float(1 << 53)


def random_unit_vector(rng: XorShift128Plus) -> Tuple[float, float, float]:
    u = rng.rand()
    v = rng.rand()
    theta = 2.0 * math.pi * u
    z = 2.0 * v - 1.0
    r = math.sqrt(max(0.0, 1.0 - z * z))
    return (r * math.cos(theta), r * math.sin(theta), z)


def read_lock_float(root: Path, rel_path: str, key_path: List[str]) -> float:
    obj = json.loads((root / rel_path).read_text(encoding="utf-8"))
    cur: Any = obj
    for k in key_path:
        cur = cur[k]
    # Lock values are stored as decimal strings.
    return float(cur)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", required=True, help="protocol.yaml path")
    ap.add_argument("--out", required=True, help="output run directory")
    args = ap.parse_args()

    prot_path = Path(args.protocol).resolve()
    prot = yaml.safe_load(prot_path.read_text(encoding="utf-8"))

    run_dir = Path(args.out).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "outputs").mkdir(exist_ok=True)

    # Compute chi_rot per paper definition: (ell_rot/a) * Omega_rot * dt
    # (toy runner reads canonical locks if present)
    root = Path(__file__).resolve().parents[3]  # .../bundle_root
    l_rot = read_lock_float(root, "registry/canon_lock.json", ["inputs", "l_rot_m"])
    a_m = read_lock_float(root, "registry/realization_lock.json", ["inputs", "a_m"])
    dt_s = read_lock_float(root, "registry/realization_lock.json", ["inputs", "dt_s"])

    omega_rot = float(prot.get("parameters", {}).get("omega_rot", 0.0))
    chi_rot = (l_rot / a_m) * omega_rot * dt_s

    axis = prot.get("parameters", {}).get("axis_u", [1.0, 0.0, 0.0])
    axis_u = (float(axis[0]), float(axis[1]), float(axis[2]))

    n_steps = int(prot.get("parameters", {}).get("n_steps", 256))
    seed0 = int(prot.get("seed_policy", {}).get("seed0", 0))

    rng = XorShift128Plus(seed0)
    directions = [random_unit_vector(rng) for _ in range(n_steps)]

    metrics = compute_metrics(axis_u=axis_u, chi_rot=chi_rot, directions=directions)
    gates = run_all_gates(metrics)

    # Minimal log
    run_log = [
        {
            "ts": prot.get("created"),
            "run_id": run_dir.name,
            "pid": "ROT-ANISO-REF",
            "ver": prot.get("module_version"),
            "phase": "simulate",
            "event": "START",
            "payload": {"seed0": seed0, "n_steps": n_steps},
        },
        {
            "ts": prot.get("created"),
            "run_id": run_dir.name,
            "pid": "ROT-ANISO-REF",
            "ver": prot.get("module_version"),
            "phase": "metrics",
            "event": "METRIC",
            "payload": {"chi_rot": chi_rot, **to_json(metrics)},
        },
    ]
    for gid, gr in gates.items():
        run_log.append(
            {
                "ts": prot.get("created"),
                "run_id": run_dir.name,
                "pid": "ROT-ANISO-REF",
                "ver": prot.get("module_version"),
                "phase": "gates",
                "event": "GATE",
                "payload": {
                    "gate_id": gid,
                    "status": gr.status,
                    "metrics": gr.metrics,
                    "thresholds": gr.thresholds,
                    "fail_code": gr.fail_code,
                },
            }
        )
    run_log.append(
        {
            "ts": prot.get("created"),
            "run_id": run_dir.name,
            "pid": "ROT-ANISO-REF",
            "ver": prot.get("module_version"),
            "phase": "final",
            "event": "END",
            "payload": {"status": "PASS" if all(gr.status == "PASS" for gr in gates.values()) else "FAIL"},
        }
    )

    append_jsonl(run_dir / "run_log.jsonl", run_log)

    # metrics.json
    metrics_obj = {
        "run_id": run_dir.name,
        "pid": "ROT-ANISO-REF",
        "ver": prot.get("module_version"),
        "metrics": {"chi_rot": chi_rot, **to_json(metrics)},
        "units": {"chi_rot": "dimensionless", "beta_g": "dimensionless", "A_parallel": "dimensionless", "A_perp": "dimensionless", "Delta_bb": "dimensionless"},
        "provenance": {
            "protocol": str(prot_path.relative_to(root)),
            "protocol_sha256": sha256_file(prot_path),
            "locks": {
                "canon_lock": "registry/canon_lock.json",
                "realization_lock": "registry/realization_lock.json",
            },
        },
        "gates": {gid: {"status": gr.status, "fail_code": gr.fail_code} for gid, gr in gates.items()},
    }
    write_json(run_dir / "metrics.json", metrics_obj)

    # manifest
    manifest = build_manifest(run_dir)
    # Fill in run-level identity fields
    manifest["run_id"] = run_dir.name
    manifest["pid"] = "ROT-ANISO-REF"
    manifest["ver"] = prot.get("module_version")
    write_json(run_dir / "manifest.json", manifest)

    print("[OK] rot_aniso run written to", run_dir)


if __name__ == "__main__":
    main()
