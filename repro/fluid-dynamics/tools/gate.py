#!/usr/bin/env python3
# tools/gate.py — VP-SPEC Phase 0 tool 4/4. 8장 게이트 일괄 판정 → reports/*.gate.json
# 사용: python3 tools/gate.py --phase 1 --paper physics
import re, os, sys, csv, json, glob, hashlib, argparse
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import inventory as inv

def tools_sha():
    h=hashlib.sha256()
    for f in sorted(glob.glob("tools/*")):
        if not os.path.isfile(f): continue
        h.update(open(f,"rb").read())
    return h.hexdigest()[:16]

def read_manifest(p):
    return list(csv.DictReader(open(f"manifest/{p}.csv",encoding="utf-8")))

def main_block(html):
    m=re.search(r"<main>(.*)</main>",html,re.S)
    return m.group(1) if m else html

def words_of(html):
    t=main_block(html)
    t=re.sub(r"<aside.*?</aside>","",t,flags=re.S)
    t=re.sub(r'<p class="answer".*?</p>',"",t,flags=re.S)   # v1.8 §6/6-R: answer-first excluded from body words
    t=re.sub(r'<p class="abstract".*?</p>',"",t,flags=re.S)
    t=re.sub(r"<h1>.*?</h1>","",t,flags=re.S)
    t=re.sub(r'<nav class="pn">.*?</nav>',"",t,flags=re.S)
    t=re.sub(r"<[^>]+>"," ",t)
    return inv.word_count(t)

def phase1(p,rep):
    rows=read_manifest(p); ok=True
    dirs=[d for d in sorted(os.listdir(f"docs/{p}")) if os.path.isdir(f"docs/{p}/{d}")]
    c={"sections_manifest":len(rows),"sections_dirs":len(dirs)}
    ok &= len(rows)==len(dirs)
    per=[]; tot_disp=0; viol=[]
    for r in rows:
        f=f"docs/{p}/{r['slug']}/index.html"
        if not os.path.exists(f): per.append({"slug":r["slug"],"err":"missing"}); ok=False; continue
        h=open(f,encoding="utf-8").read()
        nd=h.count("data-eq="); nf=h.count('<figure class="fig"'); nt=h.count("<table")
        kat=h.count('class="katex'); size=len(h.encode()); dom=h.count("<")
        w=words_of(h); wm=int(r["words"]); dw=abs(w-wm)/max(wm,1)
        bad=[]
        if nd!=int(r["eq_display"]): bad.append(f"display {nd}!={r['eq_display']}")
        if nf!=int(r["figures"]): bad.append(f"fig {nf}!={r['figures']}")
        if nt!=int(r["tables"]): bad.append(f"tab {nt}!={r['tables']}")
        if kat: bad.append("katex-residue")
        if size>300*1024: bad.append(f"size {size}")
        if dom>3000: bad.append(f"dom {dom}")
        if dw>0.005: bad.append(f"words {w} vs {wm}")
        tot_disp+=int(r["eq_display"])
        if bad: viol.append({"slug":r["slug"],"bad":bad}); ok=False
    nsvg=len(glob.glob(f"docs/eq/{p}/*.svg"))
    pend = (nsvg==0 and tot_disp>0)
    if not pend and nsvg!=tot_disp: ok=False; viol.append({"svg":f"{nsvg}!={tot_disp}"})
    c.update(display_total=tot_disp,svg_files=nsvg,violations=viol,
             eq_inline_note="manifest와 동일 변환 라이브러리(inventory) 공유 — by construction 1:1")
    rep["phase1"]=c
    return ("PASS_WITH_PENDING_RENDER" if pend else "PASS") if ok else "FAIL"

