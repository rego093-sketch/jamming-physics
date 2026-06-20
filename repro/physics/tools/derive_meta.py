#!/usr/bin/env python3
# tools/derive_meta.py — VP-SPEC v1.8 Phase 2 tool (r7). 결정론 파생.
#   r6(v1.7) 기능 보존: data-phase2 후크(abstract·grade) + title/description/JSON-LD 를
#     **봉인 본문에서만** 채운다(임의 작문·요약 금지).
#   r7(v1.8) 추가: 헌법 C4 검색 수용성 —
#     (A) answer-first  <p class="answer">  : 페이지 자체완결 직답(엔티티+값/결론+등급, 40~60단어)
#     (B) 자체완결 카드  aside.vp-card        : 본문이 인용하는 잠금 정량마다 1개(레지스트리 registry/vp_locks.csv)
#   answer·vp-card 는 모두 gate.words_of 의 제외영역(answer 는 r7 gate 가 제외 추가, aside 는 기존 제외)
#     이므로 본문 단어수(±0.5%)는 구성상 불변. 본문·수식·수치는 일절 건드리지 않는다(삽입만, 멱등).
# 사용: python3 tools/derive_meta.py --paper physics
import re, os, sys, csv, json, argparse, glob, hashlib
from collections import Counter

REGISTRY = {
  "physics": {"short": "VP Theory",
              "keyfigs": ["c² = B/ρ", "m_p/m_e = 6π⁵"]},
}
GRADE = {"F": ("g-forced", "forced"), "H": ("g-hypothesis", "hypothesis"),
         "V": ("g-verified", "verified"), "O": ("g-open", "open")}
GRADE_PRIORITY = "FVHO"
GRADE_TAG = {"F": "forced", "H": "hypothesis", "V": "verified", "O": "open"}

GATEFIG = re.compile(r"[0-9].*[=×·π/^²³⁴⁵]|[=×·π].*[0-9]")
NUM = re.compile(r"\d+(?:\.\d+)?")

def strip_tags(s): return re.sub(r"<[^>]+>", " ", s)
def ws(s): return re.sub(r"\s+", " ", s).strip()

def clean(s):
    s = strip_tags(s)
    s = s.replace("$", " ")          # 인라인 수식 '$…$' 경계 보존(공백화) → 'speed$c²$' 붙음 방지
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    return ws(s)

def sentences(text):
    text = ws(text)
    parts = re.split(r"(?<=[.!?—])\s+", text)
    return [p.strip() for p in parts if p.strip()]

def _balance_open(s):
    """짝 없는 '(' 꼬리를 잘라 균형을 맞춘다(엔티티명이 '(1:' 처럼 끊기는 것을 방지)."""
    depth = 0; cut = None
    for k, c in enumerate(s):
        if c == "(":
            if depth == 0: cut = k
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
    if depth > 0 and cut is not None:
        s = s[:cut].rstrip(" ([{—-:;,")
    return ws(s)

def _trim_subj(s):
    """제목 말미의 매달린 구두점·접속/전치사 제거('… and' → '…', 'Core derivations +' → '…')."""
    s = s.rstrip(" +-—–/:;,·")
    s = re.sub(r"\s+(?:and|or|of|to|the|an?|for|with|in|on|by|that|which)$", "", s, flags=re.I)
    return s.rstrip(" +-—–/:;,·")

def subj45(h1):
    s = ws(h1)
    s = re.split(r"\s*-{2,}\s*", s)[0].strip() or s   # '---'/'--'(em-dash 대용) 구분자에서 머리만(짧아도 적용)
    if len(s) <= 45:
        r = s
    else:
        s2 = re.sub(r"\s*\([^()]*\)\s*$", "", s).strip()
        if 0 < len(s2) <= 45:
            r = s2
        else:
            s = s2 or s
            r = None
            for sep in [":", " — ", "—", ";", ",", " from "]:
                if sep in s:
                    head = s.split(sep)[0].strip()
                    if 0 < len(head) <= 45: r = head; break
                    if 0 < len(head) < len(s): s = head
            if r is None:
                if len(s) <= 45:
                    r = s
                else:
                    out = ""
                    for w in s.split():
                        if len((out + " " + w).strip()) > 45: break
                        out = (out + " " + w).strip()
                    r = out or s[:45].strip()
    return _balance_open(_trim_subj(r))

