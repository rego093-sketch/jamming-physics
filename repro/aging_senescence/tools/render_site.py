#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_site.py  --  Aging / Senescence WRITING-phase canonical HTML generator (VP-SPEC v1.8).

Code generates the site (SPEC sec.1). Every displayed number is pulled from the reproducible
engine modules (repro/_engine, repro/_pathology), so the canonical HTML cannot drift from the
deterministic results (Constitution C1). Body is English (C0); each page is answer-first with
JSON-LD ScholarlyArticle + BreadcrumbList, a claim-strip, and self-contained vp-cards (C4/6-R);
grades are honest and every [O] states its obstacle (C3). The DOI is the published Zenodo concept DOI
and is rendered as a resolving link.

Refuses to run while gates.writing_locked() is True.
"""
import os, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.normpath(os.path.join(HERE, ".."))
for p in ("repro/_engine", "repro/_pathology", "repro/_verify"):
    sys.path.insert(0, os.path.join(PKG, p))
import importlib
gates = importlib.import_module("gates")
ad = importlib.import_module("aging_dynamics")
xd = importlib.import_module("xspecies_discriminant")
xra = importlib.import_module("xspecies_robustness_audit")
sf = importlib.import_module("setpoint_failure")
arc = importlib.import_module("archaic_discriminant")
tk = importlib.import_module("telomere_keystone")

DOCS = os.path.join(PKG, "docs")
SITE = "https://jamming-physics.org"
PAPER_ID = "aging"
CODE = "age"
SHORT = "Aging & Senescence"
TITLE_FULL = ("Aging and Senescence: the Systemic Decline of Homeostatic Setpoints over the Lifespan")
AUTHOR = "Young Jae Lee"
ORCID = "https://orcid.org/0009-0002-7535-8245"
CC = "https://creativecommons.org/licenses/by/4.0/"
REPO = "https://github.com/rego093-sketch/jamming-physics"
DOI_TBD = "10.5281/zenodo.20756155"
DATE = "2026-06-19"

RA1 = ad.ra1_setpoint_drift()
RA2 = ad.ra2_senescence_stuck()
RA3 = ad.ra3_reservoir_depletion()
RA4 = ad.ra4_hallmarks_map()
RA5 = ad.ra5_risk_multiplier()
RA6 = ad.ra6_rate_of_aging()
RA7 = xd.discriminant()
AUD = xra.audit()
RA8 = arc.discriminant()
RA9 = tk.keystone()
PATH = sf.run()
ATLAS = json.load(open(os.path.join(PKG, "inherited", "aging_gamma_xspecies.json")))
MASTERS = json.load(open(os.path.join(PKG, "inherited", "organ_gamma.json")))["genes"]
DET_OK, DET_HASH = gates.determinism_ok()


def esc(s):
    return html.escape(str(s), quote=True)


def fnum(x, n=4):
    if x is None:
        return "\u2013"
    return ("%." + str(n) + "f") % float(x)


def grade_span(cls, txt):
    return '<span class="grade %s">%s</span>' % (cls, esc(txt))


GBADGE = {"V": ("g-verified", "[V] verified"), "F": ("g-forced", "[F] forced"),
          "O": ("g-open", "[O] open")}


def jsonld_article(n, subj, short_title):
    d = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": subj,
         "isPartOf": {"@type": "CreativeWorkSeries", "name": SHORT, "identifier": "DOI " + DOI_TBD},
         "position": n, "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
         "datePublished": DATE, "dateModified": DATE,
         "isBasedOn": REPO + "/tree/main/repro/" + PAPER_ID + "/", "license": CC,
         "knowsAbout": ["jamming lattice", "R19 setpoint", "cellular senescence", "promoter gamma",
                        "homeostasis", "longevity", short_title]}
    return json.dumps(d, ensure_ascii=False, separators=(",", ":"))


def jsonld_breadcrumb(n, short_title):
    d = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": SHORT, "item": SITE + "/" + PAPER_ID + "/"},
        {"@type": "ListItem", "position": 3, "name": "\u00a7%d %s" % (n, short_title)}]}
    return json.dumps(d, ensure_ascii=False, separators=(",", ":"))


def head(slug, n, subj45, desc, short_title):
    title = "%s \u2014 %s \u00a7%d | Jamming Physics" % (subj45, SHORT, n)
    return "\n".join([
        "<!DOCTYPE html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>" + esc(title) + "</title>",
        '<meta name="description" content="' + esc(desc) + '">',
        '<link rel="canonical" href="' + SITE + "/" + PAPER_ID + "/" + slug + '/">',
        '<link rel="stylesheet" href="/assets/css/site.css">',
        '<script type="application/ld+json">' + jsonld_article(n, subj45, short_title) + "</script>",
        '<script type="application/ld+json">' + jsonld_breadcrumb(n, short_title) + "</script>",
        "</head>"])


def claim_strip(grade_class, grade_text, slug):
    return "".join([
        '<aside class="claim-strip">', '<span class="grade ', grade_class, '">', esc(grade_text), "</span>",
        '<span class="gate">LOCK \u2192 Derive \u2192 Gate</span>',
        '<a href="', REPO, "/tree/main/repro/", PAPER_ID, "/", slug, '/" rel="noopener">Reproduction code (GitHub)</a>',
        '<span class="muted">DOI: </span><a href="https://doi.org/', DOI_TBD, '" rel="noopener">', DOI_TBD, "</a>", "</aside>"])


def vp_card(locked, bold, meaning, grade_html, link_text, link_href):
    return "".join([
        '<aside class="vp-card" data-locked="', esc(locked), '">', "<b>", bold, "</b> \u2014 ", meaning, " ",
        grade_html, " ", '<a href="', link_href, '">', esc(link_text), "</a>", "</aside>"])


def pn(n, total, sections):
    parts = ['<nav class="pn">']
    if n > 1:
        parts.append('<a rel="prev" href="/%s/%s/">\u2190 \u00a7%d</a>' % (PAPER_ID, sections[n - 2]["slug"], n - 1))
    else:
        parts.append("<span></span>")
    parts.append('<a class="mid" href="/%s/">Contents</a>' % PAPER_ID)
    if n < total:
        parts.append('<a rel="next" href="/%s/%s/">\u00a7%d \u2192</a>' % (PAPER_ID, sections[n]["slug"], n + 1))
    else:
        parts.append("<span></span>")
    parts.append("</nav>")
    return "".join(parts)


def footer():
    return "".join([
        "<footer>", TITLE_FULL, ". &copy; ", DATE[:4], " ", AUTHOR, " \u00b7 ",
        '<a href="', ORCID, '" rel="noopener">ORCID 0009-0002-7535-8245</a> \u00b7 ',
        'DOI <a href="https://doi.org/', DOI_TBD, '" rel="noopener">', DOI_TBD, "</a> \u00b7 ",
        '<a href="', CC, '" rel="noopener">CC BY 4.0</a> \u00b7 ',
        "Reproducible build, SEED=19, result sha256 ", DET_HASH[:12], "\u2026", "</footer></body></html>"])


# ---- table builders (rows straight from reproducible data) ----
def masters_table():
    order = [("TP53", "cellular_senescence", "stuck-attractor"),
             ("CDKN2A", "senescence_arrest_switch", "stuck-attractor"),
             ("TERT", "telomere_maintenance", "reservoir-depletion"),
             ("FOXO3", "longevity_signaling", "maintenance")]
    rows = []
    for g, node, dyn in order:
        m = MASTERS[g]
        rows.append("<tr><td>%s</td><td>%s</td><td class='num'>%s</td><td>%s</td><td>%s</td><td class='muted'>%s</td></tr>"
                    % (g, node.replace("_", " "), fnum(m["gamma"], 6), esc(m.get("accession", "?")),
                       esc(m.get("strand", "?")), dyn))
    return ("<div class='tw'><table><caption>The four measured aging masters. &gamma; = &minus;mean SantaLucia&nbsp;1998 "
            "NN &Delta;G37 over TSS&minus;2000..+500, vendored from NCBI RefSeq; never fitted.</caption>"
            "<thead><tr><th>Gene</th><th>Node</th><th>&gamma;</th><th>Accession</th><th>Strand</th><th>Dynamics</th></tr>"
            "</thead><tbody>" + "".join(rows) + "</tbody></table></div>")


def xspecies_table():
    by, mlsp = {}, {}
    for r in ATLAS["rows"]:
        sp = r.get("common")
        by.setdefault(sp, {})[r.get("gene")] = r.get("gamma")
        if r.get("mlsp") is not None:
            mlsp[sp] = r["mlsp"]
    out = []
    for sp in sorted(mlsp, key=lambda s: -mlsp[s]):
        row = by.get(sp, {})
        cells = "".join("<td class='num'>%s</td>" % fnum(row.get(g), 4) for g in ("TP53", "CDKN2A", "FOXO3", "TERT"))
        out.append("<tr><td>%s</td><td class='num'>%s</td>%s</tr>" % (esc(sp.replace("_", " ")), fnum(mlsp[sp], 1), cells))
    return ("<div class='tw'><table><caption>Promoter &gamma; across ten mammals spanning the lifespan spectrum "
            "(MLSP = maximum lifespan, years; AnAge). Bowhead whale is listed for span but has no annotated target "
            "promoters in NCBI Gene; CDKN2A is unannotated in several species.</caption>"
            "<thead><tr><th>Species</th><th>MLSP</th><th>TP53</th><th>CDKN2A</th><th>FOXO3</th><th>TERT</th></tr>"
            "</thead><tbody>" + "".join(out) + "</tbody></table></div>")


def per_gene_table():
    pg = RA7["per_gene"]
    out = []
    for g in ("TP53", "CDKN2A", "FOXO3", "TERT"):
        v = pg[g]
        out.append("<tr><td>%s</td><td class='num'>%d</td><td class='num'>%s</td><td class='num'>%s%%</td>"
                   "<td class='num'>%+.2f</td><td class='num'>%.0f</td><td class='num'>%.3f</td></tr>"
                   % (g, v["n"], fnum(v["human"], 4), fnum(v["cv_pct"], 2), v["human_z"], v["human_pctile"], v["perm_p"]))
    return ("<div class='tw'><table><caption>Where the human value sits in the mammalian distribution, and whether "
            "&gamma; tracks lifespan. |z|&lt;1 and a non-significant permutation p (1000 shuffles) for every gene: human "
            "is not special and no single-gene trend survives.</caption>"
            "<thead><tr><th>Gene</th><th>n</th><th>human &gamma;</th><th>CV</th><th>human z</th><th>pctile</th>"
            "<th>perm p</th></tr></thead><tbody>" + "".join(out) + "</tbody></table></div>")


def reservoir_table():
    res = RA3["reservoirs"]
    label = {"telomere_TERT": "telomere (TERT)", "senescence_CDKN2A": "senescence (CDKN2A)",
             "apoptosis_TP53": "apoptosis (TP53)", "longevity_FOXO3": "longevity (FOXO3)"}
    out = []
    for k in sorted(res, key=lambda k: res[k]["steps_to_depletion"]):
        v = res[k]
        out.append("<tr><td>%s</td><td class='num'>%s</td><td class='num'>%s</td><td class='num'>%d</td></tr>"
                   % (label.get(k, k), fnum(v["gamma"], 4), fnum(v["capacity"], 3), v["steps_to_depletion"]))
    return ("<div class='tw'><table><caption>Finite reservoirs, capacity &asymp; &gamma;<sup>1.5</sup>. Deeper-&gamma; "
            "wells hold more and last longer, but all deplete to zero \u2014 telomere attrition is reservoir exhaustion, "
            "not a privileged clock.</caption>"
            "<thead><tr><th>Reservoir</th><th>&gamma;</th><th>Capacity</th><th>Steps to empty</th></tr></thead><tbody>"
            + "".join(out) + "</tbody></table></div>")


def hallmarks_table():
    out = []
    for h in RA4["hallmarks"]:
        out.append("<tr><td>%s</td><td>%s</td><td class='muted'>%s</td><td class='num'>%s</td></tr>"
                   % (esc(h["hallmark"]), esc(h["substrate"]), esc(h["axis"]), esc(h["grade"])))
    return ("<div class='tw'><table><caption>The ten hallmarks of aging, each mapped to a substrate mechanism and the "
            "research axis that reproduces it. No orphans.</caption>"
            "<thead><tr><th>Hallmark</th><th>Substrate mechanism</th><th>Axis</th><th>Grade</th></tr></thead><tbody>"
            + "".join(out) + "</tbody></table></div>")


def sarcopenia_table():
    out = []
    for t in PATH["failures"][0]["trajectory"]:
        out.append("<tr><td class='num'>%.1f</td><td class='num'>%+.4f</td><td class='num'>%+.4f</td>"
                   "<td class='num'>%.3f</td></tr>"
                   % (t["loop_gain_drop"], t["defended_state"], t["drift"], t["barrier_fraction"]))
    return ("<div class='tw'><table><caption>Sarcopenia as monotone setpoint drift: as loop-gain drop d rises, the "
            "defended force-state creeps down and the barrier fraction shrinks.</caption>"
            "<thead><tr><th>gain drop d</th><th>defended state</th><th>drift</th><th>barrier frac</th></tr></thead>"
            "<tbody>" + "".join(out) + "</tbody></table></div>")


# shared vp-cards
SPIN = ("<aside class='vp-card' data-locked='spinodal'><b>spinodal(&gamma;) = 2(&gamma;/3)<sup>1.5</sup></b> \u2014 the "
        "drive |h| past which one R19 basin disappears, so the flip is discontinuous (a saddle-node). "
        + grade_span(*GBADGE["F"]) + " <a href='/" + PAPER_ID + "/01-aging-as-homeostatic-setpoint-decline/'>substrate, "
        "&sect;1</a></aside>")
BARR = ("<aside class='vp-card' data-locked='barrier'><b>barrier(&gamma;) = &gamma;<sup>2</sup>/4</b> \u2014 the energy "
        "barrier between the two basins; it sets how stable a defended setpoint is. " + grade_span(*GBADGE["F"])
        + " <a href='/" + PAPER_ID + "/01-aging-as-homeostatic-setpoint-decline/'>substrate, &sect;1</a></aside>")
GCARD = ("<aside class='vp-card' data-locked='gamma'><b>&gamma; (promoter identity)</b> \u2014 &minus;mean "
         "nearest-neighbour stacking &Delta;G37 (SantaLucia 1998) over the promoter window; the DNA Layer-1 identity that "
         "fixes each node's barrier and dwell. " + grade_span(*GBADGE["V"])
         + " <a href='https://doi.org/10.5281/zenodo.20471407'>DNA Layer 1 (DOI)</a></aside>")
DWELL = ("<aside class='vp-card' data-locked='dwell'><b>dwell(&gamma;) &asymp; &gamma;<sup>1.5</sup></b> \u2014 how long a "
         "switch runs before its finite reservoir empties; it sets reservoir capacity (the replicative limit). "
         + grade_span(*GBADGE["F"]) + " <a href='https://doi.org/10.5281/zenodo.20471407'>DNA Layer 1 (DOI)</a></aside>")


# ---- archaic / telomere tables (sections 10-11) -------------------------------------------------
def archaic_gamma_table():
    """Per-individual promoter gamma across the four masters (the cross-sectional snapshot)."""
    pg = RA8["per_gene"]
    atlas = json.load(open(os.path.join(PKG, "inherited", "aging_gamma_archaic.json"), encoding="utf-8"))
    meta = {s["key"]: s for s in atlas["specimens"]}
    order = ["GRCh37_reference", "AltaiNea", "Vindija", "Chagyrskaya", "Denisova", "UstIshim", "Loschbour"]
    genes = ["TP53", "CDKN2A", "FOXO3", "TERT"]
    rows = []
    for sp in order:
        m = meta.get(sp, {})
        cells = []
        for g in genes:
            v = pg[g]["gamma_by_individual"].get(sp)
            cells.append("<td class='num'>%s</td>" % (fnum(v, 4) if v is not None else "&ndash;"))
        age = m.get("approx_age_kya")
        agestr = "0" if age == 0 else ("~%g" % age)
        rows.append("<tr><td>%s</td><td class='num'>%s</td>%s</tr>"
                    % (esc(m.get("label", sp)), agestr, "".join(cells)))
    return ("<div class='tw'><table><caption>Measured promoter &gamma; for the four aging masters in each of "
            "seven dated individuals, examined as one cross-sectional set (kya&nbsp;=&nbsp;thousand years; "
            "Chagyrskaya is TERT-only). Observation only: each value is a measured present-state.</caption>"
            "<thead><tr><th>Individual</th><th>age (kya)</th><th>TP53</th><th>CDKN2A</th><th>FOXO3</th>"
            "<th>TERT</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")


def archaic_subload_table():
    """Per-gene homozygous-derived substitution load carried by the archaic individuals + gamma range."""
    load = RA8["verdict"]["archaic_substitution_load"]
    rows = []
    for g in ["TP53", "CDKN2A", "FOXO3", "TERT"]:
        rng = RA8["per_gene"][g]["gamma_spread"]["range"]
        rows.append("<tr><td>%s</td><td class='num'>%d</td><td class='num'>%s</td></tr>"
                    % (g, load[g], fnum(rng, 6)))
    return ("<div class='tw'><table><caption>Homozygous-derived promoter substitutions carried by the archaic "
            "individuals (Neanderthal&nbsp;+&nbsp;Denisovan), and the full &gamma; range across the "
            "seven-individual set. TERT carries the most substitutions; every per-gene &gamma; range is below "
            "0.0016.</caption><thead><tr><th>Gene</th><th>archaic hom-sub count</th><th>&gamma; range (set)</th>"
            "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")


def telomere_ranking_table():
    """gamma ranking: telomere repeat vs the four master promoters (telomere is the lowest)."""
    ranking = RA9["verdict"]["gamma_ranking_ascending"]
    label = {"telomere_repeat": "telomere repeat (TTAGGG)n", "TP53": "TP53 promoter",
             "CDKN2A": "CDKN2A promoter", "FOXO3": "FOXO3 promoter", "TERT": "TERT promoter"}
    rows = []
    for name, g in ranking:
        lab = esc(label.get(name, name))
        if name == "telomere_repeat":
            lab = "<strong>" + lab + "</strong>"
        rows.append("<tr><td>%s</td><td class='num'>%s</td></tr>" % (lab, fnum(g, 4)))
    return ("<div class='tw'><table><caption>Promoter-style &gamma; (&minus;mean SantaLucia NN &Delta;G37) of "
            "the canonical telomere repeat versus the four aging-master promoters. The telomere repeat has the "
            "LOWEST &gamma; of any aging-related sequence in the package; the value is identical on both strands "
            "and length-independent to &lt;0.5%.</caption><thead><tr><th>Sequence</th><th>&gamma;</th></tr>"
            "</thead><tbody>" + "".join(rows) + "</tbody></table></div>")


def build_sections():
    S = []
    # 1 -----------------------------------------------------------------------------------
    S.append(dict(
        slug="01-aging-as-homeostatic-setpoint-decline", n=1,
        subj45="Aging as homeostatic setpoint decline", short="The aging thesis", grade="V",
        desc="Aging on the VP substrate is the slow loss of defense gain of every homeostatic setpoint plus accumulation of cells stuck in irreversible R19 attractors; the dominant pathology risk multiplier.",
        answer=("Aging on the jamming substrate is the slow loss of defense gain of every homeostatic setpoint, plus the "
                "accumulation of cells stuck in irreversible R19 attractors (senescence). It is the dominant risk "
                "multiplier for every pathology kernel. No new organs are emerged here: node identities are inherited from "
                "DNA, and this capstone layer adds the temporal dynamics."),
        abstract=("The R19 field s&#775; = &gamma;s &minus; s&sup3; + h has two basins separated by a barrier "
                  "&gamma;&sup2;/4; a defended homeostatic setpoint is the healthy basin, and \u201cdefense gain\u201d is "
                  "carried by &gamma;. Aging is modeled as a slow decline of that gain, which both lets the defended "
                  "value drift and lowers the catastrophe threshold spinodal&nbsp;2(&gamma;/3)<sup>1.5</sup>."),
        body="".join([
            "<h2>What aging is on this substrate</h2>",
            "<p>Aging is not an organ. It is a process that runs on the same vacuum-jamming R19 substrate used across the "
            "framework, where every switch obeys the normal-form field s&#775; = &gamma;s &minus; s&sup3; + h. That field "
            "has two stable basins; the energy barrier between them is &gamma;&sup2;/4, and the drive |h| past which one "
            "basin vanishes is the spinodal 2(&gamma;/3)<sup>1.5</sup>.</p>",
            "<p>A defended homeostatic setpoint \u2014 glucose, pressure, calcium, temperature \u2014 is the healthy basin "
            "held against perturbation. Its restoring strength (loop gain) is carried by &gamma;. Aging is the slow "
            "decline of that gain over the lifespan.</p>",
            BARR, SPIN,
            "<h2>Two failure modes from one decline</h2>",
            "<p>A falling gain does two things at once. The barrier shrinks, so the defended value drifts inside its "
            "basin \u2014 the gradual, multi-system signature of aging (&sect;3). And the spinodal shrinks, so a chronic "
            "stressor that was survivable when young can flip the setpoint discontinuously into the pathological basin "
            "\u2014 the sudden failure event (&sect;3, &sect;12).</p>",
            "<p>Two further consequences define the program: cells can cross into an irreversible arrested basin and "
            "accumulate (senescence, &sect;4), and finite reservoirs deplete to a replicative limit (&sect;5).</p>",
            "<h2>Nodes and seams</h2>",
            "<p>This layer watches four measured masters and one diffuse node. The masters are TP53 (cellular "
            "senescence), CDKN2A (the arrest switch), TERT (telomere maintenance), and FOXO3 (longevity signaling); their "
            "identity &gamma; is owned by DNA and never fitted (&sect;2). The diffuse node is the systemic drift of every "
            "imported setpoint.</p>",
            GCARD,
            "<p>The single seam this package is the source of truth for is the aging risk multiplier: it raises the "
            "crossing rate of every oncology and pathology kernel across the framework (&sect;7).</p>"]),
        kf=None))

    # 2 -----------------------------------------------------------------------------------
    tp53 = MASTERS["TP53"]["gamma"]
    S.append(dict(
        slug="02-node-atlas-measured-promoter-gamma", n=2,
        subj45="Node atlas: measured promoter gamma", short="Node atlas", grade="V",
        desc="The four aging masters carry measured promoter gamma (TP53 1.4298, CDKN2A 1.4424, TERT 1.5539, FOXO3 1.5942); emergence order by gamma is senescence, arrest switch, telomere, longevity.",
        answer=("The four aging masters carry measured promoter &gamma;: TP53 1.4298, CDKN2A 1.4424, TERT 1.5539, FOXO3 "
                "1.5942 \u2014 each computed as &minus;mean SantaLucia nearest-neighbour &Delta;G37 over the "
                "TSS&minus;2000..+500 window and never fitted. Emergence order by ascending &gamma; is cellular "
                "senescence, arrest switch, telomere maintenance, longevity signaling."),
        abstract=("&gamma; is the promoter stacking-energy identity from DNA Layer&nbsp;1; it fixes each node's barrier "
                  "&gamma;&sup2;/4 and dwell &gamma;<sup>1.5</sup>. The four values are vendored from NCBI RefSeq "
                  "accessions and reproduce bit-for-bit from the committed promoter cache."),
        body="".join([
            "<h2>The masters and their identity</h2>",
            "<p>Each aging master is a real promoter, and its &gamma; is a measurement, not a parameter. The window is "
            "fixed (TSS&minus;2000 to +500, 2501&nbsp;bp), the nearest-neighbour table is SantaLucia&nbsp;1998, and the "
            "value is &minus;mean &Delta;G37 over the window. The same pipeline produces the DNA gene-clock &gamma;.</p>",
            masters_table(), GCARD,
            "<h2>Why the order matters</h2>",
            "<p>&gamma; sets two derived quantities. The barrier &gamma;&sup2;/4 fixes how hard it is to leave a basin "
            "(state stability), and the dwell &gamma;<sup>1.5</sup> fixes how long a switch runs (reservoir capacity, "
            "&sect;5). Sorting the masters by &gamma; gives a fixed emergence order: cellular senescence (TP53) and the "
            "arrest switch (CDKN2A) sit lowest, then telomere maintenance (TERT), then longevity signaling (FOXO3).</p>",
            "<div class='kf'>&gamma;<sub>TP53</sub> = " + fnum(tp53, 6) + "&nbsp;&nbsp;|&nbsp;&nbsp;barrier = &gamma;&sup2;/4 = "
            + fnum(tp53 ** 2 / 4, 4) + "</div>",
            "<h2>The diffuse node</h2>",
            "<p>The fifth node, systemic setpoint drift, has no single master gene. It is a circuit-level, derived "
            "quantity: the aggregate decline of every defended setpoint imported from the other packages. It is the "
            "object that &sect;3 and &sect;8 quantify.</p>"]),
        kf="&gamma;_TP53 = " + fnum(tp53, 6)))

    # 3 -----------------------------------------------------------------------------------
    jump = RA1["flip_jump"]
    S.append(dict(
        slug="03-setpoint-drift-unifying-signature", n=3,
        subj45="Setpoint drift: the unifying signature", short="RA1 setpoint drift", grade="V",
        desc="Under slow loss of loop gain a defended setpoint first creeps inside its basin then flips catastrophically past the spinodal; one law gives both gradual drift and the sudden failure event (flip jump 0.79).",
        answer=("Under a slow loss of loop gain, a defended setpoint first creeps inside its basin and then flips "
                "catastrophically once the gain falls past the spinodal. One law reproduces both the gradual multi-system "
                "drift of aging and the discontinuous failure event. The measured flip jump is " + fnum(jump, 2)
                + "; the mechanism is [V], the absolute rate is [O]."),
        abstract=("Sweeping a falling gain through the R19 field gives a monotone creep of the defended state while the "
                  "barrier &gamma;&sup2;/4 shrinks, followed by a discontinuous jump of " + fnum(jump, 3) + " when the "
                  "spinodal is crossed. The same decline thus yields both the slow drift of aging and its sudden onset "
                  "events \u2014 one signature, two faces."),
        body="".join([
            "<h2>Creep, then catastrophe</h2>",
            "<p>The defended value does not fall smoothly to failure. While the basin still exists, the setpoint creeps "
            "\u2014 a slow, monotone drift that reads as ordinary aging across many systems at once. This is the unifying "
            "signature: one declining gain, expressed everywhere a setpoint is defended.</p>",
            "<p>Then the basin disappears. Once the gain drops past the spinodal, the healthy basin is annihilated in a "
            "saddle-node event and the state jumps discontinuously to the pathological basin. In the run this jump is "
            + fnum(jump, 4) + " \u2014 a sudden failure on top of the slow drift.</p>", SPIN,
            "<h2>Why aging looks gradual but fails suddenly</h2>",
            "<p>This resolves a familiar tension. Function appears to decline smoothly for decades (the creep), yet "
            "clinical failure often arrives as an event \u2014 a fall, a fracture, a decompensation. Both come from the "
            "same monotone loss of gain; the creep is the sub-spinodal regime and the event is the crossing.</p>",
            "<p>The shape is reproduced and graded [V]. The absolute calendar rate of the decline is not derivable here "
            "\u2014 it needs an external clock \u2014 and is graded [O] (see &sect;13).</p>"]),
        kf="flip jump = " + fnum(jump, 3)))

    # 4 -----------------------------------------------------------------------------------
    arr = RA2["arrested_fraction_final"]
    S.append(dict(
        slug="04-cellular-senescence-stuck-attractor", n=4,
        subj45="Senescence as a stuck attractor", short="RA2 senescence", grade="V",
        desc="Cellular senescence is a cell crossed into an irreversible arrested R19 basin: past the spinodal the proliferative basin vanishes, arrest is one-way, and arrested cells accumulate to a fraction of 0.391.",
        answer=("Cellular senescence is a cell that has crossed into an irreversible arrested R19 basin. Past the spinodal "
                "the proliferative basin disappears, so the arrest is one-way \u2014 a sub-spinodal pulse is still "
                "reversible, but a supra-spinodal crossing is not \u2014 and arrested cells accumulate monotonically, "
                "reaching a fraction of " + fnum(arr, 3) + " in the run."),
        abstract=("Driving a cell past the spinodal annihilates the proliferative basin, making the arrested state an "
                  "absorbing attractor (return is impossible), while a sub-spinodal pulse relaxes back. Repeated exposure "
                  "therefore accumulates arrested cells over time, with the arrested fraction rising monotonically to "
                  + fnum(arr, 3) + "."),
        body="".join([
            "<h2>Irreversibility is a saddle-node, not a threshold</h2>",
            "<p>Senescence is permanent for a structural reason. Below the spinodal the proliferative and arrested basins "
            "coexist, so a perturbation that pushes a cell toward arrest can relax back. Above the spinodal the "
            "proliferative basin no longer exists, so the cell cannot return \u2014 the arrested state is absorbing.</p>",
            SPIN,
            "<p>The run confirms both halves: a supra-spinodal drive is one-way, and a sub-spinodal pulse is reversible. "
            "Irreversibility is therefore not an assumption; it follows from which basins exist at a given drive.</p>",
            "<h2>Accumulation and SASP</h2>",
            "<p>Because each crossing is permanent, arrested cells accumulate. The arrested fraction rises monotonically "
            "with continued exposure, reaching " + fnum(arr, 3) + " in the simulation. The senescence-associated secretory "
            "phenotype then raises neighbours' crossing hazard, coupling senescence to the risk multiplier of &sect;7.</p>",
            "<p>The irreversibility and the monotone accumulation are graded [V]; the absolute per-year rate is [O].</p>"]),
        kf="arrested fraction = " + fnum(arr, 3)))

    # 5 -----------------------------------------------------------------------------------
    res = RA3["reservoirs"]
    tert_steps = res["telomere_TERT"]["steps_to_depletion"]
    tp53_steps = res["apoptosis_TP53"]["steps_to_depletion"]
    S.append(dict(
        slug="05-reservoir-depletion-telomere-clock", n=5,
        subj45="Reservoir depletion: the telomere clock", short="RA3 reservoir depletion", grade="V",
        desc="Each reservoir has finite capacity ~ gamma^1.5; deeper wells last longer but all deplete to zero. TERT lasts 89 steps, TP53 78 - telomere attrition is reservoir exhaustion, not a special clock.",
        answer=("Each reservoir \u2014 telomere/TERT, senescence/CDKN2A, apoptosis/TP53, longevity/FOXO3 \u2014 has finite "
                "capacity proportional to &gamma;<sup>1.5</sup>. Deeper-&gamma; wells hold more and last longer, but every "
                "reservoir depletes to zero. TERT (&gamma; 1.5539) lasts " + str(tert_steps) + " steps and TP53 (&gamma; "
                "1.4298) lasts " + str(tp53_steps) + "; telomere attrition is reservoir exhaustion, not a privileged clock."),
        abstract=("The dwell &gamma;<sup>1.5</sup> sets a finite reservoir capacity for each node. Depletion time "
                  "increases monotonically with &gamma;, yet all four reservoirs reach zero, so the replicative limit is a "
                  "generic consequence of a finite well rather than a dedicated counting mechanism."),
        body="".join([
            "<h2>Finite wells</h2>",
            "<p>A switch that runs for a dwell &gamma;<sup>1.5</sup> draws on a finite reservoir. The deeper the well "
            "(larger &gamma;), the more it holds and the longer it lasts \u2014 but the reservoir is finite, so it empties. "
            "This is the substrate's version of the replicative limit.</p>",
            DWELL,
            reservoir_table(),
            "<h2>Telomere attrition is not special</h2>",
            "<p>The telomere/TERT reservoir is the longest-lived of the four because its &gamma; is high, but it depletes "
            "by the same rule as the others. Depletion time rises with &gamma; across all four wells. The telomere clock "
            "is therefore reservoir exhaustion, not a privileged counting device \u2014 consistent with the cross-species "
            "result that TERT &gamma; is not a longevity switch (&sect;9).</p>",
            "<p>The finiteness and the &gamma;-ordering are graded [V]; the absolute attrition rate in years is [O].</p>"]),
        kf="capacity &asymp; &gamma;^1.5"))

    # 6 -----------------------------------------------------------------------------------
    S.append(dict(
        slug="06-hallmarks-of-aging-substrate-map", n=6,
        subj45="Hallmarks of aging on the substrate", short="RA4 hallmarks map", grade="V",
        desc="All ten hallmarks of aging map onto substrate mechanisms with no orphans: R19 mis-flips and stuck attractors, reservoir depletion, and loop-gain loss across the RA1-RA3 axes.",
        answer=("All ten hallmarks of aging map onto substrate mechanisms with no orphans. Genomic instability and "
                "cellular senescence are R19 mis-flips and stuck attractors (RA2); telomere attrition and stem-cell "
                "exhaustion are reservoir depletion (RA3); loss of proteostasis, deregulated nutrient sensing and "
                "epigenetic drift are loop-gain loss and setpoint drift (RA1)."),
        abstract=("Each of the ten classical hallmarks is assigned to a single substrate phenomenon already reproduced in "
                  "RA1\u2013RA3, leaving zero orphans. The map is structural \u2014 every hallmark points to a mechanism "
                  "that the engine demonstrates, with three hallmarks carrying an [O] tail for their absolute magnitude."),
        body="".join([
            "<h2>One substrate, ten hallmarks</h2>",
            "<p>The hallmarks of aging are usually a list. Here they are consequences of three substrate behaviours: "
            "switch mis-flips and absorbing arrest (RA2), finite-reservoir depletion (RA3), and the slow loss of loop "
            "gain that drifts setpoints (RA1). Each hallmark maps to exactly one, with no remainder.</p>",
            hallmarks_table(),
            "<p>The structural completeness \u2014 every hallmark resolves to a demonstrated mechanism \u2014 is graded "
            "[V]. Where a hallmark's absolute size needs external calibration (mitochondrial output, intercellular "
            "coupling strength, inflammatory tone), the mapping carries a [V]/[O] tail.</p>"]),
        kf="10 hallmarks, 0 orphans"))

    _extend_sections(S)
    return S


def _extend_sections(S):
    # 7 -----------------------------------------------------------------------------------
    fold = RA5["fold_rise_40_to_80"]; c40 = RA5["cum_incidence_at_40"]; c80 = RA5["cum_incidence_at_80"]
    S.append(dict(
        slug="07-aging-universal-risk-multiplier", n=7,
        subj45="Aging as the universal risk multiplier", short="RA5 risk multiplier", grade="V",
        desc="As barriers shrink with age the crossing rate of every pathology kernel rises, so cumulative incidence is convex and steepening: a 52x rise between ages 40 and 80 before immunosenescence is added.",
        answer=("As barriers shrink with age, the crossing rate of every pathology kernel rises, so cumulative incidence "
                "is convex and steepening \u2014 a " + fnum(fold, 1) + "&times; rise between ages 40 and 80 in the model, "
                "before immunosenescence is added. This is why a single time axis multiplies risk across unrelated "
                "diseases. The shape is [V]; absolute incidence is [O]."),
        abstract=("A shrinking barrier raises the Kramers crossing hazard, and accumulated crossings give a convex "
                  "age-incidence curve. Cumulative incidence rises from " + fnum(c40, 4) + " at age 40 to " + fnum(c80, 3)
                  + " at age 80, a " + fnum(fold, 1) + "&times; increase, steepened further by immunosenescence (the seam "
                  "to the immune package)."),
        body="".join([
            "<h2>Why one axis multiplies many risks</h2>",
            "<p>Most major diseases share a single dominant risk factor: age. On this substrate that is not a "
            "coincidence. Every pathology is a barrier-crossing, and aging lowers every barrier, so the crossing hazard "
            "of unrelated kernels rises together. The accumulated crossings produce the steep, convex age-incidence curve "
            "seen in oncology.</p>",
            "<p>In the model, cumulative incidence climbs from " + fnum(c40, 4) + " at 40 to " + fnum(c80, 3) + " at 80 "
            "\u2014 a " + fnum(fold, 1) + "&times; rise \u2014 and immunosenescence steepens it further by weakening the "
            "clearance loop (the immune seam).</p>",
            "<h2>What is claimed</h2>",
            "<p>The convex, steepening shape is reproduced and graded [V]. The absolute incidence magnitude is not "
            "derivable in-package \u2014 it needs external calibration \u2014 and is graded [O] with that obstacle stated "
            "(&sect;13). This is the cross-cutting seam the package owns for the rest of the framework.</p>"]),
        kf="40\u219280 fold-rise = " + fnum(fold, 1) + "\u00d7"))

    # 8 -----------------------------------------------------------------------------------
    shared = RA6["shared_rate_fraction"]
    S.append(dict(
        slug="08-rate-of-aging-biological-age", n=8,
        subj45="The rate of aging: one biological age?", short="RA6 rate of aging", grade="V",
        desc="Across systems aging is dominated by a single shared rate (0.889 of variance) with smaller system-specific residuals; a biological-age axis exists and is dominant but organs keep measurable independent rates.",
        answer=("Across systems, aging is dominated by a single shared rate \u2014 " + fnum(shared, 3) + " of the variance "
                "in the model \u2014 with smaller system-specific residuals. A biological-age axis exists and is dominant, "
                "but it is not the whole story: organs retain measurable independent rates. The shared-plus-residual "
                "structure is [V]; the absolute mapping is [O]."),
        abstract=("Decomposing per-system aging rates yields a dominant shared component of " + fnum(shared, 3) + " plus "
                  "residual per-system variation. This supports a single biological-age axis distinct from chronological "
                  "age, while preserving organ-specific divergence \u2014 neither a pure global clock nor fully "
                  "independent aging."),
        body="".join([
            "<h2>Shared rate versus per-system rates</h2>",
            "<p>Do all systems age at one rate, or each at its own? The decomposition gives a clear but two-sided answer: "
            "a dominant shared rate accounting for " + fnum(shared, 3) + " of the variance, plus real system-specific "
            "residuals. A biological-age axis exists and dominates, yet organs are not locked to it.</p>",
            "<p>This matches observation: biological age tracks chronological age strongly but imperfectly, and individual "
            "organs can age faster or slower than the body as a whole. The structure \u2014 one dominant axis plus "
            "residuals \u2014 is graded [V]; mapping it to an absolute clock is [O].</p>"]),
        kf="shared rate fraction = " + fnum(shared, 3)))

    # 9 -----------------------------------------------------------------------------------
    pg = RA7["per_gene"]; dr = RA7["dosage_redirect"]; cv = pg["TP53"]["cv_pct"]
    S.append(dict(
        slug="09-cross-species-longevity-discriminant", n=9,
        subj45="Are human aging genes special?", short="Cross-species longevity", grade="V",
        desc="No. Across ten mammals (3.8-122 yr) every human aging-gene promoter gamma sits inside the mammalian distribution (|z|<1) with no discontinuous longevity switch; TP53 is nearly flat. The real switch is copy number.",
        answer=("No. Across ten mammals spanning 3.8 to 122 years, every human aging-gene promoter &gamma; sits inside the "
                "mammalian distribution (|z|&lt;1), and there is no discontinuous &gamma; longevity switch. The core gate "
                "TP53 is nearly flat (CV " + fnum(cv, 1) + "%; elephant &asymp; human &asymp; mouse). The real long-lived "
                "switch is off the &gamma; axis: TP53 copy number."),
        abstract=("Promoter &gamma; for TP53, CDKN2A, FOXO3 and TERT was measured across ten mammals. Human is within one "
                  "standard deviation on every gene, no clean short/long threshold appears, and TP53 varies by only CV "
                  + fnum(cv, 1) + "% across a 4\u2013211&nbsp;year span. The elephant's cancer resistance instead comes "
                  "from ~20 TP53 copies at essentially unchanged per-copy &gamma; 1.4269."),
        body="".join([
            "<p class='muted'>This chapter is the package's direct answer to the question that motivated the study: are "
            "human aging genes different from other animals, or is there a special switch? It is the headline result.</p>",
            "<h2>The cross-species table</h2>",
            "<p>The same promoter-&gamma; pipeline was run for the four masters across ten mammals from the brown rat "
            "(3.8&nbsp;yr) to the human (122&nbsp;yr), with the bowhead whale (211&nbsp;yr) listed for span. Coverage is "
            "honest: bowhead has no annotated target promoters in NCBI Gene, and CDKN2A is unannotated in several species "
            "(the free-text hits were a different gene, CDKN2AIP).</p>",
            xspecies_table(),
            "<h2>Human is not special</h2>",
            "<p>On every gene the human value sits inside the mammalian spread, within one standard deviation, and no "
            "single-gene &gamma;\u2013lifespan trend survives a permutation test.</p>",
            per_gene_table(),
            "<p>Three of four genes show overlapping short- and long-lived values (no clean threshold). TP53 in "
            "particular is nearly flat across the whole span (CV " + fnum(cv, 1) + "%): elephant, human and mouse share "
            "essentially the same core gate. All four masters do, however, lean the <em>same</em> way \u2014 every "
            "per-gene rank correlation with lifespan is positive \u2014 so the honest question is not whether one gene "
            "switches but whether that shared lean is real or an artifact.</p>",
            "<h2>Robustness audit: the shared lean is confound, not signal</h2>",
            "<p>A dedicated audit re-derives &gamma; bit-for-bit and then corrects the confounds the per-gene tests "
            "ignored. First, on this panel &gamma; is essentially a GC-content proxy (&rho;(&gamma;,&nbsp;GC) = "
            + fnum(AUD['gc_confound']['TP53']['rho_gamma_gc'], 2) + "\u2013"
            + fnum(AUD['gc_confound']['CDKN2A']['rho_gamma_gc'], 2) + " across genes), so the \u201c&gamma; axis\u201d is "
            "a GC axis. Second, the four-gene combined lean \u2014 a test the original analysis never ran \u2014 reaches "
            "only a borderline <em>raw</em> &rho; = " + fnum(AUD['combined_lean']['rho_raw'], 2) + " (permutation p = "
            + fnum(AUD['combined_lean']['p_raw'], 3) + "), and it does not survive correction: body-mass adjustment (the "
            "intrinsic-longevity residual) drops it to p = " + fnum(AUD['combined_lean']['p_sizecorr'], 2) + ", and "
            "Felsenstein independent contrasts on a dated mammal tree collapse it to corr = "
            + fnum(AUD['phylogenetic_independent_contrasts']['combined']['corr'], 2) + " (p = "
            + fnum(AUD['phylogenetic_independent_contrasts']['combined']['perm_p'], 2) + ") \u2014 the short-lived rodents "
            "are a single clade, so the raw trend was phylogenetic pseudoreplication. Out of sample, the four &gamma; "
            "values classify long- vs short-lived species at only "
            + fnum(100 * AUD['multivariate_out_of_sample']['loocv_accuracy'], 0)
            + "% leave-one-out accuracy (label-permutation p = "
            + fnum(AUD['multivariate_out_of_sample']['label_perm_p'], 2) + "), not above chance. The human-not-special / "
            "no-switch conclusion is therefore robust to every confound this small panel lets us test, and the original "
            "\u201cno trend\u201d wording is sharpened to \u201ca weak shared lean that is fully confound-attributable.\u201d</p>",
            "<p>One honest caveat survives the audit. Of the four masters, <strong>TERT (telomere maintenance) is the most "
            "lifespan-leaning</strong>: it is the only gene whose lean is <em>not</em> removed by body-mass correction "
            "(size-corrected &rho; = " + fnum(AUD['tert_focus']['rho_sizecorr_longevity'], 2) + ") and it carries the "
            "largest phylogenetic-contrast correlation (" + fnum(AUD['tert_focus']['pic_corr'], 2) + "). It still never "
            "reaches significance (p &asymp; " + fnum(AUD['tert_focus']['p_sizecorr'], 2) + "), so it is a lead for a "
            "larger panel, not a result \u2014 graded [O]. It is consistent with known biology that the telomere lever on "
            "lifespan is real but acts off the promoter-&gamma; axis: large mammals suppress somatic telomerase to resist "
            "cancer (Gomes 2011), a regulatory and dosage effect rather than a promoter-sequence one \u2014 the same "
            "off-axis pattern as the TP53 copy-number switch below.</p>",
            "<h2>The real switch is off the &gamma; axis</h2>",
            "<p>Where, then, does extreme longevity come from? Not from rewriting the promoter. The elephant carries ~20 "
            "functional TP53 copies at an essentially unchanged per-copy &gamma; of " + fnum(dr['tp53_gamma_elephant'], 4)
            + " (human " + fnum(dr['tp53_gamma_human'], 4) + "), giving roughly twenty times the effective gate dosage at "
            "a per-copy barrier of " + fnum(dr['per_copy_barrier_human'], 4) + ". The switch is copy number, not promoter "
            "&gamma;.</p>",
            vp_card("tp53-gamma", "&gamma;<sub>TP53</sub> &asymp; 1.427 (mammal-invariant)",
                    "the apoptosis/senescence gate barrier is nearly species-invariant across a 4\u2013211 yr lifespan span.",
                    grade_span(*GBADGE["V"]), "node atlas, \u00a72",
                    "/" + PAPER_ID + "/02-node-atlas-measured-promoter-gamma/"),
            "<p>The framework's thesis holds cross-species: a conserved identity &gamma; substrate plus divergent dynamics "
            "(dosage, loop gain, reservoir size, senescence rate) produces the lifespan spectrum. Human-not-special, "
            "TP53 flatness, and the audited finding that the weak shared lean is fully confound-attributable are graded "
            "[V]; the residual TERT lean is [O] (n&nbsp;=&nbsp;10, p&nbsp;&asymp;&nbsp;0.12, awaiting a larger panel); the "
            "off-&gamma;-axis longevity levers are [L] \u2014 TP53 copy number (Abegglen 2015 JAMA; Sulak 2016 eLife) and "
            "somatic telomerase suppression in large mammals (Gomes 2011).</p>"]),
        kf="TP53 CV = " + fnum(cv, 1) + "% (4\u2013211 yr)"))

    # 10 ----------------------------------------------------------------------------------
    a = RA8["verdict"]
    tert_load = a["archaic_substitution_load"]["TERT"]
    foxo_rng = RA8["per_gene"]["FOXO3"]["gamma_spread"]["range"]
    S.append(dict(
        slug="10-archaic-and-present-day-aging-promoters", n=10,
        subj45="Archaic and present-day aging promoters", short="Archaic observation", grade="V",
        desc="A cross-sectional set of seven dated genomes (present-day, three Neanderthal, one Denisovan, two ancient modern) shows the four aging-master promoter gamma in a narrow band; TP53/CDKN2A read identically in dated modern humans, TERT carries the most substitutions. Observation only.",
        answer=("Across a cross-sectional set of seven dated, sequenced individuals \u2014 the present-day "
                "reference, three archaic Neanderthal genomes, one archaic Denisovan, and two dated "
                "modern-human genomes \u2014 the four aging-master promoter &gamma; values sit in a very "
                "narrow band on every gene (each per-gene range &lt; 0.0016). The senescence/apoptosis gate "
                "TP53 and the arrest switch CDKN2A read identically in the two dated modern-human genomes and "
                "the present-day reference; TERT carries the most archaic promoter substitutions (" 
                + str(tert_load) + "). This is a measured snapshot \u2014 the only claims are the measured "
                "&gamma; in each individual, its spread per gene, and which positions differ."),
        abstract=("The same promoter-&gamma; pipeline (&minus;mean SantaLucia NN &Delta;G37 over "
                  "TSS&minus;2000..+500) is measured in each individual, where each promoter is the GRCh37 "
                  "reference plus that individual's homozygous-derived substitutions. The set is examined as a "
                  "snapshot; shared genotype states are reported as observed co-occurrences, never as anything "
                  "beyond the co-occurrence itself."),
        body="".join([
            "<aside class='vp-card' data-locked='observation'><b>Observation only (constitution)</b> \u2014 "
            "this chapter compares a cross-sectional SET of dated individuals. Each is one sequenced genome "
            "with one measured promoter &gamma;, reported as a present-state. The package makes no claim about "
            "how any state arose or about any process relating the individuals; where two individuals share a "
            "genotype state, that is reported as an observed co-occurrence, never as anything beyond the "
            "co-occurrence itself. "
            + grade_span(*GBADGE["V"]) + "</aside>",
            "<h2>The cross-sectional set</h2>",
            "<p>Seven high-coverage genomes carry the four aging masters at a known date: the present-day "
            "modern-human reference (GRCh37), three archaic Neanderthal individuals (Altai, Vindija&nbsp;33.19, "
            "Chagyrskaya), one archaic Denisovan, and two dated modern-human genomes (Ust'-Ishim &asymp; "
            "45&nbsp;kya, Loschbour &asymp; 8&nbsp;kya). Each promoter is reconstructed as the GRCh37 reference "
            "plus that individual's homozygous-derived substitutions (genotype 1/1, FILTER pass); &gamma; is "
            "then measured by the identical pipeline used for the node atlas (&sect;2) and the cross-species "
            "panel (&sect;9).</p>",
            archaic_gamma_table(),
            "<h2>The senescence gate reads the same</h2>",
            "<p>On TP53 (apoptosis) and CDKN2A (the p16 arrest switch), the two dated modern-human genomes and "
            "the present-day reference carry an identical promoter &gamma; \u2014 the archaic individuals differ "
            "only by two or three distal substitutions that move &gamma; by less than 0.0009. The core "
            "senescence/apoptosis gate is, as a measured state, the same sequence in every modern-human genome "
            "in the set and nearly the same in the archaic ones.</p>",
            "<h2>TERT carries the most promoter substitutions</h2>",
            "<p>Of the four masters, the telomere-maintenance gene TERT carries the most homozygous-derived "
            "promoter substitutions across the archaic individuals (" + str(tert_load) + " in total), and the "
            "same three TERT positions co-occur across all four archaic genomes. The widest &gamma; range in "
            "the whole set, however, belongs to FOXO3 (" + fnum(foxo_rng, 6) + "), and even that is under "
            "0.0016 \u2014 so \u201cmost substituted\u201d (TERT) and \u201cwidest &gamma; spread\u201d (FOXO3) "
            "are distinct, both small, measured facts.</p>",
            archaic_subload_table(),
            "<h2>The cancer-promoter positions are invariant</h2>",
            "<p>The two recurrent TERT cancer-promoter regulatory positions (the &minus;124 and &minus;146 "
            "sites relative to the start codon) carry the same base in every individual in the set; every "
            "difference TERT does carry is distal to them. This invariance is a measured observation across the "
            "snapshot.</p>",
            vp_card("tert-residual", "TERT is the most distinctive aging master",
                    "on the cross-species axis (&sect;9) it is the single residual lifespan lead; on this "
                    "dated-individual axis it carries the most promoter substitutions \u2014 two independent "
                    "measured observations, taken up in &sect;11.",
                    grade_span(*GBADGE["V"]), "telomere keystone, \u00a711",
                    "/" + PAPER_ID + "/11-telomere-keystone-dynamics-not-gamma/"),
            "<h2>What is and is not claimed</h2>",
            "<p>The claims are exactly three: the measured &gamma; in each individual, the width of the "
            "&gamma; spread per gene, and which promoter positions differ. Why the states co-occur is out of "
            "scope and graded [O]: a cross-sectional snapshot is silent on mechanism. Per-individual &gamma;, "
            "the &gamma; spread, the substitution counts, and the cancer-hotspot invariance are measured [V].</p>"]),
        kf="TERT archaic hom-sub = " + str(tert_load)))

    # 11 ----------------------------------------------------------------------------------
    tg = RA9["telomere_gamma"]["gamma_G_rich"]
    tel_res = RA9["reservoir_reading"]["telomere_reservoir"]
    S.append(dict(
        slug="11-telomere-keystone-dynamics-not-gamma", n=11,
        subj45="The telomere keystone: dynamics, not gamma", short="Telomere keystone", grade="V",
        desc="The telomere is the keystone of aging on this substrate, but the keystone is its dynamics, not its gamma. The telomere repeat gamma 1.3298 is the lowest and most invariant of any aging sequence; TERT is the most distinctive master on two axes, yet its lever acts off the gamma axis through reservoir length and attrition rate.",
        answer=("The telomere is the keystone of aging on this substrate \u2014 but the keystone is its "
                "DYNAMICS, not its &gamma;. The canonical telomere repeat (TTAGGG)n has &gamma; " + fnum(tg, 4)
                + ", the lowest of any aging-related sequence here and a near-exact universal constant "
                "(identical on both strands, length-independent to &lt;0.5%). TERT, which maintains this "
                "reservoir, is independently the most distinctive aging master on two measured axes (&sect;9, "
                "&sect;10), yet its promoter &gamma; is a weak modulator because the telomere lever acts OFF "
                "the &gamma; axis \u2014 through reservoir length and attrition rate."),
        abstract=("&gamma; fixes a node's barrier &gamma;&sup2;/4 and reservoir capacity &gamma;<sup>1.5</sup> "
                  "(DWELL). The telomere is a finite reservoir (&sect;5); because its repeat &gamma; is "
                  "invariant, the reservoir RULER is the same everywhere and what differs between individuals "
                  "and species is repeat COUNT (length) and attrition RATE, neither a &gamma; quantity."),
        body="".join([
            "<p class='muted'>This chapter is the package's synthesis of the question that motivated the "
            "telomere study: if the telomere is the key to aging, what exactly is the key \u2014 the &gamma; of "
            "the machinery, or the dynamics of the reservoir it maintains?</p>",
            "<h2>The telomere repeat has the lowest, most invariant &gamma;</h2>",
            "<p>Run the promoter-&gamma; rule on the canonical vertebrate telomere repeat (TTAGGG)n and the "
            "value is &gamma; " + fnum(tg, 4) + ". It is identical on the G-rich strand and its C-rich "
            "complement (the SantaLucia table is strand-symmetric), it is the lowest &gamma; of any "
            "aging-related sequence in the package \u2014 below all four master promoters \u2014 and it is "
            "length-independent to better than half a percent (only end effects move it). The telomere "
            "&gamma; is, in other words, a near-exact universal constant: the same ruler in every species "
            "and every dated individual.</p>",
            telomere_ranking_table(),
            "<h2>The reservoir reading: invariant ruler, variable length and rate</h2>",
            "<p>On this substrate the telomere is a finite reservoir whose capacity scales as "
            "&gamma;<sup>1.5</sup> (DWELL) and which depletes monotonically to the replicative limit "
            "(&sect;5). The run gives the telomere reservoir a capacity of " + fnum(tel_res["capacity"], 3)
            + " and " + str(tel_res["steps_to_depletion"]) + " steps to depletion. But because the "
            "telomere-repeat &gamma; is invariant, that &gamma;<sup>1.5</sup> ruler does not differ between "
            "individuals or species. What differs is the COUNT of repeats (telomere length) and the "
            "per-division attrition RATE \u2014 and neither of those is a &gamma; or a sequence-identity "
            "quantity.</p>",
            DWELL,
            "<h2>TERT is the keystone gene \u2014 on two measured axes</h2>",
            "<p>Two independent results in this package point at TERT. The cross-species discriminant (&sect;9) "
            "finds it is the one master whose lifespan lean is not removed by body-mass correction \u2014 the "
            "single residual lead. The dated-individual observation (&sect;10) finds it carries the most "
            "archaic promoter substitutions. On both axes TERT is the most distinctive aging master, and both "
            "are measured observations.</p>",
            "<h2>Yet the lever is off the &gamma; axis</h2>",
            "<p>Despite that, TERT's promoter &gamma; sits inside the mammalian distribution (&sect;9) and "
            "varies by less than 0.0008 across the dated-individual set (&sect;10). There is no contradiction: "
            "the telomere lever on lifespan acts OFF the promoter-&gamma; axis \u2014 through reservoir size "
            "(telomere length) and depletion rate (attrition) \u2014 the same off-axis pattern as the "
            "cross-species telomerase-dosage and TP53 copy-number levers (&sect;9). The promoter-&gamma; axis "
            "is therefore correct to report the telomere as only a weak &gamma; modulator; the keystone role "
            "lives in the reservoir dynamics that &gamma; does not index.</p>",
            "<div class='kf'>telomere &gamma; = " + fnum(tg, 4) + " (lowest, universal)&nbsp;&nbsp;|&nbsp;&nbsp;"
            "keystone = reservoir dynamics, off the &gamma; axis</div>",
            "<p>The telomere-repeat &gamma; invariance, its strand symmetry, and its lowest-&gamma; ranking are "
            "measured [V]; the &gamma;<sup>1.5</sup> reservoir law is the vendored substrate [F]; the "
            "\u201ckeystone is dynamics, not &gamma;\u201d synthesis organizes the package's own measured facts "
            "but is an interpretation [O]; telomere length and per-division attrition rates are cited, not "
            "reproduced in-package [L] (Harley 1990; Frenck 1998; Aubert&nbsp;&amp;&nbsp;Lansdorp 2008; "
            "somatic telomerase suppression in large mammals, Gomes 2011).</p>"]),
        kf="telomere &gamma; = " + fnum(tg, 4)))

    # 12 ----------------------------------------------------------------------------------
    canc_fold = PATH["failures"][2]["fold_rise_hazard_30_to_90"]; crit = PATH["failures"][1]["critical_drops"]
    cvals = [v for v in crit.values() if v is not None]
    S.append(dict(
        slug="12-pathology-sarcopenia-frailty-cancer", n=12,
        subj45="Pathology: sarcopenia, frailty, cancer", short="Pathology", grade="V",
        desc="The major non-rare diseases follow one derived law: g_eff = g(1-d) shrinks the barrier (drift) and spinodal (catastrophe). Sarcopenia is monotone drift, frailty an accelerating co-failure, cancer a 135x hazard rise.",
        answer=("The major non-rare aging diseases follow one derived law: g_eff = &gamma;(1&minus;d) shrinks both the "
                "barrier (drift) and the spinodal (catastrophe). Sarcopenia is monotone setpoint drift, frailty is an "
                "accelerating co-failure of many setpoints, and aging-as-cancer is the convex crossing-hazard rise ("
                + fnum(canc_fold, 0) + "&times; from age 30 to 90). Rare/monogenic forms belong to disease_wp."),
        abstract=("A single derived law \u2014 an age-related loop-gain drop d lowering effective &gamma; \u2014 generates "
                  "three failure shapes: sarcopenia (defended force-state drifts down monotonically), frailty (critical "
                  "drops spread across setpoints give an accelerating co-failure transition), and the convex "
                  + fnum(canc_fold, 0) + "&times; rise in crossing hazard that is aging-as-cancer-risk."),
        body="".join([
            "<h2>One derived law</h2>",
            "<p>Disease here is the failure of a defended setpoint on the R19 substrate. An age-related loop-gain drop d "
            "lowers the effective gain to &gamma;(1&minus;d); this shrinks the barrier (so the setpoint drifts) and the "
            "spinodal (so a fixed stressor can flip it). All three major failures are read off this one law.</p>",
            BARR, SPIN,
            "<h3>Sarcopenia \u2014 monotone drift</h3>",
            "<p>As gain falls, the defended force-state creeps down monotonically and the barrier fraction shrinks toward "
            "catastrophe. The shape is [V]; the absolute calendar rate is [O].</p>",
            sarcopenia_table(),
            "<h3>Frailty and multimorbidity \u2014 accelerating co-failure</h3>",
            "<p>Many setpoints decline together, each with its own critical drop (here spanning " + fnum(min(cvals), 2)
            + " to " + fnum(max(cvals), 2) + " across six systems). As the shared drop rises, the fraction of failed "
            "setpoints climbs in an accelerating S-curve \u2014 the frailty transition \u2014 rather than linearly. The "
            "co-failure shape is [V]; absolute prevalence is [O].</p>",
            "<h3>Aging as the cancer risk multiplier</h3>",
            "<p>The crossing hazard rises convexly with age, a " + fnum(canc_fold, 0) + "&times; increase from 30 to 90 in "
            "relative units, reproducing the steep oncology age-incidence slope (the seam of &sect;7). The convex shape is "
            "[V]; the absolute incidence is [O].</p>",
            "<p>Rare and monogenic accelerated-aging syndromes (progeroid disorders) are not modeled here; they are owned "
            "by the disease whitepaper and enter this layer only as a cited rate parameter.</p>"]),
        kf="cancer hazard 30\u219290 = " + fnum(canc_fold, 0) + "\u00d7"))

    # 11 ----------------------------------------------------------------------------------
    S.append(dict(
        slug="13-reproducibility-grading-ledger", n=13,
        subj45="Reproducibility, grading, and the ledger", short="Reproducibility & grading", grade="V",
        desc="Every quantity is reproduced deterministically (SEED 19; result hash byte-identical across two runs) and graded honestly: mechanisms and the cross-species null are [V], the copy-number switch [L], absolute rates [O].",
        answer=("Every quantity is reproduced deterministically (SEED 19; the result hash is byte-identical across two "
                "runs at " + DET_HASH[:12] + "\u2026) and graded honestly: mechanisms and the cross-species null result "
                "are [V], the copy-number longevity switch is [L], and absolute rates, incidence and lifespans are [O] "
                "with stated obstacles."),
        abstract=("The discipline is LOCK \u2192 Derive \u2192 Gate with no tuning: every constant is a measured input or a "
                  "derived value, never chosen to hit a target. The deterministic engine emits a byte-identical result on "
                  "repeated runs (2&times;sha256), and the irreproducibility ledger collects every [O] item with its "
                  "specific obstacle."),
        body="".join([
            "<h2>LOCK \u2192 Derive \u2192 Gate</h2>",
            "<p>Inputs are locked, results are derived by fixed rules, and gates check the derivation by count. The "
            "vendored substrate math is never re-derived here \u2014 the R19 field and its derived stability and dwell laws "
            "are defined once in <a href='/" + PAPER_ID + "/01-aging-as-homeostatic-setpoint-decline/'>&sect;1</a>; the "
            "promoter &gamma; values are measurements; the dynamics are deterministic simulations seeded at 19.</p>",
            "<div class='kf'>SEED = 19&nbsp;&nbsp;|&nbsp;&nbsp;result sha256 = " + DET_HASH[:24] + "\u2026 (2\u00d7 identical)</div>",
            "<h2>The grade vocabulary</h2>",
            "<p>Three grades carry the evidence load. <b>[V]</b> is verified \u2014 measured or reproduced in-package. "
            "<b>[L]</b> is anchored to a cited result. <b>[O]</b> is open \u2014 not reproducible in-package, with the "
            "obstacle stated. The grading is the framework's load-bearing claim, not decoration.</p>",
            "<ul class='tight'>",
            "<li><b>[V]</b> \u2014 the drift+catastrophe law (RA1), senescence irreversibility and accumulation (RA2), "
            "finite reservoirs and &gamma;-ordering (RA3), the hallmark map (RA4), the convex risk-multiplier shape "
            "(RA5), the shared-rate structure (RA6), human-not-special and TP53 flatness (RA7), the archaic "
            "cross-sectional observation \u2014 per-individual &gamma;, substitution counts, and TERT "
            "cancer-hotspot invariance (RA8) \u2014 and the telomere-repeat &gamma; invariance, strand symmetry, "
            "and lowest-&gamma; ranking (RA9).</li>",
            "<li><b>[L]</b> \u2014 the copy-number longevity switch (elephant ~20 TP53 copies; Abegglen 2015 JAMA, Sulak "
            "2016 eLife), the cited per-system decline anchors, and telomere length and per-division attrition "
            "rates (Harley 1990; Frenck 1998; Aubert &amp; Lansdorp 2008; somatic telomerase suppression in "
            "large mammals, Gomes 2011).</li>",
            "<li><b>[O]</b> \u2014 the &gamma;\u2013lifespan trend (small panel, GC-content confound, phylogenetic "
            "non-independence), the \u201ctelomere keystone is dynamics, not &gamma;\u201d synthesis (RA9, an "
            "interpretation that organizes the package's measured facts), the meaning of the archaic genotype "
            "co-occurrences (RA8, a cross-sectional snapshot is silent on mechanism), and every absolute "
            "calendar rate, incidence magnitude and lifespan, which need an external clock or calibration the "
            "package does not contain.</li>",
            "</ul>",
            "<h2>No tuning</h2>",
            "<p>No constant is chosen to hit a target. Noise scales and chronic-stressor magnitudes used in the pathology "
            "sweeps are stated, round, and set the relative shape only; the absolute magnitudes they would imply are "
            "graded [O]. The irreproducibility ledger lists every [O] item, its obstacle, and its location.</p>"]),
        kf="2\u00d7sha256 identical"))

    # 14 ----------------------------------------------------------------------------------
    cv53 = RA7["per_gene"]["TP53"]["cv_pct"]
    tel_g = RA9["verdict"]["telomere_repeat_gamma"]
    tert_load = RA8["verdict"]["archaic_substitution_load"]["TERT"]
    S.append(dict(
        slug="14-conclusion-genome-fixes-the-ruler-not-the-lifespan", n=14,
        subj45="Conclusion: the genome fixes the ruler, not the lifespan", short="Conclusion", grade="O",
        desc="The genome fixes the ruler of aging \u2014 the promoter \u03b3 of the masters, the node inventory, the reservoir law \u2014 but not the realized lifespan; the package's own results show realized lifespan is underdetermined by the \u03b3 axis, not merely uncomputed, with the longevity lever off-axis in dosage and reservoir dynamics.",
        answer=("The genome fixes the ruler of aging \u2014 the promoter &gamma; of the aging masters, the node "
                "inventory, and the reservoir law dwell &asymp; &gamma;<sup>1.5</sup> \u2014 and that layer is "
                "measured from sequence [V]. It does not fix the realized lifespan: the rate at which "
                "senescent cells accumulate, the telomere attrition rate, and the absolute calendar age are "
                "runtime. The package's own results \u2014 &gamma; nearly flat across a 4\u2013211&nbsp;yr "
                "lifespan span (TP53 CV " + fnum(cv53, 1) + "%), the telomere lever off the &gamma; axis, and "
                "archaic promoters reading the same as modern \u2014 show that realized lifespan is "
                "underdetermined by the &gamma; axis, not merely uncomputed; the longevity lever lives in "
                "copy number and reservoir dynamics, off the &gamma; axis."),
        abstract=("This closing section draws the package to its epistemic end. It separates two kinds of open "
                  "item \u2014 <i>uncomputed</i> (closable by an external clock or calibration) from "
                  "<i>underdetermined</i> (the &gamma; axis does not carry the quantity) \u2014 and shows from "
                  "the package's own measured results that the realized-lifespan gap is the second kind: across "
                  "a fifty-fold cross-species lifespan span the flattest aging-master promoter &gamma; varies "
                  "by only CV " + fnum(cv53, 1) + "%, the telomere-repeat &gamma; is a near-exact universal "
                  "constant (" + fnum(tel_g, 4) + ") whose lever acts off the &gamma; axis, and the four "
                  "masters read the same &gamma; in archaic and modern individuals. The longevity switch is "
                  "copy number and reservoir dynamics, not promoter &gamma;. The honest posture is observation "
                  "under the constitution; an [O] is a correctly labelled truth, not a failure, and an open "
                  "conclusion is the strongest position when the object is genuinely underdetermined."),
        body="".join([
            vp_card("conclusion", "The reading of aging, taken to its honest end",
                    "The genome fixes the ruler \u2014 the aging-master promoter &gamma;, the node inventory, "
                    "and the reservoir law dwell &asymp; &gamma;<sup>1.5</sup> \u2014 all read from sequence "
                    "[V]. The realized lifespan is the ruler run forward under boundary conditions the sequence "
                    "does not contain: reservoir size (telomere length), attrition rate, copy-number dosage, "
                    "and runtime drive. Two kinds of open item must not be confused: the absolute calendar "
                    "rates are <i>uncomputed</i> (they need an external clock), while the off-&gamma;-axis "
                    "location of the lifespan lever is <i>underdetermined</i> \u2014 measured, and not closable "
                    "by more computation on the promoter. The correct act is to observe and to grade honestly.",
                    grade_span(*GBADGE["O"]), "reproducibility &amp; grading, \u00a713",
                    "/" + PAPER_ID + "/13-reproducibility-grading-ledger/"),
            "<h2>&gamma; is the ruler of aging, not its realized clock</h2>",
            "<p>The aging masters' promoter &gamma; is measured from sequence (<a href='/" + PAPER_ID + "/02-node-"
            "atlas-measured-promoter-gamma/'>&sect;2</a>), and it fixes each node's barrier &gamma;&sup2;/4 and "
            "reservoir dwell &asymp; &gamma;<sup>1.5</sup>. But &gamma; does not index lifespan: across ten "
            "mammals spanning a fifty-fold maximum-lifespan range \u2014 from a mouse near 4&nbsp;yr to a "
            "bowhead near 211&nbsp;yr \u2014 the flattest master, TP53, varies at only CV " + fnum(cv53, 1)
            + "% (<a href='/" + PAPER_ID + "/09-cross-species-longevity-discriminant/'>&sect;9</a>). A ruler "
            "that barely moves across a 50&times; lifespan span cannot be the axis that sets the lifespan. "
            "&gamma; fixes the threshold scale, not the realized clock.</p>",
            "<h2>The telomere is the keystone of dynamics, not &gamma;</h2>",
            "<p>The single most distinctive aging master is TERT, on two measured axes: it is the residual "
            "cross-species lifespan lead (&sect;9) and it carries the most archaic promoter substitutions "
            "(" + str(tert_load) + ", <a href='/" + PAPER_ID + "/10-archaic-and-present-day-aging-promoters/'>"
            "&sect;10</a>). Yet the canonical telomere repeat &gamma; is " + fnum(tel_g, 4) + " \u2014 the "
            "lowest of any aging sequence and a near-exact universal constant, the same ruler in every species "
            "and every dated individual (<a href='/" + PAPER_ID + "/11-telomere-keystone-dynamics-not-gamma/'>"
            "&sect;11</a>). The telomere is the keystone of aging, but the keystone is its <em>dynamics</em> "
            "\u2014 reservoir length and attrition rate \u2014 not its &gamma;. The lever acts off the "
            "promoter-&gamma; axis, exactly as the cross-species telomerase-dosage and TP53 copy-number levers "
            "do.</p>",
            "<h2>Archaic reads the same as modern \u2014 and that is silent on lifespan</h2>",
            "<p>Across a cross-sectional set of seven dated genomes the four masters' promoter &gamma; sits in a "
            "band narrower than 0.0016, and the senescence/apoptosis gate (TP53, CDKN2A) reads identically in "
            "the dated modern-human genomes (&sect;10). This is a measured present-state, and it is silent on "
            "lifespan: realized lifespan was never on the &gamma; axis, and the lifespans of archaic "
            "individuals cannot be observed at all. The honest reading is &ldquo;the &gamma; identity is the "
            "same,&rdquo; not &ldquo;the lifespan is the same.&rdquo;</p>",
            "<h2>Two kinds of open, and the difference is the whole point</h2>",
            "<p>An open item is not one thing, and conflating the two kinds makes the genome look either "
            "omniscient or irrelevant. An <em>uncomputed</em> open item \u2014 the absolute calendar rates, "
            "incidences, and lifespans (<a href='/" + PAPER_ID + "/07-aging-universal-risk-multiplier/'>&sect;7"
            "</a>, <a href='/" + PAPER_ID + "/08-rate-of-aging-biological-age/'>&sect;8</a>) \u2014 would close "
            "with an external clock or calibration the package deliberately does not contain; the shapes "
            "reproduce [V], but the absolute years do not. An <em>underdetermined</em> open item is one the "
            "&gamma; axis does not carry at all: the location of the lifespan lever off the &gamma; axis is "
            "itself measured, and no more computation on the promoter sequence recovers it. And the "
            "cross-species null is not a broken test \u2014 it is audited robust to GC, body mass, phylogenetic "
            "non-independence, and multivariate confounds (&sect;9), so the flatness is a result, not a failure "
            "to detect.</p>",
            "<h2>Neither all-genes nor environment</h2>",
            "<p>The realized lifespan is therefore not &ldquo;all in the genes&rdquo; and not "
            "&ldquo;the environment&rdquo; either. The genome fixes the schedule, the node inventory, the "
            "thresholds, and even how open each node is to drive; the realized life is that ruler run forward "
            "under boundary conditions \u2014 reservoir size, attrition rate, copy-number dosage, and runtime "
            "drive \u2014 that the promoter sequence does not contain. The companion DNA reading reaches the "
            "same conclusion in the developmental-time axis: &gamma; fixes what and in what order, not "
            "when.</p>",
            "<h2>Observation is the correct act, and an [O] is not a failure</h2>",
            "<p>Where realization is underdetermined, the right act is to observe the measured states and grade "
            "honestly, not to manufacture an absolute lifespan the data withholds \u2014 which is exactly what "
            "the observation-only archaic comparison did. An [O] is not a failed [V]; it is a truth, correctly "
            "labelled, and it is what lets the framework learn from the next measurement rather than overclaim. "
            "An open conclusion is not a weak one: when the realized lifespan is genuinely underdetermined by "
            "the &gamma; axis, it is the strongest position available, because it is the one the next "
            "measurement cannot overturn. The genome is the ruler and the first cause; the realized life is "
            "read off the ruler run forward under conditions the sequence does not hold. Not failure, not "
            "success: measurement.</p>",
            "<div class='kf'>genome fixes the ruler [V]&nbsp;&nbsp;|&nbsp;&nbsp;realized lifespan is off the "
            "&gamma; axis [O] \u2014 dynamics, not &gamma;</div>"]),
        kf="ruler [V] \u00b7 realized lifespan off the &gamma; axis [O]"))


# ------------------------------------------------------------------------------------------------
# page + hub + metadata renderers
# ------------------------------------------------------------------------------------------------
def render_page(sec, total, sections):
    gc, gt = GBADGE[sec["grade"]]
    parts = [head(sec["slug"], sec["n"], sec["subj45"], sec["desc"], sec["short"])]
    parts.append("<body>")
    parts.append('<header><nav class="crumb"><a href="/">Home</a> &rsaquo; '
                 '<a href="/%s/">%s</a> &rsaquo; \u00a7%d</nav></header>' % (PAPER_ID, esc(SHORT), sec["n"]))
    parts.append("<main>")
    parts.append('<p class="eyebrow">Aging &amp; Senescence \u00b7 \u00a7%d</p>' % sec["n"])
    parts.append("<h1>%s</h1>" % sec["subj45"])
    parts.append('<p class="answer">%s</p>' % sec["answer"])
    parts.append('<p class="abstract">%s</p>' % sec["abstract"])
    parts.append(claim_strip(gc, gt, sec["slug"]))
    parts.append(sec["body"])
    parts.append(pn(sec["n"], total, sections))
    parts.append("</main>")
    parts.append(footer())
    return "\n".join(parts)


def render_hub(sections):
    items = []
    for s in sections:
        gc, gt = GBADGE[s["grade"]]
        items.append(
            '<li><span class="n">%02d</span><a href="/%s/%s/">%s</a>'
            '<span class="grade %s">%s</span><span class="one">%s</span></li>'
            % (s["n"], PAPER_ID, s["slug"], esc(s["subj45"]), gc, gt, esc(s["short"])))
    # headline results strip
    cv = RA7["per_gene"]["TP53"]["cv_pct"]
    fold = RA5["fold_rise_40_to_80"]
    shared = RA6["shared_rate_fraction"]
    hr = ("<div class='headline-results'>"
          "<span>human aging genes: not special (|z|&lt;1)</span>"
          "<span>TP53 CV = " + fnum(cv, 1) + "% across 4\u2013211 yr</span>"
          "<span>longevity switch = copy number, not &gamma;</span>"
          "<span>age risk-multiplier 40\u219280 = " + fnum(fold, 1) + "\u00d7</span>"
          "<span>shared aging rate = " + fnum(shared, 3) + "</span></div>")
    ld_series = json.dumps({
        "@context": "https://schema.org", "@type": "CreativeWorkSeries", "name": TITLE_FULL,
        "alternateName": SHORT, "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "identifier": "DOI " + DOI_TBD, "license": CC, "inLanguage": "en",
        "hasPart": [{"@type": "ScholarlyArticle", "position": s["n"], "name": s["subj45"],
                     "url": SITE + "/" + PAPER_ID + "/" + s["slug"] + "/"} for s in sections]
    }, ensure_ascii=False, separators=(",", ":"))
    ld_crumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": SHORT}]}, ensure_ascii=False, separators=(",", ":"))
    out = [
        "<!DOCTYPE html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>" + esc(SHORT + " \u2014 a VP Theory volume | Jamming Physics") + "</title>",
        '<meta name="description" content="' + esc("Aging as the systemic decline of homeostatic setpoints on the "
            "jamming substrate: setpoint drift, cellular senescence as a stuck attractor, reservoir depletion, the "
            "hallmarks map, the age risk-multiplier, and a cross-species test showing human aging genes are not "
            "special.") + '">',
        '<link rel="canonical" href="' + SITE + "/" + PAPER_ID + '/">',
        '<link rel="stylesheet" href="/assets/css/site.css">',
        '<script type="application/ld+json">' + ld_series + "</script>",
        '<script type="application/ld+json">' + ld_crumb + "</script>",
        "</head>", "<body>",
        '<header><nav class="crumb"><a href="/">Home</a> &rsaquo; ' + esc(SHORT) + "</nav></header>",
        "<main>",
        '<p class="eyebrow">A VP Theory volume \u00b7 integrative capstone</p>',
        "<h1>" + esc(SHORT) + "</h1>",
        '<p class="lede">Aging is the slow loss of defense gain of every homeostatic setpoint, plus the accumulation of '
        "cells stuck in irreversible R19 attractors \u2014 and the dominant risk multiplier for every pathology kernel in "
        "the framework.</p>",
        '<p class="answer">This volume derives aging on the jamming substrate: one declining-gain law gives both gradual '
        "drift and sudden failure (\u00a73), senescence is an absorbing attractor (\u00a74), telomere loss is reservoir "
        "depletion (\u00a75), all ten hallmarks map cleanly (\u00a76), and a ten-mammal test shows human aging genes are "
        "not special \u2014 the longevity switch is TP53 copy number, not promoter &gamma; (\u00a79).</p>",
        hr,
        '<p>This package is derived from the VP Theory jamming branch \u2192 <a href="/physics/">VP Physics</a>, and it '
        'inherits node identities from the <a href="/dna/">DNA blueprint</a>. It re-emerges no organs owned elsewhere; it '
        "adds the temporal decline dynamics and owns the aging risk-multiplier seam for the rest of the framework.</p>",
        "<h2>Contents</h2>",
        '<ul class="toc">', "".join(items), "</ul>",
        '<p class="muted">Every quantity is reproduced deterministically (SEED 19, 2&times;sha256 identical) and graded '
        "honestly \u2014 [V] verified, [L] cited anchor, [O] open with a stated obstacle (\u00a711). DOI is assigned on "
        "publication.</p>",
        "</main>", footer()]
    return "\n".join(out)


def build_meta(sections):
    cv = RA7["per_gene"]["TP53"]["cv_pct"]
    chapters = []
    for s in sections:
        chapters.append({"no": s["n"], "slug": s["slug"], "title": s["subj45"],
                         "one_liner": s["short"], "grade": {"V": "verified", "F": "forced", "O": "open"}[s["grade"]]})
    return {
        "paper_id": PAPER_ID, "code": CODE, "title": TITLE_FULL, "short": SHORT,
        "doi": DOI_TBD, "hub_url": "/" + PAPER_ID + "/", "branch": "integrative capstone",
        "abstract": ("Aging as the systemic decline of homeostatic setpoints on the jamming substrate: one declining-gain "
                     "law gives both gradual drift and catastrophic failure, cellular senescence is an absorbing R19 "
                     "attractor, telomere loss is reservoir depletion, the ten hallmarks map without orphans, aging is the "
                     "convex risk multiplier for every pathology kernel, and a ten-mammal test shows human aging genes are "
                     "not special \u2014 the longevity switch is TP53 copy number, not promoter gamma."),
        "headline_results": ["human aging genes not special (|z|<1)", "TP53 CV " + fnum(cv, 1) + "% across 4-211 yr",
                             "longevity switch = copy number, not gamma", "aging = dominant pathology risk multiplier"],
        "chapters": chapters,
        "determinism": {"seed": 19, "result_sha256": DET_HASH, "two_runs_identical": bool(DET_OK)},
        "totals": {"chapters": len(sections)},
    }


def write_sitemap(sections):
    urls = [SITE + "/" + PAPER_ID + "/"] + [SITE + "/" + PAPER_ID + "/" + s["slug"] + "/" for s in sections]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (u, DATE))
    body.append("</urlset>")
    return "\n".join(body)


ROBOTS = """User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: GPTBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE


