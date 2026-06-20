#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D9.0  MODERATE-OR-BELOW AUTISM COHORT ACQUISITION (NCBI RefSeq -> promoter gamma)
================================================================================
The brief: build the THERAPY-RELEVANT cohort -- "not the severe pole, the moderate-
or-below pole" -- by fetching real autism risk genes from NCBI RefSeq (GRCh38) and
placing each on the R19 substrate by its promoter gamma (the LOCKED SantaLucia-1998
metric used by DNA M0 / neuro / the disease atlas). This cohort is what the candidate
threshold-lowering operators (D9.1-D9.4) are simulated on.

WHY "moderate-or-below", operationalised (PRE-REGISTERED, transparent -- declared
here, BEFORE any gamma is read or any candidate is run):

  A gene enters the cohort iff BOTH:
    (S1 clinical-severity floor)  its canonical presentation is NOT a severe
        developmental & epileptic encephalopathy (DEE) and NOT a defined severe
        syndrome named after the gene (Rett, Angelman, tuberous sclerosis,
        neurofibromatosis, Fragile-X full mutation, the chromatin/TF ID syndromes).
        Those are the EXTREME-T / profound pole -- exactly where a threshold-lowering
        chemical has NO traction and where over-lowering is most dangerous (the
        seizure direction on a brain already prone to it). They are listed in
        EXCLUDED_SEVERE with the reason, so the exclusion is auditable, not silent.
    (S2 fault-axis legibility)  its molecular function maps to one of the substrate
        fault axes the operator can be ABOUT: excitability / E-I (ION, GABA, GLU),
        synaptic gain (SYN scaffold, RNA splicing of synaptic genes), or long-range
        wiring (SYN adhesion). The W-axis genes are KEPT IN ON PURPOSE so D9.4 can
        demonstrate the honest null -- a chemical cannot fix wiring -- on REAL ASD
        genes, not a toy.

  "Severity" here therefore means "chemical-tractability tier under the VP D7/D8
  fault model, cross-checked against the clinical DEE / severe-syndrome gene list."
  It is NOT a clinical severity score we invent. ASD severity is heterogeneous and
  is OWED at the level of any individual (D8.5). The cohort is a MODELLING cohort.

GROUNDING (the gene is real, the gamma is re-derivable offline):
  * 15 genes load from the package's verified RefSeq cache (disease_gene_promoters.json,
    the 121-gene psychiatric atlas) and their gamma is RE-DERIVED OFFLINE here from the
    cached sequence by the locked metric -- proving the C1 reproduction path stays in
    the package and matches the atlas to 1e-9.
  * 2 genes are NOT in the atlas and are fetched LIVE from NCBI on --fetch
    (GABRA5 = the extrasynaptic tonic-GABA-A alpha-5 subunit, the precise molecular
    substrate of the A3 "tonic inhibition" lever; MACROD2 = a Grove-2019 genome-wide-
    significant COMMON-VARIANT ASD locus, the "below"/small-effect pole). Their
    sequence + sha256 are written to a local cohort cache so re-runs are offline and
    deterministic. This honours "actually fetch the gene from NCBI" while keeping the
    final reproduction path inside the package.

DISORDER-CODE NOTE (from the atlas map, verbatim): "ASD ... Engine link: D7/D8
coupling pathway + E-I (autism-T inhibitory pole)." The cohort is built to that link.