def fit_desc(parts):
    d = ws(parts[0]) if parts else ""
    i = 1
    while len(d) < 80 and i < len(parts):
        d = ws(d + " " + parts[i]); i += 1
    if len(d) < 80:
        d = ws(d + " — VP Theory, Jamming Physics.")
    if len(d) > 160:
        cut = d[:160]
        cut = cut[:cut.rfind(" ")] if " " in cut else cut
        d = cut.strip()
    return d

def jesc(s): return s.replace("\\", "\\\\").replace('"', '\\"')
def aesc(s): return s.replace('"', "'")

_FIGTOK = re.compile(r"[0-9]\S*[=×·π/^²³⁴⁵]|[=×·π]\S*[0-9]")
def figure_snippet(noaside_html):
    """abstract 의 검색-대표 수치(FIG) 요건용 짧고 깨끗한 수식. greedy 표 덤프 금지."""
    gate_text = ws(re.sub(r"<[^>]+>", " ", noaside_html).replace("$", " "))  # 인라인 수식 '$' 경계화
    sents = _sent_keep_dash(_presplit(gate_text))
    # 1) 수식을 포함한 짧은(≤16어) 산문 문장 우선
    best = None
    for s in sents:
        c = _trim_tail(_clean_sent(s))
        if c and GATEFIG.search(c) and _is_prose(c) and len(c.split()) <= 16 \
           and "§" not in c and not re.match(r"^[A-Z]\.\d", c) \
           and not any(len(w) > 14 for w in c.split()):  # 절참조·표제머리('W.3')·경로토큰 배제
            if best is None or len(c.split()) < len(best.split()): best = c
    if best: return best
    # 2) 폴백: 가장 짧은 깨끗한 단일 수식 토큰('c²=B/ρ','6π⁵'); 풍부한 수학기호(π·지수·×) 우선
    eqs = []
    for w in re.findall(r"\S+", gate_text):
        e = _clean_sent(w).strip(".,;:()[]—–=×·\"'")                 # 선·후행 연산자/따옴표 제거
        e = re.sub(r"'s$", "", e)                                    # 접합 소유격 제거('3π⁴\'s'→'3π⁴')
        if e and GATEFIG.search(e) and len(e) <= 24 and not _TEXCTL.search(e) and e[-1:] != "=" \
           and not re.search(r"[A-Za-z]{3,}\d", e):                  # 'sha256' 등 단어+숫자 접합 토큰 배제
            eqs.append(e)
    if not eqs: return ""
    rich = [e for e in eqs if re.search(r"[π²³⁴⁵×·]", e)]
    return min(rich or eqs, key=len)

def build_abstract(claims, lead_sents, noaside_html):
    seen = set(); pool = []
    for x in list(claims) + list(lead_sents):         # 클레임 우선; 산문 클레임이 없으면 리드 산문으로 폴백
        k = ws(x).lower()
        if k and k not in seen: seen.add(k); pool.append(x)
    cleaned = [_trim_tail(_clean_sent(_presplit(x))) for x in pool]
    cleaned = [c for c in cleaned if c]
    prose = [c for c in cleaned if _is_prose(c)]      # 산문만(접합·라벨·수식·표제 클레임 건너뜀)
    base = (prose or cleaned)[:2]                      # 산문 없으면 정리본으로 폴백(빈 abstract 방지)
    # FIG(검색-대표 수치) 요건: base 에 수식이 없고 풀에 수식 산문이 있으면 한 문장 끌어옴
    if base and not any(GATEFIG.search(b) for b in base):
        figp = next((p for p in prose if GATEFIG.search(p)), None)
        if figp and figp not in base:
            base = ([base[0], figp] if base else [figp])[:2]
    abs_txt = ws(" ".join(b if b[-1] in ".!?—" else b + "." for b in base))
    ss = _sent_keep_dash(abs_txt)
    if len(ss) > 2: abs_txt = ws(" ".join(ss[:2]))
    # 최후: base 에 여전히 수식이 없고 본문에 수식이 있으면, 짧고 한정된 수식 구절을 부가
    if not GATEFIG.search(abs_txt):
        snip = figure_snippet(noaside_html)
        if snip and GATEFIG.search(snip):
            if abs_txt and abs_txt[-1] not in ".!?—": abs_txt += "."
            abs_txt = ws((abs_txt + " " + snip).strip())
    abs_txt = _trim_tail(abs_txt)
    if abs_txt and abs_txt[-1] not in ".!?—": abs_txt += "."
    return abs_txt

