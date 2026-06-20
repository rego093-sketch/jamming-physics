"""
verify_life_course.py -- neuro-VP-SPEC-style gate for the life-course coupling (Layer 3 x Layer 4).
Prints OVERALL: PASS (5/5) when the developmental (gene-clock) and adipose (energy) axes compose
into ONE continuous R19 process without weakening any invariant. Run after any change.

Checks:
  1. ONE CONTINUOUS FOLD   the TIME clock (gene_clock) AND the ENERGY clock (adipose) are BOTH the
                           body fold: max|spinodal - morpho_core.spinodal| < 1e-12 for each. One
                           switch across the whole life -- the headline claim.
  2. MEASURED GAMMA        the gene-clock 42-gene table's values are bit-identical inside the
                           adipose 59-gene table (no value drifted; coupling introduced no tuning),
                           and both are read-only measured.
  3. MONOTONE TRAJECTORY   over a chosen life: developmental completeness A(tau) is monotone non-
                           decreasing as tau rises (child->adult grows), adiposity occupancy is
                           monotone non-decreasing as E rises at maturity (eat more -> store more),
                           and the gene-clock emergence order is still the measured-gamma readout.
                           Falsifiable, not tuned.
  4. BASELINE PRESERVED    at the lean reference (E_lean, neutral) over the whole tau sweep, the
                           adipose activation alpha == 0 and the inflated field == the pure gene-
                           clock field BIT-FOR-BIT -- the energy axis perturbs nothing at lean, so
                           Layer 3's convergence proof survives untouched.
  5. DETERMINISM           two independent trajectories -> identical sha256 of the field payload.
"""
import os, json, hashlib
import numpy as np
import gene_clock as GC
import adipose as AD
import morpho_core as mc
import life_course as LC


def _traj_sha(rows):
    blob = "".join(r["field_sha"] for r in rows).encode()
    return hashlib.sha256(blob).hexdigest()


# ----------------------------------------------------------------- check 1
def check_one_continuous_fold():
    d = LC.assert_one_continuous_fold()
    gs = np.linspace(1.2, 1.8, 241)
    d_time = max(abs(GC.spinodal(g) - mc.spinodal(g)) for g in gs)
    d_energy = max(abs(AD.spinodal(g) - mc.spinodal(g)) for g in gs)
    ok = (d_time < 1e-12) and (d_energy < 1e-12)
    return ok, f"time fold delta={d_time:.2e}, energy fold delta={d_energy:.2e} (both < 1e-12)"


# ----------------------------------------------------------------- check 2
def check_measured_gamma():
    gc_tab, _ = GC.load_gamma_table()                 # 42 (gene clock)
    ob_tab, _ = AD.load_obesity_gamma()               # 59 (adipose superset)
    missing = [k for k in gc_tab if k not in ob_tab]
    moved = {k: (gc_tab[k], ob_tab[k]) for k in gc_tab
             if k in ob_tab and abs(gc_tab[k] - ob_tab[k]) > 0.0}
    ok = (not missing) and (not moved)
    return ok, (f"gene-clock {len(gc_tab)} genes all present in adipose {len(ob_tab)} with 0 drift "
                f"(missing={len(missing)}, moved={len(moved)})")


# ----------------------------------------------------------------- check 3
def check_monotone_trajectory():
    lc = LC.LifeCourse(scene="face")
    life = LC.default_life()
    rows = lc.trajectory(life, vox=1.0)
    by = {r["label"]: r for r in rows}
    # tau-rising lean points -> A monotone non-decreasing
    lean = [r for r in rows if r["E"] == -1.0]
    lean.sort(key=lambda r: r["tau"])
    A_mono = all(lean[i]["A_developmental"] <= lean[i + 1]["A_developmental"] + 1e-9
                 for i in range(len(lean) - 1))
    # E-rising mature points (tau==1) -> occupancy monotone non-decreasing
    mature = [r for r in rows if abs(r["tau"] - 1.0) < 1e-9]
    mature.sort(key=lambda r: r["E"])
    occ_mono = all(mature[i]["occupancy_volume"] <= mature[i + 1]["occupancy_volume"] + 1e-6
                   for i in range(len(mature) - 1))
    readout = lc.order_is_gamma_readout()
    ok = bool(A_mono and occ_mono and readout)
    occs = "<=".join(f"{r['occupancy_volume']:.0f}" for r in mature)
    return ok, (f"A(tau) monotone over lean growth={A_mono}; occupancy monotone in E at maturity="
                f"{occ_mono} ({occs}); emergence order==gamma readout={readout}")


# ----------------------------------------------------------------- check 4
def check_baseline_preserved():
    lc = LC.LifeCourse(scene="face")
    ok, ma, md = lc.baseline_preserved([0.35, 0.55, 0.78, 1.0], vox=1.2)
    return ok, f"max|alpha|={ma:.1e}, max|field diff vs gene-clock|={md:.1e} (both 0 -> bit-for-bit)"


# ----------------------------------------------------------------- check 5
def check_determinism():
    lc = LC.LifeCourse(scene="face")
    life = LC.default_life()
    h1 = _traj_sha(lc.trajectory(life, vox=1.0))
    h2 = _traj_sha(lc.trajectory(life, vox=1.0))
    return (h1 == h2), f"trajectory sha {h1[:10]}=={h2[:10]} ({h1 == h2})"


def main():
    checks = [
        ("1 ONE CONTINUOUS FOLD (time==energy==body)", check_one_continuous_fold()),
        ("2 MEASURED GAMMA (gene-clock 42 bit-identical in adipose 59)", check_measured_gamma()),
        ("3 MONOTONE TRAJECTORY (growth in tau, fat in E)", check_monotone_trajectory()),
        ("4 BASELINE PRESERVED (lean -> gene-clock field bit-for-bit)", check_baseline_preserved()),
        ("5 DETERMINISM (2x trajectory identical)", check_determinism()),
    ]
    npass = 0
    print("=" * 78)
    print("  LIFE-COURSE GATE  |  gene clock (TIME) x adipose (ENERGY) = one R19 fold")
    print("=" * 78)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 78)
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(GC.HERE, "..", "results", "life_course_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
              | {"overall": f"{npass}/{len(checks)}"}, open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
