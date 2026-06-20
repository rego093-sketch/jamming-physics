# HANDOVER — v1.50 → v1.51  (E1-SPATIAL 공간-국소화 / 장-성형 층 §43 / mind 패키지)

> **다음 세션은 이 mind zip 하나만 올리고 `MASTER_MANUAL_START_HERE.md` → 이 문서 순으로 읽으면 전체 맥락이 복원된다.**
> 이 문서는 한국어(세션 언어). 백서 본문(`docs/` HTML)은 VP-SPEC C0에 따라 **영어 전용**이며 이 문서는 거버넌스/핸드오프 문서다.

> **사명(v1.33 재정의, 유지).** 패키지는 로드맵(`RESEARCH_ROADMAP_post_autism_adhd.md`)에 따라
> **트랜스진단 결함-축 아틀라스** — 질환을 증상 체크리스트가 아니라 **공유 메커니즘(T/O/W + 동기화/시간 축)** 으로
> 재절단 — 이다. 사명·축·상태표 SSOT는 `MISSION_atlas_redefinition.md`.

> **v1.50의 성격 (E1 공간-국소화 / 장-성형 = 첫 공간 기초층 · 모델이 아니라 LAYER).** v1.46–v1.49가 E0 동역학
> 삼부작(중독 GAIN·알츠하이머 DECAY·OCD STABILISATION)과 그 종합 캡스톤(§42)으로 **시간 축**을 완성했다. 그러나 25개
> 챕터 내내 프레임워크는 뇌를 **전역으로** 구동했다 — **단일 스칼라** 결합 Kglob을 전 네트워크에 동시에 올리거나 내렸다.
> 스칼라만으로는 **focal vs diffuse 구동·off-target 누출·영역-특이 질병**을 물을 수조차 없었다. v1.50은 v1.49 핸드오버
> §5-B(E1 공간-국소화 기계)에 따라 **공간 코어**를 추가한다 = §26 E0 가소성 층(시간 코어)의 **공간 형제**. **핵심 =
> 최소 일반화·정직한 무-튜닝·SIGN/구조-only.** 스칼라 Kglob을 **노드별 벡터 Kvec**로 일반화(동일 k(b) 맵, 새 상수 0;
> 균일 바이어스면 스칼라로 붕괴해 엔진과 bit-for-bit), 노드별 **국소-결맞음 장** c_i를 **READ-ONLY**로 읽는다. 4결과
> 전부 CONFIRMED(깊이 스윕 b0∈{0.3,0.5,0.7,0.9} 생존) + S4 균일 구동이 M9 앵커 bit-for-bit. **가장 중요한 정직성(E1.4)**:
> "focal이 늘 diffuse보다 표적 게인 집중"이라는 깨끗한 가설은 **거짓** — 부호가 부위에 따라 변함(9/12 집중) → 공간 결과는
> **부위-결정적**, 이 층 위 질병 모듈은 **영역-특이여야 함**; 거부된 가설을 강요 않고 정직히 보고 = 무-튜닝 규율의 작동.

---


## 1. WHAT v1.50 DELIVERED (complete, 세 게이트 green)

### 1.1 §43 E1 공간-국소화 / 장-성형 층 (the LAYER, E1-SPATIAL) · **첫 공간 기초층 · §26 E0의 공간 형제**

