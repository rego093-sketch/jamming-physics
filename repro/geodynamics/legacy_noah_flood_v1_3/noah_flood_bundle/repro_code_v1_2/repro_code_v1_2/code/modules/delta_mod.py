import os, pandas as pd, numpy as np

def run(root):
    gci = pd.read_csv(os.path.join(root, "R10_Nile", "global_delta_CI_100yr.csv"))
    nile = pd.read_csv(os.path.join(root, "R10_Nile", "nile_core_map.csv"))
    bd = pd.read_csv(os.path.join(root, "R10_Nile", "bulk_density_summary.csv"))
    # 간단 산출: 10/50/100년 누적 하한·상한, 나일 평균 두께, 벌크밀도 중앙값
    out = {
        "global_discharge_CI": {
            str(int(r["Years_After_Event_t0"])): [float(r["Global_Discharge_Gt_per_yr_Lower_CI"]), float(r["Global_Discharge_Gt_per_yr_Upper_CI"])]
            for _, r in gci.iterrows()
        },
        "nile_core_mean_thickness": float(nile["Deposited_Thickness_m"].mean()),
        "bulk_density_median": float(bd["Median"].iloc[0])
    }
    return out
