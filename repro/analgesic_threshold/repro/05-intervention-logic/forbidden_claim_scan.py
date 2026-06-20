#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
forbidden_claim_scan.py  —  M5 gate (fail-closed). The discipline guard.  [v2.0: expanded scope]

Scans the asserted claims of the WHOLE v2.0 whitepaper for FORBIDDEN claim classes.
If any is found, the build fails closed. This is the analgesic analogue of the neuro
package's verify_em_thesis.py drift guard: it mechanically prevents the proposal from
drifting from a *target hypothesis* into a *treatment / drug / efficacy* claim.

v2.0 scope (what is SCANNED — positive assertions only):
  - proposal.json  (statement + basis of every proposal)
  - docs/index.html  <section data-claim="proposal">   (the proposal narrative)
  - docs/index.html  <section data-claim="precision">   (the local-anaesthesia narrative)
  - the new engine modules' ASSERTION text:
        03-threshold-map/expected/threshold_map.json
        10-burden-prioritisation/expected/priority_ranking.json
        11-l3-honesty/expected/l3_honesty.json
        12-precision-local-anaesthesia/expected/precision_block_map.json

What is NOT scanned (checked separately for PRESENCE — the firewall/grade/disclaimer
fields LEGITIMATELY contain negated forbidden words like "not a dose", "no potency",
"[O] ... margin, duration, dose, formulation OPEN"):
  - any key matching  firewall | *grade* | principle | label | primitive | unifying_frame
  - docs/index.html  <section data-claim="disclaimer">

Two defences against firewall false-positives:
  (1) firewall/grade/disclaimer keys are excluded from the scanned text (above);
  (2) a NEGATION GUARD suppresses DOSING/SYNTHESIS matches immediately preceded by
      no / not / without / never / non / nor  (so a stray "not a dose" never fires).
      The guard is NOT applied to SAFETY/EFFICACY, because "no side effects" /
      "without side effects" ARE themselves forbidden safety claims.

Self-test: a planted positive is scanned to prove the scanner actually fires.

Run:  python3 forbidden_claim_scan.py   -> expected/claim_scan.json ; exit 1 on any violation
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))   # package root (to find docs/, repro/)
REPRO = os.path.join(ROOT, "repro")

PATTERNS = {
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdosage\b", r"\bdose[sd]?\b",
               r"\btwice\s+daily\b", r"\bonce\s+daily\b", r"\b[bt]id\b", r"\bqd\b",
               r"\bmilligram", r"\bper\s+kg\b"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux",
                  r"\bmmol\b", r"\breaction\s+mixture\b", r"\bchromatograph", r"\bsynthetic\s+route\b",
                  r"\byield\s+\d", r"\bequiv\.\b"],
    "EFFICACY_AS_FACT": [r"\bcures\b", r"\bwill\s+cure\b", r"\btreats?\s+patients?\b",
                         r"\bproven\s+to\s+relieve\b", r"\bguarantee", r"\bis\s+effective\s+in\s+patients\b",
                         r"\beliminates?\s+pain\b", r"\bcures?\s+pain\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}

# classes for which a leading negation means "disclaimer", not "claim"
NEGATION_GUARDED = {"DOSING", "SYNTHESIS"}
# negation token, optionally followed by an article/quantifier, at the end of the preceding text:
#   "not ", "no ", "not a ", "without any ", "do not ", "never the " ...
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor)\b(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$",
                    re.IGNORECASE)

# keys whose string values are firewall / grade / disclaimer => not scanned, checked for presence
EXCLUDE_KEY_RE = re.compile(r"(firewall|grade|principle|^label$|^primitive$|^unifying_frame$)", re.I)


def _negated(text, start):
    """True if the text just before `start` ends in a negation token (+ optional article)."""
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


# ---- proposal.json (claims vs disclaimers) -------------------------------------
def claim_text():
    """ONLY the asserted claims (statement+basis). Disclaimers are checked separately."""
    pj = json.load(open(os.path.join(HERE, "proposal.json")))
    parts = []
    for p in pj["proposals"]:
        parts += [p["statement"], p["basis"]]
    return "  ".join(parts)

REQUIRED_DISCLAIMERS = [
    r"\bno\s+(dose|dosage)\b",
    r"\bno\s+(synthesis|manufacturing|formulation)\b",
    r"\bno\s+(efficacy|potency|safety)\b",
    r"\b(diagnoses|treats|cures|prevents)\b",   # appears in the negated 'nothing here ... treats/cures' line
]

def disclaimer_text():
    pj = json.load(open(os.path.join(HERE, "proposal.json")))
    return "  ".join([pj["claim_class"]] + pj["explicit_non_claims"])

def check_disclaimers(text):
    return [pat for pat in REQUIRED_DISCLAIMERS if not re.search(pat, text, flags=re.I)]


