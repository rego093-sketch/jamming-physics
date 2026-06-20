#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_tex.py -- Special-Sense Organs PUBLICATION phase: deterministic LaTeX whitepaper generator.

"Code is the agent" (VP-SPEC v1.8 sec 1): the .tex is rendered from the SAME authored chapter data
(_sns_content) and the SAME verified corpus (reports/emergence_results.json, 2xsha256 6a68bc48...) that
build the canonical HTML, so the PDF cannot drift from the site -- every quantity is injected from the
corpus, never re-typed. The PDF front matter carries the concept DOI and the "Living version" line
(hub URL + DOI) required by VP-SPEC sec "Academic channel alignment".

Output: dist/sensory_organ_vp_site.tex  (compile with tools/build_pdf.sh -> dist/sensory_organ_vp_site.pdf)

HARD RULE inherited from build_docs: refuses while writing is locked (research must be signed off).
Reproducibility: no wall-clock (BUILD_DATE fixed); compile with SOURCE_DATE_EPOCH + \\pdfinfoomitdate so
the PDF bytes are stable across runs.
"""
import os, sys, json
from html.parser import HTMLParser

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.join(_HERE, "..")
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_verify"))
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_pathology"))
import importlib
gates = importlib.import_module("gates")
render = importlib.import_module("_sns_render")     # single source for identity/DOI/site/date
content = importlib.import_module("_sns_content")

SITE = render.SITE
DOI = render.DOI
DOI_URL = render.DOI_URL
HUB_URL = render.HUB_URL
AUTHOR = render.AUTHOR
ORCID = render.ORCID
LICENSE = render.LICENSE
BUILD_DATE = render.BUILD_DATE
PAPER = render.PAPER
REPRO_BASE = render.REPRO_BASE
VERSION = open(os.path.join(_PKG, "VERSION"), encoding="utf-8").read().strip()

# ----------------------------------------------------------------- corpus
def _load_corpus():
    res = json.load(open(os.path.join(_PKG, "reports", "emergence_results.json"), encoding="utf-8"))
    path = importlib.import_module("setpoint_failure").status()
    treat = importlib.import_module("treatment").status()
    rc = json.load(open(os.path.join(_PKG, "reports", "research_complete.json"), encoding="utf-8"))
    return res, path, treat, rc

# ----------------------------------------------------------------- text -> LaTeX
# every non-ASCII character that occurs in the authored corpus (audited), mapped to a pdflatex command
_UNI = {
    "\u00b2": r"\textsuperscript{2}", "\u00b3": r"\textsuperscript{3}",
    "\u00b5": r"$\mu$", "\u00b7": r"$\cdot$", "\u00bd": r"$\tfrac{1}{2}$",
    "\u00d7": r"$\times$", "\u00ed": r"\'{\i}", "\u00fc": r'\"{u}',
    "\u0394": r"$\Delta$", "\u03b1": r"$\alpha$", "\u03b2": r"$\beta$",
    "\u03b3": r"$\gamma$", "\u03bc": r"$\mu$", "\u03c9": r"$\omega$",
    "\u2009": r"\,", "\u2013": r"--", "\u2014": r"---",
    "\u2019": r"'", "\u201c": r"``", "\u201d": r"''", "\u2026": r"\dots{}",
    "\u2032": r"$'$", "\u207a": r"\textsuperscript{+}", "\u2080": r"$_0$",
    "\u2192": r"$\rightarrow$", "\u2212": r"$-$", "\u223c": r"$\sim$",
    "\u2248": r"$\approx$", "\u2265": r"$\geq$", "\u2264": r"$\leq$",
    "\u00b0": r"$^\circ$", "\u00b1": r"$\pm$", "\u2261": r"$\equiv$",
}
_SPECIAL = [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
            ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
            ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]

def esc_text(s):
    """Escape LaTeX specials in raw text, THEN map audited Unicode to LaTeX commands (order matters:
    the Unicode replacements introduce backslashes/braces/dollars that must not be re-escaped)."""
    for a, b in _SPECIAL:
        s = s.replace(a, b)
    for u, t in _UNI.items():
        s = s.replace(u, t)
    return s

def abs_url(href):
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("/"):
        return SITE + href
    return href

class _H2T(HTMLParser):
    """Convert the limited inline HTML used in the corpus (b,i,code,sup,span,a) to LaTeX.
    convert_charrefs=True (default) means &amp;/&gamma;/&#xNN; arrive already decoded to Unicode."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "b":     self.out.append(r"\textbf{")
        elif tag == "i":   self.out.append(r"\textit{")
        elif tag == "code":self.out.append(r"\texttt{")
        elif tag == "sup": self.out.append(r"\textsuperscript{")
        elif tag == "a":
            self.out.append(r"\href{%s}{" % abs_url(a.get("href", "")))
        elif tag == "span":self.out.append(r"{")          # span.num etc: transparent group
        else:              self.out.append(r"{")
    def handle_endtag(self, tag):
        self.out.append(r"}")
    def handle_data(self, data):
        self.out.append(esc_text(data))
    def result(self):
        return "".join(self.out)