def phase2(p,rep):
    rows=read_manifest(p); ok=True; viol=[]
    for r in rows:
        f=f"docs/{p}/{r['slug']}/index.html"; h=open(f,encoding="utf-8").read()
        t=re.search(r"<title>(.*?)</title>",h,re.S); title=t.group(1).strip() if t else ""
        subj=title.split("—")[0].strip()
        d=re.search(r'name="description" content="([^"]*)"',h); desc=d.group(1) if d else ""
        bad=[]
        if not title.endswith("| Jamming Physics") or len(subj)>45 or len(title)>90: bad.append("title")
        if not (80<=len(desc)<=160): bad.append(f"desc({len(desc)})")
        if h.count("<h1")!=1: bad.append("h1")
        ab=re.search(r'<p class="abstract"[^>]*>(.*?)</p>',h,re.S)
        # v1.7: 키피겨는 '본문(aside·DOI 링크 제외)에 대표 수치가 있을 때만' abstract 에 요구
        FIG=r"[0-9].*[=×·π/^²³⁴⁵]|[=×·π].*[0-9]"
        main_noabs=re.sub(r'<p class="abstract".*?</p>',"",main_block(h),flags=re.S)
        noaside_text=re.sub(r"<[^>]+>"," ",re.sub(r"<aside.*?</aside>","",main_noabs,flags=re.S))
        abstxt=ab.group(1) if ab else ""
        if not ab: bad.append("abstract-missing")
        elif re.search(FIG,noaside_text) and not re.search(FIG,abstxt): bad.append("abstract-texteq")
        # v1.7: 반작문 — abstract·description 의 모든 수치 토큰은 본문(전체)에 존재해야 함
        # v1.7-fix: image-rendered math keeps its numbers in <img alt="{LaTeX}">; the
        # tag-strip above discards them, so a result genuinely shown in an equation was
        # mis-flagged as fabricated. Include equation alt text in the body number set.
        eq_alt=" ".join(re.findall(r'alt="([^"]*)"',main_noabs))
        src_nums=set(re.findall(r"\d+(?:\.\d+)?",re.sub(r"<[^>]+>"," ",main_noabs)+" "+eq_alt))
        for n in set(re.findall(r"\d+(?:\.\d+)?",abstxt+" "+desc)):
            if n not in src_nums: bad.append("invent-number:"+n); break
        if 'class="claim-strip"' not in h and "claim-strip" not in h: bad.append("strip")
        w=words_of(h); wm=int(r["words"])
        if abs(w-wm)/max(wm,1)>0.005: bad.append(f"words {w}/{wm}")
        for m in re.finditer(r'href="(/[^"]+)"',h):
            path=m.group(1).split("#",1)[0]                       # v1.7-fix: strip URL fragment before path check
            if not path or path.startswith(("/assets","/eq")): continue
            tgt="docs"+path.rstrip("/")+"/index.html"
            if not os.path.exists(tgt) and not os.path.exists("docs"+path): bad.append("link:"+m.group(1)); break
        if "(Phase 2" in h: bad.append("placeholder-residue")
        if bad: viol.append({"slug":r["slug"],"bad":bad}); ok=False
    rep["phase2"]={"violations":viol}
    return "PASS" if ok else "FAIL"

def phase356(p,rep):
    ok=True; v=[]
    hub=f"docs/{p}/index.html"
    if os.path.exists(hub):
        h=open(hub,encoding="utf-8").read()
        rows=read_manifest(p)
        miss=[r["slug"] for r in rows if f'/{p}/{r["slug"]}/' not in h]
        if miss: ok=False; v.append({"hub-missing":miss[:5],"n":len(miss)})
    else: v.append({"hub":"absent (Phase 3 전)"})
    if os.path.exists("docs/sitemap.xml"):
        sm=open("docs/sitemap.xml").read().count("<loc>")
        pages=len(glob.glob("docs/**/index.html",recursive=True))
        if sm!=pages: ok=False; v.append({"sitemap":f"{sm}!={pages}"})
    rep["phase356"]={"violations":v}
    return "PASS" if ok else "FAIL"

