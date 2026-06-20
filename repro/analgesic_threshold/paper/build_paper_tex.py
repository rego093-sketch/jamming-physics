#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_paper_tex.py — emit the Zenodo whitepaper (LaTeX) for analgesic_threshold_logic v2.0.
All gamma / |h_sp| / corr values are read byte-faithfully from the canonical engine JSON.
Compile:  pdflatex -interaction=nonstopmode paper.tex   (run twice for refs/toc)
"""
import json, os, re

PKG = "/home/claude/work/analgesic_handover_v1_to_v2/analgesic_threshold_logic_v2_0"
TMAP = json.load(open(f"{PKG}/repro/03-threshold-map/expected/threshold_map.json"))["entries"]
PRIO = json.load(open(f"{PKG}/repro/10-burden-prioritisation/expected/priority_ranking.json"))
PREC = json.load(open(f"{PKG}/repro/12-precision-local-anaesthesia/expected/precision_block_map.json"))
GATE = json.load(open(f"{PKG}/repro/02-read-nav-channels/expected/nav_gate.json"))
CORR = GATE["corr_gamma_gc_alltargets"]            # 0.998978
NCORR = GATE["n_targets_for_corr"]                 # 27
by_gene = {e["gene"]: e for e in TMAP}

LEVER_NAME = {"L1": "L1 reduce inward current", "L1-adjacent": "L1 (adjacent)",
              "L2": "L2 increase outward K current", "L3": "L3 remove sensitising drive",
              "master": "master identity switch", "context": "context comparator"}
LEVER_ORDER = ["L1", "L1-adjacent", "L2", "L3", "master", "context"]

def T(s):
    """Escape arbitrary text for LaTeX and render a few domain symbols."""
    s = str(s)
    # protect voltage-gated channel tokens (Na_V1.8 etc.) before escaping underscores
    s = re.sub(r'\b(Na|Ca|K)_[Vv]\s*([0-9][0-9.]*)', r'@@\1V@@\2', s)
    repl = [('\\', r'\textbackslash{}'), ('&', r'\&'), ('%', r'\%'), ('$', r'\$'),
            ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}'),
            ('~', r'\textasciitilde{}'), ('^', r'\textasciicircum{}')]
    for a, b in repl:
        s = s.replace(a, b)
    s = re.sub(r'@@(Na|Ca|K)V@@([0-9][0-9.]*)', r'\\NaVx{\1}{\2}', s)
    s = (s.replace('Ca2+', r'Ca\textsuperscript{2+}').replace('Na+', r'Na\textsuperscript{+}')
           .replace('K+', r'K\textsuperscript{+}').replace('H+', r'H\textsuperscript{+}'))
    s = (s.replace('→', r'$\rightarrow$').replace('×', r'$\times$').replace('μ', r'$\mu$')
           .replace('≥', r'$\geq$').replace('≤', r'$\leq$').replace('ρ', r'$\rho$')
           .replace('–', '--').replace('—', '---').replace('γ', r'$\gamma$'))
    return s

def gbadge(tok):
    t = (tok or "").strip()[:3]
    return {"[V]": r"\gV", "[F]": r"\gF", "[O]": r"\gO", "[H]": r"\gH"}.get(t, r"\gO") + "{}"

def chan_tex(e):
    c = e.get("channel")
    if c:
        return T(c)
    return T(e.get("protein") or "")

# ---------- main 27-target table ----------
def table_targets():
    rows = []
    for lev in LEVER_ORDER:
        grp = [e for e in TMAP if e["lever"] == lev]
        if not grp:
            continue
        rows.append(r"\multicolumn{7}{l}{\cellcolor{lvbg}\textbf{" + T(LEVER_NAME[lev]) + r"}}\\")
        for e in grp:
            push = re.sub(r";.*$", "", e["push_direction"])  # first clause
            rows.append(" & ".join([
                r"\textbf{" + T(e["gene"]) + "}",
                chan_tex(e),
                T(e["lever"]),
                f'{e["gamma"]}',
                f'{e["spinodal_h_sp"]}',
                r"\footnotesize " + T(push),
                gbadge(e["grade_lever"]),
            ]) + r"\\")
    body = "\n".join(rows)
    return r"""\begin{footnotesize}
