#!/usr/bin/env python3
"""
build_site_infra.py — VP_SPEC v1.8 section 6-R.5 (retrieval access layer)

Emits, deterministically from docs/cosmology/_meta.json and the upgraded
chapter pages:

  docs/robots.txt       allow the 7 named retrieval bots + sitemap pointer
  docs/sitemap.xml      hub + every chapter URL, lastmod = DATE_MOD
  docs/llms.txt         < 5 KB authority summary (core/research/concepts/policies)
  docs/llms-full.txt    full-volume markdown digest (answer-first + abstract/ch)

The answer-first paragraph used in llms-full.txt is the canonical self-contained
answer injected by upgrade_v1_8.py, so the digest never diverges from the pages.
"""
import json, re, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
META = json.load(open(DOCS / "cosmology" / "_meta.json", encoding="utf-8"))

SITE = "https://jamming-physics.org"
HUB = f"{SITE}/cosmology/"
DOI_URL = f"https://doi.org/{META['doi']}"
DATE_MOD = "2026-06-15"
AUTHOR = "Young Jae Lee"
ORCID = "https://orcid.org/0009-0002-7535-8245"
REPRO = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/cosmology"

BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot",
        "PerplexityBot", "ClaudeBot", "Google-Extended"]


def chap_url(slug):
    return f"{HUB}{slug}/"


def clean_title(t):
    t = t.replace("``", "\u201c").replace("''", "\u201d")
    t = t.replace("$", "")
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def strip_tags(s):
    s = re.sub(r"(?is)<sup>(.*?)</sup>", r"^\1", s)
    s = re.sub(r"(?is)<sub>(.*?)</sub>", r"_\1", s)
    s = re.sub(r"(?s)<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_block(slug, cls):
    p = DOCS / "cosmology" / slug / "index.html"
    if not p.exists():
        return ""
    t = p.read_text(encoding="utf-8")
    m = re.search(r'<p class="' + cls + r'"[^>]*>(.*?)</p>', t, re.S)
    return strip_tags(m.group(1)) if m else ""


# ---------------------------------------------------------------- robots.txt
def build_robots():
    lines = ["# VP_SPEC v1.8 6-R.5 — retrieval access policy",
             "# Canonical volume: Vacuum-Inflow Cosmology", ""]
    for b in BOTS:
        lines += [f"User-agent: {b}", "Allow: /", ""]
    lines += ["User-agent: *", "Allow: /", "",
              f"Sitemap: {SITE}/sitemap.xml", ""]
    (DOCS / "robots.txt").write_text("\n".join(lines), encoding="utf-8")
    return "docs/robots.txt"


# --------------------------------------------------------------- sitemap.xml
def build_sitemap():
    urls = [HUB] + [chap_url(c["slug"]) for c in META["chapters"]]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for i, u in enumerate(urls):
        pr = "1.0" if i == 0 else "0.8"
        out += ["  <url>", f"    <loc>{u}</loc>",
                f"    <lastmod>{DATE_MOD}</lastmod>",
                f"    <priority>{pr}</priority>", "  </url>"]
    out += ["</urlset>", ""]
    (DOCS / "sitemap.xml").write_text("\n".join(out), encoding="utf-8")
    return "docs/sitemap.xml"


# ------------------------------------------------------------------ llms.txt
def build_llms():
    title = META["title"]
    short = META["short"]
    L = []
    L.append(f"# {short} — {title}")
    L.append("")
    L.append(f"> Single-author research volume by {AUTHOR} ({ORCID}). "
             f"One physical input — the vacuum inflow rate — is locked, every "
             f"observable is *derived* from it by deterministic code, and each "
             f"claim is graded degenerate / distinguishing / conflicting against "
             f"standard cosmology. No parameter is tuned to fit data. "
             f"Canonical form is this HTML; DOI {META['doi']}.")
    L.append("")
    L.append("## Core")
    L.append(f"- [Volume hub]({HUB}): index, grading, and reading order.")
    for code in ("00", "axf", "16", "axg"):
        c = next((x for x in META["chapters"] if x["code"] == code), None)
        if c:
            L.append(f"- [{clean_title(c['title'])}]({chap_url(c['slug'])})")
    L.append("")
    L.append("## Research")
    for code in ("01", "03", "06", "07", "08", "12", "13", "14", "15"):
        c = next((x for x in META["chapters"] if x["code"] == code), None)
        if c:
            g = c.get("grade") or "—"
            L.append(f"- [{clean_title(c['title'])}]({chap_url(c['slug'])}) — grade: {g}")
    L.append("")
    L.append("## Concepts")
    L.append("- **Inflow rate**: the single locked input; sets the surface "
             "gravity scale per body.")
    L.append("- **a₀ = cH₀/2π ≈ 1.08×10⁻¹⁰ m s⁻²**: galactic acceleration "
             "scale, derived not fitted (distinguishing).")
    L.append("- **Lattice optics**: redshift as elastic-wave propagation in a "
             "non-expanding vacuum lattice.")
    L.append("- **Vacuum deficit**: the inflow account of dark-matter "
             "phenomenology.")
    L.append("")
    L.append("## Policies")
    L.append("- No-tuning lock→derive→gate governance; reclassification log is "
             "public.")
    L.append(f"- Reproducibility tree: {REPRO}/")
    L.append("- License: CC BY 4.0.")
    L.append("")
    txt = "\n".join(L)
    (DOCS / "llms.txt").write_text(txt, encoding="utf-8")
    return "docs/llms.txt", len(txt.encode("utf-8"))


# ------------------------------------------------------------- llms-full.txt
def build_llms_full():
    title = META["title"]
    short = META["short"]
    L = []
    L.append(f"# {short} — {title}")
    L.append("")
    L.append(f"Author: {AUTHOR} ({ORCID}) · DOI: {META['doi']} · "
             f"Canonical: {HUB} · Updated: {DATE_MOD}")
    L.append("")
    L.append("Full-volume digest. For each chapter: the self-contained "
             "answer-first paragraph and its abstract, grounded verbatim in the "
             "canonical HTML pages.")
    L.append("")
    for c in META["chapters"]:
        L.append(f"## {clean_title(c['title'])}")
        meta_bits = [f"URL: {chap_url(c['slug'])}"]
        if c.get("grade"):
            meta_bits.append(f"grade: {c['grade']}")
        L.append(" · ".join(meta_bits))
        L.append("")
        ans = extract_block(c["slug"], "answer")
        if ans:
            L.append(f"**Answer.** {ans}")
            L.append("")
        ab = extract_block(c["slug"], "abstract")
        if ab:
            L.append(ab)
            L.append("")
    txt = "\n".join(L)
    (DOCS / "llms-full.txt").write_text(txt, encoding="utf-8")
    return "docs/llms-full.txt", len(txt.encode("utf-8"))


if __name__ == "__main__":
    print(build_robots())
    print(build_sitemap())
    r, n = build_llms()
    print(f"{r}  ({n} bytes; limit 5120)")
    assert n < 5120, "llms.txt exceeds 5KB"
    r, n = build_llms_full()
    print(f"{r}  ({n} bytes)")
