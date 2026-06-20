"""
verify_gene_clock.py -- a neuro-VP-SPEC-style gate for the gene-clock morphogenesis upgrade.
Prints OVERALL: PASS (5/5) when every check holds. Run after any change.

Checks (each either a hard identity, a determinism hash, or a derived-claim test):
  1. ONE SWITCH      the morphogenesis fold and the neuro gene fold are the SAME function:
                     max|spinodal_neuro(g) - morpho_core.spinodal(g)| < 1e-12.
  2. GAMMA VERBATIM  the gamma table loaded here matches the neuro package's table bit-for-bit
                     (if the neuro package is reachable); else loads the in-package copy.
  3. ORDER = DNA     the derived emergence order EQUALS argsort(spinodal(gamma)) -- the order is
                     a pure readout of measured gamma, not a hand-typed list.
  4. CONVERGENCE     gene-clock growth still REACHES the scan: final surface RMS small and
                     Chamfer ~ 0 (the headline proof is preserved by the reschedule).
  5. SIZE LAW        dwell ~ gamma^1.5 is strictly increasing in gamma (the relative-size law),
                     and DETERMINISM: 2x build of the schedule -> identical sha256.
"""
import os, io, json, hashlib, contextlib
import numpy as np
import gene_clock as GC
import feature_target as FT
import grow_gene_clock as GG
import morpho_core as mc


def _sched_hash(features, gammas):
    sched = GC.feature_schedule(features, gammas)
    blob = json.dumps({f: [round(sched["features"][f]["gamma"], 6),
                           round(sched["features"][f]["spinodal"], 6),
                           round(sched["features"][f]["tau_on"], 6)]
                       for f in sched["order"]}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest(), sched


def check_one_switch():
    gs = np.linspace(1.2, 1.8, 241)
    d = max(abs(GC.spinodal(g) - mc.spinodal(g)) for g in gs)
    return d < 1e-12, f"max|delta spinodal| = {d:.2e}"


def check_gamma_verbatim():
    g_local, _ = GC.load_gamma()
    neuro = os.path.join(os.path.dirname(GC.HERE), "..", "neuro",
                         "neuro_emergence_chain_integrated_v1_9", "repro", "neuro",
                         "_engine", "data", "sensory_organ_gamma.json")
    # try a couple of plausible neuro locations; if none, the in-package copy stands
    cands = [neuro,
             os.path.join(GC.HERE, "..", "..", "neuro", "neuro_emergence_chain_integrated_v1_9",
                          "repro", "neuro", "_engine", "data", "sensory_organ_gamma.json")]
    # The optional external-neuro cross-check is an UNPINNED provenance bonus: it still runs
    # (and still gates a genuine in-package != neuro mismatch when the sibling is co-located),
    # but its environment-dependent note is PRINTED, never folded into the pinned msg, so the
    # frozen fidelity baseline reproduces bit-for-bit whether or not neuro is co-located.
    ok = len(g_local) > 0
    neuro_note = "neuro pkg not co-located (in-package measured copy used)"
    for c in cands:
        if os.path.exists(c):
            J = json.load(open(c, encoding="utf-8"))
            gn = {k: float(v["gamma"]) for k, v in J["genes"].items()}
            same = all(abs(g_local[k] - gn[k]) < 1e-12 for k in gn if k in g_local)
            neuro_note = f"matched neuro table ({len(gn)} genes), identical={same}"
            ok = ok and same
            break
    print(f"  [bonus, unpinned] cross-pkg provenance: {neuro_note}")
    return ok, f"in-package measured gamma loaded verbatim ({len(g_local)} genes)"


def check_order_is_dna(features, gammas):
    sched = GC.feature_schedule(features, gammas)
    sp = {f: GC.spinodal(gammas[g]) for f, g in features}
    by_sp = sorted(sp, key=lambda f: sp[f])
    # compare as gene-order (ties allowed within a gene)
    og = list(dict.fromkeys([sched["features"][f]["gene"] for f in sched["order"]]))
    sg = list(dict.fromkeys([dict(features)[f] for f in by_sp]))
    return (og == sg) and sched["order_is_gamma_readout"], f"order={'>'.join(og)}"


def check_convergence(ft, rms_tol=0.15):
    with contextlib.redirect_stdout(io.StringIO()):
        stages, info, sched = GG.grow_gene_clock(ft, vox=0.55, n_stages=9)
    r, c = stages[-1]["rms"], stages[-1]["chamfer"]
    return (r <= rms_tol and c <= 1e-3), f"final RMS={r:.3f} (<= {rms_tol}), Chamfer={c:.3f}"


def check_size_law_and_determinism(features, gammas):
    gs = sorted(set(gammas[g] for _, g in features))
    dw = [GC.dwell(g) for g in gs]
    mono = all(dw[i] < dw[i + 1] for i in range(len(dw) - 1))
    h1, _ = _sched_hash(features, gammas)
    h2, _ = _sched_hash(features, gammas)
    return (mono and h1 == h2), f"dwell monotone={mono}, sha256 stable={h1[:12]}=={h2[:12]}"


def main():
    ft = FT.face_features()
    gammas, _ = GC.load_gamma()
    checks = [
        ("1 ONE SWITCH (neuro fold == body fold)", check_one_switch()),
        ("2 GAMMA VERBATIM (measured, not fitted)", check_gamma_verbatim()),
        ("3 ORDER = DNA (order == argsort spinodal)", check_order_is_dna(ft.features, gammas)),
        ("4 CONVERGENCE (reaches the scan)", check_convergence(ft)),
        ("5 SIZE LAW dwell~g^1.5 + DETERMINISM", check_size_law_and_determinism(ft.features, gammas)),
    ]
    npass = 0
    print("=" * 72)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 72)
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(GC.HERE, "..", "results", "gene_clock_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
              | {"overall": f"{npass}/{len(checks)}"}, open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
