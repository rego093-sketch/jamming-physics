# START HERE — Musculoskeletal (musculoskeletal_vp_site)  ·  v0.7.0 (writing; physiology + oncology + 18-target disease battery + full TREATMENT axis + inherited non-opioid ANALGESIC axis green, each documented as a 4-page cluster §21–§24 / §25–§28; DNA-grounded; §20 register completed)

> 이 zip을 **새 창에 넣고 이 파일을 먼저 정독**하면 상위 백서 없이 바로 연구를 시작할 수 있다.
> 자족적: 기질 프리미티브(FHN/R19), VP-SPEC v1.8 전문, 장기 정체성 γ를 내부에 들고 있다.
> **현재 상태:** 생리(T1–T5)·암(4사이트)·**질환 배터리(T6–T17, 18타깃)**·**치료 축(§21–§24)**·**진통 축(§25–§28, 상속 기법)** 모두 green, 결정론 동일(엔진 해시 불변), 집필 잠금 해제. `docs/`에 §1–§28 HTML 생성 완료.
> **v0.7.0 신규:** analgesic_threshold_logic 볼륨(concept DOI 10.5281/zenodo.20733420)의 **3-레버 비(非)아편 진통 기법을 상속**하여 담당 통증질환에 적용. 이 패키지 concept DOI = **10.5281/zenodo.20755760**.

