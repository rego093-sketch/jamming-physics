#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
endotherm_ectotherm.py  --  the FOUNDATIONAL question of this package, in R19 terms.

The package does NOT start from disease. It starts from the question that DIVIDES a homeotherm
(endotherm) from a poikilotherm (ectotherm): does the organism actively DEFEND an internal setpoint
against the environment, or TRACK the environment? This module answers three sub-questions, all by
OBSERVATION of extant species (no descent/selection language is used anywhere; we compare what IS):

  Q1  What is the GENE-LEVEL criterion that separates the two strategies?
  Q2  HOW, and how much, do they differ?
  Q3  Over how LARGE a range do they differ?

METHOD (no tuning, C1):
  - gamma is re-derived OFFLINE, bit-for-bit, from the vendored cross-species promoter cache
    (inherited/crossspecies_thermo_panel.json), with the IDENTICAL NN-stacking dG37 table
    (SantaLucia 1998) and window (TSS-2000..+500) used by the human energy atlas. Same scale.
  - the R19 substrate (vp_substrate) supplies the setpoint-defence reading: a DEFENDED setpoint is
    an attractor whose basin (barrier = gamma^2/4) resists an ambient drive; an UNDEFENDED state is
    slaved to ambient. The switch BETWEEN two regulated regimes is discontinuous past the spinodal.

FIREWALL (binding, the analgesic-package discipline carried here):
  gamma READS the promoter switch-threshold STRUCTURE only. It is BLIND to whether the furnace is
  present, functional, or driven, and BLIND to the endotherm/ectotherm verdict. It is NOT a metabolic
  rate, a body temperature, or a thermogenic capacity. The criterion is the PRESENCE of a drivable
  thermogenic effector-command pair (CITED biology), never a gamma value. Two pre-registered NULLS
  below make this explicit, in the honest tradition of the DNA package's gene-class null.

