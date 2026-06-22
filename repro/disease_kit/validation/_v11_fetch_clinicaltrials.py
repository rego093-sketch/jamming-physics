#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_v11_fetch_clinicaltrials.py  --  validation.v11 NOVELTY AUDIT external oracle fetch + PRE-REGISTRATION.

  Blueprint §5.3 "Novelty audit": of the kit's `novel` leads, how many are independently PLAUSIBLE
  (the drug is under INVESTIGATION for that disease, or for a pre-registered related condition) vs
  purely STRUCTURAL?  Distinguish *genuine repurposing lead* from *structural artifact* (§5.4).

  ORACLE.  ClinicalTrials.gov API v2 -- a registry of *investigation*.  This is categorically
  INDEPENDENT of every V3-V8 pharmacology source (DGIdb / ChEMBL / GtoPdb / DrugCentral / MED-RT):
  it does not annotate a drug's TARGET (V3-V7 axis) nor an APPROVED indication (V8 axis); it records
  whether a (drug, condition) pair has ever been entered into a registered clinical study.  That is
  precisely the "is the field already pursuing this lead" signal a novelty audit needs.

  MAGNITUDE-FREE BY CONSTRUCTION.  We read ONLY: nctId, conditions[], interventions[{type,name}],
  phases[] (a categorical regulatory stage, e.g. PHASE2 -- not a magnitude, consistent with V10's
  maxClinicalStage), overallStatus (a categorical, e.g. COMPLETED).  briefTitle is DROPPED at fetch
  (titles routinely carry dose / "N patients" / "Phase 2" prose).  Enrollment counts, results,
  outcome values are NEVER requested.  The vendored snapshot is later scanned by the kit firewall
  (pipeline.firewall.magnitude_leak, verbatim) and must read PASS.

  MECHANICAL MATCH (no fuzzy trust).  ClinicalTrials.gov's search engine fuzzily expands queries; we
  do NOT trust that.  A returned trial counts as an in-disease hit for (agent, disease) ONLY iff a
  POST-FILTER passes: (a) some intervention name, FOLDED, is a superset of the agent's pre-registered
  required-token-set (drug present, rejecting same-family wrong-salt e.g. glycerol- vs sodium-
  phenylbutyrate), AND (b) some condition string, FOLDED, is a superset of one of the disease's
  pre-registered required-token-SETS (disease present, all distinguishing tokens; parent/umbrella
  conditions that lack a distinguishing token are rejected).  fold() is inherited VERBATIM from V8;
  token-overlap auto-binding is REJECTED, exactly as in V8.

  Output: V11_PREREGISTRATION.json (frozen classifier + bindings + metrics, hashed BEFORE results),
  and v11_clinicaltrials_snapshot.cache.json (the dated vendored oracle).  Deterministic; the holdout
  reads ONLY the vendored snapshot, so metrics are 2x byte-identical.  A fresh live re-pull is an
  off-manifest AUDIT sidecar (v11_external_refetch_audit.json), never on the manifest.