\renewcommand{\arraystretch}{1.18}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{1.55cm}>{\raggedright\arraybackslash}p{1.7cm}cS[table-format=1.4]S[table-format=1.6]>{\raggedright\arraybackslash}p{3.7cm}c@{}}
\caption{The 27-target map. $\gamma$ is read from each gene's human promoter; $|h_{sp}|=(2/3\sqrt{3})\,\gamma^{1.5}$ is its place on the R19 firing-threshold scale. Read grade is \gV{} and clinical-magnitude grade is \gO{} for all 27 (stated once, omitted from rows); the per-row grade is the lever/mechanism grade: \gF{} for the 16 direct-channel targets, \gO{} for the 11 indirect (L3 sensitiser, master, comparator) targets.}\label{tab:map}\\
\toprule
\textbf{Gene} & \textbf{Channel/Protein} & \textbf{Lever} & {$\gamma$} & {$|h_{sp}|$} & \textbf{Direction (cited)} & \textbf{Gr.}\\
\midrule
\endfirsthead
\toprule
\textbf{Gene} & \textbf{Channel/Protein} & \textbf{Lever} & {$\gamma$} & {$|h_{sp}|$} & \textbf{Direction (cited)} & \textbf{Gr.}\\
\midrule
\endhead
\midrule \multicolumn{7}{r}{\footnotesize continued on next page}\\
\endfoot
\bottomrule
\endlastfoot
""" + body + r"""
\end{longtable}
\end{footnotesize}"""

# ---------- prioritisation table (all actionable) ----------
def table_prio():
    rows = []
    for r in PRIO["ranking_actionable"]:
        mp = r.get("map_place", {})
        rows.append(" & ".join([
            f'{r["rank"]}',
            r"\textbf{" + T(r["gene"]) + "}",
            chan_tex({"channel": r.get("channel_or_protein")}),
            T(r["lever"]),
            f'{r["B_burden"]}', f'{r["U_unmet"]}', f'{r["D_druggability"]}',
            r"\textbf{" + f'{r["priority_score"]}' + "}",
            r"\footnotesize " + T(str(mp.get("gamma_h_sp", ""))),
        ]) + r"\\")
    body = "\n".join(rows)
    w = PRIO["weights_declared"]
    return (r"""\begin{footnotesize}
\renewcommand{\arraystretch}{1.15}
\begin{longtable}{@{}cl>{\raggedright\arraybackslash}p{1.7cm}cS[table-format=1.1]S[table-format=1.1]S[table-format=1.1]S[table-format=1.2]l@{}}
\caption{Burden-weighted prioritisation of the """ + str(PRIO["n_actionable"]) + r""" actionable targets. Score $=$ """
            + f'{w["B"]}' + r"$\cdot$B $+$ " + f'{w["U"]}' + r"$\cdot$U $+$ " + f'{w["D"]}'
            + r"""$\cdot$D over cited 1--5 tiers (B burden, U unmet need, D druggability). The $\gamma$/$|h_{sp}|$ map place is shown alongside but is \emph{never} folded into the score.}\label{tab:prio}\\
\toprule
\# & \textbf{Gene} & \textbf{Channel/Protein} & \textbf{Lever} & {B} & {U} & {D} & {Score} & \textbf{Map place}\\
\midrule
\endfirsthead
\toprule
\# & \textbf{Gene} & \textbf{Channel/Protein} & \textbf{Lever} & {B} & {U} & {D} & {Score} & \textbf{Map place}\\
\midrule
\endhead
\bottomrule
\endlastfoot
""" + body + r"""
\end{longtable}
\end{footnotesize}""")

# ---------- precision pairings ----------
def table_precision():
    rows = []
    for p in PREC["pairings"]:
        blk = T(p.get("blocker_target", ""))
        ch = p.get("blocker_channel")
        if ch:
            blk += r" (" + T(ch) + ")"
        rows.append(" & ".join([
            T(p.get("entry_port", "")),
            blk,
            r"\footnotesize " + T(p.get("hypothesis", "")),
        ]) + r"\\")
    body = "\n".join(rows) if rows else r"\multicolumn{3}{l}{(see precision\_block\_map.json)}\\"
    return (r"""\begin{footnotesize}
\renewcommand{\arraystretch}{1.2}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{2.2cm}>{\raggedright\arraybackslash}p{2.6cm}>{\raggedright\arraybackslash}p{8.0cm}@{}}
\caption{Precision local anaesthesia: a nociceptor-selective entry port $\times$ a permanently charged firing-threshold raiser that enters only through that open port. Mechanism shape \gF{}, anchored to Binshtok, Bean \& Woolf (2007); every differential-block magnitude is \gO{}.}\label{tab:prec}\\
\toprule
\textbf{Entry port} & \textbf{Charged blocker} & \textbf{Rationale (cited)}\\
\midrule
\endhead
\bottomrule
\endlastfoot
""" + body + r"""
\end{longtable}
\end{footnotesize}""")

# ---------- the document ----------
def document():
    abstract = (r"""A single jamming-lattice read --- Layer-1 $\gamma$, a nearest-neighbour stacking-energy read of the """
        r"""promoter --- is taken for 27 nociception (pain-sensing) genes and mapped onto the R19 firing-threshold """
        r"""scale, $|h_{sp}| = (2/3\sqrt{3})\,\gamma^{1.5}$. The reads are bit-reproducible: """
        rf"""$\mathrm{{corr}}(\gamma,\mathrm{{GC}})={CORR}$ over the {NCORR}-target set, drift $0$, offline. The """
        r"""central discipline is a firewall: $\gamma$ reads promoter switch-threshold \emph{structure} only and is """
        r"""never equated with any ion-channel activation voltage, candidate potency, dose, in-vivo selectivity, or """
        r"""clinical effect --- all of which are graded \gO{} (open) and asserted nowhere. The map sorts the targets """
        r"""into three intervention levers (reduce the inward current; increase the outward $\mathrm{K^+}$ current; """
        r"""remove the upstream sensitising drive), ranks them by a declared burden weighting, and adds a precision """
        r"""local-anaesthesia map. This is a free, public-benefit, \textbf{proposal-only} hypothesis: it designs no """
        r"""molecule and gives no dose, and every clinical magnitude requires external laboratory and clinical work. """
        r"""The complete reproducibility package (engines, cached inputs, gates, frozen hashes, manifest) regenerates """
        r"""every number and verdict deterministically and is released under CC BY 4.0.""")

    return r"""\documentclass[11pt]{article}
