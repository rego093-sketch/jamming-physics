#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_thermo_panel.py  --  build / extend the cross-species furnace-torpor promoter panel.

This is the EXACT pipeline that produced the vendored panel (validated v0.4.0:
re-running it reproduces all pre-existing cache entries byte-identical AND coord-identical).
It is vendored here so the cross-species reads are reproducible from symbols+assemblies, not
just from a frozen cache. NCBI is contacted only for cells NOT already in the cache (idempotent);
a cached cell is never re-fetched and never mutated, so the panel stays byte-stable.

CONVENTION (reverse-engineered from the vendored cache, then re-validated end-to-end):
  - coords: NCBI Gene esummary genomicinfo chrstart/chrstop are 0-based; gene_start = min,
    gene_end = max, strand = '+' if chrstart<=chrstop else '-'. Stored RAW (no +1).
  - promoter window (genome-forward, TSS-2000..+500 transcript-oriented, stored un-flipped):
        plus  : seq_start = gene_start - 1999, seq_stop = gene_start + 501
        minus : seq_start = gene_end   - 499 , seq_stop = gene_end   + 2001
    efetch nuccore strand=1 (plus); store the 2501-nt genome-forward string as-is.
  - gamma = -mean(SantaLucia-1998 NN dG37) over the window, round 4. The NN parameters are
    reverse-complement symmetric, so gamma is strand-invariant: storing genome-forward is exact.
  - gc = (G+C)/len, round 4.

FIREWALL (binding): gamma reads promoter switch-threshold STRUCTURE only. The hibernation_capacity
  label on each species is CITED biology declared BEFORE any fetch; gamma is BLIND to it. The whole
  point of the panel is to TEST whether any promoter read tracks that label (pre-registered NULL).

