#!/usr/bin/env python3
"""reconcile_manifest_to_html.py — VP-SPEC v1.7 헌법 C1/C2 검수 도구 (1회 실행, 결정론).

정본은 docs/ HTML 하나다(헌법 C2). manifest/{paper}.csv 는 그 HTML 의 파생 인덱스이므로
게이트가 검사하는 카운트(words, eq_display, figures, tables)를 정본 HTML 에서 재산출해 일치시킨다.
gate.py 와 '동일한' 계수 함수를 사용하므로 phase1/phase2 단어수·식수 검사는 by construction 통과한다.

부수 작업:
  - 고아 수식 SVG 삭제: 정본 HTML 어디에서도 참조되지 않는 docs/eq/{paper}/*.svg
    (예: §17.4 → §18 승격 후 잔존한 phy-17-085/086/087)
  - §18 행 CSV malformation(따옴표 없는 제목 쉼표) 교정 — csv.writer 가 자동 인용.
본문(<main> 내 물리 서술·수식·수치)은 일절 건드리지 않는다. manifest(파생 인덱스)와 고아 SVG 만 정리한다.
"""
import re, csv, os, sys, glob, hashlib

PAPER = "physics"

# --- gate.py 와 동일한 본문 단어수 계산 (words_of) ---
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inventory as inv

def main_block(html):
    m = re.search(r"<main>(.*)</main>", html, re.S)
    return m.group(1) if m else html

def words_of(html):
    t = main_block(html)
    t = re.sub(r"<aside.*?</aside>", "", t, flags=re.S)
    t = re.sub(r'<p class="abstract".*?</p>', "", t, flags=re.S)
    t = re.sub(r"<h1>.*?</h1>", "", t, flags=re.S)
    t = re.sub(r'<nav class="pn">.*?</nav>', "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return inv.word_count(t)

def html_counts(h):
    return dict(words=words_of(h),
                eq_display=h.count("data-eq="),
                figures=h.count('<figure class="fig"'),
                tables=h.count("<table"))

def read_raw_manifest(path):
    """csv.reader 로 파싱(정상 인용 제목은 그대로 처리). 단, 따옴표 없는 제목 쉼표로
    필드가 초과된 행(예: §18)은 title 의 초과분을 흡수해 10필드로 복원한다."""
    rows_raw = list(csv.reader(open(path, encoding="utf-8")))
    header = rows_raw[0]
    n = len(header)  # 10
    rows = []
    for parts in rows_raw[1:]:
        if not parts:
            continue
        if len(parts) == n:
            rows.append(dict(zip(header, parts)))
        elif len(parts) > n:
            extra = len(parts) - n
            # title(인덱스 3)에 흡수: 앞 3필드 고정, 뒤 6필드 고정, 가운데(=title)에 쉼표 병합
            title = ",".join(parts[3:4 + extra])
            vals = parts[:3] + [title] + parts[4 + extra:]
            rows.append(dict(zip(header, vals)))
            print(f"  [CSV 교정] {parts[1]} 행: 따옴표 없는 제목 쉼표 흡수 → title='{title}'")
        else:
            print(f"  [경고] 필드 부족 행 무시: {parts}")
    return header, rows

def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root (build/vp)
    mpath = f"manifest/{PAPER}.csv"
    header, rows = read_raw_manifest(mpath)

    # 1) 고아 SVG 탐지·삭제
    all_html = "".join(open(f, encoding="utf-8").read()
                       for f in glob.glob(f"docs/{PAPER}/*/index.html"))
    referenced = set(re.findall(rf"{ '|'.join([]) or 'phy' }-\d+-\d+", all_html))  # phy-XX-NNN
    referenced = set(re.findall(r"[a-z]{2,3}-[0-9a-z]+-\d+", all_html))
    orphans = []
    for svg in sorted(glob.glob(f"docs/eq/{PAPER}/*.svg")):
        eid = os.path.basename(svg)[:-4]
        if eid not in all_html:
            orphans.append(svg)
    for o in orphans:
        os.remove(o)
        print(f"  [고아 SVG 삭제] {o}")
    if not orphans:
        print("  [고아 SVG] 없음")

    # 2) 각 행 카운트를 정본 HTML 에서 재산출
    changed = []
    for r in rows:
        f = f"docs/{PAPER}/{r['slug']}/index.html"
        if not os.path.exists(f):
            print(f"  [경고] HTML 없음: {f}"); continue
        h = open(f, encoding="utf-8").read()
        c = html_counts(h)
        for k in ("words", "eq_display", "figures", "tables"):
            old = r.get(k, "")
            if str(old) != str(c[k]):
                changed.append((r["slug"], k, old, c[k]))
            r[k] = str(c[k])
        # §18: 15개 식이 manifest 에서 inline 으로 오분류돼 있었음(원본 eq_inline=15,eq_display=0).
        # 정본 HTML 은 15개 모두 display(figure.eq, data-eq=15)이므로 eq_inline 중복 제거.
        if r["slug"] == "18-time-and-gravity":
            r["eq_inline"] = "0"
        # eq_inline 은 게이트 비검사 항목 — 음수/모순만 방지
        try:
            int(r.get("eq_inline", "0"))
        except ValueError:
            r["eq_inline"] = "0"

    # 3) 재작성 (csv.writer 가 쉼표 포함 제목을 자동 인용)
    with open(mpath, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in header})

    print(f"\n  변경된 카운트 {len(changed)}건:")
    for slug, k, old, new in changed:
        print(f"    {slug}: {k} {old} → {new}")

    # 4) _meta.json(파생 카드)도 정본 HTML 에 맞춤 — 머지 Phase 5 입력 정확성
    reconcile_meta(header_rows=rows)

    print(f"\n  manifest sha256: {hashlib.sha256(open(mpath,'rb').read()).hexdigest()[:16]}")
    print(f"  남은 SVG: {len(glob.glob(f'docs/eq/{PAPER}/*.svg'))}  | HTML data-eq 합: "
          f"{sum(open(f,encoding='utf-8').read().count('data-eq=') for f in glob.glob(f'docs/{PAPER}/*/index.html'))}")


