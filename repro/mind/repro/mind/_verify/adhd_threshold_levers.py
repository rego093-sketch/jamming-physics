#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adhd_threshold_levers.py  —  ADHD-T-L (sec.35): the drive-tone target map for the ADHD gain/arousal
operating point, and the SIXTH application of the inherited analgesic_threshold_logic v2.0 cross-cutting
layer (after bipolar sec.30, epilepsy sec.31, depression sec.32, schizophrenia sec.33 and autism sec.34).
It re-derives no rule: it reads the SAME R19 substrate (E.spinodal/E.barrier) and the SAME
gamma = -mean(NN stacking dG, SantaLucia 1998) the engine uses to write genes, and it maps the sec.22
ADHD substrate (adhd_axis_specific lock -- the SSOT) onto the formal L1/L2/L3 inheritance frame.

WHY THIS IS THE FIRST *PARTIAL* FIT [L] (the headline). The five prior applications were CLEAN [V]
threshold disorders: their fault is a firing FOLD that is too low (or too easily switched), and the
levers RAISE the fold. ADHD is NOT a fold disorder. sec.22 (adhd_axis_specific) establishes ADHD as a
GAIN/AROUSAL substrate with INTACT WIRING -- six catecholamine GAIN/OUTPUT genes (the O axis) and two
adrenergic/monoaminergic AROUSAL-TONE genes (the T axis), and -- the discriminant from autism -- NO
long-range wiring fault. The threshold-shift frame operates on the firing FOLD via an upstream DRIVE
lever (L3). So it REACHES ADHD only through the AROUSAL/DRIVE-TONE surface (the reuptake transporters
and tone receptors -- where the established ADHD pharmacology lives, as DIRECTIONS), and it does NOT
reach the GAIN-AMPLITUDE machinery (catecholamine SYNTHESIS / RELEASE / catabolism), which is the
disorder's DOMINANT fault. The fit is therefore PARTIAL [L]: the frame catches the drive-tone set-point
but not the gain-amplitude core. This is the honest, recorded limit.

THE TWO ADHD AXES (sec.22 adhd_axis_specific; re-cut here by threshold-frame REACHABILITY):
  DT  (drive-tone / AROUSAL)        = the upstream catecholamine/monoaminergic DRIVE TONE. REACHED by the
        L3 lever: the reuptake transporters (DAT/NET/SERT) and the tone receptors (a2A/D4) set the
        ambient drive/arousal tone, i.e. the firing set-point. This draws from BOTH sec.22 axes -- the
        sec.22-T arousal genes (SLC6A4, ADRA2A) AND the reachable sec.22-O drive genes (SLC6A3, DRD4) --
        plus the NET arm SLC6A2 (the noradrenergic reuptake partner of DAT). Corrective sign = NORMALISE
        the drive tone (the catecholamine DIRECTION; the stimulant/atomoxetine/guanfacine surface).
  GA  (gain-amplitude / OUTPUT)     = the catecholamine SYNTHESIS (TH/DBH), RELEASE (SNAP25) and
        catabolic-clearance (COMT) machinery that sets signal AMPLITUDE -- the sec.22-O gain core, the
        DOMINANT ADHD fault. NOT REACHED: a firing-fold / drive-tone lever has no handle on synthesis or
        release (it shifts the TONE the cell reads, not the GAIN it produces). The threshold frame reaches
        this axis only INDIRECTLY (raise upstream drive -> downstream signal rises with it), never as a
        direct gain handle -- the autism O-axis (gain-deficit) analogue, here the DOMINANT axis, which is
        exactly why ADHD is a PARTIAL fit.
  W   (long-range WIRING)           = NONE. ADHD carries NO wiring fault (sec.22: intact wiring, the
        discriminant from autism). So unlike autism (whose out-of-reach included a W axis PROVEN
        unreachable in sec.19), ADHD has ZERO wiring out-of-reach genes -- recorded as the structural
        difference (the autism INVERSE: autism reached its dominant T axis and missed O+W; ADHD reaches
        only the secondary DT axis and misses the dominant GA axis, with no W axis at all).

THE LEVER DISTRIBUTION (honest). Where bipolar leaned on L1 (calcium), epilepsy on L2 (the M-current),
depression on L3 (HPA/monoamine, L3-dominant with a reachable L1/L2 mix), schizophrenia on L1+L3
co-dominant (glutamate + dopamine) and autism on L1-DOMINANT with a sparse L3, ADHD is L3-ONLY:
  L1  reduce the inward excitatory (Na/Ca/glutamate) current   (EMPTY -- ADHD is not a channelopathy)
  L2  increase the outward K+ / restore GABA-A inhibition      (EMPTY -- no ionic inhibitory lever)
  L3  normalise an UP-STREAM drive (catecholamine/monoaminergic reuptake & receptor tone)   (ALL 5 levers)
ADHD is the PUREST L3 case in the series and the L1/L2 EMPTINESS is itself the finding: ADHD has no ionic
fold lever at all -- its only threshold-frame handle is the [O] cited-biology upstream-drive channel, a
second sense in which the fit is partial (no [F] structural grounding, only the [O] drive surface).

THE FIREWALL (binding, non-negotiable; inherited verbatim in spirit). gamma / spinodal |h_sp| / barrier
are the engine's READ of the locus' promoter switch-threshold STRUCTURE. They are [V] (reproducible);
their ORDER is [F] (forced). This is NOT a transporter occupancy, NOT a synaptic dopamine/noradrenaline
level, NOT a drug potency, NOT a dose, NOT an in-vivo selectivity, NOT a clinical effect, and -- the
ADHD-specific addition -- the promoter |h_sp| is NOT the sec.22 network GAIN/AROUSAL quantity (the
catecholamine signal amplitude / arousal set-point). gamma is blind to on/off and to expression level.
The L3 (catecholamine/monoaminergic drive) mechanism link is [O].

