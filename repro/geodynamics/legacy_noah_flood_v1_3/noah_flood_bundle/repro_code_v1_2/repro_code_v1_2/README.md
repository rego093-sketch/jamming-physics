# 재현성 코드 번들 v1.2 (Scripture × U‑J × Triple Axis)
이 번들은 공개 CSV/텍스트 데이터(동봉된 `datasets_v1_2.zip`)를 읽어
간단한 검증·요약·무결성(해시) 체크와 일부 지표 산출을 수행합니다.

## 실행
```
python3 code/run_all.py --data-root ../datasets_v1_2
```

## 산출
- `docs/run_manifest.json` : 실행 환경/파일 해시/간단 요약치
- `docs/qc_report.txt` : 데이터 존재/스키마·범위 점검 결과
- `docs/metrics_summary.json` : RSL/Delta/BIO 요약치

## 의존성
- Python 3.9+
- pandas, numpy, matplotlib (플롯은 선택적. 본 스크립트는 표·요약치 중심)
