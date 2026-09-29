# Fluid-dynamics ("Configured Continuum") — Reviewer 1 of 3
## Lens: what exactly is claimed about Navier–Stokes, and does the derivation chain support it?

Date: 2026-09-29 · Scope read: hub, §01, §03, §04, §05, §06, §08, §09, §13, §14, ax-d, ax-o, ax-x (+ grep of all 39 pages), `_decl.json`, `seams.json`, manifest row, `repro/fluid-dynamics/IRREPRODUCIBILITY_LEDGER.md`, `WORDING_REVISION.md`, `ns3d.py`, `dissipation_avalanche.py`, `metriplectic_vortex.py`, drivers `dev64.py`/`embed96.py`. Also checked against the physics hub. Nothing under docs/ or repro/ was edited.

Code re-runs done for this review:
- `06-.../validate_all.py`: fails as shipped (`ModuleNotFoundError: metriplectic_vortex`). With `PYTHONPATH=../09-...` it reproduces all five PASS lines and the quoted numbers (dE=2.9e-8, dZ=5.4e-6, budget 4.4e-6).
- `ns3d.inviscid_energy_check()` (the shipped 3-D validation): **dE/E = 1.0e-8, max|k·û| = 4.1e-12**. The pages say ~1e-16 and ~1e-14 (see F-12).

---

## 0. Verdict up front

**The volume does not claim to have solved the Navier–Stokes equations. Its own text rules that out.** The author's summary ("solved the Navier–Stokes equations") is not supported by the pages, and §14 contradicts it directly. Here is what the pages actually claim, strongest wording first:

| # | NS-related claim | Where | Stated strength | What the chain supports |
|---|---|---|---|---|
| C1 | "The Navier–Stokes equations are **derived**, not overturned. They follow as the **exact** Newtonian closure of the arrangement" | §14 (`14-claims-non-claims-falsification`), echoed in §01 | unconditional, "exact" | **Conditional only.** The balance laws are the standard Irving–Kirkwood identity, which holds for any particle system. The Newtonian closure is a **[GATE]** in §6 and has not been passed (μ is never measured). |
| C2 | "Pillars I–IV then **derive its governing equations**" [DERIVE] | §01 answer badge | [DERIVE] | Same as C1: the NS step is a [GATE], not a [DERIVE]. |
| C3 | "Global regularity is **compressed to one gate**, not claimed. The configurational view **recasts the Millennium question** … rearrangement events supply a physical regularization valve … a single, sharply stated zero-width limit" | §14; §01 "recast, not yet proved" | explicit non-claim, framed as a reduction | **No reduction is shown.** No theorem links the "zero-width limit" to 3-D NS regularity. The "smooth at finite kernel width" point holds trivially and says nothing about NS (F-3). |
| C4 | Numerical solution of 2-D/3-D NS (pseudo-spectral) | §6, §9, ax-d, ax-o, ax-x | [DERIVE]/PASS | These are standard DNS solver checks plus NS phenomenology already known from the literature. They are **[V mech]** at most, and they contain nothing from the substrate. |
| C5 | Turbulence: anomaly as "channel migration"; events carry the flux; avalanche τ=1.46; Vassilicos C_ε; MDR | §9, §12, hub "passed external tests" | [DERIVE] "for the category" / "genuine prediction" | The saturation holds **by construction** (the page says so). In NS itself the event channel is identically zero. The DNS results are in-model tests of standard NS (F-6…F-10). |
| C6 | Transition class = directed percolation, "140-year problem lands where the substrate says" | §3 | [DERIVE] | Generic DP universality (Pomeau/Janssen–Grassberger). It is not specific to the substrate and not an NS result (F-11). |

So, at most, "solved NS" could mean (a) the conditional continuum derivation C1 or (b) running an NS solver (C4). Neither amounts to solving NS in the Clay sense or in any other strong sense. The Millennium question stays exactly where it was. The page calls it "recast", but the recast contains no mathematical content that bears on 3-D NS.

