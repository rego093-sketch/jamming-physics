# HANDOVER — v1.38 → v1.39  (문턱-이동 논리 기존-사례 적용 · T2a-L 뇌전증 3-레버 §31 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.38의 성격 (v1.37 핸드오버 §5 갈래 중 A 선택).** v1.37이 문턱-이동 개입 논리를 상속하고 그것을 양극성(§30)에
> 능동 적용한 뒤, v1.37 핸드오버 §5는 두 갈래를 열어 두었다 — **A: 기존 사례로 확장(권장 1순위 §25 뇌전증)** vs
> B: 로드맵 본래 T3a 중독. 이번 세션은 **권장된 A**를 택했다. 뇌전증은 over-sync 문턱-올리기가 **문자 그대로**
> L1/L2 문턱-이동이고, **KCNQ2/KCNQ3 등 5개 γ를 양극성 캐시에서 재사용**할 수 있어 비용·결정론 모두 가장 유리한
> 첫 적용 대상이었다. **T3a 중독은 또 다시 미실행으로 v1.39에 남는다.**

---

## 1. WHAT v1.38 DELIVERED (complete, 두 게이트 green)

동결 엔진 + 모든 기존 모듈(§30 양극성 레버 포함)을 READ-ONLY로 두고, 상속된 **문턱-이동 개입 논리를 §25 뇌전증에
능동 적용**해 모듈 4개 + 챕터 1개 + 거버넌스를 add-only로 출판. **새 메커니즘·새 튜닝 상수 0.**

### 1.1 능동 적용 — 뇌전증 3-레버 (§31, the APPLICATION, EPI-T2a-L)

- **무엇을 메웠나.** §25는 발작 = 네트워크가 전역 순서변수 R 위에서 **over-synchronisation 문턱**을 넘는 것이고,
  교정 **부호**는 "문턱을 올리는 것"임을 증명했지만, 그 밀기를 **단일 추상 연산자**로 두었다. §31은 그 연산자를
  **3-레버 표적 지도**로 분해 (16개 뇌전증 흥분성 유전자, **동일 R19 기질** 위):
  - **L1**(안쪽 Na/Ca/NMDA 전류↓): SCN1A(Na_V1.1)·SCN2A·SCN8A·CACNA1A(Ca_V2.1)·CACNA1H(Ca_V3.2 T형)·GRIN2A.
  - **L2 (지배 레버)**(바깥쪽 K⁺↑): KCNQ2·KCNQ3(M-전류 쌍 = **레티가빈 표적**)·KCNB1·KCNA1·KCNT1; **L2-인접**
    억제성 GABA-A GABRG2·GABRA1. 양극성이 L1(칼슘 GWAS)에 기댄 것과 달리 뇌전증은 **L2가 지배** — 가장 투명한
    항경련 원리(M-전류 개방)가 L2이고 명명된 분자 선례(레티가빈)가 있기 때문.
  - **L3**(상류 mTOR 구동 제거 [O]): DEPDC5(GATOR1)·TSC1(hamartin)·TSC2(tuberin) = **에베로리무스 방향**.
- **DNA 접지.** 각 유전자 γ = −mean(NN 스태킹 ΔG, SantaLucia 1998)를 자기 프로모터 창(TSS−2000..+500)에서 읽어
  |h_sp|=spinodal(γ), barrier=γ²/4 산출(엔진 READ-ONLY). 범위: **CACNA1H가 최강성**(γ≈1.64, |h_sp|≈0.81) ~
  **SCN2A가 최연성**(γ≈1.20, |h_sp|≈0.50). **5개(KCNQ2·KCNQ3·KCNB1·SCN2A·GRIN2A)는 양극성 캐시에서
  verbatim 재사용**(γ는 가닥-대칭이라 바이트 동일).