efficacy=0; this module ACQUIRES INPUTS only (gene identity + gamma); it makes no
treatment, dose, or efficacy claim. NOT medical advice. Governed by VP-SPEC v1.8
(C0-C4, SEED=19). ADD-ONLY; vp_mind_engine is imported READ-ONLY and untouched
(tree 0fbf4988...). 2x sha256 deterministic.
"""
import os, sys, json, math, hashlib, time, ssl, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY (constants/metric parity only)

ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"

ATLAS_CACHE  = os.path.join(HERE, "disease_gene_promoters.json")     # shipped 121-gene RefSeq cache
COHORT_CACHE = os.path.join(HERE, "cohort_extra_promoters.json")     # live-fetched extras (GABRA5, MACROD2)
RESULT       = os.path.join(HERE, "autism_cohort_moderate_results.json")
EXPECT       = os.path.join(HERE, "expected_autism_cohort_moderate_sha256.json")

# ---- the LOCKED gamma metric (SantaLucia 1998 NN; byte-identical to DNA M0 / atlas) ----
NN = {"AA": -1.00, "TT": -1.00, "AT": -0.88, "TA": -0.58, "CA": -1.45, "TG": -1.45,
      "GT": -1.44, "AC": -1.44, "CT": -1.28, "AG": -1.28, "GA": -1.30, "TC": -1.30,
      "CG": -2.17, "GC": -2.24, "GG": -1.84, "CC": -1.84}
ORG    = "Homo sapiens"
WINDOW = "[TSS-2000, TSS+500] = 2501 bp coding strand"

def gamma_of(seq):
    steps = [-NN[seq[i:i+2]] for i in range(len(seq) - 1) if seq[i:i+2] in NN]
    g  = float(sum(steps) / len(steps)) if steps else float("nan")
    gc = sum(c in "GC" for c in seq) / max(1, len(seq))
    return round(g, 4), round(gc, 4), len(seq)

# =====================================================================================
#  PRE-REGISTERED COHORT  (declared before any gamma is read)
#  axis: T = excitability/E-I (threshold)  ;  O = synaptic-gain (output)  ;  W = wiring
#  lever: A1 inward-excitatory (Nav/Cav)  ;  A2 outward-K (Kv7)  ;  A3 tonic-GABA-A
#         (lever only marks which threshold-lever a gene's channel/receptor IS;
#          O/W genes carry no lever -- they are gain/wiring, not a threshold handle)
# =====================================================================================
COHORT = {
    # --- excitability / E-I (T-axis); these ARE the threshold levers ---
    "SCN2A":   dict(cls="ION",  axis="T", lever="A1", src="SFARI-1; Nav1.2 LoF-ASD = milder O/T pole (DEE-GoF pole excluded)"),
    "CACNA1C": dict(cls="ION",  axis="T", lever="A1", src="Cav1.2 common-variant pole (Timothy-GoF excluded); cross-disorder"),
    "KCNQ3":   dict(cls="ION",  axis="T", lever="A2", src="Kv7.3; BFNE is self-limiting/benign = clearly moderate-or-below"),
    "GABRB3":  dict(cls="GABA", axis="T", lever="A3", src="GABA-A beta-3; the tonic-inhibition lever (E-I autism-T pole)"),
    "GABRA2":  dict(cls="GABA", axis="T", lever="A3", src="GABA-A alpha-2; inhibitory lever subunit"),
    # --- synaptic gain (O-axis) ---
    "SHANK3":  dict(cls="SYN",  axis="O", lever=None, src="D8.7 O-weak fault; postsynaptic scaffold (Phelan-McDermid, gain mechanism)"),
    "SHANK2":  dict(cls="SYN",  axis="O", lever=None, src="SFARI-1 scaffold; non-syndromic, milder than SHANK3"),
    "SYNGAP1": dict(cls="SYN",  axis="O", lever=None, src="synaptic Ras-GAP; gain regulator"),
    "NRXN1":   dict(cls="SYN",  axis="O", lever=None, src="neurexin-1 presynaptic; recurrent CNV, variable/milder"),
    "RBFOX1":  dict(cls="RNA",  axis="O", lever=None, src="splices synaptic-gain genes; ASD CNV (common-variant overlap)"),
    "CTTNBP2": dict(cls="SYN",  axis="O", lever=None, src="cortactin-binding; dendritic-spine gain"),
    # --- long-range wiring (W-axis) -- kept IN to demonstrate the honest null on real genes ---
    "CNTNAP2": dict(cls="SYN",  axis="W", lever=None, src="Caspr2 long-range adhesion; common-variant milder end"),
    "CNTN6":   dict(cls="SYN",  axis="W", lever=None, src="contactin-6 adhesion; CNV"),
    "DSCAM":   dict(cls="SYN",  axis="W", lever=None, src="adhesion / axon wiring"),
    "RELN":    dict(cls="SYN",  axis="W", lever=None, src="reelin lamination / wiring (cross-disorder candidate)"),
}
# genes fetched LIVE (not in the atlas cache) -- both moderate-or-below, both extend an axis
LIVE_FETCH = {
    "GABRA5":  dict(cls="GABA", axis="T", lever="A3", src="extrasynaptic GABA-A alpha-5 = the TONIC GABA-A current itself (A3 lever's exact substrate)"),
    "MACROD2": dict(cls="OTHER",axis="O", lever=None, src="Grove 2019 genome-wide-significant COMMON-VARIANT ASD locus = the 'below'/small-effect pole"),
}

# PRE-REGISTERED severe EXCLUSIONS (auditable -- why each is NOT in the moderate cohort)
EXCLUDED_SEVERE = {
    "MECP2": "Rett syndrome (severe regression)", "CDKL5": "CDKL5-deficiency DEE",
    "FOXG1": "FOXG1 syndrome (severe)", "UBE3A": "Angelman syndrome (severe)",
    "STXBP1": "DEE", "SCN1A": "Dravet (severe epilepsy)", "KCNT1": "severe epilepsy",
    "GRIN2B": "DEE (severe)", "CACNA1E": "DEE (severe)", "CHD2": "DEE",
    "TSC1": "tuberous sclerosis (severe syndrome)", "TSC2": "tuberous sclerosis",
    "NF1": "neurofibromatosis-1", "PTEN": "PTEN-hamartoma macrocephaly syndrome",
    "FMR1": "Fragile-X full mutation (moderate-severe ID syndrome)",
    "ADNP": "Helsmoortel-Van der Aa ID syndrome", "ARID1B": "Coffin-Siris syndrome",
    "FOXP1": "FOXP1 syndrome", "MED13L": "MED13L syndrome", "AUTS2": "AUTS2 syndrome",
    "CHD8": "macrocephaly/ID developmental master (W, syndromic)",
    "DYRK1A": "DYRK1A syndrome", "MAGEL2": "Schaaf-Yang syndrome",
}

# ----------------------------------- NCBI eutils (live fetch only; offline thereafter) ---
EU  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

def _get(u, tries=6):
    for k in range(tries):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "vp-autism-cohort"})
            return urllib.request.urlopen(req, timeout=60, context=CTX).read().decode()
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e):
                time.sleep(3 * (k + 1)); continue
            if k == tries - 1: raise
            time.sleep(1.5 * (k + 1))

def _coords(sym):
    term = urllib.parse.quote(f'{sym}[Gene Name] AND "{ORG}"[Organism]')
    ids = json.loads(_get(f"{EU}/esearch.fcgi?db=gene&term={term}&retmode=json")) \
        .get("esearchresult", {}).get("idlist", [])
    for gid in ids[:6]:
        time.sleep(0.34)
        try:
            doc = json.loads(_get(f"{EU}/esummary.fcgi?db=gene&id={gid}&retmode=json"))["result"][gid]
        except Exception:
            continue
        for g in doc.get("genomicinfo", []):
            if not g.get("chraccver", "").startswith("NC_"):
                continue
            a, b = int(g["chrstart"]), int(g["chrstop"])
            strand = "+" if a <= b else "-"
            gs, ge = (a, b) if strand == "+" else (b, a)
            return dict(official=doc.get("name", sym), acc=g["chraccver"],
                        strand=strand, chrstart=gs, chrstop=ge)
    return None

def _promoter(acc, gs, ge, strand):
    tss = gs if strand == "+" else ge
    lo, hi = (tss - 2000, tss + 500) if strand == "+" else (tss - 500, tss + 2000)
    u = (f"{EU}/efetch.fcgi?db=nuccore&id={acc}&rettype=fasta&retmode=text"
         f"&seq_start={lo + 1}&seq_stop={hi + 1}")
    txt = _get(u)
    return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()

def fetch_live():
    """One-time: fetch LIVE_FETCH genes from NCBI -> cohort_extra_promoters.json."""
    cache = json.load(open(COHORT_CACHE, encoding="utf-8")) if os.path.exists(COHORT_CACHE) else {
        "_what": "Live-fetched NCBI RefSeq (GRCh38) promoter cache for cohort genes NOT in the "
                 "121-gene psychiatric atlas. gamma re-derivable offline by the locked metric over " + WINDOW,
        "_window": WINDOW, "_metric": "gamma = mean(-NN dG37), SantaLucia 1998 (locked)",
        "_organism": ORG, "genes": {}}
    for sym in LIVE_FETCH:
        if sym in cache["genes"] and cache["genes"][sym].get("sequence"):
            print(f"  {sym:<9} already in cohort cache"); continue
        co = _coords(sym)
        if not co:
            print(f"  {sym:<9} NOT FOUND"); continue
        time.sleep(0.34)
        seq = _promoter(co["acc"], co["chrstart"], co["chrstop"], co["strand"])
        g, gc, L = gamma_of(seq)
        cache["genes"][sym] = dict(official_symbol=co["official"], acc=co["acc"], strand=co["strand"],
                                   chrstart=co["chrstart"], chrstop=co["chrstop"], promoter_len=L,
                                   promoter_sha256=hashlib.sha256(seq.encode()).hexdigest(),
                                   gamma=g, gc=gc, sequence=seq)
        json.dump(cache, open(COHORT_CACHE, "w", encoding="utf-8"), indent=1)
        print(f"  {sym:<9} LIVE gamma={g:.4f} gc={gc:.4f} {co['acc']} {co['strand']} len={L}")
        time.sleep(0.20)
    print(f"cohort extra cache -> {COHORT_CACHE}")

# ----------------------------------------------------------------------- offline assembly
def _load_gene(sym, ann):
    """Load a cohort gene's gamma, re-derived OFFLINE from its cached sequence."""
    atlas = json.load(open(ATLAS_CACHE, encoding="utf-8"))["genes"]
    extra = json.load(open(COHORT_CACHE, encoding="utf-8"))["genes"] if os.path.exists(COHORT_CACHE) else {}
    if sym in atlas:
        rec, where = atlas[sym], "atlas_cache"
    elif sym in extra:
        rec, where = extra[sym], "live_fetch_cache"
    else:
        return None
    g, gc, L = gamma_of(rec["sequence"])   # re-derive offline
    return dict(symbol=sym, gamma=g, gc=gc, promoter_len=L,
                gamma_matches_cache=bool(abs(g - rec["gamma"]) <= 1e-9),
                accession=rec["acc"], strand=rec["strand"],
                promoter_sha256=hashlib.sha256(rec["sequence"].encode()).hexdigest(),
                provenance=where, functional_class=ann["cls"],
                fault_axis=ann["axis"], lever=ann["lever"], basis=ann["src"])

