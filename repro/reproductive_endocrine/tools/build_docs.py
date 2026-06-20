#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Reproductive / Gonadal-Endocrine WRITING phase: per-title canonical SEO HTML generator.

HARD RULE: refuses while gates.writing_locked() is True (research signed off + PHASE=="writing").
WHEN UNLOCKED, follows VP-SPEC v1.8 (../VP_SPEC_v1_8.md): canonical HTML in docs/ (C2); ONE page per
title/section (C4 sec 6): answer-first <p class="answer"> 40-60 words, self-contained, JSON-LD
ScholarlyArticle + BreadcrumbList, canonical link, claim-strip (grade+repro+DOI), vp-card per cited
locked quantity; ENGLISH body (C0); honest grades + stated obstacles for [O] (C3); deterministic
numbers from the engine (C1). Output: docs/<slug>/index.html + hub + _meta.json + sitemap + robots + llms.

DETERMINISM: every displayed number is pulled LIVE from the research modules (run_T1..run_T5,
run_oncology, run_therapy, run_disease, emerge_organs) at build time -- the site cannot drift from the
engine because it never hard-codes a result. Display equations are rendered to canonical SVG (matplotlib
mathtext, date metadata suppressed + fixed hashsalt -> byte-stable). Two runs produce byte-identical docs/.
"""
import os, sys, json, math, re, hashlib, importlib

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.join(_HERE, "..")
_DOCS = os.path.join(_PKG, "docs")
_EQ   = os.path.join(_DOCS, "eq")
_ASSETS = os.path.join(_DOCS, "assets", "css")
_REPORTS = os.path.join(_PKG, "reports")
_MANIFEST = os.path.join(_PKG, "manifest", "reproductive_endocrine_vp_site.csv")
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_verify"))
gates = importlib.import_module("gates")

# ---------------------------------------------------------------------------------------------------
# Paper registry (this self-contained package; not yet in the central 9-paper LOCK registry).
# DOI is honestly PENDING -- the package has no Zenodo deposit yet, so we never invent one (C1/C3).
# ---------------------------------------------------------------------------------------------------
PAPER_ID = "reproductive-endocrine"
CODE     = "rep"
SHORT    = "Reproductive Endocrine"          # title-suffix abbreviation
TITLE    = ("Reproductive and Gonadal-Endocrine Emergence: the HPG Oscillator, "
            "the Menstrual Cycle, and Hormone-Driven Cancer")
BRANCH   = "jamming"
AUTHOR   = "Young Jae Lee"
ORCID    = "https://orcid.org/0009-0002-7535-8245"
LICENSE  = "https://creativecommons.org/licenses/by/4.0/"
CANON    = "https://jamming-physics.org/" + PAPER_ID          # deployment target (hub)
REPRO    = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/" + PAPER_ID
DOI         = "10.5281/zenodo.20754657"      # Zenodo *concept* DOI -- version-independent, always latest
DOI_URL     = "https://doi.org/" + DOI
# This is the Zenodo concept DOI: it always resolves to the newest version of the deposit, so it is the
# correct identifier to cite and the only DOI used as the package identifier. (Per-version DOIs are not used.)
DOI_PHYSICS = "10.5281/zenodo.17932566"      # VP Theory (jammed-vacuum substrate; R19/spinodal/barrier)
DOI_DNA     = "10.5281/zenodo.20471407"      # 4D DNA Blueprint (master-gene gamma; DWELL)

# ---------------------------------------------------------------------------------------------------
# Deterministic equation rendering: LaTeX -> canonical SVG (VP-SPEC C2/section 7B).
# ---------------------------------------------------------------------------------------------------
import matplotlib
matplotlib.use("svg")
matplotlib.rcParams["svg.hashsalt"] = "rep-endocrine"      # stable element ids -> byte-deterministic
matplotlib.rcParams["mathtext.fontset"] = "cm"
import matplotlib.pyplot as plt

_EQ_DIM = {}   # eq_id -> (w_px, h_px, latex)

def render_eq(eq_id, latex):
    """Render one display equation to docs/eq/{eq_id}.svg; record (w,h,latex). Deterministic."""
    os.makedirs(_EQ, exist_ok=True)
    fig = plt.figure(figsize=(0.1, 0.1))
    fig.text(0.0, 0.0, "$" + latex + "$", fontsize=16)
    path = os.path.join(_EQ, eq_id + ".svg")
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.04,
                transparent=True, metadata={"Date": None})
    plt.close(fig)
    head = open(path, encoding="utf-8").read(1200)
    w = re.search(r'width="([\d.]+)pt"', head); h = re.search(r'height="([\d.]+)pt"', head)
    wpx = int(round(float(w.group(1)) * 1.333)) if w else 200
    hpx = int(round(float(h.group(1)) * 1.333)) if h else 40
    _EQ_DIM[eq_id] = (wpx, hpx, latex)
    return eq_id

# canonical display equations (rendered once; referenced by id on the relevant pages)
EQS = {
 "rep-sub-001": r"V(s) = -\frac{1}{2}\gamma s^{2} + \frac{1}{4}s^{4} - h\,s",
 "rep-sub-002": r"\dot s = \gamma s - s^{3} + h \;\Rightarrow\; s^{3} - \gamma s - h = 0",
 "rep-sub-003": r"h_{\mathrm{sp}}(\gamma) = 2\left(\frac{\gamma}{3}\right)^{3/2}",
 "rep-sub-004": r"\Delta V_{0}(\gamma) = \frac{\gamma^{2}}{4}",
 "rep-gam-001": r"\gamma = -\,\langle \Delta G_{37}^{\,\mathrm{NN}} \rangle \quad(\mathrm{SantaLucia\ 1998})",
 "rep-dwl-001": r"\mathrm{DWELL}(\gamma) = \frac{\gamma^{3/2}}{K + \mathrm{brake}}",
 "rep-onc-001": r"\Delta V(\gamma,h) = V(s_{\mathrm{saddle}}) - V(s_{\mathrm{meta}})",
 "rep-onc-002": r"\mathrm{RR}(\mathrm{dose}) = \frac{\exp[-\Delta V(h)/D]}{\exp[-\Delta V(0)/D]}",
 "rep-gmt-001": r"(2N,2C)\;\to\;(2N,4C)\;\to\;(1N,2C)\;\to\;(1N,1C)",
 "rep-gmt-002": r"N_{\mathrm{assort}} = 2^{\,n} = 2^{23} = 8388608",
 "rep-gmt-003": r"F = \frac{\mathrm{Var}(k)}{\langle k\rangle} < 1",
 "rep-gmt-004": r"\tau^{\,\mathrm{flag}}_{s} < \tau^{\,\mathrm{pulse}}_{s} < \tau^{\,\mathrm{spm}}_{s} < \tau^{\,\mathrm{men}}_{s}",
 "rep-gmt-005": r"\mathrm{Ca}^{2+} > h_{\mathrm{sp}}(\gamma) \;\Rightarrow\; \mathrm{fertilise}",
 "rep-emb-001": r"(1N,1C)_{\mathrm{sperm}} + (1N,1C)_{\mathrm{egg}} \;\to\; (2N,2C)_{\mathrm{zygote}}",
 "rep-emb-002": r"N_{\mathrm{zygote}} \gtrsim \left(N_{\mathrm{gamete}}\right)^{2} \approx 10^{94}",
 "rep-emb-003": r"n_{\mathrm{cells}} = 2^{k}, \qquad \sum_i m_i = m_{\mathrm{zygote}}\ \mathrm{(conserved)}",
 "rep-emb-004": r"h_{\mathrm{competence}} > h_{\mathrm{sp}}(\gamma) \;\Rightarrow\; \mathrm{genome\ ON\ (ZGA)}",
 "rep-emb-005": r"\mathrm{emergence\ order} = \mathrm{argsort}\,[\,h_{\mathrm{sp}}(\gamma)\,] = \mathrm{argsort}(\gamma)",
 "rep-inf-001": r"P_{\mathrm{conceive}} = \prod_{i=1}^{8} g_i \in \{0,1\}",
 "rep-inf-002": r"p_{\mathrm{cycle}} = p_{\max}\,\exp\!\left[-\frac{\Delta V(d)-\Delta V_{0}}{D}\right]",
 "rep-inf-003": r"d \geq h_{\mathrm{sp}}\,\Rightarrow\,p=0\ \ (\mathrm{sterile});\quad d < h_{\mathrm{sp}}\,\Rightarrow\,p>0\ \ (\mathrm{subfertile})",
 "rep-inf-004": r"P_{\mathrm{year}} = 1-\left(1-p_{\mathrm{cycle}}\right)^{12}",
 "rep-inf-005": r"P_{\mathrm{miss}}(\mathrm{age}) = \exp\!\left[-\frac{\Delta V_{0}\,c(\mathrm{age})}{D}\right],\quad c\downarrow",
 "rep-sxr-001": r"V(s) = -\frac{1}{2}\gamma\, s^{2} + \frac{1}{4}s^{4} - h_{\mathrm{SRY}}\,s",
 "rep-sxr-002": r"h=0 \;\Rightarrow\; \mathrm{TR} = \frac{1}{2}\quad(\mathrm{fair\ coin})",
 "rep-sxr-003": r"\mathrm{TR}(h) = \frac{e^{-V_{\mathrm{drv}}/D}}{e^{-V_{\mathrm{drv}}/D}+e^{-V_{\mathrm{los}}/D}}\;\to\;1\ \ (h>h_{\mathrm{sp}})",
 "rep-sxr-004": r"\mathrm{SSR} = \mathrm{TR}(\pm\,h_{\mathrm{drive}})",
 "rep-sxr-005": r"\dot r = -k\left(r-\frac{1}{2}\right)\;\Rightarrow\; r^{\star}=\frac{1}{2}\ \ (\mathrm{stable})",
}

def eq_fig(eq_id, caption=None):
    w, h, latex = _EQ_DIM[eq_id]
    cap = ('\n  <figcaption>' + caption + '</figcaption>') if caption else ''
    alt = latex.replace('"', "'")
    return ('<figure class="eq">\n  <img src="../eq/' + eq_id + '.svg" width="' + str(w) +
            '" height="' + str(h) + '" loading="lazy" alt="' + alt + '">' + cap + '\n</figure>')

# ---------------------------------------------------------------------------------------------------
# vp-cards: self-contained restatement of each cited LOCKED quantity (VP-SPEC 6-R.2).
# ---------------------------------------------------------------------------------------------------
VP_CARDS = {
 "spinodal": ('<aside class="vp-card" data-locked="spinodal"><b>h<sub>sp</sub> = 2(&gamma;/3)<sup>3/2</sup></b> '
              '&mdash; the R19 spinodal: the drive past which the opposite basin disappears, so the flip is '
              '<b>discontinuous</b> (= 0.3849 at &gamma;=1). <b>[F]</b> forced (geometric). '
              '<a href="https://doi.org/' + DOI_PHYSICS + '" rel="noopener">canonical derivation &mdash; VP Theory</a></aside>'),
 "barrier": ('<aside class="vp-card" data-locked="barrier"><b>&Delta;V<sub>0</sub> = &gamma;<sup>2</sup>/4</b> '
             '&mdash; the energy barrier between the two R19 basins (state stability); a sustained drive tilts '
             'the well and lowers it. <b>[F]</b> forced. '
             '<a href="https://doi.org/' + DOI_PHYSICS + '" rel="noopener">canonical derivation &mdash; VP Theory</a></aside>'),
 "dwell": ('<aside class="vp-card" data-locked="dwell"><b>DWELL &prop; &gamma;<sup>3/2</sup></b> '
           '&mdash; how long an R19 switch runs, setting <b>relative</b> organ size/run-length (DNA &sect;5). '
           'Order/direction <b>[F]</b> forced; absolute magnitude <b>[O]</b> (external calibration). '
           '<a href="https://doi.org/' + DOI_DNA + '" rel="noopener">canonical derivation &mdash; 4D DNA Blueprint</a></aside>'),
 "gamma": ('<aside class="vp-card" data-locked="gamma-method"><b>&gamma; = &minus;&lang;&Delta;G<sub>37</sub><sup>NN</sup>&rang;</b> '
           '&mdash; the morphogenesis identity constant: minus the mean nearest-neighbour stacking free energy '
           '(SantaLucia 1998) over the proximal promoter (TSS&minus;2000..+500, GRCh38). <b>[V]</b> measured, never fitted. '
           '<a href="https://doi.org/' + DOI_DNA + '" rel="noopener">canonical pipeline &mdash; 4D DNA Blueprint</a></aside>'),
}

def cards(*keys):
    return "\n".join(VP_CARDS[k] for k in keys)

# ---------------------------------------------------------------------------------------------------
# Minimal external stylesheet (no inline CSS allowed -- VP-SPEC 6 template rule).
# ---------------------------------------------------------------------------------------------------
SITE_CSS = """\
:root{
  --ink:#15171a; --muted:#5b6470; --line:#e3e7ec; --bg:#ffffff; --soft:#f6f8fa;
  --accent:#7a1f4b; --accent-soft:#fbeef3; --forced:#274b8a; --verified:#1f6b3a;
  --open:#9a5b00; --code:#0b1e3a;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:"SFMono-Regular",Menlo,Consolas,"Liberation Mono",monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--serif);
  font-size:18px;line-height:1.62;font-feature-settings:"kern" 1,"liga" 1}
main,header,footer{max-width:46rem;margin-inline:auto;padding-inline:1.25rem}
header{padding-top:1.4rem}
nav.crumb{font-family:var(--sans);font-size:.82rem;color:var(--muted);letter-spacing:.01em}
nav.crumb a{color:var(--accent);text-decoration:none}
nav.crumb a:hover{text-decoration:underline}
h1{font-size:1.92rem;line-height:1.2;letter-spacing:-.012em;margin:.7rem 0 .2rem;font-weight:650}
h2{font-family:var(--sans);font-size:1.22rem;font-weight:640;letter-spacing:-.006em;
  margin:2.1rem 0 .55rem;padding-top:.3rem;border-top:1px solid var(--line)}
