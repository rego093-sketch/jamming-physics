# CHANGELOG v0.9.2 — 혼란 방지 전체 적용 (2026-06-14)

v0.9.1(표시 수치 드리프트 4건 교정 + SSOT 도구·잔차지도·규율)에 이어, 혼란 방지를 **빌드·기록·산문
전반에 적용**. 이론 예측값 불변.

## (1) 수치 드리프트 게이트를 정식 Phase로 통합 — 재발 자동 차단
- `tools/gate.py`에 **`--phase 4`** 추가: 본문(`txt/`+`docs/physics/`)과 `eq_list` 표시값이 정준
  재생성(SSOT `tools/vp_numeric_ssot.py`)과 어긋나면 **FAIL → 빌드 차단**.
- 검증: 현재 패키지 PASS / `292.244` 재주입 시 정확한 위치와 함께 FAIL(exit 1) / 원복 후 PASS.
- 80자리 A=cΔt/a 는 §3.4 placeholder 면책으로 검사 제외. 스캐폴딩(reports·dossier)은 범위 밖.
- 기존 게이트가 못 잡아 v0.7→v0.9 내내 생존하던 +57·292.244류가 이제 구조적으로 통과 불가.

## (2) 보존된 dossier/reports 정합 — 해결완료 배너
- 옛 리터럴을 *발견사항*으로 담은 10개 스캐폴딩 .md 상단에 **정밀 배너** 부착: 드리프트 4건이
  본문·eq_list·SVG에 반영되고 phase4로 차단됨을 명시(감사기록 본문은 보존, 다른 항목은 원 상태).
- 대상: reports/·verification_dossier/의 NUMERIC_LEDGER·PHASE1-2_AUDIT_FINDINGS·PHASE3_REPORT·
  VERIFICATION_AND_SUPPLEMENTATION_PLAN·PHASE1_PATCH_SPEC, remediation/PHASE1_PATCH_SPEC.

## (3) 산문 잔차 기준선 라벨 — §13.5 스타일로 누락분 부착
- 본문 잔차 121건 조사: 67건은 이미 기준선 명시, 나머지 대부분은 인접 수식이 곧 기준선이거나
  비-잔차 백분율(34% 슬롯·98% 상쇄·0.03% 민감도 등). **진짜 누락 ppm 잔차에만** 부착(과잉주입은
  오류를 심으므로 배제):
  - §13.4(L779) 길이경로 `+42 ppm` → **`+42 ppm vs measured 1836.15`** (R5).
  - §1(L463) `α_em⁻¹ +3 ppm` → **`α_em⁻¹ +3 ppm vs measured`**.
  - rf(L41) `6π⁵ (19 ppm)` → **`(19 ppm vs measured)`**.
- rf 강제계수표 뒤 + rf html에 **잔차지도 상호참조** 1줄: "흩어진 −19/+19/+42/+61 ppm은 독립 잔차
  R1·R3 둘로 환원됨(정의는 정준 원장 Residual Map)". manifest 단어수·_meta 정합 갱신.

## 검증 (모두 PASS)
- `gate.py` **Phase 1·2·3·4 전부 PASS**. 구조 46섹션/1257수식 불변.
- manifest 단어수 갱신(rf 2307→2339, §13 6123→6127, §1 6833→6835), _meta totals +38.

## 미변경
- 핵심 닫힌형 수치 전부 불변. reports/·verification_dossier/·remediation/ 은 과정 기록으로 보존.