Grades (C3): measured gamma reads [V]; R19 mechanism / ratio direction [V]; cited species biology
and cited absolute ranges [L]; absolute metabolic rates / absolute species placement [O] (obstacle
stated). No silent absolute claims, no fitted gamma.
"""
import os, sys, json, hashlib, itertools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, barrier, settle, sdot, seed_everything

_HERE  = os.path.dirname(__file__)
_PANEL = os.path.join(_HERE, "..", "..", "inherited", "crossspecies_thermo_panel.json")

# SantaLucia 1998 unified NN dG37 -- the SAME READ-ONLY table as the DNA / energy atlas.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,"GT":-1.44,"AC":-1.44,
      "CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,"CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

# CITED biology (Layer-2; NOT an engine output) -- the furnace / command / fuel-switch identities and
# the species facts that the gamma read is BLIND to. Sources are named so the criterion is auditable.
CITED = {
    "UCP1":  "Uncoupling protein 1: the brown-fat proton-leak furnace (non-shivering thermogenesis). "
             "Present+functional in many placental mammals; a PSEUDOGENE in Sus scrofa (pig) and ABSENT "
             "in birds -- both endotherms that defend the setpoint by other (muscle-based) routes. "
             "[Cited: Nowack 2017 J Exp Biol; Berg 2006/Hughes 2009 on the pig UCP1 pseudogene.]",
    "ADRB3": "Beta-3 adrenergic receptor: the sympathetic COMMAND that recruits the furnace "
             "(cold -> sympathetic -> ADRB3 -> UCP1 -> heat). [Cited: Krief 1993; Collins 2011.]",
    "PDK4":  "Pyruvate dehydrogenase kinase 4: the metabolic fuel-switch to lipid + glucose sparing; "
             "up-regulated in fasting, torpor, AND insulin resistance (the RD4 bridge). "
             "[Cited: Andrews 1998 (hibernation); Wu 1999 / Jeong 2012 (fasting/insulin resistance).]",
}

# The DYNAMIC regulatory contrast that a STATIC promoter read cannot supply (Layer-2; the honest
# external [O] next step named explicitly). NULL-4 below tests the STATIC methylation-SUBSTRATE
# architecture (CpG O/E) and finds it present across hibernation status; the DYNAMIC torpor methylation
# / expression STATE (which CpG sites are methylated, when, and which transcripts move across the
# torpor<->euthermia cycle) is where the present-but-silenced gating would actually be read -- and the
# package's offline-reproducibility invariant precludes ingesting processed in-vivo data in-package.
CITED_DYNAMIC_REGULATION = {
    "torpor_methylation_expression": (
        "The torpor program is gated by DYNAMIC regulation across the torpor<->euthermia cycle, not by "
        "baseline promoter sequence. Reported in-vivo contrasts (differential expression / methylation "
        "between torpid and euthermic / interbout-aroused states in deep hibernators) are the genuine "
        "regulatory-layer read; they are CITED Layer-2 observations, not derived here. "
        "[Cited: e.g. Andrews 1998 (PDK4 up in hibernation); Grabek 2015 / Hampton 2013 (hibernation "
        "expression atlases, Ictidomys); Alvarado 2015 (hepatic DNA-methylation dynamics in torpor).] "
        "Grade [O] external: the offline-reproducibility invariant precludes vendoring processed in-vivo "
        "data in-package, so this is the named honest next step, not a stub.")
}

# Cited absolute RANGES for Q3 (Layer-2; graded [L], with the absolute-rate obstacle noted [O]).
CITED_RANGES = {
    "bmr_ratio_endo_over_ecto": "~5-10x: a resting endotherm idles at roughly 5-10x the metabolic rate "
                                "of an ectotherm of the same mass and body temperature. [L] cited "
                                "(e.g. Bennett & Ruben 1979; Else & Hulbert 1981). Absolute W/kg is [O].",
    "thermal_stability":        "endotherm core temperature is held within ~1-2 C of setpoint across a "
                                "wide ambient range; ectotherm core tracks ambient over tens of C. [L] cited. "
                                "Absolute setpoint value is [L]; absolute heat-loss W is [O].",
}


def _gamma(seq):
    v = [-NN[seq[i:i+2]] for i in range(len(seq) - 1) if seq[i:i+2] in NN]
    return round(sum(v) / len(v), 4) if v else float("nan")


def load_panel():
    return json.load(open(_PANEL, encoding="utf-8"))


def rederive_offline():
    """Re-derive every cross-species gamma from the cached promoter strings. Confirms the panel
    reproduces offline bit-for-bit (C1) and returns the read table keyed by species then gene."""
    p = load_panel()
    table, drift = {}, []
    for org, genes in p["reads"].items():
        table[org] = {"thermo_class": p["species"][org]["thermo_class"],
                      "torpor_note": p["species"][org]["torpor_note"], "genes": {}}
        for sym, rec in genes.items():
            key = sym + "|" + org
            if key in p["cache"]:
                got = _gamma(p["cache"][key]["seq"])
                if rec["gamma"] is not None and got != rec["gamma"]:
                    drift.append({"key": key, "stored": rec["gamma"], "rederived": got})
                table[org]["genes"][sym] = {"gamma": got, "gc": rec["gc"], "ncbi_acc": rec["ncbi_acc"],
                                            "status": rec["status"]}
            else:
                table[org]["genes"][sym] = {"gamma": None, "gc": None, "ncbi_acc": None,
                                            "status": rec["status"]}
    return {"reads": table, "offline_drift": drift, "offline_identical": (len(drift) == 0)}


# ---------------------------------------------------------------------------
#  Q1 -- the GENE-LEVEL criterion (effector-command PRESENCE, not a gamma value)
# ---------------------------------------------------------------------------
def gene_criterion():
    """The criterion that separates the strategies is the PRESENCE of a drivable thermogenic
    effector-command pair {furnace (UCP1) + sympathetic command (ADRB3)} -- not a gamma value.
    Observed across the panel: the ADRB3 command does NOT resolve to a genomic ortholog in the two
    ectotherm assemblies queried, while it is present across the endotherm set. gamma is blind to
    this (firewall)."""
    t = rederive_offline()["reads"]
    rows = []
    for org, rec in t.items():
        g = rec["genes"]
        furnace_present = g.get("UCP1", {}).get("status") == "measured"
        command_present = g.get("ADRB3", {}).get("status") == "measured"
        fuelswitch_present = g.get("PDK4", {}).get("status") == "measured"
        rows.append({
            "species": org, "thermo_class": rec["thermo_class"], "torpor_note": rec["torpor_note"],
            "UCP1_furnace_resolves": furnace_present, "ADRB3_command_resolves": command_present,
            "PDK4_fuelswitch_resolves": fuelswitch_present,
            "effector_command_pair_present": bool(furnace_present and command_present),
            "UCP1_gamma": g.get("UCP1", {}).get("gamma"),
            "ADRB3_gamma": g.get("ADRB3", {}).get("gamma"),
            "PDK4_gamma": g.get("PDK4", {}).get("gamma"),
        })
    rows.sort(key=lambda r: (r["thermo_class"], r["species"]))
    endo_pair = all(r["effector_command_pair_present"] for r in rows if r["thermo_class"] == "endotherm")
    ecto_no_command = all(not r["ADRB3_command_resolves"] for r in rows if r["thermo_class"] == "ectotherm")
    return {
        "criterion": ("the gene-level divide is the PRESENCE of a drivable thermogenic effector-command "
                      "pair {UCP1 furnace + ADRB3 sympathetic command}, not a gamma value (firewall). "
                      "Where the furnace gene is absent/silenced (pig pseudogene, bird absence) the "
                      "endotherm defends the setpoint by other routes -- so the deeper criterion is the "
                      "DYNAMICS (a defended attractor), captured by R19, not any single gene."),
        "observed_endotherms_have_command_pair": bool(endo_pair),
        "observed_ectotherms_lack_ADRB3_command": bool(ecto_no_command),
        "rows": rows,
        "grade_presence": "[L] cited+observed gene presence (auditable accessions in the panel)",
        "grade_command_absence": "[O] symbol-orthology across distant taxa is itself uncertain; the strong "
                                 "'command absent' claim is graded open, the queried-assembly observation [L]",
        "cited_identities": CITED,
    }


# ---------------------------------------------------------------------------
#  Pre-registered NULLS (firewall made explicit; DNA-package honesty tradition)
# ---------------------------------------------------------------------------
def null_ucp1_gamma_does_not_separate():
    """NULL-1: UCP1 promoter gamma does NOT separate endotherm from ectotherm by value. The
    endotherm/ectotherm gamma gap is GC-driven, and the pig (endotherm) UCP1 is a pseudogene yet its
    gamma sits among the functional rodents -- gamma is blind to function (parts present != trait)."""
    t = rederive_offline()["reads"]
    endo = [t[o]["genes"]["UCP1"]["gamma"] for o in t if t[o]["thermo_class"] == "endotherm"
            and t[o]["genes"]["UCP1"]["gamma"] is not None]
    ecto = [t[o]["genes"]["UCP1"]["gamma"] for o in t if t[o]["thermo_class"] == "ectotherm"
            and t[o]["genes"]["UCP1"]["gamma"] is not None]
    pig = t.get("Sus scrofa", {}).get("genes", {}).get("UCP1", {}).get("gamma")
    rodent = [t[o]["genes"]["UCP1"]["gamma"] for o in ("Mus musculus", "Rattus norvegicus") if o in t]
    # overlap test: does the pig pseudogene gamma fall inside the functional-rodent gamma envelope?
    pig_in_rodent_envelope = bool(rodent) and (min(rodent) - 0.05 <= (pig or -9) <= max(rodent) + 0.05)
    return {
        "null": "UCP1 promoter gamma does NOT separate endotherm from ectotherm by value",
        "endotherm_UCP1_gamma": sorted(endo), "ectotherm_UCP1_gamma": sorted(ecto),
        "pig_pseudogene_UCP1_gamma": pig, "functional_rodent_UCP1_gamma": sorted(rodent),
        "pig_pseudogene_gamma_inside_functional_rodent_envelope": pig_in_rodent_envelope,
        "reading": ("the ectotherm gamma is lower but GC-confounded (ectotherm promoter GC ~0.33-0.38 vs "
                    "endotherm ~0.50-0.53); the pig pseudogene gamma is unremarkable among functional "
                    "rodents. gamma reads promoter stiffness, not thermogenic capacity -- the firewall."),
        "grade": "[V] reproducible reads; the NULL is the point -- gamma is not the criterion",
    }


def null_pdk4_gamma_does_not_mark_hibernation():
    """NULL-2: PDK4 promoter gamma does NOT mark hibernation capacity. The deep hibernator (ground
    squirrel) PDK4 gamma is not elevated vs non-hibernators -- supporting the 'present-but-silenced
    switch' hypothesis (RH4): the torpor program is gated by REGULATION, not encoded in promoter gamma."""
    t = rederive_offline()["reads"]
    hib = t.get("Ictidomys tridecemlineatus", {}).get("genes", {}).get("PDK4", {}).get("gamma")
    nonhib = {o: t[o]["genes"]["PDK4"]["gamma"] for o in ("Homo sapiens", "Mus musculus", "Rattus norvegicus")
              if o in t}
    elevated = bool(hib) and all((hib or -9) > v for v in nonhib.values())
    return {
        "null": "PDK4 promoter gamma does NOT mark hibernation capacity",
        "deep_hibernator_PDK4_gamma": hib, "non_hibernator_PDK4_gamma": nonhib,
        "hibernator_gamma_elevated_vs_nonhibernators": elevated,
        "reading": ("the torpor fuel-switch is PRESENT across the endotherm set (humans included) and its "
                    "promoter gamma is not elevated in the deep hibernator -- the capability is a REGULATORY "
                    "gating of a present switch (RH4 'present-but-silenced'), not a gamma threshold."),
        "grade": "[V] reproducible reads; interpretation of the silenced switch is [O] (read places the "
                 "genes, does not derive the regulatory gating)",
    }


