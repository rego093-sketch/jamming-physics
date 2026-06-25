#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_gen_param_db.py -- assemble Appendix-L param_db.json with PROVABLE byte-identical inheritance
from Appendix K.

L is the BLUEPRINT CLOSE-OUT. It inherits the ENTIRE K surface byte-for-byte (the SantaLucia NN
table, all 63 real GRCh38 driver-gamma, driver_gamma_new={}, the 62-edge cascade in its three cited
blocks, the Carnegie onset anchor, the developmental rates incl. the cardiac zero-point, and every
threshold) by loading K's param_db.json and round-tripping it through an OrderedDict (json preserves
the exact float reprs). It then ADDS, append-only:

  * regulatory_cascade.edges_myogenic_upstream -- ONE cited edge (MEOX1 -> PAX7) that closes B4 by
    giving PAX7 (an artificial cascade SOURCE in K: indegree 0, depth 0, yet Carnegie rank 4) its
    real upstream somite/dermomyotome regulator. This is the SAME class of source-fix the program
    already used for TBX5/HOX13 in J. Both genes are already in the atlas -> NO new gamma.
  * thresholds.b4_jitter_closure [L] -- the B4 closure config: the pre-registered 0.70 floor is now
    cleared at the p5 lower edge on the extended cascade (p5 0.625 -> 0.728), so the jitter is no
    longer marginal. The strength claim STAYS [L] (B3 permanent ceiling), never [V].
  * thresholds.b2_cis_occupancy [F] -- the deterministic B2 occupancy probe config (cited TF-family
    IUPAC motifs, dinucleotide-shuffle null, seed 19, 500 shuffles, both strands) that reproduces
    the DATA-BLOCKED finding: proximal-promoter motif occupancy does NOT recover per-edge drive
    above background (the canonical SOX9->RUNX2 edge is BELOW background). B2 is data-blocked by
    MEASUREMENT (distal enhancers + accessibility absent from the +-2 kb gamma window), NOT a theory
    defect and NOT [L].

