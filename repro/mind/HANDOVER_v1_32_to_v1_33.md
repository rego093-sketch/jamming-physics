# HANDOVER — v1.32 → v1.33  (Part II: 마음의 장애 — 자폐 3축·화학 한계·θ-cap 페이스메이커·운영원리+실현가능성·ADHD 분리·가상임상 §18–23 / mind 패키지)

> **요약 한 줄.** v1.32는 **이미 동결된** 질환 메커니즘(D-계열 disease 엔진 + θ-cap virtual-clinical VC1–VC5)을
> 연구 내용에 맞춘 **6개 well-separated SEO 챕터(§18–23)** 로 출판하고, 그 재현 코드를 `repro/mind/_verify/`에
> 통합(bit-for-bit)하며, θ-cap의 **물리적 실현가능성을 정직하게 검토**한다([O]). 자폐를 **세 축 결함(T/O/W)** 으로
> 분해하고 ADHD를 별도 페이지로 분리한다. **엔진·모든 기존 과학 결과 byte-identical, 새 튜닝 0·새 측정 0**,
> efficacy=0·NOT medical advice 방화벽 전 챕터 유지. 사용자 요청(자폐를 단일 HTML 아닌 여러 SEO 페이지로 전개 +
> ADHD 별도 + θ-cap 실현가능성 검토)을 이번 세션에 완수.

---

## 1. WHAT v1.32 DELIVERED (complete, all gates green)

**Part II: Disorders of the mind — 6 신규 정준 챕터(전부 등급 model, efficacy=0).**

- **§18 `18-autism-three-axis`** — 자폐 = 한 병변이 아니라 세 분리 가능한 결함. **T**(threshold/E-I, 점화 fold↑)·
  **O**(output/gain, 노드 구동↓)·**W**(long-range wiring, fold·구동 정상이되 local-over/long-range-under 기하).
  쌍 **(ΔPAC, 점화 fold)** 이 유일하게 지문화(T: PAC↓·fold↑ / O: PAC↓·fold 정상 / W: PAC 불변). 17-유전자 중등도
  ASD 코호트(15 atlas + 2 live NCBI: GABRA5·MACROD2; γ via SantaLucia 1998, window [TSS−2000,+500]=2501bp)가
  T(6)/O(7)/W(4)로 분할, 중증 DEE/증후군성 사전등록 제외. **어느 결함이 개인의 자폐인지 [O].**
- **§19 `19-autism-chemical-limits`** — 화학 도달 한계(마스크 vs 교정). 스칼라 gain 화학(자극제 계열 메커니즘)이
  **T 완전 역전·O 부분·W 마스크-only**(over-sync, locality 불변). tri-lever = 안전 마진이지 새 efficacy 아님.
- **§20 `20-theta-cap-pacemaker`** (keystone) — θ-cap = 외부 **페이스메이커**지 benign lane 아님. C-FORCE만 라우팅,
  수동 lane 전부 inert → **benign-lane REFUTED**. 깨끗이 제거 가능(의존성·rebound 0, 가소성 변수 없음), spinodal fold
  아래 분자 안전(비가역 flip 0). 구속 = 회로 over-sync지 분자 마모 아님.
- **§21 `21-theta-cap-operating-principle`** — 운영 원리([F disc]) + **물리적 실현가능성 검토**([O]). 동역학이
  단일 모드 강제: **minimum-effective·deficit-matched·continuous**(banking 없음). 실현가능성: 모든 구성요소
  (θ-tACS·closed-loop phase-locked EEG-tACS·multi-electrode long-range montage·MRI-optimised targeting·wearable
  delivery)는 **오늘날 존재**하나 **특정 조립은 부재** + 4 장애요인(wiring readout 부재·좁은 창 over-sync·심부
  표적화·위상 의존 가소성 부호) → **[O]**. **장치 실현가능성 ≠ 이익.**
- **§22 `22-adhd-vs-autism`** (별도 페이지) — 명시적 유전자-접지 ADHD 기질(O/gain 6·T/arousal 2·**W=없음**;
  FOXP2·ADGRL3 제외). 자극제가 ADHD 복원(자폐는 부분만)·cap은 wiring서 3.34× 선택적·**AuDHD서 간섭 없이 합성**.
  **ADHD 모델 타당성 [O].**
- **§23 `23-virtual-trial`** — 집단 그림(N=80, 76 affected). 반응자 gain-지배(r=−0.60), 비반응자 wiring-지배·cap
  32% 구제. **정직한 반증→발견(FINDING-VC5c)**: 잔여 = dose-cap/stiffness 한계지 중증-W 꼬리 아님 → 진폭은 결함에
  맞춰야. **모든 분율 = in-silico coupling state.**

