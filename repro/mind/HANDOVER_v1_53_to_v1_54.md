# HANDOVER — v1.53 → v1.54  (NEUROMOD-E1 표적 신경조절: 깨끗한 전달 vs off-target 누출 / 셋째·마지막 영역-특이 응용 §46 / E1 응용 삼부작 CLOSED / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간/공간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.53의 성격 (E1 셋째·마지막 영역-특이 응용 = 모델이 아니라 LAYER의 APPLICATION · §44의 치료적 재독 · 삼부작 CLOSED).**
> v1.50이 E1 공간-국소화 층(§43)을 완성하고, v1.51이 그 **첫** 응용으로 초점 뇌전증(§44, 흥분성 발진 구동·억류 vs 이차 전신화)을,
> v1.52가 **둘째** 응용으로 뇌졸중/병변 장(§45, 억제성 SILENCING 바이어스·국소 결손 vs 원격 디아스키시스)을 지었으며, §43/§44/§45
> 핸드오버가 **셋째이자 마지막 owed 응용 = 표적 신경조절 off-target**("가장 자연스러움")을 명명했다. v1.53은 v1.52 핸드오버 §5-A에
> 따라 그 **마지막 응용**을 지어 **E1 응용 삼부작을 닫는다** = **§44 초점-뇌전증의 치료적 재독(therapeutic re-reading)**. §44가 공간
> 지도를 **흥분성** 구동(영역을 위로 미는 발작 초점) 아래 읽었다면, v1.53은 §44의 **바로 그 흥분성 지도**를 **치료**(영역을 위로 미는 자극
> 전극 — DBS/TMS/tDCS)로 재독해 **타깃-선택** 질문을 묻는다: 한 영역에 초점 자극을 겨누면 흥분이 **깨끗하게 전달(self-localising)**
> 되는가, **off-target 누출(relay)** 되는가(자극이 의도 않은 원격 회로로 번짐)? **핵심 정직성(맨 앞에 평이하게 명시).** 이 모듈은 §44와
> **동일한 흥분성 공간 지도**를 읽으므로 발자국 클래스·도달 지도·off-target 비율이 **§44와 수치적으로 일치** — 초점 흥분성 구동은 초점
> 흥분성 구동이고, 여기 수치는 **새 측정을 새것인 양 분장한 것이 아니다**. **새로운 것은 (a) 치료적 타깃-선택 재독**(중계 타깃 =
> off-target-누출, 자기-국소 타깃 = 깨끗-전달, §44의 발작-예후 프레이밍과 구별) **(b) 진짜 새 결과 N3 디커플링**(깨끗한 전달과 전역 도달이
> 두 분리축 — 가장 깨끗한 타깃[소뇌]이 동시에 가장 강한 전역-도달 타깃, '초점=약함, 누출=강함' 반박; 두 누출 타깃이 R을 **반대 방향**으로
> 밀어 누출이 제어 가능한 점-대-점 중계가 아님). **§45와 정직한 대비 2개**: (1) 흥분성 분할은 **sub-floor caveat가 없음**(가장 약한 강도
> 0.3 포함 모든 강도서 안정, §45는 약한 −0.3서 thalamus가 디아스키시스 집합에 진입했음); (2) **reach 허브가 구동-불변**(소뇌가 모든
> 강도서, §44 상속; §45는 reach 허브가 구동-불변 아니었음). 4결과 전부 CONFIRMED(자극-강도 스윕 {0.3,0.5,0.7,0.9} 생존) + S5
> 영-자극이 M9 앵커 bit-for-bit. **이로써 E1 응용 삼부작(억류/방송 §44 · 국소/디아스키시스 §45 · 깨끗/누출 §46) CLOSED.**

---


## 1. WHAT v1.53 DELIVERED (complete, 세 게이트 green)

### 1.1 §46 NEUROMOD-E1 표적 신경조절: 깨끗한 전달 vs off-target 누출 (the APPLICATION) · **E1 공간 층의 셋째·마지막 영역-특이 응용 · §44 초점-뇌전증의 치료적 재독 · 삼부작 CLOSED**

