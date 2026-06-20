#!/usr/bin/env python3
# =============================================================================
#  stress_helical.py -- does the anchor-relative `contact_competent` read carry
#  REAL signal, or is it geometry at chance? A §11-style stress test.
#
#  THE QUESTION (the user's): if we use the helical structure as a full grammar
#  (like the A4 shell/anchor/loop grammar), does it give a real element-level read
#  -- a "100%" coordinate -- or is the bare motor->nearest-anchor same-face flag
#  just geometry that lands at chance?
#
#  TEST (deterministic):
#   For each of the 12 cross-kingdom (§11) frozen 120kb regions:
#     1. A4 = run_key(region) -> structural anchors (shell boundaries).
#     2. motors (TSS) from the region-relative feature table (parse_ft_motors).
#     3. contact_competent for each motor -> its nearest anchor (same helical face,
#        within ~60 deg; RISE 3.4 A/bp, TWIST 34.29 deg/bp -- the locked grammar).
#     4. OBSERVED same-face rate.
#     5. NULL by permutation: M random re-placements of the motors (uniform in the
#        region), nearest-anchor contact rate each -> null mean + observed percentile.
#        (Preserves anchor structure and motor count; asks if REAL TSS positions
#        phase to anchors any differently than random positions.)
#     6. ANALYTIC chance: face is uniform for arbitrary distances, so same-face
#        (|face|<0.17 or >0.83) has p = 0.34 under no phasing.
#   Pool all motor-anchor pairs across organisms for an aggregate binomial test.
#
#  CONTRAST: the frozen §11 GLOBAL WW-ACF(10-11) periodicity percentile -- the
#  descriptive nucleosome-positioning propensity -- is reported alongside. That
#  global signal is REAL (and was never retired as a *descriptive* fact); what §13
#  retired was its use as an *element-level contact* claim. This test asks whether
#  the element-level contact read adds signal beyond chance.
#
#  HONEST OUTCOME: whatever the data shows. If observed ~ null ~ 0.34, the bare
#  contact flag is chance (a Layer-1 geometry fact, not a biological phasing read),
#  and the grammar should grade it accordingly -- not claim 100% functional contact.
# =============================================================================
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GRAM = os.path.join(REPO, "repro", "dna", "_verify", "engine")
if GRAM not in sys.path:
    sys.path.insert(0, GRAM)
import key_pipeline_full as K
import dna_interpreter as DI

S11 = os.path.join(REPO, "repro", "dna", "11-cross-kingdom-stress-test")
FTDIR = os.path.join(HERE, "inputs_ft")
M_PERM = 2000
SEED = 19
TWIST = DI.TWIST_DEG            # 34.29 deg/bp (locked)
CHANCE = 2 * 0.17              # analytic same-face probability under no phasing = 0.34


def same_face(dbp):
    face = (abs(dbp) * TWIST % 360.0) / 360.0
    return min(face, 1.0 - face) < 0.17


def contact_rate(motor_pos, anchor_pos):
    ap = np.asarray(anchor_pos)
    hits = 0
    for m in motor_pos:
        j = int(np.argmin(np.abs(ap - m)))
        if same_face(int(ap[j]) - int(m)):
            hits += 1
    return hits / max(1, len(motor_pos))


