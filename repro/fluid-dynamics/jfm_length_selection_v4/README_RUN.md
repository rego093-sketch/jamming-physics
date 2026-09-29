# JFM v4 Repro Skeleton

Drop these files into the **top-level of `JFM_DOI_FULLSTORY_v4`** (same folder as `requirements.txt` and `JFM_DOI_FULLSTORY_v3.zip`).

## 1) Local run (no Docker)

```bash
# From the v4 root:
export PYTHONPATH=code
make         # or: bash scripts/run_all.sh
```

This will:
1. Unpack `JFM_DOI_FULLSTORY_v3.zip` to `./v3` (once).
2. Regenerate the tiny DNS demo suite (`scripts/run_dns_suite.py`).
3. Analyze the demo suite into `data/dns_runs/dns_suite_with_Sb.csv` and `slope.txt`.
4. Run an assertion on the synthetic ground-truth dataset from v3 (targets slope 0.5 ± 0.02).

## 2) Dockerized run

```bash
# Build image from the v4 root that includes these skeleton files
docker build -t jfm-v4 .

# Run the pipeline
docker run --rm -it jfm-v4
```

## Notes

- If you want a single entrypoint, the container's default CMD already runs `scripts/run_all.sh`.
- The assertion targets the **synthetic** dataset shipped in v3 (`source_data/Synthetic_k6*.csv`) and does **not** assert anything on the toy v4 DNS demo slope.
- For full-paper one-click regeneration (all tables/figures), extend this skeleton with a script that reads `v3/source_data/*` and recreates every item in `v3/tables/*` and `figs/*`, then wire it into `run_all.sh`.