def tex(html_str):
    p = _H2T(); p.feed(html_str); p.close()
    return p.result()

def plain_len(html_str):
    import re
    return len(re.sub(r"<[^>]+>", "", html_str))

def guard(s):
    """Protect content that begins with '[' so it is not parsed as the optional argument of a
    preceding \\\\, \\midrule, \\toprule, or \\begin{tcolorbox}."""
    return ("{}" + s) if s.lstrip().startswith("[") else s

# ----------------------------------------------------------------- block renderers
def render_table(caption, headers, rows):
    ncols = len(headers)
    # deterministic column weights from content length (soft floor via +K), normalised to sum == ncols
    lens = []
    for j in range(ncols):
        m = plain_len(headers[j])
        for r in rows:
            m = max(m, plain_len(r[j]))
        lens.append(m)
    K = 10.0
    w = [l + K for l in lens]
    s = sum(w)
    w = [ncols * x / s for x in w]
    colspec = "".join(r"R{%.4f}" % x for x in w)
    hcells = [r"\textbf{%s}" % tex(h) for h in headers]
    hcells[0] = guard(hcells[0])
    head = " & ".join(hcells) + r" \\"
    body = []
    for r in rows:
        cells = [tex(c) for c in r]
        cells[0] = guard(cells[0])
        body.append(" & ".join(cells) + r" \\")
    return ("\\begin{table}[H]\n\\footnotesize\n\\renewcommand{\\arraystretch}{1.25}\n"
            "\\caption{%s}\n"
            "\\begin{tabularx}{\\linewidth}{%s}\n\\toprule\n%s\n\\midrule\n%s\n\\bottomrule\n"
            "\\end{tabularx}\n\\end{table}\n") % (tex(caption), colspec, head, "\n".join(body))

def render_body(body):
    out = []
    for b in body:
        kind = b[0]
        if kind == "p":
            out.append(tex(b[1]) + "\n")
        elif kind == "h2":
            out.append(r"\subsection*{%s}" % tex(b[1]) + "\n")
        elif kind == "h3":
            out.append(r"\subsubsection*{%s}" % tex(b[1]) + "\n")
        elif kind == "ul":
            items = "\n".join(r"  \item %s" % tex(x) for x in b[1])
            out.append("\\begin{itemize}[leftmargin=1.2em,itemsep=2pt,topsep=3pt]\n%s\n\\end{itemize}\n" % items)
        elif kind == "t":
            out.append(render_table(b[1], b[2], b[3]))
        elif kind == "bound":
            out.append("\\begin{boundbox}\n%s\n\\end{boundbox}\n" % guard(tex(b[1])))
    return "\n".join(out)

GRADE_NAME = {"verified": "[V] verified", "calibrated": "[L] calibrated",
              "forced": "[O] open", "open": "[O] open", "hypothesis": "[H] hypothesis"}

def render_chapter(ch):
    parts = []
    parts.append(r"\section{%s}" % tex(ch["title"]))
    parts.append(r"\label{sec:%s}" % ch["slug"])
    # grade + answer-first block
    parts.append(r"\noindent{\small\textsc{Grade:} \textbf{%s}}\par\vspace{2pt}" % tex(GRADE_NAME.get(ch["grade_kind"], ch["grade_kind"])))
    parts.append("\\begin{answerbox}\n%s\n\\end{answerbox}\n" % guard(tex(ch["answer"])))
    # abstract
    parts.append(r"\noindent{\small\itshape %s}\par\vspace{4pt}" % tex(ch["abstract"]))
    # body
    parts.append(render_body(ch["body"]))
    # locked-quantity card(s)
    for c in ch.get("cards", []):
        parts.append("\\begin{cardbox}\n%s\n\\end{cardbox}\n" % guard(tex(c)))
    return "\n".join(parts)

