#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
honesty_gate.py  --  the fail-closed discipline guard (generalises analgesic M5/M6).

Two gates over every disease-emergence + treatment artifact:

  GATE 1  forbidden-claim scan.  The pipeline reads promoter switch-threshold STRUCTURE
          and proposes DIRECTIONS. It must NEVER assert a clinical magnitude. This gate
          fails closed if any emitted JSON contains a derived binding affinity, potency,
          dose, efficacy/cure claim, or any "treat this person" instruction. It also
          requires every artifact to carry a firewall string and honest grades.

  GATE 2  falsifier register.  A proposal you cannot kill is not science. Every disease
          analysis must carry >= 1 NAMED, MEASURABLE falsifier -- an experiment whose
          result would refute the emergence/treatment-direction claim.

Both gates run on the FROZEN artifacts produced by the pipeline, so the discipline is
checked on the actual bytes shipped, not on intentions.

Deterministic. stdlib only.
"""
import os, sys, json, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

# patterns that, if a derived NUMBER sits next to them, would over-claim a clinical magnitude.
FORBIDDEN_NUMERIC = [
    r"\b\d+(\.\d+)?\s*(nm|um|µm|mm|pm)\s*(kd|ki|ic50|ec50)\b",
    r"\b(kd|ki|ic50|ec50)\s*(=|of|:)\s*\d",
    r"\b\d+(\.\d+)?\s*(mg|mcg|µg|ug)\s*(/kg|per kg|dose|daily|bid|tid)\b",
    r"\bcure(s|d)?\s+(in|after|within)\s+\d",
    r"\b\d+(\.\d+)?\s*%\s*(efficacy|response|remission|cure)\b",
    r"\b\d+(\.\d+)?\s*(mv|millivolt)\b.*\b(clinic|patient|in vivo)\b",
]
# bare phrases that over-claim regardless of a number nearby.
FORBIDDEN_PHRASE = [
    r"\bguaranteed\b", r"\bwill cure\b", r"\bcures the disease\b",
    r"\bproven cure\b", r"\bmiracle\b", r"\bno side effects\b",
    r"\bsafe and effective\b", r"\bprescribe\b.*\bpatient\b",
    r"\byou should take\b", r"\bdiagnos(e|is) yourself\b",
]
REQUIRE_FIREWALL = True
REQUIRE_GRADE_TOKENS = ["[O]"]      # every analysis must disclose at least one open item


def _walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_strings(v)


def scan_forbidden(artifact):
    text = " ".join(_walk_strings(artifact)).lower()
    hits = []
    for pat in FORBIDDEN_NUMERIC + FORBIDDEN_PHRASE:
        for m in re.finditer(pat, text):
            hits.append({"pattern": pat, "match": m.group(0)[:80]})
    has_firewall = "firewall" in json.dumps(artifact).lower()
    has_open = any(tok.lower() in text for tok in [t.lower() for t in REQUIRE_GRADE_TOKENS])
    return {"forbidden_hits": hits, "has_firewall": has_firewall, "discloses_open": has_open}


def gate_forbidden(artifacts):
    results, ok = {}, True
    for name, art in artifacts.items():
        s = scan_forbidden(art)
        clean = (len(s["forbidden_hits"]) == 0
                 and (s["has_firewall"] or not REQUIRE_FIREWALL)
                 and s["discloses_open"])
        results[name] = {**s, "PASS": clean}
        ok = ok and clean
    return {"gate": "forbidden-claim scan", "PASS": ok, "per_artifact": results}


def gate_falsifiers(falsifier_register):
    """falsifier_register: {disease: [ {claim, falsifier, measurable_by}, ... ] }"""
    results, ok = {}, True
    for disease, fs in falsifier_register.items():
        good = bool(fs) and all(f.get("claim") and f.get("falsifier") and f.get("measurable_by")
                                for f in fs)
        results[disease] = {"n_falsifiers": len(fs), "PASS": good}
        ok = ok and good
    return {"gate": "falsifier register (>=1 measurable falsifier per disease)",
            "PASS": ok, "per_disease": results}


def run_gates(artifacts, falsifier_register):
    g1 = gate_forbidden(artifacts)
    g2 = gate_falsifiers(falsifier_register)
    overall = g1["PASS"] and g2["PASS"]
    out = {"OVERALL": "PASS" if overall else "FAIL", "gate_forbidden": g1, "gate_falsifiers": g2}
    out["determinism_sha"] = hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()[:12]
    return out


if __name__ == "__main__":
    # self-test: a clean artifact passes; a dirty one fails closed.
    clean = {"disease": "demo", "firewall": "structure only; not dose/potency",
             "grade": "[O] magnitude open", "direction": "UP"}
    dirty = {"disease": "bad", "claim": "Kd = 3 nM, cures the disease in 2 weeks, guaranteed"}
    fr = {"demo": [{"claim": "FGFR3 GOF lowers growth dwell",
                    "falsifier": "a GOF allele that RAISES limb length refutes the brake direction",
                    "measurable_by": "growth-plate chondrocyte proliferation assay / limb-length cohort"}]}
    res = run_gates({"clean": clean, "dirty": dirty}, fr)
    print(json.dumps(res, indent=1))
    print("\nEXPECT: dirty FAILs forbidden scan; clean PASSes; falsifier gate PASSes.")