---

## 1. Findings

Severity scale: **H** = undermines a load-bearing claim or contradicts another page; **M** = gap, hidden assumption, or mis-grade; **L** = presentation or reproducibility hygiene.

### F-1 (H) — Pages state the NS derivation at different strengths; "exact" in §14 contradicts "conditional [GATE]" in §6
- §6 (`06-pillar-i-structural-arrangement-forces`): "The Newtonian closure is **conditional, not automatic** … [GATE] (G-Newton) … if and only if the arrangement's stress responds … by local, isotropic, Markovian linear response … The value of μ … is a gate item (it must be measured …)".
- §14: "The Navier–Stokes equations are derived, not overturned. They follow as the **exact Newtonian closure** of the arrangement (Pillar I)". Its answer badge is [DERIVE]: "We **establish** … all four pillar statements".
- §01 badge: "Pillars I–IV then **derive its governing equations** … [DERIVE]".
- Hub: "This whitepaper shows those facts to be **forced** — derived as necessary consequences".
- `WORDING_REVISION.md` records that the earlier, accurate hedges were deliberately removed ("We do not overturn … we derive them" → "derived, not overturned"; the clause "*reframing is not proving*" was deleted).
- **Why it matters:** only the balance laws (continuity plus momentum with an unclosed σ) are derived. NS itself needs the G-Newton gate, which has not been passed. Nowhere in the volume is μ measured from an arrangement (Green–Kubo or dissipation matching); §14's own "Open gates" list says so. "Exact Newtonian closure" is therefore false as written.
- **Fix:** replace it in §14 and §01 with "The continuum balance laws are exact identities of the arrangement [DERIVE]. Navier–Stokes follows *if* the Newtonian gate G-Newton passes [GATE; μ not yet measured]." Restore "reframing is not proving".

### F-2 (H) — "Exactly two gates" is a miscount; the NS derivation itself sits behind a third, still-open gate
- §14 badge: "the **entire residual** is compressed to **two** named gates — global regularity and the infinite-Re flux mechanism". The regularity item says "named as the **lone** open [GATE]". §01: "**exactly two gates** remain".
- The same §14, under "Open gates", also lists: G-SOC (exact marginality under drive), the finite-rate viscosity divergence, the **Newtonian-closure gate of Pillar I**, and the G-S dimensional anchoring. `IRREPRODUCIBILITY_LEDGER.md` §2 concedes these as "finer sub-gates".
- **Why it matters:** the Newtonian-closure gate is a precondition for C1. Leaving it out of the headline count hides the one gate that governs whether NS is derived at all.
- **Fix:** give the true count (at least five: G-Newton, G-SOC, viscosity rate, G-S, flux asymptotic) plus regularity as a non-claim. Drop "entire residual" and "lone".

### F-3 (H) — The Millennium "recast" contains no reduction; the stated "zero-width limit" is the wrong limit
- §14: "coarse-grained fields are smooth at finite kernel width, and rearrangement events supply a physical regularization valve the field formulation lacks. What remains is a single, sharply stated zero-width limit".
- Why this does not bear on the Clay problem:
  1. With a smooth kernel W_ℓ and finitely many particles, ρ and ρu are smooth **by definition**, whatever the dynamics. These fields satisfy the unclosed balance laws, not NS, so their smoothness says nothing about NS solutions.
  2. The Clay problem concerns the NS PDE at **fixed ν>0** with smooth data on ℝ³/𝕋³. The volume states no theorem that the "zero-width limit" of the particle system converges to NS, let alone one that transfers regularity or blow-up in either direction.
  3. As ℓ→0 at a fixed configuration, the fields tend to sums of delta masses, not to NS fields. A hydrodynamic limit needs particle spacing a→0 **with ℓ/a→∞** (scale separation). As worded, the "zero-width limit" is ill-posed.
  4. The "regularization valve" (events) does not exist in NS: by the volume's own §6 identity dE/dt = −2νZ, NS has no event channel (see F-6). A regular particle model does not regularize the PDE.
  5. §4 lists "non-blowup of the jump dynamics" and "Γ-convergence to the continuum" as proved theorems (see F-5), but no proof appears in the volume. Even if proved, non-blowup of a particle model says nothing about NS, and Γ-convergence of energies does not give convergence of dynamics.
