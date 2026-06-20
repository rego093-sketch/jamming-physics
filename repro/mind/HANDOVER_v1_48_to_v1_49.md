# HANDOVER — v1.48 → v1.49  (OCD-T3c-D 강박장애 안정화 동역학 §41 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.48의 성격 (OCD B-ii · 제3의 E0 양태 · E0 삼부작 완성).** v1.47이 §40(OCD-T3c-L, B-i)에서 OCD의
> 지배축 = **STABILISATION 고착**(자기-지속·과공고화된 강박 루프)을 순간 레버로 **도달불가 명명**(4 유전자 `[F]`,
> "E2 현상")했다. 그것은 합류의 **한쪽 반쪽**이었다. **v1.48이 나머지 반쪽**: v1.47 핸드오버 §5-A(권장 다음 = OCD
> B-ii)에 따라 그 LOCK을 §26 E0 `PlasticConnectome` 위에서 **직접 모델**해 합류를 닫았다. **핵심 = 제3의 E0 양태**:
> §37과 다른 점은 알츠하이머처럼 업데이트의 **방향**이 아니라 **읽기(readout)** — §37의 동일 potentiating Hebbian
> 업데이트를 **음성-강화된 협응 작동점**에서 구동해 connectome이 협응을 자기 구조에 써 넣을 때까지 = 자기-지속 고착
> 루프. STABILISATION은 §37 GAIN의 공고화 **family를 공유**(동일 업데이트가 흔적 씀)하고 **자기-지속-휴지 읽기로
> 구별**된다(고착 루프가 외부 단서 없이 휴지서 자기 협응을 앵커 위로 유지). **이로써 E0 삼부작 완성**: 중독은 흔적을
> **쌓고**(GAIN, 단서-반응)·알츠하이머는 기질을 **잃고**(DECAY)·OCD는 끌개를 **얼린다**(STABILISATION, 자기-지속).
> **정직성(§39 선례)**: 엔진에 고착-루프 신호가 없으므로 안정화 부호를 엔진 병리 신호에서 접지한다고 **주장하지
> 않는다** — 부호는 §37 GAIN과 동일 E0 공고화 family로 접지(자기-지속 읽기로 구별), basin-깊이 개념은 READ-ONLY
> R19 barrier로 접지, **네트워크-hysteresis는 주장 안 함**(네트워크가 이 결합서 깨끗한 쌍안정이 없음).

---


## 1. WHAT v1.48 DELIVERED (complete, 세 게이트 green)

### 1.1 §41 OCD 안정화 동역학 (the MODULE, OCD-T3c-D) · **제3의 E0 양태(STABILISATION) · OCD B-ii · 합류 닫음 · 삼부작 완성**

