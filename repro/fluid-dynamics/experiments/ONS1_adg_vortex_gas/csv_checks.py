"""Internal-consistency checks C1-C4 on the shipped epsilon_events_ensemble.csv (PREREG)."""
import csv, json, math, os, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "../../repro/fluid-dynamics/09-pillar-iv-dissipative-arrangement-sets/"
                   "metriplectic-onsager/data/raw/epsilon_events_ensemble.csv")
rows = [dict((k, float(v)) for k, v in r.items()) for r in csv.DictReader(open(CSV))]
out = {}
# C1 merger bookkeeping
viol = [(r["N"], r["rc"], r["seed"], r["n_mergers"] + r["N_final"] - r["N"]) for r in rows
        if r["n_mergers"] + r["N_final"] != r["N"]]
out["C1_n_mergers_plus_N_final_equals_N"] = dict(
    rows_violating=len(viol), rows=len(rows),
    excess_range=[min(v[3] for v in viol), max(v[3] for v in viol)] if viol else None)
# C2 direction of n_mergers with rc
g = collections.defaultdict(list)
for r in rows:
    g[(r["N"], r["rc"])].append(r)
ratio = {int(N): np.mean([x["n_mergers"] for x in g[(N, 0.002)]]) / np.mean([x["n_mergers"] for x in g[(N, 0.01)]])
         for N in (500, 1000, 2000)}
out["C2_n_mergers_ratio_rc0.002_over_rc0.01"] = ratio
# C3 identical seed offsets / eps_tot-eps_bind across rc
c3 = {}
for N in (500, 1000, 2000):
    dev = {rc: np.array([x["eps_bind"] for x in sorted(g[(N, rc)], key=lambda z: z["seed"])]) for rc in (0.01, 0.005, 0.002)}
    dev = {rc: v - v.mean() for rc, v in dev.items()}
    gap = {rc: np.array([x["eps_tot"] - x["eps_bind"] for x in sorted(g[(N, rc)], key=lambda z: z["seed"])]) for rc in (0.01, 0.005, 0.002)}
    c3[int(N)] = dict(
        max_diff_seed_deviation_across_rc=float(max(np.abs(dev[a] - dev[b]).max() for a in dev for b in dev)),
        max_diff_eps_tot_minus_eps_bind_across_rc=float(max(np.abs(gap[a] - gap[b]).max() for a in gap for b in gap)),
        eps_std_by_rc=[float(np.std([x["eps_bind"] for x in g[(N, rc)]], ddof=1)) for rc in (0.01, 0.005, 0.002)])
out["C3_generated_table_signature"] = c3
out["C3_Re_eff_times_rc"] = sorted({round(r["Re_eff"] * r["rc"], 6) for r in rows})
# C4 energy per merger vs point-vortex binding energy ~ (1/2pi) ln(1/rc) + g0
g0 = 0.08392943988113188
pred = (math.log(1 / 0.002) / (2 * math.pi) + g0) / (math.log(1 / 0.01) / (2 * math.pi) + g0)
c4 = {}
for N in (500, 1000, 2000):
    e = lambda rc: np.mean([x["eps_bind"] / x["n_mergers"] for x in g[(N, rc)]])
    c4[int(N)] = float(e(0.002) / e(0.01))
out["C4_eps_bind_per_merger_ratio_rc0.002_over_rc0.01"] = dict(csv=c4, point_vortex_expectation=pred)
json.dump(out, open(os.path.join(HERE, "csv_checks.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
