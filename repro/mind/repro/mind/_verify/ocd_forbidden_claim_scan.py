#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ocd_forbidden_claim_scan.py  —  the discipline guard (fail-closed). Inherited from analgesic v2.0 M5
via the bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction/Alzheimer's T-L scanners.

Scans the ASSERTED claims of the OCD CSTC-loop map + the burden prioritisation for FORBIDDEN claim
classes (dosing / synthesis / efficacy-as-fact / safety-as-fact / CURE_MIRACLE / MORAL_FRAMING). If any
is found, the build fails closed. This mechanically prevents the map from drifting from a TARGET-DIRECTION
hypothesis into a treatment / dosing / efficacy / cure claim, or into a moral-framing / stigma violation.

OCD carries TWO failure modes that make this scanner as strict as the ADHD/addiction/Alzheimer's ones:
  (1) CURE / MIRACLE myth (the gravest OCD-specific YMYL): OCD is preyed upon by "cures OCD / stops the
      intrusive thoughts forever / eliminates compulsions / guaranteed relief / OCD gone / permanently
      cured / one weird trick" claims. The reachable surface of this map is REACHABLE-BUT-PARTIAL -- the
      serotonergic-drive (L3), glutamatergic-excitatory (L1) and inhibitory-restore (L2) DIRECTIONS are
      the actual mainstay/investigational routes and genuinely (PARTIALLY) help, but they do NOT unstick
      the pathological loop-LOCK; the dominant fault -- the pathological-stabilisation LOCK axis (DLGAP3/
      SLITRK5/PTPRD/BTBD3) -- is explicitly OUT OF REACH of this threshold frame. ANY phrasing that reads
      as a guaranteed cure, a permanent fix, an elimination of intrusive thoughts/compulsions, or a
      miracle is forbidden.
  (2) MORAL_FRAMING / STIGMA violation: OCD is surrounded by trivialising and willpower-shaming language --
      "just stop worrying / just relax / it is a choice / lack of willpower / a character flaw / they are
      attention-seeking / so OCD about / it is all in their head / just dirty thoughts / a moral failing".
      OCD is a treatable medical condition; intrusive thoughts are a SYMPTOM, not a confession of desire,
      and compulsions are not a choice or a weakness. ANY such framing is forbidden.
  Plus the YMYL respect inherited throughout: "cures / treats / fixes OCD" as fact, and "proven to cure"
  as fact, are forbidden. Both OCD-specific classes are NEGATION-GUARDED so the map's own disclaimers
  ("is not a cure", "does not eliminate the compulsions", "is not a moral failing", "is not a character
  flaw", "intrusive thoughts are not a confession") never trip the scanner.

What is SCANNED (positive assertions only):
  - ocd_threshold_levers_results.json   (agent direction, anchors, frame text, entries, out-of-reach)
  - ocd_burden_prioritisation.json       (the ranking rows + reading)
What is NOT scanned (checked for PRESENCE instead -- these LEGITIMATELY contain negated forbidden words
like "not a dose", "efficacy=0", "is not a cure", "not a moral failing"):
  - any key matching  firewall | *grade* | principle | honesty | primitive | unifying_frame |
    disorder_level_sign | *_direction | *_witness | reachable_but_partial | not_a_moral_failing |
    out_of_reach*
Two defences against firewall false-positives:
  (1) firewall/grade/honesty/witness/reachable-but-partial/moral/out-of-reach keys are excluded;
  (2) a NEGATION GUARD suppresses DOSING/SYNTHESIS/CURE_MIRACLE/MORAL_FRAMING matches immediately preceded
      by no/not/without/never/non/nor/cannot/does-not (so a stray "is not a cure" or "not a moral failing"
      never fires). NOT applied to SAFETY/EFFICACY because "no side effects" IS itself a forbidden safety
      claim.
NOTE: descriptive vocabulary is SAFE -- the BARE words "SSRI", "clomipramine", "serotonin", "serotonergic",
"dopamine", "glutamate", "riluzole", "memantine", "compulsion", "obsession", "intrusive", "deep-brain
stimulation", "exposure-response-prevention" are direction/biology descriptors, NOT cure or stigma claims.
The map may freely SAY that the loop-lock is out of reach and that DBS targets it; only an asserted
CURE/MIRACLE or a MORAL_FRAMING/STIGMA violation is scanned. The bare word "treatment" in "not medical
advice / not a treatment" is negation-guarded; an unguarded "treats OCD" fires.
Self-test: a planted positive proves the scanner fires (incl. CURE_MIRACLE + MORAL_FRAMING); a guard-probe
proves the negation guard works.

Run:  python3 ocd_forbidden_claim_scan.py  -> ocd_claim_scan.json ; exit 1 on violation
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))

SCAN_FILES = ["ocd_threshold_levers_results.json", "ocd_burden_prioritisation.json"]

