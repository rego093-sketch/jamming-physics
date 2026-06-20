#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
carcinogen_dose_response.py  --  Digestive / Metabolic ONCOLOGY module.

VP-NATIVE CANCER MECHANISM (one shared kernel, instantiated per organ):
  A cell-fate is the SAME R19 bistable switch. A carcinogen is a SUSTAINED aberrant drive that biases
  the switch toward a malignant basin by LOWERING the effective barrier between the healthy well and
  the saddle. Cumulative exposure (dose x time) integrates the bias; the malignant-crossing rate is
  Kramers/Arrhenius over the EXACT R19 barrier:
        rate(g,h) = exp( -barrier_exact(g,h) / D ),   RR(dose) = rate(dose)/rate(0).
  DISCRIMINANT = the dose-response SHAPE vs a CITED epidemiological anchor (RR per intake / pack-year),
  and, for gastric, the infection x diet INTERACTION (departure from additivity).

KERNEL DETAILS:
  barrier_exact(g,h)  -- exact healthy-well -> saddle barrier of the cubic s^3 - g s - h = 0 (roots:
                         healthy=min, saddle=middle). Vanishes as ~(h_sp - h)^{3/2} at the spinodal;
                         this replaces the linear placeholder. Forced by the substrate [F].
  D                   -- ONE shared substrate noise scale = barrier(1.0)/6 for every site (not per-site).
  kappa (per site)    -- the only per-site number: it maps physical dose -> bias h, calibrated by
                         bisection to ONE cited anchor RR. No curve-shape tuning.

GRADES (C3): epidemiological anchor [L]; reproduced SHAPE / synergy [V]; ABSOLUTE incidence [O] (needs
  external population calibration -- mirrors organ SIZE being [O]). No silent claims.
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
import numpy as np
from vp_substrate import barrier, spinodal, metaplastic_scale, metaplasia_barrier_drop

# ---------------------------------------------------------------------------
#  EXACT R19 barrier under bias + Kramers crossing
# ---------------------------------------------------------------------------
def U(s, g, h):
    return -(g / 2.0) * s * s + 0.25 * s ** 4 - h * s

def barrier_exact(g, h):
    """Exact healthy-well -> saddle barrier of s^3 - g s - h = 0 under bias h (>0 biases toward the
    malignant basin s>0). Returns 0 once |h| reaches the spinodal (the healthy basin is gone)."""
    sp = spinodal(g)
    if abs(h) >= sp:
        return 0.0
    r = np.roots([1.0, 0.0, -g, -h])
    rr = sorted(x.real for x in r if abs(x.imag) < 1e-7)
    if len(rr) < 3:
        return 0.0
    healthy, saddle = rr[0], rr[1]
    return float(U(saddle, g, h) - U(healthy, g, h))

D_NOISE = barrier(1.0) / 6.0          # ONE shared substrate noise scale for every site

def crossing_rate(g, h, D=D_NOISE):
    return math.exp(-barrier_exact(g, h) / D)

def RR(g, h, g0=1.0, D=D_NOISE):
    """Relative risk vs the healthy baseline (g0, h=0)."""
    return crossing_rate(g, h, D) / crossing_rate(g0, 0.0, D)

def _calib_kappa(dose_anchor, RR_anchor, g=1.0, D=D_NOISE):
    """Bisection: find kappa (dose->bias slope) s.t. RR at the cited dose hits the cited RR."""
    lo, hi = 1e-6, spinodal(g) / dose_anchor * 0.999
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if RR(g, mid * dose_anchor, g, D) < RR_anchor: lo = mid
        else: hi = mid
    return (lo + hi) / 2.0

def _calib_h(RR_t, g=1.0, D=D_NOISE):
    lo, hi = 1e-6, spinodal(g) * 0.999
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if RR(g, mid, g, D) < RR_t: lo = mid
        else: hi = mid
    return (lo + hi) / 2.0

def _calib_g(RR_t, g0=1.0, D=D_NOISE):
    """Find a REDUCED barrier-scale g_Hp (chronic inflammation lowers cell-fate stability) giving the
    target RR at h=0."""
    lo, hi = 0.2, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if RR(mid, 0.0, g0, D) < RR_t: hi = mid
        else: lo = mid
    return (lo + hi) / 2.0

