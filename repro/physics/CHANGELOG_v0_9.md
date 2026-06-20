# CHANGELOG v0.8 → v0.9 (검증 반영 업그레이드)

본 릴리스는 다회차 검증·연구의 결과를 백서에 반영한 것이다. 모든 변경은 LOCK→Derive→Gate 규율 하의 **버전 범프**(new lock_id + manifest 갱신 + 재게이트)로 적용됐고, **게이트 phase 1/2/3 전부 PASS**로 검증됐다. No-Tuning 불변 유지(잔차를 닫으려 [F] 계수를 이동한 곳 0).

new lock_id: `vp_physics_v0_9_verified` (supersedes v0.8 sealed tree). src 무결성: 본 트리는 v0.8 파생 산출물의 버전 후속본이며, 변경은 아래에 전수 기록됨.

---

## 1. 화학 절대 스케일의 정준 grounding (핵심 — β_vac 닫힘)

근거: `verification_dossier/BETA_VAC_CLOSED.md`, `BETA_VAC_RESOLUTION.md` (v0.2 + DOI 번들 교차분석).

**문제(v0.8 내부 불일치)**: 18장이 r_vac을 §18.2.2에서 4854 fm(=D)로, §18.2.5에서 r_cov·K·β_vac(=246 fm)로 써서 ~20×(=2π²) 어긋났고, β_vac=1.088이 ungrounded 입력이었다.

**해결(정준식, 발명 아님 — 이론 W.2 원장 그대로)**:
- §18.2.2: r_vac을 **정준 전자 회전 반지름 r_e = (D_anch/2)·δ = D_anch/(2π²) = 245.84 fm** 로 교정. n겹 법칙 n=1의 r_1=r_0·δ (r_0=D_anch/2=λ_C,e), 2π²=2·s_e(전자 시도율). 이미 G-RE 게이트로 grounded.
- §18.2.3 표: 원자 진폭을 1/(2π²)로 재스케일 (H 4854→245.8, C 2623→132.9, N 2017→102.2, O 1674→84.8, Fe 1138→57.7, U 817→41.4 fm).
- §18.2.5: β_vac=1.088은 독립 입력이 아니라 r_cov·K cross-check 경로가 r_e를 재현하는 **유도 잔차(≈1.087)**임을 명시. 두 경로 0.1% 수렴(다층증명).

**효과**: 화학 절대 스케일이 다른 모든 것과 같은 canon(전자 반지름, D 재밍 grounded + δ 강제 + 전자 1초 구조)에 닫힘. 별도 화학 입력 0. 차원 없는 예측(√2·P_idx)은 스케일 무관이므로 영향 없음. √2 검증은 관측 진폭의 비율이라 무영향.

## 2. T_b/T_m 기하상수 정정 (1.6 → √2.5)

근거: `verification_dossier/SIMULATION_GROUNDING_AUDIT.md` (DOI 번들 G-CHEM-TB-TM-RATIO, `sqrt2p5` 잠금).

- 18장의 T_b/T_m "≈ 1.6"을 grounded 값 **√2.5 ≈ 1.5811**로 정정(전 등장). 번들 게이트가 1.58로 PASS하며 잠금 상수가 √2.5임을 확인. "1.6"은 느슨한 반올림이었다.

## 3. ν_p 길이경로 교차검증값 반올림 통일

근거: `verification_dossier/PHASE1-2_AUDIT_FINDINGS.md` (발견 B), `NUMERIC_LEDGER.md`.

- 292.244(절단)를 정준 **292.245**(=292.245156 반올림)로 통일. 영향 페이지: 09, axf, vh, w0. (정준 ν_p=3π⁴=292.227과 별개의 [V] 교차검증값임은 유지.)

## 4. r_p 잔차 기준선 명시

근거: `PHASE1-2_AUDIT_FINDINGS.md` (발견 A — FAIL), `NUMERIC_LEDGER.md`.

