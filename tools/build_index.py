#!/usr/bin/env python3
# Deterministic builder for jamming-physics.org homepage (docs/index.html)
# Reads tools/master.json + registry/vp.manifest.json, writes docs/index.html.
import json, html, os

def _find(*cands):
    for c in cands:
        if os.path.isfile(c): return c
    raise FileNotFoundError(cands[0])

M = {r['paper_id']: r for r in json.load(open(_find('tools/master.json','master.json')))}
DOI_BASE = "https://doi.org/"
SITE = "https://jamming-physics.org/"

# Curated display tags (<=3 most characteristic shared primitives per volume)
TAGS = {
 'physics':['jammed lattice','c²=B/ρ','6π⁵'],
 'fluid-dynamics':['jammed continuum','Navier–Stokes'],
 'cosmology':['vacuum inflow','a₀=cH₀/2π'],
 'chemistry':['single anchor','φ_RCP=0.7405'],
 'geodynamics':['jamming↔unjamming','cusp'],
 'geochronology':['incorporation limit'],
 'continental-genesis-cascade':['buoyancy gate','percolation attractor','one relaxation ×3'],
 'wave-computer':['phase coding','clock-free'],
 'dna':['γ = −Σ stacking ΔG','R19','bridge'],
 'inheritance':['two channels','writable A4','RNA'],
 'neuro':['neuron = R19','θ/γ ≈ 7±2','FHN'],
 'mind':['engram = attractor','R19','open: experience'],
 'sensory_organ':['cube-root','Hopf','R = (F/β)^⅓'],
 'eye':['single-photon R19','n = √(B/ρ)','cube-root'],
 'ear':['ṡ = g·s − s³ + h','cube-root'],
 'nose':['R19','measured γ code'],
 'cardioresp':['FHN oscillator'],
 'circulatory':['MAP = CO×SVR','R19'],
 'digestive':['one clock','FHN'],
 'musculoskeletal':['measured γ','mechanical load'],
 'immune_hematologic':['population thresholds'],
 'integumentary':['barrier','UV → melanoma key'],
 'reproductive_endocrine':['measured-γ order'],
 'homeostasis_thermometabolic':['OU setpoint','three levers'],
 'homeostasis_hemodynamic':['MAP loop','R19'],
 'homeostasis_ionic':['three levers','setpoint'],
 'circadian':['measured γ = 1.33348'],
 'aging_senescence':['risk multiplier','|z|<1'],
 'analgesic_threshold':['L1/L2/L3','R19 barrier'],
 'disease_wp':['gene-key cases'],
 'disease_kit':['corrective direction [F]','magnitude [O]'],
}

