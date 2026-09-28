"""
verify_constants_and_scales.py
================================================================================
VP 잼밍 이론 — 순수 수학(상수·스케일·기하) 검증 스크립트.

이 스크립트는 외부 물리 입력 없이(또는 CODATA 비교용으로만) "닫힌 형태로 증명된
것"과 "정의에 기댄 것(MAP-1)"을 한자리에서 수치로 확인한다. 시뮬레이션이 아니라
적분/대수/격자 셈이므로 결정론적이며 어느 기계에서도 같은 값이 나온다.

다루는 항목 (모두 본 세션에서 검증했고, 인라인으로만 돌렸던 것을 문서화해 복원):

  1) 각도 상수 (닫힌 형태 [F]):
       alpha = <|cos t|>_2D = 2/pi                (정류된 평균, 2D)
       <[cos t]+>     = 1/pi                       (한쪽 정류 평균)  -> delta = (1/pi)^2 = 1/pi^2
       <|cos t|>_3D   = 1/2                        (입체각 평균, 3D)
       2*pi = alpha/delta                          (두 증명된 적분의 비)

  2) n-겹 사다리 ([D] '거의 증명급' — 정의 MAP-1 한 점에만 의존):
       1/delta = pi^2
       nu_p = 3*pi^4 = n*(1/delta)^(n-1),  n=3      (C3, 3-겹)
       m_p/m_e = 6*pi^5 = 2*pi * 3*pi^4
       D/r_p   = 6*pi^6 = pi * 6*pi^5               (= pi * (m_p/m_e), 질량비의 변장)
     => 6*pi^6 은 독립 상수가 아니라 6*pi^5(질량비)의 변장임을 수치로 보인다.

  3) 양성자 vs 양자 스케일 분리 (절대 혼동 금지):
       r_p = (2/pi)*lambda_Cp  ~ 0.84 fm           (양성자 반경; 강성껍질 균형)
       D   = 2*lambda_Ce       ~ 4.85 pm           (양자 지름; 파장식)
       D/r_p = pi*(m_p/m_e) = 6*pi^6 ~ 5768        (두 스케일은 6*pi^6 배 떨어짐)

  4) 4.96 vs 4.85 (분포 offset, 근본 오류 아님):
       ell_rot = 2*pi*lambda_light/A               (A = 격자 침투 증폭, 무차원)
       목표 D = 2*lambda_Ce.  목표를 주는 A_target 을 역산.
       (A 분포 중앙값은 05_light_emergence/ellrot_verify.py 에서 데이터로 확인:
        중앙값 ~4.96 pm, best avalanche ~4.854 pm.)

  5) 정수 코어 + 정상모드 기하:
       3D 격자 #{ i^2+j^2+k^2 <= 6 } = 81 = 3^4   (양성자 코어 82 = 81+1)
       2D 격자 #{ i^2+j^2     <= 6 } = 21          (2D 유사)
       구면 베셀 첫 영점 -> 정적 정상모드라면 D/lambda = (k R_1)/pi:
         l=0 -> 1.00,  l=1 -> 1.43,  l=2 -> 1.83
       (반례 처리: 양자는 정적 모드가 아니라 *회전체*이므로 회전 둘레 2*pi 가
        자연 길이 -> D = 2*pi*lambda/A, 정적 1.43 이 아님.)

등급: [F] 닫힌 형태 증명 / [D] 정의 MAP-1 에 의존 / [A] 단일 앵커(절대 스케일).

실행:  python3 verify_constants_and_scales.py
의존:  numpy, scipy (베셀 영점; 없으면 하드코드 영점으로 진행)
"""

import numpy as np

# ---------------------------------------------------------------- CODATA (비교 전용)
M_P_OVER_M_E = 1836.15267343          # CODATA 양성자/전자 질량비
LAMBDA_C_P   = 1.32140985539e-15      # m, 양성자 콤프턴 파장
LAMBDA_C_E   = 2.42631023867e-12      # m, 전자 콤프턴 파장
R_P_CHARGE   = 0.8414e-15             # m, CODATA-2018 양성자 전하반경 (비교용)
LAMBDA_LIGHT = 633e-9                 # m, 운반광(HeNe) — 단일 앵커

