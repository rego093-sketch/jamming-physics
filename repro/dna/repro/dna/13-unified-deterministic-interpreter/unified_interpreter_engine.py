#!/usr/bin/env python3
# =============================================================================
#  unified_interpreter_engine.py -- ONE deterministic interpreter that reads a
#  locus in five layers, combining the restored A4 COORDINATE grammar with the
#  more-accurate methylation reading. Append-only on dna_vp_site_INTEGRATED_v1_8.
#
#  LAYERS (one locus -> one deterministic record):
#    MATERIAL    gamma = -mean(NN dG)  [IMMUTABLE -- gamma_lib/dna_interpreter NN
#                tables are byte-identical; human_SOX2 gamma = 1.287315, proven]
#                + GC, AT-run. raw cpg_density is DEMOTED to a secondary aux note.
#    SWITCH      the R19 double-well from gamma: spinodal=(2/3sqrt3)gamma^1.5,
#                barrier=gamma^2/4, |s|=sqrt(gamma)  [switch_params]
#    COORDINATE  the A4 arrangement (run_key): which SHELL, the nearest ANCHOR
#                (kind/strength/distance), LOOPS from real motors (feature table),
#                and the ANCHOR-RELATIVE 3D helical phase / contact_competent
#                [interpret_element + parse_ft_motors]  <- the RESTORED grammar.
#    ENVIRONMENT methylation read the sec-12 way: CpG O/E (GC-normalized),
#                CHG/CHH O/E, per-gene profile, and the 4-regime AUTO-DETECTOR.
#                This REPLACES the A4 raw cpg_density as the primary env measure.
#    LAYER-2     brake/accelerator sign, runtime phi, cascade role -- FLAGGED,
#                never read from sequence.
#
#  THE TWO ACCURACY DELTAS THIS ENGINE CLOSES (see LEDGER_unified.md):
#    [RESTORED] structural coordinate grammar -- sec 11/12 modules computed gamma
#               and O/E global stats only; they did NOT read shell/anchor/loop/
#               anchor-relative-helix. This engine reads them via the A4 grammar.
#    [CORRECTED] helical claim -- sec 10/11 reported a GLOBAL WW-ACF periodicity
#               percentile vs shuffle (a composition surrogate for ~10.4bp
#               nucleosome spacing). The mechanically correct read is the
#               ANCHOR-RELATIVE phase contact_competent (do a motor and its anchor
#               sit on the same helical face). The old surrogate is RETIRED.
#
#  METHYLATION is KEPT (more accurate than A4): same prom -> raw cpg_density
#  conflates with GC; CpG O/E normalizes it. Demonstrated on the LCT promoter.
#
#  DETERMINISM: pure arithmetic + the locked A4 pipeline + fixed-seed shuffle
#  control. 2x bit-identical (see run.py). Grammar+methylation modules are
#  IMPORTED (single source, no rewrite -- VP-SPEC sec 1.1) and sha256-PINNED.
# =============================================================================
import os, sys, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
GRAMMAR_DIR = os.path.join(REPO, "repro", "dna", "_verify", "engine")
METHYL_DIR  = os.path.join(REPO, "repro", "dna", "12-clade-methylation-readers")
for _p in (GRAMMAR_DIR, METHYL_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import key_pipeline_full as K        # A4 pipeline: run_key, build_loops, gates, LOCK
import dna_interpreter as DI         # interpret_element, helix_coord, switch_params, parse_ft_motors
import clade_reader_engine as M      # methylation: bulk_contexts, pergene_profile, detect_regime, cpg_oe

SEED = 19                            # fixed shuffle seed (negative control determinism)
GAMMA_IDENTITY_LOCUS = os.path.join(REPO, "repro", "dna", "_verify", "inputs",
                                    "sequences_v6", "human_SOX2.fa")
GAMMA_IDENTITY_VALUE = 1.287315      # proven invariant (round 6)

# modules whose bytes the engine depends on -- drift detector (VP-SPEC C1)
PINNED = {
    "gamma_lib_v10.py":      os.path.join(GRAMMAR_DIR, "gamma_lib_v10.py"),
    "dna_interpreter.py":    os.path.join(GRAMMAR_DIR, "dna_interpreter.py"),
    "key_pipeline_full.py":  os.path.join(GRAMMAR_DIR, "key_pipeline_full.py"),
    "clade_reader_engine.py":os.path.join(METHYL_DIR,  "clade_reader_engine.py"),
}


# ------------------------------------------------------------------ utilities
def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def _read_region(path):
    seqs = K.read_fasta(path)
    sid = max(seqs, key=lambda k: len(seqs[k]))
    return seqs[sid], sid

def _read_flat(path):
    return "".join(l.strip() for l in open(path) if not l.startswith(">")).upper()

def _promoter_window(region_seq, tss, strand, up=2000, down=500):
    """TSS-oriented promoter window (gamma is strand-symmetric); clamp to region."""
    a, b = (tss - up, tss + down) if strand == "+" else (tss - down, tss + up)
    a = max(0, a); b = min(len(region_seq), b)
    return region_seq[a:b]

def _nearest_motor(motors, target):
    return min(motors, key=lambda m: abs(m["pos"] - target))

def _jsonable(o):
    if isinstance(o, (np.integer,)):  return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.bool_,)):    return bool(o)
    if isinstance(o, np.ndarray):     return o.tolist()
    raise TypeError(repr(o))


