#!/usr/bin/env python3
"""tools/build_consolidate.py — FRESH consolidation from the 30 current author packages (src30/).
No prior consolidated site is reused. For each volume: resolve the real site root (descending
through redirect-landing wrappers), nest it at OUT/docs/{canonical}/, bring resource dirs,
normalize slug variants (the package's OWN internal slug maps to its canonical first, so two
volumes that share an internal slug like 'disease' don't collide), rewrite repro links to GitHub,
drop dangling font preloads (no package ships the optional woff2; system serif stack is default),
fix a few stale intra-volume links, and synthesize a stylesheet where a volume ships none.
"""
import os, re, glob, shutil

SRC="src30"; OUT="build2/vp-site"
GH="https://github.com/rego093-sketch/jamming-physics/tree/main/repro"
RESOURCE=("assets","eq","concepts")
CANON=['physics','fluid-dynamics','cosmology','chemistry','geodynamics','geochronology','wave-computer',
 'dna','inheritance','neuro','mind','sensory_organ','eye','ear','nose','cardioresp','circulatory',
 'digestive','musculoskeletal','immune_hematologic','integumentary','reproductive_endocrine',
 'homeostasis_thermometabolic','homeostasis_hemodynamic','homeostasis_ionic','circadian',
 'aging_senescence','analgesic_threshold','disease_wp','disease_kit']
# cross-volume variant -> canonical (used for links to OTHER volumes)
SLUGMAP={'analgesic':'analgesic_threshold','thermometabolic':'homeostasis_thermometabolic',
 'digestive_vp_site':'digestive','circulatory_vp_site':'circulatory','immune_hematologic_vp_site':'immune_hematologic',
 'cardioresp_vp_site':'cardioresp','musculoskeletal_vp_site':'musculoskeletal','sensory-organs':'sensory_organ',
 'aging':'aging_senescence','homeostasis-hemodynamic':'homeostasis_hemodynamic','disease':'disease_wp'}
for c in CANON: SLUGMAP.setdefault(c,c)
# stale intra-volume links the author renamed (numeric prefix identifies the chapter)
LINKFIX={'mind':{'/mind/29-bipolar-episode/':'/mind/29-bipolar-state-switching/',
                 '/mind/05-learned-field/':'/mind/05-memory-physics/'}}

def nonres_subsites(d):
    return [s for s in os.listdir(d) if s not in RESOURCE and os.path.isdir(os.path.join(d,s))
            and os.path.isfile(os.path.join(d,s,'index.html'))]

def real_root(slug):
    base=f'{SRC}/{slug}'
    idx=sorted(glob.glob(f'{base}/**/index.html',recursive=True), key=lambda p:(p.count('/'),p))
    start=None
    for p in idx:
        if 'docs' in p.split('/'): start=os.path.dirname(p); break
    if start is None: start=os.path.dirname(idx[0])
    D=start
    while True:
        subs=nonres_subsites(D)
        if len(subs)==1: D=os.path.join(D,subs[0]); continue
        break
    return D, base

def docs_ancestor(R):
    d=R
    while os.path.basename(d)!='docs' and os.path.dirname(d)!=d: d=os.path.dirname(d)
    return d if os.path.basename(d)=='docs' else os.path.dirname(R)

def rewrite_html(path,c,smap):
    t=open(path,encoding='utf-8',errors='replace').read()
    def repl(m):
        attr,seg,rest=m.group(1),m.group(2),m.group(3)
        if seg in RESOURCE: return f'{attr}="/{c}/{seg}{rest}"'
        if seg=='repro':    return f'{attr}="{GH}{rest}"'
        if seg in smap:     return f'{attr}="/{smap[seg]}{rest}"'
        return m.group(0)
    t=re.sub(r'(href|src)="/([^"/]+)([^"]*)"',repl,t)
    # drop dangling font preload (optional woff2 not shipped; system serif stack is the default)
    t=re.sub(r'\s*<link[^>]*assets/fonts/[^>]*>','',t)
    # fix stale intra-volume links
    for bad,good in LINKFIX.get(c,{}).items(): t=t.replace(f'"{bad}"',f'"{good}"')
    open(path,'w',encoding='utf-8').write(t)

def copy_into(src,dst):
    os.makedirs(dst,exist_ok=True)
    for it in os.listdir(src):
        s,d=os.path.join(src,it),os.path.join(dst,it)
        if os.path.isdir(s): shutil.copytree(s,d,dirs_exist_ok=True)
        else: shutil.copy2(s,d)

def consolidate(slug):
    R,base=real_root(slug)
    internal=os.path.basename(R)
    smap=dict(SLUGMAP)
    if internal!='docs': smap[internal]=slug          # self before cross-volume (resolves 'disease' collision)
    tgt=f'{OUT}/docs/{slug}'; shutil.rmtree(tgt,ignore_errors=True); os.makedirs(tgt)
    copy_into(R,tgt)
    da=docs_ancestor(R)
    for d in RESOURCE:
        if os.path.exists(os.path.join(tgt,d)): continue
        anc=R
        while True:
            cand=os.path.join(anc,d)
            if os.path.isdir(cand): shutil.copytree(cand,os.path.join(tgt,d),dirs_exist_ok=True); break
            if anc==base or os.path.dirname(anc)==anc: break
            anc=os.path.dirname(anc)
    for meta in ('sitemap.xml','robots.txt','llms.txt','llms-full.txt','gate.json','CNAME','.nojekyll'):
        p=os.path.join(tgt,meta)
        if os.path.isfile(p): os.remove(p)
    for f in glob.glob(f'{tgt}/**/*.html',recursive=True): rewrite_html(f,slug,smap)
    wrapper=os.path.dirname(da); rtgt=f'{OUT}/repro/{slug}'
    shutil.rmtree(rtgt,ignore_errors=True); os.makedirs(rtgt)
    for it in os.listdir(wrapper):
        if it=='docs': continue
        s,d=os.path.join(wrapper,it),os.path.join(rtgt,it)
        if os.path.isdir(s): shutil.copytree(s,d,dirs_exist_ok=True)
        else: shutil.copy2(s,d)
    return len(glob.glob(f'{tgt}/**/index.html',recursive=True))

def synthesize_css():
    canon=None
    for s in ['physics','dna','neuro','cardioresp']:
        c=glob.glob(f'{OUT}/docs/{s}/assets/css/site.css')
        if c: canon=open(c[0],encoding='utf-8').read(); break
    made=[]
    for slug in CANON:
        refs=set()
        for f in glob.glob(f'{OUT}/docs/{slug}/**/*.html',recursive=True):
            for m in re.findall(r'(?:href|src)="(/'+re.escape(slug)+r'/assets/[^"]+\.css)"', open(f,encoding='utf-8',errors='replace').read()):
                refs.add(m)
        for ref in refs:
            disk=f'{OUT}/docs'+ref
            if not os.path.isfile(disk):
                os.makedirs(os.path.dirname(disk),exist_ok=True)
                open(disk,'w',encoding='utf-8').write(canon); made.append(ref)
    return made

if __name__=="__main__":
    shutil.rmtree(OUT,ignore_errors=True)
    os.makedirs(f'{OUT}/docs'); os.makedirs(f'{OUT}/repro')
    tot=0
    for s in CANON:
        p=consolidate(s); tot+=p; print(f"  {s:24s} {p:>5d}")
    made=synthesize_css()
    print(f"\nTOTAL pages: {tot} | docs slugs: {len(glob.glob(f'{OUT}/docs/*/index.html'))} | css synth: {sorted(set(m.split('/')[1] for m in made))}")
