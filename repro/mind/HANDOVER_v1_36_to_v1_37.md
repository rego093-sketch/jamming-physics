# HANDOVER — v1.36 → v1.37  (E2 상태-스위칭 층 §28 + T2b 양극성 §29 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33에서 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`, 동봉)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 전체 사명·축 정의·로드맵 매핑·상태표는 **`MISSION_atlas_redefinition.md`** 가 SSOT.

> **v1.36의 성격.** 로드맵 시퀀스 T1a→T2a→E0→T1b→**E2→T2b**에서 **E2(상태-스위칭 층)** 와 **T2b(양극성)** 를 닫았다.
> E0가 **느린** 구조 변수(가소성 흔적)를 줬다면, E2는 **빠른** 변수 — 스위치하고 **그대로 머무는** 상태. 핵심 = **새 기계장치 0**:
> 동결 엔진에 처음부터 있던 **R19 셀** `ṡ = g·s − s³ + h`(전 프레임워크가 의존하는 supercritical pitchfork)를 모든 이전 챕터는
> **한 순간**에 읽었고, 이 증분은 **시간에 걸쳐** 읽는다. 새 방정식·새 상수·새 측정 0. T2b는 **두 층(E2+E0)을 import**해서
> 양극성을 한 valence 축의 두 극으로 전개 — 새 메커니즘 0. (`from e2_state_switching import BistableSwitch` +
> `from e0_plasticity import PlasticConnectome`.)

---

## 1. WHAT v1.36 DELIVERED (complete, all gates green)

**동결 엔진 + E0 층을 READ-ONLY로 두고**, 빠른 스위칭 층 1개와 그 위의 양극성 질환 1개를 챕터 2개·모듈 2개로 add-only 출판.

### E2 — 상태-스위칭 층 (§28, the LAYER)

- **핵심 (새 기계장치 0).** R19 셀 `ṡ = g·s − s³ + h`(g>0에서 bistable)를 **시간에 걸쳐** 읽음. g=1.0 보편 R19 스케일,
  fold = 엔진 자신의 `spinodal(g) = 2(g/3)^1.5`, 모든 grid는 swept stimulus probe(anti-tuning). **새 방정식/상수 0.**

- **§28 「The state-switching layer — the R19 bistable cell read over time」 (model).** 4개 사전등록 + 가드:
  - **E2.1 히스테리시스** — 장을 올렸다 내리면 상승/하강 전이가 0 반대편(grid h_up=+0.39, h_dn=−0.39), 폭 `2·spinodal≈0.77`
    루프(fold 두 배로 예측, 측정이 sweep step 이내 일치). 스위치된 상태는 되돌리기 저항. (CONFIRMED.)
  - **E2.2 발작 시간경과 (§25 빚 청산)** — latency가 fold 접근 시 **발산**(critical slowing), fold 초과 시 단조 하강
    (73.4→1.36). 작은 overshoot=느린 run-up, 큰 overshoot=급격 점프 = 정성적 발작 시간경과. **§25 ictal time-course
    CLOSED**(closes-25=True). (CONFIRMED.)
  - **E2.3 장벽 = 스위칭 임계** — spinodal(g)가 우물 깊이에 단조 증가(0.18@0.6→0.64@1.4), 얕은 우물 flip·깊은 우물 hold.
    장벽을 올리는 핸들이 스위칭 임계를 올림(stabiliser 부호). (CONFIRMED.)
  - **E2.4 엔진-불변 가드** — const-drive 적분이 엔진 `settle`을 **bit-for-bit** 재현, fold는 엔진 `spinodal`에서 읽음.
    sweep 끄면 동결 엔진 정확히 복구. 순수 add-on.

### T2b — 양극성 (§29, the APPLICATION)

- **핸들 (접지, 발명 아님).** M17 valence = approach(DA 극)/avoid(M18 코르티솔 위축 극)가 단일 차원. 조증=approach 고구동,
  울증=위축 저구동, euthymia=사이의 건강 점. 각 극을 SZ/뇌전증/우울과 **동일** 맵 `k=κ/(1−|b|)`[approach]/`κ/(1+|b|)`[위축]
  cap `2κ`로 매핑 — **새 상수 0**, 모든 부호 severity sweep 유지.

