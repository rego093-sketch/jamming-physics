#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schizophrenia_forbidden_claim_scan.py  —  the discipline guard (fail-closed). Inherited from analgesic
v2.0 M5 via the bipolar/epilepsy/depression T-L scanners.

Scans the ASSERTED claims of the schizophrenia three-lever map + the burden prioritisation for FORBIDDEN
claim classes (dosing / synthesis / efficacy-as-fact / safety-as-fact). If any is found, the build fails
closed. This mechanically prevents the map from drifting from a TARGET-DIRECTION hypothesis into a
treatment / drug / efficacy claim -- which matters ACUTELY here because the antipsychotic literature
(the typical D2 antagonists, the atypicals, clozapine, the D2/D3 partial agonists, and the emerging
glutamatergic/muscarinic agents) is saturated with efficacy / "remission" / "relapse-prevention" /
"treats psychosis" language that must never leak into the asserted map. Schizophrenia is a YMYL ("your
money or your life") topic; the discipline here is tighter than any prior T-L chapter.

What is SCANNED (positive assertions only):
  - schizophrenia_threshold_levers_results.json   (agent direction, anchors, frame text, entries)
  - schizophrenia_burden_prioritisation.json       (the ranking rows + reading)
What is NOT scanned (checked for PRESENCE instead -- these LEGITIMATELY contain negated forbidden
words like "not a dose", "efficacy=0", "NOT efficacy"):
  - any key matching  firewall | *grade* | principle | honesty | primitive | unifying_frame |
    disorder_level_sign | *_direction
Two defences against firewall false-positives:
  (1) firewall/grade/honesty keys are excluded from the scanned text;
  (2) a NEGATION GUARD suppresses DOSING/SYNTHESIS matches immediately preceded by
      no/not/without/never/non/nor (so a stray "not a dose" never fires). NOT applied to
      SAFETY/EFFICACY because "no side effects" IS itself a forbidden safety claim.
NOTE: the bare word "antipsychotic" is DESCRIPTIVE (the D2-antagonist axis) and is NOT forbidden; only
efficacy-as-fact phrasings ("antipsychotic efficacy", "treats psychosis", "prevents relapse", "remission",
"psychosis-free", "relapse prevention") are scanned.
Self-test: a planted positive proves the scanner fires; a guard-probe proves the negation guard works.

Run:  python3 schizophrenia_forbidden_claim_scan.py  -> schizophrenia_claim_scan.json ; exit 1 on violation
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))

SCAN_FILES = ["schizophrenia_threshold_levers_results.json", "schizophrenia_burden_prioritisation.json"]

