#!/usr/bin/env python3
"""tools/check_integrity.py — recurrence guards for the corpus (run by tools/gate.py, or alone).

Checks
  L  links      every href/src in docs/ resolves: site-relative (/x/), absolute
                (https://jamming-physics.org/x/), relative (x/), and GitHub repro links
                (https://github.com/rego093-sketch/jamming-physics/{tree,blob}/main/<path>).
  S  scripts    every *.py a volume's pages cite exists somewhere under repro/<volume>/.
                Known gaps are listed in registry/missing_scripts_baseline.json; the check
                fails only on a NEW missing script (a regression), and reports the baseline.
  A  aggregates the generated files match a fresh regeneration: docs/index.html
                (tools/build_index.py) and docs/concepts/index.html (tools/build_concepts.py).
                A difference means an aggregate was hand-edited (AGENTS.md §9 rule 4).

Usage: python3 tools/check_integrity.py [--update-baseline]
Exit code 0 = all pass, 1 = failure.
"""
import glob, json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
BASELINE = os.path.join(ROOT, 'registry', 'missing_scripts_baseline.json')
GH = re.compile(r'https://github\.com/rego093-sketch/jamming-physics/(?:tree|blob)/main/([^"\'<>\s#?)]*)')
SITE = re.compile(r'https://jamming-physics\.org(/[^"\'<>\s#?)]*)')


def _exists_site(path):
    t = os.path.join(DOCS, path.lstrip('/'))
    return path in ('', '/') or os.path.isfile(t) or os.path.isfile(os.path.join(t, 'index.html'))


def check_links():
    bad = []
    for dp, _, fs in os.walk(DOCS):
        for f in fs:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            s = open(p, encoding='utf-8', errors='ignore').read()
            for h in re.findall(r'(?:href|src)="([^"#?]+)"', s):
                if h.startswith(('http:', 'https:', 'mailto:', 'data:', 'javascript:')):
                    continue
                ok = _exists_site(h) if h.startswith('/') else (
                    os.path.isfile(os.path.normpath(os.path.join(dp, h))) or
                    os.path.isfile(os.path.join(os.path.normpath(os.path.join(dp, h)), 'index.html')))
                if not ok:
                    bad.append((os.path.relpath(p, ROOT), h))
            for m in SITE.finditer(s):
                if not _exists_site(m.group(1)):
                    bad.append((os.path.relpath(p, ROOT), m.group(0)))
            for m in GH.finditer(s):
                if not os.path.exists(os.path.join(ROOT, m.group(1).rstrip('/'))):
                    bad.append((os.path.relpath(p, ROOT), m.group(0)))
    return bad


def cited_missing():
    miss = {}
    for vdir in sorted(glob.glob(os.path.join(DOCS, '*', ''))):
        vid = os.path.basename(os.path.dirname(vdir))
        pages = glob.glob(os.path.join(vdir, '**', 'index.html'), recursive=True)
        if not pages or not os.path.isdir(os.path.join(ROOT, 'repro', vid)):
            continue
        txt = ' '.join(re.sub(r'<aside class="lt-note".*?</aside>', '', open(p, encoding='utf-8', errors='ignore').read(), flags=re.S)
                       for p in pages)
        cited = set(re.findall(r'\b([A-Za-z][A-Za-z0-9_]*\.py)\b', txt))
        have = {os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'repro', vid, '**', '*.py'), recursive=True)}
        m = sorted(cited - have)
        if m:
            miss[vid] = m
    return miss


def check_aggregates():
    drift = []
    with tempfile.TemporaryDirectory() as tmp:
        for rel in ('docs/index.html', 'docs/concepts/index.html'):
            shutil.copy(os.path.join(ROOT, rel), os.path.join(tmp, rel.replace('/', '__')))
        try:
            for tool in ('tools/build_index.py', 'tools/build_concepts.py'):
                subprocess.run([sys.executable, os.path.join(ROOT, tool)], cwd=ROOT, check=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for rel in ('docs/index.html', 'docs/concepts/index.html'):
                a = open(os.path.join(tmp, rel.replace('/', '__')), encoding='utf-8').read()
                b = open(os.path.join(ROOT, rel), encoding='utf-8').read()
                if a != b:
                    drift.append(rel)
        finally:  # never leave the working tree changed by the check itself
            for rel in ('docs/index.html', 'docs/concepts/index.html'):
                shutil.copy(os.path.join(tmp, rel.replace('/', '__')), os.path.join(ROOT, rel))
    return drift


def main():
    update = '--update-baseline' in sys.argv
    fail = False
    bad = check_links()
    print(f"[L] links: {'PASS' if not bad else 'FAIL'} ({len(bad)} broken)")
    for b in bad[:10]:
        print('     ', b)
    fail |= bool(bad)

    miss = cited_missing()
    if update or not os.path.exists(BASELINE):
        json.dump(miss, open(BASELINE, 'w'), indent=1, sort_keys=True)
        print(f"[S] scripts: baseline written ({sum(map(len, miss.values()))} known gaps)")
    base = json.load(open(BASELINE))
    new = {v: sorted(set(m) - set(base.get(v, []))) for v, m in miss.items()}
    new = {v: m for v, m in new.items() if m}
    print(f"[S] scripts: {'PASS' if not new else 'FAIL'} (known gaps {sum(map(len, base.values()))}; new {sum(map(len, new.values()))})")
    for v, m in new.items():
        print('      NEW missing in', v, m[:8])
    fail |= bool(new)

    drift = check_aggregates()
    print(f"[A] aggregates: {'PASS' if not drift else 'FAIL'} {drift if drift else '(regeneration identical)'}")
    fail |= bool(drift)
    sys.exit(1 if fail else 0)


if __name__ == '__main__':
    main()
