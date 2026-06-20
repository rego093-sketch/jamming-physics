#!/usr/bin/env python3
"""
fix_finals.py  --  VP_SPEC v1.8 final-wording pass (deterministic).

Replaces the *inner text* of the retrieval-surface paragraphs that the
prefix-extraction pass had filled with flattened-equation fragments and
table dumps:

  * <p class="answer"> ...... </p>                 (all 28 pages)
  * <p class="abstract" data-phase2="abstract">..  (the 11 corrupted pages)

Source of truth: tools/cos_finals.json (authored from each chapter's sealed
intro/body; no new claims). Tag attributes are preserved; only inner text is
swapped, so the edit is idempotent. Word counts come from the LaTeX source via
inventory.py, and answers are word-count-excluded by spec, so C1 is untouched.

Usage:
  python3 tools/fix_finals.py            # apply
  python3 tools/fix_finals.py --check    # verify only (no write)
"""
import json, re, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COS  = os.path.join(ROOT, "docs", "cosmology")
DATA = json.load(open(os.path.join(ROOT, "tools", "cos_finals.json"), encoding="utf-8"))

ANS = DATA["answers"]
ABS = DATA["abstracts"]

def wc(s):
    return len([w for w in re.split(r"\s+", re.sub(r"<[^>]+>", " ", s).strip()) if w])

# Match <p class="answer"> ... </p>  (inner text captured, attrs preserved)
RE_ANS = re.compile(r'(<p class="answer">)(.*?)(</p>)', re.S)
# Match <p class="abstract" ... data-phase2="abstract" ...> ... </p>
RE_ABS = re.compile(r'(<p class="abstract"[^>]*data-phase2="abstract"[^>]*>)(.*?)(</p>)', re.S)

def apply_page(slug, html, check):
    notes = []
    if slug in ANS:
        new = ANS[slug]
        def _a(m):
            return m.group(1) + new + m.group(3)
        html2, n = RE_ANS.subn(_a, html, count=1)
        if n == 0:
            notes.append(f"  [WARN] {slug}: no <p class=answer> found")
        else:
            w = wc(new)
            if not (40 <= w <= 60):
                notes.append(f"  [WARN] {slug}: answer {w} words (outside 40-60)")
            html = html2
    if slug in ABS:
        new = ABS[slug]
        def _b(m):
            return m.group(1) + new + m.group(3)
        html2, n = RE_ABS.subn(_b, html, count=1)
        if n == 0:
            notes.append(f"  [WARN] {slug}: no data-phase2 abstract <p> found")
        else:
            html = html2
    return html, notes

def main():
    check = "--check" in sys.argv
    files = sorted(glob.glob(os.path.join(COS, "*", "index.html")))
    na = nb = 0
    allnotes = []
    for f in files:
        slug = os.path.basename(os.path.dirname(f))
        html = open(f, encoding="utf-8").read()
        new, notes = apply_page(slug, html, check)
        allnotes += notes
        if slug in ANS: na += 1
        if slug in ABS: nb += 1
        if not check and new != html:
            open(f, "w", encoding="utf-8").write(new)
    # verify resulting answer word counts in place
    bad = []
    for f in files:
        slug = os.path.basename(os.path.dirname(f))
        html = open(f, encoding="utf-8").read()
        m = RE_ANS.search(html)
        if m:
            w = wc(m.group(2))
            if not (40 <= w <= 60):
                bad.append(f"{slug}({w})")
    print(f"fix_finals: answers targeted={na}/{len(files)}, abstracts cleaned={nb}")
    for n in allnotes:
        print(n)
    if bad:
        print("  [FAIL] answers outside 40-60 after pass: " + ", ".join(bad))
        sys.exit(1)
    print("  all answers in 40-60 word window: OK")

if __name__ == "__main__":
    main()