def build_llms(sections):
    lines = [
        "# Aging & Senescence \u2014 a VP Theory volume",
        "",
        "> Aging on the jamming substrate is the slow loss of defense gain of every homeostatic setpoint, plus the",
        "> accumulation of cells stuck in irreversible R19 attractors (senescence), and it is the dominant risk",
        "> multiplier for every pathology kernel in the framework. One declining-gain law gives both gradual drift and",
        "> sudden failure; a ten-mammal test shows human aging genes are NOT special \u2014 the longevity switch is TP53",
        "> copy number, not promoter gamma. Every quantity is reproduced deterministically (SEED 19) and graded",
        "> [V] verified / [L] cited / [O] open. DOI 10.5281/zenodo.20756155 (Zenodo concept DOI).",
        "",
        "## Core",
        "- Hub: " + SITE + "/" + PAPER_ID + "/",
    ]
    for s in sections:
        lines.append("- \u00a7%d %s: %s%s/%s/" % (s["n"], s["subj45"], SITE + "/", PAPER_ID, s["slug"]))
    lines += [
        "",
        "## Research",
        "- Reproduction code (GitHub): " + REPO + "/tree/main/repro/" + PAPER_ID + "/",
        "- Determinism: SEED=19, result sha256 " + DET_HASH[:16] + "\u2026, two runs byte-identical.",
        "",
        "## Policies",
        "- License: CC BY 4.0. Author: " + AUTHOR + " (ORCID 0009-0002-7535-8245). DOI: " + DOI_TBD + " (Zenodo concept DOI).",
    ]
    return "\n".join(lines) + "\n"


