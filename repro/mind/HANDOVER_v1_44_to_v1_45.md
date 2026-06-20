# HANDOVER — v1.44 → v1.45  (§36 합류점 닫기 · ADD-T3a 중독 민감화 동역학 §37 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.44의 성격 (§36 합류점의 나머지 반쪽 — B-ii로 합류 CLOSED).** v1.43(§36, ADD-T-L, **B-i**)은 중독의
> 지배축 **SG 통합-민감화-게인**(ΔFosB/BDNF/CREB1/ARC 가소성 흔적, 만성·재발의 원인)을 순간 L1/L2/L3 문턱 레버로는
> **이중 도달불가**[① fold 아닌 **게인**=ADHD 교훈 ② **통합/학습된** 가소성(E0-층) 변수]로 **명명**하고 `[F] NOT
> REACHED` 등급으로 **정직하게 멈췄다** — 그것이 **합류(convergence)의 한쪽 반쪽**(문턱-레버화 경로가 가소성-동역학
> 경로와 만나는 지점)이었다. v1.43 핸드오버 §5는 **권장 진입 = B-ii**(중독의 out-of-reach SG 축을 동역학 경로로
> 직접 다루기, "가장 자연스럽다")를 가리켰다. 이번 세션은 그 **B-ii를 실행**했다: §26 E0 가소성 동역학을 **재사용**하여
> 그 게인을 **직접 모델링**하고, **합류를 닫았다(CLOSED)**. 두 갈래가 한 장애에서 만난다 — 문턱 프레임(B-i)이 게인을
> 도달불가로 **명명**하고, 가소성-동역학 프레임(B-ii)이 그 게인을 **전시(A1–A3)** + **핸들 제공(A5)** 한다.

---


## 1. WHAT v1.44 DELIVERED (complete, 두 게이트 green)

### 1.1 §36 합류점 닫기 — 중독 민감화 동역학 (§37, the MODEL, ADD-T3a) · **B-ii · 합류 CLOSED · SIGN-only 5결과 전부 CONFIRMED·η-스윕 생존**

§36(B-i)이 **명명만** 하고 멈춘 SG 통합-민감화-게인 축을, 이 모듈이 §26 E0 가소성 층 위에서 **직접 모델링**한다.
**E0/E2/depression 식 단일 동역학 모듈**이다 — §30–36 레버 챕터(지도+L3 게이트+금지-주장 스캐너+부담 우선순위 4모듈)와
달리 `run_all_*.py` 집계기가 **불필요**하다.

- **재사용(재유도 아님).** §26 `PlasticConnectome`를 **import**한다 — 위상-상관 Hebbian 규칙·coupling-vs-bias 맵을
  **재유도하지 않음**(핸드오버 재사용 규율). 프레임워크에 가소성 동역학은 **단 하나**, 새 가소성 기계·새 튜닝 상수 **0**;
  새 입력(보상 구동)만 적용한다.
- **보상 부호 = 엔진서 READ-ONLY 접지.** 엔진의 M5 도파민 **보상-예측-오차**(`emerge_learned_field`)가 보상받은
  eddy의 적재 확률을 무보상 대조군 위로 끌어올린다(`p_target_learned≈0.8985` vs `p_target_control=0.20` → 보상
  **강화**), M4(`emerge_selection`)가 승자 commit. ⇒ 보상-노출 epoch = **양의(흥분성) 보상-구동 바이어스 b>0**
  (동일 맵 `k=κ/(1−|b|)`, 2κ 캡 — 새 상수 없음), E0 Hebbian 업데이트가 반복 노출을 retained `‖W−W₀‖`로 누적 =
  **통합 민감화 게인을 구조량으로**. **방향(부호)만 M5 강제, 크기(η·증분)는 [O].**