PATTERNS = {
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdosage\b", r"\bdose[sd]?\b",
               r"\btwice\s+daily\b", r"\bonce\s+daily\b", r"\b[bt]id\b", r"\bqd\b",
               r"\bmilligram", r"\bper\s+kg\b", r"\bserum\s+level\b", r"\btrough\s+level\b",
               r"\bplasma\s+level\b"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux",
                  r"\bmmol\b", r"\breaction\s+mixture\b", r"\bchromatograph", r"\bsynthetic\s+route\b"],
    "EFFICACY_AS_FACT": [r"\bcures\b", r"\bwill\s+cure\b", r"\btreats?\s+patients?\b",
                         r"\bproven\s+to\s+(relieve|prevent|treat|resolve)\b", r"\bguarantee",
                         r"\bis\s+effective\s+in\s+patients\b",
                         # schizophrenia-specific efficacy-as-fact:
                         r"\bcures?\s+(schizophrenia|psychosis)\b", r"\btreats?\s+(schizophrenia|psychosis)\b",
                         r"\b(relieves?|resolves?|eliminates?|abolishes?)\s+(psychosis|symptoms?|delusions?|hallucinations?)\b",
                         r"\bprevents?\s+relapse\b", r"\brelapse[-\s]?prevention\b",
                         r"\b(achieves?|induces?|produces?|maintains?)\s+remission\b", r"\bremission\b",
                         r"\bpsychosis[-\s]?free\b", r"\bsymptom[-\s]?free\b",
                         r"\bantipsychotic\s+efficacy\b", r"\bantipsychotic\s+effect\b",
                         r"\bis\s+antipsychotic\b", r"\bimproves?\s+(psychosis|schizophrenia)\b",
                         r"\brestores?\s+(insight|reality\s+testing)\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}
NEGATION_GUARDED = {"DOSING", "SYNTHESIS"}
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor)\b(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$", re.I)
EXCLUDE_KEY_RE = re.compile(r"(firewall|grade|principle|honesty|^primitive$|^unifying_frame$|"
                            r"^disorder_level_sign$|_direction$)", re.I)

def _negated(text, start):
    return bool(NEG_RE.search(text[max(0, start-24):start]))

def scan(text, where):
    hits = []
    for cls, pats in PATTERNS.items():
        for p in pats:
            for mt in re.finditer(p, text, flags=re.I):
                if cls in NEGATION_GUARDED and _negated(text, mt.start()):
                    continue
                hits.append({"class": cls, "match": mt.group(0), "where": where,
                             "ctx": text[max(0, mt.start()-40):mt.end()+40].replace("\n", " ")})
    return hits

def _collect(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if EXCLUDE_KEY_RE.search(str(k)):
                continue
            _collect(v, out)
    elif isinstance(obj, list):
        for v in obj: _collect(v, out)
    elif isinstance(obj, str):
        out.append(obj)

def file_text(fn):
    p = os.path.join(HERE, fn)
    if not os.path.exists(p): return None
    out = []; _collect(json.load(open(p)), out); return "  ".join(out)

def _has_firewall(fn):
    p = os.path.join(HERE, fn)
    if not os.path.exists(p): return False
    txt = open(p, encoding="utf-8").read()
    return bool(re.search(r'"(firewall|principle|honesty)"\s*:\s*"[^"]+', txt)
                or re.search(r'"[a-z_]*grade[a-z_]*"\s*:\s*"[^"]+', txt))

if __name__ == "__main__":
    real, scanned, missing_fw = [], [], []
    for fn in SCAN_FILES:
        txt = file_text(fn)
        if txt is None: continue
        scanned.append(fn)
        real += scan(txt, fn)
        if not _has_firewall(fn): missing_fw.append(fn)

    planted = ("Give haloperidol 5 mg twice daily; this cures schizophrenia, treats psychosis, achieves "
               "remission, prevents relapse, is antipsychotic and has no side effects.")
    selftest = scan(planted, "selftest"); selftest_ok = len(selftest) >= 3
    guard_probe = "This is not a dose and we do not synthesise any compound."
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_fw and selftest_ok and guard_ok and len(scanned) >= 1)
    result = {"inherited_from": "analgesic_threshold_logic v2.0 M5 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression T-L",
              "real_violations": real, "missing_firewalls": missing_fw, "scanned_files": scanned,
              "selftest_fired": selftest_ok, "selftest_hit_classes": sorted({h["class"] for h in selftest}),
              "negation_guard_ok": guard_ok, "overall": "PASS" if ok else "FAIL"}
    json.dump(result, open(os.path.join(HERE, "schizophrenia_claim_scan.json"), "w"), indent=1)

    print("forbidden-claim scan (schizophrenia)")
    print(f"  scanned: {scanned}")
    print(f"  self-test fired on planted violation: {selftest_ok} {result['selftest_hit_classes']}")
    print(f"  negation-guard suppresses disclaimer DOSING/SYNTHESIS: {guard_ok}")
    if real:
        print(f"  [FAIL] {len(real)} forbidden claim(s):")
        for h in real[:20]:
            print(f"    - {h['class']}: '{h['match']}'  @{h['where']}  ...{h['ctx']}...")
        sys.exit(1)
    if missing_fw: print(f"  [FAIL] file(s) missing firewall/grade field: {missing_fw}"); sys.exit(1)
    if not selftest_ok: print("  [FAIL] scanner self-test did not fire"); sys.exit(1)
    if not guard_ok: print("  [FAIL] negation guard broken"); sys.exit(1)
    print("  [PASS] no forbidden claims; firewalls present; guards live")
    print("OVERALL: PASS")
