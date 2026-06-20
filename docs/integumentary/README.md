# docs/ — CANONICAL HTML (built; research gates green)

Per VP-SPEC v1.8 the canonical artifact is per-title HTML here. This site is **built** (research signed
off, PHASE=writing, gates all-green). Open `docs/index.html` (the hub); each section is one
`<slug>/index.html` with an answer-first paragraph, JSON-LD (ScholarlyArticle + BreadcrumbList),
canonical link, claim-strip, and vp-cards. English body, honest grades, every `[O]` carrying an obstacle.

Sections: 01 emergence · 02 barrier/TEWL (T1) · 03 wound healing — jamming/unjamming (T2, flagship) ·
04 melanin photoprotection (T3) · 05 turnover dwell-cascade (T4) · 06 thermoregulation interface flux
(T5) · 07 UV carcinogenesis dose-response (oncology) · 08 methods, grades & reproducibility ·
09 pathology (13 diseases) · 10 hair-follicle cycle — anagen/telogen (T6) · 11 sebaceous-duct jamming —
acne/HS (T7) · 12 cell-adhesion blistering — pemphigus/pemphigoid (T8) · 13 neurovascular reactivity —
rosacea/Raynaud (T9).

Sidecars: `sitemap.xml`, `robots.txt`, `llms.txt`, `_meta.json`, `assets/css/site.css`.

Every number is pulled live from the engine (C1). Rebuild deterministically with:

    python tools/build_docs.py          # refuses unless gates are green and PHASE=writing

Result SHA-256: 1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92
