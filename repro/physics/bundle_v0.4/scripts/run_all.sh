#!/usr/bin/env bash
set -euo pipefail

# Deterministic end-to-end reproducibility driver (v0.2.6)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/8] tools/validate_bundle.py"
python3 tools/validate_bundle.py

echo "[2/8] scripts/build_derived.py"
python3 scripts/build_derived.py

echo "[3/8] 04_vp_whitepaper/scripts/run_chem_minimal.py"
python3 04_vp_whitepaper/scripts/run_chem_minimal.py

echo "[4/8] 04_vp_whitepaper/scripts/run_chem_external_inspection.py"
python3 04_vp_whitepaper/scripts/run_chem_external_inspection.py

echo "[5/8] scripts/run_gates.py"
python3 scripts/run_gates.py

echo "[6/8] scripts/build_rcross_report.py"
python3 scripts/build_rcross_report.py

echo "[7/8] scripts/render_gate_reports_tex.py"
python3 scripts/render_gate_reports_tex.py

echo "[8/8] scripts/seal_snapshot.py"
python3 scripts/seal_snapshot.py

echo "[done] reproducibility pipeline completed."