- **단일 검증기.** `repro/mind/_verify/e1_spatial_localisation.py` (결과 sha **`48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44`**; 결정론 2× 검증). E0 가소성 템플릿과 **동형**(재사용 `SpatialField` 클래스·4 부수연구·READ-ONLY 적분기·S4 가드·`_canon`/`_blob`/2×sha256·자가-검증 sha writer).
- **최소 일반화(새 방정식·새 상수 0).** 엔진의 노드 갱신 `dθ_i = ω_i + Kglob·Σ_j W₀_ij sin(θ_j−θ_i)`에서 **스칼라 Kglob → 노드별 벡터 Kvec_i = k(b_i)·OMEGA0**(동일 `k=κ/(1−|b|)[흥분]/κ/(1+|b|)[억제] cap 2κ` 맵, SZ/뇌전증/E0 재사용, 새 상수 0). **균일 바이어스면 벡터는 스칼라로 붕괴 → 동역학 bit-for-bit 엔진**.
- **노드별 국소-결맞음 장(READ-ONLY).** `c_i = <Σ_j W₀_ij cos(θ_j−θ_i)>`(정상상태 후반부 평균). 코사인을 적분과 나란히 누적하나 **sin 갱신에 들어가지 않아 θ 궤적·R 불변**(`_integrate_spatial`이 균일 Kvec서 `E._integrate(...)[0]`와 bit-for-bit 반환).
- **형식 강제[F]·프로파일 스윕[O].** 형식 = 동결 ~1/r³ 행-확률 커널 W₀ + 기존 맵(자유 상수 0); 프로파일(구동 노드·깊이 b0)은 [O] 스윕이고 **모든 부호/구조는 깊이 스윕 b0∈{0.3,0.5,0.7,0.9} 생존 요구**(anti-tuning).
- **4결과 전부 CONFIRMED(preregistered_results P1–P4 전부 status=CONFIRMED):**
  - **E1.1 (P1) 장은 고정 공간 구조를 가짐(정확)**: `locality_all_rows=True`(12 행 전부 커널 가중이 거리에 단조 감소) AND `rows_normalised=True`(행 합=1, `max_rowsum_deviation`=2.2e-16). 기계 정밀도 정확 기하 = 모든 focal/영역 주장의 기질. grade `[V exact]`.
  - **E1.2 (P2) 섭동 도달범위 이질적·구동-안정 허브**: `reach_heterogeneous=True`(max/min 깊이별 110.965/129.543×3, 모두 >5) AND `cerebellum_rank1_all_depths=True`(소뇌가 모든 스윕 깊이서 rank-1 도달 허브) AND `ranking_invariant_moderate_high=True`(b0∈{0.5,0.7,0.9} 쌍별 Spearman=1.0). 허브 구조 = connectome 불변량.
  - **E1.3 (P3, 표제) 자기-국소 vs 중계 분류 구동-불변**: `classification_drive_invariant=True`(이진 분류가 전 깊이 스윕서 동일), `relay_set_invariant`=**{hippocampus, midbrain}**(모든 진폭서 고정), 나머지 10 노드 자기-국소. 부위가 구동을 담는지 중계하는지는 **장에서의 위치의 고정 속성**.
  - **E1.4 (P4, 정직한 무-튜닝) 보편 focal>diffuse 법칙 부재**: `focal_gt_diffuse_is_universal=False`·`sign_set_heterogeneous=True`→`no_universal_law=True`(`n_sites_focal_concentrates`=9/12). 동일 총용량 focal vs diffuse 시 `(focal−diffuse 표적-게인)` 부호가 부위에 따라 변함 = 공간 결과 **부위-결정적**, 이 층 위 질병은 **영역-특이여야 함**. **거부된 깨끗한 가설을 정직히 보고**.
- **S4 엔진-불변 가드**: `_integrate_spatial(균일 KAP·OMEGA0)[0]` == `E._integrate(OMEGA,W0,KAP·OMEGA0)[0]` == M9 앵커 **0.38961455156044245** bit-for-bit(`matches_frozen_anchor_bitwise`·`layer_matches_direct_bitwise`); off-state 장 == baseline c0 정확 일치(`offstate_field_equals_baseline=True`). E1은 순수 add-on.
- **재사용 층.** `SpatialField` 클래스(POS·W₀·baseline R0/c0·`drive(bias_vec)`·`focal(node,b0)`·`diffuse(b0)`·`reach`·`footprint_class`)가 후속 영역-특이 모듈(focal 초점·병변 장·off-target 신경조절)이 import할 객체. 그 응용은 **owed**.
- **honesty_ledger**: medium_efficacy_tested=0·no_cure_claimed=1·consciousness_claim=0·hard_problem_open=1·new_tuned_constants=0·spatial_quantities_are_structural=1·spatial_profile=OPEN[O]·applications=OWED[O]·real_field_identity=OWED[O]·clean_hypothesis_refuted(E1.4 정직 보고).

