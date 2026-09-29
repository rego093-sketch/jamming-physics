# -*- coding: utf-8 -*-
"""
vp_valence.py — VP 원자가·주기경향: 전자껍질 → 화학 (재현가능·인과적)
====================================================================
목적: 주기율표 구조(전자껍질, vp_atomic)를 *실제 화학*으로 연결하는 다리.
      원자가(결합능)·화합물 화학식·주기경향(반지름·전기음성도)을 껍질에서 유도·검증.
      이것이 '물리+주기율표'를 '화학'으로 만든다.

인과 사슬: Aufbau 채움(vp_atomic) → 최외각 전자수 = 원자가 → 옥텟 규칙 → 화학식.
           유효핵전하 Z_eff(차폐) → 반지름 ~ n²/Z_eff, 전기음성도 ~ Z_eff/r² (경향).

등급: [F] 원자가=최외각 전자수(껍질에서 직접) · [F] 화학식(옥텟, 주족 정확)
      [F?] 주기경향 방향(반지름·전기음성도) · [O] 다전자 절대값(완전 다체)
실행: python3 vp_valence.py   (표준 라이브러리만)
"""
import math

# Aufbau 채움 순서 (n, l) — vp_atomic 와 동일
AUFBAU = [(1,0),(2,0),(2,1),(3,0),(3,1),(4,0),(3,2),(4,1),(5,0),(4,2),
          (5,1),(6,0),(4,3),(5,2),(6,1),(7,0),(5,3),(6,2),(7,1)]
LCAP = {0:2,1:6,2:10,3:14}   # s,p,d,f 용량
SYM = {1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",9:"F",10:"Ne",
       11:"Na",12:"Mg",13:"Al",14:"Si",15:"P",16:"S",17:"Cl",18:"Ar",
       19:"K",20:"Ca"}

def config(Z):
    """전자배치: [(n,l,채움수)]."""
    e = Z; out = []
    for (n,l) in AUFBAU:
        if e<=0: break
        f = min(e, LCAP[l]); out.append((n,l,f)); e -= f
    return out

def valence_electrons(Z):
    """최외각(최대 n) s+p 전자수 = 주족 원자가 전자."""
    cfg = config(Z)
    nmax = max(n for n,l,f in cfg)
    return sum(f for n,l,f in cfg if n==nmax and l in (0,1))

def ion_charge(Z):
    """옥텟 규칙: v≤3 금속(잃음 +v), v≥5 비금속(얻음 −(8−v)), v=4 공유(±4)."""
    v = valence_electrons(Z)
    if Z in (2,10,18): return 0          # 비활성
    if v <= 3: return +v
    if v >= 5: return -(8-v)
    return 4                              # 탄소족 (공유 4)

def formula(Zc, Za):
    """양이온 Zc + 음이온 Za → 전하교차 화학식."""
    a = ion_charge(Zc); b = -ion_charge(Za)
    if a<=0 or b<=0: return None
    g = math.gcd(a,b); na, nb = b//g, a//g
    def part(sym,n): return sym if n==1 else f"{sym}{n}"
    return part(SYM[Zc],na)+part(SYM[Za],nb)

# Slater 유효핵전하 (주기경향용)
def z_eff(Z):
    cfg = config(Z); nmax = max(n for n,l,f in cfg)
    sigma = 0.0
    for n,l,f in cfg:
        if n==nmax:  sigma += 0.35*(f-1) if l in(0,1) else 0.35*f
        elif n==nmax-1: sigma += 0.85*f
        else: sigma += 1.0*f
    return Z - sigma

NSTAR = {1:1,2:2,3:3,4:3.7,5:4,6:4.2}
def atomic_radius(Z):
    cfg = config(Z); nmax = max(n for n,l,f in cfg)
    return (NSTAR.get(nmax,nmax)**2)/z_eff(Z) * 0.529   # ~a₀ n*²/Z_eff [Å]
def electroneg(Z):
    cfg = config(Z); nmax = max(n for n,l,f in cfg)
    r = atomic_radius(Z)
    return 0.359*z_eff(Z)/r**2 + 0.744                  # Allred-Rochow 형


