# START HERE — Aging / Senescence (aging_senescence_vp_site)  ·  v1.4.0-writing

> 이 zip을 **새 창에 넣고 이 파일 → CHARTER.md 순서로 읽으면** 상위 백서 없이 바로 연구를 시작할 수 있다.
> 자족적: 기질(FHN/R19), VP-SPEC v1.8 전문, 노드 정체성 γ를 내부에 들고 있다.  **DOI: 10.5281/zenodo.20756155 (Zenodo concept DOI, published; resolves at https://doi.org/10.5281/zenodo.20756155).**

## STATUS (v1.4.0-writing)
v1.4.0 adds the closing chapter **§14 "Conclusion: the genome fixes the ruler, not the lifespan"** (a synthesis of §9/§10/§11 — no new measurement, determinism unchanged) and a complete **LaTeX/PDF** edition (`aging_senescence_vp_whitepaper_v1_4_0.tex` / `.pdf`, 17 pages, all 14 chapters, built by `build_tex.py` from the canonical HTML). Site regenerated to 14 chapters. The rest of this status (v1.3.0) still holds:

Research is **signed off** (all gates green; determinism sha256 `62d5e1eb93db8963…`) and the canonical site is **built** in `docs/` (hub + **13 chapters**). v1.3.0 adds a **telomere deep-dive (RA9)** and an **OBSERVATION-ONLY archaic↔present-day aging-promoter comparison (RA8)**, both with new reproducible engine modules that re-derive γ bit-for-bit from a committed archaic cache (25/25 sequences match). Two new chapters were inserted after the cross-species chapter — **§10 "Archaic and present-day aging promoters"** and **§11 "The telomere keystone: dynamics, not γ"** — and the previous pathology/reproducibility chapters are renumbered **§12/§13**. Headline of the new work: across a cross-sectional set of seven dated genomes (present-day, three Neanderthal, one Denisovan, two ancient modern human), the four aging-master promoter γ values sit in a very narrow band (every per-gene range < 0.0016); the senescence gate (TP53/CDKN2A) reads identically in the dated modern-human genomes; **TERT carries the most archaic promoter substitutions (13)** and its cancer-hotspot positions are invariant — and the canonical telomere repeat γ = **1.3298** is the lowest and most invariant of any aging sequence, locating the telomere as the keystone of aging **dynamics (reservoir length + attrition), not γ**. The **published Zenodo concept DOI `10.5281/zenodo.20756155`** is wired throughout (HTML + PDF), rendered as a resolving link. The carried-forward v1.2.0 confound audit still stands (the §9 null is audited robust; TERT is the residual lead [O]). Masters are **measured + vendored**. For live state and next steps see `HANDOVER.md`; for the full record see `COMPLETION_LEDGER.md` / `CHANGELOG.md`.

## 0. 한 줄 정체
The capstone temporal layer: aging is the slow drift and loss of gain of EVERY homeostatic setpoint, plus the accumulation of cells stuck in pathological R19 attractors (senescence). It is the dominant RISK MULTIPLIER for the oncology/pathology kernels across the whole framework. Sarcopenia, frailty, and multimorbidity are the disease axis.

## 1. 즉시 실행 (연구 시작)
```
python repro/run_all.py
```
→ 측정 γ에서 노드 **창발**(미측정 master는 정직하게 "측정 대상" 보류), 진동자 박동 확인, 스트레스 배터리(발굴된 연구과제)·주요 질환(setpoint 실패) 상태, **집필 잠금 여부** 출력. HTML은 만들지 않는다.

## 2. 범위 (물리적/시간적 클래스)
mind처럼 **시뮬레이션으로 창발하여 순환**시키되, 정체성·발생순서는 DNA 인용(SSOT), 동역학만 추가. 클래스 밖은 형제 소관 — 아래 seam으로만 인용.

| master gene | node | measured γ | role | dyn class |
|---|---|---|---|---|
| TP53 | cellular_senescence | 1.429832 | cells stuck in a pathological R19 attractor (irreversible arrest + SASP) | stuck-attractor |
| CDKN2A | senescence_arrest_switch | 1.442444 | the p16INK4a senescence arrest program (the switch) | stuck-attractor |
| FOXO3 | longevity_signaling | 1.594156 | the insulin/IGF-mTOR-FOXO longevity axis (loop-gain maintenance) | maintenance |
| TERT | telomere_maintenance | 1.553876 | telomere attrition -> the replicative limit (reservoir clock) | reservoir-depletion |
| (systemic_setpoint_drift) | homeostatic_setpoint_drift | —(diffuse) | the slow drift of ALL imported setpoints (cross-package) | integrative-decline |

**상속(IN) — 내부 vendoring + 형제 seam 인용:**
- ALL packages: every defended setpoint this layer watches decline (cited)
- immune: immunosenescence raises oncology crossing (seam)
- DNA: the gene-clock life_course baseline (cited)
- substrate: FHN/R19 (vendored)

**경계(OUT):**
- aging RISK MULTIPLIER -> every oncology + pathology kernel (cross-cutting time axis; raises crossing rates)

## 3. 판별 타깃 (발굴된 연구과제 — CHARTER에 전체 프로그램)
- **RA1** setpoint drift: each setpoint (glucose/pressure/Ca/temperature) loses defense gain over time -> the defended value drifts (the unifying aging signature) [V]
- **RA2** senescence as stuck attractor: a cell crosses into an irreversible arrested R19 basin (cannot return; SASP); accumulation over time [V]
- **RA3** reservoir/stem depletion: the DWELL ~ gamma^1.5 reservoir is finite; stem exhaustion = depletion (telomere/TERT clock) [V]/[O]
- **RA4** hallmarks mapping: map the hallmarks of aging to substrate phenomena (R19 errors, stuck attractors, depletion, gain loss) [V]/[O]
- **RA5** risk multiplier: aging raises the crossing rate of EVERY oncology/pathology kernel (accumulated crossings + immunosenescence) -- the steep age-incidence slope [V], absolute [O]
- **RA6** rate of aging: one rate parameter (biological vs chronological age) or per-system rates? [V]/[O]

## 4. 주요 질환 (이 패키지가 다루는 비-희귀 질환)
질병 = 방어 setpoint/시계/감각기관의 실패(loop-gain 하락 / setpoint 표류 / attractor-shift / 기기 실패), 발암과 동일한 R19 기질. 위치: `repro/_pathology/`. **희귀·단일유전자 질환은 disease_wp 소관 — 여기선 교차참조만** 하고 파라미터로 합성한다.
- **sarcopenia** ← age-related muscle decline (cross-ref musculoskeletal) -> loss of actuator capacity  · decline rate vs cited age [L]; cross-loop [V]
- **frailty / multimorbidity** ← co-decline of multiple setpoints crossing a function threshold  · multi-setpoint co-failure [V]; cited [L]
- **aging as the cancer risk multiplier** ← accumulated R19 barrier-crossings + immunosenescence raise ALL-site incidence  · the steep age-incidence curve vs cited [L]; crossing accumulation [V]; absolute [O]
- **(progeroid syndromes -> disease_wp)** ← monogenic accelerated aging is rare/genetic  · cross-ref disease_wp; here only as a rate parameter

## 5. 절대 규칙 — 연구 먼저, 집필 나중
**엄격한 연구(많은 스트레스 실험) 완료 전 집필 금지.** `tools/build_docs.py`는 잠금 동안 거부. 해제: ① `research_gate()` all_green ② `write_research_complete()` ③ `PHASE=writing`.

## 6. 집필 규칙 (VP-SPEC v1.8 — 루트 `VP_SPEC_v1_8.md`)
정본 HTML(C2) · 제목별 별도 SEO HTML(C4: answer-first·JSON-LD·claim-strip·vp-card) · 본문 영어(C0) · 정량 결정론 재생성(C1) · 모든 [O] 사유 명시(C3). **DOI 발행 완료 — 10.5281/zenodo.20756155 (Zenodo concept DOI; https://doi.org/10.5281/zenodo.20756155).**. 출력: `docs/<slug>/index.html` + 허브 + sitemap/robots/llms.

## 7. 인수인계 (자동)
새 창은 이 파일 → `CHARTER.md`(연구 프로그램 전체)만 읽으면 범위·이음매·연구과제·질환·게이트·집필규칙·DOI상태를 전부 파악한다. 상태는 파일로만 전달, 종료 시 단일 zip으로 다음 세션에. 반환은 압축파일 1개(파편화 금지, C0).
