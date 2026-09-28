# Definitive V3 consistency notes

This is a consistency addendum for `04_vp_whitepaper/data/chem/traceability_spec_v3.txt`.
It does **not** change the locked Step7 external-inspection dataset; it only clarifies how to read the V3 derivation inside the DOI bundle.

## 1) CH4 Rule B: "exact match" is obtained in the leading-order geometry form

Using the V3 constants:

- \(\Phi_{geo}=\pi/(3\sqrt{2})\approx 0.74048049\)
- \(\Delta_{ov}=0.0132\)

the **leading-order** tetrahedral relation gives

\[
P_{idx}^{(lead)}(CH_4)=\Phi_{geo}(1-\Delta_{ov})\approx 0.730706\;\Rightarrow\;0.7307
\]

This matches the Step7 dataset value `P_IDX=0.7307` for `CH4`.

### About the full form with \(P_{avg}\)

The V3 spec also writes a fuller expression:

\[
P_{idx}(Molecule)=P_{avg}(Stoichiometry)\,\Phi_{geo}(1-\Delta_{ov})
\]

For CH4, if \(P_{avg}\) is computed explicitly from \(Z/r^2\) averaging using \(r_{cov}(H)=31\,pm\) and \(r_{cov}(C)=77\,pm\), then

- \(P_{avg}(CH_4)\approx 0.99450\)
- \(P_{idx}^{(full)}(CH_4)\approx 0.72669\)

This is within the DOI’s stated \(\pm 5\%\) amplitude tolerance, but it is **not** numerically identical to 0.7307.

**Interpretation inside the DOI bundle:** for CH4, \(P_{avg}\approx 1\) is treated as a near-unity correction and the "attack-proof" derivation uses the leading-order relation to isolate the geometry+overlap origin of 0.7307.

## 2) Constant K and the r_vac anchor

The V3 spec defines

- \(K=1000\,\alpha_{em}\) with \(\alpha_{em}\approx 1/137.035999\)
- \(\Beta_{vac}=1.088\)

Using \(r_{cov}(H)=31\,pm\), the implied vacuum amplitude is

\[
r_{vac}^{(pred)} = r_{cov}(H)\,K\,\Beta_{vac} \approx 246.125\,fm
\]

The Step7 lock uses \(r_{vac}=245.9\,fm\) (difference \(\approx 0.09\%\)).

If one insists on exact equality to the lock value using the same \(\alpha\), the corresponding \(\Beta_{vac}\) would be \(\approx 1.0870\).

## 3) Machine-readable seed

A small machine-readable seed table is provided at:

- `04_vp_whitepaper/data/chem/traceability/traceability_table_v3_seed.csv`

It records the CH4 leading-order check and the K-based scaling check.
