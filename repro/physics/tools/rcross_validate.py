#!/usr/bin/env python3
"""rcross_validate.py — RCROSS(633/532) 3-Tier Gate adjudicator, implemented from physics §11.4 (RECONSTRUCTION, 2026-09-29).

The original entry point named in the w6 provenance ledger is not in the AQD v0.4 bundle. This file implements the
adjudication rules of §11.4 verbatim:
  dev      = |dt633 - dt532| / ((dt633 + dt532)/2)                       (§11.4.3.1)
  Tier-1   = definability: required fields, lock_refs, positivity          (§11.4.4.1)
  Tier-2   = PASS iff dev <= dev_max (dev_max from gate_lock, mirrored in configs/thresholds.yaml)  (§11.4.4.2)
  Tier-3   = only if Tier-2 PASS; INCONCLUSIVE when no strengthening condition is locked               (§11.4.4.3)
  verdict  = composition of §11.4.5; labels from the §11.4.6 enumeration
Audit addition (not part of §11.4): the channel files are checked for independence. If both channels copy the
same locked value (the bundle's dt_*.txt say "Reference instance: dt := realization_lock.inputs.dt_s"), dev = 0 by
construction and the result is reported as a format check only — consistent with the §11 note of 2026-09-28.
Usage: python3 rcross_validate.py [bundle_root]   (default: ../bundle_v0.4). Deterministic; stdlib only.
"""
import hashlib, json, os, re, sys
from decimal import Decimal, getcontext
getcontext().prec = 60

root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bundle_v0.4")
reg = os.path.join(root, "registry")

def load(p):
    try: return json.load(open(p, encoding="utf-8"))
    except Exception: return None

def read_dt(p):
    if not os.path.exists(p): return None, None
    txt = open(p, encoding="utf-8").read()
    vals = [l.strip() for l in txt.splitlines() if l.strip() and not l.strip().startswith("#")]
    src = re.search(r"Reference instance:\s*(.+)", txt)
    return (Decimal(vals[0]) if vals else None), (src.group(1).strip() if src else None)

def yaml_scalar(p, key):
    if not os.path.exists(p): return None
    sec, k = key.split(".")
    cur = None
    for line in open(p, encoding="utf-8"):
        if re.match(rf"^{sec}:\s*$", line): cur = sec; continue
        if cur and re.match(r"^\S", line): cur = None
        m = re.match(rf"^\s+{k}:\s*([^\s#]+)", line)
        if cur and m: return Decimal(m.group(1))
    return None

locks = {n: load(os.path.join(reg, f"{n}_lock.json")) for n in ("canon", "realization", "analysis", "gate", "protocol")}
dt633, src633 = read_dt(os.path.join(root, "outputs", "derived", "dt_633.txt"))
dt532, src532 = read_dt(os.path.join(root, "outputs", "derived", "dt_532.txt"))
labels = []

# Tier-1
if dt633 is None or dt532 is None: labels.append("INCON-RCROSS-MISSING")
if any(v is None for v in locks.values()): labels.append("INCON-RCROSS-UNLOCK")
if dt633 is not None and dt532 is not None and (dt633 <= 0 or dt532 <= 0): labels.append("FAIL-RCROSS-NONPOS")
tier1 = "FAIL" if any(l.startswith("FAIL") for l in labels) else ("INCONCLUSIVE" if labels else "PASS")

# Tier-2
g = locks["gate"] or {}
dev_max_gate = g.get("rcross", {}).get("dev_max", g.get("tolerances", {}).get("dev_tol_max"))
dev_max_gate = Decimal(str(dev_max_gate)) if dev_max_gate is not None else None
dev_max_yaml = yaml_scalar(os.path.join(root, "configs", "thresholds.yaml"), "rcross.dev_max")
dev_max = dev_max_gate if dev_max_gate is not None else dev_max_yaml
dev = None
if tier1 == "PASS" and dev_max is not None:
    dev = abs(dt633 - dt532) / ((dt633 + dt532) / 2)
    tier2 = "PASS" if dev <= dev_max else "FAIL"
    if tier2 == "FAIL": labels.append("FAIL-RCROSS-DEV")
else:
    tier2 = "INCONCLUSIVE"

# Tier-3 (no strengthening condition locked in this bundle -> INCONCLUSIVE)
a = locks["analysis"] or {}
t3_locked = bool(a.get("rcross", {}).get("tier3")) if isinstance(a.get("rcross"), dict) else False
tier3 = ("INCONCLUSIVE" if not t3_locked else "INCONCLUSIVE") if tier2 == "PASS" else "INCONCLUSIVE"

verdict = "FAIL" if "FAIL" in (tier1, tier2, tier3) else ("PASS" if tier1 == tier2 == "PASS" and tier3 in ("PASS", "INCONCLUSIVE") else "INCONCLUSIVE")
same_source = bool(src633 and src532 and src633.split(":=")[-1].strip() == src532.split(":=")[-1].strip())
report = {"channels": ["A633", "A532"], "dt_633": str(dt633), "dt_532": str(dt532), "dev": str(dev), "dev_max": str(dev_max),
          "dev_max_gate_equals_yaml": (dev_max_gate == dev_max_yaml) if (dev_max_gate is not None and dev_max_yaml is not None) else None,
          "tier1": tier1, "tier2": tier2, "tier3": tier3, "verdict": verdict, "labels": labels,
          "audit_same_source": same_source, "audit_source": [src633, src532],
          "evidence_status": "format check only: both channels copy one locked value (dev = 0 by construction)" if same_source else "independent channels"}
txt = json.dumps(report, indent=1)
print(txt)
print("RESULT sha256 = " + hashlib.sha256(txt.encode()).hexdigest())
