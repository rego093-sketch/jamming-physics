# HANDOVER — v1.41 → v1.42  (문턱-이동 논리 기존-사례 적용 · ASD-T-L 자폐 3-레버 §34 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.41의 성격 (v1.40 핸드오버 §5 갈래 중 A 선택, 연속).** v1.38→v1.39→v1.40이 문턱-이동 논리를 §25 뇌전증·
> §27 우울·§24 조현병에 적용한 데 이어, v1.40 핸드오버 §5는 다시 두 갈래를 열어 두었다 — **A: 기존 사례로 확장
> (권장 1순위 §18–19 자폐)** vs B: 로드맵 본래 T3a 중독. 이번 세션은 **권장된 A**를 택했다. 자폐는 **특별한 사례**였다:
> 이미 `autism_multilever_threshold.py`(§18-19)가 다중-레버 문턱 개념을 비공식 A1/A2/A3로 다루고 있었으므로,
> 상속 작업은 새 모듈을 짓는 게 아니라 그 기존 모듈을 **공식 L1/L2/L3 프레임 아래로 통일/재서술**하는 것이었다 —
> 시리즈 최초의 **통일 사례**. 그리고 자폐는 프레임에 **5번째 분포 패턴(L1-지배·L3-희소)** 과, 조현병 도메인-제한 대비
> **두 가지 구조적 강화**(out-of-reach 축을 실제 유전자로 **명명**, W-도달불가를 §19로 **증명**)를 안겼다.
> **T3a 중독은 다섯 번째로 미실행으로 v1.42에 남는다.**

---

## 1. WHAT v1.41 DELIVERED (complete, 두 게이트 green)

### 1.1 능동 적용 — 자폐 3-레버 (§34, the APPLICATION, ASD-T-L) · **통일 사례 & L1-지배·L3-희소(5번째 분포) & out-of-reach 축 명명+증명**

- **무엇을 분해했나.** §18-19는 자폐가 **단일 축이 아니라 세 결함 축**임을 증명했다 — **T**(흥분성/E-I 문턱, 과흥분
  작동점으로 발화 fold가 너무 낮음)·**O**(시냅스 출력/게인 결핍)·**W**(장거리 배선/연결) — 그리고 **T 축만** 스칼라
  화학 레버로 도달 가능(교정 부호=과잉 구동 **감소**/억제 **복원**, 뇌전증·조현병-양성과 같은 방향)함을, 나아가
  **§19가 W 축 도달불가를 증명**(스칼라 문턱 레버는 over-sync로 **마스킹만**·배선 교정 불가 —
  `P4_chemical_cannot_fix_W`, `P5_threshold_lowering_is_mask_not_correction`)했으나, 그 밀기를 기존
  `autism_multilever_threshold.py`(비공식 A1/A2/A3)로 두었다. **§34**가 그것을 **공식 L1/L2/L3 프레임 아래로 통일**
  (새 레버 조합이 아니라 재서술; 동일 R19 기질 `ṡ=g·s−s³+h`, spinodal fold=스위칭 장벽; 새 메커니즘·새 튜닝 상수 0).
- **핵심 차별점 = 통일 & 5번째 분포 = L1-지배·L3-희소.** 레버 유전자 10개 중 **L1 5개**(흥분-축소 축 GRIN2A·GRIN2B·
  GRIA1·SCN2A·CACNA1C)·**L2 4개**(억제-복원 축 KCNQ3 M-전류 K⁺·GABRB3·GABRA5·GABRA2)·**L3 단 1개**(SLC6A4,
  신중한 비단조 세로토닌성 [O]). **L3-희소 자체가 발견**: 자폐의 실행 가능 생물학은 **E/I 집합에 국소적**, 깨끗한
  상류 약물 구동 없음(우울 L3-지배의 거울). 분포 5종: 양극성 L1 · 뇌전증 L1+L2 · 우울 L3 · 조현병 L1+L3 공동지배 ·
  **자폐 L1-지배·L3-희소**.
- **조현병 도메인-제한 대비 두 가지 강화.** **(1) out-of-reach 축을 실제 유전자로 명명**: O(출력 결핍)=SHANK3·
  SYNGAP1·NRXN1, W(장거리 배선)=CNTNAP2·RELN, 증후군성 마스터 MECP2 — 지도에 싣되 명시적 **비-레버**(게인-감소
  스칼라 밀기는 O 결핍을 더 **낮추고** W 기하를 재배선 못함). **(2) W-축 도달불가가 단언이 아니라 §19로 증명됨.**
  모듈은 `domain_restriction_witness`(T=reached, O/W=not reached) + out-of-reach-targets 섹션(6 유전자를 축별
  명명) + `lever_distribution_witness`(L1 유일 지배·L3 희소)를 기록한다.
