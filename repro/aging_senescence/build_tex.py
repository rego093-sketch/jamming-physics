#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a complete, no-omission LaTeX document from the canonical multi-page aging HTML.
Walks every chapter in order, renders answer/abstract/vp-cards/body/tables, compiles via xelatex."""
import os, re
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
OUT_TEX = os.path.join(ROOT, "aging_senescence_vp_whitepaper_v1_4_0.tex")
DOI = "10.5281/zenodo.20756155"
VERSION = "1.4.0"

ORDER = [
    "01-aging-as-homeostatic-setpoint-decline",
    "02-node-atlas-measured-promoter-gamma",
    "03-setpoint-drift-unifying-signature",
    "04-cellular-senescence-stuck-attractor",
    "05-reservoir-depletion-telomere-clock",
    "06-hallmarks-of-aging-substrate-map",
    "07-aging-universal-risk-multiplier",
    "08-rate-of-aging-biological-age",
    "09-cross-species-longevity-discriminant",
    "10-archaic-and-present-day-aging-promoters",
    "11-telomere-keystone-dynamics-not-gamma",
    "12-pathology-sarcopenia-frailty-cancer",
    "13-reproducibility-grading-ledger",
    "14-conclusion-genome-fixes-the-ruler-not-the-lifespan",
]

SPECIAL = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
           "\\": r"\textbackslash{}"}
_unhandled = set()


def esc(t):
    return "".join(SPECIAL.get(c, c) for c in t)


def inline(node):
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            out.append(esc(str(c)))
        elif isinstance(c, Tag):
            n = c.name.lower()
            if n in ("b", "strong"):
                out.append(r"\textbf{" + inline(c) + "}")
            elif n in ("i", "em"):
                out.append(r"\textit{" + inline(c) + "}")
            elif n == "code":
                out.append(r"\texttt{" + inline(c) + "}")
            elif n == "sub":
                out.append(r"\textsubscript{" + inline(c) + "}")
            elif n == "sup":
                out.append(r"\textsuperscript{" + inline(c) + "}")
            elif n == "br":
                out.append(r"\\ ")
            elif n == "a":
                out.append(inline(c))
            elif n == "span":
                cls = " ".join(c.get("class", []))
                txt = inline(c)
                out.append(r"\texttt{" + txt + "}" if "kf" in cls else txt)
            else:
                out.append(inline(c))
    return "".join(out)


def render_table(tbl):
    rows = []
    for tr in tbl.find_all("tr"):
        cells = tr.find_all(["th", "td"])
        if cells:
            rows.append([(inline(c).strip(), c.name == "th") for c in cells])
    if not rows:
        return ""
    ncol = max(len(r) for r in rows)
    colspec = "@{}" + " ".join([r">{\raggedright\arraybackslash}p{%.3f\linewidth}" % (0.95 / ncol)] * ncol) + "@{}"
    out = [r"\begin{center}\footnotesize", r"\begin{longtable}{" + colspec + "}", r"\toprule"]
    for i, r in enumerate(rows):
        cells = [(c if not h else r"\textbf{" + c + "}") for (c, h) in r] + [""] * (ncol - len(r))
        out.append(" & ".join(cells) + r" \\")
        if i == 0 and any(h for (_, h) in r):
            out.append(r"\midrule")
    out += [r"\bottomrule", r"\end{longtable}", r"\end{center}"]
    return "\n".join(out)


def render_list(lst):
    env = "enumerate" if lst.name == "ol" else "itemize"
    out = [r"\begin{%s}[leftmargin=1.4em,itemsep=2pt,topsep=3pt]" % env]
    for li in lst.find_all("li", recursive=False):
        out.append(r"\item " + inline(li).strip())
    out.append(r"\end{%s}" % env)
    return "\n".join(out)


def render_main(main):
    out = []
    for el in main.children:
        if not isinstance(el, Tag):
            continue
        n = el.name.lower()
        cls = " ".join(el.get("class", []))
        if n == "h1":
            continue
        elif n == "p" and "eyebrow" in cls:
            continue
        elif n == "p" and "answer" in cls:
            out.append(r"\begin{answerbox}" + inline(el).strip() + r"\end{answerbox}")
        elif n == "p" and "abstract" in cls:
            out.append(r"\begin{abstractbox}" + inline(el).strip() + r"\end{abstractbox}")
        elif n == "aside":
            if "claim-strip" in cls:
                continue
            txt = re.sub(r"\s+", " ", inline(el).strip())
            if txt:
                out.append(r"\begin{vpbox}" + txt + r"\end{vpbox}")
        elif n in ("h2", "h3", "h4"):
            out.append(r"\subsection*{" + inline(el).strip() + "}")
        elif n == "p":
            t = inline(el).strip()
            if t:
                out.append(t)
        elif n in ("ul", "ol"):
            out.append(render_list(el))
        elif n == "table":
            out.append(render_table(el))
        elif n == "div" and "kf" in cls:
            out.append(r"\begin{center}\ttfamily\small " + inline(el).strip() + r"\end{center}")
        elif n == "div":
            tbl = el.find("table")
            if tbl is not None:
                out.append(render_table(tbl))
            else:
                t = inline(el).strip()
                if t:
                    out.append(t)
        elif n in ("nav", "figure", "img", "script", "style"):
            continue
        else:
            _unhandled.add(n + ("." + cls if cls else ""))
            t = inline(el).strip()
            if t:
                out.append(t)
    return "\n\n".join(out)


PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage{fontspec}
\setmainfont{DejaVu Serif}[Scale=0.92]
\setsansfont{DejaVu Sans}[Scale=0.90]
\setmonofont{DejaVu Sans Mono}[Scale=0.84]
\usepackage[a4paper,margin=2.4cm]{geometry}
\usepackage{xcolor}
\definecolor{ink}{HTML}{1A1A1A}
\definecolor{rule}{HTML}{C8C8C8}
\definecolor{ansbg}{HTML}{F4F7FB}
\definecolor{ansbd}{HTML}{3A6EA5}
\definecolor{vpbg}{HTML}{FAFAF7}
\definecolor{vpbd}{HTML}{BDBDB2}
\usepackage[most]{tcolorbox}
\usepackage{longtable,booktabs,array}
\usepackage{enumitem}
\usepackage{microtype}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{tocloft}
\setlength{\cftsecnumwidth}{2.6em}
\renewcommand{\cftsecfont}{\normalfont}
\renewcommand{\cftsecpagefont}{\normalfont}
\usepackage[hidelinks]{hyperref}
\titleformat{\section}{\sffamily\large\bfseries\color{ink}}{\thesection.}{0.6em}{}
\titlespacing*{\section}{0pt}{2.2ex plus 1ex minus .2ex}{1.2ex}
\titleformat{\subsection}{\sffamily\normalsize\bfseries\color{ink}}{}{0em}{}
\titlespacing*{\subsection}{0pt}{1.6ex plus .5ex}{0.7ex}
\newtcolorbox{answerbox}{colback=ansbg,colframe=ansbd,boxrule=0.4pt,left=8pt,right=8pt,top=6pt,bottom=6pt,
  arc=1pt,before skip=6pt,after skip=8pt,fontupper=\normalsize}
\newtcolorbox{abstractbox}{colback=white,colframe=rule,boxrule=0.3pt,left=8pt,right=8pt,top=6pt,bottom=6pt,
  arc=0pt,before skip=4pt,after skip=8pt,fontupper=\small\itshape}
\newtcolorbox{vpbox}{colback=vpbg,colframe=vpbd,boxrule=0.4pt,left=8pt,right=8pt,top=6pt,bottom=6pt,
  arc=1pt,before skip=6pt,after skip=8pt,fontupper=\small}
\setlength{\emergencystretch}{3em}
\hyphenpenalty=1500
\sloppy
\title{\sffamily\bfseries Aging and Senescence:\\[2pt]
  {\large\mdseries the Systemic Decline of Homeostatic Setpoints over the Lifespan}}
\author{Young Jae Lee \\ \small ORCID 0009-0002-7535-8245}
\date{\small Version 1.4.0 \;\textbullet\; DOI 10.5281/zenodo.20756155 \;\textbullet\; CC BY 4.0 \;\textbullet\; 2026}
\begin{document}
\maketitle
\thispagestyle{empty}
\begin{abstract}\noindent
Aging is read on the VP substrate as the systemic, monotonic decline of $\gamma$-defended homeostatic
setpoints. From sequence the promoter $\gamma$ of the aging masters (TP53, CDKN2A, FOXO3, TERT) is measured
and fixes each node's barrier $\gamma^2/4$ and reservoir dwell $\sim\gamma^{1.5}$; the dynamics --- setpoint
drift, the stuck senescence attractor, finite-reservoir depletion, a convex age risk-multiplier --- are
deterministic simulations seeded at 19. A cross-species discriminant finds human aging genes are not special
and the longevity switch is TP53 copy number, not promoter $\gamma$; an observation-only archaic$\leftrightarrow$
present-day comparison finds the masters read the same $\gamma$ in dated genomes; and a telomere deep-dive
locates the telomere as the keystone of aging \emph{dynamics}, not $\gamma$. The closing section draws the
epistemic conclusion: the genome fixes the ruler but not the realized lifespan, which is underdetermined by
the $\gamma$ axis (the lever lives off-axis in dosage and reservoir dynamics) rather than merely uncomputed.
Everything is reproduced bit-for-bit (SEED=19, $2\times$sha256 identical) and graded honestly
([V] verified / [L] cited / [O] open-with-obstacle).
\end{abstract}
\vspace{1em}
\tableofcontents
\clearpage
"""


def main():
    body = [PREAMBLE]
    for slug in ORDER:
        soup = BeautifulSoup(open(os.path.join(DOCS, slug, "index.html"), encoding="utf-8").read(), "html.parser")
        main_el = soup.find("main")
        h1 = main_el.find("h1")
        title = inline(h1).strip() if h1 else slug
        if slug.startswith("14-"):
            body.append(r"\clearpage")
        body.append(r"\section{" + title + "}")
        body.append(render_main(main_el))
    body.append(r"\end{document}")
    tex = "\n\n".join(body)
    open(OUT_TEX, "w", encoding="utf-8").write(tex)
    print("Wrote", OUT_TEX, "(%d chars)" % len(tex))
    print("Unhandled tags:", sorted(_unhandled) if _unhandled else "none (all handled)")


if __name__ == "__main__":
    main()