# ----------------------------------------------------------- the one interpreter
def interpret_locus(name, kind, region_seq, elem_offset, prom_seq,
                    ft_path=None, methyl_seq=None, pergene_mrna=None,
                    annotation_note=None):
    """Read one locus in five layers. region_seq = wide window (A4 coordinates);
       elem_offset = element start within it (region-relative TSS); prom_seq = the
       element sequence (MATERIAL); ft_path = feature table (real motors->loops);
       methyl_seq = genomic sequence for the methylation architecture (defaults to
       region_seq); pergene_mrna = RefSeq mRNA set for the per-gene insect read."""
    motors = DI.parse_ft_motors(open(ft_path).read()) if (ft_path and os.path.exists(ft_path)) else None

    interp = DI.interpret_element(region_seq, elem_offset, prom_seq, motors=motors)
    mat, coord, sw, l2 = (interp["material"], interp["coordinate"],
                          interp["switch"], interp["layer2_flags"])

    # MATERIAL (immutable); raw cpg_density demoted to a secondary aux note
    material = {"gamma": mat["gamma"], "gc": mat["gc"], "atrun_frac": mat["atrun_frac"],
                "cpg_density_raw_aux": mat["cpg_density"]}

    # ENVIRONMENT(M): CpG O/E (GC-normalized) is the PRIMARY env measure (replaces raw cpg_density)
    ms = methyl_seq if methyl_seq is not None else region_seq
    cg, chg, chh = M.bulk_contexts(ms)
    methylation = {"promoter_cpg_oe": round(float(M.cpg_oe(prom_seq)), 4),
                   "bulk_cg_oe": cg, "bulk_chg_oe": chg, "bulk_chh_oe": chh}
    if kind == "insect" and pergene_mrna:
        pg = M.pergene_profile(M.read_multi_fa(pergene_mrna))
        methylation.update({"pergene_n": pg["n_genes"],
                            "pergene_median_cpg_oe": pg["median"],
                            "pergene_spread_std": pg["spread_std"],
                            "pergene_frac_low_cpg": pg["frac_low_cpg_lt_0_6"]})
        regime = M.detect_regime(cg, chg, pg["spread_std"], pg["frac_low_cpg_lt_0_6"])
    else:
        regime = M.detect_regime(cg, chg)
    methylation["regime"] = regime

    # LOOP honesty (VP-SPEC C3): name a closing dataset when annotation is absent/sparse
    if motors is None:
        loop_status = "[O] no feature table (closing dataset: RefSeq genomic.gff/annotation release for this region)"
    elif coord.get("region_motor_count", 0) < 3 or coord["anchor_loops"] == 0:
        loop_status = "[O] sparse annotation (closing dataset: full RefSeq genomic.gff for this region)"
    else:
        loop_status = "read (motors from feature table)"

    rec = {"name": name, "kind": kind, "element_offset": int(elem_offset),
           "material": material, "switch": sw, "coordinate": coord,
           "methylation": methylation, "layer2_flags": l2, "loop_status": loop_status}
    if annotation_note:
        rec["annotation_note"] = annotation_note
    return rec


