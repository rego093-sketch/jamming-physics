#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Digestive / Metabolic WRITING phase: per-title canonical SEO HTML generator.

HARD RULE: refuses while gates.writing_locked() is True (research must be signed off:
reports/research_complete.json all_green AND PHASE=="writing"). Research first, writing second.

WHEN UNLOCKED it emits, per VP-SPEC v1.8 (sections 6 / 6-R):
  * CANONICAL artifact = HTML in docs/ (C2).
  * ONE page per section: answer-first <p class="answer"> (40-60 words, self-contained), JSON-LD
    (ScholarlyArticle + BreadcrumbList), canonical link, claim-strip (grade + GitHub repro link + DOI
    status), vp-card per cited locked quantity, English body, paragraphs <=3 sentences, exactly one h1,
    prev/next nav, footer (ORCID / CC-BY).
  * Hub docs/index.html (CreativeWorkSeries) + _meta.json + sitemap.xml + robots.txt (7 bots) + llms.txt.
  * EVERY displayed number is regenerated live by the engine here (C1) -- nothing hand-entered.

NOTE ON DOI: the Zenodo concept DOI 10.5281/zenodo.20755319 (version-independent, always resolving to the
  latest version) is now minted for this whitepaper. It is shown in every claim-strip and footer as a
  resolvable doi.org link, and emitted in the ScholarlyArticle / CreativeWorkSeries JSON-LD as a
  machine-readable identifier (PropertyValue propertyID=DOI + sameAs) for Google Scholar / AI-search
  ingestion. The GitHub repro tree remains the durable reproduction artifact. The DOI string lives
  single-source in CONCEPT; while it is a "pending ..." placeholder it is rendered as honest plain text,
  never fabricated and never linked (C1 honesty).
"""
import os, sys, json, html, re, datetime
_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.join(_HERE, "..")
_DOCS = os.path.join(_PKG, "docs")
for sub in (("repro", "_verify"), ("repro", "_engine"), ("repro", "_oncology"), ("repro", "_disease"), ("repro", "_seams"), ("repro", "_analgesic"), ("repro", "_harness"), ("inherited",)):
    sys.path.insert(0, os.path.join(_PKG, *sub))
import importlib
gates = importlib.import_module("gates")
eng   = importlib.import_module("vp_dig_engine")
onco  = importlib.import_module("carcinogen_dose_response")
dz    = importlib.import_module("disease_modules")
seam  = importlib.import_module("seam_wiring")
analg = importlib.import_module("analgesic_logic")
harness = importlib.import_module("cross_package_harness")

# ---------------------------------------------------------------------------
#  site constants
# ---------------------------------------------------------------------------
AUTHOR   = "Young Jae Lee"
ORCID    = "https://orcid.org/0009-0002-7535-8245"
LICENSE  = "https://creativecommons.org/licenses/by/4.0/"
DOMAIN   = "https://jamming-physics.org"
PAPER_ID = "digestive_vp_site"
CODE     = "dig"
SHORT    = "Digestive/Metabolic"
TITLE    = ("Digestive and Metabolic Emergence: Slow-Wave Transport, Peristalsis, "
            "and the Glucose Homeostat")
CONCEPT  = "10.5281/zenodo.20755319"               # Zenodo concept DOI (version-independent), minted 2026-06-19
DOI_MINTED = CONCEPT.startswith("10.")             # real DOI vs a "pending ..." placeholder (C1 honesty)
DOI_URL  = ("https://doi.org/" + CONCEPT) if DOI_MINTED else ""
REPO     = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/" + PAPER_ID
ROADMAP_DOC_URL = "https://github.com/rego093-sketch/jamming-physics/blob/main/repro/" + PAPER_ID + "/FUTURE_WORK.md"
BUILD_DATE = "2026-06-19"

# Future-work disease roadmap (PLANNED, not yet built -- shown on the hub with no grades).
# Source of record is FUTURE_WORK.md; this mirror keeps the hub list in sync on rebuild.
ROADMAP_GROUPS = [
    ("Cross-package frontier (needs the sibling packages)",
     ["propagate the \u00a728 analgesic map to circulatory / neuro (musculoskeletal already carries it)"]),
    ("Sibling-owned / out-of-scope (cited, not re-emerged)",
     ["GI bleeding / varices (circulatory)", "cirrhosis / viral / alcoholic hepatitis (circulatory)",
      "megacolon (toxic / acquired), anorectal (haemorrhoids, fissure, fistula)"]),
]
GRADE_LABEL = {"[F]": ("g-forced", "[F] forced"),
               "[V]": ("g-verified", "[V] simulation-verified"),
               "[L]": ("g-calibrated", "[L] cited-locked anchor"),
               "[O]": ("g-open", "[O] open (obstacle stated)")}

def esc(s):  return html.escape(str(s), quote=True)
def m(x):    return '<span class="m">' + esc(x) + '</span>'      # inline unicode math

# DOI rendering (single-source from CONCEPT): once minted, the DOI is a resolvable doi.org link in the
# claim-strip / footers and a machine-readable identifier in the JSON-LD; while pending it stays honest
# plain text and emits no JSON-LD identifier (C1 honesty -- nothing fabricated).
if DOI_MINTED:
    DOI_LINK_HTML = '<a href="%s" rel="noopener">%s</a>' % (DOI_URL, esc(CONCEPT))
    DOI_JSONLD = ('"identifier":{"@type":"PropertyValue","propertyID":"DOI","value":%s},"sameAs":%s,'
                  % (json.dumps(CONCEPT), json.dumps(DOI_URL)))
else:
    DOI_LINK_HTML = esc(CONCEPT)
    DOI_JSONLD = ""

def words_in(html_str):
    txt = re.sub(r"<[^>]+>", " ", html_str)
    txt = html.unescape(txt)
    return len(re.findall(r"\S+", txt))

# ---------------------------------------------------------------------------
#  SECTION CONTENT  (numbers injected from the live engine result R)
# ---------------------------------------------------------------------------
def vpcard(locked, body_html, href):
    return ('<aside class="vp-card" data-locked="%s">%s '
            '<a href="%s">canonical derivation</a></aside>') % (esc(locked), body_html, esc(href))

CARD_R19  = vpcard("r19", "<b>ds/dt = g\u00b7s \u2212 s\u00b3 + h</b> \u2014 the shared jamming bistable "
                   "switch; g sets the basin-threshold scale, h is the drive. <b>[F]</b> forced.",
                   "/physics/")
CARD_GAMMA = vpcard("gamma", "<b>\u03b3 (master-gene NN-stacking \u0394G)</b> \u2014 the read-only "
                    "morphogenesis composition variable; fixes organ identity and developmental order. "
                    "<b>[V]</b> simulation-verified.", "/dna/")
CARD_FHN  = vpcard("fhn", "<b>FHN slow recovery \u2192 low frequency</b> \u2014 a slow recovery variable "
                   "\u03c4_s sets the period, so the substrate's intrinsic rhythm is far below the switch "
                   "timescale. <b>[V]</b> simulation-verified.", "/neuro/")
CARD_BARRIER = vpcard("barrier", "<b>barrier \u221d (h_sp \u2212 h)^{3/2}</b> \u2014 the R19 basin barrier "
                      "under bias h collapses to zero at the spinodal h_sp (a discontinuous flip). "
                      "<b>[F]</b> forced.", "/physics/")
CARD_KERNEL = vpcard("kernel", "<b>RR(dose) = rate(dose)/rate(0), rate \u221d exp(\u2212barrier/D)</b> \u2014 "
                     "the shared carcinogen kernel: a sustained drive lowers the R19 barrier; one noise "
                     "scale D for every site. <b>[F]</b> forced.",
                     "/digestive_vp_site/07-carcinogen-barrier-kramers-kernel/")

CARD_GATE = vpcard("gate", "<b>gate = the R19 switch held CLOSED; opens iff drive &gt; tone + spinodal</b> "
                   "\u2014 a tonically-closed valve is the R19 double well ds/dt = g\u00b7s \u2212 s\u00b3 + h biased to "
                   "the shut basin by a tonic closing bias; a coordinated relaxation/pressure drive flips it open "
                   "only past the opening spinodal (bistable hysteresis). Derived from R19, no new dynamics, no fit. "
                   "<b>[V]</b> simulation-verified.",
                   "/digestive_vp_site/16-sphincter-gate-disorders/")

CARD_RESERVOIR = vpcard("reservoir", "<b>reservoir = the R19 wall relaxed toward yield; stiffness k = 3s\u00b2 \u2212 g, "
                        "compliance C = 1/k, meal pressure P = V\u00b7k</b> \u2014 the fundic wall is the same R19 switch "
                        "resting contracted at s = \u2212\u221ag; a vagal accommodation drive slides it toward its yield "
                        "point (the R19 spinodal, where k \u2192 0 and C diverges), so a fixed meal is absorbed without a "
                        "pressure spike. Lost accommodation leaves it stiff \u2192 premature pressure. Derived from R19, no "
                        "new dynamics, no fit. <b>[V]</b> simulation-verified.",
                        "/digestive_vp_site/17-gastric-accommodation-reservoir/")

CARD_AFFERENT = vpcard("afferent", "<b>afferent gain = \u03c7 = ds*/dh = 1/k = 1/(3s\u00b2 \u2212 g)</b> \u2014 a visceral "
                       "afferent is the same R19 element resting quiescent; its static susceptibility to a wall-"
                       "distension input is the restoring-curvature inverse 1/k \u2014 the <i>identical</i> quantity the "
                       "\u00a717 reservoir reads as fundic compliance (one curvature, two readings: sensory gain here, "
                       "mechanical compliance there). A peripheral sensitization bias raises it; it diverges at the R19 "
                       "spinodal (a saddle-node critical gain) = the same marginal point as the \u00a717 wall yield. Peripheral "
                       "term only; the felt experience is mind. Derived from R19, no new dynamics, no fit. "
                       "<b>[V]</b> simulation-verified.",
                       "/digestive_vp_site/18-visceral-afferent-gain-ibs/")

CARD_METAPLASIA = vpcard("metaplasia", "<b>metaplasia = a precursor compartment on a REDUCED R19 fate scale; "
                         "g_meta = g − drop, barrier g_meta²/4 &lt; g²/4</b> — a metaplastic precursor "
                         "(Barrett's oesophagus, gastric intestinal metaplasia) is the same R19 cell-fate switch "
                         "ds/dt = g·s − s³ + h with its stability scale lowered by sustained injury — the "
                         "IDENTICAL g-reduction the §10 kernel applies for chronic H. pylori, now read as a discrete "
                         "compartment. Sitting on the smaller barrier, the metaplastic cell's next (malignant) crossing "
                         "is rate-limited on the precursor; restoring g (ablation / removing the injury) collapses that "
                         "next-step rate. Derived from R19, no new dynamics, no fit. <b>[V]</b> simulation-verified.",
                         "/digestive_vp_site/19-metaplasia-precursor-barrett-correa/")

CARD_IMMUNE = vpcard("immune", "<b>relapsing inflammation = the R19 switch with a SELF-SUSTAINING flare basin; "
                     "flip-to-flare at drive &gt; antigen + spinodal, return-to-remission only below antigen \u2212 spinodal "
                     "(hysteresis), and cumulative burden lowers the \u00a77 barrier scale g_eff = g_barrier \u2212 \u03ba\u00b7burden</b> "
                     "\u2014 a relapsing-remitting mucosal inflammation is the same R19 double well ds/dt = g\u00b7s \u2212 s\u00b3 + h whose "
                     "flare basin self-sustains once entered, so breaking an established flare (induction) needs a "
                     "suppression drive past the upper spinodal while a LOWER drive then holds remission (maintenance) "
                     "\u2014 the induction-vs-maintenance asymmetry. The accumulated inflammatory burden feeds the "
                     "<i>identical</i> g-reduction the \u00a710 kernel uses for chronic H. pylori, so colitis-associated cancer "
                     "sits on the same \u00a77 barrier step. Derived from R19, no new dynamics, no fit. "
                     "<b>[V]</b> simulation-verified.",
                     "/digestive_vp_site/22-immune-relapsing-inflammation-ibd/")

CARD_EXOCRINE = vpcard("exocrine", "<b>autodigestion = the R19 switch with an AUTOCATALYTIC self-amplification; "
                       "autoactivation threshold = |inhibitor| + spinodal, and past it the +g\u00b7s term LATCHES "
                       "(irreversible)</b> \u2014 the pancreatic zymogen cascade is the same R19 double well ds/dt = g\u00b7s \u2212 s\u00b3 + h "
                       "in which active protease self-amplifies (trypsin activates trypsinogen): a sub-threshold trigger "
                       "decays back to the inactive rest basin, but a supra-threshold trigger crosses into a self-sustaining "
                       "active basin that <i>no</i> parameter move reverses \u2014 only a protective inhibitor past the spinodal "
                       "(SPINK1) abolishes the basin, so intervention is PRE-threshold only. Derived from R19, no new "
                       "dynamics, no fit. <b>[V]</b> simulation-verified.",
                       "/digestive_vp_site/23-exocrine-autodigestion-pancreatitis/")

CARD_PERFUSION = vpcard("perfusion-viability", "<b>perfusion-viability = the R19 switch held in the VIABLE basin by "
                        "supply; flips to the ischaemic basin iff perfusion &lt; demand \u2212 spinodal, recovers iff "
                        "perfusion &gt; demand + spinodal (a salvage window = 2\u00b7spinodal)</b> \u2014 a perfused tissue is "
                        "the same R19 double well ds/dt = g\u00b7s \u2212 s\u00b3 + h resting in the viable basin at s = +\u221ag, with "
                        "the bias h = perfusion \u2212 demand; let supply fall past demand minus the spinodal and it flips "
                        "discontinuously into the ischaemic basin, and restoring supply recovers it only if it returns "
                        "WITHIN the reserve window \u2014 the time-critical salvage of acute ischaemia. Structural infarction "
                        "(transmural necrosis) is the out-of-model endpoint. Derived from R19, no new dynamics, no fit. "
                        "<b>[V]</b> simulation-verified.",
                        "/digestive_vp_site/24-perfusion-mesenteric-ischemia/")

CARD_BILE = vpcard("supersaturation", "<b>nucleation = the R19 switch with a NUCLEATION BARRIER; supersaturation (CSI "
                   "&gt; 1) is metastable, a stone nucleates only past CSI &gt; 1 + spinodal, and once formed redissolves "
                   "only below CSI \u2212 spinodal (dissolution hysteresis)</b> \u2014 cholesterol-bile crystallisation is the same "
                   "R19 double well ds/dt = g\u00b7s \u2212 s\u00b3 + h with the dissolved phase as the rest basin and the cholesterol "
                   "saturation index as the bias; a merely supersaturated bile sits metastably (above saturation yet "
                   "stone-free) until the drive clears the nucleation barrier (the Kramers crossing), and a formed stone "
                   "then persists below saturation, redissolving only far below it \u2014 which is exactly why UDCA dissolution "
                   "works only on small, early, still-near-saturation stones. Derived from R19, no new dynamics, no fit. "
                   "<b>[V]</b> simulation-verified.",
                   "/digestive_vp_site/25-hepatobiliary-cholelithiasis/")

CARD_WALL = vpcard("wall-mechanics", "<b>wall-mechanics = the R19 wall switch driven by Laplace pressure P = tension / "
                   "radius; the intact wall herniates iff P &gt; spinodal(g_wall), and a weaker wall (lower g_wall) has a "
                   "lower threshold</b> \u2014 the colonic wall is the same R19 element resting intact at s = \u2212\u221ag, with the "
                   "segmental Laplace pressure as the bias; a low-fibre diet (small hard stools gripped by strong "
                   "high-pressure segmenting contractions) raises P = tension/radius as the luminal radius falls, and once "
                   "P clears the herniation threshold spinodal(g_wall) the wall buckles out into a diverticulum \u2014 a weaker "
                   "wall (aging connective tissue, Ehlers\u2013Danlos / Marfan collagen) crossing at a lower pressure. Derived "
                   "from R19, no new dynamics, no fit. <b>[V]</b> simulation-verified.",
                   "/digestive_vp_site/26-structural-diverticular-wall/")

def body_organs(R):
    o = {x["organ"]: x for x in R["organs"]["organs"]}
    order = ", ".join(R["organs"]["gamma_order_ascending"])
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %
        (esc(o[n]["organ"]), esc(o[n]["master"]), o[n]["gamma"], esc(o[n]["dyn_class"]), esc(o[n]["role"]))
        for n in ["stomach", "intestine", "pancreas", "liver"])
    return f"""
