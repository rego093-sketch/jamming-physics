#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Circulatory Transport WRITING phase: per-title canonical SEO HTML generator.

HARD RULE: refuses while gates.writing_locked() is True (research-first). When UNLOCKED it emits,
per VP-SPEC v1.8 (sections 6 / 6-R / 9 / 11):
  docs/<slug>/index.html  per-section page (answer-first, JSON-LD ScholarlyArticle + BreadcrumbList,
                          claim-strip, vp-card per cited locked quantity);
  docs/index.html         volume hub (CreativeWorkSeries);
  docs/<paper>/_meta.json summary card (section 9);
  docs/sitemap.xml ; docs/robots.txt (7 bots) ; docs/llms.txt (<5KB);
  docs/eq/<paper>/cir-<sec>-<nnn>.svg  rendered display equations (alt = LaTeX, C2 / 7-B);
  docs/assets/css/site.css  external stylesheet (no inline CSS) ;
  manifest/circulatory_vp_site.csv  deterministic slug index (section 3).
All numbers are REGENERATED from the engine at build time (C1). Body English (C0); grades [F]/[V]/[L]/[O] (C3).
"""
import os, sys, json, re, unicodedata, html

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.join(_HERE, "..")
for p in ("repro/_verify", "repro/_engine", "repro/_oncology", "inherited"):
    sys.path.insert(0, os.path.join(_PKG, p))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import importlib
gates = importlib.import_module("gates")

def _load_publication():
    """Single-source publication identifiers from manifest/publication.json (handoff item 6).
    A missing file or a null doi yields pending behaviour, byte-identical to the pre-DOI build."""
    try:
        p = json.load(open(os.path.join(_PKG, "manifest", "publication.json"), encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        p = {}
    cvr = p.get("cross_volume_registry") or {}
    return {"doi": p.get("doi"), "concept_doi": p.get("concept_doi"),
            "cross_volume_doi": cvr.get("cross_volume_doi"), "status": p.get("status", "pending")}
_PUB = _load_publication()

PAPER = {
    "paper_id": "circulatory_vp_site", "code": "cir", "short": "Circulatory Transport",
    "title": ("Circulatory Transport and Clearance: Hemodynamics, Renal Filtration, "
              "and Hepatic Clearance from the Jamming Substrate"),
    "branch": "jamming (pressure-flow + clearance)",
    "doi": _PUB["doi"], "concept_doi": _PUB["concept_doi"],
    "cross_volume_doi": _PUB["cross_volume_doi"], "pub_status": _PUB["status"],
    "author": "Young Jae Lee", "orcid": "https://orcid.org/0009-0002-7535-8245",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "domain": "https://jamming-physics.org", "repo": "https://github.com/rego093-sketch/jamming-physics",
    "version": open(os.path.join(_PKG, "VERSION"), encoding="utf-8").read().strip(),
}
STOPWORDS = {"the", "a", "an", "of", "and", "as", "its", "for", "to", "in", "on", "with", "from"}

def slugify(num, title):
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    words = [w for w in t.split("-") if w and w not in STOPWORDS][:5]
    return "%02d-%s" % (num, "-".join(words))

# Retrieval keywords per section (VP-SPEC v1.8 C4: machine-facing fact layer for generative
# search fan-out). Emitted as <meta name="keywords"> and as schema.org knowsAbout[] on every
# chapter. These are the search phrases a cold reader would type; they do not alter the body.
SECTION_KEYWORDS = {
    1:  ["organ emergence from DNA", "master gene gamma", "SIX2 kidney", "HHEX liver",
         "nearest-neighbour stacking energy", "SantaLucia 1998", "promoter thermodynamics",
         "developmental order spinodal", "bistable cell-fate switch", "jamming lattice substrate"],
    2:  ["mean arterial pressure formula", "MAP = CO x SVR", "cardiac output systemic vascular resistance",
         "hydraulic Ohm law", "hemodynamics", "Windkessel boundary condition", "blood pressure derivation"],
    3:  ["Windkessel model", "diastolic pressure decay", "time constant RC", "arterial compliance",
         "aortic pressure waveform", "two-element Windkessel", "pulse pressure", "tau = R x C"],
    4:  ["glomerular filtration rate", "GFR autoregulation", "tubuloglomerular feedback", "Starling forces",
         "renal blood flow", "afferent arteriole", "glomerular capillary pressure", "kidney filtration plateau"],
    5:  ["osmoregulation", "plasma osmolality setpoint", "ADH vasopressin", "thirst water balance",
         "antidiuretic hormone loop", "287 mOsm/kg", "negative feedback osmostat", "body water regulation"],
    6:  ["hepatic clearance", "oral bioavailability", "first-pass metabolism", "well-stirred model",
         "extraction ratio E", "F = 1 - E", "propranolol pharmacokinetics", "flow-limited capacity-limited"],
    7:  ["carcinogenesis mechanism", "R19 bistable switch", "barrier lowering", "Kramers escape rate",
         "Arrhenius relative risk", "cell-fate transition", "spinodal collapse", "dose-response model"],
    8:  ["renal cell carcinoma smoking risk", "RCC dose response", "tobacco kidney cancer relative risk",
         "trichloroethylene", "carcinogen saturation", "Hunt 2005", "monotone saturating RR"],
    9:  ["hepatocellular carcinoma", "aflatoxin hepatitis B synergy", "aflatoxin B1 HBV multiplicative risk",
         "liver cancer relative risk", "multiplicative synergy", "parameter-free synergy", "Qian 1994"],
    10: ["arterial stiffening", "isolated systolic hypertension", "pulse pressure widening",
         "aortic compliance loss", "ISH SBP 140", "Franklin 1997", "aging arteries hemodynamics"],
    11: ["essential hypertension", "systemic vascular resistance rise", "resistance-driven blood pressure",
         "MAP = CO x SVR", "JNC7 ACC-AHA 140/90", "primary hypertension mechanism"],
    12: ["hypotension shock subtypes", "hypovolemic shock", "distributive shock", "MAP below 65",
         "Surviving Sepsis", "cardiac output drop", "vasodilatory shock", "SEPSISPAM"],
    13: ["diabetes insipidus", "ADH deficiency", "failed osmostat", "hypernatremia", "water deficit",
         "central nephrogenic DI", "uncorrected osmolality", "vasopressin loss"],
    14: ["SIADH", "syndrome of inappropriate antidiuretic hormone", "dilutional hyponatremia",
         "low plasma sodium", "inappropriate antidiuresis", "Verbalis 2013", "defended osmolality shift"],
    15: ["chronic kidney disease", "CKD GFR staging", "KDIGO stages", "nephron loss", "remaining nephron fraction",
         "G1 G2 G3 G4 G5", "90 60 45 30 15 GFR", "renal failure progression"],
    16: ["autoregulation breakthrough", "glomerular hypertension", "renal barotrauma", "GFR ceiling",
         "afferent arteriole maximal dilation", "perfusion pressure overload", "hyperfiltration"],
    17: ["hepatic impairment dose reduction", "cirrhosis pharmacokinetics", "Child-Pugh dosing",
         "high extraction drug exposure", "reduced intrinsic clearance", "first-pass loss", "drug dosing liver disease"],
    18: ["portosystemic shunt", "first-pass escape", "TIPS bioavailability", "portal bypass",
         "shunt fraction F = 1-(1-s)E", "high extraction drug shunt", "varices portal hypertension"],
    19: ["drug-drug interaction", "enzyme induction inhibition", "CYP450 clearance", "intrinsic clearance change",
         "flow-limited capacity-limited DDI", "CLint elasticity", "bioavailability interaction"],
    20: ["cancer reversibility threshold", "differentiation therapy", "spinodal responder boundary",
         "critical slowing down", "saddle-node exponent one half", "pre-malignant reversion", "relapse-prone lesion"],
    21: ["cancer prevention leverage", "de-escalation", "carcinogen removal divides risk", "barrier restoration",
         "exponential prevention benefit", "multiplicative risk reduction", "Kramers suppression"],
    22: ["renal cancer carcinogen roster", "kidney cancer prevention", "tobacco trichloroethylene aristolochic acid",
         "VHL HIF pathway", "von Hippel-Lindau", "RCC risk factors", "upper-tract urothelial carcinoma"],
    23: ["liver cancer carcinogen roster", "HCC prevention", "aflatoxin HBV HCV ethanol", "HBV HCV coinfection",
         "hemochromatosis HFE HCC", "hepatitis B vaccine prevention", "multiplicative synergy bracket"],
}

def keywords_csv(no):
    return ", ".join(SECTION_KEYWORDS.get(no, []))

def knows_about_json(no):
    return json.dumps(SECTION_KEYWORDS.get(no, []))

def write_eq_svg(docs, code, sec_code, idx, latex_alt, unicode_text):
    eqdir = os.path.join(docs, "eq", PAPER["paper_id"]); os.makedirs(eqdir, exist_ok=True)
    fname = "%s-%s-%03d.svg" % (code, sec_code, idx)
    fp = 22; w = max(140, int(len(unicode_text) * fp * 0.6) + 32); h = int(fp * 2.4)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
           'role="img" aria-label="%s">\n  <title>%s</title>\n'
           '  <text x="16" y="%d" font-family="Cambria, \'Times New Roman\', Georgia, serif" '
           'font-size="%d" font-style="italic" fill="#16202c">%s</text>\n</svg>\n') % (
        w, h, w, h, html.escape(latex_alt, quote=True), html.escape(latex_alt),
        int(h * 0.66), fp, html.escape(unicode_text))
    open(os.path.join(eqdir, fname), "w", encoding="utf-8").write(svg)
    return "/eq/%s/%s" % (PAPER["paper_id"], fname), w, h, latex_alt

def gather():
    eng = importlib.import_module("vp_cir_engine")
    onco = importlib.import_module("carcinogen_dose_response")
    stress = importlib.import_module("stress_tests")
    c = eng.circulate(); rcc = onco.rcc_smoking_doseresponse(); hcc = onco.hcc_aflatoxin_hbv_synergy()
    _, sha = eng.emit(c)
    dis = {s["target"]: s["value"] for s in stress.run_battery()["suites"]}
    return {"c": c, "rcc": rcc, "hcc": hcc, "sha": sha, "dis": dis}

def grade_class(t):
    return {"F": "g-forced", "V": "g-verified", "H": "g-hypothesis", "L": "g-calibrated", "O": "g-open"}.get(t, "g-forced")
def grade_label(t):
    return {"F": "[F] forced", "V": "[V] simulation-verified", "H": "[H] hypothesis",
            "L": "[L] literature-cited", "O": "[O] open"}.get(t, "[F] forced")
def vp_card(dl, head, meaning, t, href):
    return ('<aside class="vp-card" data-locked="%s"><b>%s</b> — %s <b>%s</b> '
            '<a href="%s">canonical derivation</a></aside>') % (dl, head, meaning, grade_label(t), href)
def eq_fig(src, w, h, alt):
    return ('<figure class="eq"><img src="%s" width="%d" height="%d" loading="lazy" alt="%s"></figure>') % (
        src, w, h, html.escape(alt, quote=True))

def xref_block(rec):
    """Render a structured cross-volume gene-key reference (owned by a sibling volume, NOT re-emerged
    here) as a labelled aside. Source: inherited/cross_references.json (single source of truth)."""
    mag = ""
    m = rec.get("anchor_magnitude")
    if m and "HR_male_C282Y_homozygote" in m:
        mag = (" Cited magnitude: hazard ratio %.1f (95%% CI %.1f&ndash;%.1f) for male homozygotes, "
               "lifetime hepatic-malignancy risk %.1f%% vs %.1f%%." % (
                   m["HR_male_C282Y_homozygote"], m["HR_CI95"][0], m["HR_CI95"][1],
                   m["lifetime_risk_to_75_pct"], m["baseline_risk_pct"]))
    return ('<aside class="xref-card" role="note">'
            '<b>Cross-volume reference &middot; %s.</b> Gene-key <code>%s</code> (%s), owned by '
            '<code>%s</code> &mdash; <em>not re-emerged here</em> (%s). %s%s '
            '<b>Seam to this volume:</b> %s '
            '<span class="xref-grade">%s</span> '
            '<span class="xref-cite">Anchor: %s</span></aside>') % (
        html.escape(rec["entity"]), html.escape(rec["gene_key"]), html.escape(rec["locus"]),
        html.escape(rec["owner_volume"]), html.escape(rec["ownership_clause"].split(" -- ")[0]),
        html.escape(rec["mechanism"]), mag, html.escape(rec["seam_to_circulatory"]),
        html.escape(rec["grade"]), html.escape(rec["anchor"]))

def build_sections(D, docs):
    c = D["c"]; hemo = c["hemodynamics"]; ren = c["renal"]; osm = c["osmoregulation"]; hep = c["hepatic"]
    organs = {o["organ"]: o for o in c["organs"]["organs"]}
    rcc = D["rcc"]["value"]; hcc = D["hcc"]["value"]; mA = hcc["modelA_additive_decrements"]
    dis = D["dis"]
    pid = PAPER["paper_id"]; code = PAPER["code"]
    gK = organs["kidney"]["gamma"]; gL = organs["liver"]["gamma"]
    szK = organs["kidney"]["rel_size_dwell"]; szL = organs["liver"]["rel_size_dwell"]
    GAMMA_SRC = PAPER["domain"] + "/dna/"
    R19_SRC = "/%s/%s/" % (pid, slugify(7, "Carcinogenesis as R19 barrier lowering"))
    CARD_GK = vp_card("gamma-six2", "&gamma;(SIX2) = 1.5556",
        "kidney master-gene NN-stacking energy (SantaLucia 1998); measured read-only, never fitted.", "V", GAMMA_SRC)
    CARD_GL = vp_card("gamma-hhex", "&gamma;(HHEX) = 1.525",
        "liver master-gene NN-stacking energy; measured read-only, never fitted.", "V", GAMMA_SRC)
    CARD_R19 = vp_card("r19", "R19 switch  ds/dt = &gamma;s &minus; s&sup3; + h",
        "shared jamming/DNA/neuron bistable cell-fate switch; barrier &gamma;&sup2;/4, spinodal 2(&gamma;/3)^1.5.", "F", R19_SRC)
    # --- intra-volume locked relations the disease sections (T8-T17) perturb (restate value+meaning+grade+link) ---
    SLUG_MAP = "/%s/%s/" % (pid, slugify(2, "Arterial pressure: MAP = CO \u00d7 SVR"))
    SLUG_TAU = "/%s/%s/" % (pid, slugify(3, "Windkessel diastolic decay \u03c4 = R \u00d7 C"))
    SLUG_GFR = "/%s/%s/" % (pid, slugify(4, "Glomerular filtration and autoregulation plateau"))
    SLUG_OSM = "/%s/%s/" % (pid, slugify(5, "Osmoregulation and the ADH thirst loop"))
    SLUG_HEP = "/%s/%s/" % (pid, slugify(6, "Hepatic clearance and oral bioavailability"))
    CARD_MAP = vp_card("map-ohm", "MAP &minus; CVP = CO &times; SVR",
        "mean arterial pressure is pump flow times downstream resistance (hydraulic Ohm law), derived on-page in &sect;2.", "F", SLUG_MAP)
    CARD_TAU = vp_card("wk-tau", "&tau; = R &times; C",
        "the Windkessel diastolic decay constant is resistance times arterial compliance (&sect;3).", "F", SLUG_TAU)
    CARD_GFR = vp_card("gfr-starling", "GFR = K_f (P_GC &minus; P_BS &minus; &pi;_GC)",
        "glomerular filtration is the Starling drive held flat by tubuloglomerular feedback over 80&ndash;180 mmHg (&sect;4).", "V", SLUG_GFR)
    CARD_OSM = vp_card("osm-setpoint", "Osm setpoint &asymp; 287 mOsm/kg",
        "plasma osmolality is defended to a setpoint by the ADH/thirst negative-feedback loop (&sect;5).", "V", SLUG_OSM)
    CARD_HEP = vp_card("hep-f", "E = f_u CL_int/(Q_H + f_u CL_int),  F = 1 &minus; E",
        "well-stirred hepatic extraction sets oral bioavailability F = 1 &minus; E (&sect;6).", "F", SLUG_HEP)
    S = []

    e = write_eq_svg(docs, code, "01", 1,
        r"s_{spin}(\gamma)=2(\gamma/3)^{3/2},\quad DWELL\propto\gamma^{3/2}",
        "s_spin(\u03b3) = 2(\u03b3/3)^{3/2} ,   DWELL \u221d \u03b3^{3/2}")
    S.append({"no":1,"title":"Organ emergence from measured \u03b3","short":"Organ emergence from measured \u03b3","tok":"V",
        "answer":("The kidney, liver and vasculature emerge as one transport\u2013clearance network from measured "
            "master-gene stacking energies \u03b3 (SIX2 \u03b3=1.5556, HHEX \u03b3=1.525), never fitted. The shared R19 "
            "spinodal orders them in developmental time \u2014 liver before kidney \u2014 and DWELL \u221d \u03b3^1.5 sets "
            "relative size. Grade [V]; absolute size [O]."),
        "abstract":("Organ identity and order are cited from the DNA morphogenesis gene-clock (grade [V], measured "
            "\u03b3). The functional spinodal s_spin = 2(\u03b3/3)^1.5 gives the ON-threshold order liver\u2192kidney; "
            "DWELL \u221d \u03b3^1.5 sets relative sizes (kidney %.3f vs liver %.3f)." % (szK, szL)),
        "cards":[CARD_GK, CARD_GL, CARD_R19],
        "body":("<h2>Organs are read out from \u03b3, not fitted</h2>"
            "<p>This is not a hand-tuned physiology model. Each organ is the same R19 bistable cell-fate switch "
            "whose threshold scale is set by a quantity \u03b3 measured directly from the organism's own DNA: the "
            "mean nearest-neighbour base-stacking free energy (SantaLucia 1998 thermodynamics) of the master "
            "gene's proximal promoter, read from the exact human reference sequence. The kidney master gene "
            "<b>SIX2</b> (chromosome 2, NCBI <code>NC_000002.12</code>) gives \u03b3=%.4f; the liver master gene "
            "<b>HHEX</b> (chromosome 10, NCBI <code>NC_000010.11</code>) gives \u03b3=%.3f. These values are "
            "read-only measurements \u2014 never fitted, never nudged to make an answer come out \u2014 and they "
            "reproduce offline bit-for-bit from a cached promoter window (TSS\u22122000..+500).</p>"
            "<p>Organ identity and developmental order are owned by the DNA morphogenesis gene-clock (a separate "
            "VP volume, grade [V]); this volume cites them and adds the functional dynamics. The chain is fully "
            "mechanical: a measured promoter energy \u03b3 sets a switch threshold, the threshold fixes which "
            "organ appears and when, and from that emerged organ the entire downstream network \u2014 hemodynamics, "
            "renal filtration, osmoregulation, hepatic clearance, fourteen named disease states, drug "
            "pharmacokinetics, and a carcinogenesis kernel \u2014 follows without any free biological parameter.</p>"
            "<p>The functional spinodal \u2014 the drive needed to switch an organ ON \u2014 is s_spin = 2(\u03b3/3)^1.5. "
            "Because \u03b3(SIX2) &gt; \u03b3(HHEX), the liver crosses threshold before the kidney, fixing developmental "
            "order as a pure \u03b3 readout rather than an assumption.</p>%s"
            "<h3>Relative size, not absolute</h3>"
            "<p>DWELL \u221d \u03b3^1.5 sets relative organ size (kidney %.3f, liver %.3f in dwell units). Order and "
            "direction are forced [F]; the absolute magnitude needs one external growth-duration constant and is "
            "logged honestly as [O] in the irreproducibility ledger rather than fitted.</p>" % (gK, gL, eq_fig(*e), szK, szL)),
        "eq_inline":4,"eq_display":1})

    e = write_eq_svg(docs, code, "02", 1, r"MAP-CVP=CO\times SVR", "MAP \u2212 CVP = CO \u00d7 SVR")
    S.append({"no":2,"title":"Arterial pressure: MAP = CO \u00d7 SVR","short":"Arterial pressure: MAP = CO\u00d7SVR","tok":"F",
        "answer":("Mean arterial pressure emerges as MAP = CO \u00d7 SVR from the cardiac pump boundary condition. The "
            "engine returns MAP \u2248 %.1f mmHg (SBP %.0f / DBP %.0f, pulse pressure %.0f) inside the cited resting "
            "human band, and the Ohm pressure\u2013flow relation holds across a wide CO\u00d7SVR grid. Grade [F]; absolute "
            "CO [L]." % (hemo["MAP_mmHg"], hemo["SBP_mmHg"], hemo["DBP_mmHg"], hemo["PP_mmHg"])),
        "abstract":("Treating the circulation as a resistive transport network, mean pressure is pump flow times "
            "downstream resistance: MAP \u2212 CVP = CO \u00d7 SVR. From the pump BC the engine reports MAP \u2248 %.1f mmHg "
            "with SBP/DBP \u2248 %.0f/%.0f mmHg." % (hemo["MAP_mmHg"], hemo["SBP_mmHg"], hemo["DBP_mmHg"])),
        "cards":[],
        "body":("<h2>Pressure is flow times resistance</h2>"
            "<p>The vasculature is the transport class: a pressure-driven flow network with no single master gene. "
            "Its steady operating point is the hydraulic Ohm law MAP \u2212 CVP = CO \u00d7 SVR, driven entirely by the "
            "cardiac-output boundary condition.</p>%s"
            "<p>Across a cardiac-output \u00d7 resistance grid the relation holds to better than 1%%, and the resting "
            "point lands at MAP \u2248 %.1f mmHg \u2014 within the cited 85\u2013100 mmHg band. The pulse pressure %.0f mmHg "
            "follows from stroke volume against arterial compliance (next section).</p>"
            % (eq_fig(*e), hemo["MAP_mmHg"], hemo["PP_mmHg"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "03", 1, r"P(t)=P_0 e^{-t/RC},\quad \tau=RC",
        "P(t) = P\u2080 e^{\u2212t/RC} ,   \u03c4 = R\u00b7C")
    S.append({"no":3,"title":"Windkessel diastolic decay \u03c4 = R \u00d7 C","short":"Windkessel decay \u03c4 = R\u00d7C","tok":"F",
        "answer":("The two-element Windkessel makes aortic pressure decay exponentially in diastole with time "
            "constant \u03c4 = R \u00d7 C. The engine measures \u03c4 \u2248 %.2f s by a log-linear fit of the diastolic segment, "
            "matching the analytic R\u00d7C product (%.2f s) and the cited human aortic value (~1.5 s). Compliance buffers "
            "pulsatile flow into perfusion. Grade [F]/[L]." % (hemo["tau_meas_s"], hemo["tau_RC_s"])),
        "abstract":("In diastole the valve is shut and the compliant aorta discharges through the peripheral "
            "resistance, so pressure decays as P(t) = P\u2080 e^(\u2212t/RC). The measured decay constant \u03c4 \u2248 %.2f s "
            "equals the R\u00d7C product %.2f s." % (hemo["tau_meas_s"], hemo["tau_RC_s"])),
        "cards":[],
        "body":("<h2>Compliance turns pulses into flow</h2>"
            "<p>The Windkessel adds one element to the resistive network: a compliance C in parallel with the "
            "peripheral resistance R. During diastole the stored volume discharges and pressure relaxes "
            "exponentially.</p>%s"
            "<p>Fitting the log of the diastolic pressure segment recovers \u03c4 \u2248 %.2f s, exactly the analytic R\u00d7C = "
            "%.2f s, and within the cited aortic range. This is why arterial pressure never collapses to zero between "
            "beats: the compliance buffers the pump into near-steady organ perfusion.</p>"
            % (eq_fig(*e), hemo["tau_meas_s"], hemo["tau_RC_s"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "04", 1, r"GFR=K_f(P_{GC}-P_{BS}-\pi_{GC})",
        "GFR = K_f \u00b7 (P_GC \u2212 P_BS \u2212 \u03c0_GC)")
    S.append({"no":4,"title":"Glomerular filtration and autoregulation plateau","short":"Glomerular autoregulation plateau","tok":"V",
        "answer":("Glomerular filtration emerges from Starling forces and is held flat by tubuloglomerular feedback. "
            "Across renal perfusion 80\u2013180 mmHg the engine holds GFR \u2248 %.0f mL/min (P_GC %.0f mmHg, renal blood flow "
            "%.0f mL/min) while the open-loop control is not flat. Autoregulation is the kidney's R19 control-loop "
            "class. Grade [V]; absolute GFR [L]." % (ren["GFR_mL_min"], ren["P_GC_mmHg"], ren["RBF_mL_min"])),
        "abstract":("Filtration is the Starling balance GFR = K_f\u00b7(P_GC \u2212 P_BS \u2212 \u03c0_GC). Tubuloglomerular "
            "feedback adjusts afferent resistance to hold GFR \u2248 %.0f mL/min across a wide perfusion range; with the "
            "loop open, GFR tracks pressure instead of plateauing." % ren["GFR_mL_min"]),
        "cards":[CARD_GK],
        "body":("<h2>Filtration set by Starling forces</h2>"
            "<p>The kidney is the control-loop class. Single-nephron filtration is the net Starling drive across the "
            "glomerular membrane times the filtration coefficient K_f.</p>%s"
            "<h3>Tubuloglomerular feedback is the plateau</h3>"
            "<p>A PI feedback on afferent arteriolar resistance senses distal flow and corrects it, holding GFR \u2248 "
            "%.0f mL/min (P_GC %.0f mmHg, RBF %.0f mL/min) as perfusion swings 80\u2013180 mmHg. The contrast test "
            "confirms the open-loop coefficient of variation is several-fold larger \u2014 the plateau is the feedback, "
            "not a passive property.</p>" % (eq_fig(*e), ren["GFR_mL_min"], ren["P_GC_mmHg"], ren["RBF_mL_min"])),
        "eq_inline":3,"eq_display":1})

    S.append({"no":5,"title":"Osmoregulation and the ADH thirst loop","short":"Osmoregulation: ADH loop","tok":"V",
        "answer":("Plasma osmolality is regulated to a setpoint by the ADH/thirst negative-feedback loop. Under an "
            "imposed osmotic load the engine returns osmolality to \u2248 %.0f mOsm/kg (under 1 mOsm residual), whereas "
            "the loop-off control drifts far beyond. Osmoregulation completes the kidney's control-loop dynamics. "
            "Grade [V]; setpoint cited [L]." % osm["osm_rest"]),
        "abstract":("Water balance is a second nephron control loop: osmoreceptor-driven ADH and thirst act on "
            "free-water handling to defend a setpoint near %.0f mOsm/kg. The loop corrects an osmotic load to within "
            "1 mOsm; the no-loop control does not." % osm["osm_set"]),
        "cards":[CARD_GK],
        "body":("<h2>A setpoint defended by feedback</h2>"
            "<p>Plasma osmolality is held near %.0f mOsm/kg. A rise above threshold drives ADH release (water "
            "retention) and thirst (water intake); the engine models this as a PI water-balance loop on the same "
            "control-loop organ.</p>"
            "<p>Imposing osmotic loads from mild to severe, the loop restores osmolality to setpoint with sub-mOsm "
            "residual, while disabling the loop lets osmolality drift well past 5 mOsm of error. The kidney thus "
            "carries two coupled loops \u2014 filtration (GFR) and water balance (osmolality) \u2014 both emergent from its "
            "\u03b3-set control-loop class.</p>" % osm["osm_set"]),
        "eq_inline":2,"eq_display":0})

    e = write_eq_svg(docs, code, "06", 1, r"E=\frac{f_u CL_{int}}{Q_H+f_u CL_{int}},\quad F=1-E",
        "E = f_u\u00b7CL_int / (Q_H + f_u\u00b7CL_int) ,   F = 1 \u2212 E")
    S.append({"no":6,"title":"Hepatic clearance and oral bioavailability","short":"Hepatic clearance & F","tok":"F",
        "answer":("The liver clears blood by first-pass extraction; the well-stirred model sets the extraction ratio "
            "E and oral bioavailability F = 1 \u2212 E. For propranolol the engine gives E \u2248 %.2f, F \u2248 %.2f (clearance "
            "%.0f mL/min). High-E drugs are flow-limited (clearance flow-elasticity \u2248 0.90), low-E drugs "
            "capacity-limited (\u2248 0.10). Grade [F]/[L]." % (hep["E"], hep["F"], hep["CL_H_mL_min"])),
        "abstract":("Hepatic extraction is E = fu\u00b7CLint/(QH + fu\u00b7CLint) and oral bioavailability is F = 1 \u2212 E. As "
            "intrinsic clearance rises, E sweeps 0\u21921 and F falls 1\u21920; propranolol sits at E \u2248 %.2f, F \u2248 %.2f, "
            "matching the cited high-extraction tracer." % (hep["E"], hep["F"])),
        "cards":[CARD_GL],
        "body":("<h2>First-pass extraction sets bioavailability</h2>"
            "<p>The liver is the clearance class. In the well-stirred model the fraction removed in one pass is E, so "
            "the orally available fraction is F = 1 \u2212 E.</p>%s"
            "<h3>Flow-limited vs capacity-limited</h3>"
            "<p>Sweeping intrinsic clearance, E rises monotonically from ~0 to ~1 and F falls accordingly. The "
            "regimes separate by the canonical discriminant \u2014 hepatic-clearance flow-elasticity d(ln CL)/d(ln Q): "
            "for high-extraction drugs \u2248 0.90 (clearance tracks blood flow), for low-extraction drugs \u2248 0.10 "
            "(clearance set by fu\u00b7CLint, flow-independent). Propranolol (E \u2248 %.2f, F \u2248 %.2f) is correctly "
            "flow-limited.</p>" % (eq_fig(*e), hep["E"], hep["F"])),
        "eq_inline":3,"eq_display":1})

    e1 = write_eq_svg(docs, code, "07", 1, r"V(s)=\tfrac14 s^4-\tfrac{\gamma}{2}s^2-h s,\quad \Delta E_b(\gamma,0)=\gamma^2/4",
        "V(s) = \u00bcs\u2074 \u2212 (\u03b3/2)s\u00b2 \u2212 h\u00b7s ,   \u0394E_b(\u03b3,0) = \u03b3\u00b2/4")
    e2 = write_eq_svg(docs, code, "07", 2, r"RR(dose)=\exp\{[\Delta E_b(0)-\Delta E_b(dose)]/D\}",
        "RR(dose) = exp{ [\u0394E_b(0) \u2212 \u0394E_b(dose)] / D }")
    S.append({"no":7,"title":"Carcinogenesis as R19 barrier lowering","short":"Carcinogenesis: barrier lowering","tok":"F",
        "answer":("A carcinogen is a sustained aberrant drive on the same R19 cell-fate switch; it lowers the barrier "
            "out of the healthy basin, and the malignant-crossing rate is Kramers/Arrhenius over that barrier. The "
            "tilted double well gives barrier = \u03b3\u00b2/4 at zero drive, falling to zero at the spinodal, so relative "
            "risk RR(dose) = exp(\u0394barrier/D). Grade [F]."),
        "abstract":("Health and malignancy are the two basins of V(s) = \u00bcs\u2074 \u2212 (\u03b3/2)s\u00b2 \u2212 hs. A carcinogen "
            "drive h lowers the escape barrier \u0394E_b, which equals \u03b3\u00b2/4 at h=0 and vanishes at the spinodal "
            "|h| = 2(\u03b3/3)^1.5; the crossing rate, hence RR, is Arrhenius in \u0394E_b."),
        "cards":[CARD_R19],
        "body":("<h2>One switch, two basins</h2>"
            "<p>Cell fate is the shared R19 switch. Its potential is a double well; the healthy and malignant states "
            "are the two minima separated by a barrier \u0394E_b = \u03b3\u00b2/4 at rest.</p>%s"
            "<h3>A carcinogen tilts the well</h3>"
            "<p>A sustained carcinogen drive h tilts the potential, shrinking the healthy basin toward its spinodal "
            "and lowering the escape barrier. The barrier is computed exactly as V(saddle) \u2212 V(healthy minimum) from "
            "the three steady-state roots, falling to zero precisely at |h| = 2(\u03b3/3)^1.5, beyond which the healthy "
            "basin disappears (barrierless).</p>%s"
            "<p>The malignant-crossing rate is Arrhenius in the barrier, so RR(dose) = exp([\u0394E_b(0) \u2212 "
            "\u0394E_b(dose)]/D). The next two sections instantiate this single kernel for renal and hepatic cancer and "
            "test it against cited epidemiology.</p>" % (eq_fig(*e1), eq_fig(*e2))),
        "eq_inline":3,"eq_display":2})

    e = write_eq_svg(docs, code, "08", 1,
        r"RR(20\,PY)\approx%.2f,\ RR(50\,PY)\approx%.2f" % (rcc["RR_eversmoker_20py"], rcc["RR_heavy_50py"]),
        "RR(20 PY) \u2248 %.2f ,   RR(50 PY) \u2248 %.2f" % (rcc["RR_eversmoker_20py"], rcc["RR_heavy_50py"]))
    b = rcc["cited_dose_bands"]
    S.append({"no":8,"title":"Renal cell carcinoma and the smoking dose response","short":"RCC smoking dose-response","tok":"V",
        "answer":("Smoking raises renal cell carcinoma risk through cumulative barrier-lowering. The kernel "
            "reproduces a monotone, saturating dose-response: RR \u2248 %.2f at ~20 pack-years and \u2248 %.2f at 50, tracking "
            "the Hunt 2005 meta dose bands (1.60/1.83/2.03). Anchor [L]; shape [V]; absolute incidence [O]."
            % (rcc["RR_eversmoker_20py"], rcc["RR_heavy_50py"])),
        "abstract":("Mapping pack-years to a sustained drive on the kidney R19 switch yields RR(dose) = exp("
            "\u0394barrier/D). The curve is monotone and saturating, giving RR \u2248 %.2f (20 PY) and \u2248 %.2f (50 PY) "
            "\u2014 inside the cited smoking bands; absolute incidence stays open."
            % (rcc["RR_eversmoker_20py"], rcc["RR_heavy_50py"])),
        "cards":[CARD_R19],
        "body":("<h2>Pack-years lower the barrier</h2>"
            "<p>Renal cell carcinoma risk rises with tobacco exposure. Cumulative pack-years map to a sustained "
            "drive that lowers the kidney switch barrier; the Arrhenius crossing rate then gives the relative "
            "risk.</p>%s"
            "<h3>Monotone, saturating, in-band</h3>"
            "<p>The dose-response is monotone and sigmoidal (saturating at high exposure), with RR \u2248 %.2f near the "
            "20 pack-year ever-smoker mark and \u2248 %.2f at 50 pack-years. The 30/40/50 PY values %.2f/%.2f/%.2f track "
            "the Hunt 2005 meta dose-dependence (1.60/1.83/2.03). The shape is forced by the barrier law; only the "
            "dose\u2192drive scale is calibrated [CAL], and the absolute incidence per 100k remains [O] pending a "
            "population baseline hazard.</p>"
            % (eq_fig(*e), rcc["RR_eversmoker_20py"], rcc["RR_heavy_50py"], b["RR_30py"], b["RR_40py"], b["RR_50py"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "09", 1, r"RR_{comb}=\exp\{(\Delta_a+\Delta_v)/D\}=RR_a\cdot RR_v",
        "RR_comb = exp{(\u0394_a + \u0394_v)/D} = RR_a \u00b7 RR_v")
    S.append({"no":9,"title":"Hepatocellular carcinoma and aflatoxin HBV synergy","short":"HCC: aflatoxin \u00d7 HBV synergy","tok":"V",
        "answer":("The framework predicts the aflatoxin \u00d7 HBV synergy in liver cancer. When two carcinogens add "
            "their barrier decrements, relative risks multiply: aflatoxin RR %.2f \u00d7 HBV RR %.1f = combined %.1f, "
            "matching the meta-analytic %.0f with no synergy parameter. Additive drives predict a supra-multiplicative "
            "crossover near the spinodal. Anchor [L]; algebra [V]."
            % (mA["RR_aflatoxin"], mA["RR_HBV"], mA["RR_combined"], mA["meta_observed"])),
        "abstract":("Two carcinogens lowering the same liver barrier by \u0394_a and \u0394_v multiply their risks: "
            "RR_comb = exp((\u0394_a+\u0394_v)/D) = RR_a\u00b7RR_v. Aflatoxin %.2f \u00d7 HBV %.1f gives %.1f, versus the cited "
            "meta product %.0f \u2014 multiplicative to %.3f%%, parameter-free."
            % (mA["RR_aflatoxin"], mA["RR_HBV"], mA["RR_combined"], mA["meta_observed"], mA["multiplicativity_dev_pct"])),
        "cards":[CARD_R19],
        "body":("<h2>Why the risks multiply</h2>"
            "<p>Aflatoxin B1 and chronic HBV both promote hepatocellular carcinoma. On the R19 picture each "
            "independently lowers the escape barrier by an amount \u0394; because the crossing rate is Arrhenius, "
            "additive barrier decrements make the relative risks multiply.</p>%s"
            "<h3>Multiplicative, with no synergy knob</h3>"
            "<p>Pinning the single-agent risks to the meta-analysis (aflatoxin RR %.2f, HBV RR %.1f) forces the "
            "combined RR to exp((\u0394_a+\u0394_v)/D) = %.1f \u2014 the product, matching the observed %.0f to within %.3f%% "
            "with no fitted synergy term. This is the headline [V] result: the substrate predicts the synergy "
            "<em>algebra</em>, not just a number.</p>"
            "<h3>The supra-multiplicative crossover</h3>"
            "<p>If instead the two exposures add their <em>drives</em> on one barrier, the synergy is "
            "sub-multiplicative at moderate dose but turns supra-multiplicative once the combined drive nears the "
            "spinodal (the barrier collapses). The framework thus predicts that supra-multiplicative cohorts (e.g. "
            "Qian 1994, RR \u2248 59 &gt; the ~24 product) are the signature of combined exposure approaching the "
            "spinodal \u2014 a falsifiable, mechanistic claim. Absolute HCC incidence remains [O].</p>"
            % (eq_fig(*e), mA["RR_aflatoxin"], mA["RR_HBV"], mA["RR_combined"], mA["meta_observed"], mA["multiplicativity_dev_pct"])),
        "eq_inline":3,"eq_display":1})

    # =====================================================================
    #  DISEASE EXTENSIONS  (sections 10-19) -- each disorder is one named
    #  setting of an existing relation; numbers regenerated from the battery.
    # =====================================================================
    d8=dis["T8"]; d9=dis["T9"]; d10=dis["T10"]; d11=dis["T11"]; d12=dis["T12"]
    d13=dis["T13"]; d14=dis["T14"]; d15=dis["T15"]; d16=dis["T16"]; d17=dis["T17"]
    ish=d8["ISH_point"]

    e = write_eq_svg(docs, code, "10", 1, r"C\downarrow:\ PP\uparrow,\ \tau=RC\downarrow,\ MAP\ \text{flat}",
        "C\u2193:  PP\u2191 ,  \u03c4 = RC\u2193 ,  MAP flat")
    S.append({"no":10,"title":"Arterial stiffening and isolated systolic hypertension","short":"Arterial stiffening \u2192 ISH","tok":"V",
        "owner":("Isolated systolic hypertension is owned by the <b>homeostasis_hemodynamic</b> sibling (a regulated "
            "pressure-setpoint disorder); its structural driver, central arterial stiffening, is an <b>aging_senescence</b> "
            "process. Shown here only as a perturbation of circulatory's Windkessel pulse-pressure/\u03c4 relation \u2014 a "
            "boundary demonstration, not a circulatory-owned disease."),
        "answer":("Stiffening the arteries \u2014 falling compliance at fixed CO\u00d7SVR \u2014 widens the pulse pressure and "
            "shortens \u03c4=RC while mean pressure stays flat, exactly the Framingham aging pattern. The engine reaches an "
            "isolated-systolic-hypertension point at C\u2248%.2f (SBP\u2248%.0f, DBP\u2248%.0f, PP\u2248%.0f). Grade [V]; Franklin 1997 anchor [L]."
            % (ish["C"], ish["SBP"], ish["DBP"], ish["PP"])),
        "abstract":("Isolated systolic hypertension is the highest-confidence disease prediction: it lands directly on the "
            "pulse pressure and \u03c4 the Windkessel already prints. Reducing arterial compliance widens PP from %.0f to %.0f mmHg and "
            "shortens \u03c4 from %.2f to %.2f s, with MAP unchanged \u2014 SBP rises, DBP falls."
            % (d8["PP_mmHg"][3], d8["PP_mmHg"][-1], d8["tau_s"][3], d8["tau_s"][-1])),
        "cards":[CARD_MAP, CARD_TAU],
        "body":("<h2>Stiffness, not resistance, widens the pulse</h2>"
            "<p>After mid-life the dominant hemodynamic change is central arterial stiffening, not a rise in peripheral "
            "resistance. On the Windkessel this is a fall in the compliance C at fixed CO\u00d7SVR. Because mean pressure is "
            "set by CO\u00d7SVR (unchanged), MAP stays flat while the pulse pressure widens and the diastolic decay \u03c4=RC "
            "shortens.</p>%s"
            "<h3>An ISH point emerges</h3>"
            "<p>Sweeping C from compliant to stiff, the engine holds MAP flat (relative range %.0e) while PP rises "
            "monotonically %.0f\u2192%.0f mmHg and \u03c4 falls %.2f\u2192%.2f s in lockstep. SBP climbs and DBP falls until, near "
            "C\u2248%.2f, the reading crosses an isolated-systolic-hypertension threshold (SBP\u2265140 with DBP&lt;90: here "
            "%.0f/%.0f). This reproduces the classic Framingham age pattern \u2014 little change in mean pressure, a plateau "
            "then rise in SBP, a fall in DBP after 50, and a dramatic PP increase \u2014 attributed to aortic stiffening with "
            "little change in peripheral resistance (Franklin SS et al., Circulation 1997;96:308\u2013315). The hemodynamic "
            "shape is forced; the absolute cardiovascular-event rate needs a population hazard model and stays [O].</p>"
            % (eq_fig(*e), d8["MAP_rel_range"], d8["PP_mmHg"][3], d8["PP_mmHg"][-1], d8["tau_s"][3], d8["tau_s"][-1],
               ish["C"], ish["SBP"], ish["DBP"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "11", 1, r"MAP=CO\times SVR\ \text{(resistance route)}",
        "MAP = CO \u00d7 SVR   (resistance route)")
    rr=d9["contrast_equal_MAP"]["resistance_route"]; fr=d9["contrast_equal_MAP"]["flow_route"]
    S.append({"no":11,"title":"Essential hypertension as a resistance rise","short":"Essential hypertension (SVR)","tok":"F",
        "owner":("Essential hypertension is owned by the <b>homeostasis_hemodynamic</b> sibling (regulated-setpoint loop "
            "dysregulation). Shown here only as circulatory's MAP=CO\u00d7SVR relation run forward \u2014 a boundary "
            "demonstration, not a circulatory-owned disease."),
        "answer":("Resistance-driven hypertension is the Ohm identity run forward: raising systemic vascular resistance "
            "drives MAP up while MAP=CO\u00d7SVR holds to &lt;1%%. The same MAP (%.0f mmHg) is reachable from a pure cardiac-output "
            "rise at normal resistance \u2014 same pressure, different mechanism. Grade [F]; JNC7/ACC-AHA threshold [L]."
            % rr["MAP"]),
        "abstract":("Essential hypertension sets the resistance knob. Sweeping SVR upward carries MAP from %.0f to %.0f mmHg "
            "with the hydraulic Ohm law exact (max deviation %.0e). A contrast run reaches the identical MAP by raising CO "
            "instead, separating resistance- from flow-driven hypertension at equal pressure."
            % (d9["MAP_mmHg"][0], d9["MAP_mmHg"][-1], d9["max_ohm_dev"])),
        "cards":[CARD_MAP],
        "body":("<h2>Pressure up the resistance axis</h2>"
            "<p>The commonest hypertension is a rise in systemic vascular resistance at near-normal cardiac output. On the "
            "transport law MAP \u2212 CVP = CO\u00d7SVR this is simply the SVR term increasing; MAP follows linearly and the Ohm "
            "identity is preserved.</p>%s"
            "<h3>Same pressure, two mechanisms</h3>"
            "<p>Across the SVR sweep MAP rises %.0f\u2192%.0f mmHg and crosses a stage-2 threshold (140/90) while the identity "
            "holds to %.0e. The contrast makes the mechanism explicit: the resistance route (SVR %.2f, CO %.0f mL/s) and a "
            "flow route (SVR %.2f, CO %.0f mL/s) reach the <em>same</em> MAP %.0f mmHg from opposite knobs. Pressure alone "
            "cannot distinguish them \u2014 the engine can, because it carries CO and SVR separately. This is the substrate for "
            "the hemodynamic sub-typing the next section completes for shock.</p>"
            % (eq_fig(*e), d9["MAP_mmHg"][0], d9["MAP_mmHg"][-1], d9["max_ohm_dev"],
               rr["SVR"], rr["CO_ml_s"], fr["SVR"], fr["CO_ml_s"], fr["MAP"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "12", 1, r"MAP<65:\ CO\downarrow\ \text{or}\ SVR\downarrow",
        "MAP < 65 :  CO\u2193  or  SVR\u2193")
    rh=d10["route_hypovolemic"]; rd=d10["route_distributive"]
    S.append({"no":12,"title":"Hypotension and shock subtypes","short":"Shock subtypes (CO vs SVR)","tok":"F",
        "owner":("Shock is owned by the <b>homeostasis_hemodynamic</b> sibling (regulated-setpoint loop failure). Shown "
            "here only as circulatory's MAP=CO\u00d7SVR relation carried to the perfusion floor \u2014 a boundary "
            "demonstration, not a circulatory-owned disease."),
        "answer":("Shock is one MAP reached by two routes. Dropping cardiac output (hypovolemic) or dropping resistance "
            "(distributive) both pull MAP below the 65 mmHg perfusion floor; at a matched %.0f mmHg the engine separates "
            "the routes \u2014 CO %.0f mL/s at normal SVR versus SVR %.2f at normal CO. Grade [F]; Surviving Sepsis MAP\u226565 [L]."
            % (d10["matched_shock_point_mmHg"], rh["CO_ml_s"], rd["SVR"])),
        "abstract":("Hypotension lands on the same Ohm identity from either factor. A cardiac-output fall and a resistance "
            "fall each drive MAP under 65 mmHg; the engine reproduces both and, at a matched MAP of %.0f mmHg, attributes "
            "them to distinct knobs \u2014 the hemodynamic basis of shock classification."
            % d10["matched_shock_point_mmHg"]),
        "cards":[CARD_MAP],
        "body":("<h2>One floor, two routes</h2>"
            "<p>The Surviving Sepsis Campaign sets a mean-arterial-pressure target of at least 65 mmHg during resuscitation; "
            "below it, organ perfusion is threatened (Asfar P et al., SEPSISPAM, N Engl J Med 2014;370:1583\u20131593, PMID "
            "24635770). On the transport law a MAP this low can arise two ways.</p>%s"
            "<h3>Hypovolemic vs distributive</h3>"
            "<p>Lowering cardiac output (hypovolemic/cardiogenic) carries MAP down %s mmHg; lowering systemic resistance "
            "(distributive/septic) carries it down %s mmHg \u2014 both cross the 65 mmHg floor. At a matched MAP of %.0f mmHg the "
            "two settings are mechanistically distinct: the hypovolemic route holds normal SVR (%.2f) with reduced CO "
            "(%.0f mL/s), while the distributive route holds normal CO (%.0f mL/s) with reduced SVR (%.2f). The engine thus "
            "reproduces the clinical principle that MAP names the emergency but CO and SVR name the cause.</p>"
            % (eq_fig(*e),
               "&rarr;".join("%.0f"%x for x in d10["hypovolemic_MAP"]),
               "&rarr;".join("%.0f"%x for x in d10["distributive_MAP"]),
               d10["matched_shock_point_mmHg"], rh["SVR"], rh["CO_ml_s"], rd["CO_ml_s"], rd["SVR"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "13", 1, r"Osm=S/W\ \text{(ADH gain}\to0\text{)}",
        "Osm = S / W   (ADH gain \u2192 0)")
    S.append({"no":13,"title":"Diabetes insipidus and the failed osmostat","short":"Diabetes insipidus (ADH\u21920)","tok":"V",
        "owner":("Diabetes insipidus is owned by the <b>homeostasis_ionic</b> sibling (defended-osmolality loop "
            "dysregulation). Shown here only as a perturbation of circulatory's ADH/osmoregulation relation \u2014 a "
            "boundary demonstration, not a circulatory-owned disease."),
        "answer":("Killing ADH-loop gain breaks the osmostat: an imposed water deficit drives osmolality up and it never "
            "returns. At a 3 L deficit the engine holds osmolality at %.0f mOsm/kg (a hypernatremia surrogate) versus %.0f "
            "for the intact loop, which corrects every load. Grade [V]; DI hyperosmolality anchor [L]; absolute Na [O]."
            % (d11["DI_osm_final"][4], d11["intact_osm_final"][4])),
        "abstract":("Diabetes insipidus sets the ADH/thirst gain to zero on the osmostat. Across graded water deficits the "
            "diseased loop fails to recover \u2014 osmolality climbs %.0f\u2192%.0f mOsm/kg and tracks the deficit \u2014 while the "
            "intact loop returns to the %.0f setpoint within 1 mOsm. The contrast, not a tuned number, is the result."
            % (d11["DI_osm_final"][0], d11["DI_osm_final"][-1], d11["osm_setpoint"])),
        "cards":[CARD_OSM],
        "body":("<h2>No antidiuresis, no recovery</h2>"
            "<p>In diabetes insipidus the antidiuretic response is absent (central) or unheeded (nephrogenic). On the "
            "osmostat this is the loop gain going to zero: the controller can no longer retain free water, so an osmotic "
            "load is not corrected.</p>%s"
            "<h3>Hyperosmolality that tracks the deficit</h3>"
            "<p>Imposing water deficits of 0.5\u20134 L, the gain-zero loop lets osmolality rise monotonically "
            "%.0f\u2192%.0f mOsm/kg and stay there, crossing the hyperosmolality band (\u2265295, a hypernatremia surrogate, Na&gt;145), "
            "while the intact loop corrects every load back to %.0f mOsm/kg (within 0.2). Each diseased value exceeds its "
            "intact counterpart by far more than the loop's own residual \u2014 a mechanistic separation rather than a fitted "
            "offset. The direction and contrast are reproduced [V]; mapping osmolality to an absolute plasma sodium needs a "
            "renal free-water-clearance calibration and stays [O].</p>"
            % (eq_fig(*e), d11["DI_osm_final"][0], d11["DI_osm_final"][-1], d11["osm_setpoint"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "14", 1, r"Osm\to OSM_{set}+\Delta,\ \Delta<0",
        "Osm \u2192 OSM_set + \u0394 ,  \u0394 < 0")
    mir=d12["mirror"]
    S.append({"no":14,"title":"SIADH as an inappropriately low osmostat","short":"SIADH (mirror of DI)","tok":"V",
        "owner":("SIADH is owned by the <b>homeostasis_ionic</b> sibling (defended-osmolality loop dysregulation). Shown "
            "here only as the mirror perturbation of circulatory's ADH/osmoregulation relation \u2014 a boundary "
            "demonstration, not a circulatory-owned disease."),
        "answer":("SIADH is the exact mirror of diabetes insipidus. A sustained inappropriate antidiuresis \u2014 modeled as a "
            "downward shift of the defended osmolality \u2014 holds osmolality below setpoint (a hyponatremia surrogate), reaching "
            "%.0f mOsm/kg while DI rises to %.0f around the %.0f setpoint. Grade [V]; SIADH Na&lt;135 anchor [L]; volume escape [O]."
            % (mir["SIADH_osm"], mir["DI_osm"], mir["setpoint"])),
        "abstract":("SIADH applies a sustained antidiuretic bias to the same osmostat, represented as a downward shift of "
            "the defended osmolality. Osmolality settles below the %.0f setpoint, deeper with larger shift "
            "(%.0f\u2192%.0f mOsm/kg), reaching the hyponatremia band \u2014 the sign-flipped image of the DI run on one loop."
            % (mir["setpoint"], d12["SIADH_osm_final"][0], d12["SIADH_osm_final"][-1])),
        "cards":[CARD_OSM],
        "body":("<h2>Antidiuresis that defends the wrong setpoint</h2>"
            "<p>In SIADH antidiuretic hormone is secreted inappropriately, so water is retained even when plasma is already "
            "dilute, producing euvolemic hyponatremia (serum Na&lt;135; Verbalis JG et al., 2013). On the osmostat the "
            "cleanest minimal representation is a downward shift of the <em>defended</em> osmolality: the loop now stably "
            "holds a low osmolality.</p>%s"
            "<h3>The mirror image of DI</h3>"
            "<p>Shifting the defended osmolality down %.0f\u2192%.0f mOsm/kg, the loop settles osmolality below setpoint and "
            "crosses the hyponatremia band (\u2264275, a Na&lt;135 surrogate). Placed beside the previous section this is an exact "
            "mirror on one mechanism: diabetes insipidus drives osmolality <em>above</em> the %.0f setpoint (to %.0f), SIADH "
            "holds it <em>below</em> (to %.0f). The direction and the DI/SIADH symmetry are reproduced [V]; the minimal "
            "osmostat omits the volume-mediated ADH escape that caps real SIADH, so absolute sodium and the escape kinetics "
            "remain [O].</p>"
            % (eq_fig(*e), d12["SIADH_osm_final"][0],
               d12["SIADH_osm_final"][-1], mir["setpoint"], mir["DI_osm"], mir["SIADH_osm"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "15", 1, r"GFR_{tot}=N\cdot K_f(P_{GC}-P_{BS}-\pi_{GC})",
        "GFR_tot = N \u00b7 K_f (P_GC \u2212 P_BS \u2212 \u03c0_GC)")
    st=d13["stages"]
    S.append({"no":15,"title":"Chronic kidney disease and GFR staging","short":"CKD / GFR staging","tok":"V",
        "owner":("Ownership decided (handoff &sect;4.4, v0.5.0): chronic kidney disease is <b>not</b> circulatory-owned. "
            "It is the downstream final-common-pathway readout of sibling etiologies \u2014 diabetic and hypertensive "
            "nephropathy owned by the <b>homeostasis</b> siblings, and intrinsic age-related nephron loss owned by "
            "<b>aging_senescence</b>. Circulatory retains this section only as a demonstration of its renal "
            "autoregulation relation (total GFR = surviving-nephron fraction \u00d7 the autoregulated per-nephron value), "
            "not as a circulatory-owned disease."),
        "answer":("Chronic kidney disease is nephron-mass loss: total GFR is the per-nephron filtration times the remaining "
            "fraction. Stepping that fraction down walks total GFR through the KDIGO stages \u2014 %.0f/%.0f/%.0f/%.0f/%.0f mL/min "
            "\u2014 while per-nephron autoregulation stays flat at each level (open loop does not). Grade [V]; KDIGO anchor [L]."
            % (st[1]["total_GFR_mL_min"], st[2]["total_GFR_mL_min"], st[3]["total_GFR_mL_min"],
               st[4]["total_GFR_mL_min"], st[5]["total_GFR_mL_min"])),
        "abstract":("CKD scales the autoregulated single-kidney GFR by the surviving nephron fraction (the intact-nephron "
            "hypothesis). The fraction steps total GFR through the KDIGO G-categories while the tubuloglomerular plateau "
            "stays flat at each reduced level (coefficient of variation ~0); the open loop instead tracks pressure "
            "(coefficient of variation %.2f)." % d13["cv_open_loop"]),
        "cards":[CARD_GFR],
        "body":("<h2>Stage is nephron mass, not a broken loop</h2>"
            "<p>A reduced filtration coefficient per nephron is compensated by tubuloglomerular feedback (the surviving "
            "nephrons hyperfilter), so it cannot by itself lower the plateau without saturating the controller. What lowers "
            "the stage is loss of nephron <em>number</em>: total GFR is the per-nephron autoregulated value times the "
            "remaining fraction N.</p>%s"
            "<h3>Walking the KDIGO ladder</h3>"
            "<p>Holding per-nephron autoregulation intact and stepping N down, total GFR lands on the KDIGO thresholds "
            "\u2014 N=%.2f\u219290, %.2f\u219260, %.2f\u219245, %.2f\u219230, %.2f\u219215 mL/min (categories G2 through G5) \u2014 and at every "
            "reduced level GFR is still flat across 80\u2013180 mmHg (coefficient of variation ~0). The contrast is decisive: with "
            "the loop open, GFR tracks pressure with a coefficient of variation of %.2f. So CKD here is a lower autoregulated "
            "plateau, faithful to the KDIGO 2012/2024 categories; absolute stage prevalence needs population data and stays "
            "[O].</p>"
            % (eq_fig(*e), st[1]["N_frac"], st[2]["N_frac"], st[3]["N_frac"], st[4]["N_frac"], st[5]["N_frac"],
               d13["cv_open_loop"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "16", 1, r"R_a\to R_a^{max}\Rightarrow GFR\propto P_a",
        "R_a \u2192 R_a^max  \u21d2  GFR \u221d P_a")
    S.append({"no":16,"title":"Autoregulation breakthrough and glomerular hypertension","short":"Autoregulation breakthrough","tok":"V",
        "owner":("The injury here \u2014 glomerular hypertension \u2014 is driven by systemic hypertension owned by the "
            "<b>homeostasis_hemodynamic</b> sibling. Shown here only as a perturbation of circulatory's renal "
            "autoregulation plateau \u2014 a boundary demonstration, not a circulatory-owned disease."),
        "answer":("Push renal perfusion past the autoregulatory ceiling and the plateau breaks: once the afferent arteriole "
            "saturates near %.0f mmHg, GFR and glomerular pressure climb with pressure (to %.0f mL/min and %.0f mmHg at "
            "240 mmHg) \u2014 a glomerular-barotrauma surrogate. Inside 80\u2013180 mmHg GFR stays flat. Grade [V]; autoregulation range [L]."
            % (d14["breakthrough_pressure_mmHg"], d14["GFR_at_240"], d14["P_GC_at_240"])),
        "abstract":("Extending the perfusion sweep past the plateau, the afferent resistance hits its ceiling and "
            "autoregulation can no longer buffer pressure. Beyond a breakthrough near %.0f mmHg, GFR and glomerular capillary "
            "pressure rise with perfusion \u2014 the surrogate for hypertensive glomerular injury \u2014 emerging from the same "
            "feedback used for the healthy plateau."
            % d14["breakthrough_pressure_mmHg"]),
        "cards":[CARD_GFR],
        "body":("<h2>When the afferent arteriole runs out of room</h2>"
            "<p>Renal autoregulation flattens GFR by constricting the afferent arteriole as pressure rises, but the "
            "arteriole has a maximum resistance. Below the ceiling the plateau holds; above it the controller is saturated "
            "and pressure passes straight through to the glomerulus.</p>%s"
            "<h3>Breakthrough and barotrauma</h3>"
            "<p>Across 80\u2013180 mmHg GFR is flat (the §4 plateau). Past a breakthrough pressure of about %.0f mmHg the "
            "afferent resistance is pinned at its ceiling, and GFR and glomerular capillary pressure both climb \u2014 reaching "
            "%.0f mL/min and %.0f mmHg by 240 mmHg. This is a mechanistic surrogate for the glomerular hypertension and "
            "barotrauma of severe systemic hypertension, and it is not a new rule: it falls out of the same "
            "tubuloglomerular-feedback block once its actuator saturates. The autoregulatory window itself (~80\u2013180 mmHg) is "
            "the cited anchor [L].</p>"
            % (eq_fig(*e), d14["breakthrough_pressure_mmHg"], d14["GFR_at_240"], d14["P_GC_at_240"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "17", 1, r"CL_{int}\downarrow\Rightarrow E\downarrow,\ F=1-E\uparrow",
        "CL_int\u2193  \u21d2  E\u2193 ,  F = 1\u2212E\u2191")
    S.append({"no":17,"title":"Hepatic impairment and the dose-reduction rule","short":"Hepatic impairment (F\u2191)","tok":"V",
        "owner":("This is a pharmacokinetic consequence of circulatory's hepatic-clearance relation F=1\u2212E, not a disease "
            "entity; the underlying hepatic disease (e.g. cirrhosis) is owned by <b>digestive_vp_site</b> / "
            "<b>disease_wp</b>. Shown here only as a PK perturbation of that relation."),
        "answer":("Liver impairment lowers intrinsic clearance, so a high-extraction drug's first-pass falls and its oral "
            "bioavailability rises \u2014 propranolol-like F climbs %.2f\u2192%.2f (%.1f\u00d7 over-exposure) as CLint falls, while a "
            "low-extraction drug barely moves (%.2f\u00d7). That is the clinical dose-reduction rule, literally F=1\u2212E. Grade [V]; Child-Pugh anchor [L]."
            % (d15["highE_F"][0], d15["highE_F"][-1], d15["highE_F_fold"], d15["lowE_F_fold"])),
        "abstract":("Hepatic impairment scales intrinsic clearance down. For a high-extraction drug E falls and F=1\u2212E rises "
            "%.0f%%\u2192%.0f%% (%.1f\u00d7), demanding dose reduction; a low-extraction drug is comparatively spared (%.2f\u00d7). The "
            "selectivity \u2014 high-E strongly affected, low-E not \u2014 is the contrast, matching hepatic-impairment pharmacokinetics."
            % (d15["highE_F"][0]*100, d15["highE_F"][-1]*100, d15["highE_F_fold"], d15["lowE_F_fold"])),
        "cards":[CARD_HEP],
        "body":("<h2>Less clearance, more drug</h2>"
            "<p>In cirrhosis the metabolic capacity of the hepatocytes falls. For a high-extraction drug \u2014 one largely "
            "removed on first pass \u2014 the oral bioavailability is F=1\u2212E, so a drop in intrinsic clearance lowers E and raises "
            "F directly.</p>%s"
            "<h3>High-extraction drugs over-expose; low-extraction spared</h3>"
            "<p>Scaling intrinsic clearance down, the propranolol-like drug's bioavailability rises %.2f\u2192%.2f \u2014 a %.1f-fold "
            "over-exposure \u2014 while a low-extraction drug rises only %.2f-fold. High-extraction drugs are defined by removal of "
            "more than ~60%% on first pass (F&lt;40%% in health); in cirrhosis their F can approach 100%% and they must be dosed "
            "very carefully (Clinical Pharmacokinetics, hepatic first-pass metabolism in liver disease). The direction and "
            "the high-E/low-E selectivity are reproduced [V]; the absolute exposure needs a severity\u2192CLint calibration per "
            "agent and stays [O].</p>"
            % (eq_fig(*e), d15["highE_F"][0], d15["highE_F"][-1], d15["highE_F_fold"], d15["lowE_F_fold"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "18", 1, r"F=1-(1-s)E,\quad dF/ds=E",
        "F = 1 \u2212 (1\u2212s)E ,   dF/ds = E")
    S.append({"no":18,"title":"Portosystemic shunt and first-pass escape","short":"Portosystemic shunt","tok":"F",
        "owner":("This is a pharmacokinetic consequence of circulatory's first-pass relation, not a disease entity; the "
            "underlying portal-hypertension/shunt pathology is owned by <b>digestive_vp_site</b> / <b>disease_wp</b>. "
            "Shown here only as a PK perturbation of that relation."),
        "answer":("A portosystemic shunt lets a fraction s of portal blood bypass the hepatocytes, so oral bioavailability "
            "becomes F=1\u2212(1\u2212s)E. The slope dF/ds equals the extraction ratio E exactly, so high-extraction drugs are most "
            "affected (slope %.2f vs %.2f for a low-E drug). Grade [F], a corollary of the clearance result."
            % (d16["dF_ds_highE"], d16["dF_ds_lowE"])),
        "abstract":("Shunting routes part of the portal flow around the liver, escaping first pass. The oral bioavailability "
            "is F=1\u2212(1\u2212s)E and its sensitivity to the shunt fraction is dF/ds=E \u2014 so flow-limited high-extraction drugs gain "
            "the most (here F rises %.2f\u2192%.2f) while low-extraction drugs barely change."
            % (d16["highE_F"][0], d16["highE_F"][-1])),
        "cards":[CARD_HEP],
        "body":("<h2>Bypassing the first pass</h2>"
            "<p>Portal hypertension opens porto-systemic collaterals, so a fraction s of orally absorbed drug reaches the "
            "systemic circulation without crossing hepatocytes. The bypassed fraction escapes extraction entirely, giving "
            "F = s + (1\u2212s)(1\u2212E) = 1\u2212(1\u2212s)E.</p>%s"
            "<h3>High-extraction drugs gain the most</h3>"
            "<p>The sensitivity to the shunt is exactly dF/ds = E. For the high-extraction drug (E=%.2f) bioavailability "
            "rises steeply %.2f\u2192%.2f as s goes 0\u21920.8 (slope %.2f); for a low-extraction drug (E=%.2f) it barely moves "
            "(slope %.2f). This is a direct corollary of the clearance flow-elasticity result in §6 \u2014 flow-limited drugs are "
            "the ones whose first pass a shunt can steal \u2014 and it matches the clinical observation that shunting raises the "
            "bioavailability of moderate-to-high-extraction drugs toward unity (PLOS One; Frontiers in Medicine 2022).</p>"
            % (eq_fig(*e), d16["E_high"], d16["highE_F"][0], d16["highE_F"][-1], d16["dF_ds_highE"],
               d16["E_low"], d16["dF_ds_lowE"])),
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "19", 1, r"\tfrac{d\ln CL}{d\ln CL_{int}}\approx 1\,(\text{low-}E),\ \approx 0\,(\text{high-}E)",
        "d ln CL / d ln CL_int \u2248 1 (low-E) ,  \u2248 0 (high-E)")
    S.append({"no":19,"title":"Enzyme induction, inhibition, and drug interactions","short":"Enzyme induction/inhibition (DDI)","tok":"V",
        "owner":("Drug\u2013drug interactions are a pharmacology consequence of circulatory's hepatic-clearance relation, not "
            "a disease at all. Shown here only as a perturbation of that relation by an interacting drug."),
        "answer":("A drug interaction is a change in intrinsic clearance. The clearance CLint-elasticity is ~1 for "
            "low-extraction drugs (capacity-limited, interaction-sensitive: here %.2f) and ~0 for high-extraction drugs "
            "(flow-limited: %.2f). Inhibition raises bioavailability, induction lowers it (F %.2f\u2192%.2f). Grade [V]; typical DDI fold-changes [L]."
            % (d17["CLint_elasticity_lowE"], d17["CLint_elasticity_highE"], d17["lowE_F_inhibited"], d17["lowE_F_induced"])),
        "abstract":("Enzyme induction and inhibition multiply intrinsic clearance up or down. The well-stirred model predicts "
            "the regime signature: low-extraction clearance is CLint-elastic (~%.2f, capacity-limited) and high-extraction "
            "clearance is CLint-inelastic (~%.2f, flow-limited), with inhibition raising F and induction lowering it."
            % (d17["CLint_elasticity_lowE"], d17["CLint_elasticity_highE"])),
        "cards":[CARD_HEP],
        "body":("<h2>Interactions move intrinsic clearance</h2>"
            "<p>Co-administered inhibitors or inducers change the intrinsic clearance CLint of the affected drug. Whether "
            "that matters depends on the extraction regime \u2014 the same split (flow-limited vs capacity-limited) that governs "
            "the healthy liver.</p>%s"
            "<h3>The regime signature, and the direction</h3>"
            "<p>Measuring the CLint-elasticity of hepatic clearance, the low-extraction drug is capacity-limited with "
            "elasticity %.2f (clearance \u2248 fu\u00b7CLint, so it tracks CLint almost one-for-one), while the high-extraction drug is "
            "flow-limited with elasticity %.2f (clearance \u2248 hepatic blood flow, nearly CLint-independent). The direction is "
            "correct too: for the capacity-limited drug, inhibition (CLint down) raises bioavailability %.2f\u2192%.2f and "
            "induction (CLint up) lowers it %.2f\u2192%.2f. So the engine predicts which drugs are vulnerable to interactions "
            "(low-extraction, capacity-limited) and which are buffered (high-extraction, flow-limited) \u2014 the mirror of the "
            "shunt result, under a perturbed CLint rather than a perturbed flow.</p>"
            % (eq_fig(*e), d17["CLint_elasticity_lowE"], d17["CLint_elasticity_highE"],
               d17["lowE_F_base"], d17["lowE_F_inhibited"], d17["lowE_F_base"], d17["lowE_F_induced"])),
        "eq_inline":3,"eq_display":1})

    # =====================================================================
    #  ONCOLOGY THERAPEUTIC-TARGET LAYER (sections 20-21) -- circulatory's
    #  distinctive, falsifiable contribution: from barrier collapse (root) to
    #  barrier restoration (treatment). Numbers regenerated from the battery.
    # =====================================================================
    d18=dis["T18"]; d19=dis["T19"]; d20=dis["T20"]; d21=dis["T21"]
    SLUG_SYN = "/%s/%s/" % (pid, slugify(9, "Hepatocellular carcinoma and aflatoxin HBV synergy"))
    CARD_SYN = vp_card("hcc-synergy", "RR_comb = RR_a &times; RR_v",
        "additive R19 barrier decrements make carcinogen risks multiply (aflatoxin&times;HBV &asymp; 72), parameter-free (&sect;9).", "V", SLUG_SYN)
    rcc=d18["RCC"]; hcc_=d18["HCC"]

    e = write_eq_svg(docs, code, "20", 1,
        r"\text{revert} \iff |h|<h_{sp}=2(\gamma/3)^{3/2};\quad \tau\sim(h_{sp}-h)^{-1/2}",
        "revert \u21d4 |h| < h_sp = 2(\u03b3/3)^1.5 ;   \u03c4 ~ (h_sp \u2212 h)^\u22121/2")
    S.append({"no":20,"title":"Carcinogenesis root: the reversibility threshold","short":"Reversibility threshold (spinodal)","tok":"H",
        "answer":("Taking the R19 root seriously, the malignant transition is REVERSIBLE by removing the carcinogen "
            "drive only below the spinodal h_sp\u2248%.2f (RCC), %.2f (HCC): past it the healthy basin has annihilated and the "
            "cell is committed. The simulated threshold equals the analytic spinodal exactly \u2014 a predicted responder "
            "boundary for de-driving therapy. Grade [H] prediction on [F]/[V] dynamics."
            % (rcc["spinodal"], hcc_["spinodal"])),
        "abstract":("Cell fate is the same R19 bistable switch whose escape barrier is &gamma;&sup2;/4 (read from the "
            "measured master-gene &gamma;); a carcinogen is a sustained drive collapsing it. This section asks the "
            "treatment question: a driven pre-malignant cell, on drive-removal, returns to health iff the drive stayed "
            "below the spinodal; beyond it the transition is irreversible. The threshold is sharp and the near-threshold "
            "reversion time diverges with the universal 1/2 fold exponent."),
        "cards":[CARD_R19],
        "body":("<h2>Why the clearance organs, and why a barrier</h2>"
            "<p>The kidney and liver meet carcinogens precisely because they are the clearance organs \u2014 aristolochic "
            "acid is concentrated by renal filtration, aflatoxin is activated by hepatic metabolism. On the R19 picture "
            "(&sect;7) each cell's fate is a bistable switch with an escape barrier &gamma;&sup2;/4 set by the measured "
            "master-gene promoter stacking energy (SIX2 &gamma;=%.4f, HHEX &gamma;=%.3f); the carcinogen is a sustained "
            "drive that lowers that barrier until the malignant crossing becomes likely.</p>%s"
            "<h3>The spinodal is a reversibility threshold</h3>"
            "<p>Start a cell in the healthy basin, apply a drive, then remove it and let it relax. Below the spinodal "
            "h_sp = 2(&gamma;/3)^1.5 the healthy basin still exists, so the cell returns to health (RCC: final state "
            "%.2f, healthy); above it the healthy basin has annihilated, the cell has fallen into the malignant basin, and "
            "drive-removal cannot retrieve it (RCC: final state +%.2f, committed). The simulated threshold "
            "(%.3f) equals the analytic spinodal (%.3f) for RCC and likewise for HCC (%.3f vs %.3f). The biological "
            "reading: <em>de-driving / differentiation therapy can revert a lesion only while it is pre-spinodal</em> \u2014 a "
            "sharp responder boundary set by how far the driver burden has pushed the cell.</p>"
            "<h3>Critical slowing: near-threshold lesions are relapse-prone</h3>"
            "<p>As the drive approaches the threshold the healthy basin goes marginally stable: its relaxation rate "
            "&lambda; = &gamma; &minus; 3 s_h&sup2; &rarr; 0, so the reversion time &tau; = 1/|&lambda;| diverges with the "
            "universal saddle-node exponent 1/2 (fitted %.3f for RCC, %.3f for HCC). A pre-malignant lesion sitting near "
            "threshold therefore reverts slowly and is easily re-driven \u2014 a predicted relapse-prone, bistable state.</p>"
            "<h3>What is, and is not, new here (honest boundary)</h3>"
            "<p>Bistable cell-fate landscapes (Waddington; Huang &amp; Kauffman) and the reversion logic behind "
            "differentiation therapy \u2014 APL with retinoic acid, IDH inhibitors in AML and glioma \u2014 are established systems "
            "biology; the reversion-on-drive-removal idea is not introduced here. What this package adds, and therefore "
            "what carries the falsifiable burden, is quantitative: (i) that the escape barrier equals &gamma;&sup2;/4 read "
            "from the measured promoter stacking energy, and (ii) that the spinodal is a sharp irreversibility threshold "
            "with a 1/2 critical exponent. The dynamics and threshold are forced [F] and reproduced [V]; the claim that a "
            "real tumour's barrier equals &gamma;&sup2;/4 is unmeasured and graded [O]/[H]. This is a testable mechanistic "
            "prediction, not clinical guidance.</p>"
            % (gK, gL, eq_fig(*e),
               rcc["pre_s_final"], rcc["post_s_final"], rcc["sim_threshold"], rcc["spinodal"],
               hcc_["sim_threshold"], hcc_["spinodal"], d19["RCC"]["fold_exponent"], d19["HCC"]["fold_exponent"])),
        "eq_inline":4,"eq_display":1})

    e = write_eq_svg(docs, code, "21", 1,
        r"\text{remove }b:\ RR_{comb}\to RR_{comb}/RR_b;\quad k\to k\,e^{-\delta/D}",
        "remove b:  RR_comb \u2192 RR_comb/RR_b ;   k \u2192 k\u00b7e^(\u2212\u03b4/D)")
    S.append({"no":21,"title":"Therapeutic leverage: de-escalation and barrier restoration","short":"De-escalation & barrier restoration","tok":"H",
        "answer":("Two prevention predictions fall out of the same kernel. Because synergistic carcinogens MULTIPLY risk, "
            "removing one DIVIDES it: dropping HBV from aflatoxin&times;HBV cuts RR %.0f\u2192%.1f (%.1f&times;), not the %.1f&times; "
            "additive thinking expects. And restoring the barrier by &delta; suppresses crossing by e^(\u2212&delta;/D) \u2014 "
            "exponential, so prevention dominates cure. Grade [H] on [F]/[V]/[L]."
            % (d20["RR_combined"], d20["remove_HBV_RR"], d20["reduction_factor"], d20["multiplicative_drop"]/max(d20["additive_drop"],1e-9))),
        "abstract":("The carcinogenesis kernel makes two quantitative prevention/treatment predictions. De-escalation: "
            "removing one of two multiplicative drivers divides the combined risk by that driver's RR (a retrodiction "
            "matching the large benefit of HBV control in aflatoxin regions). Barrier restoration: the Kramers rate makes "
            "barrier-raising suppress malignant crossing exponentially, so small reductions in drive have outsized effect."),
        "cards":[CARD_R19, CARD_SYN],
        "body":("<h2>De-escalation: removing a driver divides the risk</h2>"
            "<p>The headline synergy result (&sect;9) is that additive barrier decrements make carcinogen risks multiply: "
            "aflatoxin RR %.2f &times; HBV RR %.1f = combined %.0f. Read backwards, this is a prevention statement. Removing "
            "one driver does not subtract its excess risk \u2014 it divides the combined risk by that driver's RR. Eliminating "
            "HBV (vaccination, antivirals) takes the combined RR from %.0f to %.1f, a %.1f-fold reduction; naive additive "
            "thinking would predict only %.0f (a %.2f-fold change). The framework therefore predicts a dramatic, "
            "multiplicative benefit from removing one synergistic exposure \u2014 which matches the observed super-additive "
            "drop in hepatocellular carcinoma where HBV is controlled in aflatoxin-exposed populations.</p>%s"
            "<h3>Barrier restoration: why prevention beats cure, exponentially</h3>"
            "<p>The malignant-crossing rate is Kramers, k = k&#8320; e^(&minus;barrier/D). Any intervention that raises the "
            "effective barrier by &delta; \u2014 reducing the carcinogen drive (prevention), or a partial barrier-restoring "
            "agent \u2014 suppresses the crossing rate by e^(&minus;&delta;/D). The suppression is exponential, not "
            "proportional: with D=%.2f, restoring the barrier by 0.2 gives ~%.0f&times; fewer crossings and by 0.5 gives "
            "~%.0f&times;, where a linear expectation would predict barely a 1.3&times; effect. The log-suppression is linear "
            "in &delta; with slope &minus;1/D (%.1f). The implication is that keeping the barrier high (low drive) "
            "suppresses transformation far more than fighting an already-transformed population \u2014 the quantitative case "
            "for prevention, and for barrier-restoring rather than purely cytotoxic strategies.</p>"
            "<h3>Status</h3>"
            "<p>De-escalation (T20) is the most robust prediction \u2014 an epidemiological retrodiction \u2014 graded [V] against "
            "the cited HBV-control benefit [L]. The barrier-restoration leverage (T21) is forced by the Kramers form [F]. "
            "Both inherit the [O]/[H] caveat of &sect;20: their clinical force depends on the barrier really being "
            "&gamma;&sup2;/4 from promoter stacking energy. These are testable targets and public-health predictions, not "
            "clinical recommendations.</p>"
            % (d20["RR_aflatoxin"], d20["RR_HBV"], d20["RR_combined"], d20["RR_combined"],
               d20["remove_HBV_RR"], d20["reduction_factor"], d20["additive_naive_RR"],
               d20["RR_combined"]/max(d20["additive_naive_RR"],1e-9), eq_fig(*e), d21["D"],
               d21["fold_fewer_crossings"][2], d21["fold_fewer_crossings"][4], d21["dln_supp_d_delta"])),
        "eq_inline":4,"eq_display":1})

    # =====================================================================
    #  CARCINOGEN ROSTER + PREVENTION (sections 22-23) -- circulatory's owned
    #  cancers (RCC, HCC) covered across the FULL etiologic roster, root to
    #  prevention, per the ownership contract. Numbers from the battery.
    # =====================================================================
    d22=dis["T22"]; d23=dis["T23"]
    rcc_r=d22["RCC_roster"]; aa=d22["aristolochic_acid_UUC"]; rcc_de=d22["de_escalation"]
    hcc_r=d23["HCC_roster"]; hcc_de=d23["de_escalation"]; brk=d23["HBV_HCV_synergy_bracket"]
    xref_rcc=d22["hereditary_RCC_cross_reference"]; xref_hcc=d23["hereditary_HCC_cross_reference"]
    xref_rcc_html=xref_block(xref_rcc); xref_hcc_html=xref_block(xref_hcc)
    four_way_status=d23["four_way_combined_product_status"]

    e = write_eq_svg(docs, code, "22", 1, r"\text{remove driver }i:\ RR_{comb}\to RR_{comb}/RR_i",
        "remove driver i:  RR_comb \u2192 RR_comb / RR_i")
    S.append({"no":22,"title":"Renal cancer: the carcinogen roster and prevention","short":"Renal cancer roster & prevention","tok":"H",
        "answer":("Renal cell carcinoma's full acquired roster lands on one barrier law: tobacco (RR %.1f) and "
            "trichloroethylene (RR %.2f, IARC Group 1) each place on the kidney R19 axis at their cited risk. Removal "
            "divides combined risk (prevention). Aristolochic acid is a distinct entity \u2014 urothelial (UUC), not RCC. "
            "Grade [H] prevention on [F]/[V]/[L]."
            % (rcc_r["tobacco_smoke"]["cited_RR"], rcc_r["trichloroethylene"]["cited_RR"])),
        "abstract":("Under the ownership contract, circulatory owns the acquired, carcinogen-driven kidney cancer. Each "
            "RCC carcinogen (tobacco, trichloroethylene) is placed on the kidney R19 drive axis by inverting the barrier "
            "law at its cited relative risk; removing a driver divides the combined risk. Aristolochic acid is documented "
            "honestly as upper-tract urothelial carcinoma plus aristolochic-acid nephropathy \u2014 a different cancer, not RCC."),
        "cards":[CARD_R19],
        "body":("<h2>One barrier law, the whole roster</h2>"
            "<p>Renal cell carcinoma is the acquired, dynamics-defined kidney cancer the framework owns. Each known "
            "carcinogen is a sustained drive on the kidney R19 switch (&sect;7), placed on the drive axis by inverting the "
            "barrier law at its cited relative risk.</p>%s"
            "<h3>Tobacco and trichloroethylene</h3>"
            "<p>Tobacco smoke (RR %.1f ever-smoker) and trichloroethylene (RR %.2f; IARC Group 1, 2012) both round-trip "
            "exactly to their cited risks on the kidney axis. Trichloroethylene is notable mechanistically: its renal "
            "genotoxic metabolite acts through the same VHL pathway whose germline loss defines hereditary RCC \u2014 owned as "
            "a monogenic entity by the rare-disease volume (ownership contract), cross-referenced here. The prevention "
            "consequence is the de-escalation theorem run forward: removing a driver divides the combined risk by its RR "
            "(combined %.1f &rarr; %.2f on removing tobacco), so the highest-RR driver is the first prevention target.</p>%s"
            "<h3>Aristolochic acid is urothelial (UUC), not RCC \u2014 an honest correction</h3>"
            "<p>Aristolochic acid is frequently listed as a kidney carcinogen, but its malignancy is upper-tract "
            "<em>urothelial</em> carcinoma (UUC) together with aristolochic-acid nephropathy (a cause of CKD), carrying a "
            "specific TP53 A:T&rarr;T:A signature. It is IARC Group 1 with a dose-dependent odds ratio reported across the "
            "range %s. Two honest consequences: it is a different cancer of a different tissue (urothelium, whose master "
            "gene is unmeasured), so it is documented but not forced onto the RCC axis; and its potency (OR up to 49) "
            "exceeds the smoking-calibrated kidney axis, which saturates near RR 2.2 at the spinodal \u2014 on the framework's "
            "own logic, a hint that aristolochic acid drives cells past the irreversibility threshold. Prevention is direct: "
            "avoid Aristolochia herbal remedies.</p>"
            "<h3>Status</h3>"
            "<p>The roster placement is forced [F] and round-trips [V] to IARC/meta anchors [L]; absolute incidence is "
            "[O]. The framework's contribution is prevention and stratification \u2014 the established curative and systemic "
            "care of RCC (nephrectomy, ablation, tyrosine-kinase inhibitors, immunotherapy) is standard of care, not "
            "derived here.</p>"
            % (eq_fig(*e), rcc_r["tobacco_smoke"]["cited_RR"], rcc_r["trichloroethylene"]["cited_RR"],
               rcc_de["combined_RR_multiplicative"],
               rcc_de["per_driver_removal"]["tobacco_smoke"]["residual_RR_after_removal"],
               xref_rcc_html, aa["cited_OR_range"])),
        "cross_refs":[xref_rcc],
        "eq_inline":3,"eq_display":1})

    e = write_eq_svg(docs, code, "23", 1,
        r"\text{additive}\le RR_{obs}\le \text{multiplicative}:\ 26.5\le 115\le 178",
        "additive \u2264 RR_obs \u2264 multiplicative :  26.5 \u2264 115 \u2264 178")
    S.append({"no":23,"title":"Liver cancer: the carcinogen roster, synergy, and prevention","short":"Liver cancer roster & prevention","tok":"H",
        "answer":("Hepatocellular carcinoma's four drivers all round-trip on the liver R19 axis: aflatoxin (RR %.2f), HBV "
            "(%.1f), HCV (%.1f), ethanol (%.1f). Aflatoxin\u00d7HBV is multiplicative; HBV\u00d7HCV (observed %.0f) sits between the "
            "additive (%.0f) and multiplicative (%.0f) modes. De-escalation prioritises HBV. Grade [H] prevention on [F]/[V]/[L]."
            % (hcc_r["aflatoxin_B1"]["cited_RR"], hcc_r["chronic_HBV"]["cited_RR"], hcc_r["chronic_HCV"]["cited_RR"],
               hcc_r["heavy_ethanol"]["cited_RR"], brk["observed"], brk["additive_mode"], brk["multiplicative_mode"])),
        "abstract":("Circulatory owns the acquired liver cancer. All four HCC carcinogens place on the liver R19 axis at "
            "their cited risks; the two cited synergy datasets are bracketed by the kernel's two combination modes \u2014 "
            "aflatoxin\u00d7HBV multiplicative, HBV\u00d7HCV between additive and multiplicative \u2014 and the de-escalation theorem "
            "ranks prevention targets, HBV first."),
        "cards":[CARD_R19, CARD_SYN],
        "body":("<h2>The full roster on one axis</h2>"
            "<p>Hepatocellular carcinoma is the framework-owned acquired liver cancer. Its four IARC Group 1 drivers each "
            "place on the liver R19 drive axis by inverting the barrier law at the cited relative risk.</p>%s"
            "<h3>Four drivers, two synergies</h3>"
            "<p>Aflatoxin B1 (RR %.2f), chronic HBV (%.1f), chronic HCV (%.1f) and heavy ethanol (%.1f) all round-trip to "
            "their cited risks. The two cited synergy datasets fall exactly where the kernel's two combination modes "
            "predict: aflatoxin\u00d7HBV is multiplicative (&sect;9), while HBV\u00d7HCV co-infection (observed RR %.0f; Korean "
            "cohort) sits <em>between</em> the additive mode (%.0f) and the multiplicative mode (%.0f) \u2014 more than additive, "
            "short of the full product, at fractional position %.2f in the bracket. This is the framework's prediction that "
            "real synergies lie between the modes and approach multiplicative only as the combined drive nears the "
            "spinodal.</p>"
            "<h3>Prevention: divide, don't subtract; HBV first</h3>"
            "<p>For a multiply-exposed liver the combined risk (multiplicative mode) is the product of the driver RRs; "
            "removing any one divides it. The de-escalation theorem therefore ranks prevention by driver RR: HBV first "
            "(vaccination, nucleos(t)ide suppression), then HCV (direct-acting-antiviral cure achieving sustained "
            "virologic response), then aflatoxin reduction (grain storage), then alcohol abstinence. HCV is the cleanest "
            "case of the reversibility logic from &sect;20: curing the infection removes the drive, and post-cure HCC risk "
            "falls (though it does not vanish in already-cirrhotic livers \u2014 consistent with a partly-committed, "
            "post-threshold landscape).</p>"
            "<h3>Hereditary predisposition \u2014 a cross-volume reference</h3>"
            "<p>One predisposing route to this same liver cancer is heritable rather than exposure-driven: HFE "
            "hereditary haemochromatosis loads the liver with iron, driving cirrhosis and then HCC. It is a monogenic "
            "gene-key entity owned by the rare-disease volume (ownership contract), not re-emerged here; on the "
            "framework's logic it supplies an endogenous, heritable drive on the very liver R19 axis that the acquired "
            "carcinogens above drive exogenously.</p>%s"
            "<h3>Status</h3>"
            "<p>Roster placement and synergy bracketing are forced [F] / verified [V] against meta and cohort anchors [L]; "
            "the prevention ranking is a prediction [H]; absolute incidence is [O] and the simultaneous four-way combined "
            "product is flagged in the battery as %s. Curative and systemic care (resection, transplant, ablation, "
            "trans-arterial chemoembolisation, atezolizumab\u2013bevacizumab) is standard of care, not derived here.</p>"
            % (eq_fig(*e), hcc_r["aflatoxin_B1"]["cited_RR"], hcc_r["chronic_HBV"]["cited_RR"],
               hcc_r["chronic_HCV"]["cited_RR"], hcc_r["heavy_ethanol"]["cited_RR"],
               brk["observed"], brk["additive_mode"], brk["multiplicative_mode"], brk["position_in_bracket"],
               xref_hcc_html, four_way_status)),
        "cross_refs":[xref_hcc],
        "eq_inline":3,"eq_display":1})

    return S

def render_page(sec, slug, prev_slug, next_slug):
    pid = PAPER["paper_id"]; code = PAPER["code"]; dom = PAPER["domain"]; short = PAPER["short"]
    N = sec["no"]; tok = sec["tok"]
    canon = "%s/%s/%s/" % (dom, pid, slug)
    repro = "%s/tree/main/repro/%s/%s/" % (PAPER["repo"], pid, slug)
    title_txt = "%s &mdash; %s &sect;%d | Jamming Physics" % (sec["short"], short, N)
    desc = re.sub("<[^>]+>", "", sec["answer"])[:158]
    ispart = ('"isPartOf":{"@type":"CreativeWork","name":%s%s}' % (
        json.dumps(PAPER["title"]),
        (',"sameAs":"https://doi.org/%s"' % (PAPER["doi"] or PAPER["concept_doi"]))
            if (PAPER["doi"] or PAPER["concept_doi"]) else ""))
    ld_article = ('{"@context":"https://schema.org","@type":"ScholarlyArticle",'
        '"headline":%s,%s,"position":%d,'
        '"author":{"@type":"Person","name":%s,"sameAs":%s},'
        '"license":%s,"inLanguage":"en","isAccessibleForFree":true,'
        '"keywords":%s,"knowsAbout":%s,'
        '"isBasedOn":%s}' % (
        json.dumps(sec["short"]), ispart, N,
        json.dumps(PAPER["author"]), json.dumps(PAPER["orcid"]), json.dumps(PAPER["license"]),
        json.dumps(keywords_csv(N)), knows_about_json(N),
        json.dumps(repro)))
    ld_crumb = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"%s/"},'
        '{"@type":"ListItem","position":2,"name":%s,"item":"%s/%s/"},'
        '{"@type":"ListItem","position":3,"name":%s}]}' % (
        dom, json.dumps(short), dom, pid, json.dumps("\u00a7%d %s" % (N, sec["short"]))))
    _doi_disp = PAPER["doi"] or PAPER["concept_doi"]
    doi_link = ('<a href="https://doi.org/%s" rel="noopener">%s</a>'
                % (_doi_disp, "DOI snapshot" if PAPER["doi"] else "DOI (concept)")) if _doi_disp \
        else '<span class="doi-pending">DOI: pending (v%s)</span>' % PAPER["version"]
    cards = "\n".join(sec["cards"])
    prev_a = ('<a rel="prev" href="/%s/%s/">&larr; &sect;%d</a>' % (pid, prev_slug, N-1)) if prev_slug else '<span></span>'
    next_a = ('<a rel="next" href="/%s/%s/">&sect;%d &rarr;</a>' % (pid, next_slug, N+1)) if next_slug else '<span></span>'
    owner_html = ('<aside class="ownership-banner" role="note"><b>Scope &middot; ownership contract.</b> %s</aside>\n\n'
                  % sec["owner"]) if sec.get("owner") else ""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld_article}
</script>
<script type="application/ld+json">
{ld_crumb}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="/{pid}/">{short}</a> &rsaquo; &sect;{N}</nav></header>
<main>
<h1>{h1}</h1>

{owner}<p class="answer">{answer}</p>

<p class="abstract">{abstract}</p>

<aside class="claim-strip">
  <span class="grade {gcls}">{glabel}</span>
  <span class="gate">LOCK &rarr; Derive &rarr; Gate</span>
  <a href="{repro}" rel="noopener">Reproduce (GitHub)</a>
  {doi_link}
</aside>

{cards}

{body}

<nav class="pn">
  {prev_a}
  <a href="/{pid}/">Contents</a>
  {next_a}
</nav>
</main>
<footer>Young Jae Lee &middot; <a href="{orcid}" rel="noopener">ORCID 0009-0002-7535-8245</a> &middot;
<a href="{license}" rel="noopener license">CC BY 4.0</a> &middot; Jamming Physics &middot; v{ver}</footer>
</body>
</html>
""".format(title=title_txt, desc=html.escape(desc, quote=True), canon=canon, ld_article=ld_article,
           ld_crumb=ld_crumb, pid=pid, short=short, N=N, h1=html.escape(sec["title"]),
           answer=sec["answer"], abstract=sec["abstract"], gcls=grade_class(tok), glabel=grade_label(tok),
           repro=repro, doi_link=doi_link, cards=cards, body=sec["body"], prev_a=prev_a, next_a=next_a,
           owner=owner_html, keywords=html.escape(keywords_csv(N), quote=True),
           orcid=PAPER["orcid"], license=PAPER["license"], ver=PAPER["version"])


