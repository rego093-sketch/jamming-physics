#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adhd_forbidden_claim_scan.py  —  the discipline guard (fail-closed). Inherited from analgesic
v2.0 M5 via the bipolar/epilepsy/depression/schizophrenia/autism T-L scanners.

Scans the ASSERTED claims of the ADHD drive-tone map + the burden prioritisation for FORBIDDEN
claim classes (dosing / synthesis / efficacy-as-fact / safety-as-fact / STIMULANT-MISUSE /
COGNITIVE-ENHANCEMENT). If any is found, the build fails closed. This mechanically prevents the map
from drifting from a TARGET-DIRECTION hypothesis into a treatment / drug / efficacy / misuse claim.

ADHD carries TWO failure modes that make this scanner as strict as the autism one:
  (1) YMYL ("your money or your life"): ADHD pharmacology centres on SCHEDULE-II psychostimulants
      (methylphenidate, amphetamine). ANY phrasing that reads as a MISUSE licence -- "get high /
      snort / crush / euphoria / recreational / party drug" -- is forbidden. The drive-tone DIRECTION
      (DAT/NET reuptake) is recorded; a route-of-abuse instruction is never emitted.
  (2) COGNITIVE-ENHANCEMENT myth: stimulants are widely (and falsely) marketed as "smart drugs /
      study drugs / nootropics" that "boost focus" or make a healthy person "limitless". The map must
      never assert non-clinical cognitive enhancement. Both of these are NEGATION-GUARDED so the
      map's own disclaimers ("not a misuse licence", "is not a smart drug") never trip the scanner.
  Plus the autism-style YMYL respect: "cures / treats / fixes ADHD" as fact, and disrespectful
  "normalise the ADHD child" framings, are forbidden (ADHD is a neurodevelopmental DIFFERENCE the map
  locks, not only a deficit).

What is SCANNED (positive assertions only):
  - adhd_threshold_levers_results.json   (agent direction, anchors, frame text, entries, out-of-reach)
  - adhd_burden_prioritisation.json       (the ranking rows + reading)
What is NOT scanned (checked for PRESENCE instead -- these LEGITIMATELY contain negated forbidden
words like "not a dose", "efficacy=0", "not a misuse licence", "not a cure"):
  - any key matching  firewall | *grade* | principle | honesty | primitive | unifying_frame |
    disorder_level_sign | *_direction | *_witness | difference_not_deficit | out_of_reach*
Two defences against firewall false-positives:
  (1) firewall/grade/honesty/witness/out-of-reach keys are excluded from the scanned text;
  (2) a NEGATION GUARD suppresses DOSING/SYNTHESIS/STIMULANT_MISUSE/COGNITIVE_ENHANCEMENT/
      NORMALISE_FRAMING matches immediately preceded by no/not/without/never/non/nor/cannot (so a
      stray "not a dose" or "is not a smart drug" never fires). NOT applied to SAFETY/EFFICACY
      because "no side effects" IS itself a forbidden safety claim.
NOTE: descriptive vocabulary is SAFE -- the BARE drug-class words "stimulant", "psychostimulant",
"methylphenidate", "amphetamine", "atomoxetine", "guanfacine", "reuptake", "dopamine", "noradrenaline"
are direction descriptors, NOT misuse. Only MISUSE / ENHANCEMENT / efficacy-as-fact phrasings are
scanned. The bare word "treatment" in "not medical advice / not a treatment" is negation-guarded; an
unguarded "treats ADHD" fires.
Self-test: a planted positive proves the scanner fires (incl. STIMULANT_MISUSE + COGNITIVE_ENHANCEMENT);
a guard-probe proves the negation guard works.

Run:  python3 adhd_forbidden_claim_scan.py  -> adhd_claim_scan.json ; exit 1 on violation
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))

SCAN_FILES = ["adhd_threshold_levers_results.json", "adhd_burden_prioritisation.json"]

