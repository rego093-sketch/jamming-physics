# START HERE — Digestive / Metabolic (digestive_vp_site)  ·  v0.16.0

> **DOI (Zenodo, 개념·버전무관):** `10.5281/zenodo.20755319` — <https://doi.org/10.5281/zenodo.20755319> · CC BY 4.0 · ORCID 0009-0002-7535-8245.
> **v0.16.0 = §30이 라이브 교차-패키지 하니스를 구축 (마지막 프런티어 항목).** 이 권을 형제 VP 권들(circulatory·musculoskeletal·neuro)과 **한 프로세스**에 적재해, **라이브 형제 엔진**에 대해 §27 seam·§28 진통 계층이 신뢰로 취했던 교차-권 항등식을 확인한다: (1) **공유 R19 기질** — 모든 권의 발화-문턱 spinodal |h_sp| = 2(g/3)^1.5 및 장벽 g²/4가 byte-identical(교차-권 drift 0); (2) **circulatory 간 seam** — circulatory의 라이브 `hepatic_clearance()`가 vendored 스냅샷 재현(Q_H=1500 mL/min, E=0.75, F=0.25, CL_H=1125 mL/min); (3) **상속 27-표적 진통 지도**가 모든 권의 자체 spinodal을 통해 bit-for-bit 재유도(drift 0), 이미 진통 계층을 탑재한 두 번째 호스트 musculoskeletal이 같은 spinodal에서 레버를 읽음; (4) **neuro felt-symptom 종점** — §18→`mind` 단방향 포인터가 가리키는 말초 통각수용체(Na_V1.7/SCN9A, 마스터 PRDM12 — §28 L1 레버가 차단하는 채널). 하니스는 **모든 게이트 밖**에서 실행: 연구 게이트·정본 빌드는 여기서 아무것도 계산하지 않고 형제를 import하지 않음 — 각 권은 형제가 **부재**한 상태로 자체 아카이브에서 신뢰 상태를 재확립(verify-alone), 형제 엔진은 **파일-경로로 적재(import 아님)**, 하니스 다이제스트는 in-package 계약만 해시하므로 **형제가 디스크에 있든 없든 byte-identical**(`21509b67…`). 하니스는 자체 새 다이제스트를 지니고, 엔진(`2d363033…`)/질환(`a2c32ff9…`)/C6(`cbc73465…`)/seam(`757a8dea…`)/진통(`720a4229…`)은 모두 **불변**, 재빌드 byte-identical. 검증 계층: **새 프리미티브·새 주장·새 `[O]` 없음.**
> **v0.15.0 = §29가 in-substrate 소화기 Tier-1 표면을 REUSE로 닫음.** dyssynergic defecation(§16 게이트를 항문직장 출구에서 읽음 — 이완불능증의 거울; 추진력은 온전한데 출구가 닫혀 정체 = gate-not-drive), Hirschsprung(§4 분절 무신경절 차단 → 근위 확장), MODY(§12 표적 β-분비 병변 → 1형 폭주와 구별되는 별개의 규제된 곡선), hepatic GSD-I(§6 글리코겐 완충 방출 불능 → 공복 저혈당 + 역조절 실패), autoimmune gastritis(§22 발적을 체부-국소로 → 국소 장벽 + 산 저하). **새 프리미티브 없음·형제 패키지 없음**; 단일유전 3종(Hirschsprung RET·MODY PDX1/HHEX·GSD G6PC)은 gene-key → `disease_wp`. 엔진(`2d363033…`)/C6(`cbc73465…`)/seam(`757a8dea…`)/진통(`720a4229…`) 다이제스트는 **불변**, 질환 다이제스트만 이동 `2e98a0d7…`→`a2c32ff9…`, 재빌드 byte-identical.
> **v0.14.0 = 발행 마감 릴리스 (DOI 발행 + 발견성 프런트매터).** 새 질환 모듈은 없다.
> (1) **DOI 발행 (v0.13.0):** 확정 DOI를 정본 HTML 전체(모든 claim-strip·footer·`_meta.json`·`llms.txt`)와 ScholarlyArticle / CreativeWorkSeries JSON-LD(기계판독 identifier: PropertyValue propertyID=DOI + sameAs)에 baking.
> (2) **발견성 프런트매터 (v0.14.0):** VP-SPEC v1.8 정본 골격(answer-first·JSON-LD·claim-strip·vp-card)으로 3개 개관 페이지를 추가 — `/about/`(작업의 규모·DNA 창발 기반·전체 범위·재현성·정직한 등급), `/methods/`(DNA→γ→R19 창발 방법론, 라이브 γ 표), `/faq/`(**FAQPage 스키마** 11문항, 구글 리치결과·AI 어시스턴트용). 이 작업이 *간이 시뮬레이션이 아니라 실제 DNA를 창발한 근거 있는 결정론적 모델*임을 정면으로 드러내고 구글 노출을 노린다.
> 엔진·질환·종양·seam·진통 다이제스트는 모두 **불변**(DOI·프런트매터 모두 엔진 위 표현 레이어), 빌드는 byte-identical 재현.
>
> 이 zip을 **새 창에 넣고 이 파일을 먼저 정독**하면 상위 백서 없이 바로 연구를 시작할 수 있다.
> 이 패키지는 **자족적**이다: 기질 프리미티브(FHN/R19), VP-SPEC v1.8 전문, 장기 정체성 γ, (심폐는) 심박 앵커를 내부에 들고 있다.

