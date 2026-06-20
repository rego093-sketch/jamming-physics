#!/usr/bin/env python3
# VP-SPEC v1.7 — Phase 3 결정론 허브 생성기 (tools/build_hub.py)
# 사용: python3 tools/build_hub.py --paper physics
# _meta.json + templates/hub.html 로 docs/{paper}/index.html 를 결정론 생성한다.
# 추가 허용 항목(목차·횡단 링크·페이지 abstract·메타데이터)만 만든다. 본문·수식·수치 무변경.
import re, json, argparse, html as _html

# 레지스트리(2장) 파생 메타 — 허브 lede/횡단 링크의 출처(LOCK)
REGISTRY = {
    "physics": {
        "repo": "https://github.com/rego093-sketch/jamming-physics",
        "branch_path": "main",
        "headline": "c² = B/ρ ; m_p/m_e = 6π⁵ (−19 ppm)",
        "xlinks": [
            ("c² = B/ρ", "10-implementing-speed-light-clock-free",
             "§10 — Implementing the speed of light (clock-free)"),
            ("m_p/m_e = 6π⁵ (−19 ppm)", "axp-lattice-origin-proton-mass-integral",
             "Appendix P — Lattice origin of the proton mass"),
            ("electron mass (geometric origin)", "axe-geometric-origin-electron-mass-direct",
             "Appendix E — Geometric origin of the electron mass"),
        ],
    },
}

def ws(s): return re.sub(r"\s+", " ", s or "").strip()
def clean(s):  # derive_meta 와 동일: 인라인 math $ 제거(내부 보존)·구두점 앞 공백 정리
    s = ws(s).replace("$", "")
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    return s
def esc(s): return _html.escape(s or "", quote=True)
def aesc(s): return clean(s).replace('"', "'")

def sentences(t):
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+", ws(t)) if p.strip()]

def fit_desc(text):
    ss = sentences(text); d = ""
    for s in ss:
        d = (d + " " + s).strip()
        if len(d) >= 80: break
    if len(d) > 160:
        cut = d[:160]; cut = cut[:cut.rfind(" ")] if " " in cut else cut
        d = cut.strip()
    return d

def paper_abstract(text, n=3):
    ss = sentences(text)[:n]
    a = ws(" ".join(ss))
    if a and a[-1] not in ".!?": a += "."
    return a

def build(paper):
    meta = json.load(open(f"docs/{paper}/_meta.json", encoding="utf-8"))
    reg = REGISTRY[paper]
    tpl = open("templates/hub.html", encoding="utf-8").read()

    short = meta["short"]; title = meta["title"]; doi = meta["doi"]
    src = meta.get("paper_abstract_source", "")
    desc = clean(fit_desc(src)) or f"{short} — {title}."
    abstract = clean(paper_abstract(src))
    repro_root = f'{reg["repo"]}/tree/{reg["branch_path"]}/repro/{paper}/'
    lede = f'Canonical results: {reg["headline"]}.'

    # 목차(TOC): 전 챕터 링크(고아 0) + one_liner + 등급 배지
    GR = {"forced": "g-forced", "hypothesis": "g-hypothesis",
          "verified": "g-verified", "open": "g-open"}
    toc = ["<ol class=\"toc\">"]
    for c in meta["chapters"]:
        href = f'/{paper}/{c["slug"]}/'
        line = f'<li><a href="{href}">{esc(ws(c["title"]))}</a>'
        if c.get("one_liner"):
            line += f' <span class="ol">{esc(ws(c["one_liner"]))}</span>'
        if c.get("grade") and c["grade"] in GR:
            line += f' <span class="grade {GR[c["grade"]]}">{esc(c["grade"])}</span>'
        toc.append(line + "</li>")
    toc.append("</ol>")
    toc_html = "\n".join(toc)

    # 횡단 링크(§10): 대표 결과 → 내부 핵심 챕터(전부 존재 — 404 없음)
    xl = ["<ul class=\"xlinks\">"]
    for label, slug, name in reg["xlinks"]:
        xl.append(f'<li><span class="kf">{esc(label)}</span> → '
                  f'<a href="/{paper}/{slug}/">{esc(name)}</a></li>')
    xl.append("</ul>")
    xlinks_html = "\n".join(xl)

    # 개요(OVERVIEW): 봉인 메타/등급 원장만으로 구성(작문 없음). 장문 마케팅 산문은 저자 슬롯.
    t = meta.get("totals", {})
    from collections import Counter
    gc = Counter(c.get("grade") for c in meta["chapters"] if c.get("grade"))
    GLAB = {"forced": "forced", "verified": "verified",
            "hypothesis": "hypothesis", "open": "open"}
    grade_phrase = ", ".join(f"{gc[g]} {GLAB[g]}" for g in
                             ["forced", "verified", "hypothesis", "open"] if gc.get(g))
    ov = [f'<p class="overview">{len(meta["chapters"])} chapters · '
          f'{t.get("eq","?")} equations · {t.get("tables","?")} tables · '
          f'{t.get("words","?")} source words. Foundation paper of the Jamming '
          f'Physics program; every page carries its own reproducibility strip '
          f'(DOI + repro/ deep link) and, where the source states one, a graded verdict.</p>']
    if grade_phrase:
        ov.append(f'<p class="overview">Claim ledger across graded sections: '
                  f'{grade_phrase} (precedence forced &gt; verified &gt; hypothesis &gt; open).</p>')
    ov.append('<p class="overview"><em>Note:</em> this overview is generated '
              'deterministically from the sealed document and its claim ledger; '
              'no prose is synthesized.</p>')
    overview = "\n".join(ov)

    # JSON-LD: CollectionPage + breadcrumb(Home › short)
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": f"{short} — {title}",
        "url": f"https://jamming-physics.org/{paper}/",
        "isPartOf": {"@type": "WebSite", "name": "Jamming Physics",
                     "url": "https://jamming-physics.org/"},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": "https://jamming-physics.org/"},
            {"@type": "ListItem", "position": 2, "name": short,
             "item": f"https://jamming-physics.org/{paper}/"}]},
        "identifier": f"https://doi.org/{doi}",
    }, ensure_ascii=False)

    out = tpl
    for k, v in {
        "%%SHORT%%": esc(short), "%%TITLE_FULL%%": esc(title),
        "%%DESC%%": aesc(desc), "%%PAPER%%": paper,
        "%%CITATION_TAGS%%": "<!-- citation_tags: Phase 7 -->",
        "%%JSONLD%%": jsonld, "%%DOI%%": esc(doi),
        "%%REPRO_ROOT%%": esc(repro_root),
        "%%DERIVATION_LINE%%": esc(lede), "%%ABSTRACT%%": esc(abstract),
        "%%OVERVIEW%%": overview, "%%TOC%%": toc_html, "%%XLINKS%%": xlinks_html,
    }.items():
        out = out.replace(k, v)

    leftover = re.findall(r"%%[A-Z_]+%%", out)
    if leftover:
        raise SystemExit(f"[build_hub] 미치환 플레이스홀더: {leftover}")

    open(f"docs/{paper}/index.html", "w", encoding="utf-8").write(out)
    # _meta: hub abstract 채움(있던 (Phase 3) 표식 대체)
    meta["abstract"] = abstract
    json.dump(meta, open(f"docs/{paper}/_meta.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"[build_hub] {paper}: hub 생성 — 챕터 {len(meta['chapters'])} 링크 · "
          f"횡단 {len(reg['xlinks'])} · abstract 채움")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True)
    a = ap.parse_args()
    build(a.paper)