PATTERNS = {
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdosage\b", r"\bdose[sd]?\b",
               r"\btwice\s+daily\b", r"\bonce\s+daily\b", r"\b[bt]id\b", r"\bqd\b",
               r"\bmilligram", r"\bper\s+kg\b", r"\bserum\s+level\b", r"\btrough\s+level\b",
               r"\bplasma\s+level\b"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux",
                  r"\bmmol\b", r"\breaction\s+mixture\b", r"\bchromatograph", r"\bsynthetic\s+route\b"],
    "EFFICACY_AS_FACT": [r"\bcures\b", r"\bwill\s+cure\b", r"\btreats?\s+patients?\b",
                         r"\bproven\s+to\s+(relieve|prevent|treat|resolve|reverse)\b", r"\bguarantee",
                         r"\bis\s+effective\s+in\s+patients\b",
                         # ADHD-specific efficacy-as-fact (false claims):
                         r"\bcures?\s+adhd\b", r"\btreats?\s+adhd\b", r"\bcure\s+for\s+adhd\b",
                         r"\breverses?\s+adhd\b", r"\bfix(?:es|ed)?\s+adhd\b",
                         r"\b(resolves?|eliminates?|abolishes?)\s+adhd\b",
                         r"\b(resolves?|eliminates?|abolishes?|removes?)\s+(adhd\s+)?(symptoms?|inattention|hyperactivity|impulsivity)\b",
                         r"\bimproves?\s+adhd\b", r"\brestores?\s+(typical|normal)\s+attention\b"],
    # NEURODIVERSITY-RESPECT firewall: "fix / normalise / make normal" the ADHD person/condition
    "NORMALISE_FRAMING": [r"\bnormali[sz]e[sd]?\s+(adhd|the\s+adhd|adhd\s+(child|children|brain|people))\b",
                          r"\bmakes?\s+(?:the\s+)?(?:adhd\s+)?(?:child|children|brain|people)\s+normal\b",
                          r"\bfix(?:es|ed|ing)?\s+(adhd|adhd\s+(child|children|people|brain))\b",
                          r"\bmake\s+adhd\s+disappear\b", r"\beliminate\s+adhd\b"],
    # STIMULANT-MISUSE: the route-of-abuse vocabulary. Must never appear in an asserted claim.
    "STIMULANT_MISUSE": [r"\bget(?:s|ting)?\s+high\b", r"\bget\s+you\s+high\b", r"\bto\s+get\s+high\b",
                         r"\bsnort(?:s|ed|ing)?\b", r"\binsufflat", r"\bcrush(?:es|ed|ing)?\s+(?:and\s+)?(?:snort|inject|the\s+(?:pill|tablet))\b",
                         r"\beuphori", r"\brecreational(?:ly)?\b", r"\bparty\s+drug\b",
                         r"\bto\s+stay\s+(?:awake|up)\s+all\s+night\b", r"\bget\s+a\s+buzz\b", r"\bto\s+get\s+wired\b"],
    # COGNITIVE-ENHANCEMENT myth: "smart/study drug, nootropic, boost focus, limitless" in the healthy.
    "COGNITIVE_ENHANCEMENT": [r"\bsmart\s+drugs?\b", r"\bstudy\s+drugs?\b", r"\bnootropic",
                              r"\bcognitive\s+enhanc", r"\blimitless\b", r"\bbrain\s+booster\b",
                              r"\bboosts?\s+(?:focus|concentration|productivity|brainpower|cognition|iq)\b",
                              r"\benhances?\s+(?:focus|concentration|cognition|productivity|performance)\s+in\s+(?:healthy|the\s+healthy|non[-\s]?adhd|the\s+non)",
                              r"\bmakes?\s+you\s+(?:smarter|focus\s+better)\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}
NEGATION_GUARDED = {"DOSING", "SYNTHESIS", "STIMULANT_MISUSE", "COGNITIVE_ENHANCEMENT", "NORMALISE_FRAMING"}
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor|cannot|can\s*not|n't)\b"
                    r"(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$", re.I)
EXCLUDE_KEY_RE = re.compile(r"(firewall|grade|principle|honesty|^primitive$|^unifying_frame$|"
                            r"^disorder_level_sign$|_direction$|_witness$|difference_not_deficit|"
                            r"out_of_reach)", re.I)

def _negated(text, start):
    return bool(NEG_RE.search(text[max(0, start-28):start]))

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

    planted = ("Give 5 mg twice daily; this cures ADHD, treats ADHD, fixes ADHD, normalises the ADHD "
               "child; take it to get high, snort it for euphoria as a recreational party drug, and use "
               "it as a study drug / smart drug nootropic cognitive enhancer to boost focus and feel "
               "limitless, with no side effects.")
    selftest = scan(planted, "selftest"); selftest_ok = len(selftest) >= 4
    selftest_classes = sorted({h["class"] for h in selftest})
    # the scanner MUST be able to catch stimulant-misuse + cognitive-enhancement + a respect violation
    adhd_classes_caught = ("STIMULANT_MISUSE" in selftest_classes and
                           "COGNITIVE_ENHANCEMENT" in selftest_classes and
                           "NORMALISE_FRAMING" in selftest_classes)
    guard_probe = ("This is not a dose, we never synthesise any compound, it does not get you high, it "
                   "is not a smart drug, it is not a study drug, it does not boost focus, and it will "
                   "not normalise adhd; it is not a cure.")
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_fw and selftest_ok and adhd_classes_caught and guard_ok and len(scanned) >= 1)
    result = {"inherited_from": "analgesic_threshold_logic v2.0 M5 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia/autism T-L",
              "adhd_specific": "adds STIMULANT_MISUSE (get-high/snort/euphoria/recreational) + COGNITIVE_ENHANCEMENT (smart-drug/nootropic/boost-focus/limitless) classes, plus ADHD efficacy/respect framings",
              "real_violations": real, "missing_firewalls": missing_fw, "scanned_files": scanned,
              "selftest_fired": selftest_ok, "selftest_hit_classes": selftest_classes,
              "stimulant_misuse_and_enhancement_caught": adhd_classes_caught,
              "negation_guard_ok": guard_ok, "overall": "PASS" if ok else "FAIL"}
    json.dump(result, open(os.path.join(HERE, "adhd_claim_scan.json"), "w"), indent=1)

    print("forbidden-claim scan (ADHD)")
    print(f"  scanned: {scanned}")
    print(f"  self-test fired on planted violation: {selftest_ok} {selftest_classes}")
    print(f"  stimulant-misuse + cognitive-enhancement + respect all catchable: {adhd_classes_caught}")
    print(f"  negation-guard suppresses disclaimer MISUSE/ENHANCEMENT/DOSING: {guard_ok}")
    if real:
        print(f"  [FAIL] {len(real)} forbidden claim(s):")
        for h in real[:20]:
            print(f"    - {h['class']}: '{h['match']}'  @{h['where']}  ...{h['ctx']}...")
        sys.exit(1)
    if missing_fw: print(f"  [FAIL] file(s) missing firewall/grade field: {missing_fw}"); sys.exit(1)
    if not selftest_ok: print("  [FAIL] scanner self-test did not fire"); sys.exit(1)
    if not adhd_classes_caught: print("  [FAIL] stimulant-misuse/enhancement/respect self-test classes missing"); sys.exit(1)
    if not guard_ok: print("  [FAIL] negation guard broken"); sys.exit(1)
    print("  [PASS] no forbidden claims; firewalls present; misuse+enhancement+respect guards live")
    print("OVERALL: PASS")
