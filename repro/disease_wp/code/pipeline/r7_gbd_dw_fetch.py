#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R7 stage 1 -- GBD disability-weights FETCH (the open, credential-free D source).

Pulls the canonical Global Burden of Disease *disability-weights* table and pins
its sha256, then parses it deterministically into a machine-readable table that
the offline apply stage (r7_naturalhistory_registry2.py) reads to lift the
DISABILITY axis (D) from definition-grade [H]/[O] toward registry-grade [L].

SOURCE (open access, no credential):
  Salomon JA, Haagsma JA, Davis A, et al. "Disability weights for the Global
  Burden of Disease 2013 study." Lancet Glob Health 2015;3(11):e712-23.
  Appendix (mmc1.pdf), served openly from the Elsevier OA content CDN. The
  journal is gold open access (CC BY); the disability weights are published,
  citeable quantitative values -- a constitution C-D1 observed input, attached
  to a NAMED GBD health state, never free text we infer.

  The table reports TWO columns per state: the GBD 2013 estimate (LEFT) and the
  GBD 2010 estimate (RIGHT). This study (GBD 2013) is the canonical one, so the
  GBD 2013 / LEFT value is taken. A column-misread (accidentally taking GBD 2010)
  is the one plausible silent error, so the parser runs ANCHOR SELF-CHECKS on
  known GBD-2013 values and exits nonzero on any mismatch.

Network: this is the only R7 stage that touches the network. Idempotent -- a PDF
already on disk whose sha256 matches the pin is NOT re-downloaded. If the byte
stream ever differs from the pin the run reports it and exits 2 (never silent).

INVESTIGATION/AUTHORING support -- living code, NOT in the frozen engine pin.

Out: data/raw/gbd/salomon2015_mmc1.pdf          (pinned source PDF)
     data/raw/gbd/gbd_disability_weights.json   (parsed table: state -> dw2013, UI)
     data/raw/gbd/gbd_disability_weights.csv
     data/raw/gbd/_fetch_log.json