## 0. 한 줄 정체
Gut (ICC slow-wave + peristalsis) and the endocrine pancreas/liver (glucose-insulin-glucagon loop) emerge on the substrate; brain-facing (HPA/neuromodulator) endocrine stays in mind -- this package owns BODY-metabolic endocrine only.

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py
```
→ 측정 γ에서 장기를 **창발**하고, 진동자(FHN)가 박동함을 확인하고, 스트레스 배터리·암 모듈 상태를 출력하고,
**집필 잠금 여부**를 보고한다. (HTML은 만들지 않는다 — 집필은 게이트로 막혀 있다.)

## 2. 이 백서의 범위 (자기 범위를 명확히)
mind가 하듯 **장기를 직접 시뮬레이션으로 창발하여 순환**시킨다. 단 이 패키지는 기계(mechanism) 동역학을 다루며 felt(느낌) 층이 아니다 — felt/내수용은 mind의 몫이다.

**창발 대상 장기 (정체성·발생순서는 DNA에서 인용, 동역학만 이 패키지가 추가):**

| master gene | organ | physiological role | dyn class |
|---|---|---|---|
| BARX1 | stomach | gastric ICC slow-wave + mixing | oscillator |
| CDX2 | intestine | intestinal ICC slow-wave + peristaltic propulsion | oscillator |
| PDX1 | pancreas | endocrine islet: insulin/glucagon glucose homeostat | control-loop |
| HHEX | liver | hepatic glucose storage/release (glycogen buffer) | control-loop |

**상속(IN) — 내부 vendoring됨, 재수령 불필요:**
- DNA: organ identity (BARX1, CDX2, PDX1, HHEX) + emergence order [V]
- substrate: FHN/R19 (vendored; ICC slow-wave = FHN at very long tau_s)
- circulatory: hepatic first-pass kinetics (cited)

**경계(OUT) — 형제 패키지와의 이음매(SSOT 단일소스 유지):**
- absorbed glucose flux -> circulatory milieu
- metabolic state -> does NOT re-enter mind's HPA; firewall kept

## 3. 판별 타깃 (엄격히 통과시켜야 집필 가능)
- **T1 gastric slow wave** — ICC FHN intrinsic frequency = cited ~3 cpm [V], rate [L]
- **T2 frequency gradient** — duodenum (~12 cpm) > ileum (~8 cpm) reproduces the aboral slow-wave gradient [V]
- **T3 peristalsis** — a slow-wave phase gradient produces net aboral transport (a directed flux) [V]
- **T4 glucose homeostat** — a glucose load returns to ~5 mM via the insulin loop; setpoint [L] [V]
- **T5 counter-regulation** — hypoglycemia triggers glucagon/hepatic release back to setpoint (bounded loop) [V]
- **DZ1 dysrhythmia + gastroparesis (§11)** — τ_s가 EGG 밴드(brady<2.5 / normal~3 / tachy>3.7 cpm)를 가로지르고, 더 빠른 *결합된* 이소성 focus가 빈맥성으로 entrain, ICC 밀도가 위 배출을 단계적으로 감소 [V]/[L]/[O]
- **DZ2 diabetes T1/T2 (§12)** — 한 항상성 루프에서 β-용량 손실 → 7 mM 넘는 파국적 고혈당, 민감도 손실 → 보상된 상승 설정점; matched-depth 격차 확대 [V]/[L]/[O]
- **DZ3 gastritis/ulcer (§13)** — §7 커널 위 침식 RR 볼록(NSAID 앵커 RR≈4); 위(방어 g) vs 십이지장(산 h) 궤양 분리; 만성 Hp가 §10 암-단계 장벽 공유 [V]/[L]/[O]
- **DZ4 intestinal motility (§14)** — 추진 구동 손실 → 서행성 변비 → 역치 아래 불응성 결장 무력증; ICC 밀도 손실 → 기능적 가성폐색(내강 개방); 일시적 구동 손실 → 가역적 마비성 장폐색; 하나의 ICC 병변이 위(§11)+장(§14)을 함께 붕괴 [V]/[L]-보류/[O]. **치료표적 판독 포함**
- **DZ5 scattered Tier-1 (§15)** — 덤핑: 구우르 빠른 전달이 더 높은 포도당 피크 + 후기 이상 반응성 저혈당(3.9 mM 교차)을 §5에서 창발(기계적 크기는 정직한 [O]); 역류성 식도염 침식은 공유 §13 커널; 인슐린종은 §12 1형의 거울상(절제로 회복) + 반응성 저혈당; 기능성 소화불량은 §11 ICC 축의 경미한 점(중증 위마비와 구별); SIBO 우햌(§4 구동 감소로 잔류 분율 증가) [V]/[L]/[O]. **치료표적 판독 포함**
- **DZ6 sphincter-gate (§16, 첫 Tier-2 프리미티브)** — 장력적으로 닫힌 R19 게이트(저항 = tone + spinodal): GERD는 게이트가 닫힌 채 실패(LES tone 감소 → 역류 부담 증가, 21개 중 0→18 이벤트), 이완불능증은 같은 게이트가 열리지 않는 실패(전향성 우햌, GERD의 거울상) + 운동소실 — 하나의 게이트, 두 가지 반대 실패; 식도 경련은 §4 조율 손실로 이송 붕괴 + 진폭이 구제 못함(jackhammer); 오디 괄약근은 멉힌 게이트로 유출 폐쇄 [V] 운동 / [O] 느낌·절대치. **치료표적 판독 포함**
- **DZ7 accommodation reservoir (§17, 둘째 Tier-2 프리미티브)** — 같은 §2 R19 스위치를 위저부 벽으로 읽음: 미주 적응 구동 `h_acc`가 수축한 벽을 항복점으로 이완 → 벽 강성 `k = 3s² − g`, 컴플라이언스 `C = 1/k`, 고정 식사 압력 `P = V·k`; 적응 저하 → 저장소 경직 → 고정 식사가 조기에 압력 상승(조기 포만, 식후 불편감), 적응 스윕 전체에서 단조; 최대-컴플라이언스 항복점 = R19 스피노달(폐형식 항등식 [F]); 치료는 컴플라이언스 항을 올려 식사 압력을 낮춤 [V] 압력/컴플라이언스 + 항복 항등식 [F] / [O] 느낌·절대 부피/압력 스케일. **치료표적 판독 포함**
- **DZ8 visceral afferent gain (§18, 셋째 Tier-2 프리미티브)** — 같은 R19 요소를 내장 구심신경으로 읽음: 벽 팽창 입력에 대한 정적 감수성 `χ = ds*/dh = 1/k = 1/(3s² − g)` — §17 저장소가 위저부 컴플라이언스로 읽는 *바로 그* 곡률 역수(하나의 곡률, 두 판독). IBS = §14 이송 바이어스 운동 아형(잔류 분율로 IBS-C 0.64 → IBS-M 0.30 → IBS-D 0.00 순서; 설사측 절대 크기는 §15 보존 덩어리 천장에 막힘, 정직한 [O]) + 상승한 구심 이득(내장 과민: 이득·고정팽창 신호 단조 상승 = 이질통 ×1.99, 스피노달 넘어 정상 팽창이 불연속적으로 자발 발화로 전환); 기능성 복통 = 정상 운동에서 상승한 이득(구조적 병변 없음); 이득은 §17 저장소 항복 = 같은 R19 스피노달에서 발산. 말초 구심 항만 — 느낌·정동은 `mind`(방화벽) [V] 아형 순서 + 과민 이득/이질통 / [F] 이득=컴플라이언스 항등식 + 스피노달 발산 / [O] 느낌 통증·절대 빠른-통과 크기. **치료표적 판독 포함**
- **DZ9 immune relapsing-inflammation (§22, 첫째 Tier-3 프리미티브)** — 재발성 점막 염증을 §2 R19 스위치의 *자기지속* 발적(flare) 분지로 읽음(`flare_state`/`inflammatory_barrier_scale`, R19 유도, 맞춤 없음). IBD는 재발-완화 **히스테리시스**를 보임(발적 전환 구동 > 완화 복귀 구동 — 유발 인자가 물러나도 발적이 지속), 이것이 **유도 대 유지 용량 비대칭**을 강제(유도는 항원+스피노달 ≈ 0.885을 넘어야, 유지는 ≈ 0.115 — *같은* 중간 용량이 완화는 유지하나 발적은 깨지 못함); 누적 부담이 §10 커널이 H. pylori에 쓰는 *바로 그* §7 장벽 스케일을 낮춰 대장염 연관 대장암 RR이 인용 UC 앵커(RR≈2.4, Jess 2012)까지 단조 상승하고 지속 완화 시 1.0으로 붕괴 — §21 소장 선암 경계를 닫음; 셀리악·현미경적/호산구성/자가면역 장병증은 항원 의존 영역(구동 제거→완화, 장벽/융모 회복) [V] 히스테리시스+비대칭+부담→장벽→암 / [F] 스피노달 역치 / [L] 대장염-CRC 앵커 / [O] 절대 발생률·셀리악 흡수 크기·느낌 성분. **치료표적 판독 포함**
- **DZ10 exocrine autodigestion (§23, 둘째 Tier-3 프리미티브)** — 췌장 효소원 캐스케이드를 §2 R19 스위치의 **자가촉매** 자기증폭 항(활성 트립신이 트립시노겐 활성화)으로 읽음(`autoactivation_threshold`/`autodigestion_latched`, R19 유도, 맞춤 없음). 자가활성 역치는 보호 억제제와 함께 상승(SPINK1 ↑; PRSS1-기능획득/SPINK1-소실 ↓ — 유전성 췌장염 유전학을 하나의 역치 이동으로); 역치 아래 유발은 안전하게 소멸하나 역치 위 유발은 **latch**(유발 제거 후에도 +g·s 항이 자기지속) — 어떤 매개변수 이동으로도 비가역, 따라서 개입은 **역치 이전에만**(스피노달 넘는 강한 억제제만이 분지를 소멸); 만성 거울상: 큰 분비 예비능이 EPI/지방변을 ~90% 선포 손실까지 지연(DiMagno 1973), 잔여 용량에 단조, PERT가 소화 수요 위로 출력 복원 [V] 역치-상승+비가역 latch(역치-이전만)+강한-억제제 가역성+큰-예비능 EPI+PERT 구제 / [F] latch는 강제된 R19 히스테리시스 / [L] >90%-손실 예비능 역치 / [O] 절대 유발/억제제+수요 스케일·확립된 질환 결과(괴사·장기부전); CFTR 유전자-키 → `disease_wp`. **치료표적 판독 포함**
- **DZ11 perfusion-viability (§24, 셋째 Tier-3 프리미티브)** — 관류된 조직을 §2 R19 스위치가 **생존 분지**(s=+√g)에 정지, 편향 h = 관류 − 수요로 읽음(`perfusion_threshold`/`viability_margin`/`tissue_viable`, R19 유도, 맞춤 없음). 만성 장간막 허혈(장 협심증): 구제 역치 위 생존 여유가 식후 수요 상승에 따라 떨어져 적자로 교차(혈관재건이 양의 여유 복원). 급성 장간막 허혈/허혈성 대장염: 급성 폐색이 demand−spinodal을 넘어 생존→허혈 **플립**, 재관류는 구제창(= 2·spinodal) **이내**에서만 조직 회복(부분/지연 재관류는 경색 잔존). NAFLD/MASLD는 §12 2형 이득-손실 항상성 그대로 재사용; 간 지질-침착 층은 `circulatory` seam 선언 [V] 여유 붕괴+혈관재건+폐색 플립+시간-임계 구제창+§12 재사용 / [F] 허혈-플립·구제 역치는 정확한 spinodal 항등 / [O] 절대 관류/수요 스케일·구조적 경색·`circulatory` 지질층. **치료표적 판독 포함**
- **DZ12 hepatobiliary/bile (§25, 넷째 Tier-3 프리미티브)** — 콜레스테롤-담즙 결정화를 §2 R19 스위치(용해상 = 정지 분지, 콜레스테롤 포화지수 CSI = 편향)로 읽음(`nucleation_barrier`/`supersaturation_drive`/`stone_nucleates`, R19 유도, 맞춤 없음). 과포화(CSI>1)는 **준안정**하며 충분하지 않음 — 결석은 CSI > 1 + spinodal(Kramers 교차)을 넘어야만 핵형성하고, 형성된 결석은 **용해 히스테리시스**(포화 아래에서 지속, 훨씬 아래에서만 재용해 — UDCA는 작고 이른 결석에만)를 보임. 담낭 정체 = §16 B1 게이트 seam, 담낭염 = B1 게이트 + 인용 §22 C1 발적, 담도 운동이상 = B1 게이트, 핵형성 시간 = §7 Kramers 율 [V] 준안정 과포화+장벽-게이트 핵형성+용해 히스테리시스 / [F] 핵형성·용해 역치는 정확한 spinodal 항등, 핵형성 시간은 Kramers 율 / [O] 절대 CSI 스케일·B1/C1 정체/발적 seam·`circulatory`/`mind` seam. **치료표적 판독 포함**
- **DZ13 structural/wall (§26, 다섯째 Tier-3 프리미티브)** — 대장 벽을 §2 R19 요소가 온전히 정지(s=−√g), 분절 Laplace 압력 P = 장력/반경으로 구동되는 것으로 읽음(`laplace_pressure`/`herniation_threshold`/`wall_herniates`, R19 유도, 맞춤 없음). P = 장력/반경에 의해 저섬유소 식이(작고 단단한 대변을 강한 분절 수축이 잡음 → 작은 반경)가 반경이 줄며 벽 압력을 높이고, P > spinodal(g_wall)을 넘으면 온전한 벽이 게실로 **탈출**; 약한 벽(노화 결합조직, Ehlers–Danlos/Marfan 콜라겐)은 더 낮은 역치로 정상 벽이 견디는 압력에서 탈출. 치료는 기하의 역전: 섬유소가 대변을 부풀려(큰 반경) 분절 수축을 부드럽게(낮은 장력) → P를 역치 아래로. 게실염 = 인용 §22 C1 발적; 기계적 고정-차단 폐색(탈장(열공 포함)·염전·장중첩·유착) = §14 기능 모듈의 구조적 대응물(외과적, 모델 외) [V] 반경 감소 시 Laplace 압력 상승+불연속 탈출+약한 벽 낮은 역치+섬유소 치료 / [F] 탈출 역치는 정확한 spinodal 항등 / [O] 절대 압력/강도 스케일·§22 C1 게실염 seam·§14 폐색 대응물. **치료표적 판독 포함**
- **DZ14 잔여 in-substrate Tier-1 표면 (§29, REUSE — 새 프리미티브 없음·형제 패키지 없음)** — FUTURE_WORK §1A–§1D가 남겨둔 5개 장애를 검증된 모듈/프리미티브의 **재사용**만으로 닫음. (a) dyssynergic defecation = §16 게이트를 **항문직장 출구**에서 읽음(이완불능증의 거울) — 출구가 닫힌 채면 추진력이 온전해도 변이 정체(이완 실패 또는 역설 수축), 추진 **구동은 정상** → 병변은 게이트지 구동이 아님(대장 무력증 §14과의 반증가능 구별). (b) Hirschsprung = §1 창발 + §4 이송에 분절 무신경절 병변(진동자 부재) → 항문측 통과가 죽은 분절 길이만큼 점진 차단·심부 무신경절대 미통과·이행부 근위에 변 정체(근위 확장); RET gene-key → `disease_wp`. (c) MODY = §12 항상성에 표적 부분 β-분비 병변 → 별개의 안정·**규제된** 상승 곡선(식사가 상승한 정지점으로 복귀)으로 §12 1형 폭주와 명확히 구별; PDX1/HHEX gene-key → `disease_wp`. (d) hepatic GSD-I = §6 역조절에 간 글리코겐-완충 **방출** 불능 → 공복 포도당이 출력 저하에 따라 저혈당으로 표류·저혈당 챌린지가 정지점으로 복귀 불가(역조절 실패); G6PC gene-key → `disease_wp`. (e) autoimmune gastritis = §22 재발-염증 발적을 **체부-국소**로 + §7 장벽 → 국소 장벽 병변 + 산출력 저하(체부 장벽에 결합, 무위산), 구동 억제 시 양쪽 회복. 모든 표현형은 넓은 스윕에서 **창발**(맞춤 없음); 느낌(→`mind`)·흡수 크기(B12/철, 흡수층)·무위산 카르시노이드 경계(`disease_wp`)는 [O]. **치료표적 판독 포함** [V]/[L]/[O]
- **DZS cross-system 심을 와이어링 (§27, v0.11.0)** — 선언만 되어 있던 circulatory/mind 심을을 **인용/포인터 전용**으로 와이어: circulatory 간 인터페이스(Q_H=1500 mL/min, E=0.75, F=0.25 — circulatory가 'Seams OUT' SSOT 소유자)를 **vendored 스냅샷**으로 소비(형제 코드 import 없이)하여 §24 NAFLD/MASLD 지질 부하와 §25 담즘 콜레스테롤의 **전달 기질**로 삼고(처리/절대값은 [O], circulatory 소유); mind 느낌-증상 심을(§18 내장통, §25 담도산통)은 **단방향 forward-defer 포인터**(소비값 없음 → mind M18 내수용 경로, Saper 2002); 방화벽은 **구조적 락**(패키지 전체 0 형제-import, 대사 상태에 felt/HPA 키 없음 — mind가 neuro-측에서 돌리는 그 락)으로 강제 [V]/[F]/[O]. **치료표적 포함**
- **DZA INHERITED 진통 표적 로직 (§28, v0.12.0)** — *이 레이어는 로드맵에 없었으나 요청에 따라 상속되어 이제 지속 적용된다(주어진 내장통이 필요로 하는 약물 클래스를 가리키는 데 유용하므로).* 형제 백서 `analgesic_threshold_logic` v2.0(개념 DOI 10.5281/zenodo.20733420, CC BY 4.0 — 27개 비-아편 진통 표적의 DNA-기반 지도)을 `inherited/analgesic_targets.json`으로 vendored 하고 `repro/_analgesic/analgesic_logic.py`로 적용: 각 통증 유전자 프로모터의 γ = −mean(NN 스태킹 ΔG, SantaLucia 1998)를 R19 발화-역치 척도 |h_sp| = spinodal(γ) = 2(g/3)^1.5 위에 놓는데, 이는 **이 패키지 자신의 `inherited/vp_substrate.spinodal`과 바이트 동일** — 즉 §18 내장 구심 이득 χ=1/k가 발산하는 *바로 그* 스피노달 — 이라서 27개 표적 판독이 로컬 기질을 통해 **drift 정확히 0**으로 재유도된다. 27개는 세 약물-클래스 레버로 정렬(L1 내향 전류 감소 Na_V/Ca_V/ASIC/P2X/TRP, L2 K_V7 브레이크 열기, L3 NGF/CGRP 구동 제거)되며 **각 레버가 §18 발화 역치를 올리고 이득을 기준선으로 되돌림** — IBS 과민(§18)·기능성 복통(§18)·기능성 소화불량 통증(§17)·담도산통(§25)·식도 연축 통증(§16)에 대한 *인용된 약물-클래스 포인터*. GI 부담 우선순위(선언 가중치, γ는 점수에 결코 포함 안 함)는 Na_V1.8 → NGF → Na_V1.7을 표면화; 정밀 내장-국소마취는 네 개 장 통각 진입 포트를 하전된 역치-상승제와 짝지음. 방화벽은 **그대로 상속** — γ는 프로모터 STRUCTURE만 읽음(전압/효력/용량/생체-선택성/효과 결코 아님), 모든 임상 크기와 *느낌* 통증은 [O]/`mind`, 레버 강도 δ는 구조적이지 용량이 아님, 아무것도 처방하지 않음. 엔진/질환/종양 다이제스트는 통합으로 **불변**. **치료표적 포함** [V]/[F]/[O]
- **DZD** — 질환 레이어 2×sha256 결정론 [V]

## 4. 암(cancer) — mind와 다른 점
외부자극(발암물질) 노출 시 암이 **얼마나 더** 발생하는지의 메커니즘을 연구한다. VP-native 커널: 발암물질 = R19 스위치의 지속적 이상 드라이브 h_c → 장벽을 낮춤 → 악성 basin으로의 Kramers 교차율↑ → **RR(dose)** = rate(dose)/rate(0). 판별 = 용량-반응 기울기/형상을 인용된 역학 앵커에 맞춤. 등급: 앵커 [L] / 형상 재현 [V] / 절대 발생률 [O](장애물 명시). 위치: `repro/_oncology/`.
- **colorectal carcinoma** ← processed/red meat N-nitroso; heterocyclic amines  · anchor: RR vs processed-meat intake (IARC class) [L]; shape [V]
- **gastric carcinoma** ← H. pylori inflammation x dietary N-nitroso; high salt  · anchor: infection x carcinogen synergy RR [L]; synergy [V]
- **pancreatic carcinoma** ← tobacco smoke  · anchor: RR vs smoking pack-years [L]; shape [V]

## 5. 절대 규칙 — 연구 먼저, 집필 나중 (명시)
**매우 높은 수준의 엄격한 연구(많은 스트레스 실험 포함)를 완료하기 전에는 집필을 시작하지 않는다.**
- `tools/build_docs.py`는 `gates.writing_locked()`가 True인 동안 **무조건 거부**한다.
- 잠금 해제 조건 셋이 모두 충족돼야 집필이 열린다: ① `repro/_verify/gates.py`의 `research_gate()`가 `all_green` ② `gates.write_research_complete()` 호출로 `reports/research_complete.json` 생성 ③ 루트 `PHASE` 파일을 `writing`으로 변경.

## 6. 집필 시 규칙 (VP-SPEC v1.8 — 전문은 루트 `VP_SPEC_v1_8.md`)
- **정본은 HTML** (C2). `docs/` 아래 HTML이 정본이다 ("html이 정본").
- **제목별로 별도 HTML** (C4 / 6장): 구글·RAG 추출을 위해 섹션당 1페이지. answer-first(`<p class="answer">` 40–60단어), 자체완결, JSON-LD(ScholarlyArticle·BreadcrumbList), canonical, claim-strip(등급+재현링크+DOI), 인용 잠금량마다 vp-card.
- **본문은 영어** (C0). 표·그림 포함. 모든 정량은 결정론 재생성(C1, 2×sha256). 모든 `[O]`는 사유 명시(C3).
- 출력: `docs/<slug>/index.html`(섹션별) + `docs/index.html`(허브) + `_meta.json` + `sitemap.xml` + `robots.txt`(봇 허용) + `llms.txt`.

## 7. 사용자 반환 규약
- 작업 종료 시 **압축파일 1개**만 반환(내부 경로 = 패키지 상대경로). 파편화 금지. 받은 자료에 추가/수정분을 합쳐 단일 zip으로 반환 (C0).

## 8. 디렉토리
```
digestive_vp_site/
├── START_HERE.md            ← (이 파일) 새 창 부팅
├── CHARTER.md               ← 범위·이음매·타깃·암 범위 (정본 스코프)
├── VP_SPEC_v1_8.md          ← 작업표준 전문 (집필 시 적용)
├── PHASE                    ← "research" (집필 잠금 해제 전 고정)
├── VERSION
├── inherited/               ← vendoring된 상속 자산 (재수령 불필요)
│   ├── vp_substrate.py      ← FHN Neuron + R19 (프리미티브 단일소스, 수정 금지)
│   ├── organ_gamma.json     ← 이 패키지 장기들의 측정 γ (DNA에서)
│   ├── organ_identity.md    ← master gene → organ, 등급 [V] (DNA atlas 인용)
│
├── repro/
│   ├── _engine/vp_dig_engine.py   ← 장기 창발 + 순환 (창발·동역학 구현 완료)
│   ├── _verify/stress_tests.py     ← 스트레스 배터리 T1–T5·ONC·DZ1–DZ14·DZS(§27 seam)·DZA(§28 inherited analgesic)·DZD (전부 PASS)
│   ├── _verify/gates.py            ← 연구/집필 PHASE 게이트
│   ├── _oncology/carcinogen_dose_response.py  ← 발암물질 용량-반응 커널 (§7–§10) + C6 신생물 확장 (§19–§21: 화생 단계·시너지·가역성)
│   ├── _disease/disease_modules.py ← 질환 모듈 D1–D13 (§11–§18, §22–§26; D1–D5 Tier-1 섭동 + D6 Tier-2 게이트 + D7 Tier-2 적응-저장 + D8 Tier-2 구심-이득 + D9 Tier-3 면역-염증 + D10 Tier-3 외분비-자가소화 + D11 Tier-3 관류-생존성 + D12 Tier-3 간담도-담즙 + D13 Tier-3 구조-벽역학 + 치료표적)
│   ├── run_all.py                  ← 연구 진입점
│   └── REPRODUCE.md
├── tools/build_docs.py      ← 집필 HTML 생성 (게이트 통과 전 거부; §1–§26 생성)
├── docs/                    ← (집필 전 비어 있음) 정본 HTML 생성 위치
├── manifest/digestive_vp_site.csv
├── reports/                 ← gate.json / research_complete.json
└── IRREPRODUCIBILITY_LEDGER.md
```

## 9. 추후과제 (Future work — GI 질환 모듈 로드맵)
v0.7.0까지 **첫 8개 질환 섹션을 구현했다**: §11 위 부정맥/위마비, §12 당뇨 T1/T2 스펙트럼, §13 위염/소화성 궁양, §14 장운동/통과 장애, §15 산재된 Tier-1 섭동(덤핑·역류·인슐린종·기능성·SIBO), §16 괄약근-게이트 장애(첫 Tier-2 프리미티브인 장력 R19 게이트 — GERD·이완불능증이 하나의 게이트의 두 반대 실패), §17 위 적응-저장(accommodation reservoir) 장애(둘째 Tier-2 프리미티브 — 같은 R19 스위치를 위저부 벽으로 읽어 강성 `k = 3s² − g`이 컴플라이언스를 결정; 적응 저하 → 저장소 경직 → 고정 식사가 조기에 압력 상승 → 기능성 소화불량·식후 불편감/조기 포만; 최대-컴플라이언스 항복점 = R19 스피노달, 정확), 그리고 §18 내장 구심-이득(visceral afferent gain) 장애(셋째 Tier-2 프리미티브 — 같은 R19 요소를 내장 구심신경으로 읽어 감수성 `χ = 1/k = 1/(3s² − g)`가 §17 저장소가 컴플라이언스로 읽는 *바로 그* 곡률 역수; IBS = §14 이송 바이어스 운동 아형(IBS-C → IBS-M → IBS-D 순서) + 상승한 구심 이득(내장 과민: 이득 상승·이질통·스피노달 넘어 자발 발화), 기능성 복통 = 정상 운동에서 상승한 이득; 이득은 §17 저장소 항복 = 같은 R19 스피노달에서 발산 — 하나의 곡률, 세 판독; 느낌 통증은 `mind` 방화벽); 그리고 발암물질 커널을 **§19–§21 신생물 확장(C6, v0.8.0)**으로 확장했다 — 바렛/코레아 **화생 전구체 단계**(같은 g-감소를 이산적·율속 구획으로 읽음: 바렛→식도선암 전구체 RR≈11, 위 장상피화생 RR≈3.6; 악성 교차가 전구체에서 율속, 이형성 사다리 가속, 절제/제산이 g 복원 → 율속 붕괴), HBV×아플라톡신(간세포암)·흡연×알코올(식도편평세포암) **시너지**(결합 RR≈22/≈17, 가산-널 초과 = 초가산; 스피노달 근처 **하위곱셈성** 반증가능 예측), 그리고 H. pylori MALT 림프종이 g-복원(제균) 시 **퇴행**(가역성)·HPV 단일 드라이브 항문암(단조)과 **정직한 비커널 경계**(GIST·신경내분비종양 = 유전자-키 → `disease_wp`; 소장 선암 = 이제 §22가 닫음(C1 면역층); 담관암 = 간담도+면역층, circulatory seam) — 경계를 넘지 않고 명시; 그리고 다섯 **Tier-3** 섹션 **§22–§26(v0.9.0–v0.10.0)**을 추가했다 — §22 면역 재발-염증 층(IBD를 자기지속 발적 분지로 읽음: 재발-완화 히스테리시스가 유도≠유지 용량 비대칭을 강제하고, 누적 부담이 §10 커널과 *같은* §7 장벽을 낮춰 대장염 연관 암이 인용 UC 앵커(RR≈2.4)까지 상승하고 완화 시 붕괴 — §21 소장 경계를 닫음; 셀리악은 항원 의존 영역) — 그리고 §23 외분비 자가소화 층(급성 첌장염을 자가촉매 R19 스위치로 읽음: 역치 위 유발은 비가역적으로 **latch**되어 개입은 역치-이전에만 가능; 만성 거울상은 큰-예비능 EPI(~90% 선포 손실 이후에만 지방변) + PERT 구제; CFTR 유전자-키 → `disease_wp`) — §24 관류/혈관 층(관류-생존성 스위치, 편향 h = 관류 − 수요: 만성 장간막 허혈을 수요-구동 여유 붕괴(식후 협심증, 혈관재건이 복원)로, 급성 장간막 허혈/허혈성 대장염을 강제된 생존→허혈 플립과 시간-임계 구제창(= 2·스피노달)으로 읽음; NAFLD/MASLD는 §12 2형 항상성 재사용, 지질-침착 층은 `circulatory` seam) — §25 간담도/담즙 층(핵형성 장벽: 담석증을 준안정 과포화로 읽어 CSI > 1 + 스피노달을 넘어야만 핵형성(Kramers 교차)하고 형성된 결석은 용해 히스테리시스를 보임 — UDCA는 작고 이른 결석에만; 담낭 정체 = §16 B1 게이트 seam, 담낭염 = B1 게이트 + 인용 §22 C1 발적) — 그리고 §26 구조/기계 층(Laplace 벽-역학 스위치: 게실 질환을 P = 장력/반경이 spinodal(g_wall)을 넘으면 탈출하는 것으로 읽음 — 저섬유소 작은 반경이 P를 높이고, 약한 노화/콜라겐 벽이 더 낮게 교차; 섬유소 치료는 기하의 역전 — 큰 반경 + 부드러운 분절이 P를 역치 아래로; 게실염 = 인용 §22 C1 발적, 기계적 고정-차단 폐색 = §14 기능 모듈의 구조적 대응물(외과적, 모델 외)) — 그리고 **§27 교차-시스템 심 와이어링(v0.11.0)**으로 circulatory 간 인터페이스를 vendored 스냅샷으로 소비(§24/§25 전달 기질)하고 mind 느낌-증상 심을 단방향 포인터로 연결(방화벽은 구조적 락으로 강제), **§28 상속 진통 표적 레이어(v0.12.0)**로 형제 백서 `analgesic_threshold_logic` v2.0(DOI 10.5281/zenodo.20733420)의 27개 비-아편 진통 표적을 *이 볼륨 자신의* §18 구심 스피노달 위에서 읽어(drift 0 재유도) 세 약물-클래스 레버로 정렬, IBS·기능성 복통·기능성 소화불량 통증·담도산통·식도 연축 통증에 대한 인용된 약물-클래스 포인터를 제공(임상 크기·느낌 통증은 [O]/`mind`, γ는 STRUCTURE만, 엔진/질환/종양 다이제스트 불변) — 검증된 기반의 섭동으로 현상이 *맞춰지지 않고 창발*하며 넓은 스윈에서 판별을 통과하고(`DZ1–DZ14`·`DZS`(§27)·`DZA`(§28), 레이어 `DZD` 결정론), 각 모듈은 **치료표적 판독**(효과적
치료가 어느 파라미터를 어느 방향으로 움직이는가 + 작동 영역; 절대 효능은 [O])을 함께 싣는다. 남은 질환의
상세 구현 지시는 루트 **`NEXT_INSTRUCTIONS.md`** 에 인수인계로 기록했다. **나머지** 질환(소화불량·역류·운동장애·췌장염·IBD 등)은 루트
**`FUTURE_WORK.md`** 에 **빠짐없이** 티어별로 등록되어 있다 — 각 질환마다 VP-native 기전·판별 타깃·예상
등급·장애물(필요한 새 프리미티브)을 명시하며, 결과로 주장하지 않고 예상 등급만 부여한다. **프로그램이
완료되지 않은 동안에는 남은 로드맵을 산출물과 함께 단일 zip 으로 반환한다**(본 배포의 표준 규칙).
