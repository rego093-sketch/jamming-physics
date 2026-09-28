#!/usr/bin/env python3
"""Build derived artifacts from locked inputs.

Implements the whitepaper's LOCK → derived rule for the unified DOI bundle.

Inputs (SSOT):
  registry/canon_lock.json
  registry/realization_lock.json
  registry/protocol_lock.json
  registry/gate_lock.json

Outputs:
  derived/claims.json
  derived/claims.tex
  derived/tables/length_scales.csv
  derived/tables/mass_scales.csv
  derived/tables/invariants.csv
  derived/dag/dependency_dag.json

All numeric values in JSON outputs are stored as strings for cross-platform
reproducibility.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Dict, List, Tuple


getcontext().prec = 120


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def dec(x: Any) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def dstr(x: Decimal) -> str:
    # Deterministic string form.
    return str(x)


@dataclass(frozen=True)
class Locks:
    canon: Dict[str, Any]
    realz: Dict[str, Any]
    prot: Dict[str, Any]
    gate: Dict[str, Any]


def load_locks(root: Path) -> Locks:
    return Locks(
        canon=read_json(root / "registry" / "canon_lock.json"),
        realz=read_json(root / "registry" / "realization_lock.json"),
        prot=read_json(root / "registry" / "protocol_lock.json"),
        gate=read_json(root / "registry" / "gate_lock.json"),
    )


def build(root: Path) -> Dict[str, Any]:
    L = load_locks(root)

    # Deterministic created date (locked in protocol_lock)
    created_date = str(L.prot.get('created') or date.today())

    # --- locked constants ---
    pi = dec(L.canon["constants"]["pi"])
    h = dec(L.canon["constants"].get("h_J_s") or L.canon["constants"].get("h_Js"))

    D_anch_m = dec(L.canon["inputs"]["D_anch_m"])
    r_p_m = dec(L.canon["inputs"]["r_p_m"])

    a_m = dec(L.realz["inputs"]["a_m"])
    dt_s = dec(L.realz["inputs"]["dt_s"])
    c_ref_m_s = dec(L.realz["inputs"]["c_ref_m_s"])

    GeV_to_J = dec(L.prot.get("unit_conversions", {}).get("GeV_to_J") or L.prot.get("unit_conventions", {}).get("GeV_to_J"))
    fm_to_m = dec(L.prot.get("unit_conversions", {}).get("fm_to_m") or L.prot.get("unit_conventions", {}).get("fm_to_m"))

    # --- derived rectification constants (universal regime) ---
    delta = Decimal(1) / (pi * pi)
    alpha = Decimal(2) / pi

    # --- derived lengths ---
    r_e_m = (D_anch_m / Decimal(2)) * delta
    lambda_C_m = (pi / Decimal(2)) * r_p_m

    # --- derived resistances (dimensionless) ---
    S_e = r_e_m / a_m
    S_p = lambda_C_m / a_m

    # --- derived energy unit ---
    hc = h * c_ref_m_s
    U_lat_J = hc / a_m
    U_lat_GeV = U_lat_J / GeV_to_J

    # --- masses (GeV) ---
    m_H_GeV = U_lat_GeV / (Decimal(5) * pi)
    m_p_GeV = U_lat_GeV / S_p
    m_e_GeV = U_lat_GeV / S_e

    # --- invariants (Appendix M) ---
    I_H = (m_H_GeV * (Decimal(5) * pi)) / U_lat_GeV
    I_p = (m_p_GeV * S_p) / U_lat_GeV
    I_e = (m_e_GeV * S_e) / U_lat_GeV

    dev_H = abs(I_H - Decimal(1))
    dev_p = abs(I_p - Decimal(1))
    dev_e = abs(I_e - Decimal(1))
    dev_max = max(dev_H, dev_p, dev_e)

    dev_tol = dec(L.gate.get("tolerances", {}).get("dev_tol_max", L.gate.get("thresholds", {}).get("numeric_rel_tol_default", "1e-12")))

    claims: Dict[str, Any] = {
        "version": "v0.2.6",
        "created": created_date,
        "sources": {
            "canon_lock": "registry/canon_lock.json",
            "realization_lock": "registry/realization_lock.json",
            "protocol_lock": "registry/protocol_lock.json",
            "gate_lock": "registry/gate_lock.json",
        },
        "derived": {
            "pi": dstr(pi),
            "alpha": dstr(alpha),
            "delta": dstr(delta),
            "D_anch_m": dstr(D_anch_m),
            "r_p_m": dstr(r_p_m),
            "a_m": dstr(a_m),
            "dt_s": dstr(dt_s),
            "c_ref_m_s": dstr(c_ref_m_s),
            "hc_J_m": dstr(hc),
            "U_lat_J": dstr(U_lat_J),
            "U_lat_GeV": dstr(U_lat_GeV),
            "r_e_m": dstr(r_e_m),
            "r_e_fm": dstr(r_e_m / fm_to_m),
            "lambda_C_m": dstr(lambda_C_m),
            "lambda_C_fm": dstr(lambda_C_m / fm_to_m),
            "S_e_dimless": dstr(S_e),
            "S_p_dimless": dstr(S_p),
            "m_H_GeV": dstr(m_H_GeV),
            "m_p_GeV": dstr(m_p_GeV),
            "m_e_GeV": dstr(m_e_GeV),
            "m_H_J": dstr(m_H_GeV * GeV_to_J),
            "m_p_J": dstr(m_p_GeV * GeV_to_J),
            "m_e_J": dstr(m_e_GeV * GeV_to_J),
            "I_H": dstr(I_H),
            "I_p": dstr(I_p),
            "I_e": dstr(I_e),
            "dev_max": dstr(dev_max),
            "dev_tol_max": dstr(dev_tol),
        },
        "notes": [
            "All derived values are computed deterministically from registry locks.",
            "JSON stores numeric values as strings (decimal/scientific) for reproducibility.",
        ],
    }

    # --- Write outputs ---
    write_json(root / "derived" / "claims.json", claims)

    # LaTeX macro sheet (lightweight)
    tex_lines = [
        "% Auto-generated from scripts/build_derived.py",
        "% Do not edit by hand.",
        f"% created: {claims['created']}",
        "\\newcommand{\\UlatGeV}{" + str(U_lat_GeV) + "}",
        "\\newcommand{\\reFm}{" + str(r_e_m / fm_to_m) + "}",
        "\\newcommand{\\mpGeV}{" + str(m_p_GeV) + "}",
        "\\newcommand{\\meGeV}{" + str(m_e_GeV) + "}",
        "\\newcommand{\\mHGeV}{" + str(m_H_GeV) + "}",
        "",
    ]
    (root / "derived" / "claims.tex").write_text("\n".join(tex_lines), encoding="utf-8")

    # Tables
    (root / "derived" / "tables").mkdir(parents=True, exist_ok=True)

    # length_scales.csv
    with (root / "derived" / "tables" / "length_scales.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "value_m", "value_fm", "source"])
        w.writerow(["D_anch", dstr(D_anch_m), dstr(D_anch_m / fm_to_m), "canon_lock"])
        w.writerow(["r_p", dstr(r_p_m), dstr(r_p_m / fm_to_m), "canon_lock"])
        w.writerow(["lambda_C", dstr(lambda_C_m), dstr(lambda_C_m / fm_to_m), "derived"])
        w.writerow(["r_e", dstr(r_e_m), dstr(r_e_m / fm_to_m), "derived"])

    # mass_scales.csv
    with (root / "derived" / "tables" / "mass_scales.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "value_GeV", "value_J", "definition"])
        w.writerow(["U_lat", dstr(U_lat_GeV), dstr(U_lat_J), "hc/a"])
        w.writerow(["m_H", dstr(m_H_GeV), dstr(m_H_GeV * GeV_to_J), "U_lat/(5*pi)"])
        w.writerow(["m_p", dstr(m_p_GeV), dstr(m_p_GeV * GeV_to_J), "U_lat/S_p"])
        w.writerow(["m_e", dstr(m_e_GeV), dstr(m_e_GeV * GeV_to_J), "U_lat/S_e"])

    # invariants.csv
    with (root / "derived" / "tables" / "invariants.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "value", "ideal", "dev"])
        w.writerow(["I_H", dstr(I_H), "1", dstr(dev_H)])
        w.writerow(["I_p", dstr(I_p), "1", dstr(dev_p)])
        w.writerow(["I_e", dstr(I_e), "1", dstr(dev_e)])
        w.writerow(["dev_max", dstr(dev_max), "0", dstr(dev_max)])

    # dependency_dag.json (minimal)
    dag = {
        "nodes": [
            {"id": "registry/canon_lock.json", "role": "registry"},
            {"id": "registry/realization_lock.json", "role": "registry"},
            {"id": "registry/protocol_lock.json", "role": "registry"},
            {"id": "registry/gate_lock.json", "role": "registry"},
            {"id": "derived/claims.json", "role": "derived"},
            {"id": "derived/tables/length_scales.csv", "role": "derived"},
            {"id": "derived/tables/mass_scales.csv", "role": "derived"},
            {"id": "derived/tables/invariants.csv", "role": "derived"},
        ],
        "edges": [
            ["registry/canon_lock.json", "derived/claims.json"],
            ["registry/realization_lock.json", "derived/claims.json"],
            ["registry/protocol_lock.json", "derived/claims.json"],
            ["registry/gate_lock.json", "derived/claims.json"],
            ["derived/claims.json", "derived/tables/length_scales.csv"],
            ["derived/claims.json", "derived/tables/mass_scales.csv"],
            ["derived/claims.json", "derived/tables/invariants.csv"],
        ],
    }
    write_json(root / "derived" / "dag" / "dependency_dag.json", dag)

    return claims


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    claims = build(root)
    print("[OK] wrote derived artifacts:")
    print("  - derived/claims.json")
    print("  - derived/claims.tex")
    print("  - derived/tables/length_scales.csv")
    print("  - derived/tables/mass_scales.csv")
    print("  - derived/tables/invariants.csv")
    print("  - derived/dag/dependency_dag.json")
    # Print one headline value for convenience
    print(f"[INFO] U_lat_GeV = {claims['derived']['U_lat_GeV']}")


if __name__ == "__main__":
    main()