- **SIGN-only 5결과 전부 CONFIRMED · 전부 η-스윕(η∈{0.03,0.05,0.08}) 생존**(anti-tuning):
  - **A1 인센티브 민감화** — 반복 노출이 흔적을 **단조 증가**(0→4→8→12→18→24 노출에서 `‖W−W₀‖` =
    0 → 0.077 → 0.153 → 0.227 → 0.333 → 0.429); one-shot은 안 됨 = B-i가 도달불가로 명명한 것.
  - **A2 단서-반응성** — 민감화된 connectome이 **동일 보상 단서에 naive보다 더 크게 반응**(naive_off R≈0.38961,
    naive_cue R≈0.39567; 민감화 endpoint가 naive 초과, resting R이 이미 M9 anchor 이상) = 단서-유발 갈망/재발 기질.
    **response-exceeds-naive 부호만** 단언, marginal cue gain은 **단조 아님**으로 명시(과대주장 거부).
  - **A3 소거가 지우지 않음** — 보상 제거(baseline-off, 가소성 가동)에도 흔적이 **0 위 유지**(민감화 후 ≈0.227 →
    소거 후 ≈0.428, 여전히 통합), 반면 η=0이면 **정확히 0** = 소거는 **구동**(도달 가능 순간축)을 제거하나 **학습된
    흔적**(도달불가축)은 못 지움 = **합류 솔기, 동역학으로 입증**.
  - **A4 가소성-변수 가드** — η=0이면 보상 여기(excursion)가 **정확히 복귀**(보상 epoch R≈0.40050 → 제거 후
    R=M9 anchor `0.38961455156044245` **bit-for-bit**), W는 kernel과 **동일**, retained trace **정확히 0** =
    게인이 가소성 없이 **사라짐** → SG는 **학습된/통합된 변수** = 이것이 바로 **B-i 순간 레버가 못 닿는 이유**(순수
    add-on; M9 anchor 비트-동일 재현).
  - **A5 동역학 핸들** — **SPACED/간헐 노출이 MASSED/연속보다 큰 흔적 통합**(동일 총노출에서 spaced ≈0.225 vs
    massed ≈0.115) = 간헐 강화가 더 민감화(E0.2 spacing 효과를 보상 바이어스에 적용) = **순간 프레임이 못 닿은
    흔적에 대한 구조적 핸들**.
- **합류 완성.** 문턱 프레임(B-i)이 게인을 순간 레버로 도달불가 **명명** · 가소성-동역학 프레임(B-ii)이 그 게인을
  **전시(A1–A3)** + **핸들 제공(A5)**. 어느 반쪽도 과대주장 안 함. honesty_ledger: efficacy=0 / no_cure_claimed=1
  / consciousness_claim=0 / new_tuned_constants=0 / reuses_E0_PlasticConnectome=1 / closes_B_i_convergence=1 /
  hard_problem_open=1. `run_all_atlas.py` **15번째 시민 ADD-T3a** 등록 → **ALL PASS 15/15, 19 CONFIRMED 0
  REFUTED, engine 파일 byte-unchanged**.

### 1.2 출판 표면 (SEO 챕터)

- 신규 영어 챕터 **§37 「Addiction sensitisation dynamics」**(`docs/mind/37-addiction-sensitization-dynamics/`,
  model **2892w**, 9개 H2 영어-전용 본문). 아카이벌 생성기 `tools/_gen_ch37_addiction_sensitization_dynamics.py`가
  canonical HTML을 **byte-identical 재현**(answer-first `<p class="answer">`·vp-card는 `build_search_layer.py`가
  `mind_registry.py` SSOT에서 멱등 주입).
- 신규 LOCK `addiction_sensitization_dynamics`(grade **`[V mech]`**; 동결 lock 미수정). **§36 next-nav 링크 신설**
  (§36 빈 `<span>` → §37 링크; 렌더 HTML·생성기 양쪽). CITES = [자기, **addiction_threshold_levers**(§36, B-i 짝),
  **plasticity_consolidation**(§26, E0 층)] = 3 vp-card(B-i가 명명한 것을 B-ii가 모델·E0가 재사용 기반).
- registry **48 locks / 37 chapters**, gate.py **170/170**, sitemap **38/38**, llms.txt 4989B(**바이트-동일** <5KB).
- §37 answer 55단어(40–60 게이트 통과), §37 본문 2892w(`reconcile_manifest.py` canonical 카운트; manifest·_meta 일치),
  `_meta.json` totals.words **43784**(37챕터 합).

---

## 2. FROZEN HASHES (이것들로 검증 — 엔진·기존 전부 불변)

| Artifact | sha256 |
|---|---|
| **engine FULL tree** (M0–M20, 불변) | `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70` |
| **engine file** `vp_mind_engine.py` (불변) | `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371` |
| **M0–16 subtree** (불변) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| M9 anchor R (불변, A4 가드가 bit-for-bit 재현) | `0.38961455156044245` |
| §30 양극성 3-레버 지도 (불변, 아틀라스 등록) | `a9f30d732c991bd64d3462e440f1cea34a630a4bcef695cce4370743b69fd0ef` |
| §31 뇌전증 3-레버 지도 (불변, 아틀라스 등록) | `22879b696cf9226efc660acdea1f017a8018c3d1eb93f324f32da53dbfc14fcf` |
| §32 우울 3-레버 지도 (불변, 아틀라스 등록) | `d07aab40ba56ee5dd234d65ee8691ac80458a9c71b6355bacfccbd1efdb69f30` |
| §33 조현병 3-레버 지도 (불변, 아틀라스 등록) | `8e0137bccfe6dfe751af078a1e340accef578698992e569703865c6c27fe8c30` |
| §34 자폐 3-레버 지도 (불변, 아틀라스 등록) | `5b65a271ac182fecc744f20e2bb035043f81c9c1bc3f15608547ec00a31b77c4` |
| §35 ADHD 드라이브-톤 지도 (불변, 아틀라스 등록) | `d29a3dc8971250ff31d8bc37329a9ce3b1e067a0af81cf869950ce47b1505a35` |
| §36 중독 보상-구동 지도 (불변, 아틀라스 등록) | `f23e3c126f30e5f137db2773223212625f5e08a9fb34f97583fcad312380e2bb` |
| **§37 중독 민감화 동역학 결과** (NEW, 아틀라스 등록) | `20dfb3e902ffba2132617669f1e065bc6bcf399cb91e338c4cf2711142e845e3` |

