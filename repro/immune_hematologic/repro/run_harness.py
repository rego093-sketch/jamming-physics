#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_harness.py  --  out-of-gate runner for the LIVE CROSS-PACKAGE HARNESS (section 17).

Loads this immune volume together with its sibling VP volumes (digestive, mind) in one process and prints
the live cross-volume identities. Runs OUTSIDE every gate: it computes nothing the research gate or the
canonical build depend on, and it SKIPS cleanly (exit 0) when the siblings are not on disk -- it can never
break a sibling-free build. With the siblings present, it confirms what the seam layer (section 16) trusts:

  (1) shared substrate drift 0 across immune <-> digestive <-> mind,
  (2) the gut-immune latch identity (digestive's LIVE IBD == this volume's T23/T24 saddle-node),
  (3) the neuro-immune endpoint (mind names the HPA/cortisol IN term and the inflammatory OUT term).

The harness digest (the immune-side contract only) is byte-identical with or without the siblings.
"""
import os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "_harness"))

import cross_package_harness as H


def main():
    print("=" * 78)
    print("LIVE CROSS-PACKAGE HARNESS  --  immune_hematologic_vp_site  (section 17, out of gate)")
    print("=" * 78)

    # self-discipline (not hashed): the harness's own files contain zero sibling import statements
    disc = H.self_no_sibling_imports()
    print("self no-sibling-import discipline:", "OK" if disc["file_path_load_discipline_ok"] else "VIOLATION",
          "(%d import statements flagged)" % disc["sibling_import_statements"])

    # the hashed immune-side contract (sibling-free)
    s, h = H.digest()
    print("immune-side contract sha256:", h, "(byte-identical with or without siblings)")
    contract = H.immune_side_contract()
    print("  shared-substrate closed-form identity ok:", contract["shared_substrate"]["closed_form_identity_ok"])
    gi = contract["gut_saddle_node_identity"]
    print("  gut saddle-node identity (vs vendored): induction match",
          gi["induction_matches_vendored"], "| maintenance match", gi["maintenance_matches_vendored"])

    found = H.discover_siblings()
    print("\nsiblings discovered:", {k: (os.path.basename(v) if v else None) for k, v in found.items()})

    if not any(found.values()):
        print("\nNo sibling packages discovered -> LIVE checks SKIPPED. The build and the research gate")
        print("are unaffected (the immune-side contract above is the only hashed object). Exit 0.")
        return 0

    res = H.live_check(found)
    print("\n--- LIVE cross-volume checks ---")
    for name, chk in res["checks"].items():
        verdict = chk.get("passed", chk.get("drift_is_zero"))
        print("  [%s] %s" % ("PASS" if verdict else "----", name))
        for k, v in chk.items():
            if k in ("passed", "drift_is_zero"):
                continue
            print("        %s: %s" % (k, v))

    print("\nALL LIVE PASSED:", res["all_live_passed"])
    return 0 if res["all_live_passed"] or not res["any_sibling_present"] else 1


if __name__ == "__main__":
    sys.exit(main())