# ---------------------------------------------------------------------------
#  PER-SITE ANCHORS  (all [L], web-cited; see docs claim-strips for sources)
# ---------------------------------------------------------------------------
SITES = [
 {'site':'colorectal carcinoma','code':'crc',
  'carcinogens':'processed/red meat: heme iron, N-nitroso compounds, heterocyclic amines',
  'anchor':'IARC: RR ~1.18 per 50 g/day processed meat [L]; reproduced shape [V]',
  'dose_unit':'g/day processed meat','anchor_dose':50.0,'anchor_RR':1.18,
  'doses':[0,25,50,100,150]},
 {'site':'pancreatic carcinoma','code':'pdac',
  'carcinogens':'tobacco smoke (nitrosamines, PAHs)',
  'anchor':'Multiethnic Cohort: RR ~1.91 at 50 pack-years; current-smoker RR ~1.74 (Iodice 2008) [L]; shape [V]',
  'dose_unit':'pack-years','anchor_dose':50.0,'anchor_RR':1.91,
  'doses':[0,10,20,30,40,50]},
 {'site':'gastric carcinoma','code':'gca',
  'carcinogens':'H. pylori chronic inflammation x dietary N-nitroso / high salt',
  'anchor':'H. pylori OR ~2.5; high-salt/N-nitroso OR ~1.8; epidemiological SYNERGY (super-additive) [L]; interaction [V]',
  'dose_unit':'interaction (Hp x diet)','anchor_dose':None,'anchor_RR':None,
  'hp_alone_RR':2.5,'diet_alone_RR':1.8},
]

def dose_response(site):
    """Single-carcinogen sites: calibrate kappa to the anchor, return the RR curve over the dose grid."""
    k = _calib_kappa(site['anchor_dose'], site['anchor_RR'])
    curve = [(float(d), round(RR(1.0, k * d), 4)) for d in site['doses']]
    rrs = [v for _, v in curve]
    monotone = all(rrs[i + 1] > rrs[i] for i in range(len(rrs) - 1))
    convex = all(rrs[i + 2] - rrs[i + 1] >= rrs[i + 1] - rrs[i] - 1e-6 for i in range(len(rrs) - 2))
    anchor_hit = abs(dict(curve)[site['anchor_dose']] - site['anchor_RR']) < 0.02
    return dict(kappa=round(k, 8), curve=curve, monotone=monotone, convex=convex,
                anchor_hit=anchor_hit, grade_anchor="[L]", grade_shape="[V]", grade_absolute="[O]")

def gastric_synergy(site):
    """H. pylori = chronic inflammation lowering the barrier SCALE g; diet = additive bias h. The joint
    risk is read off the SAME exact barrier. Epidemiology reports a synergistic (super-additive)
    interaction; the model reproduces super-additivity and additionally PREDICTS sub-multiplicativity
    near the spinodal (diminishing returns at extreme dual exposure) -- a falsifiable prediction."""
    g_Hp = _calib_g(site['hp_alone_RR'])
    h_diet = _calib_h(site['diet_alone_RR'])
    rr_diet = RR(1.0, h_diet); rr_Hp = RR(g_Hp, 0.0); rr_both = RR(g_Hp, h_diet)
    add_null = rr_diet + rr_Hp - 1.0; mult_null = rr_diet * rr_Hp
    fan = []
    for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
        hd = h_diet * frac
        fan.append((int(frac * 100), round(RR(1.0, hd), 3), round(RR(g_Hp, hd), 3)))
    return dict(g_Hp=round(g_Hp, 4), h_diet=round(h_diet, 4),
                RR_diet_alone=round(rr_diet, 3), RR_Hp_alone=round(rr_Hp, 3), RR_joint=round(rr_both, 3),
                additive_null=round(add_null, 3), multiplicative_null=round(mult_null, 3),
                super_additive=bool(rr_both > add_null * 1.02),
                sub_multiplicative=bool(rr_both < mult_null),
                dose_response_fan=fan,
                grade_anchor="[L]", grade_interaction="[V]", grade_absolute="[O]")

def validate():
    """Full oncology check. PASS = every single-site curve monotone + anchor-locked, AND gastric
    interaction super-additive. Absolute incidence stays [O] (stated obstacle)."""
    crc = dose_response(SITES[0]); pdac = dose_response(SITES[1]); gca = gastric_synergy(SITES[2])
    rr30 = dict(pdac['curve'])[30.0]
    passed = bool(crc['monotone'] and crc['anchor_hit'] and
                  pdac['monotone'] and pdac['anchor_hit'] and (1.4 < rr30 < 2.0) and
                  gca['super_additive'])
    return dict(colorectal=crc, pancreatic=pdac, gastric=gca,
                pancreatic_RR_at_30py=rr30, shared_noise_scale_D=round(D_NOISE, 6),
                passed=passed)

