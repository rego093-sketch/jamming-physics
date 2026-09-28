#!/usr/bin/env python3
"""Render JSON gate reports into lightweight TeX include files.

Inputs:
  gate/reports/gate_report_*.json

Outputs:
  gate/reports/gate_report_*.tex

This renderer is intentionally simple:
- Uses verbatim blocks to avoid LaTeX-escaping JSON.
- Is deterministic (stable JSON ordering; uses protocol_lock.created as fallback).

Rationale:
Some gates (e.g., chemistry minimal run) may emit a slightly different JSON schema
than the core vp_whitepaper gates. This script normalizes presentation so that
all gate reports render with (Status, Created, Details, Evidence).
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any, Dict


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def protocol_created(root: Path) -> str:
    p = root / "registry" / "protocol_lock.json"
    if p.exists():
        try:
            return str(read_json(p).get("created") or "")
        except Exception:
            pass
    return str(date.today())


def json_pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    reports_dir = root / "gate" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    created_default = protocol_created(root)

    for jp in sorted(reports_dir.glob("gate_report_*.json"), key=lambda p: p.name):
        obj = read_json(jp)

        gate_id = obj.get("gate_id") or jp.stem
        status = obj.get("status") or obj.get("result") or obj.get("verdict") or "UNKNOWN"
        created = obj.get("created") or obj.get("timestamp_utc") or created_default

        evidence = obj.get("evidence")
        if evidence is None:
            evidence = {}

        details = obj.get("details")
        if details is None:
            # Shallow normalization: show everything that isn't the minimal header.
            skip = {"gate_id", "status", "created", "evidence"}
            details = {k: v for k, v in obj.items() if k not in skip}

        tex_lines = []
        tex_lines.append(f"% Auto-generated from {jp.name}")
        tex_lines.append(f"\\section*{{Gate Report: {gate_id}}}")
        tex_lines.append("\\begin{tabular}{ll}")
        tex_lines.append(f"Status & {status} \\\\")
        tex_lines.append(f"Created & {created} \\\\")
        tex_lines.append("\\end{tabular}")
        tex_lines.append("")
        tex_lines.append("\\subsection*{Details}")
        tex_lines.append("\\begin{verbatim}")
        tex_lines.append(json_pretty(details))
        tex_lines.append("\\end{verbatim}")
        tex_lines.append("")
        tex_lines.append("\\subsection*{Evidence}")
        tex_lines.append("\\begin{verbatim}")
        tex_lines.append(json_pretty(evidence))
        tex_lines.append("\\end{verbatim}")
        tex_lines.append("")

        tp = jp.with_suffix(".tex")
        tp.write_text("\n".join(tex_lines) + "\n", encoding="utf-8")

    print(f"[OK] rendered TeX for {len(list(reports_dir.glob('gate_report_*.json')))} gate report(s).")


if __name__ == "__main__":
    main()
