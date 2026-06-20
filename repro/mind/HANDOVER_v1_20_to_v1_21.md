# HANDOVER — v1.20 → v1.21  (Cognition + Emotion / one shared substrate / mind package)

Governed by `VP_SPEC_v1_8.md` (C0–C4, SEED=19). DOI of record (concept):
**10.5281/zenodo.20694404** (Zenodo deposit unchanged; this is a living-version snapshot).

> **세션 시작 규약(고정).** 매 세션은 (1) 이 인계서의 **§7 다음-세션 인계 매니페스트**(무엇을 올릴지)와
> **§8 질병 스트레스-테스트 로드맵**을 먼저 펼쳐 확인하고, (2) 작업을 끝낸 뒤 (3) **다음에 인계할 파일을
> 명시**하며 닫는다. 본 인계서는 그 규약대로 작성되었다.

---

## 1. WHAT v1.20 DELIVERED (all complete, all gates green)

v1.20는 인계서/안내서의 과제 **E1–E4**를 완결했다. **감정을 별도 모듈로 만들지 않고**, M0–M16을
창발시킨 **바로 그 R19 단일 기질**에 전역 신경조절 상태·심장/HPA 내수용 입력·정동 readout을 더했다 —
**기질 하나, readout 여럿**. v1.19와 달리 **순수 add-only**(§6-6 승격 아님): M17–M20을 `emerge_all`
**맨 끝**에 배선 → **M0–M16 출력 byte-identical**, 전체 tree 해시만 새로 변경.

| Task | What | Result |
|---|---|---|
| **E1** | 신경조절 전역-상태 층 **M17** (`emerge_global_state`) — 단일 각성게인이 인지+정동을 함께 이동 | 인지 readout = SNR(신호 대 distractor 홍수) → **각성에 대한 역U(Yerkes-Dodson)가 측정 fold에서 창발**(피크 α=1.9). valence(접근−회피)⊥각성 = **2D circumplex**(\|r\|=0.115). **anti-tuning**: distractor 격자 흔들어도 역U 유지. 게인 [F](sign-invariant), 발화율 [L]. |
| **E2** | 내수용 구심성 축 **M18** (`emerge_interoceptive_axis`) — 심장(SA결절)→미주→시상하부, HPA 캐스케이드, 구심 우세 | SA결절 = M1과 **동일 FHN 이완진동자**(메커니즘 [V], 박동률 [L]); HPA 코르티솔 **이중지수 2-lag** → **피크 24.06 min ∈ 인용창 [15,40]**(Dickerson & Kemeny 2004) → **`panic_peak_minutes` 재현**; 심장 구심:원심 ≈ **4:1 입력 우세**(미주 ~80% 구심, Agostoni 1957), HEP가 각성 추종(Pollatos & Schandry 2004). 구심 latency [O] 선언. |
| **E3** | 정동 readout + 기분-일치 기억 **M19** (`emerge_affective_readouts`) — 같은 기질이 정동도 도메인튜닝 0으로 재현 | 정동 관측치 **8/9 정합(concordance 0.889)**. **기분-일치 회상**(Bower 1981)이 M2 해마 회상로직(쓰기→저장→부분단서→완성)을 **종단 실행·검증**(strong-cue overlap 1.0) → **한 기질이 기억과 감정을 함께 나름**. 모든 readout은 이미 창발한 M2/M5/M17/M18에서 파생(끼워맞춤 0). |
| **E4** | 정동 기능적-접근 표지 **M20** (`emerge_affective_access`) — 인지 PCI의 정동 대응 | 고스트레스 게인이 M4 선택을 **접근→회피로 전이**(테스트 가능한 공포-회피). 엄밀 전역접근 = **정직-음성(HONEST_NEGATIVE)**, 느껴지는 질(층 3) = **OPEN** — **단일 하드 프라블럼이 인지처럼 정동을 덮음**. |

