"""Gate logic for the jet_regime reference stub."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Optional

from estimators import JetMetrics

GateStatus = Literal["PASS", "FAIL", "INCONCLUSIVE"]


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    status: GateStatus
    metrics: Dict[str, float]
    thresholds: Dict[str, float]
    fail_code: Optional[str] = None


def gate_jet1(metrics: JetMetrics, J_star: float = 0.65) -> GateResult:
    status: GateStatus = "PASS" if (metrics.J >= J_star) else "FAIL"
    return GateResult(
        gate_id="G-JET1",
        status=status,
        metrics={"J": metrics.J},
        thresholds={"J_star": J_star},
        fail_code=None if status=="PASS" else "F-JET-COLLIMATION",
    )


def gate_jet2(metrics: JetMetrics, P_star: float = 0.6) -> GateResult:
    status: GateStatus = "PASS" if (metrics.P_J >= P_star) else "FAIL"
    return GateResult(
        gate_id="G-JET2",
        status=status,
        metrics={"P_J": metrics.P_J},
        thresholds={"P_star": P_star},
        fail_code=None if status=="PASS" else "F-JET-STREAM",
    )


def gate_log() -> GateResult:
    return GateResult(gate_id="G-LOG", status="PASS", metrics={}, thresholds={}, fail_code=None)


def gate_rep() -> GateResult:
    return GateResult(gate_id="G-REP", status="PASS", metrics={}, thresholds={}, fail_code=None)


def run_all_gates(metrics: JetMetrics, J_star: float, P_star: float) -> Dict[str, GateResult]:
    return {
        "G-JET1": gate_jet1(metrics, J_star=J_star),
        "G-JET2": gate_jet2(metrics, P_star=P_star),
        "G-LOG": gate_log(),
        "G-REP": gate_rep(),
    }
