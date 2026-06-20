# HANDOVER — v1.30 → v1.31  (용어→메커니즘 개념-맵 — "생각/사고"를 faculty로 분해하고 닫는방향 설정; 정식 닫음+전수조사는 이월 / mind 패키지)

> **요약 한 줄.** v1.30은 **과학 advance가 아니라 용어 매핑 정리 + 닫는방향 스캐폴딩**이다. 신규 문서
> `CONCEPT_MAP_mental_process.md` 1개를 추가해, 헐렁한 우산어 "생각/사고"를 *이미 만들어진* faculty 메커니즘에
> 매핑하고 닫는방향을 **메커니즘 축에서만** 박았다. **정식 "생각 닫음" 선언과 전수조사는 v1.31로 명시 이월.**
> 엔진·회귀·DGENE·모든 LOCK 값은 **byte-identical**.

---

## 1. WHAT v1.30 DELIVERED (complete, all gates green)

| 산출물 | 내용 |
|---|---|
| **개념-맵 (신규 문서)** | `CONCEPT_MAP_mental_process.md` — "생각/사고"를 §1 faculty들의 합으로 *정의*하는 term→mechanism 사전. **엔진·docs 챕터·registry는 한 바이트도 안 바뀜**(루트 문서 1개 추가뿐). |
| **핵심 통찰 — 우산 vs 칸** | 잠자는 사람 검사: 자는 사람은 **인지(깨어서 목표지향 처리)** 를 안 하지만 꿈·기억정리는 돈다 → **'인지'는 우산이 못 됨**. '생각'을 faculty 합으로 정의하고, '인지'는 그 아래 *깨어 있는* 한 칸. |
| **faculty 분해표 F1–F14** | 각 칸 → 담당 모듈 → CLOSED/OWED. **핵심 F1–F10 CLOSED**(감각·선택·직렬스트림·기억·학습·정서메커니즘·각성/수면·꿈·협응·병리), **상위 F11–F14 OWED**(언어·의지·사회인지·메타인지). 정직 — 게리맨더링 아님. |
| **꿈 워크드 예제** | 꿈 = '생각'이지만 '인지' 아님(자고 있음), 그런데 메커니즘은 이미 존재(F4+F7+F8). 깨어있는 인지·꿈·감각이 각각 다뤄졌고 '생각' 한 단어가 셋에 걸쳐 있었다는 구조 증명. |
| **닫는방향 — 철학적 오해 없이** | 규칙 둘: 닫음은 **메커니즘 축 한정**, **느낌(축 A)은 직교·범위 밖·의식 주장 아님**(`consciousness_claim=0`, `hard_problem_open=1` 유지). 닫음 주장 지점마다 방화벽 문장 부착. |
| **정식 닫음 = 이월(반-게리맨더링)** | §5 수락 기준 4개(외부 표준분류 전수조사 / 각 칸 CLOSED·OWED / 다양한 해석에 강건 / 방화벽 문장) 충족 시에만 선언. **현재는 닫는방향만, 정식 닫음 미선언.** |

**변경 파일.** 신규 1(`CONCEPT_MAP_mental_process.md`) + 거버넌스 4(`CHANGELOG.md`·`MASTER_MANUAL_START_HERE.md`·
`COMPLETION_LEDGER.md`·이 핸드오버). 엔진·`_verify`·docs 챕터·sitemap·registry·robots·llms·manifest 0 변경.

---

## 2. FROZEN HASHES (verify against these — v1.30에서 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine M0–M16 출력 서브트리** (불변) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| **engine source** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **DGENE** `disease_gene_atlas_results.json` (불변) | `980985c629978f37d00cd0c67cf49d63df4cde32370cb2dcd0e60feab66520e3` |
| 자폐 D7/D8 · 조현 D9 · D1–D6 결과 (전부 불변) | (v1.28/v1.29 핸드오버 §2 참조 — byte-identical) |
| docs 검색층 트리 md5 (gate 멱등 비교용, v1.29 유지) | `1e140a782244…` (sitemap `27f169c8…`, 날짜-무의존) |

