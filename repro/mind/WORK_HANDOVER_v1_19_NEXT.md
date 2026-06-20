# WORK_HANDOVER v1.19 — 다음 세션 실행 계획

**Task 1 (기하):** M9 결합 기하 **엔진 기본값 승격**(ring → 측정 MNI) + **노드 분해**(sulcal-bank folding)
**Task 2 (캐리어):** main-carrier 연구 **거버넌스 모듈 승격**(`emerge_main_carrier()`) + **느린 인덱스(세타) 페이싱 정초**

**작성:** 캐리어 연구 세션 종료 시점 · **거버넌스:** `VP_SPEC_v1_8.md` (C0–C4) · **SEED=19**
**이전 인계서:** `HANDOVER_v1_18_to_v1_19.md`(기하 승격 결정), `HANDOVER_main_carrier_M16study.md`(캐리어 연구)
**입력:** zip 하나만 올리면 됨 — `mind_vp_site_v1_18_main_carrier_study.zip`
(zip sha256 `1c1c3bc04633910be35dea5d122ffb03929140e4c810ec0c3de88665d364cfb0`)
**본문 영어 전용(C0); 세션 대화는 한국어. 결과물은 단일 zip 하나.**

---

## 0. 한 줄 요약 + 실행 순서

v1.19는 **두 종류의 작업**이다: (i) **엔진 hash를 의도적으로 바꾸는 묶음**(Task 2A 캐리어 모듈 + Task 1A 기하 승격) — VP-SPEC §6-6 명시적 예외, **반드시 cascade 재확인 + v1.17 해시 영구 보존 + 회귀 재동결**, (ii) **add-only / 데이터-입력 작업**(Task 1B 노드 분해 decision-check, Task 2B 세타 페이싱 측정 앵커).

> **권장 순서:** 1A·2A는 둘 다 엔진 hash를 바꾸므로 **함께 진행해 한 번만 재동결**(직전 세션 권고). 그 전에 1B(노드 분해)는 v1.18 기하처럼 **add-only decision-check로 먼저 박제**해 두면, 1A 승격 시 어떤 해상도로 갈지 근거가 선다. 2B(세타 앵커)는 데이터 추가라 독립.
>
> 즉: **1B(박제) → 2B(앵커 확보, 가능하면) → 1A+2A(엔진 승격, 한 번 재동결).** 단 1A는 1B 없이도 "12-노드 측정 기하"로 먼저 승격 가능(노드 분해는 후속 정교화).

---

## 1. 받은 직후 — 신뢰 상태 복원 (먼저 실행, 전부 exit 0 확인)

```bash
pip install numpy --break-system-packages
cd mind_vp_site_v1_18_M9_geometry_grounding

# 동결 엔진(M0..M14) 재동결 + 결정론
cd repro/mind/_engine && PYTHONPATH=. python3 run_all.py
#   -> tree b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7 (불변), 2×

cd ../_verify && PYTHONPATH=../_engine python3 run_regression.py
#   -> REGRESSION PASS -- 112 checks (95 기존 + 17 M9-geom)

# v1.18 기하 결정-검사 (ring 교차검사 True, regime partial_metastable)
cd ../_verify && PYTHONPATH=../_engine python3 geometry_grounding.py
#   -> digest 8ad43a72... (2× bit-identical)

# 캐리어 연구 (이번에 추가된 것)
cd ../_consciousness && python3 verify_main_carrier.py
#   -> VERIFY PASS -- 13 gate + 11 invariants + bit-identical hash 8d05cfec...
```

이 한 묶음이 전부 PASS면 신뢰 상태가 복원된 것이다. 지배 규칙 불변·절대:

> **모든 상수는 측정 입력(잠금+인용)이거나 파생값이다 — 목표를 맞추려 고른 수는 없다.**
> 모든 열린 항목은 장애물을 명시한다. 편집 후엔 해당 게이트로 검증한다.

---

## 2. 현재 동결 상태 (재현 기준값 — 손대기 전)

