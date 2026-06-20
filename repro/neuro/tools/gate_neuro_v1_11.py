#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_neuro_v1_11.py — v1.11 session gate (VP-SPEC v1.8). Verifies the analgesic-inheritance
upgrade end to end:

  [1] analgesic inheritance re-derives the frozen 27-target map on THIS volume's engine, drift 0
  [2] engine identity: this volume's vp_neuro_engine.py is byte-identical to the frozen sibling engine
  [3] neuropathic-pain de-sensitisation: all 3 levers raise the threshold / return the gain to baseline
  [4] DNA-emergence grounding: inherited lineage gamma is bit-for-bit the measured atlas gamma
  [5] the 3 new chapters exist and meet the sec.6 template (answer-first, vp-card, 2x JSON-LD, h1, <300KB)
  [6] hub has zero chapter orphans (all 24 chapters linked)
  [7] C4 retrieval files present (robots 7 bots + sitemap + llms<5KB + site.css)
  [8] _meta.json totals consistent with chapters on disk

Exit 0 + prints "OVERALL: PASS" only if every check passes. Standard library only.
"""
import os, sys, re, json, glob, html as H, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs", "neuro")
REPRO = os.path.join(ROOT, "repro", "neuro")
ROOT_TOOLS = os.path.join(ROOT, "tools")

def _jsonok(s):
    try:
        json.loads(s); return True
    except Exception:
        return False

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# [1]+[2] run the re-derivation and read its summary
def run(mod, script):
    p = subprocess.run([sys.executable, script], cwd=os.path.join(REPRO, mod),
                       capture_output=True, text=True)
    return p.returncode == 0, p.stdout + p.stderr

ok1, out1 = run("21-analgesic-nociceptor-threshold", "rederive_on_neuro_engine.py")
summ = json.load(open(os.path.join(REPRO, "21-analgesic-nociceptor-threshold/expected/rederive_summary.json")))
check("[1] analgesic inheritance re-derives (drift 0)", ok1 and summ["drift"]["drift_zero"],
      f"n_targets={summ['n_targets']} levers={summ['lever_counts']}")
check("[2] engine identity byte-identical", summ["engine_identity"]["ok"],
      "sha256 " + summ["engine_identity"]["this_engine_sha256"][:16] + "…")

# [3] neuropathic-pain de-sensitisation
ok3, out3 = run("22-neuropathic-pain-firing-threshold", "neuropathic_pain_levers.py")
npl = json.load(open(os.path.join(REPRO, "22-neuropathic-pain-firing-threshold/expected/neuropathic_pain_levers.json")))
ds = npl["de_sensitisation"]
check("[3] de-sensitisation: levers raise threshold, gain -> baseline",
      ok3 and ds["all_T_rise_monotone"] and ds["all_gain_fall_monotone"] and ds["full_reversal_returns_to_baseline"],
      f"x{ds['gain_amplification']} sensitised -> baseline {ds['baseline_gain_1_over_2g']}")

# [4] DNA-emergence grounding
ok4, out4 = run("20b-dna-emergence-inheritance", "verify_dna_emergence.py")
dna = json.load(open(os.path.join(REPRO, "20b-dna-emergence-inheritance/expected/dna_emergence.json")))
check("[4] DNA-emergence grounding == measured atlas gamma",
      ok4 and dna["inherited_gamma_is_measured_atlas"], f"{dna['n_lineage_genes']} lineage genes")

# [5] new chapters meet the template
NEW = ["21-analgesic-nociceptor-threshold-map", "22-neuropathic-pain-improvement-levers",
       "23-pain-channelopathy-and-dna-grounding"]
all_ok = True
for slug in NEW:
    p = os.path.join(DOCS, slug, "index.html")
    if not os.path.exists(p):
        all_ok = False; check(f"[5] chapter {slug}", False, "missing"); continue
    h = open(p, encoding="utf-8").read()
    ld = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', h, re.S)
    ld_ok = len(ld) == 2 and all(_jsonok(b) for b in ld)
    c = (h.count('<p class="answer">') == 1 and '<p class="abstract">' in h
         and 'vp-card' in h and h.count('<h1>') == 1 and 'rel="canonical"' in h
         and '<nav class="pn">' in h and len(h) < 300000 and ld_ok)
    all_ok &= c
    check(f"[5] chapter {slug} template", c, f"{len(h)}B, JSON-LD {'ok' if ld_ok else 'BAD'}")

# [6] hub orphans 0
hub = open(os.path.join(DOCS, "index.html"), encoding="utf-8").read()
linked = set(int(x) for x in re.findall(r'/neuro/(\d\d)-', hub))
n_ch = len([d for d in os.listdir(DOCS) if re.match(r'\d\d', d) and os.path.isdir(os.path.join(DOCS, d))])
orphans = sorted(set(range(0, n_ch)) - linked)
check("[6] hub orphans 0", not orphans, f"{len(linked)} chapters linked, missing {orphans or 'none'}")

# [7] C4 retrieval files
docs_root = os.path.join(ROOT, "docs")
robots = open(os.path.join(docs_root, "robots.txt")).read() if os.path.exists(os.path.join(docs_root, "robots.txt")) else ""
bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
robots_ok = all(b in robots for b in bots)
sitemap_ok = os.path.exists(os.path.join(docs_root, "sitemap.xml")) or os.path.exists(os.path.join(DOCS, "sitemap.xml"))
llms_p = os.path.join(docs_root, "llms.txt")
llms_ok = os.path.exists(llms_p) and os.path.getsize(llms_p) < 5120
css_ok = os.path.exists(os.path.join(docs_root, "assets", "css", "site.css"))
check("[7] C4 retrieval files", robots_ok and sitemap_ok and llms_ok and css_ok,
      f"robots={robots_ok} sitemap={sitemap_ok} llms<5KB={llms_ok} css={css_ok}")

# [8] _meta totals consistent
meta = json.load(open(os.path.join(DOCS, "_meta.json")))
disk = sorted(int(d[:2]) for d in os.listdir(DOCS) if re.match(r'\d\d-', d) and os.path.isdir(os.path.join(DOCS, d)))
meta_nos = sorted(c["no"] for c in meta["chapters"])
check("[8] _meta chapters == disk", meta_nos == disk and meta["totals"]["chapters"] == len(disk),
      f"meta {len(meta_nos)} / disk {len(disk)}")

print("=" * 64)
# [9] HTML<->code drift 0 for the new chapters: rebuild them and require byte-identity
before = {s: open(os.path.join(DOCS, s, "index.html"), "rb").read() for s in NEW
          if os.path.exists(os.path.join(DOCS, s, "index.html"))}
rb = subprocess.run([sys.executable, os.path.join(ROOT_TOOLS, "build_neuro_pain_chapters.py")],
                    capture_output=True, text=True)
after = {s: open(os.path.join(DOCS, s, "index.html"), "rb").read() for s in NEW
         if os.path.exists(os.path.join(DOCS, s, "index.html"))}
identical = rb.returncode == 0 and all(before.get(s) == after.get(s) for s in NEW)
check("[9] new chapters HTML<->code drift 0 (rebuild byte-identical)", identical,
      "deterministic builder reproduces committed HTML exactly")

print("=" * 64)
npass = sum(1 for _, ok, _ in results if ok)
allp = npass == len(results)
print(f"OVERALL: {'PASS' if allp else 'FAIL'} ({npass}/{len(results)} checks)")
sys.exit(0 if allp else 1)
