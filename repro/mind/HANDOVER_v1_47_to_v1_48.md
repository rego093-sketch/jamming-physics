# HANDOVER — v1.47 → v1.48  (OCD-T3c-L 강박장애 CSTC-루프 레버 §40 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.47의 성격 (문턱-이동 논리 기존-사례 #8 · OCD B-i · 시리즈 4번째 PARTIAL [L] · NEW MODE = 제3의 E0 양태로
> E0 삼부작 완성).** v1.46 핸드오버 §5-A는 로드맵 본래 **T3c OCD**를 다음 사례로 지목하며, OCD가 CSTC 루프의
> **고착/반복** 성격 때문에 문턱 프레임이 순간 작동점은 잡되 학습된 고착 자체가 가소성 변수로 명명될지(중독 SG GAIN
> 유사 학습 흔적인지) **먼저 도달성 판정**하라 했다. **v1.47이 그 판정을 수행**: INSTANT(순간 CSTC 흥분성) 축은
> **도달**, LOCK(병적 안정화/자기-지속 강박 루프) 축은 **도달불가** — 그리고 LOCK은 중독의 E0 **GAIN**도 알츠하이머의
> E0 **DECAY**도 아닌 **제3의 뚜렷한 E0 양태 = STABILISATION**(과-심부 basin·과-광폭 hysteresis로 부적응 끌개를
> 얼림)임을 발견. 이로써 **E0 삼부작 완성**: 중독은 흔적을 **쌓고**(GAIN)·알츠하이머는 기질을 **잃고**(DECAY)·OCD는
> 끌개를 **얼린다**(STABILISATION). 상속한 문턱-이동 개입 논리(analgesic v2.0, Zenodo 10.5281/zenodo.20733420)를
> CSTC 루프 기질에 적용해 8 레버 + 4 out-of-reach LOCK = **12 유전자 3-레버 지도**(동일 R19 기질, 새 메커니즘·새 튜닝
> 상수 0, 엔진 READ-ONLY)를 만들었다. **알츠하이머의 순수-증상 표면과 달리, OCD 레버는 실제 주류/연구 경로(SSRI
> 1차·항정신병약 증강·글루탐산 조절제)이며 진짜로 (부분적으로) 도움**이 된다 — 그러나 작동점만 밀 뿐 **루프를 풀지
> (unstick) 못해** 부분적이다. **B-i(명명) 단계**다 — LOCK 축을 4 실제 유전자로 명명·`[F] NOT REACHED`. 다음(v1.48)의
> 자연스러운 **B-ii**는 중독(GAIN)·알츠하이머(DECAY) 선례처럼 그 LOCK을 E0 동역학으로 직접 모델(stuck-attractor/
> 안정화 동역학)해 **합류를 닫는** 것.

---


## 1. WHAT v1.47 DELIVERED (complete, 두 게이트 green)

### 1.1 §40 OCD CSTC-루프 레버 (the MODULE, OCD-T3c-L) · **시리즈 4번째 PARTIAL [L] · NEW MODE(STABILISATION) · L3-지배+L1-강·L2-희소·혼합 부호 · LOCK 축 도달불가 명명**