- **단일 동역학 모듈.** `repro/mind/_verify/ocd_stabilisation_dynamics.py` (결과 sha **`ef37d619baba3643a16ee564ebe2200e4b3fcc1dea7c23f651b9d9bc1a4fbe79`**; 결정론 2× 검증). §37 GAIN·§39 DECAY처럼 **집계기 불필요한 단일 모듈**(run_all_*.py 없음, `__main__`이 직접 PASS 출력).
- **E0 재사용(재유도 금지).** `from e0_plasticity import PlasticConnectome, OMEGA, OMEGA0, KAP, W0, FOLD, N, _k_bias` — 커널 W0·결합맵·차수파라미터 기계를 **import**. 프레임워크에 가소성 층은 **단 하나**. 새 가소성 기계·새 튜닝 상수 **0**.
- **제3 양태로 구동.** §37과 동일 `.epoch(bias=+0.30, eta=0.08)` potentiating Hebbian 업데이트를, **음성-강화된 협응 작동점**에서 구동(각 강박행동의 일시적 불안-완화가 강화자)하여 connectome이 협응을 자기 구조에 써 넣을 때까지 = 자기-지속 고착 루프. **§37 GAIN과 공고화 family 공유**(동일 업데이트가 흔적 씀, 질량↑), **자기-지속-휴지 읽기로 구별**.
- **충실 IC 적분기 + 비트-동일 가드.** `_integrate_ic(W,k,th0)`가 엔진 `E._integrate`를 미러. **가드**: 엔진 자신의 고정 시드-랜덤 IC(`_TH_INC=RandomState(SEED).uniform(-pi,pi,N)`)를 먹이면 `E._integrate(W0)`==M9 **bit-for-bit** 재현(확인). `_TH_COH=zeros(N)`=고착 시작. 관측량: `_trace(W)`=‖W−W0‖, `_Rlock(W)`=고착 IC서 읽기, `_Rfresh(W)`=신선 IC서 읽기.
- **SIGN-only 5결과 전부 CONFIRMED·eta·bias 스윕 생존** (EPOCHS=[0,6,12,18], SWEEP_ETAS=(0.05,0.08,0.12), SWEEP_BIASES=(0.20,0.30,0.45)):
  - **S1 진행성 안정화**: 흔적 0→0.183794→0.35285→0.497543 단조(eta·bias 스윕 둘 다) + 고착 깊어짐(Rlock_deep=0.4048148087≥Rlock_shallow=0.3985440534, 둘 다 앵커 위).
  - **S2 자기-지속 루프(정의적 읽기)**: 고착 IC서 Rlock≥M9 AND Rlock≥Rfresh(ep≥4, eta-swept); 초과 Rlock−M9: −0.001177→0.00893→0.01353→0.0152; ep18 eta0.08 Rlock=0.404815·Rfresh=0.395854. **중독 단서-반응성·알츠하이머 저하와 구별**.
  - **S3 레버가 루프를 못 풂**: 레버가 흔적 **정확히 그대로**(==), 최대 레버도 깊은 흔적(0.497543) 감소 불가.
  - **S4 구조-변수 가드**: 공고화=0 → W==W0·흔적==0·충실 적분기가 M9(R_faithful=0.3896145516)로 비트-동일·엔진 `_integrate(W0)`==M9.
  - **S5 동역학 핸들**: 낮은 eta → 동일 epoch서 엄격히 적은 흔적; 레버는 구조 핸들 없음.
- **3-양태 교차검증(구조적 대비).** GAIN trace=0.35285 / DECAY mass lost=5.515679 / STAB trace=0.35285(GAIN과 **문자적 동일**) + 자기-지속 Rlock=0.403145. `distinct=True`. **OCD를 구별하는 건 다른 흔적이 아니라 자기-지속 읽기**.
- **honesty_ledger**: efficacy=0·no_cure=1·consciousness_claim=0·hard_problem_open=1·tuned=0·reuses_E0=1·closes_OCD_B_i=1·**stabilisation_sign_grounded_in_engine_pathology_signal=0**(정직한 비유사성)·stabilisation_is_third_E0_mode=1·same_E0_family_as_addiction_gain=1·distinguished_from_gain_by_self_sustaining_loop=1·basin_depth_grounded_in_R19_barrier_readonly=1·**network_hysteresis_claimed=0**(정직 — 네트워크에 깨끗한 쌍안정 없음)·dignity=1.

### 1.2 접지 정직성 (the central honesty, §39 선례 적용)
- 엔진에는 **고착-루프 신호가 없다**(과-안정 basin·자기-지속-루프 변수 없음 — 건강한 창발 아틀라스). 그래서 안정화 부호를 **엔진 병리 신호에서 접지한다고 주장하지 않음**.
- READ-ONLY 접지 3가지: ① **기준**(동결 M9 앵커 W0, 루프가 고착하는 협응); ② **basin-깊이 개념**(엔진 R19 barrier `B(g)=g²/4=0.25` @g=1.0, cusp 정규형 basin 깊이); ③ **가드**(공고화 off → 엔진 비트-동일 복귀).
- **핵심 정직성**: 네트워크는 이 결합서 자기만의 깨끗한 쌍안정/hysteresis가 없다 → **네트워크-hysteresis 주장 안 함**. §40이 명명한 과-심부 basin/hysteresis 고착은 **E2/R19-cusp** 현상이고 READ-ONLY barrier로 접지. 안정화 **방향**은 §37 GAIN의 **동일 E0 공고화 family**(자기-지속-휴지 읽기로 구별). **부호만 단언, 크기 [O]**.

