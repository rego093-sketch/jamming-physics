# HANDOVER — v1.52 → v1.53  (E1-LES 뇌졸중/병변 장: 국소 결손 vs 원격 디아스키시스 / 둘째 영역-특이 응용 §45 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간/공간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.52의 성격 (E1 둘째 영역-특이 응용 = 모델이 아니라 LAYER의 APPLICATION · §44의 파괴-병변 쌍대).** v1.50이 E1 공간-국소화
> 층(§43)을 완성하고 v1.51이 그 **첫** 영역-특이 응용으로 초점 뇌전증(§44, 흥분성 발진 구동·억류 vs 이차 전신화)을 지었으며,
> §43/§44 핸드오버가 **둘째 owed 응용 = 뇌졸중/병변 장**(그리고 셋째 = 표적 신경조절 off-target)을 명명했다. v1.52는
> v1.51 핸드오버 §5-A(추가 E1 영역-특이 응용)에 따라 **둘째 응용 = 뇌졸중/병변 장**을 짓는다 = **§44 초점-뇌전증의 파괴-병변
> 쌍대(dual)**. §44가 공간 지도를 **흥분성** 구동(영역을 위로 미는 발작 초점) 아래 읽었다면, v1.52는 **같은 지도**를 **억제성
> (SILENCING) 바이어스 = 초점 병변**(영역을 아래로 미는 뇌졸중/절제) 아래 읽어 **쌍대** 임상 질문을 묻는다: 한 영역을 파괴하면
> 순수 **국소 결손**인가, 병변 부위 **자신보다** 원격·연결 영역을 더 교란하는가(**디아스키시스(diaschisis)**, von Monakow의
> 고전 개념 — 초점 손상 후 원격 기능부전, 예: 교차 소뇌 디아스키시스). **핵심 = 재사용·SILENCING 모델(삭제 아님)·SIGN/구조-only·
> 정직한 무-튜닝·방화벽 절대(YMYL).** §43 `SpatialField`를 import(커널/맵 재유도 금지)해 각 영역을 **억제성 바이어스 b<0**로 침묵
> 시키되 — **노드는 침묵하지 삭제하지 않는다**(노드 삭제는 동결 W0를 깨고 커널 재사용을 잃음 = 핸드오버의 명시적 병변-모델링 지침) —
> 어느 병변이 **국소 결손**에 머물고 어느 것이 **원격 디아스키시스**를 일으키는지, 그리고 디아스키시스가 **전역** 협응 교란과
> **같은 것인지**를 읽는다. **가장 중요한 정직성(L3 + §44 대비)**: "전역 협응을 가장 교란하는 병변 = 원격-디아스키시스 병변"이라는
> 깨끗한 가설은 **거짓** — 최대 전역-교란 병변은 **국소-결손성 소뇌**(off/own≪1·디아스키시스 무)이고, 게다가 **§44와 달리 reach
> 허브 자체가 구동-불변이 아님**(소뇌가 −0.5/−0.7서 top, 가장 중증 −0.9서 midbrain이 추월) → 전역-교란과 원격-디아스키시스는
> **두 분리축**, 원격-기능부전 전파는 **부위-결정적**; 거부된 가설을 강요 않고 정직히 보고 = E1.4 무-튜닝 교훈을 뇌졸중에 구체화.
> 4결과 전부 CONFIRMED(병변-심도 스윕 b0∈{−0.5,−0.7,−0.9} 생존) + S5 영-병변이 M9 앵커 bit-for-bit.

---


## 1. WHAT v1.52 DELIVERED (complete, 세 게이트 green)

### 1.1 §45 LESION-E1 뇌졸중/병변 장: 국소 결손 vs 원격 디아스키시스 (the APPLICATION) · **E1 공간 층의 둘째 영역-특이 응용 · §44 초점-뇌전증의 파괴-병변 쌍대**

