#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_harness.py  --  LIVE cross-package harness entry point (§30), OUTSIDE every gate.

This is SEPARATE from run_all.py (the research gate). run_all.py / tools/build_docs.py never touch the
sibling packages -- this volume re-establishes its entire trusted state from its OWN archive with the
siblings absent (verify-alone). This runner is the one place the sibling engines are loaded together, to
confirm the cross-volume identities the seam (§27) and inherited-analgesic (§28) layers took on trust:

  * every volume's R19 spinodal / barrier is byte-identical (cross-volume drift 0);
  * circulatory's LIVE hepatic_clearance() reproduces the vendored hepatic snapshot (Q_H/E/F/CL_H);
  * the inherited 27-target analgesic map re-derives bit-for-bit through every volume's own spinodal;
  * the neuro peripheral nociceptor the §18 -> mind felt-symptom pointer targets exists on the shared substrate.

Place the sibling packages alongside this one (or set VP_SIBLING_CIRCULATORY / VP_SIBLING_MUSCULOSKELETAL /
VP_SIBLING_NEURO to their package roots) and run:  python repro/run_harness.py
If no sibling is discoverable the live checks are skipped and this exits 0 (a sibling-free environment is fine).
"""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "_harness"))
import cross_package_harness as H

if __name__ == "__main__":
    raise SystemExit(H.main())