**신규 측정 앵커 3종 (engine `data/`):** `neuroendocrine_atlas.json` (NE/DA/5-HT/옥시토신 + HPA 코르티솔
키네틱 [L]; 농도→게인 변환 [O]) · `interoception_atlas.json` (SA결절 고유율·HEP 잠복창·HRV 대역·미주
구심분율 [L]; 구심 latency [O]) · `affect_observables_atlas.json` (정동 관측치 10종, **M12와 분리**해
M12 byte-identical 유지 → M19가 `combined_with_M12`로 보고). 각 항목 출처·등급 verbatim.

---

## 2. FROZEN HASHES (verify against these)

| Artifact | sha256 |
|---|---|
| **v1.17 PRE-promotion engine tree** (HISTORICAL anchor, preserve forever) | `b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7` |
| **v1.19 promoted engine tree** = **v1.20 M0–M16 출력 서브트리** (불변, add-only 보존점) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| **v1.20 NEW full tree** (M0–M20; 2× 결정론, SEED=19) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **v1.20 regression_scalars.json** (+M17–M20 불변) | `73c0992bc09499c393157a53c5f8792881352b5225e6385be6bd5658f3a179d8` |
| geometry decision-check (`geometry_grounding.py`) | `8ad43a72b2f8282cae801ed8468c883b79eab0c79363ebd98621cbbfc18ff80f` |
| chapter-16 phenomenology M12 (불변) | `bab1be8ff7df3a76cb838233a37d74af09df00130e70373fb4587e36812d64d4` |

**핵심 보존 불변식 (회귀가 직접 assert):**
`sha256_of({M0…M16}) == 3a1ebbbb…` — M17–M20을 더해도 M0–M16 출력은 **한 바이트도** 바뀌지 않는다.
바뀌는 것은 **전체 tree 해시뿐**(`0fbf4988…`, 의도된 add-only 결과).

**Honesty ledger (전면 불변):** `medium_efficacy_tested=0`, `hard_problem_open=1`,
`consciousness_claim=0`, `new_tuned_constants=0`. M18 심장/HPA·M19 정동은 **측정 기반 메커니즘이지
의식 주장 아님**; M20 정동-접근 = **정직 음성**.

---

## 3. GATE / REGRESSION STATUS — REGRESSION 134 / 134 PASS (exit 0)

회귀 **114 → 134**(+20): M0–M16 보존 2 + 모듈 존재 1 + M17 5 + M18 5 + M19 4 + M20 3.
런타임 ≈ **39 s** (목표 ~50 s 이내, 최적화 불필요). 기존 게이트(gate.py 71/71, boundary,
terminology, registry, em_thesis, 13/14/15/16/17 verify, geometry 역사적-앵커+승격-착지)는 v1.20
add-only로 **모두 그대로 통과**(geometry 체크는 v1.17 앵커 `b18c8626`만 참조하므로 새 tree에도 무영향).

### How to reproduce (from package root)
```bash
cd repro/mind/_engine
python3 run_all.py          # → expected_sha256.json: tree=0fbf4988…, scalars=73c0992b…
cd ../_verify
PYTHONPATH=../_engine python3 run_regression.py    # → REGRESSION PASS — 134 checks, SEED=19
```
M0–M16 보존만 따로 확인하려면:
```python
import vp_mind_engine as E
R = E.emerge_all()
sub = {k:v for k,v in R.items() if int(k.split('_')[0][1:]) <= 16}
assert E.sha256_of(sub) == "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"
```

---

## 4. ENGINE MAP after v1.20 (M0–M20, all on the R19 bistable primitive)

```
M0  organs (FOXG1/EN1/SIM1/LHX2)      ── SIM1 = 시상하부 PVN/SON = HPA 허브(정초)
M1  EM brainwave (FHN, ~c)            ── M18 SA결절이 동일 FHN 진동자 재사용
M2  hippocampal memory (theta-phase)  ── M19 기분-일치 회상이 이 로직을 종단 검증
M3  parallel eddies (_ignitability)   ── M17 SNR readout이 fold/ignitability 재사용
M4  selection (Go/NoGo THRESH=0.6)    ── M20 스트레스→회피 전이가 이 선택을 편향
M5  learned field (dopamine RPE)      ── M17 valence의 '접근' 축 = M5
M6–M11  stream/embodied/field/coord/sensory/light-memory
M12 phenomenology (+ 시상하부 루프; 카탈로그 byte-identical 보존)
M13 spectral · M14 sleep · M15 calibration · M16 main carrier
────────────────────────── v1.20 ADD-ONLY (appended LAST) ──────────────────────────
M17 global state      전역 각성게인 → 인지(역U) + 정동(각성/valence) 공변
M18 interoceptive     심장(SA·FHN)→미주(구심 우세)→시상하부 ; HPA 코르티솔 24min 피크
M19 affective readouts 같은 기질의 정동 8/9 ; 기분-일치 회상 = M2 검증
M20 affective access  스트레스→회피(테스트 가능) ; 엄밀접근 정직-음성 ; 느껴짐 OPEN
```

