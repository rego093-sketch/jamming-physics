# -*- coding: utf-8 -*-
"""
vp_crystal_field.py — VP 결정장 이론: d-궤도 갈라짐 → 색·자성 (재현가능·인과적)
====================================================================
주장: 착물에서 d-궤도 갈라짐은 리간드 점전하(EM 1/r²)와 기하학적 d-궤도(구면 조화함수)의
      반발이다 — 정확히 VP(EM + 기하). 갈라짐 패턴·4/9 비·색·자성이 모두 기하에서.

인과 사슬: d-궤도 각함수(구면 조화) × 리간드 위치 EM 1/r² 중첩 → 갈라짐 패턴.
           팔면체: 축 향한 eg 높음, 사이 t2g 낮음. 사면체: 반전, Δ_tet=(4/9)Δ_oct.
           Δ = d-d 전이에너지 → 흡수파장 → 보색(관측색). Δ vs 짝짓기 → 고/저스핀 → 자성.

등급: [F] 갈라짐 패턴·4/9 비(d-궤도 기하+EM, 정확) · [F] 색 메커니즘(Δ→λ) ·
      [F] 자성=고/저스핀 홀전자수 · [CAL] 절대 Δ(분광화학계열) · [O] 정밀 색(다중띠 스펙트럼)
실행: python3 vp_crystal_field.py   (표준 라이브러리만)
"""
import math
PI = math.pi

def d_orbitals(x, y, z):
    """정규화 실수형 d-궤도 각함수 (단위구면 위)."""
    c2 = math.sqrt(5/(16*PI)); c = math.sqrt(15/(16*PI)); c4 = math.sqrt(15/(4*PI))
    return {'dz2':c2*(3*z*z-1), 'dx2y2':c*(x*x-y*y),
            'dxy':c4*x*y, 'dxz':c4*x*z, 'dyz':c4*y*z}

def field_split(ligands):
    """리간드 위치에서 각 d-궤도의 EM 장세기 Σ|Y|² (갈라짐 패턴)."""
    tot = {k:0.0 for k in ['dz2','dx2y2','dxy','dxz','dyz']}
    for (x,y,z) in ligands:
        n = math.sqrt(x*x+y*y+z*z); x,y,z = x/n,y/n,z/n
        for k,v in d_orbitals(x,y,z).items(): tot[k] += v*v
    return tot

def unpaired_oct(d, low_spin):
    """팔면체 d^n 의 홀전자수 (고/저스핀)."""
    def unp(n, orb):  # orb개 궤도에 Hund 후 짝짓기 → 홀전자수
        f = min(n, orb); s = max(0, n-orb); return f - s
    if low_spin:
        return unp(min(d,6),3) + unp(max(0,d-6),2)   # t2g 먼저 채움
    return unp(d,5)                                    # 고스핀: 5궤도 Hund

def mu_spin(n): return math.sqrt(n*(n+2))   # 스핀온리 자기모멘트 [BM]