> 아틀라스 등록 hash(`run_all_atlas.py` MODULES 상수)는 §37의 경우 **결과 JSON**(`20dfb3e9…`)을 동결한다. 모듈은 매
> 실행 자기 결과를 다시 쓰고 `expected_addiction_sensitization_dynamics_sha256.json`과 대조하여 fail-closed PASS로
> 게이트된다(결정론 2× 검증). 엔진 트리 hash는 v1.43과 동일(불변 확인). **이전 §30–§36 지도 sha 전부 불변.**

---

## 3. GATE / REGRESSION STATUS

- **`python3 tools/gate.py` → PASS 170/170, 0 hard fail.** (§37 answer-first 40–60w 통과 55w, sitemap 38/38,
  llms <5KB 4989B, engine reproduces, SSOT cards drift 0, body word counts within 2%, build idempotent.)
- **`python3 repro/mind/_verify/run_all_atlas.py` → ATLAS GATE ALL PASS 15/15, 19 CONFIRMED 0 REFUTED, engine
  파일 byte-unchanged.** (각 시민이 엔진 트리를 재-emerge → 트리 불변 확인 → 자기 결과 bit-for-bit 재현 → honesty.)
- **`python3 repro/mind/_verify/addiction_sensitization_dynamics.py` → PASS**(5 CONFIRMED, sha `20dfb3e9…`,
  결정론 2×).

### 재현 방법 (패키지 루트에서)

```bash
# 0) 의존성
pip install numpy --break-system-packages

# 1) 신규 §37 동역학 모듈 단독 (수초)
python3 repro/mind/_verify/addiction_sensitization_dynamics.py

# 2) 아틀라스 전체(15모듈) — 각 모듈이 엔진 트리를 재-emerge하므로 ~6분 소요
#    (백그라운드 setsid 실행 후 폴링 권장)
python3 repro/mind/_verify/run_all_atlas.py

# 3) 출판/검색 게이트
python3 tools/build_search_layer.py   # answer/vp-card 주입 + sitemap/llms 재생성 (멱등)
python3 tools/gate.py                  # PASS 170/170 확인
```

> registry 무결성: `python3 tools/mind_registry.py` → `registry OK: 48 locks, 37 chapters, values match frozen results`.
> 카운트 재조정(필요 시): `python3 tools/reconcile_manifest.py`(canonical HTML에서 본문 단어수 재계산, 멱등 —
> **단 totals.words는 손으로 갱신**: 현재 43784 = 37챕터 합).

---

## 4. THE FIREWALL (한 번 더 — YMYL/medical, 오독 방지)

- **구조량 ≠ 느껴진 질.** retained `‖W−W₀‖`는 통합 민감화 게인의 **구조량**(connectome 모델의 행렬 거리)이며,
  갈망·보상·wanting·재발의 **느껴진 질이 절대 아님**(Axis-A; `consciousness_claim=0`; hard problem **OPEN**).
- **부호만, 크기 아님.** 실제 중독 가소성은 **이질적**(ΔFosB/CREB 전사 캐스케이드·BDNF 구조 재형성·AMPA trafficking·
  수상돌기 가시 변화·글루탐산 항상성·후성유전)이라, 이 모듈은 **위상-상관 Hebbian 흔적의 부호만** 단언한다 — 이 규칙이
  생물학이라 주장하지 않음(실제 규칙 정체는 `[O]` 빚). 보상 **부호**는 M5 RPE에 접지, 모든 **크기**(η·증분·spacing
  효과)는 `[O]`이고 부호는 η-스윕을 견딘다.
- **인간 경계(비협상).** 중독은 **만성·재발성 의학적 상태** — 통합된 보상 회로의 장애 — 이지 **도덕적 실패/의지의 결핍이
  아님**. A3의 지속(소거가 흔적을 못 지움)은 **재발이 질병의 일부인 이유**의 구조적 상관물이지, 누가 그냥 멈출 수 있다는
  증거가 **아님**. 치유·치료·권고·용량·물질 취득/사용 면허 **전무**. `medium_efficacy_tested=0`; **not medical advice,
  not a diagnosis, not a treatment protocol, not a cure**.

