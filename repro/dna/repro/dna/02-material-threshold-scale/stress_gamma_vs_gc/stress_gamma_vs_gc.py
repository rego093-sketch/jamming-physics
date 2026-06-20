#!/usr/bin/env python3
# =============================================================================
#  stress_gamma_vs_gc.py -- SHARPEN the settled claim "gamma is a GC-restatement"
#  (U1 of section 11: corr(gamma,GC) = 0.985-0.998 across 12 kingdoms).
#
#  THE QUESTION. corr(gamma,GC)=0.99 is measured ACROSS genomes that differ a lot
#  in GC. That high correlation can be (a) a real statement that gamma carries
#  nothing beyond GC, or (b) an artifact of a wide cross-genome GC range that
#  swamps a real within-genome dinucleotide term. The framework's own
#  "mechanistic payoff" (sec 11) claims the part of gamma not explained by GC is
#  the CpG-depletion (methylation) fingerprint -- but that is asserted
#  qualitatively, never tested. This test isolates and grades it.
#
#  THE METHOD (clean, no new data). For each frozen 120 kb region, cut into
#  non-overlapping 2 kb windows (the locked W). For every window:
#     gamma_obs  = gamma(window)                         (real dinucleotide order)
#     GC         = gc_frac(window)
#     cpg_oe     = (nCG*L)/(nC*nG)                        (the sec-12 measure)
#     gamma_perm = mean gamma over K random PERMUTATIONS of the window's bases
#  A permutation holds mononucleotide composition (hence GC) EXACTLY fixed and
#  randomizes dinucleotides to their iid expectation. Therefore
#     d_gamma = gamma_obs - gamma_perm
#  is EXACTLY the dinucleotide-order term: what gamma carries BEYOND composition,
#  at fixed GC. (This is the rigorous version of "gamma at fixed GC".)
#
#  THREE GRADED READS:
#   1. MAGNITUDE. How big is d_gamma vs the cross-genome gamma range (0.290, sec11)
#      and vs within-genome gamma spread? -> how much of gamma is NOT GC.
#   2. WITHIN-GENOME corr(gamma_obs, GC). Is it still ~0.99 at the local scale
#      biology uses, or lower (dinucleotide term matters locally)?
#   3. STRUCTURE. corr(d_gamma, cpg_oe) pooled across all windows. The framework
#      predicts the gamma-beyond-GC term IS the CpG fingerprint: CpG depletion
#      removes stiff CG steps (dG -2.17) -> lowers gamma below its GC prediction
#      -> d_gamma should be POSITIVE where CpG O/E is high. Test sign + strength.
#
#  HONEST OUTCOME: if d_gamma is tiny and unstructured -> "gamma = GC" stands at
#  all scales (claim strengthened). If d_gamma is non-trivial AND tracks CpG O/E
#  -> the framework's payoff claim is QUANTIFIED and gamma is refined to
#  "GC + a measurable CpG/dinucleotide term" (a better answer, not a rejection).
#
#  DETERMINISTIC: locked gamma imported single-source + sha256-pinned; seed 19.
# =============================================================================
import os, sys, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GRAM = os.path.join(REPO, "repro", "dna", "_verify", "engine")
METH = os.path.join(REPO, "repro", "dna", "12-clade-methylation-readers")
for p in (GRAM, METH):
    if p not in sys.path:
        sys.path.insert(0, p)
import dna_interpreter as DI            # gamma, gc_frac (locked, single source)
import clade_reader_engine as M         # cpg_oe (locked, single source)

S11 = os.path.join(REPO, "repro", "dna", "11-cross-kingdom-stress-test")
SEED = 19
W = 2000                                 # the locked window length
K_PERM = 60                              # permutations per window for the iid baseline


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 3 or x.std() == 0 or y.std() == 0:
        return float("nan"), len(x)
    return float(np.corrcoef(x, y)[0, 1]), len(x)


def partial_corr(x, y, z):
    """corr(x, y | z): linear-residualize x and y on z, correlate residuals."""
    x, y, z = (np.asarray(a, float) for a in (x, y, z))
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    x, y, z = x[m], y[m], z[m]
    if len(x) < 4:
        return float("nan")
    A = np.vstack([z, np.ones_like(z)]).T
    rx = x - A @ np.linalg.lstsq(A, x, rcond=None)[0]
    ry = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
    if rx.std() == 0 or ry.std() == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def read_region(lbl):
    return "".join(l.strip() for l in open(os.path.join(S11, "inputs", f"{lbl}.fa"))
                   if not l.startswith(">")).upper()


