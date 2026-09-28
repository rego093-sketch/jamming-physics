#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""재현성 검증용 MANIFEST.sha256 생성 스크립트.

번들 루트(이 파일이 들어 있는 scripts/의 상위 디렉토리)를 기준으로
모든 파일의 SHA-256 해시를 계산하여 `MANIFEST.sha256`에 기록한다.
`MANIFEST.sha256` 자체는 해시 대상에서 제외한다.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


EXCLUDE_NAMES = {"MANIFEST.sha256"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    files = [
        p
        for p in root.rglob("*")
        if p.is_file() and p.name not in EXCLUDE_NAMES
    ]
    files = sorted(files, key=lambda p: p.as_posix())

    lines = []
    for p in files:
        rel = p.relative_to(root).as_posix()
        lines.append(f"{sha256_file(p)}  {rel}")

    manifest = root / "MANIFEST.sha256"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {manifest} with {len(files)} entries.")


if __name__ == "__main__":
    main()
