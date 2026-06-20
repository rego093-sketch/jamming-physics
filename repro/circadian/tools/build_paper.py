#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_paper.py  --  citation-layer PDF/TeX for the Chronobiology volume (VP-SPEC v1.8 §12.C, headed C2).

The canonical artifact is the docs/ HTML (C2). The PDF is the CITATION layer (Zenodo): it is generated
ON-DEMAND FROM THE CANONICAL HTML, never re-structured, so it cannot drift from the site. The .tex is the
on-demand source (extract.py role) and -- per headed C2 -- is NOT bundled into the reproducibility zip.

Output (to repro-zip-EXTERNAL paper/ dir): paper/circadian_vp_site.tex + circadian_vp_site.pdf
Page-1 line (§12.C): "Living version: <hub URL> | DOI <concept DOI>". PDF metadata filled. Absolute URLs.
Numbers are pulled LIVE from the engine (C1); the prose is extracted verbatim from the shipped HTML.
"""
import os, sys, re, json, importlib
from html.parser import HTMLParser

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.join(_HERE, "..")
sys.path.insert(0, os.path.join(_PKG, "repro", "_verify"))
sys.path.insert(0, os.path.join(_PKG, "repro", "_engine"))
gates = importlib.import_module("gates")

SITE = "https://jamming-physics.org"
HUB = f"{SITE}/circadian/"
CONCEPT_DOI = "10.5281/zenodo.20755413"
VERSION_DOI = "10.5281/zenodo.20755414"
MIND_DOI = "10.5281/zenodo.20694404"
AUTHOR = "Young Jae Lee"
ORCID = "0009-0002-7535-8245"
PUB_DATE = "2026-06-19"
DOCS = os.path.join(_PKG, "docs", "circadian")
KEYWORDS = ("circadian rhythm, circadian clock, chronobiology, limit-cycle oscillator, BMAL1, ARNTL, "
            "phase-response curve, Arnold tongue, entrainment, suprachiasmatic nucleus, HPA axis, "
            "shift work disorder, jet lag, chronotherapy, FitzHugh-Nagumo, jamming physics, VP theory, "
            "deterministic model, measured gamma, reproducibility")


def _sha():
    eng = importlib.import_module("vp_clk_engine")
    _, h = eng.emit(eng.circulate())
    return h


# ----------------------------------------------------------------------------- LaTeX escaping
_SPECIAL = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "$": r"\$", "&": r"\&",
            "#": r"\#", "^": r"\^{}", "_": r"\_", "%": r"\%", "~": r"\textasciitilde{}",
            "<": r"\textless{}", ">": r"\textgreater{}", "|": r"\textbar{}"}


def esc(s):
    out = []
    for ch in s:
        out.append(_SPECIAL.get(ch, ch))
    return "".join(out)


def absurl(href):
    if href.startswith("/"):
        return SITE + href
    return href


# ----------------------------------------------------------------------------- HTML -> LaTeX (streaming)
class Extractor(HTMLParser):
    """Walk <main>, emit LaTeX. Skip aside/nav/header/footer/script/style/h1 (title comes from meta)."""
    SKIP = {"aside", "nav", "header", "footer", "script", "style", "h1"}

    def __init__(self):
        super().__init__(convert_charrefs=True)  # entities -> unicode in handle_data
        self.buf = []
        self.in_main = False
        self.skip = 0
        self.p_class = None
        self.suppress_p = False  # for p.abstract (folded into the answer lead)

    def w(self, s):
        if self.in_main and self.skip == 0 and not self.suppress_p:
            self.buf.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.in_main = True; return
        if not self.in_main:
            return
        if self.skip:
            if tag in self.SKIP:
                self.skip += 1
            return
        if tag in self.SKIP:
            self.skip += 1; return
        if tag == "h2":
            self.buf.append("\n\\subsection{")
        elif tag == "h3":
            self.buf.append("\n\\subsubsection{")
        elif tag == "p":
            cls = a.get("class", "")
            self.p_class = cls
            if "abstract" in cls:
                self.suppress_p = True            # drop the per-section abstract (answer carries the lead)
            elif "answer" in cls:
                self.buf.append("\n\\begin{answerbox}\n")
            else:
                self.buf.append("\n")
        elif tag == "ul":
            self.buf.append("\n\\begin{itemize}\n")
        elif tag == "ol":
            self.buf.append("\n\\begin{enumerate}\n")
        elif tag == "li":
            self.w("\\item ")
        elif tag in ("strong", "b"):
            self.w("\\textbf{")
        elif tag in ("em", "i"):
            self.w("\\textit{")
        elif tag in ("span", "code"):
            if "mono" in a.get("class", "") or tag == "code":
                self.w("\\texttt{")
            else:
                self.w("{")
        elif tag == "a":
            self.w("\\href{" + absurl(a.get("href", "")) + "}{")
        elif tag == "br":
            self.w("\\\\\n")

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False; return
        if not self.in_main:
            return
        if self.skip:
            if tag in self.SKIP:
                self.skip -= 1
            return
        if tag == "h2":
            self.buf.append("}\n")
        elif tag == "h3":
            self.buf.append("}\n")
        elif tag == "p":
            if "abstract" in (self.p_class or ""):
                self.suppress_p = False
            elif "answer" in (self.p_class or ""):
                self.buf.append("\n\\end{answerbox}\n")
            else:
                self.buf.append("\n")
            self.p_class = None
        elif tag == "ul":
            self.buf.append("\n\\end{itemize}\n")
        elif tag == "ol":
            self.buf.append("\n\\end{enumerate}\n")
        elif tag in ("strong", "b", "em", "i", "a"):
            self.w("}")
        elif tag in ("span", "code"):
            self.w("}")

    def handle_data(self, data):
        if not data:
            return
        # collapse internal whitespace but keep a single space; preserve content
        self.w(esc(data))


def chapter_latex(path):
    html = open(path, encoding="utf-8").read()
    ex = Extractor()
    ex.feed(html)
    body = "".join(ex.buf)
    # tidy: collapse 3+ newlines, strip spaces before punctuation introduced by tag breaks
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = re.sub(r"[ \t]{2,}", " ", body)
    return body.strip()


# ----------------------------------------------------------------------------- document assembly
PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage{fontspec}
\usepackage{newunicodechar}
\newunicodechar{γ}{\ensuremath{\gamma}}
\newunicodechar{κ}{\ensuremath{\kappa}}
\newunicodechar{Δ}{\ensuremath{\Delta}}
\newunicodechar{×}{\ensuremath{\times}}
\newunicodechar{−}{\ensuremath{-}}
\newunicodechar{→}{\ensuremath{\rightarrow}}
\newunicodechar{↔}{\ensuremath{\leftrightarrow}}
\newunicodechar{…}{\ldots}
\newunicodechar{·}{\textperiodcentered}
\newunicodechar{§}{\textsection}
\usepackage[a4paper,margin=2.4cm]{geometry}
\usepackage{parskip}
\usepackage{xcolor}
\definecolor{vpink}{HTML}{0A7A4B}
\definecolor{vprule}{HTML}{D8D8D8}
\definecolor{vpbg}{HTML}{F6F8F7}
\usepackage[most]{tcolorbox}
\usepackage{enumitem}
\setlist{leftmargin=1.3em,topsep=2pt,itemsep=1pt}
\usepackage[colorlinks=true,linkcolor=vpink,urlcolor=vpink,citecolor=vpink]{hyperref}
\hypersetup{
  pdftitle={Chronobiology: the Circadian Oscillator Network, Entrainment, and Clock-Disruption Disease},
  pdfauthor={%(author)s},
  pdfsubject={A deterministic, DNA-seeded circadian oscillator model on the VP jamming-lattice (FitzHugh-Nagumo R19) substrate},
  pdfkeywords={%(keywords)s}
}
\newtcolorbox{answerbox}{colback=vpbg,colframe=vpink,boxrule=0.6pt,left=6pt,right=6pt,top=4pt,bottom=4pt,
  arc=1pt,before skip=4pt,after skip=6pt}
\newtcolorbox{livingbox}{colback=white,colframe=vprule,boxrule=0.6pt,left=8pt,right=8pt,top=5pt,bottom=5pt,arc=1pt}
\newtcolorbox{groundbox}{colback=vpbg,colframe=vprule,boxrule=0.6pt,left=8pt,right=8pt,top=6pt,bottom=6pt,arc=1pt,
  before skip=8pt,after skip=10pt}
\setcounter{secnumdepth}{2}
\setcounter{tocdepth}{1}
\renewcommand{\thesection}{\S\arabic{section}}
\usepackage{titlesec}
\titleformat{\section}{\Large\bfseries\color{vpink}}{\thesection}{0.6em}{}
\title{\vspace{-1.4cm}\bfseries Chronobiology: the Circadian Oscillator Network,\\ Entrainment, and Clock-Disruption Disease}
\author{%(author)s\\ \normalsize ORCID \href{https://orcid.org/%(orcid)s}{%(orcid)s}\\ \normalsize Jamming Physics --- VP Theory programme}
\date{\normalsize Published %(pubdate)s \,\textbullet\, CC BY 4.0}
\begin{document}
\maketitle
\thispagestyle{empty}

\begin{livingbox}
\small\textbf{Living version (canonical):} \href{%(hub)s}{%(hub)s} \quad\textbullet\quad
\textbf{DOI:} \href{https://doi.org/%(concept)s}{%(concept)s} (concept; resolves to the latest version)\\
\textbf{Version snapshot:} \href{https://doi.org/%(version)s}{%(version)s} \quad\textbullet\quad
\textbf{License:} \href{https://creativecommons.org/licenses/by/4.0/}{CC BY 4.0} \quad\textbullet\quad
\textbf{Author:} %(author)s (ORCID %(orcid)s)
\end{livingbox}

\begin{abstract}
\noindent The $\sim$24\,hour circadian clock is modelled as a \textbf{self-sustained coupled limit-cycle
oscillator network} (suprachiasmatic master plus peripheral clocks) on the VP jamming-lattice
(FitzHugh--Nagumo, R19) substrate: it free-runs, is entrained by light through a biphasic phase-response
curve, synchronises as a master-led network, and \emph{gates} defended homeostatic setpoints (worked case:
the HPA cortisol axis). Disease is \textbf{clock--environment misalignment} (shift work, jet lag), and the
mind volume's explicitly locked \emph{circadian depression contributor} is supplied as a sign-only seam.
This is a \textbf{deterministic derivation seeded by a measured clock-gene} property, not a fitted toy
simulation: the molecular loop carries a measured BMAL1/ARNTL well $\gamma=1.33348$ (never fitted), every
number is produced by one engine (seed${=}$19, byte-identical on re-run) across eight falsifiable
discriminants, the $\sim$24\,h period is the only cited anchor, and the felt quality of mood stays in the
mind volume (efficacy${=}$0; not medical advice).
\end{abstract}

\begin{groundbox}
\small\textbf{Reproducibility \& grounding (read first).}
The molecular clock node is seeded by a \emph{measured} property of the real human clock gene: the well depth
$\gamma=1.33348$ of \textbf{ARNTL (alias BMAL1)} (NCBI Gene ID 406, accession NC\_000011.10), computed as
$-\mathrm{mean}$(NN stacking $\Delta G_{37}$, SantaLucia 1998) over the 2500 dinucleotides of the proximal
promoter (TSS$-2000..+500$) through the framework's shared DNA pipeline; the 2501-base promoter is cached
(sha256 \texttt{7293be92e4ad}\dots) so $\gamma$ reproduces offline. It is a measured input graded
\textbf{[V]}, never fitted. Every dynamical number in this paper is produced by one deterministic engine
(seed${=}$19) whose aggregate result hashes \emph{identically twice} (sha256
\texttt{%(sha12)s}\dots), and the eight discriminants (RC1--RC6 $+$ TX1) are \textbf{falsifiable}. No new
physical constant is introduced; the FitzHugh--Nagumo (R19) substrate is vendored byte-identical and merely
run in its oscillatory window. The absolute period is the only cited \textbf{[L]} anchor; every \textbf{[O]}
quantity is logged with its obstacle. Full reproduction code: \href{%(hub)s}{the living site} and its
GitHub \texttt{repro/circadian/} tree, frozen on Zenodo (DOI %(concept)s).
\end{groundbox}

\tableofcontents
\bigskip
"""