def hr(t): print("\n" + "="*78 + "\n" + t + "\n" + "="*78)

# ============================================================ 1) 각도 상수 [F]
hr("1) 각도 상수 (닫힌 형태 [F])")
t = np.linspace(0, 2*np.pi, 2_000_001)
alpha_2D   = np.trapezoid(np.abs(np.cos(t)), t) / (2*np.pi)      # = 2/pi
rect_plus  = np.trapezoid(np.clip(np.cos(t), 0, None), t) / (2*np.pi)  # = 1/pi
th = np.linspace(0, np.pi, 2_000_001)
cos3D = np.trapezoid(np.abs(np.cos(th))*np.sin(th), th) / 2.0    # = 1/2
delta = rect_plus**2                                            # = 1/pi^2
print(f"  alpha = <|cos|>_2D      = {alpha_2D:.8f}   vs 2/pi   = {2/np.pi:.8f}")
print(f"  <[cos]+>               = {rect_plus:.8f}   vs 1/pi   = {1/np.pi:.8f}")
print(f"  <|cos|>_3D             = {cos3D:.8f}   vs 1/2    = 0.50000000")
print(f"  delta = <[cos]+>^2     = {delta:.8f}   vs 1/pi^2 = {1/np.pi**2:.8f}")
print(f"  alpha/delta            = {alpha_2D/delta:.8f}   vs 2*pi  = {2*np.pi:.8f}   <- 2*pi 는 두 증명된 적분의 비")

# ============================================================ 2) n-겹 사다리 [D]
hr("2) n-겹 사다리 [D] (정의 MAP-1: 섹터 lock 1개 = 1/delta = pi^2 — 이 한 점에만 의존)")
inv_delta = np.pi**2
n = 3
nu_p   = n * inv_delta**(n-1)        # 3 * (pi^2)^2 = 3 pi^4
mp_me  = 2*np.pi * nu_p              # 2pi * 3pi^4 = 6 pi^5
D_ratio= np.pi * mp_me              # pi * 6pi^5 = 6 pi^6
print(f"  1/delta                = {inv_delta:.6f}  (= pi^2)")
print(f"  nu_p = n*(1/delta)^(n-1), n=3 = {nu_p:.6f}  vs 3*pi^4 = {3*np.pi**4:.6f}")
print(f"  m_p/m_e = 2pi*nu_p     = {mp_me:.6f}  vs 6*pi^5 = {6*np.pi**5:.6f}")
print(f"     CODATA m_p/m_e      = {M_P_OVER_M_E:.6f}   ->  편차 {1e6*(6*np.pi**5-M_P_OVER_M_E)/M_P_OVER_M_E:+.1f} ppm")
print(f"  D/r_p = pi*(m_p/m_e)   = {D_ratio:.4f}  vs 6*pi^6 = {6*np.pi**6:.4f}")
print(f"  => 6*pi^6 은 독립 상수가 아니라 6*pi^5(질량비)의 변장. '6*pi^6 증명' = '6*pi^5 증명' = MAP-1 한 점.")

# ============================================================ 3) 양성자 vs 양자 스케일
hr("3) 양성자 vs 양자 스케일 분리 (절대 혼동 금지)")
r_p_pred = (2/np.pi) * LAMBDA_C_P      # m
D_pred   = 2.0 * LAMBDA_C_E            # m
print(f"  양성자 r_p = (2/pi)*lambda_Cp = {r_p_pred*1e15:.4f} fm   vs CODATA 전하반경 {R_P_CHARGE*1e15:.4f} fm "
      f"({100*(r_p_pred-R_P_CHARGE)/R_P_CHARGE:+.2f}%)")
print(f"  양자  D   = 2*lambda_Ce       = {D_pred*1e12:.4f} pm   (= 2 lambda_Ce)")
print(f"  D / r_p                       = {D_pred/r_p_pred:.2f}   vs pi*(m_p/m_e) = {np.pi*M_P_OVER_M_E:.2f}, 6*pi^6 = {6*np.pi**6:.2f}")
print(f"  => 양성자(10^-15 m)와 양자(10^-12 m)는 *다른 객체*, 6*pi^6(~5768)배 떨어짐. D 는 '양자 지름'.")