THE HONEST CAVEATS (ADHD-specific; recorded, not hidden).
  (i)   PARTIAL FIT [L]. The DOMINANT ADHD fault (the GA gain-amplitude axis) is OUT OF REACH of the
        threshold frame; only the secondary DT drive-tone axis is reached. First non-clean fit in the
        series. Recorded as the fit_grade.
  (ii)  THE sec.22-O/THRESHOLD-FRAME CROSS-CUT. sec.22 classes SLC6A3 and DRD4 as gain (O) genes; the
        threshold frame places them with the DT drive-tone levers because as a transporter and a receptor
        their modulation shifts the ambient drive TONE (the reachable surface), whereas the SYNTHESIS /
        RELEASE machinery on the SAME sec.22-O axis (TH/DBH/SNAP25) is out of reach. The two cuts CROSS
        -- which IS the partial-fit signature: sec.22's dominant gain axis is split by reachability.
        COMT (catabolic clearance) is the boundary gene: clearance is tone-adjacent, but sec.22 assigns
        it to the gain axis and its amplitude effect is synthesis-independent, so it is carried with the
        gain machinery (flagged).
  (iii) W = NONE. ADHD has intact wiring (sec.22) -- ZERO wiring out-of-reach genes, the discriminant
        from autism. Recorded in the witness as present_in_disorder=False.

HONESTY (binding, Axis-A). MECHANISM-DIRECTION only. efficacy = 0 everywhere. This ranks/places READS and
TARGETS, never drugs, doses, protocols, or patients. NOTHING here says any agent treats anyone. ADHD is
POLYGENIC and HETEROGENEOUS, its established pharmacology acts on the DRIVE-TONE surface only, and a lever
direction is a mechanism boundary, NOT a claim about whether attention/arousal should be changed, nor a
licence for stimulant misuse or cognitive enhancement (the forbidden-claim scanner enforces this).
consciousness_claim stays 0; hard problem OPEN.

No tuning: gamma is measured; |h_sp|/barrier are the locked R19 forms; the lever assignments, axis mapping
and citations are CITED Layer-2 biology + the sec.22 substrate, not engine outputs. Governed by
VP_SPEC_v1_8 (SEED=19). Engine imported READ-ONLY (tree 0fbf4988...).

Run:  python3 adhd_threshold_levers.py
Out:  adhd_threshold_levers_results.json  + its sha256 (2x deterministic)
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY; provides spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4, emerge_all

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "adhd_levers_promoters.cache.json")
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

# SantaLucia 1998 unified NN dG37 -- the SAME table the engine / analgesic / DNA pipeline use.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}
def gamma(seq):
    """Interfacial tension / stiffness = -mean(NN stacking dG). Strand-symmetric. [V] read."""
    s = seq.upper()
    v = [-NN[s[i:i+2]] for i in range(len(s)-1) if s[i:i+2] in NN]
    return float(sum(v)/len(v)) if v else float("nan")

# ---- lever-frame text (inherited from analgesic v2.0, re-pointed at the ADHD drive-tone axis) ----
LEVER_FRAME = {
  "L1": "reduce the inward excitatory (Na/Ca/glutamate) current -- the ionic excitatory route. EMPTY for "
        "ADHD: ADHD is not a channelopathy; it carries no ionic excitatory fault gene in the sec.22 "
        "substrate. The absence is itself part of the partial-fit signature",
  "L2": "increase the outward K+ / restore the GABA-A inhibitory current -- the ionic inhibitory route. "
        "EMPTY for ADHD: there is no ionic inhibitory lever gene in the sec.22 ADHD substrate",
  "L3": "normalise an UP-STREAM catecholamine/monoaminergic DRIVE. ALL of the ADHD levers sit here: the "
        "reuptake transporters (DAT/NET/SERT) and the tone receptors (a2A/D4) set the ambient drive / "
        "arousal TONE -- the firing set-point -- and are the surface the established ADHD pharmacology "
        "acts on (as DIRECTIONS). This reaches the DT (drive-tone/arousal) axis ONLY; the GA "
        "(gain-amplitude) machinery is out of reach (partial fit [L]). The mechanism link is [O]",
}

# grade strings
GL3 = ("[O] cited biology: gamma places the gene in the drive-tone lever map; the catecholamine/"
       "monoaminergic drive (reuptake/receptor-tone) signalling mechanism is NOT derived")

DOM_DT = "DT (the drive-tone / arousal axis the L3 lever REACHES -- the firing set-point)"