- **메인 지도 모듈.** `repro/mind/_verify/ocd_threshold_levers.py` (결과 sha **`c5e2af0eefc404d39725faf48d6085470c63e6965596b332d29b5253882e1456`**; 결정론 2× 검증). §30–36·§38 레버 챕터와 같은 4-step 패턴(지도→부담 우선순위→L3 정직성 게이트→금지-주장 스캐너), 집계기 `run_all_ocd_levers.py`.
- **도달성 매핑(REACHABILITY).** L1/L2/L3 프레임에 도달성 기준으로 매핑. **L3 4개**(상류 세로토닌성/도파민성 구동): SLC6A4(SERT)·HTR2A·HTR1B 세로토닌성 톤 **복원**(SSRI/클로미프라민 1차약)·DRD2 도파민성 구동 **감소**(항정신병약 증강). **L1 3개**(글루탐산 흥분성 **감소**): SLC1A1/EAAT3(**가장 재현된 OCD 유전자**)·GRIN2B·GRIK2. **L2 단 1개**(억제 **복원**): GABRA1 — 단일 희소 약한 노드(OCD GABA성 팔이 얇음=발견). **9번째 분포 = L3-지배+L1-강·L2-희소·혼합 부호**.
- **혼합 부호(MIXED SIGN).** 세로토닌성 톤↑·도파민성 구동↓·글루탐산성 구동↓·억제↑ — 알츠하이머(§38)에 이은 시리즈 2번째 분할-부호.
- **시리즈 4번째 PARTIAL [L] & NEW MODE.** `partial_fit_witness` 등급 `[L] partial`, `fit_index_in_series=4`, `completes_e0_trio=True`, `deepest_partial=False`. 도달 표면=순간 CSTC 흥분성(reachable-but-partial); 지배축=LOCK 병적-안정화(자기-지속 강박 루프). LOCK 도달불가의 **3중 이유**: ① fold 아닌 게인/손실(ADHD 교훈) ② 통합/학습된 가소성 E0-층 변수(중독 교훈) ③ 그를 넘어 **병적 안정화** = 과-심부 basin·hysteresis(E2 현상) = **E0 STABILISATION**(제3 양태). 순간 레버는 작동점만 밀고 루프를 **풀지 못함** → 반응이 부분적·느림; 동역학 개입(CSTC DBS, ERP)이 난치에 닿음.
- **LOCK 축 명명·`[F] NOT REACHED`** (`out_of_reach_targets`): **DLGAP3/SAPAP3**(과그루밍 정전 OCD 마우스 모델 = 피질선조체 PSD 스캐폴드, Welch 2007)·**SLITRK5**(같은 표현형 시냅스-접착, Shmelkov 2010)·**PTPRD**(OCD GWAS 접착 포스파타제, IOCDF-GC 2018)·**BTBD3**(OCD GWAS 회로-패터닝, Stewart 2013). γ 동반·비-레버.
- **γ 접지.** γ=−mean(NN stacking dG, SantaLucia 1998)를 자기 프로모터(TSS−2000..+500, Homo sapiens)서 읽어 |h_sp|=spinodal(γ)=2(γ/3)^1.5·barrier=γ²/4(엔진 READ-ONLY). **5개 read verbatim 재사용**(SLC6A4·HTR2A=우울, DRD2=중독, GRIN2B=자폐, GABRA1=뇌전증; γ 가닥-대칭, 비트-동일), 7개(HTR1B·SLC1A1·GRIK2·DLGAP3·SLITRK5·PTPRD·BTBD3) GRCh38 strand-aware live fetch(provenance `ocd_levers_promoters.cache.json`).
- **γ는 도달성·우선순위와 직교(ORTHOGONAL) — 가장 깨끗한 형태.** 전체 최강 프로모터가 **out-of-reach LOCK 유전자 DLGAP3**(γ≈1.590, |h_sp|≈0.772)·최약은 **도달 가능 레버 GABRA1**(|h_sp|≈0.536)·4개 out-of-reach가 강성 **전 범위 분산**(최강 DLGAP3·준-최약 SLITRK5 둘 다 도달불가, 도달 가능 레버가 사이에 끼임) → 도달 가능·도달불가가 **교차배열** → 강성은 축도·도달성도·우선순위도 예측 못함(교차배열 자체가 방화벽의 가장 깨끗한 증명).

### 1.2 부담 우선순위 (`ocd_burden_prioritisation.py`)
- 가중 B=0.40/U=0.35/G=0.25, 12 유전자 전부(4 LOCK은 `actionable=False`). **OCD 미충족 시그니처 = 미충족 상한으로 표현**: 최심 미충족 tier(U=5)를 **전적으로 out-of-reach LOCK**(DLGAP3/SLITRK5/PTPRD/BTBD3 — 루프-고착엔 분자 치료 전무, DBS만)가 보유. **선두 실행 가능 = 글루탐산 수송체 SLC1A1 #1**(4.65 — 가장 재현된 OCD 유전자·가장 약물화 가능, 도달 가능하나 루프 못 풀어 **부분적**), SLC6A4 #2(4.30), 최고점 **비실행 LOCK DLGAP3 #3**(4.10). U-floor=**3**(확립됐으나 부분적 세로토닌성 경로 — ADHD floor 2보다 높음). **알츠하이머와 달리 최강 약물화 표적 SLC1A1은 도달 가능** — 도달불가인 것은 최심-미충족 tier(루프-고착). **decoupling**: 최강 프로모터 DLGAP3 우선순위 #3(최상위 아님), 최우선 SLC1A1은 4번째 강성 read뿐.

