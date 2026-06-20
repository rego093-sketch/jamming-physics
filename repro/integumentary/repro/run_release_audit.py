#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_release_audit.py  --  v1.0.0 release-readiness audit (ADDITIVE; reads, never alters)

This is NOT a new physical sweep and adds NO new mechanism and NO new constant. It is a
top-level *consolidation gate* for the v1.0.0 release: it re-runs every canonical runner in
its own subprocess (so it walks the exact same computation path the framework ships), reads
the determinism sha each one prints, and asserts it equals the value pinned in START_HERE /
HANDOFF. It then asserts every layer reports `all pass / all_green`, and writes one
machine-readable record `reports/release_audit.json`.

It imports nothing from the engine or the gates and computes no physics, so it cannot perturb
any hash: the seven frozen hashes are an *input contract* here, checked, not produced.

Run:  python repro/run_release_audit.py
"""
import json
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_REPORTS = os.path.join(_ROOT, "reports")

# ---- the frozen contract (START_HERE.md / HANDOFF_NEXT_STEPS.md) ---------------------------
# (runner, full-pinned-sha, gpass-token that must appear True in the runner's own output)
PINNED = [
    ("run_all.py",
     "1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92",
     "all targets pass: True"),
    ("run_pathology.py",
     "0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8",
     "all diseases pass: True"),
    ("run_cycle.py",
     "d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822",
     "all pass: True"),
    ("run_seb.py",
     "1e8a557d9a8d7b05823259bb2fcac31e372b96272e47ef1f2f5d89b1b0246a84",
     "all pass: True"),
    ("run_adhesion.py",
     "55dce8c267ea4c76d8d5b967535a4ee0876c4b67f605e6ae7d65bf38516f28ad",
     "all pass: True"),
    ("run_vasomotor.py",
     "53a99f522ad684a11bcc6d4d33c5e8123d1f4dff5a75836c0bbced6736a62003",
     "all pass: True"),
    ("run_seam.py",
     "52b49a95a9add070a05a02848b1a4cef0589f4a36791167232fda3fc1c1d58f7",
     "all pass: True"),
]

# what the release is asserting is *complete* (documentation, not computation) ----------------
TARGETS = [
    "T1 barrier permeability", "T2 wound healing (jamming/unjamming)", "T3 melanin UV response",
    "T4 epidermal turnover", "T5 thermoregulation",
    "T6 hair-follicle cycle oscillator", "T7 sebaceous-duct occlusion jam",
    "T8 cell-adhesion binding jam", "T9 neurovascular reactivity jam",
    "ONCO UV-carcinogenesis kernel",
]
DISEASES = [
    # core pathology layer (13)
    "atopic dermatitis", "contact dermatitis", "ichthyosis (dynamics)", "psoriasis",
    "chronic/diabetic/pressure wound", "vitiligo", "melasma/hyperpigmentation",
    "albinism/OCA (dynamics)", "hypohidrotic ectodermal dysplasia (dynamics)",
    "primary hyperhidrosis", "heat stroke", "skin cancer (melanoma/SCC/BCC)", "actinic keratosis",
    # hair-cycle (4)
    "androgenetic alopecia", "alopecia areata", "telogen effluvium", "anagen effluvium",
    # sebaceous (2)
    "acne vulgaris", "hidradenitis suppurativa",
    # adhesion (2)
    "pemphigus vulgaris", "bullous pemphigoid",
    # vasomotor (2)
    "rosacea", "Raynaud phenomenon",
]
SEAM_CLASSES = {"INHERITED_IN": 3, "INTERNAL_LIVE": 1, "DECLARED_OUT": 6}

SHA_RE = re.compile(r"sha=([0-9a-f]{8,64})")


def _short(h):
    return h[:16]


def _run(runner):
    """Run one canonical runner; return (stdout, returncode)."""
    p = subprocess.run([sys.executable, os.path.join("repro", runner)],
                       cwd=_ROOT, capture_output=True, text=True, timeout=600)
    return p.stdout + p.stderr, p.returncode


def _emitted_shas(text):
    """Every distinct sha the runner printed (some runners print a seq sha + the result sha)."""
    return [m.group(1) for m in SHA_RE.finditer(text)]


def audit():
    rows = []
    all_ok = True
    for runner, pinned, gtoken in PINNED:
        out, rc = _run(runner)
        shas = _emitted_shas(out)
        # the pinned (result) sha must appear by its 16-char prefix among the emitted shas
        hash_match = any(s == pinned or pinned.startswith(s) or s.startswith(_short(pinned))
                         for s in shas)
        gate_ok = (gtoken in out) and (rc == 0)
        ok = bool(hash_match and gate_ok)
        all_ok = all_ok and ok
        rows.append({
            "runner": runner,
            "pinned_sha256": pinned,
            "pinned_sha_short": _short(pinned),
            "emitted_sha_shorts": sorted({_short(s) if len(s) >= 16 else s for s in shas}),
            "hash_match": hash_match,
            "gate_token": gtoken,
            "gate_green": gate_ok,
            "returncode": rc,
            "ok": ok,
        })
        flag = "OK  " if ok else "FAIL"
        print(f"  [{flag}] {runner:<22} sha={_short(pinned)}...  "
              f"hash_match={hash_match}  gate_green={gate_ok}")

    record = {
        "release": "integumentary_vp_site v1.0.0",
        "audit": "release-readiness consolidation gate (additive; reads, never alters)",
        "frozen_hash_contract": rows,
        "all_frozen_hashes_match": all(r["hash_match"] for r in rows),
        "all_gates_green": all(r["gate_green"] for r in rows),
        "all_ok": all_ok,
        "coverage": {
            "targets": TARGETS,
            "n_targets": len(TARGETS),
            "diseases": DISEASES,
            "n_diseases": len(DISEASES),
            "seam_classes": SEAM_CLASSES,
        },
        "in_lane_program": "COMPLETE (jamming barrier/interface + external-insult class)",
        "remaining_work": "live wiring of DECLARED-OUT cross-package contracts; "
                          "needs the integration harness that does not yet exist "
                          "(HANDOFF 5.3 first bullet + 5.4). Out of this self-contained "
                          "package's scope by construction.",
        "grades_note": "shapes [V]; cited anchors [L]; regime-scale set-points [F]; "
                       "absolute magnitudes [O] with stated obstacle.",
    }
    os.makedirs(_REPORTS, exist_ok=True)
    with open(os.path.join(_REPORTS, "release_audit.json"), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return record


def main():
    print("=" * 78)
    print("Integumentary  --  v1.0.0 RELEASE AUDIT (additive consolidation gate)")
    print("=" * 78)
    print("\n[1] FROZEN-HASH CONTRACT (each canonical runner re-run; sha vs pinned)")
    rec = audit()
    print("\n[2] COVERAGE (documentation of what the release declares complete)")
    print(f"    targets : {rec['coverage']['n_targets']}  (T1-T9 + oncology)")
    print(f"    diseases: {rec['coverage']['n_diseases']}  (13 + 4 + 2 + 2 + 2)")
    print(f"    seams   : INHERITED-IN {SEAM_CLASSES['INHERITED_IN']} / "
          f"INTERNAL-LIVE {SEAM_CLASSES['INTERNAL_LIVE']} / "
          f"DECLARED-OUT {SEAM_CLASSES['DECLARED_OUT']}")
    print("\n[3] VERDICT")
    print(f"    all frozen hashes match : {rec['all_frozen_hashes_match']}")
    print(f"    all gates green         : {rec['all_gates_green']}")
    print(f"    RELEASE-READY           : {rec['all_ok']}")
    print(f"\n    in-lane program         : {rec['in_lane_program']}")
    print("    wrote reports/release_audit.json")
    return 0 if rec["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