NO TUNING: every gamma is a measured fetch; nothing is chosen to hit a target.
"""
import os, sys, json, time, hashlib, urllib.request, urllib.parse

_HERE  = os.path.dirname(os.path.abspath(__file__))
_PANEL = os.path.join(_HERE, "..", "inherited", "crossspecies_thermo_panel.json")

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL   = "vp_thermo_panel"
EMAIL  = "vptheory@jamming-physics.org"   # NCBI etiquette (identifies the polite client)

# SantaLucia 1998 unified NN dG37 -- the SAME READ-ONLY table as the DNA / energy atlas.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,"GT":-1.44,"AC":-1.44,
      "CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,"CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

def gamma_of(seq):
    v = [-NN[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN]
    return round(sum(v)/len(v), 4) if v else None

def gc_of(seq):
    return round((seq.count("G")+seq.count("C"))/len(seq), 4) if seq else None

# ---------------------------------------------------------------------------
#  ROSTERS  (existing 7 species x 3 genes preserved; the rest are the v0.4.0 expansion)
#  hibernation_capacity is CITED biology, declared here BEFORE any fetch (the firewall label).
# ---------------------------------------------------------------------------
SPECIES = [
    # name                          thermo_class  hibernation_capacity   torpor_note
    ("Homo sapiens",                "endotherm",  "non_hibernator",      "non-hibernator"),
    ("Mus musculus",                "endotherm",  "daily_heterotherm",   "daily-torpor-capable"),
    ("Rattus norvegicus",           "endotherm",  "non_hibernator",      "non-hibernator"),
    ("Sus scrofa",                  "endotherm",  "non_hibernator",      "UCP1 pseudogene (no functional UCP1 furnace; cited)"),
    ("Ictidomys tridecemlineatus",  "endotherm",  "deep_hibernator",     "deep hibernator (13-lined ground squirrel)"),
    ("Danio rerio",                 "ectotherm",  "ectotherm",           "ambient-tracking (teleost)"),
    ("Xenopus tropicalis",          "ectotherm",  "ectotherm",           "ambient-tracking (amphibian)"),
    # ---- v0.4.0 hibernation-bridge expansion ----
    ("Urocitellus parryii",         "endotherm",  "deep_hibernator",     "extreme deep hibernator, Tb to ~-2.9C (Arctic ground squirrel) [cited: Barnes 1989]"),
    ("Marmota marmota",             "endotherm",  "deep_hibernator",     "deep multiday hibernator (Alpine marmot)"),
    ("Mesocricetus auratus",        "endotherm",  "deep_hibernator",     "facultative deep hibernator (Syrian hamster)"),
    ("Microcebus murinus",          "endotherm",  "daily_heterotherm",   "PRIMATE heterotherm: daily + seasonal torpor (gray mouse lemur) [cited: Schmid 2000]"),
    ("Ursus americanus",            "endotherm",  "deep_hibernator",     "denning hibernator; mild-Tb multiday torpor (American black bear) [cited: Toien 2011]"),
    ("Cavia porcellus",             "endotherm",  "non_hibernator",      "non-hibernating rodent (guinea pig) -- GC-matched rodent control"),
    ("Oryctolagus cuniculus",       "endotherm",  "non_hibernator",      "non-hibernating lagomorph (rabbit)"),
]

GENES = [
    # symbol      axis            role
    ("UCP1",      "furnace",      "brown-fat proton-leak furnace (non-shivering thermogenesis)"),
    ("ADRB3",     "command",      "beta-3 adrenergic sympathetic command that recruits the furnace"),
    ("PDK4",      "fuel_switch",  "pyruvate dehydrogenase kinase 4: fuel-switch to lipid + glucose sparing"),
    # ---- v0.4.0 fuel-switch / BAT panel expansion ----
    ("PPARGC1A",  "coactivator",  "PGC-1alpha: master coactivator of mitochondrial biogenesis + adaptive thermogenesis"),
    ("DIO2",      "thyroid",      "type-2 deiodinase: local T4->T3 activation required for BAT adaptive thermogenesis"),
    ("CIDEA",     "bat_identity", "brown/beige adipocyte lipid-droplet protein (BAT identity marker)"),
    ("FGF21",     "endocrine",    "fasting/torpor endocrine signal driving browning + fuel switching"),
    ("SLC2A4",    "glucose",      "GLUT4 insulin-responsive glucose transporter (torpor glucose-sparing <-> insulin-resistance node)"),
]

# ---------------------------------------------------------------------------
#  NCBI access (polite, retried)
# ---------------------------------------------------------------------------
def _get(path, params, tries=4, pause=0.34):
    params = dict(params); params.update(tool=TOOL, email=EMAIL)
    url = EUTILS + path + "?" + urllib.parse.urlencode(params)
    last = None
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e; time.sleep(pause*(2**k) + 0.2)
    raise last

def resolve_gene(symbol, organism):
    """esearch exact-symbol within organism -> esummary -> genomic coords (RefSeq NC_ preferred)."""
    term = f'{symbol}[sym] AND "{organism}"[orgn]'
    es = json.loads(_get("esearch.fcgi", dict(db="gene", term=term, retmode="json", retmax="10")))
    ids = es.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return None
    time.sleep(0.34)
    su = json.loads(_get("esummary.fcgi", dict(db="gene", id=",".join(ids), retmode="json")))
    res = su.get("result", {})
    # prefer: exact name match + NC_ chromosome accession + has genomicinfo
    def score(gid):
        rec = res.get(gid, {})
        gi = (rec.get("genomicinfo") or [{}])[0]
        acc = gi.get("chraccver", "") or ""
        nm  = (rec.get("name", "") or "").upper()
        return (1 if nm == symbol.upper() else 0, 1 if acc.startswith("NC_") else 0, 1 if gi else 0)
    cand = sorted([g for g in ids if g in res], key=score, reverse=True)
    for gid in cand:
        rec = res[gid]; gi = (rec.get("genomicinfo") or [{}])[0]
        acc = gi.get("chraccver"); cs = gi.get("chrstart"); ce = gi.get("chrstop")
        if acc and cs is not None and ce is not None:
            cs, ce = int(cs), int(ce)
            if cs <= ce: gs, gend, strand = cs, ce, "+"
            else:        gs, gend, strand = ce, cs, "-"
            return dict(geneid=gid, name=rec.get("name"), acc=acc,
                        gene_start=gs, gene_end=gend, strand=strand)
    return None

def window(gene_start, gene_end, strand):
    if strand == "+": return gene_start - 1999, gene_start + 501
    else:             return gene_end   - 499 , gene_end   + 2001

def efetch_promoter(acc, a, b):
    txt = _get("efetch.fcgi", dict(db="nuccore", id=acc, rettype="fasta", retmode="text",
                                   seq_start=str(a), seq_stop=str(b), strand="1"))
    seq = "".join(l.strip() for l in txt.splitlines() if l and not l.startswith(">")).upper()
    return seq

# ---------------------------------------------------------------------------
#  Build / extend
# ---------------------------------------------------------------------------
def load_panel():
    return json.load(open(_PANEL, encoding="utf-8"))

def build(write=True, verbose=True):
    p = load_panel()
    cache = p.setdefault("cache", {})
    reads = p.setdefault("reads", {})
    spec  = p.setdefault("species", {})

    # refresh species block (labels are declared biology; preserves existing, adds new)
    for name, klass, hib, note in SPECIES:
        spec[name] = {"thermo_class": klass, "hibernation_capacity": hib, "torpor_note": note}

    n_new = n_cached = n_absent = 0
    for sym, axis, role in GENES:
        for name, klass, hib, note in SPECIES:
            key = f"{sym}|{name}"
            reads.setdefault(name, {})
            if key in cache:                       # idempotent: keep byte-identical, recompute read fields
                seq = cache[key]["seq"]
                reads[name][sym] = {"gamma": gamma_of(seq), "gc": gc_of(seq),
                                    "ncbi_acc": cache[key]["coords"]["acc"], "status": "measured"}
                n_cached += 1
                continue
            # not cached -> resolve + fetch
            try:
                r = resolve_gene(sym, name); time.sleep(0.34)
            except Exception as e:
                r = None
                if verbose: print(f"  [resolve-err] {key}: {e}")
            if not r:
                reads[name][sym] = {"gamma": None, "gc": None, "ncbi_acc": None,
                                    "status": "ABSENT/unresolved"}
                n_absent += 1
                if verbose: print(f"  ABSENT     {key}")
                continue
            try:
                a, b = window(r["gene_start"], r["gene_end"], r["strand"])
                seq = efetch_promoter(r["acc"], a, b); time.sleep(0.34)
            except Exception as e:
                seq = ""
                if verbose: print(f"  [fetch-err]  {key}: {e}")
            if len(seq) != 2501 or set(seq) - set("ACGTN"):
                reads[name][sym] = {"gamma": None, "gc": None, "ncbi_acc": None,
                                    "status": "ABSENT/unresolved"}
                n_absent += 1
                if verbose: print(f"  ABSENT*    {key} (len={len(seq)})")
                continue
            cache[key] = {"seq": seq, "coords": {"acc": r["acc"], "gene_start": r["gene_start"],
                                                 "gene_end": r["gene_end"], "strand": r["strand"]}}
            reads[name][sym] = {"gamma": gamma_of(seq), "gc": gc_of(seq),
                                "ncbi_acc": r["acc"], "status": "measured"}
            n_new += 1
            if verbose: print(f"  fetched    {key}  gamma={gamma_of(seq)} gc={gc_of(seq)} ({r['acc']} {r['strand']})")

    p["_what"] = ("Cross-species furnace/torpor promoter panel (UCP1 furnace, ADRB3 sympathetic command, "
                  "PDK4 + PPARGC1A/DIO2/CIDEA/FGF21/SLC2A4 fuel-switch / BAT program), across deep "
                  "hibernators, daily heterotherms, non-hibernators and ectotherms.")
    p["_gene_axes"] = {sym: {"axis": axis, "role": role} for sym, axis, role in GENES}
    if write:
        with open(_PANEL, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, sort_keys=True, indent=1)
    if verbose:
        print(f"\n  new fetched: {n_new} | kept cached: {n_cached} | absent/unresolved: {n_absent}")
        print(f"  species: {len(spec)} | genes: {len(GENES)} | cache cells: {len(cache)}")
    return p

if __name__ == "__main__":
    build(write=True, verbose=True)
