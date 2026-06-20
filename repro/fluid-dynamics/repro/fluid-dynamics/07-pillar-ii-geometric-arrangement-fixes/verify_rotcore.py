"""verify_rotcore.py — recompute RCCI robust metrics from sample-level CSV and
compare to the published DOI tables. Point CSV_DIR at the rotcore-doi archive's data/."""
import sys, numpy as np, pandas as pd
from scipy.stats import spearmanr
CSV_DIR = sys.argv[1] if len(sys.argv)>1 else "../rotcore/data"
df = pd.read_csv(f"{CSV_DIR}/metrics_long_v1.3.9.csv")
pub = pd.read_csv(f"{CSV_DIR}/metrics_robust_v139.csv").set_index(["case","method"])
worst=0.0
for (case,method),d in df.groupby(["case","method"]):
    e=np.abs(d.r_meas-d.r_pred)/d.r_pred
    rec=dict(rel_med_percent=100*np.median(e), MAPE_percent=100*np.mean(e),
             MAE=np.mean(np.abs(d.r_meas-d.r_pred)),
             NRMSE_percent=100*np.sqrt(np.mean((d.r_meas-d.r_pred)**2))/np.median(d.r_pred),
             rho_spearman=spearmanr(d.r_pred,d.r_meas).statistic)
    for k,v in rec.items():
        worst=max(worst, abs(v-pub.loc[(case,method),k])/(abs(pub.loc[(case,method),k])+1e-12))
print(f"RCCI metrics vs published: worst relative mismatch = {worst:.2e}  ->  {'PASS' if worst<1e-6 else 'FAIL'}")