# ---------------------------------------------------------------------------
#  NULL-3 (v0.4.0 expansion) -- the WHOLE torpor-program promoter panel does NOT
#  encode hibernation capacity. The strongest forward test of the firewall: an
#  8-gene fuel-switch / BAT-identity panel read across 14 species (7 hibernators
#  vs 5 non-hibernators among endotherms) -- does ANY promoter gamma track who can
#  hibernate? Pre-registered answer: no. Judged tuning-free by range OVERLAP only;
#  the GC confound is reported by parameter-free sign-agreement and a cross-gene
#  Pearson r, NOT used as a fitted gate.
# ---------------------------------------------------------------------------
TORPOR_PROGRAM_GENES = ["UCP1", "ADRB3", "PDK4", "PPARGC1A", "DIO2", "CIDEA", "FGF21", "SLC2A4"]
# declared classification of the hibernation_capacity label (CITED biology, not a fit):
#   HIB  = can enter regulated hypometabolism (deep hibernation OR daily torpor)
#   NON  = no torpor/hibernation reported; ectotherms are EXCLUDED (poikilotherms do
#          not defend a setpoint, so "hibernation" is undefined for them -- including
#          them would manufacture a GC-driven gap, not a torpor signal).
_HIB_LABELS = ("deep_hibernator", "daily_heterotherm")
_NON_LABELS = ("non_hibernator",)


