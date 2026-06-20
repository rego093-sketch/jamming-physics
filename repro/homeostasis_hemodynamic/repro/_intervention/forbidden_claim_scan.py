#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
forbidden_claim_scan.py  --  IV-firewall gate (fail-closed). The discipline guard.

Ported verbatim-in-spirit from analgesic_threshold_logic v2.0's M5 (Zenodo concept DOI
10.5281/zenodo.20733420). Scans the ASSERTED claims of the v0.7.0 comfort-intervention layer for
FORBIDDEN claim classes. If any is found, the build fails closed. This mechanically prevents the
"comfortable, counter-regulation-free blood-pressure logic" from drifting from a STRUCTURAL target
HYPOTHESIS into a DRUG / DOSE / EFFICACY / SAFETY / TOLERABILITY claim.

The single most important rule for THIS package: a "side-effect-free" / "no side effects" / "is safe"
phrasing is itself a forbidden SAFETY claim and fails the build closed. The package may state the
STRUCTURAL prediction (a reference-reset direction provokes no counter-regulation, the proven origin
of the side-effect class) -- it may NEVER assert that any molecule is safe or side-effect-free.

SCANNED (positive assertions only):
  - comfort_proposal.json  (statement + basis of every HP proposal)
  - docs <section data-claim="comfort">    (the comfort-principle narrative)
  - docs <section data-claim="proposal">   (the proposal narrative)
  - the new module ASSERTION text:
        intervention_logic.py  -> expected/comfort_map.json
        burden_prioritisation.py -> expected/comfort_priority.json
        counterreg_honesty.py  -> expected/counterreg_honesty.json

NOT scanned (checked for PRESENCE -- firewall/grade/disclaimer fields legitimately contain negated
forbidden words like "no safety result", "[O] ... not a dose"):
  - any key matching  firewall | *grade* | principle | label | primitive | imported_from |
                      comfort_principle | cross_package_contrast | unifying_frame
  - docs <section data-claim="disclaimer">

Two defences against firewall false-positives:
  (1) firewall/grade/disclaimer keys are excluded from the scanned text;
  (2) a NEGATION GUARD suppresses DOSING/SYNTHESIS matches immediately preceded by
      no / not / without / never / non / nor. The guard is NOT applied to SAFETY/EFFICACY, because
      "no side effects" / "without side effects" ARE themselves forbidden safety claims.

Self-test: a planted positive is scanned to prove the scanner actually fires.

