#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autism_forbidden_claim_scan.py  —  the discipline guard (fail-closed). Inherited from analgesic
v2.0 M5 via the bipolar/epilepsy/depression/schizophrenia T-L scanners.

Scans the ASSERTED claims of the autism three-lever map + the burden prioritisation for FORBIDDEN
claim classes (dosing / synthesis / efficacy-as-fact / safety-as-fact / QUACKERY). If any is found, the
build fails closed. This mechanically prevents the map from drifting from a TARGET-DIRECTION hypothesis
into a treatment / drug / efficacy claim.

Autism carries TWO failure modes that make this scanner the strictest of the T-L series:
  (1) YMYL ("your money or your life"): autism is targeted by a documented quackery industry --
      chelation, MMS / "miracle mineral solution" / chlorine-dioxide enemas, bleach protocols,
      hyperbaric / stem-cell / "biomed recovery" schemes. These have harmed and killed children.
      ANY phrasing that reads as "cures / treats / reverses / recovers-from autism" is forbidden, and
      the quackery vocabulary itself is forbidden in an asserted claim.
  (2) NEURODIVERSITY RESPECT: autism is a neurodevelopmental DIFFERENCE, not only a deficit (the map
      LOCKS this). "normalise / fix / make normal / eliminate autism" framings are forbidden not only
      because they are false-as-fact but because they are disrespectful framings the map must never emit.

What is SCANNED (positive assertions only):
  - autism_threshold_levers_results.json   (agent direction, anchors, frame text, entries, out-of-reach)
  - autism_burden_prioritisation.json       (the ranking rows + reading)
What is NOT scanned (checked for PRESENCE instead -- these LEGITIMATELY contain negated forbidden
words like "not a dose", "efficacy=0", "cannot fix the W axis", "not a cure"):
  - any key matching  firewall | *grade* | principle | honesty | primitive | unifying_frame |
    disorder_level_sign | *_direction | *_witness | difference_not_deficit | out_of_reach*
Two defences against firewall false-positives:
  (1) firewall/grade/honesty/witness/out-of-reach keys are excluded from the scanned text;
  (2) a NEGATION GUARD suppresses DOSING/SYNTHESIS/QUACKERY matches immediately preceded by
      no/not/without/never/non/nor/cannot (so a stray "not a dose" or "is not a cure" never fires).
      NOT applied to SAFETY/EFFICACY because "no side effects" IS itself a forbidden safety claim.
NOTE: descriptive vocabulary is SAFE -- "excitatory", "inhibitory", "GABA", "the E/I set-point",
"over-excitation", "difference", "neurodevelopmental", "scaffold", "wiring", "lamination". Only
efficacy-as-fact / quackery phrasings are scanned. The bare word "treatment" in "not medical advice /
not a treatment" is negation-guarded; an unguarded "treats autism" fires.
Self-test: a planted positive proves the scanner fires (incl. a quackery term); a guard-probe proves
the negation guard works.

Run:  python3 autism_forbidden_claim_scan.py  -> autism_claim_scan.json ; exit 1 on violation
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))