- **§29 「Bipolar disorder — two poles on one valence axis」 (model).** 5개 사전등록 + 가드:
  - **B1 두 극** — approach R=0.422>health 0.390>위축 R=0.367, 순서 `depressive<euthymic<manic` 단조. 두 질병 아닌
    한 축 두 여행. (CONFIRMED.)
  - **B2 삽화 = bistable 전이** — E2 히스테리시스(루프 0.77)+latency(31.6→1.9) 상속, 한 fold 진입·반대 fold 이탈
    (유발인 제거에 지속), critical slowing=prodrome. (CONFIRMED.)
  - **B3 kindling = E0 흔적 축적** — 교대 조증/울증 삽화가 보존 흔적 단조 심화(‖ΔW‖ 0.06→0.11→0.17→0.22→0.27→0.33,
    η sweep 전체), 깊은 흔적이 장벽 낮춤→후속 스위치 더 적은 구동. 역사가 다음 삽화를 쉽게. (CONFIRMED.)
  - **B4 안정제 부호 = 장벽 올리기** — 우물 깊이 올림→flip 임계 동반 상승(0.38→0.44→0.51→0.64), 조증·울증 둘 다 진입
    어렵게(kindling의 직접 짝). 부호만, medium_efficacy_tested=0. (CONFIRMED.)
  - **B5 두 층 import 가드** — η=0/bias 없음이 동결 M9 anchor `R=0.38961455156044245` **bit-for-bit** 재현·W 동일·정적
    극한 settle 일치. **`BistableSwitch`+`PlasticConnectome` import**(reuses E2/E0=1.0/1.0), 제3 메커니즘 0.

- **신규 재현 코드 2개(add-only).**
  - `repro/mind/_verify/e2_state_switching.py` → `e2_state_switching_results.json` sha256 `47c35e06…`(2× 결정론).
    재사용 `BistableSwitch` 클래스(`.spinodal/.settle_static/.relax/.crossing_latency`) export, E2.1–E2.4 사전등록 +
    closes-25 가드 + 엔진 불변 가드(E.emerge_all() READ-ONLY 후 tree 불변).
  - `repro/mind/_verify/bipolar_state_switching.py` → `bipolar_state_switching_results.json` sha256 `5c55c0e7…`(2× 결정론).
    **`BistableSwitch`와 `PlasticConnectome` 둘 다 import**(규칙 재유도 없음), valence 핸들을 M17/M18에서 READ-ONLY 접지,
    B1–B5 사전등록 + reuses-E2/E0 가드 + 엔진 불변 가드. `run_all_atlas.py`에 E2-SWITCH·BIP-T2b 등록 → **ALL PASS 7/7**.

- **신규 LOCK 2개**(framing, `check:None`): `state_switching`(canonical §28, §25 빚 청산 명시)·`bipolar_state_switching`
  (canonical §29). **v1.35 선례로 동결 `epilepsy_oversync` lock은 미수정**(빚 청산은 신규 lock이 발표, 옛 lock의 "owed to E2"
  framing 보존 — 역사 재작성 금지). 레지스터 **40 locks / 29 chapters**.

- **거버넌스.** `CHANGELOG.md`·`MASTER_MANUAL_START_HERE.md`(§4 롤링 포인터 v1.36)·`MISSION_atlas_redefinition.md`
  (상태표 E2·T2b→DONE·T3a→NEXT) v1.36 갱신 · hub Part II(arc list+toc+intro) §28·§29 확장 · nav 연결 §27→§28→§29
  (§27 next-nav를 `<span>`에서 §28로 갱신·bipolar "owed" 전방참조를 "§28–§29 전달"로 정정, §27 본문 1053w로 재조정) ·
  manifest/mind.csv 28·29행(words 1111·1229) · `_meta.json` 보강(누락됐던 §27 추가 + §28·§29 + totals 21158/29).

---

