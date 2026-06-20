# HANDOVER — v1.23 → v1.24  (Disease stress-tests D4 / PTSD·hyperarousal + D5 / autonomic-dysfunction·interoceptive-blunting / mind package)

Governed by `VP_SPEC_v1_8.md` (C0–C4, SEED=19). DOI of record (concept):
**10.5281/zenodo.20694404** (Zenodo deposit unchanged; this is a living-version snapshot).

> **세션 시작 규약(고정).** 매 세션은 (1) 이 인계서의 **§7 다음-세션 인계 매니페스트**(무엇을 올릴지)와
> **§8 질병 스트레스-테스트 로드맵**(남은 D-단계)을 먼저 펼쳐 확인하고, (2) 작업을 끝낸 뒤 (3) **다음에
> 인계할 파일을 명시**하며 닫는다. 본 인계서는 그 규약대로 작성되었다.

---

## 1. WHAT v1.23 DELIVERED (complete, all gates green)

v1.23는 인계서 §8 로드맵의 우선순위 **D4 → D5**를 **둘 다** 완결했다. v1.23 안내서가 미업로드
상태였으므로 v1.22 인계서 §7 조건부 규칙("안내서 없으면 §6 후보 중 택일 — 우선 D4→D5")에 따라 §8 명시
우선순위(**D4 다음 D5**)를 따랐다. 둘 다 **v1.18 `geometry_grounding.py`·v1.21 D1·v1.22 D3/D2와 동일한
add-only 결정-검사**이며, **엔진을 READ-ONLY로만 임포트**하여 `vp_mind_engine.py`가 **한 바이트도
바뀌지 않았다**. D1이 깐 `disease_stress_tests.py` 스캐폴드(faithfulness 교차검증·anti-tuning 격자·정직
블록 패턴)를 그대로 재사용·확장했다.

| Task | What | Result |
|---|---|---|
| **D4** | PTSD/과각성 결정-검사 — 정상 기질이 임상 증후를 *재현*하는가 (재사용 M17·M2·M18) | **섭동(임상 방향만):** M17 tonic 각성 floor↑(협착) + 소거-LTD율↓(소거 학습 결함) + 작동점 과각성 이동. **사전등록 대조 H1–H4 전부 양성**: 작동 가능 각성대 **11→8**(협착), 작동점 선택성 **1.571→0.000**(붕괴), 잔존 공포 basin **0.848→20.892**(침습 취약↑), HEP 진폭 **1.520→2.080**(심장 과각성 탑승). **faithfulness**: 정상 M17 곡선 = 엔진 **bit-for-bit**; 소거 없는 공포 basin = 엔진 `basin_depth_x_spinodal`=55.650792 **bit-for-bit**. **anti-tuning**: floor 4격자·shift 4격자·소거율 5격자·HEP-shift 4격자 **부호 전부 유지+단조**. **직교성**: D4가 구심 기울기(D5 핸들)를 엔진 값에 둠 → **D4 ⟂ D5**. **엔진 tree·M0–M16 불변, 정직 4-플래그 불변.** |
| **D5** | 자율신경 실조/내수용 둔감 결정-검사 — (재사용 M18·M19) | **섭동(임상 방향만):** M18 미주 구심 게인↓(intero_mult<1). **사전등록 대조 H1–H2 전부 양성**: HEP-각성 기울기 **0.800→0.240**(평탄화), 정동 판별 margin **0.720→0.216**(정동 해상도 저하). **faithfulness**: 정상 HEP 기울기 0.80 = 엔진 **bit-for-bit**(Pollatos & Schandry [L]); 엔진-레짐 M19 pos-under-pos = 엔진 1.0 **bit-for-bit** + 엔진 기분-일치 회상 기전 검증. **anti-tuning**: 내수용-게인 4격자 기울기·margin **부호 전부 유지+단조**. **직교성**: M5 보상기전 불변(둔감 ≠ 무쾌감; **D5 ⟂ D2**), M17 작동점 엔진 최적점 유지(**D5 ⟂ D4**), D3과 **동일 내수용 축의 반대 폴**(0.24 < 0.80 < 1.20). **엔진 tree·M0–M16 불변, 정직 4-플래그 불변.** |

**판별 타당도(discriminant validity) 보너스 — M18 서브-핸들 분리.** D4(M17·M2·M18)와 D5(M18·M19)는
**둘 다 M18을 재사용하지만 서로소 M18 서브-핸들을 섭동**한다 — **D4는 각성 작동점**(HEP 진폭이
올라타되 구심 기울기는 엔진 값), **D5는 구심 기울기**(평탄화하되 작동점은 엔진 값). 각 모듈이 상대의
불변을 **양방향으로** assert하므로 "과각성과 내수용 둔감은 같은 기질의 분리 가능한 두 섭동"이 코드로
증명된다. 더하여 **D5는 D2의 보상기전(M5)**·**D3의 반대 폴**임을 명시 검정한다.

