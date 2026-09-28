#!/usr/bin/env bash
set -euo pipefail

# 이 스크립트는 DOI 번들을 한 번에 재실행하기 위한 원커맨드입니다.
# 루트 디렉토리에서 실행한다고 가정합니다.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/5] proton_geometry_v1: simulate_proton.py"
python "${ROOT_DIR}/packages/proton_geometry_v1/code/simulate_proton.py"

echo "[2/5] proton_geometry_v1: analyze_vectors.py"
python "${ROOT_DIR}/packages/proton_geometry_v1/code/analyze_vectors.py"

echo "[3/5] quantum_whitepaper: whitepaper_experiments.py"
python "${ROOT_DIR}/packages/quantum_whitepaper/code/whitepaper_experiments.py"            "${ROOT_DIR}/packages/quantum_whitepaper"

echo "[4/5] jamming_qm_qbook: proton_shell_mc.py"
python "${ROOT_DIR}/packages/jamming_qm_qbook/code/proton_shell_mc.py"

echo "[5/5] Regenerating MANIFEST.sha256"
python "${ROOT_DIR}/scripts/make_manifest_sha256.py"

echo "All simulations and analyses completed."
