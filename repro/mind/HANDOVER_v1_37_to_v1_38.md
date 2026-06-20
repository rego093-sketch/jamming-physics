# HANDOVER — v1.37 → v1.38  (문턱-이동 개입 논리 상속 + T2b-L 양극성 3-레버 §30 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.37의 성격 (로드맵 시퀀스에서의 분기).** v1.36이 E2+T2b를 닫은 뒤 로드맵 권장 다음은 T3a(중독)였으나,
> 이번 세션은 **사용자 지시**로 진통 패키지의 **문턱-이동 개입 논리(threshold-shift intervention logic)** 기술
> (Zenodo 10.5281/zenodo.20733420)을 **상속·능동 적용**하는 경로를 택했다. 이것은 질환 모듈이 아니라
> **횡단(cross-cutting) 개입 층**이며, 로드맵에 없던 것을 — 사용자가 의심한 그대로 — 새로 추가한 것이다.
> **T3a는 미실행으로 v1.38에 그대로 남는다.**

---

## 1. WHAT v1.37 DELIVERED (complete, 두 게이트 green)

동결 엔진 + 모든 기존 모듈을 READ-ONLY로 두고, **횡단 개입 층 1개를 상속**하고 그것을 **양극성에 능동 적용**해
모듈 4개 + 챕터 1개 + 거버넌스 3개를 add-only로 출판.

### 1.1 상속된 기술 (the LAYER, cross-cutting)

- **출처.** `analgesic_threshold_logic v2.0`, **Zenodo DOI 10.5281/zenodo.20733420** (통증 문턱, Na_V 위 검증).
- **핵심.** 증상 = 발화 문턱 넘기, 개입 = 문턱을 **위로** 이동. 손잡이 **정확히 3개**: **L1** 안쪽(흥분) 전류↓ ·
  **L2** 바깥쪽(K⁺) 전류↑ · **L3** 상류 민감화 구동 제거. mind 전체가 의존하는 **동일 R19 기질**
  (`ṡ = g·s − s³ + h`, spinodal fold = 스위칭 장벽) 위에서 작동 → **새 메커니즘·새 상수 0**.
- **상속 부품 6개.** 3-레버 프레임 · DNA γ 읽기(SantaLucia 1998 → |h_sp|=spinodal(γ), 엔진 READ-ONLY) ·
  부담-가중 **표적** 우선순위 · L3 정직성 게이트(fail-closed) · 금지-주장 스캐너(fail-closed) · 방화벽.
- **공식 등록.** `THRESHOLD_LOGIC_INHERITANCE.md` (상속 + 기존 사례 적용 계획) · 로드맵 **§2.5** 신설.

### 1.2 능동 적용 — 양극성 3-레버 (§30, the APPLICATION, BIP-T2b-L)

