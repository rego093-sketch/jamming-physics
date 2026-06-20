#!/usr/bin/env python3
# preprocess_cosmology.py — EarthCosmos .tex 를 VP-SPEC 도구 입력으로 정규화.
#  (G1) EarthCosmos 전용 매크로 8종 펼침(물리 도구 WPMAC/MACROS 미보유분).
#  (구조) report 클래스 \chapter 를 페이지 단위(\section)로 승격, 중첩 헤딩 1단계 강등.
#         inventory.find_sections 가 \section 만 인식하므로, "챕터 페이지"(SPEC §6) 의도대로
#         \chapter→page, 그 안의 \section→h2(\subsection), \subsection→h3, \subsubsection→\paragraph.
# 결정론·stdlib. 본문 의미·수식·수치 무변경(헤딩 레벨·매크로 표기만 정규화).
import re, sys, hashlib

MACROS = [  # (name, expansion) — 긴 이름 우선 정렬은 아래에서 처리
    (r"\physvol", r"\href{https://doi.org/10.5281/zenodo.17932566}{\texttt{10.5281/zenodo.17932566}}"),
    (r"\nuH",     r"\nu_{\mathrm{H}}"),
    (r"\nup",     r"\nu_{p}"),
    (r"\nue",     r"\nu_{e}"),
    (r"\kopt",    r"\kappa_{\mathrm{opt}}"),
    (r"\persec",  r"\,\mathrm{s^{-1}}"),
    (r"\az",      r"a_{0}"),
    (r"\Q",       r"Q"),
]

def expand_macros(t):
    # \newcommand 정의 줄 제거(프리앰블; 도구가 본문만 처리하나 안전하게)
    for name, _ in MACROS:
        t = re.sub(r"\\newcommand\{" + re.escape(name) + r"\}\{[^\n]*\}\n", "", t)
    # 사용처 펼침 — 매크로 경계(뒤에 영문자 금지)
    for name, exp in sorted(MACROS, key=lambda x: -len(x[0])):
        t = re.sub(re.escape(name) + r"(?![a-zA-Z])", exp.replace("\\", "\\\\"), t)
    return t

def number_chapters(t):
    # \appendix 기준으로 본문/부록 분리 후 \chapter 제목에 번호·부록문자 부여.
    #  - \chapter*{...}(How to Read) → "0. ..."  → classify "00"
    #  - 본문 \chapter{...} 순서대로 → "1. ", "2. ", ...  → "01".."10"
    #  - \appendix 이후 \chapter{...} → "Appendix A: ", "B: ", ...  → "axa".."axe"
    parts = re.split(r"(^\\appendix\s*$)", t, maxsplit=1, flags=re.M)
    body = parts[0]
    tail = "".join(parts[1:]) if len(parts) > 1 else ""

    # 본문: \chapter*{} → 0, \chapter{} → 1,2,...
    body_counter = {"n": 0}
    def body_repl(m):
        star, title = m.group(1), m.group(2)
        if star:  # \chapter*{} = How to Read
            return r"\chapter*{0. " + title + "}"
        body_counter["n"] += 1
        return r"\chapter{" + f"{body_counter['n']}. " + title + "}"
    body = re.sub(r"\\chapter(\*?)\{([^}]*)\}", body_repl, body)

    # 부록: \chapter{} → Appendix A:, B:, ...
    app_counter = {"i": 0}
    def app_repl(m):
        title = m.group(2)
        letter = chr(ord("A") + app_counter["i"]); app_counter["i"] += 1
        return r"\chapter{Appendix " + letter + ": " + title + "}"
    tail = re.sub(r"\\chapter(\*?)\{([^}]*)\}", app_repl, tail)

    return body + tail

def promote_headings(t):
    # 깊은 레벨부터 보호 후 1단계씩 강등, 마지막에 \chapter→\section 승격
    t = re.sub(r"\\subsubsection(\*?)\{", r"⟪P4⟫\1{", t)   # 보호: → \paragraph
    t = re.sub(r"\\subsection(\*?)\{",    r"⟪H3⟫\1{", t)   # 보호: → \subsubsection
    t = re.sub(r"\\section(\*?)\{",       r"\\subsection\1{", t)   # \section → h2
    t = re.sub(r"\\chapter(\*?)\{",       r"\\section\1{", t)      # \chapter → page
    t = re.sub(r"⟪H3⟫(\*?)\{", r"\\subsubsection\1{", t)
    t = re.sub(r"⟪P4⟫(\*?)\{", r"\\paragraph\1{", t)
    return t

def main():
    src, dst = sys.argv[1], sys.argv[2]
    t = open(src, encoding="utf-8").read()
    n_chap = len(re.findall(r"^\\chapter", t, re.M))
    n_sec  = len(re.findall(r"^\\section", t, re.M))
    t = expand_macros(t)
    t = number_chapters(t)
    t = promote_headings(t)
    open(dst, "w", encoding="utf-8").write(t)
    n_page = len(re.findall(r"^\\section", t, re.M))
    sha = hashlib.sha256(t.encode()).hexdigest()
    print(f"[preprocess] chapters_in={n_chap} sections_in={n_sec} → pages_out(\\section)={n_page}")
    print(f"[preprocess] dst_sha256={sha}")

if __name__ == "__main__":
    main()
