# HANDOVER — v1.56 → v1.57  (E0E2-KINDLING kindling: 반복 상태-flip이 더 쉬워지는가 / 셋째 교차축 결합 E0×E2 §49 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간/공간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.56의 성격 (셋째 교차축 결합 = E0[가소성]과 E2[상태-전환]의 혼인 · §29 양극성 에피소드가 [O]로 남긴 trace→threshold 링크를 닫음 · 모델이 아니라 두 LAYER의 COUPLING).**
> v1.54가 E1(공간)과 E0(시간-가소성)을 잇는 **아틀라스 최초의 교차축 결합**(§47 SPC-E1E0, 공간-가소성 각인)을, v1.55가 E1(공간)과
> E2(상태-전환)을 잇는 **둘째 교차축 결합**(§48 SPC-E1E2, 공간 스위치 레버리지)을 짓고 그 핸드오버 §5 **경로 A(권장)**가 **셋째
> 교차축 결합 = E0×E2(가소성×상태-전환) = kindling 시간 진화**를 명시했다. §26 가소성 층은 동결 커널에 위상-Hebbian 갱신을 더해
> connectome이 **진화**하고 지속 흔적 ‖dW‖를 보유하게 했고, §28 상태-전환 층은 동결 **쌍안정** 셀(`ds/dt=g·s−s³+h`, M11/theta-cap/
> 뇌전증과 같은 fold)을 **시간에 걸쳐** 써서 fold·hysteresis·임계 latency를 확립했으며, §29 양극성 에피소드(B3)가 그 셀을 import해
> 교대 에피소드가 connectome trace를 **심화**함을 보였으나 — **trace→threshold 결합**(누적 trace가 역치를 **어떻게** 낮추는가)을
> 명시적으로 **[O]로 남겼다**(조건문에서 멈춤: 만약 누적 에피소드가 장벽을 낮춘다면 주기가 가속하리라). v1.56이 그 [O]를 닫는다 = 두
> 층 모두 import해 어느 층도 단독으로 못 묻는 질문(E0엔 쌍안정 flip 없어 쉽게 만들 flip이 없고·E2엔 진화하는 connectome 없어 반복이
> 축적 불가)을 묻는다 = **반복 flip이 단일 집합 쌍안정 상태를 더 쉽게 만드는가**. **핵심 정직성·새 발견(K3 정직한 음성).** 결합이
> 드러내는 것: **kindling은 공고화적 not 퇴행적** — '반복 violent flip이 협응을 **침식**해 더 쉽게 flip한다(더-kindled = 덜-협응)'
> 깨끗한 가설이 **거부**된다: flip 역치가 내려가는(K1) 동안 협응 R(W)이 비결맞음으로 떨어지지 않고 **상승**(0.3896→0.3964)하고 kindled
> connectome이 앵커 **이상**으로 끝난다 = **easier-to-flip과 degraded-coordination이 디커플링**, 역치는 **공고화로** 떨어짐(네트워크가
> 흩어지기를 배우지 않고 **전이를 배움**). 4결과 전부 CONFIRMED(율×장벽 **이중 스윕** 생존) + S5 영-가소성(η=0)이 M9 앵커 bit-for-bit·
> 영 push가 E.settle로 bit-for-bit(E0.4·E2.4 **이중** 상속). **이로써 셋째 교차축 결합(E0×E2) 완성 = §29 trace→threshold [O]
> 닫힘 = 세 교차축 결합(E1×E0 §47·E1×E2 §48·E0×E2 §49) 모두 존재.**

---


## 1. WHAT v1.56 DELIVERED (complete, 세 게이트 green)

### 1.1 §49 E0E2-KINDLING kindling: 반복 상태-flip이 더 쉬워지는가 (the COUPLING) · **셋째 교차축 결합 · §26 가소성 층(진화하는 connectome) × §28 상태-전환 층(쌍안정 flip) · §29 양극성 에피소드가 [O]로 남긴 trace→threshold 링크를 닫음**

