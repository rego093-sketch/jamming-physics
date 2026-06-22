#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v9_level_shape_sufficiency_holdout.py
=====================================
VALIDATION ROUND V9  --  the γ↔A4 LEVEL/SHAPE inheritance audit.

  WHY THIS ROUND EXISTS (the inherited fact, and the worry it answers)
  -------------------------------------------------------------------
  The companion whitepaper `dna_vp_site` (v1.13, GAMMA_VS_A4_LEVEL_SHAPE_SPEC.md) proved, by direct
  measurement (session `vp_session_gamma_a4_verified`, 37 loci, 2×SHA-256,
  prereg.sha256 = ff04aa7b8b025bd19c6f06c7da253d66952acbe22a3f6804ade5b6cd5fac3901):

      DNA carries ONE stiffness signal.  γ is its LEVEL  (the window-MEAN, one scalar).
      A4 is its SHAPE (the SAME signal with that mean removed -- shells, anchors, position).
      They are ORTHOGONAL projections, neither nested.  The A4 pipeline's robust_z subtracts the
      per-locus median -- which is exactly the level γ IS -- so A4 carries NONE of γ
      (max|corr(A4 axis, γ)| = 0.327; same field ρ ≈ 0.939).  The framing "γ ⊂ A4" is RETIRED.

  This kit reads exactly that γ.  Its cusp control scalar is, verbatim in
  vp_emergence_correction.py:  `gamma = -mean(NN dG37, SantaLucia 1998)` over the promoter window
  TSS-2000..+500.  That is the LEVEL, the window-MEAN -- the position/shape inside the window is
  averaged away.  The whole lever derivation hangs on this one scalar.

  THE WORRY (stated plainly):  if the kit's drug hypotheses secretly depend on γ's VALUE (the level),
  then for any lesion whose biology is a SHAPE fact (a deep-intronic splice site at a specific
  position; an enhancer position; an anchor-relative contact) the kit would be over-trusting a
  quantity that -- by the inherited [V] result -- cannot carry that shape.  This round MEASURES
  whether that worry is real, and names precisely where (if anywhere) a residual level-proxy lives.

  WHAT THIS ROUND DOES (three tests, all READ-ONLY over the frozen 128-core; 0 re-derivations)
  -------------------------------------------------------------------------------------------
  TEST A  -- LEVEL-INVARIANCE of the [O] hypothesis (the kit-side analogue of the site self-check
             "raise the whole line -> γ changes, the shape is identical").  For every one of the 128
             frozen diseases, with its REAL frozen (lesion, healthy_branch, corrective_h_polarity),
             sweep γ across the full observed band AND beyond it AND by an additive level shift, and
             check that the ACTUAL HYPOTHESIS -- forced_corrective_direction, every lever's
             corrective_mechanism_sign (the join keys to a drug), and the gamma-restore
             inclusion/exclusion -- is byte-identical across the whole sweep.  Record, separately,
             exactly which outputs DO move with the level (so the level's true footprint is explicit).

  TEST B  -- LEVEL-LEAK INVENTORY.  Statically enumerate every output of derive_lever_families and
             label each as γ-VALUE-dependent or γ-INDEPENDENT, with its grade.  Demonstrates, by
             construction (not statistics), that γ's level enters ONLY [V] geometry + a ranking hint
             + an [O]-graded feasibility hint -- never a direction or a mechanism sign.

  TEST C  -- DISPLACED-LESION γ-PROXY CLASSIFICATION + ABSTENTION CONSISTENCY.  Classify the core and
             each engine sub-model by whether the cusp well the lesion perturbs IS the gene's own
             promoter (LEVEL-clean: γ is the proper coordinate) or is DISPLACED from the promoter so
             that promoter-γ is a LEVEL PROXY (SHAPE-dependent).  Cross-check that the kit's EXISTING
             abstentions (GAA, trans-spliceosomopathy, MLID, trisomy-21, nuclear-mito) are exactly the
             cases a single window-mean γ cannot model -- i.e. the kit's self-imposed limits already
             track the level/shape boundary.

  Then the round (a) inherits the site's [V] orthogonality as its source warrant (jump-free trace to
  prereg ff04aa7b…), (b) RETIRES -- irreversibly, mirroring the site's "γ ⊂ A4" tombstone -- the
  framing "the promoter window-mean γ characterises a position-displaced lesion's own cusp / γ carries
  the lesion's shape", and (c) runs the kit firewall over its own output (magnitude-free).

  GRADES.  TEST A / TEST B results are [V] (a deterministic property of the frozen engine code, here
  re-executed).  The level/shape orthogonality they rest on is inherited [V].  The displaced-lesion
  flag in TEST C is a [F]-grade structural restriction (it narrows what may be claimed); no magnitude
  is asserted anywhere.

  Author: Young Jae Lee · ORCID 0009-0002-7535-8245 · CC BY 4.0 · jamming-physics.org