---

## 5. 설계 불변식 (다음 세션에서 절대 깨지 말 것)

1. **add-only 우선.** 새 모듈은 `emerge_all` **맨 끝**에 배선 → M0–M16 byte-identical. 엔진 승격이
   불가피하면 **오직 VP-SPEC §6-6** 절차(의도적 해시 변경 + 역사적 앵커 보존)로만.
2. **튜닝 금지.** 보편(universal) 또는 인용-측정(cited-measured)만 허용. **per-target 튜닝 금지**.
   상수는 [L](인용) · [F](모델링 선택, robustness sweep 필수) · [O](미해결, 선언)로 등급.
3. **방화벽 유지(축 A).** 메커니즘은 [V]/[L]/[F]로 보고하되, **느껴지는가**는 단일 하드 프라블럼
   (`hard_problem_open=1`)으로 남기고 **인지·정동을 동일하게** 덮는다. "감정 하드 프라블럼"을 따로 만들지 말 것.
4. **정직 원장 4-플래그 불변**(§2). 어떤 모듈도 efficacy/consciousness를 1로 올리지 말 것.

---

## 6. v1.21 ENTRY POINTS (작업 후보)

- **E2′ (구심 latency [O]→[L]).** 미주 구심 전도 latency의 **정본 측정 앵커**를 verbatim 인용해
  M18 `afferent_latency_grade`를 [O]→[L]로 승격. (neuro 패키지 또는 1차 문헌 필요 — §7 참조.)
- **E3′ (정동 관측치 확장).** 혐오(disgust)·놀람(surprise) 등 추가 정동 표지를
  `affect_observables_atlas.json`에 인용-측정으로 더하고 M19 concordance 재측정 (도메인튜닝 0 유지).
- **질병 스트레스-테스트(§8).** 아래 로드맵을 add-only 결정-검사 모듈로 단계 실행.

---

## 7. 다음-세션 인계 매니페스트 (★ 사용자 명시 요청)

> **원칙.** 지금은 첫 세션이라 4개 패키지를 모두 업로드했지만, **다음 세션에는 아래 "필수"만** 올리면
> 된다. 나머지는 v1.20에 이미 내재화되었거나 해당 과제에서만 필요하다.

| 인계 | 파일 | 비고 |
|:---:|---|---|
| ✅ **필수** | **v1.20 패키지 zip 1개** (`mind_vp_site_v1_20_*.zip`, 본 세션 산출물) | 모든 확장의 기반. 압축 해제 후 §3 재현으로 무결성 확인. |
| ✅ **필수** | **v1.21 안내서** (`NEXT_PHASE_GUIDE_v1_21_*.md` — 다음 과제 정의서) | 과제 스코프·DoD. 없으면 §6 후보 중 택일. |
| 🔶 **조건부** | `neuro_emergence_chain_integrated_v1_*.zip` | **E2′(미주 latency) 또는 세타-페이싱 앵커**를 [O]→[L] 승격하는 과제일 때**만**. 정본 측정 상수의 단일출처 verbatim 인용용. |
| ❌ **불필요** | `dna_vp_site_INTEGRATED_v1_9_1_FINAL.zip` (8.3 MB) | 심장 창발 참고는 v1.20에서 종료. 내수용 기능은 M18 + `interoception_atlas.json`에 **이미 내재화**. DNA-4D는 심장의 *존재*를, M18은 *기능*을 다루며 분리됨. |
| ❌ **불필요** | `dna_..._FINAL_zip.sha256` | 위 zip의 부속. 함께 불필요. |

