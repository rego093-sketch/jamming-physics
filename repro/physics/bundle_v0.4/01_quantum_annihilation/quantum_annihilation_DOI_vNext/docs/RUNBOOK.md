# RUNBOOK (실험→로그→검증→릴리즈)

## 1) 원칙
- 정준(CANON)은 `LOCK/canon_lock.json`으로 봉인한다.
- 단위구현(REALIZATION)은 `LOCK/realization_lock.json`으로 봉인한다.
- 분석 규약(PROTOCOL)은 `LOCK/analysis_lock.json`으로 봉인한다.
- 관측(OBS)은 `runs/run_<ID>/` 아래에만 존재해야 한다.
- 관측으로 정준을 역보정하는 행위(피팅/보정)는 금지.

## 2) 새 run 만들기(권장 절차)
1. `LOCK/`가 최신인지 확인(버전 고정)
2. `runs/run_<ID>/sim_lock.json` 작성(해상도/경계/seed/총틱/업데이트 규칙)
3. 시뮬 실행 → `event_log.jsonl`, (권장) `signal_log.jsonl` 생성
4. `validation/verify_one.py --write runs/run_<ID>`로 summary/checksums 생성 (릴리즈 전)
5. `bash validation/verify_all.sh`로 전체 PASS 확인
6. `python scripts/make_manifest_sha256.py`로 MANIFEST 생성
7. DOI 업로드(압축파일). 이후 변경 금지.

## 3) 로그 최소 요건
- `event_log.jsonl` : 사건 기반 카운트(전자/양성자) 기록
- `run_meta.json` : 코드해시/LOCK 해시/해상도/경계/총틱 등 메타데이터
- `checksums.json` : run 산출물 sha256
