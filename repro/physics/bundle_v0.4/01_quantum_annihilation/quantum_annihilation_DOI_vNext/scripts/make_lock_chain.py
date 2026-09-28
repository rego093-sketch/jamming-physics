#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_lock_chain.py
- 목적: LOCK/canon_lock.json, LOCK/realization_lock.json, LOCK/analysis_lock.json의 sha256을 계산하고
        결합 해시(lock_chain_sha256)를 만들어 LOCK/LOCK_CHAIN.json에 저장.
- 결합 규칙:
    lock_chain_sha256 = SHA256( sha_canon + sha_realization + sha_analysis )
  (여기서 +는 문자열 결합)
"""

from __future__ import annotations
import hashlib, json
from pathlib import Path

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def main():
    root = Path(__file__).resolve().parents[1]
    canon = root/"LOCK"/"canon_lock.json"
    real  = root/"LOCK"/"realization_lock.json"
    an    = root/"LOCK"/"analysis_lock.json"

    sha_c = sha256_file(canon)
    sha_r = sha256_file(real)
    sha_a = sha256_file(an)

    chain = sha256_bytes((sha_c + sha_r + sha_a).encode("utf-8"))

    out = {
        "canon_lock_sha256": sha_c,
        "realization_lock_sha256": sha_r,
        "analysis_lock_sha256": sha_a,
        "lock_chain_sha256": chain,
        "rule": "SHA256( sha_canon + sha_realization + sha_analysis )",
        "notes": "LOCK 체인. 이 해시가 바뀌면 다른 버전(다른 정준/단위구현/분석규약)이다."
    }

    (root/"LOCK"/"LOCK_CHAIN.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote LOCK/LOCK_CHAIN.json")
    print("lock_chain_sha256 =", chain)

if __name__ == "__main__":
    main()