def page_grade(body):
    toks = re.findall(r'<aside class="claim-strip vps"[^>]*>.*?</aside>', body, re.S)
    grades = []
    for a in toks:
        grades += re.findall(r"\[([FHVO])\]", a)
    if not grades: return None
    cnt = Counter(grades)
    best = sorted(cnt, key=lambda g: (-cnt[g], GRADE_PRIORITY.index(g)))[0]
    cls, name = GRADE[best]
    return cls, f"[{best}] {name}", name, best

# ---------- r7 (v1.8 C4): answer-first ----------
def _sent_keep_dash(text):
    """문장 분할(중간 em-dash 보존 — 이 코퍼스는 — 를 문장 내부 연결로 쓴다).
       괄호 인지: 괄호( ) 내부의 마침표/물음표에서는 분할하지 않는다(수식·약물 단편 방지)."""
    text = ws(text); res = []; cur = []; depth = 0
    ch = list(text)
    for j, c in enumerate(ch):
        cur.append(c)
        if c == "(": depth += 1
        elif c == ")" and depth > 0: depth -= 1
        elif c in ".!?" and depth == 0 and (j + 1 >= len(ch) or ch[j + 1].isspace()):
            res.append("".join(cur).strip()); cur = []
    if cur: res.append("".join(cur).strip())
    return [p for p in res if p]

def _clean_sent(s):
    """단편 정리: 짝 없는 ')' 제거, 닫히지 않은 '(' 이후 절단, 구두점 다듬기. 내용은 추가하지 않음."""
    s = ws(s); out = []; depth = 0
    for c in s:
        if c == "(": depth += 1; out.append(c)
        elif c == ")":
            if depth > 0: depth -= 1; out.append(c)   # 짝 없는 ')'는 버림
        else: out.append(c)
    s = "".join(out)
    if depth > 0:                                     # 닫히지 않은 '(' → 그 지점부터 절단
        i = s.rfind("("); s = s[:i].rstrip() if i >= 0 else s
    s = s.replace("{}", "").replace("{", "").replace("}", "")  # 빈/짝 없는 중괄호(LaTeX 잔재 '[F]{}') 제거
    s = re.sub(r"\(\s*\(", "(", s); s = re.sub(r"\)\s*\)", ")", s)  # '( (' · ') )' → 단일 괄호
    s = re.sub(r"\s+([.,;:])", r"\1", s)              # 구두점 앞 공백 제거
    s = re.sub(r"[,:]\s*\.", ".", s)                  # ',.' · ':.' → '.'
    s = re.sub(r"\.{2,}", ".", s)                     # '..' → '.'
    s = re.sub(r"\b(\w+)\s+\1\b", r"\1", s, flags=re.I)  # 인접 중복 단어('as as' → 'as')
    return ws(s).rstrip(",;: ")

_WORD3 = re.compile(r"[A-Za-z][A-Za-z]{2,}")
def _has_word(s):
    """알파벳 3자 이상 단어가 하나라도 있어야 '문장'(순수 수식 단편 배제)."""
    return bool(_WORD3.search(s))