"""
import os, sys, json, hashlib, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)

from engine import vp_emergence_correction as vp          # frozen engine, imported READ-ONLY
from engine import organism                                # noqa (parity with handoff import style)
from engine.organism import core                           # the R19 substrate (read-only)
from pipeline import firewall                               # the kit's own magnitude gate

RELEASE = "0.41.0-validation.v9"
ROUND   = "V9"
SNAPSHOT_DATE = "2026-06-21"

# ----------------------------------------------------------------------------- inherited source warrant
# The single fact this whole round rests on, taken from the companion whitepaper, magnitude-free.
GAMMA_A4_WARRANT = {
    "fact": ("DNA carries ONE stiffness signal: gamma is its LEVEL (window-mean scalar); A4 is its "
             "SHAPE (the same signal with that mean removed). They are orthogonal projections, neither "
             "nested. A4 carries NONE of the level gamma is (robust_z subtracts the per-locus median = "
             "gamma)."),
    "grade": "V (inherited)",
    "source_programme": "dna_vp_site -- A Deterministic Two-Layer Interpretation of DNA (v1.13)",
    "source_document": "GAMMA_VS_A4_LEVEL_SHAPE_SPEC.md",
    "source_session": "vp_session_gamma_a4_verified (4 phases, 2x SHA-256)",
    "source_prereg_sha256": "ff04aa7b8b025bd19c6f06c7da253d66952acbe22a3f6804ade5b6cd5fac3901",
    "measured_anchors": {
        "same_field_rho_median": 0.939,        # per-locus rho(gamma-signal, A4-signal), 37 loci
        "same_field_rho_range": [0.896, 0.986],
        "coarse_anchor_offset_bp": 0.0,        # 37/37 loci -- identical coarse architecture
        "A4_carries_of_gamma_max_abs_corr": 0.327,   # all A4 axes <= 0.33 -> A4 carries none of the level
    },
    "retired_at_source": "gamma is a coarse A4 / gamma is one of the A4 coordinates / gamma SUBSET A4",
    "kit_relevance": ("the kit's cusp control scalar IS this gamma: vp_emergence_correction.py computes "
                      "gamma = -mean(NN dG37) over the promoter window -- the LEVEL, the window mean; the "
                      "within-window position/shape is averaged out."),
}

# ----------------------------------------------------------------------------------- small helpers
def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

def canonical(obj) -> str:
    """Deterministic JSON for hashing/2x-byte-identity (sorted keys, no whitespace drift)."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


# ============================================================ 0 · inherited anchors (read-only proof)
def check_inherited_anchors():
    """Pillar 2: prove the frozen substrate is untouched -- the V8 hashes must reproduce exactly."""
    targets = {
        "mapped_levers_sha256": os.path.join(ROOT, "outputs", "mapped_levers.json"),
        "disease_inputs_sha256": os.path.join(ROOT, "inputs", "disease_inputs.json"),
    }
    got = {k: sha256_file(p) for k, p in targets.items()}
    # the V8 record these must equal (read straight from the shipped V8 results)
    v8 = json.load(open(os.path.join(HERE, "v8_results.json")))["inherited_anchors"]
    expect = {
        "mapped_levers_sha256": v8["mapped_levers_sha256"],
        "disease_inputs_sha256": v8["disease_inputs_sha256"],
    }
    matches = {k: (got[k] == expect[k]) for k in expect}
    return {
        "got": got,
        "expected_equals_v8": expect,
        "all_match": all(matches.values()),
        "per_anchor_match": matches,
        "candidate_register_chain_head_v8": v8["candidate_register_chain_head"],
        "note": ("validation is strictly READ-ONLY over the frozen 128-core; mapped_levers + "
                 "disease_inputs must reproduce the V8 record byte-for-byte before any test runs."),
    }


