#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
claim_scanner_v2.py  --  the hardened forbidden-claim scanner (fail-closed).  [M5 v2.0 analogue]

  *** INHERITED from analgesic_threshold_logic_v2_0  M5 v2.0 (forbidden_claim_scan.py),
      DOI 10.5281/zenodo.20733420.  The kit's pipeline/honesty_gate.py already carries analgesic
      v1.0's M5/M6 (forbidden scan + falsifier register) and is FROZEN into every analysis.json.
      This module adds the THREE v2.0 hardenings the kit lacked, WITHOUT touching honesty_gate.py
      (so the per-disease analysis.json hashes stay drift 0):

        (1) a NEGATION GUARD so firewall/disclaimer text ("not a dose", "no potency") never
            false-positives the DOSING/SYNTHESIS classes;
        (2) a SELF-TEST: a planted positive MUST fire (>=3 classes) or the scanner is declared
            broken and the build fails -- a scanner you can't see fire is not a guard;
        (3) NEW-MODULE SCOPE: it scans the assertion text of the v0.19.0 inherited modules
            (disease_priority_ranking.json + indirect_lever_honesty.json) AND the v0.24.0 native
            direction-recovery scoreboard (direction_recovery.json), exactly as analgesic M5 v2.0
            expanded to scan its own new modules (M9/M10/M11/M12), with firewall/grade/principle
            keys excluded from scanning and presence-checked instead. ***

Run:  python3 pipeline/claim_scanner_v2.py [--write]   -> exit 1 on any violation
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
MODDIR = os.path.join(ROOT, "repro", "modules", "expected")

# clinical-magnitude forbidden classes (disease-kit patterns + analgesic classes, unified)
PATTERNS = {
    # [O]-firewall concerns asserted clinical MAGNITUDE, which always carries a number / unit /
    # frequency. Bare "dose"/"dosage" are over-broad (gene dosage, dose-response window are
    # legitimate biology), so they are intentionally NOT matched alone — only quantified.
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdos(?:e|age)\s+of\s+\d",
               r"\btwice\s+daily\b", r"\bonce\s+daily\b", r"\b[bt]id\b", r"\bqd\b",
               r"\bmilligram", r"\bper\s+kg\b"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux",
                  r"\bmmol\b", r"\breaction\s+mixture\b", r"\bchromatograph", r"\bsynthetic\s+route\b",
                  r"\byield\s+\d", r"\bequiv\.\b"],
    "BINDING_MAGNITUDE": [r"\b(kd|ki|ic50|ec50)\s*(=|of|:)\s*\d",
                          r"\b\d+(\.\d+)?\s*(nm|um|µm|pm)\s*(kd|ki|ic50|ec50)\b"],
    "EFFICACY_AS_FACT": [r"\bcures\b", r"\bwill\s+cure\b", r"\bcures?\s+the\s+disease\b",
                         r"\btreats?\s+patients?\b", r"\bproven\s+cure\b", r"\bguarantee",
                         r"\beliminates?\s+the\s+disease\b",
                         r"\b\d+(\.\d+)?\s*%\s*(efficacy|response|remission|cure)\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}

# negation-guarded classes (a leading negation = disclaimer, not a claim)
NEGATION_GUARDED = {"DOSING", "SYNTHESIS"}
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor)\b(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$",
                    re.IGNORECASE)
# firewall/grade keys: not scanned, presence-checked instead
EXCLUDE_KEY_RE = re.compile(r"(firewall|grade|principle|^label$|^method$|tier_basis_cited|cite)", re.I)

NEW_MODULES = [
    ("disease_priority_ranking.json", "disease_priority_ranking"),
    ("indirect_lever_honesty.json", "indirect_lever_honesty"),
    ("direction_recovery.json", "direction_recovery"),   # NATIVE ROADMAP II-A scoreboard
    ("repurposing_hypotheses.json", "repurposing_hypotheses"),  # NATIVE ROADMAP III-A2 scanner
    ("open_directions_cards.json", "open_directions_cards"),    # NATIVE ROADMAP III-A cards
]


def _negated(text, start):
    return bool(NEG_RE.search(text[max(0, start - 24):start]))


def scan(text, where):
    hits = []
    for cls, pats in PATTERNS.items():
        for p in pats:
            for m in re.finditer(p, text, flags=re.IGNORECASE):
                if cls in NEGATION_GUARDED and _negated(text, m.start()):
                    continue
                hits.append({"class": cls, "match": m.group(0), "where": where,
                             "ctx": text[max(0, m.start()-40):m.end()+40].replace("\n", " ")})
    return hits


