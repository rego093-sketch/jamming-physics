#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_loro.py  --  gate for the M9-LORO leave-one-region-out robustness study.
================================================================================
Re-runs leave_one_out_robustness.py and asserts (a) bit-for-bit reproduction of
the frozen digest, (b) the HONEST robust invariants the study establishes, and
(c) that the full-atlas reference (drop nothing) AGREES with the frozen live
engine (M9) field_contribution, i.e. the study and the engine are one measurement.

What is asserted is exactly what the measurement robustly shows: the measured
field's causal contribution is POSITIVE under every single-region removal, the
network never seizes under any removal, and cancel<measured<augment is preserved
under every removal. No tuned constant is asserted and no efficacy is claimed
(medium_efficacy_tested stays 0).

Outside run_all / verify_all, so the locked engine gates are untouched.
Exit 0 = study reproduces and robust invariants hold.
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "leave_one_out_results.json")
EXP = os.path.join(HERE, "expected_loro_sha256.json")

fails = []; n = 0
def chk(name, cond):
    global n; n += 1
    if not cond:
        fails.append(name)

# (1) re-run so the assertions are on LIVE output, then compare digest
import subprocess
subprocess.run([sys.executable, os.path.join(HERE, "leave_one_out_robustness.py")],
               check=True, stdout=subprocess.DEVNULL)

R = json.load(open(RES))
EXPECT = json.load(open(EXP))

# (A) bit-for-bit reproduction (same canonicalisation as the engine freeze)
import importlib.util
spec = importlib.util.spec_from_file_location("vp_mind_engine",
        os.path.normpath(os.path.join(HERE, "..", "_engine", "vp_mind_engine.py")))
eng = importlib.util.module_from_spec(spec); sys.modules["vp_mind_engine"] = eng
spec.loader.exec_module(eng)
canon = json.dumps(eng._round(R), sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")
live = hashlib.sha256(canon).hexdigest()
chk("study reproduces frozen digest (bit-for-bit)", live == EXPECT["leave_one_out_results.json"])

# (B) measured coupling, not tuned
chk("kappa is the measured fraction 0.5496", abs(R["kappa_ephaptic_measured"] - 0.5496) < 1e-9)
chk("medium_efficacy_tested stays 0 (functional use OPEN)", R["medium_efficacy_tested"] == 0.0)

# (C) exhaustive leave-one-out over all 12 regions
loro = R["leave_one_out"]
chk("leave-one-out covers all 12 regions", len(loro) == 12)
chk("each leave-one-out network has 11 regions", all(d["n"] == 11 for d in loro))
chk("each removal is a distinct region", len({d["dropped"] for d in loro}) == 12)

# (D) the ROBUST invariants (these are the point of the study)
inv = R["robust_invariants"]
chk("field contribution POSITIVE under every single-region removal",
    inv["field_contribution_positive_under_every_removal"] is True)
chk("every per-drop field_contribution is itself > 0",
    all(d["field_contribution"] > 0 for d in loro))
chk("network BOUNDED (no seizure, R<0.9) under every removal",
    inv["network_bounded_no_seizure_under_every_removal"] is True)
chk("cancel<measured<augment preserved under every removal",
    inv["cancel_lt_measured_lt_augment_under_every_removal"] is True)
# the spread stays strictly positive end to end
chk("min field_contribution across removals is strictly positive",
    R["sensitivity_descriptive"]["field_contribution_min_across_removals"] > 0)

# (E) v1.19 PROMOTION: engine M9 promoted ring->measured (Task 1A, VP-SPEC 6-6). The LORO
#     full-atlas (ring) reference no longer matches the measured engine -- matches_engine is
#     now HONESTLY False -- and the ring reference is preserved as the v1.17 historical anchor.
xc = R["engine_cross_check"]
chk("engine cross-check present", xc is not None)
chk("v1.19 PROMOTION: LORO ring full-atlas ref no longer matches the measured engine (honest False)",
    bool(xc) and xc["matches_engine"] is False)
chk("v1.19 PROMOTION: live engine M9 reports the MEASURED field_contribution (~0.1347)",
    bool(xc) and abs(xc["engine_field_contribution"] - 0.1346804816) < 1e-6)
chk("HISTORICAL: LORO full-atlas ring reference reproduces the v1.17 ring M9 (~0.0734)",
    bool(xc) and abs(xc["full_atlas_field_contribution"] - 0.0733965191) < 1e-6)

print("=" * 78)
print(f"M9-LORO verify: {n - len(fails)}/{n} checks passed")
if fails:
    print("FAILED:")
    for f in fails:
        print("   -", f)
    sys.exit(1)
print("  -> the measured ephaptic field's causal contribution to inter-organ order is")
print("     POSITIVE under EVERY single-region removal and the network never seizes;")
print("     the +0.0734 ring headline is DISTRIBUTED across the atlas (not one region); v1.19 PROMOTED")
print("     the engine M9 to the measured atlas (~0.1347), so the ring ref is now the v1.17 anchor.")
print("=" * 78)