- **단일 검증기.** `repro/mind/_verify/lesion_field_diaschisis.py` (결과 sha **`d525a66eeb0b1736f572690b79955f527a6dc8fd6a96f2093212dfb9693a5b76`**; 결정론 2× 검증). §44 FOC-EPI 템플릿과 **동형**(import `SpatialField`·4 부수연구+S5 가드·`_canon`/`_blob`/2×sha256·자가-검증 sha writer).
- **재사용(재유도 아님).** §43 `from e1_spatial_localisation import SpatialField, REGS, N, OMEGA, OMEGA0, KAP, W0, FOLD, M9_ANCHOR_R, …` — ephaptic 커널 W0·k(b) 결합 맵 **재유도 금지**(핸드오버 재사용 규율), 엔진 import READ-ONLY byte-unchanged.
- **병변 모델·형식 강제[F]·심도 스윕[O].** 초점 병변 = 한 영역의 강한 초점 **억제성(silencing) 바이어스 b<0**(나머지 baseline, **동일** `k=κ/(1+|b|)` 억제 맵, 자유 상수 0); **노드는 침묵하지 삭제하지 않음**(`node_not_deleted` — 삭제는 동결 W0를 깨므로 온전한 커널 위서 읽음). 병변 심도 b0는 [O] 스윕이고 **모든 부호/구조는 병변-심도 스윕 b0∈{−0.5,−0.7,−0.9}(중등도-중증, E1.2 floor 상속) 생존 요구**(anti-tuning). 대표 심도 REP=−0.7, 약한 sub-floor 프로브 −0.3.
- **4결과 전부 CONFIRMED(preregistered_results L1–L4 전부 status=CONFIRMED):**
  - **L1 (the discriminant) 국소-결손/원격-디아스키시스 분할은 구동-불변**: `partition_drive_invariant=True` AND `diaschisis_set_is_E1_relay_set=True`. 각 영역을 초점 병변으로 침묵시키면 12 병변이 **국소-결손(LOCAL-DEFICIT**: 협응 변화가 병변에 집중, 기능부전 국소 잔류**)**/**원격-디아스키시스(REMOTE-DIASCHISIS**: 변화가 off-target에 더 강하게 착지, 병변이 원격 회로를 자신보다 더 교란**)**으로 분할되고, 이진 분할이 **전 병변-심도 스윕서 동일** — 디아스키시스 집합 **{hippocampus, midbrain}** 모든 심도 고정 = **E1.3 중계 집합**을 침묵 아래 읽은 것. **병변이 국소에 머무는지 원격 디아스키시스를 일으키는지는 병변 위치의 고정 속성**(병변 심도 아님). **정직한 스코프(`mild_subfloor_diaschisis_set`)**: 약한 sub-floor −0.3서 **thalamus**도 디아스키시스 집합 진입({hippocampus, midbrain, thalamus}) — 평이하게 보고되며 **구동-불변 주장에 포함 안 됨**(불변은 중등도-중증 코어서만 단언). grade `[V mech]`.
  - **L2 원격 디아스키시스 = off-target 우세(원격 기능부전의 구조적 내용)**: `diaschisis_iff_off_target_dominant_all_severities=True`. 디아스키시스 병변은 협응 변화가 **병변 자신보다 원격 회로에 더 강하게 착지**(평균 off-target |Δc| > 자기 |Δc|, 비율>1 — midbrain ≈3.0×·hippocampus ≈1.2× @REP) = 손상이 의존 회로를 교란하는 구조적 서명; 국소-결손 병변은 부위 집중(비율≪1 — cerebellum ≈0.06×, 압도적 국소). 등가가 모든 심도서 성립. grade `[V mech]`.
  - **L3 (정직한 무-튜닝) 전역 교란 ≠ 원격 디아스키시스 = 두 분리축**: `two_axes_decoupled=True`(`top_global_disruptor_is_local_at_moderate_severities=True` AND `cerebellum_is_top3_global_disruptor_all_severities=True` AND `cerebellum_off_over_own_below_1_all_severities=True`). 깨끗한 가설("**전역** 협응을 가장 교란하는 병변은 정확히 원격-디아스키시스 병변[최대 전역 reach]")이 **거짓**: 최대 **전역**-교란 병변은 **소뇌(cerebellum)**인데 **국소-결손성**(off/own≪1, 디아스키시스 무) — 중등도 심도(−0.5/−0.7)서 rank-1 전역 교란자·모든 심도서 top-3 = **병변이 최대로 국소이면서 전역 교란을 극대화**할 수 있음. 그리고 **§44와 정직한 대비**(`reach_hub_drive_invariant=False`): §44에선 전역-reach 허브(소뇌)가 **구동-불변**이었으나 여기선 reach 허브가 **구동-불변이 아님** — 소뇌가 −0.5/−0.7서 top, 가장 중증 **−0.9서 midbrain이 추월**. 디아스키시스 분할(L1)은 심도서 견고하나 전역-교란 순위는 아님 → 둘이 다른 안정성을 가짐 자체가 분리축 증거. off-target 디아스키시스(L1/L2)와 전역-협응 교란은 **두 분리·탈결합 공간 속성**, 어느 부위가 최악의 **원격** 기능부전을 일으키는지는 **부위-결정적** = E1.4 교훈을 뇌졸중에 구체화. **거부된 깨끗한 가설을 정직히 보고**. grade `[V mech]`.
  - **L4 디아스키시스 집합 = 일관된 소수 중계-허브 클래스(국소 결손이 구조적 기본값)**: `coherent_minority_relay_hub_class=True`(`diaschisis_is_strict_minority=True` AND `local_deficit_is_structural_default=True` AND `diaschisis_equals_off_target_dominant_set=True` AND `decoupled_from_global_reach_hub=True`). {hippocampus, midbrain}이 동시에 E1.3 중계 집합·off-target-우세 집합(L2)·**엄격한 소수**(12 중 2 = 국소 결손이 기본값)·전역-교란 허브(소뇌)와 분리 = 하나의 일관된 변연/뇌간 중계-허브 클래스. 원격 디아스키시스는 구조적으로 특정 중계 허브가 나르는 **예외**. **방향-전용 [L] 대응**: 임상적으로 대부분 초점 병변은 초점 결손을 내고·디아스키시스(교차 소뇌 디아스키시스·시상/변연 원격 효과·von Monakow 개념)는 특정 연결 허브의 인정된 예외(디아스키시스 집합이 중계 허브 소수임과 정합), **환자-수준 예측 절대 아님**. grade `[V mech]` 구조 + `[L]` 인용 대응.
- **S5 엔진-불변 가드**: 영(zero) 병변(영역 미침묵)이 `E._integrate(OMEGA,W0,KAP·OMEGA0)[0]` == M9 앵커 **0.38961455156044245** bit-for-bit(`matches_frozen_anchor_bitwise`·`offstate_matches_direct_bitwise`); off-state 장 == baseline c0 정확 일치(`offstate_field_equals_baseline=True`). 병변 읽기는 동결 커널 위 순수 구조적 읽기.
- **honesty_ledger**: medium_efficacy_tested=0·no_cure_claimed=1·consciousness_claim=0·hard_problem_open=1·new_tuned_constants=0·spatial_quantities_are_structural=1·reuses_E1_spatial_field=1·lesion_severity=OPEN[O]·node_not_deleted=1·clean_hypothesis_refuted(L3 정직 보고)·reach_hub_not_drive_invariant(§44 정직한 대비)·clinical_prediction=NONE·not_medical_advice=1.

### 1.2 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **23번째 시민 LESION-E1** 등록(MODULES 튜플을 **FOC-EPI-E1 직후·E0-SYNTH 직전**에 배치 — 의존하는 E1 층 JSON이 먼저 재생성, E0-SYNTH가 마지막 시민으로 유지; 도크스트링 주석 신설). invariants(engine_tree_frozen/unchanged·m0_16_subtree_unchanged)·honesty(eff=0·cc=0·tuned=0·no_cure=1)·preregistered(L1–L4) 전부 아틀라스 게이트 통과.
- 신규 영어 챕터 **§45 「Stroke and the lesion field: local deficit vs remote diaschisis」**(model **3270w** [gate body wordcount], **9 H2** 영어-전용 본문 + **4결과 대조표 1개**, position 45, canonical correct). 아카이벌 생성기 `_gen_ch45_lesion_field_diaschisis.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `lesion_field_diaschisis`(grade **`[V mech]`**, canonical "45-lesion-field-diaschisis", check=None). CITES=[자기, **e1_spatial_localisation**(§43, 공간 층 — SpatialField·E1.3 자기/중계·E1.2 이질 reach 공급), **focal_epilepsy_spread**(§44, 흥분성 쌍 — 같은 지도의 흥분 쌍대)] — **3 vp-card**. ANSWERS 59단어(40–60) 통과.
- **§44 next-nav 신설**: §44 빈 `<span>`→§45 링크(생성기·렌더 양쪽). §45 nav = prev §44 + paper contents + 빈 span(마지막 챕터).
- registry **56 locks / 45 chapters**. manifest·`_meta.json` reconcile(45행/45챕터, §45=3270w·tables=1·grade=model, totals.words 68663→**71933**·totals.tables 5→**6**). vp-cards 114(§45 +3).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → registry OK(**56 locks, 45 chapters**, values match frozen results; `validate()`가 빈 리스트 반환=드리프트 0).
- `python3 tools/gate.py` → **PASS 211/211, 0 hard fail**(전 챕터 answer-first·구조·결정론; §45 answer-first 59w·3 vp-card·JSON-LD·sitemap 46/46·llms 4989B 바이트-동일·idempotent·body wordcount 매니페스트 2% 이내). 이번 빌드에서 green 확인.
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 23/23**, engine 파일 byte-unchanged, **46 CONFIRMED 0 REFUTED**. (아틀라스 전체 재현 ~15분; 모듈마다 엔진 재-emerge. LESION-E1은 FOC-EPI-E1 직후·E0-SYNTH 직전 시민.)
- `python3 repro/mind/_verify/lesion_field_diaschisis.py` → **PASS**(4 결과 + S5 가드 + 결정론 2× + 기대-sha 일치 `d525a66e…`).


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- R19 barrier `B(g)=g²/4` → `E.barrier(1.0)=0.25`; R19 fold `E.spinodal(1.0)=0.38490017945975047`; KAPPA_EPHAPTIC=0.5496. OMEGA0=118.85692206081383(F0 평균).
- E1-SPATIAL(§43) 결과 sha(동결): `48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44`.
- FOC-EPI-E1(§44) 결과 sha(동결): `7bbf6a338133080ce0090a44fb3971f2287cd3799688c3b16ccd8e8cff39094b`.
- **LESION-E1(§45) 결과 sha(신규 동결): `d525a66eeb0b1736f572690b79955f527a6dc8fd6a96f2093212dfb9693a5b76`.**
- **공간 좌표·영역 인덱스(E1 상속).** N=12 영역, REGS 인덱스: [0]neocortex·[1]hippocampus·[2]thalamus·[3]striatum·[4]cerebellum·[5]hypothalamus·[6]midbrain·[7]brainstem·[8]pallidum·[9]forebrain_gaba_in·[10]basal_forebrain_chol·[11]olfactory_bulb. **디아스키시스/중계 집합 = {hippocampus[1], midbrain[6]}**(구동-불변, L1); **국소-결손 = 나머지 10**; **전역-교란 허브 = cerebellum[4]**(국소-결손성·구동-불변 아님, L3). off/own @REP=−0.7: midbrain≈2.95·hippocampus≈1.18(>1, 디아스키시스)·cerebellum≈0.056(≪1, 압도적 국소). **reach 허브 per severity(구동-불변 아님!): −0.5→cerebellum·−0.7→cerebellum·−0.9→midbrain**. sub-floor −0.3서 디아스키시스 집합에 thalamus 추가(정직히 제외).
- **무-튜닝 규율의 작동(중요).** (a) 약한 sub-floor 심도 −0.3서 thalamus가 디아스키시스 집합에 진입 — 이를 구동-불변 주장에 **포함시키지 않고** 중등도-중증 코어(−0.5/−0.7/−0.9)서만 불변 단언(`mild_subfloor_diaschisis_set` 별도 보고). (b) §44에선 reach 허브가 구동-불변이었으나 여기선 **구동-불변이 아님**(소뇌→midbrain @−0.9) — §44와의 차이를 **숨기지 않고 정직한 대비로 기록**(`reach_hub_drive_invariant=False`). **새 도달성/불변 주장은 항상 전 심도 스윕 생존을 먼저 확인할 것**(생존하지 않는 것은 명명하되 주장에서 제외).
- **E1 층(§43)·E1 응용(§44/§45) 관계.** §43이 공간 지도(고정 구조·이질 도달·자기/중계 분류·focal/diffuse 무-법칙)를 인증한 **층(LAYER)**, §44가 **흥분성** 응용(focal 뇌전증 억류 vs 이차 전신화), §45가 **억제성** 응용(뇌졸중 국소 결손 vs 원격 디아스키시스) = 같은 지도의 **흥분/억제 쌍대**. 둘 다 SpatialField import, 커널/맵 재유도 안 함. **남은 owed 응용 = 표적 신경조절 off-target**(아직 owed).
- 인용 표제값(§45 결과 JSON, 본문/표 정합): 디아스키시스 집합 {hippocampus, midbrain} 전 심도 고정 · off/own>1 ⟺ 디아스키시스 전 심도 · 최대 전역-교란 = 소뇌(국소-결손성) 전 심도 · reach 허브 구동-불변 아님(소뇌→midbrain @−0.9) · 국소 10/디아스키시스 2(국소가 기본값) · S5 R=0.38961455156044245.


## 4. THE FIREWALL (YMYL/medical, 오독 방지 · 절대)
국소-결손/디아스키시스 분류·off-target 우세·전역 reach 부호 — 인증된 모든 양 — 은 결합 모델이 고정 커널 위에서 협응하는 방식의 **구조적 공간량**이고, 뇌졸중의 **느껴진 경험이 절대 아니며**(한 병변이 "디아스키시스"한다는 건 connectome 모델에서 협응이 어디서 변하는지의 진술이지 뇌졸중이 거기서 느껴진다는 진술이 아님), **실제 병변·경색 지도·관류(perfusion)/확산(diffusion) MRI·connectome-디아스키시스 측정이 아니고**(per-node bias는 실제 병변이 아님), **어느 환자의 뇌졸중이 원격 교란/회복할지의 예측이 아니며**, **재활/임상 안내가 아님**(Axis-A·consciousness_claim=0·hard problem OPEN). 실제 뇌졸중은 **이질적**(개별 혈관 영역·백질 tractography·반음영(penumbra) 동역학·부종(oedema)·환자 자신의 connectome과 측부 순환)이라 동결 커널 위 초점 침묵의 **부호/구조만** 단언(실제 병변이 이 정확한 구조를 따른다 주장 안 함); 모든 **크기 [O]**(스윕 심도의 대표 읽기). 뇌졸중 진단·병변 국소화·예후·재활 계획은 **외부 임상 판단**(임상의가 실제 영상·진찰로); L4의 [L] 대응은 **방향**의 인용 유사성이지 환자-수준 주장이 아님. **신규 기계·신규 측정(READ-ONLY 장 외)·신규 튜닝 상수 전무**(엔진 import READ-ONLY byte-unchanged·SpatialField 재사용). efficacy=0, NOT medical advice, 치유·국소화·예후 없음.


## 5. v1.53 ENTRY POINTS (next session)

**A — 남은 owed E1 영역-특이 응용 = 표적 신경조절 off-target(가장 자연스러움).** §43이 명명한 세 owed 응용 중 둘(초점 뇌전증 §44·뇌졸중/병변 장 §45)이 완성됐고, **마지막 = 표적 신경조절 off-target**이 남았다: E1.3 중계 부위가 자극을 표적서 멀리 나름 = **어느 표적이 깨끗하고(self-localising) 어느 것이 누출(relay)되는지** — DBS/TMS/tDCS 같은 표적 자극의 off-target 누출의 공간 구조. **착수 전 도달성 [V]/[L] 선판단** + §44/§45 패턴 재사용 — SpatialField import, 새 커널·맵 재유도 금지, SIGN-only·강도/프로파일 스윕 생존, **거부된 깨끗한 가설은 정직히 보고**, firewall 부착. 자극은 흥분성 바이어스(b>0)로 모델(§44 패턴), off-target 누출은 E1.3 중계 분류의 직접 응용(중계 부위 자극 = 누출, 자기-국소 부위 자극 = 깨끗). 이 셋이 완성되면 **E1 영역-특이 응용 삼부작(억류/방송 · 국소/디아스키시스 · 깨끗/누출)** 닫힘.

**B — E1·E0 결합(공간×시간).** 공간 구동(E1)과 가소성(E0)을 함께 — focal 발작 초점 또는 병변이 E0 가소성과 결합해 영역-특이 흔적/kindling(발작이 반복될수록 쉬워짐, §29 양극성 kindling의 공간 형제) 또는 병변-후 재조직(diaschisis의 시간 진화·E0 DECAY의 공간 형제)을 쓰는지. 새 결합 모듈은 두 재사용 층(SpatialField + PlasticConnectome)을 import, 새 상수 0, 부호는 스윕 생존.

**C — 문턱-이동 논리 로드맵 잔여 사례.** 우선순위표상 아직 출판 안 된 사례(있다면). 새 사례도 **깨끗한 [V]인지 부분 [L]인지** 도달성 선판단 — 게인/학습/퇴행/안정화/공간 축 중 무엇이 지배적이면 부분 적합 예상. E0 양태 분류(GAIN/DECAY/STABILISATION) 또는 E1 공간 분류(억류/방송·국소/디아스키시스) 먼저.

**규율 리마인더 (모든 v1.53 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인 — 균일/영 구동이 M9 앵커 bit-for-bit); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)`, `barrier(g)=g²/4`; 동역학 rate·공간 프로파일·발진/병변 심도는 [O]·부호는 스윕 견딤); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **세 게이트(`gate.py`·`run_all_atlas.py` ALL PASS·해당 단일 모듈 PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **E1 응용 패턴(§44/§45)**: 노드별 구동을 더하는 영역-특이 응용은 (a) SpatialField를 import(커널/맵 재유도 금지), (b) 영(uniform/zero) 구동이 엔진과 bit-for-bit임을 S5 가드로 증명, (c) 모든 부호/구조를 강도/프로파일 스윕서 생존 확인, (d) 깨끗한 가설이 거짓이면 **강요 말고 정직히 보고**(L3 무-튜닝 규율) — 이 4규율을 따를 것. **병변/제거 모델은 노드 삭제 금지**(동결 W0 깨짐) — **강한 억제 바이어스(b<0, silenced)로 모델**해 커널 재사용 유지(§45 선례). **아틀라스 전체 재현 ~15분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행).

---

## 6. 변경 파일 목록 (v1.52 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `lesion_field_diaschisis.py`·`lesion_field_diaschisis_results.json`·`expected_lesion_field_diaschisis_sha256.json`.
**신규 (docs/tools)**: `docs/mind/45-lesion-field-diaschisis/index.html`·`tools/_gen_ch45_lesion_field_diaschisis.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(23rd citizen LESION-E1을 FOC-EPI-E1 직후·E0-SYNTH 직전 배치 + 주석)·`tools/mind_registry.py`(LOCK `lesion_field_diaschisis`+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 46 urls·vp-cards 114·llms-full 갱신·llms.txt 바이트-동일 4989B)·`manifest/mind.csv`(45행)·`docs/mind/_meta.json`(45챕터+totals.words 71933·tables 6)·`docs/mind/44-focal-epilepsy-spread/index.html`+`tools/_gen_ch44_focal_epilepsy_spread.py`(next-nav §45).
**거버넌스**: `CHANGELOG.md`(v1.52)·`HANDOVER_v1_52_to_v1_53.md`(이 문서)·`MISSION_atlas_redefinition.md`(E1 응용 #2 뇌졸중/병변 장 DONE)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터 v1.52).