# Tier registry: (id, eyebrow, title, intro)
TIERS = [
 (1,'Foundation · non-biological',
  'The substrate, before life',
  'The vacuum modelled as a jammed elastic solid. Eight volumes derive light, matter, fields, flow, the cosmos, the Earth, the limits of dating, the rise of dry land and its recent relaxation, and computation from one measured medium — all before biology enters.'),
 (2,'The bridge',
  'DNA — where physics becomes biology',
  'A single volume carries the substrate across. The same R19 switch is instantiated by a material stiffness γ = −mean nearest-neighbour stacking free energy, read directly from the genome and never fitted (corr(γ, GC) = 0.998).'),
 (3,'Inheritance & information',
  'Two channels on one switch',
  'The switch is read on two channels — the unwritable promoter ruler γ (the SET) and a writable coordinate (the drive). From that single substrate come environmental inheritance, the RNA layer, and the path to RNA vaccines and gene therapy.'),
 (4,'Neural & cognitive',
  'A neuron is the switch with a slow recovery',
  'Add a slow recovery variable and the R19 switch becomes a low-frequency relaxation oscillator. From it emerge brain rhythms, the θ/γ working-memory capacity (≈ 7±2, the one link with a direct causal tACS test), memory, value, and the felt stream of thought.'),
 (5,'Sensory organs',
  'The same switch, held at criticality',
  'Each sense is the identical cubic poised at its critical point — which forces cube-root compression in both the ear and the eye, exponent exactly 0.333. Every organ emerges from its master gene’s measured γ; the eye even reuses light as the jammed-lattice wave.'),
 (6,'Organ systems',
  'Emerged in measured-γ order',
  'Organs appear in the order set by the spinodal of their master gene’s measured γ, are sized by dwell ∝ γ^1.5, and run as FitzHugh–Nagumo relaxation oscillators — heart and lung, vasculature, gut, bone, blood, skin, and the reproductive–endocrine axis.'),
 (7,'Homeostasis & time',
  'Defended setpoints, read over time',
  'A defended setpoint is an Ornstein–Uhlenbeck loop with three correction levers; rhythms and aging are the same bistable switch read over time. Circadian γ is measured (BMAL1/ARNTL = 1.33348) and, like everything here, never tuned.'),
 (8,'Disease & therapy',
  'The switch pushed off, and pushed back',
  'Disease is the switch driven off its setpoint; therapy is pushing the barrier back along one of three levers. The corrective direction is forced [F]; clinical magnitude is held open [O] behind a strict no-magnitude firewall.'),
]
TIER_VOLS = {
 1:['physics','fluid-dynamics','cosmology','chemistry','geodynamics','geochronology','continental-genesis-cascade','wave-computer'],
 2:['dna'],
 3:['inheritance'],
 4:['neuro','mind'],
 5:['sensory_organ','eye','ear','nose'],
 6:['cardioresp','circulatory','digestive','musculoskeletal','immune_hematologic','integumentary','reproductive_endocrine'],
 7:['homeostasis_thermometabolic','homeostasis_hemodynamic','homeostasis_ionic','circadian','aging_senescence'],
 8:['analgesic_threshold','disease_wp','disease_kit'],
}

def esc(s): return html.escape(s, quote=True)

def grade_badges(g):
    out=[]
    if g['forced']:   out.append(f'<span class="gr gr-f">{g["forced"]} forced</span>')
    if g['verified']: out.append(f'<span class="gr gr-v">{g["verified"]} verified</span>')
    if g['open']:     out.append(f'<span class="gr gr-o">{g["open"]} open</span>')
    return ' '.join(out)

def card(pid):
    r=M[pid]
    tags=''.join(f'<li>{esc(t)}</li>' for t in TAGS.get(pid,[]))
    gb=grade_badges(r['grades'])
    grow=f'<p class="gbar">{gb}</p>' if gb else ''
    bridge=' card--bridge' if pid=='dna' else ''
    return f'''      <article class="card{bridge}">
        <h3><a href="{esc(r['hub'])}">{esc(r['short'])}</a></h3>
        <p class="hl">{esc(r['hl'])}</p>
        <ul class="tags">{tags}</ul>
        {grow}<p class="doi"><a href="{DOI_BASE}{esc(r['doi'])}" rel="noopener">doi:{esc(r['doi'])}</a> · <span class="np">{r['pages']} pages</span></p>
      </article>'''

def tier_block(tid):
    eyebrow,title,intro = next((e,t,i) for (n,e,t,i) in TIERS if n==tid)
    vols=TIER_VOLS[tid]
    cards='\n'.join(card(v) for v in vols)
    cls='tier tier--bridge' if tid==2 else 'tier'
    return f'''    <section class="{cls}" id="tier-{tid}">
      <div class="tier-head">
        <p class="eyebrow">{esc(eyebrow)}</p>
        <h2>{esc(title)}</h2>
        <p class="tier-intro">{esc(intro)}</p>
      </div>
      <div class="grid">
{cards}
      </div>
    </section>'''

# ---- JSON-LD hasPart (all 30) ----
def haspart():
    items=[]
    order=[v for t in [1,2,3,4,5,6,7,8] for v in TIER_VOLS[t]]
    for pid in order:
        r=M[pid]
        items.append({"@type":"CreativeWork","name":r['short'],
                      "url":SITE+pid+"/","identifier":"doi:"+r['doi']})
    return items

