# HANDOVER — v1.40 → v1.41  (문턱-이동 논리 기존-사례 적용 · T1a-L 조현병 3-레버 §33 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.40의 성격 (v1.39 핸드오버 §5 갈래 중 A 선택, 연속).** v1.38→v1.39가 문턱-이동 논리를 §25 뇌전증·§27 우울에
> 적용한 데 이어, v1.39 핸드오버 §5는 다시 두 갈래를 열어 두었다 — **A: 기존 사례로 확장(권장 1순위 §24 조현병)** vs
> B: 로드맵 본래 T3a 중독. 이번 세션은 **권장된 A**를 택했다. 조현병은 §24의 **T-축이 이미 흥분 문턱**(E/I 균형)이라
> L1/L3 레버화가 자연스러웠고, **GRIN2A·CACNA1C·CACNB2를 양극성 캐시에서, GRIN2B·COMT·HTR2A·GABRA1을 우울 캐시에서
> 재사용**할 수 있어 비용·결정론 모두 유리했다. 그리고 조현병은 프레임에 **두 가지 첫 사례**를 안겼다 — **첫 L1+L3
> 공동-지배**이자 **첫 도메인-제한**. **T3a 중독은 네 번째로 미실행으로 v1.41에 남는다.**

---

## 1. WHAT v1.40 DELIVERED (complete, 두 게이트 green)

동결 엔진 + 모든 기존 모듈(§30 양극성·§31 뇌전증·§32 우울 레버 포함)을 READ-ONLY로 두고, 상속된 **문턱-이동 개입 논리를
§24 조현병에 능동 적용**해 모듈 4개 + 챕터 1개 + 거버넌스를 add-only로 출판. **새 메커니즘·새 튜닝 상수 0.**

### 1.1 능동 적용 — 조현병 3-레버 (§33, the APPLICATION, SZ-T1a-L) · **첫 L1+L3 공동-지배 & 첫 도메인-제한 사례**

- **무엇을 메웠나.** §24는 조현병 양성 증상 = **과점화(over-ignition)/이상-현저성** 작동점(발화 fold가 너무 낮아 약한
  내생 어셈블리가 환각·망상으로 점화)이고, 교정 **부호**는 "과잉 구동을 **감소**/fold를 올림"(뇌전증·양극성 조증과 같은
  방향)임을, 그리고 조현병이 **단일 축이 아니라 세 도메인**(양성/음성/인지)임을 증명했지만, 그 밀기를 **단일 추상
  연산자**로 두었다. §33은 그 연산자를 **3-레버 표적 지도**로 분해 (14개 조현병 유전자, **동일 R19 기질** 위):
  - **L1 (공동-지배, 6개)**(안쪽 글루타메이트/NMDA 전류) — GRIN1(obligate GluN1, 글리신-부위)·GRIN2A(공유, 공통+희귀
    변이 모두 증거)·GRIN2B·GRIA3(AMPA)·CACNA1C(공유, Ca_V1.2)·CACNB2(공유, β2 보조).
  - **L3 (공동-지배, 6개)**(상류 도파민 구동 = 항정신병 축) 세 하위-축: **(a) 수용체** DRD2(모든 인가 약물의 표적·GWAS
    유의)·DRD4(클로자핀 친화); **(b) 합성/수송** TH(선조체 도파민 합성능 상승=가장 재현된 영상 이상)·SLC6A3(DAT);
    **(c) 세로토닌성/이화** HTR2A(5-HT2A, 비단조)·COMT(전전두 Val158Met set-point).
  - **L2 (부차, 2개)**(바깥쪽 GABA-A 억제 전류) — GABRA1(α1, 우울 캐시 재사용)·GABRB3(β3, 15q11–13). PV 인터뉴런
    복원 경로(L1 부호-미묘와 같은 결핍).
