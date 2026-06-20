# START HERE — Hemodynamic Homeostasis (homeostasis_hemodynamic_vp_site)  ·  v0.7.0 (comfort-logic intervention layer)

> 이 zip을 **새 창에 넣고 이 파일 → CHARTER.md → LITERATURE.md 순서로 읽으면** 상위 백서 없이 바로 연구를 이어갈 수 있다.
> 자족적: 기질(FHN/R19), VP-SPEC v1.8 전문, 노드 정체성 γ, 감각세포·루프·치료 모듈을 내부에 들고 있다.

## 0. 한 줄 정체
평균동맥압(MAP)은 어느 단일 장기도 소유하지 않는다 — 이 패키지는 CO×SVR×용적 루프를 형제 패키지 seam에서 폐합하고, 그 **감각세포 → 빠른(baroreflex)·느린(RAAS/압력-나트륨이뇨) 방어 → 실패(고혈압=setpoint 재설정, 심부전=basin 붕괴)**까지 결정론적으로 다룬다.

## v0.7.0에서 추가된 것 (comfort-logic 개입층 — 진통제 3-레버 기법 이식)
진통제 백서(`analgesic_threshold_logic_v2.0`, 개념 DOI `10.5281/zenodo.20733420`)의 3-레버 개입 기법을 이 패키지의 기존 범위(루프 조절장애 질병 = 본태성 고혈압 + 만성 심부전) 안에서 방어된 동맥압 setpoint에 이식했다. 근거는 이미 증명된 결과뿐이다: MAP 루프는 적분 제어기로서 작동점(operating-point) 밀어내기를 기준점으로 **되밀고**(RP4) 기준점 재설정은 지속된다(T1). 구조적으로 읽으면 그 되밀림(counter-regulation)이 **항고혈압 부작용 부류의 구조적 기원**이며, 기준점 재설정 방향은 되밀림을 유발하지 않는다. 새 층(`repro/_intervention/`)은 세 레버 — H1 기준점-재설정(counter-regulation-free, REN/SIX2 γ로 DNA 접지), H2 완충-복원(낮음), H3 효과기-부하경감(짝지음 전용, 단독은 되밀림) — 와 HP1–HP7 가설(가설 전용), 선언-가중 축 순위, 축별 정직성 게이트, 반증 등록부, fail-closed 금지주장 방화벽으로 구성된다. 배터리 21→26(IV1–IV5), 문서 13→21쪽(§13–§20, 한 쪽당 한 아이디어). 개념 DOI `10.5281/zenodo.20756801`을 하드코딩했다. **방화벽 경계:** 어떤 레버 방향이 루프의 되밀림을 유발하는지에 대한 *구조적 예측*만 진술하며, 분자·용법·효능·내약성·안전성은 일절 주장하지 않는다(`[O]`). "counter-regulation-free"는 구조적 속성이지 임상적 주장이 아니다. 의료 책임 없음.

## v0.2.0에서 추가된 것 (핵심)
이전 리비전은 연구 SKELETON이었다. 이번 리비전은 CHARTER가 요구한 **근본**을 발굴하고 스트레스 배터리를 실제로 통과시켰다(계산된 판별식 14/14, silent pass 없음).
1. **감각 변환층** `repro/_sensory/` — 압수용체 **PIEZO1/2**(빠른 루프), 치밀반(macula densa) **NKCC2** NaCl 화학수용체(느린 루프). 구심성 발화 = 공유 R19 스파이크열로 확인. (S1, S2)
2. **폐합 setpoint 루프** `repro/_engine/vp_hmd_loops.py` (RP1–RP5) — seam에서 MAP, baroreflex 완충 + PIEZO-KO labile, 신장 적분기(완전적응), 고혈압 setpoint 재설정(되밀림), 심부전 안장-마디 붕괴. 모두 실행·통과.
3. **문헌 상호작용 지도** (7노드/11엣지, `LITERATURE.md`) — 감각세포 → 구심 → 적분기/조절기 → 효과기 → MAP → 되먹임, 엣지마다 등급+근거.
4. **근본 vs 대증 치료** `repro/_therapy/fundamental_targets.py` (T1, T2) — 두 주요 질병의 더 근본적 치료책, 임상 근거와 양방향 일치.
5. **병리 법칙** `repro/_pathology/setpoint_failure.py` — 자리표시자 → 유도된 재설정 법칙(P*=P0+dPset, 되밀림)과 붕괴 법칙(spinodal(κ*)=|load| 안장-마디), 루프 스윕과 자기일치 확인.