def _collect_assertion_strings(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if EXCLUDE_KEY_RE.search(str(k)):
                continue
            _collect_assertion_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _collect_assertion_strings(v, out)
    elif isinstance(obj, str):
        out.append(obj)


def module_text(fname):
    p = os.path.join(MODDIR, fname)
    if not os.path.exists(p):
        return None
    out = []
    _collect_assertion_strings(json.load(open(p)), out)
    return "  ".join(out)


def _has_firewall(fname):
    p = os.path.join(MODDIR, fname)
    if not os.path.exists(p):
        return False
    txt = open(p, encoding="utf-8").read()
    return bool(re.search(r'"(firewall|firewall_note|principle|grade)"\s*:\s*"[^"]+', txt)
                or re.search(r'"[a-z_]*grade[a-z_]*"\s*:\s*"[^"]+', txt))


def run():
    real, scanned, missing_fw = [], [], []
    for fname, label in NEW_MODULES:
        txt = module_text(fname)
        if txt is None:
            missing_fw.append(f"{label} (module output absent -- run prioritise/indirect first)")
            continue
        scanned.append(label)
        real += scan(txt, f"module:{label}#assertions")
        if not _has_firewall(fname):
            missing_fw.append(label)

    # (2) self-test: the scanner MUST fire on a planted violation, else it is broken
    planted = "Take 50 mg/kg twice daily; Kd = 3 nM; this cures the disease and is completely safe."
    selftest_hits = scan(planted, "selftest")
    selftest_classes = sorted({h["class"] for h in selftest_hits})
    selftest_ok = len(selftest_classes) >= 3

    # (1) negation-guard self-test: a pure disclaimer must NOT fire DOSING/SYNTHESIS
    guard_probe = ("This is not a dose and carries no dosage; we do not synthesise any compound; "
                   "no mg/kg is asserted.")
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_fw and selftest_ok and guard_ok)
    result = {
        "title": "Hardened forbidden-claim scan over the v0.19.0 inherited modules  [M5 v2.0 analogue]",
        "inherited_from": "analgesic_threshold_logic_v2_0 M5 v2.0 (forbidden_claim_scan.py); DOI 10.5281/zenodo.20733420",
        "scanned_modules": scanned,
        "real_violations": real,
        "missing_firewalls": missing_fw,
        "selftest_fired": selftest_ok,
        "selftest_hit_classes": selftest_classes,
        "negation_guard_ok": guard_ok,
        "note": ("honesty_gate.py (the frozen per-disease gate) is unchanged; this hardened scanner "
                 "adds the negation guard + self-test + new-module scope without disturbing the "
                 "drift-0 per-disease hashes."),
        "overall": "PASS" if ok else "FAIL",
    }
    return result


if __name__ == "__main__":
    res = run()
    if "--write" in sys.argv:
        json.dump(res, open(os.path.join(MODDIR, "claim_scan_v2.json"), "w"), indent=1)
        print(f"wrote {os.path.relpath(os.path.join(MODDIR, 'claim_scan_v2.json'), ROOT)}")
    print("Hardened claim scan v2.0  [inherited: analgesic M5 v2.0]")
    print(f"  scanned modules: {res['scanned_modules']}")
    print(f"  self-test fired on planted violation: {res['selftest_fired']} {res['selftest_hit_classes']}")
    print(f"  negation-guard suppresses disclaimer DOSING/SYNTHESIS: {res['negation_guard_ok']}")
    if res["real_violations"]:
        print(f"  [FAIL] {len(res['real_violations'])} forbidden claim(s):")
        for h in res["real_violations"][:20]:
            print(f"    - {h['class']}: '{h['match']}'  @{h['where']}  ...{h['ctx']}...")
    if res["missing_firewalls"]:
        print(f"  [FAIL] module(s) missing firewall/grade field or absent: {res['missing_firewalls']}")
    if not res["selftest_fired"]:
        print("  [FAIL] scanner self-test did not fire -- guard is broken")
    if not res["negation_guard_ok"]:
        print("  [FAIL] negation guard broken -- disclaimer text would false-positive")
    print("OVERALL:", res["overall"])
    sys.exit(0 if res["overall"] == "PASS" else 1)
