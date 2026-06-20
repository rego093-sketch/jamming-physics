# HANDOVER — v1.51 → v1.52  (E1-FOC 초점 뇌전증: 억류 vs 이차 전신화 / 첫 영역-특이 응용 §44 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간/공간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.51의 성격 (E1 첫 영역-특이 응용 = 모델이 아니라 LAYER의 APPLICATION).** v1.50이 E1 공간-국소화 층(§43)을
> 완성하며 **첫 공간 기초층**(스칼라 Kglob→노드별 Kvec·노드별 국소-결맞음 장 READ-ONLY)을 세웠고, 그 표제 E1.3 결과
> (각 노드의 focal 발자국이 **자기-국소** 또는 **중계**, 구동-불변, 중계 집합 {hippocampus, midbrain} 고정)와 함께
> **"이 층 위 질병 모듈은 영역-특이여야 함"**이라는 지침을 넘겼다. 그리고 그 위에 지을 **첫 영역-특이 응용**으로
> **focal 뇌전증 초점·뇌졸중/병변 장·표적 신경조절 off-target**을 명명(owed)했다. v1.51은 v1.50 핸드오버 §5-A
> (E1 위 영역-특이 응용, 가장 자연스러움)에 따라, 그 중 **가장 접지가 강한 focal 뇌전증**을 첫 응용으로 짓는다 =
> **§25(T2a) 과동기화 뇌전증의 공간적 정련**. **핵심 = 재사용·SIGN/구조-only·정직한 무-튜닝·방화벽 절대(YMYL).**
> §43 `SpatialField`를 import(커널/맵 재유도 금지)해 각 영역을 focal 발작 초점(강한 흥분성 발진 구동)으로 구동하고,
> 어느 초점이 **억류(국소 잔류)**하고 어느 것이 **방송(이차 전신화)**하는지, 그리고 방송이 §25 전역 과동기화와
> **같은 것인지**를 읽는다. **가장 중요한 정직성(F3)**: "방송 초점 = 전뇌를 §25 과동기화로 구동하는 초점"이라는 깨끗한
> 가설은 **거짓** — 최대 전역-reach 초점은 **소뇌**인데 **억류성**이고 두 방송 초점이 전역 R을 **반대 방향**으로 옮김 →
> off-target 확산과 전역 과동기화는 **두 분리축**, 이차-전신화 전파는 **부위-결정적**; 거부된 가설을 강요 않고 정직히
> 보고 = E1.4 무-튜닝 교훈을 뇌전증에 구체화. 4결과 전부 CONFIRMED(발진-강도 스윕 b0∈{0.3,0.5,0.7,0.9} 생존) +
> S5 영-발진 구동이 M9 앵커 bit-for-bit.

---


## 1. WHAT v1.51 DELIVERED (complete, 세 게이트 green)

### 1.1 §44 FOC-EPI-E1 초점 뇌전증: 억류 vs 이차 전신화 (the APPLICATION) · **E1 공간 층의 첫 영역-특이 응용 · §25 T2a 과동기화 뇌전증의 공간적 정련**