- **Fix:** state plainly: "This volume proves nothing about 3-D NS global regularity. We only note that the particle model is regular at finite ℓ; no limit theorem connecting it to NS is given [O]." Remove "compressed to one gate" and "recasts the Millennium question", or supply the missing limit theorem.

### F-4 (H) — Pillar I's derivation does not cover the interaction §4 says is mandatory (three-body, spinning cores), so the chain breaks at the axioms→equations step
- §6 derives the stress **only for pair forces**: "since F_ij = −F_ji, pairing terms … Irving–Kirkwood identity". The step's stated inputs are "mass, it moves, and it pushes on itself".
- §4 says pairs are "provably unable to reproduce elementary fluid behaviour" and that the minimal interaction is the three-body U₃. Cores also carry spin L_i and torques.
- **Why it matters:**
  - (a) A three-body potential needs the many-body Irving–Kirkwood generalization (e.g. Admal–Tadmor), which the volume neither states nor derives.
  - (b) Cores with intrinsic spin and torques produce an **antisymmetric stress and couple stress**, so the coarse-grained continuum is **micropolar (Cosserat)**, not Navier–Stokes. NS needs a symmetric stress, which only holds if spin relaxes fast. That is a hidden assumption, stated nowhere.
  - (c) §13 claims "four layers … each determines the next: substrate → axioms → Π/RG → pillars". Yet Pillar I uses none of §4, and the NS solvers use none of §3–§5.
  - (d) The §4 table maps "Γ-convergence (a→0) core lattice → continuum energy" to "Pillar I (continuum limit)". Pillar I contains no a→0 limit.
- **Fix:** either extend the §6 identity to U₂+U₃ with spin (derive the antisymmetric/couple stress and state the spin-relaxation condition as part of G-Newton), or declare that Pillar I holds for generic pair-force media and is independent of §4. Remove "each determines the next".

### F-5 (H) — The two-body No-Go is an artifact of assuming second-order Newtonian dynamics; the "forced" three-body core does not follow
- §4: "a two-body interaction is **provably insufficient** … a co-rotating pair cannot self-propel … Yet a real 2D vortex dipole does self-propel".
- **Why it's wrong:**
  - Point vortices obey **first-order** Kirchhoff dynamics: x and y are canonically conjugate, and velocity is the Biot–Savart field. Their Hamiltonian H = −Σ Γ_iΓ_j ln r_ij /4π is purely **two-body**, and it does make an opposite-sign dipole translate at Γ/2πd. The No-Go holds only for m ẍ = −∇U with central forces, a dynamics the page imposes without comment. So "provably insufficient" is conditional on a modelling choice.
  - The page's own example conflates two cases. A **co-rotating** pair does not self-propel in a real fluid either; it orbits.
  - The U₃ "repair" test (`axioms.py`) measures a transverse force on the (0,1) sub-pair only. U₃ is translation-invariant, so ΣF = 0 over all three bodies and the isolated triangle's centre of mass still cannot self-propel. The test does not show that self-propulsion is restored.
  - U₃ = D·L·(r×r) is linear in the spin and **odd under time reversal**. This T-breaking in the "conservative Hamiltonian core" is undeclared: §4 lists translation, rotation, exchange and parity invariance, but not T.
  - "They collapse to derivatives of a single source function F(r)" is asserted without derivation.
