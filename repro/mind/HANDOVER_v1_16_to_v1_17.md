# HANDOVER v1.16 → v1.17 — mind / Felt Cognition

**작성:** v1.16 세션 종료 시점 · **거버넌스:** `VP_SPEC_v1_8.md` (C0–C4) · **SEED=19**
**이전 인계서:** `HANDOVER_v1_15_to_v1_16.md` (M13 스펙트럴, 1/f 폐쇄, 핵심 0.80)

---

## 0. 한 줄 요약

**M14 `emerge_sleep_architecture()` 추가 완료.** 같은 단일 기질 위에서 **시상-망상핵 수면방추(11–16 Hz)**를
창발시켜 M12가 owed로 남겼던 `sleep_spindle_hz`를 **창발로 폐쇄** → **핵심 측정-관측값 카탈로그 0.80 →
0.85 (17/20)**. 피질 **느린진동(<1 Hz)**, 방추 **점강점쇠** 시그니처, **NREM/REM 대역이동**, **REM 꿈-회상
루프**(M2 해마)까지 같은 기질에서 방출. **새 튜닝 상수 0개**, **M0–M13 14개 모듈 바이트 불변**, 회귀
**75개 검사 PASS**, 정직한 원장 불변(`efficacy=0`, `hard_problem_open=1`, `consciousness_claim=0`).

**새 동결 tree_sha256:** `8006fb9fc4cf7210600306e383b447884dbe04430d3c3aa1c878fa64872b9ec4`

---

## 1. M14 가 정확히 한 일 (물리/기전)

수면방추는 시상피질(TC)–망상핵(TRN) 루프의 11–16 Hz **점강점쇠(waxing-waning)** 진동이다. M14 는 이것을
**맞추지 않고 창발**시킨다.

### (a) 반송 주파수 = 인용 시상수가 결정 (튜닝 아님)
- 각 TC 세포 = **R19 3차 쌍안정 막**(빠른 변수 s, τ_m) + **느린 회복 변수 w = T-전류 비활성화 회복**(τ_rec).
  이 2변수 세포는 교과서적 **이완진동자**이고, 그 주기는 **τ_rec 에 매끄럽게 비례**한다(프로토타입에서
  단조 확인).
- **인용값:** τ_rec = **13 ms** (Huguenard & McCormick 1992, T-전류 비활성화 회복, 탈분극 영역),
  τ_m = **4 ms** (고전도 활성 TC 막, Destexhe et al. 2003). → 단일세포 14.89 Hz, 개체군 **15.38 Hz**.
- **핵심:** 11–16 Hz 를 목표로 상수를 고른 게 아니라, **인용 시상수가 그 대역에 떨어진다**. 창발한
  주파수를 그대로 보고한다(15.38 Hz, in-band).

### (b) 통로/순환 = M9 ephaptic 링, 단 **확산(라플라시안) 결합**
- 결합: `κ·(평균장 − s)` (행정규화 커널 Wk 의 평균장에서 자기값을 뺀 **라플라시안**). **동기화 지점에서
  0** 이 되므로 **위상만 동기화하고 반송 주파수를 흔들지 않는다**.
- **왜 중요한가(디버깅 기록):** 이전 시도(proto9)는 행정규화 ephaptic 장 `κ·Wk@s ≈ 0.55·s` 를 막
  방정식에 **직접 더해** 유효 선형이득을 1→1.55 로 바꿔 버려 반송이 **4 Hz 로 끌려갔다**. 라플라시안 결합이
  이 문제를 깨끗이 해결한다. (전체 9→17 프로토타입 기록은 이전 transcript 에 있음.)

### (c) 점강점쇠 = 쌍안정 동원 이완진동자 + 인용 Ca→Ih 적응
- **동원 변수 r**(같은 R19 3차 쌍안정): `dr/dt = (r − r³ + drive − a)/τ_r`. 게이트 G = ½(1+tanh 2r)
  ∈ [0,1] = 동원분획.
- **느린 적응 a**(Ca→Ih): `da/dt = (a_gain·G − a)/τ_a`, **τ_a = 900 ms** (Lüthi & McCormick 1998,
  Ca-매개 Ih 상향조절 → 방추 종료·불응기).
