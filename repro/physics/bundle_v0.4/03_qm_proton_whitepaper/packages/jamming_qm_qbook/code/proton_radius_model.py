"""
proton_radius_model.py

재밍 격자 · 유체역학 길이 선택 모형에서 나온
양성자 반지름 공식을 수치로 확인하는 스크립트.

기본 관계:
- 선택된 길이: L_q = λ_C = h / (m_p c)
- 무차원 압력: p_in(x)   = x^(-4)
               p_stiff(x)= α x^(-5),  α = 2/π
- 균형 조건:  p_in(x*) = p_stiff(x*)  →  x* = α
- 양성자 반지름: R_p = x* L_q = (2/π) λ_C

이 스크립트는 SI 상수(h, c, m_p)를 사용해 λ_C와 R_p를 계산하고,
단순 에너지 함수 E(R) = A/R + B/R^2를 시각화용으로 제공한다.
"""

import math

# --- 물리 상수 (CODATA 2018 값과 근사치) ---
h = 6.62607015e-34        # Planck constant [J s] (정의 값)
c = 2.99792458e8          # speed of light [m/s] (정의 값)
m_p = 1.67262192369e-27   # proton mass [kg] (근사값)

alpha_geom = 2.0 / math.pi   # α = 2/π


def compton_wavelength(m: float) -> float:
    """
    비감쇠(비축약) 콤프턴 파장 λ_C = h / (m c)
    """
    return h / (m * c)


def proton_compton_wavelength() -> float:
    """
    양성자 콤프턴 파장 λ_C (비감쇠).
    """
    return compton_wavelength(m_p)


def proton_radius(alpha: float = alpha_geom) -> float:
    """
    R_p = α λ_C  공식을 사용해 양성자 반지름을 계산.
    """
    lam_c = proton_compton_wavelength()
    return alpha * lam_c


def dimensionless_pressures(x: float, alpha: float = alpha_geom):
    """
    무차원 반지름 x = R / L_q 에서
    p_in(x) = x^-4,  p_stiff(x) = α x^-5 를 반환.
    """
    if x <= 0:
        raise ValueError("x must be positive")
    p_in = x ** -4
    p_stiff = alpha * x ** -5
    return p_in, p_stiff


def energy_function(R: float, A: float = 1.0, B: float = 1.0) -> float:
    """
    단순 에너지 함수 E(R) = A/R + B/R^2.
    절대 스케일보다는 1/R, 1/R^2 항의 상대적 형태만 사용.
    """
    if R <= 0:
        raise ValueError("R must be positive")
    return A / R + B / (R * R)


def demo():
    """
    콘솔용 간단 데모:
    - 양성자 콤프턴 파장 λ_C [fm]
    - 예측된 양성자 반지름 R_p = (2/π) λ_C [fm]
    - x* = α에서 p_in, p_stiff가 일치하는지 확인
    """
    lam_c = proton_compton_wavelength()
    R_p = proton_radius()

    fm = 1e-15
    print("=== Hydrodynamic Compton-length Proton Radius Demo ===")
    print(f"λ_C (proton Compton wavelength) = {lam_c/fm:.4f} fm")
    print(f"α = 2/π = {alpha_geom:.6f}")
    print(f"R_p = α λ_C = {R_p/fm:.4f} fm")
    print()

    x_star = alpha_geom
    p_in, p_stiff = dimensionless_pressures(x_star, alpha_geom)
    print(f"x* = α = {x_star:.6f}")
    print(f"p_in(x*)    = {p_in:.6e}")
    print(f"p_stiff(x*) = {p_stiff:.6e}")
    print("→ p_in(x*)와 p_stiff(x*)가 같은지 확인 (수치 오차 이내)")

    # 추가로 몇 점에서 압력 비율을 출력
    for x in [0.3, 0.5, 1.0, 2.0]:
        p_in_x, p_stiff_x = dimensionless_pressures(x, alpha_geom)
        ratio = p_in_x / p_stiff_x
        print(f"x={x:.2f}: p_in/p_stiff = {ratio:.3f}")


if __name__ == "__main__":
    demo()
