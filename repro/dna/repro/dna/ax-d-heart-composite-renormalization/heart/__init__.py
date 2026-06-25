# -*- coding: utf-8 -*-
"""
heart -- the HEART composite-renormalization ACCURACY package (Appendix D).

The 'challenge the heart' package: the case that 'failed' in Appendix A (the sequence
material gamma was orthogonal to developmental timing, sharpest in the heart, rho=+0.071,
p=0.882) is re-attacked with the Appendix C renormalization tower upgraded to

  (a) a real TWO-PHASE (cell + ECM/collagen) composite, with the EXACT elastic-mixture
      bounds (Voigt/Reuss/Hill) bracketing the myocardium modulus, and
  (b) MEASURED cardiac phase moduli (single-cardiomyocyte AFM, decellularized myocardial
      ECM) and a MEASURED tissue stiffening trajectory (Majkut 2013),

so an ACCURACY test becomes possible. The discovery: the heart's developmental stiffening
is a COMPOSITION + MATURATION flow (ECM collagen deposition + cell jamming), NOT the
sequence material gamma -- which is exactly why gamma was orthogonal to heart timing.

Discipline (inherited): LOCK -> Derive -> Gate; precision (정밀) != accuracy (정확);
반증 = 발견; no fitted parameters; 2x SHA-256 determinism; fail-closed gate; honest
[L]/[V]/[F]/[O] grades; completion is earned, not declared (here: False -- the heart is
mechanistically explained and bracketed, not yet quantitatively closed).

Modules:
  lock           every measured cardiac input from param_db.json; zero inline magic numbers
  composite      the exact two-phase Voigt/Reuss bracket (cell + ECM); VP wave speed
  trajectory     the measured tissue trajectory + the predicted composition-flow trajectory
  decomposition  the three parameter-free results: jamming insufficiency (falsification),
                 gamma orthogonality (explanation of the null), bracket consistency
  grading        the one place precision != accuracy; honest ledger + completion
  interpreter    interpret_heart() -- the full accuracy reading; reading_hash (2x SHA-256)
  gate           fail-closed D1..D9
"""

from . import lock, composite, trajectory, decomposition, grading, interpreter, gate

__all__ = [
    "lock", "composite", "trajectory", "decomposition",
    "grading", "interpreter", "gate",
]

__version__ = "0.1.0"