SCAN_FILES = ["autism_threshold_levers_results.json", "autism_burden_prioritisation.json"]

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
                         # autism-specific efficacy-as-fact (false claims):
                         r"\bcures?\s+autism\b", r"\btreats?\s+autism\b", r"\bcure\s+for\s+autism\b",
                         r"\breverses?\s+autism\b", r"\brecover(?:s|y|ed)?\s+from\s+autism\b",
                         r"\brecovers?\s+autism\b", r"\bautism\s+recovery\b",
                         r"\b(resolves?|eliminates?|abolishes?)\s+autism\b",
                         r"\b(resolves?|eliminates?|abolishes?|removes?)\s+(autistic\s+)?(symptoms?|traits?|behaviou?rs?)\b",
                         r"\bimproves?\s+autism\b", r"\brestores?\s+(typical|normal)\s+development\b"],
    # NEURODIVERSITY-RESPECT firewall: "fix / normalise / make normal / eliminate the condition"
    "NORMALISE_FRAMING": [r"\bnormali[sz]e[sd]?\s+(autism|the\s+autistic|autistic\s+(child|children|brain|people))\b",
                          r"\bmakes?\s+(?:the\s+)?(?:autistic\s+)?(?:child|children|brain|people)\s+normal\b",
                          r"\bfix(?:es|ed|ing)?\s+(autism|autistic\s+(child|children|people|brain))\b",
                          r"\bmake\s+autism\s+disappear\b", r"\beliminate\s+autism\b"],
    # QUACKERY: the documented autism-harm vocabulary. These words must never appear in an asserted claim.
    "QUACKERY": [r"\bchelat(?:e|es|ed|ing|ion)\b", r"\bMMS\b", r"\bmiracle\s+mineral\b",
                 r"\bchlorine\s+dioxide\b", r"\bbleach\s+(?:protocol|enema|therapy|treatment)\b",
                 r"\bCD\s+protocol\b", r"\bGcMAF\b", r"\bhyperbaric\s+(?:oxygen\s+)?(?:cure|therapy\s+cures)\b",
                 r"\bstem[-\s]?cell\s+(?:cure|therapy\s+cures)\b", r"\bbiomed\s+recovery\b",
                 r"\bfa[ei]cal\s+(?:microbiota\s+)?transplant\s+cures\b", r"\bdetox(?:es|ify|ifies)?\s+(?:the\s+)?autis"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}
NEGATION_GUARDED = {"DOSING", "SYNTHESIS", "QUACKERY", "NORMALISE_FRAMING"}
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

    planted = ("Give 5 mg twice daily; this cures autism, treats autism, reverses autism, achieves "
               "recovery from autism, normalises the autistic child, uses a chelation and MMS bleach "
               "protocol and has no side effects.")
    selftest = scan(planted, "selftest"); selftest_ok = len(selftest) >= 4
    selftest_classes = sorted({h["class"] for h in selftest})
    # the scanner MUST be able to catch quackery + a respect-violating normalise framing
    quackery_caught = "QUACKERY" in selftest_classes and "NORMALISE_FRAMING" in selftest_classes
    guard_probe = ("This is not a dose, we never synthesise any compound, it does not chelate, and it "
                   "will not normalise autism; it is not a cure.")
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_fw and selftest_ok and quackery_caught and guard_ok and len(scanned) >= 1)
    result = {"inherited_from": "analgesic_threshold_logic v2.0 M5 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia T-L",
              "autism_specific": "adds QUACKERY (chelation/MMS/bleach) + NORMALISE_FRAMING (neurodiversity-respect) classes",
              "real_violations": real, "missing_firewalls": missing_fw, "scanned_files": scanned,
              "selftest_fired": selftest_ok, "selftest_hit_classes": selftest_classes,
              "quackery_and_respect_caught": quackery_caught,
              "negation_guard_ok": guard_ok, "overall": "PASS" if ok else "FAIL"}
    json.dump(result, open(os.path.join(HERE, "autism_claim_scan.json"), "w"), indent=1)

    print("forbidden-claim scan (autism)")
    print(f"  scanned: {scanned}")
    print(f"  self-test fired on planted violation: {selftest_ok} {selftest_classes}")
    print(f"  quackery + normalise-framing both catchable: {quackery_caught}")
    print(f"  negation-guard suppresses disclaimer DOSING/SYNTHESIS/QUACKERY: {guard_ok}")
    if real:
        print(f"  [FAIL] {len(real)} forbidden claim(s):")
        for h in real[:20]:
            print(f"    - {h['class']}: '{h['match']}'  @{h['where']}  ...{h['ctx']}...")
        sys.exit(1)
    if missing_fw: print(f"  [FAIL] file(s) missing firewall/grade field: {missing_fw}"); sys.exit(1)
    if not selftest_ok: print("  [FAIL] scanner self-test did not fire"); sys.exit(1)
    if not quackery_caught: print("  [FAIL] quackery/respect self-test classes missing"); sys.exit(1)
    if not guard_ok: print("  [FAIL] negation guard broken"); sys.exit(1)
    print("  [PASS] no forbidden claims; firewalls present; quackery+respect guards live")
    print("OVERALL: PASS")
