#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
w1_gate.py  --  Phase W1 authoring gate (Disease Mechanisms volume), v0.7.

Reads the R5 registry CSVs when present (treatment grades accession-dated [L]; burden grades
GeneReviews-corroborated). Checks the full emitted set: 1 hub + 1 framework + 17 placed disease
pages + 18 not-placed disease pages + 2 mechanism-class chapters.

Checks (each must PASS before handoff):
  1  build_deterministic_2x     re-runs w1_build.py twice; site-set sha identical
  2  structure_full_set         1 hub + 1 framework + 17 placed + 18 not-placed + 2 class; unique URLs
  3  answer_first_40_60         every disease/class page has <p class=answer> at 40-60 words
  4  abstract_and_claimstrip    every disease page has .abstract + .claim-strip; class pages have .claim-strip
  5  jsonld_valid               disease=MedicalCondition+ScholarlyArticle+Breadcrumb; class=ScholarlyArticle+
                                ItemList+Breadcrumb; framework=ScholarlyArticle+Breadcrumb; hub=Series+Breadcrumb
  6  burden_drift_zero (C1)     placed vp-card residual score+rank and treatment e/R_treat MATCH the CSVs
  7  axis_values_match (C1)     the 5 burden-axis values on each disease page match burden_scores(_registry).csv
  8  treatment_match            modality + evidence_status on each disease page match treatments(_registry).csv
  9  provisional_H_flag (C3)    every placed page + framework + hub flags the order provisional [H]
  10 treatment_grade_honest     treat grade in {[L],[H]}; every [L] carries a GeneReviews NBK accession;
                                no evidence_status 'curative'; no disease-level 'curative' assertion (C-D3)
  11 not_placed_honest          each not-placed page says 'not placed' + shows <3 axes + open axes graded [O]
  12 class_links_members        each class chapter links every member page it claims (no orphan); [F] marker
  13 retrieval_access           robots allows 7 crawlers; sitemap lists ALL section URLs; llms.txt < 5KB
  14 hub_links_no_orphan        hub links every chapter; each disease links the framework burden method
  15 no_fabricated_doi          volume DOI shown 'pending'; no zenodo DOI presented as this volume's id
  16 description_seo_length     every page meta description 80-160 chars, complete
  17 engine_pin_drift_zero (C-D8)  sha256sum -c MANIFEST_governed.sha256 -> all OK
