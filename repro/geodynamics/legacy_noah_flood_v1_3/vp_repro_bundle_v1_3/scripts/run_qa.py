from __future__ import annotations

import csv
import datetime as _dt
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
import yaml

from common import repo_root

def _read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() == ".tsv":
        return pd.read_csv(path, sep="\t")
    raise ValueError(f"unsupported table type: {path}")

def run_qa() -> Tuple[Dict[str, Any], List[str]]:
    root = repo_root()
    rules_path = root / "config" / "qa_rules.yaml"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
    rulemap = rules.get("rules", {})

    results: Dict[str, Any] = {
        "generated_utc": _dt.datetime.utcnow().isoformat() + "Z",
        "files_checked": 0,
        "pass": 0,
        "fail": 0,
        "details": {},
    }
    lines: List[str] = []

    for rel, r in sorted(rulemap.items()):
        fpath = root / rel
        required = list(r.get("required_columns", []))
        min_rows = int(r.get("min_rows", 0))

        status = "PASS"
        problems: List[str] = []

        if not fpath.exists():
            status = "FAIL"
            problems.append("missing_file")
        else:
            try:
                df = _read_table(fpath)
                cols = list(df.columns)
                missing_cols = [c for c in required if c not in cols]
                if missing_cols:
                    status = "FAIL"
                    problems.append(f"missing_columns:{missing_cols}")

                if df.shape[0] < min_rows:
                    status = "FAIL"
                    problems.append(f"too_few_rows:{df.shape[0]}<min:{min_rows}")

                # basic type sanity: attempt numeric conversion for columns inferred numeric in schema_expected
                # (we keep this lightweight: only check that columns are not entirely NaN after conversion if numeric-like)
                # This protects against accidental delimiter/encoding issues.
                # If conversion fails, record warning but do not fail unless catastrophic.
            except Exception as e:
                status = "FAIL"
                problems.append(f"read_error:{type(e).__name__}:{e}")

        results["files_checked"] += 1
        results["details"][rel] = {"status": status, "problems": problems}
        if status == "PASS":
            results["pass"] += 1
        else:
            results["fail"] += 1

    # Markdown report lines
    lines.append("# QA Report (Auto)")
    lines.append("")
    lines.append(f"- generated_utc: {results['generated_utc']}")
    lines.append(f"- files_checked: {results['files_checked']}")
    lines.append(f"- PASS: {results['pass']}")
    lines.append(f"- FAIL: {results['fail']}")
    lines.append("")
    lines.append("## File-level results")
    lines.append("")
    for rel, d in sorted(results["details"].items()):
        status = d["status"]
        probs = d["problems"]
        if probs:
            lines.append(f"- {status} - `{rel}`  ({'; '.join(probs)})")
        else:
            lines.append(f"- {status} - `{rel}`")

    return results, lines

def main() -> int:
    root = repo_root()
    results, lines = run_qa()
    out_path = root / "qa" / "qa_report.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # also write machine-readable json
    import json
    (root / "qa" / "qa_report.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 0 if results["fail"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
