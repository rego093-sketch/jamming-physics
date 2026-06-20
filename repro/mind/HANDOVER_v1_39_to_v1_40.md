# HANDOVER — v1.39 → v1.40  (문턱-이동 논리 기존-사례 적용 · T1b-L 우울 3-레버 §32 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.39의 성격 (v1.38 핸드오버 §5 갈래 중 A 선택, 연속).** v1.38이 문턱-이동 논리를 §25 뇌전증에 적용한 데 이어,
> v1.38 핸드오버 §5는 다시 두 갈래를 열어 두었다 — **A: 기존 사례로 확장(권장 1순위 §27 우울)** vs B: 로드맵 본래
> T3a 중독. 이번 세션은 **권장된 A**를 택했다. 우울은 진통/양극성/뇌전증이 모두 채널(L1/L2)에 무게를 둔 것과 달리
> **L3 지배**(상류 HPA/모노아민/신경영양 구동)라 프레임의 일반성을 진짜로 시험하는 첫 사례였고, **NR3C1/CRHR1/GRIN2A/
> CACNA1C/KCNQ2/KCNQ3 6개 γ를 양극성 캐시에서, GABRA1을 뇌전증 캐시에서 재사용**할 수 있어 비용·결정론 모두 유리했다.
> **T3a 중독은 세 번째로 미실행으로 v1.40에 남는다.**

---

## 1. WHAT v1.39 DELIVERED (complete, 두 게이트 green)

동결 엔진 + 모든 기존 모듈(§30 양극성·§31 뇌전증 레버 포함)을 READ-ONLY로 두고, 상속된 **문턱-이동 개입 논리를 §27
우울에 능동 적용**해 모듈 4개 + 챕터 1개 + 거버넌스를 add-only로 출판. **새 메커니즘·새 튜닝 상수 0.**

### 1.1 능동 적용 — 우울 3-레버 (§32, the APPLICATION, DEP-T1b-L) · **첫 L3-지배 사례**

- **무엇을 메웠나.** §27은 주요우울 = 저-협응 작동점의 **만성화**(지속 HPA-구동 철수가 전역 순서변수 R을 health
  **아래로** 내리고 가소성이 그 이탈을 구조 흔적으로 굳힘)이고, 교정 **부호**는 "결핍 구동을 **복원**"하는 것임을
  증명했지만, 그 밀기를 **단일 추상 연산자**로 두었다. §32는 그 연산자를 **3-레버 표적 지도**로 분해 (18개 우울
  유전자, **동일 R19 기질** 위):
  - **L3 (지배 레버, 18개 중 12개)** — 상류 구동을 바꾼다. 세 하위-축으로 깨끗이 갈린다:
    - **(a) HPA 제거**: NR3C1(글루코코르티코이드 수용체; 방향 = **음성 피드백 복원**→스트레스 과구동 제거)·CRHR1·FKBP5.
    - **(b) 모노아민 복원**: SLC6A4(세로토닌 수송체, SSRI 자리)·SLC6A2(노르에피네프린 수송체, SNRI 자리)·
      MAOA(MAOI 자리)·COMT·TPH2(세로토닌 합성 율속)·HTR1A·HTR2A.
    - **(c) 신경영양 복원**: BDNF·NTRK2(TrkB) = **속효성(글루타메이트) 경로와 모노아민 경로의 수렴점** — 부담
      우선순위 최상위가 되는 이유.
  - **L1 (부차, 3개)**(안쪽 글루타메이트/Ca 전류): GRIN2A·GRIN2B·CACNA1C.
  - **L2 (부차, 3개)**(바깥쪽 K⁺/GABA-A): KCNQ2·KCNQ3(M-전류)·GABRA1(α1, L2-인접). 뇌전증에서 **지배**였던
    바로 그 KCNQ2/3가 우울에서는 주변부 — 우울의 무게중심이 발화-문턱이 아니라 상류에 있다는 분포 발견의 핵심.
- **질환-수준 부호 역전 (명시, 은폐 안 함).** 뇌전증/양극성 조증은 health **위**(레버 부호 = 과잉 **감소**)지만,
  우울은 health **아래**(레버 부호 = 결핍 **복원** / 만성 철수 구동 제거) — 3개 추상 레버는 그대로, **방향이 거울**.
