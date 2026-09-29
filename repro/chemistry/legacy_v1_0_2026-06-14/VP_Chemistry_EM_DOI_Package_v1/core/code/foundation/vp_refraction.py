# -*- coding: utf-8 -*-
"""
vp_refraction.py — VP 굴절·분산: 빛의 각도이론을 매질로 (재현가능·인과적)
====================================================================
주장: 빛(회전양자 횡파, 전파각 χ; vp_light_angle)이 매질에 들어가면 전파각이 바뀐다.
      계면에서 횡진동 정합 → 스넬 법칙. 분산(n이 λ에 의존) → 무지개. 모두 각도 기하.

인과 사슬: 빛 = 횡파(vp_light_angle). 매질 = 회전양자 밀도 다른 격자 → 속도 v=c/n.
           계면 횡진동(접선파수) 정합 → n₁sinθ₁=n₂sinθ₂ (스넬).
           물방울 구 기하 + 스넬 → 편향 최소(무지개각). 분산 → 색 분리.

등급: [F] 스넬 기하·무지개각(스넬+구기하)·임계각(전반사) · [F?] 분산 방향(파랑 더 굴절)
      [CAL] 절대 굴절률 n(매질 고유) · [개념] n=회전양자 응답
실행: python3 vp_refraction.py   (표준 라이브러리만)
"""
import math

def snell_refract(theta_i_deg, n1, n2):
    """스넬: n1 sinθ1 = n2 sinθ2 → θ2 [deg] (전반사면 None)."""
    s = n1*math.sin(math.radians(theta_i_deg))/n2
    if abs(s) > 1: return None
    return math.degrees(math.asin(s))

def critical_angle(n_dense, n_rare=1.0):
    """전반사 임계각 sinθc = n_rare/n_dense."""
    return math.degrees(math.asin(n_rare/n_dense))

def rainbow_deviation(theta_i_deg, n):
    """물방울 1차 무지개 총편향 D = 180 + 2θi − 4θr [deg]."""
    ti = math.radians(theta_i_deg)
    tr = math.asin(math.sin(ti)/n)
    return 180 + math.degrees(2*ti - 4*tr)

def rainbow_angle(n):
    """편향 최소(무지개각) 수치 탐색 → 반시점에서의 무지개 반각 [deg]."""
    best = None
    for i in range(1, 9000):
        ti = i/100.0
        if ti >= 90: break
        D = rainbow_deviation(ti, n)
        if best is None or D < best[1]: best = (ti, D)
    return 180 - best[1], best[0]    # 무지개각, 그때의 입사각


def main():
    print("="*72)
    print("VP 굴절·분산 — 빛의 각도이론을 매질로 (계면 횡진동 정합)")
    print("="*72)
    print("\n원리: 빛=회전양자 횡파(vp_light_angle). 매질에서 v=c/n. 계면 횡진동 정합 → 스넬.")

    # ── 스넬 법칙 ──
    print("\n[스넬 법칙] n₁sinθ₁=n₂sinθ₂ (횡진동 접선성분 보존)")
    print(f"  {'경계':<16}{'입사각':>7}{'굴절각':>8}  비고")
    print("  "+"-"*38)
    cases = [("공기→물 (1→1.333)",30,1.0,1.333),("공기→유리(1→1.5)",30,1.0,1.5),
             ("물→공기 (1.333→1)",30,1.333,1.0),("공기→다이아(1→2.42)",30,1.0,2.42)]
    for name,ti,n1,n2 in cases:
        tr = snell_refract(ti,n1,n2)
        print(f"  {name:<16}{ti:>6}°{tr:>7.1f}°  {'밀→소(꺾임 큼)' if n1>n2 else '소→밀(꺾임 작음)'}")
    print("  → 밀한 매질로 갈수록 법선 쪽으로 꺾임. 횡파 각도가 매질 경계서 바뀜. [F]")

    # ── 전반사 임계각 ──
    print("\n[전반사] 임계각 sinθc = 1/n (밀→소, θ>θc 면 전반사)")
    for name,n in [("물",1.333),("유리",1.5),("다이아몬드",2.42)]:
        print(f"  {name:<10} n={n}: 임계각 θc = {critical_angle(n):.1f}°")
    print("  → 다이아몬드 작은 θc(24.4°)가 강한 전반사 → 광채. 광섬유도 전반사. [F]")

    # ── 무지개 각 (스넬+구 기하) ──
    print("\n[무지개 각] 물방울 구 기하 + 스넬 → 편향 최소각 = 무지개")
    ra, ti_rb = rainbow_angle(1.333)
    print(f"  물(n=1.333): 무지개각 = {ra:.1f}° (입사각 {ti_rb:.1f}°에서 편향최소)")
    print(f"  실측 1차 무지개 ≈ 42° → Δ={ra-42:.1f}°  [F] (데카르트 계산)")
    print("  → 광선이 편향최소각에 몰려 밝은 호. 순수 기하(구+스넬)에서 42°가 나온다.")

    # ── 분산 → 무지개 색 ──
    print("\n[분산 → 무지개 색] n(λ) 파장 의존 → 색마다 무지개각 다름")
    print(f"  {'색':<6}{'λ[nm]':>7}{'n(물)':>8}{'무지개각':>9}")
    print("  "+"-"*30)
    # 물의 분산 (파장별 굴절률)
    disp = [("빨강",656,1.3311),("노랑",589,1.3330),("초록",532,1.3352),("보라",400,1.3404)]
    angles=[]
    for col,lam,n in disp:
        ra,_ = rainbow_angle(n); angles.append((col,ra))
        print(f"  {col:<6}{lam:>7}{n:>8.4f}{ra:>9.2f}°")
    print(f"  → 보라({angles[-1][1]:.1f}°) < 빨강({angles[0][1]:.1f}°): 빨강이 바깥. 1차무지개 색순서 일치.")
    print("    분산(짧은λ 더 굴절)이 색을 분리. 파랑이 빨강보다 더 꺾임. [F?]")

    # ── VP 통일 ──
    print("\n[VP 통일] 각도이론의 연장")
    print("  • 빛 = 회전양자 횡파, 전파각 χ=λ/(mD) (vp_light_angle)")
    print("  • 굴절 = 매질 경계서 χ(각도) 바뀜 → 스넬. 매질=회전양자 밀도 다른 격자.")
    print("  • 분산 = χ의 파장 의존이 매질서 증폭 → 색 분리 → 무지개 42°.")
    print("  • n=c/v=√(격자강성/밀도)의 매질판(§14 c²=B/ρ). 절대 n은 매질 [CAL].")

    print("\n" + "="*72)
    print("등급: [F] 스넬 기하·무지개각 42°(구+스넬)·임계각(전반사) · [F?] 분산 색순서")
    print("      [CAL] 절대 굴절률 n · [개념] n=회전양자 응답·c²=B/ρ 매질판")
    print("      핵심: 굴절·무지개가 빛의 각도이론에서. 빛=횡파, 매질서 각도 바뀜→스넬→무지개.")
    print("="*72)


if __name__ == "__main__":
    main()