- **새 구조적 발견 — 도메인-제한 (THE NEW FINDING).** 세 레버는 모두 단일 작동점에 대한 **스칼라** 연산자다. 이는 §24가
  정의한 **양성** 도메인(fold가 너무 낮음)에는 정확히 맞는 도구지만, 나머지 둘에는 **틀린** 도구다 — **음성**(출력/게인
  **결핍**)은 너무 **적은** 점화라 게인-감소 레버가 정반대로 밀고(결핍을 fold 낮춰 못 올림), **인지**(장거리 **배선**/
  dysconnection)는 **기하** 결함이라 스칼라 레버가 locality 불균형을 **정확히 불변**으로 둔다(문턱 이동은 §19 기하를
  재배선 못함). 따라서 레버 지도는 **양성 도메인에만, 양성 도메인만** 도달하고, 모듈은 이를 **도메인-제한 증거**로 기록
  (positive 도달=True, negative/cognitive 미도달=False; **축-구조이지 용량-구조 아님**). 이것이 상속 프레임이 만난
  **첫 부분-적용** 사례다 — 부분성을 정확히 포착하는 것이 세 도메인 모두 덮는 척하는 지도보다 더 정직하고 정보적이다.
- **레버 분포 — 첫 L1+L3 공동-지배.** 양극성=L1(칼슘 GWAS)·뇌전증=L2(KCNQ M-전류)·우울=L3(상류 HPA/모노아민/신경영양,
  L3-지배)와 달리 조현병은 **L1=6·L3=6 공동-지배**(L2=2) — 질환의 **두 주도 병태생리(글루타메이트 NMDA-저기능 + 도파민)**
  가 양성-도메인 교정을 **동시에** 끈다. 어느 한쪽도 종속이 아니다.
- **DNA 접지.** 각 유전자 γ = −mean(NN 스태킹 ΔG, SantaLucia 1998)를 자기 프로모터 창(TSS−2000..+500)에서 읽어
  |h_sp|=spinodal(γ), barrier=γ²/4 산출(엔진 READ-ONLY). 범위: **SLC6A3이 최강성**(γ≈1.60, |h_sp|≈0.78) ~
  **GABRA1이 최연성**(γ≈1.25, |h_sp|≈0.54); DRD4≈0.76·GRIN1≈0.76·TH≈0.73, 최우선 표적 **GRIN2A는 중간 0.69**,
  CACNA1C는 연성단 0.55. **7개(GRIN2A·CACNA1C·CACNB2=양극성 캐시, GRIN2B·COMT·HTR2A·GABRA1=우울 캐시)는 verbatim
  재사용**(γ는 가닥-대칭이라 바이트 동일). 나머지 7개(GRIN1·GRIA3·GABRB3·DRD2·DRD4·SLC6A3=disease 캐시, TH=ADHD
  캐시)도 **동일 TSS−2000..+500 창에서 바이트-동일**하게 가져와 NCBI 재-fetch 0.
- **정직한 caveat 2개 (숨기지 않고 기록).** (i) **L1 NMDA-저기능 방향은 부호-미묘** — 선도 모델은 PV 인터뉴런의 NMDA
  저기능이 하류 회로를 **탈억제**해 양성 증상이 반영하는 하류 **과점화**를 만든다, 그래서 **글리신-부위 작용제**(인터뉴런
  NMDA 기능을 올림) 방향이 naive 흥분-감소 부호와 **병존** — **우울 케타민 caveat의 조현병 유사물**; (ii) **HTR2A는
  비단조**. 바로 이것이 γ를 **프로모터 구조 전용 [V]**(형질-무관)로 두고 임상 방향을 **[O]**로 분리하는 이유다.
- **방화벽 가시화(decoupling witness).** 우선순위(부담)와 γ/|h_sp| 강성 순위가 **분리** — **최강성 프로모터 SLC6A3**
  (DAT, 깨끗한 방향 아님)이 **우선순위 하위**(rank 12/14)·비실행, **최우선 표적 GRIN2A는 중간 강성 읽기**(강성 순위
  6위). γ가 점수를 몰았다면 둘 다 그 자리에 못 있는다. 또한 **미충족-필요 가중이 글루타메이트 L1 축을 확립된 D2 경로
  위로** 올린다(D2는 이미 확립된 축이라 부담 최고·미충족 최저 → NMDA 경로가 더 높은-레버리지 미충족 방향으로 표면화;
  L1/L3 대칭을 미충족 축이 L1 쪽으로 깨뜨림). SLC6A3은 **DAT 차단이 도파민을 올려**(자극제 방향, 양성 악화) **역방향**
  이라 비실행으로 표시.