- **정직한 caveat 2개 (숨기지 않고 기록).** (i) **KCNT1은 부호-역전** — 그 기능획득(GOF)이 병리이므로 일반 L2
  방향과 반대(선례 퀴니딘은 차단제); (ii) **L1 Na-차단 방향은 Dravet/SCN1A 기능상실에서 금기** — 바로 이것이 γ를
  **프로모터 구조 전용 [V]**(형질-무관)로 두고 임상 방향을 **[O]**로 분리하는 이유다.
- **방화벽 가시화(decoupling witness).** 우선순위(부담)와 γ/|h_sp| 강성 순위가 **분리** — **최강성 프로모터 CACNA1H가
  우선순위 하위**(rank 15), **최우선 표적 SCN1A가 최연성에 가까운 읽기**(|h_sp| 강성 순위 15위). γ가 점수를 몰았다면
  둘 다 그 자리에 못 있는다 = 방화벽이 눈에 보이게 만든 것.
- **4개 모듈 전부 PASS**, 2× sha256 동일(지도 sha `22879b69…`). `run_all_atlas.py`에 **9번째 시민 EPI-T2a-L**
  등록 → **ALL PASS 9/9**.

### 1.2 출판 표면 (SEO 챕터)

- **영어 전용 챕터 §31 「Epilepsy threshold levers」** — `docs/mind/31-epilepsy-threshold-levers/index.html`.
- 레지스터 lock `epilepsy_threshold_levers`(check:None, framing) 추가, CITES=[자기, **epilepsy_oversync**(§25)],
  answer-first 58w, vp-card 2개. → **42 locks / 31 chapters**.
- §30 next-nav를 `<span>`에서 **§31로 갱신**(역사 재작성 아님, 단순 링크). manifest 31행(words 2108) 추가,
  `_meta.json` 31챕터·totals.words 24848 갱신. `build_search_layer.py` 재생성(sitemap 32, **llms 4989B 그대로
  바이트-동일**<5KB — 신규 챕터는 sitemap만, 손-큐레이트 llms 슬러그 목록 불변).
- **`gate.py` PASS 142/142 (0 hard fail)** — 기존 138 + §31의 4개 신규 체크.

---

## 2. FROZEN HASHES (이것들로 검증 — 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine file** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **M0–16 subtree** (불변) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| §30 양극성 3-레버 지도 (불변, 아틀라스 등록) | `a9f30d732c991bd64d3462e440f1cea34a630a4bcef695cce4370743b69fd0ef` |
| **§31 3-레버 지도** (NEW, 아틀라스 등록) | `22879b696cf9226efc660acdea1f017a8018c3d1eb93f324f32da53dbfc14fcf` |
| §31 L3 정직성 게이트 결과 (NEW) | `24a32f614ce0937e34e3f1bdb23f2cbbd92eb275f1c78d20585c9f50bc492c4e` |
| §31 금지-주장 스캔 결과 (NEW) | `7f75ff5bbe0c0464fe38f01b83a52821de960a60995d4a42eb7146c40ee35de8` |
| §31 부담 우선순위 결과 (NEW) | `aba196f27e483144fd4b151789627aa38e36df5b9ff708e8f6207d2677cfe1da` |
| §31 프로모터 γ 캐시 (NEW) | `cf35e269c63a9319035e85f886e516cfde8a5bef9cb565157b9b5b45a6840dc4` |

> 아틀라스 등록 hash(`run_all_atlas.py` MODULES 상수)는 **지도 결과만**(`22879b69…`) 동결한다. 나머지 3개
> 모듈은 매 실행 자기 결과를 다시 쓰며 fail-closed PASS로 게이트된다.

---

## 3. GATE / REGRESSION STATUS

- **`gate.py` (출판/검색 층): PASS 142/142, 0 hard fail.** answer-first 31챕터(§31 58w) · vp-card 73 ·
  robots 7봇 · sitemap 32/32 · llms 4989B(<5KB) · 엔진 재현 · SSOT drift 0 · 본문 wordcount ±2% · 멱등.
