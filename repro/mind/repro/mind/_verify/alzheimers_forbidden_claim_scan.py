#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
alzheimers_forbidden_claim_scan.py  —  the discipline guard (fail-closed). Inherited from analgesic
v2.0 M5 via the bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction T-L scanners.

Scans the ASSERTED claims of the Alzheimer's symptomatic-network map + the burden prioritisation for
FORBIDDEN claim classes (dosing / synthesis / efficacy-as-fact / safety-as-fact / CURE_REVERSAL /
DIGNITY). If any is found, the build fails closed. This mechanically prevents the map from drifting
from a TARGET-DIRECTION hypothesis into a treatment / dosing / efficacy / disease-reversal / cure
claim, or into a dignity violation.

Alzheimer's carries TWO failure modes that make this scanner as strict as the ADHD/addiction ones:
  (1) CURE / REVERSAL myth (the gravest Alzheimer's-specific YMYL): AD is preyed upon by "cures
      Alzheimer's / reverses dementia / stops the progression / restores lost memory / regrows
      neurons / prevents Alzheimer's guaranteed" quackery. The reachable surface of this map is
      PURELY SYMPTOMATIC -- the cholinergic-drive / excitotoxicity / inhibitory-restore DIRECTION
      (the donepezil/rivastigmine/galantamine + memantine hypothesis) does NOT slow neurodegeneration.
      The dominant fault -- the neurodegenerative PROGRESSION axis (APP/PSEN/MAPT/APOE/TREM2) -- is
      explicitly OUT OF REACH of this threshold frame. ANY phrasing that reads as halting,
      reversing, curing, or preventing the disease, or as restoring lost memory / regrowing neurons,
      is forbidden.
  (2) DIGNITY violation: dementia is surrounded by dehumanising language -- "empty shell / no longer
      a person / already gone / vegetable / lost cause / not worth treating". A person living with
      dementia REMAINS A PERSON. ANY such framing is forbidden.
  Plus the YMYL respect inherited throughout: "cures / treats / fixes Alzheimer's" as fact, and
  "proven to reverse" as fact, are forbidden. Both AD-specific classes are NEGATION-GUARDED so the
  map's own disclaimers ("does not stop the progression", "is not a cure", "does not reverse
  neurodegeneration", "the person is not an empty shell", "remains a person") never trip the scanner.

What is SCANNED (positive assertions only):
  - alzheimers_threshold_levers_results.json   (agent direction, anchors, frame text, entries, out-of-reach)
  - alzheimers_burden_prioritisation.json       (the ranking rows + reading)
What is NOT scanned (checked for PRESENCE instead -- these LEGITIMATELY contain negated forbidden
words like "not a dose", "efficacy=0", "does not slow progression", "not a cure", "remains a person"):
  - any key matching  firewall | *grade* | principle | honesty | primitive | unifying_frame |
    disorder_level_sign | *_direction | *_witness | symptomatic_only* | remains_a_person | out_of_reach*
Two defences against firewall false-positives:
  (1) firewall/grade/honesty/witness/symptomatic-only/dignity/out-of-reach keys are excluded;
  (2) a NEGATION GUARD suppresses DOSING/SYNTHESIS/CURE_REVERSAL/DIGNITY matches immediately preceded
      by no/not/without/never/non/nor/cannot/does-not (so a stray "does not reverse" or "is not a
      cure" or "is not an empty shell" never fires). NOT applied to SAFETY/EFFICACY because "no side
      effects" IS itself a forbidden safety claim.
NOTE: descriptive vocabulary is SAFE -- the BARE drug-class words "donepezil", "rivastigmine",
"galantamine", "memantine", "cholinesterase", "acetylcholine", "cholinergic", "glutamate", "NMDA",
"excitotoxicity", "amyloid", "tau", "neurodegeneration", "progression", "lecanemab", "donanemab" are
direction/biology descriptors, NOT cure or reversal claims. The map may freely SAY that the
progression axis is out of reach and that anti-amyloid antibodies target it; only an asserted
CURE/REVERSAL/PREVENTION or a DIGNITY violation is scanned. The bare word "treatment" in "not medical
advice / not a treatment" is negation-guarded; an unguarded "treats Alzheimer's" fires.
Self-test: a planted positive proves the scanner fires (incl. CURE_REVERSAL + DIGNITY); a guard-probe
proves the negation guard works.

Run:  python3 alzheimers_forbidden_claim_scan.py  -> alzheimers_claim_scan.json ; exit 1 on violation
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))

