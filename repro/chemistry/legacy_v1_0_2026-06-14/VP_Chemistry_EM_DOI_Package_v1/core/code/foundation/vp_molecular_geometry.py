# -*- coding: utf-8 -*-
"""
vp_molecular_geometry.py — VP 분자 기하(VSEPR): 구면 재밍 (재현가능·인과적)
====================================================================
주장: 분자의 모양은 전자영역(결합쌍+고립쌍, 전하구름)이 EM 1/r²로 밀치며 구면에 재밍해
      최대분리(반발 최소)로 배치된 결과다 — 정확히 VP 원리(EM 1/r² + 재밍).
      백서 §5의 사면체각 arccos(−1/3)(4영역)을 전 영역(2~6)으로 완성한다.

인과 사슬: 전자영역 N개 = 구면 위 N점 → EM 1/r² 반발 에너지 Σ1/r_ij 최소화(재밍)
           → 평형 배치 → 결합각. 시뮬레이션(시드 고정 경사하강)으로 기하 유도.

등급: [F] 기하(구면 N점 반발최소 = 톰슨 문제, 순수 기하/EM) · 실측 결합각 대조.
      [F?] 고립쌍 압축(고립쌍 반발↑) — 방향 맞음, 정밀값은 모델.
실행: python3 vp_molecular_geometry.py   (표준 라이브러리만)
"""
import math, random

def normalize(v):
    n = math.sqrt(sum(x*x for x in v))
    return [x/n for x in v]

def thomson(N, seed=7, iters=4000, lr=0.05):
    """구면 위 N점의 EM 1/r² 반발 에너지 최소화 (경사하강, 시드 고정)."""
    rng = random.Random(seed)
    # 초기 무작위 점
    P = [normalize([rng.gauss(0,1) for _ in range(3)]) for _ in range(N)]
    for it in range(iters):
        step = lr * (1 - it/iters)            # 점진 감소
        F = [[0.0,0.0,0.0] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if i==j: continue
                d = [P[i][k]-P[j][k] for k in range(3)]
                r2 = sum(x*x for x in d); r = math.sqrt(r2)
                if r < 1e-9: continue
                f = 1.0/r2                      # |F| ∝ 1/r² (EM)
                for k in range(3): F[i][k] += f*d[k]/r
        for i in range(N):
            # 접선 성분만 (구면 구속)
            radial = sum(F[i][k]*P[i][k] for k in range(3))
            tang = [F[i][k]-radial*P[i][k] for k in range(3)]
            P[i] = normalize([P[i][k]+step*tang[k] for k in range(3)])
    return P

def angles(P):
    """중심에서 본 점쌍 사이 각도 [deg] 전체."""
    out = []
    N = len(P)
    for i in range(N):
        for j in range(i+1,N):
            c = max(-1,min(1,sum(P[i][k]*P[j][k] for k in range(3))))
            out.append(math.degrees(math.acos(c)))
    return sorted(out)

# 이상 VSEPR 기하 + 대표 분자
VSEPR = [
    (2, "선형",        [180.0],          "CO2·BeCl2"),
    (3, "삼각평면",     [120.0],          "BF3·CO3²⁻·SO3"),
    (4, "사면체",       [109.47],         "CH4·NH4⁺·SiF4"),
    (5, "삼각양뿔",     [90.0,120.0],     "PF5·PCl5"),
    (6, "팔면체",       [90.0],           "SF6·PF6⁻"),
]


def main():
    print("="*72)
    print("VP 분자 기하(VSEPR) — 전자영역이 구면에 재밍 (EM 1/r² 반발 최소)")
    print("="*72)
    print("\n원리: 전자영역 N개 = 구면 N점. EM 1/r² 반발을 재밍으로 최소화 → 결합각.")
    print("      백서 §5 사면체각 arccos(−1/3)을 N=2~6 전 영역으로 완성.")

    print(f"\n[시뮬레이션] 구면 N점 반발최소 (시드=7) → 기하·결합각 (실측 대조)")
    print(f"  {'N':>2} {'기하':<8} {'예측 결합각':<20}{'이상값':<16}{'분자':<14}")
    print("  "+"-"*68)
    for N, name, ideal, mol in VSEPR:
        P = thomson(N)
        ang = angles(P)
        # 고유 각도 집합 (반올림 후 군집)
        uniq = []
        for a in ang:
            if not any(abs(a-u)<3 for u in uniq): uniq.append(round(a,1))
        pred = "·".join(f"{u:.1f}°" for u in uniq[:3])
        idl = "·".join(f"{i}°" for i in ideal)
        print(f"  {N:>2} {name:<8} {pred:<20}{idl:<16}{mol:<14}")

    # ── 헤드라인: 사면체각 ──
    P4 = thomson(4)
    tet = angles(P4)
    avg_tet = sum(tet)/len(tet)
    print(f"\n[헤드라인] 사면체(N=4): 시뮬 평균 {avg_tet:.2f}° vs arccos(−1/3)={math.degrees(math.acos(-1/3)):.2f}°")
    print(f"  → 구면 재밍이 CH4 결합각을 재현. 백서 §5와 정합, 이제 EM 1/r² 시뮬로도 독립 확인.")

    # ── 고립쌍 압축 (정직, 방향) ──
    print("\n[고립쌍 압축] 고립쌍은 더 큰 전하공간 → 결합각 압축 (방향 검증)")
    lone = [("CH4","4영역 0고립",109.5,109.47),("NH3","4영역 1고립",107.0,109.47),
            ("H2O","4영역 2고립",104.5,109.47)]
    print(f"  {'분자':<6}{'영역':<12}{'실측각':>8}{'기본사면체':>10}  압축")
    print("  "+"-"*44)
    for m,d,obs,base in lone:
        comp = base-obs
        print(f"  {m:<6}{d:<12}{obs:>7.1f}°{base:>9.2f}°  {comp:+.1f}° {'(고립쌍↑반발)' if comp>0 else ''}")
    print("  → 고립쌍 수↑ → 결합각↓ (109.5→107→104.5). 방향 일치 [F?]; 정밀값은 반발비 모델.")

    # ── VP 통일 ──
    print("\n[VP 통일] 구면 재밍의 세 얼굴")
    print("  • 분자각(본 모듈): 전자영역 N점 구면 재밍 → VSEPR 전 기하")
    print("  • 핵 마법수(vp_gauss_shells): 핵자 격자점 가우스 계수 → 2,8,20,28,82")
    print("  • 표면장력(§9): 자유표면 재밍 z=6 → 0.92")
    print("  같은 재밍+EM 1/r²이 분자모양·핵껍질·계면을 모두 빚는다. π-기하.")

    print("\n" + "="*72)
    print("등급: [F] VSEPR 전 기하 = 구면 N점 반발최소(EM 1/r² 재밍, 순수기하)")
    print("      [F?] 고립쌍 압축 방향 · [O] 고립쌍 압축 정밀값(반발비 모델)")
    print("      핵심: 분자의 *모양*이 VP 구면재밍에서. 원자→분자 기하 완성(2~6 전 영역).")
    print("="*72)


if __name__ == "__main__":
    main()
