# Release 2026-09-29: new Zenodo versions for all 32 volumes

All 32 volumes changed since their published versions: every content hash differs from `registry/integrated_versions.lock.csv`. For each record, use Zenodo's **New version** and replace the files. The concept DOI stays the same and resolves to the newest version, so the site needs no DOI change.

| File | Use |
|---|---|
| `PRIORITY.md` | The order to publish in, with the reason for each volume. |
| `descriptions/<id>.md` | The new description (English). |
| `descriptions_html/<id>.html` | The same text as HTML, to paste into Zenodo's description box. |
| `TITLES.md` | Titles stay unchanged on Zenodo. The hub titles listed there are for reference only. |
| `zips/<id>_2026-09-29.zip` | The file to upload. disease_wp has three files: the main ZIP plus `_rawdata1.zip` and `_rawdata2.zip` (its raw source data). Upload all three to the same record; the main ZIP's MANIFEST.sha256 lists every file of all three. Not committed; rebuild with `python3 tools/build_release.py 2026-09-29`. |
| `pdfs/<id>_2026-09-29.pdf` | One PDF per volume: every page of the volume in reading order, one bookmark per page. Upload it next to the ZIP in the same record so Zenodo shows a preview. disease_kit (871 pages) is printed at low quality: plain two-column text without the site styling. Not committed; rebuild with `python3 tools/build_pdfs.py 2026-09-29`. |
| `CHECKSUMS.txt` | SHA-256 of each ZIP, to check the upload. The build is deterministic. |
| `priority/<id>.json` | Severity record behind PRIORITY.md. |

Each ZIP contains:
- `docs/<id>/` — the published pages;
- `repro/<id>/` — code and data;
- `DESCRIPTION.md` and `DESCRIPTION.html`;
- `LEDGER.json` — this volume's claims-ledger rows;
- `CORPUS_GUIDE.md` — AGENTS.md;
- `MANIFEST.sha256` — a checksum for every file.

Suggested version field: `2026-09-29`.
