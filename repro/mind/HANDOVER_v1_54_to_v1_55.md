# HANDOVER — v1.54 → v1.55  (SPC-E1E0 공간-가소성 각인: 국소 전달 vs 중계 공고화 / 아틀라스 최초의 교차축 결합 E1×E0 §47 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간/공간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.54의 성격 (아틀라스 최초의 교차축 결합 = E1[공간]과 E0[시간]의 혼인 · 모델이 아니라 두 LAYER의 COUPLING).**
> v1.50–v1.53이 E1 공간-국소화 층(§43)과 그 응용 삼부작(§44 억류/방송 · §45 국소/디아스키시스 · §46 깨끗/누출)을 완성하며
> **공간 축**을 닫았고, v1.46–v1.49가 E0 가소성 층(§26)과 그 동역학 삼부작(§37 GAIN · §39 DECAY · §41 STABILISATION) +
> 종합 캡스톤(§42)을 완성하며 **시간 축**을 닫았다. 그러나 두 축은 줄곧 **분리**돼 있었다 — 모든 E1 모듈은 **같은** §43 공간 지도를
> **단일 축**(공간, 초점 구동의 **순간** 발자국)으로 읽었고, 모든 E0 모듈은 **단일 축**(시간)으로 공고화했다. v1.54는 v1.53 핸드오버 §5
> **경로 B(E1×E0 공간×시간 결합)**에 따라 그 둘을 **혼인**시키는 **아틀라스 최초의 교차축 결합**이다. 결합은 은유가 아니라 **자극이
> 실제로 무엇인가**에 의해 기계적으로 강제된다: 실제 초점 자극은 순차로 두 일을 한다 — 한 장소에 구동을 **전달**(공간 사건, E1 질문)
> 하고, 뇌가 가소적이므로 네트워크가 그 구동이 유발한 협응을 **공고화**(시간 사건, E0 질문)한다. 순수 공간 챕터는 전자만, 순수 시간
> 챕터는 후자만 보며, 어느 쪽도 초점 구동이 **착지**하는 장소가 그것이 **지속 흔적**을 남기는 장소와 같은지 물을 수 없다 = 이 챕터가
> 존재하는 질문, **두 층을 동시에** 요구. **핵심 정직성·새 발견(C3 디커플링).** 결합이 드러내는 것: **깨끗한 전달이 깨끗한 각인을
> 함의하지 않는다** — 흔적-중계 집합이 §46 순간-장-중계 집합을 **진부분집합으로 포함**(가소성이 각인을 비국소화), 여섯 부위가 장을
> 깨끗하게 전달하면서 흔적은 off-target 각인. 그리고 **결합이 다수를 뒤집음**: §46서 깨끗-전달이 기본값(10/12)이었으나 여기선
> 중계-각인이 기본값(8/12). 4결과 전부 CONFIRMED(강도×율 **이중 스윕** 생존) + S6 영-구동+η=0이 M9 앵커 bit-for-bit·η=0서 W
> 동일·focal 정확 복귀(E0.3 상속). **이로써 아틀라스 최초의 교차축 결합(E1×E0) 완성.**

---


## 1. WHAT v1.54 DELIVERED (complete, 세 게이트 green)

### 1.1 §47 SPC-E1E0 공간-가소성 각인: 국소 전달 vs 중계 공고화 (the COUPLING) · **아틀라스 최초의 교차축 결합 · §43 공간 층(어디) × §26 가소성 층(지속)**

