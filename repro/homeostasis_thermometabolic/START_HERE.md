# START HERE — Thermometabolic Homeostasis (homeostasis_thermometabolic_vp_site)  ·  v0.6.0

> **v0.6.0 status (site landed).** Research is signed off and the canonical multi-page site is built.
> **Concept DOI: [10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934)** (CC BY 4.0).
> PDK4 (torpor fuel-switch) is **measured** (γ=1.4112, NC_000007.14) and an 8-gene × 14-species torpor/BAT
> panel (107 cells) is vendored (unchanged since v0.3.0). The 16-target stress battery is **all PASS** ([V], or [O]
> with a stated obstacle for RT5 Kleiber, RH8 the γ-panel NULL, and RH9 the methylation-substrate NULL per the
> CHARTER bar); the engine is deterministic (2×sha256 identical, engine sha `08f50d6d…`) and re-derives the
> cross-species reads offline bit-for-bit. The restoration three-lever module (from the analgesic
> technology) passes its S3-honesty / forbidden-claim / falsification gates. **v0.6.0 adds the precision-routing
> layer** — the analgesic local-anaesthesia mirror: each restoration target is placed on a CITED compartment map
> and classed PRECISION / REGIONAL / SYSTEMIC (split 2/5/2; UCP1→BAT and MC4R→hypothalamus are the clean
> precision routes; INSR and TNF are honestly SYSTEMIC), keeping routability ([F] cited anatomy) distinct from
> deliverability ([O] BBB / BAT depot / no-single-locus). Its firewall is **PROVEN**: `gamma_independence_gate()`
> recomputes the whole map under a perturbed γ atlas and the routing geometry is byte-identical (routing sha
> `21021e79…`). The engine is **unchanged** (surfaced in `run_all.py`, not `circulate()`). Read `repro/run_all.py`
> output, then the site at `docs/thermometabolic/` (1 hub + 32 chapters; site sha `3bb5657b…`).
>
> 이 zip을 **새 창에 넣고 이 파일 → CHARTER.md 순서로 읽으면** 상위 백서 없이 바로 연구를 시작할 수 있다.
> 자족적: 기질(FHN/R19), VP-SPEC v1.8 전문, 노드 정체성 γ를 내부에 들고 있다.

