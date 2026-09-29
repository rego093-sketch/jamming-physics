# Chemistry legacy package v1.0 (2026-06-14): the code behind §1–§6

**Source.** The author uploaded `VP_Chemistry_EM_DOI_Package_v1.zip` on 2026-09-29. Its reserved DOI is 10.5281/zenodo.20680541, and it is vendored here unchanged.

## Checks run on 2026-09-29 (Python 3.11)

| Check | Result |
|---|---|
| `SHA256SUMS.txt` | 79/79 files match |
| `core/code/verify_chemistry.py --root .` | PASS: runs 39/39, deterministic 39/39, standard library only, case ledgers 114 + 62 rows |
| `core/code/gate_numeric_chem.py` | PASS: every number shown in the chapters matches its module; no drift |
| `apps/verify_applications.py` | ALL PASS: 9/9 modules, 46 ledger rows, no external dependencies |
| Numbers on the current site pages §1–§6 compared with this package's paper + code | All present except two (`2.2` in §3, `4.7` in §6). The site text descends from this package. |

## Coverage
This package supplies **36 of the 37** chemistry scripts that the site cites but that were missing from the repo. The one still absent is `vp_open_items_reexam.py`.

## What changed after v1.0
Several items are newer than this package and do not come from it:
- the §7 waste-heat bundle (`repro/chemistry/repro/chemistry/07-*`);
- the 2026-09-28/29 page notes;
- experiments BC1–BC4 and ESS1–ESS2 (`repro/chemistry/experiments/`).

Where a page note revises a v1.0 claim, the page note governs. One example: the black copper coating is CuO, not Cu metal. This code stays exactly as it was published.

## Run
```
cd VP_Chemistry_EM_DOI_Package_v1/core && python3 code/verify_chemistry.py --root .
cd ../apps && python3 verify_applications.py
```