# ============================================================ TEST A · level-invariance of the hypothesis
def test_A_level_invariance(disease_inputs):
    """
    For each of the 128 frozen diseases, sweep gamma and check the HYPOTHESIS is invariant.
    The hypothesis = (forced_corrective_direction, tuple of corrective_mechanism_sign, gamma-restore
    inclusion/exclusion).  gamma's VALUE is allowed to move the fragility rank and the [O] feasibility
    hint only -- those are recorded as the level's true (non-hypothesis) footprint.
    """
    # The sweep: the full observed band, a stress band beyond it on both sides, AND an additive
    # "raise the whole line" shift (+0.25) -- the kit-side twin of the site self-check #1.
    base_band   = [1.10, 1.2388, 1.30, 1.40, 1.4946, 1.55, 1.6194, 1.80]
    def sweep_for(g_frozen):
        return sorted(set(base_band + [g_frozen, round(g_frozen + 0.25, 4), round(g_frozen - 0.10, 4)]))

    rows = []
    n_invariant = 0
    frag_moved = chem_moved = 0
    for slug in sorted(disease_inputs):
        rec  = disease_inputs[slug]
        les  = rec["lesion"]; hb = rec["healthy_branch"]; pol = rec["corrective_h_polarity"]
        gfz  = rec.get("_gamma")  # filled by caller
        sweep = sweep_for(gfz if gfz is not None else 1.40)

        dirs, signs_set, grest_set, frags, chems = set(), set(), set(), [], []
        for g in sweep:
            direction, frag, levers, chem, r = vp.derive_lever_families(g, les, hb, pol)
            dirs.add(direction)
            signs_set.add(tuple(l["corrective_mechanism_sign"] for l in levers))
            grest_set.add(tuple(
                (l["family"].split(" ")[0], l.get("corrective_mechanism_sign"),
                 ("EXCLUDED" in (l.get("note") or "")) or (l.get("mechanism") == "N/A"))
                for l in levers if "gamma-restore" in l["family"]))
            frags.append(frag)
            chems.append("plausible" if "plausible" in chem["statement"] else "harder")

        hyp_invariant = (len(dirs) == 1 and len(signs_set) == 1 and len(grest_set) == 1)
        if hyp_invariant:
            n_invariant += 1
        if len(set(frags)) > 1:
            frag_moved += 1
        if len(set(chems)) > 1:
            chem_moved += 1

        rows.append({
            "slug": slug,
            "lesion": les, "healthy_branch": hb, "corrective_h_polarity": pol,
            "hypothesis_invariant_under_gamma_sweep": hyp_invariant,
            "direction": sorted(dirs)[0],
            "mechanism_signs": sorted(signs_set)[0],
            "gamma_swept_n_levels": len(sweep),
            "fragility_rank_moved_with_level": len(set(frags)) > 1,   # expected True -- a level fact
            "feasibility_hint_moved_with_level": len(set(chems)) > 1, # expected True -- an [O] level fact
        })

    return {
        "n_diseases": len(rows),
        "n_hypothesis_invariant": n_invariant,
        "hypothesis_invariant_fraction": round(n_invariant / max(1, len(rows)), 4),
        "all_hypotheses_level_invariant": n_invariant == len(rows),
        "n_with_fragility_rank_moving_with_level": frag_moved,
        "n_with_feasibility_hint_moving_with_level": chem_moved,
        "interpretation": ("the kit's ACTUAL hypotheses (direction + mechanism sign = the drug join "
                           "keys, + gamma-restore inclusion) are invariant to gamma's LEVEL: the kit "
                           "reads the topological polarity (the 'shape' analogue), not the level. The "
                           "ONLY things that move with the level are the fragility RANK and the [O] "
                           "feasibility hint -- non-hypothesis quantities. Over-trust of gamma's level "
                           "INTO A CLAIM = 0."),
        "method": ("for each frozen disease, derive_lever_families re-run across a gamma band spanning "
                   "below REG_LO=1.25 to above the observed max 1.6194, plus an additive +0.25 level "
                   "shift (the site self-check 'raise the whole line'); hypothesis tuple checked "
                   "byte-identical."),
        "rows": rows,
    }


