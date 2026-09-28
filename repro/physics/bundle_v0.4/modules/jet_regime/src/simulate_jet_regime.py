#!/usr/bin/env python3
"""Deterministic reference runner for the jet_regime module.

Usage:
  python modules/jet_regime/src/simulate_jet_regime.py --protocol modules/jet_regime/protocol.yaml --out runs/jet_regime_<id>

This runner generates toy directional-flux events, computes simple jet metrics,
then evaluates toy Gates (G-JET1, G-JET2, G-LOG, G-REP). It is intended to be
*deterministic* and schema-conforming; it does NOT constitute physical validation.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict

import yaml

# Allow running this file directly.
import sys
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from extract_event_flux import generate_events
from estimators import compute_metrics, to_json
from gates import run_all_gates
from io_schema import append_jsonl, build_manifest, sha256_file, write_json


def _uint64(x: int) -> int:
    return x & 0xFFFFFFFFFFFFFFFF


def splitmix64(seed: int) -> int:
    z = _uint64(seed + 0x9E3779B97F4A7C15)
    z = _uint64((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9)
    z = _uint64((z ^ (z >> 27)) * 0x94D049BB133111EB)
    return _uint64(z ^ (z >> 31))


class XorShift128Plus:
    def __init__(self, seed0: int):
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
        return ((self.next_u64() >> 11) & ((1 << 53) - 1)) / float(1 << 53)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    prot_path = Path(args.protocol).resolve()
    prot = yaml.safe_load(prot_path.read_text(encoding="utf-8"))

    run_dir = Path(args.out).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "outputs").mkdir(exist_ok=True)

    n_steps = int(prot.get("parameters", {}).get("n_steps", 512))
    seed0 = int(prot.get("seed_policy", {}).get("seed0", 0))
    J_star = float(prot.get("parameters", {}).get("J_star", 0.65))
    q_star = float(prot.get("parameters", {}).get("q_star", 0.7))
    P_star = float(prot.get("parameters", {}).get("P_star", 0.6))
    theta_star = float(prot.get("parameters", {}).get("theta_star", 0.35))

    rng = XorShift128Plus(seed0)
    events = generate_events(rng, n_steps=n_steps)

    metrics = compute_metrics(events, q_star=q_star, theta_star=theta_star)
    gates = run_all_gates(metrics, J_star=J_star, P_star=P_star)

    run_log = [
        {
            "ts": prot.get("created"),
            "run_id": run_dir.name,
            "pid": "JET-REGIME-REF",
            "ver": prot.get("module_version"),
            "phase": "simulate",
            "event": "START",
            "payload": {"seed0": seed0, "n_steps": n_steps},
        },
        {
            "ts": prot.get("created"),
            "run_id": run_dir.name,
            "pid": "JET-REGIME-REF",
            "ver": prot.get("module_version"),
            "phase": "metrics",
            "event": "METRIC",
            "payload": {**to_json(metrics)},
        },
    ]
    for gid, gr in gates.items():
        run_log.append(
            {
                "ts": prot.get("created"),
                "run_id": run_dir.name,
                "pid": "JET-REGIME-REF",
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
            "pid": "JET-REGIME-REF",
            "ver": prot.get("module_version"),
            "phase": "final",
            "event": "END",
            "payload": {"status": "PASS" if all(gr.status=="PASS" for gr in gates.values()) else "FAIL"},
        }
    )

    append_jsonl(run_dir / "run_log.jsonl", run_log)

    root = Path(__file__).resolve().parents[3]
    metrics_obj = {
        "run_id": run_dir.name,
        "pid": "JET-REGIME-REF",
        "ver": prot.get("module_version"),
        "metrics": {**to_json(metrics)},
        "units": {
            "J": "dimensionless",
            "dJ_x": "dimensionless",
            "dJ_y": "dimensionless",
            "dJ_z": "dimensionless",
            "theta_J": "rad",
            "P_J": "dimensionless",
            "M_J": "dimensionless"
        },
        "provenance": {
            "protocol": str(prot_path.relative_to(root)),
            "protocol_sha256": sha256_file(prot_path),
        },
        "gates": {gid: {"status": gr.status, "fail_code": gr.fail_code} for gid, gr in gates.items()},
    }
    write_json(run_dir / "metrics.json", metrics_obj)

    manifest = build_manifest(run_dir)
    manifest.update({"run_id": run_dir.name, "pid": "JET-REGIME-REF", "ver": prot.get("module_version")})
    write_json(run_dir / "manifest.json", manifest)

    print("[OK] jet_regime run written to", run_dir)


if __name__ == "__main__":
    main()
