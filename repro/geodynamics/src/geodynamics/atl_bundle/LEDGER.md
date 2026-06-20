# LEDGER — claim → script → result → 기대값/공차 (검수 매핑)

각 행은 `validate_all.py` 의 한 검사에 대응. 등급: [DERIVE]=유도/측정, [GATE]=외삽조건부.

| ID | 주장 (claim) | 스크립트 | 결과 파일 | 기대값 / 공차 | 측정값 | 등급 |
|---|---|---|---|---|---|---|
| C1a | 잼밍 액체화로 $\mu_{eff}$ 가 Ω-NoGo($10^{-2}$) 아래로 붕괴 | `engine/vp_jamming_friction.py` | `vp_jamming_results.npz` | $\mu_{eff}<10^{-2}$ | $2.2\times10^{-3}$ | [DERIVE]+[GATE] |
| C1b | 액체화는 용융점 아래에서 일어남 (무융) | 〃 | 〃 | $\Delta T<1000$K, melted=False | 25 K | [DERIVE] |
| C1c | 용융전용(언잼밍 없음)은 용융함 (대조) | 〃 | 〃 | melted=True | 1462 K | [DERIVE] |
| C2 | 열가압(확증)도 비배수 약화>50%·무융 | `engine/tp_dilatancy_prototype.py` | `tp_dilatancy_results.npz` | weaken>0.5, melted=False | 82%, 172 K | [DERIVE]+[GATE] |
| C3 | 마찰을 액체화로 고정 시 $\Lambda\propto d^2$, 임계깊이 8–20km | `engine/feasibility_map.py` | `feasibility_results.npz` | crit depth ∈ [8,20] km | 12.0 km | [DERIVE]+[GATE] |
| C4a | 잼밍 onset $\phi_{jam}\approx0.84$ (2D bidisperse) | `engine/jamming_microderive.py` | `jamming_microderive_results.npz` | $|\phi_{jam}-0.84|<0.02$ | 0.840 | [DERIVE] |
| C4b | 등정압 $z_{iso}=2d$ | 〃 | 〃 | $z_{iso}=4$ (2D) | 4 | [DERIVE] |
| C4c | 잼 위에서 $z\to z_{iso}$ | 〃 | 〃 | $z_{iso}-0.2\le z<6$ | 4.88 | [DERIVE] |
| C5a | 잼 근처 $G_{relaxed}\ll G_{Born}$ | `engine/jamming_shear_modulus.py` | `jamming_shear_results.npz` | $G_{rel}/G_{Born}<0.5$ | 0.09 | [DERIVE] |
| C5b | $G_{relaxed}\propto(z-z_{iso})$ (→0 at iso) | 〃 | 〃 | slope>0 | 0.068 | [DERIVE] |
| C5c | $G_{Born}$ 유한 O(0.1–1) | 〃 | 〃 | $0.05<G_{Born}<1$ | 0.20 | [DERIVE] |
| C6a | P8 역전 barcode 불규칙(비주기) | `engine/p8_magnetic_test.py` | `p8_results.npz` | CV(durations)>0.5 | 0.86 | [DERIVE] |
| C6b | P8: H2(공명) FAIL — 스펙트럼 broad & incoherent | 〃 | 〃 | concentration<0.5 & coh<0.5 | 0.15, +0.04 | [DERIVE] |
| C7 | C-3 논리: 줄무늬는 균일 시간압축에 축퇴(위치 동일) | `engine/c3b_braking_and_stripe_logic.py` | `c3b_results.npz` | max\|pos diff\|<1e-6 km | 1.4e-14 | [DERIVE] |
| C8a | C-5: 줄무늬는 *상대* 감속만 줌(초기/후기>2, 절대시간 무관) | `engine/c5_velocity_history.py` | `c5_results.npz` | ratio>2 | 2.6 (상대) | [DERIVE] |
| C8b | C-5: 수천 년 개방이 물리적으로 허용(액체화 구동<100 Pa) | 〃 | 〃 | max drive<100 Pa | 3–32 Pa | [DERIVE]+[GATE] |
| C8c | C-5: 브레이크=mm 전단대 재잼밍 빠름(τ<1e3 s) → 짧은 사건 | 〃 | 〃 | τ_rejam(mm)<1e3 s | 9 s | [DERIVE] |
| C9a | 쌍안정: 액체화 유지 V≫cm/yr (느린 액체화 없음) | `engine/jamming_bistability.py` | `jamming_bistability_results.npz` | V_crit/cm-yr>1e6 | ~8e8 | [DERIVE] |
| C9b | 쌍안정: 속도-약화 → 불안정 → stick-slip | 〃 | 〃 | 속도약화 구간 존재 | 142 pts | [DERIVE] |
| C9c | 3000km 개방의 누적 미끄러짐은 짧음(<1 yr) | 〃 | 〃 | <365 days | 69 days | [DERIVE] |
| C10 | C-2 트리거: 초기·모빌라이즈 ΔR 둘 다 <50km(Ω-NoGo) | `engine/c2_trigger.py` | `c2_results.npz` | ΔR<50km | 0.6, 25 km | [DERIVE]+[GATE] |
| C11a | P7: 임계깊이 ∝√W (Atlantic>홍해>Afar) 스케일 일관 예측 | `engine/c4_scalability.py` | `c4_results.npz` | dc 내림차순 | 12/3.3/1.9 km | [DERIVE] |
| C11b | **마스터 게이트 HOLD**: 시스템 타당성 lab 재현 불가(기하 부조리) | 〃 | 〃 | d_lab>0.1 m | 0.60 m@1cm | [GATE] |
| C12 | Ω-NoGo 전 항목 통과(5/5) | `engine/omega_nogo_check.py` | `omega_nogo_results.npz` | npass=ntot | 5/5 | [GATE] |
| C13 | P1: 대서양 섭입 분율 UNLOCK(최악 0.129<0.25); 수동주변부 바다 | `engine/p1_plate_boundaries.py` | `p1_results.npz` | R_sub<0.25 | 0.057 | [DATA]+[GATE] |
| C14 | P9: 레짐 분리(UHP viscous De<1; 사건 brittle De>1) → HOLD | `engine/p9_orogeny_deborah.py` | `p9_results.npz` | De_std<1 & De_fast>1 | 0.11 / 3.9e5 | [DATA] |
| C15 | P7 현장검증: 관측 깊이=열적(ρ_cold>0.9), 폭 아님(ρ_W<0.6) → 마스터 HOLD 유지 | `engine/c7_scaling_field_test.py` | `c7_field_results.npz` | ρ_cold>0.9 & ρ_W<0.6 | +1.00 / −0.56 | [GATE] |
| C16a | 통합 에너지원장: 열은 W_in 의 소부분(<20%), 대부분은 분지 PE | `engine/c16_energy_ledger.py` | `c16_energy_ledger_results.npz` | Q_fric/W_in<0.20 | 3.3% | [DERIVE] |
| C16b | 전도만으로는 kyr 사건 열 처분 불가(용융급 ΔT) → 이류 필수 | 〃 | 〃 | ΔT_cond>0.3·T_melt | 596 K | [DERIVE] |
| C16c | 이류 sink → 크고 검증가능한 열수 처리량(반증가능 P4) | 〃 | 〃 | V_fluid≥1e4 km³ | 5.0e6 km³ | [DERIVE]+[GATE] |

