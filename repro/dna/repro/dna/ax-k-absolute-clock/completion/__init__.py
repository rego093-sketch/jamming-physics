# -*- coding: utf-8 -*-
"""
Appendix K -- the absolute clock (pinning the global zero-point).

Closes the ONE channel Appendix J left open (B1), with REAL DATA and no tuning:
  B1  pin the cascade's developmental ORDER to absolute DAYS with ONE global zero-point, from TWO
      INDEPENDENT measured anchors -- the in-vitro segmentation oscillator (the SLOPE) and the
      in-vivo first-heartbeat landmark (the INTERCEPT) -- via a parameter-free linear calibration,
      validated OUT-OF-SAMPLE on held-out Carnegie stage-days and gene-days. [O] -> [L], never [V].

Everything else (the 63-gene atlas, the DAG/wavefront/order results, O1 floor, O2 sub-clock, O3
sequence-drive, the quorum/AND gate) is inherited from Appendix J and RE-AUDITED byte-for-byte.

ADD-ONLY over Appendices A-J: every prior page, number, grade, equation and DOI is unchanged.
"""
from . import (seqtools, lock, cascade, coupled, timing, nulltest, grammar,
               declaration, grading, interpreter, gate)  # noqa: F401,E402

__all__ = ["seqtools", "lock", "cascade", "coupled", "timing", "nulltest",
           "grammar", "declaration", "grading", "interpreter", "gate"]