- §4 also claims a suite of **proved** theorems ("uniqueness of the kernel, the No-Go, … non-blowup of the jump dynamics, an H-theorem, … Γ-convergence to the continuum, and a large-deviation principle"), but the volume contains no proofs or references. ax-x even says "merged here without external citation, by design".
- **Fix:** restate the No-Go as conditional on Newtonian point-particle dynamics and acknowledge the Kirchhoff two-body counterexample. Grade the triangle as a modelling choice ([H]/[L]), not a forced result. Either ship the theorem proofs or downgrade them to [O] with each obstacle stated.

### F-6 (H) — Pillar IV's "channel migration" contradicts NS; the saturation is an input
- §9: "The saturation is **not an assumption**; it follows from the structure". The same section later says: "The plateau equals the injection rate I **by construction**". §13 adds: "Pillar IV's plateau equals the injection rate I by construction".
- In `metriplectic_vortex.py`, dE/dt = I − aνE − bE with a ν-independent b>0. Then ε_bind → I as ν→0 is algebra (`validate_all.py` [4], [5] PASS). The anomaly is **assumed** through b>0 being independent of ν. That is circular.
- **Contradiction with NS:**
  - The toy model sets ε_ν = aνE → 0.
  - In NS, the volume's own exact identity (§6, eq. budget) is ε = 2νZ, and **all** dissipation is viscous. The dissipation anomaly means νZ stays finite as ν→0 (Taylor's zeroth law, which §9 itself reproduces as the C_ε plateau).
  - So in NS ε_ν does **not** go to zero, and ε_events ≡ 0 identically.
  - The 2-D/3-D DNS "events" are just regions of high **viscous** dissipation: high strain or high vorticity gradient.
  - The "migration from the smooth channel into the event channel" therefore does not happen in NS. It holds only in a reduced model that is not NS.
- **Fix:** grade the budget as bookkeeping and the saturation as "[L]: assumed ν-independent event rate b". State that in NS the event channel is identified with the high-dissipation *part* of ε_ν, not with a separate sink. Rewrite "not an assumption" accordingly.

### F-7 (H) — "From Navier–Stokes to the selection normal form" has a sign error, and the selected k is set by the forcing
- §8: "Physically the **viscous and drag channels supply the binding (k²) slot**", where the binding term is +εk² with ε>0 ("favors finer structure").
- Linearizing NS about rest gives a growth rate −νk² − α. Viscosity contributes a **negative**, stabilizing k² term, the opposite sign to +εk². The NWSH amplitude equation shown is expanded about the band centre k₀ of the **prescribed** forcing annulus, so k⋆ ≈ k₀ holds by construction, and L⋆ ∝ (σ/ε)^{1/2} ∝ 1/k₀ follows by dimensional analysis. The centre-manifold reduction is described but not performed.
- **Why it matters:** Pillar III's link to NS is the only place where "arrangement selects length" touches the NS equations. As written, the NS→SH step imports its answer from the forcing.
- **Fix:** perform the reduction explicitly, or downgrade the step to [H]. Name the physical source of +εk², for example the forcing's spectral structure or a negative-eddy-viscosity mechanism.

### F-8 (H) — The Newtonian regime is placed on opposite sides of the margin in §3 and §6
- §6: "**Far from the margin**, rearrangements are fast and local … and the closure holds; **as Δz→0** … the closure fails".
- §3 ladder: "Deep in the jammed phase (Δz large): finite G … an elastic/plastic solid"; "**At and just past the margin** (Δz→0⁺): … the Newtonian fluid is the leading … response".
- §3 also defines Δz ≡ z−2d **≥ 0**, so "just past the margin" (Δz<0) lies outside the defined domain. The §3 table adds: "Viscosity proxy diverges as Δz→0". A diverging ν at the margin, where fluidity is "established", gives Stokes flow or a yield-stress fluid, not NS with finite ν.
- **Why it matters:** the "fluidity theorem" (G→0 at the margin) and the Newtonian closure cannot both hold at the same Δz. The NS regime is not located, and the two pages locate it in opposite places.
- **Fix:** pick one side, most likely the unjammed side Δz<0, and extend the Δz axis to cover it. Reconcile it with the diverging viscosity. State that the margin gives G=0 but a non-Newtonian response.