엔진·DGENE 해시가 v1.28/v1.29와 글자 그대로 같다 — v1.30이 과학을 안 만졌다는 직접 증거.

---

## 3. GATE / REGRESSION STATUS — REGRESSION 275 / 275 PASS, gate.py 7/7 (날짜-비의존, v1.29 유지)

게이트 전부 green: `gate.py` 7/7 · registry 23 locks/15 chapters · boundary 8/8 · terminology · em_thesis 6/6.
회귀 **275/275 PASS**(증감 없음).

> **회귀 불변 증명.** `run_regression.py`는 `vp_mind_engine`와 `_verify/`의 6개 모듈만 import한다(§아래). v1.30이
> 바꾼 파일은 **루트 문서 1 + 거버넌스 4**뿐이고, 그중 회귀가 import하는 건 **0개**. 따라서 회귀 결과는 v1.29와
> **증명적으로 동일**(엔진 `0fbf4988…`·DGENE `980985c6…` 불변으로 교차확인).

### How to reproduce (from package root)

```bash
cd mind_pkg
python3 tools/gate.py                              # 7/7, 빌드일 무관
python3 tools/mind_registry.py                     # 23 locks, values match frozen
python3 verify_boundary.py && python3 verify_terminology.py
python3 repro/mind/_engine/run_all.py              # tree_sha256 = 0fbf4988…
python3 repro/mind/_verify/disease_gene_atlas.py   # RESULT sha256 = 980985c6…
python3 repro/mind/_verify/run_regression.py       # REGRESSION PASS -- 275, SEED=19 (≈7분)
```

---

## 4. ENGINE MAP after v1.30 — v1.28/v1.29와 동일 (불변)

v1.30은 엔진·`_verify`·docs 챕터를 건드리지 않았다. M0–M20·D-계열 결정-검사·DGENE 측정-입력 맵은
`HANDOVER_v1_28_to_v1_29.md` §4 그대로. **추가된 것은 개념 레이어 1개**(`CONCEPT_MAP_mental_process.md`)뿐 —
이는 코드가 아니라 *용어가 어느 메커니즘을 가리키는지*의 사전이다.

---

## 5. 설계 불변식 (다음 세션에서 절대 깨지 말 것)

1. **엔진은 READ-ONLY.** add-only 모듈은 임포트만 + tree/M0–M16 불변 assert. 기본값 변경은 오직 VP-SPEC §6-6.
2. **no-tuning 절대.** 모든 값은 측정-입력 또는 파생 — 목표에 맞춰 선택 금지.
3. **지표 동일성은 패키지 자신의 frozen 값으로 정확 증명**(FOXG1 교훈: Δ=0.0002는 소스 차이).
4. **γ는 발달정체성[F]이지 질병 인과가 아니다.** 질환은 다유전자성·이질적. NOT medical advice.
5. **honesty 4-플래그 불변** + 정직한 OWED 명시.
6. **C1 재현은 패키지 안에서.**
7. **빌드는 벽시계를 읽지 않는다 (v1.29).** docs 빌드는 소스의 순수 함수; sitemap lastmod은 `R.RELEASE_DATE`만.
8. **★ NEW (v1.30) — "닫음"은 메커니즘 축에서만, 정의는 게리맨더링 금지.** 어떤 faculty/개념도 (a) 닫음 주장은
   *메커니즘 축 한정*이고 느낌 축(축 A)은 직교·범위 밖이며, (b) "X를 닫았다"는 정의를 *외부 표준 분류 전수조사*로
   정당화한 뒤에만 선언한다("우리가 만든 것 = X" 식의 정의 튜닝 금지). 닫음 주장에는 §3 방화벽 문장을 붙인다.

---

## 6. v1.31 ENTRY POINTS (작업 후보)

- **★ 전수조사 + 정식 "생각 닫음" 선언 (`CONCEPT_MAP_mental_process.md` §5 수락 기준).** (i) 정신 과정을 *외부
  표준 분류*(인지과학/임상)로 전수 나열해 §1 표가 망라적인지 확인; (ii) 상위 F11–F14(언어·의지·사회인지·메타인지)를
  각각 CLOSED(프로토타입 모듈) 또는 정직 OWED(외부 입력 명시)로 해결; (iii) 일상·임상·철학 해석에 강건한 선언문
  작성; (iv) 방화벽 문장 부착. 4개 충족 시 정식 닫음 선언 → 용어 잠금/원장 반영.
