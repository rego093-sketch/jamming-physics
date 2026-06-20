#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_search_layer.py — apply the VP-SPEC v1.8 C4 (Retrieval-Readiness) layer to Felt Cognition.

Deterministic and idempotent. For every chapter it:
  * inserts an answer-first <p class="answer"> right after </h1> (6-R.3),
  * inserts one self-contained <aside class="vp-card"> per cited lock after the claim-strip (6-R.2),
both between HTML-comment markers so a re-run replaces rather than duplicates.

Then it writes the machine-access layer (6-R.5): docs/robots.txt (7 bots), docs/sitemap.xml
(every docs/ index.html), docs/llms.txt (<5KB authoritative summary), docs/llms-full.txt.
sitemap <lastmod> is stamped from the frozen R.RELEASE_DATE SSOT (never the wall clock), so the
docs/ tree is a pure function of source content and re-running on any day is byte-identical.

Run from anywhere: python3 tools/build_search_layer.py
Body text, equations, grades and numbers are untouched; only excluded-from-wordcount blocks
(answer / vp-card asides) and new top-level access files are added.
"""
import os, sys, re, html

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import mind_registry as R

PKG = R.PKG
DOCS = os.path.join(PKG, "docs")
MIND = os.path.join(DOCS, "mind")
SITE = "https://jamming-physics.org"

A_START, A_END = "<!-- vp:answer:start -->", "<!-- vp:answer:end -->"
C_START, C_END = "<!-- vp:cards:start -->", "<!-- vp:cards:end -->"


def _strip_block(text, start, end):
    return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n?", "", text, flags=re.S)


def _answer_html(slug):
    return (f"{A_START}\n<p class=\"answer\">{html.escape(R.ANSWERS[slug])}</p>\n{A_END}")


def _cards_html(slug):
    cards = []
    for lid in R.CITES.get(slug, []):
        lk = R.LOCKS[lid]
        canon = lk["canonical"]
        link = f"/mind/{canon}/"
        label = "this chapter" if canon == slug else f"canonical §{canon.split('-')[0]}"
        cards.append(
            f'<aside class="vp-card" data-locked="{lid}">'
            f'<b>{html.escape(lk["label"])}</b> = {html.escape(lk["value"])} — '
            f'{html.escape(lk["meaning"])} <b>{html.escape(lk["grade"])}</b>. '
            f'<a href="{link}">{label}</a></aside>'
        )
    if not cards:
        return ""
    return C_START + "\n" + "\n".join(cards) + "\n" + C_END


def patch_chapter(slug):
    path = os.path.join(MIND, slug, "index.html")
    text = open(path, encoding="utf-8").read()
    # idempotent: remove any prior injected blocks first
    text = _strip_block(text, A_START, A_END)
    text = _strip_block(text, C_START, C_END)

    # insert answer-first immediately after the (single) </h1>
    if "<h1>" in text and R.ANSWERS.get(slug):
        text = re.sub(r"(</h1>)", r"\1\n" + _answer_html(slug).replace("\\", "\\\\"), text, count=1)

    # insert cards immediately after the claim-strip </aside>
    cards = _cards_html(slug)
    if cards:
        m = re.search(r'<aside class="claim-strip">.*?</aside>', text, flags=re.S)
        if m:
            text = text[:m.end()] + "\n" + cards + text[m.end():]
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return len(R.CITES.get(slug, []))


def write_robots():
    lines = ["# Felt Cognition — AI & search crawlers allowed (VP-SPEC v1.8 / 6-R.5)"]
    for bot in R.BOTS:
        lines += [f"User-agent: {bot}", "Allow: /", ""]
    lines += ["User-agent: *", "Allow: /", "", f"Sitemap: {SITE}/sitemap.xml", ""]
    open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8").write("\n".join(lines))


def _all_index_urls():
    urls = []
    for root, _dirs, files in os.walk(DOCS):
        for f in files:
            if f == "index.html":
                rel = os.path.relpath(os.path.join(root, f), DOCS)
                url = SITE + "/" + os.path.dirname(rel).replace(os.sep, "/")
                if not url.endswith("/"):
                    url += "/"
                if url == SITE + "/./" or url == SITE + "/":
                    url = SITE + "/"
                urls.append(url)
    return sorted(set(urls))


def write_sitemap():
    # Deterministic: <lastmod> is sourced from the frozen R.RELEASE_DATE SSOT, never the wall
    # clock, so re-running on any day produces a byte-identical sitemap (VP-SPEC C1 idempotency).
    lastmod = R.RELEASE_DATE
    items = "".join(
        f"  <url><loc>{html.escape(u)}</loc><lastmod>{lastmod}</lastmod></url>\n"
        for u in _all_index_urls())
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{items}</urlset>\n")
    open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    return len(_all_index_urls())


def write_llms():
    md = []
    md.append("# Felt Cognition")
    md.append("")
    md.append("> A functional model of the stream of thought on the verified neuro chain. A thought is "
              "many parallel ionic eddies igniting in gamma (winner-take-most); the basal-ganglia loop "
              "selects one; a dopamine error shapes which eddies are laid down next; serial selection "
              "bound within a theta frame is the stream. The \"field\" is band-structured phase-coherence "
              "on ionic spikes and synaptic currents (communication-through-coherence), not a physical "
              "field. Whether the embodied real-time loop is experience is held open; no link is causal.")
    md.append("")
    md.append(f"Author: Young Jae Lee (ORCID {R.ORCID}). DOI: {R.DOI}. License: CC BY 4.0.")
    md.append("")
    md.append("## Core (verified)")
    for slug in ["03-organ-emergence", "04-em-brainwave", "05-memory-physics"]:
        md.append(f"- [{slug}]({SITE}/mind/{slug}/): {R.ANSWERS[slug].split('.')[0]}.")
    md.append("")
    md.append("## Model")
    for slug in ["06-parallel-eddies", "07-selection-loop", "08-learned-field",
                 "09-stream-of-thought", "10-felt-loop", "11-hemispheres-and-ai",
                 "13-em-coordination"]:
        md.append(f"- [{slug}]({SITE}/mind/{slug}/): {R.ANSWERS[slug].split('.')[0]}.")
    md.append("")
    md.append("## Sensory & light-binding (verified)")
    md.append(f"- [14-sensory-coupling]({SITE}/mind/14-sensory-coupling/): eight sensory "
              "streams bind to central relays at the measured kappa=0.55; cross-modal binding "
              "rides only the shared field.")
    md.append(f"- [15-light-to-memory]({SITE}/mind/15-light-to-memory/): a brainwave is emerged "
              "light; brainwave+sensory EM rectify (alpha=2/pi) into an info bit that writes a "
              "persisting engram.")
    md.append("")
    md.append("## Scope & open problem")
    for slug in ["01-constitution-scope", "02-not-a-field", "12-open-problem"]:
        md.append(f"- [{slug}]({SITE}/mind/{slug}/): {R.ANSWERS[slug].split('.')[0]}.")
    md.append("")
    md.append("## Discipline")
    md.append("- Physical-mediator rule: every claim names a carrier (ion spikes / synaptic currents "
              "gated by classified low-frequency phase); nothing asserted without being emerged.")
    md.append("- Grades: [F] forced, [V] verified in code, [O] open with a stated obstacle.")
    text = "\n".join(md) + "\n"
    open(os.path.join(DOCS, "llms.txt"), "w", encoding="utf-8").write(text)
    return len(text.encode("utf-8"))


def write_llms_full():
    """Plain-markdown rendering of the canonical chapters (answer + abstract + body text)."""
    out = ["# Felt Cognition — full text (machine-readable, generated from canonical HTML)", ""]
    for slug in R.CHAPTERS:
        path = os.path.join(MIND, slug, "index.html")
        t = open(path, encoding="utf-8").read()
        m = re.search(r"<main>(.*)</main>", t, flags=re.S)
        body = m.group(1) if m else t
        h1 = re.search(r"<h1>(.*?)</h1>", body, flags=re.S)
        out.append(f"## {re.sub(r'<[^>]+>','',h1.group(1)).strip() if h1 else slug}")
        out.append(f"({SITE}/mind/{slug}/)")
        out.append("")
        out.append(R.ANSWERS[slug])
        out.append("")
        # body text minus asides/nav/figures
        b = re.sub(r"<aside.*?</aside>", "", body, flags=re.S)
        b = re.sub(r"<nav.*?</nav>", "", b, flags=re.S)
        b = re.sub(r"<figure.*?</figure>", "", b, flags=re.S)
        b = re.sub(r"<h1>.*?</h1>", "", b, flags=re.S)
        for h2 in re.findall(r"<h2>(.*?)</h2>(.*?)(?=<h2>|$)", b, flags=re.S):
            head = re.sub(r"<[^>]+>", "", h2[0]).strip()
            para = re.sub(r"<[^>]+>", " ", h2[1])
            para = re.sub(r"&[a-zA-Z]+;", " ", para)
            para = re.sub(r"\s+", " ", para).strip()
            if head:
                out.append(f"### {head}")
            if para:
                out.append(para)
            out.append("")
    text = "\n".join(out) + "\n"
    open(os.path.join(DOCS, "llms-full.txt"), "w", encoding="utf-8").write(text)
    return len(text.encode("utf-8"))


def main():
    probs = R.validate()
    if probs:
        print("REGISTRY INVALID:", *probs, sep="\n  "); raise SystemExit(1)
    total_cards = 0
    for slug in R.CHAPTERS:
        total_cards += patch_chapter(slug)
    write_robots()
    n_sitemap = write_sitemap()
    llms_bytes = write_llms()
    full_bytes = write_llms_full()
    print(f"answer-first inserted into {len(R.CHAPTERS)} chapters")
    print(f"vp-cards inserted: {total_cards}")
    print(f"robots.txt: {len(R.BOTS)} bots allowed")
    print(f"sitemap.xml: {n_sitemap} urls")
    print(f"llms.txt: {llms_bytes} bytes ({'<5KB OK' if llms_bytes < 5000 else 'TOO BIG'})")
    print(f"llms-full.txt: {full_bytes} bytes")


if __name__ == "__main__":
    main()