def reconcile_meta(header_rows=None):
    """docs/{paper}/_meta.json 의 챕터 카운트(words·eq_display·figures·tables)와 totals 를
    정본 HTML 에서 재산출한다. 편집 필드(one_liner·grade·abstract·headline_results·branch·title)는 보존.
    totals.eq = Σ(eq_inline)+Σ(eq_display), totals.words = Σ(words) 로 자기일관화."""
    import json
    mp = f"docs/{PAPER}/_meta.json"
    if not os.path.exists(mp):
        print("  [_meta.json] 없음 — 생략"); return
    m = json.load(open(mp, encoding="utf-8"))
    meta_changed = []
    for c in m.get("chapters", []):
        slug = c.get("slug", "")
        f = f"docs/{PAPER}/{slug}/index.html"
        if not os.path.exists(f):
            continue
        h = open(f, encoding="utf-8").read()
        cc = html_counts(h)
        for k in ("words", "eq_display", "figures", "tables"):
            if str(c.get(k)) != str(cc[k]):
                meta_changed.append((slug, k, c.get(k), cc[k]))
            c[k] = cc[k]
        # §18: no='VH' 오기(=버전이력 코드 복사 오류) 및 inline 오분류 정정
        if slug == "18-time-and-gravity":
            if str(c.get("no")) != "18":
                meta_changed.append((slug, "no", c.get("no"), 18)); c["no"] = 18
            if int(c.get("eq_inline", 0)) != 0:
                meta_changed.append((slug, "eq_inline", c.get("eq_inline"), 0)); c["eq_inline"] = 0
    # totals 자기일관화
    ch = m.get("chapters", [])
    tw = sum(int(c.get("words", 0)) for c in ch)
    te = sum(int(c.get("eq_inline", 0)) for c in ch) + sum(int(c.get("eq_display", 0)) for c in ch)
    tf = sum(int(c.get("figures", 0)) for c in ch)
    tt = sum(int(c.get("tables", 0)) for c in ch)
    old_tot = dict(m.get("totals", {}))
    m["totals"] = {"words": tw, "eq": te, "figures": tf, "tables": tt}
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n  [_meta.json] 카운트 정정 {len(meta_changed)}건; totals {old_tot} → {m['totals']}")
    for slug, k, old, new in meta_changed[:12]:
        print(f"    {slug}: {k} {old} → {new}")

if __name__ == "__main__":
    main()
