from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def repo_root() -> Path:
    # scripts/ -> repo root is parent of scripts/
    return Path(__file__).resolve().parents[1]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_sha256sums(sums_path: Path) -> List[Tuple[str, str]]:
    pairs = []
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # format: <hex>  <relpath>
        parts = line.split()
        if len(parts) < 2:
            continue
        hexhash = parts[0].strip()
        relpath = parts[-1].strip()
        pairs.append((hexhash, relpath))
    return pairs

def write_sha256sums(sums_path: Path, items: List[Tuple[str, str]]) -> None:
    lines = ["# sha256  path (relative to bundle root)"]
    for h, rel in items:
        lines.append(f"{h}  {rel}")
    sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
