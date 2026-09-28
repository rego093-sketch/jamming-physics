#!/usr/bin/env python3
"""Seal a reproducibility snapshot (manifest + checksums + registry_snapshot).

Creates:
  snapshot/registry_snapshot/registry/*           (copy of registry/)
  snapshot/registry_snapshot/registry_snapshot.json
  snapshot/release_tag.json
  snapshot/checksum_exclusions.txt
  snapshot/checksums.txt
  snapshot/manifest.json

Also writes a convenience mirror:
  registry/registry_snapshot.json

Design goals:
- Deterministic: uses registry/protocol_lock.json['created'] when available.
- Idempotent: repeated runs should produce identical snapshot outputs.
- No self-recursion: checksums exclude checksums.txt and manifest.json.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import shutil
from datetime import date
from pathlib import Path
from typing import Any, Dict, List


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def guess_content_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".tex"}:
        return "text/tex"
    if ext in {".csv"}:
        return "text/csv"
    if ext in {".json"}:
        return "application/json"
    if ext in {".md"}:
        return "text/markdown"
    if ext in {".py"}:
        return "text/x-python"
    if ext in {".pdf"}:
        return "application/pdf"
    # fallback
    return mimetypes.guess_type(str(path))[0] or "application/octet-stream"


def role_for(rel: str) -> str:
    # Keep roles coarse; the manifest is mostly for completeness + sealing.
    if rel.startswith("registry/"):
        return "registry"
    if rel.startswith("snapshot/"):
        return "snapshot"
    if rel.startswith("derived/"):
        return "derived"
    if rel.startswith("gate/reports/"):
        return "gate_report"
    if rel.startswith("gate/logs/"):
        return "gate_log"
    if rel.startswith("scripts/"):
        return "script"
    if rel.startswith("data/raw/"):
        return "data_raw"
    if rel.startswith("data/processed/"):
        return "data_processed"
    # keep existing project structure visible
    if rel.startswith("00_metadata/"):
        return "metadata"
    if rel.startswith("01_") or rel.startswith("02_") or rel.startswith("03_") or rel.startswith("04_"):
        return "module"
    if rel.startswith("tools/"):
        return "tool"
    return "other"


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    # Deterministic timestamp: use locked protocol date if available
    prot_path = root / "registry" / "protocol_lock.json"
    sealed_date = None
    if prot_path.exists():
        try:
            sealed_date = read_json(prot_path).get("created")
        except Exception:
            sealed_date = None
    if not sealed_date:
        sealed_date = str(date.today())

    # Rebuild snapshot/ from scratch to avoid stale self-references.
    snap = root / "snapshot"
    if snap.exists():
        shutil.rmtree(snap)
    snap.mkdir(parents=True, exist_ok=True)

    # registry_snapshot: copy registry/ as-is
    rs_dir = snap / "registry_snapshot" / "registry"
    rs_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(root / "registry", rs_dir)

    # registry_snapshot index (single-file pointer used by G-REP style gates)
    canon = read_json(root / "registry" / "canon_lock.json")
    realz = read_json(root / "registry" / "realization_lock.json")
    prot = read_json(root / "registry" / "protocol_lock.json")
    gate = read_json(root / "registry" / "gate_lock.json")
    analysis_path = root / "registry" / "analysis_lock.json"
    analysis = read_json(analysis_path) if analysis_path.exists() else None

    lock_ids = {
        "canon_lock_id": canon.get("lock_id"),
        "realization_lock_id": realz.get("lock_id"),
        "protocol_lock_id": prot.get("lock_id"),
        "gate_lock_id": gate.get("lock_id"),
    }
    if analysis is not None:
        lock_ids["analysis_lock_id"] = analysis.get("lock_id")

    rs_files = {
        "registry/canon_lock.json": sha256_file(rs_dir / "canon_lock.json"),
        "registry/realization_lock.json": sha256_file(rs_dir / "realization_lock.json"),
        "registry/protocol_lock.json": sha256_file(rs_dir / "protocol_lock.json"),
        "registry/gate_lock.json": sha256_file(rs_dir / "gate_lock.json"),
        "registry/symbols_table.csv": sha256_file(rs_dir / "symbols_table.csv"),
        "registry/units_table.csv": sha256_file(rs_dir / "units_table.csv"),
    }
    if (rs_dir / "analysis_lock.json").exists():
        rs_files["registry/analysis_lock.json"] = sha256_file(rs_dir / "analysis_lock.json")

    rs_meta = {
        "created": sealed_date,
        "registry_snapshot_version": "v0.2.6",
        "locks": lock_ids,
        "files": rs_files,
    }
    rs_canon = json.dumps(rs_meta, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    rs_id = hashlib.sha256(rs_canon).hexdigest()
    rs_meta["registry_snapshot_id"] = f"registry_snapshot:v0.2.6:sha256:{rs_id}"
    rs_text = json.dumps(rs_meta, indent=2, ensure_ascii=False, sort_keys=True) + "\n"

    (snap / "registry_snapshot" / "registry_snapshot.json").write_text(rs_text, encoding="utf-8")
    # Convenience mirror: some appendix scripts in the TeX refer to registry/registry_snapshot.json
    (root / "registry" / "registry_snapshot.json").write_text(rs_text, encoding="utf-8")

    # release tag
    release = {
        "bundle": "AQD_DOI_bundle_unified",
        "version": "v0.2.6",
        "sealed": sealed_date,
        "notes": "Auto-generated snapshot seal for VP whitepaper reproducibility tree (registry/derived/gate/snapshot).",
    }
    (snap / "release_tag.json").write_text(
        json.dumps(release, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    # checksum exclusions
    # - checksums.txt cannot include its own hash
    # - manifest.json is excluded to avoid self-recursion
    exclusions = ["snapshot/checksums.txt", "snapshot/manifest.json"]
    (snap / "checksum_exclusions.txt").write_text("\n".join(exclusions) + "\n", encoding="utf-8")

    def relpath(p: Path) -> str:
        return p.relative_to(root).as_posix()

    # Collect files (relative paths). At this point checksums.txt and manifest.json do not exist.
    all_files: List[Path] = [p for p in root.rglob("*") if p.is_file()]

    exclude_set = set(exclusions)

    # checksums.txt
    checksum_lines: List[str] = []
    sha_map: Dict[str, str] = {}
    for p in sorted(all_files, key=lambda x: relpath(x)):
        rel = relpath(p)
        if rel in exclude_set:
            continue
        h = sha256_file(p)
        sha_map[rel] = h
        checksum_lines.append(f"{h}  ./{rel}")

    (snap / "checksums.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    # manifest.json
    # Re-collect to include checksums.txt; manifest.json is added as a null-hash entry.
    all_files2: List[Path] = [p for p in root.rglob("*") if p.is_file()]

    manifest: List[Dict[str, Any]] = []
    for p in sorted(all_files2, key=lambda x: relpath(x)):
        rel = relpath(p)
        entry = {
            "path": rel,
            "role": role_for(rel),
            "content_type": guess_content_type(p),
            "producer": "manual" if not rel.startswith(("derived/", "gate/reports/", "snapshot/")) else "script",
            "depends_on": [],
            "lock_version": dict(lock_ids),
            "hash_ref": None if rel in exclude_set else sha_map.get(rel),
            "bytes": p.stat().st_size,
        }
        manifest.append(entry)

    # Ensure manifest.json itself is present even though it does not exist yet.
    manifest.append(
        {
            "path": "snapshot/manifest.json",
            "role": role_for("snapshot/manifest.json"),
            "content_type": "application/json",
            "producer": "script",
            "depends_on": [],
            "lock_version": dict(lock_ids),
            "hash_ref": None,
            "bytes": None,
        }
    )

    (snap / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("[OK] sealed snapshot:")
    print("  - snapshot/registry_snapshot/registry/*")
    print("  - snapshot/registry_snapshot/registry_snapshot.json")
    print("  - snapshot/release_tag.json")
    print("  - snapshot/checksum_exclusions.txt")
    print("  - snapshot/checksums.txt")
    print("  - snapshot/manifest.json")


if __name__ == "__main__":
    main()