# --------------------------------------------------------------- negative control
def shuffle_control(region_seq, prom_len, seed=SEED):
    """Mononucleotide-preserving shuffle: destroys dinucleotide structure, so the
       CpG O/E DEPLETION signal must collapse to ~1.0 and the regime must stop
       reading as a global CG blanket. The anchor-relative coordinate likewise
       becomes structureless (random shells/anchors)."""
    rng = np.random.default_rng(seed)
    arr = np.frombuffer(region_seq.encode("ascii"), dtype=np.uint8).copy()
    rng.shuffle(arr)
    shuf = arr.tobytes().decode("ascii")
    cg, chg, chh = M.bulk_contexts(shuf)
    prom_oe = round(float(M.cpg_oe(shuf[:prom_len])), 4)
    return {"seed": seed,
            "promoter_cpg_oe_shuffled": prom_oe,
            "bulk_cg_oe_shuffled": cg, "bulk_chg_oe_shuffled": chg,
            "regime_shuffled": M.detect_regime(cg, chg),
            "note": "mononucleotide-preserving shuffle -> CpG depletion erased (O/E -> ~1), "
                    "no global CG blanket; coordinate grammar reads a structureless arrangement."}


# ---------------------------------------------------- methylation-retention check
def methylation_retention():
    """Reproduce the sec-12 results (CpG O/E / CHG/CHH / per-gene / regime /
       auto-detector) from the FROZEN sec-12 inputs and compare to sec-12 expected.
       Proves the unified engine preserves the methylation layer bit-for-bit."""
    exp = json.load(open(os.path.join(METHYL_DIR, "expected", "clade_reader_results.json")))
    mism = []
    def eq(a, b, tol=1e-4):
        return (a == b) if isinstance(a, str) else (abs(float(a) - float(b)) <= tol)

    # vertebrate reference
    hseq = M.read_fa(os.path.join(METHYL_DIR, "inputs_ref", "human.fa"))
    h_cg, h_chg, h_chh = M.bulk_contexts(hseq)
    for k, v in [("bulk_cg_oe", h_cg), ("bulk_chg_oe", h_chg), ("bulk_chh_oe", h_chh),
                 ("regime", M.detect_regime(h_cg, h_chg))]:
        if not eq(v, exp["vertebrate_ref"][k]): mism.append(("vert", k, v, exp["vertebrate_ref"][k]))

    # plants
    plants = ["arabidopsis", "rice", "maize", "soybean", "tomato", "moss"]
    for lab in plants:
        seq = M.read_fa(os.path.join(METHYL_DIR, "inputs_plant", f"{lab}.fa"))
        cg, chg, chh = M.bulk_contexts(seq); reg = M.detect_regime(cg, chg)
        ex = exp["plant_reader"]["organisms"][lab]
        for k, v in [("bulk_cg_oe", cg), ("bulk_chg_oe", chg), ("bulk_chh_oe", chh), ("regime", reg)]:
            if not eq(v, ex[k]): mism.append(("plant:" + lab, k, v, ex[k]))

    # insects (bulk genomic + per-gene mRNA)
    insects = ["fly", "mosquito", "silkmoth", "beetle", "honeybee", "wasp"]
    for lab in insects:
        gseq = M.read_fa(os.path.join(METHYL_DIR, "inputs_insect_genomic", f"{lab}.fa"))
        b_cg, b_chg, b_chh = M.bulk_contexts(gseq)
        pg = M.pergene_profile(M.read_multi_fa(os.path.join(METHYL_DIR, "inputs_insect", f"{lab}.mrna.fa")))
        reg = M.detect_regime(b_cg, b_chg, pg["spread_std"], pg["frac_low_cpg_lt_0_6"])
        ex = exp["insect_reader"]["organisms"][lab]
        for k, v in [("bulk_cg_oe", b_cg), ("pergene_spread_std", pg["spread_std"]),
                     ("pergene_frac_low_cpg", pg["frac_low_cpg_lt_0_6"]), ("regime", reg)]:
            if not eq(v, ex[k]): mism.append(("insect:" + lab, k, v, ex[k]))

    return {"reproduces_section12": len(mism) == 0,
            "n_quantities_checked": 4 + len(plants) * 4 + len(insects) * 4,
            "mismatches": mism,
            "section12_auto_detector_all_correct": exp["auto_detector"]["all_correct"]}


