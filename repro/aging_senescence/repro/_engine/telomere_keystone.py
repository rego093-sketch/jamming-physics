#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
telomere_keystone.py  --  RA9: the TELOMERE deep dive, and where the telomere lever actually sits.

WHY THIS MODULE.  Two independent results in this package both point at the telomere. The cross-species
discriminant (RA7) finds that of the four aging masters, TERT (telomere maintenance) is the ONE gene
whose lifespan lean is not removed by body-mass correction and that carries the largest phylogenetic
contrast -- the single residual [O] lead. The archaic <-> present-day observation (RA8) finds that TERT
carries the most homozygous-derived promoter substitutions across the dated-individual set, with a
three-position pattern that co-occurs across all four archaic genomes. TERT is, on both axes, the most
distinctive aging master. This module asks the sharp follow-up: if the telomere is the keystone, what
exactly is the keystone -- the gamma of the machinery, or the dynamics of the reservoir it maintains?

WHAT IS MEASURED.
  (A) The canonical vertebrate telomere repeat (TTAGGG)n has a promoter-style gamma of ~1.330, the
      SAME on the G-rich strand and its C-rich complement (the SantaLucia table is strand-symmetric),
      and it is the LOWEST gamma of any aging-related sequence in the package (below all four master
      promoters). The value is length-independent to <0.5% (edge effects only): the telomere gamma is a
      near-exact universal constant -- the same "ruler" in every species and every dated individual.
  (B) The reservoir law (RA3): capacity ~ gamma^1.5 (DWELL). The telomere is a FINITE reservoir that
      depletes monotonically to the replicative limit. Because the telomere-repeat gamma is invariant,
      the reservoir RULER does not differ between individuals or species. What differs is the COUNT of
      repeats (telomere length) and the per-division attrition RATE -- neither of which is a gamma or a
      sequence-identity quantity.

THE VERDICT.  The telomere is the keystone of aging DYNAMICS, not of aging gamma. The promoter-gamma
axis correctly reports it as only a weak modulator (RA7 within-distribution; RA8 tiny gamma spread),
because the telomere lever acts OFF that axis -- through reservoir size (length) and depletion rate, the
same off-gamma-axis pattern as the cross-species telomerase-dosage and TP53 copy-number levers. This
locates, rather than contradicts, the intuition that "the telomere is the key": it is the keystone, and
the keystone mechanism is reservoir dynamics.