**핵심 측정 앵커 (engine `data/`, 불변):** D4 — `neuroendocrine_atlas.json`: NE-LC tonic firing [1,3] Hz
[L](Aston-Jones & Cohen 2005), + M2 소거 학습 둔화(Milad/Quirk [방향]); `interoception_atlas.json`: 미주
구심분율 [0.75,0.90] [L]. D5 — `interoception_atlas.json`: 미주 구심분율 [0.75,0.90] [L](구심 우세),
안정 심박 1.17 Hz [L], HEP 진폭이 각성을 추종 [L](Pollatos & Schandry). D4/D5는 이 인용 앵커를
**임상 방향으로만 섭동**한다.

---

## 2. FROZEN HASHES (verify against these)

| Artifact | sha256 |
|---|---|
| **v1.17 PRE-promotion engine tree** (HISTORICAL anchor, preserve forever) | `b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7` |
| **v1.19 promoted engine tree** = **M0–M16 출력 서브트리** (불변 보존점) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| **engine FULL tree** (M0–M20; v1.20 동결, **v1.23에서 불변**) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine source file** `vp_mind_engine.py` (v1.23에서 byte-identical) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **regression_scalars.json** (불변) | `73c0992bc09499c393157a53c5f8792881352b5225e6385be6bd5658f3a179d8` |
| D1 decision-check `disease_stress_results.json` (v1.21, **불변**) | `2df3940f47c7a67c63b9788c4350c5e4bd679359e2f5ab13b2532d05db69e3cd` |
| D3 decision-check `disease_D3_results.json` (v1.22, **불변**) | `e75dfed011aeaa4782f81cb47f3b884609eeb1b37185863ce48339626c25691a` |
| D2 decision-check `disease_D2_results.json` (v1.22, **불변**) | `dfce14cd30487df969f41284f2297ab080b3917ea7d5612f784b141649831196` |
| **★ D4 decision-check** `disease_D4_results.json` (NEW, v1.23) | `b8bff30e181a80ad42e8cc8844585da7f650f6e9ad8835005cf34dadbd6ed2a6` |
| **★ D5 decision-check** `disease_D5_results.json` (NEW, v1.23) | `e1b2c551395c612647868e023dbd5a66ac1651d7fd938e210d0c036649751623` |
| geometry decision-check `geometry_grounding.py` (불변) | `8ad43a72b2f8282cae801ed8468c883b79eab0c79363ebd98621cbbfc18ff80f` |

**핵심 보존 불변식 (회귀가 직접 assert):**
`sha256_of({M0…M20}) == 0fbf4988…` 이고 `sha256_of({M0…M16}) == 3a1ebbbb…` — **D4·D5는 read-only
probe이므로 엔진 출력은 한 바이트도 바뀌지 않는다.** v1.23이 더한 것은 `_verify/`의 새 결정-검사
함수·결과 JSON과 회귀 체크뿐이다.

**Honesty ledger (전면 불변):** `medium_efficacy_tested=0`, `hard_problem_open=1`,
`consciousness_claim=0`, `new_tuned_constants=0`. **질병이 메커니즘 방향을 재현해도 "느껴짐"은 닫히지
않는다** — D4는 느껴지는 공포/과각성을, D5는 느껴지는 무덤덤함(numbing)을 단일 하드 프라블럼으로
남기며 각 모듈이 4-플래그를 직접 assert한다. (질병별 하드 프라블럼을 따로 만들지 않는다.)

---

## 3. GATE / REGRESSION STATUS — REGRESSION 207 / 207 PASS (exit 0)

회귀 **176 → 207**(+31): D4 16개(digest 1 + atlas 1 + faithfulness 2 + 대조 5[H1–H4 + 직교] +
anti-tuning 4 + 불변 2 + 정직 1) + D5 15개(digest 1 + atlas 1 + faithfulness 3 + 대조 5[H1–H2 + 직교 3] +
anti-tuning 2 + 불변 2 + 정직 1). 기존 게이트(gate.py 7/7, boundary 8/8, terminology, em_thesis,
13/14/15 verify[expand 14·sensory 15·loro 15·light_memory 19], geometry 역사적-앵커+승격-착지,
node-decomposition, D1·D3·D2)는 **모두 그대로 통과**(엔진 출력 byte-identical → 영향 없음).