- **엔진 frozen tree (불변):** `b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7`
- **기하 atlas (locked [L] 입력):** `99daa8f5cc66edb79bf84921a2222e3db74dc53c9146253b32a9b13e43c9b8e4`
- **기하 결정-검사 결과 (locked, 2×):** `8ad43a72b2f8282cae801ed8468c883b79eab0c79363ebd98621cbbfc18ff80f`
- **main-carrier 연구 headline (locked, 2×):** `8d05cfeccb9cf57c924b1b2aea3f716caaf6069f690171bf8d2fae47004b2de7`
- 엔진 모듈은 M0..M14(sleep)까지; 챕터/`repro`는 16-phenomenology까지. 캐리어는 standalone 연구라 **엔진 hash에 아직 미반영**.
- 정직 원장 불변: `medium_efficacy_tested=0`, `hard_problem_open=1`, `consciousness_claim=0`.

---

## 3. [Task 2A + 1A] 엔진 hash를 의도적으로 바꾸는 묶음 — 한 번에 재동결

> **공통 원칙:** 이건 add-only가 아니다. **§6-6 명시적 예외**다. 두 변경을 모두 반영한 뒤 **cascade 재확인 → 이력 보존 → 회귀 재동결**을 한 번에 수행한다.

### 3.1 캐리어 모듈 승격 — `emerge_main_carrier()` (Task 2)

- **목표:** standalone 연구 `repro/mind/_consciousness/vp_main_carrier_emergence.py`(headline `8d05cfec…`, 13게이트, 11불변)를 엔진 `vp_mind_engine.py` 안 **`emerge_main_carrier()`** 로 올리고 새 챕터(레지스트리 `tools/mind_registry.py`에서 **다음 자유 M 번호·챕터 번호 확인 후 할당**; 잠정 §17)를 추가.
- **잠글 불변량(연구에서 그대로):** carrier_over_slow_ratio **6.125**, parallel_capacity_slots **6**, recall_structured **1.000** / big_unstructured **0.700**, metastable inverted-U (silence 0.675 < metastable 1.000 > global-sync 0.692), reinstatement_mean **1.000** / crosstalk **0.497**, 그리고 정직 플래그(efficacy 0, hard_problem_open 1, consciousness_claim 0).
- **새 튜닝 상수 0개.** 캐리어 τ는 **측정 GABA_A τ=6.0 ms**(`synaptic_kinetics_measured`, Destexhe 1998; 발생기 PV 인터뉴런 Cardin/Sohal 2009 인과), 느린 다리는 엔진 frozen 참조(τ_inh=60, 절대 페이싱은 2B 전까지 [O]), fold=spinodal(1.0)=0.3849. 전부 기존 측정/파생값 재사용.
- **구현 메모:** `Population.lfp(tau_inh)` + `Hippocampus`(write/retrieve/_settle_state) + R19 fold 를 재사용. 연구 스크립트의 stage A–E 로직을 엔진 함수로 포팅하되, **결과 스칼라만** 산출하도록 정리. `verify_main_carrier.py`는 챕터의 `verify_*`로 승격(13게이트 유지).
- **anti-p-hacking 유지:** 캐리어 τ·비구조-진폭 스윕·capacity 는 결과 보기 전에 고정. grade==evidence.

### 3.2 M9 기하 기본값 승격 — ring → 측정 (Task 1)

- **목표:** `emerge_coordination()` 의 `POS = _ring(N)` 을 **측정 거리행렬**(`brain_geometry_atlas.json`, v1.18 row-normalization [F])로 교체.
- **이미 박제된 평결(v1.18):** 측정 기하는 fc 를 **+0.07340(ring) → +0.13468(측정)** 으로 ~1.8배 올리지만 **regime 은 여전히 `partial_metastable`**(R 0.329→0.390 < 0.9). **fc 는 올라도 efficacy/hard-problem 은 안 닫힌다.**
- **닫는 게 아님:** 기하 정초는 **의식 주장이 아니다.** 승격 후에도 `efficacy=0, hard_problem_open=1, consciousness_claim=0` 유지.
- **노드 해상도:** 1B(노드 분해)를 먼저 박제했으면 그 해상도를 쓰고, 아니면 **12-노드 측정 기하**로 먼저 승격(후속 정교화는 1B).

