#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cross_package_harness.py  --  the LIVE CROSS-PACKAGE HARNESS (immune_hematologic_vp_site, section 17).

A runner that loads THIS volume together with its sibling VP volumes IN ONE PROCESS and confirms, against
the LIVE sibling engines, the identities the seam layer (section 16) had to take on trust:

  (1) SHARED SUBSTRATE -- every volume's R19 spinodal |h_sp| = 2(g/3)^1.5 and barrier g^2/4 are
      byte-identical (cross-volume drift exactly 0). This is the foundation that lets the tolerance
      saddle-node derived HERE be READ in digestive's mucosa and in mind's HPA without a refit.
  (2) GUT-IMMUNE LATCH IDENTITY -- digestive's LIVE ibd_relapsing_course() reproduces the IBD induction /
      maintenance / relapsing snapshot this volume vendored, AND those thresholds equal this volume's
      T23 saddle-node (antigen + spinodal) and T24 suppressor complement (antigen - spinodal). So the gut
      mucosal tolerance latch the seam layer claims IS this volume's machinery localised -- verified live.
  (3) NEURO-IMMUNE ENDPOINT -- mind's engine carries the SAME spinodal (the substrate the cortisol->sigma
      descriptor and the cytokine->mood pointer both ride), and mind's depression chronification (section 27)
      names the INFLAMMATORY contributor the cytokine-tone pointer lands on (the HPA/cortisol cascade for
      the IN direction; the inflammatory term for the OUT direction) -- a real, shared-substrate reading
      rather than a dangling reference.

