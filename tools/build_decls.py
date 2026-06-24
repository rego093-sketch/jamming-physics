#!/usr/bin/env python3
"""VP-SPEC v1.9 Phase-0 — derive docs/{paper_id}/_decl.json for every volume.

Lossless by construction: the REQUIRED fields are read verbatim from the
manifest row; owns_terms come from concepts.json (owner == paper_id);
uses_terms and inherits_modules are derived by scanning each volume's body
for data-locked cards and resolving them (via the concept aka map) to
canonical concept ids.

inherits_modules rule (auditable, no over-assignment):
  - kernel: always (the bedrock every volume sits on)
  - a generative module M (light_emergence / dna_interpretation / rotor_inflow):
    inherited iff the volume cards any of M's DISTINCTIVE terms (M.bundles minus
    the kernel bundles) — i.e. the volume actually uses that module's machinery.
    dna_interpretation additionally fires on the curated `gamma` primitive (the
    measured-γ threshold), which the carded set is always a subset of.
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    return json.load(open(os.path.join(ROOT, p), encoding="utf-8"))


def main():
    manifest = load("registry/vp.manifest.json")
    concepts = load("registry/concepts.json")
    modules = load("registry/modules.json")

    # aka -> canonical concept id (detect collisions)
    aka2id, collisions = {}, []
    for e in concepts["entries"]:
        for k in [e["id"]] + e.get("aka", []):
            if k in aka2id and aka2id[k] != e["id"]:
                collisions.append((k, aka2id[k], e["id"]))
            aka2id[k] = e["id"]
    if collisions:
        print("WARN aka collisions:", collisions)

    owner = {}
    for e in concepts["entries"]:
        owner.setdefault(e["owner"], set()).add(e["id"])

    mb = {m["id"]: set(m["bundles"]) for m in modules["modules"]}
    # module owner = volume of the FIRST canonical entry (the originator)
    mod_owner = {m["id"]: m["canonical"][0]["href"].strip("/").split("/")[0]
                 for m in modules["modules"]}
    kern = mb["kernel"]
    GEN = ["light_emergence", "dna_interpretation", "rotor_inflow"]
    distinctive = {g: (mb[g] - kern) for g in GEN}

    rows = []
    for vol in manifest["volumes"]:
        pid = vol["id"]
        raw = set()
        for f in glob.glob(os.path.join(ROOT, f"docs/{pid}/**/index.html"), recursive=True):
            raw |= set(re.findall(r'data-locked="([^"]+)"',
                                  open(f, encoding="utf-8", errors="ignore").read()))
        carded = {aka2id[r] for r in raw if r in aka2id}          # canonical concept ids carded
        owns = sorted(owner.get(pid, set()))
        uses = sorted(carded - set(owns))
        inh_mods = ["kernel"]
        for g in GEN:
            trig = bool(carded & distinctive[g])
            # dna_interpretation: also triggered by the curated gamma primitive (measured-γ threshold),
            # since many biology volumes inherit the atlas via γ without carding a γ aside on every page.
            # (light_emergence / rotor_inflow have no dedicated primitive → carded-distinctive signal only.)
            if g == "dna_interpretation" and "gamma" in vol.get("primitives", []):
                trig = True
            if trig:
                inh_mods.append(g)
        # a volume ORIGINATES (owns) the modules whose first-canonical volume is itself;
        # it does not "inherit" them — split them out to remove redundant self-inheritance.
        owns_mods = [m for m in mod_owner if mod_owner[m] == pid]
        inh_mods = [m for m in inh_mods if m not in owns_mods]
        g = vol.get("grades", {})
        decl = {
            "paper_id": pid,
            "tier": vol["tier"],
            "inherits_volumes": vol.get("inherits", []),          # verbatim (lossless vs manifest)
            "owns_modules": owns_mods,                            # modules this volume originates
            "inherits_modules": inh_mods,
            "adds": vol.get("adds", []),
            "primitives": vol.get("primitives", []),
            "owns_terms": owns,
            "uses_terms": uses,
            "grades": {k: g.get(k, 0) for k in ("forced", "verified", "open", "hypothesis")},
        }
        out = os.path.join(ROOT, f"docs/{pid}/_decl.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        json.dump(decl, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        rows.append((pid, inh_mods, len(owns), len(uses)))

    print(f"wrote {len(rows)} _decl.json\n")
    print(f"{'volume':24s} {'inherits_modules':52s} own use")
    for pid, im, no, nu in rows:
        tag = "".join("K" if m == "kernel" else m[0].upper() for m in im)
        names = ", ".join(m.replace("_", " ") for m in im)
        print(f"{pid:24s} {names:52s} {no:3d} {nu:3d}")


if __name__ == "__main__":
    main()