- **단일 검증기.** `repro/mind/_verify/e0e2_kindling.py` (결과 sha **`3880e63ff23d43b10506824fdf7b6b5c54cee19ef73e3e4bd6369079e31aa9f0`**; 결정론 2× 검증). §48 SPC-E1E2 템플릿과 **동형**(4 부수연구 K1–K4 + S5 가드·`_canon`/`_blob`/2×sha256·자가-검증 sha writer)이나 **두 시간 층(가소성 E0·상태-전환 E2)을 import**하는 점·M9 Kuramoto 앵커 **그리고** `static_limit_is_E_settle`(E2처럼) **둘 다** 가드하는 점(E0.4 + E2.4 이중 상속)이 신규.
- **재사용(양쪽·재유도 아님).** §26 `from e0_plasticity import PlasticConnectome, W0, OMEGA, KAP, M9_ANCHOR_R, FOLD, …` (진화하는 connectome·위상-Hebbian 규칙·순서변수 기계) **그리고** §28 `from e2_state_switching import BistableSwitch, GG, DT, SETTLE_N` (쌍안정 셀·fold·`relax`·`crossing_latency`). **둘 다 재유도 금지**(핸드오버 재사용 규율), 엔진 import READ-ONLY byte-unchanged. **유일한 새 객체는 둘을 잇는 `KindlingSwitch`**(§28 셀을 §26 connectome 통해 구동 — `self.pc=PlasticConnectome()`·`self.cell=BistableSwitch(g)`).
- **결합 모델·형식 강제[F]·이중 스윕[O].** flip 에피소드 = 집합 상태의 지속 여기(§29가 에피소드를 모델한 그대로, 강한 흥분성 또는 복귀 시 억제성 바이어스를 네트워크에 구동), §26 가소성이 돌고 있으므로 각 에피소드가 **공고화**(위상-Hebbian 갱신이 지속 흔적 ‖dW‖를 connectome에 써 넣음); 반복 flip(교대 up/down)이 그 흔적 누적. 뒤집히는 것은 §28의 **단일 집합** 쌍안정 상태이므로, 외부 push p가 그 집합 상태를 얼마나 미는가 = connectome의 **협응 게인(coordination gain)** `L(W) = R(W)/R_anchor`(측정 결합서의 순서변수 R(W)를 동결 M9 앵커 R(W0)=0.38961455156044245로 정규화 = **순수 readout**, W=W0서 L=1; §48 결합이 **초점** 구동을 노드의 방송 레버리지로 스케일한 것을 **전역** 결맞음 게인으로 일반화). 유효 구동 `h_eff(p)=p·L(W)`; 상태는 **DOWN 고정점 s0=−√g**서 출발해 `h_eff`가 fold `spinodal(g)`(M11/theta-cap/뇌전증/E2와 **같은** fold, spinodal(1.0)≈0.3849)를 넘으면 뒤집힘 → flip 역치 `p* = spinodal(g)/L(W)` = connectome 공고화로 L이 커지면 **내려감**. 가소성 율 η∈**{0.03,0.05,0.08}** **그리고** 장벽 깊이 g∈**{0.7,1.0,1.3}**(g=1.0 엔진 보편 R19 스케일) 둘 다 [O] 스윕이고 **모든 부호는 율×장벽 전 곱 그리드 생존 요구**(anti-tuning).
- **4결과 전부 CONFIRMED(preregistered_results K1–K4 전부 status=CONFIRMED):**
  - **K1 (the discriminant) 반복 flip이 flip 역치를 내림·장벽-불변**: 보유 trace ‖dW‖가 **strictly-monotone 심화**(0→0.059→0.112→0.168→0.221→0.275→0.327→0.376→0.425, 8 에피소드 = §26 공고화 신호·§29 trace-심화) AND flip 역치 `p*=spinodal(g)/L(W)`가 un-kindled fold **아래로** 끝남(g=1.0: fold 0.3849 → kindled 0.3783, 순 하강 ≈0.0066) = **반복 flip이 더 쉬워짐**(kindling). **장벽-불변**: 매 우물 깊이서 kindled 역치가 **그 깊이 자신의** fold 아래(g=0.7: 0.2254→0.2216; g=1.3: 0.5705→0.5608, 역치가 spinodal(g)/L이라 공고화가 fold를 **같은** 게인으로 매 깊이서 재스케일). **반복 flip이 역치를 낮추는지는 공고화하는 connectome의 속성이지 우물 깊이가 아님**. 이것이 §29(B3)가 명명만 하고 [O]로 남긴 trace→threshold 결합, 이제 공급됨. grade `[V mech]`.
  - **K2 hysteresis의 학습된 변화·더 빠른 onset**: push-space **hysteresis 루프가 좁아짐**(폭 `2·spinodal(g)/L(W)`, 0.770→0.757, §28 hysteresis가 만든 상태-간 구간이 반복으로 **재성형** = 상태-전환 hysteresis의 **학습된** 변화) AND **고정** 초-역치 push서 교차 **latency 짧아짐**(≈4.96→≈4.72, L이 커지며 같은 push가 더 큰 유효 구동 p·L을 만들어 fold를 더 넘고 onset이 더 빠름, §28 ictal-onset 시간경과를 **반복으로** 단축). 둘 다 에피소드 수에 순-단조, 크기 [O]·방향만 단언. grade `[V mech]`.
  - **K3 (진짜 새 결합 결과 + 정직한 음성) kindling은 공고화적 not 퇴행적**: 깨끗한 침식 가설('반복 violent flip이 협응을 **침식**해 더 쉽게 flip한다 = 더-kindled connectome = 덜-협응 = 닳은 트랙')이 **거부**됨 — 반복 flip이 역치를 낮추는(K1) 동안 협응 R(W)이 비결맞음으로 떨어지지 **않고** **상승**(동결 앵커 0.3896→0.3964)하고 kindled connectome이 앵커 **이상**으로 끝남(더 쉽게 뒤집는 connectome이 **더** 강하게 협응, 덜이 아님). 그래서 **easier-to-flip과 degraded-coordination이 디커플링** — 역치는 **공고화로** 떨어짐(§26 위상-Hebbian 갱신이 반복 전이를 connectome 구조에 써 넣어 push가 작용하는 협응 모드를 강화, 침식으로가 아님). **정직한 caveat 공개**: 가장 낮은 율 η=0.03서 첫 단일 여기가 협응을 무시할 만큼 앵커 아래로 한 에피소드 nudge한 뒤 공고화가 지배해 순-상승(η≥0.05서는 한 번도 dip 안 함); 거부는 **순** 부호(kindled connectome이 더 협응으로 끝남)이지 step-별 주장 아님. **결합이 진술하는 데 필요한 이유**: §26 단독은 공고화 보이나 flip 없고·§28 단독은 flip 보이나 협응 변할 수 없는 동결 connectome이라, **둘 함께만** 협응을 올리는 같은 공고화가 flip 역치도 낮춤을 보일 수 있음. 거부된 깨끗한 가설은 강요 않고 정직히 보고(무-튜닝 규율). grade `[V mech]`.
  - **K4 단일 일관 공고화 솔기·trace가 kindling 변수**: 셋이 **한 현상** — 모든 flip 에피소드가 보유 trace(E0)를 남기고 그 trace가 다음 flip 역치를 낮춤(§28 fold 통해). 역치가 에피소드 **수**가 아니라 **누적 trace** ‖dW‖에 monotone-감소 = **trace가 kindling 변수**(§29가 남긴 명시적 trace→threshold 법칙: 역치가 반복이 **써 넣은 구조 trace의** 감소 함수, 깊은 trace일수록 낮은 역치); 율 스윕 전체서 세 부호 공동성립(trace strictly-up·역치 net-down·R net-up). **방향-전용 [L] 대응**: 임상 **kindling**(Goddard 전기적 kindling, 반복 sub-threshold 자극이 발작 역치를 점진적으로 낮춤)·양극성 **주기 가속**(에피소드가 illness 경과 따라 더 쉽게 재발)이 반복이 다음 전이 역치를 낮추는 인정된 현상, 보유 trace가 다음 flip을 쉽게 함과 방향-정합, **환자-수준 예측 절대 아님**. grade `[V mech]` 구조 + `[L]` 인용 대응.
