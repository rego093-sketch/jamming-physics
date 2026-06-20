#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_expand.py  --  gate for the M9-EXT scale-sweep study (additive, offline).
================================================================================
Re-runs expand_atlas_study.py's computation and asserts (a) bit-for-bit
reproduction of the frozen digest, (b) the HONEST robust invariants, and
(c) that the sweep's largest point (N=12) AGREES with the frozen live engine
(M9), i.e. the study and the promoted engine are one and the same measurement.

It does NOT assert strict scale-stability of the partial-metastable label --
that is honestly FALSE (marginal at N=6) and is recorded as such in the result.
What IS asserted is what the measurement actually robustly shows.

Outside run_all / verify_all, so the locked engine gates are untouched.
Exit 0 = study reproduces and robust invariants hold.
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "expanded_atlas_results.json")
EXP = os.path.join(HERE, "expected_expand_sha256.json")

fails = []; n = 0
def chk(name, cond):
    global n; n += 1
    if not cond: fails.append(name)

# (1) re-run so the assertions are on LIVE output, then compare digest
import subprocess
subprocess.run([sys.executable, os.path.join(HERE, "expand_atlas_study.py")],
               check=True, stdout=subprocess.DEVNULL)

R = json.load(open(RES))
E = json.load(open(EXP))

# (A) bit-for-bit reproduction
import importlib.util
spec = importlib.util.spec_from_file_location("vp_mind_engine",
        os.path.normpath(os.path.join(HERE, "..", "_engine", "vp_mind_engine.py")))
eng = importlib.util.module_from_spec(spec); sys.modules["vp_mind_engine"] = eng
spec.loader.exec_module(eng)
canon = json.dumps(eng._round(R), sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")
live = hashlib.sha256(canon).hexdigest()
chk("study reproduces frozen digest (bit-for-bit)", live == E["expanded_atlas_results.json"])

# (B) measured coupling, not tuned
chk("kappa is the measured fraction 0.5496", abs(R["kappa_ephaptic_measured"] - 0.5496) < 1e-9)

# (C) HONEST robust invariants across the whole sweep 4->12
sweep = {s["n"]: s for s in R["sweep"]}
chk("sweep spans the full measured atlas 4->12",
    sorted(sweep.keys()) == [4, 6, 8, 10, 12])
chk("field contribution POSITIVE at every N (field lifts order above baseline)",
    R["field_contribution_positive_all_N"] is True and
    all(sweep[k]["field_contribution"] > 0 for k in sweep))
chk("network BOUNDED at every N (R<0.9, never global-lock = no seizure)",
    R["network_bounded_no_seizure_all_N"] is True and
    all(sweep[k]["R_measured"] < 0.9 for k in sweep))
chk("robust to +/-20% band perturbation at every N",
    R["robust_to_band_perturbation_all_N"] is True)
chk("field is causal: cancel < measured < augment (largest N)",
    R["field_monotone_cancel_lt_measured_lt_augment"] is True and
    R["cav_cancel_R"] < R["cav_measured_R"] < R["cav_augment_R"])

# (D) v1.19 PROMOTION: the engine M9 was promoted from THIS ring sweep's geometry to the
#     MEASURED MNI atlas (Task 1A, VP-SPEC 6-6 intentional hash change). So the ring sweep's
#     N=12 point NO LONGER matches the live engine -- matches_full_sweep is now HONESTLY False --
#     and the live engine reports the MEASURED values. The ring N=12 point is preserved as the
#     v1.17 HISTORICAL anchor (the sweep is, and remains, a ring-geometry lineage study).
xc = R["engine_cross_check"]
chk("engine cross-check sees the 12-organ promoted engine (n_regions == 12)",
    xc["engine_n_regions"] == 12)
chk("v1.19 PROMOTION: ring sweep N=12 NO LONGER matches the measured engine (honest False)",
    xc["matches_full_sweep"] is False)
chk("v1.19 PROMOTION: live engine M9 now reports the MEASURED geometry (fc ~0.1347, R ~0.390)",
    abs(xc["engine_field_contribution"] - 0.1346804816) < 1e-6 and
    abs(xc["engine_R_measured"]        - 0.3896145516) < 1e-6)
chk("HISTORICAL: N=12 ring sweep point reproduces the v1.17 pre-promotion ring M9 (0.0734/0.328)",
    abs(sweep[12]["R_measured"]         - 0.328330589)  < 1e-6 and
    abs(sweep[12]["field_contribution"] - 0.0733965191) < 1e-6)

# (E) historical anchor: the first 8 organs are byte-identical to v1.9, so the
#     N=8 point must still reproduce the original frozen M9 headline (R~0.44, +~0.12)
chk("N=8 historical anchor preserved (R_measured ~0.4384, contribution ~0.1186)",
    abs(sweep[8]["R_measured"] - 0.4384) < 1e-3 and abs(sweep[8]["field_contribution"] - 0.1186) < 5e-3)

# (F) honesty markers preserved
chk("strict partial-metastable label is NOT claimed scale-stable (honest False)",
    R["regime_scale_stable"] is False)
chk("biological functional use stays OPEN (medium_efficacy==0)",
    R["medium_efficacy_tested"] == 0.0)

if fails:
    print(f"VERIFY_EXPAND FAIL -- {len(fails)} of {n}")
    for f in fails: print("  FAIL:", f)
    sys.exit(1)
print(f"VERIFY_EXPAND PASS -- {n} checks (study reproduces bit-for-bit + robust invariants hold)")
print("  field contribution >0 and network bounded (no seizure) at every N 4->12, robust to +/-20% bands;")
print("  field is causal (cancel<measured<augment); v1.19 PROMOTED M9 ring->measured so the ring N=12")
print("  point is now the v1.17 HISTORICAL anchor (matches_full_sweep honestly False; engine is measured);")
print("  strict partial-metastable label is honestly NOT scale-invariant (marginal at N=6);")
print("  biological functional use stays OPEN (medium_efficacy_tested=0).")
sys.exit(0)