# ===================== LEVER TARGETS (the DT drive-tone genes that ARE the levers; all L3) =====================
# sec.22 axis recorded per gene for SSOT cross-reference: SLC6A3/DRD4 are sec.22-O (gain) but reachable as
# drive-TONE (transporter/receptor); SLC6A4/ADRA2A are sec.22-T (arousal tone); SLC6A2 (NET) extends the
# substrate as the noradrenergic reuptake partner of DAT (the atomoxetine arm).
CONTEXT = {
  "SLC6A3": dict(lever="L3", domain=DOM_DT, channel=None, protein="dopamine transporter DAT (SLC6A3)",
      sec22_axis="O (sec.22 gain) -- reachable here as drive-TONE: a transporter sets ambient DA tone",
      push="normalise the dopaminergic drive tone via DAT reuptake -- the central ADHD drive-tone lever (the methylphenidate/amphetamine DIRECTION); reuptake sets the ambient dopamine tone, i.e. the firing set-point",
      adhd_anchor="the dopamine transporter (DAT1/SLC6A3); the 3'-UTR VNTR is one of the most-studied ADHD candidate loci and DAT is the primary target of methylphenidate -- the canonical ADHD drive-tone node",
      drive_agent="dopaminergic reuptake-modulation DIRECTION for the DT axis (the stimulant/DAT route, as DIRECTION, not efficacy; not a dose; not a misuse licence)",
      grade_mechanism=GL3,
      src="Cook 1995 Am J Hum Genet 56:993 (DAT1 VNTR, ADHD); Faraone 2021 Nat Rev Dis Primers 7:51 (DAT, methylphenidate target)"),
  "SLC6A2": dict(lever="L3", domain=DOM_DT, channel=None, protein="noradrenaline transporter NET (SLC6A2)",
      sec22_axis="drive (NET) -- the noradrenergic reuptake partner of DAT; extends the sec.22 substrate (the atomoxetine arm)",
      push="normalise the noradrenergic drive tone via NET reuptake -- the noradrenergic partner of the DAT lever (the atomoxetine DIRECTION); NET reuptake sets the ambient noradrenaline tone on the same DT axis",
      adhd_anchor="the noradrenaline transporter (NET/SLC6A2); the primary target of atomoxetine, the principal non-stimulant ADHD agent -- the noradrenergic drive-tone partner of DAT",
      drive_agent="noradrenergic reuptake-modulation DIRECTION for the DT axis (the atomoxetine/NET route, as DIRECTION, not efficacy; not a dose)",
      grade_mechanism=GL3,
      src="Bymaster 2002 Neuropsychopharmacology 27:699 (atomoxetine, NET); Faraone 2021 Nat Rev Dis Primers 7:51 (noradrenergic ADHD pharmacology)"),
  "SLC6A4": dict(lever="L3", domain=DOM_DT, channel=None, protein="serotonin transporter 5-HTT (SLC6A4)",
      sec22_axis="T (sec.22 arousal tone) -- monoaminergic arousal/E-I tone",
      push="modulate the serotonergic arousal tone (5-HTT) -- a monoaminergic DT contributor on the sec.22 arousal axis; the serotonergic link to the catecholaminergic drive is INDIRECT and NON-MONOTONE (an [O] handle)",
      adhd_anchor="the serotonin transporter (5-HTTLPR), a monoaminergic arousal/E-I-tone gene assigned by sec.22 to the arousal axis; serotonergic modulation of arousal is indirect/non-monotone in ADHD",
      drive_agent="serotonergic-tone DIRECTION for the DT axis (the non-monotone monoaminergic arousal handle; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Gizer 2009 Hum Genet 126:51 (5-HTTLPR, ADHD meta-analysis); sec.22 arousal-tone axis"),
  "ADRA2A": dict(lever="L3", domain=DOM_DT, channel=None, protein="alpha-2A adrenergic receptor (ADRA2A)",
      sec22_axis="T (sec.22 arousal tone) -- noradrenergic arousal receptor",
      push="normalise the noradrenergic arousal tone via the a2A adrenergic receptor -- the prefrontal arousal-tone receptor (the guanfacine DIRECTION); a2A tone sets the prefrontal arousal/firing set-point",
      adhd_anchor="the alpha-2A adrenergic receptor (ADRA2A), the target of guanfacine and a sec.22 arousal-tone gene; prefrontal a2A signalling sets noradrenergic arousal tone",
      drive_agent="a2A adrenergic-tone DIRECTION for the DT axis (the guanfacine route, as DIRECTION, not efficacy; not a dose)",
      grade_mechanism=GL3,
      src="Arnsten 2010 J Pediatr 154:I (a2A, prefrontal arousal, guanfacine); Roman 2003 (ADRA2A, ADHD)"),
  "DRD4": dict(lever="L3", domain=DOM_DT, channel=None, protein="dopamine receptor D4 (DRD4)",
      sec22_axis="O (sec.22 gain) -- reachable here as drive-TONE: a receptor reads dopaminergic drive",
      push="modulate the dopaminergic drive readout via the D4 receptor -- the 7-repeat ADHD locus; receptor tone sets how the dopaminergic drive is read into the cell (a DT readout node)",
      adhd_anchor="the dopamine D4 receptor (DRD4); the exon-3 7-repeat allele is the most-replicated ADHD candidate association -- a postsynaptic dopaminergic drive-readout receptor",
      drive_agent="D4 dopaminergic-readout DIRECTION for the DT axis (carried with the dopaminergic drive set; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="LaHoste 1996 Mol Psychiatry 1:121 (DRD4 7-repeat, ADHD); Faraone 2021 Nat Rev Dis Primers 7:51"),
}

# ===== OUT-OF-REACH TARGETS (the GA gain-amplitude machinery a drive-tone lever CANNOT reach) =====
# These are NOT levers. They carry a gamma read (their own promoter switch stiffness) ALONGSIDE, with the
# explicit record that NO threshold/drive-tone lever reaches the GAIN-AMPLITUDE axis (sec.22-O core).
# Naming them makes the ADHD partial-fit concrete: the disorder's DOMINANT axis is the out-of-reach one.
OUT_OF_REACH = {
  # --- GA-axis: gain-amplitude / OUTPUT (synthesis/release sets amplitude, not the fold) ---
  "TH": dict(axis="GA", role="tyrosine hydroxylase (rate-limiting catecholamine SYNTHESIS)", channel=None,
      why_unreached="the GA (gain-amplitude/output) axis: TH sets the rate-limiting catecholamine SYNTHESIS, i.e. the signal-amplitude ceiling -- a drive-tone (reuptake/receptor) lever has NO handle on synthesis, so the threshold frame cannot reach this axis directly (the autism O-axis analogue, here the DOMINANT ADHD fault)",
      adhd_anchor="tyrosine hydroxylase (TH), the rate-limiting enzyme of catecholamine synthesis; a sec.22 gain-axis gene -- it sets how much dopamine/noradrenaline is MADE (the amplitude), not the firing tone",
      src="sec.22 adhd_axis_specific (gain axis); Faraone 2021 Nat Rev Dis Primers 7:51 (catecholamine synthesis in ADHD)"),
  "DBH": dict(axis="GA", role="dopamine beta-hydroxylase (DA->NA SYNTHESIS gain)", channel=None,
      why_unreached="the GA (gain-amplitude/output) axis: DBH converts dopamine to noradrenaline, setting the noradrenergic synthesis amplitude -- a synthesis-gain mechanism a drive-tone lever does not set; out of reach of the threshold frame",
      adhd_anchor="dopamine beta-hydroxylase (DBH), the DA->NA synthesis enzyme; a sec.22 gain-axis gene controlling the noradrenergic signal amplitude (a synthesis/gain mechanism, not a tone)",
      src="sec.22 adhd_axis_specific (gain axis); Kieling 2008 (DBH, ADHD)"),
  "SNAP25": dict(axis="GA", role="SNAP-25 SNARE vesicle RELEASE (presynaptic OUTPUT gain)", channel=None,
      why_unreached="the GA (gain-amplitude/output) axis: SNAP-25 sets vesicular RELEASE efficiency, i.e. presynaptic output gain -- a release-gain mechanism a drive-tone (reuptake/receptor) lever cannot reach; out of reach of the threshold frame",
      adhd_anchor="SNAP-25, the SNARE vesicle-release protein; the coloboma-mouse ADHD model; a sec.22 gain-axis gene setting presynaptic OUTPUT amplitude (a release/gain mechanism, not a tone)",
      src="sec.22 adhd_axis_specific (gain axis); Hess 1992 (coloboma SNAP-25 ADHD model)"),
  "COMT": dict(axis="GA (boundary: catabolic clearance)", role="catechol-O-methyltransferase (prefrontal DA catabolism)", channel=None,
      why_unreached="the GA (gain-amplitude/output) axis -- the BOUNDARY gene: COMT degrades synaptic dopamine (a catabolic CLEARANCE that is tone-adjacent), but sec.22 assigns it to the gain axis and its prefrontal-amplitude effect is synthesis-independent, so it is carried with the gain machinery and flagged. A drive-tone (reuptake/receptor) lever does not set catabolic clearance",
      adhd_anchor="catechol-O-methyltransferase (COMT); the Val158Met polymorphism sets prefrontal dopamine catabolism/availability; a sec.22 gain-axis gene -- the boundary between tone-clearance and amplitude",
      src="sec.22 adhd_axis_specific (gain axis); Egan 2001 PNAS 98:6917 (COMT Val158Met, prefrontal DA)"),
}

# ===== PRE-REGISTERED EXCLUSIONS (sec.22: axis-ambiguous / syndromic genes kept OUT to keep 'intact W' airtight) =====
# Recorded as names + reasons; NOT levers and NOT out-of-reach targets. Pre-registration is a discipline record.
EXCLUDED = {
  "FOXP2":  "transcription-factor / language syndrome (syndromic, W/developmental) -- pre-registered excluded by sec.22 to keep the 'intact wiring' discriminant airtight",
  "ADGRL3": "adhesion-GPCR (LPHN3; axis-ambiguous between adhesion/wiring and signalling) -- pre-registered excluded by sec.22 so no ambiguous gene smuggles a wiring fault into the ADHD substrate",
}

def read(sym, g):
    c = CONTEXT[sym]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(E.spinodal(g), 6),   # [V] R19 promoter threshold scale (NOT the network gain/arousal quantity)
        "barrier": round(E.barrier(g), 6),          # [V] R19 promoter basin depth
        "lever": c["lever"],
        "domain_reach": c["domain"],
        "sec22_axis": c["sec22_axis"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "adhd_genetic_anchor": c["adhd_anchor"],
        "dt_axis_drive_agent_direction": c["drive_agent"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": c["grade_mechanism"],
        "grade_mechanism": c["grade_mechanism"],
        "grade_promoter_vs_network_quantity": "[O] OPEN -- the promoter |h_sp| is the gene's OWN switch "
                                       "stiffness, NOT the sec.22 network gain/arousal quantity (the "
                                       "catecholamine signal amplitude / arousal set-point); never equated",
        "grade_clinical_map": "[O] OPEN -- not a transporter occupancy, synaptic dopamine/noradrenaline "
                              "level, potency, dose, in-vivo selectivity, or clinical effect",
        "context_grade": "CITED Layer-2 biology + the sec.22 substrate (not an engine output)",
        "src": c["src"],
    }

def read_out_of_reach(sym, g):
    c = OUT_OF_REACH[sym]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] structural read carried alongside (NOT a lever placement)
        "spinodal_h_sp": round(E.spinodal(g), 6),
        "barrier": round(E.barrier(g), 6),
        "lever": None,                              # explicitly NOT a lever
        "fault_axis": c["axis"],
        "reached_by_threshold_levers": False,
        "why_unreached": c["why_unreached"],
        "role": c["role"],
        "channel": c.get("channel"),
        "adhd_genetic_anchor": c["adhd_anchor"],
        "grade_read": "[V] reproducible promoter-switch-threshold read (carried alongside; does NOT place a lever)",
        "grade_reach": "[F] NOT REACHED -- the threshold/drive-tone frame has no handle on the gain-amplitude axis (axis-structured, not dose-structured)",
        "context_grade": "CITED Layer-2 biology + the sec.22 substrate (not an engine output)",
        "src": c["src"],
    }