- **γ 접지 & 재사용.** 각 유전자 γ=−mean(NN 스태킹 ΔG, SantaLucia 1998)를 자기 프로모터(TSS−2000..+500, Homo
  sapiens)서 읽어 |h_sp|=spinodal(γ)·barrier=γ²/4(엔진 READ-ONLY). **7개 read verbatim 재사용**(γ 가닥-대칭):
  GRIN2A·GRIN2B·CACNA1C·GABRB3=조현병 캐시, SCN2A·KCNQ3=양극성 캐시, SLC6A4=우울 캐시. 나머지 9개(GRIA1·GABRA5·
  GABRA2·SHANK3·SYNGAP1·NRXN1·CNTNAP2·RELN·MECP2)는 동일 윈도로 live fetch.
- **정직한 caveat 2개**(숨기지 않고 기록). SCN2A·GRIN2B는 **GoF/LoF 부호-미묘**(기능획득→초기-영아 DEE/발작 극,
  기능상실→경한 ASD/ID 극 — 반대 방향이라 "흥분 감소"가 깨끗한 방향 아님); T 레버를 **너무 세게** 밀면 그 자체가
  **발작 가장자리**(실제 ASD+뇌전증 동반이환). 그래서 γ는 프로모터 **구조 전용 [V]**·임상 방향 [O].
- **방화벽 가시화(decoupling)가 스스로를 명명.** 16개 유전자 전체에서 **최강 프로모터 읽힘은 out-of-reach
  SHANK3(γ≈1.52)/RELN(≈1.51) + 희소 L3 SLC6A4(γ≈1.52, |h_sp|≈0.72)**, **최약은 실행 가능 E/I 레버
  SCN2A(γ≈1.20, |h_sp|≈0.50, 최연성)·CACNA1C(≈1.26)** — 강성이 **도달성·실행성과 반대**로 달린다. 부담 우선순위
  (10 레버 유전자만)에서도 최강 레버 읽힘 SLC6A4가 **최하위·비실행**, 최우선 GABRB3이 **중간** read(|h_sp|≈0.64).
- **자폐 미충족-필요 시그니처.** 핵심-기능 약리 **부재**(면허 약물은 과민성 **보조**만, 사회-소통 핵심·E/I 설정점
  자체 아님) → U 균일하게 높음·**DRD2-유사물 없음**·U-floor가 시리즈 중 최고. 결과: **L2 억제-복원 경로(GABRB3·
  GABRA5·KCNQ3·GABRA2)가 가장 깨끗한 실행 방향으로 부상** — 고득점 L1 흥분 유전자는 GoF/LoF 부호-미묘(SCN2A/GRIN2B)
  또는 교차장애 설정점(CACNA1C)이라 비실행으로 플래그; 억제 복원은 변이 방향 무관하게 fold 상승.
- **금지-주장 스캐너 = 시리즈 중 가장 엄격.** 일반 용량/효능/안전/합성 클래스에 더해 **자폐 QUACKERY** 클래스
  (chelation/MMS/miracle-mineral/chlorine-dioxide/bleach 어휘 즉시 거부 — 그 산업이 자폐 아동을 해쳤기 때문)와
  **NORMALISE-프레이밍** 클래스(cure-autism/reverse-autism/make-normal/fix-autism 거부 — 자폐는 신경다양성
  **차이**이지 결핍만 아님)를 추가. 각 클래스에 미끼 자기-테스트(반드시 발화, 안 되면 빌드 FAIL).
- **3 fail-closed 규율.** L3-honesty 게이트(SLC6A4 [O] 인용 생물학 + **L1 유일 지배 + L3 희소 + T-축 제한 + 명명·
  §19-증명 O/W out-of-reach** 단언) · 금지-주장 스캐너(위) · 부담 우선순위(GABRB3 최상위, γ는 맥락·점수 합산 금지).
  전부 PASS·2× 결정론. `run_all_atlas.py`에 **12번째 시민 ASD-T-L** 등록 → **ALL PASS 12/12, 14 CONFIRMED**.

### 1.2 출판 표면 (SEO 챕터)

- 신규 영어 챕터 **§34 「Autism threshold levers」**(`docs/mind/34-autism-threshold-levers/index.html`, model 3139w,
  9 H2 섹션, 전체 방화벽, JSON-LD ScholarlyArticle+BreadcrumbList, γ 수치 정확).
