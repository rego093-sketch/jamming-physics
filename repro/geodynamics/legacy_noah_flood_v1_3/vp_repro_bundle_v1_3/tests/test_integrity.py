from __future__ import annotations

from pathlib import Path

import pytest

from scripts.common import repo_root, sha256_file, read_sha256sums

def test_sha256sums_present():
    sums = repo_root() / "checksums" / "SHA256SUMS.txt"
    assert sums.exists()

def test_sha256sums_verify():
    root = repo_root()
    sums_path = root / "checksums" / "SHA256SUMS.txt"
    pairs = read_sha256sums(sums_path)
    assert pairs, "no checksum entries found"
    for expected, rel in pairs:
        fpath = root / rel
        assert fpath.exists(), f"missing file: {rel}"
        got = sha256_file(fpath)
        assert got.lower() == expected.lower(), f"checksum mismatch: {rel}"