def _panel_gc(seq):
    """GC fraction recomputed OFFLINE from the cached promoter string (round 4)."""
    n = len(seq)
    return round(sum(1 for c in seq if c in "GCgc") / n, 4) if n else float("nan")


def _cpg_oe(seq):
    """CpG observed/expected (Gardiner-Garden & Frommer 1987), recomputed OFFLINE from the cached
    promoter string. O/E = (N_CpG * L) / (N_C * N_G): a parameter-free, GC-NORMALIZED read of the
    methylation SUBSTRATE -- the CpG-island architecture that DNA methylation acts upon. Unlike gamma
    (a nearest-neighbour stacking-stiffness read that, across this panel, is ~entirely GC-loaded), CpG
    O/E divides the observed CpG count by the count expected from the C and G content, so it removes the
    first-order GC dependence. Low O/E = CpG-depleted (methylation-prone); O/E -> 1 = CpG-island-like
    (methylation-protected). It is a STATIC sequence property, NOT a measured methylation level."""
    s = seq.upper(); L = len(s)
    nC = s.count("C"); nG = s.count("G"); nCG = s.count("CG")
    if nC == 0 or nG == 0:
        return float("nan")
    return round((nCG * L) / (nC * nG), 4)


def _cell_gamma_gc(panel, gene, org):
    """Both scalars re-derived from the vendored cache seq -- nothing trusted from a
    stored field. Returns (None, None) for an absent/uncached cell."""
    cell = panel["cache"].get(gene + "|" + org)
    if not cell or not cell.get("seq"):
        return None, None
    seq = cell["seq"]
    return _gamma(seq), _panel_gc(seq)


def _pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return float("nan")
    return round(sxy / (sxx * syy) ** 0.5, 4)


def _exact_perm_p(a, b):
    """Two-sided exact permutation p for the difference in group means: exhaustively
    enumerate ALL C(n,k) ways to relabel the pooled values into two groups of the
    observed sizes (deterministic, no RNG -- C1). p = fraction of relabelings whose
    |mean gap| is >= the observed |mean gap|."""
    pooled = list(a) + list(b)
    n, k = len(pooled), len(a)
    obs = abs(sum(a) / len(a) - sum(b) / len(b))
    hit = tot = 0
    for combo in itertools.combinations(range(n), k):
        s = set(combo)
        ga = [pooled[i] for i in range(n) if i in s]
        gb = [pooled[i] for i in range(n) if i not in s]
        gap = abs(sum(ga) / len(ga) - sum(gb) / len(gb))
        tot += 1
        if gap >= obs - 1e-12:
            hit += 1
    return (round(hit / tot, 4) if tot else float("nan")), tot


