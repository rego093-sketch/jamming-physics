#!/usr/bin/env python3
"""
verify_boundary.py — the neuro-side lock for the neuro<->mind boundary.

Companion to verify_em_thesis.py. Where that gate pins the *content* boundary
(near-field EM affirmed / far-field carrier retired), this gate pins the
*architectural* boundary between the two separate deliverables:

    neuro = the VERIFIED SUBSTRATE  (this package; independently citable)
    mind  = the FRONTIER MODEL      (its own package; cites neuro one-way)

The full two-sided definition lives in PROJECT_BOUNDARY_neuro_mind.md. This gate
enforces the half of it that is checkable from inside the neuro package alone:

  (1) NO code-level dependency neuro -> mind.
      neuro may carry forward-defer *pointers* in prose ("deferred to Mind",
      href="/mind/"), but no neuro .py may import a mind module. A dependency
      would contaminate neuro's standalone-verifiable, citable status.
  (2) LANE PURITY — the neuro package carries no mind-lane files
      (docs/mind/, manifest/mind*.csv, repro/mind/). One file per track.
  (3) SHARED SSOT present — EM_NEAR_FAR_THESIS.md at the package root
      (the one byte-identical object shared with mind).
  (4) EM LOCK holds — verify_em_thesis.py runs and passes (6/6), tying the
      architectural boundary to the content boundary.
  (5) STANDALONE CONTRACT intact — every neuro verification entrypoint is
      present, so the package re-establishes its full trusted state from this
      one zip with no sibling package required.

No RNG, no tuned constant. Deterministic: 2x run identical.
Kept OUTSIDE run_all.py (like verify_em_thesis.py), so verify_all.py stays 5/5.
Run: `python3 verify_boundary.py`  -> prints PASS/FAIL and exits 0/1.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# mind-lane path fragments that must NOT appear inside the neuro package
MIND_LANE = [
    os.path.join("docs", "mind"),
    os.path.join("repro", "mind"),
    os.path.join("manifest", "mind"),
]
# the standalone verification contract (must all be present)
ENTRYPOINTS = [
    "verify_all.py",
    os.path.join("repro", "neuro", "run_all.py"),
    os.path.join("repro", "neuro", "16-muscle-force-length", "run.py"),
    os.path.join("repro", "neuro", "17-spinal-cord-locomotor-cpg", "run.py"),
    os.path.join("tools", "gate_neuro_16.py"),
    os.path.join("tools", "gate_neuro_17.py"),
]
EM_GATE = os.path.join("repro", "neuro", "09-bounds-open-retired", "verify_em_thesis.py")
SSOT = "EM_NEAR_FAR_THESIS.md"

# an import line whose dotted module path contains "mind" as a component
IMPORT_MIND = re.compile(
    r"^\s*(?:from|import)\s+[\w\.]*\bmind\b[\w\.]*", re.IGNORECASE
)
# allowed forward-defer pointers in prose (reported as INFO, never a failure)
DEFER_POINTER = re.compile(r'href="/mind/"|(?:deferred|carried|defer\w*)\s+to\s+Mind', re.IGNORECASE)

results = []   # (name, ok, detail)
info = []      # informational lines (no pass/fail)


def check(name, ok, detail):
    results.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def walk_files(suffixes=None):
    for dp, dn, fn in os.walk(ROOT):
        if "__pycache__" in dp:
            continue
        for f in fn:
            if suffixes and not f.endswith(suffixes):
                continue
            yield os.path.join(dp, f)


print("=" * 78)
print("NEURO<->MIND BOUNDARY — neuro-side gate")
print("=" * 78)

# ---------------------------------------------------------------------------
# (1) no code-level dependency neuro -> mind
# ---------------------------------------------------------------------------
print("\n(1) DEPENDENCY DIRECTION — neuro must not import mind (one-way cite)")
code_import_hits = []
for path in walk_files((".py",)):
    rel = os.path.relpath(path, ROOT)
    if rel == "verify_boundary.py":   # this file mentions 'mind' in strings/comments
        continue
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, 1):
                if IMPORT_MIND.match(line):
                    code_import_hits.append(f"{rel}:{i}: {line.strip()}")
    except OSError:
        pass
check("no neuro .py imports a mind module",
      len(code_import_hits) == 0,
      "0 code-level mind imports" if not code_import_hits
      else f"FOUND {len(code_import_hits)}: " + " | ".join(code_import_hits))

# informational: forward-defer pointers (the allowed neuro->mind direction)
defer_files = 0
for path in walk_files((".html",)):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            if DEFER_POINTER.search(fh.read()):
                defer_files += 1
    except OSError:
        pass
info.append(f"forward-defer pointers to Mind present in {defer_files} HTML file(s) "
            f"(prose hand-off, ALLOWED — this is the interface, not a dependency)")

# ---------------------------------------------------------------------------
# (2) lane purity — no mind-lane files in the neuro package
# ---------------------------------------------------------------------------
print("\n(2) LANE PURITY — neuro package carries no mind-lane files (one file per track)")
mind_lane_hits = []
for path in walk_files():
    rel = os.path.relpath(path, ROOT)
    for frag in MIND_LANE:
        if rel.startswith(frag) or (os.sep + frag) in (os.sep + rel):
            mind_lane_hits.append(rel)
            break
    # manifest/mind*.csv style
    if re.search(r"manifest[\\/]+mind[\w]*\.csv$", rel):
        mind_lane_hits.append(rel)
mind_lane_hits = sorted(set(mind_lane_hits))
check("no docs/mind, repro/mind, manifest/mind* in this package",
      len(mind_lane_hits) == 0,
      "lane clean" if not mind_lane_hits else f"FOUND: {mind_lane_hits}")

# ---------------------------------------------------------------------------
# (3) shared single-source-of-truth present
# ---------------------------------------------------------------------------
print("\n(3) SHARED SSOT — the one byte-identical object shared with mind")
ssot_path = os.path.join(ROOT, SSOT)
ssot_ok = os.path.isfile(ssot_path)
ssot_sha = ""
if ssot_ok:
    with open(ssot_path, "rb") as fh:
        ssot_sha = hashlib.sha256(fh.read()).hexdigest()
check(f"{SSOT} present at package root",
      ssot_ok,
      f"sha256 {ssot_sha[:16]}… (mirror byte-identical into mind)" if ssot_ok
      else "MISSING")

# ---------------------------------------------------------------------------
# (4) EM lock holds — content boundary still pinned
# ---------------------------------------------------------------------------
print("\n(4) EM LOCK — content boundary pinned (verify_em_thesis.py)")
em_path = os.path.join(ROOT, EM_GATE)
if not os.path.isfile(em_path):
    check("verify_em_thesis.py present + passes", False, f"MISSING {EM_GATE}")
else:
    try:
        proc = subprocess.run([sys.executable, em_path],
                              capture_output=True, text=True, timeout=120)
        em_ok = proc.returncode == 0 and "THESIS LOCK: PASS" in proc.stdout
        last = [l for l in proc.stdout.splitlines() if "PASS" in l or "FAIL" in l]
        detail = "EM thesis 6/6 PASS (both boundaries pinned)" if em_ok \
            else "EM thesis gate did not pass: " + (last[-1] if last else proc.stdout[-120:])
        check("verify_em_thesis.py present + passes", em_ok, detail)
    except subprocess.SubprocessError as e:
        check("verify_em_thesis.py present + passes", False, f"run error: {e}")

# ---------------------------------------------------------------------------
# (5) standalone contract intact
# ---------------------------------------------------------------------------
print("\n(5) STANDALONE CONTRACT — neuro re-verifies from this one zip alone")
missing_ep = [ep for ep in ENTRYPOINTS if not os.path.isfile(os.path.join(ROOT, ep))]
check("all neuro verification entrypoints present",
      len(missing_ep) == 0,
      "verify_all.py + run_all.py + 2 slug run.py + 2 gate_neuro_* all present"
      if not missing_ep else f"MISSING: {missing_ep}")

# ---------------------------------------------------------------------------
# verdict + report
# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
n_pass = sum(1 for _, ok, _ in results if ok)
n_tot = len(results)
verdict = "PASS" if n_pass == n_tot else "FAIL"
print(f"BOUNDARY (neuro side): {verdict}  ({n_pass}/{n_tot})")
for line in info:
    print(f"  [info] {line}")
if verdict == "PASS":
    print("  -> neuro depends on NOTHING in mind (citable, standalone);")
    print("  -> mind cites neuro one-way; the lanes do not cross;")
    print("  -> shared EM thesis present and its lock holds.")
print("-" * 78)

with open(__file__, "rb") as fh:
    gen_sha = hashlib.sha256(fh.read()).hexdigest()
report = {
    "phase": "lock",
    "paper": "neuro",
    "scope": "neuro<->mind architectural boundary (neuro side)",
    "lock": "one-way dependency (mind->neuro only) + lane purity + shared EM-thesis SSOT",
    "canonical": "PROJECT_BOUNDARY_neuro_mind.md",
    "generator": "verify_boundary.py",
    "generator_sha256": gen_sha,
    "deterministic": "no RNG; 2x run identical; every check is a structural/file invariant",
    "checks_total": n_tot,
    "checks_pass": n_pass,
    "verdict": verdict,
    "boundaries_pinned": [
        "no code-level neuro->mind dependency",
        "neuro package lane is mind-free (one file per track)",
        "EM_NEAR_FAR_THESIS.md shared SSOT present",
        "verify_em_thesis.py content-lock holds (6/6)",
        "standalone verification contract intact",
    ],
    "info": info,
    "checks": [{"name": name, "pass": ok, "detail": detail}
               for name, ok, detail in results],
}
report_path = os.path.join(ROOT, "reports", "lock-neuro-boundary.gate.json")
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=2, ensure_ascii=False)
print(f"report: reports/lock-neuro-boundary.gate.json")

sys.exit(0 if verdict == "PASS" else 1)
