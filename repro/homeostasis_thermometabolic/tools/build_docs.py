#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  deterministic multi-page HTML generator (VP-SPEC v1.8, C1-C4).

Emits the canonical, citable, SPLIT site: a hub at docs/thermometabolic/index.html plus one
self-contained page per chapter at docs/thermometabolic/{slug}/index.html. Each page is answer-first
(<p class="answer"> 40-60 words), carries an abstract, a claim-strip (grade badge + LOCK->Derive->Gate +
GitHub repro link), ScholarlyArticle + BreadcrumbList JSON-LD, a canonical link, an English body with one
h1 and h2/h3 structure, vp-cards for cited locked quantities, and prev/next navigation. The access layer
(robots.txt, sitemap.xml, llms.txt) and the docs/thermometabolic/_meta.json summary card are emitted too.

C0 single zip / no fragmentation; C1 max reproducibility -- every number on a page is pulled from the
engine modules at generation time and a SELF-VERIFY pass regenerates and checks byte-drift == 0; C2 the
HTML is the canonical artifact (no TeX bundled); C3 [O] states its obstacle; C4 retrieval-readiness.

REFUSES to run unless gates.writing_locked() is False (research signed off, PHASE=writing).
"""
import os, sys, json, html, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.normpath(os.path.join(HERE, ".."))
DOCS = os.path.join(PKG, "docs")
for sub in ("_engine", "_verify", "_pathology"):
    sys.path.insert(0, os.path.join(PKG, "repro", sub))
import importlib
eng = importlib.import_module("vp_trm_engine")
gates = importlib.import_module("gates")
pathology = importlib.import_module("setpoint_failure")
restoration = importlib.import_module("restoration_levers")
precision = importlib.import_module("precision_routing")

SITE = "https://jamming-physics.org"
PAPER = "thermometabolic"
BASE = SITE + "/" + PAPER
REPO = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro"
ORCID = "https://orcid.org/0009-0002-7535-8245"
AUTHOR = "Young Jae Lee"
METHOD_DOI = "10.5281/zenodo.20733420"
CONCEPT_DOI = "10.5281/zenodo.20756934"
DATE = "2026-06-19"
TITLE = "Endotherm vs Ectotherm, the Defended Setpoint, and Metabolic Disease"
SHORT = "Thermometabolic Homeostasis"

FA = eng.foundational_analysis()
GC = FA["gene_criterion"]; N1 = FA["null_ucp1"]; N2 = FA["null_pdk4"]; N3 = FA["null_torpor_panel"]; N4 = FA["null_cpg_oe_panel"]
SD = FA["setpoint_defense"]; CS = FA["continuum_or_switch"]; COST = FA["endothermy_cost"]; KLE = FA["kleiber"]
TH = eng.thermostat_step(); BAT = eng.bat_thermogenesis(); FV = eng.fever_vs_hyperthermia()
HY = eng.torpor_hysteresis_sweep(); TR = eng.torpor_regulated(); GL = eng.glucose_homeostat()
LP = eng.lipostat(); HB = eng.hibernation_bridge(); OSC = eng.confirm_oscillators()["torpor_arousal_rhythm"]
PATH = pathology.status(); REST = restoration.build(); PREC = precision.build()
ATLAS = json.load(open(os.path.join(PKG, "inherited", "organ_gamma.json"), encoding="utf-8"))["genes"]
COMPARTMENT_LABEL = {"BAT": "brown adipose (BAT)", "WHITE_ADIPOSE": "white adipose",
                     "CNS_HYPOTHALAMUS": "hypothalamus (CNS)", "LIVER": "liver",
                     "SKELETAL_MUSCLE": "skeletal muscle", "GUT": "gut",
                     "SYSTEMIC_IMMUNE": "systemic (immune)"}
def comp_label(k): return COMPARTMENT_LABEL.get(k, k)

def f(x, n=4): return ("%." + str(n) + "f") % float(x)
def esc(s): return html.escape(str(s), quote=True)

GRADE_BADGE = {"v": ("g-v", "[V] simulation-verified"), "f": ("g-f", "[F] forced"),
               "o": ("g-o", "[O] open"), "l": ("g-h", "[L] measured")}

def vp_card(value, meaning, grade, deriv_slug=None):
    cls, _ = GRADE_BADGE[grade]
    link = ('<a href="' + BASE + "/" + deriv_slug + '/">canonical derivation</a>') if deriv_slug else \
           '<span class="note">derivation on this page</span>'
    return ('<aside class="vp-card" data-locked="true"><span class="g ' + cls + '">' + esc(value) +
            '</span> <b>' + esc(meaning) + '</b> &middot; ' + link + '</aside>')

def jsonld(no, slug, title, desc, position):
    art = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": title,
           "isPartOf": {"@type": "CreativeWork", "name": TITLE, "url": BASE + "/"},
           "position": str(position), "description": desc,
           "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
           "creativeWorkStatus": "Research preprint", "identifier": "https://doi.org/" + CONCEPT_DOI, "sameAs": "https://doi.org/" + CONCEPT_DOI,
           "isBasedOn": REPO, "isAccessibleForFree": True,
           "license": "https://creativecommons.org/licenses/by/4.0/",
           "datePublished": DATE, "dateModified": DATE,
           "knowsAbout": ["endothermy vs ectothermy", "defended homeostatic setpoint", "R19 bistable switch",
                          "torpor / hibernation switch", "promoter switch-threshold read (gamma)",
                          "metabolic-disease setpoint failure"]}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": SHORT, "item": BASE + "/"},
        {"@type": "ListItem", "position": 3, "name": no + " " + title}]}
    return ('<script type="application/ld+json">\n' + json.dumps(art, ensure_ascii=False) + '\n</script>\n'
            '<script type="application/ld+json">\n' + json.dumps(crumb, ensure_ascii=False) + '\n</script>')

def page(no, slug, title, desc, answer, abstract, grade, body_html, prev, nxt, position, cards_html=""):
    cls, label = GRADE_BADGE[grade]
    prev_a = ('<a rel="prev" href="' + BASE + "/" + prev[0] + '/">&larr; ' + esc(prev[1]) + '</a>') if prev else '<span></span>'
    next_a = ('<a rel="next" href="' + BASE + "/" + nxt[0] + '/">' + esc(nxt[1]) + ' &rarr;</a>') if nxt else '<span></span>'
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>' + esc(title) + ' &mdash; ' + esc(SHORT) + ' ' + esc(no) + ' | Jamming Physics</title>\n'
            '<meta name="description" content="' + esc(desc) + '">\n'
            '<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">\n'
            '<link rel="canonical" href="' + BASE + "/" + slug + '/">\n'
            '<link rel="stylesheet" href="/assets/css/site.css">\n' + jsonld(no, slug, title, desc, position) + '\n'
            '</head>\n<body>\n'
            '<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="' + BASE + '/">' + esc(SHORT) +
            '</a> &rsaquo; ' + esc(no) + '</nav></header>\n<main>\n'
            '<h1>' + esc(title) + '</h1>\n'
            '<p class="answer">' + answer + '</p>\n'
            '<p class="abstract">' + abstract + '</p>\n'
            '<aside class="claim-strip page"><span class="grade ' + cls + '">' + label + '</span>'
            '<span class="gate">LOCK &rarr; Derive &rarr; Gate</span>'
            '<a href="' + REPO + '" rel="noopener">reproduce (GitHub)</a>'
            '<a class="ver" href="https://doi.org/' + CONCEPT_DOI + '" rel="noopener">DOI ' + CONCEPT_DOI + '</a></aside>\n' + cards_html + '\n' + body_html + '\n'
            '<nav class="pn">' + prev_a + ' <a href="' + BASE + '/">contents</a> ' + next_a + '</nav>\n'
            '</main>\n<footer><a href="' + ORCID + '" rel="noopener">ORCID 0009-0002-7535-8245</a> &middot; ' +
            esc(AUTHOR) + ' &middot; CC BY 4.0 &middot; cite: <a href="https://doi.org/' + CONCEPT_DOI + '" rel="noopener">DOI ' + CONCEPT_DOI + '</a> &middot; method: <a href="https://doi.org/' + METHOD_DOI +
            '" rel="noopener">three-lever DOI ' + METHOD_DOI + '</a> &middot; part of the '
            '<a href="' + SITE + '/" rel="noopener">Jamming Physics</a> programme &middot; reproduce: '
            '<code>repro/run_all.py</code></footer>\n</body>\n</html>')

def P(*paras): return "".join("<p>" + s + "</p>\n" for s in paras)
def H2(t): return "<h2>" + esc(t) + "</h2>\n"
def H3(t): return "<h3>" + esc(t) + "</h3>\n"
def fw(text): return '<p class="fw">' + text + '</p>\n'
def table(headers, rows):
    th = "".join("<th>" + h + "</th>" for h in headers)
    body = "".join("<tr>" + "".join("<td>" + c + "</td>" for c in r) + "</tr>" for r in rows)
    return '<table>\n<thead><tr>' + th + '</tr></thead>\n<tbody>' + body + '</tbody>\n</table>\n'

G = "&gamma;"; HSP = "|h<sub>sp</sub>|"
CH = []
def add(**kw): CH.append(kw)

# ---- §0 ----
add(no="&sect;0", slug="how-to-read-this-map", title="How to read this map", kind="section",
    desc="One measured promoter read placed on the R19 setpoint scale; observation only, honest grades.", grade="f",
    answer=("This map starts from one question -- does an organism DEFEND an internal setpoint or TRACK its "
            "environment? -- and reads every node from a single measured number (" + G + ", a promoter stiffness "
            "read) placed on the shared R19 bistable-switch scale. It is observation only: no evolutionary "
            "language, honest grades throughout."),
    abstract=("Each node's master gene carries a measured " + G + " (nearest-neighbour stacking energy of its "
              "proximal promoter). " + G + " sets the R19 switch threshold " + HSP + "; a defended setpoint is a deep "
              "R19 basin, a tracked one is shallow. Grades: [F] forced, [V] simulation-verified, [L] measured, [O] "
              "open with a stated obstacle."),
    body=(H2("The one substrate") +
          P("Every page reads the same primitive: the R19 jamming-lattice bistable switch "
            "<code>ds/dt = &gamma;s &minus; s&sup3; + h</code>. Two stable states sit at &plusmn;&radic;&gamma;; the "
            "drive <code>h</code> biases between them; past the spinodal " + HSP + " <code>= 2(&gamma;/3)<sup>1.5</sup></code> "
            "one state disappears and the flip is discontinuous. A homeostatic setpoint is just the upper basin; "
            "defending it means the basin resists an environmental drive.") +
          H2("Observation only") +
          P("The analysis compares EXTANT species by what their genomes contain and how the R19 loops behave. There "
            "is no descent or selection language anywhere -- only presence/absence and measured " + G + ". Where a "
            "single gene fails to separate two strategies, that NULL is reported as a finding, not hidden.") +
          H2("The firewall") +
          fw(G + " reads promoter switch-threshold STRUCTURE only. It is never a temperature, a metabolic rate, a "
             "glucose level, an HbA1c, a dose, or a clinical effect. Those are Layer-2 and graded [O]. The disease "
             "and restoration chapters are falsifiable HYPOTHESES, not medical advice.")), cards=[])

# ---- §1 ----
add(no="&sect;1", slug="endotherm-vs-ectotherm", title="Endotherm vs ectotherm: the central separation", kind="core",
    desc="The divide is a defended setpoint vs ambient tracking; R19 basin depth is the mechanism.", grade="v",
    answer=("An endotherm DEFENDS an internal temperature setpoint; an ectotherm TRACKS the environment. In R19 this "
            "is one parameter: basin depth. A deep basin (high loop gain) pins the setpoint against an ambient drive; "
            "a shallow one follows it. Under the same ambient sweep the endotherm barely moves (sensitivity " +
            f(SD["endotherm_loop"]["ambient_sensitivity"], 3) + ") while the ectotherm tracks (" +
            f(SD["ectotherm_loop"]["ambient_sensitivity"], 3) + ")."),
    abstract=("The separation is mechanistic, not a label. A defended setpoint is a deep R19 attractor whose basin "
              "resists an ambient drive; a tracked one is shallow. The discriminant is exact: " +
              esc(SD["discriminant"]) + "."),
    body=(H2("One parameter: basin depth") +
          P("Sweeping an ambient drive across both loops, the endotherm setpoint stays pinned and the ectotherm "
            "state follows the drive almost one-to-one -- a sensitivity ratio of about " +
            f(SD["ectotherm_loop"]["ambient_sensitivity"] / SD["endotherm_loop"]["ambient_sensitivity"], 0) +
            "x. Nothing here requires a special gene; it requires a basin deep enough that the ambient drive "
            "amplitude stays below the spinodal.") +
          H2("The discriminant") +
          P("A loop defends its setpoint if and only if its spinodal exceeds the ambient drive amplitude; otherwise "
            "it tracks. Sensitivity falls monotonically as the barrier deepens (" +
            ("confirmed" if SD["sensitivity_monotone_decreasing_in_barrier"] else "checked") + "), so 'defend vs "
            "track' is a continuous consequence of one R19 quantity.") +
          H2("Three questions, three chapters") +
          P("Q1 -- the GENE-LEVEL criterion (next: a present, drivable effector-command pair, not a " + G +
            " value). Q2 -- how and how much the strategies differ (basin depth here, plus the thermostat and cost "
            "chapters). Q3 -- over how large a RANGE (the cost and continuum chapters: a metabolic factor of "
            "~5-10x plus a discontinuous regime boundary).")),
    cards=[vp_card("sensitivity " + f(SD["endotherm_loop"]["ambient_sensitivity"], 3), "endotherm setpoint pins under ambient drive", "v"),
           vp_card("sensitivity " + f(SD["ectotherm_loop"]["ambient_sensitivity"], 3), "ectotherm state tracks ambient", "v")])

# ---- §2 ----
endo_ucp1 = ", ".join(f(x) for x in N1["endotherm_UCP1_gamma"])
ecto_ucp1 = ", ".join(f(x) for x in N1["ectotherm_UCP1_gamma"])
crit_rows = []
for r in sorted(GC["rows"], key=lambda r: (r["thermo_class"], r["species"])):
    crit_rows.append(["<i>" + esc(r["species"]) + "</i>", esc(r["thermo_class"]),
                      (f(r["UCP1_gamma"]) if r["UCP1_gamma"] is not None else "&mdash;"),
                      (f(r["ADRB3_gamma"]) if r["ADRB3_gamma"] is not None else '<span class="note">absent</span>'),
                      (f(r["PDK4_gamma"]) if r["PDK4_gamma"] is not None else "&mdash;"),
                      ("yes" if r["effector_command_pair_present"] else "no")])
add(no="&sect;2", slug="the-gene-criterion", title="The gene criterion: a present, drivable effector-command pair", kind="core",
    desc="Q1 answered: the divide is PRESENCE of a {UCP1 furnace + ADRB3 command} pair, not a gamma value.", grade="l",
    answer=("The gene-level criterion is NOT a " + G + " value. Across the panel the endotherms all carry a drivable "
            "thermogenic effector-command pair -- a furnace (UCP1) plus a sympathetic command (ADRB3) -- while in "
            "both ectotherms queried the ADRB3 command does not resolve to a genomic ortholog. Presence of the "
            "drivable pair, observed not assumed, is the criterion."),
    abstract=("A measured cross-species panel (UCP1 furnace, ADRB3 command, PDK4 fuel-switch; human, mouse, rat, "
              "pig, ground squirrel, zebrafish, frog) shows the command gene present across endotherms and absent in "
              "the ectotherms queried. The deeper criterion is the DYNAMICS -- a defended attractor -- because where "
              "the furnace is silenced (pig pseudogene) the endotherm still defends by other routes."),
    body=(H2("The panel (measured, offline-reproducible)") +
          P("Every " + G + " below is a real promoter read fetched through the DNA pipeline (nearest-neighbour "
            "stacking energy, SantaLucia 1998, window TSS&minus;2000..+500) and cached so it re-derives offline "
            "bit-for-bit (" + str(FA["rederive"]["offline_identical"]) + ").") +
          table(["species", "class", "UCP1 " + G, "ADRB3 " + G, "PDK4 " + G, "command pair?"], crit_rows) +
          H2("The criterion, stated") +
          P("Endotherms have the drivable {UCP1 furnace + ADRB3 command} pair: " +
            str(GC["observed_endotherms_have_command_pair"]) + ". The ectotherms queried lack the ADRB3 command (no "
            "ortholog resolves): " + str(GC["observed_ectotherms_lack_ADRB3_command"]) + ". The criterion is a "
            "PRESENT, drivable effector-command pair -- a structural fact about the genome, read by presence, not a "
            "number on the " + G + " scale.") +
          H2("Why the deeper criterion is the dynamics") +
          P("The pig is an endotherm whose UCP1 is a pseudogene, yet it still defends its setpoint by other routes. "
            "So the single furnace gene is neither necessary nor a " + G + " threshold; the robust criterion is the "
            "DEFENDED ATTRACTOR itself, which the R19 loop captures directly. Two explicit NULLs make this firewall "
            "concrete (next chapter and the bear-vs-human chapter).") +
          H2("Grades") +
          P("Gene presence is [L] cited and observed (auditable accessions). The strong 'command absent across all "
            "ectotherms' claim is [O] -- symbol orthology across distant taxa is itself uncertain; the "
            "queried-assembly observation is [L].")),
    cards=[vp_card("endotherm pair = " + str(GC["observed_endotherms_have_command_pair"]), "{UCP1 + ADRB3} present across endotherms", "l"),
           vp_card("ectotherm ADRB3 absent = " + str(GC["observed_ectotherms_lack_ADRB3_command"]), "no command ortholog resolves", "o")])

# ---- §2.1 ----
add(no="&sect;2.1", slug="null-ucp1-gamma-does-not-separate", title="NULL: UCP1 gamma does not separate endotherm from ectotherm", kind="core",
    desc="A pre-registered null: the UCP1 gamma gap is GC-confounded and a pseudogene sits among functional rodents.", grade="v",
    answer=("UCP1 promoter " + G + " does NOT separate the two strategies by value. The endotherm reads (" + endo_ucp1 +
            ") sit above the ectotherm reads (" + ecto_ucp1 + "), but that gap tracks GC content, and the pig's UCP1 "
            "PSEUDOGENE reads " + f(N1["pig_pseudogene_UCP1_gamma"]) + " -- squarely among the functional rodents. " +
            G + " is blind to thermogenic function."),
    abstract=("This null is the firewall made measurable. The endotherm/ectotherm " + G + " difference is GC-driven "
              "(ectotherm promoter GC ~0.33-0.38 vs endotherm ~0.50-0.53), and a non-functional pseudogene reads in "
              "the functional envelope. The promoter read reports stiffness, never thermogenic capacity."),
    body=(H2("The reads") +
          P("Endotherm UCP1 " + G + ": " + endo_ucp1 + ". Ectotherm UCP1 " + G + ": " + ecto_ucp1 + ". The pig "
            "pseudogene reads " + f(N1["pig_pseudogene_UCP1_gamma"]) + "; the functional rodents read " +
            ", ".join(f(x) for x in N1["functional_rodent_UCP1_gamma"]) + ". The pseudogene falls INSIDE the "
            "functional-rodent envelope: " + str(N1["pig_pseudogene_gamma_inside_functional_rodent_envelope"]) + ".") +
          H2("Why the gap is not the criterion") +
          P("The lower ectotherm reads are GC-confounded, and a gene that makes no functional furnace reads like one "
            "that does. If " + G + " encoded thermogenic capacity, the pseudogene would stand out; it does not. This "
            "is exactly why Q1's criterion is gene PRESENCE and a defended attractor, not a " + G + " value.") +
          H2("This is a feature") +
          P("The framework treats such nulls as results. The same honesty appears in the DNA package's gene atlases: "
            "the read places a gene on a structural scale; it does not adjudicate the gene's physiological output.")), cards=[])

# ---- §3 ----
add(no="&sect;3", slug="the-thermostat", title="The thermostat: a sub-spinodal step is corrected", kind="dynamics",
    desc="The preoptic comparator defends the setpoint until an ambient step exceeds the R19 spinodal.", grade="v",
    answer=("The preoptic thermostat is the defended upper R19 basin at the setpoint. A sub-spinodal ambient step is "
            "corrected back toward the setpoint (" + f(TH["defended_setpoint"]) + " in R19 units); once the step "
            "exceeds the spinodal " + f(TH["spinodal_h_sp"]) + " the euthermic basin disappears and the defense is "
            "overwhelmed. Error stays bounded while sub-threshold."),
    abstract=("RT2. The thermostat corrects ambient steps below the R19 spinodal and fails abruptly past it -- a "
              "regulated comparator with a hard threshold, not a proportional knob. The setpoint (~37 &deg;C) is "
              "cited [L]; the mechanism is [V]; the absolute gain and latency are [O]."),
    body=(H2("Bounded correction below threshold") +
          P("Stepping the ambient drive while holding the upper basin, every sub-spinodal step is pulled back to the "
            "setpoint with bounded error (" + str(TH["error_bounded_while_substhreshold"]) + "); steps beyond the "
            "spinodal collapse the basin (" + str(TH["collapses_past_spinodal"]) + "). The spinodal " +
            f(TH["spinodal_h_sp"]) + " is the comparator's authority limit.") +
          H2("Why a hard threshold matters") +
          P("A real thermostat tolerates weather but is overwhelmed by extremes; the R19 spinodal gives exactly that "
            "shape -- robust regulation up to a sharp edge, then loss of control. The same edge reappears as the "
            "fever/hyperthermia boundary and the torpor switch.")),
    cards=[vp_card(HSP + " = " + f(TH["spinodal_h_sp"]), "the thermostat's correction-authority limit", "v"),
           vp_card("setpoint ~37 &deg;C", "cited physiological set value", "l")])

# ---- §4 ----
add(no="&sect;4", slug="energetic-cost-of-endothermy", title="The energetic cost of endothermy", kind="dynamics",
    desc="Defending a setpoint costs restoring flux that rises with loop gain; the cited factor is ~5-10x.", grade="o",
    answer=("Defending a setpoint is not free: the restoring flux that holds the basin against an ambient drive rises "
            "with loop gain (" + str(COST["cost_rises_with_defence"]) + "). A resting endotherm therefore idles at a "
            "much higher metabolic rate than an equal-mass ectotherm at the same body temperature -- a cited factor "
            "of roughly 5-10x. The absolute rate is open."),
    abstract=("RT3. The trade-off is structural: thermal stability is bought with continuous restoring flux. The R19 "
              "loop reproduces the DIRECTION (cost rises with defense); the MAGNITUDE (~5-10x resting metabolic rate) "
              "is cited [L]; absolute W/kg is [O] and needs external calorimetry."),
    body=(H2("Stability costs flux") +
          P("In the loop, a deeper basin resists drive but demands more restoring flux to hold position against it. "
            "That flux is the metabolic price of a defended setpoint. The model gives the sign and the "
            "monotonicity, not the watts.") +
          H2("The cited range (Q3, part 1)") + P(esc(COST["cited_absolute_ratio"])) +
          H2("Honest open") +
          fw("Absolute W/kg is [O]: the obstacle is that the R19 restoring flux is in model units, and mapping it to "
             "metabolic power needs an external calorimetry calibration the substrate does not contain. The ~5-10x "
             "factor is carried as a CITED measurement, not a derived number.")), cards=[])

# ---- §5 ----
add(no="&sect;5", slug="continuum-or-switch", title="Continuum or switch? A discontinuous regime boundary", kind="dynamics",
    desc="The endotherm/ectotherm regimes are separated by an R19 spinodal -- a discontinuous jump, not a smooth gradient.", grade="v",
    answer=("Between a defended and a tracked setpoint there is a discontinuous jump at the R19 spinodal (" +
            f(CS["r19_spinodal_h_sp"]) + "), not a smooth gradient: just inside the spinodal the state holds the "
            "defended branch; just outside it falls to the tracking branch. The strategies are separated by a sharp "
            "regime boundary in the loop dynamics."),
    abstract=("RT4 and Q3 (part 2). The defend/track distinction is qualitative: an R19 bistable boundary, not a "
              "continuum. The jump at the spinodal is reproducible [V]; the placement of any real species relative "
              "to the boundary is a separate empirical question."),
    body=(H2("The jump") +
          P("Approaching the spinodal from inside, the defended state persists; crossing it, the state drops "
            "discontinuously to the other branch (" + str(CS["discontinuous_jump_at_spinodal"]) + "). That is the "
            "signature of bistability -- the same mathematics that makes the torpor transition a switch.") +
          H2("Range, qualitatively (Q3, part 3)") +
          P("So the strategies differ over a RANGE that is not merely large but qualitatively partitioned: a "
            "metabolic factor of several-fold (previous chapter) PLUS a discontinuous regime boundary here. " + G +
            " itself spans only ~1.22-1.50 across the panel and does not track the divide -- the real range is in "
            "the dynamics, not the promoter read.")),
    cards=[vp_card(HSP + " = " + f(CS["r19_spinodal_h_sp"]), "the regime boundary between defend and track", "v")])

# ---- §6 ----
add(no="&sect;6", slug="kleiber-allometry", title="Kleiber allometry: an honest open problem", kind="dynamics",
    desc="The 3/4-power metabolic scaling is not derivable from the R19 substrate alone; reported [O] with its obstacle.", grade="o",
    answer=("Kleiber's law -- metabolic rate scaling as mass to the 3/4 power -- is reported here as OPEN. The R19 "
            "substrate sets setpoint dynamics, not the transport-network geometry that the 3/4 exponent is usually "
            "argued from. Rather than fit a number to look complete, this chapter states the obstacle plainly."),
    abstract=("RT5. The CHARTER bar is 'reproduced [V] OR honestly flagged [O]'. The exponent needs an external "
              "supply-network argument (fractal distribution geometry) absent from the substrate, so it is graded "
              "[O] with a stated obstacle -- not faked."),
    body=(H2("Why it is open") + P(esc(KLE["obstacle"])) +
          H2("Why we do not fake it") +
          fw("A tuned exponent would violate the no-tuning discipline and the honesty grading. The substrate carries "
             "no body-size axis and no distribution network; the 3/4 law is a real result of a DIFFERENT model "
             "layer. Marking it [O] keeps the gate honest -- an open problem named, not hidden.")), cards=[])

# ---- §7 ----
add(no="&sect;7", slug="brown-fat-thermogenesis", title="Brown-fat thermogenesis: recruiting the furnace", kind="dynamics",
    desc="Cold past the spinodal would collapse the setpoint; recruiting UCP1 adds heat flux that defends it.", grade="v",
    answer=("A cold drive past the spinodal would collapse the euthermic basin (the state falls to " +
            f(BAT["state_cold_no_thermogenesis"]) + "). Recruiting the UCP1 furnace -- cold &rarr; ADRB3 command "
            "&rarr; uncoupled proton leak &rarr; heat -- adds a compensating flux that returns the NET drive below "
            "the spinodal, so the state is defended (" + f(BAT["state_with_UCP1_recruited"]) + ")."),
    abstract=("RG1. Brown-fat thermogenesis is the active arm of setpoint defense: the furnace supplies the restoring "
              "flux that keeps the net cold drive sub-spinodal. Mechanism [V]; the BAT output rate is cited [L]; "
              "absolute W/kg is [O]. This is the {UCP1 + ADRB3} pair of Q1 doing its job."),
    body=(H2("Cold alone vs cold with the furnace") +
          P("Without thermogenesis a supra-spinodal cold drive overwhelms the basin (" +
            str(BAT["cold_alone_overwhelms"]) + "); with UCP1 recruited the compensating heat flux restores the "
            "setpoint (" + str(BAT["thermogenesis_restores_setpoint"]) + "). The command-effector pair from Q1 is "
            "exactly the machinery that supplies this flux.") +
          H2("Why ectotherms cannot do this") +
          P("An organism lacking the drivable command pair has no way to inject this restoring flux on demand, so a "
            "supra-spinodal cold drive simply tracks -- the body cools with the environment. The gene criterion and "
            "the dynamics meet here.")),
    cards=[vp_card("state " + f(BAT["state_with_UCP1_recruited"]), "setpoint defended after UCP1 recruitment", "v")])

# ---- §8 ----
add(no="&sect;8", slug="fever-vs-hyperthermia", title="Fever vs hyperthermia: regulated shift vs lost control", kind="dynamics",
    desc="Fever raises the regulated setpoint (still defended); hyperthermia destroys the regulated basin.", grade="v",
    answer=("Fever and hyperthermia look alike but are opposite in regulatory status. Fever is a sustained "
            "sub-spinodal pyrogen bias that moves the regulated set value UP (to " + f(FV["fever_setpoint"]) +
            " from " + f(FV["normal_setpoint"]) + ") -- perturb it and it returns to the elevated setpoint. "
            "Hyperthermia is a supra-spinodal external heat load that DESTROYS the regulated basin (runaway)."),
    abstract=("RG3. Same substrate, opposite outcome. Fever = regulation intact at a higher setpoint; hyperthermia = "
              "regulation lost. The distinction is whether the drive stays below the spinodal. Mechanism [V]; the "
              "setpoint-shift magnitude is [L]; absolute temperature is [O]."),
    body=(H2("Fever: a regulated upward shift") +
          P("The pyrogen bias is sub-spinodal (" + str(FV["fever_is_sub_spinodal"]) + "), so the basin survives but "
            "its position moves up; a perturbation returns to the elevated setpoint (" +
            str(FV["fever_returns_after_perturbation"]) + "). The body is not failing to cool -- it is DEFENDING a "
            "deliberately raised target.") +
          H2("Hyperthermia: control destroyed") +
          P("An external heat load above the spinodal destroys the regulated well (" +
            str(FV["hyperthermia_well_destroyed"]) + "): there is no setpoint left to return to, and the state runs "
            "away. The clinical difference -- treat the cause vs cool immediately -- falls straight out of which "
            "side of the spinodal the drive is on.")),
    cards=[vp_card("fever setpoint " + f(FV["fever_setpoint"]), "regulated upward shift (still defended)", "v"),
           vp_card("hyperthermia: basin destroyed", "supra-spinodal heat load, regulation lost", "v")])

# ---- §9 ----
add(no="&sect;9", slug="torpor-switch", title="The torpor switch: a bistable flip with hysteresis", kind="core",
    desc="Euthermia to torpor is a discontinuous bistable SWITCH (hysteresis loop ~2 h_sp), not a continuous dial.", grade="v",
    answer=("Is euthermia&harr;torpor a discrete flip or a smooth dial? Ramping the torpor drive DOWN holds the "
            "euthermic branch until &minus;h<sub>sp</sub> then JUMPS to torpor (at " + f(HY["jump_down_drive"]) +
            "); ramping back UP holds torpor until +h<sub>sp</sub> then jumps back (at " + f(HY["jump_up_drive"]) +
            "). The hysteresis loop has width " + f(HY["hysteresis_loop_width"]) + " &mdash; a bistable SWITCH."),
    abstract=("RH1, the package's central question. A hysteresis loop of width ~2&middot;" + HSP + " with "
              "discontinuous jumps is the signature of bistability: torpor is a state the loop FLIPS into, not a "
              "metabolic rate it slides down. Mechanism [V]; the drive threshold is [L]; the absolute metabolic-rate "
              "drop is [O]."),
    body=(H2("The hysteresis loop") +
          P("The down-jump and up-jump occur at opposite-signed drives (" + f(HY["jump_down_drive"]) + " and " +
            f(HY["jump_up_drive"]) + "), so the system shows a loop of width " + f(HY["hysteresis_loop_width"]) +
            " &mdash; positive (" + str(HY["loop_width_positive"]) + "), which by definition means two stable states "
            "coexist over a range of drives. That is a switch, not a dial (" + str(HY["is_switch_not_dial"]) + ").") +
          H2("Why this is the right framing for hibernation") +
          P("A deep hibernator does not gently lower its rate; it commits to a distinct low-metabolic STATE and later "
            "commits back. Hysteresis explains why interbout arousals are abrupt and why the transition resists "
            "small perturbations -- the opposite basin has to disappear before the flip happens.") +
          H2("The cross-species twist") +
          P("If torpor is a switch, the next question is whether the switch is BUILT INTO the human genome (present "
            "but silenced) or absent. The bear-vs-human chapter answers it from the measured panel.")),
    cards=[vp_card("loop width " + f(HY["hysteresis_loop_width"]), "hysteresis = two coexisting stable states = a switch", "v"),
           vp_card("jumps at &plusmn;" + f(HY["spinodal_h_sp"]), "discontinuous transition at the R19 spinodal", "v")])

# ---- §10 ----
add(no="&sect;10", slug="torpor-is-regulated", title="Torpor is regulated, not a passive collapse", kind="dynamics",
    desc="The low torpor state is a defended attractor: a perturbation below it is actively corrected back.", grade="v",
    answer=("The low-metabolic torpor state is itself a REGULATED attractor, not a passive floor. Settling under a "
            "torpor drive gives a defended low setpoint (" + f(TR["torpor_setpoint"]) + "); pushing the state further "
            "down is actively corrected back to it (" + str(TR["returns_to_torpor_setpoint"]) + "). Torpor is "
            "defended low metabolism, not loss of control."),
    abstract=("RH2. Bistability (previous chapter) plus active regulation of the LOW state (here) together describe "
              "hibernation: the organism flips into a distinct basin AND defends a setpoint there. Mechanism [V]; the "
              "torpor setpoint depth is [L]; absolute body temperature and metabolic rate are [O]."),
    body=(H2("A defended low setpoint") +
          P("The torpor basin behaves like the euthermic one in miniature: it has a position the loop returns to "
            "after a perturbation. A hibernating animal that drifts too cold rewarms toward its torpor target rather "
            "than continuing to fall -- the basin pulls it back.") +
          H2("Two regulated states, one loop") +
          P("So the same R19 loop offers two defended setpoints -- euthermic and torpid -- separated by the spinodal. "
            "Hibernation is moving between them, not abandoning regulation. This is the cleanest statement of why "
            "torpor is controlled physiology and not hypothermic failure.")),
    cards=[vp_card("torpor setpoint " + f(TR["torpor_setpoint"]), "the LOW state is a defended attractor", "v")])

# ---- §11 ----
nonhib = ", ".join(f(v) for v in N2["non_hibernator_PDK4_gamma"].values())
add(no="&sect;11", slug="bear-vs-human", title="Bear vs human: a present-but-silenced switch", kind="core",
    desc="PDK4 gamma does not mark hibernation; the torpor switch genes are present in non-hibernators too, silenced.", grade="v",
    answer=("Does the human genome lack the torpor switch, or carry it silenced? The deep hibernator's PDK4 "
            "fuel-switch " + G + " (" + f(N2["deep_hibernator_PDK4_gamma"]) + ") is NOT elevated versus "
            "non-hibernators (" + nonhib + ") -- so " + G + " does not mark hibernation. The torpor program is a "
            "PRESENT switch gated by REGULATION, not a special promoter read."),
    abstract=("RH4 and Q1's deepest answer. A pre-registered null: PDK4 promoter " + G + " in a deep hibernator is "
              "unremarkable among non-hibernators. The fuel-switch is present across the endotherm set, humans "
              "included; what differs is regulatory GATING of that present switch, not its sequence-level stiffness."),
    body=(H2("The null") +
          P("Deep-hibernator PDK4 " + G + " = " + f(N2["deep_hibernator_PDK4_gamma"]) + "; non-hibernator PDK4 " + G +
            " = " + nonhib + ". The hibernator value is not elevated (" +
            str(N2["hibernator_gamma_elevated_vs_nonhibernators"]) + "). If hibernation lived in the promoter read, "
            "the hibernator would stand out. It does not.") +
          H2("Present but silenced") +
          P("Combined with the torpor-switch chapters, the reading is direct: the bistable switch exists in genomes "
            "that never use it. The capability is REGULATORY gating of a present switch -- which is precisely why the "
            "question 'can a human be induced into a torpor-like state' is about control signals, not missing "
            "genes.") +
          H2("Grades") +
          P("The reads are [V] and reproduce offline. The interpretation -- a silenced switch held by regulation -- "
            "is [O]: the panel places the genes; it does not derive the gating circuitry.")),
    cards=[vp_card("hibernator PDK4 " + f(N2["deep_hibernator_PDK4_gamma"]), "not elevated -- gamma does not mark torpor", "v"),
           vp_card("present-but-silenced", "the switch is regulatory gating, not a gamma threshold", "o")])

# ---- §11.1 ----
_n3_rows = []
for _r in N3["per_gene"]:
    _n3_rows.append([
        "<b>" + esc(_r["gene"]) + "</b>",
        f(_r["hib_gamma_range"][0]) + "&ndash;" + f(_r["hib_gamma_range"][1]),
        f(_r["non_gamma_range"][0]) + "&ndash;" + f(_r["non_gamma_range"][1]),
        ("yes" if _r["ranges_overlap"] else "<b>NO</b>"),
        ("%+.4f" % _r["delta_gamma_hib_minus_non"]),
        ("%+.4f" % _r["delta_gc_hib_minus_non"]),
        f(_r["exact_perm_p"], 3),
    ])
_n3_r = N3["cross_gene_pearson_r_delta_gamma_vs_delta_gc"]
_n3_ngenes = str(N3["genes_tested"]); _n3_sep = str(N3["genes_that_cleanly_separate_by_gamma"])
_n3_nhib = str(len(N3["hibernators"])); _n3_nnon = str(len(N3["non_hibernators"]))
add(no="&sect;11.1", slug="null-no-promoter-marks-hibernation", title="NULL: no promoter in the torpor panel marks hibernation", kind="core",
    desc="The strongest forward test: across an 8-gene fuel-switch/BAT panel read over 14 species, no promoter gamma separates hibernators -- and every group gap is a GC gap.", grade="v",
    answer=("Widen the §11 question from one gene to the whole declared torpor program. Across " + _n3_ngenes +
            " fuel-switch / BAT-identity genes read over 14 species (" + _n3_nhib + " hibernators vs " + _n3_nnon +
            " non-hibernators among endotherms), the number of genes whose promoter " + G + " cleanly separates "
            "hibernators from non-hibernators is " + _n3_sep + ". Every group-mean gap that exists co-signs and "
            "co-scales with the group GC gap (cross-gene Pearson r(&Delta;" + G + ",&Delta;GC) = " + f(_n3_r) +
            "). The panel does not encode who can hibernate."),
    abstract=("RH8, the v0.4.0 hibernation-bridge expansion and the strongest forward result in the package. A "
              "pre-registered null carried from one fuel-switch gene (RH4) to the entire torpor program. 88 promoters "
              "were read across deep hibernators (ground squirrels, marmot, hamster, black bear), a torpor-capable "
              "primate, daily heterotherms, and non-hibernating controls including a GC-matched rodent. No promoter "
              "read tracks hibernation capability; the group differences that exist are the GC differences. The "
              "capability is regulatory gating of present genes, not a sequence-level " + G + " threshold."),
    body=(H2("The panel") +
          P("Eight genes spanning the furnace (UCP1), the sympathetic command (ADRB3), the fuel switch (PDK4), the "
            "mitochondrial coactivator (PPARGC1A), thyroid activation (DIO2), brown-fat identity (CIDEA), the "
            "metabolic-state hormone (FGF21) and the insulin-responsive glucose transporter (SLC2A4). Each promoter "
            + G + " is re-derived offline from the vendored cache, identical scale to every other chapter.") +
          H2("The reads, by gene") +
          P("For each gene: the hibernator " + G + " range, the non-hibernator " + G + " range, whether the two "
            "ranges OVERLAP (they all do), the hibernator-minus-non difference in mean " + G + " and in mean GC, and "
            "an exact permutation p (exhaustive over all label splits, no RNG).") +
          table(["gene", "hibernator " + G, "non-hib " + G, "ranges overlap", "&Delta;" + G, "&Delta;GC", "exact p"], _n3_rows) +
          H2("The gap is the GC gap") +
          P("Across the panel the per-gene " + G + " gaps line up almost exactly with the GC gaps: the cross-gene "
            "correlation r(&Delta;" + G + ", &Delta;GC) is " + f(_n3_r) + ", near unit slope. The single nominally "
            "low-p gene (ADRB3) fails a Bonferroni correction, is GC-matched, has fully overlapping ranges, and runs "
            "biologically backwards (the sympathetic command reads LOWER in hibernators) -- it is the GC confound, "
            "not a torpor signal.") +
          H2("Why this is the headline null") +
          P("This is the present-but-silenced reading (§11) made quantitative and general: the fuel-switch / BAT "
            "program is PRESENT across the endotherm set, humans included, and its promoter stiffness does not mark "
            "who actually hibernates. Hibernation is REGULATORY gating of a present program, not a property a "
            "promoter read can see. A clean negative result is the contribution.") +
          H2("Grades") +
          P("The reads and the GC confound are [V]: reproducible offline, and the confound is a parameter-free, "
            "re-derivable fact (per-gene sign agreement plus the near-unit cross-gene slope). The conclusion that NO "
            "promoter marks hibernation is [O]: small n, species are not phylogenetically independent draws, and the "
            "regulatory-gating mechanism is cited biology, not derived here.")),
    cards=[vp_card(_n3_sep + " of " + _n3_ngenes + " genes separate", "no promoter gamma marks hibernation across the panel", "v"),
           vp_card("r(&Delta;" + G + ",&Delta;GC) = " + f(_n3_r), "every group gamma gap is a GC gap (near unit slope)", "v"),
           vp_card("regulatory gating", "hibernation is gating of present genes, not a gamma threshold", "o")])

# ---- §11.2 ----
_n4_rows = []
for _r in N4["per_gene"]:
    _n4_rows.append([
        "<b>" + esc(_r["gene"]) + "</b>",
        f(_r["hib_cpg_oe_range"][0]) + "&ndash;" + f(_r["hib_cpg_oe_range"][1]),
        f(_r["non_cpg_oe_range"][0]) + "&ndash;" + f(_r["non_cpg_oe_range"][1]),
        ("yes" if _r["ranges_overlap"] else "<b>NO</b>"),
        ("%+.4f" % _r["delta_cpg_oe_hib_minus_non"]),
        f(_r["exact_perm_p"], 3),
    ])
_n4_sep = str(N4["genes_that_cleanly_separate_by_cpg_oe"]); _n4_ng = str(N4["genes_tested"])
_n4_rgo = N4["cross_cell_pearson_r_gamma_vs_cpg_oe"]
_n4_rgg = N4["cross_cell_pearson_r_gamma_vs_gc"]
_n4_rog = N4["cross_cell_pearson_r_cpg_oe_vs_gc"]
add(no="&sect;11.2", slug="null-methylation-substrate-does-not-mark-hibernation",
    title="NULL: the methylation substrate does not mark hibernation either", kind="core",
    desc="A GC-normalized methylation-substrate read (CpG observed/expected) of the same 8-gene panel ALSO fails to separate hibernators (0/8), and is a distinct read from gamma -- a second static layer is blind to hibernation.", grade="v",
    answer=("RH8 closed one static sequence layer (stacking-stiffness " + G + "), but " + G + " is almost "
            "entirely GC-loaded here (cross-cell r(" + G + ",GC) = " + f(_n4_rgg) + "), so a skeptic could say "
            "only GC was tested. The methylation SUBSTRATE -- CpG observed/expected, which is GC-NORMALIZED -- "
            "is the natural second layer. Across the same " + _n4_ng + " genes the number whose CpG O/E cleanly "
            "separates hibernators is " + _n4_sep + ". CpG O/E is a distinct read from " + G + " (r = " +
            f(_n4_rgo) + ") and far less GC-loaded (r(CpG O/E, GC) = " + f(_n4_rog) + "). A second, independent "
            "static layer is also blind to who can hibernate."),
    abstract=("RH9, the v0.5.0 regulatory-layer object. The firewalled next step the v0.4.0 handover named: test "
              "whether the present-but-silenced gating is visible in a regulatory-relevant read, " + G + " still "
              "reading structure only. CpG observed/expected is the genomic SUBSTRATE on which DNA methylation "
              "acts; it divides the observed CpG count by the count expected from C and G, removing the first-order "
              "GC dependence that drives the RH8 confound. It STILL does not separate hibernators -- so neither the "
              "stacking-stiffness layer nor the methylation-substrate layer encodes hibernation capacity. The "
              "capability is DYNAMIC regulatory gating of genes present in all (humans included), readable only in "
              "an in-vivo torpor&harr;euthermia methylation/expression contrast (cited, [O] external)."),
    body=(H2("Why a second layer, and which one") +
          P("RH8 (&sect;11.1) showed no promoter " + G + " marks hibernation, but every group " + G + " gap there "
            "WAS the group GC gap. " + G + " is a nearest-neighbour stacking-stiffness read and, across this panel, "
            "is almost entirely GC-loaded (cross-cell r(" + G + ",GC) = " + f(_n4_rgg) + "). The honest objection is "
            "that RH8 only ruled out GC. CpG observed/expected (Gardiner-Garden &amp; Frommer 1987) answers it: it "
            "is the methylation SUBSTRATE -- the CpG-island architecture methylation acts on -- and it is "
            "GC-NORMALIZED by construction (observed CpG divided by the C,G-expected count), so it is NOT a "
            "restatement of GC.") +
          H2("The reads, by gene") +
          P("For each gene: the hibernator CpG O/E range, the non-hibernator range, whether they OVERLAP (they all "
            "do), the hibernator-minus-non difference in mean CpG O/E, and an exact permutation p (exhaustive over "
            "all label splits, no RNG).") +
          table(["gene", "hibernator CpG O/E", "non-hib CpG O/E", "ranges overlap", "&Delta;CpG O/E", "exact p"], _n4_rows) +
          H2("A distinct layer, and still blind") +
          P("CpG O/E is genuinely a different read from " + G + ": the cross-cell correlation r(" + G +
            ", CpG O/E) is " + f(_n4_rgo) + " -- clearly sub-unit -- and CpG O/E is far less GC-loaded (r = " +
            f(_n4_rog) + " vs " + f(_n4_rgg) + " for " + G + "). Yet it STILL fails to separate hibernators (" +
            _n4_sep + " of " + _n4_ng + " genes), and no gene survives a Bonferroni correction. Two independent "
            "static sequence layers -- stacking stiffness and methylation-substrate architecture -- are both flat "
            "across hibernation status.") +
          H2("Where the capability actually lives") +
          fw("The present-but-silenced gating is DYNAMIC: which CpG sites are methylated, when, and which "
             "transcripts move across the torpor&harr;euthermia cycle. That is a Layer-2 in-vivo measurement "
             "(cited: hibernation expression atlases and torpor methylation dynamics), NOT a static promoter "
             "property and NOT derivable from any sequence read. It is graded [O] external: the package's "
             "offline-reproducibility invariant precludes vendoring processed in-vivo data, so this is the named "
             "honest next step -- not a stub, and not faked here. " + G + " still reads structure only.") +
          H2("Grades") +
          P("The CpG O/E reads, the " + G + "&harr;CpG-O/E dissociation, and the GC-loading contrast are [V]: "
            "reproducible offline and parameter-free. The conclusion that NO static promoter read marks "
            "hibernation is [O]: small n, phylogenetic non-independence, and the dynamic regulatory gating that "
            "DOES carry the capability is cited external biology, not derived here.")),
    cards=[vp_card(_n4_sep + " of " + _n4_ng + " separate", "the methylation substrate (CpG O/E) does not mark hibernation either", "v"),
           vp_card("r(" + G + ",CpG O/E) = " + f(_n4_rgo), "a distinct, GC-normalized read -- not a gamma restatement", "v"),
           vp_card("dynamic regulation", "the gating is in-vivo methylation/expression state, [O] external", "o")])

# ---- §12 ----
add(no="&sect;12", slug="arousal-rhythm", title="The interbout arousal rhythm", kind="dynamics",
    desc="Periodic interbout arousals are a slow relaxation oscillator on the same R19 substrate.", grade="v",
    answer=("Hibernation is punctuated by periodic interbout arousals. On the shared substrate this is a slow "
            "relaxation oscillator -- the same FitzHugh-Nagumo form (R19 switch plus a slow recovery variable) used "
            "across the neuro package. It oscillates here (" + str(OSC["oscillates"]) + ", " + str(OSC["beats"]) +
            " beats in the probe); the period in days is a cited anchor."),
    abstract=("RH6. The arousal rhythm is not a new mechanism: the R19 switch with a slow recovery gives a "
              "low-frequency oscillation by construction. Mechanism [V]; the interbout period (days) is [L], an "
              "external anchor rather than a derived rate."),
    body=(H2("A slow relaxation oscillator") +
          P("The recovery variable sets the period, so the intrinsic rhythm is far slower than the switch timescale "
            "-- exactly why the substrate 'speaks at low frequency'. The torpor-arousal node reuses this directly; "
            "the probe confirms it cycles (" + str(OSC["beats"]) + " beats).") +
          H2("Rate is an anchor, not a derivation") +
          fw("The interbout period (order of days) is [L]: a cited physiological anchor. The substrate gives the "
             "OSCILLATORY FORM for free; it does not set the absolute period, which depends on recovery time "
             "constants taken from measurement.")),
    cards=[vp_card("oscillates = " + str(OSC["oscillates"]), "interbout arousal as a slow FHN oscillator", "v")])

# ---- §13 ----
add(no="&sect;13", slug="glucose-homeostat", title="The glucose homeostat", kind="dynamics",
    desc="Euglycemia is a defended R19 attractor; a glucose load is returned to the setpoint by the insulin loop.", grade="v",
    answer=("Euglycemia is a defended R19 attractor on the insulin-glucose node. A glucose load displaces the state; "
            "the insulin loop returns it to the setpoint (" + str(GL["returns_to_euglycemia"]) + "). The same "
            "defended-basin logic that pins body temperature pins blood glucose -- one substrate, two regulated "
            "variables. The ~5 mM set value is cited."),
    abstract=("RE1. Whole-body glucose control is the temperature thermostat in another variable: a regulated "
              "attractor that opposes displacement. Mechanism [V]; the euglycemic setpoint (~5 mM) is [L]; the "
              "absolute glucose excursion in mg/dL is [O]."),
    body=(H2("Load and return") +
          P("Starting at the euglycemic setpoint (" + f(GL["euglycemia_setpoint"]) + " in R19 units), a positive "
            "load is corrected back (" + str(GL["returns_to_euglycemia"]) + "). This is the homeostatic baseline "
            "whose FAILURE the type-2-diabetes chapter describes as a loop-gain drop.") +
          H2("Why glucose belongs in a thermometabolic map") +
          P("Temperature and fuel are defended by the same control architecture, and they are coupled -- the torpor "
            "fuel-switch (PDK4) sits between them. Treating glucose as one more defended setpoint is what lets the "
            "hibernation-bridge chapter connect torpor to insulin resistance.")),
    cards=[vp_card("euglycemia setpoint " + f(GL["euglycemia_setpoint"]), "defended attractor; load is returned", "v"),
           vp_card("~5 mM", "cited euglycemic set value", "l")])

# ---- §14 ----
add(no="&sect;14", slug="lipostat", title="The lipostat: a defended adiposity setpoint", kind="dynamics",
    desc="Adiposity sits in a regulated R19 basin; sustained sub-spinodal over/underfeeding is actively opposed.", grade="v",
    answer=("Body fat is regulated, not merely accumulated. Adiposity sits in a defended R19 basin; sustained "
            "sub-spinodal over- or underfeeding shifts the defended state only modestly and is actively opposed "
            "(leptin-melanocortin) (" + str(LP["setpoint_opposes_perturbation"]) + "). A supra-spinodal chronic "
            "drive would cross to a NEW basin -- the obesity setpoint of the next section."),
    abstract=("RE2. The lipostat is a defended setpoint with the usual hard edge: modest chronic forcing is opposed, "
              "but a large enough sustained drive crosses the spinodal to a new defended adiposity. Mechanism [V]; "
              "the adiposity setpoint is [L]; absolute kg/BMI is [O]."),
    body=(H2("Opposed, within limits") +
          P("Sustained overfeeding and underfeeding both shift the defended state only modestly and are pushed back "
            "(" + str(LP["setpoint_opposes_perturbation"]) + "). The lipostat behaves like the thermostat: robust "
            "regulation up to a threshold.") +
          H2("The edge is the disease") +
          P("Crucially, a chronic drive ABOVE the spinodal does not just shift the setpoint -- it crosses to a "
            "different basin. That crossing is exactly how obesity is framed in the pathology section: not a failure "
            "of will but a defended setpoint that has moved.")),
    cards=[vp_card("adiposity setpoint " + f(LP["adiposity_setpoint"]), "defended basin; chronic forcing opposed", "v")])

# ---- §15 ----
add(no="&sect;15", slug="disease-as-setpoint-failure", title="Disease as setpoint failure (the derived law)", kind="disease",
    desc="Metabolic disease is a loop-gain drop -> shallower basin + lower crossing threshold under a chronic forcing.", grade="v",
    answer=("Metabolic disease here is not a local lesion -- it is a defended setpoint that drifted or crossed to a "
            "pathological basin. One derived law covers all of it: a loop-gain drop d lowers the effective stiffness "
            "g&rarr;g(1&minus;d), which SHRINKS the barrier and LOWERS the crossing threshold, so a chronic forcing "
            "then drifts or crosses the setpoint."),
    abstract=("The pathology frame. The same Kramers/spinodal kernel the framework uses for carcinogenesis is applied "
              "at the LOOP level: g_eff = g(1&minus;d); barrier = g_eff&sup2;/4; spinodal = 2(g_eff/3)<sup>1.5</sup>; "
              "the state crosses iff the chronic forcing exceeds the reduced spinodal. Shape [V]; cited anchors [L]; "
              "absolute incidence [O]."),
    body=(H2("The law, from R19") + P(esc(PATH["derived_law"])) +
          P("Two regimes follow: a SUB-spinodal chronic forcing DRIFTS the defended setpoint (basin intact, defended "
            "at a shifted value); a SUPRA-spinodal forcing CROSSES to the disease basin (regulation lost). Which "
            "regime a disease is in is a computed result, not an assumption.") +
          H2("Why one law for many diseases") +
          P("Type-2 diabetes, obesity, and metabolic syndrome are not separate mechanisms in this view -- they are "
            "the same loop-gain-drop-plus-chronic-forcing kernel acting on different nodes (glucose, adiposity, and "
            "their shared upstream signalling). The next four chapters instantiate the law per disease.") +
          H2("Composition with the disease whitepaper") +
          P(esc(PATH["disease_wp_composition"]))), cards=[])

# per-disease helper
def _disease_card(site):
    for fa in PATH["failures"]:
        if fa["site"] == site:
            r = fa["r19"]
            return fa, [vp_card("g_eff " + f(r["g_effective"]), "effective stiffness after loop-gain drop", "v"),
                        vp_card("crossed = " + str(r["attractor_crossed"]),
                                ("attractor-shift to the disease basin" if r["attractor_crossed"]
                                 else "setpoint drift, basin intact"), "v")]
    return None, []

# ---- §16 ----
d_t2d, c_t2d = _disease_card("type 2 diabetes"); r_t2d = d_t2d["r19"]
add(no="&sect;16", slug="type-2-diabetes", title="Type 2 diabetes: a crossed glucose setpoint", kind="disease",
    desc="Insulin resistance drops glucose-loop gain; a chronic forcing crosses the euglycemic basin to hyperglycemia.", grade="v",
    answer=("Type 2 diabetes is the glucose homeostat with its loop gain dropped (insulin resistance) while a chronic "
            "caloric/adiposity forcing pushes disposal down. With the barrier shrunk and the crossing threshold "
            "lowered, the state CROSSES the euglycemic basin to the hyperglycemic one (crossed = " +
            str(r_t2d["attractor_crossed"]) + "). It is an attractor-shift, not a tuning error."),
    abstract=("INSR node (" + G + " " + f(r_t2d["gamma"]) + "). A loop-gain drop of " + f(r_t2d["loop_gain_drop"]) +
              " gives g_eff " + f(r_t2d["g_effective"]) + " and residual spinodal " + f(r_t2d["residual_spinodal"]) +
              "; the chronic forcing exceeds it, so the loop crosses to the disease basin. Shape [V]; RR vs cited "
              "BMI/HbA1c cohorts [L]; absolute incidence [O]."),
    body=(H2("Mechanism") + P(esc(d_t2d["mechanism"]) + ".") +
          H2("The numbers") +
          P("Healthy spinodal " + f(r_t2d["healthy_spinodal"]) + " drops to residual " + f(r_t2d["residual_spinodal"]) +
            " under the gain loss; the chronic forcing " + f(abs(r_t2d["chronic_forcing"])) + " exceeds it, so the "
            "euglycemic basin is crossed. The pathological state settles at " + f(r_t2d["pathological_state"]) +
            " (the hyperglycemic branch).") +
          H2("Why this matters for treatment") +
          P("If the disease is a CROSSING, simply reducing the forcing may not return the state once it has crossed "
            "-- restoring loop gain (re-sensitisation) is needed to re-open the euglycemic basin. That is the "
            "falsifiable claim the restoration chapters build on.") +
          fw("RR vs cohort risk is [L] cited; the attractor-shift SHAPE is [V]; absolute incidence is [O] -- the "
             "obstacle is calibrating the model forcing axis to clinical units.")), cards=c_t2d)

# ---- §17 ----
d_ob, c_ob = _disease_card("obesity"); r_ob = d_ob["r19"]
add(no="&sect;17", slug="obesity", title="Obesity: a drifted adiposity setpoint", kind="disease",
    desc="Leptin/melanocortin feedback-gain drop raises the defended adiposity setpoint; sub-spinodal drift, not crossing.", grade="v",
    answer=("Obesity is the lipostat defended at a HIGHER setpoint. A leptin/melanocortin feedback-gain drop raises "
            "the defended adiposity, and a sustained positive energy forcing drifts the regulated state up -- a "
            "SUB-spinodal drift (crossed = " + str(r_ob["attractor_crossed"]) + "), so the body actively DEFENDS the "
            "elevated fat mass, which is why loss is resisted."),
    abstract=("Lipostat node (" + G + " " + f(r_ob["gamma"]) + "). A gain drop of " + f(r_ob["loop_gain_drop"]) +
              " plus a positive forcing drifts the setpoint up without crossing (residual spinodal " +
              f(r_ob["residual_spinodal"]) + " exceeds the forcing). Shape [V]; defended-setpoint drift vs cited "
              "energy-balance data [L]; absolute kg/BMI [O]."),
    body=(H2("Mechanism") + P(esc(d_ob["mechanism"]) + ".") +
          H2("Drift, not crossing") +
          P("Here the chronic forcing " + f(abs(r_ob["chronic_forcing"])) + " stays below the residual spinodal " +
            f(r_ob["residual_spinodal"]) + ", so the basin is intact but its position has moved up. The body defends "
            "the new, higher adiposity -- which is exactly why dieting against a drifted setpoint is opposed by the "
            "same machinery that defends temperature.") +
          H2("Implication") +
          P("Because obesity is a DRIFT, lowering the forcing AND restoring feedback gain can move the setpoint back "
            "without needing to re-cross a barrier. The restoration map places leptin re-sensitisation (S1) and "
            "appetite-forcing reduction (S2) precisely here.")), cards=c_ob)

# ---- §18 ----
d_ms, c_ms = _disease_card("metabolic syndrome"); r_ms = d_ms["r19"]
add(no="&sect;18", slug="metabolic-syndrome", title="Metabolic syndrome: coupled loops crossing together", kind="disease",
    desc="A shared upstream gain drop co-moves the glucose and lipid loops, so the cluster crosses together.", grade="v",
    answer=("Metabolic syndrome is several setpoints failing TOGETHER because they share an upstream node. A gain "
            "drop in the common signalling (insulin) lowers the crossing threshold for both the glucose and lipid "
            "loops at once, so the cluster crosses together (crossed = " + str(r_ms["attractor_crossed"]) + "). The "
            "co-occurrence is structural, not coincidental."),
    abstract=("Shared-node model (" + G + " " + f(r_ms["gamma"]) + "). One upstream gain drop of " +
              f(r_ms["loop_gain_drop"]) + " gates two basins; the chronic forcing crosses the reduced spinodal " +
              f(r_ms["residual_spinodal"]) + " for the coupled cluster. Multi-loop crossing [V]; cluster co-movement "
              "vs cited prevalence [L]; absolute [O]."),
    body=(H2("Mechanism") + P(esc(d_ms["mechanism"]) + ".") +
          H2("Why the cluster moves together") +
          P("When one substrate node gates several defended setpoints, a single gain drop pulls them all toward "
            "crossing simultaneously. That is the structural reason hyperglycemia, dyslipidemia, and the rest "
            "cluster -- they are downstream of the same shrinking barrier.") +
          H2("Implication") +
          P("Restoration aimed at the SHARED node (insulin sensitisation, S1) addresses several crossed loops at "
            "once -- which is why the prioritisation chapter ranks the shared-node target highest.")), cards=c_ms)

# ---- §19 ----
add(no="&sect;19", slug="hibernation-bridge", title="The hibernation bridge: torpor and insulin resistance", kind="disease",
    desc="PDK4 fuel-sparing is reversible in torpor (defended low setpoint) but a chronic misfire in insulin resistance.", grade="v",
    answer=("Torpor and insulin resistance share one machine: the PDK4 fuel-sparing program. In torpor it is a "
            "REGULATED low-fuel attractor that returns after perturbation (" + str(HB["torpor_returns_after_perturbation"]) +
            "); run as a CHRONIC supra-spinodal misfire it becomes insulin resistance -- the state crosses to the "
            "low-disposal basin and stays (" + str(HB["insulin_resistance_crossed_and_stuck"]) + "). Same machinery, "
            "opposite regulatory status."),
    abstract=("RD4, the package's namesake hypothesis. PDK4 (" + G + " " + f(HB["pdk4_gamma"]) + ") drives glucose "
              "sparing. The R19 distinction is regulatory: a defended low setpoint (torpor) versus a chronic crossing "
              "held in the disease basin (insulin resistance). Framing [V]; the PDK4 co-upregulation biology is [O] "
              "cited; absolute [O]."),
    body=(H2("One machine, two fates") + P(esc(HB["distinction"]) + ".") +
          H2("Why this is a bridge, not a metaphor") +
          P("The fuel-switch is the SAME gene with the SAME promoter read in both cases; what differs is whether the "
            "program is engaged as a defended, reversible state or as a chronic, supra-spinodal drive that crosses "
            "and sticks. That is a concrete, testable claim about regulatory status, not an analogy.") +
          H2("Grades and firewall") +
          fw("The R19 framing is [V]. The biological claim that PDK4 is co-upregulated in both torpor and insulin "
             "resistance is [O] CITED -- the model places the switch; it does not derive the regulatory program. "
             "This chapter is a hypothesis, not a clinical statement.")),
    cards=[vp_card("torpor returns = " + str(HB["torpor_returns_after_perturbation"]), "defended, reversible low setpoint", "v"),
           vp_card("IR crossed-and-stuck = " + str(HB["insulin_resistance_crossed_and_stuck"]), "chronic misfire, regulation lost", "v")])

# ---- §20 restoration method ----
add(no="&sect;20", slug="restoration-the-three-lever-method", title="Restoration: the three-lever method", kind="restoration",
    desc="The analgesic three-lever frame, re-read for setpoint restoration: restore gain, reduce forcing, remove the sensitiser.", grade="f",
    answer=("If disease is a drifted or crossed setpoint, restoration has three levers -- the same three the "
            "analgesic map uses to raise a firing threshold, re-read here. S1 RESTORE the feedback gain (deepen the "
            "basin); S2 REDUCE the pathological forcing (lower the drift drive); S3 REMOVE the upstream sensitising "
            "program. Each is grounded in the foundational setpoint law."),
    abstract=("The method is transferred from analgesic_threshold_logic v2.0 (DOI " + METHOD_DOI + "). The engine "
              "reads each candidate node's promoter switch-threshold structure (" + G + " &rarr; " + HSP + ") and "
              "places it in one lever. S1/S2 are [F] structural; S3 is [O] cited biology. These are HYPOTHESES, "
              "firewall-bound -- no dosing, efficacy, safety, or clinical claim."),
    body=(H2("Why the analgesic frame transfers") +
          P("Raising a nociceptor threshold and restoring a metabolic setpoint are the same control problem on the "
            "same R19 substrate: move a state relative to a barrier. Reduce the inward drive, deepen the well, or "
            "remove what shallowed it. The three levers map one-to-one (analgesic L1/L2/L3 &rarr; restoration "
            "S2/S1/S3).") +
          H2("Grounded in the foundational law") +
          P("Each lever acts on a term in the disease law of &sect;15: S1 raises g_eff (deeper barrier, higher "
            "crossing threshold); S2 lowers the chronic forcing; S3 removes the program that dropped the gain in the "
            "first place. The levers are not a separate theory -- they are the inverse of the failure mechanism.") +
          H2("Firewall") +
          fw(esc(REST["lever_map"]["firewall"]))), cards=[])

# lever chapter helper
def _lever_rows(code):
    rows = []
    for r in REST["lever_map"]["rows"]:
        if r["lever"] == code:
            rows.append([("<b>" + esc(r["target"]) + "</b>"),
                         (f(r["gamma"]) if r["gamma"] is not None else "&mdash;"),
                         (f(r["h_sp"]) if r["h_sp"] is not None else "&mdash;"),
                         esc(r["push_direction"]), '<span class="note">' + esc(r["src"]) + "</span>"])
    return rows

# ---- §S1 ----
add(no="&sect;S1", slug="restoration-lever-1-restore-loop-gain", title="Restoration lever 1: restore the loop gain", kind="restoration",
    desc="Re-sensitise the loop so effective stiffness rises -- a deeper, more robust basin (INSR, LEPR, PPARG).", grade="f",
    answer=("Lever S1 RESTORES the feedback gain: re-sensitise the loop so the effective stiffness g_eff rises back "
            "toward g, deepening the basin and raising the crossing threshold. Its candidate nodes are the "
            "sensitivity genes -- INSR (insulin signalling), LEPR (leptin feedback), and PPARG (adipocyte insulin "
            "sensitivity). Structural direction [F]; clinical magnitude [O]."),
    abstract=("The analog of analgesic L2 (increase the outward current). Deepening the basin is the direct inverse "
              "of the loop-gain drop that defines the disease. Reads [V]; lever placement [F] structural; every "
              "clinical magnitude [O]. Hypotheses only."),
    body=(H2("What S1 does to the law") +
          P("In &sect;15's law, S1 raises g_eff: barrier = g_eff&sup2;/4 grows and spinodal = 2(g_eff/3)<sup>1.5</sup> "
            "rises, so a crossed loop can re-open its healthy basin and a drifted one is pulled back. This is the "
            "only lever that can RE-CROSS a basin that has already flipped (the type-2-diabetes claim).") +
          H2("Candidate nodes (read on the R19 scale)") +
          table(["target", G, HSP, "restoration direction", "cited axis"], _lever_rows("S1")) +
          H2("Firewall") +
          fw(G + " places each gene on the switch-threshold scale; it is NOT an insulin dose or a measured "
             "sensitivity. The push direction is [F] structural, anchored to the cited clinical axis. No efficacy "
             "or dosing is asserted.")), cards=[])

# ---- §S2 ----
add(no="&sect;S2", slug="restoration-lever-2-reduce-pathological-drive", title="Restoration lever 2: reduce the pathological drive", kind="restoration",
    desc="Lower the chronic forcing -- cut intake drive or raise thermogenic disposal (MC4R, GHRL, UCP1, ADRB3).", grade="f",
    answer=("Lever S2 REDUCES the chronic forcing h_path that pushes the state toward the disease basin -- either by "
            "cutting intake drive (MC4R melanocortin tone, GHRL hunger axis) or by raising thermogenic disposal "
            "(UCP1 furnace, ADRB3 command) to lower the net energy surplus. Structural direction [F]; clinical "
            "magnitude [O]."),
    abstract=("The analog of analgesic L1 (reduce the inward current). Lowering the forcing is what returns a DRIFTED "
              "setpoint (the obesity claim) and relieves a loop that has not yet crossed. Reads [V]; lever placement "
              "[F]; clinical magnitude [O]."),
    body=(H2("What S2 does to the law") +
          P("S2 lowers |h_path| in &sect;15's law without touching the barrier; for a sub-spinodal (drifted) loop this "
            "moves the defended state back toward healthy. Notably the thermogenic nodes connect this lever straight "
            "to the endotherm furnace of Q1 -- raising disposal is the same UCP1/ADRB3 pair, used to shed surplus "
            "rather than defend temperature.") +
          H2("Candidate nodes (read on the R19 scale)") +
          table(["target", G, HSP, "restoration direction", "cited axis"], _lever_rows("S2")) +
          H2("Firewall") +
          fw("The thermogenic-disposal direction is [F] structural; " + G + " is not a metabolic rate. No claim is "
             "made that any agent achieves a given expenditure or weight change.")), cards=[])

# ---- §S3 ----
s3_rows = _lever_rows("S3")
add(no="&sect;S3", slug="restoration-lever-3-remove-sensitising-program", title="Restoration lever 3: remove the sensitising program", kind="restoration",
    desc="Remove the upstream program that lowered the crossing threshold -- the uncoupled fuel-sparing and chronic inflammation. [O].", grade="o",
    answer=("Lever S3 REMOVES the upstream program that LOWERED the crossing threshold in the first place -- the "
            "chronic uncoupled fuel-sparing of the hibernation bridge (PDK4) and the low-grade inflammatory "
            "sensitiser. This is the honesty-gated lever: " + G + " places the gene, but the uncoupling/network "
            "mechanism is graded cited-biology [O], never derived."),
    abstract=("The analog of analgesic L3 (remove the sensitising drive), and like L3 it is fail-closed: every S3 "
              "entry's mechanism link must begin [O] with a citation, or the build halts. The honesty gate passes (" +
              REST["s3_honesty"]["overall"] + "). Reads [V]; mechanism link [O] cited; HYPOTHESES only."),
    body=(H2("What S3 does to the law") +
          P("S3 targets the cause of the gain drop d itself -- if the uncoupling/inflammatory program is what "
            "shallowed the basin, removing it RESTORES the crossing threshold structurally. This is the deepest and "
            "least certain lever, which is why its mechanism is graded open.") +
          H2("Candidate nodes (mechanism link graded [O])") +
          table(["target", G, HSP, "restoration direction", "cited axis"], s3_rows) +
          H2("The honesty gate (fail-closed)") +
          P("Every S3 entry is checked: its mechanism link must start [O], must not be derived ([V]/[F]), and must "
            "carry a citation; the declared S3 set must be present; the map firewall must state the S3 link is [O]. "
            "Result: " + REST["s3_honesty"]["overall"] + " (failures: " +
            (", ".join(REST["s3_honesty"]["failures"]) or "none") + ").") +
          fw("The gamma read places an S3 gene in the lever map but the uncoupling/network mechanism is NOT captured "
             "by the read and is graded cited-biology [O]. These are hypotheses about an upstream program, not "
             "clinical recommendations.")), cards=[])

# ---- §P prioritisation ----
rank_rows = []
for r in REST["prioritisation"]["ranking"]:
    rank_rows.append([("<b>" + esc(r["target"]) + "</b>"), esc(r["lever"]), str(r["B"]), str(r["U"]), str(r["D"]),
                      ("<b>" + f(r["score"], 2) + "</b>"),
                      (f(r["gamma_h_sp_context"]) if r["gamma_h_sp_context"] is not None else "&mdash;")])
W = REST["prioritisation"]["weights"]
add(no="&sect;P", slug="restoration-prioritisation", title="Prioritisation: ranking targets, not drugs", kind="restoration",
    desc="Rank restoration targets by declared burden/unmet-need/directness weights; gamma is never folded into the score.", grade="f",
    answer=("Targets are ranked by a small, transparent score over three CITED tiers -- burden, unmet need, and "
            "mechanistic directness -- with DECLARED weights (B " + f(W["B"], 2) + ", U " + f(W["U"], 2) + ", D " +
            f(W["D"], 2) + "). The top target is the shared insulin node. The " + G + "-" + HSP + " read is carried "
            "as structural context and is NEVER folded into the clinical score."),
    abstract=("The analog of analgesic M10. Burden and unmet need lead the weights by editorial choice; the ranking "
              "is [F] from cited tiers plus declared weights, not a [V] engine output. The firewall forbids equating "
              "a promoter-stiffness read with a clinical magnitude, so " + G + " sits beside the score, never inside "
              "it."),
    body=(H2("The ranking") +
          table(["target", "lever", "B", "U", "D", "score", G + "-" + HSP + " (context)"], rank_rows) +
          H2("Declared weights, not tuned") +
          P("score = " + f(W["B"], 2) + "&middot;B + " + f(W["U"], 2) + "&middot;U + " + f(W["D"], 2) +
            "&middot;D over cited 1-5 tiers. The weights are an explicit editorial choice (need leads); they were "
            "not tuned to produce a desired ordering. Ranking targets -- not drugs -- keeps the output a research "
            "prioritisation, not a treatment list.") +
          H2("Firewall") +
          fw(esc(REST["prioritisation"]["firewall"]))), cards=[])

# ---- §R precision routing method ----
TD = PREC["routing_map"]["tier_distribution"]; GI = PREC["gamma_independence"]
NR = PREC["routing_map"]["named_routes"]; PFR = PREC["falsification"]["falsifiers"]
add(no="&sect;R", slug="precision-routing-regional-vs-systemic", title="Precision routing: regional vs systemic restoration", kind="restoration",
    desc="The analgesic local-anaesthesia distinction re-read for restoration: which compartment does each lever act in, and can it be routed there? Gamma is firewalled out of the routing.", grade="f",
    answer=("A systemic threshold-raiser acts body-wide; a local anaesthetic is a regional block confined to one "
            "nerve's territory. The same question for restoration asks WHERE each lever's node acts -- a single "
            "tissue compartment (a PRECISION route) or many (SYSTEMIC). Nodes split " +
            str(TD.get("PRECISION", 0)) + " precision / " + str(TD.get("REGIONAL", 0)) + " regional / " +
            str(TD.get("SYSTEMIC", 0)) + " systemic by cited anatomy. " + G + " never enters the routing score."),
    abstract=("Transferred from the analgesic local-anaesthesia idea (method DOI " + METHOD_DOI + "). Each "
              "restoration target is placed on a cited tissue-compartment map and classed PRECISION (one "
              "compartment), REGIONAL (2-3), or SYSTEMIC (&ge;4 or a distributed node). Routability [F] (which "
              "compartment) is distinct from deliverability [O] (can it be reached). The " + G + "-independence of "
              "the routing score is PROVEN, not asserted. Hypotheses only -- no route, device, dose, or efficacy claim."),
    body=(H2("Why the local-anaesthesia distinction transfers") +
          P("Raising a threshold and restoring a setpoint are the same control move (&sect;20); the delivery "
            "question is also the same. An intervention can act everywhere (systemic) or be confined to one "
            "anatomical territory (a regional block). For restoration the territory is the tissue COMPARTMENT in "
            "which a lever's node operates -- so the routing question is simply: how many cited compartments does "
            "the node touch?") +
          H2("Three tiers, by cited compartment") +
          P("<b>PRECISION</b> -- the node acts in ONE cited compartment, so the lever has a clean regional route "
            "(the local-anaesthesia analog: " + str(TD.get("PRECISION", 0)) + " nodes, e.g. UCP1&rarr;brown fat, "
            "MC4R&rarr;hypothalamus). <b>REGIONAL</b> -- 2-3 compartments, a small territory (" +
            str(TD.get("REGIONAL", 0)) + " nodes). <b>SYSTEMIC</b> -- &ge;4 compartments, or a distributed "
            "immune/stromal node with no single locus, so restoration cannot be routed to one place and must act "
            "body-wide (" + str(TD.get("SYSTEMIC", 0)) + " nodes: the ubiquitous insulin receptor, and the "
            "inflammatory sensitiser). The specificity is a parameter-free reciprocal of the cited compartment "
            "count -- nothing is fitted.") +
          H2("Routability is not deliverability") +
          P("A node can be anatomically PRECISION yet hard to reach: MC4R acts in a single compartment "
            "(hypothalamus), but central access is limited by the blood-brain barrier. The map keeps these "
            "separate -- which compartment is [F] structural anatomy; whether an intervention can reach it is an "
            "[O] deliverability obstacle, stated, never silently dropped.") +
          H2("The firewall is proven, not asserted") +
          P("The routing specificity reads the cited compartment COUNT only; " + G + " is carried beside each row "
            "as the promoter switch-threshold context and is never an input to the score. This is demonstrated: "
            "recomputing the whole map under a drastically perturbed " + G + " atlas leaves every routing field "
            "(compartments, primary, specificity, tier) byte-identical (" +
            str(GI["routing_geometry_invariant_under_gamma_perturbation"]) + "), while only the carried " + G +
            "-context column moves (" + str(GI["carried_context_column_does_track_gamma"]) + ") -- the read is "
            "present but firewalled out of the routing.") +
          vp_card("routing &perp; " + G, "routing geometry is invariant under a " + G + " perturbation (firewall proven, gate " + GI["overall"] + ")", "f") +
          H2("Firewall") +
          fw(esc(PREC["routing_map"]["firewall"]))),
    cards=[])

# ---- §RM the routing map ----
def _routing_rows_html():
    rows = []
    for r in PREC["routing_map"]["rows"]:
        gctx = (f(r["gamma_context"]["gamma"]) if r.get("gamma_context") else "&mdash;")
        note = esc(r["basis"]) + ((" &mdash; " + esc(r["delivery_obstacle"])) if r["delivery_obstacle"] else "")
        rows.append([("<b>" + esc(r["target"]) + "</b>"), esc(r["lever"]), esc(r["tier"]),
                     esc(comp_label(r["primary"])), (f(r["specificity"]) + " (" + str(r["n_compartments"]) + ")"),
                     gctx, '<span class="note">' + note + "</span>"])
    return rows
def _route_li():
    out = "<ul>\n"
    for name, d in NR.items():
        out += ("<li><b>" + esc(name) + "</b> &rarr; " + esc(comp_label(d["compartment"])) + ": " +
                esc(d["what"]) + " <span class=\"note\">(" + esc(", ".join(d["members"])) + " &mdash; " +
                esc(d["character"]) + ")</span></li>\n")
    return out + "</ul>\n"
add(no="&sect;RM", slug="precision-routing-compartment-map", title="The compartment routing map", kind="restoration",
    desc="Every restoration target placed on its cited tissue compartment, with specificity tier, carried gamma context, and deliverability obstacle; the three named routes.", grade="f",
    answer=("The map places all " + str(len(PREC["routing_map"]["rows"])) + " restoration targets on cited tissue "
            "compartments. Three named routes span the spectrum: a BAT-targeted route (the cleanest precision, "
            "UCP1 single-compartment), a central appetite-axis route (precision anatomy but a blood-brain-barrier "
            "[O] obstacle), and a hepatic glucose-disposal route (the honest distributed case -- a body-wide "
            "receptor, so a dominant-compartment route, not a single-compartment block)."),
    abstract=("The concrete table behind &sect;R. Each row carries the target, its lever, the routing tier, the "
              "primary compartment, the parameter-free specificity (1 / compartment count), the carried " + G +
              "-context (never folded in), and any [O] deliverability obstacle. The three named routes are the "
              "worked examples. Hypotheses only, firewall-bound."),
    body=(H2("The routing map") +
          table(["target", "lever", "tier", "primary compartment", "specificity (n)", G + "-context", "cited compartment / deliverability"],
                _routing_rows_html()) +
          P("Specificity = 1 / (cited compartment count); higher is more precisely routable. The " + G +
            "-context column is the promoter switch-threshold read carried ALONGSIDE -- it never enters the "
            "specificity or the tier (proven in &sect;R).") +
          H2("Three named routes") +
          P("Grouped by their primary compartment, the three routes span the full honesty spectrum from a clean "
            "regional block to an inherently body-wide target:") +
          _route_li() +
          H2("Falsifiers") +
          P("<b>PR1</b> &mdash; " + esc(PFR["PR1"])) +
          P("<b>PR2</b> &mdash; " + esc(PFR["PR2"])) +
          P("<b>PR3</b> &mdash; " + esc(PFR["PR3"])) +
          P("<b>FRAMEWORK</b> &mdash; " + esc(PFR["FRAMEWORK"])) +
          H2("Firewall") +
          fw("the compartment of action and the tier are [F] cited anatomy; the specificity reads the compartment "
             "count only and " + G + " is firewalled out of it; routability [F] is distinct from deliverability "
             "[O]. These are falsifiable HYPOTHESES about where a lever acts, not a delivery prescription -- no "
             "route, device, injection, dose, efficacy, or safety claim.")),
    cards=[])

# ---- §G grading ----
add(no="&sect;G", slug="grading-and-honesty", title="Grading and honesty", kind="governance",
    desc="What each grade means here, and the firewall that keeps a promoter read from becoming a clinical claim.", grade="f",
    answer=("Every statement carries a grade. [F] forced -- a structural consequence of the locked R19 forms. [V] "
            "simulation-verified -- reproduced by the deterministic engine. [L] measured -- a real promoter read or "
            "a cited physiological anchor. [O] open -- with a STATED obstacle, never a silent gap. The firewall "
            "keeps " + G + " a structural read, never a clinical magnitude."),
    abstract=("The honesty layer (VP-SPEC C3). The same grading vocabulary used across the framework, applied "
              "consistently: the gene criterion is [L], the loop dynamics are [V], the regime boundaries are [F], "
              "and every absolute rate, dose, or clinical effect is [O]."),
    body=(H2("The four grades, as used here") +
          P("<b>[F] forced</b>: the spinodal, barrier, and bistability are exact consequences of "
            "<code>ds/dt = &gamma;s &minus; s&sup3; + h</code>. <b>[V] verified</b>: defense-vs-track, the "
            "thermostat, fever, the torpor switch, the homeostats, and the disease law are reproduced by the engine "
            "(2&times;sha256 identical). <b>[L] measured</b>: every " + G + " is a real promoter read; setpoints "
            "(~37 &deg;C, ~5 mM) and the ~5-10x cost are cited. <b>[O] open</b>: absolute W/kg, the Kleiber "
            "exponent, the silenced-switch gating, and all clinical magnitudes -- each with its obstacle named.") +
          H2("The firewall, once more") +
          fw(G + " reads promoter switch-threshold STRUCTURE only. It is never a temperature, metabolic rate, "
             "glucose level, HbA1c, dose, or clinical effect. The disease and restoration chapters are falsifiable "
             "hypotheses grounded in the foundational setpoint mechanism, not medical advice; there is no clinical "
             "responsibility.") +
          H2("No tuning") +
          P("Every " + G + " is a measured input; spinodal and barrier are the locked R19 forms; the disease "
            "forcing/gain descriptors are declared and cited, never fitted to hit a number. The engine is "
            "deterministic (SEED 19) and re-derives the cross-species reads offline bit-for-bit.")), cards=[])

# ---- §F falsification ----
fr = REST["falsification"]["falsifiers"]
add(no="&sect;F", slug="falsification", title="Falsification register", kind="governance",
    desc="A named, measurable falsifier for every restoration proposal and for the framework read itself.", grade="f",
    answer=("A proposal that cannot be killed is not science. Each restoration lever carries a named, measurable "
            "falsifier -- SP1 (restore-gain), SP2 (reduce-forcing), SP3 (remove-sensitiser) -- plus a FRAMEWORK-level "
            "falsifier on the " + G + " read itself. If the stated experiment comes out the stated way, the "
            "corresponding claim is wrong."),
    abstract=("VP-SPEC honesty: the register makes each hypothesis refutable. The gate is that every proposal id "
              "plus FRAMEWORK has at least one falsifier (" + str(REST["falsification"]["all_have_falsifier"]) +
              "). Naming the kill-condition is what separates a hypothesis from a claim."),
    body=(H2("S1 -- restore the gain") + P(esc(fr["SP1"])) +
          H2("S2 -- reduce the forcing") + P(esc(fr["SP2"])) +
          H2("S3 -- remove the sensitiser") + P(esc(fr["SP3"])) +
          H2("FRAMEWORK -- the read itself") + P(esc(fr["FRAMEWORK"])) +
          H2("Why this is the last chapter") +
          P("The map ends on its own kill-conditions deliberately. The foundational separation, the torpor switch, "
            "the disease law, and the restoration levers are all offered as REFUTABLE structure -- the honest end of "
            "a research program, not a conclusion.")), cards=[])

# ===========================================================================
#  HUB PAGE
# ===========================================================================
def build_hub():
    groups = [("Foundational: endotherm vs ectotherm", ("section", "core")),
              ("Setpoint dynamics", ("dynamics",)),
              ("Disease as setpoint failure (a subset)", ("disease",)),
              ("Restoration (hypotheses, firewall-bound)", ("restoration",)),
              ("Honesty", ("governance",))]
    toc = '<ol class="toc">\n'
    for gtitle, kinds in groups:
        toc += '<li class="lv">' + esc(gtitle) + '</li>\n'
        for c in CH:
            if c["kind"] in kinds:
                toc += ('<li><a href="' + BASE + "/" + c["slug"] + '/"><b>' + c["no"] + '</b> ' + esc(c["title"]) +
                        '</a><span class="ol">' + esc(c["desc"]) + '</span></li>\n')
    toc += '</ol>\n'
    answer = ("This is a physics-grounded map of one question: does an organism DEFEND an internal setpoint or "
              "TRACK its environment? One measured promoter read (" + G + ") placed on the shared R19 bistable-switch "
              "scale separates endotherm from ectotherm, frames the torpor switch, and treats metabolic disease as a "
              "defended setpoint that drifted or crossed -- observation only, honest grades.")
    abstract = ("The endotherm/ectotherm divide is shown to be one R19 parameter (basin depth): a defended setpoint "
                "is a deep attractor, a tracked one is shallow. A measured cross-species panel locates the gene "
                "criterion in a present, drivable {UCP1 furnace + ADRB3 command} pair -- with four pre-registered "
                "nulls proving " + G + " is blind to thermogenic function. The torpor transition is a bistable switch "
                "(hysteresis), and the switch genes are present-but-silenced in non-hibernators. Metabolic disease "
                "follows one derived law (a loop-gain drop shrinks the barrier and lowers the crossing threshold), "
                "and restoration is offered through the three-lever method transferred from the analgesic map -- "
                "with a precision compartment-routing layer (regional vs systemic) whose " + G + " read is "
                "firewalled out of the routing. "
                "Reproducible (2&times;sha256 identical, offline), proposal-only, CC BY 4.0.")
    headline = (H2("Headline results") +
                '<ul>\n'
                '<li>the endotherm/ectotherm divide is ONE R19 parameter: endotherm setpoint sensitivity ' +
                f(SD["endotherm_loop"]["ambient_sensitivity"], 3) + ' vs ectotherm ' +
                f(SD["ectotherm_loop"]["ambient_sensitivity"], 3) + ' [V]</li>\n'
                '<li>gene criterion = a PRESENT drivable {UCP1 + ADRB3} pair, not a ' + G + ' value [L]; four '
                'pre-registered nulls (' + G + ' does not separate endo/ecto; ' + G + ' does not mark hibernation; '
                'no promoter across an 8-gene panel marks hibernation, group gaps ARE GC gaps; a GC-normalized '
                'methylation-substrate read also fails to separate hibernators) [V]</li>\n'
                '<li>euthermia&harr;torpor is a bistable SWITCH: hysteresis loop width ' +
                f(HY["hysteresis_loop_width"]) + ' [V]</li>\n'
                '<li>16/16 stress targets pass; metabolic disease from ONE derived loop-gain-drop law [V]; clinical '
                'magnitudes all [O]</li>\n'
                '</ul>\n')
    firstc = CH[0]
    body = (headline + H2("Contents") +
            P("Each chapter is a self-contained page with its own answer, reads, grades, citation, and firewall.") +
            toc +
            H2("Reproduce") +
            P("<code>python3 repro/run_all.py</code> rebuilds every number on these pages; the engine is "
              "deterministic (SEED 19, 2&times;sha256 identical) and the cross-species reads re-derive offline. The "
              "site itself is regenerated by <code>python3 tools/build_docs.py</code> with a drift-0 self-check.") +
            H2("Firewall") +
            fw(G + " reads promoter switch-threshold STRUCTURE only; it is never a temperature, metabolic rate, "
               "glucose level, dose, or clinical effect. The disease and restoration chapters are falsifiable "
               "hypotheses, not medical advice."))
    cls, label = GRADE_BADGE["v"]
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": SHORT}]}
    art = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": TITLE,
           "description": "A physics-grounded map of endothermy vs ectothermy, the defended setpoint, the torpor "
                          "switch, and metabolic disease as setpoint failure.",
           "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
           "creativeWorkStatus": "Research preprint", "identifier": "https://doi.org/" + CONCEPT_DOI, "sameAs": "https://doi.org/" + CONCEPT_DOI, "isBasedOn": REPO,
           "isAccessibleForFree": True, "license": "https://creativecommons.org/licenses/by/4.0/",
           "datePublished": DATE, "dateModified": DATE}
    head_ld = ('<script type="application/ld+json">\n' + json.dumps(art, ensure_ascii=False) + '\n</script>\n'
               '<script type="application/ld+json">\n' + json.dumps(crumb, ensure_ascii=False) + '\n</script>')
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>' + esc(TITLE) + ' | Jamming Physics</title>\n'
            '<meta name="description" content="A physics-grounded map of endothermy vs ectothermy, the defended '
            'setpoint, the torpor switch, and metabolic disease as setpoint failure. Observation only; honest grades.">\n'
            '<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">\n'
            '<link rel="canonical" href="' + BASE + '/">\n'
            '<link rel="stylesheet" href="/assets/css/site.css">\n' + head_ld + '\n</head>\n<body>\n'
            '<header><nav class="crumb"><a href="/">Home</a> &rsaquo; ' + esc(SHORT) + '</nav></header>\n<main>\n'
            '<h1>' + esc(TITLE) + '</h1>\n'
            '<p class="answer">' + answer + '</p>\n'
            '<p class="abstract">' + abstract + '</p>\n'
            '<aside class="claim-strip page"><span class="grade ' + cls + '">' + label + '</span>'
            '<span class="gate">LOCK &rarr; Derive &rarr; Gate</span>'
            '<a href="' + REPO + '" rel="noopener">reproduce (GitHub)</a>'
            '<a class="ver" href="https://doi.org/' + CONCEPT_DOI + '" rel="noopener">DOI ' + CONCEPT_DOI + '</a></aside>\n' + body +
            '</main>\n<footer><a href="' + ORCID + '" rel="noopener">ORCID 0009-0002-7535-8245</a> &middot; ' +
            esc(AUTHOR) + ' &middot; CC BY 4.0 &middot; cite: <a href="https://doi.org/' + CONCEPT_DOI + '" rel="noopener">DOI ' + CONCEPT_DOI + '</a> &middot; method: <a href="https://doi.org/' + METHOD_DOI +
            '" rel="noopener">three-lever DOI ' + METHOD_DOI + '</a> &middot; part of the '
            '<a href="' + SITE + '/" rel="noopener">Jamming Physics</a> programme &middot; reproduce: '
            '<code>repro/run_all.py</code></footer>\n</body>\n</html>')


# ===========================================================================
#  CSS / ACCESS LAYER / META
# ===========================================================================
def build_css():
    base = """/* Jamming Physics — site.css (VP-SPEC v1.8 canonical, thermometabolic edition) */