jsonld = {
 "@context":"https://schema.org",
 "@graph":[
  {"@type":"WebSite","@id":SITE+"#website","url":SITE,
   "name":"Jamming Physics — the VP framework",
   "description":"The vacuum as a jammed elastic solid: one measured substrate and one bistable switch projected across 30 open-access volumes, from physics to DNA to disease.",
   "inLanguage":"en","license":"https://creativecommons.org/licenses/by/4.0/",
   "author":{"@id":SITE+"#author"}},
  {"@type":"Person","@id":SITE+"#author","name":"Young Jae Lee",
   "url":"https://orcid.org/0009-0002-7535-8245",
   "identifier":"https://orcid.org/0009-0002-7535-8245",
   "affiliation":"Independent researcher"},
  {"@type":"CollectionPage","@id":SITE+"#collection","url":SITE,
   "name":"VP framework — 30 volumes","isPartOf":{"@id":SITE+"#website"},
   "author":{"@id":SITE+"#author"},"hasPart":haspart()}
 ]
}
jsonld_s = json.dumps(jsonld, ensure_ascii=False)

# Counts for the connection-strength section (measured by grep across 30 volumes)
# Connection-strength counts are READ FROM THE MANIFEST (single source of truth,
# measured over the 30 volume bodies) so the homepage can never drift from it.
_PRIM_DISPLAY = {
 "R19":("R19 bistable switch","ṡ = g·s − s³ + h"),
 "gamma":("γ — measured promoter stiffness","γ = −mean NN stacking ΔG"),
 "emergence":("Emergence from measured γ","STATE · spinodal · dwell ∝ γ^1.5"),
 "jammed_c2":("Jammed lattice / c² = B/ρ","the bare physical substrate"),
 "kramers":("Kramers / Arrhenius barrier","escape over g²/4"),
 "fhn":("FitzHugh–Nagumo oscillator","relaxation rhythm"),
 "cube_root":("Cube-root transduction","R = (F/β)^⅓"),
}
_man = json.load(open(_find('registry/vp.manifest.json','vp.manifest.json')))['primitives']
STRENGTH = sorted(
 [(_PRIM_DISPLAY[k][0], _PRIM_DISPLAY[k][1], _man[k]['count']) for k in _PRIM_DISPLAY if k in _man],
 key=lambda x: -x[2])
_C = {k: _man[k]['count'] for k in _man}   # counts for hero facts
def strength_rows():
    out=[]
    for name,sub,n in STRENGTH:
        pct=int(round(n/30*100))
        out.append(f'''        <li class="srow">
          <div class="slabel"><span class="sname">{esc(name)}</span><span class="ssub">{esc(sub)}</span></div>
          <div class="sbar"><span style="width:{pct}%"></span></div>
          <div class="scount">{n}<span>/30</span></div>
        </li>''')
    return '\n'.join(out)

# Specializations of the one cubic
SPECS = [
 ("Set the threshold from measured γ","DNA","spinodal ∝ γ^1.5, barrier = γ²/4"),
 ("Hold at criticality, g → 0","Eye & ear","cube-root compression R = (F/β)^⅓, exponent 0.333"),
 ("Add a slow recovery variable","Neuro","relaxation oscillator; working memory = θ/γ ≈ 7±2"),
 ("Read both stable states","Mind","engram = bistable attractor; mood = a switch that persists"),
 ("Push the barrier, g²/4","Disease & therapy","the three correction levers L1 / L2 / L3"),
]
def spec_rows():
    out=[]
    for op,dom,res in SPECS:
        out.append(f'''        <li>
          <div class="op">{esc(op)}</div>
          <div class="res"><span class="dom">{esc(dom)}</span>{esc(res)}</div>
        </li>''')
    return '\n'.join(out)

# DOI index (footer) — all 30 in tier order
def doi_index():
    order=[v for t in [1,2,3,4,5,6,7,8] for v in TIER_VOLS[t]]
    out=[]
    for pid in order:
        r=M[pid]
        out.append(f'<li><a href="{esc(r["hub"])}">{esc(r["short"])}</a> <a class="dl" href="{DOI_BASE}{esc(r["doi"])}" rel="noopener">{esc(r["doi"])}</a></li>')
    return '\n'.join(out)

tiers_html='\n'.join(tier_block(t) for t in [1,2,3,4,5,6,7,8])