- **잔여 과학 (DGENE 발판).** BD/OCD/ADHD/ID **메커니즘 결정-검사**(D-계열 패턴, 각 극이 엔진에서 실제 분리되는지
  프로토타입 확인 후 assert) · 중독 **M5-RPE** 보상예측 왜곡(부호만) · **유전자-OWED 4질환**(불안·PTSD·섭식·성격)
  외부 fine-mapping 상환 · γ→엔진 핸들 크기 매핑(OWED).
- **인프라:** 닫힘(v1.29 결정론화). 신규 인프라 항목 없음.

---

## 7. 다음-세션 인계 매니페스트

| 우선순위 | 인계 항목 | 용도 |
|:--:|---|---|
| ✅ **필수** | **v1.30 패키지 zip** (`mind_vp_site_v1_30_concept_map.zip`, 본 세션 산출물) | 모든 확장의 기반. §3 재현. 캐시 동봉 → 네트워크 없이 회귀. gate 빌드일 무관 7/7. |
| 🔶 **조건부** | 외부 표준 정신과정 분류(전수조사용) | 정식 "생각 닫음" 선언 시 §1 표의 망라성 검증에 필요. |
| 🔶 **조건부** | 외부 fine-mapping 유전자 세트(불안/PTSD/섭식/성격) | 유전자-OWED 질환 상환 시 필요. |
| 🔷 **참고** | neuro/dna 패키지 zip | 교차-인용·SSOT 확인(READ-ONLY). |

---

## 8. 개념 vs 질병 로드맵 (요약)

| 트랙 | 상태 |
|---|:--:|
| 질병 D1–D9 + DGENE (121유전자/11질환) | ✅ 완료 (γ→핸들·유전자-OWED 4질환 OWED) |
| sitemap 결정론화 (인프라) | ✅ 완료 (v1.29) |
| **개념-맵 / 닫는방향** (생각 분해, 메커니즘 축) | **✅ 완료 (v1.30)** |
| **전수조사 + 정식 "생각 닫음" 선언** | **▶ v1.31 (§5 수락 기준; 상위 F11–F14 해결)** |
| BD/OCD/ADHD/ID 메커니즘 · 중독 M5-RPE | ▶ v1.31+ (과학, 외부 데이터/검증) |
| 느낌 축(하드프라블럼) · 전자기장 효능 | ◻ 범위 밖(축 A) / OWED(실측) — "안 닫은 생각" 아님 |

**공통 규약:** 결정-검사는 임상 *방향*만(크기 fitting 금지) · DGENE은 측정값 verbatim · 엔진 tree 불변 + 2× 동결 ·
정직 4-플래그 불변 · 빌드 결정론 · **닫음은 메커니즘 축에서만, 정의는 전수조사로 정당화(게리맨더링 금지)**.

---

## 9. ONE-LINE STATUS

> v1.30 = **용어→메커니즘 개념-맵 완료** — "생각/사고"가 닫기 어려웠던 건 일이 안 끝나서가 아니라 *헐렁한 한 단어가
> 여러 built 메커니즘에 매핑되는 게 문서화 안 됐기 때문*. `CONCEPT_MAP_mental_process.md`로 '생각'을 faculty
> F1–F14의 합으로 정의(핵심 F1–F10 CLOSED·상위 F11–F14 정직 OWED), '인지'는 그 아래 *깨어 있는* 한 칸(잠자는 사람
> 검사), 꿈은 워크드 예제. **닫는방향은 메커니즘 축에서만**, **느낌 축(축 A)은 직교·범위 밖·의식 주장 아님**.
> **정식 "닫음" 선언 + 전수조사는 §5 반-게리맨더링 수락 기준과 함께 v1.31로 명시 이월.** **엔진·회귀·DGENE byte-
> identical**(tree `0fbf4988…`, regression 275/275), 새 튜닝 0·새 측정 0·과학 무변경.