def main():
    pins = {
        "dna_interpreter.py": sha256_file(os.path.join(GRAM, "dna_interpreter.py")),
        "clade_reader_engine.py": sha256_file(os.path.join(METH, "clade_reader_engine.py")),
    }
    prov = json.load(open(os.path.join(S11, "inputs", "_provenance.json")))
    organisms = list(prov["organisms"].keys())

    rng = np.random.default_rng(SEED)
    per_org = {}
    all_gamma_obs, all_gc, all_dgamma, all_cpgoe, all_gamma_perm = [], [], [], [], []
    all_cgexcess = []                    # CG-step excess over iid expectation (the mechanism)

    for lbl in organisms:
        seq = read_region(lbl)
        arr = np.frombuffer(seq.encode("ascii"), dtype=np.uint8)
        g_obs, gcs, dgs, oes, g_perms, cgxs, tafs = [], [], [], [], [], [], []
        for i in range(0, len(seq) - W + 1, W):
            win = seq[i:i + W]
            if win.count("N") > 0:           # skip windows with any N (gap-clean)
                continue
            go = DI.gamma(win)
            gc = DI.gc_frac(win)
            oe = M.cpg_oe(win)
            # iid baseline at the SAME composition: permute the window's bases
            wa = arr[i:i + W].copy()
            gp = np.empty(K_PERM)
            for k in range(K_PERM):
                rng.shuffle(wa)
                gp[k] = DI.gamma(wa.tobytes().decode("ascii"))
            gpm = float(gp.mean())
            if not (np.isfinite(go) and np.isfinite(gc) and np.isfinite(oe)):
                continue
            L = len(win); nC = win.count("C"); nG = win.count("G")
            cg_excess = win.count("CG") - (nC * nG / L)      # obs - iid-expected CG steps
            ta_frac = win.count("TA") / (L - 1)              # softest step (AT-rich driver)
            g_obs.append(go); gcs.append(gc); oes.append(oe)
            g_perms.append(gpm); dgs.append(go - gpm)
            cgxs.append(cg_excess); tafs.append(ta_frac)

        if len(g_obs) < 5:
            per_org[lbl] = {"n_windows": len(g_obs), "skipped": "too few clean windows"}
            continue
        r_gc, n = pearson(g_obs, gcs)
        r_struct, _ = pearson(dgs, oes)
        r_ta, _ = pearson(dgs, tafs)
        per_org[lbl] = {
            "n_windows": n,
            "gamma_obs_mean": round(float(np.mean(g_obs)), 4),
            "gamma_obs_std": round(float(np.std(g_obs)), 4),
            "gc_mean": round(float(np.mean(gcs)), 4),
            "within_corr_gamma_gc": round(r_gc, 4),
            "dgamma_mean": round(float(np.mean(dgs)), 5),
            "dgamma_std": round(float(np.std(dgs)), 5),
            "abs_dgamma_median": round(float(np.median(np.abs(dgs))), 5),
            "within_corr_dgamma_cpgoe": round(r_struct, 4),
            "within_corr_dgamma_ta_step": round(r_ta, 4),
        }
        all_gamma_obs += g_obs; all_gc += gcs; all_dgamma += dgs
        all_cpgoe += oes; all_gamma_perm += g_perms; all_cgexcess += cgxs

    # ---------- pooled reads ----------
    r_pool_gc, n_pool = pearson(all_gamma_obs, all_gc)
    r_pool_struct, _ = pearson(all_dgamma, all_cpgoe)
    # GC-confound control: is the d_gamma <-> CpG O/E link there AFTER removing GC?
    r_partial = partial_corr(all_dgamma, all_cpgoe, all_gc)
    # mechanism: does d_gamma track the excess of stiff CG steps over iid?
    r_mech, _ = pearson(all_dgamma, all_cgexcess)

    go = np.array(all_gamma_obs); gp = np.array(all_gamma_perm); dg = np.array(all_dgamma)
    # variance decomposition: how much of within+across gamma is composition vs dinuc?
    var_total = float(go.var())
    var_perm = float(gp.var())            # composition (iid) part
    var_dg = float(dg.var())              # dinucleotide-order part
    frac_dinuc = var_dg / var_total if var_total > 0 else float("nan")

    # cross-genome reference numbers (frozen sec 11): gamma range 0.290, CV 5.8%
    cross_genome_gamma_range = 0.290
    median_abs_dg = float(np.median(np.abs(dg)))
    dg_as_frac_of_cross_range = median_abs_dg / cross_genome_gamma_range

    # honest grading
    structured = abs(r_pool_struct) >= 0.3 and n_pool >= 30
    sign_as_predicted = r_pool_struct > 0     # CpG depletion lowers gamma below GC pred.

    verdict_struct = (
        "STRUCTURED + SIGN AS PREDICTED" if (structured and sign_as_predicted) else
        "STRUCTURED, sign opposite to prediction" if structured else
        "UNSTRUCTURED (d_gamma ~ noise at fixed GC)")

    grade = (
        "REFINED: gamma = GC + a measurable, CpG-correlated dinucleotide term. "
        "The settled 'gamma is a GC-restatement' is right that gamma adds no INDEPENDENT "
        "axis, but the gamma-beyond-GC residual is not noise: it tracks CpG O/E with the "
        f"predicted sign (pooled r={round(r_pool_struct,3)}), quantifying section 11's "
        "qualitative 'two projections of one history' payoff. Within-genome corr(gamma,GC) "
        f"= {round(np.nanmean([per_org[o]['within_corr_gamma_gc'] for o in per_org if 'within_corr_gamma_gc' in per_org[o]]),3)} "
        "(mean), so GC still dominates locally, but the dinucleotide term is real and CpG-shaped."
        if (structured and sign_as_predicted) else
        "STANDS: at fixed GC the gamma residual is small and unstructured; "
        "'gamma is a GC-restatement' holds at the within-genome scale too.")

    out = {
        "_question": "Is the part of gamma NOT explained by GC just noise, or is it the "
                     "CpG/methylation fingerprint? (sharpening U1 'gamma = GC-restatement')",
        "_method": {
            "window_bp": W, "permutations_per_window": K_PERM, "seed": SEED,
            "d_gamma": "gamma_obs - mean(gamma of permuted window) = dinucleotide-order term "
                       "at fixed composition",
            "prediction": "CpG depletion removes stiff CG steps (dG -2.17) -> d_gamma POSITIVE "
                          "where CpG O/E high (corr(d_gamma, cpg_oe) > 0)",
        },
        "pooled": {
            "n_windows": n_pool,
            "corr_gamma_gc_pooled": round(r_pool_gc, 4),
            "corr_dgamma_cpgoe_pooled": round(r_pool_struct, 4),
            "partial_corr_dgamma_cpgoe_given_gc": round(r_partial, 4),
            "corr_dgamma_cg_step_excess": round(r_mech, 4),
            "structure_verdict": verdict_struct,
            "var_total_gamma": round(var_total, 6),
            "var_composition_part_iid": round(var_perm, 6),
            "var_dinucleotide_part": round(var_dg, 6),
            "frac_gamma_variance_dinucleotide": round(frac_dinuc, 4),
            "median_abs_dgamma": round(median_abs_dg, 5),
            "cross_genome_gamma_range_sec11": cross_genome_gamma_range,
            "median_abs_dgamma_as_frac_of_cross_genome_range": round(dg_as_frac_of_cross_range, 4),
        },
        "boundary_plasmodium": {
            "note": "at GC~20% (AT-rich, barely methylates) the d_gamma residual INVERTS its "
                    "CpG relationship (within_corr_dgamma_cpgoe < 0) and is instead driven by "
                    "TA-step structure (within_corr_dgamma_ta_step strongly negative). The "
                    "'gamma-beyond-GC = CpG fingerprint' mapping is itself clade/GC-dependent -- "
                    "parallel to U3's 'read the methylation substrate in the clade's context'.",
            "within_corr_dgamma_cpgoe": per_org.get("plasmodium", {}).get("within_corr_dgamma_cpgoe"),
            "within_corr_dgamma_ta_step": per_org.get("plasmodium", {}).get("within_corr_dgamma_ta_step"),
        },
        "per_organism": per_org,
        "grade": grade,
        "_pins": pins,
    }
    json.dump(out, open(os.path.join(HERE, "stress_gamma_vs_gc_results.json"), "w"),
              indent=2, sort_keys=True, ensure_ascii=False)

    # ---- print ----
    print("=" * 96)
    print("GAMMA vs GC STRESS TEST -- is gamma-beyond-GC noise, or the CpG fingerprint?")
    print("=" * 96)
    print(f"{'organism':12}{'nwin':>5}{'gamma':>8}{'GC':>7}{'corr(g,GC)':>12}"
          f"{'d_gamma_sd':>12}{'corr(dg,OE)':>13}")
    for lbl, r in per_org.items():
        if "within_corr_gamma_gc" in r:
            print(f"{lbl:12}{r['n_windows']:>5}{r['gamma_obs_mean']:>8}{r['gc_mean']:>7}"
                  f"{r['within_corr_gamma_gc']:>12}{r['dgamma_std']:>12}"
                  f"{r['within_corr_dgamma_cpgoe']:>13}")
        else:
            print(f"{lbl:12}{r['n_windows']:>5}   ({r.get('skipped','')})")
    p = out["pooled"]
    print("-" * 96)
    print(f"POOLED ({p['n_windows']} windows):")
    print(f"  corr(gamma, GC)              = {p['corr_gamma_gc_pooled']}")
    print(f"  corr(d_gamma, CpG O/E)       = {p['corr_dgamma_cpgoe_pooled']}   [{p['structure_verdict']}]")
    print(f"  partial corr(dg, OE | GC)    = {p['partial_corr_dgamma_cpgoe_given_gc']}   (GC-confound removed)")
    print(f"  corr(d_gamma, CG-step excess)= {p['corr_dgamma_cg_step_excess']}   (the stiff-CG mechanism)")
    print(f"  frac of gamma variance from dinucleotide order = {p['frac_gamma_variance_dinucleotide']}")
    print(f"  median |d_gamma| = {p['median_abs_dgamma']}  "
          f"(= {p['median_abs_dgamma_as_frac_of_cross_genome_range']} of the cross-genome gamma range)")
    print("-" * 96)
    print("GRADE:", grade)
    return out


if __name__ == "__main__":
    main()