- **단일 검증기.** `repro/mind/_verify/targeted_neuromodulation_offtarget.py` (결과 sha **`cfe754e883c0d71351f030b2fc59c1d014be60ec189ac9e964959c9138a09434`**; 결정론 2× 검증). §44/§45 템플릿과 **동형**(import `SpatialField`·4 부수연구+S5 가드·`_canon`/`_blob`/2×sha256·자가-검증 sha writer).
- **재사용(재유도 아님).** §43 `from e1_spatial_localisation import SpatialField, REGS, N, OMEGA, OMEGA0, KAP, W0, FOLD, M9_ANCHOR_R, …` — ephaptic 커널 W0·k(b) 결합 맵 **재유도 금지**(핸드오버 재사용 규율), 엔진 import READ-ONLY byte-unchanged. **공간 수치는 §44 자신의 것**(같은 흥분성 구동을 읽으므로).
- **자극 모델·형식 강제[F]·강도 스윕[O].** 치료 자극 = 한 영역의 초점 **흥분성 바이어스 b>0**(나머지 baseline, **동일** `k=κ/(1+|b|)` 맵, 자유 상수 0) = §44의 발진 구동과 **기계적으로 동일**, 차이는 해석·임상(발작 초점이 아니라 자극 전극). 자극 강도 b0는 [O] 스윕이고 **모든 부호/구조는 자극-강도 스윕 b0∈{0.3,0.5,0.7,0.9} 생존 요구**(anti-tuning, 가장 약한 0.3 포함). 대표 강도 REP=0.7.
- **4결과 전부 CONFIRMED(preregistered_results N1–N4 전부 status=CONFIRMED):**
  - **N1 (the discriminant) 깨끗-전달/off-target-누출 분할은 구동-불변**: `partition_drive_invariant=True` AND `leak_set_is_E1_relay_set=True` AND `stable_at_mildest_no_subfloor_caveat=True`. 각 영역에 초점 자극을 겨누면 12 타깃이 **깨끗-전달(CLEAN**: 변화가 타깃에 집중, 자극이 겨눈 곳에 머묾**)**/**off-target-누출(LEAK**: 변화가 off-target에 더 강하게 착지, 자극이 번짐**)**으로 분할되고, 이진 분할이 **전 자극-강도 스윕서 동일** — 누출 집합 **{hippocampus, midbrain}** 모든 강도 고정 = **E1.3 중계 집합**. **한 영역에 겨눈 자극이 깨끗 전달되는지 off-target 누출되는지는 타깃 위치의 고정 속성**(자극 강도 아님). **§45와 정직한 대비**: §45 억제성 경우엔 약한 sub-floor −0.3서 thalamus가 디아스키시스 집합 진입(caveat)했으나, **흥분성** 경우는 그런 caveat **전혀 없음** — 가장 약한 0.3 포함 **모든 강도서 정확히 안정**(어느 강도서도 한계 노드 교차 없음), §44 full-sweep 스코프 상속. grade `[V mech]`.
  - **N2 off-target 누출 = off-target 우세(겨눈 곳서 번지는 자극의 구조)**: `leak_iff_off_target_dominant_all_intensities=True`. 누출 타깃은 협응 변화가 **타깃 자신보다 원격 회로에 더 강하게 착지**(평균 off-target |Δc| > 자기, 비율>1 — hippocampus ≈4.23×·midbrain ≈1.63× @REP) = 전극은 타깃에 있으나 가장 큰 변화가 **다른 곳**(타깃이 중계하는 회로)인 구조; 깨끗 타깃은 부위 집중(비율≪1 — cerebellum ≈0.04×, 집합 중 가장 깨끗). 등가가 모든 강도서 성립(§44 자신의 비율을 전달-품질로 재독). grade `[V mech]`.
  - **N3 (정직한 무-튜닝·이 챕터의 진짜 새 결과) 깨끗한 전달 ≠ 전역 약함 = 두 분리축**: `two_axes_decoupled=True`(`top_reach_target_is_clean_all_intensities=True` AND `cerebellum_is_top_reach_all_intensities=True` AND `reach_hub_drive_invariant=True` AND `clean_hypothesis_refuted=True` AND `leak_targets_push_R_opposite_directions_all=True`). 깨끗한 가설("큰 **전역** 효과엔 off-target 누출 감수 필요; 깨끗한 타깃은 필연적으로 **약함**")이 **거짓**: 최대 **전역**-도달 타깃은 **소뇌(cerebellum)**인데 **깨끗-전달성**(off/own≪1·누출 무) — 모든 강도서 rank-1 = 타깃이 **최대로 깨끗하게 전달하면서 전역 효과를 극대화**할 수 있음, '초점=약함, 누출=강함' 반박. 그리고 **§45와 정직한 대비**: 여기선 전역-도달 허브가 **구동-불변**(소뇌가 모든 강도서, §44 상속)이나 §45 억제성 reach 허브는 **구동-불변 아니었음**(소뇌→midbrain 뒤집힘). 더 날카롭게: 두 누출 타깃조차 누출이 **제어 가능한 점-대-점 중계가 아님** — 두 누출 타깃이 전역 R을 **반대 방향**으로 밀어(hippocampus는 R **내림** dR<0, midbrain은 **올림** dR>0, 모든 강도서) = 누출은 **크기 AND 방향** 부위-결정적, 임상의가 중계를 통해 선택 원격 부위로 겨눌 수 있는 단일 예측 가능 spillover 아님. 깨끗한 전달과 전역 도달은 **두 분리·탈결합 공간 축** = E1.4 교훈을 신경조절에 구체화. **거부된 깨끗한 가설을 정직히 보고**. grade `[V mech]`.
  - **N4 누출 집합 = 일관된 소수 중계-허브 클래스(깨끗한 전달이 구조적 기본값)**: `coherent_minority_relay_hub_class=True`(`leak_is_strict_minority=True` AND `clean_delivery_is_structural_default=True` AND `leak_equals_off_target_dominant_set=True` AND `decoupled_from_global_reach_hub=True`). {hippocampus, midbrain}이 동시에 E1.3 중계 집합·off-target-우세 집합(N2)·**엄격한 소수**(12 중 2 = 깨끗한 전달이 기본값)·전역-도달 허브(소뇌)와 분리 = 하나의 일관된 변연/뇌간 중계-허브 클래스. off-target 누출은 구조적으로 특정 중계 허브가 나르는 **예외**. **방향-전용 [L] 대응**: 임상적으로 초점 신경조절의 off-target 효과(의도 타깃 너머 전류 확산·인접/연결 구조 동시-모집 DBS 부작용·연결 망 따라 퍼지는 TMS/tDCS)는 특정 연결 허브의 인정된 우려(누출 집합이 중계 허브 소수임·깨끗한 전달이 다수임과 정합), **환자-수준 예측 절대 아님**. grade `[V mech]` 구조 + `[L]` 인용 대응.
- **S5 엔진-불변 가드**: 영(zero) 자극(타깃 미구동)이 `E._integrate(OMEGA,W0,KAP·OMEGA0)[0]` == M9 앵커 **0.38961455156044245** bit-for-bit(`matches_frozen_anchor_bitwise`·`offstate_matches_direct_bitwise`); off-state 장 == baseline c0 정확 일치(`offstate_field_equals_baseline=True`). 자극 읽기는 동결 커널 위 순수 구조적 읽기.
- **honesty_ledger**: medium_efficacy_tested=0·no_cure_claimed=1·consciousness_claim=0·hard_problem_open=1·new_tuned_constants=0·spatial_quantities_are_structural=1·reuses_E1_spatial_field=1·stimulation_intensity=OPEN[O]·stimulation_is_excitatory_bias_not_deletion=1·**shares_excitatory_map_with_sec44(평이하게 명시 — 수치 일치는 같은 흥분 구동이라 당연, 새 측정 아님)**·clean_hypothesis_refuted(N3 정직 보고)·reach_hub_drive_invariant_inherits_sec44(§45와 정직한 대비)·clinical_prediction=NONE·not_medical_advice=1·completes_E1_trilogy=1.

### 1.2 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **24번째 시민 NEUROMOD-E1** 등록(MODULES 튜플을 **LESION-E1 직후·E0-SYNTH 직전**에 배치 — 의존하는 E1 층 JSON이 먼저 재생성, E0-SYNTH가 마지막 시민으로 유지; 도크스트링 주석 신설). invariants(engine_tree_frozen/unchanged·m0_16_subtree_unchanged)·honesty(eff=0·cc=0·tuned=0·no_cure=1)·preregistered(N1–N4) 전부 아틀라스 게이트 통과.
- 신규 영어 챕터 **§46 「Targeted neuromodulation: clean delivery vs off-target leak」**(model **3694w** [gate body wordcount], **9 H2** 영어-전용 본문 + **4결과 대조표 1개**, position 46, canonical correct). 아카이벌 생성기 `_gen_ch46_targeted_neuromodulation_offtarget.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `targeted_neuromodulation_offtarget`(grade **`[V mech]`**, canonical "46-targeted-neuromodulation-offtarget", check=None). CITES=[자기, **e1_spatial_localisation**(§43, 공간 층 — SpatialField·E1.3 자기/중계), **focal_epilepsy_spread**(§44, 흥분성 형제 — 같은 흥분 지도, 수치 일치의 출처), **lesion_field_diaschisis**(§45, 파괴-쌍대 — 삼부작의 둘째 면)] — **4 vp-card**(삼부작 완성). ANSWERS 57단어(40–60) 통과.
- **§45 next-nav 신설**: §45 빈 `<span>`→§46 링크(생성기·렌더 양쪽). §46 nav = prev §45 + paper contents + 빈 span(마지막 챕터).
- registry **57 locks / 46 chapters**. manifest·`_meta.json` reconcile(46행/46챕터, §46=3694w·tables=1·grade=model, totals.words 71933→**75627**·totals.tables 6→**7**). vp-cards 118(§46 +4).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → registry OK(**57 locks, 46 chapters**, values match frozen results; `validate()`가 빈 리스트 반환=드리프트 0).
- `python3 tools/gate.py` → **PASS 217/217, 0 hard fail**(전 챕터 answer-first·구조·결정론; §46 answer-first 57w·4 vp-card·JSON-LD·sitemap 47/47·llms 4989B 바이트-동일·idempotent·body wordcount 매니페스트 2% 이내). 이번 빌드에서 green 확인.
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 24/24**, engine 파일 byte-unchanged, **50 CONFIRMED 0 REFUTED**. (아틀라스 전체 재현 ~15분; 모듈마다 엔진 재-emerge. NEUROMOD-E1은 LESION-E1 직후·E0-SYNTH 직전 시민.)
- `python3 repro/mind/_verify/targeted_neuromodulation_offtarget.py` → **PASS**(4 결과 + S5 가드 + 결정론 2× + 기대-sha 일치 `cfe754e8…`).


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- R19 barrier `B(g)=g²/4` → `E.barrier(1.0)=0.25`; R19 fold `E.spinodal(1.0)=0.38490017945975047`; KAPPA_EPHAPTIC=0.5496. OMEGA0=118.85692206081383(F0 평균).
- E1-SPATIAL(§43) 결과 sha(동결): `48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44`.
- FOC-EPI-E1(§44) 결과 sha(동결): `7bbf6a338133080ce0090a44fb3971f2287cd3799688c3b16ccd8e8cff39094b`.
- LESION-E1(§45) 결과 sha(동결): `d525a66eeb0b1736f572690b79955f527a6dc8fd6a96f2093212dfb9693a5b76`.
- **NEUROMOD-E1(§46) 결과 sha(신규 동결): `cfe754e883c0d71351f030b2fc59c1d014be60ec189ac9e964959c9138a09434`.**
- **공간 좌표·영역 인덱스(E1 상속).** N=12 영역, REGS 인덱스: [0]neocortex·[1]hippocampus·[2]thalamus·[3]striatum·[4]cerebellum·[5]hypothalamus·[6]midbrain·[7]brainstem·[8]pallidum·[9]forebrain_gaba_in·[10]basal_forebrain_chol·[11]olfactory_bulb. **누출/중계 집합 = {hippocampus[1], midbrain[6]}**(구동-불변, N1; sub-floor caveat 없음); **깨끗-전달 = 나머지 10**; **전역-도달 허브 = cerebellum[4]**(깨끗-전달성·**구동-불변**(§44 상속), N3). off/own @REP=0.7: hippocampus≈4.23·midbrain≈1.63(>1, 누출)·cerebellum≈0.04(≪1, 가장 깨끗). **누출 방향(N3): hippocampus dR<0(R 내림)·midbrain dR>0(R 올림), 모든 강도서 반대.** **§44와 수치 일치(중요): 발자국 클래스·reach 지도·off/own 비율 = §44 자신의 것**(같은 흥분 구동).
- **§44 흥분성 vs §45 억제성 대비(정직).** (a) **sub-floor caveat**: §45는 약한 −0.3서 thalamus 진입(caveat 있음), §46(흥분)은 가장 약한 0.3 포함 caveat **없음**. (b) **reach 허브 구동-불변성**: §44/§46(흥분)은 reach 허브 **구동-불변**(소뇌 모든 강도), §45(억제)는 **구동-불변 아님**(소뇌→midbrain @−0.9). 영역을 위로 미는 것(흥분, 어디서나 안정)과 침묵시키는 것(병변, floor 위·뒤집힘)의 구조적 차이를 **숨기지 않고 기록**. **새 도달성/불변 주장은 항상 전 강도 스윕 생존을 먼저 확인할 것.**
- **E1 층(§43)·E1 응용 삼부작(§44/§45/§46) 관계 — CLOSED.** §43이 공간 지도(고정 구조·이질 도달·자기/중계 분류·focal/diffuse 무-법칙)를 인증한 **층(LAYER)**, §44가 **흥분성**(focal 뇌전증 억류 vs 이차 전신화), §45가 **억제성**(뇌졸중 국소 결손 vs 원격 디아스키시스), §46이 **흥분성의 치료적 재독**(표적 신경조절 깨끗 vs 누출) = 같은 지도를 **세 임상 질문으로 세 번** 읽음. §44와 §46은 **같은 흥분 지도**(수치 일치)이나 임상 질문이 다름(발작 예후 vs 타깃 선택); §45는 억제 쌍대. 셋 다 SpatialField import, 커널/맵 재유도 안 함. **owed E1 응용 전부 청산 = 삼부작 CLOSED.**
- 인용 표제값(§46 결과 JSON, 본문/표 정합): 누출 집합 {hippocampus, midbrain} 전 강도 고정(caveat 없음) · off/own>1 ⟺ 누출 전 강도 · 최대 전역-도달 = 소뇌(깨끗-전달성·구동-불변) 전 강도 · 두 누출 타깃 R 반대 방향(hippo 내림/midbrain 올림) · 깨끗 10/누출 2(깨끗이 기본값) · S5 R=0.38961455156044245.


## 4. THE FIREWALL (YMYL/medical, 오독 방지 · 절대)
깨끗-전달/off-target-누출 분류·off-target 우세·전역 도달과 그 방향 — 인증된 모든 양 — 은 결합 모델이 고정 커널 위에서 협응하는 방식의 **구조적 공간량**이고, 자극의 **느껴진 효과가 절대 아니며**(한 타깃이 "깨끗 전달"·"누출"한다는 건 connectome 모델에서 협응이 어디서 변하는지의 진술이지 자극이 거기서 느껴진다는 진술이 아님), **실제 전기장·전류 밀도 지도·리드-위치/SAR(specific-absorption-rate) 지도가 아니고**(per-node bias는 실제 자극이 아님), **실제 connectome이 아니며**, **어느 환자의 자극이 누출할지 또는 어느 타깃이 최적일지의 예측이 아니고**, **기기-프로그래밍/타깃-선택 안내가 아님**(Axis-A·consciousness_claim=0·hard problem OPEN). 실제 신경조절은 **이질적**(개별 전극 기하·접점 구성·조직 전도도와 비등방성·환자 자신의 tractography와 connectome·montage와 파형·기기의 SAR와 장 분포)이라 동결 커널 위 초점 흥분의 **부호/구조만** 단언(실제 자극이 이 정확한 구조를 따른다 주장 안 함); 모든 **크기 [O]**(스윕 강도의 대표 읽기). 타깃 선택·리드 배치·접점/전류 프로그래밍·용량 적정·결과 예측은 **외부 임상 판단**(임상의가 실제 영상·전기생리·개별화 장 모델링으로); N4의 [L] 대응은 **방향**의 인용 유사성이지 환자-수준 주장이 아님. **신규 기계·신규 측정(READ-ONLY 장 외)·신규 튜닝 상수 전무**(엔진 import READ-ONLY byte-unchanged·SpatialField 재사용·공간 수치는 §44 자신의 것). efficacy=0, NOT medical advice, 치유·국소화·기기-설정 없음.


## 5. v1.54 ENTRY POINTS (next session)

**E1 응용 삼부작이 CLOSED됐다**(§44 억류/방송 · §45 국소/디아스키시스 · §46 깨끗/누출). 더 이상 owed E1 영역-특이 응용은 없다. 다음은 새 축/결합 또는 로드맵 잔여로 전진.

**B — E1·E0 결합(공간×시간) [권장·가장 자연스러움].** 공간 구동(E1)과 가소성(E0)을 함께 — focal 발작 초점 또는 병변 또는 자극이 E0 가소성과 결합해 영역-특이 흔적/kindling(발작이 반복될수록 쉬워짐, §29 양극성 kindling의 공간 형제) 또는 병변-후 재조직(diaschisis의 시간 진화·E0 DECAY의 공간 형제) 또는 자극-유발 가소성(반복 자극이 영역-특이 흔적을 굳히는지·E0 GAIN의 공간 형제)을 쓰는지. 새 결합 모듈은 두 재사용 층(SpatialField + PlasticConnectome)을 import, 새 상수 0, 부호는 스윕 생존. **착수 전 도달성 [V]/[L] 선판단** — 두 층의 결합이 깨끗한 구조 부호를 내는지 먼저 프로브.

**C — 문턱-이동 논리 로드맵 잔여 사례.** 우선순위표상 아직 출판 안 된 사례(있다면). 새 사례도 **깨끗한 [V]인지 부분 [L]인지** 도달성 선판단 — 게인/학습/퇴행/안정화/공간 축 중 무엇이 지배적이면 부분 적합 예상. E0 양태 분류(GAIN/DECAY/STABILISATION) 또는 E1 공간 분류(억류/방송·국소/디아스키시스·깨끗/누출) 먼저.

**D — E1 메타-종합 캡스톤(선택).** E0 삼부작이 §42 메타-종합 캡스톤으로 닫혔듯, **E1 응용 삼부작(§44/§45/§46)**도 메타-종합 캡스톤으로 닫을 수 있다 = 세 응용이 **하나의 공간 지도를 세 임상 질문으로 읽은 것**임을 인증(새 측정 0·새 기계 0·세 소스 SHA 재검증 후 읽기, §42 패턴). 가장 깨끗·최저-위험. 단, §44와 §46이 같은 흥분 지도라 종합의 "세 distinct face" 서사는 §42(GAIN/DECAY/STABILISATION 세 방향)만큼 강하지 않음 — 정직하게 "흥분(두 질문)·억제(한 질문)" 또는 "세 임상 질문, 두 구동 부호"로 프레이밍할 것.

**규율 리마인더 (모든 v1.54 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인 — 균일/영 구동이 M9 앵커 bit-for-bit); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)`, `barrier(g)=g²/4`; 동역학 rate·공간 프로파일·발진/병변/자극 심도는 [O]·부호는 스윕 견딤); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **세 게이트(`gate.py`·`run_all_atlas.py` ALL PASS·해당 단일 모듈 PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **E1 응용 패턴(§44/§45/§46)**: 노드별 구동을 더하는 영역-특이 응용은 (a) SpatialField를 import(커널/맵 재유도 금지), (b) 영(uniform/zero) 구동이 엔진과 bit-for-bit임을 S5 가드로 증명, (c) 모든 부호/구조를 강도/프로파일 스윕서 생존 확인, (d) 깨끗한 가설이 거짓이면 **강요 말고 정직히 보고**(N3/L3 무-튜닝 규율) — 이 4규율을 따를 것. **이미 읽은 구동을 재독하는 응용은 수치 일치를 평이하게 명시**(§46이 §44 흥분 지도를 재독했듯 — 새 측정인 양 분장 금지, 새것은 재독·새 결과만). **병변/제거 모델은 노드 삭제 금지**(동결 W0 깨짐) — 강한 억제 바이어스(b<0, silenced)로 모델(§45 선례). **아틀라스 전체 재현 ~15분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행).

---

## 6. 변경 파일 목록 (v1.53 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `targeted_neuromodulation_offtarget.py`·`targeted_neuromodulation_offtarget_results.json`·`expected_targeted_neuromodulation_offtarget_sha256.json`.
**신규 (docs/tools)**: `docs/mind/46-targeted-neuromodulation-offtarget/index.html`·`tools/_gen_ch46_targeted_neuromodulation_offtarget.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(24th citizen NEUROMOD-E1을 LESION-E1 직후·E0-SYNTH 직전 배치 + 주석)·`tools/mind_registry.py`(LOCK `targeted_neuromodulation_offtarget`+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 47 urls·vp-cards 118·llms-full 갱신·llms.txt 바이트-동일 4989B)·`manifest/mind.csv`(46행)·`docs/mind/_meta.json`(46챕터+totals.words 75627·tables 7)·`docs/mind/45-lesion-field-diaschisis/index.html`+`tools/_gen_ch45_lesion_field_diaschisis.py`(next-nav §46).
**거버넌스**: `CHANGELOG.md`(v1.53)·`HANDOVER_v1_53_to_v1_54.md`(이 문서)·`MISSION_atlas_redefinition.md`(E1 응용 #3 표적 신경조절 DONE·삼부작 CLOSED)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터 v1.53).