def status():
    return {"kernel": "exact R19 barrier-lowering -> Kramers crossing -> RR(dose)",
            "sites": SITES, "shared_noise_scale_D": round(D_NOISE, 6),
            "status": "COMPLETE: barrier_exact derived, per-site anchors locked, exposure sweeps validated",
            "grades": "anchor [L] / shape & synergy [V] / absolute incidence [O] (needs population calibration)"}

# ===========================================================================
#  C6  --  NEOPLASTIC EXTENSION  (reuse the exact barrier-Kramers kernel above)
#
#  The same R19 cell-fate switch and the same Kramers crossing now span MORE sites by reusing the two
#  knobs already in the kernel -- a barrier-SCALE reduction g (chronic inflammation / a metaplastic
#  precursor compartment) and an additive BIAS h (a sustained carcinogenic drive) -- plus ONE new
#  reading of the substrate: a discrete METAPLASIA compartment (Barrett's / intestinal metaplasia),
#  `metaplastic_scale` / `metaplasia_barrier_drop`, vendored single-source in `inherited/vp_substrate.py`.
#  No new dynamics, no curve-fitting: each site is locked to ONE cited anchor by a single bisection.
#
#    (a) METAPLASIA-step cancers  -- a precursor compartment sits on a SMALLER R19 fate barrier, so the
#        malignant crossing is rate-limited ON the precursor; restoring g (ablation / removing the
#        injury) collapses the next-step rate. Barrett's->EAC and the gastric Correa cascade are the
#        SAME step on two organs.  [L] anchor / [V] shape & rate-limiting / [O] absolute %/yr & exact ladder.
#    (b) SYNERGY cancers          -- two drives read off the SAME exact barrier reproduce epidemiological
#        super-additivity AND additionally PREDICT sub-multiplicativity near the spinodal (a falsifiable
#        prediction). HCC = inflammation(g)xbias(h) [HBVxaflatoxin]; ESCC = bias(h)xbias(h) [smokexalcohol].
#        SAME structure as the gastric Hpxdiet interaction above.  [L]/[V]/[O].
#    (c) REVERSIBLE / SINGLE-DRIVER -- gastric MALT lymphoma is an Hp-driven g-reduction that REGRESSES
#        when g is restored (eradication); anal carcinoma is a single sustained HPV bias.  [L]/[V]/[O].
#    (d) OUT-OF-KERNEL (honest [O]) -- sites the carcinogen-Kramers kernel does NOT cover, each with a
#        stated obstacle and the owner that must supply the missing layer.
#
#  Treatment reading for ALL C6 (as section 13): the kernel makes PREVENTION / RISK-REDUCTION the lever --
#  remove the carcinogenic bias h, or raise the barrier scale g (eradicate Hp, ablate the metaplasia,
#  suppress reflux/HBV). Therapy of an ESTABLISHED tumour is out-of-model.
# ===========================================================================

def _calib_drop(RR_target, g_healthy=1.0):
    """Bisection: find the metaplasia g-DROP whose metaplastic compartment has a malignant-crossing rate
    RR_target times the healthy cell's (at h=0). One anchor, one bisection -- no shape tuning."""
    lo, hi = 1e-4, g_healthy - 0.05
    for _ in range(80):
        mid = (lo + hi) / 2.0
        rr = crossing_rate(metaplastic_scale(g_healthy, mid), 0.0) / crossing_rate(g_healthy, 0.0)
        if rr < RR_target: lo = mid
        else: hi = mid
    return (lo + hi) / 2.0

