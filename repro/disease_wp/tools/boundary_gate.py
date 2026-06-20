#!/usr/bin/env python3
"""boundary_gate.py — wiring guard for the sibling-package ownership boundary.

WHAT THIS CHECKS (honest scope): that the etiologic-class ownership boundary between
this volume (monogenic/rare disease) and the 13 body-system packages (acquired/common/
loop-dysregulation disease) is DECLARED and EMBEDDED in the package — i.e. that the
cross-package master map is carried here, that SCOPE.md states the binding boundary
rules (BOUNDARY-1 / BOUNDARY-2, the etiology-not-region axis, the tie-break, the
anti-redundancy rationale), that CONSTITUTION_disease.md carries the binding clause
C-D10, and that README points to the map.

WHAT THIS DOES NOT CHECK: whether any specific disease was classified into the correct
volume. Semantic scope compliance stays the author's call at index time under BOUNDARY-1
(SCOPE.md). This gate guarantees the rule is present and wired, not that it was obeyed.

Living tool (post-dates the R2 freeze); intentionally NOT in the frozen engine pin.
Deterministic, stdlib-only, no network. Exits nonzero on any failed check.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"


def _read(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def _norm(s: str) -> str:
    """Collapse all whitespace (incl. line wraps) to single spaces so marker
    checks are layout-independent — a marker that wraps across lines still matches."""
    return " ".join(s.split())


# Each check: (id, ok_bool, detail). A check passes iff ok_bool is True.
def run_checks() -> list[tuple[str, bool, str]]:
    checks: list[tuple[str, bool, str]] = []

    # 1 — the cross-package master map is carried at package root
    map_raw = _read("VP_FRAMEWORK_MAP.md")
    map_txt = _norm(map_raw)
    checks.append((
        "map_present_at_root",
        bool(map_raw.strip()),
        "VP_FRAMEWORK_MAP.md present and non-empty" if map_raw.strip()
        else "VP_FRAMEWORK_MAP.md missing or empty at package root",
    ))

    # 2 — the map carries the §6 ownership contract (etiology axis + the contract section)
    map_markers = ["OWNERSHIP CONTRACT", "병인", "disease_wp", "tie-break"]
    map_hits = [m for m in map_markers if m in map_txt]
    checks.append((
        "map_carries_ownership_contract",
        len(map_hits) == len(map_markers),
        f"map §6 contract markers present: {map_hits}" if len(map_hits) == len(map_markers)
        else f"map §6 contract markers MISSING: {sorted(set(map_markers) - set(map_hits))}",
    ))

    # 3 — SCOPE.md declares the sibling body-system boundary section
    scope_txt = _norm(_read("SCOPE.md"))
    scope_section = "Sibling body-system packages" in scope_txt
    checks.append((
        "scope_declares_sibling_boundary",
        scope_section,
        "SCOPE.md carries the sibling body-system boundary section" if scope_section
        else "SCOPE.md is missing the 'Sibling body-system packages' boundary section",
    ))

    # 4 — SCOPE.md carries the binding rules + anti-redundancy rationale verbatim markers
    scope_markers = [
        "etiologic class, not body region",  # the dividing axis
        "BOUNDARY-1",                          # binding ownership rule
        "BOUNDARY-2",                          # synthesis seam
        "prevent redundant research",          # the stated purpose
        "acquired/common \u2192 body-system package",  # the in_scope=false reason string
    ]
    scope_hits = [m for m in scope_markers if m in scope_txt]
    checks.append((
        "scope_carries_binding_rules",
        len(scope_hits) == len(scope_markers),
        f"SCOPE.md boundary rule markers present ({len(scope_hits)}/{len(scope_markers)})"
        if len(scope_hits) == len(scope_markers)
        else f"SCOPE.md boundary rule markers MISSING: {sorted(set(scope_markers) - set(scope_hits))}",
    ))

    # 5 — CONSTITUTION carries the binding clause C-D10 referencing map + anti-redundancy
    const_txt = _norm(_read("CONSTITUTION_disease.md"))
    const_ok = ("C-D10" in const_txt
                and "VP_FRAMEWORK_MAP.md" in const_txt
                and "redundant research" in const_txt)
    checks.append((
        "constitution_binds_c_d10",
        const_ok,
        "CONSTITUTION_disease.md carries C-D10 (map + anti-redundancy)" if const_ok
        else "CONSTITUTION_disease.md missing C-D10 / map ref / anti-redundancy language",
    ))

    # 6 — README points to the carried map
    readme_txt = _norm(_read("README.md"))
    readme_ok = "VP_FRAMEWORK_MAP.md" in readme_txt
    checks.append((
        "readme_references_map",
        readme_ok,
        "README.md references VP_FRAMEWORK_MAP.md" if readme_ok
        else "README.md does not reference the carried map",
    ))

    return checks


def main() -> int:
    checks = run_checks()
    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    status = "PASS" if passed == total else "FAIL"

    print(f"boundary_gate: {status} ({passed}/{total})")
    for cid, ok, detail in checks:
        print(f"  [{'OK' if ok else 'XX'}] {cid}: {detail}")

    REPORTS.mkdir(exist_ok=True)
    report = {
        "gate": "boundary",
        "status": status,
        "passed": passed,
        "total": total,
        "scope_note": ("checks that the sibling-package ownership boundary is DECLARED and "
                       "EMBEDDED (wiring/presence), NOT that any specific disease was classified "
                       "correctly (semantic compliance is the author's call at index time)."),
        "checks": [{"id": cid, "ok": ok, "detail": detail} for cid, ok, detail in checks],
    }
    (REPORTS / "boundary.gate.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
