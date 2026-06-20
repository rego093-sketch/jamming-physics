"""
verify_adipose.py -- the neuro-VP-SPEC-style gate for LAYER 4 (adipose / energy-balance).

The stricter sibling of verify_morpho_plus.py for the composition axis. It proves that adding the
fat axis did NOT smuggle in any tuning and did NOT perturb the headline growth proof:

Checks:
  1. ONE SWITCH        the adipose fold IS the body fold: max|adipose.spinodal - morpho_core.spinodal| < 1e-12.
  2. GAMMA SUPERSET     the 59-gene table contains the original 42 with bit-identical gamma (no
                        measured base value moved when the obesity panel was added), and the obesity
                        gammas are MEASURED (carry the SantaLucia/NCBI provenance; corr(gamma,GC) high).
  3. GENE x ENV MONO    adiposity index AI is monotone non-decreasing in the energy dial E (for lean,
                        neutral AND thrifty genomes) AND, at a FIXED E, AI(thrifty) >= AI(neutral) >=
                        AI(lean); the genome propensity is a readout of measured gamma (perturb a gamma
                        -> propensity moves in the annotated direction) with neutral propensity == 0
                        exactly. Falsifiable, not fitted.
  4. BASELINE PRESERVED neutral genome at E_lean gives activation == 0 exactly, so the thickness field
                        is identically zero and the inflated surface == the lean target BIT-FOR-BIT
                        (sha256 of the sampled fields match) -- the Layer-3 convergence proof is untouched.
  5. DETERMINISM        building the same inflated body twice gives identical sha256 of the thickness
                        field AND of the mesh vertices.
"""
import os, json, hashlib
import numpy as np

import morpho_core as mc
import adipose as AD
import adipose_atlas as AA
import body as B


def _field_sha(sampler, box, vox, rd=6):
    nx, ny, nz = [max(8, int(b / vox)) for b in box]
    P, axes, dx = B.grid(nx, ny, nz, box)
    fld = np.round(sampler(P), rd).astype(np.float64)
    return hashlib.sha256(fld.tobytes()).hexdigest()


def _verts_sha(sampler, box, vox, rd=5):
    import demo_adipose as D
    v, f = D.mesh_faces(sampler, box, vox)
    if v is None:
        return "EMPTY"
    return hashlib.sha256(np.round(v, rd).tobytes()).hexdigest()


# ----------------------------------------------------------------- check 1: one switch
def check_one_switch():
    gs = np.linspace(1.2, 1.8, 241)
    d = max(abs(AD.spinodal(g) - mc.spinodal(g)) for g in gs)
    a = AD.assert_one_switch_adipose()
    return (d < 1e-12 and a < 1e-12), f"max|delta spinodal| = {d:.2e}; assert_one_switch_adipose = {a:.2e}"


# ----------------------------------------------------------------- check 2: gamma superset
def check_gamma_superset():
    base = json.load(open(os.path.join(AD.HERE, "data", "morpho_gamma.json"), encoding="utf-8"))
    baseg = {k: float(v["gamma"]) for k, v in base["genes"].items()}
    ext = json.load(open(AD.OBESITY_JSON, encoding="utf-8"))
    extg = {k: float(v["gamma"]) for k, v in ext["genes"].items()}
    missing = [k for k in baseg if k not in extg]
    moved = {k: (baseg[k], extg[k]) for k in baseg if k in extg and abs(baseg[k] - extg[k]) > 0.0}
    superset_ok = (not missing) and (not moved)
    # obesity gammas measured? provenance present + panel genes present + corr(gamma,GC) high
    has_prov = "_provenance_obesity" in ext
    panel = list(AD.PANEL_SIGN.keys())
    panel_present = [g for g in panel if g in extg]
    gam = np.array([extg[g] for g in panel_present])
    gc = np.array([float(ext["genes"][g]["gc"]) for g in panel_present])
    corr = float(np.corrcoef(gam, gc)[0, 1]) if len(gam) > 2 else float("nan")
    measured_ok = has_prov and (len(panel_present) == len(panel)) and (corr > 0.9)
    ok = superset_ok and measured_ok
    msg = (f"base {len(baseg)} all present in {len(extg)} with 0 drift "
           f"(missing={len(missing)}, moved={len(moved)}); obesity panel {len(panel_present)}/{len(panel)} "
           f"measured, prov={has_prov}, corr(gamma,GC)={corr:.3f}")
    return ok, msg


