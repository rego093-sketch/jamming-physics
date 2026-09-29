# Reproduce (Integrity + QA)

본 번들은 **(A) 무결성 검증**과 **(B) QA/요약 재생성**을 1회 실행으로 제공합니다.
백서의 모든 표/그림을 완전 재생산하는 "전체 분석 파이프라인"은 본 번들에 포함되어 있지 않으므로,
본 번들이 약속하는 재현성은 아래 2개 범위로 정의합니다.

- 범위 A: 파일/데이터 무결성(sha256, bytes) 검증
- 범위 B: 스키마/형변환/결측/기본 QC(자동 QA 리포트 생성)

## A. Checksum verify
```bash
python scripts/verify_checksums.py
```

## B. QA + summaries
```bash
python scripts/run_qa.py
python scripts/make_summaries.py
```

또는 한 번에:
```bash
python scripts/reproduce_all.py
```

## Notes
- Full 데이터는 파일 수가 더 많지만, 제공된 스냅샷은 크기가 작아 로컬에서 빠르게 QA 가능합니다.
- QA 규칙은 config/qa_rules.yaml 에 있으며, 필요한 경우 사용자가 강화/수정할 수 있습니다.

## Optional: R8 RSL (-5 m crossing) demo
```bash
python scripts/wp_r8_rsl_crossing.py
```