"""
import os, sys, json, re, hashlib, time, urllib.request, urllib.parse, ssl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import firewall as FW

SNAPSHOT = "2026-06-21"
RELEASE  = "0.41.0-validation.v11"
API      = "https://clinicaltrials.gov/api/v2/studies"

CR_PATH  = os.path.join(ROOT, "outputs", "candidate_register.json")
DI_PATH  = os.path.join(ROOT, "inputs",  "disease_inputs.json")
ML_PATH  = os.path.join(ROOT, "outputs", "mapped_levers.json")

PREREG_PATH = os.path.join(HERE, "V11_PREREGISTRATION.json")
SNAP_PATH   = os.path.join(HERE, "v11_clinicaltrials_snapshot.cache.json")

# ---- inherited inheritance anchors (must reproduce byte-identical; read-only premise) --------------
EXPECT = dict(
    disease_inputs_sha256   = "e9003054a4f7dc9c",          # prefix-checked
    mapped_levers_sha256    = "93ba3c89781f4952",
    register_chain_head     = "ca1796255c7c91db49cd28a11b15d49a649042c49a313649bcb63643d43c3fd3",
    v10_validation_head     = "1d668453b4d484a1d3f6f7255002065bd344e22cce13608b391b3c2a3a6da663",
    v10_prereg_sha256       = "2f2e85e88d3ca8e1c86be17d13e960caea90dc1351783fa84551bb40c5065d23",
)

# ---- helpers (canon/sha/fold inherited from the V8 holdout, verbatim semantics) -------------------
def canon(o):  return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def sha(o):    return hashlib.sha256(canon(o).encode("utf-8")).hexdigest()
def sha_file(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def jdump(p, o):
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(o, fh, indent=1, ensure_ascii=False, sort_keys=True)

def fold(text):
    """lowercase; ae->e, oe->e; non-alphanumeric -> space; per-token singularize (strip one
       trailing 's' if len>3); DROP single-character tokens (no identity); return frozenset.
       Identical to V8 fold() plus the single-char drop (pre-registered)."""
    t = text.lower().replace("ae", "e").replace("oe", "e")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    toks = []
    for w in t.split():
        if len(w) == 1:
            continue
        if len(w) > 3 and w.endswith("s"):
            w = w[:-1]
        toks.append(w)
    return frozenset(toks)

def fs(*words):
    """build a required-token frozenset from raw words (folded individually, single-char dropped)."""
    out = set()
    for w in words:
        out |= set(fold(w))
    return frozenset(out)

# =================================================================================================
# FROZEN PRE-REGISTRATION DATA  (assembled into V11_PREREGISTRATION.json and hashed BEFORE results)
# =================================================================================================

# ---- AGENT specs: ct.gov intervention query + required intervention-name token-sets (OR across) ----
# Each agent: query string for query.intr, and a list of folded token-sets; a trial intervention NAME
# must be a SUPERSET of at least one set to count as "drug present".
AGENT_SPECS = {
 "sodium phenylbutyrate":   dict(q="sodium phenylbutyrate",        req=[fs("sodium","phenylbutyrate")]),
 "ursodeoxycholic acid":    dict(q="ursodeoxycholic acid",         req=[fs("ursodeoxycholic")]),
 "N-acetylcysteine":        dict(q="acetylcysteine",               req=[fs("acetylcysteine")]),
 "TSHA-101":                dict(q="TSHA-101",                     req=[fs("tsha")]),
 "encaleret":               dict(q="encaleret",                    req=[fs("encaleret")]),
 "hydroxyurea":             dict(q="hydroxyurea",                  req=[fs("hydroxyurea"), fs("hydroxycarbamide")]),
 "flecainide":              dict(q="flecainide",                   req=[fs("flecainide")]),
 "infigratinib":            dict(q="infigratinib",                 req=[fs("infigratinib")]),
 "zorevunersen":            dict(q="zorevunersen OR STK-001",      req=[fs("zorevunersen"), fs("stk","001")]),
 "ambroxol":                dict(q="ambroxol",                     req=[fs("ambroxol")]),
 "DTX401":                  dict(q="DTX401",                       req=[fs("dtx401"), fs("dtx","401")]),
 "tranexamic acid":         dict(q="tranexamic acid",              req=[fs("tranexamic")]),
 "bevacizumab":             dict(q="bevacizumab",                  req=[fs("bevacizumab")]),
 "AMT-130":                 dict(q="AMT-130",                      req=[fs("amt130"), fs("amt","130")]),
 "FBX-101":                 dict(q="FBX-101",                      req=[fs("fbx101"), fs("fbx","101")]),
 "losartan":                dict(q="losartan",                     req=[fs("losartan")]),
 "ION440":                  dict(q="ION440",                       req=[fs("ion440"), fs("ion","440")]),
 "mRNA-3705":               dict(q="mRNA-3705",                    req=[fs("mrna3705"), fs("mrna","3705")]),
 "UX111":                   dict(q="UX111 OR ABO-102",             req=[fs("ux111"), fs("abo102"), fs("abo","102")]),
 "tralesinidase alfa":      dict(q="tralesinidase",                req=[fs("tralesinidase")]),
 "tolvaptan":               dict(q="tolvaptan",                    req=[fs("tolvaptan")]),
 "trametinib":              dict(q="trametinib",                   req=[fs("trametinib")]),
 "QR-1123":                 dict(q="QR-1123",                      req=[fs("qr1123"), fs("qr","1123")]),
 # CLASS -> documented prototype (pre-registered class->instance binding, flagged):
 "L-type calcium channel blocker":
                            dict(q="verapamil", req=[fs("verapamil")],
                                 note="CLASS->prototype: verapamil is the L-type CaV1.2 blocker investigated in Timothy syndrome (a curated, flagged class->instance binding)"),
}

# ---- DISEASE bindings: keyed by the EXACT register `name`.  ct query string + required condition
# token-SETS (OR across sets; a trial condition must be a SUPERSET of at least one set).  Distilled to
# distinguishing tokens; generic words (deficiency/disease/syndrome/type/...) and gene symbols/variants
# dropped where non-distinguishing.  tier: EXACT (unambiguous proper name), SPECIFIC (curated 1:1),
# GROUP (a subtype within a heading -- the conservative sensitivity stratum).
DISEASE_BINDINGS = {
 "Adenosine deaminase deficiency (ADA-SCID) OMIM 102700":
     dict(q="ADA-SCID adenosine deaminase deficiency", tier="SPECIFIC",
          sets=[fs("adenosine","deaminase"), fs("ada","scid")]),
 "Alpha-1-antitrypsin deficiency OMIM 613490":
     dict(q="alpha-1 antitrypsin deficiency", tier="EXACT", sets=[fs("antitrypsin")]),
 "Alpha-mannosidosis (MAN2B1 deficiency) OMIM 248500":
     dict(q="alpha-mannosidosis", tier="EXACT", sets=[fs("mannosidosis")]),
 "Autosomal dominant hypocalcaemia type 1 (CASR gain-of-function) OMIM 601198":
     dict(q="autosomal dominant hypocalcemia ADH1", tier="SPECIFIC",
          sets=[fs("autosomal","dominant","hypocalcemia"), fs("adh1"), fs("hypocalcemia","casr")]),
 "Autosomal dominant retinitis pigmentosa, RHO-related (adRP; RHO toxic gain-of-function / rhodopsin misfolding, e.g. P23H) OMIM 613731":
     dict(q="autosomal dominant retinitis pigmentosa RHO", tier="SPECIFIC",
          sets=[fs("autosomal","dominant","retinitis","pigmentosa"), fs("adrp"), fs("rho","retinitis","pigmentosa")]),
 "Bardet-Biedl syndrome (BBS1-predominant; a BBSome ciliopathy) OMIM 209900":
     dict(q="Bardet-Biedl syndrome", tier="EXACT", sets=[fs("bardet","biedl")]),
 "Beta-thalassaemia (beta-thalassaemia major / intermedia) OMIM 613985":
     dict(q="beta thalassemia", tier="EXACT", sets=[fs("beta","thalassemia")]),
 "Catecholaminergic polymorphic ventricular tachycardia (RYR2 gain-of-function) OMIM 604772":
     dict(q="catecholaminergic polymorphic ventricular tachycardia", tier="EXACT",
          sets=[fs("catecholaminergic","polymorphic","ventricular","tachycardia"), fs("cpvt")]),
 "Choroideremia (CHM / REP1) OMIM 303100":
     dict(q="choroideremia", tier="EXACT", sets=[fs("choroideremia")]),
 "Classical homocystinuria (cystathionine-beta-synthase deficiency) OMIM 236200":
     dict(q="homocystinuria cystathionine beta synthase", tier="SPECIFIC",
          sets=[fs("homocystinuria")]),
 "Congenital hyperinsulinism (K_ATP-channel; ABCC8 + KCNJ11) OMIM 256450":
     dict(q="congenital hyperinsulinism", tier="EXACT", sets=[fs("hyperinsulinism")]),
 "Crouzon syndrome (FGFR2 gain-of-function) OMIM 123500":
     dict(q="Crouzon syndrome", tier="EXACT", sets=[fs("crouzon")]),
 "Cystic fibrosis OMIM 219700":
     dict(q="cystic fibrosis", tier="EXACT", sets=[fs("cystic","fibrosis")]),
 "Dravet syndrome (SCN1A; NaV1.1 loss-of-function, GABAergic-interneuron haploinsufficiency) OMIM 607208":
     dict(q="Dravet syndrome", tier="EXACT", sets=[fs("dravet")]),
 "Duchenne muscular dystrophy OMIM 310200":
     dict(q="Duchenne muscular dystrophy", tier="EXACT", sets=[fs("duchenne")]),
 "Fabry disease OMIM 301500":
     dict(q="Fabry disease", tier="EXACT", sets=[fs("fabry")]),
 "Friedreich ataxia OMIM 229300":
     dict(q="Friedreich ataxia", tier="EXACT", sets=[fs("friedreich")]),
 "Gaucher disease OMIM 230800":
     dict(q="Gaucher disease", tier="EXACT", sets=[fs("gaucher")]),
 "Glycogen storage disease type Ia / von Gierke disease (G6PC1 deficiency) OMIM 232200":
     dict(q="von Gierke glycogen storage disease type Ia", tier="SPECIFIC",
          sets=[fs("von","gierke"), fs("glycogen","storage","ia"), fs("g6pc")]),
 "Hereditary angioedema (C1-inhibitor deficiency) OMIM 106100":
     dict(q="hereditary angioedema", tier="EXACT", sets=[fs("angioedema")]),
 "Hereditary haemorrhagic telangiectasia (Osler-Weber-Rendu) OMIM 187300":
     dict(q="hereditary hemorrhagic telangiectasia", tier="EXACT",
          sets=[fs("hemorrhagic","telangiectasia"), fs("osler","weber","rendu")]),
 "Huntington disease OMIM 143100":
     dict(q="Huntington disease", tier="EXACT", sets=[fs("huntington")]),
 "Krabbe disease (globoid-cell leukodystrophy) OMIM 245200":
     dict(q="Krabbe disease", tier="EXACT", sets=[fs("krabbe")]),
 "Leber congenital amaurosis type 2 (RPE65) OMIM 204100":
     dict(q="Leber congenital amaurosis RPE65", tier="SPECIFIC",
          sets=[fs("leber","congenital","amaurosis"), fs("rpe65")]),
 "Leptin receptor deficiency (severe early-onset obesity) OMIM 614963":
     dict(q="leptin receptor deficiency", tier="SPECIFIC", sets=[fs("leptin","receptor")]),
 "MECP2 duplication syndrome OMIM 300260":
     dict(q="MECP2 duplication syndrome", tier="EXACT", sets=[fs("mecp2","duplication")]),
 "Marfan syndrome (FBN1 deficiency) OMIM 154700":
     dict(q="Marfan syndrome", tier="EXACT", sets=[fs("marfan")]),
 "Methylmalonic acidaemia (MMUT deficiency) OMIM 251000":
     dict(q="methylmalonic acidemia", tier="EXACT", sets=[fs("methylmalonic")]),
 "Mucopolysaccharidosis type I (alpha-L-iduronidase deficiency; Hurler / Hurler-Scheie / Scheie syndrome; MPS I) OMIM 607014":
     dict(q="Hurler syndrome mucopolysaccharidosis I", tier="SPECIFIC",
          sets=[fs("hurler"), fs("scheie"), fs("mucopolysaccharidosis","i"), fs("mps","i")]),
 "Mucopolysaccharidosis type IIIA (Sanfilippo syndrome type A) OMIM 252900":
     dict(q="Sanfilippo syndrome type A MPS IIIA", tier="SPECIFIC",
          sets=[fs("mucopolysaccharidosis","iiia"), fs("sanfilippo","a")]),
 "Mucopolysaccharidosis type IIIB (Sanfilippo syndrome type B) OMIM 252920":
     dict(q="Sanfilippo syndrome type B MPS IIIB", tier="SPECIFIC",
          sets=[fs("mucopolysaccharidosis","iiib"), fs("sanfilippo","b")]),
 "Mucopolysaccharidosis type IIIC (Sanfilippo syndrome type C) OMIM 252930":
     dict(q="Sanfilippo syndrome type C MPS IIIC", tier="SPECIFIC",
          sets=[fs("mucopolysaccharidosis","iiic"), fs("sanfilippo","c")]),
 "Nephrogenic diabetes insipidus, X-linked (AVPR2 loss-of-function; vasopressin V2 receptor) OMIM 304800":
     dict(q="nephrogenic diabetes insipidus", tier="SPECIFIC",
          sets=[fs("nephrogenic","diabetes","insipidus")]),
 "Nephrogenic syndrome of inappropriate antidiuresis (NSIAD) -- AVPR2 gain-of-function (constitutively-active vasopressin V2 receptor; e.g. R137C/R137L, F229V, I130N) OMIM 300539":
     dict(q="nephrogenic syndrome of inappropriate antidiuresis", tier="SPECIFIC",
          sets=[fs("nephrogenic","inappropriate","antidiuresis"), fs("nsiad")]),
 "Noonan syndrome (PTPN11 gain-of-function) OMIM 163950":
     dict(q="Noonan syndrome", tier="EXACT", sets=[fs("noonan")]),
 "Pompe disease OMIM 232300":
     dict(q="Pompe disease", tier="EXACT", sets=[fs("pompe")]),
 "Pyruvate kinase deficiency (erythrocyte / liver pyruvate kinase deficiency; PKLR; chronic non-spherocytic haemolytic anaemia) OMIM 266200":
     dict(q="pyruvate kinase deficiency", tier="SPECIFIC",
          sets=[fs("pyruvate","kinase"), fs("pklr")]),
 "Rett syndrome OMIM 312750":
     dict(q="Rett syndrome", tier="EXACT", sets=[fs("rett")]),
 "Sandhoff disease (GM2 gangliosidosis, variant 0) OMIM 268800":
     dict(q="Sandhoff disease", tier="EXACT", sets=[fs("sandhoff")]),
 "Spinal muscular atrophy (5q SMA) OMIM 253300":
     dict(q="spinal muscular atrophy", tier="EXACT",
          sets=[fs("spinal","muscular","atrophy")]),
 "Tay-Sachs disease (GM2 gangliosidosis, variant B) OMIM 272800":
     dict(q="Tay-Sachs disease", tier="EXACT", sets=[fs("tay","sachs")]),
 "Timothy syndrome (CACNA1C, CaV1.2 gain) OMIM 601005":
     dict(q="Timothy syndrome", tier="SPECIFIC", sets=[fs("timothy","syndrome"), fs("timothy","cacna1c")]),
 "Usher syndrome type 2A (USH2A loss-of-function; usherin, the photoreceptor periciliary-membrane / hair-cell ankle-link complex protein) -- combined congenital sensorineural hearing loss + retinitis pigmentosa OMIM 276901":
     dict(q="Usher syndrome type 2A USH2A", tier="SPECIFIC",
          sets=[fs("usher","2a"), fs("ush2a")]),
 "X-linked retinitis pigmentosa (RPGR) OMIM 300029":
     dict(q="X-linked retinitis pigmentosa RPGR", tier="SPECIFIC",
          sets=[fs("x","linked","retinitis","pigmentosa","rpgr"), fs("rpgr"), fs("xlrp")]),
}

# ---- M3 related-class probes (BROAD agents only; conservative, NON-upgrading transparency stratum) --
# Question answered: is the broad generic agent investigationally LIVE somewhere in the mechanistic
# neighbourhood?  An in-class hit does NOT rescue any specific (broad-agent, disease) pair from the
# structural-artifact stratum -- the artifact diagnosis is precisely that the SAME agent is mapped to
# EVERY chaperonable gene -- so M3 is reported separately and never folded into the headline.
RELATED_CLASS_PROBES = {
 "lysosomal_misfolding_chaperone": dict(
     agents=["sodium phenylbutyrate", "ursodeoxycholic acid"],
     probes={  # canonical class diseases (each: ct query + required cond token-sets)
        "cystic fibrosis (CFTR misfolding)": dict(q="cystic fibrosis", sets=[fs("cystic","fibrosis")]),
        "Gaucher disease":                   dict(q="Gaucher disease",  sets=[fs("gaucher")]),
        "Fabry disease":                     dict(q="Fabry disease",    sets=[fs("fabry")]),
        "Pompe disease":                     dict(q="Pompe disease",    sets=[fs("pompe")]),
        "urea cycle disorder":               dict(q="urea cycle disorder", sets=[fs("urea","cycle")]),
     }),
 "retinal_antioxidant": dict(
     agents=["N-acetylcysteine"],
     probes={
        "retinitis pigmentosa (any)": dict(q="retinitis pigmentosa", sets=[fs("retinitis","pigmentosa")]),
     }),
}

# =================================================================================================
def http_get(url, tries=4):
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vp-disease-kit-validation/0.41 (jamming-physics.org)"})
            with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
                return json.load(r)
        except Exception as e:
            last = e; time.sleep(1.5 * (i + 1))
    raise last

# dose/percent runs that the kit firewall flags -- redacted from stored strings (drug-IDENTITY tokens
# survive, so the mechanical fold-match is unaffected; the magnitude is not data we want).
_DOSE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:mg|mcg|µg|ug|ng|ml|dl|l|g|kg|iu|units?|u)\b(?:\s*/\s*\w+)?", re.I)
_PCT_RE  = re.compile(r"\d+(?:\.\d+)?\s*%")
def sanitize_magnitude(s):
    s = _DOSE_RE.sub(" ", s or "")
    s = _PCT_RE.sub(" ", s)
    return re.sub(r"\s{2,}", " ", s).strip()

def trim_study(s):
    """keep ONLY magnitude-free categorical fields; DROP briefTitle/enrollment/results/outcomes;
       redact dose/percent runs from condition & intervention strings (drug-ID tokens survive)."""
    ps  = s.get("protocolSection", {})
    nct = ps.get("identificationModule", {}).get("nctId", "")
    cond = [sanitize_magnitude(c) for c in (ps.get("conditionsModule", {}).get("conditions", []) or [])]
    des  = ps.get("designModule", {})
    phases = list(des.get("phases", []) or [])
    status = ps.get("statusModule", {}).get("overallStatus", "")
    interventions = []
    for it in ps.get("armsInterventionsModule", {}).get("interventions", []) or []:
        interventions.append({"type": it.get("type", ""), "name": sanitize_magnitude(it.get("name", ""))})
    return {"nctId": nct, "conditions": cond, "interventions": interventions,
            "phases": phases, "overallStatus": status}

def fetch_pair(intr_q, cond_q, page_size=50):
    """disease-scoped query (guarantees a rare in-disease match surfaces); trimmed records."""
    params = {"query.intr": intr_q, "query.cond": cond_q, "pageSize": str(page_size),
              "fields": "NCTId,Condition,InterventionName,InterventionType,Phase,OverallStatus"}
    url = API + "?" + urllib.parse.urlencode(params)
    d = http_get(url)
    return [trim_study(s) for s in d.get("studies", []) or []]

def superset_hit(name_tokens_list, req_sets):
    """True iff some folded name in the list is a SUPERSET of at least one required set."""
    for toks in name_tokens_list:
        for rs in req_sets:
            if rs and rs <= toks:
                return True
    return False

def main():
    cr = json.load(open(CR_PATH))
    novel = [r for r in cr["rows"] if r["prior_art_status"] == "novel"]

    # -- inheritance anchor re-check (read-only premise) --
    di_h = sha_file(DI_PATH); ml_h = sha_file(ML_PATH)
    anchors_ok = (di_h.startswith(EXPECT["disease_inputs_sha256"]) and
                  ml_h.startswith(EXPECT["mapped_levers_sha256"]) and
                  cr["chain_head"] == EXPECT["register_chain_head"])
    assert anchors_ok, f"INHERITANCE ANCHOR MISMATCH di={di_h[:16]} ml={ml_h[:16]} head={cr['chain_head'][:16]}"

    def base(a): return re.split(r"[\(\[]", a)[0].strip()

    # -- agent -> #novel diseases (specificity stratification; internal, deterministic) --
    from collections import defaultdict
    agent_dis = defaultdict(set)
    for r in novel:
        agent_dis[base(r["agent"])].add(r["name"])
    SPECIFICITY_K = 3  # pre-registered: agent mapped to > K novel diseases via one family => BROAD-FAMILY

    # ---------- assemble + FREEZE the pre-registration (hash BEFORE any results) ----------
    def setlist(sets): return sorted([sorted(s) for s in sets])
    prereg = dict(
        programme="jamming-physics.org / VP Disease Emergence Kit",
        author="Young Jae Lee", orcid="0009-0002-7535-8245", licence="CC BY 4.0",
        release=RELEASE, round="V11", snapshot_date=SNAPSHOT,
        section="00_CONTINUATION_BLUEPRINT.md §5.3 'Novelty audit' -- of `novel` leads, how many are "
                "independently plausible (under investigation in-disease / related condition) vs purely structural (§5.4).",
        axis="drug<->DISEASE INVESTIGATION (a clinical-trial registry) -- NOT the drug<->target axis of "
             "V3-V7, NOT the approved-indication (may_treat) axis of V8.",
        target_set=dict(label="the kit's `novel` candidate rows (direction-only untested [O] hypotheses)",
                        n_rows=len(novel), n_agents=len(agent_dis), n_diseases=len(DISEASE_BINDINGS),
                        source="outputs/candidate_register.json :: rows where prior_art_status=='novel'"),
        ground_truth=dict(
            source="ClinicalTrials.gov (U.S. NLM clinical-study registry)",
            api="ClinicalTrials.gov API v2 /studies (query.intr + query.cond, disease-scoped)",
            independence="a registry of INVESTIGATION; annotates neither drug target (V3-V7) nor approved "
                         "indication (V8); independent of DGIdb/ChEMBL/GtoPdb/DrugCentral/MED-RT.",
            magnitude_free="ONLY nctId, conditions[], interventions[type,name], phases[] (categorical "
                           "regulatory stage), overallStatus (categorical). briefTitle DROPPED; enrollment/"
                           "results/outcome values NEVER requested. Snapshot scanned by kit firewall -> PASS.",
            snapshot_file=os.path.basename(SNAP_PATH)),
        mechanical_match=dict(
            principle="trust NO fuzzy engine expansion; a trial counts ONLY if a post-filter passes.",
            drug_present="some intervention NAME, folded, is a SUPERSET of >=1 pre-registered agent token-set "
                         "(rejects wrong-salt same-family, e.g. glycerol- vs sodium-phenylbutyrate).",
            disease_present="some CONDITION, folded, is a SUPERSET of >=1 pre-registered disease token-set "
                            "(parent/umbrella conditions lacking a distinguishing token are REJECTED).",
            fold_rule="lowercase; ae->e, oe->e; non-alphanumeric->space; per-token singularize; DROP single-"
                      "char tokens; order-insensitive frozenset (V8 fold() + single-char drop).",
            token_overlap_auto_binding="REJECTED (inherited from V8).",
            superset_semantics="OR across a disease's token-SETS; AND within a set."),
        agent_specs={a: dict(query=v["q"], required_token_sets=setlist(v["req"]),
                             note=v.get("note", ""), n_novel_diseases=len(agent_dis.get(a, [])),
                             stratum=("BROAD_FAMILY" if len(agent_dis.get(a, [])) > SPECIFICITY_K else "SPECIFIC"))
                     for a, v in AGENT_SPECS.items()},
        disease_bindings={d: dict(query=v["q"], tier=v["tier"], required_token_sets=setlist(v["sets"]))
                          for d, v in DISEASE_BINDINGS.items()},
        related_class_probes={cls: dict(agents=spec["agents"],
                                        probes={p: dict(query=pv["q"], required_token_sets=setlist(pv["sets"]))
                                                for p, pv in spec["probes"].items()})
                              for cls, spec in RELATED_CLASS_PROBES.items()},
        specificity_threshold_K=SPECIFICITY_K,
        metrics=dict(
            M1_in_disease="of the N_novel pairs, the fraction with >=1 mechanically-verified in-disease "
                          "registered trial (drug-token AND disease-token both present). Full hit list w/ NCT, "
                          "phase (categorical), status. THE HEADLINE plausibility signal.",
            M2_specificity="pre-registered split SPECIFIC (agent->K or fewer novel diseases) vs BROAD_FAMILY "
                           "(agent->more than K via one generic family); M1 within each stratum => the §5.4 "
                           "genuine-lead vs structural-artifact contrast made EMPIRICAL.",
            M3_related_class="BROAD agents only: is the generic agent investigationally live in a pre-registered "
                             "related class? Reported SEPARATELY; NON-upgrading (never rescues a specific pair "
                             "from the structural stratum); a judgment-bounded transparency note.",
            M4_structural_residue="pairs with no in-disease signal, listed in full: externally-UNTESTED "
                                  "structural [O] hypotheses -- flagged & down-weighted (§5.4), NOT refuted.",
            cross_tab="re-affirm V8 novel|approved-indication=0 (these are NOT approved indications) and report "
                      "a rediscovery-set in-disease sanity floor (rediscovery pairs SHOULD carry trials)."),
        verdict_rule="report rates WITH denominators and the full miss/residue lists; an in-disease trial is "
                     "plausibility corroboration of a CORRECTLY-LABELLED novel lead (investigational != approved), "
                     "never a treatment claim; no naked 'most are plausible'.",
        expected="SPECIFIC agents (named gene-therapies/ASOs/targeted drugs developed FOR these diseases) carry "
                 "high in-disease investigation; BROAD chaperones (one generic stabiliser mapped to every "
                 "chaperonable gene) carry low/zero in-disease investigation => structural-artifact stratum "
                 "identified empirically. Under-count is expected & acceptable (acronym-only conditions, ultra-"
                 "rare indications) -- it biases AGAINST the kit, never for it.",
        inheritance_discipline=dict(
            derivation="READ-ONLY over the frozen 128-core (0 re-runs); inherited anchors re-checked byte-identical.",
            anchors=EXPECT,
            chain="APPEND-ONLY, continuing the V10 validation chain head.",
            invariants="firewall PASS (kit magnitude_leak verbatim); every emitted string magnitude-free.",
            source="vendored dated snapshot (sha recorded in results); a live re-pull is an off-manifest audit."),
        continues_from=dict(round="V10", v10_validation_chain_head=EXPECT["v10_validation_head"],
                            v10_prereg_sha256=EXPECT["v10_prereg_sha256"]),
        pre_registered_next_batch=[
            "the §5.3 four-metric ledger is then COMPLETE in-house (direction-recovery V3-V7, exclusion-"
            "calibration V10, novelty V11); the only remaining §5.3 item is PROSPECTIVE falsification -- an "
            "inherently external, append-only log of which falsifiers others test and the outcome (not an "
            "in-house round).",
            "Track-A coverage expansion on the burden-weighted dual-track roadmap (§11) -- all four audit rigs "
            "(direction, indication, level/shape, novelty) now stand to gate new in-model diseases.",
            "a finer-granularity investigational oracle (EU-CTR / WHO ICTRP) to widen the small but fully "
            "human-warranted denominator, should it become reachable."],
    )
    prereg_sha = sha(prereg)
    prereg_out = dict(prereg); prereg_out["prereg_sha256"] = prereg_sha
    jdump(PREREG_PATH, prereg_out)
    print(f"[prereg] V11_PREREGISTRATION.json written  prereg_sha={prereg_sha[:16]}…")
    print(f"[prereg] novel pairs={len(novel)}  agents={len(agent_dis)}  diseases={len(DISEASE_BINDINGS)}  K={SPECIFICITY_K}")

    # ---------- FETCH (disease-scoped per pair) ----------
    raw_by_pair = {}        # (agent_base, disease) -> [trimmed studies]
    fetched = 0
    pairs = sorted({(base(r["agent"]), r["name"]) for r in novel})
    for (ab, dn) in pairs:
        spec = AGENT_SPECS.get(ab); db = DISEASE_BINDINGS.get(dn)
        if not spec or not db:
            raw_by_pair[f"{ab} || {dn}"] = []; continue
        studies = fetch_pair(spec["q"], db["q"])
        raw_by_pair[f"{ab} || {dn}"] = studies
        fetched += 1
        time.sleep(0.25)
    print(f"[fetch] in-disease pair queries done: {fetched}/{len(pairs)}")

    # related-class probes (broad agents)
    raw_related = {}
    for cls, spec in RELATED_CLASS_PROBES.items():
        for ab in spec["agents"]:
            aspec = AGENT_SPECS[ab]
            for pname, pv in spec["probes"].items():
                key = f"{ab} || [{cls}] {pname}"
                raw_related[key] = fetch_pair(aspec["q"], pv["q"])
                time.sleep(0.25)
    print(f"[fetch] related-class probe queries done: {len(raw_related)}")

    snapshot = dict(
        meta=dict(release=RELEASE, snapshot_date=SNAPSHOT, source="ClinicalTrials.gov API v2",
                  prereg_sha256=prereg_sha,
                  fields_kept=["nctId", "conditions", "interventions(type,name)", "phases", "overallStatus"],
                  fields_dropped=["briefTitle", "enrollment", "results", "outcomes (magnitude risk)"],
                  note="disease-scoped queries; trimmed to magnitude-free categorical fields."),
        in_disease=raw_by_pair,
        related_class=raw_related,
    )
    jdump(SNAP_PATH, snapshot)
    snap_sha = sha_file(SNAP_PATH)
    print(f"[snap] {os.path.basename(SNAP_PATH)} written  snapshot_sha={snap_sha[:16]}…")

    # firewall the snapshot immediately (fail fast if any categorical string leaks)
    leaks = []
    for path, s in FW.walk_json_strings(snapshot):
        lk = FW.magnitude_leak((s or "").lower())
        if lk:
            leaks.append((path, s, lk))
    print(f"[firewall] snapshot scan: {'PASS' if not leaks else 'FAIL'} ({len(leaks)} leak-strings)")
    if leaks:
        for p, s, lk in leaks[:20]:
            print("   LEAK", lk, "::", p, "::", s[:80])

if __name__ == "__main__":
    main()
