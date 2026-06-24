#!/usr/bin/env python3
"""tools/gate.py — final audit harness for the VP consolidated repo.
Run from the repo root. Exit 0 if no FAIL, 1 otherwise. WARN = human review.
"""
import json, re, os, glob, hashlib, csv, sys

DOCS="docs"; REG="registry"
ORDER=['physics','fluid-dynamics','cosmology','chemistry','geodynamics','geochronology',
 'continental-genesis-cascade',
 'wave-computer','dna','inheritance','neuro','mind','sensory_organ','eye','ear','nose',
 'cardioresp','circulatory','digestive','musculoskeletal','immune_hematologic','integumentary',
 'reproductive_endocrine','homeostasis_thermometabolic','homeostasis_hemodynamic',
 'homeostasis_ionic','circadian','aging_senescence','analgesic_threshold','disease_wp','disease_kit']
EXPECT=set(ORDER)
R=[]  # (status, name, detail)
def ok(n,d=""):  R.append(("PASS",n,d))
def warn(n,d=""):R.append(("WARN",n,d))
def bad(n,d=""): R.append(("FAIL",n,d))

def sha(b): return hashlib.sha256(b).hexdigest()
def dirhash(base):
    if not os.path.isdir(base): return None
    parts=[]
    for f in sorted(glob.glob(os.path.join(base,"**","*"),recursive=True)):
        if os.path.isfile(f):
            parts.append(os.path.relpath(f,base)+":"+sha(open(f,"rb").read()))
    return sha("\n".join(parts).encode())

man=json.load(open(f"{REG}/vp.manifest.json"))
MV={v['id']:v for v in man['volumes']}
page=open(f"{DOCS}/index.html",encoding="utf-8").read()
agents=open("AGENTS.md",encoding="utf-8").read() if os.path.exists("AGENTS.md") else ""

# ---- A. slug-set consistency across 6 surfaces ----
surf={}
surf['docs_hubs']=set(d for d in EXPECT if os.path.isfile(f"{DOCS}/{d}/index.html"))
surf['manifest']=set(MV)
surf['repro']=set(d for d in EXPECT if os.path.isdir(f"repro/{d}"))
surf['homepage_cards']=set(re.findall(r'href="/([a-z0-9_-]+)/"',page)) & EXPECT
try:
    rows=list(csv.reader(open(f"{REG}/nodes.csv")))
    surf['registry']=set(r[0] for r in rows[1:] if r and r[0] in EXPECT)
except Exception as e:
    surf['registry']=set(); warn("registry read",str(e))
llms=open(f"{DOCS}/llms.txt").read() if os.path.exists(f"{DOCS}/llms.txt") else ""
surf['llms']=set(re.findall(r'jamming-physics\.org/([a-z0-9_-]+)/',llms)) & EXPECT
for name,s in surf.items():
    missing=EXPECT-s; extra=s-EXPECT
    if missing or extra: bad(f"slug-set [{name}]", f"missing={sorted(missing)} extra={sorted(extra)}")
    else: ok(f"slug-set [{name}]",f"{len(EXPECT)}/{len(EXPECT)}")

# ---- B. hash integrity: recompute vs manifest ----
mism=[]; rmism=[]
for vid in ORDER:
    if dirhash(f"{DOCS}/{vid}")!=MV[vid].get('content_sha256'): mism.append(vid)
    if dirhash(f"repro/{vid}")!=MV[vid].get('repro_sha256'): rmism.append(vid)
ok("content_sha256 integrity",f"all {len(ORDER)} match") if not mism else bad("content_sha256 integrity",f"drift: {mism}")
ok("repro_sha256 integrity",f"all {len(ORDER)} match") if not rmism else bad("repro_sha256 integrity",f"drift: {rmism}")

