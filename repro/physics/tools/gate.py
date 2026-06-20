#!/usr/bin/env python3
# tools/gate.py — VP-SPEC Phase 0 tool 4/4. 8장 게이트 일괄 판정 → reports/*.gate.json
# 사용: python3 tools/gate.py --phase 1 --paper physics
# phase 4 = 수치 드리프트 게이트(SSOT: tools/vp_numeric_ssot.py). 본문/eq_list 표시값이 정준 재생성과
#           어긋나면 FAIL → 빌드 차단. +57·292.244·0.841248·k_e류 재발 방지.
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
    t=re.sub(r'<p class="answer".*?</p>',"",t,flags=re.S)   # r7(v1.8): answer-first 직답은 본문 단어수 제외(6장)
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
        # v1.7: 반작문 — abstract·description 의 모든 수치 토큰은 본문(전체)에 존재해야 함.
        # 단, 섹션 참조(§N, §N.N…)는 인용 수치가 아니라 링크 대상이므로 검사에서 제외(v1.7 헌법판 정밀화).
        src_nums=set(re.findall(r"\d+(?:\.\d+)?",re.sub(r"<[^>]+>"," ",main_noabs)))
        chk=re.sub(r"§\s*\d+(?:\.\d+)*"," ",abstxt+" "+desc)   # §-섹션 참조 제거 후 수치 추출
        for n in set(re.findall(r"\d+(?:\.\d+)?",chk)):
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

def phase4(p,rep):
    """수치 드리프트 게이트(SSOT): 정본 HTML(docs/) 표시값이 정준 재생성과 어긋나면 FAIL.
    헌법 C2(v1.7): 정본은 docs/ HTML 하나다. TeX 소스(txt/·eq_list)는 비동봉이므로
    드리프트 검사 대상은 docs/{p}/ 의 본문 텍스트 + 수식 img alt(LaTeX, =SVG의 접근성 소스)다.
    단일 진실원은 tools/vp_numeric_ssot.py. 80자리 A=cΔt/a 는 §3.4 placeholder 면책으로 제외."""
    try:
        import vp_numeric_ssot as ssot
    except Exception as e:
        rep["phase4"]={"error":f"vp_numeric_ssot import 실패: {e}"}; return "FAIL"
    viol=[]
    # (a) 정본 본문 범위만 검사: docs/{p}/ (reports·dossier 스캐폴딩 제외; txt/ 는 비동봉 → HTML이 정본)
    body=glob.glob(f"docs/{p}/*/index.html")
    for pat,bad,good,why in ssot.BAD_PATTERNS:
        rx=re.compile(pat); hits=[]
        for f in body:
            try: t=open(f,encoding="utf-8",errors="ignore").read()
            except Exception: continue
            for i,ln in enumerate(t.splitlines(),1):
                if rx.search(ln): hits.append(f"{f}:{i}")
        if hits: viol.append({"drift":bad,"fix":good,"why":why,"n":len(hits),"hits":hits[:8]}); ok=False
    # (b) 수식 소스 드리프트: 정본은 SVG, 그 접근성 소스(LaTeX)는 docs/ HTML 의 img alt 에 들어 있다.
    #     별도 TeX 소스(eq_list)는 비동봉이므로, 정본 HTML 의 alt 텍스트에서 같은 불량 리터럴을 검사한다.
    try:
        for f in body:
            try: t=open(f,encoding="utf-8",errors="ignore").read()
            except Exception: continue
            for lit,good in (("{+}57","{+}61"),("8.9875517923","8.9875517874")):
                if lit in t: viol.append({"drift_eq":lit,"fix":good,"file":f})
    except Exception as e:
        viol.append({"eq_alt_scan_error":str(e)})
    # (c) SSOT 자기검증: 재생성기가 도는가 + 핵심 잔차 일치
    try:
        q=ssot.compute()
        from decimal import Decimal as _D
        r3=(q["nu_len"]/q["nu_geo"]-1)*_D(10)**6
        if abs(r3-_D("61.2"))>_D("0.5"): viol.append({"ssot_residual_drift":str(r3)})
    except Exception as e:
        viol.append({"ssot_compute_error":str(e)})
    rep["phase4"]={"scope":"docs/%s/ (정본 HTML 본문 + 수식 img alt; TeX 소스 비동봉 — 헌법 C2)"%p,"violations":viol,
        "note":"정준입력 결정론 재생성 대비 표시 드리프트 (vp_numeric_ssot.py SSOT; A=cΔt/a placeholder 면책 제외)"}
    return "PASS" if not viol else "FAIL"

