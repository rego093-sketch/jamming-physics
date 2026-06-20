#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Immune / Hematologic WRITING phase: per-title canonical SEO HTML generator.
HARD RULE: refuses while gates.writing_locked() is True (research signed off + PHASE=="writing").
WHEN UNLOCKED, follows VP-SPEC v1.8 (../VP_SPEC_v1_8.md): canonical HTML in docs/ (C2); ONE page per
section (C4 sec 6): answer-first <p class="answer"> 40-60 words, self-contained; JSON-LD
ScholarlyArticle + BreadcrumbList; canonical link; claim-strip (grade + LOCK->Derive->Gate + repro);
vp-card per cited locked quantity; ENGLISH body (C0); honest grades + stated obstacles for [O] (C3);
deterministic numbers pulled live from the engine (C1). Emits: docs/<slug>/index.html + hub +
_meta.json + sitemap.xml + robots.txt (7 bots) + llms.txt + assets/css/site.css.

Concept DOI 10.5281/zenodo.20755280 (registered) is shown in the claim-strip, footers, JSON-LD and llms.txt.
"""
import os, sys, json, html

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.join(_HERE, "..")
_DOCS = os.path.join(_PKG, "docs")
for s in ("_engine", "_dynamics", "_oncology", "_therapy", "_verify", "_seams", "_harness"):
    sys.path.insert(0, os.path.join(_PKG, "repro", s))
sys.path.insert(0, os.path.join(_PKG, "inherited"))
import importlib
gates   = importlib.import_module("gates")
eng     = importlib.import_module("vp_imm_engine")
clonal  = importlib.import_module("clonal_inflammation")
lineage = importlib.import_module("lineage_order")
onc     = importlib.import_module("carcinogen_dose_response")
therapy = importlib.import_module("fundamental_therapy")
emg_lin = importlib.import_module("emergent_lineage")     # v0.4.0 emergent developmental order (sim)
emg_kra = importlib.import_module("emergent_kramers")     # v0.4.0 emergent carcinogenesis (sim)
emg_mem = importlib.import_module("emergent_memory")      # v0.5.0 emergent memory lifetime (sim)
emg_chr = importlib.import_module("emergent_chronicity")  # v0.5.0 emergent acute/chronic boundary (sim)
emg_sea = importlib.import_module("emergent_seam")        # v0.5.0 emergent surveillance seam (sim)
emg_sel = importlib.import_module("emergent_selection")   # v0.6.0 emergent clonal-selection threshold (sim)
emg_cmp = importlib.import_module("emergent_competition") # v0.6.0 emergent immunodominance (sim)
emg_thr = importlib.import_module("emergent_therapy")     # v0.6.0 emergent therapy trajectories A&C (sim)
emg_bar = importlib.import_module("emergent_barrier_restoration")    # v0.7.0 emergent Lever B barrier restoration (sim)
emg_clr = importlib.import_module("emergent_surveillance_clearance") # v0.7.0 emergent Lever D surveillance clearance (sim)
emg_rep = importlib.import_module("emergent_repertoire")            # v0.7.0 emergent N-clone repertoire dominance (sim)
emg_reg = importlib.import_module("emergent_regrowth")             # v0.7.0 emergent cytotoxic relapse regrowth (sim)
emg_mat = importlib.import_module("emergent_maturation")          # v0.8.0 emergent affinity maturation / germinal-center loop (sim)
emg_cmb = importlib.import_module("emergent_combination")         # v0.8.0 emergent combination-therapy relapse->cure conversion (sim)
emg_xr  = importlib.import_module("emergent_crossreactivity")     # v0.8.0 emergent original-antigenic-sin / imprinting (sim)
emg_neg = importlib.import_module("emergent_negative_selection")  # v0.9.0 emergent central tolerance / clonal deletion (sim)
emg_pb  = importlib.import_module("emergent_prime_boost")         # v0.9.0 emergent prime-boost scheduling (sim)
emg_aut = importlib.import_module("emergent_autoimmunity")        # v0.9.0 emergent autoimmune tolerance break (sim)
emg_per = importlib.import_module("emergent_peripheral_tolerance") # v0.10.0 emergent peripheral tolerance / regulatory suppression (sim)
emg_exh = importlib.import_module("emergent_exhaustion")          # v0.10.0 emergent immune exhaustion / chronic-antigen hyporesponsiveness (sim)
emg_hor = importlib.import_module("emergent_hormesis")            # v0.10.0 emergent tolerance-immunity dose window (sim)
emg_ret = importlib.import_module("emergent_retolerization")      # v0.11.0 emergent therapeutic re-tolerization (sim)
emg_rec = importlib.import_module("emergent_reconstitution")      # v0.11.0 emergent immunodeficiency reconstitution (sim)
emg_sep = importlib.import_module("emergent_sepsis_latch")        # v0.11.0 emergent systemic inflammatory latch / break window (sim)
emg_alo = importlib.import_module("emergent_allotolerance")       # v0.11.0 emergent transplant allo-tolerance induction (sim)
emg_cyt = importlib.import_module("emergent_cytopenia")           # v0.11.0 emergent lineage-targeted autoimmune cytopenia (sim)
emg_isn = importlib.import_module("emergent_immunosenescence")    # v0.14.0 emergent thymic involution / immunosenescence (sim)
emg_dbr = importlib.import_module("emergent_durable_boost")       # v0.14.0 emergent durability-optimal re-boosting (sim)
emg_sen = importlib.import_module("emergent_sensitization")       # T29 allergic sensitization / desensitization (wired in v0.15.0)
seam    = importlib.import_module("seam_wiring")                  # v0.16.0 cross-package seam layer (section 16)
harness = importlib.import_module("cross_package_harness")       # v0.16.0 live cross-package harness (section 17, out of gate)

PAPER_ID = "immune_hematologic_vp_site"
CODE     = "imm"
SHORT    = "Immune/Hematologic"
FULLTITLE = "Immune & Hematologic Emergence (VP / Jamming Physics)"
ORCID    = "https://orcid.org/0009-0002-7535-8245"
AUTHOR   = "Young Jae Lee"
REPO     = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/" + PAPER_ID
BASE     = "https://jamming-physics.org/" + PAPER_ID
CCBY     = "https://creativecommons.org/licenses/by/4.0/"
DOI      = "10.5281/zenodo.20755280"                  # concept DOI (registered)
DOI_URL  = "https://doi.org/" + DOI

GRADE_CLASS = {"[F]": "g-forced", "[V]": "g-verified", "[H]": "g-hypothesis", "[O]": "g-open"}


def esc(s): return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------------------------------
# live deterministic numbers
# --------------------------------------------------------------------------------------------------
def numbers():
    base = eng.circulate()
    G = {o["organ"]: o["gamma"] for o in base["organs"]["organs"] if o.get("gamma") is not None}
    import vp_substrate as vs
    sp = {k: round(vs.spinodal(v), 6) for k, v in G.items()}
    ba = {k: round(vs.barrier(v), 6) for k, v in G.items()}
    t1 = clonal.t1_clonal_activation(G)
    t2 = clonal.t2_inflammation_hysteresis(G)
    t4 = clonal.t4_immune_memory(G)
    t3 = lineage.t3_lineage_order(G)
    orep = onc.oncology_report(G)
    trep = therapy.therapy_report(G)
    order = base["organs"]["gamma_order_ascending"]
    prov = eng.provenance_report()                                  # v0.3.0 NCBI offline check
    _inh = os.path.join(_PKG, "inherited")
    ncbi_ver = json.load(open(os.path.join(_inh, "ncbi_verification.json"), encoding="utf-8"))
    ncbi_ref = json.load(open(os.path.join(_inh, "ncbi_gene_refseq.json"), encoding="utf-8"))
    el = emg_lin.run(G)["T6"]["result"]                             # v0.4.0 emergent lineage race
    ek = emg_kra.run(G)["T7"]["result"]                             # v0.4.0 emergent carcinogenesis
    em = emg_mem.run(G)["T8"]["result"]                             # v0.5.0 emergent memory lifetime
    ec = emg_chr.run(G)["T9"]["result"]                             # v0.5.0 emergent chronicity boundary
    es = emg_sea.run(G)["T10"]["result"]                            # v0.5.0 emergent surveillance seam
    esel = emg_sel.run(G)["T11"]["result"]                          # v0.6.0 emergent clonal-selection threshold
    ecmp = emg_cmp.run(G)["T12"]["result"]                          # v0.6.0 emergent immunodominance
    ethr = emg_thr.run(G)["T13"]["result"]                          # v0.6.0 emergent therapy trajectories A&C
    ebar = emg_bar.run(G)["T14"]["result"]                          # v0.7.0 emergent Lever B barrier restoration
    eclr = emg_clr.run(G)["T15"]["result"]                          # v0.7.0 emergent Lever D surveillance clearance
    erep = emg_rep.run(G)["T16"]["result"]                          # v0.7.0 emergent N-clone repertoire dominance
    ereg = emg_reg.run(G)["T17"]["result"]                          # v0.7.0 emergent cytotoxic relapse regrowth
    emat = emg_mat.run(G)["T18"]["result"]                          # v0.8.0 emergent affinity maturation
    ecmb = emg_cmb.run(G)["T19"]["result"]                          # v0.8.0 emergent combination-therapy conversion
    exr  = emg_xr.run(G)["T20"]["result"]                           # v0.8.0 emergent original-antigenic-sin imprinting
    eneg = emg_neg.run(G)["T21"]["result"]                          # v0.9.0 emergent central tolerance / clonal deletion
    epb  = emg_pb.run(G)["T22"]["result"]                           # v0.9.0 emergent prime-boost scheduling
    eaut = emg_aut.run(G)["T23"]["result"]                          # v0.9.0 emergent autoimmune tolerance break
    eper = emg_per.run(G)["T24"]["result"]                          # v0.10.0 emergent peripheral tolerance / regulatory suppression
    eexh = emg_exh.run(G)["T25"]["result"]                          # v0.10.0 emergent immune exhaustion
    ehor = emg_hor.run(G)["T26"]["result"]                          # v0.10.0 emergent tolerance-immunity dose window
    eret = emg_ret.run(G)["T27"]["result"]                          # v0.11.0 emergent therapeutic re-tolerization
    erec = emg_rec.run(G)["T30"]["result"]                          # v0.11.0 emergent immunodeficiency reconstitution
    esep = emg_sep.run(G)["T31"]["result"]                          # v0.11.0 emergent systemic inflammatory latch / break window
    ealo = emg_alo.run(G)["T32"]["result"]                          # v0.11.0 emergent transplant allo-tolerance induction
    ecyt = emg_cyt.run(G)["T33"]["result"]                          # v0.11.0 emergent lineage-targeted autoimmune cytopenia
    eisn = emg_isn.run(G)["T34"]["result"]                          # v0.14.0 emergent thymic involution / immunosenescence
    edbr = emg_dbr.run(G)["T35"]["result"]                          # v0.14.0 emergent durability-optimal re-boosting
    esen = emg_sen.run(G)["T29"]["result"]                          # T29 allergic sensitization / desensitization (wired in v0.15.0)
    # v0.16.0 cross-package seam layer (section 16) + live harness contract (section 17). Both sibling-free:
    # validate_seams()/immune_side_contract() compute only this volume's owned reference values, and each
    # layer carries its OWN 2xsha256 separate from the engine emit() hash. No sibling is loaded at build time.
    seamv = seam.validate_seams()
    _, seam_sha = seam.digest()
    hcontract = harness.immune_side_contract()
    _, harness_sha = harness.digest()
    return dict(G=G, sp=sp, ba=ba, t1=t1, t2=t2, t4=t4, t3=t3, orep=orep, trep=trep, order=order,
                prov=prov, ncbi_ver=ncbi_ver, ncbi_ref=ncbi_ref, el=el, ek=ek, em=em, ec=ec, es=es,
                esel=esel, ecmp=ecmp, ethr=ethr, ebar=ebar, eclr=eclr, erep=erep, ereg=ereg,
                emat=emat, ecmb=ecmb, exr=exr, eneg=eneg, epb=epb, eaut=eaut,
                eper=eper, eexh=eexh, ehor=ehor,
                eret=eret, erec=erec, esep=esep, ealo=ealo, ecyt=ecyt, eisn=eisn, edbr=edbr, esen=esen,
                seamv=seamv, seam_sha=seam_sha, hcontract=hcontract, harness_sha=harness_sha)


# --------------------------------------------------------------------------------------------------
# vp-card (self-contained locked-quantity card) + page template
# --------------------------------------------------------------------------------------------------
def vp_card(token, label, meaning, grade, anchor_text, anchor_href=None):
    a = ('<a href="%s">%s</a>' % (esc(anchor_href), esc(anchor_text))) if anchor_href else esc(anchor_text)
    return ('<aside class="vp-card" data-locked="%s"><b>%s</b> — %s <b>%s</b> %s</aside>'
            % (esc(token), esc(label), esc(meaning), esc(grade), a))


def page(slug, N, title, descr, answer, abstract, grade_token, body, cards, prev_, next_, n_total):
    gclass = GRADE_CLASS.get(grade_token, "g-open")
    crumb_short = title if len(title) <= 40 else title[:40]
    ld_article = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": title,
        "isPartOf": {"@type": "CreativeWork", "name": FULLTITLE, "sameAs": [REPO, DOI_URL], "identifier": DOI},
        "position": N,
        "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI},
        "sameAs": DOI_URL,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "license": CCBY,
    }
    ld_crumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jamming-physics.org/"},
            {"@type": "ListItem", "position": 2, "name": SHORT, "item": BASE + "/"},
            {"@type": "ListItem", "position": 3, "name": "§%d %s" % (N, crumb_short)}]}
    prev_html = ('<a rel="prev" href="/%s/%s/">← §%d</a>' % (PAPER_ID, prev_[0], N - 1)) if prev_ else '<span></span>'
    next_html = ('<a rel="next" href="/%s/%s/">§%d →</a>' % (PAPER_ID, next_[0], N + 1)) if next_ else '<span></span>'
    cards_html = ("\n".join(cards)) if cards else ""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {short} §{N} | Jamming Physics</title>
<meta name="description" content="{descr}">
<link rel="canonical" href="{base}/{slug}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld_article}
</script>
<script type="application/ld+json">
{ld_crumb}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › <a href="/{paper}/">{short}</a> › §{N}</nav></header>
<main>
<h1>{title}</h1>

<p class="answer">{answer}</p>

<p class="abstract">{abstract}</p>

<aside class="claim-strip">
  <span class="grade {gclass}">{grade_token} grade</span>
  <span class="gate">LOCK → Derive → Gate</span>
  <a href="{repo}/{slug}/" rel="noopener">reproduction code (GitHub)</a>
  <span class="doi"><a href="{doi_url}" rel="noopener">DOI: {doi}</a></span>
</aside>

{cards}

{body}

<nav class="pn">
  {prev_html}
  <a href="/{paper}/">paper contents</a>
  {next_html}
</nav>
</main>
<footer>{author} · <a href="{orcid}" rel="noopener">ORCID</a> · <a href="{doi_url}" rel="noopener">DOI: {doi}</a> · <a href="{ccby}" rel="noopener">CC BY 4.0</a> · §{N} of {n_total}</footer>
</body>
</html>
""".format(title=esc(title), short=esc(SHORT), N=N, descr=esc(descr), base=BASE, slug=esc(slug),
           ld_article=json.dumps(ld_article, ensure_ascii=False),
           ld_crumb=json.dumps(ld_crumb, ensure_ascii=False),
           paper=PAPER_ID, answer=esc(answer), abstract=abstract, gclass=gclass,
           grade_token=esc(grade_token), repo=REPO, cards=cards_html, body=body,
           prev_html=prev_html, next_html=next_html, author=esc(AUTHOR), orcid=ORCID,
           ccby=CCBY, doi=esc(DOI), doi_url=DOI_URL, n_total=n_total)