"""
import os, sys, re, json, hashlib, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GBD = os.path.join(ROOT, "data", "raw", "gbd")
PDF = os.path.join(GBD, "salomon2015_mmc1.pdf")
TXT = os.path.join(GBD, "salomon2015_mmc1.layout.txt")
OUT_J = os.path.join(GBD, "gbd_disability_weights.json")
OUT_C = os.path.join(GBD, "gbd_disability_weights.csv")
LOG = os.path.join(GBD, "_fetch_log.json")
RETRIEVED = "2026-06-18"

URL = "https://ars.els-cdn.com/content/image/1-s2.0-S2214109X15000698-mmc1.pdf"
PDF_SHA_PIN = "c7d22442bad82f7ff5a0b63353a6591d769d2d88a959a5c2bac960ede179bdf4"
CITATION = ("Salomon JA, Haagsma JA, Davis A, et al. Disability weights for the Global "
            "Burden of Disease 2013 study. Lancet Glob Health 2015;3(11):e712-23 "
            "(appendix mmc1.pdf, GBD 2013 estimate column); open access (CC BY), "
            "retrieved " + RETRIEVED)

# Known GBD-2013 disability weights (LEFT column) used to guard against a column
# misread (the GBD-2010 / RIGHT value is given in parentheses for contrast). Declared
# a priori from the published table; the parse MUST reproduce every one of these.
ANCHORS = {
    "Anemia: severe": (0.149, 0.164),
    "Anemia: moderate": (0.052, 0.058),
    "Motor impairment: severe": (0.402, 0.377),
    "Musculoskeletal problems: generalised, moderate": (0.317, 0.292),
    "Intellectual disability: severe": (0.160, 0.135),
    "Motor plus cognitive impairments: severe": (0.542, 0.453),
}

SEVERITY_WORDS = ("mild", "moderate", "severe", "profound")
NAMEW = 34  # layout name-column width (measured: state label occupies cols 0..33)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_pdf():
    cached_ok = os.path.exists(PDF) and sha256_file(PDF) == PDF_SHA_PIN
    if cached_ok:
        return "cached (sha matches pin)"
    print(f"  fetching {URL} ...")
    req = urllib.request.Request(URL, headers={"User-Agent": "disease_wp/0.9 GBD-DW (research; ORCID 0009-0002-7535-8245)"})
    data = urllib.request.urlopen(req, timeout=180).read()
    with open(PDF, "wb") as fh:
        fh.write(data)
    return "downloaded"


def pdf_to_layout_text():
    # deterministic: pdftotext -layout preserves the two-column table geometry, so the
    # GBD-2013 (left) value is positionally separable from GBD-2010 (right).
    subprocess.run(["pdftotext", "-layout", PDF, TXT], check=True)
    with open(TXT, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


# Appendix Table 2a/2b rows: "<state>   W2013 (lo-hi)   W2010 (lo-hi)". The trailing
# second parenthesised weight confirms a genuine two-column data row (not prose).
RE_T2 = re.compile(r"^(?P<name>\S.*?\S)\s{2,}"
                   r"(?P<w>\d\.\d{3})\s*\((?P<lo>\d\.\d{3})-(?P<hi>\d\.\d{3})\)\s+"
                   r"\d\.\d{3}\s*\(")

# A bare weight (no parenthesis directly after) sitting in the right-hand value region
# marks an Appendix Table 3 / Table 4 lead line ("<state-frag>  <desc>  W2013  <desc>  W2010",
# the 95% intervals on the following line). 0.NNN immediately followed by '(' is a Table 2 cell.
RE_BAREW = re.compile(r"(?<![\d(])(\d\.\d{3})(?!\s*[-(])")


def _has_severity(s):
    return any(w in s.lower() for w in SEVERITY_WORDS)


def parse(lines):
    table = {}            # state -> {"dw2013", "ui_lo", "ui_hi", "table", "line"}
    seen_order = []

    # ---- pass A: Table 2a/2b parenthesised rows ----
    for i, ln in enumerate(lines):
        m = RE_T2.match(ln)
        if not m:
            continue
        name = re.sub(r"\s+", " ", m.group("name")).strip()
        if name in table:
            continue
        table[name] = {"dw2013": float(m.group("w")), "ui_lo": float(m.group("lo")),
                       "ui_hi": float(m.group("hi")), "table": "2", "line": i + 1}
        seen_order.append(name)

    # ---- pass B: Table 3/4 lead lines (bare weights; revised/new descriptions) ----
    for i, ln in enumerate(lines):
        if RE_T2.match(ln):
            continue
        # candidate lead line: a bare weight in the value region (col >= 90) and the
        # left name column is non-empty
        bare = [(mm.start(), mm.group(1)) for mm in RE_BAREW.finditer(ln) if mm.start() >= 90]
        if not bare:
            continue
        namecol = ln[:NAMEW].strip()
        if not namecol or namecol[0].islower():
            continue
        w2013 = float(bare[0][1])
        # complete a wrapped name from the following line's name column when the lead
        # line carries no severity word (e.g. "Intellectual disability:" + "moderate";
        # "Motor plus cognitive" + "impairments: severe").
        name = namecol
        if not _has_severity(name) and i + 1 < len(lines):
            cont = lines[i + 1][:NAMEW].strip()
            if cont and cont[0].islower() or (cont and ":" in cont):
                name = (name + " " + cont).strip()
        name = re.sub(r"\s+", " ", name).strip()
        # 95% UI sits on the next line as "(lo, hi)" or "(lo-hi)"
        lo = hi = None
        if i + 1 < len(lines):
            mui = re.search(r"\((\d\.\d{3})[,\-]\s*(\d\.\d{3})\)", lines[i + 1])
            if mui:
                lo, hi = float(mui.group(1)), float(mui.group(2))
        if name not in table:
            table[name] = {"dw2013": w2013, "ui_lo": lo, "ui_hi": hi,
                           "table": "3/4", "line": i + 1}
            seen_order.append(name)

    return table, seen_order


def main():
    os.makedirs(GBD, exist_ok=True)
    action = fetch_pdf()
    sha = sha256_file(PDF)
    if sha != PDF_SHA_PIN:
        print(f"  ERROR: PDF sha {sha[:12]} != pin {PDF_SHA_PIN[:12]} (source re-release?). "
              "Verify the appendix and update the pin.")
        sys.exit(2)
    lines = pdf_to_layout_text()
    table, order = parse(lines)

    # ---- anchor self-checks (guard the GBD2013-vs-GBD2010 column read) ----
    failures = []
    for state, (want2013, gbd2010) in ANCHORS.items():
        got = table.get(state, {}).get("dw2013")
        if got is None:
            failures.append(f"{state!r}: NOT PARSED (expected {want2013})")
        elif abs(got - want2013) > 1e-9:
            extra = " (== GBD2010 column -- MISREAD!)" if abs(got - gbd2010) <= 1e-9 else ""
            failures.append(f"{state!r}: parsed {got} != GBD2013 {want2013}{extra}")
    if failures:
        print("  ANCHOR SELF-CHECK FAILED -- disability-weights parse is not trustworthy:")
        for f in failures:
            print("    - " + f)
        sys.exit(3)

    # ---- write parsed table ----
    payload = {
        "schema": "disease_wp.gbd_disability_weights/v1",
        "source": CITATION,
        "url": URL,
        "pdf_sha256": sha,
        "column_taken": "GBD 2013 estimate (left); GBD 2010 (right) recorded only for anchor contrast",
        "retrieved": RETRIEVED,
        "n_states": len(table),
        "anchor_self_check": {k: {"gbd2013": v[0], "parsed": table[k]["dw2013"]}
                              for k, v in ANCHORS.items()},
        "weights": {name: table[name] for name in sorted(table)},
    }
    json.dump(payload, open(OUT_J, "w"), indent=2, ensure_ascii=False)

    with open(OUT_C, "w", newline="") as fh:
        import csv
        w = csv.writer(fh)
        w.writerow(["health_state", "dw_gbd2013", "ui_lo", "ui_hi", "appendix_table", "src_line"])
        for name in sorted(table):
            r = table[name]
            w.writerow([name, f"{r['dw2013']:.3f}",
                        "" if r["ui_lo"] is None else f"{r['ui_lo']:.3f}",
                        "" if r["ui_hi"] is None else f"{r['ui_hi']:.3f}",
                        r["table"], r["line"]])

    json.dump({"source": CITATION, "url": URL, "action": action, "pdf_bytes": os.path.getsize(PDF),
               "pdf_sha256": sha, "pdf_sha_pin": PDF_SHA_PIN, "sha_matches_pin": True,
               "n_states_parsed": len(table), "anchors_verified": len(ANCHORS),
               "retrieved": RETRIEVED}, open(LOG, "w"), indent=2)

    print(f"  source PDF: {action}  {os.path.getsize(PDF):,} B  sha {sha[:12]}  [pin OK]")
    print(f"  parsed {len(table)} GBD health states (GBD 2013 estimate column)")
    print(f"  anchor self-checks: {len(ANCHORS)}/{len(ANCHORS)} reproduce the GBD2013 column")
    for k in ANCHORS:
        print(f"    {k:52s} dw2013 = {table[k]['dw2013']:.3f}  "
              f"(UI {table[k]['ui_lo']}-{table[k]['ui_hi']})")
    print(f"  -> {os.path.relpath(OUT_J, ROOT)}  +  {os.path.relpath(OUT_C, ROOT)}")


if __name__ == "__main__":
    main()