## 파생 규칙 → ATL 마찰 모델 환원
- `vp_jamming_friction.py` 가 *가정* 하던 ($z_{iso}$, $\phi_{jam}$, $\sigma_y(z)\propto\Delta z$) 는
  이제 C4–C5 에서 **측정/유도**됨. 3D 값($z_{iso}=6$)은 스파인 S2.4; 2D 런(C4–C5)은 규칙 형태 확인.
- $\sigma_y \sim G_{relaxed}\,\gamma_y \sim (z-z_{iso}) \to 0$ → 액체화 = 마찰 붕괴 (C1).

## 재생성 → 무결성
```bash
python validate_all.py                     # 30/30 PASS
sha256sum -c SHA256SUMS.txt                 # 파일 무결성
```
변경 시 새 체크섬을 재발급(백서 규약: config/결과 변경 = 새 버전).

## r17→r18 addition: C-16 unified energy ledger (credibility hardening)
- `engine/c16_energy_ledger.py` — separates the three stresses (ΔP suction *input*,
  μ_eff·σ_n liquefied *friction→heat*, τ_drive *mean-rate kinematic*) into ONE ledger
  `W_in = ΔPE_basin + Q_fric + W_fracture`; shows heat = a few % of W_in (Q_fric~1e24–1e25 J),
  that conduction ALONE is insufficient over kyr (ΔT_cond~melt-order), and that the
  lubricating fluid the mechanism already requires is the forced advective sink,
  quantified as a falsifiable P4-thermal hydrothermal-flux prediction (~1e4–1e6 km³).
  - regen results: `python engine/c16_energy_ledger.py` (saves npz to CWD; move to results/)
  - regen figure:  `python make_c16_fig.py` → figures/fig_c16_energy_ledger.png
  - audited by validate_all.py :: C16a/b/c