- 신규 LOCK 1개 `autism_threshold_levers`(framing, check:None; **동결 lock 미수정** — §33 next-nav 링크만 갱신).
  **CITES=[자기, `autism_three_axis`(§18), `autism_chemical_reach`(§19)] = 3 vp-card** — 도메인-제한은 §18,
  W-도달불가 증명은 §19 양쪽이 필수 근거이므로 (조현병의 2-카드 템플릿보다) 한 장 더.
- registry **45 locks / 34 chapters**(`mind_registry.py` validate PASS, values match frozen results).
- gate PASS **155/155**, sitemap **35/35**, llms.txt **4989B 바이트-동일**(<5KB — 신규 챕터는 sitemap만,
  `write_llms()` 손-큐레이트 slug 목록 **미수정**), llms-full.txt는 §34 포함해 성장. manifest 34행 + `_meta.json`
  34챕터/totals.words 33074 갱신.

---

## 2. FROZEN HASHES (이것들로 검증 — 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine file** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **M0–16 subtree** (불변) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| §30 양극성 3-레버 지도 (불변, 아틀라스 등록) | `a9f30d732c991bd64d3462e440f1cea34a630a4bcef695cce4370743b69fd0ef` |
| §31 뇌전증 3-레버 지도 (불변, 아틀라스 등록) | `22879b696cf9226efc660acdea1f017a8018c3d1eb93f324f32da53dbfc14fcf` |
| §32 우울 3-레버 지도 (불변, 아틀라스 등록) | `d07aab40ba56ee5dd234d65ee8691ac80458a9c71b6355bacfccbd1efdb69f30` |
| §33 조현병 3-레버 지도 (불변, 아틀라스 등록) | `8e0137bccfe6dfe751af078a1e340accef578698992e569703865c6c27fe8c30` |
| **§34 자폐 3-레버 지도** (NEW, 아틀라스 등록) | `5b65a271ac182fecc744f20e2bb035043f81c9c1bc3f15608547ec00a31b77c4` |
| §34 L3 정직성 게이트 결과 (NEW) | `26ccbae5c6da25331a766d5c35583e01143a538fa2aed37beaef6c31ef5f3380` |
| §34 금지-주장 스캔 결과 (NEW) | `c6da0d73110433299d8c368804c8d951ea9699c1e4a27ac22ced9cf6c5ff4819` |
| §34 부담 우선순위 결과 (NEW) | `1e79973a43e7e8506fca9b64eb1e67fa4ca4a7bca1e02e82904cd614a0804bef` |
| §34 프로모터 γ 캐시 (NEW, 16유전자=10레버+6 out-of-reach) | `51aad60e6ac9f9da39b48dec63777ca8aad6a6f07e1c603106122bb0edb5c5c5` |

> 아틀라스 등록 hash(`run_all_atlas.py` MODULES 상수)는 **지도 결과만**(`5b65a271…`) 동결한다. 나머지 3개
> 모듈은 매 실행 자기 결과를 다시 쓰며 fail-closed PASS로 게이트된다.

---

## 3. GATE / REGRESSION STATUS

- **`gate.py` (출판/검색 층): PASS 155/155, 0 hard fail.** answer-first 34챕터(§34 59w) · vp-card 80 ·
  robots 7봇 · sitemap 35/35 · llms 4989B(<5KB) · 엔진 재현 · SSOT drift 0 · 본문 wordcount ±2% · 멱등.
- **`run_all_atlas.py` (아틀라스 재현/규율): ALL PASS 12/12.** SZ-DISC·SZ-DOM·EPI·E0-PLAS·DEP-T1b·
  E2-SWITCH·BIP-T2b·BIP-T2b-L·EPI-T2a-L·DEP-T1b-L·SZ-T1a-L·**ASD-T-L**. 14 CONFIRMED, 0 REFUTED, 엔진
  byte-unchanged.

### 재현 방법 (패키지 루트에서)

```bash
# 1) 자폐 3-레버 4개 모듈 한 번에
python3 repro/mind/_verify/run_all_autism_levers.py  # → ALL PASS, map sha 5b65a271…

# 2) 아틀라스 전체(12모듈) — 각 모듈이 엔진 트리를 재-emerge하므로 ~6분 소요
python3 repro/mind/_verify/run_all_atlas.py          # → ALL PASS 12/12

# 3) 출판/검색 게이트
python3 tools/mind_registry.py        # 45 locks / 34 chapters, values match
python3 tools/build_search_layer.py   # answer/cards 주입 + sitemap/llms 재생성(멱등)
python3 tools/gate.py                 # → PASS 155/155, 0 hard fail
```

