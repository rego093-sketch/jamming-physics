# HANDOVER — VP 잼밍 척추 단원 병합 (.tex) + 교차링크 + 옛문서 수정
### 작성 2026-06-05. 다음(새) 세션이 *실행*할 작업의 완전 인수인계서.
### 결정: 병합은 새 세션에서. 이유: 지적 핵심(.md 척추)은 완료, 남은 건 섬세·대용량 .tex 작업이라
###       거의 찬 세션에서 시작 시 백서가 반쯤 병합된 깨진 상태로 남을 위험이 큼.

---

## 0. WORKING CONTRACT (먼저 읽어라)
- **언어: 한국어.** 사용자(독립연구자, Daegu; ORCID 0009-0002-7535-8245; rego093@naver.com).
- 스타일: 간결, **판단 중심**. 검증보다 **정직한 오류 인정** 우선. **긍정 날조 금지.** 부정도 보고.
- 주장 등급: **[F]**act(증명/측정) · **[H]**ypothesis · **[V]**erification(시뮬) · **[D]**efinition(정의에 기댐).
- **LOCK → derive → Gate.** 목표에 맞춰 튜닝 금지. 짧은 확인("1","계속","해라")=진행.
- 영속: `/mnt/user-data/outputs/`만 남음. `/home/claude`는 세션 간 초기화.
- **수비학·과장 혐오**(사용자 명시). 합치되 "증명 완료"로 부풀리지 말 것 — 상태 원장을 같이 박아야 함.

---

## 1. 절대 틀리면 안 되는 사실 (이전 세션이 한 번 틀렸음 — 반드시 지킬 것)

### ★ 양성자(PROTON) ≠ 양자(QUANTUM) ★
| | 양성자 | 양자 |
|---|---|---|
| 크기 | **r_p = 0.84 fm** (10⁻¹⁵) | **D = 4.85 pm** (10⁻¹²) |
| 출처 | 강성껍질 균형 r⁻⁵/r⁻⁴ → x*=2/π=r_p/λ_Cp; 그라인더 82-cell(z=6=2d) | **파장식** D=2πλ/A (= 2λ_Ce) |
| 상수 | **ν_p=3π⁴**, m_p/m_e=6π⁵ | — |
| 관계 | — | **D = 6π⁶·r_p = π·(m_p/m_e)·r_p** |
- 항등식: D/r_p = (2λ_Ce)/((2/π)λ_Cp) = π·(λ_Ce/λ_Cp) = π·(m_p/m_e) = 6π⁶ = 5768.
- **파장식 = 양자 지름. 강성균형/그라인더 = 양성자. 절대 "같은 원"이라 하지 말 것.**

### 검증된 숫자(반올림 주의, 그대로 인용 가능)
- c²/a²|_{z=6} = **0.107** (N=256:0.108, N=512:0.107; affine z/2d²=z/36=0.167의 **0.65배**).
- B_relaxed@z=6 = 0.76(N256)/0.95(N512) **유한**; G_relaxed@z=6 = 0.009/−0.0005 **→0**. Born=FD 4.7e-7.
- 강제 원: 유일 양의 고정점 **x*=2/π=0.6366**, F'(x*)=**−9.56**(<0, 안정), 전역 끌개. r_p=(2/π)·1.32141fm=**0.8412 fm**.
- 그라인더: N 3000→301, 코어(r<√6) **~79–81 ≈ 82**, z_core≈8.9(조밀/비정질). Ω스윕 R_rms 3.48→2.98(Ω 0.04→0.24). `x*∝1/Ω`.
- 빛창발: A=a_med/g\* **순수 격자**(물리상수 0; 선택값 g0=2e-7만). bundle A_med=**8.01×10⁵**(내 독립 재현 6.9×10⁵; g\*/g0≈1.14–1.28). a_med≈0.183(L=1). a_phys=λ/A=**0.79 pm**. D=2π·a_phys=ℓ_rot 중앙값 **4.96 pm**, best avalanche **4.854 pm**. 정확히 4.85 주는 A=8.20×10⁵(중앙값보다 2.2%↑ ⇒ ℓ_rot **+2.3%**).
- 정수 코어: **#{r²≤6}=81=3⁴** (3D), **21**(2D); 코어 82=81+1.
- 상수: α=2/π=⟨|cosθ|⟩(2D 정류, 3D=1/2). δ=1/π²=(⟨[cosθ]₊⟩=1/π)². 2π=α/δ=6.2832. ν_p=3π⁴=292.227. m_p/m_e=6π⁵=1836.118(CODATA 1836.153, −19ppm). 6π⁶=5768.3.