## 1. 즉시 실행 (연구 재현)
```
python repro/run_all.py
```
→ 측정 γ에서 노드 **창발**(SIX2=1.5556·REN=1.3634 둘 다 측정 [V], 측정 대기 master 없음), **감각 변환층**, **RP1–RP5 폐합 루프**, **상호작용 지도**, **근본 vs 대증 치료**, **저혈압 노드 분해(RP6–RP9 + 심인성)**, **범용성: 루프 누적 setpoint 창발(C1)**, **스트레스 배터리 14/14**, **집필 잠금 여부**를 출력. HTML은 만들지 않는다.

## 2. 범위 — 질병이 아니라 **근본 메커니즘부터**
mind처럼 **시뮬레이션으로 창발하여 순환**시키되, 1차 객체는 장기가 아니라 **감각세포·루프·setpoint·basin**이다. 정체성·발생순서는 DNA 인용(SSOT), 동역학·감각·치료만 추가.

| master gene | node | measured γ | role | dyn class |
|---|---|---|---|---|
| SIX2 | kidney_volume_integrator | 1.5556 | pressure-natriuresis + RAAS volume control (the slow integrator) | setpoint-loop |
| REN | raas_endocrine | 1.3634 | renin-angiotensin-aldosterone slow pressure/volume control | slow-loop |
| (baroreflex_arc) | baroreflex | —(diffuse) | autonomic fast pressure buffer (cite cardioresp/neuro) | fast-buffer |
| (vascular_tone) | vascular_resistance | —(diffuse) | SVR / Windkessel tone (cite circulatory vessels) | effector |

**감각 변환층 (근본, NEW):**
| sensor | transducer | reads | loop | feeds |
|---|---|---|---|---|
| baroreceptor | PIEZO1/PIEZO2 | arterial-wall stretch ~ pressure | fast | baroreflex |
| macula_densa | NKCC2 (Na-K-2Cl) | luminal NaCl ~ GFR | slow | raas_endocrine(renin, inverse) + kidney integrator(TGF) |

**상속(IN) — 내부 vendoring + 형제 seam 인용:** cardioresp(CO + baroreflex edge; carotid body·cardiopulmonary receptors는 인용만, 재창발 금지) · circulatory(SVR/Windkessel) · DNA(SIX2 + 발생순서 [V]) · substrate(FHN/R19, vendored)
**경계(OUT):** defended MAP(systemic SSOT) · pressure coupling → homeostasis_thermometabolic

## 3. 판별 타깃 (전부 PASS — CHARTER에 전체 프로그램)
- **RP1** MAP = CVP + CO×SVR → 93.0 mmHg (err 0.0), 단일 장기 소유 아님 [V]/[L]/[O]
- **RP2** baroreflex 75% 완충; PIEZO 이중-KO → labile [V]/[L]
- **RP3** 압력-나트륨이뇨 완전적응(spread 0.0, "infinite gain") [V]/[L]/[O]
- **RP4** 고혈압 = setpoint 재설정(+20 mmHg); 작동점 약물은 되밀림 [V]/[L]/[O]
- **RP5** 심부전 = basin 붕괴(안장-마디 fold), 재설정과 구별 [V]/[L]/[O]
- **S1** 압수용체 PIEZO 단조 + KO 평탄 + 공유 R19 스파이크 [V]/[L]/[O]
- **S2** macula densa NKCC2: renin↓ / TGF↑ 단조, SGLT2i가 TGF 회복 [V]/[L]/[O]
- **T1** 고혈압: 작동점 약물 되밀림 vs 신장 기준 재설정 지속 [V]/[L]/[O]
- **T2** 심부전: inotrope가 여유 M 축소 vs 부하감소+악순환차단이 M 확대 [V]/[L]/[O]

## 4. 질병 — 이 시스템의 일부 (유도된 법칙)
질병 = 국소 병변이 아니라 **방어되던 setpoint의 실패**. 위치: `repro/_pathology/`. disease_wp(단일유전자 병변)와 *합성* — 유전자 병변 = 루프 파라미터 입력, 전신 궤적 = 여기서 계산.
- **essential hypertension** — 적분기 RESET: P*=P0+dPset, 되밀림. RR vs cited risk [L]; 재설정 shape [V]; 절대 발생률 [O]
- **chronic heart failure** — 안장-마디 BASIN 붕괴: spinodal(κ*)=|load| (닫힌형이 스윕과 일치). 진행 vs cited markers [L]; 붕괴 동역학 [V]; 절대율 [O]