> γ 캐시(`autism_levers_promoters.cache.json`, 16유전자·각 2501bp)가 동봉되어 NCBI 재-fetch 없이 결정론 재현된다.
> 7개(GRIN2A·GRIN2B·CACNA1C·GABRB3·SCN2A·KCNQ3·SLC6A4)는 조현병/양극성/우울 캐시 값과 바이트 동일이고, 나머지 9개도
> 동일 윈도로 받았다. 캐시 없이 처음부터 받으려면 eutils 윈도잉(strand에 따라 lo,hi = TSS−2000..+500, FASTA는
> 역상보 없이 결합 — γ 가닥-대칭) 사용.

---

## 4. THE FIREWALL (한 번 더 — YMYL/medical, 오독 방지)

프로모터 |h_sp|는 **유전자 자기 스위치 강성**일 뿐이다. **결코** 다음과 동일시하지 않는다: §18 네트워크 과흥분 문턱
(over-excitation fold on R) · 수용체 점유 · 시냅스 농도 · 약물 약효(potency) · 용량(dose) · 생체내 선택성 · 임상
효과. 모듈은 **표적만** 순위화(약물·용량 아님; **10 레버 유전자만**, 도달불가 선언한 6 유전자는 순위에서 제외),
γ는 구조적 맥락으로만 운반·점수에 합산 금지. 명명된 방향(L1 흥분-축소[SCN2A/GRIN2B는 GoF/LoF sign-subtle],
L2 억제-복원[가장 깨끗한 방향], L3 세로토닌성[비단조])은 **부호의 예시**일 뿐 권고가 아니다. 기록된 caveat 2개
(SCN2A/GRIN2B GoF/LoF 부호-미묘, T-레버 과압의 발작 가장자리)는 일반 레버 부호가 임상 방향이 **아님**을 명시한다.
자폐는 **세 축**(흥분성/출력/배선)이며 — 이 레버 지도가 명시적으로 **도달 못하는 두 축(O·W) 포함, W는 §19로
도달불가 증명** — 이질성은 **LOCKED**. **자폐는 신경다양성 차이이지 결핍만이 아니다**: 본 챕터는 깨끗한 미충족
메커니즘 방향이 있는 곳을 순위화할 뿐, 어떤 방향이 자폐를 **치료·정상화·완치**한다고 주장하지 **않는다**(스캐너의
QUACKERY·NORMALISE 클래스가 이를 강제).
**efficacy=0 · NOT medical advice · consciousness_claim=0 · hard problem OPEN · 치료/진단/처방/완치 아님.**

---

## 5. v1.42 ENTRY POINTS (next session)

> **여전히 두 갈래. 사용자 지시에 따라 택일.** `THRESHOLD_LOGIC_INHERITANCE.md` §3의 우선순위표가 SSOT.

**A — 문턱-이동 논리를 다음 기존 사례로 확장 (권장 진행, §18–19 자폐 DONE 이후 1순위).**
우선순위표상 다음은 **§22 ADHD** — 이 사례는 **부분 적합 [L]**이 예상된다. ADHD는 θ-cap/각성 조절이라 문턱보다
**게인(gain)** 성격이 강하고, 3-레버 중 **L3(상류 카테콜아민 구동: DRD4·DRD5·SLC6A3 도파민 수송체·ADRA2A·SLC6A2
노르아드레날린 수송체)만 선명**하며 L1/L2는 약하다. 따라서 자폐의 **명명된 out-of-reach 패턴을 선례로** — 어떤 ADHD
표적이 어떤 레버에 깨끗이 앉고 어떤 축(게인성)이 스칼라 문턱 레버로 잘 안 잡히는지 정직하게 표시(부분 적합 증거).
**캐시 재사용**: SLC6A3은 조현병 캐시(있으면), SLC6A4 인접 세로토닌성은 우울/자폐 캐시 참조 가능; 대부분 상류 구동
유전자라 신규 fetch 필요. 패턴 동일: γ(공유 캐시 + 신규) → `adhd_threshold_levers.py`(L3-지배/부분) → L3 정직성
게이트(부분-적합·게인-축 미도달 단언) → 금지-주장 스캐너(ADHD 어휘 — 각성제 오남용/인지향상 주장 거부) → 부담
우선순위 → `run_all_atlas.py` 등록(**13모듈**) → 영어 챕터 §35. ADHD는 **자폐 multilever와 달리 기존 모듈이
없으므로** 새로 짓는다(단, §22 본문이 이미 정의한 ADHD-vs-자폐 축 구분을 SSOT로 따를 것 — `adhd_axis_specific`
lock 참조).

