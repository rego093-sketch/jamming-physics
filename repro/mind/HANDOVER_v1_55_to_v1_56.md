# HANDOVER — v1.55 → v1.56  (SPC-E1E2 공간 스위치 레버리지: 어느 초점 구동이 집합 상태를 가장 쉽게 뒤집는가 / 둘째 교차축 결합 E1×E2 §48 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간/공간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.55의 성격 (둘째 교차축 결합 = E1[공간]과 E2[상태-전환]의 혼인 · §29 양극성 에피소드의 공간 형제 · 모델이 아니라 두 LAYER의 COUPLING).**
> v1.54가 E1(공간)과 E0(시간-가소성)을 잇는 **아틀라스 최초의 교차축 결합**(§47 SPC-E1E0, 공간-가소성 각인 = 초점 구동이 어디 지속
> 각인하는가)을 짓고 그 핸드오버 §5 **경로 A(권장)**가 **둘째 교차축 결합 = E1×E2(공간×상태-전환)**를 명시했다. §28 상태-전환 층은
> 엔진의 동결 **쌍안정** 셀(`ds/dt=g·s−s³+h`, M11/theta-cap/뇌전증과 같은 fold)을 **시간에 걸쳐** 써서 fold·hysteresis·임계
> latency(critical slowing)를 확립했고, §29가 그 셀을 import해 집합 기분 상태가 **언제(WHEN)** 시간 구동 하에 뒤집히는지 물었다.
> 그러나 §29는 셀을 **단일 스칼라** 구동으로 몰았으므로 **어디(WHERE)** 초점 구동이 가장 싸게 뒤집는지 물을 수 없었다(모든 영역이 같은
> 스칼라 h). §43 공간 층은 어디는 있었으나 초점 구동을 **순간 장**으로 읽어 뒤집을 쌍안정 상태가 없었다. v1.55는 그 둘을 **혼인**시킨다
> = 단일 집합 쌍안정 상태(§29가 쓴 **바로 그** BistableSwitch 객체)를 유지하고 **어느 영역의 초점 자극이 그것을 가장 쉽게 뒤집는가**를
> 묻는다 = §29가 **언제**를 물은 곳에서 이 챕터는 **어디**를 묻는다 = **§29 양극성 에피소드의 공간 형제**. **핵심 정직성·새 발견(C3
> 디커플링).** 결합이 드러내는 것: **스위치성이 §46 순간-발자국 축 AND §43 도달 축 둘 다와 디커플링** — §46 장-중계 집합 {hippocampus,
> midbrain}은 스위치 레버리지서 MID-rank(특별치 않음)이고 스위치 허브 basal_forebrain_chol은 §46 self-localising(깨끗 전달); 그리고
> **§43 도달 허브 cerebellum이 스위치-rank 10/12**(가장 어려운 축) = **보편 reach→switchability 법칙 부재**(멀리 도달함·깨끗하게
> 전달함·집합 상태를 뒤집음은 세 다른 속성, 방송 **레버리지**만이 어느 구동이 뒤집는지 매김). 4결과 전부 CONFIRMED(강도×장벽 **이중
> 스윕** 생존) + S6 영-구동(b0=0→h_eff=0)이 E.settle로 bit-for-bit 정착·fold는 E.spinodal서 읽음(E2.4 상속). **이로써 둘째
> 교차축 결합(E1×E2) 완성 = §29의 공간 형제.**

---


## 1. WHAT v1.55 DELIVERED (complete, 세 게이트 green)

### 1.1 §48 SPC-E1E2 공간 스위치 레버리지: 어느 초점 구동이 집합 상태를 가장 쉽게 뒤집는가 (the COUPLING) · **둘째 교차축 결합 · §43 공간 층(어디) × §28 상태-전환 층(쌍안정 뒤집기) · §29 양극성 에피소드의 공간 형제**