_SEC_NUM   = re.compile(r"^[\(\[]?\s*\d+(?:\.\d+)+")             # 절 번호 '1.2.4', '2.1'
_ROMAN     = re.compile(r"^[\(\[]?\s*(?:i{1,3}|iv|v|vi{0,3}|ix|x)\)", re.I)  # 목록 표지 '(iii)'
_LABEL     = re.compile(r"^[\(\[]?[A-Z][A-Z0-9]*[-_][A-Z0-9_.-]+") # 라벨 코드 'F-SCHEMA-003','VP-A4','[D-11.1-1]'
_TEXCTL    = re.compile(r"\\[A-Za-z]{2,}|\^\{|_\{|\^[\dA-Za-z*]") # 원시 TeX/지수 잔재 '\tau','c^{2}','c^2','g^*'
def _is_prose(s):
    """직답에 쓸 수 있는 산문 문장만 통과(제목·라벨·수식·파일명·연속 단편 배제)."""
    t = ws(s)
    if not t or not _has_word(t): return False
    if len(t.split()) < 4: return False                          # 너무 짧은 단편('They.','(iii).')
    a = next((c for c in t if c.isalpha()), "")
    if "a" <= a <= "z": return False                             # 소문자(라틴) 시작 = 연속 단편('used below…','the wh…')
    if _SEC_NUM.match(t) or _ROMAN.match(t) or _LABEL.match(t): return False
    if re.match(r"^\([A-Za-z]{1,3}-[A-Za-z0-9]", t): return False # 괄호 규칙코드 머리 '(R-c1)','(VP-A4)'
    if _TEXCTL.search(t): return False                           # 원시 TeX 제어열
    if re.search(r"[a-z][A-Zα-ωΑ-Ω]", t): return False           # 공백 누락 접합('anchorλ_ref','byA_geo')
    if re.search(r"[A-Za-z]{3,}\d", t): return False             # 단어(3+자)+숫자 접합('radius0.8414'); 버전표기 'v25'는 보존
    if any(len(w) > 30 for w in t.split()): return False         # 긴 파일명 토큰
    body = t.replace(" ", "")
    if body and sum(c.isalpha() for c in body) / len(body) < 0.45: return False  # 알파벳 비율↓ = 수식/기호 수프
    return True

def _presplit(text):
    """'---'·'--'(em-dash 대용 하이픈 런)을 문장 경계로 정규화. 단일 em-dash '—'는 보존."""
    return re.sub(r"\s*-{2,}\s*", ". ", ws(text))

_KEEP2 = {"a","i","is","to","of","or","as","at","in","on","by","up","no","so","we","he","it",
          "be","do","go","us","am","an","my","me","ok","id"}
def _trim_tail(s):
    """말미의 매달린 대시·접속/전치사/관사·짧은 비단어 토큰(예: 'the wh'의 'wh') 제거. 내용 추가 0."""
    prev = None
    while s and s != prev:
        prev = s
        s = s.rstrip(" ,;:/—–-")
        s = re.sub(r"\s*-{2,}$", "", s)
        s = re.sub(r"[\s]+(?:and/or|and|or|but|nor|into|onto|for|with|of|to|as|by|the|an?|that|which|then|thus|hence|when|where|while|because|since|if)\s*\.?$",
                   "", s, flags=re.I)
        m = re.search(r"\s+([a-z]{2})\.?$", s)          # 2자 소문자 비단어('wh')만; 단문자/대문자 수식기호(R,C,X)는 보존
        if m and m.group(1).lower() not in _KEEP2: s = s[:m.start()]
    return s.rstrip(" ,;:/—–-")