### F-9 (M) — DNS results are relabelled NS phenomenology; they test NS, not the substrate. Grade mis-assigned.
- §9 and the hub: "The framework has **passed external tests** in developed turbulence". The 3-D flux concentration, strain alignment (corr ≈ 0.8), Lin–Wyart τ and Vassilicos C_ε ∝ Re_λ^{-1} all come from `ns3d.py`, a plain NS solver with no jammed or event content.
  - Strain-aligned forward flux and intermittent concentration are textbook NS results.
  - The C_ε ∝ Re_λ^{-1} law in decay from a forced state is Goto–Vassilicos's result.
  - Power-law size distributions of intense structures are known too (e.g. Moisy–Jiménez).
- Under the corpus rules these are **[V mech]**: an in-model reproduction of known NS behaviour. They are not **[V data]**, and the interpretation ("events = unjamming avalanches", "C_ε plateau = Π_L fixed point") is an [H] layered on top. No mapping from C_ε to Π_L is derived: §5's "event RG" is the monomial scaling of Π_L with arbitrary exponents (see F-13).
- **Fix:** replace "passed external tests" with "reproduced in NS DNS (in-model)". Grade the identification as [H]. Cite the prior literature.

### F-10 (M) — Avalanche exponent τ: the "trend into the band" is grid non-convergence at fixed Re, and the prediction partly uses the measured data
- §9: "τ = 1.60 ± 0.01 at N = 64 ⇒ τ = 1.46 ± 0.01 at N = 96 … along a clean finite-Reynolds trend … a **genuine prediction** (not a postdiction)".
- The drivers `dev64.py` and `embed96.py` both use **ν = 0.008**, the same physics. A 9% shift in τ between grids is therefore a **resolution effect**, not a Reynolds trend. The page calls the 3-D flux statistics "resolution-converged" at this ν, but τ is not.
- d_f is measured from the same fields and fed into the "pre-registered" relation, and θ ≈ 0.5–0.6 is a borrowed range. τ also depends on the threshold h.
- The shipped `dissipation_avalanche.py` `__main__` runs only an N=48 "validation", and its print statement refers to production numbers from "the N=64 run below", which does not exist in the file.
- **Fix:** report τ as not grid-converged. Add a ν-sweep at a converged k_max·η. Ship the production driver.

### F-11 (M) — The DP transition class is generic; the substrate contributes nothing specific
- §3: "the framework fixes the class **in advance, with no fluid input** … A hard problem, solved by others, lands exactly where the substrate says it must".
- Any local system with a single absorbing state and no extra symmetry is in the DP class (the Janssen–Grassberger conjecture). DP for the subcritical transition was proposed by Pomeau (1986). The substrate only supplies an absorbing state plus locality, so any model with those two features gives DP.
- **Fix:** cite Pomeau and Janssen–Grassberger. Present the result as consistency, not as a prediction specific to the substrate.

### F-12 (M) — The 3-D solver validation figures are not reproduced by the shipped code
- ax-o and §9: "conserves energy to machine precision (ΔE/E∼10⁻¹⁶) and divergence-freeness (∼10⁻¹⁴)".
- Running `ns3d.inviscid_energy_check()` as shipped (N=32, dt=0.01, 150 steps) gives **ΔE/E = 1.0×10⁻⁸** and **max|k·û| = 4.1×10⁻¹²**. RK4 time integration cannot conserve a quadratic invariant to machine precision. Only the semi-discrete right-hand side is energy-orthogonal.
- This conflicts with the ledger's C1 "displayed value == regenerated value (0 drift)" attestation in `IRREPRODUCIBILITY_LEDGER.md`.
- **Fix:** display the measured 1e-8 and 4e-12 values, or state that 1e-16 refers to the instantaneous u·(ω×u) orthogonality. Audit why the gate did not catch the mismatch.

