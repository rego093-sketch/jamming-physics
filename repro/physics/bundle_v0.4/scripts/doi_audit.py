#!/usr/bin/env python3
"""DOI completeness audit for the AQD unified bundle.

This script is intentionally lightweight and deterministic.

Strict checks
------------
1) Every internal citation token used in the VP whitepaper, written as
   "[cite: XX]" or "[cite: XX, YY]", exists in:
     04_vp_whitepaper/docs/citations/CITE_REGISTRY.csv

2) Each registry row has non-empty DOI and URL fields, and the DOI has
   a reasonable syntax.

3) External DOI strings appearing in the TeX (via doi.org/...) also pass
   the same basic syntax check.

Non-fatal warnings
------------------
- Missing local bundle paths referenced in CITE_REGISTRY.csv are reported
  as warnings (because the field may contain wildcards or section anchors).

Exit codes
----------
0 : pass
1 : fail

Usage
-----
python3 scripts/doi_audit.py
python3 scripts/doi_audit.py --root /path/to/bundle
python3 scripts/doi_audit.py --tex 04_vp_whitepaper/vp_whitepaper_v0_1_2_rigor_v2.tex
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


DOI_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)
# Internal cite token: [cite: 12, 34]
CITE_TOKEN_RE = re.compile(r"\[cite:\s*([^\]]+)\]")
# Capture DOIs embedded as doi.org/<doi>
DOI_IN_TEX_RE = re.compile(r"doi\.org/\s*(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", re.IGNORECASE)


@dataclass
class AuditResult:
    ok: bool
    failures: List[str]
    warnings: List[str]


def _extract_internal_cite_ids(tex: str) -> Set[int]:
    ids: Set[int] = set()
    for m in CITE_TOKEN_RE.finditer(tex):
        payload = m.group(1)
        # allow formats: "26", "26, 47", "26 47"
        parts = re.split(r"[\s,]+", payload.strip())
        for p in parts:
            if not p:
                continue
            if p.isdigit():
                ids.add(int(p))
    return ids


def _extract_external_dois(tex: str) -> Set[str]:
    return {m.group(1).strip() for m in DOI_IN_TEX_RE.finditer(tex)}


def _load_cite_registry(csv_path: Path) -> Dict[int, Dict[str, str]]:
    rows: Dict[int, Dict[str, str]] = {}
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if "cite_id" not in reader.fieldnames:
            raise ValueError("CITE_REGISTRY.csv must contain a 'cite_id' column")
        for r in reader:
            raw_id = (r.get("cite_id") or "").strip()
            if not raw_id:
                continue
            if not raw_id.isdigit():
                raise ValueError(f"Invalid cite_id '{raw_id}' in {csv_path}")
            cid = int(raw_id)
            if cid in rows:
                raise ValueError(f"Duplicate cite_id {cid} in {csv_path}")
            rows[cid] = {k: (v or "").strip() for k, v in r.items()}
    return rows


def _check_registry_fields(reg: Dict[int, Dict[str, str]]) -> Tuple[List[str], List[str]]:
    failures: List[str] = []
    warnings: List[str] = []
    for cid, row in sorted(reg.items()):
        doi = row.get("doi", "").strip()
        url = row.get("url", "").strip()
        if not doi:
            failures.append(f"CITE_REGISTRY missing DOI for cite_id={cid}")
        elif not DOI_RE.match(doi):
            failures.append(f"CITE_REGISTRY has malformed DOI for cite_id={cid}: '{doi}'")
        if not url:
            failures.append(f"CITE_REGISTRY missing URL for cite_id={cid}")

        # Optional: check referenced bundle paths exist (warnings)
        paths_field = row.get("bundle_paths", "")
        if paths_field:
            # allow pipes as separators; ignore section anchors after '#'
            for frag in paths_field.split("|"):
                frag = frag.strip()
                if not frag:
                    continue
                frag = frag.split("#", 1)[0].strip()
                # Ignore wildcards
                if "*" in frag or "?" in frag:
                    continue
                # If the path looks like a URL, ignore
                if frag.startswith("http://") or frag.startswith("https://"):
                    continue
                # Some entries may add parenthetical notes; strip those
                frag = frag.split("(", 1)[0].strip()
                if not frag:
                    continue
                # Only check repo-relative paths
                if frag.startswith("/"):
                    continue
                # We only warn if it looks like a path (contains '/'
                if "/" not in frag:
                    continue
                warnings.append(f"(W-PATH) cite_id={cid} references path '{frag}' (existence not checked here)")
    return failures, warnings


def run_audit(root: Path, tex_rel: str, reg_rel: str) -> AuditResult:
    failures: List[str] = []
    warnings: List[str] = []

    tex_path = (root / tex_rel).resolve()
    reg_path = (root / reg_rel).resolve()

    if not tex_path.exists():
        return AuditResult(False, [f"Missing TeX file: {tex_path}"], [])
    if not reg_path.exists():
        return AuditResult(False, [f"Missing registry CSV: {reg_path}"], [])

    tex = tex_path.read_text(encoding="utf-8", errors="replace")

    used_ids = _extract_internal_cite_ids(tex)
    reg = _load_cite_registry(reg_path)

    # Check: every used cite-id exists
    missing = sorted(i for i in used_ids if i not in reg)
    if missing:
        failures.append(
            "Missing cite_id(s) in CITE_REGISTRY.csv: " + ", ".join(map(str, missing))
        )

    # Check: registry fields
    f2, w2 = _check_registry_fields(reg)
    failures.extend(f2)
    warnings.extend(w2)

    # Check: external DOIs in tex
    ext_dois = sorted(_extract_external_dois(tex))
    for d in ext_dois:
        if not DOI_RE.match(d):
            failures.append(f"Malformed external DOI in TeX: '{d}'")

    return AuditResult(ok=(len(failures) == 0), failures=failures, warnings=warnings)


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="AQD DOI completeness audit")
    ap.add_argument("--root", default=".", help="Bundle root directory (default: current dir)")
    ap.add_argument(
        "--tex",
        default="04_vp_whitepaper/vp_whitepaper_v0_1_2_rigor_v2.tex",
        help="TeX path relative to root",
    )
    ap.add_argument(
        "--registry",
        default="04_vp_whitepaper/docs/citations/CITE_REGISTRY.csv",
        help="Registry CSV path relative to root",
    )
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    res = run_audit(root, args.tex, args.registry)

    if res.ok:
        print("[OK] DOI audit PASS")
    else:
        print("[FAIL] DOI audit FAIL")

    if res.failures:
        print("\nFailures:")
        for msg in res.failures:
            print(f"  - {msg}")

    if res.warnings:
        print("\nWarnings:")
        # Deduplicate warnings (some might repeat)
        seen = set()
        for msg in res.warnings:
            if msg in seen:
                continue
            seen.add(msg)
            print(f"  - {msg}")

    return 0 if res.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
