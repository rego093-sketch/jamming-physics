"""Aggregate runs_main.json (+ runs_dt.json) into RESULT.json; apply PREREG criteria."""
import json, os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "runs_main.json")))
runs = [r for r in D["runs"] if not r.get("timeout")]
RCS = [0.01, 0.005, 0.002]
keys = ["eps_bind", "eps_tot", "eps_bind_gauge_lnL", "eps_bind_gauge_lnL_E0alt", "eps_bind_literal",
        "eps_bind_literal_E0lit", "eps_bind_core", "eps_bind_pairterm", "n_mergers", "n_mergers_window",
        "N_final", "H_int_final_over_E0", "mean_release_per_merger_over_pair_selfterm",
        "mean_release_per_merger", "max_step_drift", "sum_abs_drift", "wall_s", "steps"]
table = {}
for N in sorted({r["N"] for r in runs}, reverse=True):
    for rc in RCS:
        sel = [r for r in runs if r["N"] == N and r["rc"] == rc]
        if not sel:
            continue
        row = {"n_runs": len(sel)}
        for k in keys:
            v = np.array([np.nan if r[k] is None else r[k] for r in sel], float)
            row[k] = dict(mean=float(np.nanmean(v)), std=float(np.nanstd(v, ddof=1)) if len(v) > 1 else None)
        m, s = row["eps_bind"]["mean"], row["eps_bind"]["std"]
        row["eps_bind_cv"] = s / abs(m) if m else None
        row["per_seed_eps_bind"] = [r["eps_bind"] for r in sel]
        row["per_seed_n_mergers"] = [r["n_mergers"] for r in sel]
        table[f"N{N}_rc{rc}"] = row
res = {"table": table}
crit = {}
for N in sorted({r["N"] for r in runs}, reverse=True):
    m = {rc: table[f"N{N}_rc{rc}"]["eps_bind"]["mean"] for rc in RCS}
    mt = {rc: table[f"N{N}_rc{rc}"]["eps_tot"]["mean"] for rc in RCS}
    cv = {rc: table[f"N{N}_rc{rc}"]["eps_bind_cv"] for rc in RCS}
    P1 = m[0.002] / m[0.01] if m[0.01] else None
    P2 = all(0.15 <= x <= 0.25 for x in list(m.values()) + list(mt.values()))
    P3 = all(c is not None and abs(c) <= 0.05 for c in cv.values())
    lr = np.log(RCS)
    alpha = {}
    for k in ["eps_bind", "eps_bind_gauge_lnL", "eps_bind_literal", "n_mergers"]:
        y = [table[f"N{N}_rc{rc}"][k]["mean"] for rc in RCS]
        alpha[k] = float(np.polyfit(lr, np.log(y), 1)[0]) if all(v > 0 for v in y) else None
    ratios = {}
    for k in ["eps_bind", "eps_tot", "eps_bind_gauge_lnL", "eps_bind_literal", "eps_bind_core"]:
        y = [table[f"N{N}_rc{rc}"][k]["mean"] for rc in RCS]
        ratios[k] = dict(values=y, ratio_rc0002_over_rc001=(y[2] / y[0]) if y[0] else None)
    crit[f"N{N}"] = dict(P1_ratio=P1, P1_pass=(P1 is not None and 0.9 <= P1 <= 1.1), P2_pass=P2,
                        P3_pass=P3, eps_bind_means=m, eps_tot_means=mt, cv=cv,
                        T1_powerlaw_exponent_vs_rc=alpha, T3_accounting_variants=ratios,
                        reproduced=bool(P1 is not None and 0.9 <= P1 <= 1.1 and P2 and P3))
res["criteria"] = crit
res["verdict"] = "REPRODUCED" if all(c["reproduced"] for c in crit.values()) else "NOT REPRODUCED"
p = os.path.join(HERE, "runs_dt.json")
if os.path.exists(p):
    Dd = json.load(open(p))
    res["dt_convergence"] = [{k: r.get(k) for k in ["N", "rc", "seed", "eps_bind", "eps_tot", "n_mergers",
                              "max_step_drift", "sum_abs_drift"]} | {"dt_max_T0": Dd["cfg"]["kw"]["dt_max_T0"]}
                             for r in Dd["runs"]]
res["csv_checks"] = json.load(open(os.path.join(HERE, "csv_checks.json")))
res["timeouts"] = [(r["N"], r["rc"], r["seed"]) for r in D["runs"] if r.get("timeout")]
json.dump(res, open(os.path.join(HERE, "RESULT_raw.json"), "w"), indent=1)
for k, c in crit.items():
    print(k, json.dumps(c, indent=1))
for k, row in table.items():
    print(k, "eps_bind %.4f+-%.4f eps_tot %.4f nm %.1f Nf %.1f Hint/E0 %.3f rel/pair %.3f drift %.2e wall %.0f" % (
        row["eps_bind"]["mean"], row["eps_bind"]["std"], row["eps_tot"]["mean"], row["n_mergers"]["mean"],
        row["N_final"]["mean"], row["H_int_final_over_E0"]["mean"],
        row["mean_release_per_merger_over_pair_selfterm"]["mean"], row["sum_abs_drift"]["mean"], row["wall_s"]["mean"]))

# ---- diagnostics (run_diag.py) and analytic accounting, then RESULT.json ----
p = os.path.join(HERE, "runs_diag.json")
if os.path.exists(p):
    Dg = json.load(open(p))["runs"]
    fp = {}
    for N in (32, 64, 128):
        sel = [r for r in Dg if r["N"] == N and r.get("first_passage")]
        if not sel:
            continue
        thr = sel[0]["first_passage"]["thresholds"]
        win = np.array([r["first_passage"]["new_in_window"] for r in sel], float)
        fp[f"N{N}"] = dict(n_runs=len(sel), thresholds=thr,
                           mean_new_pairs_below_threshold_in_window=win.mean(0).tolist(),
                           per_run=win.tolist(),
                           E0=[r["E0"] for r in sel], T0=[r["T0"] for r in sel])
    res["first_passage_merger_free"] = fp
    dtc = [dict(r, dt_max_T0=1 / 4000) for r in Dg if r["rc"] == 0.002]
    res["dt_halving_check"] = [{k: r.get(k) for k in ["N", "rc", "seed", "eps_bind", "eps_tot", "n_mergers",
                                "sum_abs_drift", "max_step_drift", "timeout"]} | {"dt_max_T0": r.get("dt_max_T0")}
                               for r in dtc]
g0 = D["g0"]
Lb = 2 * math.pi
res["analytic_per_merger_release_unit_vortices"] = {
    str(rc): dict(SM_periodic=math.log(1 / rc) / (2 * math.pi) + g0,
                  SM_literal_minimage_log=math.log(1 / rc) / (2 * math.pi),
                  gauge_lnL=math.log(Lb / rc) / (2 * math.pi),
                  finite_core_a_rc_over_2=g0 - 1 / (8 * math.pi))
    for rc in RCS}
merg = [e for r in runs for e in r["mergers"]]
res["logged_mergers"] = [dict(N=r["N"], rc=r["rc"], seed=r["seed"], t_over_T0=e["t"] / r["T0"], r=e["r"],
                              dH_flow=e["dH"], pair_selfterm=e["pair"], dE_finite_core=e["dE_core"],
                              dH_SM_literal=e["dH_lit"]) for r in runs for e in r["mergers"]]
json.dump(res, open(os.path.join(HERE, "RESULT_raw.json"), "w"), indent=1)