# ---- (a) metaplasia-step sites ----
META_SITES = [
 {'site':'esophageal adenocarcinoma','code':'eac','precursor':"Barrett's oesophagus (NDBE)",
  'driver':'chronic acid/bile reflux lowers the oesophageal fate-stability scale -> a metaplastic compartment',
  'precursor_vs_general_RR':11.0,
  'anchor':"Barrett's-vs-general EAC SIR ~11 (Hvid-Jensen 2011 NEJM); NDBE->EAC ~0.33%/yr (Desai 2012) [L]",
  'ladder':[("NDBE",1.0),("LGD",1.3),("HGD",1.6)]},
 {'site':'gastric carcinoma, intestinal type','code':'gca_int','precursor':'gastric intestinal metaplasia (GIM)',
  'driver':'chronic atrophic gastritis (H. pylori) lowers the gastric fate-stability scale (Correa cascade)',
  'precursor_vs_general_RR':3.6,
  'anchor':'intestinal metaplasia raises gastric-cancer risk ~3.6x (meta-analysis); GIM->cancer ~0.25%/yr Western [L]',
  'ladder':[("IM",1.0),("LGD",1.3),("HGD",1.6)]},
]

def metaplasia_progression(site):
    """Two-stage progression healthy -> metaplastic precursor -> carcinoma, both stages on the SAME exact
    R19 barrier. The precursor's g-drop is locked to the cited precursor-vs-general RR; the malignant
    crossing is then rate-limited on that smaller-barrier compartment. A dysplasia ladder (deeper g-drop)
    accelerates the rate (SHAPE [V] only -- exact ratios & absolute %/yr are [O]); restoring g (ablation /
    reflux or Hp removal) collapses the next-step rate back toward baseline (the treatment reading)."""
    drop = _calib_drop(site['precursor_vs_general_RR'])
    g_meta = metaplastic_scale(1.0, drop)
    rr_metaplastic = crossing_rate(g_meta, 0.0) / crossing_rate(1.0, 0.0)
    barrier_fold = barrier(1.0) / barrier(g_meta)
    # the precursor's next-step RATE fold IS the rate-limiting factor (why carcinoma ~only from the precursor)
    rate_limiting = bool(rr_metaplastic > 3.0)
    # dysplasia ladder: deeper g-drop -> faster crossing (shape/direction only)
    ladder = []
    for nm, mult in site['ladder']:
        gd = min(drop * mult, 0.95)
        rate = crossing_rate(metaplastic_scale(1.0, gd), 0.0) / crossing_rate(1.0, 0.0)
        ladder.append((nm, round(gd, 4), round(rate, 3)))
    lr = [r for _, _, r in ladder]
    ladder_monotone = all(lr[i + 1] > lr[i] for i in range(len(lr) - 1))
    ladder_accelerating = all(lr[i + 2] - lr[i + 1] > lr[i + 1] - lr[i] for i in range(len(lr) - 2))
    # treatment: restore g from g_meta back toward healthy -> rate collapses
    restore = [(int(f * 100), round(crossing_rate(g_meta + (1.0 - g_meta) * f, 0.0) / crossing_rate(1.0, 0.0), 3))
               for f in [0.0, 0.25, 0.5, 0.75, 1.0]]
    rstr = [v for _, v in restore]
    treatment_lowers_rate = all(rstr[i + 1] < rstr[i] for i in range(len(rstr) - 1)) and abs(rstr[-1] - 1.0) < 0.05
    anchor_hit = abs(rr_metaplastic - site['precursor_vs_general_RR']) < 0.05
    return dict(drop=round(drop, 4), g_meta=round(g_meta, 4),
                rr_metaplastic=round(rr_metaplastic, 3), barrier_fold=round(barrier_fold, 3),
                rate_limiting=rate_limiting, dysplasia_ladder=ladder,
                ladder_monotone=bool(ladder_monotone), ladder_accelerating=bool(ladder_accelerating),
                restore_curve=restore, treatment_lowers_rate=bool(treatment_lowers_rate),
                anchor_hit=bool(anchor_hit),
                grade_anchor="[L]", grade_shape="[V]", grade_absolute="[O]")

# ---- (b) synergy sites ----
SYNERGY_SITES = [
 {'site':'hepatocellular carcinoma','code':'hcc','kind':'inflammation_x_bias',
  'a_name':'HBV chronic infection','a_RR':7.3,'b_name':'dietary aflatoxin B1','b_RR':3.4,
  'cited_joint':59.4,
  'anchor':'aflatoxin RR ~3.4, HBsAg+ RR ~7.3, joint ~59 (Qian 1994 / Ross 1992, Shanghai) [L]; newer cohorts trend sub-multiplicative',
  'seam':'SEAM to circulatory (hepatic first-pass) -- cite, do not re-emerge'},
 {'site':'esophageal squamous cell carcinoma','code':'escc','kind':'bias_x_bias',
  'a_name':'tobacco smoking','a_RR':4.0,'b_name':'heavy alcohol','b_RR':5.0,
  'cited_joint':40.0,
  'anchor':'smoking RR ~4, heavy-alcohol RR ~5, combined heavy ~40x (case-control / Prabhu 2014 meta) [L]'},
]

