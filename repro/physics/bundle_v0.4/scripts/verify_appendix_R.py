#!/usr/bin/env python3
"""Deterministic verifier for Appendix R (lattice tension → absolute force).

This file exists because the whitepaper TeX embeds it as a named artifact.

It performs two roles:
  (1) Pure-LOCK computation of the Appendix R chain:
      F_lat, lambda_C, S_p, coupling factors, and F_VP(r_p).
  (2) A *comparison-only* calculation of the Coulomb force between ±e at
      separation r_p (for target-text comparison only).

Outputs a JSON object to stdout (and optionally to --write).
All numeric values are stored as decimal strings.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Dict

getcontext().prec = 120


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def d(x: Any) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def dstr(x: Decimal) -> str:
    return str(x)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", default="", help="Optional output path for the JSON log")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]

    canon = read_json(root / "registry" / "canon_lock.json")
    realz = read_json(root / "registry" / "realization_lock.json")

    # [LOCK] constants
    pi = d(canon["constants"]["pi"])
    h = d(canon["constants"].get("h_J_s") or canon["constants"].get("h_Js") or "6.62607015e-34")
    c_ref = d(realz["inputs"]["c_ref_m_s"])
    a_m = d(realz["inputs"]["a_m"])
    r_p = d(canon["inputs"]["r_p_m"])

    # [DERIVED] lattice tension (Appendix R, Eq. F_lat)
    F_lat = (h * c_ref) / (a_m * a_m)

    # [DERIVED] lambda_C and S_p
    lambda_C = (pi / Decimal(2)) * r_p
    S_p = lambda_C / a_m

    # [DERIVED] coupling factors
    # universal regime: delta = 1/pi^2 -> eta_static = delta^2 = 1/pi^4
    eta_static = Decimal(1) / (pi ** 4)
    gamma_acc = Decimal(2).sqrt()  # sqrt(2)
    eta_eff = eta_static * gamma_acc
    D_cpl = eta_eff / Decimal(4)  # spherical correction 1/4

    # [DERIVED] absolute force at r_p
    F_vp = F_lat * (Decimal(1) / S_p) * (a_m / r_p) * D_cpl

    out: Dict[str, Any] = {
        "script": "verify_appendix_R.py",
        "scope": "Appendix R (lattice tension → absolute force)",
        "locked": {
            "pi": dstr(pi),
            "h_J_s": dstr(h),
            "c_ref_m_s": dstr(c_ref),
            "a_m": dstr(a_m),
            "r_p_m": dstr(r_p),
        },
        "derived": {
            "F_lat_N": dstr(F_lat),
            "lambda_C_m": dstr(lambda_C),
            "S_p_dimless": dstr(S_p),
            "eta_static": dstr(eta_static),
            "gamma_acc": dstr(gamma_acc),
            "eta_eff": dstr(eta_eff),
            "D_cpl": dstr(D_cpl),
            "F_VP_rp_N": dstr(F_vp),
        },
        "compare_target_text": {
            "note": "Target-text comparison only; not part of LOCK-derived chain.",
        },
    }

    # [COMPARE] Standard Coulomb force between ±e at separation r_p.
    # F = (1/(4*pi*epsilon0)) * e^2 / r_p^2
    e_C = Decimal("1.602176634e-19")
    eps0 = Decimal("8.8541878128e-12")
    k = Decimal(1) / (Decimal(4) * pi * eps0)
    F_std = k * (e_C * e_C) / (r_p * r_p)

    ratio = F_vp / F_std
    abs_rel_diff = abs(Decimal(1) - ratio)

    out["compare_target_text"].update(
        {
            "constants": {"e_C": dstr(e_C), "epsilon0_F_m": dstr(eps0)},
            "F_std_Coulomb_N": dstr(F_std),
            "ratio_FVP_over_Fstd": dstr(ratio),
            "abs_rel_diff": dstr(abs_rel_diff),
        }
    )

    text = json.dumps(out, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.write:
        Path(args.write).write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