def build_answer(subj, claims, abstract, lead_sents, gletter):
    """엔티티 명명 + 핵심 값/결론 + 등급, 40~60단어 자체완결 직답. 출처는 본문에서 파생된
       abstract(이미 큐레이트 클레임 기반)·리드 문장뿐(임의 작문 0). 결정론·멱등.
       산문 필터(_is_prose)로 제목·라벨·수식·연속 단편을 배제하고, 완전 문장만 예산에 넣어
       말미 절단 단편을 원천 차단한다."""
    raw = _sent_keep_dash(_presplit(abstract)) + [t for s in lead_sents for t in _sent_keep_dash(_presplit(s))]
    ordered = []
    for s in raw:
        s = _trim_tail(_clean_sent(s))                  # 괄호/구두점 + 문장 말미 매달림 정리
        if not _is_prose(s): continue                   # 산문이 아닌 단편(제목·라벨·수식·연속) 제외
        sl = s.lower().rstrip(".")
        skip = False; repl = None
        for k, ex in enumerate(ordered):
            exl = ex.lower().rstrip(".")
            if sl == exl or (len(sl) >= 12 and sl in exl):   # 신규가 기존의 (부분)중복
                skip = True; break
            if len(exl) >= 15 and exl in sl:                  # 기존이 신규의 접두/부분 → 더 긴 신규로 교체
                repl = k; break
        if skip: continue
        sfin = s if s[-1] in ".!?—" else s + "."
        if repl is not None: ordered[repl] = sfin
        else: ordered.append(sfin)
    # r7.2: 풀 문장이 제목(subj)으로 시작하면 그 접두를 제거(직답에서 "subj: subj:" 중복 방지)
    subj_l = subj.lower()
    def _desubj(s):
        if s.lower().lstrip().startswith(subj_l):
            rest = s.lstrip()[len(subj):].lstrip(" :—-\t")
            if rest and _is_prose(rest): return rest
        return s
    ordered = [_desubj(s) for s in ordered]
    ordered = [s for s in ordered if _is_prose(s)]
    wc = lambda s: len(s.split())
    grade_words = 3 if gletter else 0          # " Grade [F] forced." ≈ 3 words
    cap = 60 - grade_words
    if ordered:
        first = ordered[0]
        body = ws(f"{subj}: {first}")
        idx = 1
        while idx < len(ordered) and wc(body) < 40:     # 완전 문장만 추가(단어 슬라이스 금지 → 말미 단편 차단)
            nxt = ordered[idx]; idx += 1
            if wc(body) + wc(nxt) <= cap:
                body = ws(body + " " + nxt)
            else:
                break
        if wc(body) > cap:                              # 첫 문장 자체가 cap 초과 시에만 단어 경계 절단
            body = " ".join(body.split()[:cap])
    else:
        body = ws(subj)                                 # 산문 후보 없음(짧은 색인/부록) → 제목만
    body = _trim_tail(_clean_sent(body))                # 괄호/구두점 정리 + 말미 매달림/짧은 비단어 제거
    if body and body[-1] not in ".!?—": body += "."
    if gletter:
        body = ws(body + f" Grade [{gletter}] {GRADE_TAG[gletter]}.")
    return ws(body)

# ---------- r7 (v1.8 C4): vp-card from lock registry ----------
def section_label(slug):
    m = re.match(r"^(\d+)-", slug)
    if m: return "§" + str(int(m.group(1)))
    return "§" + slug.split("-")[0].upper()

def load_locks(path):
    if not os.path.exists(path): return []
    return list(csv.DictReader(open(path, encoding="utf-8")))

def build_vp_cards(main_body_text, slug, locks):
    """본문이 인용(토큰 출현)하는 잠금 정량마다 자체완결 카드 1개. 정본 SSOT 섹션 자신에는
       카드를 달지 않는다(중복·자기참조 방지). 값·의미·등급·정본 유도 링크 포함."""
    cards = []
    for L in locks:
        tok = (L.get("match_token") or "").strip()
        if not tok or tok not in main_body_text: continue
        if L.get("canon_slug") == slug: continue
        sym = L["symbol"].strip(); val = L["value"].strip(); meaning = L["meaning"].strip()
        gl = L["grade"].strip()
        sec = section_label(L["canon_slug"])
        url = f'/physics/{L["canon_slug"]}/'
        lead = f"{sym} = {val}" if val[:1] not in "≈=<>~" else f"{sym} {val}"
        cards.append(
            f'<aside class="vp-card" data-locked="{L["lock_id"]}">'
            f'<b>{lead}</b> — {meaning} <b>[{gl}]</b> {GRADE_TAG.get(gl, "")}. '
            f'<a href="{url}">canonical derivation {sec}</a></aside>'
        )
    return cards

