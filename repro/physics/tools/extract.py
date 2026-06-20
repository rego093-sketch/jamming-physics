#!/usr/bin/env python3
"""Extract readable text from VP physics chapter HTML, preserving structure,
equation LaTeX (from <img alt>), tables, and claim-strip/aside grade tokens."""
import sys, re, os
from bs4 import BeautifulSoup, NavigableString, Tag

def eq_repr(img):
    alt = (img.get('alt') or '').strip()
    src = img.get('src') or ''
    fid = os.path.basename(src).replace('.svg','')
    if alt:
        return f"  [EQ {fid}]: {alt}"
    return f"  [EQ {fid}]"

def walk(node, out, depth=0):
    if isinstance(node, NavigableString):
        t = str(node)
        if t.strip():
            out.append(t.strip())
        return
    if not isinstance(node, Tag):
        return
    name = node.name
    if name in ('script','style','nav','header','footer'):
        return
    cls = node.get('class') or []
    # equation figures
    if name == 'figure' and 'eq' in cls:
        img = node.find('img')
        if img:
            out.append('\n' + eq_repr(img))
        return
    if name == 'img':
        out.append(eq_repr(node))
        return
    if name in ('h1','h2','h3','h4'):
        txt = node.get_text(' ', strip=True)
        prefix = {'h1':'\n##### ','h2':'\n### ','h3':'\n## ','h4':'\n# '}[name]
        out.append(prefix + txt)
        return
    if name == 'aside':
        txt = node.get_text(' ', strip=True)
        if txt:
            out.append(f"\n  [ASIDE/{'/'.join(cls)}]: {txt}")
        return
    if name == 'table':
        out.append('\n[TABLE]')
        for tr in node.find_all('tr'):
            cells = [td.get_text(' ', strip=True) for td in tr.find_all(['td','th'])]
            # also catch eq images inside cells
            row = ' | '.join(c for c in cells)
            out.append('  ' + row)
        out.append('[/TABLE]')
        return
    if name == 'pre':
        out.append('\n[PRE]\n' + node.get_text())
        out.append('[/PRE]')
        return
    if name == 'li':
        # gather inline including eqs
        buf = []
        for ch in node.children:
            walk(ch, buf, depth+1)
        out.append('  - ' + ' '.join(b for b in buf if b.strip()).strip())
        return
    if name == 'p':
        buf = []
        for ch in node.children:
            walk(ch, buf, depth+1)
        joined = ' '.join(b for b in buf).strip()
        if joined:
            out.append('\n' + joined)
        return
    # default: recurse
    for ch in node.children:
        walk(ch, out, depth+1)

def extract(path):
    with open(path, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    main = soup.find('main') or soup.body or soup
    # title/meta
    head = soup.find('head')
    title = soup.find('title')
    desc = soup.find('meta', attrs={'name':'description'})
    out = []
    if title: out.append(f"[TITLE] {title.get_text(strip=True)}")
    if desc: out.append(f"[DESC] {desc.get('content','')}")
    out.append('='*70)
    body_out = []
    walk(main, body_out)
    out.extend(body_out)
    text = '\n'.join(out)
    # collapse excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

if __name__ == '__main__':
    print(extract(sys.argv[1]))