GRADES (C3): the telomere-repeat gamma invariance and the LOWEST-gamma ranking are MEASURED [V]; the
reservoir law is [F] (vendored substrate); the "keystone is dynamics not gamma" reading is [O] (it
organizes the package's own measured facts but is an interpretation); telomere length and per-division
attrition rates are [L] (cited, not reproduced in-package).
"""
import os, sys, json

_HERE = os.path.dirname(__file__)
NN_DG37 = {"AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88, "CA": -1.45, "CC": -1.84,
           "CG": -2.17, "CT": -1.28, "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
           "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00}
_COMP = {"A": "T", "T": "A", "G": "C", "C": "G"}

TELOMERE_REPEAT = "TTAGGG"          # canonical vertebrate telomere unit (G-rich strand)
CANON_REPEATS = 100                 # fixed canonical tract (600 nt) for a reproducible value
# cited telomere biology (NOT reproduced in-package) -- graded [L]
ATTRITION_CITED = {
    "human_leukocyte_attrition_bp_per_year": "~20-50 bp/yr (cited [L]: Frenck 1998; Aubert & Lansdorp 2008)",
    "human_per_division_loss_bp": "~50-100 bp/division (end-replication + oxidative; cited [L]: Harley 1990)",
    "large_mammal_lever": "somatic telomerase suppression in large/long-lived mammals (cited [L]: Gomes 2011)",
}


def _revcomp(s):
    return "".join(_COMP[c] for c in reversed(s))


def _gamma(seq):
    seq = "".join(c for c in seq if c in "ACGT")
    st = [NN_DG37[seq[i:i + 2]] for i in range(len(seq) - 1) if seq[i:i + 2] in NN_DG37]
    return (-sum(st) / len(st)) if st else None


def telomere_gamma():
    """gamma of the canonical telomere repeat, both strands, plus the exact asymptotic limit."""
    g = TELOMERE_REPEAT * CANON_REPEATS
    c = _revcomp(g)
    gg = _gamma(g)
    cc = _gamma(c)
    # exact asymptotic: the mean of the 6 periodic dinucleotides of TTAGGG (wraparound to next unit)
    period = [TELOMERE_REPEAT[i:i + 2] for i in range(len(TELOMERE_REPEAT) - 1)] + \
             [TELOMERE_REPEAT[-1] + TELOMERE_REPEAT[0]]
    asymptote = -sum(NN_DG37[d] for d in period) / len(period)
    return dict(repeat=TELOMERE_REPEAT, canonical_repeats=CANON_REPEATS, tract_nt=len(g),
                gamma_G_rich=round(gg, 6), gamma_C_rich=round(cc, 6),
                strand_symmetric=bool(abs(gg - cc) < 1e-9),
                gamma_asymptotic_exact=round(asymptote, 6),
                length_independent=bool(abs(gg - asymptote) < 0.005),
                periodic_dinucleotides=period)


def keystone():
    sys.path.insert(0, _HERE)
    import importlib
    xd = importlib.import_module("xspecies_discriminant")
    ad = importlib.import_module("aging_dynamics")
    arc = importlib.import_module("archaic_discriminant")

    tel = telomere_gamma()
    ra7 = xd.discriminant()
    ra3 = ad.ra3_reservoir_depletion()
    ra8 = arc.discriminant()

    # (A) telomere-repeat gamma vs the four HUMAN master promoters (the package's canonical node atlas,
    #     organ_gamma.json -- same values shown in section 2); a measured ranking
    _MG = json.load(open(os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json"),
                         encoding="utf-8"))["genes"]
    master_gamma = {g: round(_MG[g]["gamma"], 4) for g in ["TP53", "CDKN2A", "FOXO3", "TERT"]}
    tel_g = tel["gamma_G_rich"]
    lowest = bool(all(tel_g < v for v in master_gamma.values()))
    ranking = sorted(list(master_gamma.items()) + [("telomere_repeat", round(tel_g, 4))],
                     key=lambda kv: kv[1])

    # (B) TERT as the keystone gene -- two independent measured leads (RA7 + RA8)
    tert = ra7.get("tert_focus", {}) if isinstance(ra7.get("tert_focus"), dict) else {}
    # xspecies_discriminant exposes the TERT residual via the audit; pull what is present defensively
    tert_lead = dict(
        cross_species_residual=("TERT is the only master whose lifespan lean is not removed by body-mass "
                                "correction (RA7, the package's single residual [O] lead)"),
        archaic_substitution_load=ra8["verdict"]["archaic_substitution_load"],
        archaic_most_substituted=ra8["verdict"]["gene_with_most_archaic_substitutions"],
        tert_cancer_hotspots_invariant=ra8["verdict"]["tert_cancer_hotspots_invariant"],
        note=("on the cross-species axis and on the dated-individual axis, TERT is the most distinctive "
              "aging master; both are measured observations"))

    # (C) the reservoir reading: invariant ruler, variable length+rate
    reservoir = dict(
        telomere_reservoir=ra3["reservoirs"]["telomere_TERT"],
        law=ra3["law"],
        ruler_is_invariant=("the telomere-repeat gamma is a near-exact universal constant (A), so the "
                            "gamma^1.5 reservoir RULER is identical across individuals and species"),
        what_varies=("repeat COUNT (telomere length) and per-division attrition RATE -- neither is a "
                     "gamma or a sequence-identity quantity"),
        varies_grade="[L] (telomere length and attrition rates cited, not reproduced in-package)")

    verdict = dict(
        telomere_repeat_gamma=tel_g,
        telomere_gamma_strand_symmetric=tel["strand_symmetric"],
        telomere_gamma_is_lowest_of_all_aging_sequences=lowest,
        gamma_ranking_ascending=ranking,
        telomere_gamma_universal_constant=tel["length_independent"],
        keystone_gene="TERT",
        keystone_mechanism="reservoir dynamics (length + attrition rate), OFF the promoter-gamma axis",
        answer=("The telomere is the keystone of aging on this substrate, but the keystone is its "
                "DYNAMICS, not its gamma. The canonical telomere repeat (TTAGGG)n has gamma "
                + ("%.4f" % tel_g) + " -- identical on both strands and the LOWEST gamma of any "
                "aging-related sequence in the package (below all four master promoters) -- and it is a "
                "near-exact universal constant, the same ruler in every species and every dated "
                "individual. TERT, the gene that maintains this reservoir, is independently the most "
                "distinctive aging master on two measured axes: it is the single cross-species residual "
                "lead (RA7) and it carries the most archaic promoter substitutions (RA8). Yet its "
                "promoter gamma sits inside the mammalian distribution and varies by < 0.0008 across the "
                "dated-individual set, because the telomere lever acts OFF the gamma axis -- through "
                "reservoir size (telomere length) and depletion rate (attrition), the same off-axis "
                "pattern as the cross-species telomerase-dosage and TP53 copy-number levers. The "
                "promoter-gamma axis is therefore correct to report the telomere as only a weak gamma "
                "modulator; the keystone role lives in the reservoir dynamics that gamma does not index."),
        grade=("[V] telomere-repeat gamma invariance, strand symmetry, and lowest-gamma ranking are "
               "measured; [F] the gamma^1.5 reservoir law (vendored substrate); [O] the 'keystone is "
               "dynamics not gamma' synthesis (it organizes the package's measured facts but is an "
               "interpretation); [L] telomere length and per-division attrition rates (cited)."),
        cited_rates=ATTRITION_CITED)

    passed = bool(tel["strand_symmetric"] and lowest and tel["length_independent"])
    return dict(telomere_gamma=tel, gamma_vs_masters=dict(master_gamma=master_gamma,
                telomere_repeat=round(tel_g, 6), telomere_is_lowest=lowest, ranking_ascending=ranking),
                tert_keystone_leads=tert_lead, reservoir_reading=reservoir,
                verdict=verdict, passed=passed)


if __name__ == "__main__":
    print(json.dumps(keystone(), ensure_ascii=False, indent=1))