# ============================================================ 4) 4.96 vs 4.85
hr("4) 4.96 vs 4.85 (분포 offset — 근본 오류 아님)")
D_target = 2*LAMBDA_C_E                 # m, 목표 양자 지름
A_target = 2*np.pi*LAMBDA_LIGHT / D_target
print(f"  ell_rot = 2*pi*lambda_light/A  (lambda_light = {LAMBDA_LIGHT*1e9:.0f} nm)")
print(f"  목표 D = 2*lambda_Ce = {D_target*1e12:.4f} pm  를 주는 A_target = {A_target:.3e}")
for Amed, tag in [(8.01e5, "bundle A 중앙값"), (7.16e5, "독립 SOC A 중앙값(본 세션)")]:
    ell = 2*np.pi*LAMBDA_LIGHT/Amed
    print(f"    {tag:28s} A={Amed:.3e} -> ell_rot={ell*1e12:.3f} pm  (목표대비 {100*(ell-D_target)/D_target:+.1f}%)")
print(f"  => A 분포 중앙값이 목표보다 낮으면 ell_rot 가 높게 나옴(+%). 데이터 분포는 05/ellrot_verify.py 참조"
      f" (중앙값 ~4.96 pm, best ~4.854 pm).")

# ============================================================ 5) 정수 코어 + 정상모드
hr("5) 정수 코어 + 정상모드 기하")
def lattice_count(dim, rmax2):
    R = int(np.floor(np.sqrt(rmax2)))
    rng = range(-R, R+1)
    if dim == 2:
        return sum(1 for i in rng for j in rng if i*i+j*j <= rmax2)
    return sum(1 for i in rng for j in rng for k in rng if i*i+j*j+k*k <= rmax2)
n2 = lattice_count(2, 6); n3 = lattice_count(3, 6)
print(f"  2D  #{{ i^2+j^2     <= 6 }} = {n2}        (2D 유사)")
print(f"  3D  #{{ i^2+j^2+k^2 <= 6 }} = {n3}  = 3^4 = {3**4}   (양성자 코어 82 = 81+1)")

# 구면 베셀 첫 영점 -> 정적 정상모드 D/lambda = (kR)/pi
zeros = {0: np.pi, 1: 4.493409457909064, 2: 5.763459196894550}  # 하드코드 fallback
try:
    from scipy.special import spherical_jn
    from scipy.optimize import brentq
    grid = np.linspace(0.1, 12, 4000)
    for l in (0, 1, 2):
        vals = spherical_jn(l, grid)
        s = np.where(np.sign(vals[:-1]) != np.sign(vals[1:]))[0]
        if len(s):
            zeros[l] = brentq(lambda x: spherical_jn(l, x), grid[s[0]], grid[s[0]+1])
except Exception as e:
    print(f"  (scipy 베셀 사용 불가 -> 하드코드 영점 사용: {e})")
print("  정적 정상모드라면 D/lambda = (k R_1)/pi:")
for l in (0, 1, 2):
    print(f"    l={l}  첫 영점 x_1 = {zeros[l]:.5f}  ->  D/lambda = {zeros[l]/np.pi:.3f}")
print("  반례 처리: 양자는 *회전체*(그라인더). 정적 모드(l=1->1.43)가 아니라 회전 둘레 2*pi 가 길이")
print("            => D = 2*pi*lambda/A. 정적 1.43 과 다른 메커니즘.")

hr("요약")
print("  [F] 닫힌 형태 증명 : alpha=2/pi, <[cos]+>=1/pi, delta=1/pi^2, <|cos|>_3D=1/2, 2pi=alpha/delta,")
print("                       3D 코어 81=3^4, 2D 21, 베셀 정적 D/lambda(l=0,1,2)=1.00/1.43/1.83.")
print("  [D] 정의(MAP-1)    : 3pi^4 -> 6pi^5 -> 6pi^6 전부 '섹터 lock=pi^2' 한 점에 의존(alpha,delta 와 동일 지위).")
print("  스케일 분리        : 양성자 0.84 fm  vs  양자 4.85 pm,  비율 6pi^6 ~ 5768.")
print("  남은 열린 고리     : (1) 회전->정확히 z=2d  (2) MAP-1 기하 유도  (3) Dt 독립성(절대 4.85pm).")
