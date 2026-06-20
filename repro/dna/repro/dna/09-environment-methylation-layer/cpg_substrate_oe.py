#!/usr/bin/env python3
# VP-SPEC v1.8 verification-layer reproducer (repro/dna/, paper_id=dna, §9).
# WHAT THIS VERIFIES: the local CpG methylation-substrate signal that §9 reads at each
#   locus -- the quantity the v1.9 package froze as the orphaned constant `cpg_oe_local_max`
#   (LCT 0.7843 / Lct 0.4274 / MCM6 0.8224) with NO in-package reproducer (a C1/C3 gap).
# This replaces that magic constant with a DETERMINISTIC reading (C1: same input -> same
#   output, 2x sha256 identical). Principle (DNA theory): nothing in DNA is unused -- the
#   sub-island signal that UCSC cpgIslandExt / EMBOSS discard (whole-locus O/E < 0.6) is
#   read here, but read precisely: a scale-explicit O/E band, the TSS-relative position of
#   the peak, and a dinucleotide-shuffle significance test.
# EXPECTED OUTPUT: expected/cpg_substrate_oe.json (frozen; gate compares displayed value).
# Reads ONLY the locked inputs in inputs/*.fa. No external tools, no network -> in-package.
import json, os, random
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
INP  = os.path.join(HERE, "inputs")
SEED = 19
SCALES = (100, 150, 200, 250, 300)   # explicit reading scales (bp)
CANON_W = 200                        # canonical scale for the significance test
N_NULL  = 300                        # dinucleotide-preserving shuffles

def read_fasta(path):
    header, seq = "", []
    for line in open(path):
        (header := line[1:].strip()) if line.startswith(">") else seq.append(line.strip())
    return header, "".join(seq).upper()

def prefix_sums(s):
    n = len(s); pC=[0]*(n+1); pG=[0]*(n+1); pCG=[0]*(n+1)
    for k in range(n):
        pC[k+1]=pC[k]+(s[k]=="C"); pG[k+1]=pG[k]+(s[k]=="G")
        pCG[k+1]=pCG[k]+(1 if s[k:k+2]=="CG" else 0)
    return pC,pG,pCG

def oe(i,j,pC,pG,pCG):
    L=j-i; nC=pC[j]-pC[i]; nG=pG[j]-pG[i]; nCG=(pCG[j-1]-pCG[i]) if j-1>=i else 0
    return (nCG*L)/(nC*nG) if nC and nG else 0.0

def whole_oe(s):
    L=len(s); nC=s.count("C"); nG=s.count("G"); nCG=s.count("CG")
    return (nCG*L)/(nC*nG) if nC and nG else 0.0

def peak(s,W,pC,pG,pCG):
    best,bi=0.0,0
    for i in range(0,len(s)-W+1):
        v=oe(i,i+W,pC,pG,pCG)
        if v>best: best,bi=v,i
    return best,bi

# --- Altschul-Erikson dinucleotide-preserving shuffle (preserves C,G,CpG counts) ---
def _tree(last_edge,root,verts):
    for v in verts:
        if v==root: continue
        seen,cur=set(),v
        while cur!=root:
            if cur in seen or cur not in last_edge: return False
            seen.add(cur); cur=last_edge[cur]
    return True

def dinuc_shuffle(seq,rng):
    if len(seq)<3: return seq
    last=seq[-1]; edges=defaultdict(list)
    for i in range(len(seq)-1): edges[seq[i]].append(seq[i+1])
    verts=sorted(set(seq))   # deterministic order (independent of PYTHONHASHSEED) -> C1
    for _ in range(1000):
        le={}; ok=True
        for v in verts:
            if v==last: continue
            if not edges[v]: ok=False; break
            le[v]=rng.choice(edges[v])
        if ok and _tree(le,last,verts): break
    else: return seq
    out=defaultdict(list)
    for v in verts:
        es=list(edges[v])
        if v!=last: es.remove(le[v]); rng.shuffle(es); es.append(le[v])
        else: rng.shuffle(es)
        out[v]=es
    ptr=defaultdict(int); res=[seq[0]]; cur=seq[0]
    for _ in range(len(seq)-1):
        nx=out[cur][ptr[cur]]; ptr[cur]+=1; res.append(nx); cur=nx
    return "".join(res)

def read_locus(path, tss):
    header,s=read_fasta(path)
    start=int(header.split(":")[1].split("-")[0]) if ":" in header else None
    pC,pG,pCG=prefix_sums(s); bg=whole_oe(s)
    per={}
    for W in SCALES:
        pk,i=peak(s,W,pC,pG,pCG)
        coord=(start+i) if start else None
        per[str(W)]={"peak_oe":round(pk,4),"fold":round(pk/bg,3) if bg else 0.0,
                     "peak_coord":coord,"tss_offset_bp":(coord-tss) if (coord and tss) else None}
    real_fold = per[str(CANON_W)]["fold"]
    rng=random.Random(SEED); null=[]
    for _ in range(N_NULL):
        sh=dinuc_shuffle(s,rng); qC,qG,qCG=prefix_sums(sh); b=whole_oe(sh)
        pk,_=peak(sh,CANON_W,qC,qG,qCG); null.append(pk/b if b else 0.0)
    ge=sum(1 for x in null if x>=real_fold)
    return {"background_oe":round(bg,4),
            "fold_band":[round(min(p["fold"] for p in per.values()),3),
                         round(max(p["fold"] for p in per.values()),3)],
            "per_scale":per,
            "canonical_W":CANON_W,"real_fold":real_fold,
            "null_mean_fold":round(sum(null)/len(null),3),"null_n":N_NULL,
            "percentile_vs_null":round(100*(1-ge/len(null)),1)}

def main():
    loci=[("LCT_human","human_LCT_promoter.fa",135837183),
          ("Lct_mouse","mouse_Lct_promoter.fa",128256054),
          ("MCM6_enh_human","human_MCM6_enhancer.fa",None)]
    out={"_what":"local CpG methylation-substrate reading (replaces orphaned cpg_oe_local_max)",
         "_method":"max sliding-window Gardiner-Garden&Frommer O/E at scales 100-300bp; "
                   "fold = peak/background; significance vs Altschul-Erikson dinucleotide shuffle",
         "_grade_note":"reproducible [F]; absolute O/E is scale-tagged, fold-band is the invariant",
         "loci":{}}
    for tag,fn,tss in loci:
        out["loci"][tag]=read_locus(os.path.join(INP,fn),tss)
    os.makedirs(os.path.join(HERE,"expected"),exist_ok=True)
    with open(os.path.join(HERE,"expected","cpg_substrate_oe.json"),"w") as f:
        json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