## 2. FROZEN HASHES (verify against these — v1.36에서 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine source** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **DGENE** `disease_gene_atlas_results.json` (불변) | `980985c629978f37d00cd0c67cf49d63df4cde32370cb2dcd0e60feab66520e3` |
| **§24** `schizophrenia_results.json` (불변) | `40b9daff9a6c0501ce29c475529bba6769d95e160359f198b76e0b9875097258` |
| **§24** `schizophrenia_symptom_domains_results.json` (불변) | `0499f74f83f0539f7a34726d5f580fb583cd23192207cef54c2bdc6fec0f0fc5` |
| **§25** `epilepsy_oversync_results.json` (불변) | `d363f0a5fcfd20294e62cb0edc26550cb366dbde8fc671c83bc0814a60d95334` |
| **§26** `e0_plasticity_results.json` (불변) | `5dbfd6dff69e301dc6aa2bdaeed93599472ab582b787e0e831f657b508ce8caf` |
| **§27** `depression_chronification_results.json` (불변) | `498f546cb4a79f4af33b5e1859fa50e6b588db6c9c844fca1713bfc40fb17d62` |
| **§28** `e2_state_switching_results.json` (신규) | `47c35e06c86e6f22d9321f449f0bf438e9fa6396b6f90ecd5f6b8a2da83aa159` |
| **§29** `bipolar_state_switching_results.json` (신규) | `5c55c0e7b2815bac209ae777ae5106154f859bd641b1b63a84ef2e52cbbdd4be` |

엔진·DGENE·§24·§25·§26·§27 해시가 v1.35와 글자 그대로 같다 — v1.36이 과학(엔진·기존 모듈)을 안 만졌다는 직접 증거.
검색층은 챕터 2개가 sitemap/llms-full에 추가되며 갱신(docs C4 층 변경, 엔진/과학 결과와 무관).

**아틀라스 재현 헤드라인(패키지 내 bit-for-bit 확인).** `run_all_atlas.py` **ALL PASS 7/7** — SZ-DISC `40b9daff…` ·
SZ-DOM `0499f74f…` · EPI `d363f0a5…` · E0-PLAS `5dbfd6df…` · DEP-T1b `498f546c…` · **E2-SWITCH `47c35e06…`** ·
**BIP-T2b `5c55c0e7…`**, engine file byte-unchanged, **14 CONFIRMED / 0 REFUTED**, honesty ledger 전부 통과.
v1.32 게이트도 불변: run_all_d9 ALL PASS · run_all_vc ALL PASS.

> **E2.4/B5 가드 = 엔진 불변의 층-수준 증명.** E2 모듈은 const-drive 적분이 엔진 `settle`과 bit-for-bit 일치함을·B5는
> η=0/bias 없음에서 M9 anchor를 bit-for-bit(`0.38961455156044245`) 재현하고 W를 커널과 동일하게 둠을 자체 확인하며,
> 매 실행 `E.emerge_all()`을 READ-ONLY 호출해 live tree가 `0fbf4988…`임을 검증한다. **그리고 T2b는 `BistableSwitch`와
> `PlasticConnectome`을 둘 다 import 재사용**하므로 스위칭/가소성 규칙의 단일출처가 유지된다(drift 위험 없음).

---

## 3. GATE / REGRESSION STATUS — gate.py PASS **134/134** (0 hard fail), 회귀 byte-identically 불변

게이트 전부 green:
- **`gate.py` PASS 134/134** (v1.35 baseline 126/126 = 27 chapters → **+8** = 신규 2 챕터의 answer-first/cards×2/JSON-LD 검사).
  - answer-first **29/29**(§28=55w·§29=55w, 전부 40–60w) · sitemap **30 locs / 30 pages** · llms.txt **4989 bytes(<5KB)**
    (하드코딩 curated subset이라 챕터 추가에 불변) · engine reproduces **`0fbf4988…` == expected** · SSOT drift **0** ·
    body word counts **±2%**(§28=1111·§29=1229) · build **멱등**.
- registry **40 locks / 29 chapters**(drift 0) · **run_all_atlas ALL PASS**(7/7) · run_all_d9 ALL PASS · run_all_vc ALL PASS.

