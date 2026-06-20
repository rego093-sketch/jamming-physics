"""
verify_morpho_plus.py -- the neuro-VP-SPEC-style gate for the EXPANDED gene-clock atlas.
Prints OVERALL: PASS (5/5) when every check holds, for ALL FOUR organisms at once.
Run after any change. This is the stricter sibling of verify_gene_clock.py: it proves the
richer atlas (hair / brow / lash / iris / teeth + bird / quadruped / fish appendages) did NOT
weaken any invariant, and -- crucially -- that EXTENDING the gamma table left the original 26
measured values bit-for-bit untouched (no tuning crept in through the back door).

Checks:
  1. ONE SWITCH       the morphogenesis fold and the neuro gene fold are the SAME function:
                      max|spinodal_neuro(g) - morpho_core.spinodal(g)| < 1e-12.
  2. GAMMA SUPERSET   the EXTENDED 42-gene table contains the original 26 genes with bit-identical
                      gamma (extending the atlas did not perturb a single measured base value);
                      and, if the neuro package is reachable, those 26 still match it bit-for-bit.
  3. ORDER = DNA x4   for EACH organism the derived emergence order EQUALS argsort(spinodal(gamma))
                      -- a pure readout of measured gamma, not a hand-typed list.
  4. CONVERGENCE x4   gene-clock growth still REACHES the scan for EACH organism: final surface
                      RMS small and Chamfer ~ 0 (the headline proof survives the richer atlas).
  5. SIZE LAW + DET   dwell ~ gamma^1.5 strictly increasing in gamma over the FULL 42-gene set,
                      schedule sha256 stable across 2 builds, AND mesh-level determinism:
                      growing an organism twice -> identical sha256 of its vertex set.
"""
import os, io, json, hashlib, contextlib
import numpy as np
import gene_clock as GC
import feature_atlas_plus as FA
import grow_gene_clock as GG
import morpho_core as mc

GC.load_gamma = GC.load_gamma_table          # the atlas grows on the EXTENDED measured table
ORGANISMS = ["human_head", "bird", "quadruped", "fish"]
VOX = {"human_head": 0.60, "bird": 0.60, "quadruped": 0.66, "fish": 0.60}   # coarse = fast gate


def _gene_order(sched):
    return list(dict.fromkeys([sched["features"][f]["gene"] for f in sched["order"]]))