POSTAMBLE = r"""
\vfill
\noindent\rule{\linewidth}{0.4pt}\\
\footnotesize This PDF is the citation layer of a living document; the canonical, continuously-updated version
is the HTML at \href{%(hub)s}{%(hub)s}. Cross-volume affect seam cites the mind volume
(\href{https://doi.org/%(mind)s}{%(mind)s}); only a \emph{sign} crosses that seam (magnitude owned by mind;
\texttt{consciousness\_claim${=}$0; efficacy${=}$0}). \textbf{Not medical advice.} \copyright\ %(author)s,
licensed \href{https://creativecommons.org/licenses/by/4.0/}{CC BY 4.0}.
\end{document}
"""

CHAPTERS = [
    ("00-grounding-measured-dna-emergence", "Grounding: measured DNA emergence, determinism, and falsifiable discriminants"),
    ("01-scope-clock-oscillator", "Scope: the circadian clock as a self-sustained oscillator network"),
    ("02-free-running", "Free-running: the molecular clock self-sustains a rhythm with no input"),
    ("03-entrainment-prc", "Entrainment: the phase-response curve and the Arnold tongue"),
    ("04-master-vs-network", "Master vs network: coupled clocks synchronise, master-led"),
    ("05-setpoint-gating", "Setpoint gating: the clock imposes a daily rhythm on the HPA axis"),
    ("06-misalignment-disease", "Misalignment: shift work, jet lag, and the dysregulated setpoint"),
    ("07-circadian-mood-seam", "The circadian--mood seam: supplying the contributor mind locked"),
    ("08-chronotherapy", "Chronotherapy: re-aligning the clock with the PRC"),
]