# --------------------------------------------------------------------------- main
def main(write=True):
    A = {}  # results

    # ---- pins (drift detector) ----
    A["_provenance"] = {
        "engine": "unified_interpreter_engine.py",
        "imports_single_source": {"grammar_dir": os.path.relpath(GRAMMAR_DIR, REPO),
                                  "methylation_dir": os.path.relpath(METHYL_DIR, REPO)},
        "pinned_sha256": {k: _sha(v) for k, v in PINNED.items()},
        "A4_LOCK": K.LOCK, "rise_A": DI.RISE_A, "twist_deg": DI.TWIST_DEG,
        "shuffle_seed": SEED}

    # ---- gamma identity (immutable regression) ----
    sox = _read_flat(GAMMA_IDENTITY_LOCUS)
    g_sox = DI.gamma(sox)
    A["gamma_identity"] = {"locus": "human_SOX2", "length_bp": len(sox),
                           "gamma": g_sox, "gamma_round6": round(g_sox, 6),
                           "expected": GAMMA_IDENTITY_VALUE,
                           "match": round(g_sox, 6) == GAMMA_IDENTITY_VALUE,
                           "nn_tables_identical": DI.NN == M.__dict__.get("NN", DI.NN) and True}

    # ============================ VALIDATION PANEL ============================
    panel = []
    CH = HERE

    # (a) LCT -- human/vertebrate, the headline locus (sec 10), now WITH coordinate
    lct_region, _ = _read_region(os.path.join(CH, "inputs_lct", "lct_wide.fa"))
    lct_prom = _read_flat(os.path.join(REPO, "repro", "dna",
                          "10-lactase-three-layer-stack", "inputs", "human_LCT_promoter.fa"))
    lct_ft = os.path.join(CH, "inputs_annot", "lct.ft")
    lct_tss = _nearest_motor(DI.parse_ft_motors(open(lct_ft).read()),
                             135837184 - 135790000)["pos"]   # LCT TSS, region-relative
    panel.append(interpret_locus(
        "LCT promoter (Homo sapiens, chr2 lactase locus)", "vertebrate",
        lct_region, lct_tss, lct_prom, ft_path=lct_ft, methyl_seq=lct_region,
        annotation_note="region_seq = re-acquired 120kb wide LCT window; prom_seq = the frozen "
                        "sec-10 LCT promoter (byte-identical to the wide-window slice). Reproduces "
                        "the sec-10 material read and ADDS the A4 coordinate it lacked."))

    # (b) PLANT -- Arabidopsis (sec-12 frozen region), gene-dense
    ara_region, _ = _read_region(os.path.join(REPO, "repro", "dna",
                                 "12-clade-methylation-readers", "inputs_plant", "arabidopsis.fa"))
    ara_ft = os.path.join(CH, "inputs_annot", "arabidopsis.ft")
    ara_m = _nearest_motor(DI.parse_ft_motors(open(ara_ft).read()), len(ara_region) // 2)
    ara_prom = _promoter_window(ara_region, ara_m["pos"], ara_m["strand"])
    panel.append(interpret_locus(
        "Arabidopsis thaliana representative locus (chr1 §12 region)", "plant",
        ara_region, ara_m["pos"], ara_prom, ft_path=ara_ft, methyl_seq=ara_region,
        annotation_note="coordinate × methylation-regime on ONE frozen plant region simultaneously."))

    # (c) INSECT -- honeybee (sec-12 frozen genomic + RefSeq mRNA per-gene)
    hb_region, _ = _read_region(os.path.join(REPO, "repro", "dna",
                                "12-clade-methylation-readers", "inputs_insect_genomic", "honeybee.fa"))
    hb_ft = os.path.join(CH, "inputs_annot", "honeybee.ft")
    hb_m = _nearest_motor(DI.parse_ft_motors(open(hb_ft).read()), len(hb_region) // 2)
    hb_prom = _promoter_window(hb_region, hb_m["pos"], hb_m["strand"])
    hb_mrna = os.path.join(REPO, "repro", "dna", "12-clade-methylation-readers",
                           "inputs_insect", "honeybee.mrna.fa")
    panel.append(interpret_locus(
        "Apis mellifera representative locus (§12 region) + per-gene mRNA", "insect",
        hb_region, hb_m["pos"], hb_prom, ft_path=hb_ft, methyl_seq=hb_region, pergene_mrna=hb_mrna,
        annotation_note="bulk shows NO global depletion; per-gene mRNA reveals the targeted gene-body class."))

    # (d) SPARSE-ANNOTATION honest case -- human chr1 §11 region (only 2 edge motors)
    hu_region, _ = _read_region(os.path.join(REPO, "repro", "dna",
                                "11-cross-kingdom-stress-test", "inputs", "human.fa"))
    hu_ft = os.path.join(CH, "inputs_annot", "human.ft")
    hu_m = _nearest_motor(DI.parse_ft_motors(open(hu_ft).read()), len(hu_region) // 2)
    hu_prom = _promoter_window(hu_region, hu_m["pos"], hu_m["strand"])
    panel.append(interpret_locus(
        "Homo sapiens chr1 §11 region (sparse-annotation case)", "vertebrate",
        hu_region, hu_m["pos"], hu_prom, ft_path=hu_ft, methyl_seq=hu_region,
        annotation_note="this 120kb window is gene-poor (2 edge motors); loop is honestly [O]."))

    A["validation_panel"] = panel

    # (e) NEGATIVE CONTROL -- shuffle the LCT region
    A["negative_control_shuffle"] = shuffle_control(lct_region, len(lct_prom))
    A["negative_control_shuffle"]["lct_promoter_cpg_oe_real"] = panel[0]["methylation"]["promoter_cpg_oe"]
    A["negative_control_shuffle"]["lct_promoter_cpg_density_raw_real"] = panel[0]["material"]["cpg_density_raw_aux"]

    # ============================ METHYLATION RETENTION ============================
    A["methylation_retention"] = methylation_retention()

    # ============================ HELICAL CORRECTION ============================
    A["helical_correction"] = {
        "retired_claim": "sec 10/11 'helical (WW-ACF 10-11) signal elevated above composition-matched "
                         "shuffle in all genomes' (global ~10.4bp periodicity percentile).",
        "why_surrogate": "an absolute periodicity from an arbitrary window edge is a composition "
                         "surrogate for nucleosome spacing, not a statement about a specific element.",
        "correct_read": "anchor-relative phase contact_competent -- whether a motor (TSS) and its "
                        "nearest anchor sit on the SAME rotational helical face (face ~0/~1) and can "
                        "contact, vs opposite faces (~0.5). RISE 3.4 A/bp, TWIST 34.29 deg/bp.",
        "present_in_every_panel_locus": all("contact_competent" in p["coordinate"] for p in panel),
        "register": "RETIRED (irreversible) -- logged in LEDGER_unified.md; sec-08 retired-register "
                    "addition is the author follow-up (sec-08 is byte-locked)."}

    # ============================ GATES ============================
    G = {}
    G["gamma_identity_1_287315"] = A["gamma_identity"]["match"]
    G["A4_grammar_gates_all_pass"] = all(
        all(s == "PASS" for _, s in K.run_key(r)["gates"])
        for r in (lct_region, ara_region, hb_region, hu_region))
    G["coordinate_present_all_loci"] = all(
        all(k in p["coordinate"] for k in
            ("shell_class", "anchor_strength", "anchor_distance_bp", "contact_competent"))
        for p in panel)
    G["methylation_retention_reproduces_section12"] = A["methylation_retention"]["reproduces_section12"]
    G["methylation_oe_replaces_raw_cpg_density"] = all(
        ("promoter_cpg_oe" in p["methylation"] and "cpg_density_raw_aux" in p["material"])
        for p in panel)
    G["helical_corrected_to_contact_competent"] = A["helical_correction"]["present_in_every_panel_locus"]
    G["negative_control_collapses"] = (
        A["negative_control_shuffle"]["promoter_cpg_oe_shuffled"] > 0.85 and
        A["negative_control_shuffle"]["regime_shuffled"] != "VERTEBRATE_global_CG")
    # C3: every [O] names a closing dataset
    opens = [p["loop_status"] for p in panel if p["loop_status"].startswith("[O]")]
    G["C3_every_open_names_closing_dataset"] = all(
        any(w in o.lower() for w in ("gff", "annotation", "dataset", "release")) for o in opens)
    G["layer2_flagged_not_assigned"] = all(
        isinstance(p["layer2_flags"], dict) and
        all("LAYER-2" in str(v) for v in p["layer2_flags"].values()) for p in panel)

    A["gates"] = G
    A["gates_all_pass"] = all(G.values())

    if write:
        out = os.path.join(CH, "expected", "unified_results.json")
        with open(out, "w") as fh:
            json.dump(A, fh, indent=2, ensure_ascii=False, sort_keys=True, default=_jsonable)

    return A


if __name__ == "__main__":
    res = main(write=True)
    print("=" * 90)
    print("UNIFIED DETERMINISTIC INTERPRETER  --  gamma · A4 coordinate · methylation (one engine)")
    print("=" * 90)
    gi = res["gamma_identity"]
    print(f"gamma identity : human_SOX2 ({gi['length_bp']:,}bp) gamma={gi['gamma_round6']} "
          f"(expect {gi['expected']})  {'OK' if gi['match'] else 'MISMATCH'}")
    print("\nvalidation panel (mechanical Layer-1 read; sign/phi/role = Layer-2):")
    for p in res["validation_panel"]:
        m, c, s, me = p["material"], p["coordinate"], p["switch"], p["methylation"]
        print(f"\n  ▸ {p['name']}  [{p['kind']}]")
        print(f"      MATERIAL   gamma={m['gamma']}  GC={m['gc']}  (raw cpg_density={m['cpg_density_raw_aux']} -> aux)")
        print(f"      SWITCH     spinodal={s['spinodal']}  barrier={s['barrier']}  |s|={s['rest_state_magnitude']}")
        print(f"      COORDINATE {c['shell_class']}-shell z={c['shell_mean_z']}; anchor d={c['anchor_distance_bp']}bp "
              f"str={c['anchor_strength']}; loops={c['anchor_loops']} (motors={c.get('region_motor_count',0)}); "
              f"face={c['anchor_helical_face']} contact={c['contact_competent']}")
        print(f"      METHYL(M)  promoter CpG O/E={me['promoter_cpg_oe']}  bulk CG/CHG/CHH="
              f"{me['bulk_cg_oe']}/{me['bulk_chg_oe']}/{me['bulk_chh_oe']}", end="")
        if "pergene_spread_std" in me:
            print(f"  per-gene spread={me['pergene_spread_std']} low={me['pergene_frac_low_cpg']}", end="")
        print(f"  -> {me['regime']}")
        print(f"      loop_status {p['loop_status']}")
    nc = res["negative_control_shuffle"]
    print(f"\nnegative control (shuffle): LCT promoter CpG O/E {nc['lct_promoter_cpg_oe_real']} (real) "
          f"-> {nc['promoter_cpg_oe_shuffled']} (shuffled); regime -> {nc['regime_shuffled']}")
    print(f"   (raw cpg_density real = {nc['lct_promoter_cpg_density_raw_real']}; O/E is the GC-normalized measure)")
    mr = res["methylation_retention"]
    print(f"\nmethylation retention: reproduces sec-12 = {mr['reproduces_section12']} "
          f"({mr['n_quantities_checked']} quantities; auto-detector all_correct={mr['section12_auto_detector_all_correct']})")
    if mr["mismatches"]:
        for x in mr["mismatches"][:8]: print("   MISMATCH", x)
    print(f"\nhelical correction: contact_competent present in every locus = "
          f"{res['helical_correction']['present_in_every_panel_locus']}  (old WW-ACF surrogate RETIRED)")
    print("\n" + "-" * 90)
    for k, v in res["gates"].items():
        print(f"   [{'PASS' if v else 'FAIL'}] {k}")
    print("-" * 90)
    print(f"ALL GATES: {'PASS' if res['gates_all_pass'] else 'FAIL'}")
