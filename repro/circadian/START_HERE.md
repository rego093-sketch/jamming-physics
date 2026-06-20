# START HERE — Chronobiology (Circadian) (circadian_vp_site)  ·  v0.1.0-research

> 이 zip을 **새 창에 넣고 이 파일 → CHARTER.md 순서로 읽으면** 상위 백서 없이 바로 연구를 시작할 수 있다.
> 자족적: 기질(FHN/R19), VP-SPEC v1.8 전문, 노드 정체성 γ를 내부에 들고 있다.  **DOI: 10.5281/zenodo.20755413 (concept; 최신 버전으로 해상) · v0.2.0 스냅샷 10.5281/zenodo.20755414 · CC BY 4.0. `registry/cross_volume_doi.{csv,md}`에 등록 + 사이트 전반 배선 완료(v0.3.0).**

## 0. 한 줄 정체
The ~24h circadian clock is a self-sustained coupled limit-cycle oscillator network (SCN master + peripheral clocks) on the FHN substrate; it free-runs, entrains to light, and GATES nearly every homeostatic setpoint. Clock-environment misalignment (shift work, jet lag) is the disease axis.

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py
```
→ 측정 γ에서 노드 **창발**(미측정 master는 정직하게 "측정 대상" 보류), 진동자 박동 확인, 일주기 entrainment probe, 스트레스 배터리(발굴된 연구과제)·주요 질환(setpoint 실패) 상태, **집필 잠금 여부** 출력. HTML은 만들지 않는다.

## 2. 범위 (물리적/시간적 클래스)
mind처럼 **시뮬레이션으로 창발하여 순환**시키되, 정체성·발생순서는 DNA 인용(SSOT), 동역학만 추가. 클래스 밖은 형제 소관 — 아래 seam으로만 인용.

| master gene | node | measured γ | role | dyn class |
|---|---|---|---|---|
| (SCN_master_clock) | scn_master_oscillator | —(diffuse) | suprachiasmatic ~24h master limit-cycle (light-entrained) | oscillator |
| BMAL1 | core_clock_loop | TO-MEASURE | BMAL1/CLOCK<->PER/CRY transcription-translation feedback loop (the molecular oscillator) | oscillator |
| (peripheral_clocks) | peripheral_clock_network | —(diffuse) | liver/muscle/adipose peripheral clocks (cite organ packages) | coupled-oscillator |
| (retinal_entrainment) | light_entrainment_input | —(diffuse) | retinal light -> SCN phase reset (seam to sensory/neuro) | entrainment |

**상속(IN) — 내부 vendoring + 형제 seam 인용:**
- sensory/neuro: retinal light input -> phase reset (cited)
- ALL homeostasis + organ packages: the clock GATES their setpoints (cited, cross-cutting)
- DNA: node identity + emergence order [V]
- substrate: FHN/R19 (vendored)

**경계(OUT):**
- circadian phase / gating signal -> thermometabolic, hemodynamic, ionic, immune, ... (this pkg is SSOT for phase/timing)

## 3. 판별 타깃 (발굴된 연구과제 — CHARTER에 전체 프로그램)
- **RC1** free-running clock: the molecular TTFL self-sustains a ~24h rhythm with zero external drive (FHN limit cycle) [V], period [L]
- **RC2** entrainment: a light pulse shifts phase per a phase-response curve; the clock locks to the 24h light cycle (entrainment probe) [V]
- **RC3** master vs network: one SCN master oscillator vs a coupled SCN+peripheral network (coupling strength vs drift) [V]
- **RC4** setpoint gating: the clock imposes a daily rhythm on thermometabolic/hemodynamic/ionic setpoints (cross-cutting) [V]
- **RC5** misalignment: internal-clock vs external-time decoupling (shift work/jet lag) produces the disease state [V]

## 4. 주요 질환 (이 패키지가 다루는 비-희귀 질환)
질병 = 방어 setpoint/시계/감각기관의 실패(loop-gain 하락 / setpoint 표류 / attractor-shift / 기기 실패), 발암과 동일한 R19 기질. 위치: `repro/_pathology/`. **희귀·단일유전자 질환은 disease_wp 소관 — 여기선 교차참조만** 하고 파라미터로 합성한다.
- **circadian rhythm sleep-wake disorders** ← delayed/advanced sleep phase, non-24h, shift-work disorder, jet lag = clock<->environment misalignment  · misalignment vs cited chronotype data [L]; phase-decoupling [V]; sleep/affect cross-ref to mind/neuro
- **shift-work metabolic & cardiovascular risk** ← chronic clock disruption dysregulates the gated metabolic + pressure setpoints (seam)  · RR vs shift-work exposure [L]; cross-loop disruption [V]; absolute [O]
- **shift-work cancer risk** ← IARC class 2A: circadian disruption raises the crossing rate (clock-gated + immune)  · RR vs night-shift years (IARC anchor) [L]; clock-gated crossing [V]; ties to the oncology kernel

## 5. 절대 규칙 — 연구 먼저, 집필 나중
**엄격한 연구(많은 스트레스 실험) 완료 전 집필 금지.** `tools/build_docs.py`는 잠금 동안 거부. 해제: ① `research_gate()` all_green ② `write_research_complete()` ③ `PHASE=writing`.

## 6. 집필 규칙 (VP-SPEC v1.8 — 루트 `VP_SPEC_v1_8.md`)
정본 HTML(C2) · 제목별 별도 SEO HTML(C4: answer-first·JSON-LD·claim-strip·vp-card) · 본문 영어(C0) · 정량 결정론 재생성(C1) · 모든 [O] 사유 명시(C3). **DOI 배정 완료 — 10.5281/zenodo.20755413 (concept) 사이트 전반 배선(JSON-LD identifier/sameAs, claim-strip 스냅샷, Highwire citation 태그) + `registry/cross_volume_doi` 등록.** 출력: `docs/<slug>/index.html` + 허브 + sitemap/robots/llms.

## 7. 인수인계 (자동)
새 창은 이 파일 → `CHARTER.md`(연구 프로그램 전체)만 읽으면 범위·이음매·연구과제·질환·게이트·집필규칙·DOI상태를 전부 파악한다. 상태는 파일로만 전달, 종료 시 단일 zip으로 다음 세션에. 반환은 압축파일 1개(파편화 금지, C0).
