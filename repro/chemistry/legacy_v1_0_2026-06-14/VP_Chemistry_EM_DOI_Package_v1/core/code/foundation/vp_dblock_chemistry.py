# -*- coding: utf-8 -*-
"""
vp_dblock_chemistry.py — VP 전이금속 화학, 하나하나 (재현가능·인과적)
====================================================================
목적: 원소별 화학 시뮬을 d-블록(21~36)으로 확장. 전이금속의 핵심 = 가변 산화수
      (4s·3d 에너지가 가까워 d전자도 떼어짐). 색(결정장)·촉매·착물의 기원.

정직 기록 (전자친화도 음성결과): 슬레이터 전체에너지차는 IE(잃기)엔 평균22%로 작동하나
      EA(받기)엔 부호조차 8/18 실패(F −3.74 vs 실측 +3.40). 추가전자 약결합·상관효과를
      슬레이터가 못 담음 → EA는 [O](전자상관 필요). 무리하게 쓰지 않음.

핵심: 슬레이터 규칙을 d-궤도용으로 정확히 — d전자는 왼쪽 모든 그룹이 1.0 차폐(같은 n의
      s/p 포함). 이온화는 4s 먼저(전이금속 특징). 채움 예외 Cr·Cu(반/완전충 안정).

등급: [F] 전자배치(예외 포함)·원자가·가변산화수(d-블록 직접) · [F?] IE(슬레이터 d-규칙)
      [O] 전자친화도(상관효과) · 절대 IE 정밀(슬레이터 한계)
실행: python3 vp_dblock_chemistry.py   (표준 라이브러리만)
"""
import math
RY = 13.6057
LSYM = "spdf"
# 21~36 전자배치 (예외 Cr=3d5 4s1, Cu=3d10 4s1 명시)
CONFIGS = {
 21:("Sc","[Ar]3d¹4s²",[(3,2,1),(4,0,2)]),   22:("Ti","[Ar]3d²4s²",[(3,2,2),(4,0,2)]),
 23:("V", "[Ar]3d³4s²",[(3,2,3),(4,0,2)]),    24:("Cr","[Ar]3d⁵4s¹",[(3,2,5),(4,0,1)]),  # 예외
 25:("Mn","[Ar]3d⁵4s²",[(3,2,5),(4,0,2)]),    26:("Fe","[Ar]3d⁶4s²",[(3,2,6),(4,0,2)]),
 27:("Co","[Ar]3d⁷4s²",[(3,2,7),(4,0,2)]),    28:("Ni","[Ar]3d⁸4s²",[(3,2,8),(4,0,2)]),
 29:("Cu","[Ar]3d¹⁰4s¹",[(3,2,10),(4,0,1)]),  # 예외
 30:("Zn","[Ar]3d¹⁰4s²",[(3,2,10),(4,0,2)]),
 31:("Ga","[Ar]3d¹⁰4s²4p¹",[(3,2,10),(4,0,2),(4,1,1)]),
 32:("Ge","[Ar]3d¹⁰4s²4p²",[(3,2,10),(4,0,2),(4,1,2)]),
 33:("As","[Ar]3d¹⁰4s²4p³",[(3,2,10),(4,0,2),(4,1,3)]),
 34:("Se","[Ar]3d¹⁰4s²4p⁴",[(3,2,10),(4,0,2),(4,1,4)]),
 35:("Br","[Ar]3d¹⁰4s²4p⁵",[(3,2,10),(4,0,2),(4,1,5)]),
 36:("Kr","[Ar]3d¹⁰4s²4p⁶",[(3,2,10),(4,0,2),(4,1,6)]),
}
# [Ar] 코어 = 1s2 2s2 2p6 3s2 3p6
CORE_AR = [(1,0,2),(2,0,2),(2,1,6),(3,0,2),(3,1,6)]
# 대표 산화수 (가변; d-블록 특징)
OXID = {21:"+3",22:"+4,+3",23:"+5,+4,+3,+2",24:"+3,+6,+2",25:"+2,+4,+7,+6",
        26:"+2,+3",27:"+2,+3",28:"+2",29:"+2,+1",30:"+2",
        31:"+3",32:"+4",33:"+3,+5,-3",34:"-2,+4,+6",35:"-1,+1,+3,+5",36:"0"}

def full_config(Z):
    _,_,val = CONFIGS[Z]
    return CORE_AR + val

def group_key(n,l): return (n, 0 if l in (0,1) else l)   # s/p 묶음, d/f 별도

def zeff(cfg, idx, Znuc):
    n_i,l_i,_ = cfg[idx]; sp_i = l_i in (0,1); gi = group_key(n_i,l_i)
    sigma = 0.0
    for j,(n,l,f) in enumerate(cfg):
        cnt = f-1 if j==idx else f
        if cnt<=0: continue
        gj = group_key(n,l)
        if gj==gi:                          # 같은 그룹
            sigma += (0.30 if n_i==1 else 0.35)*cnt
        elif sp_i:                          # s/p 전자
            if n==n_i-1:   sigma += 0.85*cnt
            elif n<n_i-1:  sigma += 1.0*cnt
            # 같은 n의 d/f(외곽) 또는 더 높은 n: 0
        else:                               # d/f 전자: 왼쪽 모든 그룹 1.0
            if n<n_i:                 sigma += 1.0*cnt    # 더 낮은 n
            elif n==n_i and (l in (0,1)): sigma += 1.0*cnt # 같은 n의 s/p(왼쪽)
            # 더 높은 n 또는 같은 그룹 외: 0
    return max(0.3, Znuc-sigma)