### F-13 (M) — The "event RG" is a tautology, and the one-half exponent is dimensional
- §5: Π_L = L^{1+α} ε_bind/σ_eff, with d log Π_L / d log λ = (1+α) − ψ − χ. The event_rg.py check "PASS: Π_L exactly scale-invariant" iterates λ⁰ = 1.
- The exponents χ, ψ and α are never computed from the substrate. §8's 1/2 follows from [ε]/[σ] = L⁻², so any length built from these two quantities scales with exponent 1/2. Calling the fixed-point condition "the same statement" as the 1/2 law is asserted, not derived.
- **Fix:** grade the event RG as a definition or ansatz ([L]/[H]). Derive χ and ψ from the substrate, or declare them open.

### F-14 (M) — Seam to physics: the substrate model is substituted, and the light identification is re-imported by the hub
- The physics hub says "infinitely rigid, fully packing constituents frozen at random close packing … the vacuum behaves as an **elastic solid**". Fluid-dynamics §3 uses **harmonic soft spheres**, and its central mechanism ("the shear reserve is the overlap") needs finite overlaps, which infinitely rigid particles do not have. The substitution is not declared at the seam.
- Physics also calls the vacuum an elastic solid, while fluid-dynamics puts the same substrate at G=0, a fluid. No seam text reconciles the two.
- Fluid-dynamics §14 says: "We do **not import** the companion's speed-of-light identification". Its own hub says: "the same jammed-arrangement substrate **that fixes the speed of light there** fixes the form of fluid motion here".
- `seams.json` grades the physics edge **[F]** ("derived from the jammed-vacuum substrate"), yet §14 declares A0 "sufficient, not unique".
- **Fix:** declare the soft-sphere model as an [L] choice at the seam. Remove the speed-of-light sentence from the hub, or align it with §14. Downgrade the seam grade to match.

### F-15 (M) — Grade vocabulary is outside the corpus rules; the manifest shows zero grades
- The pages use [LOCK]/[DERIVE]/[GATE]. `_decl.json` and the manifest show `forced 0, verified 0, open 0, hypothesis 0`.
- [DERIVE] covers three different things: calculus results ([F]), solver checks and DNS phenomenology ([V mech]), and category agreement with experiments ([V data]-lite). §3's answer badge is **[GATE]** for the substrate result, while §14 lists the same result under "We **establish** … [DERIVE]".
- **Fix:** map every tag to [F]/[V mech]/[V data]/[L]/[O]/[H] per AGENTS.md §5 and regenerate the manifest grades. Make the §3 and §14 badges consistent.

### F-16 (M) — Hidden assumptions in the viscosity-sign argument
- §6: "μ ≥ 0 … (a Green–Kubo integral of a stress autocorrelation, which is nonnegative) … its sign is forced [DERIVE]".
- Green–Kubo needs an equilibrium, stationary, ergodic thermal state. The substrate in §3 is athermal (harmonic packings, "athermal stress relaxation") and driven (G-SOC), and Green–Kubo is not established for it.
- **Fix:** grade the result as conditional on equilibrium linear response, or derive μ ≥ 0 from the metriplectic positive semidefiniteness of §9 instead.

### F-17 (L) — Minor technical slip in the "identity" chain
- §6 splits v_i = u(x_i) + c_i. The exact kinetic-stress identity with a finite-width kernel needs peculiar velocities relative to **u(x)**, evaluated at the field point, because Σ m_i (v_i − u(x)) W(x−x_i) = 0. With u(x_i) the convective term is not exactly ρu⊗u. This matters because the text says "Every step is an identity".
- **Fix:** use v_i − u(x).

