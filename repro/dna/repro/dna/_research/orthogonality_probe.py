#!/usr/bin/env python3
# =============================================================================
#  orthogonality_probe.py  --  1차 조사 (재현 가능)
#  "버려지는 서열 피처(CpG-섬/위치 구조)가 γ(=GC)와 독립된 신호를 담는가?"
#
#  실행: 키트 루트에서  python3 orthogonality_probe.py
#  입력: repro/dna/_engine/*promoters.cache.json (원서열) +
#        repro/dna/_verify/inputs/sequences_v6/*.fa
#  결정성: 순수 산술. 외부 의존 numpy만.
# =============================================================================
import json, glob, os
import numpy as np

# 프레임워크와 '동일한' SantaLucia 1998 NN dG37 — γ = mean(-NN dG)
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

def gamma(s):
    v = [-NN[s[i:i+2]] for i in range(len(s)-1) if s[i:i+2] in NN]
    return float(np.mean(v)) if v else float("nan")

def cpg_oe(s):
    """CpG observed/expected (Gardiner-Garden & Frommer) — 섬 신호. GC와 별개."""
    L=len(s); nC=s.count("C"); nG=s.count("G"); nCpG=s.count("CG")
    return (nCpG*L)/(nC*nG) if nC and nG else 0.0

def gc(s): return (s.count("C")+s.count("G"))/len(s)

def win_gamma_std(s, W=250):
    """프로모터 '내부' 창간 γ 변동 — 단일 평균이 지우는 위치 구조."""
    wins=[]
    for i in range(0, len(s)-W, W):
        w=s[i:i+W]
        if w.count("N") < W*0.1:
            gv=gamma(w)
            if gv==gv: wins.append(gv)
    return float(np.std(wins)) if len(wins)>=2 else None

def is_island(s): return gc(s)>=0.50 and cpg_oe(s)>=0.60

def is_dna(x): return isinstance(x,str) and len(x)>300 and set(x.upper())<=set("ACGTN")

def load(root="."):
    seqs=[]
    for f in glob.glob(os.path.join(root,"repro/dna/_engine/*promoters.cache.json")):
        for k,v in json.load(open(f)).items():
            if is_dna(v):
                seqs.append((k.split("|")[-1], v.upper(), os.path.basename(f).split("_")[0]))
    for fa in glob.glob(os.path.join(root,"repro/dna/_verify/inputs/sequences_v6/*.fa")):
        s="".join(l.strip() for l in open(fa) if not l.startswith(">")).upper()
        if is_dna(s): seqs.append((os.path.basename(fa)[:-3], s, "seqv6"))
    return seqs

def C(a,b): return float(np.corrcoef(a,b)[0,1])

def main(root="."):
    seqs=load(root); n=len(seqs)
    g  = np.array([gamma(s) for _,s,_ in seqs])
    GC = np.array([gc(s)    for _,s,_ in seqs])
    OE = np.array([cpg_oe(s) for _,s,_ in seqs])
    isl= np.array([is_island(s) for _,s,_ in seqs])
    print(f"N = {n} 프로모터\n")

    print("[1] γ는 GC의 재명명인가  (소스별 vs 풀링)")
    bysrc={}
    for _,s,src in seqs: bysrc.setdefault(src,[]).append(s)
    for src,ss in bysrc.items():
        if len(ss)>3:
            gg=[gamma(x) for x in ss]; cc=[gc(x) for x in ss]
            r=C(gg,cc); print(f"    {src:<8} n={len(ss):>3}  corr={r:+.3f}  R²={r*r*100:3.0f}%")
    r=C(g,GC); print(f"    {'POOLED':<8} n={n:>3}  corr={r:+.3f}  R²={r*r*100:3.0f}%"
                     f"   → γ의 비-GC 정보 {100-r*r*100:.0f}%\n")

    print("[2] 메틸화-섬 신호(CpG O/E)는 γ/GC와 독립인가  ★핵심★")
    print(f"    corr(CpG O/E, GC) = {C(OE,GC):+.4f}   (≈0 → 완전 직교)")
    print(f"    corr(CpG O/E, γ ) = {C(OE,g):+.4f}   (R²={C(OE,g)**2*100:.0f}% → γ가 못 담는 {100-C(OE,g)**2*100:.0f}%)\n")

    print("[3] '동일 γ, 다른 메틸화 클래스' 쌍이 실재하는가")
    idx=np.argsort(g); pairs=[]
    for i in range(n-1):
        a,b=seqs[idx[i]],seqs[idx[i+1]]; dg=abs(g[idx[i]]-g[idx[i+1]])
        if dg<0.01:
            pairs.append((abs(OE[idx[i]]-OE[idx[i+1]]),dg,a,b,OE[idx[i]],OE[idx[i+1]]))
    pairs.sort(reverse=True)
    print(f"    {'A':<14}{'B':<14}{'|Δγ|':>7}{'O/E_A':>7}{'O/E_B':>7}")
    for d,dg,a,b,oa,ob in pairs[:5]:
        print(f"    {a[0]:<14}{b[0]:<14}{dg:>7.4f}{oa:>7.2f}{ob:>7.2f}")
    print()

    print("[4] 단일 평균 γ가 서열 '내부' 위치 구조를 지우는가")
    ws=np.array([x for x in (win_gamma_std(s) for _,s,_ in seqs) if x is not None])
    print(f"    내부 창간 γ std 중앙값 = {np.median(ws):.4f}  (종간 야드스틱 0.026)")
    print(f"    내부 변동 > 야드스틱 비율 = {np.mean(ws>0.026)*100:.0f}%  ·  90분위 = {np.percentile(ws,90):.4f}\n")

    print("[5] 서열로 바로 읽히는데 안 쓰는 메틸화-민감 클래스")
    print(f"    CpG-섬 {int(isl.sum())}/{n} ({isl.mean()*100:.0f}%)  ·  비섬 {n-int(isl.sum())}/{n}")
    print(f"    → 현재 동역학(core.sdot)이 사용하는 횟수: 0\n")

    print("결론(1차): γ는 'GC+이염기순서'이나 여전히 위치맹 스칼라. 메틸화-섬/위치 층은")
    print("γ와 직교하며 현재 전량 폐기됨. 단, '직교'는 '비중복'을 뜻할 뿐 '예측력 향상'을")
    print("보장하지 않음 — 그 검증이 심층연구의 과제(워크스트림 A/B).")

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else ".")
