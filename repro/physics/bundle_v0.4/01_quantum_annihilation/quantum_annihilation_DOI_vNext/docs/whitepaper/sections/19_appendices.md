# 19. 부록(Appendices)

> 이 파일은 DOI 패키지의 “재현성 골격”을 한 곳에 모은 부록이다.  
> 본문을 읽지 않아도, 이 부록만으로 정준값 계산, 로그 형식, 검증 절차를 재현할 수 있어야 한다.

## 19.1 정준 상수표(LOCK) & 파생값(derived)

### 19.1.1 CANON LOCK
- `LOCK/canon_lock.json`에 봉인된다.
- 관측으로 역보정하지 않는다.

### 19.1.2 REALIZATION LOCK
- `LOCK/realization_lock.json`에 봉인된다.
- c 구현으로 얻은 a, Δt를 기록한다.
- “전자 1초”에 맞추기 위한 임의 캘리브레이션 금지.

### 19.1.3 CANON DERIVED(결정론 파생)
- `scripts/compute_canon.py`가 `LOCK/canon_derived.json`을 생성한다.
- 포함: r0, δ=1/π², s_p, ν_p, r_e, s_e, ν_e(항등)

---

## 19.2 결정론 계산 스크립트
- `scripts/compute_canon.py`
- `scripts/three_sector_integerize.py`
- `scripts/build_times.py`
- `scripts/estimate_nu_from_eventlog.py`
- `scripts/make_manifest_sha256.py`
- `scripts/make_lock_chain.py`

---

## 19.3 로그/스키마(JSON Schema)
- `schema/*.schema.json`
- event_log.jsonl / signal_log.jsonl 라인 스키마 포함

---

## 19.4 Worked Examples
- `examples/WORKED_EXAMPLES.md` 참조

---

## 19.5 Runbook
- `docs/RUNBOOK.md` 참조

---

## 19.6 최소 재현 체크
```bash
python scripts/make_lock_chain.py
python scripts/compute_canon.py
bash validation/verify_all.sh
```
