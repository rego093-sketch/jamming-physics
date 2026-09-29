from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from common import repo_root

def run(cmd: list[str]) -> int:
    p = subprocess.run([sys.executable] + cmd, cwd=repo_root())
    return int(p.returncode)

def main() -> int:
    rc1 = run(["scripts/verify_checksums.py"])
    rc2 = run(["scripts/run_qa.py"])
    rc3 = run(["scripts/make_summaries.py"])
    rc4 = run(["scripts/hardgate.py"])
    # overall fail if checksum or QA fails
    return 0 if (rc1 == 0 and rc2 == 0 and rc3 == 0 and rc4 == 0) else 1

if __name__ == "__main__":
    raise SystemExit(main())
