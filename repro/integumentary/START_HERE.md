# START HERE — Integumentary (integumentary_vp_site)  ·  v1.0.0

> 이 zip을 **새 창에 넣고 이 파일을 먼저 정독**하면 상위 백서 없이 바로 연구를 시작할 수 있다.
> 자족적: 기질 프리미티브(FHN/R19), VP-SPEC v1.8 전문, 장기 정체성 γ를 내부에 들고 있다.

> **v1.0.0 상태 (in-lane 완료 릴리즈).** 담당 물리 클래스(jamming barrier/interface + external insult)의
> 연구·집필 프로그램이 **완료**됐다 — 10개 타깃(T1–T9 + oncology), 23개 질환, 교차패키지 이음매 매니페스트.
> 7개 결정론 해시가 모두 고정·green이며 `python repro/run_release_audit.py` 가 한 번에 재검증한다
> (→ `reports/release_audit.json`, `all_ok=true`). v1.0.0은 **새 메커니즘·새 상수 없이** 통합·인증만 한다.
> 남은 것은 DECLARED-OUT 교차패키지 계약의 *실배선*뿐이며, 이는 아직 없는 통합 하니스를 요구한다(정직히 보류).
> **4-문서 SSOT:** `CHANGELOG.md` · `MASTER_MANUAL.md` · `COMPLETION_LEDGER.md` · `HANDOVER.md`
> (+ `ANCHORS_VERIFIED.md` 의 [L] 앵커 네트워크 검증).

