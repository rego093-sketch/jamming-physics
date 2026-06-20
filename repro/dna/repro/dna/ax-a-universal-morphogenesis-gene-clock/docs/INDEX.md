# 문서 색인 (docs/) — universal_morphogenesis_geneclock

이 패키지의 문서는 v12.3 정리에서 `docs/` 아래로 분류되었다. **코드(`code/`), 검증
(`verify_all.py`, `expected_sha256.json`, `repro/`, `results/`)는 그대로다 — bit-for-bit 핀
무변경, 검증 OVERALL: PASS (20/20) 유지.** 문서 파일은 sha 핀 대상이 아니므로 이동해도 검증에
영향이 없다. `code/emergence_v2/`·`code/analyses/` 내부의 LEDGER/CHANGELOG/NULL 문서는 해당
엔진과 co-located 설계라 **이동하지 않고 원위치 유지**한다.

## 루트 (entry docs)
- `README.md` — 패키지 개요 + 통합 법칙 abstract claim-strip
- `VERSION` — 버전 이력 (v12.3 정리 노트 포함, 최신이 위)
- `REPRODUCE.md` — 재현 절차 (의존성 · `python3 verify_all.py`)

## docs/changelogs/ — 버전별 변경 이력 (10)
v5 · v5_1 · v6 · v7 · v8 · v9 · v10_organ · v11_organ_anatomy · v12_heart · v12_1_systemic_recovery
(누적 이력 — 삭제하지 않고 보존. 최신 작업 요약은 VERSION 머리 참조.)

## docs/handoffs/ — 세션 인계서 (4, 역사적)
- `HANDOFF.md` — 메인/누적 인계서 (대형)
- `HANDOFF_v10_organ.md` · `HANDOFF_v11_organ_anatomy.md` · `HANDOFF_v12_heart.md` — 버전별
(Phase 6 fold-in 완료 · Phase 7(v12.4) 완결 — 현재 진입점은 VERSION v12.4 노트 및
`docs/overview/DISCOVERY_AUDIT_phase7.md`(남은 로드맵 분류).)

## docs/ledgers/ — 양별 등급 원장 (12, 패키지 루트 레벨)
adipose · dev_timing · dev_timing_robust · dev_timing_wide · gene_clock · heart · life_course ·
morpho_decomposition · organ_anatomy · organ_emergence · **systemic_recovery**(통합 grade-of-record) ·
timing_predictors
> 참고: emergence 층 원장은 `code/emergence_v2/`에 co-located 유지 —
> `LEDGER_emergence_engine.md` · `LEDGER_emergence_organs.md` · `LEDGER_emergence_trajectory.md` ·
> `LEDGER_organ_allometry_wide.md`(Phase 5) · `CHANGELOG_phase5_organ_allometry_wide.md` ·
> `LEDGER_morphogen_length.md`(Phase 7) · `CHANGELOG_phase7_morphogen_length.md`.
> 경계분석 해설은 `code/analyses/NULL_존재이유_그리고_모델한계.md`.

## docs/overview/ — 종합 (3)
- `PROJECT_SUMMARY.md` — 프로젝트 전체 아크
- `WHY_THE_NULL_AND_MODEL_LIMITS.md` — null의 의미와 모델 한계
- `DISCOVERY_AUDIT_phase7.md` — 남은과제 전수 감사 (완결/선택/데이터-차단 분류; Phase 7)

---

### 등급 표기
**[V]** in-package 검증/재현(2× sha256) · **[L]** 잠긴·인용 독립측정/범용법칙 · **[F]** 고정
모델링 선택 · **[O]** 열림(측정입력 공백 명명, 미주장)

### 상호참조 안내
이동 전 일부 문서/주석은 동료 문서를 파일명(예: `LEDGER_gene_clock.md`)으로 교차참조한다. 정리 후
이 파일들은 위 `docs/` 하위에 있다 — 파일명으로 검색하면 찾을 수 있다. **pinned 코드 주석의
참조 문구는 핀 보존을 위해 수정하지 않았다**(파일명 자체는 동일하므로 추적 가능).