- **단일 검증기.** `repro/mind/_verify/spatial_switch_leverage.py` (결과 sha **`bd3a9e230a4304371bc17ced39e7ae08b5c0dcf99855c9842f3eaea84ab7ea4e`**; 결정론 2× 검증). §47 SPC-E1E0 템플릿과 **동형**(4 부수연구 C1–C4 + S6 가드·`_canon`/`_blob`/2×sha256·자가-검증 sha writer)이나 **두 층(공간 E1·상태-전환 E2)을 import**하는 점·M9 Kuramoto 앵커 대신 **scalar switch + `static_limit_is_E_settle` 플래그**(E2처럼)인 점이 신규.
- **재사용(양쪽·재유도 아님).** §43 `from e1_spatial_localisation import SpatialField, REGS, N, W0, …` (공간 구동·ephaptic 커널 W0) **그리고** §28 `from e2_state_switching import BistableSwitch, GG, FOLD, …` (쌍안정 셀·fold·`relax`·`crossing_latency`). **둘 다 재유도 금지**(핸드오버 재사용 규율), 엔진 import READ-ONLY byte-unchanged. **유일한 새 객체는 둘을 잇는 `LeverageSwitch`**(§28 셀에 동결 커널 broadcast leverage를 먹임).
- **결합 모델·형식 강제[F]·이중 스윕[O].** 초점 자극 = §46/§47과 같은 노드별 **흥분성 바이어스**(한 영역, 나머지 baseline). 구동되는 것은 노드별 장이 아니라 §28의 **단일 집합** 쌍안정 상태이므로, 초점 구동이 **전체** 상태를 얼마나 미는가 = 구동 노드의 **방송 레버리지(broadcast leverage)** `lev_j = W0.sum(0)[j] = Σ_i W0[i,j]`(동결 커널 열 합 = 노드 j가 네트워크에 주입하는 총 1-스텝 ephaptic 전류) = **순수 frozen-kernel readout**(새 메커니즘·새 상수 0). 유효 구동 `h_eff(j,b0) = b0·lev_j`; 상태는 **DOWN 고정점 s0=−√g**서 출발해 `h_eff`가 fold `spinodal(g)`(M11/theta-cap/뇌전증/E2와 **같은** fold)를 넘으면 뒤집힘 → 강도 역치 `b0* = spinodal(g)/lev_j` = **레버리지에 반비례**. 자극 강도 b0∈**{0.3,0.5,0.7,0.9}** **그리고** 장벽 깊이 g∈**{0.7,1.0,1.3}**(g=1.0 엔진 보편 R19 스케일) 둘 다 [O] 스윕이고 **모든 부호/순서는 강도×장벽 전 곱 그리드 생존 요구**(anti-tuning).
- **4결과 전부 CONFIRMED(preregistered_results C1–C4 전부 status=CONFIRMED):**
  - **C1 (the discriminant) flip-threshold 순위 = 방송-레버리지 순위·장벽-불변**: 각 영역에 초점 자극을 구동하고 집합 상태가 뒤집히는 최소 강도를 물으면 12 부위가 얼마나 싸게 뒤집는가로 순위 매겨지고, 그 적분 순위가 동결 커널서 곧장 계산한 방송-레버리지 순위와 **동일**. 가장 싼 뒤집기 = 최고-레버리지 허브 **basal_forebrain_chol**(lev≈1.79, b0≈0.22 @g=1.0), 레버리지 따라 단조로 **hypothalamus**(lev≈1.63, b0≈0.24)·forebrain_gaba_in·neocortex·hippocampus·midbrain 군집(b0≈0.28–0.30)·pallidum(0.40)·striatum(0.60)·brainstem(0.74)·cerebellum(겨우, b0≈1.0)까지; 두 부위 **{thalamus, olfactory_bulb}**(lev≈0.21,0.22)는 **어느 스윕 강도서도(b0≤1) 절대 안 뒤집힘** = **고정 비전환 소수**. 순위는 장벽 스윕 {0.7,1.0,1.3} 공통 finite-threshold 집합서 **동일**(b0*=spinodal(g)/lev라 깊은 우물은 모든 역치를 함께 올리나 재정렬 못함). **어느 초점 구동이 집합 상태를 가장 싸게 뒤집는가는 동결 커널 방송 구조의 고정 속성**(장벽 깊이도 강도도 아님). grade `[V mech]`.
  - **C2 뒤집기-용이성이 방송 레버리지 추적 + critical slowing**: 역치가 레버리지에 단조 **감소**(b0*=spinodal/lev), AND **고정** 초-역치 강도(b0=0.9)서 교차 **latency**(상태가 실제 뒤집는 데 걸리는 시간)도 레버리지에 단조 감소(basal_forebrain ≈0.72 → brainstem ≈5.68) = 고-레버리지 허브는 더 **싸게 AND 빠르게** 뒤집음. 뒤집는 최저-레버리지 부위 **brainstem**이 **가장 큰** finite latency = **critical slowing**(유효 구동이 fold에 접근하며 전이 시간 발산), §28 ictal 시간-경과를 **공간 주소**로 부여. 고정 비전환 소수는 절대 교차 안 함. grade `[V mech]`.
  - **C3 (진짜 새 결합 결과 + 정직한 음성) 스위치성이 §46 순간-발자국 축 AND §43 도달 축 둘 다와 디커플링 = 보편 reach→switchability 법칙 부재**: (a) §46 순간-장-중계 집합 **{hippocampus, midbrain}**은 스위치 레버리지서 **MID-rank**(12 중 5–6, 쉽게 전환 가능, 특별치 않음)이고 스위치 허브 basal_forebrain_chol은 §46 **SELF-LOCALISING**(깨끗 전달) = 초점 구동의 **순간** 효과가 착지하는 곳과 어느 초점 구동이 집합 상태를 뒤집는가는 **두 다른 디커플링 공간 축**(E1×E2 교훈, 어느 층도 단독 진술 불가 — E1엔 쌍안정 상태 없고 E2엔 공간 프로파일 없음). (b) 거부된 깨끗한 가설을 정직히 보고 — §43/§46 **reach 허브는 CEREBELLUM**(모든 깊이 rank-1 reach, E1 결과 `e1_spatial_localisation_results.json`서 직접 읽음)인데 cerebellum은 스위치-rank **10/12** = 상태를 뒤집기 **가장 어려운** 부위 중 하나, 그리고 뒤집기-어려운 집합 **{thalamus, olfactory_bulb, cerebellum}**이 전부 §46 **SELF-LOCALISING**이면서 집합 상태를 싸게 뒤집지 **못함** = 멀리 도달함·깨끗하게 전달함·집합 상태를 뒤집음은 **세 다른 속성**, **보편 reach→switchability 법칙 부재**. 거부된 깨끗한 가설은 강요 않고 정직히 보고. grade `[V mech]`.
  - **C4 다수-전환가능 + 고정 비전환 소수(§46과의 정직한 대비)**: 엄격한 **다수**(12 중 **10**)가 스윕 초점 구동(b0≤1)으로 집합 상태를 뒤집을 수 있고, 나머지 둘 **{thalamus, olfactory_bulb}**이 고정 비전환 소수 = **다수-전환가능, 단단한 주변부 바닥** 구조. **§46의 정직한 대비**(거기선 구조적 기본값이 깨끗한 순간 **전달**, 10/12 자기-국소) — 두 챕터는 다른 것을 읽음(§46은 구동의 순간 효과가 어디 착지, 이건 어느 구동이 쌍안정 집합 상태를 뒤집는가). **방향-전용 [L] 대응**: 최고-레버리지 허브 basal_forebrain_chol·hypothalamus는 고전적 **전역 뇌상태/각성 제어 허브**(상행 각성계·기저전뇌가 수면-각성 전이·피질 상태 게이팅)이고 잠긴/가장 어려운 부위 thalamic relay·olfactory bulb·cerebellum은 주변부 감각-중계/운동-타이밍 구조 = 방송 허브가 전역 뇌상태 전환을 게이팅함과 방향-정합, **환자-수준 예측 절대 아님**. grade `[V mech]` 구조 + `[L]` 인용 대응.
