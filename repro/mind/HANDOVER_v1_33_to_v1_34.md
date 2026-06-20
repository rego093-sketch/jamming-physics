# HANDOVER — v1.33 → v1.34  (Part II 확장: 트랜스진단 결함-축 아틀라스 — 조현병(T1a) §24 · 뇌전증(T2a) §25 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.
>
> **사명 재정의됨(v1.33).** 패키지는 이제 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`, 동봉)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 전체 사명·축 정의·로드맵 매핑·상태표는 **`MISSION_atlas_redefinition.md`** 가 SSOT.

---

## 1. WHAT v1.33 DELIVERED (complete, all gates green)

**이미 동결된 엔진을 재사용**하여, 자폐에서 보정한 T/O/W 점화 축과 동기화 축을 **자폐 너머 두 주요 질환**으로 확장·출판.
로드맵의 "먼저 할 것" 두 값싼-재사용 목표(T1a·T2a). 새 메커니즘 0 · 새 측정 0 · 새 튜닝 0.

- **§24 「Schizophrenia: the over-ignition mirror of autism」 (T1a, model).**
  - **판별식**(`schizophrenia_discriminant.py`, v1.32에 존재했으나 미출판 → 이번에 출판): 하나의 공유 점화 축
    (R19 fold = `spinodal(g)=2(g/3)^1.5=0.3849`) 위에서 조현병 = 자폐-T의 **반대 극**. 탈억제/흥분 bias가 fold를
    **내림**(점화 임계 0.245 vs 건강 0.395) → 약·무관 집합체(2,3) 점화 = **이상 현저성**, 관련 손실 0. 쌍
    (점화방향, 무관회수 vs 관련손실)이 HEALTH/AUTISM-T/SZ를 **유일 지문화**. RX 부호: gain-감소 항정신병약이
    선택성 회복 + 자폐-T 악화; 자극제는 반대(자극제-유발 정신병 방향). 극단 disorganisation 한계(전 후보 점화) +
    SLEEP 부호 정렬(진정 = 수면 방향, 자폐의 거울).
  - **증상-도메인 축 지도**(`schizophrenia_symptom_domains.py`, 신규): 양성→threshold 과점화(항정신병약 **도달**·
    이상 점화 제거)·음성→output 결핍(R=0.354<건강 0.390; 항정신병약은 gain-감소라 0.309로 **더 낮춤**=미도달)·
    인지→long-range wiring(locality 0.842>건강 0.794; 스칼라 gain이 locality 정확 불변=미도달). **하나의 gain-감소
    연산자가 양성만 역전 → 차등 항정신병약 반응 = dose-구조 아님, axis-구조** = D2 차단이 양성만 완화하는 이유의
    메커니즘 설명. "더 많은 D2 차단 → 음성/인지" **폐기**(in-silico null).

- **§25 「Epilepsy: the over-synchronisation pole」 (T2a, model).** `epilepsy_oversync.py`(신규). 프레임워크 **자신의**
  과동기화 실패 모드 — θ-cap이 아래 머물 천장(§20) — 을 **주 모듈**로. EP1 과동기화 축(흥분 bias→R 단조↑, over-sync
  천장 0.422>건강 0.390)·EP2 발작 게이트 붕괴(임계 bias +0.3 초과서 선택 게이트 붕괴, 6개 전부 점화=발작 상태)·EP3
  항경련제 부호(억제 push→R↓+게이트 복원, 발작 임계 상승)·EP4 축 정렬(**autism-T < health < schizophrenia <
  epilepsy** 한 동기화 축). 정적 susceptibility는 특성화, **발작 시간경과는 state-switching 층(E2)에 OWED**.

- **신규 재현 코드(add-only) + 오케스트레이터.** `run_all_atlas.py`(신규): 각 모듈을 **새 서브프로세스로 재실행** →
  written results.json의 sha256를 오케스트레이터 내 **동결 상수**와 대조(모듈이 매 실행 자체 expected_*.json 재기록 →
  진짜 회귀 가드 = 오케스트레이터 상수) + 엔진 file/tree 불변 + 정직 ledger 검증 → `gate_atlas.json` 기록 → **ALL PASS**.
  각 `repro/mind/24-…/README.md`·`25-…/README.md` 작성.

- **신규 LOCK 3개**(전부 framing, `check:None`): `schizophrenia_mirror`·`schizophrenia_symptom_domains`·`epilepsy_oversync`.
  레지스터 **36 locks / 25 chapters**.

- **거버넌스.** 로드맵 사본 동봉 · `MISSION_atlas_redefinition.md` 신규 · `CHANGELOG.md`·`COMPLETION_LEDGER.md`·
  `MASTER_MANUAL_START_HERE.md` v1.33 갱신 · hub Part II(arc+toc) 확장 · §23→§24→§25 nav 연결 · manifest/_meta 동기화
  (totals.words **16683**).

---

## 2. FROZEN HASHES (verify against these — v1.33에서 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine source** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **DGENE** `disease_gene_atlas_results.json` (불변) | `980985c629978f37d00cd0c67cf49d63df4cde32370cb2dcd0e60feab66520e3` |
| **§24** `schizophrenia_results.json` (판별식) | `40b9daff9a6c0501ce29c475529bba6769d95e160359f198b76e0b9875097258` |
| **§24** `schizophrenia_symptom_domains_results.json` | `0499f74f83f0539f7a34726d5f580fb583cd23192207cef54c2bdc6fec0f0fc5` |
| **§25** `epilepsy_oversync_results.json` | `d363f0a5fcfd20294e62cb0edc26550cb366dbde8fc671c83bc0814a60d95334` |
| docs 검색층 트리 md5 (gate 멱등 비교용) | `5075962e…` (sitemap `<lastmod>` = R.RELEASE_DATE, 날짜-무의존) |

엔진·DGENE 해시가 v1.28–v1.32와 글자 그대로 같다 — v1.33이 과학을 안 만졌다는 직접 증거. (검색층 md5는 챕터 2개가
sitemap/llms-full에 추가되며 v1.32의 `53f2a138…`에서 `5075962e…`로 갱신 — docs C4 층 변경이고 엔진/과학 결과와 무관.)

**아틀라스 재현 헤드라인(패키지 내 bit-for-bit 확인).** `run_all_atlas.py` **ALL PASS** — SZ-DISC `40b9daff…` ·
SZ-DOM `0499f74f…` · EPI `d363f0a5…` (3/3 reproduced, engine file byte-unchanged, honesty ledger 전부 통과).
v1.32 게이트도 불변: run_all_d9 ALL PASS · run_all_vc ALL PASS(14/1).

---

## 3. GATE / REGRESSION STATUS — gate.py PASS **118/118** (0 hard fail), 회귀 byte-identically 불변

게이트 전부 green:
- **`gate.py` PASS 118/118** (v1.32 baseline 110/110 = 23 chapters → **+8** = 신규 2 챕터의 answer-first/cards/JSON-LD 검사).
  - answer-first **25/25**(§24=56·§25=55w, 전부 40–60w) · sitemap **26 locs / 26 pages** · llms.txt **4989 bytes(<5KB)**
    (하드코딩이라 챕터 추가에 불변) · engine reproduces **`0fbf4988…` == expected** · SSOT drift **0** · body word counts
    **±2%**(§24=700·§25=611 정확 매칭) · build **멱등**(`5075962e…` 재실행 동일).
- registry **36 locks / 25 chapters**(drift 0) · **run_all_atlas ALL PASS**(3/3) · run_all_d9 ALL PASS · run_all_vc ALL PASS.

> **회귀 불변 증명.** v1.33이 바꾼 파일 중 엔진이 import하는 건 **0개**(신규 챕터·hub·manifest·_meta·registry·거버넌스·
> 신규 _verify 모듈·신규 오케스트레이터는 전부 add-only). 따라서 엔진 트리·DGENE는 v1.32와 **증명적으로 동일**(`0fbf4988…`·
> `980985c6…` 불변 교차확인). gate의 engine-reproduces 검사가 엔진 트리 byte-identical을 확증. 신규 _verify 모듈은 자체
> sha256 게이트 `run_all_atlas.py`로 검증(서브프로세스 재실행 + 동결 상수 대조).

### How to reproduce (from package root)

```bash
cd mind_pkg
python3 tools/build_search_layer.py                # 25 chapters, sitemap 26, llms.txt 4989B <5KB
python3 tools/gate.py                              # PASS 118/118, 빌드일 무관
python3 tools/mind_registry.py                     # 36 locks / 25 chapters, values match frozen
python3 repro/mind/_engine/run_all.py              # tree_sha256 = 0fbf4988…
python3 repro/mind/_verify/run_all_atlas.py        # ATLAS ALL PASS (SZ-DISC/SZ-DOM/EPI bit-reproduced)
python3 repro/mind/_verify/run_all_d9.py           # D9.0–D9.4 ALL PASS, engine byte-unchanged
python3 repro/mind/_verify/run_all_vc.py           # VC1–VC5 ALL PASS (14 CONFIRMED / 1 REFUTED)
```

---

## 4. THE FIREWALL, STATED ONCE MORE (so it cannot be misread — YMYL/medical)

이 Part II는 의료/건강(YMYL) 영역이며 방화벽은 **협상 불가**다:

- **`medium_efficacy_tested = 0` (efficacy=0).** 어떤 챕터도 약/장치가 조현병·뇌전증을 *치료한다*고 주장하지 않는다.
  RX 부호는 **부호-전용 메커니즘 방향**(예: gain-감소 항정신병약이 양성 도메인을 역전; 억제 push가 발작 게이트 복원)이지
  efficacy·용량이 아니다. **NOT medical advice.**
- **Axis-A 방화벽 — 게이트/선택 붕괴 ≠ 주관적 경험.** 발작의 게이트 붕괴도, 조현병의 극단 disorganisation 한계도
  **메커니즘 경계**지 발작/혼란의 *느낌*에 대한 주장이 아니다. `consciousness_claim = 0`, `hard_problem_open = 1`.
- **[O] 3종.** (i) *어느 극이 그 사람의 정신병인지*; (ii) *어느 증상-도메인이 지배적인지*; (iii) *발작 시간경과*
  (정적 susceptibility만 특성화; 발작 전이 동역학은 E2 필요).
- **모든 값은 in-silico coupling state**지 임상 측정·진단·처방이 아니다.

각 신규 챕터 마지막 섹션에 이 방화벽 문장이 부착되어 있다.

---

## 5. v1.34 ENTRY POINTS (next session) — 로드맵 권장 순서

> **로드맵 권장 시퀀스: T1a → T2a → E0 → T1b → T2b.** v1.33이 T1a·T2a를 닫았으므로 **다음은 E0**.

**A — E0 가소성 층 (NEW, 고노력, 기초) — 권장 1순위, 별도 집중 세션.** 후속 기분/주기 장애(T1b 우울·T2b 양극성)가
**모두 의존**하는 가소성 기질. 현 엔진은 가소성 변수가 없어(§20에서 cap이 "수리 아닌 페이싱"인 이유) 학습/적응/항우울제
지연-효과를 모델링하려면 이 층이 먼저 필요. **고노력·기초 층이므로 값싼-재사용 챕터들과 묶지 말고 자체 세션으로** —
LOCK→Derive→Gate로 가소성 핸들 1개를 엔진에 신규 추가(또는 `_verify/` 상위 모듈)하되 기존 M0–M20 불변, 새 측정 최소화.

**B — T1b 우울/TRD (E0 필요).** E0 위에서 우울을 T/O/W + 가소성 축으로; 항우울제 지연-효과·TRD를 메커니즘으로.

**C — T2b 양극성 (E2 + E0 필요).** 시간 축(state-switching E2, §25에서 OWED) + 가소성(E0) 둘 다 필요 — 조증/울증
에피소드 전이를 attractor 간 이동으로. **E2는 §25 발작 시간경과에도 공유되는 층** — 한 번 지으면 둘 다 닫힌다.

**Tier-3(추후).** T3a 중독(M5-RPE 도파민 가치 신호)·T3b 알츠하이머·T3c OCD.

**범위 외(정직한 제외).** 내용/서사 지배 조건 — 공포증·인격/해리 장애·신체상 축. T/O/W 동역학이 아니라 내용 지배라
현 메커니즘 핸들로 닿지 않음. 아틀라스에 넣지 않는다.

**규율 리마인더.** 어떤 v1.34 작업도 (i) 엔진은 READ-ONLY/byte-identical 유지(새 모듈은 `_verify/` 또는 신규 엔진
모듈로, 기존 M0–M20 불변; **E0가 엔진에 가소성 핸들을 더한다면 새 엔진 모듈로 add-only, 기존 트리 불변 확인**);
(ii) 새 튜닝 상수 0(측정값·유도값만); (iii) HTML 본문 English-only(C0); (iv) llms.txt에 챕터 추가 금지(하드코딩,
<5KB 헤드룸 ~11바이트); (v) **efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN** 방화벽을 신규 챕터마다
부착; (vi) 단일 zip 산출물(내부 폴더 항상 `mind_pkg`); (vii) 변경 후 §3 게이트 전부 green 확인 — FAIL 시 finalize 금지.