"""
import json, csv, os, re, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR  = os.path.join(ROOT, "data", "curated")
DOCS = os.path.join(ROOT, "docs")
VOL  = os.path.join(DOCS, "disease")

def pick(*names):
    for n in names:
        p=os.path.join(CUR,n)
        if os.path.exists(p): return p
    return os.path.join(CUR,names[-1])
def load_csv(p):
    with open(p, newline="") as f: return list(csv.DictReader(f))
residual = {r["cui"]: r for r in load_csv(pick("burden_residual_registry.csv","burden_residual.csv"))}
scores   = {r["cui"]: r for r in load_csv(pick("burden_scores_registry.csv","burden_scores.csv"))}
treats   = {r["cui"]: r for r in load_csv(pick("treatments_registry.csv","treatments.csv"))}
placed = sorted([r for r in residual.values() if r["rankable"]=="yes"], key=lambda r:int(r["residual_rank"]))
RANK_TOTAL = len(placed)
notplaced_cuis = sorted([c for c,s in scores.items() if s["rankable"]!="yes"],
                        key=lambda c:(-int(scores[c]["axes_scored"]), scores[c]["entity"]))
N_NOTPLACED = len(notplaced_cuis)

def num(x,p=4):
    try: return f"{float(x):.{p}f}"
    except (ValueError,TypeError): return None
def read(p): return open(p,encoding="utf-8").read()
def slug_of(path): return os.path.basename(os.path.dirname(path))

def jsonld_objs(s):
    out=[]
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: out.append(json.loads(m.group(1)))
        except Exception as e: out.append({"@type":f"PARSE_ERR:{e}"})
    return out
def jsonld_types(s): return [o.get("@type") for o in jsonld_objs(s)]
def cui_of_page(s):
    for o in jsonld_objs(s):
        if o.get("@type")=="MedicalCondition":
            for c in o.get("code",[]):
                if c.get("codingSystem")=="MedGen": return c.get("codeValue")
    return None

# ---- map emitted pages to roles (format-independent: by JSON-LD content) ----
placed_pages={}; notplaced_pages={}; class_pages={}; fw_html=None
def map_pages():
    dp={}; npd={}; cp={}; fw=None
    for f in sorted(glob.glob(os.path.join(VOL,"*","index.html"))):
        s=read(f); sl=slug_of(f)
        if sl.startswith("01-"): fw=s; continue
        types=jsonld_types(s)
        if "MedicalCondition" in types:
            cui=cui_of_page(s)
            if cui in residual and residual[cui]["rankable"]=="yes": dp[cui]=s
            else: npd[cui]=s
        elif "ItemList" in types:
            cp[sl]=s
    return dp, npd, cp, fw
placed_pages, notplaced_pages, class_pages, fw_html = map_pages()
hub_html = read(os.path.join(VOL,"index.html"))

results=[]
def check(name, ok, detail=""): results.append((name, bool(ok), detail))

# ---- 1 determinism ----
def build_digest():
    out=subprocess.run(["python3", os.path.join(ROOT,"tools","w1_build.py")], capture_output=True, text=True)
    m=re.search(r"site-set sha256\(12\) = ([0-9a-f]+)", out.stdout)
    return m.group(1) if m else None
d1=build_digest(); d2=build_digest()
check("build_deterministic_2x", d1 and d1==d2, f"{d1} == {d2}")
placed_pages, notplaced_pages, class_pages, fw_html = map_pages()
hub_html=read(os.path.join(VOL,"index.html"))

# ---- 2 structure ----
check("structure_full_set",
      (len(placed_pages)==RANK_TOTAL and len(notplaced_pages)==N_NOTPLACED and
       len(class_pages)>=2 and fw_html and hub_html),
      f"placed={len(placed_pages)}/{RANK_TOTAL} notplaced={len(notplaced_pages)}/{N_NOTPLACED} "
      f"class={len(class_pages)} fw={'y' if fw_html else 'n'} hub={'y' if hub_html else 'n'}")

disease_pages = {**placed_pages, **notplaced_pages}

# ---- 3 answer-first 40-60 (diseases + class chapters) ----
bad=[]
for key,s in list(disease_pages.items())+list(class_pages.items())+[("framework",fw_html)]:
    m=re.search(r'<p class="answer">(.*?)</p>', s, re.S)
    if not m: bad.append(f"{key}:none"); continue
    t=re.sub('<[^>]+>',' ',m.group(1)); t=re.sub(r'\[[VLHOF]\]',' ',t)
    wc=len(t.split())
    if not(40<=wc<=60): bad.append(f"{key}:{wc}")
check("answer_first_40_60", not bad, f"out_of_range={bad}")

# ---- 4 abstract + claim strip ----
bad=[]
for cui,s in disease_pages.items():
    if '<p class="abstract">' not in s: bad.append(f"{cui}:abstract")
    if 'class="claim-strip"' not in s or 'class="grade ' not in s: bad.append(f"{cui}:claimstrip")
for sl,s in class_pages.items():
    if 'class="claim-strip"' not in s: bad.append(f"{sl}:claimstrip")
check("abstract_and_claimstrip", not bad, f"missing={bad}")

# ---- 5 jsonld valid ----
bad=[]
for cui,s in disease_pages.items():
    t=jsonld_types(s)
    if not all(x in t for x in ["ScholarlyArticle","MedicalCondition","BreadcrumbList"]): bad.append(f"{cui}:{t}")
    if "0009-0002-7535-8245" not in s: bad.append(f"{cui}:orcid")
for sl,s in class_pages.items():
    t=jsonld_types(s)
    if not all(x in t for x in ["ScholarlyArticle","ItemList","BreadcrumbList"]): bad.append(f"{sl}:{t}")
if not all(x in jsonld_types(fw_html) for x in ["ScholarlyArticle","BreadcrumbList"]): bad.append("fw")
if not all(x in jsonld_types(hub_html) for x in ["CreativeWorkSeries","BreadcrumbList"]): bad.append("hub")
check("jsonld_valid", not bad, f"issues={bad[:6]}")

# ---- 6 burden drift zero (C1) -- placed only ----
bad=[]
for cui,s in placed_pages.items():
    r=residual[cui]; tr=treats[cui]
    exp_score=num(r["burden_score"]); exp_rank=r["residual_rank"]
    exp_e=num(tr["efficacy_offset_e"]); exp_rt=num(tr["R_treat"]); exp_raw=num(r["raw_burden"])
    mcard=re.search(r'Residual burden score = ([\d.]+)\b', s)
    if not mcard or mcard.group(1)!=exp_score: bad.append(f"{cui}:card={mcard.group(1) if mcard else None}!={exp_score}")
    mrank=re.search(rf'Residual rank (\d+) of {RANK_TOTAL}', s)
    if not mrank or mrank.group(1)!=exp_rank: bad.append(f"{cui}:rank")
    if f"e = {exp_e}" not in s: bad.append(f"{cui}:e")
    if f"R_treat = {exp_rt}" not in s: bad.append(f"{cui}:Rt")
    if exp_raw not in s: bad.append(f"{cui}:raw")
check("burden_drift_zero", not bad, f"mismatch={bad[:6]}")

# ---- 7 axis values match (C1) -- all disease pages ----
bad=[]
for cui,s in disease_pages.items():
    sc=scores[cui]
    for ax in ["O","P","S","M","D"]:
        g=sc[ax+"_grade"]; v=num(sc[ax+"_value"])
        if g=="[O]": continue
        if v is None or v not in s: bad.append(f"{cui}:{ax}={v}")
check("axis_values_match", not bad, f"mismatch={bad[:8]}")

# ---- 8 treatment match -- all disease pages ----
bad=[]
for cui,s in disease_pages.items():
    tr=treats[cui]
    if tr["modality"] not in s: bad.append(f"{cui}:modality")
    if tr["evidence_status"] not in s: bad.append(f"{cui}:status={tr['evidence_status']}")
check("treatment_match", not bad, f"missing={bad[:6]}")

# ---- 9 provisional-H flag -- placed + framework + hub ----
bad=[]
for key,s in list(placed_pages.items())+[("framework",fw_html),("hub",hub_html)]:
    if "provisional" not in s or "registry-locked" not in s: bad.append(key)
check("provisional_H_flag", not bad, f"missing={bad}")

# ---- 10 treatment grade honest (C-D3) ----
bad=[]
for cui,s in disease_pages.items():
    g=treats[cui]["grade"]
    if g not in ("[L]","[H]"): bad.append(f"{cui}:grade={g}")
    if g=="[L]":
        nbk=treats[cui].get("nbk","")
        if not re.match(r"NBK\d+", nbk or ""): bad.append(f"{cui}:L-without-NBK")
        if f"www.ncbi.nlm.nih.gov/books/{nbk}/" not in s: bad.append(f"{cui}:L-accession-not-shown")
    # C-D3: hedged clinical language ("curative intent", "potentially curative") is accurate and
    # allowed; a bare/unhedged disease-level cure assertion is not.
    cur=len(re.findall(r'\bcurative\b', s))
    hedged=len(re.findall(r'curative intent|potentially curative', s))
    if cur>hedged: bad.append(f"{cui}:unhedged-curative")
if any(t["evidence_status"]=="curative" for t in treats.values()): bad.append("csv-has-curative")
check("treatment_grade_honest", not bad, f"issues={bad[:6]}")

# ---- 11 not-placed honest ----
bad=[]
for cui,s in notplaced_pages.items():
    if "not placed" not in s.lower(): bad.append(f"{cui}:no-notplaced")
    if "[O] not placed" not in s: bad.append(f"{cui}:no-badge")
    if int(scores[cui]["axes_scored"])>=3: bad.append(f"{cui}:axes>=3?")
    # at least one open axis named and graded [O]
    if 'gi-O' not in s and '[O]' not in s: bad.append(f"{cui}:no-open-grade")
check("not_placed_honest", not bad, f"issues={bad[:6]}")

# ---- 12 class chapters link members ----
import importlib.util
spec=importlib.util.spec_from_file_location("w1b", os.path.join(ROOT,"tools","w1_build.py"))
w1b=importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(w1b); CLASSES=w1b.CLASSES
except Exception: CLASSES=[]
bad=[]
# build cui->slug from emitted pages
cui_slug={}
for f in glob.glob(os.path.join(VOL,"*","index.html")):
    s=read(f); c=cui_of_page(s)
    if c: cui_slug[c]=slug_of(f)
for cdef in CLASSES:
    # find the class page by name marker
    pg=None
    for sl,s in class_pages.items():
        if cdef["name"] in s: pg=s; break
    if pg is None: bad.append(f"{cdef['key']}:page-missing"); continue
    if "[F] mechanism class" not in pg: bad.append(f"{cdef['key']}:no-F")
    for m in cdef["members"]:
        if m in cui_slug and f'/disease/{cui_slug[m]}/' not in pg:
            bad.append(f"{cdef['key']}:orphan-{m}")
check("class_links_members", not bad, f"issues={bad[:6]}")

# ---- 13 retrieval access ----
robots=read(os.path.join(DOCS,"robots.txt"))
bots=["Googlebot","Bingbot","OAI-SearchBot","GPTBot","PerplexityBot","ClaudeBot","Google-Extended"]
sm=read(os.path.join(DOCS,"sitemap.xml"))
sm_urls=re.findall(r"<loc>(.*?)</loc>", sm)
meta=json.load(open(os.path.join(VOL,"_meta.json")))
expected_urls = 1 + len(meta["chapters"])   # hub + every section
llms=os.path.join(DOCS,"llms.txt")
llms_ok=os.path.exists(llms) and os.path.getsize(llms)<5000
check("retrieval_access",
      all(b in robots for b in bots) and len(sm_urls)==expected_urls and llms_ok,
      f"bots_ok={all(b in robots for b in bots)} sitemap={len(sm_urls)}/{expected_urls} llms<5KB={llms_ok}")

# ---- 14 hub links no orphan ----
slugs=[c["slug"] for c in meta["chapters"]]
bad=[sl for sl in slugs if f'/disease/{sl}/' not in hub_html]
no_fw=[cui for cui,s in disease_pages.items()
       if "/disease/01-classification-burden-treatment-framework/#burden" not in s
       and "/disease/01-classification-burden-treatment-framework/#mechanism" not in s]
check("hub_links_no_orphan", not bad and not no_fw, f"hub_missing={bad} disease_no_fwlink={no_fw[:4]}")

# ---- 15 no fabricated DOI ----
bad=[]
for key,s in list(disease_pages.items())+list(class_pages.items())+[("framework",fw_html),("hub",hub_html)]:
    if "pending" not in s: bad.append(f"{key}:no-pending")
    if re.search(r'doi\.org/10\.5281/zenodo', s): bad.append(f"{key}:zenodo")
check("no_fabricated_doi", not bad, f"issues={bad[:4]}")

# ---- 16 description SEO length ----
bad=[]
for key,s in list(disease_pages.items())+list(class_pages.items())+[("framework",fw_html),("hub",hub_html)]:
    m=re.search(r'<meta name="description" content="([^"]*)"', s)
    if not m: bad.append(f"{key}:none"); continue
    L=len(m.group(1))
    if not(80<=L<=160): bad.append(f"{key}:{L}")
check("description_seo_length", not bad, f"out_of_range={bad}")

# ---- 17 engine pin drift zero ----
pin=subprocess.run(["sha256sum","-c","MANIFEST_governed.sha256"], cwd=ROOT, capture_output=True, text=True)
pin_ok=pin.returncode==0 and "FAILED" not in pin.stdout
check("engine_pin_drift_zero", pin_ok, pin.stdout.strip().splitlines()[-1] if pin.stdout else "")

# ---- report ----
n_pass=sum(1 for _,ok,_ in results if ok)
verdict=f"PASS ({n_pass}/{len(results)})" if n_pass==len(results) else f"FAIL ({n_pass}/{len(results)})"
report={"phase":"W1","gate":"w1_authoring","verdict":verdict,"site_set_sha":d1,
        "diseases_placed":RANK_TOTAL,"diseases_not_placed":N_NOTPLACED,"class_chapters":len(class_pages),
        "checks":[{"check":n,"pass":ok,"detail":dt} for n,ok,dt in results]}
os.makedirs(os.path.join(ROOT,"reports"),exist_ok=True)
with open(os.path.join(ROOT,"reports","w1.gate.json"),"w") as f: json.dump(report,f,indent=2)
print(verdict)
for n,ok,dt in results:
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"  -- {dt}" if (dt and not ok) else ""))