### 핵심 평결(정직)
- 척추 *역학*(무한→c²→파장→강제반경; 단일속도; 회전이 크기 창발)은 **증명·검증됨**.
- 수비학 혐의는 **한 점으로 환원**: `[MAP-1]`("섹터간 위상 lock 1개 = π²=1/δ", §8.0.6). 3π⁴(거의 증명급)·6π⁵·6π⁶이 전부 이 *하나의 정의*에 매달림(α·δ와 동일 지위).
- 6π⁶은 독립 상수 아님 = π·6π⁵(질량비 변장). **억지로 새 유도 만들지 말 것.**

---

## 2. 이번 작업(병합)의 목표 — 정확히
1. **새 단원 1개**를 백서에 추가: "잼밍 척추(Jamming Spine)" — 흩어진 줄기를 한자리에 모으고
   각 단계에 [F]/[D]/[A]/[V] 딱지 + 상태 원장. 내용 원본 = `VP_jamming_spine_DRAFT.md`(5부).
2. **기존 절들에 한 줄 교차링크**: §5(α,δ), §6.2(r_p), §8.0/8.0.5(C₃·n-fold), §8.5/8.5.0(그라인더·회전언잼),
   §10.3(증폭 A), §10.9(빛각), §11.6(c²=K) → "척추 개관은 본 단원 §X 참조".
3. **옛 문서 2개 수정**(아래 §6): 양성자=양자 "같은 원" 오류 제거.
4. **재컴파일**(draftmode 먼저) → PDF 확인. (선택) 번들 재봉인은 사용자 승인 시에만.
- **LOCK 규율**: 새 단원은 [V] 기록(기존 LOCK 값 불변). \WPVersion 버전업. 기존 결론 변경 금지.

---

## 3. 입력 파일 지도 (전부 확인)
- 백서(read-only): `/mnt/user-data/uploads/vp_whitepaper_v0_4.tex` — 21,069줄, 내부 \WPVersion=**v0.3.0 (Integrated Edition)**.
- **척추 초안(병합 원본)**: `/mnt/user-data/outputs/VP_jamming_spine_DRAFT.md` ← 이게 새 단원의 살.
- 상세 사슬(참고, 단 양성자/양자 오류 있음): `/mnt/user-data/outputs/VP_theory_chain_stiffness_to_D.md`, `VP_inevitability_chain.md`.
- 번들: `/mnt/user-data/uploads/AQD_DOI_bundle_unified_v0_3_0__1_.zip` (압축풀면 `AQD_DOI_bundle_unified_v0.3.0_logic_DOI17932567/`).
- **이번 세션 검증 산출물(증거, /outputs):**
  - `bulk_c2_validated/` (bulk.py, relaxed_shear.py, bulk_run.py, results_bulk/bulkG.csv, bulk_modulus_c2.png) — S3–S4.
  - `forced_circle/` (fig_circle.py, forced_circle_attractor.png) — §4.1 강제반경.
  - `rotating_quantum/` (vp_grinder_3d.py, grind_sweep.py, rotating_quantum.png) — 회전 그라인더 + x*∼1/Ω.
  - `lattice_to_485pm/` (make_ellrot_fig.py, ellrot_485pm.png, soc_indep_avalanches.csv) — D=2πλ/A.
  - `relaxedG_validated/` (relaxed_shear.py, le_shear.py, aqs.py, results/, FINDINGS, 그림 5개) — 전단 G→0, ω*, 흐름, AQS.