**재현 코드 통합 (add-only, bit-for-bit).** `theta_cap_virtual_clinical` 패키지서 12 python 모듈 + 의존 JSON을
`repro/mind/_verify/`로 통합: `run_all_d9.py`(D9.0–D9.4 ALL PASS) + `run_all_vc.py`(VC1–VC5, 14 CONFIRMED·1
REFUTED). 6 챕터 reproduce GitHub 링크가 실제·자기완결. 각 `repro/mind/<slug>/README.md` 작성.

**신규 LOCK 9개 (전부 framing, check:None).** `autism_three_axis`·`autism_chemical_reach`·`theta_cap_pacemaker`·
`theta_cap_removable`·`theta_cap_molecular_safe`·`theta_cap_operating_principle`([F disc])·`theta_cap_feasibility`
([O])·`adhd_axis_specific`·`virtual_trial`. (자폐/VC 숫자는 `_verify/` 모듈 자체 sha256 게이트에 있고 엔진
emergence results엔 없으므로 framing-type — registry validate()의 check-bearing 교차확인 대상 아님.)

**변경 파일.** 신규 6 챕터(`docs/mind/18..23-*/index.html`) + 6 repro README(`repro/mind/18..23-*/README.md`) +
재현 모듈 12개(`repro/mind/_verify/`, add-only) + hub `docs/mind/index.html`(Part II arc+toc) + `manifest/mind.csv`
(+6행) + `docs/mind/_meta.json`(+6 챕터, totals 15372) + §17↔§18 nav 연결 + `tools/mind_registry.py`(LOCKS+9/
CITES+6/ANSWERS+6) + 거버넌스(CHANGELOG·MASTER_MANUAL·COMPLETION_LEDGER·본 HANDOVER). **엔진·`_verify` 기존
모듈·기존 docs 챕터(§01–§17) 본문 0 변경.**

---

## 2. FROZEN HASHES (verify against these — v1.32에서 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine source** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **DGENE** `disease_gene_atlas_results.json` (불변) | `980985c629978f37d00cd0c67cf49d63df4cde32370cb2dcd0e60feab66520e3` |
| docs 검색층 트리 md5 (gate 멱등 비교용) | `53f2a138cb1a…` (sitemap `<lastmod>` = R.RELEASE_DATE, 날짜-무의존) |

엔진·DGENE 해시가 v1.28–v1.31과 글자 그대로 같다 — v1.32가 과학을 안 만졌다는 직접 증거. (검색층 md5는 챕터 6개가
sitemap/llms-full에 추가되며 v1.31의 `1047a527…`에서 `53f2a138…`로 갱신 — docs C4 층 변경이고 엔진/과학 결과와 무관.)

**D9 / VC 재현 헤드라인(패키지 내 bit-for-bit 확인).** D9.0 `51ebcaf6…`·D9.1 `633e9f64…`·D9.2 `738d3f9b…`·
D9.3 `5530bace…`·D9.4 `57a065f1…` (run_all_d9 ALL PASS). VC1 `eae5e190…`·VC2 `51362445…`·VC3 `d045928f…`·
VC4 `aed19bc2…`·VC5 `527ee1df…` (run_all_vc ALL PASS, 14 CONFIRMED/1 REFUTED).

---

## 3. GATE / REGRESSION STATUS — gate.py PASS **110/110** (0 hard fail), 회귀 byte-identically 불변

게이트 전부 green:
- **`gate.py` PASS 110/110** (v1.31 baseline 83/83 = 17 chapters → **+27** = 신규 6 챕터의 answer-first/cards/
  JSON-LD 검사).
  - answer-first **23/23**(§18=53·§19=53·§20=52·§21=51·§22=51·§23=51w, 전부 40–60w) · sitemap **24 locs / 24
    pages** · llms.txt **4989 bytes(<5KB)**(하드코딩이라 챕터 추가에 불변) · engine reproduces **`0fbf4988…` ==
    expected** · SSOT drift **0** · body word counts **±2%**(§18=769·§19=645·§20=711·§21=1013·§22=580·§23=509
    정확 매칭) · build **멱등**(`53f2a138…` 재실행 동일).
- registry **33 locks / 23 chapters**(drift 0) · boundary **8/8** · terminology(금지 표현 §18–23 부재) ·
  em_thesis **6/6** · **run_all_d9 ALL PASS** · **run_all_vc ALL PASS**(14/1).

> **회귀 불변 증명.** `run_regression.py`는 `vp_mind_engine`와 `_verify/`의 모듈만 import한다. v1.32가 바꾼 파일 중
> 회귀가 import하는 건 **0개**(신규 챕터·hub·manifest·_meta·registry·거버넌스·신규 _verify 모듈은 add-only). 따라서
> 회귀 결과는 v1.31과 **증명적으로 동일**(엔진 `0fbf4988…`·DGENE `980985c6…` 불변 교차확인). gate의 engine-reproduces
> 검사가 엔진 트리 byte-identical을 확증한다. (신규 _verify 모듈은 자체 sha256 게이트 run_all_d9/run_all_vc로 검증.)