PATTERNS = {
    "DOSING": [r"\b\d+(\.\d+)?\s?mg\b", r"\bmg\s*/\s*kg\b", r"\bdosage\b", r"\bdose[sd]?\b",
               r"\btwice\s+daily\b", r"\bonce\s+daily\b", r"\b[bt]id\b", r"\bqd\b",
               r"\bmilligram", r"\bper\s+kg\b", r"\bserum\s+level\b", r"\btrough\s+level\b",
               r"\bplasma\s+level\b", r"\btitrat"],
    "SYNTHESIS": [r"\bsynthesi[sz]e[sd]?\b", r"\bsynthesi[sz]ing\b", r"\breagent", r"\breflux",
                  r"\bmmol\b", r"\breaction\s+mixture\b", r"\bchromatograph", r"\bsynthetic\s+route\b"],
    "EFFICACY_AS_FACT": [r"\bcures\b", r"\bwill\s+cure\b", r"\btreats?\s+patients?\b",
                         r"\bproven\s+to\s+(relieve|prevent|treat|resolve|cure|stop|eliminate)\b",
                         r"\bguarantee", r"\bis\s+effective\s+in\s+patients\b",
                         # OCD-specific efficacy-as-fact (false claims):
                         r"\bcures?\s+(?:ocd|obsessive[-\s]?compulsive)\b", r"\btreats?\s+(?:ocd|obsessive[-\s]?compulsive)\b",
                         r"\bcure\s+for\s+(?:ocd|obsessive[-\s]?compulsive)\b",
                         r"\bfix(?:es|ed)?\s+(?:ocd|the\s+brain)\b",
                         r"\b(resolves?|eliminates?|abolishes?)\s+(?:ocd|the\s+compulsions?|the\s+obsessions?)\b"],
    # CURE/MIRACLE myth: the gravest OCD-specific quackery -- cure / permanently stop / eliminate intrusive
    # thoughts and compulsions, miracle. The reachable surface is REACHABLE-BUT-PARTIAL; none of this is true.
    "CURE_MIRACLE": [r"\bcure[sd]?\s+(?:ocd\s+)?forever\b", r"\bpermanent(?:ly)?\s+(?:cured|relief|fix)\b",
                     r"\bstops?\s+(?:the\s+)?(?:intrusive\s+thoughts?|obsessions?|compulsions?)\s+(?:forever|permanently|for\s+good)\b",
                     r"\beliminates?\s+(?:the\s+)?(?:intrusive\s+thoughts?|obsessions?|compulsions?)\b",
                     r"\bgets?\s+rid\s+of\s+(?:the\s+)?(?:ocd|intrusive\s+thoughts?|obsessions?|compulsions?)\b",
                     r"\bocd\s+gone\b", r"\bcured\s+of\s+ocd\b", r"\bfree\s+(?:you\s+)?(?:from|of)\s+ocd\s+forever\b",
                     r"\bmiracle\s+(?:cure|treatment|drug|fix)\b", r"\bone\s+(?:weird\s+)?trick\b",
                     r"\bguaranteed?\s+(?:cure|relief|to\s+cure|recovery)\b",
                     r"\b100%\s+(?:cure|effective|relief|recovery)\b", r"\binstant(?:ly)?\s+(?:cured|relief)\b",
                     r"\bnever\s+(?:obsess|compulsion|intrusive)\s+again\b"],
    # MORAL_FRAMING / STIGMA: OCD is surrounded by trivialising / willpower-shaming language. OCD is a
    # treatable medical condition; intrusive thoughts are a symptom, not a confession, and not a weakness.
    "MORAL_FRAMING": [r"\bjust\s+stop\s+(?:worrying|obsessing|doing\s+it|the\s+compulsions?)\b",
                      r"\bjust\s+relax\b", r"\bjust\s+let\s+it\s+go\b",
                      r"\b(?:a\s+)?lack\s+of\s+willpower\b", r"\bweak[-\s]?willed\b",
                      r"\b(?:a\s+)?character\s+flaw\b", r"\b(?:a\s+)?moral\s+failing\b",
                      r"\b(?:a\s+)?choice\b\s+(?:to|not\s+to)\b", r"\bsimply\s+(?:a\s+)?(?:choice|habit)\b",
                      r"\battention[-\s]?seeking\b", r"\ball\s+in\s+(?:their|your|his|her)\s+head\b",
                      r"\bjust\s+(?:dirty|bad)\s+thoughts?\b", r"\bjust\s+being\s+(?:dramatic|difficult)\b",
                      r"\bso\s+ocd\s+about\b", r"\ba\s+bit\s+ocd\b", r"\bnot\s+a\s+real\s+(?:illness|disorder)\b",
                      r"\bsnap\s+out\s+of\s+it\b", r"\btry\s+harder\b"],
    "SAFETY_AS_FACT": [r"\bis\s+safe\b", r"\bare\s+safe\b", r"\bno\s+side[-\s]?effects?\b",
                       r"\bwithout\s+side[-\s]?effects?\b", r"\bside[-\s]?effect[-\s]?free\b",
                       r"\bcompletely\s+safe\b"],
}
NEGATION_GUARDED = {"DOSING", "SYNTHESIS", "CURE_MIRACLE", "MORAL_FRAMING"}
NEG_RE = re.compile(r"\b(?:no|not|without|never|non|nor|cannot|can\s*not|n't|does\s*not|do\s*not|doesn|don)\b"
                    r"(?:[\s\-]+(?:a|an|any|the|further|more))?[\s\-]*$", re.I)