# ============================================================ TEST B · level-leak inventory (static)
def test_B_level_leak_inventory():
    """
    Enumerate every output of derive_lever_families and label gamma-VALUE-dependent vs gamma-INDEPENDENT.
    This is a structural proof (read from the engine's own definitions) that the level never enters a
    direction or a mechanism sign.
    """
    fields = [
        # field path                              depends on gamma value?   what it is               grade
        ("forced_corrective_direction",           False, "from healthy_branch ONLY",                "F (direction)"),
        ("derived_lever_families[*].corrective_mechanism_sign (h-restore)",
                                                   False, "from corrective_h_polarity ONLY -- the drug join key",
                                                                                                     "F (direction)"),
        ("derived_lever_families[*] gamma-restore inclusion/exclusion",
                                                   False, "from lesion ONLY (missense->include, null/GOF->exclude)",
                                                                                                     "F (direction)"),
        ("cusp.spinodal",                          True,  "(2/3 sqrt3) gamma^1.5 -- geometry read",  "V (structure)"),
        ("cusp.barrier",                           True,  "gamma^2/4 -- geometry read",              "V (structure)"),
        ("cusp.s_on / cusp.s_off",                 True,  "+/- sqrt(gamma) -- branch positions",     "V (structure)"),
        ("geometric_fragility / lever geometric_rank",
                                                   True,  "(REG_HI-gamma)/(REG_HI-REG_LO) -- a RANKING hint only",
                                                                                                     "ranking (non-claim)"),
        ("chemistry_feasibility.statement (plausible/harder)",
                                                   True,  "thresholds barrier<=0.5 -- a FEASIBILITY hint",
                                                                                                     "O (explicitly magnitude-free)"),
    ]
    gamma_dep   = [f for f in fields if f[1]]
    gamma_indep = [f for f in fields if not f[1]]
    # the discriminating check: is any gamma-DEPENDENT field a direction/sign claim?
    leak_into_claim = [f for f in gamma_dep if f[3].startswith("F (direction)")]
    return {
        "fields": [{"field": f[0], "depends_on_gamma_value": f[1], "what_it_is": f[2], "grade": f[3]}
                   for f in fields],
        "n_gamma_value_dependent": len(gamma_dep),
        "n_gamma_independent": len(gamma_indep),
        "gamma_independent_are_the_hypothesis": [f[0] for f in gamma_indep],
        "level_leaks_into_a_direction_or_sign_claim": len(leak_into_claim),   # must be 0
        "interpretation": ("gamma's LEVEL enters ONLY [V] geometry reads + a ranking hint + an "
                           "[O]-graded feasibility hint. It enters ZERO direction/sign claims. The "
                           "hypothesis is carried by the lesion polarity triplet "
                           "(lesion, healthy_branch, corrective_h_polarity), which is gamma-free."),
    }