def synergy_site(site):
    """Two carcinogenic drives read off the SAME exact barrier. Reproduces the cited super-additive
    interaction and PREDICTS sub-multiplicativity near the spinodal (diminishing returns at extreme dual
    exposure -- falsifiable). `inflammation_x_bias`: a chronic-infection g-drop x a dietary bias h
    (HCC = HBV x aflatoxin). `bias_x_bias`: two additive biases h (ESCC = smoke x alcohol)."""
    if site['kind'] == 'inflammation_x_bias':
        g_a = _calib_g(site['a_RR']); h_b = _calib_h(site['b_RR'])
        rr_a = RR(g_a, 0.0); rr_b = RR(1.0, h_b); rr_both = RR(g_a, h_b)
        fan = [(int(f * 100), round(RR(1.0, h_b * f), 3), round(RR(g_a, h_b * f), 3)) for f in [0.0, 0.25, 0.5, 0.75, 1.0]]
        params = dict(a_component=round(g_a, 4), b_component=round(h_b, 4))
    else:  # bias_x_bias
        h_a = _calib_h(site['a_RR']); h_b = _calib_h(site['b_RR'])
        rr_a = RR(1.0, h_a); rr_b = RR(1.0, h_b); rr_both = RR(1.0, h_a + h_b)
        fan = [(int(f * 100), round(RR(1.0, h_b * f), 3), round(RR(1.0, h_a + h_b * f), 3)) for f in [0.0, 0.25, 0.5, 0.75, 1.0]]
        params = dict(a_component=round(h_a, 4), b_component=round(h_b, 4))
    add_null = rr_a + rr_b - 1.0; mult_null = rr_a * rr_b
    out = dict(kind=site['kind'],
               RR_a_alone=round(rr_a, 3), RR_b_alone=round(rr_b, 3), RR_joint=round(rr_both, 3),
               additive_null=round(add_null, 3), multiplicative_null=round(mult_null, 3),
               cited_joint=site['cited_joint'],
               super_additive=bool(rr_both > add_null * 1.02),
               sub_multiplicative_prediction=bool(rr_both < mult_null),
               dose_response_fan=fan, fan_cols=("exposure_%_of_b", "RR_b_only", "RR_both"),
               grade_anchor="[L]", grade_interaction="[V]", grade_absolute="[O]")
    out.update(params)
    return out

# ---- (c) reversible (MALT) + single-driver (anal) ----
def reversible_site():
    """Gastric MALT lymphoma: an H. pylori chronic-inflammation g-reduction that REGRESSES when g is
    restored by eradication -- the kernel's signature falsifiable claim (raise the barrier scale -> the
    crossing rate collapses). ~90% Hp+, ~77.5% remission on eradication (Zullo 2010, 32 studies); the
    ~22% t(11;18)/API2-MALT1 non-responders are a g-INDEPENDENT driver -> owned by `disease_wp`."""
    g_Hp = _calib_g(6.0)
    rr_Hp = RR(g_Hp, 0.0)
    restore = [(int(f * 100), round(RR(g_Hp + (1.0 - g_Hp) * f, 0.0), 3)) for f in [0.0, 0.25, 0.5, 0.75, 1.0]]
    rstr = [v for _, v in restore]
    reversible = all(rstr[i + 1] < rstr[i] for i in range(len(rstr) - 1)) and abs(rstr[-1] - 1.0) < 0.05
    return dict(site='gastric MALT lymphoma', code='malt',
                g_Hp=round(g_Hp, 4), RR_Hp=round(rr_Hp, 3),
                restore_curve=restore, reversible_on_g_restore=bool(reversible),
                hp_positive_fraction=0.90, eradication_remission=0.775,
                independent_driver_nonresponse=True,
                anchor='~90% Hp+, ~77.5% eradication remission (Zullo 2010); ~22% t(11;18) g-independent [L]',
                grade_anchor="[L]", grade_shape="[V]", grade_absolute="[O]")

