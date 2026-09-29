import os, pandas as pd, numpy as np

def run(root):
    hp = pd.read_csv(os.path.join(root, "PF_pack", "human_pigment_variants.tsv"), sep="\t")
    # SLC24A5 rs1426654 유전자형 집계
    mask = hp["rsID"]=="rs1426654"
    sub = hp[mask]
    counts = sub["Allele_1"].astype(str)+sub["Allele_2"].astype(str)
    # 간단 빈도: A 포함 비율
    A_present = counts.str.contains("A")
    freq_A = float(A_present.mean()) if len(A_present)>0 else np.nan

    # 맘모스 TRPV3 LOF 카운트 확인
    mm = pd.read_csv(os.path.join(root, "PF_pack", "mammoth_LOF_burden_tests.csv"))
    trpv3 = mm[mm["Gene"]=="TRPV3"].iloc[0].to_dict()

    # 식물 sedaDNA 속씨 비율 최신 레이어 평균
    sd = pd.read_csv(os.path.join(root, "PF_pack", "sedadna_angiosperm_fraction.csv"))
    recent = sd.sort_values("Age_BP").head(4)  # 가장 최근 4개 레이어(예시)
    angio_mean = float(recent["Angiosperm_Fraction"].mean())
    return {"freq_SLC24A5_A_any": freq_A, "TRPV3_burden_row": trpv3, "recent_angiosperm_mean": angio_mean}
