#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

OUT_DIR="validation/_out"
mkdir -p "$OUT_DIR"

echo "[verify_all] ROOT = $ROOT_DIR"
echo "[verify_all] OUT  = $OUT_DIR"

FAIL=0
OUT_CSV="$OUT_DIR/summary_table.csv"
echo "run_dir,run_id,level0_integrity,level1_schema,level2_science" > "$OUT_CSV"

for RUN in runs/run_*; do
  if [ ! -d "$RUN" ]; then
    continue
  fi
  echo "------------------------------------------------------------"
  echo "[verify_all] verifying: $RUN"

  OUT_JSON="$OUT_DIR/$(basename "$RUN")__verify_output.json"

  if python3 validation/verify_one.py "$RUN" > "$OUT_JSON"; then
    L0=$(python3 -c "import json; d=json.load(open('$OUT_JSON')); print(d['pass_fail']['level0_integrity'])")
    L1=$(python3 -c "import json; d=json.load(open('$OUT_JSON')); print(d['pass_fail']['level1_schema'])")
    L2=$(python3 -c "import json; d=json.load(open('$OUT_JSON')); print(d['pass_fail']['level2_science'])")
    RID=$(python3 -c "import json; d=json.load(open('$OUT_JSON')); print(d['run_id'])")
    echo "$(basename "$RUN"),$RID,$L0,$L1,$L2" >> "$OUT_CSV"
    if [ "$L0" != "True" ] || [ "$L1" != "True" ] || [ "$L2" != "True" ]; then
      FAIL=1
    fi
  else
    echo "[verify_all] FAIL: $RUN"
    FAIL=1
    echo "$(basename "$RUN"),$(basename "$RUN"),False,False,False" >> "$OUT_CSV"
  fi
done

echo "------------------------------------------------------------"
echo "[verify_all] summary table -> $OUT_CSV"
if [ "$FAIL" -ne 0 ]; then
  echo "[verify_all] RESULT: FAIL"
  exit 1
else
  echo "[verify_all] RESULT: PASS"
  exit 0
fi