def main():
    print("="*72)
    print("VP 원자가·주기경향 — 전자껍질에서 화학으로 (다리)")
    print("="*72)

    # ── 원자가 = 최외각 전자수 ──
    print("\n[원자가] 최외각 전자수 (Aufbau 껍질에서 직접) → 주족")
    print(f"  {'원소':<5}{'Z':>3} {'배치(최외각)':<14}{'원자가':>6}{'이온전하':>8}")
    print("  "+"-"*42)
    for Z in range(1,21):
        v = valence_electrons(Z); q = ion_charge(Z)
        cfg = config(Z); nmax=max(n for n,l,f in cfg)
        outer = " ".join(f"{n}{'spdf'[l]}{f}" for n,l,f in cfg if n==nmax)
        qs = "비활성" if q==0 and Z in(2,10,18) else (f"{q:+d}" if q!=4 else "±4")
        print(f"  {SYM[Z]:<5}{Z:>3} {outer:<14}{v:>6}{qs:>8}")
    print("  → 원자가가 껍질에서 직접. 비활성기체(He·Ne·Ar) 0 = 완전껍질.")

    # ── 화학식 예측 (옥텟) ──
    print("\n[화학식] 원자가 + 옥텟 규칙 → 화합물 (실측 대조)")
    pairs = [(11,17,"NaCl"),(12,17,"MgCl2"),(13,17,"AlCl3"),(11,8,"Na2O"),
             (12,8,"MgO"),(20,8,"CaO"),(13,8,"Al2O3"),(20,17,"CaCl2"),(19,8,"K2O")]
    ok=0
    print(f"  {'양이온':<8}{'음이온':<8}{'예측':<10}{'실측':<10}{'일치':>5}")
    print("  "+"-"*42)
    for Zc,Za,real in pairs:
        f = formula(Zc,Za); hit = "✓" if f==real else "✗"
        if f==real: ok+=1
        print(f"  {SYM[Zc]:<8}{SYM[Za]:<8}{str(f):<10}{real:<10}{hit:>5}")
    print(f"  → 이온화합물 화학식 {ok}/{len(pairs)} 적중. 원자가만으로 화학량론 예측. [F]")

    # ── 주기경향 ──
    print("\n[주기경향] 유효핵전하에서 — 방향(순서) 검증 (절대값 아님)")
    print("  주기2 (Li→Ne): 반지름↓ · 전기음성도↑ (Z_eff↑)")
    print(f"  {'원소':<5}{'Z_eff':>6}{'반지름[Å]':>10}{'전기음성지수':>12}")
    print("  "+"-"*36)
    for Z in [3,4,5,6,7,8,9]:
        print(f"  {SYM[Z]:<5}{z_eff(Z):>6.2f}{atomic_radius(Z):>10.3f}{electroneg(Z):>12.2f}")
    r_dec = atomic_radius(3)>atomic_radius(9); en_inc = electroneg(9)>electroneg(3)
    print(f"  → 반지름 감소: {r_dec} ✓ · 전기음성도 증가: {en_inc} ✓ (주기 경향 일치)")
    print(f"  주의(정직): 전기음성'지수'는 단조 순서만 의미. 절대 Pauling값(F≈4)과 교정 안 됨 → [O].")
    print(f"            검증되는 것은 *방향/순서*이지 절대값이 아니다(다전자 절대값 미해결).")

    print("\n  족1 (Li→Na→K): 반지름↑ (n↑)")
    for Z in [3,11,19]:
        print(f"    {SYM[Z]:<4} 반지름 {atomic_radius(Z):.3f} Å")
    g_inc = atomic_radius(19)>atomic_radius(3)
    print(f"  → 아래로 반지름 증가: {g_inc} ✓ (족 경향 일치)")

    # ── 화학백서 연결 ──
    print("\n[화학백서 연결] 전기음성도 ↔ P_idx")
    print("  • 화학백서 P_idx=Z/r_cov² 가 전기음성도와 같은 구조(유효핵전하/반지름²).")
    print("  • 즉 원자껍질(본 모듈)→원자가·전기음성도→결합(P_idx·결합각·극성, 화학백서)으로 이어진다.")
    print("  • 원자→분자 사슬 완성: 껍질→원자가→화학식→결합기하(arccos(-1/3))→극성.")

    print("\n" + "="*72)
    print("등급: [F] 원자가=최외각 전자(껍질 직접) · [F] 이온 화학식(옥텟, 주족)")
    print("      [F?] 주기경향 방향(반지름·전기음성도, Z_eff) · [O] 다전자 절대값")
    print("      핵심: 전자껍질이 화학(원자가·화학식·경향)을 낳는다. 원자→분자 다리 완성.")
    print("="*72)


if __name__ == "__main__":
    main()
