# C3E1: directed ejection from a three-sphere (C3) cluster, as a dynamical 3-D test

**Claim tested (author):** "In a 3-D structure, when energy concentrates, the three spheres (the C3 triangle) push the energy out to ONE side. In physics there is no outlet, so it is annihilated. The 82 (= 81 + 1) structure carries over into fluids."

**Why this test exists:** reviewers noted that the existing support is true by construction and involves no dynamics. That support is graph 2-coloring in fluid §11 `corotation.py`, Gauss closure in `rigid_shell.py`, and the "single C3 nozzle" in physics §8.0.

**Outcome in one line:** under the pre-registered rules the claim **FAILS**. In this model the co-rotating C3 triangle does not eject to one side. Almost all of the injected energy is dissipated at the frustrated contacts themselves, so the energy is "annihilated" before it can be ejected. The only strongly one-sided ejectors are the counter-rotating, gear-meshed arrangements, and the counter-rotating *pair* (the bipartite control) is the strongest of them.

## Files
- `PREREG.json`: predictions, fixed parameters and decision rule. Written **before** any physics run.
- `c3e1_run.py`: the model and all runs. About 12 min on 4 cores; numpy + scipy; `SEED = 19`; deterministic. Running it twice gave the same numbers.
- `c3e1_run.out.txt`: console log. `RESULT.json`: all numbers, per run and per site.