- **`run_all_atlas.py` (아틀라스 재현/규율): ALL PASS 9/9.** SZ-DISC·SZ-DOM·EPI·E0-PLAS·DEP-T1b·
  E2-SWITCH·BIP-T2b·BIP-T2b-L·**EPI-T2a-L**. 14 CONFIRMED, 0 REFUTED, 엔진 byte-unchanged.

### 재현 방법 (패키지 루트에서)

```bash
# 1) 뇌전증 3-레버 4개 모듈 한 번에
python3 repro/mind/_verify/run_all_epilepsy_levers.py       # → ALL PASS, map sha 22879b69…

# 2) 아틀라스 전체(9모듈) — 각 모듈이 엔진 트리를 재-emerge하므로 ~6분 소요
python3 repro/mind/_verify/run_all_atlas.py                 # → ALL PASS 9/9

# 3) 출판/검색 게이트
python3 tools/mind_registry.py        # 42 locks / 31 chapters, values match
python3 tools/build_search_layer.py   # answer/cards 주입 + sitemap/llms 재생성(멱등)
python3 tools/gate.py                 # → PASS 142/142, 0 hard fail
```

> γ 캐시(`epilepsy_levers_promoters.cache.json`, 16유전자·각 2501bp)가 동봉되어 NCBI 재-fetch 없이 결정론
> 재현된다. 5개(KCNQ2·KCNQ3·KCNB1·SCN2A·GRIN2A)는 양극성 캐시 값과 바이트 동일. 캐시 없이 처음부터 받으려면
> eutils 윈도잉(strand에 따라 lo,hi = TSS−2000..+500, FASTA는 역상보 없이 결합 — γ 가닥-대칭) 사용.

---

## 4. THE FIREWALL (한 번 더 — YMYL/medical, 오독 방지)

프로모터 |h_sp|는 **유전자 자기 스위치 강성**일 뿐이다. **결코** 다음과 동일시하지 않는다: §25 네트워크
over-sync 문턱(R 위) · 채널 활성화 전압 · 약물 약효(potency) · 용량(dose) · 생체내 선택성 · 임상 효과.
모듈은 **표적만** 순위화(약물·용량 아님), γ는 구조적 맥락으로만 운반·점수에 합산 금지. 명명된 항경련 방향
(L1의 Na/T형 차단, L2의 레티가빈 M-전류 개방, L3의 에베로리무스 mTOR 억제)는 **부호의 예시**일 뿐 권고가 아니다.
기록된 caveat 2개(SCN1A Dravet 금기, KCNT1 부호-역전)는 일반 레버 부호가 임상 방향이 **아님**을 명시한다.
**efficacy=0 · NOT medical advice · consciousness_claim=0 · hard problem OPEN · 치료/진단/처방/완치 아님.**

---

## 5. v1.39 ENTRY POINTS (next session)

> **여전히 두 갈래. 사용자 지시에 따라 택일.** `THRESHOLD_LOGIC_INHERITANCE.md` §3의 우선순위표가 SSOT.

**A — 문턱-이동 논리를 다음 기존 사례로 확장 (권장 진행, §25 뇌전증 DONE 이후 1순위).**
우선순위표상 다음은 **§27 우울(depression)** — 진통/양극성/뇌전증이 모두 채널(L1/L2)에 무게를 둔 것과 달리
우울은 **L3 지배**(상류 HPA/모노아민/신경영양 구동 제거)라 레버 분포가 질적으로 다르고, 이는 프레임의 일반성을
보이는 좋은 다음 수다. 패턴 동일: γ fetch(공유 유전자 캐시 재사용 — SLC6A4/BDNF 등은 신규) →
`depression_threshold_levers.py` 3-레버 지도 → L3 정직성 게이트 → 금지-주장 스캐너(우울 어휘: "lifts depression",
"prevents relapse" 등 추가) → 부담 우선순위 → `run_all_atlas.py` 등록(**10모듈**) → 영어 챕터 §32. 이후 §24
조현병 → §18-19 자폐(기존 multilever 통일) → §22 ADHD(부분 적합) 순.

