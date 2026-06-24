#!/usr/bin/env python3
"""VP-SPEC v1.9 audit — redundant inheritance + term inconsistency (reproducible).

Run any time: python3 tools/audit_terms.py
Reports (A) inheritance redundancy and (B) term/grade/value consistency across all
cards vs the dictionary SSOT. Structural issues are enforced by the gate; the
GRADE conflicts it lists are scientific calls left to the author.
"""
import json, glob, re, html as H
from collections import defaultdict

ROOT = __file__.rsplit("/tools/", 1)[0]
def L(p): return json.load(open(f"{ROOT}/{p}", encoding="utf-8"))

C = L("registry/concepts.json"); MD = L("registry/modules.json")
ent = {e["id"]: e for e in C["entries"]}
mods = {m["id"]: m for m in MD["modules"]}
mod_owner = {i: m["canonical"][0]["href"].strip("/").split("/")[0] for i, m in mods.items()}
decls = {p.split("/")[-2]: json.load(open(p, encoding="utf-8")) for p in glob.glob(f"{ROOT}/docs/*/_decl.json")}
CARD = re.compile(r'<aside class="vp-card"([^>]*)>(.*?)</aside>', re.S)
GR = re.compile(r'\[([FVLOH])\]')

def norm(s):
    s = H.unescape(s); s = re.sub(r'<su[bp]>(.*?)</su[bp]>', r'\1', s)
    return re.sub(r'[\s_*]', '', s).lower()

print("===== A. REDUNDANT / DUPLICATE INHERITANCE =====")
self_inh = [(v, [m for m in d["inherits_modules"] if mod_owner.get(m) == v]) for v, d in decls.items()]
self_inh = [(v, ms) for v, ms in self_inh if ms]
print(f"[A1] owner self-inheritance (originator inherits own module): {len(self_inh)}  -> {self_inh or 'CLEAN'}")
dup = [(v, k) for v, d in decls.items() for k in ("inherits_volumes", "owns_modules", "inherits_modules", "owns_terms", "uses_terms")
       if len(d.get(k, [])) != len(set(d.get(k, [])))]
print(f"[A2] duplicate ids within a list: {dup or 'CLEAN'}")
ovl = [(v, sorted(set(d["owns_terms"]) & set(d["uses_terms"]))) for v, d in decls.items() if set(d["owns_terms"]) & set(d["uses_terms"])]
print(f"[A3] owns ∩ uses overlap: {ovl or 'CLEAN'}")
omv = [(v, sorted(set(d.get("owns_modules", [])) & set(d["inherits_modules"]))) for v, d in decls.items()
       if set(d.get("owns_modules", [])) & set(d["inherits_modules"])]
print(f"[A4] owns_modules ∩ inherits_modules overlap: {omv or 'CLEAN'}")

print("\n===== B. TERM INCONSISTENCY =====")
seen = {}; col = []
for i, e in ent.items():
    for k in [i] + e.get("aka", []):
        if k in seen and seen[k] != i: col.append((k, seen[k], i))
        seen[k] = i
print(f"[B1] aka collisions (one token -> >1 concept): {col or 'CLEAN'}")

PGR = re.compile(r'\[([FVLOH])\]</b>\s*(forced|verified|calibrated|admissible|measured|open)')
byc = defaultdict(lambda: {"grades": set(), "rhs": defaultdict(int)})
for f in glob.glob(f"{ROOT}/docs/**/index.html", recursive=True):
    if "/docs/concepts/" in f: continue                 # dictionary page, not a volume usage
    for a, c in CARD.findall(open(f, encoding="utf-8", errors="ignore").read()):
        dc = re.search(r'data-concept="([^"]+)"', a)
        if not dc: continue
        cid = dc.group(1)
        pg = PGR.search(c)                              # PRIMARY grade only (ignore firewall 2nd bracket)
        if pg: byc[cid]["grades"].add(pg.group(1))
        bv = re.search(r'<b>(.*?)</b>', c)
        if bv:
            v = norm(bv.group(1)); byc[cid]["rhs"][v.split("=", 1)[1] if "=" in v else v] += 1
note = {e["id"]: e.get("grade_note") for e in C["entries"]}

print("\n[B2] method/discipline terms carrying claim grades (category error):")
mh = [(cid, sorted(byc[cid]["grades"])) for cid in byc
      if ent.get(cid, {}).get("grade") in ("discipline", "admissible") and byc[cid]["grades"] and not note.get(cid)]
for cid, gs in mh: print(f"   - {cid}: dict='{ent[cid]['grade']}' but cards grade {gs}")
print("   " + ("(none)" if not mh else f"[{len(mh)} terms]"))

print("\n[B3] same CLAIM concept graded differently across volumes (dict SSOT = one grade):")
cf = [(cid, sorted(byc[cid]["grades"]), ent[cid]["grade"]) for cid in byc
      if ent.get(cid, {}).get("grade") in ("F", "V", "L", "O") and len(byc[cid]["grades"]) > 1]
und = [(cid,gs,cg) for cid,gs,cg in cf if not note.get(cid)]
for cid, gs, cg in cf:
    tag = "  (documented legitimate split — grade_note set)" if note.get(cid) else f"  →  FIX: canonical [{cg}]"
    print(f"   - {cid}: cards {gs}{tag}")
print("   " + (f"{len(und)} undocumented conflict(s) to resolve" if und else "0 undocumented conflicts — CLEAN"))

print("\n[B4] formula RHS differs across cards (notation drift; review):")
nd = [(cid, dict(list(byc[cid]["rhs"].items())[:3])) for cid in sorted(byc) if len(byc[cid]["rhs"]) > 2]
for cid, rs in nd: print(f"   - {cid}: {rs}")
print("   " + ("(none)" if not nd else f"[{len(nd)} terms with >2 RHS variants]"))
