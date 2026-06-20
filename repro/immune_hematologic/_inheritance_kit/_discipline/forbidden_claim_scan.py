#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
forbidden_claim_scan.py  --  D5 gate (fail-closed). The discipline firewall.  [immune-tuned]

INHERITED TECHNIQUE: analgesic_threshold_logic_v2_0 / M5 (05-intervention-logic/forbidden_claim_scan.py),
DOI 10.5281/zenodo.20733420. The analgesic scanner mechanically prevents a *target hypothesis* from drifting
into a *treatment / drug / efficacy* claim and fails the build closed if it does. This is the immune analogue.

IMMUNE TUNING (the key difference from the analgesic original):
  This volume LEGITIMATELY cites EXISTING, established clinical cures as anchors -- ATRA/arsenic for APL
  (>90% cure), CAR-T / checkpoint blockade -- each graded cited-[L], and it explains dose-RESPONSE biology
  (the Kramers carcinogen curve). So the firewall must forbid the genuinely-dangerous classes while ALLOWING
  cited established-therapy language and the word "dose" inside "dose-response" / "no dose is given":
    - DOSING      : NUMERIC posology / regimen only (50 mg, mg/kg, twice daily, bid/qd, q8h, per kg) --
                    NOT the bare word "dose" (which appears in "dose-response" and in "[O] dose is open").
    - SYNTHESIS   : verbatim (a synthesis route is never in scope) -- expected absent.
    - EFFICACY    : NOVEL VP over-claims only (VP cures, will cure, guarantee, proven to cure/relieve,
                    is effective in patients, eliminates the disease) -- NOT the bare noun "cure(s)"
                    (which appears in the cited "basin-acting cures" and "ATRA cures APL [L]").
    - SAFETY      : verbatim (is safe, no side-effects, completely safe) -- expected absent.

What is SCANNED (positive DERIVED assertions only):
  - the therapy_report() derived assertion strings (claim / falsifiable_prediction / lever / synthesis text),
    EXCLUDING cited-anchor / grade / firewall / disclaimer keys;
  - the rendered docs/**/index.html visible text (tags stripped);
  - the new discipline modules' assertion strings (D2 priority_ranking, D3 mechanism_honesty, D4 falsification).

What is NOT scanned (checked for PRESENCE -- these LEGITIMATELY contain negated/cited forbidden words):
  - any key matching firewall|grade|principle|label|anchor|clinical_anchor|src|cite|citation|note|
    honest_limit|open_obstacle|disclaimer|basis|inherited_from|title;
  - a NEGATION GUARD suppresses DOSING/SYNTHESIS matches immediately preceded by no/not/without/never/non/nor.