- validator total: 27/27 → 30/30 PASS.

## r18 addition: C-17 AR-1 energy-source audit (load-bearing open link, quantified)
- `engine/c17_energy_source.py` — bounds the three candidate sources against the
  W_in~3e26 J requirement: H-E1 (release of stored internal heat) is the only
  energetically admissible class (thermal ~1e27–1e28 J; eta_mech>~few % suffices);
  H-E2-generation needs 20–200x whole-Earth heat flow (excluded); H-E2-impact ⇒ ~98 km
  impactor, excluded by absence of a global melt/ejecta signature; H-E3 core-field
  energy ~1e21–1e22 J is 4–6 orders short (excluded as a source). Verdict = honest HOLD;
  residual converted to a pre-registered AR-1-source falsifier (≥1e26 J reservoir signature).
  - regen results: `python engine/c17_energy_source.py` (saves npz to CWD; move to results/)
  - regen figure:  `python make_c17_fig.py` → figures/fig_c17_energy_source.png
  - audited by validate_all.py :: C17a/b/c
- validator total: 30/30 → 33/33 PASS.

## master-scale addition: C-19 lab->Earth extrapolation bounds (the other big HOLD, bounded)
- `engine/c19_master_scale.py` — bounds the lab-granular -> continental-shear-zone leap
  (the 'master-scale extrapolation HOLD') in the AR-1 idiom: (A) dimensionless-group transfer
  (inertial number I<<1 in BOTH => dense/quasi-static regime transfers; sigma_n/sigma_crush
  crosses ~1 at Earth => grain-crushing regime BREAKS); (B) continuum limit (N_total~1e21 =>
  phi_J finite-size correction ->0, so the LARGE scale is the clean limit); (C) the load-bearing
  low friction: dynamic weakening to mu~0.1 is EXPERIMENTALLY CONFIRMED at lithospheric sigma_n,
  V~1 m/s (Di Toro+ 2011; Tohoku <0.2; landslides 0.05-0.2), but the paper's mu_eff=0.002
  (~273x weakening) requires near-lithostatic pore pressure (lambda~0.997) -- the same sigma'->0
  endpoint as thermal pressurization. Verdict = honest HOLD; residual converted to a
  pre-registered master-scale falsifier (sustained mu_eff<~0.01 at lithospheric conditions).
  - regen: `python engine/c19_master_scale.py` (npz to CWD; move to results/);
    figure `python make_c19_fig.py` -> figures/fig_c19_master_scale.png
  - audited by validate_all.py :: C19a/b/c.
- validator total: 36/36 -> 39/39 PASS.
