# stress_gamma_vs_gc — sharpening "γ is a GC-restatement" (T2.1)

**Verifies:** whether the part of γ NOT explained by GC is noise or the CpG/methylation fingerprint.
**Method:** per 2 kb window of the 12 frozen §11 regions, isolate the dinucleotide-order term by
permutation: `d_gamma = γ_obs − γ(permuted window)` (permutation fixes composition/GC exactly, randomizes
dinucleotides to iid). Then test (1) within-genome corr(γ,GC), (2) corr(d_gamma, CpG O/E) raw + partial|GC,
(3) the stiff-CG mechanism. Locked γ and CpG O/E imported single-source + sha256-pinned. seed=19.
**Expected output:** `stress_gamma_vs_gc_results.json` (deterministic, 2× sha256 identical).

**Finding (REFINED, not rejected):** γ adds no independent axis (99% GC; within-genome corr 0.993), BUT the
1% residual is structured — pooled corr(d_gamma, CpG O/E)=0.572, partial|GC=0.572, mechanism corr(d_gamma,
CG-step excess)=0.576. This *quantifies* §11's qualitative "two projections of one history." Boundary:
*Plasmodium* (GC≈20%) inverts — residual driven by TA-step structure, not CpG (the mapping is clade/GC-dependent).
