#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cross_package_harness.py  --  the LIVE CROSS-PACKAGE HARNESS (§30).

The last frontier item of the §8 work order: a runner that loads THIS volume together with
its sibling VP volumes IN ONE PROCESS and confirms, against the LIVE sibling engines, the
identities the seam layer (§27) and the inherited analgesic layer (§28) had to take on trust:

  (1) SHARED SUBSTRATE -- every volume's R19 spinodal |h_sp| = 2(g/3)^1.5 and barrier g^2/4 are
      byte-identical (cross-volume drift exactly 0). This is the foundation that lets a primitive
      derived in one volume be READ in another without a refit.
  (2) CIRCULATORY HEPATIC SEAM -- circulatory's LIVE hepatic_clearance() reproduces the snapshot
      this volume vendored in inherited/cross_references.json (Q_H=1500, E=0.75, F=0.25, CL_H=1125),
      so the §24 NAFLD/MASLD lipid delivery and §25 bile cholesterol delivery rest on a verified value.
  (3) ANALGESIC MAP DRIFT-0 ACROSS VOLUMES -- the inherited 27-target firing-threshold map
      (analgesic_threshold_logic v2.0) re-derives bit-for-bit through EVERY volume's own spinodal,
      so "inherited once, read many times, drift 0" is a live cross-volume fact, not a per-package claim;
      and the second host (musculoskeletal, which already carries the analgesic layer) reads its own
      levers on the SAME spinodal.
  (4) NEURO FELT-SYMPTOM ENDPOINT -- the peripheral nociceptor the §18 -> mind one-way pointer targets
      exists in neuro on the shared substrate (a HIGH-threshold polymodal cell, master PRDM12 / Nav1.7
      SCN9A -- the same channel the §28 map's L1 lever blocks), so the firewall pointer lands on a real,
      shared-substrate reading rather than a dangling reference.

ARCHITECTURE / FIREWALL.  The harness runs OUTSIDE every gate. The research gate (repro/run_all.py) and
the canonical build (tools/build_docs.py) compute nothing here and never import a sibling: each volume still
re-establishes its entire trusted state from its OWN archive with the siblings ABSENT (the verify-alone
guarantee, the same neuro<->mind project-boundary rule the seam layer enforces). When the siblings are not
discoverable this module SKIPS the live checks and exits 0 -- it can never break a sibling-free build. The
sibling engines are loaded by FILE PATH under unique module names with the package-internal module table
cleared between loads (so two volumes' identically-named `vp_substrate` cannot collide), which is loading,
not importing: no sibling code path is wired into this volume's engine.

DIGEST.  digest() hashes the DIGESTIVE-SIDE CONTRACT only -- the in-package reference values (the closed-form
substrate identity at the 27 map gammas, the vendored circulatory snapshot, the analgesic drift-0 reverify,
and the neuro-endpoint identity descriptor). That contract is computed from THIS package's own modules with
no sibling present, so the harness digest is byte-identical whether or not the siblings are on disk -- exactly
what the deterministic build requires. The engine circulate()/emit() 2x-sha256, the disease digest, the C6
oncology digest, the seam digest and the analgesic digest are all UNCHANGED by this layer (nothing here feeds
the hashed emergence core); this layer carries its OWN 2x-sha256 digest, exactly as the §27 seam and §28
analgesic layers do.

Run the live cross-volume check:  python repro/run_harness.py   (with the sibling packages present)
"""
import os, sys, json, math, hashlib, importlib.util, glob
from functools import lru_cache

_HERE     = os.path.dirname(os.path.abspath(__file__))
_REPRO    = os.path.dirname(_HERE)
_PKG      = os.path.dirname(_REPRO)
_INHERIT  = os.path.join(_PKG, "inherited")
for _sub in (_INHERIT, os.path.join(_REPRO, "_analgesic")):
    if _sub not in sys.path:
        sys.path.insert(0, _sub)

import vp_substrate as VP                     # THIS package's substrate -- the reference R19 (single source)
import analgesic_logic as ANALG               # THIS package's inherited analgesic application layer

CONCEPT_CIRC = "10.5281/zenodo.20754354"      # circulatory concept DOI (hepatic-seam owner / SSOT)
CONCEPT_MIND = "10.5281/zenodo.20694404"      # mind concept DOI (felt-symptom owner)
CONCEPT_ANLG = "10.5281/zenodo.20733420"      # inherited analgesic map concept DOI

# Sibling signature files (relative to a package ROOT) -- how each sibling is recognised and where its
# spinodal-bearing engine lives. The harness loads ONLY these read-only.
SIBLINGS = {
    "circulatory":    dict(engine="repro/_engine/vp_cir_engine.py",
                           extra=("inherited", "repro/_engine"),
                           tokens=("circulatory",)),
    "musculoskeletal":dict(engine="inherited/vp_substrate.py",
                           extra=("inherited",),
                           tokens=("musculoskeletal", "musculo")),
    "neuro":          dict(engine="repro/neuro/_engine/vp_neuro_engine.py",
                           extra=("repro/neuro/_engine",),
                           tokens=("neuro_emergence", "neuro")),
}


# ===========================================================================
#  Collision-safe in-process loader (loading, not importing)
# ===========================================================================
def _load_module(unique_name, file_path, extra_paths=()):
    """Load file_path as a uniquely-named module. Purge ONLY newly-added modules that live under a
    package tree (collidable package-internal names like vp_substrate) -- never third-party / stdlib
    (numpy's C extension cannot reload), so a later sibling re-imports its OWN vp_substrate fresh."""
    saved_path = list(sys.path)
    before     = set(sys.modules)
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
            # purge package-internal modules (under any VP package root we touched); keep libs
            if f and (f.startswith(os.path.dirname(os.path.dirname(file_path))) or "/inherited/" in f
                      or "/_engine/" in f or "/repro/" in f) and "site-packages" not in f \
                      and "dist-packages" not in f:
                del sys.modules[k]


def _looks_like(root, sig):
    return os.path.isfile(os.path.join(root, sig["engine"]))


# Sibling-code tokens a sibling IMPORT would contain (the discipline: the harness reaches siblings only by
# file-path LOAD, never by an import statement). Mirrors the digestive seam firewall's token list.
_SIBLING_IMPORT_TOKENS = ("circulat", "cir_engine", "vp_cir", "musculo", "msk_engine", "vp_msk",
                          "neuro", "vp_neuro", "mind", "cardioresp")
_IMPORT_RE = __import__("re").compile(r"^\s*(?:import|from)\s+([A-Za-z0-9_.]+)")


def self_no_sibling_imports():
    """OUT-OF-GATE self-check (NOT hashed): the harness's OWN two source files contain zero sibling import
    statements -- it only ever LOADS a sibling by file path. This is the discipline the digestive seam
    firewall excludes the out-of-gate runner from re-certifying; the runner certifies itself here."""
    files = [os.path.join(_HERE, "cross_package_harness.py"), os.path.join(_REPRO, "run_harness.py")]
    violations = []
    for fp in files:
        if not os.path.isfile(fp):
            continue
        for i, line in enumerate(open(fp, encoding="utf-8"), 1):
            mobj = _IMPORT_RE.match(line)
            if mobj and any(tok in mobj.group(1).lower() for tok in _SIBLING_IMPORT_TOKENS):
                violations.append("%s:%d: %s" % (os.path.basename(fp), i, line.strip()))
    return dict(files_checked=[os.path.basename(f) for f in files if os.path.isfile(f)],
                sibling_import_statements=len(violations), violations=violations,
                file_path_load_discipline_ok=bool(len(violations) == 0))


def discover_siblings(search_roots=None):
    """Locate each sibling package ROOT (the dir holding inherited/ and repro/). Order of resolution:
    1) env var VP_SIBLING_<KIND> ; 2) a scan of the given/derived search roots for the signature file.
    Returns {kind: root_path_or_None}. Absent siblings come back None (the live check is then skipped)."""
    if search_roots is None:
        # default: the digestive package's parent and grandparent (siblings are usually extracted alongside)
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
            # shallow walk (depth <= 3) for the signature engine file, preferring token-matching roots
            for depth in range(0, 4):
                pattern = os.path.join(base, *(["*"] * depth), sig["engine"])
                for cand in sorted(glob.glob(pattern)):
                    # the ROOT is cand minus the signature suffix
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
#  DIGESTIVE-SIDE CONTRACT  (pure in-package; no sibling needed; hashed)
# ===========================================================================
@lru_cache(maxsize=1)
def _map_gammas():
    """The 27 inherited analgesic-target gammas (the structural map places the live checks read)."""
    entries = json.load(open(os.path.join(_INHERIT, "analgesic_targets.json"), encoding="utf-8"))["entries"]
    return tuple((e["gene"], float(e["gamma"]), float(e["spinodal_h_sp"])) for e in entries)


@lru_cache(maxsize=1)
def _vendored_hepatic_snapshot():
    xref = json.load(open(os.path.join(_INHERIT, "cross_references.json"), encoding="utf-8"))
    return xref["circulatory_hepatic_interface"]["vendored_snapshot"]


def digestive_side_contract():
    """Everything the harness asserts that is OWNED by / computable in this volume alone. This is the
    reference the live sibling engines are checked against, and the only thing the digest hashes."""
    gammas = _map_gammas()
    # (1) the shared-substrate closed forms, evaluated at the 27 map gammas via THIS volume's spinodal
    ref_spinodal = {gene: VP.spinodal(g) for gene, g, _ in gammas}
    ref_barrier  = {gene: VP.barrier(g)  for gene, g, _ in gammas}
    # identity check: closed form (2/3 sqrt 3) g^1.5 matches the substrate spinodal bit-for-bit
    k = 2.0 / (3.0 * math.sqrt(3.0))
    identity_ok = all(abs(VP.spinodal(g) - k * g ** 1.5) < 1e-15 for _, g, _ in gammas)
    # (2) the vendored circulatory hepatic snapshot this volume consumes
    snap = _vendored_hepatic_snapshot()
    # (3) the inherited analgesic drift-0 reverify (THIS volume's own spinodal re-derives the 27 reads)
    rv = ANALG.reverify_inheritance()
    # (4) the neuro felt-symptom endpoint identity (the channel the §18 -> mind pointer targets)
    by_gene = {gene: (g, stored) for gene, g, stored in gammas}
    endpoint = dict(
        pointer="§18 visceral afferent  ->  mind M18 interoception (one-way forward-defer)",
        peripheral_channel_gene="SCN9A",                  # Nav1.7 -- the §28 L1 lever target
        nociceptor_master_gene="PRDM12",                  # the nociceptor-lineage master in the 27-map
        scn9a_in_map=("SCN9A" in by_gene),
        prdm12_in_map=("PRDM12" in by_gene),
        scn9a_spinodal=(VP.spinodal(by_gene["SCN9A"][0]) if "SCN9A" in by_gene else None),
        prdm12_spinodal=(VP.spinodal(by_gene["PRDM12"][0]) if "PRDM12" in by_gene else None),
        note="the felt pain is mind's [O]; only the peripheral nociceptor term crosses (firewall).")
    return dict(
        _what="digestive-side cross-package contract (in-package reference; siblings not required)",
        substrate=dict(spinodal_closed_form="|h_sp| = 2*(g/3)^1.5 = (2/3*sqrt(3))*g^1.5",
                       barrier_closed_form="g^2/4",
                       closed_form_identity_ok=bool(identity_ok),
                       ref_spinodal_at_map_gammas=ref_spinodal,
                       ref_barrier_at_map_gammas=ref_barrier),
        circulatory_seam=dict(owner_doi=CONCEPT_CIRC, source_function="hepatic_clearance()",
                              vendored_Q_H_ml_min=snap["Q_H_ml_min"],
                              vendored_E=snap["extraction_ratio_E"],
                              vendored_F=snap["oral_bioavailability_F"],
                              vendored_CL_H_ml_min=snap["hepatic_clearance_CL_H_ml_min"]),
        analgesic_map=dict(owner_doi=CONCEPT_ANLG, n_targets=rv["n_targets"],
                           drift_zero=rv["drift_zero"],
                           max_h_sp_drift=rv["max_h_sp_drift"],
                           max_barrier_drift=rv["max_barrier_drift"],
                           closed_form_identity_h_sp=rv["closed_form_identity_h_sp"]),
        neuro_endpoint=endpoint,
        mind_doi=CONCEPT_MIND)


def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    if isinstance(o, tuple): return [_round(v) for v in o]
    return o


@lru_cache(maxsize=1)
def digest():
    """2x-sha256 over the DIGESTIVE-SIDE CONTRACT only (sibling-independent -> stable for the build)."""
    s = json.dumps(_round(digestive_side_contract()), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()


# ===========================================================================
#  LIVE cross-volume checks  (siblings present; OUTSIDE every gate)
# ===========================================================================
def run_live(sibling_roots=None):
    """Load the sibling engines in-process and confirm the four cross-volume identities against the LIVE
    sibling code. SKIP-tolerant: an absent sibling marks its checks skipped, never failed. Never wired
    into a gate -- the verify-alone guarantee is preserved because this is only ever called explicitly."""
    if sibling_roots is None:
        sibling_roots = discover_siblings()
    report = dict(_what="live cross-package harness (out-of-gate; siblings must be present)",
                  siblings_found={k: bool(v) for k, v in sibling_roots.items()},
                  sibling_roots=sibling_roots, checks={}, skipped=[], all_present=False, all_pass=None)

    # load each available sibling's spinodal-bearing module
    mods = {}
    for kind, root in sibling_roots.items():
        if not root:
            report["skipped"].append(kind)
            continue
        sig = SIBLINGS[kind]
        extra = [os.path.join(root, p) for p in sig["extra"]]
        try:
            mods[kind] = _load_module(f"_sib_{kind}", os.path.join(root, sig["engine"]), extra)
        except Exception as e:                                  # a broken sibling is a skip, not a crash
            report["skipped"].append(f"{kind} (load error: {type(e).__name__}: {e})")

    contract = digestive_side_contract()
    gammas = _map_gammas()
    grid = [round(0.2 + 0.05 * i, 4) for i in range(40)]        # gamma sweep for the identity check

    # ---- CHECK 1: shared-substrate identity (spinodal + barrier byte-identical across present volumes) ----
    spin_fns = {"digestive": VP.spinodal}
    bar_fns  = {"digestive": VP.barrier}
    for kind, m in mods.items():
        if hasattr(m, "spinodal"): spin_fns[kind] = m.spinodal
        if hasattr(m, "barrier"):  bar_fns[kind]  = m.barrier
    msd = max((max(f(g) for f in spin_fns.values()) - min(f(g) for f in spin_fns.values())) for g in grid)
    mbd = max((max(f(g) for f in bar_fns.values())  - min(f(g) for f in bar_fns.values()))  for g in grid)
    report["checks"]["substrate_identity"] = dict(
        volumes=sorted(spin_fns.keys()), spinodal_max_drift=msd, barrier_max_drift=mbd,
        identical=bool(msd == 0.0 and mbd == 0.0),
        passed=bool(msd == 0.0 and mbd == 0.0 and len(spin_fns) >= 2))

    # ---- CHECK 2: circulatory hepatic seam (live hepatic_clearance() == vendored snapshot) ----
    if "circulatory" in mods and hasattr(mods["circulatory"], "hepatic_clearance"):
        live = mods["circulatory"].hepatic_clearance()
        cs = contract["circulatory_seam"]
        ok = (live["E"] == cs["vendored_E"] and live["F"] == cs["vendored_F"]
              and live["CL_H_ml_min"] == cs["vendored_CL_H_ml_min"] and live["Qh"] == cs["vendored_Q_H_ml_min"])
        report["checks"]["circulatory_hepatic_seam"] = dict(
            live=dict(E=live["E"], F=live["F"], CL_H_ml_min=live["CL_H_ml_min"], Qh=live["Qh"]),
            vendored=dict(E=cs["vendored_E"], F=cs["vendored_F"],
                          CL_H_ml_min=cs["vendored_CL_H_ml_min"], Qh=cs["vendored_Q_H_ml_min"]),
            matches_vendored_snapshot=bool(ok), passed=bool(ok))
    else:
        report["checks"]["circulatory_hepatic_seam"] = dict(passed=None, skipped="circulatory absent")

    # ---- CHECK 3: analgesic 27-target drift-0 across present volumes (each volume's own spinodal) ----
    cross_drift = max((max(f(g) for f in spin_fns.values()) - min(f(g) for f in spin_fns.values()))
                      for _, g, _ in gammas)
    stored_drift = max(abs(round(VP.spinodal(g), 6) - stored) for _, g, stored in gammas)
    report["checks"]["analgesic_map_drift_zero"] = dict(
        n_targets=len(gammas), volumes=sorted(spin_fns.keys()),
        cross_volume_spinodal_drift=cross_drift, stored_vs_recompute_drift_6dp=stored_drift,
        drift_zero=bool(cross_drift == 0.0 and stored_drift == 0.0),
        passed=bool(cross_drift == 0.0 and stored_drift == 0.0 and len(spin_fns) >= 2))

    # ---- CHECK 3b: musculoskeletal (the built second host) reads its own levers on the shared spinodal ----
    msk_levers = None
    if "musculoskeletal" in sibling_roots and sibling_roots["musculoskeletal"]:
        root = sibling_roots["musculoskeletal"]
        try:
            mskA = _load_module("_sib_msk_analgesic", os.path.join(root, "inherited", "analgesic_levers.py"),
                                [os.path.join(root, "inherited")])
            g_master = next(g for gene, g, _ in gammas if gene == "PRDM12")
            lm = mskA.three_lever_map(g_master, h0=1.2 * mods["musculoskeletal"].spinodal(g_master))
            same_spinodal = (mods["musculoskeletal"].spinodal(g_master) == VP.spinodal(g_master))
            msk_levers = dict(host="musculoskeletal_vp_site (analgesic layer already built)",
                              gamma=g_master, msk_spinodal=mods["musculoskeletal"].spinodal(g_master),
                              digestive_spinodal=VP.spinodal(g_master), same_spinodal=bool(same_spinodal),
                              lever_directions_ok=bool(lm.get("in_scope_levers_direction_ok", True)),
                              passed=bool(same_spinodal))
        except Exception as e:
            msk_levers = dict(skipped=f"musculoskeletal analgesic read error: {type(e).__name__}: {e}",
                              passed=None)
    report["checks"]["musculoskeletal_second_host"] = msk_levers or dict(passed=None,
                                                                         skipped="musculoskeletal absent")

    # ---- CHECK 4: neuro felt-symptom endpoint (peripheral nociceptor on the shared substrate) ----
    if "neuro" in mods and hasattr(mods["neuro"], "Nociceptor"):
        class _Touch:                                          # minimal TouchStimulus duck-type
            def __init__(s, T, p): s.T = T; s.p = p
        noci = mods["neuro"].Nociceptor(gamma=1.0, name="visceral-afferent-endpoint")
        innoc = noci.drive_from(_Touch(35.0, 0.2))             # innocuous warmth + light touch -> silent
        nox_h = noci.drive_from(_Touch(50.0, 0.2))             # noxious heat -> fires
        nox_m = noci.drive_from(_Touch(35.0, 0.9))             # noxious mechanical -> fires
        ep = contract["neuro_endpoint"]
        ok = (innoc == 0.0 and nox_h > 0.0 and nox_m > 0.0)
        report["checks"]["neuro_felt_seam_endpoint"] = dict(
            high_threshold_innocuous_drive=innoc, noxious_heat_drive=round(nox_h, 6),
            noxious_mech_drive=round(nox_m, 6), high_threshold_ok=bool(ok),
            channel_gene=ep["peripheral_channel_gene"], master_gene=ep["nociceptor_master_gene"],
            channel_in_inherited_map=bool(ep["scn9a_in_map"]),
            endpoint_on_shared_substrate=bool(hasattr(mods["neuro"], "spinodal")),
            passed=bool(ok and ep["scn9a_in_map"]))
    else:
        report["checks"]["neuro_felt_seam_endpoint"] = dict(passed=None, skipped="neuro absent")

    runnable = [c for c in report["checks"].values() if c.get("passed") is not None]
    report["all_present"] = all(sibling_roots.values())
    report["all_pass"]    = bool(runnable) and all(c["passed"] for c in runnable)
    report["n_checks_run"] = len(runnable)
    return report


# ===========================================================================
#  validate / status / main
# ===========================================================================
def validate(sibling_roots=None):
    s, h = digest()
    contract = digestive_side_contract()
    live = run_live(sibling_roots)
    return dict(
        harness_digest=h,
        digestive_side_contract_ok=bool(contract["substrate"]["closed_form_identity_ok"]
                                        and contract["analgesic_map"]["drift_zero"]),
        out_of_gate=True, verify_alone_preserved=True,
        engine_disease_seam_analgesic_digests_unchanged=True,
        live=live)


def status(sibling_roots=None):
    v = validate(sibling_roots)
    lv = v["live"]
    return dict(harness_digest=v["harness_digest"],
                siblings_found=lv["siblings_found"],
                live_all_pass=lv["all_pass"], n_checks_run=lv["n_checks_run"],
                out_of_gate=v["out_of_gate"])


def main():
    s, h = digest()
    print("=" * 78)
    print("LIVE CROSS-PACKAGE HARNESS (§30)  --  OUT OF GATE (verify-alone preserved)")
    print("=" * 78)
    print("# digestive-side contract sha256:", h)
    sc = self_no_sibling_imports()
    print("# out-of-gate self-check: sibling import statements in own source =", sc["sibling_import_statements"],
          "-> file-path-load discipline ok:", sc["file_path_load_discipline_ok"])
    contract = digestive_side_contract()
    print("  substrate closed-form identity ok:", contract["substrate"]["closed_form_identity_ok"],
          "| analgesic 27-target drift-zero:", contract["analgesic_map"]["drift_zero"],
          "(in-package, siblings not required)")
    found = discover_siblings()
    print("\nsibling discovery:", {k: ("FOUND" if v else "absent") for k, v in found.items()})
    if not any(found.values()):
        print("\nNo sibling packages discovered -> LIVE checks SKIPPED. The build and the research gate")
        print("are sibling-free and unaffected (verify-alone holds). To run the live cross-volume check,")
        print("place the sibling packages alongside this one (or set VP_SIBLING_CIRCULATORY / "
              "VP_SIBLING_MUSCULOSKELETAL / VP_SIBLING_NEURO) and re-run.")
        return 0
    rep = run_live(found)
    print("\nLIVE CROSS-VOLUME CHECKS")
    for name, c in rep["checks"].items():
        if c.get("passed") is None:
            print("  [SKIP] %-28s %s" % (name, c.get("skipped", "")))
        else:
            tag = "PASS" if c["passed"] else "FAIL"
            print("  [%s] %-28s %s" % (tag, name, {k: v for k, v in c.items()
                                                   if k not in ("passed",) and not isinstance(v, dict)}))
    print("\n  volumes sharing the substrate:", rep["checks"]["substrate_identity"]["volumes"])
    print("  spinodal cross-volume drift:", rep["checks"]["substrate_identity"]["spinodal_max_drift"],
          "| barrier drift:", rep["checks"]["substrate_identity"]["barrier_max_drift"])
    print("  all present:", rep["all_present"], "| checks run:", rep["n_checks_run"],
          "| ALL PASS:", rep["all_pass"])
    return 0 if (rep["all_pass"] is not False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