# ----------------------------------------------------------------- front matter
def results_table(F):
    rows = [
        ("PAX6 promoter stiffness $\\gamma$ (eye)", "%s" % F["g_pax6"], "[V]"),
        ("RAX promoter stiffness $\\gamma$ (photoreceptor)", "%s" % F["g_rax"], "[V]"),
        ("EYA1 promoter stiffness $\\gamma$ (cochlear map)", "%s" % F["g_eya1"], "[V]"),
        ("SOX2 promoter stiffness $\\gamma$ (hair cell)", "%s" % F["g_sox2"], "[V]"),
        ("TAS1R3 promoter stiffness $\\gamma$ (taste)", "%s" % F["g_tas"], "[V]"),
        ("Cochlear Hopf compression exponent at criticality", "%s ($=1/3$)" % F["comp_num"], "[V]"),
        ("Small-signal gain at the bifurcation ($\\mu=0$)", "%s$\\times$" % F["gain0"], "[V]"),
        ("Reduced-eye emmetropic axial length", "%s\\,mm" % F["axial"], "[V-arith]"),
        ("Ocular axial sensitivity", "%s\\,D/mm" % F["dpm"], "[V-arith]"),
        ("Greenwood place-map span (apex--base)", "%s\\,Hz--%s\\,kHz" % (F["gw_apex"], F["gw_base_k"]), "[L]"),
        ("Semicircular-canal velocity-band flatness", "%s" % F["flat"], "[V]"),
        ("Vestibulo-ocular reflex gain", "$\\sim$%s" % F["vor"], "[L]"),
        ("Restoration demo: recovered basin depth", "%s\\%%" % F["rd_rec"], "[V-dir]"),
    ]
    head = r"\textbf{Locked quantity} & \textbf{Value} & \textbf{Grade} \\"
    body = "\n".join("%s & %s & %s \\\\" % (n, v, g) for n, v, g in rows)
    return ("\\begin{table}[H]\n\\footnotesize\n\\renewcommand{\\arraystretch}{1.25}\n"
            "\\caption{Locked quantities reproduced by \\texttt{python repro/run\\_all.py} "
            "($2\\times$sha256 identical).}\n"
            "\\begin{tabularx}{\\linewidth}{R{1.85}R{0.75}R{0.40}}\n\\toprule\n%s\n\\midrule\n%s\n\\bottomrule\n"
            "\\end{tabularx}\n\\end{table}\n") % (head, body)