- **4개 모듈 전부 PASS**, 2× sha256 동일(지도 sha `8e0137bc…`). L3 정직성 게이트는 **L1+L3 공동-지배(L3-지배 아님)
  와 양성-도메인 제한까지 단언**. `run_all_atlas.py`에 **11번째 시민 SZ-T1a-L** 등록 → **ALL PASS 11/11**.

### 1.2 출판 표면 (SEO 챕터)

- **영어 전용 챕터 §33 「Schizophrenia threshold levers」** — `docs/mind/33-schizophrenia-threshold-levers/index.html`.
- 레지스터 lock `schizophrenia_threshold_levers`(check:None, framing) 추가, CITES=[자기, **schizophrenia_symptom_domains**(§24)],
  answer-first 60w, vp-card 2개. → **44 locks / 33 chapters**.
- §32 next-nav를 `<span>`에서 **§33으로 갱신**(역사 재작성 아님, 단순 링크). manifest 33행(words 2658) 추가,
  `_meta.json` 33챕터·totals.words 29935 갱신. `build_search_layer.py` 재생성(sitemap 34, **llms 4989B 그대로
  바이트-동일**<5KB — 신규 챕터는 sitemap만, 손-큐레이트 llms 슬러그 목록 불변).
- **`gate.py` PASS 150/150 (0 hard fail)** — 기존 146 + §33의 4개 신규 체크.

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
| **§33 조현병 3-레버 지도** (NEW, 아틀라스 등록) | `8e0137bccfe6dfe751af078a1e340accef578698992e569703865c6c27fe8c30` |
| §33 L3 정직성 게이트 결과 (NEW) | `a7938dc9b13c800ccb99f1bc188c2978c642dfbf37647caca8bcf46ec4339d85` |
| §33 금지-주장 스캔 결과 (NEW) | `4cfe2552ef509093fb663a9648d59a16855456170d1e71562360d05602c8933b` |
| §33 부담 우선순위 결과 (NEW) | `5285435ef23dfe35230d67710c4548636605fdf29b49f69a08ae9bc19567a500` |
| §33 프로모터 γ 캐시 (NEW, 14유전자) | `6af18b1cc2a667c0bcf7c86fa32323c0294958dcd40fb9067838a928ad534d24` |

> 아틀라스 등록 hash(`run_all_atlas.py` MODULES 상수)는 **지도 결과만**(`8e0137bc…`) 동결한다. 나머지 3개
> 모듈은 매 실행 자기 결과를 다시 쓰며 fail-closed PASS로 게이트된다.

---

## 3. GATE / REGRESSION STATUS

- **`gate.py` (출판/검색 층): PASS 150/150, 0 hard fail.** answer-first 33챕터(§33 60w) · vp-card 77 ·
  robots 7봇 · sitemap 34/34 · llms 4989B(<5KB) · 엔진 재현 · SSOT drift 0 · 본문 wordcount ±2% · 멱등.
- **`run_all_atlas.py` (아틀라스 재현/규율): ALL PASS 11/11.** SZ-DISC·SZ-DOM·EPI·E0-PLAS·DEP-T1b·
  E2-SWITCH·BIP-T2b·BIP-T2b-L·EPI-T2a-L·DEP-T1b-L·**SZ-T1a-L**. 14 CONFIRMED, 0 REFUTED, 엔진 byte-unchanged.

### 재현 방법 (패키지 루트에서)

```bash
# 1) 조현병 3-레버 4개 모듈 한 번에
python3 repro/mind/_verify/run_all_schizophrenia_levers.py  # → ALL PASS, map sha 8e0137bc…

# 2) 아틀라스 전체(11모듈) — 각 모듈이 엔진 트리를 재-emerge하므로 ~6분 소요
python3 repro/mind/_verify/run_all_atlas.py                 # → ALL PASS 11/11

# 3) 출판/검색 게이트
python3 tools/mind_registry.py        # 44 locks / 33 chapters, values match
python3 tools/build_search_layer.py   # answer/cards 주입 + sitemap/llms 재생성(멱등)
python3 tools/gate.py                 # → PASS 150/150, 0 hard fail
```