- **되먹임 폐쇄:** 동원된 풀만 Ca 적재 → Ca 가 Ih 상향 → Ih 가 풀 탈동원 → 방추 종료 → Ca 청소 →
  재동원 → 다시 점강. **방추간 간격 ~4 s (NREM-2 적), 창발.** 정현파 아닌 펄스열이라 측정 스펙트럼의
  부엽은 15.38±~1 Hz 로 대역 내에 머문다(피크는 15.38 유지).
- **측정 신호 = G(t)·평균반송(t)**: 반송 주파수는 보존, 점강점쇠는 G(t) 가 만든다.
- **drive = 0.60 (NREM-2 흥분도 작동점):** 방추가 **일어나는 영역**(δ보다 얕고 각성보다 깊은 창)을
  고르는 것이지 **주파수를 고르는 게 아니다**. drive를 흔들면 0.55 미만에서 방추가 사라지는 분기가 있는데,
  이는 "방추는 특정 막전위 창에서만 일어난다"는 **생리학적 사실**(Steriade et al. 1993)과 일치. drive는
  ISI(반복률)만 좌우하며 보고만 한다.

### (d) 신규 관측값 (같은 기질)
- **slow_oscillation_hz** [0.1,1.0]: 피질 Up/Down 이완진동(R19 3차 + 느린 적응). τ_a = **600 ms**
  (Sanchez-Vives & McCormick 2000 / Compte 2003, Na/Ca-의존 K⁺·시냅스억압 회복) → **0.49 Hz 창발**,
  8/8 < 1 Hz.
- **spindle_waxing_waning**: 진폭변조 깊이 **0.975**, 8/8 > 0.5 (De Gennaro & Ferrara 2003).
- **nrem_rem_band_shift**: REM(θ+γ)/NREM(δ+방추) 마커비가 REM 상태에서 25.4× 더 큼, 8/8 방향 일치.

### (e) 메커니즘 시연 (재채점 안 함)
- **REM 꿈-회상 루프:** `_m13_recall` 재사용 — REM 강한 θ-γ 결합 → 해마 큐 완성(회상 **1.000**),
  NREM-SWS 약결합 → 큐 실패(**0.531**). M12 에서 **이미 matched 인** `dream_recall_theta_increase` 를
  실제 메커니즘으로 존중. **새 점수 아님** (중복 제거).

---

## 2. 카탈로그 회계 (누적, 중복 제거)

| 항목 | 값 | 비고 |
|---|---|---|
| 핵심(core) 카탈로그 | **17 / 20 = 0.85** | M13이 1/f, M14가 방추 폐쇄 |
| 확장(extended) 카탈로그 | 23 / 27 = 0.852 | 20 + M13 신규 4 + M14 신규 3 |
| M14 수면 관측값 | 4 / 4 = 1.0 | spindle·SO·waxing·band-shift 모두 matched |

**아직 owed (M15 가 닫을 것):** `sws_delta_amplitude_uv`(µV 보정), `panic_peak_minutes`(분 보정),
`p300_latency_ms`(ms 보정). 모두 **무차원 창발 → 임상 단위** 변환에 **측정·인용된 µV·ms 앵커**가 필요.

---

## 3. 복원·검증 명령 (다음 세션 첫 실행)

```bash
# 패키지 압축 해제 후 repro/mind 기준
cd repro/mind/_engine && PYTHONPATH=. python3 run_all.py
#   → tree_sha256 = 8006fb9fc4cf7210600306e383b447884dbe04430d3c3aa1c878fa64872b9ec4

cd ../_verify && PYTHONPATH=../_engine python3 run_regression.py
#   → "REGRESSION PASS -- 75 checks ... SEED=19"
```

2회 연속 `run_all.py` 의 tree_sha256 이 동일하면 결정성 OK (이번 세션에서 확인 완료).

---

## 4. 동결 기준값 — M0..M14 per-module sha256 (§5)

```
67d0e16fc0a13d91  M0_organ_emergence          ← v1.15와 동일 (바이트 불변)
93cb9217eea5bb2f  M1_em_brainwave             ← 동일
c11c9e81fecafe21  M2_hippocampal_memory       ← 동일
30d43c12ccf743e6  M3_parallel_eddies          ← 동일
f537069905bda2e6  M4_selection                ← 동일
9c3f0d700c8a4eaa  M5_learned_field            ← 동일
2acad7efe0ed4f0d  M6_stream_of_thought        ← 동일
1da341a3a7223a76  M7_embodied_open            ← 동일
678ea5b780f8ae53  M8_field_coherence          ← 동일
eba74585397d3e53  M9_em_coordination          ← 동일
42e6f81ecedc1729  M10_sensory_coupling        ← 동일
ba02b3d41d836a42  M11_light_memory_binding    ← 동일
bab1be8ff7df3a76  M12_brainwave_phenomenology ← 동일
a822468ddd037675  M13_spectral_observables    ← 동일
7866905d0babd551  M14_sleep_architecture      ← 신규 (이번 버전)
─────────────────
TREE 8006fb9fc4cf7210...  (전체 트리)
```

