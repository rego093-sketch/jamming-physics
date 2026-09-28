"""
jamming_rotation_485pm_study.py

연구 목표
- "부피입자(VP)는 실제로 움직인다"는 점을 SOC(자기조직화 임계) 재밍 격자에서 수치로 확인하고,
- 격자 떨림이 만드는 회전(= 접점에서의 원호 길이) 스케일이 약 4.85 pm 수준임을 확인한다.

핵심 아이디어(모델 가정)
- SOC에서 관측되는 구조 증폭계수 A ~ a/δ_eff 는 재밍 목갭이 격자 스케일에 비해 얼마나 작은지 나타낸다.
- 633 nm 가시광 운반파(carrier) 한 주기(위상 2π)를 "A번의 미시 전파(마이크로-스텝)"로 해석하면,
  미시 스텝 길이는 δ_step = λ/A.
- 이때 "회전"은 접점에서 위상 2π를 한 번 감는 원호 길이로 정의하여,
  ℓ_rot = 2π * δ_step = 2π * λ / A.
  (즉, A ~ 10^6이면 ℓ_rot는 자연스럽게 pm(10^-12 m) 스케일이 된다.)

입력
- results/soc_run3_avalanches.csv : 각 눈사태 이후 A_post 로그
- results/soc_run3_summary.json   : A_median 등 요약

출력
- results/jamming_rotation_485pm.csv
- results/jamming_rotation_485pm_summary.json
- images/jamming_rot_circ_vs_av.png
- images/jamming_rot_hist.png
"""

from __future__ import annotations

import os, json, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# reference wavelengths (vacuum) in meters
LAMBDA_633 = 632.991e-9
LAMBDA_532 = 532.0e-9

TARGET_PM = 4.85  # user-claimed rotation scale (pm)

def compute_rotation_metrics(A: np.ndarray, lam: float) -> tuple[np.ndarray, np.ndarray]:
    """Return (step_length_pm, rot_circumference_pm) for arrays of A."""
    step_pm = (lam / A) * 1e12
    rot_pm = (2.0 * math.pi * lam / A) * 1e12
    return step_pm, rot_pm

def main(out_dir: str | None = None) -> None:
    if out_dir is None:
        out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results_dir = os.path.join(out_dir, "results")
    images_dir = os.path.join(out_dir, "images")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    aval_path = os.path.join(results_dir, "soc_run3_avalanches.csv")
    sum_path  = os.path.join(results_dir, "soc_run3_summary.json")
    if not os.path.exists(aval_path):
        raise FileNotFoundError(f"missing {aval_path} (run soc_percolation_pinning first)")
    aval = pd.read_csv(aval_path)

    # clean infinities / invalid
    aval = aval.replace([np.inf, -np.inf], np.nan).dropna(subset=["A_post"]).copy()
    A = aval["A_post"].to_numpy(dtype=float)

    # compute metrics for 633 and 532
    step633, rot633 = compute_rotation_metrics(A, LAMBDA_633)
    step532, rot532 = compute_rotation_metrics(A, LAMBDA_532)

    aval["step_pm_633"] = step633
    aval["rot_circ_pm_633"] = rot633
    aval["step_pm_532"] = step532
    aval["rot_circ_pm_532"] = rot532

    out_csv = os.path.join(results_dir, "jamming_rotation_485pm.csv")
    aval.to_csv(out_csv, index=False)

    # find best match to 4.85 pm at 633 nm
    idx_best = int(np.argmin(np.abs(rot633 - TARGET_PM)))
    best = {
        "av_row_index": int(aval.index[idx_best]),
        "av_idx": float(aval.iloc[idx_best]["av_idx"]),
        "A_post": float(aval.iloc[idx_best]["A_post"]),
        "rot_circ_pm_633": float(aval.iloc[idx_best]["rot_circ_pm_633"]),
        "step_pm_633": float(aval.iloc[idx_best]["step_pm_633"]),
        "rot_circ_pm_532": float(aval.iloc[idx_best]["rot_circ_pm_532"]),
    }

    summary = {}
    if os.path.exists(sum_path):
        with open(sum_path, "r", encoding="utf-8") as f:
            soc_sum = json.load(f)
        summary["soc_summary"] = soc_sum

    # distribution stats
    def stats(arr: np.ndarray) -> dict:
        return {
            "count": int(arr.size),
            "median": float(np.median(arr)),
            "p10": float(np.percentile(arr, 10)),
            "p90": float(np.percentile(arr, 90)),
            "mean": float(np.mean(arr)),
        }

    summary["rot_circ_pm_633_stats"] = stats(rot633)
    summary["rot_circ_pm_532_stats"] = stats(rot532)
    summary["target_pm"] = TARGET_PM
    summary["best_match_633"] = best

    out_json = os.path.join(results_dir, "jamming_rotation_485pm_summary.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # plots
    plt.figure()
    plt.plot(aval["av_idx"].to_numpy(), rot633)
    plt.axhline(TARGET_PM)
    plt.xlabel("avalanche index")
    plt.ylabel("rotation circumference (pm) @633nm")
    plt.title("Jamming tremor → rotation scale (ℓ_rot = 2πλ/A)")
    plt.savefig(os.path.join(images_dir, "jamming_rot_circ_vs_av.png"), dpi=200, bbox_inches="tight")
    plt.close()

    plt.figure()
    plt.hist(rot633, bins=25)
    plt.axvline(TARGET_PM)
    plt.xlabel("rotation circumference (pm) @633nm")
    plt.ylabel("count")
    plt.title("Histogram of ℓ_rot across avalanches")
    plt.savefig(os.path.join(images_dir, "jamming_rot_hist.png"), dpi=200, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