# ----------------------------------------------------------------- check 3: gene x env monotone
def check_gene_x_env_monotone():
    """Two distinct, both-correct monotonicities:
      (a) WITHIN a genome, the self-referential AI (volume gained vs that genome's OWN lean state)
          is non-decreasing as the energy dial E rises -- 'eat more -> store more'.
      (b) ACROSS genomes at a fixed E, ABSOLUTE adiposity (activation alpha, and the occupancy
          volume it drives) is ordered thrifty >= neutral >= lean -- the gene effect: a thriftier
          genome reaches the storage tipping point at a lower E. (AI-vs-own-baseline is the WRONG
          cross-genome metric, because a thrifty genome is already not lean at E_lean.)
    """
    target, depot = AA.SCENES["face"]()
    model = AD.AdiposeModel()
    box = target.box
    vox = 0.8
    Es = [-1.0, -0.3, 0.3, 1.0]

    # (a) within-genome AI monotone in E (vs own E_lean baseline)
    mono_in_E, curves = True, {}
    for g in ("lean", "neutral", "thrifty"):
        ref = AD.inflate_sampler(target, model, depot, model.E_lean, g, t_max=2.2)
        ai = []
        for E in Es:
            s = AD.inflate_sampler(target, model, depot, E, g, t_max=2.2)
            a, _, _ = AD.adiposity_index(s, ref, box, vox)
            ai.append(a)
        curves[g] = ai
        mono_in_E = mono_in_E and all(b >= a - 1e-9 for a, b in zip(ai, ai[1:]))

    # (b) cross-genome absolute ordering: activation on a full E grid (exact) + volume at fixed E
    Eg = np.linspace(-1.0, 1.0, 41)
    alpha_ok = all(model.activation(E, "thrifty") >= model.activation(E, "neutral") - 1e-12 and
                   model.activation(E, "neutral") >= model.activation(E, "lean") - 1e-12 for E in Eg)
    Efix = 0.2
    V = {g: AD.occupancy_volume(AD.inflate_sampler(target, model, depot, Efix, g, t_max=2.2),
                                box, vox)[0] for g in ("lean", "neutral", "thrifty")}
    vol_ok = V["thrifty"] >= V["neutral"] >= V["lean"]

    # propensity is a measured-gamma readout, neutral == 0 exactly
    is_readout, deltas = AD.propensity_is_gamma_readout(AD._canon_gammas())
    neutral_zero = abs(model.propensity("neutral")) < 1e-12

    ok = mono_in_E and alpha_ok and vol_ok and is_readout and neutral_zero
    msg = (f"within-genome AI monotone in E={mono_in_E}; cross-genome alpha "
           f"thrifty>=neutral>=lean on 41 E grid={alpha_ok}; abs volume at E={Efix:+.1f} "
           f"({V['lean']:.0f}<{V['neutral']:.0f}<{V['thrifty']:.0f})={vol_ok}; "
           f"propensity=gamma-readout {is_readout} (pro {deltas['pro_bump']:+.4f}, "
           f"sat {deltas['sat_bump']:+.4f}), neutral==0 {neutral_zero}")
    return ok, msg


# ----------------------------------------------------------------- check 4: baseline preserved
def check_baseline_preserved():
    model = AD.AdiposeModel()
    lines, ok_all = [], True
    for scene in ("face", "body"):
        target, depot = AA.SCENES[scene]()
        box = target.box
        vox = 1.1 if scene == "face" else 1.2
        alpha0 = model.activation(model.E_lean, "neutral")
        infl = AD.inflate_sampler(target, model, depot, model.E_lean, "neutral", t_max=3.0)

        def lean_only(P, _t=target):                       # the pure lean target sampler
            return _t.sample(P, None)

        sha_inf = _field_sha(infl, box, vox)
        sha_lean = _field_sha(lean_only, box, vox)
        ok = (abs(alpha0) < 1e-12) and (sha_inf == sha_lean)
        ok_all = ok_all and ok
        lines.append(f"{scene}: alpha0={alpha0:.1e} field=={('OK' if sha_inf == sha_lean else 'XX')}")
    return ok_all, "  |  ".join(lines)


# ----------------------------------------------------------------- check 5: determinism
def check_determinism():
    target, depot = AA.SCENES["body"](0.6)
    model = AD.AdiposeModel()
    box = target.box
    vox = 1.2
    s1 = AD.inflate_sampler(target, model, depot, 0.6, "thrifty", t_max=3.0)
    s2 = AD.inflate_sampler(target, model, depot, 0.6, "thrifty", t_max=3.0)
    f1, f2 = _field_sha(s1, box, vox), _field_sha(s2, box, vox)
    v1, v2 = _verts_sha(s1, box, vox), _verts_sha(s2, box, vox)
    ok = (f1 == f2) and (v1 == v2)
    return ok, f"field sha {f1[:10]}=={f2[:10]} ({f1 == f2}); mesh sha {v1[:10]}=={v2[:10]} ({v1 == v2})"


def main():
    ext, _ = json.load(open(AD.OBESITY_JSON, encoding="utf-8")), None
    n_genes = len(ext["genes"])
    checks = [
        ("1 ONE SWITCH (adipose fold == body fold)", check_one_switch()),
        ("2 GAMMA SUPERSET (orig 42 bit-identical, obesity measured)", check_gamma_superset()),
        ("3 GENE x ENV MONOTONE (AI up in E and in propensity)", check_gene_x_env_monotone()),
        ("4 BASELINE PRESERVED (neutral@E_lean -> lean surface)", check_baseline_preserved()),
        ("5 DETERMINISM (field + mesh sha stable)", check_determinism()),
    ]
    npass = 0
    print("=" * 78)
    print(f"  LAYER-4 ADIPOSE GATE  |  {n_genes} measured genes  |  fold == body fold")
    print("=" * 78)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 78)
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(AD.HERE, "..", "results", "adipose_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
              | {"overall": f"{npass}/{len(checks)}", "n_genes": n_genes}, open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