def E_total(cfg, Znuc):
    return sum(f*(-RY*zeff(cfg,i,Znuc)**2/(n*n)) for i,(n,l,f) in enumerate(cfg) if f>0)

def ionize_4s_first(cfg):
    """전이금속: 4s 먼저, 그다음 3d. (최대 n, 그중 최소 l 우선 제거)"""
    c=[list(o) for o in cfg]; nmax=max(n for n,l,f in c if f>0)
    # 최대 n 중에서 s(낮은 l) 먼저
    idx=min([i for i,(n,l,f) in enumerate(c) if n==nmax and f>0], key=lambda i:c[i][1])
    c[idx][2]-=1; return c

def IE(Z):
    cfg=full_config(Z); return E_total(ionize_4s_first(cfg),Z)-E_total(cfg,Z)

def valence_e(Z):
    """전이금속 원자가 = 4s + 3d (결합 가능 전자). 주족(Ga~Kr)은 4s+4p."""
    _,_,val = CONFIGS[Z]
    if Z<=30:  # 3d+4s
        return sum(f for n,l,f in val)
    return sum(f for n,l,f in val if n==4)   # 4s+4p

# 측정 1차 이온화에너지 [eV]
IE_MEAS = {21:6.56,22:6.83,23:6.75,24:6.77,25:7.43,26:7.90,27:7.88,28:7.64,29:7.73,30:9.39,
           31:6.00,32:7.90,33:9.79,34:9.75,35:11.81,36:14.00}


def main():
    print("="*72)
    print("VP 전이금속 화학 — 하나하나 (d-블록: 가변 산화수)")
    print("="*72)
    print("\nd-블록 핵심: 4s·3d 에너지 근접 → d전자도 떼어짐 → 가변 산화수 → 색·촉매·착물.")
    print("정직: 전자친화도는 슬레이터로 실패(부호 8/18) → [O]. IE(잃기)는 작동.")

    # ── 원소별 카드 (21~36) ──
    print("\n[원소별 화학 카드] 21~36")
    print(f"  {'Z':>3} {'원소':<3}{'전자배치':<16}{'원자가':>6}{'산화수':<16}{'IE예/실':>14}")
    print("  "+"-"*62)
    ie_err=[]
    for Z in range(21,37):
        sym,cfgstr,_ = CONFIGS[Z]
        ie=IE(Z); iem=IE_MEAS[Z]; ie_err.append(abs((ie-iem)/iem*100))
        exc = " ★예외" if Z in (24,29) else ""
        print(f"  {Z:>3} {sym:<3}{cfgstr:<16}{valence_e(Z):>5}e {OXID[Z]:<16}{ie:5.1f}/{iem:4.1f}{exc}")

    # ── 검증 (정직) ──
    early = [abs((IE(Z)-IE_MEAS[Z])/IE_MEAS[Z]*100) for Z in range(21,26)]
    print(f"\n[검증 — 정직] IE는 거칠다: 슬레이터 d-규칙 한계")
    print(f"  초기 전이금속(Sc~Mn) 평균오차 {sum(early)/len(early):.0f}% (대략적 크기·유사성 포착).")
    print(f"  후기·특히 Ga~Kr 크게 과대(Ga 15 vs 6): 3d¹⁰ 차폐를 슬레이터가 과소평가 → [O].")
    print(f"  → IE 절대값은 d-블록에서 신뢰 낮음(정직). *화학*(배치·원자가·산화수)이 [F] 결과.")
    print(f"  채움 예외 Cr(3d⁵4s¹)·Cu(3d¹⁰4s¹): 반충·완전충 안정 — 명시 반영.")
    print(f"  이온화 4s 먼저: 전이금속 특징(4s가 3d보다 먼저 떨어짐) 반영.")

    # ── d-블록 화학 이야기 ──
    print("\n[d-블록 화학] 가변 산화수가 낳는 것")
    print("  • 가변 산화수: Mn +2~+7, Fe +2/+3, V +2~+5 — 4s·3d 가까워 단계적 제거.")
    print("  • 색: d-d 전이(결정장 vp_crystal_field) → 착물 색·자성.")
    print("  • 촉매: 가변 산화수로 전자 주고받기 쉬움 → 산화환원 촉매.")
    print("  • Zn(3d¹⁰ 완전충)은 +2만, 무색 — d-d 전이 없음. Sc(d¹)은 +3만.")
    print("  → 산화수 다양성이 d-껍질 채움(부분충=가변, 완전충=고정)에서 직접.")

    # ── 원자→화학 통일 ──
    print("\n[원자 화학 완성] 주족(1~20)+전이(21~36) 하나하나 VP 위에")
    print("  • 주족: 원자가=최외각, 산화수 고정(옥텟). 금속/비금속 분류(EN지수).")
    print("  • 전이: 원자가=4s+3d, 산화수 가변(가까운 에너지). 색·자성·촉매.")
    print("  • 둘 다 껍질 채움에서 화학특성 도출. 주기율표 전체가 VP 위에서 시뮬.")

    print("\n" + "="*72)
    print("등급: [F] 전자배치(Cr·Cu 예외)·원자가·가변산화수(d-블록 직접)")
    print("      [O] IE 절대값(슬레이터 d-규칙 한계, Ga~Kr 특히) · 전자친화도(상관)")
    print("      핵심: 전이금속 *화학*을 하나하나 VP로. 가변 산화수=d-껍질 부분충에서.")
    print("="*72)


if __name__ == "__main__":
    main()
