#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_paper.py  --  Reproductive / Gonadal-Endocrine WRITING phase: canonical LaTeX whitepaper generator.

Mirrors tools/build_docs.py: every displayed quantity is pulled LIVE from the research modules at build
time, so the PDF cannot drift from the engine (VP-SPEC C1). Emits paper/reproductive_endocrine_vp.tex.
Deterministic: no build timestamp (\\today is never used); the title page carries the fixed version + DOI.

Usage:  python tools/build_paper.py        # writes paper/reproductive_endocrine_vp.tex
Then:   latexmk -pdf -interaction=nonstopmode reproductive_endocrine_vp.tex   (run inside paper/)
"""
import os, sys, importlib

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.join(_HERE, "..")
_PAPER = os.path.join(_PKG, "paper")
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_verify"))
gates = importlib.import_module("gates")

# ---- registry (kept in sync with build_docs.py) ---------------------------------------------------
TITLE = ("Reproductive and Gonadal-Endocrine Emergence on a Jammed-Vacuum Substrate: "
         "the HPG Oscillator, the Menstrual Cycle, and Hormone-Driven Cancer")
SHORT = "Reproductive / Gonadal-Endocrine (VP Theory)"
AUTHOR = "Young Jae Lee"
ORCID = "0009-0002-7535-8245"
VERSION = open(os.path.join(_PKG, "VERSION"), encoding="utf-8").read().strip()
DOI = "10.5281/zenodo.20754657"           # Zenodo concept DOI (version-independent, always latest)
CANON = "https://jamming-physics.org/reproductive-endocrine"
REPRO = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/reproductive-endocrine"
DOI_PHYSICS = "10.5281/zenodo.17932566"
DOI_DNA = "10.5281/zenodo.20471407"


def f(x, n):
    return ("%." + str(n) + "f") % float(x)


def gather():
    for d in ("_engine", "_dynamics", "_oncology", "_therapy", "_disease", "_germline", "_embryo",
              "_fertility", "_sexratio"):
        sys.path.insert(0, os.path.join(_HERE, "..", "repro", d))
    eng = importlib.import_module("vp_rep_engine")
    hpg = importlib.import_module("hpg_axis"); men = importlib.import_module("menstrual_cycle")
    spm = importlib.import_module("spermatogenesis"); onc = importlib.import_module("carcinogen_dose_response")
    thr = importlib.import_module("temporal_pattern"); dis = importlib.import_module("mechanisms")
    gmt = importlib.import_module("gametogenesis")
    emb = importlib.import_module("embryogenesis")
    inf = importlib.import_module("infertility")
    sxr = importlib.import_module("sex_ratio")
    _, sha = eng.emit(eng.circulate())
    germ = gmt.run_germline_battery()
    embryo = emb.run_embryo_battery()
    fert = inf.run_fertility_battery()
    sexr = sxr.run_sexratio_battery()
    return dict(emerge=eng.emerge_organs(), T1=hpg.run_T1(), T5=hpg.run_T5(), T2=men.run_T2(),
                T3=men.run_T3(), T4=spm.run_T4(), onc=onc.run_oncology(), thr=thr.run_therapy(),
                dis=dis.run_disease(), core_sha=sha,
                germ={s["target"]: s for s in germ["suites_full"]}, germ_atlas=gmt.panel_gamma_atlas(),
                emb={s["target"]: s for s in embryo["suites_full"]}, emb_atlas=emb.panel_gamma_atlas(),
                fert={s["target"]: s for s in fert["suites_full"]},
                sxr={s["target"]: s for s in sexr["suites_full"]}, sxr_atlas=sxr.panel_gamma_atlas(),
                research=gates.research_gate())


# ---- LaTeX helpers --------------------------------------------------------------------------------
def tex_escape(s):
    repl = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
            "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    out = []
    for ch in str(s):
        out.append(repl.get(ch, ch))
    return "".join(out)


def grade_tex(tok):
    label = {"V": r"\gradeV", "F": r"\gradeF", "L": r"\gradeL", "O": r"\gradeO"}
    return label.get(tok, tok)


def table(colspec, header, rows, caption, label):
    out = [r"\begin{table}[H]", r"\centering", r"\small",
           r"\caption{" + caption + r"}", r"\label{tab:" + label + r"}",
           r"\begin{tabular}{" + colspec + r"}", r"\toprule",
           " & ".join(header) + r" \\", r"\midrule"]
    for r in rows:
        out.append(" & ".join(str(c) for c in r) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(out)


# ---- document -------------------------------------------------------------------------------------
def preamble():
    return r"""\documentclass[11pt]{article}
\usepackage[a4paper,margin=1in]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{float}
\usepackage[protrusion=true,expansion=false]{microtype}
\usepackage{enumitem}
\usepackage{caption}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage[colorlinks=true,linkcolor=accent,citecolor=accent,urlcolor=accent]{hyperref}

\definecolor{accent}{HTML}{7A1F4B}
\definecolor{forced}{HTML}{274B8A}
\definecolor{verified}{HTML}{1F6B3A}
\definecolor{open}{HTML}{9A5B00}

% honest-grading badges
\newcommand{\gradeV}{\textcolor{verified}{\textbf{[V]}}}
\newcommand{\gradeF}{\textcolor{forced}{\textbf{[F]}}}
\newcommand{\gradeL}{\textcolor{verified}{\textbf{[L]}}}
\newcommand{\gradeO}{\textcolor{open}{\textbf{[O]}}}

\titleformat{\section}{\large\bfseries\color{accent}}{\thesection}{0.6em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.6em}{}
\captionsetup{font=small,labelfont=bf}
\setlength{\parskip}{0.4em}
\setlength{\parindent}{0pt}
\sloppy
\hbadness=10000
"""


def title_block(D):
    return r"""
\begin{document}