Run:  python3 forbidden_claim_scan.py  -> expected/comfort_claim_scan.json ; exit 1 on any violation
"""
import os, re, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))   # package root (docs/, repro/)
REPRO = os.path.join(ROOT, "repro")

PATTERNS = {
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdosage\b", r"\bdose[sd]?\b",
               r"\btwice\s+daily\b", r"\bonce\s+daily\b", r"\b[bt]id\b", r"\bqd\b",
               r"\bmilligram", r"\bper\s+kg\b"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux",
                  r"\bmmol\b", r"\breaction\s+mixture\b", r"\bchromatograph", r"\bsynthetic\s+route\b",
                  r"\byield\s+\d", r"\bequiv\.\b"],
    "EFFICACY_AS_FACT": [r"\bcures\b", r"\bwill\s+cure\b", r"\btreats?\s+patients?\b",
                         r"\bproven\s+to\s+lower\b", r"\bguarantee", r"\bis\s+effective\s+in\s+patients\b",
                         r"\bnormalises?\s+blood\s+pressure\b", r"\bcures?\s+hypertension\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b", r"\bperfectly\s+safe\b", r"\bharmless\b"],
}

# classes for which a leading negation means "disclaimer", not "claim"
NEGATION_GUARDED = {"DOSING", "SYNTHESIS"}
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor)\b(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$",
                    re.IGNORECASE)

EXCLUDE_KEY_RE = re.compile(
    r"(firewall|grade|principle|^label$|^primitive$|^imported_from$|"
    r"comfort_principle|cross_package_contrast|unifying_frame)", re.I)


def _negated(text, start):
    pre = text[max(0, start - 24):start]
    return bool(NEG_RE.search(pre))


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


# ---- comfort_proposal.json (claims vs disclaimers) -----------------------------
def claim_text():
    pj = json.load(open(os.path.join(HERE, "comfort_proposal.json")))
    parts = []
    for p in pj["proposals"]:
        parts += [p["statement"], p["basis"]]
    return "  ".join(parts)

REQUIRED_DISCLAIMERS = [
    r"\bno\s+(dose|dosage)\b",
    r"\bno\s+(synthesis|manufacturing|formulation)\b",
    r"\bno\s+(efficacy|potency|safety|tolerability)\b",
    r"\b(diagnoses|treats|cures|prevents)\b",
]

def disclaimer_text():
    pj = json.load(open(os.path.join(HERE, "comfort_proposal.json")))
    return "  ".join([pj["claim_class"]] + pj["explicit_non_claims"])

def check_disclaimers(text):
    return [pat for pat in REQUIRED_DISCLAIMERS if not re.search(pat, text, flags=re.I)]


# ---- whitepaper tagged sections ------------------------------------------------
def _html_section(tag):
    for idx in sorted(glob.glob(os.path.join(ROOT, "docs", "**", "index.html"), recursive=True)):
        html = open(idx, encoding="utf-8").read()
        m = re.search(r"<section[^>]*data-claim=['\"]" + tag + r"['\"][^>]*>(.*?)</section>",
                      html, flags=re.S | re.I)
        if m:
            return re.sub(r"<[^>]+>", " ", m.group(1))
    return None


# ---- new modules (assertion text, firewall/grade keys excluded) ----------------
NEW_MODULES = [
    ("_intervention/expected/comfort_map.json", "comfort_map.json"),
    ("_intervention/expected/comfort_priority.json", "comfort_priority.json"),
    ("_intervention/expected/counterreg_honesty.json", "counterreg_honesty.json"),
]

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

def new_module_text(relpath):
    p = os.path.join(REPRO, relpath)
    if not os.path.exists(p):
        return None
    out = []
    _collect_assertion_strings(json.load(open(p)), out)
    return "  ".join(out)

def _has_firewall(relpath):
    p = os.path.join(REPRO, relpath)
    if not os.path.exists(p):
        return False
    txt = open(p, encoding="utf-8").read()
    return bool(re.search(r'"(firewall|firewall_note|principle)"\s*:\s*"[^"]+', txt)
                or re.search(r'"[a-z_]*grade[a-z_]*"\s*:\s*"[^"]+', txt))


def run(scan_docs=True):
    real = []
    real += scan(claim_text(), "comfort_proposal.json#claims")

    sec_comfort = _html_section("comfort") if scan_docs else None
    if sec_comfort is not None:
        real += scan(sec_comfort, "docs#comfort")
    sec_prop = _html_section("proposal") if scan_docs else None
    if sec_prop is not None:
        real += scan(sec_prop, "docs#proposal")

    scanned_modules, missing_firewalls = [], []
    for relpath, label in NEW_MODULES:
        txt = new_module_text(relpath)
        if txt is None:
            continue
        scanned_modules.append(label)
        real += scan(txt, "module:%s#assertions" % label)
        if not _has_firewall(relpath):
            missing_firewalls.append(label)

    missing_disc = check_disclaimers(disclaimer_text())

    planted = "Take 50 mg twice daily; this cures hypertension and is completely safe with no side effects."
    selftest_hits = scan(planted, "selftest")
    selftest_classes = sorted({h["class"] for h in selftest_hits})
    selftest_ok = len(selftest_hits) >= 4 and "SAFETY_AS_FACT" in selftest_classes

    guard_probe = "This is not a dose and we do not synthesise any compound."
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    safety_probe = "this approach has no side effects"
    safety_hits = scan(safety_probe, "safetyprobe")
    safety_guard_ok = any(h["class"] == "SAFETY_AS_FACT" for h in safety_hits)

    ok = (not real and not missing_disc and not missing_firewalls
          and selftest_ok and guard_ok and safety_guard_ok)
    return {"real_violations": real,
            "missing_disclaimers": missing_disc,
            "missing_firewalls": missing_firewalls,
            "scanned_sections": ["comfort_proposal.json#claims"]
                                + (["docs#comfort"] if sec_comfort is not None else [])
                                + (["docs#proposal"] if sec_prop is not None else [])
                                + ["module:%s" % m for m in scanned_modules],
            "selftest_fired": selftest_ok,
            "selftest_hit_classes": selftest_classes,
            "negation_guard_ok": guard_ok,
            "safety_not_suppressed_ok": safety_guard_ok,
            "overall": "PASS" if ok else "FAIL"}


if __name__ == "__main__":
    result = run()
    real = result["real_violations"]; missing_disc = result["missing_disclaimers"]
    missing_firewalls = result["missing_firewalls"]
    selftest_ok = result["selftest_fired"]; guard_ok = result["negation_guard_ok"]
    safety_guard_ok = result["safety_not_suppressed_ok"]
    os.makedirs(os.path.join(HERE, "expected"), exist_ok=True)
    json.dump(result, open(os.path.join(HERE, "expected", "comfort_claim_scan.json"), "w"), indent=1)

    print("IV forbidden-claim scan  [comfort intervention layer]")
    print("  scanned sections: %d" % len(result["scanned_sections"]))
    print("  self-test fired on planted violation: %s %s" % (selftest_ok, result["selftest_hit_classes"]))
    print("  negation-guard suppresses disclaimer DOSING/SYNTHESIS: %s" % guard_ok)
    print("  SAFETY not negation-suppressed ('no side effects' fires): %s" % safety_guard_ok)
    if real:
        print("  [FAIL] %d forbidden claim(s):" % len(real))
        for h in real[:20]:
            print("    - %s: '%s'  @%s  ...%s..." % (h["class"], h["match"], h["where"], h["ctx"]))
        sys.exit(1)
    if missing_disc:
        print("  [FAIL] required disclaimer phrase(s) missing: %s" % missing_disc); sys.exit(1)
    if missing_firewalls:
        print("  [FAIL] module(s) missing firewall/grade field: %s" % missing_firewalls); sys.exit(1)
    if not selftest_ok:
        print("  [FAIL] scanner self-test did not fire (or missed SAFETY)"); sys.exit(1)
    if not guard_ok:
        print("  [FAIL] negation guard broken"); sys.exit(1)
    if not safety_guard_ok:
        print("  [FAIL] SAFETY guard wrongly suppressed"); sys.exit(1)
    print("  [PASS] no forbidden claims; disclaimers + firewalls present; guards live")
    print("OVERALL: PASS")