def main():
    prov = json.load(open(os.path.join(S11, "inputs", "_provenance.json")))
    exp11 = json.load(open(os.path.join(S11, "expected", "cross_kingdom_results.json")))
    # locate the per-organism helical percentile in the frozen §11 results
    def ww_pct(lbl):
        for key in ("per_organism", "organisms"):
            if key in exp11 and lbl in exp11[key]:
                return exp11[key][lbl].get("helical_percentile")
        return exp11.get(lbl, {}).get("helical_percentile")

    rng = np.random.default_rng(SEED)
    rows, pooled_hits, pooled_n = [], 0, 0
    for lbl, o in prov["organisms"].items():
        ftp = os.path.join(FTDIR, f"{lbl}.ft")
        if not os.path.exists(ftp):
            continue
        region = "".join(l.strip() for l in open(os.path.join(S11, "inputs", f"{lbl}.fa"))
                         if not l.startswith(">")).upper()
        L = len(region)
        A4 = K.run_key(region)
        anchors = [a["pos"] for a in A4["anchors"]]
        motors = [m["pos"] for m in DI.parse_ft_motors(open(ftp).read())]
        n = len(motors)
        if n < 3:
            rows.append({"organism": lbl, "n_motors": n, "skipped": "too few motors (<3)",
                         "ww_global_percentile": ww_pct(lbl)})
            continue
        obs = contact_rate(motors, anchors)
        # permutation null: random motor positions
        null = np.empty(M_PERM)
        for i in range(M_PERM):
            rp = rng.integers(0, L, size=n)
            null[i] = contact_rate(rp.tolist(), anchors)
        nmean, nstd = float(null.mean()), float(null.std())
        pct = float((null < obs).mean() * 100)
        z = (obs - nmean) / nstd if nstd > 0 else 0.0
        pooled_hits += int(round(obs * n)); pooled_n += n
        rows.append({"organism": lbl, "n_motors": n,
                     "observed_contact_rate": round(obs, 3),
                     "null_mean": round(nmean, 3), "null_std": round(nstd, 3),
                     "observed_percentile_vs_null": round(pct, 1),
                     "z_vs_null": round(z, 2),
                     "ww_global_percentile": ww_pct(lbl)})

    # aggregate binomial: pooled observed vs chance 0.34
    p_hat = pooled_hits / pooled_n if pooled_n else float("nan")
    se = math.sqrt(CHANCE * (1 - CHANCE) / pooled_n) if pooled_n else float("nan")
    z_pool = (p_hat - CHANCE) / se if pooled_n else float("nan")

    tested = [r for r in rows if "observed_contact_rate" in r]
    n_enriched = sum(1 for r in tested if r["observed_percentile_vs_null"] >= 95)
    n_depleted = sum(1 for r in tested if r["observed_percentile_vs_null"] <= 5)
    small_n = sum(1 for r in tested if r["n_motors"] < 30)

    # The POOLED test (hundreds of pairs) is decisive; per-organism n is small
    # (most < 40, several < 10) so per-organism tails are noise that washes out
    # in the pool. Verdict keys on |pooled z|.
    at_chance = abs(z_pool) < 2.0
    verdict = ("contact_competent is AT CHANCE: across the pooled motor-anchor pairs the same-face "
               "rate is statistically indistinguishable from the analytic chance of 0.34 "
               f"(pooled z = {round(z_pool,2)}). Real TSS positions are NOT helically phased to the "
               "composition-shell anchors -- the bare nearest-anchor contact flag is Layer-1 geometry, "
               "not a biological phasing signal. (Per-organism departures are small-n noise: median "
               "motor count is low and the tails wash out when pooled.)"
               if at_chance else
               "contact_competent departs from chance at the pooled level (|z| >= 2): real TSS<->anchor "
               "phasing carries a non-random signal -- see per-organism percentiles.")

    out = {
        "_question": "Does anchor-relative contact_competent carry element-level signal, or is it "
                     "geometry at chance? (helical-as-A4-grammar stress test)",
        "_method": {"twist_deg_per_bp": TWIST, "same_face_window_deg": "~60 (|face|<0.17)",
                    "analytic_chance": CHANCE, "permutations": M_PERM, "seed": SEED,
                    "null": "uniform-random motor positions, nearest-anchor contact rate"},
        "per_organism": rows,
        "aggregate": {"organisms_tested": len(tested),
                      "pooled_motor_anchor_pairs": pooled_n,
                      "pooled_observed_rate": round(p_hat, 4),
                      "analytic_chance": CHANCE,
                      "z_pooled_vs_chance": round(z_pool, 2),
                      "n_organisms_enriched_p95": n_enriched,
                      "n_organisms_depleted_p5": n_depleted},
        "contrast_global_ww_periodicity": {
            "note": "the frozen §11 GLOBAL WW-ACF(10-11) percentile is the nucleosome-positioning "
                    "propensity -- a REAL descriptive composition signal (elevated above shuffle in "
                    "all 12). §13 retired only its use as an element-level CONTACT claim, not as a "
                    "descriptive fact. This test isolates the element-level contact question."},
        "verdict": verdict,
        "interpretation": (
            "Helical phase is sequence-derivable Layer-1 GEOMETRY and can be read for every locus "
            "(no [O] for the geometry itself). But a 100% read means 100% of the GEOMETRY, not 100% "
            "of the realized functional contact: whether two same-face loci actually loop depends on "
            "runtime factors (bound TFs, cohesin) that are Layer-2 by this paper's thesis. The global "
            "WW periodicity (nucleosome propensity) is the real, gradeable helical signal; the "
            "nearest-anchor contact flag must be graded by THIS test, not assumed.")}

    json.dump(out, open(os.path.join(HERE, "stress_helical_results.json"), "w"),
              indent=2, ensure_ascii=False)

    # ---- print ----
    print("=" * 92)
    print("HELICAL STRESS TEST -- is anchor-relative contact_competent real signal or chance?")
    print("=" * 92)
    print(f"{'organism':12}{'n':>4}{'obs':>7}{'null':>7}{'pct':>7}{'z':>7}   {'WW global pct (real)':>20}")
    for r in rows:
        if "observed_contact_rate" in r:
            print(f"{r['organism']:12}{r['n_motors']:>4}{r['observed_contact_rate']:>7}"
                  f"{r['null_mean']:>7}{r['observed_percentile_vs_null']:>7}{r['z_vs_null']:>7}"
                  f"   {str(r['ww_global_percentile']):>20}")
        else:
            print(f"{r['organism']:12}{r['n_motors']:>4}   ({r['skipped']})")
    ag = out["aggregate"]
    print("-" * 92)
    print(f"pooled: {ag['pooled_motor_anchor_pairs']} motor-anchor pairs across "
          f"{ag['organisms_tested']} organisms")
    print(f"  observed contact rate = {ag['pooled_observed_rate']}  vs  analytic chance "
          f"{ag['analytic_chance']}   (z = {ag['z_pooled_vs_chance']})")
    print(f"  organisms enriched (p>=95) = {ag['n_organisms_enriched_p95']} ; "
          f"depleted (p<=5) = {ag['n_organisms_depleted_p5']}")
    print("-" * 92)
    print("VERDICT:", verdict)
    print("\nCONTRAST: the GLOBAL WW-ACF periodicity (nucleosome propensity) is REAL and elevated")
    print("above shuffle in all 12 (frozen §11) -- that descriptive signal stands; only the")
    print("element-level CONTACT claim was retired. This test grades the contact read itself.")
    print("\nINTERPRETATION:", out["interpretation"])
    return out


if __name__ == "__main__":
    main()