- **단일 검증기.** `repro/mind/_verify/spatial_plasticity_imprint.py` (결과 sha **`cdb1623009fe2a02818c00be5fd2243034d43880501fde89b75270e0574ec036`**; 결정론 2× 검증). §44/§45/§46 템플릿과 **동형**(4 부수연구+S6 가드·`_canon`/`_blob`/2×sha256·자가-검증 sha writer)이나 **두 층을 import**하는 점이 신규.
- **재사용(양쪽·재유도 아님).** §43 `from e1_spatial_localisation import SpatialField, …` (공간 구동·ephaptic 커널 W0·k(b) 맵) **그리고** §26 `from e0_plasticity import PlasticConnectome, _rn` (위상-상관 Hebbian 업데이트). **둘 다 재유도 금지**(핸드오버 재사용 규율), 엔진 import READ-ONLY byte-unchanged. **유일한 새 객체는 둘을 잇는 결합 적분기 `_integrate_coupled`**.
- **결합 모델·형식 강제[F]·이중 스윕[O].** 초점 자극 = §46과 같은 노드별 **흥분성 바이어스**(동일 `k=κ/(1+|b|)` 맵, 자유 상수 0); 새로운 것은 구동을 순간에 읽지 않고 **가소성 층을 통해 적분** — `_integrate_coupled`가 노드별 공간 구동 벡터를 **진화하는** connectome W 위에서 고정 공고화 창(EPOCHS=8) 동안 스텝하며 §26 규칙이 구조에 써 넣는 쌍별 위상-일치를 누적 → **지속 흔적 ΔW**(순간 장 아님). 엔진 고정 비협응 IC 매 epoch 재시드(결정론). 상수 T=6.0·dt=0.001·EPOCHS=8·REP=0.7·ETA=0.05(새 튜닝 상수 0). 자극 강도 b0∈**{0.3,0.5,0.7,0.9}** **그리고** 공고화 율 η∈**{0.03,0.05,0.08}** 둘 다 [O] 스윕이고 **모든 부호/구조는 강도×율 전 곱 그리드(영역당 12 조건) 생존 요구**(anti-tuning).
- **4결과 전부 CONFIRMED(preregistered_results C1–C4 전부 status=CONFIRMED):**
  - **C1 (the discriminant) 국소-각인/중계-각인 분할은 두 스윕 모두서 구동-불변**: `partition_drive_invariant=True` AND `local_set_is_expected=True` AND `distinct_partitions_over_sweep==1`. 각 영역에 초점 자극을 구동하고 공고화하면 12 타깃이 **국소-각인(LOCAL**: 지속 흔적이 구동 노드 입사 에지에 집중**)**/**중계-각인(RELAYED**: 흔적이 off-target 에지에 더 강하게 착지**)**으로 분할되고, 분할이 **전 강도×율 그리드서 동일**(정확히 한 분할) — 국소 집합 **{brainstem, cerebellum, pallidum, striatum}** 고정, 중계 집합(여덟) 고정. **초점 구동이 국소 각인하는지 흔적을 중계하는지는 구동 부위의 고정 속성**(얼마나 세게도, 얼마나 빠르게도 아님). **§46의 깨끗-전달 집합(다수 10)과 다른 분할** — 국소-각인 집합은 엄격한 소수 넷 = 결합이 어느 부위가 머무는지를 바꿈. grade `[V mech]`.
  - **C2 중계 각인 = off-target 우세(겨눈 곳서 번지는 흔적의 구조)**: `equivalence_all_intensities_and_rates=True`. 중계 타깃은 평균 off-target 공고화 |ΔW|가 입사 |ΔW| 초과(비율>1 — neocortex ≈6.25×·forebrain_gaba_in ≈5.71×·hippocampus ≈1.36×·midbrain ≈1.44× @REP) = 구동은 타깃에 있으나 가장 큰 **지속** 변화가 다른 곳; 국소 타깃은 노드 자기 에지 집중(비율<1 — brainstem ≈0.63×). 등가가 전 그리드서 성립(§46 누출 품질을 공고화로 재독). grade `[V mech]`.
  - **C3 (진짜 새 결합 결과 + 정직한 음성) 전달과 각인은 디커플링 = 깨끗한 전달이 깨끗한 각인을 함의 않음**: `decoupled=True`(`trace_relay_strictly_contains_field_relay=True` AND `field_relay_subset_of_trace_relay=True` AND `n_witnesses_clean_field_relayed_trace==6` AND `no_universal_focal_gt_diffuse_trace_law=True`). **흔적**-중계 집합(여덟)이 §46 **순간-장**-중계 집합 **{hippocampus, midbrain}**을 **진부분집합으로 포함(STRICTLY CONTAINS)** = **가소성이 각인을 비국소화**. 두 장-중계 부위는 흔적도 중계(부분집합 진짜), 그리고 **여섯 추가 부위**(neocortex, thalamus, hypothalamus, basal_forebrain_chol, forebrain_gaba_in, olfactory_bulb)가 **순간 장을 깨끗하게 전달**(§46서 자기-국소)하면서 흔적 공고화 시 **off-target 각인** = 깨끗한 전달이 깨끗한 각인을 함의 **않음**(초점 구동이 **착지**하는 곳과 **지속 표지**를 남기는 곳은 두 다른 장소). 그리고 거부된 깨끗한 가설을 정직히 보고 — **보편 focal>diffuse 흔적 법칙 부재**(동일 총강도 focal vs diffuse 비교 시 12 중 단 **3**만 focal서 더 각인, 이질적·보편 아님) = 지속 흔적은 **날카로워진 장이 아니다**. **거부된 깨끗한 가설을 정직히 보고**. grade `[V mech]`.
  - **C4 중계 각인이 구조적 기본값(결합이 다수를 뒤집음)**: `coherent_majority_class=True`(`relayed_is_strict_majority=True` AND `sec46_field_clean_was_majority=True` AND `relayed_equals_off_target_dominant_set=True` AND `relayed_strictly_contains_field_relay=True`). 중계-각인 집합은 **엄격한 다수**(12 중 **8**) = RELAYED 각인이 구조적 기본값, **§46의 정직한 대비**(거기선 CLEAN 전달이 기본값, 순간서 10/12 자기-국소). **결합이 다수를 뒤집음** = 초점 구동의 **순간** 발자국은 기본 focal이나 **지속** 발자국은 기본 **비국소화**(공고화가 전달이 국소화한 것을 퍼뜨림). 중계-각인 집합은 동시에 off-target-우세 흔적 집합(C2)·장-중계 집합(C3)을 진부분집합으로 포함 = 하나의 일관된 다수 클래스. **방향-전용 [L] 대응**: 임상적으로 자극-유발 가소성(rTMS/tDCS 후효과·DBS가 연결 회로에 유발하는 가소성)은 자극 부위에 국한되지 않고 **망-분산**·연결성-의존(중계 각인이 구조적 다수임·각인 축이 순간-전달 축과 디커플링됨과 정합), **환자-수준 예측 절대 아님**. grade `[V mech]` 구조 + `[L]` 인용 대응.
- **S6 엔진-불변 가드**: 영(zero) 구동+공고화 OFF(η=0)이 M9 앵커 **0.38961455156044245** bit-for-bit(`zero_drive_matches_direct_bitwise`·`matches_frozen_anchor_bitwise`); η=0서 connectome W가 커널과 **동일**(`eta0_W_identical_to_kernel=True`); focal 여기가 공고화 제거 시 **정확히 복귀**(`focal_excursion_eta0_reverts_exactly=True`, E0.3 가드 상속). 결합은 동결 커널 위 순수 add-on.
- **honesty_ledger**: medium_efficacy_tested=0·no_cure_claimed=1·consciousness_claim=0·hard_problem_open=1·new_tuned_constants=0·imprint_locality_is_structural=1·reuses_E1_spatial_field=1·reuses_E0_plastic_connectome=1·**first_cross_axis_coupling=1**·**delivery_imprint_decoupled=1**·**clean_delivery_not_clean_imprint=1**·no_universal_focal_gt_diffuse_trace_law=1·relayed_imprint_is_default=1·plasticity_delocalises_imprint=1·stimulation_intensity=OPEN[O]·consolidation_rate=OPEN[O]·clinical_prediction=NONE·not_medical_advice=1.

### 1.2 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **25번째 시민 SPC-E1E0** 등록(MODULES 튜플을 **NEUROMOD-E1 직후·E0-SYNTH 직전**에 배치 — 결합하는 E1 SpatialField 층과 E0 PlasticConnectome가 먼저 재생성, E0-SYNTH가 마지막 시민으로 유지; 도크스트링 주석 신설). invariants·honesty(eff=0·cc=0·tuned=0·no_cure=1)·preregistered(C1–C4) 전부 아틀라스 게이트 통과.
- 신규 영어 챕터 **§47 「Spatial-plasticity imprint: local delivery vs relayed consolidation」**(model **3503w** [gate body wordcount], **9 H2** 영어-전용 본문 + **4결과 대조표 1개**, position 47, canonical correct, **마지막 챕터**). 아카이벌 생성기 `_gen_ch47_spatial_plasticity_imprint.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `spatial_plasticity_imprint`(grade **`[V mech]`**, canonical "47-spatial-plasticity-imprint", check=None). CITES=[자기, **e1_spatial_localisation**(§43, 공간 층 어디 — SpatialField), **plasticity_consolidation**(§26, E0 시간 층 지속 — PlasticConnectome), **targeted_neuromodulation_offtarget**(§46, 순간-전달 짝 — 흔적-중계가 진부분집합으로 포함하는 장-중계의 출처)] — **4 vp-card**(최초 교차축 결합). ANSWERS 57단어(40–60) 통과.
- **§46 next-nav 신설**: §46 빈 `<span>`→§47 링크(생성기·렌더 양쪽). §47 nav = prev §46 + paper contents + 빈 span(**마지막 챕터**).
- registry **58 locks / 47 chapters**. manifest·`_meta.json` reconcile(47행/47챕터, §47=3503w·tables=1·grade=model, totals.words 75627→**79130**·totals.tables 7→**8**). vp-cards 122(§47 +4).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → registry OK(**58 locks, 47 chapters**, values match frozen results; `validate()`가 빈 리스트 반환=드리프트 0).
- `python3 tools/gate.py` → **PASS, 0 hard fail**(전 챕터 answer-first·구조·결정론; §47 answer-first 57w·4 vp-card·JSON-LD·sitemap 48/48·llms 4989B 바이트-동일·idempotent·body wordcount 매니페스트 2% 이내[§47=3503w]). 이번 빌드에서 green 확인.
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 25/25**, engine 파일 byte-unchanged, **54 CONFIRMED 0 REFUTED**. (아틀라스 전체 재현 ~15분; 모듈마다 엔진 재-emerge. SPC-E1E0은 NEUROMOD-E1 직후·E0-SYNTH 직전 시민.)
- `python3 repro/mind/_verify/spatial_plasticity_imprint.py` → **PASS**(4 결과 C1–C4 + S6 가드 + 결정론 2× + 기대-sha 일치 `cdb16230…`).


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- R19 barrier `B(g)=g²/4` → `E.barrier(1.0)=0.25`; R19 fold `E.spinodal(1.0)=0.38490017945975047`; KAPPA_EPHAPTIC=0.5496. OMEGA0=118.85692206081383(F0 평균).
- E1-SPATIAL(§43) 결과 sha(동결): `48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44`.
- FOC-EPI-E1(§44) 결과 sha(동결): `7bbf6a338133080ce0090a44fb3971f2287cd3799688c3b16ccd8e8cff39094b`.
- LESION-E1(§45) 결과 sha(동결): `d525a66eeb0b1736f572690b79955f527a6dc8fd6a96f2093212dfb9693a5b76`.
- NEUROMOD-E1(§46) 결과 sha(동결): `cfe754e883c0d71351f030b2fc59c1d014be60ec189ac9e964959c9138a09434`.
- **SPC-E1E0(§47) 결과 sha(신규 동결): `cdb1623009fe2a02818c00be5fd2243034d43880501fde89b75270e0574ec036`.**
- **공간 좌표·영역 인덱스(E1 상속).** N=12 영역, REGS 인덱스: [0]neocortex·[1]hippocampus·[2]thalamus·[3]striatum·[4]cerebellum·[5]hypothalamus·[6]midbrain·[7]brainstem·[8]pallidum·[9]forebrain_gaba_in·[10]basal_forebrain_chol·[11]olfactory_bulb. **국소-각인 집합 = {brainstem[7], cerebellum[4], pallidum[8], striatum[3]}**(엄격한 소수 넷, 구동-불변, C1); **중계-각인 집합 = 나머지 여덟**(엄격한 다수, C4 기본값); **§46 장-중계 집합 {hippocampus[1], midbrain[6]} ⊊ 흔적-중계 집합(여덟)**(진부분집합, C3 — 가소성이 각인 비국소화); **여섯 디커플링 증인(깨끗 전달·중계 각인) = {neocortex[0], thalamus[2], hypothalamus[5], basal_forebrain_chol[10], forebrain_gaba_in[9], olfactory_bulb[11]}**(C3). off/incident @REP: neocortex≈6.25·forebrain_gaba_in≈5.71·midbrain≈1.44·hippocampus≈1.36(>1, 중계)·brainstem≈0.63(<1, 국소). **focal>diffuse 흔적: 3/12만(보편 아님, C3).**
- **§47 결합 vs §46 순간(중요).** §46(순간 장-전달)에선 CLEAN 전달이 기본값(10/12 자기-국소), 누출/장-중계 집합 {hippocampus, midbrain}(2). §47(지속 흔적-각인)에선 RELAYED 각인이 기본값(8/12), 그 중계-각인 집합이 §46 장-중계 집합을 **진부분집합으로 포함** — **결합이 다수를 뒤집음**(C4): 순간 발자국은 기본 focal이나 지속 표지는 기본 비국소화, 공고화가 전달이 국소화한 것을 퍼뜨림. **전달 축(E1)과 각인 축(E1×E0)은 디커플링**(C3): 깨끗한 전달이 깨끗한 각인을 함의 않음.
- **E1 층(§43)·E0 층(§26)·교차축 결합(§47) 관계 — 첫 결합.** §43이 공간 지도(어디 WHERE, 순간 발자국)를 인증한 **층**, §26이 가소성(지속 LASTING, 시간 흔적)을 인증한 **층**, §47이 **둘을 잇는 첫 교차축 결합**(focal 구동을 §26 Hebbian 업데이트를 통해 적분 = 지속 흔적이 어디 착지하는가). 두 층 모두 import, 커널/맵/규칙 재유도 안 함. 유일한 새 객체는 `_integrate_coupled`. **이전 모든 모듈은 단일 축**(E1=공간만 §44/§45/§46, E0=시간만 §37/§39/§41)이었고 §47이 **최초 교차**.
- 인용 표제값(§47 결과 JSON, 본문/표 정합): 국소 집합 {brainstem, cerebellum, pallidum, striatum} 전 그리드 고정 · off/incident>1 ⟺ 중계 전 그리드 · 흔적-중계(8) ⊋ 장-중계(2) {hippocampus, midbrain} · 디커플링 증인 6 · focal>diffuse 3/12(보편 아님) · 중계 8/국소 4(중계가 기본값, §46 깨끗 10과 뒤집힘) · S6 R=0.38961455156044245.


## 4. THE FIREWALL (YMYL/medical, 오독 방지 · 절대)
국소-각인/중계-각인 분류·off-target 우세 흔적·전달/각인 디커플링·focal/diffuse 무-법칙 — 인증된 모든 양 — 은 **결합** 모델이 고정 커널 위에서 **지속 구조**를 써 넣는 방식의 **구조적 공간량**이고, 자극의 **느껴진 효과도 학습의 느껴진 효과도 절대 아니며**(한 타깃이 "국소 각인"·"중계 각인"한다는 건 connectome 모델에서 지속 변화가 어디 착지하는지의 진술이지 자극이나 기억이 거기서 느껴진다는 진술이 아님), **실제 전기장·전류 밀도 지도·리드-위치/SAR(specific-absorption-rate) 지도가 아니고**(per-node bias는 실제 자극이 아님), **실제 connectome이나 시냅스-가중 행렬이 아니며**(ΔW는 실제 시냅스 변화·LTP/LTD 측정·후효과 진폭이 아님), **어느 환자의 자극이 어디 각인할지 또는 어느 타깃이 최적 공고화할지의 예측이 아니고**, **기기-프로그래밍/타깃-선택 안내가 아님**(Axis-A·consciousness_claim=0·hard problem OPEN). 실제 자극-유발 가소성은 **이질적**(개별 전극 기하·montage·조직 전도도·환자 자신의 tractography와 connectome·파형과 용량·피질 상태-의존·시냅스 변화의 분자 기계)이라 동결 커널 위 초점 구동 공고화의 **부호/구조만** 단언(실제 후효과가 이 정확한 구조를 따른다 주장 안 함); 모든 **크기 [O]**(스윕 강도·율의 대표 읽기). 타깃 선택·리드 배치·접점/전류 프로그래밍·가소성-유발 프로토콜의 용량과 타이밍·결과 예측은 **외부 임상 판단**(임상의가 실제 영상·전기생리·개별화 모델링으로); C4의 [L] 대응은 **방향**(자극의 지속 효과가 망-분산)의 인용 유사성이지 환자-수준 주장이 아님. **신규 기계(둘을 잇는 적분기 외)·신규 측정(READ-ONLY 층 외)·신규 튜닝 상수 전무**(SpatialField와 PlasticConnectome import READ-ONLY·엔진 byte-unchanged). efficacy=0, NOT medical advice, 치유·국소화·기기-설정 없음.


## 5. v1.55 ENTRY POINTS (next session)

**아틀라스 최초의 교차축 결합(E1×E0)이 완성됐다**(§47 공간-가소성 각인). 두 축(공간 E1·시간 E0)을 잇는 첫 솔기가 읽혔다. 다음은 추가 교차축 결합, 또는 결합 종합, 또는 로드맵 잔여로 전진.

**A — 추가 교차축 결합(공간×다른 축) [권장·가장 자연스러움].** §47이 E1×E0(공간×시간-가소성)을 열었으니 자연스러운 다음은 **E1×E2(공간×상태-전환)** — 초점 구동이 §28 R19 쌍안정 상태-전환과 결합해 영역-특이 flip 문턱/latency를 내는지(어느 부위의 focal 구동이 가장 쉽게 상태를 뒤집는지, §29 양극성 episode의 공간 형제), 또는 **E0×E2(가소성×상태-전환)** kindling의 시간 진화. 새 결합 모듈은 해당 두 재사용 층을 import, 새 상수 0, 부호는 (이중) 스윕 생존. **착수 전 도달성 [V]/[L] 선판단** — 두 층 결합이 깨끗한 구조 부호를 내는지 먼저 프로브(§47이 했듯 reachability probe). **결합 패턴(§47 선례)**: (a) 두 층 모두 import(재유도 금지), (b) 결합 적분기 하나만 새로 작성(`_integrate_coupled` 류), (c) 두 축 파라미터(강도·율 등)를 **둘 다 스윕**해 곱 그리드서 부호 생존, (d) 양 파라미터=0 가드로 엔진 bit-for-bit 복귀(S6 류, 두 층 가드 상속), (e) 결합이 단일-축 결과를 **뒤집거나 디커플링**하면 그것이 발견(§47 C3/C4 — 강요 말고 정직히 보고).

**B — E1×E0 결합의 추가 응용(선택).** §47은 **흥분성** 초점 구동을 가소성과 결합(자극-유발 각인). 자연스러운 변주: **억제성** 구동(병변)을 가소성과 결합 = **병변-후 재조직/diaschisis의 시간 진화**(§45 LESION-E1의 E0 형제 — 병변 흔적이 어디 공고화하는가, E0 DECAY 결과와 정합 예상), 또는 **반복** 구동의 누적(kindling — 발작이 반복될수록 쉬워짐, §29 양극성 kindling의 공간 형제). 같은 두 층 재사용, 구동 부호/반복만 다름. 도달성 선판단 후 착수.

**C — 문턱-이동 논리 로드맵 잔여 사례.** 우선순위표상 아직 출판 안 된 사례(있다면). 새 사례도 **깨끗한 [V]인지 부분 [L]인지** 도달성 선판단 — 게인/학습/퇴행/안정화/공간/결합 축 중 무엇이 지배적이면 부분 적합 예상.

**D — E1 응용 삼부작 또는 교차축 메타-종합 캡스톤(선택).** E0 삼부작이 §42 메타-종합 캡스톤으로 닫혔듯, **E1 응용 삼부작(§44/§45/§46)** 또는 **교차축 결합군**을 메타-종합 캡스톤으로 닫을 수 있다(새 측정 0·새 기계 0·소스 SHA 재검증 후 읽기, §42 패턴). 가장 깨끗·최저-위험. E1 삼부작 종합은 "흥분(두 질문 §44/§46)·억제(한 질문 §45)" 또는 "세 임상 질문, 두 구동 부호"로 정직하게 프레이밍할 것(§44/§46이 같은 흥분 지도라 "세 distinct face" 서사는 §42만큼 강하지 않음).

**규율 리마인더 (모든 v1.55 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인 — 균일/영 구동+공고화 OFF가 M9 앵커 bit-for-bit); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)`, `barrier(g)=g²/4`; 동역학 rate·공고화 율·공간 프로파일·발진/병변/자극 심도는 [O]·부호는 (이중) 스윕 견딤); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **세 게이트(`gate.py`·`run_all_atlas.py` ALL PASS·해당 단일 모듈 PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **교차축 결합 패턴(§47)**: 두 층을 잇는 결합은 (a) 두 재사용 층을 import(재유도 금지), (b) 결합 적분기 하나만 새 작성, (c) 두 축 파라미터를 **둘 다 스윕**해 곱 그리드서 부호 생존, (d) 양 파라미터=0 가드로 엔진 bit-for-bit 복귀(두 층 가드 상속), (e) 결합이 단일-축 결과를 **뒤집거나 디커플링**하면 그것이 발견 — 강요 말고 **정직히 보고**(§47 C3/C4 무-튜닝 규율). **마지막 챕터 nav**: 새 챕터가 마지막이면 nav = prev + paper contents + 빈 `<span>`; 직전 마지막 챕터의 빈 span을 새 챕터 next-link로 교체(생성기·렌더 양쪽). **아틀라스 전체 재현 ~15분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행).

---

## 6. 변경 파일 목록 (v1.54 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `spatial_plasticity_imprint.py`·`spatial_plasticity_imprint_results.json`·`expected_spatial_plasticity_imprint_sha256.json`.
**신규 (docs/tools)**: `docs/mind/47-spatial-plasticity-imprint/index.html`·`tools/_gen_ch47_spatial_plasticity_imprint.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(25th citizen SPC-E1E0를 NEUROMOD-E1 직후·E0-SYNTH 직전 배치 + 주석)·`tools/mind_registry.py`(LOCK `spatial_plasticity_imprint`+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 48 urls·vp-cards 122·llms-full 갱신·llms.txt 바이트-동일 4989B)·`manifest/mind.csv`(47행)·`docs/mind/_meta.json`(47챕터+totals.words 79130·tables 8)·`docs/mind/46-targeted-neuromodulation-offtarget/index.html`+`tools/_gen_ch46_targeted_neuromodulation_offtarget.py`(next-nav §47).
**거버넌스**: `CHANGELOG.md`(v1.54)·`HANDOVER_v1_54_to_v1_55.md`(이 문서)·`MISSION_atlas_redefinition.md`(E1×E0 첫 교차축 결합 DONE)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터 v1.54).