### How to reproduce (from package root)

```bash
cd mind_pkg
python3 tools/build_search_layer.py                # 23 chapters, sitemap 24, llms.txt 4989B <5KB
python3 tools/gate.py                              # PASS 110/110, 빌드일 무관
python3 tools/mind_registry.py                     # 33 locks / 23 chapters, values match frozen
python3 verify_boundary.py && python3 verify_terminology.py
python3 repro/mind/02-not-a-field/verify_em_thesis.py
python3 repro/mind/_engine/run_all.py              # tree_sha256 = 0fbf4988…
python3 repro/mind/_verify/run_all_d9.py           # D9.0–D9.4 ALL PASS, engine byte-unchanged
python3 repro/mind/_verify/run_all_vc.py           # VC1–VC5 ALL PASS (14 CONFIRMED / 1 REFUTED)
python3 repro/mind/_verify/run_regression.py       # REGRESSION PASS (SEED=19, ≈7분; v1.31과 동일)
```

---

## 4. THE FIREWALL, STATED ONCE MORE (so it cannot be misread — YMYL/medical)

이 Part II는 의료/건강(YMYL) 영역이며 방화벽은 **협상 불가**다:

- **`medium_efficacy_tested = 0` (efficacy=0).** buildable ≠ beneficial. 어떤 챕터도 약/장치가 자폐를 *치료한다*고
  주장하지 않는다. **NOT medical advice.**
- **cap = crutch/pacemaker, NOT repair.** 가소성 변수가 없어 제거 즉시 결함 재개 — 라우팅을 *대신 페이싱*할 뿐
  배선을 고치지 않는다.
- **[O] 3종.** (i) *어느 결함이 진짜 그 사람의 자폐인지*; (ii) *ADHD 모델 타당성*(별도 검증된 ADHD 모델 없음 —
  유전자-접지 해석); (iii) *물리적 실현가능성*(구성요소는 존재, 통합 장치는 부재).
- **`consciousness_claim = 0`, `hard_problem_open = 1`.** Part II는 메커니즘 축. 느낌 축은 직교·범위 밖.
- **모든 분율은 in-silico coupling state**지 임상 반응률·진단·처방이 아니다.

각 챕터 마지막 섹션에 이 방화벽 문장이 부착되어 있다(생성기 FW 변수).

---

## 5. v1.33 ENTRY POINTS (next session)

**A — 운영 원리 정량화 (선택, Part II를 더 닫음).** §21이 강제한 deficit-matched 모드를 in-silico로 한 발 더:
wiring readout proxy(예: 관측 가능한 far-coh / 1/f 기울기)에서 **폐루프 최소-유효 진폭 추정기**를 엔진 핸들로
구현해, "진폭을 결함에 맞춘다"를 *명시적 제어기*로 시연(여전히 efficacy=0·in-silico). FINDING-VC5c가 직접 요구하는
다음 단계.

**B — 잔여 질환 과학 (v1.30부터 이월).** (a) DGENE 발판으로 **BD/OCD/ID 메커니즘 결정-검사**(D-계열 패턴, 부호만
assert); (b) **중독 M5-RPE**(도파민 가치 신호 오작동); (c) 유전자-OWED 4질환 상환 잔여. 전부 `_verify/` add-only +
자체 sha256 게이트.

**C — 자폐 1/f readout (v1.31 §5B 이월 잔여).** 자폐 코호트의 aperiodic(1/f) 기울기를 T/O/W 축과 교차 — E/I
바이오마커로서 (ΔPAC, 점화)에 *독립적 관측축* 추가(있으면 §18 판별식 보강, 없으면 정직 음성).

**규율 리마인더.** 어떤 v1.33 작업도 (i) 엔진은 READ-ONLY/byte-identical 유지(새 모듈은 `_verify/` 또는 신규 엔진
모듈로, 기존 M0–M20 불변); (ii) 새 튜닝 상수 0(측정값·유도값만); (iii) HTML 본문 English-only(C0); (iv) llms.txt에
챕터 추가 금지(하드코딩, <5KB 헤드룸 ~11바이트); (v) **efficacy=0·NOT medical advice·[O] 3종·hard problem OPEN**
방화벽을 신규 챕터마다 부착; (vi) 단일 zip 산출물(내부 폴더 항상 `mind_pkg`); (vii) 변경 후 §3 8게이트 전부 green
확인 — FAIL 시 finalize 금지.
