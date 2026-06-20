# REPRODUCE

```
python repro/run_all.py               # research entry: emerge, circulate, stress + oncology, gate report
python repro/_engine/vp_*_engine.py   # emergence JSON (+ sha256)
python repro/_verify/gates.py         # research gate + writing-lock status
python repro/_dynamics/emergent_lineage.py    # T6: emergent developmental order (shared-drive race, sim)
python repro/_oncology/emergent_kramers.py    # T7: emergent carcinogen dose-response (barrier-crossing, sim)
python repro/_dynamics/emergent_memory.py     # T8: emergent immune-memory lifetime (ON->OFF escape, sim)
python repro/_dynamics/emergent_chronicity.py # T9: emergent acute/chronic boundary (amplitude x duration, sim)
python repro/_oncology/emergent_seam.py       # T10: emergent surveillance seam (coupled influx-clearance, sim)
python repro/_dynamics/emergent_selection.py  # T11: emergent clonal-selection threshold (rising-affinity ramp, sim)
python repro/_dynamics/emergent_competition.py# T12: emergent immunodominance (coupled shared-antigen competition, sim)
python repro/_therapy/emergent_therapy.py     # T13: emergent therapy trajectories Levers A&C (basin occupancy, sim)
python repro/_therapy/emergent_barrier_restoration.py    # T14: emergent Lever B barrier restoration (crossing-rate vs restored barrier, sim)
python repro/_therapy/emergent_surveillance_clearance.py # T15: emergent Lever D surveillance clearance (time-domain reservoir decay, sim)
python repro/_dynamics/emergent_repertoire.py # T16: emergent N-clone repertoire dominance (coupled shared-pool competition, sim)
python repro/_oncology/emergent_regrowth.py   # T17: emergent cytotoxic relapse regrowth (basin-gated population layer, sim)
python inherited/ncbi_verify.py       # γ primary-source provenance (offline gate, no network)
python -c "import sys;sys.path.insert(0,'inherited');import ncbi_verify as V;print(V.ONLINE_reverify())"  # live NCBI re-audit
```

EMERGENT SIMULATIONS (v0.4.0): T6/T7 replace two previously-assumed forms with results measured directly
from stochastic R19 simulations. T6 (`emergent_lineage.py`) drives four switches with one rising field and
MEASURES the commit order — the spinodal/γ order emerges, commit-h spacing = spinodal spacing; the
spleen↔thymus middle pair is a weak emergent bias [O], quantified (washes out under noise). T7
(`emergent_kramers.py`) integrates the overdamped Langevin R19 field and COUNTS barrier crossings — the
convex super-linear dose-response and the Kramers exponential law both emerge (log-rate∝barrier, R²≈0.98).
Both are deterministic (fixed seed=19, np.random.default_rng) and live in the stress battery, so the
`circulate()` sha is byte-identical to v0.2.0/v0.3.0 (emergent results are additive, not a re-fit).

EMERGENT SIMULATIONS (v0.5.0): T8/T9/T10 promote the last three still-analytic dynamical claims. T8
(`emergent_memory.py`) measures the ON→OFF escape lifetime (ranks ascending γ; Kramers escape law,
R²≈0.998). T9 (`emergent_chronicity.py`) measures the chronicity boundary in the (amplitude × duration)
plane (critical amplitude = spinodal organ-by-organ; monotone dose×time tradeoff). T10 (`emergent_seam.py`)
measures the surveillance seam from a coupled influx–clearance model (site-independent 1/(1−escape) common
multiplier). All remain in the stress battery; the `circulate()` sha is unchanged.

EMERGENT SIMULATIONS (v0.6.0): T11/T12/T13 complete the programme. T11 (`emergent_selection.py`) measures
the clonal-selection commit-drive from a rising-affinity ramp (commit-drive = spinodal organ-by-organ, from
below by thermal activation; orders by γ; tolerance/commitment bracket). T12 (`emergent_competition.py`)
measures immunodominance from a coupled shared-antigen competition (winner-take-all: a subdominant clone that
commits with P≈1 alone is competitively excluded; monotone in the affinity gap; symmetric at zero gap). T13
(`emergent_therapy.py`) measures therapy Levers A & C as stochastic basin-occupancy trajectories (re-flip
threshold = spinodal, non-cytotoxic; drive removal preventive-not-curative; differentiation empties the basin
while drive-removal/cytotoxic leaves it occupied = relapse). All remain in the stress battery; the
`circulate()` sha stays byte-identical (`e7a2a5b8…`). With T1–T13 every dynamical mechanism is emergent; the
remaining [O] items are absolute scales only (noise scale D, hierarchy depth, clinical dose/schedule).

EMERGENT SIMULATIONS (v0.7.0): T14/T15/T16/T17 finish FUTURE_WORK §A″ — the last two therapy levers become
measured trajectories and two richer multi-body/temporal results are added. T14
(`emergent_barrier_restoration.py`) steps the carcinogen-eroded barrier back up and COUNTS crossings: the rate
collapses (≈7.9× at full restoration) and log-rate is linear in the restored barrier (R²≈0.99, slope recovers
−1/D) — the Kramers collapse measured in the therapeutic direction (the twin of T7). T15
(`emergent_surveillance_clearance.py`) measures the reservoir N(t) decaying as surveillance is restored — the
floor falls as 1/(1−escape) (the T10 seam recovered as a trajectory endpoint, site-independent when rescaled by
influx) and clears faster with deeper surveillance (the time-domain twin of T10). T16 (`emergent_repertoire.py`)
generalises T12 to N clones and measures the dominance concentration (participation ratio N_eff ≪ N; sharpens
with affinity spread and, relative to N, with repertoire size; symmetric at zero spread). T17
(`emergent_regrowth.py`) makes relapse explicit as a basin-gated regrowth curve (cytotoxic → ≥90% K regrowth =
relapse; differentiation → ≈0 = cure; a deeper kill only lengthens the delay while every depth fully recovers,
so relapse is basin-determined). All remain in the stress battery; the `circulate()` sha stays byte-identical
(`e7a2a5b8…`). With T1–T17 all four therapy levers (A/B/C/D) are measured trajectories and relapse is an
explicit measured curve; the remaining [O] items are absolute scales only.

γ PROVENANCE (v0.3.0): the four master-gene promoter windows (TSS−2000..+500) are byte-exact verified
against the live NCBI reference assembly GRCh38.p14 (sha256), γ recomputed identical; gene→organ master +
chromosome corroborated by NCBI-Gene RefSeq. Frozen proof in inherited/ncbi_verification.json +
inherited/ncbi_gene_refseq.json; OFFLINE_check() is deterministic (in the research gate), ONLINE_reverify()
re-audits against live NCBI. The core circulate() sha is byte-identical to v0.2.0 — verification is an added
layer, not a re-fit.

Determinism (VP-SPEC C1): BLAS pinned single-thread before numpy; fixed seed; round-before-hash; sorted
JSON keys. Two engine runs yield an identical sha256. No hand-entered numbers. stdlib + numpy only.