def title_page(F, rc):
    order = " $\\rightarrow$ ".join(tex(x.replace("_", " ")) for x in F["order"])
    abstract = (
        "The special-sense organs are derived here as physical instruments on a single jamming substrate. "
        "Their nodes are not assumed: the eye (PAX6, $\\gamma=%s$), photoreceptor (RAX, $%s$), cochlear "
        "frequency map (EYA1, $%s$), hair cell (SOX2, $%s$), and taste organ (TAS1R3, $%s$) each emerge from a "
        "single measured quantity --- the DNA stacking stiffness $\\gamma$ of its master gene --- and sorting "
        "those five values gives a developmental order whose falsifiable signal (taste specified latest) is "
        "confirmed. The cellular transducer at every special sense is the same object: a cooperative, bistable "
        "ion channel, an R19 double well. The organ-level optics and acoustics (the reduced eye, the Greenwood "
        "tonotopic place map, the semicircular-canal torsion pendulum) are classical physics --- documented and "
        "cited, not re-derived --- and the cochlear active amplifier, poised at a Hopf bifurcation, yields a "
        "parameter-free cube-root compression law $R=(F/\\beta)^{1/3}$. Disease is one quadratic basin collapse "
        "of a defended setpoint, and root-cause therapy is its inverse substrate operation, instantiated for "
        "seven common eye and ear diseases with contested results flagged honestly. Every quantity is a measured "
        "input or a derived value (never tuned); results are bit-for-bit reproducible."
        % (F["g_pax6"], F["g_rax"], F["g_eya1"], F["g_sox2"], F["g_tas"]))
    sha = rc["result_sha256"]
    return r"""\thispagestyle{empty}
\begin{center}
{\footnotesize\textsc{Jamming Physics whitepaper family}\par}
\vspace{1.2em}
{\LARGE\bfseries Special-Sense Organ Dynamics:\\[2pt]
Ocular Optics, Cochlear Frequency Analysis, and Vestibular Balance\par}
\vspace{1.0em}
{\large %s\par}
{\small\href{%s}{ORCID 0009-0002-7535-8245}\par}
\vspace{0.6em}
{\small Independent researcher \quad$\cdot$\quad \href{%s}{jamming-physics.org}\par}
\vspace{1.0em}
{\small\bfseries Living version:} {\small \href{%s}{%s%s} \quad$\cdot$\quad \href{%s}{doi.org/%s}}\par
\vspace{0.3em}
{\footnotesize Concept DOI \href{%s}{%s} (resolves to the latest version) \quad$\cdot$\quad
License \href{%s}{CC BY 4.0} \quad$\cdot$\quad Version %s \quad$\cdot$\quad %s}\par
\end{center}
\vspace{0.6em}
\begin{abstractbox}
\noindent\textbf{Abstract.}\, %s
\end{abstractbox}
\vspace{0.2em}
\begin{center}{\footnotesize Developmental order (argsort of measured $\gamma$):\; %s}\end{center}
%s
\begin{center}\footnotesize
Reproducible: \texttt{python repro/run\_all.py} \;$\cdot$\; SEED-fixed, $2\times$sha256 identical
(\texttt{%s}\dots) \;$\cdot$\; RS1--RS5 PASS, \texttt{all\_green=%s}.
\end{center}
\clearpage
""" % (
        tex(AUTHOR), ORCID, SITE,
        SITE + HUB_URL, esc_text(SITE + HUB_URL[:-1]), "/", DOI_URL, DOI,
        DOI_URL, DOI, LICENSE, esc_text(VERSION), BUILD_DATE,
        abstract, order, results_table(F),
        sha[:16], str(rc["all_green"]).lower())

LEGEND = r"""\section*{Grading discipline}
\addcontentsline{toc}{section}{Grading discipline}
Every claim carries one grade, the falsifiability mechanism of this program:
\begin{description}[leftmargin=2.4em,style=nextline,itemsep=2pt,topsep=3pt]
\item[{[V]}] verified in-simulation from the substrate (and \textbf{[V-arith]} a closed-form
  arithmetic result; \textbf{[V-dir]} a verified direction, not an absolute magnitude).
\item[{[L]}] calibrated or cited --- a measured input or an established external result, listed with
  its accession or citation in the references chapter.
\item[{[O]}] open, stated with its obstacle: the claim is not closed and the missing ingredient is named.
\item[{[H]}] hypothesis --- a stated modelling assumption (e.g.\ the cochlear amplifier sitting at $\mu=0$).
\end{description}
\noindent The discipline is \emph{no tuning}: every quantity is either a measured input or a value derived
from the substrate; none is chosen to hit a target. The same inputs reproduce the same numbers bit-for-bit.
\clearpage
"""