- **단일 검증기.** `repro/mind/_verify/focal_epilepsy_spread.py` (결과 sha **`7bbf6a338133080ce0090a44fb3971f2287cd3799688c3b16ccd8e8cff39094b`**; 결정론 2× 검증). E1 공간 템플릿과 **동형**(import `SpatialField`·4 부수연구+S5 가드·`_canon`/`_blob`/2×sha256·자가-검증 sha writer).
- **재사용(재유도 아님).** §43 `from e1_spatial_localisation import SpatialField, REGS, N, DEPTHS, OMEGA, OMEGA0, KAP, W0, FOLD, M9_ANCHOR_R, …` — ephaptic 커널 W0·k(b) 결합 맵 **재유도 금지**(핸드오버 재사용 규율), 엔진 import READ-ONLY byte-unchanged.
- **발진 모델·형식 강제[F]·강도 스윕[O].** 초점 발작 초점 = 한 영역의 강한 focal **흥분성 발진(ictal) 구동**(나머지 baseline, **동일** `k=κ/(1−|b|)` 맵, 자유 상수 0); 발진 강도 b0는 [O] 스윕이고 **모든 부호/구조는 발진-강도 스윕 b0∈{0.3,0.5,0.7,0.9} 생존 요구**(anti-tuning). 대표 강도 REP=0.7.
- **4결과 전부 CONFIRMED(preregistered_results F1–F4 전부 status=CONFIRMED):**
  - **F1 (the discriminant) 억류/방송 분할은 구동-불변**: `partition_drive_invariant=True` AND `broadcast_set_is_E1_relay_set=True`. 각 영역을 focal 발작 초점으로 구동하면 12 초점이 **억류(CONTAINED**: 자기-국소, 발진 변화가 초점에 집중, 발작 국소 잔류**)**/**방송(BROADCAST**: 중계, off-target에 더 강하게 착지, 발작 이차 전신화**)**으로 분할되고, 이진 분할이 **전 발진-강도 스윕서 동일** — 방송 집합 **{hippocampus, midbrain}** 모든 강도 고정. **초점 발작이 국소에 머무는지 이차 전신화하는지는 초점 위치의 고정 속성**(발진 강도 아님), E1.3 자기/중계 분류를 발진 구동에 적용. grade `[V mech]`.
  - **F2 방송 = off-target 우세(이차 전신화의 구조적 내용)**: `broadcast_iff_off_target_dominant_all_intensities=True`. 방송 초점은 발진 국소-결맞음 변화가 **초점 자신보다 원격 회로에 더 강하게 착지**(평균 off-target |Δc| > 자기 |Δc|, 비율>1 — hippocampus ≈4.2×·midbrain ≈1.6× @REP) = 발작이 초점 **너머** 회로를 모집하는 구조적 서명; 억류 초점은 초점 집중(비율<1). 등가가 모든 강도서 성립. grade `[V mech]`.
  - **F3 (정직한 무-튜닝) off-target 확산 ≠ 전역 과동기화 = 두 분리축**: `two_axes_decoupled=True`(`top_global_reach_focus_is_contained_all_intensities=True` AND `broadcast_foci_oppose_on_global_sync_all_intensities=True`). 깨끗한 가설("방송/이차-전신화 초점은 정확히 전뇌를 §25 과동기화로 구동하는 초점[최대 전역 reach]")이 **거짓**: 최대 **전역**-reach 초점은 **소뇌(cerebellum)**인데 **억류성**(모든 강도) → 최대 전역 모집자가 방송 초점이 아님; 두 방송 초점이 전역 동기화를 **반대 방향**으로 옮김(midbrain은 R↑[과동기화 쪽]·hippocampus는 R↓, 모든 강도) → "방송"은 일관된 전역-동기화 부호 **전무**. off-target 확산(F1/F2)과 전역 과동기화(§25 과동기화 축)는 **두 분리·탈결합 공간 속성**, 이차-전신화 전파는 **부위-결정적**, 단일 "확산=과동기화" 규칙 환원 불가 = E1.4 교훈을 뇌전증에 구체화. **거부된 깨끗한 가설을 정직히 보고**. grade `[V mech]`.
  - **F4 방송 집합 = 일관된 소수 중계-허브 클래스(억류가 구조적 기본값)**: `coherent_minority_relay_hub_class=True`(`broadcast_is_strict_minority=True` AND `containment_is_structural_default=True` AND `broadcast_equals_off_target_dominant_set=True` AND `disjoint_from_global_reach_hub=True`). {hippocampus, midbrain}이 동시에 E1.3 중계 집합·off-target-우세 집합(F2)·**엄격한 소수**(12 중 2 = 억류가 기본값)·전역-reach 허브(소뇌)와 분리 = 하나의 일관된 변연/뇌간 중계-허브 클래스. 이차 전신화는 구조적으로 특정 중계 허브가 나르는 **예외**. **방향-전용 [L] 대응**: 임상적으로 대부분 초점 발작은 국소 잔류·내측측두엽(hippocampal) 초점이 이차-전신화 뇌전증의 전형(hippocampus가 방송 집합과 정합), **환자-수준 예측 절대 아님**. grade `[V mech]` 구조 + `[L]` 인용 대응.
- **S5 엔진-불변 가드**: 영(zero) 발진 구동(초점 미구동)이 `E._integrate(OMEGA,W0,KAP·OMEGA0)[0]` == M9 앵커 **0.38961455156044245** bit-for-bit(`matches_frozen_anchor_bitwise`·`offstate_matches_direct_bitwise`); off-state 장 == baseline c0 정확 일치(`offstate_field_equals_baseline=True`)·`baseline_equals_anchor=True`. focal-spread 읽기는 동결 커널 위 순수 구조적 읽기.
- **honesty_ledger**: medium_efficacy_tested=0·no_cure_claimed=1·consciousness_claim=0·hard_problem_open=1·new_tuned_constants=0·spatial_quantities_are_structural=1·reuses_E1_spatial_field=1·ictal_intensity=OPEN[O]·clean_hypothesis_refuted(F3 정직 보고)·clinical_prediction=NONE·not_medical_advice=1.

### 1.2 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **22번째 시민 FOC-EPI-E1** 등록(MODULES 튜플을 **E1-SPATIAL 직후·E0-SYNTH 직전**에 배치 — 의존하는 E1 층 JSON이 먼저 재생성, E0-SYNTH가 마지막 시민으로 유지; 도크스트링 주석 신설). invariants(engine_tree_frozen/unchanged·m0_16_subtree_unchanged)·honesty(eff=0·cc=0·tuned=0·no_cure=1)·preregistered(F1–F4) 전부 아틀라스 게이트 통과.
- 신규 영어 챕터 **§44 「Focal epilepsy: containment vs secondary generalisation」**(model **2943w** [gate body wordcount], **9 H2** 영어-전용 본문 + **4결과 대조표 1개**, position 44, canonical correct). 아카이벌 생성기 `_gen_ch44_focal_epilepsy_spread.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `focal_epilepsy_spread`(grade **`[V mech]`**, canonical "44-focal-epilepsy-spread", check=None). CITES=[자기, **e1_spatial_localisation**(§43, 공간 층 — SpatialField·E1.3 자기/중계·E1.2 이질 reach 공급), **epilepsy_oversync**(§25, 과동기화 발작 = 공간적으로 정련하는 §25 솔기)] — **3 vp-card**. ANSWERS 59단어(38–62) 통과.
- **§43 next-nav 신설**: §43 빈 `<span>`→§44 링크(생성기·렌더 양쪽). §44 nav = prev §43 + paper contents + 빈 span(마지막 챕터).
- registry **55 locks / 44 chapters**. manifest·`_meta.json` reconcile(44행/44챕터, §44=2943w·tables=1·grade=model, totals.words 65720→**68663**·totals.tables 4→**5**). vp-cards 111(§44 +3).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → registry OK(**55 locks, 44 chapters**, values match frozen results; `validate()`가 빈 리스트 반환=드리프트 0).
- `python3 tools/gate.py` → **PASS 206/206, 0 hard fail**(전 챕터 answer-first·구조·결정론; §44 answer-first 59w·3 vp-card·JSON-LD·sitemap 45/45·llms 4989B 바이트-동일·idempotent·body wordcount 매니페스트 2% 이내). 이번 빌드에서 green 확인.
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 22/22**, engine 파일 byte-unchanged, **42 CONFIRMED 0 REFUTED**. (아틀라스 전체 재현 ~15분; 모듈마다 엔진 재-emerge. FOC-EPI-E1은 E1-SPATIAL 직후·E0-SYNTH 직전 시민.)
- `python3 repro/mind/_verify/focal_epilepsy_spread.py` → **PASS**(4 결과 + S5 가드 + 결정론 2× + 기대-sha 일치 `7bbf6a33…`).


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- R19 barrier `B(g)=g²/4` → `E.barrier(1.0)=0.25`; R19 fold `E.spinodal(1.0)=0.38490017945975047`; KAPPA_EPHAPTIC=0.5496. OMEGA0=118.85692206081383(F0 평균).
- E1-SPATIAL(§43) 결과 sha(동결): `48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44`.
- **FOC-EPI-E1(§44) 결과 sha(신규 동결): `7bbf6a338133080ce0090a44fb3971f2287cd3799688c3b16ccd8e8cff39094b`.**
- **공간 좌표·영역 인덱스(E1 상속).** N=12 영역, REGS 인덱스: [0]neocortex·[1]hippocampus·[2]thalamus·[3]striatum·[4]cerebellum·[5]hypothalamus·[6]midbrain·[7]brainstem·[8]pallidum·[9]forebrain_gaba_in·[10]basal_forebrain_chol·[11]olfactory_bulb. **방송(broadcast)/중계 집합 = {hippocampus[1], midbrain[6]}**(구동-불변, F1); **억류(contained) = 나머지 10**; **최대 전역-reach 허브 = cerebellum[4]**(억류성, F3). off/own @REP: hippocampus≈4.23·midbrain≈1.64(>1, 방송); 전역 R 방향: midbrain dR≈+0.012(↑)·hippocampus dR≈−0.016(↓).
- **무-튜닝 규율의 작동(중요).** 설계 중 후보 정직성 주장 "억류성 brainstem이 두 방송 초점 모두보다 전역-reach 크다"가 **b0=0.3에서 실패**(brainstem 0.00814 < midbrain 0.01325) → **강요 않고 제외**. F3의 채택 부호(소뇌가 최대 전역-reach·억류성, 두 방송 초점이 전역 R 반대 방향)는 전 깊이 스윕서 생존 확인된 것만 단언. **새 도달성 주장은 항상 전 강도 스윕 생존을 먼저 확인할 것.**
- **E1 층(§43)·E1 응용(§44) 관계.** §43이 공간 지도(고정 구조·이질 도달·자기/중계 분류·focal/diffuse 무-법칙)를 인증한 **층(LAYER)**, §44가 그 지도를 focal 뇌전증(억류 vs 이차 전신화)에 읽는 **첫 영역-특이 응용**이자 §25 과동기화 발작의 **공간적 정련**(F3: 방송 off-target 확산 ≠ 전역 과동기화, 두 분리축). SpatialField는 import, 커널/맵 재유도 안 함. 나머지 owed 응용(뇌졸중/병변 장·표적 신경조절 off-target)은 아직 owed.
- 인용 표제값(§44 결과 JSON, 본문/표 정합): 방송 집합 {hippocampus, midbrain} 전 강도 고정 · off/own>1 ⟺ 방송 전 강도 · 최대 전역-reach = 소뇌(억류성) 전 강도 · midbrain↑/hippocampus↓ 전역 R 전 강도 · 억류 10/방송 2(억류가 기본값) · S5 R=0.38961455156044245.


## 4. THE FIREWALL (YMYL/medical, 오독 방지 · 절대)
억류/방송 분류·off-target 우세·전역 reach 부호 — 인증된 모든 양 — 은 결합 모델이 고정 커널 위에서 협응하는 방식의 **구조적 공간량**이고, 발작의 **느껴진 위치(locus)가 절대 아니며**(한 초점이 "방송"한다는 건 connectome 모델에서 협응이 어디서 변하는지의 진술이지 발작이 거기서 느껴진다는 진술이 아님), **실제 전극·EEG/SEEG 국소화·전류 밀도·발작-전파 지도가 아니고**(per-node bias는 실제 발진 구동이 아님), **어느 환자의 발작이 이차 전신화할지의 예측이 아니며**, **수술/절제(resection) 안내가 아님**(Axis-A·consciousness_claim=0·hard problem OPEN). 실제 발작 전파는 **이질적**(백질 tractography·개별 뇌전증유발 네트워크·발작 모집 동역학·환자 자신의 connectome과 병리)이라 동결 커널 위 focal 발진 구동의 **부호/구조만** 단언(실제 초점 발작이 이 정확한 구조를 따른다 주장 안 함); 모든 **크기 [O]**(스윕 강도의 대표 읽기). 뇌전증 진단·발작 국소화·초점 절제 결정은 **외부 임상 판단**(임상의가 실제 데이터로); F4의 [L] 대응은 **방향**의 인용 유사성이지 환자-수준 주장이 아님. **신규 기계·신규 측정(READ-ONLY 장 외)·신규 튜닝 상수 전무**(엔진 import READ-ONLY byte-unchanged·SpatialField 재사용). efficacy=0, NOT medical advice, 치유·국소화·예후 없음.


## 5. v1.52 ENTRY POINTS (next session)

**A — 추가 E1 영역-특이 응용(가장 자연스러움).** §43이 명명한 나머지 두 owed 응용을 짓는다: **뇌졸중/병변 장**(영역 결손이 E1.2 도달 지도로 전파 = 어느 병변이 전역 협응을 무너뜨리고 어느 것이 국소에 머무는지)·**표적 신경조절 off-target**(E1.3 중계 부위가 자극을 표적서 멀리 나름 = 어느 표적이 깨끗하고 어느 것이 누출되는지). **착수 전 도달성 [V]/[L] 선판단** + §44 패턴 재사용 — SpatialField import, 새 커널·맵 재유도 금지, SIGN-only·강도/프로파일 스윕 생존, **거부된 깨끗한 가설은 정직히 보고**(F3 무-튜닝 규율), firewall 부착. 병변 장은 노드 "제거"가 W0 동결을 깨므로 **강한 억제 바이어스(b<0, silenced)로 모델**(노드 삭제 아님)해 커널 재사용을 유지할 것.

**B — E1·E0 결합(공간×시간).** 공간 구동(E1)과 가소성(E0)을 함께 — focal 발작 초점이 E0 가소성과 결합해 영역-특이 흔적/kindling(발작이 반복될수록 쉬워짐, §29 양극성 kindling의 공간 형제)을 쓰는지. 새 결합 모듈은 두 재사용 층(SpatialField + PlasticConnectome)을 import, 새 상수 0, 부호는 스윕 생존.

**C — 문턱-이동 논리 로드맵 잔여 사례.** 우선순위표상 아직 출판 안 된 사례(있다면). 새 사례도 **깨끗한 [V]인지 부분 [L]인지** 도달성 선판단 — 게인/학습/퇴행/안정화/공간 축 중 무엇이 지배적이면 부분 적합 예상. E0 양태 분류(GAIN/DECAY/STABILISATION) 또는 E1 공간 분류(억류/방송) 먼저.

**규율 리마인더 (모든 v1.52 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인 — 균일/영 구동이 M9 앵커 bit-for-bit); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)`, `barrier(g)=g²/4`; 동역학 rate·공간 프로파일·발진 강도는 [O]·부호는 스윕 견딤); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **세 게이트(`gate.py`·`run_all_atlas.py` ALL PASS·해당 단일 모듈 PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **E1 응용 패턴(§44 신규)**: 노드별 구동을 더하는 영역-특이 응용은 §44처럼 (a) SpatialField를 import(커널/맵 재유도 금지), (b) 영(uniform/zero) 구동이 엔진과 bit-for-bit임을 S5 가드로 증명, (c) 모든 부호/구조를 강도/프로파일 스윕서 생존 확인, (d) 깨끗한 가설이 거짓이면 **강요 말고 정직히 보고**(F3 무-튜닝 규율) — 이 4규율을 따를 것. **아틀라스 전체 재현 ~15분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행).

---

## 6. 변경 파일 목록 (v1.51 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `focal_epilepsy_spread.py`·`focal_epilepsy_spread_results.json`·`expected_focal_epilepsy_spread_sha256.json`.
**신규 (docs/tools)**: `docs/mind/44-focal-epilepsy-spread/index.html`·`tools/_gen_ch44_focal_epilepsy_spread.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(22nd citizen FOC-EPI-E1을 E1-SPATIAL 직후·E0-SYNTH 직전 배치 + 주석)·`tools/mind_registry.py`(LOCK `focal_epilepsy_spread`+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 45 urls·vp-cards 111·llms-full 갱신·llms.txt 바이트-동일 4989B)·`manifest/mind.csv`(44행)·`docs/mind/_meta.json`(44챕터+totals.words 68663·tables 5)·`docs/mind/43-spatial-localisation/index.html`+`tools/_gen_ch43_spatial_localisation.py`(next-nav §44).
**거버넌스**: `CHANGELOG.md`(v1.51)·`HANDOVER_v1_51_to_v1_52.md`(이 문서)·`MISSION_atlas_redefinition.md`(E1 응용 #1 focal 뇌전증 DONE)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터 v1.51).