## 0. 한 줄 정체
Epidermis, keratinocyte barrier, melanocyte photoprotection and appendages emerge as the body boundary; wound healing is a jamming->unjamming->re-jamming transition, and UV dose-response is the cleanest R19 carcinogenesis case.

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py          # 코어 배터리 (T1–T5+oncology). sha는 1fb59f556e01... 로 고정
python repro/run_pathology.py    # 추가 레이어: 13개 질환 + 5-way opposite-sign 판별 (sha 0a4404ccde65...)
python repro/run_cycle.py        # 추가 레이어: 모낭 주기 진동자 + 4개 탈모 + 3-way 판별 (sha d910fa5d2854...)
python repro/run_seb.py          # 추가 레이어: 피지선관 jamming(T7) + 여드름·화농성한선염 + 3-way 판별 (sha 1e8a557d9a8d...)
python repro/run_adhesion.py     # 추가 레이어: 세포부착 binding jam(T8) + 천포창·수포성류천포창 + 3-axis 판별 (sha 55dce8c267ea...)
python repro/run_vasomotor.py    # 추가 레이어: 신경혈관 반응성 jam(T9) + 주사(rosacea)·레이노 + 3-axis 판별 (sha 53a99f522ad6...)
python repro/run_release_audit.py # v1.0.0: 위 모든 러너 재실행 + 7개 고정 해시 일괄 대조 → reports/release_audit.json
python repro/run_seam.py         # 가산 레이어: 교차패키지 이음매 매니페스트 — 색소소실→종양 결합 재노출(RR 2.58/10.59/1.13) + 상속/선언 이음매 + 4개 충실도 검사 (sha 52b49a95a9ad...)
```
→ `run_all`은 측정 γ에서 장기를 **창발**(미측정 master는 정직하게 "측정 대상"으로 보류), 진동자 박동 확인, 스트레스 배터리·암 모듈 상태, **집필 잠금 여부**를 출력한다. HTML은 만들지 않는다. `run_pathology`·`run_cycle`·`run_seb`·`run_adhesion`·`run_vasomotor`는 **순수 가산 레이어**로 각자의 해시를 가지며 코어 해시를 건드리지 않는다. `run_seam`은 새 물리 스윕이 아니라 **이미 내부에 있는** 인터페이스들을 하나의 라벨된 기계가독 기록으로 **통합**한다(새 메커니즘·새 상수 없음): 색소소실→종양 결합 수치는 검증된 pathology 레이어에서 **그대로 재노출**되므로 이음매 출력이 곧 내부 링크의 표면화임이 증명되고, 형제-패키지 계약은 *선언(declared), 아직 실배선 아님*으로 정직하게 표기된다.

## 2. 이 백서의 범위 (자기 범위를 명확히)
mind가 하듯 **장기를 직접 시뮬레이션으로 창발하여 순환**시킨다. 단 이 패키지는 기계(mechanism) 동역학을 다루며 felt(느낌)는 mind의 몫이다. 분해 기준은 **물리적 클래스**(이 패키지: jamming (barrier/interface + external insult))이며, 클래스 밖은 형제 패키지 소관 — 아래 이음매로만 인용한다(SSOT).

| master gene | organ | measured γ | physiological role | dyn class |
|---|---|---|---|---|
| TP63 | epidermis | 1.3643 | stratified barrier: basal->cornified transit | barrier |
| KRT14 | keratinocyte | 1.4894 | keratin barrier mechanics / structural integrity | barrier |
| MITF | melanocyte | 1.3945 | melanin synthesis + UV photoprotection | defense |
| EDAR | skin_appendage | 1.3696 | hair follicle / sweat gland (thermoregulation interface) | appendage |
| PRDM1 | sebaceous_gland | 1.3432 | sebaceous-lineage master (Blimp1); pilosebaceous duct occlusion | jamming |

> **모낭 주기 진동자 (v0.5.0):** 위 EDAR γ를 *그대로* 써서 모낭 주기를 **이완 진동자**로 창발(새 장기·새 적합상수 없음). anagen 우세 + plateau→붕괴 파형 [V], 절대 분율/주기 [O]. 가산 레이어 `repro/_cycle/`, 자체 게이트.
>
> **피지선관 jamming (v0.6.0 · T7):** **새 장기** PRDM1/Blimp1(γ=1.3432, MITF/EDAR과 동일 NCBI 프로모터-ΔG 파이프라인으로 *측정*·캐시·vendoring, 오프라인 재현). 피지선관을 *동일* R19 스위치 위 **히스테리시스 2-상태 occlusion jam**으로 창발: 상부 spinodal에서 **불연속**으로 막히고 더 낮은 spinodal에서만 열림(loop 폭≈2.01) [V], 건강 시 patent. occlusion 세트포인트는 무차원 regime scale [F], 절대 병변수는 [O]. PRDM1은 아틀라스 **최저 γ** → 최조기 spinodal(부호 등급 창발-순서 예측 [V]). 가산 레이어 `repro/_seb/`, 자체 게이트.
>
> **세포부착 binding jam (v0.7.0 · T8):** **새 장기 없음** — 위 KRT14 γ를 *그대로* 사용(desmosome/hemidesmosome가 keratin 망을 정착시키므로 부착은 이 장기의 고유 성질; 모낭-주기 패턴이지 피지선 새-장기 패턴이 아님; γ 신규 fetch 없음·적합 없음). 접합 부착을 *동일* R19 스위치 위 **히스테리시스 2-상태 binding jam**으로 창발: 하부 spinodal에서 **불연속** 박리(jump≈2.11, net adhesion≈−1.005), 더 높은 spinodal(≈+1.005)에서만 재부착(loop 폭≈2.01) [V], 건강 시 net adhesion +1.4로 상부 spinodal 위 견고 부착. *동일* γ·spinodal 위 두 구획 — cell-cell(DSG3)·cell-matrix(BP180) — 와 **유도된**(자유 플래그 아님) Nikolsky 부호. reserve/역가는 regime scale [F], 임상 매핑 [L], 절대 병변수/역가/심도/BSA [O]. 가산 레이어 `repro/_adhesion/`, 자체 게이트.
>
> **신경혈관 반응성 (v0.8.0 · T9):** **새 장기 없음** — 위 EDAR γ를 *그대로* 사용(온도조절-인터페이스 장기 EDAR은 두 자율 효과기 팔 — 발한(sudomotor, T5)과 혈관운동(vasomotor, 피부혈류) — 을 가지며, 주사(rosacea)는 혈관운동 팔의 조절이상 = 발한 팔의 다한증의 *혈관판*이므로 이 장기 고유 성질; γ 신규 fetch 없음·적합 없음). 피부 혈관운동 톤을 *동일* R19 스위치 위 **히스테리시스 2-락 반응성 jam**으로 창발: 상부 spinodal에서 **불연속** 확장-락, 하부 spinodal에서 **불연속** 수축-락(loop 폭≈2.01), 그 사이 가역-반응 [V]. 가역성은 *드라이브가 자기 락을 넘었는지*의 균일한 귀결. tone/reactivity/constrictor 드라이브 regime scale [F], 임상 매핑 [L], 절대 홍반지수/혈관밀도/말단온도/BSA [O]. **SSOT 이음매:** 진피 관류 *크기*는 상속 circulatory 인용 그대로(반응성 동역학만 추가). 가산 레이어 `repro/_vasomotor/`, 자체 게이트.

**상속(IN) — 내부 vendoring됨, 재수령 불필요:**
- circulatory: dermal perfusion (cited)
- DNA: organ identity + emergence order [V]
- substrate: FHN/R19 (vendored)

**경계(OUT) — 형제 패키지와의 이음매(SSOT 단일소스 유지):**
- barrier integrity + thermoregulation interface (systemic boundary)

## 3. 판별 타깃 (엄격히 통과시켜야 집필 가능)
- **T1 barrier permeability** — transepidermal water loss crosses a diffusion threshold as the barrier thins [V], abs [O]
- **T2 wound healing** — injury -> unjamming -> collective migration -> re-jamming closure (jamming/unjamming) [V]
- **T3 melanin UV response** — UV dose raises melanin to a protective plateau (negative feedback) [V]
- **T4 epidermal turnover** — basal->cornified transit time matches the cited window [V], rate [L]
- **T5 thermoregulation** — appendage (sweat) response to a thermal load (interface flux) [V]
- **T6 hair-follicle cycle** *(v0.5.0, oscillator on existing EDAR γ)* — anagen→catagen→telogen as an emergent relaxation oscillator; anagen-dominant + plateau→collapse waveform [V], abs fraction/period [O]
- **T7 sebaceous-duct occlusion** *(v0.6.0, new measured PRDM1 organ)* — the pilosebaceous duct as a hysteretic occlusion jam: discontinuous closure at an upper spinodal, reopening only at a lower one [V], set-points [F], abs counts [O]
- **T8 cell adhesion** *(v0.7.0, new target on existing KRT14 γ — no new organ)* — junctional adhesion as a hysteretic two-state binding jam: discontinuous detachment at a lower spinodal, re-adhesion only at a higher one, healthy-adherent, two compartments (cell-cell DSG3 / cell-matrix BP180) on the *same* γ and spinodal, a *derived* Nikolsky sign, and the three-axis opposite-property discriminant (plane / Nikolsky / tension) at the *same* antibody magnitude [V], reserve/titres [F], clinical mappings [L], abs counts/titre/depth/BSA [O]
- **T9 neurovascular reactivity** *(v0.8.0, new target on existing EDAR γ — no new organ)* — cutaneous vasomotor tone as a hysteretic two-lock reactivity jam: a discontinuous dilation lock at the upper spinodal and a discontinuous constriction lock at the lower one, responsive in the reversible middle, reversibility a uniform consequence of *whether a drive crosses its lock*, and the three-axis opposite-property discriminant (vasodilation↔vasoconstriction / fixed↔reversible / vascular↔inflammatory) at opposite drive signs [V], tone/reactivity/constrictor drives [F], clinical mappings [L], abs erythema/vessel/temperature/BSA [O]; **seam:** dermal-perfusion magnitude inherited from circulatory, not re-emerged
- **Seam manifest** *(v0.9.0 — a consolidation layer, **not** a Tn discriminant sweep; no new mechanism, no new constant)* — the master map's §9.2 interfaces gathered into one labelled, machine-readable record in three classes: **INHERITED-IN** (cited circulatory perfusion magnitude / DNA organ identity + γ [V] / R19 substrate, vendored never re-derived), **INTERNAL-LIVE** (the pigment-loss→oncology coupling, re-exported verbatim from the verified pathology layer so the output provably *is* the internal link — albinism-type screen-loss → SCC hazard RR ≈ 2.58× / melanoma burst RR ≈ 10.59×, sunscreen → SCC hazard RR ≈ 1.13×, the screen as causal lever), **DECLARED-OUT** (sibling-package contracts flagged *declared, not yet live wiring*). Grades: coupling shape [V] / cited epidemiology [L] / absolute RR [O]. Gate `seam_gate()`: re-export fidelity, coupling sign + causal lever, provenance + contract validity, non-disturbance

## 4. 담당구역 질환 + 암 (mind과 다른 점)
이 패키지의 **담당구역 질환**을 모두 망라하되, 특히 외부자극(발암물질) 노출 시 암이 **얼마나 더** 발생하는지의 메커니즘을 연구한다. VP-native 커널: 발암물질 = R19 스위치의 지속 이상 드라이브 h_c → 장벽 낮춤 → 악성 basin Kramers 교차율↑ → **RR(dose)** = rate(dose)/rate(0). 판별 = 용량-반응 형상 vs 인용 역학 앵커. 등급: 앵커 [L]/형상 [V]/절대 발생률 [O](장애물 명시). 위치: `repro/_oncology/`.
- **melanoma** ← UV radiation (cumulative + intermittent sunburn)  · anchor: cumulative-UV / sunburn RR for melanoma [L]; barrier-crossing dose-response [V]
- **squamous / basal cell carcinoma** ← UV radiation (cumulative)  · anchor: SCC near-linear with cumulative UV [L]; the clean R19 dose-response showcase [V]

**모낭 주기 질환 (v0.5.0 · T6 진동자 위 · 각각 부호 섭동, 새 상수 없음):** androgenetic alopecia(anti-growth → anagen 단축·소형화; minoxidil 역전), alopecia areata(지속 premature-catagen → anagen 정지; 제거 시 재성장 히스테리시스), telogen effluvium(일시 스트레서 → 동기 telogen 진입 → **한 telogen 뒤** 탈모, 자기제한), anagen effluvium(세포독성 anagen-matrix 손상 → **즉시** 탈모, telogen 우회·가역). 모두 임상부호+개입역전 배터리와 3-way opposite-timing 판별 통과. 발행: `docs/10-hair-follicle-cycle-anagen-telogen/`.

**피지선관 occlusion 질환 (v0.6.0 · T7 jam 위 · 각각 부호 섭동, 새 상수 없음):** acne vulgaris(지속 고-occlusion ≈1.10 → 상부 spinodal 초과 → *염증성* 면포; 레티노이드 단독은 불충분 — 하부 spinodal 아래로 내려야 — 복합 면포용해+피지억제+항균/이소트레티노인이 역전; 항염 단독은 면포성-잔존), hidradenitis suppurativa(더 깊은 아포크린 모낭의 *동일* jam ≈1.50 → plug **파열** → 흉터성 동로(sinus tract) 하위상태 — 여드름을 *낫게* 하는 동일 sub-acne 드라이브로 내려도 파열된 tract는 잔존 → 생물학제제는 활성만 진정, **절개/deroofing**만이 흉터 리셋). 둘 다 임상부호+개입역전 배터리와 3-way opposite-mode 판별(가역 표재 ↔ 비가역 심부 파열; 염증성 ↔ 면포성; 가벼운 ↔ 무거운 plug) 통과. 발행: `docs/11-sebaceous-duct-jamming-acne/`.

**세포부착 수포 질환 (v0.7.0 · T8 binding jam 위 · 각각 부호 de-adhesion, *동일* 항체 크기, 새 상수 없음):** pemphigus vulgaris(anti-DSG3 → *cell-cell* 구획 박리 → 표피내/기저상부(suprabasal) 분리, cell-matrix 결합은 유지("tombstone"); 실패 결합이 측방이므로 전단 전파 → **Nikolsky 양성**, 이완성 수포; 부분 역가 감소는 재부착 안 됨, 항체 제거(rituximab/면역억제)는 재부착), bullous pemphigoid(*동일* 크기 anti-BP180 → *cell-matrix* 구획 박리 → 표피하(subepidermal) 분리, cell-cell 결합 유지(표피가 통째로 들림); 실패 결합이 기저-기질이라 전단 비전파 → **Nikolsky 음성**, 긴장성 수포; 코르티코스테로이드/면역억제로 재부착). **Nikolsky 부호는 어느 구획이 실패했는지로부터 유도**(자유 플래그 아님). 둘 다 임상부호+개입역전 배터리와 3-axis opposite-property 판별(표피내 ↔ 표피하 plane; 양성 ↔ 음성 Nikolsky; 이완성 ↔ 긴장성 수포) 통과 — *구획만으로*, *동일* 항체 크기에서. 발행: `docs/12-cell-adhesion-blistering/`. *경계:* 선천 epidermolysis bullosa(부착 *유전자* KRT14/COL17A1/LAMB3 결함)는 유전자-키 → 유전자-병변 질환 레지스트리, 이 동역학 레이어 아님.

**신경혈관 반응성 질환 (v0.8.0 · T9 반응성 jam 위 · 각각 부호 vasomotor 드라이브, *반대 부호 극*, 새 상수 없음):** rosacea(주사)(지속 혈관확장 반응성 드라이브 / 낮아진 홍조 역치 → 순 확장 드라이브가 *상부* spinodal 초과 → 혈관 확장-락 → 지속 홍반·고정 telangiectasia; 초기 일과성 홍조는 sub-락 여행이라 *복귀*; LL-37/Demodex 염증 증폭기가 동일 확장 배경 위에서 *구진농포형* 부여; 항염은 구진을 없애지만 혈관 배경 잔존, 브리모니딘은 일시적 창백만(고정 혈관 비리셋, 히스테리시스), 레이저/IPL이 고정 telangiectasia를 구조적으로 리셋), raynaud_phenomenon(레이노)(한랭/스트레스 혈관수축 드라이브 → 순 확장 드라이브 음(-)으로 수축/허혈 basin → 가역적 말단 혈관연축 발작; *일차성* 레이노는 락을 넘지 않아 재가온에 가역, 혈관확장제/CCB가 발작 중단). 둘 다 임상부호+개입역전 배터리와 3-axis opposite-property 판별(혈관확장 ↔ 혈관수축; 고정 telangiectasia ↔ 가역 혈관연축[락 규칙]; 혈관성 홍반-telangiectatic ↔ 염증성 구진농포형) 통과 — *드라이브 부호와 락 규칙만으로*, *동일* EDAR γ에서. 발행: `docs/13-neurovascular-reactivity-rosacea/`. *경계:* **이차성 레이노**의 *고정* 말단 허혈/궤양(결합조직질환)은 하류 구조 변화 → 면역/류마티스 형제-패키지 이음매; 진피 관류 크기는 상속 circulatory 이음매 — 둘 다 이 동역학 레이어에서 재창발 안 함.

## 5. 절대 규칙 — 연구 먼저, 집필 나중 (명시)
**매우 높은 수준의 엄격한 연구(많은 스트레스 실험 포함)를 완료하기 전에는 집필하지 않는다.**
- `tools/build_docs.py`는 `gates.writing_locked()`가 True인 동안 **무조건 거부**.
- 잠금 해제: ① `research_gate()` `all_green` ② `gates.write_research_complete()` ③ 루트 `PHASE`를 `writing`으로. 셋 모두 충족 시에만 열림.

## 6. 집필 시 규칙 (VP-SPEC v1.8 — 전문은 루트 `VP_SPEC_v1_8.md`)
- **정본은 HTML**(C2). `docs/` 아래 HTML이 정본 ("html이 정본").
- **제목별 별도 HTML**(C4/6장): 섹션당 1페이지, answer-first(`<p class="answer">` 40–60단어), 자체완결, JSON-LD(ScholarlyArticle·BreadcrumbList), canonical, claim-strip(등급+재현링크+DOI), 인용 잠금량마다 vp-card.
- **본문 영어**(C0), 표·그림 포함. 모든 정량 결정론 재생성(C1, 2×sha256), 모든 `[O]`는 사유 명시(C3).
- 출력: `docs/<slug>/index.html` + `docs/index.html`(허브) + `_meta.json` + `sitemap.xml` + `robots.txt`(봇 허용) + `llms.txt`.

## 7. 사용자 반환 규약
- 종료 시 **압축파일 1개**만 반환(내부 경로 = 패키지 상대경로). 파편화 금지. 받은 자료에 추가/수정분 합쳐 단일 zip 반환(C0).

## 8. 인수인계 (자동)
새 창은 이 `START_HERE.md` → `CHARTER.md` 순서만 읽으면 범위·이음매·타깃·암·게이트·집필규칙을 모두 파악한다. 세션 간 상태는 파일로만 전달되며(이전 대화 기억에 의존 금지, VP-SPEC §1), 종료 시 단일 zip으로 다음 세션에 넘어간다.