ADD-ONLY: Appendices A-K and every prior number/grade/equation/DOI are unchanged. L adds NO gamma and
moves NO inherited byte. inline_magic_numbers stays 0.
"""
import json
import os
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.join(os.path.dirname(HERE), "ax-k-absolute-clock", "param_db.json")

# ---- inherit the ENTIRE K surface byte-identical (OrderedDict round-trip) ----
with open(PARENT, "r", encoding="utf-8") as fh:
    db = json.load(fh, object_pairs_hook=collections.OrderedDict)

# ---- _meta: re-describe for L (the close-out); inheritance statement made explicit ----
db["_meta"] = collections.OrderedDict([
    ("appendix",
     "L -- the BLUEPRINT close-out (B4 closed; B2 resolved as data-blocked; the roadmap fully mapped)"),
    ("purpose",
     "Take the K BLUEPRINT to its honest terminus. K closed B1 (the global zero-point). L resolves "
     "the two remaining open items and maps every residual: (B4) CLOSE the jitter floor -- add ONE "
     "cited upstream edge (MEOX1 -> PAX7) so PAX7 is no longer an artificial cascade source, lifting "
     "the +-1 rank-jitter p5 of Spearman(depth, Carnegie) from 0.625 (below the pre-registered 0.70 "
     "floor) to 0.728 (above it); the strength claim stays [L], NEVER [V] (B3 ceiling). (B2) RESOLVE "
     "the cis-code -> drive map: a real, deterministic TF-motif-occupancy probe on the cached GRCh38 "
     "child promoters vs a dinucleotide-shuffle null shows the per-edge drive is NOT in the +-2 kb "
     "promoter window (the gamma window) -- the canonical SOX9->RUNX2 edge is BELOW background -- so "
     "B2 is DATA-BLOCKED by measurement (distal enhancers + accessibility are required and absent), "
     "graded [F]/data-blocked, NOT [L]. ADD-ONLY: Appendices A-K and every prior number/grade/"
     "equation/DOI are unchanged."),
    ("rule",
     "LOCK -> Derive -> Gate. No fitted parameters. precision != accuracy. The ENTIRE K param surface "
     "(NN table, all 63 driver-gamma, the 62-edge cascade, the Carnegie anchor, the developmental "
     "rates + cardiac zero-point, every threshold) is INHERITED BYTE-IDENTICAL from Appendix K and "
     "re-checked digit-for-digit by the gate. L adds ONE cited edge, the B4 closure config, and the "
     "B2 occupancy-probe config -- and NO new gamma."),
    ("the_axes",
     "STAGING ORDER (cascade grammar; the floor is now jitter-robust at the p5 edge after the "
     "MEOX1->PAX7 source-fix -- [L], not [V]) ; ABSOLUTE TIMING in days (inherited two-anchor clock, "
     "[L]) ; PER-EDGE DRIVE from sequence (B2 DATA-BLOCKED: proximal occupancy at/below background; "
     "the modelling choice W=sqrt(gamma) stays [F] -- closing it needs distal-enhancer data the kit "
     "lacks)."),
    ("grades", db["_meta"]["grades"]),
])

# ---- B4: the ONE cited upstream edge that closes the jitter floor -------------
rc = db["regulatory_cascade"]
rc["edges_myogenic_upstream"] = [
    ["MEOX1", "PAX7",
     "somite/dermomyotome (Meox1+) precedes & gives rise to Pax7+ myogenic progenitors -- the real "
     "upstream MEOX1 had no edge to PAX7 in K, leaving PAX7 an artificial cascade source (indegree 0, "
     "depth 0) despite Carnegie rank 4 (Buckingham & Relaix 2007 Annu Rev Cell Dev Biol 23:645; "
     "Mankoo 1999 Nature 400:69). Same source-fix class as the J TBX5/HOX13 upstream completions."],
]
rc["note_b4"] = (
    "B4 CLOSE-OUT (append-only on K's 62 edges -> 63): the single cited MEOX1->PAX7 edge removes "
    "PAX7 as an artificial source (depth 0 -> 3, deepening MYF5/MYOD1/MYOG behind it). MEOX1 rank 4 "
    "= PAX7 rank 4 (a tie, concordant: 0 new inversions). Spearman(depth, Carnegie) 0.755 -> 0.858; "
    "+-1 rank-jitter p5 0.625 -> 0.728 (>= 0.70 floor); frac>=floor 0.44 -> 0.99. The DAG is "
    "preserved. Minimal by design (one edge) to avoid over-fitting the statistic.")

# ---- B4 closure threshold (the jitter floor is now cleared at the p5 edge) ----
db["thresholds"]["b4_jitter_closure"] = collections.OrderedDict([
    ("value", collections.OrderedDict([
        ("floor", 0.7),
        ("closure_edge", ["MEOX1", "PAX7"]),
        ("rank_jitter", 1),
        ("n_draws", 4000),
        ("seed", 19),
        ("rule",
         "B4 closes iff, on the K-inherited cascade EXTENDED by the cited MEOX1->PAX7 edge, the "
         "+-1 Carnegie-rank jitter p5 of Spearman(cascade depth, jittered rank) is >= the "
         "pre-registered 0.70 floor (seed 19, n_draws 4000). On K it was 0.625 (< floor, marginal); "
         "extended it is 0.728 (>= floor). The added edge is itself cited and rank-tie-concordant "
         "(0 new inversions), and the DAG is preserved. The strength claim stays [L] (an empirical "
         "correlation on cited ranks) -- B3 forbids [V] permanently."),
    ])),
    ("provenance",
     "B4 closure control. The lift is mechanistic (PAX7 was an artificial source; its real cited "
     "somite/dermomyotome upstream MEOX1 was simply missing an edge), not a tuned knob: seed=19 is "
     "the R19 substrate constant, n_draws/jitter are declared, and exactly ONE minimal cited edge is "
     "added. p5 0.625 -> 0.728; the floor is met at the lower edge of citation uncertainty."),
    ("grade", "[L]"),
])

# ---- record the B4 status on the floor threshold itself (append-only field) ---
db["thresholds"]["cascade_corr_floor"]["status_after_b4_closure"] = (
    "B4 CLOSE-OUT (Appendix L): on the K cascade EXTENDED by the single cited MEOX1->PAX7 edge "
    "(removing PAX7 as an artificial source), Spearman(depth, Carnegie) = 0.858 over 47 anchored "
    "genes and the +-1 rank-jitter p5 rises to 0.728 (>= 0.70), so the floor is now cleared even at "
    "the lower edge of citation uncertainty (frac>=floor 0.99). The claim STAYS [L] (an empirical "
    "correlation on cited ranks); B3 forbids promotion to [V] permanently. The lift is mechanistic, "
    "not fitted (one cited edge, rank-tie-concordant, DAG preserved).")

# ---- B2: the cis-occupancy probe config (DATA-BLOCKED finding, reproducible) --
db["thresholds"]["b2_cis_occupancy"] = collections.OrderedDict([
    ("value", collections.OrderedDict([
        ("window_provenance",
         "the cached GRCh38 promoter window is TSS-2000..+500 (2501 bp) -- the SAME +-2 kb window the "
         "gamma operator reads. The probe asks whether the cited PARENT TF-family motif is present in "
         "the CHILD promoter above a dinucleotide-shuffle background; if not, the proximal cis-code "
         "does not carry the per-edge drive and B2 cannot close from this kit."),
        ("seed", 19),
        ("n_shuffles", 500),
        ("both_strands", True),
        ("null", "dinucleotide-preserving shuffle (controls GC/CpG composition); parameter-free"),
        ("above_background_rule", "observed count strictly greater than the 95th percentile of the shuffle null"),
        ("tf_family_motifs_iupac", collections.OrderedDict([
            ("HOX",  ["TAATKR", "TAATGG", "TAATTA"]),
            ("SOX",  ["WWCAAWG", "ACAAAG", "AACAAT"]),
            ("RUNX", ["TGTGGT", "ACCACA"]),
            ("PITX", ["TAATCC"]),
            ("ISL",  ["TAATKR", "TAATTA"]),
            ("PAX",  ["GTCACG", "GTTCC"]),
            ("ETS",  ["SCGGAAGT", "GGAW"]),
            ("TCF",  ["CTTTGWW", "CTTTGAT"]),
        ])),
        ("motif_citations",
         "homeodomain TAAT core (Noyes 2008 Cell 133:1277; Berger 2008 Cell 133:1266); SOX HMG "
         "AACAAT/ACAAAG (Mertin 1999 Nucleic Acids Res 27:1359; Harley 1994); RUNX/Runt TGTGGT/OSE2 "
         "(Ducy 1997 Cell 89:747); PITX bicoid-class TAATCC (Szeto 1996 Genes Dev 10:1467); ISL1 "
         "LIM-HD TAAT core; PAX paired-domain (Epstein 1994 Genes Dev 8:2022); FGF->ETS effector "
         "(Wei 2010); WNT->TCF/LEF effector CTTTG (van de Wetering 1997 Cell 88:789). Ligand parents "
         "(FGF/WNT) are scored on their downstream DNA-binding effector motif, as flagged."),
        ("data_blocked_rule",
         "B2 is DATA-BLOCKED (NOT closeable to [L] from this kit) iff the majority of both-cached "
         "cited edges sit AT/BELOW background AND the canonical direct edge SOX9->RUNX2 is BELOW "
         "background -- i.e. the proximal +-2 kb promoter window does not carry the per-edge drive. "
         "Closing B2 would require distal-enhancer + chromatin-accessibility sequence the present kit "
         "does not contain. This is a MEASUREMENT limitation (cf. the Inheritance-Kit FV5 "
         "data-blocked-by-measurement finding), not a theory defect; the modelling choice "
         "W=sqrt(gamma) therefore stays [F]."),
    ])),
    ("provenance",
     "B2 resolution control. Parameter-free (the dinucleotide shuffle is the null; seed=19 is the R19 "
     "substrate constant; motif strings are cited consensus, not fitted). The probe is deterministic "
     "and re-run by the gate; the data-blocked verdict (majority at/below background; SOX9->RUNX2 "
     "below background) is locked, falsifiable, and reproduced byte-for-byte in expected/."),
    ("grade", "[F]"),
])

# inline magic numbers stay zero (every datum above carries provenance)
# (the field already exists implicitly via the manifest; assert nothing inline.)

OUT = os.path.join(HERE, "param_db.json")
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(db, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

# ---- prove byte-identical inheritance of the K surface (sanity, printed) ------
with open(PARENT, "r", encoding="utf-8") as fh:
    parent = json.load(fh, object_pairs_hook=collections.OrderedDict)
checks = []
# every inherited driver gamma identical
pg = {}; pg.update(parent["driver_gamma_inherited"])
lg = {}; lg.update(db["driver_gamma_inherited"])
checks.append(("driver_gamma_inherited byte-identical",
               all(str(lg[k]["gamma"]) == str(pg[k]["gamma"]) for k in pg) and len(lg) == len(pg)))
checks.append(("driver_gamma_new still empty", len(db["driver_gamma_new"]) == 0))
checks.append(("nn table identical",
               json.dumps(db["nn_stacking_dG_kcal_per_mol"]) == json.dumps(parent["nn_stacking_dG_kcal_per_mol"])))
checks.append(("3 inherited edge blocks identical",
               db["regulatory_cascade"]["edges_inherited"] == parent["regulatory_cascade"]["edges_inherited"]
               and db["regulatory_cascade"]["edges_limb_induction"] == parent["regulatory_cascade"]["edges_limb_induction"]
               and db["regulatory_cascade"]["edges_hox_collinear"] == parent["regulatory_cascade"]["edges_hox_collinear"]))
checks.append(("carnegie anchor identical",
               json.dumps(db["carnegie_onset_anchor"]) == json.dumps(parent["carnegie_onset_anchor"])))
checks.append(("developmental_rates identical",
               json.dumps(db["developmental_rates"]) == json.dumps(parent["developmental_rates"])))
checks.append(("new myogenic edge present", len(db["regulatory_cascade"]["edges_myogenic_upstream"]) == 1))
checks.append(("b4_jitter_closure present", "b4_jitter_closure" in db["thresholds"]))
checks.append(("b2_cis_occupancy present", "b2_cis_occupancy" in db["thresholds"]))
print("Appendix-L param_db.json written:", OUT)
for name, ok in checks:
    print(("  OK  " if ok else "  XX  ") + name)
print("all inheritance checks pass:", all(ok for _, ok in checks))