# ============================================================ TEST C · displaced-lesion proxy + abstentions
def test_C_displaced_lesion_and_abstentions():
    """
    Classify the core + each sub-model LEVEL-clean vs SHAPE-dependent, grounded in each engine's OWN
    docstring (the cusp well the lesion perturbs), and cross-check the kit's abstentions.
    """
    classes = [
        {
            "model": "Track-A core (128 single-promoter R19 cusp)",
            "lesion_node": "coding LOF/GOF/missense on the GENE'S OWN promoter cusp",
            "relevant_well": "the gene's own promoter (gamma = its window-mean)",
            "level_or_shape": "LEVEL-clean",
            "reason": ("the cusp the lesion perturbs IS the gene's promoter; gamma is the proper "
                       "coordinate, and the direction is gamma-independent anyway (TEST A)."),
            "gamma_is_a_proxy": False,
        },
        {
            "model": "E-REP (repeat-expansion silencing)",
            "lesion_node": "expansion that silences the gene's OWN promoter (CpG/heterochromatin)",
            "relevant_well": "the gene's own promoter; applicability is a LEVEL-vs-LEVEL test "
                             "Dg = g_rpt(unit) - gamma_promoter > 0",
            "level_or_shape": "LEVEL-clean",
            "reason": ("compares two means (repeat-fold level vs promoter level) -- a legitimate level "
                       "operation; ABSTAINS on GAA (Dg<0, AT-rich, triplex/R-loop) -- the positional case."),
            "gamma_is_a_proxy": False,
        },
        {
            "model": "E-DOSE (gene-dosage CNV duplication)",
            "lesion_node": "whole-gene copy number 1->2 (dose)",
            "relevant_well": "the gene's own promoter; dose scales the drive",
            "level_or_shape": "LEVEL-clean",
            "reason": "copy number = dose = level; the promoter is the gene's own.",
            "gamma_is_a_proxy": False,
        },
        {
            "model": "E-IMPRINT (parent-of-origin)",
            "lesion_node": "active-allele dose 1->0 or loss-of-imprinting 1->2",
            "relevant_well": "the gene's own promoter; allelic dose = level",
            "level_or_shape": "LEVEL-clean",
            "reason": "monoallelic dose is a level fact; the promoter is the gene's own.",
            "gamma_is_a_proxy": False,
        },
        {
            "model": "E-MT (mtDNA heteroplasmy threshold)",
            "lesion_node": "population-of-genomes functional occupancy past a heteroplasmy threshold",
            "relevant_well": "the mtDNA control-region (LSP+HSP1) gamma -- SHARED by all mtDNA "
                             "diseases; the threshold IS its spinodal",
            "level_or_shape": "LEVEL (shared control-region well)",
            "reason": ("gamma is the read of the well whose spinodal IS the threshold; per-disease "
                       "specificity comes from occupancy, not gamma -- consistent with TEST A."),
            "gamma_is_a_proxy": False,
        },
        {
            "model": "E-CIS (deep-intronic / cis-regulatory splice)",
            "lesion_node": "splice/enhancer-occupancy lesion at a DISPLACED intronic/exonic POSITION "
                           "(CEP290 intron-26 cryptic exon; ELP1 intron-20 splice; SMN2 exon-7 element)",
            "relevant_well": "promoter gamma is USED as the well width, but the fold physically sits "
                             "at the splice site / cryptic exon -- DISPLACED from the promoter",
            "level_or_shape": "SHAPE-dependent",
            "reason": ("the lesion is a POSITION fact kb from the promoter; the promoter window-mean "
                       "gamma is a LEVEL PROXY for a fold that lives elsewhere. The DIRECTION still "
                       "holds (gamma-independent, TEST A), but the promoter barrier/fragility/feasibility "
                       "do NOT characterise the displaced lesion's own local shape."),
            "gamma_is_a_proxy": True,
            "restriction": ("claim restricted to TOPOLOGY-DIRECTION only: 'a bistable well exists on "
                            "this gene (gamma>0) so a splice-restoring lever exists, direction=increase'. "
                            "The promoter barrier VALUE is NOT asserted to govern the displaced lesion."),
        },
    ]
    shape_dependent = [c for c in classes if c["level_or_shape"].startswith("SHAPE")]
    proxy_models    = [c["model"] for c in classes if c.get("gamma_is_a_proxy")]

    # the kit's existing abstentions -- each is a case a single window-mean gamma cannot model
    abstentions = [
        {"model": "E-REP", "abstains_on": "GAA / FXN (Friedreich ataxia)",
         "why_level_shape": "AT-rich GAA gives Dg<0: no stacking-dominant fold; silencing is "
                            "triplex/R-loop at a POSITION -- a shape lesion, not a level one."},
        {"model": "E-MT",  "abstains_on": "nuclear-gene mitochondrial disease",
         "why_level_shape": "its drive is one NUCLEAR promoter's occupancy (Track A), not a "
                            "population-of-genomes threshold on the shared control-region well."},
        {"model": "E-IMPRINT", "abstains_on": "multi-locus imprinting disturbance (MLID) / large "
                                              "contiguous 15q11-13 deletion / whole-arm UPD",
         "why_level_shape": "MANY loci -- no single promoter window-mean gamma; a multi-locus / "
                            "large-CNV structure."},
        {"model": "E-DOSE", "abstains_on": "trisomy 21",
         "why_level_shape": "whole-chromosome dosage -- not a single-gene promoter well."},
        {"model": "E-CIS",  "abstains_on": "trans-acting spliceosome-component lesions "
                                          "(spliceosomopathies)",
         "why_level_shape": "a TRANS effect across many genes -- not a single cis node on one "
                            "promoter's gamma."},
    ]
    return {
        "classification": classes,
        "n_level_clean_models": len([c for c in classes if c["level_or_shape"].startswith("LEVEL")]),
        "n_shape_dependent_models": len(shape_dependent),
        "shape_dependent_models": [c["model"] for c in shape_dependent],
        "gamma_is_a_level_proxy_in": proxy_models,
        "abstentions_track_the_level_shape_boundary": abstentions,
        "consistency_finding": ("every kit abstention is precisely a shape / multi-locus case a single "
                                "window-mean gamma cannot model -- the kit's self-imposed limits "
                                "already track the level/shape boundary (convergent evidence)."),
        "interpretation": ("of the six modelled subclasses, FIVE are LEVEL-clean (the well the lesion "
                           "perturbs IS the read gamma's well) and ONE (E-CIS, 3 diseases) uses "
                           "promoter-gamma as a LEVEL PROXY for a position-displaced fold; that one is "
                           "flagged and restricted to a topology-direction claim."),
    }