ARCHITECTURE / FIREWALL.  The harness runs OUTSIDE every gate. The research gate (repro/run_all.py) and the
canonical build (tools/build_docs.py) compute nothing here and never import a sibling: each volume still
re-establishes its entire trusted state from its OWN archive with the siblings ABSENT (the verify-alone
guarantee, the same neuro<->mind project-boundary rule the seam layer enforces). When the siblings are not
discoverable this module SKIPS the live checks and exits 0 -- it can never break a sibling-free build. The
sibling engines are loaded by FILE PATH under unique module names with the package-internal module table
cleared between loads (so two volumes' identically-named vp_substrate cannot collide), which is loading,
not importing: no sibling code path is wired into this volume's engine.

DIGEST.  digest() hashes the IMMUNE-SIDE CONTRACT only -- the in-package reference values (the closed-form
substrate identity, the vendored digestive IBD snapshot, the gut saddle-node identity, and the neuro-immune
endpoint descriptor). That contract is computed from THIS package's own modules with no sibling present, so
the harness digest is byte-identical whether or not the siblings are on disk -- exactly what the
deterministic build requires. The engine circulate()/emit() 2x-sha256 (e7a2a5b8...), the stress battery, the
discipline gates and the seam digest are all UNCHANGED by this layer; this layer carries its OWN 2x-sha256.

Run the live cross-volume check:  python repro/run_harness.py   (with the sibling packages present)
"""
import os, sys, json, math, hashlib, importlib.util, glob, re
from functools import lru_cache

_HERE     = os.path.dirname(os.path.abspath(__file__))
_REPRO    = os.path.dirname(_HERE)
_PKG      = os.path.dirname(_REPRO)
_INHERIT  = os.path.join(_PKG, "inherited")
for _sub in (_INHERIT, os.path.join(_REPRO, "_engine")):
    if _sub not in sys.path:
        sys.path.insert(0, _sub)

import vp_substrate as VP                     # THIS package's substrate -- the reference R19 (single source)

CONCEPT_IMM  = "10.5281/zenodo.20755280"      # immune concept DOI (tolerance/surveillance hub / SSOT)
CONCEPT_DIG  = "10.5281/zenodo.20755319"      # digestive concept DOI (gut mucosal localisation owner)
CONCEPT_MIND = "10.5281/zenodo.20694404"      # mind concept DOI (felt / HPA owner)
CONCEPT_CIRC = "10.5281/zenodo.20754354"      # circulatory concept DOI (vascular transport owner)
CONCEPT_MSK  = "TO-RECONCILE"                 # musculoskeletal owner DOI -- placeholder, never fabricated

# Sibling signature files (relative to a package ROOT) -- how each sibling is recognised and where its
# spinodal-bearing engine lives. The harness loads ONLY these read-only.
#
# NOTE (v0.17.0): the digestive/mind signatures are confirmed (their seams are live-verified in section 17).
# The circulatory/musculoskeletal engine RELATIVE PATHS below are PROVISIONAL -- those volumes are NOT on
# disk in this session, so the paths are a best-effort guess to be RECONCILED on the first live run with the
# sibling zip present (the discover step prints which siblings resolved, so an unresolved provisional path is
# visible, never silent). Either way the live check SKIPS cleanly when the sibling is absent -- it can never
# break a sibling-free build. These are one-way POINTER seams: the live check only needs substrate drift 0
# plus (for musculoskeletal) the OPTIONAL identity-upgrade probe; absent that, the immune-side endpoint is
# still verified in-package.
SIBLINGS = {
    "digestive": dict(engine="repro/_engine/vp_dig_engine.py",
                      extra=("inherited", "repro/_engine", "repro/_disease"),
                      ibd_module="repro/_disease/disease_modules.py",
                      tokens=("digestive",)),
    "mind":      dict(engine="repro/mind/_engine/vp_mind_engine.py",
                      extra=("repro/mind/_engine",),
                      depression_module="repro/mind/_verify/depression_chronification.py",
                      tokens=("mind",)),
    "circulatory":      dict(engine="repro/_engine/vp_circ_engine.py",   # PROVISIONAL -- reconcile on first live run
                             extra=("inherited", "repro/_engine"),
                             tokens=("circulat", "cardio"), provisional=True,
                             seam_kind="one-way pointer (leukocyte trafficking)"),
    "musculoskeletal":  dict(engine="repro/_engine/vp_msk_engine.py",    # CONFIRMED v0.19.0 (musculoskeletal_vp_site v0.7.0)
                             extra=("inherited", "repro/_engine"),
                             tokens=("musculo", "skelet", "msk"), provisional=False,
                             seam_kind="one-way pointer (marrow niche; LIVE-VERIFIED drift 0; identity candidate retired)"),
    "integumentary":    dict(engine="repro/_engine/vp_skn_engine.py",    # CONFIRMED v0.20.0 (integumentary_vp_site v1.0.0)
                             extra=("inherited", "repro/_engine"),
                             seam_manifest="repro/_seam/seam_manifest.py",
                             tokens=("integument", "skin", "skn"), provisional=False,
                             seam_kind="barrier-surface seam (LIVE substrate-verified drift 0 + reciprocal immune-seam handshake; identity immune-owned closed-form)"),
}


# ===========================================================================
#  Collision-safe in-process loader (loading, not importing)
# ===========================================================================
# Package-internal module names that COLLIDE across volumes (each volume ships its own). They must be
# purged from sys.modules before a sibling load so the sibling re-imports ITS OWN from its extra_paths,
# rather than picking up whichever volume happened to import the bare name first (e.g. this volume's
# vp_substrate, which lacks digestive's metaplastic_scale). The immune VP reference is held by NAME
# binding (import vp_substrate as VP), so deleting the sys.modules entry does not rebind VP.
_COLLIDABLE_INTERNAL = ("vp_substrate", "vp_dig_engine", "disease_modules", "carcinogen_dose_response",
                        "vp_mind_engine", "vp_circ_engine", "vp_msk_engine", "vp_skn_engine", "skn_dynamics",
                        "skin_pathology", "seam_manifest", "gamma_pipeline",
                        "ncbi_verify", "cross_references", "gates", "stress_tests", "seam_wiring",
                        "organ_identity")


def _purge_collidable():
    for name in list(sys.modules):
        if name in _COLLIDABLE_INTERNAL:
            f = getattr(sys.modules.get(name), "__file__", None) or ""
            if "site-packages" not in f and "dist-packages" not in f:
                del sys.modules[name]


def _load_module(unique_name, file_path, extra_paths=()):
    """Load file_path as a uniquely-named module. Purge collidable package-internal names (vp_substrate
    etc.) BEFORE the load so the sibling re-imports its OWN from its extra_paths, and purge newly-added
    package-internal modules AFTER -- never third-party / stdlib (numpy's C extension cannot reload)."""
    saved_path = list(sys.path)
    before     = set(sys.modules)
    _purge_collidable()
    for p in extra_paths:
        if p not in sys.path:
            sys.path.insert(0, p)
    try:
        spec = importlib.util.spec_from_file_location(unique_name, file_path)
        mod  = importlib.util.module_from_spec(spec)
        sys.modules[unique_name] = mod
        spec.loader.exec_module(mod)
        return mod
    finally:
        sys.path[:] = saved_path
        for k in set(sys.modules) - before:
            if k == unique_name:
                continue
            f = getattr(sys.modules.get(k), "__file__", None) or ""
            if f and (f.startswith(os.path.dirname(os.path.dirname(file_path))) or "/inherited/" in f
                      or "/_engine/" in f or "/_disease/" in f or "/repro/" in f) \
                      and "site-packages" not in f and "dist-packages" not in f:
                del sys.modules[k]


def _looks_like(root, sig):
    return os.path.isfile(os.path.join(root, sig["engine"]))


# Sibling-code tokens a sibling IMPORT would contain (the discipline: the harness reaches siblings only by
# file-path LOAD, never by an import statement). Mirrors the seam firewall's token list.
_SIBLING_IMPORT_TOKENS = ("vp_dig", "dig_engine", "digestive", "vp_mind", "mind_engine",
                          "vp_neuro", "neuro_engine", "neuro", "mind", "circulat",
                          "musculo", "skelet", "vp_msk", "msk_engine",
                          # v0.18.0 barrier-surface candidate volumes (future, not on disk):
                          "respirat", "airway", "pulmonary", "vp_resp",
                          "epiderm", "cutaneous", "vp_skin", "dermat")
_IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+([A-Za-z0-9_.]+)")


def self_no_sibling_imports():
    """OUT-OF-GATE self-check (NOT hashed): the harness's OWN two source files contain zero sibling import
    statements -- it only ever LOADS a sibling by file path. This is the discipline the seam firewall
    certifies for the gated package; the harness self-certifies it for its own out-of-gate files."""
    violations = []
    for fn in (os.path.join(_HERE, "cross_package_harness.py"), os.path.join(_REPRO, "run_harness.py")):
        if not os.path.isfile(fn):
            continue
        for i, line in enumerate(open(fn, encoding="utf-8"), 1):
            mobj = _IMPORT_RE.match(line)
            if mobj and any(tok in mobj.group(1).lower() for tok in _SIBLING_IMPORT_TOKENS):
                # the SIBLINGS dict literals reference path strings, not imports -- only flag real import stmts
                violations.append("%s:%d: %s" % (os.path.basename(fn), i, line.strip()))
    return dict(sibling_import_statements=len(violations), violations=violations,
                file_path_load_discipline_ok=bool(len(violations) == 0))


def discover_siblings(search_roots=None):
    """Locate each sibling package ROOT (the dir holding repro/). Resolution: 1) env var
    VP_SIBLING_<KIND>; 2) a scan of the search roots for the signature engine file. Absent siblings
    come back None (the live check is then skipped)."""
    if search_roots is None:
        search_roots = [os.path.dirname(_PKG), os.path.dirname(os.path.dirname(_PKG)), os.getcwd()]
    found = {}
    for kind, sig in SIBLINGS.items():
        env = os.environ.get("VP_SIBLING_" + kind.upper())
        if env and _looks_like(env, sig):
            found[kind] = env
            continue
        hit = None
        for base in search_roots:
            if not base or not os.path.isdir(base):
                continue
            for depth in range(0, 4):
                pattern = os.path.join(base, *(["*"] * depth), sig["engine"])
                for cand in sorted(glob.glob(pattern)):
                    root = cand[: -(len(sig["engine"]) + 1)]
                    low = root.lower()
                    if any(t in low for t in sig["tokens"]):
                        hit = root
                        break
                if hit:
                    break
            if hit:
                break
        found[kind] = hit
    return found


# ===========================================================================
#  IMMUNE-SIDE CONTRACT  (pure in-package; no sibling needed; hashed)
# ===========================================================================
@lru_cache(maxsize=1)
def _vendored_gut_snapshot():
    xref = json.load(open(os.path.join(_INHERIT, "cross_references.json"), encoding="utf-8"))
    return xref["digestive_gut_immune_interface"]["vendored_snapshot"]


def immune_side_contract():
    """Everything the harness asserts that is OWNED by / computable in this volume alone. This is the
    reference the live sibling engines are checked against, and the only thing the digest hashes."""
    # (1) the shared-substrate closed forms (identity: 2(g/3)^1.5 matches the substrate spinodal bit-for-bit)
    k = 2.0 / 3.0 ** 1.5
    test_g = (1.0, 1.3225, 1.4228, 1.4533, 1.4892)               # g=1 (mucosa) + the four master-gene gammas
    identity_ok = all(abs(VP.spinodal(g) - k * g ** 1.5) < 1e-15 for g in test_g)
    ref_spinodal = {round(g, 4): round(VP.spinodal(g), 8) for g in test_g}
    ref_barrier  = {round(g, 4): round(VP.barrier(g), 8) for g in test_g}
    # (2) the vendored digestive IBD snapshot this volume consumes
    snap = _vendored_gut_snapshot()
    g, ant = snap["ibd_mucosal_R19_scale_g"], snap["ibd_luminal_antigen_drive"]
    sp = VP.spinodal(g)
    # (3) the gut saddle-node identity: induction == antigen + spinodal (T23), maintenance == antigen - spinodal (T24)
    gut_identity = dict(
        induction_closed=round(ant + sp, 4), maintenance_closed=round(ant - sp, 4),
        induction_matches_vendored=(round(ant + sp, 4) == round(snap["ibd_induction_threshold"], 4)),
        maintenance_matches_vendored=(round(ant - sp, 4) == round(snap["ibd_maintenance_threshold"], 4)),
        relapsing_is_irreversibility=bool(snap["ibd_relapsing_hysteresis"]))
    # (4) the neuro-immune endpoint descriptor (the substrate the cortisol->sigma / cytokine->mood ride)
    endpoint = dict(
        in_pointer="mind M18 HPA/cortisol  ->  T24 suppressor sigma (sign-only, magnitude [O])",
        out_pointer="T31 cytokine tone M  ->  mind section 27 inflammatory contributor (one-way)",
        substrate_spinodal_g1=round(VP.spinodal(1.0), 8),
        cortisol_term="cortisol", inflammatory_term="inflammatory")
    # (5) section-18 one-way pointer endpoints -- BOTH land on this volume's own bone_marrow_hematopoiesis
    #     (RUNX1, g=1.3225) root, verified against this volume's substrate; both consume NO sibling value.
    g_root = 1.3225
    circulatory_pointer = dict(
        pointer="immune leukocyte effector populations (R19 ON-committed, rooted at bone_marrow_hematopoiesis)"
                "  ->  circulatory vascular transport (one-way OUT, no circulatory value consumed)",
        production_root_organ="bone_marrow_hematopoiesis", production_root_master_gene="RUNX1",
        production_root_gamma=g_root,
        production_root_spinodal=round(VP.spinodal(g_root), 8),
        production_root_barrier=round(VP.barrier(g_root), 8),
        owner="immune owns the effector populations; circulatory owns the absolute vascular transport scale [O]")
    musculoskeletal_pointer = dict(
        pointer="immune hematopoietic origin (bone_marrow_hematopoiesis, RUNX1)  ->  housed in musculoskeletal"
                " bone-marrow niche (one-way pointer, no musculoskeletal value consumed)",
        hematopoietic_root_organ="bone_marrow_hematopoiesis", hematopoietic_root_master_gene="RUNX1",
        hematopoietic_root_gamma=g_root,
        hematopoietic_root_spinodal=round(VP.spinodal(g_root), 8),
        hematopoietic_root_barrier=round(VP.barrier(g_root), 8),
        # v0.19.0 LIVE verification vendored from musculoskeletal_vp_site v0.7.0 (substrate drift 0); the MSK
        # bone gamma (RUNX2, 1.2414) is the vendored MSK-owned measured number, its spinodal computed HERE on
        # the byte-identical substrate -> the contract is identical with or without the sibling on disk.
        marrow_niche_pointer_live_verified=True,
        msk_substrate_drift=0.0,
        retired_identity=dict(
            msk_niche_built_by="RUNX2 (osteoblast)", msk_bone_gamma=1.2414,
            msk_bone_spinodal=round(VP.spinodal(1.2414), 8),               # 0.53237264, on the shared substrate
            hematopoietic_root_spinodal=round(VP.spinodal(g_root), 8),     # 0.58538506 (RUNX1)
            identity_holds=bool(round(VP.spinodal(1.2414), 8) == round(VP.spinodal(g_root), 8)),  # False
            verdict="shared-substrate identity RETIRED on live evidence: the MSK niche spinodal (RUNX2) != the "
                    "hematopoietic root spinodal (RUNX1), so the niche HOUSES hematopoiesis but is not the same "
                    "R19 switch (falsifier fired); the one-way pointer SURVIVES and is live-verified (drift 0)"),
        identity_claimed_now=False,
        owner="immune owns the hematopoietic primitive; musculoskeletal owns the absolute bone-niche scale [O]")
    # (6) section-19 BARRIER-SURFACE AGNOSTICISM -- the gut saddle-node generalises to ANY barrier surface:
    #     the offset from a surface's OWN antigen baseline is INVARIANT == +/- spinodal(1.0). Respiratory and
    #     skin are NAMED CANDIDATES (no live volume, no owned absolute antigen scale -> not declared seams).
    g_mucosa = 1.0
    sp_mucosa = VP.spinodal(g_mucosa)
    barrier_sweep = []
    offset_invariant = True
    for a in (0.30, 0.40, 0.50, 0.60, 0.70):                     # illustrative; the offset is what is asserted
        oi = round((a + sp_mucosa) - a, 8)
        om = round((a - sp_mucosa) - a, 8)
        if oi != round(sp_mucosa, 8) or om != round(-sp_mucosa, 8):
            offset_invariant = False
        barrier_sweep.append(dict(antigen=round(a, 4), offset_induction=oi, offset_maintenance=om))
    gut_on_agnostic_line = (round(snap["ibd_luminal_antigen_drive"] + sp_mucosa, 4)
                            == round(snap["ibd_induction_threshold"], 4))
    barrier_surface_agnostic = dict(
        shared_mucosal_R19_scale_g=g_mucosa,
        surface_independent_offset_induction=round(sp_mucosa, 8),
        surface_independent_offset_maintenance=round(-sp_mucosa, 8),
        offset_invariant_across_sweep=bool(offset_invariant),
        gut_is_the_one_vendored_point_on_the_line=bool(gut_on_agnostic_line),
        respiratory_candidate=dict(
            axis="airway-mucosa tolerance (inhaled-antigen)", seam_type="NAMED candidate",
            immune_side_offset=round(sp_mucosa, 8), identity_claimed_now=False,
            owner="immune owns the barrier-agnostic tolerance primitive; respiratory owns the absolute"
                  " airway-antigen scale [O]",
            owner_doi_respiratory="TO-RECONCILE"),
        skin_candidate=dict(
            axis="epidermal-barrier tolerance (contact-antigen)",
            seam_type="LIVE substrate-verified (drift 0) + reciprocal immune-seam handshake; identity immune-owned closed-form",
            immune_side_offset=round(sp_mucosa, 8), identity_claimed_now=False,
            # v0.20.0 LIVE verification vendored from integumentary_vp_site v1.0.0 (substrate drift 0); the
            # epidermal gammas (TP63 1.3643, KRT14 1.4894) are skin-owned vendored measured numbers, their
            # spinodals computed HERE on the byte-identical substrate -> contract identical with or without sibling.
            live_verified=True, skin_substrate_drift=0.0,
            real_epidermal_barrier_surface=dict(
                epidermis_master_gene="TP63", epidermis_spinodal=round(VP.spinodal(1.3643), 8),
                keratinocyte_master_gene="KRT14", keratinocyte_spinodal=round(VP.spinodal(1.4894), 8)),
            reciprocal_immune_seam_declared_by_skin=True,
            reciprocal_seam_id="out__immune_hematologic__urticaria",
            skin_implements_immune_tolerance_switch=False,
            identity_engine_verified=False, identity_contradicted=False,
            identity_disposition="immune-owned closed-form (barrier-agnosticism); real barrier surface confirmed; "
                                 "reciprocally recognised by the skin volume; NOT engine-verified (the skin defers "
                                 "the immune tolerance switch as an out-seam), NOT contradicted",
            owner="immune owns the barrier-agnostic tolerance primitive; skin owns the absolute epidermal-antigen scale [O]",
            owner_doi_skin="10.5281/zenodo.20754541"),
        barrier_sweep=barrier_sweep,
        grade="[F] closed-form barrier-surface-agnostic offset invariance (gut is the one vendored point); "
              "respiratory NAMED candidate; skin LIVE substrate-verified + reciprocal handshake (identity "
              "immune-owned closed-form) / [O] each surface's absolute antigen scale (sibling-owned)")
    return dict(
        shared_substrate=dict(closed_form_identity_ok=bool(identity_ok),
                              ref_spinodal=ref_spinodal, ref_barrier=ref_barrier),
        vendored_gut_snapshot=snap, gut_saddle_node_identity=gut_identity,
        neuroimmune_endpoint=endpoint,
        circulatory_pointer=circulatory_pointer,
        musculoskeletal_pointer=musculoskeletal_pointer,
        barrier_surface_agnostic=barrier_surface_agnostic,
        concept_dois=dict(immune=CONCEPT_IMM, digestive=CONCEPT_DIG, mind=CONCEPT_MIND,
                          circulatory=CONCEPT_CIRC, musculoskeletal=CONCEPT_MSK,
                          integumentary="10.5281/zenodo.20754541"))


# ===========================================================================
#  LIVE checks against the sibling engines (NOT hashed; skipped if absent)
# ===========================================================================
def live_check(found=None):
    """Run the live cross-volume identities against whatever siblings are discoverable. Skips cleanly."""
    if found is None:
        found = discover_siblings()
    out = dict(siblings_found={k: bool(v) for k, v in found.items()}, checks={})
    contract = immune_side_contract()

    # ---- (1)+(2) digestive: shared substrate drift 0 + LIVE IBD reproduces the vendored snapshot ----
    dig_root = found.get("digestive")
    if dig_root:
        sig = SIBLINGS["digestive"]
        extra = [os.path.join(dig_root, p) for p in sig["extra"]]
        dig_eng = _load_module("dig_engine_live", os.path.join(dig_root, sig["engine"]), extra)
        # shared substrate: digestive's spinodal/barrier == immune's, bit-for-bit
        drift = max(abs(dig_eng.spinodal(g) - VP.spinodal(g)) for g in (1.0, 1.3225, 1.4892)) \
                if hasattr(dig_eng, "spinodal") else None
        # LIVE IBD course
        dig_ibd = _load_module("dig_ibd_live", os.path.join(dig_root, sig["ibd_module"]), extra)
        course = dig_ibd.ibd_relapsing_course()
        snap = contract["vendored_gut_snapshot"]
        induction_live  = round(course["induction_threshold"], 4)
        maintenance_live = round(course["maintenance_threshold"], 4)
        reproduces = (induction_live == round(snap["ibd_induction_threshold"], 4)
                      and maintenance_live == round(snap["ibd_maintenance_threshold"], 4)
                      and bool(course["relapsing_hysteresis"]) == bool(snap["ibd_relapsing_hysteresis"]))
        gi = contract["gut_saddle_node_identity"]
        equals_immune_saddle_node = (induction_live == gi["induction_closed"]
                                     and maintenance_live == gi["maintenance_closed"])
        out["checks"]["digestive_shared_substrate_drift"] = dict(
            drift=drift, drift_is_zero=bool(drift is not None and drift < 1e-15))
        out["checks"]["gut_immune_latch_identity"] = dict(
            live_induction=induction_live, live_maintenance=maintenance_live,
            live_relapsing=bool(course["relapsing_hysteresis"]),
            live_reproduces_vendored=bool(reproduces),
            live_equals_immune_T23_T24_saddle_node=bool(equals_immune_saddle_node),
            passed=bool(reproduces and equals_immune_saddle_node))

    # ---- (3) mind: shared substrate + neuro-immune endpoint exists ----
    mind_root = found.get("mind")
    if mind_root:
        sig = SIBLINGS["mind"]
        extra = [os.path.join(mind_root, p) for p in sig["extra"]]
        mind_eng = _load_module("mind_engine_live", os.path.join(mind_root, sig["engine"]), extra)
        mdrift = max(abs(mind_eng.spinodal(g) - VP.spinodal(g)) for g in (1.0, 1.3225, 1.4892)) \
                 if hasattr(mind_eng, "spinodal") else None
        # endpoint: the depression module names the HPA/cortisol (IN) and inflammatory (OUT) terms
        dep_src = ""
        dep_path = os.path.join(mind_root, sig.get("depression_module", ""))
        if dep_path and os.path.isfile(dep_path):
            dep_src = open(dep_path, encoding="utf-8").read().lower()
        ep = contract["neuroimmune_endpoint"]
        hpa_endpoint_present = ("cortisol" in dep_src and "hpa" in dep_src)
        inflam_endpoint_present = ("inflammatory" in dep_src)
        out["checks"]["mind_shared_substrate_drift"] = dict(
            drift=mdrift, drift_is_zero=bool(mdrift is not None and mdrift < 1e-15))
        out["checks"]["neuroimmune_endpoint"] = dict(
            hpa_cortisol_in_endpoint_present=bool(hpa_endpoint_present),
            inflammatory_out_endpoint_present=bool(inflam_endpoint_present),
            passed=bool(hpa_endpoint_present and inflam_endpoint_present))

    # ---- (4) circulatory: shared substrate drift 0 (one-way pointer -> only the drift is live-checkable) ----
    circ_root = found.get("circulatory")
    if circ_root:
        sig = SIBLINGS["circulatory"]
        extra = [os.path.join(circ_root, p) for p in sig["extra"]]
        try:
            circ_eng = _load_module("circ_engine_live", os.path.join(circ_root, sig["engine"]), extra)
            cdrift = max(abs(circ_eng.spinodal(g) - VP.spinodal(g)) for g in (1.0, 1.3225, 1.4892)) \
                     if hasattr(circ_eng, "spinodal") else None
        except Exception as e:                                    # provisional path -> tolerate a load failure
            cdrift = None
        out["checks"]["circulatory_shared_substrate_drift"] = dict(
            drift=cdrift, drift_is_zero=bool(cdrift is not None and cdrift < 1e-15),
            note="one-way leukocyte-trafficking pointer; only substrate drift is live-checkable (no value consumed)")

    # ---- (5) musculoskeletal: shared substrate drift 0 + OPTIONAL identity-upgrade probe ----
    msk_root = found.get("musculoskeletal")
    if msk_root:
        sig = SIBLINGS["musculoskeletal"]
        extra = [os.path.join(msk_root, p) for p in sig["extra"]]
        try:
            msk_eng = _load_module("msk_engine_live", os.path.join(msk_root, sig["engine"]), extra)
            mdrift2 = max(abs(msk_eng.spinodal(g) - VP.spinodal(g)) for g in (1.0, 1.3225, 1.4892)) \
                      if hasattr(msk_eng, "spinodal") else None
            # OPTIONAL identity-upgrade probe: does the live niche read the SAME hematopoietic spinodal?
            niche_thr = None
            if hasattr(msk_eng, "marrow_niche_threshold"):
                try:
                    niche_thr = round(float(msk_eng.marrow_niche_threshold()), 8)
                except Exception:
                    niche_thr = None
        except Exception:
            mdrift2, niche_thr = None, None
        root_sp = round(VP.spinodal(1.3225), 8)
        out["checks"]["musculoskeletal_shared_substrate_drift"] = dict(
            drift=mdrift2, drift_is_zero=bool(mdrift2 is not None and mdrift2 < 1e-15),
            note="one-way marrow-niche pointer; substrate drift live-checkable (no value consumed)")
        out["checks"]["musculoskeletal_identity_upgrade_probe"] = dict(
            hematopoietic_root_spinodal=root_sp, live_niche_threshold=niche_thr,
            identity_would_hold=bool(niche_thr is not None and niche_thr == root_sp),
            note=("OPTIONAL: if the live musculoskeletal niche exposes marrow_niche_threshold()==%.8f the "
                  "one-way pointer could UPGRADE to a shared-substrate identity; absent that function this "
                  "stays a one-way pointer (no claim)" % root_sp))

    # ---- (6) integumentary (skin): substrate drift 0 + reciprocal immune-seam handshake ----
    #      The skin barrier-surface seam. The epidermal-tolerance IDENTITY is immune-owned closed-form
    #      (barrier-agnosticism); the skin volume supplies the real barrier surface and reciprocally declares an
    #      immune out-seam, but does NOT implement the immune tolerance switch -> identity not engine-verified,
    #      not contradicted. The live check confirms (a) substrate drift 0 and (b) the reciprocal seam exists.
    skn_root = found.get("integumentary")
    if skn_root:
        sig = SIBLINGS["integumentary"]
        extra = [os.path.join(skn_root, p) for p in sig["extra"]]
        try:
            skn_eng = _load_module("skn_engine_live", os.path.join(skn_root, sig["engine"]), extra)
            sdrift = max(abs(skn_eng.spinodal(g) - VP.spinodal(g)) for g in (1.0, 1.3225, 1.4892)) \
                     if hasattr(skn_eng, "spinodal") else None
        except Exception:
            sdrift = None
        # reciprocal immune-seam handshake: the skin volume's own seam manifest declares an OUT seam to immune
        recip_present = False
        sm_path = os.path.join(skn_root, sig.get("seam_manifest", ""))
        if sm_path and os.path.isfile(sm_path):
            sm_src = open(sm_path, encoding="utf-8").read()
            recip_present = ("out__immune_hematologic" in sm_src and "immune_hematologic" in sm_src)
        # does the skin engine implement an epidermal immune-tolerance threshold? (it does not -> identity stays immune-owned)
        skin_has_tolerance_threshold = hasattr(skn_eng, "epidermal_tolerance_threshold") if sdrift is not None else False
        out["checks"]["integumentary_shared_substrate_drift"] = dict(
            drift=sdrift, drift_is_zero=bool(sdrift is not None and sdrift < 1e-15),
            note="barrier-surface seam; substrate drift live-checkable (epidermal barrier shares the R19 substrate)")
        out["checks"]["integumentary_reciprocal_immune_seam"] = dict(
            reciprocal_immune_seam_present=bool(recip_present),
            skin_implements_immune_tolerance_switch=bool(skin_has_tolerance_threshold),
            identity_engine_verified=bool(skin_has_tolerance_threshold),   # skin defers tolerance -> False
            identity_contradicted=False,
            passed=bool(recip_present and not skin_has_tolerance_threshold),
            note=("the skin volume independently declares an out-seam to immune_hematologic (reciprocal handshake) "
                  "and does NOT implement the immune tolerance switch -> the epidermal-tolerance identity stays "
                  "immune-owned closed-form (barrier-agnosticism), confirmed-real-surface, not contradicted"))

    # overall: a run counts if ANY check ran (a "passed"-keyed identity check OR a drift check); it passes
    # iff every passed-keyed check passes AND every drift check is exactly zero. This lets pointer-only
    # siblings (circulatory/musculoskeletal, which contribute drift checks but no "passed" key) pass on their own.
    ran    = [v for v in out["checks"].values() if "passed" in v]
    drifts = [v for k, v in out["checks"].items() if "drift" in k]
    out["all_live_passed"] = bool(ran or drifts) and all(v["passed"] for v in ran) \
                             and all(v["drift_is_zero"] for v in drifts)
    out["any_sibling_present"] = bool(dig_root or mind_root or circ_root or msk_root)
    return out


def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    if isinstance(o, tuple): return [_round(v) for v in o]
    return o


@lru_cache(maxsize=1)
def digest():
    """Hash ONLY the immune-side contract -- byte-identical whether or not siblings are present."""
    s = json.dumps(_round(immune_side_contract()), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    s, h = digest()
    print(s)
    print("# harness contract sha256:", h)
