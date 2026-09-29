import os, pandas as pd, numpy as np

def run(root):
    p = os.path.join(root, "R8_RSL", "RSL_intake.csv")
    df = pd.read_csv(p)
    # 간단 요약: 분지별 평균 RSL 및 표본 수
    grouped = df.groupby("basin").agg(
        n=("RSL_m","count"),
        mean_RSL=("RSL_m","mean"),
        std_RSL=("RSL_m","std")
    ).reset_index()
    return grouped.to_dict(orient="records")