h3{font-family:var(--sans);font-size:1.02rem;font-weight:620;margin:1.35rem 0 .4rem}
p{margin:.7rem 0}
a{color:var(--accent)}
p.answer{font-family:var(--sans);font-size:1.06rem;line-height:1.5;background:var(--accent-soft);
  border-left:3px solid var(--accent);border-radius:0 8px 8px 0;padding:.85rem 1.05rem;margin:.9rem 0 .2rem;color:#2a1622}
p.abstract{color:var(--muted);font-size:.98rem;margin:.7rem 0 0}
aside.claim-strip{display:flex;flex-wrap:wrap;gap:.5rem .75rem;align-items:center;
  font-family:var(--sans);font-size:.8rem;margin:1rem 0 .4rem;padding:.55rem .7rem;
  background:var(--soft);border:1px solid var(--line);border-radius:9px}
aside.claim-strip a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}
aside.claim-strip a:hover{border-bottom-color:var(--accent)}
aside.claim-strip .gate{color:var(--muted);font-variant:small-caps;letter-spacing:.04em}
.grade{font-weight:700;padding:.06rem .42rem;border-radius:999px;font-size:.76rem;white-space:nowrap}
.g-forced{background:#e9eefb;color:var(--forced)}
.g-verified{background:#e6f4ec;color:var(--verified)}
.g-open{background:#fbf0df;color:var(--open)}
aside.vp-card{font-family:var(--sans);font-size:.86rem;line-height:1.45;background:#fff;
  border:1px solid var(--line);border-left:3px solid var(--forced);border-radius:0 8px 8px 0;
  padding:.6rem .8rem;margin:.85rem 0}
aside.vp-card[data-locked="gamma-method"]{border-left-color:var(--verified)}
aside.vp-card b{color:var(--code)}
aside.vp-card a{text-decoration:none;border-bottom:1px solid #d7dde6}
figure.eq{margin:1.2rem 0;padding:.6rem 0;text-align:center;overflow-x:auto}
figure.eq img{max-width:100%;height:auto}
figure.eq figcaption{font-family:var(--sans);font-size:.78rem;color:var(--muted);margin-top:.4rem}
table{border-collapse:collapse;width:100%;font-family:var(--sans);font-size:.86rem;margin:1rem 0;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:.4rem .6rem;text-align:left;vertical-align:top}
thead th{background:var(--soft);font-weight:640}
tbody tr:nth-child(even){background:#fcfdfe}
code,.mono{font-family:var(--mono);font-size:.9em;background:var(--soft);padding:.05rem .3rem;border-radius:4px}
.note{font-size:.92rem;color:var(--muted);border-left:2px solid var(--line);padding-left:.8rem;margin:.9rem 0}
.disclaimer{font-family:var(--sans);font-size:.84rem;background:#fff8f8;border:1px solid #f0d9d9;
  border-radius:9px;padding:.7rem .85rem;color:#6b2a2a;margin:1.3rem 0}
nav.pn{display:flex;justify-content:space-between;gap:1rem;font-family:var(--sans);font-size:.84rem;
  margin:2.2rem 0 1rem;padding-top:.9rem;border-top:1px solid var(--line)}
nav.pn a{color:var(--accent);text-decoration:none}
footer{font-family:var(--sans);font-size:.8rem;color:var(--muted);border-top:1px solid var(--line);
  margin-top:2rem;padding-top:1rem;padding-bottom:2.2rem}
footer a{color:var(--accent);text-decoration:none}
.lede{font-size:1.18rem;line-height:1.5;color:#2a2f36;margin:1rem 0}
.thesis{font-family:var(--sans);background:var(--accent-soft);border-radius:10px;padding:1rem 1.1rem;margin:1.2rem 0;font-size:.96rem}
.thesis b{color:var(--accent)}
ol.toc{list-style:none;padding:0;margin:1.2rem 0}
ol.toc li{border:1px solid var(--line);border-radius:9px;padding:.7rem .9rem;margin:.5rem 0;
  display:flex;justify-content:space-between;align-items:baseline;gap:.8rem}
ol.toc a{font-family:var(--sans);font-weight:600;text-decoration:none;font-size:1rem}
ol.toc .cn{font-family:var(--mono);color:var(--muted);font-size:.8rem;min-width:2.2rem}
ol.toc .gr{margin-left:auto}
.results{font-family:var(--mono);font-size:.84rem;background:var(--soft);border:1px solid var(--line);
  border-radius:9px;padding:.8rem .9rem;margin:1.1rem 0;line-height:1.9}
@media (max-width:560px){body{font-size:17px}h1{font-size:1.62rem}main,header,footer{padding-inline:1rem}}
@media (prefers-color-scheme:dark){
  :root{--ink:#e7eaee;--muted:#9aa4b0;--line:#2a2f37;--bg:#0e1014;--soft:#161a20;
    --accent:#e98bb6;--accent-soft:#241019;--forced:#9db8ef;--verified:#7fd3a0;--open:#e3b15f;--code:#cfe0ff}
  aside.vp-card,ol.toc li{background:#12151a}
  .disclaimer{background:#1c1314;border-color:#3a2526;color:#e7b8b8}
  thead th{background:#161a20}
}
"""

# ---------------------------------------------------------------------------------------------------
# Live data: every displayed number is pulled from the research modules at build time (C1).
# ---------------------------------------------------------------------------------------------------
def gather_data():
    for d in ("_engine", "_dynamics", "_oncology", "_therapy", "_disease", "_germline", "_embryo",
              "_fertility", "_sexratio"):
        sys.path.insert(0, os.path.join(_HERE, "..", "repro", d))
    eng = importlib.import_module("vp_rep_engine")
    hpg = importlib.import_module("hpg_axis")
    men = importlib.import_module("menstrual_cycle")
    spm = importlib.import_module("spermatogenesis")
    onc = importlib.import_module("carcinogen_dose_response")
    thr = importlib.import_module("temporal_pattern")
    dis = importlib.import_module("mechanisms")
    gmt = importlib.import_module("gametogenesis")
    emb = importlib.import_module("embryogenesis")
    fer = importlib.import_module("infertility")
    sxr = importlib.import_module("sex_ratio")
    em = eng.emerge_organs()
    _, core_sha = eng.emit(eng.circulate())
    germ = gmt.run_germline_battery()
    embryo = emb.run_embryo_battery()
    fert = fer.run_fertility_battery()
    sexr = sxr.run_sexratio_battery()
    return dict(emerge=em, T1=hpg.run_T1(), T5=hpg.run_T5(), T2=men.run_T2(),
                T3=men.run_T3(), T4=spm.run_T4(), onc=onc.run_oncology(),
                thr=thr.run_therapy(), dis=dis.run_disease(), core_sha=core_sha,
                germ={s["target"]: s for s in germ["suites_full"]},
                germ_atlas=gmt.panel_gamma_atlas(),
                emb={s["target"]: s for s in embryo["suites_full"]},
                emb_atlas=emb.panel_gamma_atlas(),
                fer={s["target"]: s for s in fert["suites_full"]},
                sxr={s["target"]: s for s in sexr["suites_full"]},
                sxr_atlas=sxr.panel_gamma_atlas(),
                research=gates.research_gate())

def f(x, n):
    return ("%." + str(n) + "f") % float(x)

# ---------------------------------------------------------------------------------------------------
# Grade badge: VP-SPEC 6 -- token -> g-class + label; page grade = most-frequent token (F>V>O).
# ---------------------------------------------------------------------------------------------------
_GLABEL = {"F": ("g-forced", "[F] forced"), "V": ("g-verified", "[V] sim-verified"),
           "L": ("g-verified", "[L] measured-anchor"), "O": ("g-open", "[O] open")}
def badge(tok):
    cls, lab = _GLABEL[tok]
    return '<span class="grade ' + cls + '">' + lab + '</span>'

# ---------------------------------------------------------------------------------------------------
# Per-title page template (VP-SPEC v1.8 section 6 + 6-R).
# ---------------------------------------------------------------------------------------------------
def page(ch, prev_ch, next_ch):
    slug, n, h1 = ch["slug"], ch["no"], ch["h1"]
    subj = ch["subj"]
    title_tag = subj + " &mdash; " + SHORT + " &sect;" + str(n) + " | Jamming Physics"
    canon = CANON + "/" + slug + "/"
    crumb_short = ch["crumb"]
    scholarly = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": subj,
        "isPartOf": {"@type": "CreativeWorkSeries", "name": SHORT, "sameAs": CANON + "/"},
        "position": n,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "isBasedOn": REPRO + "/" + slug + "/",
        "knowsAbout": ch["knows"],
        "license": LICENSE,
    }
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jamming-physics.org/"},
        {"@type": "ListItem", "position": 2, "name": SHORT, "item": CANON + "/"},
        {"@type": "ListItem", "position": 3, "name": "\u00a7" + str(n) + " " + crumb_short}]}
    grade_span = badge(ch["page_grade"])
    claim = ('<aside class="claim-strip">\n  ' + grade_span +
             '\n  <span class="gate">LOCK &rarr; Derive &rarr; Gate</span>'
             '\n  <a href="' + REPRO + '/" rel="noopener">reproduction code (GitHub)</a>'
             '\n  <a class="doi" href="' + DOI_URL + '" rel="noopener">DOI ' + DOI + '</a>\n</aside>')
    prev_a = ('<a rel="prev" href="../' + prev_ch["slug"] + '/">&larr; &sect;' + str(prev_ch["no"]) +
              "</a>") if prev_ch else '<a href="../">&larr; contents</a>'
    next_a = ('<a rel="next" href="../' + next_ch["slug"] + '/">&sect;' + str(next_ch["no"]) +
              " &rarr;</a>") if next_ch else '<a href="../">contents &rarr;</a>'
    head = "\n".join([
        '<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>' + title_tag + '</title>',
        '<meta name="description" content="' + ch["desc"] + '">',
        '<link rel="canonical" href="' + canon + '">',
        '<link rel="stylesheet" href="../assets/css/site.css">',
        '<script type="application/ld+json">',
        json.dumps(scholarly, ensure_ascii=False), '</script>',
        '<script type="application/ld+json">',
        json.dumps(breadcrumb, ensure_ascii=False), '</script>',
        '</head>'])
    body = "\n".join([
        '<body>',
        '<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="../">' + SHORT +
        '</a> &rsaquo; &sect;' + str(n) + '</nav></header>',
        '<main>',
        '<h1>' + h1 + '</h1>', '',
        '<p class="answer">' + ch["answer"] + '</p>', '',
        '<p class="abstract">' + ch["abstract"] + '</p>', '',
        claim, '',
        ch["cards"], '',
        ch["body"], '',
        '<nav class="pn">', '  ' + prev_a,
        '  <a href="../">paper contents</a>', '  ' + next_a, '</nav>',
        '</main>',
        '<footer>' + footer_html() + '</footer>',
        '</body>', '</html>'])
    return head + "\n" + body + "\n"

def footer_html():
    return ('<strong>' + SHORT + '</strong> &mdash; part of the VP Theory programme ('
            '<a href="https://doi.org/' + DOI_PHYSICS + '" rel="noopener">jamming branch</a>). '
            'Author <a href="' + ORCID + '" rel="noopener">' + AUTHOR + '</a> (ORCID). '
            'DOI: <a href="' + DOI_URL + '" rel="noopener">' + DOI + '</a>. '
            '<a href="' + LICENSE + '" rel="license noopener">CC BY 4.0</a>. '
            'Living version: <a href="' + CANON + '/">' + CANON.replace("https://", "") + '/</a>. '
            'Research package; falsifiable, deterministic, honestly graded &mdash; not clinical advice.')

# ---------------------------------------------------------------------------------------------------
# Table builders (numbers pulled from the live module returns)
# ---------------------------------------------------------------------------------------------------
def _tr(cells, head=False):
    tag = "th" if head else "td"
    return "<tr>" + "".join("<" + tag + ">" + str(c) + "</" + tag + "></" + tag[0:2] + ">"
                            .replace("</th>", "</th>").replace("</td>", "</td>") for c in cells) + "</tr>"

def table(headers, rows):
    h = "<tr>" + "".join("<th>" + str(c) + "</th>" for c in headers) + "</tr>"
    b = "".join("<tr>" + "".join("<td>" + str(c) + "</td>" for c in r) + "</tr>" for r in rows)
    return "<table>\n<thead>" + h + "</thead>\n<tbody>" + b + "</tbody>\n</table>"

def gamma_table(D):
    order = {o["organ"]: o for o in D["emerge"]["organs"]}
    rows = []
    for org in D["emerge"]["gamma_order_ascending"]:
        o = order[org]
        rows.append([o["master"], o["organ"].replace("_", " "), f(o["gamma"], 4),
                     f(o["functional_spinodal"], 4), f(o["rel_size_dwell"], 4), o["dyn_class"]])
    return table(["master gene", "organ", "&gamma; (measured)", "functional spinodal",
                  "rel. size (dwell)", "dynamical class"], rows)

def freq_table(D):
    rows = [[f(r["tau_s"], 0), r["pulses"], f(r["mean_interval_arb"], 1),
             f(r["pulse_rate_arb"], 6), r["favours"]] for r in D["T1"]["frequency_decoding"]["rows"]]
    return table(["recovery &tau;<sub>s</sub>", "pulses", "mean interval (arb)",
                  "pulse rate (arb)", "gonadotropin bias"], rows)

def universality_table(D):
    rows = [[f(r["frac"], 2), f(r["ratio"], 5), f(r["max_spread_across_gamma"], 1)]
            for r in D["onc"]["universality"]["table"]]
    return table(["h / h<sub>sp</sub>", "&Delta;V / &Delta;V<sub>0</sub>", "max spread across &gamma;"], rows)

def breast_table(D):
    rows = [[r["exposure_years"], f(r["frac"], 3), f(r["RR"], 3)] for r in D["onc"]["breast"]["rows"]]
    return table(["oestrogen-exposure years", "h / h<sub>sp</sub>", "relative risk"], rows)

def prostate_table(D):
    rows = [[f(r["drive_frac"], 1), f(r["barrier_reduction"], 3), f(r["RR"], 3)]
            for r in D["onc"]["prostate"]["rows"]]
    return table(["androgen drive (&times; h<sub>sp</sub>)", "barrier reduction", "relative risk"], rows)

def cervical_table(D):
    rows = [[f(r["joint_frac"], 2), f(r["RR_hpv"], 3), f(r["RR_smoking"], 3),
             f(r["RR_both"], 3), f(r["synergy_index"], 3)] for r in D["onc"]["cervical"]["rows"]]
    return table(["joint exposure", "RR HPV", "RR smoking", "RR both", "synergy index"], rows)

def bat_table(D):
    t = D["thr"]["bat_cycling"]["table"]
    name = {"continuous_high_T": "continuous high (T)", "continuous_low_ADT": "continuous low (ADT)",
            "cycling_BAT": "cycling (BAT)"}
    rows = [[name[k], f(t[k]["sensitive"], 4), f(t[k]["resistant"], 4),
             (f(t[k]["res_over_sens"], 2) if t[k]["res_over_sens"] is not None else "&mdash;")]
            for k in ("continuous_high_T", "continuous_low_ADT", "cycling_BAT")]
    return table(["schedule", "sensitive stress", "resistant stress", "resistant / sensitive"], rows)

def disorder_table(D):
    g2cls = {"V": "g-verified", "L": "g-verified", "O": "g-open", "F": "g-forced"}
    rows = []
    for d in D["dis"]["disorders"]:
        gr = d["grade"]
        tok = "O" if gr.strip().startswith("[O]") else ("L" if gr.strip().startswith("[L]") else
              ("F" if gr.strip().startswith("[F]") else "V"))
        rows.append([d["name"], d["mechanism"], d["better_hypothesis"],
                     '<span class="grade ' + g2cls[tok] + '">' + gr.split(";")[0] + '</span>'])
    return table(["disorder", "substrate failure mode", "model-derived hypothesis", "grade"], rows)

# ---------------------------------------------------------------------------------------------------
# Chapters (English body; answer-first per section; paragraphs <= 3 sentences; numbers live from D)
# ---------------------------------------------------------------------------------------------------
def fertility_chain_table(D):
    rows = [[c["link"], c["operation"], c["kind"]] for c in D["fer"]["F1"]["chain"]]
    return table(["operation", "substrate gate that must fire", "kind"], rows)

def f2_table(D):
    sub = D["fer"]["F2"]["subfertile"]; ster = D["fer"]["F2"]["sterile"]
    rows = [
        ["subfertile (near threshold)", f(sub["deficit"], 3), f(sub["p_per_cycle"], 3),
         f(sub["p_per_cycle_treated"], 3), f(sub["fold_response"], 2) + "&times;",
         f(sub["p_year"], 2) + " &rarr; " + f(sub["p_year_treated"], 2)],
        ["sterile (past spinodal)", f(ster["deficit"], 3), f(ster["p_per_cycle"], 3),
         f(ster["p_per_cycle_treated"], 3), "&mdash;", f(ster["p_year"], 2)],
    ]
    return table(["operation", "deficit", "p/cycle", "p/cycle (nudged)", "response", "p/year (&rarr; nudged)"], rows)

def cohesin_age_table(D):
    f4 = D["fer"]["F4"]
    ages = f4["age_years"]; mis = f4["missegregation_probability"]
    rows = [[str(a), f(m, 3)] for a, m in zip(ages, mis)]
    return table(["maternal age (y)", "modelled mis-segregation P"], rows)

def sexdet_gamma_table(D):
    P = D["sxr"]["S6"]["panel"]
    rows = []
    for s in sorted(P, key=lambda k: P[k]["gamma"]):
        rows.append([s, P[s]["axis"], f(P[s]["gamma"], 4), f(P[s]["gc"], 4)])
    return table(["gene", "axis", "&gamma;", "GC"], rows)

def transmission_table(D):
    s3, s4 = D["sxr"]["S3"], D["sxr"]["S4"]
    rows = [
        ["fair (no drive)", "h = 0", f(s3["transmission_ratio_at_zero_tilt"], 2), "Mendelian 50:50"],
        ["weak drive (sub-spinodal)", "h &lt; h<sub>sp</sub>", f(s3["transmission_ratio_subspinodal"], 2),
         "graded distortion"],
        ["strong drive (supra-spinodal)", "h &gt; h<sub>sp</sub>", f(s3["transmission_ratio_suprapinodal"], 2),
         "loser basin gone &mdash; near fixation"],
        ["X-shredder (sex-chromosome)", "+h<sub>drive</sub>", f(s4["ssr_X_shredder_male"], 2),
         "MALE-biased offspring"],
        ["Y-killer / X-driver", "&minus;h<sub>drive</sub>", f(s4["ssr_Y_killer_female"], 2),
         "FEMALE-biased offspring"],
    ]
    return table(["regime", "tilt", "transmission / sex ratio", "outcome"], rows)


def chapters(D):
    em = D["emerge"]
    g = {o["organ"]: o for o in em["organs"]}
    T1, T2, T3, T4, T5 = D["T1"], D["T2"], D["T3"], D["T4"], D["T5"]
    onc, thr, dis = D["onc"], D["thr"], D["dis"]
    bat = thr["bat_cycling"]
    pc = dis["substrate_checks"]

    CH = []

    # ---- 01 scope + substrate -------------------------------------------------------------------
    CH.append(dict(
        slug="01-scope-and-substrate", no=1,
        subj="Scope and the jammed-vacuum substrate",
        crumb="Scope &amp; substrate",
        h1="Scope and the jammed-vacuum substrate: one drive, two failures, one lever",
        knows=["jamming lattice", "R19 bistable switch", "FitzHugh-Nagumo oscillator",
               "HPG axis", "rectification constant"],
        desc=("The reproductive / gonadal-endocrine axis on a jammed-vacuum substrate: one R19 switch "
              "and one FHN oscillator give one drive, two failure modes, one temporal-pattern lever."),
        answer=("This package derives the human gonadal-endocrine (HPG) axis on a jammed-vacuum substrate, "
                "where a single bistable R19 switch and a single FitzHugh-Nagumo relaxation oscillator generate "
                "every reproductive rhythm. One sex-hormone drive h yields two failure modes &mdash; an oscillator "
                "disease and an oncogenic switch &mdash; governed by one lever: temporal pattern. Brain-facing HPA "
                "stays in the Felt Cognition paper."),
        abstract=("The substrate is the R19 tilted double well V(s) = &minus;&gamma;s&sup2;/2 + s&#8308;/4 &minus; hs, "
                  "whose spinodal h<sub>sp</sub> = 2(&gamma;/3)<sup>3/2</sup> = " + f(T3["spinodal"], 4) +
                  " at &gamma;=1 makes every fate-flip discontinuous. The same kernel, run as an FHN oscillator, "
                  "produces the GnRH pulse, the menstrual cycle, and the spermatogenic cycle by changing only the "
                  "recovery timescale &tau;<sub>s</sub>. No new physics is introduced here; the vendored primitives "
                  "are used unchanged."),
        cards=cards("spinodal", "barrier"),
        page_grade="F",
        body="\n".join([
          "<h2>The substrate is a jammed-vacuum lattice, not a new postulate</h2>",
          "<p>The VP programme treats the vacuum as a jammed granular medium; this package inherits its bistable "
          "switch and oscillator unchanged. A cell or tissue fate is a point in the R19 double-well potential, and "
          "a hormone is a tilt h on that well.</p>",
          eq_fig("rep-sub-001", "R19 tilted double-well potential (the fate landscape)."),
          "<p>The stationary states are the roots of the cubic, so for three real roots there are two minima and a "
          "saddle. As the tilt h grows the metastable minimum and the saddle approach and annihilate at the "
          "spinodal &mdash; beyond it the flip is unavoidable and discontinuous.</p>",
          eq_fig("rep-sub-002", "Force balance; its roots are the basins (outer) and the saddle (middle)."),
          "<h2>Two locked constants set every threshold and barrier</h2>",
          "<p>The spinodal fixes where a switch flips, and the barrier fixes how stable a basin is &mdash; both are "
          "forced functions of the identity constant &gamma; alone. At &gamma;=1 the spinodal is " + f(T3["spinodal"], 4) +
          " and the barrier is " + f(1.0/4, 4) + ".</p>",
          eq_fig("rep-sub-003", "Spinodal: the drive past which the opposite basin disappears."),
          eq_fig("rep-sub-004", "Inter-basin energy barrier (state stability)."),
          "<h2>The unifying thesis: one drive, two failure modes, one lever</h2>",
          "<p>One sex-hormone drive h, moved two opposite ways, produces the whole disease map. Move it the wrong "
          "<em>pattern</em> and the HPG oscillator fails (an endocrine disorder); lower the barrier and the R19 "
          "oncogenic switch crosses (a hormone-driven cancer).</p>",
          "<p>The single control axis the framework exposes is therefore temporal pattern &mdash; pulsatile versus "
          "continuous, cycling versus sustained. This thesis is developed across the discriminant targets "
          "(&sect;3&ndash;&sect;7), oncology (&sect;8), therapy (&sect;9) and the disease map (&sect;10).</p>",
          "<h2>Firewall: this package owns the gonadal axis only</h2>",
          "<p>Decomposition is by physical regime, not textbook organ-system labels: this is the jamming "
          "(hormonal-cycle / germline) class. The brain-facing hypothalamic-pituitary-adrenal (HPA) stress axis and "
          "felt experience belong to the Felt Cognition paper and are cited, never re-derived here.</p>",
          '<p class="note">Sex-hormone <em>levels</em> are this package&rsquo;s single source of truth (SSOT); '
          "sibling packages cite them rather than recomputing them.</p>",
        ]),
    ))

    # ---- 02 organ emergence ---------------------------------------------------------------------
    o_germ, o_test, o_ov, o_tr = g["germline"], g["gonad_testis"], g["gonad_ovary"], g["reproductive_tract"]
    CH.append(dict(
        slug="02-organ-emergence-measured-gamma", no=2,
        subj="Organ emergence from measured master-gene &gamma;",
        crumb="Organ emergence",
        h1="Four reproductive organs emerge from measured master-gene &gamma;",
        knows=["master-gene gamma", "morphogenesis gene-clock", "promoter free energy",
               "germline", "gonad", "developmental order"],
        desc=("Germline, testis, ovary and reproductive tract emerge on the substrate from measured promoter "
              "&gamma; (DAZL, SOX9, FOXL2, WT1); developmental order is argsort(&gamma;)."),
        answer=("Four reproductive organs emerge on the substrate from measured master-gene &gamma;: germline "
                "(DAZL " + f(o_germ["gamma"], 4) + "), testis (SOX9 " + f(o_test["gamma"], 4) + "), ovary "
                "(FOXL2 " + f(o_ov["gamma"], 4) + ") and reproductive tract (WT1 " + f(o_tr["gamma"], 4) + "). "
                "Developmental order is argsort(&gamma;) &mdash; germline &rarr; testis &rarr; ovary &rarr; tract "
                "&mdash; a sim-verified readout over measured, never-fitted constants."),
        abstract=("Each &gamma; is minus the mean nearest-neighbour stacking free energy (SantaLucia 1998) over the "
                  "proximal promoter (TSS&minus;2000..+500, GRCh38) &mdash; the identical pipeline the DNA atlas uses. "
                  "The values reproduce offline bit-for-bit from cached promoters and are validated by recovering the "
                  "vendored SOX9 anchor (&gamma;=" + f(o_test["gamma"], 4) + ", GC=0.545). Developmental order is a "
                  "&gamma;-readout over measured organs [V]; germline-first matches PGC specification preceding gonadal "
                  "differentiation."),
        cards=cards("gamma", "dwell"),
        page_grade="V",
        body="\n".join([
          "<h2>&gamma; is measured from the promoter, never fitted</h2>",
          "<p>The identity constant of each organ is read directly from its master gene&rsquo;s promoter sequence. "
          "The method is the same nearest-neighbour stacking calculation the DNA morphogenesis atlas uses, so the "
          "reproductive masters are <em>received</em>, not invented.</p>",
          eq_fig("rep-gam-001", "Identity constant from promoter nearest-neighbour stacking free energy."),
          "<p>The three formerly to-measure masters (FOXL2, DAZL, WT1) were measured through this pipeline and "
          "cached, so the values reproduce offline bit-for-bit without the network. The pipeline is accepted only "
          "because it recovers the vendored SOX9 anchor to four decimals (&gamma;=" + f(o_test["gamma"], 4) +
          ", GC=0.545).</p>",
          "<h2>The four organs and their forced quantities</h2>",
          "<p>Each measured &gamma; fixes a functional spinodal (presence threshold) and a relative dwell size; "
          "only the relative ordering of size is forced, the absolute scale is open.</p>",
          gamma_table(D),
          eq_fig("rep-dwl-001", "Dwell sets relative organ size; order [F], absolute magnitude [O]."),
          "<h2>Developmental order is a &gamma;-readout</h2>",
          "<p>Sorting the four organs by ascending &gamma; gives the emergence order germline &rarr; testis &rarr; "
          "ovary &rarr; tract. This is a derived ordering over measured constants, not a fitted timeline; "
          "germline-first is consistent with primordial-germ-cell specification preceding gonadal differentiation "
          "(a sign sanity-check).</p>",
          '<p class="note">The shared FHN oscillator runs at &gamma;=1 because rhythm depends on the recovery '
          "timescale &tau;<sub>s</sub>, not on the identity &gamma;; the measured &gamma; values drive emergence and "
          "ordering, while the dynamics chapters (&sect;3&ndash;&sect;7) vary only &tau;<sub>s</sub>.</p>",
        ]),
    ))

    # ---- 03 T1 GnRH pulse generator -------------------------------------------------------------
    fr = T1["frequency_decoding"]["rows"]
    fast, slow = fr[0], fr[-1]
    CH.append(dict(
        slug="03-gnrh-pulse-generator", no=3,
        subj="GnRH pulse generator (T1)",
        crumb="GnRH pulse generator",
        h1="The GnRH pulse generator is the shared FHN relaxation oscillator (T1)",
        knows=["GnRH pulse generator", "KNDy network", "LH FSH frequency decoding",
               "relaxation oscillator", "gonadotropin"],
        desc=("T1: the hypothalamic GnRH pulse generator as the shared FHN relaxation oscillator; pulse frequency "
              "decodes to LH/FSH balance as a monotone function of the recovery timescale."),
        answer=("The hypothalamic GnRH pulse generator is the shared FitzHugh-Nagumo relaxation oscillator: a fast "
                "switch with slow recovery emits a relaxation pulse train (" + str(T1["pulses"]) + " pulses at "
                "&tau;<sub>s</sub>=60). Pulse <em>frequency</em> decodes to gonadotropin identity &mdash; fast pulses "
                "favour LH, slow favour FSH &mdash; reproduced as a monotone function of the recovery timescale "
                "&tau;<sub>s</sub>. The mechanism is sim-verified; the absolute pulse rate is a measured anchor."),
        abstract=("Run as the vendored FHN at &tau;<sub>s</sub>=60 the generator emits " + str(T1["pulses"]) +
                  " pulses with mean interval " + f(T1["mean_interval_arb"], 1) + " (arb). Sweeping &tau;<sub>s</sub> "
                  "from " + f(fast["tau_s"], 0) + " to " + f(slow["tau_s"], 0) + " drops the pulse rate "
                  "monotonically from " + f(fast["pulse_rate_arb"], 6) + " to " + f(slow["pulse_rate_arb"], 6) +
                  ", so frequency maps onto the LH/FSH balance &mdash; the substrate basis of GnRH frequency coding."),
        cards=cards("spinodal"),
        page_grade="V",
        body="\n".join([
          "<h2>The generator is a relaxation pulse train, not a sinusoid</h2>",
          "<p>The arcuate KNDy network that paces GnRH release is, on this substrate, the same fast-slow FHN system "
          "used everywhere in the package. A fast R19 switch with slow recovery fires a sharp pulse, recovers, and "
          "fires again &mdash; a relaxation pulse train rather than a smooth wave.</p>",
          "<p>At the follicular setting (&tau;<sub>s</sub>=60) the generator emits " + str(T1["pulses"]) +
          " pulses over the run with mean inter-pulse interval " + f(T1["mean_interval_arb"], 1) + " (arb). Each "
          "GnRH pulse drives one downstream gonadotrope pulse (LH/FSH).</p>",
          "<h2>Pulse frequency decodes to LH versus FSH</h2>",
          "<p>The clinically central fact &mdash; that pulse <em>frequency</em>, not amplitude, sets the LH:FSH "
          "balance &mdash; falls out of the recovery timescale. A faster generator (smaller &tau;<sub>s</sub>) fires "
          "more often and favours LH; a slower generator favours FSH, and the pulse rate is monotone in "
          "&tau;<sub>s</sub>.</p>",
          freq_table(D),
          '<p class="note">The pulse RATE is calibrated to the measured follicular figure of roughly one GnRH/LH '
          "pulse per 60&ndash;90 min [L]; the package does not claim to derive that clinical number. Only the "
          "monotone frequency-decoding <em>mechanism</em> is the sim-verified [V] claim.</p>",
        ]),
    ))

    # ---- 04 T2 menstrual cycle ------------------------------------------------------------------
    CH.append(dict(
        slug="04-menstrual-cycle-relaxation-oscillator", no=4,
        subj="Menstrual cycle as a relaxation oscillator (T2)",
        crumb="Menstrual cycle",
        h1="The menstrual cycle is the slowest relaxation oscillator (T2)",
        knows=["menstrual cycle", "follicular phase", "luteal phase", "relaxation oscillator",
               "rise fall asymmetry"],
        desc=("T2: the menstrual cycle as the slowest relaxation oscillator in the package; the rise/fall timing "
              "asymmetry is far from 1.0, confirming relaxation (not sinusoidal) dynamics."),
        answer=("The menstrual cycle is the slowest relaxation oscillator in the package: a long follicular charge "
                "and a fast ovulatory discharge, not a sinusoid. The rise/fall timing asymmetry is " +
                f(T2["asymmetry_ratio"], 1) + " (a pure sinusoid is exactly 1.0), confirming relaxation dynamics. The "
                "~28-day period is a measured anchor set by the recovery timescale &tau;<sub>s</sub>, not derived "
                "from the substrate."),
        abstract=("Over the run the slow FHN completes " + str(T2["cycles"]) + " cycles with period " +
                  f(T2["period_arb"], 1) + " (arb). The waveform is strongly asymmetric &mdash; a short upstroke (" +
                  f(T2["rise_arb"], 2) + ") and a long recovery (" + f(T2["fall_arb"], 1) + "), giving an asymmetry "
                  "ratio of " + f(T2["asymmetry_ratio"], 1) + ". A sinusoid would give exactly 1.0, so the shape is "
                  "unambiguously that of a relaxation oscillator."),
        cards="",
        page_grade="V",
        body="\n".join([
          "<h2>A long charge and a fast discharge</h2>",
          "<p>The menstrual cycle is a slow oestradiol rise as the dominant follicle grows, then a fast ovulatory "
          "excursion (the LH surge), then a luteal plateau and reset. On the substrate this is the same FHN run at "
          "the longest recovery timescale, &tau;<sub>s</sub>=600.</p>",
          "<h2>The shape discriminant: rise/fall asymmetry</h2>",
          "<p>A relaxation oscillator is time-asymmetric (slow rise, fast excursion); a sinusoid is time-symmetric. "
          "Measuring the upstroke-to-recovery timing ratio over one period gives " + f(T2["asymmetry_ratio"], 1) +
          ", which a pure sinusoid would render as exactly 1.0.</p>",
          "<p>The fraction of time spent &ldquo;high&rdquo; is deliberately not used as the discriminant, because a "
          "slow decay sits high for most of a period yet is still relaxation. The timing asymmetry is the clean, "
          "boundary-insensitive test, and the realised value sits far above any reasonable threshold.</p>",
          '<p class="note">The ~28-day period is a measured [L] anchor inherited from the recovery timescale; the '
          "relaxation <em>character</em> is the sim-verified [V] claim. The period magnitude is not derived.</p>",
        ]),
    ))

    # ---- 05 T3 oestrogen feedback switch --------------------------------------------------------
    CH.append(dict(
        slug="05-oestrogen-feedback-switch", no=5,
        subj="Oestrogen feedback switch &amp; LH surge (T3)",
        crumb="Feedback switch",
        h1="Oestrogen feedback is a bistable switch with hysteresis (T3)",
        knows=["oestrogen feedback", "LH surge", "positive feedback", "bistable switch",
               "hysteresis", "ovulation"],
        desc=("T3: oestrogen feedback as a bistable R19 switch &mdash; negative feedback flips discontinuously to "
              "the positive-feedback LH surge at the spinodal, with hysteresis."),
        answer=("Oestrogen feedback is a bistable R19 switch. Below threshold the axis sits in negative feedback "
                "(low LH); sustained high oestradiol crosses the spinodal and flips discontinuously to positive "
                "feedback &mdash; the mid-cycle LH surge (up-jump " + f(T3["up_jump_size"], 3) + "). The switch shows "
                "hysteresis (width " + f(T3["hysteresis_width"], 3) + "): the up-threshold to trigger the surge "
                "exceeds the down-threshold to return. It is the same R19 primitive as malignant transformation."),
        abstract=("Sweeping the oestradiol-analogue drive up then down, the settled axis state jumps discontinuously "
                  "by " + f(T3["up_jump_size"], 3) + " at the surge threshold (" + f(T3["surge_up_threshold"], 4) +
                  "), near the spinodal " + f(T3["spinodal"], 4) + ". The up- and down-thresholds differ by " +
                  f(T3["hysteresis_width"], 3) + " (hysteresis), the signature of a true bistable switch rather than "
                  "a graded response."),
        cards=cards("spinodal", "barrier"),
        page_grade="V",
        body="\n".join([
          "<h2>Negative feedback flips to positive at a threshold</h2>",
          "<p>For most of the cycle rising oestradiol suppresses LH (negative feedback). Once oestradiol is high "
          "enough for long enough the axis crosses the spinodal and the sign of feedback flips: the mid-cycle LH "
          "surge is the system snapping into the positive-feedback basin.</p>",
          "<p>The flip is discontinuous, jumping by " + f(T3["up_jump_size"], 3) + " in settled state at the surge "
          "threshold " + f(T3["surge_up_threshold"], 4) + " &mdash; right at the geometric spinodal " +
          f(T3["spinodal"], 4) + ". A graded (sinusoidal-feedback) model has no such jump.</p>",
          "<h2>Hysteresis confirms bistability</h2>",
          "<p>Sweeping the drive back down, the axis returns at a <em>lower</em> threshold than it left, so the "
          "up- and down-thresholds differ by " + f(T3["hysteresis_width"], 3) + ". This hysteresis loop is the "
          "defining fingerprint of a bistable switch and rules out a single-valued response curve.</p>",
          '<p class="note">This is the <em>same</em> R19 bistable primitive the oncology chapter (&sect;8) uses for '
          "malignant transformation: the surge and a cancerous fate-flip are one mechanism, read in two tissues. "
          "The switch mechanism is sim-verified [V].</p>",
        ]),
    ))

    # ---- 06 T4 spermatogenic cycle --------------------------------------------------------------
    po = T4["period_ordering"]
    CH.append(dict(
        slug="06-spermatogenic-cycle", no=6,
        subj="Spermatogenic cycle (T4)",
        crumb="Spermatogenic cycle",
        h1="The spermatogenic cycle is a third, intermediate relaxation clock (T4)",
        knows=["seminiferous epithelium", "spermatogenic cycle", "relaxation oscillator",
               "period ordering", "recovery timescale"],
        desc=("T4: the seminiferous (spermatogenic) cycle as a third relaxation clock from the same substrate, "
              "intermediate between the GnRH pulse and the menstrual cycle; the three periods order correctly."),
        answer=("The seminiferous (spermatogenic) cycle is a third relaxation oscillator from the same substrate, "
                "intermediate between the minute-scale GnRH pulse and the ~28-day menstrual cycle. At "
                "&tau;<sub>s</sub>=" + f(T4["tau_s"], 0) + " (the measured 16:28-day ratio) the three clocks come out "
                "in the correct order: pulse " + f(po["pulse_arb"], 1) + " &lt; spermatogenic " +
                f(po["spermatogenic_arb"], 1) + " &lt; menstrual " + f(po["menstrual_arb"], 1) + ". The ~16-day "
                "period is a measured anchor; the ordering is the sim-verified claim."),
        abstract=("Changing only the recovery timescale to &tau;<sub>s</sub>=" + f(T4["tau_s"], 0) + " &mdash; set "
                  "from the clinical 16:28-day ratio applied to the menstrual &tau;<sub>s</sub>, not tuned &mdash; "
                  "yields a relaxation oscillator with period " + f(T4["period_arb"], 1) + " (arb). The three "
                  "reproductive clocks then satisfy pulse &lt; spermatogenic &lt; menstrual from one kernel, with no "
                  "parameter chosen to hit a target."),
        cards="",
        page_grade="V",
        body="\n".join([
          "<h2>One kernel, a third timescale</h2>",
          "<p>The human seminiferous epithelial cycle is about 16 days &mdash; between the minute-scale GnRH pulse "
          "and the 28-day menstrual cycle. The structural claim is that the same R19/FHN substrate gives a third "
          "relaxation oscillator by changing only the slow recovery timescale &tau;<sub>s</sub>; nothing else in the "
          "kernel changes.</p>",
          "<p>&tau;<sub>s</sub> is fixed at " + f(T4["tau_s"], 0) + " from the measured period ratio 16:28 applied to "
          "the menstrual timescale the previous chapter locked. That makes the <em>period</em> a measured anchor "
          "[L]; no parameter is fitted to an output.</p>",
          "<h2>The three clocks order correctly</h2>",
          "<p>Read off the same substrate at the three locked recovery timescales, the periods come out in the "
          "right order &mdash; the package&rsquo;s [V] claim is the ordering, not the magnitudes.</p>",
          table(["clock", "recovery &tau;<sub>s</sub>", "period (arb)", "clinical anchor"],
                [["GnRH pulse (T1)", "60", f(po["pulse_arb"], 1), "~1 / 90 min [L]"],
                 ["spermatogenic (T4)", f(T4["tau_s"], 0), f(po["spermatogenic_arb"], 1), "~16 d [L]"],
                 ["menstrual (T2)", "600", f(po["menstrual_arb"], 1), "~28 d [L]"]]),
          '<p class="note">pulse &lt; spermatogenic &lt; menstrual holds exactly, so the substrate reproduces the '
          "qualitative timescale separation of the three reproductive clocks from a single mechanism.</p>",
        ]),
    ))

    # ---- 07 T5 puberty --------------------------------------------------------------------------
    CH.append(dict(
        slug="07-puberty-spinodal-crossing", no=7,
        subj="Puberty onset as a spinodal crossing (T5)",
        crumb="Puberty onset",
        h1="Puberty onset is a discontinuous spinodal crossing (T5)",
        knows=["puberty", "juvenile pause", "spinodal crossing", "gonadotropin reactivation",
               "discontinuous onset"],
        desc=("T5: puberty as a discontinuous spinodal crossing &mdash; the juvenile-paused GnRH oscillator switches "
              "ON in a single step as a slow maturation drive passes the spinodal."),
        answer=("Puberty onset is a discontinuous spinodal crossing, not a gradual ramp. As a slow maturation drive "
                "rises past the spinodal (h=" + f(T5["jump_drive"], 3) + " &approx; " + f(T5["jump_over_spinodal"], 2) +
                "&times; h<sub>sp</sub>) the pulse-enable gate jumps from OFF (state " + f(T5["state_before"], 3) +
                ") to ON (" + f(T5["state_after"], 3) + ") in a single step (jump size " + f(T5["jump_size"], 3) +
                "). The mechanism and order are sim-verified; chronological age is open."),
        abstract=("The juvenile pause is the GnRH oscillator held in the R19 OFF basin. Ramping a maturation drive "
                  "from zero, the pulse-enable gate stays off until the spinodal " + f(T5["spinodal"], 4) +
                  ", then jumps by " + f(T5["jump_size"], 3) + " (state " + f(T5["state_before"], 3) + " &rarr; " +
                  f(T5["state_after"], 3) + ") localised at " + f(T5["jump_over_spinodal"], 2) + "&times; the "
                  "spinodal. Onset is therefore a threshold crossing, not a smooth rise."),
        cards=cards("spinodal"),
        page_grade="V",
        body="\n".join([
          "<h2>The juvenile pause is an OFF basin</h2>",
          "<p>Before puberty the GnRH oscillator is not weak &mdash; it is held in the R19 OFF basin, silenced. "
          "Puberty is the same switch crossing its spinodal as a slow maturational drive rises, so the question is "
          "whether onset is gradual or discontinuous.</p>",
          "<h2>Onset is a single discontinuous jump</h2>",
          "<p>Ramping the drive slowly from zero, the pulse-enable state stays in the OFF basin (negative) until the "
          "drive reaches the spinodal, then jumps to the ON basin (positive) in one step. The jump of " +
          f(T5["jump_size"], 3) + " takes the state from " + f(T5["state_before"], 3) + " to " +
          f(T5["state_after"], 3) + ", localised at " + f(T5["jump_over_spinodal"], 2) + "&times; the spinodal "
          + f(T5["spinodal"], 4) + ".</p>",
          "<p>This is the discriminant: a gradual-maturation model predicts a smooth amplitude ramp, whereas the "
          "substrate predicts a threshold crossing. The same threshold, crossed early or not yet, gives central "
          "precocious puberty and delayed puberty respectively (&sect;10).</p>",
          '<p class="disclaimer">The model fixes the discontinuous <em>order</em> (OFF below &rarr; ON above) and '
          "the jump/spinodal ratio [V]; mapping the crossing to a calendar age needs external endocrine calibration "
          "and is left open [O].</p>",
        ]),
    ))

    # ---- 08 oncology ----------------------------------------------------------------------------
    ut = onc["universality"]["table"]
    br = onc["breast"]["rows"]; pr = onc["prostate"]["rows"]; cv = onc["cervical"]["rows"]
    CH.append(dict(
        slug="08-hormone-cancer-dose-response", no=8,
        subj="Hormone-driven cancer dose-response",
        crumb="Hormone-cancer dose-response",
        h1="Hormone-driven cancer is Kramers escape over a lowered R19 barrier",
        knows=["carcinogen dose-response", "Kramers escape", "relative risk", "oestrogen breast cancer",
               "androgen prostate", "HPV smoking synergy"],
        desc=("Hormone-driven cancer as Kramers escape over an R19 barrier a sustained hormone drive lowers; the "
              "dose-response shape is universal in &gamma; (max spread 0.0). Breast, prostate, cervical shapes."),
        answer=("Hormone-driven cancer is Kramers escape over an R19 barrier that a sustained hormone drive lowers. "
                "The dimensionless dose-response shape &Delta;V/&Delta;V<sub>0</sub> versus h/h<sub>sp</sub> is "
                "identical for every &gamma; (max spread " + f(ut[1]["max_spread_across_gamma"], 1) + ") &mdash; "
                "universal: the tissue master gene sets only the barrier scale, never the shape. Site shapes are "
                "sim-verified; epidemiological anchors are measured; absolute incidence is open."),
        abstract=("A carcinogen is a sustained aberrant drive that lowers the escape barrier out of the healthy well; "
                  "transformation is Kramers escape over it, with relative risk RR = rate(dose)/rate(0). The barrier "
                  "ratio &Delta;V(&gamma;,h)/&Delta;V<sub>0</sub> as a function of h/h<sub>sp</sub> is identical "
                  "across &gamma; (max spread " + f(ut[1]["max_spread_across_gamma"], 1) + ") &mdash; the dose-response "
                  "<em>shape</em> is universal [F], so &gamma; sets only the absolute barrier scale."),
        cards=cards("spinodal", "barrier"),
        page_grade="F",
        body="\n".join([
          "<h2>The cancer kernel is the same R19 switch</h2>",
          "<p>A cell fate is the R19 double well; a carcinogen is a sustained drive that lowers the barrier out of "
          "the healthy (metastable) well, and malignant transformation is the thermally-activated escape over it. "
          "The exact escape barrier is the saddle-minus-metastable energy of the tilted well.</p>",
          eq_fig("rep-onc-001", "Exact escape barrier out of the metastable (healthy) minimum."),
          eq_fig("rep-onc-002", "Kramers relative risk versus the unexposed baseline (lattice noise D)."),
          "<h2>The dose-response shape is universal in &gamma;</h2>",
          "<p>The dimensionless barrier ratio as a function of drive-over-spinodal is <em>identical</em> for every "
          "tissue &gamma; &mdash; the master gene sets the absolute barrier height but never the shape of the hormone "
          "dose-response. This is a forced result with no free parameters.</p>",
          universality_table(D),
          "<h2>Three sites, three falsifiable shapes</h2>",
          "<h3>Breast &mdash; cumulative oestrogen, monotone</h3>",
          "<p>Cumulative oestrogen exposure is sustained drive, so relative risk rises monotonically with exposure "
          "years until the barrier floor is reached. The WHI combined-MHT figure (RR &asymp; 1.26) is the measured "
          "anchor for the exposure-to-drive scale; risk rises from 1.0 to about " + f(br[3]["RR"], 1) +
          " across the modelled range.</p>",
          breast_table(D),
          "<h3>Prostate &mdash; androgen, concave and saturating</h3>",
          "<p>Androgen drive lowers the barrier with diminishing returns, and once the drive reaches the spinodal "
          "the barrier floor is zero, so risk <em>plateaus</em>. Past the fold (drive &ge; 1.0&times; h<sub>sp</sub>) "
          "the relative risk holds flat at " + f(pr[-1]["RR"], 1) + " &mdash; the saturation model (more testosterone "
          "is not more risk above threshold).</p>",
          prostate_table(D),
          "<h3>Cervical &mdash; HPV&times;smoking, saturating synergy</h3>",
          "<p>HPV lowers the barrier height (softens the well) while smoking adds mutagenic drive. Their synergy "
          "index is near 1.0 (multiplicative) at low joint exposure and falls to " + f(cv[-1]["synergy_index"], 3) +
          " (sub-multiplicative) at high exposure, because the barrier floor is zero &mdash; a falsifiable "
          "prediction that synergies saturate.</p>",
          cervical_table(D),
          '<p class="disclaimer">Grades (C3): the shape and universality are forced/sim-verified [F]/[V]; the '
          "epidemiological anchors are measured [L]; absolute population incidence is open [O]. The single lattice "
          "noise D=" + f(onc["noise_D"], 2) + " sets absolute rates only &mdash; every RR <em>ratio</em>, slope sign, "
          "plateau and synergy statement is invariant to it. This is not clinical advice.</p>",
        ]),
    ))

    # ---- 09 therapy -----------------------------------------------------------------------------
    t = bat["table"]
    CH.append(dict(
        slug="09-temporal-pattern-therapy", no=9,
        subj="Temporal pattern as a therapeutic lever",
        crumb="Temporal-pattern therapy",
        h1="Temporal pattern is a control axis separate from hormone level",
        knows=["pulsatile GnRH", "depot GnRH agonist", "bipolar androgen therapy", "LTED breast",
               "desensitisation", "endocrine therapy resistance"],
        desc=("The temporal pattern of a hormone drive &mdash; pulsatile vs continuous, cycling vs sustained &mdash; "
              "is a control axis separate from level; it retrodicts pulsatile-GnRH, depot agonists and BAT."),
        answer=("The temporal pattern of a hormone drive is a control axis separate from its level. The same GnRH "
                "molecule activates when pulsatile (" + str(thr["gnrh_pattern"]["pulsatile_output_pulses"]) +
                " output pulses) but suppresses when continuous (" + str(thr["gnrh_pattern"]["continuous_output_pulses"]) +
                " pulses, depolarisation block). Cycling the drive (BAT) delivers a resistant clone " +
                f(bat["cycling_over_continuous_high_resistant_fold"], 1) + "&times; its own continuous-high stress, "
                "selectively stressing the adapted clone. Principle sim-verified; clinical schedule open."),
        abstract=("Because the substrate is an oscillator on a bistable switch, the <em>pattern</em> of the drive is "
                  "a separate lever from its level. Pulsatile GnRH keeps the gonadotrope firing (" +
                  str(thr["gnrh_pattern"]["pulsatile_output_pulses"]) + " pulses) while the same agent held "
                  "continuously blocks it (" + str(thr["gnrh_pattern"]["continuous_output_pulses"]) + "); and cycling "
                  "whipsaws a resistant clone " + f(bat["cycling_over_continuous_high_resistant_fold"], 1) +
                  "&times; harder than any constant drive."),
        cards=cards("spinodal"),
        page_grade="V",
        body="\n".join([
          "<h2>Same molecule, opposite effect</h2>",
          "<p>Pulsatile GnRH re-ignites the downstream oscillator on every pulse, so the axis is activated; the same "
          "agent held continuously pins the drive past the fold, so the oscillator can no longer cycle and the axis "
          "is suppressed by desensitisation. The substrate reproduces both signs from one molecule.</p>",
          "<p>Delivered as brief supra-threshold pulses the gonadotrope fires " +
          str(thr["gnrh_pattern"]["pulsatile_output_pulses"]) + " times; held continuously above the "
          "depolarisation-block threshold it fires " + str(thr["gnrh_pattern"]["continuous_output_pulses"]) +
          " times. This retrodicts the pulsatile-GnRH pump (activation) and depot GnRH agonists for precocious "
          "puberty, endometriosis and prostate cancer (suppression).</p>",
          "<h2>Cycling defeats adaptation</h2>",
          "<p>Endocrine-therapy resistance is modelled as amplified drive-coupling &kappa; (receptor "
          "over-expression), not a deeper well. A resistant clone tolerates any <em>constant</em> drive by "
          "re-settling, but cycling the drive across the fold faster than it can settle inflicts a large transition "
          "stress it cannot escape.</p>",
          "<p>Selectivity is measured as the integrated transition stress (mean |ds/dt|) over each schedule, with no "
          "arbitrary kill threshold. Cycling delivers the resistant clone " + f(t["cycling_BAT"]["resistant"], 3) +
          " versus " + f(t["continuous_high_T"]["resistant"], 4) + " under continuous high &mdash; a " +
          f(bat["cycling_over_continuous_high_resistant_fold"], 1) + "&times; amplification, and it stresses the "
          "resistant clone more than the sensitive one.</p>",
          bat_table(D),
          '<p class="disclaimer">This retrodicts Bipolar Androgen Therapy in castration-resistant prostate cancer '
          "and oestrogen-induced apoptosis in long-term-oestrogen-deprived breast cancer. The qualitative principle "
          "is sim-verified [V]; the clinical translation (periods, doses, schedules) is open [O] and needs trials. "
          "Not clinical advice.</p>",
        ]),
    ))

    # ---- 10 disease -----------------------------------------------------------------------------
    CH.append(dict(
        slug="10-hpg-disease-mechanisms", no=10,
        subj="HPG disease mechanisms &amp; hypotheses",
        crumb="Disease mechanisms",
        h1="Eight HPG disorders on one substrate: one drive, two failures, one lever",
        knows=["PCOS", "hypothalamic amenorrhoea", "menopause", "precocious puberty",
               "anovulatory infertility", "endometriosis", "male hypogonadism"],
        desc=("Eight common HPG disorders mapped to one substrate; PCOS and hypothalamic amenorrhoea are opposite "
              "ends of one pulse-frequency axis; menopause is irreversible latch loss. Retrodictions and hypotheses."),
        answer=("Eight common HPG disorders map to one substrate: one drive, two failure modes, one lever. PCOS "
                "(fast pulse, LH-biased rate " + f(pc["pcos"]["fast_tau_rate"], 4) + ") and functional hypothalamic "
                "amenorrhoea (slow, " + f(pc["fha"]["fha_slow_rate"], 4) + ") are opposite ends of one "
                "pulse-frequency axis. Menopause is irreversible loss of the bistable secretory latch (ON " +
                f(pc["menopause"]["intact_latched_on"], 1) + " &rarr; " + f(pc["menopause"]["depleted_state"], 3) +
                "). Retrodictions sim-verified; novel hypotheses open &mdash; not clinical advice."),
        abstract=("Each disorder is mapped to the substrate failure the dynamics chapters verified, with its current "
                  "treatment read as a substrate move and a falsifiable better-treatment hypothesis. PCOS (pulse "
                  "rate " + f(pc["pcos"]["fast_tau_rate"], 4) + ") and FHA (" + f(pc["fha"]["fha_slow_rate"], 4) +
                  ") sit at opposite ends of one pulse-frequency axis; menopause is latch collapse on follicular "
                  "depletion (" + f(pc["menopause"]["intact_latched_on"], 1) + " &rarr; " +
                  f(pc["menopause"]["depleted_state"], 3) + "), irreversible."),
        cards="",
        page_grade="V",
        body="\n".join([
          "<h2>The split is by mechanism, not body part</h2>",
          "<p>This package owns the common, dynamics-defined disorders of the HPG axis; rare monogenic subtypes "
          "cross-reference to the disease whitepaper. Every disorder is one of two failure modes of the same drive "
          "&mdash; a broken oscillator or a crossed oncogenic switch &mdash; resolved by the temporal-pattern "
          "lever.</p>",
          "<h2>PCOS and FHA: opposite ends of one axis</h2>",
          "<p>PCOS is the GnRH generator stuck too fast, biasing LH over FSH so follicles are recruited but none is "
          "selected; the substrate confirms a faster generator gives a higher pulse rate (" +
          f(pc["pcos"]["fast_tau_rate"], 4) + " versus " + f(pc["pcos"]["slow_tau_rate"], 5) + "). Functional "
          "hypothalamic amenorrhoea is the same generator slowed below the ovulatory rate (" +
          f(pc["fha"]["fha_slow_rate"], 4) + " versus normal " + f(pc["fha"]["normal_rate"], 4) + ") &mdash; the two "
          "diseases are opposite ends of one pulse-frequency axis.</p>",
          "<h2>Menopause is irreversible latch loss</h2>",
          "<p>The sustained secretory (ON) state is a property of the bistable R19 well: an intact ovary latches ON "
          "and holds it at zero drive (" + f(pc["menopause"]["intact_latched_on"], 1) + "), but a depleted follicle "
          "pool removes the well so the latch collapses (" + f(pc["menopause"]["depleted_state"], 3) + "). The model "
          "is explicit that HRT is replacement, not restoration &mdash; the secretory hardware is gone.</p>",
          "<h2>The full map</h2>",
          "<p>Existing practices the framework retrodicts are flagged as validation; genuinely novel suggestions are "
          "graded open and need clinical validation.</p>",
          disorder_table(D),
          "<h2>The unifying thesis</h2>",
          "<p>One drive h, moved two opposite ways. Lower the barrier and the R19 oncogenic switch crosses (every "
          "HRT/TRT carries a cancer-risk signature); supply the wrong pattern and an HPG oscillator disease appears "
          "(every anti-hormone cancer therapy carries hypogonadal effects).</p>",
          "<p>The single control axis the framework exposes is temporal pattern, which retrodicts pulsatile-GnRH, "
          "GnRH-agonist desensitisation, the hCG trigger as a spinodal kick, Bipolar Androgen Therapy, the LTED "
          "pulse, the saturation model, and HPV&times;smoking multiplicativity.</p>",
          '<p class="disclaimer">Mechanisms are sim-verified [V]; retrodictions [V]/[L]; genuinely novel hypotheses '
          "(low-frequency pulsatile restoration in PCOS; pulsed/cycled TRT) are graded [O] and explicitly require "
          "clinical validation. None of this is clinical advice.</p>",
        ]),
    ))

    # ---- 11 the gamete itself (germline) --------------------------------------------------------
    G1, G2, G3, G4, G5, G6 = (D["germ"]["G1"], D["germ"]["G2"], D["germ"]["G3"],
                              D["germ"]["G4"], D["germ"]["G5"], D["germ"]["G6"])
    atlas = D["germ_atlas"]
    atlas_asc = sorted(atlas.items(), key=lambda kv: kv[1])
    cm = G2["crossover_model"]; hyp = G3["hyperactivation"]; lad = G3["four_clock_ladder"]
    pre = G5["preregistered_test"]; core = G5["recombination_core_cluster"]; ms = G5["module_stats"]
    prov = G6["provisioning"]; dsym = G6["division_symmetry"]
    ploidy_rows = [["start (diploid)", G1["ploidy_trajectory"]["start"]],
                   ["after S-phase (replicate)", G1["ploidy_trajectory"]["after_S"]],
                   ["after meiosis I (reductional)", G1["ploidy_trajectory"]["after_MI"]],
                   ["after meiosis II (equational)", G1["ploidy_trajectory"]["after_MII"]]]
    module_rows = [[m, ms[m]["n"], f(ms[m]["mean"], 4), f(ms[m]["sd"], 4),
                    f(ms[m]["lo"], 4) + "&ndash;" + f(ms[m]["hi"], 4)]
                   for m in ("germline", "meiosis", "sperm", "oocyte")]
    atlas_line = ", ".join(s + " " + f(gv, 4) for s, gv in atlas_asc)
    CH.append(dict(
        slug="11-gametogenesis-the-gamete-itself", no=11,
        subj="The gamete itself: meiosis, motility and the egg",
        crumb="The gamete",
        h1="The gamete, emerged from DNA: one substrate makes an oscillator and a held switch",
        knows=["meiosis", "independent assortment", "crossover interference", "sperm flagellum",
               "CatSper hyperactivation", "metaphase-II arrest", "fertilisation", "anisogamy",
               "polar body", "REC8 cohesin"],
        desc=("The germ cell on the same substrate: meiosis as one replication and two ordered divisions, "
              "non-identical gametes from assortment and interference-spaced recombination, the sperm "
              "flagellum as the fast relaxation oscillator and the egg as a held switch."),
        answer=("The four questions about the germ cell answer on the same substrate. A gamete is made by "
                "meiosis &mdash; one DNA replication then two divisions, reductional before equational, "
                "forced by ordered two-stage REC8 cohesin release (arm separase " +
                f(G1["separase_at_arm_release"], 3) + " &rarr; centromeric " +
                f(G1["separase_at_centromeric_release"], 3) + "). Gametes are NOT identical: independent "
                "assortment is exactly 2<sup>23</sup> = " + format(G2["independent_assortment_combinations"], ",") +
                ", and crossover interference is the substrate refractory period mapped onto the chromosome "
                "(sub-Poisson, Fano " + f(cm["fano_factor"], 3) + " versus Poisson " + f(cm["null_poisson_fano"], 3) +
                "). The sperm flagellum is the fast end of the oscillator ladder; the egg is a switch held at "
                "metaphase II, and fertilisation is a one-way spinodal flip. One substrate, two opposite "
                "gametes &mdash; anisogamy. <b>[V]</b> with measured-&gamma; and structural anchors."),
        abstract=("Each germ-cell question is a discriminant against the vendored R19 switch and FHN oscillator, "
                  "with measured gamete-program promoter &gamma; (TEKT1&hellip;REC8) as the only new input. Meiosis "
                  "is ploidy 2N,2C&rarr;1N,1C with the reductional&ndash;equational order set by shugoshin-protected "
                  "cohesin (a protection sign, not a tuned parameter); non-identity is 2<sup>23</sup> assortment "
                  "times interference-thinned recombination; the flagellar beat is the fastest relaxation clock "
                  "(" + f(lad["flagellum_arb"], 1) + " &lt; " + f(lad["pulse_arb"], 1) + " &lt; " +
                  f(lad["spermatogenic_arb"], 1) + " &lt; " + f(lad["menstrual_arb"], 1) + "); the egg is a held "
                  "switch whose fertilisation flip is supra-spinodal and irreversible. A pre-registered test of "
                  "whether &gamma; separates the functional modules is reported as it falls, including its null."),
        cards=cards("gamma", "spinodal"),
        page_grade="V",
        body="\n".join([
          "<h2>The package emerged the organs and the rhythms, but never the germ cell</h2>",
          "<p>Earlier chapters derived the reproductive organs from measured &gamma; and the HPG, menstrual and "
          "spermatogenic rhythms from one oscillator. None of them opened the gamete itself. This chapter asks the "
          "four questions directly &mdash; how a gamete is made, whether gametes are identical, how the sperm moves "
          "and how the egg works &mdash; and answers each as a discriminant against the same two primitives, with "
          "measured gamete-machinery promoter &gamma; as the only new input.</p>",
          '<p class="note">The gamete-program genes (TEKT1, MOS, CATSPER1, DMC1, MLH1, SPO11, PRDM9, REC8, ZP3, '
          "and the rest) were declared by function <em>before</em> any &gamma; was read, and the reception refuses "
          "to persist unless both vendored anchors (SOX9, DAZL) reproduce exactly. &gamma; enters the dynamics only "
          "where a measured master names a mechanism the substrate already owns.</p>",

          "<h2>How a gamete is made: one replication, two ordered divisions</h2>",
          "<p>Meiosis copies the genome once and then divides twice, so a diploid cell becomes four haploid gametes; "
          "fertilisation restores the diploid count. The ploidy bookkeeping is exact.</p>",
          eq_fig("rep-gmt-001", "Meiotic ploidy trajectory: one replication (S), two divisions (MI, MII)."),
          table(["meiotic stage", "ploidy (N = sets, C = chromatids)"], ploidy_rows),
          "<p>The non-trivial part is the <em>order</em>: meiosis I is reductional (it separates homologues, halving "
          "N) and meiosis II is equational (it separates sister chromatids, like mitosis). On the substrate this "
          "order is not assumed &mdash; it is forced by a two-stage release of REC8 cohesin (measured &gamma; = " +
          f(G1["rec8_gamma"], 4) + ", spinodal " + f(G1["cohesin_spinodal"], 4) + "). Arm cohesin is unprotected and "
          "releases first (separase reaches " + f(G1["separase_at_arm_release"], 3) + " at MI); centromeric cohesin "
          "is shielded by shugoshin, modelled as a protection offset, and only releases at MII (separase " +
          f(G1["separase_at_centromeric_release"], 3) + "). The order follows from the sign of the protection, not "
          "from any tuned rate.</p>",

          "<h2>Are gametes identical? No &mdash; by an astronomical margin</h2>",
          "<p>Two independent mechanisms make two identical gametes effectively impossible. Independent assortment of "
          "the 23 homologue pairs gives exactly 2<sup>23</sup> orientations on its own.</p>",
          eq_fig("rep-gmt-002", "Independent assortment: 2 raised to the haploid chromosome number."),
          "<p>Recombination then adds far more, and it does so in a structured way. Crossovers are not placed at "
          "random: they show <em>interference</em> &mdash; one crossover suppresses another nearby. On this substrate "
          "interference is the same refractory dead-zone that regularises FHN spikes, but mapped from time onto the "
          "chromosome axis. Dense candidate crossovers thinned by a minimum-separation refractory length become "
          "sub-Poisson and regularly spaced, with an obligate crossover per bivalent.</p>",
          eq_fig("rep-gmt-003", "Crossover interference as spatial refractoriness: the count is sub-Poisson."),
          "<p>The modelled crossover count is " + f(cm["mean_crossovers"], 2) + " per bivalent with Fano factor " +
          f(cm["fano_factor"], 3) + " &mdash; far below the Poisson null of " + f(cm["null_poisson_fano"], 3) +
          " &mdash; gap CV " + f(cm["gap_cv"], 2) + " (more regular than random), and an obligate-crossover fraction "
          "of " + f(cm["obligate_crossover_fraction"], 1) + ". Combined with assortment, the floor on distinct "
          "gametes exceeds 10<sup>" + str(int(G2["diversity"]["log10_distinct_gametes_floor"])) + "</sup>: two "
          "identical gametes from one person are, for all practical purposes, impossible. <b>[V]</b></p>",

          "<h2>Sperm motility: the flagellum is the fast end of the oscillator ladder</h2>",
          "<p>The flagellar beat is not a new device. It is the same relaxation oscillator that runs every other "
          "reproductive rhythm, taken to its fast limit by shortening the recovery timescale. That places it at the "
          "bottom of a four-clock ladder.</p>",
          eq_fig("rep-gmt-004", "Four-clock ladder: the flagellar beat is the fastest relaxation oscillator."),
          "<p>In arbitrary substrate units the periods order as " + f(lad["flagellum_arb"], 1) + " (flagellum) &lt; " +
          f(lad["pulse_arb"], 1) + " (GnRH pulse) &lt; " + f(lad["spermatogenic_arb"], 1) + " (spermatogenic) &lt; " +
          f(lad["menstrual_arb"], 1) + " (menstrual), anchored to a beat of about " + f(G3["beat_anchor_hz"], 0) +
          "&nbsp;Hz. Hyperactivation &mdash; the switch to the whip-like motility that lets a sperm penetrate the "
          "egg coat &mdash; is driven by CatSper Ca<sup>2+</sup> (measured &gamma; = " + f(G3["catsper_gamma"], 4) +
          "), modelled as a rise in oscillator gain. Two co-signatures must move together, and they do: the beat "
          "grows in amplitude (" + f(hyp["activated_amp"], 2) + " &rarr; " + f(hyp["hyperactivated_amp"], 2) +
          ") and slows (" + str(hyp["activated_beats"]) + " &rarr; " + str(hyp["hyperactivated_beats"]) +
          " beats). The 9+2 axoneme&rsquo;s nine-fold symmetry is a structural integer the framework does <em>not</em> "
          "derive &mdash; it is declared open, not back-fitted.</p>",

          "<h2>The egg: a switch held at the brink, released once</h2>",
          "<p>Where the sperm is a free-running oscillator, the egg is the opposite use of the same kernel: a switch "
          "<em>held</em> in a metastable basin. The mature egg arrests at metaphase II, waiting, held there by a "
          "sustained cytostatic drive (c-Mos, measured &gamma; = " + f(G4["mos_gamma"], 4) + "; arrested state " +
          f(G4["arrested_state"], 3) + "). Fertilisation is a single supra-spinodal kick: a Ca<sup>2+</sup> transient "
          "below the spinodal (" + f(G4["activation_spinodal"], 4) + ") does nothing, but one above it flips the "
          "switch irreversibly.</p>",
          eq_fig("rep-gmt-005", "Fertilisation as a one-way spinodal flip; past the spinodal it cannot reverse."),
          "<p>The same irreversibility is the polyspermy block: once the egg has flipped, the basin it sat in is "
          "gone, so a second sperm&rsquo;s Ca<sup>2+</sup> has nothing left to trigger (ZP3 receptor &gamma; = " +
          f(G4["zp3_gamma"], 4) + "). The egg does not need an active &lsquo;lock&rsquo; &mdash; past-spinodal "
          "geometry is the lock. <b>[V]</b></p>",

          "<h2>The measured &gamma; atlas, and an honest null</h2>",
          "<p>The gamete-program promoters were measured through the identical DNA pipeline used for the organ "
          "masters. In ascending &gamma;: " + atlas_line + ".</p>",
          table(["module", "n", "mean &gamma;", "sd", "range"], module_rows),
          "<p>A pre-registered test asked whether promoter &gamma; <em>separates</em> the three functional modules "
          "(meiosis / sperm / oocyte). It does not: the permutation test returns F-like " +
          f(pre["f_like_statistic"], 3) + ", p = " + f(pre["p_permutation"], 3) + " &mdash; a null, reported as it "
          "falls. What <em>is</em> supported is narrower and was tested separately: the core recombination genes "
          "(SPO11, DMC1, MLH1, PRDM9) form a tight &gamma; cluster (CV " + f(core["core_cv"], 4) + " versus panel CV " +
          f(core["panel_cv"], 4) + ", p = " + f(core["p_core_tighter_than_random"], 4) + "). The framework claims "
          "only the second result, and only at the grade the test supports.</p>",

          "<h2>One substrate, two gametes: the dynamical root of anisogamy</h2>",
          "<p>The chapter closes where it began. The same kernel is a free-running oscillator for the sperm and a "
          "held switch for the egg &mdash; motion versus patience, read off one equation. The count asymmetry has "
          "the same origin: spermatogenesis divides symmetrically into " + str(dsym["spermatogenesis_symmetric_gametes"]) +
          " equal gametes, while oogenesis divides asymmetrically into " + str(dsym["oogenesis_eggs"]) + " large egg "
          "plus " + str(dsym["oogenesis_polar_bodies"]) + " vanishing polar bodies, concentrating the cytoplasm "
          "(egg:polar-body mass " + f(prov["egg_over_polar_body"], 0) + "&times;). The measured size consequence is "
          "an egg:sperm volume ratio of about " + format(int(prov["volume_ratio_anchor"]), ",") + " &times; (" +
          f(prov["oocyte_um"], 0) + "&nbsp;&micro;m versus " + f(prov["sperm_head_um"], 1) + "&nbsp;&micro;m, cubed). "
          "Anisogamy &mdash; the deepest asymmetry in reproduction &mdash; is, on this substrate, an oscillator and a "
          "switch built from one rule. The evolutionary &lsquo;why&rsquo; of that asymmetry is game-theoretic and "
          "sits outside the substrate; it is marked open.</p>",
          '<p class="disclaimer">Mechanisms and ploidy logic are sim-verified [V]; promoter &gamma; and the size, '
          "cohesin and Ca<sup>2+</sup> magnitudes are measured or anchored [L]; separase kinetics, the integer 9 of "
          "the axoneme, the realised per-meiosis crossover count, and the evolutionary origin of anisogamy are "
          "declared open [O]. This is a research model, not clinical advice.</p>",
        ]),
    ))

    # ---- 12 the embryo: fertilisation to fetus (embryogenesis) ----------------------------------
    E1, E2, E3, E4, E5, E6 = (D["emb"]["E1"], D["emb"]["E2"], D["emb"]["E3"],
                              D["emb"]["E4"], D["emb"]["E5"], D["emb"]["E6"])
    enc = E1["encounter"]; dna = E1["dna_emergence"]; uniq = E1["genome_uniqueness"]
    cleav = E2; massd = E2["mass"]; fate = E2["first_fate_switch"]
    zga = E3["zga_crossing"]; mat = E3["maternal_stores"]
    clk = E4; stest = E4["preregistered_stage_test"]; htest = E4["preregistered_hox_test"]
    arc = E5["arc"]; fet = E5["fetus"]
    eatlas = D["emb_atlas"]
    # developmental gamma atlas table, grouped by stage then ascending gamma
    struct_by_master = {s["master"]: s for s in E4["structures"]}
    stage_label = {"pluripotency": "pluripotency", "germ_layer": "germ layer",
                   "organ_primordium": "organ primordium", "ap_axis": "AP-axis (HOX)"}
    atlas_rows = []
    for s in E4["emergence_order_gamma_ascending"]:
        st = struct_by_master[s]
        atlas_rows.append([s, stage_label.get(st["stage"], st["stage"]), f(st["gamma"], 4),
                           f(st["functional_spinodal"], 4), f(st["rel_size_dwell"], 4)])
    ploidy_emb_rows = [["sperm pronucleus", dna["sperm_pronucleus"]],
                       ["egg pronucleus (on activation)", dna["egg_pronucleus"]],
                       ["zygote (syngamy)", dna["zygote"]],
                       ["zygote after S-phase", dna["zygote_after_S"]]]
    stage_means = clk["stage_means"]
    order_line = " &rarr; ".join(E4["emergence_order_gamma_ascending"])
    CH.append(dict(
        slug="12-embryogenesis-fertilisation-to-fetus", no=12,
        subj="The embryo: fertilisation to fetus",
        crumb="Fertilisation to fetus",
        h1="From two gametes to a fetus: syngamy, cleavage, genome activation, and the gene-clock",
        knows=["fertilisation", "syngamy", "zygote", "pronuclear fusion", "cleavage", "blastocyst",
               "inner cell mass", "zygotic genome activation", "maternal-to-zygotic transition",
               "morphogenesis gene-clock", "body plan", "HOX colinearity"],
        desc=("The embryo on the same substrate: the sperm (oscillator) meets the egg (held switch) and "
              "flips it, two haploids fuse to a unique diploid genome, cleavage and ZGA follow, and the "
              "gene-clock argsort(spinodal(gamma)) lays out the body plan of a fetus."),
        answer=("The two gametes meet and a fetus is built on the same substrate. The sperm (a free "
                "oscillator) delivers a supra-spinodal Ca&sup2;&#8314; kick that flips the egg (a held "
                "switch) one-way; two haploid pronuclei fuse, restoring diploidy (1N+1N&rarr;2N) and "
                "emerging a genome unique to a floor of 10<sup>" + str(int(uniq["log10_distinct_zygotes_floor"])) +
                "</sup>. Cleavage is 2<sup>n</sup> symmetric divisions at conserved mass; the zygotic "
                "genome switches on in one spinodal crossing (ZGA); then the morphogenesis gene-clock "
                "&mdash; emergence order = argsort(spinodal(&gamma;)) &mdash; lays out the body plan, "
                "pluripotency first and organ primordia last. Events and order are sim-verified; absolute "
                "gestational timing is open."),
        abstract=("Each step is a discriminant against the vendored R19 switch and FHN oscillator, reusing "
                  "the gamete results (G1&ndash;G6) and adding a measured developmental master-gene &gamma; "
                  "panel as the only new input. Fertilisation reuses the egg switch (a supra-spinodal flip "
                  "with a polyspermy block); diploidy restoration is exact and the new genome's uniqueness "
                  "floor is the square of the gamete floor. The body-plan order is the cited DNA gene-clock "
                  "argsort(spinodal(&gamma;)); a pre-registered test finds &gamma; rises with developmental "
                  "stage (Spearman &rho; = " + f(stest["spearman_rho"], 3) + ", p = " +
                  f(stest["p_permutation_one_sided"], 3) + "), while the HOX colinearity test is reported as "
                  "a partial result. The full-body atlas remains the DNA package's single source of truth."),
        cards=cards("gamma", "spinodal", "dwell"),
        page_grade="V",
        body="\n".join([
          "<h2>The gametes were made; now they meet</h2>",
          "<p>The previous chapter emerged the two gametes as opposite uses of one kernel &mdash; a "
          "free-running oscillator (the sperm) and a switch held at metaphase II (the egg). This chapter "
          "answers the obvious next question: let them meet, let a genome emerge, and let a fetus be built. "
          "Every step is a discriminant against the same R19 switch and FHN oscillator, and the only new "
          "input is a measured developmental master-gene &gamma; panel.</p>",
          '<p class="note">Firewall: this package owns the <em>fertilisation event</em> (its two gametes '
          "meeting) and the early embryo (the oocyte-to-embryo transition). The full multi-organ "
          "morphogenesis atlas and the gene-clock law are owned by the 4D DNA Blueprint package and cited "
          "here, never re-derived. The body-plan panel below is a measured demonstration of that clock.</p>",

          "<h2>Syngamy: the egg flips, two haploids fuse, a unique genome emerges</h2>",
          "<p>The sperm&rsquo;s arrival is a Ca<sup>2+</sup> transient at the egg cortex. The egg switch "
          "behaves exactly as it did in isolation: a sub-spinodal contact does nothing (" +
          ("flips" if enc["incomplete_contact_flips"] else "no flip") + "), while a supra-spinodal contact "
          "flips it one-way (" + ("flips" if enc["fertilising_contact_flips"] else "no flip") +
          "), and a second sperm is excluded because the basin it would need is gone (polyspermy block = " +
          str(enc["polyspermy_block_one_sperm"]) + ").</p>",
          "<p>Activation triggers pronuclear fusion, and this is where the new genome emerges: a haploid "
          "sperm pronucleus and a haploid egg pronucleus combine to restore the diploid count. The ploidy "
          "bookkeeping is exact.</p>",
          eq_fig("rep-emb-001", "Syngamy: two haploid pronuclei fuse to the diploid zygote."),
          table(["meiotic / zygotic stage", "ploidy (N = sets, C = chromatids)"], ploidy_emb_rows),
          "<p>The emerged genome is <em>unique</em>. Each gamete was one draw from the diversity of the "
          "previous chapter (assortment &times; interference-spaced recombination, a floor of 10<sup>" +
          str(int(uniq["log10_distinct_gametes_floor"])) + "</sup> per gamete); the zygote is the product of "
          "two such draws, so its distinct-genome floor is the square &mdash; about 10<sup>" +
          str(int(uniq["log10_distinct_zygotes_floor"])) + "</sup>. This diploid genome has, for all "
          "practical purposes, never existed before and will not recur.</p>",
          eq_fig("rep-emb-002", "Genome uniqueness: the zygote floor is the square of the gamete floor."),

          "<h2>Cleavage: more cells, not a bigger embryo</h2>",
          "<p>The zygote then cleaves. Unlike oogenesis, which divided asymmetrically into one large egg "
          "and three vanishing polar bodies, cleavage is <em>symmetric</em> &mdash; each blastomere splits "
          "into two equal daughters, so the count doubles: " +
          " &rarr; ".join(str(c) for c in cleav["cell_counts"]) + ".</p>",
          eq_fig("rep-emb-003", "Cleavage: 2^n symmetric divisions at conserved cytoplasmic mass."),
          "<p>The defining feature is that cleavage <em>subdivides a fixed mass</em> rather than growing it: "
          "the summed blastomere mass stays at the zygote value (" + f(massd["total_after_cleavage"], 3) +
          "), and each blastomere shrinks to 1/2<sup>n</sup> of the zygote (" +
          f(massd["per_blastomere_fraction"], 4) + "). The first cell-fate decision of the new organism is "
          "the inner-cell-mass versus trophectoderm split, and it is the same R19 bistable switch as every "
          "other fate flip: position sets the drive sign, giving an inner basin (ICM state " +
          f(fate["icm_state"], 3) + ", &rarr; the embryo proper) and an outer basin (TE state " +
          f(fate["te_state"], 3) + ", &rarr; the placenta).</p>",

          "<h2>Zygotic genome activation: the genome&rsquo;s own switch-on</h2>",
          "<p>Before activation the embryo runs on maternal stores laid down in the oocyte &mdash; the "
          "oocyte-program genes the gamete chapter measured (ZAR1, the zygote-arrest / oocyte-to-embryo "
          "factor; NLRP5; c-Mos), with the zygotic genome transcriptionally off. Zygotic genome activation "
          "is a rising competence drive crossing the spinodal, and the genome switches on in one "
          "discontinuous step &mdash; the genome&rsquo;s analogue of the puberty crossing.</p>",
          eq_fig("rep-emb-004", "ZGA: the zygotic genome switches on past the competence spinodal."),
          "<p>Ramping the competence drive from zero, the genome-enable state stays off on maternal-only "
          "input until the spinodal " + f(zga["spinodal"], 4) + ", then jumps by " + f(zga["jump_size"], 3) +
          " at drive " + f(zga["zga_drive"], 4) + " &mdash; a one-step crossing, not a gradual ramp. This is "
          "the handoff from the gamete program this package owns (maternal: " +
          ", ".join(E3["handoff"]["maternal_program"]) + ") to the embryo&rsquo;s own genome (the "
          "developmental panel below).</p>",

          "<h2>The gene-clock builds the body of a fetus</h2>",
          "<p>With the genome on, the body plan unfolds. The morphogenesis gene-clock &mdash; cited from "
          "the 4D DNA Blueprint &mdash; says the emergence order is the argsort of the spinodal over the "
          "master genes; because the spinodal is monotone in &gamma;, that order is simply &gamma; "
          "ascending: a lower-&gamma; master clears its presence threshold sooner and acts earlier.</p>",
          eq_fig("rep-emb-005", "The gene-clock: emergence order is argsort of the spinodal, i.e. gamma ascending."),
          "<p>Measured through the identical promoter pipeline (validated on the SOX9 and DAZL anchors), the "
          "developmental panel orders as: " + order_line + ". Each master&rsquo;s functional spinodal sets "
          "its place in developmental time, and its dwell sets relative size.</p>",
          table(["master gene", "stage", "&gamma; (measured)", "functional spinodal", "rel. size (dwell)"],
                atlas_rows),
          "<p>The pre-registered test asks whether &gamma; rises with developmental stage. It does: the "
          "stage means climb from pluripotency (" + f(stage_means[1], 4) + ") through germ-layer (" +
          f(stage_means[2], 4) + ") to organ-primordium (" + f(stage_means[3], 4) + "), and the "
          "Spearman correlation of &gamma; against the declared stage rank is &rho; = " +
          f(stest["spearman_rho"], 3) + " (permutation p = " + f(stest["p_permutation_one_sided"], 3) +
          "). Pluripotency masters sit earliest on the clock and organ masters latest &mdash; the body plan "
          "is laid down in the order the framework predicts.</p>",
          "<p>A second pre-registered test &mdash; HOX 3&prime;&rarr;5&prime; colinearity (anterior genes "
          "early, posterior genes late) &mdash; is reported as a <em>partial</em> result, in the honest "
          "style of the gamete chapter&rsquo;s null. The posterior-most HOX (" + htest["order_3to5"][-1] +
          ") does carry the highest &gamma; of the sub-panel, but across only three genes the rank "
          "correlation (&rho; = " + f(htest["spearman_rho"], 3) + ", p = " + f(htest["p_exact_one_sided"], 3) +
          ") does not reach significance; only the narrow claim is made.</p>",

          "<h2>The whole arc: one sperm, one egg, one fetus</h2>",
          "<p>Run end-to-end, a specific sperm and a specific egg &mdash; each a deterministic draw from "
          "the gamete diversity &mdash; produce a zygote whose genome fingerprint is reproducible and "
          "unique. The arc passes at every stage: syngamy (" + arc["E1_syngamy"] + "), cleavage (" +
          arc["E2_cleavage"] + "), genome activation (" + arc["E3_zga"] + "), and the gene-clock body plan "
          "(" + arc["E4_gene_clock"] + ").</p>",
          "<p>The result is a fetus carrying a unique diploid genome (floor 10<sup>" +
          str(int(fet["genome_uniqueness_log10"])) + "</sup>), an inner-cell-mass-derived body of " +
          str(fet["total_body_plan_structures"]) + " gene-clock-ordered structures, with the placenta on "
          "the trophectoderm side. The earliest structures laid down are " +
          ", ".join(fet["body_plan_first_structures"][:4]) + ". Every step is one R19 switch or one FHN "
          "oscillator, reused; nothing new was added to the substrate.</p>",
          '<p class="disclaimer">Mechanisms and the emergence <em>order</em> are sim-verified [V]; the '
          "developmental &gamma; values and the diversity, cleavage and Ca<sup>2+</sup> anchors are measured "
          "or structural [L]; the absolute gestational timing (days post-fertilisation, weeks of gestation) "
          "is open [O] and needs external endocrine calibration, exactly as puberty&rsquo;s calendar age is "
          "left open. The full multi-organ morphogenesis atlas and the gene-clock law are owned by the 4D "
          "DNA Blueprint package and cited here. This is a physics-derived research model, not clinical "
          "advice.</p>",
        ]),
    ))

    # ---- 13 infertility and subfertility (fertility) --------------------------------------------
    F1, F2, F3, F4, F5 = D["fer"]["F1"], D["fer"]["F2"], D["fer"]["F3"], D["fer"]["F4"], D["fer"]["F5"]
    fsub = F2["subfertile"]; fster = F2["sterile"]
    CH.append(dict(
        slug="13-infertility-and-subfertility", no=13,
        subj="Infertility and subfertility: past a spinodal vs near a threshold",
        crumb="Infertility &amp; subfertility",
        h1="Infertility and subfertility: one distinction, a spinodal apart",
        knows=["infertility", "subfertility", "fecundability", "Kramers escape rate", "azoospermia",
               "anovulation", "ovarian reserve", "cohesin fatigue", "aneuploidy", "ICSI"],
        desc=("Conception is an AND of substrate operations; infertility is an operation past a spinodal "
              "(categorical), subfertility is one near a threshold (a finite Kramers rate per cycle)."),
        answer=("The reproductive arc is a chain of substrate operations and conception requires every one "
                "to succeed. Infertility is an operation on the wrong side of a spinodal &mdash; categorical "
                "and deterministic, a per-cycle probability of exactly zero that a sub-threshold drive cannot "
                "move. Subfertility is an operation near its threshold &mdash; a small but finite Kramers "
                "crossing rate per cycle, so the same drive that does nothing across a spinodal moves it "
                "exponentially. One distinction, two failure classes. <b>[V]</b>"),
        abstract=("Each link of the chain is an operation the earlier chapters verified (the GnRH pulse, the "
                  "follicle/sperm switch, ordered REC8 meiosis, gamete number, the metaphase-II flip, syngamy, "
                  "ZGA, the gene-clock). The categorical/probabilistic split is computed on the same R19 "
                  "spinodal and Kramers exp(&minus;&Delta;V/D) the oncology chapter uses: a fixed drive nudge "
                  "raises a near-threshold cycle probability " + f(fsub["fold_response"], 2) + "&times; while "
                  "leaving a past-spinodal operation at exactly zero. Male factor is oscillator throughput; "
                  "female factor adds REC8 cohesin fatigue, the rising-with-age mis-segregation clock; and "
                  "treatment is read as a substrate move. Honestly graded; a research model, not a diagnostic."),
        cards=cards("spinodal", "barrier"),
        page_grade="V",
        body="\n".join([
          "<h2>Conception is an AND of substrate operations</h2>",
          "<p>Every step the package built &mdash; the GnRH pulse, the follicle and sperm switches, ordered "
          "meiosis, gamete number, the metaphase-II flip, syngamy, ZGA, the gene-clock body plan &mdash; is "
          "an operation that must succeed. Conception is their logical AND, so a single link below threshold "
          "is sterility, whatever the rest of the chain does.</p>",
          eq_fig("rep-inf-001", "Conception as the product (AND) of the substrate gates; one zero zeroes it."),
          fertility_chain_table(D),
          "<h2>The central distinction: a spinodal apart</h2>",
          "<p>Infertility and subfertility are not two points on one scale; they are two sides of a spinodal. "
          "An operation pushed past its spinodal loses the conception basin entirely &mdash; per-cycle success "
          "is exactly zero, and a sub-threshold change in drive does nothing. An operation that merely sits "
          "<em>near</em> its threshold still has the basin, just behind a high barrier.</p>",
          eq_fig("rep-inf-003", "Categorical (past the spinodal) versus probabilistic (below it)."),
          "<p>For the near-threshold case the per-cycle probability is a Kramers crossing &mdash; the same "
          "escape-over-a-barrier the oncology chapter uses, here for a <em>good</em> outcome. Because the rate "
          "is exponential in the barrier, a modest favourable drive moves it a lot.</p>",
          eq_fig("rep-inf-002", "Per-cycle conception as a Kramers rate over the residual barrier."),
          "<p>The dissociation is the whole point. A single fixed drive nudge raises the subfertile cycle "
          "probability from " + f(fsub["p_per_cycle"], 3) + " to " + f(fsub["p_per_cycle_treated"], 3) +
          " (" + f(fsub["fold_response"], 2) + "&times;), turning a " + f(fsub["p_year"], 2) + " annual chance "
          "into " + f(fsub["p_year_treated"], 2) + "; the identical nudge applied past the spinodal leaves the "
          "sterile operation at " + f(fster["p_per_cycle"], 1) + ". Same drive, exponential versus nothing.</p>",
          f2_table(D),
          eq_fig("rep-inf-004", "Cumulative-over-cycles: subfertility is a delay, infertility a wall."),
          "<h2>Male factor: spermatogenesis is oscillator throughput</h2>",
          "<p>Whether sperm are made at all is an R19 switch: below its spinodal the switch never flips, which "
          "is azoospermia &mdash; categorical, sterile. How <em>many</em> are made once it is on is oscillator "
          "throughput: the seminiferous and flagellar beat (the fast clock of &sect;11), whose rate falls from "
          + str(F3["normal_throughput"]["beats"]) + " beats to " + str(F3["oligo_astheno_subfertile"]["beats"]) +
          " as the recovery slows &mdash; oligo- and asthenozoospermia, subfertile but not zero.</p>",
          "<p>Hyperactivation is a separate gate. Without the supra-spinodal CatSper gain (measured &gamma; = " +
          f(F3["catsper_gate"]["catsper_gamma"], 4) + ") the beat cannot enter the penetrating regime, so a "
          "normal count can still fail at the egg coat &mdash; a categorical sub-case sitting on top of the "
          "throughput axis.</p>",
          "<h2>Female factor: the ovulation switch and REC8 cohesin fatigue</h2>",
          "<p>Anovulation is the mid-cycle surge switch failing to flip &mdash; sub-spinodal drive, no surge, "
          "sterile &mdash; the same switch &sect;5 and &sect;10 describe. The deeper female clock is the egg "
          "itself: a bivalent is held for decades by REC8 cohesin (measured &gamma; = " +
          f(F4["cohesin_gamma"], 4) + "), a switch whose holding barrier is the same &gamma;&sup2;/4 the "
          "substrate sets.</p>",
          "<p>As cohesin integrity decays with the years held, that barrier falls and the per-egg "
          "mis-segregation (aneuploidy) escape rate rises &mdash; from " +
          f(F4["missegregation_probability"][0], 3) + " modelled at " + str(F4["age_years"][0]) + " to " +
          f(F4["missegregation_probability"][-1], 3) + " by " + str(F4["age_years"][-1]) +
          ". This rising shape is the molecular clock of age-related subfertility; the latch lost early and "
          "irreversibly is premature ovarian insufficiency, the menopause failure of &sect;10 brought "
          "forward.</p>",
          eq_fig("rep-inf-005", "Cohesin fatigue: the held barrier decays, mis-segregation rises with age."),
          cohesin_age_table(D),
          "<h2>Treatment is a move on the substrate</h2>",
          "<p>The clinic&rsquo;s tools read as three substrate moves. The hCG trigger and ovulation induction "
          "are a supra-spinodal kick that forces a stuck switch across (the spinodal kick &sect;10 already "
          "retrodicts); pulsatile GnRH restarts the oscillator where continuous suppresses it (" +
          str(F5["pulsatile_pulses"]) + " pulses versus " + str(F5["continuous_pulses"]) +
          ", from &sect;9); and ICSI or IVF bypass a missing gate by supplying the flip it could not reach.</p>",
          "<p>Each maps onto the chain: push a near-threshold operation across, restart a stalled oscillator, "
          "or substitute for a categorical gate. The framework adds the <em>why</em> &mdash; which class of "
          "failure each tool is for &mdash; not a schedule.</p>",
          '<p class="disclaimer">The chain-AND logic and the categorical/probabilistic dissociation are '
          "sim-verified [V]; fecundability, the Kramers temperature, REC8/CatSper &gamma; and the clinical "
          "age-aneuploidy anchor are measured or anchored [L]; every absolute per-cycle probability, the map "
          "from a real semen or age value to a drive, and specific azoospermia/POI gene &gamma; are open [O]. "
          "This is a physics-derived research model, not a diagnosis or a treatment plan.</p>",
        ]),
    ))

    # ---- 14 sex determination and sex-ratio distortion (sex-ratio) -------------------------------
    S1, S2, S3, S4, S5, S6 = (D["sxr"]["S1"], D["sxr"]["S2"], D["sxr"]["S3"], D["sxr"]["S4"],
                              D["sxr"]["S5"], D["sxr"]["S6"])
    ag = S1["antagonist_gamma"]
    CH.append(dict(
        slug="14-sex-determination-and-sex-ratio-distortion", no=14,
        subj="Sex determination and sex-ratio distortion: tilting a fair coin",
        crumb="Sex &amp; sex-ratio distortion",
        h1="Sex determination and sex-ratio distortion: how a gene tilts a fair coin",
        knows=["sex determination", "SRY", "SOX9", "FOXL2", "DMRT1", "meiotic drive",
               "segregation distortion", "transmission ratio", "sex ratio", "X-shredder", "Fisher principle"],
        desc=("Mammalian sex is the SOX9<->FOXL2 bistable switch; Mendel is the same switch untilted; "
              "a drive gene tilts it, and a sex-chromosome driver skews the offspring sex ratio."),
        answer=("Mammalian sex is one bistable switch: SOX9 (testis, measured &gamma; = " + f(ag["SOX9"], 4) +
                ") against FOXL2 (ovary, &gamma; = " + f(ag["FOXL2"], 4) + "), with SRY the tipping drive. "
                "Mendelian 50:50 is that switch untilted &mdash; a fair coin. A meiotic-drive gene tilts it, so "
                "transmission climbs from one-half and, past the spinodal, fixes near one. A sex-chromosome-"
                "linked driver tilts the X-versus-Y gamete switch, skewing offspring sex &mdash; male for an "
                "X-shredder, female for a Y-killer &mdash; while Fisher&rsquo;s restoring force holds the "
                "population at 1:1. <b>[V]</b>"),
        abstract=("The sex-determination masters are measured through the identical DNA pipeline (testis axis "
                  "SRY/SOX9/DMRT1, ovary axis FOXL2/RSPO1/WNT4), validated by reproducing the SOX9 and FOXL2 "
                  "anchors. Sex is the mutual-antagonism toggle reduced to one R19 well; segregation is that "
                  "well untilted (transmission " + f(S2["transmission_ratio_analytic"], 2) + "); a drive is a "
                  "tilt whose transmission ratio is a Boltzmann basin occupancy, rising to " +
                  f(S3["transmission_ratio_suprapinodal"], 2) + " past the spinodal. A sex-chromosome driver is "
                  "the same tilt with a sign, giving an " + f(S4["ssr_X_shredder_male"], 2) + " male or " +
                  f(S4["ssr_Y_killer_female"], 2) + " female secondary ratio. A pre-registered test of whether "
                  "the axis separates promoter &gamma; is reported as it falls, including its null."),
        cards=cards("gamma", "spinodal"),
        page_grade="V",
        body="\n".join([
          "<h2>Sex itself is one bistable switch</h2>",
          "<p>Mammalian sex is not a gradient but a switch: the testis programme (SOX9, measured &gamma; = " +
          f(ag["SOX9"], 4) + ") and the ovary programme (FOXL2, &gamma; = " + f(ag["FOXL2"], 4) +
          ") mutually repress, and that antagonism reduces along its order parameter to a single R19 double "
          "well. SRY is a transient supra-spinodal drive that selects the testis basin; the basin then holds "
          "itself.</p>",
          eq_fig("rep-sxr-001", "The sex switch: the SOX9/FOXL2 antagonism as one R19 well, SRY the drive."),
          "<p>Because the well is bistable the choice is hysteretic, which is why the adult gonad is "
          "<em>maintained</em>: a sub-spinodal perturbation cannot flip it, but a supra-spinodal one "
          "transdifferentiates &mdash; exactly the FOXL2- and DMRT1-knockout result. The switch is held for "
          "life, not set once.</p>",
          "<h2>Mendel&rsquo;s first law is a fair coin</h2>",
          "<p>A heterozygous transmission locus is the same switch with no tilt. With the two alleles as two "
          "equal-depth basins, segregation is unbiased: an ensemble of meioses splits " +
          f(S2["transmission_ratio_simulated"], 3) + " to the positive basin, the analytic " +
          f(S2["transmission_ratio_analytic"], 2) + ". Mendelian 50:50 is an untilted R19 switch &mdash; this "
          "is the null the rest of the chapter departs from.</p>",
          eq_fig("rep-sxr-002", "Mendelian segregation: the symmetric (untilted) switch is a fair coin."),
          "<h2>Meiotic drive is a tilt on the switch</h2>",
          "<p>A segregation-distorter gene imposes a tilt on the segregation switch, deepening its own basin. "
          "The transmission ratio is then a Boltzmann occupancy of the two basins, climbing smoothly from "
          "one-half as the tilt grows. Below the spinodal the distortion is graded (" +
          f(S3["transmission_ratio_subspinodal"], 2) + " at a sub-spinodal tilt); past it the loser basin "
          "vanishes and transmission fixes near " + f(S3["transmission_ratio_suprapinodal"], 2) +
          " &mdash; the t-haplotype and Segregation-Distorter limit.</p>",
          eq_fig("rep-sxr-003", "Transmission ratio as basin occupancy; supra-spinodal drive fixes the allele."),
          transmission_table(D),
          "<h2>Sex-ratio distortion: a tilt with a sign</h2>",
          "<p>Now make the driver sit on a sex chromosome. It tilts the switch deciding which sperm class "
          "&mdash; X-bearing or Y-bearing &mdash; survives meiosis, so the offspring sex ratio skews. An "
          "X-shredder that cleaves X-bearing sperm over-transmits the Y, giving a male-biased secondary ratio "
          "of " + f(S4["ssr_X_shredder_male"], 2) + "; a Y-killer or X-driver does the opposite, " +
          f(S4["ssr_Y_killer_female"], 2) + " &mdash; female-biased.</p>",
          eq_fig("rep-sxr-004", "Sex-ratio skew: the same tilt with a sign sets which sex predominates."),
          "<p>It is one mechanism with two signs, and a weaker driver gives a partial skew (" +
          f(S4["ssr_subspinodal_partial"], 2) + ") rather than all-or-none &mdash; the same graded-then-fixed "
          "behaviour as autosomal drive, now read out as the sex of the children. This is the direct answer to "
          "how a gene makes one sex predominate.</p>",
          "<h2>Fisher&rsquo;s restoring force holds the population at 1:1</h2>",
          "<p>Drive tilts the individual switch, but the population does not run away. The rarer sex has higher "
          "per-capita reproductive value, so selection favours producers of it and suppressors of drive spread "
          "&mdash; making a 1:1 population ratio a stable attractor. A persistent weak driver only shifts the "
          "fixed point a little (to " + f(S5["r_under_weak_drive"], 3) + "), not to fixation.</p>",
          eq_fig("rep-sxr-005", "Fisher: 1:1 is a stable fixed point; drive shifts it only boundedly."),
          "<p>The human secondary sex ratio (~" + f(S5["human_secondary_sex_ratio"], 3) + " male) is exactly "
          "this kind of tiny residual, not a strong-drive case; its cause &mdash; paternal-age and "
          "hormonal-timing hypotheses &mdash; is left open, because the genetics are not pinned.</p>",
          "<h2>The measured &gamma; atlas and an honest null</h2>",
          "<p>The sex-determination masters were measured through the identical DNA pipeline and validated on "
          "the SOX9 and FOXL2 anchors. A pre-registered test asked whether the axis (testis versus ovary) "
          "<em>separates</em> promoter &gamma;: the ovary axis trends higher (" +
          f(S6["ovary_axis_mean_gamma"], 4) + " versus " + f(S6["testis_axis_mean_gamma"], 4) +
          "), but with SRY a strong low-&gamma; outlier and three genes per axis the permutation test returns "
          "p = " + f(S6["permutation_p"], 2) + " &mdash; not significant. The null is reported as it falls; the "
          "chapter&rsquo;s verified claims do not depend on it.</p>",
          sexdet_gamma_table(D),
          '<p class="disclaimer">The bistable switch, the fair-coin null, drive-as-a-tilt, the signed '
          "sex-ratio skew and Fisher&rsquo;s two-level dynamics are sim-verified [V]; the sex-determination "
          "&gamma; and the observed drive transmission ratios are measured or anchored [L]; the cause of the "
          "human sex-ratio residual, the absolute transmission numbers, and whether axis separates &gamma; at "
          "this sample size are open [O]. The full sex-determination atlas and the gene-drive population "
          "genetics are owned by the DNA and population-genetics packages and cited here. A research model, "
          "not clinical or reproductive advice.</p>",
        ]),
    ))

    return CH

# ===================================================================================================
# HUB (docs/index.html) -- paper front page: thesis, contents, headline results (VP-SPEC sec 6, hub).
# ===================================================================================================
def build_hub(D, CH):
    em = D["emerge"]; T1, T2, T3, T4, T5 = D["T1"], D["T2"], D["T3"], D["T4"], D["T5"]
    onc, thr = D["onc"], D["thr"]
    order = {o["organ"]: o for o in em["organs"]}
    order_names = " &rarr; ".join(order[o]["organ"].replace("gonad_", "").replace("reproductive_", "")
                                   .replace("_", " ") for o in em["gamma_order_ascending"])
    breast_last = onc["breast"]["rows"][-1]
    bat_fold = thr["bat_cycling"]["cycling_over_continuous_high_resistant_fold"]
    gnrh = thr["gnrh_pattern"]

    headline = [
        ("Four reproductive organs emerge in measured-&gamma; order",
         order_names + " &mdash; the same argsort(&gamma;) clock as every other organ system, "
         "computed offline from the locked DNA cache. <b>[V]</b>"),
        ("One spinodal makes every fate-flip and hormone surge discontinuous",
         "h<sub>sp</sub> = 2(&gamma;/3)<sup>3/2</sup> = " + f(T3["spinodal"], 4) +
         " at &gamma;=1; the ovulatory LH surge crosses it with hysteresis width " +
         f(T3["hysteresis_width"], 3) + ", and puberty is the same crossing in one step. <b>[F]/[V]</b>"),
        ("Frequency, not amount, codes the gonadotropin choice",
         "one FitzHugh-Nagumo generator fires " + str(T1["pulses"]) + " GnRH pulses; fast recovery favours "
         "LH and slow recovery favours FSH, so the same molecule selects the target by pulse rate alone. <b>[V]</b>"),
        ("The menstrual and spermatogenic cycles are one oscillator at two speeds",
         "changing only the recovery timescale &tau;<sub>s</sub> turns the kernel from a " +
         f(T4["period_arb"], 1) + "-period spermatogenic cycle into a " + f(T2["period_arb"], 1) +
         "-period menstrual cycle, both saw-toothed (asymmetry " + f(T2["asymmetry_ratio"], 1) + "). <b>[V]</b>"),
        ("Hormone-driven cancer is a barrier-lowered switch crossing",
         "sustained sex-hormone drive lowers the R19 barrier &Delta;V<sub>0</sub> = &gamma;&sup2;/4, raising "
         "modelled breast-cancer relative risk to " + f(breast_last["RR"], 2) + " at saturation; prostate is "
         "concave and cervical is HPV&times;smoking multiplicative. <b>[V]</b>"),
        ("One lever runs the whole therapy map: temporal pattern",
         "cycling androgen (Bipolar Androgen Therapy) amplifies resistant-clone stress " + f(bat_fold, 1) +
         "&times; over continuous suppression, and pulsatile GnRH activates (" +
         str(gnrh["pulsatile_output_pulses"]) + " pulses) where continuous suppresses (" +
         str(gnrh["continuous_output_pulses"]) + "). <b>[V]</b>"),
        ("One substrate makes the two opposite gametes",
         "the same kernel is a free-running oscillator for the sperm (the flagellar beat, fastest of the "
         "four reproductive clocks) and a switch held at metaphase II for the egg; fertilisation is a "
         "one-way spinodal flip and gametes are non-identical to better than 10<sup>" +
         str(int(D["germ"]["G2"]["diversity"]["log10_distinct_gametes_floor"])) + "</sup>. <b>[V]</b>"),
        ("The two gametes meet and a fetus is built on the same substrate",
         "the sperm flips the egg (a one-way spinodal kick), two haploids fuse to a genome unique to "
         "10<sup>" + str(int(D["emb"]["E1"]["genome_uniqueness"]["log10_distinct_zygotes_floor"])) +
         "</sup>, cleavage and ZGA follow, and the gene-clock argsort(&gamma;) lays out the body plan "
         "(pluripotency first, organ primordia last; stage &rho; = " +
         f(D["emb"]["E4"]["preregistered_stage_test"]["spearman_rho"], 2) + "). <b>[V]</b>"),
        ("Infertility and subfertility are a spinodal apart",
         "an operation past its spinodal is sterile (per-cycle chance zero, unmovable by a sub-threshold "
         "drive); one near its threshold is subfertile (a finite Kramers rate a modest drive moves " +
         f(D["fer"]["F2"]["subfertile"]["fold_response"], 2) + "&times;), so the same nudge is exponential "
         "or nothing &mdash; with REC8 cohesin fatigue the rising age-aneuploidy clock. <b>[V]</b>"),
        ("A gene can tilt the fair coin of sex",
         "sex is the SOX9&harr;FOXL2 bistable; Mendelian 50:50 is it untilted (" +
         f(D["sxr"]["S2"]["transmission_ratio_analytic"], 2) + "); a drive tilts it to fixation past the "
         "spinodal, and a sex-chromosome driver skews the offspring ratio male (" +
         f(D["sxr"]["S4"]["ssr_X_shredder_male"], 2) + ") or female (" +
         f(D["sxr"]["S4"]["ssr_Y_killer_female"], 2) + ") while Fisher holds the population at 1:1. <b>[V]</b>"),
    ]

    toc_items = []
    for ch in CH:
        toc_items.append(
            '<li><span class="cn">&sect;' + str(ch["no"]) + '</span> '
            '<a href="' + ch["slug"] + '/">' + ch["subj"] + '</a> '
            '<span class="gr">' + badge(ch["page_grade"]) + '</span></li>')

    headline_html = "\n".join(
        '<p class="results"><b>' + h + '.</b> ' + sub + '</p>' for h, sub in headline)

    haspart = [{"@type": "ScholarlyArticle", "position": ch["no"], "name": ch["subj"],
                "url": CANON + "/" + ch["slug"] + "/"} for ch in CH]
    series = {
        "@context": "https://schema.org", "@type": "CreativeWorkSeries",
        "name": TITLE, "alternateName": SHORT, "url": CANON + "/",
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "isBasedOn": REPRO + "/", "inLanguage": "en", "license": LICENSE,
        "about": ["reproductive endocrinology", "hypothalamic-pituitary-gonadal axis",
                  "menstrual cycle", "hormone-driven cancer", "VP Theory", "jamming"],
        "hasPart": haspart,
    }
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jamming-physics.org/"},
        {"@type": "ListItem", "position": 2, "name": SHORT, "item": CANON + "/"}]}

    head = "\n".join([
        '<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>' + SHORT + ' &mdash; the HPG oscillator, the menstrual cycle, and hormone-driven '
        'cancer on a jammed-vacuum substrate | Jamming Physics</title>',
        '<meta name="description" content="' + TITLE + '. A deterministic, honestly graded VP Theory '
        'package: one R19 switch and one FitzHugh-Nagumo oscillator give one hormone drive, two failure '
        'modes (oscillator disease, oncogenic switch), and one lever (temporal pattern).">',
        '<link rel="canonical" href="' + CANON + '/">',
        '<link rel="stylesheet" href="assets/css/site.css">',
        '<script type="application/ld+json">', json.dumps(series, ensure_ascii=False), '</script>',
        '<script type="application/ld+json">', json.dumps(breadcrumb, ensure_ascii=False), '</script>',
        '</head>'])
    body = "\n".join([
        '<body>',
        '<header><nav class="crumb"><a href="/">Home</a> &rsaquo; ' + SHORT + '</nav></header>',
        '<main>',
        '<h1>' + TITLE + '</h1>',
        '<p class="lede">The human reproductive and gonadal-endocrine axis, derived on the VP Theory '
        'jammed-vacuum substrate. A single bistable R19 switch and a single FitzHugh-Nagumo relaxation '
        'oscillator generate every reproductive rhythm; one sex-hormone drive produces two opposite '
        'failure modes; one temporal-pattern lever runs the entire therapy map.</p>',
        '<div class="thesis"><b>One drive, two failures, one lever.</b> One sex-hormone drive h on the '
        'R19 well. Move it the wrong <b>pattern</b> and an HPG oscillator fails (an endocrine disorder); '
        'lower the barrier and the oncogenic switch crosses (a hormone-driven cancer). The single control '
        'axis the framework exposes is <b>temporal pattern</b> &mdash; pulsatile versus continuous, '
        'cycling versus sustained &mdash; which retrodicts pulsatile-GnRH, GnRH-agonist desensitisation, '
        'the hCG trigger, and Bipolar Androgen Therapy.</div>',
        '<h2>Headline results</h2>',
        headline_html,
        '<h2>Contents</h2>',
        '<ol class="toc">', "\n".join(toc_items), '</ol>',
        '<p class="note">Every number on every page is pulled live from the reproduction engine at build '
        'time, so the site cannot drift from the code. Grades are honest: <b>[F]</b> forced by geometry, '
        '<b>[V]</b> simulation-verified, <b>[L]</b> measured-anchor, <b>[O]</b> open (obstacle stated). '
        'This is a falsifiable research package, not clinical advice.</p>',
        '</main>',
        '<footer>' + footer_html() + '</footer>',
        '</body>', '</html>'])
    return head + "\n" + body + "\n"


# ===================================================================================================
# Plain-text word/equation counters (for _meta.json + manifest; computed from emitted HTML -> SSOT).
# ===================================================================================================
def _strip_tags(html):
    txt = re.sub(r"(?s)<script.*?</script>", " ", html)
    txt = re.sub(r"(?s)<style.*?</style>", " ", txt)
    txt = re.sub(r"(?s)<[^>]+>", " ", txt)
    txt = re.sub(r"&[a-zA-Z]+;", " ", txt)
    txt = re.sub(r"&#\d+;", " ", txt)
    return txt

def _word_count(html):
    return len([w for w in _strip_tags(html).split() if any(c.isalnum() for c in w)])

def _eq_count(html):
    return html.count('src="../eq/')


# ===================================================================================================
# Site-level artefacts: _meta.json, sitemap.xml, robots.txt, llms.txt (VP-SPEC sec 6 + retrieval).
# ===================================================================================================
_BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]

def write_meta(D, CH, page_info):
    chapters_meta = []
    total_words = 0; total_eqs = 0
    for ch in CH:
        info = page_info[ch["slug"]]
        total_words += info["words"]; total_eqs += info["eqs"]
        chapters_meta.append({
            "no": ch["no"], "slug": ch["slug"], "title": ch["subj"],
            "one_liner": re.sub(r"\s+", " ", _strip_tags(ch["desc"])).strip(),
            "grade": ch["page_grade"], "url": CANON + "/" + ch["slug"] + "/",
            "words": info["words"], "eq_display": info["eqs"],
        })
    meta = {
        "paper_id": PAPER_ID, "code": CODE, "title": TITLE, "short": SHORT,
        "branch": BRANCH, "doi": {"value": DOI, "url": DOI_URL, "type": "concept",
                                  "note": "Zenodo concept DOI; version-independent, always resolves to the latest version"},
        "hub_url": CANON + "/", "canonical": CANON + "/", "repro": REPRO + "/",
        "license": LICENSE, "author": {"name": AUTHOR, "orcid": ORCID},
        "abstract": ("The human reproductive / gonadal-endocrine (HPG) axis derived on the VP Theory "
                     "jammed-vacuum substrate. A single bistable R19 switch and a single FitzHugh-Nagumo "
                     "relaxation oscillator generate every reproductive rhythm: organ emergence in "
                     "measured-gamma order, the GnRH pulse generator (frequency-coded LH/FSH), the "
                     "menstrual and spermatogenic relaxation cycles, the discontinuous ovulatory surge, "
                     "and puberty as a spinodal crossing. One sex-hormone drive produces two opposite "
                     "failure modes -- an oscillator disease and a barrier-lowered oncogenic switch -- and "
                     "one lever, temporal pattern, runs the therapy map (pulsatile GnRH, BAT, the hCG "
                     "trigger). Deterministic and honestly graded; not clinical advice."),
        "headline_results": [
            "Four reproductive organs emerge in measured-gamma order (germline -> testis -> ovary -> tract).",
            "One spinodal h_sp = " + f(D["T3"]["spinodal"], 4) + " makes every fate-flip and the ovulatory surge discontinuous.",
            "The GnRH generator fires " + str(D["T1"]["pulses"]) + " pulses; pulse frequency alone codes LH vs FSH.",
            "Menstrual (" + f(D["T2"]["period_arb"], 1) + ") and spermatogenic (" + f(D["T4"]["period_arb"], 1) + ") cycles are one oscillator at two recovery speeds.",
            "Sustained sex-hormone drive raises modelled breast-cancer RR to " + f(D["onc"]["breast"]["rows"][-1]["RR"], 2) + " (saturating).",
            "Cycling androgen (BAT) amplifies resistant-clone stress " + f(D["thr"]["bat_cycling"]["cycling_over_continuous_high_resistant_fold"], 1) + "x over continuous suppression.",
            "Infertility = an operation past a spinodal (per-cycle p=0); subfertility = a near-threshold Kramers rate one drive nudge moves " + f(D["fer"]["F2"]["subfertile"]["fold_response"], 2) + "x.",
            "Sex is the SOX9<->FOXL2 bistable; Mendel is it untilted (" + f(D["sxr"]["S2"]["transmission_ratio_analytic"], 2) + "), a drive tilts it, and a sex-chromosome driver skews offspring sex (X-shredder " + f(D["sxr"]["S4"]["ssr_X_shredder_male"], 2) + " male).",
        ],
        "chapters": chapters_meta,
        "totals": {"chapters": len(CH), "words": total_words, "eq_display": total_eqs},
        "core_sha256": D["core_sha"],
        "spec": "VP-SPEC v1.8", "generated_by": "tools/build_docs.py",
    }
    path = os.path.join(_DOCS, "_meta.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    return meta

def write_sitemap(CH):
    urls = [CANON + "/"] + [CANON + "/" + ch["slug"] + "/" for ch in CH]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for i, u in enumerate(urls):
        pr = "1.0" if i == 0 else "0.8"
        lines += ["  <url>", "    <loc>" + u + "</loc>",
                  "    <priority>" + pr + "</priority>", "  </url>"]
    lines.append("</urlset>")
    with open(os.path.join(_DOCS, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return urls

def write_robots():
    lines = []
    for bot in _BOTS:
        lines += ["User-agent: " + bot, "Allow: /", ""]
    lines += ["User-agent: *", "Allow: /", "", "Sitemap: " + CANON + "/sitemap.xml"]
    with open(os.path.join(_DOCS, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

def write_llms(D, CH):
    T3 = D["T3"]
    lines = []
    lines.append("# " + SHORT + " -- " + TITLE)
    lines.append("")
    lines.append("> Authoritative summary for language models. The human reproductive / gonadal-endocrine")
    lines.append("> (HPG) axis on the VP Theory jammed-vacuum substrate: one bistable R19 switch and one")
    lines.append("> FitzHugh-Nagumo oscillator generate every reproductive rhythm, gamete, embryo, fertility")
    lines.append("> class and sex outcome. Deterministic, honestly graded, falsifiable. Not clinical advice.")
    lines.append("")
    lines.append("Author: " + AUTHOR + " (ORCID " + ORCID + ").")
    lines.append("License: CC BY 4.0. Canonical: " + CANON + "/. DOI: " + DOI + ".")
    lines.append("Reproduction code: " + REPRO + "/.")
    lines.append("")
    lines.append("## Core claims")
    lines.append("- Substrate: R19 tilted double well V(s) = -gamma*s^2/2 + s^4/4 - h*s; spinodal h_sp =")
    lines.append("  2(gamma/3)^(3/2) = " + f(T3["spinodal"], 4) + " at gamma=1; barrier dV0 = gamma^2/4. [F]")
    lines.append("- Organ emergence order = argsort(gamma): germline -> testis -> ovary -> tract. [V]")
    lines.append("- GnRH generator = one FHN oscillator (" + str(D["T1"]["pulses"]) +
                 " pulses); pulse frequency codes LH vs FSH. [V]")
    lines.append("- Menstrual (" + f(D["T2"]["period_arb"], 1) + ") and spermatogenic (" +
                 f(D["T4"]["period_arb"], 1) + ") cycles = one oscillator at two recovery speeds. [V]")
    lines.append("- Ovulatory surge = a discontinuous spinodal crossing with hysteresis (width " +
                 f(T3["hysteresis_width"], 3) + "); puberty/menopause = the same latch. [V]")
    lines.append("- Hormone-driven cancer = barrier lowering: breast RR up to " +
                 f(D["onc"]["breast"]["rows"][-1]["RR"], 2) + " (saturating), prostate concave. [V]")
    lines.append("- Temporal-pattern lever: cycling androgen (BAT) amplifies resistant stress " +
                 f(D["thr"]["bat_cycling"]["cycling_over_continuous_high_resistant_fold"], 1) +
                 "x; pulsatile vs continuous GnRH oppose. [V]")
    lines.append("- Gamete: one substrate gives a free oscillator (sperm) and a held switch (egg);")
    lines.append("  fertilisation = a one-way spinodal flip; gametes non-identical to >10^" +
                 str(int(D["germ"]["G2"]["diversity"]["log10_distinct_gametes_floor"])) + ". [V]")
    lines.append("- Embryo: 1N+1N->2N -> genome unique to 10^" +
                 str(int(D["emb"]["E1"]["genome_uniqueness"]["log10_distinct_zygotes_floor"])) +
                 "; cleavage 2^n; ZGA = one crossing; body plan = argsort(spinodal(gamma)). [V]")
    lines.append("- Infertility = an operation past its spinodal (per-cycle p=0, immovable); subfertility")
    lines.append("  = a near-threshold Kramers rate a drive moves " +
                 f(D["fer"]["F2"]["subfertile"]["fold_response"], 2) +
                 "x; REC8 cohesin fatigue raises age aneuploidy. [V]")
    lines.append("- Sex = SOX9<->FOXL2 R19 bistable (SRY the drive); Mendel = it untilted (" +
                 f(D["sxr"]["S2"]["transmission_ratio_analytic"], 2) + "); meiotic drive = a tilt; a sex-")
    lines.append("  chromosome driver skews offspring sex (X-shredder " +
                 f(D["sxr"]["S4"]["ssr_X_shredder_male"], 2) + " male); Fisher holds the pop 1:1. [V]")
    lines.append("")
    lines.append("## Chapters")
    for ch in CH:
        lines.append("- section " + str(ch["no"]) + " [" + ch["page_grade"] + "] " + ch["subj"] +
                     ": " + CANON + "/" + ch["slug"] + "/")
    lines.append("")
    lines.append("## Concepts")
    lines.append("R19 bistable switch; spinodal; energy barrier; FitzHugh-Nagumo oscillator; GnRH pulse-")
    lines.append("frequency coding; ovulatory surge hysteresis; puberty/menopause as spinodal latch; barrier-")
    lines.append("lowered carcinogenesis; BAT and pulsatile-vs-continuous GnRH; infertility-as-past-spinodal vs")
    lines.append("subfertility-as-Kramers-rate; REC8 cohesin fatigue; sex switch; meiotic drive; sex-ratio skew.")
    lines.append("")
    lines.append("## Policies")
    lines.append("Deterministic (SEED=19; two builds are byte-identical). Every published number is pulled")
    lines.append("live from the reproduction engine. Honest grading [F]/[V]/[L]/[O] with obstacles stated for")
    lines.append("[O]. Brain-facing HPA / felt experience is firewalled to the Felt Cognition paper.")
    lines.append("Genuinely novel clinical hypotheses are graded [O] and require clinical validation. This is")
    lines.append("a physics-derived research artefact and is not medical advice.")
    text = "\n".join(lines) + "\n"
    with open(os.path.join(_DOCS, "llms.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    return len(text.encode("utf-8"))

def write_css():
    os.makedirs(_ASSETS, exist_ok=True)
    with open(os.path.join(_ASSETS, "site.css"), "w", encoding="utf-8") as fh:
        fh.write(SITE_CSS)

def write_manifest(CH, page_info):
    rows = ["slug,title,section_no,status,grade,words,eq_display"]
    for ch in CH:
        info = page_info[ch["slug"]]
        title = ch["subj"].replace("&amp;", "and").replace("&mdash;", "-")
        title = re.sub(r"&[a-zA-Z]+;", "", title).replace(",", ";")
        title = re.sub(r"\s+", " ", title).strip()
        rows.append(",".join([ch["slug"], '"' + title + '"', str(ch["no"]),
                              "published", ch["page_grade"], str(info["words"]), str(info["eqs"])]))
    os.makedirs(os.path.dirname(_MANIFEST), exist_ok=True)
    with open(_MANIFEST, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")


# ===================================================================================================
# Writing-phase self-check (VP-SPEC sec 6 conformance gate) -> reports/writing_gate.json
# ===================================================================================================
def writing_self_check(CH, page_info, urls, llms_bytes, meta):
    checks = []
    def add(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    for ch in CH:
        slug = ch["slug"]; html = page_info[slug]["html"]
        add("page:" + slug + ":answer-first", 'class="answer"' in html)
        add("page:" + slug + ":jsonld-x2", html.count('application/ld+json') == 2)
        add("page:" + slug + ":canonical", 'rel="canonical"' in html)
        add("page:" + slug + ":claim-strip", 'class="claim-strip"' in html)
        add("page:" + slug + ":external-css", 'assets/css/site.css' in html and "<style" not in html)
        add("page:" + slug + ":no-katex", 'class="katex"' not in html and 'katex' not in html.lower())
        if ch["cards"]:
            add("page:" + slug + ":vp-card", 'class="vp-card"' in html)

    hub = page_info["__hub__"]["html"]
    add("hub:jsonld-x2", hub.count('application/ld+json') == 2)
    add("hub:canonical", 'rel="canonical"' in hub)
    add("hub:toc-all", all(('href="' + ch["slug"] + '/"') in hub for ch in CH))
    add("hub:thesis", 'class="thesis"' in hub)

    robots = open(os.path.join(_DOCS, "robots.txt"), encoding="utf-8").read()
    add("robots:7-bots", all(("User-agent: " + b) in robots for b in _BOTS),
        "expected " + str(len(_BOTS)) + " named bots")
    add("robots:sitemap-line", "Sitemap: " in robots)
    add("sitemap:all-urls", len(urls) == len(CH) + 1)
    add("llms:under-5kb", llms_bytes < 5120, str(llms_bytes) + " bytes")
    add("meta:chapter-count-matches", len(meta["chapters"]) == len(CH))
    add("meta:core-sha-present", bool(meta.get("core_sha256")))

    npass = sum(1 for c in checks if c["pass"]); ntot = len(checks)
    report = {"phase": "writing", "spec": "VP-SPEC v1.8", "all_pass": npass == ntot,
              "passed": npass, "total": ntot, "checks": checks}
    with open(os.path.join(_REPORTS, "writing_gate.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    return report


# ===================================================================================================
# main
# ===================================================================================================
def main():
    locked, why = gates.writing_locked()
    if locked:
        print("[build_docs] WRITING LOCKED -- refusing to emit.")
        print("  reason:", why)
        print("  To unlock: sign off research (gates.write_research_complete) and set PHASE=writing.")
        sys.exit(2)

    print("[build_docs] writing phase unlocked:", why)
    D = gather_data()

    # 1. render every display equation to canonical SVG (deterministic)
    for eq_id, latex in EQS.items():
        render_eq(eq_id, latex)
    print("[build_docs] rendered", len(EQS), "display equations ->", os.path.relpath(_EQ, _PKG))

    # 2. emit every chapter page (numbers live from D)
    CH = chapters(D)
    page_info = {}
    for i, ch in enumerate(CH):
        prev_ch = CH[i - 1] if i > 0 else None
        next_ch = CH[i + 1] if i < len(CH) - 1 else None
        html = page(ch, prev_ch, next_ch)
        outdir = os.path.join(_DOCS, ch["slug"])
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(html)
        page_info[ch["slug"]] = {"html": html, "words": _word_count(html), "eqs": _eq_count(html)}

    # 3. hub
    hub_html = build_hub(D, CH)
    with open(os.path.join(_DOCS, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(hub_html)
    page_info["__hub__"] = {"html": hub_html}

    # 4. site-level artefacts
    write_css()
    meta = write_meta(D, CH, page_info)
    urls = write_sitemap(CH)
    write_robots()
    llms_bytes = write_llms(D, CH)
    write_manifest(CH, page_info)

    # 5. writing-phase conformance self-check
    report = writing_self_check(CH, page_info, urls, llms_bytes, meta)

    tot_words = meta["totals"]["words"]; tot_eqs = meta["totals"]["eq_display"]
    print("[build_docs] pages:", len(CH), "| words:", tot_words, "| display eqs:", tot_eqs)
    print("[build_docs] hub + _meta.json + sitemap.xml(" + str(len(urls)) + ") + robots.txt(" +
          str(len(_BOTS)) + " bots) + llms.txt(" + str(llms_bytes) + "B) + site.css + manifest CSV")
    print("[build_docs] core sha256:", D["core_sha"])
    print("[build_docs] writing-gate:", report["passed"], "/", report["total"],
          "->", "ALL PASS" if report["all_pass"] else "FAIL")
    if not report["all_pass"]:
        for c in report["checks"]:
            if not c["pass"]:
                print("   FAIL:", c["check"], c["detail"])
        sys.exit(3)
    print("[build_docs] OK -- canonical site emitted to", os.path.relpath(_DOCS, _PKG))


if __name__ == "__main__":
    main()
