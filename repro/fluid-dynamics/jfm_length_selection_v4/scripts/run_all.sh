#!/usr/bin/env bash
set -euo pipefail

echo "== Repro run started: $(date)"
echo "Python: $(python -V)"
echo "Working dir: $PWD"

# Allow scripts to import code/dns2d.py as 'dns2d'
export PYTHONPATH="${PWD}/code:${PYTHONPATH:-}"

# 1) Prepare v3 data (unpack once)
if [ ! -d "v3" ]; then
  echo "== Unpacking JFM_DOI_FULLSTORY_v3.zip -> ./v3"
  unzip -q JFM_DOI_FULLSTORY_v3.zip -d v3
else
  echo "== v3 already unpacked -> ./v3"
fi

# 2) (Re)generate the tiny DNS suite (v4 demo)
echo "== Running DNS demo suite (v4)"
python scripts/run_dns_suite.py

# 3) Analyze demo suite -> Sb, L* and a small log–log slope (demo only)
echo "== Analyzing DNS demo suite (v4)"
python scripts/analyze_dns_suite.py

# 4) Assertions on ground-truth synthetic dataset (from v3 archive)
echo "== Running assertions (synthetic ground-truth; target slope 0.5 ± 0.02)"
python scripts/assert_reproduction.py --v3-root v3 --tol 0.02

# 5) Show outputs
echo "== Outputs in data/dns_runs:"
ls -lh data/dns_runs || true
echo "== DONE"