# --------------------------------------------------------------------------------------------------
# section content (English bodies, deterministic numbers spliced in)
# --------------------------------------------------------------------------------------------------
def build_sections(NUM):
    G, sp, ba = NUM["G"], NUM["sp"], NUM["ba"]
    bm, sB, ord_ = G["bone_marrow_hematopoiesis"], sp["bone_marrow_hematopoiesis"], NUM["order"]
    t1r = NUM["t1"]["rows"][0]
    aml = NUM["orep"]["AML_dose_response"]
    trep = NUM["trep"]
    A = trep["lever_A"]["rows"][0]; B = trep["lever_B"]["rows"][0]
    Daml = trep["lever_D"]["sites"]["AML"]
    esel = NUM["esel"]; ecmp = NUM["ecmp"]; ethr = NUM["ethr"]   # v0.6.0 emergent threshold / immunodominance / therapy
    ebar = NUM["ebar"]; eclr = NUM["eclr"]; erep = NUM["erep"]; ereg = NUM["ereg"]   # v0.7.0 Lever B / Lever D / repertoire / regrowth
    emat = NUM["emat"]; ecmb = NUM["ecmb"]; exr = NUM["exr"]   # v0.8.0 affinity maturation / combination therapy / antigenic imprinting
    eneg = NUM["eneg"]; epb = NUM["epb"]; eaut = NUM["eaut"]   # v0.9.0 central tolerance / prime-boost scheduling / autoimmune break
    eper = NUM["eper"]; eexh = NUM["eexh"]; ehor = NUM["ehor"]   # v0.10.0 peripheral tolerance / exhaustion / dose window
    eret = NUM["eret"]; erec = NUM["erec"]; esep = NUM["esep"]   # v0.11.0 re-tolerization / reconstitution / systemic latch
    ealo = NUM["ealo"]; ecyt = NUM["ecyt"]   # v0.11.0 allo-tolerance induction / lineage-targeted cytopenia
    eisn = NUM["eisn"]; edbr = NUM["edbr"]   # v0.14.0 thymic involution / immunosenescence; durability-optimal re-boosting
    esen = NUM["esen"]   # v0.15.0 wired: allergic sensitization / desensitization (T29)

    gamma_card = vp_card("gamma", "γ (promoter stacking)",
        "−mean SantaLucia-1998 nearest-neighbour stacking ΔG37 over the promoter window TSS−2000..+500; "
        "owned by the DNA volume (SSOT), measured here for the four master genes "
        "(RUNX1 1.3225, TLX1 1.4228, FOXN1 1.4533, PAX5 1.4892). All four promoter sequences are "
        "byte-exact verified against the live NCBI reference assembly (GRCh38.p14), so γ is primary-source "
        "grounded, not just cached.",
        "[L]", "canonical derivation: DNA volume §γ", None)
    spinodal_card = vp_card("spinodal", "spinodal |h|=2(γ/3)^1.5",
        "the drive magnitude past which the opposite basin disappears, making the R19 flip discontinuous; "
        "it sets every activation / erase / re-flip threshold in this volume.",
        "[F]", "canonical derivation: substrate R19", None)
    barrier_card = vp_card("barrier", "barrier = γ²/4",
        "the energy barrier between the two basins; it ranks state stability and sets the Kramers crossing "
        "rate, so larger-γ organs hold memory and resist transformation more strongly.",
        "[F]", "canonical derivation: substrate R19", None)

    secs = []

    # 1 — T1 clonal selection
    secs.append(dict(
        slug="01-clonal-selection-saddle-node-threshold", N=1,
        title="Clonal Selection as a Saddle-Node Threshold",
        descr="Lymphocyte clonal selection is an R19 saddle-node crossing: a clone activates exactly when "
              "antigen-affinity drive exceeds the spinodal, and stays tolerant below it.",
        answer="Clonal selection is a saddle-node crossing of the R19 switch. Rather than assume the threshold, this "
               "volume simulates a rising antigen-affinity signal under noise and measures it: the commit-drive equals "
               "each organ's spinodal |h|=2(γ/3)^1.5 and orders by γ, while sub-spinodal drive stays tolerant. "
               "Immunodominance, maturation, imprinting, tolerance and exhaustion follow from the same shared-pool "
               "competition. Grade [V].",
        abstract="The activation threshold is measured, not posited: a rising-affinity simulation commits at the "
                 "spinodal organ-by-organ (marrow ratio %.3f×, lymphoid %.3f×, approached from below by thermal "
                 "activation), and a sub-spinodal drive stays tolerant (P(commit)=%.3f). Immunodominance emerges from "
                 "competition for a shared antigen pool: a subdominant clone that commits with probability %.2f alone is "
                 "competitively excluded to %.2f while the dominant clone commits first (P=%.2f)."
                 % (esel["commit_drive"]["bone_marrow_hematopoiesis"]["commit_drive_over_spinodal"],
                    esel["commit_drive"]["lymphoid_adaptive"]["commit_drive_over_spinodal"],
                    esel["tolerance_commitment_bracket"]["bone_marrow_hematopoiesis"]["p_commit_subspinodal"],
                    ecmp["sweep"][-1]["subdominant_commit_alone"], ecmp["sweep"][-1]["subdominant_commit_competition"],
                    ecmp["sweep"][-1]["P_dominant_commits_first"]),
        grade_token="[V]",
        cards=[gamma_card, spinodal_card],
        body="""<h2>The switch, not a dial</h2>
<p>Clonal selection is discontinuous by construction. A clone is a single R19 switch whose drive is set by
antigen affinity; the saddle-node at the spinodal means there is no graded half-activated clone, only a
committed crossing.</p>
<p>Self-tolerance is the same statement read backwards: any clone whose affinity drive stays below the
spinodal never leaves the OFF basin, so it cannot be activated against self. No separate tolerance rule is
needed — it is the sub-spinodal region of the one switch.</p>
<h2>The activation threshold is measured, not assumed</h2>
<p>Rather than read the threshold off the closed-form spinodal, the volume <em>simulates</em> it. A resting
clone is driven by a slowly rising antigen-affinity signal under independent cellular noise, and the drive at
which it first crosses the ridge is <em>measured</em>. The commit-drive that comes out equals each organ's own
spinodal (commit-drive ÷ spinodal = %.3f, %.3f, %.3f, %.3f for marrow, spleen, thymus, lymphoid), so the
saddle-node threshold is confirmed dynamically. It is approached from just below the spinodal because thermal
activation lets a clone cross while the shrinking barrier still exists; the ratio rises toward 1 as the noise
falls.</p>
<p>The measured thresholds order by γ — a higher-γ (deeper-well) compartment demands a stronger affinity
signal to activate. And the bracket straddles the spinodal: a drive clearly below it essentially never commits
however long it is held (self-tolerance, P(commit)=%.3f on marrow), while a drive clearly above it commits with
probability %.3f. Only the absolute noise scale D is left [O].</p>
<h2>Immunodominance emerges from clonal competition</h2>
<p>A real response is not one clone in isolation but many clones of the adaptive compartment racing for one
finite antigen pool. The volume simulates two clones of the same γ, differing only in affinity, sharing one
pool that committed clones deplete. Immunodominance is then <em>measured</em>, not imposed: the higher-affinity
clone reaches its spinodal first, commits, and consumes the shared antigen, which starves the lower-affinity
clone. A subdominant clone that would commit with probability %.2f on its own is competitively excluded to
%.2f, and the dominant clone commits first with probability %.2f.</p>
<p>The hierarchy sharpens monotonically with the affinity gap and — honestly — vanishes when the gap does: at
equal affinity the contest is a symmetric coin-flip (P(first)≈%.2f), with no spurious winner. The depth of the
hierarchy, set by the consumption rate and the noise scale, is [O]; its existence, direction, and monotonicity
are measured.</p>
<h2>A repertoire concentrates on a few clones</h2>
<p>Scaling the two-clone contest to a full repertoire — N clones of the adaptive compartment with a spread of
affinities sharing one pool — turns dominance into a measured concentration. With N=%d clones the response
collapses onto an effective %.1f clones (the participation ratio of the measured commit probabilities): the
high-affinity clones capture it and the rest are competitively excluded. Widening the affinity spread sharpens
the focus — the effective number falls from %.1f at equal affinity to %.1f at the widest spread — and a larger
repertoire concentrates further still relative to its size, the shared pool sustaining only a few committers.
At equal affinity the response stays evenly shared, with no spurious winner. The absolute depth is [O]; the
concentration and its scaling with spread and repertoire size are measured.</p>
<h2>Affinity maturation matures the repertoire round over round</h2>
<p>A germinal centre is the repertoire contest run as a Darwinian loop. Each round the higher-affinity clones
commit first and deplete the shared pool — excluding the slow clones exactly as immunodominance does — and the
committed parents are re-seeded with <em>symmetric</em> somatic hypermutation before the next round. Nothing
about &ldquo;improvement&rdquo; is imposed: mutation is an unbiased random walk and selection is only the
competition outcome. Yet the measured mean affinity of the responding set <em>rises</em> round over round,
climbing from %.3f to %.3f over %d rounds (gain %.3f).</p>
<p>The rise is causally dissected, not assumed. It needs mutation: at zero hypermutation the gain stalls
(%.4f), and it accelerates as the mutation step grows (gain %.3f → %.3f → %.3f). It needs competition: an
effectively unlimited pool removes the selection pressure and the affinity drifts neutrally (gain %.4f ≈ 0).
And the pressure itself has an honest optimum — too tight a pool starves even the winners, so the gain peaks at
an intermediate pool (%.3f at the optimum vs %.3f in the weak regime) rather than rising forever. Direction,
mutation-dependence, competition-dependence and the inverted-U are measured; the absolute maturation rate stays
[O].</p>
<h2>Imprinting biases recall toward experienced clones</h2>
<p>Re-exposure to a drifted antigen is a two-clone contest of a different kind: an experienced memory clone
with a recall head-start (it starts nearer the ridge) against a fresh naïve clone that is fully OFF but better
matched to the new antigen. The memory clone's affinity degrades with antigenic distance, so beyond a crossover
distance (here d≈%.3f) the naïve clone is strictly the better fit. The bias is then <em>measured</em>: at an
intermediate distance the experienced clone is still preferentially recalled even though the naïve clone is
better matched — P(memory wins)=%.3f at the first distance where the naïve clone already holds the affinity
edge. This is original antigenic sin emerging from competition, not a fitted rule.</p>
<p>The bias is bounded and causally controlled. It decays monotonically with antigenic distance — P(memory)
falls %.3f → %.3f → %.3f across the better-matched zone — until the naïve clone takes over (P(naïve)=%.3f at the
farthest distance). And it is experience-driven, not affinity-driven: removing the recall head-start abolishes
it entirely, so in the same zone the better-matched naïve clone always wins (P(memory) collapses to %.3f, %.3f,
%.3f). The existence of the imprint, its decay with distance and the head-start control are measured; the
absolute imprinting magnitude stays [O].</p>
<h2>Central tolerance deletes self-reactive clones</h2>
<p>Negative selection is clonal selection read with the opposite sign. The same rising-affinity ramp is run on a
self-reactive clone in the thymic context, but now a crossing to ON marks the clone for <em>deletion</em>, not
activation. The measured deletion drive is again each organ's spinodal (deletion-drive ÷ spinodal = %.3f, %.3f,
%.3f, %.3f for marrow, spleen, thymus, lymphoid) and orders by γ exactly as activation does — the very same
saddle-node, now culling rather than committing. A sub-threshold self-drive is ignored (P(delete)=%.3f on
marrow) and a supra-threshold one is reliably deleted (P=%.3f).</p>
<p>The consequence is a measured tolerance ceiling on what leaves the thymus. Educating a uniform spread of
self-affinities through the deletion channel caps the exported self-affinity at the spinodal (max exported =
%.3f× spinodal) and empties the autoreactive tail (exported-autoreactive fraction %.3f with the channel on),
while %.1f%% of the self-reactive repertoire is deleted. Switching the channel off lets that tail straight
through — exported-autoreactive jumps to %.3f and the ceiling rises to %.2f× — so central tolerance is
<em>required</em>, not incidental. Only the absolute deletion rate and the width of the escaped near-threshold
sliver are [O].</p>
<h2>Prime-boost scheduling has an interior optimum</h2>
<p>A vaccination campaign is the maturation loop asked a temporal question: at a fixed campaign length, how does
the matured affinity depend on the <em>spacing</em> of the boosts? The only added physics is antigen
pharmacokinetics — each boost tops up a slowly-clearing depot, and every round runs the measured maturation
competition at the current depot level. The answer is <em>measured</em>, an inverted-U in the boost interval with
an interior optimum: boosting every round over-supplies the depot (mean pool %.2f) into the weak large-pool
regime of maturation, so the gain is starved to %.3f; the optimum sits at an intermediate interval (gain %.3f at
interval %d); and spacing the boosts too far under-uses the fixed campaign (gain %.3f).</p>
<p>The interior optimum is the temporal face of the maturation inverted-U, and it is causally controlled.
Clamping the depot's carrying capacity down to the productive pool removes the over-supply penalty — now even the
most frequent schedule only ever holds a productive pool, so more boosts is strictly better and the optimum
collapses to the most-frequent boundary (gain %.3f at interval %d). The existence of an interior optimum and the
over-supply mechanism are measured; the absolute optimal interval (depot clearance, dose, campaign length, noise
scale D) stays [O].</p>
<h2>Peripheral tolerance re-contains the escaped clone</h2>
<p>Central deletion leaves an escaped near-threshold sliver, and (next volume) an inflammatory insult can break it.
A second, peripheral layer of tolerance &mdash; regulatory suppression &mdash; guards exactly that sliver. The
volume models it as a suppressor field that subtracts from the escaped self-clone's drive, and <em>measures</em>
the suppression at which the clone is re-contained. The threshold that comes out is the saddle-node
<em>complement</em>: &sigma;<sub>crit</sub> = (residual self-drive + insult) &minus; spinodal, organ by organ
(&sigma;<sub>crit</sub> = %.3f, %.3f for marrow and lymphoid, both matching the %.3f&times; overshoot). The
regulatory field cancels exactly the amount by which the escaped clone's total drive overshoots the switch &mdash;
suppression and drive are one currency read with opposite sign.</p>
<p>The two tolerance layers add. Sweeping the escapee's residual self-drive (its negative-selection depth), the
required suppression rises one-for-one with it (measured slope %.3f &asymp; 1): a deeper escapee, closer to having
broken through central deletion, needs proportionally more peripheral suppression to stay quiescent. And
suppression is <em>required</em> &mdash; with the field off the escaped clone driven by a supra-threshold insult
breaks (P=%.3f), and engaging sufficient suppression re-contains it (P=%.3f). Only the absolute suppression
strength (the map from &sigma; to a regulatory-cell count) and the escaped-sliver width are [O].</p>
<h2>Chronic antigen exhausts the response, reversibly</h2>
<p>Affinity maturation is the productive arc of a response; exhaustion is its dynamical mirror. The volume drives a
committed clone under <em>persistent</em> antigen and couples in an accumulating feedback &mdash; an inhibitory
tone that builds while the cell is ON and antigen is present, and relaxes only when antigen is withdrawn. The
response is <em>measured</em> to rise to a peak (%.3f) and then collapse to a hyporesponsive floor (%.3f, drop
%.3f) as the feedback accumulates: chronic stimulation extinguishes the very response it drives. The collapse needs
the feedback &mdash; with the coupling off the same chronic drive holds the response up indefinitely (floor
%.3f).</p>
<p>The silencing is reversible, and gated by the switch's own bifurcation. Because the committed cell sits in a
bistable ON basin, the feedback must push it past its <em>negative</em> saddle-node to force it OFF &mdash; so the
onset is <em>measured</em> at a coupling (%.3f) near the closed-form reverse-saddle-node estimate (%.3f). And it is
a functional silencing, not a deletion: withdrawing antigen lets the feedback decay, so a re-challenge recovers the
response (%.3f) while a continuously-stimulated clone stays extinguished (%.3f). Only the absolute exhaustion rate
(accumulation time, coupling, noise scale D) is [O].</p>""" % (
            esel["commit_drive"]["bone_marrow_hematopoiesis"]["commit_drive_over_spinodal"],
            esel["commit_drive"]["spleen"]["commit_drive_over_spinodal"],
            esel["commit_drive"]["thymus"]["commit_drive_over_spinodal"],
            esel["commit_drive"]["lymphoid_adaptive"]["commit_drive_over_spinodal"],
            esel["tolerance_commitment_bracket"]["bone_marrow_hematopoiesis"]["p_commit_subspinodal"],
            esel["tolerance_commitment_bracket"]["bone_marrow_hematopoiesis"]["p_commit_supraspinodal"],
            ecmp["sweep"][-1]["subdominant_commit_alone"], ecmp["sweep"][-1]["subdominant_commit_competition"],
            ecmp["sweep"][-1]["P_dominant_commits_first"], ecmp["sweep"][0]["P_dominant_commits_first"],
            erep["baseline"]["N"], erep["baseline"]["N_eff"],
            erep["experiment_A_vary_spread"][0]["N_eff"], erep["experiment_A_vary_spread"][-1]["N_eff"],
            emat["baseline_trajectory"][0]["mean_responding_affinity"],
            emat["baseline_trajectory"][-1]["mean_responding_affinity"],
            emat["rounds"], emat["baseline_affinity_gain"],
            emat["experiment_A_sweep_mutation"][0]["affinity_gain"],
            emat["experiment_A_sweep_mutation"][1]["affinity_gain"],
            emat["experiment_A_sweep_mutation"][2]["affinity_gain"],
            emat["experiment_A_sweep_mutation"][3]["affinity_gain"],
            emat["control_unlimited_pool"]["affinity_gain"],
            emat["peak_pool_gain"], emat["weak_pool_gain"],
            exr["crossover_distance"],
            exr["experienced_sweep"][2]["P_memory_dominates"],
            exr["experienced_sweep"][2]["P_memory_dominates"],
            exr["experienced_sweep"][3]["P_memory_dominates"],
            exr["experienced_sweep"][4]["P_memory_dominates"],
            exr["experienced_sweep"][4]["P_naive_dominates"],
            exr["control_no_recall_sweep"][2]["P_memory_dominates"],
            exr["control_no_recall_sweep"][3]["P_memory_dominates"],
            exr["control_no_recall_sweep"][4]["P_memory_dominates"],
            eneg["deletion_threshold"]["bone_marrow_hematopoiesis"]["deletion_threshold_over_spinodal"],
            eneg["deletion_threshold"]["spleen"]["deletion_threshold_over_spinodal"],
            eneg["deletion_threshold"]["thymus"]["deletion_threshold_over_spinodal"],
            eneg["deletion_threshold"]["lymphoid_adaptive"]["deletion_threshold_over_spinodal"],
            eneg["ignorance_deletion_bracket"]["bone_marrow_hematopoiesis"]["p_delete_subthreshold"],
            eneg["ignorance_deletion_bracket"]["bone_marrow_hematopoiesis"]["p_delete_suprathreshold"],
            eneg["exported_repertoire_with_deletion"]["max_exported_self_affinity"],
            eneg["exported_repertoire_with_deletion"]["exported_autoreactive_fraction"],
            eneg["exported_repertoire_with_deletion"]["fraction_deleted"] * 100.0,
            eneg["exported_repertoire_without_deletion"]["exported_autoreactive_fraction"],
            eneg["exported_repertoire_without_deletion"]["max_exported_self_affinity"],
            epb["oversupply_on_sweep"][0]["mean_depot_pool"],
            epb["oversupply_on_sweep"][0]["affinity_gain"],
            epb["peak_gain"], epb["optimal_interval"],
            epb["oversupply_on_sweep"][-1]["affinity_gain"],
            epb["oversupply_off_sweep"][0]["affinity_gain"], epb["control_optimal_interval"],
            eper["suppression_threshold"]["bone_marrow_hematopoiesis"]["sigma_crit_over_spinodal"],
            eper["suppression_threshold"]["lymphoid_adaptive"]["sigma_crit_over_spinodal"],
            eper["saddle_node_excess_ref"], eper["sigma_vs_residual_slope"],
            eper["suppression_required"]["p_break_sigma0"], eper["suppression_required"]["p_break_sigma_040"],
            eexh["trajectory"]["peak"], eexh["trajectory"]["floor"], eexh["trajectory"]["drop"],
            eexh["control_kappa0"]["floor"],
            eexh["onset"]["measured_kappa"], eexh["onset"]["predicted_reverse_saddle_node"],
            eexh["reversibility"]["rechallenge_peak"], eexh["reversibility"]["continued_chronic"]),
    ))

    # 2 — T2 hysteresis
    secs.append(dict(
        slug="02-inflammation-bistable-hysteresis", N=2,
        title="Inflammation as Bistable Hysteresis",
        descr="Acute inflammation resolves but chronic inflammation latches because the R19 switch is "
              "hysteretic: a brief sub-spinodal pulse decays, a sustained supra-spinodal drive stays ON.",
        answer="Inflammation is bistable hysteresis of the R19 switch. Rather than assume the boundary, this volume "
               "simulates stochastic pulses and measures it: the critical amplitude equals the spinodal "
               "organ-by-organ, sub-spinodal insults never latch, and dose trades off against duration. The autoimmune "
               "tolerance break is the same latch on an escaped self-clone. Grade [V].",
        abstract="The chronicity boundary is measured by direct stochastic pulse simulation: the critical amplitude "
                 "equals the spinodal for every organ (within 1%%), a sub-spinodal insult never latches "
                 "(P=%.3f at the longest duration), and the dose×duration tradeoff is monotone — the latched "
                 "pathological basin." % NUM["ec"]["subspinodal_p_latch_long_duration"],
        grade_token="[V]",
        cards=[spinodal_card],
        body="""<h2>Two fates from one switch</h2>
<p>Resolution and chronicity are not two mechanisms. They are the two outcomes of a single hysteretic switch
driven for different durations and amplitudes.</p>
<p>An acute insult that stays below the spinodal cannot leave the OFF basin; once the insult clears the state
relaxes back — the inflammation resolves on its own. A drive that exceeds the spinodal and persists long
enough crosses into the ON basin and is then held there by the barrier even after the drive is withdrawn.</p>
<h2>The latched basin</h2>
<p>Chronic inflammation is therefore a memory phenomenon: the system records the supra-threshold history in
its basin occupancy. This is the same barrier that, in the therapy volume, must be acted on to reverse a
committed state — culling mediators without moving the basin lets it refill.</p>
<h2>The chronicity boundary emerges in the amplitude × duration plane</h2>
<p>Rather than assert that acute resolves and chronic latches, the volume <em>simulates</em> the stochastic R19
switch directly: each organ's OFF state is hit with a rectangular insult of a given amplitude and duration under
independent cellular noise, the drive is withdrawn, and whether the state has latched ON is <em>measured</em>.
The critical amplitude that comes out is the spinodal itself, organ-by-organ (a<sub>crit</sub>/spinodal = %.3f,
%.3f, %.3f, %.3f for the four organs — all within 1%%), so the analytic threshold is confirmed dynamically, not
assumed.</p>
<p>Two further facts emerge. A sub-spinodal insult never becomes chronic no matter how long it is applied (latch
probability only %.3f at the longest duration tested), and above the spinodal the required duration trades off
against amplitude monotonically: the critical dwell falls %d → %d → %d → %d steps as the amplitude rises
1.10× → 1.25× → 1.50× → 2.00× the spinodal. The boundary is thus a measured curve in the amplitude × duration
plane, with only the absolute noise scale D (transition sharpness) left [O].</p>
<h2>Tolerance breaks as a bistable latch</h2>
<p>The same hysteresis has a pathological mirror in autoimmunity. Take a self-reactive clone that escaped central
tolerance (§1): its residual self-antigen drive sits just below the spinodal, so the switch is bistable — a
resting tolerant basin and a self-sustaining autoreactive basin both exist. Hit with an inflammatory insult
pulse, the break boundary is <em>measured</em> to be the switch's saddle-node. Across a sweep of the residual
self-drive the critical <em>total</em> drive (residual + insult) stays at the spinodal (sum = %.3f, %.3f, %.3f,
%.3f, %.3f× spinodal as the residual rises 0 → 0.8×), so self-antigen and inflammation are interchangeable ways
of reaching the same ridge — the critical insult falls %.3f → %.3f → %.3f× as the residual self-drive deepens.</p>
<p>The break is irreversible — a pathological memory. A supra-threshold insult latches the clone ON and it
<em>stays</em> ON after the insult is withdrawn to the persisting self-drive (P(autoreactive)=%.3f, unchanged
when the settle is tripled), whereas a sub-threshold insult resolves (P=%.3f) and a deeply-tolerant clone under a
sub-spinodal total never breaks (P=%.3f). The dose×duration tradeoff carries over (critical dwell %d → %d → %d
steps as the insult strengthens), and — the link back to §1 — because the critical insult shrinks as the residual
self-drive nears the deletion threshold, <em>deeper</em> negative selection leaves only smaller-residual
survivors and so <em>raises</em> the insult needed to break tolerance. Autoimmune susceptibility is set by
deletion depth; only the absolute break rate (residual depth, insult amplitude/duration, noise scale D) is
[O].</p>
<h2>A tolerance&ndash;immunity dose window between ignorance and deletion</h2>
<p>Self-antigen dose has two safe regimes and one dangerous one between them, and the volume <em>measures</em>
where the edges fall by composing two of its own processes over a swept dose: central deletion (&sect;1) removes a
high-dose clone, while the inflammatory break (above) fires an escaped clone whose residual drive is large enough.
The net break-risk is single-peaked in dose &mdash; %.3f at low dose (the clone is ignored), peaking at an
intermediate dose (here d=%.2f), and %.3f at high dose (the clone is deleted, central tolerance). The honest sign
is the dual of the textbook &ldquo;safe window&rdquo;: the interior is the <em>danger</em> band, flanked by two
safe regimes &mdash; ignorance below and central deletion above.</p>
<p>The band's edges are mechanistic and move predictably. The lower (break) edge = spinodal &minus; insult, so it
tracks the insult one-for-one: as the insult rises 0.2 &rarr; 0.4 &rarr; 0.6&times; the lower edge falls %.3f
&rarr; %.3f &rarr; %.3f (measured slope %.3f &asymp; &minus;1), and d<sub>lo</sub> + insult stays at the spinodal
(%.3f, %.3f, %.3f&times;) &mdash; the &sect;1 commit threshold. The upper (deletion) edge is insult-independent
(fixed at %.3f&times; by central tolerance), so the band <em>width</em> grows one-for-one with the insult (%.3f
&rarr; %.3f as the insult widens, slope %.3f &asymp; +1) and <em>collapses</em> when the insult vanishes &mdash; no
insult, no danger band. The window position tracks each organ's spinodal (the deletion edge is a constant
dimensionless fraction across all four organs). Only the absolute edges (thermal lowering of the deletion edge,
insult amplitude, noise scale D) are [O]; the slopes are the clean invariants.</p>""" % (
            NUM["ec"]["critical_amplitude"]["bone_marrow_hematopoiesis"]["a_crit_over_spinodal"],
            NUM["ec"]["critical_amplitude"]["spleen"]["a_crit_over_spinodal"],
            NUM["ec"]["critical_amplitude"]["thymus"]["a_crit_over_spinodal"],
            NUM["ec"]["critical_amplitude"]["lymphoid_adaptive"]["a_crit_over_spinodal"],
            NUM["ec"]["subspinodal_p_latch_long_duration"],
            NUM["ec"]["dose_time_d_crit_steps"]["a=1.10*sp"], NUM["ec"]["dose_time_d_crit_steps"]["a=1.25*sp"],
            NUM["ec"]["dose_time_d_crit_steps"]["a=1.50*sp"], NUM["ec"]["dose_time_d_crit_steps"]["a=2.00*sp"],
            eaut["total_drive_invariant"][0]["total_drive_over_spinodal"],
            eaut["total_drive_invariant"][1]["total_drive_over_spinodal"],
            eaut["total_drive_invariant"][2]["total_drive_over_spinodal"],
            eaut["total_drive_invariant"][3]["total_drive_over_spinodal"],
            eaut["total_drive_invariant"][4]["total_drive_over_spinodal"],
            eaut["susceptibility_vs_deletion_depth"][0]["critical_insult"],
            eaut["susceptibility_vs_deletion_depth"][2]["critical_insult"],
            eaut["susceptibility_vs_deletion_depth"][4]["critical_insult"],
            eaut["persistence"]["p_break_supra"], eaut["persistence"]["p_break_sub"],
            eaut["persistence"]["p_far_below"],
            eaut["dose_time_tradeoff"][0]["d_crit"], eaut["dose_time_tradeoff"][2]["d_crit"],
            eaut["dose_time_tradeoff"][3]["d_crit"],
            ehor["net_curve"]["low_flank"], ehor["net_curve"]["peak_dose"], ehor["net_curve"]["high_flank"],
            ehor["insult_sweep"][0]["d_lo"], ehor["insult_sweep"][1]["d_lo"], ehor["insult_sweep"][2]["d_lo"],
            ehor["lower_edge_slope"],
            ehor["commit_threshold_tie_in"]["lo_plus_insult"][0],
            ehor["commit_threshold_tie_in"]["lo_plus_insult"][1],
            ehor["commit_threshold_tie_in"]["lo_plus_insult"][2],
            ehor["insult_sweep"][0]["d_hi"],
            ehor["insult_sweep"][0]["width"], ehor["insult_sweep"][2]["width"], ehor["width_slope"]),
    ))

    # 3 — T3 lineage order
    ncbi_rows_html = "\n".join(
        "      <tr><td>%s</td><td>%s</td><td><code>%s</code></td><td>%s</td><td>%.4f</td><td>%s</td></tr>"
        % (esc(NUM["ncbi_ref"]["genes"][sym]["official_symbol"]),
           esc(NUM["ncbi_ver"]["genes"][sym]["organ"].replace("_", " ")),
           esc(NUM["ncbi_ver"]["genes"][sym]["accession"]),
           esc(NUM["ncbi_ref"]["genes"][sym]["map_location"]),
           NUM["ncbi_ver"]["genes"][sym]["live_gamma"],
           "✓ byte-exact" if NUM["ncbi_ver"]["genes"][sym]["verified"] else "FAIL")
        for sym in ("RUNX1", "TLX1", "FOXN1", "PAX5"))
    prov_body = """<h2>Primary-source provenance (NCBI)</h2>
<p>The four γ values are not just cached numbers. Each proximal-promoter window (TSS−2000..+500, 2501 bp)
was re-fetched live from the NCBI reference assembly %s by its exact accession, coordinate window, and
strand, then compared byte-for-byte against the shipped cache — all four match to the sha256, and γ
recomputes identically. NCBI-Gene RefSeq independently corroborates that each gene is the master regulator
for its organ (TLX1 “required for normal development of the spleen”; RUNX1 “involved in normal
haematopoiesis”) and that every accession’s chromosome matches its map location.</p>
<table class="prov">
  <thead><tr><th>master gene</th><th>organ</th><th>NCBI accession</th><th>map</th><th>γ</th><th>vs live NCBI</th></tr></thead>
  <tbody>
%s
  </tbody>
</table>
<p class="fineprint">Verified %s against %s. The check is offline-reproducible (the frozen proof ships in
<code>inherited/ncbi_verification.json</code>; the gate is <code>inherited/ncbi_verify.py</code>) and
re-auditable online via <code>ONLINE_reverify()</code>. γ remains owned by the DNA volume (SSOT) and is
verified here, never re-fitted.</p>
""" % (esc(NUM["ncbi_ver"]["_assembly"]), ncbi_rows_html,
       esc(NUM["ncbi_ver"]["_verified_on"]), esc(NUM["ncbi_ver"]["_assembly"]))
    secs.append(dict(
        slug="03-developmental-lineage-order-gamma-readout", N=3,
        title="Developmental Lineage Order from γ",
        descr="The developmental order of haematopoietic and lymphoid organs is an ascending-γ readout: "
              "lower γ means a lower spinodal and earlier emergence. Endpoints match cited embryology. "
              "All four γ are byte-exact verified against NCBI GRCh38.p14.",
        answer="Developmental order is a γ readout. Ranking the four organs by ascending γ gives "
               "bone-marrow-haematopoiesis → spleen → thymus → lymphoid-adaptive; lower γ is a lower spinodal "
               "and therefore earlier emergence. The endpoints match cited embryology (haematopoiesis earliest, "
               "adaptive lymphoid latest), and all four γ are byte-exact verified against NCBI. Grade [V].",
        abstract="Ascending γ order is %s, and the order is reproduced by an emergent shared-drive race (commit-h "
                 "spacing = spinodal spacing). The earliest endpoint is robust; the spleen↔thymus middle pair is a "
                 "weak emergent bias that washes out under noise — graded [O] for a measured reason. All four "
                 "promoter windows are byte-exact verified against NCBI GRCh38.p14." % " → ".join(ord_),
        grade_token="[V]",
        cards=[gamma_card],
        body="""<h2>Order is a threshold, not a clock</h2>
<p>The volume does not posit a developmental timetable. It reads order off the measured γ: the organ with the
lowest spinodal can cross into existence under the weakest drive, so it emerges first.</p>
<p>The ascending-γ sequence places bone-marrow haematopoiesis first and adaptive lymphoid tissue last. Both
endpoints agree with cited embryology — yolk-sac/AGM haematopoiesis is the earliest blood programme and
PAX5-dependent adaptive memory is the latest to mature.</p>
<h2>The order emerges from a shared-drive race (not a γ sort)</h2>
<p>Ranking γ is just bookkeeping. To test whether the order is real, the four R19 switches are driven by one
shared, slowly-rising morphogenetic field with independent cellular noise, and the drive value at which each
organ commits (its state crosses the ridge) is <em>measured</em> from the dynamics. The emergence order that
comes out is the ascending-γ order, and the measured spleen→thymus commitment spacing is %.4f — equal to the
forced spinodal spacing %.4f. The mechanism “lower spinodal commits earlier under a shared drive” is therefore
confirmed dynamically, not assumed.</p>
<h2>Honest middle, now quantified</h2>
<p>The race also shows <em>which</em> orderings are real. Bone-marrow-haematopoiesis commits first in essentially
every run (P=%.2f) because its spinodal gap to the next organ is large (%.3f). The spleen↔thymus pair has the
<em>smallest</em> gap (%.3f), comparable to the commitment jitter, so it is only a weak emergent bias
(P(spleen&lt;thymus)=%.2f at low noise) that washes toward a coin-flip as noise rises
(%.2f → %.2f → %.2f across the noise scan). The middle pair is thus graded [O] for a measured, falsifiable
reason — its separation-to-jitter ratio is ≈%.2f — not for lack of an embryology citation. The robust claims
are the earliest endpoint and the direction; the fine middle ordering is honestly left open.</p>
""" % (NUM["el"]["commit_h_spacing_spleen_thymus"], NUM["el"]["forced_spinodal_spacing_spleen_thymus"],
       NUM["el"]["endpoints"]["bone_marrow_first_P"], NUM["el"]["adjacent_pairs"]["marrow_before_spleen"]["gap"],
       NUM["el"]["adjacent_pairs"]["spleen_before_thymus"]["gap"],
       NUM["el"]["adjacent_pairs"]["spleen_before_thymus"]["P"],
       NUM["el"]["noise_scan"][0]["P_spleen_before_thymus"], NUM["el"]["noise_scan"][1]["P_spleen_before_thymus"],
       NUM["el"]["noise_scan"][2]["P_spleen_before_thymus"], NUM["el"]["middle_pair_separation_to_jitter"]) + prov_body,
    ))

    # 4 — T4 memory
    secs.append(dict(
        slug="04-immune-memory-barrier-persistence", N=4,
        title="Immune Memory as Barrier Persistence",
        descr="Immunological memory is barrier-protected persistence: an activated clone stays ON after antigen "
              "clears, the erase drive equals the spinodal, and memory stability ranks by the γ²/4 barrier.",
        answer="Immune memory is barrier-protected persistence of the ON state. This volume does not just assert "
               "stability — it removes the drive and simulates the stochastic ON→OFF escape, and the measured mean "
               "lifetime ranks in ascending γ order while the Kramers law (log-rate linear in barrier) emerges. "
               "Higher-γ organs remember longest. Grade [V].",
        abstract="With the drive removed the ON state persists; the measured mean lifetime (MFPT) ranks in the same "
                 "ascending order as γ (%s), and log(escape-rate) is linear in the barrier (R²=%.3f) — the Kramers "
                 "law emerging from a direct stochastic escape simulation, with absolute lifetime [O]."
                 % (" → ".join(ord_), NUM["em"]["arrhenius_R2"]),
        grade_token="[V]",
        cards=[barrier_card, spinodal_card],
        body="""<h2>Persistence without a drive</h2>
<p>Memory is the ON basin surviving the removal of antigen. The barrier γ²/4 is what keeps the clone in the ON
basin once the affinity drive falls to zero, so no ongoing antigen is required to remember.</p>
<p>Forgetting is not passive decay here: erasing the memory takes a reverse drive of at least the spinodal,
the mirror of activation. Below that, the memory is stable.</p>
<h2>Stability ranking</h2>
<p>Because the barrier grows with γ, the organs rank in durability exactly as they rank in γ. The adaptive
lymphoid compartment has the largest barrier and so is the most stable long-term store — consistent with
durable adaptive immunity outliving innate responses.</p>
<h2>The durability ordering emerges from a stochastic escape simulation</h2>
<p>Rather than infer stability from the barrier height alone, the volume <em>simulates</em> forgetting directly:
each organ's clone is initialised in the ON basin, the antigen drive is removed (h=0), and an ensemble of cells
evolves under overdamped Langevin noise until they escape back to OFF. The mean ON-state lifetime is
<em>measured</em> as the inverse escape rate, and it ranks bone-marrow %.1f &lt; spleen %.1f &lt; thymus %.1f
&lt; lymphoid %.1f — exactly the ascending-γ order, so the durability ranking is confirmed dynamically rather
than read off the barrier.</p>
<p>The Kramers law itself emerges: the logarithm of the measured escape rate is linear in the independently
computed γ²/4 barrier (R²=%.3f) with an Arrhenius slope of %.1f, recovering the expected −1/D=%.1f. The
stability ordering and the exponential law are therefore [V] (simulation-measured); only the absolute lifetime,
which depends on the uncalibrated cellular-noise scale D, is left [O].</p>""" % (
            NUM["em"]["mean_lifetime_MFPT"]["bone_marrow_hematopoiesis"],
            NUM["em"]["mean_lifetime_MFPT"]["spleen"], NUM["em"]["mean_lifetime_MFPT"]["thymus"],
            NUM["em"]["mean_lifetime_MFPT"]["lymphoid_adaptive"],
            NUM["em"]["arrhenius_R2"], NUM["em"]["arrhenius_slope"], NUM["em"]["expected_slope_minus_1_over_D"]),
    ))

    # 5 — T5 surveillance seam
    secs.append(dict(
        slug="05-immunosurveillance-escape-cross-cutting-seam", N=5,
        title="Immunosurveillance: the Escape Seam",
        descr="Immunosurveillance is a cross-cutting seam: net malignant burden = crossing-rate × immune-escape "
              "factor, and the escape factor is a common multiplier acting on every site and every organ system.",
        answer="Immunosurveillance enters as a multiplicative seam: net malignant burden equals an influx rate "
               "times an immune-escape factor. This volume does not assume that form — it simulates a coupled "
               "stochastic influx–clearance process, and the AML and lymphoma burden curves collapse onto one "
               "shared 1/(1−escape) multiplier. One cross-cutting lever for the whole body. Grade [V].",
        abstract="Net burden is measured from a coupled stochastic influx–clearance simulation: it is monotone in "
                 "the escape factor, and rescaled by site influx the AML and lymphoma curves collapse onto a single "
                 "1/(1−escape) multiplier (max cross-site gap %.4f). This is the cross-cutting lever the therapy "
                 "volume restores in Lever D." % NUM["es"]["max_cross_site_gap"],
        grade_token="[V]",
        cards=[barrier_card],
        body="""<h2>One factor, every site</h2>
<p>The seam is deliberately minimal: surveillance does not change how fast cells cross into the malignant
basin, only how many crossed cells survive. Net burden is the product of the two.</p>
<p>The escape factor is the same multiplier for acute myeloid leukaemia and for lymphoma, and the seam exports
it to every other organ volume's cancer kernel. That shared multiplier is why a single immune intervention
can lower burden everywhere at once.</p>
<h2>The lever it sets up</h2>
<p>Read as a treatment target, this seam is Lever D of the therapy volume: lowering the escape factor (restoring
clearance) reduces burden even when the crossing-rate is untouched, and it removes the committed reservoir that
drive-removal alone leaves behind.</p>
<h2>The multiplicative seam emerges from a coupled stochastic model</h2>
<p>Rather than assert that burden factorises into influx × escape, the volume <em>simulates</em> the seam:
malignant cells arrive at each site as a measured R19-crossing influx (a Langevin process) and are cleared at a
rate that surveillance escape reduces, and the time-averaged steady-state burden is <em>measured</em> for each
site across the escape range. The burden is monotone in escape at both sites, and — the key test — once each
site's curve is rescaled by its own measured influx, the acute-myeloid-leukaemia and lymphoma curves collapse
onto the <em>same</em> universal multiplier (maximum cross-site gap only %.4f).</p>
<p>That shared multiplier is the ideal 1/(1−escape) form to within %.4f, so the cross-cutting seam — one escape
factor acting identically on every site — is an emergent property of the coupled dynamics, not an imposed
algebraic shortcut. Only the absolute burden scale (the population constant K and clearance scale μ0) is
uncalibrated and left [O], so no fabricated incidence numbers are claimed.</p>""" % (
            NUM["es"]["max_cross_site_gap"], NUM["es"]["max_gap_vs_one_over_one_minus_escape"]),
    ))

    # 6 — oncology
    secs.append(dict(
        slug="06-carcinogen-dose-response-kramers-kernel", N=6,
        title="Carcinogen Dose–Response (Kramers)",
        descr="Carcinogens lower the R19 barrier; the malignant crossing rate follows a convex, super-linear "
              "Kramers dose–response that diverges as the barrier is erased. Benzene→AML is the cleanest anchor.",
        answer="A carcinogen lowers the R19 barrier, raising the malignant crossing rate. This volume does not "
               "assume the Kramers law — it simulates the stochastic R19 field and counts crossings, and both a "
               "convex super-linear dose–response and the Kramers exponential emerge from the dynamics. "
               "Benzene→AML (IARC Group 1) anchors it. Grade [V] shape+law / [L] anchor / [O] steepness.",
        abstract="The dose–response is measured by direct stochastic barrier-crossing simulation: it is "
                 "convex/super-linear (convex=%s) and the Kramers law emerges (log-rate linear in barrier, "
                 "R²=%.3f). Sites: AML←benzene/radiation/alkylators; lymphoma←radiation/immunosuppression/EBV. "
                 "Absolute steepness (noise scale D) is uncalibrated and graded [O]."
                 % (aml["convex_superlinear"], NUM["ek"]["arrhenius_R2"]),
        grade_token="[V]",
        cards=[barrier_card, spinodal_card],
        body="""<h2>Why the curve bends up</h2>
<p>The kernel is one line: a carcinogen erodes the barrier, and the Kramers rate depends exponentially on the
remaining barrier. A small extra dose near the top of the range removes proportionally more barrier, so the
crossing rate accelerates — the curve is convex, not linear.</p>
<p>At the spinodal the barrier reaches zero and the rate diverges: with no barrier left the transformation is
deterministic rather than thermally activated. This is the mathematical face of a saturating carcinogen.</p>
<h2>The shape is measured, not assumed</h2>
<p>Rather than write down the Kramers formula and trust it, the volume <em>simulates</em> the stochastic R19
field directly: a population of healthy cells under overdamped Langevin dynamics with a carcinogen drive that
erodes the barrier, and the malignant crossing rate is <em>counted</em> from how many cells cross the ridge.
Two things emerge from the dynamics. First, the measured dose–response is convex and super-linear
(convex=%s; the measured relative rate runs roughly %s across the dose fractions). Second, the logarithm of the
measured rate is linear in the independently-computed effective barrier (R²=%.3f) with an Arrhenius slope of
%.1f, recovering the expected −1/D=%.1f — so the Kramers exponential law is an <em>emergent</em> property of
the simulated substrate, not an assumed kernel.</p>
<h2>Anchors, honestly graded</h2>
<p>Benzene→acute myeloid leukaemia is the cleanest occupational anchor (IARC Group 1, ppm-years exposure
metric); lymphoma is anchored to ionizing radiation, chronic immunosuppression, and EBV drive. The shape and
the Kramers law are [V] (simulation-measured) and the anchors are [L], but the absolute incidence and the
steepness depend on the cellular-noise scale D, which the volume does not calibrate — stated [O], no fabricated
relative-risk numbers.</p>""" % (
            NUM["ek"]["convex_superlinear"],
            "1 → %.0f → %.0f → %.0f" % (NUM["ek"]["RR"][1], NUM["ek"]["RR"][len(NUM["ek"]["RR"])//2], NUM["ek"]["RR"][-1]),
            NUM["ek"]["arrhenius_R2"], NUM["ek"]["arrhenius_slope"], NUM["ek"]["expected_slope_minus_1_over_D"]),
    ))

    # 7 — fundamental therapy
    secs.append(dict(
        slug="07-fundamental-treatment-levers-attractor-landscape", N=7,
        title="Fundamental Treatment Levers",
        descr="Four fundamental treatment levers follow from the R19 attractor landscape — basin re-flip, "
              "barrier restoration, drive removal, surveillance restoration — and explain why cytotoxic-only "
              "therapy relapses.",
        answer="Treating cancer as an attractor fact forces four levers: re-flip the basin (differentiation), "
               "restore the barrier, remove the drive, restore surveillance. All four are now measured as "
               "stochastic trajectories, and cytotoxic relapse is an explicit regrowth curve — the malignant "
               "fraction regrows when the basin is intact, decays when it is emptied. APL and CAR-T validate two "
               "levers. Grade [V]/[L].",
        abstract="All four levers are measured as stochastic trajectories. Differentiation (Lever A) empties the "
                 "malignant basin as the drive crosses the spinodal (residual ON occupancy %.2f→%.2f, "
                 "non-cytotoxic); drive removal (Lever C) leaves a committed population occupied (%.2f, relapse) "
                 "but a healthy one prevented (%.2f). Barrier restoration (Lever B) collapses the counted crossing "
                 "rate ~%.0f× as the barrier is restored; surveillance restoration (Lever D) clears the reservoir "
                 "as a time course; and cytotoxic relapse is an explicit regrowth curve recovering to %.0f%% of "
                 "capacity while differentiation decays to ≈0."
                 % (ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverA_subspinodal_ON_occupancy"],
                    ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverA_supraspinodal_ON_occupancy"],
                    ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverC_committed_ON_after_drive_removal"],
                    ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverC_healthy_ON_after_drive_removal"],
                    1.0 / ebar["aml_restoration_trajectory"]["full_restoration_rate_drop"],
                    ereg["cytotoxic_final_fraction"] * 100.0),
        grade_token="[V]",
        cards=[spinodal_card, barrier_card],
        body="""<h2>Malignancy is a basin, not a headcount</h2>
<p>The deep claim of this volume is that a tumour is a region of the attractor landscape, not merely a number
of cells. A durable cure must change the landscape — empty or destabilise the malignant basin — rather than
only reducing the count of cells sitting in it.</p>
<h2>Four levers, all from one kernel</h2>
<p><b>Lever A — basin re-flip (differentiation).</b> A malignant cell re-flips into a healthy basin once a
differentiating drive reaches the spinodal, with no cytotoxicity. The clinical anchor is acute promyelocytic
leukaemia, the first acute leukaemia cured by a non-cytotoxic, differentiating regimen (all-trans retinoic
acid plus arsenic trioxide).</p>
<p><b>Lever B — barrier restoration.</b> Restoring tumour-suppressor or epigenetic control raises the barrier,
and the Kramers rate collapses exponentially — a large multiplicative drop in crossing rate for a modest
barrier gain.</p>
<p><b>Lever C — drive removal (etiologic).</b> Removing the carcinogen drive prevents un-committed crossings,
but by hysteresis it does not reverse an already-committed cell. It is preventive, not curative once committed
— matching smoking-cessation epidemiology, where future risk falls while an established tumour persists.</p>
<p><b>Lever D — surveillance restoration.</b> This volume's own seam. Lowering the immune-escape factor clears
the committed reservoir at a fixed crossing-rate and, because the factor is a common multiplier, acts across
every site. The anchor is CAR-T and checkpoint blockade, curative in refractory leukaemia and lymphoma.</p>
<h2>Why cytotoxic-only relapses</h2>
<p>Cytotoxic killing removes cells but leaves the barrier and the basin unchanged, so any surviving malignant
cell stays malignant and the basin refills — hysteretic relapse. The kernel therefore predicts that the
cleanest durable cures are attractor- and field-level and non-cytotoxic; the two cleanest real haematologic
cures (differentiation in APL, surveillance in CAR-T) are exactly Lever A and Lever D.</p>
<h2>Levers A and C emerge as measured trajectories</h2>
<p>Levers A and C are no longer read off a single deterministic settle; they are <em>measured</em> from direct
stochastic simulations of the substrate. For Lever A a population starts in the malignant basin and a
differentiating drive is applied: the residual malignant-basin occupancy collapses from %.2f to %.2f as the
drive crosses the spinodal (measured 0.5-crossing at %.2f× the spinodal, approached from below because thermal
activation helps the cell over the shrinking barrier), with no cytotoxicity. The re-flip threshold is therefore
the spinodal, measured organ-by-organ.</p>
<p>For Lever C the carcinogen drive is removed under noise. A committed population stays in the malignant basin
(occupancy %.2f — hysteresis, the substrate origin of relapse) while a healthy population stays out of it
(occupancy %.2f — prevention), so removing the cause is preventive but not curative. Cytotoxic killing is the
same measurement: it leaves the landscape intact, so its survivors keep occupancy %.2f and the basin refills.
Only differentiation drives occupancy to %.2f and empties the basin — the measured reversal-vs-relapse contrast,
with the absolute agent dose and schedule left [O].</p>
<h2>Levers B and D emerge as measured trajectories</h2>
<p><b>Lever B — barrier restoration.</b> The crossing-rate collapse is no longer read off the closed-form
exponential; it is <em>measured</em>. As a fraction of the carcinogen-eroded barrier is stepped back up, the
counted malignant crossing rate falls monotonically — a %.1f× multiplicative drop at full restoration — and the
logarithm of the measured rate is linear in the restored barrier (R²=%.3f, Arrhenius slope %.1f recovering
−1/D=%.1f), so the Kramers collapse emerges in the therapeutic direction rather than being assumed.</p>
<p><b>Lever D — surveillance restoration.</b> The reservoir clearance is <em>measured</em> as a time course.
Starting from a high-escape reservoir, restoring surveillance makes the counted committed reservoir decay toward
a floor that falls with deeper surveillance; floor × surveillance is constant, so the floor scales as
1/(1−escape) — the steady T10 seam recovered as a trajectory endpoint — and, rescaled by influx, the AML and
lymphoma floors collapse onto the same 1/surveillance curve (cross-site gap %.3f). Deeper surveillance also
clears the reservoir faster.</p>
<h2>Cytotoxic relapse is a measured regrowth curve</h2>
<p>The relapse failure mode is made explicit as a population trajectory gated by the measured R19 basin
fraction. After cytotoxic killing the survivors remain in the malignant basin (measured ON fraction %.2f) and
the malignant fraction regrows toward the carrying capacity, recovering to %.0f%% — relapse. After a
differentiating re-flip the basin is emptied (measured ON fraction %.2f) and the malignant fraction decays to
%.0f%% — a cure, with no cytotoxicity. Sweeping the kill fraction shows the decisive point: a deeper kill only
lengthens the regrowth delay (time-to-half %.1f → %.1f as the kill rises %.0f%%→%.0f%%) while every depth still
recovers fully. Relapse is determined by the basin, not by how many cells are killed — maximal cytotoxic kill
does not cure, the attractor does.</p>
<h2>Combination therapy converts relapse into cure</h2>
<p>The relapse curve and the cure curve can be put on the same axes and combined. A cytotoxic cull alone drives
the malignant fraction down at first but, because the basin is untouched, it regrows to the carrying capacity
(final %.0f%% of K — relapse). A single basin-acting lever already cures (differentiation alone and restored
surveillance both decay to ≈0). The decisive measurement is the combination: adding the cytotoxic cull to
either basin lever keeps the cure (final ≈0) <em>and</em> lowers the cumulative burden — the area under N(t)/K
falls from %.2f (differentiation alone) to %.2f with a cull added, and from %.2f (surveillance alone) to %.2f —
so the cull accelerates the approach without changing the destination.</p>
<p>The control is explicit and honest: the same cull <em>alone</em> never cures at any depth — only a
basin/niche lever converts relapse to cure. And the surveillance channel shows an emergent threshold at the
growth rate: a sub-threshold surveillance (μ=%.1f) relapses to an interior fixed point at the predicted
N*=K(1−μ/r) (measured %.0f%% of K), while a supra-threshold surveillance (μ=%.1f, %.1f) clears to a cure
(%.1f%%, %.1f%% of K). The conversion, the cull's burden reduction, the cull-alone insufficiency and the
growth-rate threshold are measured; the absolute rates and the clinical schedule stay [O].</p>
<h2>What the kernel does not claim</h2>
<p>VP does not invent these therapies. It re-derives why they are the fundamental class and names the
cytotoxic relapse failure mode mechanically. The kernel predicts a class of intervention and the relapse
mode; it does not predict a molecule, a dose, a schedule, or an individual patient's response, which require
pharmacology and biomarkers outside the deterministic substrate — stated [O].</p>""" % (
            ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverA_subspinodal_ON_occupancy"],
            ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverA_supraspinodal_ON_occupancy"],
            ethr["leverA_measured_crossing_over_spinodal"],
            ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverC_committed_ON_after_drive_removal"],
            ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverC_healthy_ON_after_drive_removal"],
            ethr["per_organ"]["bone_marrow_hematopoiesis"]["cytotoxic_survivors_ON_occupancy"],
            ethr["per_organ"]["bone_marrow_hematopoiesis"]["leverA_supraspinodal_ON_occupancy"],
            1.0 / ebar["aml_restoration_trajectory"]["full_restoration_rate_drop"],
            ebar["aml_restoration_trajectory"]["arrhenius_R2"],
            ebar["aml_restoration_trajectory"]["arrhenius_slope"],
            ebar["aml_restoration_trajectory"]["expected_slope_minus_1_over_D"],
            eclr["max_cross_site_gap"],
            ereg["measured_basin_fraction"]["cytotoxic_survivors_ON"], ereg["cytotoxic_final_fraction"] * 100.0,
            ereg["measured_basin_fraction"]["differentiation_residual_ON"], ereg["differentiation_final_fraction"] * 100.0,
            ereg["kill_depth_sweep"][0]["time_to_half_K"], ereg["kill_depth_sweep"][-1]["time_to_half_K"],
            ereg["kill_depth_sweep"][0]["kill_fraction"] * 100.0, ereg["kill_depth_sweep"][-1]["kill_fraction"] * 100.0,
            ecmb["arms"]["cytotoxic_alone"]["final"] * 100.0,
            ecmb["arms"]["differentiation_alone"]["auc"], ecmb["arms"]["cytotoxic_plus_diff"]["auc"],
            ecmb["arms"]["surveillance_alone"]["auc"], ecmb["arms"]["cytotoxic_plus_surv"]["auc"],
            ecmb["surveillance_threshold_sweep"][0]["mu_surv"],
            ecmb["surveillance_threshold_sweep"][0]["final_fraction"] * 100.0,
            ecmb["surveillance_threshold_sweep"][1]["mu_surv"], ecmb["surveillance_threshold_sweep"][2]["mu_surv"],
            ecmb["surveillance_threshold_sweep"][1]["final_fraction"] * 100.0,
            ecmb["surveillance_threshold_sweep"][2]["final_fraction"] * 100.0),
    ))

    # ---------------------------------------------------------------------------------------------
    # chapter 08 (v0.15.0 split): disease/treatment AXIS OVERVIEW + one self-contained page per
    # disease class (autoimmunity / transplant / allergy / immunodeficiency / cytopenia / systemic).
    # Bodies are transferred verbatim from the former combined chapter 8; per-page numbers are
    # spliced from the SAME already-pulled result dicts (no science re-run). answer-first 40-60 words.
    # ---------------------------------------------------------------------------------------------

    # 8 — disease/treatment AXIS OVERVIEW (framing + organizing claim + boundaries; links the six pages)
    secs.append(dict(
        slug="08-disease-treatment-axis-basin-acting-cures", N=8,
        title="The Disease/Treatment Axis: Basin-Acting Cures vs Suppression-Only Relapse",
        descr="Across autoimmunity, transplantation, allergy, immunodeficiency, autoimmune cytopenia and "
              "systemic inflammation the same R19 substrate gives one verdict: a basin-acting intervention "
              "(re-tolerization, induction, reconstitution, latch-break) is the durable class, while "
              "drive-suppression-only is preventive-not-curative and relapses on withdrawal.",
        answer="A pathological immune state is a latched basin of the same bistable switch, so a durable treatment "
               "must move the system ACROSS the saddle-node (basin-acting), not merely hold the drive down "
               "(suppression-only). Re-tolerization, tolerance induction, reconstitution and latch-break are the "
               "durable class; suppression refills on withdrawal. DIRECTION/CLASS only, not medical advice. Grade [V].",
        abstract="Across six disease classes the substrate gives one verdict: a basin-acting intervention is the "
                 "durable class and drive-suppression-only relapses on withdrawal. The autoimmune break latches "
                 "past the spinodal (residual autoreactive occupancy %.2f after the insult clears); a transient "
                 "re-tolerization pulse empties it durably (final autoreactive fraction %.2f) while a sub-critical "
                 "suppressor only contains it and refills on withdrawal (%.2f). The same contrast recurs in "
                 "transplantation (durable induction trajectory %.2f vs indefinite-immunosuppression rejection "
                 "%.2f), in lineage-targeted autoimmune cytopenia (lineage output restored to %.0f%% durably vs "
                 "%.0f%% after suppression is withdrawn), and in systemic inflammation, where the cytokine latch "
                 "self-sustains after the trigger is removed (supra-threshold %.0f%% vs sub-threshold %.0f%% "
                 "occupancy) and the break is time-critical."
                 % (eaut["persistence"]["p_break_supra"],
                    eret["durable_vs_relapsing"]["retolerization_final_fraction"],
                    eret["durable_vs_relapsing"]["suppression_final_fraction"],
                    ealo["durable_vs_relapsing"]["induce_traj_end"],
                    ealo["durable_vs_relapsing"]["immuno_traj_end"],
                    ecyt["durable_vs_relapsing"]["retolerize_output_end"] * 100.0,
                    ecyt["durable_vs_relapsing"]["suppress_output_after_withdrawal"] * 100.0,
                    esep["self_sustain"]["frac_supra_after_withdraw"] * 100.0,
                    esep["self_sustain"]["frac_sub_after_withdraw"] * 100.0),
        grade_token="[V]",
        cards=[spinodal_card, barrier_card],
        body="""<h2>One landscape, many diseases</h2>
<p>The earlier chapters established that an immune commitment &mdash; a selected clone, a memory state, an inflamed
tissue &mdash; is a basin of a bistable R19 switch separated from its resting state by a saddle-node at the spinodal.
This chapter collects the disease counterpart: many named immune diseases are the SAME switch latched in the
wrong basin, and their treatments fall into exactly two mechanical classes. A <em>basin-acting</em> intervention
moves the system across the saddle-node into the other basin, so the change persists after the intervention is
withdrawn. A <em>suppression-only</em> intervention merely lowers the drive without crossing the saddle-node, so
it holds the state down while applied but the basin refills the moment the pressure is released. The whole
chapter is one measured statement: across every disease class, the basin-acting class is the durable one.</p>

<h2>The six disease classes, one page each</h2>
<p>Each disease class is treated in full on its own self-contained, answer-first page; follow the links for the
measured numbers, grades and boundaries:</p>
<ul>
<li><a href="/immune_hematologic_vp_site/09-autoimmunity-break-and-retolerization/">Autoimmunity</a> &mdash; the tolerance break past the spinodal and its durable cure by therapeutic re-tolerization.</li>
<li><a href="/immune_hematologic_vp_site/10-transplant-allotolerance-induction/">Transplantation</a> &mdash; allo-tolerance induction versus indefinite immunosuppression, and the induction window.</li>
<li><a href="/immune_hematologic_vp_site/11-allergy-sensitization-desensitization/">Allergy</a> &mdash; dose&times;repetition sensitization, the latch, and controlled desensitization.</li>
<li><a href="/immune_hematologic_vp_site/12-immunodeficiency-reconstitution/">Immunodeficiency</a> &mdash; one surveillance lever, two diseases, and threshold-gated reconstitution.</li>
<li><a href="/immune_hematologic_vp_site/13-autoimmune-cytopenia-lineage-targeted/">Autoimmune cytopenia</a> &mdash; the attack read out on a blood count, durable restoration versus re-collapse.</li>
<li><a href="/immune_hematologic_vp_site/14-systemic-inflammation-cytokine-latch/">Systemic inflammation</a> &mdash; the self-sustaining cytokine latch and the time-critical break window.</li>
</ul>

<h2>The organizing claim</h2>
<p>Six disease classes, one verdict. In every case the durable intervention is the one that moves the system
ACROSS the saddle-node &mdash; re-tolerization of an autoreactive clone, induction of allo-tolerance, threshold-crossing
immune reconstitution, and the active break of a self-sustaining inflammatory latch. In every case
drive-suppression-only is preventive-not-curative: it contains the state while applied, but the basin refills on
withdrawal. This is why chronic immunosuppression in autoimmunity and transplantation manages rather than cures,
why partial reconstitution fails below threshold, and why removing a trigger does not stop an established cytokine
storm. The substrate names the class of durable intervention and the relapse failure mode mechanically, from one
bistable switch.</p>

<h2>What this is &mdash; and is not</h2>
<p>This is a re-description of well-known immune-disease and treatment dynamics in the R19 formalism, and a
principled statement of treatment DIRECTION and CLASS with its boundaries (the induction window, the
reconstitution threshold, the break window). It is NOT a drug, a dose, a schedule, a clinical protocol, or a
recommendation for any individual; those require pharmacology, biomarkers and trials outside the deterministic
substrate, and every absolute and clinical scale here is left [O] with the obstacle stated. It is NOT a
validation of VP theory, and NOT medical advice. The measured content is the qualitative dynamics &mdash; the
saddle-node thresholds, the durable-versus-relapsing contrast, the windows and the one-lever-two-diseases
structure &mdash; each graded [V] and reproduced deterministically from the same kernel as the rest of this volume.</p>""",
    ))

    # 9 — autoimmunity (T23 tolerance break + T27 therapeutic re-tolerization)
    secs.append(dict(
        slug="09-autoimmunity-break-and-retolerization", N=9,
        title="Autoimmunity: The Tolerance Break and Its Durable Re-Tolerization",
        descr="An autoimmune state is the R19 switch latched past the spinodal; a transient re-tolerization pulse "
              "moves it back across the negative saddle-node and cures durably, while drive-suppression-only "
              "contains it and relapses on withdrawal.",
        answer="An autoimmune state is the same R19 switch latched ON: an insult past the spinodal leaves residual "
               "autoreactive occupancy that persists after it clears. A transient re-tolerization pulse empties that "
               "basin durably, while sub-critical suppression only contains it and refills on withdrawal. "
               "DIRECTION/CLASS only, not medical advice. Grade [V].",
        abstract="An escaped self-clone is bistable: an inflammatory insult past the spinodal latches it ON and it "
                 "stays ON after the insult clears, the dark mirror of immune memory. A transient deep-suppression / "
                 "barrier-restoration pulse pushes the latched clone back across the negative saddle-node into the "
                 "tolerant basin and the cure is durable, whereas a continuously held sub-critical suppressor only "
                 "dampens the effector and the basin refills on withdrawal. Measured dynamics graded [V]; absolute "
                 "clinical scale [O], not medical advice.",
        grade_token="[V]",
        cards=[spinodal_card, barrier_card],
        body="""<h2>Autoimmunity: the break and its cure</h2>
<p>An escaped self-clone carries a sub-spinodal residual self-drive, so it is bistable. An inflammatory insult
that pushes the total drive past the spinodal latches it ON, and it <em>stays</em> ON after the insult clears
(measured residual autoreactive occupancy %.2f) &mdash; a self-sustaining autoimmune state, the dark mirror of immune
memory. The therapeutic dual is measured directly: a transient deep-suppression / barrier-restoration pulse can
push the latched clone back across the NEGATIVE saddle-node into the tolerant basin. The re-tolerization
threshold is that other saddle-node &mdash; the critical suppression makes the total pulse drive reach &minus;1&times;spinodal,
i.e. suppress_crit = 1 + residual (measured %.3f&times; the spinodal at the reference residual). Crucially the cure is
DURABLE: a supra-threshold pulse leaves the clone tolerant after withdrawal (final autoreactive fraction %.2f,
unchanged when the settle is tripled), whereas a sub-critical suppressor held continuously only DAMPENS the
effector while applied and the autoreactive basin REFILLS on withdrawal (final fraction %.2f). Basin-acting
re-tolerization cures; suppression-only relapses.</p>
<p class="fineprint">Part of the <a href="/immune_hematologic_vp_site/08-disease-treatment-axis-basin-acting-cures/">disease/treatment axis</a>: a pathological immune state is a latched basin, and the durable class of intervention moves the system across the saddle-node rather than only holding the drive down, which relapses on withdrawal.</p>""" % (
            eaut["persistence"]["p_break_supra"],
            eret["durability"]["critical_suppress"],
            eret["durable_vs_relapsing"]["retolerization_final_fraction"],
            eret["durable_vs_relapsing"]["suppression_final_fraction"]),
    ))

    # 10 — transplantation (T32 allo-tolerance induction vs indefinite immunosuppression)
    secs.append(dict(
        slug="10-transplant-allotolerance-induction", N=10,
        title="Transplantation: Allo-Tolerance Induction vs Indefinite Immunosuppression",
        descr="Transplant tolerance is a negative saddle-node crossing: a deep transient induction yields durable "
              "operational tolerance off-therapy, while indefinite immunosuppression only contains rejection and "
              "relapses on withdrawal, with an induction window that closes as the alloresponse consolidates.",
        answer="A graft is a standing allo-antigen load on the same switch. A deep transient induction crosses the "
               "negative saddle-node and yields durable operational tolerance off-therapy, while continuous "
               "sub-critical immunosuppression only contains rejection and the graft is rejected on withdrawal. The "
               "induction threshold rises the longer the alloresponse consolidates. DIRECTION/CLASS only, not "
               "medical advice. Grade [V].",
        abstract="A graft presents a standing allo-antigen load — the same substrate problem with a larger residual "
                 "drive, whose induction threshold is the negative saddle-node shifted by the load. A deep transient "
                 "induction yields durable operational tolerance off-therapy, while continuous sub-critical "
                 "immunosuppression only contains rejection and rejects on withdrawal; the induction threshold rises "
                 "the longer the alloresponse runs unopposed, defining an induction window. Host-versus-graft and "
                 "graft-versus-host are the same crossing with the compartments swapped; measured dynamics [V], "
                 "absolute scale [O].",
        grade_token="[V]",
        cards=[spinodal_card, barrier_card],
        body="""<h2>Transplantation: induction vs indefinite immunosuppression</h2>
<p>A graft presents a standing allo-antigen LOAD &mdash; the same substrate problem with a larger residual drive. The
induction threshold is again the negative saddle-node, shifted by the load: the critical suppression depth at
which operational tolerance is induced makes the total drive reach &minus;1&times;spinodal, i.e. suppress_crit = 1 + allo-load
(measured %.3f&times; the spinodal). A deep transient induction yields DURABLE operational tolerance &mdash; the alloreactive
trajectory empties to %.2f of capacity and the graft is accepted off-therapy &mdash; whereas continuous sub-critical
immunosuppression only CONTAINS rejection while applied and REJECTS on withdrawal (trajectory %.2f, the basin
refilled). The transplant-specific fact is timing: the alloresponse CONSOLIDATES the longer it runs unopposed, so
the measured induction threshold RISES with the delay-to-induction (suppress_crit %.3f early &rarr; %.3f late) &mdash; an
induction window in which tolerance is easier before the alloresponse consolidates. The mechanism is
direction-symmetric: host-versus-graft and graft-versus-host are the same saddle-node crossing with the
alloreactive compartment and target swapped.</p>
<p class="fineprint">Part of the <a href="/immune_hematologic_vp_site/08-disease-treatment-axis-basin-acting-cures/">disease/treatment axis</a>: a pathological immune state is a latched basin, and the durable class of intervention moves the system across the saddle-node rather than only holding the drive down, which relapses on withdrawal.</p>""" % (
            ealo["induction_threshold"]["per_organ"]["lymphoid_adaptive"]["suppress_crit_over_spinodal"],
            ealo["durable_vs_relapsing"]["induce_traj_end"],
            ealo["durable_vs_relapsing"]["immuno_traj_end"],
            ealo["induction_window"]["suppress_crit_early"],
            ealo["induction_window"]["suppress_crit_late"]),
    ))

    # 11 — allergy (T29 sensitization / desensitization; wired in v0.15.0 -- NEW body, numbers from esen)
    secs.append(dict(
        slug="11-allergy-sensitization-desensitization", N=11,
        title="Allergy: Dose-by-Repetition Sensitization, the Latch, and Controlled Desensitization",
        descr="Allergy is a failure of immune ignorance on the R19 switch: a sub-threshold antigen dose repeated "
              "accumulates priming and sensitizes, the state latches, and a controlled below-crossover exposure "
              "protocol raises the threshold and desensitizes.",
        answer="Allergy is a failure of immune ignorance: a single sub-spinodal exposure stays tolerant, but a "
               "sub-threshold dose REPEATED accumulates priming and sensitizes after a critical count that falls as "
               "the dose rises, and the sensitized state latches after antigen clears. A controlled below-crossover "
               "protocol raises the challenge threshold and desensitizes. DIRECTION/CLASS only, not medical advice. "
               "Grade [V].",
        abstract="Allergy is the failure mode of immune ignorance on the same effector: a single exposure commits "
                 "only past the spinodal, but a sub-threshold supra-crossover dose repeated accumulates priming and "
                 "sensitizes after a critical exposure count that falls as the dose rises, and the sensitized "
                 "effector latches after the antigen clears. A controlled below-crossover exposure protocol raises "
                 "the challenge threshold so the once-sensitizing dose no longer commits — re-tolerization through "
                 "exposure — while an over-aggressive above-crossover protocol sensitizes instead, so the "
                 "desensitization window is real. Measured dynamics [V]; absolute dose, crossover and exposure count "
                 "[O], not medical advice.",
        grade_token="[V]",
        cards=[spinodal_card, barrier_card],
        body="""<h2>Allergy: sensitization, the latch, and controlled desensitization</h2>
<p>Allergy is the failure mode of immune ignorance on the same R19 effector. A single antigen exposure commits the
effector only when it crosses the spinodal (measured critical dose %.3f&times; the spinodal, the same commit threshold
as the tolerance/immunity window), so a sub-threshold dose alone stays tolerant. The pathology is in REPETITION: a
sub-threshold but supra-crossover dose REPEATED accumulates priming and sensitizes after a measured critical
number of exposures, and that number FALLS as the dose rises (N_crit = %d exposures at the lower dose, down to %d
at the higher).</p>
<p>Once sensitized the effector LATCHES: it stays ON after the antigen has cleared (measured residual occupancy
%.3f), the same R19 memory that protective immunity uses, here turned against a harmless antigen. Removing the
antigen therefore does not by itself reset the sensitized state.</p>
<p>The cure is a controlled re-exposure, and it is a window. A controlled BELOW-crossover exposure protocol
accumulates tolerance faster than priming and RAISES the challenge threshold, so a dose that commits a naive
effector no longer commits the treated one (measured challenge commit falling from %.3f naive to %.3f after the
protocol, the threshold raised monotonically with protocol length). The window is real and bounded: an
over-aggressive ABOVE-crossover protocol SENSITIZES instead (measured challenge commit %.2f), because tolerance
out-accumulates priming only below the measured crossover dose %.3f. Basin-acting controlled re-tolerization
desensitizes; avoidance alone leaves the latched state in place.</p>
<p class="fineprint">Part of the <a href="/immune_hematologic_vp_site/08-disease-treatment-axis-basin-acting-cures/">disease/treatment axis</a>: a pathological immune state is a latched basin, and the durable class of intervention moves the system across the saddle-node rather than only holding the drive down, which relapses on withdrawal.</p>""" % (
            esen["sensitization_threshold"]["single_dose"]["lymphoid_adaptive"]["d_crit_over_spinodal"],
            esen["sensitization_threshold"]["repetition"][0]["n_crit"],
            esen["sensitization_threshold"]["repetition"][-1]["n_crit"],
            esen["latch"]["on_after_clear"],
            esen["desensitization"]["naive_commit"],
            esen["desensitization"]["protected_commit"],
            esen["controlled_window"]["aggressive_commit"],
            esen["controlled_window"]["crossover_dose"]),
    ))

    # 12 — immunodeficiency reconstitution (T30 one lever, two diseases; threshold-gated)
    secs.append(dict(
        slug="12-immunodeficiency-reconstitution", N=12,
        title="Immunodeficiency Reconstitution: One Lever, Two Diseases",
        descr="Acquired immunodeficiency is the collapse of one surveillance-strength lever that drives both "
              "opportunistic infection and immune-escape malignancy; reconstitution is threshold-gated, so partial "
              "restoration below the coverage threshold is not a partial cure.",
        answer="Acquired immunodeficiency is the collapse of a single surveillance-strength lever: below a coverage "
               "threshold broad protection fails and opportunistic burden rises as 1/surveillance, while on the same "
               "lever a tumour escapes below its own threshold — one lever, two diseases. Reconstitution is "
               "threshold-gated; partial restoration below it is not a partial cure. DIRECTION/CLASS only, not "
               "medical advice. Grade [V].",
        abstract="Acquired immunodeficiency is a collapse of a single surveillance-strength lever: below a coverage "
                 "threshold broad protection collapses and pathogen burden rises as 1/surveillance, while on the same "
                 "lever a tumour escapes below its own threshold — one lever, two diseases. Reconstitution is "
                 "threshold-gated: restoring surveillance past a critical level re-establishes coverage and clears "
                 "the burden, while sub-threshold restoration fails and the required level scales with the depth of "
                 "the deficit. Partial immune reconstitution is not a partial cure; measured dynamics [V], absolute "
                 "scale [O].",
        grade_token="[V]",
        cards=[spinodal_card, barrier_card],
        body="""<h2>Immunodeficiency reconstitution: one lever, two diseases</h2>
<p>Acquired immunodeficiency is a collapse of a single surveillance-strength lever. Below a coverage threshold
(measured surveillance %.2f) broad protection collapses and the pathogen burden rises as 1/surveillance, while on
the SAME lever a tumour escapes below its own threshold (%.2f) &mdash; one lever, two diseases (an opportunistic
infection and an immune-escape malignancy), the unified substrate of the immunocompromised state. Reconstitution
is THRESHOLD-GATED: restoring surveillance past a critical level (measured %.2f) re-establishes coverage and
clears the burden, while sub-threshold restoration fails, and the required level scales with the DEPTH of the
deficit. Partial immune reconstitution is not a partial cure &mdash; it must cross the coverage threshold.</p>
<p class="fineprint">Part of the <a href="/immune_hematologic_vp_site/08-disease-treatment-axis-basin-acting-cures/">disease/treatment axis</a>: a pathological immune state is a latched basin, and the durable class of intervention moves the system across the saddle-node rather than only holding the drive down, which relapses on withdrawal.</p>""" % (
            erec["coverage_collapse"]["sv_coverage_crit"],
            erec["coverage_collapse"]["sv_opportunistic_crit"],
            erec["reconstitution"]["reconstitution_threshold"]),
    ))

    # 13 — lineage-targeted autoimmune cytopenia (T33 attack read out on a blood count)
    secs.append(dict(
        slug="13-autoimmune-cytopenia-lineage-targeted", N=13,
        title="Lineage-Targeted Autoimmune Cytopenia: The Attack Read Out on a Blood Count",
        descr="Lineage-targeted autoimmune cytopenia is the autoreactive R19 switch reading out on a blood count: a "
              "transient re-tolerization restores output durably while suppression lets it re-collapse, and lineage "
              "support sets only the rate, not the destination.",
        answer="When the autoreactive clone targets a blood lineage, the latched attack collapses produced output "
               "from healthy to a cytopenic floor, gated by the same supra-spinodal break. Transient re-tolerization "
               "restores output durably, while suppression lets it re-collapse on withdrawal; lineage support alone "
               "is cleared, but support plus the cure reaches health faster. DIRECTION/CLASS only, not medical "
               "advice. Grade [V].",
        abstract="When the autoreactive clone's target is a produced blood lineage, the disease reads out on a cell "
                 "count: while the clone is latched ON the produced output collapses from its healthy level to a "
                 "cytopenic floor, gated by the same supra-spinodal break. A transient re-tolerization restores the "
                 "output durably while a sub-critical suppressor only contains the attack and the output re-collapses "
                 "on withdrawal; lineage support alone is cleared, but support plus the cure reaches the same healthy "
                 "destination faster — the cure sets the destination, support only the rate. Measured dynamics [V], "
                 "absolute clinical scale [O], not medical advice.",
        grade_token="[V]",
        cards=[spinodal_card, barrier_card],
        body="""<h2>Lineage-targeted autoimmune cytopenia</h2>
<p>When the autoreactive clone's target is a produced blood lineage, the disease reads out on a cell count. While
the clone is latched ON it raises the clearance of the lineage, so the produced output COLLAPSES from its healthy
level to a cytopenic floor (measured %.2f &rarr; %.2f of healthy) &mdash; and the collapse is gated by the same +spinodal
break, a sub-spinodal insult leaving the output healthy (%.2f) and a supra-spinodal one collapsing it (%.2f). The
treatment classes separate exactly as before: a transient re-tolerization restores the output DURABLY (to %.0f%%
of healthy) while a sub-critical suppressor only contains the attack and the output RE-COLLAPSES on withdrawal
(to %.0f%%). Lineage SUPPORT alone is insufficient &mdash; the ongoing attack clears the supported output (%.0f%%) &mdash;
but the COMBINATION of re-tolerization plus support reaches the SAME healthy destination FASTER than the cure
alone (time-to-recovery %d vs %d steps): the cure sets the destination, support only sets the rate.</p>
<p class="fineprint">Part of the <a href="/immune_hematologic_vp_site/08-disease-treatment-axis-basin-acting-cures/">disease/treatment axis</a>: a pathological immune state is a latched basin, and the durable class of intervention moves the system across the saddle-node rather than only holding the drive down, which relapses on withdrawal.</p>""" % (
            ecyt["output_collapse"]["healthy_output_norm"],
            ecyt["output_collapse"]["attacked_output_norm"],
            ecyt["output_collapse"]["break_sub_spinodal_output"],
            ecyt["output_collapse"]["break_supra_spinodal_output"],
            ecyt["durable_vs_relapsing"]["retolerize_output_end"] * 100.0,
            ecyt["durable_vs_relapsing"]["suppress_output_after_withdrawal"] * 100.0,
            ecyt["combination"]["support_only_output_end"] * 100.0,
            ecyt["combination"]["t_recover_combination"], ecyt["combination"]["t_recover_retolerize"]),
    ))

    # 14 — systemic inflammation (T31 self-sustaining cytokine latch + time-critical break window)
    secs.append(dict(
        slug="14-systemic-inflammation-cytokine-latch", N=14,
        title="Systemic Inflammation: The Cytokine Latch and the Break Window",
        descr="Systemic inflammation past a critical insult is a self-sustaining cytokine latch that holds itself ON "
              "after the trigger is removed; the latch must be actively broken and the break is time-critical, with "
              "the coupling-off control staying flat.",
        answer="A systemic inflammatory response couples responders through shared cytokine tone. Past a critical "
               "insult the population self-sustains after the trigger is removed, the cytokine feed-forward holding "
               "itself ON, so removing the trigger is insufficient and the latch must be actively broken within a "
               "time-critical window. With coupling off the system cannot latch. DIRECTION/CLASS only, not medical "
               "advice. Grade [V].",
        abstract="A systemic inflammatory response couples many responders through a shared cytokine tone, and past "
                 "a critical insult near the single-cell threshold the population self-sustains after the external "
                 "trigger is removed — the cytokine feed-forward holds itself ON, the cytokine-storm latch. Removing "
                 "the trigger is therefore insufficient: the latch must be actively broken, and the break is "
                 "time-critical, an intervention window monotone in delay. The honest control switches the coupling "
                 "off, and the same insult sweep stays flat; measured dynamics [V], absolute scale [O].",
        grade_token="[V]",
        cards=[spinodal_card, barrier_card],
        body="""<h2>Systemic inflammation: the cytokine latch and the break window</h2>
<p>A systemic inflammatory response couples many responders through a shared cytokine tone. Past a critical
insult (measured %.3f&times; the spinodal, near the single-cell threshold) the population SELF-SUSTAINS after the
external trigger is REMOVED &mdash; the cytokine feed-forward holds itself ON (supra-threshold occupancy %.0f%% versus
sub-threshold %.0f%% after the trigger is withdrawn) &mdash; the cytokine-storm latch. Removing the trigger alone is
therefore insufficient; the latch must be actively broken. And the break is TIME-CRITICAL: an early counter-pulse
breaks the latch, but the same pulse applied too late fails, a measured intervention window monotone in delay.
The control is explicit: with the cytokine coupling switched off the system cannot latch and the same insult
sweep stays flat (occupancy range %.0f%% versus %.0f%% with coupling on).</p>
<p class="fineprint">Part of the <a href="/immune_hematologic_vp_site/08-disease-treatment-axis-basin-acting-cures/">disease/treatment axis</a>: a pathological immune state is a latched basin, and the durable class of intervention moves the system across the saddle-node rather than only holding the drive down, which relapses on withdrawal.</p>""" % (
            esep["systemic_latch_threshold"]["lymphoid_adaptive"]["a_crit_over_spinodal"],
            esep["self_sustain"]["frac_supra_after_withdraw"] * 100.0,
            esep["self_sustain"]["frac_sub_after_withdraw"] * 100.0,
            esep["feedback_control"]["range_alpha0"] * 100.0,
            esep["feedback_control"]["range_alpha_on"] * 100.0),
    ))

    # ---- chapter 15 (was 09; v0.14.0 science, unchanged): repertoire ageing (T34 immunosenescence) + durability-optimal re-boosting (T35) ----
    _isn_wy = eisn["windows"][0]; _isn_wo = eisn["windows"][-1]
    _isn_esc_y = eisn["escaped_young"] * 100.0; _isn_esc_o = eisn["escaped_old"] * 100.0
    _isn_nai_y = eisn["naive_young"] * 100.0;   _isn_nai_o = eisn["naive_old"] * 100.0
    _isn_affs = [w["escaped_mean_self_affinity"] for w in eisn["window_sweep"]
                 if w["escaped_mean_self_affinity"] is not None]
    _isn_aff = _isn_affs[-1] if _isn_affs else float("nan")
    _dbr_rep   = edbr["per_organ"]["lymphoid_adaptive"]
    _dbr_nb    = edbr["n_boost"]; _dbr_theta = edbr["theta"]
    _dbr_opt   = _dbr_rep["pf_optimum"] * 100.0
    _dbr_freq  = _dbr_rep["pf_too_frequent"] * 100.0
    _dbr_spc   = _dbr_rep["pf_too_spaced"] * 100.0
    _dbr_ivs   = ", ".join("%.1f" % x for x in edbr["optimal_interval_ascending_gamma"])
    secs.append(dict(
        slug="15-repertoire-ageing-durable-protection", N=15,
        title="Repertoire Ageing and Durable Protection: Thymic Involution and the Optimal Re-Boost Interval",
        descr="Two faces of immune time on the same R19 substrate. Thymic involution shrinks the education "
              "window so the repertoire drifts in opposite directions (autoreactive escape rises, naive export "
              "falls); and under a fixed booster budget the durability-optimal re-boost interval emerges at the "
              "measured memory half-life, with too-frequent and too-spaced boosting both losing coverage. "
              "Direction/class only \u2014 not medical advice.",
        answer="Immune time enters twice, each measured. Thymic involution shrinks the education window, so positive "
               "and negative selection truncate oppositely: autoreactive escape RISES while naive export FALLS. "
               "Under a fixed booster budget, protection peaks when the re-boost interval equals the measured memory "
               "half-life; too frequent or too sparse loses ground. DIRECTION/CLASS only, not a real-time schedule "
               "or medical advice. Grade [V].",
        abstract=f"Two ageing phenomena are read off the same kernel. Thymic involution is the same central-"
                 f"tolerance education run with a slowly shrinking window: as the window shrinks (model-time "
                 f"{_isn_wy:.0f}\u2009\u2192\u2009{_isn_wo:.0f}, absolute scale [O]) the measured escaped-autoreactive "
                 f"fraction RISES ({_isn_esc_y:.2f}%\u2009\u2192\u2009{_isn_esc_o:.2f}% of the cohort) while the healthy "
                 f"naive-export rate FALLS ({_isn_nai_y:.1f}%\u2009\u2192\u2009{_isn_nai_o:.1f}%), the escapees concentrated "
                 f"just above threshold (mean self-affinity {_isn_aff:.3f}\u00d7 the spinodal). For protective memory "
                 f"that wanes by the measured barrier-crossing decay, a fixed budget of {_dbr_nb} boosters over a "
                 f"finite horizon gives an interior-peaked protected fraction: the optimum sits at the measured "
                 f"half-life (peak coverage {_dbr_opt:.0f}% of the horizon), boosting too frequently falls to "
                 f"{_dbr_freq:.0f}% and too sparsely to {_dbr_spc:.0f}%, and the optimal interval tracks durability "
                 f"across compartments (ascending-durability optimal intervals {_dbr_ivs}, model-time, [O]).",
        grade_token="[V]",
        cards=[barrier_card, spinodal_card],
        body=f"""<h2>Two faces of immune time</h2>
<p>The preceding chapters treated the immune system at a fixed age. This chapter adds TIME in two distinct
senses, both read off the SAME R19 substrate. The first is the slow ageing of the repertoire-generating organ:
thymic involution, the lifelong shrinking of the thymic education window, and what that shrinking does to the
cells the thymus exports. The second is the waning of established protective memory and how to re-boost it:
given a fixed budget of boosters and a finite protection horizon, what spacing keeps protection up for the
largest fraction of that horizon. Neither answer is assumed; each EMERGES, measured, from dynamics already used
in this volume.</p>

<h2>Thymic involution: one shrinking window, two opposite drifts</h2>
<p>This volume established thymic education as a saddle-node problem. A thymocyte carries a self-affinity and is
educated under a corresponding self-drive; POSITIVE selection (survival) requires it to accumulate enough
self-engagement within the window or it dies by neglect, while NEGATIVE selection DELETES it if its
self-reactivity carries it across the activation threshold. Both events are CROSSINGS that take time. Thymic
involution is that same education run with a slowly SHRINKING window, and because both selection events are
time-costed, a shorter (older) window truncates them &mdash; in OPPOSITE directions, which the simulation measures
directly. As the window shrinks from its youngest to its oldest setting (model-time {_isn_wy:.0f}&nbsp;&rarr;&nbsp;{_isn_wo:.0f},
absolute scale [O]) the measured escaped-autoreactive fraction RISES (from {_isn_esc_y:.2f}% to {_isn_esc_o:.2f}%
of the cohort) while the healthy naive-export rate FALLS (from {_isn_nai_y:.1f}% to {_isn_nai_o:.1f}%). The two
outputs DIVERGE: an older thymus exports FEWER fresh naive cells AND lets MORE self-reactive clones slip
through.</p>
<p>The mechanism of each direction is explicit. Near-threshold self-reactive clones need the LONGEST time to
cross the activation threshold, so they are the first to miss deletion when the window shortens &mdash; the escapees
are concentrated just above threshold (measured mean self-affinity {_isn_aff:.3f}&times; the spinodal at the
oldest window), exactly the central-tolerance sliver of the earlier tolerance chapter widened by age. Marginal
clones near the survival cut need the longest time to accumulate their positive-selection signal, so they are
the first to die by neglect when the window shortens, and the export rate falls. The youngest window is the
honest control: there the escaped fraction is only {_isn_esc_y:.2f}% and the export rate is at its maximum, so
the drift is an ageing effect of the shrinking window, not a baseline artefact. This is the dynamical signature
of immunosenescence &mdash; falling thymic output AND rising autoreactive escape &mdash; read as a single coupled
consequence of one shrinking education window, measured rather than assumed.</p>

<h2>Durable protection: re-boost as protection wanes</h2>
<p>The memory chapter (&sect;4) measured that a protective ON state decays by spontaneous barrier crossing, with
a durability that ranks by the barrier across the four compartments. Build on that measured decay. Suppose
protective memory has been established and then WANES by exactly that process, and you hold a FIXED budget of
{_dbr_nb} booster events to spend over a finite protection horizon; a booster re-flips the waning pool back to
full protection. The question is purely about SPACING: what re-boost interval keeps the model protected &mdash; the
protected pool fraction above the protection threshold &theta;&nbsp;=&nbsp;{_dbr_theta} &mdash; for the largest fraction of the
horizon.</p>
<p>The answer EMERGES from the measured decay curve. Sweeping the re-boost interval as a multiple r of the
MEASURED protection half-life, the protected fraction of the horizon is an INTERIOR-peaked function: it rises to
a clear maximum and falls on both sides. The peak sits at r&nbsp;&asymp;&nbsp;1 &mdash; the optimal spacing is to re-boost JUST AS
protection wanes through the threshold, so the optimal interval EQUALS the measured memory half-life, read off
the substrate rather than posited (peak coverage {_dbr_opt:.0f}% of the horizon). Both failure modes are
measured. Boosting TOO FREQUENTLY (r well below 1) piles the fixed budget up early while protection is still
high, exhausts it before the horizon ends, and leaves the late horizon unprotected (protected fraction falls to
{_dbr_freq:.0f}%). Boosting TOO SPARSELY (r well above 1) lets each booster's protection lapse before the next
arrives, opening susceptible gaps between boosters (protected fraction {_dbr_spc:.0f}%). The optimum also TRACKS
durability across compartments: because the optimal multiple is r&nbsp;&asymp;&nbsp;1 for every compartment, the absolute
optimal interval inherits the memory-durability ranking &mdash; the longer-memory (deeper-barrier) compartment
carries the LONGER optimal re-boost interval (measured optimal intervals in model-time, ascending durability:
{_dbr_ivs}; absolute scale [O]). The honest control switches the decay OFF: with memory that never wanes the
protected fraction is FLAT across every interval, so the interior optimum is created by the MEASURED waning, not
by the bookkeeping of the schedule.</p>
<p>This durability optimum is mechanistically DISTINCT from the affinity-maturation prime&ndash;boost optimum
established earlier in this volume. That inverted-U arises from germinal-centre maturation kinetics under a
persisting antigen depot; this one arises from the half-life of protective memory. Two different optima from two
different mechanisms, each measured from the substrate.</p>

<h2>What this is &mdash; and is not</h2>
<p>Both results are re-descriptions of well-known immune-ageing and booster-scheduling phenomena in the R19
formalism. The measured content is QUALITATIVE and relative: the direction of the two repertoire drifts and
their divergence, the near-threshold concentration of the escapees, and &mdash; for re-boosting &mdash; the existence and
INTERIOR location of the protected-fraction optimum, its coincidence with the measured memory half-life, the two
failure modes, the cross-compartment tracking, and the decay-driven control. This is a DIRECTION/CLASS statement
about repertoire ageing and re-boost timing; it is NOT a schedule, an interval in real time, a clinical
protocol, or a recommendation for any individual, and it is NOT medical advice. The model does not invent any
absolute scale: the education-window length, the positive-selection quota, the protection threshold &theta;, the
re-boost interval and memory half-life in real units, and the cellular-noise scale are all left [O] with the
obstacle stated. It is NOT a validation of VP theory. Every measured direction here is graded [V] and reproduced
deterministically from the same kernel as the rest of this volume.</p>""",
    ))

    # ------------------------------------------------------------------ v0.16.0 cross-package seam layer
    sv = NUM["seamv"]; sgut = sv["gut_immune_identity"]; snin = sv["neuroimmune_stress_in"]
    snout = sv["neuroimmune_cytokine_out"]; sfw = sv["firewall"]; sss = sv["ssot_consistency"]
    s_ind  = sgut["digestive_induction"]; s_mnt = sgut["digestive_maintenance"]
    s_spg1 = sgut["substrate_spinodal_g1"]; s_antig = round(s_ind - s_spg1, 4)
    seam_sha = NUM["seam_sha"]; fw_imports = sfw["sibling_import_count"]; fw_files = sfw["python_files_scanned"]
    DIG_DOI = "10.5281/zenodo.20755319"; MIND_DOI = "10.5281/zenodo.20694404"
    DIG_URL = "https://doi.org/" + DIG_DOI; MIND_URL = "https://doi.org/" + MIND_DOI

    gut_seam_card = vp_card("gut-seam", "gut–immune seam",
        "digestive's IBD mucosal latch IS this volume's tolerance switch localised: the LIVE induction "
        "threshold %.4f equals the T23 saddle-node (luminal antigen %.2f + spinodal %.4f = total drive at the "
        "spinodal) and the maintenance threshold %.4f equals the T24 suppressor complement (antigen − spinodal); "
        "relapsing hysteresis is the T23 irreversibility. Same byte-identical R19 substrate. This volume owns the "
        "systemic tolerance primitive; digestive owns the mucosal localisation and the absolute antigen scale [O]."
        % (s_ind, s_antig, s_spg1, s_mnt),
        "[V]", "digestive volume §22 (gut mucosal owner)", DIG_URL)
    neuro_seam_card = vp_card("neuro-seam", "neuro–immune seam",
        "two firewall-respecting directions on the shared substrate. IN: mind's HPA/cortisol descriptor maps "
        "onto the T24 suppressor σ as a SIGN only (sustained cortisol deepens peripheral tolerance, lowering "
        "surveillance); the magnitude is [O] and σ is swept, never tuned, and no cortisol value is imported. "
        "OUT: the cytokine tone M (T31) is a one-way pointer to mind's INFLAMMATORY contributor to depression "
        "(mind §27); felt low mood stays behind mind's Axis-A consciousness firewall.",
        "[F]", "mind volume (felt / HPA owner)", MIND_URL)
    onc_hub_card = vp_card("onc-hub", "oncology hub spoke",
        "the immune_escape_factor is a site-independent 1/(1−escape) multiplier on EVERY volume's cancer kernel "
        "(T10, measured from a coupled influx–clearance process), and Lever D (T15) is its therapy face. This is "
        "the third hub spoke and the one seam this volume already shipped internally (chapter 5).",
        "[V]", "this volume §5 (surveillance seam)", None)

    secs.append(dict(
        slug="16-cross-system-seams-wired", N=16,
        title="Cross-System Seams, Wired",
        descr="The immune volume is a hub: three seams wire it to the digestive and mind volumes and to every "
              "cancer kernel, all on one byte-identical R19 substrate with the no-sibling-import firewall enforced.",
        answer="This volume is a hub. Three seams wire it to its siblings on one byte-identical substrate: "
               "digestive's IBD mucosal latch IS this volume's T23 saddle-node (induction %.4f) and T24 suppressor "
               "complement (maintenance %.4f); mind's cortisol raises T24 suppression (sign only) while cytokine "
               "tone exits to mind's inflammatory mood contributor; immune-escape multiplies every cancer kernel. "
               "Zero sibling imports. Grade [V]."
               % (s_ind, s_mnt),
        abstract="The seam layer carries its OWN 2×sha256 (%s…), separate from the engine emit() hash, and imports "
                 "ZERO sibling code across %d scanned files. Gut–immune: induction %.4f = antigen %.2f + spinodal "
                 "%.4f (T23 saddle-node) and maintenance %.4f = antigen − spinodal (T24 suppressor complement), "
                 "relapsing = T23 irreversibility, all closed-form on the shared substrate. Neuro–immune IN: "
                 "cortisol→T24 σ is consumed as sign only (wired=%s, no numeric mind value). Neuro–immune OUT: "
                 "cytokine M→mood is a one-way pointer (dependency=%s). SSOT consistent: %s."
                 % (seam_sha[:8], fw_files, s_ind, s_antig, s_spg1, s_mnt,
                    str(bool(snin["wired"])).lower(), str(not snout["pointer_not_dependency"]).lower(),
                    str(bool(sss["ssot_consistent"])).lower()),
        grade_token="[V]",
        cards=[gut_seam_card, neuro_seam_card, onc_hub_card],
        body=f"""<h2>The immune volume is a hub, not an island</h2>
<p>The intra-volume roadmap of this package is exhausted: the thirty-five stress targets from clonal selection
through immunosenescence all read out one R19 substrate. The natural next growth is OUTWARD &mdash; the immune
system is where three other VP volumes physically meet. Immunosurveillance touches every cancer kernel; gut
mucosal tolerance is the immune tolerance switch localised to the gut wall; and the stress/inflammation axis is
the immune system reading the mind's HPA cascade and writing back an inflammatory tone. This chapter WIRES those
three seams &mdash; and the wiring is disciplined: the gated package imports zero sibling code (scan over
{fw_files} Python files returns {fw_imports} violations), so each volume still re-establishes its entire trusted
state from its own archive with the siblings absent.</p>

<h2>Seam 1 &mdash; gut&ndash;immune: IBD mucosal latch IS the tolerance saddle-node</h2>
<p>The digestive volume's inflammatory-bowel-disease course is not a separate model. On the byte-identical R19
substrate, its mucosal latch is exactly this volume's tolerance switch localised to the gut wall. The seam reads
digestive's vendored IBD snapshot (mucosal R19 scale &gamma;=1, luminal antigen drive {s_antig:.2f}) and confirms
in CLOSED FORM that the induction threshold <b>{s_ind:.4f}</b> equals the T23 saddle-node &mdash; antigen
{s_antig:.2f} plus the substrate spinodal {s_spg1:.4f}, i.e. the total drive sitting exactly at the spinodal where
the OFF basin disappears &mdash; while the maintenance threshold <b>{s_mnt:.4f}</b> equals the T24 suppressor
complement, antigen minus spinodal. The relapsing hysteresis of IBD is the T23 irreversibility (pathological
memory): once the latch flips, removing the trigger does not restore the OFF state. Two volumes, one switch. The
division of ownership is explicit: THIS volume owns the systemic tolerance primitive (the T23/T24 saddle-node and
its complement); the digestive volume owns the gut localisation, the absolute mucosal antigen scale, and the felt
visceral dimension &mdash; all [O] here, owned there.</p>

<h2>Seam 2 &mdash; neuro&ndash;immune: two firewall-respecting directions</h2>
<p>The mind volume and this one share the substrate but are separated by a strict firewall: the mind owns
everything FELT (its Axis-A consciousness-claim firewall is held at zero), and this volume owns everything
immune. Two directions cross that boundary without breaching it.</p>
<p><b>IN (stress &rarr; suppression).</b> The mind's HPA/cortisol cascade (PVN&rarr;ACTH&rarr;cortisol) is read in
as a SIGN only: a sustained cortisol/stress drive deepens peripheral tolerance, raising the T24 suppressor
&sigma; and lowering surveillance &mdash; the textbook stress-immunosuppression direction. The CLAIM is the sign;
the MAGNITUDE (how much &sigma; per unit cortisol) is left [O], and &sigma; is SWEPT across its range rather than
fitted, so nothing is tuned. The immune engine never imports a cortisol number (sign-only consumption confirmed:
takes_no_numeric_mind_value = {str(bool(snin["takes_no_numeric_mind_value"])).lower()}).</p>
<p><b>OUT (inflammation &rarr; mood).</b> The cytokine tone M from the systemic-inflammation latch (T31) is a
ONE-WAY forward pointer to the mind volume's depression chronification (mind &sect;27), which lists an
INFLAMMATORY contributor alongside the monoaminergic, HPA-axis, circadian and psychosocial ones &mdash; not a
single mechanism. The pointer states WHERE the inflammatory drive travels; it consumes no mind value
(pointer_not_dependency = {str(bool(snout["pointer_not_dependency"])).lower()}). The felt low mood itself is the
mind's, behind its firewall. This volume claims only that the cytokine tone it owns is an input to that
multi-factor picture, never that inflammation IS depression.</p>

<h2>Seam 3 &mdash; the oncology hub spoke</h2>
<p>The third spoke is the one this volume already shipped internally. The immune_escape_factor is a
site-independent multiplier 1/(1&minus;escape) on every volume's cancer kernel (chapter 5, T10, measured from a
coupled influx&ndash;clearance process), and Lever D (T15) is its therapy face. Surveillance is therefore not a
local immune story but a cross-cutting seam onto every malignancy the VP program models &mdash; the hub's first
and oldest spoke, now sitting alongside the gut and neuro seams.</p>

<h2>The firewall, enforced not asserted</h2>
<p>The seam layer is gated by an architectural lock, not a promise. A scan of every Python file in the package
({fw_files} files) returns {fw_imports} sibling imports; and the emitted EMERGENCE state (the engine's
circulate() object) carries no felt/HPA/cortisol/mind key, so organ emergence, the tolerance saddle-node, the
cytokine latch and the surveillance seam are all computed with zero reference to a mind quantity. The seam layer
carries its own 2&times;sha256 ({seam_sha[:8]}&hellip;), entirely separate from the engine emit() determinism
hash, the thirty-five-target stress battery and the six discipline gates &mdash; all of which are byte-unchanged
by this layer. The single source of truth is inherited/cross_references.json: all three seams are declared there
once, and the gut induction/maintenance values used in the identity match that file
(ssot_consistent = {str(bool(sss["ssot_consistent"])).lower()}).</p>

<h2>What this is &mdash; and is not</h2>
<p>This chapter makes structural identity claims on a shared substrate, not numeric predictions. The gut&ndash;
immune identity is closed-form and exact; the neuro&ndash;immune seams are a SIGN (IN) and a one-way POINTER
(OUT), both deliberately magnitude-free. No absolute scale is invented here: the mucosal antigen scale, the
cortisol&rarr;&sigma; gain, and the cytokine&rarr;mood weight are all [O], each owned by the volume that can
anchor it. It is a DIRECTION/CLASS statement about how the immune hub couples to digestion and to the mind; it is
NOT a clinical claim and NOT medical advice. It is NOT a validation of VP theory &mdash; only a demonstration that
one substrate, derived once, is read consistently across four volumes without a refit.</p>""",
    ))

    # ------------------------------------------------------------------ v0.16.0 live cross-package harness
    hc = NUM["hcontract"]; h_sha = NUM["harness_sha"]
    h_idok = hc["shared_substrate"]["closed_form_identity_ok"]
    h_gi = hc["gut_saddle_node_identity"]; h_ind = h_gi["induction_closed"]; h_mnt = h_gi["maintenance_closed"]

    harness_card = vp_card("harness-digest", "harness contract digest",
        "the harness digest (%s…) hashes ONLY the immune-side contract — the closed-form substrate identity, the "
        "vendored digestive IBD snapshot, the gut saddle-node identity and the neuro-immune endpoint descriptor — "
        "all computed from this package's own modules with NO sibling present, so it is byte-identical whether the "
        "siblings are on disk or absent. The engine emit() 2×sha256, the 35-target battery and the six discipline "
        "gates are all unchanged; this layer carries its own 2×sha256." % h_sha[:8],
        "[F]", "out of gate: repro/run_harness.py", None)
    drift_card = vp_card("substrate-drift", "cross-volume substrate drift",
        "every sibling volume's spinodal 2(γ/3)^1.5 and barrier γ²/4 are byte-identical with this volume's — "
        "the live runner measures cross-volume drift exactly 0 across immune↔digestive↔mind — which is the "
        "foundation that lets the tolerance saddle-node derived here be READ in digestive's mucosa and mind's "
        "HPA cascade with no refit.",
        "[V]", "canonical derivation: substrate R19", None)

    secs.append(dict(
        slug="17-live-cross-package-harness", N=17,
        title="The Live Cross-Package Harness",
        descr="An out-of-gate runner loads the sibling volumes live and checks the chapter-16 seam identities "
              "against their real engines; its digest hashes only the immune-side contract, byte-identical with "
              "or without siblings.",
        answer="The seam layer takes the sibling identities on trust; this harness verifies them live. An "
               "out-of-gate runner loads digestive and mind and confirms cross-volume substrate drift is exactly 0, "
               "digestive's LIVE IBD course reproduces the T23/T24 thresholds (induction %.4f, maintenance %.4f), "
               "and mind's module names the HPA and inflammatory endpoints. The digest hashes only the immune-side "
               "contract. Grade [V]."
               % (h_ind, h_mnt),
        abstract="The harness runs OUTSIDE every gate and SKIPS cleanly when siblings are absent, so it can never "
                 "break a sibling-free build. Its digest (%s…) hashes ONLY the immune-side contract — the "
                 "closed-form substrate identity (ok=%s), the vendored IBD snapshot, the gut saddle-node identity "
                 "(induction %.4f, maintenance %.4f) and the neuro-immune endpoint — computed with no sibling "
                 "present, hence byte-identical with or without them. When run with siblings present, all five live "
                 "checks pass: substrate drift 0 (immune↔digestive and immune↔mind), digestive's live "
                 "ibd_relapsing_course() reproduces the vendored thresholds AND equals this volume's T23/T24 "
                 "saddle-node, and mind's §27 module carries the HPA-cortisol (IN) and inflammatory (OUT) endpoints."
                 % (h_sha[:8], str(bool(h_idok)).lower(), h_ind, h_mnt),
        grade_token="[V]",
        cards=[harness_card, drift_card],
        body=f"""<h2>From trust to verification</h2>
<p>The seam layer (chapter 16) had to take three things on trust because the gated package may never import a
sibling: that digestive's substrate is byte-identical to this one, that digestive's LIVE inflammatory-bowel
course actually produces the IBD thresholds this volume vendored, and that the mind volume really carries the
endpoints the neuro&ndash;immune pointers land on. This harness discharges that trust. It loads THIS volume
together with its sibling volumes IN ONE PROCESS and checks the identities against the LIVE sibling engines
&mdash; not snapshots.</p>

<h2>The three live checks</h2>
<p><b>(1) Shared substrate, drift 0.</b> The harness loads each sibling's spinodal-bearing engine by file path and
compares its R19 spinodal 2(&gamma;/3)<sup>1.5</sup> and barrier &gamma;<sup>2</sup>/4 against this volume's,
bit-for-bit, over several &gamma; values. The measured cross-volume drift is exactly 0 for both immune&harr;
digestive and immune&harr;mind. This is the foundation: a zero-drift substrate is what lets the tolerance
saddle-node derived HERE be read in digestive's mucosa and in mind's HPA cascade without any refit.</p>
<p><b>(2) Gut&ndash;immune latch identity, live.</b> The harness calls digestive's LIVE
ibd_relapsing_course() and confirms its induction threshold ({h_ind:.4f}), maintenance threshold
({h_mnt:.4f}) and relapsing flag reproduce the snapshot this volume vendored &mdash; AND that those live
thresholds equal this volume's own T23 saddle-node (antigen + spinodal) and T24 suppressor complement
(antigen &minus; spinodal). So the claim of chapter 16 &mdash; that the gut mucosal tolerance latch IS this
volume's machinery localised &mdash; is verified against digestive's real code, not merely asserted from a
copied number.</p>
<p><b>(3) Neuro&ndash;immune endpoint, live.</b> The harness loads the mind engine (confirming the same spinodal)
and reads mind's depression-chronification module (mind &sect;27), confirming it names the HPA/cortisol cascade
(the substrate for the IN direction) and the INFLAMMATORY contributor (where the OUT cytokine pointer lands).
The seam endpoints are real reading points in the sibling volume, not dangling references.</p>

<h2>Why this cannot break the build</h2>
<p>The harness runs OUTSIDE every gate. The research gate (repro/run_all.py) and the canonical build
(tools/build_docs.py) compute nothing here and never import a sibling; each volume still re-establishes its
entire trusted state from its own archive with the siblings ABSENT &mdash; the verify-alone invariant. When the
siblings are not discoverable on disk, this module SKIPS the live checks and exits cleanly. The sibling engines
are loaded by FILE PATH under unique module names with the package-internal module table cleared between loads
(so two volumes' identically-named vp_substrate cannot collide) &mdash; this is loading, not importing: no
sibling code path is wired into this volume's engine.</p>
<p>Crucially, the harness digest hashes ONLY the immune-side contract &mdash; the closed-form substrate identity
(ok={str(bool(h_idok)).lower()}), the vendored IBD snapshot, the gut saddle-node identity ({h_ind:.4f} /
{h_mnt:.4f}) and the neuro&ndash;immune endpoint descriptor. That contract is computed from THIS package's own
modules with no sibling present, so the harness digest ({h_sha[:8]}&hellip;) is byte-identical whether or not the
siblings are on disk &mdash; exactly what a deterministic build requires. The engine circulate()/emit()
2&times;sha256 (e7a2a5b8&hellip;), the thirty-five-target stress battery, the six discipline gates and the seam
digest are ALL unchanged by this layer; the harness carries its OWN 2&times;sha256.</p>

<h2>What this is &mdash; and is not</h2>
<p>The harness is a reproducibility instrument, not a new scientific claim. It adds no physics &mdash; it
confirms that the four volumes share one substrate and that the seam identities hold against the live sibling
code. It is run with <code>python repro/run_harness.py</code> when the sibling packages are present. It is NOT
part of any gate, NOT a clinical claim, and NOT a validation of VP theory; it is the evidence that the
cross-package identities of chapter 16 are real, live, and deterministic.</p>""",
    ))

    # ------------------------------------------------------------------ v0.17.0 circulatory + musculoskeletal spokes (S18)
    seamv18 = NUM["seamv"]
    circ = seamv18["circulatory_trafficking"]; msk = seamv18["musculoskeletal_marrow"]
    seam_sha18 = NUM["seam_sha"]
    c_org = circ["production_root_organ"]; c_gene = circ["production_root_master_gene"]
    c_sp = circ["production_root_spinodal_live"]; c_ba = circ["production_root_barrier_live"]
    m_sp = msk["hematopoietic_root_spinodal_live"]; m_ba = msk["hematopoietic_root_barrier_live"]
    CIRC_DOI = "10.5281/zenodo.20754354"
    circ_ok = bool(circ["pointer_not_dependency"] and circ["endpoint_is_real"])
    msk_ok = bool(msk["pointer_not_dependency"] and msk["endpoint_is_real"])

    circ_spoke_card = vp_card("circulatory-spoke", "leukocyte-trafficking pointer",
        "the leukocyte effector populations (R19 ON-committed clones, rooted at %s, %s, spinodal %.6f) point "
        "one-way OUT into the circulatory vasculature; the pointer consumes no circulatory value and lands on "
        "a REAL in-package organ (pointer-not-dependency %s). The circulatory volume owns the absolute "
        "vascular transport scale [O]."
        % (c_org, c_gene, c_sp, str(circ_ok).lower()),
        "[F]", "circulatory volume (owner)", "https://doi.org/" + CIRC_DOI)
    msk_spoke_card = vp_card("marrow-niche-spoke", "marrow-niche pointer + identity candidate (resolved §20)",
        "the haematopoietic origin (%s, %s, spinodal %.6f, barrier %.6f) is housed in the musculoskeletal "
        "marrow niche; declared as a one-way pointer (no musculoskeletal value consumed, pointer-not-dependency "
        "%s), with a shared-substrate-identity UPGRADE NAMED here as a candidate. It was later LIVE-VERIFIED and "
        "RETIRED in §20 once the musculoskeletal volume arrived — the niche is built by RUNX2, a different switch "
        "from the hematopoietic RUNX1, so the pointer survives but the identity does not."
        % (msk["hematopoietic_root_organ"], msk["hematopoietic_root_master_gene"], m_sp, m_ba,
           str(bool(msk["pointer_not_dependency"])).lower()),
        "[F]", "musculoskeletal volume (owner; DOI to-reconcile)", None)

    secs.append(dict(
        slug="18-circulatory-musculoskeletal-spokes", N=18,
        title="Circulatory & Musculoskeletal Spokes",
        descr="Two inherited adjacencies become declared one-way-pointer seams: leukocyte trafficking into the "
              "circulatory vasculature and the haematopoietic root housed in the musculoskeletal marrow niche, "
              "with the firewall and the byte-identical engine hash kept.",
        answer="Two more spokes promote inherited adjacencies to declared seams. Leukocyte effector populations, "
               "rooted at bone-marrow haematopoiesis (%s), point one-way into the circulatory vasculature; the "
               "same haematopoietic root is housed in the musculoskeletal marrow niche. Both consume no sibling "
               "value; engine hash byte-identical; the niche identity is a named candidate, not claimed."
               % c_gene,
        abstract="The seam layer now carries five declared seams under one 2×sha256 (%s…), still importing ZERO "
                 "sibling code. Circulatory: the leukocyte effector populations (rooted at %s, %s; spinodal "
                 "%.6f, barrier %.6f) are a one-way pointer OUT to vascular transport — the immune volume owns "
                 "the populations, the circulatory volume owns the absolute transport scale [O]. Musculoskeletal: "
                 "the haematopoietic root (same organ) is housed in the marrow niche — a one-way pointer now, "
                 "with a shared-substrate-identity upgrade (niche threshold = %.6f) NAMED but not claimed awaiting "
                 "a live musculoskeletal run. Both pointers land on a real in-package organ; neither feeds the "
                 "hashed engine core."
                 % (seam_sha18[:8], c_org, c_gene, c_sp, c_ba, m_sp),
        grade_token="[F]",
        cards=[circ_spoke_card, msk_spoke_card],
        body=f"""<h2>From inherited adjacency to a declared spoke</h2>
<p>The hub picture of chapter 16 listed two relationships that were already present through inherited
primitives but had not yet been promoted to explicitly declared seams: the circulatory volume carries the
vasculature on which immune cells traffic, and the musculoskeletal volume holds the bone compartment that
houses haematopoiesis. This chapter promotes both to declared entries in the single source of truth
(inherited/cross_references.json), each as a one-way POINTER — the weakest, safest seam kind, which states
where something travels and consumes no sibling value. The hub now has five spokes, not three, and the
discipline is unchanged: the gated package imports zero sibling code, and the engine emit() determinism hash
is byte-identical because nothing here feeds the hashed core.</p>

<h2>Circulatory: leukocyte trafficking is a one-way pointer</h2>
<p>The leukocyte effector populations of this volume — the ON-committed clones of the R19 switch, rooted at
the haematopoietic organ {c_org} (master gene {c_gene}, spinodal {c_sp:.6f}, barrier {c_ba:.6f}) and selected
through the adaptive lymphoid compartment — travel through the circulatory vasculature to reach peripheral
tissue. That is the seam: a one-way pointer OUT from the immune effector populations to the circulatory
transport layer. The pointer carries no circulatory snapshot and consumes no circulatory value, so it is a
directional statement, not a numeric dependency. The ownership split is explicit: this volume owns the
effector populations (its own measured R19-committed output), while the circulatory volume owns the absolute
vascular transport scale — vessel geometry, blood flow, margination and extravasation kinetics — which stays
[O] here. Because the two volumes share one byte-identical R19 substrate, neither re-derives the other's part;
but unlike the gut seam this is deliberately not a closed-form identity, only a pointer, because no equality
between an immune quantity and a circulatory quantity is asserted.</p>

<h2>Musculoskeletal: the marrow niche, with a named identity upgrade</h2>
<p>The haematopoietic origin of every immune cell — the same organ {msk["hematopoietic_root_organ"]}
({msk["hematopoietic_root_master_gene"]}, spinodal {m_sp:.6f}, barrier {m_ba:.6f}), the stem-cell-to-lineage
branching that is the root of the whole system — is physically housed in the bone-marrow niche, the bone
compartment owned by the musculoskeletal volume. This chapter declares that relationship as a one-way pointer:
the immune volume owns the haematopoietic primitive, the musculoskeletal volume owns the absolute bone-niche
scale (trabecular architecture, niche capacity, marrow volume), which stays [O] here.</p>
<p>There is a stronger claim available, and the honest move is to name it without asserting it. If the
musculoskeletal volume's marrow-niche reading rides the same RUNX1 substrate, then the niche's
haematopoietic-commit threshold would equal this volume's {msk["hematopoietic_root_organ"]} spinodal
{m_sp:.6f} in closed form — a shared-substrate identity exactly analogous to the gut seam, where the IBD
induction threshold equals luminal antigen plus the spinodal. But verifying a shared-substrate identity
requires the live sibling engine, the way the gut identity is checked against digestive's live relapsing
course. The musculoskeletal volume is not on disk in this session, so the identity cannot be verified live.
The chapter therefore declares the weaker one-way pointer now and records the identity as a NAMED CANDIDATE
with a stated promotion path (add the volume to the live harness, confirm substrate drift zero and the niche
threshold equality) and a stated falsifier (if the niche threshold did not reduce to the haematopoietic
spinodal, the identity candidate is dead — the pointer survives, because a pointer asserts no equality).</p>

<h2>Why a pointer consumes nothing, and what is owned elsewhere</h2>
<p>A one-way pointer is the safest cross-package construct in the program precisely because it consumes no
sibling value. The immune engine computes the effector populations and the haematopoietic root with zero
circulatory or musculoskeletal input; the sibling volumes read only where those populations and that root sit
in their own tissue frame. The firewall is enforced, not asserted: a scan of every Python file in the gated
package returns zero sibling imports, and the emitted emergence state carries no sibling key. Each new pointer
lands on a real in-package organ — {c_org} — verified against this volume's own substrate, so neither pointer
is a dangling reference. The owner split is recorded for every cross-package quantity: the absolute vascular
transport scale belongs to the circulatory volume, the absolute bone-niche scale to the musculoskeletal
volume, and both are openly [O] here with their owner named.</p>

<h2>What this is &mdash; and is not</h2>
<p>This chapter is architecture and bookkeeping, not new physics. It adds no measurement to the thirty-five
stress targets and changes no number in the engine; it declares two structural relationships and states
honestly which is a pointer, which is a candidate identity, and what absolute scale is owned elsewhere and is
therefore [O] here. The cross-package statements are direction-and-structure claims — not medical advice, not
a validation of VP theory. The seam layer carries its own 2&times;sha256 ({seam_sha18[:8]}&hellip;), separate
from the engine emit() hash, which stays byte-identical.</p>""",
    ))
    # ------------------------------------------------------------------ v0.18.0 barrier-surface mucosal immunity (S19)
    bsa = NUM["seamv"]["barrier_surface_agnostic"]
    resp_c = NUM["seamv"]["respiratory_candidate"]; skin_c = NUM["seamv"]["skin_candidate"]
    seam_sha19 = NUM["seam_sha"]
    b_sp = bsa["substrate_spinodal_g1"]                          # 0.38490018
    b_oi = bsa["surface_independent_offset_induction"]           # +0.38490018
    b_om = bsa["surface_independent_offset_maintenance"]         # -0.38490018
    b_ga = bsa["gut_anchor_antigen"]                             # 0.50 (the one vendored point)
    b_gi = bsa["gut_anchor_induction"]                           # 0.8849
    b_gm = bsa["gut_anchor_maintenance"]                         # 0.1151
    sweep_n = len(bsa["antigen_sweep_rows"])
    b_sweep_str = ", ".join("%.2f" % r["antigen"] for r in bsa["antigen_sweep_rows"])
    IMM_DOI19 = "10.5281/zenodo.20755280"
    bsa_ok = bool(bsa["barrier_surface_agnostic"])
    resp_ok = bool(resp_c["named_candidate_not_claimed"] and resp_c["immune_side_tolerance_primitive_is_real"])
    skin_ok = bool(skin_c["pointer_live_verified"] and skin_c["reciprocal_immune_seam_present"]
                   and skin_c["immune_side_tolerance_primitive_is_real"])

    barrier_card = vp_card("barrier-agnostic", "surface-independent tolerance offset",
        "across an illustrative %d-point antigen sweep at the mucosal R19 scale (g=1.0), the offset from each "
        "surface's OWN antigen baseline is invariant: induction = antigen + %.5f, maintenance = antigen − %.5f "
        "(offset-invariant %s). The gut (antigen %.2f) is the one vendored, live-verified point on a "
        "barrier-agnostic line."
        % (sweep_n, b_oi, b_sp, str(bsa_ok).lower(), b_ga),
        "[F]", "immune volume (owner)", "https://doi.org/" + IMM_DOI19)
    resp_card = vp_card("respiratory-candidate", "airway-mucosa tolerance candidate",
        "a respiratory volume would localise this volume's T23/T24 tolerance switch to the airway mucosa — the "
        "gut shared-substrate identity re-applied to a second barrier surface (offset %.5f). NAMED candidate, "
        "NOT a declared seam (named-not-claimed %s): it needs the live respiratory volume and that volume's "
        "OWNED absolute airway-antigen scale [O]."
        % (b_oi, str(resp_ok).lower()),
        "[F]", "respiratory volume (future owner; DOI to-reconcile)", None)
    skin_card = vp_card("skin-candidate", "epidermal-barrier tolerance (live-verified §21)",
        "a skin volume localises the same switch to the epidermal barrier — the third barrier surface on "
        "the barrier-agnostic line (offset %.5f). Named here in v0.18.0; LIVE substrate-verified in §21 against "
        "integumentary_vp_site v1.0.0 (drift 0 + reciprocal immune-seam handshake %s). The identity stays "
        "immune-owned closed-form — the skin supplies the real barrier surface and owns the absolute "
        "epidermal-antigen scale [O], but defers the immune tolerance switch as an out-seam."
        % (b_oi, str(skin_ok).lower()),
        "[F]", "skin volume (integumentary_vp_site v1.0.0; DOI 10.5281/zenodo.20754541)", None)

    secs.append(dict(
        slug="19-barrier-surface-mucosal-immunity", N=19,
        title="Barrier-Surface Mucosal Immunity",
        descr="The gut tolerance latch generalises to any barrier surface: the offset from a surface's own "
              "antigen baseline is invariant at ±the spinodal, naming respiratory and skin barrier-immunity "
              "candidates while keeping the firewall and the byte-identical engine hash.",
        answer="The gut tolerance latch generalises. Across an antigen sweep the offset from a surface's own "
               "baseline is invariant at ±spinodal(1.0)=±%.5f, so the saddle-node is barrier-surface-agnostic. "
               "The gut (antigen %.2f) is the one verified point; respiratory (airway) and skin (epidermal) "
               "barriers are named candidates, each awaiting its live volume. Grade [F]."
               % (b_sp, b_ga),
        abstract="The seam layer now generalises the gut identity to other barrier surfaces under the same "
                 "2×sha256 (%s…), still importing ZERO sibling code. The gut saddle-node (induction = antigen + "
                 "spinodal, maintenance = antigen − spinodal) is shown barrier-surface-agnostic: across an "
                 "illustrative %d-point antigen sweep at g=1.0 the surface-independent offset is invariant at "
                 "+%.5f / −%.5f, so the gut (antigen %.2f → induction %.4f, maintenance %.4f) is the one vendored "
                 "point on a barrier-agnostic line. Respiratory (airway) and skin (epidermal) barriers are NAMED "
                 "candidates — each needs its live volume and owned absolute antigen scale [O], not claimed here. "
                 "Nothing feeds the hashed engine core."
                 % (seam_sha19[:8], sweep_n, b_oi, b_sp, b_ga, b_gi, b_gm),
        grade_token="[F]",
        cards=[barrier_card, resp_card, skin_card],
        body=f"""<h2>Generalising the gut identity to any barrier surface</h2>
<p>Chapter 16 established a closed-form identity at one barrier surface: the intestinal mucosal tolerance latch
that digestive's IBD module reads IS this volume's T23 saddle-node and T24 suppressor complement, on the
byte-identical R19 substrate. The induction threshold equals the luminal antigen plus the substrate spinodal,
and the maintenance threshold equals the antigen minus the spinodal. This chapter asks whether that identity is
specific to the gut or generic to barrier surfaces, and shows &mdash; in closed form &mdash; that it is
generic.</p>

<h2>The surface-independent offset is invariant</h2>
<p>Write the tolerance thresholds for an arbitrary barrier-surface antigen <em>a</em> at the shared mucosal R19
scale (&gamma;&nbsp;=&nbsp;1.0): induction&nbsp;=&nbsp;<em>a</em>&nbsp;+&nbsp;spinodal(1.0), and
maintenance&nbsp;=&nbsp;<em>a</em>&nbsp;&minus;&nbsp;spinodal(1.0). The quantity that does not depend on the
surface is the OFFSET from that surface's own antigen baseline: induction&nbsp;&minus;&nbsp;<em>a</em>&nbsp;=
&nbsp;+spinodal(1.0)&nbsp;=&nbsp;+{b_oi:.8f}, and maintenance&nbsp;&minus;&nbsp;<em>a</em>&nbsp;=&nbsp;&minus;
spinodal(1.0)&nbsp;=&nbsp;&minus;{b_sp:.8f}. Across an illustrative {sweep_n}-point antigen sweep
({b_sweep_str}) the offset is invariant to the eighth decimal &mdash; it never depends on <em>a</em>. That is
what barrier-surface agnosticism means: the tolerance switch behaves identically at every barrier surface; only
the surface's own antigen baseline differs. The gut is not a special case &mdash; it is the one point on this
line that happens to be vendored and live-verified (antigen {b_ga:.2f} &rarr; induction {b_gi:.4f}, maintenance
{b_gm:.4f}).</p>

<h2>Respiratory: a named airway-mucosa candidate</h2>
<p>A respiratory or lung VP volume would localise this volume's tolerance switch to the airway mucosa &mdash;
inhaled-antigen tolerance, with airway hypersensitivity as the airway reading of a broken latch. By
barrier-surface agnosticism the structural prediction is exact: the airway induction threshold would equal the
airway antigen plus spinodal(1.0), and the maintenance threshold the airway antigen minus spinodal(1.0) &mdash;
a shared-substrate identity exactly analogous to the gut seam, differing only in the surface-owned antigen
baseline. This is declared as a NAMED CANDIDATE, not a declared seam. The honest reason is the same discipline
that keeps the musculoskeletal marrow-niche identity a candidate: the respiratory volume is not on disk in this
session, so neither a vendored airway snapshot nor a live airway engine exists to verify the identity or to
supply the absolute airway-antigen scale. The immune-side tolerance primitive (T23/T24, barrier-surface-
agnostic) is real in this archive; the airway localisation and its absolute antigen scale are [O], owned by the
future respiratory volume.</p>

<h2>Skin: a named epidermal-barrier candidate</h2>
<p>A skin VP volume would localise the same switch to the epidermal barrier &mdash; contact tolerance, with
contact hypersensitivity as the skin reading of the same broken latch. The structural prediction is identical in
form: epidermal induction&nbsp;=&nbsp;epidermal antigen&nbsp;+&nbsp;spinodal(1.0),
maintenance&nbsp;=&nbsp;epidermal antigen&nbsp;&minus;&nbsp;spinodal(1.0). It too is a NAMED CANDIDATE for the
same reason &mdash; no live skin volume, no owned absolute epidermal-antigen scale on disk &mdash; and it rides
the same barrier-agnostic line as the gut and the airway. The immune volume owns the tolerance primitive; the
skin volume owns the epidermal localisation and its absolute antigen scale, [O] here.</p>

<h2>Why candidates and not seams, and what is owned elsewhere</h2>
<p>The program's discipline is that a shared-substrate identity is only claimed when it can be verified against
the live sibling engine, the way the gut identity is checked against digestive's live relapsing course. The
barrier-surface-agnosticism proof is owned and verified here &mdash; it rests on the measured T23 saddle-node
and T24 suppressor complement of this volume and is computed from this archive alone, with zero sibling imports.
What is NOT owned here is each real surface's absolute antigen scale: the airway aeroallergen load and airway
mucosal scale belong to the respiratory volume, the epidermal contact-antigen load and barrier scale to the
skin volume. Both are openly [O] with their owner named, exactly as the circulatory transport scale and the
bone-niche scale were in chapter 18. Each candidate carries a stated promotion path (add the volume to the live
harness, confirm substrate drift zero and that its barrier threshold reduces to barrier-antigen &plusmn; the
spinodal) and a stated falsifier (if the offset were not &plusmn;the spinodal across the antigen sweep,
barrier-surface agnosticism is dead and both candidates fall &mdash; the gut seam and its vendored
antigen-{b_ga:.2f} point survive, because they assert nothing about a surface that has not been built).</p>

<h2>What this is &mdash; and is not</h2>
<p>This chapter is architecture and bookkeeping, not new physics. It adds no measurement to the thirty-five
stress targets and changes no number in the engine; it proves one closed-form invariance and names two
structural candidates, stating honestly which is owned and verified (the barrier-agnostic offset), which is
named-not-claimed (the respiratory and skin identities), and what absolute scale is owned elsewhere and is
therefore [O]. The cross-package statements are direction-and-structure claims &mdash; direction/class only, not
medical advice, and not a validation of VP theory. The seam layer carries its own 2&times;sha256
({seam_sha19[:8]}&hellip;), separate from the engine emit() hash, which stays byte-identical.</p>""",
    ))
    # ------------------------------------------------------------------ v0.19.0 musculoskeletal LIVE verification (S20)
    mskv = NUM["seamv"]["musculoskeletal_marrow"]
    msk_hc = NUM["hcontract"]["musculoskeletal_pointer"]
    ri = msk_hc["retired_identity"]
    seam_sha20 = NUM["seam_sha"]; harness_sha20 = NUM["harness_sha"]
    root_sp20 = mskv["hematopoietic_root_spinodal_live"]          # 0.58538506 (RUNX1)
    niche_sp20 = mskv["msk_bone_spinodal_recomputed"]            # 0.53237264 (RUNX2)
    msk_gene20 = mskv["msk_bone_master_gene"]                    # RUNX2
    root_gene20 = mskv["hematopoietic_root_master_gene"]         # RUNX1
    niche_gamma20 = ri["msk_bone_gamma"]                         # 1.2414
    drift20 = mskv["msk_substrate_drift"]                        # 0.0
    gap20 = round(abs(root_sp20 - niche_sp20), 8)               # 0.05301242
    pointer_live20 = bool(mskv["pointer_live_verified"])
    retired20 = bool(mskv["identity_upgrade_retired_on_live_evidence"])
    IMM_DOI20 = "10.5281/zenodo.20755280"

    msk_live_card = vp_card("msk-live-verified", "marrow-niche pointer — LIVE-VERIFIED",
        "the §18 harness loaded musculoskeletal_vp_site v0.7.0 and measured cross-volume substrate drift = %.1f "
        "over γ∈{1.0, 1.3225, 1.4892}: the immune hematopoietic root (%s, spinodal %.8f) and the MSK bone-marrow "
        "niche share one byte-identical R19 substrate, so the one-way niche-housing pointer is LIVE-VERIFIED "
        "(pointer-live-verified %s)."
        % (drift20, root_gene20, root_sp20, str(pointer_live20).lower()),
        "[V]", "musculoskeletal volume (sibling, v0.7.0)", None)
    msk_retired_card = vp_card("msk-identity-retired", "identity candidate — RETIRED (honest negative)",
        "the MSK niche is built by osteoblasts (%s, γ=%.4f, spinodal %.8f), a DIFFERENT switch from the "
        "hematopoietic %s (γ=1.3225, spinodal %.8f) — %.8f ≠ %.8f, gap %.8f. The niche HOUSES hematopoiesis but "
        "is not the same R19 switch, so the threshold-equality identity does not reduce: falsifier fired, "
        "identity RETIRED (retired-on-live-evidence %s), pointer survives."
        % (msk_gene20, niche_gamma20, niche_sp20, root_gene20, root_sp20, niche_sp20, root_sp20, gap20,
           str(retired20).lower()),
        "[V]", "immune volume (owner)", "https://doi.org/" + IMM_DOI20)

    secs.append(dict(
        slug="20-musculoskeletal-seam-live-verified", N=20,
        title="Musculoskeletal Seam: Live-Verified, Identity Retired",
        descr="The musculoskeletal volume arrives and the marrow-niche pointer is tested live: substrate drift 0 "
              "confirms the pointer, while the shared-substrate-identity candidate is retired on live evidence — "
              "the niche is built by RUNX2, a different switch from the hematopoietic RUNX1.",
        answer="The musculoskeletal volume arrived, so the niche pointer was tested live. Substrate drift is 0 — "
               "the hematopoietic root and the MSK bone niche share one R19 substrate, so the pointer is "
               "live-verified. But the identity candidate is retired: the niche is built by RUNX2 (spinodal "
               "%.3f), not the hematopoietic RUNX1 (%.3f) — housing, not identity. An honest negative. Grade [V]."
               % (niche_sp20, root_sp20),
        abstract="The first live cross-package verification against a real sibling engine. With "
                 "musculoskeletal_vp_site v0.7.0 on disk, the §18 harness loads its engine and measures "
                 "cross-volume substrate drift = %.1f over γ∈{1.0, 1.3225, 1.4892} — the immune hematopoietic root "
                 "(%s) and the MSK bone-marrow niche sit on one byte-identical R19 substrate, so the one-way "
                 "niche-housing pointer is LIVE-VERIFIED. The named shared-substrate-identity upgrade is RETIRED "
                 "on live evidence: the MSK niche is built by osteoblasts (%s, γ=%.4f, spinodal %.8f), a different "
                 "master gene and spinodal from the hematopoietic %s (%.8f); the niche houses hematopoiesis but is "
                 "not the same switch (gap %.8f). The falsifier fired; nothing was tuned to rescue the identity; "
                 "the pointer survives. Engine hash byte-identical."
                 % (drift20, root_gene20, msk_gene20, niche_gamma20, niche_sp20, root_gene20, root_sp20, gap20),
        grade_token="[V]",
        cards=[msk_live_card, msk_retired_card],
        body=f"""<h2>The first live test against a real sibling</h2>
<p>Until now every sibling volume was absent and the live harness (chapter 17) SKIPped its cross-package checks;
the seam identities were verified only against this volume's own substrate and a vendored snapshot. This chapter
records the first time a sibling volume — musculoskeletal_vp_site v0.7.0 — was actually present, so the
chapter-18 marrow-niche pointer could be tested against the LIVE musculoskeletal engine. The result is reported
exactly as measured, including the part that did not go the way the named candidate hoped.</p>

<h2>The pointer is live-verified: substrate drift 0</h2>
<p>The harness loads the musculoskeletal engine by file path and compares its R19 spinodal
2(&gamma;/3)<sup>1.5</sup> and barrier &gamma;<sup>2</sup>/4 against this volume's, bit-for-bit, over
&gamma;&isin;{{1.0, 1.3225, 1.4892}}. The measured cross-volume drift is exactly {drift20:.1f} — the two volumes
share one byte-identical substrate. That is precisely what the one-way niche-housing pointer asserts: the immune
hematopoietic root (bone_marrow_hematopoiesis, {root_gene20}, spinodal {root_sp20:.8f}) and the musculoskeletal
bone-marrow niche sit on one substrate, so the statement &ldquo;the hematopoietic root is housed in the marrow
niche&rdquo; lands on a real organ in a real sibling, with no refit. The pointer is now LIVE-VERIFIED — upgraded
from &ldquo;verified against this volume's own substrate&rdquo; to &ldquo;verified against the live
musculoskeletal engine.&rdquo;</p>

<h2>The identity candidate is retired — an honest negative</h2>
<p>Chapter 18 named a stronger claim without asserting it: if the musculoskeletal niche read the same
{root_gene20} hematopoietic substrate, the niche's hematopoietic-commit threshold would equal {root_sp20:.8f} in
closed form — a shared-substrate identity like the gut seam. The live engine settles it. The musculoskeletal
volume models the bone-marrow niche through OSTEOBLASTS, whose master gene is {msk_gene20}
(&gamma;={niche_gamma20:.4f}, spinodal {niche_sp20:.8f}), not the hematopoietic switch {root_gene20}
(&gamma;=1.3225, spinodal {root_sp20:.8f}). {msk_gene20} and {root_gene20} are different master genes —
paralogues on different chromosomes — with different measured &gamma; and different spinodals
({niche_sp20:.8f}&nbsp;&ne;&nbsp;{root_sp20:.8f}, a gap of {gap20:.8f}). The musculoskeletal engine exposes no
marrow-niche hematopoietic-commit threshold at all, and its closest niche-building organ sits at a different
spinodal. So the niche HOUSES hematopoiesis but is not the same R19 switch: the threshold-equality identity does
not reduce. The falsifier stated in chapter 18 fired exactly as written, and the identity candidate is retired,
with nothing tuned to rescue it. The one-way pointer survives, because a pointer asserts only housing, not
equality.</p>

<h2>Why this is the right biological answer</h2>
<p>The retirement is not a defeat for the model; it is the model agreeing with the biology. The osteoblastic
bone-marrow niche supports haematopoietic stem cells but is a distinct cell type with a distinct master
regulator: the niche ({msk_gene20}) builds the compartment, the stem cells ({root_gene20}) live in it. A
housing-and-support relationship, not an identity, is exactly what the substrate verdict reports — different
switch, different spinodal, therefore a pointer and not an identity. A framework that had instead forced the
niche threshold onto the hematopoietic spinodal would have asserted an equality the biology does not support;
recording the honest negative keeps the cross-package map faithful and is the falsifiable discipline working as
intended.</p>

<h2>What this is &mdash; and is not</h2>
<p>This chapter adds one live verification and one retired claim; it adds no measurement to the thirty-five
stress targets and changes no number in the engine. The cross-package statement is a direction-and-structure
result &mdash; direction/class only, not medical advice, and not a validation of VP theory. The immune package
still reproduces alone: with the sibling absent the harness SKIPs cleanly and the immune-side contract is
byte-identical with or without it, and the engine emit() hash stays byte-identical. The seam layer and the
harness each carry their own 2&times;sha256 (seam {seam_sha20[:8]}&hellip;, harness {harness_sha20[:8]}&hellip;),
separate from the engine hash.</p>""",
    ))
    # ------------------------------------------------------------------ v0.20.0 integumentary LIVE verification (S21)
    skv = NUM["seamv"]["skin_candidate"]
    skhc = NUM["hcontract"]["barrier_surface_agnostic"]["skin_candidate"]
    surf21 = skhc["real_epidermal_barrier_surface"]
    seam_sha21 = NUM["seam_sha"]; harness_sha21 = NUM["harness_sha"]
    drift21 = skv["skin_substrate_drift"]                         # 0.0
    offset21 = skv["surface_independent_offset"]                  # 0.38490018
    epi_gene21 = surf21["epidermis_master_gene"]; epi_sp21 = surf21["epidermis_spinodal"]      # TP63, 0.61335644
    krt_gene21 = surf21["keratinocyte_master_gene"]; krt_sp21 = surf21["keratinocyte_spinodal"]  # KRT14, 0.69962471
    recip_id21 = skhc["reciprocal_seam_id"]                       # out__immune_hematologic__urticaria
    skin_doi21 = skhc["owner_doi_skin"].strip()                   # 10.5281/zenodo.20754541
    live21 = bool(skv["pointer_live_verified"]); recip21 = bool(skv["reciprocal_immune_seam_present"])
    eng_verified21 = bool(skv["identity_engine_verified"]); contra21 = bool(skv["identity_contradicted"])
    IMM_DOI21 = "10.5281/zenodo.20755280"

    skin_live_card = vp_card("skin-live-verified", "barrier-surface seam — LIVE substrate-verified + reciprocal handshake",
        "the §18 harness loaded integumentary_vp_site v1.0.0 and measured cross-volume substrate drift = %.1f over "
        "γ∈{1.0, 1.3225, 1.4892}: the epidermal barrier and the immune tolerance machinery share one byte-identical "
        "R19 substrate, the barrier surface is real (epidermis %s spinodal %.8f, keratinocyte %s spinodal %.8f), and "
        "the skin volume INDEPENDENTLY declares a reciprocal immune out-seam (%s) — pointer-live-verified %s, "
        "reciprocal-seam %s."
        % (drift21, epi_gene21, epi_sp21, krt_gene21, krt_sp21, recip_id21, str(live21).lower(), str(recip21).lower()),
        "[V]", "integumentary volume (sibling, v1.0.0)", "https://doi.org/" + skin_doi21)
    skin_identity_card = vp_card("skin-identity-closed-form", "epidermal-tolerance identity — immune-owned closed-form (not contradicted)",
        "the surface-independent offset is ±spinodal(1.0)=±%.8f; the skin supplies the real barrier surface but "
        "defers the immune tolerance switch as an out-seam, so the identity is CONFIRMED-REAL-SURFACE and NOT "
        "contradicted (identity-engine-verified %s, identity-contradicted %s) — a third outcome, between the gut "
        "(verified identity) and the marrow niche (retired identity)."
        % (offset21, str(eng_verified21).lower(), str(contra21).lower()),
        "[F]", "immune volume (owner)", "https://doi.org/" + IMM_DOI21)

    secs.append(dict(
        slug="21-integumentary-barrier-seam-live-verified", N=21,
        title="Integumentary Barrier Seam: Live-Verified, Identity Holds as Closed-Form",
        descr="The skin volume arrives and the epidermal barrier seam is tested live: substrate drift 0 confirms a "
              "real epidermal barrier on the shared substrate, the skin volume reciprocally declares an immune "
              "out-seam, and the epidermal-tolerance identity stays immune-owned closed-form — neither engine-"
              "verified nor contradicted.",
        answer="The skin volume arrived, so the epidermal barrier seam was tested live. Substrate drift is 0, the "
               "epidermal barrier is real (%s, %s), and the skin volume independently declares an immune out-seam — "
               "a reciprocal handshake. The epidermal-tolerance identity stays immune-owned closed-form: "
               "confirmed-real-surface, not contradicted, but not engine-verified, since the skin defers immune "
               "tolerance. Grade [V]." % (epi_gene21, krt_gene21),
        abstract="The second live cross-package verification against a real sibling — and a third distinct outcome. "
                 "With integumentary_vp_site v1.0.0 (concept DOI %s) on disk, the §18 harness measures cross-volume "
                 "substrate drift = %.1f: the epidermal barrier and the immune tolerance machinery share one "
                 "byte-identical R19 substrate, and the barrier surface the candidate posited is real (epidermis "
                 "%s, keratinocyte %s). The skin volume independently declares a reciprocal immune out-seam (%s) — a "
                 "bidirectional handshake. But the skin volume models the barrier structure and defers the immune "
                 "tolerance switch as an out-seam, so the epidermal-tolerance identity (induction = epidermal-antigen "
                 "+ spinodal(1.0)) remains immune-owned closed-form: confirmed-real-surface, not contradicted, not "
                 "engine-verified. Between the gut (verified identity) and the marrow niche (retired identity), the "
                 "skin is the honest middle. Engine hash byte-identical."
                 % (skin_doi21, drift21, epi_gene21, krt_gene21, recip_id21),
        grade_token="[V]",
        cards=[skin_live_card, skin_identity_card],
        body=f"""<h2>The second live test — and a third kind of answer</h2>
<p>The marrow-niche seam (chapter 20) retired its identity; the gut seam (chapter 16) verified one. The skin
barrier seam lands between them. With integumentary_vp_site v1.0.0 on disk, the chapter-18/19 epidermal barrier
candidate could be tested against the live skin engine — and the result is neither a clean promotion nor a
retirement, but an honestly partial outcome, reported exactly as measured.</p>

<h2>The barrier surface is real and shares the substrate: drift 0</h2>
<p>The harness loads the skin engine and compares its R19 spinodal 2(&gamma;/3)<sup>1.5</sup> and barrier
&gamma;<sup>2</sup>/4 against this volume's, bit-for-bit, over &gamma;&isin;{{1.0, 1.3225, 1.4892}}. The drift is
exactly {drift21:.1f} — the epidermal barrier and the immune tolerance machinery sit on one byte-identical
substrate. The barrier surface the v0.18.0 candidate posited is real: the skin volume builds the epidermis
({epi_gene21}, spinodal {epi_sp21:.8f}) and the keratinocyte barrier ({krt_gene21}, spinodal {krt_sp21:.8f}) on
that shared substrate. So there genuinely is an epidermal barrier surface for the immune tolerance switch to
localise to.</p>

<h2>A reciprocal handshake: the skin volume declares an immune seam back</h2>
<p>The immune package declared a skin barrier-immunity candidate (immune&rarr;skin) in v0.18.0. The skin volume,
written independently, declares an immune out-seam in the other direction: its own seam manifest carries
<code>{recip_id21}</code>, a contract to immune_hematologic for the mast-cell / histamine effector (urticaria /
angioedema). Both volumes recognise the same barrier&harr;immune adjacency from opposite sides, with no
coordination — a bidirectional cross-reference that can now be closed. (The skin emphasises the mast-cell
effector; the immune-side candidate emphasises epidermal tolerance — related immune functions at the same barrier
surface.)</p>

<h2>The identity stays immune-owned closed-form — not verified, not contradicted</h2>
<p>The stronger claim was a shared-substrate identity: that the skin's epidermal tolerance threshold equals
epidermal-antigen + spinodal(1.0) in closed form, the offset invariant at &plusmn;{offset21:.8f}. The live engine
neither confirms nor denies it, for a clean reason: the skin volume does not implement an immune tolerance switch
at all. It models the barrier structure, physical and thermal insult tolerance, pigment, appendages, and —
notably — autoantibody-driven adhesion saddle-nodes (pemphigus and pemphigoid, where an antibody drives a
desmosomal or hemidesmosomal bond below its spinodal, with hysteresis). That last is the same R19 saddle-node
formalism applied to a different compartment, driven by an immune effector from outside. But the immune tolerance
decision itself the skin names as an un-modelled out-seam. So there is no epidermal tolerance threshold in the
skin engine to equate. The identity therefore remains the immune-owned closed-form result of barrier-surface
agnosticism — now with a confirmed real surface and a reciprocal seam, neither over-claimed as engine-verified nor
retired. The absolute epidermal-antigen scale stays skin-owned [O].</p>

<h2>Why three different outcomes is the discipline working</h2>
<p>Three sibling volumes have now been tested live, and they gave three different answers: the gut identity
verified (the digestive course reproduces the saddle-node), the marrow-niche identity retired (the niche is built
by a different switch), and the skin identity stands as immune-owned closed-form (the barrier surface is real and
reciprocally recognised, but the tolerance switch is immune-owned). A framework that returned the same verdict
every time would be asserting, not testing. Recording each outcome as it actually came back — verified, retired,
or closed-form-not-contradicted — is what keeps the cross-package map faithful.</p>

<h2>What this is &mdash; and is not</h2>
<p>This chapter adds one live verification and one reciprocal-seam handshake; it adds no measurement to the
thirty-five stress targets and changes no number in the engine. The cross-package statement is a
direction-and-structure result &mdash; direction/class only, not medical advice, and not a validation of VP
theory. The immune package still reproduces alone: with the sibling absent the harness SKIPs cleanly and the
immune-side contract is byte-identical with or without it, and the engine emit() hash stays byte-identical. The
seam layer and the harness each carry their own 2&times;sha256 (seam {seam_sha21[:8]}&hellip;, harness
{harness_sha21[:8]}&hellip;), separate from the engine hash.</p>""",
    ))
    return secs


# --------------------------------------------------------------------------------------------------
# hub + sidecars
# --------------------------------------------------------------------------------------------------
def hub_html(secs, NUM):
    items = "\n".join(
        '  <li><a href="/%s/%s/">§%d %s</a> — <span class="grade %s">%s</span><br><span class="one">%s</span></li>'
        % (PAPER_ID, s["slug"], s["N"], esc(s["title"]), GRADE_CLASS.get(s["grade_token"], "g-open"),
           esc(s["grade_token"]), esc(s["one"]))
        for s in secs)
    ld = {"@context": "https://schema.org", "@type": "CreativeWorkSeries", "name": FULLTITLE,
          "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
          "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI},
          "sameAs": DOI_URL,
          "license": CCBY, "url": BASE + "/"}
    order = " → ".join(NUM["order"])
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full} | Jamming Physics</title>
<meta name="description" content="Immune and haematologic organs as a population of R19 bistable switches: clonal selection, inflammation hysteresis, lineage order, memory, immunosurveillance, carcinogenesis, and four fundamental treatment levers.">
<link rel="canonical" href="{base}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › {short}</nav></header>
<main>
<h1>{full}</h1>
<p class="answer">This volume emerges the thymus, spleen, bone-marrow haematopoiesis, and adaptive lymphoid
tissue from one measured parameter γ as a population of R19 bistable switches, then derives clonal selection,
inflammation, lineage order, memory, immunosurveillance, carcinogenesis, and four fundamental treatment
levers. Developmental order (ascending γ): {order}. Research phase; concept DOI {doi}.</p>
<p class="abstract">All quantities are forced or measured under the no-tuning discipline; grades are honest
([V] verified, [L] measured/cited, [O] open with a stated obstacle). The four master-gene γ are byte-exact
verified against the NCBI reference assembly (GRCh38.p14). Numbers are reproduced deterministically
by <code>repro/run_all.py</code>.</p>
<ul class="toc">
{items}
</ul>
</main>
<footer>{author} · <a href="{orcid}" rel="noopener">ORCID</a> · <a href="{doi_url}" rel="noopener">DOI: {doi}</a> · <a href="{ccby}" rel="noopener">CC BY 4.0</a></footer>
</body>
</html>
""".format(full=esc(FULLTITLE), base=BASE, short=esc(SHORT), ld=json.dumps(ld, ensure_ascii=False),
           order=esc(order), items=items, author=esc(AUTHOR), orcid=ORCID, ccby=CCBY,
           doi=esc(DOI), doi_url=DOI_URL)


def robots_txt():
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    lines = []
    for b in bots:
        lines.append("User-agent: %s" % b)
        lines.append("Allow: /")
        lines.append("")
    lines.append("Sitemap: %s/sitemap.xml" % BASE)
    return "\n".join(lines) + "\n"


def sitemap_xml(secs):
    urls = [BASE + "/"] + ["%s/%s/" % (BASE, s["slug"]) for s in secs]
    body = "\n".join("  <url><loc>%s</loc></url>" % u for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n")


def llms_txt(secs, NUM):
    order = " → ".join(NUM["order"])
    head = ("# %s\n\n"
            "> Immune and haematologic organs (thymus, spleen, bone-marrow haematopoiesis, adaptive lymphoid)\n"
            "> emerge from one measured promoter-stacking parameter γ as a population of R19 bistable switches.\n"
            "> Clonal selection is a saddle-node crossing at the spinodal; inflammation is bistable hysteresis;\n"
            "> developmental order is an ascending-γ readout (%s); memory is barrier-protected persistence;\n"
            "> immunosurveillance is a multiplicative cross-cutting seam; carcinogenesis is a convex Kramers\n"
            "> dose-response; and four fundamental treatment levers (basin re-flip, barrier restoration, drive\n"
            "> removal, surveillance restoration) follow from the attractor landscape, explaining why\n"
            "> cytotoxic-only therapy relapses. No-tuning discipline; honest [V]/[L]/[O] grades; concept DOI 10.5281/zenodo.20755280.\n\n"
            % (FULLTITLE, order))
    core = "## core\n" + "\n".join("- [§%d %s](%s/%s/)" % (s["N"], s["title"], BASE, s["slug"]) for s in secs[:5])
    research = ("\n\n## research\n- [§6 Carcinogen dose–response (Kramers)](%s/%s/)\n- [§7 Fundamental treatment levers](%s/%s/)"
                % (BASE, secs[5]["slug"], BASE, secs[6]["slug"]))
    concepts = ("\n\n## concepts\n- γ = −mean SantaLucia-1998 NN stacking ΔG37 (DNA-volume SSOT); the four "
                "master-gene promoter windows are byte-exact verified against NCBI GRCh38.p14 (sha256), "
                "γ recomputed identical; gene→organ master corroborated by NCBI-Gene RefSeq\n"
                "- spinodal |h| = 2(γ/3)^1.5 (discontinuous flip threshold)\n"
                "- barrier = γ²/4 (state stability; Kramers rate)\n")
    policies = ("\n## policies\n- License CC BY 4.0; author ORCID 0009-0002-7535-8245; reproduction: "
                "repro/run_all.py; γ provenance audit: inherited/ncbi_verify.py (offline gate + online re-verify)\n")
    return head + core + research + concepts + policies


def meta_json(secs, NUM):
    ver = NUM["ncbi_ver"]
    return {
        "paper_id": PAPER_ID, "code": CODE, "title": FULLTITLE,
        "author": AUTHOR, "orcid": ORCID, "license": CCBY,
        "doi": DOI, "doi_url": DOI_URL, "phase": "writing", "version": open(os.path.join(_PKG, "VERSION")).read().strip(),
        "developmental_order_ascending_gamma": NUM["order"],
        "gammas": {k: round(v, 6) for k, v in sorted(NUM["G"].items())},
        "gamma_provenance": {
            "method": "−mean SantaLucia-1998 NN stacking ΔG37 over TSS−2000..+500 (2501 bp)",
            "primary_source": ver.get("_database"), "assembly": ver.get("_assembly"),
            "verified_on": ver.get("_verified_on"), "all_four_byte_exact": ver.get("_all_four_verified"),
            "per_gene": {sym: {"accession": v["accession"], "map": NUM["ncbi_ref"]["genes"][sym]["map_location"],
                               "gamma": v["live_gamma"], "byte_exact_vs_live_ncbi": v["sha256_match"]}
                         for sym, v in ver["genes"].items()},
            "audit": "inherited/ncbi_verify.py OFFLINE_check() (offline gate) / ONLINE_reverify() (live)"},
        "chapters": [{"position": s["N"], "slug": s["slug"], "title": s["title"],
                      "one_liner": s["one"], "grade": s["grade_token"]} for s in secs],
        "reproduction": "python repro/run_all.py  (deterministic, 2×sha256 identical)",
    }


SITE_CSS = """:root{--ink:#15202b;--mut:#5b6b7a;--line:#dfe6ee;--bg:#fff;--card:#f6f9fc;--acc:#0b6;--accF:#06c;--accO:#b60}
*{box-sizing:border-box}body{margin:0;font:16px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
main{max-width:760px;margin:0 auto;padding:1.4rem 1.1rem 3rem}header,footer{max-width:760px;margin:0 auto;padding:.8rem 1.1rem;color:var(--mut);font-size:.86rem}
footer{border-top:1px solid var(--line);margin-top:2rem}.crumb a{color:var(--accF);text-decoration:none}
h1{font-size:1.7rem;line-height:1.25;margin:.2rem 0 1rem}h2{font-size:1.18rem;margin:1.8rem 0 .5rem}
p{margin:.6rem 0}.answer{font-size:1.06rem;background:var(--card);border-left:3px solid var(--acc);padding:.8rem 1rem;border-radius:0 6px 6px 0}
.abstract{color:#26323d}.claim-strip{display:flex;flex-wrap:wrap;gap:.5rem .9rem;align-items:center;font-size:.8rem;margin:1rem 0;padding:.5rem .7rem;background:var(--card);border:1px solid var(--line);border-radius:6px}
.claim-strip a{color:var(--accF);text-decoration:none}.grade{font-weight:700;padding:.05rem .4rem;border-radius:4px;color:#fff}
.g-forced{background:var(--accF)}.g-verified{background:var(--acc)}.g-open{background:var(--accO)}.g-hypothesis{background:#789}
.gate{color:var(--mut)}.doi a{color:var(--accF);text-decoration:none}.doi a:hover{text-decoration:underline}
.vp-card{background:#fbfdff;border:1px solid var(--line);border-left:3px solid var(--accF);padding:.6rem .8rem;border-radius:0 6px 6px 0;margin:.8rem 0;font-size:.92rem}
.vp-card a{color:var(--accF);text-decoration:none}.pn{display:flex;justify-content:space-between;gap:1rem;margin-top:2.2rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.92rem}
.pn a{color:var(--accF);text-decoration:none}.toc{list-style:none;padding:0}.toc li{padding:.7rem 0;border-bottom:1px solid var(--line)}
.toc a{color:var(--accF);text-decoration:none;font-weight:600}.one{color:var(--mut);font-size:.9rem}code{background:var(--card);padding:.1rem .3rem;border-radius:4px;font-size:.9em}
table.prov{border-collapse:collapse;width:100%;font-size:.88rem;margin:.8rem 0}table.prov th,table.prov td{border:1px solid var(--line);padding:.4rem .55rem;text-align:left}table.prov thead th{background:var(--card);font-weight:700}
.fineprint{color:var(--mut);font-size:.84rem}
"""


def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Sign off research first: gates.write_research_complete(); echo writing > PHASE")
        return 1

    NUM = numbers()
    secs = build_sections(NUM)
    # attach one-liners
    one_liners = {
        1: "Clonal selection = measured saddle-node at the spinodal; immunodominance, repertoire dominance, affinity maturation and antigenic imprinting all emerge from clonal competition.",
        2: "Acute inflammation resolves, chronic latches: bistable hysteresis, loop width 2×spinodal.",
        3: "Developmental order is an ascending-γ readout; endpoints match embryology.",
        4: "Memory = barrier-protected persistence; erase drive = spinodal; stability ranks by γ²/4.",
        5: "Surveillance is a multiplicative cross-cutting seam: burden = crossing-rate × escape.",
        6: "Carcinogens lower the barrier → convex Kramers dose–response diverging at the spinodal.",
        7: "Four levers from the attractor landscape, all measured as trajectories; cytotoxic relapse is an explicit regrowth curve, and a cull + basin lever converts relapse into cure.",
        8: "The disease/treatment axis: across six immune diseases, basin-acting cures (re-tolerization, induction, reconstitution, latch-break) are the durable class while drive-suppression-only relapses on withdrawal — one verdict, six self-contained pages. Direction/class only — not medical advice.",
        9: "Autoimmunity is the R19 switch latched past the spinodal; a transient re-tolerization pulse cures durably, while sub-critical suppression only contains it and refills on withdrawal. Direction/class only — not medical advice.",
        10: "Transplant tolerance is a negative saddle-node crossing: deep transient induction gives durable off-therapy tolerance, indefinite immunosuppression only contains rejection and relapses; the induction window closes as the alloresponse consolidates. Direction/class only — not medical advice.",
        11: "Allergy is failed immune ignorance: a sub-threshold dose repeated sensitizes (N_crit falls as dose rises) and latches, while a controlled below-crossover protocol raises the threshold and desensitizes; an over-aggressive protocol sensitizes instead. Direction/class only — not medical advice.",
        12: "Immunodeficiency is the collapse of one surveillance lever driving both opportunistic infection and immune escape; reconstitution is threshold-gated, so partial restoration below the coverage threshold is not a partial cure. Direction/class only — not medical advice.",
        13: "Autoimmune cytopenia is the attack read out on a blood count: re-tolerization restores output durably while suppression lets it re-collapse, and lineage support sets only the rate, not the destination. Direction/class only — not medical advice.",
        14: "Systemic inflammation past a critical insult is a self-sustaining cytokine latch holding itself ON after the trigger clears; it must be actively broken and the break is time-critical, with the coupling-off control flat. Direction/class only — not medical advice.",
        15: "Immune time on one substrate: thymic involution makes the repertoire drift (autoreactive escape rises, naive export falls) as the education window shrinks; and under a fixed booster budget the durable re-boost interval emerges at the measured memory half-life — too frequent wastes it, too spaced opens gaps. Direction/class only — not medical advice.",
        16: "The immune volume is a hub: three seams on one byte-identical substrate wire it to its siblings — digestive's IBD mucosal latch IS this volume's T23 saddle-node and T24 suppressor complement, mind's HPA cortisol raises T24 suppression (sign only) while cytokine tone points one-way to mind's inflammatory mood contributor, and immune-escape multiplies every cancer kernel — with zero sibling imports. Direction/class only — not medical advice.",
        17: "The seam layer takes the sibling identities on trust; an out-of-gate harness verifies them live — cross-volume substrate drift exactly 0, digestive's live IBD course reproducing this volume's T23/T24 thresholds, and mind's depression module carrying the HPA and inflammatory endpoints — while its digest hashes only the immune-side contract, byte-identical with or without siblings.",
        18: "Two inherited adjacencies become declared one-way-pointer spokes: leukocyte effector populations (rooted at bone-marrow haematopoiesis, RUNX1) traffic into the circulatory vasculature, and the same haematopoietic root is housed in the musculoskeletal marrow niche — both consume no sibling value, the firewall and the byte-identical engine hash hold, and the niche's shared-substrate-identity upgrade is named here as a candidate (subsequently live-verified and retired in §20).",
        19: "The gut tolerance latch is barrier-surface-agnostic: across an antigen sweep the offset from a surface's own baseline is invariant at ±the spinodal(1.0), so the saddle-node identity generalises to any barrier surface (the gut is the one vendored point on the line). Respiratory (airway) is a named candidate; skin (epidermal) was LIVE substrate-verified in §21 against integumentary_vp_site v1.0.0 (drift 0 + reciprocal immune-seam handshake), with the identity staying immune-owned closed-form. Firewall and byte-identical engine hash kept. Direction/class only — not medical advice.",
        20: "The first live cross-package verification against a real sibling engine: with musculoskeletal_vp_site v0.7.0 present, cross-volume substrate drift is exactly 0 — so the marrow-niche pointer is LIVE-VERIFIED (the hematopoietic root and the MSK bone niche share one R19 substrate) — while the shared-substrate-identity candidate is RETIRED on live evidence: the niche is built by RUNX2 (spinodal 0.532), a different switch from the hematopoietic RUNX1 (0.585), so it houses hematopoiesis but is not the same switch (falsifier fired, pointer survives). An honest negative. Direction/class only — not medical advice.",
        21: "The second live cross-package verification, and a third distinct outcome: with integumentary_vp_site v1.0.0 present, substrate drift is 0 (the epidermal barrier and immune tolerance share one R19 substrate, the barrier surface real — TP63/KRT14), and the skin volume independently declares a reciprocal immune out-seam (a bidirectional handshake). The epidermal-tolerance identity stays immune-owned closed-form — confirmed-real-surface, not contradicted, but not engine-verified, since the skin defers the immune tolerance switch as an out-seam. Between the gut (verified) and the marrow niche (retired), the honest middle. Direction/class only — not medical advice.",
    }
    for s in secs:
        s["one"] = one_liners[s["N"]]

    os.makedirs(_DOCS, exist_ok=True)
    os.makedirs(os.path.join(_DOCS, "assets", "css"), exist_ok=True)
    open(os.path.join(_DOCS, "assets", "css", "site.css"), "w", encoding="utf-8").write(SITE_CSS)

    n_total = len(secs)
    for i, s in enumerate(secs):
        prev_ = (secs[i - 1]["slug"],) if i > 0 else None
        next_ = (secs[i + 1]["slug"],) if i < n_total - 1 else None
        d = os.path.join(_DOCS, s["slug"])
        os.makedirs(d, exist_ok=True)
        h = page(s["slug"], s["N"], s["title"], s["descr"], s["answer"], s["abstract"],
                 s["grade_token"], s["body"], s["cards"], prev_, next_, n_total)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(h)

    open(os.path.join(_DOCS, "index.html"), "w", encoding="utf-8").write(hub_html(secs, NUM))
    open(os.path.join(_DOCS, "robots.txt"), "w", encoding="utf-8").write(robots_txt())
    open(os.path.join(_DOCS, "sitemap.xml"), "w", encoding="utf-8").write(sitemap_xml(secs))
    open(os.path.join(_DOCS, "llms.txt"), "w", encoding="utf-8").write(llms_txt(secs, NUM))
    json.dump(meta_json(secs, NUM), open(os.path.join(_DOCS, "_meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    pages = n_total + 1
    print("BUILT %d HTML pages (hub + %d chapters) + sitemap/robots/llms/_meta/css into docs/." % (pages, n_total))
    print("Canonical base:", BASE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