# ---- whitepaper tagged sections ------------------------------------------------
def _html_section(tag):
    """Find the first <section data-claim='tag'> across all docs/**/index.html.
    Robust to layout: works for the single-file canonical (docs/index.html) and the
    multi-page canonical (docs/analgesic/{slug}/index.html, mirroring vp_physics)."""
    import glob
    for idx in sorted(glob.glob(os.path.join(ROOT, "docs", "**", "index.html"), recursive=True)):
        html = open(idx, encoding="utf-8").read()
        m = re.search(r"<section[^>]*data-claim=['\"]" + tag + r"['\"][^>]*>(.*?)</section>",
                      html, flags=re.S | re.I)
        if m:
            return re.sub(r"<[^>]+>", " ", m.group(1))
    return None


# ---- new engine modules (assertion text, firewall/grade keys excluded) ---------
NEW_MODULES = [
    ("03-threshold-map/expected/threshold_map.json", "threshold_map.json"),
    ("10-burden-prioritisation/expected/priority_ranking.json", "priority_ranking.json"),
    ("11-l3-honesty/expected/l3_honesty.json", "l3_honesty.json"),
    ("12-precision-local-anaesthesia/expected/precision_block_map.json", "precision_block_map.json"),
]

def _collect_assertion_strings(obj, out):
    """Walk a JSON value; collect string leaves whose KEY is not a firewall/grade key."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if EXCLUDE_KEY_RE.search(str(k)):
                continue            # firewall/grade/disclaimer field -> not scanned
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
    """Each new module must carry a non-empty firewall / principle / grade field (presence check)."""
    p = os.path.join(REPRO, relpath)
    if not os.path.exists(p):
        return False
    txt = open(p, encoding="utf-8").read()
    return bool(re.search(r'"(firewall|firewall_note|principle)"\s*:\s*"[^"]+', txt)
                or re.search(r'"[a-z_]*grade[a-z_]*"\s*:\s*"[^"]+', txt))


if __name__ == "__main__":
    real = []
    real += scan(claim_text(), "proposal.json#claims")

    sec_prop = _html_section("proposal")
    if sec_prop is not None:
        real += scan(sec_prop, "docs#proposal")
    sec_prec = _html_section("precision")
    if sec_prec is not None:
        real += scan(sec_prec, "docs#precision")

    scanned_modules, missing_firewalls = [], []
    for relpath, label in NEW_MODULES:
        txt = new_module_text(relpath)
        if txt is None:
            continue
        scanned_modules.append(label)
        real += scan(txt, f"module:{label}#assertions")
        if not _has_firewall(relpath):
            missing_firewalls.append(label)

    missing_disc = check_disclaimers(disclaimer_text())

    # self-test: the scanner MUST fire on a planted violation, else it is broken
    planted = "Take 50 mg twice daily; this cures pain and is completely safe."
    selftest_hits = scan(planted, "selftest")
    selftest_ok = len(selftest_hits) >= 3

    # negation-guard self-test: a pure disclaimer must NOT fire DOSING/SYNTHESIS
    guard_probe = "This is not a dose and we do not synthesise any compound."
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_disc and not missing_firewalls and selftest_ok and guard_ok)
    result = {"real_violations": real,
              "missing_disclaimers": missing_disc,
              "missing_firewalls": missing_firewalls,
              "scanned_sections": ["proposal.json#claims"]
                                  + (["docs#proposal"] if sec_prop is not None else [])
                                  + (["docs#precision"] if sec_prec is not None else [])
                                  + [f"module:{m}" for m in scanned_modules],
              "selftest_fired": selftest_ok,
              "selftest_hit_classes": sorted({h["class"] for h in selftest_hits}),
              "negation_guard_ok": guard_ok,
              "overall": "PASS" if ok else "FAIL"}
    json.dump(result, open(os.path.join(HERE, "expected", "claim_scan.json"), "w"), indent=1)

    print("M5 forbidden-claim scan  [v2.0 expanded scope]")
    print(f"  scanned: proposal + {len(scanned_modules)} modules"
          + ("" if sec_prec is None else " + precision whitepaper"))
    print(f"  self-test fired on planted violation: {selftest_ok} {result['selftest_hit_classes']}")
    print(f"  negation-guard suppresses disclaimer DOSING/SYNTHESIS: {guard_ok}")
    if real:
        print(f"  [FAIL] {len(real)} forbidden claim(s) in scanned assertions:")
        for h in real[:20]:
            print(f"    - {h['class']}: '{h['match']}'  @{h['where']}  ...{h['ctx']}...")
        sys.exit(1)
    if missing_disc:
        print(f"  [FAIL] required disclaimer phrase(s) missing: {missing_disc}")
        sys.exit(1)
    if missing_firewalls:
        print(f"  [FAIL] module(s) missing firewall/grade field: {missing_firewalls}")
        sys.exit(1)
    if not selftest_ok:
        print("  [FAIL] scanner self-test did not fire — guard is broken")
        sys.exit(1)
    if not guard_ok:
        print("  [FAIL] negation guard broken — disclaimer text would false-positive")
        sys.exit(1)
    print("  [PASS] no forbidden claims; disclaimers + firewalls present; guards live")
    print("OVERALL: PASS")