**B — 로드맵 본래 다음, T3a 중독 (두 번째 연기 중).** v1.36 핸드오버 §5-A가 상세. E0 가소성 위 민감화 핸들만
연결(E2 불요), `from e0_plasticity import PlasticConnectome`, M5-RPE 가치 신호를 READ-ONLY로 먼저 접지.
사전등록: 반복 노출이 보상 반응 단조 강화 · cue-반응성↑ · 소거가 흔적 0으로 못 돌림 · η=0 가드. 9→10모듈.
**문턱-이동 논리도 중독에 적용 가능**(L3 = 상류 보상/도파민 구동) — A의 우울 다음에 중독을 레버화하면 A와 B가
자연히 합쳐진다.

**규율 리마인더 (모든 v1.39 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, η=0/bias=0
가드로 자체 확인); (ii) 새 튜닝 상수 0(γ는 측정, |h_sp|·barrier는 엔진 함수 `spinodal(g)=2(g/3)^1.5`,
`barrier(g)=g²/4`); (iii) HTML 본문 English-only(C0); (iv) llms.txt 챕터 추가 금지(<5KB 헤드룸 — 현재 4989B로
**여유 거의 없음**, 신규 챕터는 sitemap만; `write_llms()`의 손-큐레이트 슬러그 목록을 건드리지 말 것); (v) 신규
챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 방화벽 부착; (vi) 단일 zip(내부 폴더
`mind_pkg`); (vii) 변경 후 **두 게이트(`gate.py` 142+, `run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시
finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **재사용 우선**: 공유 유전자(SCN2A,
GRIN2A, KCNQ2/3, KCNB1, CACNA1C)는 γ 캐시 재사용. **아틀라스 전체 재현은 ~6분** 걸리므로(모듈마다 엔진
재-emerge) 시간 예산 확보 — 백그라운드 `setsid` 실행 후 폴링 권장.

---

## 6. 변경 파일 목록 (v1.38 add-only)

**신규:**
- `repro/mind/_verify/epilepsy_threshold_levers.py` (+ `_results.json`, `expected_…sha256.json`)
- `repro/mind/_verify/epilepsy_l3_honesty.py` (+ `_…json`)
- `repro/mind/_verify/epilepsy_forbidden_claim_scan.py` (+ `epilepsy_claim_scan.json`)
- `repro/mind/_verify/epilepsy_burden_prioritisation.py` (+ `_…json`)
- `repro/mind/_verify/run_all_epilepsy_levers.py`
- `repro/mind/_verify/epilepsy_levers_promoters.cache.json`
- `docs/mind/31-epilepsy-threshold-levers/index.html`
- `tools/_gen_ch31_epilepsy_levers.py`
- `HANDOVER_v1_38_to_v1_39.md`

**수정(최소·add-only 성격):**
- `repro/mind/_verify/run_all_atlas.py` (MODULES에 EPI-T2a-L + docstring 문단)
- `tools/mind_registry.py` (lock/CITES/ANSWERS 각 1개)
- `tools/_gen_ch30_bipolar_levers.py` + `docs/mind/30-bipolar-threshold-levers/index.html` (next-nav 링크만)
- `manifest/mind.csv` (31행), `docs/mind/_meta.json` (31챕터+totals)
- `THRESHOLD_LOGIC_INHERITANCE.md` (§25 뇌전증 DONE 표시), `RESEARCH_ROADMAP_post_autism_adhd.md`,
  `CHANGELOG.md`, `MASTER_MANUAL_START_HERE.md`(롤링 포인터 → v1.38)
- `build_search_layer.py` 재생성물: `docs/sitemap.xml`, `docs/llms.txt`(바이트-동일), `docs/llms-full.txt`,
  `docs/robots.txt`, 각 챕터의 answer/vp-card 주입 블록(멱등)