- **DNA 접지.** 각 유전자 γ = −mean(NN 스태킹 ΔG, SantaLucia 1998)를 자기 프로모터 창(TSS−2000..+500)에서 읽어
  |h_sp|=spinodal(γ), barrier=γ²/4 산출(엔진 READ-ONLY). 범위: **KCNQ2가 최강성**(γ≈1.58, |h_sp|≈0.76) ~
  **GABRA1이 최연성**(γ≈1.25, |h_sp|≈0.54); HPA의 CRHR1≈0.75·SLC6A4≈0.72, BDNF는 중간 0.66, NR3C1은 연성단
  0.55. **7개(NR3C1·CRHR1·GRIN2A·CACNA1C·KCNQ2·KCNQ3=양극성 캐시, GABRA1=뇌전증 캐시)는 verbatim 재사용**
  (γ는 가닥-대칭이라 바이트 동일). 신규 fetch 11개(FKBP5·SLC6A4·SLC6A2·MAOA·TPH2·HTR1A·HTR2A·COMT·BDNF·NTRK2·GRIN2B).
- **정직한 caveat 2개 (숨기지 않고 기록).** (i) **L1 글루타메이트 방향은 NMDA 길항제**(케타민/에스케타민)가
  **하류 BDNF/TrkB** 신호를 경유해 작동 — **흥분 감소가 아님** → naive L1 부호를 sign-subtle로 표시; (ii) **HTR2A는
  비단조** — 작용제(사이키델릭) 경로와 길항제 경로가 둘 다 문헌에 출현 → 단일 부호 레버로 못 담음. 바로 이것이 γ를
  **프로모터 구조 전용 [V]**(형질-무관)로 두고 임상 방향을 **[O]**로 분리하는 이유다.
- **방화벽 가시화(decoupling witness).** 우선순위(부담)와 γ/|h_sp| 강성 순위가 **분리** — **최강성 프로모터 KCNQ2**(부차
  탐색적 L2)가 **우선순위 하위**(rank 17/18)·비실행, **최우선 표적 BDNF는 중간 강성 읽기**(강성 순위 10위). γ가 점수를
  몰았다면 둘 다 그 자리에 못 있는다 = 방화벽이 눈에 보이게 만든 것. 또한 미충족 수요 가중이 상류 HPA/신경영양/글루타메이트
  표적을 잘-처리된 모노아민 수송체(SLC6A4 등) 위로 올린다.
- **4개 모듈 전부 PASS**, 2× sha256 동일(지도 sha `d07aab40…`). L3 정직성 게이트는 **L3 지배(L1·L2보다 많음)까지
  단언**. `run_all_atlas.py`에 **10번째 시민 DEP-T1b-L** 등록 → **ALL PASS 10/10**.

### 1.2 출판 표면 (SEO 챕터)

- **영어 전용 챕터 §32 「Depression threshold levers」** — `docs/mind/32-depression-threshold-levers/index.html`.
- 레지스터 lock `depression_threshold_levers`(check:None, framing) 추가, CITES=[자기, **depression_chronification**(§27)],
  answer-first 60w, vp-card 2개. → **43 locks / 32 chapters**.
- §31 next-nav를 `<span>`에서 **§32로 갱신**(역사 재작성 아님, 단순 링크). manifest 32행(words 2429) 추가,
  `_meta.json` 32챕터·totals.words 27277 갱신. `build_search_layer.py` 재생성(sitemap 33, **llms 4989B 그대로
  바이트-동일**<5KB — 신규 챕터는 sitemap만, 손-큐레이트 llms 슬러그 목록 불변).
- **`gate.py` PASS 146/146 (0 hard fail)** — 기존 142 + §32의 4개 신규 체크.

---

## 2. FROZEN HASHES (이것들로 검증 — 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine file** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **M0–16 subtree** (불변) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| §30 양극성 3-레버 지도 (불변, 아틀라스 등록) | `a9f30d732c991bd64d3462e440f1cea34a630a4bcef695cce4370743b69fd0ef` |
| §31 뇌전증 3-레버 지도 (불변, 아틀라스 등록) | `22879b696cf9226efc660acdea1f017a8018c3d1eb93f324f32da53dbfc14fcf` |
| **§32 우울 3-레버 지도** (NEW, 아틀라스 등록) | `d07aab40ba56ee5dd234d65ee8691ac80458a9c71b6355bacfccbd1efdb69f30` |
| §32 L3 정직성 게이트 결과 (NEW) | `fa4bd6f84839be6b20f6ab974a08b1af59ac92ac29c5bafc337b93bcc53cb9b4` |
| §32 금지-주장 스캔 결과 (NEW) | `5c2586e098399044ee7cded44f441efe3fb1ca49b03c1757ac0873993b05b9b9` |
| §32 부담 우선순위 결과 (NEW) | `36f3cdb6b25252a7040d831230d7970ca7e79e8e0e23d29ba794ee73ef813088` |
| §32 프로모터 γ 캐시 (NEW, 18유전자) | `f635f3e5650e68d9fa417f8c306264e9b0a9da9f563532fa3d0a1ec4519594ff` |