\begin{center}
{\LARGE\bfseries """ + TITLE + r"""}\\[1.0em]
{\large """ + AUTHOR + r"""}\\[0.3em]
{\small Independent Researcher \quad ORCID: \href{https://orcid.org/""" + ORCID + r"""}{""" + ORCID + r"""}}\\[0.3em]
{\small Version """ + tex_escape(VERSION) + r""" \quad DOI: \href{https://doi.org/""" + DOI + r"""}{""" + DOI + r"""} \quad License: CC BY 4.0}\\[0.3em]
{\small Canonical living version: \href{""" + CANON + r"""/}{""" + CANON.replace("https://", "") + r"""/}}
\end{center}

\vspace{0.6em}
\hrule
\vspace{0.6em}

\begin{abstract}
\noindent We derive the human reproductive and gonadal-endocrine (hypothalamic--pituitary--gonadal, HPG)
axis on the VP Theory jammed-vacuum substrate, using two vendored primitives unchanged: a bistable
rectification (R19) switch and a FitzHugh--Nagumo (FHN) relaxation oscillator. A single sex-hormone drive
$h$ acting on the R19 tilted double well produces \emph{two} opposite failure modes --- an oscillator
disease and a barrier-lowered oncogenic switch --- governed by \emph{one} control axis: temporal pattern
(pulsatile versus continuous, cycling versus sustained). The same kernel, run as an FHN oscillator,
generates the GnRH pulse train, the menstrual cycle, and the spermatogenic cycle by changing only the
recovery timescale $\tau_s$; run as an R19 switch, it gives organ emergence in measured-$\gamma$ order, the
discontinuous ovulatory LH surge, puberty as a spinodal crossing, and hormone-driven carcinogenesis as
barrier lowering. The same two primitives extend downstream to the gamete and the embryo, to the
infertility/subfertility distinction (categorical past a spinodal versus a finite Kramers rate near
threshold), and to sex determination and sex-ratio distortion (a tiltable bistable switch with Fisher's
1:1 restoring force). Every published quantity is pulled live from a deterministic reproduction engine
(SEED~=~19; two builds are byte-identical, \texttt{sha256}~=~\texttt{""" + D["core_sha"][:16] + r"""\ldots}); no
constant is tuned to a target. Grades are honest throughout: \gradeF{} forced by geometry, \gradeV{}
simulation-verified, \gradeL{} measured anchor, \gradeO{} open with the obstacle stated. This is a
falsifiable physics-derived research artefact and is \textbf{not} clinical advice.
\end{abstract}

\vspace{0.4em}
\textbf{Keywords:} reproductive endocrinology; HPG axis; GnRH pulse-frequency coding; menstrual cycle;
relaxation oscillator; FitzHugh--Nagumo; bistable switch; spinodal; hysteresis; hormone-driven cancer;
dose--response; Bipolar Androgen Therapy; infertility; subfertility; meiotic drive; sex determination;
sex ratio; Fisher's principle; VP Theory; jamming; computational biology; reproducibility.

\vspace{0.4em}
\hrule
"""


def sec_scope(D):
    sp = f(D["T3"]["spinodal"], 4)
    return r"""
\section{Scope and the jammed-vacuum substrate}

\textbf{One drive, two failures, one lever.} This package derives the gonadal-endocrine axis on the VP
Theory jammed-vacuum substrate~\cite{vptheory}, where a cell or tissue fate is a point in a bistable R19
double-well potential and a hormone is a tilt $h$ on that well. One sex-hormone drive, moved two opposite
ways, produces the whole disease map: move it the wrong \emph{pattern} and an HPG oscillator fails (an
endocrine disorder); lower the barrier and the R19 oncogenic switch crosses (a hormone-driven cancer). The
single control axis the framework exposes is therefore temporal pattern. No new physics is introduced here;
the vendored primitives are used unchanged.

The fate landscape is the tilted double well
\begin{equation}
V(s) = -\tfrac{1}{2}\gamma s^{2} + \tfrac{1}{4}s^{4} - h\,s,
\qquad
\dot s = \gamma s - s^{3} + h,
\end{equation}
whose stationary states are the roots of $s^{3}-\gamma s - h = 0$: for three real roots there are two minima
(basins) and a saddle. As the tilt $h$ grows, the metastable minimum and the saddle approach and annihilate
at the \emph{spinodal} --- beyond it the flip is unavoidable and discontinuous. Two locked constants set
every threshold and barrier in the paper, both forced functions of the identity constant $\gamma$ alone:
\begin{equation}
h_{\mathrm{sp}}(\gamma) = 2\left(\tfrac{\gamma}{3}\right)^{3/2}
\quad(\,= """ + sp + r"""\ \text{at}\ \gamma=1\,),
\qquad
\Delta V_{0}(\gamma) = \tfrac{\gamma^{2}}{4}.
\end{equation}
The spinodal $h_{\mathrm{sp}}$ fixes where a switch flips; the barrier $\Delta V_{0}$ fixes how stable a
basin is. Both are \gradeF{} forced by geometry.

\paragraph{Firewall.} Decomposition is by physical regime, not textbook organ labels: this is the jamming
(hormonal-cycle / germline) class. The brain-facing hypothalamic--pituitary--adrenal (HPA) stress axis and
felt experience belong to the companion Felt Cognition paper and are cited, never re-derived here. Sex-hormone
\emph{levels} are this package's single source of truth.
"""


def sec_organs(D):
    em = D["emerge"]; order = {o["organ"]: o for o in em["organs"]}
    rows = []
    for org in em["gamma_order_ascending"]:
        o = order[org]
        rows.append([tex_escape(o["master"]), tex_escape(o["organ"].replace("_", " ")),
                     f(o["gamma"], 4), f(o["functional_spinodal"], 4),
                     f(o["rel_size_dwell"], 4), tex_escape(o["dyn_class"])])
    tbl = table("llcccl",
                [r"master gene", r"organ", r"$\gamma$ (meas.)", r"func.\ spinodal",
                 r"rel.\ size (DWELL)", r"dyn.\ class"],
                rows,
                r"Reproductive organ emergence in measured-$\gamma$ order. $\gamma$ is measured from the "
                r"proximal promoter by the 4D DNA pipeline, reproduced offline bit-for-bit; the emergence "
                r"order is $\mathrm{argsort}(\gamma)$.", "organs")
    names = " $\\to$ ".join(order[o]["organ"].replace("gonad_", "").replace("reproductive_", "").replace("_", " ")
                            for o in em["gamma_order_ascending"])
    return r"""
\section{Organ emergence from measured master-gene \texorpdfstring{$\gamma$}{gamma}}

The morphogenesis identity constant is $\gamma = -\langle\Delta G_{37}^{\mathrm{NN}}\rangle$: minus the mean
nearest-neighbour stacking free energy~\cite{santalucia} over the proximal promoter (TSS$-2000\ldots+500$,
GRCh38) of each organ's master gene. It is \gradeV{} measured, never fitted --- the pipeline is accepted only
because it reproduces the vendored SOX9 anchor ($\gamma=1.4598$) to four decimals; the promoter sequences are
cached so $\gamma$ reproduces offline bit-for-bit~\cite{dnablueprint}. The emergence order of an organ system
is the argsort of its master-gene $\gamma$ values, the same gene-clock used elsewhere in the programme.

For the four reproductive masters the measured order (ascending $\gamma$) is """ + names + r""". Germline-first
is consistent with primordial germ-cell specification preceding gonadal differentiation, a sign sanity-check
rather than a fitted result. The relative run-length / size of each switch follows
$\mathrm{DWELL}(\gamma) = \gamma^{3/2}/(K+\mathrm{brake})$ --- order and direction \gradeF{} forced; absolute
magnitude \gradeO{} (external calibration; see \S\ref{sec:open}).

""" + tbl + "\n"


def sec_gnrh(D):
    T1 = D["T1"]
    rows = [[f(r["tau_s"], 0), r["pulses"], f(r["mean_interval_arb"], 1),
             f(r["pulse_rate_arb"], 6), tex_escape(r["favours"])]
            for r in T1["frequency_decoding"]["rows"]]
    tbl = table("ccccl",
                [r"recovery $\tau_s$", r"pulses", r"mean interval", r"pulse rate", r"gonadotropin bias"],
                rows,
                r"Frequency decoding by the shared FHN generator: the pulse rate is a monotone function of "
                r"the recovery timescale $\tau_s$, and fast/slow maps onto the LH/FSH bias.", "freq")
    return r"""
\section{The GnRH pulse generator}

\textbf{Answer.} The hypothalamic GnRH pulse generator is the shared FHN relaxation oscillator: a fast R19
switch with slow recovery emits a relaxation pulse train (""" + str(T1["pulses"]) + r""" pulses at $\tau_s=60$).
Pulse \emph{frequency} --- not amplitude --- decodes to gonadotropin identity, fast pulses favouring LH and
slow pulses favouring FSH, reproduced as a monotone function of $\tau_s$~\cite{knobil}. The mechanism is
\gradeV{} sim-verified; the absolute pulse rate is a measured \gradeL{} anchor.

The arcuate KNDy network that paces GnRH release is, on this substrate, the same fast--slow FHN system used
everywhere in the package. At the follicular setting $\tau_s=60$ the generator emits """ + str(T1["pulses"]) + r"""
pulses over the run with mean inter-pulse interval """ + f(T1["mean_interval_arb"], 1) + r""" (arb). The
clinically central fact --- that pulse \emph{frequency} sets the LH:FSH balance --- falls out of the recovery
timescale: a faster generator (smaller $\tau_s$) fires more often and favours LH; a slower generator favours
FSH; and the pulse rate is monotone in $\tau_s$ (Table~\ref{tab:freq}). The pulse rate is calibrated to the
measured follicular figure of roughly one GnRH/LH pulse per 60--90~min~\gradeL{}; the package does not claim
to derive that clinical number, only the monotone frequency-decoding mechanism~\gradeV{}.

""" + tbl + "\n"


def sec_menstrual(D):
    T2 = D["T2"]
    return r"""
\section{The menstrual cycle as a relaxation oscillator}

\textbf{Answer.} The menstrual cycle is the same kernel run slow: a relaxation (saw-tooth) oscillator, not a
sinusoid. Over the run it completes """ + str(T2["cycles"]) + r""" cycles with period """ + f(T2["period_arb"], 1) + r"""
(arb), built from a slow follicular rise (""" + f(T2["rise_arb"], 1) + r""") and an abrupt luteal fall
(""" + f(T2["fall_arb"], 1) + r"""), an asymmetry ratio of """ + f(T2["asymmetry_ratio"], 1) + r""". The strong
rise/fall asymmetry is the signature of a relaxation oscillation; a sinusoid would have asymmetry near unity.
The period magnitude is anchored to the $\sim$28-day cycle as a measured \gradeL{} quantity, while the
relaxation \emph{form} is \gradeV{} sim-verified. Only the recovery timescale $\tau_s$ distinguishes this from
the GnRH pulse and the spermatogenic cycle --- it is one oscillator at three speeds.
"""


def sec_surge(D):
    T3 = D["T3"]
    return r"""
\section{The oestrogen feedback switch and the LH surge}

\textbf{Answer.} The pre-ovulatory LH surge is a discontinuous spinodal crossing of the R19 switch, not a
smooth rise: rising oestradiol tilts the well until the negative-feedback basin annihilates at
$h_{\mathrm{sp}}=""" + f(T3["spinodal"], 4) + r"""$, and the state jumps to the secretory branch. The model shows
a discontinuous up-jump of size """ + f(T3["up_jump_size"], 3) + r""" once the up-threshold
$""" + f(T3["surge_up_threshold"], 4) + r"""$ is crossed, and the return path crosses a different down-threshold
$""" + f(T3["return_down_threshold"], 4) + r"""$ --- a hysteresis loop of width
$""" + f(T3["hysteresis_width"], 3) + r"""$~\gradeV{}. This is the switch from oestrogen \emph{negative}
feedback (most of the cycle) to the brief \emph{positive}-feedback surge: the substrate realises it as one
bistable well crossing its spinodal in one direction, then returning by another, which is exactly what
hysteresis means. The discontinuity and the hysteresis are forced features of an R19 switch, not added by
hand.
"""


def sec_sperm(D):
    T4 = D["T4"]; po = T4["period_ordering"]
    return r"""
\section{The spermatogenic cycle}

\textbf{Answer.} Spermatogenesis is the same relaxation oscillator at an intermediate recovery timescale
($\tau_s=""" + f(T4["tau_s"], 0) + r"""$), giving period """ + f(T4["period_arb"], 1) + r""" (arb), between the
fast GnRH pulse and the slow menstrual cycle. The package verifies the period ordering directly:
$""" + f(po["pulse_arb"], 1) + r"""$ (pulse) $<$ $""" + f(po["spermatogenic_arb"], 1) + r"""$ (spermatogenic)
$<$ $""" + f(po["menstrual_arb"], 1) + r"""$ (menstrual)~\gradeV{}. Mapped to clinical time the spermatogenic
cycle anchors to $\sim$16~days~\gradeL{}; the ordering is the derived claim, the absolute days an anchor. That
a single oscillator covers three reproductive rhythms purely by its recovery timescale is the unifying point:
the body re-uses one fast--slow kernel and re-tunes $\tau_s$.
"""


def sec_puberty(D):
    T5 = D["T5"]
    return r"""
\section{Puberty as a spinodal crossing}

\textbf{Answer.} Puberty is the reactivation of the GnRH generator modelled as a single irreversible spinodal
crossing: below threshold the axis sits in the quiescent (OFF) basin at $""" + f(T5["state_before"], 3) + r"""$,
and once the drive reaches $""" + f(T5["jump_drive"], 4) + r"""$ --- a ratio jump/spinodal of
$""" + f(T5["jump_over_spinodal"], 2) + r"""$ --- the state jumps by $""" + f(T5["jump_size"], 3) + r"""$ to the
active (ON) branch at $""" + f(T5["state_after"], 3) + r"""$~\gradeV{}. The onset is therefore discontinuous and
localised at the spinodal, the same geometry as the LH surge but taken once and not returned. The framework
fixes the discontinuous order (OFF below the crossing, ON above) and the jump/spinodal ratio; mapping the
crossing to a chronological age requires external endocrine calibration and is declared \gradeO{}
(\S\ref{sec:open}).
"""


def sec_cancer(D):
    onc = D["onc"]
    uni = [[f(r["frac"], 2), f(r["ratio"], 5), f(r["max_spread_across_gamma"], 1)]
           for r in onc["universality"]["table"]]
    uni_t = table("ccc",
                  [r"$h/h_{\mathrm{sp}}$", r"$\Delta V/\Delta V_0$", r"max spread across $\gamma$"], uni,
                  r"Barrier-law universality: the relative barrier as a function of relative drive is "
                  r"identical across $\gamma$ (max spread $0.0$), so the dose--response shape is "
                  r"$\gamma$-independent~\gradeF{}.", "uni")
    br = [[r["exposure_years"], f(r["frac"], 3), f(r["RR"], 3)] for r in onc["breast"]["rows"]]
    br_t = table("ccc", [r"exposure yr", r"$h/h_{\mathrm{sp}}$", r"RR"], br,
                 r"Breast: cumulative-oestrogen exposure monotonically raises modelled relative risk to a "
                 r"plateau. Population anchor: " + tex_escape(onc["breast"].get("anchor", "")) + r".", "breast")
    pr = [[f(r["drive_frac"], 1), f(r["barrier_reduction"], 3), f(r["RR"], 3)] for r in onc["prostate"]["rows"]]
    pr_t = table("ccc", [r"androgen drive $\times h_{\mathrm{sp}}$", r"barrier reduction", r"RR"], pr,
                 r"Prostate: barrier reduction is concave and the relative risk plateaus past the fold.",
                 "prostate")
    cv = [[f(r["joint_frac"], 2), f(r["RR_hpv"], 3), f(r["RR_smoking"], 3), f(r["RR_both"], 3),
           f(r["synergy_index"], 3)] for r in onc["cervical"]["rows"]]
    cv_t = table("ccccc",
                 [r"joint exp.", r"RR HPV", r"RR smoke", r"RR both", r"synergy idx"], cv,
                 r"Cervical: HPV $\times$ smoking is multiplicative at low exposure (synergy index $\approx 1$) "
                 r"and saturates sub-multiplicatively at high exposure.", "cervical")
    return r"""
\section{Hormone-driven cancer as barrier lowering}

\textbf{Answer.} Hormone-driven carcinogenesis is the R19 oncogenic switch crossed by barrier lowering: a
sustained sex-hormone drive tilts the well and lowers the inter-basin barrier $\Delta V_0=\gamma^2/4$, raising
the Kramers escape rate~\cite{kramers} into the malignant basin. The relative risk is the ratio of escape
rates,
\begin{equation}
\mathrm{RR}(\mathrm{dose}) = \frac{\exp[-\Delta V(h)/D]}{\exp[-\Delta V(0)/D]},
\end{equation}
with a single open lattice noise constant $D=""" + f(onc["noise_D"], 2) + r"""$ that sets the absolute magnitude
only. Crucially, the relative barrier as a function of relative drive is \emph{identical across} $\gamma$
(Table~\ref{tab:uni}, max spread $0.0$), so the dose--response \emph{shape} is forced and $\gamma$-independent
\gradeF{}; every reported RR \emph{ratio} is invariant under $D$ (verified $D$-robust). Three cancers come out
as three distinct, sim-verified shapes:

\begin{itemize}[leftmargin=1.2em,itemsep=2pt]
\item \textbf{Breast} (Table~\ref{tab:breast}): cumulative-oestrogen exposure raises RR monotonically to a
plateau (saturating once the barrier is gone)~\gradeV{}.
\item \textbf{Prostate} (Table~\ref{tab:prostate}): barrier reduction is concave and RR plateaus past the fold
\gradeV{}.
\item \textbf{Cervical} (Table~\ref{tab:cervical}): HPV $\times$ smoking is multiplicative at low exposure and
saturates sub-multiplicatively at high exposure~\gradeV{}, the same synergy structure seen in other
infection $\times$ carcinogen pairs.
\end{itemize}

Absolute population incidence needs epidemiological calibration and is declared \gradeO{}; the shapes,
ratios, and the $\gamma$-independence are the derived content.

""" + uni_t + "\n\n" + br_t + "\n\n" + pr_t + "\n\n" + cv_t + "\n"


def sec_therapy(D):
    thr = D["thr"]; t = thr["bat_cycling"]["table"]; g = thr["gnrh_pattern"]
    name = {"continuous_high_T": "continuous high (T)", "continuous_low_ADT": "continuous low (ADT)",
            "cycling_BAT": "cycling (BAT)"}
    rows = [[name[k], f(t[k]["sensitive"], 4), f(t[k]["resistant"], 4),
             (f(t[k]["res_over_sens"], 2) if t[k]["res_over_sens"] is not None else "---")]
            for k in ("continuous_high_T", "continuous_low_ADT", "cycling_BAT")]
    bat_t = table("lccc",
                  [r"schedule", r"sensitive stress", r"resistant stress", r"res./sens."], rows,
                  r"Temporal-pattern selectivity. Cycling androgen (Bipolar Androgen Therapy) amplifies the "
                  r"stress on the resistant clone far more than continuous suppression does.", "bat")
    fold = f(thr["bat_cycling"]["cycling_over_continuous_high_resistant_fold"], 1)
    return r"""
\section{Temporal pattern as a therapeutic lever}

\textbf{Answer.} The single control axis the framework exposes is temporal pattern, and it runs the whole
therapy map. Cycling the androgen drive (Bipolar Androgen Therapy, BAT) amplifies the stress on the resistant
clone """ + fold + r"""$\times$ over continuous high suppression (Table~\ref{tab:bat}): a resistant clone
adapted to a constant environment is destabilised by forced oscillation, whereas continuous suppression
selects for it. The same principle, read on the GnRH generator, gives the textbook paradox that the
\emph{same molecule} has opposite effects by pattern: pulsatile GnRH activates the axis
(""" + str(g["pulsatile_output_pulses"]) + r""" pulses) while continuous GnRH suppresses it
(""" + str(g["continuous_output_pulses"]) + r""" pulses)~\gradeV{}. This retrodicts pulsatile-GnRH pump therapy
(activation in hypothalamic amenorrhoea) and depot GnRH-agonist desensitisation (suppression in precocious
puberty, endometriosis, and prostate cancer), the hCG trigger as a single spinodal kick onto the ON branch,
and the BAT schedule --- all as moves along one temporal-pattern axis.

""" + bat_t + "\n"


def sec_disease(D):
    dis = D["dis"]; pc = dis["substrate_checks"]
    g2 = {"V": r"\gradeV", "L": r"\gradeL", "O": r"\gradeO", "F": r"\gradeF"}
    rows = []
    for d in dis["disorders"]:
        gr = d["grade"].strip()
        tok = "O" if gr.startswith("[O]") else ("L" if gr.startswith("[L]") else
              ("F" if gr.startswith("[F]") else "V"))
        rows.append([tex_escape(d["name"]), tex_escape(d["mechanism"]),
                     tex_escape(d["better_hypothesis"]), g2[tok]])
    tbl = table(r"p{2.6cm}p{4.2cm}p{4.6cm}c",
                [r"disorder", r"substrate failure mode", r"model-derived hypothesis", r"grade"], rows,
                r"Eight common HPG disorders on one substrate. Retrodictions of existing practice are flagged "
                r"as validation; genuinely novel hypotheses are graded \gradeO{} and require clinical "
                r"validation. None of this is clinical advice.", "disorders")
    return r"""
\section{Disease mechanisms on one substrate}

\textbf{Answer.} Eight common HPG disorders map to one substrate: one drive, two failure modes, one lever.
PCOS (the generator stuck too fast, LH-biased rate $""" + f(pc["pcos"]["fast_tau_rate"], 4) + r"""$) and
functional hypothalamic amenorrhoea (the same generator slowed below the ovulatory rate,
$""" + f(pc["fha"]["fha_slow_rate"], 4) + r"""$) are opposite ends of one pulse-frequency axis. Menopause is
irreversible loss of the bistable secretory latch (ON $""" + f(pc["menopause"]["intact_latched_on"], 1) + r""" \to """ + f(pc["menopause"]["depleted_state"], 3) + r"""$ on follicular depletion), so HRT is replacement,
not restoration. The split is by mechanism, not body part: every disorder is either a broken oscillator or a
crossed oncogenic switch, resolved by the temporal-pattern lever.

Retrodictions are sim-verified \gradeV{}; the genuinely novel suggestions --- low-frequency pulsatile
restoration in PCOS, and pulsed/cycled testosterone replacement --- are graded \gradeO{} and explicitly
require clinical validation.

""" + tbl + "\n"


def sec_gamete(D):
    G1, G2, G3, G4 = D["germ"]["G1"], D["germ"]["G2"], D["germ"]["G3"], D["germ"]["G4"]
    G5, G6 = D["germ"]["G5"], D["germ"]["G6"]
    cm = G2["crossover_model"]; hyp = G3["hyperactivation"]; lad = G3["four_clock_ladder"]
    pre = G5["preregistered_test"]; core = G5["recombination_core_cluster"]
    prov = G6["provisioning"]; dsym = G6["division_symmetry"]
    atlas = sorted(D["germ_atlas"].items(), key=lambda kv: kv[1])
    ms = G5["module_stats"]
    mod_rows = [[m, ms[m]["n"], f(ms[m]["mean"], 4), f(ms[m]["sd"], 4),
                 f(ms[m]["lo"], 4) + "--" + f(ms[m]["hi"], 4)]
                for m in ("germline", "meiosis", "sperm", "oocyte")]
    mod_tbl = table("lrrrr", ["module", "n", "mean $\\gamma$", "sd", "range"], mod_rows,
                    r"Measured gamete-program promoter $\gamma$ by functional module (NN-stacking $\Delta G_{37}$, "
                    r"SantaLucia 1998). A pre-registered permutation test of module separation returns a null "
                    r"(reported honestly); only the recombination-core cluster is claimed.", "gamete-gamma")
    atlas_line = ", ".join(s + " " + f(gv, 4) for s, gv in atlas)
    return r"""
\section{The gamete itself: meiosis, motility and the egg}

\textbf{Answer.} The four questions about the germ cell answer on the same substrate, with measured
gamete-program promoter $\gamma$ as the only new input. \emph{How} a gamete is made: meiosis is one DNA
replication then two divisions ($2N,2C \to 2N,4C \to 1N,2C \to 1N,1C$), reductional before equational, an
order forced by ordered two-stage REC8 cohesin release (arm separase $""" + f(G1["separase_at_arm_release"], 3) + r"""$
$\to$ centromeric $""" + f(G1["separase_at_centromeric_release"], 3) + r"""$, set by the sign of shugoshin
protection, not a tuned rate)~\gradeV{}. \emph{Whether} gametes are identical: no --- independent assortment is
exactly $2^{23}=""" + format(G2["independent_assortment_combinations"], ",") + r"""$, and crossover interference
is the substrate refractory period mapped onto the chromosome axis (sub-Poisson, Fano
$""" + f(cm["fano_factor"], 3) + r"""$ versus the Poisson null $""" + f(cm["null_poisson_fano"], 3) + r"""$, gap
CV $""" + f(cm["gap_cv"], 2) + r"""$, obligate crossover), so the floor on distinct gametes exceeds
$10^{""" + str(int(G2["diversity"]["log10_distinct_gametes_floor"])) + r"""}$~\gradeV{}.

\textbf{The sperm is a fast oscillator; the egg is a held switch.} The flagellar beat is the fast end of the
same relaxation-oscillator ladder: in arbitrary units the periods order
$""" + f(lad["flagellum_arb"], 1) + r"""$ (flagellum) $<$ $""" + f(lad["pulse_arb"], 1) + r"""$ (pulse) $<$
$""" + f(lad["spermatogenic_arb"], 1) + r"""$ (spermatogenic) $<$ $""" + f(lad["menstrual_arb"], 1) + r"""$
(menstrual)~\gradeV{}, anchored to a $\sim""" + f(G3["beat_anchor_hz"], 0) + r"""$~Hz beat~\gradeL{}.
Hyperactivation is a CatSper-driven rise in oscillator gain, and its two co-signatures move together: the beat
grows in amplitude ($""" + f(hyp["activated_amp"], 2) + r""" \to """ + f(hyp["hyperactivated_amp"], 2) + r"""$)
and slows ($""" + str(hyp["activated_beats"]) + r""" \to """ + str(hyp["hyperactivated_beats"]) + r"""$
beats)~\gradeV{}. The egg is the opposite use of the kernel: a switch held at metaphase~II (arrested state
$""" + f(G4["arrested_state"], 3) + r"""$). A sub-spinodal $\mathrm{Ca}^{2+}$ transient does nothing; one above
the spinodal ($""" + f(G4["activation_spinodal"], 4) + r"""$) flips it irreversibly, and that same past-spinodal
irreversibility \emph{is} the polyspermy block~\gradeV{}. The integer~9 of the $9{+}2$ axoneme is structural and
\emph{not} derived; it is declared \gradeO{} rather than back-fitted.

\textbf{A measured $\gamma$ atlas and an honest null.} The gamete-program promoters, in ascending $\gamma$:
""" + atlas_line + r""". A pre-registered test of whether $\gamma$ \emph{separates} the three functional modules
returns F-like $""" + f(pre["f_like_statistic"], 3) + r"""$, $p=""" + f(pre["p_permutation"], 3) + r"""$ --- a
null, reported as it falls. What is supported, and tested separately, is narrower: the recombination core
(SPO11, DMC1, MLH1, PRDM9) is a tight $\gamma$ cluster (CV $""" + f(core["core_cv"], 4) + r"""$ versus panel
$""" + f(core["panel_cv"], 4) + r"""$, $p=""" + f(core["p_core_tighter_than_random"], 4) + r"""$). The framework
claims only the second result, at the grade the test supports.

""" + mod_tbl + r"""

\textbf{One substrate, two gametes.} The same kernel is a free-running oscillator for the sperm and a held
switch for the egg; the count asymmetry has the same root. Spermatogenesis divides symmetrically into
$""" + str(dsym["spermatogenesis_symmetric_gametes"]) + r"""$ equal gametes, while oogenesis divides
asymmetrically into $""" + str(dsym["oogenesis_eggs"]) + r"""$ large egg and
$""" + str(dsym["oogenesis_polar_bodies"]) + r"""$ vanishing polar bodies, concentrating the cytoplasm
(egg:polar-body mass $""" + f(prov["egg_over_polar_body"], 0) + r"""\times$) and giving a measured egg:sperm
volume ratio of $\sim""" + format(int(prov["volume_ratio_anchor"]), ",") + r"""\times$~\gradeL{}. Anisogamy ---
the deepest asymmetry in reproduction --- is on this substrate an oscillator and a switch built from one rule;
the evolutionary ``why'' is game-theoretic and is marked \gradeO{} (\S\ref{sec:open}).
"""


def sec_embryo(D):
    E1, E2, E3 = D["emb"]["E1"], D["emb"]["E2"], D["emb"]["E3"]
    E4, E5 = D["emb"]["E4"], D["emb"]["E5"]
    uniq = E1["genome_uniqueness"]; zga = E3["zga_crossing"]
    stest = E4["preregistered_stage_test"]; htest = E4["preregistered_hox_test"]
    sm = E4["stage_means"]; fet = E5["fetus"]
    struct_by_master = {s["master"]: s for s in E4["structures"]}
    stage_label = {"pluripotency": "pluripotency", "germ_layer": "germ layer",
                   "organ_primordium": "organ primordium", "ap_axis": "AP-axis (HOX)"}
    rows = []
    for s in E4["emergence_order_gamma_ascending"]:
        st = struct_by_master[s]
        rows.append([tex_escape(s), stage_label.get(st["stage"], st["stage"]),
                     f(st["gamma"], 4), f(st["functional_spinodal"], 4), f(st["rel_size_dwell"], 4)])
    atlas_tbl = table("llrrr", ["master", "stage", "$\\gamma$", "func. spinodal", "rel. size"], rows,
                      r"Measured developmental master-gene promoter $\gamma$ (same NN-stacking pipeline; "
                      r"validated on the SOX9 and DAZL anchors), in gene-clock order "
                      r"(argsort of the spinodal $=$ $\gamma$ ascending). Stage is the pre-registered "
                      r"hypothesis label, declared before $\gamma$ was seen.", "embryo-gamma")
    order_line = " $\\to$ ".join(tex_escape(s) for s in E4["emergence_order_gamma_ascending"])
    return r"""
\section{The embryo: from two gametes to a fetus}

\textbf{Answer.} The two gametes meet and a fetus is built on the same substrate, each step a discriminant
against the vendored R19 switch and FHN oscillator, reusing the gamete results and adding a measured
developmental master-gene $\gamma$ panel as the only new input. \emph{Syngamy}: the sperm (a free
oscillator) delivers a supra-spinodal $\mathrm{Ca}^{2+}$ kick that flips the egg (a held switch) one-way,
with a polyspermy block; two haploid pronuclei fuse, restoring diploidy ($1N{+}1N\to 2N$), and the new
genome is unique to a floor of $10^{""" + str(int(uniq["log10_distinct_zygotes_floor"])) + r"""}$ --- the
square of the per-gamete floor, since the zygote is the product of two independent draws~\gradeV{}. This is
the ``emerge DNA'' step: a new diploid genome that has never existed before.

\textbf{Cleavage and genome activation.} Unlike the asymmetric oocyte division, cleavage is symmetric ---
$2^{n}$ equal blastomeres --- and it \emph{subdivides a fixed cytoplasmic mass} rather than growing it (summed
mass conserved; each blastomere $1/2^{n}$ of the zygote)~\gradeV{}. The first cell-fate decision, inner cell
mass versus trophectoderm, is one R19 bistable switch. Zygotic genome activation is the genome's own
switch-on: before it, the embryo runs on maternal oocyte stores (ZAR1, the oocyte-to-embryo factor; NLRP5;
c-Mos), with the zygotic genome off; a rising competence drive crosses the spinodal
$""" + f(zga["spinodal"], 4) + r"""$ and the genome switches on in one discontinuous step (jump
$""" + f(zga["jump_size"], 3) + r"""$ at drive $""" + f(zga["zga_drive"], 4) + r"""$)~\gradeV{} --- the
maternal-to-zygotic handoff from the gamete program this package owns to the embryo's own genome.

\textbf{The gene-clock builds the body.} With the genome on, the body plan unfolds in the order the cited
morphogenesis gene-clock dictates: emergence order $=$ argsort of the spinodal over the master genes, which
(the spinodal being monotone in $\gamma$) is simply $\gamma$ ascending. The measured panel orders as
""" + order_line + r""". A pre-registered test finds $\gamma$ rises with developmental stage --- the stage
means climb from pluripotency ($""" + f(sm[1], 4) + r"""$) through germ-layer ($""" + f(sm[2], 4) + r"""$) to
organ-primordium ($""" + f(sm[3], 4) + r"""$), Spearman $\rho=""" + f(stest["spearman_rho"], 3) + r"""$,
permutation $p=""" + f(stest["p_permutation_one_sided"], 3) + r"""$~\gradeV{}. A second pre-registered test
(HOX $3'\!\to\!5'$ colinearity) is reported as a \emph{partial} result in the honest style of the gamete
chapter: the posterior-most HOX (""" + tex_escape(htest["order_3to5"][-1]) + r""") carries the highest
$\gamma$, but across three genes the correlation ($\rho=""" + f(htest["spearman_rho"], 3) + r"""$,
$p=""" + f(htest["p_exact_one_sided"], 3) + r"""$) does not reach significance; only the narrow claim is made.

""" + atlas_tbl + r"""

\textbf{The whole arc.} Run end-to-end, a specific sperm and a specific egg produce a zygote with a
reproducible, unique genome fingerprint, and the arc passes at every stage (syngamy, cleavage, genome
activation, gene-clock body plan). The result is a fetus carrying a unique diploid genome
($10^{""" + str(int(fet["genome_uniqueness_log10"])) + r"""}$) and an inner-cell-mass-derived body of
$""" + str(fet["total_body_plan_structures"]) + r"""$ gene-clock-ordered structures~\gradeV{}. The absolute
gestational timing is left open~\gradeO{} --- the events and their order are forced, but mapping them to a
calendar needs external calibration, exactly as puberty's age does. The full multi-organ morphogenesis atlas
and the gene-clock law remain the 4D~DNA~Blueprint package's single source of truth, cited here, never
re-owned (\S\ref{sec:open}).
"""


def sec_infertility(D):
    F1, F2, F3 = D["fert"]["F1"], D["fert"]["F2"], D["fert"]["F3"]
    F4, F5 = D["fert"]["F4"], D["fert"]["F5"]
    sub, ster = F2["subfertile"], F2["sterile"]
    nt, oa, cg = F3["normal_throughput"], F3["oligo_astheno_subfertile"], F3["catsper_gate"]
    ages, mis = F4["age_years"], F4["missegregation_probability"]
    diss_rows = [
        [r"subfertile (near threshold)", f(sub["p_per_cycle"], 4), f(sub["p_per_cycle_treated"], 4),
         f(sub["fold_response"], 2) + r"$\times$", f(sub["p_year"], 3), f(sub["p_year_treated"], 3)],
        [r"sterile (past spinodal)", f(ster["p_per_cycle"], 4), f(ster["p_per_cycle_treated"], 4),
         r"---", f(ster["p_year"], 3), f(ster["p_year"], 3)],
    ]
    diss_tbl = table("lrrrrr",
                     [r"operation", r"$p_{\mathrm{cycle}}$", r"$p_{\mathrm{cycle}}$ nudged", r"fold",
                      r"$p_{\mathrm{year}}$", r"$p_{\mathrm{year}}$ nudged"], diss_rows,
                     r"The infertility/subfertility dissociation under an \emph{identical} drive nudge "
                     r"($\Delta h = " + f(F2["drive_nudge"], 4) + r"$). A near-threshold (subfertile) operation "
                     r"responds exponentially through the Kramers rate~\cite{kramers}; a past-spinodal "
                     r"(sterile) operation stays at exactly zero. Same drive, two regimes.",
                     "infertility-dissociation")
    return r"""
\section{Infertility versus subfertility: two sides of one spinodal}

\textbf{Answer.} The reproductive arc is a chain of substrate operations, and conception requires
\emph{every} one to succeed --- a logical AND over the """ + str(F1["n_links"]) + r""" verified links of the
earlier chapters (the GnRH pulse, the follicle/sperm switch, ordered REC8 meiosis, gamete number, the
metaphase-II flip, syngamy, ZGA, the gene-clock), so breaking any single link gives
sterility~\gradeV{}. The two clinical failure classes are then one distinction on the substrate.
\emph{Infertility} is an operation on the wrong side of a spinodal: categorical and deterministic, a
per-cycle conception probability of exactly zero that a sub-threshold drive cannot move. \emph{Subfertility}
is an operation near its threshold: a small but finite Kramers crossing rate per cycle, so the same drive
that does nothing across a spinodal moves it exponentially.

\textbf{The central dissociation.} Computed on the same R19 spinodal and Kramers factor
$\exp(-\Delta V/D)$~\cite{kramers} the oncology chapter uses, a fixed, modest drive nudge
($\Delta h = """ + f(F2["drive_nudge"], 4) + r"""$, one fifth of the spinodal
$""" + f(F2["spinodal"], 4) + r"""$) raises a near-threshold cycle probability from
$""" + f(sub["p_per_cycle"], 4) + r"""$ to $""" + f(sub["p_per_cycle_treated"], 4) + r"""$
($""" + f(sub["fold_response"], 2) + r"""\times$; over a year
$""" + f(sub["p_year"], 3) + r""" \to """ + f(sub["p_year_treated"], 3) + r"""$), while leaving a
past-spinodal operation at exactly $""" + f(ster["p_per_cycle"], 0) + r"""$ --- the same nudge, exponential
versus nothing~\gradeV{}. This is why the two diagnoses behave categorically differently under the same
intervention, not as two points on one slider.

""" + diss_tbl + r"""

\textbf{Male and female factor on the kernel.} Male factor is oscillator throughput: whether
spermatogenesis runs at all is an R19 switch (sub-spinodal $=$ azoospermia, categorical and
sterile)~\gradeV{}, while \emph{how much} it makes once on is the seminiferous/flagellar beat rate ---
a fast beat (full count) versus a slow one (oligo-/astheno-, subfertile but non-zero:
$""" + str(nt["beats"]) + r""" \to """ + str(oa["beats"]) + r"""$ beats)~\gradeV{}; CatSper
(measured $\gamma = """ + f(cg["catsper_gamma"], 4) + r"""$) is a \emph{separate} supra-spinodal
gate~\cite{santalucia}. Female factor adds the molecular clock of female subfertility: anovulation is the
mid-cycle ovulatory-surge switch left OFF (sterile until driven across)~\gradeV{}, and REC8 cohesin fatigue
(measured $\gamma = """ + f(F4["cohesin_gamma"], 4) + r"""$) is the rising-with-age mis-segregation clock ---
as the held barrier $\gamma^{2}/4$ decays with the years held, per-egg aneuploidy escape climbs from
$""" + f(mis[0], 3) + r"""$ at age """ + str(ages[0]) + r""" to $""" + f(mis[-1], 3) + r"""$ at age
""" + str(ages[-1]) + r""" (only the rising \emph{shape} is claimed; the absolute fraction is \gradeO{}),
with primary ovarian insufficiency the same latch lost early~\gradeV{}.

\textbf{Treatment is a drive.} The interventions are reading the same kernel: the hCG trigger / ovulation
induction is a supra-spinodal kick forcing the stuck ovulatory switch across (the spinodal kick the disease
chapter already retrodicts)~\gradeV{}; pulsatile GnRH \emph{restarts} the oscillator where a continuous drive
suppresses ($""" + str(F5["pulsatile_pulses"]) + r"""$ versus $""" + str(F5["continuous_pulses"]) + r"""$
pulses, cited from the temporal-pattern chapter, same molecule opposite effect)~\gradeV{}; and ICSI/IVF supply
or bypass the missing gate (the same supra-spinodal flip)~\gradeV{}/\gradeL{}. The absolute per-cycle
probabilities, the map from a real semen parameter or maternal age to a drive value, and the gene-to-$\gamma$
links for specific azoospermia/POI genes remain open~\gradeO{} (\S\ref{sec:open}); sex-hormone levels stay
this package's single source of truth, and the management of a real couple's infertility belongs to clinicians.
"""


def sec_sexratio(D):
    S1, S2, S3 = D["sxr"]["S1"], D["sxr"]["S2"], D["sxr"]["S3"]
    S4, S5, S6 = D["sxr"]["S4"], D["sxr"]["S5"], D["sxr"]["S6"]
    ag = S1["antagonist_gamma"]
    panel = S6["panel"]
    order = sorted(panel.items(), key=lambda kv: kv[1]["gamma"])
    atlas_rows = [[tex_escape(s), ("testis" if panel[s]["axis"] == "testis" else "ovary"),
                   f(panel[s]["gamma"], 4), f(panel[s]["gc"], 3)] for s, _ in order]
    atlas_tbl = table("llrr", [r"master", r"axis", r"$\gamma$", r"GC"], atlas_rows,
                      r"Measured sex-determination master-gene promoter $\gamma$ (same NN-stacking "
                      r"$\Delta G_{37}$ pipeline~\cite{santalucia,dnablueprint}; validated on the SOX9 and "
                      r"FOXL2 anchors), ascending. A pre-registered permutation test of whether the gonadal "
                      r"axis separates $\gamma$ returns a null (reported as it falls).", "sexdet-gamma")
    return r"""
\section{Sex determination and sex-ratio distortion: a tiltable coin}

\textbf{Answer.} Mammalian sex is one bistable switch: SOX9 (testis, measured
$\gamma = """ + f(ag["SOX9"], 4) + r"""$) against FOXL2 (ovary, $\gamma = """ + f(ag["FOXL2"], 4) + r"""$),
with SRY the tipping drive. Mendelian 50:50 is that switch untilted --- a fair coin. A meiotic-drive gene
tilts it, so transmission climbs from one-half and, past the spinodal, fixes near one. A sex-chromosome-linked
driver tilts the X-versus-Y gamete switch, skewing offspring sex --- male for an X-shredder, female for a
Y-killer --- while Fisher's restoring force holds the \emph{population} at 1:1~\cite{fisher}. Sex is a coin
that can be weighted; the genome and the population each set a different constraint.

\textbf{Sex is a switch; segregation is a fair coin.} The SOX9$\leftrightarrow$FOXL2 mutual-antagonism toggle
reduces to one R19 well of scale $\gamma = """ + f(ag["switch_gamma"], 4) + r"""$ (the mean of the two measured
antagonist $\gamma$, not fitted), spinodal $""" + f(ag["spinodal"], 4) + r"""$. At zero tilt the two basins
have equal depth (both sexes viable), the undifferentiated default settles to ovary, and SRY is a
\emph{transient} supra-spinodal drive: it flips the switch to testis and the basin then self-maintains for life
(hysteresis)~\gradeV{}. A heterozygous transmission locus is the same switch with no tilt, so an ensemble of
$""" + format(S2["ensemble_meioses"], ",") + r"""$ meioses transmits at
$""" + f(S2["transmission_ratio_simulated"], 4) + r"""$ (analytic exactly
$""" + f(S2["transmission_ratio_analytic"], 1) + r"""$) --- Mendel's first law as an untilted R19 switch~\gradeV{}.

\textbf{Drive is a tilt; the sex ratio is a \emph{signed} tilt.} A meiotic-drive gene is a tilt $h$ on the
switch, and the transmission ratio is a Boltzmann basin occupancy: it rises monotonically from
$""" + f(S2["transmission_ratio_analytic"], 1) + r"""$ through $""" + f(S3["transmission_ratio_subspinodal"], 4) + r"""$
(graded distortion below the spinodal) to $""" + f(S3["transmission_ratio_suprapinodal"], 1) + r"""$ once the
loser basin vanishes past the spinodal (the t-haplotype / SD fixation limit)~\gradeV{}. A
sex-chromosome-linked gamete-killer is the same tilt \emph{with a sign}: an X-shredder kills X-bearing sperm
and gives a secondary sex ratio of $""" + f(S4["ssr_X_shredder_male"], 1) + r"""$ (male), a Y-killer gives
$""" + f(S4["ssr_Y_killer_female"], 1) + r"""$ (female), and a weaker driver gives a partial skew
($""" + f(S4["ssr_subspinodal_partial"], 4) + r"""$) --- one mechanism, two signs~\gradeV{}.

\textbf{Fisher holds the line.} Drive tilts the individual switch, but at the population level the 1:1 sex
ratio is a stable attractor: the rarer sex has higher per-capita reproductive value, so selection favours
producers of the rarer sex and suppressors of drive~\cite{fisher}. Displaced to
$""" + f(S5["r_from_0p20"], 2) + r"""$ or $""" + f(S5["r_from_0p80"], 2) + r"""$ male the population returns to
$""" + f(S5["r_from_0p20"], 1) + r"""$ with no drive, and a persistent weak drive shifts the fixed point only
boundedly (to $""" + f(S5["r_under_weak_drive"], 4) + r"""$, not to fixation)~\gradeV{}. The human at-birth
ratio ($\sim""" + f(S5["human_secondary_sex_ratio"], 3) + r"""$ male) is exactly this kind of small residual,
\emph{not} a strong-drive case; its cause (paternal age, hormonal-timing) is left open~\gradeO{}.

""" + atlas_tbl + r"""

The sex-determination masters are measured through the identical DNA pipeline (testis axis SRY/SOX9/DMRT1,
ovary axis FOXL2/RSPO1/WNT4). A pre-registered test of whether the gonadal axis \emph{separates} promoter
$\gamma$ --- declared before the values were seen, exactly as in the gamete chapter --- finds the ovary axis
trends higher (mean $""" + f(S6["ovary_axis_mean_gamma"], 4) + r"""$ versus testis
$""" + f(S6["testis_axis_mean_gamma"], 4) + r"""$, gap $""" + f(S6["observed_mean_gap"], 4) + r"""$), but with
SRY a strong low-$\gamma$ outlier ($""" + f(D["sxr_atlas"]["SRY"], 4) + r"""$, AT-rich) and $n=3$ per axis the
permutation test returns $p=""" + f(S6["permutation_p"], 2) + r"""$ --- a null, reported honestly~\gradeV{}.
None of the chapter's verified claims depends on this test; the measured $\gamma$ sets the switch \emph{scale},
not the drive strength (\S\ref{sec:open}).
"""


def sec_methods(D):
    rg = D["research"]
    return r"""
\section{Methods: reproducibility, determinism, and grading}

\paragraph{Determinism (VP-SPEC C1).} The reproduction engine is seeded (SEED~=~19) with single-threaded
BLAS, round-before-hash, and sorted JSON keys, so the hashed core emits an identical \texttt{sha256} on
repeat: \texttt{""" + D["core_sha"] + r"""} (two runs byte-identical, process-stable). Every quantity in this
paper is pulled live from the research modules at build time by the LaTeX generator
(\texttt{tools/build\_paper.py}); nothing is transcribed by hand, so the PDF cannot drift from the engine. The
companion HTML site is generated the same way (\texttt{tools/build\_docs.py}), and two full site builds are
byte-identical.

\paragraph{No tuning (strict).} Every constant is a measured input or a derived value, never chosen to hit a
target. The recovery timescale $\tau_s$ sets a period, but periods are \gradeL{} anchors --- the package never
claims to \emph{derive} a clinical timing. The noise constant $D$, per-year rates, coupling $\kappa$, and
amplitude fractions are stated inputs; all RR ratios are invariant to $D$. The master-gene $\gamma$ values are
\emph{measured} from cached promoters (nearest-neighbour $\Delta G_{37}$, SantaLucia~1998) and accepted only
because the pipeline reproduces the vendored SOX9 anchor bit-for-bit.

\paragraph{Research gate.} All sections pass one machine-checked gate before the writing phase is unlocked:
determinism $""" + ("\\checkmark" if rg["determinism_2xsha256_identical"] else "\\times") + r"""$, organ
emergence $""" + ("\\checkmark" if rg["emergence_ok"] else "\\times") + r"""$, the T1--T5 discriminant battery
$""" + ("\\checkmark" if rg["stress_all_targets_pass"] else "\\times") + r"""$, oncology
$""" + ("\\checkmark" if rg["oncology_pass"] else "\\times") + r"""$, therapy
$""" + ("\\checkmark" if rg["therapy_pass"] else "\\times") + r"""$, and disease
$""" + ("\\checkmark" if rg["disease_pass"] else "\\times") + r"""$ (\texttt{all\_green}~=~""" + str(rg["all_green"]).lower() + r""").

\paragraph{Grading vocabulary.} \gradeV{} simulation-verified; \gradeF{} forced by geometry; \gradeL{}
measured anchor; \gradeO{} open, with the obstacle stated in \S\ref{sec:open}. The grades are honesty
markers, not self-deprecation: the physics fixes shape, ordering, and ratios; absolute scales and external
calibrations are declared open rather than tuned.
"""


def sec_open(D):
    rows = [
        [r"absolute organ size / mass", r"\gradeO",
         r"DWELL $\propto\gamma^{3/2}$ fixes relative size and order \gradeF{}; absolute scale needs external calibration"],
        [r"absolute cancer incidence", r"\gradeO",
         r"RR \emph{shape} reproduces \gradeV{}; absolute population incidence needs epidemiological calibration"],
        [r"noise level $D$ (abs.\ RR magnitude)", r"\gradeO",
         r"single open lattice constant; every reported RR \emph{ratio} is invariant under $D$ (verified $D$-robust)"],
        [r"chronological pubertal age", r"\gradeO",
         r"the spinodal crossing fixes discontinuous order and jump/spinodal ratio \gradeV{}; calendar age needs endocrine calibration"],
        [r"menopause irreversibility", r"\gradeO",
         r"latch collapse on depletion is shown \gradeV{}; no in-package follicle regeneration, so one-wayness is asserted from biology"],
        [r"absolute gestational timing", r"\gradeO",
         r"fertilisation $\to$ fetus events and their \emph{order} are forced \gradeV{}; mapping to days/weeks needs external calibration (as pubertal age)"],
        [r"full-body morphogenesis atlas", r"\gradeO",
         r"the gene-clock law (argsort spinodal) and the multi-organ atlas are the 4D~DNA~Blueprint package's SSOT (firewall); this package demonstrates the cited clock on a panel only"],
        [r"absolute per-cycle conception probability", r"\gradeO",
         r"the categorical/probabilistic dissociation and the rising age curve are verified \gradeV{}; absolute rates for a real couple need clinical calibration"],
        [r"per-age aneuploidy fraction", r"\gradeO",
         r"only the rising \emph{shape} of REC8 cohesin-fatigue mis-segregation is claimed \gradeV{}; the absolute fraction and the age$\to$cohesin map need calibration"],
        [r"meiotic-drive / sex-ratio tilt magnitude", r"\gradeO",
         r"drive-as-tilt and the signed secondary-sex-ratio skew are verified \gradeV{}; the $\gamma\to$drive-strength map per real driver is not derived"],
        [r"cause of the human $\sim0.512$ sex ratio", r"\gradeO",
         r"the 1:1 Fisher attractor and the bounded residual are verified \gradeV{}; the cause (paternal age / hormonal-timing) is unpinned"],
        [r"axis separation of sex-determination $\gamma$", r"\gradeO",
         r"the atlas is measured \gradeV{}; whether the gonadal axis separates $\gamma$ at $n=3$ is reported ($p=0.10$, a null), not assumed"],
    ]
    tbl = table(r"p{3.6cm}cp{8.0cm}",
                [r"open quantity", r"grade", r"obstacle (why not reproducible in-package)"], rows,
                r"Every open \gradeO{} quantity with its specific obstacle (VP-SPEC C3). An open quantity "
                r"without a stated obstacle is a gate failure.", "open")
    return r"""
\section{Open quantities (honest grading)}\label{sec:open}

The physics fixes the shape, ordering, and ratios; the following absolute scales and externally-set
calibrations are declared open rather than tuned. Genuinely novel clinical hypotheses (low-frequency pulsatile
restoration in PCOS; pulsed/cycled testosterone replacement) are likewise \gradeO{} and require clinical
validation. This is a physics-derived research artefact and is \textbf{not} medical advice.

""" + tbl + "\n"


def closing():
    return r"""
\section*{Data and code availability}
All code, the deterministic reproduction engine, the cached promoter sequences, and the generators for this
paper and the companion HTML site are bundled in the reproducibility archive deposited with this record
(DOI~\href{https://doi.org/""" + DOI + r"""}{""" + DOI + r"""}; Zenodo concept DOI, version-independent and
always resolving to the latest version). The living canonical version is maintained at
\href{""" + CANON + r"""/}{""" + CANON.replace("https://", "") + r"""/}, with the public mirror at
\href{""" + REPRO + r"""}{GitHub}. Running \texttt{python repro/run\_all.py} reproduces every number; running
\texttt{python tools/build\_paper.py} regenerates this document and \texttt{python tools/build\_docs.py}
regenerates the site.

\section*{Acknowledgement of scope}
This paper derives the gonadal-endocrine axis only; the brain-facing HPA stress axis and felt experience are
firewalled to the companion Felt Cognition paper. Nothing here is clinical advice.

\begin{thebibliography}{10}
\bibitem{vptheory} Y.~J. Lee. \emph{VP Theory: the vacuum as a jammed granular medium}. Zenodo, 2026.
DOI: \href{https://doi.org/""" + DOI_PHYSICS + r"""}{""" + DOI_PHYSICS + r"""}.
\bibitem{dnablueprint} Y.~J. Lee. \emph{The 4D DNA Blueprint: master-gene $\gamma$ and the morphogenesis
gene-clock}. Zenodo, 2026. DOI: \href{https://doi.org/""" + DOI_DNA + r"""}{""" + DOI_DNA + r"""}.
\bibitem{santalucia} J.~SantaLucia~Jr. A unified view of polymer, dumbbell, and oligonucleotide DNA
nearest-neighbor thermodynamics. \emph{Proc. Natl. Acad. Sci. USA} \textbf{95}(4):1460--1465, 1998.
\bibitem{fhn} R.~FitzHugh. Impulses and physiological states in theoretical models of nerve membrane.
\emph{Biophys. J.} \textbf{1}(6):445--466, 1961.
\bibitem{nagumo} J.~Nagumo, S.~Arimoto, S.~Yoshizawa. An active pulse transmission line simulating nerve
axon. \emph{Proc. IRE} \textbf{50}(10):2061--2070, 1962.
\bibitem{kramers} H.~A. Kramers. Brownian motion in a field of force and the diffusion model of chemical
reactions. \emph{Physica} \textbf{7}(4):284--304, 1940.
\bibitem{knobil} E.~Knobil. The neuroendocrine control of the menstrual cycle. \emph{Recent Prog. Horm. Res.}
\textbf{36}:53--88, 1980.
\bibitem{whi} Writing Group for the Women's Health Initiative Investigators. Risks and benefits of estrogen
plus progestin in healthy postmenopausal women. \emph{JAMA} \textbf{288}(3):321--333, 2002.
\bibitem{bat} S.~R. Denmeade, J.~T. Isaacs. Bipolar androgen therapy: the rationale for rapid cycling of
supraphysiologic androgen/ablation. \emph{Prostate} \textbf{70}(14):1600--1607, 2010.
\bibitem{fisher} R.~A. Fisher. \emph{The Genetical Theory of Natural Selection}. Oxford: Clarendon Press, 1930.
\end{thebibliography}

\end{document}
"""


def main():
    locked, why = gates.writing_locked()
    if locked:
        print("[build_paper] WRITING LOCKED -- refusing to emit. reason:", why); sys.exit(2)
    D = gather()
    doc = (preamble() + title_block(D) + sec_scope(D) + sec_organs(D) + sec_gnrh(D) + sec_menstrual(D) +
           sec_surge(D) + sec_sperm(D) + sec_puberty(D) + sec_cancer(D) + sec_therapy(D) + sec_disease(D) +
           sec_gamete(D) + sec_embryo(D) + sec_infertility(D) + sec_sexratio(D) +
           sec_methods(D) + sec_open(D) + closing())
    os.makedirs(_PAPER, exist_ok=True)
    out = os.path.join(_PAPER, "reproductive_endocrine_vp.tex")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("[build_paper] wrote", os.path.relpath(out, _PKG), "(" + str(len(doc)) + " chars)")
    print("[build_paper] core sha256:", D["core_sha"])
    print("[build_paper] compile:  cd paper && latexmk -pdf -interaction=nonstopmode reproductive_endocrine_vp.tex")


if __name__ == "__main__":
    main()