- 전사(긴 대화 원본): `/mnt/transcripts/2026-06-05-05-29-54-vp_jamming_relaxedg_session.txt` (필요시 read로 부분 조회).
- 번들 핵심 스크립트(읽어둘 것):
  - `.../legacy_bundle/jamming_rotation_485pm_study.py` — D=2πλ/A, ℓ_rot 정의(광주기=A 미시스텝).
  - `.../code/soc_percolation_pinning.py` — A=a_med/g\* (g_star_exact: gap=max(dist−2R,0) 이진탐색, far_fraction 0.8; g0=2e-7, k_nn=12, N=200).
  - `.../jamming_rotation_verification_v0.3/modules/proton_formation_3d.py` — 회전 그라인더(역회전 반구, 수축, 밀도1, 소멸).
  - `.../modules/wavelength_jamming.py` — c²=B_eff/ρ_eff (내 bulk가 재현).

---

## 4. 척추 단원 내용 (5부 — `VP_jamming_spine_DRAFT.md` 그대로, .tex로 옮길 것)
0. **한눈에**: 줄기 박스 + 이번 세션 [V] 4개.
1. **양성자 vs 양자** 못박기(§1 표).
2. **무한강성 → c²** 단계별 S1–S4 (S2 SOC, S3 Maxwell 한계→G→0·B유한, S4 c²=B/ρ; [V] 숫자).
3. **파장이 왜 나오는가** (주인공): 동작원리(ω=cq→λ=c/ν; 광주기=A 미시스텝; D=2π·a_phys=2πλ/A) +
   **반론4**(차원맞춤/임의λ/순환A/) + **반례2**(정적모드 D/λ=1.43은 회전이 해소; 4.96vs4.85=분포 offset).
4. **강성껍질 → D**: 회전언잼(§8.5.0)→r⁻⁴ 유입→x*=2/π→r_p; 양자 D=파장식; 연결 D=6π⁶r_p=π·(m_p/m_e).
5. **정직한 상태 원장**(표) + **열린 3고리**.
+ 부록 A(산출물), 부록 B(백서 연결).

---

## 5. 백서 구조·매크로 (병합 시 맞출 것 — 정독 필수)
- **섹션 번호 수동**: 프리앰블에 `secnumdepth=0` 류 — 즉 `\section{13. Mass: ...}`처럼 **번호를 손으로** 박음.
  새 단원 번호는 빈 자리를 골라라(예: §11과 §13 사이, 또는 §17 부근). 기존 번호와 충돌 금지.
- **등급 매크로**: `\Fm`(F), `\Hm`(H), `\Vm`(V) 사용 중(예: "graded \Vm{}"). 본문에서 그대로 쓸 것.
- **hyperref 라벨**: `\label{hub:stiffness}`(§11.6), `\label{hub:grinder}`(§8.5), `\label{hub:RpLq}`(§6.2),
  `\label{hub:nucleon}`(§8.0.5), `\label{hub:nucompute}`(§9.4), `\label{hub:mpme}`(§13.5),
  `\label{hub:lightangle}`(§10.9), `\label{hub:Adef}`(§10.5), `\label{hub:lrot}`(§3.4), `\label{hub:chain}`(§W.5).
  새 단원에 `\label{hub:spine}` 부여하고, 교차링크는 `\hyperref[hub:spine]{척추 §X}`로.
- **재현표 양식**: §11.6.5(줄 13200~)의 `\begin{tabular}...PASS` 형식을 모방(상태 원장·증거표에).
- **주요 절 줄번호(현 파일)**: §3.4=2610, §6.2=4948, §8.0=6920, §8.0.5=6975 부근/§8.0.6=7034,
  §8.5=8394·§8.5.0=8394 직후, §9.4=9078, §10.3.5=10021, §10.5=9307, §10.9(grep `hub:lightangle`),
  §11.6=13167·§11.6.5=13200, §13.5=14081, §W.5(grep `hub:chain`).
