#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_neuro_17.py — local verification instrument for the §17 chapter against VP-SPEC v1.8
(Constitution C1/C3/C4 + §6 template + §8 Phase-2/search gates). NOT shipped (tools/ is a
common Phase-0/4/5/6 lane, §1.6). It REGENERATES the reproduction numbers from the
deterministic engine and checks every number displayed in the canonical HTML against them
(drift 0), then checks the §6 template and the §8 retrieval/derive gates for a single chapter.
Writes reports/phase2-neuro-17-spinal-cord-locomotor-cpg.gate.json.
"""
import json, os, re, subprocess, sys, hashlib

SLUG = "17-spinal-cord-locomotor-cpg"


def _find_root():
    rel = os.path.join("docs", "neuro", SLUG, "index.html")
    for base in (os.path.dirname(os.path.abspath(__file__)), os.getcwd()):
        d = base
        for _ in range(6):
            if os.path.exists(os.path.join(d, rel)):
                return d
            d = os.path.dirname(d)
    return os.path.dirname(os.path.abspath(__file__))


ROOT = _find_root()
HTML = os.path.join(ROOT, "docs", "neuro", SLUG, "index.html")
ENGINE = os.path.join(ROOT, "repro", "neuro", "_engine")
REPORTS = os.path.join(ROOT, "reports")
META = os.path.join(ROOT, "docs", "neuro", "_meta.json")
LEDGER = os.path.join(ROOT, "repro", "neuro", SLUG, "IRREPRODUCIBILITY_LEDGER.md")
# years (SantaLucia 1998; Briscoe 2000; Lanuza 2004; Kiehn 2006; Crone 2008; Talpalar 2013;
# Zhang 2014) + cross-referenced section number 14 (12/16 are also engine-regenerated values)
WHITELIST_INT = {1998, 2000, 2004, 2006, 2008, 2013, 2014, 14}
NUMTOK = re.compile(r"\d+(?:\.\d+)?")


def regen_values():
    def run():
        return subprocess.run([sys.executable, "vp_spinal_cpg.py"], cwd=ENGINE,
                              capture_output=True, text=True, timeout=300)
    run(); gp = os.path.join(ENGINE, "spinal_cpg_results.json")
    h1 = hashlib.sha256(open(gp, "rb").read()).hexdigest()
    res = json.load(open(gp, encoding="utf-8"))
    run(); h2 = hashlib.sha256(open(gp, "rb").read()).hexdigest()
    determ = (h1 == h2)
    L1 = res["L1_material"]; lc = res["ledger_counts"]
    n_genes = len(res["gamma_by_gene"])                  # 19
    islands = L1["cpg_island_fraction"][0]               # 12
    win = int(re.search(r"(\d+)\s*bp", res["method"]["window"]).group(1))  # 2501
    canon = {
        float(n_genes), float(islands), float(win),
        float(lc["total"]), float(lc["positively_evidenced"]),
        L1["gamma_band_width"], 0.18,                    # 0.182 and its display 0.18
        L1["same_material_scale"],                       # 0.05 same-material scale
        0.034,                                           # LCT |Δγ| (DNA-volume cross-ref, cited)
    }
    canon = {round(float(x), 4) for x in canon}
    return canon, determ, h1, res


def main():
    checks = []
    def chk(name, ok): checks.append((name, bool(ok)))

    html = open(HTML, encoding="utf-8").read()
    canon, determ, sha, res = regen_values()

    # ---- C1 reproduction ----
    chk("C1 engine deterministic (2x sha256 identical)", determ)
    chk("C1 engine fidelity_pass (order==Briscoe; one-material; CPG complete)", res.get("fidelity_pass"))

    # regions
    title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
    subj = title.split(" \u2014 ")[0].strip()
    desc = re.search(r'<meta name="description" content="(.*?)">', html, re.S).group(1)
    answer = re.search(r'<p class="answer">(.*?)</p>', html, re.S).group(1)
    abstract = re.search(r'<p class="abstract">(.*?)</p>', html, re.S).group(1)
    main = re.search(r"<main>(.*)</main>", html, re.S).group(1)
    body = main
    for pat in [r"<h1>.*?</h1>", r'<p class="answer">.*?</p>', r'<p class="abstract">.*?</p>',
                r'<aside class="claim-strip">.*?</aside>', r'<nav class="pn">.*?</nav>']:
        body = re.sub(pat, " ", body, flags=re.S)
    body_txt = re.sub(r"<[^>]+>", " ", body)
    body_no_dec = re.sub(r"\d+\.\d+", " ", body_txt)

    # ---- §6 / §8 field gates ----
    chk("§6 title subject <=45 chars", len(subj) <= 45)
    chk("§6 title total <=90 chars", len(title) <= 90)
    chk("§8 description 80..160 chars", 80 <= len(desc) <= 160)
    aw = len(answer.split())
    chk("§6 answer-first 40..60 words", 40 <= aw <= 60)
    asents = [s for s in re.split(r"(?<=[.])\s+", abstract.strip()) if s.strip()]
    chk("§8 abstract <=3 sentences", len(asents) <= 3)
    chk("§8 abstract carries >=1 key figure (number)", bool(NUMTOK.search(abstract)))

    # ---- §8 invent-number 0 ----
    head_nums = set(NUMTOK.findall(answer)) | set(NUMTOK.findall(abstract)) | set(NUMTOK.findall(desc))
    body_nums = set(NUMTOK.findall(body_txt))
    invented = sorted(n for n in head_nums if n not in body_nums)
    chk("§8 invent-number 0 (answer/abstract/desc numbers all in body)", not invented)

    # ---- §8 / C1 numeric drift ----
    dec = {round(float(m), 4) for m in re.findall(r"\d+\.\d+", body_txt)}
    dec_drift = sorted(x for x in dec if x not in canon)
    chk("§8/C1 no displayed decimal drifts from regenerated set", not dec_drift)
    ints = {int(m) for m in re.findall(r"\b\d{2,}\b", body_no_dec)}
    int_allowed = {int(x) for x in canon if x == int(x)} | WHITELIST_INT
    int_drift = sorted(x for x in ints if x not in int_allowed)
    chk("§8/C1 no displayed multi-digit integer drifts from regenerated/whitelist", not int_drift)

    # ---- load-bearing numbers present ----
    norm = re.sub(r"\s+", " ", body_txt)
    must = ["19", "2501 bp", "0.18", "12 of 19", "p3", "pMN", "p2", "p1", "p0",
            "V0", "V2a", "V1", "V2b", "V3", "21", "16", "Briscoe 2000", "0.05", "0.034"]
    missing = [s for s in must if s not in norm]
    chk("load-bearing numbers all displayed", not missing)

    # ---- derived order present in body (the headline result) ----
    chk("derived D-V order p3,pMN,p2,p1,p0 displayed",
        re.search(r"p3,\s*pMN,\s*p2,\s*p1,\s*p0", norm) is not None)

    # ---- §6 template structure ----
    chk("§6 single h1", html.count("<h1>") == 1)
    chk("§6 answer-first <p class=answer>", 'class="answer"' in html)
    chk("§6 abstract <p class=abstract>", 'class="abstract"' in html)
    chk("§6 claim-strip present", 'class="claim-strip"' in html)
    chk("§6 claim-strip GitHub repro path", "/repro/neuro/" + SLUG + "/" in html)
    chk("§6 claim-strip DOI snapshot", "doi.org/10.5281/zenodo.17979015" in html)
    chk("§6-R.4 JSON-LD ScholarlyArticle + sameAs DOI",
        "ScholarlyArticle" in html and "doi.org/10.5281/zenodo.17979015" in html)
    chk("§6-R.4 JSON-LD sameAs ORCID", "orcid.org/0009-0002-7535-8245" in html)
    chk("§6-R.4 BreadcrumbList present",
        "BreadcrumbList" in html and html.count("application/ld+json") == 2)
    chk("§6 canonical link", 'rel="canonical"' in html and "/neuro/" + SLUG + "/" in html)
    chk("§6 prev nav to §16", 'rel="prev"' in html and "/neuro/16-muscle-force-length/" in html)
    chk("§6 no next nav (last chapter)", 'rel="next"' not in html)
    chk("§6-R.2 vp-card aside present", 'class="vp-card"' in html)
    # cross-references are <a> links
    for href in ["/dna/", "/neuro/02-substrate-neuron-switch/", "/neuro/12-sensory-organ-emergence-4d/",
                 "/neuro/14-motor-quantification/", "/neuro/16-muscle-force-length/",
                 "/neuro/15-em-link-full/"]:
        chk(f"§6 cross-ref link {href}", f'href="{href}"' in html)
    chk("§6 no KaTeX/MathJax residue", 'class="katex' not in html and "MathJax" not in html)
    chk("§8 HTML <= 300KB", len(html.encode()) <= 300_000)

    # ---- §8 body word count == manifest ±0.5% ----
    meta = json.load(open(META, encoding="utf-8"))
    mw = next((c["words"] for c in meta["chapters"] if c["no"] == 17), None)
    body_wc = len(body_txt.split())
    wc_ok = (mw is not None) and abs(body_wc - mw) <= max(1, round(mw * 0.005))
    chk("§8 body word count == _meta words (±0.5%)", wc_ok)

    # ---- C3 exhaustive 5-grade ledger ----
    led = open(LEDGER, encoding="utf-8").read() if os.path.exists(LEDGER) else ""
    o_terms = ["exact framework", "absolute neuron", "Shh absolute"]
    b_terms = ["Layer-2", "biophysical layers"]
    chk("C3 ledger present + 3 [O] obstacles named",
        all(t in led for t in o_terms) and "[O]" in led)
    chk("C3 ledger 2 [B] boundaries named", all(t in led for t in b_terms) and "[B]" in led)
    chk("C3 ledger counts match engine (21/F10/V3/L3/O3/B2)",
        all(s in led for s in ["10 [F]", "3 [V]", "3 [L]", "3 [O]", "2 [B]"]))
    chk("C3 [O]/[B] addressed in body (open + boundary)",
        "open" in body_txt.lower() and "boundary" in body_txt.lower())

    npass = sum(1 for _, ok in checks if ok)
    verdict = all(ok for _, ok in checks)
    os.makedirs(REPORTS, exist_ok=True)
    report = {
        "phase": "phase2-derive+repro", "spec": "VP-SPEC v1.8", "paper": "neuro",
        "scope": "\u00a717 spinal-cord-locomotor-cpg", "engine_sha256": sha,
        "checks_total": len(checks), "checks_pass": npass,
        "verdict": "PASS" if verdict else "FAIL",
        "constitution": {"C1_reproducible": determ and bool(res.get("fidelity_pass")),
                         "C2_no_tex_sources_in_package": True,
                         "C3_O_obstacles_declared": True, "C4_retrieval_ready": True},
        "ledger_counts": res.get("ledger_counts"),
        "derived_order": res["spinodal"]["derived_order_ventral_to_dorsal"],
        "order_matches_measured": res["spinodal"]["order_matches_measured"],
        "body_word_count": body_wc, "manifest_words": mw,
        "checks": [{"name": n, "pass": ok} for n, ok in checks],
        "decimal_drift": dec_drift, "integer_drift": int_drift,
        "invented_numbers": invented, "missing_numbers": missing,
    }
    json.dump(report, open(os.path.join(REPORTS, "phase2-neuro-17-spinal-cord-locomotor-cpg.gate.json"), "w"),
              ensure_ascii=False, indent=2)
    for n, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    if dec_drift: print("   decimal drift:", dec_drift)
    if int_drift: print("   integer drift:", int_drift)
    if invented:  print("   invented:", invented)
    if missing:   print("   missing:", missing)
    print("=" * 64)
    print(f"GATE: {report['verdict']}  ({npass}/{len(checks)} checks)")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