# manifest self-hash recompute
m2=json.loads(json.dumps(man)); m2['lineage']['this_sha256']=""
calc=sha(json.dumps(m2,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())
ok("manifest self-hash","recomputes correctly") if calc==man['lineage']['this_sha256'] else bad("manifest self-hash",f"stale: {calc[:12]} vs {man['lineage']['this_sha256'][:12]}")

# ---- C. lineage chain ----
ch=[json.loads(l) for l in open(f"{REG}/lineage.jsonl").read().splitlines() if l.strip()]
if ch and ch[0]['parent_sha256'] is None and ch[-1]['this_sha256']==man['lineage']['this_sha256']:
    okchain=True
    for i in range(1,len(ch)):
        if ch[i]['parent_sha256']!=ch[i-1]['this_sha256']: okchain=False
    ok("lineage chain",f"{len(ch)} entry(ies), genesis valid") if okchain else bad("lineage chain","parent/child break")
else: bad("lineage chain","genesis or tip mismatch")

# ---- D. internal link + asset resolution across ALL pages ----
allfiles=set(os.path.relpath(f,DOCS) for f in glob.glob(f"{DOCS}/**/*",recursive=True) if os.path.isfile(f))
def resolves(srcrel, ref):
    ref=ref.split('#')[0].split('?')[0]
    if not ref or ref.startswith(('http://','https://','mailto:','tel:','data:','javascript:')): return True
    if ref.startswith('/'):
        target=ref[1:]
    else:
        target=os.path.normpath(os.path.join(os.path.dirname(srcrel),ref))
    if target in ('','.'):
        return 'index.html' in allfiles
    if ref.endswith('/'):
        return (target.rstrip('/')+'/index.html') in allfiles
    if target in allfiles:
        return True
    return (target.rstrip('/')+'/index.html') in allfiles
broken=[]; brokenassets=[]
htmls=glob.glob(f"{DOCS}/**/*.html",recursive=True)
for f in htmls:
    rel=os.path.relpath(f,DOCS)
    html=open(f,encoding="utf-8",errors="replace").read()
    for ref in re.findall(r'href="([^"]+)"',html):
        if not resolves(rel,ref): broken.append((rel,ref))
    for ref in re.findall(r'(?:src|href)="([^"]+\.(?:css|js|png|jpg|jpeg|svg|webp|woff2?|gif))"',html):
        if not resolves(rel,ref): brokenassets.append((rel,ref))
ok("internal links",f"{len(htmls)} pages, all resolve") if not broken else bad("internal links",f"{len(broken)} broken e.g. {broken[:3]}")
ok("asset refs","all resolve") if not brokenassets else bad("asset refs",f"{len(brokenassets)} broken e.g. {brokenassets[:3]}")

# ---- E. sitemap bijection ----
smap=set(re.findall(r'<loc>https://jamming-physics\.org/([^<]*)</loc>',open(f"{DOCS}/sitemap.xml").read()))
smap_paths=set((s if s=="" else s.rstrip('/')+'/')+("index.html" if s=="" else "") for s in smap)
idxfiles=set(os.path.relpath(f,DOCS) for f in glob.glob(f"{DOCS}/**/index.html",recursive=True))
sm_norm=set((DOCS and (s.rstrip('/')+'/index.html' if s else 'index.html')) for s in smap)
miss_in_smap=idxfiles-sm_norm; extra_in_smap=sm_norm-idxfiles
ok("sitemap bijection",f"{len(idxfiles)} pages") if not miss_in_smap and not extra_in_smap else bad("sitemap bijection",f"missing={list(miss_in_smap)[:3]} extra={list(extra_in_smap)[:3]}")

# ---- F. DOI consistency (set equality across surfaces) ----
doi_man=set(v['doi'] for v in man['volumes'])
doi_page=set(re.findall(r'doi\.org/(10\.5281/zenodo\.\d+)',page))
doi_llms=set(re.findall(r'doi:(10\.5281/zenodo\.\d+)',llms))
ok(f"DOIs: {len(ORDER)} in manifest, well-formed") if len(doi_man)==len(ORDER) and all(re.match(r'10\.5281/zenodo\.\d+$',d) for d in doi_man) else bad("DOIs manifest",f"{len(doi_man)} unique")
ok("DOI set: homepage⊇manifest") if doi_man<=doi_page else bad("DOI homepage",f"missing {sorted(doi_man-doi_page)[:3]}")
ok("DOI set: llms⊇manifest") if doi_man<=doi_llms else warn("DOI llms",f"missing {sorted(doi_man-doi_llms)[:3]}")

# ---- G. number consistency manifest==homepage==AGENTS ----
mc=sorted((v['count'] for v in man['primitives'].values()),reverse=True)
pc=sorted((int(x) for x in re.findall(r'class="scount">(\d+)<span>/30',page)),reverse=True)
ac=sorted((int(x) for x in re.findall(r'\| (\d+) / 30 \|',agents)),reverse=True)
ok("primitive counts","manifest==homepage==AGENTS "+str(mc)) if mc==pc==ac else bad("primitive counts",f"man={mc} page={pc} ag={ac}")

# ---- H. magnitude firewall scan (disease/therapy bodies) ----
DOSE=re.compile(r'\b\d+(?:\.\d+)?\s?(?:mg|mcg|µg|ug|mL|mg/kg|mg/day|IU|g/day)\b')
hits=[]
for vid in ['disease_wp','disease_kit','analgesic_threshold']:
    for f in glob.glob(f"{DOCS}/{vid}/**/*.html",recursive=True):
        t=re.sub(r'<[^>]+>',' ',open(f,encoding="utf-8",errors="replace").read())
        for m in set(DOSE.findall(t)): pass
        found=DOSE.findall(t)
        if found: hits.append((vid,os.path.relpath(f,DOCS),found[:3]))
ok("magnitude firewall","no dose-like magnitudes in therapy/disease bodies") if not hits else warn("magnitude firewall",f"{len(hits)} pages with dose-like tokens (review): {hits[:2]}")

# ---- I. hygiene ----
nested=[]
for s in ['eye','ear','nose','wave-computer','inheritance']:
    for meta in ['sitemap.xml','robots.txt','llms.txt','llms-full.txt']:
        if os.path.exists(f"{DOCS}/{s}/{meta}"): nested.append(f"{s}/{meta}")
ok("no nested meta in new slugs") if not nested else warn("nested meta",str(nested))
ok("CNAME present") if os.path.exists(f"{DOCS}/CNAME") else warn("CNAME","missing")
ok(".nojekyll present") if os.path.exists(f"{DOCS}/.nojekyll") else warn(".nojekyll","missing (GitHub Pages may strip _dirs)")
rob=open(f"{DOCS}/robots.txt").read() if os.path.exists(f"{DOCS}/robots.txt") else ""
bots=['Googlebot','Bingbot','GPTBot','ClaudeBot','PerplexityBot','OAI-SearchBot','Google-Extended']
miss_bots=[b for b in bots if b not in rob]
ok("robots.txt 7 bots") if not miss_bots else warn("robots.txt",f"missing {miss_bots}")
pyc=glob.glob("**/__pycache__",recursive=True)
ok("no __pycache__") if not pyc else warn("__pycache__",str(pyc[:3]))

# ---- report ----
nf=sum(1 for s,_,_ in R if s=="FAIL"); nw=sum(1 for s,_,_ in R if s=="WARN"); np=sum(1 for s,_,_ in R if s=="PASS")
print(f"\n{'='*64}\nVP REPO FINAL AUDIT  —  {np} PASS · {nw} WARN · {nf} FAIL\n{'='*64}")
for s,n,d in R:
    mark={'PASS':'  ✓','WARN':' ⚠ ','FAIL':' ✗ '}[s]
    print(f"{mark} [{s}] {n}" + (f"  — {d}" if d else ""))
print(f"\nVERDICT: {'CLEAN (no failures)' if nf==0 else str(nf)+' FAILURE(S) — must fix'}"
      + (f"; {nw} warning(s) for review" if nw else ""))
sys.exit(1 if nf else 0)
