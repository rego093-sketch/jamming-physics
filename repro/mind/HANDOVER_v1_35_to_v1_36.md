# HANDOVER — v1.35 → v1.36  (T1b: 우울/TRD §27 — 첫 시간적 장애, E0 위에 세움 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.
>
> **사명(v1.33에서 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`, 동봉)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 전체 사명·축 정의·로드맵 매핑·상태표는 **`MISSION_atlas_redefinition.md`** 가 SSOT.
>
> **v1.35의 성격.** 로드맵 시퀀스 T1a→T2a→E0→**T1b**→T2b 중 **T1b(우울/TRD)** 를 닫았다. 이것은 **첫 시간적(temporal)
> 장애**이자 **E0 가소성 층 위에 세워진 첫 모듈** — 질환 챕터가 새 메커니즘을 만든 게 아니라 **E0가 공급한 만성화 기질을
> import해서 HPA 핸들에 연결**한 것. 새 메커니즘 0, 새 측정 0, 새 튜닝 0. (`from e0_plasticity import PlasticConnectome`,
> 규칙 재유도 없음.)

---

## 1. WHAT v1.35 DELIVERED (complete, all gates green)

**동결 엔진 + E0 층을 READ-ONLY로 두고**, 우울을 **저-협응 작동점의 만성화**로 모델링하는 모듈 1개와 챕터 1개를 add-only로
출판. 구조 아틀라스(자폐 T/O/W·조현병·뇌전증)는 점화/동기화 축의 **정적 작동점**만 읽었다. E0가 시간 축(가소성)을 열었고,
v1.35는 그 위에 **첫 시간적 질환**을 세운다. HPA/스트레스 축(M18 코르티솔 + M17 valence, 코르티솔=위축 극, 이미 창발)을
bias 핸들로 연결.

- **핸들 (접지, 발명 아님).** M17 valence = approach(DA) − avoid(cortisol), 코르티솔이 위축 극; M18 HPA cascade
  (PVN/SIM1 → ACTH → 코르티솔, peak 인용 15–40분 창, glucocorticoid 음성 피드백). 만성 HPA 구동 → 지속 **위축 bias**
  `b<0` → SZ/뇌전증/E0와 **동일** 맵 `k=κ/(1−|b|)`[흥분]/`κ/(1+|b|)`[억제] cap `2κ`로 결합 하강 — **새 상수 0**.
  **부호만** 주장(만성 스트레스 → 위축 → 저-협응, M17 valence 기하가 고정), **크기 [O]**, 부호는 sweep 위에서 유지. HPA
  kinetics는 M18에서 **인용 [L]**.

- **§27 「Depression and treatment resistance — the chronification of a low-coordination operating point」 (model).**
  4개 사전등록 결과 + 가드:
  - **D1 급성 우울 작동점** — 지속 위축 bias가 전역 order parameter R을 health 아래로(모든 수준 0.390 아래, severe
    R≈0.331<mild). 급성·반응성 우울 = 저-협응. 정적 기질 가역. (CONFIRMED.)
  - **D2 만성화 = 가역→만성 스위치(HPA 핸들)** — η=0이면 위축 여행이 스트레스 제거 즉시 **정확히 복귀**(반응성 저기분),
    η>0이면 복귀하지 않는 **보존 구조 흔적**, 노출에 비례 단조 심화(‖ΔW‖ 0.075→0.151→0.227→0.338), η sweep 유지.
    **정직**: 강건 신호는 구조 흔적 ‖ΔW‖; 제거-후 R은 **baseline 아래로 주장 안 함**(위상-Hebb이 잔존 in-phase 공고화→R
    오를 수 있음). 지속 객체는 흔적. (CONFIRMED.)
  - **D3 항우울제 지연 발현 = 공고화 타임스케일** — 복원 이동 ‖W_k−W_dep‖이 epochs에 걸쳐 **단조 누적**·1 epoch에
    미미(0.018 vs 8 epoch 0.138), 즉 weeks-to-onset이 공고화 타임스케일이지 PK 지연 아님. 방향은 치료적(코스 후 R 상승),
    rate×strength sweep 유지. (CONFIRMED.)
  - **D4 치료 저항(TRD) = 흔적 깊이** — 고정 복원 예산에서 항우울제가 중화하는 우울 흔적의 **분율**이 깊이에 따라 **단조
    감소**(깊을수록 비례적으로 덜 도달, 더 큰 잔여), rate×budget sweep 유지. (CONFIRMED.)
  - **D5 엔진-불변 가드** — η=0/stress=0이 동결 M9 anchor `R=0.38961455156044245` **bit-for-bit** 재현·W 동일. 순수 add-on.

- **신규 재현 코드(add-only).** `repro/mind/_verify/depression_chronification.py` → `depression_chronification_results.json`
  sha256 `498f546c…`(2× 결정론 확인). epilepsy/E0 패턴: READ-ONLY 엔진 import + **`from e0_plasticity import
  PlasticConnectome`**(규칙 재유도 없음, 핸드오프 규율 준수) + HPA 핸들을 M17/M18에서 READ-ONLY 접지 + D1–D4 사전등록 +
  D5 가드 + honesty_ledger + invariants(E.emerge_all() READ-ONLY 후 tree 불변 확인). 증분 체크포인트 + 연결체 복제로
  캐싱(값 불변, 계산만 단축 — 런타임 ~100s). `run_all_atlas.py`에 DEP-T1b 튜플 등록 → **ALL PASS 5/5**.

- **신규 LOCK 1개**(framing, `check:None`): `depression_chronification`(canonical §27). 레지스터 **38 locks / 27 chapters**.

- **거버넌스.** `CHANGELOG.md`·`COMPLETION_LEDGER.md`·`MASTER_MANUAL_START_HERE.md`(§4 롤링 포인터 v1.35)·
  `MISSION_atlas_redefinition.md`(상태표 T1b→DONE·T2b→NEXT) v1.35 갱신 · hub Part II(arc list+toc) §27 확장 ·
  §26→§27 nav 연결 · manifest/mind.csv 27행(words 1047).

---

## 2. FROZEN HASHES (verify against these — v1.35에서 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine source** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **DGENE** `disease_gene_atlas_results.json` (불변) | `980985c629978f37d00cd0c67cf49d63df4cde32370cb2dcd0e60feab66520e3` |
| **§24** `schizophrenia_results.json` (불변) | `40b9daff9a6c0501ce29c475529bba6769d95e160359f198b76e0b9875097258` |
| **§24** `schizophrenia_symptom_domains_results.json` (불변) | `0499f74f83f0539f7a34726d5f580fb583cd23192207cef54c2bdc6fec0f0fc5` |
| **§25** `epilepsy_oversync_results.json` (불변) | `d363f0a5fcfd20294e62cb0edc26550cb366dbde8fc671c83bc0814a60d95334` |
| **§26** `e0_plasticity_results.json` (불변) | `5dbfd6dff69e301dc6aa2bdaeed93599472ab582b787e0e831f657b508ce8caf` |
| **§27** `depression_chronification_results.json` (신규) | `498f546cb4a79f4af33b5e1859fa50e6b588db6c9c844fca1713bfc40fb17d62` |

엔진·DGENE·§24·§25·§26(E0) 해시가 v1.34와 글자 그대로 같다 — v1.35가 과학(엔진·기존 모듈)을 안 만졌다는 직접 증거.
검색층은 챕터 1개가 sitemap/llms-full에 추가되며 갱신(docs C4 층 변경, 엔진/과학 결과와 무관).

**아틀라스 재현 헤드라인(패키지 내 bit-for-bit 확인).** `run_all_atlas.py` **ALL PASS 5/5** — SZ-DISC `40b9daff…` ·
SZ-DOM `0499f74f…` · EPI `d363f0a5…` · E0-PLAS `5dbfd6df…` · **DEP-T1b `498f546c…`**, engine file byte-unchanged,
7 CONFIRMED / 0 REFUTED, honesty ledger 전부 통과. v1.32 게이트도 불변: run_all_d9 ALL PASS · run_all_vc ALL PASS.

> **D5 가드 = 엔진 불변의 층-수준 증명.** DEP 모듈은 η=0/stress=0에서 M9 anchor를 bit-for-bit(`0.38961455156044245`)
> 재현하고 W를 커널과 동일하게 둔다. 또 매 실행 `E.emerge_all()`을 READ-ONLY 호출하여 live tree가 `0fbf4988…`임을 자체
> 확인한다. **그리고 E0의 `PlasticConnectome`을 import 재사용**하므로 가소성 규칙의 단일출처가 유지된다(drift 위험 없음).

---

## 3. GATE / REGRESSION STATUS — gate.py PASS **126/126** (0 hard fail), 회귀 byte-identically 불변

게이트 전부 green:
- **`gate.py` PASS 126/126** (v1.34 baseline 122/122 = 26 chapters → **+4** = 신규 1 챕터의 answer-first/cards×2/JSON-LD 검사).
  - answer-first **27/27**(§27=57w, 전부 40–60w) · sitemap **28 locs / 28 pages** · llms.txt **4989 bytes(<5KB)**
    (하드코딩 curated subset이라 챕터 추가에 불변) · engine reproduces **`0fbf4988…` == expected** · SSOT drift **0** ·
    body word counts **±2%**(§27=1047) · build **멱등**.
- registry **38 locks / 27 chapters**(drift 0) · **run_all_atlas ALL PASS**(5/5) · run_all_d9 ALL PASS · run_all_vc ALL PASS.

> **회귀 불변 증명.** v1.35가 바꾼 파일 중 엔진이 import하는 건 **0개**(신규 챕터·hub·manifest·registry·거버넌스·신규
> _verify 모듈·신규 generator는 전부 add-only). 따라서 엔진 트리·DGENE·§24·§25·§26은 v1.34와 **증명적으로 동일**.
> 신규 DEP 모듈은 자체 sha256 게이트 `run_all_atlas.py`로 검증(서브프로세스 재실행 + 동결 상수 대조) + D5 가드로 엔진
> byte-unchanged 자체 확인.

### How to reproduce (from package root)

```bash
cd mind_pkg
python3 tools/build_search_layer.py                # 27 chapters, sitemap 28, llms.txt 4989B <5KB
python3 tools/gate.py                              # PASS 126/126, 빌드일 무관
python3 tools/mind_registry.py                     # 38 locks / 27 chapters, values match frozen
python3 repro/mind/_engine/run_all.py              # tree_sha256 = 0fbf4988…
python3 repro/mind/_verify/run_all_atlas.py        # ATLAS ALL PASS 5/5 (SZ-DISC/SZ-DOM/EPI/E0/DEP) — ~8분 소요(모듈 5개 직렬 재실행)
python3 repro/mind/_verify/depression_chronification.py  # DEP PASS, RESULT sha256 = 498f546c…, D1–D4 CONFIRMED, D5 guard (~100s)
python3 repro/mind/_verify/run_all_d9.py           # D9.0–D9.4 ALL PASS, engine byte-unchanged
python3 repro/mind/_verify/run_all_vc.py           # VC1–VC5 ALL PASS (14 CONFIRMED / 1 REFUTED)
```

> **참고(런타임).** `depression_chronification.py`는 6000-step 적분을 다수 sweep에서 반복하므로 단일 실행 ~100s,
> `run_all_atlas.py`는 5모듈 직렬이라 ~8분. 결정론(2×sha256 동일)은 확인됨. 다음 세션이 모듈을 추가할 때 같은 캐싱
> 패턴(증분 체크포인트 + 연결체 복제)을 쓰면 런타임을 통제할 수 있다.

---

## 4. THE FIREWALL, STATED ONCE MORE (so it cannot be misread — YMYL/medical)

T1b는 의료/건강(YMYL) **핵심** 영역이며 방화벽은 **협상 불가**다:

- **`medium_efficacy_tested = 0` (efficacy=0).** §27은 어떤 자극/투여가 우울을 *치료한다*고 주장하지 않는다.
  "항우울제 지연 발현 = 공고화 타임스케일"·"TRD = 흔적 깊이"는 **부호/타임스케일 방향**(보존 구조 흔적의 부호·분율)이지
  efficacy·용량·프로토콜이 아니다. **NOT medical advice.**
- **Axis-A 방화벽 — 보존 구조 흔적 ≠ 주관적 경험.** 만성화(η>0에서 보존되는 흔적)는 **메커니즘 경계**지 만성/난치성 우울의
  *느낌*에 대한 주장이 아니다. `consciousness_claim = 0`, `hard_problem_open = 1`.
- **정직한 음성(주장 안 함).** 제거-후 협응 R은 **baseline 아래로 주장하지 않는다** — 위상-Hebb이 잔존 in-phase 구조를
  공고화해 R이 오를 수 있어, 강건·부호-안정 신호는 보존 **구조** 흔적 ‖ΔW‖로 한정. (보고할 뿐.)
- **[O]/OWED 다종.** (i) 스트레스→bias *크기*(representative; 부호만 sweep으로 주장); (ii) *rate η*([O], E0 대표값);
  (iii) *실제 가소성 규칙의 정체성*(이질적 — LTP/LTD·STDP·homeostatic·metaplasticity); (iv) *어느 아형이 개인의 병인지*
  (멜랑콜릭·비정형·정신병성·주산기·계절성·양극성 우울; 모노아민·HPA·염증·일주기·심리사회 기여 — 외부); (v) *어느 치료가
  개인에게 도움되는지*(외부, 처방 아님). 모든 값은 in-silico coupling state지 임상 측정·진단·처방이 아니다.

§27 마지막 섹션(D4 firewall 단락)에 이 방화벽 문장이 부착되어 있다.

---

## 5. v1.36 ENTRY POINTS (next session) — 로드맵 권장 순서

> **로드맵 시퀀스: T1a → T2a → E0 → T1b → T2b.** v1.35가 T1b를 닫았으므로 **다음은 T2b(양극성)** — 단, T2b는 새 층 **E2
> (state-switching)** 가 필요하다.

**A — T2b 양극성 (권장 1순위, E2 + E0 필요).** 양극성을 **attractor 간 전이 + 삽화 누적**으로: 조증/울증 에피소드 전이를
attractor 간 이동(state-switching **E2**)으로, 에피소드 누적을 E0 흔적 축적으로. **E2는 §25(발작 시간경과)와 §27(만성화)이
공유하는 층** — R19 bistable 스위치를 **시간에 걸쳐** 쓰는 동역학 층. **한 번 지으면 뇌전증 ictal time-course(§25 OWED)와
양극성 둘 다 닫힌다.** 재사용: `from e0_plasticity import PlasticConnectome`(흔적 축적) + 신규 E2 state-switch primitive.
LOCK→Derive→Gate로 `_verify/bipolar_*.py`(+ E2 모듈) → `run_all_atlas.py` 등록. **efficacy=0·Axis-A·[O] 방화벽 부착.**

**B — T3a 중독 (E0 민감화 필요, T1b/T2b와 독립).** M5-RPE 도파민 가치 신호 + E0 민감화(반복 노출이 흔적을 심화시켜
sensitisation). T1b처럼 `PlasticConnectome` import. E2 불요라 양극성과 독립 진행 가능.

**Tier-3(추후).** T3b 알츠하이머·T3c OCD.

**범위 외(정직한 제외).** 내용/서사 지배 조건 — 공포증·인격/해리 장애·신체상 축. T/O/W·동기화·시간 동역학이 아니라
내용 지배라 현 메커니즘 핸들로 닿지 않음. 아틀라스에 넣지 않는다.

**규율 리마인더.** 어떤 v1.36 작업도 (i) 엔진은 READ-ONLY/byte-identical 유지(새 모듈은 `_verify/`로 add-only, 기존
M0–M20 불변; **T1b처럼 η=0/bias=0 가드로 엔진 byte-unchanged 자체 확인**); (ii) 새 튜닝 상수 0(측정값·유도값만 — bias
핸들은 SZ/뇌전증/E0/T1b와 동일 맵 재사용); (iii) HTML 본문 English-only(C0); (iv) llms.txt에 챕터 추가 금지(하드코딩
curated subset, <5KB 헤드룸); (v) **efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN** 방화벽을 신규
챕터마다 부착; (vi) 단일 zip 산출물(내부 폴더 항상 `mind_pkg`); (vii) 변경 후 §3 게이트 전부 green 확인 — FAIL 시 finalize
금지. **재사용 우선:** T2b/T3a는 `PlasticConnectome`을 import할 것 — 가소성 규칙 재유도는 중복이자 drift 위험. E2를 지을 땐
**§25 ictal time-course와 양극성이 공유**하도록 한 번에 설계(중복 금지).
