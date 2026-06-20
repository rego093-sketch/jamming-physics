#!/usr/bin/env python3
# tools/derive_meta.py — VP-SPEC v1.7 Phase 2 tool (5/5). 결정론 파생: Phase-1 골격의
#   data-phase2 후크(abstract·grade) + 제목/description/JSON-LD 를 **봉인 본문에서만** 채운다.
# 사용: python3 tools/derive_meta.py --paper physics
# 원칙(SPEC 1장 준수): 본문 의미·수식·수치 무변경. 채우는 값은 전부 본문 내 큐레이트 클레임
#   (<q class="one">)·본문 산문·레지스트리 핵심 수치에서만 파생(임의 작문·임의 요약 금지).
#   편집 대상은 <head> + .abstract <p> + 페이지 .claim-strip 의 grade span 뿐 → 모두
#   gate.words_of 의 제외영역이므로 단어수(±0.5%) 불변(구성상 보장).
import re, os, sys, csv, json, argparse, glob, hashlib
from collections import Counter

# 2장 레지스트리 핵심 수치(텍스트 수식) — abstract 키피겨 화이트리스트 보강용(논리 출처)
REGISTRY = {
  "physics": {"short": "VP Theory",
              "keyfigs": ["c² = B/ρ", "m_p/m_e = 6π⁵"]},
  "cosmology": {"short": "Vacuum-Inflow Cosmology",
              "keyfigs": ["a₀ = cH₀/2π", "a₀ ≈ 1.08×10⁻¹⁰", "δ = 1.751″"]},
}

# --- v1.7 일반화(승인세션): paper별 등급 어휘 site_seed/grade_vocab_{paper}.csv 연동 ---
# 하드코딩 [FHVO] 외 어휘(degenerate/distinguishing/conflicting 등)를 본문에서 인식.
VOCAB = None          # main()에서 채움: {token_lower: (site_class, priority_idx)}
VOCAB_RX = None       # 토큰 정규식
def load_grade_vocab(paper):
    global VOCAB, VOCAB_RX
    p = f"site_seed/grade_vocab_{paper}.csv"
    if not os.path.exists(p): return
    vmap, order = {}, []
    for r in csv.DictReader(open(p, encoding="utf-8")):
        sc = (r.get("site_class_proposal") or "").strip()
        tok = (r.get("token") or "").strip()
        if sc.startswith("g-") and tok:
            vmap[tok.lower()] = (sc, len(order)); order.append(tok)
    if order:
        VOCAB = vmap
        VOCAB_RX = re.compile(r"\b(" + "|".join(re.escape(o) for o in order) + r")\b", re.I)
GRADE = {"F": ("g-forced", "forced"), "H": ("g-hypothesis", "hypothesis"),
         "V": ("g-verified", "verified"), "O": ("g-open", "open")}
GRADE_PRIORITY = "FVHO"  # 동률 시 우선순위(load-bearing 우선)

# gate.py phase2 의 abstract 키피겨 정규식과 동일 클래스(=×·π/^²³⁴⁵) — by construction 정합
GATEFIG = re.compile(r"[0-9].*[=×·π/^²³⁴⁵]|[=×·π].*[0-9]")   # gate.py 와 동일(라인 단위, re.S 미적용)
NUM = re.compile(r"\d+(?:\.\d+)?")

def strip_tags(s): return re.sub(r"<[^>]+>", " ", s)
def ws(s): return re.sub(r"\s+", " ", s).strip()

def clean(s):
    # 결정론 정규화(내용 무변경): 인라인 math 구분자 $ 제거(내부 보존), 구두점 앞 공백 정리
    s = strip_tags(s)
    s = s.replace("$", "")
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    return ws(s)

def sentences(text):
    text = ws(text)
    parts = re.split(r"(?<=[.!?—])\s+", text)
    return [p.strip() for p in parts if p.strip()]

