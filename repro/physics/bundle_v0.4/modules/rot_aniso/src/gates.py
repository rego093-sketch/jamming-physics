"""Gate logic for the rot_aniso reference stub.

The whitepaper defines Gate concepts at the document level. This module provides
toy implementations to demonstrate deterministic PASS/FAIL plumbing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Optional

from estimators import RotAnisoMetrics

GateStatus = Literal["PASS", "FAIL", "INCONCLUSIVE"]


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    status: GateStatus
    metrics: Dict[str, float]
    thresholds: Dict[str, float]
    fail_code: Optional[str] = None


def gate_aniso(
    metrics: RotAnisoMetrics,
    beta_g_max: float = 0.25,
    A_diff_max: float = 0.05,
) -> GateResult:
    diff = abs(metrics.A_parallel - metrics.A_perp)
    ok_beta = metrics.beta_g <= beta_g_max
    ok_diff = diff <= A_diff_max
    status: GateStatus = "PASS" if (ok_beta and ok_diff) else "FAIL"
    fail_code = None if status == "PASS" else "F-ANISO-FAIL"
    return GateResult(
        gate_id="G-ANISO",
        status=status,
        metrics={"beta_g": metrics.beta_g, "A_diff": diff},
        thresholds={"beta_g_max": beta_g_max, "A_diff_max": A_diff_max},
        fail_code=fail_code,
    )


def gate_rep() -> GateResult:
    # In this stub, deterministic replay is guaranteed by construction.
    return GateResult(
        gate_id="G-REP",
        status="PASS",
        metrics={},
        thresholds={},
        fail_code=None,
    )


def run_all_gates(metrics: RotAnisoMetrics) -> Dict[str, GateResult]:
    return {
        "G-ANISO": gate_aniso(metrics),
        "G-REP": gate_rep(),
    }
