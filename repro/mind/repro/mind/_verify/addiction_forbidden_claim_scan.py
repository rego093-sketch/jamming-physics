#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
addiction_forbidden_claim_scan.py  —  the discipline guard (fail-closed). Inherited from analgesic
v2.0 M5 via the bipolar/epilepsy/depression/schizophrenia/autism/ADHD T-L scanners.

Scans the ASSERTED claims of the addiction reward-drive map + the burden prioritisation for FORBIDDEN
claim classes (dosing / synthesis / efficacy-as-fact / safety-as-fact / DRUG_SEEKING / CURE_MIRACLE).
If any is found, the build fails closed. This mechanically prevents the map from drifting from a
TARGET-DIRECTION hypothesis into a treatment / drug / efficacy / drug-acquisition / cure claim.

Addiction carries TWO failure modes that make this scanner as strict as the ADHD one:
  (1) DRUG-SEEKING / HARM (the gravest YMYL): addiction concerns substances of abuse. ANY phrasing that
      reads as a ROUTE TO OBTAIN OR USE a substance -- "how to get / where to buy / score / inject /
      smoke / snort / get high / get a fix / dose to feel" -- is forbidden. The reward-drive DIRECTION
      (the naltrexone/varenicline/bupropion/acamprosate/topiramate normalisation hypothesis) is recorded;
      a route-of-acquisition or route-of-use instruction is NEVER emitted.
  (2) CURE-MIRACLE myth: addiction is widely preyed upon by "miracle cure / guaranteed sober / one-shot
      detox / cured forever / addiction gone" quackery. The map must never assert a cure or guaranteed
      sobriety. Both classes are NEGATION-GUARDED so the map's own disclaimers ("no route to obtain any
      substance", "not a cure", "addiction is not cured") never trip the scanner.
  Plus the ADHD-style YMYL respect: "cures / treats / fixes addiction" as fact, and the disrespectful
  "moral failing / failure of will / just stop" framings -- addiction is a TREATABLE MEDICAL CONDITION
  the map locks, not a moral failing -- are forbidden.

What is SCANNED (positive assertions only):
  - addiction_threshold_levers_results.json   (agent direction, anchors, frame text, entries, out-of-reach)
  - addiction_burden_prioritisation.json       (the ranking rows + reading)
What is NOT scanned (checked for PRESENCE instead -- these LEGITIMATELY contain negated forbidden
words like "not a dose", "efficacy=0", "no route to obtain any substance", "not a cure"):
  - any key matching  firewall | *grade* | principle | honesty | primitive | unifying_frame |
    disorder_level_sign | *_direction | *_witness | treatable_not_moral_failing | out_of_reach*
Two defences against firewall false-positives:
  (1) firewall/grade/honesty/witness/out-of-reach keys are excluded from the scanned text;
  (2) a NEGATION GUARD suppresses DOSING/SYNTHESIS/DRUG_SEEKING/CURE_MIRACLE/MORAL_FRAMING matches
      immediately preceded by no/not/without/never/non/nor/cannot (so a stray "no route to obtain" or
      "is not a cure" never fires). NOT applied to SAFETY/EFFICACY because "no side effects" IS itself
      a forbidden safety claim.
NOTE: descriptive vocabulary is SAFE -- the BARE drug-class words "naltrexone", "nalmefene",
"varenicline", "bupropion", "acamprosate", "topiramate", "opioid", "dopamine", "nicotinic", "reuptake",
"sensitisation", "withdrawal", "relapse", "tolerance", "dependence" are direction/biology descriptors,
NOT acquisition or cure. Only DRUG-SEEKING / CURE / efficacy-as-fact phrasings are scanned. The bare
word "treatment" in "not medical advice / not a treatment" is negation-guarded; an unguarded "treats
addiction" fires.
Self-test: a planted positive proves the scanner fires (incl. DRUG_SEEKING + CURE_MIRACLE); a
guard-probe proves the negation guard works.

Run:  python3 addiction_forbidden_claim_scan.py  -> addiction_claim_scan.json ; exit 1 on violation
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))

