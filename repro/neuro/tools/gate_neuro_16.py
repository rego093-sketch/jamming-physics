#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_neuro_16.py — VP-SPEC C1/C4 gate for the §16 muscle chapter. It REGENERATES the
reproduction values from the deterministic engine and checks that every number DISPLAYED
in the canonical HTML matches a regenerated value (drift 0), then checks the §6 template
requirements (answer-first, claim-strip with repro+DOI, two JSON-LD, single h1, canonical,
prev nav, vp-card). Writes reports/upgrade-neuro-16.gate.json.
"""
import json, os, re, subprocess, sys, hashlib

def _find_root():
    """Locate the repo root (the dir containing docs/neuro/16-.../index.html), searching
    upward from both this script's dir and the cwd, so the gate runs from tools/ or root."""
    rel = os.path.join("docs", "neuro", "16-muscle-force-length", "index.html")
    cands = []
    for base in (os.path.dirname(os.path.abspath(__file__)), os.getcwd()):
        d = base
        for _ in range(6):
            cands.append(d); d = os.path.dirname(d)
    for d in cands:
        if os.path.exists(os.path.join(d, rel)):
            return d
    return os.path.dirname(os.path.abspath(__file__))

ROOT = _find_root()
HTML = os.path.join(ROOT, "docs", "neuro", "16-muscle-force-length", "index.html")
ENGINE = os.path.join(ROOT, "repro", "neuro", "_engine")
REPORTS = os.path.join(ROOT, "reports")


def regen_values():
    """Run the engine twice (determinism) and return the canonical number set + sha."""
    def run():
        return subprocess.run([sys.executable, "vp_muscle_force_law.py"], cwd=ENGINE,
                              capture_output=True, text=True, timeout=300)
    r1 = run(); gp = os.path.join(ENGINE, "muscle_force_law_results.json")
    h1 = hashlib.sha256(open(gp, "rb").read()).hexdigest()
    res = json.load(open(gp, encoding="utf-8"))
    r2 = run(); h2 = hashlib.sha256(open(gp, "rb").read()).hexdigest()
    determ = (h1 == h2)
    d = res["derived"]; v = res["validation_vs_GHJ1966"]; lock = res["lock"]
    canon = {
        d["zero_long"], d["plateau_bot"], d["plateau_top_lo"], d["plateau_top_hi"], d["steepen"],
        v["zero_long"]["measured"], v["plateau_bot"]["measured"], v["plateau_top"]["measured"],
        v["steepen"]["measured"], res["max_abs_err_um"],
        lock["thick"], lock["thin"], lock["bare_lo"], lock["bare_hi"], lock["z"],
    }
    canon = {round(float(x), 4) for x in canon}
    return canon, determ, h1, res


def main():
    checks = []
    def chk(name, ok): checks.append((name, bool(ok)))

    html = open(HTML, encoding="utf-8").read()
    canon, determ, sha, res = regen_values()
    chk("engine deterministic (2x sha256 identical)", determ)
    chk("engine fidelity_pass (derived vs GHJ within tolerance)", res.get("fidelity_pass"))

    # body text (strip head/scripts) for number extraction; drop boilerplate blocks
    # (footer carries 'CC BY 4.0', claim-strip carries the DOI link) so only body CLAIMS remain
    body = html.split("</head>", 1)[-1]
    body = re.sub(r"<footer>.*?</footer>", " ", body, flags=re.S)
    body = re.sub(r'<aside class="claim-strip">.*?</aside>', " ", body, flags=re.S)
    body_txt = re.sub(r"<[^>]+>", " ", body)

    # the displayed muscle landmark numbers must each be a regenerated value (drift 0)
    # extract decimal numbers that look like micrometre landmarks (one or two decimals, 0<x<5)
    nums = set()
    for m in re.findall(r"\b\d\.\d{1,2}\b", body_txt):
        x = round(float(m), 4)
        if 0.0 < x < 5.0:
            nums.add(x)
    # the canonical landmark/dimension values that MUST appear and match
    must_appear = {3.65, 2.05, 2.2, 2.25, 1.65, 1.67, 0.02, 1.6, 1.0, 0.15, 0.05}
    missing = sorted(x for x in must_appear if x not in nums)
    chk("all canonical landmark/dimension numbers displayed in HTML", not missing)
    # every displayed landmark-range number is a regenerated value (no drift / no stray claim)
    # (restrict to the muscle landmark band to avoid section numbers/years; 0.2 also a dim)
    allowed = canon | {0.2, 1.27}   # 0.2 bare_hi shown as '0.2'; 1.27 is the declared [O] value
    drift = sorted(x for x in nums if x not in allowed)
    chk("no displayed landmark number drifts from regenerated set", not drift)

    # §6 template structure
    chk("single h1", html.count("<h1>") == 1)
    chk("answer-first <p class=\"answer\">", 'class="answer"' in html)
    chk("abstract <p class=\"abstract\">", 'class="abstract"' in html)
    chk("claim-strip present", 'class="claim-strip"' in html)
    chk("claim-strip links reproduction (GitHub repro path)", "/repro/neuro/16-muscle-force-length/" in html)
    chk("claim-strip links DOI snapshot", "doi.org/10.5281/zenodo.17979015" in html)
    chk("two JSON-LD blocks (ScholarlyArticle + BreadcrumbList)",
        html.count("application/ld+json") == 2 and "ScholarlyArticle" in html and "BreadcrumbList" in html)
    chk("canonical link", 'rel="canonical"' in html and "/neuro/16-muscle-force-length/" in html)
    chk("prev nav to §15", 'rel="prev"' in html and "/neuro/15-em-link-full/" in html)
    chk("vp-card aside present", 'class="vp-card"' in html)
    chk("no KaTeX/MathJax span residue", 'class="katex' not in html)
    chk("HTML <= 300KB", len(html.encode()) <= 300_000)

    npass = sum(1 for _, ok in checks if ok)
    verdict = all(ok for _, ok in checks)
    os.makedirs(REPORTS, exist_ok=True)
    report = {
        "phase": "chapter-build", "paper": "neuro", "scope": "§16 muscle-force-length",
        "engine_sha256": sha, "checks_total": len(checks), "checks_pass": npass,
        "verdict": "PASS" if verdict else "FAIL",
        "checks": [{"name": n, "pass": ok} for n, ok in checks],
        "drift": drift, "missing": missing,
    }
    json.dump(report, open(os.path.join(REPORTS, "upgrade-neuro-16.gate.json"), "w"), indent=2)
    for n, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print("=" * 62)
    print(f"GATE: {report['verdict']}  ({npass}/{len(checks)} checks)")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