**요약: 기본 인계 세트 = {v1.20 zip, v1.21 안내서} 2개.** (E2′/세타 과제면 neuro zip 1개 추가.)

---

## 8. 질병 스트레스-테스트 로드맵 (★ 사용자 명시 요청; 완성 후 단계 실행)

**목적.** 정상 기질이 임상 증후를 *재현*하는지로 모델의 **구성 타당도**를 시험한다. **튜닝 절대 금지** —
질병은 **이미 [L]로 인용된 파라미터를 측정된 임상 방향으로 섭동(perturb)**해서만 만든다(예: HPA 게인↑,
신경조절 게인↓). 각 단계는 **add-only 결정-검사**(엔진 기본값 불변, M0–M16 byte-identical)로 구현하고,
"정상이 재현하는 임상 사실"을 **사전 등록 가설**로 박은 뒤 **있는 그대로** 보고한다. 의식/efficacy 플래그는
**불변**; 어떤 질병도 "느껴짐"을 주장하지 않는다.

| # | 질병/상태 | 섭동(측정 방향) | 재현 목표(사전등록, 인용 필요) | 재사용 모듈 | 등급 |
|:--:|---|---|---|---|:--:|
| D1 | **만성 스트레스 / HPA 과활성** | HPA 게인↑·음성피드백↓ (코르티솔 baseline↑, 회복 지연) | 코르티솔 피크/회복 창 이동; **M17 역U가 과각성쪽으로 이동**(스트레스-주의협착 악화) | M17·M18 | [F]섭동+[L]앵커 |
| D2 | **우울증 / 둔마(anhedonia)** | 도파민 RPE 게인↓ (M5), 보상민감도↓ | **기분-일치 회상이 부정쪽으로 편향**(Bower); 접근(valence+) 약화 | M5·M17·M19 | [F]섭동 |
| D3 | **불안 / 공황** | 위협 게인↑, M20 회피 임계↓ | 저스트레스에서도 **회피 전이**(D2와 분리); HEP-각성 결합 과민(과각성 내수용) | M18·M20 | [F]섭동+[L]HEP |
| D4 | **PTSD / 과각성** | NE-LC tonic↑(각성 baseline↑), 소거 학습 저하 | M17 각성 baseline 상승 → **역U 작동점 협착**; 침습 단서 과반응 | M17·M2·M18 | [F]섭동 |
| D5 | **자율신경 실조 / 내수용 둔감** | 미주 구심 게인↓ (afferent:efferent 4:1 → 저하) | **HEP-각성 추종 약화** → 정동 해상도 저하(둔마와 직교 검정) | M18·M19 | [F]섭동+[L] |
| D6 | **번아웃 / HPA 저활성(말기)** | 만성 후 HPA 게인↓ (코르티솔 무딘 반응) | D1의 거울상 — 급성 코르티솔 피크 **소실**; 회복 곡선 평탄화 | M18 | [F]섭동 |

**공통 검증 규약(각 D-모듈):** (i) 섭동은 **단조·해석 가능**해야 하며 임상 *방향*만 사용(크기 fitting 금지);
(ii) **anti-tuning**: 섭동 격자/시드를 흔들어도 *질적 방향*(예: 회피 전이, 회상 편향)이 유지됨을 보고;
(iii) **정상 ↔ 질병 대조**가 핵심 readout(예: D2 = 기분-일치 회상의 정→부 전환); (iv) 엔진 tree **불변**
확인 + 결과 2× 결정론 동결; (v) 정직 원장 4-플래그 **불변**. **우선순위 제안: D1 → D3 → D2**
(HPA 축이 v1.20에서 가장 잘 정초됨 → 불안/공황 → 둔마 순).

---

## 9. ONE-LINE STATUS

> v1.20 = **인지·감정 단일 기질 완성**(M17–M20, 순수 add-only). 전체 tree `0fbf4988…`,
> M0–M16 `3a1ebbbb…` **불변**, 회귀 **134 PASS**, 정직 원장 **불변**.
> 다음 인계 = **{v1.20 zip, v1.21 안내서}**; 다음 과제 후보 = **질병 스트레스-테스트 D1→D3→D2**(§8).
