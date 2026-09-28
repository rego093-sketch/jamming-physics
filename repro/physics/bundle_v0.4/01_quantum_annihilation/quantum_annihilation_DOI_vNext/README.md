# 양자 소멸(유입/소멸) — 재현성 DOI 패키지 (vNext)

이 패키지는 다음을 **구조적으로** 보장하기 위해 설계되었습니다.

- **정준(CANON)**: 이론 입력(LOCK)만으로 파생되는 값(예: νₚ, νₑ)을 고정하고, 관측으로 역보정하지 않는다.
- **단위구현(REALIZATION)**: 시뮬(칸/틱)→SI 매핑(a, Δt)을 독립 봉인한다.
- **관측(OBS)**: run 단위로 로그(event/signal)를 남기고, 분석 규약(analysis_lock)으로만 처리한다.
- **검증(VALIDATION)**: 자동 PASS/FAIL로 재현성을 판정한다.

## 빠른 실행
```bash
pip install -r reproduce/requirements.txt
python scripts/make_lock_chain.py
python scripts/compute_canon.py
bash validation/verify_all.sh
```

## 핵심 정준값(LOCK 기반)
- rₚ = 0.8412 fm
- νₚ = (D_anch/2rₚ)·(1/π²) = 292.339978122… s⁻¹
- νₑ = 1 s⁻¹ (항등)

## 폴더 구조(요약)
- `LOCK/` : 정준 입력, 단위구현 입력, 분석 규약(봉인)
- `runs/` : run 단위 관측 로그 및 요약
- `scripts/` : 결정론 계산 스크립트
- `validation/` : 자동 검증(PASS/FAIL)
- `schema/` : JSON 스키마(형식 고정)
- `docs/` : Runbook 및 백서

## 불변성 원칙(중요)
- DOI로 릴리즈된 패키지는 **LOCK/와 analysis_lock을 바꿀 수 없습니다.**
- 릴리즈 이후 `validation/verify_one.py --write` 사용은 금지입니다.
