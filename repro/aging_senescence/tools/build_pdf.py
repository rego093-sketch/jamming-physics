#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pdf.py  --  Aging / Senescence citation-layer PDF generator (VP-SPEC v1.8, publication phase).

It builds ONE whitepaper PDF *from the canonical HTML* in docs/ (no restructuring): the same chapter
order, the same prose, the same numbers. Because every displayed number already lives in the canonical
HTML -- which the engine generated (Constitution C1) -- the PDF cannot drift from the reproducible
result. Web-only furniture (breadcrumb nav, page nav, JSON-LD, the claim-strip GitHub/DOI link) is
dropped; the scholarly content (title, answer-first, abstract, body, tables, vp-cards, grades) is kept.
Page 1 is the citation front matter: full title, author + ORCID, version, DOI (published Zenodo concept DOI,
never fabricated) and the hub URL.

Determinism: reportlab is put in invariant mode (rl_config.invariant = 1), so two builds are byte
-identical. The PDF is written to pdf/aging_senescence_vp_site.pdf; the canonical docs/ site is untouched.

Refuses to run while gates.writing_locked() is True (research-first), exactly like build_docs.py.
Requires the canonical site to be built first (docs/<slug>/index.html).
"""
import os, re, sys, json, importlib

# --- invariant (deterministic) reportlab output: set BEFORE importing platypus -----------------------
from reportlab import rl_config
rl_config.invariant = 1  # fixed timestamps + stable doc id => byte-identical builds

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, FrameBreak, NextPageTemplate, CondPageBreak,
)
from xml.sax.saxutils import escape as xml_escape
from bs4 import BeautifulSoup, NavigableString, Tag

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.normpath(os.path.join(HERE, ".."))
DOCS = os.path.join(PKG, "docs")
OUTDIR = os.path.join(PKG, "pdf")
OUTPDF = os.path.join(OUTDIR, "aging_senescence_vp_site.pdf")

sys.path.insert(0, os.path.join(PKG, "repro", "_verify"))
gates = importlib.import_module("gates")

# --- canonical provenance (mirror of render_site.py constants; kept identical) -----------------------
SITE = "https://jamming-physics.org"
PAPER_ID = "aging"
HUB_URL = SITE + "/" + PAPER_ID + "/"
TITLE_FULL = "Aging and Senescence: the Systemic Decline of Homeostatic Setpoints over the Lifespan"
SHORT = "Aging & Senescence"
AUTHOR = "Young Jae Lee"
ORCID = "https://orcid.org/0009-0002-7535-8245"
ORCID_ID = "0009-0002-7535-8245"
CC = "CC BY 4.0"
CC_URL = "https://creativecommons.org/licenses/by/4.0/"
REPO = "https://github.com/rego093-sketch/jamming-physics"
DOI_TBD = "10.5281/zenodo.20756155"  # published Zenodo concept DOI
DATE = "2026-06-19"
try:
    VERSION_STR = open(os.path.join(PKG, "VERSION"), encoding="utf-8").read().strip()
except Exception:
    VERSION_STR = "1.3.0-writing"
BRANCH = "integrative capstone (the temporal decline axis)"

# ---------------------------------------------------------------------------------------------------
# Fonts (DejaVu: full Greek + math-symbol coverage; serif body, sans labels, mono hashes)
# ---------------------------------------------------------------------------------------------------
_FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _register_fonts():
    reg = [
        ("Body", "DejaVuSerif.ttf"), ("Body-Bold", "DejaVuSerif-Bold.ttf"),
        ("Body-Italic", "DejaVuSerif-Italic.ttf"), ("Body-BoldItalic", "DejaVuSerif-BoldItalic.ttf"),
        ("Sans", "DejaVuSans.ttf"), ("Sans-Bold", "DejaVuSans-Bold.ttf"),
        ("Sans-Oblique", "DejaVuSans-Oblique.ttf"),
        ("Mono", "DejaVuSansMono.ttf"),
    ]
    for name, fn in reg:
        pdfmetrics.registerFont(TTFont(name, os.path.join(_FONT_DIR, fn)))
    pdfmetrics.registerFontFamily(
        "Body", normal="Body", bold="Body-Bold", italic="Body-Italic", boldItalic="Body-BoldItalic")
    pdfmetrics.registerFontFamily(
        "Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Oblique", boldItalic="Sans-Bold")


# ---------------------------------------------------------------------------------------------------
# Palette + paragraph styles
# ---------------------------------------------------------------------------------------------------
INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#5b6168")
ACCENT = colors.HexColor("#2563a8")
RULE = colors.HexColor("#c9cdd2")
ANSWER_BG = colors.HexColor("#eef4fb")
CARD_BG = colors.HexColor("#f6f7f9")
HEAD_BG = colors.HexColor("#eceef1")
ZEBRA = colors.HexColor("#f6f7f9")
G_VERIFIED = colors.HexColor("#1a7f37")
G_OPEN = colors.HexColor("#9a6700")
G_FORCED = colors.HexColor("#b35900")


def _styles():
    S = {}
    S["body"] = ParagraphStyle("body", fontName="Body", fontSize=9.5, leading=14.2,
                               textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7)
    S["muted"] = ParagraphStyle("muted", parent=S["body"], textColor=MUTED, fontName="Body-Italic")
    S["answer"] = ParagraphStyle("answer", fontName="Body", fontSize=10.5, leading=15.5,
                                 textColor=INK, alignment=TA_LEFT, spaceAfter=0)
    S["abstract"] = ParagraphStyle("abstract", fontName="Body-Italic", fontSize=9.2, leading=13.6,
                                   textColor=colors.HexColor("#333a40"), alignment=TA_JUSTIFY, spaceAfter=7)
    S["h2"] = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=11.5, leading=14.5,
                             textColor=ACCENT, spaceBefore=11, spaceAfter=4, keepWithNext=1)
    S["h1"] = ParagraphStyle("h1", fontName="Sans-Bold", fontSize=18, leading=21,
                             textColor=INK, spaceBefore=0, spaceAfter=3, keepWithNext=1)
    S["eyebrow"] = ParagraphStyle("eyebrow", fontName="Sans-Bold", fontSize=8, leading=10,
                                  textColor=ACCENT, spaceAfter=1)
    S["card"] = ParagraphStyle("card", fontName="Body", fontSize=8.8, leading=12.8,
                               textColor=colors.HexColor("#2a2f34"), alignment=TA_LEFT, spaceAfter=0)
    S["cell"] = ParagraphStyle("cell", fontName="Body", fontSize=7.8, leading=9.8,
                               textColor=INK, alignment=TA_LEFT)
    S["cell_num"] = ParagraphStyle("cell_num", parent=S["cell"], alignment=TA_CENTER)
    S["cell_head"] = ParagraphStyle("cell_head", fontName="Sans-Bold", fontSize=7.8, leading=9.8,
                                    textColor=INK, alignment=TA_CENTER)
    S["caption"] = ParagraphStyle("caption", fontName="Body-Italic", fontSize=7.6, leading=10.2,
                                  textColor=MUTED, alignment=TA_LEFT, spaceBefore=2, spaceAfter=8)
    # title-page styles
    S["t_title"] = ParagraphStyle("t_title", fontName="Sans-Bold", fontSize=21, leading=25,
                                  textColor=INK, alignment=TA_LEFT, spaceAfter=4)
    S["t_sub"] = ParagraphStyle("t_sub", fontName="Body-Italic", fontSize=11, leading=15,
                                textColor=MUTED, alignment=TA_LEFT, spaceAfter=14)
    S["t_meta"] = ParagraphStyle("t_meta", fontName="Body", fontSize=9.5, leading=14.5,
                                 textColor=INK, alignment=TA_LEFT)
    S["t_label"] = ParagraphStyle("t_label", fontName="Sans-Bold", fontSize=8, leading=12,
                                   textColor=ACCENT, alignment=TA_LEFT)
    S["t_abs"] = ParagraphStyle("t_abs", fontName="Body", fontSize=9.5, leading=14.2,
                                textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
    S["mono"] = ParagraphStyle("mono", fontName="Mono", fontSize=7.6, leading=10.4,
                               textColor=colors.HexColor("#333a40"), alignment=TA_LEFT)
    S["toc"] = ParagraphStyle("toc", fontName="Body", fontSize=9.8, leading=15,
                              textColor=INK, alignment=TA_LEFT)
    return S


# ---------------------------------------------------------------------------------------------------
# Inline HTML -> reportlab mini-markup (escape text nodes; keep sub/sup/b/i; links -> text only)
# ---------------------------------------------------------------------------------------------------
_WS = re.compile(r"\s+")


def _grade_color(cls):
    if "g-verified" in cls:
        return "#1a7f37"
    if "g-open" in cls:
        return "#9a6700"
    if "g-forced" in cls:
        return "#b35900"
    return None


def inline(node):
    out = []
    for ch in node.children:
        if isinstance(ch, NavigableString):
            out.append(xml_escape(_WS.sub(" ", str(ch))))
        elif isinstance(ch, Tag):
            nm = ch.name.lower()
            cls = " ".join(ch.get("class", []) or [])
            inner = inline(ch)
            if nm == "sub":
                out.append("<sub>%s</sub>" % inner)
            elif nm in ("sup", "super"):
                out.append("<super>%s</super>" % inner)
            elif nm in ("b", "strong"):
                out.append("<b>%s</b>" % inner)
            elif nm in ("i", "em", "cite"):
                out.append("<i>%s</i>" % inner)
            elif nm == "code":
                out.append('<font face="Mono">%s</font>' % inner)
            elif nm == "br":
                out.append("<br/>")
            elif nm == "a":
                out.append("<i>%s</i>" % inner)  # print: keep link text, drop URL
            elif nm == "span":
                col = _grade_color(cls)
                out.append('<font color="%s">%s</font>' % (col, inner) if col else inner)
            else:
                out.append(inner)
    return _WS.sub(" ", "".join(out)).strip()


# ---------------------------------------------------------------------------------------------------
# Boxed flowables (answer block, vp-card) -- 1-cell table with accent left border
# ---------------------------------------------------------------------------------------------------
def boxed(flowable, bg, accent, pad=7, accent_w=2.6):
    t = Table([[flowable]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), accent_w, accent),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), pad + 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad - 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 1),
    ]))
    return t


# ---------------------------------------------------------------------------------------------------
# Table builder (caption rendered separately, below the grid)
# ---------------------------------------------------------------------------------------------------
def build_table(div, S, avail_w):
    tbl = div.find("table")
    head = tbl.find("thead")
    body = tbl.find("tbody")
    head_cells = head.find_all("th")
    ncol = len(head_cells)
    header = [Paragraph(inline(th), S["cell_head"]) for th in head_cells]
    rows = [header]
    align_num = [False] * ncol  # first column label, rest centered numeric by default
    for tr in body.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        row = []
        for j, td in enumerate(cells):
            is_num = "num" in (td.get("class", []) or [])
            row.append(Paragraph(inline(td), S["cell_num"] if (is_num or j > 0) else S["cell"]))
        # pad short rows
        while len(row) < ncol:
            row.append(Paragraph("", S["cell"]))
        rows.append(row)
    # column widths: first column wider, remaining equal
    first = min(0.34, max(0.18, 1.6 / ncol)) * avail_w
    rest = (avail_w - first) / (ncol - 1) if ncol > 1 else avail_w
    col_w = [first] + [rest] * (ncol - 1)
    t = Table(rows, colWidths=col_w, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.HexColor("#9aa0a6")),
        ("LINEBELOW", (0, -1), (-1, -1), 0.7, colors.HexColor("#9aa0a6")),
        ("LINEABOVE", (0, 0), (-1, 0), 0.7, colors.HexColor("#9aa0a6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
    ]
    # zebra rows
    for r in range(1, len(rows)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), ZEBRA))
    t.setStyle(TableStyle(style))
    flows = [t]
    cap = tbl.find("caption")
    if cap is not None:
        flows.append(Paragraph(inline(cap), S["caption"]))
    return KeepTogether(flows) if len(rows) <= 6 else flows


# ---------------------------------------------------------------------------------------------------
# Parse one canonical chapter HTML -> ordered list of flowables
# ---------------------------------------------------------------------------------------------------
def parse_chapter(slug, no, S, avail_w):
    path = os.path.join(DOCS, slug, "index.html")
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    main = soup.find("main")
    flows = []

    h1 = main.find("h1")
    grade_txt = None
    cs = main.find("aside", class_="claim-strip")
    if cs is not None:
        g = cs.find("span", class_="grade")
        if g is not None:
            grade_txt = g.get_text(" ", strip=True)

    flows.append(Paragraph("Section %d" % no, S["eyebrow"]))
    flows.append(Paragraph(inline(h1), S["h1"]))
    if grade_txt:
        col = _grade_color(" ".join(cs.find("span", class_="grade").get("class", [])))
        flows.append(Paragraph('<font color="%s">%s</font>' % (col or "#5b6168", xml_escape(grade_txt)),
                               S["t_label"]))
    flows.append(Spacer(1, 5))

    # walk top-level children of <main> in order
    for el in main.find_all(recursive=False):
        if not isinstance(el, Tag):
            continue
        nm = el.name.lower()
        cls = " ".join(el.get("class", []) or [])
        if nm == "p" and "eyebrow" in cls:
            continue
        if nm == "h1":
            continue
        if nm == "nav":  # page nav
            continue
        if nm == "aside" and "claim-strip" in cls:
            continue
        if nm == "p" and "answer" in cls:
            flows.append(Spacer(1, 1))
            flows.append(boxed(Paragraph(inline(el), S["answer"]), ANSWER_BG, ACCENT))
            flows.append(Spacer(1, 7))
        elif nm == "p" and "abstract" in cls:
            flows.append(Paragraph(inline(el), S["abstract"]))
        elif nm == "p" and "muted" in cls:
            flows.append(Paragraph(inline(el), S["muted"]))
        elif nm == "p":
            flows.append(Paragraph(inline(el), S["body"]))
        elif nm == "h2":
            flows.append(Paragraph(inline(el), S["h2"]))
        elif nm == "h3":
            flows.append(Paragraph(inline(el), S["h2"]))
        elif nm == "div" and "tw" in cls:
            built = build_table(el, S, avail_w)
            flows.append(Spacer(1, 2))
            if isinstance(built, list):
                flows.extend(built)
            else:
                flows.append(built)
            flows.append(Spacer(1, 3))
        elif nm == "aside" and "vp-card" in cls:
            flows.append(Spacer(1, 2))
            flows.append(boxed(Paragraph(inline(el), S["card"]), CARD_BG, colors.HexColor("#9aa0a6"),
                               pad=6, accent_w=2.0))
            flows.append(Spacer(1, 6))
        else:
            # any other paragraph-ish content: render its text
            txt = inline(el)
            if txt:
                flows.append(Paragraph(txt, S["body"]))
    return flows


# ---------------------------------------------------------------------------------------------------
# Title page + TOC (front matter)  --  "DOI + hub URL on page 1"
# ---------------------------------------------------------------------------------------------------
def title_page(meta, S, avail_w, det):
    flows = []
    flows.append(Spacer(1, 6))
    flows.append(Paragraph("Jamming Physics &middot; VP Theory", S["t_label"]))
    flows.append(Spacer(1, 10))
    flows.append(Paragraph(xml_escape("Aging and Senescence"), S["t_title"]))
    flows.append(Paragraph(xml_escape("The Systemic Decline of Homeostatic Setpoints over the Lifespan"),
                           S["t_sub"]))

    # author / identity block
    info = [
        ("Author", '%s &middot; ORCID <i>%s</i>' % (xml_escape(AUTHOR), xml_escape(ORCID_ID))),
        ("Branch", xml_escape(BRANCH)),
        ("Version", xml_escape(VERSION_STR)),
        ("Date", xml_escape(DATE)),
        ("DOI", "%s (Zenodo concept DOI)" % DOI_TBD),
        ("Hub", '<i>%s</i>' % xml_escape(HUB_URL)),
        ("Code", '<i>%s</i>' % xml_escape(REPO + "/tree/main/repro/aging/")),
        ("License", '%s &middot; <i>%s</i>' % (xml_escape(CC), xml_escape(CC_URL))),
    ]
    rows = []
    for label, val in info:
        rows.append([Paragraph(label.upper(), S["t_label"]), Paragraph(val, S["t_meta"])])
    t = Table(rows, colWidths=[2.4 * cm, avail_w - 2.4 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LINEBEFORE", (0, 0), (0, -1), 2.0, ACCENT),
        ("LEFTPADDING", (0, 0), (0, -1), 9),
    ]))
    flows.append(t)
    flows.append(Spacer(1, 16))

    flows.append(Paragraph("ABSTRACT", S["t_label"]))
    flows.append(Spacer(1, 3))
    flows.append(Paragraph(xml_escape(meta["abstract"]), S["t_abs"]))
    flows.append(Spacer(1, 8))

    # headline results
    flows.append(Paragraph("HEADLINE RESULTS", S["t_label"]))
    flows.append(Spacer(1, 3))
    hr = "".join("&bull;&nbsp; %s<br/>" % xml_escape(h) for h in meta["headline_results"])
    flows.append(Paragraph(hr, S["t_meta"]))
    flows.append(Spacer(1, 12))

    # reproducibility line
    flows.append(Paragraph("REPRODUCIBILITY", S["t_label"]))
    flows.append(Spacer(1, 3))
    repro = ("Deterministic build, SEED=19. Result sha256 "
             "<font face='Mono'>%s</font>; byte-identical across two runs. "
             "Every number in this document is pulled from the reproducible engine and mirrors the "
             "canonical HTML at the hub above (no value is entered by hand). Grading is honest: "
             "<font color='#1a7f37'>[V] verified</font>, [L] cited/anchored, "
             "<font color='#9a6700'>[O] open</font> (each open item lists its obstacle in &sect;11)."
             % det["result_sha256"])
    flows.append(Paragraph(repro, S["t_meta"]))

    flows.append(Spacer(1, 16))
    flows.append(Table([[""]], colWidths=[avail_w], rowHeights=[0.6],
                       style=TableStyle([("LINEABOVE", (0, 0), (-1, 0), 0.6, RULE)])))
    flows.append(Spacer(1, 4))
    flows.append(Paragraph(
        "The integrative capstone (temporal) layer of VP Theory. Aging is modeled as the slow loss of "
        "defense gain of every homeostatic setpoint, plus the accumulation of cells stuck in irreversible "
        "R19 attractors (senescence); it is the dominant risk multiplier for every pathology kernel in the "
        "framework. This volume emerges no organs owned elsewhere &mdash; node identity &gamma; is inherited "
        "from the DNA atlas (single source of truth); only the temporal dynamics are added here.",
        S["muted"]))
    flows.append(PageBreak())
    return flows


def toc_page(meta, S, avail_w):
    flows = [Paragraph("Contents", S["h1"]), Spacer(1, 8)]
    rows = []
    gmap = {"verified": ("[V]", "#1a7f37"), "open": ("[O]", "#9a6700"), "forced": ("[F]", "#b35900")}
    for ch in meta["chapters"]:
        gtag, gcol = gmap.get(ch.get("grade", ""), ("", "#1a1a1a"))
        num = Paragraph("&sect;%d" % ch["no"], ParagraphStyle("n", parent=S["toc"],
                                                              fontName="Sans-Bold", textColor=ACCENT))
        title = Paragraph("%s <font color='#5b6168'>&nbsp;&mdash; %s</font>"
                          % (xml_escape(ch["title"]), xml_escape(ch["one_liner"])), S["toc"])
        grade = Paragraph("<font color='%s'>%s</font>" % (gcol, gtag),
                          ParagraphStyle("g", parent=S["toc"], alignment=TA_CENTER, fontName="Sans-Bold"))
        rows.append([num, title, grade])
    t = Table(rows, colWidths=[1.4 * cm, avail_w - 1.4 * cm - 1.4 * cm, 1.4 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.HexColor("#e6e8ea")),
    ]))
    flows.append(t)
    flows.append(PageBreak())
    return flows


# ---------------------------------------------------------------------------------------------------
# Running header / footer (content pages only; title page is clean)
# ---------------------------------------------------------------------------------------------------
def _decorate(canvas, doc):
    canvas.saveState()
    w, h = A4
    lm, rm = doc.leftMargin, doc.rightMargin
    # header
    canvas.setFont("Sans", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(lm, h - 1.25 * cm, "Aging and Senescence  \u00b7  Jamming Physics / VP Theory")
    canvas.drawRightString(w - rm, h - 1.25 * cm, HUB_URL)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(lm, h - 1.4 * cm, w - rm, h - 1.4 * cm)
    # footer
    canvas.setFont("Sans", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(lm, 1.05 * cm, "\u00a9 2026 %s  \u00b7  %s  \u00b7  DOI %s  \u00b7  SEED=19" %
                      (AUTHOR, CC, DOI_TBD))
    canvas.drawRightString(w - rm, 1.05 * cm, "%d" % canvas.getPageNumber())
    canvas.setLineWidth(0.4)
    canvas.line(lm, 1.3 * cm, w - rm, 1.3 * cm)
    canvas.restoreState()


def _blank(canvas, doc):
    pass


# ---------------------------------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------------------------------
def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked (research-first).")
        print("Reason:", why)
        return 1
    meta_path = os.path.join(DOCS, "_meta.json")
    if not os.path.exists(meta_path):
        print("REFUSED: canonical site not built. Run  python tools/build_docs.py  first.")
        return 1
    meta = json.load(open(meta_path, encoding="utf-8"))
    det = meta["determinism"]

    _register_fonts()
    S = _styles()
    os.makedirs(OUTDIR, exist_ok=True)

    LM = RM = 1.9 * cm
    TM = 1.9 * cm
    BM = 1.7 * cm
    avail_w = A4[0] - LM - RM

    doc = BaseDocTemplate(
        OUTPDF, pagesize=A4,
        leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
        title=TITLE_FULL, author=AUTHOR, subject="VP Theory \u2014 aging & senescence (capstone)",
        creator="build_pdf.py (VP-SPEC v1.8)", keywords="VP Theory, aging, senescence, R19, promoter gamma",
    )
    frame = Frame(LM, BM, avail_w, A4[1] - TM - BM, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="title", frames=[frame], onPage=_blank),
        PageTemplate(id="content", frames=[frame], onPage=_decorate),
    ])

    story = []
    story.append(NextPageTemplate("title"))
    story += title_page(meta, S, avail_w, det)
    story.append(NextPageTemplate("content"))
    story += toc_page(meta, S, avail_w)
    for i, ch in enumerate(meta["chapters"]):
        story += parse_chapter(ch["slug"], ch["no"], S, avail_w)
        if i != len(meta["chapters"]) - 1:
            story.append(PageBreak())

    doc.build(story)
    size = os.path.getsize(OUTPDF)
    print("Wrote %s  (%d chapters, %.1f KB)" % (os.path.relpath(OUTPDF, PKG),
                                                len(meta["chapters"]), size / 1024.0))
    print("DOI: %s (Zenodo concept DOI).  Hub: %s" % (DOI_TBD, HUB_URL))
    print("Source: canonical HTML in docs/ (numbers from the engine, C1).  Determinism SEED=19.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