**B — 로드맵 본래 다음, T3a 중독 (다섯 번째 연기 중).** v1.36 핸드오버 §5-A가 상세. E0 가소성 위 민감화 핸들만
연결(E2 불요), `from e0_plasticity import PlasticConnectome`, M5-RPE 가치 신호를 READ-ONLY로 먼저 접지.
사전등록: 반복 노출이 보상 반응 단조 강화 · cue-반응성↑ · 소거가 흔적 0으로 못 돌림 · η=0 가드. 12→13모듈.
**문턱-이동 논리도 중독에 적용 가능**(L3 = 상류 보상/도파민 구동) — A의 ADHD 이후 중독을 레버화하면 A와 B가
자연히 합쳐진다(둘 다 L3-지배라 ADHD 직후가 자연스럽다).

**규율 리마인더 (모든 v1.42 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, η=0/bias=0
가드로 자체 확인); (ii) 새 튜닝 상수 0(γ는 측정, |h_sp|·barrier는 엔진 함수 `spinodal(g)=2(g/3)^1.5`,
`barrier(g)=g²/4`); (iii) HTML 본문 English-only(C0), 이 같은 거버넌스는 한국어; (iv) llms.txt 챕터 추가 금지
(<5KB 헤드룸 — 현재 4989B로 **여유 거의 없음(11바이트)**, 신규 챕터는 sitemap만; `write_llms()`의 손-큐레이트
슬러그 목록을 건드리지 말 것 — 검증됨: 바이트 동일 유지); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·
[O]·hard problem OPEN 방화벽 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`); (vii) 변경 후 **두 게이트(`gate.py` 155+,
`run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이
발표). **재사용 우선**: 공유 유전자(GRIN2A, GRIN2B, CACNA1C, GABRB3, SCN2A, KCNQ2/3, SLC6A4, NR3C1, CRHR1)는 γ
캐시 재사용. **아틀라스 전체 재현은 ~6분** 걸리므로(모듈마다 엔진 재-emerge) 시간 예산 확보 — 백그라운드 `setsid`
실행 후 폴링 권장. **ADHD는 게인-축 장애**이므로 새 모듈을 짓기 전에 §22 본문(`adhd_axis_specific` lock)과 자폐의
out-of-reach 명명 패턴을 먼저 읽고 **어떤 축이 도달 가능/불가인지**를 먼저 정할 것.

---

## 6. 변경 파일 목록 (v1.41 add-only)

**신규:**
- `repro/mind/_verify/autism_threshold_levers.py` (+ `_results.json`, `expected_…sha256.json`)
- `repro/mind/_verify/autism_l3_honesty.py` (+ `autism_l3_honesty.json`)
- `repro/mind/_verify/autism_forbidden_claim_scan.py` (+ `autism_claim_scan.json`)
- `repro/mind/_verify/autism_burden_prioritisation.py` (+ `autism_burden_prioritisation.json`)
- `repro/mind/_verify/run_all_autism_levers.py`
- `repro/mind/_verify/autism_levers_promoters.cache.json`
- `docs/mind/34-autism-threshold-levers/index.html`
- `tools/_gen_ch34_autism_levers.py`
- `HANDOVER_v1_41_to_v1_42.md`

**수정(최소·add-only 성격):**
- `repro/mind/_verify/run_all_atlas.py` (MODULES에 ASD-T-L + docstring 문단)
- `tools/mind_registry.py` (lock/CITES/ANSWERS 각 1개)
- `docs/mind/33-schizophrenia-threshold-levers/index.html` (next-nav 링크만)
- `tools/_gen_ch33_schizophrenia_levers.py` (NEXT 상수만 — 위 next-nav 병행)
- `manifest/mind.csv` (34행), `docs/mind/_meta.json` (34챕터+totals.words 33074)
- `THRESHOLD_LOGIC_INHERITANCE.md` (§18-19 자폐 DONE 표시, 잔여 1순위 §22 ADHD로 전진),
  `CHANGELOG.md`, `MASTER_MANUAL_START_HERE.md`(롤링 포인터 → v1.41)
- `build_search_layer.py` 재생성물: `docs/sitemap.xml`, `docs/llms.txt`(바이트-동일), `docs/llms-full.txt`,
  `docs/robots.txt`, 각 챕터의 answer/vp-card 주입 블록(멱등)