- "−0.018%"에 기준선 **vs CODATA 0.8414 fm** 명시(01, 13장). ("+61 ppm"은 이미 "cross-check"로 맥락화돼 있어 유지.) 세 잔차(예측 vs 잠금 +61 ppm, 예측 vs CODATA −0.018%, 잠금 vs CODATA −0.024%)가 기준선과 함께 정합.

---

## 5. 검증 도시에 동봉 (`verification_dossier/`) — 누락 없는 연구 반영

전체 검증·연구 산출물 18종을 동봉:
- **계획·감사**: VERIFICATION_AND_SUPPLEMENTATION_PLAN, PHASE1-2_AUDIT_FINDINGS, PHASE3_REPORT, numeric-consistency-audit.json, xref-headroom.json, PHASE1_PATCH_SPEC.
- **정준 원장(SSOT)**: NUMERIC_LEDGER.md, numeric_ledger.json (각 양의 정준값 + 기준선 명시 잔차). `docs/CANONICAL_NUMERIC_LEDGER.md`에도 배치.
- **이해도/혼란 제거**: DOUBT_REMOVAL_MAP(7개 의심 유도 해소), FORCED_CHAIN_MAP(빛→질량 단방향 의존성), MULTILAYER_PROOF_MAP(다양한 수치=교차검증), README_STRENGTHENING_PACKAGE(단일 진입 안내).
- **시뮬 근거**: SIMULATION_GROUNDING_AUDIT, GROUNDING_LEDGER(모든 v0.8 숫자→번들 게이트/연구 매핑).
- **화학 격상**: PHASE4_CHEMISTRY_ELEVATION(예측·촉매 도구 설계), PHASE5_FRONTIER_ROADMAP.
- **β_vac 닫힘**: BETA_VAC_CLOSED, BETA_VAC_RESOLUTION.

---

## 6. 게이트 검증 (모두 PASS)

```
gate.py --phase 1 physics: PASS
gate.py --phase 2 physics: PASS
gate.py --phase 3 physics: PASS
```
manifest: 18장 단어수 4032→4142 갱신(정준 교정 +110단어). 그 외 편집은 ±0.5% 내. eq/그림/표 카운트·링크 해소·고아·sitemap 패리티 전부 PASS.

## 7. 적용하지 않은 것 (정직한 경계)

- **교차참조 xref 승격(bare 422건)**: 변환층 작업으로 §→앵커 매핑표가 필요. 결정론 toolchain(remediation/inject_xrefs)에서 매핑 가능분 처리 권고. 단어수 중립이라 안전.
- **끊긴 수식 참조 5건**(다의적): 인과적으로 일의적이지 않아 silent 재연결 시 오염 위험 → 공동 추론 대상(상세 PHASE1_PATCH_SPEC B1). 확신도 높음 1건(S09_04_delta_def→S09_03_delta_def)은 toolchain에서 적용 가능.
- **화학 예측 격상 실제 구현**(사전등록·G-CHEM-PRED 게이트·candidate-committed 티어): 설계 완료(PHASE4), 소스/툴 레인 구현 대기.
- **[O] 프런티어**(절대 g·α_em): 정직하게 열린 채 유지. n겹 법칙은 이미 [F](유일 잔여는 [MAP] 정의적 매핑).

이 항목들은 누락이 아니라 **결정론 toolchain 또는 공동 추론이 필요한 것**으로 명시 기록됨. 본 릴리스는 혼자 검증 가능한 모든 교정을 반영하고 게이트로 봉인했다.

---

## 요약

v0.9는 (1) 화학 절대 스케일을 정준 전자 반지름에 grounding하여 β_vac을 닫고, (2) T_b/T_m을 √2.5로, (3) ν_p를 292.245로, (4) r_p 잔차에 기준선을 명시했으며, (5) 전체 검증 도시에를 동봉했다. 모든 변경은 게이트 PASS로 검증됐고 No-Tuning을 보존한다. 이론은 바뀌지 않았다 — 흩어졌던 정합성과 grounding이 드러나고 닫혔을 뿐이다.