def _strip_tags(s):
    s=re.sub(r"<[^>]+>"," ",s); return re.sub(r"\s+"," ",s).strip()

def _load_locked(p):
    fp=f"registry/locked_quantities.{p}.json"
    if not os.path.exists(fp): return []
    return json.load(open(fp,encoding="utf-8")).get("quantities",[])

def phase_search(p,rep):
    """v1.8 search gate (Constitution C4 / 6-R). hard=FAIL, soft=warn."""
    rows=read_manifest(p); ok=True; viol=[]; warn=[]
    locked=_load_locked(p)
    for r in rows:
        f=f"docs/{p}/{r['slug']}/index.html"
        if not os.path.exists(f): continue
        h=open(f,encoding="utf-8").read(); bad=[]
        am=re.search(r'<p class="answer">(.*?)</p>',h,re.S)
        if not am: bad.append("answer-missing")
        else:
            ai=h.find('<p class="answer"'); bi=h.find('<p class="abstract"')
            if bi!=-1 and ai>bi: bad.append("answer-not-first")
            wcA=len(re.findall(r"[A-Za-z0-9][A-Za-z0-9\-'’/×·]*",_strip_tags(am.group(1))))
            if not (30<=wcA<=70): warn.append({r["slug"]:f"answer-words {wcA}"})
        for q in locked:
            if q.get("home_slug")==r["slug"]: continue
            if any(pat in h for pat in q["match"]) and f'data-locked="{q["id"]}"' not in h:
                bad.append("vp-card-missing:"+q["id"])
        if "0009-0002-7535-8245" not in h: bad.append("jsonld-orcid")
        if "doi.org/10.5281" not in h and "zenodo" not in h: bad.append("jsonld-doi")
        for m in re.finditer(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',h,re.S):
            try: json.loads(m.group(1))
            except Exception: bad.append("jsonld-invalid"); break
        body=re.sub(r"<aside.*?</aside>|<figure.*?</figure>","",main_block(h),flags=re.S)
        longp=sum(1 for pm in re.finditer(r"<p>(.*?)</p>",body,re.S)
                  if len(re.findall(r"[.!?](?:\s|$)",_strip_tags(pm.group(1))))>3)
        if longp: warn.append({r["slug"]:f"long-paras {longp}"})
        if bad: viol.append({"slug":r["slug"],"bad":bad}); ok=False
    hub=f"docs/{p}/index.html"
    if os.path.exists(hub):
        hh=open(hub,encoding="utf-8").read()
        if not ('"CreativeWorkSeries"' in hh or '"Book"' in hh): viol.append({"hub":"not-series"}); ok=False
        if '"BreadcrumbList"' not in hh: viol.append({"hub":"no-breadcrumb"}); ok=False
    acc=[]
    rb="docs/robots.txt"
    if not os.path.exists(rb): acc.append("robots-missing")
    else:
        rt=open(rb,encoding="utf-8").read()
        bots=["Googlebot","Bingbot","OAI-SearchBot","GPTBot","PerplexityBot","ClaudeBot","Google-Extended"]
        miss=[b for b in bots if b not in rt]
        if miss: acc.append("robots-bots:"+",".join(miss))
    sm="docs/sitemap.xml"
    if not os.path.exists(sm): acc.append("sitemap-missing")
    else:
        n=open(sm,encoding="utf-8").read().count("<loc>")
        pages=len(glob.glob("docs/**/index.html",recursive=True))
        if n!=pages: acc.append(f"sitemap-count {n}!={pages}")
    ll="docs/llms.txt"
    if not os.path.exists(ll): acc.append("llms-missing")
    elif os.path.getsize(ll)>=5*1024: acc.append(f"llms-size {os.path.getsize(ll)}")
    if acc: viol.append({"access":acc}); ok=False
    rep["search"]={"violations":viol,"warnings":warn[:40]}
    return "PASS" if ok else "FAIL"

def phase_constitution(p,rep):
    """v1.7/v1.8 constitution gate C1/C2/C3 (required before merge/release)."""
    ok=True; v=[]
    tex=[f for f in glob.glob("**/*.tex",recursive=True)]
    eql=[f for f in glob.glob("**/*.eq_list.*",recursive=True)]
    txt=[d for d in glob.glob("**/txt",recursive=True) if os.path.isdir(d)]
    c2=[]
    if tex: c2.append({"tex":tex[:5]})
    if eql: c2.append({"eq_list":eql[:5]})
    if txt: c2.append({"txt_dirs":txt[:5]})
    if c2: ok=False; v.append({"C2":c2})
    rows=read_manifest(p); c1=[]; tot_dataeq=0
    for r in rows:
        f=f"docs/{p}/{r['slug']}/index.html"
        if not os.path.exists(f): continue
        h=open(f,encoding="utf-8").read()
        nd=h.count("data-eq="); tot_dataeq+=nd
        w=words_of(h); wm=int(r["words"])
        if abs(w-wm)/max(wm,1)>0.005: c1.append({r["slug"]:f"words {w}/{wm}"})
        if nd!=int(r["eq_display"]): c1.append({r["slug"]:f"data-eq {nd}/{r['eq_display']}"})
    nsvg=len(glob.glob(f"docs/eq/{p}/*.svg"))
    if tot_dataeq!=nsvg: c1.append({"orphan":f"data-eq sum {tot_dataeq} != display svg {nsvg}"})
    meta=f"docs/{p}/_meta.json"
    if os.path.exists(meta):
        md=json.load(open(meta,encoding="utf-8"))
        man_w=sum(int(r["words"]) for r in rows)
        meta_w=(md.get("totals") or {}).get("words")
        if meta_w is not None and man_w and abs(meta_w-man_w)/man_w>0.05:
            c1.append({"_meta.totals.words":f"{meta_w} vs manifest {man_w}"})
    if c1: ok=False; v.append({"C1":c1})
    led="IRREPRODUCIBILITY_LEDGER.md"; c3=[]; o_pages=[]
    for r in rows:
        f=f"docs/{p}/{r['slug']}/index.html"
        if os.path.exists(f) and re.search(r"\[O\]",open(f,encoding="utf-8").read()):
            o_pages.append(r["slug"])
    if not os.path.exists(led): c3.append("ledger-missing")
    else:
        lt=open(led,encoding="utf-8").read()
        for s in o_pages:
            if s not in lt: c3.append("O-not-in-ledger:"+s)
    if c3: ok=False; v.append({"C3":c3})
    rep["constitution"]={"violations":v,"O_pages":o_pages,"data_eq_sum":tot_dataeq,"display_svg":nsvg}
    return "PASS" if ok else "FAIL"


if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--phase",required=True); ap.add_argument("--paper",required=True)
    a=ap.parse_args(); rep={"phase":a.phase,"paper":a.paper,"tools_sha16":tools_sha()}
    if os.path.exists(f"src/{a.paper}"):
        for f in glob.glob(f"src/{a.paper}/*"):
            rep.setdefault("src_sha",{})[os.path.basename(f)]=hashlib.sha256(open(f,'rb').read()).hexdigest()
    v={"1":phase1,"2":phase2,"3":phase356,"5":phase356,"6":phase356,"search":phase_search,"constitution":phase_constitution}[a.phase](a.paper,rep)
    rep["verdict"]=v
    os.makedirs("reports",exist_ok=True)
    out=f"reports/phase{a.phase}-{a.paper}.gate.json"
    json.dump(rep,open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"[gate] phase{a.phase} {a.paper}: {v} → {out}")
    if v=="FAIL":
        print(json.dumps(rep.get(f"phase{a.phase}",rep),ensure_ascii=False)[:1200]); sys.exit(1)