EXCLUDE_KEY_RE = re.compile(r"(firewall|grade|principle|honesty|^primitive$|^unifying_frame$|"
                            r"^disorder_level_sign$|_direction$|_witness$|reachable_but_partial|"
                            r"moral|out_of_reach)", re.I)

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

    planted = ("Give 5 mg twice daily; this cures OCD, treats obsessive-compulsive disorder, and is a "
               "miracle cure that permanently stops the intrusive thoughts forever, eliminates the "
               "compulsions and gets rid of the obsessions, guaranteed cure with no side effects -- and "
               "anyway OCD is not a real illness, just a lack of willpower and a character flaw, a moral "
               "failing where they should just stop worrying, snap out of it and try harder; they are "
               "just attention-seeking and it is all in their head.")
    selftest = scan(planted, "selftest"); selftest_ok = len(selftest) >= 4
    selftest_classes = sorted({h["class"] for h in selftest})
    # the scanner MUST be able to catch cure-miracle + moral-framing
    ocd_classes_caught = ("CURE_MIRACLE" in selftest_classes and "MORAL_FRAMING" in selftest_classes)
    guard_probe = ("This is not a dose, we never synthesise any compound, it is not a cure, it does not "
                   "permanently stop the intrusive thoughts, it does not eliminate the compulsions; and "
                   "OCD is not a moral failing, not a character flaw, not a lack of willpower, and "
                   "intrusive thoughts are a symptom, not a confession.")
    guard_hits = scan(guard_probe, "guardprobe")
    guard_ok = len([h for h in guard_hits if h["class"] in NEGATION_GUARDED]) == 0

    ok = (not real and not missing_fw and selftest_ok and ocd_classes_caught and guard_ok and len(scanned) >= 1)
    result = {"inherited_from": "analgesic_threshold_logic v2.0 M5 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction/Alzheimer's T-L",
              "ocd_specific": "adds CURE_MIRACLE (cure/permanently stop the intrusive thoughts, eliminate the compulsions, miracle cure, one weird trick, OCD gone) + MORAL_FRAMING/STIGMA (just stop worrying / lack of willpower / character flaw / moral failing / attention-seeking / all in their head / so OCD about / not a real illness -- OCD is a treatable medical condition and intrusive thoughts are a symptom, not a confession or a weakness) classes; the reachable surface is REACHABLE-BUT-PARTIAL and the pathological-stabilisation LOCK axis is explicitly out of reach",
              "real_violations": real, "missing_firewalls": missing_fw, "scanned_files": scanned,
              "selftest_fired": selftest_ok, "selftest_hit_classes": selftest_classes,
              "cure_miracle_and_moral_framing_caught": ocd_classes_caught,
              "negation_guard_ok": guard_ok, "overall": "PASS" if ok else "FAIL"}
    json.dump(result, open(os.path.join(HERE, "ocd_claim_scan.json"), "w"), indent=1)

    print("forbidden-claim scan (OCD)")
    print(f"  scanned: {scanned}")
    print(f"  self-test fired on planted violation: {selftest_ok} {selftest_classes}")
    print(f"  cure-miracle + moral-framing both catchable: {ocd_classes_caught}")
    print(f"  negation-guard suppresses disclaimer CURE_MIRACLE/MORAL_FRAMING/DOSING: {guard_ok}")
    if real:
        print(f"  [FAIL] {len(real)} forbidden claim(s):")
        for h in real[:20]:
            print(f"    - {h['class']}: '{h['match']}'  @{h['where']}  ...{h['ctx']}...")
        sys.exit(1)
    if missing_fw: print(f"  [FAIL] file(s) missing firewall/grade field: {missing_fw}"); sys.exit(1)
    if not selftest_ok: print("  [FAIL] scanner self-test did not fire"); sys.exit(1)
    if not ocd_classes_caught: print("  [FAIL] cure-miracle/moral-framing self-test classes missing"); sys.exit(1)
    if not guard_ok: print("  [FAIL] negation guard broken"); sys.exit(1)
    print("  [PASS] no forbidden claims; firewalls present; cure-miracle+moral-framing guards live")
    print("OVERALL: PASS")