def single_driver_site():
    """Anal squamous cell carcinoma: a single sustained HPV (E6/E7) bias h. ~90% HPV-attributable
    (HPV16 ~80%, De Sanjose 2019); the bias is preventable (vaccination). Monotone RR with exposure."""
    h_HPV = _calib_h(8.0)
    curve = [(int(f * 100), round(RR(1.0, h_HPV * f), 3)) for f in [0.0, 0.25, 0.5, 0.75, 1.0]]
    rrs = [v for _, v in curve]
    monotone = all(rrs[i + 1] > rrs[i] for i in range(len(rrs) - 1))
    return dict(site='anal squamous cell carcinoma', code='anal',
                h_HPV=round(h_HPV, 4), curve=curve, monotone=bool(monotone),
                hpv_attributable_fraction=0.90,
                anchor='~90% HPV-attributable, HPV16 ~80% (De Sanjose 2019) [L]',
                grade_anchor="[L]", grade_shape="[V]", grade_absolute="[O]")

# ---- (d) honest out-of-kernel boundary ----
OUT_OF_KERNEL = [
 {'site':'GI stromal tumour (GIST)','reason':'KIT/PDGFRA gain-of-function gene-key driver, not a carcinogen bias',
  'obstacle':'no gene-key oncogenic-driver primitive in the carcinogen-Kramers kernel','owner':'disease_wp'},
 {'site':'gastroenteropancreatic NET / carcinoid','reason':'neuroendocrine lineage outside the epithelial fate switch (MEN1 subset gene-key)',
  'obstacle':'no neuroendocrine-differentiation layer','owner':'disease_wp (MEN1 subset)'},
 {'site':'small-bowel adenocarcinoma','reason':'rare, predisposition-driven (Crohn\'s / coeliac chronic inflammation)',
  'obstacle':'needs the C1 immune/inflammation layer to supply the barrier-lowering driver','owner':'me (via C1 bridge to the section-7 kernel)'},
 {'site':'cholangiocarcinoma','reason':'liver-fluke / PSC biliary-inflammation aetiology',
  'obstacle':'needs a hepatobiliary + immune layer; SEAM to circulatory','owner':'me (C4 hepatobiliary) + circulatory seam'},
]

def validate_c6():
    """C6 check. PASS = every metaplasia site anchor-locked + rate-limiting + ladder monotone +
    treatment lowers rate; every synergy site super-additive (with the sub-multiplicative prediction
    recorded); MALT reversible on g-restore; anal monotone. Absolute incidence stays [O] (stated obstacle)."""
    meta = {s['code']: metaplasia_progression(s) for s in META_SITES}
    syn = {s['code']: synergy_site(s) for s in SYNERGY_SITES}
    malt = reversible_site(); anal = single_driver_site()
    meta_ok = all(m['anchor_hit'] and m['rate_limiting'] and m['ladder_monotone'] and
                  m['ladder_accelerating'] and m['treatment_lowers_rate'] for m in meta.values())
    syn_ok = all(s['super_additive'] for s in syn.values())
    passed = bool(meta_ok and syn_ok and malt['reversible_on_g_restore'] and anal['monotone'])
    return dict(metaplasia=meta, synergy=syn, malt=malt, anal=anal,
                out_of_kernel=OUT_OF_KERNEL, shared_noise_scale_D=round(D_NOISE, 6),
                passed=passed)

def c6_status():
    return {"extension": "C6 neoplastic -- same barrier-Kramers kernel, more sites + a metaplasia compartment",
            "metaplasia_sites": [s['site'] for s in META_SITES],
            "synergy_sites": [s['site'] for s in SYNERGY_SITES],
            "reversible": "gastric MALT lymphoma (regresses on g-restore)",
            "single_driver": "anal SCC (HPV bias)",
            "out_of_kernel": [o['site'] for o in OUT_OF_KERNEL],
            "status": "COMPLETE: metaplasia step added, per-site anchors locked, synergy + reversibility validated",
            "grades": "anchor [L] / shape, rate-limiting & synergy [V] / absolute incidence & exact ladder [O]"}

def c6_digest():
    """Deterministic 2xsha256 of the full C6 validation payload (canonical json)."""
    payload = json.dumps(validate_c6(), sort_keys=True, ensure_ascii=False)
    import hashlib
    h1 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
    return payload, h2

if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
    print(json.dumps(validate_c6(), ensure_ascii=False, indent=2))
