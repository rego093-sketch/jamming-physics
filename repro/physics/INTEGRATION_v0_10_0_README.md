# v0.10.0 integration — what changed and how to verify

This bundle is the v0.9.3 physics whitepaper with the **Time & Gravity** sector integrated as a
featured chapter §18 (time and gravity kept as two separate tracks, connected by the river identity).

## Changed/added (source of truth = txt/ + manifest/)
- NEW  txt/18-time-and-gravity.txt                  (featured chapter; eq phy-18-000..014)
- EDIT manifest/physics.csv                          (+1 row: §18, featured)
- EDIT manifest/physics.eq_list.tsv                  (+15 rows: phy-18-000..014, base64 TeX)
- EDIT txt/w0-result-scorecard-one-page-summary.txt  (+ "Time & Gravity (featured)" block + scope note)
- EDIT txt/17-extensions-optional-reading.txt        (+ 1 PROMOTION NOTE block under §17.4; NO derivation/number changed — verified)
- EDIT txt/14-force-lattice-tension-1-r2.txt         (+ 1 cross-ref clause on the §14.0.6 'exact v/c scaling' status bullet)
- NEW  tools/vp_timegravity_ssot.py, vp_inflow_competition.py, vp_exact_sqrt.py, vp_cap_depart.py
- NEW  reports/time_gravity.gate.json + four *_LEDGER.csv
- NEW  CHANGELOG_v0_10_0.md

## Integrity
- §17.4 derivations and ALL numbers preserved verbatim (diff beyond the stub = none).
- No free parameter added; No-Tuning preserved (no coefficient migrated).
- All gates re-run PASS; modules deterministic (2x sha256 identical), standard-library only.

## To render the site
docs/ HTML is a build artifact (as the original docs/ were). Regenerate via the existing pipeline
(split.py / render_eq.js / build_hub.py) so §18 appears in docs/physics/. The SSOT (txt/ + manifest/)
is complete; only the HTML rebuild remains.

## Reproduce (5 lines)
cd tools && python3 vp_exact_sqrt.py && python3 vp_timegravity_ssot.py && \
  python3 vp_inflow_competition.py && python3 vp_cap_depart.py && \
  python3 vp_timegravity_ssot.py --check ../txt/18-time-and-gravity.txt