> 아틀라스 등록 hash(`run_all_atlas.py` MODULES 상수)는 **지도 결과만**(`d07aab40…`) 동결한다. 나머지 3개
> 모듈은 매 실행 자기 결과를 다시 쓰며 fail-closed PASS로 게이트된다.

---

## 3. GATE / REGRESSION STATUS

- **`gate.py` (출판/검색 층): PASS 146/146, 0 hard fail.** answer-first 32챕터(§32 60w) · vp-card 75 ·
  robots 7봇 · sitemap 33/33 · llms 4989B(<5KB) · 엔진 재현 · SSOT drift 0 · 본문 wordcount ±2% · 멱등.
- **`run_all_atlas.py` (아틀라스 재현/규율): ALL PASS 10/10.** SZ-DISC·SZ-DOM·EPI·E0-PLAS·DEP-T1b·
  E2-SWITCH·BIP-T2b·BIP-T2b-L·EPI-T2a-L·**DEP-T1b-L**. 14 CONFIRMED, 0 REFUTED, 엔진 byte-unchanged.

### 재현 방법 (패키지 루트에서)

```bash
# 1) 우울 3-레버 4개 모듈 한 번에
python3 repro/mind/_verify/run_all_depression_levers.py     # → ALL PASS, map sha d07aab40…

# 2) 아틀라스 전체(10모듈) — 각 모듈이 엔진 트리를 재-emerge하므로 ~6분 소요
python3 repro/mind/_verify/run_all_atlas.py                 # → ALL PASS 10/10

# 3) 출판/검색 게이트
python3 tools/mind_registry.py        # 43 locks / 32 chapters, values match
python3 tools/build_search_layer.py   # answer/cards 주입 + sitemap/llms 재생성(멱등)
python3 tools/gate.py                 # → PASS 146/146, 0 hard fail
```

> γ 캐시(`depression_levers_promoters.cache.json`, 18유전자·각 2501bp)가 동봉되어 NCBI 재-fetch 없이 결정론
> 재현된다. 7개(NR3C1·CRHR1·GRIN2A·CACNA1C·KCNQ2·KCNQ3·GABRA1)는 양극성/뇌전증 캐시 값과 바이트 동일.
> 캐시 없이 처음부터 받으려면 eutils 윈도잉(strand에 따라 lo,hi = TSS−2000..+500, FASTA는 역상보 없이 결합 —
> γ 가닥-대칭) 사용.

---

## 4. THE FIREWALL (한 번 더 — YMYL/medical, 오독 방지)

프로모터 |h_sp|는 **유전자 자기 스위치 강성**일 뿐이다. **결코** 다음과 동일시하지 않는다: §27 네트워크 작동점
(coordination level R) · 수용체 점유 · 시냅스 모노아민 농도 · 약물 약효(potency) · 용량(dose) · 생체내 선택성 ·
임상 효과. 모듈은 **표적만** 순위화(약물·용량 아님), γ는 구조적 맥락으로만 운반·점수에 합산 금지. 명명된 항우울
방향(L3의 SSRI/SNRI/MAOI·글루코코르티코이드/CRH 경로, L1의 케타민[sign-subtle], L2의 M-전류 개방)은 **부호의
예시**일 뿐 권고가 아니다. 기록된 caveat 2개(L1 NMDA 길항제의 하류-BDNF 경로, HTR2A 비단조)는 일반 레버 부호가
임상 방향이 **아님**을 명시한다. 우울 이질성(melancholic/atypical/psychotic/peripartum/seasonal/양극성 우울;
모노아민/HPA/염증/일주기/심리사회 기여; ~30% 치료저항)은 **LOCKED**.
**efficacy=0 · NOT medical advice · consciousness_claim=0 · hard problem OPEN · 치료/진단/처방/완치 아님.**

---

## 5. v1.40 ENTRY POINTS (next session)

> **여전히 두 갈래. 사용자 지시에 따라 택일.** `THRESHOLD_LOGIC_INHERITANCE.md` §3의 우선순위표가 SSOT.

