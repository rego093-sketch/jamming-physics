#!/usr/bin/env python3
"""VP-SPEC v1.9 §8 — Shared-Infrastructure Gate (executable enforcement of C5).

Checks one paper's _decl.json against the LOCK registries (concepts.json,
modules.json) and the manifest, and (if the hub HTML is present) the body
notation (inherits-strip + data-concept cards). This is what makes "lossless
incorporation" enforceable rather than aspirational.

Usage:  python3 tools/gate_shared_infra.py <paper_id> [--no-body]
Exit 0 = all required checks PASS; exit 1 = at least one FAIL.
"""
import json, os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECL_FIELDS = ["paper_id", "tier", "inherits_volumes", "inherits_modules",
               "adds", "primitives", "owns_terms", "uses_terms", "grades"]


def load(p):
    return json.load(open(os.path.join(ROOT, p), encoding="utf-8"))


def gate(paper_id, check_body=True):
    results = []  # (level, name, ok, detail)   level: REQ | BODY

    decl_path = f"docs/{paper_id}/_decl.json"
    if not os.path.isfile(os.path.join(ROOT, decl_path)):
        results.append(("REQ", "_decl.json exists", False, decl_path))
        return results
    decl = load(decl_path)
    results.append(("REQ", "_decl.json exists", True, ""))
    results.append(("REQ", "7+ required fields", all(f in decl for f in DECL_FIELDS),
                    [f for f in DECL_FIELDS if f not in decl]))

    concepts = load("registry/concepts.json")
    modules = load("registry/modules.json")
    manifest = load("registry/vp.manifest.json")
    cids = {e["id"] for e in concepts["entries"]}
    cowner = {e["id"]: e["owner"] for e in concepts["entries"]}
    mids = {m["id"] for m in modules["modules"]}
    row = next((v for v in manifest["volumes"] if v["id"] == paper_id), None)

    # registry resolution
    bad_mod = [i for i in decl.get("inherits_modules", []) if i not in mids]
    results.append(("REQ", "inherits_modules resolve in modules.json", not bad_mod, bad_mod))
    bad_own = [i for i in decl.get("owns_terms", []) if i not in cids]
    bad_use = [i for i in decl.get("uses_terms", []) if i not in cids]
    results.append(("REQ", "owns_terms + uses_terms resolve in concepts.json",
                    not bad_own and not bad_use, {"owns": bad_own, "uses": bad_use}))
    # ownership consistency
    wrong_owner = [i for i in decl.get("owns_terms", []) if cowner.get(i) != paper_id]
    results.append(("REQ", "owns_terms owner == paper_id", not wrong_owner, wrong_owner))

    # manifest drift-0
    if row:
        mm = (set(decl.get("inherits_volumes", [])) == set(row.get("inherits", []))
              and set(decl.get("primitives", [])) == set(row.get("primitives", [])))
        g = row.get("grades", {})
        gm = decl.get("grades", {}) == {k: g.get(k, 0) for k in ("forced", "verified", "open", "hypothesis")}
        am = set(decl.get("adds", [])) == set(row.get("adds", []))
        results.append(("REQ", "manifest inherits/primitives match (drift 0)", mm, ""))
        results.append(("REQ", "manifest grades match", gm, {"decl": decl.get("grades"), "manifest": g}))
        results.append(("REQ", "manifest adds match", am,
                        {"decl": decl.get("adds"), "manifest": row.get("adds")}))
    else:
        results.append(("REQ", "volume present in manifest", False, paper_id))

    # body notation (optional — requires the hub + chapter HTML)
    if check_body:
        hub = os.path.join(ROOT, f"docs/{paper_id}/index.html")
        if not os.path.isfile(hub):
            results.append(("BODY", "hub HTML present", False, "skipped — no hub"))
        else:
            import glob
            aka2id = {}
            for e in concepts["entries"]:
                for k in [e["id"]] + e.get("aka", []):
                    aka2id[k] = e["id"]
            html = open(hub, encoding="utf-8", errors="ignore").read()
            # (1) inherits-strip on hub lists exactly inherits_modules, each linking /modules/#id
            strip = re.search(r'class="inherits-strip".*?</aside>', html, re.S)
            if not strip:
                results.append(("BODY", "inherits-strip present", False, "add aside.inherits-strip (6-M.2)"))
            else:
                linked = set(re.findall(r'/modules/#([a-z_]+)', strip.group(0)))
                want = set(decl.get("inherits_modules", [])) | set(decl.get("owns_modules", []))
                results.append(("BODY", "module strip == owns ∪ inherits", linked == want,
                                {"missing": sorted(want - linked), "extra": sorted(linked - want)}))
            # scan ALL chapter pages of the volume for cards + carded concept ids
            vol_html = "".join(open(f, encoding="utf-8", errors="ignore").read()
                               for f in glob.glob(os.path.join(ROOT, f"docs/{paper_id}/**/index.html"), recursive=True))
            cards = re.findall(r'<aside class="vp-card"([^>]*)>(.*?)</aside>', vol_html, re.S)
            # (2) every DICTIONARY-resolving card carries data-concept == canonical(data-locked) + /concepts link
            #     volume-local quantities (data-locked not a dictionary term), untagged, and ="true" are exempt
            bad = []
            for attrs, content in cards:
                dl = re.search(r'data-locked="([^"]+)"', attrs)
                if not dl or dl.group(1) == "true" or dl.group(1) not in aka2id:
                    continue                                  # exempt
                cid = aka2id[dl.group(1)]
                dc = re.search(r'data-concept="([^"]+)"', attrs)
                if not dc or dc.group(1) != cid or f"/concepts/#{cid}" not in content:
                    bad.append(dl.group(1))
            results.append(("BODY", "dictionary cards: data-concept==canonical + /concepts link",
                            not bad, {"n_bad": len(bad), "sample": sorted(set(bad))[:8]}))
            # (3) uses_terms each carded (data-concept) somewhere in the volume body
            body_ids = set(re.findall(r'data-concept="([A-Za-z_0-9]+)"', vol_html))
            uncarded = [t for t in decl.get("uses_terms", []) if t not in body_ids]
            results.append(("BODY", "uses_terms all carded in volume", not uncarded, {"uncarded": uncarded}))

    return results


def main():
    if len(sys.argv) < 2:
        print("usage: gate_shared_infra.py <paper_id> [--no-body]"); sys.exit(2)
    pid = sys.argv[1]
    body = "--no-body" not in sys.argv
    res = gate(pid, body)
    req = [r for r in res if r[0] == "REQ"]
    bod = [r for r in res if r[0] == "BODY"]
    print(f"=== Shared-Infrastructure Gate (VP-SPEC v1.9 §8) — {pid} ===\n")
    print("REQUIRED (declaration / registry / manifest):")
    for _, name, ok, det in req:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"   {det}" if (not ok and det) else ""))
    req_ok = all(ok for _, _, ok, _ in req)
    if bod:
        print("\nBODY NOTATION (v1.9 retrofit checklist):")
        for _, name, ok, det in bod:
            print(f"  {'PASS' if ok else 'TODO'}  {name}" + (f"   {det}" if (not ok and det) else ""))
    print(f"\nREQUIRED tier: {'PASS' if req_ok else 'FAIL'}")
    sys.exit(0 if req_ok else 1)


if __name__ == "__main__":
    main()