### F-18 (L) — Headline wording overstates the input: "a single measured structure"
- §01: "One thesis, forced four ways from a **single measured structure**". §01 body: "we **posit** an arrangement". §14: "A0 is a sufficient model".
- The arrangement is posited. Marginality is measured in a chosen simulation model.
- **Fix:** "from one posited arrangement (A0), whose marginality is measured in simulation".

### F-19 (L) — Inheritance label: "Inherits: R19 switch"
- The fluid-dynamics hub shows "Inherits: R19 switch". Per AGENTS.md and the physics hub, R19 is first stated in `dna`, which lies **downstream** of fluid-dynamics. `_decl.json` says `inherits_modules: ["kernel"]`, and no page body uses R19.
- **Fix:** change the hub label to the substrate kernel (c² = B/ρ).

### F-20 (L) — Reproducibility hygiene
- `06-.../validate_all.py` cannot run standalone: it imports `metriplectic_vortex` from the §9 folder.
- The 3-D "converged" figures depend on drivers (`run3d.py`, `dev64.py`, `embed96.py`) that the page describes only in prose.

### F-21 (L) — LaTeX leaks in rendered pages
- "Section~\ref{sec:thesis}" (§01, many times); "\S§3" (§3, §9, §14); "\emph{not}" (§14 heading); "\vspace{1em} \rule… \end{document}" (ax-x); a stray ")}" (ax-d, ax-o); "$Pi$" in the §5 title; "Thetaσ" (§4 description); "Rey_λ" (§9 description).

### F-22 (L) — Undeclared imports despite "without external citation, by design" (ax-x)
- Irving–Kirkwood, Maxwell counting, Green–Kubo, the GENERIC/metriplectic formalism, Kelvin impulse, Newell–Whitehead–Swift–Hohenberg, Duchon–Robert, the Germano filter, Clauset–Shalizi–Newman, Lin–Wyart, Goto–Vassilicos, Pomeau/DP and the Onsager conjecture are all used by name without references. This conflicts with the corpus rule of "no silent borrowing" (AGENTS.md §3.2 rule 5).
- **Fix:** add a references appendix. Mark each such result as imported rather than derived.

---

## 2. Logic chain, summarized

```
A0 (posited jammed arrangement)
 └─ §3 soft-sphere margin: G_rel→0, B finite       [V mech, local sim]  — seam to physics (rigid, elastic solid) undeclared (F-14)
     └─ fluidity "at margin" — but viscosity diverges there; Newtonian regime located oppositely in §3 vs §6 (F-8)
 └─ §4 No-Go → U3 forced                            conditional on Newtonian 2nd-order dynamics (F-5); theorems unshown
     └─ NOT used by Pillar I (pair-force IK only; spin ⇒ micropolar, not NS) (F-4)
 └─ §6 balance laws (IK)                            [F] but generic to any particle system
     └─ NS = Newtonian closure                      [GATE] not passed (F-1, F-2)
         └─ 3-D regularity                          nothing proved; "recast" has no reduction (F-3)
 └─ §8 NS → SH normal form                          sign error; k⋆ from forcing (F-7)
 └─ §9 anomaly as channel migration                 assumed (b>0); contradicts NS ε=2νZ (F-6)
     └─ 2-D/3-D DNS, τ, C_ε                         standard NS phenomenology, [V mech]; τ not grid-converged (F-9, F-10, F-12)
```

## 3. Recommended wording for the author's summary
Replace "solved the Navier–Stokes equations" with something like: *"The volume shows that continuum balance laws are exact bookkeeping identities of a particle arrangement, and that Navier–Stokes follows **if** a Newtonian-closure gate passes (not yet tested). It reproduces standard 2-D/3-D NS turbulence phenomenology numerically and offers a configurational interpretation of it. It makes **no** claim on NS existence or smoothness (the Clay problem)."*