## Model (everything put in by hand is listed here)
- **3-D DEM of soft frictional spheres**, with translational and rotational degrees of freedom. The lattice itself is simulated; there is no continuum closure. Units are d = m = k_n = 1. The contact force is a harmonic normal spring plus a normal dashpot (γ_n = 0.05). The tangential force is viscous-Coulomb (γ_t = 0.5, capped at μF_n with μ = 0.5). There is **no tangential spring**. Integration uses velocity Verlet with dt = 0.02.
- **Media:**
  - (A) A perfect FCC crystal of 6912 spheres with 2 % overlap. Its (111) triangle has C3v site symmetry: a tetrahedral cap sphere on one side and an octahedral hole on the other.
  - (B) Random jammed packings (the framework's vacuum): N = 4000, φ = 0.66, FIRE-minimised to |F| < 1e-10, z ≈ 7.2. There are 2 packings × 6 triangle sites.
  - (C) A simple-cubic crystal (16³) holding the **81-core**, the sites with x²+y²+z² ≤ 6. The code confirms that the R² = 7 shell is empty.
- **Injection:** spin only, |ω|·d/2 = 0.2 on the cluster spheres, with the medium at rest. The whole domain is a periodic box, so it is closed and has no outlet.
- **Observable:** energy flux across a sphere of radius R_s = 3 (also 4.5) around the cluster. It is counted contact by contact as ½(P_on_j − P_on_i), with P = F·v + τ·ω, and integrated over t ≤ 10. From it the run computes the dipole D, the quadrupole q, the 60° lobe fraction and the bipolarity. In medium B the dipole vector is also averaged in the cluster frame, so that the disorder contribution cancels.

## Grades
- **[F] symmetry identities** (these are theorems, not results):
  - A C3-co-rotating triangle in a mirror-symmetric environment has D = 0 exactly (C3 + σ_h).
  - In FCC the only allowed dipole lies along [111], and only because the lattice's cap/hole asymmetry permits it.
  - The 81-core co-rotating about z has C4h symmetry, so D = 0 exactly.
  - A closed box conserves momentum.
  - All four are confirmed numerically to between 1e-13 and 1e-15.
  - Consequence: a single lobe from T+++ can only come from the environment or from spontaneous symmetry breaking. The three-body geometry cannot supply it on its own.
- **[V mech] in-model dynamics:** everything below. These results hold for this contact law only.

## Results (R_s = 3)
| test | numbers | verdict |
|---|---|---|
| P1 T+++ one lobe (RCP) | D_sys = 0.118 (1σ noise floor 0.133); f_lobe 0.437; bipolarity 0.72 | **FAIL** |
| P2 controls not directed and T+++ ≥ 2× controls (RCP) | D_sys: P++ 0.30, P+- 0.20, S 0.55 (all within about 1–2σ of noise); T+++ is not larger | **FAIL** |
| P3 T+++ one lobe along [111] (FCC) | D = 0.0058, along [111] as symmetry requires. Post-hoc D_gross = 0.0006. S and P++ have D = 0 (symmetry sanity check passes) | **FAIL** |
| P4 T+-+ (one frustrated contact) more directed than T+++ | 0.195 > 0.118 in RCP (formal pass, but within noise). In FCC, clearly: D_gross 0.25 vs 0.0006 | PASS (formal; see note) |
| P5 closed box (FCC, t = 200) | momentum 3.8e-15 ✓; late KE dipole 0.008 ✓; 99.9 % dissipated ✓; energy-balance bookkeeping error 1.37e-3 against a threshold of 1e-3 ✗ | **FAIL** (balance sub-criterion only) |
| P6 81-core spontaneous single lobe | D = 5.6e-6 at ε = 1e-6 and 5.6e-4 at ε = 1e-4, so D is exactly proportional to ε: no amplification | **FAIL** |

**Post-hoc diagnostic (not pre-registered).** It was added after the first run showed that the net flux is close to zero, which makes the pre-registered D ill-conditioned. Normalising by the gross |flux| instead:
- By t = 10, **96.6–99.7 % of the injected energy is already dissipated at the cluster's own contacts**. Only 2.6–4.6 % (RCP) or 0.3–1 % (FCC) of E0 ever crosses R_s.
- In RCP the per-run anisotropy D_gross is about 0.08–0.11 for *every* configuration, and the systematic part is ≤ 0.05. The anisotropy comes from medium disorder, not from the cluster.
- In the clean FCC medium the one-sided ejectors are:
  - P+- (counter-rotating pair): D_gross = 0.40, directed perpendicular to the bond.
  - T+-+: D_gross = 0.25, directed along the frustrated edge rather than toward it.
  - Both follow the "gear-pump" direction of the meshed (counter-rotating) contacts.
- In the SC lattice the co-rotating 81-core lets only 7 % of E0 out, against 37 % for the checkerboard (bipartite) core. Frustrated co-rotation **dissipates internally**; it does not eject.

## What the logic suggests (instead of forcing a pass)
1. **"Annihilated" is supported, but for a different reason.** Co-rotating neighbours slide against each other at every contact, which is exactly what "frustration" means here. With a dissipative contact law that sliding converts the spin to heat locally. So the energy is annihilated *at the triangle*, not after being ejected to one side. The closed box adds nothing beyond conservation. Note that the dissipation is put in by hand (γ_t, μ).
2. **One-sidedness needs a broken mirror plus meshing, not three-body frustration.** The symmetry identities [F] forbid a lobe from the C3-symmetric co-rotating core. Dynamically, the directed flux comes from counter-rotating, gear-meshed pairs, which act as a pump. This is the particle analogue of the known fact that a counter-rotating vortex pair self-propels, while a co-rotating pair does not (fluid §4). The "+1 nozzle" reading, in which the frustrated contact is the outlet, is not what the dynamics shows: the T+-+ flux runs along the frustrated edge, driven by the two meshed contacts.
3. **Next test, not run here:** replace the viscous tangential law with a conservative Cundall–Strack tangential spring (a Cosserat solid), so that spin can radiate as rotational/shear waves instead of turning into heat. Pre-register again whether T+++ then produces a [111] lobe in FCC and a systematic lobe in RCP. On the evidence here and the symmetry identities, a C3-symmetric co-rotating core should not produce one unless the environment picks the side.

## Honesty notes
- Before the run, only a timing and correctness smoke test was made: 50 steps of a single spinning sphere, plus one FIRE packing timing. No outcome was examined.
- The pre-registered D was computed exactly as registered. Its NaN and >1 values come from a net flux that is close to zero or negative. They are reported as they are, and the gross-normalised numbers are clearly labelled post-hoc.
- Nothing was re-tuned.
- `docs/` was not edited.