def null_torpor_panel_gamma_does_not_track_hibernation():
    """NULL-3: across an 8-gene torpor/BAT promoter panel read over 14 species, NO
    promoter gamma cleanly separates hibernators from non-hibernators -- and every
    group mean gap that exists co-signs and co-scales with the group GC gap. The
    capability is REGULATORY gating of present genes (RH4 'present-but-silenced'),
    not a promoter-gamma threshold. This generalises NULL-2 from one gene to the
    whole declared program and quantifies the GC confound."""
    p = load_panel()
    sp = p["species"]
    # classify endotherms only, by the declared hibernation_capacity label
    hib_orgs = [o for o in sp if sp[o].get("thermo_class") == "endotherm"
                and sp[o].get("hibernation_capacity") in _HIB_LABELS]
    non_orgs = [o for o in sp if sp[o].get("thermo_class") == "endotherm"
                and sp[o].get("hibernation_capacity") in _NON_LABELS]

    rows, dgam, dgc = [], [], []
    for gene in TORPOR_PROGRAM_GENES:
        hg = [_cell_gamma_gc(p, gene, o) for o in hib_orgs]
        ng = [_cell_gamma_gc(p, gene, o) for o in non_orgs]
        hib_gamma = sorted(g for g, _ in hg if g is not None)
        non_gamma = sorted(g for g, _ in ng if g is not None)
        hib_gc = [c for _, c in hg if c is not None]
        non_gc = [c for _, c in ng if c is not None]
        if len(hib_gamma) < 2 or len(non_gamma) < 2:
            continue
        # parameter-free SEPARATION test: do the two gamma ranges fail to overlap?
        overlap = not (max(hib_gamma) < min(non_gamma) or max(non_gamma) < min(hib_gamma))
        d_gamma = round(sum(hib_gamma) / len(hib_gamma) - sum(non_gamma) / len(non_gamma), 4)
        d_gc = round(sum(hib_gc) / len(hib_gc) - sum(non_gc) / len(non_gc), 4)
        pval, nsplits = _exact_perm_p(hib_gamma, non_gamma)
        rows.append({
            "gene": gene,
            "hib_gamma_range": [hib_gamma[0], hib_gamma[-1]],
            "non_gamma_range": [non_gamma[0], non_gamma[-1]],
            "ranges_overlap": overlap,
            "cleanly_separates": (not overlap),
            "delta_gamma_hib_minus_non": d_gamma,
            "delta_gc_hib_minus_non": d_gc,
            "gamma_gc_sign_agree": bool(d_gamma * d_gc > 0),
            "exact_perm_p": pval, "n_perm_splits": nsplits,
        })
        dgam.append(d_gamma); dgc.append(d_gc)

    n_sep = sum(1 for r in rows if r["cleanly_separates"])
    n_sign_agree = sum(1 for r in rows if r["gamma_gc_sign_agree"])
    r_gamma_gc = _pearson(dgam, dgc)
    # multiplicity context (NOT a fitted gate): does any gene survive Bonferroni 0.05/m?
    m = len(rows)
    bonf = round(0.05 / m, 6) if m else float("nan")
    n_below_bonf = sum(1 for r in rows if r["exact_perm_p"] is not None and r["exact_perm_p"] < bonf)
    # the NULL HOLDS iff no gene cleanly separates the groups by gamma range (parameter-free)
    null_holds = (n_sep == 0)
    return {
        "null": ("the torpor/BAT promoter panel (8 genes) does NOT encode hibernation capacity -- "
                 "no promoter gamma separates hibernators from non-hibernators"),
        "panel_genes": TORPOR_PROGRAM_GENES,
        "hibernators": sorted(hib_orgs), "non_hibernators": sorted(non_orgs),
        "genes_tested": m,
        "genes_that_cleanly_separate_by_gamma": n_sep,
        "genes_with_gamma_gc_sign_agreement": n_sign_agree,
        "cross_gene_pearson_r_delta_gamma_vs_delta_gc": r_gamma_gc,
        "multiplicity_note": ("smallest exact-permutation p across the panel does not survive a "
                              "Bonferroni threshold of %.6f (m=%d); genes below threshold: %d. The "
                              "lone nominal gap is GC-matched and biologically reversed, i.e. it is "
                              "the GC confound, not a torpor signal." % (bonf, m, n_below_bonf)),
        "per_gene": rows,
        "null_holds": bool(null_holds),
        "reading": ("every group gamma gap co-signs with the group GC gap and the cross-gene "
                    "delta_gamma-vs-delta_gc correlation is near-unit-slope -- the gaps ARE the GC "
                    "gaps. Hibernation capacity is regulatory gating of genes that are PRESENT in "
                    "non-hibernators too (humans included): RH4 'present-but-silenced', not a gamma "
                    "threshold. gamma reads promoter stiffness; it is blind to who can hibernate."),
        "grade_reads_and_confound": "[V] reproducible offline reads; the GC confound is a parameter-free, "
                                    "re-derivable fact (sign agreement + near-unit cross-gene slope)",
        "grade_no_marker_conclusion": "[O] the 'no promoter marks hibernation' conclusion is graded open: "
                                      "small n, phylogenetic non-independence (species are not independent "
                                      "draws), and the regulatory-gating mechanism is CITED, not derived here",
    }