### How to reproduce (from package root)
```bash
cd repro/mind/_engine
python3 run_all.py            # → tree=0fbf4988…, scalars=73c0992b… (불변)
cd ../_verify
PYTHONPATH=../_engine python3 disease_stress_tests.py   # → D1 2df3940f… · D3 e75dfed0… · D2 dfce14cd… · D4 b8bff30e… · D5 e1b2c551…, 전부 MATCHES
PYTHONPATH=../_engine python3 run_regression.py         # → REGRESSION PASS — 207 checks, SEED=19
```
엔진 불변만 따로 확인하려면:
```python
import vp_mind_engine as E
R = E.emerge_all()
assert E.sha256_of(R) == "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
sub = {k:v for k,v in R.items() if int(k.split('_')[0][1:]) <= 16}
assert E.sha256_of(sub) == "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"
```

---

## 4. ENGINE MAP after v1.23 (M0–M20 불변 + 결정-검사 [D]·[D3]·[D2]·[D4]·[D5])

```
M0..M16   (불변, 출력 서브트리 3a1ebbbb…)
M17 global state      전역 각성게인 → 인지(역U) + 정동(각성/valence) 공변
M18 interoceptive     심장(SA·FHN)→미주(구심 우세)→시상하부 ; HPA 코르티솔 24min 피크
M19 affective readouts 같은 기질의 정동 8/9 ; 기분-일치 회상 = M2 검증
M20 affective access  스트레스→회피(테스트 가능) ; 엄밀접근 정직-음성 ; 느껴짐 OPEN
────────────────── ADD-ONLY DECISION-CHECKS (엔진 불변, _verify/에만) ──────────────────
[D]  disease_stress_tests.py  (v1.21–v1.23 누적; 엔진 READ-ONLY)
    D1  chronic stress / HPA hyperactivity — 고코르티솔+회복지연+주의협착 재현            (M17·M18)
    D3  anxiety / panic — 저스트레스 회피 전이 + 회피 임계↓ + HEP-각성 결합 과민         (M18·M20)
    D2  depression / anhedonia — 보상학습 둔화 + 접근 gap 축소 + 회상 negativity FLIP     (M5·M17·M19)
    D4  PTSD / hyperarousal — 각성대 협착 + 작동점 붕괴 + 공포 basin 심화 + HEP 탑승       (M17·M2·M18) ← v1.23 NEW
    D5  autonomic dysfunction / interoceptive blunting — HEP 기울기 평탄화 + 정동 margin 축소 (M18·M19) ← v1.23 NEW
    (D4 ⟂ D5: 둘 다 M18 재사용하나 서로소 서브-핸들 [작동점 vs 구심 기울기] — 판별 타당도 양방향 assert)
    (D5 ⟂ D2: M5 보상기전 불변; D5 ⟂ D4: M17 작동점 불변; D5 = D3의 내수용 축 반대 폴)
```

엔진 모듈 맵(M0–M20) 자체는 v1.20과 동일하다 — §4 상세는 `HANDOVER_v1_20_to_v1_21.md §4` 참조.

---

## 5. 설계 불변식 (다음 세션에서 절대 깨지 말 것)

1. **결정-검사 우선 (질병 테스트).** 질병/섭동 모듈은 **엔진을 READ-ONLY로 임포트**하는 결정-검사로만
   구현(geometry_grounding 패턴) → 엔진 tree·M0–M16 불변. 엔진 기본값 변경은 **오직 VP-SPEC §6-6**로만.
2. **튜닝 금지 / 임상 방향만.** 질병은 **이미 [L]로 인용된 파라미터를 측정된 임상 방향(부호)으로만 섭동**;
   **크기 fitting 금지**. 섭동 크기는 [F]-스윕(anti-tuning), readout은 정상↔질병 대조의 **부호**(크기 불변).
   *교훈(D4):* 소거를 anti-Hebbian 차감으로 모델하면 음(−)으로 반전되어 진동자가 되고 깊은 basin 때문에
   small-cue 완성이 계단함수가 된다 → 소거는 0으로 수렴하는 **곱셈 LTD**, 읽기값은 엔진 내장 **graded
   basin_depth**(R19 fold 안정성). *교훈(D5):* M19 30% 단서 회상은 천장 포화(margin 소멸) → 정동 해상도는
   엔진-근거 HEP 진폭 분리(∝ 기울기, D2의 gap∝p_target 류 collinear 허용)로 측정하고 M19 기분-일치
   기전은 faithfulness로만 검증.