## 0. 한 줄 정체
Skeletal muscle (the actuator neuro commands), cartilage and bone emerge as load-bearing structures on the jamming substrate; bone remodeling under mechanical load is a yield/jamming threshold (Wolff's law).

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py
```
→ 측정 γ에서 장기를 **창발**, 진동자 박동 확인, 스트레스 배터리[3]·**질환 배터리[3b]**·**치료 축[3c]**·**진통 축[3d]**·암 모듈[4] 상태, 게이트[5]와 **집필 잠금 여부**를 출력한다. HTML은 만들지 않는다. 집필(HTML 생성)은 `python tools/build_docs.py` (잠금 해제 시에만).

## 2. 이 백서의 범위 (자기 범위를 명확히)
mind가 하듯 **장기를 직접 시뮬레이션으로 창발하여 순환**시킨다. 단 이 패키지는 기계(mechanism) 동역학을 다루며 felt(느낌)는 mind의 몫이다. 분해 기준은 **물리적 클래스**(이 패키지: jamming (solid-mechanics / load-bearing))이며, 클래스 밖은 형제 패키지 소관 — 아래 이음매로만 인용한다(SSOT).

| master gene | organ | measured γ | physiological role | dyn class |
|---|---|---|---|---|
| MYOD1 | skeletal_muscle | 1.4933 | myogenic contraction: recruitment + force-frequency (the actuator neuro commands) | actuator |
| SOX9 | cartilage | 1.4598 | chondrocyte load-bearing matrix + growth plate | structural |
| TBX5 | limb_skeleton | 1.4392 | appendicular skeletal patterning (load-bearing scaffold) | structural |
| RUNX2 | bone | 1.2414 (측정완료 [V]) | osteoblast mineralization + load remodeling (Wolff = yield/jamming) | load-remodel |

**상속(IN) — 내부 vendoring됨, 재수령 불필요:**
- neuro: motor command -> muscle recruitment (cited; neuro owns the command)
- DNA: organ identity + emergence order [V]
- substrate: FHN/R19 (vendored)

**경계(OUT) — 형제 패키지와의 이음매(SSOT 단일소스 유지):**
- marrow cavity -> immune_hematologic_vp_site (hematopoiesis site seam)
- mechanical load / posture (systemic)

## 3. 판별 타깃 (생리 — 전부 PASS)
- **T1 force-frequency** — twitch summation -> fused tetanus at cited stimulation frequency [V], rate [L] — **PASS**
- **T2 length-tension** — active force vs sarcomere overlap reproduces the cited curve peak [V] — **PASS**
- **T3 bone remodeling** — sustained load raises density past a yield threshold (Wolff; jamming/yield) [F] — **PASS**
- **T4 growth-plate** — developmental threshold order ranked by gamma over measured organs [V] — **PASS**
- **T5 fatigue** — sustained drive -> reversible force decline with a cited time constant [V] — **PASS**

### 3b. 질환 배터리 (생리 타깃의 인용-중증도 섭동 — 전부 PASS, hard 게이트는 T7d 제외)
판별 = **임상 징후의 방향/형상 재현**(절대값 금지, No-Tuning). 엔진 `repro/_disease/vp_msk_disease.py`,
게이트/문서용 reshape는 `repro/_verify/stress_tests.py::run_disease_suite()`. 연구 게이트가 이 배터리 green도 요구한다.
- **T7a/b/c** master-gene dosage dysplasias — CCD(RUNX2)/campomelic(SOX9)/Holt-Oram limb(TBX5): 0.5 반접합 → **γ-무관 교차 절벽(WT 드라이브의 ⅔)** 아래로 → 교차 실패/부분. 기전 [V]; 임계이동 [F]; 절대 타이밍 [O]. (**T7d** MYOD1=2차 [V?], hard 게이트 제외)
- **T6/T6b** mechanostat 질환 — 폐용성 골다공증 = T3의 **거울**(저-역치 부하가 dense basin 장벽 낮춤) [F]; 골화석증 = 루프 down-branch 제거 [V]. Frost 셋포인트 [L]; 절대 BMD [O].
- **T8/T8b** 신경근전달 — MG: NMJ 역치↑ → 저주파 힘 감소 >10%(RNS), 병변 단조 [V]; LEMS: 시냅스전 결핍 → 고주파 증가(반대 부호) [V]. 임상 징후 [L]; 고주파 강화 미모델 [O].
- **T10** 대사/미토콘드리아 근병증 — T5 섭동: τ 단축(빠른 감소) + 불완전 회복(회복분율 <0.95) [V]; 앵커 [L]; 절대 크기 [O].
- **T9** 골관절염 — 연골 unjamming: **인용 Paris/Basquin** 피로손상법칙(m=2)을 T2 접촉수에 적용; 저-역치 보호, 손실은 부하+BMI에 볼록 [V]; 법칙 형태 [L]; 절대 속도 [O].
- **T4-ext** 연골무형성증 — FGFR3-GOF를 SOX9 성장판 스위치의 억제 드라이브로 → 절벽 있는 단축 사다리 [V]; 절대 장골 길이 [O].
- **T11** 근이영양증(DMD/BMD) — 디스트로핀 소실 = 기계적 취약성 → 수축 접촉수의 Paris/Basquin 피로; reading-frame 규칙(Monaco 1988)이 중증도 결정(DMD null < BMD partial < normal), 비회복성(T5/T10과 구별) [V]; 타임라인 [O].
- **T12** 채널병증(근긴장증/주기성마비) — FHN 흥분성 직접 섭동: 근긴장증은 탈분극-차단 역치 ↑(과흥분, 반복방전), 주기성마비는 ↓(작은 탈분극이 침묵) — MG/LEMS처럼 반대 부호, β에 단조 [V].
- **T13** 피로골절+골유합 — 골은 T4 항복 아래 피로 ENDURANCE LIMIT 보유; 그 위 sub-yield 순환부하는 골절(S-N), sub-endurance는 보호; 골절은 부하로 dense basin 재교차하여 **유합**(연골과 대조) [V]; 골절까지 사이클수 [O].
- **T14** 건병증 — OA 피로 커널을 건 콜라겐 접촉수에 적용: sub-threshold 보호, 과사용에 볼록 [V]; 절대 속도 [O]. (재료-[O] 등록부에서 이동)
- **T15** 근감소증 — 점진적 다축 노화 감소(운동단위 탈락 × 섬유 위축 × 피로 τ 단축): 최대근력 ↓ + 조기 피로 [V]; 절대 근력/속도 [O].
- **T16** 골연화증/구루병 — 무기질화 천장: 밀도 = 매트릭스 점유 × 무기질 공급, 결핍 시 부하로도 천장 캡; 결정적 판별 — 부하는 골다공증은 회복시키나 골연화증은 **회복 불가**(무기질 부재) [V]; 절대 무기질 밀도 [O].
- **T17** 용해성 골질환(골수종/거대세포종) — mechanostat 파골/조골 탈공역: 골수종은 형성 arm 비활성(lytic 고정 = 골화석증의 **거울**), 거대세포종 RANKL 드라이브는 치밀골도 흡수 [V]; 병변 크기/발생률 [O]. 발암 커널 아닌 T3/T6로 모델링.
- **클래스 외/재료 등록부(docs §20)** — 재료질환(OI, EDS/Marfan, 신성 골이영양증)·무(無)-단일스위치-신호 질환(Paget, 척추측만증/고관절이형성/내반족)은 정직한 [O]; **추간판 변성**은 기존 OA(§12)/건병증(§17) Paris/Basquin 피로커널의 **1함수 재사용**이므로 중복(SSOT) 회피 위해 별도 페이지 미생성([O] 아님, 능력 부재 아님); 자가면역(RA/AS/PsA)·결정(통풍)·통증(섬유근통)·감염(화농성 관절염)·원격 원발 골전이는 형제 볼륨으로 이음매 라우팅 — 재창발 금지(SSOT). (건병증은 §17에서 [V]로 구현 완료.)

### 3c. 진통 축 (§25–§28 · 상속한 3-레버 비아편 진통 기법 · 전부 PASS, hard 게이트는 honest-partial 제외)
**새 물리 없음 — analgesic_threshold_logic 볼륨(concept DOI 10.5281/zenodo.20733420)의 3-레버 기법을 그대로 상속**(R19/FHN 프리미티브를 vendoring하듯)하여 담당 통증질환에 **능동 적용**. 통증 = 질환이 섭동하는 **동일 R19 장벽 ΔV=γ²/4** 위의 **역치-교차율**(Kramers): 침해 드라이브 h가 장벽을 깎고 nociceptor가 rate≈exp(−ΔV_eff/D)로 발화. ΔV_eff = max(0, γ²/4 + ΔV_L1 − κ·h). **h는 각 질환 커널의 인용 중증도에서 읽는다**(단일소스, 통증점수로 튜닝 금지).
- **3-레버** — **L1** 말초 역치↑(ΔV_L1↑→rate↓; 국소마취/Na_v차단/국소제, 구조-**비공역**) · **L2** 침해 드라이브↓(h↓→rate↓; NSAID + **기계적 하중 경감**, 구조-**공역**) · **L3** 중추 이득↓(g↓; gabapentinoid/SNRI, **중추 이득 = neuro/mind 소관, 이음매로만 인용·재창발 금지**). 아편 = 4번째 하행성/μ 레버, 비아편 로직 밖(미모델).
- **결정적 판별(falsifiable)** — **L2는 교차율과 질환 자체 구조손실을 둘 다** 낮춘다(공역); **L1은 교차율만 낮추고 병변은 평탄**(비공역). 이 대비가 grounded 커널임을 증명(리도카인 패치가 연골 불변인 채 무릎 통증만 완화). 엔진 `repro/_disease/vp_msk_analgesia.py`(질환 커널 verbatim 재사용, **엔진 미접촉**), reshape `stress_tests.py::run_analgesia_suite()`, 게이트 `analgesia_all_inscope_levers_direction_ok` 요구, 러너 `[3d]`.
- **Ax-T9 골관절염 / Ax-T14 건병증 / Ax-T13 피로골절 / Ax-T17 용해성 골질환** — 4개 채점 통증질환 모두 **L1↓·L2↓ + L2-공역·L1-비공역 교차검증 통과**(DIRECTION, No-Tuning). 실제 약/하중은 인용 [L] 앵커.
- **Ax-T15 운동성 근육통**(근감소/근병증) — L1·L2 모두 방향상 교차율↓이나 **교차검증할 이산 병변 부재** → DIRECTION-only honest-partial(기록, 미탈락, hard 게이트 제외).
- **범위(정직한 [O], 능력 부재 아님)** — L3 중추 이득(neuro/mind, 이음매), 아편 레버(비아편 로직 밖), 신경병증성/섬유근통/중추감작(형제 볼륨 라우팅, §20과 동일). `IRREPRODUCIBILITY_LEDGER.md`에 장애물 명시.
- **기존 연구사례 적용** — 담당 통증질환 각 장(§12·§14·§16·§17·§19)에 "Analgesic lever map (cross-reference)" 블록을 달아 레버 분류를 명시하고 §25–§27로 링크(SSOT: 레버는 §25–§28에서 1회 창발, 질환 장은 인용만).

## 4. 담당구역 질환 + 암 (mind과 다른 점)
이 패키지의 **담당구역 질환**을 모두 망라하되, 특히 외부자극(발암물질) 노출 시 암이 **얼마나 더** 발생하는지의 메커니즘을 연구한다. VP-native 커널: 발암물질 = R19 스위치의 지속 이상 드라이브 h_c → 장벽 낮춤 → 악성 basin Kramers 교차율↑ → **RR(dose)** = rate(dose)/rate(0). 판별 = 용량-반응 형상 vs 인용 역학 앵커. 등급: 앵커 [L]/형상 [V]/절대 발생률 [O](장애물 명시). 위치: `repro/_oncology/`.
- **osteosarcoma** ← ionizing radiation (therapeutic/occupational)  · anchor: radiation RR for bone sarcoma [L]; environmental-carcinogen link WEAK -> mostly genetic [O]; do not overclaim
- **soft-tissue sarcoma** ← ionizing radiation; some chemicals  · anchor: radiation RR [L]; otherwise baseline crossing only (honest: no clean dose-response anchor)
- **chondrosarcoma** ← IDH1/2 neomorphic 2-HG (대사·유전, 환경노출 아님)  · SHAPE만 [V]; 노출 용량앵커 없음, dose축 = 정규화 드라이브 [O]
- **Ewing sarcoma** ← EWSR1-FLI1 융합(유전, 환경 아님; 세포기원 논쟁)  · SHAPE만 [V]; lineage 매핑 stand-in + 용량앵커 [O]

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