SCAN_FILES = ["alzheimers_threshold_levers_results.json", "alzheimers_burden_prioritisation.json"]

PATTERNS = {
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdosage\b", r"\bdose[sd]?\b",
               r"\btwice\s+daily\b", r"\bonce\s+daily\b", r"\b[bt]id\b", r"\bqd\b",
               r"\bmilligram", r"\bper\s+kg\b", r"\bserum\s+level\b", r"\btrough\s+level\b",
               r"\bplasma\s+level\b", r"\btitrat"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux",
                  r"\bmmol\b", r"\breaction\s+mixture\b", r"\bchromatograph", r"\bsynthetic\s+route\b"],
    "EFFICACY_AS_FACT": [r"\bcures\b", r"\bwill\s+cure\b", r"\btreats?\s+patients?\b",
                         r"\bproven\s+to\s+(relieve|prevent|treat|resolve|reverse|halt|slow|stop|restore)\b",
                         r"\bguarantee", r"\bis\s+effective\s+in\s+patients\b",
                         # Alzheimer's-specific efficacy-as-fact (false claims):
                         r"\bcures?\s+(?:alzheimer'?s?|dementia|ad)\b", r"\btreats?\s+(?:alzheimer'?s?|dementia)\b",
                         r"\bcure\s+for\s+(?:alzheimer'?s?|dementia)\b",
                         r"\bfix(?:es|ed)?\s+(?:alzheimer'?s?|dementia|the\s+brain)\b",
                         r"\b(resolves?|eliminates?|abolishes?)\s+(?:alzheimer'?s?|dementia)\b"],
    # CURE/REVERSAL myth: the gravest AD-specific quackery -- halt / reverse / cure / prevent the disease,
    # restore lost memory, regrow neurons. The reachable surface is SYMPTOMATIC ONLY; none of this is true.
    "CURE_REVERSAL": [r"\breverses?\s+(?:alzheimer'?s?|dementia|neurodegeneration|the\s+disease|the\s+damage|cognitive\s+decline|memory\s+loss)\b",
                      r"\bprevents?\s+(?:alzheimer'?s?|dementia)\b",
                      r"\bstops?\s+(?:the\s+)?(?:progression|neurodegeneration|decline|disease|amyloid|tau)\b",
                      r"\bhalts?\s+(?:the\s+)?(?:progression|neurodegeneration|decline|disease|amyloid|tau)\b",
                      r"\b(?:slows?|slowing)\s+(?:the\s+)?(?:progression|neurodegeneration|decline|disease)\b",
                      r"\bdisease[-\s]?modifying\b",
                      r"\brestores?\s+(?:lost\s+)?memor(?:y|ies)\b", r"\bbrings?\s+back\s+(?:lost\s+)?memor(?:y|ies)\b",
                      r"\bregrow(?:s|n|ing)?\s+(?:neurons?|brain|tissue)\b",
                      r"\bregenerates?\s+(?:neurons?|brain|tissue|the\s+brain)\b",
                      r"\bclears?\s+(?:the\s+)?(?:amyloid|plaques?|tangles?)\b",
                      r"\bmiracle\s+(?:cure|treatment|drug)\b", r"\bguaranteed?\s+(?:cure|to\s+cure|recovery)\b",
                      r"\bcure[sd]?\s+(?:alzheimer'?s?\s+)?forever\b", r"\bdementia\s+gone\b",
                      r"\breverses?\s+aging\b", r"\bone[-\s]?shot\s+cure\b",
                      r"\b100%\s+(?:cure|effective|recovery)\b", r"\binstant(?:ly)?\s+(?:cured|restored)\b"],
    # DIGNITY violation: dementia is surrounded by dehumanising language. A person with dementia REMAINS a person.
    "DIGNITY": [r"\bempty\s+shell\b", r"\bno\s+longer\s+a\s+person\b", r"\bnot\s+a\s+person\s+anymore\b",
                r"\balready\s+gone\b", r"\bas\s+good\s+as\s+(?:dead|gone)\b", r"\bjust\s+a\s+(?:body|shell|vegetable)\b",
                r"\bvegetable\b", r"\blost\s+cause\b", r"\bnot\s+worth\s+(?:treating|saving|the\s+effort)\b",
                r"\bhusk\s+of\s+a\s+person\b", r"\bgone\s+already\b", r"\bnothing\s+left\s+of\s+(?:them|him|her)\b",
                r"\bbrain[-\s]?dead\b", r"\bwrite\s+(?:them|him|her)\s+off\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}
NEGATION_GUARDED = {"DOSING", "SYNTHESIS", "CURE_REVERSAL", "DIGNITY"}
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor|cannot|can\s*not|n't|does\s*not|do\s*not|doesn|don)\b"
                    r"(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$", re.I)