## 5. 절대 규칙 — 연구 먼저, 집필 나중
**매우 높은 수준의 엄격한 연구(많은 스트레스 실험) 완료 전에는 집필 금지.** `tools/build_docs.py`는 잠금 동안 거부. 연구는 GREEN·서명 완료(`reports/research_complete.json`, all_green=true)이며, **`PHASE=writing`로 docs 발행 완료**(v0.5.0).

## 6. 집필 규칙 (VP-SPEC v1.8 — 루트 `VP_SPEC_v1_8.md`)
정본 HTML(C2) · 제목별 별도 SEO HTML(C4: answer-first·JSON-LD·claim-strip·vp-card) · 본문 영어(C0) · 정량 결정론 재생성(C1) · 모든 [O] 사유 명시(C3). 출력: `docs/<slug>/index.html` + 허브 + sitemap/robots/llms.

## 7. 인수인계 (자동) — 다음 세션이 할 일
**연구 GREEN·집필 FINALIZED (v0.6.0).** `PHASE=writing`, `docs/`에 정본 SEO HTML **13페이지(허브+12)** 발행 완료 — 집필 마감 패스에서 **DNA 실측 창발 전용 챕터(§2 `hmd-dna-grounding`)** 신설(각 노드 정체성이 master-gene γ를 실제 human promoter에서 SantaLucia 1998로 측정·SIX2 atlas bit-for-bit 검증한 근거 전면화), 기존 §2–§11 → §3–§12로 재배치, 전 섹션 본문 심화(충실 렌더, 새 수치 없음)·자기비하 어구 제거·SEO 키워드(질병명·기전·DNA 차별점) 메타/JSON-LD 보강. `reports/writing_gate.json` all_pass=true, 전체 트리 결정적(연구 sha=`2e24f935…`, HTML 트리 2×빌드 동일). 재빌드는 멱등(`python tools/build_docs.py`). v0.4.0에서 원장 `[O]→[V]` 1건(REN γ) 측정 완료 — 측정 대기 master 없음. v0.5.0에서 대칭·범용성 완성(저혈압 노드 분해 RP6–RP9·심인성, 범용성 C1). **v0.6.0에서 절대 스케일 `[CAL]` 캘리브레이션 트랙 완성**: 선언된 절대 `[O]` 스케일 9건 각각에 동반 `[CAL]` 행 — 인용 anchor → 이미 잠긴 `[V]` 관계(새 substrate 수학 없음) → anchor로 쓰지 않은 독립 참조로 계산된 판별식 교차검증. 1차원리 유도는 여전히 `[O]`(캘리브레이션 ≠ 유도, 물리 권의 절대 *g* 와 동형), 캘리브레이션 불가 5건(질병 발생률·단일네프론 GFR/K_m·임상 HR/NNT·종간 압력·정확한 계통 전이 clade)은 강제 PASS 없이 잔여 `[O]`. 스트레스 14/14 → **21/21**, 단일 해시 결정적. **집필 마감 — 남은 것은 Phase 7(배포+DOI)뿐이며 저자가 마감 후 진행.**

남은 과제는 아래 트랙뿐 — 전부 파일에 기록되어 있음:

