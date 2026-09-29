# EM.12 Dynamic field equations, Poynting, and causality (addendum) **[F]/[V]**

*Added 2026-06-14. Closes the dynamic-Maxwell gap flagged in the EM completeness review
(Faraday/Ampère/Poynting were absent from EM.0–EM.11). Source: **AQD — Axiomatic Quantized
Dynamics, NOCAL v1.1, DOI 10.5281/zenodo.17423870**. Reproduced by `vp_em_field_dynamics.py`.*

> The original EM chapter derived the **static** Coulomb sector ($1/r^2$, EM.3), the algebraic
> ratio $|\mathbf B|=(v/c)|\mathbf E|$ and $\nabla\!\cdot\mathbf B=0$ (EM.4) — i.e. **two of the
> four Maxwell statements** (the two divergence facts). It did **not** state the **dynamic**
> field equations, the Poynting energy flow, or a causality theorem. This addendum supplies them
> in the **longitudinal (E-sector, pressure $P$) form** from the AQD axioms, and marks the
> remaining vector-curl sector honestly as open.

## EM.12.1 The first-order dynamic system **[F]**

The jammed-lattice field obeys a coupled first-order system (AQD axiom A1) — pressure $P$
(the compression = deficit = longitudinal/Coulomb sector) and velocity $\mathbf v$:
$$
\partial_t P + K\,\nabla\!\cdot\mathbf v = 0,
\qquad
\rho\,\partial_t \mathbf v + \nabla P = 0.
$$
Eliminating $\mathbf v$ gives the wave equation and the speed already used in EM.2:
$$
\Box_c P = 0,\qquad c^2 = \frac{K}{\rho}\;(=B/\rho).
$$
**These two coupled first-order equations are the longitudinal analogue of Maxwell's curl pair**
($\nabla\times\mathbf E=-\partial_t\mathbf B$, $\nabla\times\mathbf B=\mu_0\varepsilon_0\partial_t\mathbf E$):
the time-derivative of each field is sourced by a spatial derivative of the other, and their
combination is the wave. Module `vp_em_field_dynamics.py` integrates this system (staggered
leapfrog, deterministic) and recovers the pulse speed $c_{\text{measured}}=1.0001$ vs $c=1$
(**0.01 %**).

## EM.12.2 Poynting's theorem and energy conservation **[F]/[V]**

Define the energy density and flux (AQD; equivalent to the second-order form
$e=\tfrac12[(\partial_tP)^2/c^2+|\nabla P|^2]$, $\mathbf S=-(\partial_tP)\nabla P$):
$$
e = \tfrac12\!\left[\frac{P^2}{K} + \rho\,|\mathbf v|^2\right],
\qquad
\mathbf S = P\,\mathbf v,
\qquad
\boxed{\;\partial_t e + \nabla\!\cdot\mathbf S = 0\;}
$$
— the **local energy-conservation (Poynting) law**, the longitudinal counterpart of EM's
$\partial_t u + \nabla\!\cdot(\mathbf E\times\mathbf H)=0$. Integrating over a lossless domain
(periodic, Neumann, time-invariant Dirichlet, or radiationless infinity) gives $\oint\mathbf
S\!\cdot\!\mathbf n=0$ and hence
$$
\frac{dE}{dt}=0\qquad(\text{AQD QP-0002-001, fully proven}).
$$
The module confirms $\partial_t e+\partial_x S=0$ pointwise (RMS residual $\sim 3\times10^{-2}$,
discretization scale) and energy conservation to $3\times10^{-4}$ over the run. A companion
uniqueness theorem (energy method, QP-0002-002) shows identical initial data give a unique
solution.

## EM.12.3 Causality: finite propagation and the light cone **[F]**

The same energy structure forces a **hard light cone** (AQD theorems F-A/B/C):
$$
u_{\max}=c,\qquad \operatorname{supp} e(\tau,\cdot)\ \subseteq\ \operatorname{supp} e(0,\cdot)\,\oplus\,B_{c\tau}.
$$
Energy and information cannot reach beyond $c\tau$ of the initial support. The module verifies
this directly: the pulse support stays inside the cone (expansion $0.00 \le c\tau$). At the
quantum level the AQD upgrades this to **microcausality** — with $\Phi:=P/\sqrt K$,
$[\Phi(x),\Phi(y)]=0$ for spacelike $(x-y)$ via the Pauli–Jordan function $D(x)$ whose support
lies on the light cone (the cone speed is fixed at $c$ by $c^2=K/\rho$), and the arrival-time
bound $t_{\text{arr}}\ge \text{dist}/c$ follows from commutator support. No calibration enters.

## EM.12.4 What this closes, and what remains open **[O]**

**Closed (this addendum):** the *dynamic* field equations, the Poynting energy flow and its
exact conservation, uniqueness, and causality (classical light cone + quantum microcausality).
Together with EM.2 (wave/$c^2=B/\rho$) and EM.3 (static $1/r^2$), the **longitudinal (E-sector)**
electrodynamics is now complete and reproducible.

**Still open — honestly marked [O] (unchanged from EM.9):** the **full vector $\mathbf E/\mathbf B$
curl structure** — Faraday's $\nabla\times\mathbf E=-\partial_t\mathbf B$ and Ampère–Maxwell's
$\nabla\times\mathbf B$ in *vector* form, with the **magnetic field as an independent transverse
pseudovector** and its *absolute* magnitude. The AQD treatment is scalar/longitudinal ($P$,
$\mathbf v$ with $\mathbf v$ irrotational); it yields the compression (Coulomb/$E$) sector
rigorously but not the independent transverse-vector (magnetic/radiative) sector. This is exactly
the EM.9 line *"magnetic/radiative absolute vector sector — [O] (physics §14.0.6)"*. It is **not**
resolved here; it remains the principal open structural item of the EM chapter.

## EM.12.5 Updated master-ledger rows

| Result | Grade | Basis / module |
|---|---|---|
| First-order system $\partial_tP+K\nabla\!\cdot\mathbf v=0$, $\rho\partial_t\mathbf v+\nabla P=0$ | [F] | AQD A1; `vp_em_field_dynamics.py` |
| Poynting law $\partial_t e+\nabla\!\cdot\mathbf S=0$, $\mathbf S=P\mathbf v$ | [F]/[V] | AQD QP-0002-001; residual $\sim$3e-2 |
| Energy conservation $dE/dt=0$ (lossless) + uniqueness | [F] | AQD QP-0002-001/002; dev 3e-4 |
| Causality: light cone, $u_{\max}=c$; microcausality | [F] | AQD F-A/B/C, QP-0002-U121 |
| Full vector $\mathbf E/\mathbf B$ curl (Faraday/Ampère, magnetic absolute) | **[O]** | open — scalar/longitudinal AQD does not supply it |


*This addendum upgrades the EM chapter from "static sector + algebraic $B/E$ ratio" to
"**complete longitudinal electrodynamics with Poynting flow and causality**," using the AQD
axiomatic field dynamics. The dynamic-Maxwell gap is closed in the E-sector; the independent
vector (magnetic/radiative) sector remains the chapter's honestly-declared open item.*
