# HANDOVER — v1.34 → v1.35  (E0: 가소성·공고화 층 §26 — 모든 시간적 장애의 기초 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.
>
> **사명(v1.33에서 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`, 동봉)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 전체 사명·축 정의·로드맵 매핑·상태표는 **`MISSION_atlas_redefinition.md`** 가 SSOT.
>
> **v1.34의 성격.** 로드맵 시퀀스 T1a→T2a→**E0**→T1b→T2b 중 **E0(가소성 층)** 을 닫았다. 이것은 질환 챕터가
> 아니라 **기초 층** — 동결 엔진에 없던 가소성 변수를 add-only로 추가하여, 이후 모든 기분/주기 장애(우울·양극성·중독)가
> **import**할 재사용 기질을 만든 것. 새 메커니즘은 forced-form 가소성 규칙 1개, 새 측정 0, 새 튜닝 0.

---

## 1. WHAT v1.34 DELIVERED (complete, all gates green)

**동결 엔진을 READ-ONLY로 두고**, 그 위에 느린 **위상-상관 Hebbian 갱신**을 ephaptic 커널 W에 add-only로 얹는 한 층을
추가·출판. 구조 아틀라스(자폐 T/O/W·조현병·뇌전증)는 모두 **정적 작동점**만 읽었다 — 엔진에 사용에 따라 변하는 변수가
없기 때문. 바로 그래서 θ-cap 챕터(§20–21)가 cap을 "pacing, not repair"로 읽었고(ON/OFF 순환에 rebound·획득 의존
없던 이유: 기질이 보존 못 함) 작동 원리의 가소성 부호가 **OPEN [O]** 였다. v1.34가 그 변수를 공급하여 그 [O]를 닫는다.

- **규칙 (form FORCED [F]; rate [O], 튜닝 아님).** 위상 진동자에서 시간-평균 STDP 창은 위상차의 함수로 환원 —
  동위상 강화·반위상 약화, 즉 위상으로 읽은 Hebb. 정상상태 쌍별 상관 `C_ij = <cos(θ_j−θ_i)>` 를 신호로,
  `W_ij ← max(0, W_ij·(1 + η·C_ij))` 후 row-renormalise. FORM은 자유상수 0(대각 0·비음수·row-stochastic이라
  `~1/r³` ephaptic locality 보존). RATE η는 representative **[O]**(절대 Hz·ring 기하·R_BRAIN이 M9에서 [O]인 것과
  동일), 부호는 η **sweep** 위에서 유지(anti-tuning). 구동/결함 bias→유효결합 맵은 SZ/뇌전증 모듈과 **동일**
  `k=κ/(1−|b|)`[흥분]/`κ/(1+|b|)`[억제] cap `2κ` — **새 상수 0**.

- **§26 「The plasticity layer — consolidation and the reversible→chronified switch」 (model).** 4개 사전등록 결과:
  - **E0.1 공고화·잔효** — 건강 작동점 구동 후 제거 → R 기저선 이상(0.390→0.391), η sweep 전체 양수. 학습·자극
    잔효·사용-의존 변화의 기질. (P1 CONFIRMED.)
  - **E0.2 연속 vs 주기 투여 — open device 질문 해소** — 동일 총 cap dose를 MASSED(연속)·SPACED(주기 ON/OFF,
    가소성이 OFF 간격 통과) 두 방식으로. Spaced가 단위 dose당 **더 큰 보존 구조 흔적** `‖ΔW‖`(0.225 vs 0.115) —
    순수 위상-가소성의 **spacing effect**. 가소성 있으면 cap은 **REPAIR**(지속 흔적), holding보다 pacing이 더 공고화:
    **pulse, do not hold**. **§20–21 [O] 채움.** η×epochs 9점 전부 부호 유지. (P2 CONFIRMED. robust 신호는 구조
    흔적 ‖ΔW‖; 구동-후 R은 spaced에서 보통이나 항상은 아님 — 정직 보고.)
  - **E0.3 가역→만성 스위치** — η=0이면 결함 여행이 bias 제거 즉시 **정확히 복귀**(§20 결과 = 가소성-없는 기질의
    귀결임을 증명), η>0이면 보존 흔적(0.394>0.390). **가소성이 가역과 만성 사이의 스위치.** Axis-A: 보존 흔적은
    메커니즘 경계지 만성질환의 느낌 주장 아님. (P3 CONFIRMED. 노출 단조성은 거짓 — 주장 안 함.)
  - **E0.4 엔진-불변 가드** — η=0이 동결 M9 anchor `R=0.38961455156044245` **bit-for-bit** 재현·W 동일. 순수 add-on.

- **신규 재현 코드(add-only).** `repro/mind/_verify/e0_plasticity.py` → `e0_plasticity_results.json` sha256
  `5dbfd6df…`(2× 결정론 확인). epilepsy_oversync.py 패턴: READ-ONLY 엔진 import·재사용 **`PlasticConnectome`**
  클래스(T1b/T2b/T3a가 import할 층)·`_integrate_corr`(E._integrate 미러+상관 누적, R bit-identical)·4 하위 연구·
  honesty_ledger·invariants(E.emerge_all() READ-ONLY 후 tree 불변 확인). `run_all_atlas.py`에 E0 튜플 등록 →
  **ALL PASS 4/4**.

- **신규 LOCK 1개**(framing, `check:None`): `plasticity_consolidation`(canonical §26). 레지스터 **37 locks / 26 chapters**.

- **거버넌스.** `CHANGELOG.md`·`COMPLETION_LEDGER.md`·`MASTER_MANUAL_START_HERE.md`(§4 롤링 포인터)·
  `MISSION_atlas_redefinition.md`(상태표 E0→DONE·T1b→NEXT) v1.34 갱신 · hub Part II(arc 단락+arc list+toc) 확장 ·
  §25→§26 nav 연결 · manifest/_meta 동기화(totals.words **17712**, §26 body 1029).

---

## 2. FROZEN HASHES (verify against these — v1.34에서 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine source** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **DGENE** `disease_gene_atlas_results.json` (불변) | `980985c629978f37d00cd0c67cf49d63df4cde32370cb2dcd0e60feab66520e3` |
| **§24** `schizophrenia_results.json` (불변) | `40b9daff9a6c0501ce29c475529bba6769d95e160359f198b76e0b9875097258` |
| **§24** `schizophrenia_symptom_domains_results.json` (불변) | `0499f74f83f0539f7a34726d5f580fb583cd23192207cef54c2bdc6fec0f0fc5` |
| **§25** `epilepsy_oversync_results.json` (불변) | `d363f0a5fcfd20294e62cb0edc26550cb366dbde8fc671c83bc0814a60d95334` |
| **§26** `e0_plasticity_results.json` (신규) | `5dbfd6dff69e301dc6aa2bdaeed93599472ab582b787e0e831f657b508ce8caf` |
| docs 검색층 트리 md5 (gate 멱등 비교용) | `fba08ed9…` (sitemap `<lastmod>` = R.RELEASE_DATE, 날짜-무의존) |

엔진·DGENE·§24·§25 해시가 v1.33과 글자 그대로 같다 — v1.34가 과학을 안 만졌다는 직접 증거. (검색층 md5는 챕터 1개가
sitemap/llms-full에 추가되며 v1.33의 `5075962e…`에서 `fba08ed9…`로 갱신 — docs C4 층 변경이고 엔진/과학 결과와 무관.)

**아틀라스 재현 헤드라인(패키지 내 bit-for-bit 확인).** `run_all_atlas.py` **ALL PASS 4/4** — SZ-DISC `40b9daff…` ·
SZ-DOM `0499f74f…` · EPI `d363f0a5…` · **E0-PLAS `5dbfd6df…`** (4/4 reproduced, engine file byte-unchanged, honesty
ledger 전부 통과). v1.32 게이트도 불변: run_all_d9 ALL PASS · run_all_vc ALL PASS(14/1).

> **E0.4 가드 = 엔진 불변의 층-수준 증명.** E0 모듈은 η=0에서 M9 anchor를 bit-for-bit(`0.38961455156044245`) 재현하고
> W를 커널과 동일하게 둔다. 즉 가소성을 끄면 동결 엔진을 정확히 회복 — 이것이 "add-only"의 operational 보증이다. 또
> 모듈은 매 실행 `E.emerge_all()` 을 READ-ONLY 호출하여 live tree가 `0fbf4988…`임을 자체 확인한다.

---

## 3. GATE / REGRESSION STATUS — gate.py PASS **122/122** (0 hard fail), 회귀 byte-identically 불변

게이트 전부 green:
- **`gate.py` PASS 122/122** (v1.33 baseline 118/118 = 25 chapters → **+4** = 신규 1 챕터의 answer-first/cards×2/JSON-LD 검사).
  - answer-first **26/26**(§26=60w, 전부 40–60w) · sitemap **27 locs / 27 pages** · llms.txt **4989 bytes(<5KB)**
    (하드코딩 curated subset이라 챕터 추가에 불변) · engine reproduces **`0fbf4988…` == expected** · SSOT drift **0** ·
    body word counts **±2%**(§26=1029 정확 매칭) · build **멱등**(`fba08ed9…` 재실행 동일).
- registry **37 locks / 26 chapters**(drift 0) · **run_all_atlas ALL PASS**(4/4) · run_all_d9 ALL PASS · run_all_vc ALL PASS.

> **회귀 불변 증명.** v1.34가 바꾼 파일 중 엔진이 import하는 건 **0개**(신규 챕터·hub·manifest·_meta·registry·거버넌스·
> 신규 _verify 모듈은 전부 add-only; 신규 generator `tools/_gen_ch26_plasticity.py`도 일회성 도구). 따라서 엔진 트리·
> DGENE·§24·§25는 v1.33과 **증명적으로 동일**(`0fbf4988…`·`980985c6…` 불변 교차확인). gate의 engine-reproduces 검사가
> 엔진 트리 byte-identical을 확증. 신규 E0 모듈은 자체 sha256 게이트 `run_all_atlas.py`로 검증(서브프로세스 재실행 +
> 동결 상수 대조) + E0.4 가드로 엔진 byte-unchanged 자체 확인.

### How to reproduce (from package root)

```bash
cd mind_pkg
python3 tools/build_search_layer.py                # 26 chapters, sitemap 27, llms.txt 4989B <5KB
python3 tools/gate.py                              # PASS 122/122, 빌드일 무관
python3 tools/mind_registry.py                     # 37 locks / 26 chapters, values match frozen
python3 repro/mind/_engine/run_all.py              # tree_sha256 = 0fbf4988…
python3 repro/mind/_verify/run_all_atlas.py        # ATLAS ALL PASS 4/4 (SZ-DISC/SZ-DOM/EPI/E0-PLAS bit-reproduced)
python3 repro/mind/_verify/e0_plasticity.py        # E0 PASS, RESULT sha256 = 5dbfd6df…, 4 sub-results CONFIRMED
python3 repro/mind/_verify/run_all_d9.py           # D9.0–D9.4 ALL PASS, engine byte-unchanged
python3 repro/mind/_verify/run_all_vc.py           # VC1–VC5 ALL PASS (14 CONFIRMED / 1 REFUTED)
```

---

## 4. THE FIREWALL, STATED ONCE MORE (so it cannot be misread — YMYL/medical)

E0는 의료/건강(YMYL) 인접 영역이며 방화벽은 **협상 불가**다:

- **`medium_efficacy_tested = 0` (efficacy=0).** §26은 어떤 자극/투여가 무엇을 *치료한다*고 주장하지 않는다. "pacing이
  holding을 이긴다"·"cap이 repair한다"는 **부호-전용 메커니즘 방향**(보존 구조 흔적 ‖ΔW‖의 부호)이지 efficacy·용량·
  프로토콜이 아니다. **NOT medical advice.**
- **Axis-A 방화벽 — 보존 구조 흔적 ≠ 주관적 경험.** 만성화(η>0에서 보존되는 흔적)는 **메커니즘 경계**지 만성질환·학습·
  자극의 *느낌*에 대한 주장이 아니다. `consciousness_claim = 0`, `hard_problem_open = 1`.
- **[O] 3종.** (i) *rate η*(representative; 부호만 η sweep으로 주장, magnitude 미적합); (ii) *application*(우울·양극성·
  중독은 이 층을 import하는 후속 모듈에 OWED); (iii) *실제 가소성 규칙의 정체성*(실제 시냅스 가소성은 이질적 —
  LTP/LTD·STDP·homeostatic scaling·metaplasticity — 어느 규칙이 작동하는지는 외부; 위상-상관 Hebbian **부호**와 그
  3 귀결만 주장).
- **모든 값은 in-silico coupling state**지 임상 측정·진단·처방이 아니다.

§26 마지막 두 섹션(E0.3·E0.4)에 이 방화벽 문장이 부착되어 있다.

---

## 5. v1.35 ENTRY POINTS (next session) — 로드맵 권장 순서

> **로드맵 시퀀스: T1a → T2a → E0 → T1b → T2b.** v1.34가 E0를 닫았으므로 **다음은 T1b(우울/TRD)**.
> E0가 만성화 기질을 공급하므로 T1b의 핵심 의존성은 충족됨 — 남은 외부 입력은 **HPA/스트레스 축**.

**A — T1b 우울/TRD (권장 1순위, E0 완비).** 우울을 **저-협응 작동점의 만성화**로: E0의 가역→만성 스위치 위에서,
지속된 저-arousal/저-결합 bias가 (η>0) 구조에 자기를 기록 = 만성 우울 기질. **필요한 추가 입력 = HPA/스트레스 축
(M17–M20 신경내분비 아틀라스, 엔진에 이미 존재)** — 코르티솔/스트레스 축을 bias 핸들로 연결. 항우울제 **지연-효과**는
E0의 공고화 타임스케일로(즉효 아닌 누적 구조 변화), **TRD**는 만성화된 흔적의 깊이로 설명 가능. 재사용:
`from e0_plasticity import PlasticConnectome` — 규칙 재유도 금지. LOCK→Derive→Gate로 `_verify/depression_*.py` +
`run_all_atlas.py` 등록. **efficacy=0·Axis-A·[O] 방화벽 부착.**

**B — T2b 양극성 (E2 + E0 필요).** 시간 축(state-switching **E2**, §25 발작 시간경과에서도 OWED) + 가소성(E0) 둘 다
필요 — 조증/울증 에피소드 전이를 **attractor 간 이동**으로, 에피소드 누적을 E0 흔적 축적으로. **E2는 §25(발작 시간경과)와
§26(만성화) 양쪽이 공유하는 층** — 한 번 지으면 뇌전증 ictal time-course와 양극성 둘 다 닫힌다. E2를 먼저 지을지
T1b를 먼저 닫을지는 작성자 선택(둘 다 독립적으로 진행 가능; T1b는 E2 불요).

**Tier-3(추후).** T3a 중독(M5-RPE 도파민 가치 신호 + E0 민감화)·T3b 알츠하이머·T3c OCD.

**범위 외(정직한 제외).** 내용/서사 지배 조건 — 공포증·인격/해리 장애·신체상 축. T/O/W·동기화·시간 동역학이 아니라
내용 지배라 현 메커니즘 핸들로 닿지 않음. 아틀라스에 넣지 않는다.

**규율 리마인더.** 어떤 v1.35 작업도 (i) 엔진은 READ-ONLY/byte-identical 유지(새 모듈은 `_verify/`로 add-only, 기존
M0–M20 불변; **E0처럼 η=0/bias=0 가드로 엔진 byte-unchanged 자체 확인**); (ii) 새 튜닝 상수 0(측정값·유도값만 —
T1b의 bias 핸들도 SZ/뇌전증/E0와 동일 맵 재사용); (iii) HTML 본문 English-only(C0); (iv) llms.txt에 챕터 추가 금지
(하드코딩 curated subset, <5KB 헤드룸 ~11바이트); (v) **efficacy=0·NOT medical advice·Axis-A·[O]·hard problem
OPEN** 방화벽을 신규 챕터마다 부착; (vi) 단일 zip 산출물(내부 폴더 항상 `mind_pkg`); (vii) 변경 후 §3 게이트 전부
green 확인 — FAIL 시 finalize 금지. **재사용 우선:** T1b/T2b/T3a는 `PlasticConnectome`을 import할 것 — 가소성 규칙
재유도는 중복이자 drift 위험.