> γ 캐시(`schizophrenia_levers_promoters.cache.json`, 14유전자·각 2501bp)가 동봉되어 NCBI 재-fetch 없이 결정론
> 재현된다. 7개(GRIN2A·CACNA1C·CACNB2·GRIN2B·COMT·HTR2A·GABRA1)는 양극성/우울 캐시 값과 바이트 동일이고, 나머지
> 7개도 동일 윈도(disease/ADHD 캐시)에서 바이트 동일하게 받았다. 캐시 없이 처음부터 받으려면 eutils 윈도잉(strand에
> 따라 lo,hi = TSS−2000..+500, FASTA는 역상보 없이 결합 — γ 가닥-대칭) 사용.

---

## 4. THE FIREWALL (한 번 더 — YMYL/medical, 오독 방지)

프로모터 |h_sp|는 **유전자 자기 스위치 강성**일 뿐이다. **결코** 다음과 동일시하지 않는다: §24 네트워크 과점화 문턱
(over-ignition fold on R) · 수용체 점유 · 시냅스 도파민 농도 · 약물 약효(potency) · 용량(dose) · 생체내 선택성 ·
임상 효과. 모듈은 **표적만** 순위화(약물·용량 아님), γ는 구조적 맥락으로만 운반·점수에 합산 금지. 명명된 항정신병
방향(L3의 D2-길항 수용체 축·선조체 합성 축, L1의 글리신-부위/NMDA-강화[sign-subtle], 5-HT2A[비단조])은 **부호의
예시**일 뿐 권고가 아니다. 기록된 caveat 2개(L1 NMDA-저기능의 인터뉴런-탈억제 경로, HTR2A 비단조)는 일반 레버 부호가
임상 방향이 **아님**을 명시한다. 조현병은 **세 도메인**(양성/음성/인지, 별개 경과)이며 — 이 레버 지도가 명시적으로
**도달 못하는 두 도메인 포함** — 이질성은 **LOCKED**.
**efficacy=0 · NOT medical advice · consciousness_claim=0 · hard problem OPEN · 치료/진단/처방/완치 아님.**

---

## 5. v1.41 ENTRY POINTS (next session)

> **여전히 두 갈래. 사용자 지시에 따라 택일.** `THRESHOLD_LOGIC_INHERITANCE.md` §3의 우선순위표가 SSOT.

**A — 문턱-이동 논리를 다음 기존 사례로 확장 (권장 진행, §24 조현병 DONE 이후 1순위).**
우선순위표상 다음은 **§18–19 자폐(autism)** — 그런데 이 사례는 **특별**하다: 이미 `autism_multilever_threshold.py`
(§18-19)가 **다중-레버 문턱** 개념을 다루므로, 상속 작업은 **새 모듈을 처음부터 짓는 게 아니라** 기존 모듈을 **공식
L1/L2/L3 프레임 아래로 통일/재서술**하는 것이다. 자폐는 **L1 중심**(E/I 흥분 과잉 **축소**; SCN2A·GRIN2A 공유)이고
화학적 한계(§19)가 있어 **L3는 신중히 [O]**. 조현병·양극성과 **GRIN2A·CACNA1C γ 캐시 공유**. 핵심 주의: 자폐는 §19의
**화학 도달 한계** 결과가 있으므로(어떤 표적은 문턱 이동으로 도달 불가) 조현병의 **도메인-제한 패턴을 선례로** — 어떤
레버가 어떤 자폐 축에 도달하고 어떤 것은 못 하는지 정직하게 표시. 패턴 동일: γ(공유 캐시 재사용 + SHANK3/NRXN1/MECP2
등 신규) → `autism_threshold_levers.py`(또는 기존 multilever 재서술) 3-레버 통일 → L3 정직성 게이트 → 금지-주장
스캐너(자폐 어휘) → 부담 우선순위 → `run_all_atlas.py` 등록(**12모듈**) → 영어 챕터 §34. 이후 **§22 ADHD(L3 부분
적합 — 각성/게인 성격이라 L3만 선명, 정직하게 부분 적합 표시)**.

