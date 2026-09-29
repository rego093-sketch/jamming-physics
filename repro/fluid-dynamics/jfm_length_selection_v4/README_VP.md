# JFM length-selection package (v4) — vendored for reference

**What it is.** This is an unpublished manuscript package by the author, supplied on 2026-09-29. The author does not intend to submit it. It concerns **length selection** under a spectrally rotating forcing: the selected length L\* and its scaling with a control observable S_b. Fluid-dynamics Pillar III (§8) and the β ≈ 0.5 selection exponent rest on this work.

**Contents.**
- `JFM_DOI_FULLSTORY_v3.zip` is the original v3 archive. It holds the tables, the source data, and the synthetic ground-truth set `source_data/Synthetic_k6*.csv`.
- `code/dns2d.py`, `scripts/` and `data/dns_runs/` add a small 2-D Navier–Stokes DNS demo suite: 5 runs at N = 64.

**What the checks actually test.** The two checks behave differently:
- `scripts/assert_reproduction.py` asserts the slope 0.5 ± 0.02 on the **synthetic** v3 dataset, not on DNS. The package README says so.
- The shipped tiny DNS demo gives a slope of **0.000** (`data/dns_runs/slope.txt`). The package notes that it does not assert anything on that demo.

So β ≈ 0.5 is established on synthetic data. It has not been shown by the DNS. The volume's own nonlinear run gives β̂ = 0.464, and a finer re-run gives 0.424 (see `reviews/fluid-dynamics/2026-09-29_reviewer2_code_data.md`).

**Grade.** [V mech] on synthetic data. The DNS confirmation is data-pending: it needs a production-resolution suite of the rotating-forcing DNS with L\* measured.