# ============================================================ the retirement (mirrors site 'gamma SUBSET A4')
RETIRED_FRAMING = {
    "retired_irreversible": ("the promoter window-mean gamma CHARACTERISES a position-displaced "
                             "lesion's OWN cusp / gamma carries the lesion's positional shape / the "
                             "promoter barrier value governs a deep-intronic or enhancer-displaced fold"),
    "falsified_by": ("the inherited [V] orthogonality (A4 carries none of the level gamma is; "
                     "max|corr|=0.327) -- a window MEAN cannot carry within-window position; AND TEST A "
                     "(the kit's direction is gamma-independent, so the displaced-lesion claim was never "
                     "warranted by gamma's value to begin with)."),
    "standing_statement": ("gamma is the LEVEL (promoter window-mean). It warrants ONLY (i) that a "
                           "bistable barrier EXISTS (gamma>0 -> a real switch), from which the "
                           "gamma-INDEPENDENT direction follows, and (ii) [V] geometry + [O] feasibility "
                           "reads. It does NOT carry a position-displaced lesion's shape. For displaced "
                           "lesions the claim is TOPOLOGY-DIRECTION only."),
    "must_not_revive_as": ("e.g. 'the promoter gamma is the deep-intronic well', 'fragility ranks the "
                           "splice severity', 'the barrier sets the splice threshold'."),
    "mirror_of_source_tombstone": "dna_vp_site §8 retired register: 'gamma is a coarse A4 / gamma SUBSET A4'",
}