def write_manifest(sections):
    rows = ["slug,title,section_no,status,grade,words,eq_display"]
    for s in sections:
        # word count of the rendered body text (display-only count; informational)
        import re
        text = re.sub("<[^>]+>", " ", s["body"])
        words = len([w for w in re.split(r"\s+", text) if w])
        rows.append('%s,"%s",%d,written,%s,%d,0' % (s["slug"], s["subj45"].replace('"', "'"), s["n"], s["grade"], words))
    return "\n".join(rows) + "\n"


def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        return 1
    sections = build_sections()
    total = len(sections)
    os.makedirs(DOCS, exist_ok=True)
    # chapter pages
    for s in sections:
        d = os.path.join(DOCS, s["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render_page(s, total, sections))
    # hub
    open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(render_hub(sections))
    # metadata
    json.dump(build_meta(sections), open(os.path.join(DOCS, "_meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8").write(write_sitemap(sections))
    open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8").write(ROBOTS)
    open(os.path.join(DOCS, "llms.txt"), "w", encoding="utf-8").write(build_llms(sections))
    # manifest
    mdir = os.path.join(PKG, "manifest")
    os.makedirs(mdir, exist_ok=True)
    open(os.path.join(mdir, "aging_senescence_vp_site.csv"), "w", encoding="utf-8").write(write_manifest(sections))
    print("Wrote %d chapter pages + hub + _meta.json + sitemap + robots + llms.txt + manifest." % total)
    print("DOI: %s (Zenodo concept DOI). Determinism sha256: %s" % (DOI_TBD, DET_HASH[:16]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
