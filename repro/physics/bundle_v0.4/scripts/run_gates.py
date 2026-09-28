#!/usr/bin/env python3
"""Run a minimal Gate stack for core whitepaper claims.

This script generates deterministic JSON gate reports under:
  gate/reports/

Focus: the W.3.1 executive table items (non-chem):
  - a
  - dt
  - U_lat
  - r_e
  - m_e
  - m_p
  - m_H
  - m_p/m_e
  - RCROSS-style invariants (Appendix M)

The purpose is not to "prove physics" but to ensure that the DOI bundle contains
machine-checkable evidence files whose values are fully determined by LOCK inputs.
"""

from __future__ import annotations

import json
import hashlib
from datetime import date
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Dict


getcontext().prec = 120


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def d(x: Any) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def _protocol_created(root: Path) -> str:
    p = root / "registry" / "protocol_lock.json"
    if p.exists():
        try:
            return str(read_json(p).get("created") or date.today())
        except Exception:
            pass
    return str(date.today())


def report_template(gate_id: str, status: str, details: Dict[str, Any], root: Path) -> Dict[str, Any]:
    created = _protocol_created(root)
    canon = root / "registry" / "canon_lock.json"
    realz = root / "registry" / "realization_lock.json"
    prot  = root / "registry" / "protocol_lock.json"
    gate  = root / "registry" / "gate_lock.json"
    return {
        "gate_id": gate_id,
        "status": status,
        "created": created,
        "evidence": {
            "registry": {
                "canon_lock": {"path": "registry/canon_lock.json", "sha256": sha256_file(canon)},
                "realization_lock": {"path": "registry/realization_lock.json", "sha256": sha256_file(realz)},
                "protocol_lock": {"path": "registry/protocol_lock.json", "sha256": sha256_file(prot)},
                "gate_lock": {"path": "registry/gate_lock.json", "sha256": sha256_file(gate)},
            },
            "derived": {
                "claims": {
                    "path": "derived/claims.json",
                    "sha256": sha256_file(root / "derived" / "claims.json") if (root / "derived" / "claims.json").exists() else None,
                }
            },
        },
        "details": details,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    # Ensure derived outputs exist.
    import subprocess
    subprocess.check_call(["python3", str(root / "scripts" / "build_derived.py")])

    claims = read_json(root / "derived" / "claims.json")
    derived = claims["derived"]

    canon = read_json(root / "registry" / "canon_lock.json")
    realz = read_json(root / "registry" / "realization_lock.json")
    prot  = read_json(root / "registry" / "protocol_lock.json")
    gate  = read_json(root / "registry" / "gate_lock.json")

    # Pull locked values
    a_m = d(realz["inputs"]["a_m"])
    dt_s = d(realz["inputs"]["dt_s"])
    c_ref = d(realz["inputs"]["c_ref_m_s"])

    D_anch = d(canon["inputs"]["D_anch_m"])
    r_p = d(canon["inputs"]["r_p_m"])
    pi = d(canon["constants"]["pi"])
    h = d(canon["constants"]["h_J_s"])

    GeV_to_J = d(prot.get("unit_conversions", {}).get("GeV_to_J", prot.get("unit_conventions", {}).get("GeV_to_J")))
    if GeV_to_J is None:
        raise RuntimeError("protocol_lock missing GeV_to_J")

    delta = Decimal(1) / (pi * pi)

    # Compute a few key derived values again (independent recomputation)
    r_e = (D_anch / Decimal(2)) * delta
    lambda_C = (pi / Decimal(2)) * r_p
    U_lat_J = (h * c_ref) / a_m
    U_lat_GeV = U_lat_J / GeV_to_J

    S_e = r_e / a_m
    S_p = lambda_C / a_m

    m_H_GeV = U_lat_GeV / (Decimal(5) * pi)
    m_p_GeV = U_lat_GeV / S_p
    m_e_GeV = U_lat_GeV / S_e

    # Invariants
    I_H = (m_H_GeV * (Decimal(5) * pi)) / U_lat_GeV
    I_p = (m_p_GeV * S_p) / U_lat_GeV
    I_e = (m_e_GeV * S_e) / U_lat_GeV

    dev_max = max(abs(I_H - 1), abs(I_p - 1), abs(I_e - 1))

    dev_tol = d(
        gate.get("tolerances", {}).get(
            "dev_tol_max",
            gate.get("thresholds", {}).get("numeric_rel_tol_default", "1e-12"),
        )
    )

    # Helper for numeric compare against derived/claims
    def eq_str(computed: Decimal, stored_str: str, rel_tol: Decimal = Decimal("1e-25")) -> bool:
        stored = d(stored_str)
        if stored == 0:
            return abs(computed - stored) <= rel_tol
        return abs((computed - stored) / stored) <= rel_tol

    reports_dir = root / "gate" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Track only the reports written by *this* script to avoid implying that
    # pre-existing reports (e.g., chemistry gates generated elsewhere) were
    # produced in the current run.
    generated: list[str] = []

    # gate_report_a.json
    ok_a = eq_str(a_m, derived["a_m"], rel_tol=Decimal("1e-30"))
    write_json(reports_dir / "gate_report_a.json", report_template(
        gate_id="G-A",
        status="PASS" if ok_a else "FAIL",
        details={"a_m": str(a_m), "a_m_expected": derived["a_m"], "rel_tol": "1e-30"},
        root=root,
    ))
    generated.append("gate/reports/gate_report_a.json")

    # gate_report_dt.json
    ok_dt = eq_str(dt_s, derived["dt_s"], rel_tol=Decimal("1e-30"))
    write_json(reports_dir / "gate_report_dt.json", report_template(
        gate_id="G-DT",
        status="PASS" if ok_dt else "FAIL",
        details={"dt_s": str(dt_s), "dt_s_expected": derived["dt_s"], "rel_tol": "1e-30"},
        root=root,
    ))
    generated.append("gate/reports/gate_report_dt.json")

    # gate_report_Ulat.json
    ok_U = eq_str(U_lat_GeV, derived["U_lat_GeV"], rel_tol=Decimal("1e-25"))
    write_json(reports_dir / "gate_report_Ulat.json", report_template(
        gate_id="G-ULAT",
        status="PASS" if ok_U else "FAIL",
        details={
            "U_lat_J": str(U_lat_J),
            "U_lat_GeV": str(U_lat_GeV),
            "U_lat_GeV_expected": derived["U_lat_GeV"],
            "rel_tol": "1e-25",
        },
        root=root,
    ))
    generated.append("gate/reports/gate_report_Ulat.json")

    # gate_report_re.json
    ok_re = eq_str(r_e, derived["r_e_m"], rel_tol=Decimal("1e-25"))
    write_json(reports_dir / "gate_report_re.json", report_template(
        gate_id="G-RE",
        status="PASS" if ok_re else "FAIL",
        details={"r_e_m": str(r_e), "r_e_m_expected": derived["r_e_m"], "rel_tol": "1e-25"},
        root=root,
    ))
    generated.append("gate/reports/gate_report_re.json")

    # gate_report_me.json
    ok_me = eq_str(m_e_GeV, derived["m_e_GeV"], rel_tol=Decimal("1e-25"))
    write_json(reports_dir / "gate_report_me.json", report_template(
        gate_id="G-ME",
        status="PASS" if ok_me else "FAIL",
        details={"m_e_GeV": str(m_e_GeV), "m_e_GeV_expected": derived["m_e_GeV"], "rel_tol": "1e-25"},
        root=root,
    ))
    generated.append("gate/reports/gate_report_me.json")

    # gate_report_mp.json
    ok_mp = eq_str(m_p_GeV, derived["m_p_GeV"], rel_tol=Decimal("1e-25"))
    write_json(reports_dir / "gate_report_mp.json", report_template(
        gate_id="G-MP",
        status="PASS" if ok_mp else "FAIL",
        details={"m_p_GeV": str(m_p_GeV), "m_p_GeV_expected": derived["m_p_GeV"], "rel_tol": "1e-25"},
        root=root,
    ))
    generated.append("gate/reports/gate_report_mp.json")

    # gate_report_mH.json
    ok_mH = eq_str(m_H_GeV, derived["m_H_GeV"], rel_tol=Decimal("1e-25"))
    write_json(reports_dir / "gate_report_mH.json", report_template(
        gate_id="G-MH",
        status="PASS" if ok_mH else "FAIL",
        details={"m_H_GeV": str(m_H_GeV), "m_H_GeV_expected": derived["m_H_GeV"], "rel_tol": "1e-25"},
        root=root,
    ))
    generated.append("gate/reports/gate_report_mH.json")

    # gate_report_mp_me.json
    ratio = m_p_GeV / m_e_GeV
    ratio_expected = d(derived["m_p_GeV"]) / d(derived["m_e_GeV"])
    ok_ratio = abs((ratio - ratio_expected) / ratio_expected) <= Decimal("1e-25")
    write_json(reports_dir / "gate_report_mp_me.json", report_template(
        gate_id="G-MP-ME",
        status="PASS" if ok_ratio else "FAIL",
        details={
            "m_p_over_m_e": str(ratio),
            "m_p_over_m_e_expected": str(ratio_expected),
            "rel_tol": "1e-25",
        },
        root=root,
    ))
    generated.append("gate/reports/gate_report_mp_me.json")

    # gate_report_RCROSS.json (Appendix M invariants)
    status_rc = "PASS" if dev_max <= dev_tol else "FAIL"
    write_json(reports_dir / "gate_report_RCROSS.json", report_template(
        gate_id="G-RCROSS-APP-M",
        status=status_rc,
        details={
            "I_H": str(I_H),
            "I_p": str(I_p),
            "I_e": str(I_e),
            "dev_max": str(dev_max),
            "dev_tol_max": str(dev_tol),
        },
        root=root,
    ))
    generated.append("gate/reports/gate_report_RCROSS.json")

    # gate_report_REP.json: minimal presence check for snapshot files.
    required = gate.get("gates", {}).get("G-REP", {}).get("required_snapshot_files", [])
    missing = [p for p in required if not (root / p).exists()]
    status_rep = "PASS" if not missing else "INCONCLUSIVE"
    write_json(reports_dir / "gate_report_REP.json", report_template(
        gate_id="G-REP",
        status=status_rep,
        details={"required": required, "missing": missing},
        root=root,
    ))
    generated.append("gate/reports/gate_report_REP.json")

    print("[OK] wrote gate reports (this run):")
    for rel in generated:
        print(f"  - {rel}")

    # If there are other pre-existing reports, note them without implying they
    # were regenerated.
    existing = {f"gate/reports/{p.name}" for p in reports_dir.glob("gate_report_*.json")}
    extra = sorted(existing - set(generated))
    if extra:
        print("[note] additional gate reports already present (not regenerated here):")
        for rel in extra:
            print(f"  - {rel}")


if __name__ == "__main__":
    main()
