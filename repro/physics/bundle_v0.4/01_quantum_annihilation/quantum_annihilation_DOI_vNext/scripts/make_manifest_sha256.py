#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_manifest_sha256.py
- 목적: DOI 패키지 전체 파일의 sha256 목록을 MANIFEST.sha256로 생성.
- 불변성:
  * 검증 과정에서 생성될 수 있는 임시 산출물(validation/_out)은 MANIFEST에 포함하지 않는다.
  * __pycache__, *.pyc 등 환경 의존 산출물도 제외한다.
- 주의: MANIFEST.sha256 자체는 제외한다.
"""

from __future__ import annotations
import hashlib
from pathlib import Path

EXCLUDE_NAMES = {"MANIFEST.sha256"}
EXCLUDE_DIRS  = {"__pycache__", ".pytest_cache", "validation/_out"}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def is_excluded(path: Path, root: Path) -> bool:
    if path.name in EXCLUDE_NAMES:
        return True
    if path.suffix == ".pyc":
        return True
    rel = path.relative_to(root).as_posix()
    # 디렉터리 기반 제외
    for d in EXCLUDE_DIRS:
        if rel == d or rel.startswith(d + "/"):
            return True
    # __pycache__가 중간에 끼어있으면 제외
    if "/__pycache__/" in rel or rel.endswith("/__pycache__"):
        return True
    return False

def main():
    root = Path(".").resolve()
    files = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if is_excluded(p, root):
            continue
        files.append(p)

    files = sorted(files, key=lambda p: p.as_posix())

    lines = []
    for p in files:
        rel = p.relative_to(root).as_posix()
        lines.append(f"{sha256_file(p)}  {rel}")

    (root/"MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote MANIFEST.sha256 ({len(files)} files; excluded validation/_out, __pycache__, *.pyc)")

if __name__ == "__main__":
    main()