Two self-tests prove the scanner and its guard are live.
Run:  python3 forbidden_claim_scan.py   -> expected/claim_scan.json ; exit 1 on any violation
"""
import os, re, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
PKG  = os.path.normpath(os.path.join(HERE, "..", ".."))
DOCS = os.path.join(PKG, "docs")
for sub in ("_engine", "_therapy"):
    sys.path.insert(0, os.path.join(PKG, "repro", sub))
sys.path.insert(0, os.path.join(PKG, "inherited"))
import vp_imm_engine as ENG
import fundamental_therapy as TH

PATTERNS = {
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\b\d+(\.\d+)?\s?(?:mcg|µg|ug)\b",
               r"\b\d+(\.\d+)?\s?g\s*/\s*day\b", r"\btwice\s+daily\b", r"\bonce\s+daily\b",
               r"\b[bt]id\b", r"\bqd\b", r"\bq\d+h\b", r"\bmilligram", r"\bper\s+kg\b",
               r"\b\d+\s?(?:mg|g)\s+(?:po|iv|sc|im)\b"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux",
                  r"\bmmol\b", r"\breaction\s+mixture\b", r"\bchromatograph", r"\bsynthetic\s+route\b",
                  r"\byield\s+\d", r"\bequiv\.\b"],
    "EFFICACY_AS_FACT": [r"\bVP\s+(?:cures|treats|eliminates)\b", r"\bwill\s+cure\b", r"\bguarantee",
                         r"\bproven\s+to\s+(?:cure|relieve|treat)\b", r"\bis\s+effective\s+in\s+patients\b",
                         r"\beliminates?\s+the\s+disease\b", r"\bcures?\s+the\s+patient\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}
NEGATION_GUARDED = {"DOSING", "SYNTHESIS"}
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor)\b(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$",
                    re.IGNORECASE)
EXCLUDE_KEY_RE = re.compile(
    r"(firewall|grade|principle|^label$|^anchor$|clinical_anchor|^src$|cite|citation|^note$|"
    r"honest_limit|open_obstacle|disclaimer|^basis$|inherited_from|^title$)", re.I)


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
                             "ctx": text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")})
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


def therapy_assertions():
    res = ENG.circulate()
    G = {o["organ"]: o["gamma"] for o in res["organs"]["organs"] if o.get("gamma") is not None}
    out = []
    _collect_assertion_strings(TH.therapy_report(G), out)
    return "  ".join(out)


def docs_text():
    parts = []
    for idx in sorted(glob.glob(os.path.join(DOCS, "**", "index.html"), recursive=True)):
        html = open(idx, encoding="utf-8").read()
        html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)   # drop JSON-LD blocks
        parts.append(re.sub(r"<[^>]+>", " ", html))
    return "  ".join(parts)


NEW_MODULES = [
    ("priority_ranking.json", "D2 priority_ranking", True),
    ("mechanism_honesty.json", "D3 mechanism_honesty", True),
    ("falsification.json", "D4 falsification", True),
]


def new_module_text(fname):
    p = os.path.join(HERE, "expected", fname)
    if not os.path.exists(p):
        return None
    out = []
    _collect_assertion_strings(json.load(open(p)), out)
    return "  ".join(out)


def _has_firewall(fname):
    p = os.path.join(HERE, "expected", fname)
    if not os.path.exists(p):
        return False
    txt = open(p, encoding="utf-8").read()
    return bool(re.search(r'"(firewall|principle)"\s*:\s*"[^"]+', txt)
                or re.search(r'"[a-z_]*grade[a-z_]*"\s*:\s*"[^"]+', txt))


REQUIRED_DISCLAIMERS = [r"not\s+medical\s+advice", r"direction\s*/\s*class", r"does\s+not\s+invent"]


def check_disclaimers(text):
    return [p for p in REQUIRED_DISCLAIMERS if not re.search(p, text, flags=re.I)]


if __name__ == "__main__":
    real = []
    real += scan(therapy_assertions(), "therapy_report#assertions")
    dtext = docs_text()
    real += scan(dtext, "docs#visible-text")

    scanned_modules, missing_firewalls = [], []
    for fname, label, need_fw in NEW_MODULES:
        txt = new_module_text(fname)
        if txt is None:
            continue
        scanned_modules.append(label)
        real += scan(txt, "module:%s#assertions" % label)
        if need_fw and not _has_firewall(fname):
            missing_firewalls.append(label)

    missing_disc = check_disclaimers(dtext + "  " + therapy_assertions())

    # self-test: the scanner MUST fire on a planted violation, else it is broken
    planted = "Give 50 mg/kg twice daily; synthesise the reagent; VP cures the disease and is completely safe."
    selftest_hits = scan(planted, "selftest")
    selftest_ok = len({h["class"] for h in selftest_hits}) >= 3

    # negation-guard self-test: a pure disclaimer must NOT fire DOSING/SYNTHESIS
    guard_probe = "This gives no dose and we do not synthesise any compound; not a mg/kg regimen."
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_disc and not missing_firewalls and selftest_ok and guard_ok)
    result = {"title": "D5 forbidden-claim firewall scan [immune-tuned]",
              "inherited_from": "analgesic_threshold_logic_v2_0/M5 (DOI 10.5281/zenodo.20733420)",
              "firewall": ("the R19 read derives a treatment DIRECTION/CLASS; it is never a numeric dose, a "
                           "synthesis route, a novel VP efficacy claim, or a safety claim. Cited established "
                           "therapies ([L]) and dose-RESPONSE biology are allowed; numeric posology is not."),
              "real_violations": real, "missing_disclaimers": missing_disc,
              "missing_firewalls": missing_firewalls,
              "scanned_sections": ["therapy_report#assertions", "docs#visible-text"]
                                  + ["module:%s" % m for m in scanned_modules],
              "selftest_fired": selftest_ok,
              "selftest_hit_classes": sorted({h["class"] for h in selftest_hits}),
              "negation_guard_ok": guard_ok,
              "overall": "PASS" if ok else "FAIL"}
    os.makedirs(os.path.join(HERE, "expected"), exist_ok=True)
    json.dump(result, open(os.path.join(HERE, "expected", "claim_scan.json"), "w"), indent=1)

    print("D5 forbidden-claim firewall scan  [immune-tuned]")
    print("  scanned: therapy_report + docs + %d discipline modules" % len(scanned_modules))
    print("  self-test fired on planted violation: %s %s" % (selftest_ok, result["selftest_hit_classes"]))
    print("  negation-guard suppresses disclaimer DOSING/SYNTHESIS: %s" % guard_ok)
    if real:
        print("  [FAIL] %d forbidden claim(s):" % len(real))
        for h in real[:20]:
            print("    - %s: '%s'  @%s  ...%s..." % (h["class"], h["match"], h["where"], h["ctx"]))
        sys.exit(1)
    if missing_disc:
        print("  [FAIL] required disclaimer phrase(s) missing: %s" % missing_disc)
        sys.exit(1)
    if missing_firewalls:
        print("  [FAIL] module(s) missing firewall/grade field: %s" % missing_firewalls)
        sys.exit(1)
    if not selftest_ok:
        print("  [FAIL] scanner self-test did not fire -- guard is broken")
        sys.exit(1)
    if not guard_ok:
        print("  [FAIL] negation guard broken -- disclaimer text would false-positive")
        sys.exit(1)
    print("  [PASS] no forbidden claims; disclaimers + firewalls present; guards live")
    print("OVERALL: PASS")