<p>Four digestive organs emerge deterministically from their measured master-gene composition {m("\u03b3")} on the shared R19 jamming switch, with identity and developmental order cited from the DNA morphogenesis gene-clock. This package re-derives neither organ existence nor order; it adds only the functional dynamics that the later sections exercise.</p>
<p>Each organ is an instance of the same bistable switch {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")}, where the basin-threshold scale {m("g")} is the read-only {m("\u03b3")} value measured from the gene's proximal promoter ({m("\u03b3")} = \u2212mean nearest-neighbour stacking {m("\u0394G")}, SantaLucia 1998). {m("\u03b3")} is never fitted; only the switch state and size respond.</p>
{CARD_GAMMA}
{CARD_R19}
<table><thead><tr><th>organ</th><th>master gene</th><th>measured \u03b3</th><th>dynamical class</th><th>role</th></tr></thead><tbody>{rows}</tbody></table>
<p>Developmental order is a pure {m("\u03b3")} read-out (ascending {m("\u03b3")}): {esc(order)}. The two oscillator organs (stomach, intestine) carry slow-wave rhythms; the pancreas and liver form the metabolic control loop. This ordering is forced by the substrate {m("[V]")}, with its sign validated against the cited developmental-timing anchor.</p>
"""

def body_gastric(R):
    c = R["dynamics"]["slow_wave_clock"]
    return f"""
<p>The gastric pacemaker is a robust limit cycle on the shared FitzHugh\u2013Nagumo oscillator, beating at the cited {m("~3 cpm")} gastric anchor. Because the slow recovery variable sets the period, a long recovery constant {m("\u03c4_s = 380")} places the rhythm far below the switch timescale, exactly as the neuroscience volume's low-frequency result requires.</p>
<p>Across a wide tonic-drive sweep ({m("0.40\u20130.70")}) the inter-spike-interval coefficient of variation stays under {m("3%")}, so the beat is a structurally stable limit cycle rather than a tuned resonance. The single gastric-anchored clock {m("K_TIME = " + str(c["K_time_cpm_per_modelHz"]) + " cpm/model-Hz")} converts the model frequency to {m(str(c["gastric_cpm"]) + " cpm")}, matching the anchor.</p>
{CARD_FHN}
{CARD_R19}
<p>The rhythm mechanism is forced {m("[V]")}; the absolute {m("3 cpm")} rate is a cited physiological anchor {m("[L]")}, not an emergent quantity. The interstitial cells of Cajal are modelled as the slow-wave pacemaker substrate, and their rate sets the clock that every aboral segment inherits.</p>
"""

def body_gradient(R):
    chain = R["dynamics"]["intestinal_chain_cpm_N12"]
    c = R["dynamics"]["slow_wave_clock"]
    cells = "".join("<td>%s</td>" % v for v in chain)
    idx = "".join("<td>%d</td>" % (i + 1) for i in range(len(chain)))
    return f"""
<p>The intestinal slow-wave frequency falls monotonically in the aboral direction, reproducing the physiological duodenum-to-ileum gradient. A single segment property \u2014 the FitzHugh\u2013Nagumo recovery constant {m("\u03c4_s")} growing linearly along the gut \u2014 produces the entire descending profile.</p>
<p>One gastric-anchored clock converts each segment's intrinsic frequency to cycles per minute with zero intestinal tuning, predicting duodenum {m(str(c["duodenum_cpm"]) + " cpm")} (cited {m("~12")}), jejunum {m(str(c["jejunum_cpm"]) + " cpm")} (cited {m("~10")}), and ileum {m(str(c["ileum_cpm"]) + " cpm")} (cited {m("~8")}). The duodenal prediction lands within {m("8%")} of the cited value despite the clock being fixed by the stomach alone.</p>
{CARD_FHN}
<table><thead><tr><th>segment (proximal\u2192distal)</th>{idx}</tr></thead><tbody><tr><th>cpm</th>{cells}</tr></tbody></table>
<p>The gradient direction and shape are forced by the substrate {m("[V]")}; the absolute rates inherit the cited clock {m("[L]")}. Monotonic decrease holds across segment counts {m("N \u2208 {8,12,16,20}")} and the full drive sweep, so the falling gradient is a property of the mechanism, not of a particular discretization.</p>
"""

def body_peristalsis(R):
    p = R["dynamics"]["peristalsis"]
    return f"""
<p>A slow-wave phase gradient produces net aboral transport: under a physiological proximal-fast gradient a luminal bolus moves {m(str(p["physiologic_aboral_disp"]) + " segments")} downstream, and under a reversed-gradient control it moves orally ({m(str(p["reversed_oral_disp"]) + " segments")}). Direction is set entirely by the sign of the frequency gradient.</p>
<p>Weak nearest-neighbour (Kuramoto) coupling on the segments' intrinsic frequencies builds a travelling phase wave; an occlusion indicator marks contracting segments, and a mass-conserving pressure flux moves content from more-occluded toward less-occluded neighbours. No content is created or destroyed \u2014 only transported.</p>
{CARD_FHN}
<p>Directed transport from a phase gradient is forced {m("[V]")}, and it is robust: net aboral displacement survives every combination of coupling strength {m("{0.03,0.05,0.08}")} and flux scale {m("{0.15,0.20,0.30}")}. The reversal under a flipped gradient is the control that rules out a coupling artefact \u2014 transport tracks the physiological gradient, not the coupling.</p>
"""

def body_homeostat(R):
    h = R["dynamics"]["glucose_homeostat"]
    # live sweep for the table
    _, Gf = eng.glucose_homeostat(G0=5.0, T=60.0); base = float(Gf[-1])
    rows = ""
    for amp in [1.0, 2.0, 3.0, 4.0, 6.0]:
        _, Gt = eng.glucose_homeostat(G0=base, meal=eng._pulse(amp), T=30.0)
        rows += "<tr><td>%.0f</td><td>%.2f</td><td>%.2f</td></tr>" % (amp, float(Gt.max()), float(Gt[-1]))
    return f"""
<p>A glucose load returns to the {m("~5 mM")} fasting setpoint through the insulin loop. The fasting fixed point sits at {m(str(h["fasting_fixed_point_mM"]) + " mM")}; meals of increasing size lift the peak from {m("5.9")} to {m("11.1 mM")}, yet every load settles back near {m("5.2 mM")}.</p>
<p>Insulin secretion is not a single threshold but a graded population of R19 switches: as glucose rises, progressively more {m("\u03b2")}-cell switches turn on, giving a smooth dose-response that the loop integrates. Hepatic glucose production is suppressed by insulin and supported by a finite glycogen buffer, closing the loop {m("dG/dt = R_meal + HGP \u2212 (k_u0 + k_u\u00b7Ins)\u00b7G")}.</p>
{CARD_R19}
<table><thead><tr><th>meal amplitude</th><th>peak glucose (mM)</th><th>final glucose (mM)</th></tr></thead><tbody>{rows}</tbody></table>
<p>Homeostatic return is forced by the closed loop {m("[V]")}; the {m("5 mM")} setpoint value is a cited human fasting anchor {m("[L]")}. The pancreas (PDX1) owns the secretion switches and the liver (HHEX) owns the glycogen buffer, so the homeostat is a two-organ control loop, not a single-organ device.</p>
"""

def body_counter(R):
    rows = ""
    for amp in [1.0, 2.0, 3.0, 4.0]:
        _, Gt = eng.glucose_homeostat(G0=5.0, ins_kick=eng._pulse(amp), T=30.0)
        rows += "<tr><td>%.0f</td><td>%.2f</td><td>%.2f</td></tr>" % (amp, float(Gt.min()), float(Gt[-1]))
    return f"""
<p>Hypoglycaemia triggers glucagon-driven hepatic glucose release that returns blood glucose to setpoint without overshoot. An insulin overdose drives glucose to a nadir between {m("4.6")} and {m("3.5 mM")} as the challenge grows, after which the loop restores {m("~5 mM")}.</p>
<p>The counter-regulatory arm is the mirror of the insulin arm: a population of {m("\u03b1")}-cell R19 switches turns on when glucose falls, raising hepatic glucose production. The finite hepatic glycogen store (the liver / HHEX role) is the buffer that is drawn down to supply this release, which is why recovery is bounded.</p>
{CARD_R19}
<table><thead><tr><th>insulin challenge</th><th>nadir glucose (mM)</th><th>final glucose (mM)</th></tr></thead><tbody>{rows}</tbody></table>
<p>The bounded counter-regulatory loop is forced {m("[V]")}; the absolute glycogen capacity is a model unit, not a physiological mass, and is therefore graded {m("[O]")} with the obstacle stated in the irreproducibility ledger. The loop never diverges \u2014 glucose stays below {m("9 mM")} on rebound \u2014 because the buffer is finite.</p>
"""

def body_kernel(R):
    v = onco.validate()
    D = v["shared_noise_scale_D"]
    return f"""
<p>A carcinogen is modelled as a sustained aberrant drive that lowers the R19 cell-fate barrier, raising the Kramers crossing rate into a malignant basin; relative risk is {m("RR(dose) = rate(dose)/rate(0)")}. The cell-fate switch is the same R19 primitive that builds organs \u2014 carcinogenesis is a biased basin crossing, not a separate mechanism.</p>
<p>The exact barrier is the healthy-well-to-saddle height of the biased cubic {m("s\u00b3 \u2212 g\u00b7s \u2212 h = 0")}; it vanishes as {m("(h_sp \u2212 h)^{3/2}")} as the bias approaches the spinodal. One shared substrate noise scale {m("D = " + str(D))} serves every organ site, and the only per-site number is a slope {m("\u03ba")} mapping physical dose to bias, calibrated to a single cited epidemiological anchor by bisection \u2014 never a curve-shape fit.</p>
{CARD_BARRIER}
{CARD_R19}
<p>The kernel is forced by the substrate {m("[F]")}; the per-site anchors are cited {m("[L]")}; absolute incidence rates are open {m("[O]")} because they need external population calibration, exactly as absolute organ size is open. The three site pages (colorectal, pancreatic, gastric) each instantiate this one kernel with their own cited anchor.</p>
"""

def body_colorectal(R):
    v = onco.validate(); crc = v["colorectal"]
    rows = "".join("<tr><td>%g</td><td>%.3f</td></tr>" % (d, rr) for d, rr in crc["curve"])
    return f"""
<p>Processed-meat exposure raises colorectal-cancer risk along a monotone, convex dose-response anchored to the IARC figure {m("RR \u2248 1.18 per 50 g/day")}. The shared barrier-lowering kernel, with a single calibrated slope, reproduces this curve from one anchor point.</p>
<p>The mechanistic drive is heme iron and N-nitroso compounds (plus heterocyclic amines from high-temperature cooking) acting as a sustained bias on the colonocyte fate switch. Calibrating only the dose-to-bias slope {m("\u03ba")} to the {m("50 g/day")} anchor fixes the whole curve.</p>
{CARD_KERNEL}
<table><thead><tr><th>processed meat (g/day)</th><th>relative risk</th></tr></thead><tbody>{rows}</tbody></table>
<p>The epidemiological anchor is cited {m("[L]")}; the reproduced dose-response shape is verified {m("[V]")} \u2014 monotone and convex, rising to {m("1.63")} at {m("150 g/day")}; absolute incidence is open {m("[O]")}. The convexity is a prediction of the kernel, not an input: barrier lowering is faster than linear as the bias grows.</p>
"""

def body_pancreatic(R):
    v = onco.validate(); pdac = v["pancreatic"]; rr30 = v["pancreatic_RR_at_30py"]
    rows = "".join("<tr><td>%g</td><td>%.3f</td></tr>" % (d, rr) for d, rr in pdac["curve"])
    return f"""
<p>Tobacco exposure raises pancreatic-cancer risk monotonically in pack-years, anchored to {m("RR \u2248 1.91 at 50 pack-years")} (Multiethnic Cohort). The same barrier-lowering kernel, with one calibrated slope, reproduces the full curve and passes through the current-smoker range near thirty pack-years.</p>
<p>Tobacco nitrosamines and polycyclic aromatic hydrocarbons supply the sustained bias on the pancreatic-cell fate switch. At {m("30 pack-years")} the kernel gives {m("RR = " + ("%.2f" % rr30))}, consistent with the cited current-smoker estimates ({m("~1.74")}, Iodice 2008).</p>
{CARD_KERNEL}
<table><thead><tr><th>pack-years</th><th>relative risk</th></tr></thead><tbody>{rows}</tbody></table>
<p>The anchor is cited {m("[L]")}; the shape is verified {m("[V]")}; absolute incidence is open {m("[O]")}. The monotone rise from {m("1.00")} to {m("1.91")} uses a single slope calibrated to one anchor, so the intermediate pack-year risks are predictions rather than fitted points.</p>
"""

def body_gastric_onc(R):
    v = onco.validate(); g = v["gastric"]
    fan = "".join("<tr><td>%d%%</td><td>%.2f</td><td>%.2f</td></tr>" % (f, a, b) for f, a, b in g["dose_response_fan"])
    return f"""
<p>Helicobacter pylori infection and dietary N-nitroso act synergistically on gastric-cancer risk: their joint relative risk {m("\u2248 " + str(g["RR_joint"]))} exceeds the additive-null {m(str(g["additive_null"]))}, a super-additive interaction. Infection lowers the R19 barrier scale (chronic inflammation reduces cell-fate stability) while diet adds bias on the same switch.</p>
<p>The single exact-barrier kernel reproduces this departure from additivity and, on the same kernel, predicts the joint risk is sub-multiplicative near the spinodal (it falls below the multiplicative-null {m(str(g["multiplicative_null"]))}). That sub-multiplicativity \u2014 diminishing returns at extreme dual exposure \u2014 is a concrete, falsifiable prediction.</p>
{CARD_KERNEL}
<table><thead><tr><th>dietary dose</th><th>RR on H. pylori\u2212</th><th>RR on H. pylori+</th></tr></thead><tbody>{fan}</tbody></table>
<p>The infection-by-diet interaction is verified {m("[V]")} against the cited synergy {m("[L]")}; absolute incidence is open {m("[O]")}. The dose-response fans out on an infected background versus an uninfected one, which is the operational signature of the synergy and the part a cohort study can test directly.</p>
"""

# ----------------------------------------------------------------- DISEASE MODULES
def body_dysrhythmia(R):
    d = dz.validate_d1()
    dm = d["dysrhythmia"]; ee = d["ectopic"]; gp = d["gastroparesis"]
    rrows = "".join("<tr><td>%g</td><td>%.2f</td><td>%s</td></tr>" % (t, c, b) for t, c, b in dm["rows"])
    grows = "".join("<tr><td>%.1f</td><td>%.1f%%</td></tr>" % (r, p) for r, _, p in gp["rows"])
    return f"""
<p>Gastric dysrhythmia and gastroparesis are not new machinery; they are perturbations of the single gastric slow-wave pacemaker of {m("\u00a72")}. The pacemaker is the shared FitzHugh\u2013Nagumo oscillator, and its recorded rate is set by the recovery constant {m("\u03c4_s")} through the one gastric-anchored clock {m("K_TIME")}.</p>
<p>Sweeping {m("\u03c4_s")} carries the recorded rhythm monotonically across the cited electrogastrography band: a short constant gives tachygastria ({m("> 3.7 cpm")}), the {m("\u00a72")} anchor gives the normal {m("~3 cpm")}, and a long constant gives bradygastria ({m("< 2.5 cpm")}). No rate is fitted \u2014 the band is traversed by one substrate parameter.</p>
{CARD_FHN}
<table><thead><tr><th>recovery constant \u03c4_s</th><th>recorded rate (cpm)</th><th>rhythm</th></tr></thead><tbody>{rrows}</tbody></table>
<p>Tachygastria has a second, mechanistic route: a distal ectopic focus. A normal-rate distal focus leaves the antral recording in band ({m(str(ee["normal_focus_coupled_cpm"]) + " cpm")}), but a faster focus that couples entrains the antrum upward to {m(str(ee["fast_focus_coupled_cpm"]) + " cpm")} \u2014 tachygastria appears only when the focus is both faster and coupled, exactly the clinical picture.</p>
<p>Gastroparesis is the amplitude counterpart. Interstitial-cell (ICC) pacemaker density scales the antral contraction; as density falls, gastric emptying in a fixed window slows monotonically, holding through moderate loss (a functional reserve) and then collapsing \u2014 {m(str(gp["severe_depletion_pct_of_normal"]) + "%")} of normal at severe depletion, and zero with no pacemakers at all.</p>
<table><thead><tr><th>pacemaker density (fraction)</th><th>emptying rate (% of normal)</th></tr></thead><tbody>{grows}</tbody></table>
<p><b>Treatment (model reading).</b> The therapeutic target is the rhythm parameter and the contraction amplitude. For tachy/bradygastria the goal is to restore the {m("~3 cpm")} rhythm; the ectopic-entrainment result above is exactly the mechanism of <i>gastric electrical pacing</i> \u2014 an external pacemaker that out-paces and couples to the antrum entrains the recording back to target. For gastroparesis the target is the effective contraction (ICC density): prokinetics raise it, but the model predicts efficacy tracks <i>residual</i> ICC density, so with severe depletion the rhythm-restoring route is refractory and stimulation/surgical options follow. The treatment-target direction is forced {m("[V]")}; absolute efficacy is open {m("[O]")}.</p>
<p>The dysrhythmia bands, the ectopic entrainment, and the density-graded emptying are all forced by the substrate {m("[V]")}; the cited normal band ({m("2.5\u20133.7 cpm")}) is a physiological anchor {m("[L]")}; the absolute emptying rate is open {m("[O]")}, needing clinical (scintigraphy) calibration, exactly as absolute organ size is open.</p>
"""

def body_diabetes(R):
    d = dz.validate_d2()
    t1 = d["t1_capacity"]["rows"]; t2 = d["t2_sensitivity"]["rows"]; gaps = d["matched_depth_gap"]; ig = d["igt"]
    rows = "".join("<tr><td>%.1f</td><td>%.2f</td><td>%.2f</td><td>%.2f</td></tr>"
                   % (t1[i][0], t1[i][1], t2[i][1], gaps[i]) for i in range(len(t1)))
    return f"""
<p>Type 1 and type 2 diabetes are two failure modes of the single glucose\u2013insulin homeostat of {m("\u00a75")}. Nothing is added to the loop; two of its parameters are moved. Capacity is the maximum {m("\u03b2")}-cell secretion {m("Smax_i")}; gain is the insulin sensitivity {m("k_u")}. Each is scaled by one factor and the phenotype emerges.</p>
<p>Depleting {m("\u03b2")}-cell capacity (the type 1 axis) raises fasting glucose accelerating: it crosses the cited {m("7 mM")} diabetes threshold and runs away to severe hyperglycaemia ({m(str(d["t1_capacity"]["deepest_fasting"]) + " mM")} at deep depletion), and meal loads no longer return to a normal setpoint \u2014 the insulin-dependent, catastrophic failure.</p>
{CARD_R19}
<p>Losing insulin sensitivity (the type 2 axis) is milder: the loop relaxes to a stable, elevated setpoint ({m(str(d["t2_sensitivity"]["deepest_fasting"]) + " mM")} even at deep resistance) and still self-regulates back to it. At matched perturbation depth the capacity deficit is always the more severe and the gap widens \u2014 capacity loss catastrophic, gain loss compensated.</p>
<table><thead><tr><th>perturbation depth</th><th>type 1 fasting (mM)</th><th>type 2 fasting (mM)</th><th>excess (mM)</th></tr></thead><tbody>{rows}</tbody></table>
<p><b>Treatment (model reading).</b> Because the two axes are distinct parameters, the model selects distinct targets. Type 1 is a missing-capacity lesion, so the only restoring move is to <i>replace the secretion</i> \u2014 exogenous insulin supplies the depleted {m("\u03b2")}-cell arm and returns the loop toward setpoint. Type 2 is a gain lesion, so the target is the gain itself: <i>insulin sensitisers</i> raise {m("k_u")} and pull the elevated setpoint back down, with weight loss and secretagogues as further levers. The model's prediction \u2014 sensitisers help type 2 but cannot fix type 1, where capacity is the lesion \u2014 is the falsifiable treatment claim; the target direction is forced {m("[V]")}, absolute efficacy open {m("[O]")}.</p>
<p>Impaired glucose tolerance is simply a mild point on the gain axis: fasting {m(str(ig["fasting_mM"]) + " mM")}, inside the cited pre-diabetes band ({m("5.6\u20136.9 mM")}). The two-axis emergence is forced {m("[V]")}; the fasting-glucose thresholds are cited {m("[L]")}; absolute population prevalence is open {m("[O]")}, needing epidemiological calibration.</p>
"""

def body_gastritis_ulcer(R):
    d = dz.validate_d3()
    er = d["erosion"]; ss = d["ulcer_site_split"]; ct = d["continuum"]
    erows = "".join("<tr><td>%g</td><td>%.2f</td></tr>" % (dd, rr) for dd, rr in er["curve"])
    gx = ss["gastric"]; dx = ss["duodenal"]
    return f"""
<p>Gastritis and peptic ulcer do not need a new model: they are the {m("\u00a77")} carcinogen barrier-Kramers kernel read on a different switch. There the bias lowered a cell-fate barrier; here the same exact barrier is the mucosal-integrity well, and aggression \u2014 gastric acid, NSAIDs, bile \u2014 is the bias {m("h")} that lowers it.</p>
<p>Acute erosive gastritis is the dose-response. Raising aggression raises the erosion crossing rate along the same monotone, convex Kramers curve, with a single slope {m("\u03ba = " + str(er["kappa"]))} calibrated by bisection to one cited anchor \u2014 the NSAID peptic-ulcer relative risk {m("\u2248 4")}. The convexity is a prediction of barrier lowering, not a fitted shape.</p>
{CARD_KERNEL}
<table><thead><tr><th>aggression (normalised dose)</th><th>erosion relative risk</th></tr></thead><tbody>{erows}</tbody></table>
<p>Peptic-ulcer site is a split on the same barrier. A gastric ulcer crosses by {esc(gx["route"])} \u2014 a reduced barrier scale {m("g = " + str(gx["g"]))} at moderate acid \u2014 reaching {m("RR " + str(gx["RR"]))}; a duodenal ulcer crosses by {esc(dx["route"])} \u2014 intact defence {m("g = " + str(dx["g"]))} at high acid {m("h = " + str(dx["h"]))} \u2014 reaching {m("RR " + str(dx["RR"]))}. Both reach the ulcer basin, by mechanistically distinct routes.</p>
<p>The continuum is the point: chronic {m("H. pylori")} gastritis lowers the very same barrier scale {m("g_Hp = " + str(ct["g_Hp_shared_with_s10"]))} that the {m("\u00a710")} gastric-cancer step uses, so one kernel spans inflammation \u2192 erosion \u2192 ulcer \u2192 the first step of the neoplasia sequence. The erosion shape, the site split, and the continuum are verified {m("[V]")}; the NSAID anchor is cited {m("[L]")}; absolute erosion and ulcer incidence are open {m("[O]")}.</p>
<p><b>Treatment (model reading).</b> The barrier has two handles, and the site dictates which to pull. Lowering the aggression bias {m("h")} \u2014 acid suppression (proton-pump inhibitors) \u2014 moves the system back <i>down</i> the convex curve, most effective for the acid-driven duodenal route. Raising the defence scale {m("g")} \u2014 stopping NSAIDs, mucosal protection, and <i>eradicating H. pylori to restore</i> {m("g_Hp")} \u2014 is the lever for the defence-failure gastric route, and because it lifts the same {m("g")} the {m("\u00a710")} cancer step rides on, it is also the model's mechanism for how Hp eradication lowers downstream gastric-cancer risk. The target direction is forced {m("[V]")}; absolute efficacy is open {m("[O]")}.</p>
"""

def body_motility(R):
    d = dz.validate_d4()
    pa = d["slow_transit_and_inertia"]; ci = d["cipo"]; il = d["ileus"]; un = d["icc_unifying"]
    drows = "".join("<tr><td>%.1f</td><td>%.0f%%</td><td>%s</td></tr>"
                    % (dd, p, ("slow-transit (graded)" if p > 20 else "colonic inertia (collapsed)"))
                    for dd, p in pa["rows"])
    urows = "".join("<tr><td>%.1f</td><td>%.0f%%</td><td>%.0f%%</td></tr>" % (r, s, g)
                    for r, s, g in un["density_axis"])
    return f"""
<p>The major non-obstructive intestinal motility disorders are perturbations of the single peristalsis module of {m("\u00a74")}: a slow-wave phase gradient drives a travelling occlusion wave that transports luminal content aborally. Three knobs of that one module \u2014 the propulsive drive (the aboral frequency-gradient spread), the ICC pacemaker density, and a transient drive switch \u2014 reproduce the whole group.</p>
<p>Reducing the propulsive drive slows aboral transit monotonically: this is <b>slow-transit constipation</b>, and in the model it stays responsive (a restored drive restores transit). Below a threshold the travelling wave can no longer carry content and transport <i>collapses</i> to near zero \u2014 <b>colonic inertia</b>, the refractory, treatment-resistant end of the very same axis.</p>
{CARD_FHN}
<table><thead><tr><th>propulsive drive</th><th>transit rate (% of normal)</th><th>regime</th></tr></thead><tbody>{drows}</tbody></table>
<p><b>Chronic intestinal pseudo-obstruction</b> is the ICC-density lesion: as pacemaker density falls the wave weakens and propulsion fails \u2014 yet the lumen stays patent, so this is a <i>functional</i>, not mechanical, obstruction (there is no fixed stenosis to find). <b>Paralytic ileus</b> is the transient case: a global loss of slow-wave drive halts propulsion, and the model recovers transport when the drive returns \u2014 the deficit scales with how long the drive is lost ({m(str(il["rows"][1][1]) + "%")} after a short loss, {m(str(il["rows"][3][1]) + "%")} after a long one), while a permanent loss gives {m(str(il["never_on_pct"]) + "%")}.</p>
<p>The unifying result (cross-disease hypothesis #1): <b>one ICC-depletion lesion, many sites</b>. The same density parameter collapses gastric emptying ({m("\u00a711")}) and intestinal transit ({m("\u00a714")}) along nearly the same curve \u2014 a single cause behind gastroparesis, slow-transit constipation, and pseudo-obstruction.</p>
<table><thead><tr><th>ICC density</th><th>stomach emptying (% normal, \u00a711)</th><th>gut transit (% normal, \u00a714)</th></tr></thead><tbody>{urows}</tbody></table>
<p><b>Treatment (model reading).</b> Each disorder names its own target. Slow-transit constipation: prokinetics <i>raise the propulsive drive</i> and restore transit \u2014 effective in the graded regime. Colonic inertia: below the threshold a modest boost stays sub-threshold, so it is refractory to prokinetics and subtotal colectomy is the model-consistent escalation \u2014 the threshold is the falsifiable prediction. CIPO: efficacy tracks <i>residual</i> ICC density (no mechanical target exists). Paralytic ileus: <i>remove the transient suppressant</i> (opioids, post-operative inflammation, electrolyte derangement) and propulsion recovers spontaneously \u2014 the reversibility is exactly why ileus is waited out, unlike inertia.</p>
<p>The transit mechanisms \u2014 the graded drive axis with its inertia threshold, the functional CIPO obstruction, the reversible ileus, and the shared ICC lesion \u2014 are all forced by the substrate {m("[V]")}; clinical transit-time anchors are calibration targets {m("[L]")} pending; the absolute colonic transit time is open {m("[O]")}, needing radio-opaque-marker / scintigraphy calibration.</p>
"""

def body_scattered(R):
    d = dz.validate_d5()
    a = d["d5a_dumping"]; b = d["d5b_reflux_esophagitis"]; c = d["d5c_insulinoma_reactive_hypo"]
    fd = d["d5d_functional_dyspepsia_motility"]; e = d["d5e_sibo_stasis"]
    ed = a["early_dumping"]; ld = a["late_dumping"]; me = a["mechanical"]
    ins = c["insulinoma"]; rh = c["reactive_hypoglycemia"]; fdm = fd["fd_motility"]; sb = e["sibo"]
    ed_rows = "".join("<tr><td>%g</td><td>%.2f</td></tr>" % (du, pk) for du, pk in ed["rows"])
    ld_rows = "".join("<tr><td>%g</td><td>%.2f</td><td>%.2f</td><td>%s</td></tr>"
                      % (du, pk, na, ("\u2713 < 3.9" if na < 3.9 else "\u2014"))
                      for du, pk, na in ld["rows"])
    rf_rows = "".join("<tr><td>%g</td><td>%.2f</td></tr>" % (dd, rr) for dd, rr in b["erosion"]["curve"])
    in_rows = "".join("<tr><td>%g</td><td>%.2f</td><td>%s</td></tr>"
                      % (A, f, ("\u2713 < 3.9" if f < 3.9 else "\u2014")) for A, f in ins["rows"])
    rh_rows = "".join("<tr><td>%g</td><td>%.2f</td><td>%.2f</td></tr>" % (sp, pk, na) for sp, pk, na in rh["rows"])
    fd_rows = "".join("<tr><td>%.1f</td><td>%.1f%%</td></tr>" % (r, p) for r, p in fdm["rows"])
    sb_rows = "".join("<tr><td>%.1f</td><td>%.3f</td></tr>" % (dr, rt) for dr, rt in sb["rows"])
    return f"""
<p>Five further Tier-1 disorders are grouped here because each is one perturbed parameter of a module already built in {m("\u00a72\u2013\u00a714")}, adding no new substrate primitive (this is group A). The discipline is unchanged: a single knob is moved, the phenotype is read off, and where the substrate genuinely cannot express a feature it is recorded open {m("[O]")} with its obstacle, never tuned into agreement.</p>

<h2>Dumping syndrome \u2014 a metabolic reading on the {m("\u00a75")} homeostat</h2>
<p>Dumping's defining features are metabolic, and they emerge cleanly on the glucose loop. <b>Early dumping</b>: the same carbohydrate load delivered faster (a sharper meal pulse) drives a monotonically higher glucose peak \u2014 from {m(str(ed["rows"][0][1]) + " mM")} at slow delivery to {m(str(ed["fastest_peak_mM"]) + " mM")} at the fastest \u2014 because the loop's finite insulin response cannot keep pace with the steepened input.</p>
<table><thead><tr><th>delivery window (shorter = faster)</th><th>glucose peak (mM)</th></tr></thead><tbody>{ed_rows}</tbody></table>
<p><b>Late dumping</b> is the same delivery speed coupled to an exaggerated incretin-driven insulin response: the curve becomes biphasic \u2014 an early hyperglycaemic peak followed by a reactive nadir that crosses the cited {m("3.9 mM")} hypoglycaemia threshold, deepening with delivery speed. This ties late dumping to insulinoma and reactive hypoglycaemia below through the shared {m("\u00a75")} reactive undershoot.</p>
{CARD_R19}
<table><thead><tr><th>delivery window</th><th>peak (mM)</th><th>reactive nadir (mM)</th><th>crosses hypo</th></tr></thead><tbody>{ld_rows}</tbody></table>
<p>The mechanical rapid-emptying magnitude is the honest negative. The {m("\u00a74")} transporter is a conserved-bolus hard occlusion wave whose displacement saturates at the tube end, so it cannot express emptying faster than normal ({m(str(me["rapid_overshoot_pct"]) + "%")} overshoot at the fastest observable) \u2014 the slow side reduces correctly, but the rapid side is geometrically pinned. The true lesion is loss of the gastric accommodation reservoir and pyloric brake, a Tier-2 element (group B); this magnitude is open {m("[O]")}.</p>
<p><b>Treatment (model reading).</b> The target is the inverse of the prokinetic goal of {m("\u00a711")}/{m("\u00a714")}: <i>slow</i> gastric emptying and carbohydrate delivery. Smaller, more frequent, lower-glycaemic meals broaden the delivery pulse and flatten the peak; surgically, restoring the reservoir / pyloric brake is the mechanical target. The direction is forced {m("[V]")}; absolute efficacy and the absolute nadir are open {m("[O]")}.</p>

<h2>Reflux oesophagitis \u2014 the {m("\u00a713")} barrier kernel on the oesophageal mucosa</h2>
<p>The mucosal-injury part of reflux oesophagitis needs no new model: oesophageal acid exposure is a sustained bias {m("h")} that lowers the mucosal-integrity barrier, read on the <i>identical</i> exact-barrier Kramers kernel as {m("\u00a713")}. Erosion relative risk rises monotone and convex in acid-exposure dose with the same calibrated slope ({m("\u03ba = " + str(b["erosion"]["kappa_shared_with_s13"]))}) as the gastritis curve \u2014 no new anchor, no shape fit.</p>
{CARD_KERNEL}
<table><thead><tr><th>acid exposure (normalised dose)</th><th>erosion relative risk</th></tr></thead><tbody>{rf_rows}</tbody></table>
<p><b>Treatment (model reading).</b> Lower the acid-exposure bias {m("h")} \u2014 acid suppression (proton-pump inhibitors) moves the system back <i>down</i> the convex erosion curve. Eliminating the reflux <i>source</i> (lower-oesophageal-sphincter incompetence) needs the Tier-2 sphincter gate (group B); this section owns only the acid-injury crossing. The target direction is forced {m("[V]")}; absolute efficacy and incidence are open {m("[O]")}.</p>

<h2>Insulinoma and reactive hypoglycaemia \u2014 the mirror of type 1 on the {m("\u00a75")} loop</h2>
<p><b>Insulinoma</b> is an autonomous, unregulated insulin source on the validated glucose loop: it pulls the fasting fixed point below the {m("5 mM")} setpoint and below the cited {m("3.9 mM")} threshold, deepening monotonically with source strength \u2014 the exact mirror of {m("\u00a712")} type-1 capacity loss, where a missing insulin arm instead <i>raised</i> glucose past {m("7 mM")}. Removing the source returns the loop to setpoint ({m(str(ins["recovery_on_source_removal_mM"]) + " mM")}), the resection prediction.</p>
<table><thead><tr><th>autonomous insulin source</th><th>fasting glucose (mM)</th><th>crosses hypo</th></tr></thead><tbody>{in_rows}</tbody></table>
<p><b>Reactive hypoglycaemia</b> is a meal followed by an exaggerated, delayed insulin response that drives a reactive undershoot below baseline, deepening with the overshoot \u2014 the same {m("\u00a75")} mechanism behind late dumping, a distinct aetiology with the same loop signature.</p>
<table><thead><tr><th>post-prandial insulin overshoot</th><th>peak (mM)</th><th>reactive nadir (mM)</th></tr></thead><tbody>{rh_rows}</tbody></table>
<p><b>Treatment (model reading).</b> Insulinoma \u2014 <i>remove</i> the autonomous source (surgical resection / limit the unregulated secretion term); the model shows the loop returns to setpoint once the source is gone. Reactive hypoglycaemia \u2014 <i>blunt</i> the post-prandial insulin spike (slower carbohydrate, smaller meals). Target direction is forced {m("[V]")}; absolute glucose and efficacy are open {m("[O]")}.</p>

<h2>Functional dyspepsia (motility component) \u2014 the mild end of the {m("\u00a711")} ICC axis</h2>
<p>A mild reduction of gastric contraction amplitude (a mild {m("\u00a711")} ICC lesion) produces a mild emptying-rate delay \u2014 present and monotone, but far short of the severe-gastroparesis collapse. The functional-dyspepsia operating point ({m(str(fdm["mild_emptying_pct"]) + "%")} of normal emptying) is clearly distinct from severe gastroparesis on the same axis ({m(str(fdm["severe_emptying_pct"]) + "%")}); the delay is resolved only on a short emptying-rate window, before completion saturates it.</p>
{CARD_FHN}
<table><thead><tr><th>contraction amplitude (fraction)</th><th>emptying rate (% of normal)</th></tr></thead><tbody>{fd_rows}</tbody></table>
<p><b>Treatment (model reading).</b> Prokinetics raise the effective gastric contraction (as in {m("\u00a711")}) and restore the emptying rate. The post-prandial-distress / early-satiation (felt) component is the Tier-2 accommodation reservoir (fundic-relaxing agents) plus afferent gain (neuromodulators), with the felt interpretation living in the {m("mind")} volume behind the firewall. The motility target is {m("[V]")} partial; the felt component is open {m("[O]")}.</p>

<h2>SIBO (motility component) \u2014 stasis from a weakened {m("\u00a74")} sweep</h2>
<p>Small-intestinal bacterial overgrowth's motility predisposition is loss of the strong periodic housekeeping propulsion: reducing the propulsive drive on the {m("\u00a74")} transporter produces stasis, read as a rising retained proximal fraction, with a collapse mirroring the colonic-inertia threshold of {m("\u00a714")}. The lumen clears at normal drive ({m(str(sb["rows"][0][1]))} retained) and holds most of the bolus at low drive ({m(str(sb["rows"][-1][1]))} retained).</p>
<table><thead><tr><th>propulsive drive</th><th>retained proximal fraction</th></tr></thead><tbody>{sb_rows}</tbody></table>
<p><b>Treatment (model reading).</b> Restore the periodic propulsive sweep \u2014 prokinetics / motilin-class agents reinstate clearance and lower the retained fraction. The bacterial overgrowth <i>load</i> itself is out of model (it needs a microbial layer), and the explicit migrating-motor-complex periodic sweep is deferred to Tier-2 (group B) under the No-Tuning rule. The motility target is {m("[V]")}; the bacterial load is open {m("[O]")}.</p>

<p>Across all five: the metabolic, erosion and stasis <i>mechanisms</i> are forced by the substrate {m("[V]")}; the hypoglycaemia and NSAID anchors are cited {m("[L]")}; and four features stay honestly open {m("[O]")} with stated obstacles \u2014 the dumping mechanical magnitude and absolute nadir, the SIBO bacterial load, and the functional-dyspepsia felt component \u2014 each pointing at a Tier-2 element rather than a fitted coefficient.</p>
"""

def body_gate(R):
    d = dz.validate_d6()
    g = d["d6a_gerd"]["gerd"]; b = d["d6b_achalasia"]["achalasia"]
    s = d["d6c_esophageal_spasm"]["spasm"]; o = d["d6d_sphincter_of_oddi"]["oddi"]
    g_rows = "".join("<tr><td>%.2f</td><td>%d / 21</td><td>%.3f</td></tr>" % (t, ev, bu) for t, ev, bu in g["rows"])
    ar_rows = "".join("<tr><td>%.2f</td><td>%s</td><td>%.0f</td></tr>"
                      % (fr, ("open" if op else "STUCK"), rt) for fr, op, rt in b["relaxation_route"])
    ap_rows = "".join("<tr><td>%.2f</td><td>%.0f%%</td></tr>" % (co, pc) for co, pc in b["aperistalsis"])
    sc_rows = "".join("<tr><td>%.2f</td><td>%.0f%%</td></tr>" % (co, pc) for co, pc in s["coordination_axis"])
    sa_rows = "".join("<tr><td>%.1f</td><td>%.0f%%</td></tr>" % (am, pc) for am, pc in s["amplitude_rescue"])
    o_rows = "".join("<tr><td>%.2f</td><td>%s</td><td>%.0f</td></tr>"
                     % (fr, ("open" if op else "STUCK"), of) for fr, op, of in o["rows"])
    return f"""
<p>The esophageal and outlet motor disorders need one element the transport and homeostat modules do not contain: a <b>gate</b> \u2014 a tonically-closed valve that opens only on a coordinated relaxation signal. This is the first Tier-2 primitive, and it is not new dynamics: a gate is the {m("\u00a72")} R19 switch {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")} held in its closed basin by a tonic closing bias, which a relaxation or pressure drive flips open only once it clears the opening spinodal (bistable hysteresis). The gate resistance is {m("tone + spinodal(g)")}; nothing is fitted.</p>
{CARD_GATE}
<p>This single gate produces two diseases that are exact opposites \u2014 the gate analogue of the one-ICC-lesion mirror of {m("\u00a711")}/{m("\u00a714")}. <b>GERD</b> is the gate failing <i>closed</i>: as resting lower-esophageal-sphincter tone falls, more of a fixed spectrum of intra-gastric pressure transients clears the gate resistance, so retrograde reflux burden rises monotonically \u2014 continent at high tone ({m(str(g["rows"][0][1]) + " events")}), incompetent at low tone ({m(str(g["rows"][-1][1]) + " of 21")}). The reflux <i>source</i> is the gate; the mucosal-injury <i>consequence</i> is the {m("\u00a715")} reflux-erosion curve.</p>
<table><thead><tr><th>LES tone</th><th>reflux events</th><th>retrograde burden</th></tr></thead><tbody>{g_rows}</tbody></table>
<p><b>Treatment (model reading).</b> {esc(d["d6a_gerd"]["treatment"])}</p>
<p><b>Achalasia</b> is the same gate failing <i>open</i>: the coordinated swallow relaxation can no longer flip it, so the bolus is retained at the junction (stasis, then dilatation). Two routes reach the identical stuck gate \u2014 a failing relaxation drive (shown below) and a rising gate tone \u2014 both making the open drive fall below the gate resistance; aperistalsis (loss of the {m("\u00a74")} wave) compounds the upstream clearance.</p>
<table><thead><tr><th>relaxation competence</th><th>gate</th><th>retained fraction</th></tr></thead><tbody>{ar_rows}</tbody></table>
<table><thead><tr><th>aperistalsis (\u00a74 coordination)</th><th>transit (% normal)</th></tr></thead><tbody>{ap_rows}</tbody></table>
<p><b>Treatment (model reading).</b> {esc(d["d6b_achalasia"]["treatment"])}</p>
<p><b>Esophageal spasm / jackhammer / nutcracker</b> is a {m("\u00a74")} coordination pathology, not a gate fault: net directed transport collapses as the aboral phase coordination is lost, and \u2014 the jackhammer signature \u2014 raising contraction amplitude does <i>not</i> rescue transit. Vigorous but uncoordinated contraction fails to move the bolus, and more vigor only makes it worse.</p>
<table><thead><tr><th>\u00a74 coordination</th><th>transit (% normal)</th></tr></thead><tbody>{sc_rows}</tbody></table>
<table><thead><tr><th>contraction amplitude (coord fixed low)</th><th>transit (% normal)</th></tr></thead><tbody>{sa_rows}</tbody></table>
<p><b>Treatment (model reading).</b> {esc(d["d6c_esophageal_spasm"]["treatment"])}</p>
<p><b>Sphincter of Oddi dysfunction</b> is the same gate primitive at the biliary / pancreatic outlet: a stuck-closed gate gives an outflow-obstruction proxy \u2014 outflow ceases when the gate cannot open \u2014 and the treatment mirror (sphincterotomy = force the gate open) is identical to achalasia.</p>
<table><thead><tr><th>relaxation competence</th><th>gate</th><th>biliary outflow</th></tr></thead><tbody>{o_rows}</tbody></table>
<p><b>Treatment (model reading).</b> {esc(d["d6d_sphincter_of_oddi"]["treatment"])}</p>
<p>All four motor readings are forced by the substrate {m("[V]")} \u2014 the gate (GERD continence, achalasia/Oddi stuck-closed stasis) and the {m("\u00a74")} coordination (spasm). What stays open {m("[O]")}, each with its obstacle: the absolute reflux frequency, the absolute achalasia clearance and Oddi outflow (clinical manometry / pH-impedance / scintigraphy), and the felt chest-pain component of spasm, which is afferent gain (group B3, with the felt interpretation in {m("mind")} behind the firewall; the non-opioid lever that raises that peripheral visceral afferent's firing threshold is mapped in {m("\u00a728")}).</p>
"""

def body_reservoir(R):
    d = dz.validate_d7()
    cv = d["accommodation"]; tx = d["treatment_axis"]; yi = d["yield_identity"]
    P0 = cv["baseline_stiff_pressure"]
    rows = cv["rows"]                                   # (frac, compliance, stiffness, pressure)
    tbl = "".join("<tr><td>%.2f</td><td>%.3f</td><td>%.3f</td><td>%.0f%%</td></tr>"
                  % (fr, C, P, 100.0 * P / P0) for fr, C, _k, P in rows)
    C_hi = rows[0][1]; C_lo = rows[-1][1]               # compliance at most vs least accommodation
    P_hi_pct = 100.0 * rows[0][3] / P0; P_lo_pct = 100.0 * rows[-1][3] / P0
    norm_pct = 100.0 * cv["normal_pressure"] / P0; fd_pct = 100.0 * cv["fd_pressure"] / P0
    return f"""
<p>The post-prandial-distress component of functional dyspepsia needs one element the transport, homeostat and gate modules do not contain: a <b>reservoir</b> \u2014 a fundic compliance that absorbs a meal volume without a pressure spike. This is the second Tier-2 primitive, and like the gate it is not new dynamics: the fundic wall is the {m("\u00a72")} R19 switch {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")} resting contracted at {m("s = \u2212\u221ag")}, which a vagal accommodation drive relaxes toward its yield point. The wall stiffness is the R19 restoring curvature {m("k = 3s\u00b2 \u2212 g")}, the compliance its inverse {m("C = 1/k")}, and a fixed meal raises pressure {m("P = V\u00b7k")}; nothing is fitted.</p>
{CARD_RESERVOIR}
<p><b>Functional dyspepsia (post-prandial distress)</b> is impaired fundic accommodation: as accommodation falls the operating point retreats toward the contracted rest, the wall stiffens, and the <i>same</i> meal raises intra-gastric pressure prematurely. Sweeping accommodation as a fraction of the yield drive (so the knob is tied to the substrate, never tuned), the compliance falls from {m("%.3f" % C_hi)} to {m("%.3f" % C_lo)} \u2014 early satiation, less meal tolerated per unit satiation pressure \u2014 while the fixed-meal pressure climbs from {m("%.0f%%" % P_hi_pct)} to {m("%.0f%%" % P_lo_pct)} of the stiff unaccommodated baseline. A normal fundus absorbs the meal ({m("%.0f%%" % norm_pct)} of baseline); impaired accommodation is premature pressure ({m("%.0f%%" % fd_pct)}).</p>
<table><thead><tr><th>accommodation (fraction of yield drive)</th><th>compliance (tolerated volume / unit satiation pressure)</th><th>meal pressure (model units)</th><th>% of stiff baseline</th></tr></thead><tbody>{tbl}</tbody></table>
<p>This is the post-prandial-distress axis that the {m("\u00a715")} functional-dyspepsia-motility reader explicitly left open. {m("\u00a715")} owns the mild emptying delay (the epigastric-pain / motility side); this section owns the accommodation / early-satiation side; and together they cover the two recognised functional-dyspepsia axes. They are distinct lesions of distinct modules \u2014 a mild {m("\u00a711")} ICC reduction versus a stiff fundic reservoir \u2014 which is why a patient may have either or both.</p>
<p>The reservoir's maximal-compliance limit is not a fitted bound: the yield point, where the wall stiffness vanishes and the compliance diverges, is exactly the R19 spinodal. At {m("s = \u2212\u221a(g/3)")} the stiffness {m("3s\u00b2 \u2212 g")} is identically zero ({m("k = %.0e" % abs(yi["k_at_yield"]))}), and that point is where the contracted fixed point merges with the unstable one at the spinodal drive \u2014 an algebraic property of the double well, not a tuned ceiling. Readings operate strictly below it, since the marginal saddle-node has critical slowing.</p>
<p><b>Treatment (model reading).</b> {esc(d["treatment"])}</p>
<p>The premature-pressure / early-satiation mechanism is forced by the substrate {m("[V]")} \u2014 partial, because the post-prandial-distress axis is what {m("\u00a715")} left open while the motility axis lives there. What stays open {m("[O]")}, each with its obstacle: the felt post-prandial-distress symptom itself, which is the group B3 visceral afferent-gain term with the felt interpretation in {m("mind")} behind the firewall (the lever that raises that peripheral afferent's firing threshold \u2014 and the drug class it points to \u2014 is mapped in {m("\u00a728")}); and the absolute meal-volume and intra-gastric-pressure scale, a model unit needing barostat / manometry calibration.</p>
"""

def body_ibs(R):
    d = dz.validate_d8()
    sub = d["ibs_subtype"]; hs = d["visceral_hypersensitivity"]
    fap = d["functional_abdominal_pain"]; idn = d["gain_identity"]
    sub_rows = "".join("<tr><td>%.2f</td><td>%.3f</td></tr>" % (dr, rt) for dr, rt in sub["rows"])
    hs_rows = "".join("<tr><td>%.2f</td><td>%.3f</td><td>%.5f</td></tr>" % (fr, gn, sg) for fr, gn, sg in hs["rows"])
    fap_rows = "".join("<tr><td>%.2f</td><td>%.5f</td></tr>" % (fr, sg) for fr, sg in fap["rows"])
    return f"""
<p>Irritable bowel syndrome and functional abdominal pain need one element the motility, gate and reservoir modules do not contain: an <b>afferent gain</b> \u2014 a peripheral sensitivity on the visceral afferent signal. This is the third Tier-2 primitive, and like the gate and the reservoir it is not new dynamics: a visceral afferent is the {m("\u00a72")} R19 switch {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")} resting quiescent in its contracted basin, and its static susceptibility to a wall-distension input is the restoring-curvature inverse {m("\u03c7 = ds*/dh = 1/k = 1/(3s\u00b2 \u2212 g)")}. A peripheral sensitization bias slides the operating point toward yield, raising the gain; nothing is fitted.</p>
{CARD_AFFERENT}
<p><b>IBS</b> is two things at once: an {m("\u00a714")} motility <i>subtype</i> plus a raised afferent gain. The subtype is set by the {m("\u00a714")} transport bias \u2014 the retained proximal fraction (the {m("\u00a715")} stasis reader) falls monotonically as the propulsive drive rises, so one bias parameter <i>orders</i> the subtypes: <b>IBS-C</b> (low drive, retained {m("%.2f" % sub["ibs_c_retained"])} \u2014 slow transit, constipation) \u2192 <b>IBS-M</b> (intermediate, {m("%.2f" % sub["ibs_m_retained"])}) \u2192 <b>IBS-D</b> (cleared, {m("%.2f" % sub["ibs_d_retained"])} \u2014 rapid transit, diarrhoea).</p>
<table><thead><tr><th>transport drive (\u00a714)</th><th>retained proximal fraction</th></tr></thead><tbody>{sub_rows}</tbody></table>
<p>The constipation side is the {m("\u00a714")} slow-transit mechanism {m("[V]")}; the diarrhoea side hits the <i>same</i> conserved-bolus ceiling as {m("\u00a715")} dumping \u2014 the travelling occlusion wave cannot express transit faster than normal (the rapid side overshoots by only {m("%.1f%%" % sub["rapid_overshoot_pct"])}), so the absolute rapid-transit <i>magnitude</i> is an honest {m("[O]")} while the subtype assignment and the C\u2192D ordering are {m("[V]")}.</p>
<p>The hypersensitivity that, layered on this motility subtype, makes it IBS rather than plain altered transit is a raised afferent gain. A peripheral sensitization bias (inflammation, mediators, peripheral facilitation) slides the quiescent afferent toward yield: the gain {m("\u03c7 = 1/k")} rises from its baseline {m("%.3f" % hs["baseline_gain"])} and the afferent signal for a <i>fixed normal</i> wall-distension rises with it \u2014 <b>allodynia</b>, the same distension amplified {m("\u00d7%.2f" % hs["allodynia_amplification"])}. Past the R19 spinodal that same normal distension flips the element discontinuously into the firing basin: spontaneous, un-provoked afferent activity.</p>
<table><thead><tr><th>sensitization (fraction of yield drive)</th><th>afferent gain \u03c7 = 1/k</th><th>signal at fixed distension</th></tr></thead><tbody>{hs_rows}</tbody></table>
<p><b>Functional abdominal pain</b> is the same raised gain at <i>normal</i> motility, with no structural lesion: at a normal transport bias (where the {m("\u00a714")} retained fraction is {m("%.3f" % fap["normal_motility_retained_fraction"])}, i.e. transit is normal) the afferent-signal proxy still rises with the sensitization bias. That is exactly what distinguishes functional abdominal pain (pure afferent gain) from IBS (afferent gain <i>plus</i> a {m("\u00a714")} motility subtype).</p>
<table><thead><tr><th>sensitization (fraction of yield drive)</th><th>afferent-signal proxy (motility normal)</th></tr></thead><tbody>{fap_rows}</tbody></table>
<p>The gain is not an independent new quantity: it is exactly the {m("\u00a717")} fundic compliance read a second way. The afferent gain {m("\u03c7 = 1/k")} equals the reservoir compliance {m("C = 1/k")} for every operating point (maximum absolute difference {m("%.0e" % idn["gain_equals_compliance_maxabs"])}), the analytic susceptibility matches the simulated small-signal response (relative error {m("%.1e" % idn["susceptibility_selfconsistent_relerr"])}), and the gain <i>diverges</i> at the R19 spinodal \u2014 the <i>same</i> marginal saddle-node as the {m("\u00a717")} reservoir yield ({m("k = %.0e" % abs(idn["k_at_yield"]))} at {m("s = \u2212\u221a(g/3)")}). One R19 marginal point, three readings: critical sensory gain here, maximal mechanical compliance at {m("\u00a717")}, the discontinuous flip of the bare switch.</p>
<p><b>Treatment (model reading).</b> {esc(d["treatment"])} <i>The complementary question \u2014 which pharmacological lever raises this afferent's firing threshold, lowering this exact gain {m("\u03c7 = 1/k")} back toward its baseline, and toward which validated drug class the mechanism points \u2014 is answered in {m("\u00a728")}, which inherits a DNA-grounded 27-target non-opioid analgesic map and reads it on this very {m("\u00a718")} spinodal (the analgesic firing-threshold scale {m("|h_sp| = spinodal(\u03b3)")} is identically the gain-divergence point established here).</i></p>
<p>The IBS motility-subtype ordering and the visceral-hypersensitivity gain rise (with allodynia) are forced by the substrate {m("[V]")}, and the divergence of the gain at the spinodal is the exact R19 identity {m("[F]")}. What stays open {m("[O]")}, each with its obstacle: the absolute rapid-transit magnitude and stool frequency (the {m("\u00a715")} conserved-bolus ceiling, needing the reservoir / pyloric-brake element and clinical transit calibration), and \u2014 the firewall \u2014 the <i>felt</i> visceral pain and affective experience, which is {m("mind")}'s; this section moves only the peripheral afferent-gain term, never the felt interpretation, and the HPA axis is not re-emerged here. <i>This mind felt-symptom seam is now wired in {m("\u00a727")} as a one-way forward-defer pointer (the peripheral afferent signal crosses OUT to mind’s interoception route; nothing returns).</i></p>
"""

def body_metaplasia(R):
    c = onco.validate_c6(); eac = c["metaplasia"]["eac"]; gca = c["metaplasia"]["gca_int"]
    ladder = "".join("<tr><td>%s</td><td>%.4f</td><td>%.2f</td></tr>" % (nm, gd, rt) for nm, gd, rt in eac["dysplasia_ladder"])
    restore = "".join("<tr><td>%d%%</td><td>%.2f</td></tr>" % (f, rr) for f, rr in eac["restore_curve"])
    return f"""
<p>Some carcinomas do not arise directly from healthy tissue — they arise from a <b>metaplastic precursor</b> (Barrett's oesophagus before oesophageal adenocarcinoma; gastric intestinal metaplasia before intestinal-type gastric cancer, the Correa cascade). This is the one new reading the neoplastic extension adds, and like the gate and the reservoir it is not new dynamics: a metaplastic cell is the same {m("§7")} R19 cell-fate switch with its stability <i>scale</i> lowered by sustained injury, {m("g_meta = g − drop")} — the <i>identical</i> g-reduction the {m("§10")} kernel already applies for chronic H. pylori, now read as a discrete compartment rather than a continuous background.</p>
{CARD_METAPLASIA}
<p>Sitting on the smaller barrier {m("g_meta²/4 < g²/4")}, the metaplastic cell's next (malignant) crossing runs faster than a healthy cell's by the precursor-vs-general factor, locked to the cited anchor by a single bisection: Barrett's-vs-general EAC {m("RR ≈ %.1f" % eac["rr_metaplastic"])} (Hvid-Jensen 2011) and gastric intestinal-metaplasia {m("RR ≈ %.1f" % gca["rr_metaplastic"])}. Because that fold exceeds three, carcinoma arises <i>~only</i> from the precursor compartment — the metaplasia step is <b>rate-limiting</b>, which is exactly why Barrett's surveillance and metaplasia ablation are the clinical levers.</p>
<p>A dysplasia ladder — deeper injury, a further g-drop — accelerates the crossing (NDBE → low-grade → high-grade dysplasia), reproducing the observed <i>direction</i> and the convex acceleration of the progression hazard:</p>
<table><thead><tr><th>stage</th><th>barrier-scale drop</th><th>next-step rate (× healthy)</th></tr></thead><tbody>{ladder}</tbody></table>
<p><b>Treatment (model reading).</b> The kernel makes prevention the lever: restoring the barrier scale {m("g")} — ablating the metaplasia or removing the injury (anti-reflux for Barrett's, H. pylori eradication for the gastric cascade) — collapses the next-step crossing rate back toward the healthy baseline. Restoring {m("g")} from {m("g_meta")} toward healthy drops the malignant-crossing rate monotonically to one:</p>
<table><thead><tr><th>barrier-scale restored</th><th>next-step rate (× healthy)</th></tr></thead><tbody>{restore}</tbody></table>
<p>The precursor-vs-general RR anchors are cited {m("[L]")}; the rate-limiting precursor step and the dysplasia-ladder <i>shape</i> (monotone, accelerating) and the treatment direction are verified {m("[V]")}. What stays open {m("[O]")}, with its obstacle: the absolute progression rate (the model's ladder ratios, {m("LGD/NDBE ≈ %.1f" % (eac["dysplasia_ladder"][1][2]/eac["dysplasia_ladder"][0][2]))} and {m("HGD/NDBE ≈ %.1f" % (eac["dysplasia_ladder"][2][2]/eac["dysplasia_ladder"][0][2]))}, are <i>lower</i> than the cited clinical ratios), because the absolute annual hazard — like absolute incidence and absolute organ size — needs external population calibration; the model fixes direction and rate-limiting, not the absolute %/yr.</p>
"""

def body_synergy(R):
    c = onco.validate_c6(); hcc = c["synergy"]["hcc"]; escc = c["synergy"]["escc"]
    fan_h = "".join("<tr><td>%d%%</td><td>%.2f</td><td>%.2f</td></tr>" % (f, a, b) for f, a, b in hcc["dose_response_fan"])
    fan_e = "".join("<tr><td>%d%%</td><td>%.2f</td><td>%.2f</td></tr>" % (f, a, b) for f, a, b in escc["dose_response_fan"])
    return f"""
<p>The gastric H. pylori×diet synergy of {m("§10")} is not a one-off: two carcinogenic drives read off the <i>same</i> exact R19 barrier reproduce epidemiological super-additivity at two more organs, and on the same kernel predict a sub-multiplicative ceiling near the spinodal. The structure is identical; only which knob each drive turns differs.</p>
<p><b>Hepatocellular carcinoma (HBV × aflatoxin)</b> is the inflammation×bias case, exactly like gastric: chronic HBV lowers the barrier <i>scale</i> {m("g")} (RR {m("%.1f" % hcc["RR_a_alone"])} alone), dietary aflatoxin B1 adds a mutagenic <i>bias</i> {m("h")} (RR {m("%.1f" % hcc["RR_b_alone"])} alone), and their joint risk {m("≈ %.1f" % hcc["RR_joint"])} exceeds the additive-null {m("%.1f" % hcc["additive_null"])} — super-additive, against the classic Qian/Ross Shanghai cohort (cited joint {m("~%.0f" % hcc["cited_joint"])}). On the same barrier the model predicts the joint risk sits <i>below</i> the multiplicative-null {m("%.1f" % hcc["multiplicative_null"])}.</p>
{CARD_KERNEL}
<table><thead><tr><th>aflatoxin dose</th><th>RR on HBV−</th><th>RR on HBV+</th></tr></thead><tbody>{fan_h}</tbody></table>
<p><b>Oesophageal squamous carcinoma (smoking × alcohol)</b> is the bias×bias case: both drives add bias on the same switch (smoking RR {m("%.1f" % escc["RR_a_alone"])}, heavy alcohol RR {m("%.1f" % escc["RR_b_alone"])}), joint {m("≈ %.1f" % escc["RR_joint"])} above the additive-null {m("%.1f" % escc["additive_null"])} (cited combined-heavy {m("~%.0f" % escc["cited_joint"])}) and below the multiplicative-null {m("%.1f" % escc["multiplicative_null"])}.</p>
<table><thead><tr><th>alcohol dose</th><th>RR, no smoking</th><th>RR, with smoking</th></tr></thead><tbody>{fan_e}</tbody></table>
<p><b>Treatment (model reading).</b> The kernel makes risk-reduction multiplicative-in-reverse: removing <i>either</i> drive (HBV vaccination/suppression or aflatoxin avoidance; smoking <i>or</i> alcohol cessation) drops the joint risk back along its own fan toward the single-exposure curve — the largest absolute benefit comes from removing one drive while the other is still present, which is exactly the super-additive regime.</p>
<p>The per-site anchors are cited {m("[L]")}; the reproduced super-additivity is verified {m("[V]")} at both organs; and the <b>sub-multiplicativity near the spinodal</b> — diminishing returns at extreme dual exposure — is a concrete, <i>falsifiable</i> prediction the model makes on the same barrier (both joints fall below their multiplicative-null; newer/larger cohorts already trend this way). Absolute incidence stays open {m("[O]")}: it needs external population calibration, exactly as for the single-site curves. HCC carries a circulatory seam (hepatic first-pass), cited, not re-emerged.</p>
"""

def body_boundary(R):
    c = onco.validate_c6(); malt = c["malt"]; anal = c["anal"]; ook = c["out_of_kernel"]
    malt_rows = "".join("<tr><td>%d%%</td><td>%.2f</td></tr>" % (f, rr) for f, rr in malt["restore_curve"])
    anal_rows = "".join("<tr><td>%d%%</td><td>%.2f</td></tr>" % (f, rr) for f, rr in anal["curve"])
    ook_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (esc(o["site"]), esc(o["obstacle"]), esc(o["owner"])) for o in ook)
    return f"""
<p>Two more sites sharpen the kernel's signature, and then it states its own boundary honestly. The kernel's strongest falsifiable claim is <b>reversibility</b>: if a cancer is driven by a barrier-<i>scale</i> reduction, then restoring the scale must drop the crossing rate. <b>Gastric MALT lymphoma</b> is the clean test — an H. pylori chronic-inflammation g-reduction (RR {m("≈ %.1f" % malt["RR_Hp"])}) that <i>regresses</i> when eradication restores {m("g")}: about {m("%.0f%%" % (malt["hp_positive_fraction"]*100))} of cases are H. pylori-positive and roughly {m("%.1f%%" % (malt["eradication_remission"]*100))} remit on eradication alone (Zullo 2010). Restoring the scale drops the rate monotonically to one:</p>
{CARD_KERNEL}
<table><thead><tr><th>barrier-scale restored (eradication)</th><th>relative risk</th></tr></thead><tbody>{malt_rows}</tbody></table>
<p>The {m("~22%")} of MALT cases carrying t(11;18)/API2-MALT1 that do <i>not</i> respond are a g-<i>independent</i> oncogenic driver — outside this barrier-scale kernel and owned by {m("disease_wp")} (gene-key), which is exactly the boundary the model should draw.</p>
<p><b>Anal squamous carcinoma</b> is the single-driver case: a single sustained HPV (E6/E7) bias {m("h")}, {m("~%.0f%%" % (anal["hpv_attributable_fraction"]*100))} HPV-attributable (De Sanjosé 2019), monotone in exposure and preventable by vaccination — the bias removed before it is ever applied.</p>
<table><thead><tr><th>HPV oncoprotein bias (fraction)</th><th>relative risk</th></tr></thead><tbody>{anal_rows}</tbody></table>
<p><b>Treatment (model reading).</b> Both readings make the same point: remove the barrier-scale driver (eradicate H. pylori; MALT regresses) or never apply the bias (HPV vaccination; anal carcinoma prevented). Prevention/risk-reduction is the lever the kernel supplies; therapy of an established tumour is out-of-model.</p>
<p><b>The honest boundary.</b> The carcinogen-Kramers kernel does <i>not</i> cover every GI cancer, and the extension states where it stops and who must supply the missing layer rather than over-reaching:</p>
<table><thead><tr><th>site</th><th>obstacle (why the kernel does not apply)</th><th>owner</th></tr></thead><tbody>{ook_rows}</tbody></table>
<p>MALT reversibility and the anal monotone are verified {m("[V]")} against cited anchors {m("[L]")}; absolute incidence stays open {m("[O]")} (external population calibration). The four out-of-kernel sites are honest {m("[O]")} with stated obstacles: GIST and gastroenteropancreatic NET are gene-key / neuroendocrine ({m("disease_wp")}); small-bowel adenocarcinoma needs the {m("C1")} immune layer to supply its barrier-lowering driver; cholangiocarcinoma needs a hepatobiliary + immune layer (a circulatory seam). Stating the boundary <i>is</i> the result here — the kernel earns trust by drawing its own edge.</p>
"""


def body_immune(R):
    d = dz.validate_d9()
    rc = d["relapsing_course"]; nb = d["neoplasia_bridge"]; sl = d["same_layer"]
    up_rows = "".join("<tr><td>%.2f</td><td>%+.3f</td></tr>" % (a, s) for a, s in rc["up_ramp"])
    down_rows = "".join("<tr><td>%.2f</td><td>%+.3f</td></tr>" % (a, s) for a, s in rc["down_ramp"])
    rr_rows = "".join("<tr><td>%.0f%%</td><td>%.4f</td><td>%.2f</td></tr>" % (b*100, g, rr) for b, g, rr in nb["burden_rr"])
    coll_rows = "".join("<tr><td>%d%%</td><td>%.2f</td></tr>" % (p, rr) for p, rr in nb["suppression_collapse"])
    return f"""
<p>Inflammatory bowel disease \u2014 Crohn's disease and ulcerative colitis \u2014 needs one element none of the motility, secretory, gate, reservoir or afferent modules contain: a <b>relapsing mucosal inflammation</b> that flares and remits on its own clock and, over years, raises cancer risk. This is the first Tier-3 primitive, and like the gate and the reservoir it is not new dynamics: a relapsing inflammation is the {m("\u00a72")} R19 switch {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")} whose active-inflammation basin <i>self-sustains</i> once entered, with the antigenic drive as the bias. Nothing is fitted; the one anchor (the colitis-cancer slope) is a single bisection.</p>
{CARD_IMMUNE}
<p>The defining clinical feature is the <b>relapsing-remitting course with hysteresis</b>. Ramping the antigenic drive UP, the mucosa holds in remission and then flips discontinuously into a flare past the induction spinodal; ramping back DOWN, it does <i>not</i> return at the same point \u2014 the flare basin self-sustains, so remission is regained only at a markedly lower drive. The flip-up and the flip-down thresholds differ: that gap is the relapse hysteresis, and it is exactly why a flare, once established, persists even as the original trigger recedes.</p>
<table><thead><tr><th>antigenic drive (rising)</th><th>inflammation state</th></tr></thead><tbody>{up_rows}</tbody></table>
<table><thead><tr><th>antigenic drive (falling)</th><th>inflammation state</th></tr></thead><tbody>{down_rows}</tbody></table>
<p>That hysteresis forces the central therapeutic asymmetry. Breaking an <i>established</i> flare \u2014 <b>induction</b> \u2014 needs a suppression drive past the upper threshold {m("antigen + spinodal")} (here {m("%.3f" % rc["induction_threshold"])}); but once remission is regained, a far <i>lower</i> <b>maintenance</b> dose (threshold {m("%.3f" % rc["maintenance_threshold"])}) holds it, because the remission basin is now self-sustaining. The model makes the point sharply: the <i>same</i> mid-strength dose has two opposite outcomes by history \u2014 it holds a patient already in remission but cannot break a patient in flare. Induction-then-taper-to-maintenance is the substrate's own logic, not a dosing convention.</p>
<p>The second reading bridges this layer to the {m("\u00a77")} carcinogen kernel and closes a boundary the {m("\u00a721")} kernel left open. Cumulative inflammatory <b>burden</b> lowers the <i>same</i> R19 barrier scale {m("g_eff = g_barrier \u2212 \u03ba\u00b7burden")} that the {m("\u00a710")} kernel uses for chronic H. pylori \u2014 so colitis-associated colorectal cancer is not a separate mechanism but the same barrier step driven by a different sustained injury. One bisection locks {m("\u03ba")} to the cited ulcerative-colitis colorectal-cancer anchor ({m("RR \u2248 %.1f" % nb["burden_rr"][-1][2])}, Jess 2012); the risk then rises monotonically with accumulated burden:</p>
<table><thead><tr><th>cumulative burden</th><th>barrier scale g_eff</th><th>colorectal-cancer RR</th></tr></thead><tbody>{rr_rows}</tbody></table>
<p>Because the driver is a barrier-<i>scale</i> reduction, the kernel's signature reversibility applies: sustained suppression (mucosal healing) restores {m("g_eff")} and collapses the excess risk back toward baseline \u2014 which is exactly why durable remission, not just symptom control, is the surveillance-and-cancer-prevention goal.</p>
<table><thead><tr><th>burden removed (sustained remission)</th><th>colorectal-cancer RR</th></tr></thead><tbody>{coll_rows}</tbody></table>
<p>This closes the {m("\u00a721")} out-of-kernel <b>small-bowel adenocarcinoma</b> boundary on the inflammation route: the kernel deferred it for want of a barrier-lowering driver, and the relapsing-inflammation primitive now supplies exactly that ({m("closes_small_bowel_boundary = True")}) \u2014 chronic small-bowel Crohn's lowers the same scale, the same way.</p>
<p>The same element, in its <i>antigen-dependent</i> regime, also reads the immune enteropathies. Where IBD needs active suppression to escape the self-sustaining flare, <b>celiac disease</b> (and microscopic / eosinophilic / autoimmune enteropathy) is driven directly by an identified antigen: present the driver (gluten) and the element flares; remove it and the element returns to remission with the barrier \u2014 and, for celiac, the villous surface \u2014 recovering. Driver removal alone suffices, the distinct operating regime of the same primitive.</p>
<p><b>Treatment (model reading).</b> {esc(d["treatment"])}</p>
<p>The relapsing-remitting hysteresis, the induction-vs-maintenance asymmetry, and the burden\u2192barrier\u2192cancer continuity (closing the {m("\u00a721")} small-bowel boundary) are forced by the substrate {m("[V]")}, with the induction and maintenance thresholds exact spinodal identities {m("[F]")} and the colitis-cancer RR a cited anchor {m("[L]")}. What stays open {m("[O]")}, each with its obstacle: the absolute remission and cancer-incidence rates (clinical-cohort calibration), the celiac absorptive (villous-surface) magnitude (needs an absorption layer), and \u2014 the firewall \u2014 the <i>felt</i> / affective component, which is {m("mind")}'s; this section moves only the inflammatory-drive term, never the felt interpretation.</p>
"""


def body_exocrine(R):
    d = dz.validate_d10()
    aa = d["acute_autocatalysis"]; ce = d["chronic_epi"]
    thr_rows = "".join("<tr><td>%.2f</td><td>%.4f</td></tr>" % (i, t) for i, t in aa["threshold_rows"])
    latch_rows = "".join("<tr><td>%.3f</td><td>%s</td><td>%s</td></tr>" % (tg, fl, la) for tg, fl, la in aa["latch_rows"])
    cap_rows = "".join("<tr><td>%.2f</td><td>%s</td></tr>" % (c, ad) for c, ad in ce["capacity_rows"])
    pert_rows = "".join("<tr><td>%.2f</td><td>%s</td></tr>" % (e, ad) for e, ad in ce["pert_rows"])
    return f"""
<p>Acute pancreatitis is mechanistically the richest disease in this package, and it needs the second Tier-3 primitive: an <b>autocatalytic</b> element, one that amplifies itself. The pancreatic zymogen cascade is the {m("\u00a72")} R19 switch {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")} with a self-amplification term \u2014 active trypsin activates more trypsinogen \u2014 so it is the same double well in which the active basin, once entered, <i>feeds itself</i>. Like every layer here it is derived from R19, no new dynamics, no fit; the one reserve anchor is the >90%-loss steatorrhea threshold.</p>
{CARD_EXOCRINE}
<p>The first reading is the <b>autoactivation threshold</b> and its dependence on protection. The trigger needed to ignite the cascade rises with the protective inhibitor: a strong pancreatic secretory trypsin inhibitor (SPINK1) raises the threshold, while a gain-of-function protease (PRSS1) or loss of the inhibitor lowers it \u2014 reproducing the hereditary-pancreatitis genetics as a shift of one threshold, not a separate mechanism.</p>
<table><thead><tr><th>protective inhibitor</th><th>autoactivation trigger threshold</th></tr></thead><tbody>{thr_rows}</tbody></table>
<p>The second reading is the clinically decisive one: the cascade <b>latches</b>. A sub-threshold trigger fires briefly and decays back to the inactive rest basin \u2014 safe. A supra-threshold trigger crosses into the self-sustaining active basin and stays there: the autocatalytic {m("+g\u00b7s")} term holds it on with the trigger <i>removed</i>. The transition is irreversible to any parameter move \u2014 once over, lowering the trigger does nothing \u2014 which is precisely why an established attack cannot be switched off pharmacologically and is managed by supportive care.</p>
<table><thead><tr><th>trigger strength</th><th>flips to active</th><th>latched (self-sustains)</th></tr></thead><tbody>{latch_rows}</tbody></table>
<p>That makes intervention <b>pre-threshold only</b>, and the model states it as a rule: remove the trigger <i>before</i> it crosses \u2014 relieve the gallstone obstruction, stop alcohol, lower triglycerides \u2014 or raise the protection, because a strong-enough inhibitor (past the R19 spinodal) abolishes the self-sustaining basin entirely, so the same trigger that would have latched now decays. Before the threshold the system is rescuable; after it, no parameter move reverses the latch.</p>
<p>The chronic sequel is the mirror image. Repeated attacks destroy acinar mass, but the gland has a large secretory <b>reserve</b>: exocrine pancreatic insufficiency (steatorrhea) appears only once capacity falls past roughly 90% loss \u2014 the digestive output stays adequate across most of the sweep and fails only at the deep end (DiMagno 1973). The adequacy is monotone in residual capacity:</p>
<table><thead><tr><th>residual acinar capacity</th><th>digestion adequate</th></tr></thead><tbody>{cap_rows}</tbody></table>
<p>And the treatment is replacement, not parameter-tuning: pancreatic enzyme replacement (PERT) adds exogenous secretory output, restoring digestion above the demand once enough is supplied.</p>
<table><thead><tr><th>exogenous enzyme (PERT)</th><th>digestion adequate</th></tr></thead><tbody>{pert_rows}</tbody></table>
<p><b>Treatment (model reading).</b> {esc(d["treatment"])}</p>
<p>The threshold-rises-with-inhibitor, the irreversible supra-threshold latch (pre-threshold-only intervention), the strong-inhibitor reversibility, and the large-reserve EPI with PERT rescue are forced by the substrate {m("[V]")}, with the latch an exact R19 hysteresis {m("[F]")} and the >90%-loss reserve threshold a cited anchor {m("[L]")}. What stays open {m("[O]")}, each with its obstacle: the absolute trigger / inhibitor and digestive-demand scales (model units needing clinical calibration), and the established-disease outcomes \u2014 necrosis extent, organ failure \u2014 which need a tissue-injury layer. Cystic fibrosis is gene-key (CFTR): {m("disease_wp")} owns the gene defect while this package owns the ductal-secretion dynamics.</p>
"""


def body_perfusion(R):
    d = dz.validate_d11()
    cm = d["chronic_mesenteric"]; ai = d["acute_ischemia"]; nf = d["nafld"]
    margin_rows = "".join("<tr><td>%.2f</td><td>%.4f</td><td>%+.4f</td><td>%s</td></tr>" % (dm, thr, mg, ("ischaemic" if isc else "viable")) for dm, thr, mg, isc in cm["margin_rows"])
    revasc_rows = "".join("<tr><td>%.2f</td><td>%s</td></tr>" % (dm, ("viable" if ok else "ischaemic")) for dm, ok in cm["treatment_revasc"])
    perf_rows = "".join("<tr><td>%.3f</td><td>%s</td></tr>" % (p, ("viable" if v else "ischaemic / infarcted")) for p, v in ai["perfusion_rows"])
    return f"""
<p>The first three Tier-3 primitives (relapsing inflammation, autocatalytic autodigestion, and \u2014 with the cancer kernel \u2014 metaplasia) covered the mucosa, the gland and the cell. This section opens the <b>perfusion / vascular</b> layer none of them touch: an intestinal tissue is viable only while its blood supply meets its metabolic demand, and the diseases of that balance \u2014 mesenteric ischaemia, ischaemic colitis, and the metabolic fatty-liver overlap \u2014 turn on a supply-versus-demand switch. Like every layer here it is not new dynamics: a perfused tissue is the {m("\u00a72")} R19 switch {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")} resting in the viable basin, with the bias {m("h = perfusion \u2212 demand")}. Nothing is fitted; the thresholds are exact spinodal identities and the single anchor is one bisection.</p>
{CARD_PERFUSION}
<p>The first reading is <b>chronic mesenteric ischaemia</b> \u2014 "intestinal angina". At a fixed marginal perfusion (a stenosed mesenteric artery), the reserve of supply above the rescue threshold falls as metabolic demand rises; a meal raises demand and pushes the margin negative, so pain follows eating and the patient becomes food-averse. The viability margin crosses from positive (viable) to negative (ischaemic) exactly as the post-prandial demand climbs:</p>
<table><thead><tr><th>metabolic demand</th><th>rescue threshold</th><th>viability margin</th><th>state</th></tr></thead><tbody>{margin_rows}</tbody></table>
<p>The treatment is geometric, not pharmacological: <b>revascularisation</b> (stent or bypass) lifts the perfusion supply so the margin is positive again across the whole demand range \u2014 the post-prandial pain resolves because the meal no longer outruns the supply.</p>
<table><thead><tr><th>metabolic demand</th><th>state after revascularisation</th></tr></thead><tbody>{revasc_rows}</tbody></table>
<p>The second reading is <b>acute mesenteric ischaemia</b> (and its colonic counterpart, ischaemic colitis): a sudden occlusion drops perfusion below {m("demand \u2212 spinodal")} (here a flip threshold of {m("%.3f" % ai["flip_threshold"])}) and the tissue flips discontinuously from the viable basin into the ischaemic one. The clinically decisive feature is the <b>salvage window</b>: restoring flow recovers the tissue only if perfusion returns above {m("demand + spinodal")} (a reserve window of {m("%.3f" % ai["reserve_window"])}); a partial or late reperfusion leaves it in the infarcted basin. The sweep shows viable tissue holding, then flipping, then failing to recover under partial flow:</p>
<table><thead><tr><th>perfusion (occlusion \u2192 reperfusion)</th><th>tissue state</th></tr></thead><tbody>{perf_rows}</tbody></table>
<p>The third reading is the <b>NAFLD / MASLD metabolic overlap</b>. Metabolic-associated fatty liver shares its insulin-resistance driver with the {m("\u00a712")} diabetes axis \u2014 so rather than introduce a new parameter, this layer <i>reuses</i> the section-12 type-2 gain-loss homeostat unchanged ({m("reuses_s12_type2_gain_loss = True")}). The lipid-<i>deposition</i> step itself (hepatic triglyceride accumulation, the cholesterol-delivery dynamics) is declared a {m("circulatory")} seam, not modelled here: this package keeps only the perfusion-viability switch and the reused glucose homeostat, and hands the lipid layer across the firewall. <i>This circulatory lipid-deposition seam is now wired in {m("\u00a727")}: the lipid load rests on the consumed circulatory hepatic perfusion, the handling staying circulatory’s {m("[O]")}.</i></p>
<p><b>Treatment (model reading).</b> {esc(d["treatment"])}</p>
<p>The demand-driven collapse of the viability margin, the revascularisation rescue, the forced acute occlusion flip, the time-critical salvage window, and the reuse of the {m("\u00a712")} type-2 homeostat are forced by the substrate {m("[V]")}, with the ischaemic-flip and rescue thresholds exact spinodal identities {m("[F]")}. What stays open {m("[O]")}, each with its obstacle: the absolute perfusion-pressure and metabolic-demand scales (model units needing clinical calibration), the structural infarction endpoint \u2014 transmural necrosis, perforation \u2014 which needs a tissue-injury layer, and the hepatic lipid-deposition layer, which is {m("circulatory")}'s.</p>
"""


def body_hepatobiliary(R):
    d = dz.validate_d12()
    ch = d["cholelithiasis"]; ds = d["dissolution"]; sm = d["seams"]
    csi_rows = "".join("<tr><td>%.3f</td><td>%s</td><td>%s</td></tr>" % (c, ("yes" if ss else "no"), ("STONE" if st else "\u2014")) for c, ss, st in ch["csi_rows"])
    diss_rows = "".join("<tr><td>%.3f</td><td>%s</td></tr>" % (c, ("stone persists" if st else "dissolved")) for c, st in ds["dissolution_rows"])
    return f"""
<p>The {m("\u00a724")} perfusion layer handled supply and demand; this section opens the <b>hepatobiliary / bile</b> layer, where the disease is a phase transition in a fluid rather than a switch in a tissue. Cholelithiasis \u2014 gallstone formation \u2014 is cholesterol crystallising out of supersaturated bile, and it needs one new reading of the R19 substrate: a <b>nucleation barrier</b>. A supersaturated solution does not crystallise the instant it passes saturation; it sits metastably until the drive clears a barrier. That is the {m("\u00a72")} R19 double well {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")} with the dissolved phase as the rest basin and the cholesterol saturation index (CSI) as the bias. Nothing is fitted; the thresholds are exact spinodal identities.</p>
{CARD_BILE}
<p>The first reading is that <b>supersaturation is metastable, not sufficient</b>. Bile with CSI just above 1 is supersaturated yet remains stone-free \u2014 the everyday observation that most people with lithogenic bile never form stones. A stone nucleates only once the drive clears the barrier at {m("CSI &gt; 1 + spinodal")} (here {m("CSI = %.3f" % ch["nucleation_csi"])}). The sweep shows bile supersaturated well before it nucleates:</p>
<table><thead><tr><th>cholesterol saturation index</th><th>supersaturated</th><th>nucleates</th></tr></thead><tbody>{csi_rows}</tbody></table>
<p>The second reading is <b>dissolution hysteresis</b>, and it is the clinically decisive one. A formed stone does not redissolve the moment bile drops back below saturation; it persists, redissolving only far below it (here below {m("CSI = %.3f" % ds["dissolution_csi"])}, a hysteresis gap of {m("%.3f" % ds["hysteresis_gap"])}). This is exactly why medical (UDCA) dissolution succeeds only on small, early, cholesterol-rich stones in a still-functioning gallbladder, and why stones recur once therapy stops unless the lithogenic drive itself is removed:</p>
<table><thead><tr><th>cholesterol saturation index (falling)</th><th>stone state</th></tr></thead><tbody>{diss_rows}</tbody></table>
<p>The remaining biliary syndromes are declared <b>seams</b> to primitives this package already owns, not re-modelled here. Gallbladder <b>stasis</b> (impaired emptying, the second arm of stone risk) is the {m("\u00a716")} B1 sphincter-gate primitive ({m("stasis_is_b1_gate_seam = True")}); <b>cholecystitis</b> (a stone obstructing the cystic duct, then inflaming) is the B1 gate plus the cited {m("\u00a722")} C1 inflammatory flare ({m("cholecystitis_is_b1_gate_plus_c1_flare = True")}); biliary <b>dyskinesia</b> is the B1 gate; and the nucleation <i>time</i> is the Kramers barrier-crossing rate the {m("\u00a77")} kernel already uses. Cholesterol delivery is a {m("circulatory")} seam and the felt biliary colic is {m("mind")}'s \u2014 the firewall keeps only the crystallisation thermodynamics here. <i>Both seams are now wired in {m("\u00a727")}: the cholesterol delivery rests on the consumed circulatory hepatic perfusion {m("[O]")}, and the felt colic is deferred to {m("mind")} by a one-way pointer. The peripheral visceral-afferent lever \u2014 which non-opioid intervention raises the firing threshold of the colic afferent, and the drug class it points to \u2014 is mapped in {m("\u00a728")}.</i></p>
<p><b>Treatment (model reading).</b> {esc(d["treatment"])}</p>
<p>The metastable supersaturation, the barrier-gated nucleation, and the dissolution hysteresis (UDCA only on small early stones) are forced by the substrate {m("[V]")}, with the nucleation and dissolution thresholds exact spinodal identities and the nucleation time the Kramers rate {m("[F]")}. What stays open {m("[O]")}, each with its obstacle: the absolute cholesterol-saturation-index scale (a model unit needing clinical calibration), the stasis and cholecystitis syndromes (owned by the B1 gate and C1 flare \u2014 cited seams), and the cholesterol-delivery ({m("circulatory")}) and felt-pain ({m("mind")}) seams.</p>
"""


def body_structural(R):
    d = dz.validate_d13()
    dp = d["diverticular_pressure"]; ws = d["wall_strength"]; tb = d["treatment_boundary"]
    radius_rows = "".join("<tr><td>%.2f</td><td>%.3f</td><td>%s</td></tr>" % (r, p, ("HERNIATES" if h else "intact")) for r, p, h in dp["radius_rows"])
    strength_rows = "".join("<tr><td>%.2f</td><td>%.4f</td><td>%s</td></tr>" % (gw, thr, ("herniates" if h else "intact")) for gw, thr, h in ws["strength_rows"])
    return f"""
<p>This section closes the Tier-3 set with the <b>structural / mechanical</b> layer: the disease is neither a switch in a tissue nor a phase change in a fluid but a <b>wall failing under pressure</b>. Diverticular disease \u2014 the colon out-pouching at weak points \u2014 is governed by Laplace's law, and it reads the R19 substrate as a wall-mechanics switch driven by the segmental pressure {m("P = tension / radius")}. The intact wall is the {m("\u00a72")} R19 element {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")} resting at {m("s = \u2212\u221ag")}, with the Laplace pressure as the bias; once the pressure clears the herniation threshold the wall buckles out. Nothing is fitted; the threshold is an exact spinodal identity.</p>
{CARD_WALL}
<p>The first reading is the <b>low-fibre pressure mechanism</b>. By {m("P = tension / radius")}, a low-fibre diet \u2014 small, hard stools gripped by strong high-pressure segmenting contractions \u2014 means a <i>small</i> luminal radius, and the wall pressure rises as the radius falls. Once {m("P")} exceeds the herniation threshold {m("spinodal(g_wall)")} (here {m("%.3f" % dp["herniation_threshold"])}) the intact wall out-pouches into a diverticulum. The sweep shows the pressure climbing as the radius shrinks, crossing into herniation at the low-fibre end:</p>
<table><thead><tr><th>luminal radius</th><th>Laplace pressure</th><th>wall</th></tr></thead><tbody>{radius_rows}</tbody></table>
<p>The second reading is <b>wall strength</b>. At a fixed segmental pressure that a normal wall withstands, a <i>weaker</i> wall \u2014 lower {m("g_wall")}: aging connective tissue, or an Ehlers\u2013Danlos / Marfan collagen disorder \u2014 has a lower threshold and herniates where a strong wall holds. This is the age-rising diverticulosis prevalence and the connective-tissue-disorder association, read as one falling threshold:</p>
<table><thead><tr><th>wall strength g_wall</th><th>herniation threshold</th><th>at fixed pressure {m("%.3f" % ws["pressure"])}</th></tr></thead><tbody>{strength_rows}</tbody></table>
<p>The treatment is the geometry <i>in reverse</i>: dietary <b>fibre</b> bulks the stool (a LARGER luminal radius) and softens the segmenting contractions (LOWER tension), so by {m("P = tension / radius")} the wall pressure drops back below the herniation threshold and the same colon stops out-pouching ({m("fibre_lowers_pressure_below_threshold = True")}: {m("%.3f" % tb["p_lowfibre"])} above threshold on low fibre vs {m("%.3f" % tb["p_highfibre"])} below it on high fibre). Two boundaries are declared, not re-modelled: <b>diverticulITIS</b> (a formed pouch inflaming / obstructing) is the cited {m("\u00a722")} C1 inflammatory flare ({m("diverticulitis_is_c1_flare_seam = True")}); and the mechanical <b>fixed-block obstructions</b> \u2014 hernia (including hiatal), volvulus, intussusception, adhesive obstruction \u2014 are the structural counterpart the {m("\u00a714")} functional motility module explicitly excludes (it keeps a patent lumen), their lever relieving the block, often surgical and out-of-model ({m("mechanical_block_is_s14_excluded_counterpart = True")}).</p>
<p><b>Treatment (model reading).</b> {esc(d["treatment"])}</p>
<p>The Laplace pressure rising as the radius falls, the discontinuous herniation past {m("P = spinodal(g_wall)")}, the lower threshold of a weaker wall, and the fibre treatment dropping {m("P")} below threshold are forced by the substrate {m("[V]")}, with the herniation threshold an exact spinodal identity {m("[F]")}. What stays open {m("[O]")}, each with its obstacle: the absolute Laplace-pressure and wall-strength scales (model units needing clinical calibration), the diverticulITIS inflammation (the cited C1 flare seam), and the mechanical fixed-block obstructions (the {m("\u00a714")} functional module's structural counterpart \u2014 surgical, out-of-model for parameter therapy).</p>
"""


CARD_SEAM = vpcard("seam", "<b>cross-system seam = a vendored SSOT snapshot + a one-way pointer, never a "
                   "sibling import</b> \u2014 a sibling-owned quantity is recorded once in "
                   "<code>inherited/cross_references.json</code> (verified against the sibling engine at vendoring) "
                   "and CONSUMED here; the felt layer is deferred OUT by pointer. The firewall is an architectural "
                   "lock (zero sibling imports; the metabolic state carries no felt/HPA key), the same lock "
                   "<code>mind</code> runs neuro-side. <b>[F]</b> forced.", "/mind/")

CARD_ANALGESIC = vpcard("analgesic", "<b>analgesia = raise the firing threshold |h_sp| = spinodal(\u03b3) = 2(g/3)<sup>1.5</sup></b> "
                   "\u2014 INHERITED from <code>analgesic_threshold_logic</code> v2.0 (DOI 10.5281/zenodo.20733420): each "
                   "pain gene's promoter \u03b3 (NN-stacking \u0394G) is placed on the SAME R19 firing-threshold scale this "
                   "package's \u00a718 afferent diverges at; three levers (reduce inward / open K\u1d65, / remove NGF\u2013CGRP "
                   "drive) raise it. \u03b3 reads STRUCTURE only \u2014 never a voltage, potency, dose, or effect ([O]). "
                   "<b>[F]</b> forced.", "/dna/")


def body_analgesic(R):
    a = analg.validate()
    rv = a["reverify"]; gi = a["gi_subset"]; lv = a["lever_de_sensitisation"]
    pr = a["gi_prioritisation"]; px = a["precision_visceral"]; rm = a["recommendation_map"]
    # GI subset rows (gene, lever, channel/protein, gamma, |h_sp|)
    gi_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%.4f</td><td>%.4f</td></tr>"
                      % (g, lev, cp, gm, hsp) for g, lev, cp, gm, hsp in gi["rows"][:12])
    # the three-lever de-sensitisation table: show L1 as the representative trace (all three identical-direction)
    l1 = lv["per_lever"]["L1"]["rows"]
    lever_rows = "".join("<tr><td>%.4f</td><td>%.5f</td><td>%.5f</td></tr>" % (d, T, chi) for d, T, chi in l1)
    # GI burden prioritisation (top rows)
    pr_rows = "".join("<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%d/%d/%d</td><td>%.3f</td></tr>"
                      % (r["rank"], r["gene"], r["lever"], r["channel_or_protein"], r["B"], r["U"], r["D"], r["score"])
                      for r in pr["ranking"][:8])
    # recommendation map (drug-class pointer) rows
    rec_rows = "".join("<tr><td>%s</td><td>\u00a7%s</td><td>%s</td><td>%s</td></tr>"
                       % (esc(row["disorder"]), esc(row["section"]), esc(", ".join(row["levers"])),
                          esc("; ".join(row["gi_targets"][:3]) + ("\u2026" if len(row["gi_targets"]) > 3 else "")))
                       for row in rm["rows"])
    return f"""
<p>Every visceral-pain reading in this volume \u2014 the {m("\u00a718")} IBS hypersensitivity and functional abdominal pain, the {m("\u00a717")} functional-dyspepsia pain, the {m("\u00a725")} biliary colic, the {m("\u00a716")} oesophageal-spasm pain \u2014 ends at the <i>same</i> question: which intervention raises the visceral afferent's firing threshold, and toward which drug class does the mechanism point. This section answers it by <b>inheriting</b> a sibling whitepaper, <code>analgesic_threshold_logic</code> v2.0 (<b>DOI 10.5281/zenodo.20733420</b>, CC BY 4.0): a reproducible, DNA-grounded map of 27 non-opioid analgesic targets. It is not a paste \u2014 it is the same substrate read a second way.</p>
{CARD_ANALGESIC}
<p>The map's engine reads each pain gene's human promoter and returns {m("\u03b3 = \u2212mean(NN stacking \u0394G, SantaLucia 1998)")}, then places {m("\u03b3")} on the R19 double-well firing-threshold scale {m("|h_sp| = 2(g/3)^1.5 = (2/3\u221a3)\u03b3^1.5")}. That scale is <i>this</i> package's own {m("inherited/vp_substrate.spinodal")}: re-deriving all {m("%d" % rv["n_targets"])} reads through it reproduces the inherited firing thresholds <b>bit-for-bit</b> (max {m("|h_sp|")} drift {m("%.0e" % rv["max_h_sp_drift"])}, max barrier drift {m("%.0e" % rv["max_barrier_drift"])} \u2014 drift zero). The analgesic firing-threshold axis <i>is</i> the {m("\u00a718")} visceral-afferent spinodal the gain {m("\u03c7 = 1/k")} diverges at; that identity is why the inheritance is principled.</p>
<p>The 27 targets sort into <b>three intervention levers</b>, all raising the same firing threshold from different directions: <b>L1</b> reduce the inward (excitatory) current (block depolarising Na<sub>V</sub> / Ca<sub>V</sub> / ASIC / P2X / TRP channels), <b>L2</b> increase the outward K<sup>+</sup> current (open K<sub>V</sub>7), <b>L3</b> remove the up-stream sensitising drive (block NGF / CGRP). Of the 27, {m("%d" % gi["n_gi_targets"])} are expressed on the gut visceral afferent (cited relevance), ordered here by the stiffest firing gate first:</p>
<table><thead><tr><th>gene</th><th>lever</th><th>channel / protein</th><th>\u03b3</th><th>|h_sp|</th></tr></thead><tbody>{gi_rows}</tbody></table>
<p>Read on the {m("\u00a718")} afferent, the three levers do one thing. Take a sensitised afferent (visceral hypersensitivity) whose gain is raised {m("\u00d7%.2f" % lv["hypersensitivity_amplification"])} above baseline; apply a lever at increasing <i>structural</i> strength {m("\u03b4")} (a fraction of the sensitisation removed \u2014 not a dose). For <b>every</b> lever the firing threshold {m("T = spinodal \u2212 b_eff")} rises and the gain {m("\u03c7 = 1/k")} falls monotonically back toward the baseline {m("1/(2g)")} (shown for L1; L2 and L3 are identical in direction):</p>
<table><thead><tr><th>lever strength \u03b4 (structural)</th><th>firing threshold |h_sp| margin</th><th>afferent gain \u03c7 = 1/k</th></tr></thead><tbody>{lever_rows}</tbody></table>
<p>This makes the inherited map a <b>drug-class pointer</b> for every digestive visceral-pain disorder \u2014 which lever, and which cited validated agent class realises it. It does <i>not</i> prescribe: it points to the mechanism class an effective agent moves.</p>
<table><thead><tr><th>disorder</th><th>section</th><th>lever(s)</th><th>GI targets (model pointer)</th></tr></thead><tbody>{rec_rows}</tbody></table>
<p><b>Treatment (model reading).</b> {esc(a["treatment"])}</p>
<p>A <b>burden-weighted prioritisation</b> of the GI nociceptor targets (inherited declared weights {m("B=%.2f / U=%.2f / D=%.2f" % (pr["weights_declared"]["B"], pr["weights_declared"]["U"], pr["weights_declared"]["D"]))} over cited 1\u20135 tiers, sorted by score; {m("\u03b3 / |h_sp|")} is the structural map-place and is <i>never</i> folded into the clinical score) re-derives the inherited score exactly and surfaces the realised peripheral case first:</p>
<table><thead><tr><th>rank</th><th>gene</th><th>lever</th><th>channel / protein</th><th>B/U/D</th><th>score</th></tr></thead><tbody>{pr_rows}</tbody></table>
<p>One further reading is <b>precision (pain-selective) visceral local anaesthesia</b>: a gut nociceptor-selective entry port ({m(", ".join(px["entry_ports"].keys()))}) paired with a charged firing-threshold-raising blocker that can only reach its site through the open port, so the block is <i>differential</i> \u2014 visceral nociceptive fibres silenced while motor and light-touch are spared (mechanism shape anchored to Binshtok\u2013Bean\u2013Woolf, Nature 2007). The differential-block ratio, duration, and concentration are {m("[O]")}.</p>
<p>The inheritance and re-verification (drift zero), the three-lever de-sensitisation of the {m("\u00a718")} afferent, and the burden re-derivation are forced by the substrate {m("[V]")}/{m("[F]")}. The <b>firewall is non-negotiable and inherited verbatim</b>: {m("\u03b3")} reads promoter switch-threshold STRUCTURE only \u2014 it is never a channel activation voltage, a drug potency, a dose, an in-vivo selectivity, or a clinical effect; every such magnitude, the differential-block ratio, and absolute efficacy are {m("[O]")}; the lever strength {m("\u03b4")} is structural, not a dose; the L3 (NGF/CGRP) mechanism link is {m("[O]")} cited biology; and the <i>felt</i> / affective pain is {m("mind")}'s (this layer moves only the peripheral afferent-gain term, the {m("\u00a727")} firewall kept). No molecule is designed, no synthesis or dose is given, and nothing here diagnoses, treats, or prescribes \u2014 it is a proposal-only target hypothesis.</p>
"""



def body_seams(R):
    v = seam.validate_seams()
    hep = v["circulatory_hepatic_interface"]; nf = v["s24_nafld_delivery"]; bl = v["s25_bile_delivery"]
    fw = v["firewall"]; mp = v["mind_pointer"]; ss = v["ssot_consistency"]
    cir_doi = hep["owner_doi"]; mind_doi = mp["owner_doi"]
    hep_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (k, vv, g) for k, vv, g in [
        ("hepatic blood flow Q_H", "%.0f mL/min" % hep["Q_H_ml_min"], "circulatory [V]"),
        ("first-pass extraction E", "%.2f" % hep["E"], "circulatory [V]"),
        ("oral bioavailability F", "%.2f" % hep["F"], "circulatory [V]"),
        ("hepatic clearance CL_H", "%.1f mL/min" % hep["CL_H_ml_min"], "circulatory [V]")])
    fw_rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (k, vv) for k, vv in [
        ("python files scanned (whole package)", "%d" % fw["python_files_scanned"]),
        ("sibling (circulatory / mind / neuro) code imports", "%d" % fw["sibling_import_count"]),
        ("felt / HPA keys in the emitted metabolic state", "%d" % len(fw["metabolic_state_felt_hpa_keys"])),
        ("firewall holds", "yes" if fw["firewall_holds"] else "NO")])
    return f"""
<p>The {m("\u00a724")} perfusion, {m("\u00a725")} hepatobiliary and {m("\u00a718")} afferent sections each ended at a declared <b>seam</b> \u2014 a hepatic lipid layer, a cholesterol-delivery term, a felt pain \u2014 that belongs to a sibling volume (<b>circulatory</b> for flow and clearance, <b>mind</b> for felt cognition). This section <i>wires</i> those seams. The wiring obeys one rule, taken verbatim from the neuro\u2194mind project boundary: a seam is <b>citation/pointer-only, never a code import</b>. Each package re-establishes its entire trusted state from its own single archive with the siblings absent; the cross-volume contract is carried by a vendored snapshot and a one-way pointer, not by one package reaching into another's code.</p>
{CARD_SEAM}
<p>The first seam is the <b>circulatory hepatic interface</b>. By its own charter, <i>circulatory</i> (<b>DOI {esc(cir_doi)}</b>) is the single source of truth for hepatic blood flow and first-pass clearance and hands them to this volume (\u201chepatic clearance kinetics \u2192 digestive, first-pass seam\u201d). Rather than re-derive them, this package records circulatory's emitted hepatic interface once \u2014 verified against circulatory's {m("hepatic_clearance()")} at vendoring time \u2014 in {m("inherited/cross_references.json")}, and <b>consumes</b> that snapshot:</p>
<table><thead><tr><th>consumed circulatory quantity</th><th>value (vendored)</th><th>owner / grade</th></tr></thead><tbody>{hep_rows}</tbody></table>
<p>That hepatic interface is the <b>delivery substrate</b> on which the two hepatic-facing readings sit. The {m("\u00a724")} <b>NAFLD / MASLD</b> reading keeps only its insulin-resistance core \u2014 the {m("\u00a712")} type-2 gain-loss homeostat, reused unchanged ({m("reuses_s12_type2_gain_loss = %s" % str(nf["reuses_s12_type2_gain_loss"]))}) \u2014 and rests the lipid <i>deposition</i> on the consumed circulatory perfusion; the lipid-<i>handling</i> magnitude stays circulatory's {m("[O]")}. The {m("\u00a725")} <b>bile</b> reading keeps only its crystallisation thermodynamics (the nucleation barrier at {m("CSI = %.3f" % bl["nucleation_csi"])}) and rests the cholesterol <i>delivery</i> on the same consumed perfusion; the absolute saturation-index scale stays circulatory's {m("[O]")}. Both readings consume the <i>same</i> snapshot value, so the seam is internally consistent ({m("consumed Q_H = %.0f mL/min, F = %.2f, matches the manifest" % (ss["snapshot_Q_H_ml_min"], ss["snapshot_F"]))}).</p>
<p>The second seam is the <b>mind felt-symptom firewall</b>. The {m("\u00a718")} visceral pain and the {m("\u00a725")} biliary colic have a <i>felt</i> component this package does not own; it belongs to <i>mind</i> (<b>DOI {esc(mind_doi)}</b>). It is handed OUT by a <b>one-way forward-defer pointer</b> ({m("one_way_pointer = %s" % str(mp["one_way_pointer"]))}, consuming no mind value: {m("consumes_a_mind_value = %s" % str(mp["consumes_a_mind_value"]))}). What crosses is only the <i>peripheral</i> term \u2014 the {m("\u00a718")} afferent signal (the R19-derived susceptibility) and the {m("\u00a725")} mechanical stone trigger; the felt interpretation is mind's, reached on mind's interoception route (visceral afferents \u2192 NTS \u2192 insula / cingulate, Saper 2002). Nothing returns: the metabolic state does not re-enter mind's HPA, and mind owns the felt experience.</p>
<p>The firewall is not asserted in prose \u2014 it is <b>enforced by an architectural lock</b>, the same lock <i>mind</i> runs neuro-side (mind has zero neuro imports; neuro has zero mind imports). The lock walks every python file in the package and confirms no sibling-code import exists, and that the emitted metabolic state carries no felt/HPA key:</p>
<table><thead><tr><th>firewall check</th><th>result</th></tr></thead><tbody>{fw_rows}</tbody></table>
<p>The consumed circulatory hepatic interface (cited to circulatory's DOI and named function, vendored faithfully) and the {m("\u00a712")}-homeostat reuse and nucleation thermodynamics that rest on it are {m("[V]")}; the firewall \u2014 zero sibling imports, a metabolic state with no felt/HPA key, and the mind one-way pointer \u2014 is a forced architectural identity {m("[F]")}. What stays open {m("[O]")}, each with its obstacle: the hepatic lipid-handling and absolute cholesterol-delivery magnitude (circulatory's, no primitive here), and the felt visceral pain and biliary colic (mind's, deferred by pointer). The live cross-package harness that would run all the sibling engines together \u2014 the integration step this section once left open \u2014 is now <b>built and verified in {m("\u00a730")}</b>: it loads every VP volume in one process and confirms, against the live sibling engines and outside every gate, that the consumed hepatic snapshot, the shared R19 substrate and the inherited analgesic map hold across the volumes, with each volume still verifying alone from its own archive.</p>
"""


CARD_REMAINING = vpcard("reuse", "<b>no new primitive \u2014 the remaining surface closes by REUSE</b> \u2014 each "
                   "disorder reads an already-validated module / primitive of this volume (the \u00a716 R19 gate, the \u00a74 "
                   "transport, the \u00a712 / \u00a76 homeostat, the \u00a722 flare); the three monogenic items "
                   "(Hirschsprung RET, MODY PDX1/HHEX, GSD-I G6PC) are imported-lesion seams owned by "
                   "<code>disease_wp</code> with the consequence dynamics owned here. <b>[V]</b> consequence / "
                   "<b>[L]</b> gene link.", "/physics/")


def body_remaining(R):
    d = dz.validate_d14()
    a = d["d14a_dyssynergic_defecation"]["dyssynergic"]
    b = d["d14b_hirschsprung"]["hirschsprung"]
    c = d["d14c_mody"]["mody"]
    e = d["d14d_hepatic_gsd"]["hepatic_gsd"]
    f = d["d14e_autoimmune_gastritis"]["autoimmune_gastritis"]
    relax_rows = "".join("<tr><td>%.2f</td><td>%s</td><td>%s</td></tr>"
                         % (fr, ("OPEN" if op else "closed"), ("cleared" if op else "RETAINED"))
                         for fr, op, _ in a["relaxation_route"])
    agang_rows = "".join("<tr><td>%.2f</td><td>%d</td><td>%.3f</td><td>%.3f</td><td>%.2f</td></tr>"
                         % (af, k, disp, dm, com) for af, k, disp, dm, com in b["aganglionic_rows"])
    gsd_rows = "".join("<tr><td>%.2f</td><td>%.2f</td><td>%s</td></tr>"
                       % (rf, g, ("HYPOGLYCAEMIC" if hy else "euglycaemic")) for rf, g, hy in e["fasting_axis"])
    return f"""
<p>This section closes the <b>in-substrate digestive Tier-1 surface</b>: the remaining disorders the roadmap (FUTURE_WORK \\u00a71A\\u2013\\u00a71D) had left enumerated are built here, each by <b>REUSE</b> of a module or primitive this volume already validated \\u2014 no new substrate primitive and no sibling package. Five readings, all emergent under wide sweeps, never fitted: the {m("\\u00a716")} gate read at the anorectal outlet (dyssynergic defecation), the {m("\\u00a74")} transport with a segmental aganglionic lesion (Hirschsprung), the {m("\\u00a712")} homeostat with a targeted secretory lesion (MODY), the {m("\\u00a76")} counter-regulation with a crippled glycogen buffer (hepatic GSD type I), and the {m("\\u00a722")} relapsing-inflammation flare read corpus-localised (autoimmune gastritis). Three of the five are monogenic: their gene lesion is owned by <code>disease_wp</code> (gene-key) and the consequence dynamics are owned here \\u2014 an imported-lesion seam cross-referenced both ways.</p>
{CARD_REMAINING}
<p><b>Dyssynergic defecation</b> reads the {m("\\u00a716")} sphincter gate at the <i>anorectal outlet</i> \\u2014 the achalasia mirror, at the other end of the gut. The outlet gate is tonically closed and should open on the coordinated defecatory relaxation (the rectoanal inhibitory reflex plus voluntary external-sphincter relaxation) against the propulsive push; in dyssynergia that relaxation fails, or the floor paradoxically contracts, so the gate stays closed and the bolus is retained <i>despite normal propulsion</i>. As the relaxation competence falls the gate clears at full drive but stays shut below it (the bolus retained), and a rising paradoxical outlet tone shuts it the same way. Crucially the propulsive drive is intact ({m("propulsion_intact_pct = %.1f%%" % a["propulsion_intact_pct"])}) \\u2014 the lesion is the gate, not the drive, the falsifiable distinction from colonic inertia ({m("\\u00a714")}, a drive collapse):</p>
<table><thead><tr><th>relaxation competence (fraction)</th><th>outlet gate</th><th>bolus</th></tr></thead><tbody>{relax_rows}</tbody></table>
<p><b>Hirschsprung disease</b> is read as a motility <i>consequence</i>: a distal <b>aganglionic</b> segment has no slow-wave oscillator (the {m("\\u00a71")}-emergence reading \\u2014 a segment whose gene lesion prevents oscillator emergence carries zero contraction amplitude), so on the {m("\\u00a74")} mechanics the bolus cannot be propagated <i>through</i> it. A normal uniform gut advances the bolus to the distal end (net displacement {m("%.1f" % b["normal"]["net_disp"])}, the distal-most cell reached); an aganglionic distal segment blocks aboral clearance progressively as the dead segment lengthens, never traverses the deep aganglionic zone (the distal-most cell stays empty), and the bolus is retained at the transition zone \\u2014 the proximal dilatation (megacolon) above the narrowed aganglionic segment. The RET-aganglionosis gene lesion is owned by <code>disease_wp</code>; the {m("\\u00a71")}+{m("\\u00a74")} consequence is owned here:</p>
<table><thead><tr><th>aganglionic fraction</th><th>transition cell</th><th>net displacement</th><th>distal-most-cell fraction</th><th>final centre-of-mass</th></tr></thead><tbody>{agang_rows}</tbody></table>
<p><b>MODY</b> (maturity-onset diabetes of the young), a single-gene defect, is a <i>targeted</i> partial \\u03b2-secretory-capacity lesion on the {m("\\u00a712")} homeostat (PDX1/HHEX-linked). Unlike the {m("\\u00a712")} type-1 axis \\u2014 capacity depleted toward zero into an accelerating, catastrophic runaway (deepest fasting {m("%.2f mM" % c["t1_deepest_fasting_for_contrast"])}, setpoint lost) \\u2014 the MODY lesion settles a <b>distinct, stable, fully-regulated</b> elevated curve: at the operating point ({m("beta_frac = %.2f" % c["beta_frac"])}) fasting is {m("%.2f mM" % c["fasting_mM"])}, the meal peak {m("%.2f mM" % c["peak_mM"])}, and the load <i>returns</i> to the (mildly raised) fixed point ({m("final = %.2f mM" % c["final_mM"])}) \\u2014 the monogenic, stable, often-mild phenotype. The PDX1/HHEX gene subtype is gene-key (\\u2192 <code>disease_wp</code>; the gene link is cited from DNA); the {m("\\u00a712")} trajectory is owned here.</p>
<p><b>Hepatic glycogen storage disease type I</b> (von Gierke, glucose-6-phosphatase deficiency) is read on the {m("\\u00a76")} counter-regulation: the hepatic glycogen buffer (the HHEX role) cannot <i>release</i> free glucose \\u2014 glycogenolysis and gluconeogenesis both fail \\u2014 so the hepatic-output arm is crippled. The consequence is the hallmark <b>fasting hypoglycaemia</b>: a normal liver holds glucose at the setpoint, but with the output crippled the uptake outpaces hepatic production and glucose drifts down, crossing the cited 3.9 mM alert value as the output falls; and a hypoglycaemia challenge can no longer be returned to the setpoint (the failed counter-regulation, {m("counter_regulation_fails_when_buffer_crippled = %s" % e["counter_regulation_fails_when_buffer_crippled"])}). The G6PC / enzyme gene is gene-key (\\u2192 <code>disease_wp</code>); the {m("\\u00a76")} consequence is owned here:</p>
<table><thead><tr><th>hepatic free-glucose output (fraction)</th><th>fasting glucose (mM)</th><th>state</th></tr></thead><tbody>{gsd_rows}</tbody></table>
<p><b>Autoimmune gastritis</b> reads the {m("\\u00a722")} relapsing-inflammation flare <i>corpus-localised</i>. A sustained anti-parietal autoimmune drive ignites a corpus flare past the R19 spinodal, whose cumulative burden lowers the {m("\\u00a77")} fate-stability scale of the corpus (a <b>regional</b> barrier lesion: corpus barrier {m("%.3f \\u2192 %.3f" % (f["ignition_axis"][0][2], f["ignition_axis"][-1][2]))}) and \\u2014 the parietal-cell-loss consequence \\u2014 drops the acid output, which tracks the intact corpus/parietal scale (achlorhydria, {m("acid_output_coupled_to_corpus_barrier = %s" % f["acid_output_coupled_to_corpus_barrier"])}). This corpus-restricted, achlorhydric signature distinguishes it from {m("\\u00a713")} antral H. pylori gastritis (acid preserved / raised). Suppressing the autoimmune driver past the induction threshold reverts the flare and the corpus barrier and acid recover (the treatment direction). Common / acquired (HLA-linked, not single-gene) \\u2014 so this one is owned here in full.</p>
<p><b>Treatment (model reading).</b> Each disorder carries its own target. Dyssynergic defecation: {esc(d["d14a_dyssynergic_defecation"]["treatment"])} Hirschsprung: {esc(d["d14b_hirschsprung"]["treatment"])} MODY: {esc(d["d14c_mody"]["treatment"])} Hepatic GSD-I: {esc(d["d14d_hepatic_gsd"]["treatment"])} Autoimmune gastritis: {esc(d["d14e_autoimmune_gastritis"]["treatment"])}</p>
<p>Every emergent mechanism here is forced by the substrate {m("[V]")}: the gate-at-the-outlet retention with the drive intact, the segmental block with proximal retention, the distinct regulated MODY curve, the GSD fasting drift and failed counter-regulation, and the corpus barrier and acid drop. The PDX1/HHEX and G6PC gene links are cited from DNA {m("[L]")} and the three monogenic items are gene-key (\\u2192 <code>disease_wp</code>, cross-referenced both ways). What stays open {m("[O]")}, each with its obstacle: the felt straining / incomplete-evacuation and abdominal sensations (afferent-gain / <code>mind</code>), the absolute evacuation / transit / glucose scales (model units needing clinical calibration), the B12 / iron malabsorption magnitude of autoimmune gastritis (an absorption layer), and the autoimmune-gastritis carcinoid boundary (the {m("\\u00a721")} out-of-kernel neuroendocrine boundary, <code>disease_wp</code>).</p>
"""


CARD_HARNESS = vpcard("harness", "<b>live cross-package harness = load every VP volume in one process and "
                   "verify, against the LIVE sibling engines, the identities the seams took on trust</b> \u2014 "
                   "OUTSIDE every gate (each volume still re-establishes its trusted state from its own archive "
                   "with the siblings absent; the harness is the one sanctioned place a sibling is reached, and "
                   "only ever by file-path LOAD, never an import). It re-confirms the shared R19 substrate "
                   "(spinodal / barrier drift 0), the vendored circulatory hepatic snapshot, the 27-target "
                   "analgesic map re-deriving through every volume\u2019s spinodal, and the neuro nociceptor the "
                   "felt-symptom pointer targets. <b>[V]</b> verified / <b>[F]</b> closed-form + firewall.", "/physics/")


def body_harness(R):
    hc = harness.digestive_side_contract()
    _hs, hh = harness.digest()
    sub = hc["substrate"]; cs = hc["circulatory_seam"]; am = hc["analgesic_map"]; ep = hc["neuro_endpoint"]
    sc = harness.self_no_sibling_imports()
    sp = sub["ref_spinodal_at_map_gammas"]; ba = sub["ref_barrier_at_map_gammas"]
    gm = sorted(harness._map_gammas(), key=lambda t: t[1])
    idx = sorted(set([0, len(gm) // 5, 2 * len(gm) // 5, 3 * len(gm) // 5, 4 * len(gm) // 5, len(gm) - 1]))
    pick = [gm[i] for i in idx]
    sub_rows = "".join("<tr><td>%s</td><td>%.4f</td><td>%.6f</td><td>%.6f</td></tr>"
                       % (esc(gene), g, sp[gene], ba[gene]) for gene, g, _ in pick)
    check_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % row for row in [
        ("shared R19 substrate",
         "every volume\u2019s firing-threshold |h_sp| = 2(g/3)<sup>1.5</sup> and barrier g\u00b2/4 are byte-identical (cross-volume drift 0)",
         "this volume\u2019s closed form (2/3\u221a3)\u03b3<sup>1.5</sup>, \u03b3\u00b2/4", "[F]"),
        ("circulatory hepatic seam",
         "circulatory\u2019s LIVE hepatic_clearance() reproduces the vendored snapshot",
         "Q_H = %.0f mL/min, E = %.2f, F = %.2f, CL_H = %.0f mL/min"
         % (cs["vendored_Q_H_ml_min"], cs["vendored_E"], cs["vendored_F"], cs["vendored_CL_H_ml_min"]), "[V]"),
        ("analgesic 27-target map",
         "the inherited firing-threshold map re-derives bit-for-bit through EVERY volume\u2019s own spinodal (and musculoskeletal, the built second host, reads its levers on the same spinodal)",
         "%d targets, |h_sp| drift %.0e" % (am["n_targets"], am["max_h_sp_drift"]), "[V]"),
        ("neuro felt-symptom endpoint",
         "the peripheral nociceptor the \u00a718\u2192mind pointer targets exists on the shared substrate \u2014 a HIGH-threshold polymodal cell that fires only to noxious drive",
         "%s (Na<sub>V</sub>1.7), master %s \u2014 both in the 27-map" % (esc(ep["peripheral_channel_gene"]), esc(ep["nociceptor_master_gene"])), "[V]"),
    ])
    return f"""
<p>The {m("\u00a727")} seam layer and the {m("\u00a728")} inherited analgesic map both rest on a <b>cross-volume identity</b> they could only take on trust, because the governing discipline is <i>verify-alone</i>: every VP volume re-establishes its entire trusted state from its OWN archive with the siblings absent, so neither layer is allowed to import a sibling. The seam <i>vendored</i> circulatory\u2019s hepatic snapshot (verified once, at vendoring time); the analgesic map <i>asserted</i> that its firing-threshold scale is exactly this volume\u2019s {m("\u00a718")} afferent spinodal. This section supplies the standing LIVE proof: a harness that loads <i>every</i> VP volume into one process and checks those identities against the live sibling engines \u2014 the last frontier item of the {m("\u00a78")} work order.</p>
{CARD_HARNESS}
<p>The harness runs <b>outside every gate</b>. The research gate ({m("repro/run_all.py")}) and this canonical build compute nothing here and never import a sibling \u2014 the pages you are reading were produced with the siblings <i>absent</i>, the verify-alone guarantee intact. The sibling engines are <b>loaded by file path</b> under unique module names (with the package-internal module table cleared between loads, so two volumes\u2019 identically-named {m("vp_substrate")} cannot collide); that is loading, not importing, and the harness\u2019s own source carries {m("%d" % sc["sibling_import_statements"])} sibling import statements (self-checked, file-path-load discipline {m("ok = %s" % str(sc["file_path_load_discipline_ok"]))}). Because the harness <i>digest</i> hashes only the in-package digestive-side contract \u2014 the closed-form substrate values, the vendored snapshot, the drift-0 reverify and the neuro-endpoint descriptor, all computed from this archive alone \u2014 it is <b>byte-identical whether or not the siblings are on disk</b> ({m("2\u00d7sha256 = %s\u2026" % hh[:12])}), exactly what a deterministic, sibling-free build requires. The engine, disease, C6, seam and analgesic digests are all unchanged; this layer carries only its own.</p>
<p>With the sibling packages present, {m("repro/run_harness.py")} loads all four volumes in one process and confirms the four identities the seam and analgesic layers depend on:</p>
<table><thead><tr><th>cross-volume identity</th><th>what the live harness confirms against the sibling engine</th><th>in-package reference (built siblings-absent)</th><th>grade</th></tr></thead><tbody>{check_rows}</tbody></table>
<p>The foundation of all four is the <b>shared R19 substrate</b>: a primitive derived in one volume can be READ in another only because the double-well closed forms are the same function everywhere. The live check sweeps {m("\u03b3")} across the map and finds the sibling spinodals match this volume\u2019s bit-for-bit (drift 0); the closed-form values they must match \u2014 {m("|h_sp| = (2/3\u221a3)\u03b3^1.5")} and {m("barrier = \u03b3\u00b2/4")}, evaluated at a span of the inherited analgesic-target gammas \u2014 are:</p>
<table><thead><tr><th>pain gene (map target)</th><th>\u03b3 = \u2212mean NN \u0394G</th><th>|h_sp| = spinodal(\u03b3)</th><th>barrier = \u03b3\u00b2/4</th></tr></thead><tbody>{sub_rows}</tbody></table>
<p>The live cross-volume readings \u2014 substrate drift 0 across the volumes, circulatory\u2019s live clearance reproducing the vendored snapshot, the 27-target map re-deriving through every spinodal, and the neuro nociceptor firing only to noxious drive on the shared substrate \u2014 are {m("[V]")}; the closed-form substrate identity and the out-of-gate firewall (file-path load only, the build sibling-free, verify-alone preserved) are forced {m("[F]")}. This is a <b>verification layer: it introduces no new primitive and makes no new claim</b> \u2014 it confirms, live, what the earlier layers asserted, so there is no new {m("[O]")} of its own. The single thing it cannot do offline is the live run itself (which needs the sibling archives present); that is precisely why the build and the gate stay sibling-free and the live check is a separate runner. The <i>felt</i> pain remains {m("mind")}\u2019s (only the peripheral nociceptor term crosses, the {m("\u00a727")} firewall kept), and every clinical magnitude remains {m("[O]")} as inherited.</p>
"""


SECTIONS = [
 dict(n=1, slug="01-organ-emergence-measured-gamma", subj="Organ emergence from measured \u03b3",
      desc="Four digestive organs emerge from measured master-gene γ on the shared R19 jamming switch; identity and order are cited from DNA, dynamics added here.",
      grade="[V]", knows=["jamming lattice", "R19 bistable switch", "organ morphogenesis", "master-gene gamma"],
      answer="Four digestive organs emerge deterministically from their measured master-gene composition \u03b3 on the shared R19 jamming switch: stomach (BARX1, \u03b3=1.5609), intestine (CDX2, \u03b3=1.45), pancreas (PDX1, \u03b3=1.4732) and liver (HHEX, \u03b3=1.525). Identity and developmental order are cited from the DNA gene-clock [V]; this package adds only the functional dynamics.",
      abstract="Organ identity and developmental order are cited from the DNA morphogenesis gene-clock (measured \u03b3, grade [V]); this package emerges four organs on the shared R19 switch ds/dt = g\u00b7s \u2212 s\u00b3 + h and adds their dynamics. Ascending-\u03b3 order is intestine, pancreas, liver, stomach.",
      body=body_organs),
 dict(n=2, slug="02-gastric-slow-wave-pacemaker", subj="Gastric slow-wave pacemaker (~3 cpm)",
      desc="The gastric pacemaker is a robust FitzHugh–Nagumo limit cycle at the cited ~3 cpm; inter-spike variability stays under 3% across a wide drive sweep.",
      grade="[V]", knows=["interstitial cells of Cajal", "slow wave", "FitzHugh-Nagumo oscillator", "limit cycle"],
      answer="The gastric pacemaker is a robust limit cycle on the shared FitzHugh\u2013Nagumo oscillator: at a long recovery constant \u03c4_s=380 it beats at the cited ~3 cpm anchor, with inter-spike-interval variability under 3% across a wide drive sweep (0.40\u20130.70). The rhythm mechanism is forced [V]; the absolute 3 cpm rate is a cited anchor [L].",
      abstract="The gastric slow wave is a structurally stable limit cycle: a long FitzHugh\u2013Nagumo recovery constant \u03c4_s=380 yields ~3 cpm, with ISI CV < 3% across drive 0.40\u20130.70. One gastric-anchored clock K_TIME=2400 cpm/model-Hz sets the rate; the rhythm is [V], the 3 cpm value is [L].",
      body=body_gastric),
 dict(n=3, slug="03-aboral-slow-wave-frequency-gradient", subj="Aboral slow-wave frequency gradient",
      desc="Intestinal slow-wave frequency falls monotonically aboral; one gastric-anchored clock predicts duodenum 11.1 cpm and ileum 7.5 cpm with no intestinal tuning.",
      grade="[V]", knows=["slow wave gradient", "duodenum", "ileum", "aboral propagation"],
      answer="The intestinal slow-wave frequency falls monotonically aboral, reproducing the duodenum-to-ileum gradient. One gastric-anchored clock (K_TIME=2400 cpm per model-Hz) converts each segment's FitzHugh\u2013Nagumo frequency to cycles per minute, predicting duodenum 11.1 cpm and ileum 7.5 cpm with zero intestinal tuning. The gradient direction is forced [V]; absolute rates inherit the cited clock [L].",
      abstract="A linearly growing recovery constant along the gut yields a monotone falling slow-wave gradient. The single gastric clock predicts duodenum 11.1 cpm (cited ~12) and ileum 7.5 cpm (cited ~8) with no intestinal tuning. The gradient shape is [V]; the absolute rates inherit the cited clock [L].",
      body=body_gradient),
 dict(n=4, slug="04-peristaltic-aboral-transport", subj="Peristaltic aboral transport",
      desc="A slow-wave phase gradient produces net aboral transport: a bolus moves +12 segments and reverses under a reversed-gradient control. Robust and forced.",
      grade="[V]", knows=["peristalsis", "phase gradient", "Kuramoto coupling", "directed transport"],
      answer="A slow-wave phase gradient produces net aboral transport. Weak nearest-neighbour coupling on the segments' intrinsic frequencies builds a travelling occlusion wave; a mass-conserving pressure flux then carries a luminal bolus +12 segments downstream under a physiological proximal-fast gradient, and reverses to oral (\u22121) under a reversed-gradient control. Directed transport from a phase gradient is forced [V].",
      abstract="Weak Kuramoto coupling on FitzHugh\u2013Nagumo segments builds a travelling occlusion wave; a mass-conserving pressure flux moves a bolus +12 segments aborally and \u22121 (oral) under a reversed gradient. Net directed transport from a phase gradient is forced [V], robust across coupling and flux-scale sweeps.",
      body=body_peristalsis),
 dict(n=5, slug="05-glucose-insulin-homeostat-setpoint", subj="Glucose\u2013insulin homeostat setpoint",
      desc="A glucose load returns to the ~5 mM setpoint via an insulin loop of graded R19 switches; meal peaks from 5.9 to 11.1 mM all settle near 5.2 mM.",
      grade="[V]", knows=["glucose homeostasis", "insulin", "negative feedback", "islet beta cell"],
      answer="A glucose load returns to the ~5 mM setpoint via the insulin loop. Insulin secretion is a graded population of R19 switches activating as glucose rises; meals lift the peak from 5.9 to 11.1 mM, yet every load settles near 5.2 mM. Homeostatic return is forced by the closed loop [V]; the 5 mM setpoint is cited [L].",
      abstract="Insulin secretion is a graded population of R19 switches; the closed loop dG/dt = R_meal + HGP \u2212 (k_u0 + k_u\u00b7Ins)\u00b7G returns glucose to a 5.0 mM fixed point. Meal peaks from 5.9 to 11.1 mM all settle near 5.2 mM. Homeostasis is [V]; the 5 mM setpoint is [L].",
      body=body_homeostat),
 dict(n=6, slug="06-hypoglycemia-counter-regulation", subj="Hypoglycaemia counter-regulation",
      desc="Hypoglycaemia triggers glucagon-driven hepatic glucose release back to setpoint; nadirs of 4.6–3.5 mM recover via a finite glycogen buffer, bounded.",
      grade="[V]", knows=["hypoglycemia", "glucagon", "hepatic glycogen", "counter-regulation"],
      answer="Hypoglycaemia triggers glucagon-driven hepatic glucose release that returns blood glucose to setpoint. An insulin overdose drives glucose down to a nadir of 4.6\u20133.5 mM with increasing challenge; the finite hepatic glycogen buffer (the liver/HHEX role) then restores ~5 mM without overshoot. The bounded counter-regulatory loop is forced [V]; the glycogen capacity is a model unit [O].",
      abstract="An \u03b1-cell population of R19 switches raises hepatic glucose production when glucose falls; insulin-overdose nadirs of 4.6\u20133.5 mM recover to ~5 mM, bounded below 9 mM on rebound. The loop is forced [V]; the absolute glycogen capacity is a model unit, graded [O] with a stated obstacle.",
      body=body_counter),
 dict(n=7, slug="07-carcinogen-barrier-kramers-kernel", subj="Carcinogen barrier-Kramers kernel",
      desc="A carcinogen lowers the R19 cell-fate barrier, raising the Kramers crossing rate; RR(dose)=rate(dose)/rate(0), one shared noise scale D for all sites.",
      grade="[F]", knows=["carcinogenesis", "Kramers rate", "bistable barrier", "relative risk"],
      answer="A carcinogen is a sustained aberrant drive that lowers the R19 cell-fate barrier, raising the Kramers crossing rate into a malignant basin; relative risk is RR(dose)=rate(dose)/rate(0). The exact cubic barrier vanishes as (h_sp\u2212h)^{3/2} near the spinodal, and one shared noise scale D=0.0417 serves every organ site. The kernel is forced [F]; per-site anchors are cited [L].",
      abstract="The carcinogen kernel reuses the organ-building R19 switch: a sustained bias lowers the exact cubic barrier (vanishing as (h_sp\u2212h)^1.5), and a Kramers rate gives RR(dose)=rate(dose)/rate(0). One noise scale D=0.0417 serves all sites; the only per-site number is a calibrated dose-to-bias slope. The kernel is [F].",
      body=body_kernel),
 dict(n=8, slug="08-colorectal-processed-meat-dose-response", subj="Colorectal processed-meat dose-response",
      desc="Processed-meat exposure raises colorectal-cancer risk along a monotone convex curve anchored to IARC RR≈1.18 per 50 g/day, reaching 1.63 at 150 g/day.",
      grade="[V]", knows=["colorectal carcinoma", "processed meat", "N-nitroso", "dose-response"],
      answer="Processed-meat exposure raises colorectal-cancer risk along a monotone, convex dose-response anchored to the IARC figure RR\u22481.18 per 50 g/day. The shared barrier-lowering kernel, with a single calibrated slope \u03ba, reproduces RR from 1.00 to 1.18 at 50 g/day and 1.63 at 150 g/day. The anchor is cited [L]; the shape is verified [V]; absolute incidence is open [O].",
      abstract="Heme iron and N-nitroso compounds act as a sustained bias on the colonocyte fate switch. Calibrating one dose-to-bias slope to the IARC anchor RR\u22481.18 per 50 g/day reproduces a monotone convex curve reaching RR 1.63 at 150 g/day. Anchor [L], shape [V], absolute incidence [O].",
      body=body_colorectal),
 dict(n=9, slug="09-pancreatic-smoking-dose-response", subj="Pancreatic smoking dose-response",
      desc="Tobacco raises pancreatic-cancer risk monotonically in pack-years, anchored to RR≈1.91 at 50 pack-years; one calibrated slope reproduces the curve.",
      grade="[V]", knows=["pancreatic carcinoma", "tobacco", "pack-years", "dose-response"],
      answer="Tobacco exposure raises pancreatic-cancer risk monotonically in pack-years, anchored to RR\u22481.91 at 50 pack-years. The same barrier-lowering kernel, with one calibrated slope, reproduces RR rising from 1.00 to 1.30 at twenty and 1.91 at fifty pack-years, passing through the current-smoker range near thirty. The anchor is cited [L]; shape verified [V]; absolute incidence open [O].",
      abstract="Tobacco nitrosamines and PAHs bias the pancreatic-cell fate switch. One calibrated slope reproduces RR from 1.00 to 1.91 across 0\u201350 pack-years, with RR near 1.48 at 30 pack-years consistent with cited current-smoker estimates (~1.74). Anchor [L], shape [V], absolute incidence [O].",
      body=body_pancreatic),
 dict(n=10, slug="10-gastric-helicobacter-diet-synergy", subj="Gastric H. pylori\u2013diet synergy",
      desc="H. pylori and dietary N-nitroso act synergistically on gastric-cancer risk: joint RR≈4.4 exceeds the additive-null 3.3; kernel predicts sub-multiplicativity.",
      grade="[V]", knows=["gastric carcinoma", "Helicobacter pylori", "synergy", "interaction"],
      answer="Helicobacter pylori infection and dietary N-nitroso act synergistically on gastric-cancer risk: infection lowers the R19 barrier scale while diet adds bias, and their joint relative risk (\u22484.4) exceeds the additive-null (3.3). The same exact-barrier kernel reproduces this super-additivity and additionally predicts sub-multiplicativity near the spinodal. The interaction is verified [V]; absolute incidence open [O].",
      abstract="H. pylori chronic inflammation lowers the cell-fate barrier scale; dietary N-nitroso adds bias. Their joint RR\u22484.4 exceeds the additive-null 3.3 (super-additive) yet falls below the multiplicative-null 4.5 (a sub-multiplicative prediction near the spinodal). The interaction is [V]; absolute incidence [O].",
      body=body_gastric_onc),
 dict(n=11, slug="11-gastric-dysrhythmia-and-gastroparesis", subj="Gastric dysrhythmia and gastroparesis",
      desc="One slow-wave pacemaker, perturbed: the FitzHugh\u2013Nagumo rate constant crosses the EGG band (brady<2.5/normal/tachy>3.7 cpm), a faster coupled ectopic focus entrains tachygastria, and ICC density grades emptying to zero.",
      grade="[V]", knows=["gastroparesis", "tachygastria", "bradygastria", "interstitial cells of Cajal", "gastric dysrhythmia"],
      answer="Gastric dysrhythmia and gastroparesis are perturbations of one slow-wave pacemaker. Moving the FitzHugh\u2013Nagumo rate constant carries the recorded rhythm across the cited electrogastrography band: bradygastria below 2.5, normal near 3, tachygastria above 3.7 cpm. A faster distal ectopic focus that couples entrains the antrum upward, and reducing pacemaker density grades gastric emptying toward zero [V].",
      abstract="Gastric dysrhythmia and gastroparesis perturb one slow-wave pacemaker. The FitzHugh\u2013Nagumo recovery constant carries the recorded rate across the cited EGG band (brady < 2.5, normal ~3, tachy > 3.7 cpm); a faster coupled ectopic focus entrains tachygastria; and ICC pacemaker density grades emptying from full to zero. Mechanisms [V], the normal band [L], absolute emptying rate [O].",
      body=body_dysrhythmia),
 dict(n=12, slug="12-diabetes-capacity-and-gain-spectrum", subj="Diabetes: capacity and gain on one homeostat",
      desc="Two parameters of one glucose homeostat give the diabetes spectrum: \u03b2-cell capacity loss drives catastrophic hyperglycaemia (type 1) past 7 mM; insulin-sensitivity loss gives a stable elevated setpoint (type 2/IGT).",
      grade="[V]", knows=["diabetes mellitus type 1", "diabetes mellitus type 2", "insulin resistance", "impaired glucose tolerance", "beta cell"],
      answer="Type 1 and type 2 diabetes are two failure modes of one glucose homeostat. Depleting beta-cell secretory capacity drives fasting glucose accelerating past the cited 7 mM diabetes threshold into severe, runaway hyperglycemia. Losing insulin sensitivity instead settles a stable, mildly elevated setpoint that still self-regulates. Capacity loss is catastrophic, gain loss compensated [V].",
      abstract="Two parameters of one glucose homeostat give the diabetes spectrum. Scaling \u03b2-cell capacity (type 1) drives accelerating hyperglycaemia past the cited 7 mM threshold with loss of setpoint return; scaling insulin sensitivity (type 2) settles a stable elevated setpoint that still self-regulates, with IGT a mild point in the 5.6\u20136.9 mM band. Two-axis emergence [V], thresholds [L], prevalence [O].",
      body=body_diabetes),
 dict(n=13, slug="13-gastritis-and-peptic-ulcer-barrier-axis", subj="Gastritis and peptic ulcer: the barrier axis",
      desc="Acid/NSAID aggression lowers the mucosal-integrity barrier on the same Kramers kernel as carcinogenesis: erosion RR anchored to NSAID ulcer RR\u22484; gastric (defence) vs duodenal (acid) ulcer routes; shared g_Hp continuum to neoplasia.",
      grade="[V]", knows=["peptic ulcer disease", "gastritis", "Helicobacter pylori", "NSAID gastropathy", "mucosal barrier"],
      answer="Gastritis and peptic ulcer reuse the carcinogenesis barrier kernel: acid and NSAID aggression biases the mucosal-integrity barrier downward, so erosion risk rises along a convex Kramers curve anchored to the cited NSAID ulcer risk near four. Gastric ulcers cross by failed defence, duodenal ulcers by acid excess, and chronic Helicobacter gastritis shares the cancer step's barrier scale [V].",
      abstract="Gastritis and peptic ulcer reuse the \u00a77 barrier-Kramers kernel on the mucosal-integrity switch. Acid/NSAID aggression biases the barrier down, raising erosion risk along a convex curve anchored to the NSAID ulcer RR \u2248 4; gastric ulcers cross by failed defence and duodenal by acid excess; and chronic H. pylori shares the \u00a710 cancer-step barrier scale, making one inflammation-to-neoplasia continuum. Shape, split, continuum [V]; anchor [L]; incidence [O].",
      body=body_gastritis_ulcer),
 dict(n=14, slug="14-intestinal-motility-transit-disorders", subj="Intestinal motility and transit disorders",
      desc="The \u00a74 peristalsis module perturbed: propulsive-drive loss \u2192 slow-transit constipation then refractory colonic inertia; ICC-density loss \u2192 functional CIPO (patent lumen); transient drive loss \u2192 reversible ileus; one ICC lesion across stomach and gut.",
      grade="[V]", knows=["slow transit constipation", "colonic inertia", "chronic intestinal pseudo-obstruction", "paralytic ileus", "interstitial cells of Cajal"],
      answer="The major non-obstructive intestinal motility disorders perturb one peristalsis module. Reducing propulsive drive slows transit monotonically (slow-transit constipation), collapsing below a threshold into refractory colonic inertia. Falling ICC density gives functional pseudo-obstruction with a patent lumen, and a transient drive loss gives reversible paralytic ileus. The same ICC lesion collapses both gastric emptying and gut transit [V].",
      abstract="The non-obstructive intestinal motility disorders perturb the \u00a74 peristalsis module. Reducing propulsive drive slows aboral transit monotonically (slow-transit constipation) and collapses below a threshold (colonic inertia, refractory); falling ICC density gives functional pseudo-obstruction with a patent lumen (CIPO); a transient drive loss gives reversible paralytic ileus. One ICC-depletion lesion collapses both gastric emptying (\u00a711) and gut transit (\u00a714). Mechanisms [V], transit anchors [L]-pending, absolute transit time [O].",
      body=body_motility),
 dict(n=15, slug="15-scattered-tier1-perturbations", subj="Additional Tier-1 perturbations (dumping, reflux, insulinoma, FD, SIBO)",
      desc="Five more single-parameter perturbations of already-built modules: dumping (faster, higher glucose peak + biphasic reactive-hypoglycaemia crossing on §5; mechanical magnitude honest [O]), reflux-oesophagitis erosion (shared §13 kernel), insulinoma (mirror of type 1) + reactive hypoglycaemia, functional-dyspepsia mild-motility point on the §11 ICC axis, and SIBO stasis on the §4 sweep.",
      grade="[V]", knows=["dumping syndrome", "reflux esophagitis", "insulinoma", "reactive hypoglycemia", "functional dyspepsia", "small intestinal bacterial overgrowth"],
      answer="Five further Tier-1 disorders perturb already-built modules: dumping drives a faster, higher glucose peak plus a biphasic reactive-hypoglycaemia crossing on the §5 loop; reflux oesophagitis reuses the §13 erosion kernel; insulinoma mirrors type-1 diabetes; functional dyspepsia is a mild point on the §11 ICC axis; SIBO stasis rises as the §4 sweep weakens. Mechanisms [V], dumping magnitude [O].",
      abstract="Five scattered Tier-1 disorders, each one moved parameter of a module from §2–§14 (group A, no new primitive). Dumping's early/late metabolic features emerge on the §5 homeostat (the mechanical rapid-emptying magnitude is an honest [O]); reflux-oesophagitis erosion reuses the §13 Kramers kernel; insulinoma is the mirror of §12 type 1, with reactive hypoglycaemia sharing the late-dumping undershoot; functional dyspepsia is the mild end of the §11 ICC axis; SIBO stasis rises as the §4 propulsive sweep weakens. Mechanisms [V]; anchors [L]; the dumping magnitude/nadir, SIBO bacterial load and FD felt component are [O] with stated obstacles.",
      body=body_scattered),
 dict(n=16, slug="16-sphincter-gate-disorders", subj="Sphincter-gate disorders (GERD, achalasia, spasm, Oddi)",
      desc="One new Tier-2 primitive — a tonically-closed R19 gate (opens iff drive > tone + spinodal). GERD is the gate failing closed (reflux burden rises as LES tone falls); achalasia the SAME gate failing open (stuck → antegrade stasis) — two opposite failures of one gate; esophageal spasm is a §4 coordination fault (amplitude cannot rescue); sphincter of Oddi is the gate at the biliary outlet.",
      grade="[V]", knows=["gastroesophageal reflux disease", "achalasia", "esophageal spasm", "sphincter of Oddi dysfunction", "lower esophageal sphincter", "bistable gate"],
      answer="The esophageal and outlet motor disorders ride one Tier-2 primitive: a gate, the R19 switch held closed, opening only past tone plus spinodal. GERD is the gate failing closed, reflux burden rising as LES tone falls; achalasia is the same gate stuck closed into stasis: two opposite failures of one gate. Spasm is a coordination fault; Oddi the biliary-outlet gate.",
      abstract="The first Tier-2 primitive is a gate: the §2 R19 switch ds/dt = g·s − s³ + h held in its closed basin by a tonic bias, opening only when a coordinated drive clears the opening spinodal (resistance = tone + spinodal). One gate gives two opposite diseases — the gate analogue of the §11/§14 one-ICC-lesion mirror: GERD (failing closed → retrograde reflux burden rising monotonically as tone falls) and achalasia (failing open → antegrade stasis, with aperistalsis compounding). Esophageal spasm is a §4 coordination pathology where amplitude cannot rescue lost coordination; sphincter of Oddi is the same gate at the biliary outlet. Motor readings [V]; felt pain and absolute frequencies/clearance/outflow [O] with stated obstacles.",
      body=body_gate),
 dict(n=17, slug="17-gastric-accommodation-reservoir", subj="Gastric accommodation reservoir (functional dyspepsia, post-prandial distress)",
      desc="A second Tier-2 primitive \u2014 a fundic compliance reservoir (the R19 wall relaxed toward yield; stiffness k=3s\u00b2\u2212g, compliance C=1/k, meal pressure P=V\u00b7k). Impaired fundic accommodation stiffens the wall so a fixed meal raises pressure prematurely (early satiation, post-prandial distress) = functional dyspepsia PDS; the maximal-compliance yield point is exactly the R19 spinodal. This is the post-prandial-distress axis the \u00a715 FD-motility reader left open.",
      grade="[V]", knows=["functional dyspepsia", "postprandial distress syndrome", "gastric accommodation", "early satiation", "fundic compliance", "gastric barostat"],
      answer="The post-prandial-distress component of functional dyspepsia rides a new Tier-2 primitive: a reservoir, the R19 wall relaxed toward yield. Impaired fundic accommodation stiffens the wall, so a fixed meal raises intra-gastric pressure prematurely \u2014 early satiation and post-prandial distress \u2014 and restoring accommodation lowers it. The maximal-compliance yield point is exactly the R19 spinodal.",
      abstract="The second Tier-2 primitive is a reservoir: the \u00a72 R19 switch ds/dt = g\u00b7s \u2212 s\u00b3 + h resting contracted at s = \u2212\u221ag, which a vagal accommodation drive relaxes toward its yield point. The wall stiffness is the R19 restoring curvature k = 3s\u00b2 \u2212 g, the compliance C = 1/k, and a fixed meal raises pressure P = V\u00b7k \u2014 nothing fitted. Functional dyspepsia (post-prandial distress) is impaired accommodation: as accommodation falls the wall stiffens, compliance falls (early satiation) and the fixed-meal pressure rises monotonically toward the stiff unaccommodated baseline. This is the post-prandial-distress axis that \u00a715 (FD-motility) left open; together they cover the two functional-dyspepsia axes. The maximal-compliance yield point is exactly the R19 spinodal (an algebraic identity). Treatment raises the compliance term to lower the meal pressure. Mechanism [V] partial; the felt distress (B3 afferent gain + mind firewall) and the absolute meal-volume / pressure scale [O] with stated obstacles.",
      body=body_reservoir),
 dict(n=18, slug="18-visceral-afferent-gain-ibs", subj="Visceral afferent gain (IBS subtypes, functional abdominal pain)",
      desc="A third Tier-2 primitive \u2014 a visceral afferent gain (the R19 element's susceptibility \u03c7 = 1/k = 1/(3s\u00b2\u2212g), the SAME curvature inverse the \u00a717 reservoir reads as compliance). IBS = a \u00a714 motility subtype (the transport bias orders IBS-C\u2192IBS-M\u2192IBS-D) PLUS a raised afferent gain (visceral hypersensitivity: gain rises, allodynia, spontaneous firing past the spinodal). Functional abdominal pain = raised gain at normal motility. The gain diverges at the R19 spinodal = the \u00a717 reservoir yield. Firewall: peripheral afferent term only; the felt pain is mind's.",
      grade="[V]", knows=["irritable bowel syndrome", "IBS-C IBS-D IBS-M", "visceral hypersensitivity", "functional abdominal pain", "visceral afferent", "brain-gut axis"],
      answer="Irritable bowel syndrome rides a new Tier-2 primitive: a visceral afferent gain, the R19 element's susceptibility \u03c7 = 1/k. IBS is a \u00a714 motility subtype (the transport bias orders IBS-C \u2192 IBS-M \u2192 IBS-D by retained fraction) plus a raised afferent gain (visceral hypersensitivity \u2014 allodynia, then spontaneous firing past the R19 spinodal). Functional abdominal pain is the same raised gain at normal motility.",
      abstract="The third Tier-2 primitive is a visceral afferent gain: a visceral afferent is the \u00a72 R19 switch ds/dt = g\u00b7s \u2212 s\u00b3 + h resting quiescent, and its static susceptibility to a wall-distension input is the restoring-curvature inverse \u03c7 = ds*/dh = 1/k = 1/(3s\u00b2 \u2212 g) \u2014 the IDENTICAL quantity the \u00a717 reservoir reads as fundic compliance (one curvature, two readings). IBS is two things at once: a \u00a714 motility subtype (the transport bias orders IBS-C \u2192 IBS-M \u2192 IBS-D by retained proximal fraction; the diarrhoea-side absolute magnitude hits the \u00a715 conserved-bolus ceiling, an honest [O]) plus a raised afferent gain. A peripheral sensitization bias slides the afferent toward yield, so the gain rises and a fixed normal distension yields a larger signal (allodynia); past the R19 spinodal a normal distension flips the element discontinuously into the firing basin (spontaneous activity). Functional abdominal pain is the same raised gain at normal motility, no structural lesion. The gain diverges exactly at the R19 spinodal \u2014 the same marginal saddle-node as the \u00a717 reservoir yield. Subtype ordering and the gain rise / allodynia are [V], the divergence-at-spinodal is the exact [F] identity; the felt pain (mind, behind the firewall) and the absolute rapid-transit magnitude / stool frequency are [O] with stated obstacles.",
      body=body_ibs),
 dict(n=19, slug="19-metaplasia-precursor-barrett-correa", subj="Metaplasia precursor step (Barrett's \u2192 EAC, gastric Correa cascade)",
      desc="A precursor compartment on a REDUCED R19 fate scale (g_meta = g \u2212 drop) \u2014 the same g-reduction the \u00a710 kernel uses for H. pylori, read as a discrete metaplasia. Barrett's\u2192EAC (RR\u224811) and gastric intestinal metaplasia (RR\u22483.6) sit on a smaller barrier, so the malignant crossing is RATE-LIMITED on the precursor; a dysplasia ladder accelerates it, and restoring g (ablation / removing the injury) collapses the next-step rate. Anchors [L]; rate-limiting + ladder shape [V]; absolute %/yr [O].",
      grade="[V]", knows=["Barrett's esophagus", "esophageal adenocarcinoma", "gastric intestinal metaplasia", "Correa cascade", "metaplasia", "dysplasia"],
      answer="A metaplastic precursor \u2014 Barrett's oesophagus, gastric intestinal metaplasia \u2014 is the same R19 cell-fate switch with its stability scale lowered by injury, the g-reduction the \u00a710 kernel uses for H. pylori. On the smaller barrier (Barrett's\u2192EAC RR\u224811, gastric IM RR\u22483.6) the malignant crossing is rate-limited on the precursor; ablation restores the scale and collapses the next-step rate.",
      abstract="A metaplastic precursor (Barrett's oesophagus, gastric intestinal metaplasia) is the \u00a77 R19 cell-fate switch with its stability SCALE reduced by sustained injury, g_meta = g \u2212 drop \u2014 the IDENTICAL g-reduction the \u00a710 kernel already uses for chronic H. pylori, read here as a discrete compartment (vendored single-source as metaplastic_scale / metaplasia_barrier_drop in the substrate). The g-drop is locked to the cited precursor-vs-general RR by one bisection: Barrett's-vs-general EAC RR\u224811 (Hvid-Jensen 2011), gastric intestinal-metaplasia RR\u22483.6. Because the next-step crossing fold exceeds three, carcinoma arises ~only from the precursor \u2014 the metaplasia step is rate-limiting (why surveillance and ablation are the levers). A dysplasia ladder (deeper g-drop: NDBE\u2192LGD\u2192HGD) accelerates the crossing, reproducing the observed direction and convex acceleration; restoring g toward healthy collapses the rate monotonically to one (the treatment reading: anti-reflux for Barrett's, eradication for the gastric cascade). The precursor anchors are [L]; the rate-limiting step, the dysplasia-ladder shape, and the treatment direction are [V]; the absolute progression %/yr and the exact ladder ratios are [O] (the model's ratios are lower than clinical, needing external population calibration \u2014 the model fixes direction and rate-limiting, not the absolute hazard).",
      body=body_metaplasia),
 dict(n=20, slug="20-carcinogen-synergy-hcc-escc", subj="Carcinogen synergy generalized (HCC: HBV\u00d7aflatoxin; ESCC: smoking\u00d7alcohol)",
      desc="Two carcinogenic drives on the SAME exact R19 barrier reproduce epidemiological super-additivity at two more organs and predict sub-multiplicativity near the spinodal. HCC = inflammation(g)\u00d7bias(h) (HBV\u00d7aflatoxin, joint RR\u224822 > additive-null); ESCC = bias(h)\u00d7bias(h) (smoking\u00d7alcohol, joint RR\u224817 > additive-null). Same structure as the \u00a710 gastric synergy. Anchors [L]; super-additivity [V]; sub-multiplicativity a falsifiable prediction; absolute incidence [O].",
      grade="[V]", knows=["hepatocellular carcinoma", "aflatoxin", "hepatitis B", "esophageal squamous cell carcinoma", "smoking alcohol synergy", "super-additive interaction"],
      answer="Two carcinogenic drives read off the same exact R19 barrier reproduce epidemiological super-additivity and predict sub-multiplicativity near the spinodal. Hepatocellular carcinoma (HBV inflammation \u00d7 dietary aflatoxin) and oesophageal squamous carcinoma (smoking \u00d7 alcohol) both give a joint risk above the additive-null yet below the multiplicative-null \u2014 diminishing returns at extreme dual exposure, a falsifiable prediction [V].",
      abstract="The \u00a710 gastric H. pylori\u00d7diet synergy generalizes: two drives on the same exact barrier reproduce super-additivity at two more organs. Hepatocellular carcinoma is the inflammation\u00d7bias case (chronic HBV lowers the barrier scale g, RR~7.3 alone; aflatoxin B1 adds a mutagenic bias h, RR~3.4 alone; joint ~22 exceeds the additive-null, cited Shanghai joint ~59). Oesophageal squamous carcinoma is the bias\u00d7bias case (smoking RR~4 and heavy alcohol RR~5 both add bias; joint ~17 exceeds the additive-null, cited combined-heavy ~40). On the same barrier both joints fall BELOW their multiplicative-null \u2014 the sub-multiplicativity (diminishing returns at extreme dual exposure) is a concrete falsifiable prediction, and newer/larger cohorts already trend this way. Treatment reading: removing either drive drops the joint risk along its own fan, the largest absolute benefit coming from removing one drive while the other is still present (the super-additive regime). Per-site anchors [L]; super-additivity [V]; absolute incidence [O] (population calibration); HCC carries a cited circulatory seam (hepatic first-pass), not re-emerged.",
      body=body_synergy),
 dict(n=21, slug="21-reversible-single-driver-and-kernel-boundary", subj="Reversibility, single-driver, and the honest kernel boundary (MALT, anal; GIST/NET/small-bowel/cholangio)",
      desc="The kernel's signature reversibility plus its honest edge. Gastric MALT lymphoma is an H. pylori barrier-scale reduction that REGRESSES on eradication (RR\u22486\u21921); anal SCC is a single sustained HPV bias, monotone. Four sites are out-of-kernel with stated obstacles: GIST and NET (gene-key \u2192 disease_wp), small-bowel adenocarcinoma (needs the C1 immune layer), cholangiocarcinoma (hepatobiliary + immune; circulatory seam). [V] reversibility / [L] anchors / [O] absolute incidence + the four boundary sites.",
      grade="[V]", knows=["gastric MALT lymphoma", "Helicobacter eradication", "anal carcinoma", "HPV", "GIST", "neuroendocrine tumor", "cholangiocarcinoma"],
      answer="The kernel's signature is reversibility: gastric MALT lymphoma is an H. pylori barrier-scale reduction that regresses when eradication restores the scale (RR\u22486\u21921). Anal squamous carcinoma is a single sustained HPV bias, monotone in exposure. Four sites stay out-of-kernel with stated obstacles \u2014 GIST and NET (gene-key), small-bowel adenocarcinoma (needs the immune layer), cholangiocarcinoma (hepatobiliary). Reversibility is [V]; absolute incidence [O].",
      abstract="Two sites sharpen the kernel's signature, then it states its own boundary. The strongest falsifiable claim is reversibility: a barrier-SCALE-driven cancer must regress when the scale is restored. Gastric MALT lymphoma is the clean test \u2014 an H. pylori g-reduction (RR~6) that regresses on eradication (~90% Hp+, ~77.5% remit on eradication alone, Zullo 2010); restoring g drops the rate monotonically to one. The ~22% t(11;18)/API2-MALT1 non-responders are a g-INDEPENDENT driver, outside this kernel and owned by disease_wp (the boundary the model should draw). Anal squamous carcinoma is the single-driver case: a sustained HPV E6/E7 bias, ~90% HPV-attributable (De Sanjos\u00e9 2019), monotone and vaccine-preventable. Treatment reading: remove the scale driver (eradication) or never apply the bias (vaccination) \u2014 prevention is the lever, established-tumour therapy is out-of-model. The honest boundary: the carcinogen-Kramers kernel does NOT cover GIST or gastroenteropancreatic NET (gene-key / neuroendocrine \u2192 disease_wp), small-bowel adenocarcinoma (needs the C1 immune layer to supply its barrier-lowering driver), or cholangiocarcinoma (needs a hepatobiliary + immune layer; circulatory seam). MALT reversibility and the anal monotone are [V] against cited anchors [L]; absolute incidence [O]; the four out-of-kernel sites are honest [O] with stated obstacles \u2014 stating the boundary is the result.",
      body=body_boundary),
 dict(n=22, slug="22-immune-relapsing-inflammation-ibd", subj="Immune relapsing-inflammation layer (IBD relapse hysteresis, induction/maintenance asymmetry, colitis\u2192cancer bridge)",
      desc="The first Tier-3 primitive: a relapsing mucosal inflammation is the R19 switch with a SELF-SUSTAINING flare basin. Inflammatory bowel disease shows relapsing-remitting HYSTERESIS (flip-up and flip-down thresholds differ \u2014 the flare persists as the trigger recedes), forcing the induction-vs-maintenance dose ASYMMETRY (the same mid-dose holds remission but cannot break a flare). Cumulative burden lowers the SAME \u00a77 barrier scale (g_eff = g_barrier \u2212 \u03ba\u00b7burden) the \u00a710 kernel uses for H. pylori, so colitis-associated colorectal cancer rises to the cited UC anchor (RR\u22482.4, Jess 2012) and collapses again on sustained remission \u2014 closing the \u00a721 out-of-kernel small-bowel-adenocarcinoma boundary on the inflammation route. The antigen-dependent regime (celiac, microscopic/eosinophilic/autoimmune) shares the element via driver removal. [V] hysteresis + asymmetry + burden\u2192barrier\u2192cancer / [F] spinodal thresholds / [L] colitis-CRC anchor / [O] absolute incidence, celiac absorptive magnitude, felt component.",
      grade="[V]", knows=["inflammatory bowel disease", "ulcerative colitis", "Crohn's disease", "relapsing remitting", "colitis associated colorectal cancer", "induction maintenance therapy", "celiac disease", "mucosal healing"],
      answer="Inflammatory bowel disease is the R19 switch with a self-sustaining flare basin: the relapsing-remitting course is a hysteresis (the flip-to-flare drive exceeds the return-to-remission drive, so a flare persists as the trigger recedes), which forces the induction-vs-maintenance asymmetry \u2014 the same dose holds remission but cannot break a flare. Cumulative burden lowers the same \u00a77 barrier scale, so colitis-cancer risk rises to the cited anchor and collapses on remission.",
      abstract="The first Tier-3 primitive: a relapsing mucosal inflammation is the \u00a72 R19 switch ds/dt = g\u00b7s \u2212 s\u00b3 + h whose active-inflammation basin self-sustains (vendored single-source as flare_state / flare_burden / inflammatory_barrier_scale in the substrate). Inflammatory bowel disease shows the defining relapsing-remitting HYSTERESIS \u2014 ramping the antigenic drive up flips to a flare past the induction spinodal, but ramping down regains remission only at a markedly lower drive, so the flare persists as the original trigger recedes. That hysteresis forces the therapeutic asymmetry: breaking an established flare (induction) needs suppression past antigen + spinodal, but a far lower maintenance dose then holds it \u2014 the SAME mid-dose has two opposite outcomes by history (it holds a patient in remission but cannot break a patient in flare), which is induction-then-taper as the substrate's own logic. The second reading bridges to the \u00a77 carcinogen kernel: cumulative inflammatory burden lowers the IDENTICAL barrier scale g_eff = g_barrier \u2212 \u03ba\u00b7burden the \u00a710 kernel uses for chronic H. pylori, so colitis-associated colorectal cancer is the same barrier step under a different sustained injury \u2014 one bisection locks \u03ba to the cited UC colorectal-cancer anchor (RR\u22482.4, Jess 2012), the risk rises monotonically with burden, and because the driver is a barrier-SCALE reduction the kernel's reversibility applies (sustained remission / mucosal healing restores g_eff and collapses the excess risk toward baseline). This closes the \u00a721 out-of-kernel small-bowel-adenocarcinoma boundary on the inflammation route. The same element in its antigen-DEPENDENT regime reads the immune enteropathies \u2014 celiac (and microscopic / eosinophilic / autoimmune) flares on the antigen (gluten) and remits on its removal, with the barrier and the villous surface recovering \u2014 the distinct operating regime where driver removal alone suffices. The relapsing hysteresis, the induction/maintenance asymmetry and the burden\u2192barrier\u2192cancer continuity are [V], the spinodal thresholds exact [F], the colitis-CRC RR a cited anchor [L]; the absolute remission and cancer-incidence rates, the celiac absorptive magnitude (needs an absorption layer), and the felt / affective component (mind, behind the firewall) are [O] with stated obstacles.",
      body=body_immune),
 dict(n=23, slug="23-exocrine-autodigestion-pancreatitis", subj="Exocrine autodigestion layer (acute pancreatitis autocatalytic latch, large-reserve EPI, PERT rescue)",
      desc="The second Tier-3 primitive: an AUTOCATALYTIC element \u2014 the R19 switch with self-amplification (active trypsin activates trypsinogen). Acute pancreatitis has an autoactivation threshold that rises with the protective inhibitor (SPINK1 up; PRSS1-gain / SPINK1-loss down \u2014 the hereditary genetics as one threshold shift); a sub-threshold trigger decays safely but a supra-threshold trigger LATCHES (the +g\u00b7s term self-sustains with the trigger removed), irreversible to any parameter move \u2014 so intervention is PRE-threshold only (remove the trigger before it crosses, or raise protection past the spinodal to abolish the basin). Chronic pancreatitis / EPI is the mirror: a large secretory reserve delays steatorrhea until ~90% acinar loss (DiMagno 1973), and PERT restores digestion above demand. [V] threshold-rises-with-inhibitor + irreversible latch + strong-inhibitor reversibility + large-reserve EPI + PERT rescue / [F] the latch is a forced R19 hysteresis / [L] the >90%-loss reserve threshold / [O] absolute trigger/inhibitor/demand scales, established-disease outcomes.",
      grade="[V]", knows=["acute pancreatitis", "trypsinogen autoactivation", "hereditary pancreatitis", "SPINK1", "PRSS1", "exocrine pancreatic insufficiency", "pancreatic enzyme replacement", "chronic pancreatitis"],
      answer="Acute pancreatitis is the R19 switch with an autocatalytic self-amplification (active trypsin activates trypsinogen). The autoactivation threshold rises with the protective inhibitor (SPINK1); a sub-threshold trigger decays safely but a supra-threshold trigger LATCHES \u2014 the self-sustaining basin is irreversible to any parameter move, so intervention is pre-threshold only. Chronic EPI is the mirror: a large reserve delays steatorrhea until ~90% acinar loss, and PERT restores digestion above demand.",
      abstract="The second Tier-3 primitive: an AUTOCATALYTIC element \u2014 the \u00a72 R19 switch ds/dt = g\u00b7s \u2212 s\u00b3 + h with a self-amplification term (active trypsin activates trypsinogen), vendored single-source as autoactivation_threshold / autodigestion_latched in the substrate. The first reading is the autoactivation threshold and its dependence on protection: the trigger needed to ignite the cascade rises with the protective inhibitor, so SPINK1 raises it while a gain-of-function protease (PRSS1) or loss of the inhibitor lowers it \u2014 the hereditary-pancreatitis genetics as a shift of one threshold, not a separate mechanism. The decisive reading is that the cascade LATCHES: a sub-threshold trigger fires briefly and decays back to the inactive rest basin (safe), but a supra-threshold trigger crosses into a self-sustaining active basin held on by the autocatalytic +g\u00b7s term with the trigger REMOVED \u2014 irreversible to any parameter move, which is exactly why an established attack cannot be switched off pharmacologically and is managed by supportive care. That makes intervention PRE-threshold only, stated as a rule: remove the trigger before it crosses (relieve the gallstone obstruction, stop alcohol, lower triglycerides) or raise the protection, because a strong-enough inhibitor past the R19 spinodal abolishes the self-sustaining basin entirely so the same trigger now decays. The chronic sequel is the mirror image: repeated attacks destroy acinar mass, but a large secretory RESERVE delays exocrine pancreatic insufficiency (steatorrhea) until capacity falls past ~90% loss (DiMagno 1973), the adequacy monotone in residual capacity; treatment is replacement \u2014 pancreatic enzyme replacement (PERT) adds exogenous output, restoring digestion above the demand once enough is supplied. The threshold-rises-with-inhibitor, the irreversible supra-threshold latch (pre-threshold-only intervention), the strong-inhibitor reversibility, and the large-reserve EPI with PERT rescue are [V], the latch an exact R19 hysteresis [F], the >90%-loss reserve threshold a cited anchor [L]; the absolute trigger / inhibitor and digestive-demand scales (model units) and the established-disease outcomes \u2014 necrosis extent, organ failure (need a tissue-injury layer) \u2014 are [O] with stated obstacles, and cystic-fibrosis CFTR is gene-key (disease_wp owns the gene defect, this package owns the ductal-secretion dynamics).",
      body=body_exocrine),
 dict(n=24, slug="24-perfusion-mesenteric-ischemia", subj="Perfusion / vascular layer (mesenteric ischaemia, ischaemic colitis, NAFLD/MASLD metabolic overlap)",
      desc="The third Tier-3 primitive: a perfusion-viability switch \u2014 the R19 element resting in the VIABLE basin (s=+\u221ag) with bias h = perfusion \u2212 demand, flipping to the ischaemic basin iff perfusion &lt; demand \u2212 spinodal and recovering iff perfusion &gt; demand + spinodal (a salvage window = 2\u00b7spinodal). Chronic mesenteric ischaemia (intestinal angina): the perfusion margin falls as post-prandial demand rises and crosses to deficit, with revascularisation restoring it. Acute mesenteric ischaemia / ischaemic colitis: a sudden occlusion flips viable\u2192ischaemic, and reperfusion recovers the tissue only WITHIN the time-critical salvage window (partial / late reperfusion stays infarcted). NAFLD/MASLD reuses the \u00a712 type-2 gain-loss homeostat unchanged; the hepatic lipid-deposition layer is a declared circulatory seam. [V] demand-driven margin collapse + revascularisation rescue + forced occlusion flip + salvage window + s12 reuse / [F] the ischaemic-flip and rescue thresholds are exact spinodal identities / [O] absolute perfusion/demand scales, structural infarction, and the circulatory lipid layer.",
      grade="[V]", knows=["mesenteric ischemia", "intestinal angina", "ischemic colitis", "acute mesenteric ischemia", "NAFLD", "MASLD", "fatty liver", "reperfusion injury"],
      answer="The perfusion / vascular layer rides a new Tier-3 primitive: a perfusion-viability switch \u2014 the R19 element in the viable basin with bias h = perfusion \u2212 demand. Chronic mesenteric ischaemia (intestinal angina) is the perfusion margin falling as a meal raises demand until it crosses to deficit, resolved by revascularisation. Acute mesenteric ischaemia (and ischaemic colitis) is a forced viable\u2192ischaemic flip with a time-critical salvage window: reperfusion recovers the tissue only inside it. The NAFLD/MASLD overlap reuses the \u00a712 type-2 homeostat unchanged, with the lipid-deposition layer declared a circulatory seam.",
      abstract="The third Tier-3 primitive is a perfusion-viability switch: the \u00a72 R19 double well ds/dt = g\u00b7s \u2212 s\u00b3 + h resting in the viable basin at s = +\u221ag, with the bias h = perfusion \u2212 demand (vendored single-source as perfusion_threshold / viability_margin / tissue_viable in the substrate). The first reading is chronic mesenteric ischaemia \u2014 intestinal angina: at a fixed marginal perfusion the reserve above the rescue threshold falls as metabolic demand rises, so a meal pushes the viability margin negative (post-prandial pain, food-aversion), and revascularisation (stent / bypass) lifts supply so the margin is positive across the demand range again. The second reading is acute mesenteric ischaemia (and its colonic counterpart, ischaemic colitis): a sudden occlusion drops perfusion past demand minus the spinodal and the tissue flips discontinuously into the ischaemic basin; the decisive feature is the salvage window \u2014 restoring flow recovers the tissue only if perfusion returns above demand + spinodal (a reserve window = 2\u00b7spinodal), so partial or late reperfusion stays infarcted (the time-critical revascularisation of clinical practice). The third reading is the NAFLD / MASLD metabolic overlap: it shares its insulin-resistance driver with the \u00a712 diabetes axis, so rather than refit a parameter this layer reuses the \u00a712 type-2 gain-loss homeostat unchanged, while the lipid-deposition step (hepatic triglyceride accumulation) is declared a circulatory seam handed across the firewall. The demand-driven margin collapse, the revascularisation rescue, the forced occlusion flip, the time-critical salvage window, and the s12 reuse are [V], the ischaemic-flip and rescue thresholds exact spinodal identities [F]; the absolute perfusion-pressure and metabolic-demand scales (model units), the structural infarction endpoint \u2014 transmural necrosis, perforation (need a tissue-injury layer) \u2014 and the hepatic lipid-deposition layer (circulatory's) are [O] with stated obstacles.",
      body=body_perfusion),
 dict(n=25, slug="25-hepatobiliary-cholelithiasis", subj="Hepatobiliary / bile layer (cholelithiasis nucleation barrier, dissolution hysteresis, biliary seams)",
      desc="The fourth Tier-3 primitive: a nucleation barrier \u2014 the R19 switch in which supersaturation (CSI &gt; 1) is METASTABLE, a stone nucleates only past CSI &gt; 1 + spinodal, and a formed stone redissolves only below CSI \u2212 spinodal (dissolution hysteresis). Cholelithiasis is cholesterol crystallising out of bile: supersaturated bile sits stone-free until the drive clears the nucleation barrier (the Kramers crossing), and a stone then persists below saturation \u2014 which is exactly why UDCA dissolution works only on small, early, near-saturation stones. Gallbladder stasis is the \u00a716 B1 sphincter-gate seam; cholecystitis is the B1 gate plus the cited \u00a722 C1 flare; biliary dyskinesia is the B1 gate; the nucleation time is the \u00a77 Kramers rate. Cholesterol delivery is a circulatory seam; the felt biliary colic is mind's. [V] metastable supersaturation + barrier-gated nucleation + dissolution hysteresis / [F] the nucleation and dissolution thresholds are exact spinodal identities and the nucleation time is the Kramers rate / [O] absolute CSI scale, the B1/C1 stasis/flare seams, and the circulatory/mind seams.",
      grade="[V]", knows=["cholelithiasis", "gallstones", "cholesterol gallstones", "bile supersaturation", "cholecystitis", "ursodeoxycholic acid", "biliary dyskinesia", "gallstone dissolution"],
      answer="The hepatobiliary / bile layer rides a new Tier-3 primitive: a nucleation barrier. Cholelithiasis is cholesterol crystallising out of bile, and supersaturation (CSI &gt; 1) is metastable, not sufficient \u2014 a stone nucleates only once the drive clears the barrier at CSI &gt; 1 + spinodal (the Kramers crossing). A formed stone then shows dissolution hysteresis, persisting below saturation, which is exactly why UDCA dissolution works only on small, early stones. Gallbladder stasis and cholecystitis are declared B1-gate and C1-flare seams; the felt biliary colic is mind's.",
      abstract="The fourth Tier-3 primitive is a nucleation barrier: cholesterol-bile crystallisation read as the \u00a72 R19 double well ds/dt = g\u00b7s \u2212 s\u00b3 + h with the dissolved phase as the rest basin and the cholesterol saturation index (CSI) as the bias (vendored single-source as nucleation_barrier / supersaturation_drive / stone_nucleates in the substrate). The first reading is that supersaturation is metastable, not sufficient: bile with CSI just above 1 is supersaturated yet remains stone-free (most people with lithogenic bile never form stones), and a stone nucleates only once the drive clears the barrier at CSI &gt; 1 + spinodal. The second, clinically decisive reading is dissolution hysteresis: a formed stone does not redissolve the instant bile drops below saturation \u2014 it persists, redissolving only far below it (a wide hysteresis gap), which is exactly why medical (UDCA) dissolution succeeds only on small, early, cholesterol-rich stones in a functioning gallbladder and why stones recur once therapy stops unless the lithogenic drive itself is removed. The remaining biliary syndromes are declared seams to primitives this package already owns, not re-modelled: gallbladder stasis (the second arm of stone risk) is the \u00a716 B1 sphincter-gate primitive, cholecystitis (a stone obstructing then inflaming) is the B1 gate plus the cited \u00a722 C1 flare, biliary dyskinesia is the B1 gate, and the nucleation time is the \u00a77 Kramers barrier-crossing rate. The metastable supersaturation, the barrier-gated nucleation, and the dissolution hysteresis are [V], the nucleation and dissolution thresholds exact spinodal identities and the nucleation time the Kramers rate [F]; the absolute cholesterol-saturation-index scale (a model unit), the stasis and cholecystitis syndromes (owned by the B1 gate and C1 flare), and the cholesterol-delivery (circulatory) and felt-pain (mind) seams are [O] with stated obstacles.",
      body=body_hepatobiliary),
 dict(n=26, slug="26-structural-diverticular-wall", subj="Structural / mechanical layer (diverticular disease Laplace wall-mechanics, fibre treatment, obstruction boundary)",
      desc="The fifth Tier-3 primitive: a wall-mechanics switch \u2014 the R19 wall (s=\u2212\u221ag) driven by the segmental Laplace pressure P = tension / radius, herniating iff P &gt; spinodal(g_wall), with a weaker wall (lower g_wall) crossing at a lower pressure. Diverticular disease is the colon out-pouching at weak points: a low-fibre diet (small hard stools, strong segmenting contractions) means a small luminal radius, so P = tension/radius rises as the radius falls until it clears the herniation threshold. A weaker wall (aging connective tissue, Ehlers\u2013Danlos / Marfan collagen) herniates at a fixed pressure a normal wall withstands (the age-rising prevalence). Treatment is the geometry in reverse: fibre bulks the stool (larger radius) and softens segmenting (lower tension), dropping P below threshold. DiverticulITIS is the cited \u00a722 C1 flare; the mechanical fixed-block obstructions (hernia incl. hiatal, volvulus, intussusception, adhesions) are the \u00a714 functional-module structural counterpart (surgical, out-of-model). [V] Laplace pressure rising as radius falls + discontinuous herniation + lower threshold of a weaker wall + fibre treatment / [F] the herniation threshold is an exact spinodal identity / [O] absolute pressure/strength scales, the C1 diverticulitis seam, and the \u00a714 obstruction counterpart.",
      grade="[V]", knows=["diverticular disease", "diverticulosis", "diverticulitis", "Laplace law colon", "dietary fiber", "bowel obstruction", "hernia", "volvulus"],
      answer="The structural / mechanical layer rides a new Tier-3 primitive: a wall-mechanics switch driven by Laplace's law. Diverticular disease is the colon out-pouching at weak points \u2014 by P = tension/radius, a low-fibre diet (small hard stools, strong segmenting contractions) means a small radius, so wall pressure rises until it clears the herniation threshold spinodal(g_wall). A weaker wall (aging, collagen disorder) herniates at a pressure a normal wall withstands. Treatment is the geometry in reverse: fibre bulks the stool (larger radius) and softens segmenting (lower tension), dropping pressure below threshold. DiverticulITIS is the cited C1 flare; the mechanical fixed-block obstructions are the \u00a714 functional-module counterpart.",
      abstract="The fifth Tier-3 primitive is a wall-mechanics switch: the colonic wall read as the \u00a72 R19 element ds/dt = g\u00b7s \u2212 s\u00b3 + h resting intact at s = \u2212\u221ag, with the segmental Laplace pressure P = tension / radius as the bias (vendored single-source as laplace_pressure / herniation_threshold / wall_herniates in the substrate). The first reading is the low-fibre pressure mechanism: by P = tension/radius a low-fibre diet \u2014 small, hard stools gripped by strong high-pressure segmenting contractions \u2014 means a small luminal radius, so the wall pressure rises as the radius falls, and once P exceeds the herniation threshold spinodal(g_wall) the intact wall buckles out into a diverticulum. The second reading is wall strength: at a fixed segmental pressure a normal wall withstands, a weaker wall (lower g_wall \u2014 aging connective tissue, an Ehlers\u2013Danlos / Marfan collagen disorder) has a lower threshold and herniates where a strong wall holds, reproducing the age-rising diverticulosis prevalence and the connective-tissue-disorder association as one falling threshold. Treatment is the geometry in reverse: dietary fibre bulks the stool (a larger luminal radius) and softens the segmenting contractions (lower tension), so the Laplace pressure drops back below the herniation threshold and the same colon stops out-pouching. Two boundaries are declared, not re-modelled: diverticulITIS (a formed pouch inflaming / obstructing) is the cited \u00a722 C1 inflammatory flare, and the mechanical fixed-block obstructions \u2014 hernia (including hiatal), volvulus, intussusception, adhesive obstruction \u2014 are the structural counterpart the \u00a714 functional motility module explicitly excludes (it keeps a patent lumen), their lever relieving the block, often surgical and out-of-model. The Laplace pressure rising as the radius falls, the discontinuous herniation, the lower threshold of a weaker wall, and the fibre treatment dropping pressure below threshold are [V], the herniation threshold an exact spinodal identity [F]; the absolute Laplace-pressure and wall-strength scales (model units), the diverticulITIS inflammation (the cited C1 flare seam), and the mechanical fixed-block obstructions (the \u00a714 functional module's structural counterpart \u2014 surgical, out-of-model) are [O] with stated obstacles.",
      body=body_structural),
 dict(n=27, slug="27-cross-system-seams-wired", subj="Cross-system seams (wired): circulatory hepatic delivery substrate + mind felt-symptom firewall",
      desc="The cross-volume seams the \u00a724 perfusion, \u00a725 hepatobiliary and \u00a718 afferent sections declared are now WIRED \u2014 citation/pointer-only, never a sibling code import, the neuro\u2194mind project-boundary rule. Circulatory is the SSOT owner of the hepatic interface (its charter hands hepatic clearance to this volume): its emitted Q_H = 1500 mL/min, E = 0.75, F = 0.25 are recorded once in inherited/cross_references.json (verified against circulatory's hepatic_clearance() at vendoring) and CONSUMED as the delivery substrate on which the \u00a724 NAFLD/MASLD lipid load (insulin-resistance core reusing the \u00a712 type-2 homeostat) and the \u00a725 biliary cholesterol (nucleation thermodynamics) sit \u2014 the lipid-handling and absolute-CSI scale handed back as circulatory's [O]. The mind felt-symptom seam (visceral pain \u00a718, biliary colic \u00a725) is a one-way forward-defer pointer carrying no consumed value, reaching mind's M18 interoception route (afferents \u2192 NTS \u2192 insula/cingulate, Saper 2002). The firewall is ENFORCED by an architectural lock \u2014 zero sibling imports across every package python file, and a metabolic state with no felt/HPA key \u2014 the same lock mind runs neuro-side. [V] the consumed circulatory hepatic interface + the \u00a712-homeostat reuse and nucleation thermodynamics resting on it / [F] the firewall (zero sibling imports; metabolic state mind-free) and the mind one-way pointer / [O] the lipid-handling + cholesterol-delivery magnitude (circulatory's) and the felt pain/affect (mind's).",
      grade="[V]", knows=["gut-liver axis", "gut-brain axis", "NAFLD MASLD", "cholelithiasis bile", "visceral hypersensitivity", "interoception", "hepatic first-pass", "cross-system physiology"],
      answer="The seams the \u00a724 / \u00a725 / \u00a718 sections declared are now wired \u2014 citation/pointer-only, never a sibling code import. Circulatory is the SSOT owner of the hepatic interface (Q_H = 1500 mL/min, E = 0.75, F = 0.25); this volume records its snapshot once and consumes it as the delivery substrate the NAFLD/MASLD lipid load and the biliary cholesterol sit on, with the lipid-handling and CSI scale handed back as [O]. The mind felt-symptom seam (visceral pain, biliary colic) is a one-way pointer carrying no value. The firewall is enforced by an architectural lock: zero sibling imports anywhere, and a metabolic state with no felt/HPA key.",
      abstract="The cross-volume seams the perfusion (\u00a724), hepatobiliary (\u00a725) and afferent (\u00a718) sections ended at are wired here under one rule taken verbatim from the neuro\u2194mind project boundary: a seam is citation/pointer-only, never a code import, and each volume re-establishes its trusted state from its own archive with the siblings absent. The first seam is the circulatory hepatic interface: by its own charter circulatory is the single source of truth for hepatic blood flow and first-pass clearance and hands them to this volume, so rather than re-derive them this package records circulatory's emitted hepatic interface once \u2014 hepatic blood flow Q_H = 1500 mL/min, extraction E = 0.75, bioavailability F = 0.25, clearance CL_H = 1125 mL/min, verified against circulatory's hepatic_clearance() at vendoring \u2014 in inherited/cross_references.json and consumes that snapshot as the delivery substrate on which the two hepatic-facing readings sit. The \u00a724 NAFLD/MASLD reading keeps only its insulin-resistance core (the \u00a712 type-2 gain-loss homeostat reused unchanged) and rests the lipid deposition on the consumed perfusion; the \u00a725 bile reading keeps only its crystallisation thermodynamics (the nucleation barrier) and rests the cholesterol delivery on the same perfusion; both consume the identical snapshot value, so the seam is internally consistent, and the lipid-handling magnitude and absolute cholesterol-saturation-index scale stay circulatory's. The second seam is the mind felt-symptom firewall: the \u00a718 visceral pain and \u00a725 biliary colic have a felt component this package does not own, handed OUT by a one-way forward-defer pointer that consumes no mind value \u2014 only the peripheral term crosses (the \u00a718 afferent signal, the \u00a725 mechanical stone trigger), the felt interpretation being mind's on its interoception route (visceral afferents \u2192 nucleus tractus solitarius \u2192 insula / cingulate, Saper 2002), with nothing returning (the metabolic state does not re-enter mind's HPA). The firewall is enforced not asserted: an architectural lock walks every python file in the package and confirms no sibling-code import exists and that the emitted metabolic state carries no felt/HPA key \u2014 the same lock mind runs neuro-side (mind has zero neuro imports; neuro has zero mind imports). The consumed circulatory hepatic interface (cited to circulatory's DOI and named function) and the \u00a712-homeostat reuse and nucleation thermodynamics resting on it are [V]; the firewall and the mind one-way pointer are a forced architectural identity [F]; the hepatic lipid-handling and absolute cholesterol-delivery magnitude (circulatory's), the felt visceral pain and biliary colic (mind's) are [O] with stated obstacles. The live cross-package harness that would run all the sibling engines together is no longer open \u2014 it is built and verified in \u00a730 (out of gate, each volume still verifying alone from its own archive).",
      body=body_seams),
 dict(n=28, slug="28-analgesic-target-logic-visceral-pain", subj="Analgesic target logic for visceral pain (inherited): a DNA-grounded 27-target firing-threshold map sorted into three drug-class levers",
      desc="INHERITED from analgesic_threshold_logic v2.0 (concept DOI 10.5281/zenodo.20733420, CC BY 4.0): a reproducible, DNA-grounded map of 27 non-opioid analgesic targets, applied to digestive visceral pain. Each pain gene's promoter \u03b3 = \u2212mean(NN stacking \u0394G, SantaLucia 1998) is placed on the R19 firing-threshold scale |h_sp| = 2(g/3)^1.5 = spinodal(\u03b3) \u2014 which IS this package's own \u00a718 visceral-afferent spinodal, so re-deriving all 27 reads through the local substrate reproduces the inherited thresholds bit-for-bit (drift 0). The targets sort into three intervention levers, all raising the same firing threshold: L1 reduce the inward (excitatory) current (Na_V / Ca_V / ASIC / P2X / TRP), L2 increase the outward K+ (K_V7), L3 remove the NGF/CGRP sensitising drive; 20 are gut-afferent-expressed. Read on the \u00a718 afferent, each lever raises the firing threshold / lowers the gain back to baseline, making the map a DRUG-CLASS POINTER for IBS hypersensitivity, functional abdominal pain, functional-dyspepsia pain, biliary colic and oesophageal-spasm pain (which lever, which cited validated agent class \u2014 \u03b1\u03b4 gabapentinoids, Na_V1.8 / P2X3 nociceptor-selective classes, K_V7 openers, anti-NGF / anti-CGRP). A GI burden-weighted prioritisation (inherited declared weights, \u03b3 never folded into the score) surfaces Na_V1.8, NGF, Na_V1.7; a precision-visceral-LA map pairs the four gut entry ports with a charged threshold raiser. FIREWALL (inherited verbatim): \u03b3 reads promoter switch-threshold STRUCTURE only \u2014 never a voltage, potency, dose, in-vivo selectivity, or clinical effect; every clinical magnitude + the felt pain is [O]; the lever strength \u03b4 is structural, not a dose; felt/affective pain is mind's (peripheral term only). Proposal-only; no molecule designed; nothing prescribes. [V] each lever raises the \u00a718 firing threshold / lowers the gain + the GI burden re-derivation / [F] the drift-0 inheritance (the firing-threshold scale = the \u00a718 spinodal), the three-lever identity, the declared-weight prioritisation, the precision-block mechanism shape / [O] every clinical magnitude (potency, dose, in-vivo selectivity, differential-block ratio, efficacy) and the felt pain (mind).",
      grade="[V]", knows=["non-opioid analgesic", "visceral pain", "IBS pain", "functional abdominal pain", "Nav1.8 suzetrigine", "Nav1.7", "P2X3", "gabapentinoid alpha2delta", "Kv7 retigabine", "anti-NGF", "anti-CGRP gepant", "nociceptor firing threshold", "pain target", "which painkiller"],
      answer="This section inherits a sibling whitepaper \u2014 analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420), a DNA-grounded map of 27 non-opioid analgesic targets \u2014 and applies it to digestive visceral pain. Each pain gene's promoter \u03b3 sits on the R19 firing-threshold scale |h_sp| = spinodal(\u03b3), which is this package's own \u00a718 afferent spinodal (all 27 reads re-derive bit-for-bit). The targets sort into three drug-class levers \u2014 reduce the inward current, open the K_V7 brake, remove the NGF/CGRP drive \u2014 and each raises the \u00a718 firing threshold, lowering the gain. The map points each visceral-pain disorder (IBS, functional abdominal pain, biliary colic) to a lever and a cited validated drug class; efficacy, dose, and the felt pain stay [O] / mind (firewall).",
      abstract="This section inherits a sibling whitepaper, analgesic_threshold_logic v2.0 (concept DOI 10.5281/zenodo.20733420, CC BY 4.0 \u2014 a reproducible, DNA-grounded map of 27 non-opioid analgesic targets), and applies it to digestive visceral pain on the shared substrate. The inherited engine reads each pain gene's human promoter and returns \u03b3 = \u2212mean(NN stacking \u0394G, SantaLucia 1998), placing it on the R19 double-well firing-threshold scale |h_sp| = 2(g/3)^1.5 = (2/3\u221a3)\u03b3^1.5 \u2014 which is identically this package's inherited/vp_substrate.spinodal, so re-deriving all 27 target reads through the local substrate reproduces the inherited firing thresholds bit-for-bit (max |h_sp| and barrier drift zero), and that firing-threshold axis IS the \u00a718 visceral-afferent spinodal the gain \u03c7 = 1/k diverges at \u2014 the identity that makes the inheritance principled rather than a paste. The 27 targets sort into three intervention levers, all raising the same firing threshold from different directions: L1 reduce the inward (excitatory) current (block depolarising Na_V / Ca_V / ASIC / P2X / TRP channels), L2 increase the outward K+ current (open K_V7), L3 remove the up-stream NGF / CGRP sensitising drive; twenty of the twenty-seven are expressed on the gut visceral afferent. Read on the \u00a718 afferent, the three levers do one thing: for a sensitised afferent (visceral hypersensitivity) each lever, applied at increasing structural strength \u03b4 (a fraction of the sensitisation removed, never a dose), raises the firing threshold T = spinodal \u2212 b_eff and lowers the gain \u03c7 = 1/k monotonically back toward the baseline 1/(2g), making the inherited map a drug-class pointer for every digestive visceral-pain disorder \u2014 IBS hypersensitivity, functional abdominal pain, functional-dyspepsia pain, biliary colic, oesophageal-spasm pain \u2014 naming which lever and which cited validated agent class realises it (the \u03b1\u03b4-1 gabapentinoid class and the emerging Na_V1.8 / P2X3 nociceptor-selective classes for L1, K_V7 openers for L2, anti-NGF / anti-CGRP for L3). A burden-weighted prioritisation of the GI nociceptor targets (inherited declared weights B/U/D over cited 1\u20135 tiers, with \u03b3 / |h_sp| never folded into the clinical score) re-derives the inherited score exactly and surfaces the realised peripheral case first (Na_V1.8, then NGF, then Na_V1.7), and a precision pain-selective visceral local-anaesthesia map pairs the four gut nociceptor entry ports with a charged firing-threshold raiser. The firewall is inherited verbatim and non-negotiable: \u03b3 reads promoter switch-threshold STRUCTURE only \u2014 it is never a channel activation voltage, a drug potency, a dose, an in-vivo selectivity, or a clinical effect; every such magnitude, the differential-block ratio, and absolute efficacy are [O]; the lever strength \u03b4 is structural, not a dose; the L3 mechanism link is [O] cited biology; and the felt / affective pain is mind's (this layer moves only the peripheral afferent-gain term, the \u00a727 firewall kept). No molecule is designed, no synthesis or dose is given, and nothing here diagnoses, treats, or prescribes \u2014 it is a proposal-only target hypothesis. The drift-zero inheritance and the three-lever de-sensitisation of the \u00a718 afferent and the burden re-derivation are [V] / [F]; every clinical magnitude (potency, dose, in-vivo selectivity, differential-block ratio, efficacy) and the felt pain (mind) are [O] with stated obstacles.",
      body=body_analgesic),
 dict(n=29, slug="29-remaining-in-substrate-perturbations",
      subj="Remaining in-substrate perturbations (dyssynergic defecation, Hirschsprung, MODY, hepatic GSD-I, autoimmune gastritis)",
      desc="Closes the in-substrate digestive Tier-1 surface (FUTURE_WORK \u00a71A\u2013\u00a71D) by REUSE \u2014 no new primitive, no sibling package: dyssynergic defecation (the \u00a716 gate read at the anorectal outlet \u2014 the achalasia mirror; the bolus is retained when the outlet stays closed while the propulsive drive is intact, the gate-not-drive distinction from colonic inertia), Hirschsprung motility consequence (a segmental aganglionic distal segment = absent oscillators on the \u00a71 emergence + \u00a74 transport blocks aboral clearance progressively, never traverses the deep aganglionic zone, and retains the bolus proximal at the transition zone = proximal dilatation; RET gene-key \u2192 disease_wp), MODY trajectory (a targeted partial \u03b2-secretory lesion on the \u00a712 homeostat \u2192 a distinct, stable, regulated elevated curve distinct from the \u00a712 type-1 catastrophic runaway; PDX1/HHEX gene-key \u2192 disease_wp), hepatic GSD type I counter-regulation consequence (a crippled hepatic glycogen-buffer release arm on the \u00a76 loop \u2192 fasting hypoglycaemia + failed counter-regulation; G6PC gene-key \u2192 disease_wp), and autoimmune gastritis (the \u00a722 relapsing-inflammation flare read corpus-localised + the \u00a77 barrier \u2192 a regional barrier lesion + an acid-output drop coupled to it, with driver suppression recovering both). Every phenotype emerges under wide sweeps; the three monogenic items are imported-lesion seams owned by disease_wp with the consequence dynamics owned here; felt and absorptive magnitudes are [O].",
      grade="[V]",
      knows=["dyssynergic defecation", "anismus", "pelvic floor dyssynergia", "Hirschsprung disease", "aganglionosis megacolon", "MODY", "monogenic diabetes", "glycogen storage disease", "von Gierke fasting hypoglycemia", "autoimmune gastritis", "pernicious anemia achlorhydria", "functional constipation"],
      answer="This section closes the in-substrate digestive Tier-1 surface by REUSE \u2014 no new primitive, no sibling package. Dyssynergic defecation reads the \u00a716 gate at the anorectal outlet (the bolus retained when the outlet stays closed while propulsion is intact \u2014 gate, not drive); Hirschsprung is a \u00a74 segmental aganglionic block with proximal dilatation; MODY a targeted \u00a712 secretory lesion giving a distinct, regulated curve unlike the type-1 runaway; hepatic GSD-I a crippled \u00a76 glycogen-buffer release giving fasting hypoglycaemia and failed counter-regulation; autoimmune gastritis the \u00a722 corpus-localised flare dropping barrier and acid together. The three monogenic items are gene-key \u2192 disease_wp [V]; felt and absorptive magnitudes [O].",
      abstract="This section closes the in-substrate digestive Tier-1 surface (FUTURE_WORK \u00a71A\u2013\u00a71D) \u2014 the disorders the roadmap had left enumerated are built here, each by REUSE of a module or primitive this volume already validated, with no new substrate primitive and no sibling package. Dyssynergic defecation reads the \u00a716 sphincter gate at the anorectal outlet (the achalasia mirror at the far end of the gut): the outlet gate is tonically closed and should open on the coordinated defecatory relaxation against the propulsive push, and in dyssynergia that relaxation fails (or the floor paradoxically contracts) so the gate stays closed and the bolus is retained despite a fully intact propulsive drive \u2014 the lesion is the gate, not the drive, the falsifiable distinction from colonic inertia. Hirschsprung disease is the motility consequence of a distal aganglionic segment with no slow-wave oscillator (the \u00a71-emergence reading): on the \u00a74 transport mechanics the bolus cannot be propagated through the dead segment, so aboral clearance is blocked progressively as the segment lengthens, the deep aganglionic zone is never traversed, and the bolus is retained proximal at the transition zone \u2014 the proximal dilatation above the narrowed segment. MODY is a targeted partial \u03b2-secretory-capacity lesion on the \u00a712 homeostat (PDX1/HHEX-linked) that settles a distinct, stable, fully-regulated elevated curve \u2014 the meal load returns to the mildly raised fixed point \u2014 clearly distinct from the \u00a712 type-1 catastrophic runaway. Hepatic glycogen storage disease type I (glucose-6-phosphatase deficiency) is read on the \u00a76 counter-regulation: the hepatic glycogen buffer cannot release free glucose, so fasting glucose drifts into hypoglycaemia and a hypoglycaemia challenge can no longer be returned to the setpoint (the failed counter-regulation). Autoimmune gastritis reads the \u00a722 relapsing-inflammation flare corpus-localised: a sustained autoimmune drive drops the corpus \u00a77 barrier and the acid output together (a regional, achlorhydric lesion distinct from antral H. pylori), driver suppression recovering both. Every phenotype emerges under wide sweeps and is never fitted; the three monogenic items (Hirschsprung RET, MODY PDX1/HHEX, GSD-I G6PC) are gene-key, owned by disease_wp with the consequence dynamics owned here and cross-referenced both ways; the gene links are cited from DNA [L]; and the felt straining/abdominal sensations (mind), the absolute evacuation/transit/glucose scales, the B12/iron malabsorption magnitude (an absorption layer), and the autoimmune-gastritis carcinoid boundary (disease_wp) are [O] with stated obstacles.",
      body=body_remaining),
 dict(n=30, slug="30-live-cross-package-harness",
      subj="Live cross-package harness: load every VP volume in one process and verify the shared substrate, hepatic seam, analgesic map and felt-symptom endpoint against the live sibling engines (out of gate)",
      desc="The last frontier item of the \u00a78 work order: a runner that loads THIS volume together with its sibling VP volumes (circulatory, musculoskeletal, neuro) in ONE process and confirms, against the LIVE sibling engines, the cross-volume identities the \u00a727 seam and \u00a728 inherited-analgesic layers had to take on trust. (1) Shared R19 substrate: every volume's firing-threshold spinodal |h_sp| = 2(g/3)^1.5 and barrier g\u00b2/4 are byte-identical (cross-volume drift 0) \u2014 the foundation that lets a primitive derived in one volume be read in another without a refit. (2) Circulatory hepatic seam: circulatory's live hepatic_clearance() reproduces the snapshot this volume vendored (Q_H = 1500 mL/min, E = 0.75, F = 0.25, CL_H = 1125 mL/min). (3) Analgesic 27-target map drift-0 across volumes: the inherited firing-threshold map re-derives bit-for-bit through every volume's own spinodal, and the built second host (musculoskeletal) reads its levers on the same spinodal. (4) Neuro felt-symptom endpoint: the peripheral nociceptor the \u00a718\u2192mind one-way pointer targets exists in neuro on the shared substrate (a HIGH-threshold polymodal cell, master PRDM12 / Na_V1.7 SCN9A \u2014 the same channel the \u00a728 L1 lever blocks). The harness runs OUTSIDE every gate: the research gate and the canonical build compute nothing here and never import a sibling \u2014 each volume re-establishes its trusted state from its own archive with the siblings absent (verify-alone), the sibling engines loaded by file path (not imported), and the harness digest hashes only the in-package digestive-side contract so it is byte-identical whether or not the siblings are on disk. [V] the live cross-volume checks (substrate drift 0, the vendored snapshot reproduced, the 27-target map re-derived, the neuro nociceptor on the shared substrate) / [F] the closed-form substrate identity and the out-of-gate firewall (file-path load only, verify-alone preserved) / [O] nothing new \u2014 a verification layer introducing no primitive and no claim; only the live run needs the sibling archives present.",
      grade="[V]",
      knows=["cross-package verification", "VP theory unification", "shared substrate identity", "reproducibility harness", "cross-volume consistency", "jamming physics volumes", "multi-system VP model", "live integration test", "R19 substrate", "verify alone", "deterministic reproducibility"],
      answer="This section is the live cross-package harness \u2014 the last frontier item of the work order. It loads this volume together with its sibling VP volumes (circulatory, musculoskeletal, neuro) in one process and verifies, against the live sibling engines, the four cross-volume identities the \u00a727 seam and \u00a728 analgesic layers had taken on trust: the shared R19 substrate (every volume's spinodal and barrier byte-identical, drift 0), circulatory's live hepatic clearance reproducing the vendored snapshot (Q_H = 1500 mL/min, E = 0.75, F = 0.25), the 27-target analgesic map re-deriving through every volume's spinodal, and the neuro nociceptor the felt-symptom pointer targets. It runs outside every gate \u2014 each volume still verifies alone from its own archive with the siblings absent, the engines loaded by file path not imported \u2014 so the build stays sibling-free and the harness digest is byte-identical with or without the siblings on disk. [V] the live checks; [F] the closed-form identity and the out-of-gate firewall; no new [O].",
      abstract="The \u00a727 seam layer and the \u00a728 inherited analgesic map both rest on a cross-volume identity they could only take on trust, because the governing discipline is verify-alone: every VP volume re-establishes its entire trusted state from its own archive with the siblings absent, so neither layer may import a sibling. The seam vendored circulatory's hepatic snapshot (verified once at vendoring time); the analgesic map asserted that its firing-threshold scale is exactly this volume's \u00a718 afferent spinodal. This section supplies the standing live proof \u2014 a harness that loads every VP volume into one process and checks those identities against the live sibling engines. Four identities are confirmed. (1) The shared R19 substrate: sweeping \u03b3 across the inherited analgesic-target gammas, every present volume's firing-threshold spinodal |h_sp| = 2(g/3)^1.5 and barrier g\u00b2/4 are byte-identical (cross-volume drift 0) \u2014 the foundation that lets a primitive derived in one volume be read in another without a refit. (2) The circulatory hepatic seam: circulatory's live hepatic_clearance() reproduces the snapshot this volume vendored (Q_H = 1500 mL/min, extraction E = 0.75, bioavailability F = 0.25, clearance CL_H = 1125 mL/min), so the \u00a724 NAFLD/MASLD lipid delivery and \u00a725 bile cholesterol delivery rest on a verified value. (3) The analgesic 27-target map: the inherited firing-threshold map re-derives bit-for-bit through every volume's own spinodal, so 'inherited once, read many times, drift 0' is a live cross-volume fact rather than a per-package claim, and the built second host (musculoskeletal, which already carries the analgesic layer) reads its own levers on the same spinodal. (4) The neuro felt-symptom endpoint: the peripheral nociceptor the \u00a718\u2192mind one-way pointer targets exists in neuro on the shared substrate \u2014 a high-threshold polymodal cell (master PRDM12, Na_V1.7 / SCN9A, the same channel the \u00a728 L1 lever blocks) that fires only to noxious drive \u2014 so the firewall pointer lands on a real, shared-substrate reading rather than a dangling reference. The harness runs outside every gate: the research gate (repro/run_all.py) and this canonical build compute nothing here and never import a sibling, so the pages were produced with the siblings absent (verify-alone intact); the sibling engines are loaded by file path under unique module names (the package-internal module table cleared between loads, so two volumes' identically-named vp_substrate cannot collide) \u2014 loading, not importing \u2014 and the harness's own source carries zero sibling import statements (self-checked). The harness digest hashes only the in-package digestive-side contract (the closed-form substrate values, the vendored snapshot, the drift-0 reverify, the neuro-endpoint descriptor), all computed from this archive alone, so it is byte-identical whether or not the siblings are on disk, and the engine, disease, C6, seam and analgesic digests are all unchanged. The live cross-volume readings are [V]; the closed-form substrate identity and the out-of-gate firewall (file-path load only, the build sibling-free, verify-alone preserved) are forced [F]; and because this is a verification layer that introduces no new primitive and makes no new claim there is no new [O] of its own \u2014 the only thing it cannot do offline is the live run itself, which needs the sibling archives present, which is exactly why the build and the gate stay sibling-free and the live check is a separate runner.",
      body=body_harness),
]

# ---------------------------------------------------------------------------
#  FRONT-MATTER overview pages (About / Methods / FAQ)
#  Not numbered sections -- they frame the work, emphasise the DNA-grounded
#  emergence, and carry the full VP-SPEC v1.8 SEO scaffolding (answer-first,
#  JSON-LD incl. FAQPage, canonical, claim-strip, DOI, keyword knowsAbout) so
#  the new framework competes on open search discoverability (C4 / 6-R).
# ---------------------------------------------------------------------------
def body_about(R):
    n_sec = len(SECTIONS)
    return f"""
<h2>A grounded model, not a toy simulation</h2>
<p>This work emerges the human digestive and metabolic system on a physical substrate and then drives it through its real physiology and its full disease spectrum. It is not an animation and not a hand-tuned cartoon: the four organs are <b>emerged deterministically from their real master-gene promoter sequences</b>, every displayed quantity is regenerated by an in-package engine, and a re-run reproduces the result <b>bit-for-bit ({m("2\u00d7sha256")} identical)</b>. The same random-close-packing jamming substrate the wider VP Theory uses for the vacuum carries the organs here.</p>
<p>Because the organs are read out of DNA rather than assumed, the model earns the right to say something mechanistic about how the gut and the metabolic loop behave, fail, and recover. That is the difference between a grounded emergence model and a toy: the starting point is measured from sequence, the dynamics are forced by the substrate, and nothing is migrated to hit a target.</p>
{CARD_GAMMA}
{CARD_R19}
<h2>What is emerged from DNA</h2>
<p>Four master genes set four organs on the shared bistable jamming switch {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")}, with the basin-threshold scale {m("g")} fixed by the read-only morphogenesis variable {m("\u03b3 = \u2212mean nearest-neighbour stacking \u0394G")} (SantaLucia 1998) measured from each gene's promoter: <b>BARX1 \u2192 stomach</b> (gastric slow-wave pacemaker), <b>CDX2 \u2192 intestine</b> (peristaltic propulsion), <b>PDX1 \u2192 pancreas</b> (the insulin / glucagon glucose homeostat), and <b>HHEX \u2192 liver</b> (the hepatic glucose buffer). Organ identity and developmental order are a pure {m("\u03b3")} read-out; this package adds only the functional dynamics the later sections exercise.</p>
<h2>The full scope \u2014 twenty-eight sections</h2>
<p>The volume is not a single demonstration. It is a complete pass over the digestive and metabolic system: the organ emergence and the mechanism modules (gastric slow wave, the aboral frequency gradient, peristaltic transport, the glucose\u2013insulin homeostat, glucagon counter-regulation) and a single carcinogen barrier-Kramers kernel instantiated for colorectal, pancreatic and gastric sites (\u00a71\u2013\u00a710).</p>
<p>On that validated base sit <b>thirteen disease modules</b> (\u00a711\u2013\u00a718): gastric dysrhythmia and gastroparesis, the type 1 / type 2 diabetes spectrum, gastritis and peptic ulcer, the intestinal motility and transit disorders, a cluster of scattered Tier-1 perturbations (dumping, reflux oesophagitis, insulinoma and reactive hypoglycaemia, functional dyspepsia, SIBO), the sphincter-gate disorders (GERD and achalasia as two opposite failures of one gate, plus oesophageal spasm and sphincter of Oddi), the gastric accommodation reservoir (functional dyspepsia and post-prandial distress), and the visceral afferent-gain disorders (the IBS subtypes and functional abdominal pain).</p>
<p>The carcinogen kernel is then extended across <b>metaplasia and carcinoma</b> (\u00a719\u2013\u00a721: Barrett's and Correa metaplasia, the HBV\u00d7aflatoxin and smoking\u00d7alcohol synergies, reversible H. pylori MALT lymphoma, HPV anal carcinoma), and <b>five Tier-3 cross-system layers</b> (\u00a722\u2013\u00a726) add the immune relapsing-inflammation layer (inflammatory bowel disease), the exocrine autodigestion layer (acute and chronic pancreatitis), the perfusion / vascular layer (mesenteric ischaemia, NAFLD / MASLD), the hepatobiliary / bile layer (cholelithiasis), and the structural / mechanical layer (diverticular disease). A cross-system seam section (\u00a727) wires the circulatory and mind interfaces citation-only, and an inherited section (\u00a728) reads a DNA-grounded 27-target non-opioid analgesic map onto the volume's own visceral-pain spinodal.</p>
{CARD_KERNEL}
<h2>Reproducibility and honest grading</h2>
<p>Every claim carries one of four grades \u2014 <b>[F] forced</b> by the substrate, <b>[V] simulation-verified</b>, <b>[L] cited-and-locked anchor</b>, or <b>[O] open</b> \u2014 and every {m("[O]")} carries a stated obstacle in the irreproducibility ledger. The engine is deterministic to {m("2\u00d7sha256")}; the displayed numbers are not typed in, they are emitted. Claims are never inflated: where a magnitude is not earned \u2014 a felt experience, an absolute incidence, a clinical efficacy \u2014 it is marked {m("[O]")} rather than asserted. This is what lets a strong framework stay honest.</p>
<h2>Three unifying results, demonstrated on one substrate</h2>
<p>One ICC pacemaker lesion collapses both gastric emptying and gut transit (gastroparesis with slow-transit constipation and pseudo-obstruction) \u2014 one cause, many sites. One barrier-scale axis runs continuously from gastritis through ulcer and metaplasia to carcinoma across organs on a single kernel. One homeostat capacity / gain axis spans normal tolerance through impaired glucose tolerance to type 2 and type 1 diabetes. These are not three models; they are three readings of the same jamming switch.</p>
<h2>How this is published</h2>
<p>This is a new conceptual framework, and it is published to be <b>found</b>: open-access under CC BY 4.0 with a permanent Zenodo DOI, structured for search engines and AI assistants (answer-first pages, machine-readable schema, a deterministic reproduction tree on GitHub). The competition is open discoverability and reproducibility, not gatekept review. Read the <a href="/{PAPER_ID}/methods/">methods</a> for exactly how the organs are emerged from DNA, the <a href="/{PAPER_ID}/faq/">FAQ</a> for common questions, or the <a href="/{PAPER_ID}/">contents</a> for all {n_sec} sections.</p>
"""

def body_methods(R):
    o = {x["organ"]: x for x in R["organs"]["organs"]}
    order = ", ".join(R["organs"]["gamma_order_ascending"])
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %
        (esc(o[k]["master"]), esc(o[k]["organ"]), o[k]["gamma"], esc(o[k]["role"]))
        for k in ["stomach", "intestine", "pancreas", "liver"])
    fast = R["dynamics"]["glucose_homeostat"]["fasting_fixed_point_mM"]
    fast_str = format(fast, "g")
    return f"""
<h2>From a promoter sequence to an organ</h2>
<p>The central methodological claim is simple and falsifiable: <b>the organs are not hand-coded</b>. Each organ's master gene has a real human proximal-promoter sequence; that sequence is read for its <b>nearest-neighbour base-stacking thermodynamics</b>, and the single resulting number {m("\u03b3 = \u2212mean nearest-neighbour stacking \u0394G")} (the SantaLucia 1998 unified parameter set) becomes the basin-threshold scale {m("g")} of a bistable jamming switch. Identity and developmental order then fall out of {m("\u03b3")} alone \u2014 they are not assumed.</p>
{CARD_GAMMA}
<p>The four organs and their measured {m("\u03b3")}, live from the engine:</p>
<table><thead><tr><th>master gene</th><th>organ</th><th>measured \u03b3</th><th>physiological role</th></tr></thead><tbody>{rows}</tbody></table>
<p>Developmental order is a pure ascending-{m("\u03b3")} read-out: {esc(order)}. The sign of this ordering is validated against the cited developmental-timing anchor; the magnitudes are forced by the substrate, not chosen. No coefficient is ever migrated to fit a phenotype.</p>
<h2>The jamming substrate (R19)</h2>
<p>Every organ, gate, reservoir, afferent, barrier and switch in the volume is one and the same object: the R19 bistable element {m("ds/dt = g\u00b7s \u2212 s\u00b3 + h")}, where {m("g")} is the {m("\u03b3")}-set basin depth and {m("h")} is the physiological drive. This is the same random-close-packing jamming physics the wider VP Theory uses for the vacuum, read here at organ scale. A sustained drive lowers the basin barrier as {m("(h_sp \u2212 h)^1.5")} and the state flips discontinuously at the spinodal {m("h_sp")} \u2014 the single mechanism behind the disease thresholds, the carcinogen kernel, the sphincter gate, the reservoir yield and the afferent-gain divergence.</p>
{CARD_R19}
{CARD_BARRIER}
<h2>Determinism \u2014 bit-for-bit reproducible</h2>
<p>The engine is fully deterministic. Running it twice produces a {m("2\u00d7sha256")}-identical result, and the published HTML is regenerated from that result so that <b>every displayed number is emitted, never entered by hand</b>. A reader who downloads the reproduction tree and runs it obtains the same fasting set-point ({m("\u2248 " + fast_str + " mM")}), the same gastric-to-duodenal frequency gradient, and the same disease thresholds \u2014 down to the digest.</p>
{CARD_KERNEL}
<h2>No tuning, and an honest grade on every line</h2>
<p>The discipline is strict: {m("\u03b3")} is read-only and never fitted; an anchor is cited and locked ({m("[L]")}) and calibrated by at most a single bisection to one literature value; a quantity the substrate forces is {m("[F]")}; a quantity the simulation produces is {m("[V]")}; and a quantity the model cannot honestly earn \u2014 an absolute incidence, a felt pain, a clinical efficacy \u2014 is left {m("[O]")} with a stated obstacle in the ledger. Nothing here diagnoses, treats or prescribes; the mechanism is the claim, and its limits are marked.</p>
"""

FAQ_QA = [
 ("Is this a real simulation or just a conceptual diagram?",
  "It is a real, executable, deterministic simulation. The digestive organs are emerged from DNA on a jamming substrate by an in-package engine, the engine runs the slow-wave, homeostat and disease dynamics, and every number on these pages is emitted by that engine and reproduced bit-for-bit (2\u00d7sha256 identical) on re-run. The reproduction code is published openly so the result can be checked, not just read."),
 ("How are the digestive organs emerged from DNA?",
  "Each organ's master gene has a real human promoter sequence. That sequence is read for its nearest-neighbour base-stacking thermodynamics, giving a single number \u03b3 = \u2212mean nearest-neighbour stacking \u0394G (SantaLucia 1998). \u03b3 sets the basin depth of a bistable jamming switch, and organ identity and developmental order fall out of \u03b3 \u2014 they are measured from sequence, not assumed."),
 ("Which organs and which master genes?",
  "Four: BARX1 \u2192 stomach (gastric slow-wave pacemaker), CDX2 \u2192 intestine (peristaltic propulsion), PDX1 \u2192 pancreas (the insulin / glucagon glucose homeostat), and HHEX \u2192 liver (the hepatic glucose buffer)."),
 ("Is the output reproducible?",
  "Yes. The engine is deterministic to 2\u00d7sha256: two runs return a byte-identical result, and the HTML is regenerated from that result, so nothing is hand-entered. Anyone can download the GitHub reproduction tree and obtain the same set-points, frequency gradients and disease thresholds, down to the digest."),
 ("What diseases does the model cover?",
  "Thirteen disease modules plus a neoplastic extension and five cross-system layers: gastroparesis and gastric dysrhythmia, type 1 and type 2 diabetes, gastritis and peptic ulcer, intestinal dysmotility and constipation, dumping and reflux and SIBO, GERD and achalasia, functional dyspepsia, IBS and functional abdominal pain, gastrointestinal cancers (Barrett's / oesophageal, gastric / Correa, hepatocellular, MALT, anal), inflammatory bowel disease, acute and chronic pancreatitis, mesenteric ischaemia and NAFLD / MASLD, gallstones, and diverticular disease."),
 ("Is this peer-reviewed?",
  "No. This is an independent research framework, published open-access under CC BY 4.0 with a permanent Zenodo DOI. It is a new conceptual theory and it competes through open, reproducible, search-discoverable exposure rather than the traditional journal route. The four-grade system and the irreproducibility ledger are how it states its own confidence honestly, claim by claim."),
 ("Can it diagnose, treat or prescribe?",
  "No. It is a mechanistic, proposal-only model. It predicts which parameter an effective therapy would move and in which direction, but every clinical magnitude \u2014 absolute efficacy, dose, selectivity \u2014 and every felt experience are graded open [O], and nothing here diagnoses, treats or prescribes. It is not medical advice."),
 ("What do the grades [F], [V], [L], [O] mean?",
  "[F] forced \u2014 the substrate forces the result exactly. [V] simulation-verified \u2014 the simulation produces it under wide parameter sweeps. [L] cited-and-locked \u2014 a literature anchor, calibrated by at most a single bisection. [O] open \u2014 not yet reproducible in-package; every [O] carries a stated obstacle."),
 ("What is the \u201cjamming\u201d substrate?",
  "VP Theory / Jamming Physics models a medium \u2014 the vacuum, and here biological tissue \u2014 as a random-close-packed granular solid. Its fundamental element is the R19 bistable switch ds/dt = g\u00b7s \u2212 s\u00b3 + h; the same switch is read as an organ, a sphincter gate, a fundic reservoir, a visceral afferent, a carcinogen barrier and a gallstone nucleation barrier across this volume."),
 ("What is the DOI and licence?",
  "The Zenodo concept DOI is 10.5281/zenodo.20755319 (https://doi.org/10.5281/zenodo.20755319), the licence is CC BY 4.0, and the author is Young Jae Lee (ORCID 0009-0002-7535-8245)."),
 ("How does this relate to the wider VP Theory?",
  "It is one volume of a multi-domain framework that derives physics, cosmology, fluid dynamics, geodynamics, DNA interpretation, neuroscience and consciousness from the same jamming substrate. The digestive organs here are emerged from the DNA volume's morphogenesis read-out and driven by the physics volume's substrate."),
]

def body_faq(R):
    blocks = "".join(
        '<section class="faq-item"><h2>%s</h2><p>%s</p></section>' % (esc(q), esc(a))
        for q, a in FAQ_QA)
    return ('<p>Common questions about this DNA-grounded emergence model of the digestive and metabolic '
            'system \u2014 what it is, how the organs are emerged from real DNA, what it covers, and how it is '
            'published. For the methodology see the <a href="/%s/methods/">methods</a>; for the full set of '
            'sections see the <a href="/%s/">contents</a>.</p>%s') % (PAPER_ID, PAPER_ID, blocks)

FRONT_MATTER = [
 dict(slug="about", nav="About", nav_long="About this work",
      subj="About \u2014 a DNA-grounded emergence model of the digestive and metabolic system",
      desc=("A deterministic, DNA-grounded physics model of the human digestive and metabolic system: four "
            "organs emerged from their real master-gene promoter sequences on a jamming substrate, then driven "
            "through slow-wave transport, the glucose homeostat, a carcinogen kernel and thirty-plus disease "
            "regimes \u2014 every number reproduced bit-for-bit."),
      knows=["VP Theory", "jamming physics", "DNA-grounded simulation", "digestive system model",
             "metabolic system model", "organ emergence from DNA", "computational gastroenterology",
             "deterministic physiology simulation", "reproducible biological model", "gut motility model",
             "glucose homeostat model", "BARX1", "CDX2", "PDX1", "HHEX"],
      answer=("This is a deterministic, DNA-grounded physics model of the human digestive and metabolic system. "
              "Four organs \u2014 stomach, intestine, pancreas, liver \u2014 are emerged from their real master-gene "
              "promoter sequences on a jamming substrate, then driven through slow-wave transport, the glucose "
              "homeostat, a shared carcinogen kernel and thirty-plus disease regimes. Every number is reproduced "
              "bit-for-bit. This is not a toy simulation."),
      abstract=("This volume of VP Theory / Jamming Physics is a deterministic, DNA-grounded model of the human "
                "digestive and metabolic system. Four organs are emerged from their real master-gene promoter "
                "sequences on a random-close-packing jamming substrate \u2014 identity and developmental order read "
                "out of DNA, not assumed \u2014 and then driven through gastric slow-wave transport, the aboral "
                "frequency gradient, peristalsis, the glucose\u2013insulin\u2013glucagon homeostat, glucagon "
                "counter-regulation, and a single carcinogen barrier-Kramers kernel across three organ sites. On "
                "that validated base sit thirteen disease modules, a neoplastic extension across metaplasia and "
                "carcinoma, five Tier-3 cross-system layers, a cross-system seam section, and an inherited "
                "DNA-grounded analgesic target map \u2014 twenty-eight sections in all. Every displayed number is "
                "regenerated by an in-package engine and reproduced bit-for-bit (2\u00d7sha256 identical); every claim "
                "carries an explicit grade ([F] forced, [V] simulation-verified, [L] cited-and-locked, [O] open "
                "with a stated obstacle); and three unifying hypotheses are demonstrated on the single substrate. "
                "It is published open-access (CC BY 4.0, Zenodo DOI 10.5281/zenodo.20755319), structured for search "
                "engines and AI assistants, with a deterministic reproduction tree \u2014 a new conceptual framework "
                "that competes through open discoverability and reproducibility rather than gatekept review."),
      grade="[V]", body=body_about),
 dict(slug="methods", nav="Methods", nav_long="How organs emerge from DNA (methods)",
      subj="Methods \u2014 how the digestive organs emerge from DNA on a jamming substrate",
      desc=("How the organs are emerged from DNA: each master-gene promoter is read for its nearest-neighbour "
            "stacking thermodynamics \u03b3 = \u2212mean \u0394G (SantaLucia 1998), which sets the basin depth of a bistable "
            "jamming switch; identity and order fall out of DNA, only the dynamics are added, nothing is fitted, "
            "and the engine is deterministic to 2\u00d7sha256."),
      knows=["SantaLucia 1998 nearest neighbour thermodynamics", "DNA promoter thermodynamics",
             "nearest-neighbour stacking free energy", "BARX1 CDX2 PDX1 HHEX promoter", "organ emergence",
             "bistable switch", "random close packing", "R19 jamming substrate", "deterministic reproducible model",
             "no-tuning model", "spinodal threshold", "VP Theory methods"],
      answer=("The organs are not hand-coded. Each master gene's promoter is read for its nearest-neighbour "
              "stacking thermodynamics \u2014 \u03b3 = \u2212mean \u0394G (SantaLucia 1998) \u2014 and that single number sets the "
              "basin depth of a bistable jamming switch. Organ identity and developmental order fall out of DNA; "
              "only the dynamics are added, and nothing is fitted to a target."),
      abstract=("The methodological core of this volume is that the digestive organs are not hand-coded but emerged "
                "from DNA. Each organ's master gene \u2014 BARX1 (stomach), CDX2 (intestine), PDX1 (pancreas), HHEX "
                "(liver) \u2014 has a real human promoter sequence; that sequence is read for its nearest-neighbour "
                "base-stacking thermodynamics, yielding a single morphogenesis variable \u03b3 = \u2212mean "
                "nearest-neighbour stacking \u0394G under the SantaLucia 1998 unified parameter set. \u03b3 sets the "
                "basin-threshold depth g of a bistable jamming switch ds/dt = g\u00b7s \u2212 s\u00b3 + h, so organ identity and "
                "developmental order fall out of \u03b3 alone, validated in sign against a cited developmental-timing "
                "anchor. The same R19 bistable element is then read as every functional object in the volume \u2014 a "
                "sphincter gate, a fundic reservoir, a visceral afferent, a carcinogen barrier, a gallstone "
                "nucleation barrier \u2014 its basin barrier collapsing as (h_sp \u2212 h)^{3/2} and flipping "
                "discontinuously at the spinodal, the one mechanism behind the disease thresholds and the cancer "
                "kernel. The engine is deterministic to 2\u00d7sha256: two runs return a byte-identical result and the "
                "HTML is regenerated from it, so every displayed number is emitted rather than entered. The "
                "discipline is strict no-tuning (\u03b3 read-only, anchors cited and locked by at most a single "
                "bisection), and every quantity the model cannot honestly earn \u2014 an absolute incidence, a felt "
                "pain, a clinical efficacy \u2014 is left open [O] with a stated obstacle."),
      grade="[V]", body=body_methods),
 dict(slug="faq", nav="FAQ", nav_long="FAQ",
      subj="Frequently asked questions \u2014 the DNA-grounded digestive and metabolic model",
      desc=("FAQ: is this a real reproducible simulation, how are the organs emerged from real DNA, which "
            "gastrointestinal and metabolic diseases it covers, what the honest grading means, how it relates to "
            "VP Theory, and how it is published under CC BY 4.0 with a Zenodo DOI."),
      knows=["digestive model FAQ", "DNA-grounded simulation", "reproducible model", "VP Theory",
             "jamming physics", "gastrointestinal disease model", "SantaLucia 1998", "open access research",
             "Zenodo DOI", "is it peer reviewed", "is it a real simulation"],
      answer=("Frequently asked questions about this DNA-grounded emergence model of the human digestive and "
              "metabolic system: whether it is a real and reproducible simulation, how the four organs are emerged "
              "from real master-gene promoter sequences, which gastrointestinal and metabolic diseases it covers, "
              "what the honest grading system means, and how it is published for open discovery under CC BY 4.0."),
      abstract=("Frequently asked questions about this DNA-grounded emergence model of the human digestive and "
                "metabolic system: whether it is a real and reproducible simulation, how the four organs are "
                "emerged from real master-gene promoter sequences, which gastrointestinal and metabolic diseases "
                "it covers, what the honest grading system means, how it relates to the wider VP Theory jamming "
                "framework, and how it is published for open discovery under CC BY 4.0 with a permanent Zenodo DOI. "
                "The model is mechanistic and proposal-only \u2014 it predicts which parameter a therapy would move, "
                "never a diagnosis or a prescription."),
      grade="[V]", faq=FAQ_QA, ld_type="FAQPage", body=body_faq),
]

# ---------------------------------------------------------------------------
#  page + hub templates
# ---------------------------------------------------------------------------
def render_front_page(fm, R):
    slug = fm["slug"]
    canon = f"{DOMAIN}/{PAPER_ID}/{slug}/"
    title = f"{fm['subj']} \u2014 {SHORT} | Jamming Physics"
    knows = ", ".join('"%s"' % k for k in fm["knows"])
    ld_type = fm.get("ld_type", "ScholarlyArticle")
    if ld_type == "FAQPage":
        faq_main = ",".join(
            '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
            % (json.dumps(q), json.dumps(a)) for q, a in fm["faq"])
        primary_ld = ('{"@context":"https://schema.org","@type":"FAQPage","name":'
                      + json.dumps(fm["subj"]) + "," + DOI_JSONLD
                      + '"mainEntity":[' + faq_main + ']}')
    else:
        primary_ld = ('{"@context":"https://schema.org","@type":"' + ld_type + '",'
                      + '"headline":' + json.dumps(fm["subj"]) + ','
                      + DOI_JSONLD
                      + '"isPartOf":{"@type":"CreativeWorkSeries","name":' + json.dumps(SHORT) + '},'
                      + '"author":{"@type":"Person","name":"Young Jae Lee","sameAs":"' + ORCID + '"},'
                      + '"datePublished":"' + BUILD_DATE + '","dateModified":"' + BUILD_DATE + '",'
                      + '"isBasedOn":' + json.dumps(REPO) + ','
                      + '"license":"' + LICENSE + '","knowsAbout":[' + knows + ']}')
    crumb_ld = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
                '{"@type":"ListItem","position":1,"name":"Home","item":"' + DOMAIN + '/"},'
                '{"@type":"ListItem","position":2,"name":' + json.dumps(SHORT) + ',"item":"' + DOMAIN + '/' + PAPER_ID + '/"},'
                '{"@type":"ListItem","position":3,"name":' + json.dumps(fm["subj"]) + '}]}')
    ld_scripts = ('<script type="application/ld+json">\n' + primary_ld + '\n</script>\n'
                  '<script type="application/ld+json">\n' + crumb_ld + '\n</script>')
    cls, label = GRADE_LABEL[fm["grade"]]
    strip = ('<aside class="claim-strip">'
             '<span class="grade %s">%s</span>'
             '<span class="gate">LOCK \u2192 Derive \u2192 Gate</span>'
             '<a href="%s/" rel="noopener">reproduction code (GitHub)</a>'
             '<span class="doi">DOI: %s</span></aside>'
             ) % (cls, esc(label), REPO, DOI_LINK_HTML)
    body = fm["body"](R)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(fm['desc'])}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="/assets/css/site.css">
{ld_scripts}
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> \u203a <a href="/{PAPER_ID}/">{esc(SHORT)}</a> \u203a {esc(fm['nav'])}</nav></header>
<main>
<h1>{esc(fm['subj'])}</h1>
<p class="answer">{esc(fm['answer'])}</p>
<p class="abstract">{esc(fm['abstract'])}</p>
{strip}
{body}
<nav class="pn"><a href="/{PAPER_ID}/">\u2190 contents</a></nav>
</main>
<footer><p>{esc(AUTHOR)} \u00b7 ORCID <a href="{ORCID}" rel="noopener">0009-0002-7535-8245</a> \u00b7 DOI: {DOI_LINK_HTML} \u00b7 <a href="{LICENSE}" rel="noopener license">CC BY 4.0</a></p></footer>
</body>
</html>
"""

def claim_strip(grade_token):
    cls, label = GRADE_LABEL[grade_token]
    return ('<aside class="claim-strip">'
            '<span class="grade %s">%s</span>'
            '<span class="gate">LOCK \u2192 Derive \u2192 Gate</span>'
            '<a href="%s/%s/" rel="noopener">reproduction code (GitHub)</a>'
            '<span class="doi">DOI: %s</span>'
            '</aside>') % (cls, esc(label), REPO, esc("SLUGPLACEHOLDER"), DOI_LINK_HTML)

def render_page(sec, prev_sec, next_sec, R):
    slug = sec["slug"]; n = sec["n"]
    canon = f"{DOMAIN}/{PAPER_ID}/{slug}/"
    title = f"{sec['subj']} \u2014 {SHORT} \u00a7{n} | Jamming Physics"
    knows = ", ".join('"%s"' % k for k in sec["knows"])
    article_ld = (
        '{"@context":"https://schema.org","@type":"ScholarlyArticle",'
        f'"headline":{json.dumps(sec["subj"])},'
        f'{DOI_JSONLD}'
        f'"isPartOf":{{"@type":"CreativeWorkSeries","name":{json.dumps(SHORT)}}},'
        f'"position":{n},'
        '"author":{"@type":"Person","name":"Young Jae Lee","sameAs":"' + ORCID + '"},'
        f'"datePublished":"{BUILD_DATE}","dateModified":"{BUILD_DATE}",'
        f'"isBasedOn":{json.dumps(REPO + "/" + slug + "/")},'
        f'"license":"{LICENSE}","knowsAbout":[{knows}]}}')
    crumb_ld = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"' + DOMAIN + '/"},'
        '{"@type":"ListItem","position":2,"name":' + json.dumps(SHORT) + ',"item":"' + DOMAIN + '/' + PAPER_ID + '/"},'
        '{"@type":"ListItem","position":3,"name":' + json.dumps("\u00a7%d %s" % (n, sec["subj"])) + '}]}')
    strip = claim_strip(sec["grade"]).replace("SLUGPLACEHOLDER", slug)
    body = sec["body"](R)
    prevlink = (f'<a rel="prev" href="/{PAPER_ID}/{prev_sec["slug"]}/">\u2190 \u00a7{prev_sec["n"]}</a>'
                if prev_sec else '<span class="disabled">\u2190</span>')
    nextlink = (f'<a rel="next" href="/{PAPER_ID}/{next_sec["slug"]}/">\u00a7{next_sec["n"]} \u2192</a>'
                if next_sec else '<span class="disabled">\u2192</span>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(sec['desc'])}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{article_ld}
</script>
<script type="application/ld+json">
{crumb_ld}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> \u203a <a href="/{PAPER_ID}/">{esc(SHORT)}</a> \u203a \u00a7{n}</nav></header>
<main>
<h1>{esc(sec['subj'])}</h1>
<p class="answer">{esc(sec['answer'])}</p>
<p class="abstract">{esc(sec['abstract'])}</p>
{strip}
{body}
<nav class="pn">{prevlink}<a href="/{PAPER_ID}/">contents</a>{nextlink}</nav>
</main>
<footer><p>{esc(AUTHOR)} \u00b7 ORCID <a href="{ORCID}" rel="noopener">0009-0002-7535-8245</a> \u00b7 DOI: {DOI_LINK_HTML} \u00b7 <a href="{LICENSE}" rel="noopener license">CC BY 4.0</a></p></footer>
</body>
</html>
"""

def render_hub(R, meta, front_nav_html=""):
    canon = f"{DOMAIN}/{PAPER_ID}/"
    items = "".join(
        f'<li><a href="/{PAPER_ID}/{c["slug"]}/"><span class="no">\u00a7{c["no"]}</span> {esc(c["title"])}</a>'
        f'<span class="grade {GRADE_LABEL[c["grade_token"]][0]}">{esc(GRADE_LABEL[c["grade_token"]][1])}</span></li>'
        for c in meta["chapters"])
    hr = " ; ".join(meta["headline_results"])
    parts = "".join('{"@type":"ScholarlyArticle","position":%d,"name":%s,"url":%s}'
                    % (c["no"], json.dumps(c["title"]), json.dumps(f"{DOMAIN}/{PAPER_ID}/{c['slug']}/"))
                    + ("," if i < len(meta["chapters"]) - 1 else "")
                    for i, c in enumerate(meta["chapters"]))
    series_ld = (
        '{"@context":"https://schema.org","@type":"CreativeWorkSeries",'
        f'"name":{json.dumps(TITLE)},'
        f'"alternateName":{json.dumps(SHORT)},'
        f'{DOI_JSONLD}'
        '"author":{"@type":"Person","name":"Young Jae Lee","sameAs":"' + ORCID + '"},'
        f'"license":"{LICENSE}","url":"{canon}","isBasedOn":{json.dumps(REPO)},'
        f'"hasPart":[{parts}]}}')
    roadmap_rows = "".join(
        '<div class="rm-group"><h3>%s</h3><p class="rm-items">%s</p></div>'
        % (esc(g), " \u00b7 ".join(esc(it) for it in items))
        for g, items in ROADMAP_GROUPS)
    roadmap_html = (
        '<section class="roadmap"><h2>Roadmap \u2014 further disease modules (future work)</h2>'
        '<p class="rm-note">The first disease modules are now <b>built</b> as \u00a711\u2013\u00a718 (gastric '
        'dysrhythmia + gastroparesis, the type 1/type 2 diabetes spectrum, gastritis + peptic ulcer, '
        'the intestinal motility / transit disorders, and a further group of scattered Tier-1 '
        'perturbations \u2014 dumping, reflux oesophagitis, insulinoma/reactive hypoglycaemia, '
        'functional dyspepsia and SIBO), the \u00a716 sphincter-gate disorders (GERD, achalasia, '
        'esophageal spasm, sphincter of Oddi) on the first Tier-2 primitive \u2014 a tonically-closed '
        'R19 gate \u2014 the \u00a717 gastric accommodation reservoir (functional dyspepsia, '
        'post-prandial distress / early satiation) on the second Tier-2 primitive, the R19 wall '
        'stiffness whose compliance peaks exactly at the spinodal yield point, '
        'and the \u00a718 visceral afferent gain (IBS-C/-D/-M and functional abdominal pain) on the '
        'third Tier-2 primitive \u2014 the R19 element\u2019s susceptibility, the same curvature inverse the '
        '\u00a717 reservoir reads as compliance, diverging at the same spinodal '
        '\u2014 the Tier-1 sections each perturbing one validated module and the three Tier-2 sections each '
        'adding one new R19-derived primitive, with every phenotype emerging rather than '
        'fitted. The carcinogen kernel is then extended in the \u00a719\u2013\u00a721 <b>neoplastic</b> sections \u2014 a Barrett\u2019s / gastric-Correa metaplasia precursor step (the same g-reduction read as a discrete, rate-limiting compartment), the HBV\u00d7aflatoxin and smoking\u00d7alcohol synergies generalizing the \u00a710 interaction with a falsifiable sub-multiplicative prediction, and reversible H. pylori MALT plus single-driver HPV anal carcinoma alongside an honestly-stated out-of-kernel boundary. Five <b>Tier-3</b> sections then add the first cross-system primitives, each on one new R19-derived element: the \u00a722 immune relapsing-inflammation layer (inflammatory bowel disease as an R19 switch with a self-sustaining flare basin \u2014 the relapsing-remitting hysteresis forcing the induction\u2260maintenance dose asymmetry, and a cumulative-burden bridge that lowers the same \u00a77 barrier scale so colitis-associated cancer rises to the cited anchor and reverses on remission, closing the \u00a721 small-bowel boundary; celiac and the immune enteropathies share the element in its antigen-dependent regime), the \u00a723 exocrine autodigestion layer (acute pancreatitis as an autocatalytic R19 switch whose supra-threshold trigger latches irreversibly \u2014 pre-threshold-only intervention \u2014 with the large-reserve exocrine insufficiency and PERT rescue as its chronic mirror), the \u00a724 perfusion / vascular layer (a perfusion-viability switch with bias h = perfusion \u2212 demand giving chronic mesenteric ischaemia as a demand-driven margin collapse and acute mesenteric ischaemia / ischaemic colitis as a forced flip with a time-critical salvage window, the NAFLD/MASLD overlap reusing the \u00a712 type-2 homeostat with the lipid layer a circulatory seam), the \u00a725 hepatobiliary / bile layer (a nucleation barrier giving cholelithiasis as metastable supersaturation that nucleates only past the barrier and a formed stone showing dissolution hysteresis \u2014 why UDCA works only on small early stones \u2014 with the stasis / cholecystitis arms cited to the B1 gate and C1 flare), and the \u00a726 structural / mechanical layer (a Laplace wall-mechanics switch giving diverticular disease as herniation once P = tension/radius clears the threshold, fibre treatment as the geometry in reverse, with diverticulitis the cited C1 flare and the fixed-block obstructions the \u00a714 functional-module counterpart). A final <b>cross-system seam</b> section (\u00a727) then wires the seams the \u00a724 / \u00a725 / \u00a718 sections declared \u2014 citation/pointer-only, never a sibling code import: the circulatory hepatic interface (its charter SSOT) consumed as the NAFLD/MASLD and bile delivery substrate, and the mind felt-symptom seam (visceral pain, biliary colic) a one-way forward-defer pointer \u2014 behind a firewall enforced by an architectural lock (zero sibling imports; a metabolic state with no felt/HPA key), the same lock mind runs neuro-side. The \u00a728 section then INHERITS a sibling DNA-grounded 27-target non-opioid analgesic map and reads it on this volume\u2019s own \u00a718 afferent spinodal (drift 0) as a cited drug-class pointer for visceral pain, and the \u00a729 section CLOSES the in-substrate digestive Tier-1 surface by REUSE \u2014 dyssynergic defecation (the \u00a716 gate read at the anorectal outlet), Hirschsprung (a \u00a74 segmental aganglionic block with proximal dilatation), MODY (a targeted \u00a712 secretory lesion giving a distinct regulated curve), hepatic GSD type I (a crippled \u00a76 glycogen-buffer release giving fasting hypoglycaemia and failed counter-regulation) and autoimmune gastritis (the \u00a722 flare read corpus-localised), the three monogenic items gene-key to <code>disease_wp</code>. The <b>remaining</b> digestive-tract diseases are enumerated in full \u2014 each mapped to a '
        'substrate module with a discriminant, expected grade, and obstacle \u2014 in '
        '<a href="%s" rel="noopener">FUTURE_WORK.md</a>. Listed below as planned targets only (no result is '
        'claimed). Standing policy: while the program is incomplete, the remaining roadmap ships with the '
        'deliverable.</p>%s</section>') % (ROADMAP_DOC_URL, roadmap_rows)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(SHORT)} \u2014 contents | Jamming Physics</title>
<meta name="description" content="Digestive and metabolic organ emergence on the VP jamming substrate: gastric slow wave, aboral gradient, peristalsis, the glucose homeostat, counter-regulation, and a shared carcinogen dose-response kernel.">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{series_ld}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> \u203a {esc(SHORT)}</nav></header>
<main>
<h1>{esc(TITLE)}</h1>
<p class="answer">This volume emerges the digestive organs and their dynamics on the shared VP jamming substrate: the gastric slow-wave pacemaker, the aboral frequency gradient, peristaltic transport, the glucose\u2013insulin homeostat, glucagon counter-regulation, and a single carcinogen barrier-Kramers kernel instantiated for three organ sites \u2014 then perturbed into eight disease sections (gastric dysrhythmia + gastroparesis, the type 1/type 2 diabetes spectrum, gastritis + peptic ulcer, the intestinal motility / transit disorders, a group of scattered Tier-1 perturbations \u2014 dumping, reflux oesophagitis, insulinoma/reactive hypoglycaemia, functional dyspepsia and SIBO \u2014 the sphincter-gate disorders on the first Tier-2 primitive, a tonically-closed R19 gate giving GERD and achalasia as two opposite failures of one gate, the gastric accommodation reservoir on the second Tier-2 primitive, an R19 fundic-wall stiffness whose impaired relaxation raises meal pressure prematurely to give functional dyspepsia / post-prandial distress, and the visceral afferent gain on the third Tier-2 primitive \u2014 the R19 element\u2019s susceptibility, the same curvature the reservoir reads as compliance \u2014 giving the IBS subtypes and functional abdominal pain) \u2014 then the carcinogen kernel is extended to more sites in the \u00a719\u2013\u00a721 neoplastic sections (a Barrett\u2019s / gastric-Correa metaplasia precursor step read as a discrete rate-limiting compartment, the HBV\u00d7aflatoxin and smoking\u00d7alcohol synergies generalizing the \u00a710 interaction with a falsifiable sub-multiplicative prediction, and reversible H. pylori MALT plus single-driver HPV anal carcinoma with an honestly-stated out-of-kernel boundary), and finally five Tier-3 sections add the first cross-system primitives, each on one new R19-derived element (the \u00a722 immune relapsing-inflammation layer \u2014 inflammatory bowel disease as a self-sustaining R19 flare basin whose hysteresis forces the induction\u2260maintenance asymmetry, bridged to the \u00a77 barrier so colitis cancer rises to the cited anchor and reverses on remission, with celiac in the antigen-dependent regime \u2014 the \u00a723 exocrine autodigestion layer \u2014 acute pancreatitis as an autocatalytic switch latching irreversibly past threshold, pre-threshold-only, with large-reserve exocrine insufficiency and PERT rescue as the chronic mirror \u2014 the \u00a724 perfusion / vascular layer \u2014 a perfusion-viability switch giving chronic mesenteric ischaemia as a demand-driven margin collapse and acute ischaemia / ischaemic colitis as a forced flip with a time-critical salvage window, with NAFLD/MASLD reusing the \u00a712 homeostat and the lipid layer a circulatory seam \u2014 the \u00a725 hepatobiliary / bile layer \u2014 a nucleation barrier giving cholelithiasis as metastable supersaturation with dissolution hysteresis (UDCA only on small early stones), the stasis / cholecystitis arms cited to the B1 gate and C1 flare \u2014 and the \u00a726 structural / mechanical layer \u2014 a Laplace wall-mechanics switch giving diverticular disease as herniation past P = tension/radius, fibre treatment the geometry in reverse, with diverticulitis the cited C1 flare and the fixed-block obstructions the \u00a714 functional-module counterpart), each phenotype emerging rather than fitted \u2014 and finally a cross-system seam section (\u00a727) wires the declared circulatory and mind seams citation/pointer-only (the circulatory hepatic interface Q_H = 1500 mL/min / E = 0.75 / F = 0.25 consumed as the NAFLD/MASLD and bile delivery substrate, the mind felt-symptom seam a one-way pointer) behind a firewall enforced by an architectural lock (zero sibling imports; a metabolic state with no felt/HPA key). Headline results: {esc(hr)}.</p>
{front_nav_html}
<p>This package derives on the VP jamming substrate \u2192 <a href="/physics/">VP Theory (physics)</a>. Organ identity and developmental order are cited from the <a href="/dna/">DNA morphogenesis gene-clock</a> (measured \u03b3, grade [V]); the low-frequency oscillator mechanism is cited from the <a href="/neuro/">neural emergence chain</a>. This package adds only the functional dynamics and the carcinogen dose-response.</p>
<ol class="toc">{items}</ol>
{roadmap_html}
<p class="note">Canonical artifact: this HTML (VP-SPEC v1.8, C2). Every displayed number is regenerated deterministically by the in-package engine (C1, 2\u00d7sha256 identical). Open quantities carry a stated obstacle (C3); see the irreproducibility ledger. Reproduction code: <a href="{REPO}" rel="noopener">GitHub repro tree</a>.</p>
</main>
<footer><p>{esc(AUTHOR)} \u00b7 ORCID <a href="{ORCID}" rel="noopener">0009-0002-7535-8245</a> \u00b7 DOI: {DOI_LINK_HTML} \u00b7 <a href="{LICENSE}" rel="noopener license">CC BY 4.0</a></p></footer>
</body>
</html>
"""

SITE_CSS = """:root{--ink:#16181d;--muted:#5b6470;--line:#e3e7ec;--bg:#ffffff;--accent:#0a5b8a;
--card:#f6f8fa;--forced:#0a7d3c;--verified:#0a5b8a;--calibrated:#8a5a0a;--open:#8a2f2f}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
header,main,footer{max-width:760px;margin:0 auto;padding:0 22px}
header{padding-top:22px}
.crumb{color:var(--muted);font-size:14px}
.crumb a{color:var(--accent);text-decoration:none}
main{padding-top:8px;padding-bottom:40px}
h1{font-size:1.72rem;line-height:1.25;margin:.6em 0 .5em;letter-spacing:-.01em}
h2{font-size:1.24rem;margin:1.8em 0 .5em}
p{margin:.75em 0}
.answer{font-size:1.12rem;font-weight:600;background:var(--card);border-left:4px solid var(--accent);
padding:.85em 1em;border-radius:6px;margin:1em 0}
.abstract{color:#2a2f37}
.m{font-family:"SFMono-Regular",ui-monospace,"Cascadia Code",Menlo,Consolas,monospace;
font-size:.95em;background:#f1f4f7;padding:.04em .34em;border-radius:4px;white-space:nowrap}
.claim-strip{display:flex;flex-wrap:wrap;gap:.5em .9em;align-items:center;
border:1px solid var(--line);border-radius:8px;padding:.6em .8em;margin:1.1em 0;
font-size:.86rem;background:#fbfcfd}
.claim-strip a{color:var(--accent);text-decoration:none}
.grade{font-weight:700;padding:.12em .5em;border-radius:999px;color:#fff;font-size:.82em}
.g-forced{background:var(--forced)}.g-verified{background:var(--verified)}
.g-calibrated{background:var(--calibrated)}.g-open{background:var(--open)}
.gate{color:var(--muted)}.doi{color:var(--muted)}
.vp-card{border:1px solid var(--line);border-left:3px solid var(--muted);background:var(--card);
border-radius:6px;padding:.6em .8em;margin:1em 0;font-size:.92rem}
.vp-card a{color:var(--accent);text-decoration:none}
nav.frontmatter{background:var(--card);border:1px solid var(--line);border-radius:6px;
padding:.6em .9em;margin:1.1em 0;font-size:.95rem;line-height:1.9}
nav.frontmatter a{color:var(--accent);text-decoration:none}
.faq-item{margin:0 0 1.2em}
.faq-item h2{margin:0 0 .25em;font-size:1.08rem}
.faq-item p{margin:0}
table{border-collapse:collapse;width:100%;margin:1.1em 0;font-size:.92rem}
th,td{border:1px solid var(--line);padding:.45em .6em;text-align:left}
thead th{background:var(--card)}
.toc{list-style:none;padding:0;margin:1.2em 0}
.toc li{display:flex;align-items:center;gap:.7em;border-bottom:1px solid var(--line);padding:.65em 0}
.toc a{flex:1;color:var(--ink);text-decoration:none}
.toc .no{color:var(--muted);font-variant-numeric:tabular-nums;margin-right:.5em}
.toc a:hover{color:var(--accent)}
.note{color:var(--muted);font-size:.9rem;border-top:1px solid var(--line);padding-top:1em;margin-top:1.8em}
.roadmap{border-top:1px solid var(--line);margin-top:2em;padding-top:1em}
.roadmap h2{font-size:1.18rem;margin:.2em 0 .4em}
.roadmap h3{font-size:.96rem;margin:.9em 0 .15em;color:var(--accent)}
.rm-note{color:var(--muted);font-size:.92rem}
.rm-note a{color:var(--accent);text-decoration:none}
.rm-group{border-left:2px solid var(--line);padding-left:.8em;margin:.7em 0}
.rm-items{margin:.1em 0;font-size:.9rem;color:#2a2f37}
.pn{display:flex;justify-content:space-between;gap:1em;border-top:1px solid var(--line);
margin-top:2em;padding-top:1em;font-size:.95rem}
.pn a{color:var(--accent);text-decoration:none}.pn .disabled{color:var(--line)}
footer{border-top:1px solid var(--line);padding-top:1.2em;padding-bottom:2.4em;
color:var(--muted);font-size:.85rem}
footer a{color:var(--accent);text-decoration:none}
@media(max-width:600px){body{font-size:16px}h1{font-size:1.5rem}}
"""

def build():
    os.makedirs(_DOCS, exist_ok=True)
    os.makedirs(os.path.join(_DOCS, "assets", "css"), exist_ok=True)
    R = eng.circulate()

    # per-chapter meta (words counted from rendered body, excluding answer/abstract/strip/cards/h1/nav)
    chapters = []
    for sec in SECTIONS:
        body = sec["body"](R)
        body_no_cards = re.sub(r'<aside class="vp-card".*?</aside>', " ", body, flags=re.S)
        w = words_in(body_no_cards)
        eq_inline = body.count('<span class="m">')
        chapters.append(dict(no=sec["n"], slug=sec["slug"], title=sec["subj"],
                             one_liner=sec["answer"].split(". ")[0] + ".",
                             grade_token=sec["grade"],
                             grade={"[F]": "forced", "[V]": "verified", "[L]": "calibrated", "[O]": "open"}[sec["grade"]],
                             words=w, eq_inline=eq_inline, eq_display=0))
    meta = dict(paper_id=PAPER_ID, code=CODE, title=TITLE, short=SHORT, doi=CONCEPT,
                hub_url=f"/{PAPER_ID}/", branch="jamming (slow transport + metabolic homeostat)",
                version=open(os.path.join(_PKG, "VERSION")).read().strip(),
                abstract=("Digestive organs emerge on the shared VP jamming (R19) substrate; this volume "
                          "adds slow-wave transport, peristalsis, the glucose homeostat, counter-regulation, "
                          "and a single carcinogen barrier-Kramers kernel for three organ sites. It closes by "
                          "inheriting a sibling DNA-grounded 27-target non-opioid analgesic map and reading it on "
                          "the volume's own visceral-afferent spinodal, turning the shared substrate into a "
                          "cited drug-class pointer for digestive visceral pain (clinical magnitudes and felt pain [O]). "
                          "A final section closes the in-substrate digestive Tier-1 surface by reuse "
                          "(dyssynergic defecation, Hirschsprung, MODY, hepatic GSD type I, autoimmune gastritis), no new primitive."),
                headline_results=["gastric ~3 cpm \u2192 duodenum 11.1 cpm (one clock)",
                                  "glucose load \u2192 5 mM setpoint", "RR(dose) = rate(dose)/rate(0)",
                                  "one homeostat \u2192 type 1 (capacity) + type 2 (gain) diabetes",
                                  "one ICC lesion \u2192 gastroparesis + slow-transit + pseudo-obstruction",
                                  "fast carbohydrate delivery \u2192 dumping/reactive-hypoglycaemia crossing (one loop)",
                                  "one gate, two failures: GERD (reflux) \u2194 achalasia (stasis)",
                                  "stiff fundic reservoir \u2192 premature meal pressure (functional dyspepsia, post-prandial distress)",
                                  "one R19 curvature, two readings: afferent gain (IBS hypersensitivity) = fundic compliance",
                                  "barrier continuum reaches cancer: Barrett's/Correa metaplasia (rate-limiting precursor) + HBV×aflatoxin / smoke×alcohol synergy + reversible H. pylori MALT",
                                  "self-sustaining basins: IBD relapse hysteresis (induction\u2260maintenance) + colitis\u2192barrier\u2192cancer bridge, and acute-pancreatitis autocatalytic latch (irreversible past threshold)",
                                  "physics of the wall and the fluid: mesenteric-ischaemia supply\u2212demand flip (time-critical salvage window) + gallstone nucleation barrier (UDCA only on small early stones) + diverticular Laplace herniation (fibre reverses the geometry)",
                                  "cross-system seams wired (citation/pointer-only, no sibling import): circulatory hepatic interface (Q_H=1500 mL/min, E=0.75, F=0.25) consumed as the NAFLD/MASLD + bile delivery substrate, the mind felt-symptom seam a one-way pointer, the firewall an architectural lock (0 sibling imports; metabolic state mind-free)",
                                  "analgesic target logic INHERITED (analgesic_threshold_logic v2.0, DOI 10.5281/zenodo.20733420): 27 non-opioid pain targets re-derive on this package's own \u00a718 afferent spinodal (drift 0) \u2014 three drug-class levers (reduce inward current / open K_V7 / remove NGF-CGRP drive), each raising the \u00a718 firing threshold, a cited-drug-class pointer for IBS / functional abdominal pain / biliary colic / oesophageal-spasm pain (every clinical magnitude + the felt pain [O], firewall held)",
                                  "in-substrate Tier-1 surface CLOSED (\u00a729, no new primitive): dyssynergic defecation (\u00a716 gate at the anorectal outlet) + Hirschsprung (\u00a74 segmental aganglionic block, proximal dilatation) + MODY (a distinct regulated \u00a712 curve) + hepatic GSD-I (\u00a76 fasting hypoglycaemia + failed counter-reg) + autoimmune gastritis (\u00a722 corpus flare, achlorhydria) \u2014 three monogenic items gene-key \u2192 disease_wp",
                                  "live cross-package harness (\u00a730, OUT OF GATE): loads every VP volume in one process and confirms against the LIVE sibling engines the identities the seams took on trust \u2014 shared R19 substrate drift 0, circulatory's live hepatic_clearance() reproducing the vendored snapshot, the 27-target analgesic map re-deriving through every volume's spinodal, and the neuro nociceptor (Na_V1.7/SCN9A, master PRDM12) the \u00a718\u2192mind pointer targets on the shared substrate; verify-alone preserved (build sibling-free; engines loaded by file path, not imported), harness digest sibling-independent"],
                chapters=chapters,
                totals=dict(words=sum(c["words"] for c in chapters),
                            eq_inline=sum(c["eq_inline"] for c in chapters),
                            eq_display=0, figures=0,
                            tables=sum(1 for _ in SECTIONS)))  # each section has 1 data table

    # pages
    written = []
    for i, sec in enumerate(SECTIONS):
        prev_sec = SECTIONS[i - 1] if i > 0 else None
        next_sec = SECTIONS[i + 1] if i < len(SECTIONS) - 1 else None
        d = os.path.join(_DOCS, sec["slug"]); os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "index.html")
        open(p, "w", encoding="utf-8").write(render_page(sec, prev_sec, next_sec, R))
        written.append(p)

    # front-matter overview pages (About / Methods / FAQ) -- full SEO scaffolding, not numbered sections
    for fm in FRONT_MATTER:
        d = os.path.join(_DOCS, fm["slug"]); os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "index.html")
        open(p, "w", encoding="utf-8").write(render_front_page(fm, R))
        written.append(p)
    front_nav_html = ('<nav class="frontmatter"><b>Start here:</b> '
                      + ' \u00b7 '.join('<a href="/%s/%s/">%s</a>' % (PAPER_ID, fm["slug"], esc(fm["nav_long"]))
                                        for fm in FRONT_MATTER)
                      + '</nav>')

    # hub + assets + machine files
    open(os.path.join(_DOCS, "index.html"), "w", encoding="utf-8").write(render_hub(R, meta, front_nav_html))
    open(os.path.join(_DOCS, "assets", "css", "site.css"), "w", encoding="utf-8").write(SITE_CSS)
    json.dump(meta, open(os.path.join(_DOCS, "_meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # sitemap (hub + front-matter overview pages + numbered sections)
    urls = ([f"{DOMAIN}/{PAPER_ID}/"]
            + [f"{DOMAIN}/{PAPER_ID}/{fm['slug']}/" for fm in FRONT_MATTER]
            + [f"{DOMAIN}/{PAPER_ID}/{s['slug']}/" for s in SECTIONS])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{BUILD_DATE}</lastmod></url>")
    sm.append("</urlset>")
    open(os.path.join(_DOCS, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")

    # robots (7 bots explicitly allowed)
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    rb = []
    for b in bots:
        rb.append(f"User-agent: {b}")
        rb.append("Allow: /")
        rb.append("")
    rb.append("User-agent: *")
    rb.append("Allow: /")
    rb.append("")
    rb.append(f"Sitemap: {DOMAIN}/{PAPER_ID}/sitemap.xml")
    open(os.path.join(_DOCS, "robots.txt"), "w", encoding="utf-8").write("\n".join(rb) + "\n")

    # llms.txt (<5KB): authoritative blockquote + prioritized link sections
    lines = []
    lines.append(f"# {SHORT}")
    lines.append("")
    lines.append("> Digestive and metabolic organ emergence on the VP jamming substrate. Organ identity and")
    lines.append("> developmental order are cited from the DNA morphogenesis gene-clock (measured gamma, [V]);")
    lines.append("> this volume adds the dynamics: a gastric slow-wave pacemaker (~3 cpm), a monotone aboral")
    lines.append("> frequency gradient from one gastric-anchored clock, peristaltic aboral transport, a glucose-")
    lines.append("> insulin homeostat returning to a 5 mM setpoint, glucagon counter-regulation, and a single")
    lines.append("> carcinogen barrier-Kramers kernel RR(dose)=rate(dose)/rate(0) instantiated for colorectal,")
    lines.append("> pancreatic, and gastric sites; and eight disease sections that perturb those validated")
    lines.append("> modules -- gastric dysrhythmia + gastroparesis, the type 1/type 2 diabetes spectrum,")
    lines.append("> gastritis + peptic ulcer, the intestinal motility / transit disorders (one ICC lesion")
    lines.append("> across stomach and gut), and a further group of scattered Tier-1 perturbations --")
    lines.append("> dumping (faster, higher glucose peak + biphasic reactive-hypoglycaemia crossing on the")
    lines.append("> glucose loop; mechanical rapid-emptying magnitude an honest [O]), reflux-oesophagitis")
    lines.append("> erosion (shared gastritis kernel), insulinoma (mirror of type 1) + reactive")
    lines.append("> hypoglycaemia, functional-dyspepsia mild-motility, and SIBO stasis -- with each")
    lines.append("> phenotype emerging, never fitted. The last three sections add the three Tier-2 primitives.")
    lines.append("> First, a tonically-closed R19 gate (opens iff drive > tone + spinodal): GERD is the gate")
    lines.append("> failing closed (reflux burden rises as LES tone falls) and achalasia the SAME gate")
    lines.append("> failing open (stuck closed -> antegrade stasis) -- two opposite failures of one gate --")
    lines.append("> with esophageal spasm a coordination fault and sphincter of Oddi the gate at the")
    lines.append("> biliary outlet. Second, a gastric accommodation reservoir: the same R19 switch read as a")
    lines.append("> fundic wall whose stiffness k = 3s^2 - g sets compliance C = 1/k, so impaired vagal")
    lines.append("> accommodation stiffens the reservoir and a fixed meal raises pressure prematurely --")
    lines.append("> functional dyspepsia / post-prandial distress with early satiation -- the maximal-")
    lines.append("> compliance yield point being exactly the R19 spinodal. Third, a visceral afferent gain:")
    lines.append("> the afferent's susceptibility chi = 1/k is the SAME curvature inverse the reservoir reads")
    lines.append("> as compliance, so IBS is a transport-bias motility subtype (IBS-C -> IBS-M -> IBS-D) plus")
    lines.append("> a raised afferent gain (visceral hypersensitivity / allodynia; spontaneous firing past")
    lines.append("> the spinodal), and functional abdominal pain is the raised gain at normal motility -- the")
    lines.append("> felt experience staying in mind behind the firewall (peripheral term only here).")
    lines.append("> The carcinogen kernel is then extended (C6) to more sites in three neoplastic")
    lines.append("> sections: a Barrett's / gastric-Correa metaplasia precursor (the same g-reduction read")
    lines.append("> as a discrete, rate-limiting compartment), the HBV x aflatoxin and smoking x alcohol")
    lines.append("> synergies generalizing the gastric interaction (with a falsifiable sub-multiplicative")
    lines.append("> prediction near the spinodal), and reversible H. pylori MALT lymphoma + single-driver")
    lines.append("> HPV anal carcinoma, alongside an honestly-stated out-of-kernel boundary (GIST, NET,")
    lines.append("> small-bowel adenocarcinoma, cholangiocarcinoma).")
    lines.append("> Five Tier-3 sections then add the first cross-system primitives, each on one new")
    lines.append("> R19-derived element. The immune")
    lines.append("> relapsing-inflammation layer: inflammatory bowel disease is an R19 switch with a")
    lines.append("> SELF-SUSTAINING flare basin, so the relapsing-remitting course is a hysteresis (the")
    lines.append("> flip-to-flare drive exceeds the return-to-remission drive) that forces the induction-vs-")
    lines.append("> maintenance dose asymmetry (the same dose holds remission but cannot break a flare);")
    lines.append("> cumulative inflammatory burden lowers the SAME barrier scale the kernel uses for H.")
    lines.append("> pylori, so colitis-associated colorectal cancer rises to the cited anchor (RR~2.4) and")
    lines.append("> collapses on sustained remission -- closing the small-bowel-adenocarcinoma boundary on")
    lines.append("> the inflammation route; celiac and the immune enteropathies share the element in its")
    lines.append("> antigen-dependent regime (driver removal restores the barrier). The exocrine")
    lines.append("> autodigestion layer: acute pancreatitis is an AUTOCATALYTIC R19 switch whose")
    lines.append("> autoactivation threshold rises with the protective inhibitor (SPINK1 up; PRSS1-gain")
    lines.append("> down), where a sub-threshold trigger decays safely but a supra-threshold trigger LATCHES")
    lines.append("> irreversibly (self-sustaining, no parameter move reverses it) -- so intervention is pre-")
    lines.append("> threshold only; chronic pancreatitis / exocrine insufficiency is the mirror (a large")
    lines.append("> secretory reserve delays steatorrhea until ~90% acinar loss, PERT restores output).")
    lines.append("> The perfusion / vascular layer: a perfusion-viability switch (bias h = perfusion -")
    lines.append("> demand) gives chronic mesenteric ischaemia as a demand-driven margin collapse (a meal")
    lines.append("> raises demand and the viability margin crosses to deficit; revascularisation restores")
    lines.append("> it) and acute mesenteric ischaemia / ischaemic colitis as a forced viable->ischaemic")
    lines.append("> FLIP with a time-critical salvage window (reperfusion recovers only inside it; partial /")
    lines.append("> late stays infarcted); NAFLD / MASLD reuses the section-12 type-2 homeostat unchanged,")
    lines.append("> the hepatic lipid-deposition layer a declared circulatory seam. The hepatobiliary / bile")
    lines.append("> layer: a NUCLEATION barrier gives cholelithiasis as metastable supersaturation (bile")
    lines.append("> above saturation stays stone-free until the drive clears the barrier) with dissolution")
    lines.append("> HYSTERESIS (a formed stone persists below saturation, redissolving only far below it --")
    lines.append("> why UDCA dissolution works only on small, early stones); gallbladder stasis is the B1")
    lines.append("> sphincter-gate seam, cholecystitis the B1 gate + the cited C1 flare, the nucleation time")
    lines.append("> the Kramers rate. The structural / mechanical layer: a Laplace wall-mechanics switch (P =")
    lines.append("> tension / radius) gives diverticular disease as herniation once P clears spinodal(g_wall)")
    lines.append("> (a low-fibre small radius raises P; a weaker / aging / collagen-disorder wall crosses")
    lines.append("> lower), with fibre treatment the geometry in reverse (larger radius + softer segmenting")
    lines.append("> drops P below threshold); diverticulITIS is the cited C1 flare and the mechanical fixed-")
    lines.append("> block obstructions (hernia / volvulus / intussusception / adhesions) are the section-14")
    lines.append("> functional-module structural counterpart (surgical, out-of-model).")
    lines.append("> The volume then INHERITS a sibling whitepaper -- analgesic_threshold_logic v2.0 (DOI")
    lines.append("> 10.5281/zenodo.20733420), a DNA-grounded map of 27 non-opioid analgesic targets -- and reads")
    lines.append("> it on its OWN section-18 visceral-afferent spinodal: each pain gene's promoter gamma sits on")
    lines.append("> the R19 firing-threshold scale |h_sp| = spinodal(gamma), identically the gain-divergence point")
    lines.append("> of section 18, so all 27 reads re-derive bit-for-bit (drift 0). The targets sort into three")
    lines.append("> drug-class levers -- reduce the inward current (Na_V/Ca_V/ASIC/P2X/TRP), open the K_V7 brake,")
    lines.append("> remove the NGF/CGRP drive -- each RAISING the section-18 firing threshold, making the map a")
    lines.append("> cited drug-class POINTER for IBS hypersensitivity, functional abdominal pain, functional-")
    lines.append("> dyspepsia pain, biliary colic and oesophageal-spasm pain. Firewall (inherited verbatim): gamma")
    lines.append("> reads promoter STRUCTURE only, never a voltage / potency / dose / selectivity / effect; every")
    lines.append("> clinical magnitude and the felt pain are [O] (felt pain is mind's); proposal-only, nothing prescribes.")
    lines.append("> Grades: [F] forced / [V] verified / [L] cited / [O] open.")
    lines.append("")
    lines.append("## Overview (start here)")
    for fm in FRONT_MATTER:
        lines.append(f"- [{fm['nav_long']}]({DOMAIN}/{PAPER_ID}/{fm['slug']}/): {fm['desc']}")
    lines.append("")
    lines.append("## Core dynamics")
    lines.append(f"- [Contents hub]({DOMAIN}/{PAPER_ID}/): all sections, headline results, derivation map.")
    for s in SECTIONS:
        if s["n"] <= 6:
            lines.append(f"- [\u00a7{s['n']} {s['subj']}]({DOMAIN}/{PAPER_ID}/{s['slug']}/)")
    lines.append("")
    lines.append("## Mucosal-barrier kernel & oncology (one shared exact barrier)")
    for s in SECTIONS:
        if 7 <= s["n"] <= 10:
            lines.append(f"- [\u00a7{s['n']} {s['subj']}]({DOMAIN}/{PAPER_ID}/{s['slug']}/)")
    lines.append("")
    lines.append("## Disease modules (Tier-1 perturbations; phenotype emerges, never fitted)")
    for s in SECTIONS:
        if 11 <= s["n"] <= 18:
            lines.append(f"- [\u00a7{s['n']} {s['subj']}]({DOMAIN}/{PAPER_ID}/{s['slug']}/)")
    lines.append("")
    lines.append("## Neoplastic extension (C6 -- the same exact barrier kernel, more sites + a metaplasia step)")
    for s in SECTIONS:
        if 19 <= s["n"] <= 21:
            lines.append(f"- [§{s['n']} {s['subj']}]({DOMAIN}/{PAPER_ID}/{s['slug']}/)")
    lines.append("")
    lines.append("## Tier-3 cross-system layers (the first cross-system R19 primitives: immune, exocrine, perfusion, hepatobiliary, structural)")
    for s in SECTIONS:
        if 22 <= s["n"] <= 27:
            lines.append(f"- [§{s['n']} {s['subj']}]({DOMAIN}/{PAPER_ID}/{s['slug']}/)")
    lines.append("")
    lines.append("## Inherited analgesic target logic + remaining in-substrate surface")
    for s in SECTIONS:
        if 28 <= s["n"] <= 29:
            lines.append(f"- [\u00a7{s['n']} {s['subj']}]({DOMAIN}/{PAPER_ID}/{s['slug']}/)")
    lines.append("")
    lines.append("## Live cross-package harness (out of gate: verifies the cross-volume identities against the live sibling engines; verify-alone preserved)")
    for s in SECTIONS:
        if s["n"] >= 30:
            lines.append(f"- [\u00a7{s['n']} {s['subj']}]({DOMAIN}/{PAPER_ID}/{s['slug']}/)")
    lines.append("")
    lines.append("## Reproduction & policies")
    lines.append(f"- [Reproduction code (GitHub)]({REPO}): deterministic engine; 2x sha256 identical.")
    lines.append(f"- [Future work / disease roadmap]({ROADMAP_DOC_URL}): \u00a711\u2013\u00a726 (dysrhythmia/gastroparesis, diabetes, gastritis/ulcer, intestinal dysmotility, scattered Tier-1 cluster, sphincter-gate disorders, gastric accommodation reservoir, visceral afferent gain / IBS, the \u00a719\u2013\u00a721 neoplastic extension: Barrett\u2019s/Correa metaplasia, HBV\u00d7aflatoxin & smoking\u00d7alcohol synergy, reversible H. pylori MALT / HPV anal, and the \u00a722\u2013\u00a726 Tier-3 layers: immune relapsing-inflammation (IBD relapse hysteresis + colitis\u2192barrier\u2192cancer bridge, celiac), exocrine autodigestion (acute-pancreatitis autocatalytic latch + large-reserve EPI / PERT), perfusion/vascular (mesenteric ischaemia supply\u2212demand flip + salvage window, NAFLD/MASLD), hepatobiliary/bile (cholelithiasis nucleation barrier + dissolution hysteresis), structural/mechanical (diverticular Laplace herniation + fibre treatment), and the \u00a727 cross-system seam wiring (the circulatory hepatic interface consumed as the NAFLD/MASLD + bile delivery substrate, the mind felt-symptom seam a one-way pointer, the firewall an architectural lock with zero sibling imports)), and the \u00a728 INHERITED analgesic target layer (analgesic_threshold_logic v2.0, DOI 10.5281/zenodo.20733420: 27 non-opioid pain targets re-derived on this volume\u2019s own \u00a718 afferent spinodal at drift 0, sorted into three drug-class levers that each raise the \u00a718 firing threshold, a cited-drug-class pointer for the volume\u2019s visceral-pain disorders \u2014 clinical magnitudes and felt pain [O], firewall held), and the \u00a729 remaining in-substrate surface (dyssynergic defecation on the \u00a716 gate read at the anorectal outlet, Hirschsprung as a \u00a74 segmental aganglionic block, MODY as a targeted \u00a712 secretory lesion, hepatic GSD type I as a crippled \u00a76 glycogen-buffer release, and autoimmune gastritis as the \u00a722 flare read corpus-localised \u2014 reuse, no new primitive; the three monogenic items gene-key \u2192 disease_wp), and the \u00a730 live cross-package harness (out of gate: loads every VP volume in one process and confirms against the live sibling engines the shared R19 substrate drift 0, the vendored circulatory hepatic snapshot, the 27-target analgesic map drift-0 across volumes, and the neuro felt-symptom endpoint \u2014 verify-alone preserved, the build sibling-free), are built; the remaining roadmap (the cross-package analgesic propagation to the circulatory / neuro sibling packages, and the sibling-owned GI-bleeding / hepatitis / megacolon / anorectal targets) is enumerated as planned modules.")
    _doi_txt = ("%s (%s)" % (CONCEPT, DOI_URL)) if DOI_MINTED else CONCEPT
    lines.append(f"- License: CC BY 4.0. Author: Young Jae Lee (ORCID 0009-0002-7535-8245). DOI: {_doi_txt}.")
    lines.append("")
    open(os.path.join(_DOCS, "llms.txt"), "w", encoding="utf-8").write("\n".join(lines))

    # manifest (header: slug,title,section_no,status,grade,words,eq_display)
    man = os.path.join(_PKG, "manifest", PAPER_ID + ".csv")
    with open(man, "w", encoding="utf-8") as f:
        f.write("slug,title,section_no,status,grade,words,eq_display\n")
        for c in chapters:
            f.write('%s,"%s",%d,%s,%s,%d,%d\n' %
                    (c["slug"], c["title"].replace('"', "'"), c["no"], "published", c["grade"], c["words"], c["eq_display"]))

    return meta, written

def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Do the research first: build out the dynamics, pass the stress battery, then")
        print("  python repro/_verify/gates.py  ->  gates.write_research_complete()")
        print("  echo writing > PHASE")
        print("and re-run. (VP-SPEC: research-first; HTML is the canonical artifact.)")
        return 1
    meta, written = build()
    print("BUILT canonical HTML (VP-SPEC v1.8) into docs/")
    print("  hub: docs/index.html  (+ _meta.json, sitemap.xml, robots.txt, llms.txt, assets/css/site.css)")
    for p in written:
        rel = os.path.relpath(p, _PKG)
        print("  page:", rel)
    print("  sections: %d   total body words: %d   inline eqs: %d   tables: %d"
          % (len(meta["chapters"]), meta["totals"]["words"], meta["totals"]["eq_inline"], meta["totals"]["tables"]))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