### 1.3 두 fail-closed 게이트
- **L3 정직성 게이트** `ocd_l3_honesty.py` (15검사 PASS): 4 세로토닌성/도파민성 구동 링크 전부 [O]; L3 유일 지배·L1>0·L2 SPARSE(==1)·INSTANT 혼합-부호 도메인 제한·LOCK-축 명명-도달불가·PARTIAL [L]·completes_e0_trio 단언.
- **금지-주장 스캐너** `ocd_forbidden_claim_scan.py` (PASS): 일반 용량/효능/안전/합성 + **CURE_MIRACLE**(치유/강박사고-영구-정지/강박행동-제거/OCD-사라짐/기적/원-위어드-트릭)·**MORAL_FRAMING/STIGMA**(그냥-걱정-그만/의지박약/성격결함/도덕적-실패/관심끌기/so-OCD-about/진짜-병-아님) 추가. negation-guarded + 미끼 자기-테스트. **주의(정직한 수정)**: "high-dose SSRI"·"higher doses" 문자열이 DOSING 스캐너를 오발화 → "SSRI/클로미프라민 세로토닌성 방향"·"더 지속적·강한 세로토닌성 경과"로 재서술(스캐너가 실제로 잡은 빚).

### 1.4 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **18번째 시민 OCD-T3c-L** 등록(MODULES 튜플 + 도크스트링 커버리지 문단; honesty 불변식 medium_efficacy_tested=0·consciousness_claim=0·new_tuned_constants=0·hard_problem_open=1 포함).
- 신규 영어 챕터 **§40 「OCD threshold levers」**(model 4721w, 9 H2 영어-전용 본문, position 40, canonical correct). 아카이벌 생성기 `_gen_ch40_ocd_levers.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `ocd_threshold_levers`(grade **`[L partial · O links]`**, canonical "40-ocd-threshold-levers"). CITES=[자기, **addiction_threshold_levers**(§36, 형제 부분-적합/학습-흔적), **alzheimers_threshold_levers**(§38, 형제 부분-적합/E0 양태)] — 3 vp-card. ANSWERS 40–60단어 통과.
- **§39 next-nav 신설**: §39 빈 `<span>`→§40 링크 + "paper contents" 중간 링크 신설로 3-요소 nav 정규화(생성기·렌더 양쪽). §40 nav도 prev §39 + paper contents + 빈 span(마지막 챕터).
- registry **51 locks / 40 chapters**. manifest·`_meta.json` reconcile(40행/40챕터, §40=4721w, totals.words 51268→**55989**).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → **registry OK: 51 locks, 40 chapters, values match frozen results**.
- `python3 tools/gate.py` → PASS(전 챕터 answer-first·구조·결정론). **이번 빌드에서 green 확인 후 finalize.**
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 18/18**, engine 파일 byte-unchanged. (아틀라스 전체 재현 ~6분; 모듈마다 엔진 재-emerge.)
- `python3 repro/mind/_verify/run_all_ocd_levers.py` → **ALL PASS**(4-step + 결정론 2×).


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- OCD-T3c-L 지도 결과 sha(신규 동결): **`c5e2af0eefc404d39725faf48d6085470c63e6965596b332d29b5253882e1456`**.
- γ/|h_sp| 레버(강성순): SLC6A4 1.516/0.719·GRIK2 1.490/0.700·SLC1A1 1.485/0.697·DRD2 1.481/0.694·HTR1B 1.475/0.689·GRIN2B 1.361/0.611·HTR2A 1.321/0.584·GABRA1 1.246/0.536. out-of-reach LOCK: DLGAP3 1.590/0.772(전체 최강)·PTPRD 1.451/0.673·BTBD3 1.416/0.648·SLITRK5 1.293/0.566.
- E0 삼부작: 중독 GAIN(§36/§37) · 알츠하이머 DECAY(§38/§39) · **OCD STABILISATION(§40, B-i; B-ii 미완)**.


## 4. THE FIREWALL (YMYL/medical, 오독 방지)
프로모터 |h_sp|는 유전자 자신의 스위치 강성, **basin 깊이·hysteresis 폭·강박 고착의 강도·수용체 점유·시냅스 세로토닌/도파민/글루탐산 수준·약효·용량·임상효과가 절대 아님**. 도달 가능 레버는 작동점을 밀 뿐 **루프를 풀지 못함**(CSTC 심부뇌자극·노출-반응-방지가 동역학 핸들). efficacy=0, NOT medical advice, 치유·기적·강박사고-영구-정지·강박행동-제거 주장 전무. **인간 경계(비협상)**: OCD는 **치료 가능한 의학적 상태**이고 **침습적 사고는 증상이지 도덕적 실패가 아니다** — 강박은 선택이 아니고 인격 결함이 아니며, 장애는 회로의 병적 고착이지 성격의 흠이 아님. 프로모터 읽힘·레버 배정은 메커니즘 경계이지 강박·충동·완화의 **느껴진 질**에 관한 주장이 아님(Axis-A·consciousness_claim=0·hard problem OPEN). 실제 OCD는 다인자·이질적, 확립된 세로토닌성 1차약은 **부분적** 효과(잔여/난치 다수).


## 5. v1.48 ENTRY POINTS (next session)

> 네 PARTIAL [L] 사례(ADHD·중독·알츠하이머·OCD) 모두 출판, **E0 삼부작(GAIN/DECAY/STABILISATION) 완성**.
> `THRESHOLD_LOGIC_INHERITANCE.md` §3 우선순위표·§3.8 적합도 요약표가 SSOT. 사용자 지시에 따라 택일.

**A (가장 자연스러운 다음) — OCD B-ii: 루프-고착/안정화 동역학 직접 모델로 합류 닫기.** 중독(§37, E0 GAIN)·알츠하이머(§39, E0 DECAY)가 B-i 명명을 B-ii E0 동역학 모델로 닫은 **두 선례**가 있다. OCD의 LOCK = **병적 안정화(STABILISATION)** 는 그 둘과 구조적으로 다른 제3 양태이므로, §41(가칭 OCD-T3c-D)에서 §26 E0 `PlasticConnectome`를 READ-ONLY **import**(재유도 금지)하고 **안정화 변형**(예: basin을 깊게 하는 양성-피드백 공고화 = 강박-완화의 음성-강화 누적; 또는 hysteresis 폭 증가)을 적용해 SIGN-only로 (i) 루프가 자기-안정화로 깊어짐, (ii) 순간 레버가 작동점은 밀되 basin 깊이를 못 줄임(unstick 실패 = B-i가 명명한 도달불가의 동역학 입증), (iii) 안정화 변수 가드(파라미터=0 복귀 = M9 앵커 bit-for-bit), (iv) 동역학 핸들은 안정화 축에만(=DBS/ERP가 닿는 곳) 을 보일 수 있는지 검토. **접지 정직성(§39 선례 필수)**: 엔진에 강박-안정화 신호가 없으면 부호를 엔진 신호에서 접지한다고 **주장하지 말 것** — 깊어지는/얕아지는 기준과 가드만 READ-ONLY 접지하고 방향은 정의/구조로 접지, honesty_ledger에 `*_grounded_in_engine_pathology_signal=0` 정직 플래그.

**B (잔여) — 문턱-이동 논리를 다음 기존 사례로 확장.** 우선순위표상 잔여 사례. 새 사례도 **깨끗한 [V]인지 부분 [L]인지**를 먼저 도달성으로 판정 — 게인/학습/퇴행/안정화 축이 지배적이면 부분 적합 예상, 그 경우 B-i(명명)+B-ii(E0 동역학) 쌍으로 닫을 수 있는지 검토.

**규율 리마인더 (모든 v1.48 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)=2(g/3)^1.5`, `barrier(g)=g²/4`; 동역학 rate/decay/안정화율은 [O]·부호는 스윕 견딤); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **두 게이트(`gate.py`, `run_all_atlas.py` ALL PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **재사용 우선**: E0 동역학 모듈은 `from e0_plasticity import PlasticConnectome` 패턴(§37 GAIN·§39 DECAY 선례), 공유 유전자 γ 캐시 재사용. **아틀라스 전체 재현 ~6분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행; sh에서 `disown` 불가). **새 모듈 전에** 네 부분-적합 패턴(지배축 out-of-reach 명명: fold vs 게인 vs 학습 흔적 vs 퇴행/DECAY vs 안정화/STABILISATION)과 두 닫힌 **B-i↔B-ii 합류**(중독 GAIN·알츠하이머 DECAY)를 먼저 읽고 어떤 축이 도달 가능/불가인지 먼저 정할 것.

---

## 6. 변경 파일 목록 (v1.47 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `ocd_threshold_levers.py`·`ocd_burden_prioritisation.py`·`ocd_l3_honesty.py`·`ocd_forbidden_claim_scan.py`·`run_all_ocd_levers.py`·`_build_ocd_levers_cache.py`·`ocd_levers_promoters.cache.json`·`ocd_threshold_levers_results.json`·`ocd_burden_prioritisation.json`·`expected_ocd_threshold_levers_sha256.json`.
**신규 (docs/tools)**: `docs/mind/40-ocd-threshold-levers/index.html`·`tools/_gen_ch40_ocd_levers.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(18th citizen)·`tools/mind_registry.py`(LOCK+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 41 urls 등)·`manifest/mind.csv`(40행)·`docs/mind/_meta.json`(40챕터+totals)·`docs/mind/39-alzheimers-progression-dynamics/index.html`+`tools/_gen_ch39_alzheimers_progression_dynamics.py`(next-nav §40).
**거버넌스**: `CHANGELOG.md`(v1.47)·`HANDOVER_v1_47_to_v1_48.md`(이 문서)·`THRESHOLD_LOGIC_INHERITANCE.md`(§3.9·§3.8 표·§5)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터).