def _sched_hash(features, gammas):
    sched = GC.feature_schedule(features, gammas)
    blob = json.dumps({f: [round(sched["features"][f]["gamma"], 6),
                           round(sched["features"][f]["spinodal"], 6),
                           round(sched["features"][f]["tau_on"], 6)]
                       for f in sched["order"]}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


def _verts_hash(ft, vox):
    with contextlib.redirect_stdout(io.StringIO()):
        stages, _, _ = GG.grow_gene_clock(ft, vox=vox, n_stages=5)
    v = np.round(stages[-1]["verts"], 5)
    return hashlib.sha256(v.tobytes()).hexdigest()


# ----------------------------------------------------------------- check 1: one switch
def check_one_switch():
    gs = np.linspace(1.2, 1.8, 241)
    d = max(abs(GC.spinodal(g) - mc.spinodal(g)) for g in gs)
    return d < 1e-12, f"max|delta spinodal| = {d:.2e}"


# ----------------------------------------------------------------- check 2: gamma superset
def check_gamma_superset():
    # read the base-26 table straight from disk (NOT via GC.load_gamma, which is monkeypatched
    # to the extended table at import time) so this comparison is genuinely 26-vs-42.
    Jb = json.load(open(GC.GAMMA_JSON, encoding="utf-8"))
    base = {k: float(v["gamma"]) for k, v in Jb["genes"].items()}
    ext, _ = GC.load_gamma_table()                  # extended 42
    missing = [k for k in base if k not in ext]
    moved = {k: (base[k], ext[k]) for k in base if k in ext and abs(base[k] - ext[k]) > 0.0}
    superset_ok = (not missing) and (not moved)
    # The optional external-neuro cross-check is an UNPINNED provenance bonus: it still runs
    # (and still gates a genuine in-package base-26 != neuro mismatch when the sibling is
    # co-located), but its environment-dependent note is PRINTED, never folded into the pinned
    # msg, so the frozen fidelity baseline reproduces bit-for-bit with or without neuro present.
    cands = [os.path.join(GC.HERE, "..", "..", "neuro_emergence_chain_integrated_v1_9",
                          "repro", "neuro", "_engine", "data", "sensory_organ_gamma.json"),
             os.path.join(GC.HERE, "..", "..", "neuro", "neuro_emergence_chain_integrated_v1_9",
                          "repro", "neuro", "_engine", "data", "sensory_organ_gamma.json")]
    neuro_note = "neuro pkg not co-located (in-package base used)"
    for c in cands:
        if os.path.exists(c):
            J = json.load(open(c, encoding="utf-8"))
            gn = {k: float(v["gamma"]) for k, v in J["genes"].items()}
            nsame = all(abs(base[k] - gn[k]) < 1e-12 for k in gn if k in base)
            neuro_note = f"base 26 == neuro table bit-for-bit: {nsame} ({len(gn)} genes)"
            superset_ok = superset_ok and nsame
            break
    print(f"  [bonus, unpinned] cross-pkg provenance: {neuro_note}")
    msg = (f"base {len(base)} genes all present in extended {len(ext)} with 0 value drift "
           f"(missing={len(missing)}, moved={len(moved)})")
    return superset_ok, msg


# ----------------------------------------------------------------- check 3: order = DNA x4
def check_order_is_dna_all(gammas):
    lines, ok_all = [], True
    for name in ORGANISMS:
        ft = FA.ATLAS[name]()
        sched = GC.feature_schedule(ft.features, gammas)
        sp = {f: GC.spinodal(gammas[g]) for f, g in ft.features}
        by_sp = sorted(sp, key=lambda f: sp[f])
        og = _gene_order(sched)
        sg = list(dict.fromkeys([dict(ft.features)[f] for f in by_sp]))
        ok = (og == sg) and sched["order_is_gamma_readout"]
        ok_all = ok_all and ok
        lines.append(f"{name}: {'OK' if ok else 'XX'} {'>'.join(og)}")
    return ok_all, "  |  ".join(lines)


# ----------------------------------------------------------------- check 4: convergence x4
def check_convergence_all(rms_tol=0.15):
    lines, ok_all = [], True
    for name in ORGANISMS:
        ft = FA.ATLAS[name]()
        with contextlib.redirect_stdout(io.StringIO()):
            stages, info, sched = GG.grow_gene_clock(ft, vox=VOX[name], n_stages=9)
        r, c = stages[-1]["rms"], stages[-1]["chamfer"]
        npres = sum(1 for a in stages[-1]["present"].values() if a > 0.5)
        ok = (r <= rms_tol and c <= 1e-3 and npres == len(ft.features))
        ok_all = ok_all and ok
        lines.append(f"{name}: {'OK' if ok else 'XX'} RMS {r:.3f} Chamfer {c:.4f} "
                     f"{npres}/{len(ft.features)}")
    return ok_all, "  |  ".join(lines)


# ----------------------------------------------------------------- check 5: size law + det
def check_size_law_and_determinism(gammas):
    # size law over the FULL measured set
    gs = sorted(set(gammas.values()))
    dw = [GC.dwell(g) for g in gs]
    mono = all(dw[i] < dw[i + 1] for i in range(len(dw) - 1))
    # schedule determinism on the largest atlas (human head)
    ft = FA.ATLAS["human_head"]()
    h1 = _sched_hash(ft.features, gammas)
    h2 = _sched_hash(ft.features, gammas)
    sched_det = (h1 == h2)
    # mesh-level determinism: grow the bird twice (coarse) -> identical vertices
    bird = FA.ATLAS["bird"]()
    m1 = _verts_hash(bird, 0.8)
    m2 = _verts_hash(bird, 0.8)
    mesh_det = (m1 == m2)
    ok = mono and sched_det and mesh_det
    return ok, (f"dwell monotone over {len(gs)} gammas={mono}; sched sha {h1[:10]}=={h2[:10]} "
                f"({sched_det}); mesh sha {m1[:10]}=={m2[:10]} ({mesh_det})")


def main():
    gammas, prov = GC.load_gamma_table()
    checks = [
        ("1 ONE SWITCH (neuro fold == body fold)", check_one_switch()),
        ("2 GAMMA SUPERSET (base 26 bit-identical)", check_gamma_superset()),
        ("3 ORDER = DNA  x4 organisms", check_order_is_dna_all(gammas)),
        ("4 CONVERGENCE x4 organisms (reaches scan)", check_convergence_all()),
        ("5 SIZE LAW dwell~g^1.5 + DETERMINISM", check_size_law_and_determinism(gammas)),
    ]
    npass = 0
    print("=" * 78)
    print(f"  EXPANDED GENE-CLOCK GATE  |  {len(gammas)} measured genes  |  "
          f"{len(ORGANISMS)} organisms")
    print("=" * 78)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 78)
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(GC.HERE, "..", "results", "morpho_plus_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
              | {"overall": f"{npass}/{len(checks)}", "n_genes": len(gammas),
                 "organisms": ORGANISMS}, open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