- **빌드 레시피**: 백서를 `/home/claude/wpbuild/`로 복사(uploads는 read-only). **draftmode로 먼저** 통과시키고
  (빠름·에러만 확인), 그다음 전체 컴파일. 보조 파일(aqd_constants.tex 등) 동봉 여부 확인. PDF ~468p.
  누락 패키지는 `tlmgr`/`apt` 불가할 수 있으니, 안 되면 draftmode 통과만으로 구조 검증.

---

## 6. 옛 문서 2개 수정(양성자/양자 오류)
- `VP_theory_chain_stiffness_to_D.md`: §Link6 부근 "**같은 원이 두 얼굴: 강성껍질 반경(Link4)과 빛-창발 회전호(Link5)**" →
  "양성자 r_p=0.84fm(Link4)와 양자 D=4.85pm(Link5)는 **다른 스케일**, D=6π⁶r_p로 연결" 로 교체.
- `VP_inevitability_chain.md`: Link6 "양자 = 강제된 원형 닫힌 흐름 … 같은 원 두 얼굴" 동일 취지로 수정.
- 두 문서 모두 D를 "proton diameter"라 부른 곳 → "**quantum diameter**"로 정정.

---

## 7. 실행 순서(권장)
1. 이 인수인계서 + `VP_jamming_spine_DRAFT.md` 정독. §1 양성자/양자 표 암기.
2. 백서 프리앰블/매크로(\Fm,\Hm,\Vm) + §11.6.5 표 양식 확인. 새 단원 번호·위치 결정.
3. 백서를 `/home/claude/wpbuild/`로 복사. `VP_jamming_spine_DRAFT.md` 5부를 .tex 단원으로 작성
   (\section{X. Jamming Spine ...}\label{hub:spine}, 등급 매크로·표 적용, 검증숫자 §1 인용).
4. 기존 ~7개 절에 한 줄 `\hyperref[hub:spine]{...}` 교차링크 삽입.
5. draftmode 빌드 → 에러 0 확인 → 전체 빌드 → PDF 페이지/단원 육안 확인.
6. 옛 문서 2개 수정(§6).
7. \WPVersion 버전업 한 줄. (번들 재봉인은 **사용자 승인 시에만**.)
8. present_files로 산출물 제시 + 간결 보고.

---

## 8. 열린 항목(척추 미완 3고리 — 단원의 "원장"에 정직히 박을 것, 닫으려 무리하지 말 것)
1. **회전 ⇒ 정확히 z=2d** (SOC pinning만 보임, [H]). 결판: 구동 하 z=2d pinning 시뮬 / Maxwell 끌개 증명.
2. **[MAP-1] 유도** — 섹터 lock 생존=δ=1/π²를 기하로. 닫히면 3π⁴·6π⁵·6π⁶ 정리화, **수비학 혐의 소멸**.
3. **Δt 독립성** — A_geo=cΔt/a의 Δt가 c로부터 자유로운가. 닫히면 절대 4.85pm 비순환 완결.

---

## 9. 환경 노트
- numpy 2.4.4: `np.trapezoid`(trapz 없음), `np.linalg.eigvalsh`. scipy 1.17.1. **단일 CPU**(병렬 없음).
- 툴 타임아웃 ~290s → 모든 러너 청크/CSV 재개식. 큰 그라인더/스윕은 steps 줄여 분할.
- 시뮬 재실행 필요 시: bulk(`bulk_run.py N 0 4`), 그라인더(`vp_grinder_3d.py`, ~23s), SOC(`soc_percolation_pinning.run_soc`, N=200).
- **750 격자 절대 돌리지 말 것**(~10시간, 사용자 명시).

---

## 10. 하지 말 것 (요약)
- 양성자(0.84fm)와 양자(4.85pm)를 섞지 말 것. D는 양자 지름.
- [MAP-1]/6π⁶/6π⁵에 **억지 유도** 붙이지 말 것 — 정직히 "정의층(α·δ 지위)"으로.
- 척추를 "증명 완료"로 과장하지 말 것 — 상태 원장 필수.
- 백서를 반쯤 편집하고 빌드 안 한 채 두지 말 것(draftmode로 매 단계 검증).
- 기존 LOCK 값/결론 변경 금지(새 단원은 [V] 추가일 뿐).