def render_hub(secs, sha):
    pid = PAPER["paper_id"]; dom = PAPER["domain"]; short = PAPER["short"]
    items = []
    for s in secs:
        slug = slugify(s["no"], s["title"])
        items.append('<li><a href="/%s/%s/"><span class="n">&sect;%d</span> %s</a> '
                     '<span class="g %s">%s</span></li>' % (
            pid, slug, s["no"], html.escape(s["title"]), grade_class(s["tok"]), grade_label(s["tok"]).split()[0]))
    ld = ('{"@context":"https://schema.org","@type":"CreativeWorkSeries","name":%s,'
          '"author":{"@type":"Person","name":%s,"sameAs":%s},"license":%s,"inLanguage":"en",'
          '"description":"Organs emerged from measured human master-gene promoter thermodynamics, then a full transport and clearance physiology, fourteen disease states, drug pharmacokinetics and a carcinogenesis kernel derived deterministically and graded.",'
          '"keywords":"organ emergence from DNA, jamming physics, vacuum as jammed medium, hemodynamics MAP CO SVR, Windkessel model, glomerular filtration autoregulation, tubuloglomerular feedback, osmoregulation ADH, hepatic clearance bioavailability, carcinogenesis dose-response, aflatoxin HBV synergy, renal cell carcinoma, hepatocellular carcinoma",'
          '"knowsAbout":["jamming lattice substrate","R19 bistable cell-fate switch","master-gene gamma","SIX2 kidney","HHEX liver","mean arterial pressure","Windkessel","tubuloglomerular feedback","osmoregulation","well-stirred hepatic clearance","Kramers barrier-lowering carcinogenesis","aflatoxin hepatitis B synergy"],'
          '"about":"vacuum-as-jammed-medium circulatory transport, renal filtration, hepatic clearance, carcinogen dose-response"}' % (
        json.dumps(PAPER["title"]), json.dumps(PAPER["author"]), json.dumps(PAPER["orcid"]),
        json.dumps(PAPER["license"])))
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{short} | Jamming Physics</title>
<meta name="description" content="Organs emerged from measured human master-gene DNA thermodynamics, then a full transport-clearance physiology: MAP=CO×SVR, Windkessel τ=RC, GFR autoregulation, osmoregulation, hepatic clearance, plus 14 disease states and a carcinogenesis kernel (aflatoxin×HBV synergy, RCC, HCC) — each graded and deterministically reproducible.">
<meta name="keywords" content="organ emergence from DNA, jamming physics, vacuum as jammed medium, hemodynamics, MAP CO SVR formula, Windkessel model, glomerular filtration rate autoregulation, tubuloglomerular feedback, osmoregulation ADH vasopressin, hepatic clearance oral bioavailability, well-stirred model, carcinogenesis dose-response, aflatoxin hepatitis B liver cancer synergy, renal cell carcinoma smoking risk, hepatocellular carcinoma, deterministic reproducible simulation">
<link rel="canonical" href="{dom}/{pid}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; {short}</nav></header>
<main>
<h1>{title}</h1>
<p class="answer">The kidney, liver and circulation are built as one pressure-flow and clearance network from one premise &mdash; the vacuum as a jammed medium. The organs are not assumed: they <b>emerge from measured human master-gene DNA</b> (SIX2, HHEX stacking energy &gamma;), and hemodynamics, renal filtration, osmoregulation, hepatic clearance, fourteen disease states and a carcinogenesis kernel follow deterministically.</p>
<aside class="method-panel" role="note">
<p><b>What this is &mdash; and what it is not.</b> Not a curve-fit and not a toy demo. It is a deterministic, end-to-end pipeline: a quantity &gamma; read directly from the organism's own promoter DNA (SantaLucia 1998 nearest-neighbour thermodynamics, never fitted) sets a bistable cell-fate switch; the switch fixes which organ appears, in what order, and at what relative size; and the emerged organs then reproduce <b>23 quantitative targets</b> spanning hemodynamics, renal filtration, osmoregulation, hepatic pharmacokinetics, and carcinogenesis &mdash; all from one substrate with no free biological parameter. Two independent runs give a byte-identical result digest.</p>
<p>New to the framework? Start with the <a href="/{pid}/about/">overview: how organs are emerged from DNA, and the full scope</a>.</p>
</aside>
<p class="hub-lead">This volume is derived from <a href="/physics/">VP Theory (jamming branch)</a>. The shared R19 switch and &gamma; are common to the <a href="/dna/">DNA</a> and <a href="/neuro/">neural</a> volumes.</p>
<ol class="toc">
{items}
</ol>
<p class="repro-note">Every claim carries an honest grade [F] forced / [V] simulation-verified / [L] literature-anchored / [O] open, and a deterministic reproduction path. All 23 discriminant targets pass; two independent runs give the byte-identical result digest <code>{sha}</code>. Reproduction code (stdlib-only, offline): <a href="{repo}" rel="noopener">{repo}</a>.</p>
</main>
<footer>Young Jae Lee &middot; <a href="{orcid}" rel="noopener">ORCID 0009-0002-7535-8245</a> &middot;
<a href="{license}" rel="noopener license">CC BY 4.0</a> &middot; v{ver}</footer>
</body>
</html>
""".format(short=short, dom=dom, pid=pid, ld=ld, title=html.escape(PAPER["title"]),
           items="\n".join(items), sha=sha[:16], repo=PAPER["repo"], orcid=PAPER["orcid"],
           license=PAPER["license"], ver=PAPER["version"])


def render_about(D, secs):
    """Dedicated overview page (/{paper_id}/about/): the answer-first, keyword-rich, self-contained
    statement of what the volume IS -- organs emerged from measured promoter DNA, the deterministic
    cascade from gamma to physiology to disease to oncology, and the reproducibility discipline.
    A standalone retrieval surface (VP-SPEC v1.8 C4) so a cold search reader meets the full scope,
    not a single section. Numbers are live from the engine; no claim is introduced here that the
    chapters do not carry."""
    pid = PAPER["paper_id"]; dom = PAPER["domain"]; short = PAPER["short"]
    c = D["c"]; hemo = c["hemodynamics"]; ren = c["renal"]; osm = c["osmoregulation"]; hep = c["hepatic"]
    organs = {o["organ"]: o for o in c["organs"]["organs"]}
    gK = organs["kidney"]["gamma"]; gL = organs["liver"]["gamma"]
    szK = organs["kidney"]["rel_size_dwell"]; szL = organs["liver"]["rel_size_dwell"]
    hcc = D["hcc"]["value"]; sha = D["sha"]
    n_sec = len(secs)
    canon = "%s/%s/about/" % (dom, pid)
    ld = ('{"@context":"https://schema.org","@type":"TechArticle",'
          '"headline":"How organs are emerged from DNA, and the full scope of the Circulatory Transport volume",'
          '"inLanguage":"en","isAccessibleForFree":true,'
          '"author":{"@type":"Person","name":%s,"sameAs":%s},"license":%s,'
          '"isPartOf":{"@type":"CreativeWorkSeries","name":%s},'
          '"keywords":"organ emergence from DNA, jamming physics, vacuum as jammed medium, master gene gamma, SantaLucia 1998 nearest-neighbour thermodynamics, R19 bistable cell-fate switch, deterministic reproducible simulation, hemodynamics, renal filtration, hepatic clearance, carcinogenesis dose-response",'
          '"knowsAbout":["organ emergence from promoter DNA","jamming lattice substrate","R19 bistable switch","master-gene gamma","SIX2","HHEX","developmental order spinodal","Windkessel hemodynamics","tubuloglomerular feedback","osmoregulation","well-stirred hepatic clearance","Kramers carcinogenesis"]}' % (
        json.dumps(PAPER["author"]), json.dumps(PAPER["orcid"]), json.dumps(PAPER["license"]),
        json.dumps(PAPER["title"])))
    crumb = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"%s/"},'
        '{"@type":"ListItem","position":2,"name":%s,"item":"%s/%s/"},'
        '{"@type":"ListItem","position":3,"name":"Overview"}]}' % (
        dom, json.dumps(short), dom, pid))
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>How organs emerge from DNA &mdash; {short} overview | Jamming Physics</title>
<meta name="description" content="An overview of the Circulatory Transport volume: organs emerged from measured human master-gene promoter DNA (SantaLucia 1998 thermodynamics, never fitted), then a deterministic cascade to hemodynamics, renal filtration, osmoregulation, hepatic pharmacokinetics, 14 disease states and a carcinogenesis kernel — 23 targets, all reproducible.">
<meta name="keywords" content="organ emergence from DNA, grounded simulation, jamming physics, vacuum as jammed medium, master gene gamma, SIX2 HHEX promoter, SantaLucia 1998 nearest-neighbour thermodynamics, R19 bistable cell-fate switch, developmental order spinodal, deterministic reproducible model, hemodynamics MAP CO SVR, Windkessel, glomerular filtration autoregulation, tubuloglomerular feedback, osmoregulation ADH, hepatic clearance bioavailability, carcinogenesis Kramers dose-response, aflatoxin HBV synergy, renal cell carcinoma, hepatocellular carcinoma">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld}
</script>
<script type="application/ld+json">
{crumb}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="/{pid}/">{short}</a> &rsaquo; Overview</nav></header>
<main>
<h1>How organs are emerged from DNA &mdash; and the full scope of this volume</h1>

<p class="answer">This volume emerges the kidney and liver from one premise &mdash; the vacuum as a jammed medium &mdash; and a quantity read directly from the organism's own DNA: each master gene's promoter stacking energy &gamma;, measured by SantaLucia&nbsp;1998 thermodynamics, never fitted. From them a full transport-clearance physiology, fourteen disease states and a carcinogenesis kernel follow deterministically across 23 reproducible targets.</p>

<p class="lede">A note on how to read this work: it is a <b>grounded, mechanistic simulation</b>, not a curve-fit and not an illustrative toy. The starting number comes from real human reference DNA; every downstream value is regenerated by deterministic, standard-library code; and every claim carries an explicit grade and a one-command reproduction path. The sections below state the method, the cascade, the scope, and the discipline in full.</p>

<h2>1. One premise, one substrate</h2>
<p>The whole VP program takes a single hypothesis &mdash; that the physical vacuum behaves as a jammed granular medium &mdash; and derives physics across many domains from it. The microscopic carrier shared across the DNA, neural and circulatory volumes is the <b>R19 bistable switch</b>, ds/dt = &gamma;s &minus; s&sup3; + h: a double-well cell-fate switch whose barrier is &gamma;&sup2;/4 and whose spinodal (the drive past which one state vanishes discontinuously) is 2(&gamma;/3)^1.5. The same switch that decides a base-pair register in the DNA volume, and a neuron's firing in the neural volume, decides whether an organ is present here. Nothing in this volume re-derives the substrate; it is vendored and reused.</p>

<h2>2. Organs are emerged from measured promoter DNA, never fitted</h2>
<p>The threshold scale &gamma; of each organ's switch is not a free knob. It is the mean nearest-neighbour base-stacking free energy of the master gene's proximal promoter, computed with the SantaLucia&nbsp;1998 unified nearest-neighbour parameters from the exact human reference sequence (window TSS&minus;2000..+500). The values are read-only measurements cached for bit-for-bit offline reproduction:</p>
<table class="keytable">
<thead><tr><th>Master gene</th><th>Organ</th><th>Source (NCBI)</th><th>Measured &gamma;</th><th>Relative size (DWELL)</th></tr></thead>
<tbody>
<tr><td><b>SIX2</b></td><td>kidney (metanephric nephron)</td><td><code>NC_000002.12</code>, chr2</td><td>{gK}</td><td>{szK}</td></tr>
<tr><td><b>HHEX</b></td><td>liver (hepatic clearance)</td><td><code>NC_000010.11</code>, chr10</td><td>{gL}</td><td>{szL}</td></tr>
<tr><td>(diffuse mesoderm)</td><td>vasculature (pressure-flow)</td><td>no single master gene</td><td>&mdash;</td><td>&mdash;</td></tr>
</tbody>
</table>
<p>Because &gamma;(SIX2) &gt; &gamma;(HHEX), the liver's switch crosses threshold before the kidney's: the developmental order <b>liver &rarr; kidney</b> is a pure readout of measured DNA, not an imposed sequence. DWELL &prop; &gamma;^1.5 then sets relative organ size. The direction and order are forced; only the absolute size needs one external growth-duration constant, which is logged honestly as open rather than fitted.</p>

<h2>3. The deterministic cascade: from &gamma; to physiology to disease to cancer</h2>
<p>From the emerged organs, the entire network follows with no free biological parameter. Each step is a forced relation exercised by a wide-sweep stress battery and paired with a contrast so that passing means a mechanism, not a tuned point:</p>
<ol class="chain">
<li><b>Emergence</b> &mdash; measured &gamma; &rarr; organ identity, developmental order (spinodal), relative size (DWELL).</li>
<li><b>Hemodynamics</b> &mdash; the cardiac pump boundary condition drives a two-element Windkessel: mean arterial pressure MAP = CO&times;SVR ({hemo_map} mmHg, with SBP/DBP {hemo_sbp}/{hemo_dbp}), and the diastolic decay constant &tau; = R&times;C.</li>
<li><b>Renal filtration</b> &mdash; Starling forces set glomerular filtration; tubuloglomerular feedback holds GFR flat ({gfr} mL/min) across an 80&ndash;180 mmHg perfusion band while the open loop does not.</li>
<li><b>Osmoregulation</b> &mdash; the ADH/thirst negative-feedback loop defends plasma osmolality to a setpoint ({osm} mOsm/kg) against imposed loads.</li>
<li><b>Hepatic clearance</b> &mdash; the well-stirred liver sets extraction E and oral bioavailability F = 1 &minus; E (propranolol E&asymp;{E}, F&asymp;{F}), with flow- vs capacity-limited regimes.</li>
<li><b>Disease as named knob-settings</b> &mdash; hypertension, isolated systolic hypertension, shock subtypes, diabetes insipidus, SIADH, CKD staging, autoregulation breakthrough, hepatic impairment, portosystemic shunt, and drug interactions are each one setting of an existing knob, not a new mechanism.</li>
<li><b>Carcinogenesis</b> &mdash; a carcinogen is a sustained aberrant drive on the same R19 switch; it lowers the escape barrier, and because crossing is Arrhenius, additive barrier decrements make relative risks multiply. The aflatoxin&times;HBV synergy in liver cancer comes out multiplicative ({hcc_comb} vs the meta-analytic {hcc_meta}) with no synergy parameter.</li>
</ol>

<h2>4. Scope at a glance</h2>
<div class="scope-grid">
<div class="cell"><b>{n_sec} sections</b><span>One page each, answer-first and self-contained for retrieval.</span></div>
<div class="cell"><b>23 discriminant targets</b><span>All pass under wide sweeps with healthy/opposite contrasts.</span></div>
<div class="cell"><b>3 organs, 1 substrate</b><span>Kidney, liver, vasculature on the shared R19 switch.</span></div>
<div class="cell"><b>14 disease states</b><span>Each a named setting of an existing engine knob.</span></div>
<div class="cell"><b>2 cancers, full rosters</b><span>RCC and HCC carcinogen rosters with cited epidemiology.</span></div>
<div class="cell"><b>Deterministic</b><span>Two runs &rarr; identical digest <code>{sha}</code>.</span></div>
</div>

<h2>5. The discipline: honest grades and bit-for-bit reproduction</h2>
<p>Every quantitative claim carries one of four grades, kept visible on each page: <b>[F]</b> forced (the relation is structurally derived), <b>[V]</b> simulation-verified (the engine reproduces the cited operating point), <b>[L]</b> literature-anchored (an absolute input is a cited measurement), and <b>[O]</b> open (a value is not yet reproducible, with the obstacle stated). Absolute organ mass and absolute cancer incidence are marked [O] with their obstacles named, never fitted to look settled. The reproduction code is standard-library-only and runs offline; two independent executions yield the byte-identical result digest above. This is the difference between a grounded derivation and a fitted picture: the reader can re-run it and get the same numbers.</p>

<p class="repro-note">Read the full volume from the <a href="/{pid}/">contents</a>, or start with <a href="/{pid}/01-organ-emergence-measured/">&sect;1 Organ emergence from measured &gamma;</a>. Reproduction code (stdlib-only, offline): <a href="{repo}" rel="noopener">{repo}</a>. Author: Young Jae Lee (<a href="{orcid}" rel="noopener">ORCID 0009-0002-7535-8245</a>), CC BY 4.0.</p>
</main>
<footer>Young Jae Lee &middot; <a href="{orcid}" rel="noopener">ORCID 0009-0002-7535-8245</a> &middot;
<a href="{license}" rel="noopener license">CC BY 4.0</a> &middot; Jamming Physics &middot; v{ver}</footer>
</body>
</html>
""".format(short=short, canon=canon, ld=ld, crumb=crumb, pid=pid,
           gK=("%.4f" % gK), gL=("%.3f" % gL), szK=("%.3f" % szK), szL=("%.3f" % szL),
           hemo_map=("%.1f" % hemo["MAP_mmHg"]), hemo_sbp=("%.0f" % hemo["SBP_mmHg"]),
           hemo_dbp=("%.0f" % hemo["DBP_mmHg"]), gfr=("%.0f" % ren["GFR_mL_min"]),
           osm=("%.0f" % osm["osm_rest"]), E=("%.2f" % hep["E"]), F=("%.2f" % hep["F"]),
           hcc_comb=("%.0f" % hcc["modelA_additive_decrements"]["RR_combined"]),
           hcc_meta=("%.0f" % hcc["modelA_additive_decrements"]["meta_observed"]), n_sec=n_sec, sha=sha[:16],
           repo=PAPER["repo"], orcid=PAPER["orcid"], license=PAPER["license"], ver=PAPER["version"])


