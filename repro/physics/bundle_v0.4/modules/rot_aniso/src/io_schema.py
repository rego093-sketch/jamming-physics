"""I/O helpers for the rot_aniso reference stub.

This file is intentionally lightweight and deterministic.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def write_json(path: Path, obj: Any) -> None:
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    path.write_text(text, encoding="utf-8")


def append_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def build_manifest(run_dir: Path, hash_alg: str = "sha256") -> Dict[str, Any]:
    # Deterministic file ordering by path.
    files = []
    for p in sorted(run_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(run_dir).as_posix()
        if rel in {"manifest.json"}:
            # computed last
            continue
        h = sha256_file(p)
        files.append({"path": rel, "bytes": p.stat().st_size, "sha256": h})
    return {"hash_alg": hash_alg, "files": files}