EXCLUDE_KEY_RE = re.compile(r"(firewall|grade|principle|honesty|^primitive$|^unifying_frame$|"
                            r"^disorder_level_sign$|_direction$|_witness$|symptomatic_only|"
                            r"remains_a_person|dignity|out_of_reach)", re.I)

def _negated(text, start):
    return bool(NEG_RE.search(text[max(0, start-32):start]))

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

    planted = ("Give 5 mg twice daily; this cures Alzheimer's, treats dementia, and is a "
               "disease-modifying miracle cure that reverses neurodegeneration, stops the "
               "progression, halts the disease, restores lost memory and regrows neurons, "
               "guaranteed to cure forever with no side effects -- and anyway the patient is "
               "an empty shell, no longer a person, just a vegetable, already gone and not "
               "worth treating.")
    selftest = scan(planted, "selftest"); selftest_ok = len(selftest) >= 4
    selftest_classes = sorted({h["class"] for h in selftest})
    # the scanner MUST be able to catch cure-reversal + dignity
    ad_classes_caught = ("CURE_REVERSAL" in selftest_classes and "DIGNITY" in selftest_classes)
    guard_probe = ("This is not a dose, we never synthesise any compound, it does not reverse "
                   "neurodegeneration, it does not stop the progression, it is not a cure, it does "
                   "not restore lost memory; and the person is not an empty shell, is not a "
                   "vegetable, and remains a person.")
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_fw and selftest_ok and ad_classes_caught and guard_ok and len(scanned) >= 1)
    result = {"inherited_from": "analgesic_threshold_logic v2.0 M5 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction T-L",
              "alzheimers_specific": "adds CURE_REVERSAL (reverse/cure/prevent Alzheimer's, stop/halt the progression, restore lost memory, regrow neurons, miracle cure) + DIGNITY (empty shell / no longer a person / vegetable / already gone / not worth treating -- a person with dementia remains a person) classes; the reachable surface is SYMPTOMATIC ONLY and the neurodegenerative-progression axis is explicitly out of reach",
              "real_violations": real, "missing_firewalls": missing_fw, "scanned_files": scanned,
              "selftest_fired": selftest_ok, "selftest_hit_classes": selftest_classes,
              "cure_reversal_and_dignity_caught": ad_classes_caught,
              "negation_guard_ok": guard_ok, "overall": "PASS" if ok else "FAIL"}
    json.dump(result, open(os.path.join(HERE, "alzheimers_claim_scan.json"), "w"), indent=1)

    print("forbidden-claim scan (Alzheimer's)")
    print(f"  scanned: {scanned}")
    print(f"  self-test fired on planted violation: {selftest_ok} {selftest_classes}")
    print(f"  cure-reversal + dignity both catchable: {ad_classes_caught}")
    print(f"  negation-guard suppresses disclaimer CURE_REVERSAL/DIGNITY/DOSING: {guard_ok}")
    if real:
        print(f"  [FAIL] {len(real)} forbidden claim(s):")
        for h in real[:20]:
            print(f"    - {h['class']}: '{h['match']}'  @{h['where']}  ...{h['ctx']}...")
        sys.exit(1)
    if missing_fw: print(f"  [FAIL] file(s) missing firewall/grade field: {missing_fw}"); sys.exit(1)
    if not selftest_ok: print("  [FAIL] scanner self-test did not fire"); sys.exit(1)
    if not ad_classes_caught: print("  [FAIL] cure-reversal/dignity self-test classes missing"); sys.exit(1)
    if not guard_ok: print("  [FAIL] negation guard broken"); sys.exit(1)
    print("  [PASS] no forbidden claims; firewalls present; cure-reversal+dignity guards live")
    print("OVERALL: PASS")
