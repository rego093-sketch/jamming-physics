#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gates.py  --  Cardiorespiratory research/writing PHASE gate (VP-SPEC C1/C3 + research-first rule).

research_gate()   -- determinism (2x sha256 identical) + emergence runs + stress battery all PASS.
writing_locked()  -- True UNLESS PHASE=="writing" AND reports/research_complete.json all_green=true.
                     tools/build_docs.py refuses while True. Call write_research_complete() only when
                     run_battery() is genuinely green. This enforces "research first, then write".
"""
import os, sys, json
_HERE = os.path.dirname(__file__)
_PKG  = os.path.join(_HERE, "..", "..")
_REPORTS = os.path.join(_PKG, "reports")
_PHASE   = os.path.join(_PKG, "PHASE")
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "_oncology"))
sys.path.insert(0, os.path.join(_HERE, "..", "_disease"))
import importlib
eng = importlib.import_module("vp_car_engine")
stress = importlib.import_module("stress_tests") if os.path.exists(os.path.join(_HERE, "stress_tests.py")) else None

def determinism_ok():
    _, h1 = eng.emit(eng.circulate()); _, h2 = eng.emit(eng.circulate())
    return h1 == h2, h1

def research_gate():
    det, h = determinism_ok()
    batt = stress.run_battery() if stress else {"all_targets_pass": False, "emergence_ok": False}
    green = bool(det and batt.get("emergence_ok") and batt.get("all_targets_pass"))
    return {"determinism_2xsha256_identical": det, "result_sha256": h,
            "emergence_ok": batt.get("emergence_ok"), "stress_all_targets_pass": batt.get("all_targets_pass"),
            "all_green": green}

def read_phase():
    try: return open(_PHASE, encoding="utf-8").read().strip()
    except FileNotFoundError: return "research"

def writing_locked():
    if read_phase() != "writing": return True, "PHASE != writing"
    rc = os.path.join(_REPORTS, "research_complete.json")
    if not os.path.exists(rc): return True, "reports/research_complete.json absent (research not signed off)"
    try:
        if not json.load(open(rc, encoding="utf-8")).get("all_green"):
            return True, "research_complete.json present but all_green != true"
    except Exception as e:
        return True, "research_complete.json unreadable: " + str(e)
    return False, "writing unlocked"

def write_research_complete():
    g = research_gate(); os.makedirs(_REPORTS, exist_ok=True)
    json.dump(g, open(os.path.join(_REPORTS, "research_complete.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return g

def _canonical_blob():
    """Deterministic union of every report-producing computation, as sorted-key JSON."""
    parts = {}
    raw, sha = eng.emit(eng.circulate())
    parts["engine_sha"] = sha
    parts["engine"] = json.loads(raw)
    if stress:
        parts["stress"] = stress.run_battery()
    try:
        onc = importlib.import_module("carcinogen_dose_response"); parts["onco"] = onc.results()
    except Exception:
        pass
    try:
        dis = importlib.import_module("disease_battery"); parts["disease"] = dis.run_battery()
    except Exception:
        pass
    return json.dumps(parts, sort_keys=True, ensure_ascii=False)


def drift_ok():
    """Recompute the full canonical result blob twice; bytes must be identical (drift 0)."""
    import hashlib
    a = _canonical_blob(); b = _canonical_blob()
    ha = hashlib.sha256(a.encode("utf-8")).hexdigest()
    hb = hashlib.sha256(b.encode("utf-8")).hexdigest()
    return {"ok": ha == hb, "blob_sha256": ha, "second_sha256": hb}


def offline_ok():
    """Prove no network dependency: disable socket.socket, then reproduce the engine + battery."""
    import socket
    saved = socket.socket
    def _no_net(*a, **k):
        raise OSError("network disabled for offline reproducibility proof")
    socket.socket = _no_net
    try:
        _raw, sha = eng.emit(eng.circulate())
        ok = bool(sha)
        if stress:
            ok = ok and bool(stress.run_battery().get("all_targets_pass"))
        return {"ok": ok, "note": "engine + stress battery reproduce with socket.socket disabled"}
    except Exception as ex:
        return {"ok": False, "note": "offline proof FAILED: %r" % ex}
    finally:
        socket.socket = saved


if __name__ == "__main__":
    print("research_gate:", json.dumps(research_gate(), ensure_ascii=False, indent=2))
    print("writing_locked:", writing_locked())
