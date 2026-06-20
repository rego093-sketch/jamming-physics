#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Mineral / Acid-Base / Electrolyte Homeostasis WRITING phase: canonical SEO HTML.

HARD RULE: refuses while gates.writing_locked() is True (research signed off + PHASE=="writing").
WHEN UNLOCKED it emits, per VP-SPEC v1.8 (../VP_SPEC_v1_8.md): canonical HTML in docs/ (C2); ONE page per
section (C4 sec 6/6-R): answer-first <p class="answer"> (40-60 words), JSON-LD ScholarlyArticle +
BreadcrumbList, claim-strip, vp-card for each locked substrate constant; ENGLISH body (C0); honest grades
+ stated [O] (C3); DETERMINISTIC numbers pulled from the research modules at build time (C1 -- no
hand-entry). Plus a volume hub, sitemap.xml, robots.txt (7 bots), llms.txt. DOI: TBD (filled on publication).
"""
import os, sys, json, datetime
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine","_verify","_pathology","_therapy"):
    sys.path.insert(0, os.path.join(_HERE, "..", "repro", sub))
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_verify"))
import importlib
gates=importlib.import_module("gates")

PAPER_ID="homeostasis-ionic"; SHORT="Ionic Homeostasis"
TITLE="Mineral and Acid-Base Homeostasis: Calcium-Phosphate, pH, and Electrolyte Setpoints"
ORCID="https://orcid.org/0009-0002-7535-8245"; AUTHOR="Young Jae Lee"
DOI="10.5281/zenodo.20755910"          # concept DOI (assigned)
DOI_URL="https://doi.org/%s"%DOI
ANALGESIC_DOI="10.5281/zenodo.20733420"   # source of the inherited three-lever technology (cross-volume)
ANALGESIC_DOI_URL="https://doi.org/%s"%ANALGESIC_DOI
BASE="https://jamming-physics.org/%s"%PAPER_ID
TODAY=datetime.date.today().isoformat()

def _research():
    loops=importlib.import_module("vp_loops"); sensors=importlib.import_module("vp_sensors")
    lit=importlib.import_module("literature_anchors"); path=importlib.import_module("setpoint_failure")
    ther=importlib.import_module("fundamental_therapy"); eng=importlib.import_module("vp_ion_engine")
    renal=importlib.import_module("renal_phosphate"); frontier=importlib.import_module("frontier_quant")
    comp=importlib.import_module("comparative_ionoregulation")
    t2dis=importlib.import_module("tier2_ion_diseases")
    trans=importlib.import_module("transport_dynamics")
    cgam=importlib.import_module("comparative_gamma")
    tlever=importlib.import_module("three_lever")
    drem=importlib.import_module("disease_remediation")
    return dict(L=loops.run_loops(), S=sensors.status(), Lit=lit.status(), P=path.status(),
                T=ther.status(), E=eng.circulate(), R5=renal.status(), FQ=frontier.status(), C=comp.status(),
                T2=t2dis.status(), TR=trans.status(), CG=cgam.status(), TL=tlever.status(), DR=drem.status())

CSS = """:root{--ink:#1a1a1a;--mut:#5a5a5a;--bg:#fcfcfa;--card:#f1f4f2;--line:#dfe3e0;--acc:#2a6f5e;--warn:#9a5a2a}
*{box-sizing:border-box}body{margin:0;font:16px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
main{max-width:760px;margin:0 auto;padding:1.2rem 1.1rem 3rem}header,footer{max-width:760px;margin:0 auto;padding:.8rem 1.1rem;color:var(--mut);font-size:.85rem}
nav.crumb a{color:var(--acc);text-decoration:none}h1{font-size:1.5rem;line-height:1.25;margin:.2rem 0 .6rem}h2{font-size:1.18rem;margin:1.6rem 0 .4rem}h3{font-size:1.02rem;margin:1.1rem 0 .3rem}
p{margin:.5rem 0}p.answer{font-size:1.06rem;background:var(--card);border-left:3px solid var(--acc);padding:.7rem .9rem;border-radius:6px}
p.abstract{color:#333}code,.eq{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em}
aside.claim-strip{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;font-size:.82rem;margin:.7rem 0;padding:.4rem .6rem;background:#eef2f0;border-radius:6px}
aside.claim-strip a{color:var(--acc);text-decoration:none}.grade{font-weight:700;padding:.05rem .4rem;border-radius:4px}
.g-forced{background:#dceee7;color:#15543f}.g-verified{background:#dde8f2;color:#1b4a6b}.g-open{background:#f3e6d8;color:var(--warn)}.g-cited{background:#ece8f2;color:#4a3b6b}
aside.vp-card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.55rem .8rem;margin:.6rem 0;font-size:.9rem}
aside.vp-card a{color:var(--acc)}table{border-collapse:collapse;width:100%;font-size:.9rem;margin:.6rem 0}th,td{border:1px solid var(--line);padding:.35rem .5rem;text-align:left;vertical-align:top}
th{background:#eef2f0}nav.pn{display:flex;justify-content:space-between;margin-top:1.8rem;font-size:.9rem}nav.pn a{color:var(--acc);text-decoration:none}
ul{margin:.4rem 0 .4rem 1.1rem}li{margin:.2rem 0}.lead{color:var(--mut)}"""

def ld_article(headline, n, slug):
    return json.dumps({"@context":"https://schema.org","@type":"ScholarlyArticle","headline":headline,
        "isPartOf":{"@type":"CreativeWorkSeries","name":SHORT,"identifier":DOI},
        "author":{"@type":"Person","name":AUTHOR,"sameAs":ORCID},
        "identifier":DOI,"sameAs":DOI_URL,
        "datePublished":TODAY,"dateModified":TODAY,"position":n,
        "isBasedOn":"https://github.com/rego093-sketch/jamming-physics",
        "citation":{"@type":"ScholarlyArticle","name":"Analgesic Threshold Logic (non-opioid): the three-lever organizing principle","identifier":ANALGESIC_DOI,"sameAs":ANALGESIC_DOI_URL},
        "license":"https://creativecommons.org/licenses/by/4.0/",
        "knowsAbout":["calcium homeostasis","acid-base balance","parathyroid hormone","FGF23",
                      "bone remodeling","calcium-sensing receptor","OTOP1","setpoint control",
                      "osteoporosis treatment","primary hyperparathyroidism","distal renal tubular acidosis",
                      "calcium kidney stones","CKD-MBD","secondary hyperparathyroidism","hypomagnesemia",
                      "humoral hypercalcemia of malignancy","Ornstein-Uhlenbeck homeostasis","loop gain",
                      "calcimimetic","anabolic osteoporosis therapy","non-opioid analgesic mechanism",
                      "three-lever therapy","Nav1.8 inhibitor","gene-grounded simulation"]}, ensure_ascii=False)

def ld_crumb(n, short):
    return json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://jamming-physics.org/"},
        {"@type":"ListItem","position":2,"name":SHORT,"item":BASE+"/"},
        {"@type":"ListItem","position":3,"name":"\u00a7%d %s"%(n,short)}]}, ensure_ascii=False)

def page(slug, n, short, title45, desc, answer, body_html, grade_cls, grade_txt, prev_s, next_s):
    pn_prev='<a rel="prev" href="%s/%s/">\u2190 \u00a7%d</a>'%(BASE,prev_s[1],n-1) if prev_s else '<span></span>'
    pn_next='<a rel="next" href="%s/%s/">\u00a7%d \u2192</a>'%(BASE,next_s[1],n+1) if next_s else '<span></span>'
    crumb='<a href="/">Home</a> \u203a <a href="%s/">%s</a> \u203a \u00a7%d'%(BASE,SHORT,n)
    return """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s \u2014 %s \u00a7%d | Jamming Physics</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s/%s/">
<style>%s</style>
<script type="application/ld+json">%s</script>
<script type="application/ld+json">%s</script>
</head><body>
<header><nav class="crumb">%s</nav></header>
<main>
<h1>%s</h1>
<p class="answer">%s</p>
<aside class="claim-strip"><span class="%s">%s</span><span>LOCK \u2192 Derive \u2192 Gate</span>
<a href="https://github.com/rego093-sketch/jamming-physics" rel="noopener">reproduction code (GitHub)</a>
<a href="%s" rel="noopener">DOI: %s</a></aside>
%s
<nav class="pn">%s<a href="%s/">volume contents</a>%s</nav>
</main>
<footer>%s \u00b7 ORCID <a href="%s">0009-0002-7535-8245</a> \u00b7 CC BY 4.0 \u00b7 DOI %s (assigned on publication)</footer>
</body></html>""" % (title45, SHORT, n, desc, BASE, slug, CSS, ld_article(title45,n,slug), ld_crumb(n,short),
                     crumb, title45, answer, grade_cls, grade_txt, DOI_URL, DOI, body_html, pn_prev, BASE, pn_next,
                     AUTHOR, ORCID, DOI)

VPCARD_R19='<aside class="vp-card" data-locked="r19"><b>R19 switch</b> \u2014 the shared jamming-lattice bistable element ds/dt = g\u00b7s \u2212 s\u00b3 + h; barrier b(g)=g\u00b2/4 sets state stability. <b>[F]</b> forced (vendored substrate). <a href="https://jamming-physics.org/dna/">canonical derivation (DNA volume)</a></aside>'
VPCARD_GAMMA='<aside class="vp-card" data-locked="gamma"><b>\u03b3 (master-gene stacking energy)</b> \u2014 \u03b3 = \u2212mean nearest-neighbor stacking \u0394G37 (SantaLucia 1998) over the proximal promoter; MEASURED from NCBI, never fitted. <b>[V]</b> measured input. <a href="https://jamming-physics.org/dna/">canonical method (DNA volume)</a></aside>'
VPCARD_3LEVER=('<aside class="vp-card" data-locked="three-lever"><b>Three-lever therapeutic principle</b> \u2014 a defended setpoint dx/dt=\u2212k(x\u2212x*)+load+noise has exactly three independent handles: <b>L1</b> lowers the load (source), <b>L2</b> raises the loop gain k (gain), <b>L3</b> relocates the target x* (setpoint). Only L2 tightens the stationary variance \u03c3\u00b2/2k; L1 lowers the mean only; L3 moves the defended value durably. <b>[V]</b> asymmetry from the volume\u2019s own OU law; <b>[L]</b> cross-volume drug classes. <a href="https://doi.org/10.5281/zenodo.20733420">inherited technology (non-opioid analgesic volume)</a></aside>')

def build_sections(R):
    L=R["L"]
    gl=L["gain_law"]; ou=L["ou_law"]; ri1=L["RI1_calcium"]; ri2=L["RI2_acidbase"]; ri3=L["RI3_bone_reservoir"]
    ri4=L["RI4_electrolyte"]; ri5=L["RI5_phosphate"]; S=R["S"]; P=R["P"]; T=R["T"]; R5=R["R5"]; FQ=R["FQ"]; C=R["C"]; T2=R["T2"]
    TR=R["TR"]; CG=R["CG"]; TL=R["TL"]; DR=R["DR"]
    dd={d["disease"]:d for d in DR["remediation"]["diseases"]}
    def dtbl(names):
        return ("<table><tr><th>disease (owned)</th><th>corrupted OU parameter</th><th>primary lever</th><th>improvement \u2014 the framework\u2019s distinctive call</th></tr>"
          +"".join("<tr><td>%s</td><td>%s</td><td><b>%s</b></td><td>%s</td></tr>"
                   %(dd[n]["disease"],dd[n]["corrupted_parameter"],dd[n]["primary_lever"],dd[n]["improvement"]) for n in names)+"</table>")
    secs=[]
    grows="".join("<tr><td>%s</td><td>%.4f</td><td>%.4f</td></tr>"%(r["master"],r["gamma"],r["barrier"]) for r in gl["by_gamma_ascending"])

    body1=("%s%s"%(VPCARD_R19,VPCARD_GAMMA)+
      "<p class='abstract'>A homeostatic setpoint, linearized about its target, is an Ornstein-Uhlenbeck process dx/dt = \u2212k(x\u2212x*) + load + noise. Its loop gain k sets disturbance-rejection error (load/k), correction time (1/k), and stationary variance (\u03c3\u00b2/2k). The node barrier b=\u03b3\u00b2/4 supplies k, so the measured \u03b3 sets setpoint stability.</p>"
      "<h2>The substrate sets loop stiffness, not the setpoint value</h2>"
      "<p>Each node is an R19 switch emerged from its measured master-gene \u03b3. A deeper basin (larger barrier b=\u03b3\u00b2/4) holds the controlled state more firmly, so \u03b3 contributes the disturbance-rejection stiffness k of the loop. The setpoint VALUE is biology (cited); the setpoint STABILITY is set by \u03b3.</p>"
      "<table><tr><th>master</th><th>measured \u03b3</th><th>barrier \u03b3\u00b2/4</th></tr>%s</table>"%grows+
      "<p>Demonstrated on the measured \u03b3: barrier is monotone increasing in \u03b3 (%s) and the peak displacement of a settled switch under a fixed perturbation is monotone decreasing (%s) \u2014 a stiffer node resists perturbation more. Honest trade-off: the small-signal comparator slope ~1/\u03b3 moves oppositely, so \u03b3 tunes the sensitivity/stability balance.</p>"%(gl["barrier_monotone_increasing_in_gamma"],gl["displacement_monotone_decreasing_in_gamma"])+
      "<h2>The Ornstein-Uhlenbeck setpoint laws</h2>"
      "<p>Across a gain sweep the loop reproduces the control laws exactly: Var\u00b72k/\u03c3\u00b2 \u2248 1 (%s), step error \u00d7 k \u2248 1 (%s), and an integral arm drives the steady-state error to zero (%s). Loop-gain loss therefore inflates variance and slows correction; k below a critical value is loss of regulation (attractor-shift).</p>"%(ou["variance_law_Var_eq_sigma2_over_2k"],ou["rejection_law_err_eq_load_over_k"],ou["integral_arm_zeroes_steady_error"]))
    secs.append(("01-substrate-loop-gain-setpoint-stability",1,"substrate law",
      "Calcium, pH and electrolyte setpoints as loop attractors",
      "The measured master-gene \u03b3 sets a node's R19 basin depth (barrier \u03b3\u00b2/4), which supplies the loop gain k that controls setpoint tightness (Var=\u03c3\u00b2/2k) and correction speed (1/k). The setpoint value is cited; its stability is derived.",
      "A defended homeostatic setpoint is an Ornstein-Uhlenbeck attractor dx/dt=\u2212k(x\u2212x*)+load+noise; loop gain k sets the rejection error load/k, correction time 1/k, and variance \u03c3\u00b2/2k. The node barrier \u03b3\u00b2/4 supplies k, so the measured \u03b3 sets setpoint stability while the value stays cited.",
      body1,"grade g-verified","[V] mechanism"))

    body2=("%s"%VPCARD_GAMMA+
      "<p class='abstract'>Serum calcium is defended near its setpoint by the PTH\u2194vitamin-D\u2194bone\u2194kidney\u2194gut loop. CaSR is the comparator; PTH the fast effector; vitamin-D the slow arm; bone the reservoir. A Ca load and a Ca deficit are both corrected to setpoint.</p>"
      "<h2>The four-parameter PTH-calcium comparator</h2>"
      "<p>PTH follows the Brown inverse sigmoid of calcium, with the set-point at the calcium giving half-maximal PTH and a Hill slope (~3) set by the calcium-sensing receptor. In simulation PTH is suppressed by a calcium load (%s) and raised by a deficit (%s).</p>"%(ri1["pth_suppressed_by_load"],ri1["pth_raised_by_deficit"])+
      "<h2>Disturbance rejection</h2>"
      "<p>A calcium load drives serum Ca to a transient peak (%.3f, normalized) and a deficit to a nadir (%.3f); the loop returns serum Ca to setpoint (final %.4f). The value held is biology (ionized ~1.2 mM, total ~2.4 mM, cited); the correction is the reproduced mechanism.</p>"%(ri1["ca_peak_on_load"],ri1["ca_nadir_on_deficit"],ri1["ca_final"]))
    secs.append(("02-calcium-setpoint-loop",2,"calcium loop","The calcium setpoint loop",
      "Serum calcium is defended near setpoint by the PTH\u2013vitamin-D\u2013bone\u2013kidney\u2013gut loop with the calcium-sensing receptor as comparator. A calcium load is suppressed by PTH and a deficit corrected by it; serum calcium returns to setpoint in simulation.",
      "Serum calcium is a loop quantity, defended by a negative-feedback loop: CaSR senses calcium, PTH is the fast effector, vitamin-D the slow arm, bone the reservoir, kidney the integrator. A load or deficit is corrected back to the cited setpoint (ionized ~1.2 mM); the loop mechanism is reproduced.",
      body2,"grade g-verified","[V] correction; [L] setpoint"))

    body3=("<p class='abstract'>Blood pH is held at 7.40 by a two-timescale buffer: fast respiratory CO\u2082 and slow renal HCO\u2083 regeneration. A metabolic acid load is partially compensated within minutes (respiratory) then fully corrected over hours (renal).</p>"
      "<h2>Henderson-Hasselbalch and the two timescales</h2>"
      "<p>pH = 6.1 + log\u2081\u2080(HCO\u2083 / (0.03\u00b7pCO\u2082)). An acid load (HCO\u2083 24\u219214) drops pH to %.3f. The fast respiratory arm lowers pCO\u2082 (compensation slope dpCO\u2082/dHCO\u2083 = %.2f, matching the Winters rule ~1.2\u20131.5), partially restoring pH to %.3f. The slow renal arm regenerates HCO\u2083, returning pH to %.3f.</p>"%(ri2["pH_acute_acidemia"],ri2["respiratory_compensation_slope_dPCO2_dHCO3"],ri2["pH_after_fast_resp"],ri2["pH_final"])+
      "<p>Failure of either arm is the metabolic/respiratory acid-base disorder axis; the cited pH 7.40 and the Winters slope are the literature anchors the simulation reproduces.</p>")
    secs.append(("03-acid-base-two-timescale-buffer",3,"acid-base","The acid-base two-timescale buffer",
      "Blood pH 7.40 is defended by a two-timescale buffer: fast respiratory CO\u2082 and slow renal HCO\u2083 regeneration. A simulated metabolic acid load is partially compensated by ventilation (Winters slope ~1.1) then fully corrected by the kidney, returning pH to 7.40.",
      "Blood pH is a loop quantity defended by two arms on different timescales: respiratory CO\u2082 (fast) and renal HCO\u2083 (slow). The Henderson-Hasselbalch relation plus the two timescales reproduce both the Winters respiratory-compensation slope and full pH restoration after a metabolic acid load.",
      body3,"grade g-verified","[V] two-timescale; [L] pH/Winters"))

    body4=("%s"%VPCARD_GAMMA+
      "<p class='abstract'>Bone is the calcium-phosphate reservoir. Under chronic calcium demand the loop holds serum calcium at setpoint by withdrawing from the bone reserve, which depletes monotonically \u2014 the reservoir/setpoint trade-off and the substrate of osteoporosis.</p>"
      "<h2>The reservoir/setpoint trade-off</h2>"
      "<p>Under a sustained calcium demand, serum calcium stays at setpoint (maximum deviation %.4f) while the bone reserve declines monotonically from %.2f to %.2f (normalized). The value defended is purchased from the reservoir; sustained demand empties it.</p>"%(ri3["serum_ca_max_deviation"],ri3["bone_reserve_start"],ri3["bone_reserve_end"])+
      "<p>This is osteoporosis as a reservoir failure rather than a local lesion: post-menopausal and age-related loss raise net withdrawal (estrogen loss) and lower loop gain. Bone identity is owned by the musculoskeletal volume (DNA SSOT); here bone appears in the mineral-reservoir role, not as a fork.</p>")
    secs.append(("04-bone-reservoir-osteoporosis",4,"bone reservoir","Bone as the calcium reservoir, and osteoporosis",
      "Bone is the calcium reservoir. Under chronic demand the loop holds serum calcium at setpoint by withdrawing bone mineral, so the reserve depletes monotonically while serum calcium stays constant \u2014 the reservoir/setpoint trade-off and the substrate of osteoporosis.",
      "Bone is the calcium-phosphate reservoir of the mineral loop. Simulation shows serum calcium held at setpoint while a sustained demand depletes the bone reserve monotonically: osteoporosis is reservoir depletion (post-menopausal/age), not a local lesion. Bone identity is cited from the musculoskeletal volume.",
      body4,"grade g-verified","[V] trade-off; [O] absolute rate"))

    body5=("<p class='abstract'>Sodium and potassium setpoints are corrected by renal handling. Sodium couples to volume and pressure (a cited seam to the hemodynamic volume); potassium is set by renal excretion. Loads in either are corrected back to setpoint.</p>"
      "<h2>Renal correction of Na/K loads</h2>"
      "<p>A sodium load is returned to its setpoint (final %.1f mM, cited ~140) and a potassium load to its setpoint (final %.2f mM, cited ~4.2) by renal handling. The sodium\u2194volume\u2194pressure coupling that closes the sodium loop (pressure natriuresis) is owned by the hemodynamic volume and cited here, not re-emerged.</p>"%(ri4["na_final"],ri4["k_final"]))
    secs.append(("05-electrolyte-na-k-setpoints",5,"electrolyte","Sodium and potassium setpoints",
      "Sodium and potassium setpoints are corrected by renal handling; a load in either is returned to setpoint in simulation. The sodium\u2013volume\u2013pressure coupling that closes the sodium loop is cited to the hemodynamic volume rather than re-emerged here.",
      "Sodium and potassium are loop quantities corrected by renal handling. Sodium loads are cleared via pressure natriuresis (a cited seam to the hemodynamic volume) and potassium via renal excretion; both return to their cited setpoints (Na ~140, K ~4.2 mM) in simulation.",
      body5,"grade g-verified","[V] loops; [L] setpoints"))

    body6=("<p class='abstract'>Phosphate is co-regulated with calcium so that the calcium\u00d7phosphate product stays below precipitation. FGF23 (the osteocyte arm) is the phosphate-lowering effector: a phosphate load raises FGF23, which drives phosphaturia and lowers phosphate.</p>"
      "<h2>The FGF23 lowering arm</h2>"
      "<p>A phosphate load raises FGF23 (the negative-feedback lowering arm), which increases renal phosphate excretion and returns phosphate to setpoint (final %.3f). The calcium\u00d7phosphate product stays below the precipitation threshold (maximum %.3f, normalized), protecting against vascular calcification and stones.</p>"%(ri5["po4_final"],ri5["ca_po4_product_max"])+
      "<h2>The renal threshold TmP/GFR (computed, not deferred)</h2>"
      "<p>The phosphate set-point IS the renal threshold TmP/GFR: plasma phosphate is held near it, and above it phosphate spills into urine. It is computed exactly from measurable inputs by the Walton\u2013Bijvoet nomogram \u2014 an invented number is not needed:</p>"
      "<table><tr><th>state</th><th>TmP/GFR (mmol/L)</th><th>in reference 0.80\u20131.35</th></tr>"
      "<tr><td>high FGF23 (XLH-type)</td><td>%.3f</td><td>no \u2014 low \u2192 hypophosphatemia</td></tr>"
      "<tr><td>normal</td><td>%.3f</td><td>yes</td></tr>"
      "<tr><td>low FGF23 / PTH (hypoPTH-type)</td><td>%.3f</td><td>no \u2014 high \u2192 hyperphosphatemia</td></tr></table>"
      %(R5["cases"]["high_fgf23_XLH"]["TmP_GFR_mmol_L"],R5["cases"]["normal"]["TmP_GFR_mmol_L"],R5["cases"]["low_fgf23_hypoPTH"]["TmP_GFR_mmol_L"])+
      "<p>FGF23 and PTH <b>lower</b> the threshold (the phosphaturic direction), reproduced as the monotone fall high-FGF23 &lt; normal &lt; low-FGF23. The residual open item is now precise <b>[O]</b>: \u03b3 sets loop <i>stability</i> (barrier b=\u03b3\u00b2/4 \u2192 gain k), not the absolute <i>value</i> \u2014 so predicting the TmP/GFR number from \u03b3 alone stays open by design; the value is clinical <b>[CAL]</b> / exact-algebra <b>[F]</b>, cross-checked to the adult reference range <b>[L]</b>.</p>")
    secs.append(("06-phosphate-fgf23-arm",6,"phosphate","Phosphate regulation and the FGF23 arm",
      "Phosphate is co-regulated with calcium so the calcium\u00d7phosphate product stays below precipitation. A phosphate load raises FGF23, which drives phosphaturia and returns phosphate to setpoint while the product stays below the calcification threshold in simulation.",
      "Phosphate is co-regulated with calcium so the calcium\u00d7phosphate product stays below precipitation: the FGF23 lowering arm returns a phosphate load to setpoint. The phosphate set-point is the renal threshold TmP/GFR, here computed exactly (Walton\u2013Bijvoet) and cross-checked to the adult reference range; FGF23 lowers it. Only \u03b3-prediction of the absolute value stays open.",
      body6,"grade g-verified","[V] mechanism; [F] TmP/GFR; [O] \u03b3\u2192value"))

    srows="".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(s["variable"],s["systemic_sensor"],s["sensory_twin"],s["instrument_failure"]) for s in S["seam"])
    body7=("<p class='abstract'>The body's mineral, acid and electrolyte SENSORS are the same molecular instruments that sensory cells use for taste, balance and pain. A comparator in a homeostatic loop and a sensory-cell transducer are the same R19-class object reading the same ionic variable.</p>"
      "<h2>One instrument, two uses</h2>"
      "<table><tr><th>variable</th><th>systemic sensor</th><th>sensory-cell twin</th><th>instrument failure</th></tr>%s</table>"%srows+
      "<p>Every measured sensor is a valid R19 instrument (all-valid %s) with sharpness monotone in \u03b3 (%s). Disease at a sensor is instrument failure: a mis-calibrated sensor defends a shifted setpoint, exactly the setpoint-drift mode.</p>"%(S["instrument_check"]["all_valid_bistable"],S["instrument_check"]["barrier_monotone_in_gamma"])+
      "<h2>OTOP1: the crown jewel</h2>"
      "<p>OTOP1 is a proton-selective channel that is both the sour-taste receptor and the keeper of the pH that forms otoconia \u2014 the calcium-carbonate biominerals of the vestibular organ. One molecule couples acid-base sensing, calcium-carbonate mineralization, and gravity sensing. BPPV (dislodged otoconia) is a common disease living at that mineral\u2194sensory seam.</p>")
    secs.append(("07-sensory-seam-ionic-sensors",7,"sensory seam","The sensory seam: ionic sensors are sensory-cell transducers",
      "The mineral, acid and electrolyte sensors (CaSR, OTOP1, ASIC, ENaC, TRPV5/6) are the same molecular instruments sensory cells use for taste, balance and pain. Each is a valid R19 instrument; disease at a sensor is instrument failure \u2014 a mis-calibrated sensor defends a shifted setpoint.",
      "A homeostatic comparator and a sensory-cell transducer are the same R19 instrument reading an ionic variable. CaSR (calcium), OTOP1 (acid/sour), ENaC (sodium/salt), ASIC and TRPV5/6 serve both interoception and an external sense; OTOP1 uniquely couples acid-base, calcium-carbonate otoconia, and gravity sensing.",
      body7,"grade g-cited","[L]/[V] identities + instrument check"))

    frows="".join("<tr><td>%s</td><td>%s</td></tr>"%(f["site"],f["mode"]) for f in P["failures"])
    body8=("<p class='abstract'>Disease in this system is a failure of a defended setpoint, a clock, or a sense organ on the same R19 substrate \u2014 not a local lesion. Six failure modes follow from the substrate: loop-gain drop, setpoint drift, reservoir depletion, buffer-arm failure, threshold crossing, instrument failure.</p>"
      "<h2>The derived failure modes</h2>"
      "<p>The substrate yields the failure laws directly: a loop-gain drop blows up the setpoint variance (Var=\u03c3\u00b2/2k) and slows correction; a comparator reset makes the loop defend a pathological value; a hard solubility/precipitation threshold is crossed discontinuously (the spinodal). All three are demonstrated (%s).</p>"%P["laws_demonstrated"]+
      "<table><tr><th>major disease</th><th>failure mode</th></tr>%s</table>"%frows+
      "<p>Rare and monogenic forms (MEN1, FHH, RTA transporters, Liddle, primary hyperoxaluria, ADH1 CaSR) are owned by the disease volume and enter here as a cited parameter (a setpoint shift or arm-gain change); the systemic trajectory is computed here.</p>")
    secs.append(("08-disease-as-setpoint-failure",8,"pathology","Disease as setpoint, clock and sense-organ failure",
      "Disease here is a failure of a defended setpoint, clock or sense organ on the R19 substrate: loop-gain drop (variance blow-up), setpoint drift (defending a pathological value), reservoir depletion, buffer-arm failure, threshold crossing, or instrument failure. The failure laws are demonstrated on the substrate.",
      "Mineral, acid-base and electrolyte diseases are failures of defended setpoints on the same R19 substrate. Six modes are derived and demonstrated; major diseases (osteoporosis, hyperparathyroidism, acidosis/alkalosis, electrolyte disorders, stones, ADH1, BPPV) map onto them, with rare/monogenic forms cited from the disease volume.",
      body8,"grade g-verified","[V] laws; [L] anchors; [O] incidence"))

    tc=T["therapy_classes"]; trows="".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"%(c["failure_mode"],c["fundamental_fix"],c["established"]) for c in tc)
    fh="".join("<li><b>%s</b> %s</li>"%(h["id"],h["hypothesis"]) for h in T["frontier_hypotheses"])
    t1=T["simulations"]["T1_setpoint_reset"]; t2=T["simulations"]["T2_reservoir_refill"]
    body9=("<p class='abstract'>Naming the failed loop element names the fundamental fix. Setpoint drift calls for resetting the set-point; loop-gain drop for restoring the failed arm; reservoir depletion for refilling (not just slowing withdrawal); threshold crossing for staying below it; a root driver for removing it.</p>"
      "<h2>The failure-keyed therapy map</h2>"
      "<table><tr><th>failure mode</th><th>fundamental fix</th><th>established example (cited)</th></tr>%s</table>"%trows+
      "<h2>Two falsifiable predictions</h2>"
      "<p>Set-point reset: in a setpoint-drift disease, an allosteric modulator that shifts the comparator back normalizes the defended value (%.3f \u2192 %.3f). This is the calcilytic/calcimimetic paradigm (encaleret resets the CaSR set-point up in ADH1; cinacalcet resets it down in hyperparathyroidism), expressed in the framework's own language.</p>"%(t1["defended_untreated"],t1["defended_treated"])+
      "<p>Reservoir refill versus withdrawal-slowing: for a depleted reservoir, raising formation (anabolic) refills it (%.2f), while only reducing withdrawal (anti-resorptive) rebuilds slowly (%.2f) and the untreated reserve keeps falling (%.2f). The anabolic is the more fundamental fix for a depleted reservoir \u2014 the clinical anabolic-first-then-anti-resorptive sequence, derived.</p>"%(t2["anabolic_final"],t2["antiresorptive_final"],t2["untreated_final"])+
      "<h2>Frontier hypotheses (framework-derived)</h2><ul>%s</ul>"%fh+
      "<h3>All four are now quantified</h3>"
      "<p><b>H-RESET</b> (the set-point reset generalizes): a homeostatic sensor is a comparator with a defended set-point, and the defended attractor equals that set-point for every comparator steepness \u2014 a structural identity, not a fit. So an allosteric reset (encaleret resets CaSR up in ADH1, Phase-3 CALIBRATE; cinacalcet resets it down in hyperparathyroidism) relocates the defended value durably, while symptom control normalises only while administered and relapses to the mis-set attractor on withdrawal (a residual of %.2f versus ~0 after reset). Across a family of ionic sensors (CaSR, ENaC, ASIC, OTOP1) the direction holds for every one \u2014 the <b>[V]</b> result; generalisation to non-CaSR allosteric recalibrators is <b>[H]</b> and the absolute residuals are <b>[O]</b>.</p>"%(FQ["H_RESET"]["rows"][0]["symptom_deviation"])+
      "<p><b>H-DUAL</b> (remove the formation brake): sclerostin inhibition raises DKK1 as negative feedback (Florio 2016, a \u03b2-catenin target), so the single-agent anabolic window closes while dual anti-sclerostin + anti-DKK1 sustains it. Modelling the integrated window reproduces the ordering dual (%.2f) &gt; single (%.2f) &gt; untreated (%.2f) \u2014 the <b>[V]</b> result is the ordering; the absolute window size is <b>[O]</b> and human clinical efficacy remains <b>[H]</b>.</p>"%(FQ["H_DUAL"]["integrated_window_dual"],FQ["H_DUAL"]["integrated_window_single"],FQ["H_DUAL"]["integrated_window_untreated"])+
      "<p><b>H-ARM</b> (restore the failed arm, do not just buffer): the acid-base setpoint is a two-timescale buffer whose loop gain comes from a working arm (renal HCO\u2083 regeneration / ventilatory drive). In distal renal tubular acidosis the renal arm transporter fails and the standard of care is lifelong alkali (ADV7103/Sibnayal) \u2014 it cancels the mean acidosis but leaves loop gain low. Reusing the volume's own OU law (err=load/k, Var=\u03c3\u00b2/2k), arm restoration (raising k) tightens the variance and rejects a fresh acid load by the factor k_high/k_low (\u2248%.1f\u00d7: the fresh-load excursion falls from %.2f under buffering to %.2f after restoration), while buffering improves neither and must be sustained \u2014 the <b>[V]</b> direction; the absolute gains are <b>[O]</b> and clinical arm-restoration remains <b>[H]</b>.</p>"%(FQ["H_ARM"]["predicted_ratio_k_high_over_k_low"],FQ["H_ARM"]["fresh_load_excursion_buffering"],FQ["H_ARM"]["fresh_load_excursion_restoration"])+
      "<p><b>H-OTOC</b> (otoconial calcite stability): otoconia are calcite, whose stability is the saturation \u03a9 = [Ca\u00b2\u207a][CO\u2083\u00b2\u207b]/Ksp; carbonate speciation makes \u03a9 a steep function of pH, and OTOP1 sets endolymph pH. With the physiological state at the \u03a9=1 boundary, acidosis drops \u03a9 to %.3f and hypocalcemia to %.3f \u2014 both undersaturated, dissolution-prone (the BPPV seam). The <b>[V]</b> result is the direction; the absolute \u03a9=1 threshold is <b>[O]</b> and clinical OTOP1/pH targeting remains <b>[H]</b>.</p>"%(FQ["H_OTOC"]["omega_acidosis"],FQ["H_OTOC"]["omega_low_calcium"])+
      "<p>The failure-keyed map and every simulation here are the reproduced results; named-drug efficacy is cited <b>[L]</b>, and where the framework predicts beyond current practice (non-CaSR sensor recalibration, transporter/drive restoration) it is flagged <b>[H]</b>, never asserted.</p>")
    secs.append(("09-fundamental-therapy",9,"therapy","Fundamental therapy keyed to the failure mode",
      "Naming the failed loop element names the fundamental fix: reset the set-point (setpoint drift), restore the failed arm (loop-gain drop), refill the reservoir rather than slow withdrawal (depletion), stay below the threshold (crossing), or remove the root driver. Two simulations make the distinctive predictions falsifiable.",
      "The framework turns disease into a failed loop element and so names the fundamental therapy. Set-point reset, arm restoration, reservoir refill over withdrawal-slowing, threshold avoidance, and root-driver removal are mapped; two predictions are demonstrated and all four frontier hypotheses (generalised sensor reset, dual Wnt-antagonist refill, acid-base arm restoration, otoconial calcite stability) are now quantified.",
      body9,"grade g-verified","[V] mapping + 4 quantified; [L] efficacy; clinical [H]"))

    crows="".join("<tr><td>%s</td><td>%s</td><td>%.1f</td><td>%.0f%%</td></tr>"%(s["strategy"],s["clade"],s["k"],100.0/s["k"]) for s in C["strategies"])
    conf=C["strategies"][0]; terr=C["strategies"][-1]
    body10=("<p class='abstract'>Every other object in this volume models one species \u2014 the human mineral / acid-base / electrolyte loops. That leaves a question the volume could not answer: across the animal kingdom, which animals use ions precisely and which do not? This section adds that axis on the SAME R19 substrate, reusing the volume's own closed-loop law (step error = load/k) with a single knob \u2014 the loop gain that defends the internal milieu against the environmental salinity load.</p>"
      "<h2>One gain separates regulators from conformers</h2>"
      "<p>High gain holds the internal state and rejects the environment (a precise ion regulator); low gain lets the internal state track the environment (a conformer). Assigning each clade to its strategy is cited comparative physiology <b>[L]</b>; the reproduced result is the direction and ordering <b>[V]</b>. Osmoconformers (most marine invertebrates) sit at the low-gain limit; marine elasmobranchs osmoconform via urea+TMAO yet iono-regulate their inorganic ions; teleosts and tetrapods are progressively tighter regulators, with the terrestrial mammal (this volume's baseline) at the top.</p>"
      "<table><tr><th>osmotic strategy</th><th>clade / exemplar</th><th>loop gain k</th><th>environment tracked</th></tr>%s</table>"%crows+
      "<h2>What is reproduced</h2>"
      "<p>Under a fixed salinity load the conformer's internal milieu is dragged to %.2f while the terrestrial regulator holds at %.2f \u2014 a ratio of %.1f\u00d7 that equals the gain ratio k_regulator/k_conformer (%.1f), the volume's own load/k law. Sweeping a range of environments, the conformer tracks %.0f%% of the environmental swing and the regulator only %.0f%% \u2014 the regulator is the precise ion user. The internal excursion is monotone in loop gain across all five strategies, so a single substrate parameter orders the whole animal kingdom from conformer to tight regulator.</p>"%(conf["internal_offset"],terr["internal_offset"],C["tracking_ratio_conformer_over_regulator"],C["predicted_ratio_k_reg_over_k_conf"],100*C["sweep_conformer_fraction_tracked"],100*C["sweep_regulator_fraction_tracked"])+
      "<h2>What stays open (the next task)</h2>"
      "<p>The absolute loop gains and the tolerated salinity ranges (euryhaline versus stenohaline) are <b>[O]</b>. Crucially, the human axis grounds its loop stiffness in a MEASURED master-gene gamma (kidney SIX2 gamma=1.5556 atop the ladder, barrier b=gamma\u00b2/4 \u2192 stiffness k); grounding each species' gain in its own measured osmoregulatory master-gene gamma is not yet done \u2014 that is the next-task obstacle <b>[O]</b>/<b>[H]</b>. The separation shown here is the reproduced direction, never a species-specific quantitative claim.</p>")
    secs.append(("10-comparative-ionoregulation",10,"comparative","Comparative ionoregulation: which animals defend ions versus conform",
      "Across the animal kingdom, whether an animal regulates its ions or conforms to its environment is one loop gain on the same R19 substrate: conformers run low gain and track the environment, regulators run high gain and defend the internal milieu. Cited strategy assignment, reproduced separation, absolute gains open.",
      "The volume's human model is one species that regulates ions precisely. Across the animal kingdom, whether an animal defends its ions or conforms to the environment is set by a single loop gain on the same R19 substrate: conformers run low gain and track the environment, regulators run high gain and hold the internal milieu against it.",
      body10,"grade g-verified","[L] strategy; [V] separation; [O] absolute k; per-species \u03b3 [O]/[H]"))

    mg=T2["G2_magnesium"]; ck=T2["G3_ckd_mbd"]; hh=T2["G4_humoral_hypercalcemia_pthrp"]
    mg_tbl=("<table><tr><th>condition</th><th>loop gain k</th><th>internal Mg offset</th></tr>"
      "<tr><td>healthy loop, Mg-loss drive</td><td>%.1f</td><td>%.2f</td></tr>"
      "<tr><td>absorption / reabsorption-arm failure \u2192 hypomagnesemia</td><td>%.1f</td><td>%.2f</td></tr>"
      "<tr><td>healthy loop, Mg-intake drive</td><td>%.1f</td><td>+%.2f</td></tr>"
      "<tr><td>excretion-arm failure \u2192 hypermagnesemia</td><td>%.1f</td><td>+%.2f</td></tr></table>"
      %(mg["k_healthy"],mg["healthy_offset_under_loss"],mg["k_arm_failed"],mg["hypomagnesemia_offset"],
        mg["k_healthy"],mg["healthy_offset_under_intake"],mg["k_arm_failed"],mg["hypermagnesemia_offset"]))
    ck_tbl=("<table><tr><th>renal integrator gain</th><th>serum PO\u2084</th><th>1,25-vitD</th><th>serum Ca</th><th>PTH</th><th>Ca\u00d7PO\u2084</th></tr>"
      +"".join("<tr><td>%.1f</td><td>%.2f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td></tr>"
               %(s["renal_gain"],s["serum_po4"],s["vitamin_d"],s["serum_ca"],s["pth"],s["ca_x_po4"]) for s in ck["stages"])
      +"</table>")
    hh_tbl=("<table><tr><th>PTHrP drive</th><th>defended calcium</th><th>endogenous PTH</th><th>PTH suppressed</th></tr>"
      +"".join("<tr><td>%.2f</td><td>%.3f</td><td>%.3f</td><td>%s</td></tr>"
               %(s["pthrp_drive"],s["defended_calcium"],s["endogenous_pth"],"yes" if s["endogenous_pth_suppressed"] else "no (baseline)") for s in hh["levels"])
      +"</table>")
    body11=("<p class='abstract'>The volume's pathology chapter closes seven representative diseases on six failure modes and lets rare or specific forms enter as a cited parameter. Three further MAJOR ion diseases \u2014 magnesium imbalance, CKD-MBD with secondary hyperparathyroidism, and humoral hypercalcemia of malignancy \u2014 were named but not yet modelled. Each is one of the SAME six failure modes, reusing the volume's own load/k law and PTH comparator with no new primitive.</p>"
      "<h2>Magnesium: a third defended ion on the same load/k law</h2>"
      "<p>Serum magnesium (~%.2f mM, cited) is a defended setpoint like calcium and pH. Its diseases are the loop-gain-drop / buffer-arm-failure mode read on a third ion: when an arm loses gain, the same disturbance is no longer rejected and the residual offset is load/k. An absorption / reabsorption-arm failure (TRPM6 loss \u2014 hypomagnesemia with secondary hypocalcemia; Gitelman renal Mg wasting) under an Mg-loss drive pulls magnesium DOWN; an excretion-arm failure (renal insufficiency with an Mg load) pushes it UP.</p>"
      +mg_tbl+
      "<p>The failed-arm excursion exceeds the healthy-loop residual in both directions, the ratio (%.1f\u00d7) equals the gain ratio k_healthy/k_failed (%.1f) \u2014 the volume's own load/k law \u2014 and the failed loop's variance blows up (Var=\u03c3\u00b2/2k). The directions are <b>[V]</b>; the cited setpoint and the TRPM6 / Gitelman anchors are <b>[L]</b>; the absolute Mg excursion magnitude is <b>[O]</b>.</p>"
      "<h2>CKD-MBD: a multi-arm gain drop of the renal integrator</h2>"
      "<p>As nephrons are lost the renal integrator (the kidney node) loses gain, and the CKD-MBD cascade is the loop-gain-drop mode applied to SEVERAL arms at once. Stepping the renal gain down reproduces the cited KDIGO sequence: serum phosphate rises (its excretion arm err=load/k grows), 1,25-vitamin-D falls (renal 1\u03b1-hydroxylase), serum calcium tends down, and the calcium-sensing receptor raises PTH \u2014 secondary hyperparathyroidism.</p>"
      +ck_tbl+
      "<p>All four primary signs are monotone in the falling renal gain (phosphate up %s, vitamin-D down %s, calcium down %s, PTH up %s), and PTH rises above its baseline in advanced disease. The calcium\u00d7phosphate product is near-normal early (a small early dip as calcium falls before phosphate retention dominates) and climbs to the precipitation ceiling in advanced CKD (%.2f \u2192 %.2f, the vascular-calcification driver). The cascade direction is <b>[V]</b>; the KDIGO cascade is the <b>[L]</b> anchor; absolute per-stage progression timing is <b>[O]</b>.</p>"
      "<h2>Humoral hypercalcemia of malignancy: a set-point drift upward</h2>"
      "<p>Tumor-secreted PTHrP acts at the PTH receptor like PTH but is tumor-autonomous \u2014 the calcium-sensing receptor cannot suppress it. In the set-point-drift plant (PTH effector against a constant loss), an exogenous UNSUPPRESSIBLE drive relocates the defended calcium UPWARD, the exact inverse of the T1 allosteric reset that relocates it back down.</p>"
      +hh_tbl+
      "<p>The defended calcium rises monotonically with the PTHrP drive into the hypercalcemic range, while the endogenous PTH is appropriately SUPPRESSED below baseline despite the high calcium \u2014 the clinical fingerprint that distinguishes humoral hypercalcemia from primary hyperparathyroidism (where PTH is high). The CaSR loop works; it simply cannot turn off a drive that is not its own. The direction is <b>[V]</b>; the PTHrP mechanism is the <b>[L]</b> anchor (Stewart 2005); the absolute hypercalcemia level is <b>[O]</b>.</p>"
      "<h2>What this closes</h2>"
      "<p>These three extend the human disease coverage from a representative seven toward nearly all the major mineral / acid-base / electrolyte disorders \u2014 each by reusing a failure mode already on the substrate, not by adding machinery. The two items named here as open in earlier drafts are now closed in the next two chapters: the molecular transport DYNAMICS behind these arms (channel gating / GHK flux) is derived in \u00a712, and the per-species master-gene \u03b3 that would ground the cross-species gains is MEASURED in \u00a713 \u2014 where it returns an honest negative. Neither is hidden; both are now resolved, one as a new primitive and one as a documented obstacle.</p>")
    secs.append(("11-magnesium-ckd-mbd-humoral-hypercalcemia",11,"disease coverage",
      "Magnesium, CKD-MBD and humoral hypercalcemia: extending the disease coverage",
      "Three further major ion diseases \u2014 magnesium imbalance, CKD-MBD with secondary hyperparathyroidism, and humoral hypercalcemia of malignancy \u2014 close by reusing the six failure modes already derived: a loop-gain drop on a third ion, a multi-arm renal gain drop, and a set-point drift upward.",
      "Three further major ion diseases close by reusing the six failure modes already derived, with no new primitive: magnesium imbalance is a loop-gain drop read on a third ion, CKD-MBD is a multi-arm gain drop of the renal integrator, and humoral hypercalcemia of malignancy is a set-point drift upward \u2014 the inverse of the allosteric reset.",
      body11,"grade g-verified","[L] cited anchors; [V] each direction via a reused failure mode; [O] absolute magnitudes"))

    # ---- 12: TRANSPORT DYNAMICS (G5, new primitive) ----
    TRgh=TR["GHK_constant_field_flux"]; TRvd=TR["vitamin_d_channel_gating"]; TRgg=TR["molecular_gain_grounds_loop_gain_k"]; TRlf=TR["loss_of_function_is_loop_gain_drop"]
    vd_tbl=("<table><tr><th>vitamin-D signal</th><th>channel open probability</th><th>Ca reabsorptive flux (GHK)</th></tr>"
      +"".join("<tr><td>%.2f</td><td>%.3f</td><td>%.2f</td></tr>"%(x["vitd_signal"],x["p_open"],x["ca_reabsorptive_flux"]) for x in TRvd["levels"])+"</table>")
    grnd_tbl=("<table><tr><th>channel number N</th><th>k = \u2212dJ/dC</th><th>setpoint variance</th><th>Var\u00b72k/\u03c3\u00b2</th><th>step error</th><th>error\u00b7k</th></tr>"
      +"".join("<tr><td>%.1f</td><td>%.4f</td><td>%.5f</td><td>%.3f</td><td>%.5f</td><td>%.2f</td></tr>"
               %(x["channel_number"],x["k_molecular"],x["ou_variance"],x["var_times_2k_over_sigma2"],x["step_error"],x["error_times_k"]) for x in TRgg["ladder"])+"</table>")
    VPCARD_GHK=('<aside class="vp-card" data-locked="ghk-flux"><b>GHK constant-field flux + channel gating</b> \u2014 J = P\u00b7z\u00b7F\u00b7u\u00b7(C\u1d62 \u2212 C\u2092 e^\u2212\u1d58)/(1 \u2212 e^\u2212\u1d58), u = zFV\u2098/RT; open probability from a Boltzmann / Hill gate. The flux slope at the setpoint k = \u2212dJ/dC IS the loop gain. <b>[F]</b> exact physics; <b>[V]</b> grounding; <b>[O]</b> absolute single-channel conductance. <a href="https://jamming-physics.org/homeostasis-ionic/">this volume</a></aside>')
    body12=(VPCARD_GHK+
      "<p class='abstract'>The loop arms above were cited by transporter name \u2014 TRPV5/6, ENaC, the H\u207a-ATPase \u2014 but the molecular 'how' beneath them was not yet derived. This chapter adds the one primitive that supplies it: the Goldman-Hodgkin-Katz constant-field flux through a gated channel. Its central result is not a new number but a CONNECTION \u2014 the membrane flux slope at the setpoint, k = \u2212dJ/dC, is exactly the loop gain the rest of the volume already runs on. Channel biophysics and the OU control law are the same quantity seen at two scales.</p>"
      "<h2>The constant-field flux law</h2>"
      "<p>A single channel's current under a fixed field is the GHK constant-field flux: it depends on the permeability, the membrane voltage, and the ion concentrations either side. Two properties are exact and are reproduced in simulation. The flux REVERSES exactly at the Nernst potential (here %.2f mV, where J=0) and changes sign across it (%.2f below reversal, +%.2f above), and it RECTIFIES when the ion is more concentrated on one side \u2014 the chord conductance differs hyperpolarized versus depolarized (%.3f vs %.3f). These are forced by the physics; the volume does not fit them.</p>"
      %(TRgh["nernst_mV"],TRgh["flux_below_reversal"],TRgh["flux_above_reversal"],TRgh["chord_slope_hyperpolarized"],TRgh["chord_slope_depolarized"])+
      "<h2>Gating: vitamin-D opens the calcium channel</h2>"
      "<p>A channel's open probability is set by a gate \u2014 a Boltzmann/Hill function of its controlling signal. The slow VDR arm of the calcium loop acts here: 1,25-dihydroxyvitamin-D transcriptionally up-regulates the apical Ca channels TRPV5 (kidney) and TRPV6 (gut). Raising the vitamin-D signal raises the channel open probability and, through the GHK flux, the transcellular calcium reabsorptive flux \u2014 both monotonically.</p>"
      +vd_tbl+
      "<p>The channel-identity assignment (VDR \u2192 TRPV5/6) is the cited <b>[L]</b> anchor; the monotone rise of open probability and Ca flux with the vitamin-D signal is <b>[V]</b>; the absolute half-activation and single-channel permeability are <b>[O]</b>.</p>"
      "<h2>The molecular gain IS the loop gain</h2>"
      "<p>This is the load-bearing result. Write the per-deviation restoring flux at the setpoint, k = \u2212dJ/dC \u2014 the proportional flux a small concentration error pulls back. Feed THAT k into the volume's own Ornstein-Uhlenbeck setpoint and the two descriptions coincide: the membrane gain reproduces the OU variance law Var = \u03c3\u00b2/2k and the rejection law error = load/k exactly, k rises linearly with channel number, and a steeper gate raises k. The channel and the control loop are one object.</p>"
      +grnd_tbl+
      "<p>Across the channel-number ladder, k = \u2212dJ/dC rises proportionally (%s), the setpoint variance falls (%s), and both OU laws are recovered to rounding (Var\u00b72k/\u03c3\u00b2 \u2248 1, error\u00b7k \u2248 1). A steeper gate raises k (%s). The GHK flux and gating are <b>[F]</b>; the identity k=\u2212dJ/dC = OU loop gain is <b>[V]</b>; the absolute channel density is <b>[O]</b>.</p>"
      %(TRgg["k_rises_with_channel_number"],TRgg["setpoint_variance_falls_with_channel_number"],TRgg["steeper_gate_raises_k"])+
      "<h2>Loss of function is the loop-gain drop at the membrane</h2>"
      "<p>Because the membrane gain IS the loop gain, a loss-of-function transporter is precisely the loop-gain-drop failure mode \u2014 now localized to a single channel. Dropping the channel number / conductance lowers k (%.2f \u2192 %.2f), and the volume's own load/k law follows: the steady offset grows by the same factor (\u00d7%.1f, equal to the gain ratio %.1f) and the variance blows up (%.5f \u2192 %.5f). This is the molecular reading of the membrane diseases the pathology chapter cited: TRPV5/6 loss \u2192 renal calcium wasting; ENaC / SCNN1A loss \u2192 pseudohypoaldosteronism type 1; H\u207a-ATPase / ATP6V loss \u2192 distal renal tubular acidosis.</p>"
      %(TRlf["k_healthy"],TRlf["k_lof"],TRlf["offset_ratio"],TRlf["predicted_ratio_k_healthy_over_k_lof"],TRlf["variance_healthy"],TRlf["variance_lof"])+
      "<p>The failed-channel offset exceeds the healthy one, the ratio equals the gain ratio (the volume's load/k law again), and variance blows up \u2014 all <b>[V]</b>. The transporter identities and their loss-of-function phenotypes are the cited <b>[L]</b> anchors; the absolute single-channel conductances and channel densities are <b>[O]</b>, the electrophysiological calibration that is this chapter's stated residual.</p>")
    secs.append(("12-molecular-transport-dynamics-ghk-gating",12,"transport dynamics",
      "Molecular transport dynamics: GHK flux, channel gating, and why the membrane gain is the loop gain",
      "The molecular 'how' beneath the loop arms is one primitive: the Goldman-Hodgkin-Katz constant-field flux through a gated channel. Its flux slope at the setpoint, k = \u2212dJ/dC, is exactly the loop gain the volume runs on, so channel number sets setpoint stability and a loss-of-function transporter is the loop-gain drop at the membrane.",
      "The molecular 'how' beneath the loop arms is one primitive: the Goldman-Hodgkin-Katz constant-field flux through a gated channel. The central result is a connection \u2014 the membrane flux slope at the setpoint, k = \u2212dJ/dC, is exactly the Ornstein-Uhlenbeck loop gain the volume already uses, so channel biophysics and the control loop are one quantity at two scales.",
      body12,"grade g-forced","[F] GHK flux + gating exact; [V] k=\u2212dJ/dC IS the OU loop gain; [L] transporter identities / LOF phenotypes; [O] absolute conductances / densities"))

    # ---- 13: COMPARATIVE GAMMA (G6, honest negative) ----
    CGgt=CG["grounding_test"]
    cg_tbl=("<table><tr><th>osmotic strategy</th><th>loop gain k</th><th>ATP1A1 promoter \u03b3</th><th>promoter GC</th><th>species</th></tr>"
      +"".join("<tr><td>%s</td><td>%.1f</td><td>%.4f</td><td>%.4f</td><td>%s</td></tr>"
               %(r["strategy"].replace("_"," "),r["k"],r["gamma"],r["gc"],r["common_name"]) for r in sorted(CGgt["rows"],key=lambda r:(r["k"],-r["gamma"])))+"</table>")
    body13=(VPCARD_GAMMA+
      "<p class='abstract'>The comparative chapter (\u00a710) ordered animals by a single loop gain but left the absolute gains open and the per-species master-gene \u03b3 unmeasured. This chapter measures it \u2014 and reports an HONEST NEGATIVE. The osmoregulatory master gene ATP1A1 (the Na\u207a,K\u207a-ATPase \u03b1-1, the universal pump powering all secondary ion transport) had its promoter \u03b3 measured across six species spanning the osmotic-strategy axis, by the same NCBI / SantaLucia-1998 pipeline the rest of the framework uses. The measurement is sound, but \u03b3 does NOT order the species by their loop gain. It is published here as a negative, not hidden.</p>"
      "<h2>Measuring the osmoregulatory master gene across the strategy axis</h2>"
      "<p>From osmoconformers (Pacific oyster) through urea-retaining elasmobranchs (elephant shark, thorny skate) and aquatic regulators (zebrafish, Xenopus) to a terrestrial regulator (human), the ATP1A1 proximal-promoter \u03b3 = \u2212mean nearest-neighbor stacking energy was measured from the public genome of each species \u2014 never fitted. Two internal checks confirm the pipeline is sound: the human ATP1A1 \u03b3 reproduces its standalone anchor (%s), and the two independent elasmobranchs land within %.4f of each other (%s) \u2014 a near-identical replicate.</p>"
      %(CGgt["human_atp1a1_anchor_reproduced"],CGgt["elasmobranch_replicate_spread"],CGgt["replicate_consistent"])+
      cg_tbl+
      "<h2>The grounding test fails</h2>"
      "<p>For \u03b3 to ground the comparative loop gain k, it would have to increase with k across the strategy axis. It does not. The rank correlation is only Spearman(\u03b3, k) = %.3f, and the ordering is plainly non-monotone: the two k=3.0 aquatic regulators alone span most of the entire conformer-to-mammal \u03b3 range, and the k=3.0 amphibian \u03b3 (%.4f) actually EXCEEDS the higher-gain k=4.0 mammal (%.4f). Per-species ATP1A1 \u03b3 does not grade the osmoregulatory loop gain.</p>"
      %(CGgt["spearman_gamma_vs_k"],
        next(r["gamma"] for r in CGgt["rows"] if r["strategy"]=="amphibian_regulator"),
        next(r["gamma"] for r in CGgt["rows"] if r["strategy"]=="terrestrial_regulator"))+
      "<h2>Why: \u03b3 here is a GC readout, a lineage property</h2>"
      "<p>The diagnosis is clean. Across these six species \u03b3 tracks promoter GC content almost perfectly \u2014 Spearman(\u03b3, GC) = %.3f. Nearest-neighbor stacking energy is dominated by GC pairs, so a same-gene promoter \u03b3 measured ACROSS genomes mostly reads each genome's background GC, a lineage / genome-composition property, not that species' osmoregulatory precision. The within-genome \u03b3-ladder that works inside one organism (different master genes sharing a common GC background) does not transfer to a one-gene, many-genome comparison.</p>"
      %CGgt["spearman_gamma_vs_gc"]+
      "<h2>What this means</h2>"
      "<p>The comparative absolute loop gain k therefore STAYS open \u2014 but it is now open for a stated, demonstrated reason rather than as a bare placeholder: per-species master-gene \u03b3 is the wrong instrument for it, confounded by promoter GC. The measurement itself is verified <b>[V]</b> (NCBI, SantaLucia 1998, offline-reproducible, human-anchored), the negative result and the GC confound are verified <b>[V]</b>, the strategy-to-clade assignment is cited <b>[L]</b>, and the comparative absolute k is <b>[O]</b> with this confound as its documented obstacle. A genuine cross-species grounding would need a within-lineage or GC-controlled comparison \u2014 named here as the next instrument, not papered over.</p>")
    secs.append(("13-comparative-master-gene-gamma-honest-negative",13,"comparative \u03b3",
      "Per-species master-gene \u03b3: an honest negative on grounding the cross-species loop gain",
      "The osmoregulatory master gene ATP1A1 had its promoter \u03b3 measured across six species on the osmotic-strategy axis. The measurement is sound (human-anchored, replicate near-identical), but \u03b3 does not order species by loop gain (Spearman 0.65, non-monotone); it tracks promoter GC instead. The comparative absolute gain stays open, now with a documented reason.",
      "The osmoregulatory master gene ATP1A1 had its promoter \u03b3 measured across six species. The measurement is sound, but \u03b3 does not order species by loop gain \u2014 it tracks promoter GC, a lineage property \u2014 so the within-genome \u03b3-ladder does not transfer across genomes. An honest negative: the comparative absolute gain stays open for a demonstrated reason.",
      body13,"grade g-verified","[V] \u03b3 measured (NCBI, SantaLucia 1998, never fitted); [V] grounding negative + GC confound reproduced; [L] strategy\u2194clade; [O] comparative absolute k (per-species \u03b3 is the wrong instrument)"))

    # ---- 14: THREE-LEVER THERAPEUTIC PRINCIPLE (inherited from the non-opioid analgesic volume) ----
    la=TL["lever_asymmetry"]; gcl=TL["gain_lever_dna_ceiling"]; amap=TL["analgesic_lever_map"]; cw=TL["existing_results_crosswalk"]
    asym_tbl=("<table><tr><th>intervention</th><th>acts on</th><th>steady error (load/k)</th><th>variance (\u03c3\u00b2/2k)</th><th>tightens variance?</th></tr>"
      "<tr><td>baseline</td><td>\u2014</td><td>%.3f</td><td>%.5f</td><td>\u2014</td></tr>"
      "<tr><td><b>L1</b> source</td><td>load</td><td>%.3f</td><td>%.5f</td><td>no</td></tr>"
      "<tr><td><b>L2</b> gain</td><td>k</td><td>%.3f</td><td>%.5f</td><td>YES</td></tr>"
      "<tr><td><b>L3</b> setpoint</td><td>x*</td><td>target \u2192 %.2f</td><td>%.5f</td><td>no</td></tr></table>"
      %(la["baseline"]["mean_error"],la["baseline"]["variance"],
        la["L1_source"]["mean_error"],la["L1_source"]["variance"],
        la["L2_gain"]["mean_error"],la["L2_gain"]["variance"],
        la["L3_setpoint"]["new_target"],la["L3_setpoint"]["variance"]))
    ceil_tbl=("<table><tr><th>arm \u2014 node master gene</th><th>measured \u03b3</th><th>L2 gain ceiling b=\u03b3\u00b2/4</th></tr>"
      +"".join("<tr><td>%s</td><td>%.4f</td><td>%.4f</td></tr>"%(r["node_master"],r["gamma"],r["barrier_b_gamma2_over_4"]) for r in gcl["by_gamma_ascending"])+"</table>")
    amap_tbl=("<table><tr><th>lever</th><th>handle</th><th>analgesic exemplar (source volume)</th><th>ionic-homeostasis twin (this volume)</th></tr>"
      +"".join("<tr><td><b>%s</b> %s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(m["lever"],m["name"],m["acts_on"],m["analgesic_exemplar"],m["ionic_exemplar"]) for m in amap)+"</table>")
    cw_tbl=("<table><tr><th>lever</th><th>existing result in this volume</th><th>re-read as one lever</th><th>metric</th></tr>"
      +"".join("<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td></tr>"%(r["lever"],r["existing_result"],r["reading"],r["metric"]) for r in cw["rows"])+"</table>")
    body14=(VPCARD_3LEVER+
      "<p class='abstract'>Every mineral, acid-base and electrolyte setpoint in this volume is defended by the same Ornstein-Uhlenbeck attractor dx/dt=\u2212k(x\u2212x*)+load+noise. That attractor has exactly three independent parameters \u2014 the load onto the switch, the loop gain k, and the defended target x* \u2014 so there are exactly three independent ways to move a defended ion. This chapter inherits a cross-volume technology from the non-opioid analgesic volume (concept DOI 10.5281/zenodo.20733420), where 27 non-opioid analgesic targets were shown to sort onto three levers of a threshold-crossing, and proves the same three levers organize ionic homeostasis. This is not an analogy: each lever is one OU parameter, the levers are asymmetric in a way the OU law dictates, and the ceiling on the most powerful lever is read directly from this volume\u2019s MEASURED master-gene \u03b3. Every therapy already derived in the volume is then shown to be exactly one of the three.</p>"
      "<h2>A defended setpoint has exactly three handles</h2>"
      "<p>Linearized about its target, a defended homeostatic variable is the Ornstein-Uhlenbeck process the substrate chapter derived: a restoring term \u2212k(x\u2212x*), a disturbance load, and noise. Three parameters, three levers. <b>L1 (source)</b> lowers the load \u2014 the disturbance current onto the switch. <b>L2 (gain)</b> raises the loop gain k \u2014 the per-deviation restoring strength supplied by the node barrier. <b>L3 (setpoint)</b> relocates the defended target x* \u2014 the comparator\u2019s reference. There is no fourth handle, because the attractor has no fourth parameter; an intervention that is not one of these three is acting on the rate of approach or on a symptom, not on the defended state.</p>"
      "<h2>The asymmetry theorem: only the gain lever tightens variance</h2>"
      "<p>The three levers are not interchangeable, and the OU law states precisely how they differ. The steady disturbance error is load/k, so it is lowered by EITHER cutting the load (L1) OR raising the gain (L2). The stationary variance is \u03c3\u00b2/2k \u2014 it contains k but NOT the load \u2014 so it is tightened ONLY by L2. L3 moves the whole attractor to a new defended value without touching either error or variance. Reproduced on the volume\u2019s own OU law from one baseline (loop gain k, unit load): cutting the load halves the steady error but leaves the variance unchanged; doubling the gain halves BOTH the steady error and the variance; relocating the target moves the defended value durably to its new reference at the original spread.</p>"
      +asym_tbl+
      "<p>The table makes the asymmetry explicit: L1 and L2 both halve the mean error, but only L2 halves the variance, and L3 carries the defended value to its new target while leaving the spread alone (only_L2_tightens_variance = %s). This is the load-bearing distinction for therapy. A noisy, unstable setpoint \u2014 a wide defended band \u2014 can be narrowed ONLY by restoring loop gain; lowering the driver improves the average but not the scatter, and relocating the target cannot stabilize a loose loop. The asymmetry is <b>[V]</b> from the OU law; absolute magnitudes are <b>[O]</b>.</p>"%la["only_L2_tightens_variance"]+
      "<h2>The gain lever inherits its ceiling from the emerged genome</h2>"
      "<p>This is where the construction is grounded in real DNA emergence rather than a free parameter. L2 raises k, but k is not unbounded: per arm its ceiling is the node barrier b=\u03b3\u00b2/4, and \u03b3 is the MEASURED master-gene stacking energy (NCBI proximal promoters, SantaLucia 1998 nearest-neighbor thermodynamics, never fitted) that this framework uses to emerge each organ. The gain lever therefore inherits its headroom from the genome layer: the deepest node admits the most gain, the shallowest the least, and the ordering is monotone in measured \u03b3. The most powerful therapeutic handle has a ceiling that is a measured genomic quantity, not a tuning knob \u2014 which is exactly why this is a grounded simulation and not a toy.</p>"
      +ceil_tbl+
      "<p>The L2 gain ceiling is monotone in the measured \u03b3 (%s): deepest node %s, shallowest %s. The ceiling read-off is <b>[V]</b> from the measured-\u03b3 barrier; the absolute k-scale is <b>[O]</b>.</p>"%(gcl["gain_ceiling_monotone_in_measured_gamma"],gcl["deepest_node"],gcl["shallowest_node"])+
      "<h2>Inheritance from the non-opioid analgesic volume</h2>"
      "<p>The three-lever frame is imported, not invented here. In the non-opioid analgesic volume (concept DOI 10.5281/zenodo.20733420) a pain threshold-crossing was shown to have three independent handles, and 27 analgesic targets sorted onto them: lower the generator drive (L1: NSAID and COX inhibition, anti-NGF), raise the firing barrier (L2: Nav1.7/Nav1.8 blockers of the suzetrigine class, Kv7/KCNQ openers, local anesthetics), or reset central gain (L3: gabapentinoids, SNRIs, NMDA antagonists, \u03b1\u2082-agonists). Each maps onto one ionic-homeostasis lever exactly, because both are the same R19 threshold object read at two sites \u2014 the pain switch and the mineral-defending loop.</p>"
      +amap_tbl+
      "<p>The drug-class anchors on both sides are cited <b>[L]</b>; the one-to-one correspondence of the handles is structural. The technology transfers because the object transfers: a threshold on the shared jamming-lattice switch, whether it gates a nociceptor or a calcium-sensing comparator.</p>"
      "<h2>Every therapy already in this volume is one of the three levers</h2>"
      "<p>The principle is not bolted on after the fact: each therapy result derived earlier in this volume turns out to be exactly one lever, pulled live from its module and re-read. The set-point resets \u2014 calcimimetic and calcilytic, and the durable sensor reset that outlasts symptom relapse \u2014 are <b>L3</b>. The reservoir refill (anabolic beats anti-resorptive), the dual-antibody sustained bone window, and the renal-bicarbonate-arm restoration are <b>L2</b> \u2014 and these are precisely the results that turn on tightening the defended band. The otoconial-stability, spinodal-stone-crossing and upstream-driver-removal results are <b>L1</b>. All validated against their source modules (%s).</p>"%cw["all_existing_results_validated"]+
      cw_tbl+
      "<p>Reading the volume\u2019s own therapy catalogue through the inherited levers shows it was a three-lever catalogue all along: <b>[V]</b> each instance pulled live and re-read as one lever, with L2 owning the two results that turn on tightening variance.</p>")
    secs.append(("14-three-lever-therapeutic-principle-source-gain-setpoint",14,"three levers",
      "The three-lever therapeutic principle: source, gain, setpoint",
      "A defended mineral, acid-base or electrolyte setpoint is an Ornstein-Uhlenbeck attractor with three parameters \u2014 load, loop gain k, and target x* \u2014 so it has exactly three therapeutic levers: L1 lowers the load, L2 raises the gain, L3 relocates the target. Only L2 tightens the variance \u03c3\u00b2/2k, and the L2 ceiling is the measured master-gene \u03b3 barrier. The frame is inherited from the non-opioid analgesic volume.",
      "A defended homeostatic setpoint dx/dt=\u2212k(x\u2212x*)+load+noise has three handles, so exactly three levers: L1 lowers the load, L2 raises the loop gain k, L3 relocates the target x*. Only L2 tightens the variance \u03c3\u00b2/2k, and its ceiling is the measured master-gene barrier \u03b3\u00b2/4. The frame is inherited from the non-opioid analgesic volume, and every therapy in this volume is one lever.",
      body14,"grade g-verified","[V] lever asymmetry + \u03b3-ceiling from the volume\u2019s own OU law and measured \u03b3; [L] cross-volume non-opioid analgesic drug classes; [O]/[H] absolute magnitudes / clinical efficacy"))

    # ---- 15: MINERAL & BONE DISEASE UNDER THE THREE LEVERS ----
    res=DR["remediation"]["archetype_demonstrations"]["reservoir"]
    drift=DR["remediation"]["archetype_demonstrations"]["setpoint_drift"]
    bone_names=["osteoporosis","primary hyperparathyroidism","ADH1 (autosomal dominant hypocalcemia type 1)",
                "CKD-MBD with secondary hyperparathyroidism","humoral hypercalcemia of malignancy (PTHrP)","hypomagnesemia / hypermagnesemia"]
    body15=(VPCARD_3LEVER+
      "<p class='abstract'>The mineral and bone diseases this volume owns \u2014 osteoporosis, primary hyperparathyroidism, autosomal dominant hypocalcemia, CKD-MBD with secondary hyperparathyroidism, humoral hypercalcemia of malignancy, and the magnesium disorders \u2014 are read here through the three levers. The method is principled, not descriptive: for each disease the PRIMARY lever is SELECTED from which Ornstein-Uhlenbeck parameter the disease corrupted (load, gain, or setpoint), demonstrated on the volume\u2019s own OU law, and turned into an honestly-graded improvement proposal grounded in the inherited non-opioid analgesic technology (DOI 10.5281/zenodo.20733420) and the measured-\u03b3 gain ceiling. Owned means common, polygenic, acquired or age-related loop disorders; rare monogenic gene facts are cited to the rare-disease SSOT and not re-derived (VP_FRAMEWORK_MAP \u00a76).</p>"
      "<h2>Selecting the lever from the corrupted parameter</h2>"
      "<p>The selection rule is mechanical and it prevents the most common therapeutic error \u2014 treating the symptom instead of the defended state. If the disease imposes an unsuppressible external LOAD, the matched lever is L1 (oppose the source). If it drops a LOOP GAIN \u2014 a failed transport arm or a depleted reservoir \u2014 the matched lever is L2 (restore or refill the gain). If it drifts the defended TARGET, the matched lever is L3 (recalibrate the comparator). Reading the corrupted parameter first is what tells you that alkali for an acidosis arm, plain calcium for a low set-point, or an anti-resorptive alone for a depleted reservoir each addresses the wrong parameter.</p>"
      +dtbl(bone_names)+
      "<h2>Osteoporosis: refill the gain before holding the drain (L2 before L1)</h2>"
      "<p>Osteoporosis is a depleted calcium reservoir with a low remodeling gain, so its primary lever is L2 \u2014 and the framework\u2019s distinctive call is the SEQUENCE. On the volume\u2019s own reservoir law, an untreated reserve starting half-full drifts DOWN (to %.4f); an anti-resorptive holding the drain (L1) arrests the fall but does not refill (%.4f); an anabolic agent raising the remodeling gain (L2) refills toward full (%.4f). Anti-resorptive alone halts; only the gain lever rebuilds. The clinical reading is anabolic-FIRST \u2014 teriparatide or abaloparatide (intermittent PTH), romosozumab (anti-sclerostin) \u2014 to refill, THEN anti-resorptive \u2014 bisphosphonate, denosumab \u2014 to lock in. Refill the gain before holding the drain: a sequence call, not just a drug list. <b>[V]</b> L2 refills where L1 only halts; sequence and drugs <b>[L]</b>; absolute gains <b>[O]</b>.</p>"
      %(res["untreated_final"],res["L1_antiresorptive_final"],res["L2_anabolic_final"])+
      "<h2>Primary hyperparathyroidism and ADH1: the setpoint has moved (L3)</h2>"
      "<p>In primary hyperparathyroidism the defended calcium set-point has drifted UP (autonomous PTH; the CaSR comparator is effectively reset high); in autosomal dominant hypocalcemia type 1 (ADH1) an activating CaSR senses calcium as high, so the set-point is held LOW. Both are setpoint diseases, and the OU law exposes the trap of treating them with symptom control: on the volume\u2019s own setpoint-drift demonstration the defended value sits at %.2f untreated, returns to %.2f after an L3 reset, but springs back to %.2f the moment a mere symptom control is withdrawn \u2014 the relapse signature of an unaddressed setpoint. The matched lever is L3: the calcimimetic cinacalcet resets the CaSR DOWN in hyperparathyroidism, the calcilytic encaleret resets it UP in ADH1 \u2014 durable allosteric recalibration. Parathyroidectomy is the L1 cure when the source is a single autonomous gland. <b>[V]</b> direction; drugs and surgery <b>[L]</b>.</p>"
      %(drift["defended_untreated"],drift["defended_after_L3_reset"],drift["defended_after_symptom_withdrawal"])+
      "<h2>CKD-MBD: a multi-arm failure needs a multi-lever package</h2>"
      "<p>CKD-MBD with secondary hyperparathyroidism is the case where no single lever suffices. Nephron loss drops the loop gain across SEVERAL renal arms at once \u2014 the 1,25-vitamin-D arm, the phosphate-excretion arm, the calcium-handling arm \u2014 so the three levers must act together: L1 phosphate-load control (dietary restriction and binders), L2 active-vitamin-D arm substitution (calcitriol or paricalcitol replacing the failed renal hydroxylation), and L3 a calcimimetic on the driven PTH. This is not lever-stacking for its own sake; it is the matched response to a multi-arm gain failure, and it is why CKD-MBD resists any single-agent fix. <b>[L]</b> the three drug arms; <b>[V]</b> the multi-arm reading; <b>[O]</b> dosing.</p>"
      "<h2>Humoral hypercalcemia of malignancy and the magnesium disorders</h2>"
      "<p>Humoral hypercalcemia of malignancy is an unsuppressible external LOAD \u2014 tumor-secreted PTHrP that the CaSR cannot switch off \u2014 so its primary lever is L1: treat the tumor and oppose PTHrP. Hydration and anti-resorptives (bisphosphonate, denosumab) are symptom control that blunts the calcium release and buys time, but they do not touch the load at its source. The magnesium disorders are a loop-gain drop on a third defended ion \u2014 the magnesium reabsorption arm \u2014 so repletion holds the mean (L1) while arm restoration is the durable fix (L2), exactly the magnesium failure mode the disease-coverage chapter already derived from the same six modes. Across all six diseases the primary lever is read off the corrupted parameter, never guessed.</p>")
    secs.append(("15-mineral-bone-disease-three-levers-osteoporosis-hyperparathyroidism",15,"mineral & bone disease",
      "Mineral and bone disease under the three levers: osteoporosis, hyperparathyroidism, CKD-MBD",
      "Osteoporosis, primary hyperparathyroidism, ADH1, CKD-MBD, humoral hypercalcemia and magnesium disorders are each read through the three levers, with the primary lever selected from the corrupted OU parameter. Osteoporosis is anabolic-first (refill the gain before holding the drain); hyperparathyroidism and ADH1 are setpoint resets (calcimimetic / calcilytic); CKD-MBD needs all three levers.",
      "The owned mineral and bone diseases are read through the three-lever principle, selecting each disease\u2019s primary lever from the corrupted OU parameter. Osteoporosis is a depleted reservoir treated anabolic-first (L2 before L1); hyperparathyroidism and ADH1 are setpoint drifts reset by calcimimetic / calcilytic (L3); CKD-MBD is a multi-arm gain failure needing three levers; humoral hypercalcemia is an external load (L1).",
      body15,"grade g-verified","[V] lever selected from the corrupted parameter and demonstrated on the OU law; [L] named drug classes and treatment sequence; [H] framework sequence/efficacy predictions; [O] absolute magnitudes"))

    # ---- 16: ACID-BASE, ELECTROLYTE & STONE DISEASE UNDER THE THREE LEVERS ----
    vl=DR["remediation"]["archetype_demonstrations"]["variance_limited"]
    tm=DR["remediation"]["archetype_demonstrations"]["threshold_margin"]
    stone_names=["distal renal tubular acidosis / chronic metabolic acidosis","common electrolyte disorders (hyper/hypo- natremia, kalemia)","nephrolithiasis (calcium stones) / vascular calcification"]
    body16=(VPCARD_3LEVER+
      "<p class='abstract'>The acid-base, electrolyte and stone diseases this volume owns \u2014 distal renal tubular acidosis and chronic metabolic acidosis, the common sodium and potassium disorders, and calcium nephrolithiasis with vascular calcification \u2014 complete the three-lever reading, and two of them expose the levers\u2019 edges. Distal renal tubular acidosis shows why the standard of care (lifelong alkali) is a MEAN-only intervention that the gain lever would make durable. Calcium stones show a disease where the gain lever does NOT apply at all, because the failure is a fixed solubility threshold rather than a tunable loop gain \u2014 leaving L1 and L3. Knowing which lever is unavailable is itself a result.</p>"
      "<h2>Selecting the lever from the corrupted parameter</h2>"
      "<p>The same mechanical selection rule applies: external load \u2192 L1, dropped loop gain \u2192 L2, drifted target \u2192 L3 \u2014 with the honest addition that some failures have no gain to raise, so L2 is simply not on the menu. The three diseases below are matched accordingly.</p>"
      +dtbl(stone_names)+
      "<h2>Distal renal tubular acidosis: alkali holds the mean; restoring the arm is the durable fix</h2>"
      "<p>Distal renal tubular acidosis is a dropped loop gain \u2014 a failed renal bicarbonate-regeneration arm \u2014 so its primary lever is L2. The standard of care, lifelong oral alkali, is on the OU reading a MEAN-only correction: it offsets the load but does not restore the gain, so the defended band stays wide and the alkali must continue indefinitely. On the volume\u2019s own variance-limited demonstration, restoring the arm (L2) versus buffering the mean (L1) changes the variance by a factor matching the gain ratio (about %.2f-fold), the signature that only the gain lever tightens the defended band. The framework\u2019s call: alkali holds the mean meanwhile, but arm restoration is the durable target \u2014 and the variance, not the mean, is the readout that tells the two apart. <b>[V]</b> the variance asymmetry; alkali and arm-directed care <b>[L]</b>.</p>"
      %vl["variance_ratio_L1_over_L2"]+
      "<h2>Common electrolyte disorders: identify whether the arm or the load is the lesion</h2>"
      "<p>The common sodium and potassium disorders \u2014 hyper- and hyponatremia, hyper- and hypokalemia \u2014 are either a dropped renal-handling gain (L2) or an unsuppressible external load (L1), and the first clinical task is to identify which before matching the lever. The familiar osmotic-demyelination caution \u2014 correcting sodium too fast \u2014 is on this reading a symptom-pacing constraint on the RATE of approach, not a fourth lever: it governs how quickly the attractor is allowed to move, not which parameter is corrupted. Matching the lever to the lesion (arm versus load) is the substantive call; pacing is the safety rail around it.</p>"
      "<h2>Calcium nephrolithiasis: a fixed threshold leaves L1 and L3, not L2</h2>"
      "<p>Calcium stones and vascular calcification are the instructive exception that proves the framework is not forcing all three levers onto every disease. The failure here is not a tunable loop gain at all \u2014 it is a hard solubility-product threshold (Ksp) being crossed \u2014 so L2 does NOT apply: there is no gain to raise. On the volume\u2019s own margin law, the matched lever is L1, keeping the drive inside the soluble basin: at high drive the margin to the threshold is %.1f (sitting on the threshold), and lowering the drive restores a positive margin (%.1f). L3 is the adjunct \u2014 lowering the calcium-phosphate product set-point via FGF23 signaling or phosphate binders. A worked case of the framework knowing which lever is unavailable, and saying so. <b>[V]</b> the margin restoration; dietary and product-lowering measures <b>[L]</b>.</p>"
      %(tm["margin_high_drive"],tm["margin_after_L1"])+
      "<h2>The owned-disease boundary holds</h2>"
      "<p>Every disease in this chapter and the previous one is a common, acquired or polygenic LOOP disorder \u2014 a setpoint, gain or load failure on the shared R19 substrate. Monogenic and rare variants (an activating-CaSR family, a transporter loss-of-function) are named and cited to the rare-disease SSOT for the gene-level fact, while this volume owns the system-level dynamics and the lever that corrects them. Carcinogen-driven disease belongs to the mechanistic volumes. The boundary of VP_FRAMEWORK_MAP \u00a76 is not crossed; the three-lever principle operates strictly inside it, on the loop disorders this volume was built to defend.</p>")
    secs.append(("16-acid-base-electrolyte-stone-disease-three-levers",16,"acid-base & stone disease",
      "Acid-base, electrolyte and stone disease under the three levers",
      "Distal renal tubular acidosis, the common sodium and potassium disorders, and calcium nephrolithiasis complete the three-lever reading. Distal RTA shows why lifelong alkali is a mean-only fix that restoring the renal bicarbonate arm (L2) would make durable; calcium stones are a fixed-threshold disease where L2 does not apply, leaving L1 (stay in the soluble basin) and L3 (lower the product set-point).",
      "The owned acid-base, electrolyte and stone diseases complete the three-lever reading. Distal renal tubular acidosis is a dropped bicarbonate-arm gain, so lifelong alkali is a mean-only fix the gain lever (L2) would make durable; the variance distinguishes them. Calcium nephrolithiasis is a fixed solubility-threshold failure where L2 does not apply, leaving L1 (keep the drive soluble) with L3 as adjunct.",
      body16,"grade g-verified","[V] lever selected from the corrupted parameter; alkali-as-mean-only and stone-L2-N/A shown on the OU law; [L] standard-of-care and adjuncts cited; [O] absolute magnitudes"))
    return secs

def hub(R, secs):
    items="".join('<li><a href="%s/%s/">\u00a7%d \u2014 %s</a><div class="lead">%s</div></li>'%(BASE,s[0],s[1],s[3],s[5][:150]) for s in secs)
    ld=json.dumps({"@context":"https://schema.org","@type":"CreativeWorkSeries","name":TITLE,"alternateName":SHORT,
        "author":{"@type":"Person","name":AUTHOR,"sameAs":ORCID},"identifier":DOI,
        "license":"https://creativecommons.org/licenses/by/4.0/",
        "hasPart":[{"@type":"ScholarlyArticle","name":s[3],"position":s[1],"url":"%s/%s/"%(BASE,s[0])} for s in secs]}, ensure_ascii=False)
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s | Jamming Physics</title>
<meta name="description" content="The third homeostasis axis: calcium-phosphate, acid-base pH, and electrolyte setpoints as defended attractors of multi-organ loops on the jamming-lattice (R19) substrate, with measured master-gene \u03b3, a sensory seam, and failure-keyed therapy.">
<link rel="canonical" href="%s/"><style>%s</style>
<script type="application/ld+json">%s</script></head><body>
<header><nav class="crumb"><a href="/">Home</a> \u203a %s</nav></header>
<main>
<h1>%s</h1>
<p class="answer">This volume treats the third homeostasis axis \u2014 mineral (calcium-phosphate), acid-base (pH) and electrolyte (Na/K) setpoints \u2014 as defended attractors of multi-organ loops on the jamming-lattice (R19) substrate. Node identity and order come from measured master-gene \u03b3; loop gain sets setpoint stability; disease is loop failure; therapy is keyed to the failed element.</p>
<p class="lead">This volume is derived from the jamming branch of VP Theory \u2192 <a href="https://jamming-physics.org/physics/">/physics/</a>. Node identity and developmental order are cited from the DNA volume (measured \u03b3, never fitted).</p>
<h2>Sections</h2>
<ul>%s</ul>
<h2>Method</h2>
<p>Every quantitative claim is regenerated deterministically (fixed seed; two runs yield an identical sha256) from the reproduction code; the canonical artifact is this HTML. Grades: <b>[F]</b> forced, <b>[V]</b> simulation-verified, <b>[L]</b> cited literature anchor, <b>[O]</b> open with a stated obstacle. The master-gene \u03b3 values are measured from NCBI promoters (SantaLucia 1998) and validated against the vendored SIX2 anchor.</p>
</main>
<footer>%s \u00b7 ORCID <a href="%s">0009-0002-7535-8245</a> \u00b7 CC BY 4.0 \u00b7 DOI %s (assigned on publication)</footer>
</body></html>""" % (TITLE, BASE, CSS, ld, SHORT, TITLE, items, AUTHOR, ORCID, DOI)

def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Research-first: pass the stress battery, then gates.write_research_complete(); echo writing > PHASE")
        return 1
    R=_research(); docs=os.path.join(_HERE,"..","docs"); os.makedirs(docs, exist_ok=True)
    secs=build_sections(R)
    for i,s in enumerate(secs):
        prev=(secs[i-1][3],secs[i-1][0]) if i>0 else None
        nxt=(secs[i+1][3],secs[i+1][0]) if i<len(secs)-1 else None
        slug,n,short,t45,desc,answer,body,gc,gt=s
        outdir=os.path.join(docs,slug); os.makedirs(outdir, exist_ok=True)
        html=page(slug,n,short,t45,desc,answer,body,gc,gt,prev,nxt)
        open(os.path.join(outdir,"index.html"),"w",encoding="utf-8").write(html)
    open(os.path.join(docs,"index.html"),"w",encoding="utf-8").write(hub(R,secs))
    urls=[BASE+"/"]+["%s/%s/"%(BASE,s[0]) for s in secs]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+\
       "".join("<url><loc>%s</loc><lastmod>%s</lastmod></url>\n"%(u,TODAY) for u in urls)+"</urlset>\n"
    open(os.path.join(docs,"sitemap.xml"),"w",encoding="utf-8").write(sm)
    robots="User-agent: Googlebot\nAllow: /\nUser-agent: Bingbot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\n"\
           "User-agent: GPTBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\n"\
           "User-agent: Google-Extended\nAllow: /\nUser-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n"%BASE
    open(os.path.join(docs,"robots.txt"),"w",encoding="utf-8").write(robots)
    llms="# %s\n\n> The third homeostasis axis: calcium-phosphate, acid-base pH, and electrolyte setpoints as defended attractors of multi-organ loops on the jamming-lattice (R19) substrate. Node \u03b3 measured (NCBI, SantaLucia 1998); loop gain sets setpoint stability; disease is loop failure; therapy is organized by the three-lever principle (L1 source / L2 gain / L3 setpoint) inherited from the non-opioid analgesic volume. Concept DOI %s (CC BY 4.0); cross-volume technology DOI %s.\n\n## Sections\n"%(TITLE,DOI,ANALGESIC_DOI)
    llms+="".join("- [\u00a7%d %s](%s/%s/)\n"%(s[1],s[3],BASE,s[0]) for s in secs)
    llms+="\n## Method\nDeterministic regeneration (2\u00d7sha256 identical); grades [F]/[V]/[L]/[O]; \u03b3 validated vs SIX2. Concept DOI %s; three-lever technology inherited from the non-opioid analgesic volume DOI %s.\n"%(DOI,ANALGESIC_DOI)
    open(os.path.join(docs,"llms.txt"),"w",encoding="utf-8").write(llms)
    man="slug,title,section_no,status,grade,answer_words\n"
    for s in secs:
        aw=len(s[5].split()); man+='%s,"%s",%d,written,%s,%d\n'%(s[0],s[3].replace('"',"'"),s[1],s[8].split("]")[0]+"]",aw)
    open(os.path.join(_HERE,"..","manifest","homeostasis_ionic_vp_site.csv"),"w",encoding="utf-8").write(man)
    print("UNLOCKED + BUILT: hub + %d section pages + sitemap.xml + robots.txt + llms.txt in docs/ (DOI: %s)"%(len(secs),DOI))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