**M0–M13 14개가 v1.15 §5 와 한 글자도 다르지 않음** = 가산(additive)-only 증명. M14 만 새 해시.

---

## 5. 다음 작업 — v1.17 = M15 `emerge_calibration_bridge()` (제안)

**목표:** 무차원 창발을 임상 단위로 옮기는 **단 하나의 측정·인용된 µV 앵커 + 하나의 ms 앵커**. 이로써
세 개의 owed 관측값(`sws_delta_amplitude_uv`, `panic_peak_minutes`, `p300_latency_ms`)이 닫힌다.

- **반드시 측정·인용값일 것.** 예: SWS 델타 진폭의 인용된 두피 µV 범위 1개, P300 잠복의 인용된 ms 1개.
  **목표를 맞추려고 스케일을 고르면 안 된다** — M13 의 각성-평탄화를 7/8 < 0.9 게이트로 **owed 로 남긴
  규율**을 그대로 따른다.
- **단일 앵커 원칙:** 전압 스케일 1개·시간 스케일 1개만 도입(둘 다 감사 가능하게 인용). 나머지는 그
  앵커로부터 **유도**. 새 자유 상수 금지.
- **M0–M14 바이트 불변** 유지(가산-only), 회귀에 M15 불변량 추가, 결정성 2회 확인, 문서/버전 갱신,
  재패키징.
- M15 후보 절차는 `RESEARCH_PROGRAM_brainwave.md` §"v1.17 — M15 calibration bridge" 참조.

**그 다음 프런티어(여전히 OPEN, 정직):** `medium_efficacy_tested` 는 **외부 in-vivo 두개내 장-상쇄/증강
실험**이 있어야 0→1 이 될 수 있다. 하드 문제는 건드리지 않는다. 어떤 값도 날조로 채우지 않는다.

---

## 6. 반-드리프트 / 비-튜닝 체크 (매 편집 전 재확인)

1. **튜닝 금지.** 일치율은 **실제 창발 기전** 또는 **명명된 측정·인용 외부보정**으로만 올린다. 공차를
   절대 느슨하게 하지 않는다. **완전성보다 정직함.**
2. **측정값만 채점.** 각 관측값 = 측정현상(Hz/비율/관계사실) + 인용 + 공차. **해석은 채점하지 않는다.**
3. **단일 기질.** R19 쌍안정 + 측정 κ=0.5496 + atlas 주파수 재사용. **새 튜닝 상수 0개.**
4. **정직한 원장.** `medium_efficacy_tested=0`, `hard_problem_open=1`, `is_consciousness_claim=0`.
   사용자가 탐구를 "의식의 비밀"로 표현해도 — **수면 리듬의 재현은 의식·경험의 주장이 아니다.**
5. **바이트 보존.** 새 모듈은 기존 모듈 출력을 **per-module sha256 로 바이트 불변** 증명. BLAS 단일스레드
   고정(numpy import 전), SEED=19, float 10자리 반올림, JSON sort_keys → 2회 실행 동일 sha256.

---

## 7. 이번 세션 산출물

- `repro/mind/_engine/vp_mind_engine.py` — `emerge_sleep_architecture()` + `_m14_*` 헬퍼 추가
  (emerge_all·regression_scalars 배선). **기존 코드 수정 없음, 가산만.**
- `repro/mind/_engine/data/sleep_architecture_atlas.json` — 측정 시상수·관측값·인용·공차 (신규).
- `repro/mind/_verify/run_regression.py` — M14 검사 13개 추가 (62→75).
- `CHANGELOG.md` · `COMPLETION_LEDGER.md` · `MASTER_MANUAL_START_HERE.md` ·
  `RESEARCH_PROGRAM_brainwave.md` — v1.16 / 0.85 갱신.
- 동결: `expected_sha256.json`, `results/*.json` 재동결.