# ----------------------------- PAGE -----------------------------
PAGE = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jamming Physics — one substrate, one switch, 30 volumes from physics to disease</title>
<meta name="description" content="The VP framework models the vacuum as a jammed elastic solid whose bistable R19 switch is the single kernel behind 30 open-access volumes — physics, DNA, the senses, the organs, homeostasis, and disease — with every number measured, never fitted.">
<link rel="canonical" href="{SITE}">
<meta name="author" content="Young Jae Lee">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jamming Physics">
<meta property="og:title" content="Jamming Physics — one substrate, one switch, 30 volumes">
<meta property="og:description" content="One measured substrate and one bistable switch (ṡ = g·s − s³ + h) projected across 30 open-access volumes, from the vacuum to the genome to disease.">
<meta property="og:url" content="{SITE}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Jamming Physics — one substrate, one switch, 30 volumes">
<meta name="twitter:description" content="One measured substrate, one bistable switch, projected across 30 open-access volumes from physics to disease.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<script type="application/ld+json">{jsonld_s}</script>
<style>
:root{{
  --paper:#f6f7f4; --panel:#ffffff; --ink:#15191d; --soft:#3c434a; --mut:#697079;
  --line:#e3e6e0; --line2:#eef0eb;
  --sub:#0a5a8a; --bridge:#a86f10; --bridge-bg:#fbf3e2; --bio:#0f6e56;
  --g-f:#0b6b2e; --g-v:#0a5a8a; --g-o:#9a4310;
  --serif:'Spectral',Georgia,'Times New Roman',serif;
  --sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,'SFMono-Regular','JetBrains Mono','Menlo',Consolas,monospace;
  --wrap:1140px;
}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}}
a{{color:var(--sub);text-decoration:none}}
a:hover{{text-decoration:underline}}
.skip{{position:absolute;left:-9999px;top:0;background:var(--ink);color:#fff;padding:.6em 1em;border-radius:6px;z-index:50}}
.skip:focus{{left:12px;top:12px}}
.wrap{{max-width:var(--wrap);margin:0 auto;padding:0 24px}}
.eyebrow{{font-family:var(--sans);font-size:12.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--mut);margin:0 0 .6em;font-weight:600}}
.mono{{font-family:var(--mono)}}

/* header */
.site{{border-bottom:1px solid var(--line);background:var(--paper);position:sticky;top:0;z-index:30;backdrop-filter:saturate(1.2) blur(6px)}}
.site .wrap{{display:flex;align-items:center;justify-content:space-between;height:60px;gap:18px}}
.brand{{font-family:var(--serif);font-weight:600;font-size:18px;color:var(--ink);letter-spacing:.01em;white-space:nowrap}}
.brand .dot{{color:var(--bridge)}}
.nav{{display:flex;gap:22px;font-size:14px;color:var(--soft)}}
.nav a{{color:var(--soft)}}
@media(max-width:760px){{.nav{{display:none}}}}

/* hero */
.hero{{padding:72px 0 30px;border-bottom:1px solid var(--line)}}
.hero h1{{font-family:var(--serif);font-weight:600;font-size:clamp(2rem,4.6vw,3.35rem);line-height:1.08;letter-spacing:-.012em;margin:.1em 0 .35em;max-width:18ch}}
.hero h1 em{{font-style:italic;color:var(--sub)}}
.lead{{font-family:var(--serif);font-size:clamp(1.08rem,1.7vw,1.32rem);line-height:1.5;color:var(--soft);max-width:60ch;margin:.2em 0 1.3em}}
.stamp{{display:inline-flex;align-items:baseline;gap:.7em;font-family:var(--mono);font-size:clamp(1.05rem,2vw,1.45rem);background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--bridge);border-radius:0 8px 8px 0;padding:.6em .95em;color:var(--ink);margin:.2em 0 1.5em}}
.stamp b{{color:var(--bridge);font-weight:500}}
.stamp span{{font-family:var(--sans);font-size:13px;color:var(--mut);letter-spacing:.02em}}
.facts{{display:flex;flex-wrap:wrap;gap:30px;margin:0 0 8px;padding-top:6px}}
.fact b{{display:block;font-family:var(--serif);font-size:1.7rem;font-weight:600;line-height:1.1}}
.fact span{{font-size:12.5px;color:var(--mut);letter-spacing:.04em;text-transform:uppercase}}
.fact .lc{{font-style:normal;text-transform:none}}
.meta{{color:var(--mut);font-size:13.5px;margin-top:20px}}
.meta a{{color:var(--sub)}}