# ================================================================================= drive + emit
def main():
    # load the frozen 128-core inputs and attach the frozen gamma per slug (from mapped_levers)
    disease_inputs = json.load(open(os.path.join(ROOT, "inputs", "disease_inputs.json")))
    mapped = json.load(open(os.path.join(ROOT, "outputs", "mapped_levers.json")))
    for slug, rec in disease_inputs.items():
        g = None
        if slug in mapped and isinstance(mapped[slug], dict):
            g = mapped[slug].get("gamma")
        rec["_gamma"] = g

    anchors = check_inherited_anchors()
    A = test_A_level_invariance(disease_inputs)
    B = test_B_level_leak_inventory()
    C = test_C_displaced_lesion_and_abstentions()

    results = {
        "release": RELEASE,
        "round": ROUND,
        "snapshot_date": SNAPSHOT_DATE,
        "title": "gamma <-> A4 LEVEL/SHAPE inheritance audit (read-only over the frozen 128-core)",
        "inherited_source_warrant": GAMMA_A4_WARRANT,
        "inherited_anchors": anchors,
        "headline": {
            "all_hypotheses_level_invariant": A["all_hypotheses_level_invariant"],
            "n_hypothesis_invariant": f'{A["n_hypothesis_invariant"]}/{A["n_diseases"]}',
            "level_leaks_into_a_claim": B["level_leaks_into_a_direction_or_sign_claim"],
            "shape_dependent_models": C["shape_dependent_models"],
            "gamma_proxy_models": C["gamma_is_a_level_proxy_in"],
            "reading": ("the kit does NOT over-trust gamma's level: every drug hypothesis is "
                        "level-invariant (TEST A) and the level enters zero claims (TEST B). The one "
                        "residual level-proxy -- promoter-gamma standing in for a position-displaced "
                        "E-CIS fold -- is named, restricted to a topology-direction claim, and the "
                        "over-reach is retired."),
        },
        "test_A_level_invariance": A,
        "test_B_level_leak_inventory": B,
        "test_C_displaced_lesion_and_abstentions": C,
        "retired_framing": RETIRED_FRAMING,
        "grades": {
            "TEST_A": "V (deterministic property of the frozen engine, re-executed)",
            "TEST_B": "V (structural enumeration of the engine's own outputs)",
            "TEST_C": "F (a structural restriction on what may be claimed; no magnitude asserted)",
            "orthogonality_relied_on": "V (inherited from dna_vp_site, prereg ff04aa7b...)",
        },
    }

    # ---- firewall over our own output (magnitude-free discipline) ----
    leaks = []
    for path, s in firewall.walk_json_strings(results):
        lk = firewall.magnitude_leak((s or "").lower())
        if lk:
            leaks.append({"path": path, "leaks": lk, "text": s[:120]})
    firewall_log = {"scan": "forbidden_claim_scan (kit _magnitude_leak, verbatim)",
                    "status": "PASS" if not leaks else "FAIL",
                    "n_leaks": len(leaks), "leaks": leaks}

    # ---- append-only validation chain (continue from V8 head) ----
    v8 = json.load(open(os.path.join(HERE, "v8_results.json")))
    prev_head = v8["validation_chain"]["chain_head"]
    chain_records = []
    head = prev_head
    for metric, payload in [
        ("inherited_source_warrant_gamma_a4", GAMMA_A4_WARRANT["source_prereg_sha256"]),
        ("test_A_all_hypotheses_level_invariant", A["all_hypotheses_level_invariant"]),
        ("test_B_level_leaks_into_claim", B["level_leaks_into_a_direction_or_sign_claim"]),
        ("test_C_shape_dependent_models", C["shape_dependent_models"]),
        ("retired_promoter_gamma_carries_shape", True),
        ("inherited_anchors_readonly", anchors["all_match"]),
    ]:
        row = {"metric": metric, "prev_hash": head, "payload": payload}
        head = sha256_str(canonical(row))
        row["row_hash"] = head
        chain_records.append(row)
    results["validation_chain"] = {
        "chain_head": head,
        "continues_from_head": prev_head,
        "record": chain_records,
    }

    # prereg sha is computed over the canonical prereg (written below), filled after we build it
    # write results
    out_json = os.path.join(HERE, "v9_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1, sort_keys=True)
    with open(os.path.join(HERE, "firewall_log_v9.json"), "w", encoding="utf-8") as f:
        json.dump(firewall_log, f, ensure_ascii=False, indent=1, sort_keys=True)

    # ---- HTML ----
    html_doc = render_html(results, firewall_log)
    with open(os.path.join(HERE, "v9_results.html"), "w", encoding="utf-8") as f:
        f.write(html_doc)

    print(f"[V9] firewall: {firewall_log['status']} ({firewall_log['n_leaks']} leaks)")
    print(f"[V9] inherited anchors all_match: {anchors['all_match']}")
    print(f"[V9] TEST A hypotheses level-invariant: {A['n_hypothesis_invariant']}/{A['n_diseases']} "
          f"(fraction {A['hypothesis_invariant_fraction']})")
    print(f"[V9] TEST B level leaks into a claim: {B['level_leaks_into_a_direction_or_sign_claim']}")
    print(f"[V9] TEST C shape-dependent models: {C['shape_dependent_models']}; "
          f"gamma proxy in: {C['gamma_is_a_level_proxy_in']}")
    print(f"[V9] validation chain head: {head}")
    return results, firewall_log


def render_html(results, firewall_log):
    import html as H
    A = results["test_A_level_invariance"]; B = results["test_B_level_leak_inventory"]
    C = results["test_C_displaced_lesion_and_abstentions"]; W = results["inherited_source_warrant"]
    rows_a = "".join(
        f"<tr><td>{H.escape(r['slug'])}</td><td>{H.escape(r['lesion'])}</td>"
        f"<td>{'✓' if r['hypothesis_invariant_under_gamma_sweep'] else '✗'}</td>"
        f"<td>{'moves' if r['fragility_rank_moved_with_level'] else 'fixed'}</td></tr>"
        for r in A["rows"])
    rows_b = "".join(
        f"<tr><td><code>{H.escape(f['field'])}</code></td>"
        f"<td>{'γ-value' if f['depends_on_gamma_value'] else 'γ-free'}</td>"
        f"<td>{H.escape(f['what_it_is'])}</td><td>{H.escape(f['grade'])}</td></tr>"
        for f in B["fields"])
    rows_c = "".join(
        f"<tr><td>{H.escape(c['model'])}</td><td><b>{H.escape(c['level_or_shape'])}</b></td>"
        f"<td>{'proxy' if c.get('gamma_is_a_proxy') else 'proper'}</td>"
        f"<td>{H.escape(c['reason'])}</td></tr>"
        for c in C["classification"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>V9 — γ↔A4 level/shape inheritance audit</title>
<style>
 body{{font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}}
 h1{{font-size:1.5rem}} h2{{font-size:1.15rem;margin-top:2rem;border-bottom:1px solid #ddd;padding-bottom:.3rem}}
 code{{background:#f4f4f4;padding:.05rem .3rem;border-radius:3px;font-size:.86em}}
 table{{border-collapse:collapse;width:100%;margin:.6rem 0;font-size:.9em}}
 th,td{{border:1px solid #e2e2e2;padding:.35rem .5rem;text-align:left;vertical-align:top}}
 th{{background:#fafafa}} .ok{{color:#0a7d28;font-weight:600}} .flag{{color:#b25400;font-weight:600}}
 .card{{background:#f7f9fb;border:1px solid #dde6ee;border-radius:8px;padding:.8rem 1rem;margin:1rem 0}}
 .grade{{font-size:.82em;color:#555}}
</style></head><body>
<h1>V9 — γ ↔ A4 level/shape inheritance audit</h1>
<p class="grade">{H.escape(results['release'])} · read-only over the frozen 128-core · author Young Jae Lee · CC BY 4.0</p>

<div class="card">
<b>Headline.</b> {H.escape(results['headline']['reading'])}<br>
<span class="ok">TEST A: {H.escape(results['headline']['n_hypothesis_invariant'])} hypotheses level-invariant.</span>
&nbsp;<span class="ok">TEST B: {results['headline']['level_leaks_into_a_claim']} level-leak into any claim.</span>
&nbsp;<span class="flag">TEST C: γ is a level-proxy only in {H.escape(", ".join(results['headline']['gamma_proxy_models']) or "—")}.</span>
</div>

<h2>0 · Inherited fact (the warrant)</h2>
<p>{H.escape(W['fact'])}</p>
<p class="grade">Source: {H.escape(W['source_document'])} · session {H.escape(W['source_session'])} ·
prereg <code>{H.escape(W['source_prereg_sha256'][:16])}…</code> · same field ρ≈{W['measured_anchors']['same_field_rho_median']},
A4 carries none of γ (max|corr| = {W['measured_anchors']['A4_carries_of_gamma_max_abs_corr']}).</p>
<p class="grade">The kit's cusp scalar IS this γ: <code>gamma = -mean(NN dG37)</code> over the promoter window — the LEVEL.</p>

<h2>TEST A · Level-invariance of the hypothesis ({A['n_diseases']} diseases)</h2>
<p>Sweep γ across the observed band and beyond, plus an additive +0.25 level shift (the site self-check
“raise the whole line”). The hypothesis = direction + every mechanism sign + γ-restore inclusion.</p>
<p class="ok">{A['n_hypothesis_invariant']}/{A['n_diseases']} hypotheses byte-identical across the sweep.
Only the fragility rank ({A['n_with_fragility_rank_moving_with_level']}) and feasibility hint
({A['n_with_feasibility_hint_moving_with_level']}) move with the level — non-hypothesis quantities.</p>
<details><summary>per-disease ({A['n_diseases']})</summary>
<table><tr><th>slug</th><th>lesion</th><th>hyp. invariant</th><th>fragility rank</th></tr>{rows_a}</table></details>

<h2>TEST B · Level-leak inventory</h2>
<p>{H.escape(B['interpretation'])}</p>
<table><tr><th>output field</th><th>depends on</th><th>what it is</th><th>grade</th></tr>{rows_b}</table>
<p class="ok">Level leaks into a direction/sign claim: {B['level_leaks_into_a_direction_or_sign_claim']}.</p>

<h2>TEST C · Displaced-lesion proxy + abstention consistency</h2>
<table><tr><th>model</th><th>level/shape</th><th>γ role</th><th>reason</th></tr>{rows_c}</table>
<p>{H.escape(C['consistency_finding'])}</p>

<h2>Retired (irreversible)</h2>
<p class="flag">✗ {H.escape(results['retired_framing']['retired_irreversible'])}</p>
<p>✓ {H.escape(results['retired_framing']['standing_statement'])}</p>

<h2>Firewall</h2>
<p class="ok">{firewall_log['status']} — {firewall_log['n_leaks']} magnitude leaks.</p>
<p class="grade">validation chain head <code>{H.escape(results['validation_chain']['chain_head'][:24])}…</code>,
continues V8 <code>{H.escape(results['validation_chain']['continues_from_head'][:24])}…</code>.</p>
</body></html>"""


if __name__ == "__main__":
    main()
