#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[reproduce] 1) LOCK chain 생성"
python3 scripts/make_lock_chain.py

echo "[reproduce] 2) 정준 파생값 생성"
python3 scripts/compute_canon.py

echo "[reproduce] 3) run 검증"
bash validation/verify_all.sh

echo "[reproduce] DONE"