- **A. 배포/DOI (Phase 7, 절차):** ① `docs/` → jamming-physics.org `/homeostasis-hemodynamic` 게시, ② `repro/` → `github.com/rego093-sketch/jamming-physics`의 `repro/homeostasis-hemodynamic/<slug>/`에 push, ③ Zenodo concept DOI 발급 후 `pending(ORCID)` → 실 DOI 치환 (`docs/_meta.json` + claim-strip + `tools/build_docs.py`의 DOI 상수). 근거: `BUILD_NOTES.md` §Assumptions #2·#3.
- **B. 연구 — 등급 상승 [완료, v0.4.0]:** `REN` master-gene γ `[O]→[V]` 측정 완료 = **1.3634** (gc 0.4746). DNA NN-stacking ΔG37(SantaLucia 1998) 파이프라인을 SIX2로 정확 재현(1.5556/0.6381, 무피팅) 검증 후 동일 컨벤션으로 측정(피팅 금지) → `inherited/organ_gamma.json`(genes.REN) 갱신, slow-loop 카드 [V] 승격, 프로모터 `inherited/organ_promoters.cache.json` 캐시 + `inherited/measure_gamma.py` 오프라인 재현. 근거: `IRREPRODUCIBILITY_LEDGER.md` Resolved.
- **B2. 연구 — 대칭·범용성 [완료, v0.5.0]:** ① **저혈압 노드 분해** `repro/_pathology/hypotension_family.py` — RP6 기립성/자율(빠른 완충 상실, RP2 대칭)·RP7 부신(적분기 reference 하향 reset, RP4 거울: 수액 되밀림, mineralocorticoid 지속)·RP8 분포성(SVR effector 붕괴, perfusion floor; 승압>강심)·RP9 저혈량(단방향 나트륨이뇨 → 용적 결손은 수혈만 회복하는 fold)·심인성(RP5 극단, timescale 역전). 노드별 치료 T3. ② **범용성** `repro/_comparative/setpoint_emergence.py` — 방어 setpoint는 닫힌회로+effector+적분기 동시성립 시 창발(C1): open계 incidental → 단일회로 오차규제 → 폐쇄 방어. 둘 다 엔진 `circulate()` + 스트레스 배터리에 배선, **9/9 → 14/14 PASS**, 전부 기존 primitive(새 substrate 수학 없음). 근거: `CHARTER.md` 연구 프로그램 RP6–RP9·C1, `IRREPRODUCIBILITY_LEDGER.md` Open(저혈압 임계·종간 압력).
- **B3. 연구 — 절대 스케일 캘리브레이션 [완료, v0.6.0]:** `repro/_calibration/scale_calibration.py` 신설(엔진 `circulate()`에 `calibration_layer()` 배선, 스트레스 배터리에 CAL1–CAL7 gated). 선언된 절대 `[O]` 9건을 `[CAL]`로 폐합 — 각각 **(i)** 인용 외부 anchor → **(ii)** 이미 잠긴 `[V]` 관계 통과(기존 primitive 재사용, 새 substrate 수학 없음, C1) → **(iii)** anchor로 쓰지 않은 독립 인용 참조와 **계산된 판별식** 교차검증(silent pass 없음). CAL1 mmHg 압력(CO/SVR/CVP→RP1, 네 값 동시 임상범위)·CAL2 baroreflex gain(G=3→완충 0.75)·CAL3 발화 Hz(F_max anchor 1개→전 곡선; setpoint ~50 Hz)·CAL4 macula-densa NaCl/GFR(정직한 ~2× 주석)·CAL5 임상 SBP 고혈압 reset·CAL6 치료 효과크기(RDN 15 % 이내·HF 부호 일치)·CAL7 perfusion floor(≥65)+기립성 임계(≥20). **1차원리 유도는 `[O]` 유지(캘리브레이션 ≠ 유도)**, 캘리브레이션 불가 5건은 잔여 `[O]`(강제 PASS 없음). 스트레스 14/14 → **21/21 PASS**, 결정적. 근거: `IRREPRODUCIBILITY_LEDGER.md` Calibrated (v0.6.0), `CHARTER.md` 연구 프로그램 CAL1–CAL7.
- **C. 선언된 경계 [O] → [CAL] [완료, v0.6.0]:** 절대 스케일 9건(혈압 mmHg / baroreflex gain·latency / 압수용체 Hz / macula-densa NaCl·GFR / 고혈압 발생률 / HF 사건률 / 치료 효과크기 / 저혈압 임계·shock 발생률 / 종간 압력·전이 clade)을 위 **B3 `[CAL]` 트랙**으로 클리닉 스케일에 정착시키고 독립 교차검증. 단, **1차원리 유도와 캘리브레이션 불가 5건은 의도적으로 `[O]` 유지** — 닫힌 것은 "임상 스케일 정착"이지 "유도"가 아님. 근거: `IRREPRODUCIBILITY_LEDGER.md` Calibrated (v0.6.0) 표 + 잔여 Open.
- **D. 외부 의존:** cardiorespiratory 시블링(심박출량 + baroreflex edge, carotid-body/심폐 afferent 인용 시임) 미발행 시 인용 끊김. circulatory(SVR/Windkessel)는 v0.7.0 충족. 근거: `CHARTER.md` Seams IN.

상태는 파일로만 전달, 종료 시 단일 zip으로 다음 세션에. 반환은 압축파일 1개(파편화 금지, C0).