def derive_section(html, prow, reg, locks):
    body_m = re.search(r"<main>(.*)</main>", html, re.S)
    body = body_m.group(1) if body_m else html
    body_noaside = re.sub(r"<aside.*?</aside>", "", body, flags=re.S)
    body_noaside = re.sub(r'<p class="abstract".*?</p>', "", body_noaside, flags=re.S)
    body_noaside = re.sub(r'<p class="answer".*?</p>', "", body_noaside, flags=re.S)  # r7.2: 자기 주입 직답 환류 차단(멱등)

    h1 = prow.get("h1") or (re.search(r"<h1>(.*?)</h1>", html, re.S) or [None, ""])[1]
    subj = subj45(clean(h1))

    claims = [clean(x) for x in re.findall(r'<q class="one">(.*?)</q>', body, re.S)]
    if not claims:
        claims = [clean(x) for x in (prow.get("one_liner_pool", "").split("|")) if clean(x)]

    lead_sents = []
    for p in re.findall(r"<p>(.*?)</p>", body_noaside, re.S):
        for t in _sent_keep_dash(_presplit(clean(p))):
            t = _clean_sent(t)
            if _is_prose(t): lead_sents.append(t if t[-1] in ".!?—" else t + ".")
        if len(lead_sents) >= 4: break
    if not lead_sents:                                  # 산문 <p> 부재 시 li/td/캡션에서 산문만
        for tag in ("li", "td", "caption", "figcaption", "div", "blockquote"):
            for x in re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", body_noaside, re.S):
                for t in _sent_keep_dash(_presplit(clean(x))):
                    t = _clean_sent(t)
                    if _is_prose(t): lead_sents.append(t if t[-1] in ".!?—" else t + ".")
                if len(lead_sents) >= 3: break
            if lead_sents: break
    if not lead_sents:                                  # 최후: 기존 관대 추출(abstract 비지 않게)
        for p in re.findall(r"<p>(.*?)</p>", body_noaside, re.S):
            lead_sents += sentences(clean(p))
            if len(lead_sents) >= 3: break
    if not lead_sents:
        for tag in ("li", "td", "caption", "figcaption", "div", "blockquote"):
            for x in re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", body_noaside, re.S):
                t = clean(x)
                if len(t) >= 12 and not t.replace(" ", "").replace(".", "").isdigit():
                    lead_sents.append(t if t[-1] in ".!?—" else t + ".")
                if len(lead_sents) >= 3: break
            if lead_sents: break
    if not lead_sents:
        heads = [clean(x) for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body_noaside, re.S)]
        if heads: lead_sents = [" · ".join(heads[:4]) + "."]

    abstract = build_abstract(claims, lead_sents, body_noaside)
    desc = fit_desc(claims[:3] if claims else lead_sents[:3])
    grade = page_grade(body)
    gletter = grade[3] if grade else None
    answer = build_answer(subj, claims, abstract, lead_sents, gletter)

    # 반작문: abstract·desc·answer 의 모든 수치는 본문 ∪ 레지스트리에 존재
    body_nums = set(NUM.findall(strip_tags(body)))
    reg_nums = set()
    for kf in reg["keyfigs"]: reg_nums |= set(NUM.findall(kf))
    def strip_secrefs(t): return re.sub(r"§\s*\d+(?:\.\d+)*", " ", t)
    for n in set(NUM.findall(strip_secrefs(abstract))) | set(NUM.findall(strip_secrefs(desc))) \
             | set(NUM.findall(strip_secrefs(answer))):
        if n not in body_nums and n not in reg_nums:
            return None, f"invent-number:{n}"

    # vp-card 입력: main 본문 텍스트(기존 vp-card 제거 후, 태그 제거)
    main_for_cards = re.sub(r'<aside class="vp-card".*?</aside>', "", body, flags=re.S)
    main_text = strip_tags(main_for_cards)
    cards = build_vp_cards(main_text, prow.get("slug", ""), locks)

    edits = 0
    new = html

    def sub1(pattern, repl, s, flags=0):
        return re.subn(pattern, repl, s, count=1, flags=flags)

    new, n = sub1(r"<title>.*?(VP Theory\s*§[^<|]*\|\s*Jamming Physics)</title>",
                  lambda mo: f"<title>{subj} — {mo.group(1)}</title>", new, re.S)
    if n != 1: return None, "title-marker-miss"
    edits += n

    new, n = sub1(r'(<meta name="description" content=")[^"]*(">)',
                  lambda mo: mo.group(1) + aesc(desc) + mo.group(2), new)
    if n != 1: return None, "desc-marker-miss"
    edits += n

    new, n = sub1(r'("headline":")[^"]*(")',
                  lambda mo: mo.group(1) + jesc(subj) + mo.group(2), new)
    edits += n

    def bc(mo):
        stub = mo.group(2); sec = stub.split()[0] if stub.split() else "§"
        return mo.group(1) + f"{sec} {jesc(subj)}" + mo.group(3)
    new, n = sub1(r'("position":3,"name":")([^"]*)(")', bc, new)
    edits += n

    new, n = sub1(r'(<p class="abstract"[^>]*>).*?(</p>)',
                  lambda mo: mo.group(1) + abstract + mo.group(2), new, re.S)
    if n != 1: return None, "abstract-marker-miss"
    edits += n

    if grade:
        cls, label, _, _ = grade
        new, n = sub1(r'<span class="g"(\s+data-phase2="grade")></span>',
                      lambda mo: f'<span class="g {cls}"{mo.group(1)}>{label}</span>', new)
        edits += n

    # --- r7: answer-first 삽입(멱등: 기존 제거 후 h1 직후 삽입) ---
    new = re.sub(r'\s*<p class="answer">.*?</p>', "", new, flags=re.S)
    ans_block = f'\n<p class="answer">{answer}</p>'
    new, n = sub1(r"(</h1>)", lambda mo: mo.group(1) + ans_block, new)
    if n != 1: return None, "answer-h1-miss"
    edits += n

    # --- r7: vp-card 삽입(멱등: 기존 제거 후, 페이지 claim-strip 직후; 없으면 abstract 직후) ---
    new = re.sub(r'\s*<aside class="vp-card".*?</aside>', "", new, flags=re.S)
    if cards:
        block = "\n" + "\n".join(cards)
        new2, n = sub1(r'(<aside class="claim-strip page">.*?</aside>)',
                       lambda mo: mo.group(1) + block, new, re.S)
        if n != 1:
            new2, n = sub1(r'(<p class="abstract"[^>]*>.*?</p>)',
                           lambda mo: mo.group(1) + block, new, re.S)
        if n == 1:
            new = new2; edits += 1

    meta = {"one_liner": (claims[0] if claims else None),
            "grade": (grade[2] if grade else None)}
    return (new, meta), None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True)
    ap.add_argument("--locks", default="registry/vp_locks.csv")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    paper = a.paper
    reg = REGISTRY[paper]
    locks = load_locks(a.locks)

    prefill = {}
    pf = f"reports/phase2-prefill-{paper}.csv"
    if os.path.exists(pf):
        for r in csv.DictReader(open(pf)):
            prefill[r["slug"]] = r

    files = sorted(glob.glob(f"docs/{paper}/*/index.html"))
    meta_path = f"docs/{paper}/_meta.json"
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {"chapters": []}
    by_slug = {c.get("slug"): c for c in meta.get("chapters", [])}

    ok = 0; errs = []; ncards = 0; nans = 0
    for f in files:
        slug = os.path.basename(os.path.dirname(f))
        html = open(f, encoding="utf-8").read()
        prow = dict(prefill.get(slug, {})); prow["slug"] = slug
        res, err = derive_section(html, prow, reg, locks)
        if err:
            errs.append((slug, err)); continue
        new_html, m = res
        nans += new_html.count('<p class="answer">')
        ncards += new_html.count('<aside class="vp-card"')
        if not a.dry:
            open(f, "w", encoding="utf-8").write(new_html)
            if slug in by_slug:
                by_slug[slug]["one_liner"] = m["one_liner"]
                by_slug[slug]["grade"] = m["grade"]
        ok += 1

    if not a.dry:
        json.dump(meta, open(meta_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"[derive_meta r7] {paper}: filled {ok}/{len(files)} sections | "
          f"answer-first={nans} | vp-cards={ncards}"
          + ("" if not a.dry else " (dry)"))
    if errs:
        print(f"[derive_meta] {len(errs)} section(s) FAILED (not written):")
        for s, e in errs[:20]: print(f"   - {s}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
