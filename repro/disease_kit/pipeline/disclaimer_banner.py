#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
disclaimer_banner.py  --  the SINGLE SOURCE OF TRUTH for the patient-facing
                          simulation disclaimer.

Per the author's instruction: this banner must appear AT THE VERY TOP of any
human-facing rendering of a disease read -- BEFORE the explanation -- and must
make UNMISTAKABLY clear that the output is a COMPUTER SIMULATION built on a
DNA-EMERGENCE (창발) model that MAY DIFFER FROM REALITY.

It is bilingual (한국어 + English) because the kit's governance is Korean while
its deliverables are English, and a patient/carer in either language must be able
to read the caveat first.

Anything that renders a disease for a person -- the CLI explainer
(`pipeline/explain_disease.py`), and any future VP-SPEC v1.8 HTML site -- MUST
import `banner()` / `html_banner()` from here and emit it FIRST. Do not re-type
the text elsewhere; change it once, here.

This module is READ-ONLY with respect to every `diseases/<slug>/analysis.json`
and the engine, so it perturbs NO determinism hash.

CLI:
    python3 pipeline/disclaimer_banner.py            # print the text banner
    python3 pipeline/disclaimer_banner.py --html     # emit the HTML banner block
"""
import sys

# ---------------------------------------------------------------------------
# The canonical disclaimer lines. Each tuple is (Korean, English). The FIRST
# line is the headline simulation caveat the author asked to lead with.
# ---------------------------------------------------------------------------
_LINES = [
    ("\u26a0  컴퓨터 시뮬레이션 결과입니다 \u2014 현실과 다를 수 있습니다",
     "\u26a0  COMPUTER-SIMULATION OUTPUT \u2014 it may differ from reality"),

    ("이 자료는 'DNA 창발(emergence)' 모델을 이용한 컴퓨터 시뮬레이션이며, 실제 생물학 및 임상 현실과 차이가 있을 수 있습니다.",
     "This is a computer simulation using a DNA-emergence model; it may differ from real biology and clinical reality."),

    ("의료 조언이 아닙니다. 진단\u00b7치료\u00b7예방 수단이 아니며, 어떤 개인도 이 자료에 근거해 행동해서는 안 됩니다.",
     "It is NOT medical advice. Not a diagnosis, treatment, or cure for any individual; no one should act on it."),

    ("이 모델은 치료의 '방향'만 제시하며(강제), 효과\u00b7용량\u00b7안전성의 '크기'는 전혀 주장하지 않습니다 ([O] = 미검증 가설).",
     "The model gives only the DIRECTION of an intervention (forced); it asserts NO magnitude \u2014 no efficacy, dose, or safety ([O] = untested hypothesis)."),

    ("새 치료를 발견한 것이 아니라, 이미 알려진 승인약의 방향을 재도출한 '방법 검증'입니다.",
     "It does not discover new treatments; it re-derives the direction of already-known drugs as a method check."),

    ("반드시 주치의\u00b7전문 의료진과 상의하세요. 신뢰할 수 있는 실제 환자 자료: Orphanet \u00b7 NORD \u00b7 GeneReviews \u00b7 ClinicalTrials.gov \u00b7 MedlinePlus.",
     "Always consult your physician. Trusted patient resources: Orphanet \u00b7 NORD \u00b7 GeneReviews \u00b7 ClinicalTrials.gov \u00b7 MedlinePlus."),
]


def _wrap(text, width):
    """Width-aware wrap that counts East-Asian wide chars as 2 columns."""
    def w(ch):
        o = ord(ch)
        # CJK / Hangul / fullwidth ranges -> width 2
        if (0x1100 <= o <= 0x115F or 0x2E80 <= o <= 0xA4CF or
                0xAC00 <= o <= 0xD7A3 or 0xF900 <= o <= 0xFAFF or
                0xFE30 <= o <= 0xFE4F or 0xFF00 <= o <= 0xFF60 or
                0xFFE0 <= o <= 0xFFE6):
            return 2
        return 1
    out, line, col = [], "", 0
    for word in text.split(" "):
        wd = sum(w(c) for c in word)
        if line and col + 1 + wd > width:
            out.append(line)
            line, col = word, wd
        else:
            if line:
                line += " "
                col += 1
            line += word
            col += wd
    if line:
        out.append(line)
    return out or [""]


def _disp_len(s):
    def w(ch):
        o = ord(ch)
        if (0x1100 <= o <= 0x115F or 0x2E80 <= o <= 0xA4CF or
                0xAC00 <= o <= 0xD7A3 or 0xF900 <= o <= 0xFAFF or
                0xFE30 <= o <= 0xFE4F or 0xFF00 <= o <= 0xFF60 or
                0xFFE0 <= o <= 0xFFE6):
            return 2
        return 1
    return sum(w(c) for c in s)


def banner(width=78, lang="both"):
    """Return the disclaimer as a boxed plain-text string.

    lang: 'both' (default) | 'ko' | 'en'.
    """
    inner = width - 4  # "| " ... " |"
    top = "+" + "=" * (width - 2) + "+"
    blank = "|" + " " * (width - 2) + "|"
    rows = [top, blank]

    def emit(s, fill=" "):
        for ln in _wrap(s, inner):
            pad = inner - _disp_len(ln)
            rows.append("| " + ln + fill * max(0, pad) + " |")

    for i, (ko, en) in enumerate(_LINES):
        if lang in ("both", "ko"):
            emit(ko)
        if lang in ("both", "en"):
            emit(en)
        if i < len(_LINES) - 1:
            rows.append(blank)
    rows.append(blank)
    rows.append(top)
    return "\n".join(rows)


def html_banner(lang="both"):
    """Return an accessible HTML disclaimer block for the VP-SPEC v1.8 site.

    Designed to sit as the FIRST element inside <body>, role=alert so screen
    readers announce it before the page content.
    """
    import html as _h
    items = []
    for ko, en in _LINES:
        parts = []
        if lang in ("both", "ko"):
            parts.append('<span lang="ko">' + _h.escape(ko) + "</span>")
        if lang in ("both", "en"):
            parts.append('<span lang="en">' + _h.escape(en) + "</span>")
        items.append("    <li>" + "<br>".join(parts) + "</li>")
    return (
        '<aside role="alert" class="vp-sim-disclaimer" '
        'style="border:3px solid #b00;background:#fff6f6;color:#222;'
        'padding:1rem 1.25rem;margin:0 0 1.5rem;border-radius:8px;'
        'font-size:0.95rem;line-height:1.5;">\n'
        "  <ul style=\"margin:0;padding-left:1.2rem;\">\n"
        + "\n".join(items)
        + "\n  </ul>\n</aside>"
    )


def print_banner(width=78, lang="both"):
    print(banner(width=width, lang=lang))


if __name__ == "__main__":
    if "--html" in sys.argv:
        print(html_banner())
    else:
        print_banner()