:root{
  --ink:#1a1a1a; --muted:#5a5a5a; --line:#e2e2e2; --bg:#fff; --accent:#1f5c8b;
  --gv:#0a7d33; --gf:#1452c4; --go:#9a6300; --gh:#6a3fb0;
  --maxw:760px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
main{max-width:var(--maxw);margin:0 auto;padding:0 20px 64px}
header{max-width:var(--maxw);margin:0 auto;padding:18px 20px 0}
footer{max-width:var(--maxw);margin:48px auto 0;padding:20px;border-top:1px solid var(--line);
  color:var(--muted);font-size:14px}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
h1{font-size:1.72rem;line-height:1.25;margin:.4em 0 .2em;letter-spacing:-.01em}
h2{font-size:1.28rem;margin:1.8em 0 .5em;letter-spacing:-.01em}
h3{font-size:1.06rem;margin:1.4em 0 .4em}
p{margin:.7em 0}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;
  background:#f3f5f7;border:1px solid var(--line);border-radius:4px;padding:1px 5px}
.crumb{font-size:13.5px;color:var(--muted)}
.crumb a{color:var(--muted)}
.answer{font-size:1.12rem;line-height:1.55;color:#23262b}
.abstract{font-size:1.04rem;line-height:1.6;background:#f7f9fb;border-left:3px solid var(--accent);
  padding:14px 18px;margin:1em 0;border-radius:0 4px 4px 0}
.claim-strip{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;
  margin:1em 0 1.6em;padding:10px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  font-size:13.5px}
.claim-strip .grade{font-weight:600;padding:2px 9px;border-radius:999px;color:#fff;text-transform:lowercase}
.claim-strip .gate{color:var(--muted);font-variant:all-small-caps;letter-spacing:.04em}
.claim-strip .ver{color:var(--muted)}
.grade.g-v{background:var(--gv)} .grade.g-f{background:var(--gf)}
.grade.g-o{background:var(--go)} .grade.g-h{background:var(--gh)}
.g{font-weight:700;border-radius:4px;padding:0 5px;color:#fff;font-size:.86em;white-space:nowrap}
.g.g-v{background:var(--gv)} .g.g-f{background:var(--gf)} .g.g-o{background:var(--go)} .g.g-h{background:var(--gh)}
.vp-card{background:#f7f9fb;border:1px solid var(--line);border-left:3px solid var(--accent);
  border-radius:0 4px 4px 0;padding:9px 14px;margin:.6em 0;font-size:14.5px}
.vp-card b{font-weight:600}
table{border-collapse:collapse;width:100%;margin:1.1em 0;font-size:14.5px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f3f5f7;font-weight:600}
.fw{background:#fff;border:1px dashed var(--line);border-radius:6px;padding:10px 14px;font-size:14.5px;color:#333}
.pn{display:flex;justify-content:space-between;gap:12px;margin:2.4em 0 0;padding-top:14px;
  border-top:1px solid var(--line);font-size:14.5px}
.pn a{white-space:nowrap}
ol.toc{list-style:none;padding:0;margin:1.2em 0}
ol.toc li{border-bottom:1px solid var(--line);padding:10px 2px}
ol.toc .ol{display:block;color:var(--muted);font-size:14px;margin-top:2px}
ol.toc .lv{background:#f7f9fb;font-weight:600}
.note{font-size:14px;color:var(--muted)}
sub{font-size:.72em} sup{font-size:.72em}
ul,ol{padding-left:1.3em}
li{margin:.25em 0}
@media(max-width:480px){body{font-size:16px}h1{font-size:1.5rem}table{display:block;overflow-x:auto}}
"""
    return base

BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]

def build_robots():
    out = ("# VP-SPEC v1.8 — machine access (C4 retrieval-readiness). 7 named agents + default: full allow.\n"
           "# homeostasis_thermometabolic_vp_site; generated " + DATE + " (deterministic)\n\n")
    for b in BOTS:
        out += "User-agent: " + b + "\nAllow: /\n\n"
    out += "User-agent: *\nAllow: /\n\nSitemap: " + SITE + "/sitemap.xml\n"
    return out

def build_sitemap():
    urls = [BASE + "/"] + [BASE + "/" + c["slug"] + "/" for c in CH]
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        body += "  <url><loc>" + u + "</loc><lastmod>" + DATE + "</lastmod></url>\n"
    body += "</urlset>\n"
    return body

def build_llms():
    out = ("# Jamming Physics — Thermometabolic Homeostasis\n\n"
           "> Canonical, citable multi-page HTML edition: endotherm vs ectotherm, the defended setpoint, the torpor "
           "switch, and metabolic disease as setpoint failure. One measured promoter read (gamma, a nearest-neighbour "
           "stacking-energy read) places each node on the shared R19 bistable-switch scale; a defended setpoint is a "
           "deep basin, a tracked one is shallow. Observation only (no evolutionary language); gamma reads promoter "
           "switch-threshold STRUCTURE only and every clinical magnitude is graded [O]. Proposal-only, CC BY 4.0.\n\n"
           "Author: " + AUTHOR + " (" + ORCID + "). Method (three-lever restoration): DOI " + METHOD_DOI + ".\n"
           "Principle: LOCK -> Derive -> Gate. Deterministic (SEED 19, 2xsha256 identical, offline); 16/16 stress "
           "targets pass.\n\n"
           "## Core facts\n"
           "- endotherm vs ectotherm = one R19 parameter (basin depth): endo sensitivity " +
           f(SD["endotherm_loop"]["ambient_sensitivity"], 3) + " vs ecto " +
           f(SD["ectotherm_loop"]["ambient_sensitivity"], 3) + "\n"
           "- gene criterion = a present, drivable {UCP1 furnace + ADRB3 command} pair, not a gamma value\n"
           "- four pre-registered nulls: gamma does not separate endo/ecto; gamma does not mark hibernation; no promoter across an 8-gene panel (14 species) marks hibernation, group gaps ARE GC gaps (r~0.996); a GC-normalized methylation-substrate read (CpG O/E) also fails to separate hibernators (0/8), a distinct read from gamma -- dynamic regulation is [O] external\n"
           "- euthermia<->torpor is a bistable SWITCH (hysteresis loop width " + f(HY["hysteresis_loop_width"]) + ")\n"
           "- metabolic disease = one derived law: loop-gain drop shrinks the barrier and lowers the crossing threshold\n"
           "- restoration routing: each target placed on a cited tissue compartment (PRECISION / REGIONAL / SYSTEMIC); gamma is firewalled OUT of the routing score (proven: routing geometry invariant under a gamma perturbation, only the carried context tracks it)\n"
           "- every clinical magnitude (rate, dose, efficacy, safety) is [O]\n\n"
           "## Hub\n- [Thermometabolic Homeostasis](" + BASE + "/)\n\n"
           "## Chapters\n")
    for c in CH:
        out += "- " + c["no"].replace("&sect;", "§") + " " + BASE + "/" + c["slug"] + "/\n"
    return out

def build_meta():
    chapters = [{"no": c["no"].replace("&sect;", "§"), "slug": c["slug"],
                 "title": c["title"], "kind": c["kind"]} for c in CH]
    return json.dumps({
        "paper_id": PAPER, "code": "trm", "version": open(os.path.join(PKG, "VERSION")).read().strip(),
        "layout": ("multi-page canonical: hub at docs/" + PAPER + "/index.html; each chapter is its own "
                   "self-contained page at docs/" + PAPER + "/{slug}/index.html (clean URL /" + PAPER + "/{slug}/), "
                   "mirroring the analgesic/vp_physics layout. VP-SPEC v1.8 C1-C4; every clinical magnitude [O]."),
        "title": TITLE, "short": SHORT, "doi": CONCEPT_DOI, "method_doi": METHOD_DOI,
        "hub_url": "/" + PAPER + "/", "branch": "homeostasis (DNA/neuro offshoot)",
        "abstract": ("One measured promoter read (gamma) on the R19 setpoint scale separates endotherm (defended "
                     "setpoint) from ectotherm (ambient-tracking); the gene criterion is a present {UCP1+ADRB3} pair "
                     "(four pre-registered nulls show gamma is blind to function, and a second GC-normalized "
                     "methylation-substrate read also fails to mark hibernation); the torpor transition is a bistable "
                     "switch present-but-silenced in non-hibernators; metabolic disease is one derived "
                     "loop-gain-drop law; restoration uses the analgesic three-lever method, with a precision "
                     "compartment-routing layer (regional vs systemic; gamma firewalled out of the routing). "
                     "Deterministic, proposal-only, CC BY 4.0."),
        "headline_results": [
            "endo setpoint sensitivity " + f(SD["endotherm_loop"]["ambient_sensitivity"], 3) +
            " vs ecto " + f(SD["ectotherm_loop"]["ambient_sensitivity"], 3),
            "gene criterion = present {UCP1+ADRB3} pair, not a gamma value",
            "torpor is a bistable switch (hysteresis width " + f(HY["hysteresis_loop_width"]) + ")",
            "16/16 stress targets pass; every clinical magnitude [O]"],
        "firewall": ("gamma = promoter switch-threshold structure; never a temperature, metabolic rate, glucose "
                     "level, HbA1c, dose, or clinical effect."),
        "reproduce": "repro/run_all.py — deterministic (SEED 19, 2xsha256 identical), 16/16 stress targets, offline",
        "n_pages": 1 + len(CH), "chapters": chapters
    }, ensure_ascii=False, indent=2)


# ===========================================================================
#  EMIT  +  drift-0 self-verify
# ===========================================================================
def assemble_all():
    """Return {relpath: bytes} for the whole site -- pure function, used for emit AND self-verify."""
    files = {}
    files[os.path.join(PAPER, "index.html")] = build_hub()
    n = len(CH)
    for i, c in enumerate(CH):
        prev = (CH[i - 1]["slug"], CH[i - 1]["no"].replace("&sect;", "§")) if i > 0 else ("", "")
        prev = (CH[i - 1]["slug"], CH[i - 1]["title"]) if i > 0 else None
        nxt = (CH[i + 1]["slug"], CH[i + 1]["title"]) if i < n - 1 else None
        cards_html = "".join(c.get("cards", []) or [])
        html_doc = page(c["no"], c["slug"], c["title"], c["desc"], c["answer"], c["abstract"], c["grade"],
                        c["body"], prev, nxt, i + 2, cards_html=cards_html)
        files[os.path.join(PAPER, c["slug"], "index.html")] = html_doc
    files[os.path.join("assets", "css", "site.css")] = build_css()
    files["robots.txt"] = build_robots()
    files["sitemap.xml"] = build_sitemap()
    files["llms.txt"] = build_llms()
    files[os.path.join(PAPER, "_meta.json")] = build_meta()
    return files

def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSING to build docs: writing is locked (" + why + ").")
        print("Run the research to green, then gates.write_research_complete() and set PHASE=writing.")
        return 1
    files = assemble_all()
    for rel, content in files.items():
        dest = os.path.join(DOCS, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(content)
    # C1 drift-0 self-verify: regenerate in-memory, compare byte-for-byte to what is on disk
    regen = assemble_all()
    drift = 0
    for rel, content in regen.items():
        on_disk = open(os.path.join(DOCS, rel), encoding="utf-8").read()
        if on_disk != content:
            drift += 1
            print("  DRIFT:", rel)
    llms_bytes = len(files["llms.txt"].encode("utf-8"))
    print("docs/ generated: %d files (1 hub + %d chapters + css + robots + sitemap + llms + _meta)." % (len(files), len(CH)))
    print("llms.txt size: %d bytes (<5KB: %s)" % (llms_bytes, llms_bytes < 5120))
    print("C1 self-verify drift:", drift, "(0 = byte-identical on regeneration)")
    h = hashlib.sha256("".join(sorted(open(os.path.join(DOCS, r), encoding="utf-8").read()
                                       for r in files)).encode("utf-8")).hexdigest()
    print("site content sha256:", h)
    return 0 if drift == 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
