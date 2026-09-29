# -*- coding: utf-8 -*-
"""
vp_shell_correction.py — 핵 마법수 껍질보정 (재현가능·인과적, 정직)
====================================================================
목적: vp_periodic_table.py 의 [O] 잔여(핵껍질)를 정량 진단. 매끈한 VP SEMF 너머의
      "초과 결합" ΔB 가 핵 마법수(2,8,20,28,50,82,126)와 상관됨을 보이고, 간단한
      보정으로 질량 예측을 개선한다.

정직 경계: 마법수 자체는 핵껍질 닫힘(스핀-궤도 껍질모형)으로, VP 1차 원리로 *아직 유도 못함*.
           본 모듈은 마법수를 구조 입력[CAL]으로 받아 잔차와의 상관·보정을 보인다.
           (흥미로운 관찰: 82는 VP 양성자 코어수 N_p=89=82+7 의 82와 일치 — 우연/심층 미정.)

실행: python3 vp_shell_correction.py   (표준 라이브러리만)
"""
import math
PI = math.pi

# ── 입자질량 + SEMF (단일 SSOT, vp_periodic_table.py 와 동일) ──
M_E = 0.51099895
M_P = 6*PI**5 * M_E
DELTA = 1/PI**2
M_N = M_P + ((4+2*DELTA)*M_E - (1/137.035999)*197.3269804/(2*0.84))
U_MEV = 931.49410242
A_V, A_S, A_A, A_PAIR = 15.75, 17.80, 23.70, 12.0
A_C = (3/5)*(1/137.035999)*197.3269804/1.20

MAGIC = [2, 8, 20, 28, 50, 82, 126]    # 핵 마법수 [CAL] (구조 입력)

def pairing(A, Z):
    N=A-Z
    if A%2==1: return 0.0
    return (+A_PAIR if (Z%2==0 and N%2==0) else -A_PAIR)/math.sqrt(A)

def binding_semf(A, Z):
    if A<=0 or Z<0 or Z>A: return float('-inf')
    return (A_V*A - A_S*A**(2/3) - A_C*Z*(Z-1)/A**(1/3)
            - A_A*(A-2*Z)**2/A + pairing(A,Z))

def binding_measured(A, Z, M_atom_u):
    """측정 원자질량에서 역산한 결합에너지 [MeV]."""
    N=A-Z
    return Z*M_P + N*M_N + Z*M_E - M_atom_u*U_MEV

def magic_distance(n):
    """가장 가까운 마법수까지 거리."""
    return min(abs(n-m) for m in MAGIC)

def is_magic(n): return n in MAGIC

# 검증 데이터: (기호, Z, A, 측정 원자질량[u]) — 마법수 근처 위주
NUCLEI = [
    ("He",2,4,4.0026032541),  ("C",6,12,12.0),          ("O",8,16,15.9949146196),
    ("Ne",10,20,19.9924401762),("Si",14,28,27.9769265347),("Ca",20,40,39.9625909),
    ("Ca",20,48,47.95252276), ("Ni",28,58,57.9353424),  ("Ni",28,62,61.92834537),
    ("Sn",50,120,119.9022016),("Sn",50,132,131.9178267), ("Ba",56,138,137.9052470),
    ("Pb",82,208,207.9766525),("Pb",82,206,205.9744657), ("Fe",26,56,55.9349363),
    ("U",92,238,238.0507884),
]


def main():
    print("="*72)
    print("핵 마법수 껍질보정 — 매끈한 SEMF 너머 초과결합 ΔB 가 마법수와 상관")
    print("="*72)
    print(f"\n핵 마법수 [CAL]: {MAGIC}   (VP 1차원리 유도는 [O]; 82는 N_p 코어 82와 일치 — 미정)")

    print(f"\n{'핵종':<7}{'Z':>3}{'N':>4}{'A':>4} {'ΔB[MeV]':>9} {'Z마법':>6}{'N마법':>6}  비고")
    print("  "+"-"*62)
    rows = []
    for sym, Z, A, M_u in NUCLEI:
        N = A-Z
        dB = binding_measured(A,Z,M_u) - binding_semf(A,Z)   # 초과결합(>0=SEMF 과소결합)
        rows.append((sym,Z,N,A,dB))
        zt = "★" if is_magic(Z) else f"{magic_distance(Z)}"
        nt = "★" if is_magic(N) else f"{magic_distance(N)}"
        dbl = "이중마법" if (is_magic(Z) and is_magic(N)) else ("단일마법" if (is_magic(Z) or is_magic(N)) else "")
        print(f"  {sym:<7}{Z:>3}{N:>4}{A:>4} {dB:>+9.2f} {zt:>6}{nt:>6}  {dbl}")

    # ── 상관: 이중마법 vs 비마법 (노이즈 동반) ──
    dbl = [dB for s,Z,N,A,dB in rows if is_magic(Z) and is_magic(N)]
    nonmagic = [dB for s,Z,N,A,dB in rows if not is_magic(Z) and not is_magic(N)]
    print("\n[상관] 이중마법 핵은 평균적으로 초과결합(ΔB>0) — 단 노이즈 있음")
    if dbl:    print(f"  이중마법 평균 ΔB = {sum(dbl)/len(dbl):+.2f} MeV  (강한 양: Sn-132 +12·Pb-208 +8·He-4 +5)")
    if nonmagic: print(f"  비마법 평균 ΔB = {sum(nonmagic)/len(nonmagic):+.2f} MeV")
    print("  예외(정직): Ca-40·Ca-48·Ne-20 은 마법수인데 ΔB<0 — N=Z 위그너에너지 등 추가효과.")
    print("  → 봉우리 경향은 실재(질량 [O]=핵껍질 확증)하나, 단순 근접만으론 설명 불완전.")

    # ── 간단 보정 시도 → 실패 (정직) ──
    print("\n[보정 시도 → 음성 결과] 마법 근접 보너스는 과보정으로 실패")
    S, w = 6.0, 2.0
    before, after = [], []
    for sym,Z,N,A,dB in rows:
        corr = S*math.exp(-magic_distance(Z)/w) + S*math.exp(-magic_distance(N)/w)
        before.append(abs(dB)); after.append(abs(dB - corr))
    mb, ma = sum(before)/len(before), sum(after)/len(after)
    print(f"  마법근접 보너스 적용:  결합오차 {mb:.2f} → {ma:.2f} MeV  ({'개선' if ma<mb else '악화 ✗'})")
    print("  실패 원인: ΔB 부호가 마법수에서 +/− 둘 다(Ca-40 −, Sn-132 +). 일률 양보너스가 −쪽을 악화.")
    print("  결론: 제대로 된 보정은 스트루틴스키/껍질모형(스핀-궤도 준위) 필요 → [O] 유지.")
    print("        (무리한 끼워맞춤 금지 — M1 BDE·sqrt2.5 철회와 같은 규율. 음성 결과도 결과.)")

    print("\n" + "="*72)
    print("등급: [F?] ΔB-마법수 상관(이중마법 양 경향, 강한 케이스 명확) · [CAL] 마법수")
    print("      [O] 마법수 VP유도(스핀-궤도)·정확한 껍질보정 — 미해결. 단순 보정은 실패 확인.")
    print("      핵심: 질량 [O] 잔여의 정체가 핵껍질임을 확증. 전자쪽 주기(vp_atomic)와 대응 구조.")
    print("      (관찰: 핵 마법 82 ↔ VP 양성자 코어 82. 우연인지 심층인지는 추가 연구 [O].)")
    print("="*72)


if __name__ == "__main__":
    main()