# ----------------------------------------------------------------- preamble
def preamble():
    return r"""\documentclass[11pt]{article}
% --- reproducible PDF: omit creation/mod dates and fix the trailer id (compile with SOURCE_DATE_EPOCH) ---
\pdfinfoomitdate=1
\pdftrailerid{}
\pdfsuppressptexinfo=-1
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{mathptmx}
\usepackage[scaled=0.92]{helvet}
\usepackage{courier}
\usepackage[a4paper,margin=2.5cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage[protrusion=true,expansion=false]{microtype}
\usepackage{array}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{float}
\usepackage{caption}
\captionsetup{labelformat=empty,font={footnotesize,it},justification=centering,skip=4pt}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{parskip}
\usepackage[most]{tcolorbox}
\usepackage{xcolor}
\usepackage[colorlinks=true,allcolors=accent,breaklinks=true,
  pdfauthor={Young Jae Lee},
  pdftitle={Special-Sense Organ Dynamics: Ocular Optics, Cochlear Frequency Analysis, and Vestibular Balance},
  pdfsubject={Jamming Physics whitepaper family},
  pdfkeywords={special-sense organs, DNA stacking stiffness, R19 bistable transducer, cochlear Hopf amplifier, vestibular, jamming physics}]{hyperref}

\definecolor{accent}{HTML}{1F4E6B}
\definecolor{ansbg}{HTML}{EEF4F8}
\definecolor{cardbg}{HTML}{F6F3EC}
\definecolor{boundbg}{HTML}{F4F4F4}
\definecolor{rule}{HTML}{C8D4DC}

% weighted, wrapping tabularx column
\newcolumntype{R}[1]{>{\hsize=#1\hsize\raggedright\arraybackslash}X}

\titleformat{\section}{\large\bfseries\sffamily\color{accent}}{\thesection}{0.6em}{}
\titleformat{\subsection}{\normalsize\bfseries\sffamily}{\thesubsection}{0.5em}{}
\titlespacing*{\section}{0pt}{1.4em}{0.5em}

\newtcolorbox{answerbox}{breakable,enhanced,colback=ansbg,colframe=accent,boxrule=0pt,
  leftrule=2.5pt,arc=1pt,left=8pt,right=8pt,top=6pt,bottom=6pt,
  fontupper=\normalsize}
\newtcolorbox{abstractbox}{breakable,enhanced,colback=ansbg,colframe=rule,boxrule=0.4pt,
  arc=1pt,left=10pt,right=10pt,top=8pt,bottom=8pt}
\newtcolorbox{cardbox}{breakable,enhanced,colback=cardbg,colframe=cardbg,boxrule=0pt,
  leftrule=2.5pt,colframe=accent,arc=1pt,left=8pt,right=8pt,top=5pt,bottom=5pt,
  fontupper=\small,before skip=6pt,after skip=8pt}
\newtcolorbox{boundbox}{breakable,enhanced,colback=boundbg,colframe=rule,boxrule=0.4pt,
  arc=1pt,left=8pt,right=8pt,top=5pt,bottom=5pt,fontupper=\small,
  before skip=6pt,after skip=8pt}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize\textsc{Special-Sense Organs}}
\fancyhead[R]{\footnotesize doi.org/""" + DOI + r"""}
\fancyfoot[C]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\headheight}{14pt}

\setcounter{tocdepth}{1}
\sloppy
"""

# ----------------------------------------------------------------- assemble
def build_tex():
    res, path, treat, rc = _load_corpus()
    F = content.build_F(res, path, treat)
    chs = content.chapters(F)
    doc = [preamble(), r"\begin{document}", title_page(F, rc), LEGEND,
           r"\tableofcontents", r"\clearpage"]
    for ch in chs:
        doc.append(render_chapter(ch))
        doc.append("")
    # closing colophon
    doc.append(r"""\bigskip
\begin{center}\footnotesize
\rule{0.4\linewidth}{0.3pt}\\[4pt]
\textbf{Special-Sense Organ Dynamics} \;$\cdot$\; %s (\href{%s}{ORCID})\;$\cdot$\;
\href{%s}{CC BY 4.0}\;$\cdot$\; Concept DOI \href{%s}{%s}\\[2pt]
Part of the Jamming Physics whitepaper family. Single-author, no-tuning, bit-for-bit reproducible.\\[2pt]
Reproduction code: \href{%s}{%s}
\end{center}""" % (tex(AUTHOR), ORCID, LICENSE, DOI_URL, DOI, REPRO_BASE, esc_text(REPRO_BASE)))
    doc.append(r"\end{document}")
    return "\n".join(doc), chs, F

def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing/publication is locked.\nReason:", why)
        return 1
    out_dir = os.path.join(_PKG, "dist")
    os.makedirs(out_dir, exist_ok=True)
    tex_str, chs, F = build_tex()
    tex_path = os.path.join(out_dir, "sensory_organ_vp_site.tex")
    open(tex_path, "w", encoding="utf-8").write(tex_str)
    print("WROTE %s" % tex_path)
    print("  chapters : %d" % len(chs))
    print("  DOI      : %s (concept)" % DOI)
    print("  version  : %s" % VERSION)
    print("  next     : tools/build_pdf.sh  ->  dist/sensory_organ_vp_site.pdf")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