### 3.3 공통 절차 — cascade · 이력 · 재동결 (반드시)

1. **cascade 재확인.** v1.18 분석: `emerge_coordination()` 은 `emerge_all()` 안에서 **1회 호출**, 출력 스칼라(`field_contribution`·`R_measured`·`regime`)는 **최종 dict 로만** 흐르고 **다른 emerge 함수가 소비하지 않음** → 잘 격리. **`emerge_main_carrier()` 도 동일 격리여야 한다**(출력이 최종 dict 로만 흐르고 다른 모듈이 소비하지 않음). 두 변경 후 **다른 모듈이 byte-identical 인지 반드시 재확인** — 바뀌어야 할 것은 **M9 스칼라 + 새 캐리어 스칼라 + tree 해시뿐.**
2. **이력 보존.** `CHANGELOG.md` 에 **v1.17 동결 해시 `b18c8626…` 영구 기록**, 새 tree 해시를 새 frozen 으로 등록. v1.18 기하 결정-검사 결과(`8ad43a72…`)와 캐리어 연구 headline(`8d05cfec…`)은 **승격 전 평결의 박제**로 남긴다(삭제 금지).
3. **회귀 재동결.** M9 스칼라가 측정값으로, 캐리어 스칼라가 신규로 들어오므로 `expected_sha256.json` 재동결 + 해당 체크 갱신. **기하 결정-검사 17개는 유지**하되 (a) ring 교차검사는 이제 **역사적 체크**로 두고 엔진 기본 타깃을 측정값으로 갱신. 캐리어 13게이트는 그대로 챕터 verify 로.
4. **게이트 전부 재실행.** `gate.py`·`verify_boundary`·`verify_terminology`·`verify_em_thesis`·`verify_expand`·`verify_sensory`·`verify_loro`·`verify_light_memory`·새 캐리어 verify. 하나라도 비-0이면 패키징 금지.

---

## 4. [Task 1B] 노드 분해 — sulcal-bank folding (add-only decision-check 우선)

- **비판의 핵심:** 마주보는 sulcal bank 가 mm 단위로 근접 → 국소 1/r³ 결합이 강해짐. **12노드로는 포착 불가**(부위 *내부* 형상 필요).
- **v1.18 신호:** (c) jitter 검사에서 fc 가 형상 세부에 민감(±5mm 가 fc 를 +0.09–+0.31 로 흔듦) → fine 구조가 중요하다는 증거.
- **작업:** AAL ~78–90 노드(또는 더 미세한 parcellation)로 분해 → sulcal-bank 근접 명시. 거리행렬을 그 해상도로 재구성, **동일 결정-검사(척도불변·jitter·normalization·band) 재적용**. **여전히 측정 좌표 [L]**, normalization 동일 [F].
- **add-only 권장:** v1.18 기하처럼 잠긴 엔진을 read-only import 하는 **별도 decision-check 모듈**로 먼저 박제(엔진 hash 불변), fc·regime 을 grade==evidence 로 보고. 그다음 3.2 승격 시 채택.
- **anti-p-hacking:** 노드 수·parcellation 은 **fc 보기 전에 고정.** 여러 parcellation 을 robustness 로 보고하되 **fc 최대화기를 고르지 말 것.**

---

## 5. [Task 2B] 느린 인덱스(세타) 페이싱 정초