> **회귀 불변 증명.** v1.36이 바꾼 파일 중 엔진이 import하는 건 **0개**(신규 챕터·hub·manifest·registry·거버넌스·신규
> _verify 모듈 2개·신규 generator 2개는 전부 add-only; §27 챕터는 nav·전방참조 정정으로만 재생성, 모듈 sha 불변).
> 따라서 엔진 트리·DGENE·§24·§25·§26·§27 모듈은 v1.35와 **증명적으로 동일**. 신규 E2/BIP 모듈은 자체 sha256 게이트
> `run_all_atlas.py`로 검증(서브프로세스 재실행 + 동결 상수 대조) + E2.4/B5 가드로 엔진 byte-unchanged 자체 확인.

### How to reproduce (from package root)

```bash
cd mind_pkg
python3 tools/build_search_layer.py                # 29 chapters, sitemap 30, llms.txt 4989B <5KB
python3 tools/gate.py                              # PASS 134/134, 빌드일 무관
python3 tools/mind_registry.py                     # 40 locks / 29 chapters, values match frozen
python3 repro/mind/_engine/run_all.py              # tree_sha256 = 0fbf4988…
python3 repro/mind/_verify/run_all_atlas.py        # ATLAS ALL PASS 7/7 (SZ-DISC/SZ-DOM/EPI/E0/DEP/E2/BIP) — ~수 분 소요(모듈 7개 직렬 재실행)
python3 repro/mind/_verify/e2_state_switching.py   # E2 PASS, RESULT sha256 = 47c35e06…, E2.1–E2.4 CONFIRMED, closes-25
python3 repro/mind/_verify/bipolar_state_switching.py  # BIP PASS, RESULT sha256 = 5c55c0e7…, B1–B5 CONFIRMED, reuses E2/E0
python3 repro/mind/_verify/run_all_d9.py           # D9.0–D9.4 ALL PASS, engine byte-unchanged
python3 repro/mind/_verify/run_all_vc.py           # VC1–VC5 ALL PASS (14 CONFIRMED / 1 REFUTED)
```

> **참고(런타임).** E2/BIP 모듈은 적분을 다수 sweep에서 반복하므로 각 단일 실행은 짧지만, `run_all_atlas.py`는 이제 7모듈
> 직렬이라 v1.35(5모듈)보다 길다. 결정론(2×sha256 동일)은 둘 다 확인됨. 다음 세션이 모듈을 추가할 때 같은 캐싱 패턴을 쓰면
> 런타임을 통제할 수 있다.

---

## 4. THE FIREWALL, STATED ONCE MORE (so it cannot be misread — YMYL/medical)

T2b(양극성)는 의료/건강(YMYL) **핵심** 영역이며 방화벽은 **협상 불가**다:

- **`medium_efficacy_tested = 0` (efficacy=0).** §28·§29는 어떤 자극/투여가 양극성을 *치료한다*고 주장하지 않는다.
  "안정제 = 장벽 올리기"·"kindling = 흔적 축적"은 **부호/방향**(장벽 변화 부호·흔적 깊이)이지 efficacy·용량·프로토콜이 아니다.
  **NOT medical advice.**
- **Axis-A 방화벽 — bistable 전이·보존 흔적 ≠ 주관적 경험.** 극간 스위치(E2)와 누적 흔적(E0)은 **메커니즘 경계**지 조증/울증의
  *느낌*에 대한 주장이 아니다. `consciousness_claim = 0`, `hard_problem_open = 1`.
- **이질성 LOCKED.** 양극 I/II·순환성(cyclothymia)·혼재 상태·급속순환·정신병성 — 임상 이질성은 **LOCKED**, 모델은 어느 양극성이
  개인의 것인지 말하지 않는다.
- **[O]/OWED 다종.** (i) fold *깊이*(sweep probe, 튜닝 아님); (ii) *rate η*([O], E0 대표값); (iii) *실제 가소성/스위칭 규칙의
  정체성*; (iv) *어느 아형이 개인의 병인지*(유전·일주기·모노아민·심리사회 기여 — 외부); (v) *어느 치료가 개인에게 도움되는지*
  (외부, 처방 아님). 모든 값은 in-silico coupling state지 임상 측정·진단·처방이 아니다.