- **S6 엔진-불변 가드**: 초점 구동 제거(b0=0 → h_eff=0)가 집합 상태를 **E.settle로 bit-for-bit 정착**(정적 극한이 동결 엔진 자체 = E2.4 가드 상속, DOWN 상태는 spurious flip 없이 DOWN 유지)·fold는 E.spinodal서 읽음(새 상수 0)·초점 여기가 제거되면 DOWN 끝점으로 정확히 복귀. 결합은 동결 커널 위 순수 add-on.
- **honesty_ledger**: medium_efficacy_tested=0·no_cure_claimed=1·consciousness_claim=0·hard_problem_open=1·new_tuned_constants=0·collective_state_is_structural=1·reuses_E1_spatial_field=1·reuses_E2_state_switching=1·**couples_E1_and_E2=1**·broadcast_leverage_is_frozen_kernel_readout=1·**switchability_decoupled_from_instantaneous_footprint=1**·**switchability_decoupled_from_reach=1**·reach_to_switchability_law_refuted·stimulation_intensity=OPEN[O]·barrier_depth=OPEN[O]·clinical_prediction=NONE·not_medical_advice=1·**opens_E1xE2_coupling=1**.

### 1.2 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **26번째 시민 SPC-E1E2** 등록(MODULES 튜플을 **SPC-E1E0 직후·E0-SYNTH 직전**에 배치 — 결합하는 E1 SpatialField 층과 E2 BistableSwitch가 먼저 재생성, E0-SYNTH가 마지막 시민으로 유지; 도크스트링 주석 신설). invariants(static_limit_is_E_settle 플래그)·honesty(eff=0·cc=0·tuned=0·no_cure=1)·preregistered(C1–C4) 전부 아틀라스 게이트 통과.
- 신규 영어 챕터 **§48 「Spatial switch leverage: which focal drive most easily flips the collective state」**(model **3620w** [gate body wordcount], **9 H2** 영어-전용 본문 + **4결과 대조표 1개**, position 48, canonical correct, **마지막 챕터**). 아카이벌 생성기 `_gen_ch48_spatial_switch_leverage.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `spatial_switch_leverage`(grade **`[V mech]`**, canonical "48-spatial-switch-leverage", check=None). CITES=[자기, **e1_spatial_localisation**(§43, 공간 층 어디 — SpatialField·방송 레버리지의 출처), **state_switching**(§28, E2 상태-전환 층 쌍안정 셀·fold), **targeted_neuromodulation_offtarget**(§46, 순간-발자국 짝 — 스위치성이 디커플링되는 §46 장-중계 축의 출처)] — **4 vp-card**(둘째 교차축 결합). ANSWERS 58단어(40–60) 통과.
- **§47 next-nav 신설**: §47 빈 `<span>`→§48 링크(생성기·렌더 양쪽). §48 nav = prev §47 + paper contents + 빈 span(**마지막 챕터**).
- registry **59 locks / 48 chapters**. manifest·`_meta.json` reconcile(48행/48챕터, §48=3620w·tables=1·grade=model, totals.words 79130→**82750**·totals.tables 8→**9**). vp-cards 126(§48 +4).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → registry OK(**59 locks, 48 chapters**, values match frozen results; `validate()`가 빈 리스트 반환=드리프트 0).
- `python3 tools/gate.py` → **PASS, 0 hard fail**(전 챕터 answer-first·구조·결정론; §48 answer-first 59w·4 vp-card·JSON-LD·sitemap 49/49·llms 4989B 바이트-동일·idempotent·body wordcount 매니페스트 2% 이내[§48=3620w]). 이번 빌드에서 **229/229** green 확인.
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 26/26**, engine 파일 byte-unchanged, **58 CONFIRMED 0 REFUTED**. (아틀라스 전체 재현 ~15분; 모듈마다 엔진 재-emerge. SPC-E1E2는 SPC-E1E0 직후·E0-SYNTH 직전 시민.)
- `python3 repro/mind/_verify/spatial_switch_leverage.py` → **PASS**(4 결과 C1–C4 + S6 가드 + 결정론 2× + 기대-sha 일치 `bd3a9e23…`).


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- R19 barrier `B(g)=g²/4` → `E.barrier(1.0)=0.25`; R19 fold `E.spinodal(1.0)=0.38490017945975047`; KAPPA_EPHAPTIC=0.5496. OMEGA0=118.85692206081383(F0 평균).
- E1-SPATIAL(§43) 결과 sha(동결): `48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44`.
- FOC-EPI-E1(§44) 결과 sha(동결): `7bbf6a338133080ce0090a44fb3971f2287cd3799688c3b16ccd8e8cff39094b`.
- LESION-E1(§45) 결과 sha(동결): `d525a66eeb0b1736f572690b79955f527a6dc8fd6a96f2093212dfb9693a5b76`.
- NEUROMOD-E1(§46) 결과 sha(동결): `cfe754e883c0d71351f030b2fc59c1d014be60ec189ac9e964959c9138a09434`.
- SPC-E1E0(§47) 결과 sha(동결): `cdb1623009fe2a02818c00be5fd2243034d43880501fde89b75270e0574ec036`.
- **SPC-E1E2(§48) 결과 sha(신규 동결): `bd3a9e230a4304371bc17ced39e7ae08b5c0dcf99855c9842f3eaea84ab7ea4e`.**
- **공간 좌표·영역 인덱스(E1 상속).** N=12 영역, REGS 인덱스: [0]neocortex·[1]hippocampus·[2]thalamus·[3]striatum·[4]cerebellum·[5]hypothalamus·[6]midbrain·[7]brainstem·[8]pallidum·[9]forebrain_gaba_in·[10]basal_forebrain_chol·[11]olfactory_bulb. **방송 레버리지 `lev_j = colsum_j of W0`(쉬움→어려움): basal_forebrain_chol[10] 1.7933 > hypothalamus[5] 1.6319 > forebrain_gaba_in[9] 1.4244 > neocortex[0] 1.3894 > hippocampus[1] 1.3882 > midbrain[6] 1.3826 > pallidum[8] 0.9780 > striatum[3] 0.6587 > brainstem[7] 0.5326 > cerebellum[4] 0.3932 > olfactory_bulb[11] 0.2181 > thalamus[2] 0.2095.** flip 역치 @g=1.0(b0): basal_fb 0.22·hypothal 0.24·forebrain_gaba/neocortex/hippo 0.28·midbrain 0.30·pallidum 0.40·striatum 0.60·brainstem 0.74·cerebellum 1.0. **고정 비전환 소수 = {thalamus[2], olfactory_bulb[11]}**(b0≤1서 절대 안 뒤집힘, C1/C4); **다수-전환가능 = 나머지 10**(C4). latency @b0=0.9(쉬움→어려움): basal_fb ≈0.72 → brainstem ≈5.68(critical slowing, C2). **§46 장-중계 {hippocampus[1], midbrain[6]}은 스위치 MID-rank 5–6/12**(C3); **§43 reach 허브 cerebellum[4]은 스위치-rank 10/12**(가장 어려운, C3 보편 reach→switchability 법칙 부재); 뒤집기-어려운 집합 {thalamus, olfactory_bulb, cerebellum} 전부 §46 self-localising(C3).
- **§48 결합 vs §46 순간 / §47 가소성-각인 / §29 시간-flip(중요).** §46(순간 장-전달)은 구동의 순간 효과가 어디 착지(깨끗/누출). §47(지속 흔적-각인)은 구동이 어디 지속 표지를 남기는가(국소/중계). §48(상태-flip)은 **어느 구동이 단일 집합 쌍안정 상태를 가장 싸게 뒤집는가**(방송 레버리지가 순서 결정). 세 공간 축은 **디커플링**(C3): 스위치 허브 basal_forebrain_chol은 §46 self-localising, §43 reach 허브 cerebellum은 스위치 최난. **§29와의 관계**: §29는 집합 상태가 **언제**(시간 구동 하) 뒤집히는지, §48은 **어디**(어느 초점 구동) 가장 싸게 뒤집히는지 = §48이 **§29의 공간 형제**.
- **E1 층(§43)·E2 층(§28)·교차축 결합(§48) 관계 — 둘째 결합.** §43이 공간 지도(어디 WHERE)를 인증한 **층**, §28이 상태-전환(쌍안정 셀·fold·latency)을 인증한 **층**, §48이 **둘을 잇는 둘째 교차축 결합**(focal 구동의 방송 레버리지가 §28 쌍안정 상태를 뒤집음 = 어느 구동이 집합 상태를 가장 싸게 뒤집는가). 두 층 모두 import, 커널/셀 재유도 안 함. 유일한 새 객체는 `LeverageSwitch`. **§47이 최초 교차(E1×E0), §48이 둘째 교차(E1×E2)**.
- 인용 표제값(§48 결과 JSON, 본문/표 정합): flip-threshold 순위 = 레버리지 순위·장벽-불변(C1) · 고정 비전환 소수 {thalamus, olfactory_bulb} · 역치&latency 둘 다 레버리지에 단조 감소·brainstem 최대 latency(critical slowing, C2) · §46 장-중계 {hippocampus, midbrain} 스위치 MID-rank 5–6 · reach 허브 cerebellum 스위치-rank 10/12(C3 보편 법칙 부재) · 다수-전환 10/고정 비전환 2(C4) · S6 fold spinodal(1.0)=0.3849·E.settle bit-for-bit.


## 4. THE FIREWALL (YMYL/medical, 오독 방지 · 절대)
집합 쌍안정 상태와 그 뒤집힘·flip 역치·방송-레버리지 순위·교차 latency·전환가능/비전환 분류 — 인증된 모든 양 — 은 **결합** 모델이 고정 커널 위 **단일 쌍안정 변수**를 뒤집는 방식의 **구조적 양**이고, **느껴진 상태·경험된 각성·의식 수준이 절대 아니며**(집합 상태가 "뒤집힌다"는 건 모델의 쌍안정 변수가 0을 교차한다는 진술이지 경험된 각성 변화가 거기서 일어난다는 진술이 아님), **실제 connectome·전기장·전류 밀도 지도·리드-위치/SAR(specific-absorption-rate) 지도가 아니고**(per-node bias는 실제 자극이 아님, lev_j는 영역이 뇌상태를 구동하는 실제 척도가 아님), **단일 집합 쌍안정 상태는 실제 전역 뇌상태가 아니며**, **어느 환자의 자극이 어느 뇌상태를 뒤집을지의 예측이 아니고**, **기기-프로그래밍/타깃-선택 안내가 아님**(Axis-A·consciousness_claim=0·hard problem OPEN). 실제 뇌상태 전환은 **분산 신경조절계**(상행 각성핵·기저전뇌·시상피질/피질피질 루프·다중 신경전달물질·상태-의존 전도도)이라 동결 커널 방송 레버리지가 단일 쌍안정 상태를 가장 싸게 뒤집는 **주소의 부호/순서만** 단언(실제 상태 제어가 이 정확한 규칙을 따른다 주장 안 함); 모든 **크기 [O]**(스윕 강도·장벽의 대표 읽기). 타깃 선택·리드 배치·접점/전류 프로그래밍·결과 예측은 **외부 임상 판단**(임상의가 실제 영상·전기생리·개별화 모델링으로); C4의 [L] 대응은 **방향**(방송/각성 허브가 전역 뇌상태 전환을 게이팅)의 인용 유사성이지 환자-수준 주장이 아님. **신규 기계(둘을 잇는 leverage-driven switch 외)·신규 측정(READ-ONLY 층 외)·신규 튜닝 상수 전무**(SpatialField와 BistableSwitch import READ-ONLY·엔진 byte-unchanged). efficacy=0, NOT medical advice, 치유·국소화·기기-설정 없음.


## 5. v1.56 ENTRY POINTS (next session)

**둘째 교차축 결합(E1×E2)이 완성됐다**(§48 공간 스위치 레버리지 = §29의 공간 형제). 두 교차 솔기(E1×E0 §47 · E1×E2 §48)가 읽혔다. 다음은 **세 번째** 교차축 결합, 또는 교차축 메타-종합, 또는 로드맵 잔여로 전진.

**A — 세 번째 교차축 결합(남은 쌍) [권장·가장 자연스러움].** 세 단일 축은 E0(시간-가소성)·E1(공간)·E2(상태-전환)이고, 가능한 교차 쌍 셋 중 **둘이 완료**(E1×E0 §47 · E1×E2 §48). 남은 자연스러운 결합은 **E0×E2(가소성×상태-전환)** — §26 PlasticConnectome(시간-가소성)과 §28 BistableSwitch(상태-전환)를 결합해 **반복 상태-flip이 그 자체로 더 쉬워지는가**(가소성이 flip 역치를 시간에 걸쳐 낮추는가 = **kindling의 시간 진화 / 상태-전환 hysteresis의 학습된 변화**) — §29 양극성 kindling(반복될수록 쉬워짐)·§41 OCD STABILISATION(자기-지속 루프)의 자연스러운 교차. 새 결합 모듈은 §26·§28 두 층을 import(재유도 금지), 새 상수 0, 부호는 (이중) 스윕 생존. **착수 전 도달성 [V]/[L] 선판단** — 두 층 결합이 깨끗한 구조 부호를 내는지 먼저 프로브(§47/§48이 했듯 reachability probe). **결합 패턴(§47/§48 선례, 아래 규율 리마인더 참조).**

**B — E1×E2 결합의 추가 응용(선택).** §48은 **흥분성** 초점 구동의 방송 레버리지로 단일 집합 상태를 뒤집었다. 자연스러운 변주: **억제성** 구동(병변)이 집합 상태를 어느 부위서 가장 쉽게 **아래로** 뒤집는가(§45 LESION-E1의 상태-전환 형제), 또는 **여러 노드 동시** 구동의 leverage 합이 flip을 어떻게 바꾸는가(focal vs distributed 자극의 flip 효율 — §43 E1.4 focal/diffuse 무-법칙의 상태-전환 판). 같은 두 층 재사용, 구동 부호/분포만 다름. 도달성 선판단 후 착수.

**C — 교차축 결합 메타-종합 캡스톤(선택).** E0 삼부작이 §42 메타-종합 캡스톤으로 닫혔듯, **교차축 결합군**(E1×E0 §47 · E1×E2 §48 · (있다면) E0×E2)을 메타-종합 캡스톤으로 닫을 수 있다(새 측정 0·새 기계 0·소스 SHA 재검증 후 읽기, §42 패턴). 가장 깨끗·최저-위험. 결합 종합은 "공간이 시간을 만나면(각인 §47)·공간이 상태를 만나면(flip §48)·시간이 상태를 만나면(kindling)" 세 솔기를 **디커플링/뒤집기** 관점에서 나란히 프레이밍할 것(§47 C3/C4·§48 C3가 공통적으로 단일-축 결과를 디커플링함이 종합의 헤드라인 후보). 세 번째 결합(E0×E2)이 먼저 있어야 삼중 종합이 깨끗함.

**D — 문턱-이동 논리 로드맵 잔여 사례.** 우선순위표상 아직 출판 안 된 사례(있다면). 새 사례도 **깨끗한 [V]인지 부분 [L]인지** 도달성 선판단 — 게인/학습/퇴행/안정화/공간/결합 축 중 무엇이 지배적이면 부분 적합 예상.

**규율 리마인더 (모든 v1.56 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인 — 영 구동이 엔진 정착/앵커 bit-for-bit); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)`, `barrier(g)=g²/4`; 동역학 rate·공고화 율·공간 프로파일·자극 심도·장벽 깊이는 [O]·부호는 (이중) 스윕 견딤; **방송 레버리지 lev_j = colsum of W0는 frozen-kernel readout이지 새 상수 아님**); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **세 게이트(`gate.py`·`run_all_atlas.py` ALL PASS·해당 단일 모듈 PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **교차축 결합 패턴(§47/§48)**: 두 층을 잇는 결합은 (a) 두 재사용 층을 import(재유도 금지), (b) 결합 객체/적분기 하나만 새 작성(`LeverageSwitch`/`_integrate_coupled` 류), (c) 두 축 파라미터(강도·율·장벽 등)를 **둘 다 스윕**해 곱 그리드서 부호/순서 생존, (d) 양 파라미터=0(또는 영-구동) 가드로 엔진 bit-for-bit 복귀(두 층 가드 상속 — E2 결합이면 `static_limit_is_E_settle` 플래그·E.settle, E0 결합이면 M9 앵커·η=0), (e) 결합이 단일-축 결과를 **뒤집거나 디커플링**하면 그것이 발견 — 강요 말고 **정직히 보고**(§47 C3/C4·§48 C3 무-튜닝 규율). **마지막 챕터 nav**: 새 챕터가 마지막이면 nav = prev + paper contents + 빈 `<span>`; 직전 마지막 챕터의 빈 span을 새 챕터 next-link로 교체(생성기·렌더 양쪽). **아틀라스 전체 재현 ~15분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행).

---

## 6. 변경 파일 목록 (v1.55 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `spatial_switch_leverage.py`·`spatial_switch_leverage_results.json`·`expected_spatial_switch_leverage_sha256.json`.
**신규 (docs/tools)**: `docs/mind/48-spatial-switch-leverage/index.html`·`tools/_gen_ch48_spatial_switch_leverage.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(26th citizen SPC-E1E2를 SPC-E1E0 직후·E0-SYNTH 직전 배치 + 주석)·`tools/mind_registry.py`(LOCK `spatial_switch_leverage`+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 49 urls·vp-cards 126·llms-full 갱신·llms.txt 바이트-동일 4989B)·`manifest/mind.csv`(48행)·`docs/mind/_meta.json`(48챕터+totals.words 82750·tables 9)·`docs/mind/47-spatial-plasticity-imprint/index.html`+`tools/_gen_ch47_spatial_plasticity_imprint.py`(next-nav §48).
**거버넌스**: `CHANGELOG.md`(v1.55)·`HANDOVER_v1_55_to_v1_56.md`(이 문서)·`MISSION_atlas_redefinition.md`(E1×E2 둘째 교차축 결합 DONE)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터 v1.55).
