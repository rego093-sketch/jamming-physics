# DOI 업로드 메모

이 저장물은 “정준(CANON) / 단위구현(REALIZATION) / 관측(OBS) / 분석(PROTOCOL)”을 분리하여
튜닝 논란 없이 재현성을 확보하는 것을 목표로 한다.

## 핵심 파일
- LOCK/canon_lock.json
- LOCK/realization_lock.json
- LOCK/analysis_lock.json
- LOCK/LOCK_CHAIN.json
- LOCK/canon_derived.json
- schema/*.schema.json
- validation/verify_all.sh, validation/verify_one.py
- runs/run_*/ (최소 1개)

## 무결성
- MANIFEST.sha256 : 전체 파일 sha256 목록
- runs/run_*/checksums.json : run 단위 sha256 목록