SITE_CSS = """:root{--ink:#16202c;--mut:#5a6b7b;--line:#dce4ec;--bg:#fff;--card:#f4f8fb;--acc:#0b6;--accw:#b91c1c;--accc:#1d6fb8}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;color:var(--ink);background:var(--bg);font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:760px;margin:0 auto;padding:0 20px 64px}
header,footer{max-width:760px;margin:0 auto;padding:16px 20px;color:var(--mut);font-size:13.5px}
footer{border-top:1px solid var(--line);margin-top:48px}
a{color:var(--accc);text-decoration:none}a:hover{text-decoration:underline}
.crumb a{color:var(--mut)}
h1{font-size:1.72rem;line-height:1.25;margin:.4em 0 .5em}
h2{font-size:1.24rem;margin:1.8em 0 .5em;padding-top:.3em}
h3{font-size:1.05rem;margin:1.4em 0 .4em;color:#27384a}
p{margin:.75em 0}
.answer{font-size:1.12rem;line-height:1.6;background:var(--card);border-left:4px solid var(--acc);padding:14px 16px;border-radius:0 8px 8px 0;margin:1em 0}
.abstract{color:#27384a}
.claim-strip{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;font-size:13px;border:1px solid var(--line);background:#fafcfe;border-radius:10px;padding:10px 14px;margin:1.1em 0}
.claim-strip .gate{color:var(--mut)}
.grade{font-weight:700;padding:2px 9px;border-radius:999px;font-size:12px}
.g-forced{background:#e7f7ee;color:#0a7a44}.g-verified{background:#e8f1fb;color:#15589c}
.g-calibrated{background:#fff4e5;color:#9a6400}.g-hypothesis{background:#f3eafc;color:#6b39a8}.g-open{background:#fdeaea;color:var(--accw)}
.doi-pending{color:var(--mut)}
.vp-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:.8em 0;font-size:14.5px}
.vp-card b:first-child{color:#0a3d62}
.ownership-banner{font-size:13.5px;line-height:1.5;color:#5a4a2a;background:#fbf6ec;border:1px solid #ecdcb8;border-left:4px solid #c79a3a;border-radius:0 8px 8px 0;padding:9px 14px;margin:.6em 0 1.1em}
.ownership-banner b{color:#7a5a14}
.xref-card{display:block;font-size:13.5px;line-height:1.55;color:#28323e;background:#f1f5fb;border:1px solid #d3e0f0;border-left:4px solid #3a6ea5;border-radius:0 8px 8px 0;padding:10px 14px;margin:1em 0}
.xref-card>b:first-child{color:#234c77}
.xref-card code{background:#e3ecf7;color:#1d3a5c;padding:1px 5px;border-radius:4px;font-size:12.5px}
.xref-card .xref-grade{display:inline-block;margin-top:.5em;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;color:#3a6ea5}
.xref-card .xref-cite{display:block;margin-top:.35em;font-size:12px;color:#5a6b7d}
figure.eq{margin:1.1em 0;overflow-x:auto;text-align:center}
figure.eq img{max-width:100%;height:auto}
nav.pn{display:flex;justify-content:space-between;gap:12px;margin:2.4em 0 0;padding-top:14px;border-top:1px solid var(--line);font-size:14px}
ol.toc{list-style:none;padding:0;margin:1.2em 0}
ol.toc li{display:flex;align-items:baseline;gap:10px;padding:9px 0;border-bottom:1px solid var(--line)}
ol.toc .n{color:var(--mut);font-variant-numeric:tabular-nums;min-width:2.4em}
ol.toc .g{margin-left:auto;font-size:11px;padding:1px 7px;border-radius:999px}
.hub-lead{color:var(--mut)}.repro-note{font-size:13.5px;color:var(--mut);border-top:1px solid var(--line);padding-top:14px;margin-top:24px}
code{background:#eef3f7;padding:1px 5px;border-radius:5px;font-size:.92em}
.method-panel{background:#f4f8fb;border:1px solid #d3e0f0;border-left:4px solid var(--accc);border-radius:0 10px 10px 0;padding:4px 16px;margin:1.2em 0;font-size:14.5px}
.method-panel b{color:#0a3d62}
.lede{font-size:1.05rem;color:#27384a;margin:1em 0}
.scope-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:1.3em 0}
.scope-grid .cell{border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:#fafcfe}
.scope-grid .cell b{color:#0a3d62;display:block;margin-bottom:3px}
.scope-grid .cell span{font-size:13px;color:var(--mut)}
.chain{list-style:none;padding:0;margin:1.2em 0;counter-reset:step}
.chain li{position:relative;padding:10px 0 10px 40px;border-bottom:1px solid var(--line)}
.chain li::before{counter-increment:step;content:counter(step);position:absolute;left:0;top:10px;width:26px;height:26px;border-radius:50%;background:var(--accc);color:#fff;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center}
.chain li b{color:#0a3d62}
.keytable{width:100%;border-collapse:collapse;margin:1.2em 0;font-size:14px}
.keytable th,.keytable td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.keytable th{color:var(--mut);font-weight:600;font-size:12.5px;text-transform:uppercase;letter-spacing:.02em}
.keytable code{font-size:12.5px}
"""