3. **방화벽 유지(축 A).** 질병이 메커니즘 방향을 재현해도 **느껴지는가**는 단일 하드 프라블럼으로 남긴다
   ("질병 하드 프라블럼"을 따로 만들지 말 것). 각 D-모듈은 정직 4-플래그를 직접 assert한다.
4. **정직 원장 4-플래그 불변**(§2). 어떤 질병/모듈도 efficacy/consciousness를 1로 올리지 말 것.
5. **add-only 우선(엔진 확장 시).** 새 엔진 모듈은 `emerge_all` **맨 끝**에 배선 → M0–M16 byte-identical.
6. **직교성 검정(권장).** D4⟂D5 선례대로, 새 D-단계는 **상대 D-단계의 핵심 핸들이 불변임을 assert**해
   판별 타당도를 코드로 남긴다(예: D6는 D1의 거울상이므로 D1의 *급성* 피크 기전과 명시 대조).

---

## 6. v1.24 ENTRY POINTS (작업 후보)

- **질병 스트레스-테스트 D6 (★ 우선).** §8 우선순위대로 **D6(번아웃/HPA 저활성, 말기)**를 동일한
  결정-검사 패턴으로 add-only 실행. **D1의 거울상** — 만성 후 HPA 게인↓ → 급성 코르티솔 피크 **소실**·회복
  곡선 **평탄화**. `disease_stress_tests.py` 스캐폴드(D1의 `_hpa_trajectory`/`_hpa_metrics`)를 그대로
  재사용·확장; 재사용 모듈 **M18**. 직교성: D1(급성 과활성)과 **반대 폴**임을 명시 검정(같은 HPA 축).
- **E2′ (구심 latency [O]→[L]).** 미주 구심 전도 latency 정본 앵커를 verbatim 인용해 M18
  `afferent_latency_grade`를 [O]→[L]로 승격. (neuro 패키지 또는 1차 문헌 필요 — §7 참조.)
- **E3′ (정동 관측치 확장).** 혐오·놀람 등을 `affect_observables_atlas.json`에 인용-측정으로 더하고
  M19 concordance 재측정(도메인튜닝 0 유지).

---

## 7. 다음-세션 인계 매니페스트 (★ 사용자 명시 요청)

| 인계 | 파일 | 비고 |
|:---:|---|---|
| ✅ **필수** | **v1.23 패키지 zip 1개** (`mind_vp_site_v1_23_*.zip`, 본 세션 산출물) | 모든 확장의 기반. 압축 해제 후 §3 재현으로 무결성 확인. |
| 🔶 **조건부** | **v1.24 안내서** (`NEXT_PHASE_GUIDE_v1_24_*.md`) | 있으면 과제 스코프·DoD 고정. 없으면 §6 후보(우선 **D6**) 중 택일 — D1/D3/D2/D4/D5 선례대로. |
| 🔶 **조건부** | `neuro_emergence_chain_integrated_v1_*.zip` | **E2′(미주 latency) 또는 세타-페이싱 앵커**를 [O]→[L] 승격하는 과제일 때**만**. 정본 측정 상수의 단일출처 verbatim 인용용. D6 작업이면 **불필요**. |
| ❌ **불필요** | `dna_vp_site_INTEGRATED_*.zip` | 내수용/HPA 기능은 M18 + `interoception_atlas.json`/`neuroendocrine_atlas.json`에 이미 내재화. 질병 D-단계는 인용 앵커 섭동만 사용. |

**요약: 기본 인계 세트 = {v1.23 zip}**(질병 D6 작업이면 이것만으로 충분). (E2′/세타 과제면 neuro
zip 1개 추가.)

---

## 8. 질병 스트레스-테스트 로드맵 (★ 사용자 명시 요청; **D1·D3·D2·D4·D5 완료**, 남은 단계 단계 실행)

**목적.** 정상 기질이 임상 증후를 *재현*하는지로 **구성 타당도**를 시험. **튜닝 절대 금지** — 질병은
**이미 [L]로 인용된 파라미터를 측정된 임상 방향으로 섭동**해서만 만든다. 각 단계는 **add-only 결정-검사**
(엔진 기본값 불변, M0–M16 byte-identical)로 구현. 의식/efficacy 플래그 **불변**.