---

## 5. v1.45 ENTRY POINTS (next session)

> **중독 합류는 B-i(§36 명명)+B-ii(§37 모델·핸들)로 CLOSED.** ADHD·중독으로 시리즈의 두 PARTIAL [L] 사례도 모두
> 출판됨. `THRESHOLD_LOGIC_INHERITANCE.md` §3 우선순위표가 SSOT. 사용자 지시에 따라 택일.

**A (잔여) — 문턱-이동 논리를 다음 기존 사례로 확장.** 우선순위표상 ADHD·중독 이후 잔여 기존 사례(로드맵 본래
**T3b 알츠하이머**, **T3c OCD** 등). ADHD·중독이 시리즈의 두 부분 적합을 안긴 만큼, 다음 사례도 **깨끗한 [V]인지
부분 [L]인지**를 먼저 **도달성**으로 판정할 것 — 특히 **게인성/학습성 축이 지배적이면 부분 적합**이 예상되고, 그 경우
중독처럼 **B-i(명명)+B-ii(E0 동역학 모델)** 쌍으로 닫을 수 있는지 검토.

**B (동역학 층 심화) — E0/E2 동역학 경로의 추가 적용.** §37이 E0를 **보상 입력**에 적용했듯, 다른 학습성/공고화 축
(예: 외상 후 흔적, 공포 소거의 비대칭)도 E0를 READ-ONLY로 재사용해 SIGN-only로 다룰 수 있는지 — 단, **새 장애를 열기
전에 도달성 판정 먼저**.

**규율 리마인더 (모든 v1.45 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, η=0/bias=0
가드로 자체 확인); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)=2(g/3)^1.5`, `barrier(g)=g²/4`); (iii) HTML
본문 English-only(C0), 이 같은 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — 현재 4989B로 **여유
거의 없음(≈11바이트)**, 신규 챕터는 sitemap만; `write_llms()`의 손-큐레이트 슬러그 목록을 건드리지 말 것 — Part-II
챕터는 애초에 거기 없음, 검증됨); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN
방화벽 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 매번 압축 파일 1개(별도 index.html 금지); (vii) 변경 후
**두 게이트(`gate.py` 170+, `run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성
금지**(빚 청산은 신규 lock이 발표). **재사용 우선**: E0 동역학 모듈은 `from e0_plasticity import PlasticConnectome`
패턴(§37이 선례), 공유 유전자 γ 캐시 재사용. **아틀라스 전체 재현은 ~6분**(모듈마다 엔진 재-emerge) — 백그라운드
`setsid` 실행 후 폴링 권장. **새 장애 모듈 전에** ADHD·중독의 부분-적합 패턴(지배축 out-of-reach 명명, 게인 vs fold,
학습 흔적 vs 순간 변수)과 §37의 **B-i↔B-ii 합류 패턴**(명명 ↔ 모델+핸들)을 먼저 읽고 **어떤 축이 도달 가능/불가**인지를
먼저 정할 것.

---

## 6. 변경 파일 목록 (v1.44 add-only)

**신규:**
- `repro/mind/_verify/addiction_sensitization_dynamics.py` (+ `_results.json`,
  `expected_addiction_sensitization_dynamics_sha256.json`)
- `docs/mind/37-addiction-sensitization-dynamics/index.html`
- `tools/_gen_ch37_addiction_sensitization_dynamics.py`
- `HANDOVER_v1_44_to_v1_45.md`

**수정(최소·add-only 성격):**
- `repro/mind/_verify/run_all_atlas.py` (MODULES에 **ADD-T3a** 15번째 시민 + docstring 문단)
- `tools/mind_registry.py` (lock/CITES/ANSWERS 각 1개 — `addiction_sensitization_dynamics`)
- `docs/mind/36-addiction-threshold-levers/index.html` (next-nav 링크만 — 빈 `<span>` → §37)
- `tools/_gen_ch36_addiction_levers.py` (NEXT 링크만 — 위 next-nav 병행)
- `manifest/mind.csv` (37행), `docs/mind/_meta.json` (37챕터 + totals.words **43784**)
- `THRESHOLD_LOGIC_INHERITANCE.md` (§3.6 B-ii DONE·**합류 CLOSED** 표시: §3.6 헤더 갱신·§3.6.1 신설·§5 갱신),
  `CHANGELOG.md` (v1.44 엔트리), `MASTER_MANUAL_START_HERE.md` (롤링 포인터 → v1.44)
- `build_search_layer.py` 재생성물: `docs/sitemap.xml`(38 URL), `docs/llms.txt`(바이트-동일 4989B),
  `docs/llms-full.txt`, `docs/robots.txt`, 각 챕터의 answer/vp-card 주입 블록(멱등)