def render_site_index():
    pid = PAPER["paper_id"]; dom = PAPER["domain"]; short = PAPER["short"]
    ld = ('{"@context":"https://schema.org","@type":"CollectionPage","name":"Jamming Physics",'
          '"hasPart":{"@type":"CreativeWorkSeries","name":%s,"url":"%s/%s/"},'
          '"author":{"@type":"Person","name":%s,"sameAs":%s}}' % (
        json.dumps(PAPER["title"]), dom, pid, json.dumps(PAPER["author"]), json.dumps(PAPER["orcid"])))
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jamming Physics</title>
<meta name="description" content="The vacuum as a jammed granular medium: a multi-volume research program deriving physics across domains from one premise. This deployment hosts the Circulatory Transport and Clearance volume — organs emerged from measured DNA, then hemodynamics, renal filtration, hepatic clearance and a carcinogenesis kernel, deterministically reproduced.">
<meta name="keywords" content="jamming physics, vacuum as jammed medium, organ emergence from DNA, circulatory transport, hemodynamics, renal filtration, hepatic clearance, carcinogenesis dose-response, deterministic reproducible physics">
<link rel="canonical" href="{dom}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<header><nav class="crumb">Jamming Physics</nav></header>
<main>
<h1>Jamming Physics</h1>
<p class="answer">Jamming Physics models the vacuum as a jammed granular medium and derives physics across many domains from that single premise. This deployment hosts the <a href="/{pid}/">Circulatory Transport and Clearance</a> volume &mdash; where the kidney and liver are emerged from measured human master-gene DNA, and a full pressure-flow and clearance physiology, fourteen disease states and a shared R19 carcinogenesis kernel follow deterministically.</p>
<ol class="toc">
<li><a href="/{pid}/"><span class="n">Vol</span> {short} &mdash; hemodynamics, renal filtration, hepatic clearance, carcinogen dose-response</a></li>
<li><a href="/{pid}/about/"><span class="n">&rsaquo;</span> Overview &mdash; how organs are emerged from DNA, and the full scope</a></li>
</ol>
<p class="repro-note">Author: Young Jae Lee (<a href="{orcid}" rel="noopener">ORCID 0009-0002-7535-8245</a>). CC BY 4.0. Code: <a href="{repo}" rel="noopener">{repo}</a>.</p>
</main>
<footer>Young Jae Lee &middot; CC BY 4.0 &middot; v{ver}</footer>
</body>
</html>
""".format(dom=dom, ld=ld, pid=pid, short=short, orcid=PAPER["orcid"], repo=PAPER["repo"], ver=PAPER["version"])


def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Do the research first: pass the stress battery, then")
        print("  gates.write_research_complete();  echo writing > PHASE")
        return 1

    D = gather()
    docs = os.path.join(_PKG, "docs")
    pid = PAPER["paper_id"]
    paper_dir = os.path.join(docs, pid)                       # served at /{paper_id}/ (canonical URL folder)
    os.makedirs(paper_dir, exist_ok=True)
    os.makedirs(os.path.join(docs, "assets", "css"), exist_ok=True)
    secs = build_sections(D, docs)                            # eq SVGs -> docs/eq/{pid}/ (site-root absolute)
    slugs = [slugify(s["no"], s["title"]) for s in secs]

    # per-section pages  ->  docs/{paper_id}/{slug}/index.html
    for i, s in enumerate(secs):
        slug = slugs[i]
        prev_slug = slugs[i-1] if i > 0 else None
        next_slug = slugs[i+1] if i < len(secs)-1 else None
        d = os.path.join(paper_dir, slug); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            render_page(s, slug, prev_slug, next_slug))

    # paper hub  ->  docs/{paper_id}/index.html   (served at /{paper_id}/)
    open(os.path.join(paper_dir, "index.html"), "w", encoding="utf-8").write(render_hub(secs, D["sha"]))
    # volume overview  ->  docs/{paper_id}/about/index.html  (served at /{paper_id}/about/, C4 retrieval surface)
    about_dir = os.path.join(paper_dir, "about"); os.makedirs(about_dir, exist_ok=True)
    open(os.path.join(about_dir, "index.html"), "w", encoding="utf-8").write(render_about(D, secs))
    # site-root landing  ->  docs/index.html (served at /), links to the paper hub (section 11)
    open(os.path.join(docs, "index.html"), "w", encoding="utf-8").write(render_site_index())
    # css
    open(os.path.join(docs, "assets", "css", "site.css"), "w", encoding="utf-8").write(SITE_CSS)

    # _meta.json (section 9)
    pid = PAPER["paper_id"]
    meta = {"paper_id": pid, "code": PAPER["code"], "title": PAPER["title"], "short": PAPER["short"],
            "doi": PAPER["doi"], "concept_doi": PAPER["concept_doi"],
            "cross_volume_doi": PAPER["cross_volume_doi"], "publication_status": PAPER["pub_status"],
            "hub_url": "/%s/" % pid, "branch": PAPER["branch"],
            "version": PAPER["version"], "result_sha256": D["sha"],
            "abstract": ("The kidney and liver are emerged from measured human master-gene promoter DNA (SIX2, HHEX "
                         "stacking energy gamma; SantaLucia 1998, never fitted); from them a full transport-clearance "
                         "physiology (MAP=CO*SVR, Windkessel tau=RC, GFR autoregulation, osmoregulation, hepatic "
                         "first-pass clearance), 14 disease states and a shared R19 carcinogen dose-response follow "
                         "deterministically across 23 reproducible targets."),
            "headline_results": ["MAP = CO x SVR", "tau = R x C", "GFR autoregulation plateau",
                                 "F = 1 - E (well-stirred)", "aflatoxin x HBV: additive decrements => multiplicative RR (~72 vs 73)"],
            "chapters": [{"no": s["no"], "slug": slugs[i], "title": s["title"],
                          "grade": grade_class(s["tok"]).split("-")[1], "eq_inline": s["eq_inline"],
                          "eq_display": s["eq_display"],
                          "owner_note": (re.sub("<[^>]+>", "", s["owner"]) if s.get("owner") else None),
                          "cross_references": s.get("cross_refs")}
                         for i, s in enumerate(secs)],
            "totals": {"chapters": len(secs),
                       "eq_display": sum(s["eq_display"] for s in secs),
                       "eq_inline": sum(s["eq_inline"] for s in secs)}}
    os.makedirs(os.path.join(docs, pid), exist_ok=True)
    json.dump(meta, open(os.path.join(docs, pid, "_meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # sitemap.xml
    urls = ["%s/" % PAPER["domain"], "%s/%s/" % (PAPER["domain"], pid),
            "%s/%s/about/" % (PAPER["domain"], pid)] + \
           ["%s/%s/%s/" % (PAPER["domain"], pid, sl) for sl in slugs]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>%s</loc></url>" % u)
    sm.append("</urlset>\n")
    open(os.path.join(docs, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))

    # robots.txt (7 bots allowed, section 6-R.5)
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    rb = []
    for bdir in bots:
        rb.append("User-agent: %s\nAllow: /\n" % bdir)
    rb.append("User-agent: *\nAllow: /\n")
    rb.append("Sitemap: %s/sitemap.xml\n" % PAPER["domain"])
    open(os.path.join(docs, "robots.txt"), "w", encoding="utf-8").write("\n".join(rb))

    # llms.txt (<5KB)
    lines = ["# %s" % PAPER["title"], "",
             "> A grounded, deterministic derivation -- not a curve-fit or a toy. The kidney and liver are EMERGED",
             "> from measured human master-gene promoter DNA (SIX2, HHEX stacking energy gamma; SantaLucia 1998",
             "> nearest-neighbour thermodynamics, never fitted), and from them a full transport-clearance physiology,",
             "> 14 disease states, drug pharmacokinetics and a shared R19 carcinogenesis kernel follow across 23",
             "> reproducible targets. Every claim carries an honest grade [F]/[V]/[L]/[O]; two runs give an identical digest.", "",
             "Author: %s (ORCID 0009-0002-7535-8245). License: CC BY 4.0. Version: %s." % (PAPER["author"], PAPER["version"]),
             "Reproduction code: %s" % PAPER["repo"], "",
             "## Core",
             "- [Overview: how organs are emerged from DNA + full scope](%s/%s/about/)" % (PAPER["domain"], pid),
             "- [%s hub](%s/%s/)" % (PAPER["short"], PAPER["domain"], pid)]
    for i, s in enumerate(secs):
        lines.append("- [%s](%s/%s/%s/) %s" % (
            s["short"], PAPER["domain"], pid, slugs[i], grade_label(s["tok"]).split()[0]))
    lines += ["", "## Headline results",
              "- MAP = CO x SVR (forced); Windkessel tau = R x C (forced).",
              "- GFR autoregulation plateau via tubuloglomerular feedback (verified).",
              "- Hepatic well-stirred F = 1 - E; flow- vs capacity-limited by clearance elasticity (forced/cited).",
              "- aflatoxin x HBV: additive barrier decrements => exactly multiplicative RR (~72 vs meta 73), parameter-free (verified).", ""]
    txt = "\n".join(lines)
    open(os.path.join(docs, "llms.txt"), "w", encoding="utf-8").write(txt)

    # manifest (section 3)
    man = os.path.join(_PKG, "manifest", "circulatory_vp_site.csv")
    os.makedirs(os.path.dirname(man), exist_ok=True)
    rows = ["slug,title,section_no,status,grade,words,eq_display"]
    for i, s in enumerate(secs):
        body_words = len(re.sub("<[^>]+>", " ", s["body"]).split())
        rows.append('%s,"%s",%d,published,%s,%d,%d' % (
            slugs[i], s["title"].replace('"', "'"), s["no"], grade_class(s["tok"]).split("-")[1],
            body_words, s["eq_display"]))
    open(man, "w", encoding="utf-8").write("\n".join(rows) + "\n")

    print("UNLOCKED -> emitted canonical SEO HTML into docs/:")
    print("  %d section pages + hub; sitemap (%d urls); robots (%d bots); llms.txt (%d bytes); _meta.json; site.css" % (
        len(secs), len(urls), len(bots), len(txt.encode("utf-8"))))
    print("  result_sha256 =", D["sha"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