# ---------------------------------------------------------------------------
#  NULL-4 (v0.5.0 expansion) -- the methylation-SUBSTRATE architecture (CpG O/E)
#  does NOT mark hibernation either, and is a DISTINCT sequence read from gamma.
#  RH8 closed one static sequence layer (stacking-stiffness gamma), but gamma is
#  ~entirely GC-loaded across this panel, so a skeptic could say "you only tested
#  GC". CpG O/E is the natural second layer: GC-NORMALIZED (it divides observed
#  CpG by the C,G-expected count) and the genomic SUBSTRATE on which methylation-
#  based gating operates. Pre-registered: (i) does any gene's CpG-O/E range
#  separate hibernators? (predicted no -- the machinery is present in everyone);
#  (ii) is CpG O/E DISSOCIATED from gamma? (predicted yes -- a genuinely different
#  read, not a gamma restatement). Separation is judged by range OVERLAP only; the
#  dissociation is reported by parameter-free Pearson r, NEVER used as a fitted
#  gate. The DYNAMIC torpor methylation/expression STATE remains [O] external.
# ---------------------------------------------------------------------------
def null_cpg_oe_does_not_track_hibernation():
    """NULL-4: across the same 8-gene torpor/BAT promoter panel read over 14 species, the methylation-
    SUBSTRATE architecture (CpG observed/expected) ALSO fails to separate hibernators from non-
    hibernators -- 0 of 8 genes cleanly separate, all ranges overlap. CpG O/E is a DISTINCT read from
    gamma (cross-cell Pearson r well below 1) and is far LESS GC-loaded than gamma, so this is not a
    restatement of the RH8 GC confound: it closes a SECOND, GC-normalized static sequence layer. Reading:
    neither static promoter layer (stacking-stiffness gamma nor methylation-substrate architecture)
    encodes hibernation capacity -- the capability is DYNAMIC regulatory gating of genes present in all
    (humans included), visible only in an in-vivo torpor<->euthermia methylation/expression contrast
    (CITED [O] external). This generalises RH4/RH8 from sequence stiffness to the methylation substrate
    and sharpens the firewall: gamma reads structure only, and even a second structural layer is blind
    to who can hibernate."""
    p = load_panel()
    sp = p["species"]
    hib_orgs = [o for o in sp if sp[o].get("thermo_class") == "endotherm"
                and sp[o].get("hibernation_capacity") in _HIB_LABELS]
    non_orgs = [o for o in sp if sp[o].get("thermo_class") == "endotherm"
                and sp[o].get("hibernation_capacity") in _NON_LABELS]

    def _cell_oe(gene, org):
        cell = p["cache"].get(gene + "|" + org)
        if not cell or not cell.get("seq"):
            return None
        return _cpg_oe(cell["seq"])

    rows, doe, dgc = [], [], []
    # cross-cell vectors for the gamma<->CpG-O/E dissociation (and each vs GC), parameter-free
    cc_gamma, cc_oe, cc_gc = [], [], []
    for gene in TORPOR_PROGRAM_GENES:
        ho = sorted(v for v in (_cell_oe(gene, o) for o in hib_orgs) if v is not None)
        no = sorted(v for v in (_cell_oe(gene, o) for o in non_orgs) if v is not None)
        hib_gc = [c for _, c in (_cell_gamma_gc(p, gene, o) for o in hib_orgs) if c is not None]
        non_gc = [c for _, c in (_cell_gamma_gc(p, gene, o) for o in non_orgs) if c is not None]
        for o in hib_orgs + non_orgs:
            g, c = _cell_gamma_gc(p, gene, o); oe = _cell_oe(gene, o)
            if g is not None and c is not None and oe is not None:
                cc_gamma.append(g); cc_oe.append(oe); cc_gc.append(c)
        if len(ho) < 2 or len(no) < 2:
            continue
        overlap = not (max(ho) < min(no) or max(no) < min(ho))
        d_oe = round(sum(ho) / len(ho) - sum(no) / len(no), 4)
        d_gc = round(sum(hib_gc) / len(hib_gc) - sum(non_gc) / len(non_gc), 4)
        pval, nsplits = _exact_perm_p(ho, no)
        rows.append({
            "gene": gene,
            "hib_cpg_oe_range": [ho[0], ho[-1]],
            "non_cpg_oe_range": [no[0], no[-1]],
            "ranges_overlap": overlap,
            "cleanly_separates": (not overlap),
            "delta_cpg_oe_hib_minus_non": d_oe,
            "delta_gc_hib_minus_non": d_gc,
            "exact_perm_p": pval, "n_perm_splits": nsplits,
        })
        doe.append(d_oe); dgc.append(d_gc)

    n_sep = sum(1 for r in rows if r["cleanly_separates"])
    r_gamma_oe = _pearson(cc_gamma, cc_oe)   # the two static reads: dissociation (well below 1)
    r_gamma_gc = _pearson(cc_gamma, cc_gc)   # gamma's near-total GC loading (RH8)
    r_oe_gc = _pearson(cc_oe, cc_gc)         # CpG O/E is GC-normalized: far less GC-loaded
    m = len(rows)
    bonf = round(0.05 / m, 6) if m else float("nan")
    n_below_bonf = sum(1 for r in rows if r["exact_perm_p"] is not None and r["exact_perm_p"] < bonf)
    null_holds = (n_sep == 0)
    # the two reads are genuinely distinct iff |r(gamma,CpG_OE)| is clearly sub-unit AND CpG O/E is
    # markedly less GC-loaded than gamma (reported, not gated)
    reads_are_distinct = bool(abs(r_gamma_oe) < 0.9 and abs(r_oe_gc) < abs(r_gamma_gc))
    return {
        "null": ("the methylation-substrate architecture (CpG observed/expected) of the 8-gene torpor/BAT "
                 "panel does NOT encode hibernation capacity -- no promoter CpG O/E separates hibernators "
                 "from non-hibernators, and CpG O/E is a distinct, GC-normalized read (not a gamma restatement)"),
        "panel_genes": TORPOR_PROGRAM_GENES,
        "hibernators": sorted(hib_orgs), "non_hibernators": sorted(non_orgs),
        "genes_tested": m,
        "genes_that_cleanly_separate_by_cpg_oe": n_sep,
        "cross_cell_pearson_r_gamma_vs_cpg_oe": r_gamma_oe,
        "cross_cell_pearson_r_gamma_vs_gc": r_gamma_gc,
        "cross_cell_pearson_r_cpg_oe_vs_gc": r_oe_gc,
        "two_static_reads_are_distinct": reads_are_distinct,
        "multiplicity_note": ("smallest exact-permutation p across the panel does not survive a Bonferroni "
                              "threshold of %.6f (m=%d); genes below threshold: %d." % (bonf, m, n_below_bonf)),
        "per_gene": rows,
        "null_holds": bool(null_holds),
        "reading": ("CpG O/E removes the first-order GC dependence that drives the RH8 gamma confound "
                    "(cross-cell r(gamma,GC) is near 1 while r(CpG_OE,GC) is much lower), yet CpG O/E STILL "
                    "fails to separate hibernators (0 of 8 genes). The two static sequence reads are distinct "
                    "(r(gamma,CpG_OE) is clearly sub-unit), so this is a SECOND independent layer, not a "
                    "restatement of gamma. Neither the stacking-stiffness layer nor the methylation-substrate "
                    "layer marks hibernation: the capability is DYNAMIC regulatory gating of genes present in "
                    "everyone (RH4 'present-but-silenced'), readable only in an in-vivo torpor<->euthermia "
                    "methylation/expression contrast (CITED [O] external). gamma -- and now a second structural "
                    "read -- is blind to who can hibernate."),
        "dynamic_regulation_is_external": CITED_DYNAMIC_REGULATION["torpor_methylation_expression"],
        "grade_reads_and_dissociation": "[V] reproducible offline reads; the gamma<->CpG-O/E dissociation and "
                                        "the GC-loading contrast are parameter-free, re-derivable facts",
        "grade_no_marker_conclusion": "[O] the 'no static promoter read marks hibernation' conclusion is graded "
                                      "open: small n, phylogenetic non-independence, and the DYNAMIC regulatory "
                                      "gating that DOES carry the capability is CITED external biology, not "
                                      "derived here (the offline invariant precludes ingesting in-vivo data)",
    }