- **S5 엔진-불변 가드(이중 상속)**: (E0.4) η=0이면 connectome 동결·R = 동결 M9 앵커 **bit-for-bit**(`R_eta0 == R_ANCHOR`)·게인 L=1·역치 = un-kindled fold(`thr_is_fold`); (E2.4) 영 push면(h_eff=0) 집합 상태 E.settle로 **bit-for-bit 정착**(`repr(E.settle(...)) == repr(BistableSwitch.relax(...))`)·DOWN 상태 spurious flip 없이 DOWN 유지·fold E.spinodal서 읽음. 두 극한 모두 동결 엔진을 잔여 없이 복원 = 진화하는 위상-Hebbian connectome 통해 집합 쌍안정 상태를 구동하는 것이 두 동결 층의 **읽기**이지 어느 쪽 수정이 아님.
- **honesty_ledger**: medium_efficacy_tested=0·no_cure_claimed=1·consciousness_claim=0·hard_problem_open=1·new_tuned_constants=0·collective_state_is_structural=1·reuses_E0_plasticity=1·reuses_E2_state_switching=1·**couples_E0_and_E2=1**·**closes_bipolar_trace_to_threshold_owed=1**·coordination_gain_is_connectome_readout=1·**kindling_is_consolidative_not_degradative=1**·erosion_hypothesis_refuted·plasticity_rate=[O] 스윕·barrier_depth_g=[O] 스윕(장벽-불변)·clinical_prediction=NONE·not_medical_advice=1·**third_cross_axis_coupling=1**.