def phase_search(p,rep):
    """8장 검색 게이트(v1.8): C4 검색 수용성. answer-first·자체완결 vp-card·JSON-LD·기계 접근을 판정.
    BINDING: answer-first 존재, 인용 잠금마다 vp-card(맨-참조 0), JSON-LD 유효(장=ScholarlyArticle·
             용어=DefinedTerm 허브=CreativeWorkSeries/Book+BreadcrumbList), sameAs(ORCID·DOI),
             robots.txt(7봇)+sitemap.xml+llms.txt(<5KB).  SOFT: answer 40~60단어, 단락 ≤3문장.
    봉인 색인/부록 페이지는 작문 없이 40단어를 채울 수 없으므로 WARN(자체완결성은 유지)."""
    ok=True; viol=[]; soft=[]
    ORCID="0009-0002-7535-8245"; DOI="10.5281/zenodo.17932566"
    BOTS=["Googlebot","Bingbot","OAI-SearchBot","GPTBot","PerplexityBot","ClaudeBot","Google-Extended"]
    # 잠금 레지스트리(자체완결 카드 판정의 단일 출처)
    locks=[]
    lp="registry/vp_locks.csv"
    if os.path.exists(lp):
        locks=list(csv.DictReader(open(lp,encoding="utf-8")))
    else:
        viol.append({"registry":"registry/vp_locks.csv 없음 — vp-card 판정 불가"}); ok=False

    rows=read_manifest(p)
    a_present=0; a_inband=0; cards_total=0
    SENT=re.compile(r"[.!?。]\s")
    for r in rows:
        slug=r["slug"]; f=f"docs/{p}/{slug}/index.html"
        if not os.path.exists(f): viol.append({"slug":slug,"err":"missing"}); ok=False; continue
        h=open(f,encoding="utf-8").read()
        body=main_block(h)
        # (1) answer-first 직답
        am=re.search(r'<p class="answer"[^>]*>(.*?)</p>',h,re.S)
        if not am: viol.append({"slug":slug,"bad":"answer-first 없음"}); ok=False
        else:
            a_present+=1
            aw=len(re.sub(r"<[^>]+>"," ",am.group(1)).split())
            if 40<=aw<=60: a_inband+=1
            elif aw<12: viol.append({"slug":slug,"bad":f"answer 과소({aw}w)"}); ok=False
            else: soft.append({"slug":slug,"answer_words":aw,"note":"봉인 색인/부록 — 작문 없이 40~60 불가"})
        # (2) 자체완결: 인용된 잠금마다 vp-card 존재(자기-정준 섹션은 면제). 맨-참조 금지.
        locked_ids=set(re.findall(r'data-locked="([^"]+)"',h))
        cards_total+=len(re.findall(r'<aside class="vp-card"',h))
        for L in locks:
            tok=L["match_token"]; cid=L["lock_id"]
            if tok and tok in body and slug!=L["canon_slug"]:
                if cid not in locked_ids:
                    viol.append({"slug":slug,"bad":f"인용 잠금 '{cid}'({tok}) self-contained 카드 없음"}); ok=False
        # (3) JSON-LD: 장=ScholarlyArticle + BreadcrumbList
        if '"ScholarlyArticle"' not in h: viol.append({"slug":slug,"bad":"JSON-LD ScholarlyArticle 없음"}); ok=False
        if '"BreadcrumbList"' not in h: viol.append({"slug":slug,"bad":"BreadcrumbList 없음"}); ok=False
        if ORCID not in h: viol.append({"slug":slug,"bad":"sameAs ORCID 없음"}); ok=False
        if DOI not in h: soft.append({"slug":slug,"note":"DOI 미기재(장 단위 — 소프트)"})
        # (S) 단락 길이 소프트: 본문 <p>(answer/abstract 제외)가 대체로 ≤3문장인가
        bod=re.sub(r"<aside.*?</aside>","",body,flags=re.S)
        for pm in re.findall(r'<p(?! class="(?:answer|abstract)")[^>]*>(.*?)</p>',bod,re.S):
            txt=re.sub(r"<[^>]+>"," ",pm).strip()
            if len(SENT.findall(txt))>=4: soft.append({"slug":slug,"long_para":txt[:60]+"…"}); break

    # (3b) 허브 JSON-LD: CreativeWorkSeries/Book + BreadcrumbList
    hub=f"docs/{p}/index.html"
    if os.path.exists(hub):
        hh=open(hub,encoding="utf-8").read()
        if not ('"CreativeWorkSeries"' in hh or '"Book"' in hh):
            viol.append({"hub":"CreativeWorkSeries/Book JSON-LD 없음"}); ok=False
        if '"BreadcrumbList"' not in hh: viol.append({"hub":"BreadcrumbList 없음"}); ok=False
        if ORCID not in hh: viol.append({"hub":"sameAs ORCID 없음"}); ok=False
    else:
        viol.append({"hub":"absent"}); ok=False

    # (4) 기계 접근 파일
    rb="docs/robots.txt"
    if os.path.exists(rb):
        rbt=open(rb,encoding="utf-8").read()
        miss=[b for b in BOTS if not re.search(r"User-agent:\s*"+re.escape(b),rbt,re.I)]
        if miss: viol.append({"robots_missing_bots":miss}); ok=False
        if "Sitemap:" not in rbt: viol.append({"robots":"Sitemap: 라인 없음"}); ok=False
    else: viol.append({"robots.txt":"없음"}); ok=False
    sm="docs/sitemap.xml"
    if os.path.exists(sm):
        nloc=open(sm,encoding="utf-8").read().count("<loc>")
        npg=len(glob.glob("docs/**/index.html",recursive=True))
        if nloc!=npg: viol.append({"sitemap_loc":f"{nloc}!={npg}"}); ok=False
    else: viol.append({"sitemap.xml":"없음"}); ok=False
    lt="docs/llms.txt"
    if os.path.exists(lt):
        sz=os.path.getsize(lt)
        if sz>5120: viol.append({"llms.txt":f"{sz}B > 5KB"}); ok=False
    else: viol.append({"llms.txt":"없음"}); ok=False

    rep["search"]={"answer_first":f"{a_present}/{len(rows)}","answer_in_40_60":f"{a_inband}/{len(rows)}",
                   "vp_cards_total":cards_total,"violations":viol,"soft":soft[:40],
                   "criteria":"v1.8 8장: answer-first·self-contained vp-card·JSON-LD·robots/sitemap/llms"}
    return "PASS" if ok else "FAIL"

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--phase",required=True); ap.add_argument("--paper",required=True)
    a=ap.parse_args(); rep={"phase":a.phase,"paper":a.paper,"tools_sha16":tools_sha()}
    if os.path.exists(f"src/{a.paper}"):
        for f in glob.glob(f"src/{a.paper}/*"):
            rep.setdefault("src_sha",{})[os.path.basename(f)]=hashlib.sha256(open(f,'rb').read()).hexdigest()
    v={"1":phase1,"2":phase2,"3":phase356,"4":phase4,"5":phase356,"6":phase356,"search":phase_search}[a.phase](a.paper,rep)
    rep["verdict"]=v
    os.makedirs("reports",exist_ok=True)
    out=f"reports/phase{a.phase}-{a.paper}.gate.json"
    json.dump(rep,open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"[gate] phase{a.phase} {a.paper}: {v} → {out}")
    if v=="FAIL":
        print(json.dumps(rep.get(f"phase{a.phase}",rep),ensure_ascii=False)[:1200]); sys.exit(1)