def subj45(h1):
    s = ws(h1)
    if len(s) <= 45: return s
    s2 = re.sub(r"\s*\([^()]*\)\s*$", "", s).strip()       # 후미 괄호 제거
    if 0 < len(s2) <= 45: return s2
    s = s2 or s
    for sep in [":", " --- ", " — ", "—", ";", ",", " from "]:  # 후미 부제 제거
        if sep in s:
            head = s.split(sep)[0].strip()
            if 0 < len(head) <= 45: return head
            if 0 < len(head) < len(s): s = head
    if len(s) <= 45: return s
    out = ""                                                  # 단어경계 절단(중간 절단 금지)
    for w in s.split():
        if len((out + " " + w).strip()) > 45: break
        out = (out + " " + w).strip()
    return out or s[:45].strip()

def fit_desc(parts):
    d = ws(parts[0]) if parts else ""
    i = 1
    while len(d) < 80 and i < len(parts):
        d = ws(d + " " + parts[i]); i += 1
    if len(d) < 80:
        d = ws(d + " — VP Theory, Jamming Physics.")
    if len(d) > 160:
        cut = d[:160]
        cut = cut[:cut.rfind(" ")] if " " in cut else cut    # 마지막 공백까지(>80 유지)
        d = cut.strip()
    return d

def jesc(s): return s.replace("\\", "\\\\").replace('"', '\\"')
def aesc(s): return s.replace('"', "'")   # HTML 속성용

def figure_snippet(noaside_html):
    # gate 와 동일 기반: no-aside 본문에서 태그만 제거(개행 보존), 첫 키피겨 주변 절을 발췌
    gate_text = re.sub(r"<[^>]+>", " ", noaside_html)
    m = GATEFIG.search(gate_text)
    if not m: return ""
    i, j = m.start(), m.end()
    lo = gate_text.rfind(" ", max(0, i - 90), i); lo = lo + 1 if lo != -1 else max(0, i - 90)
    hi = gate_text.find(" ", j, j + 90);          hi = hi if hi != -1 else min(len(gate_text), j + 90)
    return clean(gate_text[lo:hi]).lstrip(")]}>,;:–— ")

def build_abstract(claims, lead_sents, noaside_html):
    base = claims[:2] if claims else lead_sents[:2]
    abs_txt = ws(" ".join(base))
    ss = sentences(abs_txt)
    if len(ss) > 2: abs_txt = ws(" ".join(ss[:2]))           # 리드 2문장으로 우선 제한(키피겨 자리 확보)
    if not GATEFIG.search(abs_txt):                          # 키피겨는 gate 와 동일 기반에서 3번째 문장으로 확보
        snip = figure_snippet(noaside_html)
        if snip:
            if abs_txt and abs_txt[-1] not in ".!?—": abs_txt += "."
            abs_txt = ws((abs_txt + " " + snip).strip())
    if abs_txt and abs_txt[-1] not in ".!?—": abs_txt += "."
    return abs_txt

def page_grade(body):
    # (A) paper vocab 있으면 본문 텍스트에서 어휘 토큰 집계(우선순위=vocab 순서)
    if VOCAB and VOCAB_RX:
        txt = re.sub(r"<[^>]+>", " ", body)
        found = [m.group(1).lower() for m in VOCAB_RX.finditer(txt)]
        if found:
            cnt = Counter(found)
            best = sorted(cnt, key=lambda t: (-cnt[t], VOCAB[t][1]))[0]
            cls = VOCAB[best][0]
            label = f"{cls.replace('g-','').capitalize()}"  # 예: g-distinguishing → Distinguishing
            return cls, label, best
        return None
    # (B) 폴백: 물리식 [FHVO] vps aside
    toks = re.findall(r'<aside class="claim-strip vps"[^>]*>.*?</aside>', body, re.S)
    grades = []
    for a in toks:
        grades += re.findall(r"\[([FHVO])\]", a)
    if not grades: return None
    cnt = Counter(grades)
    best = sorted(cnt, key=lambda g: (-cnt[g], GRADE_PRIORITY.index(g)))[0]
    cls, name = GRADE[best]
    return cls, f"[{best}] {name}", name

