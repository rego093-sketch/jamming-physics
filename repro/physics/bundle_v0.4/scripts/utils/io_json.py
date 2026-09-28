"""Stable JSON IO helpers.

These helpers enforce:
  - UTF-8 encoding
  - sorted keys
  - deterministic whitespace

They are intentionally minimal to keep the bundle dependency-free.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    path.write_text(text, encoding='utf-8')
