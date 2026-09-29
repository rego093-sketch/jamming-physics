# vp_repro_bundle_v1_3 (single-zip reproducibility bundle)

이 압축파일은 다음을 **단독으로** 제공하도록 구성했습니다.

1) 데이터 스냅샷(Full + Mini)
2) 스키마/코드북/정제 요약
3) 체크섬(sha256) 및 검증 스크립트
4) QA(인수) 자동 생성 스크립트(파일 존재/컬럼/행수/결측/형변환 점검)
5) 백서 TEX 원문(whitepaper/)

## 빠른 시작 (Python)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt

python scripts/reproduce_all.py
```

생성물:
- qa/qa_report.md
- outputs/mini/summary_tables.csv
- outputs/full/summary_tables.csv

## 포함 내용(요약)
- data/full/datasets_v1_2/ : 원본 데이터 스냅샷 + 원 manifest.csv
- data/mini/pf_whitepaper_v1_3_minidata_data/ : R6–R10 미니 재현 CSV
- docs/mini_docs/ : provenance/codebook/methods (원본)
- config/ : 스키마/QA 규칙(자동 생성)
- checksums/ : 통합 SHA256SUMS + 원본 체크섬/manifest 보관
- scripts/ : 체크섬 검증 + QA + 요약 생성
- tests/ : pytest용 간단 무결성 테스트
- whitepaper/ : noah_flood_whitepaper_unified_compat_v2.tex

Generated: 2025-12-30T01:34:52.787331Z

## 중요 (원본 체크섬/QA 보관 파일)
- `checksums/orig_mini_checksums/sha256sum.txt` 와 `qa/orig_mini_qa/qa_report.md` 는 **원본 보관용**입니다.
- 본 번들에서 무결성 검증의 기준은 `checksums/SHA256SUMS.txt` 및 `checksums/manifest_all.csv` 입니다.