/* generic section */
section.band{{padding:54px 0;border-bottom:1px solid var(--line)}}
section.band h2{{font-family:var(--serif);font-weight:600;font-size:clamp(1.45rem,2.4vw,2rem);line-height:1.15;margin:.1em 0 .5em;letter-spacing:-.01em}}
.prose{{max-width:68ch;color:var(--soft);font-size:16.5px}}
.prose p{{margin:.5em 0 1em}}
.prose strong{{color:var(--ink);font-weight:600}}
.kbd{{font-family:var(--mono);font-size:.92em;background:var(--line2);padding:.06em .35em;border-radius:4px;color:var(--ink)}}

/* one-kernel showcase */
.kernel-box{{margin-top:26px;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.kernel-eq{{padding:20px 24px;border-bottom:1px solid var(--line);background:linear-gradient(0deg,var(--bridge-bg),var(--bridge-bg))}}
.kernel-eq .e{{font-family:var(--mono);font-size:clamp(1.3rem,2.6vw,1.7rem);color:var(--ink)}}
.kernel-eq .c{{font-size:13.5px;color:var(--bridge);font-weight:600;letter-spacing:.02em;margin-top:.2em}}
.kernel-box ul{{list-style:none;margin:0;padding:0}}
.kernel-box li{{display:grid;grid-template-columns:minmax(180px,1fr) 2fr;gap:16px;padding:14px 24px;border-top:1px solid var(--line2);align-items:baseline}}
.kernel-box li:first-child{{border-top:0}}
.kernel-box .op{{font-family:var(--mono);font-size:14px;color:var(--sub);font-weight:500}}
.kernel-box .res{{color:var(--soft);font-size:15px}}
.kernel-box .dom{{display:inline-block;font-family:var(--sans);font-weight:600;color:var(--ink);margin-right:.5em}}
@media(max-width:620px){{.kernel-box li{{grid-template-columns:1fr;gap:4px}}}}

/* strength bars */
.strength ul{{list-style:none;margin:24px 0 0;padding:0}}
.srow{{display:grid;grid-template-columns:minmax(0,1.5fr) 2.2fr auto;gap:18px;align-items:center;padding:11px 0;border-top:1px solid var(--line2)}}
.srow:first-child{{border-top:0}}
.slabel{{display:flex;flex-direction:column;line-height:1.25}}
.sname{{font-weight:600;font-size:14.5px}}
.ssub{{font-family:var(--mono);font-size:12px;color:var(--mut)}}
.sbar{{height:9px;background:var(--line2);border-radius:6px;overflow:hidden}}
.sbar span{{display:block;height:100%;background:var(--sub);border-radius:6px}}
.scount{{font-family:var(--mono);font-weight:600;font-size:15px;color:var(--ink);text-align:right;white-space:nowrap}}
.scount span{{color:var(--mut);font-weight:400;font-size:12px}}
@media(max-width:620px){{.srow{{grid-template-columns:1fr auto;gap:6px 14px}}.sbar{{grid-column:1/-1;order:3}}}}

/* architecture svg */
.map-figure{{margin:26px 0 0}}
.map-figure svg{{width:100%;height:auto;display:block}}
.map-cap{{font-size:13px;color:var(--mut);margin-top:10px;max-width:70ch}}

/* tiers + cards */
.volumes{{padding:54px 0 10px}}
.volumes>.wrap>.eyebrow{{margin-bottom:.2em}}
.volumes h2.sect{{font-family:var(--serif);font-weight:600;font-size:clamp(1.5rem,2.6vw,2.1rem);margin:.05em 0 .3em}}
.volumes p.sect-sub{{color:var(--soft);max-width:64ch;margin:0 0 8px}}
.tier{{padding:34px 0;border-top:1px solid var(--line)}}
.tier-head{{max-width:64ch;margin-bottom:20px}}
.tier-head h2{{font-family:var(--serif);font-weight:600;font-size:1.5rem;margin:.05em 0 .35em;letter-spacing:-.01em}}
.tier-intro{{color:var(--soft);font-size:15.5px;margin:0}}
.tier--bridge .tier-head h2{{color:var(--bridge)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(316px,1fr));gap:16px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 18px 16px;display:flex;flex-direction:column;transition:border-color .15s,transform .15s}}
.card:hover{{border-color:#c9cec6;transform:translateY(-1px)}}
.card h3{{margin:0 0 .35em;font-size:1.12rem;font-family:var(--serif);font-weight:600;line-height:1.25}}
.card h3 a{{color:var(--ink)}}
.card h3 a:hover{{color:var(--sub);text-decoration:none}}
.card .hl{{margin:.1em 0 .7em;font-family:var(--mono);font-size:12.7px;line-height:1.5;color:var(--soft)}}
.tags{{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0 0 .7em;padding:0}}
.tags li{{font-size:11.5px;color:var(--sub);background:#eef4f8;border:1px solid #dce8f0;border-radius:20px;padding:.12em .6em;letter-spacing:.01em}}
.gbar{{margin:0 0 .6em;display:flex;flex-wrap:wrap;gap:6px}}
.gr{{font-size:11px;font-weight:600;border-radius:5px;padding:.1em .45em;letter-spacing:.02em}}
.gr-f{{color:var(--g-f);background:#e8f3ea}}
.gr-v{{color:var(--g-v);background:#e8f1f7}}
.gr-o{{color:var(--g-o);background:#f6ece2}}
.card .doi{{margin:auto 0 0;padding-top:.5em;font-size:11.8px;color:var(--mut);border-top:1px solid var(--line2)}}
.card .doi a{{font-family:var(--mono);color:var(--sub)}}
.card .np{{font-family:var(--mono)}}
.card--bridge{{border-color:#e7cf95;background:linear-gradient(0deg,var(--bridge-bg),#fff 60%)}}
.card--bridge h3 a{{color:var(--bridge)}}

/* method / honesty */
.cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:22px;margin-top:24px}}
.col h3{{font-family:var(--sans);font-size:14px;letter-spacing:.04em;text-transform:uppercase;color:var(--mut);margin:0 0 .4em;font-weight:600}}
.col p{{margin:0;color:var(--soft);font-size:15px}}
.col .mono{{font-size:13px;color:var(--ink)}}
.pull{{font-family:var(--serif);font-size:clamp(1.2rem,2.4vw,1.6rem);line-height:1.35;color:var(--ink);max-width:24ch;margin:0;font-weight:500}}
.pull em{{font-style:italic;color:var(--bridge)}}
.honesty .inner{{display:grid;grid-template-columns:1fr 1.3fr;gap:40px;align-items:start}}
@media(max-width:760px){{.honesty .inner{{grid-template-columns:1fr;gap:22px}}}}

/* footer */
footer.site-foot{{background:#101418;color:#c5cbd1;padding:48px 0 40px;font-size:14px}}
footer.site-foot a{{color:#9cc6e6}}
footer.site-foot h4{{font-family:var(--sans);font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;color:#7f8893;margin:0 0 14px;font-weight:600}}
.foot-grid{{display:grid;grid-template-columns:1.1fr 2fr;gap:40px}}
@media(max-width:760px){{.foot-grid{{grid-template-columns:1fr;gap:28px}}}}
.foot-intro p{{margin:0 0 1em;color:#aeb6bf;max-width:42ch}}
.doi-list{{list-style:none;margin:0;padding:0;columns:2;column-gap:34px}}
.doi-list li{{break-inside:avoid;margin:0 0 .55em;font-size:13px;line-height:1.4}}
.doi-list .dl{{display:block;font-family:var(--mono);font-size:11.5px;color:#6f788a}}
@media(max-width:520px){{.doi-list{{columns:1}}}}
.foot-meta{{margin-top:34px;padding-top:20px;border-top:1px solid #242a30;color:#7f8893;font-size:12.5px;display:flex;flex-wrap:wrap;gap:18px}}
.foot-meta a{{color:#9aa3ad}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site">
  <div class="wrap">
    <span class="brand">Jamming Physics<span class="dot">.</span></span>
    <nav class="nav">
      <a href="#kernel">The kernel</a>
      <a href="#strength">Connections</a>
      <a href="#map">Architecture</a>
      <a href="#volumes">30 volumes</a>
      <a href="#method">Method</a>
      <a href="https://orcid.org/0009-0002-7535-8245" rel="noopener">ORCID</a>
    </nav>
  </div>
</header>

<main id="main">

<section class="hero">
  <div class="wrap">
    <p class="eyebrow">A single-substrate physical framework · CC BY 4.0</p>
    <h1>One substrate. One switch. <em>Thirty volumes</em>, from the vacuum to disease.</h1>
    <p class="lead">The VP framework models the vacuum as a jammed elastic solid. Its bistable R19 switch is the single kernel behind every volume — and a material stiffness <span class="mono">γ</span>, measured from DNA and never fitted, carries it from physics into all of biology.</p>
    <div class="stamp"><b>ṡ = g·s − s³ + h</b> <span>the R19 bistable switch</span></div>
    <div class="facts">
      <div class="fact"><b>30</b><span>open-access volumes</span></div>
      <div class="fact"><b>{_C.get("R19",0)}/30</b><span>share the R19 switch</span></div>
      <div class="fact"><b>{_C.get("emergence",0)}/30</b><span>emerge from measured <i class="lc">γ</i></span></div>
      <div class="fact"><b>0</b><span>fitted parameters</span></div>
    </div>
    <p class="meta">Young Jae Lee · <a href="https://orcid.org/0009-0002-7535-8245" rel="noopener">ORCID 0009-0002-7535-8245</a> · independent researcher · every volume an independent Zenodo DOI · <a href="/llms.txt">llms.txt</a> · <a href="/sitemap.xml">sitemap</a></p>
  </div>
</section>

<section class="band" id="kernel">
  <div class="wrap">
    <p class="eyebrow">The kernel</p>
    <h2>Everything here is one equation, specialized</h2>
    <div class="prose">
      <p>Begin with a single physical claim: the vacuum is a <strong>jammed elastic solid</strong> — space filled by rigid constituents frozen at random close packing, so the speed of light is its elastic-wave speed, <span class="kbd">c² = B/ρ</span>. On that medium sits one object, a bistable double-well written in normal form as the cubic <span class="kbd">ṡ = g·s − s³ + h</span> — the <strong>R19 switch</strong>.</p>
      <p>Biology does not add new physics. Each gene’s promoter has a measurable stiffness <span class="kbd">γ = −mean nearest-neighbour stacking ΔG</span> (SantaLucia), and that single measured number sets the switch: its threshold scales as <span class="kbd">spinodal ∝ γ^1.5</span> and its barrier as <span class="kbd">γ²/4</span>. Nothing is tuned to fit an outcome — <strong>γ is read from the genome and used as-is</strong>.</p>
      <p>From there the same cubic specializes. The list below is not an analogy between fields; it is the identical equation, operated differently.</p>
    </div>

    <div class="kernel-box" role="group" aria-label="One cubic specialized five ways">
      <div class="kernel-eq">
        <div class="e">ṡ = g·s − s³ + h</div>
        <div class="c">one cubic — specialized five ways</div>
      </div>
      <ul>
{spec_rows()}
      </ul>
    </div>
  </div>
</section>

<section class="band strength" id="strength">
  <div class="wrap">
    <p class="eyebrow">Connection strength · measured across all 30 volumes</p>
    <h2>How tightly the volumes are bound</h2>
    <div class="prose"><p>These are not loose thematic links. A full-text scan of every volume shows the shared primitives appearing almost everywhere — the same switch, the same measured stiffness, the same emergence recipe. The bars below count how many of the 30 volumes carry each primitive.</p></div>
    <ul>
{strength_rows()}
    </ul>
  </div>
</section>

<section class="band" id="map">
  <div class="wrap">
    <p class="eyebrow">Architecture</p>
    <h2>Non-biological physics, the DNA bridge, then biology</h2>
    <div class="prose"><p>The volumes are ordered by derivation, not discipline. Seven non-biological volumes fix the substrate; the DNA volume is the hinge where the switch meets a measured genome; and twenty-two biological volumes emerge beneath it — every organ from its master gene’s measured γ.</p></div>
    <figure class="map-figure">
      {{MAP_SVG}}
      <figcaption class="map-cap">Click any tier in the list below to open its volumes. Colour marks the three zones: the physical substrate (blue), the DNA bridge (amber), and the emerged biology (teal).</figcaption>
    </figure>
  </div>
</section>

<section class="volumes" id="volumes">
  <div class="wrap">
    <p class="eyebrow">The library</p>
    <h2 class="sect">Thirty volumes, one derivation order</h2>
    <p class="sect-sub">Each card carries the volume’s headline result, the shared primitives it uses, its graded-claim ledger where present, and a permanent Zenodo DOI. Non-biological foundation first; biology emerges below the DNA bridge.</p>
{tiers_html}
  </div>
</section>

<section class="band" id="method">
  <div class="wrap">
    <p class="eyebrow">Method &amp; governance</p>
    <h2>Why the numbers can be trusted</h2>
    <div class="cols">
      <div class="col"><h3>No tuning</h3><p>Every quantity is measured or derived. <span class="mono">γ</span> comes from NCBI promoters; it is never fitted to reproduce a result. A number with no reproduction path is marked, not assumed.</p></div>
      <div class="col"><h3>LOCK → Derive → Gate</h3><p>Inputs are locked, outputs are produced by deterministic code, and counts are checked against the canonical HTML. Re-running yields a byte-identical result (<span class="mono">SEED = 19</span>, 2×SHA-256).</p></div>
      <div class="col"><h3>Honest grading</h3><p>Each claim is graded in the open: <span class="mono" style="color:var(--g-f)">[F]</span> forced, <span class="mono" style="color:var(--g-v)">[V]</span> verified, <span class="mono">[L]</span> anchored, <span class="mono" style="color:var(--g-o)">[O]</span> open — every <span class="mono">[O]</span> states its specific obstacle.</p></div>
      <div class="col"><h3>Magnitude firewall</h3><p>For disease and therapy the framework gives <strong>direction only</strong>. Clinical magnitudes are deliberately withheld <span class="mono">[O]</span> — a corrective lever, never a dose.</p></div>
    </div>
  </div>
</section>

<section class="band honesty">
  <div class="wrap inner">
    <p class="pull">A falsification is not a failure here. <em>It is a finding</em> — recorded with the same weight as a success.</p>
    <div class="prose">
      <p>The framework states where it reaches and where it stops. Human aging genes come out <strong>not special</strong> (|z| &lt; 1); a falsifiable test finds γ <strong>orthogonal</strong> to developmental timing; the origin of subjective experience is marked <strong>open</strong>, not solved. These negatives are kept in the open ledger rather than smoothed away.</p>
      <p>Scientific honesty is treated as more valuable than completeness. The aim is a single substrate that survives its own tests — and an explicit record wherever it does not.</p>
    </div>
  </div>
</section>

</main>

<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-intro">
      <h4>Jamming Physics</h4>
      <p>The vacuum as a jammed elastic solid: one measured substrate and one bistable switch, projected across thirty open-access volumes from physics to disease.</p>
      <p>Young Jae Lee · <a href="https://orcid.org/0009-0002-7535-8245" rel="noopener">ORCID</a> · CC BY 4.0</p>
      <p><a href="/llms.txt">llms.txt</a> · <a href="/sitemap.xml">sitemap.xml</a></p>
    </div>
    <div class="foot-dois">
      <h4>All 30 volumes · permanent DOIs</h4>
      <ul class="doi-list">
{doi_index()}
      </ul>
    </div>
  </div>
  <div class="wrap"><div class="foot-meta">
    <span>© Young Jae Lee · CC BY 4.0</span>
    <span>Each volume is an independent open-access work with its own Zenodo DOI.</span>
    <span>Verification code lives in <span class="mono">/repro/</span> (not web-served).</span>
  </div></div>
</footer>
</body>
</html>
'''

_svg = open(_find('tools/map.svg','map.svg'),encoding='utf-8').read().strip()
PAGE = PAGE.replace('{MAP_SVG}', _svg)
os.makedirs('docs', exist_ok=True)
open('docs/index.html','w',encoding='utf-8').write(PAGE)
print("wrote docs/index.html:", len(PAGE), "bytes")
print("cards:", sum(len(v) for v in TIER_VOLS.values()))
print("strength counts:", {n:c for n,_,c in STRENGTH})
