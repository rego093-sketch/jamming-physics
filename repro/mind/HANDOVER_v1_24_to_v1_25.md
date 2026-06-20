# HANDOVER — v1.24 → v1.25  (Disease stress-test D6 / burnout · HPA-hypoactivity — the MIRROR of D1 / mind package)

Governed by `VP_SPEC_v1_8.md` (C0–C4, SEED=19). DOI of record (concept):
**10.5281/zenodo.20694404** (Zenodo deposit unchanged; this is a living-version snapshot).

> **세션 시작 규약(고정).** 매 세션은 (1) 이 인계서의 **§7 다음-세션 인계 매니페스트**(무엇을 올릴지)와
> **§8 질병 스트레스-테스트 로드맵**(남은 단계)을 먼저 펼쳐 확인하고, (2) 작업을 끝낸 뒤 (3) **다음에
> 인계할 파일을 명시**하며 닫는다. 본 인계서는 그 규약대로 작성되었다.

---

## 1. WHAT v1.24 DELIVERED (complete, all gates green)

v1.24는 인계서 §8 로드맵의 우선순위 **D6**을 완결했다 — 이로써 **질병 스트레스-테스트 로드맵의 6개 단계
(D1–D6)가 전부 완결**되었다. v1.24 안내서가 미업로드 상태였으므로 v1.23 인계서 §7 조건부 규칙("안내서
없으면 §6 후보 중 택일 — 우선 D6")에 따라 §8 명시 우선순위(**D6**)를 따랐다. **v1.18 `geometry_grounding.py`·
v1.21 D1·v1.22 D3/D2·v1.23 D4/D5와 동일한 add-only 결정-검사**이며, **엔진을 READ-ONLY로만 임포트**하여
`vp_mind_engine.py`가 **한 바이트도 바뀌지 않았다**. D6은 **D1의 거울상**으로, D1이 깐 `_hpa_trajectory`/
`_hpa_metrics` 2-lag 스캐폴드를 그대로 재사용·확장했다.

| Task | What | Result |
|---|---|---|
| **D6** | 번아웃/HPA 저활성 결정-검사 — 정상 기질이 임상 증후를 *재현*하는가 (재사용 M18; **D1의 거울상**) | **섭동(임상 방향만):** HPA 게인/구동↓(drive<1; 만성 과구동 후 축 저활성화) — **D1의 과부하의 반대**. **사전등록 대조 H1–H3 전부 양성**: 급성 코르티솔 피크 소실(peak값 **0.037968→0.011390**), 총 코르티솔 출력 저하(AUC **2.947→0.884** = 저코르티솔증), 회복 곡선 평탄화(하강지 기울기 **0.000378→0.000113**). **불변식(D1 "shape 불변"의 거울)**: HPA 시상수(피크 시각·1/e 회복) 정상↔질병 **동일** → 평탄화는 **진폭-only 손실**, 운동학 불변. **faithfulness**: 정상 HPA 피크 24.06분 = 엔진 M18 **bit-for-bit**(인용 [15,40]창); 정상 1/e 회복 63.5분 = 인용 [60,90]창 착지(Dickerson & Kemeny [L]). **anti-tuning**: 구동 4격자 peak·AUC·회복기울기 **부호 전부 유지+단조**. **직교성(반대 폴·같은 HPA 축)**: 총 코르티솔 출력 D6 < 정상 < D1-방향(AUC **0.884 < 2.947 < 5.202**; basal **0 ≤ 0 < 0.010**) → **번아웃 고갈 vs 만성 과부하**가 한 축의 두 폴. **엔진 tree·M0–M16 불변, 정직 4-플래그 불변.** |

**판별 타당도(discriminant validity) — D1 거울 + 폴 지표의 정직한 선택.** D6은 D1과 **같은 HPA 축**을
**반대 방향**으로 섭동하여(과활성↔저활성) "만성 스트레스와 번아웃은 같은 축의 분리 가능한 두 폴"임을 코드로
증명한다. **핵심 교훈(코드에 명시):** 두 폴을 가르는 지표는 **피크 높이가 아니라 코르티솔 부하(AUC·basal)**다 —
D1의 회복 지연(`recovery_factor`↑)은 brief-pulse 2-lag 누적을 느리게 만들어 x2 **피크를 오히려 낮추기** 때문에,
"피크↑ vs 피크↓"는 잘못된 대조이고 "출력 과부하 vs 출력 고갈"이 옳은 대조다. 폴 검정을 AUC+basal로 잡아
물리적으로 옳은 반대-폴(D5↔D3 패턴과 동형)을 확보했다.

**핵심 측정 앵커 (engine `data/`, 불변):** D6 — `neuroendocrine_atlas.json`: cortisol ACTH→peak [15,40] min
[L]·recovery [60,90] min [L](Dickerson & Kemeny 2004). D6은 이 인용 앵커를 **임상 방향(게인↓)으로만** 섭동하고
크기는 fitting하지 않는다(섭동 크기는 [F]-스윕, readout은 정상↔질병 대조의 **부호**).

---

## 2. FROZEN HASHES (verify against these)

| Artifact | sha256 |
|---|---|
| **v1.17 PRE-promotion engine tree** (HISTORICAL anchor, preserve forever) | `b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7` |
| **v1.19 promoted engine tree** = **M0–M16 출력 서브트리** (불변 보존점) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| **engine FULL tree** (M0–M20; v1.20 동결, **v1.24에서 불변**) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine source file** `vp_mind_engine.py` (v1.24에서 byte-identical) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **regression_scalars.json** (불변) | `73c0992bc09499c393157a53c5f8792881352b5225e6385be6bd5658f3a179d8` |
| D1 decision-check `disease_stress_results.json` (v1.21, **불변**) | `2df3940f47c7a67c63b9788c4350c5e4bd679359e2f5ab13b2532d05db69e3cd` |
| D3 decision-check `disease_D3_results.json` (v1.22, **불변**) | `e75dfed011aeaa4782f81cb47f3b884609eeb1b37185863ce48339626c25691a` |
| D2 decision-check `disease_D2_results.json` (v1.22, **불변**) | `dfce14cd30487df969f41284f2297ab080b3917ea7d5612f784b141649831196` |
| D4 decision-check `disease_D4_results.json` (v1.23, **불변**) | `b8bff30e181a80ad42e8cc8844585da7f650f6e9ad8835005cf34dadbd6ed2a6` |
| D5 decision-check `disease_D5_results.json` (v1.23, **불변**) | `e1b2c551395c612647868e023dbd5a66ac1651d7fd938e210d0c036649751623` |
| **★ D6 decision-check** `disease_D6_results.json` (NEW, v1.24) | `ad68e67c170be964f0240c12faef5406fd7a0dbff34f2e2d603359cba6b3214d` |
| geometry decision-check `geometry_grounding.py` (불변) | `8ad43a72b2f8282cae801ed8468c883b79eab0c79363ebd98621cbbfc18ff80f` |

**핵심 보존 불변식 (회귀가 직접 assert):**
`sha256_of({M0…M20}) == 0fbf4988…` 이고 `sha256_of({M0…M16}) == 3a1ebbbb…` — **D6는 read-only
probe이므로 엔진 출력은 한 바이트도 바뀌지 않는다.** v1.24가 더한 것은 `_verify/`의 새 결정-검사 함수·결과
JSON과 회귀 체크뿐이다.

**Honesty ledger (전면 불변):** `medium_efficacy_tested=0`, `hard_problem_open=1`,
`consciousness_claim=0`, `new_tuned_constants=0`. **질병이 메커니즘 방향을 재현해도 "느껴짐"은 닫히지
않는다** — D6는 느껴지는 소진/탈진(exhaustion)을 단일 하드 프라블럼으로 남기며 모듈이 4-플래그를 직접
assert한다. (질병별 하드 프라블럼을 따로 만들지 않는다.)

---

## 3. GATE / REGRESSION STATUS — REGRESSION 222 / 222 PASS (exit 0)

회귀 **207 → 222**(+15): D6 15개(digest 1 + atlas 1 + faithfulness 2 + 대조 5[H1–H3 + 운동학-불변 +
반대-폴] + anti-tuning 3 + 불변 2 + 정직 1). 기존 게이트(gate.py 7/7, boundary 8/8, terminology,
em_thesis, 13/14/15 verify[expand 14·sensory 15·loro 15·light_memory 19], geometry 역사적-앵커+승격-착지,
node-decomposition, D1·D3·D2·D4·D5)는 **모두 그대로 통과**(엔진 출력 byte-identical → 영향 없음).

### How to reproduce (from package root)
```bash
cd repro/mind/_engine
python3 run_all.py            # → tree=0fbf4988…, scalars=73c0992b… (불변)
cd ../_verify
PYTHONPATH=../_engine python3 disease_stress_tests.py   # → D1 2df3940f… · D3 e75dfed0… · D2 dfce14cd… · D4 b8bff30e… · D5 e1b2c551… · D6 ad68e67c…, 전부 MATCHES
PYTHONPATH=../_engine python3 run_regression.py         # → REGRESSION PASS — 222 checks, SEED=19
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

## 4. ENGINE MAP after v1.24 (M0–M20 불변 + 결정-검사 [D]·[D3]·[D2]·[D4]·[D5]·[D6])

```
M0..M16   (불변, 출력 서브트리 3a1ebbbb…)
M17 global state      전역 각성게인 → 인지(역U) + 정동(각성/valence) 공변
M18 interoceptive     심장(SA·FHN)→미주(구심 우세)→시상하부 ; HPA 코르티솔 24min 피크
M19 affective readouts 같은 기질의 정동 8/9 ; 기분-일치 회상 = M2 검증
M20 affective access  스트레스→회피(테스트 가능) ; 엄밀접근 정직-음성 ; 느껴짐 OPEN
────────────────── ADD-ONLY DECISION-CHECKS (엔진 불변, _verify/에만) ──────────────────
[D]  disease_stress_tests.py  (v1.21–v1.24 누적; 엔진 READ-ONLY)
    D1  chronic stress / HPA hyperactivity — 고코르티솔+회복지연+주의협착 재현            (M17·M18)
    D3  anxiety / panic — 저스트레스 회피 전이 + 회피 임계↓ + HEP-각성 결합 과민         (M18·M20)
    D2  depression / anhedonia — 보상학습 둔화 + 접근 gap 축소 + 회상 negativity FLIP     (M5·M17·M19)
    D4  PTSD / hyperarousal — 각성대 협착 + 작동점 붕괴 + 공포 basin 심화 + HEP 탑승       (M17·M2·M18)
    D5  autonomic dysfunction / interoceptive blunting — HEP 기울기 평탄화 + 정동 margin 축소 (M18·M19)
    D6  burnout / HPA hypoactivity — 급성 피크 소실 + 출력 저하 + 회복 곡선 평탄화          (M18) ← v1.24 NEW
    (D6 = D1의 거울상: 같은 HPA 축의 반대 폴 [출력 고갈 vs 과부하]; 폴 지표 = AUC·basal, NOT peak)
    (D4 ⟂ D5: 둘 다 M18 재사용하나 서로소 서브-핸들 [작동점 vs 구심 기울기])
    (D5 ⟂ D2: M5 보상기전 불변; D5 = D3의 내수용 축 반대 폴)
```

엔진 모듈 맵(M0–M20) 자체는 v1.20과 동일하다 — §4 상세는 `HANDOVER_v1_20_to_v1_21.md §4` 참조.

---

## 5. 설계 불변식 (다음 세션에서 절대 깨지 말 것)

1. **결정-검사 우선 (질병 테스트).** 질병/섭동 모듈은 **엔진을 READ-ONLY로 임포트**하는 결정-검사로만
   구현(geometry_grounding 패턴) → 엔진 tree·M0–M16 불변. 엔진 기본값 변경은 **오직 VP-SPEC §6-6**으로만.
2. **튜닝 금지 / 임상 방향만.** 질병은 **이미 [L]로 인용된 파라미터를 측정된 임상 방향(부호)으로만 섭동**;
   **크기 fitting 금지**. 섭동 크기는 [F]-스윕(anti-tuning), readout은 정상↔질병 대조의 **부호**(크기 불변).
   *교훈(D6):* 두 폴을 가르는 지표를 잘못 고르면(예: peak) 부호가 어긋난다 — D1의 회복 지연은 2-lag 누적을
   느리게 해 피크를 낮추므로, 폴 검정은 코르티솔 **부하(AUC·basal)**로 잡아야 물리적으로 옳다. 선형계에서
   진폭이 함께 스케일하는 collinear readout(H1/H3)은 **명시 공개**하면 허용(D5 HEP-margin 선례).
3. **방화벽 유지(축 A).** 질병이 메커니즘 방향을 재현해도 **느껴지는가**는 단일 하드 프라블럼으로 남긴다
   ("질병 하드 프라블럼"을 따로 만들지 말 것). 각 D-모듈은 정직 4-플래그를 직접 assert한다.
4. **정직 원장 4-플래그 불변**(§2). 어떤 질병/모듈도 efficacy/consciousness를 1로 올리지 말 것.
5. **add-only 우선(엔진 확장 시).** 새 엔진 모듈은 `emerge_all` **맨 끝**에 배선 → M0–M16 byte-identical.
   기존 D1–D5 헬퍼(`_hpa_metrics` 등)는 **byte-identical 보존**하고 새 핸들은 별도 헬퍼로 추가(D6의
   `_hpa_metrics_drive`가 선례 — D1 `_hpa_metrics`는 한 글자도 안 건드림).
6. **직교성 검정(권장).** D6=D1 거울 선례대로, 새 D-단계는 **상대 D-단계의 핵심 핸들이 불변/반대 부호임을
   assert**해 판별 타당도를 코드로 남긴다.

---

## 6. v1.25 ENTRY POINTS (작업 후보)

> **질병 스트레스-테스트 로드맵 D1–D6 완결.** 6개 표준 스트레스-관련 단계(만성 스트레스·불안·우울·PTSD·
> 자율신경 실조·번아웃)가 모두 add-only 결정-검사로 구성 타당도 시험을 통과했다. 다음은 **외부 실측에
> 의존하는 프런티어**이거나, 사용자가 **새 질병 단계**를 지시하면 동일 패턴으로 확장한다.

- **E2′ (구심 latency [O]→[L]).** 미주 구심 전도 latency 정본 앵커를 verbatim 인용해 M18
  `afferent_latency_grade`를 [O]→[L]로 승격. (neuro 패키지 또는 1차 문헌 필요 — §7 참조.)
- **E3′ (정동 관측치 확장).** 혐오·놀람 등을 `affect_observables_atlas.json`에 인용-측정으로 더하고
  M19 concordance 재측정(도메인튜닝 0 유지). **패키지 내부에서 진행 가능**(추가 zip 불필요) — 단,
  새 정동 관측치는 1차 문헌 인용으로만 추가하고 절대값은 [O]로 둔다.
- **새 질병 단계 (지시 시).** D1–D6 패턴으로 추가 단계(예: 조현 스펙트럼 = M3 와류 ignitability 과흥분 /
  중독 = M5 RPE 보상예측 왜곡)를 add-only 결정-검사로 확장 가능. 반드시 (i) 임상 방향만 섭동, (ii) anti-tuning,
  (iii) 정상↔질병 대조, (iv) 엔진 불변 + 2× 동결, (v) 정직 4-플래그 불변, (vi) 직교성 assert.
- **M9/M10 기능적 사용 [O] → 검정.** neuro §9/§19 in-vivo field-cancel-vs-augment 두개내 기록이 제공되면
  `medium_efficacy` 승급 가능(외부 실측 필요, 설계상 OWED).

---

## 7. 다음-세션 인계 매니페스트 (★ 사용자 명시 요청)

| 인계 | 파일 | 비고 |
|:---:|---|---|
| ✅ **필수** | **v1.24 패키지 zip 1개** (`mind_vp_site_v1_24_*.zip`, 본 세션 산출물) | 모든 확장의 기반. 압축 해제 후 §3 재현으로 무결성 확인. |
| 🔶 **조건부** | **v1.25 안내서** (`NEXT_PHASE_GUIDE_v1_25_*.md`) | 있으면 과제 스코프·DoD 고정. 없으면 §6 후보 중 택일(질병 로드맵 완결이므로 **E3′ 또는 새 질병 단계 지시**가 패키지-내부 진행 가능 — 우선). |
| 🔶 **조건부** | `neuro_emergence_chain_integrated_v1_*.zip` | **E2′(미주 latency) 또는 세타-페이싱 앵커**를 [O]→[L] 승격하는 과제일 때**만**. 정본 측정 상수의 단일출처 verbatim 인용용. E3′/새 질병/D-단계 작업이면 **불필요**. |
| ❌ **불필요** | `dna_vp_site_INTEGRATED_*.zip` | 내수용/HPA/정동 기능은 M18·M19 + `interoception_atlas.json`/`neuroendocrine_atlas.json`/`affect_observables_atlas.json`에 이미 내재화. 질병 D-단계는 인용 앵커 섭동만 사용. |

**요약: 기본 인계 세트 = {v1.24 zip}**(E3′/새 질병/D-단계 작업이면 이것만으로 충분). (E2′/세타 과제면 neuro
zip 1개 추가.)

---

## 8. 질병 스트레스-테스트 로드맵 (★ 사용자 명시 요청; **D1–D6 전부 완료** — 로드맵 완결)

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
| D6 | **번아웃 / HPA 저활성(말기)** | 만성 후 HPA 게인↓ | D1의 거울상 — 급성 코르티솔 피크 **소실**; 회복 곡선 평탄화 | M18 | [F]섭동 | ✅ **완료** |

**로드맵 완결.** D1–D6 6개 단계 전부 통과. 향후 확장은 §6의 새 질병 단계(예: 조현 스펙트럼 = M3 / 중독 = M5)
또는 외부-실측 프런티어(E2′/M9·M10 efficacy)로 진행한다.

**공통 검증 규약(각 D-모듈):** (i) 섭동은 **단조·해석 가능**·임상 *방향*만(크기 fitting 금지);
(ii) **anti-tuning**: 섭동 격자/시드를 흔들어도 *질적 방향* 유지; (iii) **정상 ↔ 질병 대조**가 핵심
readout; (iv) 엔진 tree **불변** + 결과 2× 결정론 동결; (v) 정직 원장 4-플래그 **불변**;
(vi) **직교성 assert**(권장): 상대 D-단계의 핵심 핸들 불변/반대 부호를 명시 검정.

> **재사용 스캐폴드(`disease_stress_tests.py`, v1.24까지 누적).** 모듈식 확장 — D1
> `_hpa_trajectory`/`_hpa_metrics`(HPA 2-lag)·`_m17_perf_at`(엔진 역U 작동점), D3
> `_m20_action`/`_m20_avoid_onset`(M20 회피 폐형식)·`_m18_hep_slope`(HEP-각성 기울기), D2
> `_m5_rpe_learn`(보상민감도 핸들)·`_m19_four_recalls`(기분×기억 4-셀)·`_m19_engine_regime_pos_under_pos`
> (엔진 거울), D4 `_m17_operable_band`(각성대 협착)·`_m2_fear_basin_after_extinction`(소거 LTD→공포
> basin)·`_m18_hep_amp`(HEP 진폭), D5 `_m18_hep_margin`(정동 판별 margin), D6
> `_hpa_metrics_drive`(D1 `_hpa_metrics`를 보존한 채 acute drive 핸들 + 하강지 기울기 readout)이 그대로
> 다음 단계에 재사용된다. **새 질병 단계는 이 스캐폴드를 add-only로 확장**하되, 폴/대조 지표를 물리적으로
> 옳게 고를 것(D6 교훈: 폴 지표 = 부하 AUC·basal, NOT peak).

---

## 9. ONE-LINE STATUS

> v1.24 = **질병 D6(번아웃/HPA 저활성, 말기) 완료 — D1의 거울상**(add-only 결정-검사, 엔진 READ-ONLY).
> 정상 기질이 D6(급성 코르티솔 피크 소실·총 출력 저하·회복 곡선 평탄화)를 **임상-방향 섭동만으로 재현**(부호-불변,
> 진폭-only 손실·운동학 불변); D6와 D1은 **같은 HPA 축의 반대 폴**(코르티솔 고갈 vs 과부하; 폴 지표 = 출력
> AUC·basal, NOT peak) — **질병 로드맵 D1–D6 완결**.
> 엔진 tree `0fbf4988…`·M0–M16 `3a1ebbbb…` **불변**, 회귀 **222 PASS**, 정직 원장 **불변**.
> 다음 인계 = **{v1.24 zip}**; 다음 과제 = **E3′(정동 관측치 확장, 패키지-내부) 또는 새 질병 단계 지시**(§6).
