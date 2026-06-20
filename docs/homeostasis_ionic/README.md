# docs/ — CANONICAL HTML (built only after research gates are green)

Per VP-SPEC v1.8 the canonical artifact is per-title HTML here (one <slug>/index.html per section, answer-first, JSON-LD, English body). Concept DOI: **10.5281/zenodo.20755910** (embedded in JSON-LD identifier/sameAs, claim-strip, footer, llms.txt), with a cross-volume citation to the non-opioid analgesic volume (DOI 10.5281/zenodo.20733420). Built: hub + **16 section pages** + sitemap.xml + robots.txt + llms.txt. Rebuild with `python tools/build_docs.py` after the research gate is green (`PHASE=writing`).