**B — 로드맵 본래 다음, T3a 중독 (네 번째 연기 중).** v1.36 핸드오버 §5-A가 상세. E0 가소성 위 민감화 핸들만
연결(E2 불요), `from e0_plasticity import PlasticConnectome`, M5-RPE 가치 신호를 READ-ONLY로 먼저 접지.
사전등록: 반복 노출이 보상 반응 단조 강화 · cue-반응성↑ · 소거가 흔적 0으로 못 돌림 · η=0 가드. 11→12모듈.
**문턱-이동 논리도 중독에 적용 가능**(L3 = 상류 보상/도파민 구동) — A의 자폐 이후 중독을 레버화하면 A와 B가
자연히 합쳐진다.

**규율 리마인더 (모든 v1.41 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, η=0/bias=0
가드로 자체 확인); (ii) 새 튜닝 상수 0(γ는 측정, |h_sp|·barrier는 엔진 함수 `spinodal(g)=2(g/3)^1.5`,
`barrier(g)=g²/4`); (iii) HTML 본문 English-only(C0); (iv) llms.txt 챕터 추가 금지(<5KB 헤드룸 — 현재 4989B로
**여유 거의 없음**, 신규 챕터는 sitemap만; `write_llms()`의 손-큐레이트 슬러그 목록을 건드리지 말 것); (v) 신규
챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 방화벽 부착; (vi) 단일 zip(내부 폴더
`mind_pkg`); (vii) 변경 후 **두 게이트(`gate.py` 150+, `run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시
finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **재사용 우선**: 공유 유전자(GRIN2A,
CACNA1C, CACNB2, GRIN2B, SCN2A, KCNQ2/3, NR3C1, CRHR1)는 γ 캐시 재사용. **아틀라스 전체 재현은 ~6분** 걸리므로
(모듈마다 엔진 재-emerge) 시간 예산 확보 — 백그라운드 `setsid` 실행 후 폴링 권장. **자폐는 기존 multilever 모듈이
있으므로** 새로 짓기 전에 `autism_multilever_threshold.py`를 먼저 읽고 통일 전략을 정할 것.

---

## 6. 변경 파일 목록 (v1.40 add-only)

**신규:**
- `repro/mind/_verify/schizophrenia_threshold_levers.py` (+ `_results.json`, `expected_…sha256.json`)
- `repro/mind/_verify/schizophrenia_l3_honesty.py` (+ `schizophrenia_l3_honesty.json`)
- `repro/mind/_verify/schizophrenia_forbidden_claim_scan.py` (+ `schizophrenia_claim_scan.json`)
- `repro/mind/_verify/schizophrenia_burden_prioritisation.py` (+ `schizophrenia_burden_prioritisation.json`)
- `repro/mind/_verify/run_all_schizophrenia_levers.py`
- `repro/mind/_verify/schizophrenia_levers_promoters.cache.json`
- `docs/mind/33-schizophrenia-threshold-levers/index.html`
- `tools/_gen_ch33_schizophrenia_levers.py`
- `HANDOVER_v1_40_to_v1_41.md`

**수정(최소·add-only 성격):**
- `repro/mind/_verify/run_all_atlas.py` (MODULES에 SZ-T1a-L + docstring 문단)
- `tools/mind_registry.py` (lock/CITES/ANSWERS 각 1개)
- `docs/mind/32-depression-threshold-levers/index.html` (next-nav 링크만)
- `tools/_gen_ch32_depression_levers.py` (NEXT 상수만 — 위 next-nav 병행)
- `manifest/mind.csv` (33행), `docs/mind/_meta.json` (33챕터+totals)
- `THRESHOLD_LOGIC_INHERITANCE.md` (§24 조현병 DONE 표시, 잔여 1순위 §18-19 자폐로 전진),
  `CHANGELOG.md`, `MASTER_MANUAL_START_HERE.md`(롤링 포인터 → v1.40)
- `build_search_layer.py` 재생성물: `docs/sitemap.xml`, `docs/llms.txt`(바이트-동일), `docs/llms-full.txt`,
  `docs/robots.txt`, 각 챕터의 answer/vp-card 주입 블록(멱등)