def derive_section(html, prow, reg):
    body_m = re.search(r"<main>(.*)</main>", html, re.S)
    body = body_m.group(1) if body_m else html
    body_noaside = re.sub(r"<aside.*?</aside>", "", body, flags=re.S)
    body_noaside = re.sub(r'<p class="abstract".*?</p>', "", body_noaside, flags=re.S)

    h1 = prow.get("h1") or (re.search(r"<h1>(.*?)</h1>", html, re.S) or [None, ""])[1]
    subj = subj45(clean(h1))
    # 인용부호 누수 정리(``...'' → 제거), 양끝 따옴표/백틱/엔티티 제거
    subj = re.sub(r"`+", "", subj)
    subj = re.sub(r"(&#x27;|&#39;|&quot;|[\"'“”‘’])+", "", subj)
    subj = ws(subj)
    # 전체 제목 ≤90자 예산: 약칭이 길면(예: Vacuum-Inflow Cosmology) 주제부를 더 줄인다
    _suf = re.search(r"<title>.*?—\s*(" + re.escape(reg["short"]) + r"\s*§[^<|]*\|\s*Jamming Physics)</title>", html, re.S)
    if _suf:
        budget = 90 - len(" — ") - len(_suf.group(1).strip())
        if len(subj) > budget:
            words = subj.split()
            while words and len(" ".join(words)) > budget:
                words.pop()
            subj = " ".join(words) or subj[:max(budget, 1)]
    _STOPEND = {"the","a","an","of","and","as","its","for","to","in","on","with","from","by"}
    _w = subj.split()
    while _w and _w[-1].lower() in _STOPEND and not re.fullmatch(r"[A-Z]", _w[-1]): _w.pop()
    subj = " ".join(_w) or subj

    claims = [clean(x) for x in re.findall(r'<q class="one">(.*?)</q>', body, re.S)]
    if not claims:                                            # 폴백 1: prefill 큐레이트 one-liner 풀
        claims = [clean(x) for x in (prow.get("one_liner_pool", "").split("|")) if clean(x)]

    lead_sents = []
    for p in re.findall(r"<p>(.*?)</p>", body_noaside, re.S):  # 서사 문단 우선
        lead_sents += sentences(clean(p))
        if len(lead_sents) >= 3: break
    if not lead_sents:                                        # 폴백 2: 구조 섹션(표·목록·노트·표제)
        for tag in ("li", "td", "caption", "figcaption", "div", "blockquote"):
            for x in re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", body_noaside, re.S):
                t = clean(x)
                if len(t) >= 12 and not t.replace(" ", "").replace(".", "").isdigit():
                    lead_sents.append(t if t[-1] in ".!?—" else t + ".")
                if len(lead_sents) >= 3: break
            if lead_sents: break
    if not lead_sents:                                        # 폴백 3: h2/h3 표제 결합
        heads = [clean(x) for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body_noaside, re.S)]
        if heads: lead_sents = [" · ".join(heads[:4]) + "."]

    body_fig = re.sub(r'<p class="abstract".*?</p>', "", body, flags=re.S)  # 누수 방지: 플레이스홀더 제거 후 키피겨 탐색
    abstract = build_abstract(claims, lead_sents, body_noaside)             # 키피겨는 aside(클레임-스트립) 제외 본문에서만
    desc = fit_desc(claims[:3] if claims else lead_sents[:3])
    grade = page_grade(body)
    if re.match(r"\s*(How to Read|Read First)", clean(h1), re.I):
        grade = None   # 등급 체계를 정의·설명하는 메타 안내 페이지 → 클레임 아님 → null

    # --- 반작문(anti-invention) 자체검사: abstract·desc 의 모든 수치는 본문 ∪ 레지스트리에 존재 ---
    body_nums = set(NUM.findall(strip_tags(body)))
    reg_nums = set()
    for kf in reg["keyfigs"]: reg_nums |= set(NUM.findall(kf))
    for n in set(NUM.findall(abstract)) | set(NUM.findall(desc)):
        if n not in body_nums and n not in reg_nums:
            return None, f"invent-number:{n}"

    # --- 타깃 치환(유일 마커, 각 1회) ---
    edits = 0
    new = html

    def sub1(pattern, repl, s, flags=0):
        return re.subn(pattern, repl, s, count=1, flags=flags)

    short_rx = re.escape(reg["short"])
    new, n = sub1(r"<title>.*?(" + short_rx + r"\s*§[^<|]*\|\s*Jamming Physics)</title>",
                  lambda mo: f"<title>{subj} — {mo.group(1)}</title>", new, re.S)
    if n != 1: return None, "title-marker-miss"
    edits += n

    new, n = sub1(r'(<meta name="description" content=")[^"]*(">)',
                  lambda mo: mo.group(1) + aesc(desc) + mo.group(2), new)
    if n != 1: return None, "desc-marker-miss"
    edits += n

    new, n = sub1(r'("headline":")[^"]*(")',
                  lambda mo: mo.group(1) + jesc(subj) + mo.group(2), new)
    edits += n  # 선택적

    def bc(mo):
        stub = mo.group(2); sec = stub.split()[0] if stub.split() else "§"
        return mo.group(1) + f"{sec} {jesc(subj)}" + mo.group(3)
    new, n = sub1(r'("position":3,"name":")([^"]*)(")', bc, new)
    edits += n  # 선택적

    new, n = sub1(r'(<p class="abstract"[^>]*>).*?(</p>)',
                  lambda mo: mo.group(1) + abstract + mo.group(2), new, re.S)
    if n != 1: return None, "abstract-marker-miss"
    edits += n

    if grade:
        cls, label, _ = grade
        new, n = sub1(r'<span class="g"(\s+data-phase2="grade")></span>',
                      lambda mo: f'<span class="g {cls}"{mo.group(1)}>{label}</span>', new)
        edits += n

    meta = {"one_liner": (claims[0] if claims else None),
            "grade": (grade[2] if grade else None)}
    return (new, meta), None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    paper = a.paper
    reg = REGISTRY[paper]
    load_grade_vocab(paper)

    prefill = {}
    pf = f"reports/phase2-prefill-{paper}.csv"
    if os.path.exists(pf):
        for r in csv.DictReader(open(pf)):
            prefill[r["slug"]] = r

    files = sorted(glob.glob(f"docs/{paper}/*/index.html"))
    meta_path = f"docs/{paper}/_meta.json"
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {"chapters": []}
    by_slug = {c.get("slug"): c for c in meta.get("chapters", [])}

    ok = 0; errs = []
    for f in files:
        slug = os.path.basename(os.path.dirname(f))
        html = open(f, encoding="utf-8").read()
        prow = prefill.get(slug, {})
        res, err = derive_section(html, prow, reg)
        if err:
            errs.append((slug, err)); continue
        new_html, m = res
        if not a.dry:
            open(f, "w", encoding="utf-8").write(new_html)
            if slug in by_slug:
                by_slug[slug]["one_liner"] = m["one_liner"]
                by_slug[slug]["grade"] = m["grade"]
        ok += 1

    if not a.dry:
        json.dump(meta, open(meta_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"[derive_meta] {paper}: filled {ok}/{len(files)} sections"
          + (f" | _meta chapters updated" if not a.dry else " (dry)"))
    if errs:
        print(f"[derive_meta] {len(errs)} section(s) FAILED (not written):")
        for s, e in errs[:20]: print(f"   - {s}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