### 1.2 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **27번째 시민 E0E2-KINDLING** 등록(MODULES 튜플을 **SPC-E1E2 직후·E0-SYNTH 직전**에 배치 — 결합하는 E0 PlasticConnectome 층과 E2 BistableSwitch가 먼저 재생성, E0-SYNTH가 마지막 시민으로 유지; 도크스트링 주석 신설). invariants(engine_tree_unchanged·static_limit_is_E_settle·eta0_R_anchor_bitwise)·honesty(eff=0·cc=0·tuned=0·no_cure=1)·preregistered(K1–K4) 전부 아틀라스 게이트 통과.
- 신규 영어 챕터 **§49 「Kindling — do repeated state-flips become easier?」**(model **3806w** [gate body wordcount], **9 H2** 영어-전용 본문 + **4결과 대조표 1개**, position 49, canonical correct, **마지막 챕터**). 아카이벌 생성기 `_gen_ch49_kindling.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `e0e2_kindling`(grade **`[V mech]`**, canonical "49-kindling", check=None). CITES=[자기, **plasticity_consolidation**(§26, E0 가소성 층 — 진화하는 connectome·위상-Hebbian 규칙·순서변수의 출처), **state_switching**(§28, E2 상태-전환 층 — R19 쌍안정 셀·fold·hysteresis의 출처), **bipolar_state_switching**(§29, kindling 형제 — trace→threshold [O]를 닫는 양극성 에피소드)] — **4 vp-card**(셋째 교차축 결합). ANSWERS 51단어(40–60) 통과.
- **§48 next-nav 신설**: §48 빈 `<span>`→§49 링크(생성기·렌더 양쪽). §49 nav = prev §48 + paper contents + 빈 span(**마지막 챕터**).
- registry **60 locks / 49 chapters**. manifest·`_meta.json` reconcile(49행/49챕터, §49=3806w·tables=1·grade=model, totals.words 82750→**86556**·totals.tables 9→**10**). vp-cards 130(§49 +4).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → registry OK(**60 locks, 49 chapters**, values match frozen results; `validate()`가 빈 리스트 반환=드리프트 0).
- `python3 tools/gate.py` → **PASS, 0 hard fail**(전 챕터 answer-first·구조·결정론; §49 answer-first 51w·4 vp-card·JSON-LD·sitemap 50/50·llms 4989B 바이트-동일·idempotent·body wordcount 매니페스트 2% 이내[§49=3806w]). 이번 빌드에서 **235/235** green 확인.
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 27/27**, engine 파일 byte-unchanged, **62 CONFIRMED 0 REFUTED**. (아틀라스 전체 재현 ~15분; 모듈마다 엔진 재-emerge. E0E2-KINDLING은 SPC-E1E2 직후·E0-SYNTH 직전 시민.)
- `python3 repro/mind/_verify/e0e2_kindling.py` → **PASS**(4 결과 K1–K4 + S5 가드 + 결정론 2× + 기대-sha 일치 `3880e63f…`).


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- R19 barrier `B(g)=g²/4` → `E.barrier(1.0)=0.25`; R19 fold `E.spinodal(1.0)=0.38490017945975047`; KAPPA_EPHAPTIC=0.5496. OMEGA0=118.85692206081383(F0 평균).
- E1-SPATIAL(§43) 결과 sha(동결): `48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44`.
- FOC-EPI-E1(§44) 결과 sha(동결): `7bbf6a338133080ce0090a44fb3971f2287cd3799688c3b16ccd8e8cff39094b`.
- LESION-E1(§45) 결과 sha(동결): `d525a66eeb0b1736f572690b79955f527a6dc8fd6a96f2093212dfb9693a5b76`.
- NEUROMOD-E1(§46) 결과 sha(동결): `cfe754e883c0d71351f030b2fc59c1d014be60ec189ac9e964959c9138a09434`.
- SPC-E1E0(§47) 결과 sha(동결): `cdb1623009fe2a02818c00be5fd2243034d43880501fde89b75270e0574ec036`.
- SPC-E1E2(§48) 결과 sha(동결): `bd3a9e230a4304371bc17ced39e7ae08b5c0dcf99855c9842f3eaea84ab7ea4e`.
- **E0E2-KINDLING(§49) 결과 sha(신규 동결): `3880e63ff23d43b10506824fdf7b6b5c54cee19ef73e3e4bd6369079e31aa9f0`.**
- **kindling 프로토콜 상수(§49, 전부 [O] 스윕 또는 대표값).** B_MAG=0.30(flip 바이어스 크기)·EP_LEN=3(에피소드당 가소성 epoch)·EPISODES=8·ETA_SWEEP={0.03,0.05,0.08}(가소성 율)·BARRIER_SWEEP={0.7,1.0,1.3}(우물 깊이 g)·ETAREP=0.05(대표 율)·GREP=1.0(대표 장벽=엔진 R19 스케일)·PTEST=0.50(latency용 고정 초-역치 push). **협응 게인 L(W)=R(W)/R_anchor**(순수 readout, W0서 =1); **flip 역치 p*=spinodal(g)/L(W)**(공고화로 내려감); **hysteresis 루프폭 2·spinodal(g)/L(W)**(공고화로 좁아짐).
- **인증 표제값(§49 결과 JSON, 본문/표 정합).** K1 trace strictly-mono 0→0.425(8 에피소드)·flip 역치 g=1.0서 0.3849→0.3783(순 하강 ≈0.0066)·장벽-불변(g=0.7: 0.2254→0.2216·g=1.3: 0.5705→0.5608). K2 루프폭 0.770→0.757·latency 4.96→4.72. K3 R(W) 0.3896→0.3964(순-상승, dR≈+0.0068)·kindled connectome이 앵커 이상으로 끝남·η=0.03서 첫 에피소드만 무시할 transient dip(정직 공개). K4 역치가 누적 trace에 monotone-감소·trace가 kindling 변수·[L] 방향(Goddard kindling·양극성 주기 가속). S5 η=0서 R==M9 앵커 bit-for-bit·역치==un-kindled fold·영 push서 E.settle bit-for-bit.
- **§49 결합 vs §47 공간-가소성 각인 / §48 공간-상태전환 / §29 시간-flip(중요).** §47(E1×E0)은 초점 구동이 **어디** 지속 표지를 남기는가(국소/중계 각인). §48(E1×E2)은 **어느** 초점 구동이 단일 집합 쌍안정 상태를 가장 싸게 뒤집는가(방송 레버리지가 순서). §49(E0×E2)는 **반복** flip이 단일 집합 쌍안정 상태를 더 쉽게 만드는가(협응 게인 공고화가 역치를 낮춤 = kindling). **§29와의 관계**: §29(B3)는 교대 에피소드가 trace를 **심화**함을 보였으나 trace→threshold 결합을 **[O]로 남겼고**, §49가 그것을 닫음(누적 trace가 역치를 낮춤·trace가 kindling 변수, K1/K4). §29의 **시간** 형제이자 §29 [O]의 **공급자**.
- **E0 층(§26)·E2 층(§28)·교차축 결합(§49) 관계 — 셋째 결합.** §26이 가소성(진화하는 connectome·위상-Hebbian·지속 흔적)을 인증한 **층**, §28이 상태-전환(쌍안정 셀·fold·latency)을 인증한 **층**, §49가 **둘을 잇는 셋째 교차축 결합**(반복 flip이 §26 가소성을 구동해 connectome 공고화·그 협응 게인이 §28 flip 역치를 낮춤). 두 층 모두 import, 커널/규칙/셀/fold 재유도 안 함. 유일한 새 객체는 `KindlingSwitch`. **§47이 최초 교차(E1×E0), §48이 둘째(E1×E2), §49가 셋째(E0×E2) — 세 교차축 결합 모두 존재.**


## 4. THE FIREWALL (YMYL/medical, 오독 방지 · 절대)
집합 쌍안정 상태와 그 flip 역치·보유 trace ‖dW‖·협응 게인 L(W)·hysteresis 루프폭·교차 latency — 인증된 모든 양 — 은 **결합** 모델이 단일 쌍안정 집합 상태의 역치를 반복 flip이 진화하는 위상-Hebbian connectome을 구동하며 낮추는 방식의 **구조적 양**이고, **느껴진 상태·경험된 기분·의식 수준·경험된 재발-용이성이 절대 아니며**(집합 상태가 반복으로 더 쉽게 "뒤집힌다"는 건 모델의 쌍안정 변수가 더 낮은 구동서 0을 교차한다는 진술이지 경험이 kindle한다는 진술이 아님), **실제 connectome·시냅스-가중 행렬이 아니고**(연결성은 동결 ~1/r³ 커널 + 위상-Hebbian readout이지 실제 시냅스 가소성이 아님), **실제 kindling/발작 역치 측정이 아니며**, **어느 환자의 에피소드가 가속할지의 예측이 아님**(Axis-A·consciousness_claim=0·hard problem OPEN). 실제 kindling·주기 가속은 **이질적**(altered gene expression·이끼섬유 발아(mossy-fibre sprouting)·수용체 trafficking·망 재조직·allostatic load)이라 동결 두 층 위 반복 flip이 협응 게인으로 스케일된 유효 구동 하 집합 flip 역치를 낮추는지의 **부호/방향만** 단언(실제 kindling이 이 정확한 규칙을 따른다 주장 안 함); 모든 **크기 [O]**(스윕 율·장벽의 대표 읽기). 어느 환자의 에피소드가 가속할지·얼마나·무엇을 할지는 **외부 임상 판단**(임상의가 실제 병력·전기생리·개별화 평가로); K4의 [L] 대응은 **방향**(임상 kindling·주기 가속이 반복이 다음 전이 역치를 낮추는 현상)의 인용 유사성이지 환자-수준 주장이 아님. **신규 기계(둘을 잇는 KindlingSwitch 외)·신규 측정(READ-ONLY 층 외)·신규 튜닝 상수 전무**(PlasticConnectome와 BistableSwitch import READ-ONLY·엔진 byte-unchanged). efficacy=0, NOT medical advice, 치유·예후·기기-설정 없음.


## 5. v1.57 ENTRY POINTS (next session)

**셋째 교차축 결합(E0×E2)이 완성됐다**(§49 kindling = §29 trace→threshold [O] 닫힘). **이제 세 교차축 결합 모두 존재**(E1×E0 §47 공간-가소성·E1×E2 §48 공간-상태전환·E0×E2 §49 가소성-상태전환). 다음은 **교차축 결합 메타-종합 캡스톤**(가장 자연스러움, §42 패턴), 또는 추가 응용, 또는 로드맵 잔여로 전진.

**A — 교차축 결합 메타-종합 캡스톤 [권장·가장 자연스러움·최저-위험].** E0 삼부작이 §42 메타-종합 캡스톤으로 닫혔듯(GAIN/DECAY/STABILISATION을 단일 E0 층의 세 읽기로 인증), **이제 세 교차축 결합이 모두 존재하므로** 그것들을 메타-종합 캡스톤으로 닫을 수 있다 — **E1×E0(§47 공간-가소성 각인)·E1×E2(§48 공간-상태전환 레버리지)·E0×E2(§49 가소성-상태전환 kindling)** 을 단일 종합으로(새 측정 0·새 기계 0·소스 SHA 재검증 후 읽기, §42 4규율: `new_measurement=0`/`is_a_synthesis_of_frozen_modules=1` 선언·소스 SHA를 읽기 전에 재검증·아틀라스 시민 등록 시 **맨 끝** 배치·본문 인용값은 종합 결과 JSON에서만). **종합의 헤드라인 후보**: 세 결합이 공통적으로 **단일-축 결과를 디커플링**한다 — §47 C3(깨끗한 전달 ≠ 깨끗한 각인)·§48 C3(스위치성이 발자국·도달 둘 다와 디커플링)·§49 K3(easier-flip이 침식과 디커플링, kindling은 공고화적). 세 솔기를 "공간이 시간을 만나면(각인 §47)·공간이 상태를 만나면(flip §48)·시간이 상태를 만나면(kindling §49)" 디커플링/뒤집기 관점에서 나란히 프레이밍. 세 결합이 모두 동결됐으므로 삼중 종합이 깨끗함(§42가 E0 삼부작 닫은 그대로). **착수 전**: 세 소스 결과 JSON sha 재검증 → 읽기, 엔진 READ-ONLY emerge byte-unchanged, 종합 인증(T1 단일 교차축 결합군·T2 각 결합의 새 객체[적분기/스위치]·T3 세 디커플링·T4 공통 패턴·T5 단일 결합 규율 등 §42 구조).

**B — 교차축 결합의 추가 응용(선택).** §48/§49의 자연스러운 변주: (i) **억제성** 구동(병변)이 집합 상태를 어느 부위서 가장 쉽게 **아래로** 뒤집는가(§45 LESION-E1의 상태-전환 형제 = E1×E2 변주), (ii) **여러 노드 동시** 구동의 leverage 합이 flip을 어떻게 바꾸는가(focal vs distributed 자극의 flip 효율 = §43 E1.4 무-법칙의 상태-전환 판), (iii) **공간-국소화된** kindling(어느 부위의 반복 flip이 가장 빨리 kindle하는가 = E1×E0×E2 삼중 결합 — 단, §49는 노드별 게인이 아닌 전역 게인이라 §43 E1 층의 per-node 구동 추가 필요, 도달성 선판단 필수). 같은 층 재사용, 구동 부호/분포/공간성만 다름. 도달성 선판단 후 착수.

**C — 문턱-이동 논리 로드맵 잔여 사례.** 우선순위표상 아직 출판 안 된 사례(있다면). 새 사례도 **깨끗한 [V]인지 부분 [L]인지** 도달성 선판단 — 게인/학습/퇴행/안정화/공간/결합 축 중 무엇이 지배적이면 부분 적합 예상.

**규율 리마인더 (모든 v1.57 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인 — 영 구동이 엔진 정착/앵커 bit-for-bit); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)`, `barrier(g)=g²/4`; 동역학 율·공고화 율·공간 프로파일·자극 심도·장벽 깊이·push 강도는 [O]·부호는 (이중) 스윕 견딤; **협응 게인 L(W)=R(W)/R_anchor·방송 레버리지 lev_j는 frozen/evolving-kernel readout이지 새 상수 아님**); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **세 게이트(`gate.py`·`run_all_atlas.py` ALL PASS·해당 단일 모듈 PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **교차축 결합 패턴(§47/§48/§49)**: 두 층을 잇는 결합은 (a) 두 재사용 층을 import(재유도 금지), (b) 결합 객체/적분기 하나만 새 작성(`LeverageSwitch`/`_integrate_coupled`/`KindlingSwitch` 류), (c) 두 축 파라미터(강도·율·장벽 등)를 **둘 다 스윕**해 곱 그리드서 부호/순서 생존, (d) 양 파라미터=0(또는 영-구동) 가드로 엔진 bit-for-bit 복귀(두 층 가드 상속 — E2 결합이면 `static_limit_is_E_settle`·E.settle, E0 결합이면 M9 앵커·η=0; **E0×E2 결합이면 둘 다**), (e) 결합이 단일-축 결과를 **뒤집거나 디커플링**하면 그것이 발견 — 강요 말고 **정직히 보고**(§47 C3/C4·§48 C3·§49 K3 무-튜닝 규율, 특히 §49 K3은 깨끗한 침식 가설을 거부한 정직한 음성). **메타-종합 패턴(§42, 경로 A)**: (a) `is_a_synthesis_of_frozen_modules=1`/`new_measurement=0` 선언, (b) 소스 SHA를 **읽기 전에** 재검증(1바이트 표류 시 실행 거부), (c) 아틀라스 시민 등록 시 **맨 끝** 배치(소스 먼저 재생성), (d) 본문 인용값은 종합 결과 JSON에서만. **마지막 챕터 nav**: 새 챕터가 마지막이면 nav = prev + paper contents + 빈 `<span>`; 직전 마지막 챕터의 빈 span을 새 챕터 next-link로 교체(생성기·렌더 양쪽). **아틀라스 전체 재현 ~15분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행).

---

## 6. 변경 파일 목록 (v1.56 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `e0e2_kindling.py`·`e0e2_kindling_results.json`·`expected_e0e2_kindling_sha256.json`.
**신규 (docs/tools)**: `docs/mind/49-kindling/index.html`·`tools/_gen_ch49_kindling.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(27th citizen E0E2-KINDLING를 SPC-E1E2 직후·E0-SYNTH 직전 배치 + 주석)·`tools/mind_registry.py`(LOCK `e0e2_kindling`+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 50 urls·vp-cards 130·llms-full 갱신·llms.txt 바이트-동일 4989B)·`manifest/mind.csv`(49행)·`docs/mind/_meta.json`(49챕터+totals.words 86556·tables 10)·`docs/mind/48-spatial-switch-leverage/index.html`+`tools/_gen_ch48_spatial_switch_leverage.py`(next-nav §49).
**거버넌스**: `CHANGELOG.md`(v1.56)·`HANDOVER_v1_56_to_v1_57.md`(이 문서)·`MISSION_atlas_redefinition.md`(E0×E2 셋째 교차축 결합 DONE)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터 v1.56).