## 0. 한 줄 정체
Starts from the endotherm-vs-ectotherm question -- does the organism DEFEND an internal setpoint or TRACK the environment? -- and covers thermoregulation, brown-fat thermogenesis, the torpor/hibernation switch, whole-body energy homeostasis, and metabolic disease as ONE coupled setpoint-dynamics problem. Disease is a subset.

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py
```
→ 측정 γ에서 노드 **창발**(미측정 master는 정직하게 "측정 대상" 보류), 진동자 박동 확인, **겨울잠 스위치 probe**(중심 질문 RH1), 스트레스 배터리(발굴된 연구과제)·질병(setpoint 실패) 상태, **집필 잠금 여부** 출력. HTML은 만들지 않는다.

## 2. 범위 — 질병이 아니라 **근본 메커니즘부터**
이 패키지는 **항온(endothermy) vs 변온(ectothermy)** — 생물이 내부 setpoint를 *방어*하는가 아니면 환경을 *추종*하는가 — 라는 질문에서 시작한다. 체온조절·갈색지방 열생성·**겨울잠(torpor) 스위치**·전신 에너지 항상성·대사질환을 하나의 결합된 *setpoint 동역학* 문제로 다룬다. **질병은 마지막 층(SUBSET)이지 출발점이 아니다.**

mind처럼 **시뮬레이션으로 창발하여 순환**시키되, 이 패키지의 1차 객체는 장기가 아니라 **루프·setpoint·스위치**다. 정체성·발생순서는 DNA 인용(SSOT), 동역학만 추가.

| master gene | node | measured γ | role | dyn class |
|---|---|---|---|---|
| UCP1 | brown_adipose_thermogenesis | 1.4054 | uncoupled proton leak = heat, not ATP (the endotherm furnace) | thermogenic-switch |
| ADRB3 | sympathetic_thermo_drive | 1.4462 | beta3-adrenergic activation of BAT (cold -> heat command) | effector |
| PPARG | white_adipose_storage | 1.3902 | lipid storage + adipokine secretion (the lipostat storage node) | storage |
| MC4R | melanocortin_appetite | 1.272 | hypothalamic energy-balance setpoint (intake control) | setpoint-loop |
| LEPR | leptin_feedback | 1.4554 | adiposity feedback signal (storage -> brain) | feedback |
| INSR | insulin_glucose_effector | 1.4956 | insulin-mediated glucose disposal (the euglycemia effector) | feedback |
| GHRL | ghrelin_hunger | 1.355 | gut hunger signal (drives intake; opposes leptin) | feedback |
| PDK4 | torpor_fuel_switch | TO-MEASURE | metabolic fuel-switch to lipid + glucose sparing (torpor-associated program) | torpor-switch |
| (hypothalamic_thermostat) | preoptic_thermostat | —(diffuse) | preoptic setpoint comparator (the thermostat itself; circuit, no single master) | setpoint-comparator |
| (torpor_arousal_cycle) | torpor_arousal_rhythm | —(diffuse) | periodic interbout arousal during hibernation (slow relaxation oscillator) | oscillator |

**상속(IN) — 내부 vendoring + 형제 seam 인용:**
- digestive: pancreas-liver glucose homeostat CORE (cited, SSOT) -- this pkg closes the whole-body loop
- musculoskeletal: insulin-mediated glucose disposal arm (cited)
- integumentary + circulatory: heat-dissipation arm (vasodilation/sweat, cited)
- immune: pyrogen drive for fever (cited)
- mind: brain appetite/arousal edge (cross-referenced, not re-emerged)
- DNA: node identity (obesity_gamma masters) + emergence order [V]
- substrate: FHN/R19 (vendored)

**경계(OUT):**
- defended core temperature + metabolic rate (systemic; this pkg is SSOT for the thermal/energy setpoints)
- MAP coupling note -> homeostasis_hemodynamic (metabolic syndrome cluster)
- monogenic metabolic lesions <-> disease_wp (parameter in / trajectory out)

## 3. 판별 타깃 (발굴된 연구과제 — CHARTER에 전체 프로그램)
- **RT1** setpoint-defend vs track: under an ambient sweep, core temp stays pinned (homeotherm) vs follows ambient (poikilotherm) [V]
- **RT2** thermostat: an ambient step is corrected to setpoint ~37C with cited gain/latency [V], setpoint [L]
- **RT3** endothermy cost: BMR needed to defend setpoint vs cited heat-loss; thermal-stability/energy trade-off [V], abs [O]
- **RT4** continuum vs discrete: R19 spinodal between endotherm/ectotherm regimes vs smooth gradient (cited species data) [V]
- **RT5** Kleiber: metabolic rate ~ mass^(3/4) exponent reproduced [V] or flagged [O]
- **RG1** BAT thermogenesis: cold step recruits UCP1 to defend setpoint; rate matches cited BAT output [V]
- **RG3** fever: a regulated UPWARD setpoint shift (immune pyrogen), distinct from hyperthermia (defense overwhelmed) [V]
- **RH1** torpor switch: euthermia<->torpor shows hysteresis/discontinuity (bistable SWITCH) vs smooth dial -- torpor_switch_probe [V]
- **RH2** torpor is regulated: a perturbation below the low torpor setpoint is actively corrected [V]
- **RH4** bear vs human: torpor-program genes present-but-silenced in human genome vs absent (cross-species) [V]/[O]
- **RH6** arousal rhythm: interbout arousal as a slow FHN oscillator; period (days) [L]
- **RH8** torpor panel: across 8 fuel-switch/BAT genes × 14 species, NO promoter γ marks hibernation; group gaps ARE GC gaps (cross-gene r=0.9957) [V]/[O]
- **RH9** methylation substrate: a GC-normalized CpG-O/E read of the same 8 genes ALSO fails to separate hibernators (0/8); CpG O/E is a distinct read from γ (r=0.5601) and far less GC-loaded (0.4927 vs 0.9955) — a SECOND static layer is blind to hibernation; dynamic regulation [O] external [V]/[O]
- **RE1** glucose homeostat: a glucose load returns to ~5 mM via the whole-body closed loop [V], setpoint [L]
- **RE2** lipostat: a defended adiposity setpoint opposes chronic over/underfeeding (leptin-melanocortin) [V]
- **RD4** hibernation bridge: insulin resistance as an uncoupled, chronic misfire of a torpor-like fuel-sparing program [V]/[O]

## 4. 질병 — 이 시스템의 일부 (setpoint 실패)
질병 = 국소 병변이 아니라 **방어되던 setpoint의 실패**(loop-gain 하락 / setpoint 표류 / attractor-shift). 발암 모듈과 같은 R19 기질: 건강 setpoint = 조절된 attractor, 질병 = 병적 basin으로의 교차. 위치: `repro/_pathology/`. disease_wp(단일유전자 병변)와는 *합성*된다 — 유전자 병변 = 루프 파라미터 입력, 전신 궤적 = 여기서 계산.
- **type 2 diabetes** ← insulin resistance -> glucose-loop gain drop -> hyperglycemic attractor  · RR / progression vs cited risk (BMI, HbA1c cohorts) [L]; attractor-shift shape [V]; absolute incidence [O]
- **obesity** ← leptin resistance -> lipostat setpoint drifts up -> defended at higher adiposity  · defended-setpoint drift vs cited energy-balance data [L]; shape [V]; absolute [O]
- **metabolic syndrome** ← co-failure of coupled glucose+lipid+pressure loops (shared upstream node)  · cluster co-movement vs cited prevalence [L]; multi-loop [V]; absolute [O]
- **(MODY / monogenic, via disease_wp)** ← gene lesion = a loop PARAMETER perturbation; trajectory computed here  · parameter from disease_wp [cited]; systemic trajectory [V]

## 5. 절대 규칙 — 연구 먼저, 집필 나중
**매우 높은 수준의 엄격한 연구(많은 스트레스 실험) 완료 전에는 집필 금지.** `tools/build_docs.py`는 잠금 동안 거부. 해제: ① `research_gate()` all_green ② `write_research_complete()` ③ `PHASE=writing`.

## 6. 집필 규칙 (VP-SPEC v1.8 — 루트 `VP_SPEC_v1_8.md`)
정본 HTML(C2) · 제목별 별도 SEO HTML(C4: answer-first·JSON-LD·claim-strip·vp-card) · 본문 영어(C0) · 정량 결정론 재생성(C1) · 모든 [O] 사유 명시(C3). 출력: `docs/<slug>/index.html` + 허브 + sitemap/robots/llms.

## 7. 인수인계 (자동)
새 창은 이 파일 → `CHARTER.md`(연구 프로그램 전체)만 읽으면 범위·이음매·연구과제·질병·게이트·집필규칙을 전부 파악한다. 상태는 파일로만 전달, 종료 시 단일 zip으로 다음 세션에. 반환은 압축파일 1개(파편화 금지, C0).