SCAN_FILES = ["addiction_threshold_levers_results.json", "addiction_burden_prioritisation.json"]

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
                         # addiction-specific efficacy-as-fact (false claims):
                         r"\bcures?\s+addiction\b", r"\btreats?\s+addiction\b", r"\bcure\s+for\s+addiction\b",
                         r"\breverses?\s+addiction\b", r"\bfix(?:es|ed)?\s+addiction\b",
                         r"\b(resolves?|eliminates?|abolishes?)\s+addiction\b",
                         r"\b(resolves?|eliminates?|abolishes?|removes?)\s+(addiction\s+)?(craving|cravings|dependence|withdrawal)\b",
                         r"\bends?\s+addiction\b", r"\bbeats?\s+addiction\b"],
    # DIGNITY-RESPECT firewall: "moral failing / failure of will / just stop" -- addiction is a medical condition
    "MORAL_FRAMING": [r"\bmoral\s+failing\b", r"\bmoral\s+weakness\b", r"\bfailure\s+of\s+will\b",
                      r"\bweak[-\s]?willed\b", r"\black\s+of\s+willpower\b", r"\bjust\s+(?:stop|quit)\b",
                      r"\bjust\s+say\s+no\b", r"\bchoose\s+to\s+stop\b"],
    # DRUG-SEEKING: the route-of-acquisition / route-of-use vocabulary. Must never appear in an asserted claim.
    "DRUG_SEEKING": [r"\bget(?:s|ting)?\s+high\b", r"\bget\s+you\s+high\b", r"\bto\s+get\s+high\b",
                     r"\bwhere\s+to\s+(?:buy|get|score|find)\b", r"\bhow\s+to\s+(?:buy|get|obtain|score|make|cook)\b",
                     r"\bscore\s+(?:some\s+)?(?:drugs?|dope|heroin|coke|meth|pills?)\b",
                     r"\binject(?:s|ed|ing)?\b", r"\bsnort(?:s|ed|ing)?\b", r"\bsmoke\s+(?:it|crack|meth|heroin)\b",
                     r"\bget\s+a\s+fix\b", r"\bscore\s+a\s+(?:hit|fix|bag)\b", r"\beuphori",
                     r"\bdose\s+to\s+feel\b", r"\bget\s+(?:wired|a\s+buzz|wasted|loaded)\b",
                     r"\bto\s+get\s+drunk\b", r"\bdealer\b"],
    # CURE-MIRACLE myth: "miracle cure / guaranteed sober / one-shot detox / cured forever / addiction gone".
    "CURE_MIRACLE": [r"\bmiracle\s+cure\b", r"\bcure[sd]?\s+(?:addiction\s+)?forever\b",
                     r"\bguaranteed?\s+(?:sober|sobriety|clean|abstinen)", r"\bone[-\s]?shot\s+(?:cure|detox)\b",
                     r"\bdetox\s+miracle\b", r"\bmiracle\s+detox\b", r"\baddiction\s+gone\b",
                     r"\bnever\s+crave\s+again\b", r"\bpermanent(?:ly)?\s+(?:cured|sober)\b",
                     r"\b100%\s+(?:cure|success|sober)\b", r"\binstant(?:ly)?\s+(?:cured|sober|clean)\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}
NEGATION_GUARDED = {"DOSING", "SYNTHESIS", "DRUG_SEEKING", "CURE_MIRACLE", "MORAL_FRAMING"}
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor|cannot|can\s*not|n't)\b"
                    r"(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$", re.I)
EXCLUDE_KEY_RE = re.compile(r"(firewall|grade|principle|honesty|^primitive$|^unifying_frame$|"
                            r"^disorder_level_sign$|_direction$|_witness$|treatable_not_moral|"
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

    planted = ("Give 5 mg twice daily; this cures addiction, treats addiction, fixes addiction, it is "
               "a moral failing so just stop; here is where to buy and how to obtain it, inject it or "
               "snort it to get high for euphoria, and it is a miracle cure that leaves you guaranteed "
               "sober, permanently cured, addiction gone, with no side effects.")
    selftest = scan(planted, "selftest"); selftest_ok = len(selftest) >= 4
    selftest_classes = sorted({h["class"] for h in selftest})
    # the scanner MUST be able to catch drug-seeking + cure-miracle + a respect violation
    addiction_classes_caught = ("DRUG_SEEKING" in selftest_classes and
                                "CURE_MIRACLE" in selftest_classes and
                                "MORAL_FRAMING" in selftest_classes)
    guard_probe = ("This is not a dose, we never synthesise any compound, it does not get you high, "
                   "it is not a miracle cure, it is not a moral failing, and there is no dealer; "
                   "it is not a cure.")
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_fw and selftest_ok and addiction_classes_caught and guard_ok and len(scanned) >= 1)
    result = {"inherited_from": "analgesic_threshold_logic v2.0 M5 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia/autism/ADHD T-L",
              "addiction_specific": "adds DRUG_SEEKING (where-to-buy/how-to-obtain/inject/snort/get-high/euphoria) + CURE_MIRACLE (miracle-cure/guaranteed-sober/detox-miracle/addiction-gone) classes, plus addiction efficacy/dignity framings (addiction is a treatable medical condition, not a moral failing)",
              "real_violations": real, "missing_firewalls": missing_fw, "scanned_files": scanned,
              "selftest_fired": selftest_ok, "selftest_hit_classes": selftest_classes,
              "drug_seeking_and_cure_miracle_caught": addiction_classes_caught,
              "negation_guard_ok": guard_ok, "overall": "PASS" if ok else "FAIL"}
    json.dump(result, open(os.path.join(HERE, "addiction_claim_scan.json"), "w"), indent=1)

    print("forbidden-claim scan (addiction)")
    print(f"  scanned: {scanned}")
    print(f"  self-test fired on planted violation: {selftest_ok} {selftest_classes}")
    print(f"  drug-seeking + cure-miracle + dignity all catchable: {addiction_classes_caught}")
    print(f"  negation-guard suppresses disclaimer DRUG_SEEKING/CURE_MIRACLE/DOSING: {guard_ok}")
    if real:
        print(f"  [FAIL] {len(real)} forbidden claim(s):")
        for h in real[:20]:
            print(f"    - {h['class']}: '{h['match']}'  @{h['where']}  ...{h['ctx']}...")
        sys.exit(1)
    if missing_fw: print(f"  [FAIL] file(s) missing firewall/grade field: {missing_fw}"); sys.exit(1)
    if not selftest_ok: print("  [FAIL] scanner self-test did not fire"); sys.exit(1)
    if not addiction_classes_caught: print("  [FAIL] drug-seeking/cure-miracle/dignity self-test classes missing"); sys.exit(1)
    if not guard_ok: print("  [FAIL] negation guard broken"); sys.exit(1)
    print("  [PASS] no forbidden claims; firewalls present; drug-seeking+cure-miracle+dignity guards live")
    print("OVERALL: PASS")