- **무엇을 메웠나.** §29 **B4**는 "안정제 부호 = 장벽 올리기"를 증명했지만 안정제를 **단일 추상 연산자**로 둠.
  §30은 그 연산자를 **3-레버 표적 지도**로 분해 (16개 양극성 흥분성 유전자):
  - **L1**(안쪽 흥분↓): CACNA1C(Ca_V1.2, #1 GWAS)·CACNA1D·CACNA1I·SCN2A·GRIN2A; **L1-인접** CACNB2·ANK3(#2 GWAS).
  - **L2**(바깥쪽 K⁺↑): KCNQ2·KCNQ3(M-전류 쌍)·KCNB1.
  - **L3**(상류 구동 제거 [O]): ARNTL(BMAL1)·CLOCK·PER2·NR3C1·CRHR1·GSK3B(리튬 표적).
- **DNA 접지.** 각 유전자 γ = −mean(NN 스태킹 ΔG)를 자기 프로모터 창(TSS−2000..+500)에서 읽어
  |h_sp|=spinodal(γ) 산출. **KCNQ2/KCNQ3는 진통 캐시에서 verbatim 재사용**(같은 유전자·같은 숫자).
- **방화벽 가시화.** 우선순위(CACNA1C #1)와 γ/|h_sp| 강성 순위(KCNQ2 #1)가 **분리** — γ는 맥락일 뿐 점수에 합산 안 됨.
- **4개 모듈 전부 PASS**, 2× sha256 동일. `run_all_atlas.py`에 **8번째 시민 BIP-T2b-L** 등록 → **ALL PASS 8/8**.

### 1.3 출판 표면 (SEO 챕터)

- **영어 전용 챕터 §30 「Bipolar threshold levers」** — `docs/mind/30-bipolar-threshold-levers/index.html`.
- 레지스터 lock `bipolar_threshold_levers`(check:None, framing) 추가, CITES=[자기, bipolar_state_switching],
  answer-first 56w, vp-card 2개. → **41 locks / 30 chapters**.
- §29 next-nav를 `<span>`에서 **§30으로 갱신**(역사 재작성 아님, 단순 링크). manifest 30행(words 1582) 추가,
  `_meta.json` 30챕터·totals.words 22740 갱신. `build_search_layer.py` 재생성(sitemap 31, llms 4989B<5KB).
- **`gate.py` PASS 138/138 (0 hard fail)** — 기존 134 + §30의 4개 신규 체크.

---

## 2. FROZEN HASHES (이것들로 검증 — 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine file** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **M0–16 subtree** (불변) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| §29 bipolar (불변) | `5c55c0e7b2815bac209ae777ae5106154f859bd641b1b63a84ef2e52cbbdd4be` |
| **§30 3-레버 지도** (NEW, 아틀라스 등록) | `a9f30d732c991bd64d3462e440f1cea34a630a4bcef695cce4370743b69fd0ef` |
| §30 L3 정직성 게이트 결과 (NEW) | `0a321b50eeead94da0a81dc063d8b1180e8a690d0da7aef10129b1f7f0fc8dae` |
| §30 금지-주장 스캔 결과 (NEW) | `87825c6b30053c139195c637f3ff2bfc5586410fd8bc4ac5c41379149954421e` |
| §30 부담 우선순위 결과 (NEW) | `6e7b769e438656d225788688fe7886e294cb830b7ce49afd17544c1aca1c2d01` |
| §30 프로모터 γ 캐시 (NEW) | `bbf14e17b87b133b8771faac57ab1149c3d9c000a457df43c63bc728bbf9a61e` |

> 아틀라스 등록 hash(`run_all_atlas.py` MODULES 상수)는 **지도 결과만**(`a9f30d73…`) 동결한다. 나머지 3개
> 모듈은 매 실행 자기 결과를 다시 쓰며 fail-closed PASS로 게이트된다.

---

## 3. GATE / REGRESSION STATUS

- **`gate.py` (출판/검색 층): PASS 138/138, 0 hard fail.** answer-first 30챕터(§30 56w) · vp-card 71 ·
  robots 7봇 · sitemap 31/31 · llms 4989B(<5KB) · 엔진 재현 · SSOT drift 0 · 본문 wordcount ±2% · 멱등.
- **`run_all_atlas.py` (아틀라스 재현/규율): ALL PASS 8/8.** SZ-DISC·SZ-DOM·EPI·E0-PLAS·DEP-T1b·
  E2-SWITCH·BIP-T2b·**BIP-T2b-L**. 14 CONFIRMED, 0 REFUTED, 엔진 byte-unchanged.

### 재현 방법 (패키지 루트에서)

```bash
# 1) 양극성 3-레버 4개 모듈 한 번에
python3 repro/mind/_verify/run_all_bipolar_levers.py        # → ALL PASS, map sha a9f30d73…

# 2) 아틀라스 전체(8모듈)
python3 repro/mind/_verify/run_all_atlas.py                 # → ALL PASS 8/8

# 3) 출판/검색 게이트
python3 tools/mind_registry.py        # 41 locks / 30 chapters, values match
python3 tools/build_search_layer.py   # answer/cards 주입 + sitemap/llms 재생성(멱등)
python3 tools/gate.py                 # → PASS 138/138, 0 hard fail
```

> γ 캐시(`bipolar_levers_promoters.cache.json`)가 동봉되어 NCBI 재-fetch 없이 결정론 재현된다. 캐시 없이
> 처음부터 받으려면 `fetch_bipolar_promoters.py` 패턴(TSS−2000..+500, eutils) 사용. ARNTL은 공식 심볼이
> 이제 BMAL1이라 **gene id 406**으로 fetch해야 한다.

---

## 4. THE FIREWALL (한 번 더 — YMYL/medical, 오독 방지)

프로모터 |h_sp|는 **유전자 자기 스위치 강성**일 뿐이다. **결코** 다음과 동일시하지 않는다: §29 네트워크
mood-switch 장벽 g · 채널 활성화 전압 · 약물 약효(potency) · 용량(dose) · 생체내 선택성 · 임상 효과.
모듈은 **표적만** 순위화(약물·용량 아님), γ는 구조적 맥락으로만 운반·점수에 합산 금지. 명명된 기분안정제
(L1의 Na-채널 차단 항경련제, L3의 리튬-GSK3B/일주기)는 **부호의 예시**일 뿐 권고가 아니다.
**efficacy=0 · NOT medical advice · consciousness_claim=0 · hard problem OPEN · 치료/진단/처방/완치 아님.**

---

## 5. v1.38 ENTRY POINTS (next session)

> **두 갈래가 열려 있다. 사용자 지시에 따라 택일.**

**A — 문턱-이동 논리를 기존 사례로 확장 (사용자 "기존 연구사례 적용" 계획의 실행).**
`THRESHOLD_LOGIC_INHERITANCE.md` §3의 우선순위표를 그대로 따른다. **권장 1순위: §25 뇌전증(T2a)** —
로드맵 T2a 산출물 정의("어느 개입이 over-sync 문턱을 올리는가")가 **문자 그대로 L1/L2 문턱-올리기**이고,
**KCNQ2/KCNQ3 γ 캐시를 재사용**할 수 있어 비용·결정론 모두 유리. 패턴: γ fetch(공유 유전자는 캐시 재사용) →
`epilepsy_threshold_levers.py` 3-레버 지도 → L3 게이트 → 금지-주장 스캐너 → 부담 우선순위 →
`run_all_atlas.py` 등록(9모듈) → 영어 챕터 §31. 이후 §27 우울(L3 지배) → §24 조현병 → §18-19 자폐(기존
multilever 통일) → §22 ADHD(부분 적합) 순.

**B — 로드맵 본래 다음, T3a 중독.** v1.36 핸드오버 §5-A가 상세. E0 가소성 위 민감화 핸들만 연결(E2 불요),
`from e0_plasticity import PlasticConnectome` import, M5-RPE 가치 신호를 READ-ONLY로 먼저 접지.
사전등록: 반복 노출이 보상 반응 단조 강화 · cue-반응성↑ · 소거가 흔적 0으로 못 돌림 · η=0 가드. 8→9모듈.
**문턱-이동 논리도 중독에 적용 가능**(L3 = 상류 보상/도파민 구동) — A와 B가 합쳐질 수 있다.

**규율 리마인더 (모든 v1.38 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, η=0/bias=0
가드로 자체 확인); (ii) 새 튜닝 상수 0(γ는 측정, |h_sp|·barrier는 엔진 함수); (iii) HTML 본문 English-only(C0);
(iv) llms.txt 챕터 추가 금지(<5KB 헤드룸 — 현재 4989B로 **여유 거의 없음**, 신규 챕터는 sitemap만); (v)
신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 방화벽 부착; (vi) 단일 zip(내부 폴더
`mind_pkg`); (vii) 변경 후 **두 게이트(`gate.py` 138+, `run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시
finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **재사용 우선**: 공유 유전자(SCN2A,
GRIN2A, KCNQ2/3, CACNA1C)는 γ 캐시 재사용.

---

## 6. 변경 파일 목록 (v1.37 add-only)

**신규:**
- `repro/mind/_verify/bipolar_threshold_levers.py` (+ `_results.json`, `expected_…sha256.json`)
- `repro/mind/_verify/bipolar_l3_honesty.py` (+ `_…json`)
- `repro/mind/_verify/bipolar_forbidden_claim_scan.py` (+ `bipolar_claim_scan.json`)
- `repro/mind/_verify/bipolar_burden_prioritisation.py` (+ `_…json`)
- `repro/mind/_verify/run_all_bipolar_levers.py`
- `repro/mind/_verify/bipolar_levers_promoters.cache.json`
- `docs/mind/30-bipolar-threshold-levers/index.html`
- `tools/_gen_ch30_bipolar_levers.py`
- `THRESHOLD_LOGIC_INHERITANCE.md`, `HANDOVER_v1_37_to_v1_38.md`

**수정(최소·add-only 성격):**
- `repro/mind/_verify/run_all_atlas.py` (MODULES에 BIP-T2b-L + docstring)
- `tools/mind_registry.py` (lock/CITES/ANSWERS 각 1개)
- `docs/mind/29-bipolar-state-switching/index.html` (next-nav 링크만)
- `manifest/mind.csv` (30행), `docs/mind/_meta.json` (30챕터+totals)
- `RESEARCH_ROADMAP_post_autism_adhd.md` (§2.5 신설), `CHANGELOG.md`, `MASTER_MANUAL_START_HERE.md`(롤링 포인터)
- `build_search_layer.py` 재생성물: `docs/sitemap.xml`, `docs/llms.txt`, `docs/llms-full.txt`, `docs/robots.txt`,
  각 챕터의 answer/vp-card 주입 블록(멱등)