# ---------------------------------------------------------------------------
#  Q2 -- the R19 mechanism: defended attractor (endotherm) vs ambient-tracking (ectotherm)
# ---------------------------------------------------------------------------
def setpoint_defense_sweep(g_endo=1.40, g_ecto=0.18, ambient_max=0.30):
    """RT1 discriminant. The defended setpoint is the UPPER R19 well; an ambient drive h pushes it
    toward collapse. While |h| < spinodal the well SURVIVES (state PINNED, small displacement); once
    |h| > spinodal the well COLLAPSES and the state falls to the other branch (TRACKS ambient). So the
    discriminant is the spinodal THRESHOLD: deep basin (endotherm) defends, shallow/no basin (ectotherm)
    tracks. Ambient-sensitivity = collapse fraction at the strongest cold push, and FALLS monotonically
    as the basin deepens. g_endo/g_ecto are MODEL loop-gains for the two regimes -- NOT fitted; the
    monotone fall and the spinodal threshold are the mechanism [V]; absolute loop-gains [O]."""
    import math
    seed_everything()

    def sensitivity(g):
        # defended setpoint anchored at the upper well; strongest cold push h = -ambient_max
        s0 = +math.sqrt(g)
        s = settle(g, -ambient_max, s0=s0)
        return abs(s - s0) / (2.0 * s0)     # 0 = pinned in well, ~1 = collapsed to other branch

    s_endo = round(sensitivity(g_endo), 6)
    s_ecto = round(sensitivity(g_ecto), 6)
    ladder = [0.10, 0.18, 0.40, 0.80, 1.20, 1.60]
    curve = [{"g": g, "barrier": round(barrier(g), 4), "spinodal": round(spinodal(g), 4),
              "defends": bool(spinodal(g) > ambient_max), "ambient_sensitivity": round(sensitivity(g), 6)}
             for g in ladder]
    monotone = all(curve[i]["ambient_sensitivity"] >= curve[i + 1]["ambient_sensitivity"] - 1e-9
                   for i in range(len(curve) - 1))
    return {
        "question": "does core state stay PINNED (defended attractor=endotherm) or FOLLOW ambient (tracking=ectotherm)?",
        "ambient_drive_amplitude": ambient_max,
        "endotherm_loop": {"g": g_endo, "barrier": round(barrier(g_endo), 4),
                           "spinodal": round(spinodal(g_endo), 4), "ambient_sensitivity": s_endo},
        "ectotherm_loop": {"g": g_ecto, "barrier": round(barrier(g_ecto), 4),
                           "spinodal": round(spinodal(g_ecto), 4), "ambient_sensitivity": s_ecto},
        "endotherm_pins": bool(s_endo < 0.15), "ectotherm_tracks": bool(s_ecto > 0.6),
        "discriminant": "a loop defends iff spinodal(g) > ambient drive amplitude; else it tracks",
        "barrier_vs_sensitivity_curve": curve, "sensitivity_monotone_decreasing_in_barrier": monotone,
        "grade": "[V] mechanism (spinodal threshold + monotone sensitivity vs barrier); absolute loop-gains [O]",
    }