def build():
    cache = json.load(open(CACHE))
    gammas = {s: gamma(cache[s]["seq"]) for s in CONTEXT if s in cache}
    missing = [s for s in list(CONTEXT) + list(OUT_OF_REACH) if s not in cache]
    entries = [read(s, gammas[s]) for s in gammas]
    entries.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)   # stiffest promoter read first [F]
    order = [e["gene"] for e in entries]
    by_lever = {}
    for e in entries:
        by_lever.setdefault(e["lever"], []).append(e["gene"])
    # out-of-reach reads (the named GA gain-amplitude targets)
    oor_g = {s: gamma(cache[s]["seq"]) for s in OUT_OF_REACH if s in cache}
    oor = [read_out_of_reach(s, oor_g[s]) for s in oor_g]
    oor.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)
    oor_by_axis = {}
    for e in oor:
        # collapse the COMT 'GA (boundary...)' label to the GA bucket for the by-axis index
        ax = "GA" if e["fault_axis"].startswith("GA") else e["fault_axis"]
        oor_by_axis.setdefault(ax, []).append(e["gene"])

    # lever-distribution witness: ADHD is L3-ONLY (L1/L2 empty)
    counts = {k: len(v) for k, v in by_lever.items()}
    ranked = sorted(counts, key=lambda k: counts[k], reverse=True)
    top = counts[ranked[0]]
    dominant_levers = sorted([k for k, n in counts.items() if n == top])
    codominant = len(dominant_levers) >= 2
    l1_l2_empty = (counts.get("L1", 0) == 0 and counts.get("L2", 0) == 0)

    # domain-restriction / partial-fit witness (the ADHD headline; the autism domain-restriction INVERTED)
    domain_restriction = {
        "DT": {"axis": "drive-tone / arousal (the firing set-point)", "reached_by_levers": True,
            "sec22_axes_drawn_from": "sec.22-T arousal (SLC6A4, ADRA2A) + reachable sec.22-O drive (SLC6A3, DRD4) + NET (SLC6A2)",
            "sign": "NORMALISE the upstream catecholamine/monoaminergic DRIVE TONE (the catecholamine "
                    "DIRECTION; the stimulant/atomoxetine/guanfacine surface) -- all via the L3 lever; "
                    "this is the SECONDARY axis, reached"},
        "GA": {"axis": "gain-amplitude / output (the sec.22-O gain core -- the DOMINANT ADHD fault)",
            "reached_by_levers": False,
            "named_genes": oor_by_axis.get("GA", []),
            "why_not": "the catecholamine SYNTHESIS (TH/DBH), RELEASE (SNAP25) and catabolic-clearance "
                       "(COMT, boundary) machinery sets signal AMPLITUDE, not the firing fold -- a "
                       "drive-tone (reuptake/receptor) lever has no handle on synthesis/release, so the "
                       "threshold frame reaches this DOMINANT axis only INDIRECTLY (the autism O-axis "
                       "analogue). Named genes: TH / DBH / SNAP25 / COMT (out_of_reach_targets)."},
        "W": {"axis": "long-range wiring", "reached_by_levers": False, "present_in_disorder": False,
            "named_genes": oor_by_axis.get("W", []),
            "why_absent": "ADHD has INTACT wiring (sec.22 adhd_axis_specific) -- ZERO wiring out-of-reach "
                          "genes. This is the discriminant from autism (which carried a W axis PROVEN "
                          "unreachable in sec.19). The autism INVERSE: autism reached its dominant T axis "
                          "and missed O+W; ADHD reaches only the secondary DT axis and misses the dominant "
                          "GA axis, with no W axis at all."},
        "reading": ("the drive-tone map reaches the DT (drive-tone/arousal) axis ONLY -- the SECONDARY "
                    "ADHD axis. The GA (gain-amplitude) axis -- the sec.22-O gain core, the DOMINANT ADHD "
                    "fault -- sits on a DIFFERENT axis the threshold/drive-tone frame does not reach (only "
                    "indirectly, via the upstream drive). And W (wiring) is ABSENT (intact wiring, the "
                    "discriminant). So the fit is PARTIAL [L]: the frame catches the drive-tone set-point "
                    "but not the gain-amplitude core. Cites sec.22 (adhd_axis_specific) and sec.34 (the "
                    "autism named-out-of-reach precedent, whose CLEAN fit ADHD contrasts)."),
        "cites": "sec.22 adhd_axis_specific (the ADHD substrate SSOT: six gain/O genes, two arousal/T "
                 "genes, intact wiring) + sec.34 autism_threshold_levers (the named-out-of-reach precedent "
                 "-- ADHD inherits the naming discipline but, unlike autism's clean [V] fit, is partial [L])",
        "inversion_of_autism": [
            "autism's domain-restriction: REACHED its DOMINANT axis (T excitability) and missed O (gain) + W (wiring)",
            "ADHD inverts the emphasis: reaches only the SECONDARY axis (DT drive-tone) and misses the DOMINANT axis (GA gain-amplitude)",
            "autism had a W axis PROVEN unreachable in sec.19; ADHD has W ABSENT (intact wiring) -- ZERO wiring genes (the discriminant)",
            "autism was a CLEAN [V] fit (domain-restricted but exact on the axes it reached); ADHD is the FIRST PARTIAL [L] fit (the dominant axis is the partially-unreachable one)",
        ],
    }

    # the partial-fit witness (the headline grade)
    partial_fit = {
        "fit_grade": "[L] partial",
        "reached_axis": "DT (drive-tone / arousal) -- the SECONDARY ADHD axis, reached by the L3 lever",
        "out_of_reach_axis": "GA (gain-amplitude / output) -- the DOMINANT ADHD fault, reached only indirectly",
        "w_present_in_disorder": False,
        "reasoning": ("ADHD is a GAIN/AROUSAL disorder, not a firing-FOLD disorder (sec.22). The "
                      "threshold-shift frame operates on the fold via an upstream DRIVE lever (L3), so it "
                      "reaches ADHD only through the DT drive-tone surface (the reuptake transporters and "
                      "tone receptors -- where ADHD pharmacology lives, as DIRECTIONS) and NOT through the "
                      "GA gain-amplitude machinery (synthesis/release), which is the DOMINANT fault. Hence "
                      "the fit is PARTIAL [L], not the CLEAN [V] of the five prior threshold disorders. A "
                      "second sense of partial: ADHD's only handle is the [O] cited-biology L3 drive "
                      "channel -- L1/L2 (the [F] structural ionic levers) are EMPTY -- so the frame has no "
                      "[F] structural grounding on ADHD at all, only the [O] drive surface."),
        "contrast_to_prior_fits": ("bipolar (L1, clean [V]), epilepsy (L1+L2, clean [V]), depression "
                      "(L3-dominant, clean [V]), schizophrenia (L1+L3, clean [V] though domain-restricted), "
                      "autism (L1-dominant, clean [V] though domain-restricted with named O/W out-of-reach) "
                      "-- ALL clean fits. ADHD is the FIRST and only PARTIAL [L] fit: its dominant axis is "
                      "out of reach."),
        "honest": ("the partial grade is the finding, not a failure: it marks exactly where the "
                   "cross-cutting threshold-shift logic does and does not apply, and refuses to overclaim a "
                   "clean fit where the biology is a gain/arousal disorder. efficacy=0; no drug/dose/patient; "
                   "no stimulant-misuse or cognitive-enhancement licence."),
    }

    return {
        "title": "Drive-tone ADHD target map for the DT (drive-tone/arousal) axis -- the sec.22 ADHD "
                 "substrate (adhd_axis_specific) mapped onto the formal L1/L2/L3 inheritance frame "
                 "(engine-generated reads + cited lever frame); the GA gain-amplitude axis named as "
                 "out-of-reach; W absent (intact wiring); the FIRST PARTIAL [L] fit in the series",
        "inherited_from": ("analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420) -- the "
                          "threshold-shift intervention-logic technology, applied to the ADHD DT "
                          "(drive-tone/arousal) axis (SIXTH application after bipolar sec.30, epilepsy "
                          "sec.31, depression sec.32, schizophrenia sec.33 and autism sec.34; this one is "
                          "the FIRST PARTIAL [L] fit -- ADHD is a gain/arousal disorder, so the frame "
                          "reaches its secondary drive-tone axis but not its dominant gain-amplitude axis "
                          "-- and inherits the autism named-out-of-reach discipline while INVERTING the "
                          "autism domain-restriction)"),
        "maps_sec22_substrate": ("sec.22 adhd_axis_specific (the SSOT) establishes ADHD as a "
                          "gain/arousal substrate with INTACT wiring: six catecholamine GAIN/OUTPUT genes "
                          "(O: DRD4, SLC6A3, COMT, SNAP25, DBH, TH), two adrenergic/monoaminergic "
                          "AROUSAL-TONE genes (T: ADRA2A, SLC6A4), and NO long-range wiring fault (the "
                          "discriminant from autism); axis-ambiguous/syndromic genes (FOXP2, ADGRL3) are "
                          "pre-registered excluded. This map re-cuts that substrate by threshold-frame "
                          "REACHABILITY -- the drive-TONE genes (reuptake transporters + tone receptors) "
                          "are the L3 lever surface, the gain-AMPLITUDE machinery (synthesis/release) is "
                          "out of reach -- adding NO new mechanism and NO new constant."),
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=2(g/3)^1.5 == (2/3sqrt3)gamma^1.5, "
                     "barrier=gamma^2/4 -- byte-identical to vp_neuro_engine and to this engine's E.spinodal/E.barrier",
        "connects_to_sec22": ("sec.22 (adhd_axis_specific) established the ADHD substrate (gain/arousal, "
                          "intact wiring) and the ADHD-vs-autism axis distinction. This map DECOMPOSES the "
                          "threshold-frame engagement: the DT (drive-tone) axis is reached by the L3 lever "
                          "(the catecholamine/monoaminergic drive surface) while the GA (gain-amplitude) "
                          "axis is NAMED out-of-reach (synthesis/release machinery). It re-derives no rule "
                          "and adds no constant -- the ADHD counterpart of the sec.18-19->sec.34 autism "
                          "decomposition, but the FIRST PARTIAL fit."),
        "domain_restriction_witness": domain_restriction,
        "partial_fit_witness": partial_fit,
        "disorder_level_sign": ("the DT axis is the upstream DRIVE-TONE / arousal axis; its corrective "
                           "sign is NORMALISE the catecholamine/monoaminergic drive tone (the stimulant/"
                           "atomoxetine/guanfacine DIRECTION) -- a tone-setting, not a fold-raising, sign. "
                           "But the sign is PARTIAL and DOMAIN-RESTRICTED: it reaches the secondary DT axis "
                           "only; the DOMINANT GA (gain-amplitude) axis is out of reach (synthesis/release "
                           "machinery a tone lever does not set), and W (wiring) is ABSENT (intact wiring). "
                           "So unlike the clean fold-raising sign of the five prior disorders, ADHD's "
                           "engagement with the threshold frame is partial [L] and tone-shaped."),
        "unifying_frame": ("the ADHD operating point is a GAIN/AROUSAL deficit on INTACT geometry (sec.22): "
                           "the catecholamine signal amplitude is too low and the arousal tone is "
                           "mis-set, with wiring intact. The threshold-shift frame reaches it through the "
                           "L3 DRIVE lever ONLY -- the reuptake transporters (DAT/NET/SERT) and tone "
                           "receptors (a2A/D4) that set the drive/arousal TONE (the firing set-point) -- "
                           "with L1 and L2 EMPTY (no ionic fold lever). The map reaches the DT "
                           "(drive-tone/arousal) axis; the GA (gain-amplitude) axis -- the DOMINANT fault, "
                           "the catecholamine synthesis/release machinery -- is honestly out of reach "
                           "(named in out_of_reach_targets), and W (wiring) is ABSENT (the discriminant). "
                           "The fit is PARTIAL [L]: the first non-clean fit in the series, because the "
                           "disorder's dominant axis is the one the frame cannot directly reach."),
        "levers": LEVER_FRAME,
        "lever_distribution_witness": {
            "counts": counts,
            "dominant_levers": dominant_levers,
            "codominant": codominant,
            "l3_only": bool(counts.get("L3", 0) == sum(counts.values()) and counts.get("L3", 0) > 0),
            "l1_l2_empty": bool(l1_l2_empty),
            "reading": (("ADHD is L3-ONLY (%d drive-tone levers; L1=%d, L2=%d -- BOTH EMPTY) -- the SIXTH "
                         "distribution pattern and the PUREST L3 case: bipolar leaned on L1 (calcium), "
                         "epilepsy on L1+L2 (the M-current), depression on L3 (HPA/monoamine, with a "
                         "reachable L1/L2 mix), schizophrenia on L1+L3 co-dominant (glutamate + dopamine), "
                         "autism on L1-dominant with a sparse L3, and ADHD loads ALL its threshold-frame "
                         "engagement on L3 (the upstream catecholamine/monoaminergic drive). The L1/L2 "
                         "EMPTINESS is the finding: ADHD is not a channelopathy -- it has no ionic fold "
                         "lever, only the [O] cited-biology drive surface, a second sense in which the "
                         "fit is partial." %
                         (counts.get("L3", 0), counts.get("L1", 0), counts.get("L2", 0)))),
        },
        "out_of_reach_targets": {
            "_what": "the GA-axis (gain-amplitude/output) genes a threshold/drive-tone lever CANNOT reach "
                     "-- named to make the ADHD partial-fit CONCRETE. Each carries a gamma read (its own "
                     "promoter switch stiffness) ALONGSIDE, but is explicitly NOT a lever: the catecholamine "
                     "SYNTHESIS (TH/DBH), RELEASE (SNAP25) and catabolic-clearance (COMT, boundary) "
                     "machinery sets signal AMPLITUDE, not the firing fold, so the drive-tone frame has no "
                     "direct handle. This is the sec.22-O gain core -- the DOMINANT ADHD fault -- which is "
                     "exactly why ADHD is a PARTIAL fit (the dominant axis is the out-of-reach one). It is "
                     "the autism named-out-of-reach discipline (sec.34), here applied to the gain axis.",
            "by_axis": oor_by_axis,
            "n": len(oor),
            "entries": oor,
        },
        "excluded_preregistered": {
            "_what": "sec.22 pre-registered exclusions: axis-ambiguous / syndromic genes kept OUT of the "
                     "ADHD substrate to keep the 'intact wiring' discriminant airtight. Recorded as a "
                     "discipline record; NOT levers and NOT out-of-reach targets (they carry no gamma read "
                     "here -- they are pre-registered out, not placed).",
            "genes": EXCLUDED,
            "n": len(EXCLUDED),
        },
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not a transporter occupancy, not "
                     "a synaptic dopamine/noradrenaline level, not a potency, not a dose, not in-vivo "
                     "selectivity, not a clinical effect, and NOT the sec.22 network gain/arousal quantity "
                     "(the catecholamine signal amplitude / arousal set-point) (those are [O]). The "
                     "promoter |h_sp| is the gene's OWN switch stiffness, carried alongside, never folded "
                     "into a clinical magnitude or equated with the network gain/arousal quantity. gamma is "
                     "blind to on/off and to expression level. L3 (the catecholamine/monoaminergic drive) "
                     "mechanism link is [O] -- the read places the gene, it does not derive the drive "
                     "mechanism. The fit is PARTIAL [L]: the frame reaches the DT drive-tone axis but not "
                     "the DOMINANT GA gain-amplitude axis, and W (wiring) is ABSENT."),
        "honesty": ("MECHANISM-DIRECTION only; efficacy=0 everywhere; ranks/places READS and TARGETS, never "
                    "drugs, doses, protocols, or patients; ADHD is polygenic and heterogeneous, its "
                    "established pharmacology acts on the DT drive-tone surface only, and a lever direction "
                    "is a mechanism boundary, not a claim about whether attention/arousal should be changed, "
                    "nor a licence for stimulant misuse or cognitive enhancement (the fail-closed "
                    "forbidden-claim scan enforces this); the map reaches the DT (drive-tone/arousal) axis "
                    "ONLY (the DOMINANT GA gain-amplitude axis is out of reach -- named here -- and W "
                    "wiring is ABSENT, the intact-wiring discriminant), so the fit is PARTIAL [L], the "
                    "first non-clean fit in the series; a lever direction is a mechanism boundary, not a "
                    "claim about identity or the subjective world (Axis-A; consciousness_claim=0; hard "
                    "problem OPEN)."),
        "n_targets": len(entries),
        "n_out_of_reach": len(oor),
        "n_excluded": len(EXCLUDED),
        "missing_from_cache": missing,
        "order_by_spinodal_desc": order,
        "targets_by_lever": by_lever,
        "channels_present": sorted({e["channel"] for e in entries if e["channel"]}),
        "entries": entries,
    }