**A — 문턱-이동 논리를 다음 기존 사례로 확장 (권장 진행, §27 우울 DONE 이후 1순위).**
우선순위표상 다음은 **§24 조현병(schizophrenia)** — §24의 **T-축이 이미 흥분 문턱**(E/I 균형)이라 L1/L3 레버화가
자연스럽다(탈억제 bias가 fold 내림 = 이상 현저성). 양극성/우울과 **GRIN2A·CACNA1C γ 캐시 공유**. 단, 조현병은
**양성/음성/인지 도메인 분리**가 본질이므로(§24가 이미 도메인 축 지도 보유), 레버 지도를 도메인-인지된 방식으로
구성하는 것이 핵심 — gain-감소 항정신병약이 양성만 역전하고 D2 차단이 음성/인지에 못 미치는 axis-구조적 이유를
3-레버로 재서술. 패턴 동일: γ fetch(공유 유전자 캐시 재사용 — DRD2/GRIN2B/일부 신규) →
`schizophrenia_threshold_levers.py` 3-레버 지도 → L3 정직성 게이트 → 금지-주장 스캐너(조현병 어휘 추가) →
부담 우선순위 → `run_all_atlas.py` 등록(**11모듈**) → 영어 챕터 §33. 이후 §18-19 자폐(기존 multilever 통일) →
§22 ADHD(부분 적합) 순.

**B — 로드맵 본래 다음, T3a 중독 (세 번째 연기 중).** v1.36 핸드오버 §5-A가 상세. E0 가소성 위 민감화 핸들만
연결(E2 불요), `from e0_plasticity import PlasticConnectome`, M5-RPE 가치 신호를 READ-ONLY로 먼저 접지.
사전등록: 반복 노출이 보상 반응 단조 강화 · cue-반응성↑ · 소거가 흔적 0으로 못 돌림 · η=0 가드. 10→11모듈.
**문턱-이동 논리도 중독에 적용 가능**(L3 = 상류 보상/도파민 구동) — A의 조현병 이후 중독을 레버화하면 A와 B가
자연히 합쳐진다.

**규율 리마인더 (모든 v1.40 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, η=0/bias=0
가드로 자체 확인); (ii) 새 튜닝 상수 0(γ는 측정, |h_sp|·barrier는 엔진 함수 `spinodal(g)=2(g/3)^1.5`,
`barrier(g)=g²/4`); (iii) HTML 본문 English-only(C0); (iv) llms.txt 챕터 추가 금지(<5KB 헤드룸 — 현재 4989B로
**여유 거의 없음**, 신규 챕터는 sitemap만; `write_llms()`의 손-큐레이트 슬러그 목록을 건드리지 말 것); (v) 신규
챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 방화벽 부착; (vi) 단일 zip(내부 폴더
`mind_pkg`); (vii) 변경 후 **두 게이트(`gate.py` 146+, `run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시
finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **재사용 우선**: 공유 유전자(GRIN2A,
GRIN2B, CACNA1C, KCNQ2/3, NR3C1, CRHR1)는 γ 캐시 재사용. **아틀라스 전체 재현은 ~6분** 걸리므로(모듈마다 엔진
재-emerge) 시간 예산 확보 — 백그라운드 `setsid` 실행 후 폴링 권장.

---

## 6. 변경 파일 목록 (v1.39 add-only)

**신규:**
- `repro/mind/_verify/depression_threshold_levers.py` (+ `_results.json`, `expected_…sha256.json`)
- `repro/mind/_verify/depression_l3_honesty.py` (+ `depression_l3_honesty.json`)
- `repro/mind/_verify/depression_forbidden_claim_scan.py` (+ `depression_claim_scan.json`)
- `repro/mind/_verify/depression_burden_prioritisation.py` (+ `depression_burden_prioritisation.json`)
- `repro/mind/_verify/run_all_depression_levers.py`
- `repro/mind/_verify/depression_levers_promoters.cache.json`
- `docs/mind/32-depression-threshold-levers/index.html`
- `tools/_gen_ch32_depression_levers.py`
- `HANDOVER_v1_39_to_v1_40.md`

**수정(최소·add-only 성격):**
- `repro/mind/_verify/run_all_atlas.py` (MODULES에 DEP-T1b-L + docstring 문단)
- `tools/mind_registry.py` (lock/CITES/ANSWERS 각 1개)
- `docs/mind/31-epilepsy-threshold-levers/index.html` (next-nav 링크만)
- `manifest/mind.csv` (32행), `docs/mind/_meta.json` (32챕터+totals)
- `THRESHOLD_LOGIC_INHERITANCE.md` (§27 우울 DONE 표시, 잔여 1순위 §24로 전진),
  `CHANGELOG.md`, `MASTER_MANUAL_START_HERE.md`(롤링 포인터 → v1.39)
- `build_search_layer.py` 재생성물: `docs/sitemap.xml`, `docs/llms.txt`(바이트-동일), `docs/llms-full.txt`,
  `docs/robots.txt`, 각 챕터의 answer/vp-card 주입 블록(멱등)