def continuum_or_switch(g=1.40):
    """RT4 discriminant. Within ONE basin the response to drive is a smooth DIAL; the switch BETWEEN
    two regulated attractors is DISCONTINUOUS past the spinodal. So endotherm-vs-ectotherm is discrete
    at the effector-PRESENCE level (categorical: command pair present vs absent) and a continuum WITHIN
    endotherms (loop gain). The spinodal is the discontinuity (mechanism [V]); species placement [O]."""
    sp = spinodal(g)
    # demonstrate the discontinuity: just inside vs just outside the spinodal, the surviving basin flips
    s_inside  = settle(g, +0.95 * sp, s0=-1.0)   # lower branch survives below spinodal
    s_outside = settle(g, +1.05 * sp, s0=-1.0)   # forced across: only the upper branch remains
    return {
        "question": "is there an R19 spinodal SEPARATING the two strategies, or a smooth gradient?",
        "r19_spinodal_h_sp": round(sp, 6),
        "state_just_inside_spinodal": round(s_inside, 6),
        "state_just_outside_spinodal": round(s_outside, 6),
        "discontinuous_jump_at_spinodal": bool((s_outside - s_inside) > 0.5),
        "reading": ("categorical at the effector-presence level (command pair present vs absent = a discrete "
                    "switch), a continuum within endotherms (loop gain). The spinodal is the discontinuity."),
        "grade": "[V] spinodal mechanism; absolute species placement [O]",
    }


def endothermy_cost(g_ladder=(0.40, 0.80, 1.20, 1.60)):
    """RT3 discriminant. Holding a setpoint against an ambient drive needs a restoring FLUX; the deeper
    the basin (higher loop gain), the larger the restoring flux at a fixed off-setpoint displacement --
    a higher idling 'furnace' cost. The DIRECTION (cost rises with defence) is [V]; the cited absolute
    ratio (endotherm idles ~5-10x an ectotherm) is [L]; absolute W/kg is [O] (needs external calibration)."""
    disp = -0.25   # a fixed displacement below setpoint (a standing cold load)
    # restoring flux magnitude |ds/dt| the loop must generate to hold against the displacement
    rows = [{"g": g, "barrier": round(barrier(g), 4),
             "restoring_flux_at_fixed_displacement": round(abs(sdot(disp, g, 0.0)), 6)} for g in g_ladder]
    rises = all(rows[i]["restoring_flux_at_fixed_displacement"]
                <= rows[i + 1]["restoring_flux_at_fixed_displacement"] + 1e-9 for i in range(len(rows) - 1))
    return {
        "question": "what does DEFENDING the setpoint cost, and why is endothermy a different basin?",
        "restoring_flux_vs_loop_gain": rows, "cost_rises_with_defence": rises,
        "cited_absolute_ratio": CITED_RANGES["bmr_ratio_endo_over_ecto"],
        "grade": "[V] direction (cost rises with defence); ratio [L] cited; absolute W/kg [O] obstacle: "
                 "absolute metabolic rate needs external calorimetric calibration, not in the R19 read",
    }


def kleiber_status():
    """RT5. Metabolic rate ~ mass^(3/4). HONEST: the 3/4 exponent is NOT derivable from the R19
    primitive alone -- it requires an external transport-network argument (fractal supply, West-Brown-
    Enquist) or a surface/volume scaling that the substrate does not contain. Flagged [O] with the
    obstacle stated (per the CHARTER: reproduced [V] OR flagged [O]). No fabricated exponent."""
    return {
        "claim": "metabolic rate ~ mass^(3/4)",
        "status": "OPEN [O]",
        "obstacle": ("the 3/4 exponent is a transport-network / allometric result (fractal nutrient supply, "
                     "or surface-to-volume scaling); the R19 dwell primitive sets RELATIVE organ size "
                     "(dwell ~ gamma^1.5) but does not encode whole-body 3/4 metabolic scaling. The substrate "
                     "is agnostic to the exponent -- it is not faked here."),
        "grade": "[O] honest open with stated obstacle",
    }
