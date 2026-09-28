#!/usr/bin/env python3
"""Build outputs/gates/rcross_report.json from locked RCROSS artifacts.

This script exists to satisfy vp_whitepaper_v0_1_2_rigor_v2.tex §11.5.

Inputs (must be present in the bundle):
  - registry/*_lock.json (canon/realization/analysis/gate/protocol)
  - outputs/derived/dt_633.txt
  - outputs/derived/dt_532.txt
  - configs/thresholds.yaml

Output:
  - outputs/gates/rcross_report.json

The purpose is reproducibility scaffolding: it produces a deterministic, fully
traceable JSON report sealed by snapshot checksums.
"""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Dict

getcontext().prec = 120


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml_scalar(path: Path, key_path: str, default: str | None = None) -> str | None:
    """Very small YAML scalar reader (supports only 'a: b' nesting by 2 spaces).

    We intentionally avoid external deps to keep the bundle self-contained.
    """
    wanted = key_path.split(".")
    stack: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        # update stack based on indent (2 spaces per level)
        level = indent // 2
        stack = stack[:level]
        stack.append(k)
        if stack == wanted and v != "":
            return v
    return default


def read_dt_txt(path: Path) -> Decimal:
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        return Decimal(s)
    raise ValueError(f"No numeric payload found in {path}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    # locks
    canon_p = root / "registry" / "canon_lock.json"
    realz_p = root / "registry" / "realization_lock.json"
    analysis_p = root / "registry" / "analysis_lock.json"
    gate_p = root / "registry" / "gate_lock.json"
    prot_p = root / "registry" / "protocol_lock.json"

    canon = read_json(canon_p)
    realz = read_json(realz_p)
    analysis = read_json(analysis_p)
    gate = read_json(gate_p)
    prot = read_json(prot_p)

    created = str(prot.get("created") or "")

    # artifacts
    dt633_p = root / "outputs" / "derived" / "dt_633.txt"
    dt532_p = root / "outputs" / "derived" / "dt_532.txt"
    thresholds_p = root / "configs" / "thresholds.yaml"

    dt_633 = read_dt_txt(dt633_p)
    dt_532 = read_dt_txt(dt532_p)

    dt_mean = (dt_633 + dt_532) / Decimal(2)
    dev = abs(dt_633 - dt_532) / dt_mean if dt_mean != 0 else Decimal(0)

    # threshold: from gate_lock (primary) and thresholds.yaml (mirror)
    dev_max_gate = Decimal(str(gate.get("rcross", {}).get("dev_max", gate.get("tolerances", {}).get("dev_tol_max", "1e-12"))))
    dev_max_yaml = Decimal(str(read_yaml_scalar(thresholds_p, "rcross.dev_max", "1e-12")))

    # Require agreement between the two to avoid silent drift
    dev_max = dev_max_gate
    threshold_consistent = (dev_max_gate == dev_max_yaml)

    status = "PASS" if (threshold_consistent and dev <= dev_max) else ("FAIL" if threshold_consistent else "INCONCLUSIVE")

    report: Dict[str, Any] = {
        "report_type": "rcross_report",
        "report_version": "v0.2.6",
        "created": created,
        "mode": "reference_instance",
        "status": status,
        "lock_refs": {
            "canon_lock": {"path": "registry/canon_lock.json", "lock_id": canon.get("lock_id"), "sha256": sha256_file(canon_p)},
            "realization_lock": {"path": "registry/realization_lock.json", "lock_id": realz.get("lock_id"), "sha256": sha256_file(realz_p)},
            "analysis_lock": {"path": "registry/analysis_lock.json", "lock_id": analysis.get("lock_id"), "sha256": sha256_file(analysis_p)},
            "gate_lock": {"path": "registry/gate_lock.json", "lock_id": gate.get("lock_id"), "sha256": sha256_file(gate_p)},
            "protocol_lock": {"path": "registry/protocol_lock.json", "lock_id": prot.get("lock_id"), "sha256": sha256_file(prot_p)},
        },
        "artifacts": {
            "thresholds": {"path": "configs/thresholds.yaml", "sha256": sha256_file(thresholds_p)},
            "dt_633": {"path": "outputs/derived/dt_633.txt", "sha256": sha256_file(dt633_p)},
            "dt_532": {"path": "outputs/derived/dt_532.txt", "sha256": sha256_file(dt532_p)},
        },
        "dt_633": str(dt_633),
        "dt_532": str(dt_532),
        "dt_mean": str(dt_mean),
        "dev": str(dev),
        "dev_max": str(dev_max),
        "rcross": {
            "channels": ["A633", "A532"],
            "dt_633": str(dt_633),
            "dt_532": str(dt_532),
            "dt_mean": str(dt_mean),
            "dev": str(dev),
            "dev_definition": analysis.get("rcross", {}).get("dev_definition"),
            "dev_max": str(dev_max),
            "threshold_consistent": threshold_consistent,
        },
        "hash_refs": {
            "manifest": {"path": "snapshot/manifest.json"},
            "checksums": {"path": "snapshot/checksums.txt"},
            "registry_snapshot": {"path": "snapshot/registry_snapshot/registry_snapshot.json"},
        },
        "notes": [
            "Reference-instance RCROSS report: values are not experimental measurements.",
            "Sealing requires snapshot/manifest.json and snapshot/checksums.txt to include this file.",
        ],
    }

    # Give the report its own deterministic id (hash of canonical json without report_id)
    rep2 = dict(report)
    rep2.pop("report_id", None)
    canon_bytes = json.dumps(rep2, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    rid = hashlib.sha256(canon_bytes).hexdigest()
    report["report_id"] = f"rcross_report:v0.2.6:sha256:{rid}"

    out_p = root / "outputs" / "gates" / "rcross_report.json"
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    print(f"[OK] wrote {out_p.relative_to(root)} (status={status})")


if __name__ == "__main__":
    main()