def _round(o, nd=6):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, dict):  return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v, nd) for v in o]
    return o

def sha256_of(obj):
    return hashlib.sha256(json.dumps(_round(obj), sort_keys=True,
                          ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()

def run():
    E.seed_everything()
    full = {**COHORT, **LIVE_FETCH}
    genes, missing = {}, []
    for sym, ann in full.items():
        rec = _load_gene(sym, ann)
        if rec is None:
            missing.append(sym)
        else:
            genes[sym] = rec
    if missing:
        print(f"  MISSING (run --fetch): {missing}")

    # cohort statistics by axis (the gamma distribution that emerges the cohort cerebrum)
    by_axis = {}
    for ax in ("T", "O", "W"):
        gs = [genes[s]["gamma"] for s in genes if genes[s]["fault_axis"] == ax]
        if gs:
            by_axis[ax] = dict(n=len(gs), gamma_min=min(gs), gamma_max=max(gs),
                               gamma_mean=round(sum(gs) / len(gs), 6))
    all_g = [genes[s]["gamma"] for s in genes]
    lever_genes = {lv: sorted(s for s in genes if genes[s]["lever"] == lv) for lv in ("A1", "A2", "A3")}

    all_match = all(genes[s]["gamma_matches_cache"] for s in genes)

    out = {
        "_what": "D9.0 moderate-or-below autism cohort: 17 real ASD risk genes (15 from the verified "
                 "atlas cache, 2 live-fetched from NCBI), each placed on the R19 substrate by its "
                 "promoter gamma (locked SantaLucia-1998 metric, re-derived OFFLINE). Severity is "
                 "operationalised as chemical-tractability tier under the D7/D8 fault model, with severe "
                 "DEE/syndrome genes pre-registered as EXCLUDED. The gamma distribution here is the input "
                 "to D9.2 (cohort cerebrum) and the gene-grounded stiffness tags for D9.1/D9.3 candidates.",
        "preregistration": {
            "S1_clinical_severity_floor": "exclude severe DEE / defined severe syndrome (extreme-T/profound pole)",
            "S2_fault_axis_legibility": "include only ION/GABA/GLU/SYN/RNA whose mechanism maps to a substrate axis",
            "severity_means": "chemical-tractability tier under VP D7/D8, cross-checked vs clinical DEE/syndrome list; NOT an invented clinical score; individual severity is OWED (D8.5)",
            "declared_before_reading_gamma": True,
        },
        "cohort_n": len(genes),
        "genes": genes,
        "gamma_distribution": {
            "overall": dict(n=len(all_g), gamma_min=min(all_g), gamma_max=max(all_g),
                            gamma_mean=round(sum(all_g) / len(all_g), 6)),
            "by_fault_axis": by_axis,
        },
        "threshold_levers_grounded_in_genes": lever_genes,
        "excluded_severe": EXCLUDED_SEVERE,
        "live_fetch": {s: LIVE_FETCH[s]["src"] for s in LIVE_FETCH},
        "checks": {
            "all_gamma_re_derive_offline_match_cache": all_match,
            "cohort_complete": len(missing) == 0,
            "missing": missing,
            "n_T_axis": by_axis.get("T", {}).get("n", 0),
            "n_O_axis": by_axis.get("O", {}).get("n", 0),
            "n_W_axis": by_axis.get("W", {}).get("n", 0),
        },
        "firewall": "ACQUIRES INPUTS only (gene identity + promoter gamma). No dose, no synthesis, no "
                    "efficacy, no treatment claim. gamma is blind to on/off; a drug cannot change a "
                    "promoter gamma (it is a fixed measured input -- D8.7). efficacy=0; NOT medical advice.",
        "honesty_ledger": {"medium_efficacy_tested": 0, "consciousness_claim": 0,
                           "new_tuned_constants": 0, "no_cure_claimed": 1},
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "metric_locked": "gamma = mean(-NN dG37), SantaLucia 1998",
            "window": WINDOW,
        },
    }
    return out

if __name__ == "__main__":
    if "--fetch" in sys.argv:
        fetch_live()
    res = run()
    payload = json.dumps(_round(res), indent=1, sort_keys=True, ensure_ascii=False)
    open(RESULT, "w", encoding="utf-8").write(payload)
    h = hashlib.sha256(json.dumps(_round(res), sort_keys=True, ensure_ascii=False,
                                  separators=(",", ":")).encode()).hexdigest()
    json.dump({"autism_cohort_moderate_results.json": h}, open(EXPECT, "w"), indent=1)
    c = res["checks"]
    print(f"\nCOHORT n={res['cohort_n']}  T={c['n_T_axis']} O={c['n_O_axis']} W={c['n_W_axis']}  "
          f"gamma in [{res['gamma_distribution']['overall']['gamma_min']}, "
          f"{res['gamma_distribution']['overall']['gamma_max']}]")
    print(f"all gamma re-derive offline == cache: {c['all_gamma_re_derive_offline_match_cache']}  "
          f"complete: {c['cohort_complete']}")
    print(f"levers grounded: {res['threshold_levers_grounded_in_genes']}")
    print(f"result sha256: {h}")
