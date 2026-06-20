#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
claim_scanner.py  --  fail-closed forbidden-claim scanner.

Inherited technology (from analgesic_threshold_logic v2.0, where it was the M5 gate). This package
models cardiorespiratory MECHANISM DYNAMICS only (CHARTER; FUTURE_WORK section 6). It is NOT a
clinical, pharmacological, or treatment artifact. The canonical site must therefore never carry:
  * drug dosing language (mg, mg/kg, dosing regimen, "twice daily", a recommended/therapeutic dose),
  * prescriptive medical advice ("prescribe", "should be administered", "consult ... and take"),
  * treatment-of-disease assertions ("treat patients with X", "is a cure/therapy for Y"),
  * efficacy / safety claims ("clinically proven", "safe and effective", "proven to cure").

The legitimate epidemiological vocabulary of the oncology chapter -- "carcinogen dose-response",
"low-dose slope", "dose-to-bias conversion" -- is deliberately NOT matched; nor is narrative usage
such as "treated separately in the next section" or "predicts the clinical direction". The patterns
target prescriptive clinical/drug claims, not the words in isolation.

scan() returns the list of hits; a non-empty list is a gate FAIL (fail-closed).
"""
import os, re, html, json

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.abspath(os.path.join(_HERE, "..", ".."))
_DOCS = os.path.join(_PKG, "docs")

# Each pattern is (label, compiled regex). Matched against tag-stripped, entity-unescaped text.
_FORBIDDEN = [
    ("drug-dose-mg",        re.compile(r"\b\d+(?:\.\d+)?\s*mg\b", re.I)),
    ("drug-dose-mgkg",      re.compile(r"\bmg\s*/\s*kg\b", re.I)),
    ("clinical-dose-qual",  re.compile(r"\b(?:recommended|therapeutic|effective|starting|maintenance|daily)\s+dose\b", re.I)),
    ("dosing-regimen",      re.compile(r"\bdos(?:e|ing)\s+(?:regimen|schedule)\b", re.I)),
    ("dosing-frequency",    re.compile(r"\b(?:once|twice|three\s+times|q\d+h)\s+(?:a\s+day|daily|per\s+day|nightly)\b", re.I)),
    ("prescribe",           re.compile(r"\bprescrib(?:e|es|ed|ing|tion)\b", re.I)),
    ("administer-advice",   re.compile(r"\bshould\s+(?:take|be\s+(?:given|administered|prescribed|dosed))\b", re.I)),
    ("take-dose",           re.compile(r"\b(?:take|give|administer)\s+\d+(?:\.\d+)?\s*(?:mg|g|ml|tablets?|capsules?)\b", re.I)),
    ("treat-patients",      re.compile(r"\btreat(?:s|ed|ing|ment)?\s+(?:the\s+)?patients?\s+(?:with|using|by)\b", re.I)),
    ("treatment-for-is",    re.compile(r"\bis\s+(?:a\s+|an\s+|the\s+)?(?:treatment|cure|therapy)\s+for\b", re.I)),
    ("cure",                re.compile(r"\bcures?\b|\bcured\b", re.I)),
    ("clinically-proven",   re.compile(r"\bclinically\s+(?:proven|effective|validated)\b", re.I)),
    ("safe-and-effective",  re.compile(r"\bsafe\s+and\s+effective\b", re.I)),
    ("proven-to",           re.compile(r"\bproven\s+to\s+(?:treat|cure|reduce|prevent|relieve)\b", re.I)),
    ("reduces-mortality",   re.compile(r"\b(?:reduces|prevents|eliminates|abolishes)\s+(?:mortality|death|the\s+disease)\b", re.I)),
    ("guaranteed",          re.compile(r"\bguaranteed\s+to\b", re.I)),
]

_TAG = re.compile(r"<[^>]+>")


def _text_of(path):
    raw = open(path, encoding="utf-8").read()
    # drop <script>/<style> blocks (JSON-LD etc.) before stripping tags
    raw = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", raw, flags=re.I | re.S)
    return html.unescape(_TAG.sub(" ", raw))


def _html_files():
    out = []
    for root, _dirs, files in os.walk(_DOCS):
        for fn in files:
            if fn.endswith(".html"):
                out.append(os.path.join(root, fn))
    return sorted(out)


def scan():
    hits = []
    files = _html_files()
    for ap in files:
        text = _text_of(ap)
        rp = os.path.relpath(ap, _PKG).replace(os.sep, "/")
        for label, rx in _FORBIDDEN:
            for m in rx.finditer(text):
                a = max(0, m.start() - 30); b = min(len(text), m.end() + 30)
                snippet = re.sub(r"\s+", " ", text[a:b]).strip()
                hits.append({"file": rp, "label": label, "match": m.group(0), "context": snippet})
    return {"ok": len(hits) == 0, "n_files": len(files), "n_patterns": len(_FORBIDDEN), "hits": hits}


if __name__ == "__main__":
    print(json.dumps(scan(), ensure_ascii=False, indent=2))
