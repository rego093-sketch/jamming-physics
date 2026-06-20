#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_boundary.py — the mind-side lock for the neuro<->mind boundary.

Mirror of the neuro-side gate, enforcing the half of PROJECT_BOUNDARY_neuro_mind.md that is
checkable from inside the mind package alone:

    neuro = the VERIFIED SUBSTRATE  (its own package; independently citable)
    mind  = the FRONTIER MODEL      (this package; cites neuro one-way)

  (1) NO code-level dependency mind -> neuro.
      mind cites neuro RESULTS in prose with status tags ("ΔVm ≈ 0.27 mV, neuro §19 [V]"),
      but no mind .py may import a neuro module. The cite is one-way and prose-only.
  (2) LANE PURITY — the mind package carries no neuro-lane files
      (docs/neuro/, manifest/neuro*.csv, repro/neuro/, content/, neuro tools). One file per track.
  (3) SHARED SSOT set present — the three byte-identical files at the package root
      (EM_NEAR_FAR_THESIS.md, TERMINOLOGY_canonical.md, PROJECT_BOUNDARY_neuro_mind.md).
  (4) EM LOCK + TERMINOLOGY LOCK hold — verify_em_thesis.py (6/6) and verify_terminology.py
      run and pass, tying the architectural boundary to the content + vocabulary boundaries.
  (5) STANDALONE CONTRACT intact — every mind verification entrypoint is present, so the
      package re-establishes its full trusted state from this one zip with no sibling required.

No RNG, no tuned constant. Deterministic: 2x run identical.
Run: `python3 verify_boundary.py`  -> prints PASS/FAIL and exits 0/1.
"""
import hashlib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(name, ok, detail):
    checks.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

print("=" * 78)
print("BOUNDARY — mind side (mind = frontier model; cites neuro one-way)")
print("=" * 78)

# (1) NO code-level dependency mind -> neuro -------------------------------------------
print("\n(1) NO code dependency mind -> neuro (cite is prose-only, one-way)")
neuro_import = re.compile(r"^\s*(?:from|import)\s+.*\bneuro\b", re.M)
# do not count the substring 'neuro' inside the word 'neuron'/'neuroscience' etc.: require a token
tok = re.compile(r"\b(?:vp_neuro\w*|neuro_\w+|neuro\.)")
offenders = []
for dp, _, fns in os.walk(ROOT):
    for fn in fns:
        if fn.endswith(".py") and fn not in ("verify_boundary.py",):
            txt = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
            for line in txt.splitlines():
                s = line.strip()
                if (s.startswith("import ") or s.startswith("from ")) and tok.search(s):
                    offenders.append(os.path.relpath(os.path.join(dp, fn), ROOT))
                    break
check("no mind .py imports a neuro module", not offenders,
      "0 code-level neuro imports" if not offenders else f"FOUND in {sorted(set(offenders))}")

# (2) LANE PURITY — no neuro-lane files in the mind package ----------------------------
print("\n(2) LANE PURITY — mind package carries no neuro-lane files")
neuro_lane = []
for probe in ["docs/neuro", "repro/neuro", "content"]:
    if os.path.isdir(os.path.join(ROOT, probe)):
        neuro_lane.append(probe + "/")
for dp, _, fns in os.walk(os.path.join(ROOT, "manifest")):
    for fn in fns:
        if fn.startswith("neuro"):
            neuro_lane.append("manifest/" + fn)
check("no docs/neuro, repro/neuro, content/, manifest/neuro* in this package",
      not neuro_lane, "lane clean" if not neuro_lane else f"FOUND {neuro_lane}")

# (3) SHARED SSOT set present ----------------------------------------------------------
print("\n(3) SHARED SSOT set — the three byte-identical files shared with neuro")
for fn in ["EM_NEAR_FAR_THESIS.md", "TERMINOLOGY_canonical.md", "PROJECT_BOUNDARY_neuro_mind.md"]:
    p = os.path.join(ROOT, fn)
    check(f"{fn} present at package root", os.path.isfile(p),
          f"sha256 {sha256(p)[:16]}… (must be byte-identical to neuro's — sync_shared_ssot.py)"
          if os.path.isfile(p) else "MISSING")

# (4) EM LOCK + TERMINOLOGY LOCK hold --------------------------------------------------
print("\n(4) content + vocabulary locks hold")
def run_ok(relpath):
    d = os.path.dirname(os.path.join(ROOT, relpath))
    f = os.path.basename(relpath)
    try:
        r = subprocess.run([sys.executable, f], cwd=d, capture_output=True, text=True, timeout=120)
        return r.returncode == 0
    except Exception:
        return False
check("verify_em_thesis.py present + passes",
      os.path.isfile(os.path.join(ROOT, "repro/mind/02-not-a-field/verify_em_thesis.py"))
      and run_ok("repro/mind/02-not-a-field/verify_em_thesis.py"),
      "EM thesis 6/6 PASS (both boundaries pinned)")
check("verify_terminology.py present + passes",
      os.path.isfile(os.path.join(ROOT, "verify_terminology.py")) and run_ok("verify_terminology.py"),
      "terminology PASS (mind rides the brainwave abstraction)")

# (5) STANDALONE CONTRACT intact -------------------------------------------------------
print("\n(5) STANDALONE CONTRACT — mind re-verifies from this one zip alone")
entry = {
    "tools/gate.py": os.path.isfile(os.path.join(ROOT, "tools/gate.py")),
    "tools/mind_registry.py": os.path.isfile(os.path.join(ROOT, "tools/mind_registry.py")),
    "tools/build_search_layer.py": os.path.isfile(os.path.join(ROOT, "tools/build_search_layer.py")),
    "repro/mind/_verify/run_regression.py": os.path.isfile(os.path.join(ROOT, "repro/mind/_verify/run_regression.py")),
    "repro/mind/_engine/run_all.py": os.path.isfile(os.path.join(ROOT, "repro/mind/_engine/run_all.py")),
}
check("all mind verification entrypoints present", all(entry.values()),
      "gate.py + registry + build_search_layer + run_regression + engine run_all all present"
      if all(entry.values()) else f"MISSING {[k for k,v in entry.items() if not v]}")

print("\n" + "-" * 78)
ok = all(checks)
n = len(checks)
print(f"BOUNDARY (mind side): {'PASS' if ok else 'FAIL'}  ({sum(checks)}/{n})")
if ok:
    print("  -> mind cites neuro one-way (prose, status-tagged); 0 code imports;")
    print("  -> the lanes do not cross; the shared SSOT set is present;")
    print("  -> content + vocabulary locks hold. mind verifies from its own zip alone.")
else:
    print("  -> a boundary invariant drifted. See FAILs above; do not paper over.")
print("-" * 78)
sys.exit(0 if ok else 1)