### 1.2 아틀라스 등록 · 챕터 · 레지스트리
- `run_all_atlas.py` **21번째 시민 E1-SPATIAL** 등록(MODULES 튜플을 **E0-SYNTH 직전**에 배치 — E0-SYNTH가 마지막 시민으로 유지; E1은 삼부작 일부가 아닌 **새 기초 축**, 도크스트링 주석 신설). invariants(`engine_tree_frozen`/`engine_tree_sha256_unchanged`==FROZEN·`engine_tree_unchanged`·`m0_16_subtree_unchanged`)·honesty(eff=0·cc=0·tuned=0·no_cure=1)·preregistered(P1–P4) 전부 아틀라스 게이트 통과.
- 신규 영어 챕터 **§43 「Spatial localisation」**(model **2745w** [gate body wordcount], **11 H2** 영어-전용 본문 + **4결과 대조표 1개**, position 43, canonical correct). 아카이벌 생성기 `_gen_ch43_spatial_localisation.py`(주입-전 스켈레톤 emit, build가 answer/cards 주입).
- 신규 LOCK `e1_spatial_localisation`(grade **`[V mech]`**, canonical "43-spatial-localisation", check=None). CITES=[자기, **coord_kappa**(§13, 커널이 지어지는 측정 ephaptic 결합 κ=0.5496), **plasticity_consolidation**(§26, E0 시간 형제)] — **3 vp-card**. ANSWERS 57단어(40–60) 통과.
- **§42 next-nav 신설**: §42 빈 `<span>`→§43 링크(생성기·렌더 양쪽). §43 nav = prev §42 + paper contents + 빈 span(마지막 챕터).
- registry **54 locks / 43 chapters**. manifest·`_meta.json` reconcile(43행/43챕터, §43=2745w·tables=1·grade=model, totals.words 62975→**65720**·totals.tables 3→**4**). vp-cards 108(§43 +3).


## 2. GATES (finalize 전 필수)
- `python3 tools/mind_registry.py` → registry OK(**54 locks, 43 chapters**, values match frozen results; `validate()`가 빈 리스트 반환=드리프트 0).
- `python3 tools/gate.py` → **PASS 201/201, 0 hard fail**(전 챕터 answer-first·구조·결정론; §43 answer-first 57w·3 vp-card·sitemap 44/44·llms 4989B 바이트-동일·idempotent·body wordcount 매니페스트 2% 이내). 이번 빌드에서 green 확인.
- `python3 repro/mind/_verify/run_all_atlas.py` → **ALL PASS 21/21**, engine 파일 byte-unchanged, 38 CONFIRMED 0 REFUTED. (아틀라스 전체 재현 ~6분; 모듈마다 엔진 재-emerge. E1-SPATIAL은 E0-SYNTH 직전 시민.)
- `python3 repro/mind/_verify/e1_spatial_localisation.py` → **PASS**(4 결과 + S4 가드 + 결정론 2× + 기대-sha 일치 `48c83d85…`).


