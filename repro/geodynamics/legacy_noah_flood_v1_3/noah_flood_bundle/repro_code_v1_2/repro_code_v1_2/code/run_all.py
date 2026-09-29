import os, json, hashlib, argparse, pandas as pd, numpy as np
from modules import qc, rsl_mod, delta_mod, bio_mod

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default="../datasets_v1_2", help="데이터 루트 폴더")
    args = ap.parse_args()

    os.makedirs("../docs", exist_ok=True)
    report = {}

    # QC
    qc_report = qc.run(args.data_root)
    with open("../docs/qc_report.txt", "w", encoding="utf-8") as f:
        f.write(qc_report)

    # RSL
    rsl_out = rsl_mod.run(args.data_root)
    # Delta
    delta_out = delta_mod.run(args.data_root)
    # BIO
    bio_out = bio_mod.run(args.data_root)

    # 요약 병합
    metrics = {"RSL": rsl_out, "Delta": delta_out, "BIO": bio_out}
    with open("../docs/metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    # 매니페스트(파일 해시)
    manifest = qc.hash_manifest(args.data_root)
    with open("../docs/run_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("DONE. See docs/qc_report.txt and docs/metrics_summary.json")

if __name__ == "__main__":
    main()