def build_tex():
    sha = _sha()
    ctx = {"author": AUTHOR, "orcid": ORCID, "pubdate": PUB_DATE, "hub": HUB,
           "concept": CONCEPT_DOI, "version": VERSION_DOI, "mind": MIND_DOI,
           "keywords": KEYWORDS, "sha12": sha[:12]}
    parts = [PREAMBLE % ctx]
    parts.append("\\setcounter{section}{-1}\n")  # first \section -> §0
    for slug, title in CHAPTERS:
        path = os.path.join(DOCS, slug, "index.html")
        body = chapter_latex(path)
        parts.append("\n\\section{" + esc(title.replace("--", "—")) + "}\n")
        parts.append(body + "\n")
    parts.append(POSTAMBLE % ctx)
    return "".join(parts), sha


def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        return 1
    outdir = os.path.join(_PKG, "..", "paper")  # EXTERNAL to the repro zip (headed C2)
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)
    tex, sha = build_tex()
    tex_path = os.path.join(outdir, "circadian_vp_site.tex")
    open(tex_path, "w", encoding="utf-8").write(tex)
    print("wrote", tex_path, "(engine sha %s…)" % sha[:12])
    print("compile: xelatex -interaction=nonstopmode circadian_vp_site.tex  (run twice for TOC)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