### 1.3 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **19번째 시민 OCD-T3c-D** 등록(MODULES 튜플 + 도크스트링 커버리지 문단; honesty 불변식 medium_efficacy_tested=0·consciousness_claim=0·new_tuned_constants=0·hard_problem_open=1 포함).
- 신규 영어 챕터 **§41 「OCD stabilisation dynamics」**(model **3977w**, 9 H2 영어-전용 본문, position 41, canonical correct). 아카이벌 생성기 `_gen_ch41_ocd_stabilisation_dynamics.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `ocd_stabilisation_dynamics`(grade **`[V mech]`**, canonical "41-ocd-stabilisation-dynamics"). CITES=[자기, **ocd_threshold_levers**(§40, B-i 짝), **plasticity_consolidation**(§26, E0 층)] — 3 vp-card. ANSWERS 40–60단어(gate 60w) 통과.
- **§40 next-nav 신설**: §40 빈 `<span>`→§41 링크(생성기·렌더 양쪽). §41 nav = prev §40 + paper contents + 빈 span(마지막 챕터).
- registry **52 locks / 41 chapters**. manifest·`_meta.json` reconcile(41행/41챕터, §41=3977w, totals.words 55989→**59966**).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → **registry OK: 52 locks, 41 chapters, values match frozen results**.
- `python3 tools/gate.py` → PASS(전 챕터 answer-first·구조·결정론; §41 answer-first 60w·sitemap 42/42·llms 4989B·idempotent·wordcount 2% 이내). **이번 빌드에서 green 확인 후 finalize.**
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 19/19**, engine 파일 byte-unchanged. (아틀라스 전체 재현 ~6분; 모듈마다 엔진 재-emerge.)
- `python3 repro/mind/_verify/ocd_stabilisation_dynamics.py` → **PASS**(5결과 + 결정론 2× + 기대-sha 일치).
- (참고) `run_all_ocd_levers.py`는 §40 4-step 집계기 — §41 추가에 영향 없음, 여전히 PASS.


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- R19 barrier `B(g)=g²/4` → `E.barrier(1.0)=0.25`; R19 fold `E.spinodal(1.0)=0.38490017945975047`; KAPPA_EPHAPTIC=0.5496.
- OCD-T3c-D 결과 sha(신규 동결): **`ef37d619baba3643a16ee564ebe2200e4b3fcc1dea7c23f651b9d9bc1a4fbe79`**.
- OCD-T3c-L 지도 sha(v1.47 동결, 불변): `c5e2af0eefc404d39725faf48d6085470c63e6965596b332d29b5253882e1456`.
- **E0 삼부작 완성**: 중독 GAIN(§36 B-i / §37 B-ii) · 알츠하이머 DECAY(§38 B-i / §39 B-ii) · **OCD STABILISATION(§40 B-i / §41 B-ii)**. 셋 다 §26 E0 `PlasticConnectome` 재사용; GAIN/STAB는 공고화 family 공유(STAB는 자기-지속 읽기로 구별), DECAY는 그 구조적 역.


## 4. THE FIREWALL (YMYL/medical, 오독 방지)
retained 흔적은 안정화의 **구조량**, 침습적 사고·충동·강박의 고통의 **느껴진 질이 절대 아님**(Axis-A·consciousness_claim=0·hard problem OPEN). 도달 가능 레버(§40)는 작동점을 밀 뿐 **루프를 풀지 못함**; 핸들은 **공고화(학습/가소성) 축에만** = ERP가 새 소거 학습으로 루프를 재작성하는 곳(CSTC DBS도 동역학 축). efficacy=0, NOT medical advice, 치유·역전·예방 주장 전무. **인간 경계(비협상)**: OCD는 **치료 가능한 의학적 상태**이고 **침습적 사고는 증상이지 소망·인격 결함·도덕적 실패가 아니다** — 누구도 자신의 강박이나 루프의 책임자로 취급할 면허 없음. 실제 OCD는 이질적(CSTC 과연결·세로토닌성/글루탐산성 조절이상·SAPAP3/DLGAP3 PSD 병리·SLITRK5·기저핵 게이팅·오류-모니터링)이라 **자기-지속 안정화의 부호만** 단언(이 공고화가 생물학이라 주장 안 함, 실제 기전 [O]); 안정화 부호는 §37 GAIN 동일 family(엔진엔 고착-루프 신호 없음)·basin-깊이는 READ-ONLY R19 barrier(네트워크-hysteresis 주장 안 함)·크기 [O]·부호는 eta·bias 스윕 생존.


## 5. v1.49 ENTRY POINTS (next session)

> 네 PARTIAL [L] 사례(ADHD·중독·알츠하이머·OCD) 모두 출판. **세 B-i↔B-ii 합류 모두 닫힘 → E0 삼부작(GAIN/DECAY/STABILISATION) 완성.**
> `THRESHOLD_LOGIC_INHERITANCE.md` §3 우선순위표·§3 적합도 요약표가 SSOT. 사용자 지시에 따라 택일.

**A — 문턱-이동 논리를 로드맵 잔여 사례로 확장.** 우선순위표상 아직 출판 안 된 사례(있다면). 새 사례도 **깨끗한 [V]인지 부분 [L]인지**를 먼저 도달성으로 판정 — 게인/학습/퇴행/안정화 축이 지배적이면 부분 적합 예상, 그 경우 B-i(명명)+B-ii(E0 동역학) 쌍으로 닫을 수 있는지 검토. **E0 양태 분류 먼저**: 새 부분-적합의 out-of-reach 축이 GAIN(쌓임·단서-반응)·DECAY(잃음)·STABILISATION(자기-지속 얼림) 중 무엇인지, 혹은 **제4의 양태**인지 판정. 셋 중 하나면 해당 B-ii 선례(§37/§39/§41) 패턴 재사용; 제4 양태면 새 읽기를 정의하되 honesty_ledger에 `*_grounded_in_engine_pathology_signal` 정직 플래그·family 관계·읽기 구별 기록.

**B — 삼부작 메타-종합(선택).** GAIN/DECAY/STABILISATION 세 양태를 한 챕터로 종합하는 capstone(같은 E0 층의 세 얼굴: 공고화 방향·읽기·임상 핸들의 대비표). 새 과학 결과 없이 세 동결 모듈(§37/§39/§41)의 교차-읽기만 — 새 측정 0. 작성 시 세 모듈 결과 JSON에서 직접 인용(GAIN trace 0.227·DECAY mass lost 5.52·STAB self-sustaining Rlock 0.40 등), 동결 sha 불변.

**C — 로드맵 다른 축.** 로드맵에 남은 T/O/W·동기화·시간 축의 미착수 항목. `RESEARCH_ROADMAP_post_autism_adhd.md`·`MISSION_atlas_redefinition.md` 상태표 확인.

**규율 리마인더 (모든 v1.49 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)=2(g/3)^1.5`, `barrier(g)=g²/4`; 동역학 rate/decay/안정화율은 [O]·부호는 스윕 견딤); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **세 게이트(`gate.py`·`run_all_atlas.py` ALL PASS·해당 단일 모듈 PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **재사용 우선**: E0 동역학 모듈은 `from e0_plasticity import PlasticConnectome` 패턴(§37 GAIN·§39 DECAY·§41 STABILISATION 선례), 공유 유전자 γ 캐시 재사용. **아틀라스 전체 재현 ~6분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행; sh에서 `disown` 불가). **새 모듈 전에** 네 부분-적합 패턴과 **세 닫힌 B-i↔B-ii 합류**(중독 GAIN·알츠하이머 DECAY·OCD STABILISATION)를 먼저 읽고 어떤 축이 도달 가능/불가인지, 어떤 E0 양태인지 먼저 정할 것. **충실-적분기 패턴(§41 신규)**: 자기-지속/IC-hysteresis 읽기가 필요한 새 모듈은 §41처럼 엔진 고정 IC서 비트-동일 가드를 먼저 통과시켜야 고착/신선 읽기가 정당화됨.

---

## 6. 변경 파일 목록 (v1.48 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `ocd_stabilisation_dynamics.py`·`ocd_stabilisation_dynamics_results.json`·`expected_ocd_stabilisation_dynamics_sha256.json`.
**신규 (docs/tools)**: `docs/mind/41-ocd-stabilisation-dynamics/index.html`·`tools/_gen_ch41_ocd_stabilisation_dynamics.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(19th citizen + coverage 문단)·`tools/mind_registry.py`(LOCK+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 42 urls·vp-cards 101·llms-full 갱신·llms.txt 바이트-동일)·`manifest/mind.csv`(41행)·`docs/mind/_meta.json`(41챕터+totals 59966)·`docs/mind/40-ocd-threshold-levers/index.html`+`tools/_gen_ch40_ocd_levers.py`(next-nav §41).
**거버넌스**: `CHANGELOG.md`(v1.48)·`HANDOVER_v1_48_to_v1_49.md`(이 문서)·`THRESHOLD_LOGIC_INHERITANCE.md`(§3.9.1·§3 표 행·§5)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터).