def main():
    print("="*72)
    print("VP 결정장 이론 — d-궤도가 리간드 EM장에 갈라져 색·자성을 낳는다")
    print("="*72)
    print("\n원리: 리간드 점전하(EM 1/r²)가 기하학적 d-궤도(구면 조화)를 밀침 → 갈라짐.")

    # ── 갈라짐 패턴 (기하 유도) ──
    oct_lig = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
    tet_lig = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
    o = field_split(oct_lig); t = field_split(tet_lig)
    print("\n[갈라짐 패턴] d-궤도 EM 장세기 (리간드 향한 밀도)")
    print(f"  {'궤도':<7}{'팔면체':>9}{'사면체':>9}")
    print("  "+"-"*26)
    for k in ['dz2','dx2y2','dxy','dxz','dyz']:
        print(f"  {k:<7}{o[k]:>9.3f}{t[k]:>9.3f}")
    eg=(o['dz2']+o['dx2y2'])/2; t2g=(o['dxy']+o['dxz']+o['dyz'])/3
    e=(t['dz2']+t['dx2y2'])/2;  t2=(t['dxy']+t['dxz']+t['dyz'])/3
    print(f"  → 팔면체: eg(축향)={eg:.3f} 높음, t2g(사이)={t2g:.3f} 낮음")
    print(f"    사면체: e={e:.3f} 낮음, t2={t2:.3f} 높음 — 반전!")

    # ── 4/9 비 (정확) ──
    print(f"\n[4/9 비] Δ_tet/Δ_oct = {(t2-e)/(eg-t2g):.4f}  vs 이론 4/9={4/9:.4f}  정확 ✓")
    print("  → d-궤도 기하 + EM 중첩만으로 유명한 4/9 비가 강제. 자유계수 0. [F]")

    # ── 색 (메커니즘 + 단일띠 예, 정직) ──
    print("\n[색] Δ = d-d 전이에너지 → 흡수파장(정확) → 보색이 관측색")
    print("  메커니즘: λ_흡수[nm] = 10⁷/Δ[cm⁻¹]. 관측색 = 흡수색의 보색.")
    lam = 1e7/20300
    print(f"  예) [Ti(H2O)6]³⁺: Δ=20300 cm⁻¹ → λ_흡수={lam:.0f} nm (가시 청록) → 적자색 관측")
    print(f"     d¹ 단일전이라 Δ가 가시광에 떨어져 보색이 색이 됨. 실제 보라/적자색과 대략 일치.")
    print("  정직: 다중전자(Cu d⁹·Ni d⁸)는 여러 띠+띠너비 → 단일 Δ 모형 불충분(색 정밀예측 [O]).")
    print("        단, '색 = d-d 전이 = Δ' *메커니즘*은 VP 기하 [F]. Δ가 가시광이면 색을 띤다.")

    # ── 자성 (고/저스핀) ──
    print("\n[자성] Δ vs 짝짓기에너지 → 고/저스핀 → 홀전자수 → 자기모멘트")
    print(f"  {'d^n':<5}{'고스핀 홀e':>10}{'μ[BM]':>7}{'저스핀 홀e':>11}{'μ[BM]':>7}")
    print("  "+"-"*42)
    for d in range(4,8):
        hu = unpaired_oct(d, False); lu = unpaired_oct(d, True)
        print(f"  d{d:<4}{hu:>10}{mu_spin(hu):>7.2f}{lu:>11}{mu_spin(lu):>7.2f}")
    print("  → 약한장(H2O): 고스핀(Δ<짝짓기). 강한장(CN⁻): 저스핀(Δ>짝짓기).")
    print("    예: [Fe(H2O)6]³⁺ 고스핀 5홀(μ=5.92), [Fe(CN)6]³⁻ 저스핀 1홀(μ=1.73). [F]")

    # ── 분광화학계열 ──
    print("\n[분광화학계열] 리간드 장세기 순서 (절대 Δ 정함) [CAL]")
    print("  I⁻ < Br⁻ < Cl⁻ < F⁻ < H2O < NH3 < CN⁻ < CO")
    print("  약한장(고스핀·작은Δ·붉은흡수) → 강한장(저스핀·큰Δ·푸른흡수).")
    print("  → 순서는 [CAL](경험), 갈라짐 패턴·색·자성 *구조*는 VP 기하 [F].")

    # ── VP 통일 ──
    print("\n[VP 통일] 구면 기하 + EM 1/r²의 또 한 얼굴")
    print("  • 분자각(VSEPR): 구 위 N점 반발 → 모양")
    print("  • 결정장(본 모듈): 구면 조화 d-궤도 × 리간드 EM → 색·자성")
    print("  • 둘 다 EM 1/r² + 구면 기하. Lewis 산-염기(전자쌍)→배위화학→광학·자기로 이어짐.")

    print("\n" + "="*72)
    print("등급: [F] 갈라짐 패턴·4/9 비(d-궤도 기하+EM, 정확) · [F] 색 메커니즘·자성=홀전자")
    print("      [CAL] 절대 Δ(분광화학계열) · [O] 정밀 색(다중띠 스펙트럼)")
    print("      핵심: 전이금속 색·자성이 d-궤도 기하 + 리간드 EM에서. 배위화학이 VP 위에.")
    print("="*72)


if __name__ == "__main__":
    main()