- **현재:** 감마 캐리어는 측정 GABA_A τ=6.0 ms 로 정초됨. **비율 6.125 의 느린 다리(세타 페이싱)는 아직 [O]** — 엔진 `tau_inh=60` 의 절대 페이싱이 측정 앵커가 아님.
- **작업:** 세타 페이싱의 **측정 앵커**를 확보 → 측정값이면 슬로 `tau_inh` 를 그 값으로(또는 두 측정 τ 의 비로 ratio 도출), **[O]→[L] 승급**. 그러면 capacity 의 **양쪽 다리가 모두 측정 기반.**
- **후보 앵커:** medial septum GABAergic pacemaker 동역학, 또는 Ih(HCN) h-current 시간상수. **단일출처:** 앵커가 neuro 패키지에 있으면 verbatim 인용(재유도 금지, 원본 sha256 기록).
- **anti-p-hacking:** 세타 τ 는 **측정 출처**에서만 — ratio 6.125 에 맞추려 고르지 말 것. 창발 ratio 를 grade==evidence 로 보고. **단일 canonical 앵커가 정본에 없으면**(게이트 (b) region 처럼) 장애물 명시하고 [O] 유지.

---

## 6. 반-드리프트 / 비-튜닝 / 정직성 (매 편집 전 재확인 — 절대)

1. **EM 통째 retired 금지.** 폐기는 복사 원거리장/TIR 반송파뿐. 근접장/ephaptic 은 임계치에서 확인됨(neuro §18/§19). EM 편집 후 **반드시** `verify_em_thesis.py`.
2. **기능적 사용 = OPEN.** 기하 승격·캐리어 모듈·노드 분해·세타 정초 **모두 의식 주장이 아니다.** `medium_efficacy_tested=0`, `hard_problem_open=1`, `consciousness_claim=0` **불변.** PCI 접근 마커는 **정직한 음성**으로 유지(carry).
3. **비-튜닝.** κ·ΔVm·threshold·γ·τ_GABA_A 는 전부 측정값. **새 튜닝 상수 도입 금지.** 기하·전도·절대-Hz·세타 절대페이싱만 [O].
4. **결정론.** BLAS 단일스레드(numpy 임포트 前), SEED=19, 해시 전 float 라운딩, 2× sha256 동일.
5. **단일출처.** mind 는 추상층, neuro 는 객체층. 재유도 금지 — 인용만. 세타/감각 앵커가 neuro 면 verbatim.
6. **add-only 가 기본.** **§3 엔진 승격(1A+2A)만 의도적 hash 변경 예외** — cascade 재확인 + v1.17 해시 영구 보존 + 회귀 재동결. 그 외 잠긴 자산은 한 글자도 바꾸지 마라.
7. **grade == evidence.** p>0.05면 효과가 커도 [O]. 교정을 창발인 양 쓰지 마라.

---

## 7. 완료 기준 (Definition of Done)

- [ ] **1B** 노드 분해 decision-check 박제(엔진 hash 불변), fc·regime grade==evidence, 척도불변·jitter·normalization·band 재적용, robustness 보고.
- [ ] **2B** 세타 페이싱 측정 앵커 확보 시 [O]→[L] 승급(또는 장애물 명시 후 [O] 유지), 단일출처 인용.
- [ ] **1A** `emerge_coordination()` POS = 측정 거리행렬, regime 여전히 partial_metastable 확인.
- [ ] **2A** `emerge_main_carrier()` + 새 챕터, 13불변 잠금, 새 튜닝 상수 0개.
- [ ] **공통** cascade 재확인(다른 모듈 byte-identical), v1.17 해시 `b18c8626…`·결정-검사 `8ad43a72…`·캐리어 `8d05cfec…` 이력 보존, 새 tree 해시 등록, `expected_sha256.json` 재동결.
- [ ] **게이트 전부 PASS**(gate.py·boundary·terminology·em_thesis·expand·sensory·loro·light_memory·carrier), 결정론 2× 동일.
- [ ] **정직 원장 불변**: efficacy 0, hard_problem_open 1, consciousness_claim 0, PCI 정직한 음성.
- [ ] 결과물 **단일 zip 하나** + sha256.