## 3. KEY FACTS / SHAs (동결)
- 엔진 READ-ONLY byte-frozen: `vp_mind_engine.py` sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`; tree `0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70`. M9 anchor R=0.38961455156044245.
- R19 barrier `B(g)=g²/4` → `E.barrier(1.0)=0.25`; R19 fold `E.spinodal(1.0)=0.38490017945975047`; KAPPA_EPHAPTIC=0.5496. OMEGA0=118.85692206081383(F0 평균).
- E1-SPATIAL 결과 sha(신규 동결): **`48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44`**.
- **공간 좌표·커널.** N=12 영역, POS=`E._measured_geometry(REGS)`(측정 MNI), W₀=`E._ephaptic_kernel(POS)`(~1/r³ 행-확률). 중계(relay) 집합 = {hippocampus, midbrain}(구동-불변); rank-1 도달 허브 = cerebellum(모든 깊이). reach 이질 max/min = {0.3:110.965, 0.5/0.7/0.9:129.543}.
- **E0(시간)·E1(공간) 형제 관계.** E0(§26)가 연결성 W에 느린 Hebbian 갱신을 더한 **시간 코어**, E1(§43)이 스칼라 결합을 노드별 벡터로 일반화한 **공간 코어**. 둘 다 동결 커널 위 READ-ONLY add-on, 둘 다 off-state서 M9 앵커 bit-for-bit. E1.4는 **보편 focal/diffuse 법칙 부재**를 정직히 확립(거부된 가설) → 영역-특이 후속 모듈을 요구.
- 인용 표제값(E1 결과 JSON, 본문/표 정합): locality 12/12 rows · rowsum dev 2.2e-16 · reach max/min >110 · cerebellum rank-1 all depths · Spearman=1.0(b0≥0.5) · relay {hippocampus,midbrain} · focal>diffuse 9/12 concentrate · S4 R=0.38961455156044245.


## 4. THE FIREWALL (YMYL/medical, 오독 방지 · 절대)
인증된 모든 양 — 국소-결맞음 장·도달 지도·자기/중계 분류 — 은 결합 모델이 고정 커널 위에서 협응하는 방식의 **구조적 공간량**이고, 경험의 **느껴진 위치(locus)가 절대 아니며**(구동이 한 영역에 "국소화"한다는 건 connectome 모델에서 협응이 어디서 변하는지의 진술이지 경험이 거기서 느껴진다는 진술이 아님), **실제 전극·전류 밀도·용량이 아님**(Axis-A·consciousness_claim=0·hard problem OPEN). 실제 부피 전도/ephaptic 결합은 **이질적**·주파수-의존(조직 전도도 비등방성·뇌회 기하·수초화)이라 동결 커널 위 노드별 구동의 **부호/구조만** 단언(실제 피질 장이 이 정확한 1/r³ 법칙을 따른다 주장 안 함); 모든 **크기 [O]**(스윕 프로파일의 대표 읽기). **신규 기계·신규 측정(READ-ONLY 장 외)·신규 튜닝 상수 전무**(엔진 import READ-ONLY byte-unchanged). E1은 **층**이지 응용이 아님 — 영역-특이 장애(focal 뇌전증 초점·뇌졸중/병변 장·표적 신경조절 off-target)는 **owed**, SpatialField는 그들이 import할 재사용 객체. efficacy=0, NOT medical advice, 치유·역전·예방 없음.


## 5. v1.51 ENTRY POINTS (next session)

**A — E1 위에 영역-특이 응용(가장 자연스러움).** E1이 공간 지도(고정 구조·이질 도달·자기/중계 분류)와 "영역-특이여야 함"이라는 지침을 넘겼으므로, 그 위에 **첫 영역-특이 응용**을 짓는다: focal 뇌전증 초점(어느 초점이 국소에 머물고 어느 것이 방송하는지 = E1.3 중계 집합 활용)·뇌졸중/병변 장(영역 결손이 도달 지도로 전파)·표적 신경조절 off-target(중계 부위가 자극을 표적서 멀리 나름). **착수 전 도달성 [V]/[L] 선판단** + E0 응용 패턴(§37/§39/§41) 재사용 — SpatialField를 import, 새 커널·맵 재유도 금지, SIGN-only·깊이/프로파일 스윕 생존·firewall 부착.

**B — E1·E0 결합(공간×시간).** 공간 구동(E1)과 가소성(E0)을 함께 — focal 구동이 가소성과 결합해 영역-특이 흔적/봉쇄를 쓰는지. 새 결합 모듈은 두 재사용 층(SpatialField + PlasticConnectome)을 import, 새 상수 0, 부호는 스윕 생존.

**C — 문턱-이동 논리 로드맵 잔여 사례.** 우선순위표상 아직 출판 안 된 사례(있다면). 새 사례도 **깨끗한 [V]인지 부분 [L]인지** 도달성 선판단 — 게인/학습/퇴행/안정화 축이 지배적이면 부분 적합 예상(B-i 명명 + B-ii E0 동역학 쌍). E0 양태 분류(GAIN/DECAY/STABILISATION 또는 제4 양태) 먼저.

**규율 리마인더 (모든 v1.51 작업).** (i) 엔진 READ-ONLY/byte-identical(새 모듈 `_verify/` add-only, 파라미터=0 가드 자체확인 — 균일 구동/η=0이 M9 앵커 bit-for-bit); (ii) 새 튜닝 상수 0(γ는 측정, `|h_sp|=spinodal(g)=2(g/3)^1.5`, `barrier(g)=g²/4`; 동역학 rate·공간 프로파일은 [O]·부호는 스윕 견딤); (iii) HTML 본문 English-only(C0), 거버넌스는 한국어; (iv) **llms.txt 챕터 추가 금지**(<5KB 헤드룸 — Part-II 챕터는 손-큐레이트 슬러그 목록에 애초에 없음, sitemap만; `write_llms()` 목록 건드리지 말 것); (v) 신규 챕터마다 efficacy=0·NOT medical advice·Axis-A·[O]·hard problem OPEN 부착; (vi) 단일 zip(내부 폴더 `mind_pkg`), 출력은 압축 파일 1개; (vii) 변경 후 **세 게이트(`gate.py`·`run_all_atlas.py` ALL PASS·해당 단일 모듈 PASS)** green 확인 — FAIL 시 finalize 금지. **동결 lock 재작성 금지**(빚 청산은 신규 lock이 발표). **공간 모듈 패턴(§43 신규)**: 노드별 구동을 더하는 모듈은 §43처럼 (a) 스칼라→벡터 일반화가 균일 입력서 엔진과 bit-for-bit임을 S4 가드로 증명, (b) 장 읽기를 READ-ONLY 부수계산으로(θ 궤적 불변), (c) 모든 부호/구조를 깊이/프로파일 스윕서 생존 확인, (d) 깨끗한 가설이 거짓이면 **강요 말고 정직히 보고**(E1.4 무-튜닝 규율) — 이 4규율을 따를 것. **아틀라스 전체 재현 ~6분** — 백그라운드 `setsid stdbuf -oL -eL ... </dev/null &` 후 폴링(백그라운드 프로세스가 reaped될 수 있어 0-byte 로그/조기 종료 시 재실행).

---

## 6. 변경 파일 목록 (v1.50 add-only / 기존 갱신)

**신규 (repro/mind/_verify/)**: `e1_spatial_localisation.py`·`e1_spatial_localisation_results.json`·`expected_e1_spatial_localisation_sha256.json`.
**신규 (docs/tools)**: `docs/mind/43-spatial-localisation/index.html`·`tools/_gen_ch43_spatial_localisation.py`.
**갱신**: `repro/mind/_verify/run_all_atlas.py`(21st citizen E1-SPATIAL을 E0-SYNTH 직전 배치 + 주석)·`tools/mind_registry.py`(LOCK `e1_spatial_localisation`+CITES+ANSWERS)·`tools/build_search_layer.py` 산출물(sitemap 44 urls·vp-cards 108·llms-full 갱신·llms.txt 바이트-동일 4989B)·`manifest/mind.csv`(43행)·`docs/mind/_meta.json`(43챕터+totals.words 65720·tables 4)·`docs/mind/42-e0-triad-synthesis/index.html`+`tools/_gen_ch42_e0_triad_synthesis.py`(next-nav §43).
**거버넌스**: `CHANGELOG.md`(v1.50)·`HANDOVER_v1_50_to_v1_51.md`(이 문서)·`MISSION_atlas_redefinition.md`(E1 공간-국소화 기초층 DONE)·`MASTER_MANUAL_START_HERE.md`(롤링 포인터 v1.50).