§28·§29 마지막 섹션(E2.4 / B5 firewall 단락)에 이 방화벽 문장이 부착되어 있다.

---

## 5. v1.37 ENTRY POINTS (next session) — 로드맵 권장 순서

> **로드맵 시퀀스: T1a → T2a → E0 → T1b → E2 → T2b → T3a.** v1.36이 E2+T2b를 닫았으므로 **다음은 T3a(중독)** — T3a는
> 새 층이 필요 없다(E0 가소성 위에 민감화 핸들만 연결, **E2 불요**).

**A — T3a 중독 (권장 1순위, E0 민감화 필요, E2 불요라 독립).** 중독을 **보상-예측 오류의 점진적 민감화**로: M5-RPE 도파민
가치 신호가 반복 노출에서 E0 흔적을 심화시켜 **sensitisation**(자극-반응이 노출에 따라 강화)으로. T1b/T2b처럼
`from e0_plasticity import PlasticConnectome` import — 가소성 규칙 재유도 없음. **E2(상태-스위칭)는 불필요** — 중독은 극간
스위치가 아니라 한 방향 흔적 강화이므로 T2b와 독립 진행 가능. 사전등록 예: (i) 반복 노출이 보상 반응을 단조 강화(민감화 방향,
η sweep)·(ii) 같은 흔적 축적이 cue-반응성을 높임·(iii) 소거(extinction)는 흔적을 0으로 되돌리지 못함(보존 구조)·(iv)
η=0 가드로 M9 anchor bit-for-bit. LOCK→Derive→Gate로 `_verify/addiction_*.py` → `run_all_atlas.py` 등록(8모듈).
**efficacy=0·Axis-A·[O] 방화벽 부착.** ⚠ M5-RPE가 엔진에서 어떻게 노출되는지(가치 신호 핸들)를 먼저 READ-ONLY로 확인할 것 —
v1.35 HPA 핸들을 M17/M18에서 접지했듯, 중독 핸들을 M5에서 접지하고 발명하지 말 것.

**Tier-3(추후).** T3b 알츠하이머(E0 흔적/공고화 실패 — 흔적이 형성·유지되지 못하는 방향)·T3c OCD(루프/게이트 + E2 스위칭 재사용
가능 — 강박-충동 루프를 게이트 동역학으로).

**범위 외(정직한 제외).** 내용/서사 지배 조건 — 공포증·인격/해리 장애·신체상 축. T/O/W·동기화·시간 동역학이 아니라 내용
지배라 현 메커니즘 핸들로 닿지 않음. 아틀라스에 넣지 않는다.

**규율 리마인더.** 어떤 v1.37 작업도 (i) 엔진은 READ-ONLY/byte-identical 유지(새 모듈은 `_verify/`로 add-only, 기존
M0–M20 불변; **η=0/bias=0 가드로 엔진 byte-unchanged 자체 확인**); (ii) 새 튜닝 상수 0(측정값·유도값만 — 핸들은
SZ/뇌전증/E0/T1b/T2b와 동일 맵 재사용); (iii) HTML 본문 English-only(C0); (iv) llms.txt에 챕터 추가 금지(하드코딩 curated
subset, <5KB 헤드룸); (v) **efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN** 방화벽을 신규 챕터마다 부착;
(vi) 단일 zip 산출물(내부 폴더 항상 `mind_pkg`); (vii) 변경 후 §3 게이트 전부 green 확인 — FAIL 시 finalize 금지.
**재사용 우선:** T3a는 `PlasticConnectome`을 import할 것 — 가소성 규칙 재유도는 중복이자 drift 위험. **동결 lock 재작성 금지** —
빚 청산/해소는 신규 lock이 발표하고 옛 lock의 framing은 보존(v1.36이 `epilepsy_oversync`를 보존한 선례). T3c가 E2 스위칭을
재사용한다면 `from e2_state_switching import BistableSwitch`로 import(재유도 금지).
