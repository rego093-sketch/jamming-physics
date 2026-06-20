# 물리백서 v0.9 — 화학·응용 완전 제거 최종 변경내역서 (final)

## 결과
순수 물리 백서로 정리 완료. **46개 섹션**, 게이트 **Phase 1/2/3 PASS**, 패키지 전체 **실제 화학 콘텐츠 0**.
물리 척추(λ_ref 앵커 → a/Δt → α=2/π·δ=1/π² → ν_p=3π⁴ → m_p/m_e=6π⁵ → U_lat → m_H=U_lat/5π → r_p=(2/π)λ_C,p → r_e=D/2π²)는 전부 보존.

## A. 섹션 완전 절제 (3개)
| 섹션 | 정체 | 처리 |
|---|---|---|
| §18 Chemistry / Materials Engineering Extension | 화학장 | 폴더·txt·SVG(phy-18 11개)·manifest·_meta·sections_map·eq_list·허브 TOC 완전 삭제 |
| 부록 J Black-Coated Copper ESS | ESS 응용 공학 부록 | 폴더·txt·SVG(phy-axj 13개)·manifest·_meta·허브 TOC 완전 삭제 |
| 부록 I DOI-anchored Citation Registry | 인용 12행 전부 §18 화학용(Fe-Mo·N2·CO2·해수·P_idx) | 표·폴더·txt·manifest·_meta·허브 TOC 완전 삭제 |

## B. nav 체인 재배선 (절제 후 무손상 연결)
- 번호장: §15 → §12 → ~~§18~~ → §1 → §16  ⇒  §12.next=§1, §1.prev=§12
- 부록: §AXG → §AXH → ~~§AXI~~ → ~~§AXJ~~ → §AXK  ⇒  §AXH.next=§AXK, §AXK.prev=§AXH
- 잔여 제거링크 전 페이지 디링크(§AXL의 AXI 참조 포함)

## C. 본문 내 화학 제거
- **§12**: "Non-evidence: catalytic-turnover coincidence(v35 철회)" 소단원 + 촉매 오염 초록을 html·txt 양쪽에서 제거. 초록은 물리(전자 1초 = ν_e=1 s⁻¹ 내부정합 시계)로 재작성.
- **§15**: "; §18 is an optional extension" 절 삭제.
- **rf**: 본문 범위 "§2–§18" → "§2–§17".
- **§10**: 잉여 `[cite: 110]` 마커 제거(번들 경로는 인라인 유지; 이 토큰은 본래 레지스트리에 행이 없던 항목).
- **수치 원장**(docs/CANONICAL_NUMERIC_LEDGER.md + verification_dossier/NUMERIC_LEDGER.md): 화학행 **T_b/T_m(√2.5)·beta_vac(r_cov 의존)** 삭제. r_e 행은 물리량으로 유지하되 화학 주석("= r_vac, chem scale", "chemistry absolute amplitude scale", "supersedes legacy 4854 fm", "eliminates beta_vac") 전부 제거.
- **_meta.json**: upgrade_note의 "canonical chemistry grounding / Tb/Tm=sqrt(2.5) / r_vac" → 물리만("canonical grounding (r_e), nu_p rounding, r_p residual baselines").

## D. 감사 자취(verification_dossier·reports) 화학 제거 — 물리 검증 내용은 보존
- **삭제**: BETA_VAC_CLOSED.md, BETA_VAC_RESOLUTION.md (화학 beta_vac 전용), PHASE4_CHEMISTRY_ELEVATION.md(앞선 단계에서 삭제).
- **화학 라인 일괄 제거**: SIMULATION_GROUNDING_AUDIT(118→80), GROUNDING_LEDGER(88→77), VERIFICATION_AND_SUPPLEMENTATION_PLAN(180→169), PHASE5_FRONTIER_ROADMAP(64→62), README_STRENGTHENING_PACKAGE(52→50), DOUBT_REMOVAL_MAP(79→76), PHASE1-2_AUDIT_FINDINGS, PHASE3_REPORT — 화학 섹션·게이트(G-CHEM)·Phase4 격상계획·P_idx/r_eff/r_vac/T_b/T_m/CH4 행 제거.
- **빌드로그**: phase2-prefill-physics.csv(§18·axj 행 제거, 51→49), fix_residues.report.json(§18 엔트리 제거).

## E. 유지한 "물리" 용어 (화학 아님 — grep 글자충돌만, 보고용)
- **§17 "R_eff"**: ρ가중 RMS 반경 통계량 `R_eff² = Σ‖x(n)−x_cm‖²ρ / Σρ`. 대규모변동 판단용 운영 통계로 §17 안에서 자체 정의. 화학의 r_eff(전자 진폭)와 전혀 다른 양 → **유지**(원하면 별도 개명 가능, 단 방정식 이미지 phy-17-038.svg 재생성 필요).
- **§03 "chemical/thermal" 구동, §14 "chemical contact forces"**: 연성구동/판데르발스·Casimir 문맥의 표준 물리 어휘 → 유지.
- **§07/§09 "turnover"**: 사건 전환율(canonical event/turnover rate ν_p) → 유지. 촉매 turnover와 무관.

## F. 구조적 영향(허용)
- 번호장이 §17에서 끝남(§18 없음). 부록 문자 **I·J 결번**(§AXH 다음 §AXK). 섹션 제거의 자연스러운 결과.
- 게이트 정합 유지: 섹션수=manifest=디렉터리(46), display_eq=svg, per-page 카운트 일치, 끊긴/고아 내부링크 0.

## G. 게이트
Phase 1/2/3 **PASS**. 섹션 46/46, 위반 없음. _meta totals ≈ {words: 132,890, eq: 7,720, figures: 1, tables: 48}.