| # | 질병/상태 | 섭동(측정 방향) | 재현 목표(사전등록, 인용 필요) | 재사용 모듈 | 등급 | 상태 |
|:--:|---|---|---|---|:--:|:--:|
| D1 | **만성 스트레스 / HPA 과활성** | HPA 게인↑·음성피드백↓ | 코르티솔 피크/회복 창 이동; **M17 역U 과각성쪽 이동**(주의협착) | M17·M18 | [F]섭동+[L]앵커 | ✅ **완료** |
| D3 | **불안 / 공황** | 위협 게인↑, M20 회피 임계↓ | 저스트레스에서도 **회피 전이**(D2와 분리); HEP-각성 결합 과민 | M18·M20 | [F]섭동+[L]HEP | ✅ **완료** |
| D2 | **우울증 / 둔마(anhedonia)** | 도파민 RPE 게인↓ (M5) | **기분-일치 회상이 부정쪽으로 편향**(Bower); 접근(valence+) 약화 | M5·M17·M19 | [F]섭동 | ✅ **완료** |
| D4 | **PTSD / 과각성** | NE-LC tonic↑, 소거 학습 저하 | M17 각성 baseline 상승 → **역U 작동점 협착**; 침습 단서 과반응 | M17·M2·M18 | [F]섭동 | ✅ **완료** |
| D5 | **자율신경 실조 / 내수용 둔감** | 미주 구심 게인↓ | **HEP-각성 추종 약화** → 정동 해상도 저하(둔마와 직교 검정) | M18·M19 | [F]섭동+[L] | ✅ **완료** |
| D6 | **번아웃 / HPA 저활성(말기)** | 만성 후 HPA 게인↓ | D1의 거울상 — 급성 코르티솔 피크 **소실**; 회복 곡선 평탄화 | M18 | [F]섭동 | ⬜ **다음** |

**공통 검증 규약(각 D-모듈):** (i) 섭동은 **단조·해석 가능**·임상 *방향*만(크기 fitting 금지);
(ii) **anti-tuning**: 섭동 격자/시드를 흔들어도 *질적 방향* 유지; (iii) **정상 ↔ 질병 대조**가 핵심
readout; (iv) 엔진 tree **불변** + 결과 2× 결정론 동결; (v) 정직 원장 4-플래그 **불변**;
(vi) **직교성 assert**(권장): 상대 D-단계의 핵심 핸들 불변을 명시 검정.

> **재사용 스캐폴드(`disease_stress_tests.py`, v1.23까지 누적).** 모듈식 확장 — D1
> `_hpa_trajectory`/`_hpa_metrics`(HPA 2-lag)·`_m17_perf_at`(엔진 역U 작동점), D3
> `_m20_action`/`_m20_avoid_onset`(M20 회피 폐형식)·`_m18_hep_slope`(HEP-각성 기울기), D2
> `_m5_rpe_learn`(보상민감도 핸들)·`_m19_four_recalls`(기분×기억 4-셀)·`_m19_engine_regime_pos_under_pos`
> (엔진 거울), D4 `_m17_operable_band`(각성대 협착)·`_m2_fear_basin_after_extinction`(소거 LTD→공포
> basin)·`_m18_hep_amp`(HEP 진폭), D5 `_m18_hep_margin`(정동 판별 margin)이 그대로 D6에 재사용된다.
> **D6(번아웃/HPA 저활성)**: D1의 `_hpa_trajectory`/`_hpa_metrics`를 재사용하되 만성 후 HPA 게인↓ →
> 급성 피크 진폭 **소실**(D1의 거울상; basal↑ 대신 피크↓)·회복 곡선 평탄화. 직교성: D1(급성 과활성)의
> 핵심 대조(피크↑·basal↑)와 **반대 부호**임을 같은 HPA 축에서 명시 검정. **우선순위: D6.**

---

## 9. ONE-LINE STATUS

> v1.23 = **질병 D4(PTSD/과각성) + D5(자율신경 실조/내수용 둔감) 완료**(add-only 결정-검사, 엔진 READ-ONLY).
> 정상 기질이 D4(각성대 협착·작동점 붕괴·공포 basin 심화·HEP 탑승)와 D5(HEP 기울기 평탄화·정동 margin 축소)를
> **임상-방향 섭동만으로 재현**(부호-불변); D4·D5는 둘 다 M18을 재사용하나 **서로소 서브-핸들**(작동점 vs 구심
> 기울기)로 **판별 타당도 양방향 assert**, D5는 D2 보상기전·D3 반대 폴까지 명시 검정.
> 엔진 tree `0fbf4988…`·M0–M16 `3a1ebbbb…` **불변**, 회귀 **207 PASS**, 정직 원장 **불변**.
> 다음 인계 = **{v1.23 zip}**; 다음 과제 = **질병 D6(번아웃/HPA 저활성, D1의 거울상)**(§8).