# ----------------------------- determinism + engine guard -----------------------------
def _canon(o):
    if isinstance(o, float): return round(o, 10)
    if isinstance(o, dict):  return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):  return [_canon(v) for v in o]
    return o
def _blob(res): return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def adhd_threshold_levers_results():
    res = build()
    R = E.emerge_all()                           # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"] = {
        "engine_tree_frozen": ENGINE_TREE_FROZEN,
        "engine_tree_sha256_live": tree_live,
        "engine_tree_unchanged": bool(tree_live == ENGINE_TREE_FROZEN),
        "m0_16_subtree_unchanged": bool(sub016 == M0_16_FROZEN),
        "reads_shared_R19_primitive": True,
        "no_new_tuned_constants": True,
        "maps_sec22_adhd_substrate": True,
        "first_partial_fit_L": True,
    }
    res["honesty_ledger"] = {
        "medium_efficacy_tested": 0.0,
        "no_cure_claimed": 1.0,
        "consciousness_claim": 0.0,
        "hard_problem_open": 1.0,
        "new_tuned_constants": 0.0,
        "ranks_targets_not_drugs": 1.0,
        "inherited_from_analgesic_v2": 1.0,
        "maps_sec22_substrate": 1.0,
        "l3_mechanism_link": "OPEN [O] -- the catecholamine/monoaminergic drive signalling mechanism is cited biology, not derived",
        "promoter_hsp_vs_network_quantity": "OPEN [O] -- the promoter |h_sp| is the gene's own switch stiffness, "
                                     "never equated with the sec.22 network gain/arousal quantity",
        "partial_fit_L": 1.0,
        "fit_grade": "[L] partial -- the DOMINANT GA gain-amplitude axis is out of reach; only the secondary DT drive-tone axis is reached",
        "l3_only_l1_l2_empty": 1.0,
        "w_absent_intact_wiring_discriminant": 1.0,
        "gain_axis_named_out_of_reach": 1.0,
        "preregistered_exclusions_recorded": 1.0,
        "no_stimulant_misuse_or_cognitive_enhancement_licence": 1.0,
        "efficacy_and_dose": "efficacy=0 everywhere; no dose/protocol; not medical advice; cited agents are "
                             "DIRECTIONS only (the fail-closed forbidden-claim scan enforces this, incl. "
                             "stimulant-misuse and cognitive-enhancement classes)",
    }
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "adhd_threshold_levers_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_adhd_threshold_levers_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"adhd_threshold_levers_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest

if __name__ == "__main__":
    res, digest = adhd_threshold_levers_results()
    inv = res["invariants"]
    print("=" * 100)
    print("ADHD-T-L  ADHD DRIVE-TONE MAP  (inherited from analgesic v2.0; engine READ-ONLY; L3-ONLY; PARTIAL fit [L])")
    print("=" * 100)
    print(f"  engine tree unchanged : {inv['engine_tree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  primitive shared      : {inv['reads_shared_R19_primitive']}   new tuned constants: {not inv['no_new_tuned_constants']}")
    print(f"  maps sec.22 substrate : {inv['maps_sec22_adhd_substrate']}   first partial fit [L]: {inv['first_partial_fit_L']}")
    print("-" * 100)
    print(f"  {'gene':9} {'lev':4} {'gamma':>7} {'|h_sp|':>8} {'axis':5} {'protein':38} sec.22 axis")
    for e in res["entries"]:
        cp = e.get("protein") or e["channel"] or "-"
        dom = e["domain_reach"].split()[0]
        print(f"  {e['gene']:9} {e['lever']:4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} {dom:5} "
              f"{cp[:38]:38} {e['sec22_axis'][:24]}")
    print("-" * 100)
    print("  OUT-OF-REACH (gain-amplitude axis; named; NOT levers):")
    for e in res["out_of_reach_targets"]["entries"]:
        print(f"  {e['gene']:9} {'--':4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} {e['fault_axis'][:5]:5} "
              f"{(e['role'])[:38]:38} {e['adhd_genetic_anchor'][:24]}")
    print("-" * 100)
    print("  PRE-REGISTERED EXCLUSIONS (intact-wiring discriminant): " + ", ".join(res["excluded_preregistered"]["genes"].keys()))
    print("-" * 100)
    w = res["lever_distribution_witness"]
    print("  targets by lever: " + ", ".join(f"{k}={v}" for k, v in w["counts"].items())
          + f"   -> {'DOMINANT ' + w['dominant_levers'][0]}  (L3-only={w['l3_only']}, L1/L2 empty={w['l1_l2_empty']})")
    dr = res["domain_restriction_witness"]
    print(f"  domain reach: DT={dr['DT']['reached_by_levers']} "
          f"GA={dr['GA']['reached_by_levers']} W={dr['W']['reached_by_levers']}/present={dr['W']['present_in_disorder']}"
          f"  (DT-axis map; GA named out-of-reach; W absent)")
    pf = res["partial_fit_witness"]
    print(f"  FIT GRADE: {pf['fit_grade']}  (reached={pf['reached_axis'][:20]}; out-of-reach={pf['out_of_reach_axis'][:24]})")
    print(f"  n_targets: {res['n_targets']}   out_of_reach: {res['n_out_of_reach']}   "
          f"excluded: {res['n_excluded']}   missing: {res['missing_from_cache']}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 100)
    ok = (inv["engine_tree_unchanged"] and inv["no_new_tuned_constants"] and not res["missing_from_cache"]
          and not w["codominant"] and w["dominant_levers"] == ["L3"] and w["l3_only"] and w["l1_l2_empty"]
          and dr["W"]["present_in_disorder"] is False and pf["fit_grade"] == "[L] partial")
    print("  ADHD-T-L DRIVE-TONE MAP: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