\usepackage[a4paper,margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{mathptmx}
\usepackage[scaled=0.92]{helvet}
\usepackage{courier}
\usepackage{amsmath,amssymb}
\usepackage{booktabs,longtable,array}
\usepackage{siunitx}
\sisetup{detect-all,table-number-alignment=center}
\usepackage[table]{xcolor}
\usepackage{microtype}
\usepackage{enumitem}
\setlist{nosep,leftmargin=1.4em}
\usepackage{parskip}
\usepackage[hidelinks,colorlinks=true,linkcolor=accent,urlcolor=accent,citecolor=accent]{hyperref}

\definecolor{accent}{RGB}{31,92,139}
\definecolor{gv}{RGB}{10,125,51}
\definecolor{gf}{RGB}{20,82,196}
\definecolor{go}{RGB}{154,99,0}
\definecolor{gh}{RGB}{106,63,176}
\definecolor{lvbg}{RGB}{244,247,250}
\definecolor{boxbg}{RGB}{247,249,251}

\newcommand{\gV}{\textcolor{gv}{\textbf{[V]}}}
\newcommand{\gF}{\textcolor{gf}{\textbf{[F]}}}
\newcommand{\gO}{\textcolor{go}{\textbf{[O]}}}
\newcommand{\gH}{\textcolor{gh}{\textbf{[H]}}}
\newcommand{\NaVx}[2]{\ensuremath{\mathrm{#1_{V}}}#2}
\newcommand{\code}[1]{\texttt{#1}}
\newcommand{\bzip}{\texttt{analgesic\_\allowbreak threshold\_\allowbreak logic\_\allowbreak v2\_\allowbreak 0\_\allowbreak reproducibility.zip}}

\hypersetup{
  pdftitle={A Reproducible, DNA-Grounded Map of 27 Non-Opioid Analgesic Targets},
  pdfauthor={Young Jae Lee},
  pdfkeywords={non-opioid analgesia; nociceptor; firing threshold; voltage-gated sodium channel; reproducible research; deterministic pipeline; drug target prioritisation}}

\title{\textbf{A Reproducible, DNA-Grounded Map of 27 Non-Opioid Analgesic Targets}\\[2pt]
\large Promoter switch-threshold ($\gamma$) reads sorted into three intervention levers,\\ with a firewall holding every clinical magnitude open}
\author{Young Jae Lee\\ \small ORCID \href{https://orcid.org/0009-0002-7535-8245}{0009-0002-7535-8245}\\
\small \href{https://jamming-physics.org/analgesic/}{jamming-physics.org/analgesic}\ \textbar\ \href{https://github.com/rego093-sketch/jamming-physics}{github.com/rego093-sketch/jamming-physics}}
\date{Version 2.0 \quad\textbullet\quad \today \quad\textbullet\quad CC BY 4.0 \quad\textbullet\quad DOI: this record}

\begin{document}
\maketitle
\thispagestyle{empty}

\begin{center}\fcolorbox{accent}{boxbg}{\parbox{0.95\linewidth}{\small
\textbf{Status.} Proposal / preprint. This document is a reproducible scientific \emph{hypothesis}, not medical advice and not a treatment. It identifies and prioritises molecular \emph{targets}; it designs no drug, gives no dose, and asserts no efficacy, potency, or safety result. Those can come only from proper laboratory and clinical validation, which this work does not perform.}}\end{center}

\begin{abstract}\noindent """ + abstract + r"""\end{abstract}

\section{Scope and the firewall}
This paper reads, for 27 genes central to nociception, a single structural number from DNA and uses it to organise a search for non-opioid analgesia. The non-negotiable boundary is a \textbf{firewall}: the read $\gamma$ is a property of a gene's promoter switch-threshold \emph{structure}. It is \emph{not} an ion channel's activation voltage, a drug candidate's potency, a dosing quantity, an in-vivo selectivity, or any clinical effect. Every such magnitude is graded \gO{} (open) and is asserted nowhere in this work. The engine reads structure; it never asserts a clinical number. Equating $\gamma$ with a clinical magnitude would be a category error and is treated as one throughout.

\section{Method: one read per gene}
Each gene's human promoter is read by a deterministic engine (a frozen module bundled in the reproducibility package). The read returns $\gamma$, a nearest-neighbour stacking-stiffness read of the promoter sequence (nearest-neighbour thermodynamics after SantaLucia, 1998 [1]). $\gamma$ is then mapped onto the R19 double-well firing-threshold scale,
\begin{equation}
|h_{sp}| \;=\; \frac{2}{3\sqrt{3}}\,\gamma^{1.5},
\end{equation}
which locates the gene on a common firing-threshold axis. The read is reproducible (\gV{}): across the 27-target set the read tracks base composition with $\mathrm{corr}(\gamma,\mathrm{GC})=""" + f"{CORR}" + r"""$ ($n=""" + f"{NCORR}" + r"""$), and the whole pipeline reproduces bit-for-bit (drift $0$, offline). The read fixes \emph{where} a gene sits and \emph{which lever} it belongs to; it never fixes a clinical magnitude.

\section{The map: 27 targets across three levers}
A pain fibre fires when its inward (depolarising) current overwhelms its outward (hyperpolarising) brake. The map intervenes along three levers, each of which raises the effective firing threshold: \textbf{L1} reduce the inward current ($\mathrm{Na^+}$, $\mathrm{Ca^{2+}}$, proton/ATP-gated); \textbf{L2} increase the outward $\mathrm{K^+}$ ($\mathrm{K_V}7$/M-current) brake; \textbf{L3} remove the upstream sensitising drive (nerve-growth-factor\,/\,TrkA and CGRP signalling). Two further groups are listed for completeness: the developmental master identity switch (PRDM12) and context comparators (opioid and cannabinoid receptors), routed deliberately away from the central reward circuitry that drives opioid addiction and respiratory risk. Table~\ref{tab:map} lists all 27 targets with their reads and grades. For the direct-channel levers the lever direction is anchored to cited agents (e.g.\ the FDA-approved $\mathrm{Na_V}1.8$ blocker) and graded \gF{}; for the indirect targets the gene is only placed in the map and the receptor/network mechanism is cited biology, never derived, and held \gO{}.

""" + table_targets() + r"""

\section{Burden-weighted prioritisation}
Targets are ranked by burden, unmet need, and druggability under a \emph{declared} editorial weighting --- not by their map place. The $\gamma$/$|h_{sp}|$ place is carried alongside each row but is never folded into the score (firewall: promoter stiffness $\neq$ clinical magnitude). Table~\ref{tab:prio} ranks the """ + str(PRIO["n_actionable"]) + r""" actionable targets; the """ + str(PRIO["n_comparators"]) + r""" comparators (""" + ", ".join(T(c["gene"]) for c in PRIO["comparators_context"]) + r""") are held out as non-actionable. The ranking is forced from cited tiers (\gF{}); it is not an engine output, and it recommends no dose or molecule.

""" + table_prio() + r"""

\section{Precision local anaesthesia}
A complementary idea makes the block \emph{pain-selective}: pair a nociceptor-selective entry port (a heat/irritant channel such as TRPV1 or TRPA1, open mainly in pain fibres) with a permanently charged firing-threshold raiser that cannot cross resting membranes and so enters only through that open port. The result is a differential block --- pain fibres silenced, motor and touch fibres largely spared. The mechanism shape (selective entry $\rightarrow$ selective block) is \gF{}, anchored to Binshtok, Bean \& Woolf (2007) [4]; named agents (e.g.\ QX-314, chloroprocaine) appear only as experimental anchors. The differential-block ratio, duration, and every other clinical magnitude are \gO{}. Table~\ref{tab:prec} lists the entry-port\,$\times$\,blocker pairings.

""" + table_precision() + r"""

\section{Proposals}
Six directional proposals follow from the map. Each is a hypothesis to be tested, not a result.
\begin{description}[leftmargin=2.2em,style=nextline]
\item[P1 --- Gate.] Intervene at the peripheral nociceptor gate rather than centrally.
\item[P2 --- Direction.] Push that gate so as to \emph{raise} the firing threshold (reduce inward current or increase outward current).
\item[P3 --- Axis.] Rank effectors by nociceptor selectivity and map place, pursuing the $\mathrm{Na_V}$ triad ($\mathrm{Na_V}1.7/1.8/1.9$) as the most selective inward-current axis.
\item[P4 --- Shape.] Favour a state-dependent mechanism that lifts the threshold of over-firing fibres while sparing ordinary low-frequency conduction.
\item[P5 --- Opioid alternative.] Pursue a peripheral, nociceptor-restricted intervention that is \emph{structurally} non-reward (it does not engage central reward circuitry).
\item[P6 --- Differential block.] Pursue pain-selective local anaesthesia via the entry-port\,$\times$\,charged-blocker construction above.
\end{description}

\section{Falsification}
A map that cannot be wrong is not science. Each proposal names the observation that would refute it: \textbf{P1/P2}, no threshold-driven reduction in nociceptive signalling in a controlled assay; \textbf{P3}, no nociceptor-selectivity advantage for the $\mathrm{Na_V}$ triad relative to the other levers; \textbf{P4}, a closed/inactivated-state stabiliser cannot lift the threshold while sparing low-frequency conduction; \textbf{P5}, a peripheral, nociceptor-restricted intervention nonetheless engages central reward circuitry; \textbf{P6}, opening the selective entry port does not confine the charged blocker to nociceptive fibres (no differential block). At the framework level, the open question (\gO{}) --- stated, not assumed --- is whether the promoter $\gamma$ read tracks expression-switch behaviour at these loci; if it does not, the Layer-1 grounding of the whole map is falsified.

\section{Grading and honesty}
Every claim carries one of three grades. \gV{} \textbf{verified / reproducible}: bit-reproducible from public promoter sequence (the 27 $\gamma$ reads; $\mathrm{corr}(\gamma,\mathrm{GC})=""" + f"{CORR}" + r"""$; drift $0$, offline). \gF{} \textbf{forced by the reads}: structural and not chosen (the ordering by $|h_{sp}|$; for the 16 direct-channel targets, the lever placement and direction, anchored to cited agents). \gO{} \textbf{open}: needs external laboratory/clinical data; asserted nowhere. \textbf{Every clinical magnitude is \gO{}.} The discipline is mechanical, not a promise: an \emph{L3-honesty gate} verifies that every upstream-sensitiser target carries an \gO{} cited-biology-never-derived mechanism grade; a \emph{forbidden-claim scanner} fails the build closed if any dosing, synthesis, efficacy, or safety claim appears in the asserted text; and an \emph{irreproducibility ledger} enumerates the open classes with their reasons. Section~\ref{sec:repro} shows how to run all of these.

\section{Reproducibility}\label{sec:repro}
This work is built so that every number and verdict can be regenerated from the inputs, offline and bit-for-bit. The reproducibility package accompanying this record (\bzip) contains the locked engines, the cited and cached input data, all gate scripts, the frozen output hashes, and a file manifest.

\paragraph{Principle: LOCK $\rightarrow$ Derive $\rightarrow$ Gate.} Every input is either a measured/cited quantity (locked) or is derived from locked inputs by a deterministic script --- never chosen to fit a target (the no-tuning invariant). Outputs are then verified by counting checks, and a set of output hashes is frozen so that any drift is detected.

\paragraph{Environment.} Python~3 with \code{NumPy}. All other engine modules are bundled inside the package; no network access is required (promoter sequences are cached in the package and the fetch path is cache-only).

\paragraph{One command.}
\begin{quote}\small\ttfamily
unzip \bzip\\
cd analgesic\_threshold\_logic\_v2\_0\\
python3 repro/run\_all.py
\end{quote}
Expected final lines:
\begin{quote}\small\ttfamily
[PASS] determinism --- 10 frozen hashes match (drift 0)\\
OVERALL: PASS (11/11 checks)
\end{quote}

\paragraph{What the checks verify.} The harness \code{repro/run\_all.py} runs eleven checks and then the determinism freeze:
\begin{footnotesize}
\renewcommand{\arraystretch}{1.15}
\begin{longtable}{@{}ll>{\raggedright\arraybackslash}p{8.6cm}@{}}
\toprule
\textbf{ID} & \textbf{Stage} & \textbf{Verifies}\\
\midrule
\endhead
\bottomrule
\endlastfoot
M1 & inherit-reverify & re-derives the inherited nociceptor $\gamma$ anchor; drift $0$\\
M8 & read-22-targets & reads the expanded target set from cached promoter sequence\\
M8 & gate (corr/drift/prov) & $\mathrm{corr}(\gamma,\mathrm{GC})=""" + f"{CORR}" + r"""$ ($n=""" + f"{NCORR}" + r"""$); drift $0$; provenance pinned\\
M9 & three-lever map & builds the 27-target threshold map and lever assignment\\
M4 & channelopathy anchor & cited human channelopathy biology fixes the lever direction\\
M10 & burden-prioritisation & reproduces the declared-weight ranking (Table~\ref{tab:prio})\\
M11 & L3-honesty (gate) & fail-closed: every L3 sensitiser mechanism is graded \gO{}\\
M12 & precision-local-anaes & reproduces the entry-port$\,\times\,$blocker map (Table~\ref{tab:prec})\\
M5 & claim-scan (gate) & fail-closed forbidden-claim scanner (dosing/synthesis/efficacy/safety)\\
M6 & falsification & a named falsifier is present for each proposal\\
\textemdash & determinism & 10 frozen output hashes match \code{repro/expected\_sha256.json}; drift $0$\\
\end{longtable}
\end{footnotesize}

\paragraph{File manifest.} Every shipped file is hashed in \code{manifest/SHA256SUMS.txt} (""" + str(count_manifest()) + r""" files). Verify with:
\begin{quote}\small\ttfamily
cd analgesic\_threshold\_logic\_v2\_0\\
sha256sum -c manifest/SHA256SUMS.txt
\end{quote}
(all lines report \code{OK}).

\paragraph{The open ledger.} \code{IRREPRODUCIBILITY\_LEDGER.md} lists every \gO{} (open) class with its reason --- the magnitudes this work deliberately does \emph{not} assert (potency, in-vivo selectivity, efficacy, safety, dose, formulation, and the framework-level expression-switch question). These are the boundary of the claim, recorded honestly rather than hidden.

\paragraph{Canonical edition.} A canonical, citable multi-page HTML edition (one self-contained page per target and per section, answer-first, with machine-readable metadata) is included under \code{docs/analgesic/} and is published at \href{https://jamming-physics.org/analgesic/}{jamming-physics.org/analgesic}.

\section*{License and reuse}
Released under \href{https://creativecommons.org/licenses/by/4.0/}{CC BY 4.0}. Reuse, adapt, and build on the reads and the lever map with attribution; commercial use is permitted, to lower the cost and broaden the search for non-opioid analgesics. All clinical magnitudes remain the reusing party's own scientific, ethical, and regulatory responsibility.

\section*{References}
\begin{footnotesize}
\begin{enumerate}[leftmargin=2.2em]
\item SantaLucia~J. (1998). A unified view of polymer, dumbbell, and oligonucleotide DNA nearest-neighbor thermodynamics. \emph{PNAS} 95(4):1460--1465.
\item Akopian~A.N., Sivilotti~L., Wood~J.N. (1996). A tetrodotoxin-resistant voltage-gated sodium channel expressed by sensory neurons. \emph{Nature} 379:257--262. ($\mathrm{Na_V}1.8$/SCN10A)
\item Dib-Hajj~S.D., Waxman~S.G., et al. $\mathrm{Na_V}1.7$ (SCN9A) and inherited pain phenotypes (congenital insensitivity / erythromelalgia).
\item Binshtok~A.M., Bean~B.P., Woolf~C.J. (2007). Inhibition of nociceptors by targeting capsaicin-receptor--permeating QX-314. \emph{Nature} 449:607--610.
\item Brown~D.A., Passmore~G.M. M-current ($\mathrm{K_V}7$/KCNQ) and neuronal excitability.
\item Suzetrigine (VX-548), a selective $\mathrm{Na_V}1.8$ inhibitor; U.S.\ FDA approval, 2025 (closed-state mechanism). Cited as a target-validation anchor only.
\item Lee~Y.J. The Vacuum as a Jammed Elastic Solid (VP theory; the jamming-lattice framework underlying the Layer-1 $\gamma$ read). DOI \href{https://doi.org/10.5281/zenodo.17932566}{10.5281/zenodo.17932566}.
\end{enumerate}
\end{footnotesize}

\appendix
\section{Reproducibility package layout}
\begin{footnotesize}\begin{verbatim}
""" + file_tree() + r"""
\end{verbatim}\end{footnotesize}

\end{document}
"""

def count_manifest():
    p = f"{PKG}/manifest/SHA256SUMS.txt"
    return 94  # final manifested count incl. paper/ (set explicitly to avoid circular self-reference)

def file_tree():
    return """analgesic_threshold_logic_v2_0/
  README.md  CONSTITUTION.md  VP_SPEC_v1_8.md  IRREPRODUCIBILITY_LEDGER.md
  CHANGELOG_v2_0_multipage.md   build_multipage_analgesic.py
  paper/   analgesic_threshold_logic_v2_0.tex  .pdf  build_paper_tex.py
  docs/
    analgesic/index.html              hub (answer-first + contents + cross-links)
    analgesic/<slug>/index.html       40 self-contained pages: how-to-read,
                                      5 levers, 27 per-target, 7 sections
    assets/css/site.css  robots.txt  sitemap.xml  llms.txt  analgesic/_meta.json
  repro/
    _engine/                          locked engines (dna_interpreter, vp_neuro_engine)
    _inherited_data/                  inherited gamma + cached promoter sequences
    01-inherit-reverify/   02-read-nav-channels/   03-threshold-map/
    04-channelopathy-anchor/  05-intervention-logic/ (forbidden_claim_scan.py)
    06-falsification/  10-burden-prioritisation/  11-l3-honesty/
    12-precision-local-anaesthesia/
    run_all.py            expected_sha256.json   (10 frozen hashes)
  manifest/SHA256SUMS.txt             every shipped file hashed
  reports/                            gate snapshots
"""

if __name__ == "__main__":
    out = f"{PKG}/paper/analgesic_threshold_logic_v2_0.tex"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(document())
    print("wrote", out, "(", os.path.getsize(out), "bytes )")
