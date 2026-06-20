#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Musculoskeletal WRITING phase: per-title canonical SEO HTML generator (VP-SPEC v1.8).

HARD RULE: refuses while gates.writing_locked() is True (research signed off + PHASE=="writing").
When UNLOCKED it emits, into docs/, the canonical HTML site (C2/C4):
  - docs/<paper_id>/<slug>/index.html      one answer-first page per title/section (sec 6)
  - docs/<paper_id>/index.html             paper hub
  - docs/<paper_id>/_meta.json             summary card (sec 9)
  - docs/index.html                        top-level hub
  - docs/sitemap.xml, robots.txt, llms.txt (sec 6-R.5)
  - docs/assets/css/site.css               external stylesheet (no inline CSS in pages)
Each page: <p class="answer"> 40-60 words self-contained; .abstract with the key unicode result;
.claim-strip (grade + GitHub repro + DOI); aside.vp-card per cited locked quantity; JSON-LD
ScholarlyArticle + BreadcrumbList; canonical link; ENGLISH body (C0); honest grades + [O] obstacles (C3).
ALL numbers are pulled LIVE from the deterministic engine (C1) -- nothing is hand-entered.
"""
import os, sys, json, html, datetime, re
_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.join(_HERE, "..")
for sub in ("_engine", "_verify", "_oncology"):
    sys.path.insert(0, os.path.join(_PKG, "repro", sub))
import importlib
gates = importlib.import_module("gates")

# --------------------------------------------------------------------------- identity (CHARTER)
PAPER_ID = "musculoskeletal_vp_site"
CODE     = "msk"
TITLE    = "Musculoskeletal Emergence: Muscle Actuation, Cartilage and Bone as Load-Bearing Jammed Matter"
ABBR     = "Musculoskeletal Emergence"
AUTHOR   = "Young Jae Lee"
ORCID    = "https://orcid.org/0009-0002-7535-8245"
LICENSE  = "https://creativecommons.org/licenses/by/4.0/"
DOMAIN   = "https://jamming-physics.org"
REPO     = "https://github.com/rego093-sketch/jamming-physics"
REPRO    = REPO + "/tree/main/repro/" + PAPER_ID + "/"
CONCEPT_DOI      = "10.5281/zenodo.20755760"                       # this volume's CONCEPT (all-versions) DOI
DOI_URL          = "https://doi.org/" + CONCEPT_DOI
DOI_NOTE         = "DOI: " + CONCEPT_DOI + " (concept)"
ANALGESIC_DOI    = "10.5281/zenodo.20733420"                       # inherited non-opioid analgesic three-lever technique
ANALGESIC_DOI_URL = "https://doi.org/" + ANALGESIC_DOI
DATE     = datetime.date.today().isoformat()
DNA_HUB  = DOMAIN + "/dna/"        # 4D DNA Blueprint volume owns the measured master-gene gamma
PHY_HUB  = DOMAIN + "/physics/"    # VP Theory volume owns the jamming substrate / R19 switch
NEU_HUB  = DOMAIN + "/neuro/"      # Neural Emergence Chain volume owns the motor command

def esc(s):
    return html.escape(str(s), quote=True)

# --------------------------------------------------------------------------- live numbers (C1)
def load_numbers():
    eng = importlib.import_module("vp_msk_engine")
    st  = importlib.import_module("stress_tests")
    on  = importlib.import_module("carcinogen_dose_response")
    em   = eng.emerge_organs()
    batt = st.run_battery()
    suites = {s["target"]: s for s in batt["suites"]}
    dis = st.run_disease_suite()
    dis_suites = {s["target"]: s for s in dis["suites"]}
    trx = st.run_treatment_suite()
    trx_suites = {s["target"]: s for s in trx["suites"]}
    anlg = st.run_analgesia_suite()
    anlg_suites = {s["target"]: s for s in anlg["suites"]}
    onc = on.run_oncology()
    return {"em": em, "organs": {o["organ"]: o for o in em["organs"]}, "suites": suites,
            "dis": dis, "dis_suites": dis_suites, "trx": trx, "trx_suites": trx_suites,
            "anlg": anlg, "anlg_suites": anlg_suites, "onc": onc,
            "gammas": {o["organ"]: o["gamma"] for o in em["organs"]}}

# --------------------------------------------------------------------------- vp-cards (6-R.2)
def vp_card(locked, head, meaning, gtag, gword, href, link_text):
    # `meaning` and `head` are author-supplied HTML (they carry entities like &gamma; / &mdash; that must
    # render); only the machine-supplied fields (grade tokens, URL, link text) are escaped.
    return ('<aside class="vp-card" data-locked="%s"><b>%s</b> &mdash; %s <b>%s</b> %s. '
            '<a href="%s" rel="noopener">%s</a></aside>'
            % (esc(locked), head, meaning, esc(gtag), esc(gword), esc(href), esc(link_text)))

def gamma_card(master, organ, gamma):
    return vp_card("gamma_" + master, "&gamma;(%s) = %.4f" % (master, gamma),
        "master-gene composition &gamma; = &minus;mean nearest-neighbour stacking &Delta;G&#8323;&#8327; "
        "(SantaLucia 1998) over the %s proximal promoter; a read-only MEASURED input, never fitted." % organ,
        "[V]", "verified (measured)", DNA_HUB, "canonical derivation: 4D DNA Blueprint")

CARD_SPINODAL = vp_card("spinodal", "s* = 2(&gamma;/3)<sup>3/2</sup>",
    "spinodal of the R19 bistable switch &mdash; the drive at which the low (resorbed/off) basin vanishes; "
    "the load-bearing YIELD threshold.", "[F]", "forced", PHY_HUB, "canonical substrate: VP Theory")
CARD_BARRIER = vp_card("barrier", "&Delta;V = &gamma;&sup2;/4",
    "escape-barrier height of the R19 double well; a carcinogen lowers it toward 0 as the aberrant drive "
    "approaches the spinodal.", "[F]", "forced", PHY_HUB, "canonical substrate: VP Theory")
CARD_NOCICEPTION = vp_card("nociceptive_rate",
    "rate &asymp; exp(&minus;&Delta;V<sub>eff</sub>/D),&nbsp; &Delta;V<sub>eff</sub> = max(0, &gamma;&sup2;/4 + "
    "&Delta;V<sub>L1</sub> &minus; &kappa;h)",
    "nociception as a THRESHOLD-CROSSING (Kramers) rate on the SAME R19 barrier: a noxious drive h erodes the "
    "barrier; L1 raises it (&Delta;V<sub>L1</sub>), L2 lowers h, L3 scales the downstream gain. Three-lever "
    "technique inherited from the VP non-opioid analgesic volume.", "[L]", "cited technique",
    ANALGESIC_DOI_URL, "inherited: non-opioid analgesic threshold logic (DOI 10.5281/zenodo.20733420)")

# --------------------------------------------------------------------------- section bodies
def sec_emergence(N):
    em = N["em"]; org = N["organs"]; order = em["gamma_order_ascending"]; g = N["gammas"]
    rows = "".join("<tr><td>%s</td><td>%s</td><td>%.4f</td><td>%.4f</td><td>%.3f</td></tr>"
        % (esc(o), esc(org[o]["master"]), org[o]["gamma"], org[o]["functional_spinodal"], org[o]["rel_size_dwell"])
        for o in order)
    answer = ("Four musculoskeletal organs emerge deterministically from a single MEASURED master-gene "
        "number &gamma; on the jamming substrate: skeletal&nbsp;muscle (MYOD1, &gamma;=%.4f), cartilage "
        "(SOX9, %.4f), limb&nbsp;skeleton (TBX5, %.4f) and bone (RUNX2, %.4f). &gamma; is read-only and "
        "never fitted; identity and order are inherited from the DNA volume."
        % (g["skeletal_muscle"], g["cartilage"], g["limb_skeleton"], g["bone"]))
    abstract = ("Each organ is an R19 bistable switch whose functional spinodal and relative size follow "
        "from its measured &gamma;. The four values order as RUNX2 %.4f &lt; TBX5 %.4f &lt; SOX9 %.4f &lt; "
        "MYOD1 %.4f, fixing a developmental THRESHOLD ranking tested in &sect;5. No coefficient is tuned: "
        "&gamma; is imported from the 4D DNA Blueprint volume."
        % (g["bone"], g["limb_skeleton"], g["cartilage"], g["skeletal_muscle"]))
    body = (
      "<h2>One measured number per organ</h2>"
      "<p>The musculoskeletal package emerges its organs by simulation, not by assertion. Organ identity and "
      "developmental order are owned by the DNA morphogenesis gene-clock and cited here; this volume is the "
      "single source only for the load-bearing DYNAMICS (&sect;2&ndash;&sect;6) and the carcinogen "
      "dose-response (&sect;7).</p>"
      "<p>Every organ is built as the same R19 bistable switch parameterised by one read-only quantity: the "
      "master-gene composition &gamma; = &minus;mean nearest-neighbour stacking &Delta;G&#8323;&#8327; "
      "(SantaLucia 1998) over the proximal promoter. RUNX2's &gamma; was MEASURED this cycle from "
      "NC_000006.12 (window TSS&minus;2000..+500, MANE NM_001024630.4) by the identical pipeline; "
      "&gamma;=%.4f is measured, not fitted.</p>"
      "<h2>Emergent table (all values live from the engine)</h2>"
      "<table><thead><tr><th>organ</th><th>master</th><th>&gamma;</th><th>functional spinodal</th>"
      "<th>relative size</th></tr></thead><tbody>%s</tbody></table>"
      "<p>The functional spinodal s* = 2(&gamma;/3)<sup>3/2</sup> increases monotonically with &gamma;, so a "
      "lower-&gamma; organ crosses its switching threshold under a smaller drive. Relative size scales as "
      "&gamma;<sup>3/2</sup> through the dwell law. These primitives are inherited from the jamming substrate "
      "and are not re-derived here.</p>" % (g["bone"], rows))
    cards = [gamma_card("MYOD1", "skeletal_muscle", g["skeletal_muscle"]),
             gamma_card("SOX9", "cartilage", g["cartilage"]),
             gamma_card("TBX5", "limb_skeleton", g["limb_skeleton"]),
             gamma_card("RUNX2", "bone", g["bone"]), CARD_SPINODAL]
    oneliner = ("Four organs emerge from measured master-gene &gamma; (RUNX2 %.4f &lt; TBX5 %.4f &lt; SOX9 "
        "%.4f &lt; MYOD1 %.4f); &gamma; is read-only, never fitted."
        % (g["bone"], g["limb_skeleton"], g["cartilage"], g["skeletal_muscle"]))
    return answer, abstract, body, cards, oneliner

def sec_t1(N):
    v = N["suites"]["T1"]["value"]; ff = v["fusion_freq_hz"]; band = v["fusion_band_hz"]
    tr = v["fusion_tracking"]
    trtxt = ", ".join("%g&nbsp;ms&rarr;%g&nbsp;Hz" % (t["ct_ms"], t["fusion_freq_hz"]) for t in tr)
    answer = ("Twitch summation reproduces the muscle force-frequency relationship: individual twitches "
        "(2nd-order critically-damped activation impulses) superpose into a smooth fused tetanus at "
        "%g&nbsp;Hz, inside the cited fusion band %g&ndash;%g&nbsp;Hz. The fusion frequency tracks 1/&tau; "
        "across fast&harr;slow fibres &mdash; a verified, anchor-respecting result [V]."
        % (ff, band[0], band[1]))
    abstract = ("Mean force rises monotonically with stimulation frequency and the fusion index falls below "
        "0.10 at %g&nbsp;Hz (band %g&ndash;%g&nbsp;Hz). Shortening the cited contraction time raises the "
        "fusion frequency in step (%s), confirming the 1/&tau; law with no tuning. The tetanus:twitch "
        "AMPLITUDE ratio is left uncalibrated [O]: linear superposition has no force ceiling."
        % (ff, band[0], band[1], trtxt))
    body = (
      "<h2>Twitches that add up</h2>"
      "<p>A single motor spike drives a unit twitch modelled as the impulse response of a 2nd-order "
      "critically-damped activation&rarr;force cascade k(u) = (u/&tau;)&middot;e<sup>1&minus;u/&tau;</sup>, "
      "peaking at the cited contraction time &tau;. Repetitive stimulation superposes these twitches; as the "
      "inter-spike interval falls below &tau; the ripples merge into a fused plateau.</p>"
      "<p>Sweeping stimulation frequency, the steady mean force increases monotonically and the fusion index "
      "(ripple/peak) drops below 0.10 at %g&nbsp;Hz, within the cited whole-muscle fusion band "
      "%g&ndash;%g&nbsp;Hz. This is the discriminant: a non-summating actuator would not fuse.</p>"
      "<h2>Fusion tracks 1/&tau; (no tuning)</h2>"
      "<p>Across the physiological contraction-time range the fusion frequency moves inversely with &tau;: "
      "%s. Faster fibres fuse at higher frequency, exactly as the 1/&tau; law requires, and the anchor was "
      "never adjusted to hit the band &mdash; the shape is emergent.</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>The tetanus:twitch amplitude ratio from pure linear superposition has no contractile force ceiling, "
      "so it is uncalibrated and graded [O]. A bounded ratio needs Ca&sup2;&#8314;/cross-bridge "
      "activation-saturation kinetics whose half-activation constant the jamming substrate does not fix; "
      "tuning it to the cited ~3&ndash;5 would violate No-Tuning.</p>" % (ff, band[0], band[1], trtxt))
    cards = [gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"])]
    oneliner = ("Twitches superpose into fused tetanus at %g&nbsp;Hz (band %g&ndash;%g) and fusion tracks "
        "1/&tau; [V]; amplitude ratio uncalibrated [O]." % (ff, band[0], band[1]))
    return answer, abstract, body, cards, oneliner

def sec_t2(N):
    v = N["suites"]["T2"]["value"]; pl = v["plateau_um"]; pb = v["plateau_band_um"]
    z = v["zero_force_um"]; za = v["anchor_zero_um"]
    answer = ("Active muscle force equals the thin/thick filament OVERLAP &mdash; the load-bearing contact "
        "number, the jamming order parameter. From cited frog filament geometry the model produces the "
        "classic length-tension curve with its plateau at %g&ndash;%g&nbsp;&micro;m (cited optimum "
        "%g&ndash;%g) and zero force near %g&nbsp;&micro;m (cited %g) [V]."
        % (pl[0], pl[1], pb[0], pb[1], z, za))
    abstract = ("Force is the length of thin filament engaged within the cross-bridge-bearing zone of the "
        "thick filament, with a double-overlap penalty on the ascending limb. Using only cited "
        "Gordon-Huxley-Julian (1966) lengths, the plateau lands at %g&ndash;%g&nbsp;&micro;m and the "
        "descending limb reaches zero at %g&nbsp;&micro;m &mdash; the cited curve, geometry [L], peak [V]."
        % (pl[0], pl[1], z))
    body = (
      "<h2>Force is a contact number</h2>"
      "<p>In the jamming picture, active tension counts engaged cross-bridges, and that count is purely "
      "geometric: it is the overlap between the actin thin filament and the cross-bridge-bearing region of "
      "the myosin thick filament. Overlap is the load-bearing contact number &mdash; the same order parameter "
      "that governs every jammed contact network.</p>"
      "<p>With the cited half-sarcomere geometry (thick 1.60&nbsp;&micro;m, bare zone 0.20&nbsp;&micro;m, thin "
      "1.025&nbsp;&micro;m), the engaged overlap rises on the ascending limb, saturates across the plateau "
      "where the thin tips span the full bridge region, and falls on the descending limb as the filaments "
      "pull apart.</p>"
      "<h2>The cited curve, reproduced</h2>"
      "<p>The plateau of maximal force sits at sarcomere length %g&ndash;%g&nbsp;&micro;m, matching the cited "
      "optimum %g&ndash;%g&nbsp;&micro;m, and the descending limb crosses zero near %g&nbsp;&micro;m (cited "
      "%g&nbsp;&micro;m). A double-overlap penalty produces the short-length force drop. The geometry is cited "
      "[L]; the curve peak and intercept are verified [V].</p>" % (pl[0], pl[1], pb[0], pb[1], z, za))
    cards = [gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"])]
    oneliner = ("Active force = filament overlap (contact number); plateau %g&ndash;%g&nbsp;&micro;m, zero "
        "near %g&nbsp;&micro;m, matching the cited length-tension curve [V]." % (pl[0], pl[1], z))
    return answer, abstract, body, cards, oneliner

def sec_t3(N):
    v = N["suites"]["T3"]["value"]; g = N["gammas"]["bone"]
    thr = v["yield_threshold_spinodal"]; cr = v["crossing_load"]; jp = v["max_density_jump"]
    hy = v["hysteresis_area"]; sub = v["sub_threshold_density"]; sup = v["supra_threshold_density"]
    answer = ("Bone remodelling is a jamming yield transition. Bone density is the R19 state, mechanical load "
        "is the drive, and the spinodal s*=%.4f IS the yield threshold. Sustained supra-threshold load flips "
        "density to the dense basin (jump %.2f); the load loop shows hysteresis (area %.2f) &mdash; bone "
        "memory. Threshold and memory are FORCED by the bistable substrate [F]." % (thr, jp, hy))
    abstract = ("A quasi-static load sweep crosses to the dense basin only above the spinodal (crossing load "
        "%.2f &gt; 0): half-threshold load leaves density at %.2f while 1.5&times; threshold drives it to "
        "%.0f. The up and down branches enclose a hysteresis loop (area %.2f), the mechanical memory behind "
        "Wolff's law. Setpoint cited (Frost mechanostat) [L]; absolute density [O]." % (cr, sub, sup, hy))
    body = (
      "<h2>Density as a bistable state</h2>"
      "<p>Wolff's law &mdash; bone adapts its density to the loads it bears &mdash; is, in the jamming "
      "framework, a yield/unjamming transition. Bone density is the settled R19 state: a resorbed (low) basin "
      "and a dense (high) basin separated by a barrier. Mechanical load is the drive h that tilts the double "
      "well.</p>"
      "<p>The spinodal s* = 2(&gamma;/3)<sup>3/2</sup> = %.4f (with the bone master RUNX2, &gamma;=%.4f) is "
      "exactly the yield threshold: below it the resorbed basin survives; above it that basin vanishes and "
      "density jumps to the dense state. The transition is near-discontinuous, with a density jump of %.2f at "
      "the crossing.</p>"
      "<h2>Hysteresis = bone memory</h2>"
      "<p>Loading then unloading does not retrace the same path: the up and down branches enclose a hysteresis "
      "loop of area %.2f. The dense state, once formed, persists as the load is removed &mdash; the mechanical "
      "memory that lets trained bone stay strong. Half-threshold load leaves density at %.2f (no spurious "
      "formation); 1.5&times; threshold drives it to full mineralization (%.0f).</p>"
      "<h2>Grades</h2>"
      "<p>The existence of a threshold, the near-discontinuous jump and the hysteresis loop are FORCED by the "
      "bistable substrate [F]. The numerical setpoint is anchored to the Frost mechanostat [L]. Absolute bone "
      "mineral density in g&middot;cm&#8315;&sup3; is not fixed by the substrate and is graded [O].</p>"
      % (thr, g, jp, hy, sub, sup))
    cards = [gamma_card("RUNX2", "bone", g), CARD_SPINODAL, CARD_BARRIER]
    oneliner = ("Bone density = R19 state, load = drive, spinodal %.4f = yield threshold; supra-threshold load "
        "flips density with hysteresis (memory) [F]." % thr)
    return answer, abstract, body, cards, oneliner

def sec_t4(N):
    v = N["suites"]["T4"]["value"]; g = N["gammas"]
    order = v["gamma_threshold_order_ascending"]
    answer = ("Developmental THRESHOLD order is read directly off &gamma;: the functional spinodal is monotone "
        "in &gamma;, so ranking the measured masters by &gamma; reproduces the cited patterning/"
        "differentiation sequence limb&nbsp;skeleton&rarr;cartilage&rarr;muscle (TBX5&rarr;SOX9&rarr;MYOD1) "
        "[V]. Absolute endochondral ossification timing is drive-gated and left open [O].")
    abstract = ("Sorting organs by ascending &gamma; gives %s. Over the three patterning/differentiation "
        "masters this is exactly the cited order TBX5(%.4f)&rarr;SOX9(%.4f)&rarr;MYOD1(%.4f). RUNX2's low "
        "&gamma;=%.4f ranks bone's switching threshold earliest &mdash; consistent with early "
        "osteochondroprogenitor RUNX2 &mdash; but ossification waits on the cartilage template, so absolute "
        "timing is [O]." % (esc(order), g["limb_skeleton"], g["cartilage"], g["skeletal_muscle"], g["bone"]))
    body = (
      "<h2>Order without tuning</h2>"
      "<p>The growth plate's developmental ordering is not a free parameter here: it is a readout of the same "
      "&gamma; that built each organ. Because the functional spinodal increases monotonically with &gamma;, a "
      "lower-&gamma; master crosses its switching threshold under a smaller drive and is therefore ranked "
      "earlier.</p>"
      "<p>Ranking the measured patterning/differentiation masters by &gamma; gives "
      "limb&nbsp;skeleton&nbsp;(TBX5,&nbsp;%.4f)&rarr;cartilage&nbsp;(SOX9,&nbsp;%.4f)&rarr;"
      "muscle&nbsp;(MYOD1,&nbsp;%.4f) &mdash; the cited developmental sequence, reproduced from independently "
      "measured promoter numbers [V].</p>"
      "<h2>An honest negative: bone timing</h2>"
      "<p>The measured RUNX2 &gamma;=%.4f is the LOWEST of the four, so the &gamma;-rank places bone's "
      "switching THRESHOLD earliest. This is consistent with the documented early expression of RUNX2 in "
      "osteochondroprogenitors. It is NOT a claim that bone ossifies first: endochondral ossification is a "
      "STATE/drive-gated EVENT &mdash; the cartilage template must form and signal before mineralization "
      "proceeds. 'Parts present &ne; trait.' Absolute ossification timing is therefore graded [O] and not "
      "forced from &gamma;. The threshold-ordering result is reported only over the three patterning masters, "
      "where it holds exactly.</p>" % (g["limb_skeleton"], g["cartilage"], g["skeletal_muscle"], g["bone"]))
    cards = [gamma_card("TBX5", "limb_skeleton", g["limb_skeleton"]),
             gamma_card("SOX9", "cartilage", g["cartilage"]),
             gamma_card("MYOD1", "skeletal_muscle", g["skeletal_muscle"]),
             gamma_card("RUNX2", "bone", g["bone"]), CARD_SPINODAL]
    oneliner = ("&gamma;-rank reproduces limb&rarr;cartilage&rarr;muscle (TBX5&rarr;SOX9&rarr;MYOD1) [V]; bone "
        "ossification timing is drive-gated [O].")
    return answer, abstract, body, cards, oneliner

def sec_t5(N):
    v = N["suites"]["T5"]["value"]
    drop = v["force_drop_frac"]; tau = v["tau_recovered_s"]; band = v["anchor_band_s"]; rec = v["recovered_frac"]
    answer = ("Muscle fatigue is a reversible relaxation. Sustained maximal drive loads a slow adaptation "
        "variable that suppresses force, giving a monotone exponential decline to a plateau (here a %.0f%% "
        "loss) with time constant %g&nbsp;s, inside the cited band %g&ndash;%g&nbsp;s. Rest recovers force to "
        "%.0f%% &mdash; shape and reversibility verified [V], time constant cited [L]."
        % (drop * 100, tau, band[0], band[1], rec * 100))
    abstract = ("Under continuous drive the force follows F = 1 &minus; depth&middot;(1 &minus; "
        "e<sup>&minus;t/&tau;</sup>), declining monotonically by %.0f%% with a recovered time constant of "
        "%g&nbsp;s (cited band %g&ndash;%g&nbsp;s); on rest it returns to %.0f%% of baseline. A log-linear "
        "round-trip recovers the input &tau; across the physiological band. Decline magnitude is left open [O]."
        % (drop * 100, tau, band[0], band[1], rec * 100))
    body = (
      "<h2>A slow variable that gives way</h2>"
      "<p>Fatigue here is not damage; it is a reversible relaxation of a slow adaptation variable &phi; that "
      "accumulates under sustained drive and relaxes at rest. Force is suppressed in proportion to &phi;, so a "
      "maintained maximal contraction produces a monotone exponential decline toward a plateau: F = 1 &minus; "
      "depth&middot;(1 &minus; e<sup>&minus;t/&tau;</sup>).</p>"
      "<p>The simulated decline loses %.0f%% of force with a time constant of %g&nbsp;s, inside the cited "
      "sustained-MVC band %g&ndash;%g&nbsp;s. Removing the drive lets &phi; relax and force recovers to %.0f%% "
      "of baseline &mdash; the defining signature that this is fatigue, not injury.</p>"
      "<h2>Faithful, not fitted</h2>"
      "<p>A log-linear round-trip on the simulated curve recovers the input time constant across the whole "
      "physiological band (25, 60, 110&nbsp;s in &rarr; the same out), confirming the integrator is faithful "
      "and the constant is genuinely the cited one, not tuned. The reversible exponential SHAPE and recovery "
      "are verified [V]; the time constant is cited (Bigland-Ritchie) [L]; the absolute force-loss MAGNITUDE "
      "is not fixed by the substrate and is graded [O].</p>" % (drop * 100, tau, band[0], band[1], rec * 100))
    cards = [gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"])]
    oneliner = ("Sustained drive &rarr; reversible exponential force decline, &tau;&asymp;%g&nbsp;s (band "
        "%g&ndash;%g), recovery to %.0f%% [V]; magnitude [O]." % (tau, band[0], band[1], rec * 100))
    return answer, abstract, body, cards, oneliner

def sec_onco(N):
    onc = N["onc"]
    osteo = next(s for s in onc["sites"] if s["site"].startswith("osteosarcoma"))
    rr45 = osteo["RR_at_dose"]["0.45"]; rr90 = osteo["RR_at_dose"]["0.90"]
    answer = ("A carcinogen is a sustained aberrant drive that lowers the R19 escape barrier, so the "
        "malignant-crossing rate is Kramers-like and the dose-response RR(dose) is monotone and convex "
        "(accelerating). With the natural barrier scale it collapses to a universal law RR = "
        "e<sup>dose/dose*</sup> (RR&asymp;%.2f at 90%% of the yield drive) &mdash; shape verified [V], "
        "radiation anchor cited [L], absolute incidence open [O]." % rr90)
    abstract = ("Modelling the carcinogen as a barrier-lowering drive gives RR(dose)=rate(dose)/rate(0) that "
        "rises convexly with dose (RR&asymp;%.2f at 0.45, %.2f at 0.90 of the spinodal drive). The lineage "
        "&gamma; cancels in the ratio, so the NORMALISED dose-response is the universal convex law RR="
        "e<sup>dose/dose*</sup>. Radiation RR for bone sarcoma is cited [L]; absolute incidence and the "
        "genetic-dominant aetiology are open [O]." % (rr45, rr90))
    body = (
      "<h2>One kernel for cell fate and cancer</h2>"
      "<p>The cell-fate switch that emerges each organ is reused for oncology. A carcinogen acts as a "
      "sustained aberrant drive h_c that lowers the escape barrier out of the healthy basin; the "
      "malignant-crossing rate is Kramers-like, rate(h_c) = rate&#8320;&middot;e<sup>&minus;&Delta;V_eff/"
      "scale</sup>, with &Delta;V_eff&rarr;0 as the drive approaches the spinodal. The relative risk RR(dose) "
      "= rate(dose)/rate(0) is therefore monotone and convex &mdash; the signature of barrier-limited "
      "escape.</p>"
      "<p>With the natural Kramers scale (the barrier height &Delta;V = &gamma;&sup2;/4) the lineage &gamma; "
      "cancels in the ratio, and the normalised dose-response collapses to a single parameter-free law RR = "
      "e<sup>dose/dose*</sup>, where dose* is the spinodal drive. The curve gives RR&asymp;%.2f at 45%% and "
      "%.2f at 90%% of dose*. The SHAPE (monotone, convex, RR&gt;1) is verified on the substrate [V].</p>"
      "<h2>Lineage mapping (measured &gamma;)</h2>"
      "<p>Osteosarcoma is modelled on the osteoblast-lineage switch RUNX2 (bone, &gamma;=%.4f); soft-tissue "
      "sarcoma on the myogenic-lineage switch MYOD1 (muscle, &gamma;=%.4f) &mdash; MYOD1 is the canonical "
      "rhabdomyosarcoma marker. Because &gamma; cancels in RR, both sites share the same convex normalised "
      "curve; &gamma; sets only the absolute drive scale.</p>"
      "<h2>Two further sites, with an honest dose axis</h2>"
      "<p>The same kernel extends to <b>chondrosarcoma</b> (cartilage lineage, SOX9 &gamma;=%.4f) and "
      "<b>Ewing sarcoma</b> (a bone-associated small-round-cell tumour). For both, the driver is NOT an "
      "environmental exposure: chondrosarcoma is driven by IDH1/2 neomorphic metabolism (the 2-HG "
      "oncometabolite) and Ewing by the constitutive EWSR1&ndash;FLI1 fusion. The kernel still reproduces the "
      "barrier-lowering SHAPE, but the dose axis is then the NORMALISED aberrant drive, not a cited exposure "
      "dose, and that distinction is recorded as an open item [O]. Ewing's cell of origin is debated "
      "(mesenchymal / neural-crest), so RUNX2 is only a bone-mesenchyme context stand-in &mdash; the lineage "
      "assignment itself is graded [O].</p>"
      "<h2>What is cited, and what is NOT claimed</h2>"
      "<p>Radiation relative risk for bone sarcoma rising with cumulative dose is the cited anchor [L] (radium "
      "dial painters; Tucker et al. 1987; UNSCEAR). The open items [O], not overclaimed: (1) absolute "
      "incidence in cases per person-year &mdash; the kernel gives RELATIVE risk only, the baseline hazard is "
      "not fixed by the substrate; (2) osteosarcoma is predominantly GENETIC (RB1, TP53/Li-Fraumeni, Paget), "
      "so the dose-response applies only to the radiation-attributable fraction; (3) chemical "
      "soft-tissue-sarcoma dose-response has no clean cited anchor (confounded, low incidence); (4) for "
      "chondrosarcoma and Ewing the aetiology is metabolic/fusion-genetic, so there is no environmental "
      "exposure dose-response and the dose axis is the normalised drive only.</p>"
      % (rr45, rr90, N["gammas"]["bone"], N["gammas"]["skeletal_muscle"], N["gammas"]["cartilage"]))
    cards = [CARD_BARRIER, CARD_SPINODAL, gamma_card("RUNX2", "bone", N["gammas"]["bone"]),
             gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"]),
             gamma_card("SOX9", "cartilage", N["gammas"]["cartilage"])]
    oneliner = ("Carcinogen = barrier-lowering drive &rarr; Kramers RR(dose) collapses to universal convex "
        "RR=e<sup>dose/dose*</sup> [V] across four sites; radiation anchor [L]; incidence + fusion/metabolic "
        "aetiology [O].")
    return answer, abstract, body, cards, oneliner

# --------------------------------------------------------------------------- disease cards + sections
CARD_CLIFF = vp_card("dosage_cliff", "dosage* = (1/1.5)<sup>2/3</sup> &asymp; 0.763... &rarr; cliff at &frac23; of WT drive",
    "the WT switch is driven at 1.5&times; its spinodal; halving the master's dosage drops the drive below the "
    "spinodal, so the OFF basin no longer releases &mdash; a &gamma;-independent crossing CLIFF.",
    "[F]", "forced", PHY_HUB, "canonical substrate: VP Theory")

def _disease_strip_note(suite):
    """Inline honest-grade + cited-severity line reused inside disease bodies."""
    return ('<p class="abstract"><b>Cited severity (No-Tuning):</b> %s<br><b>Grade:</b> %s</p>'
            % (esc(suite["cited_severity"]), esc(suite["grade"])))

def sec_t7_master_dosage(N):
    s = {k: N["dis_suites"][k] for k in ("T7a", "T7b", "T7c", "T7d")}
    a = s["T7a"]; d = a["detail"]; cliff = a["value"]["critical_dosage_cliff"]
    wt_occ = a["value"]["wt_occupancy"]; het_occ = a["value"]["het_occupancy"]
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s (&gamma;=%.4f)</td><td>%.3f</td><td>%.3f</td><td>%s</td></tr>"
        % (esc(s[t]["target"]), esc(s[t]["disease"]), esc(s[t]["value"]["master"]), s[t]["value"]["gamma"],
           s[t]["value"]["wt_occupancy"], s[t]["value"]["het_occupancy"],
           "no" if not s[t]["value"]["het_crosses"] else "yes")
        for t in ("T7a", "T7b", "T7c", "T7d"))
    answer = ("Halving a master gene's dosage is a haploinsufficiency: it drops the organ's R19 switch drive "
        "below the spinodal, so the switch fails to cross from the OFF basin and development is delayed or "
        "incomplete. With WT occupancy %.2f, the heterozygote collapses to %.2f &mdash; reproducing the "
        "documented dysplasias of RUNX2, SOX9 and TBX5 loss. The crossing CLIFF at &#8532; of WT drive is "
        "FORCED by the substrate [F]." % (wt_occ, het_occ))
    abstract = ("The WT master drives its switch at 1.5&times; its spinodal; a 0.5 dosage halving lands it at "
        "0.75&times; spinodal, below the &gamma;-independent crossing cliff at dosage &asymp; %.3f. Occupancy "
        "is monotone in dosage, so the defect scales with loss; below the cliff the switch never crosses "
        "(latency undefined). Mechanism [V]; threshold shift [F]; absolute developmental timing/morphology [O]."
        % cliff)
    body = (
      "<h2>The cleanest test of the &gamma;-switch claim</h2>"
      "<p>The package's central claim is that each organ is an R19 bistable switch governed by its MEASURED "
      "master-gene &gamma;. The sharpest human falsification is a Mendelian haploinsufficiency: halve the "
      "master's effective dosage and the switch should fail to cross on schedule, reproducing the documented "
      "developmental defect. The severity is CITED (heterozygous loss = 0.5 dosage), never fitted.</p>"
      "<h2>A forced crossing cliff</h2>"
      "<p>In the kit, a successfully developing organ is driven at 1.5&times; its spinodal s* = "
      "2(&gamma;/3)<sup>3/2</sup>. Scaling the drive by dosage <i>x</i> gives x&middot;1.5&middot;s*; this "
      "stays above the spinodal only while x &gt; 1/1.5 = &#8532;. The critical dosage cliff is therefore "
      "&asymp; %.3f and &mdash; remarkably &mdash; <b>independent of &gamma;</b>: it is the same for every "
      "master. A 0.5 haploinsufficiency sits below it, so the heterozygous switch cannot release from the OFF "
      "basin: occupancy collapses from %.2f (WT) to %.2f and the crossing latency becomes undefined.</p>"
      "<h2>Three master genes, three dysplasias</h2>"
      "<table><thead><tr><th>id</th><th>disease</th><th>master (organ)</th><th>WT occ.</th>"
      "<th>het occ.</th><th>het crosses?</th></tr></thead><tbody>%s</tbody></table>"
      "<p>RUNX2 &rarr; cleidocranial dysplasia (open fontanelles, clavicular hypoplasia, supernumerary teeth "
      "as &lsquo;incomplete crossing&rsquo;); SOX9 &rarr; campomelic dysplasia (hypoplastic, bowed cartilage "
      "template); TBX5 &rarr; the limb component of Holt-Oram (radial-ray / appendicular reduction; the "
      "cardiac component is OUT of class and routed to the cardiovascular sibling). T7d (MYOD1) is reported as "
      "a SECONDARY, weaker case [V?] &mdash; human MYOD1 LoF disease is rare and recent &mdash; and is "
      "excluded from the hard gate, though it passes the same cliff.</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>The DIRECTION (failed/partial crossing) and the forced threshold shift are the result. The absolute "
      "developmental calendar and the precise morphology (how many millimetres of clavicle, which fontanelle, "
      "when) are NOT fixed by the substrate and stay [O]: occupancy is a switch-state proxy, not a "
      "morphogenetic geometry.</p>" % (cliff, wt_occ, het_occ, rows))
    cards = [CARD_CLIFF, CARD_SPINODAL,
             gamma_card("RUNX2", "bone", N["gammas"]["bone"]),
             gamma_card("SOX9", "cartilage", N["gammas"]["cartilage"]),
             gamma_card("TBX5", "limb_skeleton", N["gammas"]["limb_skeleton"])]
    oneliner = ("Haploinsufficiency (dosage 0.5) drops the master switch below a &gamma;-independent crossing "
        "cliff at &#8532; WT drive: CCD/RUNX2, campomelic/SOX9, Holt-Oram/TBX5 fail to cross [F]; timing [O].")
    return answer, abstract, body, cards, oneliner

def sec_t6_mechanostat(N):
    t6 = N["dis_suites"]["T6"]; t6b = N["dis_suites"]["T6b"]; lad = t6["detail"]["ladder"]
    sp = t6["value"]["spinodal"]
    mild = next(r for r in lad if r["state"].startswith("mild"))
    space = next(r for r in lad if r["state"].startswith("spaceflight"))
    full = next(r for r in lad if "complete" in r["state"])
    rows = "".join(
        "<tr><td>%s</td><td>%.3f</td><td>%.3f&times;</td><td>%.3f</td></tr>"
        % (esc(r["state"]), r["disuse_drive"], r["rel_loss_rate"], r["settled_density_from_dense"])
        for r in lad)
    answer = ("Osteoporosis is the exact MIRROR of Wolff remodelling (&sect;4). Where supra-threshold load "
        "flips bone to the dense basin, sustained sub-threshold (disuse) load lowers the dense-basin escape "
        "barrier, so density drains back toward the resorbed basin. The relative loss rate rises monotonically "
        "with disuse (1.00&times; maintained &rarr; %.2f&times; at spaceflight &rarr; %.2f&times; at complete "
        "unloading) &mdash; barrier-limited escape, FORCED by the same bistable substrate [F]."
        % (space["rel_loss_rate"], full["rel_loss_rate"]))
    abstract = ("Below the Frost mechanostat setpoint (MES_resorption ~75&nbsp;&micro;&epsilon;, cited [L]) the "
        "loss rate climbs from baseline through mild disuse (%.2f&times;), bedrest and spaceflight (%.2f&times;) "
        "to complete unloading (%.2f&times;), with settled density falling from 1.00 to %.3f. Past the spinodal "
        "drive the dense basin vanishes outright (catastrophic resorption). Mirror of T3 [F]; setpoint [L]; "
        "absolute BMD and %%/month [O]." % (mild["rel_loss_rate"], space["rel_loss_rate"],
        full["rel_loss_rate"], full["settled_density_from_dense"]))
    body = (
      "<h2>The other arm of the mechanostat</h2>"
      "<p>T3 proved that loading flips bone to the dense basin with hysteresis. Bone disease is the same "
      "double well read the other way: <b>disuse and post-menopausal osteoporosis</b> is sustained "
      "<i>sub</i>-threshold load. The unloading drive lowers the escape barrier OUT of the dense basin, so the "
      "Kramers escape rate &mdash; the resorption rate &mdash; rises as the load drops further below the Frost "
      "minimum effective strain. Nothing new is added: it is the T3 settle run below threshold.</p>"
      "<h2>Loss accelerates as load falls (cited setpoint)</h2>"
      "<table><thead><tr><th>state</th><th>disuse drive</th><th>rel. loss rate</th>"
      "<th>settled density</th></tr></thead><tbody>%s</tbody></table>"
      "<p>The rate is normalised to 1.00&times; in the maintenance &lsquo;lazy zone&rsquo;. It rises smoothly "
      "with deeper unloading, matching the clinical ordering bedrest &lt; spaceflight &lt; complete "
      "immobilisation. The cited weight-bearing BMD loss of ~1.0&ndash;1.5&nbsp;%%/month in spaceflight and "
      "bedrest sets the SCALE [L]; the substrate supplies the rising SHAPE, not the absolute percentage [O].</p>"
      "<h2>Osteopetrosis: the loop loses its lower branch</h2>"
      "<p>The opposite disease is <b>osteopetrosis</b> (CLCN7 / TCIRG1 osteoclast failure). Here the "
      "resorption pathway is disabled &mdash; the DOWN-branch of the T3 loop is removed. On unloading, normal "
      "bone returns to baseline density (%.2f) but osteopetrotic bone stays locked high (%.2f): the hysteresis "
      "loop can no longer descend. The MECHANISM (removed down-branch &rarr; density cannot fall) is shown "
      "[V]; the resulting brittleness is a material property and stays [O].</p>"
      "<h2>Honest boundary</h2>"
      "<p>Paget's disease (disorganised runaway cross-basin cycling) and renal osteodystrophy / osteomalacia "
      "(a mineralization-supply defect, not a switch-threshold defect) have no clean single-switch signature "
      "and are recorded as [O] in the out-of-class register (&sect;20).</p>"
      % (rows, t6b["value"]["unloaded_density_normal"], t6b["value"]["unloaded_density_osteopetrosis"]))
    cards = [CARD_SPINODAL, CARD_BARRIER, gamma_card("RUNX2", "bone", N["gammas"]["bone"])]
    oneliner = ("Disuse osteoporosis = sub-threshold load lowering the dense-basin barrier; loss rate rises "
        "1.00&rarr;%.2f&times; with unloading [F]; osteopetrosis removes the loop's down-branch [V]; BMD [O]."
        % full["rel_loss_rate"])
    return answer, abstract, body, cards, oneliner

def sec_t8_nmj(N):
    t8 = N["dis_suites"]["T8"]; t8b = N["dis_suites"]["T8b"]
    decN = t8["value"]["decrement_pct_normal"]; decM = t8["value"]["decrement_pct_mg"]
    thr = t8["value"]["clinical_threshold_pct"]; f8 = t8["value"]["test_freq_hz"]
    inc = t8b["value"]["increment_pct_high_freq"]; f8b = t8b["value"]["test_freq_hz"]
    sweep = t8["detail"]["severity_sweep"]; incfreq = t8b["detail"]["increment_vs_freq"]
    srow = "".join("<tr><td>%.2f</td><td>%.2f%%</td></tr>" % (r["theta_safety_factor"], r["decrement_pct"]) for r in sweep)
    irow = "".join("<tr><td>%g&nbsp;Hz</td><td>+%.1f%%</td></tr>" % (r["freq_hz"], r["increment_pct"]) for r in incfreq)
    answer = ("Myasthenia gravis is a perturbation of the force-frequency machinery (&sect;2). Post-synaptic "
        "ACh-receptor block raises the per-pulse activation threshold, so during low-frequency repetitive "
        "stimulation transmitter run-down makes successive pulses fall short: force DECREMENTS pulse-to-pulse. "
        "At %g&nbsp;Hz the model gives a %.1f%% decrement versus %.2f%% normal &mdash; above the %g%% clinical "
        "RNS threshold, and monotone in lesion severity [V]." % (f8, decM, decN, thr))
    abstract = ("The same depression+facilitation NMJ that drives T1 is pushed past its safety factor: at "
        "%g&nbsp;Hz the decrement rises from %.2f%% (normal) to %.1f%% (MG), crossing the cited &gt;10%% "
        "diagnostic line, and grows with the lesion (sweep below). Lambert-Eaton is the mirror: a presynaptic "
        "deficit with use-dependent facilitation gives a high-frequency INCREMENT (+%.1f%% at %g&nbsp;Hz), the "
        "opposite sign. Direction + threshold [V]; clinical sign cited [L]." % (f8, decN, decM, inc, f8b))
    body = (
      "<h2>Decrement = transmission below its safety factor</h2>"
      "<p>Neuromuscular transmission normally has a large safety factor: each motor nerve impulse releases far "
      "more ACh than needed to fire the fibre, so T1's force-frequency curve is flat pulse-to-pulse at low "
      "rates. <b>Myasthenia gravis</b> blocks post-synaptic ACh receptors, cutting that safety margin. Now "
      "the physiological run-down of release during a 2&ndash;5&nbsp;Hz train drops successive end-plate "
      "potentials below the firing threshold, and the muscle force decrements &mdash; the classic repetitive "
      "nerve-stimulation (RNS) sign. This is the SAME NMJ model used in T1 with the threshold raised; no new "
      "mechanism.</p>"
      "<h2>Above the cited diagnostic line, and dose-dependent</h2>"
      "<p>At %g&nbsp;Hz the modelled decrement is %.1f%% against %.2f%% in the unblocked junction, clearing "
      "the cited &gt;%g%% RNS threshold. Deepening the block (lower safety factor) monotonically deepens the "
      "decrement:</p>"
      "<table><thead><tr><th>safety factor</th><th>decrement</th></tr></thead><tbody>%s</tbody></table>"
      "<h2>Lambert-Eaton: the opposite sign</h2>"
      "<p><b>Lambert-Eaton myasthenic syndrome</b> is a PREsynaptic deficit: baseline release is low (a weak "
      "first response) but use-dependent facilitation builds up during high-frequency activity, so the "
      "response INCREMENTS. The model reproduces the reversal &mdash; an increment that grows with frequency:</p>"
      "<table><thead><tr><th>frequency</th><th>increment</th></tr></thead><tbody>%s</tbody></table>"
      "<p>MG decrements at low frequency; LEMS increments at high frequency. The kit reproduces both DIRECTIONS "
      "from one NMJ, which is the discriminant.</p>"
      "<h2>Seam and what is NOT claimed</h2>"
      "<p>The synaptic CAUSE (autoantibody against the ACh receptor or the presynaptic calcium channel) is "
      "owned by the neuro / immune volumes and only cited here; the in-class result is the muscle-side force "
      "change. The clinical threshold is cited [L]. One limit is recorded [O]: this depression-only NMJ does "
      "not model high-frequency post-activation potentiation, so the brief facilitation seen in MG at high "
      "rates is out of scope.</p>"
      % (f8, decM, decN, thr, srow, irow))
    cards = [gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"])]
    oneliner = ("MG raises the NMJ threshold &rarr; %.1f%% low-frequency force decrement (&gt;%g%% clinical) "
        "[V]; LEMS gives the opposite high-frequency increment (+%.1f%%) [V]; synaptic cause cited [L]."
        % (decM, thr, inc))
    return answer, abstract, body, cards, oneliner

def sec_t10_metabolic(N):
    t = N["dis_suites"]["T10"]; v = t["value"]
    tN = v["tau_fit_normal_s"]; tM = v["tau_fit_metabolic_s"]
    rN = v["recovered_frac_normal"]; rM = v["recovered_frac_metabolic"]
    answer = ("Metabolic and mitochondrial myopathy is a direct perturbation of the fatigue dynamics "
        "(&sect;6). Impaired ATP resynthesis makes the slow fatigue variable load FASTER and recover "
        "INCOMPLETELY: the fitted time constant shortens from %.0f&nbsp;s (normal) to %.0f&nbsp;s, and "
        "recovered force after rest falls from %.3f to %.3f &mdash; below the 0.95 reversibility floor that "
        "defines healthy fatigue. Both DIRECTIONS are verified [V]." % (tN, tM, rN, rM))
    abstract = ("T5's reversible exponential decline is re-run with a shortened &tau; and a non-recovering "
        "residual term. Force then declines faster (&tau; %.0f&rarr;%.0f&nbsp;s) and rest no longer restores "
        "it (recovered fraction %.3f vs %.3f normal, vs the &ge;0.95 healthy threshold) &mdash; the "
        "exercise-intolerance phenotype. Recovery is monotone in the residual deficit. Direction [V]; "
        "anchor [L]; absolute magnitude [O]." % (tN, tM, rM, rN))
    body = (
      "<h2>Fatigue that comes early and does not lift</h2>"
      "<p>T5 established muscle fatigue as a reversible exponential force decline to a plateau, fully "
      "recovered on rest, with a cited time constant. <b>Metabolic / mitochondrial myopathy</b> perturbs "
      "exactly that variable: defective oxidative ATP supply means the fatigue process charges faster and its "
      "recovery is incomplete. Two cited features of the phenotype map onto two changes to T5 &mdash; a "
      "shorter &tau; and a residual, non-recovering deficit &mdash; with no new dynamics.</p>"
      "<h2>Faster onset, incomplete recovery</h2>"
      "<p>The fitted fatigue time constant shortens from %.0f&nbsp;s to %.0f&nbsp;s, so force falls earlier "
      "into exertion. After the standard rest period the normal muscle recovers a fraction %.3f of its force "
      "(effectively full), while the metabolic muscle recovers only %.3f &mdash; below the 0.95 floor that "
      "characterises healthy, fully reversible fatigue. That persistent deficit is the modelled correlate of "
      "exercise intolerance and post-exertional weakness. Deepening the residual deficit monotonically lowers "
      "the recovered fraction.</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>The DIRECTIONS &mdash; faster decline and sub-threshold recovery &mdash; are the result, and the "
      "fatigue time-constant band is cited [L]. The absolute magnitude of the force loss and the precise "
      "recovery percentage for any specific enzyme defect are not fixed by the substrate and stay [O].</p>"
      % (tN, tM, rN, rM))
    cards = [gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"])]
    oneliner = ("Metabolic myopathy shortens the T5 fatigue &tau; (%.0f&rarr;%.0f&nbsp;s) and leaves recovery "
        "incomplete (%.3f&lt;0.95) [V]; magnitude [O]." % (tN, tM, rM))
    return answer, abstract, body, cards, oneliner

def sec_t9_oa(N):
    t = N["dis_suites"]["T9"]; lad = t["detail"]["ladder"]
    rows = "".join(
        "<tr><td>%s</td><td>%.1f&times;</td><td>%.3f</td><td>%.3f</td></tr>"
        % (esc(r["loading"]), r["sigma_over_sigma_star"], r["contact_number_final"], r["matrix_loss"])
        for r in lad)
    sub = next(r for r in lad if r["sigma_over_sigma_star"] < 1.0)
    over = next(r for r in lad if "overload + high BMI" in r["loading"])
    sev = next(r for r in lad if r["loading"].startswith("severe"))
    answer = ("Osteoarthritis is cartilage unjamming. Cartilage load capacity is the T2 contact number; "
        "cyclic SUPRA-threshold load fatigues that contact network, so the matrix progressively loses "
        "load-bearing contacts &mdash; the joint-space-narrowing analogue. Sub-threshold exercise is "
        "protected (%.0f%% matrix retained), but at overload with high BMI the matrix loss climbs to %.1f%% "
        "and accelerates convexly with load. Shape verified [V] on a CITED fatigue-damage law." %
        (sub["contact_number_final"] * 100, over["matrix_loss"] * 100))
    abstract = ("A cited Paris/Basquin cyclic fatigue-damage law (exponent m=2, FORM cited [L]) is applied to "
        "the cartilage contact number under load &sigma;/&sigma;*. Below threshold (0.8&times;) the matrix is "
        "protected (loss %.3f); at normal load loss is modest (%.3f), rising convexly to %.3f at overload+BMI "
        "and %.3f at severe overload. Loss accelerates with load magnitude and BMI, the OA epidemiology. "
        "Shape [V]; damage-law form [L]; absolute progression rate [O]." %
        (sub["matrix_loss"], lad[1]["matrix_loss"], over["matrix_loss"], sev["matrix_loss"]))
    body = (
      "<h2>A joint as a load-bearing contact network</h2>"
      "<p>Cartilage is modelled as load-bearing jammed matter, and its integrity is the same order parameter "
      "as muscle force in T2: the number of load-bearing contacts. <b>Osteoarthritis</b> is the fatigue of "
      "that network. Unlike bone (which can remodel back across the T3 yield threshold), cyclic "
      "supra-threshold loading accumulates irreversible damage in the contact number &mdash; progressive loss "
      "of load-bearing matrix, the mechanical analogue of joint-space narrowing.</p>"
      "<h2>A cited damage law, not a fitted one</h2>"
      "<p>This is the one disease in the battery that needs a small ADDED mechanism, so it is held to the "
      "cited-anchor discipline: damage accumulates by a Paris/Basquin-type cyclic-fatigue law with a CITED "
      "exponent (m=2), not a curve tuned to land. Applied to the contact number under normalised contact "
      "stress &sigma;/&sigma;*:</p>"
      "<table><thead><tr><th>loading</th><th>&sigma;/&sigma;*</th><th>final contact number</th>"
      "<th>matrix loss</th></tr></thead><tbody>%s</tbody></table>"
      "<p>Three signatures emerge and match OA epidemiology: (1) a threshold &mdash; sub-threshold moderate "
      "exercise is PROTECTED (no loss), consistent with exercise not causing OA; (2) monotonic acceleration "
      "&mdash; loss rises with load magnitude; (3) convexity in load and BMI &mdash; the documented dose "
      "effect of joint overload and obesity. The mechanism is cartilage UNJAMMING under cyclic fatigue.</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>The SHAPE (threshold, monotonic, convex, BMI-sensitive) is the result and the damage-law FORM is "
      "cited [L]. The absolute progression rate &mdash; the rate constant A that sets years-to-narrowing "
      "&mdash; is NOT fixed by the substrate and stays [O]; only relative, normalised loss is claimed.</p>"
      % rows)
    cards = [gamma_card("SOX9", "cartilage", N["gammas"]["cartilage"]), CARD_SPINODAL]
    oneliner = ("OA = cyclic-fatigue unjamming of the cartilage contact number (cited Paris/Basquin m=2): "
        "sub-threshold protected, loss convex in load+BMI [V]; absolute rate [O].")
    return answer, abstract, body, cards, oneliner

def sec_t4ext_achondroplasia(N):
    t = N["dis_suites"]["T4-ext"]; lad = t["detail"]["growth_output_ladder"]
    rows = "".join(
        "<tr><td>%s</td><td>%.3f</td><td>%.3f</td></tr>"
        % (esc(r["genotype"]), r["suppressive_drive"], r["growth_plate_output"])
        for r in lad)
    wt = next(r for r in lad if r["genotype"] == "wild-type")
    ach = next(r for r in lad if r["genotype"].startswith("achondroplasia"))
    answer = ("Achondroplasia maps FGFR3 gain-of-function to a SUPPRESSIVE drive on the SOX9 chondrocyte "
        "switch at the growth plate (&sect;5). FGFR3 normally brakes chondrocyte proliferation; the activating "
        "G380R mutation turns that brake up, shifting the growth-plate switch toward OFF and shortening "
        "long-bone output. The model gives a graded ladder &mdash; full output %.2f in WT collapsing to %.2f "
        "in achondroplasia &mdash; with a clear cliff [V]." % (wt["growth_plate_output"], ach["growth_plate_output"]))
    abstract = ("Adding a negative regulator to T4: a suppressive drive (FGFR3-GOF) on the chondrocyte switch "
        "lowers growth-plate output. The ladder runs WT %.2f &rarr; hypochondroplasia (mild) &rarr; "
        "achondroplasia %.2f &rarr; thanatophoric (severe), a graded shortening with a threshold &mdash; FGFR3 "
        "dose maps to severity. Mechanism (suppressive drive shifts the chondrocyte threshold) [V]; absolute "
        "long-bone length [O]." % (wt["growth_plate_output"], ach["growth_plate_output"]))
    body = (
      "<h2>A growth-plate brake turned up</h2>"
      "<p>T4 ranked developmental thresholds by master-gene &gamma;. <b>Achondroplasia</b> and the related "
      "chondrodysplasias perturb that growth plate with a NEGATIVE regulator. FGFR3 is a physiological brake "
      "on chondrocyte proliferation; the activating G380R substitution (and its stronger alleles) increases "
      "that braking as a sustained SUPPRESSIVE drive on the SOX9 chondrocyte switch, pushing it toward the OFF "
      "basin and cutting endochondral long-bone output. It is the inverse perturbation to a master-gene "
      "loss.</p>"
      "<h2>FGFR3 dose maps to severity</h2>"
      "<table><thead><tr><th>genotype</th><th>suppressive drive</th><th>growth-plate output</th></tr></thead>"
      "<tbody>%s</tbody></table>"
      "<p>The output ladder is graded and shows a threshold: a mild suppressive drive (hypochondroplasia) "
      "barely dents output, the achondroplasia allele drops it sharply to %.2f, and the severe "
      "(thanatophoric) drive collapses it further. Stronger FGFR3 activation &rarr; shorter bone, matching the "
      "clinical allelic series. The DIRECTION and the graded cliff are the result.</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>The growth-plate output is a switch-state proxy, so the relative ladder is claimed but the ABSOLUTE "
      "long-bone length in centimetres is NOT fixed by the substrate and stays [O].</p>"
      % (rows, ach["growth_plate_output"]))
    cards = [gamma_card("SOX9", "cartilage", N["gammas"]["cartilage"]), CARD_SPINODAL]
    oneliner = ("Achondroplasia = FGFR3-GOF suppressive drive on the SOX9 growth-plate switch; graded "
        "shortening WT %.2f&rarr;%.2f with a cliff [V]; absolute length [O]." %
        (wt["growth_plate_output"], ach["growth_plate_output"]))
    return answer, abstract, body, cards, oneliner

def sec_out_of_class(N):
    answer = ("Some musculoskeletal-presenting diseases are deliberately NOT emerged here. Material diseases "
        "(osteogenesis imperfecta, Ehlers-Danlos / Marfan) and signatureless ones (Paget, scoliosis) are "
        "carried as honest [O] with stated obstacles; degenerative disc disease is left to an existing kernel "
        "to avoid a duplicate page. Diseases whose CAUSE is out-of-class are ROUTED to siblings via a named "
        "seam &mdash; single-source-of-truth.")
    abstract = ("This register keeps honesty explicit. The substrate already grades absolute bone density and "
        "material strength [O]; connective-tissue diseases inherit that obstacle rather than forcing a claim. "
        "Out-of-class diseases are listed so they are not silently dropped, each with the sibling owner and the "
        "single seam variable cited &mdash; SSOT, no duplicate emergence.")
    body = (
      "<h2>Material and signatureless diseases &mdash; honest [O], not forced</h2>"
      "<p>The kit fixes the SHAPE of bone and cartilage mechanics but not their absolute material constants; "
      "that boundary is graded [O] throughout. The following connective-tissue diseases live in that open "
      "region and are recorded with their obstacle, not overclaimed:</p>"
      "<ul>"
      "<li><b>Osteogenesis imperfecta</b> (COL1A1/2) &mdash; a qualitatively lower matrix yield threshold is "
      "plausible [V?], but the quantitative brittleness is a material property the substrate does not fix [O].</li>"
      "<li><b>Ehlers-Danlos / Marfan</b> (collagen, fibrillin) &mdash; connective-tissue laxity; a material "
      "compliance change, [O].</li>"
      "<li><b>Tendinopathy</b> &mdash; NOW IMPLEMENTED in &sect;17: the OA cyclic-fatigue kernel applied to a "
      "tendon collagen contact number gives a verified shape [V]; only the absolute progression rate "
      "remains [O]. (Moved out of this open-material list this cycle.)</li>"
      "<li><b>Paget's disease</b> &mdash; disorganised runaway cross-basin remodelling; no clean single-switch "
      "signature [O]. <b>Renal osteodystrophy / osteomalacia</b> &mdash; a mineralization-supply defect, "
      "outside the switch-threshold scope [O].</li>"
      "<li><b>Scoliosis, developmental dysplasia of the hip, clubfoot</b> &mdash; three-dimensional "
      "structural / developmental deformities with no clean single-switch signature to perturb; the substrate "
      "fixes load-bearing mechanics, not three-dimensional skeletal geometry. Carried as honest [O], the same "
      "category as Paget's. (Out of current scope; the posture / mechanical-load seam is where any future "
      "treatment would attach.)</li>"
      "</ul>"
      "<h2>Covered by an existing kernel &mdash; deliberately not duplicated</h2>"
      "<p>One residual disease is <b>not</b> open for lack of a mechanism &mdash; it is deliberately left "
      "un-emerged to avoid a duplicate. <b>Degenerative (intervertebral) disc disease</b> is a cyclic-fatigue "
      "unjamming of a load-bearing collagen matrix, mechanically identical to osteoarthritis (&sect;12) and "
      "tendinopathy (&sect;17). The same CITED Paris/Basquin damage law (m=2) applied to an intervertebral-disc "
      "contact number would reproduce the same signature &mdash; sub-threshold protected, loss convex in cyclic "
      "load &mdash; a verified SHAPE [V] with only the absolute rate left [O]. It is a one-function reuse of the "
      "existing kernel. We deliberately do NOT give it a third identical-kernel page: that would duplicate a "
      "source of truth (SSOT) without adding physics. The distinction is honest book-keeping &mdash; a parsimony "
      "choice, not a capability gap &mdash; and it couples through the same posture / mechanical-load seam.</p>"
      "<h2>Out-of-class diseases &mdash; routed via seams (SSOT)</h2>"
      "<p>These are real musculoskeletal presentations whose CAUSE belongs to another physical class. They are "
      "emerged in the sibling package and only the seam variable is cited here; re-deriving them would "
      "duplicate a source of truth.</p>"
      "<table><thead><tr><th>disease</th><th>true owner</th><th>seam cited</th></tr></thead><tbody>"
      "<tr><td>Rheumatoid arthritis, ankylosing spondylitis, psoriatic arthritis (autoimmune)</td>"
      "<td>immune / inflammatory volume</td><td>immune-attack-on-joint</td></tr>"
      "<tr><td>Gout / pseudogout (crystal / metabolic)</td><td>metabolic sibling</td>"
      "<td>crystal-deposition</td></tr>"
      "<tr><td>Fibromyalgia, chronic musculoskeletal pain</td><td>neuro / mind volume</td>"
      "<td>nociception</td></tr>"
      "<tr><td>Bone metastases from breast / prostate / lung</td><td>primary-tumour sibling + bone</td>"
      "<td>metastasis-to-bone (bone microenvironment is in-class; the primary is not)</td></tr>"
      "<tr><td>Septic arthritis / osteomyelitis (infection)</td><td>infectious sibling</td>"
      "<td>pathogen-load</td></tr>"
      "</tbody></table>"
      "<p>The bone-metastasis row is the instructive one: the bone microenvironment (osteoclast/osteoblast "
      "coupling) IS in-class and couples to the T3/T6 remodelling axis, but the primary tumour is owned by its "
      "own sibling. The seam carries only what crosses the boundary.</p>")
    cards = [CARD_SPINODAL, CARD_BARRIER]
    oneliner = ("Material diseases (OI, EDS/Marfan) and signatureless ones (Paget, scoliosis) carried as honest [O] "
        "(tendinopathy now §17); degenerative disc disease deferred to the existing OA/tendinopathy kernel to "
        "avoid duplication; autoimmune, crystal, pain, infection and distant-primary tumours routed to siblings "
        "via named seams (SSOT).")
    return answer, abstract, body, cards, oneliner

# --------------------------------------------------------------------------- treatment axis (mirror of disease)
# Mechanism-page slugs each treatment links back to (cross-reference, SSOT: the mechanism is derived once).
_TX_MECH_SLUG = {
    "Tx-T16": "18-osteomalacia-rickets-mineralization-ceiling",
    "Tx-T6":  "09-mechanostat-disease-osteoporosis-osteopetrosis",
    "Tx-T6b": "09-mechanostat-disease-osteoporosis-osteopetrosis",
    "Tx-T17": "19-osteolytic-bone-disease-uncoupling",
    "Tx-T13": "16-stress-fracture-and-fracture-healing",
    "Tx-T4-ext": "13-achondroplasia-growth-plate-suppression",
    "Tx-T9":  "12-osteoarthritis-cartilage-unjamming",
    "Tx-T8":  "10-neuromuscular-transmission-mg-lems",
    "Tx-T8b": "10-neuromuscular-transmission-mg-lems",
    "Tx-T12": "15-muscle-channelopathies-myotonia-paralysis",
    "Tx-T11": "14-muscular-dystrophy-and-sarcopenia",
    "Tx-T15": "14-muscular-dystrophy-and-sarcopenia",
    "Tx-T14": "17-tendinopathy-collagen-network-unjamming",
    "Tx-T10": "11-metabolic-mitochondrial-myopathy",
    "Tx-T7":  "08-master-gene-dosage-dysplasias",
    "Tx-ONCO": "07-carcinogen-dose-response-bone-soft",
}

def _tx_txt(s):
    """Escape a battery-sourced plain-ASCII string and render a couple of tokens nicely."""
    out = esc(s or "")
    return out.replace("-&gt;", " &rarr; ").replace("/", " / ")

def _tx_detail(N, target):
    """Render one treatment as an answer-first block: H3 + direct sentence + kernel action + MOA + grade,
    with a link back to the once-derived mechanism page (SSOT)."""
    s = N["trx_suites"].get(target, {})
    mech = _TX_MECH_SLUG.get(target)
    mech_link = (' <a href="%s">mechanism &sect;%s</a>' % (page_url(mech), mech.split("-")[0].lstrip("0"))) if mech else ""
    return (
      "<h3>%s</h3>"
      "<p><b>Treatment:</b> %s.%s</p>"
      "<p><b>Kernel action (mirror):</b> %s. <b>How the real intervention acts:</b> %s</p>"
      "<p><b>Grade:</b> %s</p>" % (
        _tx_txt(s.get("disease")),
        _tx_txt(s.get("treatment")), mech_link,
        _tx_txt(s.get("kernel_action")), _tx_txt(s.get("moa")),
        _tx_txt(s.get("grade"))))

def _tx_table(N, targets):
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            _tx_txt(N["trx_suites"][t].get("disease")), _tx_txt(N["trx_suites"][t].get("treatment")),
            _tx_txt(N["trx_suites"][t].get("kernel_action")), N["trx_suites"][t].get("status"))
        for t in targets if t in N["trx_suites"])
    return ("<table><thead><tr><th>disease</th><th>treatment (cited anchor)</th>"
            "<th>kernel action (mirror)</th><th>restored?</th></tr></thead><tbody>" + rows + "</tbody></table>")

# ===== §21  methodology + DNA grounding =====================================================
def sec_treatment_axis(N):
    g_bone = N["gammas"]["bone"]
    trx = N["trx"]; n_rev = len([s for s in trx["suites"] if not s.get("honest_open_or_partial")])
    answer = ("Every bone, cartilage and muscle switch here is emerged from a MEASURED gene parameter "
        "(&gamma;) read from the human genome; the treatment of each disease is the MIRROR of its mechanism on "
        "that same DNA-grounded switch &mdash; restore the barrier, drive, branch or supply. %d reversible "
        "treatments restore the healthy attractor; developmental cliffs and cartilage regeneration remain open." % n_rev)
    abstract = ("This is not a toy simulation. Each organ switch is emerged from a measured promoter parameter "
        "&gamma; (for bone&rsquo;s RUNX2, &gamma; = %.4f, read from the human reference genome), so disease and "
        "treatment are perturbations and restorations of a switch grounded in real DNA, deterministic and "
        "reproducible bit-for-bit (engine hash unchanged). The treatment axis is the disease axis run in reverse "
        "on one kernel: %d reversible mirror treatments restore the healthy attractor by direction (No-Tuning), "
        "each citing the real drug or load; developmental dosage cliffs, cartilage regeneration and "
        "established-tumour chemotherapy are graded open with a stated obstacle." % (g_bone, n_rev))
    body = (
      "<h2>Grounded in emerged DNA, not a toy model</h2>"
      "<p>The switches treated here are not free parameters. Each organ is emerged from a single MEASURED gene "
      "parameter &mdash; &gamma;, the negative mean nearest-neighbour stacking free energy (&minus;&Delta;G37, "
      "SantaLucia 1998) of the master gene&rsquo;s promoter, read directly from the human reference genome.</p>"
      "<p>For bone, RUNX2 gives &gamma; = %.4f, measured offline from assembly NC_000006.12 (MANE "
      "NM_001024630.4, promoter window TSS&minus;2000..+500) by the identical DNA pipeline used across the VP "
      "body-physiology program. This value is read, not fitted: it reproduces bit-for-bit on any machine.</p>"
      "<p>So the entire disease and treatment battery sits on a DNA-grounded substrate. A disease perturbs a "
      "switch that the genome built; a treatment restores it. The mechanism for each disease is derived once on "
      "its own page (&sect;7&ndash;&sect;19) and only referenced here &mdash; single source of truth.</p>"
      "<h2>One kernel, run in reverse</h2>"
      "<p>A treatment is the mirror of a disease on the same switch. Each disease in this volume lowers an R19 "
      "escape barrier, shifts a setpoint past a spinodal, disables one branch of a remodelling hysteresis loop, "
      "or caps a supply.</p>"
      "<p>Its treatment performs the inverse operation: raise the barrier, restore the drive across the spinodal, "
      "re-enable the disabled branch, or refill the capped supply. The treatment code imports the disease "
      "function verbatim and moves its single cited knob back toward health.</p>"
      "<p>This makes the treatment axis forced, not decorative. It adds no new physics and no new constant; it is "
      "the disease kernel evaluated with the sign reversed.</p>"
      "<h2>How each treatment is verified (No-Tuning)</h2>"
      "<p>Each treatment is a monotone restoration sweep: an intensity from 0 (untreated) to 1 (full restoration "
      "of that knob). It passes when the disease signature moves monotonically back toward the healthy attractor "
      "and ends closer to health than the untreated state.</p>"
      "<p>The sweep is never tuned to a clinical efficacy figure. The DIRECTION &mdash; does restoring the knob "
      "undo the sign of the lesion? &mdash; is the result, and the real drug or load is the cited anchor for "
      "WHICH knob it targets. Vosoritide lifts an FGFR3 suppressive drive; pyridostigmine restores the "
      "neuromuscular safety factor; denosumab removes a giant-cell-tumour resorptive drive; vitamin D refills the "
      "mineral ceiling.</p>"
      "<h2>Determinism and gate</h2>"
      "<p>The treatment battery is a separate module that reuses the disease kernels and never touches the "
      "engine, so the engine determinism hash is byte-identical to the disease-only build (2&times;sha256 "
      "identical).</p>"
      "<p>Treatments are gated exactly as diseases are: the reversible mirror treatments must all restore (a hard "
      "gate), and honest open / partial entries are logged, never silently dropped. Disease and treatment are two "
      "readings of one DNA-grounded switch.</p>"
      "<h2>Map of the treatment cluster</h2>"
      "<p>The per-disease treatment detail is split across three pages so each answer stays self-contained:</p>"
      "<ul>"
      "<li><a href=\"%s\">&sect;22 &mdash; Bone and cartilage treatments</a>: osteoporosis, osteopetrosis, "
      "osteomalacia, osteolytic bone disease, stress fracture, achondroplasia, osteoarthritis.</li>"
      "<li><a href=\"%s\">&sect;23 &mdash; Muscle and neuromuscular treatments</a>: myasthenia gravis, "
      "Lambert-Eaton syndrome, channelopathies, muscular dystrophy, sarcopenia, tendinopathy.</li>"
      "<li><a href=\"%s\">&sect;24 &mdash; Honest treatment limits and scope</a>: developmental dosage cliffs, "
      "cartilage regeneration, established-tumour therapy versus prevention, metabolic myopathy.</li>"
      "</ul>") % (g_bone,
                  page_url("22-treatment-bone-and-cartilage"),
                  page_url("23-treatment-muscle-and-neuromuscular"),
                  page_url("24-treatment-honest-limits-and-scope"))
    cards = [CARD_SPINODAL, CARD_BARRIER]
    oneliner = ("Treatment = disease run in reverse on a DNA-grounded switch (each organ emerged from a measured "
        "gene parameter gamma read from the human genome): restore the barrier / drive / branch / supply. %d "
        "reversible mirror treatments restore the healthy attractor by direction (No-Tuning), each citing the real "
        "drug or load; developmental cliffs, cartilage regeneration and established-tumour chemotherapy are honest "
        "[O]. Engine hash unchanged." % n_rev)
    keywords = ["disease treatment mechanism model", "barrier restoration", "R19 bistable switch",
                "DNA-grounded simulation", "measured gene gamma", "promoter nearest-neighbor stacking energy",
                "RUNX2", "jamming physics", "musculoskeletal disease treatment", "No-Tuning reproducible model"]
    return answer, abstract, body, cards, oneliner, keywords

# ===== §22  bone & cartilage treatments ====================================================
def sec_treatment_bone(N):
    targets = ["Tx-T6", "Tx-T6b", "Tx-T16", "Tx-T17", "Tx-T13", "Tx-T4-ext", "Tx-T9"]
    answer = ("Bone and cartilage treatments are mirror operations on the DNA-emerged RUNX2 and SOX9 switches: "
        "mechanical loading and antiresorptives reverse osteoporosis, vitamin D refills osteomalacia, HSCT "
        "re-enables resorption in osteopetrosis, denosumab removes the osteolytic resorptive drive, rest plus "
        "loading heals stress fracture, vosoritide partially relieves achondroplasia, and unloading arrests "
        "osteoarthritis.")
    abstract = ("Each bone or cartilage treatment restores the exact knob its disease perturbs on the RUNX2 / "
        "SOX9 switch. Osteoporosis is re-crossed to the dense basin by load and its escape barrier raised by "
        "antiresorptives; osteomalacia is a refilled mineral ceiling; osteopetrosis is a re-enabled resorption "
        "branch; osteolytic bone disease is a relieved formation cap plus a removed RANKL drive. Achondroplasia "
        "relief is held below the spinodal cliff (improved, not normalised) and osteoarthritis is arrest-only "
        "because cartilage does not regenerate [O].")
    body = (
      "<h2>Bone and cartilage: restoring the RUNX2 / SOX9 switch</h2>"
      "<p>Every disease in this group perturbs the bone (RUNX2) or cartilage (SOX9) switch that the genome "
      "emerged; each treatment restores that switch&rsquo;s knob. The table is the summary; the blocks below give "
      "the mirror action and the real intervention for each.</p>"
      + _tx_table(N, targets) +
      "<h2>Treatment by disease</h2>"
      + _tx_detail(N, "Tx-T6")
      + _tx_detail(N, "Tx-T6b")
      + _tx_detail(N, "Tx-T16")
      + _tx_detail(N, "Tx-T17")
      + _tx_detail(N, "Tx-T13")
      + _tx_detail(N, "Tx-T4-ext")
      + _tx_detail(N, "Tx-T9") +
      "<h2>Two honest limits in this group</h2>"
      "<p>Achondroplasia relief is deliberately partial. Vosoritide lifts the FGFR3 suppressive drive but is held "
      "below the spinodal cliff, so growth-plate output rises without flipping the chondrocyte switch fully on "
      "&mdash; improved stature, not normalised, matching the clinical result.</p>"
      "<p>Osteoarthritis is arrest-only. Unloading below the fatigue threshold stops further cartilage-contact "
      "loss, but the kernel has no matrix-resynthesis term and cartilage does not regenerate, so already-lost "
      "contacts are not restored; this open item is carried in the ledger.</p>")
    cards = [CARD_SPINODAL, CARD_BARRIER]
    oneliner = ("Bone / cartilage mirror treatments on the RUNX2 / SOX9 switch: loading + antiresorptive reverse "
        "osteoporosis, vitamin D refills osteomalacia, HSCT re-enables resorption (osteopetrosis), denosumab "
        "removes the osteolytic / giant-cell-tumour RANKL drive, rest + load heals stress fracture, vosoritide "
        "partially relieves achondroplasia, unloading arrests osteoarthritis (no cartilage regen [O]).")
    keywords = ["osteoporosis treatment mechanism", "vitamin D osteomalacia rickets", "denosumab giant cell tumour",
                "osteopetrosis stem cell transplant", "vosoritide achondroplasia mechanism",
                "stress fracture healing", "osteoarthritis load reduction", "bisphosphonate antiresorptive model",
                "RUNX2 SOX9 bone cartilage switch", "barrier restoration bone remodelling"]
    return answer, abstract, body, cards, oneliner, keywords

# ===== §23  muscle & neuromuscular treatments ==============================================
def sec_treatment_muscle(N):
    targets = ["Tx-T8", "Tx-T8b", "Tx-T12", "Tx-T11", "Tx-T15", "Tx-T14"]
    answer = ("Muscle and neuromuscular treatments restore the excitability and contractile knobs the disease "
        "perturbs: pyridostigmine restores the myasthenic safety factor, amifampridine raises Lambert-Eaton "
        "quantal content, mexiletine normalises channelopathy excitability, steroids and gene therapy slow "
        "muscular dystrophy, resistance training partially reverses sarcopenia, and eccentric loading rebuilds "
        "tendinopathy.")
    abstract = ("Each muscle or neuromuscular treatment moves the cited knob back toward normal. Myasthenia "
        "gravis restores the post-synaptic safety factor so the RNS decrement falls below the 10% diagnostic "
        "threshold; Lambert-Eaton raises presynaptic quantal content; channelopathies return the depolarization-"
        "block threshold from both excitability signs. Muscular-dystrophy therapy is disease-modifying (lower "
        "damage rate, raise dystrophin, shifting Duchenne toward Becker) and sarcopenia training is partial "
        "&mdash; it stays below young values because the ageing floor remains [O].")
    body = (
      "<h2>Muscle and neuromuscular: restoring excitability and contractile knobs</h2>"
      "<p>This group perturbs the shared FitzHugh-Nagumo membrane and the muscle contractile contact number; each "
      "treatment restores the specific knob its disease moved. The table summarises; the blocks give the mirror "
      "action and the real drug or load.</p>"
      + _tx_table(N, targets) +
      "<h2>Treatment by disease</h2>"
      + _tx_detail(N, "Tx-T8")
      + _tx_detail(N, "Tx-T8b")
      + _tx_detail(N, "Tx-T12")
      + _tx_detail(N, "Tx-T11")
      + _tx_detail(N, "Tx-T15")
      + _tx_detail(N, "Tx-T14") +
      "<h2>Disease-modifying, not curative &mdash; stated plainly</h2>"
      "<p>Muscular-dystrophy therapy is disease-modifying. Corticosteroids lower the per-contraction damage scale "
      "and partial dystrophin restoration reconnects the contractile lattice, shifting a Duchenne trajectory "
      "toward Becker; neither is a cure, and the absolute timeline stays open.</p>"
      "<p>Sarcopenia training is partial. Resistance training reclaims part of the lost recruitment and "
      "fibre-size axes but stays below young values: the ageing floor remains. Tendinopathy deloading arrests "
      "further loss, and eccentric loading is the mechanotransductive rebuild, but the absolute regenerated "
      "collagen fraction is open.</p>")
    cards = [CARD_SPINODAL, CARD_BARRIER]
    oneliner = ("Muscle / neuromuscular mirror treatments: pyridostigmine restores the myasthenic safety factor "
        "(decrement below 10%), amifampridine raises Lambert-Eaton quantal content, mexiletine normalises "
        "channelopathy excitability, steroids + gene therapy modify muscular dystrophy (Duchenne toward Becker), "
        "resistance training partially reverses sarcopenia (ageing floor [O]), eccentric loading rebuilds "
        "tendinopathy.")
    keywords = ["myasthenia gravis pyridostigmine mechanism", "Lambert-Eaton amifampridine 3,4-DAP",
                "muscle channelopathy mexiletine", "muscular dystrophy exon skipping gene therapy",
                "sarcopenia resistance training", "tendinopathy eccentric loading",
                "neuromuscular junction safety factor", "FitzHugh-Nagumo excitability model",
                "Duchenne Becker dystrophin", "muscle disease treatment mechanism"]
    return answer, abstract, body, cards, oneliner, keywords

# ===== §24  honest treatment limits & scope ================================================
def sec_treatment_negatives(N):
    answer = ("Three disease classes have no kernel restoration, and saying so is the result: developmental "
        "dosage dysplasias (the master-switch window has closed), osteoarthritis cartilage regeneration (no "
        "resynthesis term), and established-tumour cytotoxic therapy (the kernel models initiation, not "
        "cell-killing). Primary cancer prevention &mdash; remove the carcinogen &mdash; is verified [V]; general "
        "metabolic myopathy is open [O].")
    abstract = ("The framework is most useful where it declines to over-claim. Developmental dosage cliffs are not "
        "postnatally reversible because the master-switch crossing is a closed-window decision and the formed "
        "skeleton is fixed; cartilage does not regenerate; and chemotherapy kills transformed cells, which is not "
        "a barrier-restoration of the original switch. Primary prevention (dose down &rarr; risk down) is in scope "
        "and verified; only a cofactor-responsive subset of metabolic myopathy reverses. Every open item names "
        "its obstacle in the ledger.")
    body = (
      "<h2>Honest negatives are results, not failures</h2>"
      "<p>Three classes of disease have no restoration knob in this kernel. Recording that plainly, with the "
      "obstacle named, is the honest scientific outcome and matches the constitution&rsquo;s open-grade "
      "discipline.</p>"
      "<h3>Developmental dosage dysplasias (CCD / RUNX2, campomelic / SOX9, Holt-Oram / TBX5)</h3>"
      "<p>There is no restoration knob. The master-switch crossing is a one-shot decision inside a closed "
      "developmental window, the spinodal-cliff commitment is already settled, and the formed skeleton is fixed. "
      "No postnatal intervention re-runs development; management is surgical and symptomatic, not dosage-"
      "restoring. (<a href=\"" + page_url("08-master-gene-dosage-dysplasias") + "\">mechanism &sect;8</a>.)</p>"
      "<h3>Osteoarthritis cartilage regeneration</h3>"
      "<p>Unloading below the fatigue threshold arrests further cartilage-contact loss, which is verified, but "
      "the kernel has no matrix-resynthesis term and cartilage does not clinically regenerate, so already-lost "
      "contacts are not restored. Joint replacement substitutes hardware, outside the kernel. "
      "(<a href=\"" + page_url("12-osteoarthritis-cartilage-unjamming") + "\">mechanism &sect;12</a>.)</p>"
      "<h3>Established-tumour therapy versus primary prevention</h3>"
      "<p>The carcinogenesis kernel models initiation: a carcinogen dose lowers the R19 barrier, raising the "
      "Kramers crossing rate and the relative risk. Chemotherapy, resection and radiation kill already-"
      "transformed cells, which is not a barrier-restoration of the original switch, so therapy-response is out "
      "of scope [O].</p>"
      "<p>Primary prevention is in scope and verified. Removing the carcinogen lowers the dose, raising the "
      "barrier back and lowering the initiation rate &mdash; the framework-native treatment claim for cancer is "
      "prevention, graded [V]. (<a href=\"" + page_url("07-carcinogen-dose-response-bone-soft") + "\">mechanism "
      "&sect;7</a>.)</p>"
      "<h3>Metabolic / mitochondrial myopathy</h3>"
      "<p>Only a cofactor-responsive subset reverses. Supplementing riboflavin, CoQ10 or carnitine lengthens the "
      "fatigue time-constant and clears the non-recovering residual in that subset; the general primary-"
      "mitochondrial case has no kernel knob and is supportive only. "
      "(<a href=\"" + page_url("11-metabolic-mitochondrial-myopathy") + "\">mechanism &sect;11</a>.)</p>"
      "<h2>Why stating limits strengthens the model</h2>"
      "<p>A model that reversed every disease would be tuned, not grounded. Because each treatment is the literal "
      "mirror of a DNA-grounded mechanism, the cases it cannot reverse are exactly the cases where biology has no "
      "single knob &mdash; a closed developmental window, an absent regeneration pathway, a post-transformation "
      "cell population.</p>"
      "<p>Each open item above is listed in the irreproducibility ledger with its obstacle, as the constitution "
      "requires. The boundary is the evidence that the reversible results are mechanism, not curve-fitting.</p>")
    cards = [CARD_SPINODAL, CARD_BARRIER]
    oneliner = ("Honest treatment limits (results, not failures): developmental dosage cliffs are not postnatally "
        "reversible (closed window), osteoarthritis cartilage does not regenerate (arrest-only), established-tumour "
        "chemotherapy is out of the initiation kernel&rsquo;s scope while primary prevention is verified [V], and "
        "only a cofactor-responsive subset of metabolic myopathy reverses; every open item names its obstacle.")
    keywords = ["cancer prevention versus treatment", "carcinogen dose response relative risk",
                "achondroplasia developmental window", "cartilage does not regenerate",
                "metabolic myopathy cofactor riboflavin CoQ10", "honest open grade obstacle",
                "Kramers barrier carcinogenesis", "cleidocranial dysplasia Holt-Oram",
                "treatment model limits", "no-tuning falsifiable"]
    return answer, abstract, body, cards, oneliner, keywords
# --------------------------------------------------------------------------- wave-2 disease sections
def sec_t11_t15_muscle_loss(N):
    d = N["dis_suites"]["T11"]; s = N["dis_suites"]["T15"]
    rn = d["value"]["retained_normal"]; rb = d["value"]["retained_bmd"]; rd = d["value"]["retained_dmd"]
    dsweep = d["detail"]["severity_sweep"]; srow = s["detail"]["ladder"]
    drow = "".join("<tr><td>%.2f</td><td>%.4f</td></tr>" % (r["dystrophin"], r["retained"]) for r in dsweep)
    arow = "".join("<tr><td>%.2f</td><td>%.3f</td><td>%.3f</td><td>%.4f</td><td>%.0f&nbsp;s</td></tr>"
        % (r["age_frac"], r["motor_unit_fraction"], r["fibre_size_fraction"], r["max_force"], r["fatigue_tau_s"])
        for r in srow)
    answer = ("Two ways muscle loses force, both perturbations of the contractile contact number (&sect;3). "
        "<b>Muscular dystrophy</b> is dystrophin-loss fragility: each contraction tears load-bearing contacts, a "
        "cyclic fatigue whose rate is set by the reading-frame rule &mdash; Duchenne (null) retains only %.2f of "
        "force at the test cycle count versus Becker (partial) %.2f and normal %.2f. <b>Sarcopenia</b> is a "
        "gradual multi-axis ageing decline. Both verified [V]." % (rd, rb, rn))
    abstract = ("Dystrophin couples the contractile lattice to the membrane; its loss makes fibres fragile, so a "
        "Paris/Basquin law removes contacts per contraction with rate &prop; (1&minus;dystrophin)&sup2;. The "
        "reading-frame rule (Monaco 1988) sets severity, NOT a fit: DMD (null) declines far faster than BMD "
        "(in-frame, partial). The loss is structural and NON-recovering, distinct from the reversible metabolic "
        "fatigue of T5/T10. Sarcopenia declines max force and fatigue &tau; together along motor-unit, fibre and "
        "endurance axes. Mechanism [V]; reading-frame ordering [L]; absolute timeline/force [O].")
    body = (
      "<h2>Dystrophy: fragility as contractile-contact fatigue</h2>"
      "<p>The contractile apparatus is a load-bearing lattice (the same contact-number order parameter as the "
      "length-tension test T2). Dystrophin anchors that lattice to the sarcolemma and ECM; without it, the "
      "membrane and cytoskeleton are mechanically FRAGILE, so every forceful contraction tears a few "
      "load-bearing contacts. That is a cyclic fatigue process &mdash; the same Paris/Basquin law used for OA "
      "(&sect;12) &mdash; with the per-contraction damage rate set by fragility = (1 &minus; dystrophin). The "
      "force loss is STRUCTURAL and does not recover on rest, which is what distinguishes it from the reversible "
      "metabolic fatigue of T5 and T10.</p>"
      "<h2>The reading-frame rule sets severity (no fit)</h2>"
      "<p>Severity is CITED from the dystrophin reading-frame rule (Monaco 1988): out-of-frame / nonsense "
      "deletions abolish dystrophin &rarr; Duchenne (severe); in-frame deletions leave a partial, shortened but "
      "functional dystrophin &rarr; Becker (mild). Mapping that to a fragility (null &asymp; 0, partial &asymp; "
      "0.5, normal = 1.0), retained force at the test cycle count falls monotonically as dystrophin falls:</p>"
      "<table><thead><tr><th>dystrophin</th><th>retained force</th></tr></thead><tbody>%s</tbody></table>"
      "<p>Normal stays at full force (%.2f), Becker declines slowly (%.2f) and Duchenne collapses (%.2f), and "
      "the Duchenne trajectory is progressive across contraction count &mdash; the documented severity order, "
      "reproduced from the genotype rule alone.</p>"
      "<h2>Sarcopenia: gradual multi-axis ageing</h2>"
      "<p>Ageing muscle loss is different in character: not a fast fibre-tearing defect but a gradual decline "
      "along several axes at once &mdash; motor-unit dropout (recruitment), type-II fibre atrophy (the contact "
      "number) and reduced fatigue resistance (a shorter T5 &tau;). Scaling all three with an age parameter:</p>"
      "<table><thead><tr><th>age (frac)</th><th>motor units</th><th>fibre size</th><th>max force</th>"
      "<th>fatigue &tau;</th></tr></thead><tbody>%s</tbody></table>"
      "<p>Maximum force falls AND fatigue onsets earlier with age, simultaneously across axes &mdash; the "
      "sarcopenia direction. The cited direction is ~1&nbsp;%%/yr strength loss after ~50; the absolute force and "
      "rate are not fixed by the substrate [O].</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>For dystrophy the absolute age-at-milestone (loss of ambulation, etc.) is not fixed by the substrate "
      "[O]; the reading-frame ORDER and the progressive shape are the result. For sarcopenia the DIRECTION is "
      "claimed; absolute force and the rate of loss are [O].</p>" % (drow, rn, rb, rd, arow))
    cards = [gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"])]
    oneliner = ("Dystrophy = contractile-contact fatigue with reading-frame severity (DMD %.2f &lt; BMD %.2f &lt; "
        "normal %.2f) [V]; sarcopenia = gradual multi-axis ageing decline [V]; absolute timeline/force [O]."
        % (rd, rb, rn))
    return answer, abstract, body, cards, oneliner

def sec_t12_channelopathy(N):
    t = N["dis_suites"]["T12"]; v = t["value"]
    btn = v["block_threshold_normal"]; btm = v["block_threshold_myotonia"]; btp = v["block_threshold_paralysis"]
    probe = t["detail"]["probe_drive"]; sn = t["detail"]["spikes_at_probe_normal"]
    sm = t["detail"]["spikes_at_probe_myotonia"]; sp_ = t["detail"]["spikes_at_probe_paralysis"]
    sweep = t["detail"]["severity_sweep"]
    srow = "".join("<tr><td>%.2f</td><td>%s</td></tr>" % (r["beta"], ("%.2f" % r["block_threshold"]) if r["block_threshold"] is not None else "&gt; 2.0 (no block)") for r in sweep)
    answer = ("Muscle channelopathies are perturbations of membrane excitability &mdash; the FitzHugh-Nagumo "
        "substrate itself. <b>Myotonia</b> (CLCN1/SCN4A gain) is hyperexcitable: it RAISES the "
        "depolarization-block threshold to %.2f (versus normal %.2f), giving repetitive discharge and delayed "
        "relaxation. <b>Periodic paralysis</b> (SCN4A/CACNA1S) LOWERS it to %.2f, so a small depolarizing shift "
        "silences the fibre &mdash; the opposite sign, like the MG/LEMS pair [V]." % (btm, btn, btp))
    abstract = ("The block threshold is the sustained depolarizing drive at which firing collapses (Na "
        "inactivation). It moves monotonically with the recovery conductance: myotonia (hyperexcitable) pushes it "
        "UP (%.2f), periodic paralysis (inactivation-prone) pushes it DOWN (%.2f), bracketing normal (%.2f). At a "
        "depolarizing challenge of %.2f, myotonia still fires (%d spikes) while paralysis is silenced (%d) and "
        "normal is at its block edge (%d). Excitability perturbation [V]; clinical signs [L]; absolute [O]."
        % (btm, btp, btn, probe, sm, sp_, sn))
    body = (
      "<h2>Excitability is the substrate, so its diseases are too</h2>"
      "<p>The kit's membrane model is the FitzHugh-Nagumo relaxation oscillator vendored in the substrate. "
      "Skeletal-muscle channelopathies perturb exactly that excitability, so they are the most direct test of "
      "the substrate at the membrane level &mdash; no added mechanism. The relevant quantity is the "
      "<b>depolarization-block threshold</b>: the sustained depolarizing drive above which the membrane stops "
      "firing because the fast (sodium-like) channel inactivates. Normal muscle fires in its operating window "
      "and blocks only under a strong depolarizing shift.</p>"
      "<h2>Two opposite signs from one membrane</h2>"
      "<p><b>Myotonia congenita</b> (loss of the CLCN1 chloride conductance, or SCN4A gain) makes the membrane "
      "HYPEREXCITABLE: it resists block, firing repetitively even under a depolarizing challenge that quiets a "
      "normal fibre &mdash; the electrical correlate of myotonic runs and delayed muscle relaxation. In the "
      "model its block threshold rises to %.2f against normal %.2f.</p>"
      "<p><b>Periodic paralysis</b> (SCN4A / CACNA1S) is the opposite: the membrane is INACTIVATION-PRONE, so a "
      "modest depolarizing shift (a potassium disturbance) tips it into depolarization block &mdash; the fibre "
      "becomes inexcitable and the muscle is transiently paralysed. Its block threshold falls to %.2f. The two "
      "diseases therefore bracket normal from opposite sides, exactly as myasthenia and Lambert-Eaton do at the "
      "synapse (&sect;10).</p>"
      "<h2>Monotone in the channel defect</h2>"
      "<p>Sweeping the recovery conductance, the block threshold moves monotonically &mdash; more "
      "inactivation-prone, lower threshold:</p>"
      "<table><thead><tr><th>recovery &beta;</th><th>block threshold</th></tr></thead><tbody>%s</tbody></table>"
      "<p>At a depolarizing challenge of %.2f, the three states separate cleanly: myotonia fires %d spikes, "
      "normal %d (at its block edge), periodic paralysis %d (silenced). The DIRECTIONS are the result.</p>"
      "<h2>Seam and what is NOT claimed</h2>"
      "<p>The specific channel mutation is cited from the genetics/neuro side; the in-class result is the "
      "muscle-membrane excitability sign. The clinical signs are cited [L]; the absolute membrane parameters "
      "(true conductances, exact thresholds in mV) are not fixed by the substrate [O].</p>"
      % (btm, btn, btp, srow, probe, sm, sn, sp_))
    cards = [gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"])]
    oneliner = ("Myotonia raises the depolarization-block threshold (%.2f), periodic paralysis lowers it (%.2f) "
        "vs normal (%.2f) &mdash; opposite excitability signs from one FHN membrane [V]; absolute [O]."
        % (btm, btp, btn))
    return answer, abstract, body, cards, oneliner

def sec_t13_stress_fracture(N):
    t = N["dis_suites"]["T13"]; v = t["value"]; cyc = t["detail"]["cycle_curve"]
    yld = v["single_event_yield_spinodal"]; du = t["detail"]["healing_density_unloaded"]; dl = t["detail"]["healing_density_loaded"]
    crow = "".join("<tr><td>%s</td><td>%.4f</td></tr>" % ("{:,}".format(r["cycles"]), r["contact_number"]) for r in cyc)
    lad = t["detail"]["ladder"]
    lrow = "".join("<tr><td>%s</td><td>%.1f</td><td>%.3f</td><td>%s</td></tr>"
        % (esc(r["regime"]), r["sigma_over_endurance"], r["contact_number_final"], "yes" if r["fractured"] else "no")
        for r in lad)
    answer = ("Stress fracture is bone fatigue BELOW the single-event yield. T4's Wolff threshold (spinodal "
        "%.4f) is the load that flips bone in one step; bone also has a lower fatigue ENDURANCE LIMIT, and "
        "cyclic load above it accumulates microdamage until the bone contact network fails &mdash; the runner's "
        "stress fracture &mdash; even though no single cycle reaches yield. Sub-endurance load is protected. And "
        "the fracture HEALS: load re-crosses the switch to the dense basin [V]." % yld)
    abstract = ("A Paris/Basquin law on the bone contact number, thresholded at the fatigue endurance limit "
        "(below the T3 yield), removes contacts only for supra-endurance cyclic load. Sub-endurance loading is "
        "protected indefinitely (the S-N plateau); supra-endurance, sub-yield loading fractures after enough "
        "cycles, faster at higher load. Crucially bone HEALS &mdash; from a fractured low-density state, "
        "physiologic load drives density back from %.2f to %.2f (callus = T3 re-cross), unlike cartilage/OA. "
        "Shape + healing [V]; endurance-limit + damage-law form [L]; absolute cycles-to-fracture [O]."
        % (du, dl))
    body = (
      "<h2>Two thresholds, not one</h2>"
      "<p>T4 (Wolff) established a single-event YIELD threshold: a load above the spinodal flips bone to the "
      "dense basin in one step. But bone, like any load-bearing solid, also has a lower FATIGUE ENDURANCE LIMIT. "
      "Between the endurance limit and the yield threshold lies the stress-fracture regime: each individual "
      "cycle is sub-yield and &lsquo;safe&rsquo;, yet repeated loading accumulates microdamage in the contact "
      "network until it fails. This is the classic stress fracture of runners and military recruits &mdash; "
      "injury from repetition, not from a single overload.</p>"
      "<h2>Sub-yield, but it still breaks</h2>"
      "<p>Applying the same Paris/Basquin damage law used for OA to the bone contact number, with the damage "
      "threshold at the endurance limit, the regimes separate:</p>"
      "<table><thead><tr><th>regime</th><th>&sigma;/endurance</th><th>final contact no.</th>"
      "<th>fractured?</th></tr></thead><tbody>%s</tbody></table>"
      "<p>Sub-endurance loading (rest, easy activity) is protected indefinitely. Supra-endurance loading, though "
      "still sub-yield, accumulates damage; at the running load the contact number declines progressively with "
      "cycle count:</p>"
      "<table><thead><tr><th>load cycles</th><th>contact number</th></tr></thead><tbody>%s</tbody></table>"
      "<p>Higher loads fracture in fewer cycles &mdash; an S-N (W&ouml;hler) curve. This is distinct from T4: "
      "the bone never sees a yield-level single event.</p>"
      "<h2>And it heals (unlike cartilage)</h2>"
      "<p>Bone repairs itself, and the same T3 switch explains it: from a fractured, low-density state, "
      "physiologic loading re-crosses the R19 switch to the dense basin (density rises from %.2f to %.2f) "
      "&mdash; the callus and remodelling of fracture healing. This is a meaningful contrast with cartilage: OA "
      "(&sect;12) unjams irreversibly because cartilage cannot remodel back, while bone fractures heal because "
      "it can. The same substrate captures both the failure and the repair.</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>The SHAPE (endurance plateau, accelerating supra-endurance failure, S-N ordering) and the load-driven "
      "healing re-cross are the result; the endurance-limit concept and the damage-law form are cited [L]. The "
      "absolute number of cycles to fracture is not fixed by the substrate and stays [O].</p>"
      % (lrow, crow, du, dl))
    cards = [CARD_SPINODAL, CARD_BARRIER, gamma_card("RUNX2", "bone", N["gammas"]["bone"])]
    oneliner = ("Stress fracture = sub-yield cyclic bone fatigue above an endurance limit (S-N), sub-endurance "
        "protected [V]; and the fracture HEALS via T3 re-cross (%.2f&rarr;%.2f) unlike OA; absolute cycles [O]."
        % (du, dl))
    return answer, abstract, body, cards, oneliner

def sec_t14_tendinopathy(N):
    t = N["dis_suites"]["T14"]; lad = t["detail"]["ladder"]
    rows = "".join("<tr><td>%s</td><td>%.1f&times;</td><td>%.3f</td><td>%.3f</td></tr>"
        % (esc(r["loading"]), r["sigma_over_sigma_star"], r["contact_number_final"], r["fibre_loss"]) for r in lad)
    over = next(r for r in lad if r["loading"] == "overuse")
    answer = ("Tendinopathy is the tendon analogue of osteoarthritis: cyclic-fatigue unjamming of a load-bearing "
        "collagen network. Overuse drives the same Paris/Basquin damage law (&sect;12) on the tendon contact "
        "number, so fibres are lost progressively &mdash; %.1f%% at overuse &mdash; while sub-threshold use is "
        "protected and loss accelerates with overuse. Shape verified [V] on the cited damage-law form." %
        (over["fibre_loss"] * 100))
    abstract = ("A tendon is a load-bearing collagen contact network; tendinopathy is its cyclic-fatigue "
        "degeneration under overuse. Reusing the OA Paris/Basquin law (exponent m=2, FORM cited) on the tendon "
        "contact number: sub-threshold use is protected, fibre loss rises with overuse load and is convex. Same "
        "kernel, different tissue. Shape [V]; damage-law form [L]; absolute progression rate [O].")
    body = (
      "<h2>The same unjamming, a different tissue</h2>"
      "<p>Tendon is modelled as a load-bearing collagen network &mdash; the same kind of contact-number order "
      "parameter as cartilage. <b>Tendinopathy</b> is overuse fatigue of that network: repetitive "
      "supra-threshold loading accumulates damage and progressively degrades the collagen, exactly as cyclic "
      "loading unjams cartilage in OA. So the OA fatigue kernel transfers directly, with no new mechanism, only "
      "a different tissue.</p>"
      "<h2>Sub-threshold protected, overuse accelerates</h2>"
      "<table><thead><tr><th>loading</th><th>&sigma;/&sigma;*</th><th>final contact no.</th>"
      "<th>fibre loss</th></tr></thead><tbody>%s</tbody></table>"
      "<p>Rest and sub-threshold use are protected (no loss); fibre loss rises with overuse load and is convex "
      "&mdash; the documented dose effect of training overload. The mechanism is collagen-network unjamming "
      "under cyclic fatigue.</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>The SHAPE is the result and the Paris/Basquin damage-law FORM is cited [L]; the absolute progression "
      "rate (the rate constant) is not fixed by the substrate and stays [O]. Tendinopathy was a registered "
      "open-material item in the previous version; giving it the OA kernel moves it from [O] to a verified "
      "shape, while the absolute rate remains open.</p>" % rows)
    cards = [gamma_card("MYOD1", "skeletal_muscle", N["gammas"]["skeletal_muscle"]), CARD_SPINODAL]
    oneliner = ("Tendinopathy = cyclic-fatigue unjamming of the tendon collagen contact number (OA kernel): "
        "sub-threshold protected, loss convex in overuse [V]; absolute rate [O].")
    return answer, abstract, body, cards, oneliner

def sec_t16_osteomalacia(N):
    t = N["dis_suites"]["T16"]; lad = t["detail"]["ladder"]
    rows = "".join("<tr><td>%s</td><td>%.2f</td><td>%.3f</td><td>%.3f</td></tr>"
        % (esc(r["state"]), r["mineral_supply"], r["matrix_occupancy_at_load"], r["mineral_density_at_load"]) for r in lad)
    defc = next(r for r in lad if r["state"] == "rickets/osteomalacia")
    answer = ("Osteomalacia and rickets are a mineralization ceiling, not a remodeling defect. The T4 switch lays "
        "down bone matrix normally &mdash; under load the matrix occupancy still reaches full &mdash; but "
        "mineralization needs mineral, so vitamin-D / phosphate deficiency caps radiographic density at the "
        "supply ceiling (%.2f here). The decisive contrast: LOAD rescues osteoporosis but CANNOT rescue "
        "osteomalacia, because the mineral itself is missing [V]." % defc["mineral_density_at_load"])
    abstract = ("Radiographic density = matrix occupancy (set by the T3 switch) &times; mineral supply M. The "
        "switch builds osteoid normally, so loading drives occupancy to full; but density is capped at M, which "
        "falls with 25-OH-vitamin-D / phosphate deficiency (replete=1.0, deficient~0.5, severe/XLH~0.3). "
        "Density is monotone in supply. The key discriminant against osteoporosis: under the same load, the "
        "osteoporotic matrix is rescued (occupancy &rarr; full) while osteomalacic density stays capped &mdash; "
        "osteoporosis is load-responsive, osteomalacia is mineral-limited. Mechanism [V]; ceiling form [L]; "
        "absolute mineral density [O].")
    body = (
      "<h2>Two different low-density diseases</h2>"
      "<p>It is tempting to lump every low-bone-density disease together, but the substrate separates them by "
      "MECHANISM. Osteoporosis (&sect;9) is a remodeling/threshold disease: too little load lets the switch fall "
      "to the resorbed basin, and crucially it is REVERSIBLE &mdash; restore load and density climbs back. "
      "Osteomalacia and rickets are different: the remodeling switch works, the matrix (osteoid) is laid down, "
      "but it cannot be MINERALIZED because the mineral (calcium-phosphate, gated by vitamin D and phosphate) is "
      "in short supply.</p>"
      "<h2>Density = matrix occupancy &times; mineral supply</h2>"
      "<p>We write radiographic density as the matrix occupancy from the T3 switch multiplied by a mineral "
      "supply fraction M. Under physiologic load the switch drives occupancy to full, but the achievable "
      "density is capped at M, and M falls with deficiency:</p>"
      "<table><thead><tr><th>state</th><th>mineral supply M</th><th>matrix occupancy at load</th>"
      "<th>mineral density at load</th></tr></thead><tbody>%s</tbody></table>"
      "<p>The matrix column is full in every row &mdash; the bone-building switch is not the problem &mdash; yet "
      "the density column is capped at the supply ceiling and falls monotonically with deficiency. That is the "
      "soft, deformable, radiolucent bone of rickets/osteomalacia: plenty of osteoid, too little mineral.</p>"
      "<h2>The decisive test: load cannot rescue it</h2>"
      "<p>This is what makes the model falsifiable rather than a relabelling. Osteoporosis and osteomalacia both "
      "show low density, but they respond to loading in OPPOSITE ways. Apply the same physiologic load to a "
      "low-density bone: if the deficit is osteoporotic (matrix in the resorbed basin), load rescues it &mdash; "
      "occupancy returns to full. If the deficit is osteomalacic (mineral-capped), load drives the matrix but "
      "density stays capped, because no amount of mechanical loading supplies the missing mineral. The substrate "
      "reproduces exactly this dissociation, which is the clinical basis for treating the two diseases "
      "completely differently (load/anti-resorptives vs vitamin D / phosphate).</p>"
      "<h2>What is NOT claimed</h2>"
      "<p>The mechanism (a mineral-supply ceiling that load cannot lift, and the osteoporosis contrast) is the "
      "result; the multiplicative ceiling FORM is the cited modelling choice [L]. The absolute mineral density "
      "for a given vitamin-D / phosphate level is not fixed by the substrate and stays [O].</p>" % rows)
    cards = [CARD_SPINODAL, gamma_card("RUNX2", "bone", N["gammas"]["bone"])]
    oneliner = ("Osteomalacia/rickets = mineralization ceiling (density = matrix &times; mineral supply); load "
        "rescues osteoporosis but NOT osteomalacia [V]; absolute mineral density [O].")
    return answer, abstract, body, cards, oneliner

def sec_t17_osteolytic(N):
    t = N["dis_suites"]["T17"]; v = t["value"]
    nlo, nhi = t["detail"]["density_normal_low_to_high"]; mlo, mhi = t["detail"]["myeloma_density_low_to_high"]
    gct = t["detail"]["gct_density_from_dense"]
    answer = ("Osteolytic bone disease is osteoclast/osteoblast UNCOUPLING &mdash; the exact mirror of "
        "osteopetrosis. Osteopetrosis (&sect;9) disables resorption and locks density HIGH; multiple myeloma "
        "disables FORMATION (osteoblast suppression), so loading cannot re-form bone and density stays lytic "
        "(%.2f vs a normal %.2f under the same load). Giant-cell tumour adds a strong RANKL resorptive drive "
        "that resorbs even dense bone [V]." % (mhi, nhi))
    abstract = ("On the T3/T6 mechanostat, normal bone couples resorption (down) and formation (up): from a "
        "resorbed state, load re-forms bone (density 0&rarr;%.2f). Multiple myeloma suppresses osteoblasts "
        "(DKK1) while RANKL drives resorption, disabling the formation arm &mdash; loading cannot lift density "
        "past a low cap (0&rarr;%.2f), a lytic lesion that does not heal. This is the precise MIRROR of "
        "osteopetrosis (resorption disabled &rarr; locked high). Giant-cell tumour drives RANKL osteoclast "
        "recruitment, resorbing even dense bone (&rarr;%.2f). Mechanism [V]; absolute lesion size/incidence [O]."
        % (nhi, mhi, gct))
    body = (
      "<h2>The mechanostat has two arms; disease disables one</h2>"
      "<p>Bone remodeling couples two opposing processes: osteoclast RESORPTION (the down arm) and osteoblast "
      "FORMATION (the up arm). The T3 hysteresis loop (&sect;4) and osteopetrosis (&sect;9) already exercised "
      "this: osteopetrosis disables the resorption arm, so density can only go up and locks HIGH. Osteolytic "
      "bone disease is the opposite lesion &mdash; disable the FORMATION arm.</p>"
      "<h2>Myeloma: formation disabled, locked lytic</h2>"
      "<p>In multiple myeloma, tumour-secreted DKK1 and related factors suppress osteoblasts while RANKL drives "
      "osteoclast resorption. In mechanostat terms the up arm is disabled: starting from a resorbed state, "
      "increasing load re-forms bone in normal tissue (density %.2f &rarr; %.2f) but in myeloma the density "
      "cannot climb past a low cap (%.2f &rarr; %.2f) &mdash; the punched-out lytic lesion that, unlike a "
      "fracture (&sect;16), does NOT heal under loading because the bone-forming response itself is gone. This "
      "is the exact mirror of osteopetrosis: one disease removes the down arm and locks density high, the other "
      "removes the up arm and locks it low.</p>"
      "<h2>Giant-cell tumour: a strong resorptive drive</h2>"
      "<p>Giant-cell tumour of bone recruits osteoclasts through massive RANKL signalling. That is a strong "
      "resorptive (negative) drive: applied to dense bone it pushes the switch past the resorption spinodal and "
      "density collapses (&rarr; %.2f) &mdash; aggressive local osteolysis. The same RANKL axis is why "
      "denosumab (anti-RANKL) treats both myeloma bone disease and giant-cell tumour, which the shared "
      "mechanism makes natural.</p>"
      "<h2>Why this is the mechanostat, not the carcinogen kernel</h2>"
      "<p>These are tumour-associated, but the BONE lesion is not a carcinogen dose-response (&sect;7) &mdash; it "
      "is osteoclast/osteoblast uncoupling on the remodeling switch. Modelling them here, as perturbations of "
      "the T3/T6 mechanostat, places the mechanism where it actually acts. The absolute lesion size and "
      "incidence are not fixed by the substrate and stay [O].</p>" % (nlo, nhi, mlo, mhi, gct))
    cards = [CARD_SPINODAL, CARD_BARRIER, gamma_card("RUNX2", "bone", N["gammas"]["bone"])]
    oneliner = ("Osteolytic bone disease = osteoclast/osteoblast uncoupling: myeloma disables formation (locked "
        "lytic %.2f), the mirror of osteopetrosis; GCT's RANKL drive resorbs dense bone (&rarr;%.2f) [V]; "
        "absolute lesion [O]." % (mhi, gct))
    return answer, abstract, body, cards, oneliner

# =====================================================================================================
#  ANALGESIC AXIS (sec 25-28) -- the inherited non-opioid three-lever threshold logic applied to the
#  painful diseases this volume owns. Reuses the disease kernels (SSOT) via the live analgesia suite.
# =====================================================================================================
def _anlg(N, target):
    return N["anlg_suites"].get(target, {}).get("detail", {})

def _lever_sweep_table(sweep, val_key, val_head, knob_key, knob_head):
    rows = "".join("<tr><td>%.1f</td><td>%s</td><td>%s</td></tr>"
                   % (r["intensity"], esc(r.get(knob_key)), esc(r.get(val_key))) for r in sweep)
    return ("<table><thead><tr><th>lever intensity</th><th>%s</th><th>%s</th></tr></thead><tbody>"
            % (knob_head, val_head) + rows + "</tbody></table>")

def _paired_sweep_table(sweep, losses, val_key, val_head, loss_head):
    rows = "".join("<tr><td>%.1f</td><td>%s</td><td>%s</td></tr>"
                   % (sweep[i]["intensity"], esc(sweep[i].get(val_key)), esc(losses[i]))
                   for i in range(min(len(sweep), len(losses))))
    return ("<table><thead><tr><th>lever intensity</th><th>%s</th><th>%s</th></tr></thead><tbody>"
            % (val_head, loss_head) + rows + "</tbody></table>")

# ===== sec 25  methodology: the three-lever threshold logic (inherited) ===============================
def sec_analgesic_axis(N):
    g_bone = N["gammas"]["bone"]
    anlg = N["anlg"]
    n_scored = len([s for s in anlg["suites"] if not s.get("honest_open_or_partial")])
    answer = ("Pain here is a THRESHOLD-CROSSING rate on the same DNA-grounded R19 switch the diseases perturb: "
        "a noxious drive erodes the escape barrier and the nociceptor fires at a Kramers rate. Every non-opioid "
        "analgesic pulls one of three levers &mdash; L1 raise the peripheral barrier, L2 lower the drive, L3 cut "
        "the central gain &mdash; a technique inherited from the VP non-opioid analgesic volume.")
    abstract = ("This axis adds no new physics. It imports the three-lever non-opioid analgesic technique "
        "(concept DOI 10.5281/zenodo.20733420) and expresses it on the SAME R19 barrier &Delta;V = &gamma;&sup2;/4 "
        "this volume already emerges from a measured gene parameter (bone&rsquo;s RUNX2, &gamma; = %.4f). "
        "Nociception is modelled as a threshold-crossing rate exp(&minus;&Delta;V<sub>eff</sub>/D); the noxious "
        "drive h is READ from each disease kernel&rsquo;s own cited severity (single source). %d painful diseases "
        "are graded by DIRECTION (No-Tuning): pulling an in-scope lever must lower the crossing rate monotonically, "
        "and the real drug or load is the cited anchor for WHICH lever it pulls. The engine hash is unchanged." 
        % (g_bone, n_scored))
    body = (
      "<h2>Pain as a threshold-crossing rate (no new physics)</h2>"
      "<p>A nociceptor terminal is treated as an excitable R19 element with the same escape barrier the rest of "
      "this volume uses: &Delta;V = &gamma;&sup2;/4. A noxious drive h pushes the membrane state toward the saddle, "
      "and the firing (threshold-crossing) rate follows a Kramers law, rate &asymp; exp(&minus;&Delta;V<sub>eff</sub>/D).</p>"
      "<p>The effective barrier is &Delta;V<sub>eff</sub> = max(0, &gamma;&sup2;/4 + &Delta;V<sub>L1</sub> &minus; "
      "&kappa;h): the drive h erodes it, and a peripheral block adds &Delta;V<sub>L1</sub> back. The perceived "
      "signal is a downstream gain g times that rate. Nothing new is introduced &mdash; this is the inherited "
      "analgesic logic on the barrier the genome already set.</p>"
      "<h2>The three levers (inherited from the analgesic volume)</h2>"
      "<p>The three-lever organising principle is the core technique of the VP non-opioid analgesic volume "
      "(<a href=\"%s\" rel=\"noopener\">DOI 10.5281/zenodo.20733420</a>), reused here verbatim, exactly as the "
      "neuro R19/FHN primitives are vendored. Every non-opioid analgesic acts on exactly one lever:</p>"
      "<ul>"
      "<li><b>L1 &mdash; raise the peripheral threshold</b> (&Delta;V<sub>L1</sub> up &rarr; rate down). Anchors: "
      "local anaesthetics / Na<sub>v</sub> blockers, topical agents. Structure-DECOUPLED.</li>"
      "<li><b>L2 &mdash; lower the noxious drive</b> (h down &rarr; rate down). Anchors: NSAIDs/coxibs and &mdash; "
      "the musculoskeletal special case &mdash; mechanical unloading. Structure-COUPLED.</li>"
      "<li><b>L3 &mdash; reduce the central gain</b> (g down &rarr; signal down). Anchors: gabapentinoids, SNRIs. "
      "This is CENTRAL gain, owned by neuro / mind.</li>"
      "</ul>"
      "<p>Opioids act on a fourth, descending / &mu;-receptor lever; that is outside the non-opioid logic and is "
      "not modelled here.</p>"
      "<h2>Scope (strictly inside the musculoskeletal volume)</h2>"
      "<p>L2 is fully in scope because the musculoskeletal noxious drive IS the mechanical load knob the disease "
      "kernel already perturbs &mdash; so lowering it is the same operation that arrests the lesion (the "
      "convergence in &sect;26). L1 is in scope as a DIRECTION result on the vendored substrate, with the real "
      "agent as the cited anchor.</p>"
      "<p>L3 central gain is reached only as a NAMED SEAM to neuro / mind and is never re-emerged here (single "
      "source of truth). Neuropathic pain, fibromyalgia and central sensitisation syndromes are routed to sibling "
      "volumes, as in the out-of-class register (&sect;20).</p>"
      "<h2>How each lever is verified (No-Tuning)</h2>"
      "<p>Each lever is a monotone sweep, intensity 0 to 1. It passes when the crossing rate (L1/L2) moves "
      "monotonically down; the intensity is never tuned to a pain score. The decisive cross-check (&sect;27) is "
      "that L2 also lowers the disease&rsquo;s own structural loss (coupled) while L1 leaves it unchanged "
      "(decoupled).</p>"
      "<h2>Map of the analgesic cluster</h2>"
      "<p>The per-disease detail is split across three further pages so each answer stays self-contained:</p>"
      "<ul>"
      "<li><a href=\"%s\">&sect;26 &mdash; L2 on the load-bearing diseases</a>: osteoarthritis, tendinopathy, "
      "stress fracture &mdash; where analgesia and disease-modification converge.</li>"
      "<li><a href=\"%s\">&sect;27 &mdash; L1 and the coupled / decoupled discriminant</a>: the falsifiable test, "
      "plus osteolytic / myeloma bone pain.</li>"
      "<li><a href=\"%s\">&sect;28 &mdash; Limits and the central-gain seam</a>: L3 routed out, opioid lever out "
      "of scope, exertional muscle pain, neuropathic routing.</li>"
      "</ul>") % (ANALGESIC_DOI_URL,
                  page_url("26-analgesic-l2-drive-load-bearing-convergence"),
                  page_url("27-analgesic-l1-threshold-coupled-decoupled-discriminant"),
                  page_url("28-analgesic-limits-and-central-gain-seam"))
    cards = [CARD_NOCICEPTION, CARD_BARRIER, gamma_card("RUNX2", "bone", g_bone)]
    oneliner = ("Non-opioid analgesia = pull one of three levers on the nociceptive THRESHOLD-CROSSING rate on the "
        "same DNA-grounded R19 barrier (L1 raise the peripheral barrier / L2 lower the noxious drive / L3 cut the "
        "central gain). Technique inherited from the VP non-opioid analgesic volume (DOI 10.5281/zenodo.20733420); "
        "the noxious drive is read from each disease kernel (single source). PASS = crossing rate falls "
        "monotonically (DIRECTION, No-Tuning). L3 central gain is a neuro/mind seam; opioid lever out of scope. "
        "Engine hash unchanged.")
    keywords = ["non-opioid analgesia mechanism", "pain threshold logic", "nociceptor Kramers crossing rate",
                "three-lever analgesic model", "R19 escape barrier", "peripheral vs central analgesia",
                "NSAID mechanism of action", "DNA-grounded simulation", "musculoskeletal pain", "No-Tuning reproducible model"]
    return answer, abstract, body, cards, oneliner, keywords

# ===== sec 26  L2 on the load-bearing diseases: the convergence ======================================
def sec_analgesic_l2(N):
    oa = _anlg(N, "Ax-T9"); td = _anlg(N, "Ax-T14"); sf = _anlg(N, "Ax-T13")
    g_cart = N["gammas"]["cartilage"]; g_bone = N["gammas"]["bone"]
    oa_l2 = oa.get("lever_map", {}).get("L2", {}).get("sweep", [])
    oa_loss = oa.get("L2_lesion_loss_sweep", [])
    answer = ("In the load-bearing diseases the noxious drive IS the mechanical load on the failing structure, so "
        "the L2 lever (unload / NSAID) lowers BOTH the nociceptive crossing rate AND the cartilage, tendon or bone "
        "loss. Analgesia and disease-modification are the same operation &mdash; one knob, two effects &mdash; for "
        "osteoarthritis, tendinopathy and stress fracture.")
    abstract = ("Osteoarthritis, tendinopathy and stress-fracture pain share one structure: a supra-threshold "
        "mechanical load drives both the Paris/Basquin contact loss (the lesion) and the nociceptor (the pain). "
        "Because both read the SAME load knob, the L2 sweep that lowers the crossing rate also lowers the "
        "disease&rsquo;s own contact loss &mdash; verified here on the cartilage (SOX9, &gamma; = %.4f) and bone "
        "(RUNX2, &gamma; = %.4f) switches. This convergence is the musculoskeletal signature: the disease-modifying "
        "move (offload) is itself the dominant analgesic move, by DIRECTION and No-Tuning." % (g_cart, g_bone))
    body = (
      "<h2>Why L2 is the musculoskeletal lever</h2>"
      "<p>In a degenerating joint, an overused tendon or a fatigued bone, the noxious input is the mechanical "
      "overload itself. That overload is exactly the knob the disease kernel perturbs (the relative load "
      "&sigma;/&sigma;* in the cyclic-fatigue law). So the noxious drive h is read straight from the disease, not "
      "invented.</p>"
      "<p>Lowering h is therefore one move with two consequences: the nociceptor fires less, and the structure "
      "stops losing contacts. This is why, in this volume, the L2 analgesic lever and the mirror disease-modifying "
      "treatment (&sect;22) are the same operation.</p>"
      "<h2>Osteoarthritis: the L2 sweep lowers rate and lesion together</h2>"
      "<p>As the L2 lever unloads the joint (intensity 0 &rarr; 1), the nociceptor crossing rate falls "
      "monotonically:</p>"
      + _lever_sweep_table(oa_l2, "rate", "nociceptive crossing rate", "drive_h", "noxious drive h")
      + "<p>And the SAME sweep lowers the cartilage&rsquo;s own contact loss &mdash; the lesion arrests as the pain "
      "falls (the convergence):</p>"
      + _paired_sweep_table(oa_l2, oa_loss, "rate", "crossing rate", "cartilage contact loss")
      + "<p>Real anchors for the L2 lever in OA: %s. The mirror disease-modifying treatment is the same unloading "
      "(&sect;22).</p>"
      "<h2>Tendinopathy and stress fracture: the same structure</h2>"
      "<p>Tendinopathy reuses the OA cyclic-fatigue kernel on a tendon contact number, so the L2 lever (deload) "
      "again lowers rate and tendon loss together; the mirror treatment then ADDS eccentric loading to rebuild, a "
      "separate up-step that is not analgesia. Stress-fracture pain is driven by supra-endurance cyclic bone load, "
      "so offloading below the endurance limit lowers the crossing rate and halts microdamage, letting the "
      "documented healing re-cross proceed.</p>"
      "<p>Anchors &mdash; tendinopathy L2: %s; stress fracture L2: %s. In all three, the load that hurts is the "
      "load that damages, so one lever moves both.</p>"
      ) % (esc(oa.get("L2_agent")), esc(td.get("L2_agent")), esc(sf.get("L2_agent")))
    cards = [CARD_NOCICEPTION, gamma_card("SOX9", "cartilage", g_cart), gamma_card("RUNX2", "bone", g_bone)]
    oneliner = ("L2 (lower the noxious drive) on osteoarthritis, tendinopathy and stress fracture: the noxious "
        "drive is the mechanical load the disease kernel perturbs, so unloading lowers BOTH the nociceptive "
        "crossing rate AND the structural contact loss (verified by DIRECTION). Analgesia and disease-modification "
        "converge on one knob; the mirror treatment (offload) is the dominant analgesic. No-Tuning.")
    keywords = ["osteoarthritis pain mechanism", "load reduction analgesia", "tendinopathy pain", "stress fracture pain",
                "mechanical unloading", "disease-modifying analgesia convergence", "Paris Basquin fatigue",
                "NSAID osteoarthritis", "nociceptive drive", "No-Tuning reproducible model"]
    return answer, abstract, body, cards, oneliner, keywords

# ===== sec 27  L1 + the coupled/decoupled discriminant + osteolytic bone pain =========================
def sec_analgesic_l1_discriminant(N):
    oa = _anlg(N, "Ax-T9"); ol = _anlg(N, "Ax-T17")
    g_bone = N["gammas"]["bone"]
    oa_l1 = oa.get("lever_map", {}).get("L1", {}).get("sweep", [])
    oa_l1_loss = oa.get("L1_lesion_loss_sweep", [])
    answer = ("The L1 lever (a peripheral block) lowers the crossing rate while leaving the lesion UNCHANGED, "
        "whereas L2 lowers both. That coupled-versus-decoupled contrast is the decisive, falsifiable test that this "
        "is a grounded kernel, not a relabelling: a lidocaine patch quietens an arthritic knee without changing the "
        "cartilage, exactly as the model predicts.")
    abstract = ("L1 raises the peripheral barrier &Delta;V<sub>L1</sub>; a full block restores the resting firing "
        "threshold against the present drive, so the crossing rate falls &mdash; but the mechanical load is "
        "untouched, so the disease&rsquo;s contact loss is FLAT. This is the structure-DECOUPLED signature, and its "
        "contrast with the structure-COUPLED L2 (&sect;26) is a real prediction the kernel makes and could fail. "
        "Osteolytic / myeloma bone pain is the clean L2 case where the antiresorptive that relieves the RANKL drive "
        "is simultaneously the mirror treatment and the analgesic; cancer bone pain is clinically opioid-first-line, "
        "and the opioid lever is honestly out of this non-opioid scope.")
    body = (
      "<h2>The decisive cross-check: coupled vs decoupled</h2>"
      "<p>Two levers both lower pain, but they differ in what they do to the LESION. L2 lowers the mechanical drive, "
      "so the structure stops losing contacts (coupled). L1 only raises the terminal&rsquo;s threshold, so the "
      "structure is untouched (decoupled).</p>"
      "<p>This is the test that the analgesic axis is grounded rather than cosmetic: the model PREDICTS that a "
      "peripheral block relieves pain with no structural change, and that prediction could fail but does not.</p>"
      "<h2>Osteoarthritis L1: rate falls, lesion flat</h2>"
      "<p>As the L1 lever raises the peripheral barrier (intensity 0 &rarr; 1), the crossing rate falls while the "
      "cartilage contact loss stays constant:</p>"
      + _paired_sweep_table(oa_l1, oa_l1_loss, "rate", "nociceptive crossing rate", "cartilage contact loss (flat)")
      + "<p>Contrast this with the L2 table in &sect;26, where the same drop in crossing rate is accompanied by a "
      "FALLING contact loss. Same disease, two levers, two different structural fingerprints &mdash; the "
      "discriminant. L1 anchor in OA: %s.</p>"
      "<h2>Osteolytic / myeloma bone pain: L2 = the mirror treatment as analgesia</h2>"
      "<p>Here the noxious drive is the RANKL-driven resorptive drive that destroys bone (h = 1.3 &times; spinodal, "
      "the cited resorptive drive itself on the RUNX2 switch, &gamma; = %.4f). The L2 lever is an antiresorptive "
      "(denosumab / zoledronate): removing the RANKL drive lowers BOTH the crossing rate AND the bone destruction.</p>"
      "<p>So for osteolytic bone, the L2 analgesic lever IS the mirror disease-modifying treatment (relieve the "
      "resorptive drive, &sect;22) &mdash; the same convergence, now on a resorptive rather than a load lesion. "
      "L2 anchor: %s.</p>"
      "<p><b>Honest scope:</b> cancer bone pain is clinically OPIOID-first-line; the non-opioid levers modelled here "
      "are ADJUNCTIVE, and the opioid (descending / &mu;) lever is outside the non-opioid logic and not modelled.</p>"
      ) % (esc(oa.get("L1_agent")), g_bone, esc(ol.get("L2_agent")))
    cards = [CARD_NOCICEPTION, CARD_BARRIER, gamma_card("RUNX2", "bone", g_bone)]
    oneliner = ("L1 (raise the peripheral barrier) lowers the crossing rate but leaves the lesion FLAT "
        "(structure-decoupled), while L2 lowers both (structure-coupled) -- that contrast is the decisive "
        "falsifiable discriminant. Osteolytic/myeloma bone pain is the clean L2 case where the antiresorptive that "
        "relieves the RANKL drive is both the mirror treatment and the analgesic; cancer bone pain is "
        "opioid-first-line and the opioid lever is honestly out of the non-opioid scope.")
    keywords = ["peripheral vs central analgesia", "lidocaine mechanism", "structure-coupled analgesia",
                "myeloma bone pain", "denosumab bone pain", "RANKL resorption", "cancer bone pain opioid",
                "falsifiable model discriminant", "nociceptor barrier", "No-Tuning reproducible model"]
    return answer, abstract, body, cards, oneliner, keywords

# ===== sec 28  honest limits + the central-gain seam =================================================
def sec_analgesic_limits_seam(N):
    ex = _anlg(N, "Ax-T15")
    answer = ("The central-gain lever (L3) is real but is OWNED by neuro / mind and is reached only as a named "
        "seam, never re-emerged here; the opioid lever is outside the non-opioid logic entirely. Exertional muscle "
        "pain has no discrete structural lesion to cross-check, and neuropathic and fibromyalgia pain are routed to "
        "sibling volumes &mdash; results stated as scope, not failures.")
    abstract = ("This page states what the analgesic axis does NOT claim. L3 (reduce the downstream gain) lowers the "
        "signal on the shared substrate, but central gain is a neuro / mind property; this volume cites it as a seam "
        "and does not re-emerge central pain (single source of truth). The opioid descending / &mu; lever is outside "
        "the non-opioid three-lever logic; exertional muscle pain is graded DIRECTION-only because there is no "
        "discrete contact-loss lesion to cross-check; and neuropathic pain, fibromyalgia and central sensitisation "
        "are routed to sibling volumes, exactly as in the out-of-class register (&sect;20).")
    body = (
      "<h2>L3 central gain: a seam, not re-emerged</h2>"
      "<p>The third lever reduces the downstream gain that amplifies a crossing into a perceived signal. On the "
      "shared substrate that lowers the signal monotonically, so the lever clearly exists. But central gain "
      "(dorsal-horn and descending modulation, central sensitisation) is a property of the neuro / mind volumes, "
      "not of load-bearing matter.</p>"
      "<p>So this volume names L3 as a SEAM to neuro / mind and stops there &mdash; it does not re-emerge central "
      "pain machinery (single source of truth). Gabapentinoids and SNRIs (duloxetine) are the L3 anchors, owned at "
      "that seam. This is the same discipline that routes fibromyalgia and neuropathic pain out (&sect;20).</p>"
      "<h2>The opioid lever is out of the non-opioid logic</h2>"
      "<p>Opioids raise central inhibitory tone through a separate descending / &mu;-receptor lever. That is a "
      "fourth lever, outside the non-opioid three-lever technique, and is not modelled here. Where opioids are "
      "clinically first-line (e.g. cancer bone pain, &sect;27), the non-opioid levers are stated as adjunctive.</p>"
      "<h2>Exertional muscle pain: DIRECTION only (honest partial)</h2>"
      "<p>Exertional and overuse muscle pain (the sarcopenia / myopathy context) does have an L1 and L2 lever, and "
      "both lower the crossing rate by direction on the MYOD1-grounded substrate. But there is no discrete "
      "structural contact-loss lesion to cross-check, so the coupled-versus-decoupled discriminant of &sect;27 "
      "cannot be run here.</p>"
      "<p>It is therefore graded as a DIRECTION-only result with no structural cross-check &mdash; logged, not "
      "dropped, exactly like the secondary entries elsewhere in this volume. L2 anchor: %s.</p>"
      "<h2>Routed out (single source of truth)</h2>"
      "<p>Neuropathic pain, fibromyalgia and central sensitisation syndromes are not musculoskeletal-mechanism "
      "diseases; they are routed to sibling volumes via the named seams, never re-emerged here. The analgesic axis "
      "stays strictly inside the load-bearing class: it treats the nociceptive drive that this volume&rsquo;s own "
      "mechanical diseases generate, and cites everything else.</p>"
      "<p>That boundary is the point. The contribution is to show that, for the diseases this volume owns, the "
      "inherited three-lever technique lands cleanly &mdash; L2 in scope and convergent, L1 in scope and "
      "decoupled, L3 and opioids honestly out.</p>"
      ) % (esc(ex.get("L2_agent")),)
    cards = [CARD_NOCICEPTION]
    oneliner = ("Honest limits: L3 central gain is owned by neuro/mind and cited as a seam (not re-emerged); the "
        "opioid descending/mu lever is outside the non-opioid logic; exertional muscle pain is DIRECTION-only with "
        "no structural cross-check; neuropathic pain and fibromyalgia are routed to sibling volumes (SSOT). The "
        "axis stays strictly inside the load-bearing class -- results stated as scope, not failures.")
    keywords = ["analgesia scope limits", "central sensitization neuro seam", "opioid descending modulation",
                "gabapentinoid duloxetine central gain", "neuropathic pain routing", "fibromyalgia out of scope",
                "single source of truth", "exertional muscle pain", "honest open grade", "musculoskeletal pain boundary"]
    return answer, abstract, body, cards, oneliner, keywords

# --------------------------------------------------------------------------- section registry
SECTIONS = [
    {"no": 1, "slug": "01-organ-emergence-measured-gamma",
     "subj": "Organ Emergence from Measured Gamma", "h1": "Organ Emergence from Measured Master-Gene Gamma",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_emergence},
    {"no": 2, "slug": "02-force-frequency-twitch-summation-fused",
     "subj": "Force-Frequency: Twitch Summation to Fused Tetanus",
     "h1": "Force-Frequency: Twitch Summation to Fused Tetanus",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t1},
    {"no": 3, "slug": "03-length-tension-filament-overlap",
     "subj": "Length-Tension from Filament Overlap", "h1": "Length-Tension as a Filament-Overlap Contact Number",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t2},
    {"no": 4, "slug": "04-wolff-remodelling-yield-threshold",
     "subj": "Wolff Remodelling as a Yield Threshold", "h1": "Wolff Remodelling as a Jamming Yield Threshold",
     "gclass": "forced", "glabel": "[F] forced", "build": sec_t3},
    {"no": 5, "slug": "05-growth-plate-ordering-gamma-rank",
     "subj": "Growth-Plate Ordering by Gamma Rank", "h1": "Growth-Plate Developmental Order from Gamma Rank",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t4},
    {"no": 6, "slug": "06-muscle-fatigue-reversible-decline",
     "subj": "Muscle Fatigue as Reversible Decline", "h1": "Muscle Fatigue as a Reversible Exponential Decline",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t5},
    {"no": 7, "slug": "07-carcinogen-dose-response-bone-soft",
     "subj": "Carcinogen Dose-Response in Bone and Soft Tissue",
     "h1": "Carcinogen Dose-Response: a Barrier-Lowering Kernel",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_onco},
    {"no": 8, "slug": "08-master-gene-dosage-dysplasias",
     "subj": "Master-Gene Dosage Dysplasias (CCD, Campomelic, Holt-Oram)",
     "h1": "Master-Gene Dosage Dysplasias as a Forced Crossing Cliff",
     "gclass": "forced", "glabel": "[F] forced threshold-shift", "build": sec_t7_master_dosage},
    {"no": 9, "slug": "09-mechanostat-disease-osteoporosis-osteopetrosis",
     "subj": "Mechanostat Disease: Osteoporosis and Osteopetrosis",
     "h1": "Mechanostat Disease: Osteoporosis and Osteopetrosis as the Mirror of Wolff's Law",
     "gclass": "forced", "glabel": "[F] forced", "build": sec_t6_mechanostat},
    {"no": 10, "slug": "10-neuromuscular-transmission-mg-lems",
     "subj": "Neuromuscular Transmission: Myasthenia and Lambert-Eaton",
     "h1": "Neuromuscular Transmission Failure: Myasthenia Gravis and Lambert-Eaton",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t8_nmj},
    {"no": 11, "slug": "11-metabolic-mitochondrial-myopathy",
     "subj": "Metabolic and Mitochondrial Myopathy",
     "h1": "Metabolic and Mitochondrial Myopathy as a Fatigue Perturbation",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t10_metabolic},
    {"no": 12, "slug": "12-osteoarthritis-cartilage-unjamming",
     "subj": "Osteoarthritis as Cartilage Unjamming",
     "h1": "Osteoarthritis as Cyclic-Fatigue Unjamming of the Cartilage Contact Network",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t9_oa},
    {"no": 13, "slug": "13-achondroplasia-growth-plate-suppression",
     "subj": "Achondroplasia as Growth-Plate Suppression",
     "h1": "Achondroplasia and Chondrodysplasias as Growth-Plate Switch Suppression",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t4ext_achondroplasia},
    {"no": 14, "slug": "14-muscular-dystrophy-and-sarcopenia",
     "subj": "Muscular Dystrophy and Sarcopenia",
     "h1": "Progressive Muscle Loss: Dystrophy (Contractile-Contact Fatigue) and Sarcopenia",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t11_t15_muscle_loss},
    {"no": 15, "slug": "15-muscle-channelopathies-myotonia-paralysis",
     "subj": "Muscle Channelopathies: Myotonia and Periodic Paralysis",
     "h1": "Muscle Channelopathies as Depolarization-Block-Threshold Shifts",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t12_channelopathy},
    {"no": 16, "slug": "16-stress-fracture-and-fracture-healing",
     "subj": "Stress Fracture and Fracture Healing",
     "h1": "Stress Fracture as Sub-Yield Bone Fatigue, and Fracture Healing as Remodeling Re-Cross",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t13_stress_fracture},
    {"no": 17, "slug": "17-tendinopathy-collagen-network-unjamming",
     "subj": "Tendinopathy as Collagen-Network Unjamming",
     "h1": "Tendinopathy as Cyclic-Fatigue Unjamming of the Tendon Collagen Network",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t14_tendinopathy},
    {"no": 18, "slug": "18-osteomalacia-rickets-mineralization-ceiling",
     "subj": "Osteomalacia and Rickets as a Mineralization Ceiling",
     "h1": "Osteomalacia and Rickets as a Mineralization Ceiling (Load Cannot Rescue)",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t16_osteomalacia},
    {"no": 19, "slug": "19-osteolytic-bone-disease-uncoupling",
     "subj": "Osteolytic Bone Disease as Osteoclast/Osteoblast Uncoupling",
     "h1": "Osteolytic Bone Disease (Myeloma, Giant-Cell Tumour) as Osteoclast/Osteoblast Uncoupling",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_t17_osteolytic},
    {"no": 20, "slug": "20-out-of-class-and-material-register",
     "subj": "Out-of-Class and Material Disease Register",
     "h1": "Out-of-Class and Material Diseases: Honest Open Grades and Seam Routing",
     "gclass": "open", "glabel": "[O] open / routed", "build": sec_out_of_class},
    {"no": 21, "slug": "21-treatment-axis-barrier-restoration",
     "subj": "Treatment Axis: Barrier Restoration",
     "h1": "The Treatment Axis: Disease Run in Reverse on a DNA-Grounded Switch (Barrier Restoration)",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_treatment_axis},
    {"no": 22, "slug": "22-treatment-bone-and-cartilage",
     "subj": "Bone and Cartilage Treatments",
     "h1": "Bone and Cartilage Treatments as Mirror Operations on the RUNX2/SOX9 Switch",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_treatment_bone},
    {"no": 23, "slug": "23-treatment-muscle-and-neuromuscular",
     "subj": "Muscle and Neuromuscular Treatments",
     "h1": "Muscle and Neuromuscular Treatments: Restoring Excitability and Contractile Knobs",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_treatment_muscle},
    {"no": 24, "slug": "24-treatment-honest-limits-and-scope",
     "subj": "Honest Treatment Limits and Scope",
     "h1": "Honest Treatment Limits: Where the Kernel Has No Restoration Knob (Results, Not Failures)",
     "gclass": "open", "glabel": "[O] open / scope", "build": sec_treatment_negatives},
    {"no": 25, "slug": "25-analgesic-three-lever-threshold-logic",
     "subj": "Analgesic Axis: Three-Lever Threshold Logic",
     "h1": "Non-Opioid Analgesia as a Threshold-Crossing Rate: The Inherited Three-Lever Technique",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_analgesic_axis},
    {"no": 26, "slug": "26-analgesic-l2-drive-load-bearing-convergence",
     "subj": "L2 on Load-Bearing Disease: Analgesia-Disease Convergence",
     "h1": "Lever L2 on the Load-Bearing Diseases: Where Analgesia and Disease-Modification Converge",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_analgesic_l2},
    {"no": 27, "slug": "27-analgesic-l1-threshold-coupled-decoupled-discriminant",
     "subj": "L1 and the Coupled/Decoupled Discriminant",
     "h1": "Lever L1 and the Falsifiable Coupled/Decoupled Discriminant (with Osteolytic Bone Pain)",
     "gclass": "verified", "glabel": "[V] verified", "build": sec_analgesic_l1_discriminant},
    {"no": 28, "slug": "28-analgesic-limits-and-central-gain-seam",
     "subj": "Analgesic Limits and the Central-Gain Seam",
     "h1": "Analgesic Limits and the Central-Gain Seam: What Is Routed Out and Why (Results, Not Failures)",
     "gclass": "open", "glabel": "[O] open / scope", "build": sec_analgesic_limits_seam},
]

# --------------------------------------------------------------------------- HTML rendering
def page_url(slug): return "%s/%s/%s/" % (DOMAIN, PAPER_ID, slug)

def desc_from(answer):
    t = re.sub("<[^>]+>", "", answer)
    rep = {"&nbsp;": " ", "&minus;": "-", "&mdash;": "-", "&ndash;": "-", "&gamma;": "gamma", "&micro;": "u",
           "&asymp;": "~", "&harr;": "<->", "&rarr;": "->", "&sup2;": "2", "&sup3;": "3", "&#8314;": "+",
           "&#8315;": "-", "&ne;": "!=", "&times;": "x", "&amp;": "&", "&lt;": "<", "&gt;": ">",
           "&frac23;": "2/3", "&#8532;": "2/3", "&epsilon;": "e", "&deg;": "deg", "&middot;": "*",
           "&frac12;": "1/2", "&lsquo;": "'", "&rsquo;": "'", "&le;": "<=", "&ge;": ">="}
    for k, vv in rep.items(): t = t.replace(k, vv)
    t = " ".join(t.split())
    if len(t) > 158: t = t[:158].rsplit(" ", 1)[0] + "..."
    return t

# --------------------------------------------------------------------------- analgesic cross-references
# Requirement: the inherited three-lever analgesic technique is applied to the EXISTING painful disease
# cases, not only stated in the new axis. Each owned painful disease chapter therefore carries a back-link
# to its lever classification in the analgesic axis (SSOT: the levers are emerged once in sec 25-28; here we
# only cross-reference, never re-derive). Keyed by section number -> (one-line classification HTML, [targets]).
ANLG_XREF = {
    12: ("Osteoarthritis is the primary L2-coupled case: the joint load that hurts is the load that erodes the "
         "cartilage, so the unloading (L2) analgesic move is the same operation that arrests the lesion, while a "
         "peripheral block (L1) relieves pain with the cartilage left unchanged.",
         [("26-analgesic-l2-drive-load-bearing-convergence", "&sect;26 L2 convergence"),
          ("27-analgesic-l1-threshold-coupled-decoupled-discriminant", "&sect;27 L1 coupled/decoupled discriminant")]),
    14: ("Exertional and overuse muscle pain carries an L1 and an L2 lever that both lower the crossing rate by "
         "DIRECTION, but there is no discrete contact-loss lesion to run the coupled/decoupled cross-check, so it is "
         "graded DIRECTION-only (honest partial).",
         [("28-analgesic-limits-and-central-gain-seam", "&sect;28 limits / honest partial")]),
    16: ("Stress-fracture pain is an L2-coupled case: offloading below the bone endurance limit lowers the nociceptive "
         "crossing rate and halts the microdamage at once, letting the documented healing re-cross proceed.",
         [("26-analgesic-l2-drive-load-bearing-convergence", "&sect;26 L2 convergence")]),
    17: ("Tendinopathy pain reuses the same cyclic-fatigue kernel, so the L2 (deload) lever lowers both the crossing "
         "rate and the tendon contact loss; the mirror disease-modifying step then ADDS eccentric loading, a separate "
         "up-step that is not analgesia.",
         [("26-analgesic-l2-drive-load-bearing-convergence", "&sect;26 L2 convergence")]),
    19: ("Osteolytic / myeloma bone pain is the clean resorptive-drive L2 case: the antiresorptive (denosumab / "
         "zoledronate) that relieves the RANKL drive is simultaneously the mirror treatment and the analgesic. Cancer "
         "bone pain is clinically opioid-first-line, and the opioid lever is honestly outside the non-opioid scope.",
         [("27-analgesic-l1-threshold-coupled-decoupled-discriminant", "&sect;27 osteolytic L2 detail")]),
}

def _analgesic_xref_block(sec_no):
    if sec_no not in ANLG_XREF:
        return ""
    note, targets = ANLG_XREF[sec_no]
    links = ", ".join('<a href="%s">%s</a>' % (page_url(slug), label) for slug, label in targets)
    return ("<h2>Analgesic lever map (cross-reference)</h2>"
            "<p>%s See <a href=\"%s\">&sect;25 the three-lever threshold logic</a> for the inherited technique "
            "(concept DOI <a href=\"%s\" rel=\"noopener\">10.5281/zenodo.20733420</a>), and %s for the worked lever "
            "sweeps. The analgesic axis adds no new physics: pain is a threshold-crossing rate on the same R19 "
            "barrier this chapter already uses.</p>"
            % (note, page_url("25-analgesic-three-lever-threshold-logic"), ANALGESIC_DOI_URL, links))

def render_chapter(sec, prev_sec, next_sec, N):
    built = sec["build"](N)
    answer, abstract, body, cards, oneliner = built[:5]
    body = body + _analgesic_xref_block(sec["no"])
    kw = built[5] if len(built) > 5 else None
    url = page_url(sec["slug"])
    title = "%s &mdash; %s &sect;%d | Jamming Physics" % (sec["subj"][:45], ABBR, sec["no"])
    # SEO: each section may carry its own knowsAbout keyword list (Google / AI-search entity surface);
    # falls back to the shared substrate keywords when a section does not specify one.
    knows = sec.get("keywords") or kw or ["jamming lattice", "R19 bistable switch", "load-bearing contact number",
                                          "Wolff's law", "force-frequency", "master-gene gamma"]
    ld_article = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": sec["subj"],
        "isPartOf": {"@type": "CreativeWorkSeries", "name": TITLE, "url": "%s/%s/" % (DOMAIN, PAPER_ID)},
        "position": sec["no"], "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "license": LICENSE, "datePublished": DATE, "dateModified": DATE, "isBasedOn": REPRO,
        "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": CONCEPT_DOI}, "sameAs": DOI_URL,
        "knowsAbout": knows}
    ld_crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": ABBR, "item": "%s/%s/" % (DOMAIN, PAPER_ID)},
        {"@type": "ListItem", "position": 3, "name": "\u00a7%d %s" % (sec["no"], sec["subj"])}]}
    claim_strip = ('<aside class="claim-strip"><span class="grade g-%s">%s</span>'
        '<span class="gate">LOCK &rarr; Derive &rarr; Gate</span>'
        '<a href="%s" rel="noopener">reproduction code (GitHub)</a>'
        '<a class="doi" href="%s" rel="noopener">%s</a></aside>' % (sec["gclass"], esc(sec["glabel"]), esc(REPRO), esc(DOI_URL), esc(DOI_NOTE)))
    pn = '<nav class="pn">'
    pn += ('<a rel="prev" href="%s">&larr; &sect;%d %s</a>' % (page_url(prev_sec["slug"]), prev_sec["no"], esc(prev_sec["subj"]))) if prev_sec else '<span></span>'
    pn += '<a href="%s/%s/">contents</a>' % (DOMAIN, PAPER_ID)
    pn += ('<a rel="next" href="%s">&sect;%d %s &rarr;</a>' % (page_url(next_sec["slug"]), next_sec["no"], esc(next_sec["subj"]))) if next_sec else '<span></span>'
    pn += '</nav>'
    o = []
    o.append('<!DOCTYPE html>\n<html lang="en">\n<head>')
    o.append('<meta charset="utf-8">')
    o.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    o.append('<title>%s</title>' % title)
    o.append('<meta name="description" content="%s">' % esc(desc_from(answer)))
    o.append('<link rel="canonical" href="%s">' % esc(url))
    o.append('<link rel="stylesheet" href="/assets/css/site.css">')
    o.append('<script type="application/ld+json">\n%s\n</script>' % json.dumps(ld_article, ensure_ascii=False, indent=1))
    o.append('<script type="application/ld+json">\n%s\n</script>' % json.dumps(ld_crumb, ensure_ascii=False, indent=1))
    o.append('</head>\n<body>')
    o.append('<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="/%s/">%s</a> &rsaquo; &sect;%d</nav></header>' % (PAPER_ID, esc(ABBR), sec["no"]))
    o.append('<main>')
    o.append('<h1>%s</h1>' % sec["h1"])
    o.append('<p class="answer">%s</p>' % answer)
    o.append('<p class="abstract">%s</p>' % abstract)
    o.append(claim_strip)
    for c in cards: o.append(c)
    o.append(body)
    o.append(pn)
    o.append('</main>')
    o.append('<footer>%s &middot; <a href="%s" rel="noopener author">ORCID 0009-0002-7535-8245</a> &middot; '
             '<a href="%s" rel="license noopener">CC BY 4.0</a> &middot; <a href="%s" rel="noopener">%s</a></footer>'
             % (esc(AUTHOR), esc(ORCID), esc(LICENSE), esc(DOI_URL), esc(DOI_NOTE)))
    o.append('</body>\n</html>')
    return "\n".join(o), oneliner

def render_hub(N, oneliners):
    url = "%s/%s/" % (DOMAIN, PAPER_ID); g = N["gammas"]
    ld = {"@context": "https://schema.org", "@type": "CreativeWorkSeries", "name": TITLE, "url": url,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID}, "license": LICENSE,
        "datePublished": DATE, "dateModified": DATE,
        "hasPart": [{"@type": "ScholarlyArticle", "headline": s["subj"], "position": s["no"],
                     "url": page_url(s["slug"])} for s in SECTIONS]}
    items = "".join('<li><a href="%s"><b>&sect;%d %s</b></a> <span class="grade g-%s">%s</span><br>'
        '<span class="ol">%s</span></li>'
        % (page_url(s["slug"]), s["no"], esc(s["subj"]), s["gclass"], esc(s["glabel"]), oneliners[s["slug"]])
        for s in SECTIONS)
    o = []
    o.append('<!DOCTYPE html>\n<html lang="en">\n<head>')
    o.append('<meta charset="utf-8">')
    o.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    o.append('<title>%s | Jamming Physics</title>' % esc(ABBR))
    o.append('<meta name="description" content="%s">' % esc("Muscle, cartilage and bone emerge from one "
        "measured master-gene number on the jamming substrate; bone remodelling is a yield threshold. Five "
        "physiology tests plus a 16-target disease battery (dysplasias, osteoporosis, myasthenia, OA, dystrophy, channelopathies, stress fracture, tendinopathy, sarcopenia) pass; honest grades."))
    o.append('<link rel="canonical" href="%s">' % esc(url))
    o.append('<link rel="stylesheet" href="/assets/css/site.css">')
    o.append('<script type="application/ld+json">\n%s\n</script>' % json.dumps(ld, ensure_ascii=False, indent=1))
    o.append('</head>\n<body>')
    o.append('<header><nav class="crumb"><a href="/">Home</a> &rsaquo; %s</nav></header>' % esc(ABBR))
    o.append('<main>')
    o.append('<h1>%s</h1>' % esc(TITLE))
    o.append('<p class="answer">Skeletal muscle, cartilage, limb skeleton and bone emerge deterministically '
        'from one read-only master-gene number &gamma; on the jamming substrate. Muscle actuation '
        '(force-frequency, length-tension, fatigue), Wolff bone remodelling as a yield threshold, and '
        '&gamma;-ranked growth-plate order all reproduce cited signatures; a carcinogen is a barrier-lowering '
        'drive. Five physiology tests and an 18-target battery of cited-severity disease perturbations all pass.</p>')
    o.append('<p class="abstract">The four measured &gamma; order as RUNX2 %.4f &lt; TBX5 %.4f &lt; SOX9 %.4f '
        '&lt; MYOD1 %.4f. The disease pages are PERTURBATIONS of the passing physiology &mdash; haploinsufficiency '
        'dysplasias (a forced crossing cliff), disuse osteoporosis (the mirror of Wolff), myasthenia / '
        'Lambert-Eaton, metabolic myopathy, osteoarthritis as cartilage unjamming and achondroplasia &mdash; '
        'muscular dystrophy (reading-frame severity), muscle channelopathies (myotonia/periodic paralysis), stress '
        'fracture with fracture healing, tendinopathy, sarcopenia, osteomalacia/rickets (a mineralization ceiling) and '
        'osteolytic bone disease (myeloma/giant-cell tumour) &mdash; each with a CITED severity and honest '
        'grade. Every quantity below is regenerated deterministically '
        '(2&times;sha256 identical) with a reproduction path.'
        % (g["bone"], g["limb_skeleton"], g["cartilage"], g["skeletal_muscle"]))
    o.append('<aside class="claim-strip"><span class="grade g-verified">[V] research signed off</span>'
        '<span class="gate">LOCK &rarr; Derive &rarr; Gate</span>'
        '<a href="%s" rel="noopener">reproduction code (GitHub)</a>'
        '<a class="doi" href="%s" rel="noopener">%s</a></aside>' % (esc(REPRO), esc(DOI_URL), esc(DOI_NOTE)))
    o.append('<h2>Sections</h2><ol class="toc">%s</ol>' % items)
    o.append('<h2>Provenance &amp; seams</h2><p>Organ identity and developmental order are inherited from the '
        '<a href="%s" rel="noopener">4D DNA Blueprint</a> volume (measured &gamma;); the R19 bistable switch '
        'and the jamming lattice are inherited from <a href="%s" rel="noopener">VP Theory</a>; the motor '
        'command is owned by the <a href="%s" rel="noopener">Neural Emergence Chain</a>. This volume is the '
        'single source only for the load-bearing dynamics and the carcinogen dose-response.</p>'
        % (DNA_HUB, PHY_HUB, NEU_HUB))
    o.append('</main>')
    o.append('<footer>%s &middot; <a href="%s" rel="noopener author">ORCID 0009-0002-7535-8245</a> &middot; '
        '<a href="%s" rel="license noopener">CC BY 4.0</a> &middot; <a href="%s" rel="noopener">%s</a></footer>'
        % (esc(AUTHOR), esc(ORCID), esc(LICENSE), esc(DOI_URL), esc(DOI_NOTE)))
    o.append('</body>\n</html>')
    return "\n".join(o)

def render_top_index():
    url = DOMAIN + "/"
    o = []
    o.append('<!DOCTYPE html>\n<html lang="en">\n<head>')
    o.append('<meta charset="utf-8">')
    o.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    o.append('<title>Jamming Physics &mdash; the vacuum as a jammed solid</title>')
    o.append('<meta name="description" content="A program deriving physics, biology and disease from a jammed '
        'granular vacuum. This node: musculoskeletal emergence on the load-bearing substrate.">')
    o.append('<link rel="canonical" href="%s">' % esc(url))
    o.append('<link rel="stylesheet" href="/assets/css/site.css">')
    o.append('</head>\n<body>')
    o.append('<main>')
    o.append('<h1>Jamming Physics</h1>')
    o.append('<p class="answer">Jamming Physics models the vacuum as a jammed granular medium and derives '
        'physics, cosmology, fluids, geodynamics, biology and disease from one substrate. This node hosts the '
        'musculoskeletal volume: muscle, cartilage and bone as load-bearing jammed matter.</p>')
    o.append('<h2>Volume on this node</h2><ul class="toc"><li><a href="/%s/"><b>%s</b></a><br>'
        '<span class="ol">Muscle actuation, cartilage and bone as load-bearing jammed matter; Wolff '
        'remodelling as a yield threshold.</span></li></ul>' % (PAPER_ID, esc(ABBR)))
    o.append('<p>Sibling volumes (VP&nbsp;Theory, 4D&nbsp;DNA&nbsp;Blueprint, Neural&nbsp;Emergence&nbsp;Chain '
        'and others) live across the <a href="%s" rel="noopener">jamming-physics</a> program.</p>' % esc(REPO))
    o.append('</main>')
    o.append('<footer>%s &middot; <a href="%s" rel="license noopener">CC BY 4.0</a></footer>'
        % (esc(AUTHOR), esc(LICENSE)))
    o.append('</body>\n</html>')
    return "\n".join(o)

def render_meta(N, oneliners):
    g = N["gammas"]
    return {"paper_id": PAPER_ID, "code": CODE, "title": TITLE, "abbr": ABBR, "author": AUTHOR, "orcid": ORCID,
        "license": LICENSE, "doi": CONCEPT_DOI, "doi_url": DOI_URL, "doi_status": "concept DOI (all versions)",
        "inherited_analgesic_technique_doi": ANALGESIC_DOI,
        "canonical": "%s/%s/" % (DOMAIN, PAPER_ID), "repro": REPRO,
        "branch": "jamming (solid-mechanics / load-bearing)", "generated": DATE,
        "measured_gamma": {o: round(g[o], 6) for o in sorted(g)},
        "gamma_order_ascending": N["em"]["gamma_order_ascending"],
        "discriminant_targets_all_pass": all(N["suites"][t]["status"] == "PASS" for t in N["suites"]),
        "disease_targets_all_pass": N["dis"]["all_disease_targets_pass"],
        "disease_targets": [{"target": s["target"], "disease": s["disease"], "perturbs": s["perturbs"],
                             "secondary": s.get("secondary", False), "status": s["status"], "grade": s["grade"]}
                            for s in N["dis"]["suites"]],
        "oncology_shape_ok": N["onc"]["all_sites_shape_ok"],
        "oncology_sites": [s["site"] for s in N["onc"]["sites"]],
        "chapters": [{"no": s["no"], "slug": s["slug"], "title": s["subj"], "h1": s["h1"], "grade": s["glabel"],
                      "url": page_url(s["slug"]), "one_liner": re.sub("<[^>]+>", "", oneliners[s["slug"]])}
                     for s in SECTIONS]}

def render_sitemap():
    urls = [DOMAIN + "/", "%s/%s/" % (DOMAIN, PAPER_ID)] + [page_url(s["slug"]) for s in SECTIONS]
    body = "".join('<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (esc(u), DATE) for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % body)

def render_robots():
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    lines = ["User-agent: %s\nAllow: /\n" % b for b in bots]
    lines.append("User-agent: *\nAllow: /\n")
    lines.append("\nSitemap: %s/sitemap.xml\n" % DOMAIN)
    return "\n".join(lines)

def render_llms(N, oneliners):
    g = N["gammas"]; L = []
    L.append("# %s" % TITLE); L.append("")
    L.append("> Skeletal muscle, cartilage, limb skeleton and bone emerge deterministically from one")
    L.append("> read-only master-gene number gamma on a jammed-solid vacuum substrate. Muscle actuation,")
    L.append("> Wolff bone remodelling as a yield threshold, gamma-ranked growth-plate order and a")
    L.append("> barrier-lowering carcinogen kernel reproduce cited signatures. A DISEASE BATTERY then")
    L.append("> perturbs that passing machinery with CITED severities: haploinsufficiency dysplasias")
    L.append("> (a forced crossing cliff), disuse osteoporosis (the mirror of Wolff), myasthenia and")
    L.append("> Lambert-Eaton, metabolic myopathy, osteoarthritis, achondroplasia, muscular dystrophy")
    L.append("> (reading-frame severity), muscle channelopathies (myotonia/periodic paralysis), stress")
    L.append("> fracture with fracture healing, tendinopathy, sarcopenia, osteomalacia/rickets")
    L.append("> (mineralization ceiling) and osteolytic bone disease (myeloma/giant-cell tumour).")
    L.append("> Every number is regenerated deterministically (2x sha256 identical); each claim carries an")
    L.append("> honest grade [F]forced / [V]verified / [L]cited-anchor / [O]open, with an obstacle for every [O].")
    L.append("")
    L.append("Author: %s (ORCID 0009-0002-7535-8245). License: CC BY 4.0. Reproduction: %s" % (AUTHOR, REPRO))
    L.append("Measured gamma (never fitted): RUNX2=%.4f < TBX5=%.4f < SOX9=%.4f < MYOD1=%.4f"
        % (g["bone"], g["limb_skeleton"], g["cartilage"], g["skeletal_muscle"]))
    L.append(""); L.append("## Core sections (physiology, oncology, disease battery)")
    for s in SECTIONS:
        ol = re.sub("<[^>]+>", "", oneliners[s["slug"]])
        for k, vv in {"&nbsp;": " ", "&gamma;": "gamma", "&rarr;": "->", "&micro;": "u", "&asymp;": "~",
                      "&minus;": "-", "&ndash;": "-", "&amp;": "&", "&lt;": "<", "&gt;": ">",
                      "&frac23;": "2/3", "&#8532;": "2/3", "&times;": "x", "&epsilon;": "e", "&harr;": "<->"}.items():
            ol = ol.replace(k, vv)
        ol = " ".join(ol.split())
        L.append("- [%s %s](%s): %s" % ("\u00a7%d" % s["no"], s["subj"], page_url(s["slug"]), ol))
    L.append(""); L.append("## Policies")
    L.append("- No-Tuning: coefficients are never migrated to close residuals; disease severities are CITED")
    L.append("  (haploinsufficiency = 0.5 dosage; Frost MES; RNS >10% threshold; Paris/Basquin damage-law form).")
    L.append("- Disease PASS = reproduce the DIRECTION/SHAPE of the clinical sign, never an absolute number.")
    L.append("- SSOT: derivations live once; gamma is imported from the 4D DNA Blueprint volume; out-of-class")
    L.append("  diseases (autoimmune, crystal, pain, infection, distant primary) are routed to siblings via seams.")
    L.append("- Honest negatives: ossification timing, absolute incidence, absolute BMD, long-bone length and")
    L.append("  material strength are graded [O] with obstacles.")
    return "\n".join(L) + "\n"

SITE_CSS = """:root{--ink:#15171a;--mut:#5b6470;--line:#e3e6ea;--bg:#fff;--acc:#1f6feb;--card:#f6f8fa;
--f:#0a7d33;--v:#1f6feb;--h:#8a5a00;--o:#9445c9}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;color:var(--ink);background:var(--bg);font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
header,main,footer{max-width:760px;margin:0 auto;padding:0 20px}
header{padding-top:18px}main{padding-bottom:40px}
.crumb{color:var(--mut);font-size:14px}.crumb a{color:var(--mut);text-decoration:none}.crumb a:hover{color:var(--acc)}
h1{font-size:30px;line-height:1.22;margin:.5em 0 .35em;letter-spacing:-.01em}
h2{font-size:20px;margin:1.7em 0 .5em;letter-spacing:-.005em}h3{font-size:17px;margin:1.3em 0 .4em}
p{margin:.7em 0}a{color:var(--acc)}
.answer{font-size:19px;line-height:1.5;font-weight:500;margin:.6em 0 .8em}
.abstract{color:#2b3036;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.claim-strip{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0;font-size:13.5px}
.claim-strip>*{border:1px solid var(--line);border-radius:999px;padding:4px 11px;background:#fff;text-decoration:none}
.grade{font-weight:700;border:none!important;color:#fff!important}
.g-forced{background:var(--f)}.g-verified{background:var(--v)}.g-hypothesis{background:var(--h)}.g-open{background:var(--o)}
.gate{color:var(--mut)}.doi{color:var(--mut)}
.vp-card{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;padding:10px 13px;margin:10px 0;font-size:14.5px}
.vp-card b:first-child{font-variant-numeric:tabular-nums}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:14.5px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left}th{background:var(--card)}
td{font-variant-numeric:tabular-nums}
.pn{display:flex;justify-content:space-between;gap:12px;margin:2em 0 0;padding-top:14px;border-top:1px solid var(--line);font-size:14px}
.pn a{text-decoration:none}.pn span{flex:1}
.toc{list-style:none;padding:0}.toc li{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:9px 0}
.toc a{text-decoration:none}.toc .grade{display:inline-block;margin-left:6px;font-size:12px;padding:2px 8px}
.ol{color:var(--mut);font-size:14px}
footer{color:var(--mut);font-size:13px;border-top:1px solid var(--line);padding-top:16px;padding-bottom:40px;margin-top:10px}
footer a{color:var(--mut)}
@media(max-width:480px){h1{font-size:25px}.answer{font-size:17px}}
"""

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def update_manifest(N, oneliners):
    import csv
    p = os.path.join(_PKG, "manifest", PAPER_ID + ".csv")
    rows = [["slug", "title", "section_no", "status", "grade", "words", "eq_display"]]
    for s in SECTIONS:
        body = s["build"](N)[2]
        words = len(re.sub("<[^>]+>", " ", body).split())
        rows.append([s["slug"], s["subj"], s["no"], "PASS", s["glabel"], words, 0])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Do the research first: fetch to_measure gamma, build the dynamics, pass the stress battery, then")
        print("  python repro/_verify/gates.py  ->  gates.write_research_complete()  ;  echo writing > PHASE")
        print("and re-run. (VP-SPEC: research-first; HTML is the canonical artifact.)")
        return 1

    N = load_numbers()
    docs = os.path.join(_PKG, "docs")
    oneliners = {}

    # chapter pages
    for i, sec in enumerate(SECTIONS):
        prev_sec = SECTIONS[i - 1] if i > 0 else None
        next_sec = SECTIONS[i + 1] if i < len(SECTIONS) - 1 else None
        page_html, oneliner = render_chapter(sec, prev_sec, next_sec, N)
        oneliners[sec["slug"]] = oneliner
        write(os.path.join(docs, PAPER_ID, sec["slug"], "index.html"), page_html)

    # hub, top index, meta, sitemap, robots, llms, css
    write(os.path.join(docs, PAPER_ID, "index.html"), render_hub(N, oneliners))
    write(os.path.join(docs, "index.html"), render_top_index())
    write(os.path.join(docs, PAPER_ID, "_meta.json"),
          json.dumps(render_meta(N, oneliners), ensure_ascii=False, indent=2))
    write(os.path.join(docs, "sitemap.xml"), render_sitemap())
    write(os.path.join(docs, "robots.txt"), render_robots())
    write(os.path.join(docs, "llms.txt"), render_llms(N, oneliners))
    write(os.path.join(docs, "assets", "css", "site.css"), SITE_CSS)
    update_manifest(N, oneliners)

    pages = len(SECTIONS) + 2
    print("UNLOCKED -> wrote %d HTML pages + sitemap/robots/llms/css/_meta + manifest into docs/." % pages)
    print("  canonical hub: %s/%s/" % (DOMAIN, PAPER_ID))
    for s in SECTIONS:
        print("   §%d  %-46s [%s]  %s" % (s["no"], s["slug"], s["glabel"], "docs/%s/%s/index.html" % (PAPER_ID, s["slug"])))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
